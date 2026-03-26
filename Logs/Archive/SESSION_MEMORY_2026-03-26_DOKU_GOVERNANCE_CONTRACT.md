# Session Memory: Doku Governance Contract

- Date: 2026-03-26
- Focus: Zentraler Drift-/Pages-Vertrag, Workflow-Referenzen, Task-Status und Doku-Konsistenz

## Context
- Die Doku war zwar bereits teilweise auf `Homepage > Quellen > Wiki Pages` und `docs/Siebenwind_Wiki/` ausgerichtet, aber die Regeln waren noch mehrfach verteilt.
- Mehrere Workflows und Governance-Dokumente enthielten Redundanzen oder alte Referenzen, darunter ein veralteter Handover-Skriptpfad und uneinheitliche `pages validate`-Formulierungen.
- Ziel war eine kanonische Vertrauensquelle fuer Drift, Pages-Integritaet und Praezedenz, auf die die anderen Dokumente nur noch kurz verweisen.

## What Changed
- Neu angelegt: [System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md](/Users/alexandrerabe/siebenwind/7w_wiki/System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md) als zentrale Vertragsquelle.
- Aktualisiert: [AGENTS.md](/Users/alexandrerabe/siebenwind/7w_wiki/AGENTS.md), [System/AGENT_OPERATIONS_HANDBOOK.md](/Users/alexandrerabe/siebenwind/7w_wiki/System/AGENT_OPERATIONS_HANDBOOK.md), [System/Synapse_Board/SY_INTEROP.md](/Users/alexandrerabe/siebenwind/7w_wiki/System/Synapse_Board/SY_INTEROP.md), [System/Synapse_Board/SY_TESTING.md](/Users/alexandrerabe/siebenwind/7w_wiki/System/Synapse_Board/SY_TESTING.md), [System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md](/Users/alexandrerabe/siebenwind/7w_wiki/System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md), [.agent/workflows/start.md](/Users/alexandrerabe/siebenwind/7w_wiki/.agent/workflows/start.md), [.agent/workflows/tech_master.md](/Users/alexandrerabe/siebenwind/7w_wiki/.agent/workflows/tech_master.md), [.agent/workflows/qa_master.md](/Users/alexandrerabe/siebenwind/7w_wiki/.agent/workflows/qa_master.md), [.agent/workflows/handover.md](/Users/alexandrerabe/siebenwind/7w_wiki/.agent/workflows/handover.md), [MASTER_TASK_LIST.md](/Users/alexandrerabe/siebenwind/7w_wiki/MASTER_TASK_LIST.md), [System/COORDINATION_HUB.md](/Users/alexandrerabe/siebenwind/7w_wiki/System/COORDINATION_HUB.md).
- Entfernt: mehrere altezzeitige `updated_at`-Header in Governance-Dokumenten, weil sie keinen belastbaren Wartungsnutzen mehr hatten.
- Der Handover-Workflow verweist jetzt auf `.agent/scripts/` statt auf den alten `wiki_schmied`-Pfad.
- `pages validate --json --strict-links` ist nun auch in den Workflow-Texten klar als harter Gate-Modus beschrieben; `--strict` wird nicht mehr als unklare Ersatzform verwendet.
- `MASTER_TASK_LIST.md` markiert den Drift-/Pages-Governance-Abgleich jetzt als erledigt und verweist auf den neuen Vertrag.

## Verification
- `./7w_wiki.py test --suite interop-doc-links` PASS
- `./7w_wiki.py test --suite workflow-matrix-contract` PASS
- `./7w_wiki.py test --suite pages-link-contract` teilweise gruen, aber `audit-pages-json` faellt an einem Audit-JSON-Formatproblem
- `./7w_wiki.py test --suite takeover-handover` faellt an einer `ERGEBNIS:`-Erwartung im Audit-Reporting-Check
- `./7w_wiki.py pages validate --json --skip-audit` PASS mit `WARN`-Status auf der bestehenden Site-Drift-Lage

## Open Points
- Die Restfehler in `pages-link-contract` und `takeover-handover` sind keine Doku-Konflikte mehr, sondern Runtime-/Audit-Formatfragen.
- Die Seiten- und Quellen-Altlasten im Wiki-Bestand bleiben bestehen und muessen getrennt von der Doku-Konsolidierung bearbeitet werden.
