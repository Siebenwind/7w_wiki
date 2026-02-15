# DELEGATION ORDER: GITHUB PAGES STYLING & WIKILINK REPAIR

Du wirst als **Interim-Gestalter (Styling Agent)** für das Siebenwind Wiki Projekt eingesetzt. Deine Mission ist die technische und ästhetische Aufwertung der GitHub Pages Repräsentation unter Wahrung der "Sanguine-Ingenieurs-Ästhetik".

## 🏰 Projekt-Vison
Wir restaurieren das digitale Gedächtnis von Falandrien. Das Wiki nutzt **MkDocs (Material Theme)** und soll wie ein technisches Manuskript der Renaissance wirken (Rötel-Zeichnungen auf Pergament).

## 🎯 Deine Missionsziele

### 1. Wikilink Repair (Prio 1)
Aktuell werden im Wiki Begriffe in doppelten Klammern (z.B. `[[Toran_Dur]]`) zwar als Text, aber **nicht als klickbare Links** gerendert.
- **Problem**: Die aktuelle `wikilinks` Extension in `mkdocs.yml` scheint nicht korrekt zu greifen oder mit der Ordnerhierarchie (`Siebenwind_Wiki/XX_Kategorie/...`) nicht klarzukommen.
- **Auftrag**: Repariere die Link-Logik. Überprüfe die `mkdocs.yml` und installiere/konfiguriere ggf. ein robusteres Plugin (z.B. `mkdocs-roamlinks-plugin`), damit alle `[[WikiLinks]]` auf die korrekten .md Dateien verweisen.

### 2. Visuelle Aufwertung (Layout & Banner)
Das Layout ist funktional, aber noch zu "nackt".
- **Banner**: Erneure den Banner (`docs/assets/banner.png`). Er soll das "Modern Scholar" Aesthetic widerspiegeln: Leonardo-inspirierte Skizzen, technisches Diagramm-Feeling, Rötel auf Beige.
- **Logo**: Optimiere das Logo (`docs/assets/logo.png`) für die Header-Anzeige.
- **Layout/CSS**: Verfeinere die `docs/assets/custom.css`.
    - Nutze subtile Micro-Animationen (Hovers).
    - Implementiere ein "Glassmorphism" Feeling für Sidebars oder Nav-Elemente (dezent!).
    - Optimiere das Font-Rendering (nutze ggf. Google Fonts wie *Inter* oder *Outfit* in Kombination mit einer Serif-Schrift für Content).

## 🛠️ Technische Rahmenbedingungen
- **Repository-Struktur**:
    - `docs/`: Alle Inhalte für MkDocs.
    - `mkdocs.yml`: Zentrale Konfiguration.
    - `docs/assets/`: CSS, Bilder, Fonts.
- **Einschränkungen**: Ändere niemals den Content der `.md` Dateien (außer zur Link-Korrektur, falls nötig), sondern konzentriere dich auf die Darstellung.

## 📜 Abgabe & Verifikation
- Dokumentiere deine Änderungen in einer `STYLING_STABILITY_REPORT.md` im System-Ordner.
- Führe nach Abschluss einen lokalen Build-Test durch (falls möglich) oder verifiziere die HTML-Struktur der generierten Links.

**Bist du bereit für den Golden Polish, Archivar?**
