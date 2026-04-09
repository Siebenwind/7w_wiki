---
description: Standardisierter Testdurchlauf fuer Interop, Takeover/Handover und Clean-Client-State
---

# Workflow: `/test_run` (Test-Waechter Protokoll)

## Interop-Status
- runtime_commands:
  - `7w_wiki.py test --suite clean-client-state`
  - `7w_wiki.py test --suite takeover-handover`
  - `7w_wiki.py test --suite interop-doc-links`
  - `7w_wiki.py test --suite interop-command-registry`
  - `7w_wiki.py test --suite catalog-contract`
  - `7w_wiki.py test --suite adapter-surfaces-contract`
  - `7w_wiki.py test --suite delegation-policy-contract`
  - `7w_wiki.py test --suite repo-hygiene-contract`
  - `7w_wiki.py test --suite manifest-contract`
  - `7w_wiki.py test --suite source-tree-contract`
  - `7w_wiki.py test --suite legacy-doc-contract`
  - `7w_wiki.py test --suite asset-surface-contract`
  - `7w_wiki.py test --suite workflow-matrix-contract`
  - `7w_wiki.py test --suite tool-manifest-contract`
  - `7w_wiki.py test --suite pages-link-contract`
  - `7w_wiki.py test --suite backlog-repair-contract`
  - `7w_wiki.py test --suite source-link-hygiene`
  - `7w_wiki.py test --suite process-dispatch-curiosity`
  - `7w_wiki.py test --suite bridge-placeholder-guard`
  - `7w_wiki.py test --suite reader-stats-contract`
  - `7w_wiki.py test --suite all`
  - `7w_wiki.py test --suite all --include-rag`
  - `7w_wiki.py test --suite rag-relevance-smoke --timeout 30`
  - `7w_wiki.py test --suite all --post-failures --from-agent <name> --to-agent ALL --priority HIGH`
  - `7w_wiki.py pages validate --json [--strict-links]`
  - `7w_wiki.py mail inbox --status OPEN`
  - `7w_wiki.py mail claim <id> --agent <name>`
  - `7w_wiki.py mail done <id> --agent <name> --note "<abschluss>"`
- method_only:
  - `/test_run`
- method_hints_non_runtime:
  - Optional: Defect-Task in `task.md` referenzieren, falls kein Dispatch-MSG verwendet wird.
- catalog_id: `workflow.test_run`
- primary_command: `7w_wiki.py test --suite all`
- followup_commands:
  - `7w_wiki.py test --suite adapter-surfaces-contract`
  - `7w_wiki.py pages validate --json`
  - `7w_wiki.py mail inbox --status OPEN`
- adapter_targets:
  - `codex:workflow_test_run`
  - `mcp:prompt/test_run`
- deprecated_aliases:

## 1. Agentenmentalitaet (verbindlich)

### Test-Waechter (Tester)
- Arbeitet skeptisch und reproduzierbar.
- Fuehrt keine stillen Fixes aus.
- Bei FAIL: erstellt zuerst Kommunikationsartefakt (Dispatch oder Task), dann uebergibt.

### Fix-Agent
- Nimmt nur geclaimte Defects an (`mail claim` oder referenzierter Task).
- Liefert Fix + Re-Test + Changelog mit Verweis auf Message-ID/Task-ID.

### Koordinator
- Priorisiert Defects (P1/P2/P3), verteilt Claims, schliesst `DONE`.

## 2. Standarddurchlauf

// turbo
1. `./7w_wiki.py test --suite clean-client-state`
2. `./7w_wiki.py test --suite takeover-handover`
3. `./7w_wiki.py test --suite interop-doc-links` (lokale Markdown-Links)
4. `./7w_wiki.py test --suite interop-command-registry` (Live-CLI gegen Governance-Inventare)
5. `./7w_wiki.py test --suite catalog-contract` (kanonischer Katalog + Schema + Pflichtsektionen)
6. `./7w_wiki.py test --suite adapter-surfaces-contract` (Codex-Adapter, MCP-nahe Artefakte, keine Thin-Wrapper)
7. `./7w_wiki.py test --suite delegation-policy-contract` (Delegationsrichtlinie + Thread-Limit + Profil-Mapping)
8. `./7w_wiki.py test --suite repo-hygiene-contract` (Hot/Cold/Runtime/Build-Klassifikation und Schutzregeln)
9. `./7w_wiki.py test --suite manifest-contract` (generiertes `lore_manifest.json` gegen Katalog und CLI)
10. `./7w_wiki.py test --suite source-tree-contract` (aktiver Tree-Kanon fuer `docs/Siebenwind_Wiki/`)
11. `./7w_wiki.py test --suite legacy-doc-contract` (keine Pflicht-Links mehr in `_archive` oder alte Singleton-Standards)
12. `./7w_wiki.py test --suite asset-surface-contract` (aktive Docs/Skills zeigen nur auf kanonische Asset-Surfaces)
13. `./7w_wiki.py test --suite workflow-matrix-contract` (generierte Matrix + Workflow-Referenzen)
14. `./7w_wiki.py test --suite tool-manifest-contract` (typed tools.json + Alias-Kompatibilitaet)
15. `./7w_wiki.py test --suite pages-link-contract` (Pages snapshot + advisor freshness + policy file)
16. `./7w_wiki.py test --suite source-link-hygiene` (MkDocs-Strict-Risiken in Quellenlinks)
17. `./7w_wiki.py test --suite backlog-repair-contract` (Backlog-Board + Lane-1-Repair-Surface)
18. `./7w_wiki.py test --suite process-dispatch-curiosity` (Workflow-/Persona-Prozesslogik)
19. `./7w_wiki.py test --suite bridge-placeholder-guard` (verhindert Rueckfall in Stub-/Bridge-Policy-Fehler)
20. `./7w_wiki.py test --suite reader-stats-contract` (Reader-Stats-Contract + Snapshot-Schnittstelle)
21. Optional Vollabgleich: `./7w_wiki.py test --suite all` (ohne RAG-Smoke; stabiler Standardlauf)

## 3. Failure-Protokoll

Bei FAIL gilt:

1. Dispatch erstellen (oder Task referenzieren):
   - Empfohlen: `./7w_wiki.py test --suite <name> --post-failures --from-agent <name> --to-agent ALL --priority HIGH`
2. Fix-Agent uebernimmt:
   - `./7w_wiki.py mail claim <MSG-ID> --agent <name>`
3. Nach Fix:
   - Re-Test der betroffenen Suite
   - Danach `./7w_wiki.py test --suite all` (RAG nur bei Bedarf via `--include-rag`)
   - Fuer schnelle Technik-/QA-Vorchecks optional: `./7w_wiki.py pages validate --json --fast`
   - Fuer harte Site-Gates optional: `./7w_wiki.py pages validate --json --strict-links`
4. Abschluss:
   - `./7w_wiki.py mail done <MSG-ID> --agent <name> --note "<kurzabschluss>"`
   - Changelog-Eintrag mit Verweis auf Message-ID/Task-ID

## 4. Definition of Done

- Alle relevanten Suiten PASS.
- Jede Fehlerserie ist ueber Dispatch/Task nachverfolgbar.
- Re-Test wurde nach jedem Fix protokolliert.
