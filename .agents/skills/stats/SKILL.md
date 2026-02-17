---
name: Stats Bridge
description: Thin wrapper for reader-first wiki statistics and progress transparency via ./7w_wiki.py stats.
---

# Skill: Stats
> **Wrapper for**: `.agent/workflows/stats.md`

Use this skill when updating the reader-facing status page and its progress context.

## Usage

```bash
./7w_wiki.py stats
./7w_wiki.py test --suite reader-stats-contract
```

## Output Surfaces
- Reader page: `Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md`
- Tracking detail: `Logs/INGESTION_TRACKING_REGISTER.md`
- Machine snapshot (interchangeable for scripts/tools): `Logs/Archive/STATS_SNAPSHOT_latest.json`

## Contract
- Keep the page reader-centric.
- Keep workshop transparency visible but compact.
- Preserve references to live progress sources (`Audit`, `TEST`, `MASTER_TASK_LIST`, `CHANGELOG`).
