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
- [x] Wiki-Statistik-Dashboard & `/stats` Workflow (Ingestion, Lore-Dichte, Epistemik, Link-Hubs)
- [x] Dokumentations-Audit (README.md Komplett-Rewrite, MkDocs Deployment-Readiness)

## 🟡 Priorität 2: Inhalte & Ingestion (Massenverarbeitung)
- [/] Integration der verbleibenden 150+ Quellen (Status `Pending` in [[INVENTUR_QUELLEN.md]])
- [x] Erstellung der Geografie-Hauptseiten: [[Brandenstein]], [[Falkensee]], [[Greifenklipp]]
- [x] **Phase 11: Boten 171-175** – Politischer Umbruch (Erlass des Königs, Auflösung der Kronmark, Ersonter Bund, Pakt der Viereinigkeit), klerikale Aufstiege (Benion → Erzgeweihter, Proveus Herand → Erzgeweihter), Dämonen (Blinder Maler, Hutmacher), Terra'Dorotor-Krieg, Schwarzer Samen
- [x] **Phase 12:** Integrate Siebenwind Bote 176-180 (21 n.H.).
- [x] **Phase 13:** Integrate Siebenwind Bote 181-185 (21-22 n.H.).
- [ ] **Boten-Integration:** 10 fehlende Ausgaben (133-140, 191-193) einpflegen (Quellen vorhanden)
- [ ] **Index-Korrektur:** `Die_Chronik.md` vervollständigen (Boten 176-190 fehlen im Index)
- [ ] Laufende Register-Synchronisation (Personen, Organisationen, Bestiarium)

## 🔴 Priorität 3: Qualität & Politur
- [ ] **Orphan-Resolution:** 22 verwaiste Profile zuordnen (siehe Audit-Report)
- [ ] Review aller Stubs auf "Roman-Qualität" (Atmosphäre, Motivation, Kontext)
- [ ] Überprüfung der bi-direktionalen Verlinkung (Backlinks unter `## Überlieferungen`)
- [x] Bereinigung des [[Konsistenzbericht_2026.md]] (Status `⚠️ Offen` in Audit-Prozess überführt)

## 🧠 Priorität 3b: Intelligente Wissensvernetzung (Phase 3)
- [/] **Das Orakel** – RAG-System (Semantische Vektorsuche)
  - [x] Architektur & Modellauswahl (jina-embeddings-v3 + bge-reranker-v2-m3)
  - [x] Setup, Indexierung & Verifikation (Auto-Config via `benchmark_hardware.py`)
  - [x] Historiker-Workflow (Deep Lore Review: Benedict Rabenfels abgeschlossen)
- [x] Register-Audit & Cleanup (Manuelle Bereinigung und Duplikat-Entfernung Feb 2026)
- [x] **Audit der Magieschulen** (Kanon-Bereinigung & Erstellung fehlender Institutionen)

---
*Zuletzt aktualisiert: 13.02.2026 durch Antigravity (Statistik-Dashboard & Dokumentations-Audit)*
