---
layout: wiki_page
name: Scanner (Ingestion)
description: Fähigkeit, Verzeichnisstrukturen zu analysieren und relevante Dateien zu lesen.
---

# Scanner (Skill)

**Epistemischer Status:** #perspektive

Dieser Skill dient der Aufnahme von Informationen aus dem lokalen Dateisystem (`/Quellen`).

## Interop-Hinweis
- Dateisichtung und Dateilektuere sind **method hints (non-runtime)**.
- Runtime-Vertrag fuer Recherche bleibt `./7w_wiki.py search ...`.

## Arbeitsweise
1.  **Erkundung (method hint, non-runtime):** Zielordner inventarisieren (z. B. via `rg --files`).
2.  **Filterung:** Priorisiere **.md Dateien**.
3.  **Lektüre (method hint, non-runtime):** Inhalt im Editor/Lesetool lesen.
4.  **Deep Scan - External Boards:**
    - Nutzen des `scout` Kommandos (`7w_wiki.py scout`) zur Extraktion von Metadaten und Trends aus legacy Foren (`Bekanntmachungen`, `News`).
    - Vermeidung von "OOC-Poison" durch Fokus auf strukturelle Marker unter Einhaltung der **Silicon Inquisition** Standards.

## Ziel
Aufbau eines temporären Wissens-Kontexts für die Weiterverarbeitung im RVW-Loop.
