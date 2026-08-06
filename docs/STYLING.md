# Styling-Profil & Portabilität

`docs/assets/custom.css` ist der einzige in `mkdocs.yml` geladene Einstiegspunkt. Er importiert die beiden Schichten in fester Reihenfolge und enthaelt anschliessend die komponentenspezifischen Regeln der Archivoberflaeche:

1. `docs/assets/themes/base.css`
   - Portabler Kern (Farbtokens, Typografie, Tabellen, Banner)
   - Ohne Abhängigkeit von `.md-*` Klassen
2. `docs/assets/themes/material.css`
   - Optionales Profil für MkDocs Material / GitHub Pages
   - Enthält nur `md-*`-spezifische Overrides

3. `docs/assets/custom.css`
   - Kanonischer Bundle-Einstieg fuer MkDocs
   - Startseite, Aktivitaetskarten und mobile Korrekturen

## Umschalten auf anderes Wiki-Layout

In `mkdocs.yml` bleibt nur `assets/custom.css` eingetragen. Fuer ein anderes Wiki-Layout werden dessen Imports angepasst; so kann keine der drei aktiven CSS-Schichten versehentlich aus der publizierten Seite fallen.

Asset-Regel:
- `docs/assets/` ist die Live-Asset-Surface fuer publizierte Artefakte und production-only.
- `System/Design_Assets/` ist historischer bzw. quellseitiger Design-Bestand.

## Designrichtung

- Serioeser Archiv-Look mit Silberstift-Linien und sparsamen Roetel-Akzenten
- Subtile Ornamente statt schwerer Flaechen
- Fokus auf Lesbarkeit, Orientierung und langfristige Wartbarkeit

## Mobile Mindestregeln

- Die Startseite zeigt nach dem kompakten Hero unmittelbar `Was geschieht?`.
- Kartenraster werden auf schmalen Ansichten einspaltig.
- Tabellen und Mermaid-Diagramme bleiben im Inhaltsbereich und erhalten bei Bedarf einen horizontalen Scrollbereich.
- Primaere Bedienelemente bieten mindestens 44 Pixel Beruehrungshoehe.
