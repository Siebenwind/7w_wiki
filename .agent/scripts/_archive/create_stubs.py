import os

names = [
    "Aelfrid_Wildgaden",
    "Gimbart_Galdora",
    "Gorion",
    "Hornstoß",
    "Knochenfürst",
    "Magister_ad_Sinister",
    "Markus",
    "Mehr'thak",
    "Nirluk",
    "Püppchen",
    "Szarmaduk",
    "Todward_von_Saalhorn"
]

target_dir = "/Users/alexandrerabe/siebenwind/7w_wiki/Siebenwind_Wiki/07_Persoenlichkeiten"

template = """---
layout: post
title: "{title}"
category: Personen
status: Stub
---

# {title}

> [!INFO]
> Dieser Artikel ist ein Stub. Er wurde automatisch aus dem Personenregister generiert.

**Zugehörigkeit:** Unbekannt
**Status:** Unbekannt

## Beschreibung
Bisher liegen keine detaillierten Informationen zu **{title}** vor.
"""

for name in names:
    title = name.replace("_", " ")
    filename = f"{name}.md"
    filepath = os.path.join(target_dir, filename)
    
    if os.path.exists(filepath):
        print(f"Skipping {filename}, already exists.")
        continue
        
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(template.format(title=title))
    print(f"Created {filename}")
