---
uuid: 52af70d6-90f7-4201-9374-c6cc2ce0c57e
status: ACTIVE
epistemic: "#meta"
---

# SY_WORKFLOW_CLI_MATRIX

Zweck: Abgleich zwischen historisch gewachsenen Slash-Workflows und tatsaechlich ausfuehrbaren CLI-Kommandos im kanonischen Core.

## Runtime Commands

<!-- BEGIN GENERATED RUNTIME COMMANDS -->
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
<!-- END GENERATED RUNTIME COMMANDS -->

## Adaptermatrix

| Workflow-Slash | Status | Runtime-Adapter | Hinweis |
|---|---|---|---|

<!-- BEGIN GENERATED ADAPTER ROWS -->
| `/start` | executable | `7w_wiki.py start [--run]` | `7w_wiki.py start` shows the workflow by default; `--run` executes the checklist; `--resume` resumes workflow state. |
| `/takeover` | executable | `7w_wiki.py takeover [--run]` | `7w_wiki.py takeover` shows the workflow by default; `--run` executes the checklist; `--resume` resumes workflow state. |
| `/handover` | executable | `7w_wiki.py handover [--run]` | `7w_wiki.py handover` shows the workflow by default; `--run` executes the checklist; `--resume` resumes workflow state. |
| `/scout` | executable | `7w_wiki.py scout` | Promoted discovery entrypoint; intentionally first-class for external source discovery. Backend implementation remains under `.agent/scripts/`. |
| `/antigravity` | executable | `7w_wiki.py antigravity` | Deprecated compatibility alias. `./7w_wiki.py antigravity` now prints a deprecation note and then shows `/start`. |
| `/decide` | method_only | `7w_wiki.py mail inbox --status OPEN + 7w_wiki.py mail read <id> + 7w_wiki.py mail claim <id> --agent <name> + 7w_wiki.py mail done <id> --agent <name>` | Hochgeschwindigkeits-Workflow für Nutzerentscheidungen (/decide) |
| `/delegate` | method_only | `7w_wiki.py start + 7w_wiki.py audit` | Delegation ist policy-driven und host-abhaengig. Die kanonische Konfiguration liegt in `.agent/config/delegation_policy.json`; Ausuebung ist optional. |
| `/forum_search` | executable | `7w_wiki.py scout --forum <allowlisted-board> --pages N` | Spezialisierter Betriebsweg fuer forum-basierte Quellenjagd; der promoted Umbrella-Workflow `/scout` bleibt fuer breitere Discovery zustaendig. |
| `/herold` | method_only | `7w_wiki.py stats` | Der "Herold von Siebenwind" – PR, Design & Außendarstellung |
| `/historian` | executable | `7w_wiki.py historian [query]` | `7w_wiki.py historian` shows this workflow by default; passing a query starts the Oracle-backed analysis handoff. |
| `/ingest_master` | method_only | `7w_wiki.py advisor + 7w_wiki.py search <query> --source wiki\|quellen\|all + 7w_wiki.py repair --check-collision "<Name>" + 7w_wiki.py ingest <file> [--move-to <dir>] + 7w_wiki.py mail inbox --status OPEN + 7w_wiki.py mail post --from Ingestor --to <agent\|ALL> --subject "<text>" --body "<text>" + 7w_wiki.py archive sync` | Method workflow for ingestion discipline; dispatch stays mandatory via inbox, question-first escalation, and status heartbeats. |
| `/lore_master` | method_only | `7w_wiki.py search <query> --source wiki\|quellen\|all + 7w_wiki.py historian <query> + 7w_wiki.py score <file> + 7w_wiki.py mail inbox --status OPEN + 7w_wiki.py mail post --from Historian --to <agent\|ALL> --subject "<text>" --body "<text>"` | Department Master Workflow für Lore-Forschung, Narrative und Kanon-Updates |
| `/meta_master` | method_only | `7w_wiki.py start + 7w_wiki.py stats + 7w_wiki.py leitpunkt [status\|check\|scaffold] + 7w_wiki.py test --suite reader-stats-contract + 7w_wiki.py test --suite clean-client-state + 7w_wiki.py test --suite pages-link-contract + 7w_wiki.py mail inbox --status OPEN + 7w_wiki.py mail post --from Coordinator --to <agent\|ALL> --subject "<text>" --body "<text>"` | Department Master Workflow für Projekt-Meta, Statistiken und Handover |
| `/qa_master` | method_only | `7w_wiki.py audit + 7w_wiki.py audit --pages + 7w_wiki.py repair [--full] + 7w_wiki.py repair --fix-roamlinks [--auto] [--dry-run] + 7w_wiki.py sanitize --auto + 7w_wiki.py test --suite clean-client-state + 7w_wiki.py test --suite pages-link-contract + 7w_wiki.py stats + 7w_wiki.py mail inbox --status OPEN + 7w_wiki.py mail post --from Guardian --to <agent\|ALL> --subject "<text>" --body "<text>"` | Universeller Master Workflow für Konsistenz, Links und Qualitätssicherung |
| `/tech_master` | method_only | `7w_wiki.py sanitize --auto + 7w_wiki.py package --platform ubuntu\|debian\|macos\|wsl --profile full\|agent-only + 7w_wiki.py pages status\|build\|validate + 7w_wiki.py pages validate --json [--strict-links] + 7w_wiki.py watch + 7w_wiki.py index --status + 7w_wiki.py audit --pages + 7w_wiki.py repair --fix-roamlinks [--auto] [--dry-run] + 7w_wiki.py repair --backlog-board [--json] + 7w_wiki.py repair --apply-lane1 [--auto] [--dry-run] [--json] + 7w_wiki.py mail inbox --status OPEN + 7w_wiki.py mail post --from Technician --to <agent\|ALL> --subject "<text>" --body "<text>" + 7w_wiki.py tech --sync-catalog + 7w_wiki.py tech --sync-codex-skills + 7w_wiki.py tech --sync-a2a + 7w_wiki.py tech --sync-surfaces + 7w_wiki.py tech --sync-matrix + 7w_wiki.py tech --sync-docs + 7w_wiki.py tech --sync-interop + 7w_wiki.py tech --repo-hygiene [--apply] [--json] + 7w_wiki.py tech --sync-bridges + 7w_wiki.py tech --manifest` | Department workflow for runtime-authoritative maintenance; helper scripts are implementation detail behind `7w_wiki.py tech`. |
| `/test_run` | method_only | `7w_wiki.py test --suite clean-client-state + 7w_wiki.py test --suite takeover-handover + 7w_wiki.py test --suite interop-doc-links + 7w_wiki.py test --suite interop-command-registry + 7w_wiki.py test --suite catalog-contract + 7w_wiki.py test --suite adapter-surfaces-contract + 7w_wiki.py test --suite delegation-policy-contract + 7w_wiki.py test --suite repo-hygiene-contract + 7w_wiki.py test --suite manifest-contract + 7w_wiki.py test --suite source-tree-contract + 7w_wiki.py test --suite legacy-doc-contract + 7w_wiki.py test --suite asset-surface-contract + 7w_wiki.py test --suite workflow-matrix-contract + 7w_wiki.py test --suite tool-manifest-contract + 7w_wiki.py test --suite pages-link-contract + 7w_wiki.py test --suite backlog-repair-contract + 7w_wiki.py test --suite source-link-hygiene + 7w_wiki.py test --suite process-dispatch-curiosity + 7w_wiki.py test --suite bridge-placeholder-guard + 7w_wiki.py test --suite reader-stats-contract + 7w_wiki.py test --suite all + 7w_wiki.py test --suite all --include-rag + 7w_wiki.py test --suite rag-relevance-smoke --timeout 30 + 7w_wiki.py test --suite all --post-failures --from-agent <name> --to-agent ALL --priority HIGH + 7w_wiki.py pages validate --json [--strict-links] + 7w_wiki.py mail inbox --status OPEN + 7w_wiki.py mail claim <id> --agent <name> + 7w_wiki.py mail done <id> --agent <name> --note "<abschluss>"` | Standardisierter Testdurchlauf fuer Interop, Takeover/Handover und Clean-Client-State |
| `/translate` | executable | `7w_wiki.py translate [args...]` | Falandrische Texte übersetzen & Sprachdatensätze pflegen |
| `/wiki_style_guide` | method_only | `7w_wiki.py check + 7w_wiki.py sanitize --auto` | Siebenwind Wiki Style Guide & Convention |
<!-- END GENERATED ADAPTER ROWS -->

## Regel
Neue Workflows muessen vor Aktivierung in diese Matrix eingetragen werden. 
**Auto-Update:** Die Runtime-Liste und Adapterzeilen werden ueber `./7w_wiki.py tech --sync-matrix` regeneriert.
Die Zeilen innerhalb der generierten Bloecke sind nicht manuell zu pflegen.
Die Matrix beschreibt Runtime-Adapter und technische Ausfuehrbarkeit. Epistemische Autoritaet wird nicht aus dem CLI-Ziel oder dem Edit-Baum abgeleitet, sondern im kanonischen Drift-/Pages-Vertrag und in `SY_INTEROP` gespiegelt. `antigravity` bleibt nur als deprecated Kompatibilitaetsalias sichtbar.
