# Changelog

#### [2026-03-08.01] - Workflow & Skill Consolidation Strategy (Phase E)
### Prioritaet: P1
### Hinzugefügt
- `qa_master.md`, `ingest_master.md`, `lore_master.md`, `tech_master.md`, `meta_master.md` als The 5 Pillars of the 7w_wiki.
### Geändert
- 33 überlappende fragmentierte Workflows in 5 überschaubare, prozesssichere Master-Workflows konsolidiert.
- `/start` Workflow completely rewritten into a persona-routing decision tree.
- `COORDINATION_HUB.md` repaired to reflect the new architecture.
### Gelöscht
- 18 redundante Workflows gelöscht (z.B. `audit.md`, `repair.md`, `ask.md`, `tech.md`, etc.).
### Validiert
- `update_matrix.py` auto-registration.
- `interop-doc-links` passed with 0 broken links.

#### [2026-02-20.03] - Frontmatter Fixes & Ingestion 2.0 (Bote 118, 186-194)
- **P1**
- **Hinzugefügt**:
  - `Siebenwind_Bote_118.md` aus dem Webarchiv (`bote.siebenwind.de`) abgerufen und integriert.
- **Geändert**:
  - `check` CLI: Verbleibende Frontmatter-Inkonsistenzen (Fehlende H1s/Titel-Mismatches) via Custom-Python-Scripting behoben. Die Wiki-Konsistenz-Probleme wurden von 249 auf 0 strukturelle Fehler reduziert (15 kosmetische Rest-Probleme verbleiben).
  - Batch-Ingestion fuer Boten 186-194 verifiziert und durch die Ingest-Pipeline abgeschlossen.
- **Validiert**:
  - `./7w_wiki.py check` (Strukturelle Konsistenz hergestellt)
  - `./7w_wiki.py ingest` für fehlende Boten erfolgreich.
- **P1**
- **Hinzugefügt**:
  - `nexus_config.py`: Zentrales Modul zum Laden der Lore-Manifest Parameter (`WORLD_NAME`, `WIKI_DIR` etc.).
  - `compile_skills.py`: Rendert `.tpl` Dateien in vollwertige `SKILL.md` Files mit injizierten Variablen.
  - `lore.world_name`, `lore.chronology`, `lore.directories` in `lore_manifest.json`.
- **Geändert**:
  - `7w_wiki.py`: Komplett entkoppelt von Hardcodes.
  - `generate_wiki_indices.py`, `generate_wiki_stats.py`, `register_check.py`, `wiki_sanitizer.py`, `advisor.py` migriert auf `nexus_config.py`.
  - `Lore-Gelehrter` Skill auf `.tpl` umgestellt.

#### [2026-02-20.01] - Nordwind Discovery Research & Toran Dur Ingestion
- **P2**
- **Hinzugefügt**:
  - `RESEARCH-2026-017`: Research ticket for the 1 n.H. discovery of Siebenwind (Armgard Torbenson).
  - Neuer Artikel: `Eigenschaften_der_Elemente.md` (Amanda Dunkelbaum).
  - Register: `Ronwo` zum `Personenregister.md` hinzugefuegt.
- **Geändert**:
  - `rvw_loop.md`: Abbruch-Regel bei Überkomplexität (Zwei-Pass-Verfahren) hinzugefügt, um Informationsverlust zu vermeiden.
  - `Amanda_Dunkelbaum.md` um ihr zweites Werk `Eigenschaften der Elemente` erweitert.
  - `MASTER_TASK_LIST.md` aktualisiert.
- **Validiert**:
  - `./7w_wiki.py score` fuer `Eigenschaften_der_Elemente.md`.

#### [2026-02-19.07] - MCP Server Implementation (Model Context Protocol)
- **P1**
- **Hinzugefügt**:
  - **MCP Server**: `System/MCP/server.py` — Thin-Relay-Architektur mit Dual-Mode-Startup (stdio + streamable-http). Delegiert alle Aufrufe an `./7w_wiki.py`. Oracle-Probe mit Grep-Fallback bei Offline-Index.
  - **Auto-Extraction Pipeline**: `System/MCP/generate_mcp_tools.py` — generiert **27 MCP-Tool-Definitionen** automatisch aus `./7w_wiki.py --help-json`. Zero-Maintenance: neuer CLI-Befehl = neues MCP-Tool.
  - **Client Config**: `mcp_config.json` im Repo-Root für Auto-Discovery durch MCP-Clients (Antigravity, Claude Desktop, Cursor).
  - **CLI-Befehl**: `./7w_wiki.py mcp [--transport stdio|streamable-http] [--port 7777]`.
  - **`[QUIP]` Tag**: Neuer offizieller Dispatch-Tag für interdepartmentale Humor-Nachrichten. `wiki_mail_quip` als MCP-Tool (280 Zeichen, Priority LOW, auto-DONE).
  - **Doku**: `System/MCP/README.md` (Quick Start, Daemon Setup, Tool-Liste, Architektur).
- **Geändert**:
  - `AGENTS.md`: MCP-Sektion, Command-Registry-Eintrag, QUIP-Encouragement. Standard auf v1.2 (MCP-Enabled) angehoben.
  - `SY_DISPATCH.md`: `[QUIP]` Tag in der Routing-Sektion ergänzt.
  - `7w_wiki.py`: `mcp` Subcommand (Parser + Handler) hinzugefügt.
- **Validiert**:
  - `generate_mcp_tools.py` generiert 27 Tools (Syntax OK).
  - `server.py` Syntax-Check (PASS).
  - MCP SDK Herkunft verifiziert (offizielles Anthropic Repo `modelcontextprotocol/python-sdk`).
  - Runtime-Test pending (benötigt `pip install 'mcp[cli]'`).

#### [2026-02-19.06] - Full Automation Upgrade: Cleanup, Archivar & v3.0
- **P1**
- **Hinzugefügt**:
  - **Version Management**: `VERSION` Datei als Single Source of Truth. `./7w_wiki.py version [--bump major|minor|patch]` mit automatischer Propagation zu `MASTER_TASK_LIST.md` und `Siebenwind_Wiki/index.md`. Wiki-Standard auf **v3.0** angehoben.
  - **Archivar (Tier C)**: `./7w_wiki.py archive rotate [--dry-run] [--keep-days N]` komprimiert veraltete Logs in datierte `.tar.gz` Archive, rotiert DONE-Dispatches, archiviert abgeschlossene Tickets. `./7w_wiki.py archive unpack <name>` für On-Demand-Entpackung.
  - **Handover Automation**: `archive rotate` und `tech --manifest` als `// turbo` Schritte im Handover-Workflow verankert.
  - **`// turbo` Annotations**: `audit.md`, `docs.md`, `test_run.md` mit Automatisierungsmarkern versehen.
- **Geändert**:
  - **README.md**: Feature-Liste und Tech-Tour auf v3.0 aktualisiert (lint, ingest, archivar, version, JSON API).
  - **AGENTS.md**: `.agents/skills/` Referenz durch `tools.json` und `--help-json` ersetzt.
  - **`tools.json`**: Regeneriert mit 28 Tools (neu: `version`).
- **Entfernt (Tier A Cleanup)**:
  - 12 Dead Scripts nach `.agent/scripts/_archive/` verschoben (source_integrator, fix_absolute_links, fix_bridge_metadata, fix_nested_links, restore_index_links, standardize_filenames, create_stubs, link_guard, refactor_changelog, refactor_master_task_list, metadata_helper, reference_fixer).
  - 8 redundante Bridge Skills aus `.agents/skills/` gelöscht (sanitize, lektor-check, stats, oracle, onboarding, historian, interop-audit, test-run). Nur `art_director` bleibt.
  - `persona_extractor` Skill gelöscht (Vaporware: referenziert nicht-existentes Script).
  - `PRODUCTION_NOTE_TEMPLATE.md` gelöscht (nie verwendet).
- **Behoben (Skill Fixes)**:
  - `time_keeper`: H1 von `# Unknown` auf `# Time Keeper – Sonnenzirkel Kalender` korrigiert.
  - `lektor`: Nutzungssektion auf `./7w_wiki.py check` aktualisiert (statt roher Python-Pfade).
  - `wiki_schmied`: Referenz auf archivierten `metadata_helper.py` entfernt.
- **Validiert**:
  - Archivar Erstlauf: 698 Dateien verarbeitet (445 Audits, 240 Tests, 4 Snapshots, 6 Sessions). `Logs/Archive/`: 755 → 97 Dateien, 24 MB → 10 MB.
  - Version v3.0 erfolgreich propagiert.
  - `tools.json` mit 28 Einträgen regeneriert.

#### [2026-02-19.05] - Inter-AI Compliance Upgrade (6 Pillars)
- **P1**
- **Hinzugefügt**:
  - **Pillar 1: Tool Discoverability**: `./7w_wiki.py tech --manifest` generiert `.agent/config/tools.json` (27 OpenAI-kompatible Tool-Definitionen). Neues Skript `generate_tools_manifest.py`.
  - **Pillar 2: Universal JSON Output**: `--json` Flag für `sanitize`, `check`, `stats` implementiert. `--help-json` liefert das vollständige CLI-Schema als JSON. Neue Tests J-005 bis J-007 in `json-interop-contract.json`.
  - **Pillar 3: Workflow State Persistence**: `--resume` Flag für `start`, `takeover`, `handover`. Zustand wird in `.agent/data/workflow_state.json` persistiert.
  - **Pillar 4: Structured Dispatch Payloads**: `--report-path` in `agent_mail.py` mit 1000-Zeichen Body-Limit (Link Method). `test_runner.py` nutzt die neue Schnittstelle.
  - **Pillar 5: CLI Consolidation**: `./7w_wiki.py lint <target> [--fix] [--json]` orchestriert Sanitizer, Lektor und Lore Score.
  - **Pillar 6: Workflow Orchestration**: `./7w_wiki.py ingest <file>` automatisiert den Zyklus der Weisheit (Lint → Archive Sync → Audit).
- **Geändert**:
  - `sanitize` akzeptiert nun ein optionales Ziel-Argument (Datei oder Verzeichnis).
  - `lore_score_manager.py`: `yaml`-Abhängigkeit entfernt, natives Frontmatter-Parsing.
  - `run_workflow()` zeigt Fortschritt `[i/n]` und unterstützt `// turbo-all` Annotation.

#### [2026-02-19.04] - CLI Robustness & Workflow Automation
- **P1**
- **Hinzugefügt**:
  - `--run` und `--yes` Flags für `start`, `takeover` und `handover` Workflows in `7w_wiki.py` zur automatisierten Ausführung von `// turbo` Kommandos (MSG-2026-0034).
  - `json-interop-contract` Testsuite implementiert, um Maschinenlesbarkeit für `advisor`, `audit`, `mail` und `stats` sicherzustellen.
- **Behoben**:
  - Unterdrückung von `print()` Ausgaben in `advisor.py` und `register_check.py` bei `--json`-Nutzung, behebt JSON-Parsingfehler.
  - Subprozess-Logs in `7w_wiki.py` auf `stderr` umgeleitet, um `stdout`-JSON sauber zu halten.
  - `test_runner.py` Artifact-Speicher auf `/tmp/7w_test_XXXXXX` ausgelagert, schützt vor environment-abhängigen `PermissionError` Crashes in der CI (MSG-2026-0040).

#### [2026-02-19.03] - System Permission Repair Attempts & Diagnostic Handover
- **P1**
- **Geändert**:
  - **Permission Repair**: Erstellung von `repair_permissions.sh` (externer Agent) fur globale xattr-Bereinigung.
  - **Diagnostic**: Umfangreiche Analyse von `Operation not permitted` Fehlern in `Logs/Archive` und Oracle Venv.
  - **Cleanup**: Rekursive Entfernung von `com.apple.provenance` und `com.apple.quarantine` (erfolgreich bei deaktiviertem Sandbox-Modus).
- **Validiert**:
  - `repair_permissions.sh` (User-Execution ohne Fehler).
  - Venv Rebuild (Erfolgreich).
  - **Sandbox-Check**: `Operation not permitted` persistiert bei aktiviertem Sandbox-Modus.
  - **Fix / Workaround**: Deaktivierung von "Enable Terminal Sandboxing" in den Antigravity-Einstellungen löst die Blockade vollständig auf.

#### [2026-02-19.02] - Dispatch Hygiene & Link-Flood Restoration
- **P1**
- **Geändert**:
  - **Dispatch**: Bulk-Closing von 32 redundanten OPEN-Nachrichten (`MSG-2026-0033` abgeschlossen).
  - **Link Repair**: Semantische Wiederherstellung von 1034 korrupten `[[index]]`-Links in 517 Dateien (Kategorien, Header, Body).
  - **Standardisierung**: Unifizierung von `[[Toran_Dur]]`-Links (36 Fixes) und Ergänzung verpflichtender Bridge-Metadaten für 20 Platzhalter (Interop Norm 1b).
- **Behoben**:
  - **Permissions**: Eskalation von `Operation not permitted` Fehlern in `Logs/Archive` via Dispatch `MSG-2026-0042`.
- **Validiert**:
  - `grep` Verifikation (0 verbleibende korrupte Index-Links).
  - `test --suite clean-client-state` (PASS).
  - Manuelle Stichproben in `Anijane_Lavid.md` und `Personenregister.md`.

#### [2026-02-19.01] - UI/UX Polish: Search Fix & Landing Page Unification
- **P1**
- **Geändert**:
  - **Search UX**: `z-index` Fix in `custom.css` behoben; Suchergebnisse überlagern nun nicht mehr den Content.
  - **Landing Pages**: Vereinheitlichung aller Kategorie-Indizes (`00_Fundament` bis `10_Archiv`) auf das "Siebenwind Archiv" Design (Hero Header + Grid Layout).
  - **Wiki-Root**: `Siebenwind_Wiki/index.md` als visueller Content-Hub neugestaltet.
- **Validiert**:
  - Manuelle Code-Review der Landing-Pages (Aesthetic Consistency).

#### [2026-02-18.13] - JSON API & Test Suite Audit
- **P1**
- **Hinzugefügt**:
  - **JSON API**: `--json` Flag für `advisor`, `audit`, `search` und `mail inbox` für maschinenlesbare Automation.
  - **Messaging Enhancements**: Fuzzy-ID Matching (z.B. `32` für `MSG-2026-0032`), Auto-Claim bei `mail done`, Force-Claim Option.
  - **Test Suite Audit**: Formaler Bericht `Logs/Reports/2026-02-18_Test_Suite_Audit.md` und Dispatch `MSG-2026-0040`.
- **Geändert**:
  - `AGENTS.md`: Mandatory Mission Reports und Inquisitive Protocol verankert.
  - `SY_DISPATCH.md`: Dokumentation der neuen Messaging-Features.
  - `search.py`: ASCII-Banner bei JSON-Output unterdrückt.
- **Validiert**:
  - `./7w_wiki.py advisor --json` (PASS)
  - `./7w_wiki.py search "Tiamat" --json` (PASS)
  - `./7w_wiki.py audit --json` (PASS)
  - `./7w_wiki.py mail claim --force` (Funktional)

#### [2026-02-18.12] - Link Integrity Restoration & Precision Repair
- **P1**
- **Geändert**:
  - **Link Engine**: Rollback von `ezlinks` auf `roamlinks` zur Behebung von 404-Fehlern auf GitHub Pages.
  - **Infrastruktur**: Migration von `docs/` Symlinks zu physischen Verzeichnissen.
  - **Massen-Reparatur**: 502 Links in `Quellen/` (Spielergeschichten) via `repair.py` normalisiert.
  - **Geografie**: "Grünland" (ex Grönlanden) normalisiert, Stub erstellt und Duplikate in `Siebenwind.md` entfernt.
- **Hinzugefügt**:
  - `RESEARCH-2026-012` (Auftrag für Grünland-Forschung).
- **Validiert**:
  - `./7w_wiki.py pages build` (PASS)
  - `grep` Verifikation der Pfade in `site/` (PASS)

#### [2026-02-18.11] - Oracle Stability & Bridge Rewrite Batch 1
- **P1**
- **Hinzugefügt**:
  - `--fast` Mode in `search.py` für schnellere Suche ohne Re-Ranking.
  - Automatischer MPS-Fallback bei Permission-Errors (`mpsgraph`) in `search.py` und `build_index.py`.
- **Geändert**:
  - **Link-Migration (Batch 1)**: 64 Dateien aktualisiert, um Brückenartikel (Vitama, Adel, Gesellschaft) zu eliminieren.
  - Obsolete Brückendateien (10 Stk) nach `Siebenwind_Wiki/10_Archiv/Cleanup_2026-02-18/` archiviert.
  - `MASTER_TASK_LIST.md` und `AGENT_DOSSIER_2026-02-18_BRIDGE_REWRITE_PROGRAM.md` auf den neuesten Stand gebracht.
- **Validiert**:
  - `./7w_wiki.py search "Aequitas" --fast` (Latency ~14.5s)
  - `python3 archive_bridge_files.py` (Archivierung erfolgreich)
  - `./.agent/skills/oracle/venv/bin/python3 .agent/skills/oracle/build_index.py --cpu` (Index stabil)



*Ältere Einträge siehe [Archiv](docs/Archiv/CHANGELOG_ARCHIVE_FEB_2026.md)*
