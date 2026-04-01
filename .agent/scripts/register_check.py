#!/usr/bin/env python3
"""
register_check.py — Automatisierte Konsistenzprüfung für das Siebenwind Wiki.

Prüft:
1. Duplikate im Personenregister
2. Verwaiste Profile (Datei existiert, kein Register-Eintrag)
3. Registrierte Personen ohne Profildatei
4. Boten-Lücken (Quellen vorhanden, nicht integriert)
5. Index-Lücken (Dateien vorhanden, nicht in Die_Chronik.md)

Nutzung:
    python3 .agent/scripts/register_check.py

Ausgabe: Strukturierter Report auf stdout.
"""

import argparse
import json
import re
import sys
import time
import uuid
from pathlib import Path
from collections import Counter
from content_contract import scan_contract
from nexus_config import WIKI_DIR, WORLD_NAME
from pages_integrity import collect_pages_build_report, now_iso

# --- Configuration (relative to project root) ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
QUELLEN_DIR = PROJECT_ROOT / "Quellen" / "Zeitung 7w Bote"
REGISTER_FILE = WIKI_DIR / "00_Fundament" / "Personenregister.md"
PROFILE_DIR = WIKI_DIR / "07_Persoenlichkeiten"
CHRONIK_DIR = WIKI_DIR / "04_Chronik"
CHRONIK_INDEX = CHRONIK_DIR / "Die_Chronik.md"
INGESTION_REPORTS_DIR = PROJECT_ROOT / "Logs" / "Ingestion"

CHRONIK_INDEX = CHRONIK_DIR / "Die_Chronik.md"
SOURCE_HYGIENE_DIRS = [
    WIKI_DIR,
    PROJECT_ROOT / "Logs" / "Ingestion",
]
SOURCE_HYGIENE_FILES = [
    PROJECT_ROOT / "docs" / "COORDINATION_HUB.md",
]
BRIDGE_MARKER_PATTERNS = [
    r"Brueckenartikel zur Stabilisierung bestehender WikiLinks",
    r"Brückenartikel zur Stabilisierung bestehender WikiLinks",
    r"Brueckenartikel fuer numerische Legacy-Verweise",
    r"Brückenartikel für numerische Legacy-Verweise",
    r"Brueckenartikel fuer Legacy-Linkziel",
    r"Brückenartikel für Legacy-Linkziel",
]
BRIDGE_REQUIRED_FIELDS = [
    "bridge_mode:",
    "bridge_target:",
    "bridge_ticket:",
    "bridge_review_until:",
]

def get_all_wiki_files() -> tuple[dict[str, Path], dict[str, Path]]:
    """Create maps of filename (stem) and title to their absolute Path."""
    wiki_files = {}
    wiki_titles = {}
    # Search in Siebenwind_Wiki and Quellen
    search_paths = [WIKI_DIR, PROJECT_ROOT / "Quellen"]
    for base_path in search_paths:
        if not base_path.exists():
            continue
        for f in base_path.rglob("*.md"):
            wiki_files[f.stem] = f
            # Extract title from frontmatter
            try:
                content = f.read_text(encoding="utf-8")[:1000]
                match = re.search(r'^title:\s*(.*)', content, re.MULTILINE)
                if match:
                    title = match.group(1).strip()
                    # Strip quotes if present
                    if (title.startswith('"') and title.endswith('"')) or (title.startswith("'") and title.endswith("'")):
                        title = title[1:-1]
                    wiki_titles[title] = f
            except Exception:
                pass
    return wiki_files, wiki_titles

def check_wikilinks(wiki_files: dict[str, Path], wiki_titles: dict[str, Path]) -> list[tuple[Path, str, str]]:
    """Scan all .md files for [[Links]] and verify they exist in files or titles."""
    broken_links = []
    search_paths = [WIKI_DIR, PROJECT_ROOT / "Quellen"]
    
    # Create lowercase maps for case-insensitive fallback check
    wiki_files_low = {k.lower(): v for k, v in wiki_files.items()}
    wiki_titles_low = {k.lower(): v for k, v in wiki_titles.items()}

    for base_path in search_paths:
        if not base_path.exists():
            continue
        for fpath in base_path.rglob("*.md"):
            try:
                content = fpath.read_text(encoding="utf-8")
                # Strip code blocks and mermaid blocks to avoid false positives
                content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
                content = re.sub(r'`.*?`', '', content)
                
                # Find all [[Target]] or [[Target|Display]] or [[Target#Anchor|Display]]
                # Use strictly 2 or more brackets to avoid single-bracket markdown links
                links = re.findall(r'\[{2,}([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]{2,}', content)
                for link in links:
                    link_target = link.strip()
                    # Filter out malformed patterns or alerts
                    if not link_target or link_target.startswith("!") or link_target.replace(".", "") == "" or link_target == "…":
                        continue
                    
                    # 1. Exact match (File or Title)
                    if link_target in wiki_files or link_target in wiki_titles:
                        continue
                    
                    # 2. Case-insensitive match (File or Title) - still problematic for MkDocs but better than "Missing"
                    if link_target.lower() in wiki_files_low or link_target.lower() in wiki_titles_low:
                        broken_links.append((fpath, link_target, "Casing Match Only"))
                        continue

            except Exception as e:
                # Mute to stderr so it doesn't break JSON
                import sys
                print(f"Error reading {fpath}: {e}", file=sys.stderr)
    return broken_links


def _iter_source_hygiene_files() -> list[Path]:
    files: list[Path] = []
    for directory in SOURCE_HYGIENE_DIRS:
        if directory.exists():
            files.extend(sorted(directory.rglob("*.md")))
    for file_path in SOURCE_HYGIENE_FILES:
        if file_path.exists():
            files.append(file_path)
    return files


def _clean_markdown_target(raw_target: str) -> str:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1].strip()
    target = target.split(" ", 1)[0]
    target = target.split("#", 1)[0]
    return target


def check_source_link_hygiene() -> list[tuple[Path, str, str]]:
    """
    Scan markdown links for patterns that routinely break mkdocs --strict:
    - double URL encoding (%25xx),
    - unresolved [[index]] placeholders in paths,
    - absolute file:// links,
    - malformed nested markdown in Quellen paths,
    - source links that still point to .html.
    """
    findings: list[tuple[Path, str, str]] = []
    md_link_re = re.compile(r'(?<!\!)\[[^\]]+\]\(([^)]+)\)')

    for fpath in _iter_source_hygiene_files():
        try:
            content = fpath.read_text(encoding="utf-8")
        except Exception:
            continue

        # Explicit malformed pattern seen in historical ingestion artifacts.
        if "../../Quellen/[index](" in content:
            findings.append((fpath, "../../Quellen/[index](", "Malformed Quellen link syntax"))

        for raw_target in md_link_re.findall(content):
            target = _clean_markdown_target(raw_target)
            if not target:
                continue

            if "file://" in target:
                findings.append((fpath, target, "file:// URI is forbidden"))
                continue

            # Restrict hygiene checks to source-like paths to avoid noise in generic links.
            if "Quellen/" not in target and "Archiv/Ingestion_Reports/" not in target:
                continue

            if re.search(r"%25[0-9A-Fa-f]{2}", target):
                findings.append((fpath, target, "Double-encoded URL sequence"))
            if "[[index]]" in target or "%5B%5Bindex%5D%5D" in target:
                findings.append((fpath, target, "Unresolved [[index]] placeholder in path"))
            if target.endswith(".html"):
                findings.append((fpath, target, "Source link points to .html instead of .md"))

    # Stable output: unique triplets, sorted by file then target.
    unique = sorted(set(findings), key=lambda x: (str(x[0]), x[1], x[2]))
    return unique


def _extract_first(raw: str, patterns: list[str]) -> str:
    for pattern in patterns:
        match = re.search(pattern, raw, re.MULTILINE)
        if match:
            return match.group(1).strip()
    return ""


def analyze_ingestion_reports() -> dict:
    reports: list[dict] = []
    if not INGESTION_REPORTS_DIR.exists():
        return {
            "total": 0,
            "with_core_tracking": 0,
            "with_lqs": 0,
            "missing_examples": [],
            "lqs_distribution": {},
            "profile_distribution": {},
        }

    for report_path in sorted(INGESTION_REPORTS_DIR.glob("*.md")):
        try:
            raw = report_path.read_text(encoding="utf-8")
        except Exception:
            continue
        if not re.search(r"^#\s+📥\s+Ingestion Report", raw, re.MULTILINE):
            continue

        source = _extract_first(raw, [r"- \*\*Quelle\*\*:\s*`?(.+?)`?\s*$"])
        evaluator = _extract_first(raw, [r"- \*\*Ausgewertet von\*\*:\s*(.+?)\s*$", r"- \*\*Verantwortlicher Agent\*\*:\s*(.+?)\s*$"])
        evaluated_at = _extract_first(raw, [r"- \*\*Auswertungszeitpunkt \(UTC\)\*\*:\s*(.+?)\s*$", r"- \*\*Datum der Verarbeitung\*\*:\s*(.+?)\s*$"])
        lqs = _extract_first(
            raw,
            [
                r"\*\*Gesamt \(LQS(?: 0-10)?\)\*\*\s*\|\s*\*\*([0-9]+(?:\.[0-9]+)?)\/10\*\*",
                r"- \*\*Lore-Score \(LQS\)\*\*:\s*([0-9]+(?:\.[0-9]+)?)\/10",
            ],
        )
        profile = _extract_first(raw, [r"- \*\*Quality-Profil \(A/T/K/B/U\)\*\*:\s*([0-9/]+)\s*$"])
        if not profile:
            a = _extract_first(raw, [r"\| \*\*Abdeckung\*\* \|\s*([0-9]+)\s*\|", r"\| \*\*A: Abdeckung\*\* \|\s*([0-9]+)\s*\|"])
            t = _extract_first(raw, [r"\| \*\*Tiefe\*\* \|\s*([0-9]+)\s*\|", r"\| \*\*T: Tiefe\*\* \|\s*([0-9]+)\s*\|"])
            k = _extract_first(raw, [r"\| \*\*Konsistenz\*\* \|\s*([0-9]+)\s*\|", r"\| \*\*K: Kanon-Konsistenz\*\* \|\s*([0-9]+)\s*\|"])
            if a and t and k:
                profile = f"{a}/{t}/{k}"

        reports.append(
            {
                "path": report_path.relative_to(PROJECT_ROOT),
                "source": source,
                "evaluator": evaluator,
                "evaluated_at": evaluated_at,
                "lqs": lqs,
                "profile": profile,
                "has_core_tracking": bool(source and evaluator and evaluated_at),
            }
        )

    lqs_counter = Counter(r["lqs"] for r in reports if r["lqs"])
    profile_counter = Counter(r["profile"] for r in reports if r["profile"])
    missing = [r for r in reports if not r["has_core_tracking"]]

    return {
        "total": len(reports),
        "with_core_tracking": sum(1 for r in reports if r["has_core_tracking"]),
        "with_lqs": sum(1 for r in reports if r["lqs"]),
        "missing_examples": missing[:10],
        "lqs_distribution": dict(sorted(lqs_counter.items(), key=lambda x: float(x[0]))),
        "profile_distribution": dict(profile_counter.most_common()),
    }


def analyze_bridge_placeholder_pages() -> dict:
    """
    Detect bridge/placeholder pages and enforce explicit exception metadata.
    This does not ban all temporary bridges, but it makes untracked ones visible.
    """
    with_exception: list[Path] = []
    without_exception: list[tuple[Path, list[str]]] = []

    for fpath in sorted(WIKI_DIR.rglob("*.md")):
        try:
            raw = fpath.read_text(encoding="utf-8")
        except Exception:
            continue

        raw_low = raw.lower()
        has_marker = any(re.search(pattern, raw, re.IGNORECASE) for pattern in BRIDGE_MARKER_PATTERNS)
        declares_bridge = "bridge_mode:" in raw_low
        if not has_marker and not declares_bridge:
            continue

        missing_fields = [field for field in BRIDGE_REQUIRED_FIELDS if field not in raw_low]
        if missing_fields:
            without_exception.append((fpath, missing_fields))
        else:
            with_exception.append(fpath)

    return {
        "total": len(with_exception) + len(without_exception),
        "with_exception": len(with_exception),
        "without_exception": len(without_exception),
        "examples_without_exception": without_exception[:20],
    }


def extract_register_names(register_path: Path) -> list[str]:
    """Extract person names (first [[Name]] per table row) from the Personenregister."""
    names = []
    if not register_path.exists():
        return names
    for line in register_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        # Only process table data rows (start with | and contain [[)
        if not line.startswith('|') or '[[' not in line:
            continue
        # Skip header/separator rows
        if line.startswith('| :') or line.startswith('| Name'):
            continue
        # Extract FIRST [[Name]] in the row — this is the person's name
        match = re.search(r'\[\[([^\]]+)\]\]', line)
        if match:
            names.append(match.group(1))
    return names


def find_duplicates(names: list[str]) -> dict[str, int]:
    """Find names that appear more than once."""
    counts = Counter(names)
    return {name: count for name, count in counts.items() if count > 1}


def get_profile_files(profile_dir: Path) -> set[str]:
    """Get all profile filenames (without .md extension)."""
    if not profile_dir.exists():
        return set()
    return {f.stem for f in profile_dir.glob("*.md")}


def get_boten_numbers(directory: Path, pattern: str) -> set[int]:
    """Extract Boten edition numbers from filenames in a directory."""
    numbers = set()
    if not directory.exists():
        return numbers
    for f in directory.iterdir():
        match = re.search(pattern, f.name)
        if match:
            try:
                numbers.add(int(match.group(1)))
            except ValueError:
                pass
    return numbers


def get_chronik_index_numbers(index_path: Path) -> set[int]:
    """Extract Boten numbers listed in Die_Chronik.md."""
    numbers = set()
    if not index_path.exists():
        return numbers
    content = index_path.read_text(encoding="utf-8")
    for match in re.finditer(r'Siebenwind_Bote_(\d+)', content):
        try:
            numbers.add(int(match.group(1)))
        except ValueError:
            pass
    return numbers


def main():
    parser = argparse.ArgumentParser(description=f"{WORLD_NAME} Register Check (Audit)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON findings")
    parser.add_argument("--pages", action="store_true", help="Include Pages / Roamlinks integrity diagnostics")
    args = parser.parse_args()

    report_id = str(uuid.uuid4())
    issues_found = 0
    
    # Structure for JSON
    audit_data = {
        "report_id": report_id,
        "generated_at": now_iso(),
        "issues_found": 0,
        "timings_ms": {},
        "categories": {
            "content_backlog": {"issues": 0},
            "wiki_integrity": {"issues": 0},
            "source_hygiene": {"issues": 0},
            "site_integrity": {"issues": 0},
            "render_hygiene": {"issues": 0},
            "contract_violations": {"issues": 0},
            "stub_inventory": {"issues": 0, "total": 0},
            "bridge_inventory": {"issues": 0, "total": 0},
            "split_brain": {"issues": 0},
            "traceability_gaps": {"issues": 0},
        },
        "details": {
            "duplicates": [],
            "orphans": [],
            "missing_profiles": [],
            "missing_sources": [],
            "missing_index": [],
            "source_hygiene": [],
            "ingestion_issues": [],
            "broken_links": [],
            "bridge_pages": [],
            "render_hygiene": [],
            "contract_violations": [],
            "stub_inventory": {},
            "bridge_inventory": {},
            "split_brain": [],
            "traceability_gaps": {},
        },
    }

    # Capture output for file writing
    output_lines = []
    
    def log(msg=""):
        if not args.json:
            print(msg)
        output_lines.append(msg)

    log("=" * 60)
    log(f"  {WORLD_NAME.upper()} WIKI — REGISTER-CHECK")
    log(f"  Report-ID: {report_id}")
    log("=" * 60)
    log()
    audit_started = time.perf_counter()

    # --- 1. Duplikat-Scan ---
    log("## 1. Duplikate im Personenregister")
    register_names = extract_register_names(REGISTER_FILE)
    duplicates = find_duplicates(register_names)
    if duplicates:
        for name, count in sorted(duplicates.items()):
            log(f"  ⚠️  {name} — {count}x vorhanden")
            audit_data["details"]["duplicates"].append({"name": name, "count": count})
            issues_found += 1
    else:
        log("  ✅ Keine Duplikate gefunden.")
    log()

    # --- 2. Verwaiste Profile ---
    log("## 2. Verwaiste Profile (Datei ohne Register-Eintrag)")
    profile_files = get_profile_files(PROFILE_DIR)
    register_set = set(register_names)
    register_set.add("index") # Special case: directory indexes are not person profiles
    orphans = sorted(profile_files - register_set)
    if orphans:
        for name in orphans:
            fpath = PROFILE_DIR / f"{name}.md"
            has_quelle = False
            try:
                content = fpath.read_text(encoding="utf-8")[:500]
                has_quelle = "quelle:" in content.lower()
            except Exception:
                pass
            status = "📎 hat quelle:" if has_quelle else "❓ keine quelle:"
            log(f"  ⚠️  {name} — {status}")
            audit_data["details"]["orphans"].append({"name": name, "has_quelle": has_quelle})
            issues_found += 1
    else:
        log("  ✅ Alle Profile sind registriert.")
    log()

    # --- 3. Registriert ohne Profildatei ---
    log("## 3. Registrierte Personen ohne Profildatei")
    missing_profiles = sorted(register_set - profile_files)
    skip_prefixes = ("Siebenwind", "Region_", "Rasse_", "Ecclesia", "Kirche",
                     "Pakt_", "Graue_", "Löwen", "Ersonter", "Dwarshim",
                     "Bellum", "Vitama", "Ignis", "Enhor", "Morsan", "Xan",
                     "Persönlichkeiten", "index", "Geografie", "Geschichte")
    missing_profiles = [n for n in missing_profiles
                       if not any(n.startswith(p) for p in skip_prefixes)]
    if missing_profiles:
        for name in missing_profiles:
             audit_data["details"]["missing_profiles"].append(name)
             issues_found += 1

        for name in missing_profiles[:30]:
            log(f"  📝 {name} — Profildatei fehlt")
        if len(missing_profiles) > 30:
            log(f"  ... und {len(missing_profiles) - 30} weitere.")
    else:
        log("  ✅ Alle registrierten Personen haben Profildateien.")
    log()

    # --- 4. Boten-Lücken ---
    log("## 4. Boten-Lücken (Quellen vorhanden, nicht integriert)")
    quellen_numbers = get_boten_numbers(QUELLEN_DIR, r'Bote\s+(\d+)')
    wiki_numbers = get_boten_numbers(CHRONIK_DIR, r'Bote_(\d+)')
    missing_boten = sorted(quellen_numbers - wiki_numbers)
    if missing_boten:
        for num in missing_boten:
            log(f"  ⚠️  Bote {num} — Quelle vorhanden, nicht integriert")
            audit_data["details"]["missing_sources"].append({"id": num, "type": "Bote"})
            issues_found += 1
    else:
        log("  ✅ Alle verfügbaren Boten sind integriert.")
    log()

    # --- 5. Index-Lücken ---
    log("## 5. Index-Lücken (Dateien vorhanden, nicht in Die_Chronik.md)")
    index_numbers = get_chronik_index_numbers(CHRONIK_INDEX)
    unindexed = sorted(wiki_numbers - index_numbers)
    if unindexed:
        for num in unindexed:
            log(f"  ⚠️  Bote {num} — Datei existiert, fehlt im Index")
            audit_data["details"]["missing_index"].append({"id": num, "type": "Bote"})
            issues_found += 1
    else:
        log("  ✅ Alle Boten-Dateien sind im Index erfasst.")
    log()

    # --- 6. Source Link Hygiene ---
    log("## 6. Source Link Hygiene (MkDocs Strict Risks)")
    source_findings = check_source_link_hygiene()
    if source_findings:
        grouped_source: dict[Path, list[tuple[str, str]]] = {}
        for fpath, target, reason in source_findings:
            rel_path = fpath.relative_to(PROJECT_ROOT)
            grouped_source.setdefault(rel_path, []).append((target, reason))
            audit_data["details"]["source_hygiene"].append({
                "file": str(rel_path),
                "target": target,
                "reason": reason
            })

        for rel_path, items in sorted(grouped_source.items()):
            log(f"  ⚠️  {rel_path}:")
            for target, reason in sorted(set(items)):
                log(f"    - {reason}: {target}")
            issues_found += len(set(items))
    else:
        log("  ✅ Keine kritischen Source-Link-Muster gefunden.")
    log()

    # --- 7. Ingestion Tracking Coverage ---
    log("## 7. Ingestion Tracking & Score Distribution")
    ingestion = analyze_ingestion_reports()
    total_reports = ingestion["total"]
    if total_reports == 0:
        log("  ⚠️  Keine Ingestion-Reports gefunden.")
        issues_found += 1
    else:
        with_core = ingestion["with_core_tracking"]
        with_lqs = ingestion["with_lqs"]
        log(f"  Reports gesamt: {total_reports}")
        log(f"  Mit Kern-Tracking (Quelle + Wer + Wann): {with_core}")
        log(f"  Mit LQS: {with_lqs}")

        if with_core < total_reports:
            missing_count = total_reports - with_core
            log(f"  ⚠️  {missing_count} Report(s) ohne vollstaendige Tracking-Felder.")
            issues_found += missing_count
            for entry in ingestion["missing_examples"]:
                log(f"    - {entry['path']}")
                audit_data["details"]["ingestion_issues"].append({"file": str(entry["path"]), "error": "Missing core tracking"})

        if ingestion["lqs_distribution"]:
            lqs_text = ", ".join(f"{k}:{v}" for k, v in ingestion["lqs_distribution"].items())
            log(f"  LQS-Verteilung: {lqs_text}")
        if ingestion["profile_distribution"]:
            top_profile, top_count = next(iter(ingestion["profile_distribution"].items()))
            profile_text = ", ".join(f"{k}:{v}" for k, v in list(ingestion["profile_distribution"].items())[:5])
            log(f"  Profil-Cluster: {profile_text}")
            if top_count / max(1, with_lqs) >= 0.5:
                log(f"  ⚠️  Score-Cluster auffaellig eng (Top-Profil {top_profile} = {top_count}/{with_lqs}).")
                issues_found += 1
    log()

    # --- 8. Deep WikiLink Check ---
    log("## 8. Deep WikiLink Check (Internal Integrity)")
    wiki_files, wiki_titles = get_all_wiki_files()
    broken = check_wikilinks(wiki_files, wiki_titles)
    if broken:
        grouped = {}
        for fpath, target, reason in broken:
            rel_path = fpath.relative_to(PROJECT_ROOT)
            if rel_path not in grouped:
                grouped[rel_path] = []
            grouped[rel_path].append((target, reason))
            audit_data["details"]["broken_links"].append({
                "file": str(rel_path),
                "target": target,
                "reason": reason
            })
            
        for rel_path, items in sorted(grouped.items()):
            log(f"  ⚠️  {rel_path}:")
            for target, reason in sorted(set(items)):
                log(f"    - [[{target}]] ({reason})")
            issues_found += len(set(items))
    else:
        log("  ✅ Alle [[WikiLinks]] sind valide.")
    log()

    # --- 9. Bridge Placeholder Hygiene ---
    log("## 9. Bridge Placeholder Hygiene (Preventive)")
    bridge = analyze_bridge_placeholder_pages()
    if bridge["total"] == 0:
        log("  ✅ Keine Bridge-/Placeholder-Seiten gefunden.")
    else:
        log(f"  Gefundene Bridge-/Placeholder-Seiten: {bridge['total']}")
        log(f"  Mit Ausnahme-Metadaten: {bridge['with_exception']}")
        log(f"  Ohne Ausnahme-Metadaten: {bridge['without_exception']}")

        if bridge["without_exception"] > 0:
            issues_found += bridge["without_exception"]
            for fpath, missing_fields in bridge["examples_without_exception"]:
                rel_path = fpath.relative_to(PROJECT_ROOT)
                log(f"  ⚠️  {rel_path} — fehlend: {', '.join(missing_fields)}")
                audit_data["details"]["bridge_pages"].append({
                    "file": str(rel_path),
                    "missing": missing_fields
                })

            remaining = bridge["without_exception"] - len(bridge["examples_without_exception"])
            if remaining > 0:
                log(f"  ... und {remaining} weitere.")
    log()

    # --- 10. Content Contract / Drift ---
    log("## 10. Content Contract / Drift Prevention")
    contract_started = time.perf_counter()
    contract = scan_contract(WIKI_DIR)
    audit_data["timings_ms"]["content_contract"] = round((time.perf_counter() - contract_started) * 1000, 2)
    audit_data["details"]["stub_inventory"] = contract["stub_inventory"]
    audit_data["details"]["bridge_inventory"] = contract["bridge_inventory"]
    audit_data["details"]["split_brain"] = contract["split_brain"]["files"]
    audit_data["details"]["traceability_gaps"] = contract["traceability_gaps"]

    render_examples = []
    contract_examples = []
    for detail in contract["details"]:
        for change in detail.get("changes", []):
            if change["type"] == "inline_metadata_block":
                render_examples.append({"file": detail["path"], "change": change})
            elif change["type"] in {"legacy_field", "duplicate_frontmatter_key", "missing_frontmatter", "title_h1_mismatch"}:
                contract_examples.append({"file": detail["path"], "change": change})
    audit_data["details"]["render_hygiene"] = render_examples[:50]
    audit_data["details"]["contract_violations"] = contract_examples[:50]

    log(f"  Render-Hygiene-Issues: {contract['render_hygiene']['issues']}")
    log(f"  Contract-Verletzungen: {contract['contract_violations']['issues']}")
    log(f"  Stubs gesamt / invalid: {contract['stub_inventory']['total']} / {contract['stub_inventory']['invalid']}")
    log(f"  Bridges gesamt / invalid: {contract['bridge_inventory']['total']} / {contract['bridge_inventory']['invalid']}")
    log(f"  Split-Brain-Dateien: {contract['split_brain']['issues']}")
    log(f"  Inventar: {contract['traceability_gaps']['inventory_path']}")
    issues_found += (
        contract["render_hygiene"]["issues"]
        + contract["contract_violations"]["issues"]
        + contract["stub_inventory"]["invalid"]
        + contract["bridge_inventory"]["invalid"]
        + contract["split_brain"]["issues"]
        + contract["traceability_gaps"]["issues"]
    )
    log()

    if args.pages:
        pages_started = time.perf_counter()
        pages_report = collect_pages_build_report(config="mkdocs.yml", no_clean=False)
        audit_data["timings_ms"]["pages_integrity"] = round((time.perf_counter() - pages_started) * 1000, 2)
        pages_health = pages_report["pages_health"]
        audit_data["details"]["site_integrity"] = pages_health
        site_issues = pages_health.get("unallowlisted_total", 0) + len(pages_health.get("other_warnings", []))
        issues_found += site_issues

        log("## 11. Pages Site Integrity (MkDocs / Roamlinks)")
        log(f"  Status: {pages_health.get('status', 'UNKNOWN')}")
        log(
            "  Unresolved internal links: "
            f"total={pages_health.get('unresolved_total', 0)}, "
            f"allowlisted={pages_health.get('allowlisted_total', 0)}, "
            f"planned_fix={pages_health.get('planned_fix_total', 0)}, "
            f"unallowlisted={pages_health.get('unallowlisted_total', 0)}"
        )
        for target in pages_health.get("targets", [])[:20]:
            sources = ", ".join(target.get("source_pages", [])[:3]) or "unbekannt"
            log(
                f"  ⚠️  {target['target']} x{target['count']} "
                f"[{target.get('policy_status', 'untracked')}] in {sources}"
            )
        remaining_targets = len(pages_health.get("targets", [])) - min(20, len(pages_health.get("targets", [])))
        if remaining_targets > 0:
            log(f"  ... und {remaining_targets} weitere Targets.")
        for warning in pages_health.get("other_warnings", [])[:10]:
            log(f"  ⚠️  Warning: {warning}")
        log()

    audit_data["timings_ms"]["total"] = round((time.perf_counter() - audit_started) * 1000, 2)

    # --- Summary ---
    audit_data["categories"]["content_backlog"]["issues"] = len(audit_data["details"]["missing_sources"])
    audit_data["categories"]["source_hygiene"]["issues"] = len(audit_data["details"]["source_hygiene"])
    audit_data["categories"]["wiki_integrity"]["issues"] = (
        len(audit_data["details"]["duplicates"])
        + len(audit_data["details"]["orphans"])
        + len(audit_data["details"]["missing_profiles"])
        + len(audit_data["details"]["missing_index"])
        + len(audit_data["details"]["ingestion_issues"])
        + len(audit_data["details"]["broken_links"])
        + len(audit_data["details"]["bridge_pages"])
    )
    audit_data["categories"]["site_integrity"]["issues"] = len(audit_data["details"].get("site_integrity", {}).get("other_warnings", [])) + int(audit_data["details"].get("site_integrity", {}).get("unallowlisted_total", 0))
    audit_data["categories"]["render_hygiene"]["issues"] = contract["render_hygiene"]["issues"]
    audit_data["categories"]["contract_violations"]["issues"] = contract["contract_violations"]["issues"]
    audit_data["categories"]["stub_inventory"]["issues"] = contract["stub_inventory"]["invalid"]
    audit_data["categories"]["stub_inventory"]["total"] = contract["stub_inventory"]["total"]
    audit_data["categories"]["bridge_inventory"]["issues"] = contract["bridge_inventory"]["invalid"]
    audit_data["categories"]["bridge_inventory"]["total"] = contract["bridge_inventory"]["total"]
    audit_data["categories"]["split_brain"]["issues"] = contract["split_brain"]["issues"]
    audit_data["categories"]["traceability_gaps"]["issues"] = contract["traceability_gaps"]["issues"]
    audit_data["issues_found"] = issues_found
    log("=" * 60)
    log(f"  ERGEBNIS: {issues_found} Probleme gefunden.")
    if issues_found == 0:
        log("  🎉 Das Wiki ist konsistent!")
    else:
        log("  → Siehe /audit Workflow für Bearbeitungsschritte.")
    log("=" * 60)

    # Save report to file (Always, nicely formatted)
    log_dir = PROJECT_ROOT / "Logs" / "Archive"
    log_dir.mkdir(parents=True, exist_ok=True)
    report_file = log_dir / f"Audit_{report_id}.txt"
    try:
        report_file.write_text("\n".join(output_lines), encoding="utf-8")
        if not args.json:
            print(f"\n[INFO] Report gespeichert unter: {report_file}")
    except Exception as e:
        if not args.json:
            print(f"\n[ERROR] Konnte Report nicht speichern: {e}", file=sys.stderr)

    if args.json:
        print(json.dumps(audit_data, indent=2, ensure_ascii=False))
        return 1 if issues_found > 0 else 0


if __name__ == "__main__":
    sys.exit(main())
