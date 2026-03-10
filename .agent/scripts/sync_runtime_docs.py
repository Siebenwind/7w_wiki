#!/usr/bin/env python3
"""
Sync runtime command inventories and registry tables from the live CLI schema.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CLI_PATH = REPO_ROOT / "7w_wiki.py"

AGENTS_FILE = REPO_ROOT / "AGENTS.md"
INTEROP_FILE = REPO_ROOT / "System" / "Synapse_Board" / "SY_INTEROP.md"
HANDBOOK_FILE = REPO_ROOT / "System" / "AGENT_OPERATIONS_HANDBOOK.md"

TABLE_START = "<!-- BEGIN GENERATED COMMAND REGISTRY -->"
TABLE_END = "<!-- END GENERATED COMMAND REGISTRY -->"
LIST_START = "<!-- BEGIN GENERATED RUNTIME COMMAND LIST -->"
LIST_END = "<!-- END GENERATED RUNTIME COMMAND LIST -->"


def load_cli_schema() -> dict:
    result = subprocess.run(
        [sys.executable, str(CLI_PATH), "--help-json"],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=True,
    )
    return json.loads(result.stdout)


def format_command_signature(command: dict) -> str:
    name = command["name"]
    parts = [name]
    for arg in command.get("arguments", []):
        if arg.get("kind") != "positional":
            continue
        arg_name = arg["name"].replace("_", "-")
        token = f"<{arg_name}>"
        if not arg.get("required", False):
            token = f"[{arg_name}]"
        if arg.get("nargs") == "REMAINDER":
            token = f"[{arg_name}...]"
        parts.append(token)
    if command.get("subcommands"):
        sub_names = "|".join(sub["name"] for sub in command["subcommands"])
        parts.append(f"<{sub_names}>")
    if command.get("supports_run_mode"):
        parts.append("[--run]")
    return f"`{' '.join(parts)}`"


def build_agents_table(commands: list[dict]) -> str:
    lines = [TABLE_START, "| Command | Purpose | Context |", "| :--- | :--- | :--- |"]
    for command in commands:
        signature = format_command_signature(command)
        purpose = command.get("summary", "").replace("|", "\\|")
        context = f"`{command.get('context', '')}`"
        lines.append(f"| {signature} | {purpose} | {context} |")
    lines.append(TABLE_END)
    return "\n".join(lines)


def build_runtime_list(commands: list[dict]) -> str:
    lines = [LIST_START]
    for command in commands:
        lines.append(f"- `{command['name']}`")
    lines.append(LIST_END)
    return "\n".join(lines)


def replace_section(content: str, start_regex: str, end_regex: str, new_block: str) -> str:
    import re

    pattern = re.compile(start_regex + r".*?" + end_regex, re.DOTALL)
    replacement = lambda match: match.group(1) + "\n" + new_block + "\n" + match.group(2)
    updated, count = pattern.subn(replacement, content, count=1)
    if count != 1:
        raise RuntimeError("Managed section not found while syncing runtime docs.")
    return updated


def sync_agents(commands: list[dict]) -> None:
    content = AGENTS_FILE.read_text(encoding="utf-8")
    table = build_agents_table(commands)
    content = replace_section(
        content,
        r"(## 🛠️ Command Registry \(Executable Capabilities\)\n\nUse `\./7w_wiki\.py <command>` for all operations\.\n\n)",
        r"(\n## 📂 Documentation Map)",
        table,
    )
    AGENTS_FILE.write_text(content, encoding="utf-8")


def sync_runtime_list(path: Path, start_regex: str, end_regex: str, commands: list[dict]) -> None:
    content = path.read_text(encoding="utf-8")
    runtime_list = build_runtime_list(commands)
    content = replace_section(content, start_regex, end_regex, runtime_list)
    path.write_text(content, encoding="utf-8")


def main() -> int:
    schema = load_cli_schema()
    commands = schema.get("commands", [])
    sync_agents(commands)
    sync_runtime_list(
        INTEROP_FILE,
        r"(## Norm 3: Command Registry \(Single Source\)\nDie operative Kommandoliste lautet aktuell:\n)",
        r"(\n\nBei CLI-Aenderungen muss diese Liste in derselben Session synchronisiert werden\.)",
        commands,
    )
    sync_runtime_list(
        HANDBOOK_FILE,
        r"(## Runtime Commands\n)",
        r"(\n## Maintainer-Leitpunkt \(Menschliche Steuerung\))",
        commands,
    )
    print("Synced AGENTS.md, SY_INTEROP.md, and AGENT_OPERATIONS_HANDBOOK.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
