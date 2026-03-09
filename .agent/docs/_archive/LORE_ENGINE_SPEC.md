# 📜 Spezifikation: Siebenwind Lore Engine v2.1

## 1. Philosophie & Vision
Die **Siebenwind Lore Engine** ist ein standardisiertes Framework zur Verwaltung komplexer Rollenspiel-Lores. Sie ist darauf ausgelegt, als **Wissens-Layer** zwischen rohen Quelldaten (Logs, Wikis, Geschichten) und intelligenten Agenten (LLMs, CLIs) zu fungieren.

### Kernprinzipien:
*   **AI-Agnostizität**: Die Engine ist unabhängig von spezifischen KI-Anbietern. Sie nutzt Standard-Markdown und Python-Tools.
*   **Epistemische Integrität**: Jede Information hat einen Wahrheitsrang (#canon bis #perspektive).
*   **Maschinenlesbarkeit**: Durch das `lore_manifest.json` können KIs das Projekt ohne menschliche Hilfe "onboarden".

## 2. Architektur (The Three-Tier System)

### I. Data Layer (`/Siebenwind_Wiki/`)
*   **Format**: GFM (GitHub Flavored Markdown).
*   **Metadata**: Strukturierte YAML-Frontmatter mit UUIDs und Status-Tags.
*   **Linking**: Ausschließlich relative WikiLinks `[[Page]]`.

### II. Intelligence Layer (`/.agent/`)
*   **Skills**: Modulare Python-Tools (z.B. Orakel für RAG).
*   **Workflows**: Definierte Prozessbeschreibungen im Markdown-Format.
*   **Prompts**: Persona-Definitionen (Oberarchivar), die das Verhalten der KI steuern.

### III. Interface Layer (`/7w.py`)
*   Ein vereinheitlichter Entry-Point (CLI Wrapper), der die technische Komplexität abstrahiert.
*   Unterstützt standardisierte Befehlssätze für Suche, Statistiken und Wartung.

## 3. CLI Spezifikation (`7w.py`)
Die Schnittstelle folgt dem Muster `./7w.py [command] [options]`.

| Command | Zielsetzung | Tool-Referenz |
| :--- | :--- | :--- |
| `search` | Semantische Recherche | `oracle/search.py` |
| `stats` | KPI & Dashboarding | `scripts/generate_wiki_stats.py` |
| `audit` | Konsistenzprüfung | `scripts/register_check.py` |
| `index` | Vektor-Management | `oracle/build_index.py` |
| `repair` | Automatisierte Korrektur | `scripts/repair.py` |

## 4. Integration mit externen Systemen
Die Engine kann via `lore_manifest.json` gekoppelt werden. Externe KIs (z.B. Google Gemini CLI) nutzen das Manifest, um Pfade und Fähigkeiten zu lokalisieren.

### Beispiel-Koppelung:
```json
{
  "interface": {
    "cli": "./7w.py",
    "commands": ["search", "stats"]
  }
}
```

## 5. Wartung & Evolution
Das System ist selbst-reinigernd durch Audits und Repair-Workflows. Änderungen an der Lore werden im `CHANGELOG.md` und in den `Wiki Statistiken` reflektiert.

---
*Status: Finalisiert & Gesichert | Stand: 13.02.2026*
