---
uuid: eff887fc-dbee-4ae5-82e2-b105c4d608de
status: ACTIVE
created_at: 2026-02-17T23:30:02Z
epistemic: "#meta"
---

# Agent Dossier: Bridge Rewrite Program

## Zweck
Repository-weite Leitlinie fuer alle Agenten zur Vermeidung von "Brueckenartikel statt echter Reparatur".

## Lagebild (Stand 2026-02-18)
- Audit: `Logs/Archive/Audit_9fb6318b-4048-4f5d-be61-a94bb5b54aa2.txt`
- Gesamtprobleme: 437
- Bridge-/Placeholder-Seiten erkannt: 89
- Davon mit Ausnahme-Metadaten: 0
- Davon ohne Ausnahme-Metadaten: 89
- Wiki-Statistik: `Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md`
  - Artikel: 1360
  - Worte: 188405
  - Personen: 586
  - Ingestion-Reports: 54
  - Tracking vollstaendig: 50

## Verbindliche Policy (alle Agenten)
1. Rewrite-first: Link auf kanonisches Ziel reparieren, keine Placebo-Seite erzeugen.
2. Neue Seite nur mit belastbarer Quelle (`quelle:` relativ, nicht Blindwert).
3. Temporaere Bridge nur mit allen Feldern:
   - `bridge_mode: temporary`
   - `bridge_target: [[...]]`
   - `bridge_ticket: MSG-...` oder Task-ID
   - `bridge_review_until: YYYY-MM-DD`
4. Abschluss ohne Guard nicht zulaessig:
   - `./7w_wiki.py test --suite bridge-placeholder-guard`
   - `./7w_wiki.py audit`

## Rollenauftrag
- Guardian:
  - Fuehrt Batch-Audits und Link-Rewrites.
  - Markiert/verhindert neue Bridge-Seiten ohne Metadaten.
- Ingestor:
  - Liefert fehlende Quellenzuordnung fuer betroffene Seiten.
  - Meldet unklare Faelle als Spezialistenfrage via Dispatch.
- Historian:
  - Klaert Namens-/Alias-Konflikte fuer kanonisches Zielrouting.
- Coordinator:
  - Priorisiert Batches und verfolgt KPI-Delta pro Batch.
  - Sichert Session-Memory + Changelog/Task-Verweise.
- Technician:
  - Haelt Test-Suiten und Audit-Regeln reproduzierbar und hart.

## Batch-Plan (operativ)
1. Batchgroesse: 10-20 Bridge-Seiten pro Lauf.
2. Pro Seite:
   - Zielseite ermitteln und Links umhaengen.
   - Wenn unklar: temporaere Ausnahme sauber metadatiert + Ticket.
3. Nach jedem Batch:
   - `./7w_wiki.py test --suite bridge-placeholder-guard`
   - `./7w_wiki.py audit`
   - Delta dokumentieren (Bridge ohne Metadaten, Gesamtprobleme).

## KPI-Tracking
- KPI-1: `bridge_without_exception` (Startwert 89, **Aktuell 79**, Ziel 0)
- KPI-2: `audit_total_problems` (Startwert 437, Ziel sinkend pro Batch)
- KPI-3: `tracking_complete_reports` (Startwert 50/54, Ziel 54/54)

## Batch-Historie
- **Batch 1 (2026-02-18)**: 10 Core-Bridges (Vitama, Rien, Adel, Gesellschaft etc.) repariert. 64 Repo-weite Linkfixes.

## Validierung (aktuelle Suite-Reports)
- `Logs/Archive/TEST_bridge-placeholder-guard_2026-02-18_002720.md` (PASS)
- `Logs/Archive/TEST_process-dispatch-curiosity_2026-02-18_002734.md` (PASS)
- `Logs/Archive/TEST_source-link-hygiene_2026-02-18_002739.md` (PASS)
- `Logs/Archive/TEST_clean-client-state_2026-02-18_002821.md` (PASS)
