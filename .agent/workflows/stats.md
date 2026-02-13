---
description: Generiere aktuelle Statistiken für das Siebenwind Wiki
---

Dieser Workflow generiert eine Übersicht über den Wiki-Status, Ingestion-Fortschritt und Lore-Dichte.

1. Führe das Statistik-Skript aus:
// turbo
```bash
python3 .agent/scripts/generate_wiki_stats.py
```

2. Die Ergebnisse werden unter [Wiki_Statistiken.md](file:///Users/alexandrerabe/siebenwind/7w_wiki/Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md) gespeichert.
3. **Lore Trust Metrics:** Ergänze manuell oder via Skript die Anzahl offener/gelöster Tickets vom Board `/System/Synapse_Board/` sowie eine Übersicht der `lore_trust` Verteilung (0-10).

3. (Optional) Committe die Änderungen:
```bash
git add Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md
git commit -m "docs: update wiki statistics"
```
