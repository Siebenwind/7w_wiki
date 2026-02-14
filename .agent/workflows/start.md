---
description: Zentraler Startpunkt & Entscheidungshilfe für neue Agenten
---

# Workflow: `/start` (Das Orakel von Siebenwind)

Willkommen, Oberarchivar. Du stehst vor dem gewaltigen Wissen von 20 Jahren Siebenwind. Dieser Workflow hilft dir, dich zu orientieren und die nächsten Schritte zu wählen.

## 1. Lagefeststellung (Situational Awareness)
Der erste Schritt jedes Agenten ist zu verstehen, wo wir stehen.

// turbo
1. Führe `./7w_wiki.py advisor` aus, um eine aktuelle Status-Analyse zu erhalten.
2. Prüfe die [MASTER_TASK_LIST.md](file:///Users/alexandrerabe/siebenwind/7w_wiki/MASTER_TASK_LIST.md) auf Prioritäten.
3. Suche im [Synapse Board](file:///Users/alexandrerabe/siebenwind/7w_wiki/System/Synapse_Board/LORE_RESEARCH_BOARD.md) nach unerledigten Forschungsaufträgen.

## 2. Wähle deinen Pfad (Options)

Welche Rolle nimmst du heute ein?

### 🛡️ Pfad A: Der Ingestor (Quell-Verarbeitung)
*Ziel: Rohes Wissen aus den Quellen ins Wiki überführen.*
- **Wann?** Wenn der Advisor meldet, dass noch "Offene Quellen" (Pending) vorhanden sind.
- **Tools:** `/batch`, `/ingestion_protocol`.

### ⚖️ Pfad B: Der Lektor (Qualität & Konsistenz)
*Ziel: Das Wiki sauber halten und Link-Dämonen bannen.*
- **Wann?** Wenn der Advisor/Audit Fehler meldet oder Brüche in der Verlinkung auffallen.
- **Tools:** `/repair`, `/audit`.

### 🏛️ Pfad C: Der Historiker (Lore-Klärung)
*Ziel: Komplexe Widersprüche auflösen und tiefe Recherche betreiben.*
- **Wann?** Wenn du einen Forschungsauftrag übernimmst oder User-Fragen zu tiefen Lore-Zusammenhängen hast.
- **Tools:** `/historian`, `/ask`.

### 📊 Pfad D: Der Chronist (Wartung & Reporting)
*Ziel: Fortschritte dokumentieren und Statistiken pflegen.*
- **Wann?** Am Ende jeder Session oder nach großen Batches.
- **Tools:** `/stats`, `/docs`, `/handover`.

## 3. Goldene Regeln
- **Keine Halluzinationen:** Wenn Wissen fehlt, markiere es mit `[UNGEKLÄRT]` oder schreibe ein Ticket.
- **Relative Links:** Nutze ausschließlich `[[WikiLinks]]`.
- **Epistemische Tags:** Nutze `#canon`, `#bote`, `#perspektive`.

*Bereit? Wähle einen Pfad und beginne dein Werk.*
