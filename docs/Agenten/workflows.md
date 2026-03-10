# Workflow- und Skill-Bruecken

Dieser Bereich zeigt die Bruecke zwischen autoritativen Workflows in `.agent/` und den discoverbaren Codex-Wrappern in `.agents/skills/`.

## Architektur

- Autoritativ: `.agent/workflows/`, `.agent/skills/`, `.agent/instructions/`
- Interop-Wrapper: `.agents/skills/` (Codex/Jules)
- Runtime: `./7w_wiki.py`

## Wichtige Bruecken-Skills

- `session_start` -> `./7w_wiki.py start`, `advisor`, Inbox, Clean-State
- `session_takeover` -> `./7w_wiki.py takeover`, `start`, `advisor`
- `session_handover` -> `./7w_wiki.py handover`, `test --suite all`, `stats`
- `workflow_tech_master` -> `./7w_wiki.py tech`, `tech --sync-interop`, `pages validate --json`
- `workflow_test_run` -> `./7w_wiki.py test --suite all`, `test --suite codex-workflow-bridges`
- `workflow_forum_search` -> `./7w_wiki.py scout --forum bekanntmachungen --pages 3`

## Zugeordnete Workflows

- `/start`
- `/takeover`
- `/handover`
- `/forum_search`
- `/tech_master`
- `/test_run`

## Discovery-Split

- `/scout` bleibt der breite externe Discovery-Einstieg.
- `/forum_search` ist der operative Spezialpfad fuer neue ingestierbare Forenquellen.

## Pages-Validierung (Runtime)

```bash
./7w_wiki.py pages status
./7w_wiki.py pages validate --json
./7w_wiki.py pages validate --json --strict-links
./7w_wiki.py pages build --strict
```

## Kanonische Quellen

- `.agent/workflows/start.md`
- `.agent/workflows/takeover.md`
- `.agent/workflows/handover.md`
- `.agent/workflows/forum_search.md`
- `.agent/workflows/tech_master.md`
- `.agent/workflows/test_run.md`
