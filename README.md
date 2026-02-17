# Siebenwind Wiki (7w_wiki)

Kuratiertes Lore-Archiv fuer die Welt Siebenwind.
Das Projekt verbindet historische Quellenbewahrung, KI-gestuetzte Erschliessung und redaktionelle Qualitaetskontrolle.

## Schnellstart nach Ziel

### Lesen
- Public Pages: <https://siebenwind.github.io/7w_wiki/>
- Wiki-Startpunkt: [Siebenwind_Wiki/index.md](Siebenwind_Wiki/index.md)
- Kuratierte Einstiege: [Interessante Artikel](Siebenwind_Wiki/10_Archiv/Interessante_Artikel.md)

### Mitwirken
- Leitfaden: [CONTRIBUTING.md](CONTRIBUTING.md)
- Aktuelle Prioritaeten: [MASTER_TASK_LIST.md](MASTER_TASK_LIST.md)
- Aenderungshistorie: [CHANGELOG.md](CHANGELOG.md)

### Agentenbetrieb und Technik
- Kanonische Agenteninstruktionen: [AGENTS.md](AGENTS.md)
- Betriebsuebersicht: [System/AGENT_OPERATIONS_HANDBOOK.md](System/AGENT_OPERATIONS_HANDBOOK.md)
- Interop-Standards: [System/Synapse_Board/SY_INTEROP.md](System/Synapse_Board/SY_INTEROP.md)

## Praesentation vs. Betrieb

- **Praesentation (Leserfokus):** `Siebenwind_Wiki/`, `docs/index.md`, `docs/Siebenwind_Wiki/`
- **Betrieb (Prozessfokus):** `System/`, `System/Synapse_Board/`, `.agent/`, `.agents/`
- **Regel:** Runtime-Aktionen laufen ausschliesslich ueber `./7w_wiki.py`.

## Runtime Authority

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

# Qualitaet und Publikation
./7w_wiki.py test --suite clean-client-state
./7w_wiki.py test --suite interop-doc-links
./7w_wiki.py pages validate
./7w_wiki.py audit
```

## Lizenz

- Code: [MIT](LICENSE)
- Inhalte: CC BY-NC-SA 4.0 (Community Legacy)
