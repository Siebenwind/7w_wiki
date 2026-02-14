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
Aktuelle Ära: **"Codex Atlanticus"** (High Renaissance / Da Vinci)

| Parameter | Wert |
| :--- | :--- |
| **Medium** | Rötelzeichnung (Red Chalk), Sepia-Tusche, Silberstift |
| **Untergrund** | Altes Pergament, texturiertes Papier (Vellum) |
| **Stimmung** | Akademisch, mystisch, "Unvollendetes Meisterwerk" |
| **Verbotene Elemente** | Fotorealismus, 3D-Render, Anime, Moderne Schriftarten, Neon (außer Magie), Steampunk-Zahnräder (außer explizit gefordert) |
| **Erlaubte Elemente** | Spiegelschrift, anatomische Studien, geometrische Hilfslinien, Ley-Linien, Runenkreise |

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
  "style_preset": "Codex Atlanticus",
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
2.  **Prompt Engineering:** Wende das "Codex Atlanticus" Preset an.
    *   *Prefix:* "Leonardo da Vinci style red chalk sketch on parchment..."
    *   *Suffix:* "...detailed, masterpiece, faint mirror writing."
3.  **Generierung:** Führe `generate_image` aus.
4.  **Validierung:** Prüfe das Ergebnis visuell (via `view_file` oder Browser). Passt der Stil?
5.  **Archivierung:** Speichere Bild + JSON.

## Zukunfts-Sicherheit
Sollte sich der Art Style ändern (z.B. zu "Oil Painting" oder "Pixel Art"), wird lediglich der Abschnitt **1. Style Presets** in diesem Skill aktualisiert. Die Metadaten alter Bilder bleiben erhalten und dokumentieren ihre Epoche.
