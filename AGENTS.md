# 🤖 Siebenwind Wiki: Agent Protocols

> **Canonical Entry Point for Autonomous Agents**
> *Compatible with: Google Jules, OpenAI Codex, Gemini CLI, Antigravity*

## 🎯 Mission Statement
You are operating on the **Siebenwind Wiki**, a 20-year-old collaborative world-building project. Your goal is to preserve its history while modernizing its infrastructure.
**Repository Root:** `/Users/alexandrerabe/siebenwind/7w_wiki`

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
| `search <query>` | Semantic RAG search (The Oracle). | `.agent/skills/oracle` |
| `audit` | Consistency check (duplicates, orphans). | `.agent/scripts/register_check.py` |
| `repair` | Interactive fix for audit findings. | `.agent/scripts/repair.py` |
| `historian <topic>` | Deep lore analysis & reconstruction. | `.agent/workflows/historian.md` |
| `mail` | Agent-to-Agent messaging (Dispatch). | `System/Synapse_Board/DISPATCH` |
| `inquisition` | Batch ingestion of legacy sources. | `Silicon Inquisition` |
| `stats` | Generate project statistics. | `.agent/scripts/generate_wiki_stats.py` |

## 📂 Documentation Map

-   **Governance**: [SY_INTEROP.md](System/Synapse_Board/SY_INTEROP.md) (Interop Standards)
-   **Coordination**: [COORDINATION_HUB.md](System/COORDINATION_HUB.md) (Registry)
-   **Workflows**: `.agent/workflows/*.md` (Standard Operating Procedures)
-   **Personas**: `.agent/instructions/*.md` (Role definitions)

## 🚀 How to Work Here (Standard Loop)

1.  **Orient**: Run `./7w_wiki.py advisor` to see the current situation.
2.  **Plan**: Check `MASTER_TASK_LIST.md` and `task.md` (if available).
3.  **Execute**: Use `7w_wiki.py` tools. Do NOT edit `7w_wiki.py` unless assigned to "DevOps".
4.  **Verify**: Run `./7w_wiki.py audit` before committing.
5.  **Log**: Update `CHANGELOG.md` or `Logs/` as appropriate.

---
*Generated: 2026-02-16 | Standard: v1.0 (Jules-Ready)*
