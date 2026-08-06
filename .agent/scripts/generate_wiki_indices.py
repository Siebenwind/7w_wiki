#!/usr/bin/env python3
from __future__ import annotations

import os
import re
from pathlib import Path

import nexus_config
from content_contract import TECHNICAL_WIKI_ROOT


def get_h1(file_path: Path) -> str | None:
    try:
        for line in file_path.read_text(encoding="utf-8").splitlines():
            match = re.match(r"^#\s+(.*)", line)
            if match:
                return match.group(1).strip()
    except Exception:
        return None
    return None


def generate_indices(target_dir: Path) -> None:
    for root, dirs, files in os.walk(target_dir):
        root_path = Path(root)
        if root_path == target_dir:
            continue

        rel_dir = root_path.relative_to(target_dir)
        category_name = root_path.name
        category_title = category_name.split("_", 1)[-1] if "_" in category_name else category_name
        category_title = category_title.replace("_", " ")
        page_title = f"{nexus_config.WORLD_NAME} Wiki - {category_title}"
        index_path = root_path / "index.md"

        md_files = [f for f in files if f.endswith(".md") and f != "index.md"]
        sub_dirs = [d for d in dirs if not d.startswith(".")]

        content = [
            "---",
            f'title: "{page_title}"',
            f"category: {category_title}",
            "---",
            "",
            f"# {page_title}",
            "",
            f"Indexseite fuer die Sektion {category_title}.",
            "",
            "## Inhalte",
            "",
        ]

        if sub_dirs:
            content.append("### Kategorien")
            for directory in sorted(sub_dirs):
                d_title = directory.split("_", 1)[-1] if "_" in directory else directory
                d_title = d_title.replace("_", " ")
                content.append(f"* **[[{directory}/index|{d_title}]]**")
            content.append("")

        if md_files:
            content.append("### Artikel")
            for file_name in sorted(md_files):
                file_path = root_path / file_name
                title = get_h1(file_path) or file_name[:-3].replace("_", " ")
                content.append(f"* [[{file_name[:-3]}|{title}]]")
            content.append("")

        index_path.write_text("\n".join(content).rstrip() + "\n", encoding="utf-8")
        print(f"Generated index for {rel_dir}")


if __name__ == "__main__":
    wiki_root = Path(nexus_config.WIKI_DIR)
    if not wiki_root.exists():
        wiki_root = TECHNICAL_WIKI_ROOT
    if wiki_root.exists():
        generate_indices(wiki_root)
    else:
        print(f"Error: Wiki root not found at {wiki_root}")
