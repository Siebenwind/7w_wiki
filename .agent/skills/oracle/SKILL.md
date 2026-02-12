---
name: Das Orakel (Semantische Suche)
description: Lokale Vektorsuche (RAG) über das gesamte Siebenwind-Wissen. Nutzt jina-embeddings-v3 für Embedding und bge-reranker-v2-m3 für Re-Ranking.
---

# Das Orakel – Semantische Wissenssuche

**Epistemischer Status:** #perspektive

Das Orakel ermöglicht semantische, nicht-lineare Suche über das gesamte Siebenwind-Archiv. Es denkt assoziativ: Wenn ein Text „Der dunkle König" erwähnt, findet das Orakel auch Einträge zu „Schattenherrscher", ohne dass das Keyword identisch sein muss.

## Architektur

- **Embedding:** `jinaai/jina-embeddings-v3` (570M Params, 8192 Token Kontext, LoRA-Adapter für Retrieval)
- **Re-Ranker:** `BAAI/bge-reranker-v2-m3` (568M Params, Cross-Encoder für präzises Re-Ranking)
- **Vektor-DB:** ChromaDB (persistent, lokal unter `.agent/data/chroma_db/`)
- **GPU:** Apple MPS (Metal Performance Shaders) für ~4-5× Beschleunigung
- **Modell-Cache:** `.agent/data/models/` (persistent über Sandbox-Neustarts)

## Zwei getrennte Datenbanken

| Collection | Inhalt | Level |
|------------|--------|-------|
| `siebenwind_quellen` | `/Quellen/` — Rohmaterial | canon, chronicle, lore, legend |
| `siebenwind_wiki` | `/Siebenwind_Wiki/` — Abgeleitetes Wissen | wiki |

## Voraussetzungen

```bash
# Einmalige Installation
bash .agent/skills/oracle/setup.sh
```

### 2. Nutzung (CLI)
Der Skill wird über das Terminal aufgerufen.

**Basis-Suche (Standard: Nur Wiki):**
```bash
.agent/skills/oracle/venv/bin/python3 .agent/skills/oracle/search.py "Wer ist der Gott des Feuers?"
```

**Erweiterte Suche (Quellen / Alles):**
```bash
# Nur in Rohdaten suchen
.agent/skills/oracle/venv/bin/python3 .agent/skills/oracle/search.py "Tiamat" --source quellen

# Alles durchsuchen (Wiki + Quellen)
.agent/skills/oracle/venv/bin/python3 .agent/skills/oracle/search.py "Tiamat" --source all

# Ohne Re-Ranking (schneller)
.agent/skills/oracle/venv/bin/python3 .agent/skills/oracle/search.py "Tiamat" --no-rerank

# Mehr Ergebnisse
.agent/skills/oracle/venv/bin/python3 .agent/skills/oracle/search.py "Tiamat" --top 10
```

## Index neu aufbauen

```bash
# Nach neuen Quellen oder Wiki-Änderungen
.agent/skills/oracle/venv/bin/python3 .agent/skills/oracle/build_index.py
```

## Agent-Integration (Historiker-Workflow)

1. **Artikel-Review:** „Gibt es in den Quellen Infos zu X, die im Artikel fehlen?"
2. **Konsistenzprüfung:** „Was sagen verschiedene Quellen über Ereignis Y?"
3. **Deep Lore:** „Welche Spielergeschichten erwähnen Ort Z?"
