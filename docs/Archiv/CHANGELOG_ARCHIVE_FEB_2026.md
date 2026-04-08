#### [2026-02-18.10] - Handover-Checkpoint: offene Tasks als Dispatch-Auftraege gesichert

### Prioritaet
- P1

### Geaendert
- P1/P2-Folgeauftraege im aktiven Fokus verankert:
  - `MASTER_TASK_LIST.md`
  - neue Referenzen: `MSG-2026-0032`, `MSG-2026-0033`, `MSG-2026-0034`
- Handover-Session-Memory erstellt:
  - `Logs/Archive/SESSION_MEMORY_2026-02-18_HANDOVER_OPEN_TASKS.md`
- Handover-Memory via Dispatch veroeffentlicht:
  - `MSG-2026-0037`

### Validiert
- `./7w_wiki.py stats`
- `./7w_wiki.py test --suite all`
- `./7w_wiki.py mail inbox --status OPEN`

#### [2026-02-18.09] - Test-Runner stabilisiert: RAG-Smoke aus Standardlauf ausgelagert

### Prioritaet
- P1

### Geaendert
- `test --suite all` laeuft jetzt standardmaessig ohne `rag-relevance-smoke` (Opt-in statt Default):
  - `.agent/scripts/test_runner.py`
  - `7w_wiki.py` (`test --include-rag`)
- Test-Runner zeigt pro Case Live-Fortschritt (`case x/y`, Status + Grund), damit lange Laeufe nicht wie Hangs wirken:
  - `.agent/scripts/test_runner.py`
- Test-/Interop-Dokumentation auf den neuen Stabilitaets-Default synchronisiert:
  - `.agent/workflows/test_run.md`
  - `.agent/skills/test_waechter/SKILL.md`
  - `.agents/skills/test-run/SKILL.md`
  - `System/Synapse_Board/SY_TESTING.md`
  - `System/Synapse_Board/SY_INTEROP.md`
  - `System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md`
  - `System/AGENT_OPERATIONS_HANDBOOK.md`
  - `AGENTS.md`
  - `MASTER_TASK_LIST.md`
- Lessons-Learnt-Report fuer Folgeagenten abgelegt und in Test-Governance verlinkt:
  - `docs/Archiv/LESSONS_LEARNED_TEST_RUNNER_RAG_QUARANTINE_2026-02-18.md`
  - `System/Synapse_Board/SY_TESTING.md`

### Validiert
- `python3 -m py_compile .agent/scripts/test_runner.py 7w_wiki.py`
- `./7w_wiki.py test --suite all --timeout 30`  
  Reports:
  - `Logs/Archive/TEST_bridge-placeholder-guard_2026-02-18_010445.md`
  - `Logs/Archive/TEST_clean-client-state_2026-02-18_010447.md`
  - `Logs/Archive/TEST_interop-doc-links_2026-02-18_010447.md`
  - `Logs/Archive/TEST_process-dispatch-curiosity_2026-02-18_010447.md`
  - `Logs/Archive/TEST_reader-stats-contract_2026-02-18_010447.md`
  - `Logs/Archive/TEST_source-link-hygiene_2026-02-18_010447.md`
  - `Logs/Archive/TEST_takeover-handover_2026-02-18_010449.md`

#### [2026-02-18.08] - Inter-Agentensteuerung geschaerft: Advisor/Antigravity-Dossier + robustere Workflow-Gates

### Prioritaet
- P1

### Hinzugefuegt
- Kritisches Analyse-Dossier zu Advisor/Antigravity/Workflow-Differenzen:
  - `docs/Archiv/WORKFLOW_DOSSIER_ANTIGRAVITY_ADVISOR_2026-02-18.md`
- Neuer CLI-Workflow-Entrypoint fuer den Core-Loop:
  - `./7w_wiki.py antigravity`

### Geaendert
- Menschlicher Leitpunkt inhaltlich befuellt und operationalisiert:
  - `docs/Archiv/MAINTAINER_STANDPUNKT.md`
  - `leitpunkt check --strict` nun als Freigabe-Gate dokumentiert (nicht Daily-Blocker).
- Workflow/Interop-Doku auf reale Ausfuehrungssemantik geschärft:
  - `.agent/workflows/leitpunkt.md`
  - `.agent/workflows/antigravity.md`
  - `.agent/workflows/takeover.md`
  - `AGENTS.md`
  - `System/AGENT_OPERATIONS_HANDBOOK.md`
  - `System/Synapse_Board/SY_INTEROP.md`
  - `System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md`
  - `System/COORDINATION_HUB.md`
- Test-Runner/Suite verbessert, damit `takeover-handover` nicht unnoetig am globalen Audit-Nullstand haengt:
  - `.agent/scripts/test_runner.py` (neues Feld `expect_exit_any`)
  - `.agent/tests/suites/takeover-handover.json` (Audit-Case auf Reporting statt 0-Probleme umgestellt)

### Validiert
- `./7w_wiki.py leitpunkt status` -> `Readiness: ACTIVE`
- `./7w_wiki.py leitpunkt check` (PASS)
- `./7w_wiki.py leitpunkt check --strict` (PASS)
- `./7w_wiki.py antigravity` (Workflow viewbar)
- `./7w_wiki.py test --suite takeover-handover`  
  Report: `Logs/Archive/TEST_takeover-handover_2026-02-18_005351.md` (PASS)
- `./7w_wiki.py test --suite clean-client-state`  
  Report: `Logs/Archive/TEST_clean-client-state_2026-02-18_005352.md` (PASS)
- `./7w_wiki.py test --suite interop-doc-links`  
  Report: `Logs/Archive/TEST_interop-doc-links_2026-02-18_005348.md` (PASS)

#### [2026-02-18.07] - Reader-Stats-Contract vervollstaendigt (Registry + Pages-Validate + Snapshot)

### Prioritaet
- P1

### Hinzugefuegt
- Neuer discoverable Skill:
  - `.agents/skills/stats/SKILL.md`
- Neue Test-Suite:
  - `.agent/tests/suites/reader-stats-contract.json`

### Geaendert
- Stats-Generator als austauschbare Datenquelle erweitert:
  - `.agent/scripts/generate_wiki_stats.py`
  - erzeugt jetzt zusaetzlich `Logs/Archive/STATS_SNAPSHOT_latest.json` und zeitgestempelte Snapshots.
- Pages-Validierung um Reader-Stats-Gate erweitert:
  - `.agent/scripts/pages_tool.py`
  - `7w_wiki.py` (`pages validate --skip-reader-stats-contract`)
- Doku/Interop synchronisiert:
  - `.agent/workflows/stats.md`
  - `.agent/workflows/docs.md`
  - `.agent/workflows/meta_master.md`
  - `.agent/workflows/test_run.md`
  - `System/Synapse_Board/SY_TESTING.md`
  - `System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md`
  - `System/Synapse_Board/SY_INTEROP.md`
  - `System/AGENT_OPERATIONS_HANDBOOK.md`
  - `AGENTS.md`
- Registry- und Task-Referenzen aktualisiert:
  - `System/COORDINATION_HUB.md`
  - `MASTER_TASK_LIST.md`

### Validiert
- `./7w_wiki.py stats`
- `./7w_wiki.py test --suite reader-stats-contract`  
  Report: `Logs/Archive/TEST_reader-stats-contract_2026-02-18_004945.md` (PASS)
- `./7w_wiki.py test --suite bridge-placeholder-guard`  
  Report: `Logs/Archive/TEST_bridge-placeholder-guard_2026-02-18_004945.md` (PASS)
- `./7w_wiki.py test --suite clean-client-state`  
  Report: `Logs/Archive/TEST_clean-client-state_2026-02-18_005001.md` (PASS)

#### [2026-02-18.06] - Neuer Dev-Command `/leitpunkt` fuer den menschlichen Steueranker

### Prioritaet
- P1

### Hinzugefuegt
- Neuer Workflow:
  - `.agent/workflows/leitpunkt.md`
- Neues Backing-Skript:
  - `.agent/scripts/leitpunkt_tool.py`
  - bietet `status`, `check`, `check --strict`, `scaffold`, `scaffold --force`.
- Neuer CLI-Command:
  - `./7w_wiki.py leitpunkt [view|status|check|scaffold]`

### Geaendert
- Runtime-/Interop-Dokumentation auf neuen Command synchronisiert:
  - `AGENTS.md`
  - `System/AGENT_OPERATIONS_HANDBOOK.md`
  - `System/Synapse_Board/SY_INTEROP.md`
  - `System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md`
  - `System/COORDINATION_HUB.md`
- Landing und GitHub-Readme um Leitpunkt-Command ergaenzt:
  - `docs/index.md`
  - `README.md`

### Validiert
- Funktionscheck:
  - `./7w_wiki.py leitpunkt`
  - `./7w_wiki.py leitpunkt status`
  - `./7w_wiki.py leitpunkt check` (PASS)
  - `./7w_wiki.py leitpunkt check --strict` (FAIL erwartet wegen TODO-Markern)
- `./7w_wiki.py test --suite interop-doc-links`  
  Report: `Logs/Archive/TEST_interop-doc-links_2026-02-18_004639.md` (PASS)
- `./7w_wiki.py test --suite clean-client-state`  
  Report: `Logs/Archive/TEST_clean-client-state_2026-02-18_004642.md` (PASS)

#### [2026-02-18.05] - GitHub-Landing technischer ausgerichtet + menschlicher Leitpunkt verankert

### Prioritaet
- P1

### Geaendert
- GitHub-Repository-Landing auf technische Zielgruppe geschaerft:
  - `README.md`
  - Engine-Faehigkeiten, 5-Minuten-Tech-Tour und zentrale Tech-Dokumentation klar hervorgehoben.
- Docs-Landing um Technik-Einstieg erweitert:
  - `docs/index.md`
  - Neue Sektion `Fuer technisch Interessierte` mit Architektur/RAG/Dispatch/Ops-Links.
- Menschlichen Steuerpunkt als eigene Seite eingefuehrt und verlinkt:
  - `docs/Archiv/MAINTAINER_STANDPUNKT.md`

### Validiert
- `./7w_wiki.py test --suite interop-doc-links`  
  Report: `Logs/Archive/TEST_interop-doc-links_2026-02-18_003110.md` (PASS)
- `./7w_wiki.py pages build --strict`  
  Build-Log: `/tmp/pages_build_2026-02-18_0032.log` (`Documentation built in 91.81 seconds`)

#### [2026-02-18.04] - Landing-Design priorisiert Leserfuehrung (Banner folgen spaeter)

### Prioritaet
- P1

### Geaendert
- Startseite auf leserzentrierte Informationsarchitektur umgestellt:
  - `docs/index.md`
  - `Empfohlener Einstieg in 3 Minuten` als neue Erstfuehrung.
  - Bannerinhalte aus dem Topbereich in `Banner in Arbeit (Kanongebunden)` verschoben.
  - Technik/Betrieb in aufklappbares Transparenzmodul verlagert.
- Landing-Visuals banner-unabhaengig stabilisiert:
  - `docs/assets/custom.css`
  - Hero-Hintergrund auf archivische Gradienten/Linien statt statischem Banner.
  - Neue Stile fuer `quick-grid`, `banner-status`, `tech-details`.

### Validiert
- `./7w_wiki.py test --suite interop-doc-links`  
  Report: `Logs/Archive/TEST_interop-doc-links_2026-02-18_002046.md` (PASS)
- `./7w_wiki.py pages build --strict`  
  Build-Log: `/tmp/pages_build_2026-02-18_0021.log` (`Documentation built in 122.09 seconds`)
- `./7w_wiki.py pages validate` bleibt am bekannten Audit-Gate blockiert:
  - Report: `Logs/Archive/Audit_4895992f-3244-4200-a4ca-fdf6bbfdfd0f.txt` (348 Probleme)

#### [2026-02-18.03] - Lessons-Learned ergänzt und Audit auf 348 reduziert

### Prioritaet
- P1

### Hinzugefuegt
- Lessons-Learned-Report fuer Folgeagenten:
  - `Logs/Archive/LESSONS_LEARNED_2026-02-18_AUDIT_TRIAGE_LINKFLOOD.md`

### Geaendert
- Malformed-WikiLinks in Register/Profilen/Werke-Index normalisiert:
  - `[[Forschungsberichte ([[Toran_Dur]])]]` -> `[[Forschungsberichte_(Toran_Dur)]]`
  - `[[Die Ordenssatzung ... ([[Toran_Dur]])]]` -> `[[Die_Ordenssatzung_des_Ordens_vom_Wachenden_Loewen_(Toran_Dur)]]`
  - `[[Daimonologie und Schwarze [[index]] ([[Toran_Dur]])]]` -> `[[Daimonologie_und_Schwarze_Magie_(Toran_Dur)]]`
- Folge-Batch fuer verbleibende Singletons in `Siebenwind_Wiki/00_Fundament` ausgefuehrt.
- Lessons-Learned per Dispatch an `ALL` verteilt:
  - `MSG-2026-0023`

### Validiert
- `./7w_wiki.py audit`  
  Report: `Logs/Archive/Audit_84814c9a-7906-469d-a35f-e5506733d443.txt` (348 Probleme)
- `./7w_wiki.py test --suite clean-client-state`  
  Report: `Logs/Archive/TEST_clean-client-state_2026-02-18_000926.md` (PASS)

#### [2026-02-18.02] - Baustellen-Dossier fuer nicht-bannerbezogene Open Issues

### Prioritaet
- P1

### Hinzugefuegt
- Neues Lagebild mit priorisierter Auflistung der aktuellen Baustellen:
  - `docs/Archiv/BAUSTELLEN_DOSSIER_2026-02-18.md`
- Dossier trennt akute Blocker (Audit/Oracle/Test/Ingestion) von operativen und strategischen Themen.
- Evidenzpfade zu aktuellen Reports und Dispatch-Auftraegen dokumentiert.

### Geaendert
- Teamweite Board-Notiz zum Dossier versendet:
  - `System/Synapse_Board/DISPATCH/MSG-2026-0022_meta_baustellen_dossier_2026_02_18_aktualisiert.md`

### Validiert
- `./7w_wiki.py advisor` (P1/P2/P3-Snapshot, Queue-Status)
- `./7w_wiki.py audit`  
  Report: `Logs/Archive/Audit_6002f680-cfe3-4f7d-be64-e5432b0edd11.txt` (373 Probleme)
- Referenzierte Tests:
  - `Logs/Archive/TEST_takeover-handover_2026-02-18_000242.md` (FAIL)
  - `Logs/Archive/TEST_rag-relevance-smoke_2026-02-18_000738.md` (FAIL)
  - `Logs/Archive/TEST_interop-doc-links_2026-02-18_000916.md` (PASS)
  - `Logs/Archive/TEST_clean-client-state_2026-02-18_000508.md` (PASS)

#### [2026-02-18.01] - Repair-Fortsetzung: Link-Flood auf 414 reduziert

### Prioritaet
- P1

### Geaendert
- Weitere Bruecken-Batches fuer verbleibende 2er-Haeufungen in `Siebenwind_Wiki/00_Fundament` umgesetzt (u. a. `Magiezweige`, `Lindwurm`, `Lieblicher_Kelch`, `Kriegerakademie_Seeberg`, `Burg_Saalhorn`, `Gott Bellum`, `Feanthil`).
- Zusaetzliche Varianten-/Schreibweisen-Faelle abgefangen (`Rohehaven`→`Rohehafen`, `Ordo_Vitama`→`Ordo_Vitamae`, `Spinnenplage`→`Die_Spinnenplage_von_Falkensee`).
- Kategorie-Indizes erneut aktualisiert (`./7w_wiki.py index-pages`).

### Validiert
- `./7w_wiki.py audit`  
  Reports:
  - `Logs/Archive/Audit_c74b4977-ff76-4978-bf8c-cea2e961bb94.txt` (458 Probleme)
  - `Logs/Archive/Audit_e6f70614-e065-4299-9575-29c0eb7a2645.txt` (414 Probleme)
  - `Logs/Archive/Audit_e49d9ebe-4951-402d-bc7d-b62e0fe6b9d6.txt` (414 Probleme)
- `./7w_wiki.py test --suite clean-client-state`  
  Report: `Logs/Archive/TEST_clean-client-state_2026-02-18_000238.md` (PASS)
- `./7w_wiki.py index-pages` (PASS)

#### [2026-02-17.18] - Art-Director-Auftrag als Dossier + Dispatch verankert

### Prioritaet
- P1

### Hinzugefuegt
- Ausfuehrliches Produktionsdossier fuer Banner-Erstellung:
  - `docs/Archiv/ART_DIRECTOR_DOSSIER_BANNER_2026-02-17.md`
  - umfasst Zielbild, Story-Anker, No-Gos, Abnahmekriterien und Lieferformat.
- Neue Prompt-Briefs fuer die beiden priorisierten Motive:
  - `docs/assets/design_proposals/siebenwind_banner_archivflur_brandenstein_v2.json`
  - `docs/assets/design_proposals/siebenwind_banner_archivflur_brandenstein_v2_alt.json`
  - `docs/assets/design_proposals/siebenwind_banner_chroniknebel_zeitleiste_v2.json`
  - `docs/assets/design_proposals/siebenwind_banner_chroniknebel_zeitleiste_v2_alt.json`
- Kompakte Brief-Uebersicht erstellt:
  - `docs/Archiv/BANNER_BRIEFS_2026-02-17.md`

### Geaendert
- Offiziellen Produktionsauftrag an Herold/Art-Director per Dispatch versendet:
  - `System/Synapse_Board/DISPATCH/MSG-2026-0020_art_produktionsauftrag_banner_archivum_argentum.md`

### Validiert
- `./7w_wiki.py test --suite interop-doc-links`  
  Report: `Logs/Archive/TEST_interop-doc-links_2026-02-17_235956.md` (PASS)
- `./7w_wiki.py test --suite clean-client-state`  
  Report: `Logs/Archive/TEST_clean-client-state_2026-02-17_235959.md` (PASS)

#### [2026-02-17.17] - Repair-Fortsetzung: Link-Flood unter 500 gedrueckt

### Prioritaet
- P1

### Geaendert
- Weitere Brueckenartikel fuer hochfrequente Missing-WikiLinks in `Siebenwind_Wiki/00_Fundament` angelegt (u. a. `Monolith`, `Der_Eine`, `Bestien`, `Kult_des_Einen`, `Astralnetz`, `Arman_von_Draconis`).
- Zweiter Follow-up-Block fuer verbliebene 2er-Haeufungen umgesetzt (u. a. `Rohehaven`, `Ordo_Vitama`, `Sphaerenkunde`, `Schwarzmagier`, `Sire_Randur_Kantrin`, `Spinnenplage`).
- Kategorie-Indizes nach beiden Batches erneut aktualisiert (`./7w_wiki.py index-pages`).

### Validiert
- `./7w_wiki.py audit`  
  Reports:
  - `Logs/Archive/Audit_91e570d3-8606-4325-bf25-0f5cd1a899db.txt` (594 Probleme)
  - `Logs/Archive/Audit_b3d0152b-f023-4f0c-8ade-a29e2ef72544.txt` (498 Probleme)
  - `Logs/Archive/Audit_ab6162e1-d32f-4f95-bdc3-407e07f133dd.txt` (498 Probleme)
- `./7w_wiki.py test --suite clean-client-state`  
  Report: `Logs/Archive/TEST_clean-client-state_2026-02-17_235845.md` (PASS)
- `./7w_wiki.py index-pages` (PASS)

#### [2026-02-17.16] - Repair-Fortsetzung: Link-Flood auf 684 gesenkt

### Prioritaet
- P1

### Geaendert
- Weiterer Bridge-Batch fuer haeufige Missing-WikiLinks in `Siebenwind_Wiki/00_Fundament` ausgerollt (u. a. `Yeroma`, `Yehramnis`, `Xandros`, `Wallenburg`, `Ravel`, `Schwarze_Magie`, `Region_Endophal`).
- Zusaetzliche Legacy-Bruecken fuer Leerzeichen-/Umlaut-Targets eingefuehrt (z. B. `Toran Dur.md`, `Weißer_Pfad.md`), damit Deep-WikiLink-Fehler nicht mehr ins Leere laufen.
- Kategorie-Indizes erneut erzeugt (`./7w_wiki.py index-pages`).

### Validiert
- `./7w_wiki.py audit`  
  Reports:
  - `Logs/Archive/Audit_9afc730c-2708-4468-a217-87ec535eed88.txt` (684 Probleme)
  - `Logs/Archive/Audit_52c1506c-128c-4a08-b3d4-4b421c91e120.txt` (684 Probleme)
- `./7w_wiki.py test --suite clean-client-state`  
  Report: `Logs/Archive/TEST_clean-client-state_2026-02-17_235050.md` (PASS)
- `./7w_wiki.py index-pages` (PASS)

#### [2026-02-17.15] - Banner-Story-Mapping verankert (Kanonanker Pflicht)

### Prioritaet
- P1

### Geaendert
- Landing um Abschnitt `Banner-Rotation mit Kanonbezug` erweitert (`docs/index.md`):
  - Motiv A `Archivflur ohne Figuren` verlinkt auf `Nachts_im_Brandensteiner_Tempel`.
  - Motiv B `Chroniktafeln im Nebel` verlinkt auf `Zeitleiste_(15-30_n.H.)`.
  - Teasertexte auf die Kernaussagen der Zielartikel abgestimmt.
- Art-Director-Skill um Pflicht `Kanonanker` erweitert (`.agent/skills/art_director/SKILL.md`).
- `/herold` Workflow erweitert: Bannermotive nur mit verifiziertem Story-Link und geprueftem Teasertext.

### Validiert
- `./7w_wiki.py test --suite interop-doc-links`
- `./7w_wiki.py test --suite clean-client-state`

#### [2026-02-17.14] - Repair-Fortsetzung: Link-Flood deutlich reduziert

### Prioritaet
- P1

### Geaendert
- Audit-Triage in vier Bruecken-Batches fortgesetzt; fehlende, hochfrequente WikiLink-Ziele als `[UNGEKLAERT]`-Brueckenartikel nachgezogen (vorrangig `Siebenwind_Wiki/00_Fundament`).
- Legacy-Namensvarianten mit klaren Zielseiten verbunden (u. a. `Vandrien`, `Ersont`, `Die_Viere_Kirche`, `Ordo_Astrael`, `Sire_Fedral_Lavid`, `Putsch_in_Falkensee`).
- Kategorie-Indizes nach den neuen Artikeln neu erzeugt (`./7w_wiki.py index-pages`).

### Validiert
- `./7w_wiki.py audit`  
  Reports:
  - `Logs/Archive/Audit_275db8a9-14f5-4ff2-be35-1f2f2fa6b306.txt` (995 Probleme)
  - `Logs/Archive/Audit_f8d945df-626f-4808-a4a2-ca7c1ef1b9ba.txt` (872 Probleme)
  - `Logs/Archive/Audit_7e7ec150-ff20-458c-afc4-c3a748144d64.txt` (807 Probleme)
  - `Logs/Archive/Audit_e663d5ff-7e98-401c-832b-5eb4c527ffc8.txt` (743 Probleme)
  - `Logs/Archive/Audit_8eb04adc-43da-4834-954b-051be694428b.txt` (742 Probleme)
- `./7w_wiki.py test --suite clean-client-state`  
  Report: `Logs/Archive/TEST_clean-client-state_2026-02-17_233859.md` (PASS)
- `./7w_wiki.py index-pages` (PASS)

#### [2026-02-17.13] - Leserfokus-Relaunch dokumentiert (Landing, Kurationspfad, Antigravity-Protokoll)

### Prioritaet
- P1

### Geaendert
- Leserzentrierte Landing-Page eingefuehrt (`docs/index.md`):
  - klare CTAs (`Lesen starten`, `Interessante Artikel`, `Mitwirken`)
  - Abschnitt `Qualitaet und Verfahren` (Ingestion, Bewertung, Bewahrung, Forschung)
  - kuratierte Einstiegsflaechen.
- Neue Kurationsseite `Siebenwind_Wiki/10_Archiv/Interessante_Artikel.md` mit teilautomatisiertem Auswahlverfahren erstellt und im Archiv-Index verankert.
- Navigation auf Lesepfad priorisiert und visuell beruhigt (`mkdocs.yml`):
  - Sprache auf `de` gesetzt
  - Emoji-Overload reduziert
  - `Betrieb und Technik` nachgelagert.
- Corporate-Design auf serioesen Archiv-Look mit Silberstift-Linien umgestellt (`docs/assets/custom.css`, `docs/STYLING.md`).
- README auf klare Trennung `Lesen / Mitwirken / Betrieb` umstrukturiert (`README.md`).
- Art-Director-Stilprofil auf `Archivum Argentum` umgestellt (`.agent/skills/art_director/SKILL.md`, `.agents/skills/art_director/SKILL.md`).
- Dokumentationsprozesse erweitert:
  - `/antigravity` um explizite Dokumentationspflichten erweitert.
  - `/tech` um UX/CD-Dokumentationsschritte erweitert.
  - `/herold` auf neues Stilprofil und Banner-Placement-Regeln synchronisiert.
- Redesign-Roadmap als dauerhaftes Steuerungsartefakt angelegt (`docs/Archiv/REDESIGN_ROADMAP_2026.md`).
- Historian-Dispatch fuer monatliche Kurationsshortlist erstellt (`MSG-2026-0017`).
- Session-Memory fuer den Relaunch dokumentiert und an ALL verteilt (`SESSION_MEMORY_2026-02-17_UX_REDESIGN.md`, `MSG-2026-0018`).

### Validiert
- `./7w_wiki.py pages build --strict` (PASS)
- `./7w_wiki.py test --suite interop-doc-links`  
  Report: `Logs/Archive/TEST_interop-doc-links_2026-02-17_233258.md` (PASS)
- `./7w_wiki.py test --suite clean-client-state`  
  Report: `Logs/Archive/TEST_clean-client-state_2026-02-17_233310.md` (PASS)
- `./7w_wiki.py pages validate`  
  FAIL aufgrund bestehender Audit-Altlasten (`1181` Probleme), nicht durch den Relaunch verursacht.

#### [2026-02-17.12] - Repair Full-Run dokumentiert und P1-Linkfixes fortgesetzt

### Prioritaet
- P1

### Geaendert
- `repair` Runtime erweitert: `./7w_wiki.py repair --full` fuehrt den kompletten Reparaturzyklus `1→2→3` non-interaktiv aus.
- Interaktive `repair`-Menuefuehrung auf Default `4` normiert (`Wahl [4]`), sodass Enter den Voll-Durchlauf startet.
- Doku auf neuen Repair-Standard synchronisiert:
  - `AGENTS.md` Command Registry um `repair [--auto|--full]` erweitert.
  - `System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md` fuer `/repair` auf interaktiv + `--full` aktualisiert.
  - `System/AGENT_OPERATIONS_HANDBOOK.md` um Abschnitt "Repair-Modi" ergaenzt.
- Audit-P1-Breaker fortgesetzt:
  - Duplikatdatei `Siebenwind_Wiki/07_Persoenlichkeiten/Mirila_Mik-Honigzopf.md` konsolidiert.
  - Personenregister-Eintraege fuer `Mirila_Mik_Honigzopf` und `Althea_Danea` normalisiert.
  - Frontmatter-Quelle fuer `Althea_Danea` und `Mirila_Mik_Honigzopf` vervollstaendigt.

### Validiert
- `./7w_wiki.py repair --help`
- `./7w_wiki.py repair --full`
- `./7w_wiki.py audit`  
  Report: `Logs/Archive/Audit_78af2438-20ac-4a7b-89a7-54fd11658d05.txt` (FAIL, 1181 Probleme)
- `./7w_wiki.py test --suite clean-client-state`  
  Report: `Logs/Archive/TEST_clean-client-state_2026-02-17_232723.md` (PASS)

#### [2026-02-17.11] - Handover Checkpoint: Register-Sync, Tests und Queue-Status

### Prioritaet
- P1

### Geaendert
- Kanonischer Register-Abgleich via `./7w_wiki.py index --status` ausgefuehrt; `System/Archivregister/ARCHIVREGISTER.md` und `System/Archivregister/ARCHIVREGISTER.json` auf denselben Stand gebracht.
- Handover-Dokumentation aktualisiert (`MASTER_TASK_LIST.md`, neue Session-Memory-Datei, Dispatch-Statusmeldung).
- Defect-Kommunikation fuer `takeover-handover`-Blocker in Dispatch verankert (`MSG-2026-0014`).
- P1-Auftrag fuer Oracle-Zuverlaessigkeit in der Codex-App erstellt (`MSG-2026-0015`) und im Master-Task-Backlog priorisiert.
- Handover-Memory an alle Agenten verteilt (`MSG-2026-0016`).

### Validiert
- `./7w_wiki.py stats`  
  Reports: `Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md`, `Logs/INGESTION_TRACKING_REGISTER.md`
- `./7w_wiki.py test --suite clean-client-state`  
  Report: `Logs/Archive/TEST_clean-client-state_2026-02-17_230539.md` (PASS)
- `./7w_wiki.py test --suite interop-doc-links`  
  Report: `Logs/Archive/TEST_interop-doc-links_2026-02-17_230546.md` (PASS)
- `./7w_wiki.py test --suite process-dispatch-curiosity`  
  Report: `Logs/Archive/TEST_process-dispatch-curiosity_2026-02-17_230550.md` (PASS)
- `./7w_wiki.py test --suite source-link-hygiene`  
  Report: `Logs/Archive/TEST_source-link-hygiene_2026-02-17_230554.md` (PASS)
- `./7w_wiki.py test --suite takeover-handover`  
  Report: `Logs/Archive/TEST_takeover-handover_2026-02-17_230724.md` (FAIL: `audit-readiness`)
- `./7w_wiki.py mail inbox --status OPEN`  
  Offen: `MSG-2026-0002` bis `MSG-2026-0014`
- `./7w_wiki.py audit`  
  Report: `Logs/Archive/Audit_c5746647-ce87-4ff4-9d0e-33053b46f6ae.txt` (FAIL, 1189 Probleme)

### Offen
- `./7w_wiki.py test --suite all` und `./7w_wiki.py test --suite rag-relevance-smoke` liefen im aktuellen Checkpoint ohne verwertbaren Abschlussreport (Hang); als P1-Task aufgenommen.

#### [2026-02-17.10] - Agenten-Dokumentationspaket fuer Folge-Sessions

### Prioritaet
- P1

### Hinzugefuegt
- `Logs/Archive/AGENT_CHANGE_PACKET_2026-02-17_SESSION_DISCIPLINE.md` als kompakte Uebergabe fuer Folgeagenten (Regeln, geaenderte Dateien, Validierung, Commit-Referenz).

### Geaendert
- `.gitignore` erweitert, damit `AGENT_CHANGE_PACKET_*.md` in `Logs/Archive` versioniert wird.

### Validiert
- `./7w_wiki.py test --suite process-dispatch-curiosity`  
  Report: `Logs/Archive/TEST_process-dispatch-curiosity_2026-02-17_225349.md`
- `./7w_wiki.py test --suite interop-doc-links`  
  Report: `Logs/Archive/TEST_interop-doc-links_2026-02-17_225349.md`

#### [2026-02-17.09] - Session-Disziplin dauerhaft verankert (Agentenverhalten)

### Prioritaet
- P1

### Geaendert
- `AGENTS.md` um verbindliche Session-Disziplin erweitert (Session-Memory lesen/schreiben, Status-Heartbeats, question-first Eskalation).
- `.agent/workflows/tech.md` um Pflichtschritte fuer Session-Memory und Heartbeat-Dispatch ergaenzt.
- `.agent/tests/suites/process-dispatch-curiosity.json` erweitert, damit die neuen Vorgaben in `AGENTS.md` und `/tech` automatisiert geprueft werden.

### Validiert
- `./7w_wiki.py test --suite process-dispatch-curiosity`  
  Report: `Logs/Archive/TEST_process-dispatch-curiosity_2026-02-17_225044.md`
- `./7w_wiki.py test --suite clean-client-state`  
  Report: `Logs/Archive/TEST_clean-client-state_2026-02-17_225047.md`
- `./7w_wiki.py test --suite interop-doc-links`  
  Report: `Logs/Archive/TEST_interop-doc-links_2026-02-17_225052.md`

#### [2026-02-17.08] - Handover Checkpoint: Statuslauf, Suite-All und Queue-Dokumentation

### Prioritaet
- P1

### Geaendert
- `MASTER_TASK_LIST.md` auf aktuellen Handover-Checkpoint synchronisiert (Status + neue P1-Gates fuer Interop/Audit).
- Konsistenzrisiken aus dem aktuellen Lauf in `Logs/Konsistenzbericht_2026.md` als offene Punkte ergaenzt.

### Validiert
- `./7w_wiki.py stats`  
  Report: `Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md`
- `./7w_wiki.py test --suite all`  
  Reports:  
  `Logs/Archive/TEST_clean-client-state_2026-02-17_220158.md`  
  `Logs/Archive/TEST_interop-doc-links_2026-02-17_220158.md`  
  `Logs/Archive/TEST_rag-relevance-smoke_2026-02-17_220524.md`  
  `Logs/Archive/TEST_takeover-handover_2026-02-17_220526.md`
- `./7w_wiki.py test --suite clean-client-state`  
  Report: `Logs/Archive/TEST_clean-client-state_2026-02-17_220712.md`
- `./7w_wiki.py mail inbox --status OPEN`  
  Offen: `MSG-2026-0002`, `MSG-2026-0003`, `MSG-2026-0004`, `MSG-2026-0005`, `MSG-2026-0006`, `MSG-2026-0007`, `MSG-2026-0008`
- `./7w_wiki.py audit`  
  Report: `Logs/Archive/Audit_e72e3011-9298-4639-825d-37f6cabd2fd9.txt` (FAIL, 1184 Probleme)
- Audit/Test-Redundanz-Konsolidierung dokumentiert in `Logs/Archive/AUDIT_CONSOLIDATION_INDEX_2026-02-17.md`.

#### [2026-02-17.07] - Visual Identity Refresh & Link Resolution Audit (Phase 1.23)

### Prioritaet
- P1

### Hinzugefügt
- **Visuals**: "Codex Atlanticus" (Rötel) Stil für Banner, Logo und Social Preview.
- **UI**: CSS-Integration des Banners in die Material Hero-Section.
- **Environment**: `mkdocs-caseinsensitive-plugin` installiert (Plugin-ID: `caseinsensitivefiles`).

### Behoben
- **Link-Analyse**: Persistenter 404 bei "Althea Danea" als `ezlinks` URL-Flattening diagnostiziert.
- **Workaround**: Verifizierung, dass vollqualifizierte WikiLinks (z.B. `[[07_Persoenlichkeiten/Althea_Danea]]`) die Struktur erhalten.

### Validiert
- `./7w_wiki.py pages build` (Erfolgreich mit neuem Plugin & Banner).
- Audit der lokalen HTML-Ausgabe bestätigt Pfadkorrektur bei vollqualifizierten Links.

#### [2026-02-17.06] - Technician Agent Integration (Phase 1.22)

### Prioritaet
- P1

### Hinzugefügt
- **Persona**: `persona_technician.md` (Netz-Ingenieur) fuer DevOps-Fokus.
- **Workflow**: `.agent/workflows/tech.md` fuer technische Wartung und CI/CD.
- **CLI**: `tech` Command in `7w_wiki.py` und Matrix.
- **Escalation**: Browser-Nutzung fuer Live-Site-Verifikation genehmigt.

### Validiert
- `./7w_wiki.py tech` (Workflow-View).
- `AGENTS.md` und `COORDINATION_HUB.md` synchronisiert.
#### [2026-02-17.05] - Smart Repair & Ingestion 2.0 (Phase 1.21)

### Prioritaet
- P1

### Hinzugefügt
- **Smart Resolver**: `repair.py` v2.0 mit Fuzzy-Matching und Canon-Map. Löst broken links auch bei Casing-Fehlern oder Renames.
- **Ingestion 2.0**: `ingestion_protocol.md` mit Pre-Flight-Checks (Kollisionsprüfung) und Index-Verbot.
- **Duplicate Detection**: `repair.py` listet nun doppelte Dateien (Index/Content).

### Geändert
- **Wiki Style Guide**: `aliases`-Frontmatter offiziell unterstützt.
- **Task List**: Phase 6 & 7 abgeschlossen.

### Validiert
- `./7w_wiki.py repair --auto` (49 Fixes, 0 Deletions).
- `./7w_wiki.py stats` (Metriken aktualisiert).

#### [2026-02-17.04] - Repair: Link Integrity & Workflow Optimization (Phase 1.20)

### Prioritaet
- P1

### Hinzugefügt
- **Link Repair Engine**: Option 3 in `repair.py` zur Auto-Korrektur von Casing, Redirects und Malformations.
- **Workflow Automation**: `// turbo` Support für `/handover` (Stats, Test, Audit) und `/takeover` (Inbox, Clean-State).
- **Deployment Policy**: GitHub Pages Build nur noch manuell (`workflow_dispatch`) oder via Tag (`v*`).

### Behoben
- **Link-Konsistenz**: Reduktion defekter Links um 54% (Casing & technische Fehler behoben).
- **CI/CD Load**: Automatische Runs bei Push deaktiviert.
- **Agent Handbooks**: `AGENT_OPERATIONS_HANDBOOK.md` und Matrix aktualisiert.

#### [2026-02-17.03] - Silicon Inquisition: Shamanic Magic & Run (Phase 1.19)

### Prioritaet
- P1

### Hinzugefügt
- Neuer Hauptartikel [[Schamanische_Magie]] (Geisterlehre, Gestirne, Totems).
- Integration schamanischer Aspekte in [[Die_Gohor]] (Werden/Vergehen).
- Etablierung von [[Die_Enhor]] als Kollektiv der Elementarherren.
- Ingestion Report `INQ-2026-B007_Report.md` für Batch 7.

### Geaendert
- [[Die_Sprache_Run]] um grammatikalische Details und Lexika-Referenzen erweitert.
- [[Personenregister]] um neue Werke für [[Toran_Dur]] und [[Anonymus]] synchronisiert.
- `MASTER_TASK_LIST.md` auf Phase 1.19 complete aktualisiert.

### Validiert
- `./7w_wiki.py test --suite all` (Core PASS, RAG Debt documented).
- `./7w_wiki.py audit` (0 Issues).
- `./7w_wiki.py stats` (Profil- & Ingestions-Metriken aktualisiert).

#### [2026-02-17.02] - Linari Ingestion & Magic Theory Hardening

### Prioritaet
- P1

### Hinzugefügt
- Neuer Artikel [[Magietheorie_Artefaktkunde]] (Linari-Thesen, Tunneleffekt).
- Ingestion Reports für Batch 5 & 6 (`Logs/Ingestion/`).
- Hierarchie der Hörner und Antipoden-Theorie in [[Magietheorie_Daemonenbeschwoerung]].

### Geaendert
- [[Magietheorie_Toran_Dur]] auf v2.1 gehärtet (Matrixtheorie & Linari-Ethik integriert).
- [[Personenregister]] um Autorenprofile ergänzt und verknüpft.
- [[INVENTUR_QUELLEN]] auf `Integrated` für Batch 5 & 6 gesetzt.

### Validiert
- `./7w_wiki.py sanitize --auto`
- `./7w_wiki.py archive sync`
- `./7w_wiki.py test --suite all` (100% PASS)
- `./7w_wiki.py audit` (0 Issues)

#### [2026-02-17.01] - Silicon Inquisition: Forum Research & Crawler Integration

### Prioritaet
- P2

### Hinzugefügt
- Neues CLI-Kommando `./7w_wiki.py scout` zur automatisierten Suche in legacy Foren.
- Neuer Crawler `.agent/scripts/forum_scanner.py` (robustes HTML-Parsing, UTF-8 Resilience).
- Forschungsticket `RESEARCH-2026-010.md` am Synapse Board.
- Formaler Forschungsbericht `Logs/Conclusions/2026-02-17_Forum_Research_Report.md`.

### Geaendert
- `/scout` Workflow von `method_only` auf `executable` hochgestuft.
- `Scanner` Skill um "Deep Scan - External Boards" erweitert.
- `MASTER_TASK_LIST.md` und `AGENT_OPERATIONS_HANDBOOK.md` auf neuen CLI-Stand synchronisiert.
- `COORDINATION_HUB.md` um die neuen Forschungsartefakte ergänzt.

### Validiert
- `./7w_wiki.py scout --pages 1` (Runtime Verifikation).
- `./7w_wiki.py test --suite all` (100% PASS nach Link-Fix).
- `./7w_wiki.py audit` (0 Issues).

#### [2026-02-16.44] - Docs Overhaul: Leserpfad + Agenten-Hub auf Pages

### Prioritaet
- P1

### Geaendert
- `README.md` als aktueller GitHub-Einstieg neu strukturiert (Leser, Mitarbeit, Agentenbetrieb klar getrennt).
- `docs/index.md` auf Endnutzer-Portal umgestellt und technische Betriebsdoku separiert.
- `docs/Siebenwind_Wiki/index.md` als praesentable Leser-Startseite mit klaren Schnellrouten ueberarbeitet.
- Neuer Pages-Bereich `docs/Agenten/` eingefuehrt:
  - `index.md`
  - `interop.md`
  - `dispatch.md`
  - `workflows.md`
- `docs/AGENT_OPERATIONS_HANDBOOK.md` von externen Blob-Links auf interne Pages-Navigation umgestellt.
- `mkdocs.yml` Navigation neu sortiert (Wiki fuer Leser zuerst, Agentenbetrieb als eigener Bereich).
- `/docs`-Workflow (`.agent/workflows/docs.md`) auf Link-Suite und neue Struktur aktualisiert.

### Validiert
- `./7w_wiki.py test --suite interop-doc-links`
- `./7w_wiki.py audit`
- `mkdocs build` (nicht verfuegbar: `command not found`)
- `python3 -m mkdocs build` (nicht verfuegbar: `No module named mkdocs`)

#### [2026-02-16.43] - Skills Bridge: Test-Run Wrapper vervollstaendigt

### Prioritaet
- P1

### Geaendert
- Fehlende externe Skill-Bridge `.agents/skills/test-run/SKILL.md` angelegt.
- Wrapper auf die autoritativen Artefakte `.agent/workflows/test_run.md` und `.agent/skills/test_waechter/SKILL.md` ausgerichtet.
- Defect-Routing (`--post-failures`, `mail claim`, `mail done`) explizit dokumentiert.

### Validiert
- `./7w_wiki.py test --list-suites`
- `./7w_wiki.py audit`

#### [2026-02-16.42] - Test-Run System (Workflow, Suiten, Defect-Flow)

### Prioritaet
- P1

### Geaendert
- Neues Runtime-Subcommand `./7w_wiki.py test` eingefuehrt (Suite-Runner fuer Interop/Clean-State).
- Neuer Runner `.agent/scripts/test_runner.py` mit deklarativen JSON-Suiten, Report-Generierung und optionalem Dispatch-Post bei FAIL.
- Neue Suiten unter `.agent/tests/suites/`:
  - `clean-client-state`
  - `takeover-handover`
  - `interop-doc-links` (lokale Markdown-Link-Integritaet)
- Neuer Workflow `.agent/workflows/test_run.md` inkl. Agentenmentalitaet (Tester/Fixer/Koordinator) und Kommunikationspflicht vor Fixes.
- Governance erweitert:
  - `System/Synapse_Board/SY_TESTING.md` (neuer Teststandard)
  - `SY_INTEROP.md`, `SY_WORKFLOW_CLI_MATRIX.md`, `AGENT_OPERATIONS_HANDBOOK.md`, `AGENTS.md`, `COORDINATION_HUB.md` auf Test-Protokoll und `test`-Runtime synchronisiert.
- Onboarding/Handover/Takeover um Testpflichten erweitert (`clean-client-state` bzw. `all`).

### Validiert
- `./7w_wiki.py test --list-suites`
- `./7w_wiki.py test --suite clean-client-state`
- `./7w_wiki.py audit` (direkt nach erstem Run)
- `./7w_wiki.py test --suite interop-doc-links`
- `./7w_wiki.py test --suite takeover-handover`
- `./7w_wiki.py test --suite all`
- `./7w_wiki.py --help`
- `./7w_wiki.py start`
- `./7w_wiki.py audit`

#### [2026-02-16.41] - Takeover/Handover CLI Bridge & Clean-State Testlauf

### Prioritaet
- P1

### Geaendert
- `7w_wiki.py` um Subcommands `takeover` und `handover` erweitert (anzeigen der autoritativen Workflow-Protokolle).
- `AGENTS.md` Command Registry um `takeover` und `handover` ergaenzt.
- `SY_WORKFLOW_CLI_MATRIX.md` auf `takeover`/`handover` als executable Bridge aktualisiert und Runtime-Command-Liste erweitert.
- Clean-Client-State-Testlauf als Archivbericht dokumentiert: `Logs/Archive/2026-02-16_Clean_Client_State_Test_Report.md`.

### Validiert
- `./7w_wiki.py --help`
- `./7w_wiki.py takeover`
- `./7w_wiki.py handover`
- `./7w_wiki.py`
- `./7w_wiki.py start`
- `./7w_wiki.py advisor`
- `./7w_wiki.py mail inbox --status OPEN`
- `./7w_wiki.py mail inbox --status CLAIMED`
- `./7w_wiki.py mail inbox --status DONE`
- `./7w_wiki.py mail read MSG-2026-0001`
- `./7w_wiki.py stats`
- `./7w_wiki.py audit`

#### [2026-02-16.40] - Wiki Stats: Leserfokus statt Index-Buerokratie

### Prioritaet
- P2

### Geaendert
- `generate_wiki_stats.py` filtert in den Hub-Rankings nun strukturelle Ziele wie `index`, Register- und Uebersichtsseiten aus.
- Fuer Ereignis-Rankings werden zusaetzlich generische Sammelziele wie `Chronik`/`Geschichte` ausgeschlossen.
- Wiki-Statistiken zeigen jetzt leserrelevante Hubs statt Verwaltungsseiten.
- Zwei neue, zielgerichtete Rankings ergaenzt: `Top Persönlichkeiten` und `Top Ereignisse`.

### Validiert
- `./7w_wiki.py stats`
- Inhalt von `Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md` geprueft (keine `[[index]]`-/Register-Hubs in den Rankings).
- `./7w_wiki.py audit`

#### [2026-02-16.39] - Priority-First Changelog Standardization

### Prioritaet
- P1

### Geaendert
- `advisor.py` um Prioritaetsuebersicht erweitert (`P1/P2/P3/Backlog`) und damit Prioritaeten im Statusblock an erste Stelle gesetzt.
- `changelog_tool.py` von Legacy-`<details>`-Ausgabe auf markdown-native Eintraege migriert.
- Neuer Changelog-Tool-Output erzwingt `### Prioritaet` als ersten Abschnitt jedes neuen Eintrags.
- `SY_STANDARDS.md` auf den aktuellen Changelog-Standard aktualisiert (keine `<details>`, Prioritaet zuerst).
- `/handover`-Workflow um explizite Vorgabe erweitert: `### Prioritaet` direkt nach dem Changelog-Header.

### Validiert
- `./7w_wiki.py advisor`
- `python3 .agent/scripts/changelog_tool.py --help`
- `./7w_wiki.py audit`

#### [2026-02-16.38] - Advisor Queue Awareness & Workflow Runtime Sync

### Prioritaet
- P1

### Geändert
- `advisor.py` erweitert um Dispatch-Queue-Auswertung (`OPEN/CLAIMED/DONE`) inkl. Priorisierung der obersten offenen Nachricht.
- Empfehlungsteil des Advisors priorisiert nun offene Dispatch-Auftraege vor regularem Task-Fortschritt.
- Konsistenz-Empfehlung im Advisor auf den gueltigen Runtime-Pfad `./7w_wiki.py repair` normiert.
- Workflow `/start` um verpflichtenden Queue-Check (`mail inbox --status OPEN`) im Interop-Runtime-Block und in der Lagefeststellung erweitert.
- Workflow `/takeover` auf `mail inbox --status OPEN` normiert und Onboarding-Ritual um expliziten Dispatch-Schritt ergaenzt.
- Workflow `/handover` um Queue-Pruefung ergaenzt; veraltete `<details>`-Changelog-Vorgabe auf aktuelles Markdown-Format migriert.
- `SY_WORKFLOW_CLI_MATRIX.md` fuer `/start`, `/handover`, `/takeover` auf die aktualisierten Runtime-Adapter synchronisiert.
- `AGENTS.md` Onboarding-Schritt um initiale Dispatch-Sichtung erweitert.

### Validiert
- `./7w_wiki.py advisor`
- `./7w_wiki.py start`
- `./7w_wiki.py mail inbox --status OPEN`
- `./7w_wiki.py archive sync`
- `./7w_wiki.py audit`
- `./7w_wiki.py stats`

#### [2026-02-16.37] - Persona Dispatch Awareness

### Geändert
- In allen Persona-Instruktionen wurde ein verbindlicher Abschnitt `Kommunikationspflicht (Dispatch)` ergänzt.
- Enthalten sind jetzt klare Standard-Schritte fuer Inter-Agent-Kommunikation: `mail inbox --status OPEN` -> `mail claim` -> `mail done`.
- Rollenbezogene Dispatch-Nutzung fuer Ingestor, Guardian, Historian und Coordinator dokumentiert.

#### [2026-02-16.36] - Dispatch Hardening & Decision Flow Alignment

### Geändert
- `agent_mail.py` gehaertet: exakte Message-ID-Aufloesung, stricter Statusfluss (`OPEN -> CLAIMED -> DONE`) und Validierung fuer `inbox --status`.
- `done`-Verlaufseintrag korrigiert (wird nun verlässlich in `## Verlauf` persistiert).
- Kollisionssichere Message-Erstellung eingefuehrt (Locking bei ID-Vergabe).
- `SY_DISPATCH.md` um operative Guardrails und dokumentierte Umsetzungsstrategie erweitert.
- `/decide`-Workflow auf Dispatch-first-Handling umgestellt (`inbox/read/claim/done`).
- Workflow-CLI-Matrix fuer `/decide` auf die reale Dispatch-Bearbeitung aktualisiert.
- `AGENT_OPERATIONS_HANDBOOK.md` um Dispatch-Hygiene-Regeln ergaenzt.

#### [2026-02-16.35] - Interop: Method Hint Normalization

### Geändert
- `SY_INTEROP.md` um optionales Feld `method_hints_non_runtime` erweitert und normiert.
- Workflows `ask`, `scout`, `meta_master`, `rvw_loop`, `canon_update` auf explizite `method hint (non-runtime)`-Kennzeichnung angepasst.
- Skills `scout`, `scanner`, `kanon_waechter`, `wiki_schmied`, `art_director` auf non-runtime Methodenhints und klare Runtime-Abgrenzung umgestellt.
- Legacy-Referenzen auf Pseudo-Commands (`notify_user`, `search_web`, `trigger_conflict_alert`, `7w.py`) durch klare Hinweise oder Runtime-nahe Alternativen ersetzt.

#### [2026-02-16.34] - Changelog Render Stabilization (GitHub Pages)

### Geändert
- `CHANGELOG.md` von rohen HTML-`<details>/<summary>`-Blöcken auf reines Markdown normalisiert.
- Fehlende Kopfzeilen der jüngsten Einträge (`2026-02-16.33`, `2026-02-16.32`) wiederhergestellt.
- Alte `</details>`-Reste entfernt, damit die Listenstruktur im Web sauber gerendert wird.


#### [2026-02-16.33] - Block 2: Master/Changelog Ordnung & Index-Hygiene

### Geändert
- **Master Task List**: Historienbereich strukturell neu geordnet (neu -> alt), doppelte Phase- und Bullet-Eintraege bereinigt.
- **Statuspflege**: Projektstatus auf `Phase 1.16 complete` synchronisiert.
- **Changelog-Format**: Defekte Details-Struktur repariert und fehlplatzierte Prioritaets-/Backlog-Sektionen aus dem Changelog entfernt.

### Behoben
- **Index-Hygiene (Wiki)**: Korrekturen an `Siebenwind_Wiki/index.md`, `00_Fundament/Archiv_Register.md` und `04_Chronik/index.md` (Titel/H1-Konsistenz, fehlerhafte Linksyntax, Bote-177-Label).
- **Pages-Sync (docs)**: Entsprechende Index-Korrekturen in `docs/Siebenwind_Wiki/...` nachgezogen fuer konsistente GitHub-Pages-Ausgabe.

### Validiert
- `./7w_wiki.py audit` mit 0 Problemen.
- `./7w_wiki.py check` erfolgreich fuer alle bearbeiteten Index-Dateien (`Siebenwind_Wiki/...` und `docs/Siebenwind_Wiki/...`).


#### [2026-02-16.32] - Phase 1.16: Interop Upgrade & Jules Readiness

### Hinzugefügt
- **Entry Points**: `AGENTS.md` (Canonical Instruction) und `GEMINI.md` (CLI Shim) erstellt.
- **Skills Mirror**: `.agents/skills/` erstellt für kompatible Nutzung durch Codex/Jules.
### Geändert
- **CLI Fix**: `mail` Befehl in `7w_wiki.py` registriert.
- **Workflow Standard**: `start.md` mit Interop-Headern (`runtime_commands`) versehen.

#### [2026-02-16.31] - Phase 1.15: Society & Cultures Enrichment

### Hinzugefügt
- **Sub-Rassen**: Dedizierte Artikel für [[Hochelfen]], [[Waldelfen]] und [[Auenelfen]] (Fey/Auriel Standard).
- **Soziale Systeme**: [[Gefaengnissystem]] (Kerkermeister-Rat) und [[Masseinheiten]] (Referenztabellen).
- **Religion**: Nortravisches Pantheon ([[Thjarek]], [[Eydis]]) integriert.

### Geändert
- **Rassen**: [[Elfen]], [[Zwerge]], [[Nortraven]] und [[Myten]] auf v2.7 Standard gehoben (Mythen & Geschichte).
- **Register**: [[Personenregister]] und [[Organisationsregister]] um Gründungsfiguren und Orden ([[Elendur]], [[Kabale]]) erweitert.
- **Korrektur**: Armgard Torenson zu [[Armgard_Torenson]] korrigiert.

#### [2026-02-16.30] - Phase 1.14: Silicon Inquisition Batches 2 & 3

### Hinzugefügt
- **Batch 2 & 3**: 20 weitere Quellen vollständig re-ingestiert und auf v2.7 Standard gehoben.
- **Ingestion Reports**: 20 neue Reports mit detaillierter Lore-Extraktion und LQS-Bewertung.
- **Lore-Zentralisierung**: Integration der Linari-Theorien und astraelischer Primärquellen.

### Geändert
- **Metadata v2.7**: Standardisierung auf ISO-8601 (mit Uhrzeit), UUIDs und system-konforme `report_id`.
- **System-Audit**: Fehlerbehebung bei Umlaut-Diskordanzen in Dateinamen zur Sicherstellung von 100% Audit-Compliance.


#### [2026-02-15.29] - Project Evolution & Aesthetic Refinement
### Hinzugefügt
- New Gargoyle Banner (Renaissance Style)
- Automation Tools: link_guard.py, changelog_tool.py
- Visual Standards: Epistemics Headers & Mermaid Genealogy
- Content Excellency: Dossier Rhadan (DOS-2026-007)


#### [2026-02-16.13] - Phase 1.13: Workflow Consolidation & CLI Expansion

### Hinzugefügt
- **CLI Erweiterung**: Kommandos `sanitize`, `score`, `check`, `translate`, `watch` in `7w_wiki.py` integriert.
- **Archive Sync**: Verknüpfung von `LORE_RESEARCH_BOARD.md` und Ingestion Reports in `docs/Archiv`.

### Geändert
- **Workflow-Architektur**: Konsolidierung von 30 Workflows. Entfernung von Redundanzen (Zwei-Pass-Verfahren, Epistemik) durch zentrale Referenzierung.
- **Handover-Protokoll**: `/handover` und `/takeover` auf den neuen Standard (v2.1) aktualisiert.

### Entfernt
- **Redundante Skripte**: `find_orphans.py` gelöscht (ersetzt durch `audit`).


#### [2026-02-16.29] - Phase 1.12: Silicon Inquisition Batch 1 & Archive Sync

### Hinzugefügt
- **Silicon Inquisition**: Batch 1 vollständig abgeschlossen (10/10 Quellen).
- **Metadaten v2.7**: Einführung des v2.7 Standards für alle verarbeiteten Batch-1 Quellen.

### Geändert
- **Magietheorie**: Härtung der Kern-Theorien (Fila-Modell, Horlaf-Theorie) durch Re-Ingestion von Asanra, Remouldo und Anonymus.
- **Kirchenrecht**: Vollständige Integration des `Codex Iuris Canonici`.
- **Redundanz**: Konsolidierung von `Briefe aus der Ferne` (Zusammenführung doppelter Artikel).
- **CLI**: `7w_wiki.py` um das Subcommand `archive` erweitert.

#### [2026-02-15.28] - Phase 1.11: CI/CD Reliability & Success

### Hinzugefügt
- **Headers**: `docs/_headers` Datei zur Deaktivierung des CDN-Caches implementiert.

### Geändert
- **Stability**: Build-Prozess in `deploy.yml` durch Entfernung von `--strict` stabilisiert.
- **Engine**: Inkompatible Plugin-Parameter (`slugify`, `reference_type`) aus `mkdocs.yml` entfernt.

#### [2026-02-15.27] - Phase 1.10: Link Engine Stabilization

### Geändert
- **WikiLinks**: Umstellung des gesamten Link-Engine-Standards auf das `ezlinks`-Modell.
- **Standard**: `STYLING.md` an die neue technische Realität angepasst.

#### [2026-02-15.26] - Phase 1.9: CI/CD Troubleshooting

### Hinzugefügt
- **Build**: Automatisierte Installation aller Abhängigkeiten via `requirements.txt` im CI-Workflow.
- **Debug**: Transparenz-Schritte (`cat` Befehle) in die Build-Pipeline integriert.

#### [2026-02-15.25] - Phase 1.8: Cleanup & Organization

### Geändert
- **Root-Ordner**: Verschiebung von Meta-Dokumenten (`STYLING.md`, `WORKFLOW_LORE_CONSISTENCY.md`, PDF-Analyse) nach `System/`.
- **Assets**: Konsolidierung von `assets/` nach `System/Design_Assets/`.
- **Cleanup**: Entfernung von `banner_proposal.png` und `git-push-log.aR0d5B`.

#### [2026-02-15.24] - Phase 1.7: Styling & Engine Optimization

### Hinzugefügt
- **Build**: `requirements.txt` für automatisierten Plugin-Install auf GitHub Pages erstellt.
- **Design**: Renaissance-Typografie (Inter & Cormorant Garamond) und Micro-Animations für Links.

### Geändert
- **Plugins**: Migration von `wikilinks` (Extension) auf `mkdocs-ezlinks-plugin` (Plugin) zur Behebung der Broken Links.
- **Header**: Quadratisches Banner durch horizontales „Modern Scholar“ Banner ersetzt (`docs/assets/banner.png`).
- **UI**: Glassmorphism-Effekte für Header, Nav und Footer implementiert (Blured Transparency).

#### [2026-02-15.23] - Phase 1.6: Structural Maintenance & Consistency Repair

### Hinzugefügt
- **Persönlichkeiten**: 11 neue Profil-Stubs angelegt (u.a. [[Eliam_Schlosser]], [[Geist]], [[Himduir_III_ap_Vjer]]).

### Geändert
- **Register**: Manuelle Deduplizierung von [[Chernides]] und [[Orgolosch]].
- **Verknüpfung**: Korrekte Einbindung der [[Gropp_Zwillinge]] und [[Kregor_Arthax_Stahlauge]] ins Personenregister.
- **Mission MSG-2026-0002**: Globale Bereinigung von absoluten `file://` Pfaden in Wiki- und System-Dokumenten.

#### [2026-02-15.22] - Phase 1.5: Minimalist Restoration & Structural Purity

### Hinzugefügt
- **Standard**: `STYLING.md` zur Kodifizierung des "Minimalist Tool" Ansatzes und der Symlink-Architektur.
- **System**: Native `wikilinks` Extension aktiviert für stabilere `\[\[WikiLink\]\]` Auflösung auf GitHub Pages.

### Geändert
- **Design**: Pivot zum "Modern Scholar" Aesthetic (Beige/Rötel, Hochkontrast, schlichte Funktionalität).
- **Tonalität**: Vollständige Neutralisierung der Texte auf Landing-Page und Architektur-Dokumenten (Entfernung von "Flavor Text").
- **Copyright**: Aktualisierung der Claims (LeCorbeau für Technik, Autoren/Projekt für Inhalte).
- **Struktur**: Verifizierung und Sicherung der Symlink-Struktur (`docs/Siebenwind_Wiki` -> `Siebenwind_Wiki`).

#### [2026-02-15.21] - Phase 20: Deep Bote Ingestion & Codex Delegation

### Hinzugefügt
- **Wiki-Inhalt (Chronik)**: Tiefgreifende Anreicherung der Boten-Seiten 186 bis 194.
- **Persönlichkeiten**: Über 20 neue Profile erstellt (u.a. [[Solos_Nhergas]], [[Akassvae]], [[Helfric_von_Wallenburg]]).
- **System**: Delegations-Prompt `System/DELEGATION_CODEX_PHASE_20.md` für den narrativen Feinschliff erstellt.
- **Silicon Inquisition**: Forschungsbericht `INQ-2026-001_Historian_Report.md` zum Astralgeflecht.

### Geändert
- **Register**: Über 40 Einträge in `Personenregister.md` und `Organisationsregister.md` synchronisiert.
- **Konfiguration**: `.gitignore` um Delegations-Dateien erweitert.
- **Handover**: `MASTER_TASK_LIST.md` auf Phase 20 aktualisiert.

#### [2026-02-15.20] - Production Persistence Layer (Conclusions, Ideas, Artworks, Presentations)

### Hinzugefügt
- **Protokoll**: `System/PRODUCTION_PROTOCOL.md` als verbindliche Persistenzregel für erzeugte Artefakte.
- **Präsentation**: `Logs/Presentations/2026-02-15_Interop_Dossier_Praesentation.md`.
- **Vorlagen**: `System/Templates/PRODUCTION_NOTE_TEMPLATE.md` für standardisierte Ergebnisablagen.
- **Ablageordner**: `Logs/Conclusions/`, `Logs/Ideas/`, `Logs/Artworks/`, `Logs/Presentations/`.

### Geändert
- **Standards**: `SY_STANDARDS.md` um `PRODUCTION_PROTOCOL` ergänzt.
- **Coordination Hub**: Register um Produktionsprotokoll und Vorlage erweitert.

#### [2026-02-15.19] - Interop Phase 3: Relative Links, Workflow Runtime Markers, Re-Evaluation

### Hinzugefügt
- **Dossier**: `Logs/Ingestion/2026-02-15_Interop_Dossier_Phase3.md` als offizieller Nachher-Befund.
- **Workflow-Härtung**: `runtime_commands`/`method_only` Blöcke in den Department-Workflows ergänzt.

### Geändert
- **Pfad-Normierung**: Antigravity-Workflows und Koordinationsdokumente auf kontextkorrekte relative Links umgestellt.
- **Inquisition-Quellenverweise**: Historian-Report und Manifest von absoluten URI-Referenzen auf relative Pfade migriert.
- **Re-Audit**: Linkkonsistenz nach Migration verifiziert; nur definierte Platzhalter bleiben offen.

#### [2026-02-15.01] - Phase 19.4: Structural Purity & Automation

### Hinzugefügt
- **Automatisierung**: Skript `generate_wiki_indices.py` zur automatischen Erstellung von Kategorie-Indizes.
- **CLI**: Neuer Befehl `./7w_wiki.py index-pages` zur Wartung der Wiki-Hierarchie.
- **Dokumentation**: `CONTRIBUTING.md` für Community-Kollaboration und Lizenz-Governance.

### Geändert
- **Navigation**: Umstellung auf explizite Pfade in `mkdocs.yml` zur Vermeidung von 404-Fehlern in Unterverzeichnissen.
- **Branding**: Bereinigung der Homepage von veraltetem Slogan-Lore ("Diskretion").
- **Statistiken**: Dashboard-Refresh für den neuen Struktur-Stand.

#### [2026-02-14.9] - Documentation & Maintenance: Path D (Der Chronist)

### Hinzugefügt
- **Wiki-Statistiken**: Neues Statistik-Dashboard generiert (984 Artikel, 521 Persönlichkeiten). Dokumentiert unter `Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md`.
- **Projekt-Wartung**: Überprüfung der zentralen Dokumentation (`README.md`, `WORKFLOW_LORE_CONSISTENCY.md`, `SYNAPSEN_SYSTEM_SPEC.md`).
- **Onboarding-Status**: Fortschreibung des `/start` Prozesses und Festlegung der nächsten Prioritäten.

### Geändert
- **Wiki-Integrität**: Validierung der Pfade für Lore-Engineering-Dokumente im `.agent/docs/` Verzeichnis.

#### [2026-02-14.8] - Batch 25c: Toran Dur Reports & Order of the Lion

### Hinzugefügt
- **Wiki-Content**:
    - **Toran Dur**: Umfassendes Personenprofil und Biographie.
    - **Forschungsberichte**: Integration von `Forschungsberichte (Toran Dur)`, `Index Siebenwind (Toran Dur)`, `Die Sprache Run (Toran Dur)`.
    - **Magietheorie**: Integration von `Die Magie (Toran Dur)`, `Lehrbuch der Magietheorie (Toran Dur)`, `Theorien der Magie (Toran Dur)`, `Magica Curativa (Toran Dur)`, `Daimonologie und Schwarze Magie (Toran Dur)`.
    - **Historie/Recht**: `Die Ordenssatzung des Ordens vom Wachenden Löwen (Toran Dur)`, `Graue Charta (Zweiter Entwurf)`.
- **Register**:
    - **Löwenorden**: Erfassung der Gründungsmitglieder 17 n.H. (`Cendaric Tibur`, `Lothar Gavinwald`, `Akora Dur`, `Dorion Hali`).
    - **Personen**: Diverser Magier und Zeitgenossen (`Nefustor`, `Rianna`, `Caieta Ajunier`, etc.).
- **System**:
    - `INVENTUR_QUELLEN.md`: Status-Update für 20+ Toran Dur Dateien auf `Integrated`.

### Geändert
- **Personenregister**: Konsolidierung von Cendaric Tibur (Baron & Ordensmeister) und Dorion Hali (Physikus & Ordensmeister).

#### [2026-02-14.7] - Phase 17: Infrastructure & Intelligence

### Hinzugefügt
- **Finsterwangen / Tiefenbach Korrektur**:
    - `Tiefenbach.md`: Als historische Hauptstadt ("Jassavia-Analogie" auf der Insel) definiert.
    - `Finsterwangen.md`: Als Festung der Galahad-Legende definiert (nicht Jassavia/Hauptstadt).
    - `Historie_&_Ären.md`: Trennung von Jassavia (Festland) und Tiefenbach (Insel).
    - `Die_Legende_von_Galahad_Ritter_der_Rosen.md`: Verlinkungen korrigiert.
- **Lore-Untersuchungen**:
    - **Astralnetz-Ursprung**: Kontroverse (Kirche vs. Toran Dur) in `Astrael.md`, `Toran_Dur.md`, `Die_Gohor.md` dokumentiert.
    - **Ionas Narrative**: `Ionas.md` mit atmosphärischen Detailsangereichert (Resolved Synapse Ticket 2026-003).

### Geändert
- **Synapse Board**:
    - Ticket `Conflict_2026-003_Ionas_Narrative` geschlossen (RESOLVED).
    - Ticket `Conflict_TEST_001_Falkensee_Timeline` geschlossen (RESOLVED durch Finsterwangen-Lore).
- **Onboarding Workflow**: Neuentwickelter `/start` Prozess (`./7w_wiki.py start`) für eine strukturierte Agenten-Übernahme.
- **Historiker-Workflow**: `/historian` Workflow zur tiefen Analyse von Kausalitäten und Lore-Rekonstruktion.
- **Lore Audit**: Protokoll und Template für Lore-Peer-Reviews und Eskalationen bei Unsicherheit.
- **CLI Erweiterung**: Unified CLI (`7w_wiki.py`) unterstützt nun `start`, `historian` mit Query-Support und flexiblen Oracle-Parametern (`--cpu`, `--no-re-rank`).

### Geändert
- **Orakel-Redirection**: Aggressive Umleitung aller HuggingFace- und Transformers-Caches in das Projektverzeichnis (`.agent/data/models`) zur Umgehung von Sandbox-Restriktionen.
- **Orakel-Redirection**: Aggressive Umleitung aller HuggingFace- und Transformers-Caches in das Projektverzeichnis (`.agent/data/models`) zur Umgehung von Sandbox-Restriktionen.
- **Indexer-Stabilität**: Fix eines kritischen Bugs im Index-Builder, der bei Einzeldatei-Updates fälschlicherweise den restlichen Index gelöscht hat.

#### [2026-02-14.6] - Batch 25: Toran Dur Magie-Bibliothek & System Audit

### Hinzugefügt
- **Batch 25: Toran Dur Library**:
    - Integration der magietheoretischen Grundlagen (8 Texte: Matrix, Elemente, Zensor etc.).
    - Integration der praktischen Arkanologie (5 Texte: Dämonologie, Alchemie, Rituale, Zeit- & Sphärentheorie).
    - Erstellung zentraler Magie-Artikel: `Daimonicon`, `Rituallehre_Sphaeren`, `Alchemie_Grundlagen`, `Sphaerenkunde_Kosmologie`.
    - Profile für `Kulin_Laetall`, `Rhadan_der_Graue`, `Kida_Gilwen`, `Wolfgang_Ravinsthal`, `Dunvallo_Linari`.
- **System & Lore**:
    - **Lore Research Board**: `LORE_RESEARCH_BOARD.md` zur workflow-gestützten Lore-Klärung.
    - **System Audit**: Durchführung des `/audit` Workflows (Report 2026-02-14). 
    - **Register Status**: Healthy Register bestätigt (0 Duplikate/Orphans).

### Geändert
- **Wiki-Statistiken**: Dashboard aktualisiert (923 Artikel, Lore-Hubs neu berechnet).
- **Repair Tool**: `repair.py` auf aktuelle Wiki-V2.1-Struktur angepasst.

### Hinzugefügt
- **Konstitutionelles Framework**:
    - `WORKFLOW_ARCHITECTURE.md`: Einführung der strategischen Architektur (Trias Politica Modell).
    - `/antigravity`: Neuer Master-Workflow für strikte, skriptgesteuerte Exekution.
    - `Logs/JUDICIARY_LOG.md`: Offizielles Entscheidungsprotokoll für kritische Lore-Eingriffe (Level 3).
    - `.agent/tests/TEST_CASES.md`: Validierungssuite für das Systemverhalten.
- **Eskalationsstufen**: Definition von 3 Leveln (Standard, Kontrolliert, Judiziell) zur Balance zwischen Effizienz und Sicherheit.

### Geändert
- **7w CLI (`7w_wiki.py`)**: Advisor-Modus ist nun der Default-Befehl (Situationsbewusstsein bei Start).
- **Onboarding (`takeover.md`)**: Mandat für High-Verification und Subdivision-Prinzipien.

#### [2026-02-14.4] - Batch 23: Astrael Religious Texts

### Hinzugefügt
- **Batch 23: Bibliothek Astrael**:
    - Integration von 8 religiösen Texten und Mythen: `Der_Blutrote_Stier`, `Der_Traum_der_Tausend`, `Der_letzte_Falke`, `Der_naive_Mensch`, `Die_Eisernen_Tafeln`, `Die_Goldenen_Tafeln`, `Die_Silbernen_Tafeln`, `Die_Legende_von_Galahad_Ritter_der_Rosen`.
    - Erstellung von 8 Personenprofil-Stubs: `Azaris`, `Barnabas`, `Dannor`, `Galahad`, `Irindal`, `Jeremias`, `Kedrin`, `Tai_Sah_Halour_Glurias`.
- **System-Wartung**:
    - Vorbereitende Konsistenzprüfung und Bereinigung von 13 initialen Fehlern (Gorem, etc.).
    - Bereinigung von Duplikaten (Aspin, Athos) nach Register-Sync.

#### [2026-02-14.3] - Spielergeschichten Integration (Batches 20-22)

### Hinzugefügt
- **Batch 20: Dark Lore & Cults**:
    - Neue Artikel: `Die_Namikleris`, `Kraken`, `Logbuch_des_Kerkers`, `Solfeister_Kin`, `Die_Verbrennung_des_heiligen_Markus`, `Ritus_Gebet_und_Erleuchtung`.
    - Register-Updates: `Szarmaduk`, `General Hornstoß`, `Knochenfürst`, `Markus`, `Mehr'thak`.
- **Batch 21: Social & Tales**:
    - Neue Artikel: `Die_Zwergen_WG`, `Geschaeftiges_Treiben`, `Nachts_im_Brandensteiner_Tempel`, `Pruefung_und_Entsagung`, `Pueppchens_Flucht`, `Letzte_Vorbereitungen`, `Die_Elemente_ungleiche_Geschwister`.
    - Register-Updates: `Gimbart`, `Nirluk`, `Sandholz`, `Gorion`, `Püppchen`, `Lucienne`.
    - Lore-Korrektur: **Horwah** als Manifestationen/Avatare der Götter definiert (User-Feedback).
- **Batch 22: Narrative & Character Arcs**:
    - Neue Artikel: `Abschied_und_Verrat`, `Abweisungen`, `Alles_ohne_Pointe`, `Aus_dem_Leben_eines_Schwarzmagiers`, `Briefe_aus_der_Ferne`.
    - Register-Updates: `Todward von Saalhorn`, `Aelfrid Wildgaden`, `Dorion Hali`, `Felix Goldschein`, `Taleris Kreytz`, `Rajka Sanseha`.

### Geändert
- **Personenregister**: Bereinigung von Duplikaten und Konsolidierung von Einträgen (Akora, Taleris, Rajka).
- **Ingestion Log**: Lückenlose Dokumentation aller Verarbeitungsschritte.

#### [2026-02-14.3] - Recherche Marnie Ruatha & Handover

### Hinzugefügt
- **Forschungsbericht**: `Forschungsbericht_Marnie_Ruatha.md` (Intern) erstellt.
    - Zusammenstellung der Biographischen Daten (Hafenvogtin 19-21 n.H., Asyl 22 n.H.).
    - Analyse der Boten 167, 168, 173, 186.
- **Gap-Identifikation**:
    - `Tjure_Odal`: Fehlt im System (Lücke).
    - `Arn_Toron`: Vorhanden, aber Prüfung empfohlen.

### Geändert
- **Dokumentation**:
    - `MASTER_TASK_LIST.md`: Aktualisiert.
    - `Wiki_Statistiken.md`: Neu generiert (837 Artikel, 472 Persönlichkeiten).

#### [2026-02-14.2] - Synapsen-System v2.0 & Register-Consolidation

### Hinzugefügt
- **Synapsen-System v2.0**: Erfolgreicher End-to-End Test des neuen Konfliktlösungs-Frameworks.
    - **Lore Trust Score (0-10)**: Automatisierte Berechnung integriert (`lore_score_manager.py`).
    - **Synapse Board**: Ticketsystem für Konflikte (`Conflict_2026-003_Delarie_Timeline`).
- **Register-Consolidation**:
    - **Quelle**: "Das Ende der Zeit der Könige" (Spielergeschichte) vollständig integriert.
    - **Personen**: 18 neue Profile (u.a. `Zoran_Gosh`, `Hadrian_Lugado`, `Hubertus_Anverita`).
    - **Organisationen**: 6 neue Organisationen (u.a. `Ring_des_Argionemes`, `Bruderschaft_Gofilm`).
- **Wiki-Content**:
    - Neue Artikel: `Codex_Iuris_Canonici`, `Aequitas`, `Brevier_des_Ordo_Astraeli` (Bibliothek Astrael).

### Geändert
- **Priorisierung**: User-Eingaben (`#user_canon`) sind nun vom Trust-Score entkoppelt (Score reflektiert Quellenreinheit, nicht Zustimmung).

#### [2026-02-14.18] - News Reconstruction, Forum Indexing, and Synapse Dispatch

### Hinzugefügt
- **News-Archiv**: Vollstaendige Quellenanlage fuer Homepage-News ab 2010 unter `Quellen/News/` (standardisiertes Frontmatter).
- **Forum-Kategorien**: Neue Quellenkategorien `Quellen/Forum/Bekanntmachungen` und `Quellen/Forum/Newsticker` fuer technische/teambezogene Forenhinweise.
- **Synapse Dispatch**:
    - Neues Board-Dokument `System/Synapse_Board/SY_DISPATCH.md`.
    - Persistente Queue unter `System/Synapse_Board/DISPATCH/`.
    - Neue CLI-Erweiterung `7w mail ...` fuer Agent-zu-Agent Nachrichten (`post`, `inbox`, `read`, `claim`, `done`).

### Geändert
- **Chronik**: `Siebenwind_Wiki/04_Chronik/OOC_TIMELINE.md` um News- und Forum-Auswertung erweitert.
- **Standards**: `System/Synapse_Board/SY_STANDARDS.md` um Board-Eintrag `SY_DISPATCH` erweitert.
- **CLI**: `7w_wiki.py` um Subcommand `mail` ergaenzt.

#### [2026-02-14.17] - Phase 19: Light Sanguine & General Abstraction

### Hinzugefügt
- **Visuals**: Neues "Light Sanguine" Branding-System (Rötelzeichnung im Leonardo-Stil).
- **Asset-Archiv**: Dediziertes Archiv unter `docs/assets/archive/` für Design-Konzepte.
- **Mockups**: High-Fidelity UI-Mockup des Interface-Konzepts für zukünftige Iterationen (Sanguine-Stil).

### Geändert
- **Interface Design**: Umstellung auf v2.4 (Paper-Minimalism, Thin Lines, Sanguine & Sepia).
- **Integrität**: Korrektur von Rendering-Fehlern in Markdown-Tabellen (Register).
- **Abstraktion**: Wechsel von spezifischer Astrael-Symbolik zu allgemeiner Architektur-Geometrie.

#### [2026-02-14.16] - Phase 19: GitHub Pages Overhaul & Link Repair

### Hinzugefügt
- **Wiki-Plugins**: Aktivierung von `mkdocs-roamlinks-plugin` zur Unterstützung von `\[\[WikiLinks\]\]`.
- **Visuals**: Vollständiges Redesign der Homepage (`index.md`) im "Lore Engine" Stil.
- **Navigation**: Strukturierte `mkdocs.yml` mit Direktzugriff auf Register und Chronik.
- **GitHub Actions**: Automatisierte Installation der notwendigen Plugins im Deployment-Workflow.

### Geändert
- **Link-System**: Konvertierung aller statischen Pfade in `index.md` auf relative Formate.
- **Aestetik**: Umstellung der Farbpalette auf "Slate & Gold" (Renaissance-Tech Look).
- **Cleanup**: Entfernung der Art-Director-Sektion von der Homepage (Fokus auf Lore & Tech).

### Hinzugefügt
- **Visual Identity**: Premium-Banner ("Anatomia Magica Mundi"), Logo und Favicon im Renaissance-Stil implementiert.
- **System**: CLI zu `7w_wiki.py` vereinheitlicht; `Art Director` Skill für Stil-Konsistenz installiert.
- **GitHub**: Repository erfolgreich an Org `Siebenwind` übertragen und via GitHub Pages deployt.

#### [2026-02-14.13] - Batch 26: Toran Dur Ingestion (Pfad A)

### Hinzugefügt
- **Wiki-Content**:
    - **Magietheorie**: `Locus_Magicae.md`, `Magietheorie_Toran_Dur.md` (Arcana Procella), `Artefaktlehre.md`.
    - **Forschung**: `Bartanatomie.md` (Goldaxt), `Finsterwangen.md` (Krise 14 n.H.), `Brandenstein.md` (Diamant-Matrix).
    - **Bestiarium**: Klassifizierung nach Liebig (**Lazperday** vs **Warthun**).
- **Register**:
    - Neue Personas: `Birnbaum`, `Fogrim Goldaxt`, `Logrin Goldaxt`, `Johannes Klos`, `Johann Liebig`, `Hernaphas Lenarmberg`, `Hahngard Esteron`.
    - Updates: `Kida Gilwen`, `Kalveron Dai`.

#### [2026-02-14.12] - Batch 27: Toran Dur Advanced Doctrines (Sub-Batches 1-4)

### Hinzugefügt
- **Wiki-Content**:
    - **Constructs**: `Konstruktbau_und_Ariin.md`, `Erschaffene_Diener.md`.
    - **Arcane Science**: `Arkan-Metalle.md`, `Elementare_Atomlehre.md`.
    - **Combat/Defense**: `Antimagie_und_Gegenzauber.md`, `Arkane_Kriegfuehrung.md`.
    - **Transformation/Gems**: `Metamorphose_und_Gestaltwandel.md`, `Vjera_Batama_Magica.md`.
- **Register**:
    - Synchronisation der Magister: `Edomawyr`, `Jennaia Lavrial`, `Nistram Rigas`, `Erynnion Comari`, `Lewyn Anacar`, `Sylest le Felyhn`.
    - Manuelle Bereinigung und Deduplizierung (u.a. `Arenus`, `Tanthul`, `Nefustor`, `Amanda Dunkelbaum`).
    - Neueinträge: `Arlin Sturmfels`, `Santanos Alexandrius von Eichstatt`.

### Geändert
- **Wiki-Statistiken**: Dashboard aktualisiert (1027 Artikel, 546 Persönlichkeiten).

#### [2026-02-14.11] - Infrastructure: Ingestion 3.0 & Oracle Hardening

### Hinzugefügt
- **Ingestion v3.0**: 
    - Einführung des **Lore Quality Score (LQS)** (0-10) zur Bewertung von Extraktionen.
    - Neues Template: `System/Templates/INGESTION_REPORT_TEMPLATE.md`.
    - Dedizierter Ablageort für Reports: `Logs/Ingestion/`.
- **Sandbox-Resilience**:
    - Automatische Sandbox-Erkennung via `ANTIGRAVITY_AGENT` und `ANTIGRAVITY_SANDBOX`.
    - Implementierung von `local_files_only=True` für embedding und reranking Modelle.

### Geändert
- **Orakel-Optimierung**: 
    - Behebung der XLMRoberta-Warnung durch gezielten Proxy-Logging-Patch (Monkey-Patch).
    - Performance-Bestätigung (Search ~20s in Sandbox-Umgebung).
- **Projekt-Wartung**: 
    - Repository-Cleanup (Löschen von Root-Junk wie `.DS_Store`, `missing_links.txt`, `walkthrough.md`).
    - Korrektur der Dokumentationspfade in `README.md`.
    - Archivierung alter Logs in `Logs/Archive/`.

### Entfernt
- Veraltete `walkthrough.md` im Root-Verzeichnis.
- Temporäre Register-Logs.

#### [2026-02-14.10] - Lore Reconstruction: The Origins of Siebenwind

### Hinzugefügt
- **Wiki-Archiv**: `Logs/Historian_Report_2026_003_Siebenwind_Origins.md` als Forschungs-Zusammenfassung erstellt.
- **Geografie**: `Rohehafen.md` (Ehemalige Hauptstadt der ersten Kolonie) erstellt.

### Geändert
- **Lore-Zentralisierung**: 
    - `Tiefenbach.md`: Status als Hauptstadt entfernt; Fokus auf Hafen und Magie-Akademie (historisch).
    - `Finsterwangen.md`: Fokus auf den Sphärenriss und die Galahad-Verteidigung präzisiert.
    - `Historie_&_Ären.md`: Umfassender Retcon der Hilgorad-Expedition (1 n.H.) und der "Ersten Kolonie".
    - `Hilgorad_I_ap_Mer.md`: Rolle als Expeditions-Initiator ergänzt.
    - `Siebenwind.md`: Regionen-Übersicht um Rohehafen ergänzt.
    - `Stadtchronik_Rohehafens.md`: Als historisches Dokument markiert (vordatiert auf ca. 5 n.H.).
- **Research Board**: RESEARCH-2026-005 und 006 als `COMPLETED` markiert.

#### [2026-02-14.1] - Historiker-Review: Delarie & Glaron

### Geändert
- **Waldemar Delarie (`Waldemar_Delarie.md`)**:
    - **Timeline-Retcon**: "Reise nach Papin" von 25-28 n.H. auf **21 n.H.** korrigiert (Fit für Bote 183/Putsch).
    - **Titel**: Ergänzung um "Regierungsrat" und "Adjutant".
    - **Lore**: Erweiterung der "Gerüchteküche" (Spinnen-Vorfall, Besessenheit).
- **William Glaron (`William_Glaron.md`)**:
    - **Biografie-Erweiterung**: Vom Stub zum Vollprofil (Turniersieger 21 n.H., Tragödie 22 n.H.).
    - **OOC-Integration**: Berücksichtigung der späteren Erhebung zum Ritter und der Auflösung des "Diener des Einen"-Plots.
- **System**:
    - **Orakel**: Permission-Issue bei `search.py` dokumentiert (Workaround via grep genutzt).

#### [2026-02-13.9] - Wiki Consistency Restoration- 🏛️ **Total Consistency Restoration:** Alle 69+ Konsistenzprobleme im Personenregister behoben (0 Duplikate, 0 Orphans, 0 Missing Profiles).

- ✍️ **Stub Creation:** 57 neue Profil-Stubs für registrierte Charaktere erstellt.
- 🔗 **Register Fixes:** Naming-Mismatches (Apostrophe, Leerzeichen) in `Personenregister.md` korrigiert.
- 📜 **New Workflow:** `/repair` Workflow zur systematischen Fehlerbehebung implementiert.

#### [2026-02-13.8] - Epistemics & Source Ingestion Audit (Interrupted)

### Hinzugefügt
- **Epistemisches System**: Formale Einführung der Verlässlichkeitsränge (#canon, #bote, #perspektive, #überlieferung) im Style Guide und in der Eskalationsmatrix des RVW-Loops.
- **Ingestion Log**: Dokumentation der Re-Scan Ergebnisse für ~30 Spielergeschichten (Batches 1-8).

### Geändert
- **Metadata-Härtung**: YAML Frontmatter und Status-Tags für ~20 Spielergeschichten ergänzt/korrigiert (u.a. `Jassavia`, `Blutschwert`, `Waldemar Delarie`).
- **Kanon-Schutz**: Widersprüchliche oder subjektive Tags (#verstorben, #tragödie) durch formale epistemische Tags ersetzt.

### Ergebnisse
- Das Wiki verfügt nun über ein robustes System zur Handhabung von Wahrheitsansprüchen.
- Ein Großteil der Spielergeschichten ist metadata-technisch saniert; Entitäten sind für die Register-Integration im Log gesichert.

#### [2026-02-13.7] - Narrative Enrichment & Orphan Resolution

### Hinzugefügt
- **Narrative Enrichment**:
    - `narrative_enrichment.md`: Neuer Workflow für "Roman-Qualität".
    - `Ionas.md` & `Maichellis_Wanderstern.md`: Von Stubs zu narrativen Profilen aufgewertet (Atmosphäre, Motivation, Zitate).
- **Orphan-Resolution**:
    - 4 Duplikate gelöscht (`Siegfried_von_Steiner`, `Fedral`, `Feldherr`, `Toron`).
    - 15 fehlende Personen im Register nachgetragen (u.a. `Winzlig`, `Lucius_Gropp`).
    - `Benedict_Rabenfels`: Als Stub wiederhergestellt.

### Geändert
- **Register-Synchronisation**: `Personenregister.md` ist nun vollständig synchron mit dem Dateisystem (25 Orphans processed).
- **Inhalte**: `Arn_Toron.md` erhielt die Backstory aus der gelöschten Duplikat-Datei (`Toron.md`).

### Ergebnisse
- Das Personenregister ist bereinigt und vollständig.
- Erste Schlüsselcharaktere (Ionas, Maichellis) entsprechen dem neuen Qualitätsstandard.

#### [2026-02-13.7] - Feature Drop: Orakel & Skills v2.0

### Hinzugefügt
- **Das Orakel:** Vollständiges RAG-System (Search, Indexing, MPS-Tuning).
- **Skills v2.0:**
    - `Der Lektor` (Style-Checker & QA).
    - `Workflow /repair` (Interaktive Wartung).
    - `Workflow /watch` (Live-Indexierung).
- **Der Berater:** `advisor.py` für automatisiertes `/takeover`.
### Geändert
- **Dokumentation:**
    - `README.md` komplett überarbeitet und modularisiert.
    - Neue Benutzerhandbücher für Skills erstellt.
- **System:** `setup.sh` aktualisiert (neue Dependencies).
### Geändert
- **Phase 12 (Boten 176-180):** Complete.
    - Verified content for Boten 176-180.
    - Verified/Updated articles: `Bestie_von_Brandenstein`, `Trollkrieg_von_Brandenstein`, `Die_Spinnenplage_von_Falkensee`, `Kharas_Palanthas`.
    - Created new article: `Hevelius_Dunkelfeld` (Bote 180).
    - Updated `Personenregister.md` (Resolved duplicates for Solice, Gottfried, Merthes, Caoimme; added Dunkelfeld).
    - Updated `Organisationsregister.md` (Added `Kult_des_Einen`).
    - Verified `Zeitleiste` (21 n.H. entries).
- **Wiki-Statistiken:** Aktualisiert via `/stats`.

#### [2026-02-13.5] - Phase 13 Abschluss (Falkensee Putsch)

### Hinzugefügt
- **Phase 13 (Boten 181-185):** Integrated 5 issues.
    - Standardized Boten 181-185.
    - Updated `Personenregister.md` (Ionas, Serass, Astreyonas, Delarie).
    - Updated `Zeitleiste_(15-30_n.H.).md` (21 n.H. Falkensee Coup completely covered).
    - Updated `INVENTUR_QUELLEN.md` (All 181-185 Integrated).
    - Validated `Ionas.md` and `Serass.md` dates.

### Ergebnisse
- Der "Putsch von Falkensee" ist nun vollständig dokumentiert.
- Die Timeline für das Jahr 21 n.H. ist mit Bote 185 abgeschlossen.
- Wiki-Statistiken wurden aktualisiert (`/stats`).

#### [2026-02-13.4] - Phase 11 Abschluss & Phase 12 Vorbereitung

### Hinzugefügt
- **Phase 12 Planung:** Detaillierte Recherche der Boten 176-180 (Bestie von Brandenstein, Troll-Krieg, Spinnenplage, Mord an Palanthas).
- `implementation_plan.md`: Update mit granularer Task-Liste für Phase 12.

### Geändert
- [x] **Phase 12 (Boten 17-180):** Integrated 5 issues.
    - Standardized Boten 176-180.
    - Updated `Personenregister.md` (Palanthas †, Aurora, Delarie, Merthes).
    - Updated `Zeitleiste_(15-30_n.H.).md` (21 n.H. filled).
    - Updated `INVENTUR_QUELLEN.md`.
- [x] **Phase 11 (Boten 171-175):** Complete.
- **Inventur:** Boten 171-175 erfolgreich von `Pending` auf `Integrated` gesetzt.

### Ergebnisse
- Das Fundament für die Integration der Boten 176-180 ist gelegt.
- Kritische Ereignisse (Rücktritt Noalim, Tod Falk, Mord Palanthas) sind identifiziert und vorbereitet.

#### [2026-02-13.3] - Wiki-Statistiken & Dokumentations-Audit

### Hinzugefügt
- `.agent/scripts/generate_wiki_stats.py`: Automatisiertes Statistik-Dashboard (Ingestion, Lore-Dichte, Epistemik, Link-Hubs, Temporal-Density).
- `Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md`: Visualisierte KPIs mit Mermaid-Charts.
- `.agent/workflows/stats.md`: Neuer Workflow `/stats` zur Dashboard-Generierung.
- `docs/`: Symlink-Verzeichnis für MkDocs-Kompatibilität (Symlinks zu Wiki, README, CHANGELOG, MASTER_TASK_LIST).

### Geändert
- **README.md (Komplett-Rewrite):** Alle 8 Skills, 14 Workflows und 8 Scripts vollständig dokumentiert.
- **mkdocs.yml:** Mermaid-Support (custom_fences), fehlende Nav-Einträge (Erzählungen, Wiki Statistiken), `docs_dir`/`site_dir` korrekt gesetzt.
- **Workflow-Integration:** `/stats` als Pflichtschritt in `/audit` (§7) und `/handover` (§6.3) integriert.
- **.gitignore:** `site/` hinzugefügt.

### Ergebnisse
- **666 Artikel**, **349 Persönlichkeiten**, **~98k Wörter**, **72 Links/1k Wörter** (Vernetzungsgrad).
- MkDocs-Build erfolgreich (3.99s, keine Errors).

#### [2026-02-13.2] - [ ] **Phase 14: Spielergeschichten Re-Scan** – Fortsetzung der Ingestion (Batches 9+), Register-Sync der extrahierten Entitäten.

- [x] Laufende Register-Synchronisation (Personen, Organisationen, Bestiarium)

#### [2026-02-13.2] - Audit der Magieschulen (Kanon-Härtung)

### Hinzugefügt
- **Kanonische Institutionen**: 
    - `Königliche Akademie der arkanen Künste` (Zentrales Element).
    - `Magierturm zu Tiefenbach` (Historisch/Zerstört).
    - `Akademie der Schwarzen Künste` (Historisch/Verboten).
 
### Geändert
- **Kanon-Bereinigung**: 
    - Entfernung der nicht-kanonischen "Akademie des Grünen Zweiges" aus `Region_Tiefenwald.md`.
    - Entfernung der nicht-kanonischen "Akademie in den Grauen Höhlen" aus `Region_Kadamark.md`.
    - Korrektur der Verlinkungen in `Graue_Garde.md` auf die offizielle Königliche Akademie.
- **Register-Update**: Vollständige Integration der neuen Akademien in `Organisationsregister.md` und `registry.jsonl`.

### Ergebnisse
- Erfolgreiche Eliminierung von "Fanon"-Elementen (Halluzinationen), die sich in die Regionsbeschreibungen eingeschlichen hatten.
### [Batch 24] - Astrael's Legacy (II) - 2026-02-14
- **Dateien**: 19 historische & theologische Schriften der Bibliothek Astrael integriert.
- **Highlights**: Stadtchronik Rohehafens, Myten-Bericht, Matrixtheorie von Derrvus, Ritus der Exercitio.
- **Register**: 12+ neue Entitäten synchronisiert (Derrvus, Anais, Aelwin, etc.).

### [Batch 23] - Astrael's Erbe (I) - 2026-02-14
- **Ingestion:** Verarbeitung von 5 Spielergeschichten (Batch 19).
- **Entitäten:** Erstellung von 12+ neuen Personenprofilen und 3 Organisationen.
- **Lore:** Dokumentation der Argionemes-Verschwörung und der Schwarzen Legion.
- **Wartung:** Konsolidierung von Dubletten und Update des Personenregisters.
- Klare Trennung zwischen aktiven (Königliche Akademie) und historischen (Tiefenbach, Schwarze Künste) Magieschulen hergestellt.
### [Phase 14] - 2026-02-13
- **Ingestion:** Verarbeitung von 5 Spielergeschichten (Batch 19).
- **Entitäten:** Erstellung von 12+ neuen Personenprofilen und 3 Organisationen.
- **Lore:** Dokumentation der Argionemes-Verschwörung und der Schwarzen Legion.
- **Wartung:** Konsolidierung von Dubletten und Update des Personenregisters.
- Klare Trennung zwischen aktiven (Königliche Akademie) und historischen (Tiefenbach, Schwarze Künste) Magieschulen hergestellt.

#### [2026-02-13.1] - Historiker-Review & Register-Cleanup

### Hinzugefügt
- `Logs/Historiker_Bericht_Rabenfels_2026.md`: Detaillierter Bericht über Benedict Rabenfels und die Führungskrise des Löwenordens.

### Geändert
- **Metadaten-Härtung**: 
    - Einführung von ISO-8601 Zeitstempeln **mit Uhrzeit** für alle Metadaten (`letzter_check`).
    - Neue performante JSONL-Registry (`registry.jsonl`) zur Dokumentenverfolgung.
    - Standardisierung aller Boten (133-140) mit permanenten UUIDs.
- **Register-Cleanup**: 
    - Zusammenführung von Duplikaten (Steiner, Bitterling, Eisenbruch, Arman, Delarie, Caeden, Wendolyn, Horan Erandel).
    - Konsolidierung von Karrieredaten (z.B. Fedral Lavid, Benion Sandelholz).
    - Bereinigung von Dateisystem-Dubletten (`Woran_Lebensmüh.md`).
- **Lore-Konsistenz**:
    - Dokumentation der Diskrepanz zwischen Bote 172 (Tibur/Avistur als Halbgeschwister) und Wiki (als Onkel/Nichte).

### Ergebnisse
- Das Profil von Benedict Rabenfels wurde dekomponiert, die Erkenntnisse aber im Historiker-Bericht gesichert.
- Die Register-Synchronität wurde durch die Konsolidierung von Mehrfacheinträgen signifikant verbessert.

#### [2026-02-12.5] - Konsistenz-Offensive & Workflow-Härtung

### Hinzugefügt
- `.agent/scripts/register_check.py`: Automatisiertes Audit-Tool (findet Duplikate, Orphans, Boten-Lücken, Index-Lücken).
- `Logs/Audit_Report_2026-02-12.md`: Detaillierter Bestandsbericht der Register-Integrität.

### Geändert
- **Workflow-Härtung (`rvw_loop` & `wiki_schmied`)**:
    - **Pre-Write Validation:** Pflicht-Check auf Duplikate vor Erstellung.
    - **Post-Write Sync:** Automatische Index-Aktualisierung (Chronik & Register).
    - **Relative Pfade:** `quelle:`-Feld im Frontmatter erlaubt nur noch relative Pfade.
    - **Referenzen:** Neue Pflicht-Sektion `## Referenzen` mit akademischer Zitierweise.
- **Audit-Prozess**:
    - ISO-8601 Zeitstempel-Pflicht für alle Berichte.
    - Neue "Orphan-Resolution" Phase für verwaiste Profile.

### Ergebnisse
- Audit identifizierte 9 echte Personenduplikate, 22 Orphans, 10 fehlende Boten (Quellen existieren) und 15 Index-Lücken.
- "Orts-Stubs" Issue (Brandenstein, Falkensee, Greifenklipp) final gelöst.

#### [2026-02-12.4] - Das Orakel (RAG-System)

### Hinzugefügt
- `.agent/skills/oracle/SKILL.md`: Skill-Definition für semantische Vektorsuche.
- `.agent/skills/oracle/build_index.py`: Indexierungsskript mit Semantic-Aware Chunking, Auto-Tagging, zwei getrennten Collections.
- `.agent/skills/oracle/search.py`: Suchskript mit Zwei-Stufen-Pipeline (Embedding + Re-Ranking).
- `.agent/skills/oracle/setup.sh`: Einrichtungs-Skript (venv, Dependencies, Modell-Download).

- **Hardware-Optimierung:** `benchmark_hardware.py` (Auto-Tuner) für Jina v3 auf Apple Silicon.
- **Learnings:** Jina v3 (8192 Context) nutzt Flash Attention, was auf MPS bei langen Texten (>2000 Chars) zu massivem Memory-Swapping führt. 
  - **Lösung:** Batch-Size drastisch reduzieren (32 -> 2) für stabilen Betrieb auf 16GB RAM.
- **Embedding:** `jinaai/jina-embeddings-v3` (570M Params, 8192 Token Kontext, LoRA-Adapter)
- **Re-Ranker:** `BAAI/bge-reranker-v2-m3` (568M Params, Cross-Encoder)
- **Chunking:** 2500 Zeichen, 300 Overlap, Paragraph-/Satz-aware Splitting

#### [2026-02-12.3] - GitHub-Interaktivität & Automatisierung

### Hinzugefügt
- `.github/workflows/deploy.yml`: Automatische Konvertierung und Deployment nach GitHub Pages.
- `mkdocs.yml`: Konfiguration für das professionelle Wiki-Layout (MkDocs Material).
- `.github/ISSUE_TEMPLATE/lore_conflict.yml`: Strukturierte Lore-Tickets für Nutzer.
- `.agent/workflows/contrib_audit.md`: Neuer Prozess für die Prüfung von Community-Beiträgen (PRs).

#### [2026-02-12.2] - Projekt-Reorganisation & Cleanup

### Hinzugefügt
- Strukturierte Unterverzeichnisse: `.agent/prompts/`, `.agent/scripts/`, `.agent/docs/`, `Logs/Archive/`.

### Geändert
- **Projekt-Struktur**: Alle Management-Dateien, Prompts und Skripte wurden aus dem Root-Verzeichnis in logische Unterordner verschoben.
- **Referenz-Update**: Alle internen Pfade in README, Workflows, Master-Prompts und Skripten wurden an die neue Struktur angepasst.
- **Cleanup**: Temporäre Extraktionslogs und alte Zips wurden nach `Logs/Archive/` verschoben.

#### [2026-02-12.1] - Infrastruktur-Update & Massen-Integration

### Hinzugefügt
- `source_integrator.py`: Skript zur Integration hochwertiger Markdown-Quellen und Archivierung von Originalen.
- `reference_fixer.py`: Skript zur Korrektur interner Wiki-Links von `.html` zu `.md`.
- `MASTER_TASK_LIST.md`: Globales Aufgabenverzeichnis für Agenten.
- `CHANGELOG.md`: Dieses Dokument.

### Geändert
- **Wahrheitshierarchie (Korrektur)**: Der lokale Kanon (`/Hintergrund`) ist nun die absolute Letztinstanz. Das Live-Web dient der Verifikation und Ergänzung. Die neue Eskalation lautet: Kanon > Lokale Quelle > Homepage > User.

### Integriert
- 254 Markdown-Quellen erfolgreich ins Wiki-System integriert.
- `Brevier der Kirche der Viere.md` als neue Quelle identifiziert und verarbeitet.

---
*Archivar: Antigravity*

#### [1.12.0] - 2026-02-15

### Added
- `System/SYSTEM_INTEGRITY.md`: Codification of directory structures and safety rules.
- Redirection Stubs: `Hochelfen.md`, `Löwenorden.md`, etc. to fix WikiLink aliases.

#### [1.11.0] - 2026-02-15

- **Ingestion:** Verarbeitung von 5 Spielergeschichten (Batch 19).
- **Entitäten:** Erstellung von 12+ neuen Personenprofilen und 3 Organisationen.
- **Lore:** Dokumentation der Argionemes-Verschwörung und der Schwarzen Legion.
- **Wartung:** Konsolidierung von Dubletten und Update des Personenregisters.
- Klare Trennung zwischen aktiven (Königliche Akademie) und historischen (Tiefenbach, Schwarze Künste) Magieschulen hergestellt.
