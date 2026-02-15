---
description: Universelles Ingestion-Protokoll für alle Quellentypen (Boten, Spielergeschichten, Bibliothek, Hintergrund)
---

# Universelles Ingestion-Protokoll

Dieses Protokoll standardisiert die Erfassung **aller** Quellentypen und stellt sicher, dass keine Entitäten übersehen werden.

## Quellentyp bestimmen

> Siehe [Wiki Style Guide §3.1 (Epistemisches System)](../../.agent/workflows/wiki_style_guide.md) für Entscheidungsregeln bei Widersprüchen.

| Ordner | Quellentyp | Epistemik | Verlässlichkeit |
|---|---|---|---|
| `/Quellen/Hintergrund/` | Hintergrund | #canon | 🥇 Absolut |
| `/Quellen/Zeitung 7w Bote/` | Periodika | #bote | 🥈 Hoch |
| `/Quellen/Bibliothek/` | Bibliothek | #überlieferung | 🥉 Mittel |
| `/Quellen/Spielergeschichten/` | Spielergeschichte | #perspektive | Gering |
| `/Quellen/Forum/` | Forum | #perspektive | Gering |
| `/Quellen/News/` | News | #news | OOC |

## Checkliste pro Quelle

### 1. Metadaten-Scan
- [ ] Datum (Sonnenzirkel) erfassen (falls vorhanden)
- [ ] Ausgabe-Nummer / Titel
- [ ] Epistemischer Status bestimmen (siehe Tabelle oben)
- [ ] **Lore Trust Score**: Vorläufigen Score (0-10) vergeben (siehe [Score Guide](../../System/Synapse_Board/CORE_LORE_SCORE_GUIDE.md))

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

1.  **Ingestion Report [PFLICHT]**:
    *   Erstelle für jede Quelle ein Protokoll basierend auf `System/Templates/INGESTION_REPORT_TEMPLATE.md`.
    *   Speichere den Report unter `Logs/Ingestion/[ISO-DATE]_[QUELLE].md`.
    *   Berechne den **Lore Quality Score (LQS)** gewissenhaft.
2.  **Wiki-Einträge**: Erstellung fehlender Dateien in den zuständigen Ordnern.
    *   **PFLICHT**: Verlinke die `report_id` im Frontmatter jedes neuen/aktualisierten Artikels.
3.  **Archiv-Synchronisation**: Führe `./7w archive sync` aus, um den neuen Report im Wiki-Archiv sichtbar zu machen.
4.  **Register-Update**: Nutzung von `multi_replace_file_content` für:
    - `Personenregister.md`
    - `Organisationsregister.md`
    - `Bestiarium_Register.md`
4.  **Truth-Sync**: Bei gravierenden Widersprüchen (LQS-Konsistenz < 2) zwingende Eskalation via Synapse Board.

## Qualitätssicherung
- [ ] Wurde der **LQS** ehrlich vergeben?
- [ ] Wurden "Tote" (†) markiert?
- [ ] Wurde die `report_id` bi-direktional verknüpft?
- [ ] Wurde das Entity Manifest vollständig abgearbeitet?
