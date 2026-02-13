#!/usr/bin/env python3
"""
watcher.py — Live-Indexierung für das Siebenwind Wiki.

Nutzt `watchdog`, um Änderungen an .md Dateien zu erkennen und sofort
den Index für diese Dateien zu aktualisieren.

Nutzung:
    .agent/skills/oracle/venv/bin/python3 .agent/scripts/watcher.py
"""

import sys
import time
import subprocess
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# --- Configuration ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
WATCH_DIRS = [
    PROJECT_ROOT / "Siebenwind_Wiki",
    PROJECT_ROOT / "Quellen"
]
BUILD_INDEX_SCRIPT = PROJECT_ROOT / ".agent" / "skills" / "oracle" / "build_index.py"
PYTHON_BIN = sys.executable  # Use current venv python

class WikiEventHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_trigger = {}
        self.debounce_seconds = 2.0

    def on_modified(self, event):
        if event.is_directory:
            return
        self._process(event.src_path)

    def on_moved(self, event):
        if event.is_directory:
            return
        # Indexiere die NEUE Datei. Die alte wird beim nächsten Full-Scan irgendwann "gelöscht" erkannt,
        # oder wir könnten hier auch explizit löschen, aber build_index --file unterstützt nur update.
        self._process(event.dest_path)

    def _process(self, filepath):
        path = Path(filepath)
        if path.suffix.lower() != ".md":
            return
            
        # Debounce
        now = time.time()
        if filepath in self.last_trigger:
            if now - self.last_trigger[filepath] < self.debounce_seconds:
                return
        self.last_trigger[filepath] = now

        print(f"\n[WATCHER] Änderung erkannt: {path.name}")
        
        # Call build_index.py
        try:
            cmd = [PYTHON_BIN, str(BUILD_INDEX_SCRIPT), "--file", str(path)]
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[ERROR] Indexierung fehlgeschlagen: {e}")
        except Exception as e:
            print(f"[ERROR] Unerwarteter Fehler: {e}")

def main():
    print("╔═══════════════════════════════════════════════════╗")
    print("║   Das Orakel – Autopilot (Live-Indexierung)      ║")
    print("╚═══════════════════════════════════════════════════╝")
    print(f"Überwache Verzeichnisse:")
    for d in WATCH_DIRS:
        print(f"  - {d}")
    print("\nDrücke Ctrl+C zum Beenden.\n")

    event_handler = WikiEventHandler()
    observer = Observer()
    
    for d in WATCH_DIRS:
        if d.exists():
            observer.schedule(event_handler, str(d), recursive=True)
        else:
            print(f"⚠️  Warnung: Verzeichnis existiert nicht: {d}")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()
