# Master Task List: Siebenwind-Wiki-Rekonstruktion

Dieses Dokument dient als agentenübergreifendes Gedächtnis. Es trennt den **aktiven Fokus** von der **Projekthistorie** und definiert klare Standards für die Aufgabenpriorisierung.

## 📊 Status-Übersicht
- **Wiki-Standard:** v3.0 (Inter-AI Compliant)
- **RAG-Status (Orakel):** DEGRADED; lokaler Modell-/Indexcache fehlt, direkte Quellenprüfung bleibt der aktive Fallback (`MSG-2026-0192`).
- **Last Handover**: 2026-10-21 (Leserrelease, technische Dokumentation und erneute Abnahme)
- **Status**: Maßgeblich sind `./7w_wiki.py advisor --json` und `.agent/data/pages_health.json` mit Messdatum und Umfang. Leserzahlen kommen aus `./7w_wiki.py stats`; überfällige Brücken aus der gemeinsamen Lifecycle-Prüfung. Ein lokaler Vollbau bestätigt keine tatsächliche Veröffentlichung.

---

## 🔴 Priorität 1: Aktueller Fokus (Next Step)

- [x] **Layout-Contract Cleanup & Audit-Zaehllogik**: Die `layout`-Altfelder aus den audit-relevanten Seiten wurden entfernt; `audit --json` meldet keine `legacy_field: layout`-Verletzungen mehr und weist den verbleibenden Ingestion-Score-Cluster konsistent unter `details.ingestion_issues` aus.

- [x] **Zeitstrahl Structural Repair**: `docs/Siebenwind_Wiki/05_Geschichte/Zeitstrahl.md` wurde von einem strukturell korrumpierten Mischdokument auf eine kompakte Chronik-Uebersicht mit Verweisen auf `Historie & Aeren` und `Zeitleiste (15-30 n.H.)` zurueckgefuehrt.

- [ ] **Semantic Pages Backlog Triage**: Aktuelle Zahlen ausschließlich aus `.agent/data/pages_health.json` lesen; Berichtsalter beachten. Bestehende Board-Artefakte (`.agent/data/backlog_cluster_board.json`, `.agent/data/backlog_escalations.json`, `RESEARCH-2026-018`) verwenden. Semantische Begriffsarbeit bleibt getrennt von mechanischen Reparaturen.

- [ ] **Bridge-Retirement statt Fristverlängerung (`MSG-2026-0241`)**: Die 84 bekannten Brücken mit Reviewfrist 30. Juni werden nun als überfälliger Altbestand ausgewiesen. `MSG-2026-0240` ist technisch abgeschlossen; neue oder verschlechterte Fälle sperren die Abnahme. Eingehende Links zuerst auf belastbare kanonische Ziele heben, dann Brücken entfernen. Unklare Gleichsetzungen bleiben beim Historian/Coordinator.

- [ ] **Verbleibende Leserabnahme**: Reale iOS-/Android-Geräte und ein echter Screenreader fehlen noch. Die 53 zunächst ungeprüften Dokumenteinträge wurden am 21. Oktober technisch abgeglichen und korrigiert; fachliche Lorefragen sind davon nicht freigegeben. Ergebnisse und Grenzen stehen in `System/READER_RELEASE_REVIEW_2026-09-12.md`.

- [x] **Forum-Ingestion v2 Pilot**: Die Forum-Volltextarchivierung und agentische Verarbeitung sind als Runtime-Pfad umgesetzt. Zwei Pilotquellen sind integriert (`Ergon` als Update, `Orkisches Handelskontor` als Neuanlage), das Forumregister bleibt bei `201` Eintraegen mit `2 integrated`, und die Draft-Stilregel verhindert kuenftig OOC-Formulierungen im Artikelkoerper.

- [x] **Fallback `[[index]]`-Platzhalterbereinigung**: Das Orakel/RAG war fuer diese Session nicht funktionstuechtig; die Bereinigung wurde deshalb ueber direkte `rg`-Suchen, Kontextlektüre und konservative Klartext-Ersetzungen durchgefuehrt. Ergebnis: `rg "\[\[index\]\]" docs/Siebenwind_Wiki -g '*.md'` findet keine Treffer mehr; unklare Stellen wurden nicht erfunden, sondern mit `[UNGEKLÄRT]` markiert.

- [ ] **Pages-Linkbacklog nach `[[index]]`-Welle**: Nach der Platzhalterbereinigung ist der naechste operative Block der allgemeine Pages-Linkbacklog aus `./7w_wiki.py pages validate --contract --json`: zuerst `safe_exact_match` und `planned_fix`, dann `generic_term_conflict`, danach die `needs_historian`-Ziele.

- [ ] **Review- und Scan-Restbestand schliessen**: `RESEARCH-2026-004` und `RESEARCH-2026-007` stehen weiter auf `IN_REVIEW_HISTORIAN`, waehrend der Forum-Scan fuer `3` allowlistete Boards als stale gilt. Der naechste Agent soll entscheiden, ob zuerst die Historian-Reviews publiziert/geschlossen oder die Foren-Pipeline reaktiviert wird.

- [x] **Forum-Historikerlauf – fünf Quellen (`MSG-2026-0229`)**: Die Topics `31020`, `48524`, `109905`, `107595` und `109867` wurden in der festgelegten Reihenfolge quellenkritisch integriert. Vier neue Leserartikel entstanden, zwölf bestehende Seiten wurden inhaltlich oder als Linkziel aktualisiert und der abgelaufene Brückenplatzhalter `Rasse Orken.md` wurde nach Linkhebung entfernt. Alle fünf Quellen stehen im Forumregister auf `integrated`; Details stehen in `Logs/Archive/SESSION_MEMORY_2026-08-05_HISTORIKERLAUF_31020_BIS_109867.md`.
- [x] **Forum-Historikerlauf – fünf Quellen (`109571` bis `108788`)**: Die Topics `109571`, `109483`, `108944`, `109310` und `108788` wurden quellenkritisch integriert. Fuenf Erzaehlungsartikel, die neue Personenseite Volandurs und substanzielle Aktualisierungen an Maichellis, Akassvae, Huns, Brandenstein, Falkenwall und Claiomhs Wacht verbinden Perspektivtexte mit den Boten 132/133 und 191/193/194. Details stehen in `Logs/Archive/SESSION_MEMORY_2026-08-06_HISTORIKERLAUF_109571_BIS_108788.md`.
- [x] **Forum-Ingestorlauf – fünf Quellen (`MSG-2026-0228`)**: Die Topics `106975`, `109430`, `109411`, `103341` und `99477` wurden in Registerreihenfolge quellenkritisch integriert. Maichellis, Ras Altanin, Erynnion und Celedelair erhielten belastbare Erweiterungen; `Thjareks Brecher` wurde als eigenständiges, durch Bote 190 bestätigtes Kriegsschiff erschlossen. Vier technische Laufzeitabweichungen sind an den Technician delegiert. Details stehen in `Logs/Archive/SESSION_MEMORY_2026-08-23_FORUM_FUENFERLAUF_106975_BIS_99477.md`.

- [x] **Residual Bridge Decision Gate**: `MSG-2026-0089` ist abgeschlossen; `docs/Siebenwind_Wiki/00_Fundament/Arman_von_Draconis.md` verweist temporaer auf `[[Arman]]`, `bridge_inventory.invalid = 0`, und der fruehere P1-Blocker ist damit aus dem aktiven Fokus gefallen.

- [x] **Wave 2: Pages Surface Hardening & Root-Tree Retirement**: `Siebenwind_Wiki/` wurde als physischer Altbaum entfernt, `pages validate --contract --json` als deterministischer Vertragsmodus eingefuehrt, `docs/assets/` auf produktive Assets begrenzt und die Maschinenoberflaechen auf `legacy_root_status = removed` umgestellt.

- [x] **Bridge Blocker Pass**: `00_Religion_Uebersicht` und `03_Gesellschaft` wurden auf ihre kanonischen Zielartikel gehoben; fuer `Werke_index` entstand mit `docs/Siebenwind_Wiki/03_Wissen/Werke.md` ein stabiler Landing-Artikel. Ergebnis: `audit --json` fiel von `9` auf `3` Issues, `bridge_inventory.invalid` von `4` auf `1`.

- [x] **Religions-Cluster Resolver Follow-Up**: Die Review-Grundlage liegt unter `.agent/data/religion_cluster_review.json` und `.agent/data/religion_cluster_escalations.json`. Der Folgeschritt ueber publizierte Ingestion-Reports und Maintainer-Doku ist erfolgt; Religions-Restziele wurden aus dem aktiven Repair-Fokus in dokumentierte Historie ueberfuehrt.

- [x] **Bridge Lifecycle Metadata Cleanup**: Die `84` Kandidaten wurden gegen semantische Verluste geprueft und mit den vier Pflichtfeldern fuer temporaere Bridges versehen. Dieser abgeschlossene Schritt stellte nur formale Gueltigkeit her; er entfernte die Bruecken nicht. Die eigentliche Stilllegung ist deshalb wieder als eigener offener P1-Lauf aufgefuehrt.

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
- [ ] **Forum-Queue Batchweise verarbeiten**: Nach den Piloten weitere Forumquellen über `ingest forum-queue`, `forum-inspect`, `forum-draft` und `forum-finalize` bearbeiten. Aktueller Registerstand: `201` Themen, davon `101` volltextarchiviert, `79` integriert, `5` ohne Wikiänderung abgeschlossen, `17` Volltexte fachlich offen und `100` nur als Metadaten vorhanden. Das Paket `106975`, `109430`, `109411`, `103341` und `99477` ist abgeschlossen; der nächste Lauf muss seine Quellen erneut in der Reihenfolge des Forumregisters bestimmen. Nächster zulässiger Metadatenkandidat bleibt Topic `108636` (`Pflicht`); Topic `104857` wird wegen seiner bestehenden Dublettenentscheidung korrekt übersprungen.
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

- [x] **12. September 2026: Leserzugang und verlässlicher Betrieb**: Gemeinsame Pagefind-Suche, mobile Darstellung, Themenzugänge, Neuigkeiten und getrennte Betriebsdiagnose umgesetzt. Die ersten Leserwege wurden anhand von Homepage und Originalquellen korrigiert. `MSG-2026-0240` und `MSG-2026-0259` sind abgeschlossen; fünf alte Abschlussmeldungen wurden einzeln als INFO eingeordnet. Der veröffentlichte Commit wird separat über `pages verify-live` nachgewiesen.

*Aktiver Drift-/Pages-Vertrag:* `System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md`


Die vollständige Projekthistorie (v1.0 bis v3.0) wurde archiviert unter: `System/_archive/Dossiers_2026-02/PROJECT_HISTORY.md`
