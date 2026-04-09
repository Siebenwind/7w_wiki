---
name: Test Waechter
description: Standardized suite execution, defect routing via Dispatch/Task, and re-test discipline.
---

# Codex Skill: Test Waechter

> **Canonical skill**: `.agent/skills/test_waechter/SKILL.md`
> **Marker**: Generated Codex adapter skill. Do not edit manually.

This adapter is generated from the canonical catalog. Runtime execution stays on `./7w_wiki.py`; `.agent/` remains the source of truth.

## Primary Runtime Command
`./7w_wiki.py test --suite clean-client-state`

## Follow-up Commands
- `./7w_wiki.py test --suite all`
- `./7w_wiki.py test --suite adapter-surfaces-contract`

## Instructions
- Use this adapter for standardized suite execution and defect-routing discipline.
- On failure, create or claim the defect communication artifact before editing.
- Re-run focused suites first, then the broader regression pass.

## References
- `.agent/skills/test_waechter/SKILL.md`
- `.agent/workflows/test_run.md`
