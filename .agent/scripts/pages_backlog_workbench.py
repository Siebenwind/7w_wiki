#!/usr/bin/env python3
"""Human-friendly Pages backlog workbench.

This script is intentionally a thin orchestration layer over the existing
Pages/repair inventory. It separates Historian-operable backlog clusters from
true human escalation instead of treating every non-mechanical target as one
manual queue.
"""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

from repair import (
    MARKDOWN_LINK_RE,
    PROJECT_ROOT,
    READONLY_BACKLOG_ROOTS,
    WIKILINK_OCCURRENCE_RE,
    _build_backlog_inventory,
    _is_within,
    get_canon_map,
    DOCS_WIKI_DIR,
    normalize_key,
)


DECISIONS_PATH = PROJECT_ROOT / ".agent" / "data" / "pages_backlog_historian_decisions.json"
REPORT_DIR = PROJECT_ROOT / "Logs" / "Reviews"
BULK_WARNING_REASON = "bulk_semantic_apply_requires_explicit_warning_ack"

KNOWN_SEMANTIC_ALIASES = {
    "gnome": "Hoehere_Wesenheiten",
    "djinns": "Hoehere_Wesenheiten",
    "djinn": "Hoehere_Wesenheiten",
    "moorlaeuferin": "Riesenspinnen",
    "moorlaeuferinnen": "Riesenspinnen",
    "kreuzrueckenspinne": "Riesenspinnen",
    "kreuzrueckenspinnen": "Riesenspinnen",
}

CLUSTER_ORDER = [
    "format_wrappers",
    "register_links",
    "generic_magie",
    "werke_links",
    "archive_reports",
    "personenregister",
    "readonly_quellen_residue",
    "human_escalations",
    "historian_other",
]

CLUSTER_DESCRIPTIONS = {
    "format_wrappers": "Technische Markdown-/WikiLink-Wrapper mit eindeutigem Pfad-Replacement.",
    "register_links": "Register- und Indexseiten mit semantisch zu pruefenden Zielbegriffen.",
    "generic_magie": "Magie-/Terminologieziele, die eine Historian-Disambiguierung brauchen.",
    "werke_links": "Werk-/Bibliothekslinks, meist Zielnamen- oder Werktitel-Abgleich.",
    "archive_reports": "Archiv-/Report-Reste, oft publizierte Arbeitsberichte statt Lore-Seiten.",
    "personenregister": "Personenregister-Vorkommen mit Ziel-/Alias-Pruefung.",
    "readonly_quellen_residue": "Rohquellen-Residuen; werden nicht editiert.",
    "human_escalations": "Echte Maintainer-/Human-Entscheidungen.",
    "historian_other": "Sonstige Historian-Faelle ohne sicheren automatischen Cluster.",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def normalize_for_cluster(value: str) -> str:
    translation = str.maketrans({
        "ä": "ae",
        "ö": "oe",
        "ü": "ue",
        "ß": "ss",
        "Ä": "ae",
        "Ö": "oe",
        "Ü": "ue",
    })
    return re.sub(r"[^a-z0-9]", "", value.translate(translation).lower())


def cluster_for_occurrence(occurrence: dict) -> str:
    file_path = str(occurrence.get("file", ""))
    target = str(occurrence.get("target", ""))
    classification = str(occurrence.get("classification", "needs_historian"))
    repair_status = str(occurrence.get("repair_status", ""))
    target_norm = normalize_for_cluster(target)

    if classification == "needs_human":
        return "human_escalations"
    if repair_status == "read_only_source_residue" or file_path.startswith("docs/Quellen/"):
        return "readonly_quellen_residue"
    if occurrence.get("link_kind") == "markdown_url_wrapper":
        return "format_wrappers"
    if "Personenregister.md" in file_path:
        return "personenregister"
    if "Register" in file_path or target_norm.endswith("register") or "register" in target_norm:
        return "register_links"
    if target_norm == "magie" or target_norm.startswith("magie") or "magie" in target_norm:
        return "generic_magie"
    if "/Werke" in file_path or "werk" in target_norm or "bibliothek" in target_norm:
        return "werke_links"
    if file_path.startswith("docs/Archiv/"):
        return "archive_reports"
    return "historian_other"


def action_for_occurrence(occurrence: dict) -> str:
    cluster = cluster_for_occurrence(occurrence)
    if cluster == "human_escalations":
        return "escalate_human"
    if cluster == "readonly_quellen_residue":
        return "readonly_note"
    if occurrence.get("link_kind") == "markdown_url_wrapper" and occurrence.get("replacement"):
        return "fix"
    return "defer"


def build_clusters(inventory: dict) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for occurrence in inventory.get("occurrences", []):
        grouped[cluster_for_occurrence(occurrence)].append(occurrence)
    for item in inventory.get("unfound_targets", []):
        synthetic = {
            "file": "",
            "line": None,
            "column": None,
            "link_kind": "target_without_occurrence",
            "target": item.get("target", ""),
            "classification": item.get("classification", "needs_historian"),
            "policy_status": item.get("policy_status", "untracked"),
            "canonical_candidates": item.get("canonical_candidates", []),
            "replacement_target": item.get("replacement_hint"),
            "replacement": None,
            "repair_status": "target_without_occurrence",
        }
        grouped[cluster_for_occurrence(synthetic)].append(synthetic)
    return grouped


def cluster_summary(name: str, items: list[dict]) -> dict:
    action_counts: dict[str, int] = defaultdict(int)
    targets: dict[str, int] = defaultdict(int)
    files: set[str] = set()
    fixable = 0
    readonly = 0
    human = 0
    for item in items:
        action = action_for_occurrence(item)
        action_counts[action] += 1
        if action == "fix":
            fixable += 1
        elif action == "readonly_note":
            readonly += 1
        elif action == "escalate_human":
            human += 1
        target = str(item.get("target", ""))
        if target:
            targets[target] += 1
        file_path = str(item.get("file", ""))
        if file_path:
            files.add(file_path)
    return {
        "cluster": name,
        "description": CLUSTER_DESCRIPTIONS.get(name, ""),
        "occurrences": len(items),
        "target_count": len(targets),
        "file_count": len(files),
        "fixable_occurrences": fixable,
        "readonly_occurrences": readonly,
        "human_escalations": human,
        "action_counts": dict(sorted(action_counts.items())),
        "top_targets": [
            {"target": target, "count": count}
            for target, count in sorted(targets.items(), key=lambda entry: (-entry[1], entry[0]))[:10]
        ],
        "example_files": sorted(files)[:8],
    }


def build_summary() -> dict:
    inventory = _build_backlog_inventory()
    grouped = build_clusters(inventory)
    clusters = [
        cluster_summary(name, grouped.get(name, []))
        for name in CLUSTER_ORDER
        if grouped.get(name)
    ]
    recommended = [
        cluster["cluster"]
        for cluster in clusters
        if cluster["cluster"] != "human_escalations"
    ][:3]
    return {
        "generated_at": now_iso(),
        "status": "ok",
        "pages_health": inventory["pages_health"],
        "inventory_summary": inventory["summary"],
        "cluster_count": len(clusters),
        "clusters": clusters,
        "recommended_next": recommended,
        "semantics": {
            "needs_historian": "Historian-operable cluster lane",
            "needs_human": "Final human escalation only",
        },
    }


def print_summary(payload: dict) -> None:
    pages = payload["pages_health"]
    print("Pages Backlog Workbench")
    print(f"Pages: {pages['status']} unresolved={pages['unresolved_total']} unallowlisted={pages['unallowlisted_total']}")
    print(f"Classification: {pages.get('classification_counts', {})}")
    print("")
    print("Historian Cluster:")
    for cluster in payload["clusters"]:
        print(
            f"- {cluster['cluster']}: occurrences={cluster['occurrences']} "
            f"targets={cluster['target_count']} fixable={cluster['fixable_occurrences']} "
            f"readonly={cluster['readonly_occurrences']} human={cluster['human_escalations']}"
        )
    print("")
    print("Next:")
    for cluster in payload["recommended_next"]:
        print(f"  ./7w_wiki.py pages backlog historian --cluster {cluster} --dry-run")


def build_cluster_plan(cluster_name: str) -> dict:
    inventory = _build_backlog_inventory()
    grouped = build_clusters(inventory)
    items = grouped.get(cluster_name, [])
    planned = []
    for item in items:
        file_path = str(item.get("file", ""))
        action = action_for_occurrence(item)
        editable = bool(file_path) and not file_path.startswith("docs/Quellen/")
        planned.append(
            {
                "action": action,
                "file": file_path,
                "line": item.get("line"),
                "target": item.get("target"),
                "url_target": item.get("url_target"),
                "replacement": item.get("replacement"),
                "replacement_target": item.get("replacement_target"),
                "classification": item.get("classification"),
                "repair_status": item.get("repair_status"),
                "editable": editable,
                "reason": action_reason(action),
            }
        )
    counts: dict[str, int] = defaultdict(int)
    for item in planned:
        counts[item["action"]] += 1
    return {
        "generated_at": now_iso(),
        "status": "ok",
        "cluster": cluster_name,
        "description": CLUSTER_DESCRIPTIONS.get(cluster_name, ""),
        "summary": cluster_summary(cluster_name, items),
        "action_counts": dict(sorted(counts.items())),
        "planned": planned,
        "apply_supported": cluster_name == "format_wrappers",
        "apply_rule": "Only markdown_url_wrapper entries with concrete replacements are applied.",
    }


def project_rel_path(path_value: str) -> str:
    path = Path(path_value)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    try:
        return str(path.resolve().relative_to(PROJECT_ROOT))
    except Exception:
        return str(path_value)


def build_page_index() -> dict[str, dict]:
    canon_map = get_canon_map(DOCS_WIKI_DIR)
    index: dict[str, dict] = {}
    for paths in canon_map.values():
        for path in paths:
            if not _is_within(path, (DOCS_WIKI_DIR,)):
                continue
            stem = path.stem
            index.setdefault(stem, {
                "target": stem,
                "file": str(path.relative_to(PROJECT_ROOT)),
                "normalized": normalize_key(stem),
            })
    return index


def collect_items_for_scope(cluster_name: str | None, article: str | None, run_all: bool) -> tuple[dict, list[dict], str]:
    inventory = _build_backlog_inventory()
    grouped = build_clusters(inventory)
    article_rel = project_rel_path(article) if article else None
    if run_all:
        items = []
        for name in CLUSTER_ORDER:
            if name in {"readonly_quellen_residue", "human_escalations"}:
                continue
            items.extend(grouped.get(name, []))
        scope = "run_all"
    elif cluster_name:
        items = list(grouped.get(cluster_name, []))
        scope = cluster_name
    elif article_rel:
        items = list(inventory.get("occurrences", []))
        scope = article_rel
    else:
        raise ValueError("resolve benoetigt --cluster, --article oder --run-all.")
    if article_rel:
        items = [item for item in items if str(item.get("file", "")) == article_rel]
    return inventory, items, scope


def evidence_for_decision(item: dict, replacement: str | None = None, reason: str | None = None) -> list[str]:
    evidence = []
    file_path = str(item.get("file") or "")
    if file_path:
        line = item.get("line")
        evidence.append(f"{file_path}:{line}" if line else file_path)
    candidates = item.get("canonical_candidates") or []
    if candidates:
        evidence.append(f"canonical_candidates={','.join(str(candidate) for candidate in candidates[:3])}")
    if replacement:
        evidence.append(f"replacement={replacement}")
    if reason:
        evidence.append(reason)
    return evidence


def semantic_resolution_for_item(item: dict, page_index: dict[str, dict]) -> dict:
    file_path = str(item.get("file") or "")
    target = str(item.get("target") or "")
    cluster = cluster_for_occurrence(item)
    editable = bool(file_path) and not file_path.startswith("docs/Quellen/")
    target_norm = normalize_key(target)

    base = {
        "file": file_path,
        "line": item.get("line"),
        "target": target,
        "cluster": cluster,
        "editable": editable,
        "classification": item.get("classification"),
        "repair_status": item.get("repair_status"),
        "replacement": None,
        "confidence": 0.0,
        "evidence": [],
    }

    if cluster == "readonly_quellen_residue" or file_path.startswith("docs/Quellen/"):
        return {
            **base,
            "action": "readonly_note",
            "reason": "Rohquelle oder read-only residue; nicht editieren.",
            "evidence": evidence_for_decision(item, reason="readonly_source"),
        }
    if cluster == "human_escalations" or item.get("classification") == "needs_human":
        return {
            **base,
            "action": "needs_human",
            "reason": "Echte Human-Entscheidung erforderlich.",
            "confidence": 0.0,
            "evidence": evidence_for_decision(item, reason="needs_human"),
        }
    if not editable:
        return {
            **base,
            "action": "leave",
            "reason": "Kein konkreter editierbarer Vorkommensort vorhanden.",
            "evidence": evidence_for_decision(item, reason="target_without_occurrence"),
        }

    if item.get("replacement_target"):
        replacement = str(item["replacement_target"])
        return {
            **base,
            "action": "replace",
            "replacement": replacement,
            "confidence": 0.95,
            "reason": "Vorhandener eindeutiger Replacement-Hinweis aus Pages-Inventar.",
            "evidence": evidence_for_decision(item, replacement, "inventory_replacement"),
        }

    alias_target = KNOWN_SEMANTIC_ALIASES.get(target_norm)
    if alias_target and alias_target in page_index:
        return {
            **base,
            "action": "replace",
            "replacement": alias_target,
            "confidence": 0.9,
            "reason": "Bekannte lokale Historian-Zuordnung auf vorhandene Zielseite.",
            "evidence": evidence_for_decision(item, alias_target, "known_semantic_alias"),
        }

    candidates = [str(candidate) for candidate in item.get("canonical_candidates", []) if str(candidate)]
    existing_candidates = [candidate for candidate in candidates if candidate in page_index]
    if len(existing_candidates) == 1:
        replacement = existing_candidates[0]
        return {
            **base,
            "action": "replace",
            "replacement": replacement,
            "confidence": 0.85,
            "reason": "Genau ein vorhandener kanonischer Kandidat.",
            "evidence": evidence_for_decision(item, replacement, "single_canonical_candidate"),
        }
    if len(existing_candidates) > 1:
        return {
            **base,
            "action": "needs_human",
            "confidence": 0.0,
            "reason": "Mehrere vorhandene kanonische Kandidaten.",
            "evidence": evidence_for_decision(item, reason="multiple_canonical_candidates"),
        }

    return {
        **base,
        "action": "leave",
        "reason": "Keine belastbare lokale Zielseite gefunden.",
        "evidence": evidence_for_decision(item, reason="no_local_target"),
    }


def summarize_resolutions(resolutions: list[dict]) -> dict:
    counts: dict[str, int] = defaultdict(int)
    files = set()
    for decision in resolutions:
        counts[decision.get("action", "unknown")] += 1
        if decision.get("file"):
            files.add(decision["file"])
    return {
        "total": len(resolutions),
        "action_counts": dict(sorted(counts.items())),
        "file_count": len(files),
        "files": sorted(files)[:20],
    }


def build_resolution_plan(cluster_name: str | None = None, article: str | None = None, run_all: bool = False) -> dict:
    _inventory, items, scope = collect_items_for_scope(cluster_name, article, run_all)
    page_index = build_page_index()
    resolutions = [semantic_resolution_for_item(item, page_index) for item in items]
    return {
        "generated_at": now_iso(),
        "status": "ok",
        "mode": "resolve",
        "scope": "run_all" if run_all else "article" if article else "cluster",
        "cluster": cluster_name,
        "article": project_rel_path(article) if article else None,
        "target_scope": scope,
        "warning": "Semantic bulk run may change many links; use --apply --yes --i-understand-bulk-semantics to write." if run_all else None,
        "summary": summarize_resolutions(resolutions),
        "resolutions": resolutions,
    }


def replacement_wikilink(match: re.Match, replacement: str) -> str:
    target = match.group("target").strip()
    anchor = match.group("anchor") or ""
    label_group = match.group("label") or ""
    label = label_group[1:] if label_group.startswith("|") else ""
    display = label or target
    if replacement == target and not label:
        return match.group(0)
    return f"[[{replacement}{anchor}|{display}]]"


def apply_resolution_plan(plan: dict, *, yes: bool, bulk_ack: bool) -> dict:
    if not yes:
        return {
            "status": "blocked",
            "reason": "apply_requires_yes",
            "scope": plan.get("scope"),
            "cluster": plan.get("cluster"),
            "article": plan.get("article"),
        }
    if plan.get("scope") == "run_all" and not bulk_ack:
        return {
            "status": "blocked",
            "reason": BULK_WARNING_REASON,
            "warning": "Vollautomatische semantische Backlog-Laeufe koennen viele Links veraendern. Wiederhole mit --i-understand-bulk-semantics.",
        }

    entries_by_file: dict[str, list[dict]] = defaultdict(list)
    decisions = plan.get("resolutions", [])
    for decision in decisions:
        if decision.get("action") != "replace" or not decision.get("file") or not decision.get("replacement"):
            continue
        file_path = PROJECT_ROOT / decision["file"]
        if _is_within(file_path, READONLY_BACKLOG_ROOTS):
            continue
        entries_by_file[decision["file"]].append(decision)

    changed_files = []
    planned_files = []
    for rel_path, entries in sorted(entries_by_file.items()):
        file_path = PROJECT_ROOT / rel_path
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            continue

        line_entries: dict[int, list[dict]] = defaultdict(list)
        for entry in entries:
            if entry.get("line"):
                line_entries[int(entry["line"])].append(entry)

        new_lines = []
        for number, line in enumerate(content.splitlines(keepends=True), start=1):
            active = line_entries.get(number, [])
            if not active:
                new_lines.append(line)
                continue

            def repl(match: re.Match) -> str:
                target = match.group("target").strip()
                for entry in active:
                    if target == entry.get("target"):
                        return replacement_wikilink(match, str(entry["replacement"]))
                return match.group(0)

            new_lines.append(WIKILINK_OCCURRENCE_RE.sub(repl, line))

        new_content = "".join(new_lines)
        if new_content == content:
            continue
        planned_files.append(rel_path)
        file_path.write_text(new_content, encoding="utf-8")
        changed_files.append(rel_path)

    result = {
        "status": "ok",
        "mode": "resolve_apply",
        "scope": plan.get("scope"),
        "cluster": plan.get("cluster"),
        "article": plan.get("article"),
        "planned_files": planned_files,
        "changed_files": changed_files,
        "planned_files_total": len(planned_files),
        "changed_files_total": len(changed_files),
        "decision_summary": plan.get("summary", {}),
        "decisions": decisions,
    }
    if changed_files:
        append_decision(result)
        write_report(plan, result)
    return result


def action_reason(action: str) -> str:
    return {
        "fix": "Eindeutige technische Format-/Wrapper-Reparatur.",
        "defer": "Historian-Kontextpruefung noetig; keine automatische Ersetzung.",
        "readonly_note": "Rohquelle oder read-only residue; nicht editieren.",
        "escalate_human": "Echte Human-Entscheidung erforderlich.",
    }.get(action, "Unklassifizierte Aktion.")


def print_cluster_plan(plan: dict) -> None:
    print(f"Historian Cluster: {plan['cluster']}")
    print(plan["description"])
    print(f"Occurrences: {plan['summary']['occurrences']} | fixable={plan['summary']['fixable_occurrences']}")
    print("")
    for item in plan["planned"][:40]:
        location = item["file"] or "<target-only>"
        if item.get("line"):
            location += f":{item['line']}"
        print(f"- {item['action']}: {item['target']} @ {location}")
        if item.get("replacement"):
            print(f"  -> {item['replacement']}")
    if len(plan["planned"]) > 40:
        print(f"... {len(plan['planned']) - 40} weitere Eintraege")
    print("")
    if plan["apply_supported"]:
        print(f"Dry-run: ./7w_wiki.py pages backlog historian --cluster {plan['cluster']} --dry-run")
        print(f"Apply:   ./7w_wiki.py pages backlog historian --cluster {plan['cluster']} --apply --yes")
    else:
        print("Dieser Cluster ist ein Historian-Dossier; keine automatische Apply-Aktion.")


def print_resolution_plan(plan: dict) -> None:
    print("Pages Backlog Historian Resolution")
    print(f"Scope: {plan['scope']} {plan.get('target_scope') or ''}".strip())
    if plan.get("warning"):
        print(f"Warnung: {plan['warning']}")
    summary = plan.get("summary", {})
    print(f"Resolutions: {summary.get('total', 0)} {summary.get('action_counts', {})}")
    print("")
    for decision in plan.get("resolutions", [])[:40]:
        location = decision.get("file") or "<target-only>"
        if decision.get("line"):
            location += f":{decision['line']}"
        replacement = f" -> {decision['replacement']}" if decision.get("replacement") else ""
        print(f"- {decision.get('action')}: {decision.get('target')}{replacement} @ {location}")
    if len(plan.get("resolutions", [])) > 40:
        print(f"... {len(plan['resolutions']) - 40} weitere Entscheidungen")


def apply_format_wrapper_plan(plan: dict, *, dry_run: bool, yes: bool) -> dict:
    if not dry_run and not yes:
        return {
            "status": "blocked",
            "reason": "apply_requires_yes",
            "cluster": plan["cluster"],
        }
    by_file: dict[str, list[dict]] = defaultdict(list)
    for item in plan.get("planned", []):
        if item.get("action") != "fix" or not item.get("file") or not item.get("replacement"):
            continue
        by_file[item["file"]].append(item)

    changed_files: list[str] = []
    planned_files: list[str] = []
    for rel_path, entries in sorted(by_file.items()):
        file_path = PROJECT_ROOT / rel_path
        if _is_within(file_path, READONLY_BACKLOG_ROOTS):
            continue
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            continue

        def repl(match: re.Match) -> str:
            target = match.group("target").strip()
            for entry in entries:
                if (
                    target == entry.get("url_target")
                    or target == entry.get("replacement_target")
                    or target == entry.get("target")
                ):
                    replacement = str(entry.get("replacement") or "")
                    if replacement:
                        return f"[{match.group('label')}]({replacement})"
            return match.group(0)

        new_content = MARKDOWN_LINK_RE.sub(repl, content)
        if new_content == content:
            continue
        planned_files.append(rel_path)
        if not dry_run:
            file_path.write_text(new_content, encoding="utf-8")
            changed_files.append(rel_path)

    result = {
        "status": "dry_run" if dry_run else "ok",
        "cluster": plan["cluster"],
        "planned_files": planned_files,
        "changed_files": changed_files,
        "planned_files_total": len(planned_files),
        "changed_files_total": len(changed_files),
    }
    if not dry_run:
        append_decision(result)
        write_report(plan, result)
    return result


def append_decision(result: dict) -> None:
    DECISIONS_PATH.parent.mkdir(parents=True, exist_ok=True)
    if DECISIONS_PATH.exists():
        try:
            data = json.loads(DECISIONS_PATH.read_text(encoding="utf-8"))
        except Exception:
            data = {"version": 1, "decisions": []}
    else:
        data = {"version": 1, "decisions": []}
    data.setdefault("decisions", []).append({
        "timestamp": now_iso(),
        "cluster": result.get("cluster"),
        "article": result.get("article"),
        "scope": result.get("scope"),
        "status": result.get("status"),
        "mode": result.get("mode"),
        "changed_files": result.get("changed_files", []),
        "decision_summary": result.get("decision_summary", {}),
        "semantic_decisions": result.get("decisions", []),
    })
    DECISIONS_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_report(plan: dict, result: dict) -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")
    path = REPORT_DIR / f"PAGES_BACKLOG_HISTORIAN_{stamp}.md"
    title = plan.get("cluster") or plan.get("article") or plan.get("target_scope") or "run_all"
    decisions = result.get("decisions", plan.get("resolutions", []))
    lines = [
        f"# Pages Backlog Historian: {title}",
        "",
        f"- Zeitpunkt: `{now_iso()}`",
        f"- Status: `{result['status']}`",
        f"- Modus: `{plan.get('mode', 'apply')}`",
        f"- Geaenderte Dateien: `{result.get('changed_files_total', 0)}`",
        "",
        "## Dateien",
        "",
    ]
    lines.extend(f"- `{file}`" for file in result.get("changed_files", []))
    if decisions:
        lines.extend(["", "## Entscheidungen", ""])
        for decision in decisions[:200]:
            lines.append(
                f"- `{decision.get('action')}` `{decision.get('target')}`"
                f" -> `{decision.get('replacement')}` @ `{decision.get('file') or '<target-only>'}`"
            )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Pages backlog workbench")
    sub = parser.add_subparsers(dest="cmd")

    summary = sub.add_parser("summary", help="Show Pages backlog cluster summary")
    summary.add_argument("--json", action="store_true")

    historian = sub.add_parser("historian", help="Run or inspect Historian-operable backlog clusters")
    historian.add_argument("--next", action="store_true", help="Show next suggested clusters")
    historian.add_argument("--cluster", choices=CLUSTER_ORDER, help="Cluster to inspect or apply")
    historian.add_argument("--article", help="Limit Historian workbench to one repo-relative article path")
    historian.add_argument("--run-all", action="store_true", help="Resolve all non-readonly Historian clusters")
    historian.add_argument("--resolve", action="store_true", help="Build semantic Historian resolution decisions")
    historian.add_argument("--dry-run", action="store_true", help="Preview without writing")
    historian.add_argument("--apply", action="store_true", help="Apply supported cluster fixes")
    historian.add_argument("--yes", action="store_true", help="Confirm apply")
    historian.add_argument("--i-understand-bulk-semantics", action="store_true", help="Acknowledge warning for run-all semantic apply")
    historian.add_argument("--json", action="store_true")

    args = parser.parse_args()

    if args.cmd == "summary":
        payload = build_summary()
        if args.json:
            print(json.dumps(payload, indent=2, ensure_ascii=False))
        else:
            print_summary(payload)
        return 0

    if args.cmd == "historian":
        if args.next:
            payload = build_summary()
            if args.json:
                print(json.dumps({
                    "status": "ok",
                    "recommended_next": payload["recommended_next"],
                    "clusters": payload["clusters"],
                }, indent=2, ensure_ascii=False))
            else:
                print_summary(payload)
            return 0
        if args.resolve:
            if not args.cluster and not args.article and not args.run_all:
                parser.error("historian --resolve benoetigt --cluster, --article oder --run-all.")
            plan = build_resolution_plan(cluster_name=args.cluster, article=args.article, run_all=args.run_all)
            if args.apply:
                payload = apply_resolution_plan(
                    plan,
                    yes=args.yes,
                    bulk_ack=args.i_understand_bulk_semantics,
                )
                if args.json:
                    print(json.dumps(payload, indent=2, ensure_ascii=False))
                else:
                    print(json.dumps(payload, indent=2, ensure_ascii=False))
                return 0 if payload["status"] == "ok" else 1
            if args.json:
                print(json.dumps(plan, indent=2, ensure_ascii=False))
            else:
                print_resolution_plan(plan)
            return 0
        if not args.cluster:
            parser.error("historian benoetigt --next, --resolve oder --cluster.")
        plan = build_cluster_plan(args.cluster)
        if args.apply:
            if args.cluster != "format_wrappers":
                payload = {
                    "status": "blocked",
                    "reason": "cluster_apply_not_supported",
                    "cluster": args.cluster,
                    "plan": plan,
                }
            else:
                payload = apply_format_wrapper_plan(plan, dry_run=args.dry_run, yes=args.yes)
                payload["plan"] = plan
            if args.json:
                print(json.dumps(payload, indent=2, ensure_ascii=False))
            else:
                print(json.dumps(payload, indent=2, ensure_ascii=False))
            return 0 if payload["status"] in {"ok", "dry_run"} else 1
        if args.json:
            print(json.dumps(plan, indent=2, ensure_ascii=False))
        else:
            print_cluster_plan(plan)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
