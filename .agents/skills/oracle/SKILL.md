---
name: Das Orakel (Semantische Suche)
description: Lokale Vektorsuche (RAG) über das gesamte Siebenwind-Wissen. Nutzt jina-embeddings-v3 für Embedding und bge-reranker-v2-m3 für Re-Ranking.
---

# Codex Skill: Das Orakel (Semantische Suche)

> **Canonical skill**: `.agent/skills/oracle/SKILL.md`
> **Marker**: Generated Codex adapter skill. Do not edit manually.

This adapter is generated from the canonical catalog. Runtime execution stays on `./7w_wiki.py`; `.agent/` remains the source of truth.

## Primary Runtime Command
`./7w_wiki.py search <query> [remaining...]`

## Follow-up Commands
- `./7w_wiki.py search <query> --source all`
- `./7w_wiki.py index --status`

## Instructions
- Use this adapter for semantic search across wiki pages and source material.
- Set --source deliberately so the result set matches the epistemic layer you are checking.
- Check index status before assuming search quality problems are content problems.

## References
- `.agent/skills/oracle/SKILL.md`
- `.agent/skills/oracle/search.py`
- `.agent/skills/oracle/build_index.py`
