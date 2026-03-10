#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CLI_PATH = REPO_ROOT / "7w_wiki.py"
TOOLS_JSON_PATH = REPO_ROOT / ".agent" / "config" / "tools.json"

LEGACY_COMPOUND_ALIASES = {
    "mail": {"arg": "mail_args"},
    "pages": {"arg": "pages_cmd", "raw_args": "raw_args"},
    "archive": {"arg": "archive_cmd", "raw_args": "raw_args"},
    "leitpunkt": {"arg": "leit_cmd", "raw_args": "raw_args"},
}


def get_cli_schema() -> dict:
    result = subprocess.run(
        [sys.executable, str(CLI_PATH), "--help-json"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
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


def build_tool(function_name: str, description: str, properties: dict, required: list[str]) -> dict:
    return {
        "type": "function",
        "function": {
            "name": function_name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        },
    }


def build_simple_tool(command: dict) -> dict:
    properties = {}
    required = []
    for arg in command.get("arguments", []):
        properties[arg["name"]] = property_from_arg(arg)
        if arg.get("required"):
            required.append(arg["name"])
    return build_tool(
        f"cli_{command['name'].replace('-', '_')}",
        command.get("summary") or f"Execute the {command['name']} command in 7w_wiki.",
        properties,
        required,
    )


def build_subcommand_tool(command: dict, subcommand: dict) -> dict:
    properties = {}
    required = []
    for arg in subcommand.get("arguments", []):
        properties[arg["name"]] = property_from_arg(arg)
        if arg.get("required"):
            required.append(arg["name"])
    description = (
        f"{command.get('summary', command['name'])} ({subcommand['name']}). "
        "Structured subcommand interface."
    )
    return build_tool(
        f"cli_{command['name'].replace('-', '_')}_{subcommand['name'].replace('-', '_')}",
        description,
        properties,
        required,
    )


def build_legacy_alias(command: dict) -> dict:
    alias = LEGACY_COMPOUND_ALIASES[command["name"]]
    properties = {}
    required = []
    subcommands = [sub["name"] for sub in command.get("subcommands", [])]
    arg_name = alias["arg"]
    properties[arg_name] = {
        "type": "string",
        "description": (
            "Deprecated compatibility alias. Prefer the structured "
            f"`cli_{command['name'].replace('-', '_')}_*` tools."
        ),
    }
    if subcommands and arg_name != "mail_args":
        properties[arg_name]["enum"] = subcommands
        required.append(arg_name)
    if "raw_args" in alias:
        properties[alias["raw_args"]] = {
            "type": "string",
            "description": "Optional raw trailing arguments for deprecated compatibility use.",
        }
    return build_tool(
        f"cli_{command['name'].replace('-', '_')}",
        (
            f"Deprecated compatibility alias for `{command['name']}`. "
            "Prefer the structured subcommand tools."
        ),
        properties,
        required,
    )


def generate_tools(schema: dict) -> list[dict]:
    tools: list[dict] = []
    for command in schema.get("commands", []):
        if command.get("subcommands"):
            for subcommand in command["subcommands"]:
                tools.append(build_subcommand_tool(command, subcommand))
            if command["name"] in LEGACY_COMPOUND_ALIASES:
                tools.append(build_legacy_alias(command))
        else:
            tools.append(build_simple_tool(command))
    return tools


def main() -> int:
    cli_schema = get_cli_schema()
    openai_tools = generate_tools(cli_schema)
    TOOLS_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    TOOLS_JSON_PATH.write_text(json.dumps(openai_tools, indent=2), encoding="utf-8")
    print(f"Successfully wrote {len(openai_tools)} tools to {TOOLS_JSON_PATH.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
