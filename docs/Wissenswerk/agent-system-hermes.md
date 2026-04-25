---
layout: wiki_page
title: Wissenswerk Agent System Integration
category: Technical
---

# Wissenswerk Agent System Integration

Wissenswerk is designed so Hermes, Codex, Jules, Gemini CLI, Cursor, Aider, and future hosts can work from the same neutral contracts.

## Hermes Role

Hermes should act as a `coordinator` by default:

1. Read `AGENTS.md`, `DESIGN.md`, `project_manifest.json`, and `wissenswerk.yaml`.
2. Run `./wissenswerk.py doctor --json`.
3. Inspect `./wissenswerk.py export plan --json` before public-repo work.
4. Delegate bounded work to `curator`, `verifier`, or `maintainer` roles.
5. End with concise status and machine-readable reports.

## Role Mapping

- `coordinator`: plans runs, checks state, decides escalation
- `curator`: imports RagPrep artifacts and drafts article plans
- `verifier`: checks provenance, conflicts, links, and audit reports
- `maintainer`: changes core code, provider layer, migrations, tests, and export tooling

Localized display names are aliases only. Public role IDs stay English.

## Skill Surfaces

Hermes should prefer these neutral surfaces:

- CLI JSON from `./wissenswerk.py`
- `AGENTS.md` and nested tenant instructions
- `DESIGN.md`
- `project_manifest.json`
- `wissenswerk_export_manifest.json`
- MCP and tool manifests

Host-specific skill folders are generated adapter outputs. They must not contain unique semantics absent from the neutral contracts.

## Standard Automated Flow

```text
doctor -> export plan -> ingest -> curate -> wiki build -> search -> audit/report
```

For maintainer work:

```text
doctor -> hygiene reports -> plan -> apply -> tests -> export plan -> report
```

Hermes should never treat memory or chat history as factual authority. Facts come from sources, wiki pages, provenance, retrieval, and audits.
