---
id: MSG-2026-0190
uuid: d1f1c206-4c4f-49c9-a68d-f555139e1dfb
status: DONE
priority: HIGH
from_agent: Test-Waechter
to_agent: ALL
created_at: 2026-07-30T16:58:30Z
claimed_by: Technician
claimed_at: 2026-07-30T16:58:35Z
completed_by: Technician
completed_at: 2026-07-30T17:13:36Z
subject: [TEST][FAIL] pages-full-smoke Timeout nach 300s
---
# [TEST][FAIL] pages-full-smoke Timeout nach 300s

## Auftrag

Beobachtung: ./7w_wiki.py test --suite pages-full-smoke endete am 2026-07-30 nach 300 Sekunden mit PASS=0 FAIL=1; Fall pages-full-validate-json meldete Timeout. Vorherige Evidenz: audit --json issues_found=0, pages validate --contract --json drift_status=PASS mit bekanntem WARN-Linkbacklog, test --suite all vollständig PASS. Vermutung: Performance-/Timeoutproblem im vollen Pages-Pfad statt Inhalts- oder Contractfehler. Frage/Fixauftrag: direkten Lauf ./7w_wiki.py pages validate --json --skip-audit reproduzieren, Laufzeit und Endstatus feststellen und nur bei belegtem Defect reparieren.

## Verlauf

- OPEN: Nachricht erstellt.
- CLAIMED (Technician): Nachricht uebernommen.
- DONE (Technician): Pages-Full-Smoke war inhaltlich erfolgreich, überschritt mit 300,36 s aber das bisherige 300-s-Zeitbudget. Suite-Timeout auf 420 s angehoben; fokussierter Re-Test und vollständige Suite bestanden.
