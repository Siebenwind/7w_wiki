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
2.  **Filterung:** Priorisiere **.md Dateien** (hochwertige Konvertierungen). Nutze .html, .docx, .pdf nur, wenn keine .md vorhanden ist.
    - *Archiv:* Originale wurden nach `Quellen/_ARCHIV_ORIGINAL/` verschoben.
3.  **Lektüre (method hint, non-runtime):** Inhalt im Editor/Lesetool lesen.
    *   *Markdown:* Liest sich direkt.
    *   *HTML (Legacy):* Lies nur die relevanten Abschnitte (z.B. `<div id="content">`).

## Ziel
Aufbau eines temporären Wissens-Kontexts für die Weiterverarbeitung im RVW-Loop.
