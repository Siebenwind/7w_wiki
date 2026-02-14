#!/usr/bin/env python3
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime
from collections import Counter

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
WIKI_DIR = PROJECT_ROOT / "Siebenwind_Wiki"
LOGS_DIR = PROJECT_ROOT / "Logs"
OUTPUT_FILE = WIKI_DIR / "10_Archiv" / "Wiki_Statistiken.md"
ORGANISATIONS_REGISTER = WIKI_DIR / "00_Fundament" / "Organisationsregister.md"

def collect_stats():
    stats = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_word_count": 0,
        "total_links": 0,
        "total_files": 0,
        "personalities_count": 0,
        "files_per_category": Counter(),
        "link_hubs": Counter(),
    }

    for md_file in WIKI_DIR.rglob("*.md"):
        if md_file.name == "Wiki_Statistiken.md":
            continue
            
        stats["total_files"] += 1
        content = md_file.read_text(encoding="utf-8")
        
        rel_path = md_file.relative_to(WIKI_DIR)
        category = rel_path.parts[0] if len(rel_path.parts) > 1 else "Root"
        stats["files_per_category"][category] += 1
        
        if "07_Persoenlichkeiten" in str(md_file):
            stats["personalities_count"] += 1

        words = len(re.findall(r'\w+', content))
        stats["total_word_count"] += words
        
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        stats["total_links"] += len(links)
        for link in links:
            target = link.split('|')[0].split('#')[0].strip()
            stats["link_hubs"][target] += 1

    return stats

def generate_markdown(stats):
    md = f"""---
layout: wiki_page
title: Wiki Status
category: Index
---

# 📊 Wiki Status

**Stand:** {stats['timestamp']}

---

| Metrik | Wert |
| :--- | :--- |
| **Artikel** | {stats['total_files']} |
| **Worte** | {stats['total_word_count']:,} |
| **Personen** | {stats['personalities_count']} |

---

```mermaid
pie title Sektionen
{"\n".join([f'    "{k}" : {v}' for k, v in stats['files_per_category'].items() if v > 10])}
```

---

## 🏆 Hubs
Die am stärksten vernetzten Artikel.

| Entität | Links |
| :--- | :--- |
"""
    for name, count in stats["link_hubs"].most_common(5):
        md += f"| [[{name}]] | {count} |\n"

    md += """
---
> [!NOTE]
> Die Essenz der Lore. Bewahrung durch Diskretion.
"""
    return md

if __name__ == "__main__":
    data = collect_stats()
    markdown_content = generate_markdown(data)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(markdown_content, encoding="utf-8")
    print(f"Stats generated at {OUTPUT_FILE}")
