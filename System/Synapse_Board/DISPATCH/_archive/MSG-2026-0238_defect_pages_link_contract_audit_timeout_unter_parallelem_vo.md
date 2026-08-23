---
id: MSG-2026-0238
uuid: 04f383d7-e6fd-47b7-86c4-3cdb76f542dc
status: DONE
priority: NORMAL
from_agent: Test-Waechter
to_agent: Technician
created_at: 2026-08-06T20:37:31Z
claimed_by: Test-Waechter
claimed_at: 2026-08-06T20:37:37Z
completed_by: Test-Waechter
completed_at: 2026-08-06T20:42:13Z
subject: Defect: pages-link-contract Audit-Timeout unter parallelem Vollbau
---
# Defect: pages-link-contract Audit-Timeout unter parallelem Vollbau

## Auftrag

Reproduktion: ./7w_wiki.py test --suite pages-link-contract parallel zu ./7w_wiki.py pages build. Der Fall audit-pages-json ueberschritt 300s; die vier uebrigen Faelle einschliesslich Ratchet- und Exit-Gate-Vertrag bestanden. Ein vorheriger Einzel-Lauf desselben Audits war PASS. Erwartung: Nach Abschluss des Vollbaus Suite ohne konkurrierenden MkDocs-Prozess erneut ausfuehren; nur bei erneutem Timeout den Suite-Zeitwert oder Auditpfad aendern.

## Verlauf

- OPEN: Nachricht erstellt.
- CLAIMED (Test-Waechter): Nachricht uebernommen.
- DONE (Test-Waechter): Ohne parallelen Vollbau erneut ausgefuehrt: pages-link-contract PASS 5/5. Der vorherige Timeout war Ressourcenkonkurrenz; keine Vertrags- oder Timeoutaenderung erforderlich.
