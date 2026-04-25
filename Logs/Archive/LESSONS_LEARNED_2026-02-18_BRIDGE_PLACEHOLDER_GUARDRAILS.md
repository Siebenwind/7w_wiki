# Lessons Learned: Bridge-Placeholder Guardrails

Datum: 2026-02-18
Kontext: Praevention von "Brueckenartikel statt echter Link-Reparatur"

## Kernerkenntnisse
- Link-Fixes muessen kanonische Ziele priorisieren; Placeholder-Seiten verschieben das Problem nur.
- Policy alleine reicht nicht: Guardrails muessen als testbare Suite und als Audit-Metrik vorliegen.
- Ohne Ausnahme-Metadaten bleiben temporaere Bruecken unsichtbar und werden schnell zu Dauerzustand.

## Messstand
- Audit Report: `Logs/Archive/Audit_f5c0c076-73e9-48c5-a127-cae689633d0d.txt`
- Bridge-/Placeholder-Seiten erkannt: 89
- Mit Ausnahme-Metadaten (`bridge_mode`, `bridge_target`, `bridge_ticket`, `bridge_review_until`): 0
- Neue Policy-Suite: `bridge-placeholder-guard` PASS

## Verbindliche Guardrails
1. Keine generischen Brueckenartikel als Standard-Fix.
2. Rewrite auf kanonisches Ziel vor Neuanlage.
3. Temporäre Bruecken nur mit Ablaufmetadaten und Ticket.
4. Vor Abschluss: `./7w_wiki.py test --suite bridge-placeholder-guard`.

## Empfehlung fuer Folgeagenten
- Bestehende 89 Bridge-Seiten schrittweise abbauen: pro Batch 10-20 Seiten auf Zielseite umhaengen oder sauber als temporaere Ausnahme markieren.
- Jede Ausnahme mit Dispatch-ID und Review-Datum versehen.
