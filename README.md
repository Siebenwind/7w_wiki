# Siebenwind Wiki (7w_wiki)

Kuratiertes Lore-Archiv fuer die Welt Siebenwind mit offenem KI-Betrieb, Audit-Trails und redaktioneller Qualitaetskontrolle.

- Public Pages: <https://siebenwind.github.io/7w_wiki/>
- Leser-Einstieg: [docs/index.md](docs/index.md)
- Technische Regeln: [AGENTS.md](AGENTS.md)

## Fuer Leser

- Wiki-Startpunkt: [docs/Siebenwind_Wiki/index.md](docs/Siebenwind_Wiki/index.md)
- Kuratierte Einstiege: [docs/Siebenwind_Wiki/10_Archiv/Interessante_Artikel.md](docs/Siebenwind_Wiki/10_Archiv/Interessante_Artikel.md)
- Chronik-Zeitrahmen: [docs/Siebenwind_Wiki/00_Fundament/Zeitrechnung_(Der_Sonnenzirkel).md](docs/Siebenwind_Wiki/00_Fundament/Zeitrechnung_(Der_Sonnenzirkel).md)

## Fuer technisch Interessierte: Was die Engine kann

- **Einheitliche Runtime Authority:** Alle Operationen laufen ueber `./7w_wiki.py <command>`.
- **Oracle/RAG mit Source-Scope:** Reproduzierbare semantische Suche mit `--source wiki|quellen|all`.
- **Self-Describing CLI:** `./7w_wiki.py --help-json` fuer dynamische Introspection, `.agent/config/tools.json` fuer OpenAI-kompatible Tool-Definitionen.
- **Universal JSON:** Alle Kernkommandos unterstuetzen `--json` fuer maschinenlesbare Ausgabe.
- **Lint- und Ingest-Pipelines:** `lint` (Sanitizer + Lektor + Score) und `ingest` (Lint + Archive Sync + Audit) als Ein-Befehl-Pipelines.
- **Version Management:** Zentrales `VERSION` File mit `./7w_wiki.py version --bump`.
- **Archivar:** `archive rotate` komprimiert veraltete Logs, rotiert DONE-Dispatches und archiviert abgeschlossene Tickets.
- **Repo-Hygiene:** `tech --repo-hygiene [--apply] [--json]` klassifiziert Hot/Cold/Runtime/Build-Pfade und fuehrt konservative Bereinigung aus.
- **Workflow Automation:** `--run` und `--resume` fuer Start/Takeover/Handover Workflows.
- **Qualitaetsgates:** Standardisierte Testsuiten plus Audit-Check als Integritaetsbarriere.
- **Agentenkoordination:** Dispatch-Bus mit `--report-path` und strukturierten Payloads.
- **Kompatibilitaetsmanifest:** `lore_manifest.json` bleibt als generierte, AI-agnostische Surface erhalten und wird aus dem Katalog aktualisiert.

## 5-Minuten Tech Tour

```bash
# 1) Lagebild und Prioritaeten
./7w_wiki.py advisor

# 2) Oracle mit expliziter Quelle
./7w_wiki.py search "Dunvallo Linari" --source wiki

# 3) Lint-Pipeline (Sanitizer + Lektor + Score)
./7w_wiki.py lint docs/Siebenwind_Wiki/00_Fundament/Magie_Grundlagen.md --fix

# 4) Ingest-Pipeline (Lint + Archive Sync + Audit)
./7w_wiki.py ingest Quellen/Zeitung\ 7w\ Bote/Bote_194.md

# 5) Archivar (Log-Rotation)
./7w_wiki.py archive rotate --dry-run

# 6) Version pruefen
./7w_wiki.py version

# 7) Repo-Hygiene und Retention
./7w_wiki.py tech --repo-hygiene --json
```

## Kernbereiche im Repository

- **Praesentation (Leserfokus):** `docs/index.md`, `docs/Siebenwind_Wiki/`, `docs/assets/`
- **Betrieb (Prozessfokus):** `System/`, `System/Synapse_Board/`, `.agent/`, `.agents/`
- **Kompatibilitaet & Discovery:** `.agent/catalog/`, `lore_manifest.json`, `mcp_config.json`, `docs/.well-known/agent.json`
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
