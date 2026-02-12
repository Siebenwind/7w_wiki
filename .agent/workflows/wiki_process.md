---
description: Der "Zyklus der Weisheit" – Prozess zur Integration neuer Dokumente
---

Dieser Workflow beschreibt den standardisierten Prozess, um neue Quellen (HTML, DOCX, PDF, MD) in das Siebenwind-Wiki zu integrieren.

### Phase 1: Sichtung & Klassifizierung (Screening)
1.  **Inventar prüfen:** Öffne die [INVENTUR_QUELLEN.md](file:///Users/alexandrerabe/siebenwind/7w_wiki/INVENTUR_QUELLEN.md).
2.  **Dateiwahl:** Wähle eine Datei mit dem Status "Pending".
3.  **Wahrheitsgehalt (Epistemik) bestimmen:**
    - `/Quellen/Hintergrund/` -> `#canon`
    - `/Quellen/Zeitung 7w Bote/` -> `#bote`
    - `/Quellen/Bibliothek/` -> `#überlieferung`
    - `/Quellen/Spielergeschichten/` -> `#perspektive`
4.  **Inkonsistenz-Precheck:** Suche nach bestehenden Artikeln zum Thema. Falls die neue Quelle dem vorhandenen Wiki-Stand widerspricht, lege **sofort** einen Eintrag im [Konsistenzbericht 2026](file:///Users/alexandrerabe/siebenwind/7w_wiki/Logs/Konsistenzbericht_2026.md) an.
5.  **Auto-Sync:** Führe den Sync-Automator aus:
    ```bash
    python3 .agent/skills/wiki_schmied/scripts/source_sync_automator.py
    ```

### Phase 2: Extraktion & Reinigung (Extraction)
1.  **Inhalt extrahieren:** 
    - **Markdown-Quelle:** Falls eine `.md`-Datei existiert, ist der Text bereits bereinigt. Prüfe ihn nur auf Konsistenz.
    - **Legacy-Quelle (HTML, DOCX):** Nutze Skills zur Extraktion. Entferne Layout-Reste und Meta-Daten. **Öffne HTML niemals im Browser.**
2.  **Markdown-Konvertierung:** Erzeuge (falls nötig) eine saubere Markdown-Datei.

### Phase 3: Standardisierung (Normalization)
1.  **Style Guide:** Wende den [Wiki Style Guide](file:///Users/alexandrerabe/siebenwind/7w_wiki/.agent/workflows/wiki_style_guide.md) an.
layout: wiki_page
3.  **H1-Check:** Die `# H1` Überschrift muss exakt dem `title` im YAML entsprechen.
4.  **Skript-Einsatz:** Nutze zur Automatisierung:
    ```bash
    python3 .agent/skills/wiki_schmied/scripts/wiki_sanitizer.py [Dateipfad]
    ```

### Phase 4: Validierung & Konsistenz (Validation)
1.  **Kanon-Check:** Abgleich mit `/Hintergrund/` (#canon) und `/Zeitung 7w Bote/` (#bote).
2.  **Linguistik-Check (Skill: Linguist):** 
    - Werden Begriffe korrekt übersetzt? 
    - Sind die Sprach-Flags (`[run]`, `[isd]`, etc.) korrekt gesetzt?
    - Entspricht das Vokabular der [[Linguistik_Übersicht]]?
3.  **Widersprüche loggen [PFLICHT]:** Jeder identifizierte Lore-Konflikt (Web vs. Lokal oder Quelle A vs. Quelle B) muss **vor dem Speichern** des Artikels im Bericht vermerkt werden.
4.  **Wiki-Check:** Entspricht der Entwurf den bestehenden Artikeln?

### Phase 5: Integration & Verwebung (Linking)
1.  **Einsortieren:** Verschiebe die fertige Datei in den passenden Unterordner von `/Siebenwind_Wiki/`.
2.  **Verlinkung:** Führe den Link-Weaver aus, um `[[WikiLinks]]` und Backlinks zu erzeugen:
    ```bash
```
3.  **Register-Refinement:** Bereinige und sortiere die zentralen Register:
    - **Personen:** `python3 .agent/skills/wiki_schmied/scripts/person_registry_refiner.py`
    - **Bestiarium:** Prüfung der Kategorisierung und Verlinkung.
    - **Organisationen:** Konsistenz-Check mit dem Personenregister (Gildenmeister).
    - **Chronik:** Sicherstellung der korrekten Datumslinks.

### Phase 5: Dokumentation (Logging)
1.  **Inventar aktualisieren:** Ändere den Status in `Logs/INVENTUR_QUELLEN.md` von "Pending" auf "Integrated".
2.  **Commit:** Erstelle einen Git-Commit: `Wiki-Processing: [Dateiname] integriert.`
