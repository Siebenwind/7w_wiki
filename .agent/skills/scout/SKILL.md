# Skill: Der Netz-Wächter (Web-Scout)

Der Netz-Wächter ist darauf spezialisiert, dynamische Inhalte aus dem Internet (Homepage, Forum) zu extrahieren und in das Siebenwind-Wiki zu integrieren.

## Interop-Hinweis
- Runtime-Vertrag bleibt `./7w_wiki.py` (z. B. `./7w_wiki.py advisor`).
- Browser/URL-Werkzeuge sind **method hints (non-runtime)** und von der Host-Umgebung abhängig.

## Fähigkeiten

### 0. Der passive Beobachter (Wissenschaftlicher Kodex)
- **Keine Interaktion**: Der Agent interagiert niemals aktiv mit dem Forum oder der Webseite (kein Posten, kein Kommentieren).
- **Distanzierte Analyse**: Informationen werden "aus der Ferne" gesichtet, analysiert und dokumentiert, ohne das Ökosystem zu beeinflussen.
- **Transparenz**: Alle Kommentare und Einordnungen erfolgen ausschließlich im Wiki-System, nicht extern.

### 1. Web-Extraction (Phase 1: News)
- Nutzt Browser-/URL-Tooling als **method hint (non-runtime)** für den Zugriff auf `siebenwind.de`.
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
- Browser-Tooling (method hint, non-runtime): Für komplexe Navigation (Navigation, Screenshots).
- URL-Textauslese (method hint, non-runtime): Für schnelles Scraping von Text-Inhalten.
- Runtime-Entry bleibt `./7w_wiki.py` (kein Legacy-CLI-Alias).
