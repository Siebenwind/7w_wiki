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
        "03_Hintergrund": "Hintergrund",
        "10_Archiv": "Archiv",
        "05_Religion": "Religion",
        "06_Gruppen": "Gruppen",
        "01_Welt": "Welt"
    }
    return mapping.get(parent_name, "Allgemein")

def fix_frontmatter(files: list[Path]):
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

def main():
    parser = argparse.ArgumentParser(description="Siebenwind Repair Tool")
    parser.add_argument("--path", default=str(WIKI_DIR), help="Zielverzeichnis scanning")
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
        print("  q) Beenden")
        
        choice = input("\nWahl: ").lower()
        
        if choice == '1':
            fix_frontmatter(files)
        elif choice == '2':
            check_links(files)
        elif choice == 'q':
            break
        else:
            print("Ungültige Eingabe.")

if __name__ == "__main__":
    main()
