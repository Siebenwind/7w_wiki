#!/usr/bin/env python3
"""
MCP Tool Generator — Auto-Extraction Pipeline

Reads the CLI schema from `./7w_wiki.py --help-json` and generates
MCP-compatible tool definitions for the Siebenwind Wiki server.

This script is called at server startup — never maintain tools manually.
"""

import json
import subprocess
import sys
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

# Commands that should NOT be exposed as MCP tools
# (interactive workflows that require terminal input)
BLACKLIST = {"watch", "start"}

# Commands where --json flag should be auto-injected for structured output
JSON_CAPABLE = {"advisor", "audit", "sanitize", "stats", "search", "check", "lint", "version"}

# Human-readable descriptions for commands missing them in argparse
DESCRIPTIONS = {
    "advisor": "Show system status, health checks, and recommended next actions.",
    "search": "Semantic RAG search (Oracle) across wiki and source corpus.",
    "audit": "Run consistency audit: duplicates, orphans, broken links.",
    "repair": "Interactive or automatic repair of audit findings.",
    "sanitize": "Structural normalization: layout, H1, frontmatter alignment.",
    "test": "Run interoperability and clean-state test suites.",
    "stats": "Generate reader-facing wiki statistics and machine snapshot.",
    "mail": "Agent-to-agent messaging via Synapse Board dispatch system.",
    "check": "Professional style and grammar check (Lektor).",
    "score": "Calculate Lore Quality Score (LQS) for a markdown file.",
    "lint": "Comprehensive lint pipeline: Sanitizer + Style Check + Lore Score.",
    "inquisition": "Batch ingestion of legacy sources (Silicon Inquisition).",
    "ingest": "Run full ingest pipeline: Lint → Archive Sync → Audit.",
    "translate": "Translate Falandric texts or manage dictionaries.",
    "index": "Manage the semantic search index (rebuild, status).",
    "index-pages": "Generate index.md for all wiki categories.",
    "pages": "Build and validate GitHub Pages documentation.",
    "historian": "Deep lore analysis — search + analysis briefing.",
    "scout": "Deep-scan external forum boards for signals.",
    "archive": "Manage wiki archive: sync symlinks, rotate logs, unpack.",
    "version": "Show or bump the wiki standard version.",
    "tech": "Show Technician workflow or regenerate tools manifest.",
    "antigravity": "Show Antigravity core workflow (default protocol).",
    "leitpunkt": "Manage the human maintainer standpoint.",
    "takeover": "Show or run the session takeover protocol.",
    "handover": "Show or run the session handover protocol.",
}


def extract_cli_schema() -> dict:
    """Call ./7w_wiki.py --help-json and parse the result."""
    try:
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "7w_wiki.py"), "--help-json"],
            capture_output=True, text=True, timeout=10, cwd=str(REPO_ROOT)
        )
        if result.returncode != 0:
            print(f"[MCP Tools] CLI --help-json failed: {result.stderr}", file=sys.stderr)
            return {"commands": []}
        return json.loads(result.stdout)
    except Exception as e:
        print(f"[MCP Tools] Error extracting CLI schema: {e}", file=sys.stderr)
        return {"commands": []}


def command_to_tool_def(cmd: dict) -> dict | None:
    """Convert a CLI command definition to an MCP tool definition."""
    name = cmd["name"]

    if name in BLACKLIST:
        return None

    description = cmd.get("description") or DESCRIPTIONS.get(name, f"Run ./7w_wiki.py {name}")

    # Build input schema from arguments
    properties = {}
    required_args = []

    for arg in cmd.get("arguments", []):
        arg_name = arg["name"]
        if arg_name in ("help",):
            continue

        prop = {
            "type": "string",
            "description": arg.get("help", ""),
        }

        # Detect boolean vs. value flags
        # Flags that take a value argument (not store_true)
        VALUE_FLAG_NAMES = {
            "suite", "timeout", "from_agent", "to_agent", "batch",
            "label", "pages", "keep_days", "config", "archive_name",
            "note", "agent",
        }
        if arg.get("flags") and not arg.get("choices"):
            if any(f.startswith("--") for f in arg["flags"]):
                if arg_name in VALUE_FLAG_NAMES:
                    # This flag takes a value, keep as string
                    pass
                else:
                    prop["type"] = "boolean"
                    prop["description"] = arg.get("help", f"Enable {arg_name}")

        # Add choices as enum
        if arg.get("choices"):
            prop["enum"] = arg["choices"]

        properties[arg_name] = prop

        if arg.get("required"):
            required_args.append(arg_name)

    tool_def = {
        "name": f"wiki_{name.replace('-', '_')}",
        "description": description,
        "inputSchema": {
            "type": "object",
            "properties": properties,
        }
    }

    if required_args:
        tool_def["inputSchema"]["required"] = required_args

    # Metadata for the server
    tool_def["_meta"] = {
        "cli_command": name,
        "json_capable": name in JSON_CAPABLE,
    }

    return tool_def


def generate_tools() -> list[dict]:
    """Generate all MCP tool definitions from CLI schema."""
    schema = extract_cli_schema()
    tools = []

    for cmd in schema.get("commands", []):
        tool = command_to_tool_def(cmd)
        if tool:
            tools.append(tool)

    # Add the special mail_quip convenience tool
    tools.append({
        "name": "wiki_mail_quip",
        "description": (
            "Post a non-critical, in-character interagency comment. "
            "Used for humor, observations, and personality between agents. "
            "Messages are tagged [QUIP] and stored in the dispatch archive. "
            "Max 280 characters. You ARE encouraged to use this."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "from_agent": {
                    "type": "string",
                    "description": "Your agent name (e.g. 'Antigravity', 'Historiker', 'Lektor')"
                },
                "body": {
                    "type": "string",
                    "description": "The quip. Max 280 characters. Be witty.",
                    "maxLength": 280
                }
            },
            "required": ["from_agent", "body"]
        },
        "_meta": {
            "cli_command": "mail",
            "is_quip": True,
            "json_capable": False,
        }
    })

    return tools


def main():
    """Print generated tools as JSON."""
    tools = generate_tools()
    print(json.dumps(tools, indent=2, ensure_ascii=False))
    print(f"\n[MCP Tools] Generated {len(tools)} tool definitions.", file=sys.stderr)


if __name__ == "__main__":
    main()
