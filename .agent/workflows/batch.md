---
description: Konsolidierter Workflow zur Massenverarbeitung von Quellen (Batch-Processing)
---

# Workflow: /batch [Bereich]

Dieser Workflow ist das "Arbeitstier" des Oberarchivars. Er bündelt die Ingestion, Verifikation und Produktion für eine Gruppe von Dokumenten.

## 1. Voraussetzungen
- Der Agent wurde bereits initialisiert (normalerweise durch den [Takeover](file:///Users/alexandrerabe/siebenwind/7w_wiki/.agent/workflows/takeover.md) oder Kickoff-Prompt).
- Ein Zielbereich (z.B. "Bote 146-150" oder ein Ordnerpfad) wurde definiert.

## 2. Ablauf (Automatisiert)

### A. Inventur & Screening
1. Scanne den Zielbereich in `/Quellen/`.
2. Identifiziere alle Dateien mit Status `Pending` in der [INVENTUR_QUELLEN.md](file:///Users/alexandrerabe/siebenwind/7w_wiki/Logs/INVENTUR_QUELLEN.md).
3. Wende das [Ingestion-Protokoll](file:///Users/alexandrerabe/siebenwind/7w_wiki/.agent/workflows/ingestion_protocol.md) an, um alle Entitäten (Personen, Orte, Events) vorab zu erfassen.

### B. RVW-Loop (Massendurchlauf)
Für jede identifizierte Datei wird der [RVW-Loop](file:///Users/alexandrerabe/siebenwind/7w_wiki/.agent/workflows/rvw_loop.md) ausgeführt:
1. **Read:** Extraktion des Inhalts (Fokus auf "Roman-Qualität").
    - **PFLICHT:** Entity Manifest erstellen (Schritt 1.5 des RVW-Loops).
    - **PFLICHT:** Manifest gegen bestehende Register abgleichen (✅/❌).
    - **PFLICHT:** Bei Texten > 100 Zeilen das Zwei-Pass-Verfahren anwenden.
2. **Verify:** Abgleich mit dem `#canon` (Lokal-Kanon ist oberstes Gesetz).
3. **Write:** Erstellung/Aktualisierung der Wiki-Files unter Einhaltung des [Style Guides](file:///Users/alexandrerabe/siebenwind/7w_wiki/.agent/workflows/wiki_style_guide.md).

### C. Register-Synchronisation
Nach jedem erfolgreichen Schreibvorgang werden die zentralen Register (`Personenregister.md`, `Organisationsregister.md`) aktualisiert.

### D. Scoring & Board-Reporting
1.  **Lore Scoring:** Führe `lore_score_manager.py` über den gesamten Batch-Output aus.
2.  **Board Report:** Erstelle bei signifikanten Konflikten oder Massen-Updates ein automatisches Ticket (Status: `AUTO_RESOLVED` oder `NEEDS_REVIEW`), um die Batch-Integrität zu dokumentieren.

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
- Ingestion-Log Einträge: X (siehe [INGESTION_LOG.md](file:///Users/alexandrerabe/siebenwind/7w_wiki/Logs/INGESTION_LOG.md))

---
**Nutzung:** `/batch Bote 191-193`
