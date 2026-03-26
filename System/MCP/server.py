#!/usr/bin/env python3
"""
Siebenwind Wiki — MCP Server (Thin Relay)

A Model Context Protocol server that exposes the 7w_wiki.py CLI as
structured tools for AI agents (Antigravity, Gemini CLI, Codex, Claude).

Architecture:
  MCP Client → server.py (this file) → ./7w_wiki.py <command> → result

The server has NO own logic. It delegates everything to the CLI.
Tool definitions are auto-generated from `./7w_wiki.py --help-json`.

Usage:
  # Standalone daemon (primary)
  python System/MCP/server.py

  # Via CLI entry point
  ./7w_wiki.py mcp

  # With streamable HTTP transport (for network access)
  python System/MCP/server.py --transport streamable-http --port 7777
"""

import argparse
import json
import os
import shlex
import socket
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / ".agent" / "scripts"))

from content_contract import TECHNICAL_WIKI_ROOT

# Resolve repo root (System/MCP/server.py → ../../)
REPO_ROOT = Path(__file__).resolve().parents[2]
CLI_PATH = REPO_ROOT / "7w_wiki.py"

# --- Lazy SDK import (fail gracefully if not installed) ---

def _check_sdk():
    """Check if the MCP SDK is available, provide install instructions if not."""
    try:
        import mcp  # noqa: F401
        return True
    except ImportError:
        print(
            "╔══════════════════════════════════════════════════════╗\n"
            "║  MCP SDK not installed.                             ║\n"
            "║                                                     ║\n"
            "║  Install with:                                      ║\n"
            "║    pip install 'mcp[cli]'                           ║\n"
            "║                                                     ║\n"
            "║  Or in a venv:                                      ║\n"
            "║    python -m venv .venv && source .venv/bin/activate ║\n"
            "║    pip install 'mcp[cli]'                           ║\n"
            "╚══════════════════════════════════════════════════════╝",
            file=sys.stderr
        )
        return False


# ──────────────────────────────────────────────
# Tool Execution Engine
# ──────────────────────────────────────────────

def run_cli_command(cli_path: list[str], args: list[str], use_json: bool = False) -> str:
    """
    Execute a 7w_wiki.py command and return its output.

    This is the ONLY execution path. Everything goes through the CLI.
    Golden Rule #1: The ONLY executable interface is ./7w_wiki.py.
    """
    cmd = [sys.executable, str(CLI_PATH)] + cli_path + args
    if use_json:
        cmd.append("--json")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=str(REPO_ROOT),
            env={**os.environ, "PYTHONUNBUFFERED": "1"}
        )

        output = result.stdout.strip()
        if result.returncode != 0 and result.stderr:
            output += f"\n[stderr]: {result.stderr.strip()}"

        return output or "(no output)"

    except subprocess.TimeoutExpired:
        return f"[ERROR] Command timed out after 120s: ./7w_wiki.py {' '.join(cli_path)}"
    except Exception as e:
        return f"[ERROR] Failed to execute: {e}"


def probe_oracle() -> bool:
    """Check if the Oracle (semantic search) is available."""
    try:
        result = subprocess.run(
            [sys.executable, str(CLI_PATH), "index", "--status"],
            capture_output=True, text=True, timeout=10, cwd=str(REPO_ROOT)
        )
        return result.returncode == 0 and "READY" in result.stdout.upper()
    except Exception:
        return False


# ──────────────────────────────────────────────
# Tool Definition Loading
# ──────────────────────────────────────────────

def load_tool_definitions() -> list[dict]:
    """
    Load tool definitions from the auto-extraction pipeline.
    Falls back to a minimal set if extraction fails.
    """
    generator = Path(__file__).parent / "generate_mcp_tools.py"
    try:
        result = subprocess.run(
            [sys.executable, str(generator)],
            capture_output=True, text=True, timeout=15, cwd=str(REPO_ROOT)
        )
        if result.returncode == 0:
            tools = json.loads(result.stdout)
            return tools
    except Exception as e:
        print(f"[MCP Server] Tool generation failed: {e}", file=sys.stderr)

    # Minimal fallback
    return [
        {
            "name": "wiki_advisor",
            "description": "Show system status and recommended next actions.",
            "inputSchema": {"type": "object", "properties": {}},
            "_meta": {"cli_path": ["advisor"], "json_capable": True}
        },
        {
            "name": "wiki_stats",
            "description": "Generate wiki statistics.",
            "inputSchema": {"type": "object", "properties": {}},
            "_meta": {"cli_path": ["stats"], "json_capable": True}
        }
    ]


# ──────────────────────────────────────────────
# MCP Server Setup
# ──────────────────────────────────────────────

def create_server():
    """Create and configure the FastMCP server with all tools."""
    from mcp.server.fastmcp import FastMCP

    mcp = FastMCP(
        "Siebenwind Wiki",
        instructions=(
            "You are connected to the Siebenwind Wiki — a 20-year-old collaborative "
            "world-building project. Use the available tools to search lore, check "
            "system status, run audits, and communicate with other agents via the "
            "dispatch system. You ARE encouraged to use wiki_mail_quip for "
            "in-character commentary and interdepartmental humor."
        ),
    )

    # Load tool definitions from auto-extraction pipeline
    tool_defs = load_tool_definitions()
    oracle_available = probe_oracle()

    # Register each tool dynamically
    for tool_def in tool_defs:
        meta = tool_def.get("_meta", {})
        cli_path = meta.get("cli_path", [])
        json_capable = meta.get("json_capable", False)
        is_quip = meta.get("is_quip", False)

        # Skip search tool if Oracle is offline (register stub instead)
        if cli_path == ["search"] and not oracle_available:
            _register_search_unavailable(mcp)
            continue

        # Register the tool using a closure to capture the right values
        _register_tool(mcp, tool_def, cli_path, json_capable, is_quip)

    # Register wiki content as a resource
    @mcp.resource("wiki://status")
    def wiki_status() -> str:
        """Current wiki system status (advisor output)."""
        return run_cli_command(["advisor"], ["--json"], use_json=False)

    @mcp.resource("wiki://dispatch/open")
    def open_dispatches() -> str:
        """Currently open dispatch messages."""
        return run_cli_command(["mail", "inbox"], ["--status", "OPEN"])

    return mcp


def _register_tool(mcp, tool_def: dict, cli_path: list[str], json_capable: bool, is_quip: bool):
    """Register a single tool on the MCP server."""

    tool_name = tool_def["name"]
    description = tool_def["description"]
    schema = tool_def.get("inputSchema", {})
    meta = tool_def.get("_meta", {})
    properties = schema.get("properties", {})
    arguments = meta.get("arguments", [])
    compat_mode = meta.get("compat_mode")
    compat_arg = meta.get("compat_arg")
    compat_raw_arg = meta.get("compat_raw_arg")

    if is_quip:
        @mcp.tool(name=tool_name, description=description)
        def mail_quip(from_agent: str, body: str) -> str:
            """Post an in-character interagency quip."""
            if len(body) > 280:
                return "[ERROR] Quip exceeds 280 characters. Be more concise."
            return run_cli_command([
                "mail",
                "post",
            ], [
                "--from", from_agent,
                "--to", "ALL",
                "--subject", "[QUIP] Zur Kenntnis",
                "--body", body,
                "--priority", "LOW"
            ])
        return

    # Generic tool registration via dynamic function
    @mcp.tool(name=tool_name, description=description)
    def generic_tool(**kwargs) -> str:
        """Execute a CLI command with the given arguments."""
        if compat_mode == "mail_passthrough":
            raw = kwargs.get(compat_arg, "") if compat_arg else ""
            return run_cli_command(cli_path + shlex.split(raw), [], use_json=json_capable)

        if compat_mode == "subcommand_passthrough":
            subcommand = kwargs.get(compat_arg)
            raw_args = kwargs.get(compat_raw_arg, "") if compat_raw_arg else ""
            passthrough = [subcommand] if subcommand else []
            passthrough.extend(shlex.split(raw_args))
            return run_cli_command(cli_path + passthrough, [], use_json=json_capable)

        args = []
        for arg in arguments:
            key = arg["name"]
            value = kwargs.get(key)
            if value is None:
                continue
            if arg.get("kind") == "positional":
                args.append(str(value))
                continue
            flag = arg.get("flags", [f"--{key.replace('_', '-')}"])[0]
            if arg.get("type") == "boolean":
                if value:
                    args.append(flag)
                continue
            args.extend([flag, str(value)])

        return run_cli_command(cli_path, args, use_json=json_capable)


def _register_search_unavailable(mcp):
    """Register a stub search tool when Oracle is offline."""

    @mcp.tool(
        name="wiki_search",
        description=(
            "⚠️ Oracle (semantic search) is currently OFFLINE. "
            "The index may need rebuilding. Run wiki_index with rebuild=true first. "
            "As a fallback, this performs a basic text search via grep."
        )
    )
    def search_fallback(query: str) -> str:
        """Grep-based fallback search when Oracle is unavailable."""
        try:
            result = subprocess.run(
                ["grep", "-ril", "--include=*.md", query,
                 str(TECHNICAL_WIKI_ROOT)],
                capture_output=True, text=True, timeout=15
            )
            files = result.stdout.strip().split("\n")[:10]
            if files and files[0]:
                matches = "\n".join(f"  - {Path(f).relative_to(REPO_ROOT)}" for f in files)
                return f"[GREP FALLBACK] Found {len(files)} files matching '{query}':\n{matches}"
            return f"[GREP FALLBACK] No files found matching '{query}'."
        except Exception as e:
            return f"[ERROR] Fallback search failed: {e}"


# ──────────────────────────────────────────────
# Dual-Mode Startup
# ──────────────────────────────────────────────

def is_port_in_use(port: int) -> bool:
    """Check if a server is already running on the given port."""
    try:
        with socket.create_connection(("localhost", port), timeout=1):
            return True
    except (ConnectionRefusedError, OSError):
        return False


def main():
    parser = argparse.ArgumentParser(description="Siebenwind Wiki MCP Server")
    parser.add_argument(
        "--transport", choices=["stdio", "streamable-http"],
        default="stdio",
        help="Transport mode (default: stdio for direct agent connection)"
    )
    parser.add_argument(
        "--port", type=int, default=7777,
        help="Port for HTTP transport (default: 7777)"
    )
    args = parser.parse_args()

    if not _check_sdk():
        sys.exit(1)

    # Dual-mode: If HTTP and port already in use, warn
    if args.transport == "streamable-http" and is_port_in_use(args.port):
        print(
            f"[MCP Server] Port {args.port} already in use. "
            f"Another instance may be running. Connect to it instead.",
            file=sys.stderr
        )
        sys.exit(0)

    server = create_server()

    print(f"[MCP Server] Siebenwind Wiki — starting ({args.transport})", file=sys.stderr)
    print(f"[MCP Server] Repo: {REPO_ROOT}", file=sys.stderr)

    if args.transport == "streamable-http":
        print(f"[MCP Server] Listening on http://localhost:{args.port}/mcp", file=sys.stderr)
        server.run(transport="streamable-http", port=args.port)
    else:
        server.run(transport="stdio")


if __name__ == "__main__":
    main()
