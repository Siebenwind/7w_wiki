# Session Memory: Codex Workflow Bridges & Forum Search

- Date: 2026-03-10
- Focus: Generated Codex workflow bridges, dedicated forum-search workflow, and interop/test enforcement

## Context
- The repo already exposed skills to external agents through `.agents/skills/`, but Codex had no dedicated workflow-facing entrypoints comparable to the Antigravity UX.
- `/scout` also mixed broad discovery and forum-source hunting, which made Codex-facing source discovery too fuzzy.

## What Changed
- Added `.agent/workflows/forum_search.md` as a dedicated workflow for finding new ingestable forum sources.
- Kept `/scout` as the promoted umbrella discovery workflow and clarified the split between broad recon and board-first source hunting.
- Added workflow metadata for Codex bridge generation to `/start`, `/takeover`, `/handover`, `/tech_master`, `/test_run`, and `/forum_search`.
- Added `.agent/scripts/generate_workflow_bridges.py` and wired it into `./7w_wiki.py tech --sync-bridges` / `--sync-interop`.
- Generated six Codex-facing workflow wrappers under `.agents/skills/`.
- Extended the workflow matrix generator so a workflow can be marked executable via an existing runtime adapter even without a same-named CLI command.
- Replaced stale bridge-language in docs (`onboarding`, `test-run`, `interop-audit`) with the actual generated wrapper model.
- Added `codex-workflow-bridges` as a regression suite and integrated it into the standard validation path.

## Files of Note
- `7w_wiki.py`
- `.agent/scripts/generate_workflow_bridges.py`
- `.agent/scripts/update_matrix.py`
- `.agent/workflows/forum_search.md`
- `.agents/skills/workflow_forum_search/SKILL.md`
- `.agent/tests/suites/codex-workflow-bridges.json`

## Verification
- `./7w_wiki.py tech --sync-interop`
- `./7w_wiki.py test --suite codex-workflow-bridges`
- `./7w_wiki.py test --suite workflow-matrix-contract`
- `./7w_wiki.py test --suite interop-doc-links`
- `./7w_wiki.py test --suite all`

## Notes / Risks
- Bridge regeneration under `.agents/skills/` required running `./7w_wiki.py tech --sync-interop` with elevated filesystem permission in this environment because the sandbox could not create new directories there.
- `/forum_search` is intentionally procedural only; execution still flows through the existing `scout` runtime family.
