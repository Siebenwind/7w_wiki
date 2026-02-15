# Master Task List: Siebenwind-Wiki-Rekonstruktion

Dieses Dokument dient als agentenübergreifendes Gedächtnis. Es trennt den **aktiven Fokus** von der **Projekthistorie** und definiert klare Standards für die Aufgabenpriorisierung.

## 📊 Status-Übersicht
- **Wiki-Standard:** v2.4 (Automated Indices & Structural Purity)
- **RAG-Status (Orakel):** Aktiv & Sandbox-Resilienz (v1.1)
- **Letzter Handover:** (15.02.2026) durch Antigravity (Phase 19.4 Abschluss)

---

## 🔴 Priorität 1: Aktueller Fokus (Next Step)
- [ ] **Content Ingestion**: Fortsetzung der Boten-Verarbeitung (Bote 186+).
- [ ] **Technical Maintenance**: Periodischer Check der automatischen Index-Generierung via `./7w_wiki.py index-pages`.

## 🟡 Priorität 2: Operative Ingestion (Inhalte)
- [ ] **Massen-Ingestion**: Integration der verbleibenden Quellen (Status `Pending`).
- [ ] **Lore Research Board**: Abarbeitung der offenen Ausschreibungen (Angamon, Ödland, Linari).
- [ ] **Lore Research Board**: Abarbeitung der offenen Ausschreibungen (Angamon, Ödland, Linari).

## 🔬 Aktuelle Lore-Ausschreibungen (Research Board)
*Detaillierte Aufträge siehe [[LORE_RESEARCH_BOARD.md]]*
- [ ] **RESEARCH-2026-001**: Die Neun Domänen des Angamon (🔴)
- [ ] **RESEARCH-2026-002**: Die Transformation des Ödlands (🟡)
- [ ] **RESEARCH-2026-003**: Die Linari-Matrix (🟡)
- [ ] **RESEARCH-2026-007**: Dossier Rhadan (Zeichnung Tares) (🔴)

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

### Phase 20: Deep Ingestion & Delegation (Feb 2026)
- **Bote 186-194**: Vollständige Ingestion von 9 Boten-Ausgaben.
- **Register-Sync**: Über 40 neue/aktualisierte Entitäten im Personenregister und Organisationsregister.
- **Narrative Infrastructure**: Erstellung von Schlüsselprofilen ([[Solos_Nhergas]], [[Akassvae]], [[Helfric_von_Wallenburg]], etc.).
- **Silicon Inquisition**: Dokumentation der Astralgeflecht-Anomalie (INQ-2026-001).
- **Delegation**: Vorbereitung des Codex-Agents für den "Golden Polish" (Phase 20).

### Phase 19: Leonardo Sanguine & Master Sketchbook (Feb 2026)
- **Design Pivot**: Abkehr vom Obsidian-Style hin zur "Leonardo Sanguine" Ästhetik.
- **Light & Airy**: Implementierung eines minimalistischen, auf Weißraum und 0.5px Linien basierenden Layouts (v2.4).
- **Abstraktion**: Ersetzung spezifischer Lore-Symbole durch universelle architektonische Geometrie (Kreis, Quadrate, Proportionsstudien).
- **Archivierung**: Lückenlose Sicherung aller Design-Iterationen (Obsidian, Astrael, Sanguine) in `docs/assets/archive/`.
- **Structural Purity**: Sanierung der Markdown-Inkompatibilitäten in allen Register-Tabellen.

### Phase 1: Netz-Wächter & Brand Identity (Feb 2026)
- **Netz-Wächter**: OOC-Timeline (`04_Chronik`) etabliert; Pilot-Ingestion (`siebenwind.de`) erfolgreich.
- **Brand Identity**: Premium-Banner ("Anatomia Magica Mundi"), Logo und Favicon im Renaissance-Stil implementiert.
- **GitHub Deployment**: Wiki live unter `Siebenwind.github.io`. Repository-Transfer an Organisation `Siebenwind`.
- **Documentation Overhaul**: Erstellung von `architecture.md`, `setup_rag.md` und Community-Standards.
- **System-Härtung**: Art Director Skill installiert; CLI zum `7w_wiki.py` Standard vereinheitlicht.

### Phase 18: Toran Dur Advanced Doctrines & Register Polish (Feb 2026)
- **Batch 27 (Toran Dur Advanced)**: Integration of Sub-Batches 1-4.
- **Arcane Science**: Integration of `Arkan-Metalle.md`, `Elementare_Atomlehre.md`, and `Metamorphose_und_Gestaltwandel.md`.
- **Combat & Counter-Magic**: Detailed articles on `Antimagie_und_Gegenzauber.md` and `Arkane_Kriegfuehrung.md`.
- **Gemstone Magic**: Comprehensive integration of `Vjera_Batama_Magica.md`.
- **Register Maintenance**: Manual deduplication and refinement of magister profiles in `Personenregister.md` (Arenus, Tanthul, Nefustor, etc.).

### Phase 17: Advanced Intelligence Infrastructure & Lore Reconstruction (Feb 2026)
- **Orakel-Resilience**: Behebung von Permission-Issues durch Cache-Redirection und Optimierung der Boot-Sequenz.
- **Historiker-Workflow**: Einführung des `/historian` Workflows zur Rekonstruktion komplexer Kausalitäten.
- **Lore Reconstruction**: Klärung der "Hauptstadt-Frage". Rohehafen als erste Kolonie (1 n.H.) etabliert; Tiefenbach als Magiezentrum korrigiert. 
- **Consistency Blitz**: Vollständige Bereinigung des Personenregisters (Deduplizierung & Erstellung von 25 Stubs). Wiki-Status: 100% konsistent.
- **Chronicler Duties**: Automatisierte Statistik-Generierung und Dokumentations-Audit.
- **Onboarding Workflow**: Einführung von `/start` (`./7w_wiki.py start`) als zentraler Einstiegspunkt für neue Agenten.

### Phase 16: Magie & Kosmologie (Feb 2026)
- **Batch 25 (Toran Dur Library)**: Vollständige Integration von 13 magietheoretischen und kosmologischen Texten.
- **Dämonologie & Rituale**: Erstellung des `Daimonicon` und der `Rituallehre`.
- **System-Repair**: Healthy Register Status erreicht (0 Duplikate, 0 Orphans).
- **Batch 25c (Toran Dur Reports)**: Integration von 10 weiteren Texten (Forschungsberichte, Ordenssatzung, Sprache Run).
- **Register-Sync**: Vollständige Erfassung der Gründungsmitglieder des Löwenordens und Toran Durs Biographie.
- **Lore-Board**: Erstellung des `LORE_RESEARCH_BOARD.md` zur Nachverfolgung offener Lore-Fragen.

### Phase 15: Die Verfassung der Verantwortung (Feb 2026)
- **Safe Defaults**: `7w_wiki.py` läuft nun standardmäßig im Advisor-Modus (Situationsbewusstsein zuerst).
- **Konstitution**: Erstellung der `WORKFLOW_ARCHITECTURE.md` (Gewaltenteilung: Legislative, Judikative, Exekutive).
- **Eskalations-Matrix**: Einführung von 3 Log-Levels zur Vermeidung bürokratischer Overheads.
- **Ur-Prozess**: Workflow `/antigravity` als Master-Protokoll etabliert.
- **Judicial Logging**: `Logs/JUDICIARY_LOG.md` für Level-3 Entscheidungen implementiert.

### Phase 13: Politische Krisen (Feb 2026)
- [x] **Agenten-Personas**: Dedizierte Instruktions-Dateien für Ingestor, Wächter, Historiker und Koordinator aktiv.
- [x] **Coordination Hub**: Zentrales Grundbuch (`COORDINATION_HUB.md`) für Dokumenten-Registrierung und Board-Metadaten aktiv.
- [x] **Silicon Inquisition**: AI-internes Parallel-Archiv für kritische Hinterfragung und Lore-Hypothesen initialisiert.
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
*Zuletzt aktualisiert: 14.02.2026 durch Antigravity (Handover Phase 19)*
