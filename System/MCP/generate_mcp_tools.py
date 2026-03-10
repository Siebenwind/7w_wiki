#!/usr/bin/env python3
"""
Generate MCP tools from the typed CLI schema exposed by ./7w_wiki.py --help-json.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

BLACKLIST = {"watch", "start"}
LEGACY_COMPOUND_ALIASES = {
    "mail": {"arg": "mail_args", "mode": "mail_passthrough"},
    "pages": {"arg": "pages_cmd", "raw_args": "raw_args", "mode": "subcommand_passthrough"},
    "archive": {"arg": "archive_cmd", "raw_args": "raw_args", "mode": "subcommand_passthrough"},
    "leitpunkt": {"arg": "leit_cmd", "raw_args": "raw_args", "mode": "subcommand_passthrough"},
}


def extract_cli_schema() -> dict:
    result = subprocess.run(
        [sys.executable, str(REPO_ROOT / "7w_wiki.py"), "--help-json"],
        capture_output=True,
        text=True,
        timeout=10,
        cwd=str(REPO_ROOT),
        check=True,
    )
    return json.loads(result.stdout)


def property_from_arg(arg: dict) -> dict:
    prop = {
        "type": arg.get("type", "string"),
        "description": arg.get("help", ""),
    }
    if arg.get("choices"):
        prop["enum"] = arg["choices"]
    return prop


def build_meta(arguments: list[dict], cli_path: list[str], json_capable: bool) -> dict:
    return {
        "cli_path": cli_path,
        "arguments": arguments,
        "json_capable": json_capable,
    }


def build_tool(name: str, description: str, properties: dict, required: list[str], meta: dict) -> dict:
    return {
        "name": name,
        "description": description,
        "inputSchema": {
            "type": "object",
            "properties": properties,
            "required": required,
        },
        "_meta": meta,
    }


def simple_tool(command: dict) -> dict:
    arguments = command.get("arguments", [])
    properties = {arg["name"]: property_from_arg(arg) for arg in arguments}
    required = [arg["name"] for arg in arguments if arg.get("required")]
    return build_tool(
        f"wiki_{command['name'].replace('-', '_')}",
        command.get("summary") or f"Run ./7w_wiki.py {command['name']}",
        properties,
        required,
        build_meta(arguments, [command["name"]], command.get("json_capable", False)),
    )


def subcommand_tool(command: dict, subcommand: dict) -> dict:
    arguments = subcommand.get("arguments", [])
    properties = {arg["name"]: property_from_arg(arg) for arg in arguments}
    required = [arg["name"] for arg in arguments if arg.get("required")]
    return build_tool(
        f"wiki_{command['name'].replace('-', '_')}_{subcommand['name'].replace('-', '_')}",
        f"{command.get('summary', command['name'])} ({subcommand['name']}). Structured subcommand interface.",
        properties,
        required,
        build_meta(arguments, [command["name"], subcommand["name"]], command.get("json_capable", False)),
    )


def legacy_alias_tool(command: dict) -> dict:
    alias = LEGACY_COMPOUND_ALIASES[command["name"]]
    properties = {
        alias["arg"]: {
            "type": "string",
            "description": (
                f"Deprecated compatibility alias for `{command['name']}`. "
                "Prefer the structured subcommand tools."
            ),
        }
    }
    required: list[str] = []
    if command.get("subcommands") and alias["arg"] != "mail_args":
        properties[alias["arg"]]["enum"] = [sub["name"] for sub in command["subcommands"]]
        required.append(alias["arg"])
    if "raw_args" in alias:
        properties[alias["raw_args"]] = {
            "type": "string",
            "description": "Optional raw trailing arguments for deprecated compatibility use.",
        }
    return build_tool(
        f"wiki_{command['name'].replace('-', '_')}",
        f"Deprecated compatibility alias for `{command['name']}`. Prefer structured tools.",
        properties,
        required,
        {
            "cli_path": [command["name"]],
            "json_capable": command.get("json_capable", False),
            "compat_mode": alias["mode"],
            "compat_arg": alias["arg"],
            "compat_raw_arg": alias.get("raw_args"),
        },
    )


def generate_tools() -> list[dict]:
    schema = extract_cli_schema()
    tools: list[dict] = []
    for command in schema.get("commands", []):
        if command["name"] in BLACKLIST:
            continue
        if command.get("subcommands"):
            for subcommand in command["subcommands"]:
                tools.append(subcommand_tool(command, subcommand))
            if command["name"] in LEGACY_COMPOUND_ALIASES:
                tools.append(legacy_alias_tool(command))
        else:
            tools.append(simple_tool(command))

    tools.append({
        "name": "wiki_mail_quip",
        "description": (
            "Post a non-critical, in-character interagency comment. "
            "Messages are tagged [QUIP] and stored in the dispatch archive. Max 280 characters."
        ),
        "inputSchema": {
            "type": "object",
            "properties": {
                "from_agent": {"type": "string", "description": "Your agent name."},
                "body": {"type": "string", "description": "The quip body.", "maxLength": 280},
            },
            "required": ["from_agent", "body"],
        },
        "_meta": {
            "cli_path": ["mail", "post"],
            "json_capable": False,
            "is_quip": True,
        },
    })
    return tools


def main() -> None:
    tools = generate_tools()
    print(json.dumps(tools, indent=2, ensure_ascii=False))
    print(f"\n[MCP Tools] Generated {len(tools)} tool definitions.", file=sys.stderr)


if __name__ == "__main__":
    main()
