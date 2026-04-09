---
name: Time Keeper
description: Utilities for handling the Siebenwind "Sonnenzirkel" time system (Calendar, Seasons, Dates).
---

# Codex Skill: Time Keeper

> **Canonical skill**: `.agent/skills/time_keeper/SKILL.md`
> **Marker**: Generated Codex adapter skill. Do not edit manually.

This adapter is generated from the canonical catalog. Runtime execution stays on `./7w_wiki.py`; `.agent/` remains the source of truth.

## Primary Runtime Command
`./7w_wiki.py search "Sonnenzirkel" --source all`

## Follow-up Commands
- `./7w_wiki.py mail post --from TimeKeeper --to Historian --subject "<calendar question>" --body "<summary>"`

## Instructions
- Use this adapter for calendar, season, and date-validation questions tied to the Sonnenzirkel system.
- The bundled helper script remains the detailed reference implementation until a first-class CLI command exists.
- Treat search results as canon context and escalate ambiguous chronology questions rather than improvising.

## References
- `.agent/skills/time_keeper/SKILL.md`
- `.agent/skills/time_keeper/scripts/sonnenzirkel.py`
