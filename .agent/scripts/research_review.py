#!/usr/bin/env python3
import argparse
import contextlib
import io
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from agent_mail import cmd_post


REPO_ROOT = Path(__file__).resolve().parents[2]
SYSTEM_RESEARCH_BOARD = REPO_ROOT / "System" / "Synapse_Board" / "LORE_RESEARCH_BOARD.md"
ARCHIVE_RESEARCH_BOARD = REPO_ROOT / "docs" / "Archiv" / "Research_Board.md"
RESEARCH_REVIEW_REGISTER = REPO_ROOT / "Logs" / "Reviews" / "RESEARCH_REVIEW_REGISTER.md"
DISPATCH_RELATIVE_REGISTER = "Logs/Reviews/RESEARCH_REVIEW_REGISTER.md"

ACTIVE_ROW_RE = re.compile(
    r"^\| \[\[(RESEARCH-\d{4}-\d{3})\]\] \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$"
)
ARCHIVED_ROW_RE = re.compile(
    r"^\| \[\[(RESEARCH-\d{4}-\d{3})\]\] \| (.*?) \| (.*?) \| (.*?) \|$"
)
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)
STATUS_SECTION_RE = re.compile(r"(?ms)^## Status\n.*?(?=^## |\n---\n|\Z)")
REVIEW_SECTION_RE = re.compile(r"(?ms)^## Review-Stand\n.*?(?=^## |\n---\n|\Z)")


@dataclass
class ReviewCandidate:
    research_id: str
    title: str
    priority: str
    status: str
    focus: str


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def today_date() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def save_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def list_review_candidates() -> list[ReviewCandidate]:
    content = load_text(SYSTEM_RESEARCH_BOARD)
    candidates: list[ReviewCandidate] = []
    for line in content.splitlines():
        match = ACTIVE_ROW_RE.match(line.strip())
        if not match:
            continue
        research_id, title, priority, status, focus = match.groups()
        normalized_status = status.upper()
        if normalized_status not in {"IN_REVIEW_HISTORIAN", "AWAITING_HUMAN_DECISION"}:
            continue
        candidates.append(
            ReviewCandidate(
                research_id=research_id,
                title=title,
                priority=priority,
                status=status,
                focus=focus,
            )
        )
    return candidates


def capture_dispatch_post(from_agent: str, to_agent: str, subject: str, body: str) -> str | None:
    args = argparse.Namespace(
        from_agent=from_agent,
        to_agent=to_agent,
        subject=subject,
        body=body,
        report_path=DISPATCH_RELATIVE_REGISTER,
        priority="NORMAL",
    )
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = cmd_post(args)
    if rc != 0:
        return None
    output = buf.getvalue().strip()
    if output:
        print(output)
        return output.split(" ", 1)[0]
    return None


def ensure_review_register() -> None:
    if RESEARCH_REVIEW_REGISTER.exists():
        return
    save_text(
        RESEARCH_REVIEW_REGISTER,
        "\n".join(
            [
                "---",
                "uuid: research-review-register-2026",
                "status: ACTIVE",
                f"updated_at: {now_iso()}",
                "epistemic: \"#meta\"",
                "---",
                "",
                "# RESEARCH_REVIEW_REGISTER",
                "",
                "Zentrales Review-Register fuer Forschungsfreigaben, Rueckgaben und fachliche Kommentare.",
                "",
                "## Eintraege",
                "",
            ]
        )
        + "\n",
    )


def append_review_register(
    research_id: str,
    reviewer: str,
    role: str,
    decision: str,
    note: str,
    dispatch_ref: str | None,
) -> None:
    ensure_review_register()
    content = load_text(RESEARCH_REVIEW_REGISTER).rstrip()
    entry = "\n".join(
        [
            f"### {today_date()} - {research_id}",
            "",
            f"- Zeitpunkt: `{now_iso()}`",
            f"- Research: `{research_id}`",
            f"- Reviewer: `{reviewer}`",
            f"- Rolle: `{role}`",
            f"- Entscheidung: `{decision}`",
            f"- Kurzbegruendung: {note}",
            f"- Dispatch: `{dispatch_ref or 'N/A'}`",
            "",
        ]
    )
    save_text(RESEARCH_REVIEW_REGISTER, content + "\n\n" + entry)


def summarize_public_note(note: str) -> str:
    clean = " ".join(note.strip().split())
    if len(clean) <= 180:
        return clean
    return clean[:177].rstrip() + "..."


def archive_page_path(research_id: str) -> Path:
    return REPO_ROOT / "docs" / "Archiv" / f"{research_id}.md"


def update_frontmatter_status(raw: str, new_status: str) -> str:
    match = FRONTMATTER_RE.search(raw)
    if not match:
        return raw
    lines = match.group(1).splitlines()
    replaced = False
    for i, line in enumerate(lines):
        if line.startswith("status:"):
            lines[i] = f"status: {new_status}"
            replaced = True
        elif line.startswith("letzter_check:"):
            lines[i] = f"letzter_check: {today_date()}"
    if not replaced:
        lines.append(f"status: {new_status}")
    frontmatter = "---\n" + "\n".join(lines) + "\n---\n"
    return raw[: match.start()] + frontmatter + raw[match.end() :]


def update_archive_page(
    research_id: str,
    decision: str,
    reviewer: str,
    role: str,
    note: str,
    dispatch_ref: str | None,
) -> None:
    path = archive_page_path(research_id)
    raw = load_text(path)
    if decision == "approved":
        status_frontmatter = "resolved"
        status_text = f"## Status\n**Historisch geklaert.** Menschliche Freigabe erteilt am {today_date()} durch `{reviewer}`."
    elif decision == "returned":
        status_frontmatter = "open_historian"
        status_text = f"## Status\n**Fachlich offen.** Nach menschlichem Review vom {today_date()} zur weiteren Historian-Synthese zurueckgegeben."
    else:
        status_frontmatter = "in_review_historian"
        status_text = "## Status\n**Fachlich offen.** Historian-Gutachten liegt vor; finale Freigabe oder weitere Synthese steht aus."

    public_note = summarize_public_note(note)
    review_text = "\n".join(
        [
            "## Review-Stand",
            f"- Letzte Entscheidung: `{decision}`",
            f"- Reviewer: `{reviewer}`",
            f"- Rolle: `{role}`",
            f"- Datum: `{today_date()}`",
            f"- Oeffentliche Notiz: {public_note}",
            f"- Dispatch-Referenz: `{dispatch_ref or 'N/A'}`",
        ]
    )

    if STATUS_SECTION_RE.search(raw):
        raw = STATUS_SECTION_RE.sub(status_text, raw, count=1)
    else:
        raw += "\n\n" + status_text + "\n"

    if REVIEW_SECTION_RE.search(raw):
        raw = REVIEW_SECTION_RE.sub(review_text, raw, count=1)
    else:
        insertion = "\n\n" + review_text + "\n"
        marker = "\n---\n"
        if marker in raw:
            raw = raw.replace(marker, insertion + marker, 1)
        else:
            raw = raw.rstrip() + insertion

    raw = update_frontmatter_status(raw, status_frontmatter)
    save_text(path, raw)


def move_or_update_board_row(board_path: Path, research_id: str, decision: str) -> None:
    lines = load_text(board_path).splitlines()
    active_idx = None
    active_match = None
    archived_idx = None
    for idx, line in enumerate(lines):
        active = ACTIVE_ROW_RE.match(line.strip())
        if active and active.group(1) == research_id:
            active_idx = idx
            active_match = active
        archived = ARCHIVED_ROW_RE.match(line.strip())
        if archived and archived.group(1) == research_id:
            archived_idx = idx

    if active_match is None and archived_idx is None:
        return

    if decision == "commented":
        save_text(board_path, "\n".join(lines) + "\n")
        return

    if decision == "returned" and active_match is not None:
        research_id, title, priority, _status, focus = active_match.groups()
        lines[active_idx] = f"| [[{research_id}]] | {title} | {priority} | OPEN_HISTORIAN | {focus} |"
        save_text(board_path, "\n".join(lines) + "\n")
        return

    if decision == "approved" and active_match is not None:
        research_id, title, _priority, _status, _focus = active_match.groups()
        del lines[active_idx]
        archive_row = f"| [[{research_id}]] | {title} | RESOLVED | [[{research_id}]] |"
        insert_idx = None
        for idx, line in enumerate(lines):
            if line.strip().startswith("| ID | Gegenstand | Status | Ergebnis / Bericht |"):
                insert_idx = idx + 2
                break
        if archived_idx is not None:
            lines[archived_idx] = archive_row
        elif insert_idx is not None:
            lines.insert(insert_idx, archive_row)
        save_text(board_path, "\n".join(lines) + "\n")
        return


def maybe_update_system_ticket(research_id: str, new_status: str) -> None:
    path = REPO_ROOT / "System" / "Synapse_Board" / f"{research_id}.md"
    if not path.exists():
        return
    raw = load_text(path)
    match = FRONTMATTER_RE.search(raw)
    if not match:
        return
    lines = match.group(1).splitlines()
    for i, line in enumerate(lines):
        if line.startswith("status:"):
            lines[i] = f"status: {new_status}"
    frontmatter = "---\n" + "\n".join(lines) + "\n---\n"
    raw = raw[: match.start()] + frontmatter + raw[match.end() :]
    save_text(path, raw)


def apply_review_action(research_id: str, decision: str, reviewer: str, role: str, note: str) -> int:
    candidates = {candidate.research_id for candidate in list_review_candidates()}
    if research_id not in candidates and decision != "commented":
        print(f"{research_id} ist derzeit nicht im REVIEW-Status.")
        return 1

    dispatch_subject = f"Research review: {research_id} {decision}"
    dispatch_body = (
        f"Review-Entscheidung fuer {research_id}: {decision}. Reviewer: {reviewer} ({role}). "
        f"Notiz: {note}"
    )
    dispatch_ref = capture_dispatch_post(role.split("_", 1)[0].title(), "Coordinator", dispatch_subject, dispatch_body)
    append_review_register(research_id, reviewer, role, decision, note, dispatch_ref)
    update_archive_page(research_id, decision, reviewer, role, note, dispatch_ref)
    move_or_update_board_row(SYSTEM_RESEARCH_BOARD, research_id, decision)
    move_or_update_board_row(ARCHIVE_RESEARCH_BOARD, research_id, decision)
    if decision == "approved":
        maybe_update_system_ticket(research_id, "RESOLVED")
    elif decision == "returned":
        maybe_update_system_ticket(research_id, "OPEN_HISTORIAN")
    print(f"{research_id}: {decision} durch {reviewer} ({role})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Research review and approval helper")
    parser.add_argument("--list", action="store_true", help="List research review candidates")
    parser.add_argument("--research-id", help="Research ID, e.g. RESEARCH-2026-004")
    parser.add_argument("--decision", choices=["approved", "returned", "commented"])
    parser.add_argument("--reviewer")
    parser.add_argument("--role", choices=["human_final", "historian_comment", "coordinator_note"])
    parser.add_argument("--note")
    args = parser.parse_args()

    if args.list:
        candidates = list_review_candidates()
        if not candidates:
            print("Keine Research-Auftraege im REVIEW-Status.")
            return 0
        for candidate in candidates:
            print(
                f"{candidate.research_id} | {candidate.status} | {candidate.title} | "
                f"{candidate.priority} | {candidate.focus}"
            )
        return 0

    if not all([args.research_id, args.decision, args.reviewer, args.role, args.note]):
        parser.error("Fuer Review-Aktionen sind --research-id, --decision, --reviewer, --role und --note erforderlich.")

    if args.role != "human_final" and args.decision in {"approved", "returned"}:
        parser.error("Nur human_final darf Forschung final freigeben oder zur Nacharbeit zurueckgeben.")

    return apply_review_action(args.research_id, args.decision, args.reviewer, args.role, args.note)


if __name__ == "__main__":
    raise SystemExit(main())
