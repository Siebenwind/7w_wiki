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


def normalize_wikilink_target(target: str) -> str:
    clean = target.strip().replace(" ", "_")
    clean = re.sub(r"_+", "_", clean)
    return clean.casefold()


def denormalize_for_link(target_norm: str) -> str:
    return target_norm.replace(" ", "_")


def is_structural_target(target_norm: str) -> bool:
    base = target_norm.split("/")[-1]
    exact_blocklist = {
        "index",
        "die_chronik",
        "chronik",
        "geschichte",
        "wiki_statistiken",
        "personenregister",
        "organisationsregister",
        "bestiarium_register",
        "archiv_register",
        "persoenlichkeiten_uebersicht",
        "inhaltsverzeichnis",
    }
    if base in exact_blocklist:
        return True
    if base.endswith("_register") or base.endswith("register"):
        return True
    if "index" in base or "uebersicht" in base:
        return True
    return False

def collect_stats():
    stats = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_word_count": 0,
        "total_links": 0,
        "total_files": 0,
        "personalities_count": 0,
        "files_per_category": Counter(),
        "link_hubs": Counter(),
        "personality_hubs": Counter(),
        "event_hubs": Counter(),
    }

    personalities_lookup = {}
    events_lookup = {}
    article_lookup = {}

    for md_file in WIKI_DIR.rglob("*.md"):
        if md_file.name == "Wiki_Statistiken.md":
            continue
        rel_path = md_file.relative_to(WIKI_DIR)
        stem = md_file.stem
        target_norm = normalize_wikilink_target(stem)
        article_lookup[target_norm] = stem
        if "07_Persoenlichkeiten" in str(rel_path):
            personalities_lookup[target_norm] = stem
        if "04_Chronik" in str(rel_path) or "05_Geschichte" in str(rel_path):
            events_lookup[target_norm] = stem

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
            target_raw = link.split('|')[0].split('#')[0].strip()
            target_norm = normalize_wikilink_target(target_raw)
            if not target_norm:
                continue
            if not is_structural_target(target_norm):
                stats["link_hubs"][target_norm] += 1
            if target_norm in personalities_lookup and not is_structural_target(target_norm):
                stats["personality_hubs"][target_norm] += 1
            if target_norm in events_lookup and not is_structural_target(target_norm):
                stats["event_hubs"][target_norm] += 1

    stats["personality_lookup"] = personalities_lookup
    stats["events_lookup"] = events_lookup
    stats["article_lookup"] = article_lookup
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
Leserrelevante, stark vernetzte Artikel (ohne Index/Register).

| Entität | Links |
| :--- | :--- |
"""
    for name_norm, count in stats["link_hubs"].most_common(5):
        display = stats["article_lookup"].get(name_norm, denormalize_for_link(name_norm))
        md += f"| [[{display}]] | {count} |\n"

    md += """

## 👤 Top Persönlichkeiten
| Persönlichkeit | Links |
| :--- | :--- |
"""
    for name_norm, count in stats["personality_hubs"].most_common(5):
        display = stats["personality_lookup"].get(name_norm, denormalize_for_link(name_norm))
        md += f"| [[{display}]] | {count} |\n"

    md += """

## 🕰️ Top Ereignisse
| Ereignis | Links |
| :--- | :--- |
"""
    for name_norm, count in stats["event_hubs"].most_common(5):
        display = stats["events_lookup"].get(name_norm, denormalize_for_link(name_norm))
        md += f"| [[{display}]] | {count} |\n"

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
