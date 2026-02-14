# Master Task List: Siebenwind-Wiki-Rekonstruktion

Dieses Dokument dient als agentenübergreifendes Gedächtnis. Es trennt den **aktiven Fokus** von der **Projekthistorie** und definiert klare Standards für die Aufgabenpriorisierung.

## 📊 Status-Übersicht
- **Wiki-Standard:** v2.1 (Epistemik implementiert)
- **Ingestion-Fortschritt:** ~85% (Spielergeschichten Re-Scan läuft)
- **RAG-Status (Orakel):** Aktiv & MPS-optimiert (Hardware-Auto-Tuning aktiv)

---

- [x] **Handover-Vorbereitung**: Statistiken generiert, Changelog gepflegt.
- [x] **System-Repair**: Behebung von register_check Inkonsistenzen (Healthy Register).
- [x] **Konstitution & Sicherheit**: Implementierung der "Constitution of Responsibility".
- [x] **Batch 25**: Integration der Toran Dur Magie-Bibliothek.
- [x] **Audit**: Vollständiger System-Audit Feb 2026.


- [ ] **Massen-Ingestion**: Integration der verbleibenden Quellen (Status `Pending`). Batch 25 (Toran Dur Library) abgeschlossen. Nächster Schritt: Batch 26.
- [ ] **Vernetzung (Weaving)**: Überprüfung der bi-direktionalen Verlinkung.
- [x] **Lore Research Board**: Initialisierung des Boards mit 3 aktiven Ausschreibungen.
- [ ] **Narrative Enrichment**: Ausbau von Stubs zu profunden Artikeln ("Roman-Qualität"). Fokus auf Motivation, Atmosphäre und Zitate.

## 🔬 Aktuelle Lore-Ausschreibungen (Research Board)
*Detaillierte Aufträge siehe [[LORE_RESEARCH_BOARD.md]]*
- [ ] **RESEARCH-2026-001**: Die Neun Domänen des Angamon (🔴)
- [ ] **RESEARCH-2026-002**: Die Transformation des Ödlands (🟡)
- [ ] **RESEARCH-2026-003**: Die Linari-Matrix (🟡)

## 🔵 Priorität 3: Qualität & Politur (Optimierung)
*Verbesserungen an System und Lore, die den Nutzwert steigern.*

- [ ] **Chronik-Konsolidierung**: Abgleich der neuen Erkenntnisse aus den Spielergeschichten mit der offiziellen [[Zeitrechnung_(Der_Sonnenzirkel).md]].
- [ ] **Feature: „Der Kartograph“**: Implementierung eines Skills zur geografischen Datenverwaltung und Reisezeiten-Berechnung.

## ⚪ Backlog / Future (Ideenspeicher)
*Langfristige Ziele ohne aktuelle Zeitplanung.*

- [ ] **Skill: „Der Herold“**: Automatisches News-Broadcasting basierend auf Wiki-Änderungen.
- [ ] **Workflow: `/map_sync`**: Visuelle Verknüpfung von Wiki-Entitäten mit einer externen Karte.
- [ ] **Workflow: `/cleanup`**: Vollautomatisierter Bot zur kontinuierlichen Pfad-Bereinigung.

---

### Phase 16: Magie & Kosmologie (Feb 2026)
- **Batch 25 (Toran Dur Library)**: Vollständige Integration von 13 magietheoretischen und kosmologischen Texten.
- **Dämonologie & Rituale**: Erstellung des `Daimonicon` und der `Rituallehre`.
- **System-Repair**: Healthy Register Status erreicht (0 Duplikate, 0 Orphans).
- **Lore-Board**: Erstellung des `LORE_RESEARCH_BOARD.md` zur Nachverfolgung offener Lore-Fragen.

### Phase 15: Die Verfassung der Verantwortung (Feb 2026)
- **Safe Defaults**: `7w.py` läuft nun standardmäßig im Advisor-Modus (Situationsbewusstsein zuerst).
- **Konstitution**: Erstellung der `WORKFLOW_ARCHITECTURE.md` (Gewaltenteilung: Legislative, Judikative, Exekutive).
- **Eskalations-Matrix**: Einführung von 3 Log-Levels zur Vermeidung bürokratischer Overheads.
- **Ur-Prozess**: Workflow `/antigravity` als Master-Protokoll etabliert.
- **Judicial Logging**: `Logs/JUDICIARY_LOG.md` für Level-3 Entscheidungen implementiert.

### Phase 13: Politische Krisen (Feb 2026)
- **Boten 181-185**: Rekonstruktion des Putsches in Falkensee und der Führungskrise des Löwenordens.
- **Historiker-Audit**: Fall Benedict Rabenfels (Analyse der Korruption).
- **Register-Cleanup**: 25 Orphans saniert, 9 echte Personen-Duplikate gelöscht.

### Phase 12: Epistemik & Struktur (Feb 2026)
- **Epistemisches System**: Implementierung der 4 Säulen der Wahrheit (#canon, #bote, #perspektive, #überlieferung) im Style Guide.
- **Eskalationsmatrix**: Definition klarer Regeln zur Auflösung von Lore-Widersprüchen.
- **Wiki v2.0**: Globaler Sanitizer-Lauf über alle Artikel (YAML/H1-Sync).

### Phase 14: Synapsen-System v2.0 & Register-Consolidation (Feb 2026)
- **Live-Test**: Erfolgreicher Batch-Run (`/batch`) für Bibliothek Astrael (`Aequitas`, `Codex`, `Brevier`).
- **Lore Trust Score**: Implementierung der 0-10 Skala und Integration in `lore_score_manager.py`.
- **Register-Consolidation**: Vollständige Integration von "Das Ende der Zeit der Könige" (18 Personen, 6 Organisationen).
- **Register-Consolidation**: Vollständige Integration von "Das Ende der Zeit der Könige" (18 Personen, 6 Organisationen).
- **Conflict Resolution**: Exemplarische Lösung des Delarie-Timeline-Konflikts via Synapse Board.

### Phase 14b: Recherche & Analyse (Feb 2026)
- **Marnie Ruatha**: Forschungsbericht erstellt. Klärung der Rolle als Hafenvogtin und des Kirchenasyls.
- **Gap-Analyse**: Identifikation fehlender Akte `Tjure_Odal` und Prüfbedarf bei `Arn_Toron`.

### Phase 14b: Spielergeschichten Processing (Feb 2026)
- **Batch 20-22**: Integration von 18 Spielergeschichten (Dark Lore, Social, Narrative Arcs).
- **Lore-Härtung**: Definition von "Horwah", Nekromantie-Ritualen und Dämonenseuchen.
- **Register-Sync**: ~20 neue Profile erstellt und verknüpft.

### Phase 14c: Astrael Integration & System Health (Feb 2026)
- **Batch 23**: Integration von 8 religiösen Texten der Bibliothek Astrael.
- **System-Repair**: Bereinigung von 13 Inkonsistenzen (Gorem-Duplikate, fehlende Profile).
- **Register-Sync**: Konsolidierung von Aspin/Athos und Erstellung von 8 neuen Profilen.

### Infrastruktur & Tools (Jan/Feb 2026)
- **Das Orakel**: Einführung der semantischen Suche (RAG) auf Basis von Jina v3.
- **Automatisierung**: Scripts für Statistiken, Link-Weben und Hardware-Tuning.

---
*Zuletzt aktualisiert: 14.02.2026 durch Oberarchivar (Handover)*
