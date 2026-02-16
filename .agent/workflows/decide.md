---
description: Hochgeschwindigkeits-Workflow für Nutzerentscheidungen (/decide)
---

# Workflow: /decide

## Interop-Status
- runtime_commands:
  - `7w_wiki.py mail inbox --status OPEN`
  - `7w_wiki.py mail read <id>`
  - `7w_wiki.py mail claim <id> --agent <name>`
  - `7w_wiki.py mail done <id> --agent <name>`
- method_only:
  - `/decide`

Dieser Workflow erlaubt es dem Nutzer (Meister), schnell ueber offene Direktiven und Entscheidungsvorlagen zu entscheiden.

## 1. Status-Abfrage
Der Agent listet alle offenen Dispatch-Nachrichten (`OPEN`) und priorisiert jene mit Verweisen auf Konflikt-/Research-Tickets.

## 2. Präsentation
Fuer jede relevante Nachricht praesentiert der Agent:
- **Message-ID & Betreff**
- **Der Konflikt** (Kurzfassung)
- **🧠 Historiker-Meinung** (Lore-Expertise)
- **🏛️ Oberarchivar-Empfehlung** (Verfahrensweise)

## 3. Die Entscheidung
Der Nutzer antwortet mit:
- `/decide [MSG-ID] [Lösungsweg]` (z.B. "Übernimm Siedlungsspuren")
- Oder einfach: `/decide all [Empfehlung]` (Akzeptiert alle Empfehlungen der Agenten).

## 4. Umsetzung (Execution)
1. Der Agent claimgt die Nachricht: `./7w_wiki.py mail claim <id> --agent <name>`.
2. Der Agent fuehrt die entsprechende Aenderung im Wiki bzw. im verlinkten Ticket durch.
3. Falls ein Konflikt-/Research-Ticket referenziert ist: dort finalen Status/Loesung nachziehen.
4. Der Agent schliesst die Nachricht: `./7w_wiki.py mail done <id> --agent <name> --note "<Kurzabschluss>"`.
5. Git Commit: `Lore-Sync: Dispatch <id> umgesetzt.`

---
**Nutzung:** `/decide` (Listet alle) | `/decide MSG-2026-0001 Option A`
