#!/usr/bin/env python3
import os
from pathlib import Path

WIKI_DIR = Path("Siebenwind_Wiki")

BRIDGE_FILES = [
    "00_Fundament/Arman_von_Draconis.md",
    "00_Fundament/Ars_Magica_Metamorphosia.md",
    "00_Fundament/Astraelorden.md",
    "00_Fundament/Astreyon.md",
    "00_Fundament/Aurora.md",
    "00_Fundament/Baumwesen.md",
    "00_Fundament/Benion.md",
    "00_Fundament/Burg_Saalhorn.md",
    "00_Fundament/Comari.md",
    "00_Fundament/Die_Viere_Kirche.md",
    "00_Fundament/Erin_Caiomme.md",
    "00_Fundament/Ersont.md",
    "00_Fundament/Feanthil.md",
    "00_Fundament/Feldmeister_Harlas.md",
    "00_Fundament/Feldmeister_Llewellyen.md",
    "00_Fundament/Galadonien.md",
    "00_Fundament/Galadons.md",
    "00_Fundament/Gerdenwald.md",
    "00_Fundament/Gohor.md",
    "00_Fundament/Gott Bellum.md"
]

def fix_bridge(fpath):
    full_path = WIKI_DIR / fpath
    if not full_path.exists(): return
    
    content = full_path.read_text(encoding="utf-8")
    if "bridge_mode:" in content: return # Already fixed or has partial
    
    # Simple replacement in frontmatter
    # We look for 'quelle: UNGEKLAERT' or the end of frontmatter '---'
    if "quelle: UNGEKLAERT" in content:
        replacement = "quelle: UNGEKLAERT\nbridge_mode: temporary\nbridge_target: [[Personenregister]]\nbridge_ticket: MSG-2026-0033\nbridge_review_until: 2026-03-31"
        new_content = content.replace("quelle: UNGEKLAERT", replacement)
    else:
        new_content = content.replace("\n---", "\nbridge_mode: temporary\nbridge_target: [[Personenregister]]\nbridge_ticket: MSG-2026-0033\nbridge_review_until: 2026-03-31\n---", 1)

    if new_content != content:
        full_path.write_text(new_content, encoding="utf-8")
        print(f"Fixed bridge: {fpath}")

def main():
    for bf in BRIDGE_FILES:
        fix_bridge(bf)

if __name__ == "__main__":
    main()
