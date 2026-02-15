# Styling-Profil & Portabilität

Dieses Wiki nutzt ein zweistufiges Styling:

1. `assets/themes/base.css`
   - Portabler Kern (Farbtokens, Typografie, Tabellen, Banner)
   - Ohne Abhängigkeit von `.md-*` Klassen
2. `assets/themes/material.css`
   - Optionales Profil für MkDocs Material / GitHub Pages
   - Enthält nur `md-*`-spezifische Overrides

## Umschalten auf anderes Wiki-Layout

In `mkdocs.yml` unter `extra_css`:

- Für maximale Portabilität: nur `assets/themes/base.css` laden.
- Für MkDocs Material: zusätzlich `assets/themes/material.css` laden.

## Designrichtung

- Leichter Rötel-Look
- Subtile Ornamente statt schwerer Flächen
- Fokus auf Lesbarkeit und langfristige Wartbarkeit
