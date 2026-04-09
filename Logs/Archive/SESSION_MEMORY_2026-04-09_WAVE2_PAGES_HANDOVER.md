# Session Memory: Wave 2 Pages Handover 2026-04-09

- Datum: 2026-04-09
- Abschlussrolle: Oberarchivar
- Aktive Lane vor Handover: Technik / Interop / Pages-Haertung

## Abgeschlossene Arbeit in dieser Session
- Wave 2 der Pages-/Public-Surface-Haertung umgesetzt: der physische Root-Baum `Siebenwind_Wiki/` wurde entfernt, ohne den publizierten URL-/Nav-Segmentnamen `Siebenwind_Wiki/...` unter `docs/` anzutasten.
- Deterministischen Vertragsmodus `./7w_wiki.py pages validate --contract --json` eingefuehrt; der langsame Operator-Pfad `pages validate --json` bzw. `--fast` bleibt weiter verfuegbar.
- Maschinenoberflaechen auf finalen Root-Retirement-Status gehoben: `legacy_wiki_root = null`, `legacy_root_status = "removed"` in Pages-Report, Advisor und `lore_manifest.json`.
- Aktive Skripte, Prompts und Konflikt-/Research-Metadaten auf `docs/Siebenwind_Wiki/...` bzw. explizite Test-Fixtures umgestellt; Twin-Tree-Annahmen aus der Reparaturlogik entfernt.
- Entwurfs-Assets aus `docs/assets/design_proposals/` in `System/Design_Assets/design_proposals/2026-04-wave2/` verschoben; `docs/assets/` ist nun produktions-/publikationsorientiert.
- Neue Wave-2-Suites eingefuehrt: `pages-contract-mode-contract`, `pages-full-smoke`, `root-tree-retirement-contract`, `styling-surface-contract`.
- `MASTER_TASK_LIST.md` auf den realen Restbestand umgestellt: Arman-Bridge ist nicht mehr P1; offener Fokus sind jetzt Layout-Vertragsreste, `Zeitstrahl`, semantischer Pages-Backlog und offene Historian-/Forum-Spuren.

## Wichtige Ergebnisse
- `bridge_inventory.invalid = 0`; der fruehere Restfall `Arman_von_Draconis` ist durch `MSG-2026-0089` / `MSG-2026-0099` geklaert und zeigt temporaer auf `[[Arman]]`.
- `pages validate --contract --json` ist jetzt CI-tauglich und schreibt keine repo-getrackten Snapshots.
- `pages-full-smoke` und `test --suite all` liefen gruen; die Root-/Asset-/Styling-Vertraege sind aktiv.
- `advisor --json` bleibt `DEGRADED`, aber nun aus echten Restbestandsgruenden:
  - `Pages WARN`
  - `637` unresolved / `637` unallowlisted
  - `625 needs_historian`
  - `5 generic_term_conflict`
  - `forum_scan_stale = 3`
- `audit --json` meldet `27` Issues; sichtbar ausgewiesen sind `26` `legacy_field: layout`-Verletzungen. Dieser Delta-Zaehler sollte im naechsten Technikpass explizit verifiziert werden.

## Relevante Artefakte
- `MASTER_TASK_LIST.md`
- `CHANGELOG.md`
- `lore_manifest.json`
- `.agent/scripts/pages_tool.py`
- `.agent/scripts/pages_integrity.py`
- `.agent/scripts/advisor.py`
- `.agent/tests/suites/pages-contract-mode-contract.json`
- `.agent/tests/suites/pages-full-smoke.json`
- `.agent/tests/suites/root-tree-retirement-contract.json`
- `.agent/tests/suites/styling-surface-contract.json`
- `System/Design_Assets/design_proposals/2026-04-wave2/`
- `System/Synapse_Board/DISPATCH/MSG-2026-0117_wave_2_complete_pages_contract_mode_and_root_tree_retirement.md`

## Validierung
- `python3 -m py_compile .agent/scripts/advisor.py .agent/scripts/content_contract.py .agent/scripts/generate_lore_manifest.py .agent/scripts/pages_integrity.py .agent/scripts/pages_tool.py .agent/scripts/repair.py .agent/scripts/repo_hygiene.py .agent/scripts/sync_runtime_docs.py .agent/scripts/test_runner.py 7w_wiki.py`
- `./7w_wiki.py tech --sync-interop`
- `./7w_wiki.py tech --manifest`
- `./7w_wiki.py tech --repo-hygiene --apply --json`
- `./7w_wiki.py stats`
- `./7w_wiki.py archive rotate`
- `./7w_wiki.py advisor --json`
- `./7w_wiki.py audit --json`
- `./7w_wiki.py start --list-reviews`
- `./7w_wiki.py mail inbox --status OPEN`
- `./7w_wiki.py test --suite all`
- `./7w_wiki.py test --suite pages-full-smoke`

## Offene Punkte fuer den naechsten Agenten
- **P1: Layout-Contract Cleanup**: Die verbleibenden Audit-Verstoesse sind aktuell fast vollstaendig auf `layout`-Altfelder konzentriert. Zuerst die betroffenen Seiten bereinigen und dabei pruefen, ob der `27`→`26`-Delta ein Audit-Aggregationsfehler ist.
- **P1: Zeitstrahl Structural Repair**: `docs/Siebenwind_Wiki/05_Geschichte/Zeitstrahl.md` bleibt strukturell beschaedigt und ist noch kein rein mechanischer Linkfix.
- **P1/P2: Semantic Pages Backlog**: Nicht blind `repair --fix-roamlinks --auto` auf den ganzen Restbestand werfen. Die `625 needs_historian` und `5 generic_term_conflict` ueber bestehende Cluster-/Research-Artefakte (`.agent/data/backlog_cluster_board.json`, `.agent/data/backlog_escalations.json`, `RESEARCH-2026-018`) bearbeiten.
- **P2: Historian Reviews**: `RESEARCH-2026-004` und `RESEARCH-2026-007` stehen weiter auf `IN_REVIEW_HISTORIAN`. Naechster Agent soll entscheiden, ob Freigabe/Publikation oder Rueckfrage noetig ist.
- **P2: Forum-Pipeline**: `advisor --json` meldet `forum_scan_stale = 3`; die allowlisteten Boards wurden laenger nicht mehr gescannt.
- Die Dispatch-Queue ist weiterhin gross (`60 OPEN`); nichts davon wurde stillschweigend geschlossen. Fuer echte Inhaltsarbeit zuerst relevante OPEN-Nachrichten lesen, statt den gesamten Altbestand umzuraeumen.

## Empfohlene Startsequenz fuer den Nachfolger
1. `./7w_wiki.py advisor --json`
2. `./7w_wiki.py audit --json`
3. `./7w_wiki.py start --list-reviews`
4. `./7w_wiki.py mail read MSG-2026-0099`
5. Je nach Lane:
   - Technik: `./7w_wiki.py repair --fix-roamlinks --dry-run` nur fuer mechanische Kandidaten und danach gezielter Layout-/Zeitstrahl-Pass
   - Historian: `RESEARCH-2026-004`, `RESEARCH-2026-007`, `RESEARCH-2026-018` priorisieren
