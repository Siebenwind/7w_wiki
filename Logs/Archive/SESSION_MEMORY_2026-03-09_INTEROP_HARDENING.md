# Session Memory: Interop Hardening

- Date: 2026-03-09
- Focus: Workflow/documentation consistency, typed CLI interop, matrix/doc/tool generation parity

## Context
- The repo had drift between live CLI commands, workflow docs, governance docs, `tools.json`, MCP tool generation, and legacy test suites.
- `scout` remained an intentional product-level exception in prominence, but needed to be normalized as a command-level exception rather than a filesystem-policy exception.

## What Changed
- Extended `./7w_wiki.py --help-json` to emit typed argument metadata, nested subcommand schemas, and command-level interop metadata.
- Reworked `mail` into structured subcommands in the CLI schema while keeping runtime behavior compatible with the dispatch backend.
- Expanded `./7w_wiki.py tech` to expose matrix/doc/interop sync through the canonical runtime surface.
- Replaced the append-only matrix updater with a generator that rebuilds managed matrix sections and preserves the `scout` special-case note.
- Added a dedicated runtime-doc sync script and regenerated `AGENTS.md`, `SY_INTEROP.md`, and `AGENT_OPERATIONS_HANDBOOK.md`.
- Unified `tools.json` and MCP generation around the same typed schema and added structured compound-command tools plus deprecated compatibility aliases.
- Updated workflows and docs to remove stale references to deleted workflows and to standardize `start` / `takeover` / `handover` execution semantics.
- Updated Oracle interpreter resolution to prefer platform-appropriate venv Python paths and fall back to `sys.executable`.
- Added new interop regression suites and refreshed stale guard suites after workflow consolidation.

## Files of Note
- `7w_wiki.py`
- `.agent/scripts/update_matrix.py`
- `.agent/scripts/sync_runtime_docs.py`
- `.agent/scripts/generate_tools_manifest.py`
- `System/MCP/generate_mcp_tools.py`
- `System/MCP/server.py`
- `AGENTS.md`
- `System/Synapse_Board/SY_INTEROP.md`
- `System/AGENT_OPERATIONS_HANDBOOK.md`
- `System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md`

## Verification
- `./7w_wiki.py tech --sync-interop`
- `./7w_wiki.py test --suite interop-command-registry`
- `./7w_wiki.py test --suite workflow-matrix-contract`
- `./7w_wiki.py test --suite tool-manifest-contract`
- `./7w_wiki.py test --suite interop-doc-links`
- `./7w_wiki.py test --suite process-dispatch-curiosity`
- `./7w_wiki.py test --suite bridge-placeholder-guard`
- `./7w_wiki.py test --suite all`

## Notes / Risks
- `tools.json` compatibility aliases are intentionally retained for one deprecation cycle; downstream consumers should migrate to structured subcommand tools.
- `Logs/INGESTION_TRACKING_REGISTER.md` and `Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md` changed as part of normal test/stat output refresh during validation.
