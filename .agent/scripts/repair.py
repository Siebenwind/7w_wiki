#!/usr/bin/env python3
"""
repair.py — Interaktives Reparatur-Werkzeug für das Siebenwind Wiki.

Funktionen:
1. Frontmatter Fixer: Ergänzt fehlende YAML-Header.
2. Link Checker: Findet tote interne Links [[...]].
3. Orphan Manager: (Geplant) Findet verwaiste Dateien.

Nutzung:
    python3 .agent/scripts/repair.py
"""

import os
import sys
import re
import argparse
from pathlib import Path

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
WIKI_DIR = PROJECT_ROOT / "Siebenwind_Wiki"

def derive_category(path: Path) -> str:
    """Bestimmt die Kategorie anhand des Ordnernamens."""
    parent_name = path.parent.name
    # Mapping basierend auf der aktuellen Struktur
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

LORE_REDIRECTS = {
    "chronik": "Die_Chronik",
    "malthust": "Region_Malthust",
    "suedfall": "Südfall",
    "oedland": "Ödland",
    "01_bellum": "Bellum",
    "02_astrael": "Astrael",
    "03_bellum": "Bellum",
    "04_vitama": "Vitama",
    "05_morsan": "Morsan",
    "06_ignis": "Ignis",
    "07_rien": "Rien",
    "08_ventus": "Ventus",
    "09_xan": "Xan",
    "rasse_orken": "Orken",
    "rasse_halblinge": "Halblinge",
    "magie": "Magie_Grundlagen",
    "siebenwind_bote": "Die_Chronik",
    "ersonter_garde": "Graue_Garde",
    "kesselklamm": "Bragarim", # Often used as city but is the race homeland
    "dur": "Toran_Dur",
    "westhever": "Dunkeltief", # Westhever -> Dunkeltief area
    "lehens_banner": "Lehensbanner",
}

def get_wiki_map(files: list[Path]):
    """Maps stem and title (lowercase) to canonical target."""
    wiki_map = {}
    for f in files:
        wiki_map[f.stem.lower()] = f.stem
        try:
            content = f.read_text(encoding="utf-8")[:1000]
            match = re.search(r'^title:\s*(.*)', content, re.MULTILINE)
            if match:
                title = match.group(1).strip().strip('"').strip("'")
                wiki_map[title.lower()] = title
        except: pass
    return wiki_map

def fix_frontmatter(files: list[Path], auto: bool = False):
    """Sucht und repariert fehlendes Frontmatter."""
    print(f"\n{BLUE}--- Frontmatter Fixer ---{RESET}")
    count = 0
    fixed = 0
    
    for file_path in files:
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            continue
            
        if not content.startswith("---"):
            count += 1
            print(f"{YELLOW}Problem:{RESET} {file_path.name} hat kein Frontmatter.")
            
            # Vorschlag generieren
            title = file_path.stem.replace("_", " ")
            category = derive_category(file_path)
            frontmatter = (
                "---\n"
                f"layout: post\n"
                f"title: \"{title}\"\n"
                f"category: {category}\n"
                "---\n\n"
            )
            
            if auto:
                choice = 'y'
                print(f"  Reparieren? (Auto-Mode) [y]")
            else:
                choice = input(f"  Reparieren? (Fügt Titel '{title}' & Kategorie '{category}' hinzu) [y/n/q]: ").lower()
            if choice == 'q':
                break
            if choice == 'y':
                new_content = frontmatter + content
                file_path.write_text(new_content, encoding="utf-8")
                print(f"  {GREEN}Repariert!{RESET}")
                fixed += 1
                
    if count == 0:
        print(f"{GREEN}Keine Dateien ohne Frontmatter gefunden.{RESET}")
    else:
        print(f"\n{fixed} von {count} Dateien repariert.")

def check_links(files: list[Path]):
    """Findet tote interne Links."""
    print(f"\n{BLUE}--- Link Checker ---{RESET}")
    
    # 1. Alle existierenden Dateinamen sammeln (als Ziel)
    # Normierung: Leerzeichen/Underscores sind oft austauschbar im Wiki-Link, 
    # aber wir prüfen erstmal exakten Match oder Name.
    existing_files = {f.stem.lower(): f for f in files}
    
    broken_links = []
    
    for file_path in files:
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            continue
            
        # Finde alle [[Link]] oder [[Link|Text]]
        links = re.findall(r'\[\[(.*?)(?:\|.*?)?\]\]', content)
        for link in links:
            target = link.strip()
            # Ignoriere Anker #...
            if '#' in target:
                target = target.split('#')[0]
            
            if not target: continue
            
            target_norm = target.lower().replace(" ", "_")
            target_norm_alt = target.lower().replace("_", " ")
            
            if target_norm not in existing_files and target_norm_alt not in existing_files:
                broken_links.append((file_path.name, target))
                
    if not broken_links:
        print(f"{GREEN}Keine toten Links gefunden.{RESET}")
    else:
        print(f"{RED}{len(broken_links)} tote Links gefunden:{RESET}")
        for source, target in broken_links[:20]: # Limit output
            print(f"  {source} -> [[{target}]]")
        if len(broken_links) > 20:
            print(f"  ... und {len(broken_links) - 20} weitere.")

def repair_links(files: list[Path], auto: bool = False):
    """Repariert casing, redirects und malformed links."""
    print(f"\n{BLUE}--- Link Repair Engine ---{RESET}")
    wiki_map = get_wiki_map(files)
    count = 0
    
    # Precompile regex for performance
    # 1. Triple/Quad brackets: [[[Link]]] -> [[Link]]
    re_brackets = re.compile(r'\[{3,}(.*?)\]{3,}')
    # 2. Quotes: [["Link"]] -> [[Link]]
    re_quotes_dbl = re.compile(r'\[\["(.*?)"\]\]')
    re_quotes_sgl = re.compile(r"\[\['(.*?)'\]\]")
    # 3. Path prefixes & Casing & Redirects
    re_general = re.compile(r'\[\[(?:Quellen/|Siebenwind_Wiki/|docs/)?([^\]|#]+)(#[^\]|]+)?(\|[^\]]+)?\]\]')

    def fix_path_canonical(match):
        target, anchor, display = match.groups()
        # If target contains a path separator, take the last part
        if target and "/" in target:
            target = target.split("/")[-1]
        
        anchor_str = anchor if anchor else ""
        display_str = display if display else ""
        
        low_target = target.lower()
        
        # Check Redirects
        if low_target in LORE_REDIRECTS:
            target = LORE_REDIRECTS[low_target]
        # Check Casing
        elif low_target in wiki_map:
            target = wiki_map[low_target]
            
        return f"[[{target}{anchor_str}{display_str}]]"

    for fpath in files:
        try:
            content = fpath.read_text(encoding="utf-8")
            orig_content = content
            
            # Apply fixes in sequence
            content = re_brackets.sub(r'[[\1]]', content)
            content = re_quotes_dbl.sub(r'[[\1]]', content)
            content = re_quotes_sgl.sub(r'[[\1]]', content)
            content = re_general.sub(fix_path_canonical, content)
            
            if content != orig_content:
                if not auto:
                    print(f"\n{YELLOW}Änderungen an {fpath.name}:{RESET}")
                    # Simple diff heuristic (first change)
                    # For brevity, just ask
                    choice = input(f"  Reparieren? [y/n/q]: ").lower()
                    if choice == 'q': return
                    if choice != 'y': continue
                
                fpath.write_text(content, encoding="utf-8")
                print(f"  {GREEN}Repariert: {fpath.name}{RESET}")
                count += 1
        except Exception as e:
            print(f"{RED}Fehler bei {fpath.name}: {e}{RESET}")

    if count == 0:
        print(f"{GREEN}Keine Reparaturen notwendig.{RESET}")
    else:
        print(f"\n{count} Dateien erfolgreich repariert.")

def main():
    parser = argparse.ArgumentParser(description="Siebenwind Repair Tool")
    parser.add_argument("--path", default=str(WIKI_DIR), help="Zielverzeichnis scanning")
    parser.add_argument("--auto", action="store_true", help="Automatische Reparatur ohne Rückfragen")
    args = parser.parse_args()
    
    target_dir = Path(args.path)
    if not target_dir.exists():
        print(f"{RED}Verzeichnis nicht gefunden:{RESET} {target_dir}")
        sys.exit(1)
        
    print(f"Scanne {target_dir}...")
    files = list(target_dir.rglob("*.md"))
    print(f"{len(files)} Markdown-Dateien gefunden.")
    
    while True:
        print("\nOptionen:")
        print("  1) Frontmatter prüfen & reparieren")
        print("  2) Tote Links suchen (Report)")
        print("  3) Link-Engine (Casing, Redirects, Fixes)")
        print("  q) Beenden")
        
        choice = input("\nWahl: ").lower()
        
        if choice == '1':
            fix_frontmatter(files, auto=args.auto)
        elif choice == '2':
            check_links(files)
        elif choice == '3':
            repair_links(files, auto=args.auto)
        elif choice == 'q':
            break
        else:
            print("Ungültige Eingabe.")

if __name__ == "__main__":
    main()
