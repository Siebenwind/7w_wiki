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
./wissenswerk.py reset index --dry-run --json
./wissenswerk.py wipe tenant --dry-run --json
```

Reset and wipe commands are dry-run-first. `wipe all` requires the explicit confirm token `WIPE-WISSENSWERK` when applied.

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
