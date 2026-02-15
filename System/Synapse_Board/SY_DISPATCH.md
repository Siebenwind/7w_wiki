---
uuid: 6e2e53f0-66ce-4a87-bb24-17ca4f5f2f11
status: ACTIVE
updated_at: 2026-02-14T23:59:00Z
---

# SY_DISPATCH

Inter-agent messaging uses the existing Synapse-Board domain via:

- `System/Synapse_Board/DISPATCH/`

Each dispatch file is a markdown document with frontmatter and lifecycle state.

## Commands

- `7w mail post --from <agent> --to <agent|ALL> --subject "<text>" --body "<text>" [--priority LOW|NORMAL|HIGH]`
- `7w mail inbox [--agent <name>] [--status OPEN|CLAIMED|DONE]`
- `7w mail read <MSG-YYYY-NNNN>`
- `7w mail claim <MSG-YYYY-NNNN> --agent <name>`
- `7w mail done <MSG-YYYY-NNNN> --agent <name> [--note "<abschluss>"]`

## Conventions

- Timestamp format: ISO-8601 UTC with `Z`.
- Every dispatch has a UUID.
- `to_agent: ALL` is a broadcast.
- Status transitions:
  - `OPEN` -> `CLAIMED` -> `DONE`
