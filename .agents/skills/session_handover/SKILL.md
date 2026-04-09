---
name: Session Handover
description: Codex-native closeout adapter for session memory, dispatch, and validation handoff.
---

# Codex Skill: Session Handover

> **Canonical workflow**: `.agent/workflows/handover.md`
> **Marker**: Generated Codex adapter skill. Do not edit manually.

This adapter is generated from the canonical catalog. Runtime execution stays on `./7w_wiki.py`; `.agent/` remains the source of truth.

## Primary Runtime Command
`./7w_wiki.py handover`

## Execution Modes
- View workflow: `./7w_wiki.py handover`
- Execute checklist: `./7w_wiki.py handover --run`

## Follow-up Commands
- `./7w_wiki.py test --suite all`
- `./7w_wiki.py stats`
- `./7w_wiki.py mail post --from Oberarchivar --to Coordinator --subject "<abschluss>" --body "<summary>`

## Instructions
- Use this adapter when ending a working session and preparing the next agent handoff.
- Keep validation, session-memory creation, and dispatch reporting coupled; no silent closeout is acceptable.
- If technical or published-doc surfaces changed, include the pages snapshot or pages validation result in the handoff note.

## References
- `.agent/workflows/handover.md`
- `CHANGELOG.md`
- `Logs/Archive/SESSION_MEMORY_*.md`
