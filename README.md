# Siebenwind Wiki (7w_wiki)

Kuratiertes Lore-Archiv fuer die Welt Siebenwind mit offenem KI-Betrieb, Audit-Trails und redaktioneller Qualitaetskontrolle.

- Public Pages: <https://siebenwind.github.io/7w_wiki/>
- Leser-Einstieg: [docs/index.md](docs/index.md)
- Technische Regeln: [AGENTS.md](AGENTS.md)

## Fuer Leser

- Wiki-Startpunkt: [Siebenwind_Wiki/index.md](Siebenwind_Wiki/index.md)
- Kuratierte Einstiege: [Interessante Artikel](Siebenwind_Wiki/10_Archiv/Interessante_Artikel.md)
- Chronik-Zeitrahmen: [Zeitrechnung (Der Sonnenzirkel)](Siebenwind_Wiki/00_Fundament/Zeitrechnung_(Der_Sonnenzirkel).md)

## Fuer technisch Interessierte: Was die Engine kann

- **Einheitliche Runtime Authority:** Alle Operationen laufen ueber `./7w_wiki.py <command>`.
- **Oracle/RAG mit Source-Scope:** Reproduzierbare Suche mit `--source wiki|quellen|all`.
- **Qualitaetsgates:** Standardisierte Testsuiten plus Audit-Check als Integritaetsbarriere.
- **Pages-Pipeline:** Lokale Validierung und Strict Build fuer GitHub Pages.
- **Agentenkoordination:** Dispatch-Bus fuer Auftragsrouting, Claim/Done-Flow und nachvollziehbare Historie.
- **Transparenter Betrieb:** Changelog, Reports, Taskliste und Synapse-Board sind im Repo sichtbar.

## 5-Minuten Tech Tour

```bash
# 1) Lagebild und Prioritaeten
./7w_wiki.py advisor

# 2) Oracle mit expliziter Quelle
./7w_wiki.py search "Dunvallo Linari" --source wiki

# 3) Interop- und Basiszustand pruefen
./7w_wiki.py test --suite interop-doc-links
./7w_wiki.py test --suite clean-client-state

# 4) Integritaets- und Publishing-Checks
./7w_wiki.py audit
./7w_wiki.py pages build --strict

# 5) Menschlichen Leitpunkt pruefen
./7w_wiki.py leitpunkt status
./7w_wiki.py leitpunkt check
```

## Kernbereiche im Repository

- **Praesentation (Leserfokus):** `Siebenwind_Wiki/`, `docs/index.md`, `docs/Siebenwind_Wiki/`
- **Betrieb (Prozessfokus):** `System/`, `System/Synapse_Board/`, `.agent/`, `.agents/`
- **Koordination:** `MASTER_TASK_LIST.md`, `CHANGELOG.md`, `System/Synapse_Board/DISPATCH/`

## Technische Dokumentation

- Architektur: [docs/architecture.md](docs/architecture.md)
- RAG Setup: [docs/setup_rag.md](docs/setup_rag.md)
- Operations Handbook: [System/AGENT_OPERATIONS_HANDBOOK.md](System/AGENT_OPERATIONS_HANDBOOK.md)
- Interop Standards: [System/Synapse_Board/SY_INTEROP.md](System/Synapse_Board/SY_INTEROP.md)
- Testing Protocol: [System/Synapse_Board/SY_TESTING.md](System/Synapse_Board/SY_TESTING.md)
- Menschlicher Leitpunkt: [docs/Archiv/MAINTAINER_STANDPUNKT.md](docs/Archiv/MAINTAINER_STANDPUNKT.md)

## Mitwirken

- Leitfaden: [CONTRIBUTING.md](CONTRIBUTING.md)
- Aktuelle Prioritaeten: [MASTER_TASK_LIST.md](MASTER_TASK_LIST.md)
- Aenderungshistorie: [CHANGELOG.md](CHANGELOG.md)

## Lizenz

- Code: [MIT](LICENSE)
- Inhalte: CC BY-NC-SA 4.0 (Community Legacy)
