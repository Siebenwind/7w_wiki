---
uuid: e9f7dc2f-4ece-40bf-95f3-0f4dcc0a9eb8
status: ACTIVE
updated_at: 2026-02-15T00:45:00Z
epistemic: "#meta"
---

# PRODUCTION_PROTOCOL

Verbindliches Protokoll, präzisiert am 21. Oktober 2026: Beauftragte, wiederverwendbare Ergebnisse werden innerhalb der ausdrücklich erlaubten Schreibgrenzen abgelegt. Reine Leseaufträge und temporäre Testartefakte erfordern keine zusätzlichen Repositorydateien.

## Ablagepflicht
- Schlussfolgerungen -> `Logs/Conclusions/`
- Ideen & Hypothesen -> `Logs/Ideas/`
- Artworks/Visual-Konzepte -> `Logs/Artworks/`
- Praesentationen/Dossiers -> `Logs/Presentations/`

## Mindestmetadaten je Artefakt
- `uuid`
- `date` (ISO-8601)
- `author`
- `status`
- `epistemic`

## Benennung
- `YYYY-MM-DD_Kurzbeschreibung.md`
- ASCII bevorzugt fuer Dateinamen.

## Operative Regel
- Beauftragte Ergebnisse mit Quellen, Prüfstand und offenen Punkten nachvollziehbar übergeben; keine ungefragten dauerhaften Nebenartefakte anlegen.
- Projektruntime ausschließlich über `./7w_wiki.py`; Abschluss mit Session-Memory und `mail done` oder `mail post` gemäß `AGENTS.md`. Zulässige temporäre Berichte können referenziert werden, ohne sie in das Repository zu übernehmen.
