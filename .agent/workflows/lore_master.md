---
description: Department Master Workflow für Lore-Forschung und Narrative
---

# Department: 📜 Geschichtsschreibung (LORE)

Dieses Department klärt komplexe Lore-Widersprüche und veredelt Artikel narrativ. Es fusioniert `/historian`, `/ask`, `/narrative_enrichment` und `/translate`.

## Interop-Status
- runtime_commands:
  - `7w_wiki.py historian <query>`
  - `7w_wiki.py search <query> --source all`
- method_only:
  - `/lore_master`
  - `/ask`
  - `/narrative_enrichment`
  - `/translate`

## 2. Durchführung (Analyse & Veredelung)
Dieses Department nutzt spezialisierte Methoden zur Klärung von Lore-Fragen.

### A. Lore-Analyse
Nutze den [historian.md](../../.agent/workflows/historian.md) (Standard-Analyse) für:
- **Rekonstruktion**: Kausalitäten und zeitliche Abfolgen.
- **Wahrheitsmodell**: Epistemische Einordnung (#canon vs #bote).
- **Gutachten**: Erstellung der finalen historischen Einordnung.

### B. Narrative Veredelung
Nutze [narrative_enrichment.md](../../.agent/workflows/narrative_enrichment.md) zur Aufwertung von Fakt-Artikeln auf **Novel Quality**.

## 3. Projektabschluss
- [ ] Überführung der Erkenntnisse ins Wiki.
- [ ] Schließen des Forschungstickets (CLAIMED -> COMPLETED).

#lore #forschung #geschichte #master
