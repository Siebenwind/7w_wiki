---
uuid: 9e6a6a7c-4ef6-4f73-96d7-967f21bf90e8
status: ACTIVE
updated_at: 2026-02-16T21:18:56Z
owners:
  - Koordinator
  - Test-Waechter
epistemic: "#meta"
---

# SY_TESTING

Verbindlicher Standard fuer reproduzierbare Testdurchlaeufe, Defect-Kommunikation und Re-Tests.

## Ziel

1. Testlaeufe standardisieren (`clean-client-state`, `takeover-handover`, `all`).
2. Defects ohne stille Fixes behandeln.
3. Fixes nur auf Basis kommunizierter Auftraege umsetzen.

## Runtime-Einstieg

- `./7w_wiki.py test --list-suites`
- `./7w_wiki.py test --suite clean-client-state`
- `./7w_wiki.py test --suite takeover-handover`
- `./7w_wiki.py test --suite interop-doc-links`
- `./7w_wiki.py test --suite all`
- `./7w_wiki.py test --suite <name> --post-failures --from-agent <name> --to-agent ALL --priority HIGH`

Suite-Definitionen liegen in:
- `.agent/tests/suites/*.json`

Testberichte liegen in:
- `Logs/Archive/TEST_<suite>_<timestamp>.md`

## Agentenmentalitaet

### Tester (Test-Waechter)
- Skeptisch, reproduzierbar, read-first.
- Keine stillen Produktivfixes.
- Bei FAIL: zuerst Defect kommunizieren (Dispatch oder Task).

### Fix-Agent
- Arbeitet nur auf geclaimten Defects.
- Jeder Fix muss Message-ID/Task-ID referenzieren.
- Re-Test ist Pflicht vor Abschluss.

### Koordinator
- Priorisiert Defects.
- Steuert Claiming und Abschluss.
- Prueft Changelog-/Report-Referenzen.

## Kommunikationspflicht (hart)

Ein Fix ist nur zulaessig, wenn mindestens eines vorliegt:
1. Dispatch-Message (`mail post`, danach `claim`), oder
2. referenzierter Task-Eintrag (`task.md`/aehnlich).

## Defect-Lebenszyklus

1. Test ausfuehren.
2. Bei FAIL:
   - Defect posten (`--post-failures`) oder Task erstellen.
3. Fix-Agent uebernimmt (`mail claim` oder Task-Referenz).
4. Fix umsetzen.
5. Re-Test:
   - erst betroffene Suite
   - danach `--suite all`
6. Abschluss:
   - `mail done` (oder Task als done markieren)
   - Changelog-Eintrag mit Defect-Referenz

## Verweise

- `.agent/workflows/test_run.md`
- `.agent/scripts/test_runner.py`
- `System/Synapse_Board/SY_DISPATCH.md`
- `System/Synapse_Board/SY_INTEROP.md`
