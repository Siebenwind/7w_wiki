---
title: MkDocs Warnungsabbau - Vorgehensdokumentation
date: 2026-02-15
status: done
uuid: 0ecf0f91-8d35-45b9-9c17-a43b61f73ff5
owner: Netz-Waechter
---

# Ziel

Reduktion der MkDocs-Build-Warnungen ohne inhaltliche Kanon-Aenderung.

# Vorgehen (Waypoints)

## Waypoint 0 - Baseline messen

- Build ausgefuehrt: `.venv/bin/mkdocs build -f mkdocs.yml`
- Ergebnis:
  - `TOTAL_WARN = 181`
  - `LINK_WARN = 179`
  - `MISSING_TARGET_WARN = 178`

## Waypoint 1 - Dokumentations-Sicht auf Quellen vervollstaendigen

- Problem: Viele Links zielten auf `Quellen/...`, aber `docs/` hatte keinen Zugriffspfad.
- Massnahme:
  - Symlink `docs/Quellen -> ../Quellen`
  - Symlink `docs/Hintergrund -> ../Quellen/Hintergrund`
- Ergebnis nach Rebuild:
  - `TOTAL_WARN = 50`
  - `LINK_WARN = 48`
  - `MISSING_TARGET_WARN = 47`

## Waypoint 2 - Restwarnungen clustern

- Restgruppen identifiziert:
  - Fehlende historische Bote-Dateien: `Siebenwind Bote 176/178/179/180/181/182/185/118`
  - Einzelpfad-Drift: `Hintergrund/Kanon.md`, `Quellen/Hintergrund/Khalandra.md`
  - Dateinamen-Drift: `Aus dem Leben eines Schwarzmagiers.md` vs. `Aus_dem_Leben_eines_Schwarzmagiers.md`
  - Altformat-Link: `Die Sprache Run.html` vs. vorhandene `.md`
  - Interne Relativpfade aus `Siebenwind_Wiki/index.md` auf Root-Dokumente

## Waypoint 3 - Gezielte Kompatibilitaetsaliases

- Prinzip: vorhandene Inhalte nicht umschreiben, stattdessen kompatible Alias-Dateien/Symlinks an den erwarteten Zielpfaden bereitstellen.
- Umgesetzt:
  - `docs/Quellen`, `docs/Hintergrund` als Sichtpfade fuer Dokumentation
  - Aliasziele fuer fehlende Bote-Verweise (`176/178/179/180/181/182/185`) auf vorhandene Chronikseiten
  - Platzhalter fuer `Siebenwind Bote 118` als explizit fehlende Primarquelle
  - Dateinamen-Aliasse (`Aus dem Leben eines Schwarzmagiers`, `Die Sprache Run.html`, `Kanon/Khalandra`)
  - Relativlink-Korrekturen in `Siebenwind_Wiki/index.md`
  - Nav-Korrektur in `mkdocs.yml`
  - Fehlende Zielseite `Siebenwind_Wiki/00_Fundament/Wiki_Style_Guide.md` angelegt
  - Korrektur des Style-Guide-Links in `docs/CONTRIBUTING.md`

## Abschlussmessung

- Rebuild nach allen Korrekturen:
  - `TOTAL_WARN = 0`
  - Build erfolgreich abgeschlossen

# Leitplanken

- Keine inhaltlichen Lore-Interpretationen im Rahmen dieses Schritts.
- Fokus auf technische Erreichbarkeit und stabile Navigierbarkeit.
- Jede Aenderung muss per Build-Metrik validiert werden.
