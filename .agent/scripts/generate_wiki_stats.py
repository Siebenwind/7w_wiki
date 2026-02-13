#!/usr/bin/env python3
import os
import re
from pathlib import Path
from datetime import datetime
from collections import Counter

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
WIKI_DIR = PROJECT_ROOT / "Siebenwind_Wiki"
QUELLEN_DIR = PROJECT_ROOT / "Quellen"
LOGS_DIR = PROJECT_ROOT / "Logs"
OUTPUT_FILE = WIKI_DIR / "10_Archiv" / "Wiki_Statistiken.md"
INVENTUR_FILE = LOGS_DIR / "INVENTUR_QUELLEN.md"

def has_frontmatter(content):
    return content.startswith('---') and '---' in content[3:]

def collect_stats():
    stats = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "categories": {},
        "epistemic": Counter(),
        "total_word_count": 0,
        "total_links": 0,
        "total_files": 0,
        "ingestion": {"Integrated": 0, "Pending": 0, "Done": 0},
        "temporal": Counter(),
        "personalities_count": 0,
        "link_hubs": Counter()
    }

    # 1. Ingestion Stats from INVENTUR_QUELLEN.md
    if INVENTUR_FILE.exists():
        content = INVENTUR_FILE.read_text(encoding="utf-8")
        stats["ingestion"]["Integrated"] = len(re.findall(r'\| Integrated \|', content))
        stats["ingestion"]["Pending"] = len(re.findall(r'\| Pending \|', content))
        stats["ingestion"]["Done"] = len(re.findall(r'\| Done \|', content))

    # 2. Iterate Wiki Files
    for md_file in WIKI_DIR.rglob("*.md"):
        if md_file.name == "Wiki_Statistiken.md":
            continue
            
        stats["total_files"] += 1
        content = md_file.read_text(encoding="utf-8")
        
        # Category (folder based or FM)
        rel_path = md_file.relative_to(WIKI_DIR)
        category = rel_path.parts[0] if len(rel_path.parts) > 1 else "Root"
        stats["categories"][category] = stats["categories"].get(category, 0) + 1
        
        if "07_Persoenlichkeiten" in str(md_file):
            stats["personalities_count"] += 1

        # Frontmatter check
        if has_frontmatter(content):
            pass # We could extract specific fields here if needed
        
        # Extract Epistemic Tags from content
        tags = re.findall(r'#(canon|bote|perspektive|überlieferung)', content.lower())
        for tag in tags:
            stats["epistemic"][tag] += 1

        # Temporal Density (Years n.H.)
        years = re.findall(r'(\d+)\s+n\.H\.', content)
        for year in years:
            stats["temporal"][year] += 1

        # Word Count & Links
        words = len(re.findall(r'\w+', content))
        stats["total_word_count"] += words
        
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        stats["total_links"] += len(links)
        for link in links:
            # Normalize link (remove section, alias)
            target = link.split('|')[0].split('#')[0].strip()
            stats["link_hubs"][target] += 1

    return stats

def generate_markdown(stats):
    # Calculate density
    density = stats["total_links"] / (stats["total_word_count"] / 1000) if stats["total_word_count"] > 0 else 0
    
    # Top Hubs
    top_hubs = stats["link_hubs"].most_common(10)
    
    # Sort temporal stats
    sorted_years = sorted(stats["temporal"].items(), key=lambda x: int(x[0]) if x[0].isdigit() else 999)
    top_years = sorted_years[-15:] # Last 15 mentioned years

    md = f"""---
layout: wiki_page
title: Wiki Statistiken
category: Index
---

# Wiki Statistiken

**Letztes Update:** {stats["timestamp"]}

## 📊 High-Level KPIs

| Metrik | Wert |
| :--- | :--- |
| **Gesamtanzahl Artikel** | {stats["total_files"]} |
| **Bekannte Persönlichkeiten** | {stats["personalities_count"]} |
| **Gesamtwortzahl** | {stats["total_word_count"]:,} |
| **Vernetzungsgrad (Links/1k Worte)** | {density:.2f} |

---

## 📥 Ingestions-Status (Quellen)

```mermaid
pie title Quellen Integrations-Status
    "Integriert" : {stats["ingestion"]["Integrated"] + stats["ingestion"]["Done"]}
    "Ausstehend" : {stats["ingestion"]["Pending"]}
```

---

## 📂 Verteilung nach Kategorien

```mermaid
bar-chart
    title Artikel pro Kategorie
    x-axis [ {", ".join([f'"{k}"' for k in stats["categories"].keys()])} ]
    y-axis Artikel [ {", ".join([str(v) for v in stats["categories"].values()])} ]
```

---

## ⚖️ Epistemische Sicherheit

```mermaid
pie title Wissens-Fundament
    "Canon" : {stats["epistemic"]["canon"]}
    "Bote" : {stats["epistemic"]["bote"]}
    "Überlieferung" : {stats["epistemic"]["überlieferung"]}
    "Perspektive" : {stats["epistemic"]["perspektive"]}
```

---

## ⏳ Lore-Evolution (Zeitliche Dichte)
Häufigkeit der Erwähnung von Jahren in der Zeitrechnung "n.H.".

```mermaid
xychart-beta
    title Erwähnungen pro Jahr (n.H.)
    x-axis [ {", ".join([f'"{y}"' for y, _ in top_years])} ]
    y-axis "Nennungen"
    bar [ {", ".join([str(c) for _, c in top_years])} ]
```

---

## 🏆 Zentrale Wissensknoten (Top Hubs)
Die am häufigsten verlinkten Artikel im Wiki.

| Rang | Entität | Verlinkungen |
| :--- | :--- | :--- |
"""
    for i, (name, count) in enumerate(top_hubs, 1):
        md += f"| {i} | [[{name}]] | {count} |\n"

    md += """
---
> [!NOTE]
> Diese Seite wird automatisch generiert. Sie dient der Übersicht über das Wachstum und die Qualität des Wissensarchivs.
"""
    return md

if __name__ == "__main__":
    print("Collecting statistics...")
    data = collect_stats()
    print("Generating Markdown...")
    markdown_content = generate_markdown(data)
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(markdown_content, encoding="utf-8")
    print(f"Statistics generated: {OUTPUT_FILE}")
