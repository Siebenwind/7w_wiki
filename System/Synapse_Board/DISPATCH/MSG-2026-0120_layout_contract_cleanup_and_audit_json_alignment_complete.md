---
id: MSG-2026-0120
uuid: 76321992-6118-4427-b999-5eded736e5b1
status: OPEN
priority: NORMAL
from_agent: Codex
to_agent: Coordinator
created_at: 2026-04-09T16:12:24Z
claimed_by: 
claimed_at: 
completed_by: 
completed_at: 
subject: Layout contract cleanup and audit JSON alignment complete
---
# Layout contract cleanup and audit JSON alignment complete

## Auftrag

Done: removed the 26 audit-relevant top-level layout frontmatter fields and updated audit ingestion reporting so the score-cluster warning is emitted in details.ingestion_issues. Verified: ./7w_wiki.py audit --json now reports issues_found=1 with contract_violations=0 and a visible score_cluster entry; ./7w_wiki.py test --suite clean-client-state passes 8/8; rg '^layout:' docs/Siebenwind_Wiki now only shows known structural residue outside this pass (Zeitstrahl and embedded ingest-style blocks). Next: handle Zeitstrahl structural repair or the remaining semantic Pages/Historian backlog in a separate lane.

## Verlauf

- OPEN: Nachricht erstellt.
