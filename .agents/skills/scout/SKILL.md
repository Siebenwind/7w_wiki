---
name: Skill: Der Netz-Wächter (Web-Scout)
description: Der Netz-Wächter ist darauf spezialisiert, dynamische Inhalte aus dem Internet (Homepage, Forum) zu extrahieren und in das Siebenwind-Wiki zu integrieren.
---

# Codex Skill: Skill: Der Netz-Wächter (Web-Scout)

> **Canonical skill**: `.agent/skills/scout/SKILL.md`
> **Marker**: Generated Codex adapter skill. Do not edit manually.

This adapter is generated from the canonical catalog. Runtime execution stays on `./7w_wiki.py`; `.agent/` remains the source of truth.

## Primary Runtime Command
`./7w_wiki.py scout --forum bekanntmachungen --pages 3`

## Follow-up Commands
- `./7w_wiki.py scout --forum news --pages 3`
- `./7w_wiki.py mail post --from Scout --to Ingestor --subject "<source lead>" --body "<summary>"`

## Instructions
- Use this adapter for external discovery work that touches homepage or forum surfaces.
- Stay passive: no posting, no interaction, only observation and structured lead capture.
- Route ingest leads to the Ingestor and reserve historian escalation for real contention.

## References
- `.agent/skills/scout/SKILL.md`
- `.agent/workflows/forum_search.md`
