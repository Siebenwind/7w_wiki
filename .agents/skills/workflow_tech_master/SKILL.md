---
name: Workflow Tech Master
description: Codex-native maintenance adapter for interop sync, pages health, and runtime hygiene.
---

# Codex Skill: Workflow Tech Master

> **Canonical workflow**: `.agent/workflows/tech_master.md`
> **Marker**: Generated Codex adapter skill. Do not edit manually.

This adapter is generated from the canonical catalog. Runtime execution stays on `./7w_wiki.py`; `.agent/` remains the source of truth.

## Primary Runtime Command
`./7w_wiki.py tech --sync-surfaces`

## Follow-up Commands
- `./7w_wiki.py tech --sync-interop`
- `./7w_wiki.py pages validate --json`
- `./7w_wiki.py audit --pages`

## Instructions
- Use this adapter for runtime-authoritative maintenance work: docs sync, adapter generation, pages integrity, and CLI surface hygiene.
- Prefer ./7w_wiki.py tech --sync-surfaces for the full surface refresh. --sync-bridges remains compatibility-only.
- Treat GitHub Pages and Codex integration as derived UX layers; keep .agent plus ./7w_wiki.py authoritative.

## References
- `.agent/workflows/tech_master.md`
- `System/Synapse_Board/SY_INTEROP.md`
- `System/MCP/README.md`
