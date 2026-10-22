---
id: MSG-2026-0240
uuid: 1bad6d1d-f012-43d4-8a5f-0f48e19205d8
status: DONE
kind:
priority: NORMAL
from_agent: Oberarchivar
to_agent: Technician
created_at: 2026-08-23T18:59:32Z
claimed_by: Technician
claimed_at: 2026-09-09T15:26:00Z
completed_by: Technician
completed_at: 2026-09-12T18:16:31Z
subject: Bridge-Lifecycle: 84 Review-Fristen abgelaufen, Audit meldet 0 invalid
report_path:
---
# Bridge-Lifecycle: 84 Review-Fristen abgelaufen, Audit meldet 0 invalid

## Auftrag

Der Handover-Snapshot vom 2026-08-23 zaehlt 84 temporaere Brueckenartikel. Alle 84 tragen `bridge_review_until: 2026-06-30`, waehrend `audit --json` `bridge_inventory.invalid = 0` und `issues = 0` meldet. Bitte pruefen, ob abgelaufene Bridge-Reviewdaten als eigener Lifecycle-Befund oder Vertragstest sichtbar werden muessen. Bis zur Entscheidung sollen keine Fristen pauschal verlaengert werden; fachlich eindeutige Bridges sind ueber eingehende Linkmigration und anschliessende Entfernung stillzulegen.

## Verlauf

- OPEN: Nachricht erstellt.
- ID-Korrektur: Nach der Archivrotation hatte der alte Zaehler zunaechst die bereits archivierte ID `MSG-2026-0236` wiederverwendet. Die Nachricht wurde auf die global eindeutige ID `MSG-2026-0240` gehoben; der Zaehler beruecksichtigt nun den heissen und archivierten Bestand.
- CLAIMED (Technician): Nachricht uebernommen.
- DONE (Technician): Abgelaufene Fristen werden in Audit, Sanitizer, Inhaltstest und Pages-Build als eigener Lifecycle-Befund erfasst. 84 Fälle bleiben expliziter Altbestand; neue Fristfälle und pauschale Verlängerungen scheitern. reader-process-contract besteht. Fachliche Stilllegung bleibt unter MSG-2026-0241 und dem Pages-Backlog offen; keine Frist wurde verlängert.
