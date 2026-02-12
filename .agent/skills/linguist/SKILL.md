---
layout: wiki_page
name: Linguist (Analyse & Pflege)
description: Fähigkeit, falandrische Sprachen zu erkennen, zu interpretieren und die Datensätze zu pflegen.
---

# Linguist (Skill)

**Epistemischer Status:** #kanon

Dieser Skill stellt die linguistische Korrektheit im Wiki sicher und verwaltet die Sprach-Datensätze.

## Arbeitsweise

### 1. Erkennung & Interpretation
- Scannt Texte auf bekannte Marker (z.B. Apostrophe bei Isdira, Komposita bei Dwarschim, phonetische Verzerrungen bei Orkisch).
- Nutzt `translator.py`, um Bedeutungsebenen zu erschließen.
- **Kontext-Check:** Achtet auf Dialekte (z.B. Talzwergisch vs. Bergzwergisch).

### 2. Datenpflege (Feedback-Loop)
- Findet der Scanner unbekannte Begriffe in kanonischen Quellen?
    - **Aktion:** Vorschlag zur Erweiterung der entsprechenden JSON-Datei in `.agent/data/languages/`.
    - **Validierung:** Abgleich mit dem [Sprach-Kanon]([[Linguistik_Übersicht]]).

### 3. Wiki-Konforme Flaggung
Der Linguist weist jedem Sprachfragment den passenden Status zu:
- **#kanon:** Begriffe aus offiziellen Hintergrund-Dokumenten.
- **#bote:** Begriffe, die nur im [[Siebenwind_Bote]] auftauchen (könnten IC-Bezeichnungen sein).
- **#überlieferung:** Legendäre oder archaische Begriffe (z.B. Run).
- **#perspektive:** Volkstümliche Bezeichnungen oder Slang.

## Ziel
Ein konsistentes und lebendiges Sprachsystem, das automatisch mit neuen Entdeckungen wächst.
