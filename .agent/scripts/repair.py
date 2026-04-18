#!/usr/bin/env python3
"""
repair.py — Interaktives Reparatur-Werkzeug für das Siebenwind Wiki.

Funktionen:
1. Frontmatter Fixer: Ergänzt fehlende YAML-Header.
2. Smart Link Resolver: Findet tote Links und korrigiert sie durch Fuzzy-Matching & Canon-Mapping.
3. Source Reference Repair: Normalisiert problematische Quellen-Links (file://, %25xx, [[index]]).
4. Duplicate Detector: Findet doppelte Dateien (Kollisionen im Canon).

Nutzung:
    python3 .agent/scripts/repair.py [--auto|--full] [--check-collision NAME]
"""

import os
import sys
import re
import argparse
import json
from pathlib import Path
from collections import defaultdict
import difflib
from urllib.parse import unquote
from datetime import datetime, timezone

from content_contract import (
    REPO_ROOT,
    TECHNICAL_WIKI_ROOT,
    canonical_markdown_files,
    derive_category,
    normalize_document,
    scan_contract,
    serialize_frontmatter,
    split_frontmatter,
)
from pages_integrity import collect_pages_build_report, load_pages_health_snapshot

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

PROJECT_ROOT = REPO_ROOT
WIKI_DIR = TECHNICAL_WIKI_ROOT
QUELLEN_DIR = PROJECT_ROOT / "Quellen"
INGESTION_DIR = PROJECT_ROOT / "Logs" / "Ingestion"
DOCS_COORDINATION_HUB = PROJECT_ROOT / "docs" / "COORDINATION_HUB.md"
DOCS_WIKI_DIR = TECHNICAL_WIKI_ROOT
ROAMLINK_REPORT_DIR = PROJECT_ROOT / "Logs" / "Archive"
BACKLOG_BOARD_PATH = PROJECT_ROOT / ".agent" / "data" / "backlog_cluster_board.json"
BACKLOG_ESCALATIONS_PATH = PROJECT_ROOT / ".agent" / "data" / "backlog_escalations.json"
BACKLOG_ARTIFACT_VERSION = 1
SOURCE_DIR_TOKENS = ("bibliothek astrael", "bibliothek toran dur", "spielergeschichten", "zeitung 7w bote", "hintergrund", "forum", "news")
SOURCE_SHORT_TOKENS = ("astrael", "toran", "bote", "spielergeschichten")
CATEGORY_WIKILINK_RE = re.compile(r"^\s*\[\[(?P<target>[^\]|]+)(?:\|(?P<label>[^\]]+))?\]\]\s*$")
BACKLOG_ALIAS_EXCLUDES = {"persoenlichkeiten", "buergerwehr"}
BRIDGE_TARGET_LINE_RE = re.compile(r"^\s*Siehe auch:\s*(?P<targets>.+?)\s*$", re.IGNORECASE | re.MULTILINE)
WIKILINK_TARGET_RE = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")
WIKILINK_OCCURRENCE_RE = re.compile(
    r"\[\[(?P<target>[^\]|#\n]+)(?P<anchor>#[^\]\n|]+)?(?P<label>\|[^\]\n]+)?\]\]"
)
MARKDOWN_LINK_RE = re.compile(r"(?<!!)\[(?P<label>[^\n]*?)\]\((?P<target>[^)\n]+)\)")
ENCODED_OR_LITERAL_WIKILINK_WRAPPER_RE = re.compile(r"(\[\[|\]\]|%5B%5B|%5D%5D)", re.IGNORECASE)
DERIVED_BACKLOG_ROOTS = (
    DOCS_WIKI_DIR,
    PROJECT_ROOT / "docs" / "Archiv",
)
READONLY_BACKLOG_ROOTS = (
    PROJECT_ROOT / "docs" / "Quellen",
)

# Known Redirects / Hardcoded Fixes
LORE_REDIRECTS = {
    "chronik": "Die_Chronik",
    "malthust": "Region_Malthust",
    "suedfall": "Südfall",
    "oedland": "Ödland",
    "kesselklamm": "Bragarim",
    "dur": "Toran_Dur",
    "westhever": "Dunkeltief",
    "lehens_banner": "Lehensbanner",
    "isgrimm": "Isgrim",
    "lorien": "Riens_Lorien_Arden",
    "tar_sala": "Vorfall_im_Haus_TharSala",
    "morsanschrein": "Morsan",
    "seker": "Zeitrechnung_(Der_Sonnenzirkel)",
    "drachenschwingen": "Region_Auren",
    "barzak’dhan": "Region_Auren",
    "barzakdhan": "Region_Auren",
    "iria": "Personenregister",
    "jolanda_herdfeuer": "Personenregister",
    "ooc_timeline_(shard-historie)": "Die_Chronik",
    "groenlanden": "Grünland",
    "grönlanden": "Grünland",
    "gönelande": "Grünland",
}

def derive_category(path: Path) -> str:
    """Bestimmt die Kategorie anhand des Ordnernamens."""
    parent_name = path.parent.name
    mapping = {
        "04_Chronik": "Chronik",
        "07_Persoenlichkeiten": "Personen",
        "02_Geografie": "Geografie",
        "03_Gesellschaft": "Gesellschaft",
        "10_Archiv": "Archiv",
        "01_Pantheon": "Religion",
        "05_Magie": "Magie",
        "05_Geschichte": "Geschichte"
    }
    return mapping.get(parent_name, "Allgemein")

def normalize_key(name: str) -> str:
    """Normalisiert einen Dateinamen für den Vergleich (lowercase, no space/underscore)."""
    translation = str.maketrans({
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "ß": "ss",
        "Ä": "ae",
        "Ö": "oe",
        "Ü": "ue",
    })
    normalized = name.translate(translation).lower()
    return re.sub(r"[^a-z0-9]", "", normalized)


def _clean_link_target(target: str) -> str:
    cleaned = target.strip()
    if cleaned.startswith("<") and cleaned.endswith(">"):
        cleaned = cleaned[1:-1].strip()
    cleaned = cleaned.split(" ", 1)[0]
    cleaned = cleaned.split("#", 1)[0]
    return cleaned


def _source_repair_file_set(base_files: list[Path]) -> list[Path]:
    files = set(base_files)
    if INGESTION_DIR.exists():
        files.update(INGESTION_DIR.rglob("*.md"))
    if DOCS_COORDINATION_HUB.exists():
        files.add(DOCS_COORDINATION_HUB)
    return sorted(files)


def _build_quellen_lookup() -> dict[str, list[Path]]:
    lookup: dict[str, list[Path]] = defaultdict(list)
    if not QUELLEN_DIR.exists():
        return lookup
    for fpath in QUELLEN_DIR.rglob("*.md"):
        lookup[normalize_key(fpath.stem)].append(fpath)
    return lookup


def _best_quellen_match(raw_target: str, lookup: dict[str, list[Path]]) -> Path | None:
    decoded = unquote(_clean_link_target(raw_target))
    basename = Path(decoded).name
    if not basename:
        return None
    if basename.lower().endswith(".html"):
        basename = basename[:-5] + ".md"

    key = normalize_key(Path(basename).stem)
    candidates = lookup.get(key, [])
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]

    decoded_low = decoded.lower()
    scored = []
    for cand in candidates:
        cand_low = str(cand.relative_to(PROJECT_ROOT)).lower()
        score = 0
        for token in ("bibliothek astrael", "bibliothek toran dur", "spielergeschichten", "zeitung 7w bote", "hintergrund", "forum", "news"):
            if token in decoded_low and token in cand_low:
                score += 3
        for token in ("astrael", "toran", "bote", "spielergeschichten"):
            if token in decoded_low and token in cand_low:
                score += 1
        scored.append((score, len(str(cand)), cand))
    scored.sort(key=lambda x: (-x[0], x[1]))
    return scored[0][2]


def _quellen_candidates(raw_target: str, lookup: dict[str, list[Path]]) -> list[Path]:
    decoded = unquote(_clean_link_target(raw_target))
    basename = Path(decoded).name
    if not basename:
        return []
    if basename.lower().endswith(".html"):
        basename = basename[:-5] + ".md"

    key = normalize_key(Path(basename).stem)
    return list(lookup.get(key, []))


def _strict_quellen_match(raw_target: str, lookup: dict[str, list[Path]]) -> Path | None:
    candidates = _quellen_candidates(raw_target, lookup)
    if not candidates:
        return None
    if len(candidates) == 1:
        return candidates[0]

    decoded_low = unquote(_clean_link_target(raw_target)).lower()
    token_filtered = [
        cand for cand in candidates
        if any(token in decoded_low and token in str(cand.relative_to(PROJECT_ROOT)).lower() for token in SOURCE_DIR_TOKENS)
    ]
    if len(token_filtered) == 1:
        return token_filtered[0]

    short_filtered = [
        cand for cand in candidates
        if any(token in decoded_low and token in str(cand.relative_to(PROJECT_ROOT)).lower() for token in SOURCE_SHORT_TOKENS)
    ]
    if len(short_filtered) == 1:
        return short_filtered[0]
    return None

def get_canon_map(target_dir: Path) -> dict:
    """
    Erstellt eine Map aller existierenden Dateien.
    Key: Normalisierter Name
    Value: Liste von Pfaden (für Duplikat-Erkennung)
    """
    canon_map = defaultdict(list)
    for f in target_dir.rglob("*.md"):
        key = normalize_key(f.stem)
        canon_map[key].append(f)
        
        # Check Frontmatter Aliases (Basic Regex)
        try:
            content = f.read_text(encoding="utf-8")[:2000]
            aliases_match = re.search(r'^aliases:\s*\[(.*?)\]', content, re.MULTILINE)
            if aliases_match:
                aliases = aliases_match.group(1).split(",")
                for alias in aliases:
                    alias_key = normalize_key(alias.strip().strip('"\''))
                    canon_map[alias_key].append(f)
        except: pass
        
    return canon_map

def resolve_link(target: str, canon_map: dict) -> str | None:
    """
    Versucht, einen Link intelligent aufzulösen.
    1. Check Redirects
    2. Check Canon Map (Exact normalized match)
    """
    # 1. Hardcoded Redirects
    target_clean = target.lower().replace(" ", "_")
    if target_clean in LORE_REDIRECTS:
        return LORE_REDIRECTS[target_clean]

    # 2. Canon Map Match
    key = normalize_key(target)
    if key in canon_map:
        matches = canon_map[key]
        if matches:
            # Priorisierung: Nimm die Datei mit dem kürzesten Pfad oder tiefsten Nesting?
            # Hier nehmen wir einfach die erste, idealerweise sollte man Logik haben.
            # Aber wir returnen den *Stem* (Dateinamen ohne Extension), da WikiLinks relativ sind.
            return matches[0].stem
            
    return None

def check_duplicates(canon_map: dict):
    """Listet Dateien auf, die den gleichen normalisierten Namen haben."""
    print(f"\n{BLUE}--- Duplicate Detector ---{RESET}")
    found = False
    for key, paths in canon_map.items():
        if len(paths) > 1:
            # Filter out intentional duplicates if they are in different major folders?
            # For now, just list them.
            print(f"{YELLOW}Doppelte Einträge für '{key}':{RESET}")
            for p in paths:
                print(f"  - {p.resolve().relative_to(PROJECT_ROOT.resolve())}")
            found = True
            
    if not found:
        print(f"{GREEN}Keine Duplikate gefunden.{RESET}")
    else:
        print(f"\n{YELLOW}Hinweis:{RESET} Diese Dateien könnten kollidieren. Bitte manuell prüfen.")

def repair_links(files: list[Path], canon_map: dict, auto: bool = False):
    """Repariert tote links mittels Smart Resolver."""
    print(f"\n{BLUE}--- Smart Link Repair ---{RESET}")
    count = 0
    link_regex = re.compile(r'\[\[([^\]|#]+)(#[^\]|]+)?(\|[^\]]+)?\]\]')

    def replace_callback(match):
        original_target = match.group(1)
        anchor = match.group(2) or ""
        text = match.group(3) or ""
        
        # Check if valid first
        norm_key = normalize_key(original_target)
        if norm_key in canon_map:
            # Existiert (zumindest als Match).
            # Prüfen ob Case stimmt.
            best_match = canon_map[norm_key][0].stem
            if best_match != original_target:
                # Casing repair or Redirect
                return f"[[{best_match}{anchor}{text}]]"
            return match.group(0) # Unverändert
        
        # Dead Link -> Versuch Resolve
        resolved = resolve_link(original_target, canon_map)
        if resolved:
            return f"[[{resolved}{anchor}{text}]]"
        
        return match.group(0) # Kann nicht repariert werden

    for fpath in files:
        try:
            content = fpath.read_text(encoding="utf-8")
            new_content = link_regex.sub(replace_callback, content)
            
            if new_content != content:
                if not auto:
                    print(f"Änderung an {fpath.name}:")
                    # Diff anzeigen wäre gut, aber hier kurz halten
                
                if auto or input("  Änderungen speichern? [y/n]: ").lower() == 'y':
                    fpath.write_text(new_content, encoding="utf-8")
                    print(f"  {GREEN}Repariert.{RESET}")
                    count += 1
        except Exception:
            pass

    print(f"\n{count} Dateien repariert.")


def repair_source_references(files: list[Path], auto: bool = False):
    """
    Repariert fehleranfällige Quellen-Links:
    - file:// URIs
    - doppelt encodierte Targets (%25xx)
    - [[index]] Platzhalter in Quellenpfaden
    - markdown links auf Quellen -> robustes Pfadformat mit Backticks
    """
    print(f"\n{BLUE}--- Source Reference Repair ---{RESET}")
    count = 0
    link_re = re.compile(r'(?<!\!)\[(?P<label>[^\]]+)\]\((?P<target>[^)]+)\)')
    malformed_re = re.compile(r"\.\./\.\./Quellen/\[index\]\(\.\./10_Archiv/index\.md")
    quellen_lookup = _build_quellen_lookup()

    def repl(match, source_file: Path):
        label = match.group("label").strip()
        target_raw = match.group("target").strip()
        target = _clean_link_target(target_raw)
        if not target:
            return match.group(0)

        is_source_like = (
            "Quellen/" in target
            or "Archiv/Ingestion_Reports/" in target
            or target.startswith("file://")
            or re.search(r"%25[0-9A-Fa-f]{2}", target) is not None
            or "[[index]]" in target
            or "%5B%5Bindex%5D%5D" in target
            or "[[" in target
            or "]]" in target
        )
        if not is_source_like:
            return match.group(0)

        needs_repair = (
            target.startswith("file://")
            or re.search(r"%25[0-9A-Fa-f]{2}", target) is not None
            or "[[index]]" in target
            or "%5B%5Bindex%5D%5D" in target
            or "[[" in target
            or "]]" in target
            or target.endswith(".html")
        )
        if not needs_repair:
            return match.group(0)

        resolved = None
        if "Quellen/" in target or target.startswith("file://"):
            match_path = _strict_quellen_match(target, quellen_lookup)
            if match_path is not None:
                resolved = os.path.relpath(match_path, start=source_file.parent).replace(os.sep, "/")

        if resolved is None:
            fallback = unquote(target)
            fallback = fallback.replace("%5B%5Bindex%5D%5D%20", "")
            fallback = fallback.replace("[[index]]%20", "")
            fallback = fallback.replace("[[index]] ", "")
            fallback = fallback.replace("%2520", "%20")
            fallback = fallback.replace("%25C2%25B7", "%C2%B7")
            if fallback.startswith("file://"):
                fallback = fallback[len("file://"):]
                try:
                    fallback_path = Path(fallback)
                    if fallback_path.exists():
                        fallback = os.path.relpath(fallback_path, start=source_file.parent).replace(os.sep, "/")
                except Exception:
                    pass
            resolved = fallback

        return f"{label} (`{resolved}`)"

    for fpath in files:
        try:
            content = fpath.read_text(encoding="utf-8")
        except Exception:
            continue

        new_content = content
        # Handle a known malformed nested markdown pattern from legacy ingestions.
        new_content = malformed_re.sub("../../Quellen/10_Archiv/index.md", new_content)
        new_content = link_re.sub(lambda m: repl(m, fpath), new_content)

        if new_content != content:
            if not auto:
                print(f"Änderung an {fpath.relative_to(PROJECT_ROOT)}")
            if auto or input("  Änderungen speichern? [y/n]: ").lower() == 'y':
                fpath.write_text(new_content, encoding="utf-8")
                print(f"  {GREEN}Repariert.{RESET}")
                count += 1

    print(f"\n{count} Dateien mit Source-Referenzen repariert.")


def repair_frontmatter_categories(files: list[Path], auto: bool = False, dry_run: bool = False) -> dict:
    """
    Normalisiert bare WikiLinks im category-Frontmatter auf den kanonischen Klartextwert.
    Special case: [[index]] wird auf derive_category(path) gehoben.
    """
    changed_files = 0
    touched: list[str] = []

    for file_path in files:
        try:
            raw = file_path.read_text(encoding="utf-8")
        except Exception:
            continue
        meta, body, order, _, had_frontmatter = split_frontmatter(raw)
        if not had_frontmatter or "category" not in meta:
            continue
        category_value = meta.get("category", "")
        match = CATEGORY_WIKILINK_RE.match(category_value)
        if not match:
            continue

        target = (match.group("label") or match.group("target") or "").strip()
        if normalize_key(target) == "index":
            normalized = derive_category(file_path)
        else:
            normalized = derive_category(file_path)
        if normalized == category_value:
            continue

        meta["category"] = normalized
        new_raw = serialize_frontmatter(meta, body, order)
        touched.append(str(file_path.relative_to(PROJECT_ROOT)))
        if not dry_run and auto:
            file_path.write_text(new_raw, encoding="utf-8")
            changed_files += 1

    return {
        "cluster": "frontmatter_category_wikilinks",
        "changed_files": changed_files,
        "matched_files": len(touched),
        "files": touched,
    }


def repair_quelle_frontmatter(files: list[Path], auto: bool = False, dry_run: bool = False) -> dict:
    """
    Normalisiert problematische quelle:-Felder konservativ:
    - bare/broken wikilinks werden in Plaintext überführt
    - Quellen/Bote-Dateireferenzen werden nur bei genau einem realen Treffer lookup-basiert auf relative Pfade gesetzt
    """
    changed_files = 0
    touched: list[str] = []
    quellen_lookup = _build_quellen_lookup()

    for file_path in files:
        try:
            raw = file_path.read_text(encoding="utf-8")
        except Exception:
            continue
        meta, body, order, _, had_frontmatter = split_frontmatter(raw)
        if not had_frontmatter or "quelle" not in meta:
            continue

        original_value = meta.get("quelle", "").strip()
        new_value = original_value
        if "[[" in new_value or "]]" in new_value:
            new_value = re.sub(r"\[\[(.*?)(?:\|.*?)?\]\]", r"\1", new_value)
            new_value = new_value.replace("[", "").replace("]", "").strip()

        if (
            "Quellen/" in new_value
            or new_value.startswith("file://")
            or "Siebenwind_Bote" in new_value
            or "Siebenwind Bote" in new_value
            or new_value.endswith(".html")
        ):
            match_path = _strict_quellen_match(new_value, quellen_lookup)
            if match_path is not None:
                new_value = os.path.relpath(match_path, start=file_path.parent).replace(os.sep, "/")

        if new_value == original_value:
            continue

        meta["quelle"] = new_value
        new_raw = serialize_frontmatter(meta, body, order)
        touched.append(str(file_path.relative_to(PROJECT_ROOT)))
        if not dry_run and auto:
            file_path.write_text(new_raw, encoding="utf-8")
            changed_files += 1

    return {
        "cluster": "quelle_frontmatter_lookup",
        "changed_files": changed_files,
        "matched_files": len(touched),
        "files": touched,
    }

def fix_frontmatter(files: list[Path], auto: bool = False):
    """Sucht und repariert fehlendes Frontmatter."""
    print(f"\n{BLUE}--- Frontmatter Fixer ---{RESET}")
    count = 0
    for file_path in files:
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            continue

        new_content, changes, _, _ = normalize_document(content, file_path)
        if not changes:
            continue
        if auto or input(f"Frontmatter/Metadaten für {file_path.name} normalisieren? [y/n]: ").lower() == 'y':
            file_path.write_text(new_content, encoding="utf-8")
            print(f"  {GREEN}Repariert.{RESET}")
            count += 1
    print(f"{count} Frontmatter hinzugefügt.")


def run_full_repair(files: list[Path], source_files: list[Path], canon_map: dict, auto: bool = False):
    """Führt die Reparaturmodule 1→3 in Reihenfolge aus."""
    fix_frontmatter(files, auto=auto)
    repair_links(files, canon_map, auto=auto)
    repair_source_references(source_files, auto=auto)


def now_stamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")


def _roamlink_target_candidates(target: str, canon_map: dict) -> tuple[str | None, list[str]]:
    exact = resolve_link(target, canon_map)
    if exact:
        return exact, []

    norm_target = normalize_key(target)
    scored: list[tuple[float, str]] = []
    for key, paths in canon_map.items():
        if not paths:
            continue
        score = difflib.SequenceMatcher(None, norm_target, key).ratio()
        scored.append((score, paths[0].stem))
    scored.sort(key=lambda item: (-item[0], item[1]))
    if not scored:
        return None, []
    top_score, top_name = scored[0]
    second_score = scored[1][0] if len(scored) > 1 else 0.0
    if top_score >= 0.92 and (top_score - second_score) >= 0.05:
        return top_name, []
    suggestions = [name for _, name in scored[:5]]
    return None, suggestions


def _replace_target_in_content(content: str, original_target: str, replacement: str) -> str:
    pattern = re.compile(rf"(\[{{2,}})({re.escape(original_target)})(#[^\]|]+)?(\|[^\]]+)?(\]{{2,}})")
    return pattern.sub(lambda m: f"{m.group(1)}{replacement}{m.group(3) or ''}{m.group(4) or ''}{m.group(5)}", content)


def _resolve_source_repair_paths(source_pages: list[str]) -> list[Path]:
    resolved: list[Path] = []
    for rel in source_pages:
        docs_path = PROJECT_ROOT / rel
        if docs_path.exists():
            resolved.append(docs_path)
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in resolved:
        if path in seen:
            continue
        seen.add(path)
        unique.append(path)
    return unique


def _load_pages_health_for_backlog() -> dict:
    snapshot = load_pages_health_snapshot()
    if snapshot and snapshot.get("pages_health"):
        return snapshot.get("pages_health", {})
    report = collect_pages_build_report(config="mkdocs.yml", no_clean=False, fast=True)
    return report.get("pages_health", {})


def _mechanical_alias_candidate(item: dict) -> str | None:
    target = str(item.get("target", "")).strip()
    candidates = [candidate for candidate in item.get("canonical_candidates", []) if candidate]
    if len(candidates) != 1 or not target:
        return None
    if normalize_key(target) in BACKLOG_ALIAS_EXCLUDES:
        return None
    candidate = candidates[0]
    if normalize_key(target) != normalize_key(candidate):
        return None
    if target == candidate:
        return None
    return candidate


def _is_within(path: Path, roots: tuple[Path, ...]) -> bool:
    resolved = path.resolve()
    for root in roots:
        try:
            resolved.relative_to(root.resolve())
            return True
        except ValueError:
            continue
    return False


def _relpath(path: Path) -> str:
    return str(path.relative_to(PROJECT_ROOT))


def _backlog_scan_files(include_sources: bool = True) -> list[Path]:
    roots = list(DERIVED_BACKLOG_ROOTS)
    if include_sources:
        roots.extend(READONLY_BACKLOG_ROOTS)
    files: set[Path] = set()
    for root in roots:
        if root.exists():
            files.update(root.rglob("*.md"))
    return sorted(files)


def _canonical_target_exists(target: str, canon_map: dict) -> bool:
    return normalize_key(target) in canon_map


def _backlog_item_replacement(item: dict, canon_map: dict) -> tuple[str | None, str]:
    candidate = _mechanical_alias_candidate(item)
    if candidate:
        return candidate, "safe_exact_match"

    candidates = [candidate for candidate in item.get("canonical_candidates", []) if candidate]
    if str(item.get("classification", "")) == "safe_alias_match" and len(candidates) == 1:
        return candidates[0], "safe_alias_match"

    replacement_hint = str(item.get("replacement_hint") or "").strip()
    if (
        str(item.get("policy_status", "")) == "planned_fix"
        and replacement_hint
        and _canonical_target_exists(replacement_hint, canon_map)
    ):
        return replacement_hint, "planned_fix"

    return None, ""


def _backlog_target_indexes(pages_health: dict, canon_map: dict) -> tuple[dict[str, dict], dict[str, tuple[str, str]]]:
    items_by_target: dict[str, dict] = {}
    replacements_by_target: dict[str, tuple[str, str]] = {}
    for item in pages_health.get("targets", []):
        target = str(item.get("target", "")).strip()
        if not target:
            continue
        items_by_target[target] = item
        replacement, replacement_reason = _backlog_item_replacement(item, canon_map)
        if replacement:
            replacements_by_target[target] = (replacement, replacement_reason)
    return items_by_target, replacements_by_target


def _markdown_target_without_wrappers(target: str) -> str:
    fixed = target.replace("[[", "").replace("]]", "")
    fixed = re.sub(r"%5B%5B", "", fixed, flags=re.IGNORECASE)
    fixed = re.sub(r"%5D%5D", "", fixed, flags=re.IGNORECASE)
    return fixed


def _markdown_target_path_exists(source_file: Path, target: str) -> bool:
    clean_target = target.strip()
    if not clean_target or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", clean_target):
        return False
    clean_target = clean_target.split("#", 1)[0]
    try:
        decoded = unquote(clean_target)
        return (source_file.parent / decoded).resolve().exists()
    except Exception:
        return False


def _backlog_repair_status(
    file_path: Path,
    item: dict,
    replacement: str | None,
    replacement_reason: str,
) -> str:
    if _is_within(file_path, READONLY_BACKLOG_ROOTS):
        return "read_only_source_residue"
    if not _is_within(file_path, DERIVED_BACKLOG_ROOTS):
        return "out_of_scope"
    if replacement and replacement_reason == "planned_fix":
        return "auto_safe_policy"
    if replacement:
        return "auto_safe"
    classification = str(item.get("classification", "needs_historian"))
    if classification in {"generic_term_conflict", "needs_historian", "needs_human"}:
        return "manual_review"
    return "no_safe_replacement"


def _build_backlog_inventory(pages_health: dict | None = None) -> dict:
    pages_health = pages_health or _load_pages_health_for_backlog()
    canon_map = get_canon_map(WIKI_DIR)
    if DOCS_WIKI_DIR.exists():
        docs_canon = get_canon_map(DOCS_WIKI_DIR)
        for key, paths in docs_canon.items():
            canon_map[key].extend(path for path in paths if path not in canon_map[key])

    items_by_target, replacements_by_target = _backlog_target_indexes(pages_health, canon_map)
    occurrences: list[dict] = []
    seen_targets: set[str] = set()

    for file_path in _backlog_scan_files(include_sources=True):
        try:
            lines = file_path.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue
        rel_path = _relpath(file_path)
        for line_number, line in enumerate(lines, start=1):
            for match in WIKILINK_OCCURRENCE_RE.finditer(line):
                target = match.group("target").strip()
                item = items_by_target.get(target)
                if not item:
                    continue
                seen_targets.add(target)
                replacement, replacement_reason = replacements_by_target.get(target, (None, ""))
                label = match.group("label") or ""
                anchor = match.group("anchor") or ""
                occurrences.append(
                    {
                        "file": rel_path,
                        "line": line_number,
                        "column": match.start() + 1,
                        "link_kind": "wikilink",
                        "target": target,
                        "classification": item.get("classification", "needs_historian"),
                        "policy_status": item.get("policy_status", "untracked"),
                        "canonical_candidates": item.get("canonical_candidates", []),
                        "replacement_target": replacement,
                        "replacement": f"[[{replacement}{anchor}{label}]]" if replacement else None,
                        "repair_status": _backlog_repair_status(file_path, item, replacement, replacement_reason),
                    }
                )

            for match in MARKDOWN_LINK_RE.finditer(line):
                target = match.group("target").strip()
                if not ENCODED_OR_LITERAL_WIKILINK_WRAPPER_RE.search(target):
                    continue
                fixed_target = _markdown_target_without_wrappers(target)
                nested_targets = [
                    nested.group("target").strip()
                    for nested in WIKILINK_OCCURRENCE_RE.finditer(target)
                    if nested.group("target").strip()
                ]
                for nested_target in nested_targets:
                    for unresolved_target in items_by_target:
                        if unresolved_target.startswith("[") and normalize_key(unresolved_target) == normalize_key(nested_target):
                            seen_targets.add(unresolved_target)
                target_exists = fixed_target != target and _markdown_target_path_exists(file_path, fixed_target)
                if _is_within(file_path, READONLY_BACKLOG_ROOTS):
                    repair_status = "read_only_source_residue"
                elif _is_within(file_path, DERIVED_BACKLOG_ROOTS) and target_exists:
                    repair_status = "auto_safe_wrapper"
                elif _is_within(file_path, DERIVED_BACKLOG_ROOTS):
                    repair_status = "missing_resolved_path"
                else:
                    repair_status = "out_of_scope"
                occurrences.append(
                    {
                        "file": rel_path,
                        "line": line_number,
                        "column": match.start() + 1,
                        "link_kind": "markdown_url_wrapper",
                        "target": ", ".join(nested_targets) if nested_targets else target,
                        "url_target": target,
                        "classification": "technical_wrapper",
                        "policy_status": "untracked",
                        "canonical_candidates": [],
                        "replacement_target": fixed_target if target_exists else None,
                        "replacement": fixed_target if target_exists else None,
                        "repair_status": repair_status,
                    }
                )

    status_counts: dict[str, int] = defaultdict(int)
    kind_counts: dict[str, int] = defaultdict(int)
    for occurrence in occurrences:
        status_counts[occurrence["repair_status"]] += 1
        kind_counts[occurrence["link_kind"]] += 1

    unresolved_targets = pages_health.get("targets", [])
    unfound_targets = []
    for item in unresolved_targets:
        target = str(item.get("target", "")).strip()
        if target and target not in seen_targets:
            unfound_targets.append(
                {
                    "target": item.get("target", ""),
                    "count": item.get("count", 0),
                    "classification": item.get("classification", "needs_historian"),
                    "policy_status": item.get("policy_status", "untracked"),
                    "canonical_candidates": item.get("canonical_candidates", []),
                    "replacement_hint": item.get("replacement_hint"),
                }
            )

    return {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "mode": "inventory",
        "pages_health": {
            "status": pages_health.get("status", "UNKNOWN"),
            "unresolved_total": pages_health.get("unresolved_total", 0),
            "unallowlisted_total": pages_health.get("unallowlisted_total", 0),
            "classification_counts": pages_health.get("classification_counts", {}),
            "last_validated_at": pages_health.get("last_validated_at"),
        },
        "summary": {
            "occurrences_total": len(occurrences),
            "status_counts": dict(sorted(status_counts.items())),
            "kind_counts": dict(sorted(kind_counts.items())),
            "unfound_targets_total": len(unfound_targets),
        },
        "occurrences": occurrences,
        "unfound_targets": unfound_targets,
    }


def emit_backlog_inventory(json_output: bool = False) -> int:
    inventory = _build_backlog_inventory()
    if json_output:
        print(json.dumps(inventory, indent=2, ensure_ascii=False))
        return 0

    print(f"\n{BLUE}--- Backlog Occurrence Inventory ---{RESET}")
    print(f"Pages: {inventory['pages_health']['status']} unresolved={inventory['pages_health']['unresolved_total']}")
    for status, count in inventory["summary"]["status_counts"].items():
        print(f"- {status}: {count}")
    print(f"Unfound targets: {inventory['summary']['unfound_targets_total']}")
    return 0


def _apply_backlog_occurrence_repairs(pages_health: dict, auto: bool = False, dry_run: bool = False) -> dict:
    inventory = _build_backlog_inventory(pages_health)
    eligible_statuses = {"auto_safe", "auto_safe_policy", "auto_safe_wrapper"}
    entries_by_file: dict[str, list[dict]] = defaultdict(list)
    for occurrence in inventory.get("occurrences", []):
        if occurrence.get("repair_status") not in eligible_statuses:
            continue
        entries_by_file[occurrence["file"]].append(occurrence)

    planned_files: list[str] = []
    applied_files: list[str] = []
    item_summaries: list[dict] = []

    for rel_path, entries in sorted(entries_by_file.items()):
        file_path = PROJECT_ROOT / rel_path
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            continue
        new_content = content

        direct_replacements: dict[str, str] = {}
        wrapper_count = 0
        for entry in entries:
            if entry.get("link_kind") == "wikilink" and entry.get("replacement_target"):
                direct_replacements[entry["target"]] = entry["replacement_target"]
            elif entry.get("link_kind") == "markdown_url_wrapper":
                wrapper_count += 1

        for target, replacement in sorted(direct_replacements.items()):
            new_content = _replace_target_in_content(new_content, target, replacement)

        if wrapper_count:
            def wrapper_repl(match: re.Match) -> str:
                target = match.group("target").strip()
                if not ENCODED_OR_LITERAL_WIKILINK_WRAPPER_RE.search(target):
                    return match.group(0)
                fixed_target = _markdown_target_without_wrappers(target)
                if fixed_target == target or not _markdown_target_path_exists(file_path, fixed_target):
                    return match.group(0)
                return f"[{match.group('label')}]({fixed_target})"

            new_content = MARKDOWN_LINK_RE.sub(wrapper_repl, new_content)

        if new_content == content:
            continue

        planned_files.append(rel_path)
        if not dry_run and auto:
            file_path.write_text(new_content, encoding="utf-8")
            applied_files.append(rel_path)

        item_summaries.append(
            {
                "file": rel_path,
                "occurrences": len(entries),
                "wikilink_targets": sorted(direct_replacements),
                "markdown_url_wrappers": wrapper_count,
            }
        )

    return {
        "cluster": "backlog_occurrence_repairs",
        "changed_files": len(planned_files) if dry_run else len(applied_files),
        "planned_files": planned_files,
        "applied_files": applied_files,
        "files": planned_files,
        "matched_occurrences": sum(len(entries) for entries in entries_by_file.values()),
        "items": item_summaries,
    }


def _collect_category_frontmatter_matches(files: list[Path]) -> list[str]:
    matches: list[str] = []
    for file_path in files:
        try:
            raw = file_path.read_text(encoding="utf-8")
        except Exception:
            continue
        meta, _, _, _, had_frontmatter = split_frontmatter(raw)
        if not had_frontmatter:
            continue
        category_value = meta.get("category", "")
        if CATEGORY_WIKILINK_RE.match(category_value):
            matches.append(str(file_path.relative_to(PROJECT_ROOT)))
    return matches


def _collect_quelle_frontmatter_matches(files: list[Path]) -> list[str]:
    matches: list[str] = []
    for file_path in files:
        try:
            raw = file_path.read_text(encoding="utf-8")
        except Exception:
            continue
        meta, _, _, _, had_frontmatter = split_frontmatter(raw)
        if not had_frontmatter:
            continue
        value = meta.get("quelle", "")
        if not value:
            continue
        if "[[" in value or "]]" in value or "Siebenwind_Bote" in value or "Siebenwind Bote" in value or value.startswith("file://") or value.endswith(".html"):
            matches.append(str(file_path.relative_to(PROJECT_ROOT)))
    return matches


def _extract_bridge_targets(path_str: str) -> list[str]:
    path = PROJECT_ROOT / path_str
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception:
        return []
    match = BRIDGE_TARGET_LINE_RE.search(raw)
    if not match:
        return []
    return [target.strip() for target in WIKILINK_TARGET_RE.findall(match.group("targets")) if target.strip()]


def _build_backlog_board(write_artifacts: bool = True) -> tuple[dict, dict]:
    files = canonical_markdown_files(TECHNICAL_WIKI_ROOT)
    pages_health = _load_pages_health_for_backlog()
    contract = scan_contract(TECHNICAL_WIKI_ROOT, refresh_inventory=False)

    alias_items = []
    escalation_items: list[dict] = []
    for item in pages_health.get("targets", []):
        target = str(item.get("target", "")).strip()
        if not target:
            continue
        candidate = _mechanical_alias_candidate(item)
        if candidate:
            alias_items.append({
                "target": target,
                "canonical_target": candidate,
                "count": item.get("count", 0),
                "source_pages": item.get("source_pages", [])[:10],
            })
            continue
        candidates = [candidate for candidate in item.get("canonical_candidates", []) if candidate]
        if len(candidates) > 1 or (len(candidates) == 1 and normalize_key(target) != normalize_key(candidates[0])):
            escalation_items.append({
                "cluster": "pages_target_ambiguous",
                "source_page": (item.get("source_pages") or [""])[0],
                "current_target": target,
                "candidates": candidates,
                "proposed_decision": candidates[0] if len(candidates) == 1 else "",
                "reason": "multiple or semantically non-identical canonical target candidates",
            })

    category_matches = _collect_category_frontmatter_matches(files)
    quelle_matches = _collect_quelle_frontmatter_matches(files)
    bridge_single_target: list[dict] = []
    bridge_escalation_examples: list[dict] = []
    for detail in contract.get("details", []):
        analysis = detail.get("analysis", {})
        if analysis.get("bridge_status") in {"incomplete", "untracked"}:
            bridge_targets = _extract_bridge_targets(detail.get("path", ""))
            if len(bridge_targets) == 1:
                bridge_single_target.append({
                    "file": detail.get("path", ""),
                    "canonical_target": bridge_targets[0],
                    "bridge_status": analysis.get("bridge_status"),
                })
            else:
                bridge_escalation_examples.append({
                    "file": detail.get("path", ""),
                    "targets": bridge_targets,
                    "bridge_status": analysis.get("bridge_status"),
                })
                escalation_items.append({
                    "cluster": "bridge_invalid",
                    "source_page": detail.get("path", ""),
                    "current_target": "",
                    "candidates": bridge_targets,
                    "proposed_decision": bridge_targets[0] if len(bridge_targets) == 1 else "",
                    "reason": f"bridge page is {analysis.get('bridge_status')} and has {len(bridge_targets)} explicit target(s)",
                })

    board = {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "version": BACKLOG_ARTIFACT_VERSION,
        "pages_health": {
            "status": pages_health.get("status", "UNKNOWN"),
            "unresolved_total": pages_health.get("unresolved_total", 0),
            "unallowlisted_total": pages_health.get("unallowlisted_total", 0),
            "last_validated_at": pages_health.get("last_validated_at"),
        },
        "contract": {
            "bridge_invalid": contract.get("bridge_inventory", {}).get("invalid", 0),
            "contract_violations": contract.get("contract_violations", {}).get("issues", 0),
        },
        "clusters": [
            {
                "cluster": "lane1_target_normalization",
                "match_rule": "pages target has exactly one canonical candidate and normalize_key(target) == normalize_key(candidate)",
                "canonical_target": "per-item single canonical candidate",
                "lane": "lane1",
                "auto_apply_allowed": True,
                "escalate_if": "candidate set is empty, >1, or semantically non-identical",
                "count": len(alias_items),
                "examples": alias_items[:20],
            },
            {
                "cluster": "frontmatter_category_wikilinks",
                "match_rule": "frontmatter category is a bare wikilink such as [[index]] or [[Geschichte]]",
                "canonical_target": "derive_category(path)",
                "lane": "lane1",
                "auto_apply_allowed": True,
                "escalate_if": "file category intentionally differs from enclosing folder",
                "count": len(category_matches),
                "examples": category_matches[:20],
            },
            {
                "cluster": "quelle_frontmatter_lookup",
                "match_rule": "frontmatter quelle contains broken wikilinks or source-like path text and lookup yields exactly one real file",
                "canonical_target": "relative path to unique docs/Quellen file",
                "lane": "lane1",
                "auto_apply_allowed": True,
                "escalate_if": "lookup returns 0 or >1 plausible source files",
                "count": len(quelle_matches),
                "examples": quelle_matches[:20],
            },
            {
                "cluster": "bridge_single_target_review",
                "match_rule": "bridge page has exactly one explicit 'Siehe auch' target",
                "canonical_target": "per-page explicit target",
                "lane": "lane2",
                "auto_apply_allowed": False,
                "escalate_if": "entity type changes or target is semantically lossy",
                "count": len(bridge_single_target),
                "examples": bridge_single_target[:20],
            },
            {
                "cluster": "bridge_escalation",
                "match_rule": "bridge page has zero or multiple explicit targets",
                "canonical_target": "",
                "lane": "lane3",
                "auto_apply_allowed": False,
                "escalate_if": "replacement target is unclear or bridge must remain temporary",
                "count": len(bridge_escalation_examples),
                "examples": bridge_escalation_examples[:20],
            },
        ],
    }
    escalations = {
        "generated_at": board["generated_at"],
        "version": BACKLOG_ARTIFACT_VERSION,
        "items": escalation_items,
    }
    if write_artifacts:
        BACKLOG_BOARD_PATH.parent.mkdir(parents=True, exist_ok=True)
        BACKLOG_BOARD_PATH.write_text(json.dumps(board, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        BACKLOG_ESCALATIONS_PATH.write_text(json.dumps(escalations, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return board, escalations


def _apply_alias_target_normalization(pages_health: dict, auto: bool = False, dry_run: bool = False) -> dict:
    canon_map = get_canon_map(WIKI_DIR)
    if DOCS_WIKI_DIR.exists():
        docs_canon = get_canon_map(DOCS_WIKI_DIR)
        for key, paths in docs_canon.items():
            canon_map[key].extend(path for path in paths if path not in canon_map[key])

    changed_files = 0
    changed_file_paths: set[str] = set()
    fixed_entries: list[dict] = []
    for item in pages_health.get("targets", []):
        target = str(item.get("target", "")).strip()
        replacement = _mechanical_alias_candidate(item)
        if not replacement:
            continue
        source_pages = item.get("source_pages", [])
        target_files = _resolve_source_repair_paths(source_pages)
        per_item_changed: list[str] = []
        for file_path in target_files:
            try:
                content = file_path.read_text(encoding="utf-8")
            except Exception:
                continue
            new_content = _replace_target_in_content(content, target, replacement)
            if new_content == content:
                continue
            per_item_changed.append(str(file_path.relative_to(PROJECT_ROOT)))
            if not dry_run and auto:
                file_path.write_text(new_content, encoding="utf-8")
                changed_files += 1
                changed_file_paths.add(str(file_path.relative_to(PROJECT_ROOT)))
        fixed_entries.append({
            "target": target,
            "canonical_target": replacement,
            "count": item.get("count", 0),
            "source_pages": source_pages[:10],
            "changed_files": per_item_changed,
        })

    return {
        "cluster": "lane1_target_normalization",
        "changed_files": changed_files,
        "matched_targets": len(fixed_entries),
        "files": sorted(changed_file_paths),
        "items": fixed_entries,
    }


def repair_backlog_lane1(auto: bool = False, dry_run: bool = False, json_output: bool = False) -> int:
    pages_health = _load_pages_health_for_backlog()
    files = canonical_markdown_files(TECHNICAL_WIKI_ROOT)
    board, escalations = _build_backlog_board(write_artifacts=not dry_run)

    cluster_results = [
        _apply_backlog_occurrence_repairs(pages_health, auto=auto, dry_run=dry_run),
        repair_frontmatter_categories(files, auto=auto, dry_run=dry_run),
        repair_quelle_frontmatter(files, auto=auto, dry_run=dry_run),
    ]
    planned_files: set[str] = set()
    for item in cluster_results:
        planned_files.update(item.get("files", []))

    summary = {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "mode": "dry-run" if dry_run else "apply",
        "lane": "lane1",
        "auto": auto,
        "artifacts": {
            "backlog_board": str(BACKLOG_BOARD_PATH.relative_to(PROJECT_ROOT)),
            "escalations": str(BACKLOG_ESCALATIONS_PATH.relative_to(PROJECT_ROOT)),
            "written": not dry_run,
        },
        "before": {
            "unresolved_total": pages_health.get("unresolved_total", 0),
            "unallowlisted_total": pages_health.get("unallowlisted_total", 0),
            "last_validated_at": pages_health.get("last_validated_at"),
            "bridge_invalid": board.get("contract", {}).get("bridge_invalid", 0),
        },
        "clusters": cluster_results,
        "escalation_count": len(escalations.get("items", [])),
        "changed_files_total": sum(item.get("changed_files", 0) for item in cluster_results),
        "planned_files_total": len(planned_files),
    }
    if json_output:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
    else:
        print(f"\n{BLUE}--- Backlog Lane 1 Repair ---{RESET}")
        if summary["artifacts"]["written"]:
            print(f"Artifacts: {summary['artifacts']['backlog_board']}, {summary['artifacts']['escalations']}")
        else:
            print("Artifacts: dry-run, keine Board-Dateien geschrieben")
        for item in cluster_results:
            matched = item.get("matched_occurrences", item.get("matched_targets", item.get("matched_files", 0)))
            print(f"- {item['cluster']}: matched={matched} changed={item.get('changed_files', 0)}")
        if dry_run:
            print(f"{YELLOW}Dry-run aktiv: keine Dateien geschrieben.{RESET}")
        else:
            print(f"{GREEN}{summary['changed_files_total']} Dateien aktualisiert.{RESET}")
    return 0


def emit_backlog_board(json_output: bool = False, dry_run: bool = False) -> int:
    board, escalations = _build_backlog_board(write_artifacts=not dry_run)
    payload = {
        "generated_at": board["generated_at"],
        "version": board["version"],
        "artifacts": {
            "backlog_board": str(BACKLOG_BOARD_PATH.relative_to(PROJECT_ROOT)),
            "escalations": str(BACKLOG_ESCALATIONS_PATH.relative_to(PROJECT_ROOT)),
            "written": not dry_run,
        },
        "pages_health": board["pages_health"],
        "contract": board["contract"],
        "clusters": board["clusters"],
        "escalation_count": len(escalations.get("items", [])),
    }
    if json_output:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
    else:
        print(f"\n{BLUE}--- Backlog Cluster Board ---{RESET}")
        if payload["artifacts"]["written"]:
            print(f"Board: {payload['artifacts']['backlog_board']}")
            print(f"Eskalationen: {payload['artifacts']['escalations']}")
        else:
            print("Dry-run: keine Board-Dateien geschrieben.")
        for cluster in payload["clusters"]:
            print(f"- {cluster['cluster']}: {cluster['count']} [{cluster['lane']}]")
    return 0


def repair_roamlinks(auto: bool = False, dry_run: bool = False) -> int:
    print(f"\n{BLUE}--- Pages / Roamlinks Repair ---{RESET}")
    snapshot = load_pages_health_snapshot()
    if not snapshot or (
        snapshot.get("pages_health", {}).get("status") == "UNKNOWN"
        and not snapshot.get("pages_health", {}).get("targets")
    ):
        snapshot = collect_pages_build_report(config="mkdocs.yml", no_clean=False)
    pages_health = snapshot.get("pages_health", {})
    targets = pages_health.get("targets", [])
    if not targets:
        print(f"{GREEN}Keine unresolved Pages-Targets gefunden.{RESET}")
        return 0

    canon_map = get_canon_map(WIKI_DIR)
    if DOCS_WIKI_DIR.exists():
        docs_canon = get_canon_map(DOCS_WIKI_DIR)
        for key, paths in docs_canon.items():
            canon_map[key].extend(path for path in paths if path not in canon_map[key])

    fixed_entries: list[dict] = []
    ambiguous_entries: list[dict] = []
    files_changed = 0
    repairable_classes = {"safe_exact_match", "safe_alias_match"}
    classification_counts: dict[str, int] = {
        "safe_exact_match": 0,
        "safe_alias_match": 0,
        "generic_term_conflict": 0,
        "needs_historian": 0,
        "needs_human": 0,
    }

    for item in targets:
        target = item["target"]
        source_pages = item.get("source_pages", [])
        classification = str(item.get("classification", "needs_historian"))
        classification_counts.setdefault(classification, 0)
        classification_counts[classification] += item.get("count", 0)
        if classification not in repairable_classes:
            ambiguous_entries.append(
                {
                    "target": target,
                    "count": item.get("count", 0),
                    "source_pages": source_pages,
                    "classification": classification,
                    "suggestions": item.get("canonical_candidates", []),
                }
            )
            continue
        replacement, suggestions = _roamlink_target_candidates(target, canon_map)
        if not replacement:
            ambiguous_entries.append(
                {
                    "target": target,
                    "count": item.get("count", 0),
                    "source_pages": source_pages,
                    "classification": classification,
                    "suggestions": suggestions,
                }
            )
            continue

        target_files = _resolve_source_repair_paths(source_pages)
        changed_files: list[str] = []
        for file_path in target_files:
            try:
                content = file_path.read_text(encoding="utf-8")
            except Exception:
                continue
            new_content = _replace_target_in_content(content, target, replacement)
            if new_content == content:
                continue
            changed_files.append(str(file_path.relative_to(PROJECT_ROOT)))
            if not dry_run and (auto or input(f"{file_path.relative_to(PROJECT_ROOT)} auf [[{replacement}]] aktualisieren? [y/n]: ").lower() == "y"):
                file_path.write_text(new_content, encoding="utf-8")
                files_changed += 1

        fixed_entries.append(
            {
                "target": target,
                "replacement": replacement,
                "count": item.get("count", 0),
                "source_pages": source_pages,
                "changed_files": changed_files,
                "classification": classification,
            }
        )

    report = {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "mode": "dry-run" if dry_run else "apply",
        "classification_counts": classification_counts,
        "fixed": fixed_entries,
        "ambiguous": ambiguous_entries,
        "files_changed": files_changed,
    }
    ROAMLINK_REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = ROAMLINK_REPORT_DIR / f"ROAMLINK_REPAIR_REPORT_{now_stamp()}.json"
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"Fixbare Targets: {len(fixed_entries)}")
    print(f"Ambiguous / suggestion-only: {len(ambiguous_entries)}")
    print(f"Report: {report_path.relative_to(PROJECT_ROOT)}")
    if dry_run:
        print(f"{YELLOW}Dry-run aktiv: keine Dateien geschrieben.{RESET}")
    else:
        print(f"{GREEN}{files_changed} Dateien aktualisiert.{RESET}")
    return 0 if fixed_entries or ambiguous_entries else 0


def main():
    parser = argparse.ArgumentParser(description="Siebenwind Repair Tool 2.0")
    parser.add_argument("--path", default=str(WIKI_DIR), help="Zielverzeichnis")
    parser.add_argument("--auto", action="store_true", help="Auto-Repair ohne Nachfrage")
    parser.add_argument("--full", action="store_true", help="Voller Durchlauf (1-3) ohne Nachfrage")
    parser.add_argument("--check-collision", help="Prüft, ob ein Dateiname bereits existiert")
    parser.add_argument("--fix-roamlinks", action="store_true", help="Aggressive repair path for unresolved Pages / Roamlinks targets")
    parser.add_argument("--backlog-board", action="store_true", help="Build cluster-based backlog board and escalation artifacts")
    parser.add_argument("--backlog-inventory", action="store_true", help="Inventory concrete Pages backlog occurrences without writing artifacts")
    parser.add_argument("--apply-lane1", action="store_true", help="Apply the conservative lane-1 mechanical backlog wave")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing files")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable JSON for backlog-oriented repair modes")
    args = parser.parse_args()
    
    target_dir = Path(args.path)
    if not target_dir.exists():
        print(f"Verzeichnis fehlt: {target_dir}")
        sys.exit(1)

    # Collision Check Mode
    if args.check_collision:
        print(f"Indiziere Canon Map für {target_dir}...")
        canon_map = get_canon_map(target_dir)
        key = normalize_key(args.check_collision)
        if key in canon_map:
            print(f"{RED}KOLLISION GEFUNDEN:{RESET}")
            for p in canon_map[key]:
                print(f"  - {p}")
            sys.exit(1)
        else:
            print(f"{GREEN}Keine Kollision. Name ist frei.{RESET}")
            sys.exit(0)

    if args.fix_roamlinks:
        sys.exit(repair_roamlinks(auto=args.auto, dry_run=args.dry_run))

    if args.backlog_inventory:
        sys.exit(emit_backlog_inventory(json_output=args.json))

    if args.backlog_board:
        sys.exit(emit_backlog_board(json_output=args.json, dry_run=args.dry_run))

    if args.apply_lane1:
        sys.exit(repair_backlog_lane1(auto=args.auto, dry_run=args.dry_run, json_output=args.json))

    print(f"Indiziere Canon Map für {target_dir}...")
    canon_map = get_canon_map(target_dir)

    # Normal Mode
    files = list(target_dir.rglob("*.md"))
    source_files = _source_repair_file_set(files)
    
    if args.auto or args.full:
        mode_label = "FULL REPAIR" if args.full else "AUTO REPAIR"
        print(f"{BLUE}=== {mode_label} STARTED ==={RESET}")
        check_duplicates(canon_map)
        run_full_repair(files, source_files, canon_map, auto=True)
        print(f"{GREEN}=== FERTIG ==={RESET}")
    else:
        check_duplicates(canon_map)
        while True:
            print("\nOptionen:")
            print("  1) Frontmatter Fixer")
            print("  2) Smart Link Repair")
            print("  3) Source Reference Repair")
            print("  4) Voller Durchlauf (1-3) [Standard]")
            print("  q) Beenden")
            c = input("Wahl [4]: ").strip().lower() or "4"
            if c == '1': fix_frontmatter(files)
            elif c == '2': repair_links(files, canon_map)
            elif c == '3': repair_source_references(source_files)
            elif c == '4': run_full_repair(files, source_files, canon_map)
            elif c == 'q': break

if __name__ == "__main__":
    main()
