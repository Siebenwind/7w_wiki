---
description: Falandrische Texte übersetzen & Sprachdatensätze pflegen
---

# Workflow: /translate

Dieser Workflow beschreibt die Handhabung des Sprach-Übersetzers für falandrische Dialekte.

## 1. Übersetzung durchführen
Nutze das Skript `translator.py`, um Texte mit Sprach-Flags zu verarbeiten.

**Syntax:**
```bash
python translator.py "[run]Ta'e lahir enwunji[/run]"
```
*Ausgabe: "Ich schreibe Buch"*

## 2. Spracherkennung & Flags
Das System erkennt automatisch Sprachen, für die eine Datei in `.agent/data/languages/` existiert.
- `[run]...[/run]` -> Run (Altgaladonisch)
- `[linfan]...[/linfan]` -> Alt-Linfan (Latein)
- `[ork]...[/ork]` -> Orkisch (Phonetik)

## 3. Neue Sprachen hinzufügen
1. Erstelle eine JSON-Datei in `.agent/data/languages/` (z.B. `zwergisch.json`).
2. Definiere den `tag` (z.B. "zwer") und das Wörterbuch.
3. Das Skript lädt die neue Sprache beim nächsten Start automatisch.

## 4. Datenpflege & Maintenance (Skill: Linguist)
Wenn unbekannte Begriffe (markiert mit `<Wort?>`) auftauchen, muss eine Pflege der Datensätze erfolgen:
1.  **Recherche:** Suche nach dem Begriff in `/Quellen/` (#kanon) oder im [[Siebenwind_Bote]] (#bote).
2.  **Update:** Ergänze die JSON-Datei in `.agent/data/languages/`.
3.  **Wiki-Flaggung:** 
    - Nutze `#kanon`, wenn der Begriff aus offiziellen Hintergrund-Dokumenten stammt.
    - Nutze `#bote`, wenn er nur in Zeitungsartikeln vorkommt.
    - Nutze `#überlieferung` für archaische Begriffe (Run-Sprache).
4.  **Logging:** Vermerke Dialekt-Abweichungen oder widersprüchliche Übersetzungen im [Konsistenzbericht 2026](Logs/Konsistenzbericht_2026.md) unter `[LINGUISTIK]`.

## 5. Korrekte Interpretation
Achte auf den Kontext:
- **Beispiel:** Ein Zwerg aus dem Tal (Arphet) nutzt andere Begriffe als ein Bergzwerg. 
- **Aktion:** Dokumentiere Dialekt-Abweichungen in der [[Linguistik_Übersicht]].

---
// turbo
### Skript-Test
```bash
python translator.py "[run]Gala Hor[/run]"
```
