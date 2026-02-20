#!/usr/bin/env python3
import os
import re
import nexus_config

def get_h1(file_path):
    """Extracts the first H1 from a markdown file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                match = re.match(r'^#\s+(.*)', line)
                if match:
                    return match.group(1).strip()
    except Exception:
        pass
    return None

def generate_indices(target_dir):
    """Recursively generates index.md files for each directory."""
    for root, dirs, files in os.walk(target_dir):
        # Skip root itself if needed, but here we want indices for all subfolders
        if root == target_dir:
            continue

        rel_dir = os.path.relpath(root, target_dir)
        category_name = os.path.basename(root)
        # Clean up numeric prefix for title
        category_title = category_name.split("_", 1)[-1] if "_" in category_name else category_name
        category_title = category_title.replace("_", " ")

        index_path = os.path.join(root, "index.md")
        
        md_files = [f for f in files if f.endswith(".md") and f != "index.md"]
        sub_dirs = [d for d in dirs if not d.startswith(".")]

        content = [
            "---",
            "layout: wiki_page",
            f"title: {category_title}",
            "---",
            "",
            f"# [[{nexus_config.WORLD_NAME}]] Wiki - {category_title}",
            "Das Archiv der " + category_title + ".",
            "",
            "## Inhalte",
            ""
        ]

        # List subdirectories
        if sub_dirs:
            content.append("### Kategorien")
            for d in sorted(sub_dirs):
                d_title = d.split("_", 1)[-1] if "_" in d else d
                d_title = d_title.replace("_", " ")
                content.append(f"*   **[[{d}/index|{d_title}]]**")
            content.append("")

        # List markdown files
        if md_files:
            content.append("### Artikel")
            for f in sorted(md_files):
                f_path = os.path.join(root, f)
                title = get_h1(f_path) or f[:-3].replace("_", " ")
                content.append(f"*   [[{f[:-3]}|{title}]]")

        with open(index_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(content) + "\n")
        
        print(f"Generated index for {rel_dir}")

if __name__ == "__main__":
    wiki_root = str(nexus_config.WIKI_DIR)
    if os.path.exists(wiki_root):
        generate_indices(wiki_root)
    else:
        print(f"Error: Wiki root not found at {wiki_root}")
