#!/usr/bin/env python3
import sys
import subprocess
import argparse
import os

"""
Siebenwind Lore Engine CLI (7w)
Unified entry point for all archival and intelligence tools.
"""

# --- GLOBAL CACHE REDIRECTION (For Sandbox compatibility) ---
# Ensure models and caches are stored project-local
REPO_ROOT = os.path.dirname(os.path.abspath(__file__))
MODEL_CACHE = os.path.join(REPO_ROOT, ".agent/data/models")
os.makedirs(MODEL_CACHE, exist_ok=True)

os.environ["HF_HOME"] = os.path.join(MODEL_CACHE, "huggingface")
os.environ["HF_HUB_CACHE"] = os.path.join(MODEL_CACHE, "huggingface/hub")
os.environ["SENTENCE_TRANSFORMERS_HOME"] = MODEL_CACHE
os.environ["XDG_CACHE_HOME"] = os.path.join(MODEL_CACHE, "xdg_cache")
os.environ["TOKENIZERS_PARALLELISM"] = "false"

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

def view_workflow(name):
    path = os.path.join(os.path.dirname(__file__), f".agent/workflows/{name}.md")
    if os.path.exists(path):
        with open(path, 'r') as f:
            print(f.read())
    else:
        print(f"Workflow {name} not found at {path}")

def main():
    parser = argparse.ArgumentParser(description="Siebenwind Lore Engine CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Search (Oracle)
    search_parser = subparsers.add_parser("search", help="Semantic search via the Oracle (RAG)")
    search_parser.add_argument("query", help="The search query")
    search_parser.add_argument("--source", choices=["wiki", "quellen", "all"], default="wiki", help="Search target")
    # Add remnant args to pass through
    search_parser.add_argument('remaining', nargs=argparse.REMAINDER, help="Additional arguments for search.py")

    # Stats
    subparsers.add_parser("stats", help="Generate Wiki Statistics and Dashboard")

    # Start (Onboarding)
    subparsers.add_parser("start", help="Start here (Onboarding & Options)")

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

    # Index Pages
    subparsers.add_parser("index-pages", help="Automatically generate index.md files for all wiki categories")

    # Advisor (Default)
    subparsers.add_parser("advisor", help="Show system status and recommendations (Default)")

    # Inquisition (Great Re-Ingestion)
    inq_parser = subparsers.add_parser("inquisition", help="Great Re-Ingestion of legacy sources (Silicon Inquisition)")
    inq_parser.add_argument("--batch", type=int, default=10, help="Number of sources to process in this run")
    inq_parser.add_argument("--audit-only", action="store_true", help="Only list missing reports without processing")

    # Archive Management
    archive_parser = subparsers.add_parser("archive", help="Manage Wiki Archive (Symlinks, Research Board)")
    archive_sub = archive_parser.add_subparsers(dest="archive_cmd")
    archive_sub.add_parser("sync", help="Synchronize reports and board into the docs directory")

    # Agent Messaging (Dispatch)

    # Check if no arguments provided, default to advisor
    if len(sys.argv) == 1:
        args = parser.parse_args(["advisor"])
    else:
        args = parser.parse_args()

    if args.command == "search":
        search_args = [args.query]
        if args.source:
            search_args.extend(["--source", args.source])
        if args.remaining:
            search_args.extend(args.remaining)
        run_script(".agent/skills/oracle/search.py", search_args)

    elif args.command == "advisor":
        run_script(".agent/scripts/advisor.py")

    elif args.command == "start":
        print(f"🌟 {BOLD}Willkommen beim Siebenwind Archiv-System{RESET}")
        view_workflow("start")

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
            view_workflow("historian")

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

    elif args.command == "index-pages":
        print(f"📂 {BOLD}Generiere Kategorie-Indizes...{RESET}")
        run_script(".agent/scripts/generate_wiki_indices.py")

    elif args.command == "inquisition":
        inq_args = ["--batch", str(args.batch)]
        if args.audit_only:
            inq_args.append("--audit-only")
        run_script(".agent/scripts/inquisition.py", inq_args)

    elif args.command == "archive":
        if args.archive_cmd == "sync":
            print(f"🔄 {BOLD}Synchronisiere Archiv-Symlinks...{RESET}")
            # Ensure docs/Archiv exists
            archive_dir = os.path.join(REPO_ROOT, "docs/Archiv")
            ingestion_dir = os.path.join(REPO_ROOT, "docs/Archiv/Ingestion_Reports")
            os.makedirs(ingestion_dir, exist_ok=True)
            
            # Link Research Board
            rb_source = os.path.join(REPO_ROOT, "System/Synapse_Board/LORE_RESEARCH_BOARD.md")
            rb_target = os.path.join(archive_dir, "Research_Board.md")
            if os.path.exists(rb_source) and not os.path.exists(rb_target):
                os.symlink("../../System/Synapse_Board/LORE_RESEARCH_BOARD.md", rb_target)
                print(f"  - Research Board verknüpft.")
            
            # Sync Ingestion Reports
            logs_ingestion = os.path.join(REPO_ROOT, "Logs/Ingestion")
            if os.path.exists(logs_ingestion):
                for f in os.listdir(logs_ingestion):
                    if f.endswith(".md"):
                        src = f"../../../Logs/Ingestion/{f}"
                        dst = os.path.join(ingestion_dir, f)
                        if not os.path.exists(dst):
                            os.symlink(src, dst)
                print(f"  - Ingestion Reports synchronisiert.")

    elif args.command == "mail":
        if not args.mail_args:
            print("Usage: 7w mail <post|inbox|read|claim|done> [args]")
            sys.exit(1)
        run_script(".agent/scripts/agent_mail.py", args.mail_args)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
