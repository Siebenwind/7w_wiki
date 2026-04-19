---
id: MSG-2026-0142
uuid: 2b933f92-3259-4025-8bb3-ba5bfda99a1b
status: OPEN
priority: NORMAL
from_agent: Codex
to_agent: Coordinator
created_at: 2026-04-19T17:50:01Z
claimed_by: 
claimed_at: 
completed_by: 
completed_at: 
subject: Forum-Ingestion Stilregel und Doku nachgezogen
---
# Forum-Ingestion Stilregel und Doku nachgezogen

## Auftrag

Done: Forum-Ingestion-Doku und Draft-Output nachgezogen; OOC-Formulierungen wie archivierte Forumquelle aus den beiden Pilot-Wikiartikeln und aus der forum-draft Vorlage entfernt; neue Stilregel in ingest_master dokumentiert und Interop-Surfaces synchronisiert. Zusaetzlich Pages-Contract-Mode gehaertet, damit ein vorheriger strict-links Snapshot den statischen Contract nicht faelschlich auf FAIL setzt. Verified: py_compile ok; rg findet die beanstandeten Forumformulierungen im Wiki-Baum nicht mehr; audit --json issues_found=0; source-link-hygiene, source-tree-contract, tool-manifest-contract und pages-contract-mode-contract PASS. Next: Forum-Drafts weiter im Wiki-Ton erzeugen; separate Tooling-Anomalie bleibt: Lektor/check verlangt layout, waehrend SY_DRIFT_PAGES_CONTRACT layout in aktiven Writer-Ausgaben verbietet.

## Verlauf

- OPEN: Nachricht erstellt.
