#!/usr/bin/env python3
"""
Generate Codex-facing workflow bridge skills from workflow interop metadata.
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
WORKFLOWS_DIR = REPO_ROOT / ".agent" / "workflows"
BRIDGES_DIR = REPO_ROOT / ".agents" / "skills"

GENERATED_MARKER = "Generated workflow bridge. Do not edit manually."


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
        "codex_bridge_name": "",
        "codex_bridge_enabled": False,
        "codex_bridge_summary": "",
        "codex_bridge_primary_command": "",
        "codex_bridge_followups": [],
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
        if stripped == "- codex_bridge_followups:":
            current = "codex_bridge_followups"
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
        if stripped.startswith("- codex_bridge_name:"):
            data["codex_bridge_name"] = stripped.split(":", 1)[1].strip()
            current = None
            continue
        if stripped.startswith("- codex_bridge_enabled:"):
            data["codex_bridge_enabled"] = stripped.split(":", 1)[1].strip().lower() == "true"
            current = None
            continue
        if stripped.startswith("- codex_bridge_summary:"):
            data["codex_bridge_summary"] = stripped.split(":", 1)[1].strip()
            current = None
            continue
        if stripped.startswith("- codex_bridge_primary_command:"):
            match = re.search(r"`([^`]+)`", stripped)
            data["codex_bridge_primary_command"] = match.group(1) if match else stripped.split(":", 1)[1].strip()
            current = None
            continue
        if current:
            if not stripped:
                continue
            if re.match(r"^\s{2,}- `", line):
                match = re.search(r"`([^`]+)`", stripped)
                if match:
                    data[current].append(match.group(1))
                continue
            current = None
    return data


def bridge_title(name: str) -> str:
    return name.replace("_", " ").strip().title()


def build_bridge_content(
    workflow_name: str,
    workflow_rel: str,
    description: str,
    interop: dict,
) -> str:
    bridge_name = interop["codex_bridge_name"]
    title = bridge_title(bridge_name)
    summary = interop["codex_bridge_summary"] or description or f"Codex bridge for /{workflow_name}."
    primary_command = interop["codex_bridge_primary_command"] or interop["runtime_adapter"]
    followups = interop["codex_bridge_followups"] or interop["runtime_commands"][:3]

    lines = [
        "---",
        f"name: {title}",
        f"description: {summary}",
        "---",
        "",
        f"# Workflow Bridge: /{workflow_name}",
        "",
        f"> **Wrapper for**: `{workflow_rel}`",
        f"> **Marker**: {GENERATED_MARKER}",
        "",
        "This is a generated Codex-facing workflow bridge. Runtime execution must stay on `./7w_wiki.py`.",
        "",
    ]

    if primary_command:
        lines.extend(
            [
                "## Primary Runtime Command",
                f"`./{primary_command}`" if not primary_command.startswith("./") else f"`{primary_command}`",
                "",
            ]
        )

    if workflow_name in {"start", "takeover", "handover"}:
        lines.extend(
            [
                "## Execution Mode",
                f"- View workflow: `./7w_wiki.py {workflow_name}`",
                f"- Execute checklist: `./7w_wiki.py {workflow_name} --run`",
                "",
            ]
        )

    if workflow_name == "forum_search":
        lines.extend(
            [
                "## Supported Board Scopes",
                "- `bekanntmachungen`",
                "- `news`",
                "",
                "## Comparison Target",
                "- `Quellen/Forum/...`",
                "",
            ]
        )

    if followups:
        lines.append("## Follow-up Commands")
        for command in followups:
            rendered = command if command.startswith("./") else f"./{command}"
            lines.append(f"- `{rendered}`")
        lines.append("")

    lines.extend(
        [
            "## Usage Rule",
            f"Read `{workflow_rel}` for the authoritative process. Do not guess workflow semantics from this bridge file alone.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def remove_stale_generated_bridges(valid_names: set[str]) -> list[str]:
    removed: list[str] = []
    if not BRIDGES_DIR.exists():
        return removed
    for bridge_dir in BRIDGES_DIR.iterdir():
        if not bridge_dir.is_dir():
            continue
        skill_file = bridge_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        try:
            raw = skill_file.read_text(encoding="utf-8")
        except Exception:
            continue
        if GENERATED_MARKER not in raw:
            continue
        if bridge_dir.name in valid_names:
            continue
        shutil.rmtree(bridge_dir)
        removed.append(bridge_dir.name)
    return removed


def main() -> int:
    BRIDGES_DIR.mkdir(parents=True, exist_ok=True)
    generated: list[str] = []

    for workflow_path in sorted(WORKFLOWS_DIR.glob("*.md")):
        raw = workflow_path.read_text(encoding="utf-8")
        interop = parse_interop_status(raw)
        if not interop["codex_bridge_enabled"]:
            continue

        bridge_name = interop["codex_bridge_name"].strip()
        if not bridge_name:
            raise RuntimeError(f"{workflow_path.name} is codex_bridge_enabled but missing codex_bridge_name")

        description = extract_frontmatter_description(raw)
        workflow_rel = str(workflow_path.relative_to(REPO_ROOT))
        content = build_bridge_content(workflow_path.stem, workflow_rel, description, interop)

        bridge_dir = BRIDGES_DIR / bridge_name
        bridge_dir.mkdir(parents=True, exist_ok=True)
        (bridge_dir / "SKILL.md").write_text(content, encoding="utf-8")
        generated.append(bridge_name)

    removed = remove_stale_generated_bridges(set(generated))
    print(f"Generated {len(generated)} workflow bridges.")
    if removed:
        print("Removed stale workflow bridges:", ", ".join(sorted(removed)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
