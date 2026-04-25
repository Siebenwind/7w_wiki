# Wissenswerk

Wissenswerk is a platform-independent knowledge compiler. It imports prepared document corpora, builds an auditable Markdown wiki, preserves provenance and reports, and exposes the same knowledge through search, bot adapters, and future API surfaces.

The project is designed for agents and humans working together through open repository contracts instead of IDE-specific assumptions.

## Quick Start

```bash
./wissenswerk.py init --json
./wissenswerk.py ingest --from-ragprep tests/fixtures/ragprep --apply --json
./wissenswerk.py curate --json
./wissenswerk.py wiki build --apply --json
./wissenswerk.py search "example question" --source all --json
./wissenswerk.py task digest --json
```

## Core Principles

- **Markdown-first:** generated knowledge remains inspectable and portable.
- **RagPrep boundary:** parsing, cleanup, and pre-chunking happen before Wissenswerk.
- **Provenance first:** auto-apply runs produce reports, auditable state, and rollback hints.
- **Provider-neutral:** chat, summary, embeddings, and rerank use OpenAI-compatible endpoints.
- **pgvector default:** PostgreSQL + pgvector is the default retrieval target.
- **Signals, not chat:** agents use local Tasks for anomalies, blockers, handoffs, approvals, audit findings, and run events.
- **Agent-readable contracts:** `AGENTS.md`, `DESIGN.md`, `wissenswerk.yaml`, `project_manifest.json`, JSON CLI output, and future MCP/tool manifests are canonical.

## Roles

Public role IDs are English and stable:

- `coordinator`: run planning, reports, delegation, human escalation.
- `curator`: corpus inventory, RagPrep import, article planning, source mapping.
- `verifier`: citations, conflicts, link checks, provenance and audit.
- `maintainer`: core code, providers, migrations, tests, releases.

Localized display names belong in tenant configuration.

## Signals & Tasks

Wissenswerk uses a local coordination layer instead of a committed message board:

```bash
./wissenswerk.py task raise --type anomaly --severity medium --summary "Unexpected source shape" --json
./wissenswerk.py task list --status submitted --json
./wissenswerk.py task claim TASK-2026-0001 --agent verifier --json
./wissenswerk.py task resolve TASK-2026-0001 --summary "Checked and documented" --json
./wissenswerk.py run status --json
```

Task state lives under `.wissenswerk/tasks/` and is ignored by git. It coordinates work; it is never factual authority.

## Verification

```bash
python3 -m py_compile wissenswerk.py
./wissenswerk.py doctor --json
./wissenswerk.py export plan --strict --json
./wissenswerk.py test --json
git diff --check
```

To create and verify a candidate public repository tree:

```bash
./wissenswerk.py export materialize --target /tmp/wissenswerk-public --apply --json
./wissenswerk.py export verify --target /tmp/wissenswerk-public --json
```

## GitHub Readiness

The repository includes:

- `README.md`, `LICENSE`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, and `SUPPORT.md`
- issue templates, pull request template, CODEOWNERS, and Python CI under `.github/`
- `.gitignore` coverage for secrets, runtime state, local databases, and generated reports
- `AGENTS.md` and `DESIGN.md` as agent-readable root contracts
- `pyproject.toml` for package metadata and the `wissenswerk` console script

## Documentation

- Agent contract: [AGENTS.md](AGENTS.md)
- Design contract: [DESIGN.md](DESIGN.md)
- CLI and operations: [docs/Wissenswerk/cli.md](docs/Wissenswerk/cli.md)
- Architecture: [docs/Wissenswerk/architecture.md](docs/Wissenswerk/architecture.md)
- Retrieval and memory: [docs/Wissenswerk/retrieval.md](docs/Wissenswerk/retrieval.md)
- Publication readiness: [docs/Wissenswerk/publication-readiness.md](docs/Wissenswerk/publication-readiness.md)

## License

Wissenswerk is licensed under the [MIT License](LICENSE).
