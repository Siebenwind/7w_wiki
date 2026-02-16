---
name: Interop Audit Bridge
description: Thin wrapper for interoperability checks using canonical CLI commands and SY_INTEROP governance.
---

# Skill: Interop Audit
> **Wrapper for**: `System/Synapse_Board/SY_INTEROP.md`

Use this skill to validate runtime/documentation consistency.

## Usage
Run the core checks:

```bash
./7w_wiki.py audit
./7w_wiki.py start
./7w_wiki.py advisor
./7w_wiki.py search "<query>" --source wiki
./7w_wiki.py search "<query>" --source quellen
./7w_wiki.py search "<query>" --source all
```

## Validation Focus
- `runtime_commands` and `method_only` blocks in workflows.
- Runtime command references stay on `./7w_wiki.py`.
- Dispatch lifecycle remains aligned with `SY_DISPATCH`.
