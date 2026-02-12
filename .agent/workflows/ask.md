---
description: Lore-Anfrage & Konsistenzprüfung durch den Auskunfts-Archivar (/ask)
---

# Workflow: /ask

Dieser Workflow dient der direkten Abfrage von Wissen und der Prüfung von Lore-Konsistenz. Durch diesen Befehl wechselt der Agent in die Rolle des **Auskunfts-Archivars**.

## 1. Initialisierung
Sobald dieser Workflow aufgerufen wird:
1.  **Persona laden:** Lies den [Auskunfts-Archivar - Master Prompt](file:///Users/alexandrerabe/siebenwind/7w_wiki/Auskunfts-Archivar - Master Prompt.md).
2.  **Skill-Aktivierung:** Nutze primär den [Lore-Gelehrten (Skill)](file:///Users/alexandrerabe/siebenwind/7w_wiki/.agent/skills/lore_gelehrter/SKILL.md).
3.  **Wiki-Kontext:** Erfasse das gesamte Wiki (`/Siebenwind_Wiki/`) als Arbeitsgrundlage.

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
- **Log-Pflicht:** Identifiziert der Agent während der Anfrage eine Inkonsistenz oder eine Wissenslücke, MUSS er diese im [Konsistenzbericht 2026](file:///Users/alexandrerabe/siebenwind/7w_wiki/Logs/Konsistenzbericht_2026.md) unter Angabe der Kategorie `[KONFLIKT]` oder `[GAP]` vermerken.
- **Transparenz:** Gib immer an, auf welcher Faktenbasis (Epistemischer Status) deine Antwort beruht.

---

**Beispiel:**
> `/ask Wer herrschte während der großen Dürre über Galadon?`
