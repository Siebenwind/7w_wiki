---
description: Hochgeschwindigkeits-Workflow für Nutzerentscheidungen (/decide)
---

# Workflow: /decide

Dieser Workflow erlaubt es dem Nutzer (Meister), schnell über offene Lore-Konflikte auf dem Synapse-Board zu entscheiden.

## 1. Status-Abfrage
Der Agent listet alle Tickets im Verzeichnis `/System/Synapse_Board/` auf, die den Status `AWAITING_USER` haben.

## 2. Präsentation
Für jedes Ticket präsentiert der Agent:
- **ID & Titel**
- **Der Konflikt** (Kurzfassung)
- **🧠 Historiker-Meinung** (Lore-Expertise)
- **🏛️ Oberarchivar-Empfehlung** (Verfahrensweise)

## 3. Die Entscheidung
Der Nutzer antwortet mit:
- `/decide [ID] [Lösungsweg]` (z.B. "Übernimm Siedlungsspuren")
- Oder einfach: `/decide all [Empfehlung]` (Akzeptiert alle Empfehlungen der Agenten).

## 4. Umsetzung (Execution)
1. Der Agent führt die entsprechende Änderung im Wiki durch.
2. **Internal Marking:** Wenn die Entscheidung vom Kanon abweicht oder eine Lücke schließt, wird die Stelle im Wiki-Text mit `[Intervention: Rank 0]` (unsichtbar im gerenderten Wiki / HTML, sichtbar im Markdown) markiert.
3. Der Agent aktualisiert das Ticket:
   - Status: `HUMAN_RESOLVED`
   - trust_level: 0 (User-Canon)
   - Lösung (FINAL) wird ausgefüllt.
4. Git Commit: `Lore-Sync: Ticket [ID] durch User-Entscheid gelöst (Rank 0).`

---
**Nutzung:** `/decide` (Listet alle) | `/decide 2026-001 Option A`
