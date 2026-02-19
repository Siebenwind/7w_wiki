# 🤖 Siebenwind Wiki: Agent Protocols

> **Canonical Entry Point for Autonomous Agents**
> *Compatible with: Google Jules, OpenAI Codex, Gemini CLI, Antigravity*

## 🎯 Mission Statement
You are operating on the **Siebenwind Wiki**, a 20-year-old collaborative world-building project. Your goal is to preserve its history while modernizing its infrastructure.
**Repository Root:** `.`

## 📜 The Golden Rules (Non-Negotiable)

1.  **Runtime Authority**: The **ONLY** executable interface is `./7w_wiki.py`. Do not create custom scripts or use `sed`/`awk` for complex logic.
2.  **Epistemic Integrity**: Never hallucinate lore. If information is missing, use tags like `[UNGEKLÄRT]`.
3.  **Link Hygiene**:
    -   **NO** absolute paths (`file://`).
    -   Use `[[WikiLinks]]` for knowledge base articles.
    -   Use repo-relative paths (`System/...`) for documentation.
4.  **Coordination Central**:
    -   Every new system file MUST be registered in `System/COORDINATION_HUB.md`.
    -   Use `System/Synapse_Board/` for conflict resolution.
5.  **Agent Interop**:
    -   Respect the folder structure: `.agent/` is for internal logic.
    -   Use `.agent/config/tools.json` for machine-readable tool discovery (OpenAI-compatible schema).
    -   Use `./7w_wiki.py --help-json` for dynamic CLI introspection.
6.  **Mission Report Protocol**:
    -   Every session or task MUST end with a status report via `mail done` (if working on a specific message) or `mail post` (for general updates).
    -   Reports must be concise but include: What was done, what was verified, and what is next.
7.  **Inquisitive Protocol**:
    -   If you find an anomaly unrelated to your current task, **ASK**. Do not ignore it.
    -   Use `mail post` to query the `Coordinator` or `Technician`.
8.  **Machine-Readable First**:
    -   When available, agents MUST use CLI commands with `--json` (e.g., `advisor --json`, `audit --json`) for reliable parsing.
    -   Output parsing of human-readable text is discouraged if a JSON flag exists.
9.  **No Bridge-Placeholders by Default**:
    -   Fix links to canonical targets first.
    -   Do not ship generic bridge/stub pages as final repairs.
    -   Temporary bridge exceptions require lifecycle metadata (`bridge_mode`, `bridge_target`, `bridge_ticket`, `bridge_review_until`).

## 🛠️ Command Registry (Executable Capabilities)

Use `./7w_wiki.py <command>` for all operations.

| Command | Purpose | Context |
| :--- | :--- | :--- |
| `advisor` | **START HERE.** System status & next steps. | `System/Advisor` |
| `start [--run]` | Interactive onboarding workflow. `--run` executes the checklist. | `.agent/workflows/start.md` |
| `test [--suite <name>|all] [--include-rag]` | Run standardized interoperability and clean-state test suites (`all` excludes `rag-relevance-smoke`). Validates `json-interop-contract`. | `.agent/scripts/test_runner.py` |
| `takeover [--run]` | Show takeover protocol (`/takeover`) for session adoption. `--run` executes the checklist. | `.agent/workflows/takeover.md` |
| `handover [--run]` | Show handover protocol (`/handover`) for session transfer. `--run` executes the checklist. | `.agent/workflows/handover.md` |
| `search <query> [--source wiki\|quellen\|all]` | Semantic RAG search (The Oracle) with explicit source scope. | `.agent/skills/oracle` |
| `historian [query]` | Deep lore analysis (workflow or direct topic run). | `.agent/workflows/historian.md` |
| `audit` | Consistency check (duplicates, orphans). | `.agent/scripts/register_check.py` |
| `repair [--auto\|--full]` | Interactive fix for audit findings; `--full` runs 1→3 in one pass. | `.agent/scripts/repair.py` |
| `sanitize [--auto]` | Structural normalization (layout, H1, frontmatter). | `.agent/scripts/wiki_sanitizer.py` |
| `check [path]` | Style and grammar checks (Lektor). Default target: `Siebenwind_Wiki`. | `.agent/skills/lektor/style_checker.py` |
| `score <file>` | Lore Quality Score (LQS) for one markdown file. | `.agent/scripts/lore_score_manager.py` |
| `index [--status] [--rebuild]` | Semantic index status or rebuild. | `.agent/skills/oracle/build_index.py` |
| `index-pages` | Generate `index.md` for wiki categories. | `.agent/scripts/generate_wiki_indices.py` |
| `pages status\|build\|validate` | Validate and build GitHub Pages docs via project-local mkdocs tooling. | `.agent/scripts/pages_tool.py` |
| `inquisition [--batch N] [--audit-only]` | Batch ingestion of legacy sources. | `Silicon Inquisition` |
| `translate ...` | Translation and dictionary operations. | `.agent/scripts/translator.py` |
| `watch` | Live watcher for real-time indexing. | `.agent/scripts/watcher.py` |
| `archive sync` | Sync archive symlinks into `docs/Archiv`. | `docs/Archiv` |
| `mail <subcommand...>` | Agent-to-agent dispatch (`post`, `inbox`, `read`, `claim`, `done`). | `System/Synapse_Board/SY_DISPATCH.md` |
| `scout [--forum bekanntmachungen\|news --pages N]` | Deep-scan external forum boards for signals. | `Scripts/forum_scanner.py` |
| `stats` | Generate reader-facing wiki status, tracking register, and machine snapshot. | `.agent/scripts/generate_wiki_stats.py` |
| `tech` | Show Technician workflow (DevOps logic). | `.agent/workflows/tech.md` |
| `antigravity` | Show core default protocol (`/antigravity`). | `.agent/workflows/antigravity.md` |
| `leitpunkt [view\|status\|check\|scaffold]` | Manage the human maintainer standpoint (workflow + validation). | `.agent/workflows/leitpunkt.md` |
| `mcp [--transport stdio\\|streamable-http] [--port N]` | Start MCP Server (structured tool interface for AI agents). | `System/MCP/server.py` |

## 📂 Documentation Map

-   **Governance**: [SY_INTEROP.md](System/Synapse_Board/SY_INTEROP.md) (Interop Standards)
-   **Coordination**: [COORDINATION_HUB.md](System/COORDINATION_HUB.md) (Registry)
-   **Operations Overview**: [AGENT_OPERATIONS_HANDBOOK.md](System/AGENT_OPERATIONS_HANDBOOK.md) (Agents, Skills, Workflows, Dispatch)
-   **Testing Protocol**: [SY_TESTING.md](System/Synapse_Board/SY_TESTING.md) (Suites, Defect-Flow, Agent Mentality)
-   **Workflow-CLI Bridge**: [SY_WORKFLOW_CLI_MATRIX.md](System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md)
-   **Workflows**: `.agent/workflows/*.md` (Standard Operating Procedures)
-   **Personas**: `.agent/instructions/*.md` (Role definitions)

## 🚀 How to Work Here (Standard Loop)

1.  **Onboard**: Run `./7w_wiki.py start`, `./7w_wiki.py advisor`, and `./7w_wiki.py mail inbox --status OPEN` first. Read the latest `Logs/Archive/SESSION_MEMORY_*.md` before starting new work.
2.  **Plan**: Check `MASTER_TASK_LIST.md` and `task.md` (if available).
3.  **Execute**: Use `7w_wiki.py` tools. Do NOT edit `7w_wiki.py` unless assigned to "DevOps". Send status heartbeats via `mail post` on long tasks and route contradictions as specialist questions (question-first).
4.  **Verify**: Run `./7w_wiki.py audit`, `./7w_wiki.py test --suite clean-client-state`, `./7w_wiki.py test --suite bridge-placeholder-guard`, and `./7w_wiki.py test --suite reader-stats-contract` before committing.
5.  **Log**: Update `CHANGELOG.md` or `Logs/` as appropriate. End each session with `Logs/Archive/SESSION_MEMORY_YYYY-MM-DD_<THEMA>.md` and reference it via `./7w_wiki.py mail post`.

## 🔎 Oracle Source Policy

For any non-trivial research, run the Oracle with explicit source scope:
- `--source wiki` for curated wiki facts
- `--source quellen` for raw source corpus
- `--source all` for combined cross-checking

---

## 🔌 MCP Server (Model Context Protocol)

An MCP server is available that wraps the entire CLI as structured, typed tools for AI agents.

- **Start**: `./7w_wiki.py mcp` (stdio) or `./7w_wiki.py mcp --transport streamable-http --port 7777` (network)
- **Auto-Discovery**: `mcp_config.json` at repo root for MCP-capable clients
- **Docs**: [System/MCP/README.md](System/MCP/README.md)
- **27 Tools** auto-generated from `--help-json` — zero maintenance
- **`wiki_mail_quip`**: You ARE encouraged to use this tool for in-character interagency commentary, humor, and personality. See `[QUIP]` tag in [SY_DISPATCH.md](System/Synapse_Board/SY_DISPATCH.md).

> **Dependency**: `pip install 'mcp[cli]'`

---
*Generated: 2026-02-19 | Standard: v1.2 (MCP-Enabled)*
