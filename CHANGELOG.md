# Changelog

#### [2026-04-17.01] - Fallback-index-Platzhalter global bereinigt
### Prioritaet: P1
### Geändert
- `docs/Siebenwind_Wiki/**`: alle exakten `[[index]]`-Platzhalter konservativ auf kontextnahe Klartextbegriffe, bestehende kanonische Ziele oder `[UNGEKLÄRT]` gehoben. Bearbeitet wurden unter anderem `00_Fundament`, `01_Pantheon`, `02_Geografie`, `03_Gesellschaft`, `03_Wissen`, `04_Chronik`, `05_Geschichte`, `05_Magie`, `07_Persoenlichkeiten`, `08_Bestiarium`, `09_Bibliothek` und `10_Archiv`.
- `docs/Siebenwind_Wiki/01_Pantheon/*` und `docs/Siebenwind_Wiki/03_Gesellschaft/*`: alte `Quellen/index Astrael`- bzw. `Quellen/index ...`-Metadatenpfade auf vorhandene `Quellen/Bibliothek Astrael`- und `Quellen/Bibliothek Toran Dur`-Pfade korrigiert.
- `System/Synapse_Board/RESEARCH-2026-018.md` und `docs/Archiv/RESEARCH-2026-018.md`: als Arbeits- und Archivanker fuer die Fallback-Bereinigung genutzt.
### Validiert
- `rg "\[\[index\]\]" docs/Siebenwind_Wiki -g '*.md'` ohne Treffer.
- `./7w_wiki.py audit --json` (`0 contract_violations`; bekannter `score_cluster` bleibt einziges Issue).
- `./7w_wiki.py pages validate --json` (`source-link-hygiene` PASS; Gesamtstatus FAIL wegen bekanntem Audit-Precheck).
- `./7w_wiki.py pages validate --contract --json` (`drift_status = PASS`; WARN wegen bestehendem breiteren unresolved-Linkbacklog, nicht wegen `[[index]]`).

#### [2026-04-09.02] - Zeitstrahl-Handoversync und Runtime-Artefakte aktualisiert
### Prioritaet: P1
### Geändert
- `CHANGELOG.md`, `MASTER_TASK_LIST.md` und der Handover-Stand: Session auf den tatsaechlichen Restbestand gehoben; aktiver Fokus jetzt semantischer Pages-Backlog, Historian-Reviews `RESEARCH-2026-004` / `RESEARCH-2026-007` und stale Forum-Scan-Pipeline.
- `docs/Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md`, `Logs/INGESTION_TRACKING_REGISTER.md` und die generierten Cache-/Inventarartefakte unter `.agent/data/`: durch `stats`, `audit`, `pages validate` und die Handover-Validierung auf den aktuellen Stand regeneriert.
- `.agent/data/backlog_cluster_board.json` und `.agent/data/backlog_escalations.json`: Pages-/Backlog-Snapshot auf den bereinigten Vertragsstand (`contract_violations = 0`) und den aktuellen unresolved-Stand gehoben.
### Hinzugefügt
- `Logs/Archive/SESSION_MEMORY_2026-04-09_ZEITSTRAHL_HANDOVER_SYNC.md`: Session-Memory mit Abschlusslage, Validierung und offenem Restbestand fuer den naechsten Agenten.
- `.agent/data/wiki_inventory_history/wiki_inventory_2026-04-09_181833.json`, `.agent/data/wiki_inventory_history/wiki_inventory_2026-04-09_181840.json` und `.agent/data/wiki_inventory_history/wiki_inventory_2026-04-09_181842.json`: neue Inventar-Snapshots aus dem Handover-Lauf.
### Validiert
- `./7w_wiki.py stats`
- `./7w_wiki.py archive rotate`
- `./7w_wiki.py tech --manifest`
- `./7w_wiki.py audit --json`
- `./7w_wiki.py pages validate --json` (`FAIL` nur wegen Runtime-Precheck auf dem bekannten `score_cluster`, keine neuen Contract-Verletzungen)
- `./7w_wiki.py test --suite all` (vollstaendige Reportmenge unter `/var/folders/m0/28md0wx56p7d_3y66c75ggfc0000gn/T/7w_test_rk82__tl`; in den erzeugten Reports keine `FAIL`-/`SKIP`-Marker gefunden, aber der Wrapper lieferte im beobachteten Fenster keine finale Summary zurueck)
- `./7w_wiki.py mail inbox --status OPEN`
- `./7w_wiki.py start --list-reviews`

#### [2026-04-09.01] - Wave 2 Pages-Haertung abgeschlossen und Restbestand fuer Handover neu fokussiert
### Prioritaet: P1
### Geändert
- `7w_wiki.py`, `.agent/scripts/pages_tool.py` und `.agent/scripts/pages_integrity.py`: deterministischen Vertragsmodus `./7w_wiki.py pages validate --contract --json` eingefuehrt; Full-Validate bleibt fuer Operatoren erhalten.
- `.agent/scripts/advisor.py`, `.agent/scripts/content_contract.py`, `.agent/scripts/generate_lore_manifest.py` und `lore_manifest.json`: Legacy-Root-Surface auf `legacy_wiki_root = null` und `legacy_root_status = "removed"` umgestellt.
- `docs/assets/design_proposals/*` nach `System/Design_Assets/design_proposals/2026-04-wave2/` verlagert; `docs/assets/` damit auf produktive/publizierte Assets begrenzt.
- `MASTER_TASK_LIST.md`: den veralteten P1-Blocker `Arman_von_Draconis` aus dem aktiven Fokus entfernt und den realen Restbestand auf `layout`-Contract-Cleanup, `Zeitstrahl`-Reparatur, semantischen Pages-Backlog sowie offene Historian-/Forum-Spuren umgestellt.
- `System/STYLING.md`, `System/Synapse_Board/SY_INTEROP.md`, `System/Synapse_Board/SY_TESTING.md`, `docs/Agenten/interop.md`, `docs/Agenten/workflows.md` und `AGENTS.md`: auf Root-Tree-Retirement, produktive Asset-Surface und die neuen Suites `pages-contract-mode-contract`, `pages-full-smoke`, `root-tree-retirement-contract` und `styling-surface-contract` gehoben.
### Hinzugefügt
- `.agent/tests/suites/pages-contract-mode-contract.json`, `.agent/tests/suites/pages-full-smoke.json`, `.agent/tests/suites/root-tree-retirement-contract.json` und `.agent/tests/suites/styling-surface-contract.json`: neue Wave-2-Vertraege fuer deterministische Pages-Validierung, finalen Root-Tree-Retirement-Check und die Styling-Autoritaet.
- `Logs/Archive/SESSION_MEMORY_2026-04-09_WAVE2_PAGES_HANDOVER.md`: Handover-Notiz mit Restbestand, Validierung und Operationsplan fuer den naechsten Agenten.
### Validiert
- `python3 -m py_compile .agent/scripts/advisor.py .agent/scripts/content_contract.py .agent/scripts/generate_lore_manifest.py .agent/scripts/pages_integrity.py .agent/scripts/pages_tool.py .agent/scripts/repair.py .agent/scripts/repo_hygiene.py .agent/scripts/sync_runtime_docs.py .agent/scripts/test_runner.py 7w_wiki.py`
- `./7w_wiki.py tech --sync-interop`
- `./7w_wiki.py tech --manifest`
- `./7w_wiki.py tech --repo-hygiene --apply --json`
- `./7w_wiki.py stats`
- `./7w_wiki.py archive rotate`
- `./7w_wiki.py advisor --json`
- `./7w_wiki.py audit --json`
- `./7w_wiki.py start --list-reviews`
- `./7w_wiki.py test --suite all`
- `./7w_wiki.py test --suite pages-full-smoke`

#### [2026-04-08.11] - Semantischen Restbestand in Historian- und Technician-Spur aufgeteilt
### Prioritaet: P2
### Hinzugefügt
- `System/Synapse_Board/RESEARCH-2026-018.md`: neuer aktiver Historian-Fall fuer die Disambiguierung der verbleibenden generischen `Magie`-/`index`-Verwendungen nach ausgeschoepfter mechanischer Linkreparatur.
- `docs/Archiv/RESEARCH-2026-018.md`: oeffentliche Archivseite zum neuen Historian-Fall gemaess Publikationsprinzip.
### Geändert
- `docs/Archiv/Research_Board.md` und `System/Synapse_Board/LORE_RESEARCH_BOARD.md`: um `RESEARCH-2026-018` als offenen Historian-Fall ergaenzt; Professorenansicht und Detailbeschreibung auf den neuen semantischen Restbestand erweitert.
- `System/COORDINATION_HUB.md`: neues Research-Artefakt registriert.

#### [2026-04-08.10] - Welle 2 der Linkhygiene mechanisch fortgesetzt
### Prioritaet: P2
### Geändert
- `docs/Siebenwind_Wiki/07_Persoenlichkeiten/Kalveron_Dai.md`, `docs/Siebenwind_Wiki/07_Persoenlichkeiten/Raisha_al_Javet.md` und `docs/Siebenwind_Wiki/07_Persoenlichkeiten/Themus_Takai.md`: Werkreferenzen auf die kanonischen disambiguierten Zieltitel umgestellt.
- `docs/Siebenwind_Wiki/04_Chronik/Siebenwind_Bote_174.md`: Personenlink auf `[[Beladriel_Blaettertanz]]` normalisiert und H1/frontmatter fuer `check` begradigt.
- `docs/Siebenwind_Wiki/00_Fundament/Organisationsregister.md`: kaputte `[[[Siebenwind]]`-Klammer im Redaktionsverweis bereinigt und Frontmatter-Hygiene nachgezogen.
### Validiert
- `./7w_wiki.py check docs/Siebenwind_Wiki/07_Persoenlichkeiten/Kalveron_Dai.md`
- `./7w_wiki.py check docs/Siebenwind_Wiki/07_Persoenlichkeiten/Raisha_al_Javet.md`
- `./7w_wiki.py check docs/Siebenwind_Wiki/07_Persoenlichkeiten/Themus_Takai.md`
- `./7w_wiki.py check docs/Siebenwind_Wiki/04_Chronik/Siebenwind_Bote_174.md`
- `./7w_wiki.py check docs/Siebenwind_Wiki/00_Fundament/Organisationsregister.md`
- `./7w_wiki.py pages validate --json --skip-audit` (`unresolved_total` von 653 auf 641, `generic_term_conflict` von 15 auf 5, `safe_alias_match` von 4 auf 2)

#### [2026-04-08.09] - Statistik entmischt, Geist entflechtet und konservative index-Welle gefahren
### Prioritaet: P2
### Hinzugefügt
- `docs/Siebenwind_Wiki/00_Fundament/Geist.md`: neuer Begriffsartikel fuer den metaphysischen und magietheoretischen Gebrauch von `Geist`, klar getrennt von der Personenebene.
### Geändert
- `.agent/scripts/generate_wiki_stats.py`: Leserstatistik zeigt jetzt aktive Bearbeitungstage statt nackter Commit-Zahl, liest reale aktuelle Testreports aus Archiv und Temp-Verzeichnissen und blendet automatische Platzhalter aus den Personen-Rankings aus; ausserdem wird ein `index`-Placeholder-Inventar im Snapshot mitgefuehrt.
- `.agent/scripts/pages_integrity.py`, `.agent/scripts/repair.py` und `.agent/scripts/advisor.py`: unresolved Pages-Targets werden jetzt in `safe_exact_match`, `safe_alias_match`, `generic_term_conflict`, `needs_historian` und `needs_human` klassifiziert; Advisor und Roamlink-Repair unterscheiden dadurch mechanische von begrifflichen Faellen.
- `docs/Siebenwind_Wiki/07_Persoenlichkeiten/Herr_Geist.md`, `docs/Siebenwind_Wiki/00_Fundament/Personenregister.md` und `docs/Siebenwind_Wiki/07_Persoenlichkeiten/index.md`: der Assassine wird jetzt eindeutig als `Herr_Geist` gefuehrt; `Geist` als generischer Begriff rankt nicht mehr als Persoenlichkeits-Stub.
- `docs/Siebenwind_Wiki/**/*.md` und `docs/Quellen/**/*.md`: konservative erste `index`-Bereinigung fuer exakte Platzhalter in `category: [[index]]`, reinen `##/### [[index]]`-Ueberschriften und Glossar-Stubs.
- `docs/Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md`, `Logs/INGESTION_TRACKING_REGISTER.md` und `Logs/Archive/STATS_SNAPSHOT_latest.json`: auf den neuen Statistikstand regeneriert.
### Validiert
- `python3 -m py_compile .agent/scripts/generate_wiki_stats.py .agent/scripts/pages_integrity.py .agent/scripts/repair.py .agent/scripts/advisor.py`
- `./7w_wiki.py stats`
- `./7w_wiki.py test --suite reader-stats-contract`
- `./7w_wiki.py test --suite source-link-hygiene`
- `./7w_wiki.py check docs/Siebenwind_Wiki/00_Fundament/Geist.md`
- `./7w_wiki.py check docs/Siebenwind_Wiki/07_Persoenlichkeiten/Herr_Geist.md`
- `./7w_wiki.py pages validate --json --skip-audit` (`unresolved_total` von 681 auf 653, `generic_term_conflict` jetzt explizit sichtbar)
- `./7w_wiki.py repair --fix-roamlinks --dry-run`

#### [2026-04-08.08] - Research Board auf Historian-Docket und operativen Default zurueckgebaut
### Prioritaet: P2
### Geändert
- `.agent/scripts/advisor.py` und `.agent/scripts/forum_scanner.py`: Advisor-Semantik auf `historian_pending_count`, `human_decision_required_count` und `forum_scan_stale` umgestellt; Geschichten-Scans archivieren jetzt roh, ohne standardmaessige Menschvorlage.
- `.agent/scripts/research_review.py` sowie `docs/Archiv/Research_Board.md` und `System/Synapse_Board/LORE_RESEARCH_BOARD.md`: Research-/Review-Statuswortschatz auf `OPEN_HISTORIAN`, `IN_REVIEW_HISTORIAN`, `AWAITING_HUMAN_DECISION`, `RESOLVED` und `THEMATIC_BACKLOG` gehoben.
- `docs/Archiv/RESEARCH-2026-002/003/004/007/010/011/012/015/016/017.md`, `docs/Siebenwind_Wiki/10_Archiv/Interessante_Artikel.md`, `docs/Siebenwind_Wiki/10_Archiv/index.md` und `docs/index.md`: nur noch freigegebene Berichte als Neuveroeffentlichung sichtbar; offene Historian-Faelle bleiben im Docket.
- `.agent/workflows/*`, `.agent/instructions/persona_historian.md`, `.agent/skills/lore_gelehrter/SKILL.md`, `.agent/skills/lore_gelehrter/SKILL.md.tpl`, `System/Synapse_Board/_TEMPLATE_RESEARCH.md`, `System/Synapse_Board/SY_STANDARDS.md`, `System/Synapse_Board/SY_REVIEW.md` und `System/Synapse_Board/SY_HISTORIAN_TRACEABILITY.md`: operativ-zuerst, Historian-nur-bei-Unklarheit, Mensch-nur-bei-Kontroverse dokumentiert.
### Validiert
- `python3 -m py_compile .agent/scripts/advisor.py .agent/scripts/forum_scanner.py .agent/scripts/research_review.py .agent/skills/oracle/build_index.py`
- `./7w_wiki.py advisor --json`
- `./7w_wiki.py start --list-reviews`
- `./7w_wiki.py check .agent/workflows/start.md`
- `./7w_wiki.py check .agent/workflows/forum_search.md`
- `./7w_wiki.py check .agent/workflows/ingest_master.md`
- `./7w_wiki.py check .agent/workflows/historian.md`
- `./7w_wiki.py check .agent/workflows/lore_master.md`
- `./7w_wiki.py check .agent/workflows/takeover.md`
- `./7w_wiki.py check docs/Archiv/Research_Board.md`
- `./7w_wiki.py check docs/Archiv/RESEARCH-2026-004.md`
- `./7w_wiki.py check docs/Siebenwind_Wiki/10_Archiv/Interessante_Artikel.md`
- `./7w_wiki.py check docs/index.md`
- `./7w_wiki.py check System/Synapse_Board/LORE_RESEARCH_BOARD.md`
- `./7w_wiki.py check System/Synapse_Board/SY_REVIEW.md`
- `./7w_wiki.py test --suite workflow-matrix-contract`

#### [2026-04-08.07] - Research-Approval und forumgestuetzte Story-Quellenpipeline eingefuehrt
### Prioritaet: P2
### Hinzugefügt
- `.agent/scripts/research_review.py`: Review-Helfer fuer Research-Freigaben, Rueckgaben und Historian-Kommentare mit Register- und Dispatch-Spur.
- `.agent/data/forum_scan_register.json`: maschinenlesbares Sichtungsregister fuer Forenscans.
### Geändert
- `7w_wiki.py`: `/start` um Research-Review-Aktionen erweitert und `scout --forum` fuer allowlistete Story-Boards vorbereitet.
- `.agent/scripts/forum_scanner.py`: forumweite Allowlist, Roharchiv-Metadaten fuer neue Story-Funde und zentrales Scan-Register eingebaut.
- `.agent/scripts/advisor.py`: zeigt jetzt zusaetzlich offene Research-Reviews und menschlich zu pruefende Story-Quellen an.
- `.agent/workflows/start.md`, `.agent/workflows/forum_search.md`, `System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md` und `System/Synapse_Board/SY_REVIEW.md`: neuen Review- und Forum-Scan-Prozess dokumentiert.
### Validiert
- `./7w_wiki.py start --list-reviews`
- `./7w_wiki.py advisor --json`
- `./7w_wiki.py scout --help`

#### [2026-04-08.06] - Archiv-Publikationsmodell und Interessante Artikel zur Releaseflaeche ausgebaut
### Prioritaet: P2
### Geändert
- `docs/Siebenwind_Wiki/10_Archiv/Interessante_Artikel.md`: von reiner Kurationsnotiz zu einer oeffentlichen Kombination aus Lesestrecke und Releaseflaeche fuer neue Forschungsseiten ausgebaut.
- `docs/index.md` und `docs/Siebenwind_Wiki/10_Archiv/index.md`: publizierte Forschungsseiten und Historian Reports als sichtbare Einstiege nachgezogen.
- `docs/Archiv/QUALITAETSRAHMEN_2026.md`, `docs/Archiv/REDESIGN_ROADMAP_2026.md` und `docs/Archiv/Research_Board.md`: die Regel dokumentiert, dass Forschungsfortschritt auf publizierten Archivseiten sichtbar gehalten werden muss.
### Validiert
- `./7w_wiki.py check docs/Siebenwind_Wiki/10_Archiv/Interessante_Artikel.md`
- `./7w_wiki.py check docs/index.md`

#### [2026-04-08.05] - Stats refresh und Research-Archiv als publizierte Seiten nachgezogen
### Prioritaet: P2
### Hinzugefügt
- `docs/Archiv/RESEARCH-2026-001.md` bis `docs/Archiv/RESEARCH-2026-017.md` fuer die aktuell im Research Board referenzierten Auftragsseiten als publizierte Archivziele.
- `docs/Archiv/Historian_Report_2026_003.md` als publizierte Fassung des bislang nur im Log referenzierten Historian-Berichts zu `RESEARCH-2026-005/006`.
### Geändert
- `docs/Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md`, `Logs/INGESTION_TRACKING_REGISTER.md` und `Logs/Archive/STATS_SNAPSHOT_latest.json`: Statistikstand auf 2026-04-08 aktualisiert.
- `docs/Archiv/Research_Board.md`: Archiv-Board wieder auf echte publizierte Zielseiten gehoben und die veraltete Quelle `Alchemie_Grundlagen` auf `Alchemie_Kompendium` retargetet.
- `System/Synapse_Board/LORE_RESEARCH_BOARD.md`: Quellanker und Konsolidierungsstand an den Archivpass angepasst.
- `docs/Siebenwind_Wiki/07_Persoenlichkeiten/Dunvallo_Linari.md`: veralteten Verweis auf `Alchemie_Grundlagen` auf die reale Seite `Alchemie_Kompendium` gehoben.
### Validiert
- `./7w_wiki.py stats`
- `./7w_wiki.py test --suite reader-stats-contract`

#### [2026-04-08.04] - Historian: RESEARCH-2026-007 als kosmologisches Schema statt Magierlegende eingeordnet
### Prioritaet: P2
### Hinzugefügt
- `Logs/Research/RESEARCH-2026-007_Summary.md`: Forschungsbericht zur `Zeichnung Tares` mit Bildsichtung, Kosmologie-Abgleich und dokumentiertem Oracle-Fallback nach lokalem Reranker-Ausfall.
- `docs/Siebenwind_Wiki/03_Wissen/Werke/Zeichnung_Tares.md`: neuer kanonischer Werkartikel fuer die Rhadan zugeschriebene Kosmologieskizze.
### Geändert
- `docs/Archiv/Dossier_Rhadan.md`: vom spekulativen Rhadan-Expose auf den belastbaren Befund zur `Zeichnung Tares` umgestellt.
- `docs/Siebenwind_Wiki/07_Persoenlichkeiten/Rhadan_der_Graue.md`: um die gesichert ueberlieferten Werke `Ari'in`, `Die Ritualisierung` und `Zeichnung Tares` ergaenzt und quellenstrenger formuliert.
- `docs/Siebenwind_Wiki/00_Fundament/Fela.md`, `docs/Siebenwind_Wiki/00_Fundament/Tare.md`, `docs/Siebenwind_Wiki/00_Fundament/Vitamalin.md`, `docs/Siebenwind_Wiki/00_Fundament/Astreyon.md` und `docs/Siebenwind_Wiki/00_Fundament/Dorayon.md`: von Platzhaltern bzw. unscharfer Kurzfassung auf quellengetragene Minimalartikel gehoben.
- `docs/Siebenwind_Wiki/03_Wissen/Werke/index.md`: um `Zeichnung Tares` erweitert.
- `System/Synapse_Board/LORE_RESEARCH_BOARD.md`, `docs/Archiv/Research_Board.md` und `MASTER_TASK_LIST.md`: `RESEARCH-2026-007` auf `REVIEW` gehoben und mit dem aktuellen Forschungsbefund versehen.
### Validiert
- manuelle Bildsichtung von `Rhadan der Graue - Zeichnung Tares.jpg`
- manuelle Quellenlektuere von `Rhadan der Graue - AriÔin.md`, `Toran Dur - Die Magie.md` und `Monde Tares | Siebenwind | Ultima Online Freeshard | Siebenwind.md`
- `./7w_wiki.py search "Rhadan Zeichnung Tares Ari´in" --source all` (Oracle-Ausfall dokumentiert; Fallback auf Direktquellen)

#### [2026-04-08.03] - Historian: RESEARCH-2026-004 auf belastbare Quellenlage reduziert
### Prioritaet: P2
### Hinzugefügt
- `Logs/Research/RESEARCH-2026-004_Summary.md`: Forschungsbericht zur Causa `Tjure Odal` / `Arn Toron` mit Quellenabgleich gegen den Bote-Strang 167-186 und expliziter Historian-Fallback-Dokumentation nach Oracle-Ausfall.
### Geändert
- `docs/Siebenwind_Wiki/07_Persoenlichkeiten/Arn_Toron.md`: vom pauschalen Verräter-/Ketzerprofil auf den quellengetragenen Befund als ehemaliger Konsul, Kaufmann und späterer Brandensteiner Exilant gehoben; Ketzerstatus jetzt als Anklagesprache markiert.
- `docs/Siebenwind_Wiki/07_Persoenlichkeiten/Tjure_Odal.md`: auf den belastbaren Minimalbefund zurückgeführt; Tjure bleibt biografisch [UNGEKLAERT] und ist im aktuellen Corpus nur in Bote 186 namentlich fassbar.
- `docs/Siebenwind_Wiki/07_Persoenlichkeiten/Marnie_Ruatha.md`: die 22-n.H.-Krisenpassage vervollständigt und an die rekonstruierte Anklagelage angeschlossen.
- `docs/Siebenwind_Wiki/04_Chronik/Siebenwind_Bote_168.md`: die nicht durch die Primärquelle bestätigte Arn-Toron-Nennung aus der Summary entfernt.
- `docs/Siebenwind_Wiki/00_Fundament/Personenregister.md`: Registereinträge für `Arn_Toron` und `Tjure_Odal` auf den Forschungsbefund abgestimmt.
- `System/Synapse_Board/LORE_RESEARCH_BOARD.md`, `docs/Archiv/Research_Board.md` und `MASTER_TASK_LIST.md`: `RESEARCH-2026-004` auf `REVIEW` gehoben und die alte Problembeschreibung an den aktuellen Repo-Stand angepasst.
### Validiert
- manuelle Quellenlektüre von `Siebenwind Bote 167`, `Siebenwind Bote 168`, `Siebenwind_Bote_184` und `Siebenwind Bote 186`
- `./7w_wiki.py search "Tjure Odal Arn Toron" --source all` (Oracle-Ausfall dokumentiert; Fallback auf Direktquellen)

#### [2026-04-08.02] - Historian: April-Kuration fuer "Interessante Artikel" auf Draconis-Thema gedreht
### Prioritaet: P2
### Geändert
- `docs/Siebenwind_Wiki/10_Archiv/Interessante_Artikel.md`: von einer generischen Grundlagenliste auf die April-2026-Rotation `Unter dem Weissen Hochturm` umgestellt. Die Seite enthaelt jetzt eine thematische Shortlist mit Kanon-Begruendung, Quellenbasis, Leserwert und vorgeschlagenen Archiv-Themenmotiven.
- `docs/index.md`: das Startseitenmodul `Interessante Artikel` auf die aktuelle Rotation gespiegelt und die drei Anrisskarten auf `Draconis`, `Codex Iuris Canonici` und `Arman` umgestellt.
- `docs/Siebenwind_Wiki/02_Geografie/Draconis.md`, `docs/Siebenwind_Wiki/01_Pantheon/Das_Pantheon.md`, `docs/Siebenwind_Wiki/01_Pantheon/Codex_Iuris_Canonici.md`, `docs/Siebenwind_Wiki/03_Gesellschaft/Ring_des_Argionemes.md` und `docs/Siebenwind_Wiki/07_Persoenlichkeiten/Arman.md`: fuer die Kurationsvorauswahl mit aktuellem Score versehen und auf sauberes `layout`-Frontmatter gehoben, damit der Stilcheck fuer die ausgewaehlte Rotation grün laeuft.
### Validiert
- `./7w_wiki.py score docs/Siebenwind_Wiki/02_Geografie/Draconis.md`
- `./7w_wiki.py score docs/Siebenwind_Wiki/01_Pantheon/Das_Pantheon.md`
- `./7w_wiki.py score docs/Siebenwind_Wiki/01_Pantheon/Codex_Iuris_Canonici.md`
- `./7w_wiki.py score docs/Siebenwind_Wiki/03_Gesellschaft/Ring_des_Argionemes.md`
- `./7w_wiki.py score docs/Siebenwind_Wiki/07_Persoenlichkeiten/Arman.md`
- `./7w_wiki.py check docs/Siebenwind_Wiki/02_Geografie/Draconis.md`
- `./7w_wiki.py check docs/Siebenwind_Wiki/01_Pantheon/Das_Pantheon.md`
- `./7w_wiki.py check docs/Siebenwind_Wiki/01_Pantheon/Codex_Iuris_Canonici.md`
- `./7w_wiki.py check docs/Siebenwind_Wiki/03_Gesellschaft/Ring_des_Argionemes.md`
- `./7w_wiki.py check docs/Siebenwind_Wiki/07_Persoenlichkeiten/Arman.md`

#### [2026-04-08.01] - Bridge-Blocker-Pass auf einen Historian-Restfall reduziert
### Prioritaet: P1
### Hinzugefügt
- `docs/Siebenwind_Wiki/03_Wissen/Werke.md`: neuer kanonischer Landing-Artikel fuer Legacy-Verweise auf das Werkarchiv.
- `Logs/Archive/SESSION_MEMORY_2026-04-08_BRIDGE_BLOCKER_PASS.md`: Session-Memory fuer den Bridge-Resolver-Lauf mit Delta, Validierung und offenem Historian-Blocker.
### Geändert
- `docs/Siebenwind_Wiki/00_Fundament/00_Religion_Uebersicht.md`: mit Lifecycle-Metadaten versehen und auf `[[Religion_Übersicht]]` gehoben.
- `docs/Siebenwind_Wiki/00_Fundament/03_Gesellschaft.md`: mit Lifecycle-Metadaten versehen und auf `[[Gesellschaft]]` gehoben.
- `docs/Siebenwind_Wiki/00_Fundament/Werke_index.md`: mit Lifecycle-Metadaten versehen und auf `[[Werke]]` gehoben.
- `docs/Siebenwind_Wiki/00_Fundament/Arman_von_Draconis.md`: bewusst unresolved belassen, aber explizit auf `MSG-2026-0089` / `MSG-2026-0090` als offene Zielentscheidung verwiesen.
- `MASTER_TASK_LIST.md`: Status-Ueberblick und P1-Fokus auf den letzten Restfall `Arman_von_Draconis` fortgeschrieben.
### Validiert
- `./7w_wiki.py sanitize --json`
- `./7w_wiki.py audit --json`
- `./7w_wiki.py pages validate --json --strict-links`
- `./7w_wiki.py test --suite interop-doc-links`
- `./7w_wiki.py test --suite pages-link-contract`
- `./7w_wiki.py test --suite bridge-placeholder-guard`

#### [2026-04-03.03] - Advisor: Pages-WARN Routing auf advisory statt Technician-Pflicht gelockert
### Prioritaet: P3
### Geändert
- `.agent/scripts/advisor.py`: Pages-Health-Routing zentral klassifiziert (`required`, `advisory`, `not_needed`) und `advisor --json` um `routing.tech_master.{mode,trigger,command}` erweitert. `WARN` erzwingt damit keinen Technician-First-Pfad mehr, waehrend `FAIL`, `UNKNOWN` und veraltete Snapshots weiter hart auf `/tech_master` routen.
- `.agent/workflows/start.md`, `.agent/workflows/takeover.md` und `System/AGENT_OPERATIONS_HANDBOOK.md`: Onboarding- und Betriebstexte auf dieselbe Routing-Regel gehoben, damit Runtime und Dokumentation nicht erneut auseinanderlaufen.
- `.agent/tests/suites/json-interop-contract.json`: JSON-Vertrag fuer `advisor --json` um die neue Routing-Surface erweitert.
- `System/Synapse_Board/DISPATCH/MSG-2026-0093_advisor_routing_relaxed_for_pages_warn.md`: Arbeitsbericht fuer die Session an den Coordinator gepostet.
### Validiert
- `./7w_wiki.py test --suite json-interop-contract`
- `./7w_wiki.py test --suite clean-client-state`
- `./7w_wiki.py test --suite interop-doc-links`
- `./7w_wiki.py advisor --json`
- `./7w_wiki.py start`

#### [2026-04-03.02] - Tech Master: Pages-/Bridge-Backlog auf vier semantische Restfaelle reduziert
### Prioritaet: P1
### Hinzugefügt
- `Logs/Archive/SESSION_MEMORY_2026-04-03_TECH_MASTER_BRIDGE_HANDOVER.md`: Session-Memory fuer den Technician-/Handover-Lauf mit Delta, Validierung und Empfehlungspaket fuer die vier verbleibenden Bridge-Entscheidungen.
### Geändert
- `docs/Siebenwind_Wiki/04_Chronik/Zeitleiste_(15-30_n.H.).md`, `docs/Siebenwind_Wiki/04_Chronik/Zeitleiste_15_30_nH.md`, `docs/Siebenwind_Wiki/06_Erzählungen/Die_Nacht_des_Dunkeltiefs.md` und `docs/Siebenwind_Wiki/07_Persoenlichkeiten/Herr_Merik.md`: den driftigen Zielbegriff `[[Dämonen]]` auf den kanonischen aktiven Zielartikel `[[Daemonen]]` gehoben.
- `Quellen/Zeitung 7w Bote/Siebenwind Bote 176.md`, `Quellen/Zeitung 7w Bote/Siebenwind Bote 178.md`, `Quellen/Zeitung 7w Bote/Siebenwind Bote 179.md`, `Quellen/Zeitung 7w Bote/Siebenwind Bote 180.md`, `Quellen/Zeitung 7w Bote/Siebenwind Bote 181.md`, `Quellen/Zeitung 7w Bote/Siebenwind Bote 182.md` und `Quellen/Zeitung 7w Bote/Siebenwind Bote 185.md`: defekte Root-Symlinks auf die kanonischen Rohquellen umgehoben, sodass der harte Pages-Precheck keine fehlenden Datei-Ziele mehr meldet.
- `docs/Siebenwind_Wiki/00_Fundament/` sowie einzelne Restseiten in `01_Pantheon/` und `05_Geschichte/`: die Single-Target-Bridge-Welle mit temporaerer Lifecycle-Metadatenhygiene abgeschlossen (`bridge_mode`, `bridge_target`, `bridge_ticket`, `bridge_review_until`; Ticket `MSG-2026-0087`).
- `MASTER_TASK_LIST.md`: Status-Snapshot auf den reduzierten Restbestand (`9` Issues / `4` invalide Bridges) und die Eskalationen `MSG-2026-0089` / `MSG-2026-0090` fortgeschrieben.
### Validiert
- `./7w_wiki.py repair --fix-roamlinks --auto`
- `./7w_wiki.py audit --json`
- `./7w_wiki.py pages validate --json --strict-links`
- `./7w_wiki.py advisor --json`

#### [2026-04-03.01] - Historian Research: Astrael-/Waldelfen-Kanon gegen Live-Homepage abgeglichen
### Prioritaet: P2
### Geändert
- `Logs/Research/RESEARCH-2026-010-011_Summary.md`: den bisherigen Kurzbericht zu einem datierten Historiker-Gutachten ausgebaut. Der Bericht trennt jetzt explizit zwischen Live-Kanon (Homepage am 2026-04-03), archivierten offiziellen News/Hintergrundquellen und aktuellem Wiki-Bestand.
- `MASTER_TASK_LIST.md`: Status-Ueberblick und P2-Research-Block auf den Abschluss von `MSG-2026-0005` aktualisiert.
- `System/Synapse_Board/DISPATCH/MSG-2026-0005_forschungsauftrag_inquisition_g_tter_elfen.md`: Forschungsauftrag durch den Historian uebernommen und abgeschlossen.
- `System/Synapse_Board/DISPATCH/MSG-2026-0082_session_kickoff_complete_start_snapshot.md` und `System/Synapse_Board/DISPATCH/MSG-2026-0083_lore_gelehrter_standby_and_queue_triage.md`: Session-Start- und Lore-Triage-Status fuer die Dispatch-Historie abgelegt.
### Validiert
- Live-Abgleich gegen `https://www.siebenwind.de/hintergrund/gotterwelt/kirche-der-viere/`
- Live-Abgleich gegen `https://www.siebenwind.de/hintergrund/rassen-und-klassen/waldelfen/`
- Live-Abgleich gegen `https://www.siebenwind.de/hintergrund/rassen-und-klassen/myten/`
- `./7w_wiki.py search "Astrael rückt auf" --source all --json --fast`
- `./7w_wiki.py search "Waldelfen Myten" --source all --json --fast`

#### [2026-03-31.01] - Magie-Cluster: publizierte Report-Ziele auf kanonische Theorie- und Ritualseiten gehoben
### Prioritaet: P1
### Geändert
- `Logs/Ingestion/2026-02-16_Dunvallo_Linari_-_Alte_Magietheorie.md`: generische Zielspalte `[[Magie]]` auf `[[Magietheorie_Linari]]` gehoben.
- `Logs/Ingestion/2026-02-16_Dunvallo_Linari_-_Magietheoretische_Grundlagen_zur_Zauberwirkung_Matrixtheorie.md`: generische Zielspalte `[[Magie]]` auf `[[Matrixtheorie_Linari]]` gehoben.
- `Logs/Ingestion/2026-02-20_Dunkelbaum_Eigenschaften_Elemente.md`: `[[Magie_Elementarmagie]]` auf `[[Magietheorie_Eigenschaften_der_Elemente]]` gehoben.
- `Logs/Ingestion/2026-02-14_Linari_Thesen.md`: `[[Magietheorie_Grundlagen]]` auf `[[Magietheorie_Linari]]` gehoben.
- `Logs/Ingestion/2026-02-14_Linari_Rituale.md`, `Logs/Ingestion/2026-02-14_Linari_Artefakte.md` und `Logs/Ingestion/2026-02-14_Liebig_Wesenheiten.md`: `[[Magische_Rituale]]` auf `[[Rituallehre_Sphaeren]]` gehoben.
- `CHANGELOG.md`, `MASTER_TASK_LIST.md` und `Logs/Archive/SESSION_MEMORY_2026-03-31_MAGIE_CLUSTER.md`: Snapshot-Delta und den naechsten Cluster nachgezogen.
### Validiert
- `./7w_wiki.py pages validate --json --fast --skip-audit`
- `./7w_wiki.py pages validate --json --skip-audit`

#### [2026-03-30.04] - Historie-Cluster: Zeitstrahl auf Historie & Ären retargetiert
### Prioritaet: P1
### Geändert
- `docs/Siebenwind_Wiki/05_Geschichte/Zeitstrahl.md`: alle neun unresolved `[[Historie]]`-Vorkommen konservativ auf `[[Historie_&_Ären|Historie]]` gehoben. Das Ziel wurde gegen die bestehende Chronikseite `docs/Siebenwind_Wiki/04_Chronik/Historie_&_Ären.md` verifiziert.
- `CHANGELOG.md`, `MASTER_TASK_LIST.md` und `Logs/Archive/SESSION_MEMORY_2026-03-30_HISTORIE_CLUSTER.md`: Snapshot-Delta und die neue Priorisierung auf den Magie-Cluster nachgezogen.
### Validiert
- `./7w_wiki.py pages validate --json --fast --skip-audit`
- `./7w_wiki.py pages validate --json --skip-audit`

#### [2026-03-30.03] - Publish-Hygiene-Cluster: Religions-Resolver-Reste aus Reports und Maintainer-Doku reduziert
### Prioritaet: P1
### Geändert
- `docs/Siebenwind_Wiki/01_Pantheon/Der_naive_Mensch.md`: den Linkstil fuer den Sammelbegriff `Gottheiten` von der Alias-Form auf `Gottheiten (siehe [[Religion_Übersicht]])` umgestellt, damit der Zielbegriff nicht weiter als eigener Wikilink-Target im aktiven Wiki auftaucht.
- `docs/Siebenwind_Wiki/04_Chronik/Siebenwind_Bote_128.md`, `docs/Siebenwind_Wiki/04_Chronik/Siebenwind_Bote_159.md`, `docs/Siebenwind_Wiki/04_Chronik/Siebenwind_Bote_187.md` und `docs/Siebenwind_Wiki/07_Persoenlichkeiten/Utrich_Rothnang.md`: Alias-Formen `[[Kirche_der_Viere|Die Kirche]]` auf direkten kanonischen Linkstil `[[Kirche_der_Viere]]` zurueckgefuehrt.
- `Logs/Ingestion/2026-02-15_Aequitas.md`, `Logs/Ingestion/2026-02-15_Alles_ohne_Pointe.md`, `Logs/Ingestion/2026-02-15_Althea_Danea_-_Kompendium_der_Wei·magie.md`, `Logs/Ingestion/2026-02-16_Der_Blutrote_Stier.md`, `Logs/Ingestion/2026-02-16_Der_Traum_der_Tausend.md`, `Logs/Ingestion/2026-02-16_Der_letzte_Falke.md` und `Logs/Ingestion/2026-02-16_Die_Goldenen_Tafeln.md`: publizierte Ingestion-Reports normalisiert, sodass `Die Kirche`-/`Gottheiten`-Resolver-Reste nicht mehr ueber den Symlink `docs/Archiv/Ingestion_Reports -> ../../Logs/Ingestion` in den Pages-Build eingespeist werden.
- `CHANGELOG.md`, `MASTER_TASK_LIST.md` und die Session-Logs vom 2026-03-30: maintainerseitige Religions-Target-Nennungen auf Plaintext bzw. kanonische Zielseiten umgestellt, damit die Doku selbst keine kuenstlichen unresolved targets mehr erzeugt.
- `.agent/data/religion_cluster_review.json` und `.agent/data/religion_cluster_escalations.json`: Religions-Cluster auf einen Publish-/Archiv-Follow-up fortgeschrieben; die verbliebenen aktiven Content-Rewrites gelten damit als abgeschlossen.
### Validiert
- `./7w_wiki.py pages validate --json --skip-audit`
- `./7w_wiki.py test --suite content-contract`
- `./7w_wiki.py test --suite render-hygiene`
- `./7w_wiki.py test --suite interop-doc-links`

#### [2026-03-30.02] - Religions-Cluster Phase 2: Kontext-Heuristik angewandt, Resolver-Rest offengelegt
### Prioritaet: P1
### Geändert
- `docs/Siebenwind_Wiki/01_Pantheon/Der_naive_Mensch.md`: den Zielbegriff `Gottheiten` auf `Religion_Übersicht` gehoben.
- `docs/Siebenwind_Wiki/04_Chronik/Siebenwind_Bote_128.md`, `docs/Siebenwind_Wiki/04_Chronik/Siebenwind_Bote_159.md`, `docs/Siebenwind_Wiki/04_Chronik/Siebenwind_Bote_187.md` und `docs/Siebenwind_Wiki/07_Persoenlichkeiten/Utrich_Rothnang.md`: kontextsichere galadonisch-viergoettliche Vorkommen von `Die Kirche` explizit auf `[[Kirche_der_Viere|Die Kirche]]` gehoben.
- `docs/Siebenwind_Wiki/03_Gesellschaft/Ecclesia_Elementorum.md`: ambige Selbstreferenz `Die Kirche` zu `Die Gemeinschaft` entschaerft.
- `docs/Siebenwind_Wiki/03_Gesellschaft/Kirche_der_Viere.md`: alte freischwebende `[[Die Kirche der Viere in Galadon]]`-Verweise auf den echten Quellenpfad `docs/Quellen/Hintergrund/Die Kirche der Viere in Galadon.md` umgestellt.
- `.agent/data/religion_cluster_review.json` und `.agent/data/religion_cluster_escalations.json`: Phase-2-Stand nachgezogen; verbleibende Religionsziele werden jetzt als Resolver-/Archiv-Rest dokumentiert statt als weitere sichere Content-Rewrites.
- `MASTER_TASK_LIST.md`: aktiven Fokus vom reinen Religions-Review auf Religions-Resolver-/Archivreste verschoben.
### Validiert
- `./7w_wiki.py pages validate --json --fast --skip-audit`
- `./7w_wiki.py pages validate --json --skip-audit`
- `./7w_wiki.py pages validate --json --strict-links` (weiter am bekannten Audit-/Bridge-Altbestand rot)
- `./7w_wiki.py test --suite content-contract`
- `./7w_wiki.py test --suite render-hygiene`
- `./7w_wiki.py test --suite interop-doc-links`

#### [2026-03-30.01] - Konservativer Religions-Cluster: Enhor-Alias bereinigt, Institutionen/Gattungsziele eskaliert
### Prioritaet: P1
### Hinzugefügt
- `.agent/data/religion_cluster_review.json` und `.agent/data/religion_cluster_escalations.json`: Arbeitsartefakte fuer die konservative Religions-Welle mit Delta-Nachweis, Review-Status und expliziten Eskalationen fuer institutionelle/generische Restziele.
- `Logs/Archive/SESSION_MEMORY_2026-03-30_RELIGION_CLUSTER.md`: Sitzungsprotokoll fuer den Religions-/Pantheon-Cluster mit Baseline, Ergebnis und Restfaellen.
### Geändert
- `docs/Siebenwind_Wiki/09_Bibliothek/Die_Elemente_ungleiche_Geschwister.md`: Doppelte Frontmatter-/Legacy-Layout-Reste entfernt, Metadatenblock normalisiert und den abgeleiteten Wiki-Verweis `[[En'Hor]]` konservativ auf `[[Die_Enhor|Enhor]]` gehoben; reine Quellenorthographie wurde dabei nicht angefasst.
- `docs/Siebenwind_Wiki/01_Pantheon/Der_naive_Mensch.md`: Doppelte Frontmatter-/Legacy-Layout-Reste entfernt und Metadatenblock normalisiert; der generische Zielbegriff `Gottheiten` blieb in Phase 1 noch bewusst unangetastet und wurde zunächst in die Eskalationsliste ueberfuehrt.
- `MASTER_TASK_LIST.md`: Fokus auf den laufenden Religions-Cluster und die explizit review-pflichtigen Restziele `Gottheiten`, `Die_Kirche` und `Die_Vier_Kirchen` aktualisiert.
### Validiert
- `./7w_wiki.py pages validate --json --fast --skip-audit`
- `./7w_wiki.py pages validate --json --skip-audit`
- `./7w_wiki.py pages validate --json --strict-links` (bleibt am bekannten Altbestand im Audit-Precheck rot)
- `./7w_wiki.py test --suite content-contract`
- `./7w_wiki.py test --suite render-hygiene`
- `./7w_wiki.py test --suite interop-doc-links`

#### [2026-03-28.01] - Pantheon-Navigation symmetrisiert und Sahor/Enhor-Nomenklatur geklaert
### Prioritaet: P1
### Geändert
- `mkdocs.yml`: Die Sonderbehandlung von `Astrael` in der GitHub-Pages-Navigation wurde beendet. `Pantheon und Religion` fuehrt die Vier nun symmetrisch als Gruppe `Die Viere (Sahor)` und stellt `Die Elementarherren (Enhor)` als eigene Pantheon-Gruppe daneben.
- `docs/Siebenwind_Wiki/01_Pantheon/Das_Pantheon.md`: Ueberschriften auf die kanonische Begriffspaare `Die Viere (Sahor)` und `Die Elementarherren (Enhor)` ausgerichtet.
- `docs/Siebenwind_Wiki/00_Fundament/Religion_Übersicht.md`: Doppelbenennung praezisiert (`Viere` als alltagsreligiöser Begriff, `Sahor`/`Enhor` als kosmologisch-theologische Sammelnamen), fehlerhaften `Rien`-Link repariert und den alten Agenten-Review-Satz entfernt.
- `docs/Siebenwind_Wiki/00_Fundament/Viere.md`, `docs/Siebenwind_Wiki/00_Fundament/Die_Viere_Kirche.md`, `docs/Siebenwind_Wiki/03_Gesellschaft/Kirche_der_Viere.md` und `docs/Siebenwind_Wiki/03_Gesellschaft/Ecclesia_Elementorum.md`: Begriffs- und Institutionsseiten erklaeren jetzt sauber die Beziehung `Viere <-> Sahor` und `Elementarherren <-> Enhor`; offensichtliche Placeholder-/Syntaxreste wurden bereinigt.
### Validiert
- `./7w_wiki.py test --suite content-contract`
- `./7w_wiki.py test --suite render-hygiene`
- `./7w_wiki.py test --suite interop-doc-links`
- `./7w_wiki.py pages validate --json --skip-audit`

#### [2026-03-27.01] - Konservative Lane-1 Backlog-Welle für Pages und Contract-Drift
### Prioritaet: P1
### Hinzugefügt
- `.agent/scripts/repair.py`: Neue Backlog-Modi `--backlog-board` und `--apply-lane1` erzeugen ein clusterbasiertes Arbeitsboard, eine Eskalationsliste und die erste konservative Auto-Welle fuer mechanische Pages-/Contract-Reparaturen.
- `.agent/data/backlog_cluster_board.json` und `.agent/data/backlog_escalations.json`: Maschinenlesbare Artefakte fuer Cluster-Reihenfolge, Lane-Zuordnung und strittige Restfaelle.
- `.agent/tests/suites/backlog-repair-contract.json`: Vertrags-Suite fuer die neuen Backlog-Repair-JSON-Surfaces.
### Geändert
- `.agent/scripts/content_contract.py`: `category: [[...]]` im Frontmatter wird jetzt kanonisch auf Klartext-/Ordnerkategorie normalisiert; `quelle:`-Felder mit kaputten Wikilinks werden robuster in Plaintext ueberfuehrt.
- `.agent/scripts/repair.py`: Lane-1 repariert konservativ Alias-/Umlaut-/Syntaxdrift mit genau einem kanonischen Zielkandidaten, normalisiert `category`-Wikilinks und hebt `quelle:`-Felder bei eindeutigem Quellenlookup auf echte relative Pfade.
- `7w_wiki.py`, `.agent/workflows/tech_master.md`, `.agent/workflows/test_run.md` und `MASTER_TASK_LIST.md`: Runtime und Wartungsdoku kennen jetzt das Backlog-Board und die konservative Lane-1-Welle.
### Validiert
- `python3 -m py_compile 7w_wiki.py .agent/scripts/repair.py .agent/scripts/content_contract.py`
- `./7w_wiki.py test --suite backlog-repair-contract`
- `./7w_wiki.py repair --backlog-board --json`
- `./7w_wiki.py repair --apply-lane1 --dry-run --auto --json`
- `./7w_wiki.py repair --apply-lane1 --auto --json`
- `./7w_wiki.py audit --pages --json`
- `./7w_wiki.py pages validate --json --strict-links --skip-audit`
- `./7w_wiki.py advisor --json`

#### [2026-03-26.01] - Pages Fast Precheck, Telemetrie & Backlog-Triage
### Prioritaet: P1
### Hinzugefügt
- `./7w_wiki.py pages validate --fast`: Neuer advisory Vorcheck auf Basis gecachter Analyseartefakte. Der schnelle Modus liefert Fruehwarnung fuer Drift-/Link-/Contract-Signale, ersetzt aber bewusst keinen echten MkDocs-Gate-Lauf.
### Geändert
- `7w_wiki.py`, `.agent/scripts/pages_tool.py`, `.agent/scripts/pages_integrity.py` und `.agent/scripts/register_check.py`: Pages- und Audit-Ausgaben enthalten jetzt Timing-/Phasenfelder sowie Cache-Metadaten (`hit`, `inputs_fingerprint`, `duration_ms`) fuer Docs-Linkindex, Canonical-Name-Index und Tree-Drift-Analyse.
- `.agent/scripts/advisor.py`: Empfehlungen verweisen nun auf den praezisen harten Gate `./7w_wiki.py pages validate --json --strict-links` statt auf das unschaerfere `--strict`.
- `.agent/scripts/content_contract.py` und `.agent/scripts/repair.py`: Legacy-Indexziele, verschachtelte Quellenlinks und Umlaut-/Alias-Drift werden robuster normalisiert; viele `quelle:`-Felder und Bote-Referenzen im Wiki wurden auf das kanonische Contract-Format ueberfuehrt.
- `mkdocs.yml`: Unnoetige `roamlinks`-Plugin-Option entfernt, damit der Build nicht mehr mit einem vermeidbaren Konfigurations-Warnsignal startet.
- `MASTER_TASK_LIST.md`, `.agent/workflows/tech_master.md`, `.agent/workflows/test_run.md` und `System/MCP/README.md`: Dokumentation auf `--fast`-Vorcheck, Timing-Transparenz und den naechsten Pages-Backlog-Track angepasst.
### Validiert
- `python3 -m py_compile 7w_wiki.py .agent/scripts/advisor.py .agent/scripts/content_contract.py .agent/scripts/pages_integrity.py .agent/scripts/pages_tool.py .agent/scripts/register_check.py .agent/scripts/repair.py`
- `./7w_wiki.py test --suite content-contract`
- `./7w_wiki.py test --suite split-brain-guard`
- `./7w_wiki.py test --suite takeover-handover`
- `./7w_wiki.py test --suite interop-doc-links`
- `./7w_wiki.py test --suite workflow-matrix-contract`
- `./7w_wiki.py test --suite tool-manifest-contract`
- `./7w_wiki.py test --suite codex-workflow-bridges`
- `./7w_wiki.py test --suite pages-link-contract`
- `./7w_wiki.py pages validate --json --skip-audit`
- `./7w_wiki.py pages validate --json --fast --skip-audit`
- `./7w_wiki.py audit --pages --json`
- `./7w_wiki.py advisor --json`

#### [2026-03-10.03] - Handover Closeout & Workflow Bridge Parser Fix
### Prioritaet: P2
### Behoben
- `.agent/scripts/generate_workflow_bridges.py`: Der Parser beendet `codex_bridge_followups` jetzt sauber, sodass spaetere Workflow-Bullets nicht mehr in generierte Codex-Bridge-Follow-ups auslaufen.
- `.agents/skills/session_handover/SKILL.md`: Die generierte Handover-Bridge listet wieder nur die kanonischen Follow-up-Kommandos statt Verzeichnis-Bullets aus dem restlichen Workflow.
### Geändert
- `MASTER_TASK_LIST.md`: `Last Handover` und Status-Ueberblick fuer die naechste Session aktualisiert.
### Validiert
- `./7w_wiki.py test --suite all`
- `./7w_wiki.py test --suite codex-workflow-bridges`
- `./7w_wiki.py tech --sync-bridges`
- `./7w_wiki.py stats`

#### [2026-03-10.02] - Codex Bridge Docs Polish
### Prioritaet: P2
### Geändert
- `AGENTS.md`: Neue menschenlesbare Sektion `Codex Workflow Bridges` mit praktischer Zuordnung von `session_start`, `workflow_forum_search` und dem `/scout` vs. `/forum_search` Split.
- `System/AGENT_OPERATIONS_HANDBOOK.md`: Maintainer-Regel ergänzt, dass Workflow-Bridges ausschließlich aus Workflow-Metadaten generiert werden und `tech --sync-bridges` Schreibzugriff auf `.agents/skills/` benötigt.
### Validiert
- `./7w_wiki.py test --suite codex-workflow-bridges`
- `./7w_wiki.py test --suite interop-doc-links`

#### [2026-03-10.01] - Codex Workflow Bridges & Forum Search Split
### Prioritaet: P1
### Hinzugefügt
- `.agent/workflows/forum_search.md`: Neuer dedizierter Workflow fuer board-first Forenquellensuche und Ingestion-Leads.
- `.agent/scripts/generate_workflow_bridges.py`: Generator fuer Codex-facing Workflow-Bridges in `.agents/skills/`.
- `.agent/tests/suites/codex-workflow-bridges.json`: Vertrags-Suite fuer generierte Workflow-Bridges und die Bereinigung veralteter Bridge-Namen in den Docs.
- Generierte Workflow-Bridges: `.agents/skills/session_start/`, `.agents/skills/session_takeover/`, `.agents/skills/session_handover/`, `.agents/skills/workflow_tech_master/`, `.agents/skills/workflow_test_run/`, `.agents/skills/workflow_forum_search/`.
### Geändert
- `7w_wiki.py`: `tech --sync-bridges` und `tech --sync-interop` regenerieren nun neben Skill-Bridges auch die Codex-Workflow-Bridges.
- `.agent/scripts/update_matrix.py`: Workflows koennen jetzt explizit auf bestehende Runtime-Adapter gemappt werden; `/forum_search` wird dadurch als spezialisierter, aber ausfuehrbarer Pfad ueber `scout` dargestellt.
- `start`, `takeover`, `handover`, `tech_master`, `test_run`, `scout`, `ingest_master` und die Interop-Dokumente modellieren nun explizit den Split zwischen breitem `/scout` und dediziertem `/forum_search`.
- `docs/Agenten/interop.md`, `docs/Agenten/workflows.md`, `AGENTS.md`, `System/AGENT_OPERATIONS_HANDBOOK.md`, `System/Synapse_Board/SY_INTEROP.md`, `System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md` und `System/COORDINATION_HUB.md` dokumentieren jetzt den Codex-Bridge-Ansatz statt veralteter Pseudo-Bridge-Namen wie `onboarding` oder `test-run`.
### Validiert
- `./7w_wiki.py tech --sync-interop`
- `./7w_wiki.py test --suite codex-workflow-bridges`
- `./7w_wiki.py test --suite workflow-matrix-contract`
- `./7w_wiki.py test --suite interop-doc-links`
- `./7w_wiki.py test --suite all`

#### [2026-03-09.03] - Pages Integrity & Tech Cadence Hardening
### Prioritaet: P1
### Hinzugefügt
- `.agent/scripts/pages_integrity.py`: Gemeinsame MkDocs-/Roamlinks-Diagnostik fuer `pages`, `audit`, `repair` und `advisor`.
- `.agent/config/pages_link_policy.json`: Maschinenlesbare Allowlist-/Planned-Fix-Policy fuer bekannte unresolved Pages-Targets.
- `.agent/data/pages_health.json`: Runtime-Snapshot fuer Advisor, Workflows und Tech-Hygiene.
- `.agent/tests/suites/pages-link-contract.json`: Vertrags-Suite fuer Pages-Health, Snapshot, Policy und Advisor-Freshness.
### Geändert
- `7w_wiki.py`: `audit --pages`, `repair --fix-roamlinks [--auto] [--dry-run]` und `pages validate --json [--strict-links]` sind jetzt Teil des kanonischen Runtime-Vertrags; `run_script()` propagiert Exitcodes, ohne JSON-Ausgaben durch Wrapper-Fehlertexte zu korrumpieren.
- `.agent/scripts/pages_tool.py`, `.agent/scripts/register_check.py`, `.agent/scripts/repair.py`, `.agent/scripts/advisor.py`: Pages-Integritaet wird ueber Build-Warnungen normalisiert, in Audit/Repair eingespeist, als Snapshot persistiert und im Advisor mit Freshness-/Tech-Hygiene-Signalen exponiert.
- `AGENTS.md`, `System/Synapse_Board/SY_INTEROP.md`, `System/AGENT_OPERATIONS_HANDBOOK.md`, `System/MCP/README.md`, `System/COORDINATION_HUB.md` und die Standard-Workflows dokumentieren jetzt den Pages-Health-Loop (`audit --pages`, `pages validate --json`, `repair --fix-roamlinks`) als regulare Technik-/QA-Praxis.
- `.agent/scripts/test_runner.py` versteht verschachtelte JSON-Pfad-Asserts und respektiert suite-spezifische Timeouts fuer die neuen langsamen Pages-Kontrakte.
### Validiert
- `./7w_wiki.py tech --sync-interop`
- `./7w_wiki.py advisor --json`
- `./7w_wiki.py pages validate --json --skip-audit`
- `./7w_wiki.py repair --fix-roamlinks --dry-run`
- `./7w_wiki.py test --suite pages-link-contract --timeout 300`
- `./7w_wiki.py test --suite all`

#### [2026-03-09.02] - Workflow & Interop Consistency Hardening
### Prioritaet: P1
### Hinzugefügt
- `.agent/scripts/sync_runtime_docs.py`: Neue Sync-Strecke fuer die generierten Runtime-Command-Register in `AGENTS.md`, `SY_INTEROP.md` und `AGENT_OPERATIONS_HANDBOOK.md`.
- `.agent/tests/suites/interop-command-registry.json`, `.agent/tests/suites/workflow-matrix-contract.json`, `.agent/tests/suites/tool-manifest-contract.json`: Neue Vertrags-Suiten fuer Live-CLI-Inventar, Matrix-Regeneration und typisierte Tool-Manifeste.
### Geändert
- `7w_wiki.py`: `--help-json` liefert nun typisierte Argument-Metadaten, verschachtelte Subcommand-Schemata und Command-Metadaten fuer Interop-Generatoren; `mail` ist als strukturierte Subcommand-Familie modelliert; `tech` exponiert Matrix-/Doc-/Interop-Sync ueber die Runtime; Oracle-Python-Aufloesung ist plattformfaehig.
- `.agent/scripts/update_matrix.py`, `.agent/scripts/generate_tools_manifest.py`, `System/MCP/generate_mcp_tools.py`, `System/MCP/server.py`: Interop-Oberflaechen werden jetzt aus derselben typisierten CLI-Beschreibung erzeugt; strukturierte Subcommand-Tools und deprecated compatibility aliases bleiben parallel verfuegbar.
- `AGENTS.md`, `System/Synapse_Board/SY_INTEROP.md`, `System/AGENT_OPERATIONS_HANDBOOK.md`, `System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md` und die Kern-Workflows wurden auf konsistente Runtime-Semantik, aktuelle Workflow-Namen und den `scout`-Sonderfall vereinheitlicht.
### Validiert
- `./7w_wiki.py tech --sync-interop`
- `./7w_wiki.py test --suite interop-command-registry`
- `./7w_wiki.py test --suite workflow-matrix-contract`
- `./7w_wiki.py test --suite tool-manifest-contract`
- `./7w_wiki.py test --suite interop-doc-links`
- `./7w_wiki.py test --suite process-dispatch-curiosity`
- `./7w_wiki.py test --suite bridge-placeholder-guard`
- `./7w_wiki.py test --suite all`

#### [2026-03-09.01] - Handover Run Dispatch Autofill
### Prioritaet: P1
### Geändert
- `7w_wiki.py`: Bare `mail post` steps inside `handover --run` now auto-resolve to a structured dispatch using the latest `Logs/Archive/SESSION_MEMORY_*.md`.
- `.agent/workflows/handover.md`: Defect warning replaced with the documented auto-dispatch defaults for the handover closeout step.
- `.agent/tests/suites/takeover-handover.json`: Added regression coverage for the documented handover auto-dispatch behavior.
### Validiert
- `./7w_wiki.py handover --run --yes --resume`
- `./7w_wiki.py test --suite takeover-handover`
- `./7w_wiki.py test --suite clean-client-state`

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



*Ältere Einträge siehe `docs/Archiv/CHANGELOG_ARCHIVE_FEB_2026.md`.*
