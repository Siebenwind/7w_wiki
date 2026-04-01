# Session Memory: Pantheon-Nomenklatur und Nav-Symmetrie

- Date: 2026-03-28
- Focus: GitHub-Pages-Navigation im Pantheon entasymmetrieren und die kanonische Doppelbenennung `Viere/Sahor` sowie `Elementarherren/Enhor` auf den zentralen Seiten konsistent verankern

## Context
- Ausloeser war die konkrete Maintainer-Frage, warum in GitHub Pages `Astrael` noch als einzelner Reiter unter `Pantheon` auftaucht, waehrend `Enhor` und `Sahor` nicht gleichrangig sichtbar sind.
- Repo-Befund vor dem Eingriff:
  - `mkdocs.yml` privilegierte `Astrael` in der manuellen `nav`.
  - `Das_Pantheon.md` nutzte noch asymmetrische bzw. veraltete Sammelbegriffe.
  - `Viere.md` und `Die_Viere_Kirche.md` waren noch schwache Placeholder-/Bridge-Seiten.
  - `Religion_Übersicht.md` enthielt zwar die korrekte Primärlogik, aber noch Agentenreste und inkonsistente Formulierungen.

## What Changed
- `mkdocs.yml`
  - `Astrael` ist kein einzelner Sonderreiter mehr.
  - `Pantheon und Religion` fuehrt jetzt:
    - `Religion Übersicht`
    - `Das Pantheon`
    - `Die Viere (Sahor)` als symmetrische Untergruppe mit `Astrael`, `Bellum`, `Vitama`, `Morsan`
    - `Die Elementarherren (Enhor)`
    - `Die Gohor`
    - `Angamon`
- `docs/Siebenwind_Wiki/01_Pantheon/Das_Pantheon.md`
  - `Die Viereinigkeit (Die Guten)` -> `Die Viere (Sahor)`
  - `Die Elemente & Andere` -> `Die Elementarherren (Enhor)`
- `docs/Siebenwind_Wiki/00_Fundament/Religion_Übersicht.md`
  - Doppelbenennung explizit geklaert:
    - `Die Viere` = gebraeuchlicher religioeser/alltagssprachlicher Ausdruck
    - `Sahor` = kosmologisch-theologischer Sammelname
    - `Elementarherren` = beschreibender Alltagsbegriff
    - `Enhor` = Eigenname der Gruppe
  - fehlerhaften `Rien`-Link bereinigt
  - alten Agenten-Review-Satz entfernt
- `docs/Siebenwind_Wiki/00_Fundament/Viere.md`
  - von schwachem Brueckenartikel zu kurzer kanonischer Begriffsseite gehoben
- `docs/Siebenwind_Wiki/00_Fundament/Die_Viere_Kirche.md`
  - von `UNGEKLAERT`-Bridge zu klarer Alias-/Begriffsseite fuer `Kirche_der_Viere` gehoben
- `docs/Siebenwind_Wiki/03_Gesellschaft/Kirche_der_Viere.md`
  - Einleitung auf `Viere` vs. `Sahor` ausgerichtet
  - offensichtliche Syntaxreste (`Bellum`, `Region_Sae`) bereinigt
- `docs/Siebenwind_Wiki/03_Gesellschaft/Ecclesia_Elementorum.md`
  - Institution als organisierte Verehrung der `Enhor`/`Elementarherren` praezisiert

## Verification
- `./7w_wiki.py test --suite content-contract`
- `./7w_wiki.py test --suite render-hygiene`
- `./7w_wiki.py test --suite interop-doc-links`
- `./7w_wiki.py pages validate --json --skip-audit`

## Result
- `mkdocs build`: `exit_code = 0`
- `pages_health.status = WARN`
- `pages_health.unresolved_total = 746`
- `pages_health.unallowlisted_total = 744`
- `pages_health.drift_status = PASS`
- Der Pantheon-Bereich ist navigationsseitig nicht mehr auf `Astrael` verengt, sondern als Gruppenstruktur sichtbar.

## Notes / Next Agent
- Diese Welle war bewusst terminologisch und navigationsbezogen, kein neuer allgemeiner Pages-Repair-Lauf.
- Das naechste passende Folgethema ist ein semantisch konservativer Cluster fuer Religions-/Pantheon-Ziele wie:
  - `En'Hor -> Enhor`
  - `Die_Kirche`
  - `Die_Vier_Kirchen`
  - `Gottheiten`
- Dabei weiter streng zwischen:
  - mechanischer Alias-Reparatur
  - review-pflichtiger Religions-/Institutionssemantik
  - epistemischer Eskalation gegen Homepage-/Quellenlage
