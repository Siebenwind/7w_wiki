# Master Task List: Siebenwind-Wiki-Rekonstruktion

Dieses Dokument dient als agentenübergreifendes Gedächtnis. Es trennt den **aktiven Fokus** von der **Projekthistorie** und definiert klare Standards für die Aufgabenpriorisierung.

## 📊 Status-Übersicht
- **Wiki-Standard:** v3.0 (Inter-AI Compliant)
- **RAG-Status (Orakel):** DEGRADED; lokaler Modell-/Indexcache fehlt, direkte Quellenprüfung bleibt der aktive Fallback (`MSG-2026-0192`).
- **Last Handover**: 2026-08-04 (Codex → Next Agent)
- **Status**: Der Forumprozess umfasst 201 registrierte Themen: 101 Volltexte sind archiviert, 74 davon integriert, fünf ohne Wikiänderung abgeschlossen und 22 warten auf fachliche Sichtung; 100 Themen liegen erst als Metadaten vor. Der aktuelle Wiki-Snapshot umfasst 1.417 Artikel und 115 vollständig getrackte Ingestion-Berichte. Der jüngste Historikerlauf ist in `Logs/Archive/SESSION_MEMORY_2026-08-06_HISTORIKERLAUF_109571_BIS_108788.md` dokumentiert; Audit und Pages-Drift sind sauber, der bekannte globale Linkaltbestand bleibt separat offen.

---

## 🔴 Priorität 1: Aktueller Fokus (Next Step)

- [x] **Layout-Contract Cleanup & Audit-Zaehllogik**: Die `layout`-Altfelder aus den audit-relevanten Seiten wurden entfernt; `audit --json` meldet keine `legacy_field: layout`-Verletzungen mehr und weist den verbleibenden Ingestion-Score-Cluster konsistent unter `details.ingestion_issues` aus.

- [x] **Zeitstrahl Structural Repair**: `docs/Siebenwind_Wiki/05_Geschichte/Zeitstrahl.md` wurde von einem strukturell korrumpierten Mischdokument auf eine kompakte Chronik-Uebersicht mit Verweisen auf `Historie & Aeren` und `Zeitleiste (15-30 n.H.)` zurueckgefuehrt.

- [ ] **Semantic Pages Backlog Triage**: Die aktuelle Pages-Validierung meldet `624` unresolved Targets, `622` unallowlisted, `611 needs_historian` und `5 generic_term_conflict`; nur das Strict-Link-Gate bleibt hart. `drift_status = PASS`, und `repair --apply-lane1 --dry-run --json` plant aktuell `0` sichere mechanische Dateiedits. Der naechste Agent soll die bestehenden Board-/Backlog-Artefakte (`.agent/data/backlog_cluster_board.json`, `.agent/data/backlog_escalations.json`, `RESEARCH-2026-018`) als Arbeitsgrundlage verwenden und die semantische Begriffsarbeit strikt von mechanischen Reparaturen trennen.

- [x] **Forum-Ingestion v2 Pilot**: Die Forum-Volltextarchivierung und agentische Verarbeitung sind als Runtime-Pfad umgesetzt. Zwei Pilotquellen sind integriert (`Ergon` als Update, `Orkisches Handelskontor` als Neuanlage), das Forumregister bleibt bei `201` Eintraegen mit `2 integrated`, und die Draft-Stilregel verhindert kuenftig OOC-Formulierungen im Artikelkoerper.

- [x] **Fallback `[[index]]`-Platzhalterbereinigung**: Das Orakel/RAG war fuer diese Session nicht funktionstuechtig; die Bereinigung wurde deshalb ueber direkte `rg`-Suchen, Kontextlektüre und konservative Klartext-Ersetzungen durchgefuehrt. Ergebnis: `rg "\[\[index\]\]" docs/Siebenwind_Wiki -g '*.md'` findet keine Treffer mehr; unklare Stellen wurden nicht erfunden, sondern mit `[UNGEKLÄRT]` markiert.

- [ ] **Pages-Linkbacklog nach `[[index]]`-Welle**: Nach der Platzhalterbereinigung ist der naechste operative Block der allgemeine Pages-Linkbacklog aus `./7w_wiki.py pages validate --contract --json`: zuerst `safe_exact_match` und `planned_fix`, dann `generic_term_conflict`, danach die `needs_historian`-Ziele.

- [ ] **Review- und Scan-Restbestand schliessen**: `RESEARCH-2026-004` und `RESEARCH-2026-007` stehen weiter auf `IN_REVIEW_HISTORIAN`, waehrend der Forum-Scan fuer `2` allowlistete Boards als stale gilt. Der naechste Agent soll entscheiden, ob zuerst die Historian-Reviews publiziert/geschlossen oder die Foren-Pipeline reaktiviert wird.

- [x] **Forum-Historikerlauf – fünf Quellen (`MSG-2026-0229`)**: Die Topics `31020`, `48524`, `109905`, `107595` und `109867` wurden in der festgelegten Reihenfolge quellenkritisch integriert. Vier neue Leserartikel entstanden, zwölf bestehende Seiten wurden inhaltlich oder als Linkziel aktualisiert und der abgelaufene Brückenplatzhalter `Rasse Orken.md` wurde nach Linkhebung entfernt. Alle fünf Quellen stehen im Forumregister auf `integrated`; Details stehen in `Logs/Archive/SESSION_MEMORY_2026-08-05_HISTORIKERLAUF_31020_BIS_109867.md`.
- [x] **Forum-Historikerlauf – fünf Quellen (`109571` bis `108788`)**: Die Topics `109571`, `109483`, `108944`, `109310` und `108788` wurden quellenkritisch integriert. Fuenf Erzaehlungsartikel, die neue Personenseite Volandurs und substanzielle Aktualisierungen an Maichellis, Akassvae, Huns, Brandenstein, Falkenwall und Claiomhs Wacht verbinden Perspektivtexte mit den Boten 132/133 und 191/193/194. Details stehen in `Logs/Archive/SESSION_MEMORY_2026-08-06_HISTORIKERLAUF_109571_BIS_108788.md`.

- [x] **Residual Bridge Decision Gate**: `MSG-2026-0089` ist abgeschlossen; `docs/Siebenwind_Wiki/00_Fundament/Arman_von_Draconis.md` verweist temporaer auf `[[Arman]]`, `bridge_inventory.invalid = 0`, und der fruehere P1-Blocker ist damit aus dem aktiven Fokus gefallen.

- [x] **Wave 2: Pages Surface Hardening & Root-Tree Retirement**: `Siebenwind_Wiki/` wurde als physischer Altbaum entfernt, `pages validate --contract --json` als deterministischer Vertragsmodus eingefuehrt, `docs/assets/` auf produktive Assets begrenzt und die Maschinenoberflaechen auf `legacy_root_status = removed` umgestellt.

- [x] **Bridge Blocker Pass**: `00_Religion_Uebersicht` und `03_Gesellschaft` wurden auf ihre kanonischen Zielartikel gehoben; fuer `Werke_index` entstand mit `docs/Siebenwind_Wiki/03_Wissen/Werke.md` ein stabiler Landing-Artikel. Ergebnis: `audit --json` fiel von `9` auf `3` Issues, `bridge_inventory.invalid` von `4` auf `1`.

- [x] **Religions-Cluster Resolver Follow-Up**: Die Review-Grundlage liegt unter `.agent/data/religion_cluster_review.json` und `.agent/data/religion_cluster_escalations.json`. Der Folgeschritt ueber publizierte Ingestion-Reports und Maintainer-Doku ist erfolgt; Religions-Restziele wurden aus dem aktiven Repair-Fokus in dokumentierte Historie ueberfuehrt.

- [x] **Bridge Lifecycle Cleanup**: Die `84` Single-Target-Kandidaten wurden gegen semantische Verluste geprueft und mit temporaerer Bridge-Metadatenhygiene versehen. Uebrig geblieben sind nur die `4` echten Eskalationen (`bridge_escalation`), die jetzt bei Historian/Coordinator liegen.

- [x] **Source Path Canonicalization fuer Quellen**: Die defekten Root-Symlinks fuer `Siebenwind Bote 176`, `178`-`182` und `185` wurden auf die kanonischen Rohquellen im Quellenbaum umgehoben. Der bekannte `strict-links`-Precheck scheitert damit nicht mehr an fehlenden Datei-Zielen, sondern nur noch an den vier semantischen Bridge-Resten.

- [x] **Pages Backlog Cluster Repair**: Der `Dämonen`-Drift wurde auf `Daemonen` gehoben, die defekten Quellenpfade wurden repariert und `repair --fix-roamlinks --auto` nachgezogen. Ergebnis: `audit --json` sank von `173` auf `9` Issues; der operative Massen-Backlog ist damit in einen kleinen Entscheidungsrest ueberfuehrt.

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
- [x] **Kanon-Abgleich (RESEARCH-2026-010/011)**: `MSG-2026-0005` ist abgeschlossen; der Bericht `Logs/Research/RESEARCH-2026-010-011_Summary.md` trennt jetzt sauber zwischen Live-Kanon (`Astrael` ohne Goetterverschmelzung) und historischem Projekt-/Plotstatus (`Waldelfen`/`Myten` als Diaspora bzw. inaktive Rassen statt Weltloeschung).
- [x] **[MSG-2026-0034]** [P2][DEV] Workflow-Execute-Mode + Alias advisor: Integration von `--run` für start/takeover/handover und Alias-Normierung.
- [x] **[MSG-2026-0040]** Test Suite Status: Tests in `/tmp` entkoppelt und JSON-Verträge etabliert.
- [ ] **Massen-Ingestion**: Zwei offizielle Newsquellen stehen auf `pending`: `2025-10-30_Kuerbisschreck.md` und `2025-12-15_Ankuendigung_Dunkeltief.md`.
- [ ] **Forum-Queue Batchweise verarbeiten**: Nach den Piloten weitere Forumquellen über `ingest forum-queue`, `forum-inspect`, `forum-draft` und `forum-finalize` bearbeiten. Aktueller Registerstand: `201` Themen, davon `101` volltextarchiviert, `74` integriert, `5` ohne Wikiänderung abgeschlossen, `22` Volltexte fachlich offen und `100` nur als Metadaten vorhanden. Das nächste Fünferpaket beginnt mit `106975` („Der alte Aktenschrank“), danach folgen `109430`, `109411`, `103341` und `99477`. Nächster zulässiger Metadatenkandidat bleibt Topic `108636` (`Pflicht`); Topic `104857` wird wegen seiner bestehenden Dublettenentscheidung korrekt übersprungen.
- [ ] **Lore Research Board**: Abarbeitung der offenen Ausschreibungen (Angamon, Ödland).

## 🔬 Aktuelle Lore-Ausschreibungen (Research Board)
*Detaillierte Aufträge siehe [[LORE_RESEARCH_BOARD.md]]*

| ID | Thema | Priorität | Status |
| :--- | :--- | :--- | :--- |
| [[RESEARCH-2026-001]] | Die Neun Domänen des Angamon | 🔴 | [ ] Offen |
| [[RESEARCH-2026-002]] | Die Transformation des Ödlands | 🟡 | [ ] Offen |
| [[RESEARCH-2026-003]] | Die Linari-Matrix | 🟡 | [ ] Offen |
| [[RESEARCH-2026-004]] | Causa Tjure Odal & Arn Toron | 🔴 | [x] Review |
| [[RESEARCH-2026-007]] | Dossier Rhadan (Zeichnung Tares) | 🔴 | [x] Review |
| [[RESEARCH-2026-018]] | Magie/index-Disambiguierung nach mechanischer Linkwelle | 🔴 | [x] Operativ bereinigt; Rest ist Pages-Linkbacklog |
| [[RESEARCH-2026-012]] | Das Grünland (Geografie & Siedlung) | 🔴 | [ ] Offen |
| [[RESEARCH-2026-017]] | Die Entdeckung Siebenwinds (1 n.H.) | 🟡 | [x] Bearbeitung |

## 🔵 Priorität 3: Qualität & Politur (Optimierung)
*Verbesserungen an System und Lore, die den Nutzwert steigern.*

- [x] **Advisor WARN Routing Relaxation**: `advisor`, `/start`, `/takeover` und das Betriebshandbuch behandeln `Pages Health = WARN` jetzt als sichtbares Advisory statt als automatischen Technician-First-Pfad. Die neue JSON-Surface `routing.tech_master` macht diese Routing-Entscheidung maschinenlesbar.
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
