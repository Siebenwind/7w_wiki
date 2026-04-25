# Forum-Geschichten Scout - 2026-04-19

## Done

- `./7w_wiki.py scout --forum geschichten --pages 5` ausgefuehrt.
- Erster Sandbox-Lauf scheiterte an DNS; zweiter Lauf mit genehmigtem Netzwerkzugriff war erfolgreich.
- 205 gesichtete Themen aus Forum `f=27` verarbeitet.
- 201 eindeutige Topic-IDs als Roh-Metadaten archiviert unter `docs/Quellen/Forum/Geschichten_aus_dem_Spiel/`.
- `.agent/data/forum_scan_register.json` aktualisiert.
- Scanner gehärtet:
  - `title`-Frontmatter wird kuenftig YAML-sicher quoted geschrieben.
  - Wiederholte Scans behalten bei vorhandenen Topic-IDs den bestehenden `source_ref`.

## Scope

- Es wurden keine Lore-Seiten angelegt.
- Es wurde kein Foren-Volltext extrahiert.
- Die neuen Dateien sind nur Roh-Metadaten aus der Forenuebersicht.
- Epistemischer Status bleibt `#forum`; Ingestion muss einzeln gegen hoehere Quellen und bestehende Wiki-Artikel geprueft werden.

## Inventur

- Neue Rohquellen-Dateien: 201.
- Board: `Geschichten aus dem Spiel`.
- Forum-ID: `27`.
- Register-Stand: `.agent/data/forum_scan_register.json`.
- Beispiel-Quelle: `docs/Quellen/Forum/Geschichten_aus_dem_Spiel/undated_angriff_auf_westhever_piraten_in_sicht_und_ein_angebot.md`.

## Erste Triage-Kandidaten

Diese Kandidaten wirken nach Titel und Weltbezug als sinnvoller erster Ingestion-Schnitt. Das ist noch keine Lore-Bewertung:

- `110175` - Angriff auf Westhever, Piraten in Sicht und ein Angebot
- `110194` - Erforschung und Entdeckungen in der neuen Heimat
- `110186` - Dur'sches Hoheitsgebiet
- `110158` - der etwas andere Besuch der Magierakademie
- `109946` - In der Kapelle von Ewigwacht
- `109905` - Ewigwacht
- `109818` - Reinigung des Morsanschreins
- `108735` - Das Gefolge - Ein Buch aus Finsterwangen
- `107362` - Neue Chronik Finsterwangen
- `107180` - Die Kanzlerdebatte - Redebeitraege
- `107457` - Westhever - Fornvinnr - Brandenstein
- `107351` - Am Ort der Daemonenbannung
- `107057` - Die Eiswoelfe ziehen in die Heimat
- `106598` - Die ewige Schlacht
- `106143` - Die Macht der Miliz
- `106220` - Der alte Wall - Neu entdeckt
- `105411` - Wacht fuer Angamon und ein erster Kontakt
- `104898` - Der Angriff auf den Wall
- `104494` - Umbau in Falkensee - Ab- und Aufbruchsstimmung

## Low-Priority / Filter

Folgende Titel sollten vorerst nicht in die erste Ingestion-Welle, weil sie nach Titel eher Meta, OOC, Humor oder persoenliches Kleinstformat sein koennen:

- `102477` - Zweck dieses Forums
- `31020` - Hintergrundexkurse
- `109282` - Mein erster Char
- `97823` - Susens Witzekiste
- `96919` - Gehirnscreenshot

## Verified

- `./7w_wiki.py test --suite source-link-hygiene`: PASS.
- `./7w_wiki.py test --suite pages-contract-mode-contract`: PASS.
- `./7w_wiki.py test --suite source-tree-contract`: PASS.
- `./7w_wiki.py test --suite tool-manifest-contract`: PASS.
- `./7w_wiki.py pages validate --contract --json`: `drift_status=PASS`, `legacy_root_status=removed`, Pages bleibt `WARN` mit bekanntem Backlog.
- `./7w_wiki.py audit --json`: weiterhin nur der bekannte `score_cluster`.
- `git diff --check`: clean.

## Next

- Erste Ingestion-Welle aus 10 bis 20 priorisierten Topic-Metadaten vorbereiten.
- Fuer jeden Kandidaten zuerst Foren-Volltext nachziehen oder manuell bestaetigen lassen; nicht aus dem Titel allein Lore ableiten.
- Danach Einzel-Ingestion gegen bestehende Artikel und Quellenkorpus abgleichen.
