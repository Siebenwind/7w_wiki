# Interop Guidelines

Goal: consistent behavior across Codex, MCP-capable IDEs/CLIs, and future agent hosts without making any host-specific adapter authoritative.

## Core Rules

1. Generic Wissenswerk operations run through `./wissenswerk.py`.
2. Legacy Siebenwind operations run through `./7w_wiki.py`.
3. Platform-neutral contracts come first: `AGENTS.md`, `DESIGN.md`, `wissenswerk.yaml`, `project_manifest.json`, JSON CLI output, tool manifests, and MCP.
4. IDE-specific files such as `.agents/skills/` and `.codex/config.toml` are generated adapters.
5. `project_manifest.json` is the generic product manifest; `lore_manifest.json` is a legacy Siebenwind compatibility surface.

## Layer Model

- Wissenswerk core: `./wissenswerk.py`, `wissenswerk.yaml`, `project_manifest.json`, `AGENTS.md`, `DESIGN.md`.
- Legacy core: `.agent/` plus `./7w_wiki.py`.
- Open runtime surface: JSON CLI and MCP.
- Tool discovery: `.agent/config/tools.json`, `.agent/catalog/catalog.v1.json`.
- Host adapters: `.agents/skills/`, `.codex/config.toml`, future Gemini/Cursor/Aider/Jules adapters.

## Required Checks

```bash
python3 -m py_compile wissenswerk.py
./wissenswerk.py doctor --json
./wissenswerk.py hygiene reports --json
./wissenswerk.py export plan --json
./7w_wiki.py test --suite wissenswerk-contract --timeout 60
git diff --check
```

When interop contracts changed, add:

```bash
./7w_wiki.py test --suite interop-command-registry --timeout 60
./7w_wiki.py test --suite manifest-contract --timeout 60
./7w_wiki.py test --suite tool-manifest-contract --timeout 60
```

Legacy `audit`, Pages validation, full MkDocs builds, and source/content/render suites are not default checks for Wissenswerk-only work. They belong to Siebenwind tenant or legacy tooling changes.

## Runtime and State Hygiene

- Runtime state, local DBs, provider secrets, pgvector dumps, bot sessions, and private RagPrep outputs are not repository truth.
- Use `./wissenswerk.py reset ... --dry-run --json` for Wissenswerk state planning.
- Use `./7w_wiki.py tech --repo-hygiene [--apply] [--json]` for legacy hot/cold/runtime/build classification.

## Canonical Sources

- `AGENTS.md`
- `DESIGN.md`
- `System/Synapse_Board/SY_INTEROP.md`
- `System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md`
- `System/AGENT_OPERATIONS_HANDBOOK.md`
