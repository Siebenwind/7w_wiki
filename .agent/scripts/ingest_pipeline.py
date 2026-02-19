#!/usr/bin/env python3
import sys
import argparse
import subprocess
import os
from pathlib import Path

BOLD = "\033[1m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

REPO_ROOT = Path(__file__).parent.parent.parent

def run_script(script_path: str, args: list[str]) -> int:
    executable = sys.executable
    cmd = [executable, os.path.join(REPO_ROOT, script_path)] + args
    
    print(f"\n{BOLD}▶ {script_path} {' '.join(args)}{RESET}")
    result = subprocess.run(cmd)
    return result.returncode

def main() -> int:
    parser = argparse.ArgumentParser(description="Unified Ingest Pipeline for Siebenwind Wiki")
    parser.add_argument("file", help="Path to the markdown file to ingest/process")
    
    args = parser.parse_args()
    target_path = Path(args.file)
    
    if not target_path.exists():
        print(f"Error: Target path {args.file} does not exist.", file=sys.stderr)
        return 1
        
    print(f"{BOLD}🛡️  Starte Ingest-Pipeline fuer: {args.file}{RESET}")
    print(f"Dieser Workflow fuehrt automatisch Linting, Archive-Sync und einen abschliessenden Audit-Check aus.\n")
    
    # 1. Lint and Fix
    print(f"{BOLD}Phase 1: Lint, Score & Sanitize{RESET}")
    rc_lint = run_script("7w_wiki.py", ["lint", args.file, "--fix"])
    if rc_lint != 0:
        print(f"{YELLOW}⚠ Lint-Phase meldete Warnungen. Fortsetzung...{RESET}")
        
    # 2. Archive Sync
    print(f"\n{BOLD}Phase 2: Archive Sync{RESET}")
    rc_sync = run_script("7w_wiki.py", ["archive", "sync"])
    
    # 3. Audit
    print(f"\n{BOLD}Phase 3: Consistency Audit{RESET}")
    rc_audit = run_script("7w_wiki.py", ["audit"])
    
    overall = max(rc_lint, rc_sync, rc_audit)
    
    print("\n" + "="*50)
    if overall == 0:
        print(f"{BOLD}{GREEN}✓ Ingest-Pipeline (Zyklus der Weisheit) erfolgreich abgeschlossen.{RESET}")
    else:
        print(f"{BOLD}{YELLOW}⚠ Ingest-Pipeline mit Warnungen oder Fehlern beendet (Highest Exit: {overall}).{RESET}")
        print(f"Bitte pruefe den finalen Audit-Report auf offene Registrierungs-Inkonsistenzen.")
            
    return overall

if __name__ == "__main__":
    sys.exit(main())
