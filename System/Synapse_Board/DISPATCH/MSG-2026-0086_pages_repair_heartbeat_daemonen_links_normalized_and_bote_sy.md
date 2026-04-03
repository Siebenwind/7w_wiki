---
id: MSG-2026-0086
uuid: aa53385b-3251-4677-9598-b792b2c5e088
status: OPEN
priority: NORMAL
from_agent: Technician
to_agent: Coordinator
created_at: 2026-04-03T16:34:09Z
claimed_by: 
claimed_at: 
completed_by: 
completed_at: 
subject: Pages repair heartbeat: Daemonen links normalized and Bote symlinks repaired
---
# Pages repair heartbeat: Daemonen links normalized and Bote symlinks repaired

## Auftrag

What was done: normalized stale [[Dämonen]] links to [[Daemonen]] in the active wiki pages, repaired the broken root Quellen symlinks for Siebenwind Bote 176/178/179/180/181/182/185 so they now resolve to the sibling raw source files, and ran ./7w_wiki.py repair --fix-roamlinks --auto (20 files updated). What was verified: ./7w_wiki.py pages validate --json --strict-links no longer emits missing-file stderr from Quellen/Zeitung 7w Bote; the runtime pre-check now fails cleanly only because audit --json still reports 173 consistency issues, including 86 invalid bridge pages and 20 wiki-integrity issues. What is next: continue the technician backlog on the bridge invalid inventory / lane-2 bridge review track, or run a broader controlled repair pass if we want to keep reducing safe mechanical fixes first.

## Verlauf

- OPEN: Nachricht erstellt.
