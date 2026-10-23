# Agenten-Dossier: Banner-Produktion (Archivum Argentum)

## Auftrag

Erstelle neue Hero-Banner fuer die Landing-Page des Siebenwind-Wikis.
Die Banner muessen den Leserfokus (85%) staerken und inhaltlich korrekt auf konkrete Story-Anker verweisen.

## Verbindliche Zielsetzung

- Oeffentliche Wirkung: serioeses, kuratiertes Archiv.
- Ton: ruhig, glaubwuerdig, dokumentarisch.
- Ergebnis: Banner, die Geschichte andeuten statt illustrativ ueberladen.
- Pflicht: Motiv und verlinkter Artikel muessen inhaltlich zusammenpassen.

## Kanonische Story-Anker (Featured)

### Motiv A: Archivflur ohne Figuren
- Zielartikel: `Siebenwind_Wiki/09_Bibliothek/Nachts_im_Brandensteiner_Tempel/`
- Kanonischer Kern:
  - naechtliches Schutzritual im Schrein zu Brandenstein
  - alternder Morsan-Geweihter
  - Vorbereitung auf das Dunkeltief
  - Ritualspuren/Siegel, sakrale Ernsthaftigkeit

### Motiv B: Chroniktafeln im Nebel
- Zielartikel: `Siebenwind_Wiki/04_Chronik/Zeitleiste_(15-30_n.H.)/`
- Kanonischer Kern:
  - dokumentierter Botenzeitraum 120-193
  - politische Umbrueche und Konfliktlagen
  - Chronik als vernetztes Zeitdokument, nicht als Szenenbild

## Stilvorgabe (Pflicht)

- Preset: `Archivum Argentum`
- Medium: Silberstift/Graphit, feine Linien, sparsame Roetel-Akzente
- Look: archivisch, reduziert, ruhig, serioes
- Komposition: viel Negativraum fuer Headline + CTA

## Harte Ausschlusskriterien (No-Gos)

- Keine Figuren als Hauptmotiv (insbesondere keine zentralen Personenportraets)
- Keine Gear-/Mechanikmotive (ausser expliziter Dwarschim/Uhrmacher-Auftrag)
- Kein Fantasy-Poster-Look, kein Cinematic-Fotorealismus
- Keine Motivik ohne eindeutigen Bezug zum jeweiligen Zielartikel

## Produktionsumfang

- 2 finale Motive:
  - A: Archivflur ohne Figuren
  - B: Chroniktafeln im Nebel
- Je Motiv mindestens 2 Varianten (insgesamt mind. 4 Entwuerfe)
- Format: 3:1 (Hero-Banner)

## Technische Lieferform

- Bilddatei plus Sidecar-JSON gemaess Art-Director-Skill
- JSON muss enthalten:
  - `asset_name`
  - `style_preset`
  - `prompt_used`
  - `parameters.aspect_ratio`
  - `story_anchor.title`
  - `story_anchor.link`
  - `copy_hint.headline/subline/cta`

## Qualitaetspruefung (Abnahmecheck)

1. Story-Fit:
   - Kann das Motiv glaubwuerdig als visuelle Einleitung des Zielartikels gelesen werden?
2. Lesbarkeit:
   - Ist ausreichend ruhige Flaeche fuer UI-Text vorhanden?
3. Stil-Fit:
   - Archivum-Argentum-Ton getroffen?
4. Verbotenes:
   - Keine Figurenfalle, keine Gear-Falle, keine ueberspitzte Effektdichte.

## Bereits vorbereitete Prompt-Briefs

Nutze diese Dateien als Startpunkt:

- `docs/assets/design_proposals/siebenwind_banner_archivflur_brandenstein_v2.json`
- `docs/assets/design_proposals/siebenwind_banner_archivflur_brandenstein_v2_alt.json`
- `docs/assets/design_proposals/siebenwind_banner_chroniknebel_zeitleiste_v2.json`
- `docs/assets/design_proposals/siebenwind_banner_chroniknebel_zeitleiste_v2_alt.json`

## Ehrliche Risiken

- Vorhandene Altbanners sind teilweise stilfremd (Figuren/Gears/zu illustrativ).
- Ohne strikte Story-Pruefung droht Motiv-Text-Mismatch.
- Deshalb: vor Finalisierung je Motiv ein 3-Zeilen-Story-Abgleich gegen den Zielartikel dokumentieren.

## Erwartetes Ergebnis fuer die Freigabe

- Eine klare Empfehlung: welches Motiv als aktueller Hero live geht.
- Das zweite Motiv als naechste Rotation.
- Kurze Begruendung (Story-Fit, Lesbarkeit, Markenfit).
