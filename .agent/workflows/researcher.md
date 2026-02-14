---
description: Dedizierter Workflow für Lore-Forschung und das Research Board
---

# Workflow: /researcher (Der Forscher)

Dieser Workflow fokussiert sich auf die systematische Abarbeitung von Forschungsaufträgen und die Verwaltung des `LORE_RESEARCH_BOARD.md`.

## 1. Board-Sichtung
- [ ] Öffne `System/Synapse_Board/LORE_RESEARCH_BOARD.md`.
- [ ] Identifiziere `TENDERED` oder `IN_PROGRESS` Aufgaben.
- [ ] Prüfe verwandte Tickets auf dem `Synapse_Board`.

## 2. Research-Setup
- [ ] Erstelle ein Arbeitsticket basierend auf `_TEMPLATE_RESEARCH.md`.
- [ ] Claimer: Setze deinen Namen und das aktuelle Datum.

## 3. Vertiefte Forschung (Historian Mode)
- [ ] Wechsle in den **Historiker-Modus**:
    - Nutze `./7w_wiki.py search "[Thema]" --source all --top 50`.
    - Durchsuche `/Quellen/Hintergrund/` manuell nach Axiomen.
    - Befrage das **Orakel** zu Kausalzusammenhängen.

## 4. Dokumentation der Erkenntnisse
- [ ] Erstelle einen Forschungsbericht unter `Logs/Research/[ID]_[Thema].md`.
- [ ] Fasse die Quellenlage zusammen: Was ist gesichert (#canon), was ist Gerücht (#überlieferung)?

## 5. Transfer ins Wiki
- [ ] Überführe die Erkenntnisse in bestehende oder neue Wiki-Artikel.
- [ ] Nutze den **Wiki-Schmied** Standard (UUID, Frontmatter, relative Links).
- [ ] Setze das Board-Ticket auf `COMPLETED` und verlinke den Wikipedia-Artikel / Forschungsbericht.

#recherche #forscher #historik #board #wissen
