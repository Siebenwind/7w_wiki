---
name: Wiki-Schmied (Production)
description: Fähigkeit, standardisierte Wiki-Artikel zu erstellen.
---

# Codex Skill: Wiki-Schmied (Production)

> **Canonical skill**: `.agent/skills/wiki_schmied/SKILL.md`
> **Marker**: Generated Codex adapter skill. Do not edit manually.

This adapter is generated from the canonical catalog. Runtime execution stays on `./7w_wiki.py`; `.agent/` remains the source of truth.

## Primary Runtime Command
`./7w_wiki.py sanitize [target]`

## Follow-up Commands
- `./7w_wiki.py audit`
- `./7w_wiki.py repair --fix-roamlinks --dry-run`

## Instructions
- Use this adapter for production-safe wiki article shaping, structure hygiene, and link integrity follow-through.
- Keep report_id, source references, and anti-bridge policy aligned with the canonical production skill.
- Validate the page and its references after structural edits.

## References
- `.agent/skills/wiki_schmied/SKILL.md`
- `System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md`
