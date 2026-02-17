---
name: Historian Bridge
description: Thin wrapper for deep lore analysis via ./7w_wiki.py historian and Oracle search.
---

# Skill: The Historian (Lore Reconstruction)
> **Wrapper for**: `.agent/workflows/historian.md`

This skill is a procedural workflow for deep lore analysis and conflict resolution.

## Usage
To start a historian session:
```bash
./7w_wiki.py historian "<Topic>"
```

## Workflow Steps
1.  **Search**: Runs the Oracle in three scopes:
    - `./7w_wiki.py search "<Topic>" --source wiki`
    - `./7w_wiki.py search "<Topic>" --source quellen`
    - `./7w_wiki.py search "<Topic>" --source all`
2.  **Timeline**: Constructs a chronological sequence of events.
3.  **Conflict Check**: Identifies contradictions between sources.
4.  **Synthesis**: Proposes a canonical version (or tags as `[UNGEKLÄRT]`).
5.  **Dispatch Discipline**: Report progress and specialist follow-ups via `./7w_wiki.py mail ...` (inbox/claim/done/post).
