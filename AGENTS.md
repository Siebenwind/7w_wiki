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
    -   Use `.agents/skills/` for discoverable skills (Codex/Jules).

## 🛠️ Command Registry (Executable Capabilities)

Use `./7w_wiki.py <command>` for all operations.

| Command | Purpose | Context |
| :--- | :--- | :--- |
| `advisor` | **START HERE.** System status & next steps. | `System/Advisor` |
| `start` | Interactive onboarding workflow. | `.agent/workflows/start.md` |
| `test [--suite <name>|all]` | Run standardized interoperability and clean-state test suites. | `.agent/scripts/test_runner.py` |
| `takeover` | Show takeover protocol (`/takeover`) for session adoption. | `.agent/workflows/takeover.md` |
| `handover` | Show handover protocol (`/handover`) for session transfer. | `.agent/workflows/handover.md` |
| `search <query> [--source wiki\|quellen\|all]` | Semantic RAG search (The Oracle) with explicit source scope. | `.agent/skills/oracle` |
| `historian [query]` | Deep lore analysis (workflow or direct topic run). | `.agent/workflows/historian.md` |
| `audit` | Consistency check (duplicates, orphans). | `.agent/scripts/register_check.py` |
| `repair` | Interactive fix for audit findings. | `.agent/scripts/repair.py` |
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
| `stats` | Generate project statistics. | `.agent/scripts/generate_wiki_stats.py` |
| `tech` | Show Technician workflow (DevOps logic). | `.agent/workflows/tech.md` |

## 📂 Documentation Map

-   **Governance**: [SY_INTEROP.md](System/Synapse_Board/SY_INTEROP.md) (Interop Standards)
-   **Coordination**: [COORDINATION_HUB.md](System/COORDINATION_HUB.md) (Registry)
-   **Operations Overview**: [AGENT_OPERATIONS_HANDBOOK.md](System/AGENT_OPERATIONS_HANDBOOK.md) (Agents, Skills, Workflows, Dispatch)
-   **Testing Protocol**: [SY_TESTING.md](System/Synapse_Board/SY_TESTING.md) (Suites, Defect-Flow, Agent Mentality)
-   **Workflow-CLI Bridge**: [SY_WORKFLOW_CLI_MATRIX.md](System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md)
-   **Workflows**: `.agent/workflows/*.md` (Standard Operating Procedures)
-   **Personas**: `.agent/instructions/*.md` (Role definitions)

## 🚀 How to Work Here (Standard Loop)

1.  **Onboard**: Run `./7w_wiki.py start`, `./7w_wiki.py advisor`, and `./7w_wiki.py mail inbox --status OPEN` first.
2.  **Plan**: Check `MASTER_TASK_LIST.md` and `task.md` (if available).
3.  **Execute**: Use `7w_wiki.py` tools. Do NOT edit `7w_wiki.py` unless assigned to "DevOps".
4.  **Verify**: Run `./7w_wiki.py audit` and `./7w_wiki.py test --suite clean-client-state` before committing.
5.  **Log**: Update `CHANGELOG.md` or `Logs/` as appropriate.

## 🔎 Oracle Source Policy

For any non-trivial research, run the Oracle with explicit source scope:
- `--source wiki` for curated wiki facts
- `--source quellen` for raw source corpus
- `--source all` for combined cross-checking

---
*Generated: 2026-02-16 | Standard: v1.1 (Interop-Aligned)*
