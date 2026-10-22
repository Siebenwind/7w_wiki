# Übergabe: Leserrelease und Dokumentationsabgleich

Stand: 21. Oktober 2026. Fortsetzung des ausdrücklich beauftragten Leserplans einschließlich Commit, Push und anschließender Auswertung. Branch: `main`; Ausgangscommit `0a9c99a8b126d17530425a584916d74471424706`. Die beiden bereits vorhandenen unveröffentlichten Vorgängercommits gehören zur Veröffentlichung.

## Ergebnis und Nachweise

Pagefind, mobile und dunkle Leseroberflächen, Themenzugänge, gemeinsame Suchlogik, Quellenkontext, strukturierte Neuigkeiten und gezielte Prozessreparaturen werden zusammen veröffentlicht. Die redaktionelle Nachprüfung der ersten Leserwege korrigiert unter anderem Falkensee als Ruinenstadt sowie Arman/Karamir, Brandenstein, Pantheon und Zeitrechnung. Quellen, Vorher-/Nachher-Befunde und Grenzen: `System/READER_RELEASE_REVIEW_2026-09-12.md`.

Die 53 im September noch ungeprüften Dokumenteinträge wurden einzeln gegen CLI, Implementierung und Dateibaum abgeglichen. Nach Korrektur und unabhängiger Nachprüfung enthält das Inventar 67 aktuelle und 24 ausdrücklich historische Texte. Insbesondere werden die nicht vorhandene Kollisionsoption, die mutierende Score-Heuristik und unbelegte Kanonversprechen nicht länger als aktive Anweisung weitergegeben. Historische Texte bleiben als solche erhalten. Der Dokumentationstestagent bestätigte den Abschluss in `7w_documentation_review_20261021.md` im System-Temporärverzeichnis.

Ein zuletzt erkannter Clean-Checkout-Fehler ist repariert: Ohne lokalen Pages-Snapshot liefert die gemeinsame Diagnose alle erwarteten Felder mit unbekannten Messwerten. Die Statistikerzeugung darf deshalb weder abbrechen noch null offene Links behaupten. Der isolierte Regressionstest deckt diesen Zustand ab.

## Lokale Abnahme

- Audit Exit 0, `issues_found = 0`; Lifecycle-Warnungen und Linkaltbestand ausdrücklich getrennt. Initialer Bericht: `333943fe-adf3-4bd7-98db-529712a536bb`.
- Vollständiger Pages-Smoke-Test Exit 0; `TEST_pages-full-smoke_2026-10-21_235021.md` im temporären Verzeichnis `7w_test_7znjebtd`. Snapshotzeit: `2026-10-21T21:50:21Z`.
- Pages-Gesamtstatus WARN: 612 ungelöste, davon 610 nicht freigestellte Linkvorkommen. Ratchet und technischer Drift PASS. Gegenüber dem ursprünglichen Planstand 621/619 kein Wachstum.
- 2.633 generierte HTML-Seiten, keine fehlenden internen Linkziele im gerenderten Bestand. Historische Verweise in unverändertem Quellen-HTML werden gesondert geführt.
- Pagefind-Index PASS, 2.539 indexierte Seiten. Der lokale Build gehört zum noch uncommitteten Arbeitsstand und ist kein Deploymentnachweis.

Die ersten Browserstarts scheiterten an Sandbox-Portbindung beziehungsweise fehlenden Browserdateien; daraus wurde kein Urteil zur Website abgeleitet. Der beauftragte Testagent wurde anschließend zweimal durch ein Nutzungslimit unterbrochen. Die abschließende neue Browsermatrix und die erneute vollständige Regression nach dem Clean-Checkout-Fix sind deshalb nicht als bestanden nachgewiesen.

## Abschluss am 22. Oktober

Der Nutzer beauftragte die Übernahme von Astra, Commit, Push und Merge ausdrücklich **ohne weitere Tests**. Es werden keine zusätzlichen lokalen Testläufe gestartet und keine vorhandenen GitHub-Schutzmechanismen umgangen. Der Übergabebericht unterscheidet die bereits abgeschlossenen Nachweise vom nicht erneut vollständig geprüften letzten Stand.

Die zusätzliche redaktionelle Prüfung bestätigte die ersten Leserwege und fand eine unbelegte Begleiterbiografie in Karamir. Sie wurde anhand des direkt gelesenen Boten 123 berichtigt; Arman verlinkt die korrigierte Seite. Eine unabhängige redaktionelle Nachprüfung bestätigte beide Artikel. Der Quellenabgleich stellt auch klar, dass das Veröffentlichungsdatum der Zeitung kein Ereignisdatum der mit „vor langer Zeit“ eingeleiteten Erzählung ist.

Die Veröffentlichung erfolgt über einen eigenen `codex/`-Branch und Pull Request nach `main`, einschließlich der zwei bereits vorhandenen unveröffentlichten Vorgängercommits. Die fünf sachfremden Dispatchdateien bleiben ausgeschlossen.

## Veröffentlichung und offene Grenzen

Nach dem Commit und Push muss der GitHub-Pages-Workflow erfolgreich sein. Sein Schritt `Verify delivered build identity` und `./7w_wiki.py pages verify-live --commit <Release-Commit>` müssen die tatsächlich ausgelieferte Commitkennung bestätigen. Zusätzlich werden die ersten Leserwege auf der veröffentlichten Website im Browser geprüft. Diese Übergabe behauptet keine vorweggenommene Live-Abnahme.

Reale iOS-/Android-Geräte und ein echter Screenreader stehen nicht zur Verfügung. Menschliche Freigabe der Empfehlungen, 84 überfällige Brücken, semantischer Linkrückstand, RESEARCH-2026-004/007 und Oracle bleiben getrennte Folgearbeiten. Die geprüften Einstiege sind keine fachliche Zertifizierung des gesamten Archivs.

MSG-2026-0240 und MSG-2026-0259 sind technisch abgeschlossen; fünf belegte Abschlussmeldungen wurden einzeln als INFO eingeordnet. Die fünf sachfremden unversionierten Dateien MSG-2026-0199 und MSG-2026-0254 bis 0257 bleiben unverändert außerhalb des Commits. September-Übergabe und damalige Rotation sind in `Logs/Archive/SESSION_MEMORY_2026-09-12_LESERZUGANG.md` dokumentiert.
