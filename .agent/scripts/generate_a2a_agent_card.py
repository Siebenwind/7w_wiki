#!/usr/bin/env python3
"""
Generate a discovery-only agent card from the canonical catalog.
"""
from __future__ import annotations

import json
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = REPO_ROOT / ".agent" / "catalog" / "catalog.v1.json"
AGENT_CARD_PATH = REPO_ROOT / "docs" / ".well-known" / "agent.json"


def load_catalog() -> dict:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def main() -> int:
    catalog = load_catalog()
    codex_skills = catalog.get("surfaces", {}).get("codex", {}).get("skills", [])
    workflows = catalog.get("workflows", [])

    card = {
        "schemaVersion": "0.2.5",
        "protocol": "discovery-only",
        "name": "Siebenwind Wiki",
        "description": (
            "Cross-platform multi-agent librarian system for the Siebenwind Wiki. "
            "Canonical runtime lives on ./7w_wiki.py and the MCP server; Codex skills are derived adapters."
        ),
        "url": "https://siebenwind.github.io/7w_wiki/",
        "documentationUrl": "https://siebenwind.github.io/7w_wiki/Agenten/",
        "preferredTransport": "mcp",
        "transports": [
            {
                "type": "mcp",
                "entrypoint": "./7w_wiki.py mcp",
                "config": "mcp_config.json",
            }
        ],
        "capabilities": {
            "mcp": True,
            "codex_skills": True,
            "a2a_transport": False,
        },
        "skills": [
            {
                "id": skill["id"],
                "name": skill["name"],
                "description": skill["description"],
            }
            for skill in codex_skills
        ],
        "workflows": [
            {
                "id": workflow["id"],
                "name": workflow["name"],
                "primary_command": workflow.get("interop", {}).get("primary_command", ""),
            }
            for workflow in workflows
        ],
        "metadata": {
            "catalog": ".agent/catalog/catalog.v1.json",
            "generatedAt": catalog.get("generated_at"),
            "phase": "phase1-codex-plus-mcp",
        },
    }

    AGENT_CARD_PATH.parent.mkdir(parents=True, exist_ok=True)
    AGENT_CARD_PATH.write_text(json.dumps(card, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {AGENT_CARD_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
