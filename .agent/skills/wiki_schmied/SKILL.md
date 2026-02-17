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
    *   **Kein Blindwert:** `quelle: UNGEKLAERT` ist fuer neue Seiten kein Standardwert.
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
        - Primärquelle: Quellenpfad `../../Quellen/Zeitung 7w Bote/Siebenwind Bote 123.md`
        - Siehe auch: [[Siebenwind_Bote_122]]
        ```
4.  **Konflikt-Management (Synapsen-System):**
    *   **Proaktive Erkennung:** Falls während der Erstellung ein unlösbarer Widerspruch auftritt (z.B. zwei Quellen widersprechen sich fundamental im Kanon), erstelle ein Ticket manuell anhand `System/Synapse_Board/_TEMPLATE_TICKET.md`.
    *   **Ticket-Zuweisung:** Nutze das `/System/Synapse_Board/_TEMPLATE_TICKET.md` und speichere es als `Conflict_[ID].md`.
    *   **Frage-Format (Pflicht):** Formuliere Widersprüche als konkrete Fachfrage an Spezialisten (Beobachtung -> Vermutung -> Frage) und sende sie via `./7w_wiki.py mail post`.
5.  **Validierung:** Prüfe, ob die Datei erfolgreich erstellt wurde und alle Pflicht-Sektionen vorhanden sind.

## Anti-Bridge Leitplanken (Pflicht)
1. **Rewrite first:** Vor jeder Neuanlage erst kanonische Zielseite suchen und vorhandene Verweise korrigieren.
2. **Keine Placebo-Seiten:** Reine Platzhaltertexte wie „Brueckenartikel zur Stabilisierung bestehender WikiLinks“ sind kein valider Output.
3. **Temporäre Brücke nur als Ausnahme:**
   - `bridge_mode: temporary`
   - `bridge_target: [[Kanonisches_Ziel_oder_TODO]]`
   - `bridge_ticket: MSG-YYYY-NNNN` (oder Task-ID)
   - `bridge_review_until: YYYY-MM-DD`
4. **Verantwortungspfad:** Jede temporäre Brücke braucht ein Dispatch-/Task-Ticket und einen klaren Abbauzeitpunkt.

## Ziel
Erstellung eines sauberen, vernetzten, akademisch referenzierten Wikis ohne manuellen Eingriff des Nutzers.
