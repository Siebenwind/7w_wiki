#!/usr/bin/env python3
import argparse
import datetime as dt
import re
import uuid
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MAIL_ROOT = REPO_ROOT / "System" / "Synapse_Board" / "DISPATCH"
QUEUE_DIR = MAIL_ROOT


def now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def ensure_dirs() -> None:
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return re.sub(r"_+", "_", text).strip("_")[:60] or "nachricht"


def parse_frontmatter(raw: str) -> tuple[dict[str, str], str]:
    if not raw.startswith("---\n"):
        return {}, raw
    end = raw.find("\n---\n", 4)
    if end == -1:
        return {}, raw
    head = raw[4:end].splitlines()
    body = raw[end + 5 :]
    data: dict[str, str] = {}
    for line in head:
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        data[k.strip()] = v.strip()
    return data, body


def render_frontmatter(meta: dict[str, str], body: str) -> str:
    lines = ["---"]
    for key in [
        "id",
        "uuid",
        "status",
        "priority",
        "from_agent",
        "to_agent",
        "created_at",
        "claimed_by",
        "claimed_at",
        "completed_by",
        "completed_at",
        "subject",
    ]:
        lines.append(f"{key}: {meta.get(key, '')}")
    lines.append("---")
    lines.append("")
    return "\n".join(lines) + body


def all_messages() -> list[Path]:
    ensure_dirs()
    return sorted(QUEUE_DIR.glob("MSG-*.md"))


def next_id() -> str:
    year = dt.datetime.now(dt.timezone.utc).year
    prefix = f"MSG-{year}-"
    nums = []
    for path in all_messages():
        m = re.match(rf"{re.escape(prefix)}(\d{{4}})", path.stem)
        if m:
            nums.append(int(m.group(1)))
    nxt = max(nums, default=0) + 1
    return f"{prefix}{nxt:04d}"


def find_by_id(message_id: str) -> Path | None:
    path = QUEUE_DIR / f"{message_id}.md"
    if path.exists():
        return path
    return None


def cmd_post(args: argparse.Namespace) -> int:
    ensure_dirs()
    msg_id = next_id()
    subject_slug = slugify(args.subject)
    path = QUEUE_DIR / f"{msg_id}_{subject_slug}.md"
    meta = {
        "id": msg_id,
        "uuid": str(uuid.uuid4()),
        "status": "OPEN",
        "priority": args.priority.upper(),
        "from_agent": args.from_agent,
        "to_agent": args.to_agent,
        "created_at": now_iso(),
        "claimed_by": "",
        "claimed_at": "",
        "completed_by": "",
        "completed_at": "",
        "subject": args.subject,
    }
    body = "\n".join(
        [
            f"# {args.subject}",
            "",
            "## Auftrag",
            "",
            args.body.strip(),
            "",
            "## Verlauf",
            "",
            "- OPEN: Nachricht erstellt.",
            "",
        ]
    )
    path.write_text(render_frontmatter(meta, body), encoding="utf-8")
    print(f"{msg_id} -> {path.relative_to(REPO_ROOT)}")
    return 0


def cmd_inbox(args: argparse.Namespace) -> int:
    found = 0
    for path in all_messages():
        raw = path.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(raw)
        to_agent = meta.get("to_agent", "")
        status = meta.get("status", "")
        if args.agent and args.agent not in (to_agent, "ALL"):
            continue
        if args.status and status != args.status.upper():
            continue
        found += 1
        print(
            f"{meta.get('id','?')} | {status} | {meta.get('priority','')} | "
            f"to={to_agent} | from={meta.get('from_agent','')} | {meta.get('subject','')}"
        )
    if found == 0:
        print("Keine Nachrichten gefunden.")
    return 0


def cmd_read(args: argparse.Namespace) -> int:
    target = None
    for path in all_messages():
        if path.stem.startswith(args.id):
            target = path
            break
    if not target:
        print(f"Nachricht nicht gefunden: {args.id}")
        return 1
    print(target.read_text(encoding="utf-8"))
    return 0


def _mutate_status(message_id: str, updater) -> int:
    target = None
    for path in all_messages():
        if path.stem.startswith(message_id):
            target = path
            break
    if not target:
        print(f"Nachricht nicht gefunden: {message_id}")
        return 1
    raw = target.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(raw)
    updater(meta, body)
    target.write_text(render_frontmatter(meta, body), encoding="utf-8")
    print(f"Aktualisiert: {target.relative_to(REPO_ROOT)}")
    return 0


def cmd_claim(args: argparse.Namespace) -> int:
    def update(meta, _body):
        meta["status"] = "CLAIMED"
        meta["claimed_by"] = args.agent
        meta["claimed_at"] = now_iso()

    return _mutate_status(args.id, update)


def cmd_done(args: argparse.Namespace) -> int:
    def update(meta, body):
        meta["status"] = "DONE"
        meta["completed_by"] = args.agent
        meta["completed_at"] = now_iso()
        note = args.note.strip() if args.note else "Abgeschlossen."
        body += f"- DONE ({args.agent}): {note}\n"

    return _mutate_status(args.id, update)


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Agent messaging queue")
    sub = p.add_subparsers(dest="cmd", required=True)

    post = sub.add_parser("post", help="Create new message")
    post.add_argument("--from", dest="from_agent", required=True)
    post.add_argument("--to", dest="to_agent", required=True)
    post.add_argument("--subject", required=True)
    post.add_argument("--body", required=True)
    post.add_argument("--priority", default="NORMAL", choices=["LOW", "NORMAL", "HIGH"])
    post.set_defaults(fn=cmd_post)

    inbox = sub.add_parser("inbox", help="List messages")
    inbox.add_argument("--agent")
    inbox.add_argument("--status")
    inbox.set_defaults(fn=cmd_inbox)

    read = sub.add_parser("read", help="Read a message")
    read.add_argument("id")
    read.set_defaults(fn=cmd_read)

    claim = sub.add_parser("claim", help="Claim a message")
    claim.add_argument("id")
    claim.add_argument("--agent", required=True)
    claim.set_defaults(fn=cmd_claim)

    done = sub.add_parser("done", help="Mark message as done")
    done.add_argument("id")
    done.add_argument("--agent", required=True)
    done.add_argument("--note")
    done.set_defaults(fn=cmd_done)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    raise SystemExit(main())
