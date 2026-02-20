---
description: Standard workflow for processing raw data into Wiki artifacts (Read-Verify-Write Loop)
---

# [Entity Name]

## Interop-Status
- runtime_commands:
  - `7w_wiki.py search <query> --source all`
  - `7w_wiki.py sanitize --auto`
  - `7w_wiki.py score <file>`
  - `7w_wiki.py audit`
- method_only:
  - `/rvw_loop`
- method_hints_non_runtime:
  - Dateiinventur/Lesen via Host-Tooling (`rg --files`, Editor)
  - Web-Sichtung via Host-Tooling
  - Manuelle Ticketerstellung per Synapse-Template

**Epistemischer Status:** #perspektive

This workflow defines the standard process for the Oberarchivar agent to convert raw source material into valid Siebenwind Wiki entries.

## 1. INGESTION (Lesen & Verstehen)
*   **Step:** Identify a target file or folder (e.g., `Region Galadon.md`).
*   **Action:**
    *   **Method Hint (non-runtime):** Dateien inventarisieren, z. B. mit `rg --files`. **Prioritize .md files.**
    *   **Method Hint (non-runtime):** Inhalte im Editor/Lesetool prüfen.
*   **Goal:** 
    - **Narrative Extraction:** Look beyond facts. Extract character motivations, social context, environmental descriptions, and emotional undertones.
    - **Markdown Source:** If the source is already .md, verify its structural quality. If it's legacy HTML, perform full extraction.
    - **Entity Targets:** Specifically hunt for **Notable Figures**, **Historic Events**, **Guild/Craft Secrets**, and **Creature Lore**. Aim for "Roman-Qualität" (Novel quality).
    - **Linguistic Extraction (Skill: Linguist):** Identify new vocabulary or language fragments (e.g., `[isd]`, `[dw]`).

### Lange Texte (> 100 Zeilen) – Zwei-Pass-Verfahren
Bei Texten über 100 Zeilen **MUSS** ein Zwei-Pass-Verfahren angewendet werden:

**Pass 1 – Struktur-Scan:** Den gesamten Text überfliegen und grobe Sektionen identifizieren (Kapitel, Zeitsprünge, Perspektivenwechsel). Jede Sektion kurz zusammenfassen.

**Pass 2 – Detail-Scan:** Jede Sektion einzeln durchgehen und das Entity Manifest (Schritt 1.5) befüllen. Besonders auf **beiläufig erwähnte Entitäten** achten (z.B. "die Gilde der Feinschmiede" in einem Nebensatz, ein Ortsname in einer Wegbeschreibung, ein Titel eines Amtsträgers).

### 🛑 Abbruch bei Überkomplexität
**WICHTIG:** Wenn ein Text inhaltlich oder strukturell zu komplex für einen Standard-Durchlauf wird, **breche die sofortige Ingestion ab und notiere dies!** 
Die Datei muss dokumentiert und dann in einem dedizierten Prozess **einzeln durchgesehen** werden. Niemals komplexe Texte mit Gewalt in das Standard-Schema pressen, um Informationsverlust zu vermeiden.

## 1.5 ENTITY MANIFEST (Pflicht-Scan)### 4. Lore-Auditor (Scoring & Qualität)
- **Score-Zuweisung:** Bewertet jeden neuen Eintrag auf einer Skala von 0 bis 10.
- **Novel Quality Check:** Sucht aktiv nach Möglichkeiten, den `lore_trust` durch präzisere Beschreibungen, sensorische Details und Kausalitäts-Checks zu erhöhen.
- **Audit-Log:** Hinterlässt einen unsichtbaren Audit-Kommentar im Markdown-File: `<!-- Audit: [Datum] | Status: [Boosted to 8] | Grund: [Bote-Kanon-Abgleich erfolgreich] -->`.
*   **Step:** Erstelle nach dem Lesen des Textes ein strukturiertes Manifest.
*   **Action:** Dieses Manifest wird im Chat ausgegeben und dient als Checkliste für Phase 3 (Production) und Phase 4 (Post-Write Sync). Gleiche **jede** gefundene Entität gegen die bestehenden Register ab.

### Scan-Kategorien (ALLE prüfen):

| Kategorie | Scan-Frage | Register-Ziel |
|---|---|---|
| **Personen** | Wer wird namentlich erwähnt? (inkl. Titel, Amt, Spitzname) | `Personenregister.md` |
| **Organisationen** | Welche Gilden, Orden, Bünde, Einheiten, Kulte werden genannt? | `Organisationsregister.md` |
| **Kreaturen** | Welche Wesen/Monster/Tiere werden beschrieben? | `Bestiarium_Register.md` |
| **Orte** | Welche Städte, Gebäude, Landmarken, Regionen werden erwähnt? | Geografie-Artikel |
| **Ereignisse** | Welche historischen Events werden erwähnt? (Kriege, Krönungen, Seuchen) | Chronik / Geschichte |
| **Gegenstände** | Werden besondere Artefakte oder Waffen erwähnt? | Bibliothek / Glossar |
| **Konzepte** | Werden Magie-Systeme, Rituale, Gesetze, Bräuche erklärt? | Fundament |
| **Zeitpunkte** | Welche konkreten Daten (Sonnenzirkel) oder Zeitspannen werden genannt? | `Zeitleiste.md` / `04_Chronik` |

### 🔍 Timeline Focus (Sonnenzirkel-Check):
Prüfe jedes Datum gegen das offizielle System:
1.  **Format:** Entspricht das Datum dem Schema `[Tag]. [Monat] [Jahr] n.H.`? (z.B. `12. Ara 23 n.H.`)
2.  **Kausalität:** Passt das Ereignis logisch in die bestehende Chronik? (z.B. kann niemand vor der Gründung Helighenstadts 0 n.H. in Falandrien regiert haben).
3.  **Widerspruch:** Falls das Datum einer anderen Quelle widerspricht:
    - Kanon (#canon) gewinnt immer.
    - Falls zwei Kanon-Quellen widersprechen -> Ticket (Conflict).

### Output-Format:
```
📋 ENTITY MANIFEST: [Quellenname]
───────────────────────────────────
👤 PERSONEN:
- [Name] | [Rolle/Titel] | [Kontext] | [Existiert im Register: ✅/❌]

🏛️ ORGANISATIONEN:
- [Name] | [Typ] | [Kontext] | [Existiert im Register: ✅/❌]

🐉 KREATUREN:
- [Name] | [Klassifizierung] | [Kontext] | [Existiert im Register: ✅/❌]

📍 ORTE:
- [Name] | [Typ] | [Region] | [Existiert als Artikel: ✅/❌]

⚔️ EREIGNISSE:
- [Event] | [Datum falls bekannt] | [Kontext]

🔮 KONZEPTE/GEGENSTÄNDE:
- [Name] | [Typ] | [Kontext]
```

## 2. VERIFICATION (Eskalationsmatrix)
*   **Step:** Validate extracted facts against the tiered source of truth.
*   **Action:** Prüfe in dieser Reihenfolge. **Stoppe, sobald eine Ebene eine definitive Antwort liefert.**

| Schritt | Prüfebene | Aktion | Bei Treffer |
|---|---|---|---|
| 🥇 | **Lokal-Kanon** (`/Hintergrund/`, `#canon`) | Cross-check mit Kanon-Dateien. Diese Dokumente sind das unumstößliche Gesetz. | → Fakt ist verifiziert |
| 🥈 | **Quell-Integrität** (aktuelle Quelle) | Prüfe die Konsistenz innerhalb der aktuell bearbeiteten Quelle (z.B. `/Bote/` oder `/Bibliothek/`). | → Fakt ist plausibel |
| 🥉 | **Web-Verifikation** (`siebenwind.de`) | **Method Hint (non-runtime):** Nutze Host-Websuche mit `site:siebenwind.de [Entity Name]`. Falls Oracle fehlschlaegt, nutze lokale Suche via `rg -n "<Entity>" Quellen Siebenwind_Wiki`. | → Fakt ergänzt |
| ❓ | **User-Eskalation** (letztes Mittel) | Wenn Informationen fehlen oder über alle Ebenen hinweg widersprüchlich sind, stelle zuerst eine präzise Fachfrage an den zuständigen Spezialisten via Dispatch; nur danach Nutzer-Eskalation. | → Ticket auf `AWAITING_USER` |

> **Verlässlichkeitsregel:** Höherer Rang überschreibt niedrigeren bei Widersprüchen.
> **Synapsen-Trigger:** Wenn die Wahrheitshierarchie keine Loesung bietet (z.B. Kanon vs. Kanon), erstelle manuell ein Ticket anhand `System/Synapse_Board/_TEMPLATE_TICKET.md` auf dem Synapse-Board und sende parallel eine Fachfrage per `mail post`.

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
    *   **Bridge-Verbot by default:** Keine Brueckenartikel/Stub-Texte als Abschlussartefakt erzeugen. Falls eine temporaere Bruecke unvermeidbar ist, nur mit `bridge_mode`, `bridge_target`, `bridge_ticket`, `bridge_review_until`.
*   **Action:**
    *   **Method Hint (non-runtime):** Datei in `/Siebenwind_Wiki/[Kategorie]/` erstellen/aktualisieren.
    *   **Filename:** `[Kategorie]_[Name].md` (e.g., `Rasse_Orken.md`).
    *   **Format:**
        ```markdown
        ---
layout: wiki_page
        title: [Entity Name]
        category: [Category]
        status: [Canon/Legend]
        quelle: ../../Quellen/[Unterordner]/[Dateiname].md
        lore_trust: [0-10] # Initialer Score gemäß Matrix
        confidence: Certain # Grad der Gewissheit
        report_id: [UUID des Audit-Reports, falls zutreffend]
        ---
        # [Title]
        
        **Epistemischer Status:** #[tag]

        ... Narrative description ...

        ## Verlinkte Themen
        *   [[Verwandter_Artikel]]

        ## Referenzen
        - Primärquelle: Quellenpfad `../../Quellen/[Unterordner]/[Dateiname].md`
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
    *   **Ingestion Log [PFLICHT]:** Append einen Eintrag in `Logs/INGESTION_LOG.md` mit:
        - Datum (ISO-8601), Quellenname, Quellentyp und Epistemik.
        - Tabelle aller extrahierten Entitäten mit Aktion (NEU/AKTUALISIERT/VERLINKT) und Zieldatei.
        - Tabelle der Register-Updates.
        - Notizen zu Inkonsistenzen (Verweis auf Konsistenzbericht).
    *   **Tracking [PFLICHT]:** In `Logs/Ingestion/<report>.md` die Metadaten `Auswertungs-ID`, `Ausgewertet von`, `Auswertungszeitpunkt`, `Workflow/Skill`, `Dispatch-Referenz` und `Quality-Profil (A/T/K/B/U)` pflegen.
    *   **Register-Refresh:** Nach Abschluss `./7w_wiki.py stats` ausführen, damit das zentrale Ingestion-Tracking aktualisiert wird.
    *   **Lore Scoring [PFLICHT]:** Führe das Scoring-Skript aus, um den `lore_trust` final zu berechnen:
        ```bash
        ./7w_wiki.py score [Zieldatei]
        ```
    *   **Historian Boost:** Markiere den Artikel für den Historiker zur Prüfung (falls Score < 7), um das Audit-Potential zu nutzen.
    *   Update `task.md` (mark item as `[x]`).
    *   Clear temporary context (focus on next item).
