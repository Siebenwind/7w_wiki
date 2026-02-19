#!/usr/bin/env python3
"""
wiki_sanitizer.py — Enforces Siebenwind Wiki v2.1 Standards.

Checks:
1. YAML/H1 Sync: Ensures the 'title' in frontmatter matches the first # Heading.
"""

import os
import re
import argparse
import json
from pathlib import Path

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
WIKI_DIR = PROJECT_ROOT / "Siebenwind_Wiki"

def sanitize_files(target_path: Path, auto_fix: bool = False, json_output: bool = False):
    if not json_output:
        print(f"Scanning {target_path} for v2.1 violations...")
        
    if target_path.is_file():
        files = [target_path]
    else:
        files = list(target_path.rglob("*.md"))
        
    violations = 0
    fixed = 0
    details = []

    for file_path in files:
        try:
            content = file_path.read_text(encoding="utf-8")
        except Exception:
            continue

        # Extract Frontmatter Title
        fm_match = re.search(r'^---\n.*?title:\s*(.*?)\n.*?---', content, re.DOTALL)
        if not fm_match:
            continue
        
        fm_title = fm_match.group(1).strip().strip('"').strip("'")
        
        # Extract H1 Title
        # Look for first line starting with # 
        # (after frontmatter, but regex finds first match in string usually)
        # We need to be careful not to match # in code blocks or comments if possible,
        # but for simple wiki files, first # line is usually the title.
        
        # Split content to find text after frontmatter
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue
            
        body = parts[2]
        h1_match = re.search(r'^\s*#\s+(.*)', body, re.MULTILINE)
        
        if not h1_match:
             # print(f"{YELLOW}Warning:{RESET} {file_path.name} has no H1 heading.")
             continue
             
        h1_title = h1_match.group(1).strip()
        
        # Remove wiki links formatting from H1 for comparison if present
        # e.g. # [[Title]] -> Title
        h1_clean = re.sub(r'\[\[(.*?)(?:\|.*?)?\]\]', r'\1', h1_title)
        
        # Compare
        # We normalize underscores to spaces for comparison if needed, or strict match.
        # Strict match is better for "Sync".
        if fm_title != h1_clean:
            violations += 1
            is_fixed = False
            
            if not json_output:
                print(f"{YELLOW}Mismatch in {file_path.name}:{RESET}")
                print(f"  YAML: '{fm_title}'")
                print(f"  H1:   '{h1_clean}'")
            
            if auto_fix:
                new_content = re.sub(r'^(title:\s*).*$', f'\\1{h1_clean}', content, count=1, flags=re.MULTILINE)
                file_path.write_text(new_content, encoding="utf-8")
                
                if not json_output:
                    print(f"  {GREEN}Fixed (YAML updated to match H1){RESET}")
                fixed += 1
                is_fixed = True
                
            details.append({
                "file": file_path.name,
                "yaml_title": fm_title,
                "h1_title": h1_clean,
                "fixed": is_fixed
            })

    if json_output:
        print(json.dumps({
            "scanned_files": len(files),
            "violations_found": violations,
            "files_fixed": fixed,
            "details": details
        }, indent=2))
    else:
        print(f"\nScanned {len(files)} files.")
        print(f"{RED}{violations} violations found.{RESET}")
        if auto_fix:
            print(f"{GREEN}{fixed} files fixed.{RESET}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("target", nargs="?", default=str(WIKI_DIR), help="Path to file/folder (default: Siebenwind_Wiki)")
    parser.add_argument("--auto", action="store_true", help="Auto-fix violations")
    parser.add_argument("--json", action="store_true", help="Output raw JSON report (suppresses stdout)")
    args = parser.parse_args()
    
    sanitize_files(Path(args.target), args.auto, args.json)
