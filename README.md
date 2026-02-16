# Siebenwind Wiki (7w_wiki)

Repository fuer das Siebenwind-Wiki, seine Quellenaufbereitung und den Agentenbetrieb.

## Schnellnavigation

- Lesen (GitHub Pages): <https://siebenwind.github.io/7w_wiki/>
- Wiki-Startpunkt im Repo: [Siebenwind_Wiki/index.md](Siebenwind_Wiki/index.md)
- Projektstatus: [MASTER_TASK_LIST.md](MASTER_TASK_LIST.md)
- Aenderungen: [CHANGELOG.md](CHANGELOG.md)

## Dieses Repository in 3 Spuren

1. Endnutzer-Wiki
- Inhalte fuer Leser liegen unter `Siebenwind_Wiki/` und werden nach `docs/Siebenwind_Wiki/` publiziert.

2. Mitarbeit und Redaktion
- Regeln und Projektablauf: [CONTRIBUTING.md](CONTRIBUTING.md)
- Qualitaetssicherung ueber die zentrale CLI `./7w_wiki.py`.

3. Agentenbetrieb und Interop
- Kanonische Agenteninstruktionen: [AGENTS.md](AGENTS.md)
- Betriebsuebersicht: [System/AGENT_OPERATIONS_HANDBOOK.md](System/AGENT_OPERATIONS_HANDBOOK.md)
- Interop-Standards: [System/Synapse_Board/SY_INTEROP.md](System/Synapse_Board/SY_INTEROP.md)

## Runtime Authority

Der einzige Runtime-Einstieg ist:

```bash
./7w_wiki.py <command>
```

Wichtige Kommandos:

```bash
# Orientierung
./7w_wiki.py start
./7w_wiki.py advisor

# Recherche (Oracle)
./7w_wiki.py search "<query>" --source wiki
./7w_wiki.py search "<query>" --source quellen
./7w_wiki.py search "<query>" --source all

# Qualitaet / Interop
./7w_wiki.py test --suite clean-client-state
./7w_wiki.py test --suite interop-doc-links
./7w_wiki.py audit
```

## Dokumentationsbereiche

- Endnutzer-Pages: `docs/index.md` + `docs/Siebenwind_Wiki/`
- Agenten-Pages-Hub: `docs/Agenten/`
- Kanonische Systemdokumente: `System/` und `System/Synapse_Board/`

## Lizenz

- Code: [MIT](LICENSE)
- Inhalte: CC BY-NC-SA 4.0 (Community Legacy)
