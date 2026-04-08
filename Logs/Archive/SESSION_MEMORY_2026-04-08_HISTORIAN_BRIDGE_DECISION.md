# Session Memory: Historian Bridge Decision

- Date: 2026-04-08
- Focus: Complete takeover into the Historian lane, repair the broken `historian` workflow entrypoint, and resolve the remaining semantic bridge decision for `Arman_von_Draconis`.

## Context
- `./7w_wiki.py historian` was broken at session start because the CLI expected `.agent/workflows/historian.md`, but that file did not exist.
- `MSG-2026-0089` asked Historian to decide the canonical target for the residual semantic bridge pages after the technician sweep.
- The only still-unresolved bridge page after the prior pass was `docs/Siebenwind_Wiki/00_Fundament/Arman_von_Draconis.md`.

## What Changed
- Added the missing workflow file:
  - `.agent/workflows/historian.md`
- Claimed `MSG-2026-0089` as `Historian`.
- Resolved `Arman_von_Draconis` as a temporary bridge to `[[Arman]]`, not `[[Draconis]]`, based on local evidence:
  - `docs/Siebenwind_Wiki/07_Persoenlichkeiten/Arman.md` establishes the person article.
  - `docs/Siebenwind_Wiki/04_Chronik/Siebenwind_Bote_123.md` names the figure only as `Arman`.
  - `docs/Siebenwind_Wiki/02_Geografie/Draconis.md` already frames `Arman_von_Draconis` as the same person later known as `Arman`.
- Updated the bridge page metadata:
  - `docs/Siebenwind_Wiki/00_Fundament/Arman_von_Draconis.md`
- Normalized the direct in-repo references that still pointed at the bridge:
  - `docs/Siebenwind_Wiki/02_Geografie/Draconis.md`
  - `docs/Siebenwind_Wiki/00_Fundament/index.md`

## Verification
- `./7w_wiki.py historian`
  - now renders the workflow successfully
- `./7w_wiki.py test --suite interop-doc-links`
  - PASS
- `./7w_wiki.py sanitize --json`
  - `bridge_inventory.invalid = 0`
- `./7w_wiki.py audit --json`
  - `bridge_inventory.invalid = 0`
  - `issues_found = 1`, despite all reported categories being `0`
- `./7w_wiki.py test --suite bridge-placeholder-guard`
  - PASS
- `./7w_wiki.py pages validate --json --strict-links`
  - FAIL
  - failure mode changed: the old semantic bridge blocker is gone; validation now stops on a runtime pre-check because `audit --json` still exits non-zero with `issues_found = 1`

## Result
- The Historian decision gate for `Arman_von_Draconis` is resolved.
- The last invalid bridge page from the prior technician pass is cleared.
- The remaining blocker is no longer lore ambiguity; it is now a technician-facing audit/precheck anomaly.

## Next
- Close `MSG-2026-0089` with the target decision `[[Arman]]`.
- Route the new audit/precheck anomaly back to Technician or Coordinator for runtime investigation.
- After the audit exit mismatch is fixed, rerun `./7w_wiki.py audit --json` and `./7w_wiki.py pages validate --json --strict-links`.
