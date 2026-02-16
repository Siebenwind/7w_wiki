# Workflow- und Skill-Bruecken

Dieser Bereich zeigt die Bruecke zwischen autoritativen Workflows in `.agent/` und den discoverbaren Wrappern in `.agents/skills/`.

## Architektur

- Autoritativ: `.agent/workflows/`, `.agent/skills/`, `.agent/instructions/`
- Interop-Wrapper: `.agents/skills/`
- Runtime: `./7w_wiki.py`

## Wichtige Bruecken-Skills

- `onboarding` -> `./7w_wiki.py start`, `advisor`, `test`, `audit`
- `interop-audit` -> Interop- und Runtime-Paritaetspruefung
- `oracle` -> `search --source wiki|quellen|all`
- `sanitize` -> strukturelle Normalisierung
- `lektor-check` -> Stil und Grammatik
- `test-run` -> standardisierte Suiten + Defect-Routing

## Zugeordnete Workflows

- `/start`
- `/takeover`
- `/handover`
- `/docs`
- `/test_run`

## Kanonische Quellen

- `.agent/workflows/start.md`
- `.agent/workflows/takeover.md`
- `.agent/workflows/handover.md`
- `.agent/workflows/docs.md`
- `.agent/workflows/test_run.md`
