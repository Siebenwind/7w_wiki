# Wissenswerk Agent Contract

> Platform-independent working rules for agents operating in a standalone Wissenswerk repository.

## Mission

Wissenswerk is a corpus-to-wiki knowledge compiler. Agents import prepared RagPrep artifacts, curate article plans, build Markdown wiki output, preserve provenance, run retrieval checks, and keep generated state auditable.

## Canonical Surfaces

- `./wissenswerk.py` is the canonical CLI.
- `wissenswerk.yaml` is the tenant configuration contract.
- `project_manifest.json` is the machine-readable product manifest.
- `DESIGN.md` is the UI and documentation design contract.
- JSON CLI output is the automation surface; prefer `--json` whenever available.
- IDE-specific adapters are generated convenience surfaces only. They must not contain semantics missing from these root contracts.

## Roles

Public role IDs are stable and English:

- `coordinator`: run planning, status, delegation, and human escalation.
- `curator`: corpus inventory, RagPrep import, article planning, and source mapping.
- `verifier`: citations, conflicts, link checks, provenance, and audit.
- `maintainer`: core code, providers, migrations, tests, and releases.

Localized role names are aliases only.

## Standard Flow

User-facing flow:

```text
init -> ingest -> curate -> wiki build -> search -> publish/bot
```

Maintainer flow:

```text
doctor -> plan -> apply -> audit -> report -> reset/rollback
```

## Rules

1. Treat sources, wiki, provenance, and retrieval indexes as factual authority. Agent memory and chat history are working context only.
2. Do not silently invent missing facts. Mark unresolved items clearly in generated reports or article drafts.
3. Auto-apply runs must write reports, provenance data, and rollback hints.
4. Reset and wipe operations are dry-run first. Destructive operations require explicit confirmation.
5. Keep public code, command IDs, role IDs, schema keys, and API names in English.
6. Keep tenant-specific terms in tenant configuration or tenant packs, not in generic core code.
7. Before UI, theme, or documentation-design changes, read `DESIGN.md` and run the design lint gate.

## Focused Verification

Run this gate for standalone Wissenswerk changes:

```bash
python3 -m py_compile wissenswerk.py
./wissenswerk.py doctor --json
./wissenswerk.py export plan --json
./wissenswerk.py test --json
git diff --check
```

Add package-level unit and integration tests as modules under `tests/`.
