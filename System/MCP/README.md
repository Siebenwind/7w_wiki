# Siebenwind Wiki — MCP Server

> Model Context Protocol Server for AI Agent Integration

## Overview

This MCP server exposes the full `7w_wiki.py` CLI as structured tools for AI agents. It follows the **Thin Relay** principle: the server has no own logic — it delegates everything to the CLI entry point.

```
MCP Client (Antigravity / Gemini CLI / Codex / Claude)
       │
       ▼
  server.py (Thin Relay)
       │
       ▼
  ./7w_wiki.py <command> <args>
```

## Quick Start

### 1. Install Dependency

```bash
pip install 'mcp[cli]'
```

### 2. Start the Server

**Option A: stdio (for direct agent connection)**
```bash
python System/MCP/server.py
```

**Option B: HTTP (for network access / multi-agent)**
```bash
python System/MCP/server.py --transport streamable-http --port 7777
```

**Option C: Via CLI**
```bash
./7w_wiki.py mcp
```

### 3. Connect a Client

Add to your MCP client config (or use the `mcp_config.json` at the repo root):

```json
{
  "mcpServers": {
    "siebenwind-wiki": {
      "command": "python3",
      "args": ["System/MCP/server.py"]
    }
  }
}
```

## Architecture

### Dual-Mode Startup

The server supports two startup modes with automatic fallback:

1. **Standalone Daemon** (primary): Run via `launchd`, systemd, or manually. Always available.
2. **Agent-Embedded Fallback**: If no daemon is running, the agent starts the server itself.

When using HTTP transport, the server probes the port first. If already in use, it assumes another instance is running and exits gracefully.

### Auto-Extraction Pipeline

Tool definitions are **never maintained manually**. On every startup, the server runs `generate_mcp_tools.py`, which calls `./7w_wiki.py --help-json` and converts the CLI schema into MCP tool definitions.

**Add a new CLI command → it automatically appears as an MCP tool.**

### Oracle Availability Probe

The `wiki_search` tool depends on the Oracle (semantic RAG index). If the index is not ready, the server registers a **grep-based fallback** that performs basic text search across `Siebenwind_Wiki/`.

## Available Tools (27)

Generated automatically from the CLI. Key tools:

| Tool | CLI Command | Description |
|---|---|---|
| `wiki_advisor` | `advisor` | System status and next actions |
| `wiki_search` | `search` | Semantic RAG search (Oracle) |
| `wiki_audit` | `audit` | Consistency check |
| `wiki_stats` | `stats` | Wiki statistics |
| `wiki_mail` | `mail` | Agent-to-agent messaging |
| `wiki_mail_quip` | `mail post` | In-character interagency humor (`[QUIP]`) |
| `wiki_test` | `test` | Run test suites |
| `wiki_lint` | `lint` | Comprehensive lint pipeline |
| `wiki_check` | `check` | Style and grammar check |
| `wiki_repair` | `repair` | Auto-repair audit findings |
| `wiki_inquisition` | `inquisition` | Batch source ingestion |
| `wiki_historian` | `historian` | Deep lore analysis |

For the full list, run:
```bash
python System/MCP/generate_mcp_tools.py
```

## Resources

The server also exposes MCP resources (read-only data):

| URI | Description |
|---|---|
| `wiki://status` | Current system status (advisor output) |
| `wiki://dispatch/open` | Open dispatch messages |

## The `[QUIP]` System

Agents are **encouraged** to use `wiki_mail_quip` for in-character commentary. Quips are:
- Tagged `[QUIP]` in the dispatch system
- Limited to 280 characters
- Priority `LOW`, status `DONE` (no claim lifecycle)
- Stored in `System/Synapse_Board/DISPATCH/`

This creates a human-readable project diary with personality.

## Daemon Setup (macOS)

For always-on availability, create a LaunchAgent:

```bash
# ~/Library/LaunchAgents/com.siebenwind.mcp.plist
```

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.siebenwind.mcp</string>
    <key>ProgramArguments</key>
    <array>
        <string>python3</string>
        <string>/path/to/7w_wiki/System/MCP/server.py</string>
        <string>--transport</string>
        <string>streamable-http</string>
        <string>--port</string>
        <string>7777</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/path/to/7w_wiki</string>
    <key>KeepAlive</key>
    <true/>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
```

Then load it:
```bash
launchctl load ~/Library/LaunchAgents/com.siebenwind.mcp.plist
```

## File Overview

| File | Purpose |
|---|---|
| `server.py` | MCP Server (Thin Relay, dual-mode startup) |
| `generate_mcp_tools.py` | Auto-extraction pipeline (CLI → MCP tools) |
| `__init__.py` | Package init |
| `../../mcp_config.json` | Client auto-discovery config |

---
*Generated: 2026-02-19 · Standard: MCP v1.0*
