---
description: Dedizierter Workflow für Lore-Forschung und das Research Board
---

# Workflow: /researcher (Der Forscher)

## Interop-Status
- runtime_commands:
  - `7w_wiki.py search <query> --source all`
  - `7w_wiki.py historian <query>`
  - `7w_wiki.py mail post --from <agent> --to <agent>`
- method_only:
  - `/researcher`

Dieser Workflow fokussiert sich auf die systematische Abarbeitung von Forschungsaufträgen und die Verwaltung des `LORE_RESEARCH_BOARD.md`.

## 1. Board-Sichtung
- [ ] Öffne `System/Synapse_Board/LORE_RESEARCH_BOARD.md`.
- [ ] Identifiziere `TENDERED` oder `IN_PROGRESS` Aufgaben.
- [ ] Prüfe verwandte Tickets auf dem `Synapse_Board`.

## 2. Research-Setup
- [ ] Erstelle ein Arbeitsticket basierend auf `_TEMPLATE_RESEARCH.md`.
- [ ] Claimer: Setze deinen Namen und das aktuelle Datum.

## 3. Vertiefte Forschung (Analyse)
Die Analyse der Quellen und die Klärung von Kausalitäten folgen dem Historiker-Protokoll.

> [!TIP]
> Sie see [historian.md](../../.agent/workflows/historian.md) für die methodische Vorgehensweise bei komplexen Lore-Fragen.

## 4. Dokumentation & Wiki-Transfer
- [ ] Erstelle einen Forschungsbericht unter `Logs/Research/[ID]_[Thema].md`.
- [ ] Überführe die Erkenntnisse ins Wiki gemäß **Wiki-Schmied** Standard.
- [ ] Setze das Board-Ticket auf `COMPLETED`.

#recherche #forscher #historik #board
