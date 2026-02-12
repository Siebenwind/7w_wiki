# Siebenwind Wiki

**Status:** Aktiv
**System:** Google Antigravity Agentic Framework
**Ziel:** Konsolidierung von 20 Jahren Rollenspiel-Lore in ein strukturiertes Markdown-Wiki.

## 1. Projekt-Übersicht

Dieses Projekt dient der Erstellung einer zentralen Wissensdatenbank ("Wiki") für die Welt von Siebenwind. Ein KI-Agent ("Oberarchivar") liest historische Quellen, verifiziert sie gegen den aktuellen Web-Kanon und erstellt standardisierte Markdown-Dateien.

### Verzeichnisstruktur

*   **`/.agent/`**: Die "Gehirn-Konfiguration" des Antigravity-Agenten.
    *   `/skills/`: Definierte Fähigkeiten (Scanner, Web-Check, Wiki-Schreiben).
    *   `/workflows/`: Definierte Prozesse (z.B. der RVW-Loop).
*   **`/Quellen/`**: Das Rohmaterial (Alte Website-Dumps, Zeitungsartikel, Geschichten).
    *   `/_ARCHIV_ORIGINAL/`: Archivierte Originaldateien (HTML, DOCX, etc.) nach der Markdown-Integration.
*   **`/Siebenwind_Wiki/`**: Das Output-Verzeichnis (Das fertige Wiki).
    *   `00_Fundament`: Götter, Magie, Zeit, **Personenregister**, **Glossar**.
    *   `01_Pantheon`: Die Götterwelt.
    *   `02_Geografie`: Länder und Orte.
    *   `03_Gesellschaft`: Gilden, Adel und Rassen.
    *   `04_Chronik`: Zeitgeschichte.
    *   `05_Geschichte`: Wichtige Ereignisse, **Zeitstrahl**.
    *   `06_Erzählungen`: Verarbeitete Spielergeschichten.
    *   `07_Persoenlichkeiten`: Biografien von Personen.
    *   `08_Bestiarium`: Kreaturen und Monster.
    *   `09_Bibliothek`: Bücher und Schriften.
    *   `10_Archiv`: Offizielle Erlasse und Gesetze.
*   **`/.agent/docs/`**: Prozessuale Dokumentation.
    *   `PROZESS_EVALUATION.md`: Analyse und Optimierung der Arbeitsweise.
    *   `WORKFLOW_LORE_CONSISTENCY.md`: Best Practices für Konsistenz (v2.0).

## 2. Nutzung des Agenten

Der Agent arbeitet autonom nach dem **RVW-Standard (Read-Verify-Write)**.

### Initialisierung
Um den Agenten in einer neuen Session zu starten, nutze den Inhalt von `.agent/prompts/Kickoff.md`. Dies lädt alle Skills und Workflows.

### Die Skills
*   **Scanner:** Liest Quellen ein.
*   **Kanon-Wächter:** Prüft Fakten auf `siebenwind.de`.
*   **Wiki-Schmied:** Erstellt formattierte `.md` Dateien.
*   **Hilfsskripte** (in `.agent/scripts/`):
    *   `fix_nested_links.py`: Repariert verschachtelte Wiki-Links.
    *   `standardize_filenames.py`: Passt Dateinamen an die Titel-Konvention an.
    *   `source_integrator.py`: Integriert hochwertige Markdown-Konvertierungen und archiviert die Originale.
    *   `reference_fixer.py`: Korrigiert Dateiendungen in internen Wiki-Links nach der Integration.

### Der Prozess (RVW-Loop) & Wahrheitshierarchie
1.  **READ:** Agent liest eine Quelle (Priorität: `.md` > `.html`).
2.  **VERIFY (Wahrheitshierarchie):**
    *   **Level 1:** Lokal-Kanon (`/Hintergrund`) - Gesetz.
    *   **Level 2:** Lokale Quelle (Bote/Story).
    *   **Level 3:** Live-Web (`siebenwind.de`) - Verifikation.
    *   **Level 4:** Eskalation an den Nutzer.
3.  **WRITE:** Agent schreibt den Wiki-Artikel. Markiert Unsicherheiten mit `[UNGEKLÄRT]`.

## 3. Dokumentation für Maintainer

*   **`.agent/prompts/Archivar.md`**: Die Persona-Definition.
*   **`.agent/docs/Projektdossier_Siebenwind_Chroniken.md`**: Die "Bibel" des Projekts (Axiome, Regeln).
*   **`Logs/INVENTUR_QUELLEN.md`**: Eine halb-automatische Liste aller verfügbaren Quelldateien.

---
*Zuletzt aktualisiert: 12.02.2026*
