# Workflow- und Skill-Adapter

Dieser Bereich zeigt die Verbindung zwischen autoritativen Artefakten in `.agent/` und den abgeleiteten Codex-Adaptern in `.agents/skills/`.

## Architektur

- Autoritativ: `.agent/workflows/`, `.agent/skills/`, `.agent/instructions/`
- Kanonischer Discovery-Katalog: `.agent/catalog/catalog.v1.json`
- AI-agnostische Kompatibilitaet: `lore_manifest.json`
- Codex-Adapter: `.agents/skills/` plus `.codex/config.toml`
- Offene Runtime: `./7w_wiki.py` plus MCP

## Wichtige Adapter-Skills

- `session_start` -> `./7w_wiki.py start`, `advisor`, Inbox, Clean-State
- `session_takeover` -> `./7w_wiki.py takeover`, `start`, `advisor`
- `session_handover` -> `./7w_wiki.py handover`, `test --suite all`, `stats`
- `workflow_tech_master` -> `./7w_wiki.py tech --sync-surfaces`, `tech --sync-interop`, `pages validate --json`
- `workflow_test_run` -> `./7w_wiki.py test --suite all`, `test --suite adapter-surfaces-contract`
- `workflow_forum_search` -> `./7w_wiki.py scout --forum bekanntmachungen --pages 3`

## Zugeordnete Workflows

- `/start`
- `/takeover`
- `/handover`
- `/forum_search`
- `/tech_master`
- `/test_run`

Legacy:
- `/antigravity` bleibt nur als deprecated Alias auf `/start`.

## Repo-Pflege

- `./7w_wiki.py tech --sync-interop` synchronisiert Matrix, Runtime-Doku, Katalog, Codex-Adapter, A2A-Karte, Manifest und Tool-Manifest.
- `./7w_wiki.py tech --repo-hygiene --json` zeigt Hot/Cold/Runtime/Build-Klassifikation.
- `./7w_wiki.py tech --repo-hygiene --apply` fuehrt nur konservative, kanonkonforme Bereinigungsschritte aus.

## Discovery-Split

- `/scout` bleibt der breite externe Discovery-Einstieg.
- `/forum_search` ist der operative Spezialpfad fuer neue ingestierbare Forenquellen.

## Pages-Validierung (Runtime)

```bash
./7w_wiki.py pages status
./7w_wiki.py pages validate --contract --json
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
