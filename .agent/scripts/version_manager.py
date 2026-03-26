#!/usr/bin/env python3
"""
Version Manager: Reads VERSION file and propagates to all known locations.
Usage: ./7w_wiki.py version [--bump minor|major|patch] [--dry-run]
"""
import argparse
import re
import sys
from pathlib import Path

from content_contract import TECHNICAL_WIKI_ROOT

REPO_ROOT = Path(__file__).resolve().parents[2]
VERSION_FILE = REPO_ROOT / "VERSION"

# Files that contain version strings to update
TARGETS = [
    {
        "file": REPO_ROOT / "MASTER_TASK_LIST.md",
        "pattern": r"(\*\*Wiki-Standard:\*\*\s+v)[\d.]+(\s+\(.*?\))?",
        "replacement": r"\g<1>{version} ({label})",
    },
    {
        "file": TECHNICAL_WIKI_ROOT / "index.md",
        "pattern": r"Reconstruction_v[\d.]+-",
        "replacement": "v{version}-",
    },
]

BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def read_version() -> str:
    if not VERSION_FILE.exists():
        print("VERSION file not found!", file=sys.stderr)
        sys.exit(1)
    return VERSION_FILE.read_text().strip()


def bump_version(current: str, bump_type: str) -> str:
    parts = current.split(".")
    while len(parts) < 3:
        parts.append("0")

    major, minor, patch = int(parts[0]), int(parts[1]), int(parts[2])

    if bump_type == "major":
        major += 1
        minor = 0
        patch = 0
    elif bump_type == "minor":
        minor += 1
        patch = 0
    elif bump_type == "patch":
        patch += 1

    return f"{major}.{minor}.{patch}" if patch > 0 else f"{major}.{minor}"


def propagate_version(version: str, label: str, dry_run: bool) -> int:
    updated = 0
    for target in TARGETS:
        fpath = target["file"]
        if not fpath.exists():
            print(f"  ⚠ Skip (not found): {fpath.relative_to(REPO_ROOT)}")
            continue

        text = fpath.read_text(encoding="utf-8")
        repl = target["replacement"].format(version=version, label=label)
        new_text = re.sub(target["pattern"], repl, text, count=1)

        if new_text != text:
            if dry_run:
                print(f"  [DRY RUN] Would update: {fpath.relative_to(REPO_ROOT)}")
            else:
                fpath.write_text(new_text, encoding="utf-8")
                print(f"  ✓ Updated: {fpath.relative_to(REPO_ROOT)}")
            updated += 1
        else:
            print(f"  — No change: {fpath.relative_to(REPO_ROOT)}")

    return updated


def main():
    parser = argparse.ArgumentParser(description="Version Manager")
    parser.add_argument("--bump", choices=["major", "minor", "patch"], help="Bump version")
    parser.add_argument("--label", default="Inter-AI Compliant", help="Version label/subtitle")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    parser.add_argument("--json", action="store_true", help="Output version as JSON")
    args = parser.parse_args()

    current = read_version()

    if args.json:
        import json
        print(json.dumps({"version": current, "file": str(VERSION_FILE)}))
        return 0

    if args.bump:
        new_version = bump_version(current, args.bump)
        print(f"{BOLD}Version Bump:{RESET} v{current} → v{new_version}")

        if not args.dry_run:
            VERSION_FILE.write_text(new_version + "\n")

        current = new_version
    else:
        print(f"{BOLD}Current Version:{RESET} v{current}")

    print(f"\n{BOLD}Propagating to targets:{RESET}")
    updated = propagate_version(current, args.label, args.dry_run)

    if args.dry_run:
        print(f"\n{YELLOW}DRY RUN: {updated} files would be updated.{RESET}")
    else:
        print(f"\n{GREEN}✓ v{current} propagated to {updated} files.{RESET}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
