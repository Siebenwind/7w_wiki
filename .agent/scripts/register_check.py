#!/usr/bin/env python3
"""
register_check.py — Automatisierte Konsistenzprüfung für das Siebenwind Wiki.

Prüft:
1. Duplikate im Personenregister
2. Verwaiste Profile (Datei existiert, kein Register-Eintrag)
3. Registrierte Personen ohne Profildatei
4. Boten-Lücken (Quellen vorhanden, nicht integriert)
5. Index-Lücken (Dateien vorhanden, nicht in Die_Chronik.md)

Nutzung:
    python3 .agent/scripts/register_check.py

Ausgabe: Strukturierter Report auf stdout.
"""

import os
import re
import sys
from pathlib import Path
from collections import Counter

# --- Configuration (relative to project root) ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
WIKI_DIR = PROJECT_ROOT / "Siebenwind_Wiki"
QUELLEN_DIR = PROJECT_ROOT / "Quellen" / "Zeitung 7w Bote"
REGISTER_FILE = WIKI_DIR / "00_Fundament" / "Personenregister.md"
PROFILE_DIR = WIKI_DIR / "07_Persoenlichkeiten"
CHRONIK_DIR = WIKI_DIR / "04_Chronik"
CHRONIK_INDEX = CHRONIK_DIR / "Die_Chronik.md"


def extract_register_names(register_path: Path) -> list[str]:
    """Extract person names (first [[Name]] per table row) from the Personenregister."""
    names = []
    if not register_path.exists():
        return names
    for line in register_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        # Only process table data rows (start with | and contain [[)
        if not line.startswith('|') or '[[' not in line:
            continue
        # Skip header/separator rows
        if line.startswith('| :') or line.startswith('| Name'):
            continue
        # Extract FIRST [[Name]] in the row — this is the person's name
        match = re.search(r'\[\[([^\]]+)\]\]', line)
        if match:
            names.append(match.group(1))
    return names


def find_duplicates(names: list[str]) -> dict[str, int]:
    """Find names that appear more than once."""
    counts = Counter(names)
    return {name: count for name, count in counts.items() if count > 1}


def get_profile_files(profile_dir: Path) -> set[str]:
    """Get all profile filenames (without .md extension)."""
    if not profile_dir.exists():
        return set()
    return {f.stem for f in profile_dir.glob("*.md")}


def get_boten_numbers(directory: Path, pattern: str) -> set[int]:
    """Extract Boten edition numbers from filenames in a directory."""
    numbers = set()
    if not directory.exists():
        return numbers
    for f in directory.iterdir():
        match = re.search(pattern, f.name)
        if match:
            try:
                numbers.add(int(match.group(1)))
            except ValueError:
                pass
    return numbers


def get_chronik_index_numbers(index_path: Path) -> set[int]:
    """Extract Boten numbers listed in Die_Chronik.md."""
    numbers = set()
    if not index_path.exists():
        return numbers
    content = index_path.read_text(encoding="utf-8")
    for match in re.finditer(r'Siebenwind_Bote_(\d+)', content):
        try:
            numbers.add(int(match.group(1)))
        except ValueError:
            pass
    return numbers


def main():
    print("=" * 60)
    print("  SIEBENWIND WIKI — REGISTER-CHECK")
    print("=" * 60)
    print()

    issues_found = 0

    # --- 1. Duplikat-Scan ---
    print("## 1. Duplikate im Personenregister")
    register_names = extract_register_names(REGISTER_FILE)
    duplicates = find_duplicates(register_names)
    if duplicates:
        for name, count in sorted(duplicates.items()):
            print(f"  ⚠️  {name} — {count}x vorhanden")
            issues_found += 1
    else:
        print("  ✅ Keine Duplikate gefunden.")
    print()

    # --- 2. Verwaiste Profile ---
    print("## 2. Verwaiste Profile (Datei ohne Register-Eintrag)")
    profile_files = get_profile_files(PROFILE_DIR)
    register_set = set(register_names)
    orphans = sorted(profile_files - register_set)
    if orphans:
        for name in orphans:
            # Check if file has quelle: in frontmatter
            fpath = PROFILE_DIR / f"{name}.md"
            has_quelle = False
            try:
                content = fpath.read_text(encoding="utf-8")[:500]
                has_quelle = "quelle:" in content.lower()
            except Exception:
                pass
            status = "📎 hat quelle:" if has_quelle else "❓ keine quelle:"
            print(f"  ⚠️  {name} — {status}")
            issues_found += 1
    else:
        print("  ✅ Alle Profile sind registriert.")
    print()

    # --- 3. Registriert ohne Profildatei ---
    print("## 3. Registrierte Personen ohne Profildatei")
    missing_profiles = sorted(register_set - profile_files)
    # Filter out common non-person links
    skip_prefixes = ("Siebenwind", "Region_", "Rasse_", "Ecclesia", "Kirche",
                     "Pakt_", "Graue_", "Löwen", "Ersonter", "Dwarshim",
                     "Bellum", "Vitama", "Ignis", "Enhor", "Morsan", "Xan",
                     "Persönlichkeiten", "index", "Geografie", "Geschichte")
    missing_profiles = [n for n in missing_profiles
                       if not any(n.startswith(p) for p in skip_prefixes)]
    if missing_profiles:
        for name in missing_profiles[:30]:
            print(f"  📝 {name} — Profildatei fehlt")
            issues_found += 1
        if len(missing_profiles) > 30:
            print(f"  ... und {len(missing_profiles) - 30} weitere.")
    else:
        print("  ✅ Alle registrierten Personen haben Profildateien.")
    print()

    # --- 4. Boten-Lücken ---
    print("## 4. Boten-Lücken (Quellen vorhanden, nicht integriert)")
    quellen_numbers = get_boten_numbers(QUELLEN_DIR, r'Bote\s+(\d+)')
    wiki_numbers = get_boten_numbers(CHRONIK_DIR, r'Bote_(\d+)')
    missing_boten = sorted(quellen_numbers - wiki_numbers)
    if missing_boten:
        for num in missing_boten:
            print(f"  ⚠️  Bote {num} — Quelle vorhanden, nicht integriert")
            issues_found += 1
    else:
        print("  ✅ Alle verfügbaren Boten sind integriert.")
    print()

    # --- 5. Index-Lücken ---
    print("## 5. Index-Lücken (Dateien vorhanden, nicht in Die_Chronik.md)")
    index_numbers = get_chronik_index_numbers(CHRONIK_INDEX)
    unindexed = sorted(wiki_numbers - index_numbers)
    if unindexed:
        for num in unindexed:
            print(f"  ⚠️  Bote {num} — Datei existiert, fehlt im Index")
            issues_found += 1
    else:
        print("  ✅ Alle Boten-Dateien sind im Index erfasst.")
    print()

    # --- Summary ---
    print("=" * 60)
    print(f"  ERGEBNIS: {issues_found} Probleme gefunden.")
    if issues_found == 0:
        print("  🎉 Das Wiki ist konsistent!")
    else:
        print("  → Siehe /audit Workflow für Bearbeitungsschritte.")
    print("=" * 60)

    return 1 if issues_found > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
