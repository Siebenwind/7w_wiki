---
description: Standardisierter Prozess zur vollständigen Erfassung von Boten-Ausgaben
---

# Ingestion-Protokoll: Siebenwind Bote

Dieses Protokoll dient dazu, die Erfassung von Boten-Ausgaben zu standardisieren und sicherzustellen, dass keine Inhalte vergessen werden.

## Checkliste pro Ausgabe

### 1. Metadaten-Scan
- [ ] Datum (Sonnenzirkel) erfassen
- [ ] Ausgabe-Nummer & Titel
- [ ] Epistemischer Status (#bote)

### 2. Entitäts-Extraktion (Vollständig)
- [ ] **Schlagzeilen-Akteure**: Alle in Hauptartikeln genannten Personen
- [ ] **Nebenfiguren**: Personen in Leserbriefen, Kleinanzeigen, "Allerlei"
- [ ] **Autoren**: Redakteure und Gastautoren (z.B. "Ein besorgter Bürger")

### 3. Organisations-Scan
- [ ] Politische Gruppen (Räte, Bünde)
- [ ] Gilden & Zünfte (auch lokale wie "Handwerkshaus Falkensee")
- [ ] Militärische Einheiten (Garden, Regimenter)
- [ ] Religiöse Gruppen (Orden, Kulte)

### 4. Bestiarium-Scan
- [ ] Namentlich genannte Kreaturen (z.B. "Riesenspinne")
- [ ] Vage Beschreibungen (z.B. "Schattenwesen", "Ungeheuer")
- [ ] Flora & Fauna (z.B. "Moorläuferin") -> Abgleich mit Bestiarium-Register

### 5. Flavor-Scan (Atmosphäre & Lore)
- [ ] **Gerüchteküche**: Jedes Gerücht als Listenpunkt erfassen
- [ ] **Kleinanzeigen**: Relevante Dienstleister oder kuriose Angebote
- [ ] **Gedichte/Lyrik**: Kurz erwähnen oder Volltext bei Relevanz

### 6. Geografie & Orte
- [ ] Genannte Orte (Städte, Gebäude, Landmarken)
- [ ] Neue Orte (z.B. "Tanzender Drache (neu)") erfassen

## Output-Erstellung

1. **Wiki-Eintrag (Chronik)**: Erstellung der Datei `Siebenwind_Bote_XXX.md`
2. **Entitäts-Files**: Erstellung fehlender Dateien in `07_Persoenlichkeiten` / `02_Organisationen`
3. **Event-Files**: Erstellung separater Dateien für Großereignisse (Kriege, Seuchen) in `05_Geschichte`
4. **Register-Update**: Nutzung von `multi_replace_file_content` für:
   - `Personenregister.md`
   - `Organisationsregister.md`
   - `Bestiarium_Register.md`

## Qualitätssicherung
- [ ] Sind alle **roten Links** (fehlende Seiten) gewollt oder ein Versäumnis?
- [ ] Wurden "Tote" (†) markiert?
- [ ] Wurden Ämterwechsel (z.B. Statthalter) historisch korrekt datiert?
