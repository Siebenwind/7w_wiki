#!/usr/bin/env python3
import sys
import argparse
import subprocess
import os

from pathlib import Path

# UI Helpers
BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

REPO_ROOT = Path(__file__).parent.parent.parent

def run_script(script_path: str, args: list[str]) -> int:
    """Helper to run a project script and return its exit code."""
    executable = sys.executable
    cmd = [executable, os.path.join(REPO_ROOT, script_path)] + args
    
    print(f"\n{BOLD}▶ {script_path} {' '.join(args)}{RESET}")
    result = subprocess.run(cmd)
    return result.returncode

def main() -> int:
    parser = argparse.ArgumentParser(description="Unified Lint Pipeline for Siebenwind Wiki")
    parser.add_argument("target", nargs="?", default="Siebenwind_Wiki", help="Path to file or directory to lint")
    parser.add_argument("--fix", action="store_true", help="Auto-fix layout and frontmatter issues")
    parser.add_argument("--json", action="store_true", help="Output raw JSON report (suppresses stdout)")
    
    args = parser.parse_args()
    
    target_path = Path(args.target)
    if not target_path.exists():
        if not args.json:
            print(f"Error: Target path {args.target} does not exist.", file=sys.stderr)
        return 1
        
    if not args.json:
        print(f"{BOLD}🛡️  Starte Lint-Pipeline fuer: {args.target}{RESET}")
        
    # Phase 1: Sanitize (Frontmatter & Layout)
    sanitize_args = [args.target]
    if args.fix:
        sanitize_args.append("--auto")
    
    # We do not pass --json to sanitize yet, as it doesn't support it, but we plan to in Pillar 2.
    # For now, let it print.
    rc_sanitize = run_script(".agent/scripts/wiki_sanitizer.py", sanitize_args)
    
    # Phase 2: Check (Style & Grammar via Lektor)
    rc_check = run_script(".agent/skills/lektor/style_checker.py", [args.target])
    
    # Phase 3: Score (Lore Quality Score) - Only applicable to single files
    rc_score = 0
    if target_path.is_file() and target_path.suffix == ".md":
        rc_score = run_script(".agent/scripts/lore_score_manager.py", [args.target])
    else:
        if not args.json:
            print(f"\n{BOLD}▶ Ueberspringe Score-Berechnung (Nutze dies nur fuer einzelne .md Dateien){RESET}")
        
    overall = max(rc_sanitize, rc_check, rc_score)
    
    if not args.json:
        print("\n" + "="*40)
        if overall == 0:
            print(f"{BOLD}{GREEN}✓ Lint-Pipeline erfolgreich.{RESET}")
        else:
            print(f"{BOLD}{YELLOW}⚠ Lint-Pipeline mit Warnungen oder Fehlern beendet (Exit: {overall}).{RESET}")
            
    return overall

if __name__ == "__main__":
    sys.exit(main())
