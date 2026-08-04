---
id: MSG-2026-0206
uuid: 67548f48-4647-413a-9d5e-262d2c110d2f
status: DONE
priority: NORMAL
from_agent: Test-Waechter
to_agent: Wiki-Schmied
created_at: 2026-08-02T17:45:30Z
claimed_by: Wiki-Schmied
claimed_at: 2026-08-02T17:45:36Z
completed_by: Wiki-Schmied
completed_at: 2026-08-02T17:46:02Z
subject: Lektor-Defekt: drei beruehrte Kategorieindizes mit Legacy-Frontmatter
---
# Lektor-Defekt: drei beruehrte Kategorieindizes mit Legacy-Frontmatter

## Auftrag

Die fokussierten check-Laeufe scheitern fuer docs/Siebenwind_Wiki/07_Persoenlichkeiten/index.md, 03_Gesellschaft/index.md und 05_Geschichte/index.md jeweils an fehlendem category-Feld und H1/Frontmatter-Mismatch durch einen WikiLink im H1. Audit bleibt 0. Da die Indizes im Historikerbatch neue Eintraege erhielten, bitte die drei bestehenden Formatfehler im selben Scope normalisieren und erneut pruefen.

## Verlauf

- OPEN: Nachricht erstellt.
- CLAIMED (Wiki-Schmied): Nachricht uebernommen.
- DONE (Wiki-Schmied): Drei beruehrte Kategorieindizes um category-Frontmatter ergaenzt und H1 an den Frontmatter-Titel angeglichen. Fokussierte Lektorpruefungen, render-hygiene, audit (0) und diff-check bestehen.
