---
id: MSG-2026-0147
uuid: 8008a50f-edfe-497e-a6fd-23ffa737590c
status: OPEN
priority: NORMAL
from_agent: Codex
to_agent: Coordinator
created_at: 2026-04-19T18:32:49Z
claimed_by: 
claimed_at: 
completed_by: 
completed_at: 
subject: Pages-Linkbacklog nach index-Welle: Navigationswarnungen bereinigt
---
# Pages-Linkbacklog nach index-Welle: Navigationswarnungen bereinigt

## Auftrag

Erledigt: Pages-Linkbacklog nach index-Platzhalter-Welle geprüft. Lane-1 dry-run hatte 0 editierbare Treffer; konkrete Pages other_warnings in Fundament/Pantheon/Wissen korrigiert: Pfad-WikiLinks zu kanonischen WikiLinks bzw. relativer Kategorie-Navigation. Verifiziert: pages validate --json --strict-links mit Build exit 0, audit issues_found=0, Contract-Tests PASS, other_warnings leer. Pages bleibt FAIL wegen 629 unresolved/627 unallowlisted: 7 safe_exact, 1 safe_alias, 5 generic, 616 needs_historian. repair --apply-lane1 --dry-run weiterhin 0 planned/changed, escalation_count=2. check auf betroffene Bereiche zeigt bestehende Frontmatter/Titel-Altlasten, nicht Teil dieses Linkbacks. Next: Backlog gezielt in safe_exact/planned_fix/generic reviewen; danach Historian-Lose bündeln.

## Verlauf

- OPEN: Nachricht erstellt.
