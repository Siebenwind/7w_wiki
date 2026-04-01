# Master Task List: Siebenwind-Wiki-Rekonstruktion

Dieses Dokument dient als agentenübergreifendes Gedächtnis. Es trennt den **aktiven Fokus** von der **Projekthistorie** und definiert klare Standards für die Aufgabenpriorisierung.

## 📊 Status-Übersicht
- **Wiki-Standard:** v3.0 (Inter-AI Compliant)
- **RAG-Status (Orakel):** Aktiv & Sandbox-Resilienz (v1.1)
- **Last Handover**: 2026-03-10 14:45 (Codex → Next Agent)
- **Status**: Die konservative Lane-1-Welle ist umgesetzt; Contract-Drift wurde stark reduziert. Die Pantheon-Navigation ist nun symmetrisch und die Begriffe `Viere/Sahor` sowie `Elementarherren/Enhor` sind auf den Kernseiten ausgerichtet. Religions-, Historie- und nun auch der Magie-Cluster sind abgearbeitet; die publizierten Ingestion-Reports der Magie-Familie verweisen jetzt auf präzise Theorie- und Ritualseiten. Der harte Pages-Snapshot liegt nun bei `703` unresolved und `701` unallowlisted. Aktueller Fokus verschiebt sich damit auf den semantisch heikleren Cluster `Dämonen`, flankiert von reportartigen Restzielen wie `Die_Sammler` und `WikiLinks`, dazu weiter Quellenpfade und die `88` Bridge-Seiten.

---

## 🔴 Priorität 1: Aktueller Fokus (Next Step)

- [ ] **Pages Backlog Cluster Repair**: Die konservative Lane-1-Welle ist gelaufen, Religions-, Historie- und Magie-Cluster sind erledigt. Der harte Gate-Lauf steht aktuell bei `703` unresolved und `701` unallowlisted Pages-Zielen. Der naechste Hauptcluster ist jetzt `Dämonen` mit dem kanonischen Kandidaten `Daemonen`, weil dort sowohl aktive Wiki-Seiten als auch Quellenmaterial betroffen sind. Daneben bleiben report-/resolverlastige Restziele wie `Die_Sammler` und `WikiLinks` als separater Techniktrack sichtbar.

- [ ] **Zeitstrahl Structural Repair**: `docs/Siebenwind_Wiki/05_Geschichte/Zeitstrahl.md` ist ueber den reinen `Historie`-Linkfehler hinaus deutlich beschaedigt und enthaelt eingebettete Fremdseitenfragmente. Dieser Defekt wurde im Historie-Cluster bewusst nicht miterledigt und braucht einen eigenen, strukturorientierten Reparaturtrack.

- [ ] **Backlog Board & Escalation Follow-Up**: Das aktuelle Cluster-Board liegt unter `.agent/data/backlog_cluster_board.json`, die Eskalationsliste unter `.agent/data/backlog_escalations.json`. Der naechste Agent soll diese Artefakte als Arbeitsgrundlage verwenden statt erneut ungeclustert in `audit --pages` einzusteigen.

- [x] **Religions-Cluster Resolver Follow-Up**: Die Review-Grundlage liegt unter `.agent/data/religion_cluster_review.json` und `.agent/data/religion_cluster_escalations.json`. Der Folgeschritt ueber publizierte Ingestion-Reports und Maintainer-Doku ist erfolgt; Religions-Restziele wurden aus dem aktiven Repair-Fokus in dokumentierte Historie ueberfuehrt.

- [ ] **Bridge Lifecycle Cleanup**: Das Backlog-Board trennt die `88` invaliden Bridges jetzt in `84` Single-Target-Bridges (`bridge_single_target_review`) und `4` echte Eskalationen (`bridge_escalation`). Naechster Schritt: die `84` Kandidaten clusterweise gegen semantische Verluste pruefen und nur die `4` Mehrdeutigkeiten separat eskalieren.

- [ ] **Source Path Canonicalization fuer Quellen**: Lane 1 hat eindeutige `quelle:`-Lookups bereits gehoben, aber der Quellenbaum mischt weiter Leerzeichen- und Unterstrich-Dateinamen. Der naechste Schritt ist ein strikter lookup-basierter Normalizer fuer die verbliebenen Boten-Faelle (`176`, `178`-`182`, `185`) und vergleichbare Mehrdeutigkeiten.

- [x] **Runtime Telemetry & Fast Pages Precheck**: `pages validate --fast` existiert jetzt als advisory Vorcheck; `pages validate --json` und `audit --pages --json` liefern Timing-/Cache-Metadaten fuer weitere Performance-Arbeit.

- [x] **Drift-Prevention Governance Alignment**: AGENTS, Handbuch, Interop, Testing und Workflow-Texte bilden die Regel `Homepage > Quellen > Wiki Pages` sowie `docs/Siebenwind_Wiki/` als technischen Edit-Baum nun konsistent ab. Der Volltext liegt in `System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md`.

- [x] **Phase E (Workflow & Skill Consolidation)**: Pruned 33 fragmented workflows into 5 core Master Workflows mapped to the 5 Agent Personas. Built a sharp decision tree in `/start` and preserved all sub-processes.
- [x] **Interop Hardening (Typed CLI + Doc Sync)**: `--help-json`, `tools.json`, MCP, governance docs und die Workflow-Matrix sind nun auf denselben typisierten Runtime-Vertrag ausgerichtet. `scout` bleibt als prominenter Sonderfall sichtbar, ohne die `.agent/scripts/`-Policy zu brechen.
- [x] **Pages Integrity & Tech Cadence Hardening**: `audit --pages`, `pages validate --json [--strict-links]`, `repair --fix-roamlinks`, Pages-Policy/Snapshot und Advisor-Freshness machen publizierte Site-Integritaet jetzt explizit sichtbar und als Standard-Loop fuer `/tech_master`, `/qa_master`, `/start`, `/takeover` und `/handover` nutzbar.
- [x] **Codex Workflow Bridges & Forum Search Split**: Generierte Workflow-Bridges in `.agents/skills/` machen `start`, `takeover`, `handover`, `tech_master`, `test_run` und die neue Forenquellenjagd `/forum_search` fuer Codex discoverbar; `/scout` bleibt der breite Discovery-Einstieg.
- [x] **Workflow Bugfix (`/handover --run`)**: Schritt 5 leitet `mail post` jetzt automatisch aus der neuesten `SESSION_MEMORY_*.md` ab (`--from Oberarchivar --to Coordinator --report-path ...`) und laeuft ohne manuellen Workaround durch. Tracking: `MSG-2026-0058`.

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

*Aktiver Drift-/Pages-Vertrag:* `System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md`


Die vollständige Projekthistorie (v1.0 bis v3.0) wurde archiviert unter: `docs/Archiv/PROJECT_HISTORY.md`
