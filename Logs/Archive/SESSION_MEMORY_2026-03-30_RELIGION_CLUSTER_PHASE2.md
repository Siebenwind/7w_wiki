# Session Memory: Religions-Cluster Phase 2

- Date: 2026-03-30
- Focus: Den Religions-/Pantheon-Cluster mit harter Kontext-Heuristik fortsetzen: `Gottheiten -> Religion_Übersicht`, eindeutige Viere-Kontexte explizit verlinken und die verbleibenden Religionsziele von einem Content- zu einem Resolver-/Archivproblem umklassifizieren.

## Context
- Ausgangslage vor Phase 2:
  - `pages_health.unresolved_total = 745`
  - `pages_health.unallowlisted_total = 743`
  - `pages_health.drift_status = PASS`
- Politische Vorgabe dieser Welle:
  - `Gottheiten` darf konservativ auf `Religion_Übersicht` gehoben werden.
  - `Die_Kirche` / `Die_Vier_Kirchen` duerfen bei eindeutigem Viere-/Galadon-Kontext auf `Kirche_der_Viere` gehoben werden.
  - `docs/Quellen/` bleibt textlich unangetastet.

## What Changed
- `docs/Siebenwind_Wiki/01_Pantheon/Der_naive_Mensch.md`
  - den Zielbegriff `Gottheiten` auf `[[Religion_Übersicht]]` gehoben.
- `docs/Siebenwind_Wiki/04_Chronik/Siebenwind_Bote_128.md`
  - `Die Kirche` im Tempelbau-Kontext auf `[[Kirche_der_Viere|Die Kirche]]` gehoben.
- `docs/Siebenwind_Wiki/04_Chronik/Siebenwind_Bote_159.md`
  - `Die Kirche` im Sammler-/Falkensee-Kontext auf `[[Kirche_der_Viere|Die Kirche]]` gehoben.
- `docs/Siebenwind_Wiki/04_Chronik/Siebenwind_Bote_187.md`
  - `Die Kirche` im Tempelwache-/Brandenstein-Kontext auf `[[Kirche_der_Viere|Die Kirche]]` gehoben.
- `docs/Siebenwind_Wiki/07_Persoenlichkeiten/Utrich_Rothnang.md`
  - `Die Kirche` im Prätor-/Scheiterhaufen-Kontext auf `[[Kirche_der_Viere|Die Kirche]]` gehoben.
- `docs/Siebenwind_Wiki/03_Gesellschaft/Ecclesia_Elementorum.md`
  - Die ambige Binnenformulierung `Die Kirche` zu `Die Gemeinschaft` entschaerft.
- `docs/Siebenwind_Wiki/03_Gesellschaft/Kirche_der_Viere.md`
  - Freischwebende `[[Die Kirche der Viere in Galadon]]`-WikiLinks auf den echten Quellenpfad `../../Quellen/Hintergrund/Die Kirche der Viere in Galadon.md` umgestellt.
- Arbeitsartefakte aktualisiert:
  - `.agent/data/religion_cluster_review.json`
  - `.agent/data/religion_cluster_escalations.json`

## Verification
- `./7w_wiki.py pages validate --json --fast --skip-audit`
- `./7w_wiki.py pages validate --json --skip-audit`
- `./7w_wiki.py pages validate --json --strict-links`
- `./7w_wiki.py test --suite content-contract`
- `./7w_wiki.py test --suite render-hygiene`
- `./7w_wiki.py test --suite interop-doc-links`

## Result
- `mkdocs build`: `exit_code = 0`
- `pages_health.drift_status = PASS`
- `pages_health.unresolved_total = 746`
- `pages_health.unallowlisted_total = 744`
- Die content-sicheren Religions-Rewrites sind im aktiven Wiki-Baum umgesetzt.
- Die Zielnamen `Gottheiten`, `Die_Kirche` und `Die_Vier_Kirchen` bleiben dennoch im Pages-Snapshot erhalten, nun ohne belastbare `source_pages`.
- Repo-/Site-Suche zeigt, dass zumindest ein Teil dieser Reste in Archiv-/Ingestion-Report-Artefakten weiterlebt, nicht mehr in den soeben bereinigten aktiven Religionsseiten.
- `pages validate --json --strict-links` bleibt am bekannten Audit-Precheck rot (`173` Issues, davon `86` Bridge-Inventar-Issues), nicht an neuen Contract-/Render-Verletzungen.

## Notes / Next Agent
- Nicht noch einmal blind denselben Religions-Content umschreiben.
- Der naechste passende Schritt ist ein kleiner Technik-/Resolver-Track:
  - Pages-Zielnamen gegen `docs/Archiv`-/Report-Quellen und generierte Site-Artefakte isolieren
  - klaeren, ob `Gottheiten`, `Die_Kirche` und `Die_Vier_Kirchen` aus Archivreports, Alt-Snapshots oder einem Resolver-Normalisierungsfehler stammen
  - erst dann entscheiden, ob weiterer Content-Fix, Report-Bereinigung oder Runtime-Anpassung noetig ist
