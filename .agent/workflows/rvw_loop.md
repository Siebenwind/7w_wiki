---
description: Standard workflow for processing raw data into Wiki artifacts (Read-Verify-Write Loop)
---

# [Entity Name]

**Epistemischer Status:** #perspektive

This workflow defines the standard process for the Oberarchivar agent to convert raw source material into valid Siebenwind Wiki entries.

## 1. INGESTION (Lesen & Verstehen)
*   **Step:** Identify a target file or folder (e.g., `Region Galadon.md`).
*   **Action:**
    *   `list_dir` to see available files. **Prioritize .md files.**
    *   `view_file` to read content.
*   **Goal:** 
    - **Narrative Extraction:** Look beyond facts. Extract character motivations, social context, environmental descriptions, and emotional undertones.
    - **Markdown Source:** If the source is already .md, verify its structural quality. If it's legacy HTML, perform full extraction.
    - **Entity Targets:** Specifically hunt for **Notable Figures**, **Historic Events**, **Guild/Craft Secrets**, and **Creature Lore**. Aim for "Roman-Qualität" (Novel quality).
    - **Linguistic Extraction (Skill: Linguist):** Identify new vocabulary or language fragments (e.g., `[isd]`, `[dw]`).

## 2. VERIFICATION (Truth Hierarchy & Escalation)
*   **Step:** Validate extracted facts against the tiered source of truth.
*   **Action:**
    1.  **Level 1: Lokal-Kanon (Absolute Wahrheit):** Cross-check with `/Hintergrund/` (#canon). Diese Dokumente sind das unumstößliche Gesetz.
    2.  **Level 2: Lokale Quell-Integrität:** Prüfe die Konsistenz innerhalb der aktuell bearbeiteten Quelle (z.B. `/Bote/` oder `/Bibliothek/`).
    3.  **Level 3: Live Web (Verifikation):** Nutze `search_web` mit `site:siebenwind.de [Entity Name]`, um Fakten zu ergänzen oder bei Unklarheiten im Archiv nachzuschlagen.
    4.  **Level 4: User Escalation:** Wenn Informationen fehlen oder über alle Ebenen hinweg widersprüchlich sind, frage den Nutzer.
*   **Decisions:**
    - **Conflict:** Mark as `[KONFLIKT]` and log in [[Konsistenzbericht_2026]].
    - **Uncertainty:** If a check yields no conclusive result, tag as `[UNGEKLÄRT]`.
    - **Consistency:** If all levels match, the fact is verified.

## 3. PRODUCTION (Wiki-Schmied)
*   **Step:** Create the Wiki Artifact.
*   **Pre-Write Validation (PFLICHT):**
    *   **Profil-Check:** Vor jeder Profilerstellung prüfen, ob `07_Persoenlichkeiten/[Name].md` bereits existiert. Falls ja: bestehende Datei aktualisieren, nicht überschreiben.
    *   **Register-Check:** Vor jedem Append ins Personenregister prüfen, ob der Name bereits eingetragen ist. Falls ja: bestehenden Eintrag aktualisieren statt neuen anlegen.
    *   **Anker-Regel:** Beim Register-Append immer **zwei** Ankerzeilen verwenden und die letzte Zeile in der Ersetzung beibehalten.
*   **Action:**
    *   `write_to_file` in `/Siebenwind_Wiki/[Kategorie]/`.
    *   **Filename:** `[Kategorie]_[Name].md` (e.g., `Rasse_Orken.md`).
    *   **Format:**
        ```markdown
        ---
layout: wiki_page
        title: [Entity Name]
        category: [Category]
        status: [Canon/Legend]
        quelle: ../../Quellen/[Unterordner]/[Dateiname].md
        report_id: [UUID des Audit-Reports, falls zutreffend]
        ---
        # [Title]
        
        **Epistemischer Status:** #[tag]

        ... Narrative description ...

        ## Verlinkte Themen
        *   [[Verwandter_Artikel]]

        ## Referenzen
        - Primärquelle: [Quellenname](../../Quellen/[Unterordner]/[Dateiname].md)
        - Siehe auch: [Verwandter Boten-Artikel](../04_Chronik/Siebenwind_Bote_XXX.md)
        ```
*   **Pflichtfelder:**
    *   `## Verlinkte Themen` — Wiki-interne Querverweise.
    *   `## Referenzen` — Quellenangaben mit **relativen Pfaden**, wie bei akademischen Publikationen.
*   **Quelle-Regel:** Das `quelle:` Frontmatter-Feld MUSS einen **relativen Pfad** zur Urquelle enthalten (z.B. `../../Quellen/Zeitung 7w Bote/Siebenwind Bote 123.md`). Absolute Pfade sind verboten.

## 4. POST-WRITE SYNC (Index & Register)
*   **Step:** After writing, synchronize all indexes.
*   **Action:**
    *   **Boten-Archiv:** Wenn ein neuer Bote verarbeitet wurde, den Eintrag in `Die_Chronik.md` unter "Siebenwind Bote Archiv" ergänzen.
    *   **Personenregister:** Neue Personen ins `Personenregister.md` eintragen (nach Pre-Write-Check).
    *   **Zeitleiste:** Wenn ein zeitlich einordbares Ereignis identifiziert wurde, in `Zeitleiste_(15-30_n.H.).md` eintragen.
    *   **Boten-Referenzen:** Am Ende des verarbeiteten Boten-Artikels (in `04_Chronik/`) eine `## Derivate` Sektion ergänzen, die alle aus diesem Boten erstellten Wiki-Artikel auflistet.

## 5. LOGGING & TRUTH-SYNC (Abschluss)
*   **Step:** Finalize task and sync lore state.
*   **Action:**
    *   **Lore Conflict Check:** Did you find contradictions? Update [[Konsistenzbericht_2026]].
    *   **Uncertainty Check:** Is anything marked `[UNGEKLÄRT]`? Document the reason in the report.
    *   Update `task.md` (mark item as `[x]`).
    *   Clear temporary context (focus on next item).


