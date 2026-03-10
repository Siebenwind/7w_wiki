#!/usr/bin/env python3
"""
Shared helpers for Pages / Roamlinks integrity diagnostics.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = REPO_ROOT / "docs"
WIKI_DIR = REPO_ROOT / "Siebenwind_Wiki"
PAGES_POLICY_PATH = REPO_ROOT / ".agent" / "config" / "pages_link_policy.json"
PAGES_HEALTH_PATH = REPO_ROOT / ".agent" / "data" / "pages_health.json"
VENV_MKDOCS = REPO_ROOT / ".venv" / "bin" / "mkdocs"

ROAMLINK_WARNING_RE = re.compile(
    r"RoamLinksPlugin unable to find (?P<target>.+?) in directory (?P<directory>.+)$"
)
WARNING_LINE_RE = re.compile(r"^WARNING -\s+(?P<message>.+)$")
WIKILINK_RE = re.compile(r"\[{2,}([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]{2,}")


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_key(value: str) -> str:
    return value.lower().replace("_", "").replace(" ", "").replace("-", "").replace("'", "")


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


def build_docs_link_index() -> dict[str, set[str]]:
    index: dict[str, set[str]] = {}
    for file_path in _iter_docs_markdown_files():
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
    return index


def build_canonical_name_index() -> dict[str, list[str]]:
    mapping: dict[str, set[str]] = {}
    search_roots = [WIKI_DIR, DOCS_DIR / "Siebenwind_Wiki"]
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
    return {key: sorted(values) for key, values in mapping.items()}


def collect_pages_build_report(config: str = "mkdocs.yml", no_clean: bool = False) -> dict:
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
    proc = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

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

    link_index = build_docs_link_index()
    canonical_index = build_canonical_name_index()
    policy_map = policy_entry_map()

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

    pages_status = "PASS"
    if proc.returncode != 0:
        pages_status = "FAIL"
    elif targets or other_warnings:
        pages_status = "WARN"

    stdout_preview = "\n".join(proc.stdout.splitlines()[:20])
    stderr_preview = "\n".join(proc.stderr.splitlines()[:20])

    return {
        "generated_at": now_iso(),
        "config": config,
        "build": {
            "command": cmd,
            "exit_code": proc.returncode,
            "mkdocs_source": mkdocs_source,
            "stdout_preview": stdout_preview,
            "stderr_preview": stderr_preview,
            "warning_count": len(raw_targets) + len(other_warnings),
        },
        "pages_health": {
            "status": pages_status,
            "unresolved_total": sum(item["count"] for item in targets),
            "allowlisted_total": allowlisted_total,
            "planned_fix_total": planned_fix_total,
            "unallowlisted_total": unallowlisted_total,
            "targets": targets,
            "other_warnings": other_warnings,
        },
    }
