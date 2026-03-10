---
name: Workflow Tech Master
description: Codex bridge for the technician maintenance loop and interop sync path.
---

# Workflow Bridge: /tech_master

> **Wrapper for**: `.agent/workflows/tech_master.md`
> **Marker**: Generated workflow bridge. Do not edit manually.

This is a generated Codex-facing workflow bridge. Runtime execution must stay on `./7w_wiki.py`.

## Primary Runtime Command
`./7w_wiki.py tech`

## Follow-up Commands
- `./7w_wiki.py tech --sync-interop`
- `./7w_wiki.py pages validate --json`
- `./7w_wiki.py audit --pages`

## Usage Rule
Read `.agent/workflows/tech_master.md` for the authoritative process. Do not guess workflow semantics from this bridge file alone.
