---
description: Live-Überwachung und automatische Indexierung des Wikis (Autopilot für das Orakel)
---

# Workflow: `/watch` (Live-Indexierung)

## Interop-Status
- runtime_commands:
  - `7w_wiki.py watch`
  - `7w_wiki.py index --status`
- method_only:
  - `/watch`

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
./7w_wiki.py watch
```

## Voraussetzungen

Stelle sicher, dass die Projekt-Abhängigkeiten gemäß Setup installiert sind (inkl. `watchdog`).
