# Session Memory: Drift Prevention

- Date: 2026-03-26
- Focus: Drift-Praevention fuer Wiki-Inhalte, ein gemeinsamer Content-Contract, kanonische Provenance-Inventare und governance-seitige Durchsetzung

## Context
- Das sichtbare Layoutproblem war ein Symptom fuer Inhaltsdrift: aufeinanderfolgende `**Label:**`-Zeilen nach dem H1 kollabierten im Rendern zu einem Absatz.
- Der technische Bestand war gespalten: reale Inhalte lagen unter `docs/Siebenwind_Wiki`, waehrend mehrere Runtime-Pfade noch `Siebenwind_Wiki` als Default behandelten.
- Legacy-Felder wie `layout: wiki_page|post` wurden von aktiven Schreibpfaden weiter emittiert, obwohl der MkDocs-Stack sie nicht mehr als Rendervertrag nutzt.
- Fuer die Wissensordnung wurde die epistemische Rangfolge festgeschrieben: Homepage > Quellen > Wiki Pages. `docs/Siebenwind_Wiki/` ist der technische Edit- und Publish-Baum, nicht die hoechste Wahrheitsinstanz.

## What Changed
- Fuehrte `.agent/scripts/content_contract.py` als gemeinsame Vertrags- und Inventarschicht ein.
- Stellte aktive Runtime-Defaults auf `docs/Siebenwind_Wiki` um und behandelte `Siebenwind_Wiki` nur noch als Legacy-/Artefaktpfad mit Split-Brain-Pruefung.
- Ersetzte den Sanitizer durch einen Content-Normalizer, der Frontmatter bereinigt, `layout` entfernt, Inline-Metadaten in einen kanonischen `!!! info "Metadaten"`-Block ueberfuehrt und Stubs auf ein Lifecycle-Template normalisiert.
- Vereinheitlichte `repair`, `index-pages`, `stats`, `pages`, `audit`, `advisor`, Oracle-Index, Watcher, Version-Manager und MCP-Fallbacks auf denselben technischen Wiki-Baum und denselben Vertrag.
- Fuegte ein generiertes Inventar unter `.agent/data/wiki_inventory.json` samt Historie unter `.agent/data/wiki_inventory_history/` hinzu.
- Erweiterte Audit- und Pages-Berichte um `render_hygiene`, `contract_violations`, `stub_inventory`, `bridge_inventory`, `split_brain` und `traceability_gaps`.
- Ergaenzte neue Testsuiten fuer `content-contract`, `split-brain-guard` und `render-hygiene` und aktualisierte bestehende Vertrags- und Stats-Suiten auf die neue Struktur.
- Aktualisierte Governance und Workflows in `AGENTS.md`, `System/AGENT_OPERATIONS_HANDBOOK.md`, `System/Synapse_Board/SY_INTEROP.md`, `System/Synapse_Board/SY_TESTING.md`, `System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md`, `.agent/workflows/start.md`, `.agent/workflows/tech_master.md`, `.agent/workflows/qa_master.md`, `.agent/workflows/handover.md`, `.agent/workflows/meta_master.md` und `MASTER_TASK_LIST.md`.
- Fuehrte `./7w_wiki.py tech --sync-interop` aus, damit Registry, Interop-Doku und Tool-Metadaten wieder mit dem neuen Vertrag uebereinstimmen.
- Fuehrte einen Bulk-Normalisierungslauf ueber `docs/Siebenwind_Wiki` aus; repraesentative Problemseiten wie `Lucius_Gropp.md` und `Siebenwind_Bote_179.md` rendern nun mit kanonischem Metadatenblock statt kollabierter Label-Zeilen.

## Current Signal
- `sanitize` auf repraesentativen Problemseiten: gruen
- `pages validate --json --skip-audit`: `WARN`, aber `drift_status: PASS`
- Drift-Pruefung: keine `legacy_only_files`, keine `content_mismatches`; `docs_only_files` sind als technischer Kanon informational
- Audit-Restbestand: `177` Issues, davon `88` historische Bridge-Seiten ohne Lifecycle-Metadaten und `20` sonstige Wiki-Integritaetsaltlasten
- Traceability: Inventar und Snapshot-Historie werden deterministisch erzeugt; keine aktuellen `traceability_gaps`

## Files of Note
- `.agent/scripts/content_contract.py`
- `.agent/scripts/wiki_sanitizer.py`
- `.agent/scripts/repair.py`
- `.agent/scripts/generate_wiki_indices.py`
- `.agent/scripts/generate_wiki_stats.py`
- `.agent/scripts/pages_integrity.py`
- `.agent/scripts/pages_tool.py`
- `.agent/scripts/register_check.py`
- `.agent/scripts/advisor.py`
- `.agent/skills/oracle/build_index.py`
- `.agent/scripts/watcher.py`
- `.agent/scripts/version_manager.py`
- `System/MCP/server.py`
- `lore_manifest.json`
- `.agent/tests/suites/content-contract.json`
- `.agent/tests/suites/split-brain-guard.json`
- `.agent/tests/suites/render-hygiene.json`
- `.agent/data/wiki_inventory.json`

## Verification
- `./7w_wiki.py sanitize docs/Siebenwind_Wiki --auto`
- `./7w_wiki.py sanitize docs/Siebenwind_Wiki/07_Persoenlichkeiten/Lucius_Gropp.md --json`
- `./7w_wiki.py sanitize docs/Siebenwind_Wiki/04_Chronik/Siebenwind_Bote_179.md --json`
- `./7w_wiki.py stats --json`
- `./7w_wiki.py pages validate --json --skip-audit`
- `./7w_wiki.py audit --json`
- `./7w_wiki.py test --suite clean-client-state`
- `./7w_wiki.py test --suite interop-command-registry`
- `./7w_wiki.py test --suite codex-workflow-bridges`
- `./7w_wiki.py test --suite workflow-matrix-contract`
- `./7w_wiki.py test --suite tool-manifest-contract`
- `./7w_wiki.py test --suite pages-link-contract`
- `./7w_wiki.py test --suite bridge-placeholder-guard`
- `./7w_wiki.py test --suite reader-stats-contract`
- `./7w_wiki.py test --suite content-contract`
- `./7w_wiki.py test --suite split-brain-guard`
- `./7w_wiki.py test --suite render-hygiene`
- `./7w_wiki.py test --suite takeover-handover`
- `./7w_wiki.py tech --sync-interop`

## Notes / Risks
- Die Drift-Praeventionsschicht ist implementiert, aber der historische Bridge-Bestand bleibt operativ offen und sollte in einer Folgearbeit entweder sauber mit Lifecycle-Metadaten versehen oder auf kanonische Ziele reduziert werden.
- `audit --json` meldet weiterhin Lesefehler fuer fehlende `Quellen/Zeitung 7w Bote/...`-Dateien; das sind Altlasten im Quellen-/Linkbestand, nicht ein Defekt des neuen Contracts.
- `pages validate` bleibt `WARN`, weil weiterhin eine grosse Link-/Navigation-Altlast auf dem publizierten Inhaltsbestand liegt.
- Der Bulk-Sanitize hat einen sehr grossen Diff erzeugt, weil Legacy-Layouts entfernt und Metadatenbloeke normiert wurden.
