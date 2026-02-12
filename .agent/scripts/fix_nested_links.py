import os
import re

WIKI_ROOT = "/Users/alexandrerabe/siebenwind/7w_wiki/Siebenwind_Wiki"

def fix_nested_links():
    pattern = re.compile(r"\[\[(.*?)\[\[(.*?)\]\](.*?)\]\]")
    for root, _, files in os.walk(WIKI_ROOT):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()
                
                if pattern.search(content):
                    print(f"Fixing nested links in {filepath}")
                    new_content = pattern.sub(r"[[\1\2\3]]", content)
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(new_content)

if __name__ == "__main__":
    fix_nested_links()
