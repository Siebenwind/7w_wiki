---
description: Zentraler Startpunkt & Entscheidungshilfe für neue Agenten
---

# Workflow: `/start` (Das Orakel von Siebenwind)

Willkommen, Oberarchivar. Du stehst vor dem gewaltigen Wissen von 20 Jahren Siebenwind. Dieser Workflow hilft dir, dich zu orientieren und die nächsten Schritte zu wählen.

## 1. Lagefeststellung (Situational Awareness)
Der erste Schritt jedes Agenten ist zu verstehen, wo wir stehen.

// turbo
1. Führe `./7w_wiki.py advisor` aus, um eine aktuelle Status-Analyse zu erhalten.
2. Führe `./7w_wiki.py archive sync` aus, um die Berichts-Symlinks zu aktualisieren.
3. Prüfe die [MASTER_TASK_LIST.md](../../MASTER_TASK_LIST.md) auf Prioritäten.
4. Suche im [Research Board](../../docs/Archiv/Research_Board.md) nach unerledigten Forschungsaufträgen.
5. Verifiziere die Interop-Basis:
   - [SY_INTEROP.md](../../System/Synapse_Board/SY_INTEROP.md)
   - [SY_DISPATCH.md](../../System/Synapse_Board/SY_DISPATCH.md)
   - [SY_STANDARDS.md](../../System/Synapse_Board/SY_STANDARDS.md)
   - [COORDINATION_HUB.md](../../System/COORDINATION_HUB.md)

## 2. Wähle deinen Pfad (Choose your Department)

Welche Rolle nimmst du heute ein?

### 🏛️ Department Lore-Archiv (INGEST)
*Ziel: Rohes Wissen aus den Quellen ins Wiki überführen.*
- **Wann?** Wenn der Advisor meldet, dass noch "Offene Quellen" (Pending) vorhanden sind.
- **Workflow:** `/ingest_master`.

### 🔍 Department Inquisition (CHECK)
*Ziel: Das Wiki sauber halten und Link-Dämonen bannen.*
- **Wann?** Wenn das Audit Fehler meldet oder Brüche in der Verlinkung auffallen.
- **Workflow:** `/check_master`.

### 📜 Department Geschichtsschreibung (LORE)
*Ziel: Komplexe Widersprüche auflösen und tiefe Recherche betreiben.*
- **Wann?** Wenn du einen Forschungsauftrag übernimmst oder User-Fragen zu Lore-Zusammenhängen hast.
- **Workflow:** `/lore_master`.

### 🎨 Das Atelier (HEROLD)
*Ziel: PR, Design und visuelle Aufwertung.*
- **Wann?** Zur Verbesserung der Präsentation oder nach großen Meilensteinen.
- **Workflow:** `/herold`.

### 📦 Department Logistik (META)
*Ziel: Fortschritte dokumentieren und Statistiken pflegen.*
- **Wann?** Am Ende jeder Session oder zur Orientierung.
- **Workflow:** `/meta_master`.

## 3. Goldene Regeln
- **Keine Halluzinationen:** Wenn Wissen fehlt, markiere es mit `[UNGEKLÄRT]` oder schreibe ein Ticket.
- **Relative Links:** Nutze ausschließlich `[[WikiLinks]]`.
- **Epistemische Tags:** Nutze `#canon`, `#bote`, `#perspektive`.

*Bereit? Wähle einen Pfad und beginne dein Werk.*
