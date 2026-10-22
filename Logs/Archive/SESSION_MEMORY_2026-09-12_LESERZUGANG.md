# Übergabe: Leserzugang, Suche und Redaktion

Stand: 12. September 2026. Der Nutzer hat Umsetzung, Commit, Push und Auswertung der veröffentlichten Website ausdrücklich beauftragt und die redaktionelle Prüfung der Einstiegsseiten ergänzt.

## Ergebnis

Die Arbeitspakete A bis D stehen im gemeinsamen Release: Pagefind statt Material-Suche, responsive Leseroberfläche, Themenzugänge, strukturierte Neuigkeiten, getrennte Leser-/Betriebsstatistik, Dokumentationsinventar, Brücken-Lifecycle und Dispatch-Arten. Neue Systemdateien sind im Coordination Hub registriert. Der ausführliche Vorher-/Nachher-Bericht steht in `System/READER_RELEASE_REVIEW_2026-09-12.md`.

Die ersten Lesestrecken wurden zusätzlich mit Homepage und Originalquellen abgeglichen: Falkensee ist eine Ruinenstadt, Brandenstein eine alte Hafenstadt. Arman wurde mit Karamir verwechselt; Pantheon, Bellum und Zeitrechnung enthielten weitere belegbar falsche oder ungestützte Aussagen. Quellen und Umfang stehen im Bericht und in MSG-2026-0260. Nicht sämtliche Artikel sind fachlich geprüft; unklare Gleichsetzungen wurden nicht erfunden. Oracle bleibt wegen Modellcache-/Netzproblemen ein separater technischer Auftrag.

## Abnahme

- 33 Standardsuiten bestanden, Berichte unter `7w_test_cb2r2vbu` im System-Temporärverzeichnis; Inhalts- und Renderverträge nach den redaktionellen Änderungen erneut bestanden.
- Vollständige Pages-Validierung: Build Exit 0, Status WARN wegen des bekannten Linkaltbestands; 621 ungelöste und 619 nicht freigestellte Ziele, kein Wachstum.
- Browserprüfung: 39 Fälle bestanden, drei Browser, fünf Breiten, hell/dunkel, Suchrangfolge, Tastatur-, Zurück-, Ausfall- und Tabellenfälle. Bericht `7w_test_qod05aln/TEST_reader-browser_2026-09-12_202137.md`; Bildbelege `7w_reader_browser__5zw76u_`.
- Finaler Smoke-Test und Vertragsprüfung laufen vor dem Handover-Commit erneut nach den letzten redaktionellen Korrekturen. Der Deployment-Workflow prüft denselben Browservertrag und die ausgelieferte Commitkennung.
- Ein lokaler Build ist kein Live-Nachweis. Veröffentlichung nach dem Push mit `./7w_wiki.py pages verify-live --commit <Handover-Commit>` prüfen; der erwartete Commit muss exakt zur ausgelieferten `build-info.json` passen.

## Koordination und Restarbeiten

MSG-2026-0240 und MSG-2026-0259 wurden anhand der Implementierung und Tests abgeschlossen. Die Meldungen 0063, 0232, 0244, 0253 und 0258 wurden einzeln geprüft und als INFO eingeordnet. Eigene Folgeaufträge bleiben erhalten; keine pauschale Bereinigung der Warteschlange. Die obligatorische Archivrotation komprimierte alte Laufzeitberichte und die vorige Session-Memory; deren Version bleibt zusätzlich in Commit `0a9c99a8` nachvollziehbar.

Offen bleiben reale iOS-/Android-Geräte, ein echter Screenreader, der fachliche Abgleich von 53 inventarisierten Dokumenten, 84 überfällige Brücken (MSG-2026-0241), semantische Linkarbeit und RESEARCH-2026-004/007. Die April-Empfehlungen sind sichtbar überfällig; ihre spätere menschliche Freigabe wird nicht vorgetäuscht. Die erste Übergabemeldung nennt noch 57: Der abschließende Inventarabgleich berücksichtigt zusätzlich fünf geprüfte Leserportale und führt eine aktive Berichtsvorlage korrekt als Anleitung, nicht als historischen Bericht.

Die fünf bereits übernommenen unversionierten, sachfremden Dispatchdateien 0199 und 0254 bis 0257 bleiben außerhalb dieses Commits. Keine neuen Pakete oder Betriebsarchive einchecken. Bestehende beiden unveröffentlichten Vorgängercommits gehören zur beauftragten Veröffentlichung.
