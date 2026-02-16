---
uuid: 1b3c8f24-7fb5-4ec3-9d43-7b1f17f69371
status: ACTIVE
updated_at: 2026-02-16T16:30:00Z
epistemic: "#meta"
---

# AGENT_OPERATIONS_HANDBOOK

Zweck: Zentrale Uebersicht fuer den operativen Betrieb von Agenten, Skills und Workflows im Repository.

## Betriebsinvarianten

1. Runtime Authority: Ausfuehrung nur ueber `./7w_wiki.py`.
2. Orchestrierung bleibt in `.agent/` autoritativ.
3. Discoverability fuer Codex/Jules ueber `.agents/skills/` als duenne Wrapper.
4. Governance-Dokumente bleiben in `System/` und `System/Synapse_Board/`.
5. Neue Systemdokumente muessen in `System/COORDINATION_HUB.md` registriert werden.

## Strukturkarte

| Pfad | Rolle | Autoritaet |
|---|---|---|
| `7w_wiki.py` | Einziger Runtime-Einstieg | Ja |
| `.agent/workflows/` | Methodische SOPs und Department-Loops | Ja |
| `.agent/instructions/` | Persona- und Rollenlogik | Ja |
| `.agent/scripts/` | Implementierte Backing-Skripte hinter CLI-Kommandos | Ja |
| `.agent/skills/` | Fachlogik (z. B. Oracle, Lektor) | Ja |
| `.agents/skills/` | Interop-Wrapper fuer externe Agenten | Bruecke |
| `System/Synapse_Board/` | Governance, Interop-Normen, Dispatch-Standards | Ja |
| `docs/` | GitHub-Pages-Ausspielung | Publishing |

## Standard-Arbeitszyklus

1. Orientieren: `./7w_wiki.py start` und `./7w_wiki.py advisor`.
2. Planen: `MASTER_TASK_LIST.md`, `task.md`, offene Dispatch-Nachrichten.
3. Umsetzen: Nur ueber CLI-Kommandos aus `7w_wiki.py`.
4. Validieren: Mindestens `./7w_wiki.py audit`, bei Dokuaenderungen auch `check`, `stats`, `archive sync`.
5. Dokumentieren: `CHANGELOG.md`, Boards, Register- und Doku-Updates.

## Oracle-Suchdisziplin

`./7w_wiki.py search` muss mit expliziter Quelle genutzt werden:

- `--source wiki`: kuratierte Wissensebene
- `--source quellen`: Rohquellenebene
- `--source all`: Kreuzabgleich beider Ebenen

Regel: Bei relevanten Lore-Entscheidungen immer mindestens `wiki` und `quellen` pruefen; bei Konflikten `all` als Gesamtabgleich.

## Dispatch-Betriebsmodell

Verbindlich gemaess `System/Synapse_Board/SY_DISPATCH.md`:

1. Pfad: `System/Synapse_Board/DISPATCH/`
2. Statusfluss: `OPEN` -> `CLAIMED` -> `DONE`
3. CLI-Nutzung ueber `./7w_wiki.py mail ...`

## Dokumentation und GitHub Pages

1. Autoritative Betriebsdokumente liegen in `System/`.
2. Fuer GitHub Pages werden sichtbare Eintraege in `docs/` und `mkdocs.yml` gepflegt.
3. Der `/docs`-Workflow ist die Pflichtstrecke fuer Doku-Paritaet.

## Verweise

- `System/Synapse_Board/SY_INTEROP.md`
- `System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md`
- `System/Synapse_Board/SY_DISPATCH.md`
- `System/COORDINATION_HUB.md`
- `.agent/workflows/start.md`
