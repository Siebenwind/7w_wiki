---
name: Workflow Forum Search
description: Codex bridge for forum-based source discovery and ingestion lead generation.
---

# Workflow Bridge: /forum_search

> **Wrapper for**: `.agent/workflows/forum_search.md`
> **Marker**: Generated workflow bridge. Do not edit manually.

This is a generated Codex-facing workflow bridge. Runtime execution must stay on `./7w_wiki.py`.

## Primary Runtime Command
`./7w_wiki.py scout --forum bekanntmachungen --pages 3`

## Supported Board Scopes
- `bekanntmachungen`
- `news`

## Comparison Target
- `Quellen/Forum/...`

## Follow-up Commands
- `./7w_wiki.py scout --forum news --pages 3`
- `./7w_wiki.py mail post --from Scout --to Ingestor --subject "<source lead>" --body "<summary>"`

## Usage Rule
Read `.agent/workflows/forum_search.md` for the authoritative process. Do not guess workflow semantics from this bridge file alone.
