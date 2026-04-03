# Session Memory: Advisor WARN Routing

- Date: 2026-04-03
- Focus: Technician-First-Routing fuer `Pages Health = WARN` lockern, die neue Routing-Semantik maschinenlesbar machen und die Onboarding-/Betriebstexte auf dieselbe Regel ziehen.

## Context
- Ausgangslage vor dem Lauf:
  - `advisor --json` meldete `Pages Health = WARN` und empfahl bei jedem `WARN` automatisch `/tech_master`.
  - `/start` und `/takeover` spiegelten dieselbe harte Regel in ihren Texten.
  - Der reale Restzustand war kein allgemeiner Technik-Blocker, sondern ein bekannter Residualzustand:
    - `audit --json`: `9` Issues
    - `bridge_inventory.invalid`: `4`
    - offene semantische Entscheidungen bereits per `MSG-2026-0089` / `MSG-2026-0090` eskaliert.
- Ziel der Session:
  - `WARN` sichtbar lassen, aber nicht mehr pauschal als Technician-Pflicht behandeln.
  - `FAIL`, `UNKNOWN` und veraltete Pages-Snapshots weiterhin als harten Technician-Trigger erhalten.

## What Changed
- Runtime:
  - `.agent/scripts/advisor.py`
    - zentrale Routing-Klassifikation `classify_tech_master_routing(...)` eingefuehrt.
    - `advisor --json` um `routing.tech_master.mode`, `routing.tech_master.trigger` und `routing.tech_master.command` erweitert.
    - menschenlesbare Empfehlungen angepasst:
      - `WARN` => advisory
      - `FAIL` / `UNKNOWN` / stale => `/tech_master` required
      - bei Konsistenzproblemen + `WARN` kein erzwungener `/tech_master`-Nachsatz mehr.
- Vertrags-/Testoberflaeche:
  - `.agent/tests/suites/json-interop-contract.json`
    - neue Assertions fuer `routing.tech_master.*`.
- Dokumentation:
  - `.agent/workflows/start.md`
  - `.agent/workflows/takeover.md`
  - `System/AGENT_OPERATIONS_HANDBOOK.md`
  - alle drei beschreiben nun dieselbe Routing-Regel wie die Runtime.
- Session-/Projektprotokolle:
  - `CHANGELOG.md`
  - `MASTER_TASK_LIST.md`
  - `System/Synapse_Board/DISPATCH/MSG-2026-0093_advisor_routing_relaxed_for_pages_warn.md`
- Workflow-closeout-Artefakte:
  - `./7w_wiki.py stats` aktualisierte:
    - `docs/Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md`
    - `Logs/INGESTION_TRACKING_REGISTER.md`
    - `Logs/Archive/STATS_SNAPSHOT_latest.json`
    - `Logs/Archive/STATS_SNAPSHOT_2026-04-03_183302.json`
  - `./7w_wiki.py test --suite all` aktualisierte Runtime-/Analyseartefakte unter `.agent/data/` (Backlog-Board, Cache-Dateien, Wiki-Inventar-Historie).

## Verification
- Zielgerichtete Implementierungschecks:
  - `./7w_wiki.py test --suite json-interop-contract`
  - `./7w_wiki.py test --suite clean-client-state`
  - `./7w_wiki.py test --suite interop-doc-links`
  - `./7w_wiki.py advisor --json`
  - `./7w_wiki.py start`
- Handover-Pflichtlauf:
  - `./7w_wiki.py stats`
  - `./7w_wiki.py archive rotate`
  - `./7w_wiki.py tech --manifest`
  - `./7w_wiki.py test --suite all`
    - Report-Verzeichnis: `/var/folders/m0/28md0wx56p7d_3y66c75ggfc0000gn/T/7w_test_qustn8w3/`
  - `./7w_wiki.py mail inbox --status OPEN`
- Pages-Snapshot im Schlusszustand:
  - `.agent/data/pages_health.json`
    - `generated_at`: `2026-04-03T18:35:42Z`
    - `pages_health.status`: `WARN`
    - `drift_status`: `PASS`
    - `unresolved_total`: `683`
    - `unallowlisted_total`: `681`

## Result
- `advisor --json` zeigt im Schlusszustand:
  - `routing.tech_master.mode = "advisory"`
  - `routing.tech_master.trigger = "pages_warn"`
  - `routing.tech_master.command = "./7w_wiki.py pages validate --json --strict-links"`
- `/start` und `/takeover` zwingen bei `WARN` nicht mehr automatisch in den Technician-Pfad.
- `FAIL`, `UNKNOWN` und veraltete Pages-Snapshots bleiben weiterhin explizit Technician-first.
- `./7w_wiki.py test --suite all`: `PASS`
- Diese Session war rein technisch/organisatorisch. Es wurden keine neuen Lore-Fakten eingefuehrt und keine epistemischen Entscheidungen gegen Homepage oder Quellen getroffen.

## Remaining Blockers
- Unveraendert offen:
  - `docs/Siebenwind_Wiki/00_Fundament/00_Religion_Uebersicht.md`
  - `docs/Siebenwind_Wiki/00_Fundament/03_Gesellschaft.md`
  - `docs/Siebenwind_Wiki/00_Fundament/Arman_von_Draconis.md`
  - `docs/Siebenwind_Wiki/00_Fundament/Werke_index.md`
- Routing-seitig bewusst **nicht** angefasst:
  - Gesamtstatus von `advisor` bleibt bei `Pages WARN` weiterhin `DEGRADED`.
  - `pages_health.status` selbst wurde nicht umbenannt oder neu semantisiert; nur die Routing-Interpretation wurde gelockert.

## Notes / Next Agent
- Wenn weitere Onboarding-/Meta-Dokumente implizit noch `WARN => /tech_master` unterstellen, koennen sie jetzt auf dieselbe advisory-Regel nachgezogen werden.
- Die durch `stats` und `test --suite all` aktualisierten `.agent/data/`-Artefakte sind technischer Beifang dieser Session und sollten vor spaeteren Commits bewusst mitgeprueft werden.
- Die eigentliche operative P1 bleibt der `Residual Bridge Decision Gate`; diese Session hat nur die Start-/Advisor-Navigation fuer nicht-blockierende `WARN`-Zustaende praezisiert.
