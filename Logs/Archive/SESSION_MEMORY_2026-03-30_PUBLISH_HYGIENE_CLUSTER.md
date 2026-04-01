# Session Memory: Publish-Hygiene-Cluster nach Religions-Phase 2

- Date: 2026-03-30
- Focus: Die nach Religions-Phase 2 verbliebenen Zielnamen `Gottheiten`, `Die_Kirche` und `Die_Vier_Kirchen` nicht erneut im aktiven Wiki umschreiben, sondern ihren Publikationspfad in Reports, Archiv-Artefakten und Maintainer-Doku bereinigen.

## Context
- Ausgangslage vor dieser Welle:
  - `pages_health.unresolved_total = 746`
  - `pages_health.unallowlisted_total = 744`
  - `pages_health.drift_status = PASS`
- Befund:
  - `docs/Archiv/Ingestion_Reports` ist ein Symlink auf `../../Logs/Ingestion` und wird damit im MkDocs-Build publiziert.
  - Die verbliebenen Religionsziele kamen nicht mehr primaer aus den zuletzt bereinigten Kernseiten, sondern aus publizierten Ingestion-Reports, Maintainer-Doku und einzelnen Alias-Formen.

## What Changed
- `docs/Siebenwind_Wiki/01_Pantheon/Der_naive_Mensch.md`
  - Alias-Form `[[Religion_Übersicht|Gottheiten]]` in `Gottheiten (siehe [[Religion_Übersicht]])` ueberfuehrt.
- `docs/Siebenwind_Wiki/04_Chronik/Siebenwind_Bote_128.md`
  - `[[Kirche_der_Viere|Die Kirche]]` auf `[[Kirche_der_Viere]]` reduziert.
- `docs/Siebenwind_Wiki/04_Chronik/Siebenwind_Bote_159.md`
  - `[[Kirche_der_Viere|Die Kirche]]` auf `[[Kirche_der_Viere]]` reduziert.
- `docs/Siebenwind_Wiki/04_Chronik/Siebenwind_Bote_187.md`
  - Viere-Kirchen-Verweis auf direkten kanonischen Linkstil normalisiert.
- `docs/Siebenwind_Wiki/07_Persoenlichkeiten/Utrich_Rothnang.md`
  - Alias-Form `[[Kirche_der_Viere|Die Kirche]]` auf direkten kanonischen Linkstil reduziert.
- Publizierte Ingestion-Reports bereinigt:
  - `Logs/Ingestion/2026-02-15_Aequitas.md`
  - `Logs/Ingestion/2026-02-15_Alles_ohne_Pointe.md`
  - `Logs/Ingestion/2026-02-15_Althea_Danea_-_Kompendium_der_Wei·magie.md`
  - `Logs/Ingestion/2026-02-16_Der_Blutrote_Stier.md`
  - `Logs/Ingestion/2026-02-16_Der_Traum_der_Tausend.md`
  - `Logs/Ingestion/2026-02-16_Der_letzte_Falke.md`
  - `Logs/Ingestion/2026-02-16_Die_Goldenen_Tafeln.md`
  - dort verbleibende Religionszielnamen auf direkte kanonische Links bzw. Plaintext reduziert.
- Maintainer-Doku bereinigt:
  - `CHANGELOG.md`
  - `MASTER_TASK_LIST.md`
  - `Logs/Archive/SESSION_MEMORY_2026-03-30_RELIGION_CLUSTER.md`
  - `Logs/Archive/SESSION_MEMORY_2026-03-30_RELIGION_CLUSTER_PHASE2.md`
  - problematische Literalformen der Restziele wurden so umgeschrieben, dass sie nicht mehr selbst unresolved targets erzeugen.
- Arbeitsartefakte fortgeschrieben:
  - `.agent/data/religion_cluster_review.json`
  - `.agent/data/religion_cluster_escalations.json`

## Verification
- `./7w_wiki.py pages validate --json --skip-audit`
- `./7w_wiki.py test --suite content-contract`
- `./7w_wiki.py test --suite render-hygiene`
- `./7w_wiki.py test --suite interop-doc-links`

## Result
- `mkdocs build`: `exit_code = 0`
- `pages_health.drift_status = PASS`
- `pages_health.unresolved_total = 734`
- `pages_health.unallowlisted_total = 732`
- Die zuvor dominanten Religionsziele sind aus dem aktiven Inhalts-Track und aus den publizierten Ingestion-/Maintainer-Artefakten weitgehend entfernt.
- Der religioese Resolver-/Archiv-Follow-up gilt damit als abgearbeitet; der naechste sinnvolle Pages-Cluster ist nicht mehr `Gottheiten`/`Die_Kirche`, sondern die generischen Top-Ziele `Historie`, `Magie`, `Magie_Elementarmagie` und danach der semantisch heiklere Cluster `Dämonen`.

## Notes / Next Agent
- Nicht zurueck in denselben Religions-Cluster fallen; der Resthebel liegt jetzt bei generischen Index-/Kategoriezielen.
- Explorer-/Codepfad-Befund:
  - `pages validate` gruppiert unresolved targets aus MkDocs-/Roamlinks-Warnings gegen den docs-only Index in `.agent/scripts/pages_integrity.py` und `.agent/scripts/pages_tool.py`.
  - Die Religionsziele `Gottheiten`, `Die_Kirche` und `Die_Vier_Kirchen` sind im Snapshot `generated_at = 2026-03-30T17:02:37Z` nicht mehr vorhanden; fruehere `source_pages: []` waren also ein Resolver-/Report-Symptom, nicht Beleg fuer noch aktive Wiki-Markdown-Vorkommen.
- Empfohlene naechste Reihenfolge:
  - Hauptcluster: `Magie`, `Magie_Elementarmagie`, `Magische_Rituale`, `Magietheorie_Grundlagen`
  - Low-Risk-Alternative: `Historie`
  - erst danach `Dämonen`, weil dort auch `docs/Quellen/Spielergeschichten/Die Nacht des Dunkeltiefs.md` betroffen ist.
