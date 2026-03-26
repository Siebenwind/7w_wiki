#!/usr/bin/env python3
"""
wiki_sanitizer.py — Content normalizer for the Siebenwind wiki.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from content_contract import REPO_ROOT, TECHNICAL_WIKI_ROOT, normalize_document, scan_contract


def sanitize_files(target_path: Path, auto_fix: bool = False, json_output: bool = False) -> int:
    report = scan_contract(target_path)
    files = []
    if target_path.is_file():
        files = [target_path]
    elif target_path.exists():
        files = sorted(target_path.rglob("*.md"))

    fixed = 0
    changed_details = []

    for file_path in files:
        try:
            raw = file_path.read_text(encoding="utf-8")
        except Exception:
            continue
        new_raw, changes, _, analysis = normalize_document(raw, file_path)
        if changes:
            changed_details.append(
                {
                    "path": str(file_path.relative_to(REPO_ROOT)),
                    "changes": changes,
                    "analysis": analysis,
                    "fixed": auto_fix,
                }
            )
            if auto_fix and new_raw != raw:
                file_path.write_text(new_raw, encoding="utf-8")
                fixed += 1

    if auto_fix:
        refreshed = scan_contract(target_path)
        refreshed["files_fixed"] = fixed
        refreshed["details"] = changed_details
        refreshed["target"] = str(target_path.relative_to(REPO_ROOT) if target_path.is_absolute() else target_path)
        report = refreshed

    report["files_fixed"] = fixed
    report["details"] = changed_details
    report["target"] = str(target_path.relative_to(REPO_ROOT) if target_path.is_absolute() else target_path)

    if json_output:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Scanning {target_path} for drift-prone wiki contract violations...")
        print(f"Scanned {report['scanned_files']} markdown files.")
        print(f"Violations found: {report['violations_found']}")
        print(f"Files fixed: {fixed}")
        print(f"Split-brain files: {report['split_brain']['issues']}")

    return 1 if report["violations_found"] > 0 else 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize wiki structure, metadata, and drift-prone legacy patterns")
    parser.add_argument("target", nargs="?", default=str(TECHNICAL_WIKI_ROOT), help="Path to file/folder (default: docs/Siebenwind_Wiki)")
    parser.add_argument("--auto", action="store_true", help="Auto-fix violations")
    parser.add_argument("--json", action="store_true", help="Output raw JSON report")
    args = parser.parse_args()

    target = Path(args.target)
    if not target.is_absolute():
        target = (REPO_ROOT / target).resolve()

    return sanitize_files(target, auto_fix=args.auto, json_output=args.json)


if __name__ == "__main__":
    sys.exit(main())
