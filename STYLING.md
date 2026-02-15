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

### 📂 Der `Siebenwind_Wiki` Ordner
- **Speicherort:** Wurzelverzeichnis (`/Siebenwind_Wiki/`).
- **Verwendung:** Alle internen Skripte, das Orakel (RAG) und der Wiki-Schmied greifen direkt auf diesen Pfad zu.
- **Wichtig:** Dieser Ordner darf nicht verschoben oder gelöscht werden.

### 🔗 Der Docs-Link
- **Pfad:** `docs/Siebenwind_Wiki` ist ein **Symbolischer Link** auf `../Siebenwind_Wiki`.
- **Zweck:** Ermöglicht MkDocs den Zugriff auf die Lore-Inhalte, während die Quelldateien für die Agenten im Wurzelverzeichnis verbleiben.
- **Gefahr:** Löschen des Originals bricht die gesamte Lore-Engine.

---

## III. Verlinkung & Rendering
- **Wikilinks:** Nutzung der Syntax `[[Seitenname]]`. Konfiguriert über die native Python-Markdown `wikilinks` Extension.
- **Relative Pfade:** Innerhalb von Markdown-Dateien für Bilder und Badges immer relative Pfade verwenden (z.B. `../assets/banner.png`).

---

## IV. Legal & Copyright (Standard)
Der Footer muss zwingend folgende Information enthalten:
`© 2026 LeCorbeau & Siebenwind Gemeinschaft | Inhalte: Autoren & Projekt Siebenwind`

*Hinweis: Der Code steht unter MIT (LeCorbeau), die Inhalte unter CC BY-NC-SA 4.0 (Gemeinschaft).*
