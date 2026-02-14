
import os
from pathlib import Path

names = [
    "Alashar", "Andaris_Maran", "Eleonore", "Erdur", "Eret",
    "Gero_von_Papin", "Hadhal", "K_endalor_Aothes", "Kaarem_Balta",
    "Maltus_Shuarshirad", "Narbenschnauze", "Plinius_Deseglieri",
    "Romualdo_Jakta", "Romualdo_Lavarin", "Samuel_der_Heiler",
    "T.", "Tantalla", "Willibald_Puckel"
]

base_path = Path("Siebenwind_Wiki/07_Persoenlichkeiten")

template = """---
layout: post
title: "{title}"
category: Personen
---

# {title}

**Epistemischer Status:** #perspektive

*Dieser Artikel ist ein Stub. Er wurde im Rahmen des Konsistenz-Audits automatisch angelegt.*

## Beschreibung
{name} ist eine Person, die im [[Personenregister]] verzeichnet ist.

## Quelle
[Unbekannt]
"""

for name in names:
    file_path = base_path / f"{name}.md"
    if not file_path.exists():
        title = name.replace("_", " ")
        content = template.format(title=title, name=title)
        file_path.write_text(content, encoding="utf-8")
        print(f"Created {file_path}")
    else:
        print(f"Skipped {file_path} (Exists)")
