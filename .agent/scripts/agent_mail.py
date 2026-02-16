#!/usr/bin/env python3
import argparse
import datetime as dt
import re
import uuid
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
MAIL_ROOT = REPO_ROOT / "System" / "Synapse_Board" / "DISPATCH"
QUEUE_DIR = MAIL_ROOT
MSG_ID_RE = re.compile(r"^MSG-\d{4}-\d{4}$")


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


def _validate_message_id(message_id: str) -> None:
    if not MSG_ID_RE.match(message_id):
        raise ValueError(f"Ungueltige Message-ID: {message_id} (erwartet: MSG-YYYY-NNNN)")


def resolve_message_path(message_id: str) -> Path | None:
    _validate_message_id(message_id)
    matches: list[Path] = []
    for path in all_messages():
        raw = path.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(raw)
        if meta.get("id") == message_id:
            matches.append(path)
    if len(matches) > 1:
        raise ValueError(f"Mehrdeutige Message-ID {message_id}: {len(matches)} Treffer.")
    return matches[0] if matches else None


def append_verlauf(body: str, line: str) -> str:
    out = body
    if "## Verlauf" not in out:
        out = out.rstrip() + "\n\n## Verlauf\n\n"
    if not out.endswith("\n"):
        out += "\n"
    out += f"- {line}\n"
    return out


def cmd_post(args: argparse.Namespace) -> int:
    ensure_dirs()
    subject_slug = slugify(args.subject)

    # Collision-safe creation under concurrent runs.
    for _ in range(20):
        msg_id = next_id()
        lock_path = QUEUE_DIR / f".{msg_id}.lock"
        try:
            with lock_path.open("x", encoding="utf-8"):
                pass
        except FileExistsError:
            continue

        try:
            if resolve_message_path(msg_id) is not None:
                continue

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
            with path.open("x", encoding="utf-8") as f:
                f.write(render_frontmatter(meta, body))
            print(f"{msg_id} -> {path.relative_to(REPO_ROOT)}")
            return 0
        except FileExistsError:
            continue
        finally:
            lock_path.unlink(missing_ok=True)

    print("Konnte keine neue Message-ID kollisionsfrei vergeben.")
    return 1


def cmd_inbox(args: argparse.Namespace) -> int:
    found = 0
    for path in all_messages():
        raw = path.read_text(encoding="utf-8")
        meta, _ = parse_frontmatter(raw)
        to_agent = meta.get("to_agent", "")
        status = meta.get("status", "")
        if args.agent and args.agent.lower() not in {to_agent.lower(), "all"}:
            continue
        if args.status and status != args.status:
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
    try:
        target = resolve_message_path(args.id)
    except ValueError as e:
        print(str(e))
        return 1
    if not target:
        print(f"Nachricht nicht gefunden: {args.id}")
        return 1
    print(target.read_text(encoding="utf-8"))
    return 0


def _mutate_status(message_id: str, updater) -> int:
    try:
        target = resolve_message_path(message_id)
    except ValueError as e:
        print(str(e))
        return 1
    if not target:
        print(f"Nachricht nicht gefunden: {message_id}")
        return 1
    raw = target.read_text(encoding="utf-8")
    meta, body = parse_frontmatter(raw)
    try:
        new_body = updater(meta, body)
        if new_body is not None:
            body = new_body
    except ValueError as e:
        print(str(e))
        return 1
    target.write_text(render_frontmatter(meta, body), encoding="utf-8")
    print(f"Aktualisiert: {target.relative_to(REPO_ROOT)}")
    return 0


def cmd_claim(args: argparse.Namespace) -> int:
    def update(meta, body):
        status = meta.get("status", "")
        if status == "DONE":
            raise ValueError("CLAIM nicht moeglich: Nachricht ist bereits DONE.")
        if status == "CLAIMED":
            if meta.get("claimed_by") == args.agent:
                return body  # idempotent
            raise ValueError(
                f"CLAIM nicht moeglich: Bereits von {meta.get('claimed_by','?')} geclaimt."
            )
        if status != "OPEN":
            raise ValueError(f"CLAIM nur aus OPEN erlaubt (aktuell: {status or 'UNSET'}).")
        meta["status"] = "CLAIMED"
        meta["claimed_by"] = args.agent
        meta["claimed_at"] = now_iso()
        return append_verlauf(body, f"CLAIMED ({args.agent}): Nachricht uebernommen.")

    return _mutate_status(args.id, update)


def cmd_done(args: argparse.Namespace) -> int:
    def update(meta, body):
        status = meta.get("status", "")
        if status == "DONE":
            if meta.get("completed_by") == args.agent:
                return body  # idempotent
            raise ValueError("DONE nicht moeglich: Nachricht ist bereits abgeschlossen.")
        if status != "CLAIMED":
            raise ValueError(f"DONE nur aus CLAIMED erlaubt (aktuell: {status or 'UNSET'}).")
        claimer = meta.get("claimed_by", "")
        if not claimer:
            raise ValueError("DONE blockiert: Nachricht ist CLAIMED ohne claimed_by.")
        if claimer != args.agent:
            raise ValueError(f"DONE nur durch claimer erlaubt (claimed_by={claimer}).")
        meta["status"] = "DONE"
        meta["completed_by"] = args.agent
        meta["completed_at"] = now_iso()
        note = args.note.strip() if args.note else "Abgeschlossen."
        return append_verlauf(body, f"DONE ({args.agent}): {note}")

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
    inbox.add_argument("--status", choices=["OPEN", "CLAIMED", "DONE"], type=str.upper)
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
