#!/usr/bin/env python3
import argparse
import os
import re
import sys
from datetime import datetime

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TARGET_REL = "docs/Archiv/MAINTAINER_STANDPUNKT.md"
TARGET_PATH = os.path.join(REPO_ROOT, TARGET_REL)

REQUIRED_HEADINGS = [
    "## 1) Nicht verhandelbar",
    "## 2) Prioritaeten-Reihenfolge",
    "## 3) Stil und Positionierung",
    "## 4) No-Gos",
    "## 5) Eskalation und Entscheidungsrecht",
    "## 6) Aenderungsprotokoll",
]

TODO_PATTERN = re.compile(r"\bTODO\b", re.IGNORECASE)

TEMPLATE = """# Maintainer-Standpunkt (Menschlicher Leitpunkt)

Status: Entwurf (wird mit dem Maintainer fortlaufend konkretisiert)

## Zweck

Diese Seite ist der verbindliche menschliche Leitpunkt fuer Agentenarbeit.
Sie reduziert permanentes Nachsteuern, indem Prioritaeten, No-Gos und Eskalationsregeln klar festgehalten werden.

## 1) Nicht verhandelbar

- TODO: Welche Prinzipien duerfen nie verletzt werden?
- TODO: Welche Qualitaetskriterien sind Pflicht vor Merge/Release?
- TODO: Welche Themen brauchen immer menschliche Freigabe?

## 2) Prioritaeten-Reihenfolge

1. TODO: Was hat absolut Vorrang?
2. TODO: Was ist wichtig, aber nachgelagert?
3. TODO: Was ist optional/Backlog?

## 3) Stil und Positionierung

- Zielgruppe: TODO
- Tonalitaet: TODO
- Visuelle Leitlinie: TODO
- KI-Transparenz: TODO

## 4) No-Gos

- TODO: Welche Design-/Inhaltsmuster sind ausgeschlossen?
- TODO: Welche technischen Abkuerzungen sind nicht erlaubt?
- TODO: Welche Betriebsweisen sind unerwuenscht?

## 5) Eskalation und Entscheidungsrecht

- Entscheidungen mit Maintainer-Veto:
  - TODO
- Entscheidungen mit Agenten-Autonomie:
  - TODO
- Eskalation bei Unsicherheit:
  - TODO (Kanal + Reaktionszeit)

## 6) Aenderungsprotokoll

- Jede Anpassung dieser Seite wird im Changelog vermerkt.
- Diese Seite hat Vorrang vor weichen Stilpraeferenzen in Einzelprompts.
"""


def _read_text():
    if not os.path.exists(TARGET_PATH):
        return None
    with open(TARGET_PATH, "r", encoding="utf-8") as f:
        return f.read()


def _analyze(text):
    missing = [h for h in REQUIRED_HEADINGS if h not in text]
    todo_count = len(TODO_PATTERN.findall(text))
    if missing:
        readiness = "BLOCKED"
    elif todo_count > 0:
        readiness = "DRAFT"
    else:
        readiness = "ACTIVE"
    return {
        "missing_headings": missing,
        "todo_count": todo_count,
        "readiness": readiness,
    }


def cmd_status():
    print("=== Leitpunkt Status ===")
    print(f"Pfad: {TARGET_REL}")
    if not os.path.exists(TARGET_PATH):
        print("Status: MISSING")
        print("Hinweis: ./7w_wiki.py leitpunkt scaffold")
        return 0

    text = _read_text()
    result = _analyze(text)
    mtime = datetime.fromtimestamp(os.path.getmtime(TARGET_PATH)).isoformat(timespec="seconds")
    print(f"Datei: vorhanden")
    print(f"Readiness: {result['readiness']}")
    print(f"TODO Marker: {result['todo_count']}")
    print(f"Pflichtsektionen fehlen: {len(result['missing_headings'])}")
    print(f"Zuletzt geaendert: {mtime}")

    if result["missing_headings"]:
        print("Fehlende Sektionen:")
        for sec in result["missing_headings"]:
            print(f"- {sec}")
    return 0


def cmd_check(strict=False):
    if not os.path.exists(TARGET_PATH):
        print("FAIL: Maintainer-Standpunkt fehlt.")
        print("Fix: ./7w_wiki.py leitpunkt scaffold")
        return 1

    text = _read_text()
    result = _analyze(text)

    if result["missing_headings"]:
        print("FAIL: Pflichtsektionen fehlen.")
        for sec in result["missing_headings"]:
            print(f"- {sec}")
        return 1

    if strict and result["todo_count"] > 0:
        print(f"FAIL: strict aktiv, aber TODO Marker vorhanden ({result['todo_count']}).")
        return 1

    mode = "strict" if strict else "normal"
    print(f"PASS: Leitpunkt-Check ({mode}).")
    print(f"Readiness: {result['readiness']} | TODO Marker: {result['todo_count']}")
    if (not strict) and result["todo_count"] > 0:
        print("Hinweis: `--strict` ist nur fuer Governance-Release/Handover/Policy-Freeze gedacht.")
    return 0


def cmd_scaffold(force=False):
    if os.path.exists(TARGET_PATH) and not force:
        print("SKIP: Datei existiert bereits.")
        print("Nutze --force fuer bewusstes Ueberschreiben.")
        return 0

    os.makedirs(os.path.dirname(TARGET_PATH), exist_ok=True)
    with open(TARGET_PATH, "w", encoding="utf-8") as f:
        f.write(TEMPLATE)
    print(f"OK: Vorlage geschrieben -> {TARGET_REL}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Maintainer-Standpunkt tooling")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("status", help="Show maintainer standpoint readiness")
    check_p = sub.add_parser("check", help="Validate required sections")
    check_p.add_argument("--strict", action="store_true", help="Fail if TODO markers remain")
    scaffold_p = sub.add_parser("scaffold", help="Create template if missing")
    scaffold_p.add_argument("--force", action="store_true", help="Overwrite existing file")

    args = parser.parse_args()
    if args.cmd == "status":
        rc = cmd_status()
    elif args.cmd == "check":
        rc = cmd_check(strict=args.strict)
    elif args.cmd == "scaffold":
        rc = cmd_scaffold(force=args.force)
    else:
        parser.print_help()
        rc = 1
    sys.exit(rc)


if __name__ == "__main__":
    main()
