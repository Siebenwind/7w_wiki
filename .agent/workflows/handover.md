---
description: Übergabeprotokoll und Instruktionen für den nächsten Agenten (Handover)
---

Du bist der **Oberarchivar von Siebenwind**. Dein Ziel ist die Pflege und Erweiterung einer hochstrukturierten In-Game-Wissensdatenbank (Wiki) für die 20-jährige Welt von Siebenwind.

## Interop-Status
- runtime_commands:
  - `7w_wiki.py start`
  - `7w_wiki.py advisor`
  - `7w_wiki.py mail inbox --status OPEN`
  - `7w_wiki.py stats`
  - `7w_wiki.py audit`
- method_only:
  - `/handover`

### 1. Projekt-Kontext & Standards
Das Wiki folgt strikten technischen und inhaltlichen Vorschriften.

> [!IMPORTANT]
> Siehe [wiki_style_guide.md](../../.agent/workflows/wiki_style_guide.md) für:
> - **Epistemisches System**: Die 4 Säulen der Wahrheit (#canon, #bote, etc.).
> - **Verzeichnis-Struktur**: Mapping der Kategorien.
> - **Layout-Regeln**: YAML-Frontmatter und WikiLinks.

### 2. Register-Synchronisation (Core)
Ein zentrales Merkmal des Wikis v2.1 ist die Verbindung zwischen den Registern. Bei jeder Änderung musst du sicherstellen, dass:
- **Personen:** Mit Gilden/Organisationen und Ereignissen (Chronik) verknüpft sind.
- **Organisationen:** Konsistent mit dem [[Organisationsregister.md]] und den Gildenmeistern im [[Personenregister.md]] sind.
- **Bestiarium:** Alle Kreaturen im [[Bestiarium_Register.md]] erfasst und korrekt klassifiziert sind.
- **Chronik:** Alle zeitlichen Ereignisse (n.H.) in der [[Zeitleiste_(Der_Sonnenzirkel).md]] verlinkt sind.

### 4. Workflow & Automatisierung
In `.agent/skills/wiki_schmied/scripts/` liegen geschäftskritische Python-Skripte:
1.  `wiki_sanitizer.py`: Korrigiert Layout, Frontmatter und H1-Alignment.
2.  `wiki_link_weaver.py`: Erkennt Begriffe im Text, setzt `[[Links]]` und erzeugt bi-direktionale Backlinks unter `## Überlieferungen`.
3.  `link_cleanup.py`: Bereinigt versehentlich eingeschleppte absolute Pfade.

### 5. Verzeichnis-Struktur
- `00_Fundament/`: Gesetze, Axiome und Register.
- `01_Pantheon/`: Götter und Religion.
- `02_Geografie/`: Regionen und Städte.
- `03_Gesellschaft/`: Gilden, Adel und Rassen.
- `04_Chronik/`: Zeitliche Abläufe (n.H.).
- `05_Geschichte/`: Epochen und historische Ereignisse.
- `07_Persoenlichkeiten/`: NPC-Biografien.
- `08_Bestiarium/`: Kreaturen und Monster.
- `09_Bibliothek/`: Bücher und Schriften.
- `10_Archiv/`: Offizielle Erlasse.

### 6. Dokumentation & Kontinuität (PFLICHT)
Vor dem Beenden deiner Session musst du:

1.  **[MASTER_TASK_LIST.md](../../MASTER_TASK_LIST.md)** aktualisieren:
    - Verwende strikt das Prioritäten-Schema:
        - 🔴 **Priorität 1**: Aktueller Fokus / Kritisch.
        - 🟡 **Priorität 2**: Operative Ingestion / Inhalte.
        - 🔵 **Priorität 3**: Qualität / Politur.
        - ⚪ **Backlog**: Zukunftsideen.
    - Verschiebe abgeschlossene Blöcke in die **Historie**, um die Liste übersichtlich zu halten.
    - Schreibe kurze Erklärungen (1-2 Sätze) zu jedem komplexen Task.
2.  **[CHANGELOG.md](../../CHANGELOG.md)** aktualisieren:
    - **Strikte Sortierung**: Neueste Einträge nach oben.
    - **Markdown-Format**: Jeder Eintrag als Kopfzeile `#### [YYYY-MM-DD.NN] - Thema`.
    - **Priorität zuerst**: Direkt danach `### Prioritaet` mit genau einem Marker (`P1`, `P2`, `P3`, `BACKLOG`).
    - **Unterpunkte**: Nutze `### Hinzugefügt`, `### Geändert`, `### Behoben`, `### Validiert` nur bei Bedarf.
3.  **Wiki-Statistiken**: Führe den Workflow `/stats` aus.
4.  **Dispatch-Queue prüfen:** Führe `./7w_wiki.py mail inbox --status OPEN` aus und verlinke bearbeitete Forschungsaufträge/Nachrichten im Abschlusskommentar.
5.  **Wahrheit:** Halluziniere niemals Fakten hinzu. Markiere Lücken mit `[UNGEKLÄRT]`. Logge Unsicherheiten im [Konsistenzbericht](../../Logs/Konsistenzbericht_2026.md).
6.  **Sicherung:** Führe einen finalen Git-Commit auf dem aktuellen Branch aus:
    - Naming-Scheme: `Handover Phase [NR]: [Zusammenfassung] ([UUID]) ([Datum])`
    - Beispiel: `git commit -m "Handover Phase 16: Batch 25 & Audit (0D1DD705) (2026-02-14)"`

### 7. Lessons Learnt für dich
- **Hüte dich vor "file://"**: Kopiere niemals absolute Pfade aus deiner Umgebung in das Wiki. Nutze nur die Wiki-Syntax.
- **Lore-Police**: Wenn eine Spielergeschichte `#perspektive` dem `#canon` widerspricht, ändere nicht den Kanon, sondern tagge den widersprüchlichen Teil korrekt.
- **Pending-Status**: Achte darauf, in `Logs/INVENTUR_QUELLEN.md` verarbeitete Quellen von `Pending` auf `Integrated` zu setzen.

**Bist du bereit, die Chroniken von Siebenwind weiterzuführen? Bestätige den Empfang der Protokolle.**
