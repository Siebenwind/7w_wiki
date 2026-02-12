import os
import re

QUELLE_PATH = "/Users/alexandrerabe/siebenwind/7w_wiki/Quellen"
WIKI_PATH = "/Users/alexandrerabe/siebenwind/7w_wiki/Siebenwind_Wiki"
INVENTUR_FILE = "/Users/alexandrerabe/siebenwind/7w_wiki/Logs/INVENTUR_QUELLEN.md"

def get_wiki_filenames():
    wiki_files = set()
    for root, _, files in os.walk(WIKI_PATH):
        for f in files:
            if f.endswith(".md"):
                wiki_files.add(f.replace(".md", ""))
    return wiki_files

def scan_sources():
    sources = []
    wiki_filenames = get_wiki_filenames()
    
    for root, dirs, files in os.walk(QUELLE_PATH):
        if "_ARCHIV_ORIGINAL" in root:
            continue
        for f in files:
            if f.startswith(".") or f == "INVENTUR_QUELLEN.md" or not f.endswith(".md"):
                continue
            
            full_path = os.path.join(root, f)
            rel_path = os.path.relpath(full_path, QUELLE_PATH)
            size = os.path.getsize(full_path)
            ext = os.path.splitext(f)[1]
            
            # Simple check for integration: does a wiki file exist with the same name?
            clean_name = os.path.splitext(f)[0].replace(" ", "_")
            status = "Integrated" if clean_name in wiki_filenames else "Pending"
            
            sources.append({
                "name": f,
                "rel_path": rel_path,
                "type": ext,
                "size": size,
                "status": status
            })
    return sources

def update_inventur(sources):
    with open(INVENTUR_FILE, "r") as f:
        content = f.read()
    
    # This is a simplified update logic. 
    # In a real scenario, we would parse the tables and update statuses.
    # For now, we report the findings.
    print(f"Scanned {len(sources)} files in /Quellen/")
    integrated = [s for s in sources if s['status'] == 'Integrated']
    pending = [s for s in sources if s['status'] == 'Pending']
    import json
    with open("/Users/alexandrerabe/siebenwind/7w_wiki/Logs/pending_sources.json", "w") as f:
        json.dump(pending, f, indent=2)
    print(f"Status: {len(integrated)} Integrated, {len(pending)} Pending.")
    print("Pending sources written to Logs/pending_sources.json")

if __name__ == "__main__":
    found_sources = scan_sources()
    update_inventur(found_sources)
