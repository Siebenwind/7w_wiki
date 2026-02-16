---
description: Der "Zyklus der Weisheit" – Prozess zur Integration neuer Dokumente
---

Dieser Workflow beschreibt den standardisierten Prozess, um neue Quellen (HTML, DOCX, PDF, MD) in das Siebenwind-Wiki zu integrieren.

## Interop-Status
- runtime_commands:
  - `7w_wiki.py archive sync`
  - `7w_wiki.py sanitize --auto`
  - `7w_wiki.py score <file>`
  - `7w_wiki.py audit`
- method_only:
  - `/wiki_process`

### Phase 1: Sichtung & Klassifizierung (Screening)
1.  **Inventar prüfen:** Öffne die [INVENTUR_QUELLEN.md](../../Logs/INVENTUR_QUELLEN.md).
2.  **Dateiwahl:** Wähle eine Datei mit dem Status "Pending".
3.  **Wahrheitsgehalt (Epistemik) bestimmen:**
    - `/Quellen/Hintergrund/` -> `#canon`
    - `/Quellen/Zeitung 7w Bote/` -> `#bote`
    - `/Quellen/Bibliothek/` -> `#überlieferung`
    - `/Quellen/Spielergeschichten/` -> `#perspektive`
4.  **Synapse check:** Prüfe das `/System/Synapse_Board/` auf offene Tickets zum Thema.
5.  **Inkonsistenz-Precheck:** Suche nach bestehenden Artikeln zum Thema. Falls die neue Quelle dem vorhandenen Wiki-Stand widerspricht, lege **sofort** ein Ticket auf dem Synapse-Board an.
5.  **Auto-Sync:** Führe den Sync-Automator aus:
    ```bash
    ./7w_wiki.py archive sync
    ```

### Phase 2: Extraktion & Reinigung (Extraction)
1.  **Inhalt extrahieren:** 
    - **Markdown-Quelle:** Falls eine `.md`-Datei existiert, ist der Text bereits bereinigt. Prüfe ihn nur auf Konsistenz.
    - **Legacy-Quelle (HTML, DOCX):** Nutze Skills zur Extraktion. Entferne Layout-Reste und Meta-Daten. **Öffne HTML niemals im Browser.**
2.  **Markdown-Konvertierung:** Erzeuge (falls nötig) eine saubere Markdown-Datei.

### Phase 3: Standardisierung (Normalization)
1.  **Style Guide:** Wende den [Wiki Style Guide](../../.agent/workflows/wiki_style_guide.md) an.
layout: wiki_page
3.  **H1-Check:** Die `# H1` Überschrift muss exakt dem `title` im YAML entsprechen.
4.  **Skript-Einsatz:** Nutze zur Automatisierung:
    ```bash
    ./7w_wiki.py sanitize --auto
    ```

### Phase 4: Validierung, Konsistenz & Scoring (Validation)
1.  **Kanon-Check:** Abgleich mit `/Hintergrund/` (#canon) und `/Zeitung 7w Bote/` (#bote).
2.  **Lore Trust Scoring:** 
    - Berechne den initialen Score (0-10).
    - Nutze `./7w_wiki.py score [Dateipfad]`.
3.  **Linguistik-Check (Skill: Linguist):** 
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
    - **Personen:** `./7w_wiki.py audit` ausführen und Register manuell anhand des Reports nachziehen.
    - **Bestiarium:** Prüfung der Kategorisierung und Verlinkung.
    - **Organisationen:** Konsistenz-Check mit dem Personenregister (Gildenmeister).
    - **Chronik:** Sicherstellung der korrekten Datumslinks.

### Phase 6: Lore-Auditor & Scoring-Boost (Post-Integration)
1.  **Revisions-Check:** Der Historiker prüft den Artikel auf erzählerische Dichte (Novel-Quality).
2.  **Score-Erhöhung:** Falls die Kriterien erfüllt sind, erhöhe den `lore_trust` manuell oder via Skript-Flag.
3.  **Transparenz-Markierung:** Setze den unsichtbaren Audit-Kommentar im Markdown.

### Phase 7: Dokumentation (Logging)
1.  **Inventar aktualisieren:** Ändere den Status in `Logs/INVENTUR_QUELLEN.md` von "Pending" auf "Integrated".
2.  **Commit:** Erstelle einen Git-Commit: `Wiki-Processing: [Dateiname] integriert (Lore-Score: X).`
