# Session Memory: Historie-Cluster

- Date: 2026-03-30
- Focus: Den generischen unresolved target `Historie` konservativ aus dem aktiven Wiki entfernen, ohne die sichtbar beschaedigte Struktur von `Zeitstrahl.md` in einen ungeplanten Grossumbau ausarten zu lassen.

## Context
- Ausgangslage vor dieser Welle:
  - `pages_health.unresolved_total = 734`
  - `pages_health.unallowlisted_total = 732`
  - `pages_health.drift_status = PASS`
- Repo-Befund:
  - `pages_health.targets` fuehrte `Historie` mit `count = 9`.
  - Alle aktiven `[[Historie]]`-Vorkommen lagen in `docs/Siebenwind_Wiki/05_Geschichte/Zeitstrahl.md`.
  - `Zeitstrahl.md` ist strukturell beschaedigt und enthaelt eingebettete Fremdseitenfragmente; der Cluster wurde deshalb bewusst auf den Zielpfad beschraenkt.
- Kanonische Zielentscheidung:
  - `Historie` meint in diesem Kontext nicht die allgemeine Geschichtskategorie, sondern die Chronikseite `docs/Siebenwind_Wiki/04_Chronik/Historie_&_Ären.md`.

## What Changed
- `docs/Siebenwind_Wiki/05_Geschichte/Zeitstrahl.md`
  - alle neun `[[Historie]]`-Vorkommen auf `[[Historie_&_Ären|Historie]]` gehoben
  - keine weitergehende Tabellen- oder Strukturreparatur derselben Datei in dieser Welle

## Verification
- `./7w_wiki.py pages validate --json --fast --skip-audit`
- `./7w_wiki.py pages validate --json --skip-audit`

## Result
- `mkdocs build`: `exit_code = 0`
- `pages_health.drift_status = PASS`
- `pages_health.unresolved_total = 725`
- `pages_health.unallowlisted_total = 723`
- `Historie` ist aus dem aktuellen Top-Target-Block verschwunden.
- `Zeitstrahl.md` bleibt als beschaedigte Datei ein separater Technik-/Content-Defekt, wurde in dieser Welle aber nicht weiter verschlechtert.

## Notes / Next Agent
- Der naechste hohe Hebel ist jetzt die `Magie`-Familie:
  - `Magie`
  - `Magie_Elementarmagie`
  - `Magische_Rituale`
  - `Magietheorie_Grundlagen`
- Wenn ein sauber isolierter Reparaturtrack fuer `Zeitstrahl.md` gestartet wird, sollte er als eigener Struktur-/Sanitizer-Task behandelt werden, nicht als normaler Link-Cluster.
