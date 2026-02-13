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
    match = re.search(r"## \[(.*?)\] - (.*)", content)
    if match:
        return f"{match.group(1)}: {match.group(2)}"
    return "Kein Eintrag gefunden."

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

def recommend_action(phase, task, pending_sources, issues):
    """Entscheidungslogik für die Empfehlung."""
    print(f"{BOLD}--- Empfehlung ---{RESET}")
    
    if issues > 0:
        print(f"{RED}⚠️  Priorität: Konsistenz wiederherstellen ({issues} Probleme).{RESET}")
        print(f"👉 Starte Workflow: {BOLD}python3 .agent/scripts/repair.py{RESET}")
        print(f"   (Alternativ: /audit Bericht lesen)")
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
    
    # 1. Changelog
    last_change = get_last_changelog_entry()
    print(f"  📅 Letzte Änderung:   {BLUE}{last_change}{RESET}")
    
    # 2. Tasks
    phase, next_task = get_next_task()
    task_display = next_task[:60] + "..." if next_task and len(next_task) > 60 else next_task
    print(f"  📌 Aktuelle Phase:    {YELLOW}{phase}{RESET}")
    if next_task:
        print(f"     Offener Task:      {task_display}")
    
    # 3. Sources
    pending = get_pending_sources_count()
    color = RED if pending > 0 else GREEN
    print(f"  📜 Offene Quellen:    {color}{pending}{RESET}")
    
    # 4. Consistency (Run check typically takes < 1s)
    print("  🔍 Konsistenz-Check:  ", end="", flush=True)
    issues = check_consistency()
    if issues == -1:
        print(f"{RED}Fehler (Skript fehlt){RESET}")
    elif issues == 0:
        print(f"{GREEN}Sauber (0 Issues){RESET}")
    else:
        print(f"{RED}{issues} Probleme gefunden{RESET}")
        
    print("")
    recommend_action(phase, next_task, pending, issues)
    print("")

if __name__ == "__main__":
    main()
