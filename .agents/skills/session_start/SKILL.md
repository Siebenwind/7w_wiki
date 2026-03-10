---
name: Session Start
description: Codex kickoff wrapper for the standard onboarding loop.
---

# Workflow Bridge: /start

> **Wrapper for**: `.agent/workflows/start.md`
> **Marker**: Generated workflow bridge. Do not edit manually.

This is a generated Codex-facing workflow bridge. Runtime execution must stay on `./7w_wiki.py`.

## Primary Runtime Command
`./7w_wiki.py start`

## Execution Mode
- View workflow: `./7w_wiki.py start`
- Execute checklist: `./7w_wiki.py start --run`

## Follow-up Commands
- `./7w_wiki.py advisor --json`
- `./7w_wiki.py mail inbox --status OPEN`
- `./7w_wiki.py test --suite clean-client-state`

## Usage Rule
Read `.agent/workflows/start.md` for the authoritative process. Do not guess workflow semantics from this bridge file alone.
