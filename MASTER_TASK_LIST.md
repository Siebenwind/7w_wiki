# Master Task List: Siebenwind-Wiki-Rekonstruktion

Dieses Dokument dient als agentenübergreifendes Gedächtnis. Es trennt den **aktiven Fokus** von der **Projekthistorie** und definiert klare Standards für die Aufgabenpriorisierung.

## 📊 Status-Übersicht
- **Wiki-Standard:** v2.7 (Engine Stabilized / CLI Unified)
- **RAG-Status (Orakel):** Aktiv & Sandbox-Resilienz (v1.1)
- **Last Handover**: 2026-02-17 16:25 (Antigravity -> User)
- **Status**: Phase 1.19 complete; Batch 7 (Shamanism & Run) integrated.

---

## 🔴 Priorität 1: Aktueller Fokus (Next Step)
- [ ] **Content Ingestion**: Fortsetzung der Boten-Verarbeitung (Bote 118, Bote 186+) - *Delegiert an Ingestor*.
- [ ] **System-Task (Directive MSG-2026-0002)**: Finalisierung der Link-Bereinigung.

## 🟡 Priorität 2: Operative Ingestion & Research
- [ ] **Kanon-Abgleich**: Wiederaufnahme der Prüfung zur Götterverschmelzung (RESEARCH-2026-010/011) - [DEFERRED].
- [ ] **Massen-Ingestion**: Integration der verbleibenden Quellen (Status `Pending`).
- [ ] **Lore Research Board**: Abarbeitung der offenen Ausschreibungen (Angamon, Ödland).

## 🔬 Aktuelle Lore-Ausschreibungen (Research Board)
*Detaillierte Aufträge siehe [[LORE_RESEARCH_BOARD.md]]*

| ID | Thema | Priorität | Status |
| :--- | :--- | :--- | :--- |
| [[RESEARCH-2026-001]] | Die Neun Domänen des Angamon | 🔴 | [ ] Offen |
| [[RESEARCH-2026-002]] | Die Transformation des Ödlands | 🟡 | [ ] Offen |
| [[RESEARCH-2026-003]] | Die Linari-Matrix | 🟡 | [ ] Offen |
| [[RESEARCH-2026-007]] | Dossier Rhadan (Zeichnung Tares) | 🔴 | [ ] Offen |

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

## 🗂️ Projekthistorie (neu → alt)

### v2.7 Upgrade-Phasen

<details open>
<summary><b>Phase 1.19: Silicon Inquisition - Shamanic Magic & Run (Feb 2026)</b></summary>

- **Lore**: Integration der Geisterlehre und Totemmagie in `Schamanische_Magie.md`.
- **Cosmology**: Schärfung des Pantheons ([[Die_Gohor]], [[Die_Enhor]]).
- **Linguistics**: Verfeinerung der arkanen Sprache [[Die_Sprache_Run]].
- **Register**: Vollständige Synchronisation von [[Toran_Dur]]-Werken.
- **Verification**: 100% Audit-Compliance und erfolgreiche Core-Testsuite.
</details>

<details>
<summary><b>Phase 1.17: Silicon Inquisition - Forum Research & Automation (Feb 2026)</b></summary>

- **Automation**: Implemented `forum_scanner.py` and unified CLI command `scout`.
- **Integration**: Upgraded `/scout` workflow and `Scanner` skill to support external board scanning.
- **Research**: Extracted 470 legacy topics; identified 45+ lore markers (Magiereform, Exodus, Zwerge-Hintergrund).
- **Governance**: Established `RESEARCH-2026-010` and formal Research Reports for forum-based lore.
</details>

<details open>
<summary><b>Phase 1.18: Linari Ingestion & Magic Theory Hardening (Feb 2026)</b></summary>

- **Magietheorie**: Vollständige Integration der Linari-Matrix (Knoten-Priorität) und philosophischen Ethik in `Magietheorie_Toran_Dur.md`.
- **Daimonologie**: Erweiterung der Dämonen-Theorie um Hörner-Hierarchien und Antipoden-Entsprechungen.
- **Artefaktkunde**: Erstellung des neuen Referenzartikels `Magietheorie_Artefaktkunde.md` (Tunneleffekt & Bindungsrituale).
- **Register**: Synchronisation von Autoren-Profilen ([[Dunvallo_Linari]], [[Santanos_Alexandrius_von_Eichstatt]]).
- **Governance**: Ingestion Reports für Batch 5 & 6 erstellt; System-Sanitize durchgeführt.
</details>

<details>
<summary><b>Phase 1.17: Silicon Inquisition - Forum Research & Automation (Feb 2026)</b></summary>

<details>
<summary><b>Phase 1.16: Interop Upgrade & Jules Readiness (Feb 2026)</b></summary>

- **Agent Sovereignty**: Created `AGENTS.md` as the single source of truth for all autonomous agents (Jules, Codex, Gemini).
- **CLI Shim**: Added `GEMINI.md` for zero-shot CLI compatibility.
- **Skills Mirror**: Established `.agents/skills/` hierarchy to expose internal capabilities (`oracle`, `historian`) to external agents.
- **Bugfix**: Registered `mail` command in `7w_wiki.py` argparse.
</details>

<details open>
<summary><b>Phase 1.15: Silicon Inquisition Batch 4 - Societies & Cultures (Feb 2026)</b></summary>

- **Race Enrichment**: Major races (Elves, Dwarves, Nortraven, Myten) updated with creation myths and religious foundations (Thjarek/Eydis).
- **Sub-Race Architecture**: Created dedicated articles for Hochelfen, Waldelfen, Auenelfen.
- **Social Infrastructure**: Implementation of the Prison System (Gefaengnissystem) and Measurement Units (Masseinheiten).
- **Register Synchronization**: 10+ historical figures added to registers; Armgard Torbenson spelling corrected.
</details>

<details open>
<summary><b>Phase 1.14: Silicon Inquisition Batches 2 & 3 (Feb 2026)</b></summary>

- **Silicon Inquisition**: Batch 2 (Ente, Galahad, Schöpfung) und Batch 3 (Rohehafen, Pantheon, Linari) vollständig nach v2.7 migriert (20 Quellen).
- **Metadata v2.7**: Einführung von UUIDs, `report_id` und ISO-8601 Timestamps für alle verarbeiteten Quellen.
- **Audit-Compliance**: 100% Validierung der Ingestion Reports durch das System.
- **Archive Sync**: Automatische Synchronisation aller Reports in das `docs/Archiv` Verzeichnis.
</details>

<details>
<summary><b>Phase 1.13: Workflow Optimization & CLI Expansion (Feb 2026)</b></summary>

- **Workflow Consolidation**: Redundanzen in 30 Workflow-Dateien eliminiert. Zentrale Referenzierung via `rvw_loop.md` und `wiki_style_guide.md`.
- **CLI Unified**: Alle losen Skripte (`sanitize`, `score`, `check`, `translate`, `watch`) in `7w_wiki.py` integriert.
- **Archive Integration**: Vollständige Synchronisation von Ingestion Reports und Research Board in das Web-Wiki.
</details>

<details>
<summary><b>Phase 1.12: Lore Research & Profile Merger (Feb 2026)</b></summary>

- **Gilden Research**: RESEARCH-2026-009 abgeschlossen. Artikel [[Gilden_und_Handwerk]] erstellt.
- **Dur Identity**: RESEARCH-2026-008 abgeschlossen. Shorthand "Dur" als Toran Dur identifiziert und Profile konsolidiert.
- **System Health**: Audit-Lauf bestätigt 0 Fehler. Wiki-Statistiken aktualisiert.
</details>

<details open>
<summary><b>Phase 1.11: CI/CD Reliability & Success (Feb 2026)</b></summary>

- **Build-Success**: Behebung von Pipeline-Fehlern durch Plugin-Cleanup und Dependency-Fixes.
- **Cache-Control**: Implementierung von CDN-Headers zur sofortigen Sichtbarkeit von Wiki-Updates.
- **Stability**: Entfernung strikter Build-Regeln zur Sicherstellung kontinuierlicher Deploys während der Lore-Migration.
</details>

<details>
<summary><b>Phase 1.10: Link Engine Stabilization (Feb 2026)</b></summary>

- **Ezlinks-Migration**: Erfolgreiche Umstellung auf das `mkdocs-ezlinks-plugin` für globale `[[WikiLinks]]`.
- **Optimization**: Verfeinerung der Engine-Konfiguration für verzeichnisübergreifende Pfadauflösung.
</details>

<details>
<summary><b>Phase 1.9: CI/CD Troubleshooting (Feb 2026)</b></summary>

- **Dependency Fix**: Integration der `requirements.txt` in den GitHub Actions Workflow.
- **Build Monitoring**: Implementierung von Debug-Logging für Konfigurationsdateien im CI-Runner.
</details>

<details>
<summary><b>Phase 1.8: Cleanup & Organization (Feb 2026)</b></summary>

- **Root-Hygiene**: Verschiebung von Meta-Dokumenten nach `System/` (PDFs, Lore-Doktrin).
- **Asset-Management**: Konsolidierung der Design-Quellen nach `System/Design_Assets/`.
- **Archivierung**: Löschen temporärer Logs und Archivierung alter Handover-Berichte.
</details>

<details>
<summary><b>Phase 1.7: Styling & Engine Optimization (Feb 2026)</b></summary>

- **Plugin Migration**: Umstellung auf `mkdocs-ezlinks-plugin` zur Behebung des Wikilink-Problems (Rendering klickbarer Links über alle Ordner).
- **Visual Overhaul**: Implementierung des neuen horizontalen "Modern Scholar" Banners.
- **Aesthetics**: Glassmorphism für Header/Nav, verbesserte Tabellenlesbarkeit und Renaissance-Typografie integriert.
- **CI-Readiness**: `requirements.txt` für automatisierten GitHub Pages Build angelegt.
</details>

<details>
<summary><b>Phase 1.6: Structural Maintenance & Consistency Repair (Feb 2026)</b></summary>

- **Deduplizierung**: Konsolidierung von [[Chernides]] und [[Orgolosch]] im Personenregister.
- **Vervollständigung**: Erstellung von 11 fehlenden Profil-Stubs (u.a. [[Eliam_Schlosser]], [[Geist]]).
- **Orphan-Links**: Korrekte Verknüpfung verwaister Profile ([[Gropp_Zwillinge]], [[Kregor_Arthax_Stahlauge]]).
- **Realignment**: Bereinigung aller absoluten `file://` Pfade im Wiki und den System-Instruktionen (Mission MSG-2026-0002).
</details>

<details>
<summary><b>Phase 1.5: Minimalist Restoration & Structural Purity (Feb 2026)</b></summary>

- **Design Pivot**: Umstellung auf das "Modern Scholar" Aesthetic (Beige/Rötel).
- **Usability**: Fokus auf hohen Kontrast und Lesbarkeit (Dunkelrot auf Beige).
- **Integrität**: Bereinigung der Landing-Page von "Bla Bla" und dramatischem Ton; Fix der Link-Rendering Engine (Native Wikilinks).
- **Struktur**: Codifizierung der Symlink-Architektur in `STYLING.md` zur Vermeidung zukünftiger Duplikats-Missverständnisse.
- **Git Deployment**: Erfolgreiche Live-Verifikation auf GitHub Pages.
</details>

### Legacy-Phasen (v2.0 bis v2.6)

<details>
<summary><b>Phase 20: Deep Ingestion & Delegation (Feb 2026)</b></summary>

- **Bote 186-194**: Vollständige Ingestion von 9 Boten-Ausgaben.
- **Register-Sync**: Über 40 neue/aktualisierte Entitäten im Personenregister und Organisationsregister.
- **Narrative Infrastructure**: Erstellung von Schlüsselprofilen ([[Solos_Nhergas]], [[Akassvae]], [[Helfric_von_Wallenburg]], etc.).
- **Silicon Inquisition**: Dokumentation der Astralgeflecht-Anomalie (INQ-2026-001).
- **Delegation**: Vorbereitung des Codex-Agents für den "Golden Polish" (Phase 20).
</details>

<details>
<summary><b>Phase 19: Leonardo Sanguine & Master Sketchbook (Feb 2026)</b></summary>

- **Design Pivot**: Abkehr vom Obsidian-Style hin zur "Leonardo Sanguine" Ästhetik.
- **Light & Airy**: Implementierung eines minimalistischen, auf Weißraum und 0.5px Linien basierenden Layouts (v2.4).
- **Abstraktion**: Ersetzung spezifischer Lore-Symbole durch universelle architektonische Geometrie (Kreis, Quadrate, Proportionsstudien).
- **Archivierung**: Lückenlose Sicherung aller Design-Iterationen (Obsidian, Astrael, Sanguine) in `docs/assets/archive/`.
- **Structural Purity**: Sanierung der Markdown-Inkompatibilitäten in allen Register-Tabellen.
</details>

<details>
<summary><b>Phase 18: Toran Dur Advanced Doctrines & Register Polish (Feb 2026)</b></summary>

- [x] Pilot Batch (5/5)
  - [x] Batch 1 (10/10)
  - [ ] Batch 2 (0/10)
- **Batch 27 (Toran Dur Advanced)**: Integration of Sub-Batches 1-4.
- **Arcane Science**: Integration of `Arkan-Metalle.md`, `Elementare_Atomlehre.md`, and `Metamorphose_und_Gestaltwandel.md`.
- **Combat & Counter-Magic**: Detailed articles on `Antimagie_und_Gegenzauber.md` and `Arkane_Kriegfuehrung.md`.
- **Gemstone Magic**: Comprehensive integration of `Vjera_Batama_Magica.md`.
- **Register Maintenance**: Manual deduplication and refinement of magister profiles in `Personenregister.md` (Arenus, Tanthul, Nefustor, etc.).
</details>

<details>
<summary><b>Phase 17: Advanced Intelligence Infrastructure & Lore Reconstruction (Feb 2026)</b></summary>

- **Orakel-Resilience**: Behebung von Permission-Issues durch Cache-Redirection und Optimierung der Boot-Sequenz.
- **Historiker-Workflow**: Einführung des `/historian` Workflows zur Rekonstruktion komplexer Kausalitäten.
- **Lore Reconstruction**: Klärung der "Hauptstadt-Frage". Rohehafen als erste Kolonie (1 n.H.) etabliert; Tiefenbach als Magiezentrum korrigiert.
- **Consistency Blitz**: Vollständige Bereinigung des Personenregisters (Deduplizierung & Erstellung von 25 Stubs). Wiki-Status: 100% konsistent.
- **Chronicler Duties**: Automatisierte Statistik-Generierung und Dokumentations-Audit.
- **Onboarding Workflow**: Einführung von `/start` (`./7w_wiki.py start`) als zentraler Einstiegspunkt für neue Agenten.
</details>

<details>
<summary><b>Phase 16: Magie & Kosmologie (Feb 2026)</b></summary>

- **Batch 25 (Toran Dur Library)**: Vollständige Integration von 13 magietheoretischen und kosmologischen Texten.
- **Dämonologie & Rituale**: Erstellung des `Daimonicon` und der `Rituallehre`.
- **System-Repair**: Healthy Register Status erreicht (0 Duplikate, 0 Orphans).
- **Batch 25c (Toran Dur Reports)**: Integration von 10 weiteren Texten (Forschungsberichte, Ordenssatzung, Sprache Run).
- **Register-Sync**: Vollständige Erfassung der Gründungsmitglieder des Löwenordens und Toran Durs Biographie.
- **Lore-Board**: Erstellung des `LORE_RESEARCH_BOARD.md` zur Nachverfolgung offener Lore-Fragen.
</details>

<details>
<summary><b>Phase 15: Die Verfassung der Verantwortung (Feb 2026)</b></summary>

- **Safe Defaults**: `7w_wiki.py` läuft nun standardmäßig im Advisor-Modus (Situationsbewusstsein zuerst).
- **Konstitution**: Erstellung der `WORKFLOW_ARCHITECTURE.md` (Gewaltenteilung: Legislative, Judikative, Exekutive).
- **Eskalations-Matrix**: Einführung von 3 Log-Levels zur Vermeidung bürokratischer Overheads.
- **Ur-Prozess**: Workflow `/antigravity` als Master-Protokoll etabliert.
- **Judicial Logging**: `Logs/JUDICIARY_LOG.md` für Level-3 Entscheidungen implementiert.
</details>

<details>
<summary><b>Phase 14c: Astrael Integration & System Health (Feb 2026)</b></summary>

- **Batch 23**: Integration von 8 religiösen Texten der Bibliothek Astrael.
- **System-Repair**: Bereinigung von 13 Inkonsistenzen (Gorem-Duplikate, fehlende Profile).
- **Register-Sync**: Konsolidierung von Aspin/Athos und Erstellung von 8 neuen Profilen.
- **Infrastruktur & Tools**: Einführung der semantischen Suche (RAG, Jina v3) sowie Skripte für Statistiken, Link-Weben und Silicon Inquisition.
</details>

<details>
<summary><b>Phase 14b: Recherche, Analyse & Spielergeschichten Processing (Feb 2026)</b></summary>

- **Marnie Ruatha**: Forschungsbericht erstellt. Klärung der Rolle als Hafenvogtin und des Kirchenasyls.
- **Gap-Analyse**: Identifikation fehlender Akte `Tjure_Odal` und Prüfbedarf bei `Arn_Toron`.
- **Batch 20-22**: Integration von 18 Spielergeschichten (Dark Lore, Social, Narrative Arcs).
- **Lore-Härtung**: Definition von "Horwah", Nekromantie-Ritualen und Dämonenseuchen.
- **Register-Sync**: ~20 neue Profile erstellt und verknüpft.
</details>

<details>
<summary><b>Phase 14: Synapsen-System v2.0 & Register-Consolidation (Feb 2026)</b></summary>

- **Live-Test**: Erfolgreicher Batch-Run (`/batch`) für Bibliothek Astrael (`Aequitas`, `Codex`, `Brevier`).
- **Lore Trust Score**: Implementierung der 0-10 Skala und Integration in `lore_score_manager.py`.
- **Register-Consolidation**: Vollständige Integration von "Das Ende der Zeit der Könige" (18 Personen, 6 Organisationen).
- **Conflict Resolution**: Exemplarische Lösung des Delarie-Timeline-Konflikts via Synapse Board.
</details>

<details>
<summary><b>Phase 13: Politische Krisen (Feb 2026)</b></summary>

- [x] **Agenten-Personas**: Dedizierte Instruktions-Dateien für Ingestor, Wächter, Historiker und Koordinator aktiv.
- [x] **Coordination Hub**: Zentrales Grundbuch (`COORDINATION_HUB.md`) für Dokumenten-Registrierung und Board-Metadaten aktiv.
- [x] **Silicon Inquisition**: AI-internes Parallel-Archiv für kritische Hinterfragung und Lore-Hypothesen initialisiert.
- **Boten 181-185**: Rekonstruktion des Putsches in Falkensee und der Führungskrise des Löwenordens.
- **Historiker-Audit**: Fall Benedict Rabenfels (Analyse der Korruption).
- **Register-Cleanup**: 25 Orphans saniert, 9 echte Personen-Duplikate gelöscht.
</details>

<details>
<summary><b>Phase 12: Epistemik & Struktur (Feb 2026)</b></summary>

- **Epistemisches System**: Implementierung der 4 Säulen der Wahrheit (#canon, #bote, #perspektive, #überlieferung) im Style Guide.
- **Eskalationsmatrix**: Definition klarer Regeln zur Auflösung von Lore-Widersprüchen.
- **Wiki v2.0**: Globaler Sanitizer-Lauf über alle Artikel (YAML/H1-Sync).
</details>

<details>
<summary><b>Phase 1: Netz-Wächter & Brand Identity (Feb 2026)</b></summary>

- **Netz-Wächter**: OOC-Timeline (`04_Chronik`) etabliert; Pilot-Ingestion (`siebenwind.de`) erfolgreich.
- **Brand Identity**: Premium-Banner ("Anatomia Magica Mundi"), Logo und Favicon im Renaissance-Stil implementiert.
- **GitHub Deployment**: Wiki live unter `Siebenwind.github.io`. Repository-Transfer an Organisation `Siebenwind`.
- **Documentation Overhaul**: Erstellung von `architecture.md`, `setup_rag.md` und Community-Standards.
- **System-Härtung**: Art Director Skill installiert; CLI zum `7w_wiki.py` Standard vereinheitlicht.
</details>

---
*Zuletzt aktualisiert: 2026-02-17 | Phase 1.19 Handover*
