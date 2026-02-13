---
description: Live-Überwachung und automatische Indexierung des Wikis (Autopilot für das Orakel)
---

# Workflow: `/watch` (Live-Indexierung)

Dieser Workflow aktiviert den **Autopiloten** für das Orakel. Er etabliert eine Live-Überwachung der Wiki- und Quellen-Verzeichnisse.

## Funktionsweise

Ein Python-Skript (`watcher.py`) nutzt die `watchdog`-Bibliothek, um Dateisystem-Events zu überwachen.
Wenn eine Markdown-Datei gespeichert (`MODIFIED`) oder umbenannt (`MOVED`) wird, triggert der Watcher **sofort** ein inkrementelles Update des Orakel-Index für exakt diese Datei.

Das bedeutet:
- **Keine Wartezeiten:** Wissen ist sofort suchbar.
- **Kein manuelles Bauen:** `build_index.py` muss nicht mehr händisch ausgeführt werden.

## Nutzung

Der Watcher muss im Hintergrund laufen (z.B. in einem separaten Terminal-Tab).

```bash
# Starten (blockiert das Terminal)
.agent/skills/oracle/venv/bin/python3 .agent/scripts/watcher.py
```

## Voraussetzungen

Stelle sicher, dass `watchdog` installiert ist (Teil von `setup.sh` seit v2.0).
Falls nicht:
```bash
.agent/skills/oracle/venv/bin/pip install watchdog
```
