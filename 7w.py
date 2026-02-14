#!/usr/bin/env python3
import sys
import subprocess
import argparse
import os

"""
Siebenwind Lore Engine CLI (7w)
Unified entry point for all archival and intelligence tools.
"""

# UI Helpers
BOLD = "\033[1m"
YELLOW = "\033[93m"
RESET = "\033[0m"

def run_script(path, args=[]):
    script_path = os.path.join(os.path.dirname(__file__), path)
    
    # Use venv for oracle scripts if available
    executable = sys.executable
    if "oracle" in path:
        venv_python = os.path.join(os.path.dirname(__file__), ".agent/skills/oracle/venv/bin/python3")
        if os.path.exists(venv_python):
            executable = venv_python
            
    cmd = [executable, script_path] + args
    try:
        subprocess.run(cmd, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {path}: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description="Siebenwind Lore Engine CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Search (Oracle)
    search_parser = subparsers.add_parser("search", help="Semantic search via the Oracle (RAG)")
    search_parser.add_argument("query", help="The search query")
    search_parser.add_argument("--source", choices=["wiki", "quellen"], default="wiki", help="Search target")

    # Stats
    subparsers.add_parser("stats", help="Generate Wiki Statistics and Dashboard")

    # Historian
    hist_parser = subparsers.add_parser("historian", help="Deep Lore Analysis (Workflow)")
    hist_parser.add_argument("query", nargs="?", help="Subject to analyze")

    # Repair
    subparsers.add_parser("repair", help="Interactive repair of links and metadata")

    # Audit
    subparsers.add_parser("audit", help="Run consistency audit (duplicates, orphans)")

    # Index
    index_parser = subparsers.add_parser("index", help="Manage semantic index")
    index_parser.add_argument("--rebuild", action="store_true", help="Full re-indexing")
    index_parser.add_argument("--status", action="store_true", help="Check index status")

    # Advisor (Default)
    subparsers.add_parser("advisor", help="Show system status and recommendations (Default)")

    # Check if no arguments provided, default to advisor
    if len(sys.argv) == 1:
        args = parser.parse_args(["advisor"])
    else:
        args = parser.parse_args()

    if args.command == "search":
        search_args = [args.query]
        if args.source == "quellen":
            search_args.extend(["--source", "quellen"])
        run_script(".agent/skills/oracle/search.py", search_args)

    elif args.command == "advisor":
        run_script(".agent/scripts/advisor.py")

    elif args.command == "stats":
        run_script(".agent/scripts/generate_wiki_stats.py")

    elif args.command == "historian":
        # Historian logic: If query is provided, start a search + analysis briefing
        # If not, just show the workflow instructions.
        if args.query:
            print(f"🏛️  {BOLD}Historiker-Analyse für: {args.query}{RESET}")
            # First, trigger a search to gather context
            search_args = [args.query, "--top", "10", "--source", "all"]
            run_script(".agent/skills/oracle/search.py", search_args)
            print(f"\n💡 {YELLOW}Tipp:{RESET} Nutze den Workflow `/historian` für die tiefe Rekonstruktion.")
        else:
            print(f"📖 {BOLD}Workflow: /historian{RESET}")
            run_script(".agent/workflows/historian.md") # Just show the file

    elif args.command == "repair":
        run_script(".agent/scripts/repair.py")

    elif args.command == "audit":
        run_script(".agent/scripts/register_check.py")

    elif args.command == "index":
        index_args = []
        if args.rebuild:
            index_args.append("--rebuild")
        if args.status:
            index_args.append("--status")
        run_script(".agent/skills/oracle/build_index.py", index_args)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
