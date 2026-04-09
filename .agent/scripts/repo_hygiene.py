#!/usr/bin/env python3
"""
Classify hot/cold/runtime/build path families and optionally apply conservative
cleanup actions.

This tool is intentionally conservative:
- canonical-hot paths are reported but never modified
- versioned-cold evidence is rotated into explicit cold buckets
- local runtime/build trees are pruned only when explicitly requested
"""
from __future__ import annotations

import argparse
import json
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DATA_COLD_ROOT = REPO_ROOT / ".agent" / "data" / "cold"
ARCHIVE_COLD_ROOT = REPO_ROOT / "Logs" / "Archive" / "cold"
RETENTION_LIMIT = 5
SAMPLE_LIMIT = 20


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class FamilyRule:
    id: str
    root: Path
    pattern: str
    classification: str
    reason: str
    action: str
    cold_root: Path | None = None
    keep_latest: int | None = None
    skip_suffixes: tuple[str, ...] = ()
    skip_names: tuple[str, ...] = ()


def _family_period(path: Path) -> str:
    stamp = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc)
    return stamp.strftime("%Y-%m")


def _load_index(index_path: Path) -> dict:
    if not index_path.exists():
        return {"generated_at": now_iso(), "entries": []}
    try:
        return json.loads(index_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {"generated_at": now_iso(), "entries": []}


def _write_index(index_path: Path, payload: dict) -> None:
    payload["generated_at"] = now_iso()
    index_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _iter_matching_paths(rule: FamilyRule) -> list[Path]:
    matched: list[Path] = []
    for path in sorted(rule.root.glob(rule.pattern)):
        if rule.action == "move_to_cold" and not path.is_file():
            continue
        if path.name in rule.skip_names:
            continue
        if any(path.name.endswith(suffix) for suffix in rule.skip_suffixes):
            continue
        matched.append(path)
    return matched


def _build_cold_destination(rule: FamilyRule, path: Path) -> Path:
    assert rule.cold_root is not None
    target_dir = rule.cold_root / rule.id / _family_period(path)
    target_dir.mkdir(parents=True, exist_ok=True)
    return target_dir / path.name


def classify_rule(rule: FamilyRule) -> dict:
    matched = _iter_matching_paths(rule)
    if rule.action == "move_to_cold":
        keep_latest = rule.keep_latest or len(matched)
        hot_kept = [str(path.relative_to(REPO_ROOT)) for path in matched[-keep_latest:]]
        cold_candidates = [str(path.relative_to(REPO_ROOT)) for path in matched[:-keep_latest]]
    elif rule.action == "refuse":
        keep_latest = None
        hot_kept = [str(path.relative_to(REPO_ROOT)) for path in matched[:SAMPLE_LIMIT]]
        cold_candidates = []
    else:
        keep_latest = None
        hot_kept = []
        cold_candidates = [str(path.relative_to(REPO_ROOT)) for path in matched[:SAMPLE_LIMIT]]
    return {
        "id": rule.id,
        "classification": rule.classification,
        "reason": rule.reason,
        "action": rule.action,
        "keep_latest": rule.keep_latest,
        "matched_count": len(matched),
        "hot_retained_count": len(hot_kept),
        "cold_candidate_count": len(cold_candidates),
        "hot_retained": hot_kept,
        "cold_candidates": cold_candidates,
        "truncated_hot_retained": max(0, len(matched) - len(hot_kept)) if rule.action == "refuse" else 0,
        "truncated_cold_candidates": max(0, len(matched[:-keep_latest]) - len(cold_candidates)) if rule.action == "move_to_cold" else 0,
    }


def apply_rule(rule: FamilyRule) -> dict:
    matched = _iter_matching_paths(rule)
    keep_latest = rule.keep_latest or len(matched)
    moved: list[str] = []
    deleted: list[str] = []

    if rule.action == "move_to_cold":
        if rule.cold_root is None:
            raise RuntimeError(f"{rule.id}: cold_root missing")
        for path in matched[:-keep_latest]:
            destination = _build_cold_destination(rule, path)
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(destination))
            index_path = destination.parent / "index.json"
            index_payload = _load_index(index_path)
            index_payload.setdefault("entries", []).append(
                {
                    "archived_at": now_iso(),
                    "original_path": str(path.relative_to(REPO_ROOT)),
                    "cold_path": str(destination.relative_to(REPO_ROOT)),
                    "family": rule.id,
                }
            )
            _write_index(index_path, index_payload)
            moved.append(str(destination.relative_to(REPO_ROOT)))
    elif rule.action == "prune_runtime_tree":
        for path in matched:
            if path.is_dir():
                shutil.rmtree(path)
            elif path.exists():
                path.unlink()
            deleted.append(str(path.relative_to(REPO_ROOT)))
    elif rule.action == "refuse":
        return {"id": rule.id, "status": "protected", "moved": [], "deleted": []}
    else:
        raise RuntimeError(f"{rule.id}: unsupported action {rule.action}")

    return {"id": rule.id, "status": "applied", "moved": moved, "deleted": deleted}


def rules() -> list[FamilyRule]:
    return [
        FamilyRule(
            id="canonical_core",
            root=REPO_ROOT,
            pattern=".agent/catalog/*.json",
            classification="canonical_hot",
            reason="Canonical discovery metadata is live repo truth.",
            action="refuse",
        ),
        FamilyRule(
            id="technical_wiki_tree",
            root=REPO_ROOT,
            pattern="docs/Siebenwind_Wiki/**/*.md",
            classification="canonical_hot",
            reason="The docs/Siebenwind_Wiki tree is the canonical technical edit/publish tree.",
            action="refuse",
        ),
        FamilyRule(
            id="review_snapshots",
            root=REPO_ROOT / ".agent" / "data",
            pattern="REVIEW_SNAPSHOT_*.json",
            classification="versioned_cold",
            reason="Raw review snapshots are forensic evidence; only the freshest set should stay hot.",
            action="move_to_cold",
            cold_root=DATA_COLD_ROOT,
            keep_latest=RETENTION_LIMIT,
            skip_names=("REVIEW_SNAPSHOT_latest.json",),
        ),
        FamilyRule(
            id="scout_snapshots",
            root=REPO_ROOT / ".agent" / "data",
            pattern="SCOUT_SNAPSHOT_*.json",
            classification="versioned_cold",
            reason="Scout snapshots are repeatable evidence, not hot runtime state.",
            action="move_to_cold",
            cold_root=DATA_COLD_ROOT,
            keep_latest=RETENTION_LIMIT,
            skip_names=("SCOUT_SNAPSHOT_latest.json",),
        ),
        FamilyRule(
            id="wiki_inventory_history",
            root=REPO_ROOT / ".agent" / "data" / "wiki_inventory_history",
            pattern="*.json",
            classification="versioned_cold",
            reason="Inventory history floods the hot tree; only the newest forensic tail stays nearby.",
            action="move_to_cold",
            cold_root=DATA_COLD_ROOT,
            keep_latest=RETENTION_LIMIT,
        ),
        FamilyRule(
            id="audit_reports",
            root=REPO_ROOT / "Logs" / "Archive",
            pattern="Audit_*.txt",
            classification="versioned_cold",
            reason="Bulk audit reports belong in colder archive buckets after the latest tail.",
            action="move_to_cold",
            cold_root=ARCHIVE_COLD_ROOT,
            keep_latest=RETENTION_LIMIT,
        ),
        FamilyRule(
            id="stats_snapshots",
            root=REPO_ROOT / "Logs" / "Archive",
            pattern="STATS_SNAPSHOT_*.json",
            classification="versioned_cold",
            reason="Machine snapshots are useful, but the hot tree only needs the latest rolling window.",
            action="move_to_cold",
            cold_root=ARCHIVE_COLD_ROOT,
            keep_latest=RETENTION_LIMIT,
            skip_names=("STATS_SNAPSHOT_latest.json",),
        ),
        FamilyRule(
            id="roamlink_repair_reports",
            root=REPO_ROOT / "Logs" / "Archive",
            pattern="ROAMLINK_REPAIR_REPORT_*.json",
            classification="versioned_cold",
            reason="Repair evidence should stay available, but older runs can live in cold buckets.",
            action="move_to_cold",
            cold_root=ARCHIVE_COLD_ROOT,
            keep_latest=RETENTION_LIMIT,
        ),
        FamilyRule(
            id="wiki_review_reports",
            root=REPO_ROOT / "Logs" / "Archive",
            pattern="WIKI_REVIEW_*.md",
            classification="versioned_cold",
            reason="Bulk review reports are historical evidence, not hot operator guidance.",
            action="move_to_cold",
            cold_root=ARCHIVE_COLD_ROOT,
            keep_latest=RETENTION_LIMIT,
        ),
        FamilyRule(
            id="scout_harvest_reports",
            root=REPO_ROOT / "Logs" / "Archive",
            pattern="SCOUT_HARVEST_*.json",
            classification="versioned_cold",
            reason="Harvest reports are durable evidence streams and can be cooled after the latest tail.",
            action="move_to_cold",
            cold_root=ARCHIVE_COLD_ROOT,
            keep_latest=RETENTION_LIMIT,
        ),
        FamilyRule(
            id="scout_triage_reports",
            root=REPO_ROOT / "Logs" / "Archive",
            pattern="SCOUT_TRIAGE_*.json",
            classification="versioned_cold",
            reason="Triage reports are historical diagnostics and do not belong in the hot operator surface.",
            action="move_to_cold",
            cold_root=ARCHIVE_COLD_ROOT,
            keep_latest=RETENTION_LIMIT,
        ),
        FamilyRule(
            id="local_runtime_cache",
            root=REPO_ROOT,
            pattern=".agent/data/pages_cache",
            classification="local_runtime",
            reason="Pages caches are disposable runtime acceleration, not repo truth.",
            action="prune_runtime_tree",
        ),
        FamilyRule(
            id="local_runtime_models",
            root=REPO_ROOT,
            pattern=".agent/data/models/*",
            classification="local_runtime",
            reason="Model cache contents are local runtime state and can be regenerated; the empty cache root may be recreated by the CLI bootstrap.",
            action="prune_runtime_tree",
        ),
        FamilyRule(
            id="local_runtime_vector_db",
            root=REPO_ROOT,
            pattern=".agent/data/chroma_db",
            classification="local_runtime",
            reason="Vector stores are local runtime state and should not be treated as hot repo truth.",
            action="prune_runtime_tree",
        ),
        FamilyRule(
            id="local_runtime_venv",
            root=REPO_ROOT,
            pattern=".agent/data/oracle_venv",
            classification="local_runtime",
            reason="Embedded virtualenvs are disposable runtime infrastructure.",
            action="prune_runtime_tree",
        ),
        FamilyRule(
            id="legacy_sandbox",
            root=REPO_ROOT,
            pattern="System/Sandbox",
            classification="local_runtime",
            reason="Sandbox scratch files are not active operator surfaces anymore.",
            action="prune_runtime_tree",
        ),
        FamilyRule(
            id="build_site",
            root=REPO_ROOT,
            pattern="site",
            classification="build_output",
            reason="Site build output is generated publication material, never source truth.",
            action="prune_runtime_tree",
        ),
        FamilyRule(
            id="build_dist",
            root=REPO_ROOT,
            pattern="dist",
            classification="build_output",
            reason="Bundle archives in dist/ are release outputs, not canonical repo state.",
            action="prune_runtime_tree",
        ),
        FamilyRule(
            id="tmp_runtime",
            root=REPO_ROOT,
            pattern=".tmp",
            classification="local_runtime",
            reason="Temporary files are disposable runtime state.",
            action="prune_runtime_tree",
        ),
    ]


def build_report() -> dict:
    families = [classify_rule(rule) for rule in rules()]
    return {
        "generated_at": now_iso(),
        "retention": {"keep_latest_per_family": RETENTION_LIMIT},
        "families": families,
    }


def emit_text(report: dict) -> None:
    print("Repo hygiene report")
    print(f"Generated at: {report['generated_at']}")
    print(f"Retention: keep_latest_per_family={report['retention']['keep_latest_per_family']}")
    for family in report["families"]:
        print(
            f"- {family['id']}: {family['classification']} | action={family['action']} | "
            f"matched={family['matched_count']} | cold_candidates={family['cold_candidate_count']}"
        )
        print(f"  reason: {family['reason']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Classify and conservatively clean repo path families")
    parser.add_argument("--apply", action="store_true", help="Apply approved cleanup actions")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable report")
    args = parser.parse_args()

    report = build_report()

    if args.apply:
        operations = [apply_rule(rule) for rule in rules()]
        report["operations"] = operations

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        emit_text(report)
        if args.apply:
            applied = report.get("operations", [])
            moved = sum(len(entry.get("moved", [])) for entry in applied)
            deleted = sum(len(entry.get("deleted", [])) for entry in applied)
            print(f"Applied cleanup: moved={moved}, deleted={deleted}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
