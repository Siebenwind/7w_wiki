---
description: Zentraler Startpunkt & Entscheidungshilfe für neue Agenten
---

# Workflow: `/start` (Das Orakel von Siebenwind)

## Interop-Status
- runtime_commands:
  - `7w_wiki.py advisor`
  - `7w_wiki.py mail inbox --status OPEN`
  - `7w_wiki.py test --suite clean-client-state`
  - `7w_wiki.py archive sync`
- method_only:
- interop_note: `7w_wiki.py start` shows the workflow by default; `--run` executes the checklist; `--resume` resumes workflow state.
- codex_bridge_name: session_start
- codex_bridge_enabled: true
- codex_bridge_summary: Codex kickoff wrapper for the standard onboarding loop.
- codex_bridge_primary_command: `7w_wiki.py start`
- codex_bridge_followups:
  - `7w_wiki.py advisor --json`
  - `7w_wiki.py mail inbox --status OPEN`
  - `7w_wiki.py test --suite clean-client-state`

Willkommen, Oberarchivar. Du stehst vor dem gewaltigen Wissen von 20 Jahren Siebenwind. Dieser Workflow hilft dir, dich zu orientieren und die nächsten Schritte zu wählen.

## 1. Lagefeststellung (Situational Awareness)
Der erste Schritt jedes Agenten ist zu verstehen, wo wir stehen.

// turbo
1. Führe `./7w_wiki.py advisor` aus, um eine aktuelle Status-Analyse zu erhalten.
2. Führe `./7w_wiki.py mail inbox --status OPEN` aus und bewerte offene Aufträge.
3. Führe `./7w_wiki.py test --suite clean-client-state` aus.
4. Führe `./7w_wiki.py archive sync` aus, um die Berichts-Symlinks zu aktualisieren.
5. Prüfe die [MASTER_TASK_LIST.md](../../MASTER_TASK_LIST.md) auf Prioritäten.
6. Suche im [Research Board](../../System/Synapse_Board/LORE_RESEARCH_BOARD.md) nach unerledigten Forschungsaufträgen.
7. Verifiziere die Interop-Basis:
   - [SY_INTEROP.md](../../System/Synapse_Board/SY_INTEROP.md)
   - [SY_DISPATCH.md](../../System/Synapse_Board/SY_DISPATCH.md)
   - [SY_TESTING.md](../../System/Synapse_Board/SY_TESTING.md)
   - [SY_STANDARDS.md](../../System/Synapse_Board/SY_STANDARDS.md)
   - [COORDINATION_HUB.md](../../System/COORDINATION_HUB.md)
8. Lies die aktuellste Session-Memory unter `Logs/Archive/SESSION_MEMORY_*.md` (falls vorhanden), bevor du neue Tasks startest.
9. Wenn der Advisor `Pages Health` als `WARN`, `FAIL` oder `UNKNOWN` meldet, route zuerst zu `/tech_master`.

## 2. Wähle deinen Pfad (Choose your Persona & Master-Workflow)

Welche Rolle nimmst du heute ein? Das System ist in **5 Säulen (Pillars)** unterteilt. Wähle den exakten Master-Workflow, der zu deiner Aufgabe passt.

### 🔭 Web-Aufklärung
*Ziel: Die Grenzen des Wikis überwinden und das Web nach neuem Wissen scannen.*
- **Wann?** Wenn du neue Updates von der Homepage oder dem Forum einholen willst.
- **Workflow:** `/scout`.
- **Forum-first Quellenjagd:** Nutze `/forum_search`, wenn du gezielt nach neuen ingestierbaren Forenquellen suchst.

### 🏛️ The Ingestor (Department Lore-Archiv)
*Ziel: Rohes Wissen aus den Quellen ins Wiki überführen.*
- **Wann?** Wenn der Advisor meldet, dass noch "Offene Quellen" (Pending) vorhanden sind.
- **Master-Workflow:** `/ingest_master`.

### 🛡️ The Guardian (Department Inquisition / QA)
*Ziel: Das Wiki sauber halten und Link-Dämonen bannen.*
- **Wann?** Wenn das Audit Fehler meldet, Links brechen, oder User PRs einreichen.
- **Master-Workflow:** `/qa_master`.

### 📜 The Historian (Department Geschichtsschreibung)
*Ziel: Komplexe Widersprüche auflösen, Kanon-Updates pflegen und Artikel literarisch anreichern.*
- **Wann?** Wenn du einen Forschungsauftrag übernimmst, User-Fragen beantwortest (Oracle) oder "Roman-Qualität" erzeugen willst.
- **Master-Workflow:** `/lore_master`.

### ⚙️ The Technician (Der Maschinenraum)
*Ziel: CI/CD, Scripts, GitHub Actions und Architektur am Laufen halten.*
- **Wann?** Wenn Pages-Builds fehlschlagen, Skripte Bugs haben oder Doku-Syncs nötig sind.
- **Master-Workflow:** `/tech_master`.

### 📦 The Coordinator (Department Meta & Logistik)
*Ziel: Fortschritte dokumentieren, Statistiken pflegen und den menschlichen Leitpunkt überwachen.*
- **Wann?** Am Ende jeder Session, für Dashboards, oder zur globalen Orientierung.
- **Master-Workflow:** `/meta_master`.

## 3. Goldene Regeln
- **Keine Halluzinationen:** Wenn Wissen fehlt, markiere es mit `[UNGEKLÄRT]` oder schreibe ein Ticket.
- **Relative Links:** Nutze ausschließlich `[[WikiLinks]]`.
- **Epistemische Tags:** Nutze `#canon`, `#bote`, `#perspektive`.
- **Keine Bridge-Placeholders:** Repariere Verweise auf kanonische Ziele; nutze temporäre Brücken nur mit Ticket + Review-Datum.

*Bereit? Wähle einen Pfad und beginne dein Werk.*
