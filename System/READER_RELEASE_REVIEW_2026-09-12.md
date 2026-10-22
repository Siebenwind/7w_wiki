# Leserzugang: Umsetzung und Abnahme

Stand: 12. September 2026. Auftrag: Leserzugang, Suche und verlässlicher Betrieb; ergänzt um die redaktionelle Prüfung der ersten Lesestrecken. Commit, Push und Live-Auswertung sind ausdrücklich beauftragt.

## Fortschreibung am 21. Oktober 2026

Der Leserrelease war beim Wiederaufnehmen noch uncommittet und unveröffentlicht. Die folgenden September-Prüfstände sind historische Nachweise; eine neue Abnahme erfolgt durch einen ausdrücklich beauftragten GPT-5.6-Sol-Testagenten. Der zweite Testagent hat alle 53 zunächst ungeprüften Dokumenteinträge einzeln mit CLI, Implementierung und Dateibaum abgeglichen. Die konkreten Fehlanweisungen in Style Guide, Ingestion, Scout, Auskunft, Produktionsprotokoll und Score-Leitfaden sind korrigiert. Historische Kickoffs und Hypothesen bleiben erhalten, sind aber keine aktiven Anweisungen oder Kanonbelege.

Die frühere pauschale Restliste von 53 Dokumenten ist damit ersetzt: Das erzeugte Inventar enthält 67 aktuelle und 24 ausdrücklich historische Dokumente, ohne verbleibenden ungeprüften Eintrag. Die Prüfung bestätigt technische Anleitungen und Referenzen, keine fachliche Wahrheit sämtlicher Loreartikel. Reale Geräte, echte Screenreader und menschliche Kurationsfreigaben bleiben offen. Der Oktober-Abschluss wird in `Logs/Archive/SESSION_MEMORY_2026-10-21_LESERRELEASE.md` nachgewiesen.

## Vorher und nachher

**Abschlussentscheidung vom 22. Oktober:** Der Nutzer beauftragte ausdrücklich Commit, Push und Merge ohne weitere Tests. Deshalb wird für den letzten Stand keine neue vollständige Abnahme behauptet. Nach dem vollständigen Pages-Bau vom 21. Oktober folgten noch der Clean-Checkout-Fallback und die Karamir-Korrektur. Die neue Browsermatrix konnte vor der Unterbrechung durch fehlende Browserdateien und das Nutzungslimit des Testagenten nicht abgeschlossen werden. Die historischen September-Nachweise bleiben als solche erhalten. Vorhandene automatische GitHub-Workflows werden nicht umgangen.

| Befund | Umsetzung / Nachweis |
| :--- | :--- |
| Mobile Suche zeigte eine weiße Fläche mit 0 Pixel hohem Scrollbereich. | Eigenständige, begrenzte Vorschlagsfläche mit sichtbaren Lade-, Fehler- und Leerzuständen; eine vollständige Ergebnisseite verwendet denselben Suchdienst. |
| Quellen und Brücken verdrängten passende Artikel. | Pagefind mit Wiki als Standardbereich, exakten Titeln und Aliasnamen vor Erwähnungen, kanonischer Zusammenführung und getrennten Quellen-/Forschungs-/Technikbereichen. |
| Einstieg führte in Architektur und Agentenbetrieb. | Kurzer Leserstart, acht Themenzugänge, A–Z, Neues und Quellenorientierung; Technik und Mitarbeit im Fußbereich. |
| Helle Flächen im Dunkelmodus, Tabellen schwer erreichbar. | Gemeinsame getrennte Farbtokens, begrenzte Komponentenregeln, Tastaturzugang zu Scrolltabellen. |
| HTML-Kartenlinks und Abschnittsverweise entgingen den Prüfungen. | Prüfung sämtlicher generierter HTML-Anker im Build. 14 tatsächliche Altfehler korrigiert; URL-Sonderzeichen und Indexkarten als Regressionen abgesichert. |
| Arbeit blieb hinter rollenspezifischen Changelog-Titeln verborgen. | Strukturierte Leseränderungen erzeugen Neuigkeiten und Startseitenaktivität über den Statistiklauf. |
| Überfällige Brücken wurden nicht als eigener Befund gezeigt. | 84 bekannte abgelaufene Fristen explizit als Altbestand; neue Fälle und pauschale Verlängerungen sperren die Abnahme. |
| Kopierte Statuszahlen widersprachen dem Pages-Snapshot. | Gemeinsame Snapshotauswertung für Advisor und Betriebsseite mit Messdatum, Alter und Umfang. |

## Redaktionelle Prüfung der ersten Wege

Die Startseite, Welt entdecken, Quellen & Forschung, Lesetipps und thematischen Einstiege wurden auf Sprache, Orientierung und Auswahl geprüft. Die direkt empfohlenen Einleitungen wurden mit den höherwertigen Quellen verglichen. Keine vollständige Loreprüfung sämtlicher Artikel.

| Seite | Befund und Korrektur | Primärer Nachweis |
| :--- | :--- | :--- |
| Siebenwind | Falkensee fälschlich als aktuelle Hauptstadt; historische Kronmarkverwaltung als Gegenwart. Nun Ruinenstadt und historische Verwaltung getrennt. | [Offizielle Inselbeschreibung](https://www.siebenwind.de/hintergrund/atlas/die-insel-siebenwind/) |
| Brandenstein | Unbelegte junge Hauptstadt und ausgeschmückter Gründungszustand. Einleitung nun Hafenstadt und älteste bestehende Stadt; historische Abschnitte eingeordnet. | [Offizielle Ortsbeschreibungen](https://www.siebenwind.de/hintergrund/atlas/die-insel-siebenwind/orte-auf-siebenwind/) |
| Pantheon / Religion Übersicht | Angamon als bloßer Dämonenfürst beziehungsweise Vernichter. Herrschaftsziel und Glaubenswandel präzisiert. | [Offizieller Angamon-Hintergrund](https://www.siebenwind.de/hintergrund/gotterwelt/angamon/) |
| Arman / Draconis | Arman und Karamir verwechselt: Arman stirbt in der Erzählung; Karamir tritt in Draconis dem Vitamaorden bei. Ordensbiografie und Stadtbeispiel korrigiert. | `Quellen/Zeitung 7w Bote/Siebenwind Bote 123.md`, Erzählung von Aelwin |
| Zeitrechnung | Starre 28-Tage-Monate, unvollständiges Mondmodell und unbelegte aktuelle Jahresumrechnung. Auf die belegten Grundzüge zurückgeführt. | [Offizielle Zeitrechnung](https://www.siebenwind.de/hintergrund/zeitrechnung/) |
| Lesetipps | Betriebsverfahren dominierten den Einstieg. Drei kurze Leserwege vorangestellt; April-Auswahl und ausgebliebener Review ausdrücklich datiert. | Abgleich der oben genannten Einstiegsartikel |
| Bellum | Beschädigter Einstieg und unbelegte Ausschmückungen. Kurzes Profil zu Ehre, Mut, Schmiedekunst und Gerechtigkeit mit nachvollziehbaren Quellen. | [Kirche der Viere](https://www.siebenwind.de/hintergrund/gotterwelt/kirche-der-viere/) |

Die offizielle Ortsunterseite enthält selbst ältere Falkensee-Passagen in Gegenwartsform. Die ausdrücklich aktuelle Inselübersicht und der bereits korrigierte Falkensee-Artikel stützen den Ruinenzustand. Die genaue Gleichsetzung mit Luth Chalid bleibt offen. Der Oracle-Versuch scheiterte am fehlenden Modellcache; Homepage und lokale Originalquelle wurden direkt gelesen. Dokumentiert in MSG-2026-0260.

## Dokumentation und Auftragsbestand

Die erneute redaktionelle Prüfung am 22. Oktober bestätigte die Startseiten sowie den Falkensee- und Arman-Weg. Eine unbelegte Begleiterbiografie in Karamirs Artikel wurde nach Bote 123 korrigiert: Schöpfer der Bestie, durch Arman zur Reue bewegt, später Dienst im Vitamaorden. Das Zeitungsdatum wird nicht als gesichertes Ereignisdatum ausgegeben. Arman verlinkt die korrigierte Seite. Die unabhängige Nachprüfung bestätigte die Konsistenz beider Artikel; der Umfang wurde anschließend eingefroren.

[Dokumentationsinventar](DOCUMENTATION_INVENTORY.md): 91 Dokumente inventarisiert. Der Septemberstand mit 17 aktuellen, 21 historischen und 53 ungeprüften Einträgen wurde am 21. Oktober durch den Einzelabgleich aller offenen Einträge abgeschlossen: 67 aktuell, 24 historisch. Korrigiert wurden insbesondere RAG-Anleitung, Archivar-Prompts, Styling-, Mitarbeit-, Ingestions-, Scout-, Score- und Testanleitungen. Aktive Berichtsvorlagen gelten nicht allein aufgrund ihres Dateinamens als historische Berichte.

Fünf Abschlussmeldungen wurden einzeln geprüft und als INFO eingeordnet: MSG-2026-0063, 0232, 0244, 0253 und 0258. Nachweise und erhaltene Folgeaufträge stehen jeweils in der Nachricht. Meldungen mit fehlendem Nachweis oder eigener Folgeaktion blieben offen; keine pauschale Bereinigung der übrigen Warteschlange. MSG-2026-0241 führt die fachliche Brückenstilllegung weiter. RESEARCH-2026-004 und RESEARCH-2026-007 sowie Oracle-Aufträge bleiben gesondert.

## Erneute Abnahme am 21./22. Oktober

Der vollständige Pages-Smoke-Test vom 21. Oktober endete mit Exit 0 (`TEST_pages-full-smoke_2026-10-21_235021.md`, temporäres Verzeichnis `7w_test_7znjebtd`). Der neue Snapshot von `2026-10-21T21:50:21Z` weist 612 ungelöste und 610 nicht freigestellte Linkvorkommen aus. Der Gesamtstatus bleibt WARN; Drift und Link-Ratchet bestehen. Im ursprünglichen Plan waren es 621/619.

Die Prüfung der gerenderten Verweise erfasst 2.633 generierte HTML-Seiten ohne fehlendes internes Ziel. Unverändertes Quellen-HTML wird gesondert ausgewiesen. Pagefind indexiert 2.539 Seiten erfolgreich.

Die 105 Standardprüfungen bestanden erneut. Anschließend wurde ein zusätzlicher Fall für frische Checkouts repariert: Ein fehlender lokaler Pages-Snapshot liefert unbekannte Messwerte und darf die Statistikerzeugung nicht abbrechen lassen. Dessen abschließende Regression und die Browserabnahme werden in der Oktober-Session-Memory protokolliert. Vor der Browserausführung mussten die nicht mehr vorhandenen Browserdateien nachinstalliert werden; die Startfehler sind keine Darstellungsbefunde.

## Historischer Prüfstand vom September

- Standardsuite: 33 Suiten bestanden (Berichte im temporären Verzeichnis `7w_test_cb2r2vbu`).
- `pages-full-smoke`: PASS, Bericht `7w_test_ky9ux3r0/TEST_pages-full-smoke_2026-09-12_142604.md`.
- Acht geänderte Einstiegsartikel: Lektor jeweils ohne Befund; Sanitizer ohne Vertrags-, Render- oder Traceability-Verstoß.
- Browsermatrix: 39/39 Fälle bestanden; Chromium, Firefox und WebKit, fünf Breiten, hell/dunkel sowie Such-, Ausfall- und Navigationsfälle. Bericht `7w_test_qod05aln/TEST_reader-browser_2026-09-12_202137.md`, Bilder und Detailwerte in `7w_reader_browser__5zw76u_` im System-Temporärverzeichnis.
- Vollständige Pages-Validierung: Build Exit 0, Gesamtstatus WARN wegen 621 ungelöster beziehungsweise 619 nicht freigestellter Linkziele. Kein Wachstum des bekannten Bestands.
- Veröffentlichung: Der Commit wird nach dieser lokalen Abnahme gebaut und veröffentlicht. Verbindlicher Live-Nachweis ist der erfolgreiche Workflow-Schritt `Verify delivered build identity` für dessen Commitkennung sowie der anschließende Abruf mit `pages verify-live`. Lokale Berichte behaupten keinen bereits erfolgten Deploymentnachweis.

## Grenzen der Aussage

Reale iOS-Safari- und Android-Chrome-Geräte sind nicht verfügbar. Die automatisierte Matrix ersetzt diese Geräteprüfung und eine Prüfung mit einem echten Screenreader nicht. Der semantische Linkrückstand, 84 überfällige Brücken und fachlich offene Forschungsfälle sind ausdrücklich erhalten. Originales Quellen-HTML besitzt historische, nicht mehr erreichbare Verweise; diese werden getrennt von generierten Wiki-Links ausgewiesen.

Die technische Leseroberfläche, die geprüften Anleitungen und die gezielte redaktionelle Reparatur lösen die größten Zugangsprobleme. Eine Aussage „alle Ziele vollständig erledigt“ setzt zusätzlich die fehlende Geräte- und Screenreaderabnahme sowie die menschliche Kurationsfreigabe voraus. Die gesonderten Altbestände benötigen weitere Quellenarbeit; die technische Modernisierung erklärt sie nicht für gelöst.
