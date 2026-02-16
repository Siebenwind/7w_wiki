---
name: Oracle Search Bridge
description: Thin wrapper for semantic lookup via ./7w_wiki.py search across wiki and source layers.
---

# Skill: The Oracle (Semantic Search)
> **Wrapper for**: `.agent/skills/oracle/SKILL.md`

This skill provides semantic search capabilities over the entire Siebenwind Wiki and its source materials.

## Usage
Run searches with explicit source scope:
```bash
./7w_wiki.py search "<Your Query>" --source wiki
./7w_wiki.py search "<Your Query>" --source quellen
./7w_wiki.py search "<Your Query>" --source all
```

## Capabilities
- **RAG (Retrieval Augmented Generation)**: Finds relevant lore using vector embeddings.
- **Source Selection**:
  - `--source wiki`: Curated wiki knowledge.
  - `--source quellen`: Raw source corpus.
  - `--source all`: Combined cross-layer search.

For full documentation, see: `.agent/skills/oracle/SKILL.md`
