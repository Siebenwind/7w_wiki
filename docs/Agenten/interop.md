# Interop-Leitlinien

Ziel: Einheitliches Verhalten zwischen Codex, Gemini CLI und Antigravity bei unveraenderter Runtime-Oberflaeche.

## Kernregeln

1. Runtime authority: Ausfuehrung nur ueber `./7w_wiki.py`.
2. Orchestrierung bleibt in `.agent/` autoritativ.
3. Externe Discoverability fuer Codex/Jules ueber `.agents/skills/` als duenne Wrapper.
4. Keine Semantik-Aenderung von Workflows ohne dokumentierte Governance-Entscheidung.

## Codex-Modell

- Antigravity: workflow-native UX.
- Codex: discoverbare Workflow- und Skill-Bridges in `.agents/skills/`.
- Runtime: weiterhin ausschliesslich `./7w_wiki.py`.

Codex bekommt keine repo-definierten Slash-Kommandos. Stattdessen verweisen die generierten Workflow-Bridges auf die autoritativen Workflows in `.agent/workflows/` und auf die korrekten CLI-Kommandos.

## Pflichtchecks

```bash
./7w_wiki.py test --suite clean-client-state
./7w_wiki.py test --suite takeover-handover
./7w_wiki.py test --suite interop-doc-links
./7w_wiki.py audit
```

## Codex-Workflow-Bridges

Aktuelle Einstiegspunkte:

- `session_start`
- `session_takeover`
- `session_handover`
- `workflow_tech_master`
- `workflow_test_run`
- `workflow_forum_search`

Forum-Discovery bleibt zweistufig:

- `/scout`: breiter Discovery-Einstieg fuer Homepage, News und Reconnaissance
- `/forum_search`: gezielte Forenquellensuche ueber `./7w_wiki.py scout --forum ...`

## Kanonische Quellen

- `System/Synapse_Board/SY_INTEROP.md`
- `System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md`
- `AGENTS.md`
