---
layout: wiki_page
title: Wissenswerk CLI and Operations
category: Technical
---

# Wissenswerk CLI and Operations

`./wissenswerk.py` is the generic Wissenswerk CLI. Prefer `--json` for automation, tests, and agent work.

## User Commands

### Initialize

```bash
./wissenswerk.py init --json
```

Creates a starter `wissenswerk.yaml` when one does not exist. Use `--force` only when intentionally replacing the config.

### Ingest RagPrep Artifacts

```bash
./wissenswerk.py ingest --from-ragprep <dir> --apply --json
```

Imports `.json` and `.jsonl` RagPrep artifacts. Expected chunk fields:

- `document_id`
- `chunk_id`
- `text`
- `source_path`

Optional fields include `title`, `section`, `language`, `hash`, `entities`, and `summary`.

### Curate

```bash
./wissenswerk.py curate --json
```

Reads the latest import state and produces article candidates, source paths, chunk counts, sections, summary coverage, duplicate chunk conflicts, and next recommended commands.

### Build Wiki

```bash
./wissenswerk.py wiki build --apply --json
```

Builds generated wiki artifacts and writes a report. The current implementation is a bootstrap slice with minimal generated articles from imported chunks.

### Search

```bash
./wissenswerk.py search "question" --source raw --json
./wissenswerk.py search "question" --source wiki --json
./wissenswerk.py search "question" --source all --json
```

Current retrieval is lexical bootstrap over configured roots. The target implementation is pgvector-backed search with optional answer synthesis.

## Maintainer Commands

```bash
./wissenswerk.py doctor --json
./wissenswerk.py providers check --json
./wissenswerk.py design lint --json
./wissenswerk.py task digest --json
./wissenswerk.py run status --json
./wissenswerk.py reset index --dry-run --json
./wissenswerk.py wipe tenant --dry-run --json
```

Reset and wipe commands are dry-run-first. `wipe all` requires the explicit confirm token `WIPE-WISSENSWERK` when applied.

## Signals & Tasks

Signals are coordination events. Tasks are tracked work items. They are local runtime state, not committed project knowledge.

```bash
./wissenswerk.py task raise --type anomaly --severity medium --summary "Chunk metadata looks wrong" --json
./wissenswerk.py task list --status submitted --json
./wissenswerk.py task show TASK-2026-0001 --json
./wissenswerk.py task claim TASK-2026-0001 --agent verifier --json
./wissenswerk.py task resolve TASK-2026-0001 --summary "Verified against source" --json
./wissenswerk.py task reject TASK-2026-0001 --reason "Duplicate of later task" --json
./wissenswerk.py task digest --since 24h --json
```

Supported task types are `anomaly`, `blocker`, `handoff`, `approval`, `audit_finding`, and `run_event`. Supported statuses are `submitted`, `working`, `input-required`, `auth-required`, `completed`, `failed`, `canceled`, and `rejected`.

## Export Commands

```bash
./wissenswerk.py export plan --strict --json
./wissenswerk.py export materialize --target /tmp/wissenswerk-public --json
./wissenswerk.py export materialize --target /tmp/wissenswerk-public --apply --json
./wissenswerk.py export verify --target /tmp/wissenswerk-public --json
```

`export plan` validates `wissenswerk_export_manifest.json`.

`export materialize` copies the public export tree into a target directory. It is a dry-run unless `--apply` is present.

`export verify` runs the public gates inside an already materialized target directory. Use it before creating or pushing a standalone repository.

## Test

```bash
./wissenswerk.py test --json
```

Runs the standalone stdlib unit-test suite under `tests/`.

## Verification

Recommended local checks:

```bash
python3 -m py_compile wissenswerk.py
./wissenswerk.py doctor --json
./wissenswerk.py export plan --strict --json
./wissenswerk.py test --json
git diff --check
```
