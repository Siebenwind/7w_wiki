#!/usr/bin/env python3
import os
import re
from pathlib import Path

WIKI_DIR = Path("Siebenwind_Wiki")

# Mapping for folder-based category restoration
CATEGORY_MAPPING = {
    "04_Chronik": "Chronik",
    "07_Persoenlichkeiten": "Personen",
    "02_Geografie": "Geografie",
    "03_Gesellschaft": "Gesellschaft",
    "10_Archiv": "Archiv",
    "01_Pantheon": "Religion",
    "05_Magie": "Magie",
    "05_Geschichte": "Geschichte",
    "00_Fundament": "Allgemein"
}

# Semantic patterns for in-text replacement
SEMANTIC_REPLACEMENTS = [
    (r"## \[\[index\]\] & Wirken", "## Magie & Wirken"),
    (r"Zirkel der \[\[index\]\]", "Zirkel der Magie"),
    (r"Lexikon der \[\[index\]\]", "Lexikon der Magie"),
    (r"Theorie der \[\[index\]\]", "Theorie der Magie"),
    (r"Arten der \[\[index\]\]", "Arten der Magie"),
    (r"schwarzen \[\[index\]\]", "schwarzen Magie"),
    (r"dunklen Aspekten der \[\[index\]\]", "dunklen Aspekten der Magie"),
    (r"fachliches \[\[index\]\]", "fachliches Wissen"),
    (r"tiefes \[\[index\]\]", "tiefes Wissen"),
    (r"## \[\[index\]\] der \[\[Elfen\]\]", "## Sprachen der [[Elfen]]"),
    (r"## \[\[index\]\] der \[\[Zwerge\]\]", "## Sprachen der [[Zwerge]]"),
    (r"verschiedenen \[\[index\]\] und Dialekte", "verschiedenen Sprachen und Dialekte"),
    (r"Abneigung gegen \[\[index\]\]", "Abneigung gegen Magie"),
    (r"beherrschen \[\[index\]\]", "beherrschen Magie"),
    (r"\[\[index\]\] basiert auf", "Magie basiert auf"),
    (r"Bedeutung in der praktischen \[\[index\]\]", "Bedeutung in der praktischen Magie"),
    (r"/Quellen/\[\[index\]\] \[\[Astrael\]\]/", "/Quellen/Bibliothek Astrael/"),
    (r"/Quellen/\[\[index\]\] \[\[Toran_Dur\]\]/", "/Quellen/Bibliothek Toran Dur/"),
    (r"Bote \d+\] / \[\[index\]\]", lambda m: m.group(0).replace("[[index]]", "Bote")), # e.g. [Bote 180] / [[index]] -> [Bote 180] / Bote
    (r"## \[\[index\]\]", "## Wirken"), # Fallback for personality headers
    (r"category: \[\[index\]\]", None), # Special handling
]

def restore_file(fpath):
    try:
        content = fpath.read_text(encoding="utf-8")
        new_content = content
        
        # 1. Category Fix
        if "category: [[index]]" in new_content:
            parent_folder = fpath.parent.name
            target_cat = CATEGORY_MAPPING.get(parent_folder, "Allgemein")
            new_content = new_content.replace("category: [[index]]", f"category: {target_cat}")

        # 2. Semantic Replacements
        for pattern, replacement in SEMANTIC_REPLACEMENTS:
            if replacement is None: continue # Handled above
            if callable(replacement):
                new_content = re.sub(pattern, replacement, new_content)
            else:
                new_content = re.sub(pattern, replacement, new_content)

        # 3. Last Resort: Generic replacement for remaining [[index]]
        # In Persönlichkeiten it's likely 'Persönlichkeit' or 'Wissen'
        # In Magie it's 'Magie'
        if "[[index]]" in new_content:
            if "07_Persoenlichkeiten" in str(fpath):
                new_content = new_content.replace("[[index]]", "Wissen") # safest generic for text
            elif "05_Magie" in str(fpath) or "Werke" in str(fpath):
                new_content = new_content.replace("[[index]]", "Magie")
            else:
                new_content = new_content.replace("[[index]]", "Wissen")

        if new_content != content:
            fpath.write_text(new_content, encoding="utf-8")
            return True
    except Exception as e:
        print(f"Error in {fpath}: {e}")
    return False

def main():
    count = 0
    for f in WIKI_DIR.rglob("*.md"):
        if restore_file(f):
            count += 1
            print(f"Restored: {f}")
    print(f"Total files restored: {count}")

if __name__ == "__main__":
    main()
