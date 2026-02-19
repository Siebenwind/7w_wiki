#!/usr/bin/env python3
import sys
import os
import json
import subprocess
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parents[2]
CLI_PATH = REPO_ROOT / "7w_wiki.py"
TOOLS_JSON_PATH = REPO_ROOT / ".agent" / "config" / "tools.json"

def get_cli_schema() -> dict:
    try:
        result = subprocess.run(
            [sys.executable, str(CLI_PATH), "--help-json"],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error acquiring CLI schema: {e.stderr}", file=sys.stderr)
        sys.exit(1)

def convert_to_openai_tools(schema: dict) -> list:
    tools = []
    
    for cmd in schema.get("commands", []):
        cmd_name = cmd["name"]
        
        # We model the CLI tool as a function.
        # e.g. "run_7w_wiki_start"
        function_name = f"cli_{cmd_name}"
        function_desc = cmd.get("description", "").strip() or f"Execute the {cmd_name} command in 7w_wiki."
        
        properties = {}
        required = []
        
        for arg in cmd.get("arguments", []):
            arg_name = arg["name"]
            
            # Map choice lists if available
            prop_def = {
                "type": "string",
                "description": arg.get("help", "")
            }
            if "choices" in arg:
                prop_def["enum"] = arg["choices"]
                
            properties[arg_name] = prop_def
            if arg.get("required", False):
                required.append(arg_name)

        tool_def = {
            "type": "function",
            "function": {
                "name": function_name,
                "description": function_desc,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }
        tools.append(tool_def)
        
    return tools

def main():
    print("Fetching CLI Schema via --help-json...")
    cli_schema = get_cli_schema()
    
    print("Converting schema to OpenAI Tool definitions...")
    openai_tools = list(convert_to_openai_tools(cli_schema))
    
    TOOLS_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with TOOLS_JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(openai_tools, f, indent=2)
        
    print(f"Successfully wrote {len(openai_tools)} tools to {TOOLS_JSON_PATH.relative_to(REPO_ROOT)}")

if __name__ == "__main__":
    main()
