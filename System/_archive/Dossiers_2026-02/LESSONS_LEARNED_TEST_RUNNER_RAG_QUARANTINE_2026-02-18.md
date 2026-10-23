---
uuid: b76106d7-e831-4349-bbc2-70572f98919e
status: ACTIVE
created_at: 2026-02-18T01:07:00Z
epistemic: "#meta"
---

# Lessons Learned: Test-Runner RAG Quarantine

## Kontext

- Symptom: `./7w_wiki.py test --suite rag-relevance-smoke` kann in der Codex-App den Lauf blockieren oder gefuehlt "haengen".
- Folge: `./7w_wiki.py test --suite all` wirkte unzuverlaessig, obwohl andere Suiten stabil waren.

## Entscheidung

1. `rag-relevance-smoke` ist **nicht mehr Teil von `--suite all`**.
2. RAG-Diagnose nur noch explizit:
   - `./7w_wiki.py test --suite rag-relevance-smoke --timeout 30`
   - oder `./7w_wiki.py test --suite all --include-rag`
3. Test-Runner gibt pro Case Live-Fortschritt aus (`case x/y`, Status, Grund).

## Warum das robust ist

- Standard-Interop bleibt schnell und reproduzierbar.
- Instabile Oracle-Pfade sind isoliert und blockieren den Baseline-Gate nicht.
- Agenten sehen sofort, welche Case gerade laeuft und wo es haengt.

## Agenten-Regel

- **Default fuer Abschluss-Checks**: `./7w_wiki.py test --suite all`
- **Nur bei Oracle-Problemen oder gezielter Diagnose**: `--include-rag` oder direkte RAG-Suite.
- Bei RAG-FAIL zuerst Defect-Routing (`--post-failures`), dann Fix.
