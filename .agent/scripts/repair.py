#!/usr/bin/env python3
"""
repair.py — Interaktives Reparatur-Werkzeug für das Siebenwind Wiki.

Funktionen:
1. Frontmatter Fixer: Ergänzt fehlende YAML-Header.
2. Smart Link Resolver: Findet tote Links und korrigiert sie durch Fuzzy-Matching & Canon-Mapping.
3. Source Reference Repair: Normalisiert problematische Quellen-Links (file://, %25xx, [[index]]).
4. Duplicate Detector: Findet doppelte Dateien (Kollisionen im Canon).

Nutzung:
    python3 .agent/scripts/repair.py [--auto|--full] [--check-collision NAME]
"""

import os
import sys
import re
import argparse
from pathlib import Path
from collections import defaultdict
import difflib
from urllib.parse import unquote

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
WIKI_DIR = PROJECT_ROOT / "Siebenwind_Wiki"
QUELLEN_DIR = PROJECT_ROOT / "Quellen"
INGESTION_DIR = PROJECT_ROOT / "Logs" / "Ingestion"
DOCS_COORDINATION_HUB = PROJECT_ROOT / "docs" / "COORDINATION_HUB.md"

# Known Redirects / Hardcoded Fixes
LORE_REDIRECTS = {
    "chronik": "Die_Chronik",
    "malthust": "Region_Malthust",
    "suedfall": "Südfall",
    "oedland": "Ödland",
    "kesselklamm": "Bragarim",
    "dur": "Toran_Dur",
    "westhever": "Dunkeltief",
    "lehens_banner": "Lehensbanner",
}

def derive_category(path: Path) -> str:
    """Bestimmt die Kategorie anhand des Ordnernamens."""
    parent_name = path.parent.name
    mapping = {
        "04_Chronik": "Chronik",
        "07_Persoenlichkeiten": "Personen",
        "02_Geografie": "Geografie",
        "03_Gesellschaft": "Gesellschaft",
        "10_Archiv": "Archiv",
        "01_Pantheon": "Religion",
        "05_Magie": "Magie",
        "05_Geschichte": "Geschichte"
    }
    return mapping.get(parent_name, "Allgemein")

def normalize_key(name: str) -> str:
    """Normalisiert einen Dateinamen für den Vergleich (lowercase, no space/underscore)."""
    return name.lower().replace("_", "").replace(" ", "").replace("-", "")


def _clean_link_target(target: str) -> str:
    cleaned = target.strip()
    if cleaned.startswith("<") and cleaned.endswith(">"):
        cleaned = cleaned[1:-1].strip()
    cleaned = cleaned.split(" ", 1)[0]
    cleaned = cleaned.split("#", 1)[0]
    return cleaned


def _source_repair_file_set(base_files: list[Path]) -> list[Path]:
    files = set(base_files)
    if INGESTION_DIR.exists():
        files.update(INGESTION_DIR.rglob("*.md"))
    if DOCS_COORDINATION_HUB.exists():
        files.add(DOCS_COORDINATION_HUB)
    return sorted(files)


def _build_quellen_lookup() -> dict[str, list[Path]]:
    lookup: dict[str, list[Path]] = defaultdict(list)
    if not QUELLEN_DIR.exists():
        return lookup
    for fpath in QUELLEN_DIR.rglob("*.md"):
        lookup[normalize_key(fpath.stem)].append(fpath)
    return lookup


def _best_quellen_match(raw_target: str, lookup: dict[str, list[Path]]) -> Path | None:
    decoded = unquote(_clean_link_target(raw_target))
    basename = Path(decoded).name
    if not basename:
        return None
    if basename.lower().endswith(".html"):
        basename = basename[:-5] + ".md"

    key = normalize_key(Path(basename).stem)
    candidates = lookup.get(key, [])
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]

    decoded_low = decoded.lower()
    scored = []
    for cand in candidates:
        cand_low = str(cand.relative_to(PROJECT_ROOT)).lower()
        score = 0
        for token in ("bibliothek astrael", "bibliothek toran dur", "spielergeschichten", "zeitung 7w bote", "hintergrund", "forum", "news"):
            if token in decoded_low and token in cand_low:
                score += 3
        for token in ("astrael", "toran", "bote", "spielergeschichten"):
            if token in decoded_low and token in cand_low:
                score += 1
        scored.append((score, len(str(cand)), cand))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return scored[0][2]

def get_canon_map(target_dir: Path) -> dict:
    """
    Erstellt eine Map aller existierenden Dateien.
    Key: Normalisierter Name
    Value: Liste von Pfaden (für Duplikat-Erkennung)
    """
    canon_map = defaultdict(list)
    for f in target_dir.rglob("*.md"):
        key = normalize_key(f.stem)
        canon_map[key].append(f)
        
        # Check Frontmatter Aliases (Basic Regex)
        try:
            content = f.read_text(encoding="utf-8")[:2000]
            aliases_match = re.search(r'^aliases:\s*\[(.*?)\]', content, re.MULTILINE)
            if aliases_match:
                aliases = aliases_match.group(1).split(",")
                for alias in aliases:
                    alias_key = normalize_key(alias.strip().strip('"\''))
                    canon_map[alias_key].append(f)
        except: pass
        
    return canon_map

def resolve_link(target: str, canon_map: dict) -> str | None:
    """
    Versucht, einen Link intelligent aufzulösen.
    1. Check Redirects
    2. Check Canon Map (Exact normalized match)
    """
    # 1. Hardcoded Redirects
    target_clean = target.lower().replace(" ", "_")
    if target_clean in LORE_REDIRECTS:
        return LORE_REDIRECTS[target_clean]

    # 2. Canon Map Match
    key = normalize_key(target)
    if key in canon_map:
        matches = canon_map[key]
        if matches:
            # Priorisierung: Nimm die Datei mit dem kürzesten Pfad oder tiefsten Nesting?
            # Hier nehmen wir einfach die erste, idealerweise sollte man Logik haben.
            # Aber wir returnen den *Stem* (Dateinamen ohne Extension), da WikiLinks relativ sind.
            return matches[0].stem
            
    return None

def check_duplicates(canon_map: dict):
    """Listet Dateien auf, die den gleichen normalisierten Namen haben."""
    print(f"\n{BLUE}--- Duplicate Detector ---{RESET}")
    found = False
    for key, paths in canon_map.items():
        if len(paths) > 1:
            # Filter out intentional duplicates if they are in different major folders?
            # For now, just list them.
            print(f"{YELLOW}Doppelte Einträge für '{key}':{RESET}")
            for p in paths:
                print(f"  - {p.relative_to(PROJECT_ROOT)}")
            found = True
            
    if not found:
        print(f"{GREEN}Keine Duplikate gefunden.{RESET}")
    else:
        print(f"\n{YELLOW}Hinweis:{RESET} Diese Dateien könnten kollidieren. Bitte manuell prüfen.")

def repair_links(files: list[Path], canon_map: dict, auto: bool = False):
    """Repariert tote links mittels Smart Resolver."""
    print(f"\n{BLUE}--- Smart Link Repair ---{RESET}")
    count = 0
    link_regex = re.compile(r'\[\[([^\]|#]+)(#[^\]|]+)?(\|[^\]]+)?\]\]')

    def replace_callback(match):
        original_target = match.group(1)
        anchor = match.group(2) or ""
        text = match.group(3) or ""
        
        # Check if valid first
        norm_key = normalize_key(original_target)
        if norm_key in canon_map:
            # Existiert (zumindest als Match).
            # Prüfen ob Case stimmt.
            best_match = canon_map[norm_key][0].stem
            if best_match != original_target:
                # Casing repair or Redirect
                return f"[[{best_match}{anchor}{text}]]"
            return match.group(0) # Unverändert
        
        # Dead Link -> Versuch Resolve
        resolved = resolve_link(original_target, canon_map)
        if resolved:
            return f"[[{resolved}{anchor}{text}]]"
        
        return match.group(0) # Kann nicht repariert werden

    for fpath in files:
        try:
            content = fpath.read_text(encoding="utf-8")
            new_content = link_regex.sub(replace_callback, content)
            
            if new_content != content:
                if not auto:
                    print(f"Änderung an {fpath.name}:")
                    # Diff anzeigen wäre gut, aber hier kurz halten
                
                if auto or input("  Änderungen speichern? [y/n]: ").lower() == 'y':
                    fpath.write_text(new_content, encoding="utf-8")
                    print(f"  {GREEN}Repariert.{RESET}")
                    count += 1
        except Exception:
            pass

    print(f"\n{count} Dateien repariert.")


def repair_source_references(files: list[Path], auto: bool = False):
    """
    Repariert fehleranfällige Quellen-Links:
    - file:// URIs
    - doppelt encodierte Targets (%25xx)
    - [[index]] Platzhalter in Quellenpfaden
    - markdown links auf Quellen -> robustes Pfadformat mit Backticks
    """
    print(f"\n{BLUE}--- Source Reference Repair ---{RESET}")
    count = 0
    link_re = re.compile(r'(?<!\!)\[(?P<label>[^\]]+)\]\((?P<target>[^)]+)\)')
    malformed_re = re.compile(r"\.\./\.\./Quellen/\[index\]\(\.\./10_Archiv/index\.md")
    quellen_lookup = _build_quellen_lookup()

    def repl(match, source_file: Path):
        label = match.group("label").strip()
        target_raw = match.group("target").strip()
        target = _clean_link_target(target_raw)
        if not target:
            return match.group(0)

        is_source_like = (
            "Quellen/" in target
            or "Archiv/Ingestion_Reports/" in target
            or target.startswith("file://")
            or re.search(r"%25[0-9A-Fa-f]{2}", target) is not None
            or "[[index]]" in target
            or "%5B%5Bindex%5D%5D" in target
        )
        if not is_source_like:
            return match.group(0)

        needs_repair = (
            target.startswith("file://")
            or re.search(r"%25[0-9A-Fa-f]{2}", target) is not None
            or "[[index]]" in target
            or "%5B%5Bindex%5D%5D" in target
            or target.endswith(".html")
        )
        if not needs_repair:
            return match.group(0)

        resolved = None
        if "Quellen/" in target or target.startswith("file://"):
            match_path = _best_quellen_match(target, quellen_lookup)
            if match_path is not None:
                resolved = os.path.relpath(match_path, start=source_file.parent).replace(os.sep, "/")

        if resolved is None:
            fallback = unquote(target)
            fallback = fallback.replace("%5B%5Bindex%5D%5D%20", "")
            fallback = fallback.replace("[[index]]%20", "")
            fallback = fallback.replace("[[index]] ", "")
            fallback = fallback.replace("%2520", "%20")
            fallback = fallback.replace("%25C2%25B7", "%C2%B7")
            if fallback.startswith("file://"):
                fallback = fallback[len("file://"):]
                try:
                    fallback_path = Path(fallback)
                    if fallback_path.exists():
                        fallback = os.path.relpath(fallback_path, start=source_file.parent).replace(os.sep, "/")
                except Exception:
                    pass
            resolved = fallback

        return f"{label} (`{resolved}`)"

    for fpath in files:
        try:
            content = fpath.read_text(encoding="utf-8")
        except Exception:
            continue

        new_content = content
        # Handle a known malformed nested markdown pattern from legacy ingestions.
        new_content = malformed_re.sub("../../Quellen/10_Archiv/index.md", new_content)
        new_content = link_re.sub(lambda m: repl(m, fpath), new_content)

        if new_content != content:
            if not auto:
                print(f"Änderung an {fpath.relative_to(PROJECT_ROOT)}")
            if auto or input("  Änderungen speichern? [y/n]: ").lower() == 'y':
                fpath.write_text(new_content, encoding="utf-8")
                print(f"  {GREEN}Repariert.{RESET}")
                count += 1

    print(f"\n{count} Dateien mit Source-Referenzen repariert.")

def fix_frontmatter(files: list[Path], auto: bool = False):
    """Sucht und repariert fehlendes Frontmatter."""
    print(f"\n{BLUE}--- Frontmatter Fixer ---{RESET}")
    count = 0
    for file_path in files:
        try:
            content = file_path.read_text(encoding="utf-8")
        except: continue
        
        if not content.startswith("---"):
            title = file_path.stem.replace("_", " ")
            category = derive_category(file_path)
            frontmatter = f"---\nlayout: post\ntitle: \"{title}\"\ncategory: {category}\n---\n\n"
            
            if auto or input(f"Frontmatter für {file_path.name} erstellen? [y/n]: ").lower() == 'y':
                file_path.write_text(frontmatter + content, encoding="utf-8")
                print(f"  {GREEN}Repariert.{RESET}")
                count += 1
    print(f"{count} Frontmatter hinzugefügt.")


def run_full_repair(files: list[Path], source_files: list[Path], canon_map: dict, auto: bool = False):
    """Führt die Reparaturmodule 1→3 in Reihenfolge aus."""
    fix_frontmatter(files, auto=auto)
    repair_links(files, canon_map, auto=auto)
    repair_source_references(source_files, auto=auto)


def main():
    parser = argparse.ArgumentParser(description="Siebenwind Repair Tool 2.0")
    parser.add_argument("--path", default=str(WIKI_DIR), help="Zielverzeichnis")
    parser.add_argument("--auto", action="store_true", help="Auto-Repair ohne Nachfrage")
    parser.add_argument("--full", action="store_true", help="Voller Durchlauf (1-3) ohne Nachfrage")
    parser.add_argument("--check-collision", help="Prüft, ob ein Dateiname bereits existiert")
    args = parser.parse_args()
    
    target_dir = Path(args.path)
    if not target_dir.exists():
        print(f"Verzeichnis fehlt: {target_dir}")
        sys.exit(1)

    print(f"Indiziere Canon Map für {target_dir}...")
    canon_map = get_canon_map(target_dir)

    # Collision Check Mode
    if args.check_collision:
        key = normalize_key(args.check_collision)
        if key in canon_map:
            print(f"{RED}KOLLISION GEFUNDEN:{RESET}")
            for p in canon_map[key]:
                print(f"  - {p}")
            sys.exit(1)
        else:
            print(f"{GREEN}Keine Kollision. Name ist frei.{RESET}")
            sys.exit(0)

    # Normal Mode
    files = list(target_dir.rglob("*.md"))
    source_files = _source_repair_file_set(files)
    
    if args.auto or args.full:
        mode_label = "FULL REPAIR" if args.full else "AUTO REPAIR"
        print(f"{BLUE}=== {mode_label} STARTED ==={RESET}")
        check_duplicates(canon_map)
        run_full_repair(files, source_files, canon_map, auto=True)
        print(f"{GREEN}=== FERTIG ==={RESET}")
    else:
        check_duplicates(canon_map)
        while True:
            print("\nOptionen:")
            print("  1) Frontmatter Fixer")
            print("  2) Smart Link Repair")
            print("  3) Source Reference Repair")
            print("  4) Voller Durchlauf (1-3) [Standard]")
            print("  q) Beenden")
            c = input("Wahl [4]: ").strip().lower() or "4"
            if c == '1': fix_frontmatter(files)
            elif c == '2': repair_links(files, canon_map)
            elif c == '3': repair_source_references(source_files)
            elif c == '4': run_full_repair(files, source_files, canon_map)
            elif c == 'q': break

if __name__ == "__main__":
    main()
