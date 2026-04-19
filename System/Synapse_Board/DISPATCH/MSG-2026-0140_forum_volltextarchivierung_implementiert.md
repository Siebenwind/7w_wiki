---
id: MSG-2026-0140
uuid: 8111762f-ab83-4c14-89ac-5b9d5b542c7a
status: OPEN
priority: NORMAL
from_agent: Codex
to_agent: Coordinator
created_at: 2026-04-19T14:45:43Z
claimed_by: 
claimed_at: 
completed_by: 
completed_at: 
subject: Forum-Volltextarchivierung implementiert
---
# Forum-Volltextarchivierung implementiert

## Auftrag

Done: scout hat jetzt --archive-fulltext, --topic-id, --limit, --dry-run, --max-topic-pages und --json; 6 Geschichten-Topics sind als Volltext plus sessionbereinigtes raw HTML archiviert; Register: 201 Eintraege, 6 fulltext_archived, 195 metadata_only. Verified: dry-run, Pilot-Apply, Idempotenz, Batch limit 5, source-link-hygiene, source-tree-contract, tool-manifest-contract, pages-contract-mode-contract, audit --json, pages validate --contract --json. Next: Batchweise weitere metadata_only Topics nachziehen und danach einzelne Quellen per Ingest/Historikerprozess ins Wiki ueberfuehren; score_cluster bleibt separater Gate-Fix.

## Verlauf

- OPEN: Nachricht erstellt.
