## [2026-02-15.28] - Phase 1.11: CI/CD Reliability & Success
### Hinzugefügt
- **Headers**: `docs/_headers` Datei zur Deaktivierung des CDN-Caches implementiert.

### Geändert
- **Stability**: Build-Prozess in `deploy.yml` durch Entfernung von `--strict` stabilisiert.
- **Engine**: Inkompatible Plugin-Parameter (`slugify`, `reference_type`) aus `mkdocs.yml` entfernt.

## [2026-02-15.27] - Phase 1.10: Link Engine Stabilization
### Geändert
- **WikiLinks**: Umstellung des gesamten Link-Engine-Standards auf das `ezlinks`-Modell.
- **Standard**: `STYLING.md` an die neue technische Realität angepasst.

## [2026-02-15.26] - Phase 1.9: CI/CD Troubleshooting
### Hinzugefügt
- **Build**: Automatisierte Installation aller Abhängigkeiten via `requirements.txt` im CI-Workflow.
- **Debug**: Transparenz-Schritte (`cat` Befehle) in die Build-Pipeline integriert.

## [2026-02-15.25] - Phase 1.8: Cleanup & Organization
### Geändert
- **Root-Ordner**: Verschiebung von Meta-Dokumenten (`STYLING.md`, `WORKFLOW_LORE_CONSISTENCY.md`, PDF-Analyse) nach `System/`.
- **Assets**: Konsolidierung von `assets/` nach `System/Design_Assets/`.
- **Cleanup**: Entfernung von `banner_proposal.png` und `git-push-log.aR0d5B`.

## [2026-02-15.24] - Phase 1.7: Styling & Engine Optimization
### Hinzugefügt
- **Build**: `requirements.txt` für automatisierten Plugin-Install auf GitHub Pages erstellt.
- **Design**: Renaissance-Typografie (Inter & Cormorant Garamond) und Micro-Animations für Links.

### Geändert
- **Plugins**: Migration von `wikilinks` (Extension) auf `mkdocs-ezlinks-plugin` (Plugin) zur Behebung der Broken Links.
- **Header**: Quadratisches Banner durch horizontales „Modern Scholar“ Banner ersetzt (`docs/assets/banner.png`).
- **UI**: Glassmorphism-Effekte für Header, Nav und Footer implementiert (Blured Transparency).

## [2026-02-15.23] - Phase 1.6: Structural Maintenance & Consistency Repair
### Hinzugefügt
- **Persönlichkeiten**: 11 neue Profil-Stubs angelegt (u.a. [[Eliam_Schlosser]], [[Geist]], [[Himduir_III_ap_Vjer]]).

### Geändert
- **Register**: Manuelle Deduplizierung von [[Chernides]] und [[Orgolosch]].
- **Verknüpfung**: Korrekte Einbindung der [[Gropp_Zwillinge]] und [[Kregor_Arthax_Stahlauge]] ins Personenregister.
- **Mission MSG-2026-0002**: Globale Bereinigung von absoluten `file://` Pfaden in Wiki- und System-Dokumenten.

## [2026-02-15.22] - Phase 1.5: Minimalist Restoration & Structural Purity
### Hinzugefügt
- **Standard**: `STYLING.md` zur Kodifizierung des "Minimalist Tool" Ansatzes und der Symlink-Architektur.
- **System**: Native `wikilinks` Extension aktiviert für stabilere `[[WikiLink]]` Auflösung auf GitHub Pages.

### Geändert
- **Design**: Pivot zum "Modern Scholar" Aesthetic (Beige/Rötel, Hochkontrast, schlichte Funktionalität).
- **Tonalität**: Vollständige Neutralisierung der Texte auf Landing-Page und Architektur-Dokumenten (Entfernung von "Flavor Text").
- **Copyright**: Aktualisierung der Claims (LeCorbeau für Technik, Autoren/Projekt für Inhalte).
- **Struktur**: Verifizierung und Sicherung der Symlink-Struktur (`docs/Siebenwind_Wiki` -> `Siebenwind_Wiki`).

## [2026-02-15.21] - Phase 20: Deep Bote Ingestion & Codex Delegation
### Hinzugefügt
- **Wiki-Inhalt (Chronik)**: Tiefgreifende Anreicherung der Boten-Seiten 186 bis 194.
- **Persönlichkeiten**: Über 20 neue Profile erstellt (u.a. [[Solos_Nhergas]], [[Akassvae]], [[Helfric_von_Wallenburg]]).
- **System**: Delegations-Prompt `System/DELEGATION_CODEX_PHASE_20.md` für den narrativen Feinschliff erstellt.
- **Silicon Inquisition**: Forschungsbericht `INQ-2026-001_Historian_Report.md` zum Astralgeflecht.

### Geändert
- **Register**: Über 40 Einträge in `Personenregister.md` und `Organisationsregister.md` synchronisiert.
- **Konfiguration**: `.gitignore` um Delegations-Dateien erweitert.
- **Handover**: `MASTER_TASK_LIST.md` auf Phase 20 aktualisiert.

## [2026-02-15.20] - Production Persistence Layer (Conclusions, Ideas, Artworks, Presentations)
### Hinzugefügt
- **Protokoll**: `System/PRODUCTION_PROTOCOL.md` als verbindliche Persistenzregel für erzeugte Artefakte.
- **Präsentation**: `Logs/Presentations/2026-02-15_Interop_Dossier_Praesentation.md`.
- **Vorlagen**: `System/Templates/PRODUCTION_NOTE_TEMPLATE.md` für standardisierte Ergebnisablagen.
- **Ablageordner**: `Logs/Conclusions/`, `Logs/Ideas/`, `Logs/Artworks/`, `Logs/Presentations/`.

### Geändert
- **Standards**: `SY_STANDARDS.md` um `PRODUCTION_PROTOCOL` ergänzt.
- **Coordination Hub**: Register um Produktionsprotokoll und Vorlage erweitert.

## [2026-02-15.19] - Interop Phase 3: Relative Links, Workflow Runtime Markers, Re-Evaluation
### Hinzugefügt
- **Dossier**: `Logs/Ingestion/2026-02-15_Interop_Dossier_Phase3.md` als offizieller Nachher-Befund.
- **Workflow-Härtung**: `runtime_commands`/`method_only` Blöcke in den Department-Workflows ergänzt.

### Geändert
- **Pfad-Normierung**: Antigravity-Workflows und Koordinationsdokumente auf kontextkorrekte relative Links umgestellt.
- **Inquisition-Quellenverweise**: Historian-Report und Manifest von absoluten URI-Referenzen auf relative Pfade migriert.
- **Re-Audit**: Linkkonsistenz nach Migration verifiziert; nur definierte Platzhalter bleiben offen.

## [2026-02-14.18] - News Reconstruction, Forum Indexing, and Synapse Dispatch
### Hinzugefügt
- **News-Archiv**: Vollstaendige Quellenanlage fuer Homepage-News ab 2010 unter `Quellen/News/` (standardisiertes Frontmatter).
- **Forum-Kategorien**: Neue Quellenkategorien `Quellen/Forum/Bekanntmachungen` und `Quellen/Forum/Newsticker` fuer technische/teambezogene Forenhinweise.
- **Synapse Dispatch**:
    - Neues Board-Dokument `System/Synapse_Board/SY_DISPATCH.md`.
    - Persistente Queue unter `System/Synapse_Board/DISPATCH/`.
    - Neue CLI-Erweiterung `7w mail ...` fuer Agent-zu-Agent Nachrichten (`post`, `inbox`, `read`, `claim`, `done`).

### Geändert
- **Chronik**: `Siebenwind_Wiki/04_Chronik/OOC_TIMELINE.md` um News- und Forum-Auswertung erweitert.
- **Standards**: `System/Synapse_Board/SY_STANDARDS.md` um Board-Eintrag `SY_DISPATCH` erweitert.
- **CLI**: `7w_wiki.py` um Subcommand `mail` ergaenzt.

## [2026-02-15.01] - Phase 19.4: Structural Purity & Automation
### Hinzugefügt
- **Automatisierung**: Skript `generate_wiki_indices.py` zur automatischen Erstellung von Kategorie-Indizes.
- **CLI**: Neuer Befehl `./7w_wiki.py index-pages` zur Wartung der Wiki-Hierarchie.
- **Dokumentation**: `CONTRIBUTING.md` für Community-Kollaboration und Lizenz-Governance.

### Geändert
- **Navigation**: Umstellung auf explizite Pfade in `mkdocs.yml` zur Vermeidung von 404-Fehlern in Unterverzeichnissen.
- **Branding**: Bereinigung der Homepage von veraltetem Slogan-Lore ("Diskretion").
- **Statistiken**: Dashboard-Refresh für den neuen Struktur-Stand.

## [2026-02-14.17] - Phase 19: Light Sanguine & General Abstraction
### Hinzugefügt
- **Visuals**: Neues "Light Sanguine" Branding-System (Rötelzeichnung im Leonardo-Stil).
- **Asset-Archiv**: Dediziertes Archiv unter `docs/assets/archive/` für Design-Konzepte.
- **Mockups**: High-Fidelity UI-Mockup des Interface-Konzepts für zukünftige Iterationen (Sanguine-Stil).

### Geändert
- **Interface Design**: Umstellung auf v2.4 (Paper-Minimalism, Thin Lines, Sanguine & Sepia).
- **Integrität**: Korrektur von Rendering-Fehlern in Markdown-Tabellen (Register).
- **Abstraktion**: Wechsel von spezifischer Astrael-Symbolik zu allgemeiner Architektur-Geometrie.

## [2026-02-14.16] - Phase 19: GitHub Pages Overhaul & Link Repair
### Hinzugefügt
- **Wiki-Plugins**: Aktivierung von `mkdocs-roamlinks-plugin` zur Unterstützung von `[[WikiLinks]]`.
- **Visuals**: Vollständiges Redesign der Homepage (`index.md`) im "Lore Engine" Stil.
- **Navigation**: Strukturierte `mkdocs.yml` mit Direktzugriff auf Register und Chronik.
- **GitHub Actions**: Automatisierte Installation der notwendigen Plugins im Deployment-Workflow.

### Geändert
- **Link-System**: Konvertierung aller statischen Pfade in `index.md` auf relative Formate.
- **Aestetik**: Umstellung der Farbpalette auf "Slate & Gold" (Renaissance-Tech Look).
- **Cleanup**: Entfernung der Art-Director-Sektion von der Homepage (Fokus auf Lore & Tech).

### Hinzugefügt
- **Visual Identity**: Premium-Banner ("Anatomia Magica Mundi"), Logo und Favicon im Renaissance-Stil implementiert.
- **System**: CLI zu `7w_wiki.py` vereinheitlicht; `Art Director` Skill für Stil-Konsistenz installiert.
- **GitHub**: Repository erfolgreich an Org `Siebenwind` übertragen und via GitHub Pages deployt.

## [2026-02-14.13] - Batch 26: Toran Dur Ingestion (Pfad A)
### Hinzugefügt
- **Wiki-Content**:
    - **Magietheorie**: `Locus_Magicae.md`, `Magietheorie_Toran_Dur.md` (Arcana Procella), `Artefaktlehre.md`.
    - **Forschung**: `Bartanatomie.md` (Goldaxt), `Finsterwangen.md` (Krise 14 n.H.), `Brandenstein.md` (Diamant-Matrix).
    - **Bestiarium**: Klassifizierung nach Liebig (**Lazperday** vs **Warthun**).
- **Register**:
    - Neue Personas: `Birnbaum`, `Fogrim Goldaxt`, `Logrin Goldaxt`, `Johannes Klos`, `Johann Liebig`, `Hernaphas Lenarmberg`, `Hahngard Esteron`.
    - Updates: `Kida Gilwen`, `Kalveron Dai`.

## [2026-02-14.12] - Batch 27: Toran Dur Advanced Doctrines (Sub-Batches 1-4)
### Hinzugefügt
- **Wiki-Content**:
    - **Constructs**: `Konstruktbau_und_Ariin.md`, `Erschaffene_Diener.md`.
    - **Arcane Science**: `Arkan-Metalle.md`, `Elementare_Atomlehre.md`.
    - **Combat/Defense**: `Antimagie_und_Gegenzauber.md`, `Arkane_Kriegfuehrung.md`.
    - **Transformation/Gems**: `Metamorphose_und_Gestaltwandel.md`, `Vjera_Batama_Magica.md`.
- **Register**:
    - Synchronisation der Magister: `Edomawyr`, `Jennaia Lavrial`, `Nistram Rigas`, `Erynnion Comari`, `Lewyn Anacar`, `Sylest le Felyhn`.
    - Manuelle Bereinigung und Deduplizierung (u.a. `Arenus`, `Tanthul`, `Nefustor`, `Amanda Dunkelbaum`).
    - Neueinträge: `Arlin Sturmfels`, `Santanos Alexandrius von Eichstatt`.

### Geändert
- **Wiki-Statistiken**: Dashboard aktualisiert (1027 Artikel, 546 Persönlichkeiten).

## [2026-02-14.11] - Infrastructure: Ingestion 3.0 & Oracle Hardening
### Hinzugefügt
- **Ingestion v3.0**: 
    - Einführung des **Lore Quality Score (LQS)** (0-10) zur Bewertung von Extraktionen.
    - Neues Template: `System/Templates/INGESTION_REPORT_TEMPLATE.md`.
    - Dedizierter Ablageort für Reports: `Logs/Ingestion/`.
- **Sandbox-Resilience**:
    - Automatische Sandbox-Erkennung via `ANTIGRAVITY_AGENT` und `ANTIGRAVITY_SANDBOX`.
    - Implementierung von `local_files_only=True` für embedding und reranking Modelle.

### Geändert
- **Orakel-Optimierung**: 
    - Behebung der XLMRoberta-Warnung durch gezielten Proxy-Logging-Patch (Monkey-Patch).
    - Performance-Bestätigung (Search ~20s in Sandbox-Umgebung).
- **Projekt-Wartung**: 
    - Repository-Cleanup (Löschen von Root-Junk wie `.DS_Store`, `missing_links.txt`, `walkthrough.md`).
    - Korrektur der Dokumentationspfade in `README.md`.
    - Archivierung alter Logs in `Logs/Archive/`.

### Entfernt
- Veraltete `walkthrough.md` im Root-Verzeichnis.
- Temporäre Register-Logs.

## [2026-02-14.10] - Lore Reconstruction: The Origins of Siebenwind
### Hinzugefügt
- **Wiki-Archiv**: `Logs/Historian_Report_2026_003_Siebenwind_Origins.md` als Forschungs-Zusammenfassung erstellt.
- **Geografie**: `Rohehafen.md` (Ehemalige Hauptstadt der ersten Kolonie) erstellt.

### Geändert
- **Lore-Zentralisierung**: 
    - `Tiefenbach.md`: Status als Hauptstadt entfernt; Fokus auf Hafen und Magie-Akademie (historisch).
    - `Finsterwangen.md`: Fokus auf den Sphärenriss und die Galahad-Verteidigung präzisiert.
    - `Historie_&_Ären.md`: Umfassender Retcon der Hilgorad-Expedition (1 n.H.) und der "Ersten Kolonie".
    - `Hilgorad_I_ap_Mer.md`: Rolle als Expeditions-Initiator ergänzt.
    - `Siebenwind.md`: Regionen-Übersicht um Rohehafen ergänzt.
    - `Stadtchronik_Rohehafens.md`: Als historisches Dokument markiert (vordatiert auf ca. 5 n.H.).
- **Research Board**: RESEARCH-2026-005 und 006 als `COMPLETED` markiert.

## [2026-02-14.9] - Documentation & Maintenance: Path D (Der Chronist)
### Hinzugefügt
- **Wiki-Statistiken**: Neues Statistik-Dashboard generiert (984 Artikel, 521 Persönlichkeiten). Dokumentiert unter `Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md`.
- **Projekt-Wartung**: Überprüfung der zentralen Dokumentation (`README.md`, `WORKFLOW_LORE_CONSISTENCY.md`, `SYNAPSEN_SYSTEM_SPEC.md`).
- **Onboarding-Status**: Fortschreibung des `/start` Prozesses und Festlegung der nächsten Prioritäten.

### Geändert
- **Wiki-Integrität**: Validierung der Pfade für Lore-Engineering-Dokumente im `.agent/docs/` Verzeichnis.

## [2026-02-14.7] - Phase 17: Infrastructure & Intelligence
### Hinzugefügt
- **Finsterwangen / Tiefenbach Korrektur**:
    - `Tiefenbach.md`: Als historische Hauptstadt ("Jassavia-Analogie" auf der Insel) definiert.
    - `Finsterwangen.md`: Als Festung der Galahad-Legende definiert (nicht Jassavia/Hauptstadt).
    - `Historie_&_Ären.md`: Trennung von Jassavia (Festland) und Tiefenbach (Insel).
    - `Die_Legende_von_Galahad_Ritter_der_Rosen.md`: Verlinkungen korrigiert.
- **Lore-Untersuchungen**:
    - **Astralnetz-Ursprung**: Kontroverse (Kirche vs. Toran Dur) in `Astrael.md`, `Toran_Dur.md`, `Die_Gohor.md` dokumentiert.
    - **Ionas Narrative**: `Ionas.md` mit atmosphärischen Detailsangereichert (Resolved Synapse Ticket 2026-003).

### Geändert
- **Synapse Board**:
    - Ticket `Conflict_2026-003_Ionas_Narrative` geschlossen (RESOLVED).
    - Ticket `Conflict_TEST_001_Falkensee_Timeline` geschlossen (RESOLVED durch Finsterwangen-Lore).
- **Onboarding Workflow**: Neuentwickelter `/start` Prozess (`./7w_wiki.py start`) für eine strukturierte Agenten-Übernahme.
- **Historiker-Workflow**: `/historian` Workflow zur tiefen Analyse von Kausalitäten und Lore-Rekonstruktion.
- **Lore Audit**: Protokoll und Template für Lore-Peer-Reviews und Eskalationen bei Unsicherheit.
- **CLI Erweiterung**: Unified CLI (`7w_wiki.py`) unterstützt nun `start`, `historian` mit Query-Support und flexiblen Oracle-Parametern (`--cpu`, `--no-re-rank`).

### Geändert
- **Orakel-Redirection**: Aggressive Umleitung aller HuggingFace- und Transformers-Caches in das Projektverzeichnis (`.agent/data/models`) zur Umgehung von Sandbox-Restriktionen.
- **Orakel-Redirection**: Aggressive Umleitung aller HuggingFace- und Transformers-Caches in das Projektverzeichnis (`.agent/data/models`) zur Umgehung von Sandbox-Restriktionen.
- **Indexer-Stabilität**: Fix eines kritischen Bugs im Index-Builder, der bei Einzeldatei-Updates fälschlicherweise den restlichen Index gelöscht hat.

## [2026-02-14.8] - Batch 25c: Toran Dur Reports & Order of the Lion
### Hinzugefügt
- **Wiki-Content**:
    - **Toran Dur**: Umfassendes Personenprofil und Biographie.
    - **Forschungsberichte**: Integration von `Forschungsberichte (Toran Dur)`, `Index Siebenwind (Toran Dur)`, `Die Sprache Run (Toran Dur)`.
    - **Magietheorie**: Integration von `Die Magie (Toran Dur)`, `Lehrbuch der Magietheorie (Toran Dur)`, `Theorien der Magie (Toran Dur)`, `Magica Curativa (Toran Dur)`, `Daimonologie und Schwarze Magie (Toran Dur)`.
    - **Historie/Recht**: `Die Ordenssatzung des Ordens vom Wachenden Löwen (Toran Dur)`, `Graue Charta (Zweiter Entwurf)`.
- **Register**:
    - **Löwenorden**: Erfassung der Gründungsmitglieder 17 n.H. (`Cendaric Tibur`, `Lothar Gavinwald`, `Akora Dur`, `Dorion Hali`).
    - **Personen**: Diverser Magier und Zeitgenossen (`Nefustor`, `Rianna`, `Caieta Ajunier`, etc.).
- **System**:
    - `INVENTUR_QUELLEN.md`: Status-Update für 20+ Toran Dur Dateien auf `Integrated`.

### Geändert
- **Personenregister**: Konsolidierung von Cendaric Tibur (Baron & Ordensmeister) und Dorion Hali (Physikus & Ordensmeister).

## [2026-02-14.6] - Batch 25: Toran Dur Magie-Bibliothek & System Audit
### Hinzugefügt
- **Batch 25: Toran Dur Library**:
    - Integration der magietheoretischen Grundlagen (8 Texte: Matrix, Elemente, Zensor etc.).
    - Integration der praktischen Arkanologie (5 Texte: Dämonologie, Alchemie, Rituale, Zeit- & Sphärentheorie).
    - Erstellung zentraler Magie-Artikel: `Daimonicon`, `Rituallehre_Sphaeren`, `Alchemie_Grundlagen`, `Sphaerenkunde_Kosmologie`.
    - Profile für `Kulin_Laetall`, `Rhadan_der_Graue`, `Kida_Gilwen`, `Wolfgang_Ravinsthal`, `Dunvallo_Linari`.
- **System & Lore**:
    - **Lore Research Board**: `LORE_RESEARCH_BOARD.md` zur workflow-gestützten Lore-Klärung.
    - **System Audit**: Durchführung des `/audit` Workflows (Report 2026-02-14). 
    - **Register Status**: Healthy Register bestätigt (0 Duplikate/Orphans).

### Geändert
- **Wiki-Statistiken**: Dashboard aktualisiert (923 Artikel, Lore-Hubs neu berechnet).
- **Repair Tool**: `repair.py` auf aktuelle Wiki-V2.1-Struktur angepasst.

### Hinzugefügt
- **Konstitutionelles Framework**:
    - `WORKFLOW_ARCHITECTURE.md`: Einführung der strategischen Architektur (Trias Politica Modell).
    - `/antigravity`: Neuer Master-Workflow für strikte, skriptgesteuerte Exekution.
    - `Logs/JUDICIARY_LOG.md`: Offizielles Entscheidungsprotokoll für kritische Lore-Eingriffe (Level 3).
    - `.agent/tests/TEST_CASES.md`: Validierungssuite für das Systemverhalten.
- **Eskalationsstufen**: Definition von 3 Leveln (Standard, Kontrolliert, Judiziell) zur Balance zwischen Effizienz und Sicherheit.

### Geändert
- **7w CLI (`7w_wiki.py`)**: Advisor-Modus ist nun der Default-Befehl (Situationsbewusstsein bei Start).
- **Onboarding (`takeover.md`)**: Mandat für High-Verification und Subdivision-Prinzipien.

## [2026-02-14.4] - Batch 23: Astrael Religious Texts
### Hinzugefügt
- **Batch 23: Bibliothek Astrael**:
    - Integration von 8 religiösen Texten und Mythen: `Der_Blutrote_Stier`, `Der_Traum_der_Tausend`, `Der_letzte_Falke`, `Der_naive_Mensch`, `Die_Eisernen_Tafeln`, `Die_Goldenen_Tafeln`, `Die_Silbernen_Tafeln`, `Die_Legende_von_Galahad_Ritter_der_Rosen`.
    - Erstellung von 8 Personenprofil-Stubs: `Azaris`, `Barnabas`, `Dannor`, `Galahad`, `Irindal`, `Jeremias`, `Kedrin`, `Tai_Sah_Halour_Glurias`.
- **System-Wartung**:
    - Vorbereitende Konsistenzprüfung und Bereinigung von 13 initialen Fehlern (Gorem, etc.).
    - Bereinigung von Duplikaten (Aspin, Athos) nach Register-Sync.

## [2026-02-14.3] - Spielergeschichten Integration (Batches 20-22)
### Hinzugefügt
- **Batch 20: Dark Lore & Cults**:
    - Neue Artikel: `Die_Namikleris`, `Kraken`, `Logbuch_des_Kerkers`, `Solfeister_Kin`, `Die_Verbrennung_des_heiligen_Markus`, `Ritus_Gebet_und_Erleuchtung`.
    - Register-Updates: `Szarmaduk`, `General Hornstoß`, `Knochenfürst`, `Markus`, `Mehr'thak`.
- **Batch 21: Social & Tales**:
    - Neue Artikel: `Die_Zwergen_WG`, `Geschaeftiges_Treiben`, `Nachts_im_Brandensteiner_Tempel`, `Pruefung_und_Entsagung`, `Pueppchens_Flucht`, `Letzte_Vorbereitungen`, `Die_Elemente_ungleiche_Geschwister`.
    - Register-Updates: `Gimbart`, `Nirluk`, `Sandholz`, `Gorion`, `Püppchen`, `Lucienne`.
    - Lore-Korrektur: **Horwah** als Manifestationen/Avatare der Götter definiert (User-Feedback).
- **Batch 22: Narrative & Character Arcs**:
    - Neue Artikel: `Abschied_und_Verrat`, `Abweisungen`, `Alles_ohne_Pointe`, `Aus_dem_Leben_eines_Schwarzmagiers`, `Briefe_aus_der_Ferne`.
    - Register-Updates: `Todward von Saalhorn`, `Aelfrid Wildgaden`, `Dorion Hali`, `Felix Goldschein`, `Taleris Kreytz`, `Rajka Sanseha`.

### Geändert
- **Personenregister**: Bereinigung von Duplikaten und Konsolidierung von Einträgen (Akora, Taleris, Rajka).
- **Ingestion Log**: Lückenlose Dokumentation aller Verarbeitungsschritte.

## [2026-02-14.3] - Recherche Marnie Ruatha & Handover
### Hinzugefügt
- **Forschungsbericht**: `Forschungsbericht_Marnie_Ruatha.md` (Intern) erstellt.
    - Zusammenstellung der Biographischen Daten (Hafenvogtin 19-21 n.H., Asyl 22 n.H.).
    - Analyse der Boten 167, 168, 173, 186.
- **Gap-Identifikation**:
    - `Tjure_Odal`: Fehlt im System (Lücke).
    - `Arn_Toron`: Vorhanden, aber Prüfung empfohlen.

### Geändert
- **Dokumentation**:
    - `MASTER_TASK_LIST.md`: Aktualisiert.
    - `Wiki_Statistiken.md`: Neu generiert (837 Artikel, 472 Persönlichkeiten).

## [2026-02-14.2] - Synapsen-System v2.0 & Register-Consolidation
### Hinzugefügt
- **Synapsen-System v2.0**: Erfolgreicher End-to-End Test des neuen Konfliktlösungs-Frameworks.
    - **Lore Trust Score (0-10)**: Automatisierte Berechnung integriert (`lore_score_manager.py`).
    - **Synapse Board**: Ticketsystem für Konflikte (`Conflict_2026-003_Delarie_Timeline`).
- **Register-Consolidation**:
    - **Quelle**: "Das Ende der Zeit der Könige" (Spielergeschichte) vollständig integriert.
    - **Personen**: 18 neue Profile (u.a. `Zoran_Gosh`, `Hadrian_Lugado`, `Hubertus_Anverita`).
    - **Organisationen**: 6 neue Organisationen (u.a. `Ring_des_Argionemes`, `Bruderschaft_Gofilm`).
- **Wiki-Content**:
    - Neue Artikel: `Codex_Iuris_Canonici`, `Aequitas`, `Brevier_des_Ordo_Astraeli` (Bibliothek Astrael).

### Geändert
- **Priorisierung**: User-Eingaben (`#user_canon`) sind nun vom Trust-Score entkoppelt (Score reflektiert Quellenreinheit, nicht Zustimmung).


## [2026-02-14.1] - Historiker-Review: Delarie & Glaron
### Geändert
- **Waldemar Delarie (`Waldemar_Delarie.md`)**:
    - **Timeline-Retcon**: "Reise nach Papin" von 25-28 n.H. auf **21 n.H.** korrigiert (Fit für Bote 183/Putsch).
    - **Titel**: Ergänzung um "Regierungsrat" und "Adjutant".
    - **Lore**: Erweiterung der "Gerüchteküche" (Spinnen-Vorfall, Besessenheit).
- **William Glaron (`William_Glaron.md`)**:
    - **Biografie-Erweiterung**: Vom Stub zum Vollprofil (Turniersieger 21 n.H., Tragödie 22 n.H.).
    - **OOC-Integration**: Berücksichtigung der späteren Erhebung zum Ritter und der Auflösung des "Diener des Einen"-Plots.
- **System**:
    - **Orakel**: Permission-Issue bei `search.py` dokumentiert (Workaround via grep genutzt).

## [2026-02-13.9] - Wiki Consistency Restoration- 🏛️ **Total Consistency Restoration:** Alle 69+ Konsistenzprobleme im Personenregister behoben (0 Duplikate, 0 Orphans, 0 Missing Profiles).
- ✍️ **Stub Creation:** 57 neue Profil-Stubs für registrierte Charaktere erstellt.
- 🔗 **Register Fixes:** Naming-Mismatches (Apostrophe, Leerzeichen) in `Personenregister.md` korrigiert.
- 📜 **New Workflow:** `/repair` Workflow zur systematischen Fehlerbehebung implementiert.
## [2026-02-13.8] - Epistemics & Source Ingestion Audit (Interrupted)
### Hinzugefügt
- **Epistemisches System**: Formale Einführung der Verlässlichkeitsränge (#canon, #bote, #perspektive, #überlieferung) im Style Guide und in der Eskalationsmatrix des RVW-Loops.
- **Ingestion Log**: Dokumentation der Re-Scan Ergebnisse für ~30 Spielergeschichten (Batches 1-8).

### Geändert
- **Metadata-Härtung**: YAML Frontmatter und Status-Tags für ~20 Spielergeschichten ergänzt/korrigiert (u.a. `Jassavia`, `Blutschwert`, `Waldemar Delarie`).
- **Kanon-Schutz**: Widersprüchliche oder subjektive Tags (#verstorben, #tragödie) durch formale epistemische Tags ersetzt.

### Ergebnisse
- Das Wiki verfügt nun über ein robustes System zur Handhabung von Wahrheitsansprüchen.
- Ein Großteil der Spielergeschichten ist metadata-technisch saniert; Entitäten sind für die Register-Integration im Log gesichert.

## [2026-02-13.7] - Narrative Enrichment & Orphan Resolution
### Hinzugefügt
- **Narrative Enrichment**:
    - `narrative_enrichment.md`: Neuer Workflow für "Roman-Qualität".
    - `Ionas.md` & `Maichellis_Wanderstern.md`: Von Stubs zu narrativen Profilen aufgewertet (Atmosphäre, Motivation, Zitate).
- **Orphan-Resolution**:
    - 4 Duplikate gelöscht (`Siegfried_von_Steiner`, `Fedral`, `Feldherr`, `Toron`).
    - 15 fehlende Personen im Register nachgetragen (u.a. `Winzlig`, `Lucius_Gropp`).
    - `Benedict_Rabenfels`: Als Stub wiederhergestellt.

### Geändert
- **Register-Synchronisation**: `Personenregister.md` ist nun vollständig synchron mit dem Dateisystem (25 Orphans processed).
- **Inhalte**: `Arn_Toron.md` erhielt die Backstory aus der gelöschten Duplikat-Datei (`Toron.md`).

### Ergebnisse
- Das Personenregister ist bereinigt und vollständig.
- Erste Schlüsselcharaktere (Ionas, Maichellis) entsprechen dem neuen Qualitätsstandard.

## [2026-02-13.7] - Feature Drop: Orakel & Skills v2.0
### Hinzugefügt
- **Das Orakel:** Vollständiges RAG-System (Search, Indexing, MPS-Tuning).
- **Skills v2.0:**
    - `Der Lektor` (Style-Checker & QA).
    - `Workflow /repair` (Interaktive Wartung).
    - `Workflow /watch` (Live-Indexierung).
- **Der Berater:** `advisor.py` für automatisiertes `/takeover`.
### Geändert
- **Dokumentation:**
    - `README.md` komplett überarbeitet und modularisiert.
    - Neue Benutzerhandbücher für Skills erstellt.
- **System:** `setup.sh` aktualisiert (neue Dependencies).
### Geändert
- **Phase 12 (Boten 176-180):** Complete.
    - Verified content for Boten 176-180.
    - Verified/Updated articles: `Bestie_von_Brandenstein`, `Trollkrieg_von_Brandenstein`, `Die_Spinnenplage_von_Falkensee`, `Kharas_Palanthas`.
    - Created new article: `Hevelius_Dunkelfeld` (Bote 180).
    - Updated `Personenregister.md` (Resolved duplicates for Solice, Gottfried, Merthes, Caoimme; added Dunkelfeld).
    - Updated `Organisationsregister.md` (Added `Kult_des_Einen`).
    - Verified `Zeitleiste` (21 n.H. entries).
- **Wiki-Statistiken:** Aktualisiert via `/stats`.

## [2026-02-13.5] - Phase 13 Abschluss (Falkensee Putsch)
### Hinzugefügt
- **Phase 13 (Boten 181-185):** Integrated 5 issues.
    - Standardized Boten 181-185.
    - Updated `Personenregister.md` (Ionas, Serass, Astreyonas, Delarie).
    - Updated `Zeitleiste_(15-30_n.H.).md` (21 n.H. Falkensee Coup completely covered).
    - Updated `INVENTUR_QUELLEN.md` (All 181-185 Integrated).
    - Validated `Ionas.md` and `Serass.md` dates.

### Ergebnisse
- Der "Putsch von Falkensee" ist nun vollständig dokumentiert.
- Die Timeline für das Jahr 21 n.H. ist mit Bote 185 abgeschlossen.
- Wiki-Statistiken wurden aktualisiert (`/stats`).

## [2026-02-13.4] - Phase 11 Abschluss & Phase 12 Vorbereitung
### Hinzugefügt
- **Phase 12 Planung:** Detaillierte Recherche der Boten 176-180 (Bestie von Brandenstein, Troll-Krieg, Spinnenplage, Mord an Palanthas).
- `implementation_plan.md`: Update mit granularer Task-Liste für Phase 12.

### Geändert
- [x] **Phase 12 (Boten 17-180):** Integrated 5 issues.
    - Standardized Boten 176-180.
    - Updated `Personenregister.md` (Palanthas †, Aurora, Delarie, Merthes).
    - Updated `Zeitleiste_(15-30_n.H.).md` (21 n.H. filled).
    - Updated `INVENTUR_QUELLEN.md`.
- [x] **Phase 11 (Boten 171-175):** Complete.
- **Inventur:** Boten 171-175 erfolgreich von `Pending` auf `Integrated` gesetzt.

### Ergebnisse
- Das Fundament für die Integration der Boten 176-180 ist gelegt.
- Kritische Ereignisse (Rücktritt Noalim, Tod Falk, Mord Palanthas) sind identifiziert und vorbereitet.

## [2026-02-13.3] - Wiki-Statistiken & Dokumentations-Audit
### Hinzugefügt
- `.agent/scripts/generate_wiki_stats.py`: Automatisiertes Statistik-Dashboard (Ingestion, Lore-Dichte, Epistemik, Link-Hubs, Temporal-Density).
- `Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md`: Visualisierte KPIs mit Mermaid-Charts.
- `.agent/workflows/stats.md`: Neuer Workflow `/stats` zur Dashboard-Generierung.
- `docs/`: Symlink-Verzeichnis für MkDocs-Kompatibilität (Symlinks zu Wiki, README, CHANGELOG, MASTER_TASK_LIST).

### Geändert
- **README.md (Komplett-Rewrite):** Alle 8 Skills, 14 Workflows und 8 Scripts vollständig dokumentiert.
- **mkdocs.yml:** Mermaid-Support (custom_fences), fehlende Nav-Einträge (Erzählungen, Wiki Statistiken), `docs_dir`/`site_dir` korrekt gesetzt.
- **Workflow-Integration:** `/stats` als Pflichtschritt in `/audit` (§7) und `/handover` (§6.3) integriert.
- **.gitignore:** `site/` hinzugefügt.

### Ergebnisse
- **666 Artikel**, **349 Persönlichkeiten**, **~98k Wörter**, **72 Links/1k Wörter** (Vernetzungsgrad).
- MkDocs-Build erfolgreich (3.99s, keine Errors).

## [2026-02-13.2] - [ ] **Phase 14: Spielergeschichten Re-Scan** – Fortsetzung der Ingestion (Batches 9+), Register-Sync der extrahierten Entitäten.
- [x] Laufende Register-Synchronisation (Personen, Organisationen, Bestiarium)

## 🔴 Priorität 3: Qualität & Politur
- [x] **Orphan-Resolution:** 25 verwaiste Profile bearbeitet (Duplikate gelöscht, Register ergänzt)
- [x] Review wichtiger Stubs auf "Roman-Qualität" (Ionas, Maichellis Wanderstern)
- [ ] Überprüfung der bi-direktionalen Verlinkung (Backlinks unter `## Überlieferungen`)
- [x] **Epistemik-System:** Formale Trust-Hierarchy und Eskalationsmatrix implementiert.
- [x] Bereinigung des [[Konsistenzbericht_2026.md]] (Status `⚠️ Offen` in Audit-Prozess überführt)

## 🧠 Priorität 3b: Intelligente Wissensvernetzung (Phase 3)
- [/] **Das Orakel** – RAG-System (Semantische Vektorsuche)
  - [x] Architektur & Modellauswahl (jina-embeddings-v3 + bge-reranker-v2-m3)
  - [x] Setup, Indexierung & Verifikation (Auto-Config via `benchmark_hardware.py`)
  - [x] Historiker-Workflow (Deep Lore Review: Benedict Rabenfels abgeschlossen)
- [x] Register-Audit & Cleanup (Manuelle Bereinigung und Duplikat-Entfernung Feb 2026)
- [x] **Audit der Magieschulen** (Kanon-Bereinigung & Erstellung fehlender Institutionen)

## 🔮 Future / Backlog (Ideenspeicher)
- [ ] **Skill: „Der Kartograph“** – Geographische Datenverwaltung, Koordinaten-Sync, Reisezeiten-Berechnung.
- [ ] **Skill: „Der Herold“** – Automatische Generierung von In-Game-Newslettern aus Wiki-Änderungen.
- [ ] **Workflow: `/map_sync`** – Verknüpfung von Wiki-Orten mit der Weltkarte.
- [ ] **Workflow: `/changelog_generate`** – Erstellung von "Was ist neu in der Welt"-Berichten.
- [ ] **Workflow: `/cleanup`** – Automatisches Finden und Bereinigen von file-URLs in Wiki-Artikeln.

---
*Zuletzt aktualisiert: 13.02.2026 durch Antigravity (Epistemics & Ingestion)*
## [2026-02-13.2] - Audit der Magieschulen (Kanon-Härtung)
### Hinzugefügt
- **Kanonische Institutionen**: 
    - `Königliche Akademie der arkanen Künste` (Zentrales Element).
    - `Magierturm zu Tiefenbach` (Historisch/Zerstört).
    - `Akademie der Schwarzen Künste` (Historisch/Verboten).
 
### Geändert
- **Kanon-Bereinigung**: 
    - Entfernung der nicht-kanonischen "Akademie des Grünen Zweiges" aus `Region_Tiefenwald.md`.
    - Entfernung der nicht-kanonischen "Akademie in den Grauen Höhlen" aus `Region_Kadamark.md`.
    - Korrektur der Verlinkungen in `Graue_Garde.md` auf die offizielle Königliche Akademie.
- **Register-Update**: Vollständige Integration der neuen Akademien in `Organisationsregister.md` und `registry.jsonl`.

### Ergebnisse
- Erfolgreiche Eliminierung von "Fanon"-Elementen (Halluzinationen), die sich in die Regionsbeschreibungen eingeschlichen hatten.
### [Batch 24] - Astrael's Legacy (II) - 2026-02-14
- **Dateien**: 19 historische & theologische Schriften der Bibliothek Astrael integriert.
- **Highlights**: Stadtchronik Rohehafens, Myten-Bericht, Matrixtheorie von Derrvus, Ritus der Exercitio.
- **Register**: 12+ neue Entitäten synchronisiert (Derrvus, Anais, Aelwin, etc.).

### [Batch 23] - Astrael's Erbe (I) - 2026-02-14
- **Ingestion:** Verarbeitung von 5 Spielergeschichten (Batch 19).
- **Entitäten:** Erstellung von 12+ neuen Personenprofilen und 3 Organisationen.
- **Lore:** Dokumentation der Argionemes-Verschwörung und der Schwarzen Legion.
- **Wartung:** Konsolidierung von Dubletten und Update des Personenregisters.
- Klare Trennung zwischen aktiven (Königliche Akademie) und historischen (Tiefenbach, Schwarze Künste) Magieschulen hergestellt.
### [Phase 14] - 2026-02-13
- **Ingestion:** Verarbeitung von 5 Spielergeschichten (Batch 19).
- **Entitäten:** Erstellung von 12+ neuen Personenprofilen und 3 Organisationen.
- **Lore:** Dokumentation der Argionemes-Verschwörung und der Schwarzen Legion.
- **Wartung:** Konsolidierung von Dubletten und Update des Personenregisters.
- Klare Trennung zwischen aktiven (Königliche Akademie) und historischen (Tiefenbach, Schwarze Künste) Magieschulen hergestellt.

## [1.12.0] - 2026-02-15
### Added
- `System/SYSTEM_INTEGRITY.md`: Codification of directory structures and safety rules.
- Redirection Stubs: `Hochelfen.md`, `Löwenorden.md`, etc. to fix WikiLink aliases.

### Changed
- WikiLink Engine: Migrated from `ezlinks` to `roamlinks` (Case-Sensitivity Fix).
- Build Workflow: Replaced problematic symlinks in `docs/` with physical sync logic in `deploy.yml`.
- Standardized file naming for "Das Ende der Zeit der Könige" (Removed pipes).
- Registry Polish: Consolidated `Organisationsregister` and `Personenregister` into clean, continuous table formats.
- Research Board: Standardized current task visualization in `MASTER_TASK_LIST.md`.

## [1.11.0] - 2026-02-15
- **Ingestion:** Verarbeitung von 5 Spielergeschichten (Batch 19).
- **Entitäten:** Erstellung von 12+ neuen Personenprofilen und 3 Organisationen.
- **Lore:** Dokumentation der Argionemes-Verschwörung und der Schwarzen Legion.
- **Wartung:** Konsolidierung von Dubletten und Update des Personenregisters.
- Klare Trennung zwischen aktiven (Königliche Akademie) und historischen (Tiefenbach, Schwarze Künste) Magieschulen hergestellt.

## [2026-02-13.1] - Historiker-Review & Register-Cleanup
### Hinzugefügt
- `Logs/Historiker_Bericht_Rabenfels_2026.md`: Detaillierter Bericht über Benedict Rabenfels und die Führungskrise des Löwenordens.

### Geändert
- **Metadaten-Härtung**: 
    - Einführung von ISO-8601 Zeitstempeln **mit Uhrzeit** für alle Metadaten (`letzter_check`).
    - Neue performante JSONL-Registry (`registry.jsonl`) zur Dokumentenverfolgung.
    - Standardisierung aller Boten (133-140) mit permanenten UUIDs.
- **Register-Cleanup**: 
    - Zusammenführung von Duplikaten (Steiner, Bitterling, Eisenbruch, Arman, Delarie, Caeden, Wendolyn, Horan Erandel).
    - Konsolidierung von Karrieredaten (z.B. Fedral Lavid, Benion Sandelholz).
    - Bereinigung von Dateisystem-Dubletten (`Woran_Lebensmüh.md`).
- **Lore-Konsistenz**:
    - Dokumentation der Diskrepanz zwischen Bote 172 (Tibur/Avistur als Halbgeschwister) und Wiki (als Onkel/Nichte).

### Ergebnisse
- Das Profil von Benedict Rabenfels wurde dekomponiert, die Erkenntnisse aber im Historiker-Bericht gesichert.
- Die Register-Synchronität wurde durch die Konsolidierung von Mehrfacheinträgen signifikant verbessert.

## [2026-02-12.5] - Konsistenz-Offensive & Workflow-Härtung
### Hinzugefügt
- `.agent/scripts/register_check.py`: Automatisiertes Audit-Tool (findet Duplikate, Orphans, Boten-Lücken, Index-Lücken).
- `Logs/Audit_Report_2026-02-12.md`: Detaillierter Bestandsbericht der Register-Integrität.

### Geändert
- **Workflow-Härtung (`rvw_loop` & `wiki_schmied`)**:
    - **Pre-Write Validation:** Pflicht-Check auf Duplikate vor Erstellung.
    - **Post-Write Sync:** Automatische Index-Aktualisierung (Chronik & Register).
    - **Relative Pfade:** `quelle:`-Feld im Frontmatter erlaubt nur noch relative Pfade.
    - **Referenzen:** Neue Pflicht-Sektion `## Referenzen` mit akademischer Zitierweise.
- **Audit-Prozess**:
    - ISO-8601 Zeitstempel-Pflicht für alle Berichte.
    - Neue "Orphan-Resolution" Phase für verwaiste Profile.

### Ergebnisse
- Audit identifizierte 9 echte Personenduplikate, 22 Orphans, 10 fehlende Boten (Quellen existieren) und 15 Index-Lücken.
- "Orts-Stubs" Issue (Brandenstein, Falkensee, Greifenklipp) final gelöst.

## [2026-02-12.4] - Das Orakel (RAG-System)
### Hinzugefügt
- `.agent/skills/oracle/SKILL.md`: Skill-Definition für semantische Vektorsuche.
- `.agent/skills/oracle/build_index.py`: Indexierungsskript mit Semantic-Aware Chunking, Auto-Tagging, zwei getrennten Collections.
- `.agent/skills/oracle/search.py`: Suchskript mit Zwei-Stufen-Pipeline (Embedding + Re-Ranking).
- `.agent/skills/oracle/setup.sh`: Einrichtungs-Skript (venv, Dependencies, Modell-Download).

- **Hardware-Optimierung:** `benchmark_hardware.py` (Auto-Tuner) für Jina v3 auf Apple Silicon.
- **Learnings:** Jina v3 (8192 Context) nutzt Flash Attention, was auf MPS bei langen Texten (>2000 Chars) zu massivem Memory-Swapping führt. 
  - **Lösung:** Batch-Size drastisch reduzieren (32 -> 2) für stabilen Betrieb auf 16GB RAM.
- **Embedding:** `jinaai/jina-embeddings-v3` (570M Params, 8192 Token Kontext, LoRA-Adapter)
- **Re-Ranker:** `BAAI/bge-reranker-v2-m3` (568M Params, Cross-Encoder)
- **Chunking:** 2500 Zeichen, 300 Overlap, Paragraph-/Satz-aware Splitting

## [2026-02-12.3] - GitHub-Interaktivität & Automatisierung
### Hinzugefügt
- `.github/workflows/deploy.yml`: Automatische Konvertierung und Deployment nach GitHub Pages.
- `mkdocs.yml`: Konfiguration für das professionelle Wiki-Layout (MkDocs Material).
- `.github/ISSUE_TEMPLATE/lore_conflict.yml`: Strukturierte Lore-Tickets für Nutzer.
- `.agent/workflows/contrib_audit.md`: Neuer Prozess für die Prüfung von Community-Beiträgen (PRs).

## [2026-02-12.2] - Projekt-Reorganisation & Cleanup
### Hinzugefügt
- Strukturierte Unterverzeichnisse: `.agent/prompts/`, `.agent/scripts/`, `.agent/docs/`, `Logs/Archive/`.

### Geändert
- **Projekt-Struktur**: Alle Management-Dateien, Prompts und Skripte wurden aus dem Root-Verzeichnis in logische Unterordner verschoben.
- **Referenz-Update**: Alle internen Pfade in README, Workflows, Master-Prompts und Skripten wurden an die neue Struktur angepasst.
- **Cleanup**: Temporäre Extraktionslogs und alte Zips wurden nach `Logs/Archive/` verschoben.

## [2026-02-12.1] - Infrastruktur-Update & Massen-Integration
### Hinzugefügt
- `source_integrator.py`: Skript zur Integration hochwertiger Markdown-Quellen und Archivierung von Originalen.
- `reference_fixer.py`: Skript zur Korrektur interner Wiki-Links von `.html` zu `.md`.
- `MASTER_TASK_LIST.md`: Globales Aufgabenverzeichnis für Agenten.
- `CHANGELOG.md`: Dieses Dokument.

### Geändert
- **Wahrheitshierarchie (Korrektur)**: Der lokale Kanon (`/Hintergrund`) ist nun die absolute Letztinstanz. Das Live-Web dient der Verifikation und Ergänzung. Die neue Eskalation lautet: Kanon > Lokale Quelle > Homepage > User.

### Integriert
- 254 Markdown-Quellen erfolgreich ins Wiki-System integriert.
- `Brevier der Kirche der Viere.md` als neue Quelle identifiziert und verarbeitet.

---
*Archivar: Antigravity*
