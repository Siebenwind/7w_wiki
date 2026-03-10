---
name: Session Handover
description: Codex bridge for closing a session and preparing the next agent handoff.
---

# Workflow Bridge: /handover

> **Wrapper for**: `.agent/workflows/handover.md`
> **Marker**: Generated workflow bridge. Do not edit manually.

This is a generated Codex-facing workflow bridge. Runtime execution must stay on `./7w_wiki.py`.

## Primary Runtime Command
`./7w_wiki.py handover`

## Execution Mode
- View workflow: `./7w_wiki.py handover`
- Execute checklist: `./7w_wiki.py handover --run`

## Follow-up Commands
- `./7w_wiki.py test --suite all`
- `./7w_wiki.py stats`
- `./7w_wiki.py mail post --from Oberarchivar --to Coordinator --subject "<abschluss>" --body "<summary>"`

## Usage Rule
Read `.agent/workflows/handover.md` for the authoritative process. Do not guess workflow semantics from this bridge file alone.
