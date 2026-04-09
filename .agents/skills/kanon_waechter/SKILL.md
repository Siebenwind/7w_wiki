---
name: Kanon-Wächter (Verification)
description: Fähigkeit, Fakten gegen die offizielle Homepage zu prüfen.
---

# Codex Skill: Kanon-Wächter (Verification)

> **Canonical skill**: `.agent/skills/kanon_waechter/SKILL.md`
> **Marker**: Generated Codex adapter skill. Do not edit manually.

This adapter is generated from the canonical catalog. Runtime execution stays on `./7w_wiki.py`; `.agent/` remains the source of truth.

## Primary Runtime Command
`./7w_wiki.py search <query> --source all`

## Follow-up Commands
- `./7w_wiki.py historian <query>`
- `./7w_wiki.py mail post --from Guardian --to Historian --subject "<conflict>" --body "<summary>"`

## Instructions
- Use this adapter when a claim needs canon verification against higher-precedence material.
- Search wiki and sources together first; escalate contradictions instead of silently normalizing them.
- Homepage and sources outrank wiki pages for factual resolution.

## References
- `.agent/skills/kanon_waechter/SKILL.md`
- `System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md`
