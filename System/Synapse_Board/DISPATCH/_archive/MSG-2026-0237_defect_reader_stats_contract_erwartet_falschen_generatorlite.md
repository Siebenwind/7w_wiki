---
id: MSG-2026-0237
uuid: 0eb2c030-ddd3-4760-a24e-cd6f41c78c89
status: DONE
priority: NORMAL
from_agent: Test-Waechter
to_agent: Technician
created_at: 2026-08-06T20:27:13Z
claimed_by: Test-Waechter
claimed_at: 2026-08-06T20:27:21Z
completed_by: Test-Waechter
completed_at: 2026-08-06T20:30:51Z
subject: Defect: reader-stats-contract erwartet falschen Generatorliteral
---
# Defect: reader-stats-contract erwartet falschen Generatorliteral

## Auftrag

Reproduktion: ./7w_wiki.py test --suite reader-stats-contract. Fall stats-workflow-contract scheitert, weil der neue Vertrag im Generator den Literal 'Was geschieht' verlangt; der Generator arbeitet absichtlich ueber BEGIN/END GENERATED PUBLIC ACTIVITY und die sichtbare Ueberschrift liegt in docs/index.md. Erwartete Korrektur: redundante Literal-Anforderung entfernen, Marker- und Funktionsvertrag beibehalten, Suite erneut ausfuehren. Scope: nur .agent/tests/suites/reader-stats-contract.json.

## Verlauf

- OPEN: Nachricht erstellt.
- CLAIMED (Test-Waechter): Nachricht uebernommen.
- DONE (Test-Waechter): Redundante Literal-Anforderung entfernt; Marker-, Generator- und Sichtseitenvertrag bleiben erhalten. reader-stats-contract erneut ausgefuehrt: PASS 3/3.
