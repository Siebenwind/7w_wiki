---
uuid: 9e6a6a7c-4ef6-4f73-96d7-967f21bf90e8
status: ACTIVE
owners:
  - Koordinator
  - Test-Waechter
epistemic: "#meta"
---

# SY_TESTING

Verbindlicher Standard fuer reproduzierbare Testdurchlaeufe, Defect-Kommunikation und Re-Tests.

## Ziel

1. Testlaeufe standardisieren (`clean-client-state`, `takeover-handover`, `interop-doc-links`, `interop-command-registry`, `workflow-matrix-contract`, `tool-manifest-contract`, `pages-contract-mode-contract`, `pages-full-smoke`, `root-tree-retirement-contract`, `styling-surface-contract`, `source-link-hygiene`, `process-dispatch-curiosity`, `bridge-placeholder-guard`, `reader-stats-contract`, `all` + optional `rag-relevance-smoke`).
2. Defects ohne stille Fixes behandeln.
3. Fixes nur auf Basis kommunizierter Auftraege umsetzen.
4. Technischen Drift frueh sichtbar machen (`content-contract`, `split-brain-guard`, `render-hygiene`) und epistemischen Drift getrennt behandeln. Der kanonische Volltext steht in [SY_DRIFT_PAGES_CONTRACT.md](SY_DRIFT_PAGES_CONTRACT.md).

## Runtime-Einstieg

- `./7w_wiki.py test --list-suites`
- `./7w_wiki.py test --suite clean-client-state`
- `./7w_wiki.py test --suite takeover-handover`
- `./7w_wiki.py test --suite interop-doc-links`
- `./7w_wiki.py test --suite interop-command-registry`
- `./7w_wiki.py test --suite workflow-matrix-contract`
- `./7w_wiki.py test --suite tool-manifest-contract`
- `./7w_wiki.py test --suite pages-contract-mode-contract`
- `./7w_wiki.py test --suite root-tree-retirement-contract`
- `./7w_wiki.py test --suite styling-surface-contract`
- `./7w_wiki.py test --suite source-link-hygiene`
- `./7w_wiki.py test --suite process-dispatch-curiosity`
- `./7w_wiki.py test --suite bridge-placeholder-guard`
- `./7w_wiki.py test --suite reader-stats-contract`
- `./7w_wiki.py test --suite content-contract`
- `./7w_wiki.py test --suite split-brain-guard`
- `./7w_wiki.py test --suite render-hygiene`
- `./7w_wiki.py test --suite all`
- `./7w_wiki.py test --suite all --include-rag`
- `./7w_wiki.py test --suite rag-relevance-smoke --timeout 30`
- `./7w_wiki.py test --suite <name> --post-failures --from-agent <name> --to-agent ALL --priority HIGH`

Suite-Definitionen liegen in:
- `.agent/tests/suites/*.json`

Testberichte liegen in:
- `Logs/Archive/TEST_<suite>_<timestamp>.md`

Stabilitaetsregel:
- `--suite all` laesst `rag-relevance-smoke` standardmaessig aus.
- RAG-Smoke nur als explizite Diagnose per `--include-rag` oder direktem Suite-Aufruf.
- Pages-/Link-Suiten decken technischen Publishing-Drift ab; sie belegen keine epistemische Korrektheit gegen Homepage oder Quellen.
- Fuer Pages-/Navigationsaenderungen zusaetzlich `./7w_wiki.py test --suite pages-full-smoke` oder den Operatorpfad `./7w_wiki.py pages validate --json` laufen lassen.

RAG-Diagnose- und Benchmarkdoku:
- `docs/Archiv/RAG_DIAGNOSE_2026-02-16.md`
- `System/Archivregister/ARCHIVREGISTER.md` (wird durch `./7w_wiki.py index --status` aktualisiert)
- `docs/Archiv/LESSONS_LEARNED_TEST_RUNNER_RAG_QUARANTINE_2026-02-18.md`

## Agentenmentalitaet

### Tester (Test-Waechter)
- Skeptisch, reproduzierbar, read-first.
- Keine stillen Produktivfixes.
- Bei FAIL: zuerst Defect kommunizieren (Dispatch oder Task).

### Fix-Agent
- Arbeitet nur auf geclaimten Defects.
- Jeder Fix muss Message-ID/Task-ID referenzieren.
- Re-Test ist Pflicht vor Abschluss.

### Koordinator
- Priorisiert Defects.
- Steuert Claiming und Abschluss.
- Prueft Changelog-/Report-Referenzen.

## Kommunikationspflicht (hart)

Ein Fix ist nur zulaessig, wenn mindestens eines vorliegt:
1. Dispatch-Message (`mail post`, danach `claim`), oder
2. referenzierter Task-Eintrag (`task.md`/aehnlich).

## Defect-Lebenszyklus

1. Test ausfuehren.
2. Bei FAIL:
   - Defect posten (`--post-failures`) oder Task erstellen.
   - Defect-Typ markieren: `technical drift` oder `epistemic drift`.
3. Fix-Agent uebernimmt (`mail claim` oder Task-Referenz).
4. Fix umsetzen.
   - `technical drift`: Layout, Frontmatter, Split-Brain, Generatoren, Pages/Links.
   - `epistemic drift`: Homepage/Quellen gegen Wiki-Pages abgleichen; nicht nur Seiten reparieren. Fuer die Praxis gilt [SY_DRIFT_PAGES_CONTRACT.md](SY_DRIFT_PAGES_CONTRACT.md).
5. Re-Test:
   - erst betroffene Suite
   - danach `--suite all`
6. Abschluss:
   - `mail done` (oder Task als done markieren)
   - Changelog-Eintrag mit Defect-Referenz

## Verweise

- `.agent/workflows/test_run.md`
- `.agent/scripts/test_runner.py`
- `System/Synapse_Board/SY_DISPATCH.md`
- `System/Synapse_Board/SY_INTEROP.md`
