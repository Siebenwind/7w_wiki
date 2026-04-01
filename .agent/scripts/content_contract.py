#!/usr/bin/env python3
"""
Shared content contract helpers for drift prevention.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
TECHNICAL_WIKI_ROOT = REPO_ROOT / "docs" / "Siebenwind_Wiki"
LEGACY_WIKI_ROOT = REPO_ROOT / "Siebenwind_Wiki"
SOURCES_ROOT = REPO_ROOT / "Quellen"
HOMEPAGE_URL = "https://www.siebenwind.de/"
TRUTH_HIERARCHY = ["homepage", "sources", "wiki"]
TRUTH_RANK = {"homepage": 3, "sources": 2, "wiki": 1}
INVENTORY_PATH = REPO_ROOT / ".agent" / "data" / "wiki_inventory.json"
INVENTORY_HISTORY_DIR = REPO_ROOT / ".agent" / "data" / "wiki_inventory_history"
CACHE_DIR = REPO_ROOT / ".agent" / "data" / "cache"
ALLOWED_LEGACY_ARTIFACTS = {
    Path("10_Archiv/Wiki_Statistiken.md"),
}
CONTENT_CONTRACT_SCHEMA_VERSION = 2
INVENTORY_SCHEMA_VERSION = 2
NORMALIZE_TRANSLATION = str.maketrans({
    "ä": "ae",
    "ö": "oe",
    "ü": "ue",
    "ß": "ss",
    "Ä": "ae",
    "Ö": "oe",
    "Ü": "ue",
})

LEGACY_FORBIDDEN_FRONTMATTER_KEYS = {"layout"}
STUB_REQUIRED_FIELDS = {
    "owner": "UNASSIGNED",
    "reason": "legacy_stub",
}
FRONTMATTER_ORDER = [
    "uuid",
    "title",
    "category",
    "status",
    "epistemic",
    "quelle",
    "author",
    "owner",
    "review_until",
    "reason",
    "replacement_hint",
    "bridge_mode",
    "bridge_target",
    "bridge_ticket",
    "bridge_review_until",
    "updated_at",
    "aliases",
]
METADATA_LINE_RE = re.compile(r"^\*\*(?P<label>[^*][^:]*?):\*\*\s*(?P<value>.+?)\s*$")
H1_RE = re.compile(r"^\s*#\s+(?P<title>.+?)\s*$")
LEGACY_INDEX_LINK_RE = re.compile(
    r"\[\[03_Gesellschaft/index#(?P<anchor>[^\]|]+)(?:\|(?P<label>[^\]]+))?\]\]"
)
MARKDOWN_LINK_RE = re.compile(r"(?<!\!)\[(?P<label>[^\]]+)\]\((?P<target>[^)]+)\)")
BOTE_SOURCE_LINK_RE = re.compile(
    r"\[(?P<label>(?:\[\[[^\]]+\]\][^\]]*)+)\]\((?P<target>[^)]*Quellen/[^)]*(?:\[\[[^\]]+\]\][^)]*)+)\)"
)
DOUBLE_BRACKET_LABEL_SOURCE_LINK_RE = re.compile(
    r"\[\[(?P<label>[^\]]+)\]\]\((?P<target>[^)]*(?:\[\[[^\]]+\]\][^)]*)+)\)"
)
CATEGORY_WIKILINK_RE = re.compile(r"^\s*\[\[(?P<target>[^\]|]+)(?:\|(?P<label>[^\]]+))?\]\]\s*$")
LEGACY_INDEX_LINK_TARGETS = {
    "dwarschim": "Dwarschim",
    "siebenwindkronregiment": "Siebenwind_Kronregiment",
    "loewenorden": "Löwenorden",
    "weisserpfad": "Weißer_Pfad",
    "dergrosserat": "Der_Große_Rat",
    "malthust": "Region_Malthust",
    "handwerk": "Handwerk_Übersicht",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def iso_from_timestamp(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_key(value: str) -> str:
    normalized = value.translate(NORMALIZE_TRANSLATION).lower()
    return re.sub(r"[^a-z0-9]", "", normalized)


def content_hash(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def _json_hash(payload: Any) -> str:
    normalized = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return content_hash(normalized)


def fingerprint_paths(paths: list[Path], *, extra: dict[str, Any] | None = None) -> str:
    payload = []
    for path in sorted(paths):
        try:
            stat = path.stat()
        except FileNotFoundError:
            payload.append({"path": str(path), "missing": True})
            continue
        payload.append(
            {
                "path": str(path.relative_to(REPO_ROOT) if path.is_absolute() else path),
                "size": stat.st_size,
                "mtime_ns": stat.st_mtime_ns,
            }
        )
    return _json_hash({"paths": payload, "extra": extra or {}})


def load_analysis_cache(name: str, *, version: int, inputs_fingerprint: str) -> dict | None:
    cache_path = CACHE_DIR / f"{name}.json"
    if not cache_path.exists():
        return None
    try:
        payload = json.loads(cache_path.read_text(encoding="utf-8"))
    except Exception:
        return None
    if payload.get("version") != version:
        return None
    if payload.get("inputs_fingerprint") != inputs_fingerprint:
        return None
    return payload


def write_analysis_cache(name: str, *, version: int, inputs_fingerprint: str, payload: Any) -> dict:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_payload = {
        "version": version,
        "generated_at": now_iso(),
        "inputs_fingerprint": inputs_fingerprint,
        "payload": payload,
    }
    (CACHE_DIR / f"{name}.json").write_text(
        json.dumps(cache_payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return cache_payload


def split_frontmatter(raw: str) -> tuple[dict[str, str], str, list[str], list[str], bool]:
    if not raw.startswith("---\n"):
        return {}, raw, [], [], False

    end = raw.find("\n---\n", 4)
    if end == -1:
        return {}, raw, [], [], False

    frontmatter = raw[4:end]
    body = raw[end + 5 :]
    meta: dict[str, str] = {}
    order: list[str] = []
    duplicates: list[str] = []
    seen = Counter()

    for line in frontmatter.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        key_lower = key.lower()
        seen[key_lower] += 1
        if seen[key_lower] > 1:
            duplicates.append(key_lower)
        if key_lower not in meta:
            meta[key_lower] = value
            order.append(key_lower)

    return meta, body, order, duplicates, True


def serialize_frontmatter(meta: dict[str, str], body: str, order: list[str] | None = None) -> str:
    keys: list[str] = []
    seen: set[str] = set()
    for key in FRONTMATTER_ORDER:
        if key in meta and key not in seen:
            keys.append(key)
            seen.add(key)
    if order:
        for key in order:
            if key in meta and key not in seen:
                keys.append(key)
                seen.add(key)
    for key in sorted(meta):
        if key not in seen:
            keys.append(key)
            seen.add(key)

    lines = ["---"]
    for key in keys:
        value = meta[key]
        lines.append(f"{key}: {value}")
    lines.extend(["---", ""])

    normalized_body = body
    if normalized_body and not normalized_body.endswith("\n"):
        normalized_body += "\n"
    return "\n".join(lines) + normalized_body


def extract_first_h1(body: str) -> str:
    for line in body.splitlines():
        match = H1_RE.match(line)
        if match:
            title = match.group("title").strip()
            return re.sub(r"\[\[(.*?)(?:\|.*?)?\]\]", r"\1", title).strip()
    return ""


def derive_category(path: Path) -> str:
    parent_name = path.parent.name
    mapping = {
        "04_Chronik": "Chronik",
        "07_Persoenlichkeiten": "Persoenlichkeiten",
        "02_Geografie": "Geografie",
        "03_Gesellschaft": "Gesellschaft",
        "10_Archiv": "Archiv",
        "01_Pantheon": "Religion",
        "05_Magie": "Magie",
        "05_Geschichte": "Geschichte",
        "09_Bibliothek": "Bibliothek",
        "08_Bestiarium": "Bestiarium",
        "00_Fundament": "Fundament",
    }
    return mapping.get(parent_name, parent_name.replace("_", " "))


def detect_inline_metadata_block(body: str) -> dict | None:
    lines = body.splitlines()
    h1_index = None
    for index, line in enumerate(lines):
        if H1_RE.match(line):
            h1_index = index
            break
    if h1_index is None:
        return None

    block_start = h1_index + 1
    while block_start < len(lines) and not lines[block_start].strip():
        block_start += 1

    items: list[tuple[str, str]] = []
    index = block_start
    while index < len(lines):
        line = lines[index].strip()
        match = METADATA_LINE_RE.match(line)
        if not match:
            break
        items.append((match.group("label").strip(), match.group("value").strip()))
        index += 1

    if len(items) < 2:
        return None

    return {
        "items": items,
        "start_line": block_start,
        "end_line": index,
    }


def normalize_inline_metadata_block(body: str) -> tuple[str, list[tuple[str, str]]]:
    block = detect_inline_metadata_block(body)
    if not block:
        return body, []

    lines = body.splitlines()
    start = block["start_line"]
    end = block["end_line"]
    replacement = ['!!! info "Metadaten"']
    for label, value in block["items"]:
        replacement.append(f"    - **{label}:** {value}")

    new_lines = lines[:start] + replacement + [""] + lines[end:]
    new_body = "\n".join(new_lines).rstrip() + "\n"
    return new_body, block["items"]


def normalize_legacy_index_links(body: str) -> tuple[str, list[dict]]:
    changes: list[dict] = []

    def repl(match: re.Match[str]) -> str:
        anchor = match.group("anchor").strip()
        label = (match.group("label") or "").strip()
        target = LEGACY_INDEX_LINK_TARGETS.get(normalize_key(anchor), anchor)
        replacement = f"[[{target}|{label}]]" if label and label != target else f"[[{target}]]"
        if replacement != match.group(0):
            changes.append(
                {
                    "type": "legacy_index_wikilink",
                    "from": match.group(0),
                    "to": replacement,
                }
            )
        return replacement

    return LEGACY_INDEX_LINK_RE.sub(repl, body), changes


def _flatten_wikilinks(value: str) -> str:
    flattened = re.sub(r"\[\[(.*?)(?:\|.*?)?\]\]", r"\1", value)
    return flattened.replace("[", "").replace("]", "").strip()


def normalize_source_markdown_links(body: str) -> tuple[str, list[dict]]:
    changes: list[dict] = []

    def repl(match: re.Match[str]) -> str:
        label = match.group("label")
        target = match.group("target")
        if "Quellen/" not in target and "Archiv/Ingestion_Reports/" not in target:
            return match.group(0)
        if "[[" not in label and "]]" not in label and "[[" not in target and "]]" not in target:
            return match.group(0)

        new_label = _flatten_wikilinks(label)
        new_target = target.replace("[[", "").replace("]]", "")
        replacement = f"[{new_label}]({new_target})"
        if replacement != match.group(0):
            changes.append(
                {
                    "type": "legacy_source_markdown_link",
                    "from": match.group(0),
                    "to": replacement,
                }
            )
        return replacement

    return MARKDOWN_LINK_RE.sub(repl, body), changes


def normalize_bote_source_links(body: str) -> tuple[str, list[dict]]:
    changes: list[dict] = []

    def repl(match: re.Match[str]) -> str:
        label = _flatten_wikilinks(match.group("label"))
        target = _flatten_wikilinks(match.group("target"))
        replacement = f"[{label}]({target})"
        if replacement != match.group(0):
            changes.append(
                {
                    "type": "legacy_bote_source_link",
                    "from": match.group(0),
                    "to": replacement,
                }
            )
        return replacement

    return BOTE_SOURCE_LINK_RE.sub(repl, body), changes


def normalize_flattened_source_wikilink_labels(body: str) -> tuple[str, list[dict]]:
    changes: list[dict] = []

    def repl(match: re.Match[str]) -> str:
        label = match.group("label")
        target = match.group("target")
        if "Quellen/" not in target and "Archiv/Ingestion_Reports/" not in target:
            return match.group(0)
        if ("[[" not in label and "]]" not in label) or ("[[" not in target and "]]" not in target):
            return match.group(0)

        new_label = _flatten_wikilinks(label)
        new_target = target.replace("[[", "").replace("]]", "")
        replacement = f"[{new_label}]({new_target})"
        if replacement != match.group(0):
            changes.append(
                {
                    "type": "legacy_source_markdown_link",
                    "from": match.group(0),
                    "to": replacement,
                }
            )
        return replacement

    return DOUBLE_BRACKET_LABEL_SOURCE_LINK_RE.sub(repl, body), changes


def is_stub(meta: dict[str, str], body: str) -> bool:
    status = meta.get("status", "").strip().strip('"').strip("'").lower()
    if status == "stub":
        return True
    return body.lstrip().startswith("# Stub")


def bridge_status(meta: dict[str, str], body: str) -> str:
    raw = body.lower()
    if any(key in meta for key in ("bridge_mode", "bridge_target", "bridge_ticket", "bridge_review_until")):
        required = {"bridge_mode", "bridge_target", "bridge_ticket", "bridge_review_until"}
        return "tracked" if required.issubset(set(meta)) else "incomplete"
    if "brueckenartikel" in raw or "brückenartikel" in raw:
        return "untracked"
    return "none"


def classify_file(path: Path, meta: dict[str, str], body: str) -> str:
    if path.name == "index.md":
        return "index"
    if is_stub(meta, body):
        return "stub"
    if bridge_status(meta, body) != "none":
        return "bridge"
    return "article"


def default_stub_review_until() -> str:
    return (date.today() + timedelta(days=180)).isoformat()


def normalize_document(raw: str, path: Path) -> tuple[str, list[dict], dict[str, str], dict]:
    meta, body, order, duplicates, had_frontmatter = split_frontmatter(raw)
    changes: list[dict] = []
    original_meta = dict(meta)
    original_body = body

    if not had_frontmatter:
        h1_title = extract_first_h1(body)
        meta = {
            "title": f'"{h1_title or path.stem.replace("_", " ")}"',
            "category": derive_category(path),
        }
        order = ["title", "category"]
        changes.append({"type": "missing_frontmatter"})

    for duplicate in sorted(set(duplicates)):
        changes.append({"type": "duplicate_frontmatter_key", "key": duplicate})

    for key in sorted(LEGACY_FORBIDDEN_FRONTMATTER_KEYS):
        if key in meta:
            meta.pop(key, None)
            changes.append({"type": "legacy_field", "key": key})

    source_value = meta.get("quelle", "")
    if "[[" in source_value or "]]" in source_value:
        normalized_source = _flatten_wikilinks(source_value)
        if normalized_source != source_value:
            meta["quelle"] = normalized_source
            changes.append({"type": "legacy_source_field", "from": source_value, "to": normalized_source})

    category_value = meta.get("category", "")
    category_match = CATEGORY_WIKILINK_RE.match(category_value)
    if category_match:
        normalized_category = derive_category(path)
        if normalized_category != category_value:
            meta["category"] = normalized_category
            changes.append({"type": "category_frontmatter_wikilink", "from": category_value, "to": normalized_category})

    h1_title = extract_first_h1(body)
    if h1_title:
        title_value = meta.get("title", "").strip().strip('"').strip("'")
        if title_value != h1_title:
            meta["title"] = f'"{h1_title}"'
            changes.append({"type": "title_h1_mismatch", "yaml_title": title_value, "h1_title": h1_title})

    normalized_body, metadata_items = normalize_inline_metadata_block(body)
    if metadata_items:
        body = normalized_body
        changes.append(
            {
                "type": "inline_metadata_block",
                "labels": [label for label, _ in metadata_items],
            }
        )

    normalized_body, legacy_index_changes = normalize_legacy_index_links(body)
    if legacy_index_changes:
        body = normalized_body
        changes.extend(legacy_index_changes)

    normalized_body, legacy_source_link_changes = normalize_source_markdown_links(body)
    if legacy_source_link_changes:
        body = normalized_body
        changes.extend(legacy_source_link_changes)

    normalized_body, bote_source_link_changes = normalize_bote_source_links(body)
    if bote_source_link_changes:
        body = normalized_body
        changes.extend(bote_source_link_changes)

    normalized_body, flattened_source_wikilink_changes = normalize_flattened_source_wikilink_labels(body)
    if flattened_source_wikilink_changes:
        body = normalized_body
        changes.extend(flattened_source_wikilink_changes)

    if is_stub(meta, body):
        status = meta.get("status", "stub").strip().strip('"').strip("'").lower()
        if status != "stub":
            changes.append({"type": "stub_status_normalized", "from": status, "to": "stub"})
        meta["status"] = "stub"
        for key, default_value in STUB_REQUIRED_FIELDS.items():
            if not meta.get(key):
                meta[key] = default_value
                changes.append({"type": "stub_field_added", "key": key})
        if not meta.get("review_until"):
            meta["review_until"] = default_stub_review_until()
            changes.append({"type": "stub_field_added", "key": "review_until"})

    new_raw = raw
    if meta != original_meta or body != original_body or not had_frontmatter:
        new_raw = serialize_frontmatter(meta, body, order)

    analysis = {
        "has_frontmatter": had_frontmatter,
        "duplicates": sorted(set(duplicates)),
        "classification": classify_file(path, meta, body),
        "stub_status": "stub" if is_stub(meta, body) else "none",
        "bridge_status": bridge_status(meta, body),
    }
    return new_raw, changes, meta, analysis


def inspect_file(path: Path) -> dict:
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception as exc:
        return {
            "path": str(path.relative_to(REPO_ROOT)),
            "error": str(exc),
            "changes": [],
            "analysis": {"classification": "unknown", "stub_status": "none", "bridge_status": "none"},
        }

    _, changes, meta, analysis = normalize_document(raw, path)
    return {
        "path": str(path.relative_to(REPO_ROOT)),
        "changes": changes,
        "analysis": analysis,
        "meta": meta,
    }


def canonical_markdown_files(target: Path | None = None) -> list[Path]:
    root = target or TECHNICAL_WIKI_ROOT
    if root.is_file():
        return [root]
    if not root.exists():
        return []
    return sorted(path for path in root.rglob("*.md") if path.is_file())


def canonical_target_scope(target: Path | None = None) -> str:
    if target is None:
        return "canonical_root"
    resolved = target.resolve()
    if resolved == TECHNICAL_WIKI_ROOT.resolve():
        return "canonical_root"
    return "scoped"


def detect_split_brain_files() -> list[Path]:
    if not LEGACY_WIKI_ROOT.exists():
        return []
    findings: list[Path] = []
    for path in sorted(LEGACY_WIKI_ROOT.rglob("*.md")):
        rel = path.relative_to(LEGACY_WIKI_ROOT)
        if rel in ALLOWED_LEGACY_ARTIFACTS:
            continue
        findings.append(path)
    return findings


def load_inventory() -> dict:
    if not INVENTORY_PATH.exists():
        return {}
    try:
        return json.loads(INVENTORY_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {}


def inventory_metadata() -> dict:
    snapshot_path = ""
    inventory_cache = CACHE_DIR / "wiki_inventory.json"
    if inventory_cache.exists():
        try:
            payload = json.loads(inventory_cache.read_text(encoding="utf-8"))
            snapshot_path = str(payload.get("payload", {}).get("snapshot_path", ""))
        except Exception:
            snapshot_path = ""
    return {
        "inventory_path": str(INVENTORY_PATH.relative_to(REPO_ROOT)),
        "snapshot_path": snapshot_path,
    }


def build_inventory(activity: str = "audit", agent: str = "content_contract") -> dict:
    previous = load_inventory()
    previous_map = {entry["path"]: entry for entry in previous.get("items", [])}
    items: list[dict] = []
    for path in canonical_markdown_files():
        raw = path.read_text(encoding="utf-8")
        meta, body, _, _, _ = split_frontmatter(raw)
        path_key = str(path.relative_to(REPO_ROOT))
        digest = content_hash(raw)
        previous_entry = previous_map.get(path_key)
        if previous_entry and previous_entry.get("content_hash") == digest:
            modified_at = previous_entry.get("modified_at", iso_from_timestamp(path.stat().st_mtime))
        else:
            modified_at = iso_from_timestamp(path.stat().st_mtime)

        items.append(
            {
                "path": path_key,
                "content_hash": digest,
                "modified_at": modified_at,
                "classification": classify_file(path, meta, body),
                "source_tree": "wiki",
                "truth_rank": TRUTH_RANK["wiki"],
                "activity": activity,
                "agent": agent,
                "stub_status": "stub" if is_stub(meta, body) else "none",
                "bridge_status": bridge_status(meta, body),
                "review_until": meta.get("review_until"),
            }
        )

    return {
        "generated_at": now_iso(),
        "technical_wiki_root": str(TECHNICAL_WIKI_ROOT.relative_to(REPO_ROOT)),
        "truth_hierarchy": TRUTH_HIERARCHY,
        "epistemic_precedence": {
            "homepage": HOMEPAGE_URL,
            "sources": str(SOURCES_ROOT.relative_to(REPO_ROOT)),
            "wiki": str(TECHNICAL_WIKI_ROOT.relative_to(REPO_ROOT)),
        },
        "activity": activity,
        "agent": agent,
        "items": items,
    }


def write_inventory(activity: str = "audit", agent: str = "content_contract", use_cache: bool = True) -> dict:
    files = canonical_markdown_files()
    inputs_fingerprint = fingerprint_paths(
        files,
        extra={
            "schema_version": INVENTORY_SCHEMA_VERSION,
            "technical_root": str(TECHNICAL_WIKI_ROOT.relative_to(REPO_ROOT)),
            "truth_hierarchy": TRUTH_HIERARCHY,
        },
    )
    if use_cache:
        cached = load_analysis_cache(
            "wiki_inventory",
            version=INVENTORY_SCHEMA_VERSION,
            inputs_fingerprint=inputs_fingerprint,
        )
        if cached and INVENTORY_PATH.exists():
            cached_payload = cached.get("payload", {})
            inventory = load_inventory()
            if inventory:
                inventory["latest_path"] = str(INVENTORY_PATH.relative_to(REPO_ROOT))
                inventory["snapshot_path"] = str(cached_payload.get("snapshot_path", ""))
                inventory["cache"] = {
                    "name": "wiki_inventory",
                    "hit": True,
                    "version": INVENTORY_SCHEMA_VERSION,
                    "inputs_fingerprint": inputs_fingerprint,
                }
                return inventory

    inventory = build_inventory(activity=activity, agent=agent)
    INVENTORY_PATH.parent.mkdir(parents=True, exist_ok=True)
    INVENTORY_HISTORY_DIR.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(inventory, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    INVENTORY_PATH.write_text(payload, encoding="utf-8")
    stamped = INVENTORY_HISTORY_DIR / f"wiki_inventory_{datetime.now(timezone.utc).strftime('%Y-%m-%d_%H%M%S')}.json"
    stamped.write_text(payload, encoding="utf-8")
    inventory["latest_path"] = str(INVENTORY_PATH.relative_to(REPO_ROOT))
    inventory["snapshot_path"] = str(stamped.relative_to(REPO_ROOT))
    write_analysis_cache(
        "wiki_inventory",
        version=INVENTORY_SCHEMA_VERSION,
        inputs_fingerprint=inputs_fingerprint,
        payload={
            "latest_path": inventory["latest_path"],
            "snapshot_path": inventory["snapshot_path"],
        },
    )
    inventory["cache"] = {
        "name": "wiki_inventory",
        "hit": False,
        "version": INVENTORY_SCHEMA_VERSION,
        "inputs_fingerprint": inputs_fingerprint,
    }
    return inventory


def _scan_contract_uncached(files: list[Path]) -> dict:
    details: list[dict] = []
    render_hygiene = 0
    contract_violations = 0
    stub_total = 0
    stub_invalid = 0
    bridge_total = 0
    bridge_invalid = 0
    traceability_gaps = 0

    for path in files:
        detail = inspect_file(path)
        details.append(detail)
        if "error" in detail:
            traceability_gaps += 1
            continue
        change_types = {change["type"] for change in detail["changes"]}
        if "inline_metadata_block" in change_types:
            render_hygiene += 1
        if any(change_type in change_types for change_type in {"legacy_field", "duplicate_frontmatter_key", "missing_frontmatter", "title_h1_mismatch", "legacy_index_wikilink", "legacy_source_markdown_link", "legacy_bote_source_link", "legacy_source_field", "category_frontmatter_wikilink"}):
            contract_violations += 1
        if detail["analysis"]["stub_status"] == "stub":
            stub_total += 1
            required = {"owner", "review_until", "reason"}
            if not required.issubset(set(detail["meta"])):
                stub_invalid += 1
        if detail["analysis"]["bridge_status"] != "none":
            bridge_total += 1
            if detail["analysis"]["bridge_status"] != "tracked":
                bridge_invalid += 1

    return {
        "scanned_files": len(files),
        "render_hygiene": {
            "issues": render_hygiene,
        },
        "contract_violations": {
            "issues": contract_violations,
        },
        "stub_inventory": {
            "total": stub_total,
            "invalid": stub_invalid,
        },
        "bridge_inventory": {
            "total": bridge_total,
            "invalid": bridge_invalid,
        },
        "details": details,
    }


def _contract_scan_fingerprint(files: list[Path], *, scope: str) -> str:
    return fingerprint_paths(
        files,
        extra={
            "schema_version": CONTENT_CONTRACT_SCHEMA_VERSION,
            "scope": scope,
            "legacy_forbidden_frontmatter_keys": sorted(LEGACY_FORBIDDEN_FRONTMATTER_KEYS),
            "stub_required_fields": STUB_REQUIRED_FIELDS,
            "allowed_legacy_artifacts": sorted(str(path) for path in ALLOWED_LEGACY_ARTIFACTS),
        },
    )


def scan_contract(target: Path | None = None, *, refresh_inventory: bool | None = None, use_cache: bool = True) -> dict:
    files = canonical_markdown_files(target)
    scope = canonical_target_scope(target)
    refresh_inventory = (scope == "canonical_root") if refresh_inventory is None else refresh_inventory
    inputs_fingerprint = _contract_scan_fingerprint(files, scope=scope)
    cached_payload = None

    if scope == "canonical_root" and use_cache:
        cached = load_analysis_cache(
            "content_contract_scan",
            version=CONTENT_CONTRACT_SCHEMA_VERSION,
            inputs_fingerprint=inputs_fingerprint,
        )
        if cached:
            cached_payload = cached.get("payload", {})

    report = cached_payload if cached_payload is not None else _scan_contract_uncached(files)

    split_brain = detect_split_brain_files()
    inventory = (
        write_inventory(activity="scan_contract", agent="content_contract", use_cache=use_cache)
        if refresh_inventory
        else inventory_metadata()
    )
    traceability_issues = int(report.get("traceability_gaps", {}).get("issues", 0))

    final_report = {
        **report,
        "violations_found": (
            report["render_hygiene"]["issues"]
            + report["contract_violations"]["issues"]
            + report["stub_inventory"]["invalid"]
            + report["bridge_inventory"]["invalid"]
            + len(split_brain)
            + traceability_issues
        ),
        "split_brain": {
            "issues": len(split_brain),
            "files": [str(path.relative_to(REPO_ROOT)) for path in split_brain[:50]],
        },
        "traceability_gaps": {
            "issues": traceability_issues,
            "inventory_path": inventory.get("inventory_path", inventory.get("latest_path", str(INVENTORY_PATH.relative_to(REPO_ROOT)))),
            "snapshot_path": inventory.get("snapshot_path", ""),
        },
        "cache": {
            "name": "content_contract_scan",
            "hit": cached_payload is not None,
            "scope": scope,
            "version": CONTENT_CONTRACT_SCHEMA_VERSION,
            "inputs_fingerprint": inputs_fingerprint,
        },
    }

    if scope == "canonical_root" and cached_payload is None and use_cache:
        write_analysis_cache(
            "content_contract_scan",
            version=CONTENT_CONTRACT_SCHEMA_VERSION,
            inputs_fingerprint=inputs_fingerprint,
            payload={
                "scanned_files": final_report["scanned_files"],
                "render_hygiene": final_report["render_hygiene"],
                "contract_violations": final_report["contract_violations"],
                "stub_inventory": final_report["stub_inventory"],
                "bridge_inventory": final_report["bridge_inventory"],
                "split_brain": final_report["split_brain"],
                "details": final_report["details"],
                "traceability_gaps": {"issues": traceability_issues},
            },
        )

    return final_report
