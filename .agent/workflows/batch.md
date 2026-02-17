---
description: Konsolidierter Workflow zur Massenverarbeitung von Quellen (Batch-Processing)
---

# Workflow: /batch [Bereich]

## Interop-Status
- runtime_commands:
  - `7w_wiki.py inquisition --batch <n>`
  - `7w_wiki.py advisor`
  - `7w_wiki.py search <query> --source all`
  - `7w_wiki.py score <file>`
  - `7w_wiki.py mail inbox --status OPEN`
  - `7w_wiki.py mail post --from <agent> --to <agent|ALL> --subject "<text>" --body "<text>"`
  - `7w_wiki.py mail claim <id> --agent <name>`
  - `7w_wiki.py mail done <id> --agent <name> --note "<abschluss>"`
- method_only:
  - `/batch`

Dieser Workflow ist das "Arbeitstier" des Oberarchivars. Er bündelt die Ingestion, Verifikation und Produktion für eine Gruppe von Dokumenten.

## 1. Voraussetzungen
- Der Agent wurde bereits initialisiert (normalerweise durch den [Takeover](../../.agent/workflows/takeover.md) oder Kickoff-Prompt).
- Ein Zielbereich (z.B. "Bote 146-150" oder ein Ordnerpfad) wurde definiert.

## 2. Ablauf (Automatisiert)

### A. Inventur & Screening
1. Scanne den Zielbereich in `/Quellen/`.
2. Identifiziere alle Dateien mit Status `Pending` in der [INVENTUR_QUELLEN.md](../../Logs/INVENTUR_QUELLEN.md).
3. Wende das [Ingestion-Protokoll](../../.agent/workflows/ingestion_protocol.md) an, um alle Entitäten (Personen, Orte, Events) vorab zu erfassen.

### B. RVW-Loop (Massendurchlauf)
Für jede identifizierte Datei wird der [RVW-Loop](../../.agent/workflows/rvw_loop.md) ausgeführt:
1. **Read:** Extraktion des Inhalts (Fokus auf "Roman-Qualität").
    - **PFLICHT:** Entity Manifest erstellen (Schritt 1.5 des RVW-Loops).
    - **PFLICHT:** Manifest gegen bestehende Register abgleichen (✅/❌).
    - **PFLICHT:** Bei Texten > 100 Zeilen das Zwei-Pass-Verfahren anwenden.
2. **Verify:** Abgleich mit dem `#canon` (Lokal-Kanon ist oberstes Gesetz).
3. **Write:** Erstellung/Aktualisierung der Wiki-Files unter Einhaltung des [Style Guides](../../.agent/workflows/wiki_style_guide.md).

### C. Register-Synchronisation
Nach jedem erfolgreichen Schreibvorgang werden die zentralen Register (`Personenregister.md`, `Organisationsregister.md`) aktualisiert.

### D. Scoring & Board-Reporting
1.  **Lore Scoring:** Führe `./7w_wiki.py score <Dateipfad>` über den gesamten Batch-Output aus.
2.  **Board Report:** Erstelle bei signifikanten Konflikten oder Massen-Updates ein automatisches Ticket (Status: `AUTO_RESOLVED` oder `NEEDS_REVIEW`), um die Batch-Integrität zu dokumentieren.
3.  **Ingestion-Tracking:** Jeder Report muss die Tracking-Metadaten aus `System/Templates/INGESTION_REPORT_TEMPLATE.md` enthalten (wer/wann/wie/Dispatch/LQS-Profil).
4.  **Register-Refresh:** Nach Batch-Abschluss `./7w_wiki.py stats` ausführen, damit das Tracking-Register synchron ist.

### E. Dispatch-Heartbeat (Pflicht)
1.  **Start:** Prüfe zu Beginn `./7w_wiki.py mail inbox --status OPEN`.
2.  **Statusmeldungen:** Poste nach jeweils 3-5 verarbeiteten Quellen ein kurzes Update via `mail post` (Stand, Blocker, nächste Schritte).
3.  **Neugier-Prinzip:** Wenn etwas widersprüchlich oder seltsam wirkt, stelle eine konkrete Frage an Spezialisten (z. B. Historian/Guardian/Technician) statt Annahmen zu treffen.
4.  **Abschluss:** Für übernommene Nachrichten immer `claim`/`done` sauber durchziehen.

## 3. Reporting (Ergebnisbericht)
Am Ende des Batches erstellt der Agent eine Zusammenfassung im Chat mit folgendem Schema:

### 📦 Batch-Report: [Bereich Bezeichnung]
- [x] **Quelle 1:** Integriert (Entitäten: [[Name1]], [[Name2]])
    - Neue Organisationen: [[Gilde_X]], [[Bund_Y]]
    - Neue Kreaturen: [[Wesen_Z]]
    - Fehlende Artikel: N (→ Backlog)
- [x] **Quelle 2:** Integriert (Inkonsistenz geloggt: [Typ])
- [ ] **Quelle 3:** Übersprungen (Grund: [Grund])

**Gesamtstatus:**
- Erstellte Artikel: X
- Aktualisierte Register: Y
- Synapse-Board: Z neue Tickets erstellt (siehe `/System/Synapse_Board/`)
- Ingestion-Log Einträge: X (siehe [INGESTION_LOG.md](../../Logs/INGESTION_LOG.md))

---
**Nutzung:** `/batch Bote 191-193`
