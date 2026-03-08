# Siebenwind Styling & Architektur-Profil

Dieses Dokument dient als verbindlicher Standard für das visuelle Design und die strukturelle Organisation der Siebenwind Lore-Engine.

## I. Visuelles Leitbild: "Modern Scholar / Minimalist Tool"

Das Wiki ist ein **Spezialisten-Werkzeug**, keine immersive Rollenspieldarstellung. Jegliche ästhetische Entscheidung muss der Lesbarkeit und Funktionalität untergeordnet sein.

### 🎨 Farbpalette (Rötel & Beige)
- **Hintergrund:** `#f5f2e9` (Warmes Beige / Pergament-Ton)
- **Akzente:** `#722f37` (Tiefes Rötel-Rot)
- **Textfarbe:** `#2c2420` (Dunkles Braun/Schwarz für hohen Kontrast)
- **Header:** Reinweiß (`#ffffff`) mit dunkelroter Unterstreichung für klare Abgrenzung.

### ✍️ Tonalität (Nüchtern & Sachlich)
- **Kein "Flavor Text":** Vermeidung von dramatischen Zitaten, immersiven Einleitungen oder werblichen Formulierungen ("Abgrundtief", "Gewaltiges Erbe").
- **Technischer Fokus:** Sachliche Beschreibung von System-Komponenten (Legislative, Judikative, Exekutive).
- **Referenz:** Siehe [System-Architektur](docs/architecture.md).

---

## II. Dateistruktur & Abhängigkeiten

### 📂 Kanonische Verzeichnisse

| Verzeichnis | Zweck | Git-tracked? |
|---|---|---|
| `docs/Siebenwind_Wiki/` | **Single Source of Truth** für alle Wiki-Inhalte. Wird von mkdocs direkt als Content-Quelle verwendet. | ✅ Ja |
| `Quellen/` | Rohquellen (Boten, Spielergeschichten, Bibliothek). Wird per CI in `docs/Quellen/` kopiert. | ✅ Ja |
| `docs/` | mkdocs `docs_dir` — enthält Wiki, Quellen-Kopie, Archiv und Meta-Seiten. | ✅ Ja |

> **Historischer Hinweis (2026-03):** Bis Phase B der Projektreinigung existierte ein zweites `Siebenwind_Wiki/` im Wurzelverzeichnis. Die ursprüngliche Architektur nutzte Symlinks (`docs/Siebenwind_Wiki → ../Siebenwind_Wiki`), was aber mit mkdocs inkompatibel war (mkdocs folgt keinen Directory-Symlinks). `docs/Siebenwind_Wiki/` ist nun der einzige, kanonische Speicherort.

### 🔄 CI/CD-Pipeline (`deploy.yml`)
- **Quellen-Sync:** `Quellen/` wird vor jedem Build physisch nach `docs/Quellen/` kopiert, da die Quellen außerhalb von `docs/` gepflegt werden.
- **Wiki-Inhalte:** Direkt in `docs/Siebenwind_Wiki/` editiert — kein Sync nötig.
- **Symlinks:** `CHANGELOG.md`, `LICENSE.md` und `MASTER_TASK_LIST.md` in `docs/` sind Datei-Symlinks auf ihre Pendants im Wurzelverzeichnis. Git und mkdocs unterstützen Datei-Symlinks korrekt.

### 📜 Skript-Verzeichnis
Alle Skripte liegen in `.agent/scripts/`. Das Wurzelverzeichnis enthält nur die CLI-Hauptdatei `7w_wiki.py`.

---

### III. Verlinkung & Rendering
- **Wikilinks:** Nutzung der Syntax `[[Seitenname]]`. Technisch realisiert über das `mkdocs-roamlinks-plugin`, das relative Links über alle Unterverzeichnisse hinweg auflöst.
- **Relative Pfade:** Innerhalb von Markdown-Dateien für Bilder und statische Assets immer relative Pfade verwenden (z.B. `../assets/banner.png`).

---

---

## V. Epistemik-Visualisierung (Status-Header)
Jeder Wiki-Artikel muss mit einem standardisierten Status-Header beginnen, der die Verlässlichkeit der Information (Epistemik) sofort klärt.

- **Syntax:** `!!! note "Status: [Typ]"`
- **Typen:** `#canon` (Zentral), `#bote` (Zeitgeschehen), `#perspektive` (Subjektiv), `#überlieferung` (Vage), `#fanon` (Nicht-Kanon/Legacy).

Beispiel:
```markdown
!!! note "Status: #canon"
    Diese Information entspricht dem offiziellen Kern-Kanon von Siebenwind.
```

---

## VI. Visualisierung & Komplexe Daten
- **Stammbäume:** Nutzung von Mermaid-Syntax (`graph TD`) für familiäre Verhältnisse.
- **Galerien:** Nutzung von Markdown-Carousels für Artworks und Skizzen.
- **Dossiers:** Wissenschaftliche Berichte nutzen das `[!ABSTRACT]` Tag für Zusammenfassungen.

---

## VII. Legal & Copyright (Standard)
Der Footer muss zwingend folgende Information enthalten:
`© 2026 LeCorbeau & Siebenwind Gemeinschaft | Inhalte: Autoren & Projekt Siebenwind`

*Hinweis: Der Code steht unter MIT (LeCorbeau), die Inhalte unter CC BY-NC-SA 4.0 (Gemeinschaft).*

---
*Zuletzt aktualisiert: 15.02.2026 durch Antigravity (Standard v2.8)*
