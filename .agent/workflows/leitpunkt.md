---
description: Workflow fuer den menschlichen Leitpunkt (Maintainer-Standpunkt) inkl. Governance-Checks
---

# Workflow: `/leitpunkt` (Menschlicher Leitpunkt)

## Interop-Status
- runtime_commands:
  - `7w_wiki.py leitpunkt`
  - `7w_wiki.py leitpunkt view`
  - `7w_wiki.py leitpunkt status`
  - `7w_wiki.py leitpunkt check`
  - `7w_wiki.py leitpunkt check --strict`
  - `7w_wiki.py leitpunkt scaffold`
  - `7w_wiki.py leitpunkt scaffold --force`
  - `7w_wiki.py test --suite interop-doc-links`
  - `7w_wiki.py mail post --from <agent> --to ALL --subject "<text>" --body "<text>"`
- method_only:
  - `/leitpunkt`

## 1. Zweck
Sichere einen **verbindlichen menschlichen Steuerpunkt**, damit Agenten nicht bei jeder Session neu interpretiert werden muessen.
Der zentrale Artefaktpfad ist:
- `docs/Archiv/MAINTAINER_STANDPUNKT.md`

## 2. Kurzloop (Empfohlen)
1. `./7w_wiki.py leitpunkt status`
2. `./7w_wiki.py leitpunkt check`
3. Leitpunktseite gezielt aktualisieren (Prioritaeten, No-Gos, Eskalation).
4. Optional: `./7w_wiki.py leitpunkt check --strict` (nur fuer Governance-Release/Handover/Policy-Freeze).
5. `./7w_wiki.py test --suite interop-doc-links`
6. Aenderung via Dispatch kurz broadcasten.

## 3. Check-Definition
- `status`: zeigt Reifegrad (MISSING / BLOCKED / DRAFT / ACTIVE).
- `check`: prueft Pflichtsektionen.
- `check --strict`: prueft Pflichtsektionen + keine offenen `TODO` Marker.
- `scaffold`: erstellt Vorlage, falls Datei fehlt.

## 3b. Striktheits-Regel
- `check` ist der Tagesmodus (muss stabil gruen sein).
- `check --strict` ist ein **Freigabe-Gate**, kein permanenter Entwicklungsblocker.

## 4. Freigabe-Disziplin
- Bei inhaltlicher Leitungsentscheidung immer Changelog-Eintrag.
- Bei geaendertem Leitpunkt immer kurze Dispatch-Notiz an `ALL`.
- Konflikte zwischen Leitpunkt und Einzelwunsch als explizite Entscheidungsfrage eskalieren.
