@AGENTS.md

## Notes for Claude Code

- `AGENTS.md` above is the single source of instructions for every agent in this repo; change rules there, not here.
- The MCP server is registered in `mcp_config.json`. To use it in Claude Code, add it to `.mcp.json` or run `claude mcp add siebenwind-wiki -- python3 System/MCP/server.py`.
- Skills live in `.agent/skills/*/SKILL.md`. Read the matching one before working on lore, style, translation or ingestion.
