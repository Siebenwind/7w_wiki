---
name: Lore-Gelehrter (Analytik & Auskunft)
description: Fähigkeit, das gesamte Wiki-Wissen zu aggregieren, Inkonsistenzen zu finden und präzise Auskunft zu geben.
---

# Codex Skill: Lore-Gelehrter (Analytik & Auskunft)

> **Canonical skill**: `.agent/skills/lore_gelehrter/SKILL.md`
> **Marker**: Generated Codex adapter skill. Do not edit manually.

This adapter is generated from the canonical catalog. Runtime execution stays on `./7w_wiki.py`; `.agent/` remains the source of truth.

## Primary Runtime Command
`./7w_wiki.py historian <query>`

## Follow-up Commands
- `./7w_wiki.py search <query> --source all`
- `./7w_wiki.py historian review --list --json`
- `./7w_wiki.py historian review --dossier --research-id RESEARCH-2026-XXX --json`
- `./7w_wiki.py mail post --from Historian --to ALL --subject "<lore question>" --body "<summary>"`

## Instructions
- Use this adapter for deep lore synthesis, contradiction analysis, and evidence-backed answers.
- The Historian is an escalation and synthesis organ, not the default editor for straightforward source integration.
- Use historian review for structured Research Board review backlog before relying on ad-hoc Dispatch reading.
- Route unresolved contradictions through Dispatch or the Synapse Board with explicit evidence.

## References
- `.agent/skills/lore_gelehrter/SKILL.md`
- `System/Synapse_Board/LORE_RESEARCH_BOARD.md`
