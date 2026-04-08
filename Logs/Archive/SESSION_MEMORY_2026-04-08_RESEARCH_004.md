# Session Memory: RESEARCH-2026-004

- Date: 2026-04-08
- Focus: Reconstruct the source-secure history of `Tjure Odal` and `Arn Toron` in the `Marnie Ruatha` accusation complex and bring the research board back in line with the actual repo state.

## Context
- `RESEARCH-2026-004` still appeared on the research board as `OPEN` with the description that `Tjure Odal` did not exist in the wiki and `Arn Toron` had an unclear role.
- The repo already contained draft pages for both figures, but their certainty level and source basis were uneven.
- `./7w_wiki.py search "Tjure Odal Arn Toron" --source all` failed in this runtime because the Oracle reranker model was not locally cached and network access was unavailable.

## What Changed
- Created the research report:
  - `Logs/Research/RESEARCH-2026-004_Summary.md`
- Reworked `docs/Siebenwind_Wiki/07_Persoenlichkeiten/Arn_Toron.md`:
  - added proper frontmatter / layout metadata
  - corrected the primary source anchor to `Siebenwind_Bote_184`
  - tightened the biography from a generic traitor/heretic frame to the source-secure arc:
    - former Konsul,
    - Kaufmann / Leiter des Warenkontors,
    - political actor in the Falkensee crisis,
    - later Brandenstein exile,
    - "Ketzer" only as accusation in Bote 186
- Reworked `docs/Siebenwind_Wiki/07_Persoenlichkeiten/Tjure_Odal.md`:
  - added proper frontmatter / layout metadata
  - reduced the page to the secure minimal finding:
    - only named in Bote 186,
    - no independent biography in the checked corpus,
    - all further role/network assumptions remain `[UNGEKLAERT]`
- Repaired the truncated 22-n.H. crisis passage in:
  - `docs/Siebenwind_Wiki/07_Persoenlichkeiten/Marnie_Ruatha.md`
- Removed the unsupported Arn-Toron mention from:
  - `docs/Siebenwind_Wiki/04_Chronik/Siebenwind_Bote_168.md`
- Updated the person register:
  - `docs/Siebenwind_Wiki/00_Fundament/Personenregister.md`
- Moved the board item to review state and updated the stale description in:
  - `System/Synapse_Board/LORE_RESEARCH_BOARD.md`
  - `docs/Archiv/Research_Board.md`
  - `MASTER_TASK_LIST.md`
- Documented the pass in:
  - `CHANGELOG.md`

## Verification
- Manual source reading against:
  - `Quellen/Zeitung 7w Bote/Siebenwind Bote 167.md`
  - `Quellen/Zeitung 7w Bote/Siebenwind Bote 168.md`
  - `Quellen/Zeitung 7w Bote/Siebenwind_Bote_184.md`
  - `Quellen/Zeitung 7w Bote/Siebenwind Bote 186.md`
- `./7w_wiki.py search "Tjure Odal Arn Toron" --source all`
  - failed due missing cached Oracle reranker / offline runtime
  - historian fallback to direct sources documented in the report
- `./7w_wiki.py check docs/Siebenwind_Wiki/07_Persoenlichkeiten/Arn_Toron.md`
  - PASS after H1 normalization
- `./7w_wiki.py check docs/Siebenwind_Wiki/07_Persoenlichkeiten/Tjure_Odal.md`
  - PASS
- `./7w_wiki.py check docs/Siebenwind_Wiki/07_Persoenlichkeiten/Marnie_Ruatha.md`
  - PASS
- `./7w_wiki.py check docs/Siebenwind_Wiki/04_Chronik/Siebenwind_Bote_168.md`
  - PASS after H1 normalization
- `./7w_wiki.py pages validate --json --fast --skip-audit`
  - `WARN`, but only on the pre-existing global Pages backlog outside this research topic

## Result
- `Arn Toron` is now documented as a source-attested political figure and later exile, not as a proven heretic.
- `Tjure Odal` is now documented honestly as a single-mention accusation name with unresolved biography.
- The research board no longer claims that Tjure is missing from the wiki or that Arn's role is wholly unclear.
- `RESEARCH-2026-004` is ready for review.

## Next
- Post the research closeout via dispatch.
- If a later source yields an independent mention of `Tjure Odal`, reopen the biography work from that evidence rather than from inference.
- If the broader Pages / audit backlog is tackled later, keep it scoped separately from this completed historian research pass.
