# Session Memory: Backlog Lane1

- Date: 2026-03-27
- Focus: Konservativer Hybrid-Abbau des Pages-/Bridge-Backlogs, zuerst ueber maschinenlesbare Cluster-Artefakte und eine konservative Lane-1-Welle

## Context
- Ausgangslage vor dieser Session:
  - `pages_health.unresolved_total = 774`
  - `pages_health.unallowlisted_total = 772`
  - `contract_violations = 75`
  - `bridge_inventory.invalid = 88`
- Ziel war nicht ein weiterer ungezielter Link-Fix-Lauf, sondern ein clusterbasierter Arbeitsmodus:
  - Board fuer mechanische vs. review-pflichtige vs. eskalationspflichtige Cluster
  - konservative Lane-1-Welle nur fuer eindeutige, rein mechanische Korrekturen
  - Bridge-Backlog separat klassifizieren statt pauschal als ein Block zu behandeln

## What Changed
- Erweiterte `repair` um zwei neue Runtime-Modi:
  - `./7w_wiki.py repair --backlog-board --json`
  - `./7w_wiki.py repair --apply-lane1 [--auto] [--dry-run] [--json]`
- Neue maschinenlesbare Artefakte:
  - `.agent/data/backlog_cluster_board.json`
  - `.agent/data/backlog_escalations.json`
- `content_contract.py` normalisiert jetzt zusaetzlich:
  - `category: [[...]]` im Frontmatter auf kanonischen Klartext per Ordnerkategorie
  - kaputte `quelle:`-Wikilinks robuster zu Plaintext
- `repair.py` fuehrt Lane 1 konservativ aus:
  - Alias-/Umlaut-/Syntaxdrift nur bei genau einem kanonischen Zielkandidaten und `normalize_key(target) == normalize_key(candidate)`
  - Frontmatter-`category` mit bare Wikilinks wird in Klartext gehoben
  - `quelle:`-Felder werden bei eindeutigem Quellenlookup auf echte relative Pfade gesetzt
- Dokumentation und Governance aktualisiert:
  - `CHANGELOG.md`
  - `MASTER_TASK_LIST.md`
  - `.agent/workflows/tech_master.md`
  - `.agent/workflows/test_run.md`
- Neue Vertrags-Suite:
  - `.agent/tests/suites/backlog-repair-contract.json`

## Cluster Board Snapshot
- Lane 1:
  - `lane1_target_normalization = 18` Zielcluster
  - `frontmatter_category_wikilinks = 717` Dateien
  - `quelle_frontmatter_lookup = 353` Kandidaten, davon `121` eindeutige Lookup-Rewrites
- Bridges:
  - `bridge_single_target_review = 84`
  - `bridge_escalation = 4`
  - `backlog_escalations.json` enthaelt insgesamt `13` Eskalationsfaelle (Bridge-Mehrdeutigkeiten plus nicht-mechanische Pages-Targets)

## Applied Lane-1 Result
- `./7w_wiki.py repair --apply-lane1 --auto --json` wurde real ausgefuehrt.
- Ergebnis:
  - `changed_files_total = 855` Schreiboperationen
  - `planned_files_total = 763` einzigartige betroffene Dateien
  - Alias-/Syntaxcluster schrieb in `17` Dateien
  - Frontmatter-`category`-Normalisierung schrieb breit ueber den Wiki-Bestand
  - `quelle:`-Lookup hob eindeutige Quellenpfade breit ueber Magie-, Gesellschafts-, Bibliotheks- und Persoenlichkeitsseiten

## Verification
- `python3 -m py_compile 7w_wiki.py .agent/scripts/repair.py .agent/scripts/content_contract.py`
- `./7w_wiki.py test --suite backlog-repair-contract`
- `./7w_wiki.py test --suite interop-doc-links`
- `./7w_wiki.py repair --backlog-board --json`
- `./7w_wiki.py repair --apply-lane1 --dry-run --auto --json`
- `./7w_wiki.py repair --apply-lane1 --auto --json`
- `./7w_wiki.py audit --pages --json`
- `./7w_wiki.py pages validate --json --strict-links --skip-audit`
- `./7w_wiki.py advisor --json`

## Measured Delta
- Nach `audit --pages --json`:
  - `issues_found = 931` (vorher `1037`)
  - `site_integrity.issues = 754` (vorher `785`)
  - `contract_violations = 0` (vorher `75`)
  - `bridge_inventory.invalid = 88` (unveraendert)
- Nach hartem Gate `./7w_wiki.py pages validate --json --strict-links --skip-audit`:
  - `pages_health.unresolved_total = 745` (vorher `774`)
  - `pages_health.unallowlisted_total = 743` (vorher `772`)
  - `pages_health.last_validated_at = 2026-03-27T18:03:10Z`
  - `pages_health.status = FAIL` wegen verbleibender `strict-links`-Defekte
  - `build.exit_code = 0`
  - `build.warning_count = 756`
  - `other_warnings = 11`
  - `validation_timing_ms.total ~= 122935`

## Remaining High-Value Follow-Up
- **Semantisch schwächere Restcluster**:
  - `Historie`
  - `Magie`
  - `Magie_Elementarmagie`
  - `Gottheiten`
  - `Die_Sammler`
  - `Magische_Rituale`
  - verbleibende `Dämonen`-Treffer
- **Bridge Track**:
  - zuerst die `84` `bridge_single_target_review`-Faelle gegen semantische Verluste pruefen
  - nur die `4` `bridge_escalation`-Faelle separat behandeln
- **Quellenpfade / Boten**:
  - weiterhin bekannte Fehlpfade fuer Boten `176`, `178`-`182`, `185`
  - Ursache bleibt die gemischte Leerzeichen-/Unterstrich-Namenskonvention im Quellenbaum
  - naechster Technikschritt sollte ein strikter lookup-basierter Normalizer mit realem Dateibaum-Match sein
- **Relative Indexwarnungen ausserhalb der Roamlink-Ziele**:
  - verbleiben in `00_Fundament/index.md`, `01_Pantheon/*.md`, `03_Wissen/index.md`

## Notes / Risks
- Die Fast-Checks vor dem Voll-Validate hingen noch am alten Snapshot; der harte Gate-Lauf am Ende der Session hat den Snapshot auf den neuen Stand gebracht.
- `repair --apply-lane1` ist bewusst konservativ. Mehrdeutige oder semantisch nicht-identische Zielkandidaten bleiben im Eskalationsartefakt und werden nicht still umgeschrieben.
- Die Bridge-Klassifikation ist jetzt brauchbar operationalisiert (`84/4`), aber die eigentliche Bridge-Entscheidung wurde in dieser Session noch nicht ausgefuehrt.
