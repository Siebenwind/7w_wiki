# Session Memory: Pages-Audit und Bridge-Retirement

**Datum:** 2026-08-23
**Rolle:** Oberarchivar
**Branch:** `main`
**Ausgangsstand:** `3bcf0122`

## Kontext

Die zuvor veroeffentlichten Commits `3f7b2016` und `3bcf0122` enthalten den Pages-/Mobilvertrag sowie vier Historikerlaeufe mit 20 Forumquellen. Dieser Handover aktualisiert den Betriebszustand und beantwortet die Frage, was der grosse Pages-Audit prueft und wie mit dem verbliebenen Brueckenbestand umzugehen ist. Es wurden keine neuen Loreaussagen eingefuehrt.

## Durchgefuehrte Arbeiten

- Den kanonischen Handover-Workflow ausgefuehrt: Archivrotation, Werkzeugmanifest, vollstaendige Testsuite, offene Dispatch-Queue und Pages-Vollvalidierung.
- Statistik und Leserkennzahlen erneuert: `1.417` Wikiartikel und `115` vollstaendig erfasste Ingestion-Berichte.
- `242` aeltere Audit-, Statistik- und Sessionberichte in kalte Archive gebuendelt; `33` erledigte Dispatches nach `System/Synapse_Board/DISPATCH/_archive/` verschoben.
- Den offenen Pages-Bestand auf `622` unresolved, `620` unallowlisted, `609` needs_historian und `5` generic_term_conflict bestaetigt.
- Den Brueckenbestand gesondert geprueft: `84` temporaere Bruecken sind formal valide, tragen aber ausnahmslos das ueberfaellige Reviewdatum `2026-06-30`.
- `MSG-2026-0240` an den Technician gestellt: Der Audit soll klaeren, ob ueberfaellige `bridge_review_until`-Werte als eigener Lifecycle-Befund sichtbar werden muessen.
- `MSG-2026-0241` uebergibt diesen Abschluss samt Session-Memory an den Coordinator.
- Eine durch die Rotation sichtbar gewordene Dispatch-Kollision behoben: Die ID-Vergabe betrachtet nun heisse und archivierte Nachrichten gemeinsam. Der Vertragstest `takeover-handover` deckt diese Invariante ab.

## Was der grosse Pages-Audit ist

`./7w_wiki.py audit --pages --json` erweitert den normalen Konsistenzaudit um die komplette Pages-/Roamlink-Analyse. Er prueft unter anderem Linkziele, Render- und Vertragsbefunde, Stubs, Bridges, Split-Brain-Risiken und Traceability. Bei diesem Bestand benoetigt der Lauf knapp fuenf Minuten und liegt deshalb nahe an der 300-Sekunden-Grenze des Vertragstests.

`./7w_wiki.py pages validate --json` fuehrt zusaetzlich den MkDocs-Bau aus, vergleicht den Publikationsbaum mit `docs/Siebenwind_Wiki/`, prueft Statistikfrische und Link-Ratchet und schreibt `.agent/data/pages_health.json`. `--strict-links` macht den bekannten Altbestand zum harten Gate; ohne diesen Schalter bleibt der kontrollierte Altbestand ein `WARN`.

Fuer die operative Zerlegung des Linkaltbestands dient `./7w_wiki.py pages backlog summary --json`. Die 84 funktionierenden Bruecken erscheinen dort nicht als defekte Links und benoetigen deshalb einen eigenen Retirement-Lauf.

## Validierung

- `./7w_wiki.py test --suite pages-link-contract --post-failures --from-agent Test-Waechter --to-agent Technician --priority HIGH`: PASS `5/5` im fokussierten Wiederholungslauf; es wurde kein Defect erzeugt.
- Erneuter `./7w_wiki.py test --suite all`: PASS fuer alle stabilen Standardsuiten. `pages-full-smoke` und der RAG-Smoke bleiben gemaess Standardlauf opt-in.
- `./7w_wiki.py pages validate --json`: Build Exit `0`, `drift_status = PASS`, Publikationsfrische `PASS`, Link-Ratchet `PASS`, Gesamtstatus `WARN`.
- `./7w_wiki.py audit --json`: `issues_found = 0`, `bridge_inventory.total = 84`, `bridge_inventory.invalid = 0`.
- Pages-Bauzeit: rund `242` Sekunden; der erste Gesamtlauf traf beim eingebetteten Pages-Audit einmalig das 300-Sekunden-Limit, fokussierter und erneuter Gesamtlauf bestanden danach.

## Offene Punkte und naechster Einstieg

1. `MSG-2026-0240` pruefen beziehungsweise claimen und entscheiden, ob ueberfaellige Bridge-Reviewdaten im Audit einen eigenen Lifecycle-Status benoetigen.
2. Bridge-Retirement in kleinen Wellen beginnen: eingehende WikiLinks auf das kanonische `bridge_target` migrieren, Ergebnis validieren, dann die ueberfluessige Bruecke entfernen. Keine pauschale Fristverlaengerung und keine neuen generischen Platzhalter.
3. Zuerst eindeutige Alias-/Schreibvarianten bearbeiten; semantisch verlustbehaftete oder typveraendernde Ziele an Historian/Coordinator geben.
4. Anschliessend den allgemeinen Pages-Historian-Backlog mit `register_links`, `generic_magie` und `werke_links` fortsetzen.
5. Unabhaengig davon bleiben 22 Forumvolltexte fachlich offen; das naechste Fuenferpaket beginnt mit `106975`, `109430`, `109411`, `103341` und `99477`.
6. `RESEARCH-2026-004` und `RESEARCH-2026-007` warten weiterhin auf Review; der Forum-Scan ist fuer drei konfigurierte Boards veraltet.

## Bewusst nicht veraendert

- `System/Synapse_Board/DISPATCH/MSG-2026-0199_yen_usd_carry_trade_dossier_recherchiert.md` bleibt sachfremd, unversioniert und unangetastet.
- Der generierte Buildbaum `site/` bleibt ein ignoriertes Artefakt und wird nicht eingecheckt.
- Keine der 84 Bruecken wurde im Handover entfernt oder inhaltlich umgedeutet.
