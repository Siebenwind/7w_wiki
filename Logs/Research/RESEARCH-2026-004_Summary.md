# Forschungsbericht: RESEARCH-2026-004

- Datum: 2026-04-08
- Bearbeitet von: Historian
- Gegenstand: Causa **Tjure Odal** und **Arn Toron** im Umfeld der Verhaftung von [[Marnie_Ruatha]]

## Fragestellung
Rekonstruktion der belastbaren Historie von `Tjure Odal` und `Arn Toron` auf Basis der im Repo verfuegbaren Quellen, insbesondere des Bote-Strangs 167-186.

## Methode
- Manueller Quellenabgleich gegen:
  - `Quellen/Zeitung 7w Bote/Siebenwind Bote 167.md`
  - `Quellen/Zeitung 7w Bote/Siebenwind Bote 168.md`
  - `Quellen/Zeitung 7w Bote/Siebenwind_Bote_184.md`
  - `Quellen/Zeitung 7w Bote/Siebenwind Bote 186.md`
- Abgleich mit den abgeleiteten Wiki-Seiten unter `docs/Siebenwind_Wiki/`.
- `./7w_wiki.py search "Tjure Odal Arn Toron" --source all` wurde versucht, schlug in dieser Laufzeit aber fehl, weil der Oracle-Reranker nicht lokal gecacht war und keine Netzverbindung fuer den Modellnachzug bestand. Gemäß Historian-Fallback wurde daher auf direkte Quellenlektüre umgestellt.

## Befund: Arn Toron

### Quellensichere Punkte
- **Bote 184** nennt Toron wiederholt als **einstigen Konsul**.
- In derselben Ausgabe berichtet Toron:
  - von der Gewalteskalation in Falkensee,
  - von seiner **Flucht nach Brandenstein** nach einer Geiselnahme durch Viertler,
  - von Vermittlungs- und Ratsgesprächen mit Steinhauer, Custodias und Toran Dur,
  - und davon, dass er sich anschließend **gänzlich nach Brandenstein zurückzog**.
- **Bote 184** nennt ihn außerdem als Leiter des **Warenkontors Falkensee** und Sponsor des Ersonter Bellumsmarktes.
- **Bote 186** führt ihn in der Anklage gegen [[Marnie_Ruatha]] als einen der "bekannten Ketzer" an, deren Unterstützung ihr vorgeworfen wird.

### Einordnung
Arn Toron ist im ausgewerteten Quellenlauf keine leere Namenshülle, sondern eine politisch sichtbare Figur:
ehemaliger Konsul, Kaufmann, Gesprächspartner in der Falkenseer Krise und späterer Exilant in Brandenstein.

Die Bezeichnung als **"Ketzer"** ist in den geprüften Quellen **nur als Anklagebegriff** der Malthuster Wacht belegt.
Ein eigenständiger Beweis für häretische Lehre, dämonische Praxis oder magische Verbrechen wurde in diesem Lauf **nicht** gefunden.

## Befund: Tjure Odal

### Quellensichere Punkte
- **Bote 186** nennt Tjure Odal ausschließlich innerhalb der Vorwürfe gegen [[Marnie_Ruatha]]:
  - Marnie habe "bekannten Ketzern wie Arn Toron und Tjure Odal" geholfen.

### Nicht belegt im ausgewerteten Corpus
- keine gesicherte Herkunft
- kein Amt
- keine eigene Handlung
- kein eigener Auftritt vor oder nach Bote 186
- kein unabhängiger Nachweis von Ketzerei oder Magie

### Einordnung
Tjure Odal ist nach heutigem Repo-Befund **keine rekonstruierte Biografie**, sondern ein **einmalig genannter Anklagename**.
Im Unterschied zu Arn Toron trägt die Quellenlage hier **keinen** belastbaren Schluss auf Netzwerkrolle, Amt oder Charakter.

## Marnie-Ruatha-Kontext
- **Bote 167** zeigt [[Marnie_Ruatha]] als Hafenvogtess und Wahlkandidatin in Brandenstein.
- **Bote 183** zeigt sie als militärisch/politisch handlungsfähige Vertreterin Malthusts in Falkensee.
- **Bote 186** dokumentiert die Verhaftung durch Leutnant [[Erin_Caoimme]] und den anschließenden Kirchenschutz durch [[Custodias]].

Damit wirkt die Anrufung von `Arn Toron` und `Tjure Odal` in Bote 186 weniger wie eine isolierte Glaubensfrage und stärker wie Teil des politischen Machtkampfes zwischen Malthust, Brandenstein und dem erodierenden Falkenseer Ordnungsraum.

## Historiker-Gutachten
*Arn Toron ist als politische Figur und Exilant belastbar belegt; seine "Ketzer"-Markierung bleibt im geprüften Material jedoch eine Anschuldigung. Tjure Odal dagegen ist im aktuellen Corpus lediglich als Name in eben dieser Anschuldigung greifbar. Der saubere Befund lautet daher nicht "zwei bekannte Ketzer", sondern: ein namentlich fassbarer politischer Flüchtling und ein quellenarm bleibender zweiter Belastungsname im Marnie-Ruatha-Komplex.*

## Wiki-Folge
- `[[Arn_Toron]]` sollte als **politisch belasteter Ex-Konsul / Exilant** beschrieben werden, nicht als sicherer Ork-Verbündeter oder erwiesener Ketzer.
- `[[Tjure_Odal]]` muss explizit als **[UNGEKLAERT] / nur in Bote 186 genannt** geführt werden.
- Der derivative Hinweis in `Siebenwind_Bote_168.md`, Arn Toron sei dort bereits namentlich als Verräter gebrandmarkt, wurde in diesem Lauf nicht durch die Primärquelle bestätigt und sollte nicht als gesicherter Fakt weitergeführt werden.

## Offene Folgefragen
- Gibt es außerhalb des Bote-Strangs 167-186 noch eine weitere Primärquelle zu Tjure Odal?
- Falls `Arn Toron` in älteren oder parallelen Quellen doch explizit im Orkenkontext genannt wird, sollte dies gesondert nachgezogen werden statt aus der 186er Anklage rückwärts geschlossen zu werden.
