# Siebenwind Wiki 2.0

**Status:** Aktiv & Gepflegt
**System:** Google Antigravity Agentic Framework
**Ziel:** Konsolidierung von 20 Jahren Rollenspiel-Lore in ein strukturiertes, semantisch durchsuchbares Markdown-Wiki.

## 1. Projekt-Übersicht

Dieses Projekt ist mehr als nur eine Sammlung von Textdateien. Es ist eine **intelligente Wissensdatenbank** für die Welt von Siebenwind. Ein KI-Agent ("Oberarchivar") liest historische Quellen, verifiziert sie gegen den aktuellen Web-Kanon und erstellt standardisierte Markdown-Dateien.

Neu in v2.0 ist **Das Orakel**, ein RAG-System (Retrieval-Augmented Generation), das es ermöglicht, Fragen an die Lore zu stellen ("Wer ist der Gott des Feuers?") und Antworten aus tausenden von Dokumenten zu erhalten. 

> [!IMPORTANT]
> **Status Oasis:** Die automatisierte Suche via Orakel ist derzeit volatil. Bei Timeouts oder Fehlern ist zwingend die **manuelle Suche** (grep, find) als Fallback zu nutzen.

### Verzeichnisstruktur
Das Projekt wurde für maximale Übersichtlichkeit reorganisiert:

*   **`/.agent/`**: Das "Gehirn" des Systems.
    *   `/skills/`: Modulare Fähigkeiten (Oracle, Scanner, Linguist).
    *   `/workflows/`: Definierte Arbeitsabläufe (z.B. `/ask`, `/audit`).
    *   `/prompts/`: Persona-Definitionen (Oberarchivar, Archivar).
    *   `/docs/`: Technische Dokumentation und Handover-Dossiers.
*   **`/Logs/`**: Das Gedächtnis.
    *   `MASTER_TASK_LIST.md`: Der zentrale Fortschrittsbalken.
    *   `CHANGELOG.md`: Historie aller Änderungen.
    *   `Konsistenzbericht_2026.md`: Offene Lore-Konflikte.
*   **`/Quellen/`**: Das Rohmaterial (Alte Website-Dumps, Zeitungsartikel, Geschichten).
*   **`/Siebenwind_Wiki/`**: Das Output-Verzeichnis (Das fertige Produkt).

## 2. Das Orakel (RAG System)

Das Herzstück der Recherche ist die semantische Suche. Sie versteht Zusammenhänge, nicht nur Keywords.

- **Technologie:** `jina-embeddings-v3` (8k Context) + `ChromaDB` + `BGE Re-Ranker`.
- **Hardware:** Optimiert für Apple Silicon (MPS) mit Auto-Tuning.

**Nutzung (CLI):**
```bash
# Einfache Frage (Sucht im Wiki)
.agent/skills/oracle/venv/bin/python3 .agent/skills/oracle/search.py "Was weißt du über die Gilde der Diebe?"

# Tiefenbohrung (Sucht in Roh-Quellen)
.agent/skills/oracle/venv/bin/python3 .agent/skills/oracle/search.py "Auktion Turek" --source quellen
```

**Setup:**
Führe einmalig `bash .agent/skills/oracle/setup.sh` aus, um die Umgebung zu installieren.

## 3. Workflows für Agenten

Der Agent arbeitet nicht chaotisch, sondern folgt strikten Protokollen:

| Befehl | Funktion |
|--------|----------|
| **/ask** | Beantwortet Lore-Fragen. Nutzt das Orakel. Priorisiert Wiki > Quellen. |
| **/audit** | Prüft Konsistenz, findet Duplikate und verwaiste Einträge. |
| **/rvw_loop** | **Read-Verify-Write**. Der Standard-Zyklus zur Erstellung neuer Artikel. |
| **/batch** | Konsolidierte Massenverarbeitung (Ingestion + RVW + Register-Update). |
| **/handover** | Erstellt ein Übergabeprotokoll für den nächsten Agenten. |

## 4. Die Wahrheitshierarchie (Truth Hierarchy)

Bei Widersprüchen gilt strikt folgende Priorität:
1.  **Lokal-Kanon (#canon):** Ordner `/Hintergrund`. Das Gesetz.
2.  **Siebenwind_Wiki:** Das verarbeitete, geprüfte Wissen.
3.  **Lokale Quelle (#bote):** Historische Zeitungsartikel (können veraltet sein).
4.  **Live-Web:** Zur Verifikation (Dritte Instanz).

## 5. Dokumentation

Für Entwickler und Maintainer:
*   [Projektdossier (Oracle)](Logs/PROJEKT_DOSSIER_ORACLE.md): Technische Details zur KI-Suche.
*   [Master Task List](MASTER_TASK_LIST.md): Was noch zu tun ist.
*   [Handover Dossier](.agent/docs/handover_dossier.md): Statusbericht für Nachfolger.

---
*Zuletzt aktualisiert: 13.02.2026 – Projektleitung: Antigravity*
