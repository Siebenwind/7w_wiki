#!/usr/bin/env python3
"""
changelog_tool.py

Add a top entry to CHANGELOG.md in the current markdown-native format:
#### [YYYY-MM-DD.NN] - Topic
### Prioritaet
- P1|P2|P3|BACKLOG
...
"""

import argparse
import re
from datetime import datetime
from pathlib import Path


CHANGELOG_PATH = Path("CHANGELOG.md")


def _next_version(lines: list[str], date_str: str) -> str:
    pattern = re.compile(rf"\[{re.escape(date_str)}\.(\d+)\]")
    max_idx = 0
    for line in lines:
        match = pattern.search(line)
        if match:
            max_idx = max(max_idx, int(match.group(1)))
    return f"[{date_str}.{max_idx + 1}]"


def _append_section(entry: list[str], title: str, values: list[str]) -> None:
    if not values:
        return
    entry.append(f"### {title}\n")
    for value in values:
        entry.append(f"- {value}\n")
    entry.append("\n")


def add_changelog_entry(
    topic: str,
    priority: str = "P2",
    additions: list[str] | None = None,
    changes: list[str] | None = None,
    fixes: list[str] | None = None,
    removals: list[str] | None = None,
    validated: list[str] | None = None,
) -> str:
    if not CHANGELOG_PATH.exists():
        raise FileNotFoundError(f"{CHANGELOG_PATH} nicht gefunden.")

    additions = additions or []
    changes = changes or []
    fixes = fixes or []
    removals = removals or []
    validated = validated or []

    lines = CHANGELOG_PATH.read_text(encoding="utf-8").splitlines(keepends=True)
    date_str = datetime.now().strftime("%Y-%m-%d")
    version = _next_version(lines, date_str)

    entry: list[str] = [f"#### {version} - {topic}\n\n", "### Prioritaet\n", f"- {priority}\n\n"]
    _append_section(entry, "Hinzugefuegt", additions)
    _append_section(entry, "Geaendert", changes)
    _append_section(entry, "Behoben", fixes)
    _append_section(entry, "Entfernt", removals)
    _append_section(entry, "Validiert", validated)

    insert_pos = 0
    for i, line in enumerate(lines):
        if line.startswith("# "):
            insert_pos = i + 1
            break

    final_lines = lines[:insert_pos] + ["\n"] + entry + lines[insert_pos:]
    CHANGELOG_PATH.write_text("".join(final_lines), encoding="utf-8")
    return version


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Fuegt einen neuen Changelog-Eintrag ein.")
    p.add_argument("topic", help="Titel/Thema des Eintrags")
    p.add_argument(
        "legacy_additions",
        nargs="*",
        help="Legacy-Kompatibilitaet: zusaetzliche positionale Werte werden als Hinzugefuegt behandelt.",
    )
    p.add_argument("--priority", default="P2", choices=["P1", "P2", "P3", "BACKLOG"])
    p.add_argument("--add", action="append", default=[], help="Punkt fuer Abschnitt Hinzugefuegt")
    p.add_argument("--change", action="append", default=[], help="Punkt fuer Abschnitt Geaendert")
    p.add_argument("--fix", action="append", default=[], help="Punkt fuer Abschnitt Behoben")
    p.add_argument("--remove", action="append", default=[], help="Punkt fuer Abschnitt Entfernt")
    p.add_argument("--validate", action="append", default=[], help="Punkt fuer Abschnitt Validiert")
    return p


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()
    additions = list(args.add)
    additions.extend(args.legacy_additions)
    version = add_changelog_entry(
        topic=args.topic,
        priority=args.priority,
        additions=additions,
        changes=list(args.change),
        fixes=list(args.fix),
        removals=list(args.remove),
        validated=list(args.validate),
    )
    print(f"OK: Entry {version} added to {CHANGELOG_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
