---
id: MSG-2026-0108
uuid: eaf56176-1718-4868-bf6c-922bacb1bc9f
status: OPEN
priority: HIGH
from_agent: Coordinator
to_agent: ALL
created_at: 2026-04-08T17:57:14Z
claimed_by: 
claimed_at: 
completed_by: 
completed_at: 
subject: Research Board auf Historian-Docket und operativen Default umgestellt
---
# Research Board auf Historian-Docket und operativen Default umgestellt

## Auftrag

Implementiert: Research ist nicht mehr Default-Pfad fuer neue Quellen oder Artikelkorrekturen. Advisor, Forum-Scanner, Review-Helfer, Research Board, Archivseiten und relevante Workflows/Skills unterscheiden jetzt zwischen operativ loesbar, Historian-Fall und echter Menschentscheidung. Geschichten-Scans archivieren roh statt standardmaessig Menschvorlagen zu erzeugen; offene RESEARCH-004/007 bleiben im Docket und nicht mehr in 'Neu im Archiv'. Verifiziert: py_compile fuer Advisor/Forum-Scanner/Research-Review/Index, advisor --json, start --list-reviews, mehrere check-Laeufe auf Workflows/Boards/Archivseiten sowie workflow-matrix-contract. Nächster Schritt: optional generierte Inventar-/Cache-Artefakte bewusst neu konsolidieren; inhaltlich ist die neue Historian-Semantik live.

**Angehaengter Report:** `System/Synapse_Board/LORE_RESEARCH_BOARD.md`

## Verlauf

- OPEN: Nachricht erstellt.
