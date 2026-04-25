---
layout: wiki_page
title: Wissenswerk
category: Technical
---

# Wissenswerk

Wissenswerk turns prepared document corpora into an auditable Markdown wiki with provenance, reports, retrieval, and bot/API surfaces.

## Five-Minute Flow

```bash
./wissenswerk.py init --json
./wissenswerk.py ingest --from-ragprep tests/fixtures/ragprep --apply --json
./wissenswerk.py curate --json
./wissenswerk.py wiki build --apply --json
./wissenswerk.py search "example question" --source all --json
```

## Maintainer Flow

```bash
./wissenswerk.py doctor --json
./wissenswerk.py providers check --json
./wissenswerk.py design lint --json
./wissenswerk.py reset index --dry-run --json
./wissenswerk.py wipe tenant --dry-run --json
```

## Core Contracts

- `AGENTS.md`: platform-independent agent instructions.
- `DESIGN.md`: design tokens and rationale for UI/documentation work.
- `wissenswerk.yaml`: tenant, provider, path, workflow, memory, and reset configuration.
- `project_manifest.json`: machine-readable product manifest.
- `wissenswerk_export_manifest.json`: repository export and publication contract.

## Roles

Public role IDs are English:

- `coordinator`: run planning, reporting, delegation, human escalation.
- `curator`: corpus inventory, RagPrep import, article planning, source mapping.
- `verifier`: citations, conflicts, link checks, provenance, audit.
- `maintainer`: core code, providers, migrations, tests, releases.

Tenant-specific display names can be localized.

## More

- [Architecture](architecture.md)
- [CLI and Operations](cli.md)
- [Retrieval and Memory](retrieval.md)
- [Signals and Tasks](signals-tasks.md)
- [Publication Readiness](publication-readiness.md)
- [Discord Bot](discord-bot.md)
- [Agent System Integration](agent-system-hermes.md)
- [Positioning](positioning.md)
