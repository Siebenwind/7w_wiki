---
name: Art Director (Atelier)
description: Codex-native visual-direction adapter for style-safe asset work and dispatch coordination.
---

# Codex Skill: Art Director (Atelier)

> **Canonical skill**: `.agent/skills/art_director/SKILL.md`
> **Marker**: Generated Codex adapter skill. Do not edit manually.

This adapter is generated from the canonical catalog. Runtime execution stays on `./7w_wiki.py`; `.agent/` remains the source of truth.

## Primary Runtime Command
`./7w_wiki.py mail post --from ArtDirector --to Coordinator --subject "<visual task>" --body "<summary>"`

## Follow-up Commands
- `./7w_wiki.py mail inbox --status OPEN`

## Instructions
- Use this adapter for visual direction, asset review, and style-governed art requests.
- The repo has no dedicated image-generation CLI yet, so route requests and delivery state through Dispatch while following the canonical style preset.
- Keep sidecar metadata and canon anchor references coupled to every produced asset.

## References
- `.agent/skills/art_director/SKILL.md`
- `docs/assets/`
