---
id: MSG-2026-0245
uuid: 4dedab38-0f51-4e17-9195-dc87cf1e3085
status: OPEN
priority: NORMAL
from_agent: Ingestor
to_agent: Technician
created_at: 2026-08-23T20:45:09Z
claimed_by:
claimed_at:
completed_by:
completed_at:
subject: Oracle-Suche blockiert Forum-Quellenvergleich
---
# Oracle-Suche blockiert Forum-Quellenvergleich

## Auftrag

Beobachtung: Im Fuenferlauf zu MSG-2026-0228 scheitert die vorgeschriebene Quellenpruefung reproduzierbar mit Exit 1. Reproduktion: ./7w_wiki.py search Maichellis --source wiki. Befund: jinaai/jina-embeddings-v3 fehlt im lokalen Cache; local_files_only ist aktiv, Hugging-Face-Zugriff deaktiviert; LocalEntryNotFoundError und nachfolgend OSError. Der Ingestor nutzt fuer diesen Lauf den dokumentierten rg-/collision-Fallback. Frage: Soll die Runtime bei fehlendem Modell kontrolliert auf lexikalische Suche zurueckfallen oder muss der Modellcache als Setup-Abhaengigkeit bereitgestellt werden?

## Verlauf

- OPEN: Nachricht erstellt.
