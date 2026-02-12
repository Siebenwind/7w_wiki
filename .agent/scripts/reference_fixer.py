import os
import re

WIKI_DIR = "/Users/alexandrerabe/siebenwind/7w_wiki/Siebenwind_Wiki"
QUELLEN_DIR = "/Users/alexandrerabe/siebenwind/7w_wiki/Quellen"
INVENTORY_FILE = "/Users/alexandrerabe/siebenwind/7w_wiki/Logs/INVENTUR_QUELLEN.md"

EXTENSIONS = [".html", ".doc", ".docx", ".pdf"]

def fix_links(file_path, dry_run=True):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content
    changes = 0

    # Match links to Quellen
    # Pattern: [Label](.../Quellen/... .ext)
    for ext in EXTENSIONS:
        pattern = re.compile(re.escape(ext) + r'(?=[)\s])')
        
        # We only want to replace if the resulting .md file exists or if it's within a link parenthesis
        # For simplicity, we'll replace all instances of these extensions in the context of file:/// references
        matches = list(re.finditer(r'file:///.*?Quellen/.*?' + re.escape(ext), content))
        for match in reversed(matches):
            start, end = match.span()
            link_part = content[start:end]
            md_link = link_part[:-len(ext)] + ".md"
            
            # Basic validation: does the MD file exist?
            # Stripping file:// prefex and url encoding for local check
            # Also stripping wiki-style brackets which shouldn't be in the physical path
            local_path = md_link.replace("file://", "").replace("%20", " ").replace("[[", "").replace("]]", "")
            if os.path.exists(local_path):
                new_content = new_content[:end-len(ext)] + ".md" + new_content[end:]
                changes += 1

    if changes > 0 and not dry_run:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    return changes

def run_fix(dry_run=True):
    total_changes = 0
    files_updated = 0

    for root, dirs, files in os.walk(WIKI_DIR):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                c = fix_links(path, dry_run)
                if c > 0:
                    total_changes += c
                    files_updated += 1
                    print(f"{'DRY RUN: ' if dry_run else ''}Updated {c} links in {file}")

    # Special case for INVENTUR_QUELLEN.md
    if os.path.exists(INVENTORY_FILE):
        with open(INVENTORY_FILE, 'r', encoding='utf-8') as f:
            inv_content = f.read()
        
        # In inventory, we just swap the extensions in the table column
        new_inv = inv_content
        for ext in EXTENSIONS:
            new_inv = new_inv.replace(ext + " |", ".md |")
        
        if new_inv != inv_content:
            print(f"{'DRY RUN: ' if dry_run else ''}Updated extensions in {os.path.basename(INVENTORY_FILE)}")
            if not dry_run:
                with open(INVENTORY_FILE, 'w', encoding='utf-8') as f:
                    f.write(new_inv)
            total_changes += 1
            files_updated += 1

    print(f"\nSummary: {total_changes} changes across {files_updated} files.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", action="store_true")
    args = parser.parse_args()
    
    run_fix(dry_run=not args.run)
