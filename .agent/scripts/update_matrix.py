#!/usr/bin/env python3
"""
Regenerate the workflow adapter matrix from workflow interop blocks and the live CLI schema.
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CLI_PATH = REPO_ROOT / "7w_wiki.py"
WORKFLOWS_DIR = REPO_ROOT / ".agent" / "workflows"
MATRIX_FILE = REPO_ROOT / "System" / "Synapse_Board" / "SY_WORKFLOW_CLI_MATRIX.md"

RUNTIME_START = "<!-- BEGIN GENERATED RUNTIME COMMANDS -->"
RUNTIME_END = "<!-- END GENERATED RUNTIME COMMANDS -->"
ROWS_START = "<!-- BEGIN GENERATED ADAPTER ROWS -->"
ROWS_END = "<!-- END GENERATED ADAPTER ROWS -->"

SCOUT_NOTE = (
    "Promoted discovery entrypoint; intentionally first-class for external source discovery. "
    "Backend implementation remains under `.agent/scripts/`."
)


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
    arguments = command.get("arguments", [])
    parts = [name]
    positionals = [arg for arg in arguments if arg.get("kind") == "positional"]
    for arg in positionals:
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


def build_runtime_block(commands: list[dict]) -> str:
    lines = [RUNTIME_START]
    for command in commands:
        lines.append(f"- `{command['name']}`")
    lines.append(RUNTIME_END)
    return "\n".join(lines)


def extract_frontmatter_description(raw: str) -> str:
    match = re.match(r"---\n(.*?)\n---\n", raw, re.DOTALL)
    if not match:
        return ""
    for line in match.group(1).splitlines():
        if line.startswith("description:"):
            return line.split(":", 1)[1].strip()
    return ""


def parse_interop_status(raw: str) -> dict:
    section = re.search(r"## Interop-Status\n(.*?)(?:\n## |\Z)", raw, re.DOTALL)
    data = {
        "runtime_commands": [],
        "method_only": [],
        "method_hints_non_runtime": [],
        "interop_note": "",
        "matrix_status": "",
        "runtime_adapter": "",
    }
    if not section:
        return data

    current = None
    for line in section.group(1).splitlines():
        stripped = line.strip()
        if stripped == "- runtime_commands:":
            current = "runtime_commands"
            continue
        if stripped == "- method_only:":
            current = "method_only"
            continue
        if stripped == "- method_hints_non_runtime:":
            current = "method_hints_non_runtime"
            continue
        if stripped.startswith("- interop_note:"):
            data["interop_note"] = stripped.split(":", 1)[1].strip()
            current = None
            continue
        if stripped.startswith("- matrix_status:"):
            data["matrix_status"] = stripped.split(":", 1)[1].strip()
            current = None
            continue
        if stripped.startswith("- runtime_adapter:"):
            match = re.search(r"`([^`]+)`", stripped)
            data["runtime_adapter"] = match.group(1) if match else stripped.split(":", 1)[1].strip()
            current = None
            continue
        if current and stripped.startswith("- `"):
            match = re.search(r"`([^`]+)`", stripped)
            if match:
                data[current].append(match.group(1))
    return data


def workflow_sort_key(name: str) -> tuple[int, str]:
    priority = {"start": 0, "takeover": 1, "handover": 2, "scout": 3}
    return (priority.get(name, 99), name)


def build_row(workflow_path: Path, command_map: dict[str, dict]) -> str:
    raw = workflow_path.read_text(encoding="utf-8")
    description = extract_frontmatter_description(raw)
    interop = parse_interop_status(raw)
    name = workflow_path.stem
    slash = f"/{name}"
    command = command_map.get(name)
    status = interop["matrix_status"] or ("executable" if command else "method_only")

    if interop["runtime_adapter"]:
        adapter = interop["runtime_adapter"]
    elif command:
        adapter = f"7w_wiki.py {format_command_signature(command).strip('`')}"
    else:
        adapter = " + ".join(interop["runtime_commands"]) if interop["runtime_commands"] else "-"

    note = interop["interop_note"] or description or "Workflow/CLI bridge."
    if name == "scout":
        note = SCOUT_NOTE

    adapter = adapter.replace("|", "\\|")
    note = note.replace("|", "\\|")
    return f"| `/{name}` | {status} | `{adapter}` | {note} |"


def build_rows_block(command_map: dict[str, dict]) -> str:
    workflow_files = sorted(WORKFLOWS_DIR.glob("*.md"), key=lambda path: workflow_sort_key(path.stem))
    lines = [ROWS_START]
    for workflow_path in workflow_files:
        lines.append(build_row(workflow_path, command_map))
    lines.append(ROWS_END)
    return "\n".join(lines)


def replace_section(content: str, start_regex: str, end_regex: str, new_block: str) -> str:
    pattern = re.compile(start_regex + r".*?" + end_regex, re.DOTALL)
    replacement = lambda match: match.group(1) + "\n" + new_block + "\n" + match.group(2)
    updated, count = pattern.subn(replacement, content, count=1)
    if count != 1:
        raise RuntimeError("Managed section not found in SY_WORKFLOW_CLI_MATRIX.md")
    return updated


def main() -> int:
    schema = load_cli_schema()
    commands = schema.get("commands", [])
    command_map = {command["name"]: command for command in commands}
    runtime_block = build_runtime_block(commands)
    rows_block = build_rows_block(command_map)

    content = MATRIX_FILE.read_text(encoding="utf-8")
    content = replace_section(
        content,
        r"(## Runtime Commands\n)",
        r"(\n## Adaptermatrix)",
        runtime_block,
    )
    content = replace_section(
        content,
        r"(\| Workflow-Slash \| Status \| Runtime-Adapter \| Hinweis \|\n\|---\|---\|---\|---\|\n)",
        r"(\n## Regel)",
        rows_block,
    )
    MATRIX_FILE.write_text(content, encoding="utf-8")
    print(f"Regenerated {MATRIX_FILE.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
