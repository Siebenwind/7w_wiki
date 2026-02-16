---
uuid: 6e2e53f0-66ce-4a87-bb24-17ca4f5f2f11
status: ACTIVE
updated_at: 2026-02-16T21:35:00Z
---

# SY_DISPATCH

Inter-agent messaging uses the existing Synapse-Board domain via:

- `System/Synapse_Board/DISPATCH/`

Each dispatch file is a markdown document with frontmatter and lifecycle state.

## Commands

- `./7w_wiki.py mail post --from <agent> --to <agent|ALL> --subject "<text>" --body "<text>" [--priority LOW|NORMAL|HIGH]`
- `./7w_wiki.py mail inbox [--agent <name>] [--status OPEN|CLAIMED|DONE]`
- `./7w_wiki.py mail read <MSG-YYYY-NNNN>`
- `./7w_wiki.py mail claim <MSG-YYYY-NNNN> --agent <name>`
- `./7w_wiki.py mail done <MSG-YYYY-NNNN> --agent <name> [--note "<abschluss>"]`

## Conventions

- Timestamp format: ISO-8601 UTC with `Z`.
- Every dispatch has a UUID.
- `to_agent: ALL` is a broadcast.
- Status transitions:
  - `OPEN` -> `CLAIMED` -> `DONE`

## Operational Guardrails

1. Claims are exclusive: a `CLAIMED` message is owned by `claimed_by`.
2. `DONE` requires prior claim and must be finalized by the claimer.
3. Message IDs are exact (`MSG-YYYY-NNNN`), not prefix-matched.
4. Inbox filtering uses strict status values (`OPEN|CLAIMED|DONE`).
5. Decision requests should be routed through Dispatch and link to referenced Conflict/Research tickets.

## Implementation Proposal (Documented)

1. Harden `agent_mail.py` with a strict state machine (`OPEN -> CLAIMED -> DONE`).
2. Enforce exact ID lookup by frontmatter `id`.
3. Ensure post creation is collision-safe under concurrent runs.
4. Append explicit lifecycle log lines for `CLAIMED` and `DONE` in `## Verlauf`.
5. Align `/decide` workflow to consume Dispatch first, then update linked domain tickets.
