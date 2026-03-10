---
name: Workflow Test Run
description: Codex bridge for the standard interop and regression validation loop.
---

# Workflow Bridge: /test_run

> **Wrapper for**: `.agent/workflows/test_run.md`
> **Marker**: Generated workflow bridge. Do not edit manually.

This is a generated Codex-facing workflow bridge. Runtime execution must stay on `./7w_wiki.py`.

## Primary Runtime Command
`./7w_wiki.py test --suite all`

## Follow-up Commands
- `./7w_wiki.py test --suite codex-workflow-bridges`
- `./7w_wiki.py pages validate --json`
- `./7w_wiki.py mail inbox --status OPEN`

## Usage Rule
Read `.agent/workflows/test_run.md` for the authoritative process. Do not guess workflow semantics from this bridge file alone.
