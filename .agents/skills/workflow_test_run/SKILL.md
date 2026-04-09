---
name: Workflow Test Run
description: Codex-native regression adapter for interop, adapter-surface, and clean-state verification.
---

# Codex Skill: Workflow Test Run

> **Canonical workflow**: `.agent/workflows/test_run.md`
> **Marker**: Generated Codex adapter skill. Do not edit manually.

This adapter is generated from the canonical catalog. Runtime execution stays on `./7w_wiki.py`; `.agent/` remains the source of truth.

## Primary Runtime Command
`./7w_wiki.py test --suite all`

## Follow-up Commands
- `./7w_wiki.py test --suite adapter-surfaces-contract`
- `./7w_wiki.py pages validate --json`
- `./7w_wiki.py mail inbox --status OPEN`

## Instructions
- Use this adapter for the standard QA loop after interop or infrastructure changes.
- Route failures through Dispatch or task claims before fixing; re-test after each fix.
- Treat adapter-surface, catalog, and delegation-policy checks as first-class interop gates.

## References
- `.agent/workflows/test_run.md`
- `System/Synapse_Board/SY_TESTING.md`
