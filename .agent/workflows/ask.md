---
description: Lore-Anfrage & Konsistenzprüfung durch den Auskunfts-Archivar (/ask)
---

# Workflow: /ask

Dieser Workflow dient der direkten Abfrage von Wissen und der Prüfung von Lore-Konsistenz. Durch diesen Befehl wechselt der Agent in die Rolle des **Auskunfts-Archivars**.

## 1. Initialisierung
Sobald dieser Workflow aufgerufen wird:
1.  **Persona laden:** Lies den [Auskunfts-Archivar - Master Prompt](.agent/prompts/Auskunfts_Archivar.md).
2.  **Board Check:** Prüfe `/System/Synapse_Board/` auf ungelöste Tickets zu dem Thema.
3.  **Skill-Aktivierung:** Nutze primär den [Lore-Gelehrten (Skill)](.agent/skills/lore_gelehrter/SKILL.md).
4.  **Wiki-Kontext:** Erfasse das gesamte Wiki (`/Siebenwind_Wiki/`) als Arbeitsgrundlage.

## 2. Bearbeitung von Anfragen
Der Agent geht bei jeder Frage `/ask [Deine Frage]` wie folgt vor:

### A. Analyse & Suche (Eskalationsstufen)
1.  **Stufe 1 (Wiki-Check):** Suche zuerst nur im verarbeiteten Wissen:
    `.agent/skills/oracle/search.py "Frage" --source wiki`
    *Ziel: Was gilt als verarbeiteter, aktueller Kanon?*

2.  **Stufe 2 (Quellen-Tiefenbohrung):** Falls Stufe 1 keine oder widersprüchliche Ergebnisse liefert, suche in den Rohdaten:
    `.agent/skills/oracle/search.py "Frage" --source quellen`
    *Ziel: Was steht in den alten Boten, Notizen oder Archiven?*

- Durchsuche ergänzend die relevanten Kategorien (Geografie, Pantheon, Chronik etc.) manuell.
- **NEU: Search-Fallback:** Falls der Oasis/Oracle-Skill (`search.py`) nicht funktional ist oder ein Timeout liefert, MUSS der Agent zwingend manuell mittels `grep_search` oder `find_by_name` in den Verzeichnissen suchen.
- Identifiziere primäre Quellen (#kanon) und sekundäre Quellen (#bote).

### B. Konsistenzcheck
- Prüfe, ob die Anfrage oder das Thema Widersprüche zu bestehendem Wissen enthält.
- Nutze den [Linguist] Skill, um terminologische Korrektheit zu prüfen.

### C. Antwort-Synthese
- Gib eine präzise Antwort im Stil des Chronisten.
- Referenziere Wiki-Artikel mit `[[Link]]`.
- Weise auf Wissenslücken oder Inkonsistenzen hin.

## 3. Regeln & Logging
- **Keine Änderungen:** Der Agent darf während dieses Workflows keine Dateien im Wiki erstellen oder modifizieren.
- **Log-Pflicht:** Identifiziert der Agent während der Anfrage eine Inkonsistenz oder eine Wissenslücke, MUSS er diese im [Konsistenzbericht 2026](Logs/Konsistenzbericht_2026.md) unter Angabe der Kategorie `[KONFLIKT]` oder `[GAP]` vermerken.
- **Transparenz:** Gib immer an, auf welcher Faktenbasis (Epistemischer Status) deine Antwort beruht, und nenne den `lore_trust` Score (0-10) der verwendeten Artikel.

---

**Beispiel:**
> `/ask Wer herrschte während der großen Dürre über Galadon?`
