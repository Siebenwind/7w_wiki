# Skill: The Oracle (Semantic Search)
> **Wrapper for**: `.agent/skills/oracle/SKILL.md`

This skill provides semantic search capabilities over the entire Siebenwind Wiki and its source materials.

## Usage
Run the following command to search:
```bash
./7w_wiki.py search "<Your Query>" --source all
```

## Capabilities
- **RAG (Retrieval Augmented Generation)**: Finds relevant lore using vector embeddings.
- **Source Selection**: Use `--source wiki` (default) or `--source quellen` (raw materials).

For full documentation, see: `.agent/skills/oracle/SKILL.md`
