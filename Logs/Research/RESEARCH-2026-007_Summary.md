# Forschungsbericht: RESEARCH-2026-007

- Datum: 2026-04-08
- Bearbeitet von: Historian
- Gegenstand: Dossier **Rhadan** / **Zeichnung Tares**

## Fragestellung
Was zeigt die `Zeichnung Tares` aus dem Rhadan-Corpus belastbar, und welche kosmologischen Aussagen lassen sich daraus mit den im Repo vorhandenen Quellen absichern?

## Methode
- Direkte Sichtung der Bildquelle:
  - `Quellen/Bibliothek Toran Dur/Rhadan der Graue - Zeichnung Tares.jpg`
- Direkter Textabgleich gegen:
  - `Quellen/Bibliothek Toran Dur/Rhadan der Graue - AriÔin.md`
  - `Quellen/Bibliothek Toran Dur/Toran Dur - Die Magie.md`
  - `Quellen/Hintergrund/Monde Tares | Siebenwind | Ultima Online Freeshard | Siebenwind.md`
- Abgleich mit den abgeleiteten Wiki-Seiten unter `docs/Siebenwind_Wiki/`.
- `./7w_wiki.py search "Rhadan Zeichnung Tares Ari´in" --source all` wurde versucht, scheiterte in dieser Laufzeit aber erneut daran, dass der Oracle-Reranker (`BAAI/bge-reranker-v2-m3`) lokal nicht gecacht war und wegen deaktiviertem Netz nicht nachgeladen werden konnte. Daher wurde auf direkte Quellenlekture und Bildsichtung umgestellt.

## Befund: Was die Zeichnung sicher zeigt

### Direkt beschriftete Bildelemente
- `Fela`
- `Tare`
- `Vitamalin`
- `Astreyon`
- `Dorayon`

### Sichere Lesart
- **Tare** steht im Zentrum als grosse Weltkugel.
- Im bzw. unter dem Leib `Tares` ist ein **eingerollter Drache** dargestellt.
- **Fela** erscheint als strahlender, feuriger Himmelskoerper.
- **Vitamalin** ist als grosser, strukturierter Trabant links unten eingezeichnet.
- **Astreyon** ist als kleiner, augenartiger Himmelskoerper rechts oben beschriftet.
- **Dorayon** erscheint rechts unten als dunkler, fleckiger bzw. zerfasert wirkender Trabant.

## Kosmologischer Abgleich

### Tare
`Toran Dur - Die Magie` beschreibt die erste Sphaere als vom Drachen **Tare** beherrscht, "auf dessen Ruecken wir uns befinden und der umschlungen in den Tiefen seines Leibes den Yehorn haelt". Die Zeichnung passt dazu: Tare ist nicht nur Bodenwelt, sondern selbst drachisch gedacht.

### Fela und Vitamalin
Dieselbe Quelle nennt **Fela** und **Vitamalin** explizit als Drachen, die planetare Gestalt angenommen haben. Die Zeichnung behandelt beide daher nicht als abstrakte Symbole, sondern als reale Himmelskoerper derselben kosmischen Familie.

### Astreyon
`Monde Tares` beschreibt **Astreyon** ausdrücklich als ein `silbernes Auge`, weil sein Krater den Eindruck einer Pupille erzeugt. Die Zeichnung folgt genau diesem Motiv, indem Astreyon klein, rund und augenhaft gezeichnet wird.

### Dorayon
`Monde Tares` beschreibt **Dorayon** als schmutzigen, schwer sichtbaren, von dunklem Nebel verhuellten Trabanten unter Angamons Herrschaft. Die zeichnerische Darstellung als dunkler, verwaschener Fleck stimmt mit dieser Ueberlieferung ueberein.

## Grenzen der Deutung
- Die Zeichnung ist **kein belastbares Orbitmodell**. Groessenverhaeltnisse, Abstaende und Bahnen wirken schematisch.
- Ein **unbeschrifteter dunkler Kreis** rechts von `Tare` ist sichtbar, kann im aktuellen Quellenlauf aber nicht sicher benannt werden.
- Die daneben gesetzten **Runenzeichen** lassen sich ohne weitere Primaerquelle nicht sauber deuten.
- Aus der Zeichnung allein folgt **nicht**, dass Rhadan ein exklusives Sondermodell der Kosmologie vertrat; sie illustriert vor allem die bereits anderweitig bezeugte Mandon-Lehre.

## Historiker-Gutachten
*Die `Zeichnung Tares` ist im aktuellen Repo-Befund keine freie Phantasiegrafik, sondern eine schematische kosmologische Darstellung der ersten Sphaere. Sie zeigt Tare als drachisch gedachte Weltmitte und ordnet Fela, Vitamalin, Astreyon und Dorayon als benannte Himmelskoerper darum an. Besonders stark abgesichert sind die Deutungen von Astreyon als `Auge` und Dorayon als verdunkeltem Trabanten; unbeschriftete Nebenelemente der Zeichnung bleiben dagegen [UNGEKLAERT].*

## Wiki-Folge
- `[[Zeichnung_Tares]]` sollte als eigene Werk-/Bildseite gefuehrt werden.
- `[[Rhadan_der_Graue]]` sollte neben `[[Die_Ritualisierung_(Rhadan_der_Graue)|Die Ritualisierung]]` und `[[Ariin_(Rhadan_der_Graue)|Ari'in]]` auch die kosmologische Zeichnung als ueberliefertes Werk nennen.
- Die Platzhalterseiten `[[Fela]]`, `[[Vitamalin]]`, `[[Astreyon]]` und `[[Dorayon]]` koennen auf Basis der geprueften Hintergrundquellen zu belastbaren Minimalartikeln gehoben werden.
