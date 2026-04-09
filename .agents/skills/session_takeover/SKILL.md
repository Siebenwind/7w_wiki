---
name: Session Takeover
description: Codex-native adapter for adopting an existing Siebenwind session.
---

# Codex Skill: Session Takeover

> **Canonical workflow**: `.agent/workflows/takeover.md`
> **Marker**: Generated Codex adapter skill. Do not edit manually.

This adapter is generated from the canonical catalog. Runtime execution stays on `./7w_wiki.py`; `.agent/` remains the source of truth.

## Primary Runtime Command
`./7w_wiki.py takeover`

## Execution Modes
- View workflow: `./7w_wiki.py takeover`
- Execute checklist: `./7w_wiki.py takeover --run`

## Follow-up Commands
- `./7w_wiki.py start`
- `./7w_wiki.py advisor --json`
- `./7w_wiki.py mail inbox --status OPEN`

## Instructions
- Use this adapter when inheriting work from a prior agent session.
- Prefer /start as the canonical routing surface; antigravity survives only as a compatibility alias.
- Carry forward open dispatches, the latest session memory, and unresolved historian or technician gates explicitly.

## References
- `.agent/workflows/takeover.md`
- `.agent/workflows/start.md`
- `Logs/Archive/SESSION_MEMORY_*.md`
