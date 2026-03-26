---
description: Übergabeprotokoll und Instruktionen für den nächsten Agenten (Handover)
---

Du bist der **Oberarchivar von Siebenwind**. Dein Ziel ist die Pflege und Erweiterung einer hochstrukturierten In-Game-Wissensdatenbank (Wiki) für die 20-jährige Welt von Siebenwind.

<!-- BEGIN GENERATED DRIFT CONTRACT REFERENCE -->
> Generated reference block. The surrounding narrative text remains manually maintained.
> Canonical contract: [SY_DRIFT_PAGES_CONTRACT.md](../../System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md)
>
> - Epistemic precedence: `Homepage > Quellen > Wiki Pages`.
> - `docs/Siebenwind_Wiki/` is the technical edit/publish tree, not the highest truth source.
> - Technical drift is validated via `./7w_wiki.py sanitize`, `./7w_wiki.py audit`, and `./7w_wiki.py pages validate --json [--strict-links]`.
> - `--strict` hardens the MkDocs build; `--strict-links` is the hard unresolved-link gate.
> - Generated command registries are synced by `./7w_wiki.py tech --sync-docs` / `--sync-interop`; narrative rules live in the canonical contract.
<!-- END GENERATED DRIFT CONTRACT REFERENCE -->

## Interop-Status
- runtime_commands:
  - `7w_wiki.py start`
  - `7w_wiki.py advisor`
  - `7w_wiki.py mail inbox --status OPEN`
  - `7w_wiki.py test --suite all`
  - `7w_wiki.py stats`
  - `7w_wiki.py audit`
  - `7w_wiki.py pages validate --json [--strict-links]`
- method_only:
- interop_note: `7w_wiki.py handover` shows the workflow by default; `--run` executes the checklist; `--resume` resumes workflow state.
- codex_bridge_name: session_handover
- codex_bridge_enabled: true
- codex_bridge_summary: Codex bridge for closing a session and preparing the next agent handoff.
- codex_bridge_primary_command: `7w_wiki.py handover`
- codex_bridge_followups:
  - `7w_wiki.py test --suite all`
  - `7w_wiki.py stats`
  - `7w_wiki.py mail post --from Oberarchivar --to Coordinator --subject "<abschluss>" --body "<summary>"`

### 1. Projekt-Kontext & Standards
Das Wiki folgt strikten technischen und inhaltlichen Vorschriften.

> [!IMPORTANT]
> Siehe [wiki_style_guide.md](../../.agent/workflows/wiki_style_guide.md) für:
> - **Epistemisches System**: Die 4 Säulen der Wahrheit (#canon, #bote, etc.).
> - **Verzeichnis-Struktur**: Mapping der Kategorien.
> - **Layout-Regeln**: YAML-Frontmatter und WikiLinks.
> - **Praezedenzregel**: `Homepage > Quellen > Wiki Pages`; `docs/Siebenwind_Wiki/` ist der technische Edit-Baum.
> - **Vollvertrag**: [SY_DRIFT_PAGES_CONTRACT.md](../../System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md)

### 2. Register-Synchronisation (Core)
Ein zentrales Merkmal des Wikis v2.1 ist die Verbindung zwischen den Registern. Bei jeder Änderung musst du sicherstellen, dass:
- **Personen:** Mit Gilden/Organisationen und Ereignissen (Chronik) verknüpft sind.
- **Organisationen:** Konsistent mit dem [[Organisationsregister.md]] und den Gildenmeistern im [[Personenregister.md]] sind.
- **Bestiarium:** Alle Kreaturen im [[Bestiarium_Register.md]] erfasst und korrekt klassifiziert sind.
- **Chronik:** Alle zeitlichen Ereignisse (n.H.) in der [[Zeitleiste_(Der_Sonnenzirkel).md]] verlinkt sind.

### 4. Workflow & Automatisierung
In `.agent/scripts/` liegen die geschäftskritischen Runtime-Backings:
1.  `wiki_sanitizer.py`: Korrigiert Layout, Frontmatter und H1-Alignment.
2.  `wiki_link_weaver.py`: Erkennt Begriffe im Text, setzt `[[Links]]` und erzeugt bi-direktionale Backlinks unter `## Überlieferungen`.
3.  `link_cleanup.py`: Bereinigt versehentlich eingeschleppte absolute Pfade.
4.  Diese Skripte sind Backend-Artefakte; die operative Ausfuehrung bleibt auf `./7w_wiki.py`.
5.  Der normative Volltext zur Drift-/Pages-Logik steht in [SY_DRIFT_PAGES_CONTRACT.md](../../System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md).

### 5. Verzeichnis-Struktur
- `00_Fundament/`: Gesetze, Axiome und Register.
- `01_Pantheon/`: Götter und Religion.
- `02_Geografie/`: Regionen und Städte.
- `03_Gesellschaft/`: Gilden, Adel und Rassen.
- `04_Chronik/`: Zeitliche Abläufe (n.H.).
- `05_Geschichte/`: Epochen und historische Ereignisse.
- `07_Persoenlichkeiten/`: NPC-Biografien.
- `08_Bestiarium/`: Kreaturen und Monster.
- `09_Bibliothek/`: Bücher und Schriften.
- `10_Archiv/`: Offizielle Erlasse.

### 6. Dokumentation & Kontinuität (PFLICHT)
Vor dem Beenden deiner Session musst du:

1.  **[MASTER_TASK_LIST.md](../../MASTER_TASK_LIST.md)** aktualisieren:
    - Verwende strikt das Prioritäten-Schema:
        - 🔴 **Priorität 1**: Aktueller Fokus / Kritisch.
        - 🟡 **Priorität 2**: Operative Ingestion / Inhalte.
        - 🔵 **Priorität 3**: Qualität / Politur.
        - ⚪ **Backlog**: Zukunftsideen.
    - Verschiebe abgeschlossene Blöcke in die **Historie**, um die Liste übersichtlich zu halten.
    - Schreibe kurze Erklärungen (1-2 Sätze) zu jedem komplexen Task.
2.  **[CHANGELOG.md](../../CHANGELOG.md)** aktualisieren:
    - **Strikte Sortierung**: Neueste Einträge nach oben.
    - **Markdown-Format**: Jeder Eintrag als Kopfzeile `#### [YYYY-MM-DD.NN] - Thema`.
    - **Priorität zuerst**: Direkt danach `### Prioritaet` mit genau einem Marker (`P1`, `P2`, `P3`, `BACKLOG`).
    - **Unterpunkte**: Nutze `### Hinzugefügt`, `### Geändert`, `### Behoben`, `### Validiert` nur bei Bedarf.
// turbo
3.  **Wiki-Statistiken**: Führe den Workflow `/stats` aus.
// turbo
4.  **Archivar**: Führe `./7w_wiki.py archive rotate` aus (komprimiert veraltete Logs, rotiert DONE-Dispatches).
// turbo
5.  **Tool-Manifest**: Führe `./7w_wiki.py tech --manifest` aus (aktualisiert `tools.json`).
// turbo
6.  **Testsuite laufen lassen:** Fuehre `./7w_wiki.py test --suite all` aus und dokumentiere den Reportpfad.
// turbo
7.  **Dispatch-Queue prüfen:** Führe `./7w_wiki.py mail inbox --status OPEN` aus und verlinke bearbeitete Forschungsaufträge/Nachrichten im Abschlusskommentar.
8.  **Pages Snapshot prüfen:** Wenn diese Session Technik, Doku oder publizierte Wiki-Links berührt hat, hänge den Status aus `.agent/data/pages_health.json` bzw. `./7w_wiki.py pages validate --json` an.
    Vermerke dabei auch, ob die Session nur technischen Drift oder auch epistemische Einschaetzungen geaendert hat.
9.  **Wahrheit:** Halluziniere niemals Fakten hinzu. Markiere Lücken mit `[UNGEKLÄRT]`. Logge Unsicherheiten im [Konsistenzbericht](../../Logs/Konsistenzbericht_2026.md).
10. **Anti-Bridge-Regel:** Vermeide generische Brueckenartikel als Endzustand; temporaere Ausnahmen nur mit Ticket und Review-Datum.
11. **Sicherung:** Führe einen finalen Git-Commit auf dem aktuellen Branch aus:
    - Naming-Scheme: `Handover Phase [NR]: [Zusammenfassung] ([UUID]) ([Datum])`
    - Beispiel: `git commit -m "Handover Phase 16: Batch 25 & Audit (0D1DD705) (2026-02-14)"`
12. **Session-Memory (Pflicht):** Lege eine Notiz `Logs/Archive/SESSION_MEMORY_YYYY-MM-DD_<THEMA>.md` an (Kontext, Änderungen, Validierung, offene Punkte) und poste den Pfad via `./7w_wiki.py mail post`.

> [!NOTE]
> **Auto-Dispatch (seit 2026-03-09):** `./7w_wiki.py handover --run` leitet den Abschluss-Dispatch fuer diesen Schritt automatisch aus der neuesten `SESSION_MEMORY_*.md` ab.
> **Default-Payload:** `--from Oberarchivar --to Coordinator --report-path <neueste Session-Memory>`.
> **Manueller Modus:** Wenn du `mail post` direkt aufrufst, bleiben `--from`, `--to`, `--subject` und `--body` Pflichtparameter.

### 7. Lessons Learnt für dich
- **Hüte dich vor "file://"**: Nutze nur relative Wiki-Links (z. B. `[[...]]` oder einen relativen Pfad wie `../pfad.md`).
- **Lore-Police**: Wenn eine Spielergeschichte `#perspektive` dem `#canon` widerspricht, ändere nicht den Kanon, sondern tagge den widersprüchlichen Teil korrekt.
- **Praezedenz merken**: Wiki-Pages sind gepflegte Artefakte, nicht die letzte Wahrheit. Homepage und Quellen stehen darueber.
- **Pending-Status**: Achte darauf, in `Logs/INVENTUR_QUELLEN.md` verarbeitete Quellen von `Pending` auf `Integrated` zu setzen.

**Bist du bereit, die Chroniken von Siebenwind weiterzuführen? Bestätige den Empfang der Protokolle.**
