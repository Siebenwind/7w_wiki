---
description: Generiere aktuelle Statistiken für das Siebenwind Wiki
---

Dieser Workflow generiert eine Übersicht über den Wiki-Status, Ingestion-Fortschritt und Lore-Dichte.

## Interop-Status
- runtime_commands:
  - `7w_wiki.py stats`
- method_only:
  - `/stats`

1. Führe den Statistik-Befehl aus:
// turbo
```bash
./7w_wiki.py stats
```

2. Die Ergebnisse werden unter [Wiki_Statistiken.md](../../Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md) gespeichert.
3. **Lore Trust Metrics:** Ergänze manuell oder via Skript die Anzahl offener/gelöster Tickets vom Board `/System/Synapse_Board/` sowie eine Übersicht der `lore_trust` Verteilung (0-10).

3. (Optional) Committe die Änderungen:
```bash
git add Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md
git commit -m "docs: update wiki statistics"
```
