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
    *   **Method Hint (non-runtime):** Artikeldatei im Editor/Host-Tooling erstellen oder aktualisieren.
    *   **Frontmatter:** Pflicht!
        ```yaml
        ---
        layout: wiki_page
        uuid: [Genaue UUID-v4 via metadata_helper.py]
        title: [Display Title]
        category: [Persönlichkeit | Geschichte | Erzählung | Geografie | Religion | Magie]
        quelle: ../../Quellen/[Unterordner]/[Dateiname].md
        lore_trust: [0-10] # Gemäß Lore Quality Score (LQS) des Ingestion Reports
        letzter_check: [ISO-8601 Zeitstempel]
        report_id: [UUID des zugehörigen Ingestion Reports] # ZWINGEND ERFORDERLICH
        ---
        ```
    *   **Report-ID:** Jeder Artikel MUSS die `report_id` des zugehörigen Ingestion Reports (oder Audit Reports) tragen. Dies stellt die Rechenschaftspflicht ("Chain of Custody") für jede Information sicher.
    *   **Quelle-Regel:** Das `quelle:` Feld MUSS einen **relativen Pfad** zur Urquelle enthalten. Absolute Pfade sind verboten.
    *   **Inhalt:** Markdown mit H1-Überschrift, die exakt dem `title` im Frontmatter entspricht.
    *   **Links:** Nutze `[[WikiLink]]` Syntax für interne Verweise.
3.  **Pflicht-Sektionen:**
    *   `## Verlinkte Themen` — Wiki-interne Querverweise.
    *   `## Referenzen` — Quellenangaben mit **relativen Pfaden** zur Urquelle sowie Verweise auf Archiv-Reports.
    *   **Prüfbericht-Referenz:** Falls eine `report_id` im Frontmatter existiert, MUSS ein Hinweis in den Referenzen stehen:
        ```markdown
        > [!ABSTRACT] Prüfbericht verfügbar: [[2026-02-15_Quelle_Name]] (ID: [UUID])
        ```
    *   **Referenzen-Format:**
        ```markdown
        ## Referenzen
        - Primärquelle: [Siebenwind Bote 123](../../Quellen/Zeitung%207w%20Bote/Siebenwind%20Bote%20123.md)
        - Siehe auch: [Siebenwind_Bote_122](../04_Chronik/Siebenwind_Bote_122.md)
        ```
4.  **Konflikt-Management (Synapsen-System):**
    *   **Proaktive Erkennung:** Falls während der Erstellung ein unlösbarer Widerspruch auftritt (z.B. zwei Quellen widersprechen sich fundamental im Kanon), erstelle ein Ticket manuell anhand `System/Synapse_Board/_TEMPLATE_TICKET.md`.
    *   **Ticket-Zuweisung:** Nutze das `/System/Synapse_Board/_TEMPLATE_TICKET.md` und speichere es als `Conflict_[ID].md`.
5.  **Validierung:** Prüfe, ob die Datei erfolgreich erstellt wurde und alle Pflicht-Sektionen vorhanden sind.

## Ziel
Erstellung eines sauberen, vernetzten, akademisch referenzierten Wikis ohne manuellen Eingriff des Nutzers.
