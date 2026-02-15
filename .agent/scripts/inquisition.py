#!/usr/bin/env python3
import os
import re
import argparse
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).parent.parent.parent
INVENTUR_FILE = REPO_ROOT / "Logs/INVENTUR_QUELLEN.md"
ARCHIVE_INVENTUR_FILE = REPO_ROOT / "Logs/Archive/INVENTUR_QUELLEN.md"
INGESTION_LOG_DIR = REPO_ROOT / "Logs/Ingestion"

# UI Helpers
BOLD = "\033[1m"
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def get_integrated_sources():
    sources = []
    files_to_check = [INVENTUR_FILE, ARCHIVE_INVENTUR_FILE]
    
    for f in files_to_check:
        if not f.exists():
            continue
        
        content = f.read_text(encoding="utf-8")
        lines = content.splitlines()
        for line in lines:
            if "|" in line and ("Integrated" in line or "Integrated" in line):
                parts = [p.strip() for p in line.split("|")]
                if len(parts) >= 3:
                    # Priority check for filename format
                    # Legacy: | Siebenwind Bote 120.md | Integrated |
                    # New: | Bote 118.md | Zeitung | - | Integrated |
                    fname = ""
                    for p in parts:
                        clean_p = p.strip("`").strip()
                        if clean_p.endswith(".md") or clean_p.endswith(".html"):
                            fname = clean_p
                            break
                    
                    if fname:
                        sources.append(fname)
    return sorted(list(set(sources)))

def get_existing_reports():
    if not INGESTION_LOG_DIR.exists():
        return set()
    
    reports = set()
    for f in INGESTION_LOG_DIR.glob("*.md"):
        # Reports are usually [DATE]_[SOURCE].md
        name = f.stem
        if "_" in name:
            source_part = name.split("_", 1)[1].lower()
            reports.add(source_part)
    return reports

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--batch", type=int, default=10)
    parser.add_argument("--audit-only", action="store_true")
    args = parser.parse_args()

    print(f"{BOLD}--- SILICON INQUISITION ---{RESET}")
    
    integrated = get_integrated_sources()
    reports = get_existing_reports()
    
    missing = []
    for src in integrated:
        norm_src = src.replace(".md", "").replace(" ", "_").lower()
        if norm_src not in reports:
            missing.append(src)
            
    print(f"  Geamt Integriert:  {len(integrated)}")
    print(f"  Davon ohne Report: {RED}{len(missing)}{RESET}")
    print("")

    if not missing:
        print(f"{GREEN}🎉 Das Archiv ist vollständig auditiert!{RESET}")
        return

    limit = min(args.batch, len(missing))
    targets = missing[:limit]

    if args.audit_only:
        print(f"{YELLOW}Audit-Modus: Liste der nächsten {limit} Targets:{RESET}")
        for t in targets:
            print(f"  - {t}")
    else:
        print(f"{BOLD}Die Inquisition hat folgende Ziele zur Neueinlesung bestimmt:{RESET}")
        for t in targets:
            print(f"  - {t}")
        print(f"\n👉 {YELLOW}Agentmweisung:{RESET} Bitte verarbeite diese {limit} Quellen gemäß /ingestion_protocol.")

if __name__ == "__main__":
    main()
