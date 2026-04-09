---
name: Session Start
description: Codex-native onboarding adapter for the standard session kickoff loop.
---

# Codex Skill: Session Start

> **Canonical workflow**: `.agent/workflows/start.md`
> **Marker**: Generated Codex adapter skill. Do not edit manually.

This adapter is generated from the canonical catalog. Runtime execution stays on `./7w_wiki.py`; `.agent/` remains the source of truth.

## Primary Runtime Command
`./7w_wiki.py start`

## Execution Modes
- View workflow: `./7w_wiki.py start`
- Execute checklist: `./7w_wiki.py start --run`

## Follow-up Commands
- `./7w_wiki.py advisor --json`
- `./7w_wiki.py mail inbox --status OPEN`
- `./7w_wiki.py test --suite clean-client-state`

## Instructions
- Use this adapter when opening a fresh Siebenwind session in Codex or another IDE.
- Run the primary command first; use --run only when the workflow checklist should execute interactively.
- Review advisor output, open dispatch, clean-client-state, and the latest session memory before taking new work.

## References
- `.agent/workflows/start.md`
- `MASTER_TASK_LIST.md`
- `Logs/Archive/SESSION_MEMORY_*.md`
