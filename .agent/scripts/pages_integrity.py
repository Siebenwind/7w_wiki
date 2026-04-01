#!/usr/bin/env python3
"""
Shared helpers for Pages / Roamlinks integrity diagnostics.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from content_contract import (
    ALLOWED_LEGACY_ARTIFACTS,
    CONTENT_CONTRACT_SCHEMA_VERSION,
    LEGACY_WIKI_ROOT,
    TECHNICAL_WIKI_ROOT,
    content_hash,
    fingerprint_paths,
    load_analysis_cache,
    now_iso,
    write_analysis_cache,
)

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = REPO_ROOT / "docs"
WIKI_DIR = TECHNICAL_WIKI_ROOT
PAGES_POLICY_PATH = REPO_ROOT / ".agent" / "config" / "pages_link_policy.json"
PAGES_HEALTH_PATH = REPO_ROOT / ".agent" / "data" / "pages_health.json"
VENV_MKDOCS = REPO_ROOT / ".venv" / "bin" / "mkdocs"

ROAMLINK_WARNING_RE = re.compile(
    r"RoamLinksPlugin unable to find (?P<target>.+?) in directory (?P<directory>.+)$"
)
WARNING_LINE_RE = re.compile(r"^WARNING -\s+(?P<message>.+)$")
WIKILINK_RE = re.compile(r"\[{2,}([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]{2,}")
DOCS_LINK_INDEX_CACHE_VERSION = 1
CANONICAL_NAME_INDEX_CACHE_VERSION = 1
TREE_DRIFT_CACHE_VERSION = 1
NORMALIZE_TRANSLATION = str.maketrans({
    "ä": "ae",
    "ö": "oe",
    "ü": "ue",
    "ß": "ss",
    "Ä": "ae",
    "Ö": "oe",
    "Ü": "ue",
})


def normalize_key(value: str) -> str:
    normalized = value.translate(NORMALIZE_TRANSLATION).lower()
    return re.sub(r"[^a-z0-9]", "", normalized)


def parse_frontmatter(raw: str) -> dict[str, str]:
    if not raw.startswith("---\n"):
        return {}
    end = raw.find("\n---\n", 4)
    if end == -1:
        return {}
    meta: dict[str, str] = {}
    for line in raw[4:end].splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        meta[key.strip()] = value.strip()
    return meta


def get_mkdocs_base_cmd() -> tuple[list[str] | None, str | None]:
    if VENV_MKDOCS.exists():
        return [str(VENV_MKDOCS)], str(VENV_MKDOCS)
    system_mkdocs = shutil.which("mkdocs")
    if system_mkdocs:
        return [system_mkdocs], system_mkdocs
    return None, None


def load_pages_link_policy() -> dict:
    if not PAGES_POLICY_PATH.exists():
        return {"version": 1, "updated_at": now_iso(), "entries": []}
    try:
        return json.loads(PAGES_POLICY_PATH.read_text(encoding="utf-8"))
    except Exception:
        return {"version": 1, "updated_at": now_iso(), "entries": []}


def policy_entry_map() -> dict[str, dict]:
    entries = load_pages_link_policy().get("entries", [])
    mapped: dict[str, dict] = {}
    for entry in entries:
        target = str(entry.get("target", "")).strip()
        if not target:
            continue
        mapped[normalize_key(target)] = entry
    return mapped


def load_pages_health_snapshot() -> dict | None:
    if not PAGES_HEALTH_PATH.exists():
        return None
    try:
        return json.loads(PAGES_HEALTH_PATH.read_text(encoding="utf-8"))
    except Exception:
        return None


def write_pages_health_snapshot(snapshot: dict) -> None:
    PAGES_HEALTH_PATH.parent.mkdir(parents=True, exist_ok=True)
    PAGES_HEALTH_PATH.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _iter_docs_markdown_files() -> list[Path]:
    if not DOCS_DIR.exists():
        return []
    return sorted(DOCS_DIR.rglob("*.md"))


def _cache_descriptor(name: str) -> dict:
    return {
        "path": f".agent/data/cache/{name}.json",
        "name": name,
    }


def _pages_runtime_paths(config: str = "mkdocs.yml") -> list[Path]:
    paths = [REPO_ROOT / config, PAGES_POLICY_PATH]
    if VENV_MKDOCS.exists():
        paths.append(VENV_MKDOCS)
    return [path for path in paths if path.exists()]


def build_docs_link_index(use_cache: bool = True, *, config: str = "mkdocs.yml", return_meta: bool = False):
    started = time.perf_counter()
    files = _iter_docs_markdown_files()
    inputs_fingerprint = fingerprint_paths(
        files + _pages_runtime_paths(config),
        extra={
            "cache": "docs_link_index",
            "version": DOCS_LINK_INDEX_CACHE_VERSION,
            "content_contract_schema_version": CONTENT_CONTRACT_SCHEMA_VERSION,
            "docs_dir": str(DOCS_DIR.relative_to(REPO_ROOT)),
        },
    )
    if use_cache:
        cached = load_analysis_cache(
            "docs_link_index",
            version=DOCS_LINK_INDEX_CACHE_VERSION,
            inputs_fingerprint=inputs_fingerprint,
        )
        if cached:
            payload = cached.get("payload", {})
            result = {key: set(values) for key, values in payload.get("index", {}).items()}
            meta = {
                **_cache_descriptor("docs_link_index"),
                "version": DOCS_LINK_INDEX_CACHE_VERSION,
                "inputs_fingerprint": inputs_fingerprint,
                "hit": True,
                "duration_ms": round((time.perf_counter() - started) * 1000, 2),
            }
            return (result, meta) if return_meta else result

    index: dict[str, set[str]] = {}
    for file_path in files:
        try:
            raw = file_path.read_text(encoding="utf-8")
        except Exception:
            continue
        stripped = re.sub(r"```.*?```", "", raw, flags=re.DOTALL)
        stripped = re.sub(r"`.*?`", "", stripped)
        for target in WIKILINK_RE.findall(stripped):
            normalized = normalize_key(target.strip())
            if not normalized:
                continue
            index.setdefault(normalized, set()).add(str(file_path.relative_to(REPO_ROOT)))
    if use_cache:
        write_analysis_cache(
            "docs_link_index",
            version=DOCS_LINK_INDEX_CACHE_VERSION,
            inputs_fingerprint=inputs_fingerprint,
            payload={"index": {key: sorted(values) for key, values in sorted(index.items())}},
        )
    meta = {
        **_cache_descriptor("docs_link_index"),
        "version": DOCS_LINK_INDEX_CACHE_VERSION,
        "inputs_fingerprint": inputs_fingerprint,
        "hit": False,
        "duration_ms": round((time.perf_counter() - started) * 1000, 2),
    }
    return (index, meta) if return_meta else index


def build_canonical_name_index(use_cache: bool = True, *, config: str = "mkdocs.yml", return_meta: bool = False):
    started = time.perf_counter()
    mapping: dict[str, set[str]] = {}
    search_roots = [WIKI_DIR]
    files: list[Path] = []
    for root in search_roots:
        if root.exists():
            files.extend(sorted(root.rglob("*.md")))

    inputs_fingerprint = fingerprint_paths(
        files + _pages_runtime_paths(config),
        extra={
            "cache": "canonical_name_index",
            "version": CANONICAL_NAME_INDEX_CACHE_VERSION,
            "content_contract_schema_version": CONTENT_CONTRACT_SCHEMA_VERSION,
            "wiki_root": str(WIKI_DIR.relative_to(REPO_ROOT)),
        },
    )
    if use_cache:
        cached = load_analysis_cache(
            "canonical_name_index",
            version=CANONICAL_NAME_INDEX_CACHE_VERSION,
            inputs_fingerprint=inputs_fingerprint,
        )
        if cached:
            result = cached.get("payload", {}).get("index", {})
            meta = {
                **_cache_descriptor("canonical_name_index"),
                "version": CANONICAL_NAME_INDEX_CACHE_VERSION,
                "inputs_fingerprint": inputs_fingerprint,
                "hit": True,
                "duration_ms": round((time.perf_counter() - started) * 1000, 2),
            }
            return (result, meta) if return_meta else result

    for root in search_roots:
        if not root.exists():
            continue
        for file_path in root.rglob("*.md"):
            key = normalize_key(file_path.stem)
            mapping.setdefault(key, set()).add(file_path.stem)
            try:
                raw = file_path.read_text(encoding="utf-8")
            except Exception:
                continue
            meta = parse_frontmatter(raw[:4000])
            title = meta.get("title", "").strip().strip('"').strip("'")
            if title:
                mapping.setdefault(normalize_key(title), set()).add(file_path.stem)
            aliases_raw = meta.get("aliases", "")
            if aliases_raw.startswith("[") and aliases_raw.endswith("]"):
                aliases = [part.strip().strip('"').strip("'") for part in aliases_raw[1:-1].split(",")]
                for alias in aliases:
                    if alias:
                        mapping.setdefault(normalize_key(alias), set()).add(file_path.stem)
    result = {key: sorted(values) for key, values in mapping.items()}
    if use_cache:
        write_analysis_cache(
            "canonical_name_index",
            version=CANONICAL_NAME_INDEX_CACHE_VERSION,
            inputs_fingerprint=inputs_fingerprint,
            payload={"index": result},
        )
    meta = {
        **_cache_descriptor("canonical_name_index"),
        "version": CANONICAL_NAME_INDEX_CACHE_VERSION,
        "inputs_fingerprint": inputs_fingerprint,
        "hit": False,
        "duration_ms": round((time.perf_counter() - started) * 1000, 2),
    }
    return (result, meta) if return_meta else result


def collect_tree_drift(use_cache: bool = True, *, config: str = "mkdocs.yml", return_meta: bool = False):
    started = time.perf_counter()
    docs_all = sorted(TECHNICAL_WIKI_ROOT.rglob("*.md")) if TECHNICAL_WIKI_ROOT.exists() else []
    legacy_all = sorted(LEGACY_WIKI_ROOT.rglob("*.md")) if LEGACY_WIKI_ROOT.exists() else []
    inputs_fingerprint = fingerprint_paths(
        docs_all + legacy_all + _pages_runtime_paths(config),
        extra={
            "cache": "tree_drift",
            "version": TREE_DRIFT_CACHE_VERSION,
            "content_contract_schema_version": CONTENT_CONTRACT_SCHEMA_VERSION,
            "technical_root": str(TECHNICAL_WIKI_ROOT.relative_to(REPO_ROOT)),
            "legacy_root": str(LEGACY_WIKI_ROOT.relative_to(REPO_ROOT)),
            "allowed_legacy_artifacts": sorted(str(path) for path in ALLOWED_LEGACY_ARTIFACTS),
        },
    )
    if use_cache:
        cached = load_analysis_cache(
            "tree_drift",
            version=TREE_DRIFT_CACHE_VERSION,
            inputs_fingerprint=inputs_fingerprint,
        )
        if cached:
            result = cached.get("payload", {})
            meta = {
                **_cache_descriptor("tree_drift"),
                "version": TREE_DRIFT_CACHE_VERSION,
                "inputs_fingerprint": inputs_fingerprint,
                "hit": True,
                "duration_ms": round((time.perf_counter() - started) * 1000, 2),
            }
            return (result, meta) if return_meta else result

    docs_files = {
        path.relative_to(TECHNICAL_WIKI_ROOT): path
        for path in TECHNICAL_WIKI_ROOT.rglob("*.md")
    } if TECHNICAL_WIKI_ROOT.exists() else {}
    legacy_files = {
        path.relative_to(LEGACY_WIKI_ROOT): path
        for path in LEGACY_WIKI_ROOT.rglob("*.md")
        if path.relative_to(LEGACY_WIKI_ROOT) not in ALLOWED_LEGACY_ARTIFACTS
    } if LEGACY_WIKI_ROOT.exists() else {}

    docs_only = sorted(str(path) for path in docs_files.keys() - legacy_files.keys())
    legacy_only = sorted(str(path) for path in legacy_files.keys() - docs_files.keys())
    content_mismatches: list[str] = []

    for rel in sorted(docs_files.keys() & legacy_files.keys()):
        try:
            docs_hash = content_hash(docs_files[rel].read_text(encoding="utf-8"))
            legacy_hash = content_hash(legacy_files[rel].read_text(encoding="utf-8"))
        except Exception:
            continue
        if docs_hash != legacy_hash:
            content_mismatches.append(str(rel))

    drift_status = "FAIL" if legacy_only or content_mismatches else "PASS"

    result = {
        "status": drift_status,
        "docs_only_files": docs_only,
        "legacy_only_files": legacy_only,
        "content_mismatches": content_mismatches,
    }
    if use_cache:
        write_analysis_cache(
            "tree_drift",
            version=TREE_DRIFT_CACHE_VERSION,
            inputs_fingerprint=inputs_fingerprint,
            payload=result,
        )
    meta = {
        **_cache_descriptor("tree_drift"),
        "version": TREE_DRIFT_CACHE_VERSION,
        "inputs_fingerprint": inputs_fingerprint,
        "hit": False,
        "duration_ms": round((time.perf_counter() - started) * 1000, 2),
    }
    return (result, meta) if return_meta else result


def collect_pages_build_report(config: str = "mkdocs.yml", no_clean: bool = False, *, fast: bool = False) -> dict:
    started_total = time.perf_counter()
    if fast:
        snapshot = load_pages_health_snapshot()
        drift, drift_meta = collect_tree_drift(config=config, return_meta=True)
        _, link_meta = build_docs_link_index(config=config, return_meta=True)
        _, canonical_meta = build_canonical_name_index(config=config, return_meta=True)
        if not snapshot:
            return {
                "generated_at": now_iso(),
                "mode": "fast",
                "advisory_only": True,
                "status": "FAIL",
                "build": {
                    "skipped": True,
                    "reason": "fast_precheck_requires_existing_pages_snapshot",
                    "timing_ms": {"total": round((time.perf_counter() - started_total) * 1000, 2)},
                },
                "pages_health": {
                    "status": "FAIL",
                    "canonical_wiki_root": str(TECHNICAL_WIKI_ROOT.relative_to(REPO_ROOT)),
                    "legacy_wiki_root": str(LEGACY_WIKI_ROOT.relative_to(REPO_ROOT)),
                    "analysis_cache": {
                        "docs_link_index": link_meta,
                        "canonical_name_index": canonical_meta,
                        "tree_drift": drift_meta,
                    },
                    "drift_status": drift["status"],
                    "drift_counts": {
                        "docs_only_files": len(drift["docs_only_files"]),
                        "legacy_only_files": len(drift["legacy_only_files"]),
                        "content_mismatches": len(drift["content_mismatches"]),
                    },
                    "unresolved_total": 0,
                    "allowlisted_total": 0,
                    "planned_fix_total": 0,
                    "unallowlisted_total": 0,
                    "targets": [],
                    "other_warnings": ["fast precheck requires an existing pages snapshot"],
                    "snapshot_based": False,
                },
            }

        pages_health = dict(snapshot.get("pages_health", {}))
        pages_health["canonical_wiki_root"] = str(TECHNICAL_WIKI_ROOT.relative_to(REPO_ROOT))
        pages_health["legacy_wiki_root"] = str(LEGACY_WIKI_ROOT.relative_to(REPO_ROOT))
        pages_health["drift_status"] = drift["status"]
        pages_health["drift_counts"] = {
            "docs_only_files": len(drift["docs_only_files"]),
            "legacy_only_files": len(drift["legacy_only_files"]),
            "content_mismatches": len(drift["content_mismatches"]),
        }
        pages_health["drift_examples"] = {
            "docs_only_files": drift["docs_only_files"][:20],
            "legacy_only_files": drift["legacy_only_files"][:20],
            "content_mismatches": drift["content_mismatches"][:20],
        }
        pages_health["analysis_cache"] = {
            "docs_link_index": link_meta,
            "canonical_name_index": canonical_meta,
            "tree_drift": drift_meta,
        }
        pages_health["snapshot_based"] = True
        pages_health["status"] = "FAIL" if drift["status"] == "FAIL" else pages_health.get("status", "UNKNOWN")
        pages_health.setdefault("other_warnings", [])
        pages_health["other_warnings"] = list(pages_health["other_warnings"]) + [
            "Fast precheck uses cached analyses and the latest Pages snapshot; run full validate for a hard gate."
        ]
        return {
            "generated_at": now_iso(),
            "config": config,
            "mode": "fast",
            "advisory_only": True,
            "status": pages_health["status"],
            "build": {
                "skipped": True,
                "reason": "fast_precheck_uses_snapshot_and_cached_analysis",
                "timing_ms": {"total": round((time.perf_counter() - started_total) * 1000, 2)},
            },
            "pages_health": pages_health,
        }

    mkdocs_cmd, mkdocs_source = get_mkdocs_base_cmd()
    if not mkdocs_cmd:
        return {
            "generated_at": now_iso(),
            "status": "FAIL",
            "build": {"exit_code": 1, "mkdocs_source": None},
            "pages_health": {
                "status": "FAIL",
                "unresolved_total": 0,
                "allowlisted_total": 0,
                "planned_fix_total": 0,
                "unallowlisted_total": 0,
                "targets": [],
                "other_warnings": ["mkdocs not installed"],
            },
        }

    config_path = REPO_ROOT / config
    cmd = mkdocs_cmd + ["build", "-f", str(config_path)]
    if not no_clean:
        cmd.append("--clean")
    build_started = time.perf_counter()
    proc = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    build_duration_ms = round((time.perf_counter() - build_started) * 1000, 2)

    parse_started = time.perf_counter()
    combined_output = "\n".join(part for part in [proc.stdout, proc.stderr] if part)
    other_warnings: list[str] = []
    raw_targets: list[str] = []

    for line in combined_output.splitlines():
        warning_match = WARNING_LINE_RE.match(line.strip())
        if not warning_match:
            continue
        message = warning_match.group("message")
        roam_match = ROAMLINK_WARNING_RE.search(message)
        if roam_match:
            raw_targets.append(roam_match.group("target").strip())
        else:
            other_warnings.append(message)
    warning_parse_duration_ms = round((time.perf_counter() - parse_started) * 1000, 2)

    policy_started = time.perf_counter()
    policy_map = policy_entry_map()
    policy_duration_ms = round((time.perf_counter() - policy_started) * 1000, 2)
    link_index, link_meta = build_docs_link_index(config=config, return_meta=True)
    canonical_index, canonical_meta = build_canonical_name_index(config=config, return_meta=True)

    grouping_started = time.perf_counter()
    grouped: dict[str, dict] = {}
    for target in raw_targets:
        key = normalize_key(target)
        entry = grouped.setdefault(
            key,
            {
                "target": target,
                "normalized_target": key,
                "count": 0,
                "source_pages": [],
                "canonical_candidates": canonical_index.get(key, []),
            },
        )
        entry["count"] += 1
        entry["source_pages"] = sorted(link_index.get(key, set()))[:10]

    targets: list[dict] = []
    allowlisted_total = 0
    planned_fix_total = 0
    unallowlisted_total = 0
    for key, entry in sorted(grouped.items(), key=lambda item: (-item[1]["count"], item[1]["target"].lower())):
        policy_entry = policy_map.get(key)
        policy_status = "untracked"
        if policy_entry:
            policy_status = str(policy_entry.get("status", "untracked"))
        if policy_status == "allowlisted":
            allowlisted_total += entry["count"]
        elif policy_status == "planned_fix":
            planned_fix_total += entry["count"]
            unallowlisted_total += entry["count"]
        else:
            unallowlisted_total += entry["count"]
        targets.append(
            {
                "target": entry["target"],
                "normalized_target": entry["normalized_target"],
                "count": entry["count"],
                "source_pages": entry["source_pages"],
                "canonical_candidates": entry["canonical_candidates"],
                "policy_status": policy_status,
                "reason": None if not policy_entry else policy_entry.get("reason"),
                "owner": None if not policy_entry else policy_entry.get("owner"),
                "review_until": None if not policy_entry else policy_entry.get("review_until"),
                "replacement_hint": None if not policy_entry else policy_entry.get("replacement_hint"),
                "scope": None if not policy_entry else policy_entry.get("scope"),
            }
        )
    target_grouping_duration_ms = round((time.perf_counter() - grouping_started) * 1000, 2)

    pages_status = "PASS"
    if proc.returncode != 0:
        pages_status = "FAIL"
    elif targets or other_warnings:
        pages_status = "WARN"
    drift, drift_meta = collect_tree_drift(config=config, return_meta=True)
    if drift["status"] == "FAIL":
        pages_status = "FAIL"
    elif drift["status"] == "WARN" and pages_status == "PASS":
        pages_status = "WARN"

    stdout_preview = "\n".join(proc.stdout.splitlines()[:20])
    stderr_preview = "\n".join(proc.stderr.splitlines()[:20])

    return {
        "generated_at": now_iso(),
        "config": config,
        "mode": "full",
        "advisory_only": False,
        "build": {
            "command": cmd,
            "exit_code": proc.returncode,
            "mkdocs_source": mkdocs_source,
            "stdout_preview": stdout_preview,
            "stderr_preview": stderr_preview,
            "warning_count": len(raw_targets) + len(other_warnings),
            "timing_ms": {
                "mkdocs_build": build_duration_ms,
                "warning_parse": warning_parse_duration_ms,
                "policy_load": policy_duration_ms,
                "target_grouping": target_grouping_duration_ms,
                "total": round((time.perf_counter() - started_total) * 1000, 2),
            },
        },
        "pages_health": {
            "status": pages_status,
            "canonical_wiki_root": str(TECHNICAL_WIKI_ROOT.relative_to(REPO_ROOT)),
            "legacy_wiki_root": str(LEGACY_WIKI_ROOT.relative_to(REPO_ROOT)),
            "analysis_cache": {
                "docs_link_index": link_meta,
                "canonical_name_index": canonical_meta,
                "tree_drift": drift_meta,
            },
            "drift_status": drift["status"],
            "drift_counts": {
                "docs_only_files": len(drift["docs_only_files"]),
                "legacy_only_files": len(drift["legacy_only_files"]),
                "content_mismatches": len(drift["content_mismatches"]),
            },
            "drift_examples": {
                "docs_only_files": drift["docs_only_files"][:20],
                "legacy_only_files": drift["legacy_only_files"][:20],
                "content_mismatches": drift["content_mismatches"][:20],
            },
            "unresolved_total": sum(item["count"] for item in targets),
            "allowlisted_total": allowlisted_total,
            "planned_fix_total": planned_fix_total,
            "unallowlisted_total": unallowlisted_total,
            "targets": targets,
            "other_warnings": other_warnings,
        },
    }
