---
name: Der Lektor (Qualitätssicherung)
description: Automatisierte Prüfung von Stil, Grammatik und Markdown-Formatierung für konsistente "Siebenwind Voice".
---

# Codex Skill: Der Lektor (Qualitätssicherung)

> **Canonical skill**: `.agent/skills/lektor/SKILL.md`
> **Marker**: Generated Codex adapter skill. Do not edit manually.

This adapter is generated from the canonical catalog. Runtime execution stays on `./7w_wiki.py`; `.agent/` remains the source of truth.

## Primary Runtime Command
`./7w_wiki.py check [path]`

## Follow-up Commands
- `./7w_wiki.py lint [target]`

## Instructions
- Use this adapter for style, grammar, and markdown hygiene checks.
- Run check first on the narrow target; escalate to lint when broader repo coverage is needed.
- Treat findings as quality gates before final publication or handoff.

## References
- `.agent/skills/lektor/SKILL.md`
