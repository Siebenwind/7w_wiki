---
name: Der Lektor (Qualitätssicherung)
description: Automatisierte Prüfung von Stil, Grammatik und Markdown-Formatierung für konsistente "Siebenwind Voice".
---

# Der Lektor – Qualitätssicherung

**Epistemischer Status:** #tool

Der Lektor ist ein CLI-Tool, das Markdown-Dateien gegen den **Siebenwind Style Guide** prüft. Er agiert als erste Instanz der Qualitätssicherung, bevor ein Mensch (oder der Oberarchivar) den Text finalisiert.

## Features

1.  **Stil-Prüfung:**
    - Findet verbotene Begriffe (z.B. "Level", "XP", "Spawn" außerhalb von OOC-Blöcken).
    - Warnt bei zu vielen Anglizismen.
    - Prüft auf "Passiv-Wüsten" (zu häufige Nutzung des Passivs).
2.  **Format-Prüfung:**
    - Validiert YAML Frontmatter (Pflichtfelder: layout, title, category).
    - Prüft H1-Titel-Übereinstimmung.
    - Findet tote interne Links (TODO).
3.  **Auto-Fix (Optional):**
    - Kann einfache Formatierungsfehler automatisch beheben.

## Nutzung

```bash
# Einzelne Datei prüfen
python3 .agent/skills/lektor/style_checker.py "Siebenwind_Wiki/Chronik/Schlacht_um_Siebenwind.md"

# Ganzen Ordner prüfen
python3 .agent/skills/lektor/style_checker.py "Siebenwind_Wiki/Chronik/"
```

## Konfiguration

Die Regeln sind in `style_guide.json` definiert.

| Regel | Beschreibung |
|-------|--------------|
| `no_go_words` | Liste von Begriffen, die nicht im Fließtext vorkommen dürfen. |
| `preferred_terms` | Wörterbuch für Ersetzungen (z.B. "Character" -> "Charakter"). |
| `passive_threshold` | Max. Prozentsatz an Passiv-Sätzen pro Absatz. |
