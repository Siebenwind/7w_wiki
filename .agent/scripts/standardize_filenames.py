import os
import re

WIKI_ROOT = "/Users/alexandrerabe/siebenwind/7w_wiki/Siebenwind_Wiki"

def standardize():
    rename_map = {}
    
    # 1. First pass: determine new names
    for root, dirs, files in os.walk(WIKI_ROOT):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                    title_match = re.search(r"title:\s*(.*)", content)
                    if title_match:
                        title = title_match.group(1).strip()
                        if title.lower() == "index":
                            continue
                        
                        # New filename: Title with underscores, no prefix
                        new_name = title.replace(" ", "_") + ".md"
                        if file != new_name:
                            rename_map[filepath] = os.path.join(root, new_name)

    # 2. Second pass: Rename files
    # Note: We might have collisions if we are not careful, but let's assume titles are unique for now.
    for old, new in rename_map.items():
        print(f"Renaming {old} -> {new}")
        os.rename(old, new)

if __name__ == "__main__":
    standardize()
