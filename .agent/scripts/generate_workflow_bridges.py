#!/usr/bin/env python3
"""
Deprecated compatibility shim for the old workflow bridge generator.
Use generate_codex_skills.py instead.
"""
from generate_codex_skills import main


if __name__ == "__main__":
    print("[deprecated] generate_workflow_bridges.py now delegates to generate_codex_skills.py")
    raise SystemExit(main())
