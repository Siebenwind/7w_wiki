# Workflow and Skill Surfaces

This page explains how the generic Wissenswerk process relates to legacy Siebenwind workflows and generated agent adapters.

## Generic Wissenswerk Workflow

User flow:

```text
init -> ingest -> curate -> wiki build -> search -> publish/bot
```

Maintainer flow:

```text
doctor -> plan -> apply -> audit -> report -> reset/rollback
```

CLI surface:

```bash
./wissenswerk.py init --json
./wissenswerk.py ingest --from-ragprep <dir> --apply --json
./wissenswerk.py curate --json
./wissenswerk.py wiki build --apply --json
./wissenswerk.py search "question" --source all --json
./wissenswerk.py doctor --json
./wissenswerk.py hygiene reports --json
./wissenswerk.py export plan --json
./wissenswerk.py reset index --dry-run --json
```

## Core Roles

- `coordinator`: planning, reports, delegation, human escalation.
- `curator`: corpus inventory, RagPrep import, article planning.
- `verifier`: citations, conflicts, links, provenance, audit.
- `maintainer`: core code, providers, migrations, tests, releases.

## Legacy Siebenwind Workflows

The following remain useful, but belong to legacy or tenant-specific surfaces:

- `/start`
- `/takeover`
- `/handover`
- `/forum_search`
- `/lore_master`
- `/historian`
- `/tech_master`
- `/test_run`

Siebenwind-flavored skills such as Wiki-Schmied, Kanon-Waechter, Lektor, Linguist, Time Keeper, Forum Scout, and Lore-Gelehrter should be moved toward tenant packs over time.

## Adapter Policy

Generated host adapters may improve discoverability, but they must not define unique behavior. They should point back to:

- `AGENTS.md`
- `DESIGN.md`
- `./wissenswerk.py ... --json`
- `./7w_wiki.py --help-json`
- `.agent/config/tools.json`
- MCP

## Regeneration

Legacy surfaces are regenerated through:

```bash
./7w_wiki.py tech --sync-interop
```

Generic Wissenswerk surfaces should be tested through:

```bash
python3 -m py_compile wissenswerk.py
./wissenswerk.py doctor --json
./wissenswerk.py export plan --json
./7w_wiki.py test --suite wissenswerk-contract --timeout 60
git diff --check
```
