---
layout: wiki_page
name: Scanner (Ingestion)
description: Fähigkeit, Verzeichnisstrukturen zu analysieren und relevante Dateien zu lesen.
---

# Unknown

**Epistemischer Status:** #perspektive

Dieser Skill dient der Aufnahme von Informationen aus dem lokalen Dateisystem (`/Quellen`).

## Arbeitsweise
1.  **Erkundung:** Nutze `list_dir`, um den Inhalt eines Zielordners zu erfassen.
2.  **Filterung:** Priorisiere **.md Dateien** (hochwertige Konvertierungen). Nutze .html, .docx, .pdf nur, wenn keine .md vorhanden ist.
    - *Archiv:* Originale wurden nach `Quellen/_ARCHIV_ORIGINAL/` verschoben.
3.  **Lektüre:** Nutze `view_file`, um den Inhalt zu lesen.
    *   *Markdown:* Liest sich direkt.
    *   *HTML (Legacy):* Lies nur die relevanten Abschnitte (z.B. `<div id="content">`).

## Ziel
Aufbau eines temporären Wissens-Kontexts für die Weiterverarbeitung im RVW-Loop.
