---
description: Universelles Ingestion-Protokoll für alle Quellentypen (Boten, Spielergeschichten, Bibliothek, Hintergrund)
---

# Universelles Ingestion-Protokoll

Dieses Protokoll standardisiert die Erfassung **aller** Quellentypen und stellt sicher, dass keine Entitäten übersehen werden.

## Quellentyp bestimmen

| Ordner | Quellentyp | Epistemik |
|---|---|---|
| `/Quellen/Hintergrund/` | Hintergrund | #canon |
| `/Quellen/Zeitung 7w Bote/` | Bote | #bote |
| `/Quellen/Bibliothek/` | Bibliothek | #überlieferung |
| `/Quellen/Spielergeschichten/` | Spielergeschichte | #perspektive |

## Checkliste pro Quelle

### 1. Metadaten-Scan
- [ ] Datum (Sonnenzirkel) erfassen (falls vorhanden)
- [ ] Ausgabe-Nummer / Titel
- [ ] Epistemischer Status bestimmen (siehe Tabelle oben)

### 2. Entitäts-Extraktion (Vollständig)
- [ ] **Hauptakteure**: Alle namentlich genannten Personen mit Titel/Amt/Funktion
- [ ] **Nebenfiguren**: Personen in Nebensätzen, Leserbriefen, Dialogen
- [ ] **Autoren/Erzähler**: Redakteure, Gastautoren, Ich-Erzähler
- [ ] **Erwähnte (nicht anwesende) Personen**: "Man sagte, dass König X..."

### 3. Organisations-Scan
- [ ] Politische Gruppen (Räte, Bünde, Adelsverbände)
- [ ] Gilden & Zünfte (auch lokale wie "Handwerkshaus Falkensee")
- [ ] Militärische Einheiten (Garden, Regimenter, Wachen, Bataillone)
- [ ] Religiöse Gruppen (Orden, Kulte, Tempelgemeinschaften)
- [ ] Informelle Gruppen (Banden, Netzwerke, "die Rebellen")
- [ ] Akademische Institutionen (Akademien, Schulen, Lehrstühle)

### 4. Bestiarium-Scan
- [ ] Namentlich genannte Kreaturen (z.B. "Riesenspinne")
- [ ] Vage Beschreibungen (z.B. "Schattenwesen", "Ungeheuer")
- [ ] Flora & Fauna (z.B. "Moorläuferin") → Abgleich mit Bestiarium-Register
- [ ] Haustiere & Reittiere (z.B. "Krümel die Katze")

### 5. Geografie & Orte
- [ ] Genannte Orte (Städte, Gebäude, Landmarken)
- [ ] Neue Orte (z.B. "Tanzender Drache (Taverne, neu)") erfassen
- [ ] Geographische Relationen (z.B. "Ravel grenzt an Khalandra")
- [ ] Festungen, Türme, Brücken, Pässe (militärische Infrastruktur)

### 6. Flavor-Scan (Atmosphäre & Lore)
- [ ] **Gerüchteküche**: Jedes Gerücht als Listenpunkt erfassen
- [ ] **Kleinanzeigen**: Relevante Dienstleister oder kuriose Angebote
- [ ] **Gedichte/Lyrik**: Kurz erwähnen oder Volltext bei Relevanz
- [ ] **Alltags-Lore**: Handwerke, Berufe, Alltagsgegenstände, Bräuche
- [ ] **Redewendungen / Slang**: Sprachliche Besonderheiten

### 7. Spielergeschichte-Spezifika (nur bei Quellentyp: Spielergeschichte)
- [ ] **Erzähler-Perspektive**: Wer erzählt? (Ich-Erzähler = #perspektive)
- [ ] **Soziales Netz**: Welche Beziehungen zwischen Personen werden beschrieben?
- [ ] **Charakter-Entwicklung**: Welche Veränderungen durchlaufen die Figuren?
- [ ] **Fiktive vs. kanonische Elemente**: Was ist Spieler-Erfindung, was Lore?

## Output-Erstellung

1. **Entity Manifest**: Erstelle das Manifest gemäß RVW-Loop Schritt 1.5
2. **Wiki-Einträge**: Erstellung fehlender Dateien in den zuständigen Ordnern
3. **Register-Update**: Nutzung von `multi_replace_file_content` für:
   - `Personenregister.md`
   - `Organisationsregister.md`
   - `Bestiarium_Register.md`
4. **Ingestion Log**: Eintrag in `Logs/INGESTION_LOG.md` (Pflicht)

## Qualitätssicherung
- [ ] Sind alle **roten Links** (fehlende Seiten) gewollt oder ein Versäumnis?
- [ ] Wurden "Tote" (†) markiert?
- [ ] Wurden Ämterwechsel historisch korrekt datiert?
- [ ] Wurde das Entity Manifest vollständig abgearbeitet?
