#!/usr/bin/env python3
from __future__ import annotations

import json
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

CONFIG_PATH = REPO_ROOT / ".agent" / "config" / "install_profiles.json"


def load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))


def resolve_toolchain(config: dict, platform: str, mode: str) -> dict:
    toolchain_cfg = config["toolchains"][platform]
    bundled_dir = REPO_ROOT / toolchain_cfg["bundled_dir"]
    bundled_available = bundled_dir.exists()
    if mode == "auto":
        selected = "bundled" if bundled_available else "system"
    else:
        selected = mode
    return {
        "selected_mode": selected,
        "bundled_available": bundled_available,
        "bundled_dir": str(bundled_dir.relative_to(REPO_ROOT)),
        "recommended_core_tools": toolchain_cfg["recommended_core_tools"],
    }


def collect_items(config: dict, profile: str) -> list[Path]:
    return [REPO_ROOT / item for item in config["profiles"][profile]["include"]]


def should_exclude(path: Path, excludes: list[str]) -> bool:
    rel = path.relative_to(REPO_ROOT)
    return any(rel.match(pattern) for pattern in excludes)


def build_manifest(
    config: dict,
    profile: str,
    platform: str,
    toolchain_mode: str,
    dest: Path | None,
) -> dict:
    toolchain = resolve_toolchain(config, platform, toolchain_mode)
    items = collect_items(config, profile)
    return {
        "profile": profile,
        "platform": platform,
        "platform_order": config["platform_order"],
        "exclude_globs": config.get("exclude_globs", []),
        "destination": None if dest is None else str(dest),
        "toolchain": toolchain,
        "items": [
            {
                "path": str(item.relative_to(REPO_ROOT)),
                "exists": item.exists(),
                "type": "dir" if item.is_dir() else "file",
            }
            for item in items
        ],
    }


def install_items(manifest: dict, dest: Path) -> None:
    dest.mkdir(parents=True, exist_ok=True)
    excludes = manifest.get("exclude_globs", [])
    for item in manifest["items"]:
        if not item["exists"]:
            continue
        source = REPO_ROOT / item["path"]
        target = dest / item["path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        if source.is_dir():
            def _ignore(current_dir: str, names: list[str]) -> set[str]:
                ignored = set()
                current = Path(current_dir)
                for name in names:
                    if should_exclude(current / name, excludes):
                        ignored.add(name)
                return ignored

            shutil.copytree(source, target, dirs_exist_ok=True, ignore=_ignore)
        else:
            if should_exclude(source, excludes):
                continue
            shutil.copy2(source, target)
    (dest / "INSTALL_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
