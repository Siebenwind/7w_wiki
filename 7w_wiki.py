#!/usr/bin/env python3
import sys
import subprocess
import argparse
import os
import re
import json

"""
Siebenwind Lore Engine CLI (7w)
Unified entry point for all archival and intelligence tools.
"""

def load_nexus_config():
    manifest_path = os.path.join(os.path.dirname(__file__), "lore_manifest.json")
    if os.path.exists(manifest_path):
        try:
            with open(manifest_path, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

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
GREEN = "\033[92m"
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
        print(f"Error executing {path}: {e}", file=sys.stderr)
        sys.exit(1)

def view_workflow(name):
    path = os.path.join(os.path.dirname(__file__), f".agent/workflows/{name}.md")
    if os.path.exists(path):
        with open(path, 'r') as f:
            print(f.read())
    else:
        print(f"Workflow {name} not found at {path}")

def load_workflow_state():
    import json
    state_file = os.path.join(os.path.dirname(__file__), ".agent/data/workflow_state.json")
    if os.path.exists(state_file):
        try:
            with open(state_file, "r") as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_workflow_state(state):
    import json
    state_file = os.path.join(os.path.dirname(__file__), ".agent/data/workflow_state.json")
    os.makedirs(os.path.dirname(state_file), exist_ok=True)
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2)

def run_workflow(name, auto_yes=False, resume=False):
    path = os.path.join(os.path.dirname(__file__), f".agent/workflows/{name}.md")
    if not os.path.exists(path):
        print(f"Workflow {name} not found at {path}")
        return

    with open(path, 'r') as f:
        lines = f.readlines()

    commands = []
    in_turbo = False
    for line in lines:
        stripped = line.strip()
        if stripped == "// turbo" or stripped == "// turbo-all":
            in_turbo = True
            continue
        elif not stripped or stripped.startswith("## ") or stripped.startswith("### "):
            in_turbo = False # Exit turbo block on empty or heading
        
        if in_turbo and stripped.startswith(("- ", "* ", "1. ", "2. ", "3. ", "4. ", "5. ", "6. ", "7. ", "8. ", "9. ")):
            # Check if it looks like a command
            match = re.search(r'`(./7w_wiki\.py [^`]+)`', stripped)
            if match:
                commands.append(match.group(1))

    if not commands:
        print(f"No executable commands found in {name}.")
        return

    state_dict = load_workflow_state()
    # Initialize or reset state for this workflow
    if not resume or name not in state_dict:
        state_dict[name] = {"completed": []}
    
    completed_indices = state_dict[name]["completed"]

    if len(completed_indices) == len(commands):
        print(f"\n{BOLD}{GREEN}Workflow {name} is already fully completed.{RESET}")
        print("Run again without --resume to start over.")
        return

    print(f"\n{BOLD}{YELLOW}Workflow: {name} ({len(commands)} commands){RESET}")
    for i, cmd in enumerate(commands, 1):
        if resume and i in completed_indices:
            print(f" {i}. {cmd} [{GREEN}DONE{RESET}]")
        else:
            print(f" {i}. {cmd}")

    if not auto_yes:
        ans = input(f"\nProceed with execution? [y/N]: ")
        if ans.lower() not in ('y', 'yes'):
            print("Aborted.")
            return

    for i, cmd in enumerate(commands, 1):
        if resume and i in completed_indices:
            continue
            
        print(f"\n{BOLD}Running [{i}/{len(commands)}]:{RESET} {cmd}")
        # Strip the leading './7w_wiki.py ' since sys.executable manages the entry
        args_str = cmd.replace("./7w_wiki.py ", "", 1).strip()
        import shlex
        args_list = shlex.split(args_str)
        run_script("7w_wiki.py", args_list)
        
        # Mark as completed
        completed_indices.append(i)
        state_dict[name]["completed"] = completed_indices
        save_workflow_state(state_dict)
        print("-" * 40)
        
    print(f"{BOLD}{GREEN}Workflow {name} completed.{RESET}")
    
    # Optional: Clear state upon full completion
    state_dict[name] = {"completed": []}
    save_workflow_state(state_dict)

def main():
    config = load_nexus_config()
    lore_config = config.get("lore", {})
    world_name = lore_config.get("world_name", "Siebenwind")
    default_wiki = lore_config.get("directories", {}).get("wiki", "Siebenwind_Wiki")

    parser = argparse.ArgumentParser(description=f"{world_name} Lore Engine CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Search (Oracle)
    search_parser = subparsers.add_parser("search", help="Semantic search via the Oracle (RAG)")
    search_parser.add_argument("query", help="The search query")
    search_parser.add_argument("--source", choices=["wiki", "quellen", "all"], default="wiki", help="Search target")
    search_parser.add_argument("--json", action="store_true", help="Output raw JSON")
    # Add remnant args to pass through
    search_parser.add_argument('remaining', nargs=argparse.REMAINDER, help="Additional arguments for search.py")

    # Start (Onboarding)
    start_parser = subparsers.add_parser("start", help="Start here (Onboarding & Options)")
    start_parser.add_argument("--run", action="store_true", help="Execute the workflow checklist automatically")
    start_parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation prompts during --run")
    start_parser.add_argument("--resume", action="store_true", help="Resume from last completed step")

    # Test Runner
    test_parser = subparsers.add_parser("test", help="Run interoperability and clean-state test suites")
    test_parser.add_argument("--suite", default="clean-client-state", help="Suite name or 'all'")
    test_parser.add_argument("--list-suites", action="store_true", help="List available test suites")
    test_parser.add_argument("--timeout", type=int, default=120, help="Timeout per command (seconds)")
    test_parser.add_argument("--post-failures", action="store_true", help="Post dispatch message on failures")
    test_parser.add_argument("--from-agent", default="Test-Waechter", help="Dispatch sender if --post-failures")
    test_parser.add_argument("--to-agent", default="ALL", help="Dispatch target if --post-failures")
    test_parser.add_argument("--priority", choices=["LOW", "NORMAL", "HIGH"], default="HIGH", help="Dispatch priority")
    test_parser.add_argument("--include-rag", action="store_true", help="Include unstable rag-relevance-smoke in --suite all")
    test_parser.add_argument("--allow-fail", action="store_true", help="Return 0 even if tests fail")

    # Takeover / Handover workflow views
    takeover_parser = subparsers.add_parser("takeover", help="Show takeover workflow guidance")
    takeover_parser.add_argument("--run", action="store_true", help="Execute the workflow checklist automatically")
    takeover_parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation prompts during --run")
    takeover_parser.add_argument("--resume", action="store_true", help="Resume from last completed step")

    handover_parser = subparsers.add_parser("handover", help="Show handover workflow guidance")
    handover_parser.add_argument("--run", action="store_true", help="Execute the workflow checklist automatically")
    handover_parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation prompts during --run")
    handover_parser.add_argument("--resume", action="store_true", help="Resume from last completed step")

    # Historian
    hist_parser = subparsers.add_parser("historian", help="Deep Lore Analysis (Workflow)")
    hist_parser.add_argument("query", nargs="?", help="Subject to analyze")

    # Repair
    repair_parser = subparsers.add_parser("repair", help="Interactive repair of links and metadata")
    repair_parser.add_argument("--auto", action="store_true", help="Run non-interactive auto-repair")
    repair_parser.add_argument("--full", action="store_true", help="Run full non-interactive repair cycle (1-3)")


    audit_parser = subparsers.add_parser("audit", help="Run consistency audit (duplicates, orphans)")
    audit_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    # Index
    index_parser = subparsers.add_parser("index", help="Manage semantic index")
    index_parser.add_argument("--rebuild", action="store_true", help="Full re-indexing")
    index_parser.add_argument("--status", action="store_true", help="Check index status")

    # Index Pages
    subparsers.add_parser("index-pages", help="Automatically generate index.md files for all wiki categories")

    # Pages Build / Validation
    pages_parser = subparsers.add_parser("pages", help="Build and validate GitHub Pages documentation")
    pages_sub = pages_parser.add_subparsers(dest="pages_cmd")
    pages_sub.add_parser("status", help="Show mkdocs availability and pages build prerequisites")
    pages_build = pages_sub.add_parser("build", help="Run mkdocs build via project-local tooling")
    pages_build.add_argument("--strict", action="store_true", help="Enable strict mode for mkdocs build")
    pages_build.add_argument("--no-clean", action="store_true", help="Skip mkdocs --clean")
    pages_build.add_argument("--config", default="mkdocs.yml", help="Path to mkdocs config (default: mkdocs.yml)")
    pages_validate = pages_sub.add_parser("validate", help="Run docs link suite, audit, and pages build")
    pages_validate.add_argument("--strict", action="store_true", help="Enable strict mode for mkdocs build")
    pages_validate.add_argument("--no-clean", action="store_true", help="Skip mkdocs --clean")
    pages_validate.add_argument("--skip-link-suite", action="store_true", help="Skip test --suite interop-doc-links")
    pages_validate.add_argument("--skip-source-hygiene", action="store_true", help="Skip test --suite source-link-hygiene")
    pages_validate.add_argument("--skip-process-governance", action="store_true", help="Skip test --suite process-dispatch-curiosity")
    pages_validate.add_argument("--skip-reader-stats-contract", action="store_true", help="Skip test --suite reader-stats-contract")
    pages_validate.add_argument("--skip-audit", action="store_true", help="Skip audit")
    pages_validate.add_argument("--config", default="mkdocs.yml", help="Path to mkdocs config (default: mkdocs.yml)")

    # Advisor (Default)
    advisor_parser = subparsers.add_parser("advisor", help="Show system status and recommendations (Default)")
    advisor_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    # Ingestion (Silicon Inquisition)
    inq_parser = subparsers.add_parser("inquisition", help="Great Re-Ingestion of legacy sources (Silicon Inquisition)")
    inq_parser.add_argument("--batch", type=int, default=10, help="Number of sources to process in this run")
    inq_parser.add_argument("--audit-only", action="store_true", help="Only list missing reports without processing")

    # QA & Sanitization
    sanitize_parser = subparsers.add_parser("sanitize", help="Run Wiki Sanitizer (layout, H1-alignment, frontmatter)")
    sanitize_parser.add_argument("target", nargs="?", default=default_wiki, help=f"Path to file/folder (default: {default_wiki})")
    sanitize_parser.add_argument("--auto", action="store_true", help="Auto-fix violations")
    sanitize_parser.add_argument("--json", action="store_true", help="Output raw JSON")
    
    # Lint (Orchestrator for sanitize, check, score)
    lint_parser = subparsers.add_parser("lint", help="Run comprehensive lint pipeline (Sanitizer, Style Check, Lore Score)")
    lint_parser.add_argument("target", nargs="?", default=default_wiki, help=f"Path to file/folder (default: {default_wiki})")
    lint_parser.add_argument("--fix", action="store_true", help="Auto-fix layout and frontmatter issues")
    lint_parser.add_argument("--json", action="store_true", help="Output raw JSON report (suppresses stdout)")

    # Lore Scoring
    score_parser = subparsers.add_parser("score", help="Calculate Lore Quality Score (LQS) for a file")
    score_parser.add_argument("file", help="Path to the markdown file")

    # Ingest Pipeline
    ingest_parser = subparsers.add_parser("ingest", help="Run full Ingest Pipeline (Lint -> Archive Sync -> Audit)")
    ingest_parser.add_argument("file", help="Path to the markdown file to ingest")

    # Translation
    trans_parser = subparsers.add_parser("translate", help="Translate Falandric texts or manage dictionaries")
    trans_parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments for translator.py")

    # Watcher
    subparsers.add_parser("watch", help="Start the live watcher for real-time indexing")

    # QA & Style Check (Lektor)
    check_parser = subparsers.add_parser("check", help="Run professional style and grammar check (Lektor)")
    check_parser.add_argument("path", nargs="?", default=default_wiki, help=f"Path to file/folder (default: {default_wiki})")
    check_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    # Archive Management
    archive_parser = subparsers.add_parser("archive", help="Manage Wiki Archive (Symlinks, Rotation, Compression)")
    archive_sub = archive_parser.add_subparsers(dest="archive_cmd")
    archive_sub.add_parser("sync", help="Sync archive symlinks into docs/Archiv")
    rotate_parser = archive_sub.add_parser("rotate", help="Compress stale logs and rotate dispatches")
    rotate_parser.add_argument("--dry-run", action="store_true", help="Show what would change")
    rotate_parser.add_argument("--keep-days", type=int, default=7, help="Keep files newer than N days (default: 7)")
    unpack_parser = archive_sub.add_parser("unpack", help="Unpack a compressed archive")
    unpack_parser.add_argument("archive_name", help="Name of archive to unpack")
    # Agent Messaging (Dispatch)
    mail_parser = subparsers.add_parser("mail", help="Agent Messaging (Dispatch)")
    mail_parser.add_argument("mail_args", nargs=argparse.REMAINDER, help="Arguments for agent_mail.py")

    # Scout (Forum Crawler)
    scout_parser = subparsers.add_parser("scout", help="Deep Scan of external forums (Bekanntmachungen/News)")
    scout_parser.add_argument("--forum", choices=["bekanntmachungen", "news"], default="bekanntmachungen", help="Target forum")
    scout_parser.add_argument("--pages", type=int, default=3, help="Number of pages to scan")

    # Technician (DevOps)
    tech_parser = subparsers.add_parser("tech", help="Show Technician workflow (DevOps & Infrastructure)")
    tech_parser.add_argument("--manifest", action="store_true", help="Generate OpenAPI tools.json from CLI context")
    tech_parser.add_argument("--compile-skills", action="store_true", help="Compile SKILL.md.tpl with variables from lore_manifest")

    # Version Management
    ver_parser = subparsers.add_parser("version", help="Show or bump the wiki standard version")
    ver_parser.add_argument("--bump", choices=["major", "minor", "patch"], help="Bump version")
    ver_parser.add_argument("--label", default="Inter-AI Compliant", help="Version label")
    ver_parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    ver_parser.add_argument("--json", action="store_true", help="Output version as JSON")

    # Antigravity (Core Protocol)
    subparsers.add_parser("antigravity", help="Show Antigravity core workflow (default protocol)")

    # Maintainer Standpoint (Human Steering Anchor)
    leit_parser = subparsers.add_parser("leitpunkt", help="Manage maintainer standpoint workflow and checks")
    leit_sub = leit_parser.add_subparsers(dest="leit_cmd")
    leit_sub.add_parser("view", help="Show /leitpunkt workflow guidance")
    leit_sub.add_parser("status", help="Show readiness status of MAINTAINER_STANDPUNKT")
    leit_check = leit_sub.add_parser("check", help="Validate MAINTAINER_STANDPUNKT structure")
    leit_check.add_argument("--strict", action="store_true", help="Fail if TODO markers remain")
    leit_scaffold = leit_sub.add_parser("scaffold", help="Create or reset MAINTAINER_STANDPUNKT template")
    leit_scaffold.add_argument("--force", action="store_true", help="Overwrite existing file")

    # Wiki Stats Command explicitly listed if we need options
    stats_parser = subparsers.add_parser("stats", help="Generate Wiki statistics")
    stats_parser.add_argument("--json", action="store_true", help="Output raw JSON stats block")

    # MCP Server
    mcp_parser = subparsers.add_parser("mcp", help="Start MCP Server (Model Context Protocol)")
    mcp_parser.add_argument("--transport", choices=["stdio", "streamable-http"], default="stdio", help="Transport mode")
    mcp_parser.add_argument("--port", type=int, default=7777, help="Port for HTTP transport")

    # Check for help-json explicitly before parsing (to bypass required arguments)
    if "--help-json" in sys.argv:
        schema = {
            "name": "7w_wiki_cli",
            "description": parser.description,
            "commands": []
        }
        # subparsers.choices is a dict mapping cmd_name -> subparser
        if subparsers and hasattr(subparsers, 'choices'):
            for cmd_name, subp in subparsers.choices.items():
                cmd_data = {
                    "name": cmd_name,
                    "description": subp.description or "",
                    "arguments": []
                }
                for action in subp._actions:
                    if action.dest == "help":
                        continue
                    arg_data = {
                        "name": action.dest,
                        "flags": action.option_strings,
                        "help": action.help or "",
                        "required": action.required
                    }
                    if action.choices:
                        arg_data["choices"] = list(action.choices)
                    cmd_data["arguments"].append(arg_data)
                schema["commands"].append(cmd_data)
        
        print(json.dumps(schema, indent=2))
        sys.exit(0)

    # Check if no arguments provided, default to advisor
    if len(sys.argv) == 1:
        args = parser.parse_args(["advisor"])
    else:
        args = parser.parse_args()

    if args.command == "search":
        search_args = [args.query]
        if args.source:
            search_args.extend(["--source", args.source])
        if args.json:
            search_args.append("--json")
        if args.remaining:
            search_args.extend(args.remaining)
        run_script(".agent/skills/oracle/search.py", search_args)

    elif args.command == "advisor":
        adv_args = []
        if args.json:
            adv_args.append("--json")
        run_script(".agent/scripts/advisor.py", adv_args)

    elif args.command == "start":
        if args.run:
            run_workflow("start", auto_yes=args.yes, resume=args.resume)
        else:
            print(f"🚀 {BOLD}Workflow: /start{RESET}")
            view_workflow("start")

    elif args.command == "takeover":
        if args.run:
            run_workflow("takeover", auto_yes=args.yes, resume=args.resume)
        else:
            print(f"📥 {BOLD}Workflow: /takeover{RESET}")
            view_workflow("takeover")

    elif args.command == "handover":
        if args.run:
            run_workflow("handover", auto_yes=args.yes, resume=args.resume)
        else:
            print(f"📦 {BOLD}Workflow: /handover{RESET}")
            view_workflow("handover")

    elif args.command == "stats":
        stats_args = []
        if args.json:
            stats_args.append("--json")
        run_script(".agent/scripts/generate_wiki_stats.py", stats_args)

    elif args.command == "test":
        test_args = ["--suite", args.suite, "--timeout", str(args.timeout)]
        if args.list_suites:
            test_args.append("--list-suites")
        if args.post_failures:
            test_args.append("--post-failures")
            test_args.extend(["--from-agent", args.from_agent, "--to-agent", args.to_agent, "--priority", args.priority])
        if args.include_rag:
            test_args.append("--include-rag")
        if args.allow_fail:
            test_args.append("--allow-fail")
        run_script(".agent/scripts/test_runner.py", test_args)

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
        repair_args = []
        if args.auto:
            repair_args.append("--auto")
        if args.full:
            repair_args.append("--full")
        run_script(".agent/scripts/repair.py", repair_args)

    elif args.command == "audit":
        audit_args = []
        if args.json:
            audit_args.append("--json")
        run_script(".agent/scripts/register_check.py", audit_args)

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

    elif args.command == "pages":
        if not args.pages_cmd:
            pages_parser.print_help()
            sys.exit(1)
        page_args = [args.pages_cmd]
        if hasattr(args, "strict") and args.strict:
            page_args.append("--strict")
        if hasattr(args, "no_clean") and args.no_clean:
            page_args.append("--no-clean")
        if hasattr(args, "skip_link_suite") and args.skip_link_suite:
            page_args.append("--skip-link-suite")
        if hasattr(args, "skip_source_hygiene") and args.skip_source_hygiene:
            page_args.append("--skip-source-hygiene")
        if hasattr(args, "skip_process_governance") and args.skip_process_governance:
            page_args.append("--skip-process-governance")
        if hasattr(args, "skip_reader_stats_contract") and args.skip_reader_stats_contract:
            page_args.append("--skip-reader-stats-contract")
        if hasattr(args, "skip_audit") and args.skip_audit:
            page_args.append("--skip-audit")
        if hasattr(args, "config") and args.config:
            page_args.extend(["--config", args.config])
        run_script(".agent/scripts/pages_tool.py", page_args)

    elif args.command == "inquisition":
        inq_args = ["--batch", str(args.batch)]
        if args.audit_only:
            inq_args.append("--audit-only")
        run_script(".agent/scripts/inquisition.py", inq_args)

    elif args.command == "sanitize":
        sanitize_args = [args.target]
        if args.auto:
            sanitize_args.append("--auto")
        if getattr(args, "json", False):
            sanitize_args.append("--json")
        run_script(".agent/scripts/wiki_sanitizer.py", sanitize_args)

    elif args.command == "lint":
        lint_args = [args.target]
        if args.fix:
            lint_args.append("--fix")
        if args.json:
            lint_args.append("--json")
        run_script(".agent/scripts/lint_tool.py", lint_args)

    elif args.command == "ingest":
        run_script(".agent/scripts/ingest_pipeline.py", [args.file])

    elif args.command == "score":
        run_script(".agent/scripts/lore_score_manager.py", [args.file])

    elif args.command == "translate":
        run_script(".agent/scripts/translator.py", args.args)

    elif args.command == "watch":
        run_script(".agent/scripts/watcher.py")

    elif args.command == "check":
        check_args = [args.path]
        if getattr(args, "json", False):
            check_args.append("--json")
        run_script(".agent/skills/lektor/style_checker.py", check_args)

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
        elif args.archive_cmd == "rotate":
            rotate_args = ["rotate"]
            if getattr(args, "dry_run", False):
                rotate_args.append("--dry-run")
            rotate_args.extend(["--keep-days", str(getattr(args, "keep_days", 7))])
            run_script(".agent/scripts/archive_rotate.py", rotate_args)
        elif args.archive_cmd == "unpack":
            run_script(".agent/scripts/archive_rotate.py", ["unpack", args.archive_name])
        else:
            archive_parser.print_help()

    elif args.command == "scout":
        forum_map = {"bekanntmachungen": "6", "news": "1"}
        run_script("Scripts/forum_scanner.py", ["--forum_id", forum_map[args.forum], "--pages", str(args.pages)])

    elif args.command == "mail":
        if not args.mail_args:
            print("Usage: ./7w_wiki.py mail <post|inbox|read|claim|done> [args]")
            sys.exit(1)
        run_script(".agent/scripts/agent_mail.py", args.mail_args)

    elif args.command == "tech":
        if getattr(args, "manifest", False):
            print(f"🔧 {BOLD}Regenerating tools.json manifest...{RESET}")
            run_script(".agent/scripts/generate_tools_manifest.py")
        elif getattr(args, "compile_skills", False):
            print(f"🔧 {BOLD}Compiling SKILL.md templates...{RESET}")
            run_script(".agent/scripts/compile_skills.py")
        else:
            print(f"🔧 {BOLD}Workflow: /tech{RESET}")
            view_workflow("tech")

    elif args.command == "version":
        ver_args = []
        if getattr(args, "bump", None):
            ver_args.extend(["--bump", args.bump])
        if getattr(args, "label", None):
            ver_args.extend(["--label", args.label])
        if getattr(args, "dry_run", False):
            ver_args.append("--dry-run")
        if getattr(args, "json", False):
            ver_args.append("--json")
        run_script(".agent/scripts/version_manager.py", ver_args)

    elif args.command == "antigravity":
        print(f"🧲 {BOLD}Workflow: /antigravity (Core Protocol){RESET}")
        view_workflow("antigravity")

    elif args.command == "leitpunkt":
        if not args.leit_cmd or args.leit_cmd == "view":
            print(f"🧭 {BOLD}Workflow: /leitpunkt (Menschlicher Leitpunkt){RESET}")
            view_workflow("leitpunkt")
        elif args.leit_cmd == "status":
            run_script(".agent/scripts/leitpunkt_tool.py", ["status"])
        elif args.leit_cmd == "check":
            leit_args = ["check"]
            if args.strict:
                leit_args.append("--strict")
            run_script(".agent/scripts/leitpunkt_tool.py", leit_args)
        elif args.leit_cmd == "scaffold":
            leit_args = ["scaffold"]
            if args.force:
                leit_args.append("--force")
            run_script(".agent/scripts/leitpunkt_tool.py", leit_args)
        else:
            print("Usage: ./7w_wiki.py leitpunkt [view|status|check|scaffold]")
            sys.exit(1)

    elif args.command == "mcp":
        mcp_args = ["--transport", args.transport, "--port", str(args.port)]
        run_script("System/MCP/server.py", mcp_args)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
