# Siebenwind Wiki 2.0

**Status:** Aktiv & Gepflegt
**System:** Google Antigravity Agentic Framework
**Ziel:** Konsolidierung von 20 Jahren Rollenspiel-Lore in ein strukturiertes, semantisch durchsuchbares Markdown-Wiki.

## 1. Projekt-Übersicht

Dieses Projekt ist mehr als nur eine Sammlung von Textdateien. Es ist eine **intelligente Wissensdatenbank** für die Welt von Siebenwind. Ein KI-Agent ("Oberarchivar") liest historische Quellen, verifiziert sie und erstellt standardisierte Markdown-Dateien.

Kernkomponenten:
- **Das Orakel** – RAG-System für semantische Suche über die gesamte Lore.
- **Wiki-Statistiken** – Automatisiertes Dashboard zur Erfassung von Wachstum, Qualität und Vernetzung.
- **GitHub Pages** – Automatisierte Veröffentlichung via MkDocs Material.

> [!IMPORTANT]
> **Status Orakel:** Die automatisierte Suche ist derzeit volatil. Bei Timeouts oder Fehlern ist zwingend die **manuelle Suche** (grep, find) als Fallback zu nutzen.

### Verzeichnisstruktur

*   **`/.agent/`**: Das "Gehirn" des Systems.
    *   `/skills/`: Modulare Fähigkeiten (8 Skills, siehe §3).
    *   `/workflows/`: Definierte Arbeitsabläufe (14 Workflows, siehe §4).
    *   `/scripts/`: Automatisierungsskripte (8 Scripts, siehe §5).
    *   `/prompts/`: Persona-Definitionen (Oberarchivar, Archivar, Auskunfts-Archivar, Kickoff).
    *   `/docs/`: Technische Dokumentation und Handover-Dossiers.
*   **`/.github/`**: CI/CD-Pipeline für automatisiertes Deployment.
*   **`/Logs/`**: Das Gedächtnis.
    *   `INVENTUR_QUELLEN.md`: Status aller Quellen (Integrated/Pending).
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

## 3. Skills (Modulare Fähigkeiten)

| Skill | Beschreibung |
|-------|--------------|
| **Das Orakel** | Semantische Vektorsuche (RAG) über das gesamte Wissen. |
| **Kanon-Wächter** | Faktenprüfung gegen die offizielle Homepage. |
| **Linguist** | Analyse & Pflege der falandrischen Sprachen (Erkennung, Interpretation, Datensätze). |
| **Lore-Gelehrter** | Aggregation des gesamten Wiki-Wissens, Inkonsistenzfindung und präzise Auskunft. |
| **Persona-Extractor** | Automatische Extraktion von Persönlichkeits-Profilen aus Quellen. |
| **Scanner** | Ingestion – Verzeichnisse analysieren und relevante Dateien lesen. |
| **Time Keeper** | Utilities für den Siebenwind-Kalender ("Sonnenzirkel": Kalender, Jahreszeiten, Daten). |
| **Wiki-Schmied** | Produktion standardisierter Wiki-Artikel nach v2.0-Standard. |

## 4. Workflows (Arbeitsabläufe)

| Befehl | Funktion |
|--------|----------|
| `/ask` | Beantwortet Lore-Fragen. Nutzt das Orakel. Priorisiert Wiki > Quellen. |
| `/audit` | Prüft Konsistenz, findet Duplikate und verwaiste Einträge. |
| `/batch` | Konsolidierte Massenverarbeitung (Ingestion + RVW + Register-Update). |
| `/contrib_audit` | Review & Sanitize von Community-Beiträgen. |
| `/docs` | Dokumentation, Verwendungsprüfung und Git-Synchronisation. |
| `/handover` | Erstellt ein Übergabeprotokoll für den nächsten Agenten. |
| `/ingestion_protocol` | Standardisierter Prozess zur Erfassung von Boten-Ausgaben. |
| `/rvw_loop` | **Read-Verify-Write**. Der Standard-Zyklus zur Erstellung neuer Artikel. |
| `/stats` | **Neu.** Generiert das Wiki-Statistik-Dashboard (Ingestion, Lore-Dichte, Epistemik). |
| `/takeover` | Onboarding-Prozess für einen neuen Agenten. |
| `/translate` | Falandrische Texte übersetzen & Sprachdatensätze pflegen. |
| `/update` | System-Audit & Update von Skills, Agents und Workflows. |
| `/wiki_process` | Der "Zyklus der Weisheit" – Prozess zur Integration neuer Dokumente. |
| `/wiki_style_guide` | Siebenwind Wiki Style Guide & Konventionen. |

## 5. Scripts (Automatisierung)

| Script | Funktion |
|--------|----------|
| `register_check.py` | Konsistenzprüfung: Duplikate, verwaiste Profile, Boten-Lücken. |
| `generate_wiki_stats.py` | **Neu.** Generiert das Statistik-Dashboard als Markdown mit Mermaid-Charts. |
| `source_integrator.py` | Automatisierte Konvertierung von Quellen nach Markdown. |
| `reference_fixer.py` | Automatische Korrektur von HTML→MD Links. |
| `fix_nested_links.py` | Bereinigung verschachtelter WikiLinks. |
| `standardize_filenames.py` | Dateinamen-Normalisierung. |
| `metadata_helper.py` | Frontmatter-Hilfsfunktionen. |
| `translator.py` | Übersetzungs-Utilities für falandrische Sprachen. |

## 6. Die Wahrheitshierarchie (Truth Hierarchy)

Bei Widersprüchen gilt strikt folgende Priorität:
1.  **Lokal-Kanon (#canon):** Ordner `/Hintergrund`. Das Gesetz.
2.  **Siebenwind_Wiki:** Das verarbeitete, geprüfte Wissen.
3.  **Lokale Quelle (#bote):** Historische Zeitungsartikel (können veraltet sein).
4.  **Live-Web:** Zur Verifikation (Dritte Instanz).

## 7. Deployment (GitHub Pages)

Das Wiki wird automatisch via MkDocs Material auf GitHub Pages veröffentlicht.

**Lokale Vorschau:**
```bash
pip install mkdocs-material
mkdocs serve
```

**Deployment:**
Wird automatisch bei Push auf `main` via `.github/workflows/deploy.yml` ausgelöst.

## 8. Dokumentation

Für Entwickler und Maintainer:
*   [Master Task List](MASTER_TASK_LIST.md): Was noch zu tun ist.
*   [Changelog](CHANGELOG.md): Historie aller Änderungen.
*   [Handover Dossier](.agent/docs/handover_dossier.md): Statusbericht für Nachfolger.
*   [Wiki-Statistiken](Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md): Aktuelles Dashboard.

---
*Zuletzt aktualisiert: 13.02.2026 – Projektleitung: Antigravity*
