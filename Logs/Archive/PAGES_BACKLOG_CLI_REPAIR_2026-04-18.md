# Pages Backlog CLI Repair Mode - 2026-04-18

## Done

- Added `./7w_wiki.py repair --backlog-inventory --json`.
- Reworked `./7w_wiki.py repair --apply-lane1` to use occurrence-level backlog repairs instead of target-only alias normalization.
- Changed `./7w_wiki.py repair --backlog-board --dry-run --json` so dry-run reports `artifacts.written=false` and does not write `.agent/data/backlog_*.json` artifacts.
- Applied the safe technical wrapper wave in derived wiki/archive docs: 66 files had Markdown URL targets with literal or encoded WikiLink wrappers normalized.
- Kept `docs/Quellen` read-only.

## Current Backlog

- Pages remains `WARN`: 629 unresolved / 627 unallowlisted.
- Post-apply inventory: 319 concrete publish-facing occurrences.
- Occurrence split: 310 `manual_review`, 9 `read_only_source_residue`.
- Unfound Pages targets from the current snapshot: 201.
- No remaining auto-safe Lane-1 wrapper occurrence is currently planned.

## Verified

- `./7w_wiki.py test --suite source-link-hygiene`: PASS.
- `./7w_wiki.py test --suite pages-contract-mode-contract`: PASS.
- `./7w_wiki.py test --suite tool-manifest-contract`: PASS.
- `./7w_wiki.py audit --json`: fails only for the known `score_cluster`.
- `./7w_wiki.py pages validate --contract --json`: keeps `drift_status=PASS` and `legacy_root_status=removed`.
- `./7w_wiki.py pages validate --json --skip-audit`: build succeeds, Pages remains `WARN` at 629/627.
- `./7w_wiki.py pages validate --json --strict-links`: still fails at audit precheck because `score_cluster` is separate.
- Targeted `rg` for Markdown URL targets containing nested WikiLinks in `docs/Siebenwind_Wiki` and `docs/Archiv`: clean.

## Next

- Resolve `score_cluster` as a separate audit gate fix before expecting strict Pages to proceed.
- Use `repair --backlog-inventory --json` as the working queue for remaining Pages backlog triage.
- Route `manual_review` clusters to Historian review; do not bridge or invent lore.
- Document `docs/Quellen` residues as read-only unless a future task explicitly permits purely technical wrapper or metadata corrections that preserve source wording.
