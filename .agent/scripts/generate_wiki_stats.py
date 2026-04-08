#!/usr/bin/env python3
import json
import re
import subprocess
import tempfile
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

from content_contract import HOMEPAGE_URL, INVENTORY_PATH, TRUTH_HIERARCHY, write_inventory
from nexus_config import WIKI_DIR, WORLD_NAME, WIKI_DIR_NAME

# Configuration
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LOGS_DIR = PROJECT_ROOT / "Logs"
ARCHIVE_DIR = LOGS_DIR / "Archive"
OUTPUT_FILE = WIKI_DIR / "10_Archiv" / "Wiki_Statistiken.md"
INGESTION_REPORTS_DIR = LOGS_DIR / "Ingestion"
TRACKING_REGISTER_FILE = LOGS_DIR / "INGESTION_TRACKING_REGISTER.md"
STATS_SNAPSHOT_DIR = ARCHIVE_DIR
STATS_SNAPSHOT_LATEST = STATS_SNAPSHOT_DIR / "STATS_SNAPSHOT_latest.json"

UNCLARIFIED_PATTERN = re.compile(r"\[UNGEKLAERT\]|\[UNGEKLÄRT\]", re.IGNORECASE)
EPI_PATTERN = re.compile(
    r"#(canon|bote|perspektive|ueberlieferung|überlieferung|news|meta|gemischt)",
    re.IGNORECASE,
)
INDEX_PLACEHOLDER_RE = re.compile(r"\[\[index\]\]", re.IGNORECASE)
PLACEHOLDER_MARKERS = (
    "[TBC]",
    "Platzhalter und wurde automatisch während des Konsistenz-Audits erstellt.",
    "Platzhalter und wurde automatisch waehrend des Konsistenz-Audits erstellt.",
)
GENERIC_PERSONALITY_BLOCKLIST = {
    "geist",
    "index",
    "magie",
    "persoenlichkeiten",
    "wikilink",
    "wikilinks",
}


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


def parse_frontmatter(raw: str) -> dict[str, str]:
    if not raw.startswith("---\n"):
        return {}
    lines = raw.splitlines()
    frontmatter: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip().lower()] = value.strip()
    return frontmatter


def is_resolved_quelle(value: str) -> bool:
    norm = value.strip().lower()
    if not norm:
        return False
    if "ungeklaert" in norm or "ungeklärt" in norm:
        return False
    if norm in {"n/a", "none", "null"}:
        return False
    return True


def extract_epistemic_tag(raw: str, frontmatter: dict[str, str]) -> str:
    value = frontmatter.get("epistemic", "")
    match = EPI_PATTERN.search(value)
    if not match:
        match = EPI_PATTERN.search(raw)
    if not match:
        return "unbekannt"
    tag = match.group(1).lower()
    if tag == "überlieferung":
        tag = "ueberlieferung"
    return tag


def safe_git_output(args: list[str]) -> str:
    cmd = ["git", "-C", str(PROJECT_ROOT)] + args
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return proc.stdout
    except Exception:
        return ""


def _git_activity_days(days: int) -> int:
    out = safe_git_output(
        ["log", f"--since={days} days ago", "--date=format:%Y-%m-%d", "--format=%ad", "--", WIKI_DIR_NAME]
    )
    active_days = {line.strip() for line in out.splitlines() if line.strip()}
    return len(active_days)


def collect_git_activity() -> dict:
    activity = {
        "changed_files_7d": 0,
        "changed_files_30d": 0,
        "changed_files_90d": 0,
        "active_days_7d": 0,
        "active_days_30d": 0,
        "active_days_90d": 0,
        "new_files_30d": 0,
        "commits_30d": 0,
    }

    for days, key in ((7, "changed_files_7d"), (30, "changed_files_30d"), (90, "changed_files_90d")):
        out = safe_git_output(
            ["log", f"--since={days} days ago", "--name-only", "--pretty=format:", "--", WIKI_DIR_NAME]
        )
        files = {
            line.strip()
            for line in out.splitlines()
            if line.strip().endswith(".md") and not line.strip().endswith("Wiki_Statistiken.md")
        }
        activity[key] = len(files)
        activity[f"active_days_{days}d"] = _git_activity_days(days)

    out_new = safe_git_output(
        ["log", "--since=30 days ago", "--diff-filter=A", "--name-only", "--pretty=format:", "--", WIKI_DIR_NAME]
    )
    new_files = {
        line.strip()
        for line in out_new.splitlines()
        if line.strip().endswith(".md") and not line.strip().endswith("Wiki_Statistiken.md")
    }
    activity["new_files_30d"] = len(new_files)

    out_commits = safe_git_output(["rev-list", "--count", "--since=30 days ago", "HEAD", "--", WIKI_DIR_NAME])
    try:
        activity["commits_30d"] = int(out_commits.strip())
    except Exception:
        activity["commits_30d"] = 0

    return activity


def _is_placeholder_article(raw: str) -> bool:
    return any(marker in raw for marker in PLACEHOLDER_MARKERS)


def _discover_test_report_paths() -> list[Path]:
    report_paths = sorted(ARCHIVE_DIR.glob("TEST_*.md"), key=lambda p: p.stat().st_mtime, reverse=True)
    temp_root = Path(tempfile.gettempdir())
    report_paths.extend(sorted(temp_root.glob("7w_test_*/TEST_*.md"), key=lambda p: p.stat().st_mtime, reverse=True))
    return sorted(set(report_paths), key=lambda p: p.stat().st_mtime, reverse=True)


def collect_ops_progress() -> dict:
    progress = {
        "latest_audit_file": "",
        "latest_audit_problems": 0,
        "previous_audit_file": "",
        "previous_audit_problems": 0,
        "latest_bridge_total": 0,
        "latest_bridge_without_exception": 0,
        "latest_tests": [],
        "passing_suites": 0,
        "failing_suites": 0,
    }

    audit_files = sorted(ARCHIVE_DIR.glob("Audit_*.txt"), key=lambda p: p.stat().st_mtime, reverse=True)
    if audit_files:
        latest_raw = audit_files[0].read_text(encoding="utf-8", errors="ignore")
        progress["latest_audit_file"] = str(audit_files[0].relative_to(PROJECT_ROOT))
        match = re.search(r"ERGEBNIS:\s*(\d+)\s+Probleme", latest_raw)
        if match:
            progress["latest_audit_problems"] = int(match.group(1))
        bridge_total = re.search(r"Gefundene Bridge-/Placeholder-Seiten:\s*(\d+)", latest_raw)
        bridge_wo = re.search(r"Ohne Ausnahme-Metadaten:\s*(\d+)", latest_raw)
        if bridge_total:
            progress["latest_bridge_total"] = int(bridge_total.group(1))
        if bridge_wo:
            progress["latest_bridge_without_exception"] = int(bridge_wo.group(1))

    if len(audit_files) > 1:
        previous_raw = audit_files[1].read_text(encoding="utf-8", errors="ignore")
        progress["previous_audit_file"] = str(audit_files[1].relative_to(PROJECT_ROOT))
        match = re.search(r"ERGEBNIS:\s*(\d+)\s+Probleme", previous_raw)
        if match:
            progress["previous_audit_problems"] = int(match.group(1))

    test_files = _discover_test_report_paths()
    by_suite: dict[str, Path] = {}
    for path in test_files:
        m = re.match(r"TEST_(.+)_\d{4}-\d{2}-\d{2}_\d{6}\.md$", path.name)
        if not m:
            continue
        suite = m.group(1)
        if suite not in by_suite:
            by_suite[suite] = path

    test_rows = []
    for suite, path in sorted(by_suite.items()):
        raw = path.read_text(encoding="utf-8", errors="ignore")
        result_match = re.search(r"- Ergebnis:\s*\*\*(PASS|FAIL)\*\*", raw)
        result = result_match.group(1) if result_match else "UNKLAR"
        count_match = re.search(r"- PASS:\s*(\d+)\s*\|\s*FAIL:\s*(\d+)\s*\|\s*SKIP:\s*(\d+)", raw)
        pass_count = int(count_match.group(1)) if count_match else 0
        fail_count = int(count_match.group(2)) if count_match else 0
        skip_count = int(count_match.group(3)) if count_match else 0
        test_rows.append(
            {
                "suite": suite,
                "result": result,
                "pass": pass_count,
                "fail": fail_count,
                "skip": skip_count,
                "report_file": str(path.relative_to(PROJECT_ROOT)) if path.is_relative_to(PROJECT_ROOT) else str(path),
            }
        )

    progress["latest_tests"] = test_rows
    progress["passing_suites"] = sum(1 for row in test_rows if row["result"] == "PASS")
    progress["failing_suites"] = sum(1 for row in test_rows if row["result"] == "FAIL")
    return progress


def collect_index_placeholder_inventory() -> dict:
    inventory = {
        "total_exact_placeholders": 0,
        "clusters": Counter(),
        "samples": {},
    }

    for md_file in WIKI_DIR.rglob("*.md"):
        try:
            raw = md_file.read_text(encoding="utf-8")
        except Exception:
            continue
        rel_path = md_file.relative_to(WIKI_DIR)
        section = rel_path.parts[0] if len(rel_path.parts) > 1 else "Root"
        for line_no, line in enumerate(raw.splitlines(), start=1):
            if not INDEX_PLACEHOLDER_RE.search(line):
                continue
            inventory["total_exact_placeholders"] += 1
            stripped = line.strip()
            if re.fullmatch(r"category:\s*\[\[index\]\]", stripped, re.IGNORECASE):
                cluster = "frontmatter_category"
            elif re.fullmatch(r"#{2,6}\s+\[\[index\]\]", stripped, re.IGNORECASE):
                cluster = "placeholder_heading"
            elif section in {"09_Bibliothek", "03_Wissen"}:
                cluster = "bibliothek_werk"
            elif section in {"05_Magie", "00_Fundament"}:
                cluster = "wissen_magie"
            elif section in {"03_Gesellschaft", "10_Archiv"}:
                cluster = "institution_archiv"
            else:
                cluster = "begrifflich_unklar"
            inventory["clusters"][cluster] += 1
            sample_list = inventory["samples"].setdefault(cluster, [])
            if len(sample_list) < 5:
                sample_list.append(
                    {
                        "file": str(rel_path),
                        "line": line_no,
                        "text": stripped,
                    }
                )

    inventory["clusters"] = dict(inventory["clusters"])
    return inventory


def collect_stats():
    stats = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "total_word_count": 0,
        "total_links": 0,
        "total_files": 0,
        "personalities_count": 0,
        "files_per_category": Counter(),
        "words_per_category": Counter(),
        "links_per_category": Counter(),
        "link_hubs": Counter(),
        "personality_hubs": Counter(),
        "event_hubs": Counter(),
        "files_with_frontmatter": 0,
        "files_with_quelle": 0,
        "files_with_resolved_quelle": 0,
        "unclear_markers": 0,
        "epistemic_distribution": Counter(),
        "activity": collect_git_activity(),
        "index_placeholder_inventory": collect_index_placeholder_inventory(),
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
            try:
                raw = md_file.read_text(encoding="utf-8")
            except Exception:
                raw = ""
            if not _is_placeholder_article(raw) and target_norm not in GENERIC_PERSONALITY_BLOCKLIST:
                personalities_lookup[target_norm] = stem
        if "04_Chronik" in str(rel_path) or "05_Geschichte" in str(rel_path):
            events_lookup[target_norm] = stem

    for md_file in WIKI_DIR.rglob("*.md"):
        if md_file.name == "Wiki_Statistiken.md":
            continue

        stats["total_files"] += 1
        content = md_file.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(content)

        rel_path = md_file.relative_to(WIKI_DIR)
        category = rel_path.parts[0] if len(rel_path.parts) > 1 else "Root"
        stats["files_per_category"][category] += 1

        if "07_Persoenlichkeiten" in str(md_file):
            stats["personalities_count"] += 1

        words = len(re.findall(r"\w+", content))
        stats["total_word_count"] += words
        stats["words_per_category"][category] += words

        links = re.findall(r"\[\[([^\]]+)\]\]", content)
        stats["total_links"] += len(links)
        stats["links_per_category"][category] += len(links)

        if content.startswith("---\n"):
            stats["files_with_frontmatter"] += 1

        quelle = frontmatter.get("quelle")
        if quelle is not None:
            stats["files_with_quelle"] += 1
            if is_resolved_quelle(quelle):
                stats["files_with_resolved_quelle"] += 1

        stats["unclear_markers"] += len(UNCLARIFIED_PATTERN.findall(content))
        epi_tag = extract_epistemic_tag(content, frontmatter)
        stats["epistemic_distribution"][epi_tag] += 1

        for link in links:
            target_raw = link.split("|")[0].split("#")[0].strip()
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
    stats["avg_words_per_article"] = round(stats["total_word_count"] / max(1, stats["total_files"]))
    stats["avg_links_per_article"] = round(stats["total_links"] / max(1, stats["total_files"]), 1)
    return stats


def _extract_first(raw: str, patterns: list[str]) -> str:
    for pattern in patterns:
        match = re.search(pattern, raw, re.MULTILINE)
        if match:
            return match.group(1).strip()
    return ""


def parse_ingestion_report(report_path: Path, raw: str) -> dict:
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
                raw = report_path.read_text(encoding="utf-8")
            except Exception:
                continue
            if not re.search(r"^#\s+📥\s+Ingestion Report", raw, re.MULTILINE):
                continue
            entries.append(parse_ingestion_report(report_path, raw))

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
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
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


def percent(value: int, total: int) -> float:
    return round((value / total * 100.0), 1) if total else 0.0


def progress_bar(pct: float) -> str:
    filled = max(0, min(10, round(pct / 10.0)))
    return f"`{'#' * filled}{'-' * (10 - filled)}` {pct:.1f}%"


def weather_label(ops: dict, stats: dict) -> str:
    problems = ops.get("latest_audit_problems", 0)
    unclear = stats.get("unclear_markers", 0)
    if problems >= 400 or unclear >= 400:
        return "Stuermisch: viele offene Baustellen, aber aktive Bewegung."
    if problems >= 200 or unclear >= 200:
        return "Windig: deutlich in Arbeit, noch sichtbar rau."
    return "Klar: stabile Wissenslage mit kontrollierter Werkstattlast."


def generate_markdown(stats: dict, tracking: dict, ops: dict) -> str:
    source_coverage = percent(stats["files_with_resolved_quelle"], stats["total_files"])
    tracking_coverage = percent(tracking["with_core_tracking"], tracking["total_reports"])
    lqs_coverage = percent(tracking["with_lqs"], tracking["total_reports"])
    frontmatter_coverage = percent(stats["files_with_frontmatter"], stats["total_files"])

    top_dense_categories = []
    for category, count in stats["files_per_category"].items():
        avg_words = round(stats["words_per_category"][category] / max(1, count))
        avg_links = round(stats["links_per_category"][category] / max(1, count), 1)
        top_dense_categories.append((category, avg_words, avg_links, count))
    top_dense_categories.sort(key=lambda x: x[1], reverse=True)

    md = f"""---
title: "📊 {WORLD_NAME} Kompass"
category: Index
---

# 📊 {WORLD_NAME} Kompass

**Stand:** {stats['timestamp']}

> Wissenswetter: **{weather_label(ops, stats)}**

---

## 🌍 Welt Heute

| Kennzahl | Wert |
| :--- | :--- |
| Artikel | **{stats['total_files']}** |
| Worte | **{stats['total_word_count']:,}** |
| Durchschnittliche Artikellaenge | **{stats['avg_words_per_article']} Worte** |
| Interne Verweise (`[[...]]`) | **{stats['total_links']:,}** |
| Vernetzungsdichte | **{stats['avg_links_per_article']} Links/Artikel** |
| Personenprofile | **{stats['personalities_count']}** |

---

## 🔄 Was sich bewegt

| Zeitraum | Bearbeitete Wiki-Artikel | Neue Wiki-Artikel | Aktive Tage |
| :--- | :--- | :--- | :--- |
| Letzte 7 Tage | {stats['activity']['changed_files_7d']} | - | {stats['activity']['active_days_7d']} |
| Letzte 30 Tage | {stats['activity']['changed_files_30d']} | {stats['activity']['new_files_30d']} | {stats['activity']['active_days_30d']} |
| Letzte 90 Tage | {stats['activity']['changed_files_90d']} | - | {stats['activity']['active_days_90d']} |

---

## 🧭 Sektionen

```mermaid
pie title Artikel pro Sektion
{"\n".join([f'    "{k}" : {v}' for k, v in stats['files_per_category'].items() if v > 10])}
```

## 📚 Lesetiefe nach Sektion (Top 5)

| Sektion | Artikel | Ø Worte/Artikel | Ø Links/Artikel |
| :--- | ---: | ---: | ---: |
"""

    for category, avg_words, avg_links, count in top_dense_categories[:5]:
        md += f"| `{category}` | {count} | {avg_words} | {avg_links} |\n"

    md += """

---

## 🏆 Entdecke die Welt

### Starke Knoten (gesamt)
| Entitaet | Verweise |
| :--- | ---: |
"""

    for name_norm, count in stats["link_hubs"].most_common(7):
        display = stats["article_lookup"].get(name_norm, denormalize_for_link(name_norm))
        md += f"| [[{display}]] | {count} |\n"

    md += """

### Praegende Persoenlichkeiten
| Persoenlichkeit | Verweise |
| :--- | ---: |
"""

    for name_norm, count in stats["personality_hubs"].most_common(7):
        display = stats["personality_lookup"].get(name_norm, denormalize_for_link(name_norm))
        md += f"| [[{display}]] | {count} |\n"

    md += """

### Praegende Ereignisse
| Ereignis | Verweise |
| :--- | ---: |
"""

    for name_norm, count in stats["event_hubs"].most_common(7):
        display = stats["events_lookup"].get(name_norm, denormalize_for_link(name_norm))
        md += f"| [[{display}]] | {count} |\n"

    md += f"""

---

## ✅ Qualitaet & Vertrauen

| Qualitaetsindikator | Wert | Fortschritt |
| :--- | :--- | :--- |
| Frontmatter-Abdeckung | {stats['files_with_frontmatter']}/{stats['total_files']} | {progress_bar(frontmatter_coverage)} |
| Aufgeloeste Quellenangabe (`quelle`) | {stats['files_with_resolved_quelle']}/{stats['total_files']} | {progress_bar(source_coverage)} |
| Ingestion Tracking vollstaendig | {tracking['with_core_tracking']}/{tracking['total_reports']} | {progress_bar(tracking_coverage)} |
| Ingestion Reports mit LQS | {tracking['with_lqs']}/{tracking['total_reports']} | {progress_bar(lqs_coverage)} |
| `[UNGEKLAERT]`-Marker (gesamt) | {stats['unclear_markers']} | Beobachtung |

## 🔏 Drift & Provenance
| Kennzahl | Wert |
| :--- | :--- |
| Technischer Edit-Baum | `docs/Siebenwind_Wiki/` |
| Epistemische Praezedenz | `{ " > ".join(TRUTH_HIERARCHY) }` |
| Homepage-Kanon | `{HOMEPAGE_URL}` |
| Inventar | `{INVENTORY_PATH.relative_to(PROJECT_ROOT)}` |

## Epistemische Verteilung
| Tag | Artikel |
| :--- | ---: |
"""

    for tag, count in stats["epistemic_distribution"].most_common():
        md += f"| `#{tag}` | {count} |\n"

    audit_delta = ops["latest_audit_problems"] - ops["previous_audit_problems"] if ops["previous_audit_file"] else 0
    delta_text = f"{audit_delta:+d}" if ops["previous_audit_file"] else "n/a"

    md += f"""

---

## 🛠️ Werkstattstatus (Transparenz)

| Metrik | Stand |
| :--- | :--- |
| Letzter Audit-Problemtotal | {ops['latest_audit_problems']} |
| Delta zum vorigen Audit | {delta_text} |
| Bridge-/Placeholder-Seiten | {ops['latest_bridge_total']} |
| Davon ohne Ausnahme-Metadaten | {ops['latest_bridge_without_exception']} |
| Test-Suiten PASS | {ops['passing_suites']} |
| Test-Suiten FAIL | {ops['failing_suites']} |

### Letzte Test-Suites
| Suite | Ergebnis | PASS | FAIL | SKIP |
| :--- | :--- | ---: | ---: | ---: |
"""

    for row in ops["latest_tests"]:
        md += f"| `{row['suite']}` | **{row['result']}** | {row['pass']} | {row['fail']} | {row['skip']} |\n"

    md += f"""

## 📍 Fortschritt Live Verfolgen
- Arbeitsprioritaeten: `MASTER_TASK_LIST.md`
- Change-Historie: `CHANGELOG.md`
- Tracking-Register: `Logs/INGESTION_TRACKING_REGISTER.md`
- Letzter Audit: `{ops['latest_audit_file'] or 'n/a'}`
- Letzte Testreports: `Logs/Archive/TEST_*.md` und `/tmp/7w_test_*/TEST_*.md`

---
> [!NOTE]
> Diese Seite ist leserzentriert. Technische Tiefendaten bleiben in den Log- und Board-Artefakten.
"""
    return md


def build_stats_snapshot(stats: dict, tracking: dict, ops: dict) -> dict:
    now_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return {
        "generated_at_utc": now_utc,
        "content_contract": {
            "technical_wiki_root": f"{WIKI_DIR_NAME}/",
            "epistemic_precedence": TRUTH_HIERARCHY,
            "homepage_url": HOMEPAGE_URL,
            "inventory_path": str(INVENTORY_PATH.relative_to(PROJECT_ROOT)),
        },
        "reader_metrics": {
            "articles": stats["total_files"],
            "words": stats["total_word_count"],
            "links": stats["total_links"],
            "avg_words_per_article": stats["avg_words_per_article"],
            "avg_links_per_article": stats["avg_links_per_article"],
            "personalities": stats["personalities_count"],
        },
        "quality": {
            "files_with_frontmatter": stats["files_with_frontmatter"],
            "files_with_resolved_quelle": stats["files_with_resolved_quelle"],
            "unclarified_markers_total": stats["unclear_markers"],
            "tracking_reports_total": tracking["total_reports"],
            "tracking_reports_complete": tracking["with_core_tracking"],
            "tracking_reports_with_lqs": tracking["with_lqs"],
        },
        "ops_progress": {
            "latest_audit_file": ops["latest_audit_file"],
            "latest_audit_problems": ops["latest_audit_problems"],
            "previous_audit_file": ops["previous_audit_file"],
            "previous_audit_problems": ops["previous_audit_problems"],
            "bridge_total": ops["latest_bridge_total"],
            "bridge_without_exception": ops["latest_bridge_without_exception"],
            "passing_suites": ops["passing_suites"],
            "failing_suites": ops["failing_suites"],
        },
        "activity": stats["activity"],
        "placeholder_inventory": {
            "index": stats["index_placeholder_inventory"],
        },
        "epistemic_distribution": dict(stats["epistemic_distribution"]),
        "files_per_category": dict(stats["files_per_category"]),
        "words_per_category": dict(stats["words_per_category"]),
        "links_per_category": dict(stats["links_per_category"]),
        "latest_tests": ops["latest_tests"],
    }


def write_stats_snapshot(snapshot: dict) -> Path:
    STATS_SNAPSHOT_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    stamped_path = STATS_SNAPSHOT_DIR / f"STATS_SNAPSHOT_{timestamp}.json"
    payload = json.dumps(snapshot, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    STATS_SNAPSHOT_LATEST.write_text(payload, encoding="utf-8")
    stamped_path.write_text(payload, encoding="utf-8")
    return stamped_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true", help="Output raw JSON stats block")
    args = parser.parse_args()

    data = collect_stats()
    tracking = collect_ingestion_tracking()
    ops = collect_ops_progress()
    write_inventory(activity="stats", agent="generate_wiki_stats")
    markdown_content = generate_markdown(data, tracking, ops)
    snapshot = build_stats_snapshot(data, tracking, ops)
    
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(markdown_content, encoding="utf-8")
    TRACKING_REGISTER_FILE.write_text(build_tracking_register_markdown(tracking), encoding="utf-8")
    snapshot_path = write_stats_snapshot(snapshot)
    
    if args.json:
        print(json.dumps(snapshot, indent=2))
    else:
        print(f"Stats generated at {OUTPUT_FILE}")
        print(f"Tracking register updated at {TRACKING_REGISTER_FILE}")
        print(f"Stats snapshot written to {STATS_SNAPSHOT_LATEST}")
        print(f"Stats snapshot archived at {snapshot_path}")
