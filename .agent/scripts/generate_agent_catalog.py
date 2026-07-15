#!/usr/bin/env python3
"""
Generate the canonical neutral catalog for agents, skills, workflows, and adapter
surfaces. This catalog is the source for Codex skills, MCP resources/prompts, and
future discovery adapters.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG_DIR = REPO_ROOT / ".agent" / "catalog"
CATALOG_PATH = CATALOG_DIR / "catalog.v1.json"
SCHEMA_PATH = CATALOG_DIR / "catalog.v1.schema.json"
WORKFLOWS_DIR = REPO_ROOT / ".agent" / "workflows"
SKILLS_DIR = REPO_ROOT / ".agent" / "skills"
INSTRUCTIONS_DIR = REPO_ROOT / ".agent" / "instructions"
RUNTIME_CONFIG_PATH = REPO_ROOT / ".agent" / "config" / "runtime.json"
DELEGATION_POLICY_PATH = REPO_ROOT / ".agent" / "config" / "delegation_policy.json"
CLI_PATH = REPO_ROOT / "7w_wiki.py"

LIST_FIELDS = {
    "runtime_commands",
    "method_only",
    "method_hints_non_runtime",
    "followup_commands",
    "adapter_targets",
    "deprecated_aliases",
}
SCALAR_FIELDS = {
    "interop_note",
    "matrix_status",
    "runtime_adapter",
    "catalog_id",
    "primary_command",
}

WORKFLOW_Codex_ADAPTERS = {
    "start": {
        "id": "session_start",
        "name": "Session Start",
        "description": "Codex-native onboarding adapter for the standard session kickoff loop.",
        "instructions": [
            "Use this adapter when opening a fresh Siebenwind session in Codex or another IDE.",
            "Run the primary command first; use --run only when the workflow checklist should execute interactively.",
            "Review advisor output, open dispatch, clean-client-state, and the latest session memory before taking new work."
        ],
        "references": [
            ".agent/workflows/start.md",
            "MASTER_TASK_LIST.md",
            "Logs/Archive/SESSION_MEMORY_*.md"
        ],
    },
    "takeover": {
        "id": "session_takeover",
        "name": "Session Takeover",
        "description": "Codex-native adapter for adopting an existing Siebenwind session.",
        "instructions": [
            "Use this adapter when inheriting work from a prior agent session.",
            "Prefer /start as the canonical routing surface; antigravity survives only as a compatibility alias.",
            "Carry forward open dispatches, the latest session memory, and unresolved historian or technician gates explicitly."
        ],
        "references": [
            ".agent/workflows/takeover.md",
            ".agent/workflows/start.md",
            "Logs/Archive/SESSION_MEMORY_*.md"
        ],
    },
    "handover": {
        "id": "session_handover",
        "name": "Session Handover",
        "description": "Codex-native closeout adapter for session memory, dispatch, and validation handoff.",
        "instructions": [
            "Use this adapter when ending a working session and preparing the next agent handoff.",
            "Keep validation, session-memory creation, and dispatch reporting coupled; no silent closeout is acceptable.",
            "If technical or published-doc surfaces changed, include the pages snapshot or pages validation result in the handoff note."
        ],
        "references": [
            ".agent/workflows/handover.md",
            "CHANGELOG.md",
            "Logs/Archive/SESSION_MEMORY_*.md"
        ],
    },
    "tech_master": {
        "id": "workflow_tech_master",
        "name": "Workflow Tech Master",
        "description": "Codex-native maintenance adapter for interop sync, pages health, and runtime hygiene.",
        "instructions": [
            "Use this adapter for runtime-authoritative maintenance work: docs sync, adapter generation, pages integrity, and CLI surface hygiene.",
            "Prefer ./7w_wiki.py tech --sync-surfaces for the full surface refresh. --sync-bridges remains compatibility-only.",
            "Treat GitHub Pages and Codex integration as derived UX layers; keep .agent plus ./7w_wiki.py authoritative."
        ],
        "references": [
            ".agent/workflows/tech_master.md",
            "System/Synapse_Board/SY_INTEROP.md",
            "System/MCP/README.md"
        ],
    },
    "test_run": {
        "id": "workflow_test_run",
        "name": "Workflow Test Run",
        "description": "Codex-native regression adapter for interop, adapter-surface, and clean-state verification.",
        "instructions": [
            "Use this adapter for the standard QA loop after interop or infrastructure changes.",
            "Route failures through Dispatch or task claims before fixing; re-test after each fix.",
            "Treat adapter-surface, catalog, and delegation-policy checks as first-class interop gates."
        ],
        "references": [
            ".agent/workflows/test_run.md",
            "System/Synapse_Board/SY_TESTING.md"
        ],
    },
    "forum_search": {
        "id": "workflow_forum_search",
        "name": "Workflow Forum Search",
        "description": "Codex-native discovery adapter for board-first source scanning and ingest lead generation.",
        "instructions": [
            "Use this adapter when the task is forum-first discovery rather than broad homepage or web scouting.",
            "Restrict scanning to the allowlisted boards and treat outputs as leads, not as already integrated sources.",
            "Escalate only genuine contention or unresolved canon questions; routine ingest leads go to the Ingestor."
        ],
        "references": [
            ".agent/workflows/forum_search.md",
            "Quellen/Forum/",
            "docs/Quellen/Forum/"
        ],
    },
}

SKILL_Codex_ADAPTERS = {
    "art_director": {
        "name": "Art Director (Atelier)",
        "description": "Codex-native visual-direction adapter for style-safe asset work and dispatch coordination.",
        "primary_command": "./7w_wiki.py mail post --from ArtDirector --to Coordinator --subject \"<visual task>\" --body \"<summary>\"",
        "followup_commands": [
            "./7w_wiki.py mail inbox --status OPEN"
        ],
        "instructions": [
            "Use this adapter for visual direction, asset review, and style-governed art requests.",
            "The repo has no dedicated image-generation CLI yet, so route requests and delivery state through Dispatch while following the canonical style preset.",
            "Keep sidecar metadata and canon anchor references coupled to every produced asset."
        ],
        "references": [
            ".agent/skills/art_director/SKILL.md",
            "docs/assets/"
        ],
    },
    "kanon_waechter": {
        "primary_command": "./7w_wiki.py search <query> --source all",
        "followup_commands": [
            "./7w_wiki.py historian <query>",
            "./7w_wiki.py mail post --from Guardian --to Historian --subject \"<conflict>\" --body \"<summary>\""
        ],
        "instructions": [
            "Use this adapter when a claim needs canon verification against higher-precedence material.",
            "Search wiki and sources together first; escalate contradictions instead of silently normalizing them.",
            "Homepage and sources outrank wiki pages for factual resolution."
        ],
        "references": [
            ".agent/skills/kanon_waechter/SKILL.md",
            "System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md"
        ],
    },
    "lektor": {
        "primary_command": "./7w_wiki.py check [path]",
        "followup_commands": [
            "./7w_wiki.py lint [target]"
        ],
        "instructions": [
            "Use this adapter for style, grammar, and markdown hygiene checks.",
            "Run check first on the narrow target; escalate to lint when broader repo coverage is needed.",
            "Treat findings as quality gates before final publication or handoff."
        ],
        "references": [
            ".agent/skills/lektor/SKILL.md"
        ],
    },
    "linguist": {
        "primary_command": "./7w_wiki.py translate [args...]",
        "followup_commands": [
            "./7w_wiki.py search <query> --source all"
        ],
        "instructions": [
            "Use this adapter for falandric analysis, translation tasks, and language-dataset maintenance.",
            "Resolve meaning in context, not as isolated word substitution.",
            "Cross-check canon significance through search when a term affects lore or chronology."
        ],
        "references": [
            ".agent/skills/linguist/SKILL.md"
        ],
    },
    "lore_gelehrter": {
        "primary_command": "./7w_wiki.py historian <query>",
        "followup_commands": [
            "./7w_wiki.py search <query> --source all",
            "./7w_wiki.py historian review --list --json",
            "./7w_wiki.py historian review --dossier --research-id RESEARCH-2026-XXX --json",
            "./7w_wiki.py pages backlog historian --next",
            "./7w_wiki.py pages backlog historian --cluster <cluster> --dry-run --json",
            "./7w_wiki.py pages backlog historian --article <path> --resolve --json",
            "./7w_wiki.py pages backlog historian --cluster <cluster> --resolve --json",
            "./7w_wiki.py pages backlog historian --run-all --resolve --json",
            "./7w_wiki.py mail post --from Historian --to ALL --subject \"<lore question>\" --body \"<summary>\""
        ],
        "instructions": [
            "Use this adapter for deep lore synthesis, contradiction analysis, and evidence-backed answers.",
            "The Historian is an escalation and synthesis organ, not the default editor for straightforward source integration.",
            "Use historian review for structured Research Board review backlog before relying on ad-hoc Dispatch reading.",
            "Treat Pages needs_historian as a Historian-operable cluster lane; reserve needs_human for true maintainer escalation.",
            "Use Pages backlog --resolve for article, cluster, and run-all resolution runs; bulk semantic apply requires explicit warning acknowledgement.",
            "Route unresolved contradictions through Dispatch or the Synapse Board with explicit evidence."
        ],
        "references": [
            ".agent/skills/lore_gelehrter/SKILL.md",
            "System/Synapse_Board/LORE_RESEARCH_BOARD.md"
        ],
    },
    "oracle": {
        "primary_command": "./7w_wiki.py search <query> [remaining...]",
        "followup_commands": [
            "./7w_wiki.py search <query> --source all",
            "./7w_wiki.py index --status"
        ],
        "instructions": [
            "Use this adapter for semantic search across wiki pages and source material.",
            "Set --source deliberately so the result set matches the epistemic layer you are checking.",
            "Check index status before assuming search quality problems are content problems."
        ],
        "references": [
            ".agent/skills/oracle/SKILL.md",
            ".agent/skills/oracle/search.py",
            ".agent/skills/oracle/build_index.py"
        ],
    },
    "scanner": {
        "primary_command": "./7w_wiki.py search <query> --source quellen",
        "followup_commands": [
            "./7w_wiki.py scout --forum bekanntmachungen --pages 3"
        ],
        "instructions": [
            "Use this adapter for source-corpus inventory and lead preparation before ingestion or historian work.",
            "Prefer source-targeted search first; use forum scouting only when the task expands beyond the local corpus.",
            "Treat raw file exploration as a method hint, not as a replacement for the CLI runtime contract."
        ],
        "references": [
            ".agent/skills/scanner/SKILL.md"
        ],
    },
    "scout": {
        "primary_command": "./7w_wiki.py scout --forum bekanntmachungen --pages 3",
        "followup_commands": [
            "./7w_wiki.py scout --forum news --pages 3",
            "./7w_wiki.py mail post --from Scout --to Ingestor --subject \"<source lead>\" --body \"<summary>\""
        ],
        "instructions": [
            "Use this adapter for external discovery work that touches homepage or forum surfaces.",
            "Stay passive: no posting, no interaction, only observation and structured lead capture.",
            "Route ingest leads to the Ingestor and reserve historian escalation for real contention."
        ],
        "references": [
            ".agent/skills/scout/SKILL.md",
            ".agent/workflows/forum_search.md"
        ],
    },
    "test_waechter": {
        "primary_command": "./7w_wiki.py test --suite clean-client-state",
        "followup_commands": [
            "./7w_wiki.py test --suite all",
            "./7w_wiki.py test --suite adapter-surfaces-contract"
        ],
        "instructions": [
            "Use this adapter for standardized suite execution and defect-routing discipline.",
            "On failure, create or claim the defect communication artifact before editing.",
            "Re-run focused suites first, then the broader regression pass."
        ],
        "references": [
            ".agent/skills/test_waechter/SKILL.md",
            ".agent/workflows/test_run.md"
        ],
    },
    "time_keeper": {
        "primary_command": "./7w_wiki.py search \"Sonnenzirkel\" --source all",
        "followup_commands": [
            "./7w_wiki.py mail post --from TimeKeeper --to Historian --subject \"<calendar question>\" --body \"<summary>\""
        ],
        "instructions": [
            "Use this adapter for calendar, season, and date-validation questions tied to the Sonnenzirkel system.",
            "The bundled helper script remains the detailed reference implementation until a first-class CLI command exists.",
            "Treat search results as canon context and escalate ambiguous chronology questions rather than improvising."
        ],
        "references": [
            ".agent/skills/time_keeper/SKILL.md",
            ".agent/skills/time_keeper/scripts/sonnenzirkel.py"
        ],
    },
    "wiki_schmied": {
        "primary_command": "./7w_wiki.py sanitize [target]",
        "followup_commands": [
            "./7w_wiki.py audit",
            "./7w_wiki.py repair --fix-roamlinks --dry-run"
        ],
        "instructions": [
            "Use this adapter for production-safe wiki article shaping, structure hygiene, and link integrity follow-through.",
            "Keep report_id, source references, and anti-bridge policy aligned with the canonical production skill.",
            "Validate the page and its references after structural edits."
        ],
        "references": [
            ".agent/skills/wiki_schmied/SKILL.md",
            "System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md"
        ],
    },
}

RUNTIME_SURFACE_ADAPTERS = {
    "stats": {
        "name": "Stats",
        "description": "Codex-native statistics adapter for reader-facing and machine-readable wiki status outputs.",
        "primary_command": "./7w_wiki.py stats",
        "followup_commands": [
            "./7w_wiki.py test --suite reader-stats-contract"
        ],
        "instructions": [
            "Use this adapter when reader-facing stats pages or machine snapshots need regeneration.",
            "Treat the reader page, tracking register, and JSON snapshot as a coupled contract.",
            "Validate the reader-stats contract after regeneration."
        ],
        "references": [
            "docs/Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md",
            "Logs/Archive/STATS_SNAPSHOT_latest.json",
            "Logs/INGESTION_TRACKING_REGISTER.md"
        ],
    }
}

PROMPT_WORKFLOW_IDS = [
    "start",
    "takeover",
    "handover",
    "tech_master",
    "test_run",
    "forum_search",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def extract_frontmatter(raw: str) -> dict[str, str]:
    match = re.match(r"---\n(.*?)\n---\n", raw, re.DOTALL)
    if not match:
        return {}
    data: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        data[key.strip()] = value.strip().strip("\"'")
    return data


def extract_h1(raw: str) -> str:
    match = re.search(r"^#\s+(.+)$", raw, re.MULTILINE)
    return match.group(1).strip() if match else ""


def extract_first_paragraph(raw: str) -> str:
    body = re.sub(r"^---\n.*?\n---\n", "", raw, flags=re.DOTALL)
    lines = []
    in_block = False
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_block = not in_block
            continue
        if in_block:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.startswith(">"):
            continue
        if not stripped:
            if lines:
                break
            continue
        lines.append(stripped)
    return " ".join(lines).strip()


def normalize_value(value: str) -> str:
    cleaned = value.strip()
    if cleaned.startswith("`") and cleaned.endswith("`"):
        cleaned = cleaned[1:-1]
    return cleaned.strip().strip("\"'")


def parse_interop_status(raw: str) -> dict:
    data = {
        "runtime_commands": [],
        "method_only": [],
        "method_hints_non_runtime": [],
        "followup_commands": [],
        "adapter_targets": [],
        "deprecated_aliases": [],
        "interop_note": "",
        "matrix_status": "",
        "runtime_adapter": "",
        "catalog_id": "",
        "primary_command": "",
    }
    section = re.search(r"## Interop-Status\n(.*?)(?:\n## |\Z)", raw, re.DOTALL)
    if not section:
        return data

    current_list: str | None = None
    for line in section.group(1).splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("- ") and stripped.endswith(":"):
            field = stripped[2:-1]
            current_list = field if field in LIST_FIELDS else None
            continue
        matched_scalar = False
        for field in SCALAR_FIELDS:
            prefix = f"- {field}:"
            if stripped.startswith(prefix):
                data[field] = normalize_value(stripped.split(":", 1)[1])
                current_list = None
                matched_scalar = True
                break
        if matched_scalar:
            continue
        if current_list and re.match(r"^\s{2,}-\s+", line):
            value = normalize_value(stripped[2:].strip())
            data[current_list].append(value)
            continue
        current_list = None
    return data


def load_cli_schema() -> dict:
    result = subprocess.run(
        [sys.executable, str(CLI_PATH), "--help-json"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def build_agents() -> list[dict]:
    agents: list[dict] = []
    for path in sorted(INSTRUCTIONS_DIR.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        h1 = extract_h1(raw)
        name = h1.replace("Persona:", "").strip() if h1 else path.stem.replace("_", " ")
        description = extract_first_paragraph(raw)
        agent_id = path.stem.replace("persona_", "")
        agents.append(
            {
                "id": agent_id,
                "name": name,
                "description": description,
                "source_path": str(path.relative_to(REPO_ROOT)),
            }
        )
    return agents


def build_skills() -> list[dict]:
    skills: list[dict] = []
    for path in sorted(SKILLS_DIR.glob("*/SKILL.md")):
        raw = path.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(raw)
        name = frontmatter.get("name") or extract_h1(raw) or path.parent.name.replace("_", " ")
        description = frontmatter.get("description") or extract_first_paragraph(raw)
        skills.append(
            {
                "id": path.parent.name,
                "name": name,
                "description": description,
                "source_path": str(path.relative_to(REPO_ROOT)),
            }
        )
    return skills


def build_workflows() -> list[dict]:
    workflows: list[dict] = []
    for path in sorted(WORKFLOWS_DIR.glob("*.md")):
        raw = path.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(raw)
        name = frontmatter.get("title") or extract_h1(raw) or path.stem.replace("_", " ")
        description = frontmatter.get("description") or extract_first_paragraph(raw)
        interop = parse_interop_status(raw)
        if not interop["catalog_id"]:
            interop["catalog_id"] = f"workflow.{path.stem}"
        if not interop["primary_command"] and interop["runtime_commands"]:
            interop["primary_command"] = interop["runtime_commands"][0]
        workflows.append(
            {
                "id": path.stem,
                "name": name,
                "description": description,
                "source_path": str(path.relative_to(REPO_ROOT)),
                "interop": interop,
            }
        )
    return workflows


def build_prompt_entry(workflow: dict) -> dict:
    interop = workflow["interop"]
    primary = interop.get("primary_command") or ""
    followups = interop.get("followup_commands", [])
    prompt_lines = [
        f"Use the canonical Siebenwind workflow `{workflow['id']}`.",
        "Runtime authority remains `./7w_wiki.py`.",
    ]
    if primary:
        prompt_lines.append(f"Primary command: `./{primary}`.")
    if followups:
        prompt_lines.append("Follow-up commands:")
        prompt_lines.extend(f"- `./{command}`" for command in followups)
    if interop.get("interop_note"):
        prompt_lines.append(f"Interop note: {interop['interop_note']}")
    return {
        "id": workflow["id"],
        "title": workflow["name"],
        "description": workflow["description"],
        "source_path": workflow["source_path"],
        "prompt": "\n".join(prompt_lines),
    }


def build_codex_surfaces(workflows: list[dict], skills: list[dict]) -> list[dict]:
    workflow_map = {item["id"]: item for item in workflows}
    skill_map = {item["id"]: item for item in skills}
    surfaces: list[dict] = []

    for workflow_id, adapter_meta in WORKFLOW_Codex_ADAPTERS.items():
        workflow = workflow_map[workflow_id]
        interop = workflow["interop"]
        primary = interop.get("primary_command") or workflow["interop"]["runtime_commands"][0]
        followups = interop.get("followup_commands") or workflow["interop"]["runtime_commands"][:3]
        surfaces.append(
            {
                "id": adapter_meta["id"],
                "name": adapter_meta["name"],
                "description": adapter_meta["description"],
                "source_kind": "workflow",
                "source_id": workflow_id,
                "source_path": workflow["source_path"],
                "target_path": f".agents/skills/{adapter_meta['id']}/SKILL.md",
                "primary_command": f"./{primary}",
                "followup_commands": [f"./{command}" for command in followups],
                "instructions": adapter_meta["instructions"],
                "references": adapter_meta["references"],
            }
        )

    for skill_id, adapter_meta in SKILL_Codex_ADAPTERS.items():
        skill = skill_map[skill_id]
        surfaces.append(
            {
                "id": skill_id,
                "name": adapter_meta.get("name", skill["name"]),
                "description": adapter_meta.get("description", skill["description"]),
                "source_kind": "skill",
                "source_id": skill_id,
                "source_path": skill["source_path"],
                "target_path": f".agents/skills/{skill_id}/SKILL.md",
                "primary_command": adapter_meta["primary_command"],
                "followup_commands": adapter_meta.get("followup_commands", []),
                "instructions": adapter_meta.get("instructions", []),
                "references": adapter_meta.get("references", [skill["source_path"]]),
            }
        )

    for surface_id, adapter_meta in RUNTIME_SURFACE_ADAPTERS.items():
        surfaces.append(
            {
                "id": surface_id,
                "name": adapter_meta["name"],
                "description": adapter_meta["description"],
                "source_kind": "runtime",
                "source_id": surface_id,
                "source_path": "7w_wiki.py",
                "target_path": f".agents/skills/{surface_id}/SKILL.md",
                "primary_command": adapter_meta["primary_command"],
                "followup_commands": adapter_meta["followup_commands"],
                "instructions": adapter_meta["instructions"],
                "references": adapter_meta["references"],
            }
        )

    return sorted(surfaces, key=lambda item: item["id"])


def build_catalog() -> dict:
    runtime_config = load_json(RUNTIME_CONFIG_PATH, {})
    delegation_policy = load_json(DELEGATION_POLICY_PATH, {})
    cli_schema = load_cli_schema()
    agents = build_agents()
    skills = build_skills()
    workflows = build_workflows()
    codex_surfaces = build_codex_surfaces(workflows, skills)
    prompt_entries = [build_prompt_entry(workflow) for workflow in workflows if workflow["id"] in PROMPT_WORKFLOW_IDS]

    return {
        "version": "catalog.v1",
        "generated_at": now_iso(),
        "runtime": {
            "entrypoint": "./7w_wiki.py",
            "help_json": "./7w_wiki.py --help-json",
            "commands": cli_schema.get("commands", []),
            "config_path": str(RUNTIME_CONFIG_PATH.relative_to(REPO_ROOT)),
            "config": runtime_config,
        },
        "agents": agents,
        "skills": skills,
        "workflows": workflows,
        "delegation": {
            "policy_path": str(DELEGATION_POLICY_PATH.relative_to(REPO_ROOT)),
            "policy": delegation_policy,
        },
        "surfaces": {
            "codex": {
                "config_path": ".codex/config.toml",
                "skills": codex_surfaces,
            },
            "mcp": {
                "server_path": "System/MCP/server.py",
                "config_path": "mcp_config.json",
                "resources": [
                    {"uri": "wiki://catalog", "path": ".agent/catalog/catalog.v1.json"},
                    {"uri": "wiki://workflows", "path": ".agent/catalog/catalog.v1.json#workflows"},
                    {"uri": "wiki://skills", "path": ".agent/catalog/catalog.v1.json#skills"},
                    {"uri": "wiki://agents", "path": ".agent/catalog/catalog.v1.json#agents"},
                    {"uri": "wiki://status", "path": "./7w_wiki.py advisor --json"},
                    {"uri": "wiki://dispatch/open", "path": "./7w_wiki.py mail inbox --status OPEN"},
                    {"uri": "wiki://prompts", "path": ".agent/catalog/catalog.v1.json#surfaces.mcp.prompts"},
                ],
                "prompts": prompt_entries,
            },
            "a2a": {
                "phase": "discovery-only",
                "agent_card_path": "docs/.well-known/agent.json",
            },
        },
    }


def main() -> int:
    CATALOG_DIR.mkdir(parents=True, exist_ok=True)
    catalog = build_catalog()
    CATALOG_PATH.write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {CATALOG_PATH.relative_to(REPO_ROOT)}")
    if not SCHEMA_PATH.exists():
        print(f"[warn] Schema file missing: {SCHEMA_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
