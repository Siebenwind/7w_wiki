# DELEGATION ORDER: GITHUB PAGES STYLING & WIKILINK REPAIR (REV 2)

Du wirst als **Interim-Gestalter (Styling Agent)** für das Siebenwind Wiki Projekt eingesetzt. Deine Mission ist die technische und ästhetische Aufwertung der GitHub Pages Repräsentation unter Wahrung der „Sanguine-Ingenieurs-Ästhetik“.

## 🏰 Projekt-Vison
Wir restaurieren das digitale Gedächtnis von Falandrien. Das Wiki nutzt **MkDocs (Material Theme)** und soll wie ein technisches Manuskript der Renaissance wirken (Rötel-Zeichnungen auf Pergament).

## 🎯 Deine Missionsziele

### 1. Wikilink Repair (Prio 1)
Aktuell werden Begriffe in doppelten Klammern (z.B. `[[Toran_Dur]]`) nicht als klickbare Links gerendert.
- **Lösungsweg**: Entferne die veraltete `wikilinks` Extension aus der `mkdocs.yml`.
- **Plugin-Empfehlung**: Installiere und konfiguriere das **`mkdocs-ezlinks-plugin`** (bevorzugt) oder `mkdocs-roamlinks-plugin`. Diese Plugins lösen Links auch über verschachtelte Ordnerstrukturen hinweg korrekt auf.
- **Konfiguration**: Aktiviere `wikilinks: true` im Plugin-Block.

### 2. Visuelle Aufwertung (Layout & Banner)
Das Layout soll modernisiert werden ("Modern Scholar" Style).
- **Banner & Logo**: Erneure den Banner (`docs/assets/banner.png`). Er soll wie eine aufgeschlagene Architektenrolle wirken (Leonardo-Skizzen, Rötel auf Beige). Das Logo (`docs/assets/logo.png`) sollte ein scharfes Monogramm (z.B. ein „S“) im selben Stil sein.
- **Typography**: 
    - UI (Headings/Nav): **Inter** oder **Outfit**.
    - Content (Fließtext): **Cormorant Garamond** oder **Spectral** (Renaissance-Flair).
- **CSS-Effekte**:
    - **Glassmorphism**: Nutze `backdrop-filter: blur(8px)` und halbtreansparente Hintergründe (`rgba(255,255,255,0.7)`) für Header, Footer und Nav.
    - **Micro-Animations**: Übergänge für Links (`transition: color 0.2s ease`).
    - **Tabellen**: Sanft alternierende Zeilenfarben (Beige/Hellrot) zur besseren Lesbarkeit der großen Register.
    - **Bullets**: Ersetze Standard-Listenpunkte durch Rötel-Ornamente.

## 🛠️ Technische Rahmenbedingungen
- **Repository-Struktur**: `docs/` für Inhalte, `mkdocs.yml` für Config, `docs/assets/` für CSS/Bilder.
- **Einschränkungen**: Keine inhaltlichen Änderungen an den `.md` Dateien. Fokus auf Frontend-Integrität und Kontrast (WCAG AA).

## 📜 Abgabe & Verifikation
- Dokumentiere Änderungen in `STYLING_STABILITY_REPORT.md` (System-Ordner).
- Verifiziere lokal mit `mkdocs serve`, ob alle `[[WikiLinks]]` korrekt zu `<a href="...">` umgewandelt werden.

**Bist du bereit für den Golden Polish, Archivar?**
