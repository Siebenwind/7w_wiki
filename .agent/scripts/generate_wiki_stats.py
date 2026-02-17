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
INGESTION_REPORTS_DIR = LOGS_DIR / "Ingestion"
TRACKING_REGISTER_FILE = LOGS_DIR / "INGESTION_TRACKING_REGISTER.md"


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


def _extract_first(raw: str, patterns: list[str]) -> str:
    for pattern in patterns:
        match = re.search(pattern, raw, re.MULTILINE)
        if match:
            return match.group(1).strip()
    return ""


def parse_ingestion_report(report_path: Path) -> dict:
    raw = report_path.read_text(encoding="utf-8")
    report_id = _extract_first(raw, [r"Report-ID:\s*\[?([0-9a-fA-F-]{36})\]?"]) or report_path.stem
    source = _extract_first(raw, [r"- \*\*Quelle\*\*:\s*`?(.+?)`?\s*$"])
    evaluator = _extract_first(
        raw,
        [
            r"- \*\*Ausgewertet von\*\*:\s*(.+?)\s*$",
            r"- \*\*Verantwortlicher Agent\*\*:\s*(.+?)\s*$",
        ],
    )
    evaluated_at = _extract_first(
        raw,
        [
            r"- \*\*Auswertungszeitpunkt \(UTC\)\*\*:\s*(.+?)\s*$",
            r"- \*\*Datum der Verarbeitung\*\*:\s*(.+?)\s*$",
        ],
    )
    workflow = _extract_first(raw, [r"- \*\*Workflow/Skill\*\*:\s*(.+?)\s*$"])
    dispatch_ref = _extract_first(raw, [r"- \*\*Dispatch-Referenz\*\*:\s*(.+?)\s*$"])

    lqs = _extract_first(
        raw,
        [
            r"\*\*Gesamt \(LQS(?: 0-10)?\)\*\*\s*\|\s*\*\*([0-9]+(?:\.[0-9]+)?)\/10\*\*",
            r"- \*\*Lore-Score \(LQS\)\*\*:\s*([0-9]+(?:\.[0-9]+)?)\/10",
        ],
    )

    quality_profile = _extract_first(raw, [r"- \*\*Quality-Profil \(A/T/K/B/U\)\*\*:\s*([0-9/]+)\s*$"])
    if not quality_profile:
        a = _extract_first(raw, [r"\| \*\*Abdeckung\*\* \|\s*([0-9]+)\s*\|", r"\| \*\*A: Abdeckung\*\* \|\s*([0-9]+)\s*\|"])
        t = _extract_first(raw, [r"\| \*\*Tiefe\*\* \|\s*([0-9]+)\s*\|", r"\| \*\*T: Tiefe\*\* \|\s*([0-9]+)\s*\|"])
        k = _extract_first(raw, [r"\| \*\*Konsistenz\*\* \|\s*([0-9]+)\s*\|", r"\| \*\*K: Kanon-Konsistenz\*\* \|\s*([0-9]+)\s*\|"])
        if a and t and k:
            quality_profile = f"{a}/{t}/{k}"

    return {
        "report_file": str(report_path.relative_to(PROJECT_ROOT)),
        "report_id": report_id,
        "source": source or "[UNGEKLAERT]",
        "evaluator": evaluator or "[UNGEKLAERT]",
        "evaluated_at": evaluated_at or "[UNGEKLAERT]",
        "workflow": workflow or "N/A",
        "dispatch_ref": dispatch_ref or "N/A",
        "lqs": lqs or "",
        "quality_profile": quality_profile or "",
        "has_core_tracking": bool(source and evaluator and evaluated_at),
    }


def collect_ingestion_tracking() -> dict:
    entries: list[dict] = []
    if INGESTION_REPORTS_DIR.exists():
        for report_path in sorted(INGESTION_REPORTS_DIR.glob("*.md")):
            try:
                entries.append(parse_ingestion_report(report_path))
            except Exception:
                continue

    # Latest first where possible; unknown timestamps at the end.
    entries.sort(key=lambda x: x["evaluated_at"] if x["evaluated_at"] != "[UNGEKLAERT]" else "", reverse=True)

    lqs_counter = Counter()
    profile_counter = Counter()
    for entry in entries:
        if entry["lqs"]:
            lqs_counter[entry["lqs"]] += 1
        if entry["quality_profile"]:
            profile_counter[entry["quality_profile"]] += 1

    top_profiles = ", ".join([f"{p} ({n})" for p, n in profile_counter.most_common(3)]) or "[UNGEKLAERT]"

    return {
        "entries": entries,
        "total_reports": len(entries),
        "with_core_tracking": sum(1 for e in entries if e["has_core_tracking"]),
        "with_lqs": sum(1 for e in entries if e["lqs"]),
        "lqs_counter": lqs_counter,
        "profile_counter": profile_counter,
        "top_profiles": top_profiles,
    }


def build_tracking_register_markdown(tracking: dict) -> str:
    now_utc = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    lines: list[str] = []
    lines.append("---")
    lines.append("uuid: 6af36c09-c985-4de8-9dc5-9680b9de9b5b")
    lines.append("status: ACTIVE")
    lines.append(f"updated_at: {now_utc}")
    lines.append('epistemic: "#meta"')
    lines.append("---")
    lines.append("")
    lines.append("# INGESTION_TRACKING_REGISTER")
    lines.append("")
    lines.append("Zentrales Tracking fuer Ingestion-Auswertungen (wer/wann/wie + Scoreprofil).")
    lines.append("")
    lines.append("> Dieses Dokument wird durch `./7w_wiki.py stats` aktualisiert.")
    lines.append("")
    lines.append("## Snapshot")
    lines.append("")
    lines.append(f"- Reports gesamt: {tracking['total_reports']}")
    lines.append(f"- Reports mit Tracking-Kernfeldern: {tracking['with_core_tracking']}")
    lines.append(f"- Reports mit LQS: {tracking['with_lqs']}")
    lines.append(f"- Dominante Score-Cluster: {tracking['top_profiles']}")
    lines.append("")
    lines.append("## Register")
    lines.append("")
    lines.append("| Report | Quelle | Ausgewertet von | Auswertungszeitpunkt (UTC) | Workflow/Skill | Dispatch | LQS | Profil |")
    lines.append("|---|---|---|---|---|---|---|---|")

    for entry in tracking["entries"]:
        report = f"`{entry['report_file']}`"
        source = entry["source"].replace("|", "\\|")
        evaluator = entry["evaluator"].replace("|", "\\|")
        evaluated_at = entry["evaluated_at"].replace("|", "\\|")
        workflow = entry["workflow"].replace("|", "\\|")
        dispatch = entry["dispatch_ref"].replace("|", "\\|")
        lqs = entry["lqs"] or "N/A"
        profile = entry["quality_profile"] or "N/A"
        lines.append(f"| {report} | {source} | {evaluator} | {evaluated_at} | {workflow} | {dispatch} | {lqs} | {profile} |")

    return "\n".join(lines).rstrip() + "\n"


def generate_markdown(stats, tracking):
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
| **Ingestion-Reports** | {tracking['total_reports']} |
| **Tracking vollständig** | {tracking['with_core_tracking']} |

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

    md += f"""

## 🧾 Ingestion Tracking

| Metrik | Wert |
| :--- | :--- |
| Reports gesamt | {tracking['total_reports']} |
| Reports mit Kern-Tracking (Quelle + Wer + Wann) | {tracking['with_core_tracking']} |
| Reports mit LQS | {tracking['with_lqs']} |
| Dominante Score-Cluster | {tracking['top_profiles']} |

"""

    md += """
---
> [!NOTE]
> Die Essenz der Lore. Bewahrung durch Diskretion.
"""
    return md

if __name__ == "__main__":
    data = collect_stats()
    tracking = collect_ingestion_tracking()
    markdown_content = generate_markdown(data, tracking)
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(markdown_content, encoding="utf-8")
    TRACKING_REGISTER_FILE.write_text(build_tracking_register_markdown(tracking), encoding="utf-8")
    print(f"Stats generated at {OUTPUT_FILE}")
    print(f"Tracking register updated at {TRACKING_REGISTER_FILE}")
