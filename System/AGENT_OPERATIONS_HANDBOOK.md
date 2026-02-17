---
uuid: 1b3c8f24-7fb5-4ec3-9d43-7b1f17f69371
status: ACTIVE
updated_at: 2026-02-17T23:46:00Z
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

**Automatisierung**: Die Workflows `/handover` und `/takeover` fuehren Standard-Checks (Inbox, Clean-State, Stats) automatisch aus (`// turbo`).

## Runtime Commands
- `advisor`, `archive`, `audit`, `check`, `handover`, `historian`, `index`, `index-pages`, `inquisition`, `leitpunkt`, `mail`, `pages`, `repair`, `sanitize`, `score`, `scout`, `search`, `start`, `stats`, `takeover`, `test`, `translate`, `watch`

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
4. `./7w_wiki.py test --suite source-link-hygiene`
5. `./7w_wiki.py test --suite process-dispatch-curiosity`
6. `./7w_wiki.py test --suite bridge-placeholder-guard`
7. `./7w_wiki.py test --suite reader-stats-contract`
8. Optional Gesamtlauf: `./7w_wiki.py test --suite all`

Defect-Regel:

1. Bei FAIL zuerst Kommunikationsartefakt erzeugen (Dispatch oder Task).
2. Fixes nur auf geclaimte Defects.
3. Nach Fix immer Re-Test + Changelog-Verweis auf Message-ID/Task-ID.

Referenz: `System/Synapse_Board/SY_TESTING.md`

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
   - `Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md` (Leseransicht)
   - `Logs/INGESTION_TRACKING_REGISTER.md` (Tracking-Detail)
   - `Logs/Archive/STATS_SNAPSHOT_latest.json` (maschinenlesbare Schnittstelle)
2. Pflicht-Check: `./7w_wiki.py test --suite reader-stats-contract`.

### Runtime-Konfiguration (zentral)

Gemeinsame Laufzeitparameter liegen in:

- `.agent/config/runtime.json`

Aktuell genutzt fuer:

- Dispatch-Parallelitaet (`dispatch.parallel_settle_seconds`, `dispatch.parallel_retry_limit`)
- Oracle-Defaults (`oracle.device`, `oracle.batch_size`)

Reihenfolge bei Oracle:

1. CLI-Flags (z. B. `--cpu`) haben Vorrang.
2. `.agent/skills/oracle/config.json` (Legacy/Benchmark-kompatibel).
3. `.agent/config/runtime.json` (zentrale Defaults).

## Dokumentation und GitHub Pages

1. Autoritative Betriebsdokumente liegen in `System/`.
2. Fuer GitHub Pages werden sichtbare Eintraege in `docs/` und `mkdocs.yml` gepflegt.
3. **Deployment**: Die Seite wird NICHT mehr automatisch bei Push gebaut. Deployment erfolgt nur bei **Tags (`v*`)** oder manuellem `workflow_dispatch`.
4. Der `/docs`-Workflow ist die Pflichtstrecke fuer Doku-Paritaet.

## Verweise

- `System/Synapse_Board/SY_INTEROP.md`
- `System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md`
- `System/Synapse_Board/SY_DISPATCH.md`
- `System/Synapse_Board/SY_TESTING.md`
- `System/COORDINATION_HUB.md`
- `.agent/workflows/start.md`
