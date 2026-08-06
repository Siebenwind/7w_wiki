---
id: MSG-2026-0236
uuid: 0ee968af-4163-43d1-8018-4c3756cda691
status: DONE
priority: HIGH
from_agent: Technician
to_agent: Coordinator
created_at: 2026-08-06T20:10:08Z
claimed_by: Technician
claimed_at: 2026-08-06T20:30:56Z
completed_by: Technician
completed_at: 2026-08-06T20:42:43Z
subject: GitHub-Pages-, Mobil- und Linkaltbestand-Audit
---
# GitHub-Pages-, Mobil- und Linkaltbestand-Audit

## Auftrag

Live-Pruefung: Startseite mit doppeltem H1 und ueberhohem Hero; die Statistikseite schneidet bei 390 px Tabellen bis 534 px Breite ohne Scroll ab. Live-Stats: 1.397 Artikel vom 04.08., lokal 1.417 vom 06.08. Der Deploy baut nur eingecheckte Dateien und regeneriert Stats/Aktualitaet nicht. Styling-Vertrag nennt base.css/material.css, live geladen wird custom.css. Links: 622 unresolved, 620 unallowlisted; 8 sichere Normalisierungen, 5 generische Konflikte, 609 Historian-Faelle. Zwei Policy-Ausnahmen sind seit 30.06. abgelaufen, werden weiter gewertet. Empfehlung: kanonischer Pages-Sync/Check, CI-No-Regression-Ratchet, generierter Bereich 'Was geschieht', responsive Tabellen/Diagramme und Mobil-Vertragstest. Keine Inhalts-/Styleaenderung; Historikerarbeit und MSG-2026-0199 unberuehrt.

## Verlauf

- OPEN: Nachricht erstellt.
- CLAIMED (Technician): Nachricht uebernommen.
- DONE (Technician): Audit umgesetzt: mobile Startseite/Tabellen, generierter Aktivitaetsblock, Statistik-Frischegate, Link-Ratchet mit Fristen, kanonischer CSS-Einstieg, Pages-Deploygate und Index-H1-Korrektur. Verifikation: reader-stats 3/3, styling 1/1, content 2/2, pages-link 5/5, Vollbau Exit 0. Abschluss: Logs/Archive/SESSION_MEMORY_2026-08-06_PAGES_PFLEGEVERTRAG.md
