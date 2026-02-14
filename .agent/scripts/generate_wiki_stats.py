#!/usr/bin/env python3
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
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

    # 3. Git Activity (recent changes)
    stats["activity"] = collect_git_activity()

    return stats

def collect_git_activity():
    """Collect recent file changes from git history."""
    activity = {"day": {"new": 0, "modified": 0}, "week": {"new": 0, "modified": 0}, "month": {"new": 0, "modified": 0}, "recent_files": []}
    
    try:
        # Check if we're in a git repo
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=str(PROJECT_ROOT), capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        return activity

    periods = {
        "day": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
        "week": (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d"),
        "month": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
    }

    for period_name, since_date in periods.items():
        try:
            # New files (A = added)
            result = subprocess.run(
                ["git", "log", f"--since={since_date}", "--diff-filter=A", "--name-only", "--pretty=format:", "--", "Siebenwind_Wiki/"],
                cwd=str(PROJECT_ROOT), capture_output=True, text=True, timeout=10
            )
            new_files = set(f for f in result.stdout.strip().split("\n") if f.strip() and f.endswith(".md"))
            activity[period_name]["new"] = len(new_files)

            # Modified files (M = modified)
            result = subprocess.run(
                ["git", "log", f"--since={since_date}", "--diff-filter=M", "--name-only", "--pretty=format:", "--", "Siebenwind_Wiki/"],
                cwd=str(PROJECT_ROOT), capture_output=True, text=True, timeout=10
            )
            mod_files = set(f for f in result.stdout.strip().split("\n") if f.strip() and f.endswith(".md"))
            activity[period_name]["modified"] = len(mod_files)
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
            pass

    # Recent files (last 15 changes with dates)
    try:
        result = subprocess.run(
            ["git", "log", "--since=" + periods["month"], "--diff-filter=AM", "--name-status", "--pretty=format:%ai", "--", "Siebenwind_Wiki/"],
            cwd=str(PROJECT_ROOT), capture_output=True, text=True, timeout=10
        )
        seen = set()
        current_date = ""
        for line in result.stdout.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            if re.match(r'\d{4}-\d{2}-\d{2}', line):
                current_date = line[:10]
            elif "\t" in line:
                status, filepath = line.split("\t", 1)
                if filepath.endswith(".md") and filepath not in seen:
                    seen.add(filepath)
                    basename = Path(filepath).stem.replace("_", " ")
                    category = Path(filepath).parts[1] if len(Path(filepath).parts) > 1 else "Root"
                    action = "Neu" if status == "A" else "Geändert"
                    activity["recent_files"].append((current_date, action, basename, category))
                    if len(activity["recent_files"]) >= 15:
                        break
    except (subprocess.TimeoutExpired, subprocess.CalledProcessError):
        pass

    return activity

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

## 🏆 Top 10 Best-Dokumentierte Persönlichkeiten
(Basierend auf geschätztem Umfang/Relevanz)

| Rang | Persönlichkeit | Umfang (Worte) | Links |
| :--- | :--- | :--- | :--- |
"""
    # Helper to get word count for a file
    def get_word_count(name):
        # Scan wiki for file with this name
        for f in WIKI_DIR.rglob(f"{name}.md"):
            return len(re.findall(r'\w+', f.read_text(encoding="utf-8")))
        return 0

    # Collect personalities with significant content
    personas = []
    # We use link_hubs keys that are in 07_Persoenlichkeiten
    # Or just iterate all files in 07_Persoenlichkeiten
    for f in (WIKI_DIR / "07_Persoenlichkeiten").rglob("*.md"):
        name = f.stem
        words = len(re.findall(r'\w+', f.read_text(encoding="utf-8")))
        links_in = stats["link_hubs"].get(name, 0)
        personas.append((name, words, links_in))
    
    # Sort by word count desc
    top_personas = sorted(personas, key=lambda x: x[1], reverse=True)[:10]

    for i, (name, words, links) in enumerate(top_personas, 1):
        md += f"| {i} | [[{name}]] | {words} | {links} |\n"

    md += """
---

## 🔗 Zentrale Wissensknoten (Top Hubs)
Die am häufigsten verlinkten Artikel im Wiki.

| Rang | Entität | Verlinkungen |
| :--- | :--- | :--- |
"""
    for i, (name, count) in enumerate(top_hubs, 1):
        md += f"| {i} | [[{name}]] | {count} |\n"

    # Recent Activity Section
    act = stats.get("activity", {})
    day = act.get("day", {})
    week = act.get("week", {})
    month = act.get("month", {})

    md += f"""
---

## 📅 Aktivität (Letzte Änderungen)

| Zeitraum | Neue Artikel | Geänderte Artikel |
| :--- | :--- | :--- |
| **Letzte 24h** | {day.get('new', 0)} | {day.get('modified', 0)} |
| **Letzte 7 Tage** | {week.get('new', 0)} | {week.get('modified', 0)} |
| **Letzte 30 Tage** | {month.get('new', 0)} | {month.get('modified', 0)} |
"""

    recent = act.get("recent_files", [])
    if recent:
        md += """\n### Letzte Änderungen\n\n| Datum | Aktion | Artikel | Kategorie |\n| :--- | :--- | :--- | :--- |\n"""
        for date, action, name, cat in recent:
            md += f"| {date} | {action} | {name} | {cat} |\n"

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
