import os
import re

WIKI_PATH = "/Users/alexandrerabe/siebenwind/7w_wiki/Siebenwind_Wiki"

def check_integrity():
    all_pages = {}
    links = []
    
    # 1. Collect all pages
    for root, _, files in os.walk(WIKI_PATH):
        for f in files:
            if f.endswith(".md"):
                page_name = f.replace(".md", "")
                all_pages[page_name] = os.path.join(root, f)
                
                # 2. Extract links
                with open(os.path.join(root, f), "r") as file:
                    content = file.read()
                    found_links = re.findall(r"\[\[(.*?)\]\]", content)
                    for l in found_links:
                        links.append({"from": page_name, "to": l})

    # 3. Analyze
    broken_links = [l for l in links if l['to'] not in all_pages]
    
    linked_pages = set(l['to'] for l in links)
    orphans = [p for p in all_pages if p not in linked_pages and p not in ["index", "Das_Fundament", "Das_Pantheon", "Geografie", "Gesellschaft", "Die_Chronik", "Erzählungen", "Persönlichkeiten", "Die_Archive"]]

    print(f"--- Wiki Integrity Report ---")
    print(f"Total Pages: {len(all_pages)}")
    print(f"Broken Links: {len(broken_links)}")
    for bl in broken_links:
        print(f"  - {bl['from']} -> {bl['to']} (MISSING)")
        
    print(f"Orphaned Pages: {len(orphans)}")
    for o in orphans:
        print(f"  - {o}")

if __name__ == "__main__":
    check_integrity()
