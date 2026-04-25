---
uuid: 7f6b0367-80e9-4ecf-ad50-4dfecf0cf87b
status: ACTIVE
created_at: 2026-02-18T00:10:00Z
epistemic: "#meta"
---

# Lessons Learned: Audit-Triage Link-Flood (2026-02-18)

## Kontext
- Ziel: Audit-Linkflood schnell senken, ohne laufende Interop-Guards zu brechen.
- Ausgangslage: `./7w_wiki.py audit` mit `1189` Problemen.
- Aktueller Stand: `348` Probleme (siehe Report unten).

## Ergebniskennzahlen
- Netto-Reduktion: `1189 -> 348` (`-841`, ca. `-70.7%`).
- Aktuellster Audit-Report:
  - `Logs/Archive/Audit_84814c9a-7906-469d-a35f-e5506733d443.txt`
- Clean-State:
  - `./7w_wiki.py test --suite clean-client-state` blieb durchgehend PASS.

## Wirksame Muster
1. Frequency-first statt file-first.
   - Missing-Targets zuerst nach Haeufigkeit gruppieren und in Batches beheben.
   - Ein Batch mit 15-30 Top-Targets bringt messbar mehr als Einzelfile-Korrekturen.
2. Brueckenartikel zentral in `Siebenwind_Wiki/00_Fundament`.
   - Senkt Risiko fuer Register-Orphans (Abschnitte 1-3 im Audit blieben gruen).
   - Einheitliches Frontmatter + `[UNGEKLAERT]` vermeidet Lore-Halluzination.
3. Malformed-Linkquellen direkt bereinigen.
   - Verschachtelte Muster wie `[[Forschungsberichte ([[Toran_Dur]])]]` erzeugen kuenstliche Missing-Targets.
   - Direkte Normalisierung auf existierende Werke-Links war effizient.
4. Nach jedem Batch sofort validieren.
   - `./7w_wiki.py audit`
   - `./7w_wiki.py test --suite clean-client-state`
   - optional `./7w_wiki.py index-pages` bei vielen neuen Artikeln.

## Was nicht funktioniert hat
- `./7w_wiki.py repair` / `./7w_wiki.py repair --full` waren fuer diesen Linkflood weitgehend no-op.
- Einzelne manuelle Korrekturen ohne Frequenzpriorisierung hatten geringe Hebelwirkung.

## Risiken / Tradeoffs
- Brueckenartikel stabilisieren Links schnell, erhoehen aber die Anzahl inhaltlich duenn besetzter Seiten.
- Folgearbeit bleibt erforderlich: Brueckenartikel inhaltlich ausarbeiten oder auf kanonische Zielartikel zusammenfuehren.

## Empfohlener Next-Step fuer Folgeagenten
1. Restliche Singletons batchweise abarbeiten (alphabetisch oder nach Domain-Cluster).
2. Kaputte Legacy-Patterns weiter normalisieren:
   - verschachtelte `[[...[[...]]...]]`
   - gemischte Space/Underscore-Umlaute.
3. Nach jeder Tranche:
   - Audit + Clean-State dokumentieren.
   - Delta im `CHANGELOG.md` und `MASTER_TASK_LIST.md` aktualisieren.

## Meilensteinverlauf (Audit)
- `1189` -> `1184` -> `1181` -> `994` -> `872` -> `807` -> `743` -> `684` -> `594` -> `546` -> `498` -> `458` -> `414` -> `382` -> `373` -> `348`
