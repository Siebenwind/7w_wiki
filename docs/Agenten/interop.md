# Interop-Leitlinien

Ziel: Einheitliches Verhalten zwischen Codex und anderen MCP-faehigen IDEs/CLIs bei unveraenderter Runtime-Oberflaeche.

## Kernregeln

1. Runtime authority: Ausfuehrung nur ueber `./7w_wiki.py`.
2. Orchestrierung bleibt in `.agent/` autoritativ.
3. Externe Discoverability folgt einem Layer-Modell: MCP ist die Live-Schnittstelle, `.agents/skills/` plus `.codex/config.toml` sind der Codex-Adapter.
4. `lore_manifest.json` bleibt als generierte AI-agnostische Kompatibilitaetsflaeche erhalten.
5. Keine Semantik-Aenderung von Workflows ohne dokumentierte Governance-Entscheidung.

## Layer-Modell

- Kanonischer Kern: `.agent/` + `./7w_wiki.py`
- Offene Laufzeitoberflaeche: MCP
- Kompatibilitaetsmanifest: `lore_manifest.json`
- Codex-Adapter: `.agents/skills/` + `.codex/config.toml`
- Discovery-only Zukunftsflaeche: `docs/.well-known/agent.json`

Codex bekommt keine repo-definierten Slash-Kommandos. Stattdessen verweisen die generierten Adapter-Skills auf die autoritativen Workflows und Skills in `.agent/` und auf die korrekten CLI-Kommandos.

## Repo-Hygiene

- `docs/Siebenwind_Wiki/` ist der einzige aktive technische Wiki-Baum.
- Das Wurzelverzeichnis `Siebenwind_Wiki/` ist retired; nur der publizierte URL-Segmentname bleibt bestehen.
- `docs/assets/` ist die Live-Asset-Surface fuer publizierte Artefakte und production-only.
- Entwurfs- und Proposal-Dateien liegen unter `System/Design_Assets/`.
- Historische Evidenz und Snapshot-Familien werden ueber `./7w_wiki.py tech --repo-hygiene [--apply] [--json]` in kalte Buckets verschoben.
- Build-Ausgaben (`site/`, `dist/`) und Laufzeitmassen (Caches, Modelle, venvs) sind keine Repo-Wahrheit.

## Pflichtchecks

```bash
./7w_wiki.py test --suite clean-client-state
./7w_wiki.py test --suite takeover-handover
./7w_wiki.py test --suite interop-doc-links
./7w_wiki.py test --suite repo-hygiene-contract
./7w_wiki.py test --suite manifest-contract
./7w_wiki.py test --suite root-tree-retirement-contract
./7w_wiki.py test --suite styling-surface-contract
./7w_wiki.py test --suite pages-contract-mode-contract
./7w_wiki.py audit
```

## Codex-Adapter

Aktuelle Einstiegspunkte:

- `session_start`
- `session_takeover`
- `session_handover`
- `workflow_tech_master`
- `workflow_test_run`
- `workflow_forum_search`

Antigravity bleibt nur noch als deprecated CLI-Alias zu `/start` erhalten.

Forum-Discovery bleibt zweistufig:

- `/scout`: breiter Discovery-Einstieg fuer Homepage, News und Reconnaissance
- `/forum_search`: gezielte Forenquellensuche ueber `./7w_wiki.py scout --forum ...`

## Kanonische Quellen

- `System/Synapse_Board/SY_INTEROP.md`
- `System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md`
- `AGENTS.md`
