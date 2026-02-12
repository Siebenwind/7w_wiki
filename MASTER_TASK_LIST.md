# Master Task List: Siebenwind-Wiki-Rekonstruktion

Dieses Dokument ist das agentenübergreifende Gedächtnis des Projekts. Jeder Agent muss seinen Fortschritt hier dokumentieren.

## 🟢 Priorität 1: Infrastruktur & Sicherheit
- [x] Standardisierung des Wikis auf v2.0 (YAML, H1, Links)
- [x] Implementierung der Markdown-First Quellen-Architektur
- [x] Automatische Referenz-Korrektur (HTML -> MD Links)
- [x] Proaktives Konsistenz-Logging (Logging before Writing)
- [x] Etablierung der 4-stufigen Wahrheitshierarchie (Kanon > Lokale Quelle > Live-Web > User)
- [x] Reorganisation des Projekt-Folders (Prompts, Skripte, Logs aufräumen)
- [x] GitHub Integration & Community Workflows (MkDocs, Issue Templates, PR-Audit)

## 🟡 Priorität 2: Inhalte & Ingestion (Massenverarbeitung)
- [/] Integration der verbleibenden 150+ Quellen (Status `Pending` in [[INVENTUR_QUELLEN.md]])
- [x] Erstellung der Geografie-Hauptseiten: [[Brandenstein]], [[Falkensee]], [[Greifenklipp]]
- [ ] Aufbau eines zentralen **Boten-Archivs** (Index der Chronik)
- [ ] Laufende Register-Synchronisation (Personen, Organisationen, Bestiarium)

## 🔴 Priorität 3: Qualität & Politur
- [ ] Review aller Stubs auf "Roman-Qualität" (Atmosphäre, Motivation, Kontext)
- [ ] Überprüfung der bi-direktionalen Verlinkung (Backlinks unter `## Überlieferungen`)
- [ ] Bereinigung des [[Konsistenzbericht_2026.md]] (Status `⚠️ Offen` abarbeiten)

## 🧠 Priorität 3b: Intelligente Wissensvernetzung (Phase 3)
- [/] **Das Orakel** – RAG-System (Semantische Vektorsuche)
  - [x] Architektur & Modellauswahl (jina-embeddings-v3 + bge-reranker-v2-m3)
  - [/] Setup, Indexierung & Verifikation
  - [ ] Historiker-Workflow (Deep Lore Review)

---
*Zuletzt aktualisiert: 12.02.2026 durch Antigravity (Takeover Complete)*
