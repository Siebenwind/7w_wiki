---
name: Stats
description: Generates and validates wiki statistics outputs for readers and machine consumers.
---

# Skill: Stats
> **Wrapper for**: `.agent/workflows/stats.md`

This skill executes the wiki stats workflow and verifies the reader contract output.

## Runtime
- `./7w_wiki.py stats`
- `./7w_wiki.py test --suite reader-stats-contract`

## Outputs
- `Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md` as reader-facing status page.
- `Logs/INGESTION_TRACKING_REGISTER.md` for tracking.
- `Logs/Archive/STATS_SNAPSHOT_latest.json` as machine-readable snapshot.

