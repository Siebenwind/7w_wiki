# Changelog

#### [2026-10-22.01] - Leserrelease abschließen und Karamir berichtigen
### Prioritaet: P1
### Behoben
- Die erneute Einstiegsprüfung fand im Karamir-Artikel eine unbelegte Begleiterbiografie. Der Artikel beschreibt jetzt die in Bote 123 erzählte Rolle als Schöpfer der Bestie, seine Reue und den anschließenden Dienst im Vitamaorden. Veröffentlichungsdatum und Zeit der Erzählung bleiben getrennt.
- Arman verlinkt die korrigierte Figurenbeschreibung; die redaktionelle Nachprüfung bestätigte beide Artikel.
### Abschluss
- Auf ausdrücklichen Nutzerwunsch vom 22. Oktober erfolgen Commit, Push und Merge ohne weitere Testläufe. Die letzten Änderungen am Clean-Checkout-Fallback und an Karamir wurden nicht erneut durch die vollständige Testsuite geprüft; vorhandene frühere Nachweise und offene Geräteprüfungen bleiben im Übergabebericht getrennt ausgewiesen.

#### [2026-10-21.01] - Leserrelease abschließen und aktive Anleitungen berichtigen
### Prioritaet: P1
### Geändert
- Der noch unveröffentlichte Leserrelease vom September wird am aktuellen Stand erneut abgenommen. Artikelkontext verlinkt auflösbare Originalquellen; der Live-Vergleich umgeht alte zwischengespeicherte Buildmanifeste.
- Alle 53 bislang ungeprüften Dokumenteinträge wurden einzeln mit CLI und Implementierung abgeglichen. Aktive Style-, Ingestions-, Scout-, Auskunfts- und Score-Anleitungen sind berichtigt; historische Hypothesen und Kickoff-Anweisungen klar abgegrenzt. Laufende Aufgaben- und Forschungsregister bleiben aktiv.
- `repair --check-collision` wird nicht mehr als verfügbarer Befehl verlangt. `score` ist ausdrücklich als mutierende Metadatenheuristik dokumentiert. Ausschmückung, Tags und LQS erzeugen keine Quellenbestätigung.
- Historische Changelog-Aufrufe mit `search --fast` sind alte Laufnotizen und keine aktuelle Anleitung: Der heutige Search-Adapter besitzt diese Option nicht. Frühere Einträge bleiben als historische Evidenz erhalten.
- Ein frischer Checkout ohne lokalen Pages-Snapshot erzeugt vollständig gekennzeichnete unbekannte Messwerte statt eines Statistikabbruchs oder scheinbarer Nullfehler. Der Fall ist als Regression abgesichert.

#### [2026-09-12.01] - Leserzugang, statische Suche und redaktionelle Einstiege
### Prioritaet: P1
### Hinzugefügt
- Pagefind versorgt Suchvorschläge und vollständige Ergebnisse mit gemeinsamen Bereichsfiltern, Titel-/Aliasrangfolge und kanonischer Zusammenführung. Der Suchindex und gerenderte interne Verweise werden vor der Veröffentlichung geprüft.
- Leserstart, Welt entdecken, Themen A–Z und strukturierte Neuigkeiten erschließen das Archiv. Betriebsdiagnose und Dokumentationsinventar sind von den Leserstatistiken getrennt; Bauzeit und Commitkennung machen Veröffentlichungen nachprüfbar.
### Behoben
- Mobile Suchflächen, Dunkelmodus, Tastaturzugang und Scrolltabellen wurden repariert. Redaktionelle Abschnitte bleiben bei der Indexerzeugung erhalten; Brücken verdrängen keine regulären Artikel in Such- oder Kategorielisten.
- Die ersten Leserwege trennen aktuelle und historische Ortszustände, insbesondere Falkensee als Ruinenstadt. Quellenabgleiche korrigieren Brandenstein, Pantheon, Bellum, Zeitrechnung und die Verwechslung von Arman und Karamir.
- MSG-2026-0240 und MSG-2026-0259 sind technisch abgeschlossen: Brückenfristen erscheinen als eigene Befunde, Statuszahlen verwenden dieselbe datierte Snapshotquelle. Fünf nachweislich abgeschlossene Meldungen wurden einzeln als Information eingeordnet.
### Validiert
- 33 Standardsuiten und der vollständige Pages-Smoke-Test bestanden; die Browserprüfung bestand 39 Fälle in Chromium, Firefox und WebKit bei fünf Breiten und beiden Farbschemata.
- Die vollständige Pages-Validierung baut erfolgreich; der bekannte Linkaltbestand bleibt bei 621 ungelösten und 619 nicht freigestellten Zielen sichtbar. 84 überfällige Brücken bleiben ausdrücklich Altbestand.
- Redaktioneller Umfang, Dokumentationsinventar und Abnahmegrenzen stehen in `System/READER_RELEASE_REVIEW_2026-09-12.md`. Reale Mobilgeräte, echte Screenreader und die verbleibende Bestandsredaktion sind noch offen. Der Live-Nachweis folgt dem veröffentlichten Commit über `pages verify-live`.

#### [2026-09-02.01] - Forum-Fuenferlauf kanonisch uebergeben
### Prioritaet: P2
### Geaendert
- Der abgeschlossene Forum-Fuenferlauf aus Commit `318d94bc` wurde in eine neue Session-Memory uebernommen; Statistik, Ingestion-Tracking, Wiki-Inventar und Backlog-Snapshots wurden auf den geprueften Stand aktualisiert.
- Die Archivrotation verschob zwei erledigte Dispatches in das Dispatch-Archiv und verdichtete 93 aeltere Audit-, Snapshot- und Sessiondateien in die ignorierten Betriebsarchive.
- Die sachfremden, unversionierten Auftraege `MSG-2026-0199` sowie `MSG-2026-0254` bis `MSG-2026-0257` blieben ausserhalb des Handover-Commits.
### Erkenntnisse und Grenzen
- Dieser reine Uebergabelauf fuehrt keine neuen Loreaussagen ein. Er bestaetigt den quellenkritischen Stand des vorigen Fuenferlaufs und bewahrt dessen offene Historiker- und Technikfragen fuer getrennte Folgearbeiten.
- Der Pages-Linkaltbestand bleibt mit `621` unresolved und `619` unallowlisted Verweisen sichtbar; der Ratchet besteht, der Gesamtstatus bleibt deshalb `WARN`.
### Validiert
- Der kanonische `handover --run` und die vollstaendige Standardsuite bestanden; Audit: `issues_found = 0`.
- Pages-Bau: Exit `0`, Drift `PASS`, Publikationsfrische `1.418/1.418` Artikel und `120/120` Ingestion-Berichte; Link-Ratchet `PASS`.

#### [2026-08-23.03] - Forum-Fuenferlauf zu Aktenchronik, Ras Altanin und Thjareks Brecher
### Prioritaet: P2
### Hinzugefuegt
- `Thjareks_Brecher.md` erschliesst das nortravische Kriegsschiff erstmals als eigenstaendiges Lemma. Der Bote 190 bestaetigt die Schiffseinordnung; der Forumthread liefert den quellenkritisch begrenzten Bau- und Stationsverlauf.
- Fuenf Ingestion-Berichte dokumentieren Entity-Manifeste, Kollisionspruefung, Quellenvergleich, Dry-Runs und Synthesegrenzen fuer die Topics `106975`, `109430`, `109411`, `103341` und `99477`.
### Geaendert
- `Maichellis_Wanderstern.md`, `Ras_Altanin.md`, `Erynnion_Comari.md` und `Celedelair.md` wurden bevorzugt erweitert. Die Artikel trennen bestaetigte Boten- und Newsbefunde von Amtsberichten, inneren Monologen, theologischen Selbstdeutungen und arkanen Hypothesen.
- `Siebenwind_Bote_190.md` und `Zerstoerung_von_Westhever.md` behandeln den Brecher nicht mehr faelschlich als Siedlung. `Vänskap.md` und der Geschichtsindex verknuepfen Werft, Schiff und Westhever-Einsatz.
- Alle fuenf Quellen stehen im Forumregister auf `integrated`; damit sind 79 der 101 volltextarchivierten Themen integriert und 17 noch fachlich offen.
### Erkenntnisse und Grenzen
- Die Aktenchronik bestaetigt Maichellis als militaerischen Ermittler und Einsatzleiter, erlaubt aber keine sichere Gleichsetzung der verschieden datierten roten Lindwuermer.
- Die Langzeitchronik zu Tendarion enthaelt 292 archivierte Abschnitte, jedoch nur 172 eindeutige Post-IDs. Bote 191 und die Selbstbezeichnung „Silberglanz beziehungsweise Celetheyon“ stuetzen die Zuordnung zu Celedelair; Visionen und private Deutungen bleiben Perspektive.
- Die semantische Suche, die dokumentierte Kollisionsoption, die Pagination und der Widerspruch zwischen Draft-Dry-Run und Apply wurden als `MSG-2026-0245`, `MSG-2026-0249`, `MSG-2026-0250` und `MSG-2026-0252` an den Technician gemeldet. Historian-Fragen liegen unter `MSG-2026-0246` bis `MSG-2026-0248` und der Korrektur `MSG-2026-0251`.
### Validiert
- Lektorpruefung der fuenf Zielartikel, Sanitizer und Inhaltsvertrag: PASS.
- Vollstaendige Standardsuite: PASS; `forum-ingest-contract` bestaetigt Dry-Run-, Stil- und Finalisierungstore.
- `./7w_wiki.py audit --json`: `issues_found = 0`; der anschliessende Pages-Audit bestaetigte denselben fehlerfreien Stand.
- `pages-full-smoke`: PASS nach Korrektur von vier neu gesetzten Westhever-Linkzielen. Der volle Pages-Snapshot baut 1.418/1.418 Artikel und 120/120 Berichte, meldet `drift_status = PASS` und besteht den Link-Ratchet mit `621` unresolved / `619` unallowlisted. Der Gesamtstatus bleibt wegen des bekannten Altbestands `WARN`.

#### [2026-08-23.02] - GitHub-Pages-Clean-Checkout wiederhergestellt
### Prioritaet: P1
### Behoben
- `MSG-2026-0242` korrigiert den fehlgeschlagenen GitHub-Pages-Lauf `32663980650`: Das Dokumentenregister behandelt `.agent/data/pages_health.json` nun ausdruecklich als nicht versionierten Laufzeitsnapshot statt als aufloesbaren Repository-Link.
### Validiert
- Der fokussierte Linkvertrag bestand auch ohne den lokal vorhandenen Pages-Snapshot. Pages-Vertrag, Gesamttests und der vollstaendige lokale Pages-Bau wurden ebenfalls erfolgreich geprueft. GitHub-Pages-Lauf `32664796254` veroeffentlichte Commit `fad39420` erfolgreich; der Live-Abruf antwortete mit HTTP `200` und dem neuen Aenderungszeitpunkt.


#### [2026-08-23.01] - Handover, Pages-Vollsnapshot und Bridge-Restbestand
### Prioritaet: P1
### Hinzugefuegt
- Die Session-Memory `Logs/Archive/SESSION_MEMORY_2026-08-23_PAGES_AUDIT_UND_BRIDGE_RETIREMENT.md` uebergibt den aktuellen Pages-, Forum- und Historikerstand samt ausfuehrbaren Folgekommandos.
- `MSG-2026-0240` fragt den Technician, warum 84 ueberfaellige Bridge-Reviewdaten im Audit nicht als Lifecycle-Befund erscheinen.
### Geaendert
- Der Dispatch-Zaehler beruecksichtigt bei der Vergabe neuer IDs nun auch rotierte Nachrichten unter `DISPATCH/_archive`; dadurch bleiben Message-IDs nach einer Archivrotation global eindeutig.
- `MASTER_TASK_LIST.md` unterscheidet jetzt die abgeschlossene formale Bridge-Metadatenpflege von der weiterhin offenen Stilllegung der 84 temporaeren Bruecken.
- Statistik, Wiki-Inventar, Ingestion-Tracking, Werkzeugmanifest und der kalte Archivbestand wurden ueber die kanonischen Handover-Kommandos aktualisiert.
### Validiert
- Vollstaendige Standardsuite: PASS; der zunaechst an der 300-Sekunden-Grenze abgebrochene `pages-link-contract` bestand im fokussierten Wiederholungslauf mit `5/5` und danach auch im erneuten Gesamtlauf.
- Pages-Vollbau: Exit `0`, `drift_status = PASS`, Publikationsfrische `1417/1417` Artikel und `115/115` Ingestion-Berichte; Gesamtstatus `WARN` wegen des bekannten Linkaltbestands `622/620`.
- Audit: `issues_found = 0`, `bridge_inventory.total = 84`, `bridge_inventory.invalid = 0`; die ueberfaelligen Reviewdaten bleiben als erklaerungsbeduerftige Vertragsluecke offen.

#### [2026-08-06.02] - Pages-Pflegevertrag, Leserfokus und mobile Darstellung gehaertet
### Prioritaet: P1
### Hinzugefuegt
- Die Startseite zeigt unter dem kompakten Hero den letzten abgeschlossenen Historikerlauf als `Implementierte Neuerungen`, `Erkenntnisgewinn` und `Offen geblieben`; `./7w_wiki.py stats` synchronisiert diesen Block aus dem Changelog.
- Der Pages-Bericht vergleicht die sichtbare Artikel- und Ingestion-Zahl mit dem aktuellen Publishing-Baum und meldet veraltete statische Statistiken als Fehler.
- Ein Link-Ratchet setzt den bekannten Altbestand auf hoechstens `622` unresolved und `620` unallowlisted Verweise; abgelaufene Policy-Ausnahmen sind nun ein harter Fehler.
### Geaendert
- Mobile Kartenraster sind einspaltig, der Hero ist deutlich kuerzer, Bedienelemente sind beruehrungsfreundlich und breite Tabellen beziehungsweise Mermaid-Grafiken bleiben horizontal erreichbar.
- `docs/assets/custom.css` ist der einzige geladene Styling-Einstieg und importiert die portable Basis- sowie Material-Schicht in fester Reihenfolge.
- GitHub Pages verwendet den kanonischen Pages-Validierungspfad statt eines ungesicherten direkten MkDocs-Baus; generierte Kategorieindizes erhalten kuenftig uebereinstimmende Titel und H1.
### Validiert
- `reader-stats-contract`: PASS (3/3); `styling-surface-contract`: PASS.
- Pages-Vertrag, voller Pages-Bau, gerenderte Struktur-/Mobil-CSS-Pruefung und Commit-Hygiene: siehe zugehoerigen Session-Abschluss.

#### [2026-08-06.01] - Historikerlauf zu Volandur, Maichellis, Akassvae und Huns abgeschlossen
### Prioritaet: P2
### Hinzugefuegt
- Fuenf quellenkritische Erzaehlungsseiten erschliessen die Forumthemen `109571`, `109483`, `108944`, `109310` und `108788`; fuenf Ingestion-Berichte dokumentieren Quellenwert, Abgleich und offene Grenzen.
- `Volandur.md` erschliesst erstmals den pfadlosen Adepten und die von ihm beanspruchte Rolle als „Stimme der Fey“, ohne Selbstaussagen zu frueheren Morden, Magistratsregeln oder Dunquell als unabhaengig bestaetigte Tatsachen auszugeben.
### Geaendert
- `Claiomhs_Wacht.md` wurde aus einem Platzhalter zu einer belegten Burgseite mit Burghof, Katapult, Pferdehaltung und dem Angriff Rotschuppes und Aschehorns ausgebaut.
- `Maichellis_Wanderstern.md`, `Akassvae.md` und `Falkenwall.md` verbinden Maichellis' Forumchronik mit den Boten 191, 193 und 194. Akassvaes Jugend, Pferdejagd, Friedensverhandlungen und Umsiedlung sind nun nach Quellenrang getrennt; ihr Schlüpfen wird nicht mehr unbelegt auf einen exakten Zeitpunkt im Jahr 30 festgelegt.
- `Huns_Siebzehnruebl.md` ordnet die Boten 132/133 und das Tabenbuch gemeinsam als bewusst unzuverlaessige Selbstchronik ein und erweitert seine belegte Aktivitaetszeit von 16 bis 30 n.H. `Brandenstein.md` bewahrt den unbekannten Gewuerzkessel als begrenzte Marktueberlieferung.
- Alle fuenf Quellen stehen auf `integrated`; Personenregister, Forumregister, Ingestion-Tracking, Wiki-Inventar, Kategorieindizes und Leserstatistik wurden aktualisiert. Der Bestand umfasst 1.417 Wikiartikel und 115 abgeschlossene Ingestion-Berichte; 22 archivierte Volltexte warten noch auf fachliche Bearbeitung.
### Erkenntnisse und Grenzen
- „Geruechte ueber einen neuen Riesen“ belegt nur die Erzaehlung von einem sehr grossen Mann mit Hammer. Der Bestiariumsartikel zu Riesen wurde bewusst nicht veraendert, weil keine Volks- oder Artzugehoerigkeit nachweisbar ist.
- Maichellis' Bericht zum Angriff auf Claiomhs Wacht wird durch Bote 193 in zentralen Punkten bestaetigt. Der sehr aehnliche Brandensteiner Tod Rotschuppes steht in Bote 194, dessen Ausgabenjahr 36 n.H. aber nicht bruchlos zur Forumchronologie von 2019 passt; die Datierung bleibt offen.
- Volandurs Text ist stark fuer Selbstbild, Glaubenspraxis und persoenliche Entwicklung, aber einseitig fuer Tendarions Absichten, die Festnahme in Dunquell und Regeln des Magistrats.
- Huns ist ueber vierzehn Sonnenzirkeljahre als Figur fassbar. Medizinische Milchwirkungen, Alchemierezepte, Hofanspruch und Identitaet seiner bereisten Insel bleiben humoristische oder alkoholbeeinflusste Perspektive.
### Validiert
- Lektor und Sanitizer fuer alle neuen und inhaltlich geaenderten Seiten: PASS.
- `historian-closeout-contract`, `forum-ingest-contract`, `content-contract`, `source-tree-contract`, `render-hygiene`, `clean-client-state`, `reader-stats-contract`, `bridge-placeholder-guard` und `pages-full-smoke`: PASS.
- `./7w_wiki.py audit --json`: `issues_found = 0`; eine durch die Indexerneuerung entstandene Huns-Registerdublette und 20 Titel-/H1-Abweichungen wurden vor dem finalen Audit bereinigt.
- Voller MkDocs-Bau: Exit 0; Pages-Drift `PASS`. Der bekannte globale Altbacklog bleibt unveraendert bei `622` unresolved / `620` unallowlisted / `609` needs historian.
- Repo-Hygiene klassifiziert `site/` als ignoriertes Buildprodukt; es ist kein Bestandteil der Wiki-Quelle. Die semantische Suche blieb wegen des bekannten fehlenden Modellcaches (`MSG-2026-0192`) nicht verfuegbar.

#### [2026-08-05.03] - Historikerlauf zu Haus 9, Valkun, Angamon und Goblinmedizin abgeschlossen
### Prioritaet: P2
### Hinzugefuegt
- Fuenf quellenkritische Erzaehlungsseiten erschliessen die Forumthemen `109785`, `106019`, `81975`, `109582` und `109574`; fuenf Ingestion-Berichte dokumentieren Quellenabgleich, Synthesegrenzen und Zielentscheidungen.
- `Haus_9_in_Brandenstein.md` verbindet die amtlich belegte Hausnummer `BS 09` mit dem begrenzten Forumbericht ueber einen gescheiterten Einbruch und kleine Spinnen im Jahr 33 n.H., ohne Bewohner oder Zusammenhaenge mit anderen Plagen zu erfinden.
### Geaendert
- `Angamon.md` folgt nun wieder der aktuellen Homepage: Angamon will die Schoepfung beherrschen statt vernichten, unterwarf Daemonen und wird nach dem Goetterwandel nicht mehr automatisch als Haeresie verfolgt. Die Darstellung trennt zugleich seine uneinheitlichen Stroemungen und die selbstdienlichen Forumzeugnisse.
- `Schattenhand.md` und das Organisationsregister fuehren die Schattenhand nicht mehr unbelegt als Diebesgilde. Sie unterscheiden den amtlich genannten Gruppennamen, den Propheten Schattenhand und Valkuns behaupteten inneren Kreis; ob diese Verwendungen dieselbe Organisation bezeichnen, bleibt offen.
- `Falkensee.md`, `Falkenwall.md`, `Brandenstein.md`, `Enoah_Sullin.md`, `Die_Saeulen_des_Valkun.md` und `Goblins.md` erhielten neue, nach Quellenrang begrenzte Zusammenhaenge. Der Goblinartikel bewahrt nun auch medizinische und artuebergreifende Beziehungen, ohne die unbekannte Gestalt aus dem Zeltbericht zum Goblin zu erklaeren.
- Alle fuenf Forumquellen stehen auf `integrated`; Forumregister, Ingestion-Tracking, Wiki-Inventar, Kategorieindizes und Leserstatistik wurden aktualisiert. Der Bestand umfasst nun 1.411 Wikiartikel und 110 abgeschlossene Ingestion-Berichte; 27 archivierte Volltexte warten noch auf Historikerbearbeitung.
### Erkenntnisse und Grenzen
- `Dunkle Tage, Lichte Naechte` verbindet Valkuns fruehe Angamonis-Zeit mit dem spaeteren Saeulenkomplex und ueberliefert seinen Tod durch zwei Daemonen. Seine Aussagen zu Toran Dur, Selanus, Kairodun, Seuchenratten und der Entweihung Falkensees bleiben jedoch eine selbstrechtfertigende Binnenperspektive.
- Eine zweite Forumquelle behauptet nun ausdruecklich, Luth Chalid sei auf Falkensees Ruinen entstanden und nach Chalid Mez Tulameth benannt worden. Die Homepage bestaetigt Luth Chalid als zerstoerte Wuestenstadt, aber nicht die Identitaet mit Falkensee; die Rekonstruktion ist damit stark gestuetzt, nicht amtlich entschieden.
- `Weg in den Wahnsinn` zeigt ueber elf Jahre hinweg Trauma, Erinnerungsluecken und einen spaeten Angamon-Ritus. Weder die Identitaet der Frau noch eine goettliche Ursache ihrer Stimmen und Traeume ist belegt.
- Die beiden kurzen Mitmachthemen erweitern Alltagswissen: ein ungewoehnlich kraeftiger, maskierter Lagerbewohner bleibt trotz Rohdateinamen unidentifiziert; Kruras' chronische Krankheit und seine Suche nach dem Heiler Garub belegen goblinische Heilpraxis und Kontakte zu Echsen, Gruenorken, Schwarzorken und Trollen, aber weder Diagnose noch Heilung.
### Validiert
- Sanitizer und Lektor fuer alle neuen und inhaltlich geaenderten Seiten: PASS; nach der Indexerneuerung wurden 20 rein formale Titel-/H1-Abweichungen bereinigt.
- `historian-closeout-contract`, `forum-ingest-contract`, `content-contract`, `source-tree-contract`, `render-hygiene`, `clean-client-state`, `reader-stats-contract`, `bridge-placeholder-guard` und `pages-full-smoke`: PASS.
- `./7w_wiki.py audit --json`: `issues_found = 0`; zielbezogene Historian-Dry-Runs melden keine offenen Verweise. Nur das Organisationsregister fuehrt sieben bereits vorher offene Akademie-/Ordensziele ausserhalb dieses Laufs.
- Pages-Vertrag: `drift_status = PASS`; der bekannte globale Altbacklog liegt bei `622` unresolved / `620` unallowlisted und damit unter dem vorherigen Stand. Die lokale semantische Suche blieb wegen des bereits gemeldeten fehlenden Modellcaches nicht verfuegbar; der Abgleich erfolgte direkt gegen Quellenbestand und Homepage.

#### [2026-08-05.02] - Historikerlauf zu Traumtagebuch, Blutrache, Trauerschiffen und Morsanschrein abgeschlossen
### Prioritaet: P2
### Hinzugefuegt
- Fuenf quellenkritische Erzaehlungsseiten erschliessen die Forumthemen `109847`, `109858`, `109841`, `109833` und `109818`; fuenf Ingestion-Berichte sichern Quellenabgleich, Synthesegrenzen und Zielentscheidungen.
- `Morsanschrein_in_Brandenstein.md` fuehrt die verstreuten Perspektiven zu Lage, stiller Andacht, Schlaf und Traumbeobachtung an einem gemeinsamen Ortsziel zusammen.
### Geaendert
- `Falkensee.md` beschreibt die Stadt nach Abgleich mit Homepage und offiziellen Nachrichten nicht mehr als gegenwaertige Hauptstadt, sondern als ehemalige Hauptstadt und heutige Ruine.
- `Morsan.md` wurde auf die offiziell belegten Aspekte Tod, Ruhe, Schlaf, Traeume und Zeit sowie die ueberlieferte stille Andacht ausgerichtet; die Forumgeschichte dient als begrenztes Praxisbeispiel.
- `Falkenwall.md`, `Goblins.md`, `Elementare.md`, `Brandenstein.md`, `Tevra.md`, `Neues_Chaos_auf_Tevras_Pfaden.md`, `Adhemar_Ravenforth.md`, `Rolosin_Vadebor.md` und das Personenregister erhielten neue, quellenkritisch begrenzte Zusammenhaenge.
- Alle fuenf Forumquellen stehen auf `integrated`; Forumregister, Ingestion-Tracking, Wiki-Inventar, Kategorieindizes und Leserstatistik wurden aktualisiert. Der Bestand umfasst nun 1.406 Wikiartikel und 105 Ingestion-Berichte.
### Erkenntnisse und Grenzen
- `109841` liefert den unmittelbaren Ausloeser fuer `109858`: Der Wolf toetet bei Falkenwall einen Goblin-Spaehtrupp samt Anfuehrer. Die Fortsetzung zeigt Blutrache als Frage von Stammesansehen, Stellvertretern und politischer Umdeutung; Identitaet des Wolfs und Bedeutung des „Kaezarbluts“ bleiben offen.
- Die in `109833` aus Bernstein angekuendigten zwei Trauerschiffe entsprechen nach Zahl, Fahrtrichtung und Zeitabstand sehr wahrscheinlich den zehn Tage spaeter in `109841` eintreffenden Schiffen. Passagiere und eine Beteiligung der Museumselfen sind nicht belegt.
- Das Traumtagebuch bildet eine Vorgeschichte zu Winnis spaeterer Tevra-Pilgerfahrt. Die Beziehung zwischen Sah'lien, Buochwin und Winni sowie der objektive Status der Traeume bleiben ausdruecklich ungeklaert.
- Die Reinigungserzaehlung und weitere Forumquellen zeigen den Brandensteiner Morsanschrein als Ort stillen Dienstes, der Meditation, des Schlafs und der Traumbeobachtung. Ob alle Texte denselben Schrein meinen, ist plausibel, aber nicht bewiesen.
### Validiert
- Lektor und Sanitizer fuer alle beruehrten Inhaltsseiten: PASS.
- `historian-closeout-contract`, `forum-ingest-contract`, `content-contract`, `source-tree-contract`, `render-hygiene`, `clean-client-state` und der Vertragstest zur Leserstatistik: PASS.
- `./7w_wiki.py audit --json`: `issues_found = 0`; `pages-full-smoke`: PASS.
- Zielbezogene Historian-Dry-Runs melden fuer alle neuen und geaenderten Seiten keine offenen Verweise. Der globale Pages-Stand bleibt bei bestandenem Drift-Vertrag wegen des bekannten Altbacklogs WARN; der letzte Vollsnapshot entstand noch vor der Korrektur zweier Maquira-Verweise.

#### [2026-08-05.01] - Historiker-Abschlusszusammenfassung als Pflichtvertrag kodifiziert
### Prioritaet: P2
### Hinzugefuegt
- `System/Templates/HISTORIAN_CLOSEOUT_TEMPLATE.md` definiert fuer jeden Historiker-Durchlauf die getrennten Pflichtabschnitte `Implementierte Neuerungen` und `Erkenntnisgewinn`.
- `historian-closeout-contract` prueft Workflow, Persona, Lore-Gelehrter-Skill, Governance, Vorlage, Registrierung und generierten Codex-Adapter.
### Geaendert
- Historiker-Workflow, Persona und Lore-Gelehrter verlangen nun eine nutzergerichtete, inhaltlich erklaerende Abschlusszusammenfassung statt einer reinen Datei-/Mengenzaehlung.
- Fehlende Implementierung oder fehlender Erkenntnisgewinn muessen im jeweiligen Pflichtabschnitt ausdruecklich begruendet werden; offene Punkte, Pruefstatus, Dispatch und Session-Memory sind nur Ergaenzungen.
- Testdokumentation und Koordinationsregister fuehren den neuen Vertrag als kanonische Oberflaeche.
### Validiert
- `historian-closeout-contract`: PASS mit 4/4 Faellen.
- Katalog, Codex-Skills und Workflow-Matrix wurden ueber die kanonischen `tech`-Synchronisationspfade aktualisiert.
- `./7w_wiki.py test --suite all`: PASS einschliesslich Katalog-, Adapter-, Historian-, Dispatch- und Interop-Vertraegen.

#### [2026-08-04.05] - 41 Forumvolltexte archiviert und nächsten Historikerlauf vorbereitet
### Prioritaet: P2
### Hinzugefügt
- 41 weitere Forumthemen wurden als lesbare Volltextquellen archiviert; 51 HTML-Rohseiten bewahren die quellentreuen Originalseiten mehrseitiger Threads.
- `MSG-2026-0229` übergibt dem Historian das nächste Fünferpaket: `31020`, `48524`, `109905`, `107595` und `109867`.
### Geändert
- Der Forumstand liegt bei `201` Themen, `101` Volltexten, `59` fachlichen Abschlüssen, `42` offenen Sichtungen und `100` Metadatensätzen.
- `MASTER_TASK_LIST.md` und der allgemeine Forum-/Backlogbericht nennen nun den nächsten zulässigen Metadatenkandidaten `108636`; `104857` bleibt wegen seiner Dublettenentscheidung übersprungen.
- Vier Quellen des vorbereiteten Fünferpakets stehen auf `triage_ready`; `31020` bleibt als ältester offener Volltext an erster Stelle.
### Validiert
- Volltextarchivierung: `41` neue Themen, `0` Fehler.
- Einzelinspektion: drei `historian_required`, ein `update_existing`, ein vorläufiges `create_article`; keine menschliche Eskalationspflicht.
- `./7w_wiki.py audit --json`: `issues_found = 0`.
- Vollständige Testsuite einschließlich `forum-ingest-contract`, `historian-review-contract`, `source-tree-contract`, `content-contract` und `render-hygiene`: PASS.
- Pages-Vertrag: `624` unresolved / `622` unallowlisted / `611 needs_historian`, `drift_status = PASS`.
- Statistik, Archivrotation und Werkzeugmanifest wurden für den Session-Handover aktualisiert.
- Lektor für den aktualisierten Lagebericht und `git diff --check`: PASS.

#### [2026-08-04.04] - Gesamtstatus zu Forum-Ingestion und Backlogs commitbereit dokumentiert
### Prioritaet: P2
### Hinzugefügt
- `Logs/STATUSBERICHT_2026-08-04_FORUM_INGESTION_UND_BACKLOG.md` quantifiziert Forumfortschritt, Historiker-, Research-, Pages- und Koordinationsbacklog.
### Geändert
- `MASTER_TASK_LIST.md` auf `54` Forum-Integrationen, `141` Metadatenreste, zwei ausstehende Newsquellen und den aktuellen Pages-Stand `624/622` angehoben.
- Der Statistiklauf erfasst nun `1.397` Artikel und `95` vollständig getrackte Ingestion-Berichte; die fünf jüngsten Historikerberichte erhielten den kanonischen Trackingblock.
### Hygiene
- Keine versionierten Buildartefakte gefunden; `site/`, Laufzeitcaches und virtuelle Umgebungen bleiben ignoriert.
- Forum-Raw-HTML bleibt als Quellenbeleg im Commit, die sachfremde unversionierte Dispatchdatei `MSG-2026-0199` bleibt ausgeschlossen.

#### [2026-08-04.03] - Forum-Historikerbatch zu Hadernblättern, Falkenwall, Avindhrell und Maichellis abgeschlossen
### Prioritaet: P2
### Hinzugefügt
- `Geschichten_auf_1001_Hadernblatt.md` trennt drei endophalisch geprägte Lehrgeschichten von einer bestätigten historischen Chronik.
- `Zaertliche_Cousinen.md` bewahrt den Falkenseer Einbruch vom 3. Trier 27 n.H., ohne Täter, Kartenzeichen oder Verwandtschaft zu erfinden.
- Fünf Berichte dokumentieren Quellenabgleich und Zielentscheidungen für die Topics `104750`, `104898`, `104852`, `104864` und `104860`.
### Geändert
- `Falkenwall.md` erhielt den Skelettangriff des Jahres 27 n.H. als klar begrenzte Forumsperspektive neben dem zeitnahen offiziellen Wochenüberblick.
- Die Platzhalter `Auenelfen.md` und `Avindhrell.md` wurden anhand des offiziellen Hintergrunds ausgebaut; Forum und News ergänzen den datierten Krisenbefund.
- `Maichellis_Wanderstern.md` führt nun die belegten Stationen als Obergefreiter, Vogt und militärischer Koordinator; unbelegte Charakterdeutung und zugeschriebenes Zitat wurden entfernt.
- Alle fünf Forumquellen stehen auf `integrated`; der Erzählungsindex erschließt die beiden neuen Seiten.
### Validiert
- `./7w_wiki.py audit --json`: `issues_found = 0`
- Lektor und Sanitizer für alle sieben berührten Wiki-Seiten: PASS
- `forum-ingest-contract`, `historian-review-contract`, `content-contract`, `source-tree-contract`, `render-hygiene`, `bridge-placeholder-guard` und `clean-client-state`: PASS
- `pages-full-smoke`: PASS; direkte Pages-Validierung mit erfolgreichem Build, `drift_status = PASS` und bekanntem globalem Backlog von `624` unresolved / `622` unallowlisted
- `git diff --check`: PASS

#### [2026-08-04.02] - Forum-Historikerbatch zu Endophali, Bärenkampf, Balian und Waldhütte abgeschlossen
### Prioritaet: P2
### Hinzugefügt
- `Die_Felsen_in_der_Brandung.md` bewahrt Sidras Schutzpraxis und die Spannungen um Jamar, Sarana und Valkun, ohne Figurenmagie oder Schuldzuweisungen zu kanonisieren.
- `Im_Wuestensand.md` dokumentiert die Selbstprüfung eines namenlosen endophalischen Ratsführers; Autorenkonto und lokale Machtverhältnisse werden nicht als Identitäts- oder Kanonbeleg verwendet.
- `Baerenkampf_westlich_von_Brandenstein.md` trennt vier zeitgleiche Threadbeiträge von einer unbelegten lückenlosen Kausalkette.
- `Balian_Ruhnbert.md` führt Rückkehr, Handwerk und die nur plausible Verbindung zu Balians Gesellschaftsentwurf quellenkritisch zusammen.
- `Eine_Huette_in_der_Wildnis.md` erschließt die offene Waldhütte, ohne Bewohnerin oder Besucher aus Forenkonto und Spuren zu erfinden.
- Fünf Berichte dokumentieren Quellenabgleich und Zielentscheidungen für die Topics `105159`, `105188`, `105132`, `105060` und `105023`.
### Geändert
- `Balians_Gesellschaftsentwurf.md` und `Saranas_Tod.md` erhielten die jeweils zeitnahen ergänzenden Perspektivquellen.
- Erzählungs-, Personen- und kanonisches Personenregister erschließen alle neuen Ziele.
- Alle fünf Forumquellen und die Dispatches `MSG-2026-0216` bis `MSG-2026-0220` stehen auf `integrated` beziehungsweise `DONE`.
### Beobachtet
- `MSG-2026-0221`: Der vollständige Pages-Snapshot stieg global auf `625` unresolved / `623` unallowlisted, obwohl zielbezogene Dry-Runs für alle neuen Seiten und Register jeweils `0` Residuen melden. Die Abweichung ist an den Techniker geroutet; `drift_status = PASS`.
### Validiert
- `./7w_wiki.py audit --json`: `issues_found = 0`
- Lektor und Sanitizer für alle produktiven Zielseiten: PASS
- `forum-ingest-contract`, `historian-review-contract`, `content-contract`, `source-tree-contract`, `render-hygiene`, `bridge-placeholder-guard` und `clean-client-state`: PASS
- `pages-full-smoke --timeout 360`: PASS; zielbezogene Historian-Dry-Runs ohne offene Verweise
- `git diff --check`: PASS

#### [2026-08-04.01] - Forum-Historikerbatch zu Hospiz, Lucy, Seefahrt, Gesellschaft und Sarana abgeschlossen
### Prioritaet: P2
### Hinzugefügt
- `Die_Nacht_im_Hospiz_von_Brandenstein.md` bewahrt die mehrstimmige Krankenpflege-Erzählung, ohne die unbenannte Seuche mit dem Atmenden Tod gleichzusetzen.
- `Im_starken_Schutz_des_Hoechsten.md` sichert die Kapitänserzählung; die motivische Nähe zu Lazalantin bleibt ausdrücklich ungeklärt.
- `Balians_Gesellschaftsentwurf.md` dokumentiert Organisationsidee und Satzungsentwurf, ohne eine tatsächliche Gründung zu behaupten.
- `Saranas_Tod.md` führt den elfteiligen Thread und die stützende Briefkorrespondenz quellenkritisch zusammen.
- Fünf Berichte dokumentieren Quellenabgleich und Zielentscheidungen für die Topics `105371`, `105249`, `105164`, `105219` und `105214`.
### Geändert
- `Lucy.md` trennt den Botenbeleg zur späteren Vogtin von einer nur plausibel zugehörigen frühen Forumüberlieferung.
- `Briefe_an_einen_Vitamageweihten.md` verweist nun auf den direkten Mehrperspektivthread zu Sarana; der Erzählungsindex erschließt alle vier neuen Seiten.
- Alle fünf Forumquellen und die Dispatches `MSG-2026-0208` bis `MSG-2026-0212` stehen auf `integrated` beziehungsweise `DONE`.
### Behoben
- `MSG-2026-0213`: Forum-Ton des Hospizartikels und Legacy-Frontmatter/H1 des Erzählungsindex korrigiert.
- `MSG-2026-0214`: Einen neu eingeführten, unbelegten `[[Rilamnor]]`-Link entfernt und den Pages-Zähler auf das Ausgangsniveau zurückgeführt.
### Validiert
- `./7w_wiki.py audit --json`: `issues_found = 0`
- Lektor und Sanitizer für alle sieben berührten Zielseiten: PASS
- `forum-ingest-contract`, `historian-review-contract`, `content-contract`, `source-tree-contract`, `render-hygiene`, `bridge-placeholder-guard` und `clean-client-state`: PASS
- Finaler `pages-full-smoke --timeout 360`: PASS; Fast-Snapshot bei `624` unresolved / `622` unallowlisted und `drift_status = PASS`

#### [2026-08-02.02] - Fünf Historikerfälle zu Falkenwall, Angamon und Aschespuren abgeschlossen
### Prioritaet: P2
### Hinzugefügt
- `Ibralosch_Goldfaust.md` dokumentiert den Dwarschim-Krieger und seine Beteiligung an Belagerung und Fall des Falkenwalls als klar begrenzte Figurenperspektive.
- `Akademie_zur_Linken.md` trennt den durch den Boten belegten Institutionsbestand von den parteilichen Führungs- und Kongressansprüchen der Forumquelle.
- `Aschespuren_in_Luth_Chalid_und_Brandenstein.md` führt zwei auffällig ähnliche, aber ungeklärte Vorfälle zusammen, ohne Täter oder Motiv zu erfinden.
- Fünf Historikerberichte sichern Quellenabgleich und Zielentscheidungen für die Topics `110194`, `105411`, `105233`, `105471` und `105386`.
### Geändert
- `Falkenwall.md` erhielt die Verteidigungs- und Fallchronologie aus Ibraloschs Sicht; der offiziell bestätigte Endzustand bleibt davon getrennt.
- `Bruderschaft_der_Tardukai.md` ordnet „Hinter dem Spiegel“ als ergänzende Binnenperspektive zur schwarzen Festung ein; die geschilderte Buße wird nicht zur allgemeinen Ordensregel erklärt.
- Personen-, Organisations- und Kategorieindizes wurden um die neuen Ziele ergänzt; alle fünf Forumquellen stehen auf `integrated`.
### Behoben
- Der zunächst verwaiste Personenartikel zu Ibralosch wurde quellenbezogen im Personenregister verankert (`MSG-2026-0205`).
- Eine auftragsfremde Abweichung zwischen aktueller Angamon-Homepage und Wiki wurde nicht still verändert, sondern als Kanonfrage `MSG-2026-0204` geroutet.
### Validiert
- `./7w_wiki.py audit --json`: `issues_found = 0`
- Lektor und Sanitizer für alle produktiven Zielseiten: PASS
- `forum-ingest-contract`, `historian-review-contract`, `content-contract`, `source-tree-contract`, `render-hygiene`, `bridge-placeholder-guard` und `clean-client-state`: PASS
- `pages-full-smoke --timeout 360`: PASS; Fast-Snapshot unverändert bei `624` unresolved / `622` unallowlisted und `drift_status = PASS`
- Der direkte Pages-Vollbefehl blieb erneut ohne Ausgabe und wurde kontrolliert abgebrochen; die bekannte Runtime-Frage bleibt unter `MSG-2026-0195` offen.

#### [2026-08-02.01] - Drei Historikerfälle zu Tardukai und Falkenwall abgeschlossen
### Prioritaet: P2
### Hinzugefügt
- `Die_Saeulen_des_Valkun.md` dokumentiert den mehrstimmigen Forumkomplex als Perspektivquelle; die monoalphabetisch verschlüsselten Beiträge sind quellenkritisch eingeordnet.
- Drei Historikerberichte sichern Entity-Manifeste, Quellenabgleich, Synthesegrenzen und Zielentscheidungen für die Topics `109946`, `109948` und `109969`.
### Geändert
- `Ewigwacht.md`, `Bruderschaft_der_Tardukai.md`, `Enoah_Sullin.md` und `Falkenwall.md` wurden um die belastbaren Ergebnisse der drei Fälle ergänzt.
- Die offiziellen Angamon- und Patchquellen bleiben führend; Verträge, Rituale, Verratsvorwürfe und die behauptete Urheberschaft des „Archivars“ sind ausdrücklich als Forumsperspektive begrenzt.
- `MSG-2026-0170`, `MSG-2026-0176` und `MSG-2026-0177` sowie die zugehörigen Forumquellen stehen auf `DONE` beziehungsweise `integrated`.
### Behoben
- Drei zunächst offene `[[Necris]]`-Links zeigen nun ohne Brückenseite auf das bestehende kanonische Ziel `[[Region_Morthum|Necris]]`.
### Validiert
- `./7w_wiki.py audit --json`: `issues_found = 0`
- Lektor und Sanitizer für alle fünf berührten Wikiartikel: PASS
- `forum-ingest-contract`, `historian-review-contract`, `content-contract`, `source-tree-contract`, `render-hygiene`, `bridge-placeholder-guard` und `clean-client-state`: PASS
- `pages-full-smoke` mit angepasstem Zeitlimit: PASS; aktueller Pages-Snapshot wieder auf dem Ausgangsniveau `624` unresolved / `622` unallowlisted, `drift_status = PASS`
- `git diff --check`: PASS


*Ältere Einträge siehe `System/_archive/CHANGELOG_2026-02_bis_2026-07.md`.*
