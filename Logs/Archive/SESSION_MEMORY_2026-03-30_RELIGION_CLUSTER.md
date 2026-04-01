# Session Memory: Konservativer Religions-Cluster

- Date: 2026-03-30
- Focus: Religions-/Pantheon-Backlog clusterweise abbauen, ohne Rohquellen zu modernisieren oder generische Sammelbegriffe still umzubiegen

## Context
- Diese Welle folgte direkt auf die Pantheon-Nomenklatur- und Nav-Symmetrie-Arbeit vom 2026-03-28.
- Arbeitsregel war bewusst konservativ:
  - `docs/Quellen/` bleibt texttreu.
  - `En'Hor -> Enhor` nur in abgeleiteten Wiki-Seiten.
  - institutionelle Schwachziele wie `Die_Kirche` und `Die_Vier_Kirchen` nur nach Kontextsichtung.
  - generische Sammelbegriffe wie `Gottheiten` immer eskalieren.
- Baseline vor dem Eingriff:
  - `pages_health.unresolved_total = 746`
  - `pages_health.unallowlisted_total = 744`
  - `pages_health.drift_status = PASS`
  - letzter harter Snapshot: `2026-03-28T17:32:08Z`

## What Changed
- `docs/Siebenwind_Wiki/09_Bibliothek/Die_Elemente_ungleiche_Geschwister.md`
  - doppeltes Frontmatter und Legacy-`layout` entfernt
  - Metadatenblock in das kanonische Admonition-Format gehoben
  - `[[En'Hor]]` auf `[[Die_Enhor|Enhor]]` normiert
  - derivative Prosa von `En'Hor` auf `Enhor` vereinheitlicht
- `docs/Siebenwind_Wiki/01_Pantheon/Der_naive_Mensch.md`
  - doppeltes Frontmatter und Legacy-`layout` entfernt
  - Metadatenblock kanonisch normalisiert
  - der generische Zielbegriff `Gottheiten` wurde bewusst **nicht** automatisch umgebogen
- `.agent/data/religion_cluster_review.json`
  - maschinenlesbarer Snapshot fuer Baseline, Delta und Cluster-Entscheide
- `.agent/data/religion_cluster_escalations.json`
  - explizite Review-/Eskalationsliste fuer `Die_Kirche`, `Die_Vier_Kirchen` und `Gottheiten`

## Verification
- `./7w_wiki.py pages validate --json --fast --skip-audit`
- `./7w_wiki.py pages validate --json --skip-audit`
- `./7w_wiki.py audit --pages --json`
- `./7w_wiki.py test --suite content-contract`
- `./7w_wiki.py test --suite render-hygiene`
- `./7w_wiki.py test --suite interop-doc-links`
- `./7w_wiki.py pages validate --json --strict-links`

## Result
- `mkdocs build`: `exit_code = 0`
- `pages_health.drift_status = PASS`
- `pages_health.unresolved_total = 745`
- `pages_health.unallowlisted_total = 743`
- `pages validate --json --strict-links`: `FAIL`, aber am bekannten vorgeschalteten Altbestand (`173` Audit-Issues, davon `86` Bridge-Inventar-Issues), nicht an einer neuen Religions-/Render-Regression.
- `En'Hor`-Aliasdrift ist in abgeleiteten Wiki-Seiten beseitigt.
- `Die_Kirche`, `Die_Vier_Kirchen` und `Gottheiten` wurden regelkonform in einen Review-/Eskalationspfad ueberfuehrt statt still umgeschrieben.

## Notes / Next Agent
- Diese Welle war absichtlich kein breiter Religions- oder Bridge-Repair-Lauf.
- Die naechsten passenden Folgeschritte sind:
  - Eskalationsentscheidung fuer `Gottheiten`
  - lokale Kontextsichtung fuer `Die_Kirche` / `Die_Vier_Kirchen`
  - danach Rueckkehr in den breiteren Pages-/Bridge-Backlog
- Die `84` Single-Target-Bridges und `4` Bridge-Eskalationen bleiben ein getrennter Folge-Track.
