#!/usr/bin/env python3
"""
Generate lore_manifest.json from the canonical catalog and live CLI schema.

The manifest remains a compatibility surface for external tools, but it is never
the source of truth. Source authority stays on .agent/ plus ./7w_wiki.py.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = REPO_ROOT / ".agent" / "catalog" / "catalog.v1.json"
MANIFEST_PATH = REPO_ROOT / "lore_manifest.json"
VERSION_PATH = REPO_ROOT / "VERSION"


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_catalog() -> dict:
    if not CATALOG_PATH.exists():
        raise FileNotFoundError(f"Catalog missing: {CATALOG_PATH}")
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def load_version() -> str:
    if VERSION_PATH.exists():
        return VERSION_PATH.read_text(encoding="utf-8").strip()
    return "3.0"


def pick_commands(catalog: dict) -> list[str]:
    commands = catalog.get("runtime", {}).get("commands", [])
    preferred = [
        "start",
        "advisor",
        "mail",
        "search",
        "audit",
        "repair",
        "stats",
        "pages",
        "tech",
        "mcp",
    ]
    available = {command.get("name"): command for command in commands if command.get("name")}
    ordered = [name for name in preferred if name in available]
    extras = sorted(name for name in available if name not in ordered)
    return ordered + extras


def build_manifest(catalog: dict) -> dict:
    generated_at = catalog.get("generated_at") or now_iso()
    commands = pick_commands(catalog)
    return {
        "schema_version": "lore-manifest.v3",
        "generated_at": generated_at,
        "generated_from": ".agent/catalog/catalog.v1.json",
        "project": "Siebenwind Lore Engine",
        "version": load_version(),
        "philosophy": "AI-Agnostic Lore Intelligence",
        "lore": {
            "world_name": "Siebenwind",
            "chronology": "Sonnenzirkel",
            "tone": "immersiv, historisch",
            "directories": {
                "wiki": "docs/Siebenwind_Wiki",
                "sources": "Quellen",
            },
        },
        "interface": {
            "cli": "./7w_wiki.py",
            "commands": commands,
            "machine_surfaces": {
                "catalog": ".agent/catalog/catalog.v1.json",
                "tools_manifest": ".agent/config/tools.json",
                "mcp_config": "mcp_config.json",
            },
        },
        "compatibility": {
            "legacy_cli_aliases": ["./7w.py"],
            "root_wiki_tree": "Siebenwind_Wiki",
            "note": "The root wiki tree survives only as a compatibility remnant; docs/Siebenwind_Wiki is the canonical technical tree.",
        },
        "capabilities": {
            "rag": "Oracle (semantic search with explicit source scope)",
            "verification": "Homepage > Quellen > Wiki Pages precedence with historian escalation",
            "audit": "Consistency, pages, and interop diagnostics",
            "interop": "MCP runtime plus generated Codex adapter skills",
        },
        "structure": {
            "technical_wiki_root": "docs/Siebenwind_Wiki/",
            "legacy_wiki_root": "Siebenwind_Wiki/",
            "sources_root": "Quellen/",
            "agent_core": ".agent/",
            "catalog": ".agent/catalog/",
            "codex_adapter": ".agents/skills/",
            "codex_config": ".codex/config.toml",
            "mcp_server": "System/MCP/server.py",
            "published_assets": "docs/assets/",
            "historical_design_assets": "System/Design_Assets/",
        },
        "docs": {
            "changelog": "CHANGELOG.md",
            "task_list": "MASTER_TASK_LIST.md",
            "stats": "docs/Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md",
            "architecture": "docs/architecture.md",
            "interop": "System/Synapse_Board/SY_INTEROP.md",
            "ops_handbook": "System/AGENT_OPERATIONS_HANDBOOK.md",
        },
    }


def main() -> int:
    catalog = load_catalog()
    manifest = build_manifest(catalog)
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {MANIFEST_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
