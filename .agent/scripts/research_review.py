#!/usr/bin/env python3
import argparse
import contextlib
import io
import json
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
SECTION_END_RE = r"(?=^#{1,6}\s|\n---\n|\Z)"
STATUS_SECTION_RE = re.compile(rf"(?ms)^## Status\n.*?{SECTION_END_RE}")
REVIEW_SECTION_RE = re.compile(rf"(?ms)^## Review-Stand\n.*?{SECTION_END_RE}")


@dataclass
class ReviewCandidate:
    research_id: str
    title: str
    priority: str
    status: str
    focus: str

    def as_dict(self) -> dict:
        return {
            "research_id": self.research_id,
            "title": self.title,
            "priority": self.priority,
            "status": self.status,
            "focus": self.focus,
            "system_path": rel_path(system_ticket_path(self.research_id)),
            "archive_path": rel_path(archive_page_path(self.research_id)),
            "summary_path": rel_path(summary_path(self.research_id)),
        }


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def today_date() -> str:
    return datetime.now(timezone.utc).date().isoformat()


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def save_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def rel_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def system_ticket_path(research_id: str) -> Path:
    return REPO_ROOT / "System" / "Synapse_Board" / f"{research_id}.md"


def summary_path(research_id: str) -> Path:
    return REPO_ROOT / "Logs" / "Research" / f"{research_id}_Summary.md"


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


def extract_section(raw: str, heading: str) -> str:
    pattern = re.compile(rf"(?ms)^## {re.escape(heading)}\n(.*?){SECTION_END_RE}")
    match = pattern.search(raw)
    if not match:
        return ""
    return match.group(1).strip()


def extract_frontmatter(raw: str) -> dict:
    match = FRONTMATTER_RE.search(raw)
    if not match:
        return {}
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip('"')
    return data


def make_review_dossier(research_id: str) -> dict:
    candidates = {candidate.research_id: candidate for candidate in list_review_candidates()}
    candidate = candidates.get(research_id)
    system_path = system_ticket_path(research_id)
    archive_path = archive_page_path(research_id)
    summary = summary_path(research_id)

    dossier = {
        "research_id": research_id,
        "status": "review_candidate" if candidate else "not_in_review_queue",
        "candidate": candidate.as_dict() if candidate else None,
        "paths": {
            "system_ticket": rel_path(system_path),
            "archive_page": rel_path(archive_path),
            "summary": rel_path(summary),
            "review_register": rel_path(RESEARCH_REVIEW_REGISTER),
        },
        "exists": {
            "system_ticket": system_path.exists(),
            "archive_page": archive_path.exists(),
            "summary": summary.exists(),
        },
        "frontmatter": {},
        "status_section": "",
        "review_section": "",
        "summary_preview": "",
        "required_actions": [],
        "recommended_decisions": [],
    }

    if archive_path.exists():
        raw = load_text(archive_path)
        dossier["frontmatter"] = extract_frontmatter(raw)
        dossier["status_section"] = extract_section(raw, "Status")
        dossier["review_section"] = extract_section(raw, "Review-Stand")

    if summary.exists():
        lines = [
            line.strip()
            for line in load_text(summary).splitlines()
            if line.strip() and not line.strip().startswith("---")
        ]
        dossier["summary_preview"] = "\n".join(lines[:12])

    required_actions: list[str] = []
    if not archive_path.exists():
        required_actions.append("archive_page_missing")
    if not summary.exists():
        required_actions.append("summary_missing")
    if not system_path.exists():
        required_actions.append("system_ticket_missing")
    if candidate and candidate.status == "IN_REVIEW_HISTORIAN":
        required_actions.append("human_final_approve_or_return")
        dossier["recommended_decisions"] = ["approved", "returned", "commented"]
    elif candidate and candidate.status == "AWAITING_HUMAN_DECISION":
        required_actions.append("human_final_required")
        dossier["recommended_decisions"] = ["approved", "returned"]
    elif not candidate:
        required_actions.append("not_actionable_in_review_queue")

    dossier["required_actions"] = required_actions
    return dossier


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
        raw = STATUS_SECTION_RE.sub(status_text.rstrip() + "\n\n", raw, count=1)
    else:
        raw += "\n\n" + status_text + "\n"

    if REVIEW_SECTION_RE.search(raw):
        raw = REVIEW_SECTION_RE.sub(review_text.rstrip() + "\n\n", raw, count=1)
    else:
        insertion = "\n" + review_text.rstrip() + "\n"
        h1 = re.search(r"(?m)^# .+\n", raw)
        if h1:
            raw = raw[: h1.end()] + insertion + raw[h1.end() :]
        elif (frontmatter := FRONTMATTER_RE.search(raw)):
            raw = raw[: frontmatter.end()] + insertion + raw[frontmatter.end() :]
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


def review_mutation_plan(research_id: str, decision: str, role: str) -> list[str]:
    actions = [
        "dispatch_post",
        "append_review_register",
        "update_archive_page",
        "update_system_research_board",
        "update_archive_research_board",
    ]
    if decision == "approved":
        actions.append("set_system_ticket_resolved_if_present")
    elif decision == "returned":
        actions.append("set_system_ticket_open_historian_if_present")
    if role == "human_final":
        actions.append("final_human_gate")
    return actions


def apply_review_action(
    research_id: str,
    decision: str,
    reviewer: str,
    role: str,
    note: str,
    json_mode: bool = False,
    dry_run: bool = False,
) -> int:
    candidates = {candidate.research_id for candidate in list_review_candidates()}
    if research_id not in candidates:
        payload = {
            "status": "blocked",
            "reason": "not_in_review_status",
            "research_id": research_id,
            "dossier": make_review_dossier(research_id),
        }
        if json_mode:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(f"{research_id} ist derzeit nicht im REVIEW-Status.")
        return 1
    if decision in {"approved", "returned"} and role != "human_final":
        payload = {
            "status": "blocked",
            "reason": "human_final_required",
            "research_id": research_id,
            "decision": decision,
            "role": role,
            "dossier": make_review_dossier(research_id),
        }
        if json_mode:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(f"{decision} fuer {research_id} erfordert Rolle human_final.")
        return 1

    if dry_run:
        payload = {
            "status": "dry_run",
            "research_id": research_id,
            "decision": decision,
            "reviewer": reviewer,
            "role": role,
            "would_mutate": review_mutation_plan(research_id, decision, role),
            "dossier": make_review_dossier(research_id),
        }
        if json_mode:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print(f"{research_id}: dry-run {decision} durch {reviewer} ({role})")
            print("Would mutate: " + ", ".join(payload["would_mutate"]))
        return 0

    dispatch_subject = f"Research review: {research_id} {decision}"
    dispatch_body = (
        f"Review-Entscheidung fuer {research_id}: {decision}. Reviewer: {reviewer} ({role}). "
        f"Notiz: {note}"
    )
    if json_mode:
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            dispatch_ref = capture_dispatch_post(role.split("_", 1)[0].title(), "Coordinator", dispatch_subject, dispatch_body)
        dispatch_output = buf.getvalue().strip()
    else:
        dispatch_ref = capture_dispatch_post(role.split("_", 1)[0].title(), "Coordinator", dispatch_subject, dispatch_body)
        dispatch_output = ""
    append_review_register(research_id, reviewer, role, decision, note, dispatch_ref)
    update_archive_page(research_id, decision, reviewer, role, note, dispatch_ref)
    move_or_update_board_row(SYSTEM_RESEARCH_BOARD, research_id, decision)
    move_or_update_board_row(ARCHIVE_RESEARCH_BOARD, research_id, decision)
    if decision == "approved":
        maybe_update_system_ticket(research_id, "RESOLVED")
    elif decision == "returned":
        maybe_update_system_ticket(research_id, "OPEN_HISTORIAN")
    if json_mode:
        print(json.dumps({
            "status": "ok",
            "research_id": research_id,
            "decision": decision,
            "reviewer": reviewer,
            "role": role,
            "dispatch_ref": dispatch_ref,
            "dispatch_output": dispatch_output,
            "dossier": make_review_dossier(research_id),
        }, indent=2, ensure_ascii=False))
    else:
        print(f"{research_id}: {decision} durch {reviewer} ({role})")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Research review and approval helper")
    parser.add_argument("--list", action="store_true", help="List research review candidates")
    parser.add_argument("--dossier", action="store_true", help="Show one machine-readable review dossier")
    parser.add_argument("--research-id", help="Research ID, e.g. RESEARCH-2026-004")
    parser.add_argument("--decision", choices=["approved", "returned", "commented"])
    parser.add_argument("--reviewer")
    parser.add_argument("--role", choices=["human_final", "historian_comment", "coordinator_note"])
    parser.add_argument("--note")
    parser.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    parser.add_argument("--dry-run", action="store_true", help="Validate the action and show planned mutations without writing")
    args = parser.parse_args()

    if args.list:
        candidates = list_review_candidates()
        if args.json:
            print(json.dumps({
                "status": "ok",
                "count": len(candidates),
                "results": [candidate.as_dict() for candidate in candidates],
            }, indent=2, ensure_ascii=False))
            return 0
        if not candidates:
            print("Keine Research-Auftraege im REVIEW-Status.")
            return 0
        for candidate in candidates:
            print(
                f"{candidate.research_id} | {candidate.status} | {candidate.title} | "
                f"{candidate.priority} | {candidate.focus}"
            )
        return 0

    if args.dossier:
        if not args.research_id:
            parser.error("--dossier benoetigt --research-id.")
        dossier = make_review_dossier(args.research_id)
        if args.json:
            print(json.dumps(dossier, indent=2, ensure_ascii=False))
        else:
            print(f"{args.research_id}: {dossier['status']}")
            print(f"Archivseite: {dossier['paths']['archive_page']} ({'ok' if dossier['exists']['archive_page'] else 'fehlt'})")
            print(f"Summary: {dossier['paths']['summary']} ({'ok' if dossier['exists']['summary'] else 'fehlt'})")
            print("Required actions: " + ", ".join(dossier["required_actions"]))
        return 0

    if not all([args.research_id, args.decision, args.reviewer, args.role, args.note]):
        parser.error("Fuer Review-Aktionen sind --research-id, --decision, --reviewer, --role und --note erforderlich.")

    if args.role != "human_final" and args.decision in {"approved", "returned"}:
        parser.error("Nur human_final darf Forschung final freigeben oder zur Nacharbeit zurueckgeben.")

    return apply_review_action(
        args.research_id,
        args.decision,
        args.reviewer,
        args.role,
        args.note,
        args.json,
        args.dry_run,
    )


if __name__ == "__main__":
    raise SystemExit(main())
