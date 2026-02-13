# Changelog: Siebenwind-Wiki-Rekonstruktion

Alle signifikanten technischen und inhaltlichen Änderungen werden hier festgehalten.

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
