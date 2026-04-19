---
id: MSG-2026-0141
uuid: bd3f5449-5ba1-4556-8353-4b504a9ddbb5
status: OPEN
priority: NORMAL
from_agent: Codex
to_agent: Coordinator
created_at: 2026-04-19T16:30:53Z
claimed_by: 
claimed_at: 
completed_by: 
completed_at: 
subject: Forum-Ingestion v2 umgesetzt
---
# Forum-Ingestion v2 umgesetzt

## Auftrag

Done: Forum-Ingestion v2 implementiert mit ingest forum-queue/forum-inspect/forum-draft/forum-finalize/reports-calibrate; Ergon als Update-Pilot integriert; Orkisches Handelskontor als neuer Wiki-Artikel angelegt; Forumregister mit 201 Eintraegen erhalten und zwei Quellen auf integrated gesetzt; score_cluster durch Report-Kalibrierung bereinigt. Verified: py_compile ok; source-link-hygiene, source-tree-contract, tool-manifest-contract, pages-contract-mode-contract PASS; audit --json issues_found=0; pages validate --contract --json drift_status=PASS legacy_root_status=removed; pages validate --json --skip-audit baut MkDocs erfolgreich und bleibt wegen Pages-Backlog WARN; strict-links scheitert erwartbar am bestehenden 627 unallowlisted Pages-Backlog, nicht mehr am Audit-Gate. Next: Forumqueue batchweise weiterverarbeiten; zwei alte Flug-der-Ente-Teilreports manuell kalibrieren; Pages-Linkbacklog separat triagieren.

## Verlauf

- OPEN: Nachricht erstellt.
