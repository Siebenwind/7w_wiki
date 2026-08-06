# Siebenwind Styling & Architektur-Profil

Dieses Dokument ist nur noch ein kurzer Operator-Hinweis.

## Kanonische Styling-Autoritaet

- Die aktive, publizierte Styling-Autoritaet ist [docs/STYLING.md](../docs/STYLING.md).
- `docs/assets/` ist die kanonische Live-Asset-Flaeche und production-only.
- `System/Design_Assets/` beherbergt historische oder rohe Designquellen.

## Operator-Hinweise

- `docs/Siebenwind_Wiki/` ist der einzige technische Edit- und Publishing-Baum fuer Wiki-Pages.
- Das retired Root-Verzeichnis `Siebenwind_Wiki/` ist kein aktiver Edit-Pfad mehr.
- UI- oder Theme-Aenderungen muessen gegen `docs/STYLING.md` und die Pages-Surface validiert werden.
- `docs/assets/custom.css` ist der einzige geladene Bundle-Einstieg; direkte Parallelregistrierungen weiterer Theme-Dateien in `mkdocs.yml` erzeugen wieder eine geteilte Styling-Autoritaet.

---
*Zuletzt aktualisiert: 09.04.2026 | Wave 2 Pages Surface Hardening*
