import os
import re

def cleanup_links(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Convert internal absolute wiki links: [Name](file:///.../Wiki/Path/Page.md) -> [[Page]]
    # This pattern catches [Text](file:///.../Siebenwind_Wiki/.../Page.md)
    # We want to extract the final filename without extension
    def internal_replica(match):
        path = match.group(2)
        filename = os.path.splitext(os.path.basename(path))[0]
        return f"[[{filename}]]"

    # Pattern: \[(.*?)\]\(file:///.*?/Siebenwind_Wiki/(.*?)\.md\)
    content = re.sub(r'\[(.*?)\]\(file:///.*?/Siebenwind_Wiki/(.*?)\.md\)', internal_replica, content)

    # 2. Cleanup other absolute references (like Quellen)
    # [Text](file:///.../Quellen/...) -> Text
    def source_replica(match):
        text = match.group(1)
        return text

    content = re.sub(r'\[(.*?)\]\(file:///.*?/Quellen/(.*?)\)', source_replica, content)

    # 3. Handle stray absolute file paths not in markdown link syntax if any
    content = re.sub(r'file:///Users/alexandrerabe/siebenwind/7w_wiki/Siebenwind_Wiki/.*?/(.*?)\.md', r'[[\1]]', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    wiki_root = "/Users/alexandrerabe/siebenwind/7w_wiki/Siebenwind_Wiki/"
    for root, dirs, files in os.walk(wiki_root):
        for file in files:
            if file.endswith(".md"):
                cleanup_links(os.path.join(root, file))
