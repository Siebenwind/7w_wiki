---
name: Wiki-Schmied (Production)
description: Fähigkeit, standardisierte Wiki-Artikel zu erstellen.
---

# [Display Title]

**Epistemischer Status:** #perspektive

Dieser Skill generiert die finalen Artefakte im Ordner `/Siebenwind_Wiki`.

## Arbeitsweise
1.  **Strukturierung:**
    *   Wähle den passenden Unterordner (`00_Fundament`, `01_Pantheon`, `02_Geografie`, `03_Gesellschaft`, `04_Chronik`).
    *   Bestimme den Dateinamen: `Kategorie_Name.md` (oder `Name.md` in eindeutigen Ordnern).
2.  **Formatierung:**
    *   Nutze `write_to_file`.
    *   **Frontmatter:** Pflicht!
        ```yaml
        ---
layout: wiki_page
        title: [Display Title]
        category: [Persönlichkeit | Geschichte | Erzählung | Geografie | Religion | Magie]
        quelle: [Pfad zur MD-Quelldatei in /Quellen]
        ---
        ```
    *   **Inhalt:** Markdown mit H1-Überschrift, die exakt dem `title` im Frontmatter entspricht.
    *   **Links:** Nutze `[[WikiLink]]` Syntax für Verweise.
3.  **Validierung:** Prüfe, ob die Datei erfolgreich erstellt wurde.

## Ziel
Erstellung eines sauberen, vernetzten Wikis ohne manuellen Eingriff des Nutzers.
