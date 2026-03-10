# Session Memory: Pages Integrity Hardening

- Date: 2026-03-09
- Focus: Published-site link integrity, Roamlinks repair flow, Pages health visibility, and tech cadence

## Context
- The repo already had stronger CLI/interop contracts, but published Pages integrity still lagged behind source-level audits.
- `audit` and `repair` were repo-centric; `advisor` had no view of stale site validation; workflows did not yet treat Pages health as part of routine tech hygiene.

## What Changed
- Added `.agent/scripts/pages_integrity.py` as the shared Pages warning parser and normalization layer for `pages`, `audit`, `repair`, and `advisor`.
- Added `.agent/config/pages_link_policy.json` for machine-readable allowlist / planned-fix tracking and `.agent/data/pages_health.json` for the latest validation snapshot.
- Extended `./7w_wiki.py audit` with `--pages` so site integrity is reported alongside content backlog, wiki integrity, and source hygiene.
- Extended `./7w_wiki.py repair` with `--fix-roamlinks [--auto] [--dry-run]` for bounded aggressive repairs based on unresolved Pages targets.
- Extended `./7w_wiki.py pages validate` with `--json` and `--strict-links`; default validation now warns on unresolved internal links without hard-failing unless the build fails or strict-link gating is explicitly requested.
- Extended `advisor --json` with `pages_health` and `tech_hygiene.last_sync_interop_at`, and added recommendations that route stale/degraded site health to `/tech_master`.
- Updated standard workflows and governance docs so Pages validation, Pages-aware audit, and Roamlinks repair are part of normal tech/QA cadence.
- Fixed the CLI wrapper so child-script non-zero exits propagate cleanly instead of appending wrapper error text that breaks JSON consumers.

## Current Signal
- Latest snapshot: `WARN`
- Unresolved internal targets: `813`
- Non-allowlisted unresolved targets: `811`
- Dry-run repair currently identifies `29` fixable targets and `523` ambiguous suggestion-only targets.

## Files of Note
- `7w_wiki.py`
- `.agent/scripts/pages_integrity.py`
- `.agent/scripts/pages_tool.py`
- `.agent/scripts/register_check.py`
- `.agent/scripts/repair.py`
- `.agent/scripts/advisor.py`
- `.agent/config/pages_link_policy.json`
- `.agent/data/pages_health.json`
- `.agent/tests/suites/pages-link-contract.json`

## Verification
- `./7w_wiki.py tech --sync-interop`
- `./7w_wiki.py advisor --json`
- `./7w_wiki.py pages validate --json --skip-audit`
- `./7w_wiki.py repair --fix-roamlinks --dry-run`
- `./7w_wiki.py test --suite pages-link-contract --timeout 300`
- `./7w_wiki.py test --suite all`

## Notes / Risks
- The Pages contract is green, but the published-site backlog is still real: unresolved Roamlinks remain in the hundreds and need follow-up content repair, not just infrastructure work.
- `audit --pages --json` is intentionally slow because it performs a real MkDocs build; the test suite uses extended per-case timeouts accordingly.
