# Session Memory: Codex Bridge Docs Polish

- Date: 2026-03-10
- Focus: Human-readable Codex bridge guidance for operators and maintainers

## Context
- The Codex workflow bridge implementation was present and tested, but the highest-level human-facing explanation was still thin.
- `AGENTS.md` did not yet explain the bridge names and practical startup usage, and the maintainer write-permission requirement for `.agents/skills/` only lived in transient notes.

## What Changed
- Added a compact `Codex Workflow Bridges` section to `AGENTS.md`.
- Documented the practical mapping from Antigravity-style expectations to Codex bridge wrappers.
- Added a maintainer rule to `System/AGENT_OPERATIONS_HANDBOOK.md` explaining that workflow bridges are generated from workflow metadata and require write access to `.agents/skills/` during sync.

## Verification
- `./7w_wiki.py test --suite codex-workflow-bridges`
- `./7w_wiki.py test --suite interop-doc-links`

## Notes
- This pass adds operator clarity only; no runtime or bridge-generation logic changed.
