---
name: Workflow Forum Search
description: Codex-native discovery adapter for board-first source scanning and ingest lead generation.
---

# Codex Skill: Workflow Forum Search

> **Canonical workflow**: `.agent/workflows/forum_search.md`
> **Marker**: Generated Codex adapter skill. Do not edit manually.

This adapter is generated from the canonical catalog. Runtime execution stays on `./7w_wiki.py`; `.agent/` remains the source of truth.

## Primary Runtime Command
`./7w_wiki.py scout --forum bekanntmachungen --pages 3`

## Follow-up Commands
- `./7w_wiki.py scout --forum news --pages 3`
- `./7w_wiki.py scout --forum geschichten --pages 5`
- `./7w_wiki.py mail post --from Scout --to Ingestor --subject "<source lead>" --body "<summary>`

## Instructions
- Use this adapter when the task is forum-first discovery rather than broad homepage or web scouting.
- Restrict scanning to the allowlisted boards and treat outputs as leads, not as already integrated sources.
- Escalate only genuine contention or unresolved canon questions; routine ingest leads go to the Ingestor.

## References
- `.agent/workflows/forum_search.md`
- `Quellen/Forum/`
- `docs/Quellen/Forum/`
