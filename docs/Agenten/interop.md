# Interop-Leitlinien

Ziel: Einheitliches Verhalten zwischen Codex, Gemini CLI und Antigravity bei unveraenderter Runtime-Oberflaeche.

## Kernregeln

1. Runtime authority: Ausfuehrung nur ueber `./7w_wiki.py`.
2. Orchestrierung bleibt in `.agent/` autoritativ.
3. Externe Discoverability ueber `.agents/skills/` als duenne Wrapper.
4. Keine Semantik-Aenderung von Workflows ohne dokumentierte Governance-Entscheidung.

## Pflichtchecks

```bash
./7w_wiki.py test --suite clean-client-state
./7w_wiki.py test --suite takeover-handover
./7w_wiki.py test --suite interop-doc-links
./7w_wiki.py audit
```

## Oracle-Quellenmodus

Recherche immer mit expliziter Quelle:

```bash
./7w_wiki.py search "<query>" --source wiki
./7w_wiki.py search "<query>" --source quellen
./7w_wiki.py search "<query>" --source all
```

## Kanonische Quellen

- `System/Synapse_Board/SY_INTEROP.md`
- `System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md`
- `AGENTS.md`
