---
description: Siebenwind Wiki Style Guide & Convention
---

# [Display Title]

**Epistemischer Status:** #perspektive

To ensure portability, consistency, and a high narrative standard across the Siebenwind Chronicles, all wiki entries must follow this strict structure. We aim for **"Roman-Qualität" (Novel Quality)**—entries should be immersive, providing context on motivations, surroundings, and social atmosphere.

## 1. YAML Frontmatter
Every file must start with a YAML frontmatter block containing exactly these fields:

```yaml
---
layout: wiki_page
title: [Display Title]
category: [Persönlichkeit | Geschichte | Erzählung | Geografie | Religion | Magie]
uuid: [UUID-v4]
quelle: ../../Quellen/[Unterordner]/[Dateiname].md
letzter_check: [ISO-8601 Zeitstempel inkl. Uhrzeit]
---
```

## 2. Heading Structure
- **H1 Header:** The first line after the frontmatter must be a Level 1 Heading (`# Title`) matching the `title` field in the YAML.
- **H2 Headers:** Use for main sections (e.g., `## Beschreibung`, `## Wirken`, `## Quellen`).

## 3. Metadata Section (Optional but recommended for NPCs)
Directly under the H1, include key-value pairs for quick scanning:
- **Titel:** [Official Title]
- **Epistemischer Status:** [#canon | #bote | #perspektive | #überlieferung]
- **Zugehörigkeit:** [Faction/Family]
- **Zeitraum:** [Active Period in n.H.]

## 3.1 Epistemisches System (Verlässlichkeitsränge)

Die vier epistemischen Tags definieren die **Verlässlichkeit** einer Information.
**Höherer Rang überschreibt niedrigeren Rang bei Widersprüchen.**

| Rang | Tag | Quellordner | Bedeutung | Vertrauen |
|---|---|---|---|---|
| 🥇 1 | `#canon` | `/Hintergrund/` | Offizieller Kanon, Spielleiter-Festlegung | Absolut |
| 🥈 2 | `#bote` | `/Zeitung 7w Bote/` | Redaktionelle Berichterstattung (In-World) | Hoch |
| 🥉 3 | `#überlieferung` | `/Bibliothek/` | In-World-Literatur, Mythen, Legenden | Mittel |
| 4 | `#perspektive` | `/Spielergeschichten/` | Subjektive Erzählung, Hörensagen | Gering |

### Entscheidungsregeln
1. **Widerspruch `#canon` vs. `#bote`:** `#canon` gewinnt immer.
2. **Widerspruch `#bote` vs. `#perspektive`:** `#bote` gewinnt. Die Spielergeschichte wird ergänzend notiert, nicht als Fakt übernommen.
3. **Neue Fakten nur aus `#perspektive`:** Dürfen ins Wiki, wenn sie dem Kanon nicht widersprechen. Müssen als `#perspektive` getaggt bleiben.

### Zusätzliche Meta-Tags (KEINE Verlässlichkeitsränge)
- `#meta` — Register, Index-Dateien, Übersichtsseiten (aggregieren Wissen, sind selbst keine Quellen)
- `#gemischt` — Artikel mit Informationen aus mehreren Verlässlichkeitsrängen (z.B. Kanon-Basis + Boten-Details)


## 4. Standardized Headers per Category
To maintain consistency, use these dedicated headers:
### Bestiarium (Creatures)
- `## Überblick` (Description & Type)
- `## Biologie` (Anatomy & Senses)
- `## Verhalten` (Habitat & Social patterns)

### Gesellschaft (Guilds/Craft)
- `## Sitz` (Location)
- `## Führung` (Master/Board)
- `## Aufgaben & Ziele` (Main trade or objective)

### Geschichte (Events)
- `## Hintergrund` (Cause)
- `## Verlauf` (The Event)
- `## Folgen` (Impact on the world)

## 5. Narrative Content (Roman-Qualität)
Don't just list facts. Describe:
- **Atmosphere:** The smell of the forge, the cold of the North, the tension in a city.
- **Motivations:** Why does an NPC act? What are their fears and goals?
- **Social Context:** How is a person viewed by their peers? What is the social status of a region?

## 4. Internal Linking
- Use standard Wiki-brackets: `[[Page_Name]]`.
- For external or source links, use absolute paths: `[Label](file:///absolute/path/to/source.html)`.

## 5. Directory Mapping
- `00_Fundament/`: Core laws and axioms.
- `01_Pantheon/`: Gods and religion.
- `02_Geografie/`: Regions and cities.
- `03_Gesellschaft/`: Guilds, nobility, and races.
- `04_Chronik/`: Timelines (n.H.).
- `05_Geschichte/`: Major historical events and epochs.
- `07_Persoenlichkeiten/`: NPC biographies.
- `08_Bestiarium/`: Creatures and monsters.
- `09_Bibliothek/`: Processed books and literature.
- `10_Archiv/`: Official decrees and law.
