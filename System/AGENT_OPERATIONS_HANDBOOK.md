---
uuid: 1b3c8f24-7fb5-4ec3-9d43-7b1f17f69371
status: ACTIVE
epistemic: "#meta"
---

# AGENT_OPERATIONS_HANDBOOK

Zweck: Zentrale Uebersicht fuer den operativen Betrieb von Agenten, Skills und Workflows im Repository.

## Betriebsinvarianten

1. Runtime Authority: Generische Wissenswerk-Operationen laufen ueber `./wissenswerk.py`; Legacy-Siebenwind-Operationen laufen weiter ueber `./7w_wiki.py`.
2. Orchestrierung bleibt plattformneutral: `AGENTS.md`, `DESIGN.md`, `wissenswerk.yaml`, `project_manifest.json`, JSON-CLI, Tool-Manifest und MCP sind die kanonischen Vertraege.
3. Discoverability fuer externe Hosts folgt dem Layer-Modell: Host-spezifische Adapter wie `.agents/skills/` plus `.codex/config.toml` werden aus neutralen Vertraegen abgeleitet und duerfen keine eigene Semantik enthalten.
4. Governance-Dokumente bleiben in `System/` und `System/Synapse_Board/`.
5. Neue Systemdokumente muessen in `System/COORDINATION_HUB.md` registriert werden.
6. Epistemische Praezedenz ist `Homepage > Quellen > Wiki Pages`; die volle Drift-/Pages-Regel steht in [SY_DRIFT_PAGES_CONTRACT.md](Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md).
7. `project_manifest.json` ist das generische Wissenswerk-Produktmanifest; `lore_manifest.json` ist eine generierte Siebenwind-Kompatibilitaetsoberflaeche, nicht die Quelle der Wahrheit.

<!-- BEGIN GENERATED DRIFT CONTRACT REFERENCE -->
> Generated reference block. The surrounding narrative text remains manually maintained.
> Canonical contract: [SY_DRIFT_PAGES_CONTRACT.md](Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md)
>
> - Epistemic precedence: `Homepage > Quellen > Wiki Pages`.
> - `docs/Siebenwind_Wiki/` is the technical edit/publish tree, not the highest truth source.
> - Technical drift is validated via `./7w_wiki.py sanitize`, `./7w_wiki.py audit`, and `./7w_wiki.py pages validate --json [--strict-links]`.
> - Deterministic contract/CI checks use `./7w_wiki.py pages validate --contract --json`.
> - `--strict` hardens the MkDocs build; `--strict-links` is the hard unresolved-link gate.
> - Generated command registries are synced by `./7w_wiki.py tech --sync-docs` / `--sync-interop`; narrative rules live in the canonical contract.
<!-- END GENERATED DRIFT CONTRACT REFERENCE -->

## Strukturkarte

| Pfad | Rolle | Autoritaet |
|---|---|---|
| `wissenswerk.py` | Generischer Wissenswerk Runtime-Einstieg | Ja |
| `7w_wiki.py` | Legacy-Siebenwind Runtime und Kompatibilitaetsbruecke | Kompatibilitaet |
| `wissenswerk.yaml` | Tenant-, Provider-, Workflow-, Reset- und Lokalisierungsvertrag | Ja |
| `project_manifest.json` | Generisches Produktmanifest | Ja |
| `DESIGN.md` | UI-/Dokumentationsdesignvertrag | Ja |
| `.agent/workflows/` | Legacy-SOPs und Tenant-/Maintainer-Loops | Legacy/Adapter |
| `.agent/instructions/` | Legacy-Personae; neue Kernrollen sind coordinator/curator/verifier/maintainer | Legacy/Adapter |
| `.agent/scripts/` | Implementierte Backing-Skripte hinter CLI-Kommandos | Ja |
| `.agent/skills/` | Fachlogik (z. B. Oracle, Lektor) | Ja |
| `.agent/catalog/` | Neutraler Discovery-Katalog fuer Skills, Workflows und Surfaces | Ja |
| `lore_manifest.json` | Generiertes Siebenwind-Kompatibilitaetsmanifest | Kompatibilitaet |
| `wissenswerk_export_manifest.json` | Branch-first Extraktionsvertrag fuer das spaetere Standalone-Repo | Ja |
| `.agents/skills/` | Codex-native Adapter-Surface (abgeleitet aus dem Katalog) | Adapter |
| `.codex/config.toml` | Projektweite Codex-Verdrahtung auf MCP und Adapter-Skills | Adapter |
| `System/Synapse_Board/` | Governance, Interop-Normen, Dispatch-Standards | Ja |
| `docs/` | GitHub-Pages-Ausspielung | Publishing |
| `docs/Siebenwind_Wiki/` | Technischer Edit-Baum fuer Wiki-Pages | Ja (technisch), nein (epistemisch) |
| `docs/assets/` | Live-Asset-Surface fuer publizierte Styles und Medien | Ja (publiziert) |
| `System/Design_Assets/` | Historisches Design-Archiv / Quellenmaterial | Kalt |

## Standard-Arbeitszyklus

1. Orientieren: `./7w_wiki.py start`, `./7w_wiki.py advisor --json` und fuer den generischen Kern `./wissenswerk.py doctor --json`.
2. Planen: `MASTER_TASK_LIST.md`, `task.md`, offene Dispatch-Nachrichten.
3. Umsetzen: Generische Operationen ueber `wissenswerk.py`; Legacy-Siebenwind-Operationen ueber `7w_wiki.py`.
   Drift zuerst klassifizieren: technischer Drift (Layout, Links, Split-Brain, Generatoren) vs. epistemischer Drift (Homepage/Quellen widersprechen Wiki-Pages). Fuer den verbindlichen Volltext gilt [SY_DRIFT_PAGES_CONTRACT.md](Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md).
   Repo-Hygiene, Retention und kalte Evidenzbuckets laufen ueber `./7w_wiki.py tech --repo-hygiene`; Wissenswerk-State laeuft ueber `./wissenswerk.py reset ... --dry-run --json` oder `./wissenswerk.py wipe ... --dry-run --json`. Vor Public-Repo-Arbeit immer `./wissenswerk.py hygiene reports --json` und `./wissenswerk.py export plan --json` pruefen.
4. Validieren: Fuer Wissenswerk-only Arbeit gilt der fokussierte Gate: `python3 -m py_compile wissenswerk.py`, `./wissenswerk.py doctor --json`, `./wissenswerk.py hygiene reports --json`, `./wissenswerk.py export plan --json`, `./7w_wiki.py test --suite wissenswerk-contract --timeout 60` und `git diff --check`. Bei geaenderten Vertraegen oder Navigationsdateien zusaetzlich `manifest-contract`, `interop-command-registry` und `interop-doc-links`. Legacy-Siebenwind-Pruefungen wie `audit`, `pages validate`, `pages-full-smoke`, `stats` und `archive sync` nur ausfuehren, wenn Legacy-Inhalt, Legacy-Tooling oder die publizierte Siebenwind-Seite beruehrt wurde.
5. Dokumentieren: `CHANGELOG.md`, Boards, Register- und Doku-Updates.

**Automatisierung**: Markierungen wie `// turbo` sind methodische Host-Hinweise. `7w_wiki.py start|takeover|handover` zeigen standardmaessig die Workflows an; erst `--run` startet die jeweilige Checkliste, `--resume` setzt sie fort.

## Wissenswerk 2.0 Kernprozess

Nutzerfluss:

1. `./wissenswerk.py init --json`
2. `./wissenswerk.py ingest --from-ragprep <dir> --apply --json`
3. `./wissenswerk.py curate --json`
4. `./wissenswerk.py wiki build --apply --json`
5. `./wissenswerk.py search "<query>" --source raw|wiki|all --json`
6. `./wissenswerk.py bot discord --json`

Maintainerfluss:

1. `./wissenswerk.py doctor --json`
2. `./wissenswerk.py providers check --json`
3. `./wissenswerk.py design lint --json`
4. `./wissenswerk.py hygiene reports --json`
5. `./wissenswerk.py export plan --json`
6. `./wissenswerk.py reset <memory|index|generated|wiki> --dry-run --json`
7. `./wissenswerk.py wipe <tenant|all> --dry-run --json`

Kernrollen:

- `coordinator`: Run-Planung, Reports, Delegation, menschliche Eskalation.
- `curator`: Korpus-Inventar, RagPrep-Import, Artikelplanung, Quellenzuordnung.
- `verifier`: Belege, Konflikte, Link-/Provenance-Pruefung, Audit.
- `maintainer`: Core-Code, Provider, Migrationen, Tests, Releases.

## Runtime Commands

<!-- BEGIN GENERATED RUNTIME COMMAND LIST -->
- `search`
- `start`
- `test`
- `takeover`
- `handover`
- `historian`
- `repair`
- `audit`
- `index`
- `index-pages`
- `pages`
- `advisor`
- `inquisition`
- `sanitize`
- `lint`
- `score`
- `ingest`
- `translate`
- `watch`
- `package`
- `check`
- `archive`
- `mail`
- `scout`
- `tech`
- `version`
- `antigravity`
- `leitpunkt`
- `stats`
- `mcp`
- `wissenswerk`
<!-- END GENERATED RUNTIME COMMAND LIST -->

## Maintainer-Leitpunkt (Menschliche Steuerung)

Verbindlicher Anker:
- `docs/Archiv/MAINTAINER_STANDPUNKT.md`

CLI-Unterstuetzung:
- `./7w_wiki.py leitpunkt` (Workflow anzeigen)
- `./7w_wiki.py leitpunkt status` (Reifegrad anzeigen)
- `./7w_wiki.py leitpunkt check [--strict]` (Struktur/No-TODO-Pruefung)
- `./7w_wiki.py leitpunkt scaffold [--force]` (Vorlage erzeugen)

## Repair-Modi
- Standardmodus: `./7w_wiki.py repair` (interaktiv, Default-Auswahl = Voll-Durchlauf 1→3)
- Non-interaktiv: `./7w_wiki.py repair --full` (Frontmatter Fixer + Smart Link Repair + Source Reference Repair)

## Testbetrieb (Clean-State & Interop)

Verbindlicher Einstieg:

1. `./7w_wiki.py test --suite clean-client-state`
2. `./7w_wiki.py test --suite takeover-handover`
3. `./7w_wiki.py test --suite interop-doc-links`
4. `./7w_wiki.py test --suite interop-command-registry`
5. `./7w_wiki.py test --suite workflow-matrix-contract`
6. `./7w_wiki.py test --suite catalog-contract`
7. `./7w_wiki.py test --suite adapter-surfaces-contract`
8. `./7w_wiki.py test --suite delegation-policy-contract`
9. `./7w_wiki.py test --suite repo-hygiene-contract`
10. `./7w_wiki.py test --suite manifest-contract`
11. `./7w_wiki.py test --suite source-tree-contract`
12. `./7w_wiki.py test --suite legacy-doc-contract`
13. `./7w_wiki.py test --suite asset-surface-contract`
14. `./7w_wiki.py test --suite root-tree-retirement-contract`
15. `./7w_wiki.py test --suite styling-surface-contract`
16. `./7w_wiki.py test --suite tool-manifest-contract`
17. `./7w_wiki.py test --suite pages-contract-mode-contract`
18. `./7w_wiki.py test --suite source-link-hygiene`
19. `./7w_wiki.py test --suite process-dispatch-curiosity`
20. `./7w_wiki.py test --suite bridge-placeholder-guard`
21. `./7w_wiki.py test --suite reader-stats-contract`
22. Optional Gesamtlauf: `./7w_wiki.py test --suite all` (stabiler Standardlauf ohne RAG-Smoke)
23. Optional Oracle-Diagnose: `./7w_wiki.py test --suite rag-relevance-smoke --timeout 30` oder `./7w_wiki.py test --suite all --include-rag`

Bei Pages-/Navigationsaenderungen zusaetzlich:

- `./7w_wiki.py test --suite pages-full-smoke`
- `./7w_wiki.py pages validate --json`

Defect-Regel:

1. Bei FAIL zuerst Kommunikationsartefakt erzeugen (Dispatch oder Task).
2. Fixes nur auf geclaimte Defects.
3. Nach Fix immer Re-Test + Changelog-Verweis auf Message-ID/Task-ID.

Referenz: `System/Synapse_Board/SY_TESTING.md`

## Oracle-Suchdisziplin

`./7w_wiki.py search` muss mit expliziter Quelle genutzt werden:

- `--source wiki`: abgeleitete Wiki-Ebene unter `docs/Siebenwind_Wiki/`
- `--source quellen`: Rohquellenebene
- `--source all`: Kreuzabgleich beider Ebenen

Regel: Bei relevanten Lore-Entscheidungen immer Homepage und Quellen gegenpruefen; `wiki` ist die abgeleitete Seitenebene. `all` ist ein Arbeitsabgleich, kein Override der Praezedenz.

## Adapter Surfaces

Codex bekommt workflow-nahe Einstiegspunkte ueber generierte Adapter-Skills in `.agents/skills/`.

Aktuelle Schwerpunkt-Adapter:
- `session_start`
- `session_takeover`
- `session_handover`
- `workflow_tech_master`
- `workflow_test_run`
- `workflow_forum_search`

Discovery-Split:
- `/scout` bleibt der breite Discovery-Einstieg.
- `/forum_search` ist der dedizierte Betriebsweg fuer neue ingestierbare Forenquellen.

Maintainer-Regel:
- Adapter-Skills werden nicht manuell gepflegt.
- Quelle der Wahrheit ist der kanonische Katalog in `.agent/catalog/catalog.v1.json`.
- Regeneration erfolgt ueber `./7w_wiki.py tech --sync-surfaces` oder den Vollabgleich `./7w_wiki.py tech --sync-interop`.
- Das Kompatibilitaetsmanifest `lore_manifest.json` wird aus demselben Kanon erzeugt und im Vollabgleich mitgeschrieben.
- `./7w_wiki.py tech --sync-bridges` bleibt nur als deprecated Alias fuer alte Runbooks bestehen.

## Dispatch-Betriebsmodell

Verbindlich gemaess `System/Synapse_Board/SY_DISPATCH.md`:

1. Pfad: `System/Synapse_Board/DISPATCH/`
2. Statusfluss: `OPEN` -> `CLAIMED` -> `DONE`
3. CLI-Nutzung ueber `./7w_wiki.py mail ...`

### Dispatch-Hygiene (Pflicht)

1. Session-Start: `./7w_wiki.py mail inbox --status OPEN`
2. Bei Uebernahme: `claim` setzen, dann bearbeiten, dann `done`.
3. Entscheidungen immer ueber Dispatch referenzieren und verlinkte Conflict/Research-Tickets nachziehen.
4. Bei laengeren Aufgaben aktive Status-Heartbeats senden (kurzes `mail post` zu Stand/Blocker/naechstem Schritt).
5. Widersprueche als Frage formulieren (Beobachtung -> Vermutung -> Frage) und an den passenden Spezialisten dispatchen, bevor Nutzer-Eskalation erfolgt.

### Session-Memory-Protokoll (Pflicht)

1. Jede Session endet mit einer persistierten Memory-Notiz unter `Logs/Archive/SESSION_MEMORY_YYYY-MM-DD_<THEMA>.md`.
2. Inhalt mindestens: Kontext, geaenderte Dateien, Test-/Build-Status, Commit-IDs, offene Punkte.
3. Die Notiz wird per Dispatch referenziert (`mail post`), damit Folgeagenten sie in der Inbox sehen.
4. Session-Start (`/start`/`/takeover`) muss die neueste Session-Memory lesen, bevor neue Arbeit beginnt.

### Source-Link-Hygiene

1. Keine `file://`-Links.
2. Keine `%25xx`-Doppel-Encoding-Muster in Quellenpfaden.
3. Keine `[[index]]`-Platzhalter in Markdown-Link-Targets.
4. Quellenpfade in Referenzen bevorzugt als relative Pfad-Literale dokumentieren (portable, strict-build stabil).

### Bridge-Placeholder-Hygiene

1. Keine Brueckenartikel als Standardloesung fuer defekte Verweise.
2. Primärstrategie: vorhandenes kanonisches Ziel finden und Verweise dorthin korrigieren.
3. Temporäre Bruecken nur mit `bridge_mode`, `bridge_target`, `bridge_ticket`, `bridge_review_until`.
4. Pflicht-Check: `./7w_wiki.py test --suite bridge-placeholder-guard`.

### Reader-Stats-Hygiene

1. `./7w_wiki.py stats` erzeugt drei gekoppelte Artefakte:
   - `docs/Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md` (Leseransicht)
   - `Logs/INGESTION_TRACKING_REGISTER.md` (Tracking-Detail)
   - `Logs/Archive/STATS_SNAPSHOT_latest.json` (maschinenlesbare Schnittstelle)
2. Pflicht-Check: `./7w_wiki.py test --suite reader-stats-contract`.

### Pages-Integritaet

1. `./7w_wiki.py pages validate --json` ist die kanonische Site-Integritaetsprobe fuer MkDocs/Roamlinks.
2. Default: unresolved interne Links erscheinen als `WARN`, nicht als harter FAIL.
3. Routing: `WARN` bleibt ein sichtbares Health-Signal, erzwingt aber keinen `/tech_master`-Abzweig; Technician-first gilt fuer `FAIL`, `UNKNOWN` oder veraltete Pages-Snapshots.
4. Escalation: `./7w_wiki.py pages validate --json --strict-links` failt auf nicht-allowlistete unresolved Targets.
5. `./7w_wiki.py audit --pages` zieht denselben Site-Integritaetsstatus in den Audit.
6. `./7w_wiki.py repair --fix-roamlinks --auto` ist der aggressive, aber begrenzte Reparaturpfad fuer Pages-Linkdrift.
7. Der normative Volltext steht in [SY_DRIFT_PAGES_CONTRACT.md](Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md).
8. Policy-Datei: `.agent/config/pages_link_policy.json`.
9. Snapshot-Datei: `.agent/data/pages_health.json`.
10. Pages-Integritaet verhindert technischen Publishing-Drift; sie entscheidet keine Lore-Wahrheit gegen Homepage oder Quellen.

### Runtime-Konfiguration (zentral)

Gemeinsame Laufzeitparameter liegen in:

- `.agent/config/runtime.json`
- `.agent/config/pages_link_policy.json`

Aktuell genutzt fuer:

- Dispatch-Parallelitaet (`dispatch.parallel_settle_seconds`, `dispatch.parallel_retry_limit`)
- Oracle-Defaults (`oracle.device`, `oracle.batch_size`)
- Pages-Allowlist fuer unresolved Targets (`pages_link_policy.json`)

Reihenfolge bei Oracle:

1. CLI-Flags (z. B. `--cpu`) haben Vorrang.
2. `.agent/skills/oracle/config.json` (Legacy/Benchmark-kompatibel).
3. `.agent/config/runtime.json` (zentrale Defaults).

## Dokumentation und GitHub Pages

1. Autoritative Betriebsdokumente liegen in `System/`.
2. Fuer GitHub Pages werden sichtbare Eintraege in `docs/` und `mkdocs.yml` gepflegt.
2a. `docs/Siebenwind_Wiki/` ist die technische Pflegeflaeche fuer Wiki-Pages. Epistemische Wahrheit bleibt davon getrennt und folgt `Homepage > Quellen > Wiki Pages`; der Volltext steht in [SY_DRIFT_PAGES_CONTRACT.md](Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md).
3. **Pages-Deployment**: Die Seite wird ueber `.github/workflows/deploy.yml` bei `push` auf `main`, bei **Tags (`v*`)** und per `workflow_dispatch` gebaut.
4. **Release-Bundles**: Bundles werden nicht im Git-Verlauf oder auf `gh-pages` gespeichert. `.github/workflows/release-bundles.yml` baut sie nur fuer **Tags (`v*`)** und haengt sie als GitHub Release-Assets an.
5. **Lokales Packaging**: Entwickler erzeugen Bundles ueber `./7w_wiki.py package ...`; der Standard-Ausgabeort `dist/` bleibt ein Runtime-/Release-Artefakt und wird nicht versioniert.
6. Der `/tech_master`-Workflow ist die Pflichtstrecke fuer Doku-Paritaet, Runtime-Sync und Release-Hygiene.
7. `advisor` muss Pages-Freshness (`pages_health`, `last_sync_interop_at`) sichtbar machen, damit veraltete Tech-Hygiene frueh auffaellt.
8. `docs/assets/` ist die Live-Asset-Flaeche; `System/Design_Assets/` ist historischer Quellbestand, kein primaerer Publikationspfad.

## Verweise

- `System/Synapse_Board/SY_INTEROP.md`
- `System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md`
- `System/Synapse_Board/SY_DISPATCH.md`
- `System/Synapse_Board/SY_TESTING.md`
- `System/COORDINATION_HUB.md`
- `.agent/workflows/start.md`
