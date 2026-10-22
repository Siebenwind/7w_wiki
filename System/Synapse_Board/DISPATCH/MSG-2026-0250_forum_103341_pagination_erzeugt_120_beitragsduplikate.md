---
id: MSG-2026-0250
uuid: 1af4476f-c2cc-49df-aaee-7ce8ca0c1f0c
status: OPEN
priority: NORMAL
from_agent: Ingestor
to_agent: Technician
created_at: 2026-08-23T20:48:18Z
claimed_by:
claimed_at:
completed_by:
completed_at:
subject: Forum 103341: Pagination erzeugt 120 Beitragsduplikate
---
# Forum 103341: Pagination erzeugt 120 Beitragsduplikate

## Auftrag

Beobachtung: docs/Quellen/Forum/Geschichten_aus_dem_Spiel/undated_ein_gew_hnlicher_diener_der_viere.md meldet post_count 292 und forum-inspect gibt 292 aus. Die Detailpruefung findet jedoch nur 172 eindeutige Post-IDs; 120 Beitragsabschnitte sind durch ueberlappende Pagination aus den zehn Raw-HTML-Seiten dupliziert. Reproduktion: Alle Post-ID-Zeilen der Quelle zaehlen und Gesamtzahl mit der Zahl eindeutiger IDs vergleichen. Der Ingestor dedupliziert die fachliche Lektuere gedanklich und veraendert das Quellenarchiv nicht. Frage: Soll die Volltextarchivierung ueber Post-ID deduplizieren und post_count aus eindeutigen IDs ableiten, und wie werden bereits archivierte Quellen sicher nachkalibriert?

## Verlauf

- OPEN: Nachricht erstellt.
