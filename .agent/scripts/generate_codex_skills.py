#!/usr/bin/env python3
"""
Generate real Codex-native adapter skills from the canonical agent catalog.
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
CATALOG_PATH = REPO_ROOT / ".agent" / "catalog" / "catalog.v1.json"
SKILLS_DIR = REPO_ROOT / ".agents" / "skills"
GENERATED_MARKER = "Generated Codex adapter skill. Do not edit manually."


def load_catalog() -> dict:
    if not CATALOG_PATH.exists():
        raise FileNotFoundError(f"Catalog missing: {CATALOG_PATH}")
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def build_content(surface: dict) -> str:
    source_kind = surface["source_kind"]
    source_label = {
        "workflow": "Canonical workflow",
        "skill": "Canonical skill",
        "runtime": "Canonical runtime surface",
    }.get(source_kind, "Canonical source")

    lines = [
        "---",
        f"name: {surface['name']}",
        f"description: {surface['description']}",
        "---",
        "",
        f"# Codex Skill: {surface['name']}",
        "",
        f"> **{source_label}**: `{surface['source_path']}`",
        f"> **Marker**: {GENERATED_MARKER}",
        "",
        "This adapter is generated from the canonical catalog. Runtime execution stays on `./7w_wiki.py`; `.agent/` remains the source of truth.",
        "",
        "## Primary Runtime Command",
        f"`{surface['primary_command']}`",
        "",
    ]

    if surface["id"] in {"session_start", "session_takeover", "session_handover"}:
        base_command = surface["primary_command"].replace(" --run", "")
        lines.extend(
            [
                "## Execution Modes",
                f"- View workflow: `{base_command}`",
                f"- Execute checklist: `{base_command} --run`",
                "",
            ]
        )

    if surface.get("followup_commands"):
        lines.append("## Follow-up Commands")
        for command in surface["followup_commands"]:
            lines.append(f"- `{command}`")
        lines.append("")

    if surface.get("instructions"):
        lines.append("## Instructions")
        for instruction in surface["instructions"]:
            lines.append(f"- {instruction}")
        lines.append("")

    if surface.get("references"):
        lines.append("## References")
        for reference in surface["references"]:
            lines.append(f"- `{reference}`")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def remove_stale_generated(valid_ids: set[str]) -> list[str]:
    removed: list[str] = []
    if not SKILLS_DIR.exists():
        return removed
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        skill_file = skill_dir / "SKILL.md"
        if not skill_file.exists():
            continue
        try:
            raw = skill_file.read_text(encoding="utf-8")
        except Exception:
            continue
        if GENERATED_MARKER not in raw:
            continue
        if skill_dir.name in valid_ids:
            continue
        shutil.rmtree(skill_dir)
        removed.append(skill_dir.name)
    return removed


def main() -> int:
    catalog = load_catalog()
    codex_skills = catalog.get("surfaces", {}).get("codex", {}).get("skills", [])
    SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    generated_ids: list[str] = []
    for surface in codex_skills:
        target = REPO_ROOT / surface["target_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(build_content(surface), encoding="utf-8")
        generated_ids.append(surface["id"])

    removed = remove_stale_generated(set(generated_ids))
    print(f"Generated {len(generated_ids)} Codex adapter skills.")
    if removed:
        print("Removed stale generated Codex skills:", ", ".join(sorted(removed)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
