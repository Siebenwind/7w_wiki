#!/usr/bin/env python3
"""
Sync runtime command inventories and registry tables from the live CLI schema.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CLI_PATH = REPO_ROOT / "7w_wiki.py"

AGENTS_FILE = REPO_ROOT / "AGENTS.md"
INTEROP_FILE = REPO_ROOT / "System" / "Synapse_Board" / "SY_INTEROP.md"
HANDBOOK_FILE = REPO_ROOT / "System" / "AGENT_OPERATIONS_HANDBOOK.md"
DRIFT_CONTRACT_FILE = REPO_ROOT / "System" / "Synapse_Board" / "SY_DRIFT_PAGES_CONTRACT.md"
WORKFLOW_FILES = [
    REPO_ROOT / ".agent" / "workflows" / "start.md",
    REPO_ROOT / ".agent" / "workflows" / "tech_master.md",
    REPO_ROOT / ".agent" / "workflows" / "qa_master.md",
    REPO_ROOT / ".agent" / "workflows" / "handover.md",
]

TABLE_START = "<!-- BEGIN GENERATED COMMAND REGISTRY -->"
TABLE_END = "<!-- END GENERATED COMMAND REGISTRY -->"
LIST_START = "<!-- BEGIN GENERATED RUNTIME COMMAND LIST -->"
LIST_END = "<!-- END GENERATED RUNTIME COMMAND LIST -->"
CONTRACT_REF_START = "<!-- BEGIN GENERATED DRIFT CONTRACT REFERENCE -->"
CONTRACT_REF_END = "<!-- END GENERATED DRIFT CONTRACT REFERENCE -->"


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


def build_contract_reference(path: Path) -> str:
    relative_contract = Path(os.path.relpath(DRIFT_CONTRACT_FILE, start=path.parent))
    lines = [
        "> Generated reference block. The surrounding narrative text remains manually maintained.",
        f"> Canonical contract: [{DRIFT_CONTRACT_FILE.name}]({relative_contract.as_posix()})",
        ">",
        "> - Epistemic precedence: `Homepage > Quellen > Wiki Pages`.",
        "> - `docs/Siebenwind_Wiki/` is the technical edit/publish tree, not the highest truth source.",
        "> - Technical drift is validated via `./7w_wiki.py sanitize`, `./7w_wiki.py audit`, and `./7w_wiki.py pages validate --json [--strict-links]`.",
        "> - `--strict` hardens the MkDocs build; `--strict-links` is the hard unresolved-link gate.",
        "> - Generated command registries are synced by `./7w_wiki.py tech --sync-docs` / `--sync-interop`; narrative rules live in the canonical contract.",
    ]
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


def sync_contract_reference(path: Path) -> bool:
    import re

    content = path.read_text(encoding="utf-8")
    if CONTRACT_REF_START not in content or CONTRACT_REF_END not in content:
        return False
    pattern = re.compile(
        rf"({re.escape(CONTRACT_REF_START)}\n).*?(\n{re.escape(CONTRACT_REF_END)})",
        re.DOTALL,
    )
    replacement = lambda match: match.group(1) + build_contract_reference(path) + match.group(2)
    content, count = pattern.subn(replacement, content, count=1)
    if count != 1:
        raise RuntimeError(f"Managed contract reference not found while syncing {path}.")
    path.write_text(content, encoding="utf-8")
    return True


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
    synced_contract_refs = []
    for path in [AGENTS_FILE, INTEROP_FILE, HANDBOOK_FILE, *WORKFLOW_FILES]:
        if path.exists() and sync_contract_reference(path):
            synced_contract_refs.append(str(path.relative_to(REPO_ROOT)))
    print("Synced AGENTS.md, SY_INTEROP.md, and AGENT_OPERATIONS_HANDBOOK.md")
    if synced_contract_refs:
        print("Synced drift contract references in:")
        for entry in synced_contract_refs:
            print(f"  - {entry}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
