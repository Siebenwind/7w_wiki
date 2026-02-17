---
name: Art Director (Atelier)
description: Standardisierte Bildgenerierung mit Stil-Konsistenz und Metadaten-Tracking.
---

# Art Director (Skill)

**Epistemischer Status:** #experimentell
**Verantwortlichkeit:** Visual Identity & Assets

Dieser Skill steuert die Generierung von visuellen Artefakten für das Siebenwind Wiki. Er erzwingt die Einhaltung des definierten Art Styles und die lückenlose Dokumentation (Metadaten) jedes generierten Bildes.

## Kern-Prinzipien
1.  **Konsistenz:** Alle Bilder müssen einem definierten **Style Preset** folgen. Kein "Prompt-Chaos".
2.  **Referenzierung:** Jedes Bild benötigt eine permanente Metadaten-Spur (Sidecar-File).
3.  **Qualität:** Lieber 3x generieren und kuratieren, als Artifakte oder falsche Stile akzeptieren.

## Arbeitsweise

### 1. Style Presets
Aktuelle Ära: **"Archivum Argentum"** (Silverpoint / Renaissance Draft)

| Parameter | Wert |
| :--- | :--- |
| **Medium** | Silberstift, Graphit, feine Tusche-Linien (Rötel nur als Akzent) |
| **Untergrund** | Helles Papier, vellumartige Textur, ruhiger Archivhintergrund |
| **Stimmung** | Serioes, gelehrt, zurueckhaltend, andeutend statt ausgemalt |
| **Verbotene Elemente** | Fotorealismus, 3D-Render, Anime, Neon, harte UI-Grafik, Zahnräder/Mechanik (außer Dwarschim/Uhrmacher explizit) |
| **Erlaubte Elemente** | Leichte Spiegelschrift, anatomische Studien, topografische Linien, feine Kurven, Leerraum |

### 2. Generierungs-Prozess
Bei jeder `generate_image` Aktion MUSS gleichzeitig eine `.json` Metadaten-Datei angelegt werden.

**Namenskonvention:**
*   Bild: `assets/images/[Kategorie]/[Name]_[Timestamp].png`
*   Meta: `assets/images/[Kategorie]/[Name]_[Timestamp].json`

**Metadaten-Struktur (JSON):**
```json
{
  "asset_name": "siebenwind_banner_final",
  "timestamp": "ISO-8601",
  "style_preset": "Archivum Argentum",
  "prompt_used": "Full prompt text...",
  "parameters": {
    "aspect_ratio": "3:1",
    "model": "gemini-3-pro-image"
  },
  "context": "Wiki Homepage Header",
  "user_constraints": ["No Gears", "Magic Focus"]
}
```

### 3. Workflow
1.  **Anfrage analysieren:** Welches Subjekt? Welcher Kontext?
2.  **Prompt Engineering:** Wende das "Archivum Argentum" Preset an.
    *   *Prefix:* "Leonardo-inspired silverpoint drawing on archival paper..."
    *   *Suffix:* "...restrained linework, negative space, faint mirror writing."
3.  **Generierung:** Führe `generate_image` aus.
4.  **Validierung:** Prüfe das Ergebnis visuell (method hint, non-runtime: Editor/Browser-Host-Tooling). Passt der Stil?
5.  **Archivierung:** Speichere Bild + JSON.

## Zukunfts-Sicherheit
Sollte sich der Art Style ändern, wird lediglich der Abschnitt **1. Style Presets** in diesem Skill aktualisiert. Die Metadaten alter Bilder bleiben erhalten und dokumentieren ihre Epoche.
