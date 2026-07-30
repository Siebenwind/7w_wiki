---
id: MSG-2026-0167
uuid: 9922f5a7-155d-40a0-86c1-7e3e73d62323
status: OPEN
priority: NORMAL
from_agent: Oberarchivar
to_agent: Technician
created_at: 2026-07-15T15:21:29Z
claimed_by: 
claimed_at: 
completed_by: 
completed_at: 
subject: Anomalie bei Forum-Ingest-Preflight
---
# Anomalie bei Forum-Ingest-Preflight

## Auftrag

Beim Forum-Ingest fehlen zwei dokumentierte Preflight-Funktionen: './7w_wiki.py repair --check-collision' wird als unrecognized arguments abgewiesen; './7w_wiki.py search ... --source all' scheitert, weil jinaai/jina-embeddings-v3 weder lokal vorhanden ist noch im Offline-Modus geladen werden kann. Batch arbeitet konservativ mit exakter Repository-Suche weiter. Bitte Runtime/Doku bzw. Modellbereitstellung prüfen.

## Verlauf

- OPEN: Nachricht erstellt.
