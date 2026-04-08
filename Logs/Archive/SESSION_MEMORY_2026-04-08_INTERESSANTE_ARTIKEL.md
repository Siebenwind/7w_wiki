# Session Memory: Interessante Artikel April-Rotation

- Date: 2026-04-08
- Focus: Fulfill `MSG-2026-0017` by replacing the generic reader curation with a monthly thematic shortlist and synchronizing the landing-page teaser.

## Context
- `MSG-2026-0017` requested a monthly shortlist of 3-5 articles for `Interessante Artikel`, each with canon rationale, source basis, and reader value.
- The existing curation page still contained a generic foundational list rather than a dated thematic rotation.
- The landing page still mirrored the old generic selection.

## What Changed
- Claimed `MSG-2026-0017` as `Historian`.
- Reworked `docs/Siebenwind_Wiki/10_Archiv/Interessante_Artikel.md` into the April 2026 rotation:
  - theme: `Unter dem Weissen Hochturm`
  - shortlist: `Draconis`, `Das Pantheon`, `Codex Iuris Canonici`, `Ring des Argionemes`, `Arman`
  - each entry now carries canon rationale, source basis, and reader value
  - added four non-mechanical archive motif suggestions
  - set next review target to the first calendar week of May 2026
- Updated the landing teaser in `docs/index.md` so the visible homepage picks now reflect the live rotation:
  - `Draconis`
  - `Codex Iuris Canonici`
  - `Arman`
- Updated `CHANGELOG.md` with the April curation rotation entry.
- Normalized the frontmatter of the five curated articles:
  - added `layout: wiki_page`
  - kept/updated curation score metadata where relevant

## Verification
- `./7w_wiki.py score docs/Siebenwind_Wiki/02_Geografie/Draconis.md`
- `./7w_wiki.py score docs/Siebenwind_Wiki/01_Pantheon/Das_Pantheon.md`
- `./7w_wiki.py score docs/Siebenwind_Wiki/01_Pantheon/Codex_Iuris_Canonici.md`
- `./7w_wiki.py score docs/Siebenwind_Wiki/03_Gesellschaft/Ring_des_Argionemes.md`
- `./7w_wiki.py score docs/Siebenwind_Wiki/07_Persoenlichkeiten/Arman.md`
- `./7w_wiki.py check docs/Siebenwind_Wiki/02_Geografie/Draconis.md`
  - PASS after frontmatter normalization
- `./7w_wiki.py check docs/Siebenwind_Wiki/01_Pantheon/Das_Pantheon.md`
  - PASS after frontmatter normalization
- `./7w_wiki.py check docs/Siebenwind_Wiki/01_Pantheon/Codex_Iuris_Canonici.md`
  - PASS after frontmatter normalization
- `./7w_wiki.py check docs/Siebenwind_Wiki/03_Gesellschaft/Ring_des_Argionemes.md`
  - PASS after frontmatter normalization
- `./7w_wiki.py check docs/Siebenwind_Wiki/07_Persoenlichkeiten/Arman.md`
  - PASS after frontmatter normalization
- `./7w_wiki.py pages validate --json --fast --skip-audit`
  - `WARN`, but only on pre-existing Pages snapshot / unresolved-target backlog outside this curation change

## Result
- `Interessante Artikel` is now a real monthly rotation instead of a static generic list.
- The landing page and archive curation page now point at the same live editorial theme.
- The five featured pages satisfy the repo `check` command, so the rotation no longer rests on known metadata failures.

## Next
- Mark `MSG-2026-0017` done with the April rotation summary.
- Rotate again in the first calendar week of May 2026.
- If the technician lane remains active, keep the separate Pages backlog (`pages validate --strict-links`, audit anomaly, unresolved historical targets) scoped outside this curation track.
