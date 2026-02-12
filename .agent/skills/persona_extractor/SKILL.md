---
layout: wiki_page
title: SKILL
category: Sonstiges
---

# SKILL

**Epistemischer Status:** #perspektive

This skill is designed to find, extract, and format NPC information from raw text, HTML, or Markdown files within the Siebenwind Wiki.

## Purpose
- Identify NPC names, titles (e.g., "Herzog", "Baron", "Erzgeweihter"), and affiliations.
- Extract biographical snippets and historical events associated with these personas.
- Generate standardized biography files in `07_Persoenlichkeiten/`.

## Commands
### `extract`
Scans a file or directory for NPC patterns and outputs a summary.

**Usage:**
`python3 extract_personas.py extract --path <path_to_file_or_dir>`

### `generate_bio`
Creates a biography markdown file. **MUST** follow the [Wiki Style Guide](file:///Users/alexandrerabe/siebenwind/7w_wiki/.agent/workflows/wiki_style_guide.md):
- YAML frontmatter with `layout: wiki_page`.
- H1 title matching the frontmatter `title`.
- Automatic links `[[...]]` for all related entities.

**Usage:**
`python3 extract_personas.py generate --name <persona_name> --source <source_file>`

## Logic & Patterns
The extractor looks for:
- Noble titles: König, Herzog, Fürst, Graf, Baron, Junker, Ritter, Freiherr, Edler.
- Clerical ranks: Geweihter, Erzgeweihter, Abt, Kaplan.
- Political roles: Kanzler, Patrizier, Kregor, Vogt, Richter.
- "ap" / "ahm" lineage markers.
- "von" / "zu" local markers.
