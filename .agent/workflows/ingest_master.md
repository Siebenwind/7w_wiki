---
description: Universeller Master Workflow für Ingestion (Quellen -> Wiki)
---

# Department: 🏛️ Lore-Archiv (/ingest_master)

Dieser Workflow definiert den einzigen autorisierten Prozess, um rohes Wissen (HTML, DOCX, PDF, MD) aus dem `/Quellen/`-Verzeichnis in strukturierte Wiki-Artikel (`/Siebenwind_Wiki/`) zu überführen.

Er kombiniert Lese-, Verifikations- und Schreibprozesse (Read-Verify-Write) und garantiert, dass keine Entitäten übersehen werden.

## Interop-Status
- runtime_commands:
  - `7w_wiki.py advisor`
  - `7w_wiki.py search <query> --source wiki|quellen|all`
  - `7w_wiki.py repair --check-collision "<Name>"`
  - `7w_wiki.py ingest <file> [--move-to <dir>]`
  - `7w_wiki.py mail inbox --status OPEN`
  - `7w_wiki.py mail post --from Ingestor --to <agent|ALL> --subject "<text>" --body "<text>"`
  - `7w_wiki.py archive sync`
  - `7w_wiki.py stats`
- method_only:
  - `/ingest_master`

## 1. Sichtung & Klassifizierung (Screening)
// turbo
1. Öffne die [INVENTUR_QUELLEN.md](../../Logs/INVENTUR_QUELLEN.md) und wähle eine Datei mit Status "Pending".
2. Bestimme die Epistemik (Wahrheitsgehalt):
   - `/Quellen/Hintergrund/` -> `#canon` (🥇 Absolut)
   - `/Quellen/Zeitung 7w Bote/` -> `#bote` (🥈 Hoch)
   - `/Quellen/Bibliothek/` -> `#überlieferung` (🥉 Mittel)
   - `/Quellen/Spielergeschichten/` -> `#perspektive` (Gering)
3. Prüfe das `/System/Synapse_Board/` auf offene Tickets zum Thema.
4. **Pre-Flight Check (Kollisionsprüfung):**
   Führe `./7w_wiki.py repair --check-collision "Geplanter_Name"` aus, um Duplikate zu vermeiden.

## 2. Ingestion: Der "Read-Verify-Write" Loop

### A. Lesen & Verstehen
Lies den Quelltext. Achte auf Charakter-Motivationen, soziales Gefüge und Atmosphäre (Roman-Qualität).

> **Lange Texte (> 100 Zeilen): Zwei-Pass-Verfahren (PFLICHT)**
> 1. Pass (Struktur-Scan): Text überfliegen, Kapitel und Perspektivenwechsel identifizieren und zusammenfassen.
> 2. Pass (Detail-Scan): Jede Sektion einzeln lesen und das **Entity Manifest** befüllen. Achte besonders auf beiläufig erwähnte Entitäten.

### B. Das Entity Manifest (Pflicht-Scan)
Erstelle für den Chat ein Checklisten-Manifest (*Personen, Organisationen, Kreaturen, Orte, Ereignisse, Zeitpunkte*). 
Gleiche JEDE gefundene Entität sofort gegen die aktuellen Wiki-Register ab (z.B. mittels `rg -n "<Entity>" Quellen Siebenwind_Wiki` oder dem Orakel).
Nutze das **Orakel (`./7w_wiki.py search`)** bei Unklarheiten. 

### C. Verifikation (Eskalationsmatrix)
1. **Lokal-Kanon (`#canon`)**: Ist Gesetz.
2. **Quell-Integrität**: Plausibilität innerhalb der Quelle.
3. **Web-Verifikation**: Falls nötig, manuelle Suche auf *siebenwind.de*.
4. **Fragepflicht**: Bei Widersprüchen IMMER zuerst eine Fachfrage via Dispatch (`mail post`) an den Guardian oder Historiker senden. Niemals blind überschreiben!

## 3. Die Produktion (Wiki-Schmied)

Nutze NICHT Einzelschritte, sondern IMMER die Ingest-Pipeline:
```bash
./7w_wiki.py ingest "Quellen/Zielordner/Datei.md" --move-to "Siebenwind_Wiki/Zielordner"
```
Diese Pipeline erledigt vollautomatisch:
1. **Linting & Styling:** Wendet den Wiki Style Guide an.
2. **Lore Scoring:** Berechnet den anfänglichen `lore_trust` Score (z.B. 1-10).
3. **Archive Sync:** Repariert die Index-Symlinks.
4. **Global Audit:** Prüft das Wiki auf Register-Konsistenz.

## 4. Abschluss & Register-Synchronisation
Nach dem `--ingest`:
1. **Register manuell nachziehen**: Aktualisiere `Personenregister.md`, `Organisationsregister.md`, etc. basierend auf den Entitäten, die du im Text gefunden hast.
2. **Logging [PFLICHT]**: Erstelle in `Logs/Ingestion/` einen Tracking-Report.
   - Trage Metadaten ein: `Auswertungs-ID`, `Ausgewertet von`, `Auswertungszeitpunkt`.
3. **Stats Rebuild**: Führe `./7w_wiki.py stats` aus, um das Dashboard zu aktualisieren.
4. **Inventar Update**: Ändere den Quellstatus in `Logs/INVENTUR_QUELLEN.md` auf "Integrated".
5. **Git Commit**: Committe die Arbeit präzise (`Wiki-Processing: [Dateiname] integriert`).

#ingestion #produktion #master
