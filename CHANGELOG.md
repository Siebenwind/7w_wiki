# Changelog: Siebenwind-Wiki-Rekonstruktion

Alle signifikanten technischen und inhaltlichen Änderungen werden hier festgehalten.

## [2026-02-12.4] - Das Orakel (RAG-System)
### Hinzugefügt
- `.agent/skills/oracle/SKILL.md`: Skill-Definition für semantische Vektorsuche.
- `.agent/skills/oracle/build_index.py`: Indexierungsskript mit Semantic-Aware Chunking, Auto-Tagging, zwei getrennten Collections.
- `.agent/skills/oracle/search.py`: Suchskript mit Zwei-Stufen-Pipeline (Embedding + Re-Ranking).
- `.agent/skills/oracle/setup.sh`: Einrichtungs-Skript (venv, Dependencies, Modell-Download).

### Technische Details
- **Embedding:** `jinaai/jina-embeddings-v3` (570M Params, 8192 Token Kontext, LoRA-Adapter)
- **Re-Ranker:** `BAAI/bge-reranker-v2-m3` (568M Params, Cross-Encoder)
- **Chunking:** 2500 Zeichen, 300 Overlap, Paragraph-/Satz-aware Splitting
- **GPU:** Apple MPS Beschleunigung

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
