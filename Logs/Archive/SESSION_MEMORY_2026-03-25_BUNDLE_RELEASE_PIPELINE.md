# Session Memory 2026-03-25 - Bundle Release Pipeline

## Kontext
- Ziel war, die Bundle-Pipeline aus dem normalen Git-Verlauf zu entfernen, lokale Bundle-Erzeugung aber beizubehalten.
- Ausgangslage auf dem sauberen Publish-Branch:
  - `./7w_wiki.py` hatte keinen `package`-Befehl.
  - Bundle-Artefakte in `dist/` sollten kuenftig nicht mehr versioniert werden.
  - GitHub sollte Bundles nur fuer Releases/Tags als Release-Assets bauen.

## Durchgefuehrte Aenderungen
- `./7w_wiki.py package` als oeffentlichen CLI-Befehl wiederhergestellt.
- Packaging-Helfer und Profilkonfiguration neu angelegt:
  - `.agent/scripts/install_tool.py`
  - `.agent/scripts/package_tool.py`
  - `.agent/config/install_profiles.json`
- Release-Workflow fuer Bundles angelegt:
  - `.github/workflows/release-bundles.yml`
  - Trigger nur auf `v*`-Tags
  - baut `ubuntu` + `agent-only`
  - haengt Bundle und JSON-Manifest an GitHub Releases
- Git-Hygiene verschaerft:
  - `.gitignore` ignoriert jetzt `dist/`, `Logs/Queues/`, Pages-Cache und `*_latest.json` Runtime-Artefakte
- Governance-/Interop-Doku nachgezogen:
  - `AGENTS.md`
  - `System/AGENT_OPERATIONS_HANDBOOK.md`
  - `System/Synapse_Board/SY_INTEROP.md`
  - `System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md`
  - `System/COORDINATION_HUB.md`
  - `.agent/workflows/tech_master.md`
- Repo-Sync ausgefuehrt:
  - `./7w_wiki.py tech --sync-interop`

## Validierung
- `./7w_wiki.py --help` zeigt `package`
- `./7w_wiki.py package --platform ubuntu --profile agent-only --output-dir /tmp/7w_bundle_smoke --json`
  - PASS
  - Archiv erstellt unter `/tmp/7w_bundle_smoke/7w_wiki_ubuntu_agent-only_20260325_220020.tar.gz`
- `./7w_wiki.py test --suite interop-command-registry`
- `./7w_wiki.py test --suite workflow-matrix-contract`
- `./7w_wiki.py test --suite tool-manifest-contract`
- `./7w_wiki.py test --suite interop-doc-links`
- `./7w_wiki.py test --suite clean-client-state`
- `./7w_wiki.py test --suite process-dispatch-curiosity`

## Offene Punkte / Naechster Schritt
1. Die Aenderungen sind implementiert und validiert, aber in dieser Session noch nicht committed oder gepusht.
2. Fuer einen echten Release-Durchlauf braucht es einen `v*`-Tag auf dem sauberen Publish-Pfad.
3. Der naechste Git-Schritt sollte bewusst auf dem cleanen Branch erfolgen, damit die alten grossen `dist/*.tar.gz`-Objekte nicht erneut in einen Push geraten.
