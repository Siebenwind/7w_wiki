---
report_id: INGEST-AUDIT-2026-02-14-WORKFLOWS
uuid: 8dc5f1cc-44ef-46b5-b95f-9d3f9f40128f
date: 2026-02-14T23:59:00Z
author: Netz-Waechter
scope:
  - .agent/workflows/*.md
  - .agent/instructions/*.md
  - System/COORDINATION_HUB.md
  - 7w_wiki.py
status: completed
epistemic: "#meta"
---

# Workflow & Instruction Ingest Audit

## Ergebnislage
- Gepruefte Workflows: `30`
- Gepruefte Persona-Instruktionen: `4`
- Feststellung: Governance vorhanden, aber teils von der aktuellen Runtime (`7w_wiki.py`) entkoppelt.

## Kritische Findings (P1)
- Massive Nutzung absoluter `file://` Links in Workflows und Hub, trotz eigener Regel "keine absoluten Pfade".
  - Belege: `.agent/workflows/start.md:14`, `.agent/workflows/handover.md:48`, `.agent/workflows/docs.md:10`, `System/COORDINATION_HUB.md:20`
- Referenzierte Kernartefakte fehlen im Repo.
  - `Logs/INVENTUR_QUELLEN.md` (mehrfach referenziert, nicht vorhanden)
  - `Logs/INGESTION_LOG.md` (mehrfach referenziert, nicht vorhanden)
  - `Logs/Konsistenzbericht_2026.md` (mehrfach referenziert, nicht vorhanden)
  - `WORKFLOW_LORE_CONSISTENCY.md` (referenziert, nicht vorhanden)
  - `SY_BULLETIN.md` (im Hub referenziert, nicht vorhanden)

## Hohe Findings (P2)
- Workflow-Befehle und echte CLI divergieren.
  - In Workflows prominent: `/batch`, `/ingestion_protocol`, `/check_master`, `/lore_master`, `/meta_master`, `/decide`, `/watch`, `/contrib_audit`, `/takeover`, `/translate`
  - In `7w_wiki.py` implementiert: `advisor`, `audit`, `historian`, `index`, `index-pages`, `mail`, `repair`, `search`, `start`, `stats`
  - Beleg: `7w_wiki.py:59-94`
- Tooling-Hinweise enthalten nicht vorhandene Funktionen im aktuellen Agent-Stack.
  - `notify_user` und `multi_replace_file_content` sind in Workflows genannt, aber hier nicht verfuegbar.
  - Belege: `.agent/workflows/meta_master.md:26`, `.agent/workflows/ingestion_protocol.md:77`
- Historiker-Persona verweist auf `REVIEW_BOARD.md`, waehrend das aktive Board `SY_REVIEW.md` ist.
  - Beleg: `.agent/instructions/persona_historian.md:21`

## Mittlere Findings (P3)
- Widerspruch in Stilregeln:
  - Guardian fordert keine `file://` Pfade (`persona_guardian.md`),
  - `wiki_style_guide.md` empfiehlt fuer externe/sources absolute `file:///absolute/path/...`.
  - Beleg: `.agent/workflows/wiki_style_guide.md:87`
- Dokumentationsdrift im Meta-Workflow:
  - `walkthrough.md` wird gefordert, obwohl laut Changelog entfernt.
  - Beleg: `.agent/workflows/meta_master.md:22`

## Konkrete Direktiven (Officials)
1. **Normierungswelle (Pflicht zuerst)**
Alle `file://` Links in `.agent/workflows/*.md`, `.agent/instructions/*.md`, `System/COORDINATION_HUB.md` auf repo-relative Links oder `[[WikiLinks]]` umstellen.
2. **Artefakt-Entscheid**
`INVENTUR_QUELLEN`, `INGESTION_LOG`, `Konsistenzbericht_2026`, `SY_BULLETIN` entweder:
- neu anlegen (mit Template + UUID + ISO Zeitstempel), oder
- aus allen Workflows entfernen und durch aktuelle Boards/Logs ersetzen.
3. **CLI-Realignment**
Nur zwei Wege erlauben:
- Entweder fehlende Commands in `7w_wiki.py` implementieren,
- oder alle Workflows auf vorhandene Commands abbilden.
4. **Toolnamen-Härtung**
`notify_user`, `multi_replace_file_content` durch reale Toolpfade ersetzen.
5. **Board-Konsolidierung**
`REVIEW_BOARD.md` Verweise auf `SY_REVIEW.md` migrieren.

## Umsetzungsvorschlag (Kurz)
- Phase A (2h): Pfad- und Board-Fix (`file://`, `REVIEW_BOARD`, `SY_BULLETIN` Entscheidung)
- Phase B (2h): CLI/Workflow Mapping-Tabelle in `README.md` und `start.md`
- Phase C (2h): Abschlussaudit mit `7w_wiki.py audit` und Changelog-Eintrag

## Abschluss
Das System ist arbeitsfaehig, aber aktuell nur fuer erfahrene Maintainer sicher. Fuer saubere Ingestion durch Officials muss der Drift zwischen Workflow-Texten und Runtime kurzfristig geschlossen werden.
