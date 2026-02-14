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
INVENTUR_FILE = LOGS_DIR / "Archive" / "INVENTUR_QUELLEN.md"
ORGANISATIONS_REGISTER = WIKI_DIR / "00_Fundament" / "Organisationsregister.md"

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
        "organisations_count": 0,
        "places_count": 0,
        "bestiary_count": 0,
        "files_per_category": Counter(),
        "words_per_category": Counter(),
        "link_hubs": Counter(),
        "source_fidelity": Counter()
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
        stats["files_per_category"][category] += 1
        
        if "07_Persoenlichkeiten" in str(md_file):
            stats["personalities_count"] += 1
        elif "02_Geografie" in str(md_file):
            stats["places_count"] += 1
        elif "08_Bestiarium" in str(md_file):
            stats["bestiary_count"] += 1
        elif "03_Gesellschaft" in str(md_file):
             stats["organisations_count"] += 1

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
        stats["words_per_category"][category] += words
        
        links = re.findall(r'\[\[([^\]]+)\]\]', content)
        stats["total_links"] += len(links)
        for link in links:
            target = link.split('|')[0].split('#')[0].strip()
            stats["link_hubs"][target] += 1
            
        # Source Fidelity (quelle: in frontmatter)
        if re.search(r'^quelle:', content, re.MULTILINE):
            stats["source_fidelity"]["with_source"] += 1
        else:
            stats["source_fidelity"]["no_source"] += 1

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
    density = stats["total_links"] / (stats["total_word_count"] / 1000) if stats["total_word_count"] > 0 else 0
    
    md = f"""---
layout: wiki_page
title: Wiki Status
category: Index
---

# 📊 Wiki Status

**Letztes Update:** {stats['timestamp']}

---

## 🏛️ Kern-Metriken

| Metrik | Wert |
| :--- | :--- |
| **Artikel** | {stats['total_files']} |
| **Worte (Gesamt)** | {stats['total_word_count']:,} |
| **Vernetzung** | {density:.2f} Links/1k |
| **Persönlichkeiten** | {stats['personalities_count']} |

---

## 📂 Kategorien

```mermaid
pie title Artikel nach Sektion
{"\n".join([f'    "{k}" : {v}' for k, v in stats["files_per_category"].items() if v > 0])}
```

---

## 🏆 Top Hubs
Die am stärksten vernetzten Artikel.

| Entität | Links |
| :--- | :--- |
"""
    for name, count in stats["link_hubs"].most_common(5):
        md += f"| [[{name}]] | {count} |\n"

    md += """
---
> [!NOTE]
> Fokus auf Essenz. Weniger Rauschen, mehr Lore.
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
