---
description: Department Master Workflow für Projekt-Meta, Statistiken und Handover
---

# Department: 📦 Logistik & Koordination (/meta_master)

Dieses Department ist das Revier des **Koordinators**. Es regelt den Agenten-Alltag, die Dokumentation, Statistiken, den Wissenstransfer und die Einhaltung des menschlichen Leitpunkts. Es fusioniert die Workflows `/meta_master`, `/stats` und `/leitpunkt`.

## Interop-Status
- runtime_commands:
  - `7w_wiki.py start`
  - `7w_wiki.py stats`
  - `7w_wiki.py leitpunkt [status|check|scaffold]`
  - `7w_wiki.py test --suite reader-stats-contract`
  - `7w_wiki.py test --suite clean-client-state`
  - `7w_wiki.py test --suite pages-contract-mode-contract`
  - `7w_wiki.py mail inbox --status OPEN`
  - `7w_wiki.py mail post --from Coordinator --to <agent|ALL> --subject "<text>" --body "<text>"`
- method_only:
  - `/meta_master`
  - `/takeover`
  - `/handover`

## 1. Onboarding & Steuerung
1. Führe zu Beginn `/start` oder `/takeover` aus.
2. Analysiere den **Advisor-Report** (`./7w_wiki.py advisor`).
3. **Leitpunkt-Check [PFLICHT]:** Prüfe die Vorgaben des menschlichen Maintainers.
   - `./7w_wiki.py leitpunkt status`
   - `./7w_wiki.py leitpunkt check`
   - Halte dich strikt an die Prioritäten und No-Gos in `docs/Archiv/MAINTAINER_STANDPUNKT.md`.

## 2. Statistiken & Tracking
Halte das Wiki für Leser und Maschinen transparent.
// turbo
1. `./7w_wiki.py stats`
2. `./7w_wiki.py test --suite reader-stats-contract`

*Hinweis: Dieser Befehl synchronisiert automatisch:*
- `docs/Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md` (Leseransicht)
- `Logs/INGESTION_TRACKING_REGISTER.md` (Technikdetail)
- `Logs/Archive/STATS_SNAPSHOT_latest.json` (maschinenlesbare Schnittstelle)

## 3. Dokumentation & Boards (Daily Business)
1. **Boards:** Halte die `MASTER_TASK_LIST.md` und `System/Synapse_Board/` aktuell. Räume erledigte Tasks auf.
2. **Publicity:** Aktualisiere `README.md` und `CHANGELOG.md` nach großen Meilensteinen. Arbeite hierfür mit dem `/herold` zusammen.
3. **Interop Checks:** Führe regelmäßig `./7w_wiki.py test --suite clean-client-state` und `./7w_wiki.py test --suite pages-contract-mode-contract` aus, um Repo- und Pages-Hygiene zu garantieren.
4. **Tech Freshness:** Beobachte im `advisor` die Felder `Pages Health` und `last_sync_interop_at`, damit `/tech_master` nicht veraltet.

## 4. Kommunikation (Dispatch)
Als Koordinator bist du der Node-Point für Informationen:
1. Nutze `./7w_wiki.py mail post --to ALL ...` um systemweite Änderungen anzukündigen (z.B. neue Kanon-Regeln, Leitpunkt-Updates).
2. Hole Nutzer-Entscheidungen aktiv über das CLI oder `/decide` ein, wenn Agenten blockiert sind.

## 5. Handover
Am Ende deiner Session oder Schicht:
1. Erstelle ein Übergabeprotokoll (`/handover`) für den nächsten Agenten in `Logs/Archive/SESSION_MEMORY_YYYY-MM-DD_META.md`.
2. Committe alle Änderungen mit aussagekräftigen Nachrichten (z.B. `docs(meta): updated global statistics and resolved 3 dispatch tickets`).

#meta #logistik #handover #dokumentation #stats
