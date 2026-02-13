---
layout: wiki_page
name: Lore-Gelehrter (Analytik & Auskunft)
description: Fähigkeit, das gesamte Wiki-Wissen zu aggregieren, Inkonsistenzen zu finden und präzise Auskunft zu geben.
---

# Lore-Gelehrter (Skill)

**Epistemischer Status:** #kanon

Dieser Skill ermöglicht es dem Agenten, als Experten-System zu agieren, das Wissen vernetzt betrachtet.

## Arbeitsweise

### 1. Ganzheitliche Analyse
- Durchsucht nicht nur einzelne Dateien, sondern stellt Querbeziehungen zwischen `/Geografie/`, `/Pantheon/` und `/Chronik/` her.
- **Ziel:** Erkennen von Mustern (z.B. "Diese Person kann zu diesem Zeitpunkt nicht an jenem Ort gewesen sein").

### 2. Inkonsistenz-Prüfung
- Vergleicht neue Informationen oder Hypothesen mit dem "Ground Truth" im `/Hintergrund/`.
- Zeigt logische Brüche in Erzählungen auf.
- Nutzt den [Linguist] Skill, um Inkonsistenzen in der Namensgebung oder Sprachverwendung zu finden (z.B. "Ein Talzwerg würde diesen Begriff nicht nutzen").

### 3. Aktive Ticket-Lösung (Synapsen-Board)
- Überwacht das Verzeichnis `/System/Synapse_Board/` auf Tickets mit Status `NEEDS_REVIEW`.
- Führt automatisierte RAG-Suchanfragen (Oracle) durch, um Beweise für oder gegen eine Behauptung zu finden.
- Verwendet die **Eskalationsmatrix** (v2.1) zur Entscheidung.
- **Interaktive Eskalation:** Wenn keine eindeutige Lösung möglich ist, setzt das Ticket auf `AWAITING_USER` und bereitet die Zusammenfassung für den "Council of Truth" (User-Loop) vor.

### 4. Sachliche Auskunftserteilung
- Formuliert Antworten auf Basis von Evidenz:
    - "Laut [[Chronik_Ereignis]] geschah dies im Jahr..."
    - "Im Widerspruch dazu steht die Erzählung [[Erzählung_XYZ]], die jedoch nur Status #perspektive hat."

## Ziel
Sicherstellung einer widerspruchsfreien Lore-Entwicklung und fachkundige Unterstützung bei komplexen Recherche-Fragen.
