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
    CONTENT_CONTRACT_SCHEMA_VERSION,
    RETIRED_WIKI_ROOT,
    TECHNICAL_WIKI_ROOT,
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
READER_STATS_PATH = WIKI_DIR / "10_Archiv" / "Wiki_Statistiken.md"
TRACKING_REGISTER_PATH = REPO_ROOT / "Logs" / "INGESTION_TRACKING_REGISTER.md"

ROAMLINK_WARNING_RE = re.compile(
    r"RoamLinksPlugin unable to find (?P<target>.+?) in directory (?P<directory>.+)$"
)
WARNING_LINE_RE = re.compile(r"^WARNING -\s+(?P<message>.+)$")
WIKILINK_RE = re.compile(r"\[{2,}([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]{2,}")
DOCS_LINK_INDEX_CACHE_VERSION = 1
CANONICAL_NAME_INDEX_CACHE_VERSION = 1
TREE_DRIFT_CACHE_VERSION = 2
NORMALIZE_TRANSLATION = str.maketrans({
    "ä": "ae",
    "ö": "oe",
    "ü": "ue",
    "ß": "ss",
    "Ä": "ae",
    "Ö": "oe",
    "Ü": "ue",
})
GENERIC_UNRESOLVED_TARGETS = {
    "geist",
    "index",
    "magie",
    "persoenlichkeiten",
    "wikilink",
    "wikilinks",
}
HUMAN_DECISION_OWNERS = {"human", "maintainer", "coordinator"}


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


def classify_unresolved_target(entry: dict, policy_entry: dict | None) -> str:
    target_norm = str(entry.get("normalized_target", ""))
    candidates = [candidate for candidate in entry.get("canonical_candidates", []) if candidate]
    owner = str((policy_entry or {}).get("owner", "")).strip().lower()

    if target_norm in GENERIC_UNRESOLVED_TARGETS:
        return "generic_term_conflict"
    if owner in HUMAN_DECISION_OWNERS:
        return "needs_human"
    if len(candidates) == 1:
        candidate = candidates[0]
        if normalize_key(str(entry.get("target", ""))) == normalize_key(candidate):
            return "safe_exact_match"
        return "safe_alias_match"
    return "needs_historian"


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


def policy_expiry_summary(policy: dict | None = None) -> dict:
    """Return expired policy entries so temporary exceptions cannot live forever."""
    policy = policy or load_pages_link_policy()
    today = datetime.now(timezone.utc).date()
    expired_targets: list[str] = []
    invalid_targets: list[str] = []
    for entry in policy.get("entries", []):
        target = str(entry.get("target", "")).strip()
        raw_review_until = str(entry.get("review_until", "")).strip()
        if not target or not raw_review_until:
            invalid_targets.append(target or "<missing-target>")
            continue
        try:
            if datetime.strptime(raw_review_until, "%Y-%m-%d").date() < today:
                expired_targets.append(target)
        except ValueError:
            invalid_targets.append(target)
    return {
        "status": "PASS" if not expired_targets and not invalid_targets else "FAIL",
        "expired_total": len(expired_targets),
        "expired_targets": expired_targets,
        "invalid_total": len(invalid_targets),
        "invalid_targets": invalid_targets,
    }


def collect_link_ratchet(
    unresolved_total: int | None,
    unallowlisted_total: int | None,
    *,
    policy: dict | None = None,
) -> dict:
    """Compare the current legacy-link backlog with the accepted ceiling."""
    policy = policy or load_pages_link_policy()
    baseline = policy.get("ratchet", {})
    unresolved_max = baseline.get("unresolved_max")
    unallowlisted_max = baseline.get("unallowlisted_max")
    expiry = policy_expiry_summary(policy)
    reasons: list[str] = []

    if unresolved_max is None or unallowlisted_max is None:
        reasons.append("link ratchet baseline missing")
    if unresolved_total is not None and unresolved_max is not None and unresolved_total > int(unresolved_max):
        reasons.append(f"unresolved links increased: {unresolved_total} > {unresolved_max}")
    if (
        unallowlisted_total is not None
        and unallowlisted_max is not None
        and unallowlisted_total > int(unallowlisted_max)
    ):
        reasons.append(f"unallowlisted links increased: {unallowlisted_total} > {unallowlisted_max}")
    if expiry["status"] == "FAIL":
        reasons.append("link policy contains expired or invalid review dates")

    if reasons:
        status = "FAIL"
    elif unresolved_total is None or unallowlisted_total is None:
        status = "UNKNOWN"
    else:
        status = "PASS"
    return {
        "status": status,
        "baseline": {
            "unresolved_max": unresolved_max,
            "unallowlisted_max": unallowlisted_max,
        },
        "actual": {
            "unresolved_total": unresolved_total,
            "unallowlisted_total": unallowlisted_total,
        },
        "policy_expiry": expiry,
        "reasons": reasons,
    }


def _first_int(raw: str, pattern: str) -> int | None:
    match = re.search(pattern, raw, flags=re.MULTILINE)
    return int(match.group(1)) if match else None


def collect_publication_freshness() -> dict:
    """Check that reader-facing statistics match the current publishing tree."""
    expected_articles = sum(
        1
        for path in WIKI_DIR.rglob("*.md")
        if path.name != READER_STATS_PATH.name
    ) if WIKI_DIR.exists() else 0
    stats_raw = READER_STATS_PATH.read_text(encoding="utf-8") if READER_STATS_PATH.exists() else ""
    register_raw = TRACKING_REGISTER_PATH.read_text(encoding="utf-8") if TRACKING_REGISTER_PATH.exists() else ""

    published_articles = _first_int(stats_raw, r"^\| Artikel \| \*\*(\d+)\*\* \|$")
    published_tracking_total = _first_int(
        stats_raw,
        r"^\| Ingestion Tracking vollstaendig \| \d+/(\d+) \|",
    )
    register_tracking_total = _first_int(register_raw, r"^- Reports gesamt: (\d+)$")
    reasons: list[str] = []
    if published_articles != expected_articles:
        reasons.append(
            f"reader stats article count is stale: {published_articles} != {expected_articles}"
        )
    if published_tracking_total != register_tracking_total:
        reasons.append(
            "reader stats ingestion total differs from the tracking register: "
            f"{published_tracking_total} != {register_tracking_total}"
        )
    return {
        "status": "FAIL" if reasons else "PASS",
        "expected_articles": expected_articles,
        "published_articles": published_articles,
        "tracking_register_total": register_tracking_total,
        "published_tracking_total": published_tracking_total,
        "stats_page": str(READER_STATS_PATH.relative_to(REPO_ROOT)),
        "tracking_register": str(TRACKING_REGISTER_PATH.relative_to(REPO_ROOT)),
        "sync_command": "./7w_wiki.py stats",
        "reasons": reasons,
    }


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


def legacy_root_status() -> dict:
    retired_files = sorted(RETIRED_WIKI_ROOT.rglob("*.md")) if RETIRED_WIKI_ROOT.exists() else []
    status = "present" if retired_files else "removed"
    return {
        "legacy_wiki_root": None,
        "legacy_root_status": status,
        "unexpected_files": [str(path.relative_to(REPO_ROOT)) for path in retired_files[:20]],
    }


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
    retired_all = sorted(RETIRED_WIKI_ROOT.rglob("*.md")) if RETIRED_WIKI_ROOT.exists() else []
    inputs_fingerprint = fingerprint_paths(
        docs_all + retired_all + _pages_runtime_paths(config),
        extra={
            "cache": "tree_drift",
            "version": TREE_DRIFT_CACHE_VERSION,
            "content_contract_schema_version": CONTENT_CONTRACT_SCHEMA_VERSION,
            "technical_root": str(TECHNICAL_WIKI_ROOT.relative_to(REPO_ROOT)),
            "retired_root": str(RETIRED_WIKI_ROOT.relative_to(REPO_ROOT)),
            "retired_root_strategy": "removed",
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

    retired_files = (
        {
            path.relative_to(RETIRED_WIKI_ROOT): path
            for path in RETIRED_WIKI_ROOT.rglob("*.md")
        }
        if RETIRED_WIKI_ROOT.exists()
        else {}
    )

    docs_only: list[str] = []
    legacy_only = sorted(str(path) for path in retired_files.keys())
    content_mismatches: list[str] = []
    drift_status = "FAIL" if legacy_only else "PASS"

    result = {
        "status": drift_status,
        "legacy_root_status": "present" if legacy_only else "removed",
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


def collect_pages_contract_report(config: str = "mkdocs.yml") -> dict:
    started_total = time.perf_counter()
    config_path = REPO_ROOT / config
    snapshot = load_pages_health_snapshot()
    drift, drift_meta = collect_tree_drift(config=config, return_meta=True)
    _, link_meta = build_docs_link_index(config=config, return_meta=True)
    _, canonical_meta = build_canonical_name_index(config=config, return_meta=True)
    root_state = legacy_root_status()
    publication_freshness = collect_publication_freshness()

    pages_health = dict(snapshot.get("pages_health", {})) if snapshot else {}
    pages_health["canonical_wiki_root"] = str(TECHNICAL_WIKI_ROOT.relative_to(REPO_ROOT))
    pages_health["legacy_wiki_root"] = root_state["legacy_wiki_root"]
    pages_health["legacy_root_status"] = root_state["legacy_root_status"]
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
    pages_health["snapshot_based"] = bool(snapshot)
    pages_health["snapshot_written"] = False
    pages_health["publication_freshness"] = publication_freshness
    pages_health["link_ratchet"] = collect_link_ratchet(
        pages_health.get("unresolved_total") if snapshot else None,
        pages_health.get("unallowlisted_total") if snapshot else None,
    )
    pages_health.setdefault("targets", [])
    pages_health.setdefault("other_warnings", [])
    pages_health.setdefault(
        "classification_counts",
        {
            "safe_exact_match": 0,
            "safe_alias_match": 0,
            "generic_term_conflict": 0,
            "needs_historian": 0,
            "needs_human": 0,
        },
    )
    pages_health["other_warnings"] = list(dict.fromkeys([
        *pages_health["other_warnings"],
        *(
            []
            if snapshot
            else ["Contract mode uses static config and cached analysis only; unresolved-target counts come from the last snapshot when available."]
        ),
    ]))

    static_failures: list[str] = []
    if not config_path.exists():
        static_failures.append("mkdocs config missing")
    if not DOCS_DIR.exists():
        static_failures.append("docs dir missing")
    if drift["status"] == "FAIL":
        static_failures.append("retired root tree unexpectedly present")
    if publication_freshness["status"] == "FAIL":
        static_failures.extend(publication_freshness["reasons"])
    if pages_health["link_ratchet"]["status"] == "FAIL":
        static_failures.extend(pages_health["link_ratchet"]["reasons"])

    if static_failures:
        status = "FAIL"
    elif snapshot:
        has_advisory_backlog = bool(
            pages_health.get("targets")
            or pages_health.get("other_warnings")
            or int(pages_health.get("unallowlisted_total", 0) or 0) > 0
        )
        status = "WARN" if has_advisory_backlog else "PASS"
    else:
        status = "PASS"
    pages_health["status"] = status

    return {
        "generated_at": now_iso(),
        "config": config,
        "mode": "contract",
        "advisory_only": True,
        "status": status,
        "checks": [],
        "build": {
            "skipped": True,
            "reason": "contract_validation_static_only",
            "config_exists": config_path.exists(),
            "docs_dir_exists": DOCS_DIR.exists(),
            "timing_ms": {
                "total": round((time.perf_counter() - started_total) * 1000, 2),
            },
        },
        "pages_health": pages_health,
        "drift_health": {
            "mode": "static_only",
            "unexpected_legacy_files": root_state["unexpected_files"],
        },
    }


def collect_pages_build_report(config: str = "mkdocs.yml", no_clean: bool = False, *, fast: bool = False) -> dict:
    started_total = time.perf_counter()
    publication_freshness = collect_publication_freshness()
    if fast:
        snapshot = load_pages_health_snapshot()
        drift, drift_meta = collect_tree_drift(config=config, return_meta=True)
        _, link_meta = build_docs_link_index(config=config, return_meta=True)
        _, canonical_meta = build_canonical_name_index(config=config, return_meta=True)
        root_state = legacy_root_status()
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
                    "legacy_wiki_root": root_state["legacy_wiki_root"],
                    "legacy_root_status": root_state["legacy_root_status"],
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
        pages_health["legacy_wiki_root"] = root_state["legacy_wiki_root"]
        pages_health["legacy_root_status"] = root_state["legacy_root_status"]
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
        pages_health["publication_freshness"] = publication_freshness
        pages_health["link_ratchet"] = collect_link_ratchet(
            pages_health.get("unresolved_total"),
            pages_health.get("unallowlisted_total"),
        )
        pages_health["status"] = (
            "FAIL"
            if drift["status"] == "FAIL"
            or publication_freshness["status"] == "FAIL"
            or pages_health["link_ratchet"]["status"] == "FAIL"
            else pages_health.get("status", "UNKNOWN")
        )
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
        root_state = legacy_root_status()
        return {
            "generated_at": now_iso(),
            "status": "FAIL",
            "build": {"exit_code": 1, "mkdocs_source": None},
            "pages_health": {
                "status": "FAIL",
                "canonical_wiki_root": str(TECHNICAL_WIKI_ROOT.relative_to(REPO_ROOT)),
                "legacy_wiki_root": root_state["legacy_wiki_root"],
                "legacy_root_status": root_state["legacy_root_status"],
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
    classification_counts: dict[str, int] = {
        "safe_exact_match": 0,
        "safe_alias_match": 0,
        "generic_term_conflict": 0,
        "needs_historian": 0,
        "needs_human": 0,
    }
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
        classification = classify_unresolved_target(entry, policy_entry)
        classification_counts[classification] += entry["count"]
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
                "classification": classification,
            }
        )
    target_grouping_duration_ms = round((time.perf_counter() - grouping_started) * 1000, 2)

    link_ratchet = collect_link_ratchet(
        sum(item["count"] for item in targets),
        unallowlisted_total,
    )

    pages_status = "PASS"
    if proc.returncode != 0:
        pages_status = "FAIL"
    elif targets or other_warnings:
        pages_status = "WARN"
    drift, drift_meta = collect_tree_drift(config=config, return_meta=True)
    root_state = legacy_root_status()
    if drift["status"] == "FAIL":
        pages_status = "FAIL"
    elif drift["status"] == "WARN" and pages_status == "PASS":
        pages_status = "WARN"
    if publication_freshness["status"] == "FAIL" or link_ratchet["status"] == "FAIL":
        pages_status = "FAIL"

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
            "legacy_wiki_root": root_state["legacy_wiki_root"],
            "legacy_root_status": root_state["legacy_root_status"],
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
            "publication_freshness": publication_freshness,
            "link_ratchet": link_ratchet,
            "classification_counts": classification_counts,
            "targets": targets,
            "other_warnings": other_warnings,
        },
    }
