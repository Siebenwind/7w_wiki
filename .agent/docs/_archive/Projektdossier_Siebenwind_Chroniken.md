# Projektdossier: Siebenwind Lore Engine v2.1

**Epistemischer Status:** #canon
**Status:** Primäre Projekt-Spezifikation (v2.1)
**Ziel:** Transformation von 20 Jahren Rollenspiel-Geschichte in eine standardisierte, KI-gesteuerte Lore-Intelligence-Plattform.

---

## 1. Vision & Leitbild
Die **Siebenwind Lore Engine** ist mehr als ein Wiki. Sie ist ein intelligentes Ökosystem, das historische Kausalitäten, göttliche Einflüsse und subjektive Überlieferungen in ein kohärentes Ganzes verwebt. 

Das Ziel ist die Erstellung einer **"Single Source of Truth"**, die sowohl für menschliche Leser (MkDocs) als auch für künstliche Agenten (LLMs via CLI/API) als ultimative Referenz für die Welt von Siebenwind dient.

---

## 2. Das Epistemische System (Die 4 Säulen der Wahrheit)
Wir sind von starren Quell-Leveln zu einem dynamischen Wahrheitsmodell übergegangen:

1.  **🔴 #canon (Das Fundament):** Unumstößliche Weltgesetze, geografische Axiome und göttliche Ordnung. (Quelle: `/Hintergrund`)
2.  **🟡 #bote (Die Chronik):** Zeitgeschichtliche Berichte des "Siebenwind Boten". Faktisch korrekt im Kontext ihrer Zeit. (Quelle: `/7w Bote`)
3.  **🔵 #perspektive (Das Echo):** Spielerberichte, Briefe, Biografien. Subjektiv, atmosphärisch, potenziell widersprüchlich. (Quelle: `/Spielergeschichten`)
4.  **⚪ #überlieferung (Der Mythos):** Legenden, archaische Sagen und volkstümliches Wissen. (Quelle: `## Überlieferungen` Sektionen)

---

## 3. Die Intelligenz-Architektur
Das Projekt ist in drei funktionale Schichten unterteilt:

- **Layer 1: Das Archiv (Markdown)**: Hochstandardisierte Dateien mit striktem YAML-Frontmatter und relativer Verlinkung.
- **Layer 2: Das Gehirn (Intelligence Layer)**: Modulare KI-Skills (Orakel/RAG, Linguist, Wiki-Schmied) und automatisierte Workflows.
- **Layer 3: Das Interface (Unified CLI)**: Die Schnittstelle `7w.py`, die menschlichen Nutzern und externen KIs (z.B. Gemini CLI) Zugriff auf die Lore ermöglicht.

---

## 4. Die Siebenwind-Axiome (Core Logic)
Jede Ingestion und jeder Wiki-Artikel muss diese Axiome respektieren:
1.  **Göttlicher Ursprung:** Magie und Wunder sind keine autonomen Kräfte. Sie entspringen den Göttern oder Dämonen.
2.  **Temporal-Präzision:** Ereignisse werden im "Sonnenzirkel" (n.H. - nach Gründung Helighenstadts) datiert.
3.  **Narrative Tiefe:** Artikel streben "Roman-Qualität" an. Fakten werden narrativ eingebettet, ohne die Übersichtlichkeit zu opfern.

---

## 5. Standardisierung & Wartung
Das Projekt nutzt automatisierte **Audit-Loops** (`/audit`, `/repair`), um:
- Duplikate in Registern zu verhindern.
- Verwaiste Profile (Orphans) zu erkennen und zu heilen.
- Die Konsistenz zwischen verschiedenen epistemischen Ebenen zu wahren.

---
*Zuletzt aktualisiert: 13.02.2026 durch Antigravity (Archivar & System-Architekt)*