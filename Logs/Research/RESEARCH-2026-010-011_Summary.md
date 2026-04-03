# Forschungsbericht: RESEARCH-2026-010 / RESEARCH-2026-011

- Datum: 2026-04-03
- Bearbeitet von: Historian
- Auftrag: `MSG-2026-0005`

## Gegenstand
Abgleich der Themen **Götterverschmelzung / Astraels Aufstieg** und **Waldelfen-Exodus / Myten-Verbleib** zwischen:

1. aktuellem Live-Kanon auf `www.siebenwind.de` (geprüft am 2026-04-03),
2. älteren offiziellen News-/Hintergrundquellen im Repo,
3. aktuellem Wiki-Bestand unter `docs/Siebenwind_Wiki/`.

## Methode
- Live-Abgleich gegen die Homepage:
  - `https://www.siebenwind.de/hintergrund/gotterwelt/kirche-der-viere/`
  - `https://www.siebenwind.de/hintergrund/rassen-und-klassen/waldelfen/`
  - `https://www.siebenwind.de/hintergrund/rassen-und-klassen/myten/`
- Repo-Abgleich gegen archivierte offizielle Quellen:
  - `docs/Quellen/News/2015-02-01_Was_bisher_geschah_Stand_1_Februar_2015.md`
  - `docs/Quellen/News/2018-10-21_Agenda_2018_2019.md`
  - `docs/Quellen/Hintergrund/Waldelfen | Siebenwind | Ultima Online Freeshard | Siebenwind.md`
  - `docs/Quellen/Hintergrund/Myten | Siebenwind | Ultima Online Freeshard | Siebenwind.md`
  - `docs/Quellen/Hintergrund/Kirche der Viere | Siebenwind | Ultima Online Freeshard | Siebenwind.md`
- Oracle-Abgleich via `./7w_wiki.py search --fast`, da der Default-Reranker in dieser Laufzeit nicht lokal gecacht war.

## RESEARCH-2026-010: Götterverschmelzung & Astraels Aufstieg

### Befund
- Der aktuelle Live-Kanon (`Kirche der Viere`, geprüft am 2026-04-03) führt **Astrael unverändert als einen der Viere**:
  - Herr des Wissens, der Magie und des Rechtes.
  - Bruder von Bellum, Morsan und Vitama.
  - Kein Hinweis auf Nachfolge, Aufrücken, Verschmelzung oder Ersetzung anderer Gottheiten.
- Der lokale Quellenbestand spiegelt dieselbe Ordnung:
  - `docs/Quellen/Hintergrund/Kirche der Viere | Siebenwind | Ultima Online Freeshard | Siebenwind.md`
  - `docs/Siebenwind_Wiki/01_Pantheon/Das_Pantheon.md`
  - `docs/Siebenwind_Wiki/01_Pantheon/Astrael.md`
- Das Forumsthema `t=109318` (`Astrael rückt auf`) ist im Repo nur noch indirekt über das Research-Ticket belegt. Ein kanonischer Beleg dafuer, dass diese Idee in den offiziellen Hintergrund uebernommen wurde, liegt hier **nicht** vor.

### Bewertung
Die Hypothese einer kanonischen Goetterverschmelzung zugunsten Astraels ist nach gegenwaertigem Befund **nicht bestaetigt**. Der belastbare Live-Kanon vom 2026-04-03 zeigt das klassische Viererpantheon ohne Umbau.

### Wiki-Folge
- `[[Das_Pantheon]]` ist derzeit **konsistent** mit dem Live-Kanon.
- Falls das Forumsthema spaeter rekonstruiert wird, sollte es hoechstens als:
  - OOC-Diskussion,
  - verworfener Vorschlag,
  - oder zeitgebundenes Geruecht
  dokumentiert werden, **nicht** als `#canon`, solange keine hoeherrangige Quelle vorliegt.

## RESEARCH-2026-011: Waldelfen-Exodus & Myten-Verbleib

### Befund
- Die offizielle News vom **2015-02-01** sagt explizit:
  - `Die Waldelfen und Myten haben Siebenwind verlassen.`
  - Quelle: `docs/Quellen/News/2015-02-01_Was_bisher_geschah_Stand_1_Februar_2015.md`
- Eine spaetere offizielle Staff-Agenda vom **2018-10-21** spricht von:
  - `den inaktiven Rassen der Waldelfen oder Myten`
  - Das deutet auf **Spiel-/Freischaltungsstatus**, nicht auf vollstaendige Loeschung aus dem Weltkanon.
- Der aktuelle Live-Kanon am **2026-04-03** fuehrt beide weiterhin als Hintergrundrealitaet:
  - `Waldelfen` haben eine volle Rassenbeschreibung mit Kultur, Herkunft und Klassenuebersicht.
  - `Myten` haben eine eigene Seite; dort steht explizit `DIESE KLASSE IST DERZEIT NICHT SPIELBAR`, waehrend die Rassenbeschreibung ihr Volk weiterhin auf Tare verortet.
- Der Repo-Quellenbestand stuetzt diese Lesart:
  - `docs/Quellen/Hintergrund/Waldelfen | Siebenwind | Ultima Online Freeshard | Siebenwind.md`
  - `docs/Quellen/Hintergrund/Myten | Siebenwind | Ultima Online Freeshard | Siebenwind.md`
- Der aktuelle Wiki-Bestand ist dagegen ungleichmaessig:
  - `docs/Siebenwind_Wiki/00_Fundament/Waldelfen.md` ist noch `UNGEKLAERT`.
  - `docs/Siebenwind_Wiki/03_Gesellschaft/Myten.md` beschreibt die Myten weiterhin als Volk auf Tare.

### Bewertung
Der "Exodus" ist nach heutigem Gesamtbefund **nicht** als totale Ausloeschung oder endgueltiges Verschwinden der Waldelfen und Myten aus dem Kanon zu lesen. Wahrscheinlicher ist folgende Einordnung:

1. 2015 gab es eine offizielle Abreise-/Plot- oder Projektstatus-Meldung.
2. Spaetestens 2018 wurden beide als **inaktive Rassen** behandelt.
3. Der aktuelle Live-Hintergrund fuehrt beide weiterhin als reale Voelker der Welt.

Das spricht fuer **Diaspora / Rueckzug / Nicht-Spielbarkeit**, nicht fuer **kanonische Nichtexistenz**.

### Wiki-Folge
- `[[Waldelfen]]` und `[[Myten]]` sollten **nicht** als ausgeloscht oder vollstaendig "heimgekehrt" dargestellt werden.
- Sinnvoll waere eine spaetere Textpflege mit sauberer Trennung zwischen:
  - historischem Ereignis / Abreise 2015,
  - Spaeterstatus als inaktive Spieler-Rassen,
  - fortbestehender Lore-Existenz im Live-Hintergrund.

## Historiker-Gutachten
*Der Streitfall ist asymmetrisch. Astraels "Aufstieg" bleibt ohne tragfaehigen Beleg im Bereich des Legacy-Geraeusches und darf den Kanon nicht verschieben. Der Waldelfen-/Myten-Komplex ist anders gelagert: Hier existiert eine alte offizielle Abreisemeldung, doch die spaeteren und aktuellen Homepage-Schriften fuehren beide Voelker weiter. Daraus folgt kein Weltloeschungs-Kanon, sondern ein Statuswechsel zwischen Plot, Spielbarkeit und fortbestehender Hintergrundrealitaet.*

## Konkretes Ergebnis fuer MSG-2026-0005
- Astrael:
  - Live-Kanon bestaetigt das klassische Pantheon.
  - Keine Korrektur an `[[Das_Pantheon]]` noetig.
- Waldelfen / Myten:
  - Exodus-Meldung von 2015 ist real, aber nicht als endgueltige Ausloeschung belastbar.
  - Bei kuenftigen Wiki-Edits historische Abreise von fortbestehendem Lore-Status trennen.

## Offene Folgearbeit
- `docs/Siebenwind_Wiki/00_Fundament/Waldelfen.md` inhaltlich ausbauen.
- Bei Bedarf Research-Tickets `RESEARCH-2026-010` und `RESEARCH-2026-011` mit Verweis auf diesen Bericht auf `REVIEW` oder `COMPLETED` umstellen.
- Optional: Eintrag im Konsistenzbericht fuer den Unterschied zwischen Plot-/Spielstatus und statischem Hintergrundkanon.
