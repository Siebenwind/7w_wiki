# Skill: The Historian (Lore Reconstruction)
> **Wrapper for**: `.agent/workflows/historian.md`

This skill is a procedural workflow for deep lore analysis and conflict resolution.

## Usage
To start a historian session:
```bash
./7w_wiki.py historian "<Topic>"
```

## Workflow Steps
1.  **Search**: Queries the Oracle for all relevant mentions.
2.  **Timeline**: Constructs a chronological sequence of events.
3.  **Conflict Check**: Identifies contradictions between sources.
4.  **Synthesis**: Proposes a canonical version (or tags as `[UNGEKLÄRT]`).
