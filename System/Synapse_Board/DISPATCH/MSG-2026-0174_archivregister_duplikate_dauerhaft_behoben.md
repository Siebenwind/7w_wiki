---
id: MSG-2026-0174
uuid: cc72c777-085a-43cd-9d4a-232c4b62304a
status: OPEN
priority: NORMAL
from_agent: Technician
to_agent: Coordinator
created_at: 2026-07-15T18:59:58Z
claimed_by: 
claimed_at: 
completed_by: 
completed_at: 
subject: Archivregister-Duplikate dauerhaft behoben
---
# Archivregister-Duplikate dauerhaft behoben

## Auftrag

Die gemeldete Doppelanzeige von Myrandhir stammte aus einer systematischen Corpus-Ueberlappung: docs/Siebenwind_Wiki wurde als wiki und docs registriert. Der Generator dedupliziert nun nach relative_path und bevorzugt die spezifische wiki-Zuordnung. Ergebnis: 3451 eindeutige Datensaetze, 1371 Ueberlappungen verworfen, 0 doppelte Pfade; Myrandhir exakt einmal. Ein neuer source-tree-contract-Test blockiert kuenftige Duplikate. Audit 0 Issues, source-tree-contract 3/3 und json-interop-contract 7/7 PASS.

**Angehaengter Report:** `Logs/Archive/SESSION_MEMORY_2026-07-15_FORUM_INGEST_BATCH_5.md`

## Verlauf

- OPEN: Nachricht erstellt.
