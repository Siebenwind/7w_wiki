---
name: Test Run Bridge
description: Thin wrapper for standardized interop test suites and dispatch-first defect routing.
---

# Skill: Test Run
> **Wrapper for**: `.agent/workflows/test_run.md` and `.agent/skills/test_waechter/SKILL.md`

Use this skill to execute repeatable clean-state/interoperability test runs.

## Usage

```bash
./7w_wiki.py test --list-suites
./7w_wiki.py test --suite clean-client-state
./7w_wiki.py test --suite takeover-handover
./7w_wiki.py test --suite interop-doc-links
./7w_wiki.py test --suite source-link-hygiene
./7w_wiki.py test --suite bridge-placeholder-guard
./7w_wiki.py test --suite reader-stats-contract
./7w_wiki.py test --suite all
./7w_wiki.py test --suite all --include-rag
./7w_wiki.py test --suite rag-relevance-smoke --timeout 30
```

## Failure Routing (Required)

```bash
./7w_wiki.py test --suite <name> --post-failures --from-agent Test-Waechter --to-agent ALL --priority HIGH
./7w_wiki.py mail claim <MSG-ID> --agent <name>
./7w_wiki.py mail done <MSG-ID> --agent <name> --note "<result>"
```

## Notes
- Runtime authority remains `./7w_wiki.py` only.
- `--suite all` laesst `rag-relevance-smoke` standardmaessig aus (Stabilitaets-Default).
- Fixes are performed after a claimed dispatch message or referenced task.
- For multi-step fixes, send short status heartbeats via dispatch and escalate contradictions as specialist questions.
