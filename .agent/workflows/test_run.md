---
description: Standardisierter Testdurchlauf fuer Interop, Takeover/Handover und Clean-Client-State
---

# Workflow: `/test_run` (Test-Waechter Protokoll)

## Interop-Status
- runtime_commands:
  - `7w_wiki.py test --suite clean-client-state`
  - `7w_wiki.py test --suite takeover-handover`
  - `7w_wiki.py test --suite interop-doc-links`
  - `7w_wiki.py test --suite rag-relevance-smoke`
  - `7w_wiki.py test --suite all`
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
4. `./7w_wiki.py test --suite rag-relevance-smoke` (RAG-Status + Relevanz-Smoke)
5. Optional Vollabgleich: `./7w_wiki.py test --suite all`

## 3. Failure-Protokoll

Bei FAIL gilt:

1. Dispatch erstellen (oder Task referenzieren):
   - Empfohlen: `./7w_wiki.py test --suite <name> --post-failures --from-agent <name> --to-agent ALL --priority HIGH`
2. Fix-Agent uebernimmt:
   - `./7w_wiki.py mail claim <MSG-ID> --agent <name>`
3. Nach Fix:
   - Re-Test der betroffenen Suite
   - Danach `./7w_wiki.py test --suite all`
4. Abschluss:
   - `./7w_wiki.py mail done <MSG-ID> --agent <name> --note "<kurzabschluss>"`
   - Changelog-Eintrag mit Verweis auf Message-ID/Task-ID

## 4. Definition of Done

- Alle relevanten Suiten PASS.
- Jede Fehlerserie ist ueber Dispatch/Task nachverfolgbar.
- Re-Test wurde nach jedem Fix protokolliert.
