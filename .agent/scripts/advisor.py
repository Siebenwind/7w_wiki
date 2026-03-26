#!/usr/bin/env python3
"""
advisor.py — Der Berater (The Advisor)

Analysiert den aktuellen Projektstatus und gibt Empfehlungen für den nächsten Schritt.
Dient als zentrales Dashboard für den /takeover Prozess.
"""

import os
import sys
import re
import json
import argparse
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
from pages_integrity import load_pages_health_snapshot

# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MASTER_TASK_LIST = PROJECT_ROOT / "MASTER_TASK_LIST.md"
CHANGELOG = PROJECT_ROOT / "CHANGELOG.md"
INVENTUR_QUELLEN = PROJECT_ROOT / "Logs" / "INVENTUR_QUELLEN.md"
REGISTER_CHECK_SCRIPT = PROJECT_ROOT / ".agent" / "scripts" / "register_check.py"
DISPATCH_DIR = PROJECT_ROOT / "System" / "Synapse_Board" / "DISPATCH"
TECH_SYNC_FILES = [
    PROJECT_ROOT / "AGENTS.md",
    PROJECT_ROOT / "System" / "Synapse_Board" / "SY_INTEROP.md",
    PROJECT_ROOT / "System" / "AGENT_OPERATIONS_HANDBOOK.md",
    PROJECT_ROOT / "System" / "Synapse_Board" / "SY_WORKFLOW_CLI_MATRIX.md",
    PROJECT_ROOT / ".agent" / "config" / "tools.json",
]
PAGES_STALE_DAYS = 7

# ANSI Colors
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print(f"{BOLD}{CYAN}╔═══════════════════════════════════════════════════╗{RESET}")
    print(f"{BOLD}{CYAN}║   Der Berater — System-Status & Next Actions      ║{RESET}")
    print(f"{BOLD}{CYAN}╚═══════════════════════════════════════════════════╝{RESET}")
    print(f"\n{BOLD}Identität: {RESET}Oberarchivar (Hüter der Lore)")
    print(f"{BOLD}Mission:   {RESET}Rekonstruktion des Siebenwind-Kanons\n")

def get_next_task():
    """Findet die erste offene Phase/Task in MASTER_TASK_LIST.md."""
    if not MASTER_TASK_LIST.exists():
        return "Unbekannt (Datei fehlt)", None
    
    content = MASTER_TASK_LIST.read_text(encoding="utf-8")
    current_phase = "Unbekannt"
    
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("## "):
            current_phase = line.replace("## ", "").strip()
        elif line.startswith("- [ ]") or line.startswith("- [/]"):
            task = line.strip()[6:].strip()
            # Remove bold marker if present
            task = task.replace("**", "")
            return current_phase, task
            
    return "Alles erledigt!", None

def get_priority_overview():
    """Liest offene Aufgaben je Prioritätsblock aus MASTER_TASK_LIST.md."""
    counts = {"P1": 0, "P2": 0, "P3": 0, "BACKLOG": 0}
    first_p1_task = None
    if not MASTER_TASK_LIST.exists():
        return counts, None

    current_bucket = None
    content = MASTER_TASK_LIST.read_text(encoding="utf-8")
    for raw_line in content.splitlines():
        line = raw_line.strip()
        if line.startswith("## "):
            heading = line.lower()
            if "priorität 1" in heading or "prioritaet 1" in heading:
                current_bucket = "P1"
            elif "priorität 2" in heading or "prioritaet 2" in heading:
                current_bucket = "P2"
            elif "priorität 3" in heading or "prioritaet 3" in heading:
                current_bucket = "P3"
            elif "backlog" in heading:
                current_bucket = "BACKLOG"
            else:
                current_bucket = None
            continue

        if current_bucket and (line.startswith("- [ ]") or line.startswith("- [/]")):
            counts[current_bucket] += 1
            if current_bucket == "P1" and first_p1_task is None:
                first_p1_task = line[6:].replace("**", "").strip()

    return counts, first_p1_task

def get_pending_sources_count():
    """Zählt Zeilen mit 'Pending' in INVENTUR_QUELLEN.md."""
    if not INVENTUR_QUELLEN.exists():
        return 0
    content = INVENTUR_QUELLEN.read_text(encoding="utf-8")
    return content.count("Pending")

def get_last_changelog_entry():
    """Liest den letzten Eintrag aus CHANGELOG.md."""
    if not CHANGELOG.exists():
        return "Kein Changelog gefunden."
    
    content = CHANGELOG.read_text(encoding="utf-8")
    match = re.search(r"^#{2,6}\s+\[(.*?)\]\s+-\s+(.*)$", content, re.MULTILINE)
    if match:
        return f"{match.group(1)}: {match.group(2)}"
    return "Kein Eintrag gefunden."

def parse_frontmatter(raw: str) -> dict:
    """Parst YAML-Frontmatter als flaches Key-Value dict."""
    if not raw.startswith("---\n"):
        return {}
    end = raw.find("\n---\n", 4)
    if end == -1:
        return {}
    meta = {}
    for line in raw[4:end].splitlines():
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        meta[k.strip()] = v.strip()
    return meta


def read_pages_health() -> dict:
    snapshot = load_pages_health_snapshot()
    if not snapshot:
        return {
            "status": "UNKNOWN",
            "canonical_wiki_root": "docs/Siebenwind_Wiki",
            "legacy_wiki_root": "Siebenwind_Wiki",
            "drift_status": "UNKNOWN",
            "drift_counts": {
                "docs_only_files": 0,
                "legacy_only_files": 0,
                "content_mismatches": 0,
            },
            "unresolved_total": 0,
            "unallowlisted_total": 0,
            "last_validated_at": None,
            "stale": True,
        }
    pages = snapshot.get("pages_health", {})
    last_validated_at = pages.get("last_validated_at") or snapshot.get("generated_at")
    stale = True
    if last_validated_at:
        try:
            parsed = datetime.fromisoformat(last_validated_at.replace("Z", "+00:00"))
            stale = parsed < (datetime.now(timezone.utc) - timedelta(days=PAGES_STALE_DAYS))
        except ValueError:
            stale = True

    return {
        "status": pages.get("status", snapshot.get("status", "UNKNOWN")),
        "canonical_wiki_root": pages.get("canonical_wiki_root", "docs/Siebenwind_Wiki"),
        "legacy_wiki_root": pages.get("legacy_wiki_root", "Siebenwind_Wiki"),
        "drift_status": pages.get("drift_status", "UNKNOWN"),
        "drift_counts": pages.get(
            "drift_counts",
            {"docs_only_files": 0, "legacy_only_files": 0, "content_mismatches": 0},
        ),
        "unresolved_total": int(pages.get("unresolved_total", 0)),
        "unallowlisted_total": int(pages.get("unallowlisted_total", 0)),
        "last_validated_at": last_validated_at,
        "stale": stale,
    }


def get_last_sync_interop_at() -> str | None:
    mtimes = []
    for path in TECH_SYNC_FILES:
        if path.exists():
            mtimes.append(path.stat().st_mtime)
    if not mtimes:
        return None
    latest = max(mtimes)
    return datetime.fromtimestamp(latest, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

def get_dispatch_status():
    """Liest den Dispatch-Queue-Status aus System/Synapse_Board/DISPATCH."""
    counts = {"OPEN": 0, "CLAIMED": 0, "DONE": 0, "OTHER": 0}
    open_messages = []

    if not DISPATCH_DIR.exists():
        return counts, None

    for msg_file in sorted(DISPATCH_DIR.glob("MSG-*.md")):
        try:
            meta = parse_frontmatter(msg_file.read_text(encoding="utf-8"))
        except Exception:
            counts["OTHER"] += 1
            continue

        status = meta.get("status", "").upper()
        if status in counts:
            counts[status] += 1
        else:
            counts["OTHER"] += 1

        if status == "OPEN":
            prio = meta.get("priority", "NORMAL").upper()
            prio_rank = {"HIGH": 0, "NORMAL": 1, "LOW": 2}.get(prio, 3)
            created = meta.get("created_at", "")
            open_messages.append((prio_rank, created, meta))

    if not open_messages:
        return counts, None

    open_messages.sort(key=lambda item: (item[0], item[1]))
    top_meta = open_messages[0][2]
    subject = top_meta.get("subject", "Ohne Betreff")
    if len(subject) > 56:
        subject = subject[:56] + "..."
    top_display = (
        f"{top_meta.get('id', '?')} | {top_meta.get('priority', '?')} | "
        f"to={top_meta.get('to_agent', '?')} | {subject}"
    )
    return counts, top_display

def check_consistency():
    """Führt register_check.py aus und gibt die Anzahl der Issues zurück."""
    if not REGISTER_CHECK_SCRIPT.exists():
        return -1
    
    try:
        # Run silent capture
        result = subprocess.run(
            [sys.executable, str(REGISTER_CHECK_SCRIPT)],
            capture_output=True,
            text=True
        )
        # Parse output for "X Probleme gefunden" or return code logic
        # register_check returns 1 if issues found.
        # Let's parse the stdout for "ERGEBNIS: X Probleme"
        match = re.search(r"ERGEBNIS: (\d+) Probleme", result.stdout)
        if match:
            return int(match.group(1))
        return 0 if result.returncode == 0 else 1
    except Exception:
        return -1

def build_recommendations(phase, task, pending_sources, issues, dispatch_counts, top_dispatch, pages_health):
    recommendations: list[str] = []
    if issues > 0:
        recommendations.append(f"Run ./7w_wiki.py repair ({issues} consistency issues).")
    if pages_health["stale"] or pages_health["status"] in {"WARN", "FAIL", "UNKNOWN"}:
        recommendations.append("Route to /tech_master and run ./7w_wiki.py pages validate --strict.")
    if pages_health.get("drift_status") in {"WARN", "FAIL"}:
        recommendations.append("Pages drift detected; reconcile docs/Siebenwind_Wiki with the legacy shadow and higher-precedence sources.")
    if pages_health["unresolved_total"] >= 10:
        recommendations.append("Use ./7w_wiki.py repair --fix-roamlinks --auto for concentrated Pages-link drift.")
    open_dispatch = dispatch_counts.get("OPEN", 0)
    if open_dispatch > 0:
        recommendations.append("Review ./7w_wiki.py mail inbox --status OPEN before starting new work.")
    if pending_sources > 50:
        recommendations.append("Large source backlog detected; prioritize /ingest_master.")
    elif task:
        recommendations.append(f"Continue current focus: {task}")
    else:
        recommendations.append("No immediate blocker detected; refresh stats or ask for the next task.")
    return recommendations


def recommend_action(phase, task, pending_sources, issues, dispatch_counts, top_dispatch, pages_health):
    """Entscheidungslogik für die Empfehlung."""
    print(f"{BOLD}--- Empfehlung ---{RESET}")
    
    if issues > 0:
        print(f"{RED}⚠️  Priorität: Konsistenz wiederherstellen ({issues} Probleme).{RESET}")
        print(f"👉 Starte Workflow: {BOLD}./7w_wiki.py repair{RESET}")
        print(f"   (Alternativ: /audit Bericht lesen)")
        if pages_health["stale"] or pages_health["status"] in {"WARN", "FAIL", "UNKNOWN"}:
            print(f"👉 Danach /tech_master: {BOLD}./7w_wiki.py pages validate --strict{RESET}")
        return

    if pages_health["stale"] or pages_health["status"] in {"WARN", "FAIL", "UNKNOWN"}:
        print(f"{YELLOW}🛠️  Pages Health: {pages_health['status']}{RESET}")
        if pages_health["stale"]:
            print(f"👉 Pages snapshot ist veraltet. Route zu {BOLD}/tech_master{RESET}")
        else:
            print(f"👉 Starte Workflow: {BOLD}/tech_master{RESET}")
        print(f"   Validation: {BOLD}./7w_wiki.py pages validate --strict{RESET}")
        if pages_health["unresolved_total"] >= 10:
            print(f"   Link-Reparatur: {BOLD}./7w_wiki.py repair --fix-roamlinks --auto{RESET}")
        return

    open_dispatch = dispatch_counts.get("OPEN", 0)
    if open_dispatch > 0:
        print(f"{YELLOW}📬 Offene Dispatch-Nachrichten: {open_dispatch}{RESET}")
        if top_dispatch:
            print(f"   Priorisiert: {top_dispatch}")
        print(f"👉 Queue zuerst pruefen: {BOLD}./7w_wiki.py mail inbox --status OPEN{RESET}")
        if open_dispatch >= 3:
            return

    if pending_sources > 50: # Arbitrary threshold for batch mode
        print(f"{YELLOW}📚 Viele offene Quellen ({pending_sources}).{RESET}")
        print(f"👉 Starte Workflow: {BOLD}/batch{RESET} (Massenverarbeitung)")
        return

    if task:
        print(f"{GREEN}🚀 Fokus: Projektfortschritt{RESET}")
        print(f"   Aktuelle Phase: {phase}")
        print(f"👉 Nächste Aufgabe: {task}")
        # Detect if task implies specific workflow
        if "Bote" in task or "Source" in task:
            print(f"   Empfohlener Workflow: {BOLD}/ingest_master{RESET}")
        return

    print(f"{GREEN}🎉 Nichts zu tun!{RESET}")
    print(f"👉 Starte Workflow: {BOLD}/stats{RESET} (Genieße den Erfolg)")
    print("   Oder frage den User nach neuen Aufgaben.")

def collect_advisor_data():
    """Sammelt alle Advisor-Daten in einem Dictionary."""
    prio_counts, first_p1_task = get_priority_overview()
    last_change = get_last_changelog_entry()
    phase, next_task = get_next_task()
    pending = get_pending_sources_count()
    dispatch_counts, top_dispatch = get_dispatch_status()
    issues = check_consistency()
    pages_health = read_pages_health()
    recommendations = build_recommendations(phase, next_task, pending, issues, dispatch_counts, top_dispatch, pages_health)
    degraded = issues != 0 or pages_health["stale"] or pages_health["status"] in {"WARN", "FAIL", "UNKNOWN"}

    return {
        "priorities": prio_counts,
        "first_p1_task": first_p1_task,
        "last_change": last_change,
        "current_phase": phase,
        "next_task": next_task,
        "pending_sources": pending,
        "dispatch": {
            "counts": dispatch_counts,
            "top_open": top_dispatch
        },
        "consistency_issues": issues,
        "pages_health": pages_health,
        "tech_hygiene": {
            "last_sync_interop_at": get_last_sync_interop_at(),
        },
        "status": "OK" if not degraded else "DEGRADED",
        "system_health": "Sauber" if not degraded else f"{issues} Konsistenzprobleme / Pages {pages_health['status']}",
        "recommendations": recommendations,
    }

def main():
    parser = argparse.ArgumentParser(description="Der Berater - System Status")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")
    args = parser.parse_args()

    data = collect_advisor_data()

    if args.json:
        print(json.dumps(data, indent=2))
        return

    clear_screen()
    print_header()
    
    print(f"{BOLD}Status-Analyse:{RESET}")

    # 1. Priorities
    prio_counts = data["priorities"]
    first_p1_task = data["first_p1_task"]
    print(
        "  🎯 Prioritäten:      "
        f"{RED}P1 {prio_counts['P1']}{RESET} | "
        f"{YELLOW}P2 {prio_counts['P2']}{RESET} | "
        f"{BLUE}P3 {prio_counts['P3']}{RESET} | "
        f"Backlog {prio_counts['BACKLOG']}"
    )
    if first_p1_task:
        short_p1 = first_p1_task[:60] + "..." if len(first_p1_task) > 60 else first_p1_task
        print(f"     Top P1:            {short_p1}")

    # 2. Changelog
    print(f"  📅 Letzte Änderung:   {BLUE}{data['last_change']}{RESET}")
    
    # 3. Tasks
    phase = data["current_phase"]
    next_task = data["next_task"]
    task_display = next_task[:60] + "..." if next_task and len(next_task) > 60 else next_task
    print(f"  📌 Aktuelle Phase:    {YELLOW}{phase}{RESET}")
    if next_task:
        print(f"     Offener Task:      {task_display}")
    
    # 4. Sources
    pending = data["pending_sources"]
    color = RED if pending > 0 else GREEN
    print(f"  📜 Offene Quellen:    {color}{pending}{RESET}")

    # 5. Dispatch Queue
    dispatch_counts = data["dispatch"]["counts"]
    top_dispatch = data["dispatch"]["top_open"]
    open_count = dispatch_counts.get("OPEN", 0)
    claimed_count = dispatch_counts.get("CLAIMED", 0)
    done_count = dispatch_counts.get("DONE", 0)
    queue_color = GREEN if open_count == 0 else YELLOW
    print(
        f"  ✉️ Dispatch Queue:    {queue_color}OPEN {open_count}{RESET} | "
        f"CLAIMED {claimed_count} | DONE {done_count}"
    )
    if top_dispatch:
        print(f"     Top OPEN:          {top_dispatch}")
    
    # 6. Consistency
    print("  🔍 Konsistenz-Check:  ", end="", flush=True)
    issues = data["consistency_issues"]
    if issues == -1:
        print(f"{RED}Fehler (Skript fehlt){RESET}")
    elif issues == 0:
        print(f"{GREEN}Sauber (0 Issues){RESET}")
    else:
        print(f"{RED}{issues} Probleme gefunden{RESET}")

    pages_health = data["pages_health"]
    pages_color = GREEN if pages_health["status"] == "PASS" and not pages_health["stale"] else YELLOW
    print(
        f"  🌐 Pages Health:      {pages_color}{pages_health['status']}{RESET} | "
        f"unresolved {pages_health['unresolved_total']} | "
        f"unallowlisted {pages_health['unallowlisted_total']}"
    )
    print(
        f"  🧭 Drift-Status:      {pages_health['drift_status']} | "
        f"legacy_only {pages_health['drift_counts']['legacy_only_files']} | "
        f"content_mismatches {pages_health['drift_counts']['content_mismatches']}"
    )
    print(
        "  ⚙️  Tech Sync:        "
        f"{BLUE}{data['tech_hygiene']['last_sync_interop_at'] or 'unbekannt'}{RESET}"
    )
        
    print("")
    recommend_action(phase, next_task, pending, issues, dispatch_counts, top_dispatch, pages_health)
    print("")

if __name__ == "__main__":
    main()
