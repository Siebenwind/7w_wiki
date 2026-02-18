---
description: Standardisierter Testdurchlauf fuer Interop, Takeover/Handover und Clean-Client-State
---

# Workflow: `/test_run` (Test-Waechter Protokoll)

## Interop-Status
- runtime_commands:
  - `7w_wiki.py test --suite clean-client-state`
  - `7w_wiki.py test --suite takeover-handover`
  - `7w_wiki.py test --suite interop-doc-links`
  - `7w_wiki.py test --suite source-link-hygiene`
  - `7w_wiki.py test --suite process-dispatch-curiosity`
  - `7w_wiki.py test --suite bridge-placeholder-guard`
  - `7w_wiki.py test --suite reader-stats-contract`
  - `7w_wiki.py test --suite all`
  - `7w_wiki.py test --suite all --include-rag`
  - `7w_wiki.py test --suite rag-relevance-smoke --timeout 30`
  - `7w_wiki.py test --suite all --post-failures --from-agent <name> --to-agent ALL --priority HIGH`
  - `7w_wiki.py mail inbox --status OPEN`
  - `7w_wiki.py mail claim <id> --agent <name>`
  - `7w_wiki.py mail done <id> --agent <name> --note "<abschluss>"`
- method_only:
  - `/test_run`
- method_hints_non_runtime:
  - Optional: Defect-Task in `task.md` referenzieren, falls kein Dispatch-MSG verwendet wird.

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

1. `./7w_wiki.py test --suite clean-client-state`
2. `./7w_wiki.py test --suite takeover-handover`
3. `./7w_wiki.py test --suite interop-doc-links` (lokale Markdown-Links)
4. `./7w_wiki.py test --suite source-link-hygiene` (MkDocs-Strict-Risiken in Quellenlinks)
5. `./7w_wiki.py test --suite process-dispatch-curiosity` (Workflow-/Persona-Prozesslogik)
6. `./7w_wiki.py test --suite bridge-placeholder-guard` (verhindert Rueckfall in Stub-/Bridge-Policy-Fehler)
7. `./7w_wiki.py test --suite reader-stats-contract` (Reader-Stats-Contract + Snapshot-Schnittstelle)
8. Optional Vollabgleich: `./7w_wiki.py test --suite all` (ohne RAG-Smoke; stabiler Standardlauf)
9. Optional Oracle-Diagnose: `./7w_wiki.py test --suite rag-relevance-smoke --timeout 30` oder `./7w_wiki.py test --suite all --include-rag`

## 3. Failure-Protokoll

Bei FAIL gilt:

1. Dispatch erstellen (oder Task referenzieren):
   - Empfohlen: `./7w_wiki.py test --suite <name> --post-failures --from-agent <name> --to-agent ALL --priority HIGH`
2. Fix-Agent uebernimmt:
   - `./7w_wiki.py mail claim <MSG-ID> --agent <name>`
3. Nach Fix:
   - Re-Test der betroffenen Suite
   - Danach `./7w_wiki.py test --suite all` (RAG nur bei Bedarf via `--include-rag`)
4. Abschluss:
   - `./7w_wiki.py mail done <MSG-ID> --agent <name> --note "<kurzabschluss>"`
   - Changelog-Eintrag mit Verweis auf Message-ID/Task-ID

## 4. Definition of Done

- Alle relevanten Suiten PASS.
- Jede Fehlerserie ist ueber Dispatch/Task nachverfolgbar.
- Re-Test wurde nach jedem Fix protokolliert.
