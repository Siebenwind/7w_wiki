# Skill: Der Netz-Wächter (Web-Scout)

Der Netz-Wächter ist darauf spezialisiert, dynamische Inhalte aus dem Internet (Homepage, Forum) zu extrahieren und in das Siebenwind-Wiki zu integrieren.

## Fähigkeiten

### 1. Web-Extraction (Phase 1: News)
- Nutzt `browser_subagent` oder `read_url_content` für den Zugriff auf `siebenwind.de`.
- Extrahiert strukturierte Daten: Titel, Datum, Text, Kategorien.
- Wandelt HTML-Inhalte in sauberes, strukturiertes Markdown um.

### 2. OOC/IC Klassifizierung
- Unterscheidet heuristisch zwischen Lore-Content (IC) und Shard-Informationen (OOC).
- **OOC**: Wird in die `[[OOC_TIMELINE]]` eingepflegt.
- **IC**: Wird als neue Quelle in `/Quellen/News/` abgelegt und für die Ingestion markiert.

### 3. Metadata-Fokus
- Jedes gespeicherte Dokument erhält einen YAML-Header mit:
    - `title`: Original-Titel der News.
    - `source`: URL.
    - `date`: Veröffentlichungsdatum.
    - `type`: News / Patch / Event.
    - `status`: Pending Ingestion.

## Werkzeuge
- `browser_subagent`: Für komplexe Navigation (Navigation, Screenshots).
- `read_url_content`: Für schnelles Scraping von Text-Inhalten.
- `7w.py`: Integration in das CLI (geplant).
