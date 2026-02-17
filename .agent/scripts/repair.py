#!/usr/bin/env python3
"""
repair.py — Interaktives Reparatur-Werkzeug für das Siebenwind Wiki.

Funktionen:
1. Frontmatter Fixer: Ergänzt fehlende YAML-Header.
2. Smart Link Resolver: Findet tote Links und korrigiert sie durch Fuzzy-Matching & Canon-Mapping.
3. Duplicate Detector: Findet doppelte Dateien (Kollisionen im Canon).

Nutzung:
    python3 .agent/scripts/repair.py [--auto] [--check-collision NAME]
"""

import os
import sys
import re
import argparse
from pathlib import Path
from collections import defaultdict
import difflib

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
WIKI_DIR = PROJECT_ROOT / "Siebenwind_Wiki"

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

def main():
    parser = argparse.ArgumentParser(description="Siebenwind Repair Tool 2.0")
    parser.add_argument("--path", default=str(WIKI_DIR), help="Zielverzeichnis")
    parser.add_argument("--auto", action="store_true", help="Auto-Repair ohne Nachfrage")
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
    
    if args.auto:
        print(f"{BLUE}=== AUTO REPAIR STARTED ==={RESET}")
        check_duplicates(canon_map)
        fix_frontmatter(files, auto=True)
        repair_links(files, canon_map, auto=True)
        print(f"{GREEN}=== FERTIG ==={RESET}")
    else:
        check_duplicates(canon_map)
        while True:
            print("\nOptionen:")
            print("  1) Frontmatter Fixer")
            print("  2) Smart Link Repair")
            print("  q) Beenden")
            c = input("Wahl: ").lower()
            if c == '1': fix_frontmatter(files)
            elif c == '2': repair_links(files, canon_map)
            elif c == 'q': break

if __name__ == "__main__":
    main()
