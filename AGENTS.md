# Siebenwind Wiki: Instructions for the Archive's Agents

You are working in the archive of **Siebenwind**, a fantasy world built together by its players for more than twenty years. Treat it like an old library: preserve what the chroniclers wrote, keep the shelves in order, and never invent what the sources do not say.

## The Laws of the Archive

1. **One runtime.** All operations go through `./7w_wiki.py`. Do not write ad-hoc scripts or `sed`/`awk` pipelines for logic the CLI already covers. Edit `7w_wiki.py` itself only when the task is about the tooling.
2. **Truth flows downward.** Epistemic precedence is `Homepage > Quellen > Wiki Pages`. `docs/Siebenwind_Wiki/` is the edit and publishing tree, not the highest authority. When sources conflict, reconcile the wiki upward; mark gaps with `[UNGEKLÄRT]` instead of filling them. The full rule lives in [SY_DRIFT_PAGES_CONTRACT.md](System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md).
3. **Clean links.** Use `[[WikiLinks]]` between articles and repo-relative paths (`System/...`) in documentation. Never use absolute or `file://` paths.
4. **No Bridge-Placeholders by Default.** Repair a broken link by pointing it at the real target. Do not ship generic stub pages as a fix. A temporary bridge needs `bridge_mode`, `bridge_target`, `bridge_ticket` and `bridge_review_until` in its frontmatter.
5. **Machine-readable first.** Prefer `--json` output (`advisor --json`, `audit --json`, `pages validate --json`) over parsing human text.
6. **Ask, don't guess.** If you stumble on an anomaly outside your task, or sources contradict each other, raise it as a question instead of silently deciding (question-first).
7. **Register new system files** in [COORDINATION_HUB.md](System/COORDINATION_HUB.md).

<!-- BEGIN GENERATED DRIFT CONTRACT REFERENCE -->
> Generated reference block. The surrounding narrative text remains manually maintained.
> Canonical contract: [SY_DRIFT_PAGES_CONTRACT.md](System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md)
>
> - Epistemic precedence: `Homepage > Quellen > Wiki Pages`.
> - `docs/Siebenwind_Wiki/` is the technical edit/publish tree, not the highest truth source.
> - Technical drift is validated via `./7w_wiki.py sanitize`, `./7w_wiki.py audit`, and `./7w_wiki.py pages validate --json [--strict-links]`.
> - Deterministic contract/CI checks use `./7w_wiki.py pages validate --contract --json`.
> - `--strict` hardens the MkDocs build; `--strict-links` is the hard unresolved-link gate.
> - Generated command registries are synced by `./7w_wiki.py tech --sync-docs` / `--sync-interop`; narrative rules live in the canonical contract.
<!-- END GENERATED DRIFT CONTRACT REFERENCE -->

## How to Work Here

1. **Arrive.** Run `./7w_wiki.py start` and `./7w_wiki.py advisor`. For longer work, also check `./7w_wiki.py mail inbox --status OPEN` and read the latest `Logs/Archive/SESSION_MEMORY_*.md`.
2. **Plan.** Open tasks live in `MASTER_TASK_LIST.md` and, if present, `task.md`.
3. **Work.** Before editing lore, classify the drift (homepage, Quellen or wiki page) and check the higher source first. For research, run the Oracle with an explicit scope: `search <query> --source wiki|quellen|all`.
4. **Verify.** Run `./7w_wiki.py audit` and `./7w_wiki.py test --suite all` before committing. If the published site or navigation changed, also run `./7w_wiki.py pages validate --json` and `./7w_wiki.py test --suite pages-full-smoke`.
5. **Record.** Note notable changes in `CHANGELOG.md`. Multi-step campaigns (ingestion runs, Historian runs, releases) send status heartbeats via `mail post` while they run and close with `Logs/Archive/SESSION_MEMORY_YYYY-MM-DD_<THEMA>.md`. Small, self-contained tasks need neither.

Build bundles under `dist/` are release artifacts and are never committed.

## Command Registry

<!-- BEGIN GENERATED COMMAND REGISTRY -->
| Command | Purpose | Context |
| :--- | :--- | :--- |
| `search <query> [remaining...]` | Semantic RAG search (Oracle) across wiki and source corpus. | `.agent/skills/oracle/search.py` |
| `start [--run]` | Show or run the onboarding workflow. | `.agent/workflows/start.md` |
| `test` | Run interoperability and clean-state test suites. | `.agent/scripts/test_runner.py` |
| `takeover [--run]` | Show or run the takeover workflow. | `.agent/workflows/takeover.md` |
| `handover [--run]` | Show or run the handover workflow. | `.agent/workflows/handover.md` |
| `historian [args...]` | Deep lore analysis workflow, direct topic run, and research review operations. | `.agent/workflows/historian.md` |
| `repair` | Interactive or automatic repair of audit findings, including Pages / Roamlinks fixes. | `.agent/scripts/repair.py` |
| `audit` | Run consistency audit for duplicates, broken links, and orphaned content. | `.agent/scripts/register_check.py` |
| `index` | Manage the semantic search index. | `.agent/skills/oracle/build_index.py` |
| `index-pages` | Generate category index pages for the wiki. | `.agent/scripts/generate_wiki_indices.py` |
| `pages <status|setup|serve|verify-live|build|validate|backlog>` | Build, validate, and inspect GitHub Pages documentation and backlog health. | `.agent/scripts/pages_tool.py` |
| `advisor` | Show system status and recommended next actions. | `System/Advisor` |
| `inquisition` | Run batch ingestion of legacy sources. | `.agent/scripts/inquisition.py` |
| `sanitize [target]` | Normalize structure, H1 usage, and frontmatter. | `.agent/scripts/wiki_sanitizer.py` |
| `lint [target]` | Run the combined lint pipeline. | `.agent/scripts/lint_tool.py` |
| `score <file>` | Calculate Lore Quality Score for one markdown file. | `.agent/scripts/lore_score_manager.py` |
| `ingest [args...]` | Run ingestion workflows, including forum queue, inspection, drafting, finalization, and legacy technical checks. | `.agent/scripts/ingest_pipeline.py` |
| `translate [args...]` | Translate Falandric texts or manage dictionaries. | `.agent/scripts/translator.py` |
| `watch` | Start the live watcher for index updates. | `.agent/scripts/watcher.py` |
| `package` | Build archive-first install bundles for supported platforms. | `.agent/scripts/package_tool.py` |
| `check [path]` | Run style and grammar checks. | `.agent/skills/lektor/style_checker.py` |
| `archive <sync|rotate|unpack>` | Manage archive symlinks, rotation, and unpack operations. | `docs/Archiv` |
| `mail <post|inbox|read|claim|done|classify>` | Interact with the dispatch system using structured subcommands. | `System/Synapse_Board/SY_DISPATCH.md` |
| `scout` | Promoted discovery entrypoint for external source scanning. | `.agent/scripts/forum_scanner.py` |
| `tech` | Show the technician workflow or run interop maintenance helpers. | `.agent/workflows/tech_master.md` |
| `version` | Show or bump the wiki standard version. | `.agent/scripts/version_manager.py` |
| `antigravity` | Deprecated alias for start workflow overview. | `.agent/workflows/antigravity.md` |
| `leitpunkt <view|status|check|scaffold>` | Manage the human maintainer standpoint workflow. | `.agent/scripts/leitpunkt_tool.py` |
| `stats` | Generate reader-facing stats and machine snapshots. | `.agent/scripts/generate_wiki_stats.py` |
| `mcp` | Start the MCP server for structured agent access. | `System/MCP/server.py` |
<!-- END GENERATED COMMAND REGISTRY -->

## Where Things Live

- **Canonical core:** `.agent/` (scripts, skills, workflows, personas, data) and `./7w_wiki.py`.
- **Discovery catalog:** `.agent/catalog/catalog.v1.json`. `lore_manifest.json` and `.agent/config/tools.json` are generated from it.
- **Codex adapters:** `.agents/skills/` and `.codex/config.toml` are thin generated pointers into `.agent/`. Do not edit them by hand; regenerate with `./7w_wiki.py tech --sync-surfaces` (or `--sync-interop` for everything).
- **MCP server:** `./7w_wiki.py mcp` exposes the CLI as typed tools plus the catalog as `wiki://` resources; clients find it via `mcp_config.json`. See [System/MCP/README.md](System/MCP/README.md). The `wiki_mail_quip` tool is there for in-character banter between agents; use it freely.
- **Workflows and personas:** `.agent/workflows/*.md` and `.agent/instructions/*.md`.

Deeper reading, when a task needs it:

- [AGENT_OPERATIONS_HANDBOOK.md](System/AGENT_OPERATIONS_HANDBOOK.md): agents, skills, dispatch, session memory
- [SY_INTEROP.md](System/Synapse_Board/SY_INTEROP.md): interop standards
- [SY_TESTING.md](System/Synapse_Board/SY_TESTING.md): test suites and defect flow
- [SY_WORKFLOW_CLI_MATRIX.md](System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md): which workflow maps to which command
- [SY_DISPATCH.md](System/Synapse_Board/SY_DISPATCH.md): the mail/dispatch system
