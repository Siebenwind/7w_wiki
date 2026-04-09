# Styling-Profil & Portabilität

Dieses Wiki nutzt ein zweistufiges Styling:

1. `docs/assets/themes/base.css`
   - Portabler Kern (Farbtokens, Typografie, Tabellen, Banner)
   - Ohne Abhängigkeit von `.md-*` Klassen
2. `docs/assets/themes/material.css`
   - Optionales Profil für MkDocs Material / GitHub Pages
   - Enthält nur `md-*`-spezifische Overrides

## Umschalten auf anderes Wiki-Layout

In `mkdocs.yml` unter `extra_css`:

- Für maximale Portabilität: nur `assets/themes/base.css` laden.
- Für MkDocs Material: zusätzlich `assets/themes/material.css` laden.

Asset-Regel:
- `docs/assets/` ist die Live-Asset-Surface fuer publizierte Artefakte.
- `System/Design_Assets/` ist historischer bzw. quellseitiger Design-Bestand.

## Designrichtung

- Serioeser Archiv-Look mit Silberstift-Linien und sparsamen Roetel-Akzenten
- Subtile Ornamente statt schwerer Flaechen
- Fokus auf Lesbarkeit, Orientierung und langfristige Wartbarkeit
