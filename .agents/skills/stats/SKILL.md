---
name: Stats
description: Codex-native statistics adapter for reader-facing and machine-readable wiki status outputs.
---

# Codex Skill: Stats

> **Canonical runtime surface**: `7w_wiki.py`
> **Marker**: Generated Codex adapter skill. Do not edit manually.

This adapter is generated from the canonical catalog. Runtime execution stays on `./7w_wiki.py`; `.agent/` remains the source of truth.

## Primary Runtime Command
`./7w_wiki.py stats`

## Follow-up Commands
- `./7w_wiki.py test --suite reader-stats-contract`

## Instructions
- Use this adapter when reader-facing stats pages or machine snapshots need regeneration.
- Treat the reader page, tracking register, and JSON snapshot as a coupled contract.
- Validate the reader-stats contract after regeneration.

## References
- `docs/Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md`
- `Logs/Archive/STATS_SNAPSHOT_latest.json`
- `Logs/INGESTION_TRACKING_REGISTER.md`
