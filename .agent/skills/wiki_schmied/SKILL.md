---
name: Wiki-Schmied (Production)
description: Fähigkeit, standardisierte Wiki-Artikel zu erstellen.
---

# Wiki-Schmied (Skill)

**Epistemischer Status:** #kanon

Dieser Skill generiert die finalen Artefakte im Ordner `/Siebenwind_Wiki`.

## Arbeitsweise
1.  **Strukturierung:**
    *   Wähle den passenden Unterordner (`00_Fundament`, `01_Pantheon`, `02_Geografie`, `03_Gesellschaft`, `04_Chronik`, `05_Geschichte`, `06_Erzählungen`, `07_Persoenlichkeiten`, `08_Bestiarium`, `09_Bibliothek`, `10_Archiv`).
    *   Bestimme den Dateinamen: `Kategorie_Name.md` (oder `Name.md` in eindeutigen Ordnern).
2.  **Formatierung:**
    *   Nutze `write_to_file`.
    *   **Frontmatter:** Pflicht!
        ```yaml
        ---
        layout: wiki_page
        uuid: [Genaue UUID-v4 via metadata_helper.py]
        title: [Display Title]
        category: [Persönlichkeit | Geschichte | Erzählung | Geografie | Religion | Magie]
        quelle: ../../Quellen/[Unterordner]/[Dateiname].md
        letzter_check: [ISO-8601 Zeitstempel mit Uhrzeit]
        report_id: [UUID des zugehörigen Audit-Reports, falls vorhanden]
        ---
        ```
    *   **Report-ID:** Wenn der Artikel aufgrund eines Audit-Reports (z.B. Lückenschluss) erstellt wurde, trage hier die UUID des Reports ein. Dies dient als "Funddatum".
    *   **Quelle-Regel:** Das `quelle:` Feld MUSS einen **relativen Pfad** zur Urquelle enthalten. Absolute Pfade sind verboten.
    *   **Inhalt:** Markdown mit H1-Überschrift, die exakt dem `title` im Frontmatter entspricht.
    *   **Links:** Nutze `[[WikiLink]]` Syntax für interne Verweise.
3.  **Pflicht-Sektionen:**
    *   `## Verlinkte Themen` — Wiki-interne Querverweise.
    *   `## Referenzen` — Quellenangaben mit **relativen Pfaden** zur Urquelle. Format wie akademische Publikationen:
        ```markdown
        ## Referenzen
        - Primärquelle: [Siebenwind Bote 123](../../Quellen/Zeitung%207w%20Bote/Siebenwind%20Bote%20123.md)
        - Siehe auch: [Siebenwind_Bote_122](../04_Chronik/Siebenwind_Bote_122.md)
        ```
4.  **Validierung:** Prüfe, ob die Datei erfolgreich erstellt wurde und alle Pflicht-Sektionen vorhanden sind.

## Ziel
Erstellung eines sauberen, vernetzten, akademisch referenzierten Wikis ohne manuellen Eingriff des Nutzers.

