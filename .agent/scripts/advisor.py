#!/usr/bin/env python3
"""
advisor.py — Der Berater (The Advisor)

Analysiert den aktuellen Projektstatus und gibt Empfehlungen für den nächsten Schritt.
Dient als zentrales Dashboard für den /takeover Prozess.
"""

import os
import sys
import re
import subprocess
from pathlib import Path

# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MASTER_TASK_LIST = PROJECT_ROOT / "MASTER_TASK_LIST.md"
CHANGELOG = PROJECT_ROOT / "CHANGELOG.md"
INVENTUR_QUELLEN = PROJECT_ROOT / "Logs" / "INVENTUR_QUELLEN.md"
REGISTER_CHECK_SCRIPT = PROJECT_ROOT / ".agent" / "scripts" / "register_check.py"
DISPATCH_DIR = PROJECT_ROOT / "System" / "Synapse_Board" / "DISPATCH"

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

def recommend_action(phase, task, pending_sources, issues, dispatch_counts, top_dispatch):
    """Entscheidungslogik für die Empfehlung."""
    print(f"{BOLD}--- Empfehlung ---{RESET}")
    
    if issues > 0:
        print(f"{RED}⚠️  Priorität: Konsistenz wiederherstellen ({issues} Probleme).{RESET}")
        print(f"👉 Starte Workflow: {BOLD}./7w_wiki.py repair{RESET}")
        print(f"   (Alternativ: /audit Bericht lesen)")
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
            print(f"   Empfohlener Workflow: {BOLD}/wiki_process{RESET} oder {BOLD}/ingestion_protocol{RESET}")
        return

    print(f"{GREEN}🎉 Nichts zu tun!{RESET}")
    print(f"👉 Starte Workflow: {BOLD}/stats{RESET} (Genieße den Erfolg)")
    print("   Oder frage den User nach neuen Aufgaben.")

def main():
    clear_screen()
    print_header()
    
    print(f"{BOLD}Status-Analyse:{RESET}")

    # 1. Priorities
    prio_counts, first_p1_task = get_priority_overview()
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
    last_change = get_last_changelog_entry()
    print(f"  📅 Letzte Änderung:   {BLUE}{last_change}{RESET}")
    
    # 3. Tasks
    phase, next_task = get_next_task()
    task_display = next_task[:60] + "..." if next_task and len(next_task) > 60 else next_task
    print(f"  📌 Aktuelle Phase:    {YELLOW}{phase}{RESET}")
    if next_task:
        print(f"     Offener Task:      {task_display}")
    
    # 4. Sources
    pending = get_pending_sources_count()
    color = RED if pending > 0 else GREEN
    print(f"  📜 Offene Quellen:    {color}{pending}{RESET}")

    # 5. Dispatch Queue
    dispatch_counts, top_dispatch = get_dispatch_status()
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
    
    # 6. Consistency (Run check typically takes < 1s)
    print("  🔍 Konsistenz-Check:  ", end="", flush=True)
    issues = check_consistency()
    if issues == -1:
        print(f"{RED}Fehler (Skript fehlt){RESET}")
    elif issues == 0:
        print(f"{GREEN}Sauber (0 Issues){RESET}")
    else:
        print(f"{RED}{issues} Probleme gefunden{RESET}")
        
    print("")
    recommend_action(phase, next_task, pending, issues, dispatch_counts, top_dispatch)
    print("")

if __name__ == "__main__":
    main()
