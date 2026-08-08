---
name: Test Waechter
description: Standardized suite execution, defect routing via Dispatch/Task, and re-test discipline.
---

# Skill: Test-Waechter

Dieser Skill standardisiert den Testdurchlauf fuer Interop, Takeover/Handover und Clean-Client-State.

## Runtime

```bash
./7w_wiki.py test --list-suites
./7w_wiki.py test --suite clean-client-state
./7w_wiki.py test --suite takeover-handover
./7w_wiki.py test --suite historian-closeout-contract
./7w_wiki.py test --suite bridge-placeholder-guard
./7w_wiki.py test --suite reader-stats-contract
./7w_wiki.py test --suite all
./7w_wiki.py test --suite all --include-rag
./7w_wiki.py test --suite rag-relevance-smoke --timeout 30
```

Hinweis: `--suite all` laesst `rag-relevance-smoke` standardmaessig aus (Stabilitaets-Default).

## Defect-Routing (Pflicht)

Bei FAIL vor jedem Fix:

```bash
./7w_wiki.py test --suite <name> --post-failures --from-agent Test-Waechter --to-agent ALL --priority HIGH
```

Fix-Agenten arbeiten nur auf geclaimten Defects (`mail claim`) und schliessen nach Re-Test (`mail done`).
