---
name: Scanner (Ingestion)
description: Fähigkeit, Verzeichnisstrukturen zu analysieren und relevante Dateien zu lesen.
---

# Codex Skill: Scanner (Ingestion)

> **Canonical skill**: `.agent/skills/scanner/SKILL.md`
> **Marker**: Generated Codex adapter skill. Do not edit manually.

This adapter is generated from the canonical catalog. Runtime execution stays on `./7w_wiki.py`; `.agent/` remains the source of truth.

## Primary Runtime Command
`./7w_wiki.py search <query> --source quellen`

## Follow-up Commands
- `./7w_wiki.py scout --forum bekanntmachungen --pages 3`

## Instructions
- Use this adapter for source-corpus inventory and lead preparation before ingestion or historian work.
- Prefer source-targeted search first; use forum scouting only when the task expands beyond the local corpus.
- Treat raw file exploration as a method hint, not as a replacement for the CLI runtime contract.

## References
- `.agent/skills/scanner/SKILL.md`
