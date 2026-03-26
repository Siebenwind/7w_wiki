# Session Memory: Docs And Pages Cache

- Date: 2026-03-26
- Focus: Dokumentations-Konsolidierung fuer Drift-/Pages-Regeln sowie sichere Analyse-Caches fuer `pages validate`

## Context
- Die Drift-Praeventionslogik war technisch eingefuehrt, aber die dokumentarische Regelbasis blieb auf mehrere Dateien verteilt.
- `tech --sync-docs` synchronisierte bisher nur Kommandolisten, nicht den eigentlichen Drift-/Pages-Referenzanker.
- `pages validate` und angrenzende Checks machten mehrfach Vollgaenge ueber denselben Bestand; besonders problematisch war die Kopplung von kleinen Contract-Checks an globale Inventory-Writes.

## What Changed
- Fuehrte den kanonischen Drift-/Pages-Vertrag in `System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md` ein und registrierte ihn in `System/COORDINATION_HUB.md`.
- Verdichtete die wichtigsten Governance-/Workflow-Texte auf kurze Referenzen auf den neuen Vertrag statt mehrfacher Regelwiederholung:
  - `AGENTS.md`
  - `System/AGENT_OPERATIONS_HANDBOOK.md`
  - `System/Synapse_Board/SY_INTEROP.md`
  - `System/Synapse_Board/SY_TESTING.md`
  - `System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md`
  - `.agent/workflows/start.md`
  - `.agent/workflows/tech_master.md`
  - `.agent/workflows/qa_master.md`
  - `.agent/workflows/handover.md`
  - `MASTER_TASK_LIST.md`
- Bereinigte Doku-Inkonsistenzen:
  - alte Handover-Verweise auf `.agent/skills/wiki_schmied/scripts/` entfernt
  - `pages validate --strict` vs. `--json --strict-links` semantisch klargestellt
  - Drift-Governance-Alignment in `MASTER_TASK_LIST.md` auf erledigt gezogen
- Erweiterte `.agent/scripts/sync_runtime_docs.py`:
  - synchronisiert weiter die Command-Listen
  - kann jetzt zusaetzlich standardisierte Drift-/Pages-Referenzblöcke angleichen
  - wurde ueber `./7w_wiki.py tech --sync-interop` verifiziert
- Entkoppelte Contract-Scan und globales Inventar in `.agent/scripts/content_contract.py`:
  - kleine/scoped `sanitize --json`-Checks schreiben kein globales Wiki-Inventar mehr
  - Vollbaum-Contract-Scans und Inventare sind cachebar
  - neue Cache-Artefakte leben unter `.agent/data/cache/`
- Fuehrte sichere Analyse-Caches fuer Pages ein:
  - `docs_link_index.json`
  - `canonical_name_index.json`
  - `tree_drift.json`
  - `content_contract_scan.json`
  - `wiki_inventory.json` (Cache-Metadaten neben dem eigentlichen Inventar)
- Reduzierte Doppelarbeit in `.agent/scripts/pages_tool.py`:
  - `pages validate` ruft innerhalb des Validate-Loops nicht mehr indirekt ein zweites volles Audit ueber `split-brain-guard` auf
  - bei `--skip-audit` wird `drift_health` aus dem Contract-Check statt aus Audit-Daten gespeist
- Erweiterte Tests fuer die neue Cache-/Traceability-Schicht:
  - `.agent/tests/suites/content-contract.json`
  - `.agent/tests/suites/pages-link-contract.json`
  - `.agent/tests/suites/split-brain-guard.json`

## Current Signal
- `docs/Siebenwind_Wiki` bleibt der technische Edit-/Publishing-Baum.
- Epistemische Praezedenz ist in der Doku zentralisiert: `Homepage > Quellen > Wiki Pages`.
- `pages validate --json --skip-audit` liefert jetzt Cache-Hinweise unter `pages_health.analysis_cache`.
- `audit --pages --json` liefert wieder gueltiges JSON und enthaelt Traceability-/Cache-Artefakte statt am Inventarpfad zu sterben.
- Die schwere Pages-/Link-Altlast bleibt bestehen: `pages_health.status = WARN`, `unallowlisted_total = 811`, `audit --pages --json` meldet weiterhin die bestehenden historischen Site-/Bridge-Defekte.

## Verification
- `python3 -m py_compile .agent/scripts/content_contract.py .agent/scripts/pages_integrity.py .agent/scripts/pages_tool.py .agent/scripts/sync_runtime_docs.py`
- `./7w_wiki.py test --suite content-contract`
- `./7w_wiki.py test --suite split-brain-guard`
- `./7w_wiki.py pages validate --json --skip-audit`
- `./7w_wiki.py audit --pages --json`
- `./7w_wiki.py test --suite takeover-handover`
- `./7w_wiki.py test --suite interop-doc-links`
- `./7w_wiki.py test --suite workflow-matrix-contract`
- `./7w_wiki.py test --suite tool-manifest-contract`
- `./7w_wiki.py test --suite codex-workflow-bridges`
- `./7w_wiki.py advisor --json`
- `./7w_wiki.py tech --sync-interop`

## Notes / Risks
- `pages-link-contract` war im aktuellen Shell-Lauf sehr langsam, obwohl die zugrundeliegenden Vertragsdaten (`pages validate --json --skip-audit`, `audit --pages --json`, Snapshot- und Cache-Dateien) korrekt vorlagen. Falls das reproduzierbar bleibt, sollte der Test-Runner- bzw. Timeout-/Output-Pfad separat untersucht werden.
- Die neue Cache-Schicht beschleunigt Wiederholungsarbeit, ersetzt aber bewusst keinen echten MkDocs-Build fuer harte Gates.
- Historische Pages-/Bridge-/Linkdefekte bleiben inhaltlicher Folgeaufwand und sind nicht Teil dieses Infrastrukturumbaus.
