# Betrieb der Leserseiten

Aktive Anleitung, Stand 9. September 2026. MkDocs Material und GitHub Pages bleiben die Publikationsbasis. Pagefind erzeugt einen statischen Index für Suchvorschläge und die Ergebnisseite; der Material-Suchindex ist entfernt.

## Einrichtung und Prüfung

```bash
./7w_wiki.py pages setup --browsers
./7w_wiki.py stats
./7w_wiki.py pages validate --json
./7w_wiki.py test --suite reader-browser
./7w_wiki.py test --suite reader-rendered-links
./7w_wiki.py pages serve
```

Die Vorschau läuft unter `http://127.0.0.1:8765/7w_wiki/`. Die Browserprüfung startet ihren eigenen lokalen Server und prüft Chromium, Firefox und WebKit mit 320, 390, 768, 1024 und 1440 Pixeln in beiden Farbschemata. Sie legt Ergebnisse und Bilder im System-Temporärverzeichnis unter `7w_reader_browser_*` ab. Reale iOS- und Android-Geräte benötigen eine zusätzliche manuelle Freigabeprüfung. Fehlende Geräteprüfung ausdrücklich dokumentieren.

Die übrigen Pflichtprüfungen stehen in `AGENTS.md`. Während der Bearbeitung gezielt testen; am finalen Stand einmal vollständig abnehmen. `pages-full-smoke` und vollständige Pages-Validierung bleiben erforderlich. Der semantische Linkaltbestand darf nicht wachsen.

Der Seitenbau prüft auch die tatsächlich ausgegebenen HTML-Verweise einschließlich Karten und Abschnittsziele. Fehlende Ziele in generierten Seiten stoppen den Build. Unverändert übernommenes Quellen-HTML wird separat in `site/rendered-links.json` ausgewiesen; dessen historische Links werden nicht stillschweigend als funktionierend gewertet.

## Suche

`suche/?q=Bellum&bereich=wiki` ist die öffentliche Suchroute. Standardbereich ist Wiki; Quellen, Forschung, Technik und Alles sind auswählbar. Exakte Titel und bekannte Aliasnamen stehen vor Erwähnungen. Brücken liefern Namen für eindeutige Zielartikel. Navigationsleisten und Artikel-Betriebshinweise werden nicht indexiert. Ein fehlgeschlagener Pagefind-Build stoppt die Veröffentlichung.

## Leseränderungen und Empfehlungen

`./7w_wiki.py stats` liest `.agent/data/reader_updates.json`. Einträge enthalten Datum, Titel, Kurzbeschreibung, betroffene Artikel, Nachweis und `draft` oder `published`. `published` bedeutet redaktionell zur Leseranzeige freigegeben; es behauptet keinen neuen Deploymentnachweis. Nur freigegebene Einträge bis zum heutigen Datum erscheinen unter Neues und auf der Startseite, unabhängig von der Agentenrolle.

Empfehlungen bleiben redaktionelle Entscheidungen. Überfällige Auswahlen behalten ihre Links und verlieren das Kennzeichen Neu. LQS, Tags und Linkhäufigkeit vergeben keine inhaltliche Freigabe.

Die monatliche Auswahl umfasst bis zu drei neue Empfehlungen und bis zu fünf Neuveröffentlichungen. Die Vorprüfung betrachtet Quellenbezug, verständliche Einleitungen und Anschlussartikel; Lektor und Strukturprüfung ergänzen sie. Eine menschliche Redaktion entscheidet über Leserwert, sachliche Einordnung und Freigabe. Letzten und nächsten Review sichtbar datieren, Änderungen im Changelog und Dispatch dokumentieren. Ein überfälliger Review wird nicht durch automatische Rotation verdeckt.

## Betrieb, Altbestand und Veröffentlichung

[Betrieb und Prüfstand](status.md) und Advisor verwenden dieselbe Pages-Snapshotquelle sowie dieselbe Brückenprüfung. Datum, Alter und Messumfang werden ausgewiesen. Die Brückenbaseline dokumentiert bekannte überfällige Fälle; neue oder verschlechterte Fristfälle sperren die Abnahme. Keine pauschalen Verlängerungen.

`build-info.json` enthält UTC-Bauzeit, Commitkennung, lokale Änderungen und Suchstatus. Erst ein Vergleich mit der tatsächlich ausgelieferten Datei weist die Veröffentlichung dieses Builds nach. Der lokale Status behauptet dies nie. Die Veröffentlichung ist ein eigener abschließender Schritt.

Nach der Veröffentlichung vergleicht `./7w_wiki.py pages verify-live --commit <erwartete-Commitkennung>` den tatsächlich ausgelieferten Build mit der erwarteten Version. Dieser Schritt ist auch im Deployment-Workflow enthalten.

Dispatch unterscheidet `TASK` und `INFO`. Neue Nachrichten sind standardmäßig Aufträge. `mail post --kind INFO` dokumentiert Ergebnisse ohne offene Folgeaktion. Bestehende Nachrichten werden einzeln nach Lesen ihrer Nachweise mit `mail classify ID --kind INFO --agent Technician --note "Nachweis und Begründung"` abgeschlossen. Unklare Nachrichten bleiben Aufträge.
