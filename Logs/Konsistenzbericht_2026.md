# Konsistenzbericht 2026 - Batch 120-145

**Status:** ⚠️ Dokumentierte Lücken
**Datum:** 2026-02-12

## Prüfobjekte
- Siebenwind Bote 120 - 145
- Personenregister.md (Einträge 120-145)

## Identifizierte Entitäten & Fakten
- **Zentralschicksale:** Elares Valjean (Bote 122), Woran Lebensmüh (Bote 130).
- **Orte:** Brandenstein (Zentrum), Falkensee (Baustelle), Greifenklipp (Nortraven).
- **Organisationen:** Handelsbund (aufgelöst in 130), Lehensbanner, Baronsgarde.

## Konsistenzprüfung
1. **Personenbenennung:**
    - *Steiner / von Steiner:* In 127 als " Steiner" erwähnt, in 130 als "Haus Steiner". Konsistent als Adelsgeschlecht.
    - *Laurelin:* Konsistent als Beraterin in 124 und 128.
2. **Chronologie:**
    - Alle Berichte liegen im Jahr 15 n.H. (Sekar, Carmar, Oner). Konsistent.
3. **Logikbrüche:**
    - **Handelsbund:** Grüßwort (121) -> Turnier (123) -> Anschlag/Auflösung (130). Konsistent.
    - **Baronsgarde:** Ausnahme Waffenrecht (127) -> Auflösungsfeier (128). Konsistent.

## Ergebnis
Keine kritischen Widersprüche in der Erzählung gefunden, jedoch strukturelle Defizite in der Verlinkung und fehlende fundamentale Artikel.

---
## [STRUKTUR] Verwaiste Boten-Artikel
**Quelle:** [Siebenwind_Wiki/04_Chronik/](file:///Users/alexandrerabe/siebenwind/7w_wiki/Siebenwind_Wiki/04_Chronik/)
**Inhalt:** Alle neu erstellten Bote-Artikel (120-130) sind verwaist, da kein zentrales Archiv-Verzeichnis existiert.
**Status:** ⚠️ Offen
**Aktion:** Erstellung eines Boten-Archivs oder Integration in [[Die_Chronik]].

---
## [GEOGRAFIE] Fehlende Orts-Stubs
**Quelle:** Diverse Boten / [[Personenregister]]
**Inhalt:** Zentrale Orte wie [[Brandenstein]], [[Falkensee]] und [[Greifenklipp]] werden verlinkt, existieren aber nicht in `/02_Geografie/`.
**Status:** ⚠️ Offen
**Aktion:** Erstellung von Basis-Stubs für die Hauptstädte und Siedlungen.

---
## [ENRICHMENT] Detail-Artikel erstellt
**Quelle:** [[Elares_Valjean]], [[Madame_Estrella]], [[Niemand]], [[Aschene_Wüste]]
**Inhalt:** Wie vom Nutzer gefordert, wurden nicht nur Register-Einträge, sondern auch die tatsächlichen Wiki-Artikel mit ihrem Wissen aus den Boten erstellt bzw. aktualisiert.
**Status:** ✅ Fixiert
**Aktion:** Keine.

---
## [LOGIK] Konflikt Endophal - Falkenstein
**Quelle:** [[Siebenwind_Bote_142]]
**Inhalt:** Erwähnung eines Wiederaufbaus in [[Lurath]] nach einem "zwischenzeitlichen Konflikt".
**Status:** ✅ Dokumentiert
**Aktion:** Überwachung zukünftiger Berichte auf Details zu diesem Krieg.

---
## [ENRICHMENT] Detail-Artikel Batch 141-145
**Quelle:** [[Yota]], [[Sae]], [[Endophal]], [[Lurath]], [[Sire_Fedral_Lavid]], [[Harlas]], [[Llewellyen]], [[Ödland]]
**Inhalt:** Umfangreiche Erweiterung der Geografie- und Persönlichkeits-Sektionen basierend auf den Boten-Daten.
**Status:** ✅ Fixiert
**Aktion:** Keine.

---
## [REGISTER] Datenverlust durch fehlerhaftes Append-Muster
**Quelle:** [[Personenregister]]
**Datum:** 2026-02-12 (Session Bote 189-123)
**Inhalt:** Beim Hinzufügen neuer Einträge zum Personenregister wurde ein Ersetzungsmuster verwendet, das die letzte Zeile der vorherigen Charge **ersetzte** statt nach ihr einzufügen. Folgende 6 Einträge gingen verloren:
- `[[Halvard]]` (Bote 188) — ersetzt durch Bote 189
- `[[Orgolosch]]` (Bote 189) — ersetzt durch Bote 190
- `[[Theobald_I]]` (Bote 190) — ersetzt durch Bote 120
- `[[Aelwin]]` (Bote 120) — ersetzt durch Bote 121
- `[[Sylviana_Drachenfeuer]]` (Bote 121) — ersetzt durch Bote 122
- `[[Baron_von_Gerdenwald]]` (Bote 122) — ersetzt durch Bote 123
**Status:** ✅ Fixiert (alle 6 wiederhergestellt)
**Aktion:** Künftig beim Append ans Register immer **zwei** Ankerzeilen verwenden und die letzte Zeile in der Ersetzung beibehalten.

---
## [KOLLISION] Vorexistierende Profile bei Charge 3 (Bote 120-123)
**Quelle:** `07_Persoenlichkeiten/`
**Datum:** 2026-02-12
**Inhalt:** Beim Erstellen neuer Profile für Bote 120-123 stießen folgende Dateien auf bereits existierende Einträge (vermutlich aus einer früheren Bearbeitungs-Session):
- `Paule_Bitterling.md`, `Vincent_Ebenstein.md`, `Altumion_Eisenbruch.md`, `Harwarn.md`, `Arman.md`
- `Elares_Valjean.md` — überschrieben (standardisiert)
**Status:** ⚠️ Dokumentiert
**Aktion:** Vor Profilerstellung künftig prüfen, ob Datei existiert.

---
## [PROZESS] Fehlende Protokollierung Bote 189-190
**Quelle:** Session 2026-02-12 (Charge 2 Abschluss)
**Inhalt:** Bote 189 und 190 wurden ohne begleitende Einträge im Konsistenzbericht verarbeitet.
- **Bote 189:** Ödland-Expedition, Kesselklamm-Ritual, Ayk Areson neuer Jarl, Großes Konzil gescheitert
- **Bote 190:** König Hilgorad lebt, Angriff auf Brandenstein, Zerstörung Westhever, Fürst Raziel zurück
**Status:** ✅ Nachträglich dokumentiert
**Aktion:** Keine.
