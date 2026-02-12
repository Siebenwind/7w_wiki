---
layout: wiki_page
title: Projektdossier Siebenwind Chroniken
category: Sonstiges
---

# Projektdossier Siebenwind Chroniken

**Epistemischer Status:** #perspektive
**Status:** Projekt-Spezifikation für KI-Agenten
**Ziel:** Erstellung eines konsistenten, strukturierten Wikis auf Basis historischer und aktueller Daten.

## 1. Vision
Das Ziel ist die Überführung von über 20 Jahren gewachsener Rollenspiel-Geschichte in eine strukturierte Wissensdatenbank (Wiki). Die KI muss dabei nicht nur Texte zusammenfassen, sondern die **Kausalitäten** der Welt verstehen (z.B. Wie beeinflusst der Zorn eines Gottes das Klima oder die Politik einer Region?).

## 2. Die Quell-Architektur
Die Daten sind in drei logische Layer unterteilt:

*   **Layer 1: Das Fundament (Kanon):** Daten der Homepage (www.siebenwind.de). Diese enthalten die „Naturgesetze“ (Götter, Magiesystem, Zeitrechnung, Geografie). **Priorität: Absolut.**
*   **Layer 2: Die Chronik (Staff-Lore):** Offizielle Berichte, Bücher und Weltereignisse, die von Spielleitern verfasst wurden. **Priorität: Hoch.**
*   **Layer 3: Das Echo (Spieler-Lore):** Tagebücher, Geschichten und Berichte von Charakteren. Diese enthalten wertvolle Details, können aber subjektiv gefärbt sein. **Priorität: Interpretativ.**

## 3. Die „Siebenwind-Axiome“ (Kern-Regeln)
1.  **Göttliche Kausalität:** Magie ist kein Naturgesetz, sondern ein Geschenk oder Werkzeug der Götter.
2.  **Zeitrechnung:** Alles muss in den „Sonnenzirkel“ (Siebenwind-Kalender) eingeordnet werden.
3.  **Das Königreich:** Die zentrale politische Entität mit spezifischen Hierarchien und Rechtssystemen.
4.  **Low-Fantasy-Einschlag:** Trotz Magie und Göttern ist die Welt dreckig, gefährlich und menschlich-politisch motiviert.

# Projektdossier: Wissensdatenbank Siebenwind
**Zweck:** Migration und Konsolidierung von 20 Jahren Lore in ein strukturiertes Wiki.
**System-Umgebung:** Google Antigravity Agentic Workflow.

## 1. Daten-Hierarchie (Weighting)
Die Quellen im Verzeichnis `/Quellen/` werden nach folgender Priorität gewichtet:

1.  **Level 1 - Der Anker (Kanon):** 
    - URL: `www.siebenwind.de` (Hintergrund-Sektion)
    - Lokal: `/Quellen/Hintergrund/`
    - *Bedeutung:* Unumstößliche Wahrheit.

2.  **Level 2 - Die Chronik (Offizielles Wissen):**
    - Lokal: `/Quellen/Zeitung 7w Bote/`
    - *Bedeutung:* Zeitliche Abfolge der Weltereignisse.

3.  **Level 3 - Die Überlieferung (Gelehrtentum):**
    - Lokal: `/Quellen/Bibliothek Astrael/` und `/Quellen/Bibliothek Toran Dur/`
    - *Bedeutung:* Tiefgehende Lore, oft aus spezifischen kulturellen Blickwinkeln (z.B. menschlich vs. zwergisch).

4.  **Level 4 - Das Echo (Individuelle Lore):**
    - Lokal: `/Quellen/Spielergeschichten/`
    - *Bedeutung:* Details, Atmosphäre, persönliche Schicksale. Darf Kanon ergänzen, aber nicht verändern.

## 2. Die Siebenwind-Axiome (Kern-Logik)
Jeder Agent muss diese Logik bei der Erstellung des Wikis anwenden:
- **Zeitrechnung:** Basis ist der "Sonnenzirkel".
- **Magie:** Immer göttlichen oder dämonischen Ursprungs. Keine "technische" Magie ohne Entität im Hintergrund.
- **Geografie:** Das Königreich und die Inselwelt von Siebenwind sind das primäre Setting.

## 3. Ziel-Struktur der Wissensdatenbank
Jeder Output muss als valide Markdown-Datei (`.md`) erfolgen:
- **Dateiname:** `Kategorie_Name des Artikels.md`
- **Inhalt:** Frontmatter -> Einleitung -> Strukturierter Hauptteil -> Verlinkte Themen.