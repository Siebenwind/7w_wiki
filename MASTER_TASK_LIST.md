# Master Task List: Siebenwind-Wiki-Rekonstruktion

Dieses Dokument dient als agentenübergreifendes Gedächtnis. Es trennt den **aktiven Fokus** von der **Projekthistorie** und definiert klare Standards für die Aufgabenpriorisierung.

## 📊 Status-Übersicht
- **Wiki-Standard:** v3.0 (Inter-AI Compliant)
- **RAG-Status (Orakel):** Aktiv & Sandbox-Resilienz (v1.1)
- **Last Handover**: 2026-02-20 00:20 (Antigravity → Next Agent)
- **Status**: Ingestion Batch 2 (Toran Dur) started, RESEARCH-2026-017 initiated.

---

## 🔴 Priorität 1: Aktueller Fokus (Next Step)


- [ ] **Workflow Bugfix (`/handover --run`)**: Schritt 5 ruft `mail post` ohne Pflichtparameter auf und endet mit Exit 1. Workaround aktiv: manueller `mail post` mit Parametern. Tracking: `MSG-2026-0058`.

- [x] **Handover Gate Repair**: Defekten Link in `.agent/workflows/handover.md` behoben; `interop-doc-links` und `takeover-handover` wieder gruen.
- [x] **Test Runner Stability**: Runner mit Case-Progress-Ausgabe erweitert; `rag-relevance-smoke` aus Standardlauf (`--suite all`) entfernt und nur noch per `--include-rag` / direkter Suite ausfuehrbar.
- [x] **Oracle Reliability (Codex App)**: Auftrag `MSG-2026-0015` abgeschlossen; MPS Permission Fallback implementiert und `--fast` Mode für niedrige Latenz hinzugefügt.
- [x] **Advisor API fuer Automationen**: Auftrag `MSG-2026-0032` abgeschlossen; `advisor`, `search`, `audit` und `mail inbox` unterstuetzen nun `--json`.
- [x] **Test Suite Audit**: Umfassendes Audit (`MSG-2026-0040`) deckt Schwachstellen in `reader-stats-contract` (Permissions) und fehlende Logik-Tests auf.
- [x] **Dispatch Queue Hygiene**: Auftrag `MSG-2026-0033` abgeschlossen; Bulk-Closing von 32 redundanten Nachrichten. Backlog konsolidiert.
- [x] **Audit Regression Triage**: Semantische Reparatur (index-flood) über 517 Dateien durchgeführt (1034 Fixes). `Toran_Dur` vereinheitlicht und Bridge-Metadaten standardisiert.
- [x] **Technical Link Repair**: Restored `roamlinks` and normalized 500+ links via `repair.py` to overcome 404s on GitHub Pages.
- [x] **UI/UX Polish**: Unified "Siebenwind Archiv" aesthetic across all category landing pages (`Siebenwind_Wiki/index.md`, `00_Fundament`, etc.) and fixed search overlap.
- [x] **System Permission Repair**: Resolve persistent `Operation not permitted` errors in `Logs/Archive` by disabling "Enable Terminal Sandboxing" in Antigravity settings.
- [x] **MCP Server**: Model Context Protocol Server implementiert (`System/MCP/`). 27 Tools, Dual-Mode Architektur (Daemon + Agent-Fallback), Auto-Extraction Pipeline, `[QUIP]` Mail-System. Dependency: `pip install 'mcp[cli]'`.
- [x] **Ingestion 2.0**: Fortsetzung der Boten-Verarbeitung (Bote 118, Bote 186+) - Erfolgreich importiert und integriert.

## 🟡 Priorität 2: Operative Ingestion & Research
- [ ] **Kanon-Abgleich**: Wiederaufnahme der Prüfung zur Götterverschmelzung (RESEARCH-2026-010/011) - [DEFERRED].
- [x] **[MSG-2026-0034]** [P2][DEV] Workflow-Execute-Mode + Alias advisor: Integration von `--run` für start/takeover/handover und Alias-Normierung.
- [x] **[MSG-2026-0040]** Test Suite Status: Tests in `/tmp` entkoppelt und JSON-Verträge etabliert.
- [ ] **Massen-Ingestion**: Integration der verbleibenden Quellen (Status `Pending`).
- [ ] **Lore Research Board**: Abarbeitung der offenen Ausschreibungen (Angamon, Ödland).

## 🔬 Aktuelle Lore-Ausschreibungen (Research Board)
*Detaillierte Aufträge siehe [[LORE_RESEARCH_BOARD.md]]*

| ID | Thema | Priorität | Status |
| :--- | :--- | :--- | :--- |
| [[RESEARCH-2026-001]] | Die Neun Domänen des Angamon | 🔴 | [ ] Offen |
| [[RESEARCH-2026-002]] | Die Transformation des Ödlands | 🟡 | [ ] Offen |
| [[RESEARCH-2026-003]] | Die Linari-Matrix | 🟡 | [ ] Offen |
| [[RESEARCH-2026-007]] | Dossier Rhadan (Zeichnung Tares) | 🔴 | [ ] Offen |
| [[RESEARCH-2026-012]] | Das Grünland (Geografie & Siedlung) | 🔴 | [ ] Offen |
| [[RESEARCH-2026-017]] | Die Entdeckung Siebenwinds (1 n.H.) | 🟡 | [x] Bearbeitung |

## 🔵 Priorität 3: Qualität & Politur (Optimierung)
*Verbesserungen an System und Lore, die den Nutzwert steigern.*

- [ ] **Chronik-Konsolidierung**: Abgleich der neuen Erkenntnisse aus den Spielergeschichten mit der offiziellen [[Zeitrechnung_(Der_Sonnenzirkel).md]].
- [ ] **Feature: „Der Kartograph“**: Implementierung eines Skills zur geografischen Datenverwaltung und Reisezeiten-Berechnung.

## ⚪ Backlog / Future (Ideenspeicher)
*Langfristige Ziele ohne aktuelle Zeitplanung.*

- [ ] **Skill: „Der Herold“**: Automatisches News-Broadcasting basierend auf Wiki-Änderungen.
- [ ] **Workflow: `/map_sync`**: Visuelle Verknüpfung von Wiki-Entitäten mit einer externen Karte.
- [ ] **Workflow: `/cleanup`**: Vollautomatisierter Bot zur kontinuierlichen Pfad-Bereinigung.

---

## 🗂️ Projekthistorie (neu → alt)


Die vollständige Projekthistorie (v1.0 bis v3.0) wurde archiviert unter: [[docs/Archiv/PROJECT_HISTORY.md]]
