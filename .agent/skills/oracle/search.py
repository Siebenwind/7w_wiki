#!/usr/bin/env python3
# =============================================================================
# Das Orakel – Semantische Suche
# Durchsucht die ChromaDB-Collections mit jina-embeddings-v3 und
# optionalem Re-Ranking via bge-reranker-v2-m3.
# =============================================================================
"""
Usage:
    python3 search.py "Wer ist Tiamat?"                     # Beide DBs
    python3 search.py "Tiamat" --source quellen              # Nur Quellen
    python3 search.py "Tiamat" --source wiki                 # Nur Wiki
    python3 search.py "Tiamat" --no-rerank                   # Ohne Re-Ranking
    python3 search.py "Tiamat" --top 10                      # Mehr Ergebnisse
    python3 search.py "Tiamat" --top 10 --raw                # Nur Text (für Pipes)
"""

import os
import sys
import argparse
import time
from pathlib import Path

# --- Dependency-Check ---
try:
    import chromadb
    from sentence_transformers import SentenceTransformer
except ImportError:
    print("❌ Dependencies nicht gefunden!")
    print("   Bitte zuerst setup.sh in einem normalen Terminal ausführen:")
    print("   bash .agent/skills/oracle/setup.sh")
    print("")
    print("   Danach mit dem venv-Python starten:")
    print("   .agent/skills/oracle/venv/bin/python3 .agent/skills/oracle/search.py \"Suchbegriff\"")
    sys.exit(1)

# --- Pfade auflösen ---
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent
MODEL_CACHE = REPO_ROOT / ".agent" / "data" / "models"
CHROMA_DIR = REPO_ROOT / ".agent" / "data" / "chroma_db"

os.environ["SENTENCE_TRANSFORMERS_HOME"] = str(MODEL_CACHE)
os.environ["HF_HOME"] = str(MODEL_CACHE / "huggingface")

# --- Konfiguration ---
EMBEDDING_MODEL = "jinaai/jina-embeddings-v3"
RERANKER_MODEL = "BAAI/bge-reranker-v2-m3"

COLLECTION_MAP = {
    "quellen": "siebenwind_quellen",
    "wiki": "siebenwind_wiki",
}

LEVEL_ICONS = {
    "canon": "🛡️ [KANON]",
    "chronicle": "📜 [CHRONIK]",
    "lore": "📚 [GELEHRSAMKEIT]",
    "legend": "🗣️ [LEGENDE]",
    "wiki": "📖 [WIKI]",
}

# Wie viele Ergebnisse pro Collection VOR dem Re-Ranking geholt werden
PRE_RERANK_RESULTS = 20


def load_embedding_model():
    """Lädt das Embedding-Modell mit MPS-Beschleunigung."""
    from sentence_transformers import SentenceTransformer
    device = "mps" if sys.platform == "darwin" else "cpu"
    model = SentenceTransformer(
        EMBEDDING_MODEL,
        trust_remote_code=True,
        device=device,
    )
    return model


def load_reranker():
    """Lädt den Cross-Encoder Re-Ranker."""
    from FlagEmbedding import FlagReranker
    device = "mps" if sys.platform == "darwin" else "cpu"
    reranker = FlagReranker(
        RERANKER_MODEL,
        use_fp16=True,
        device=device,
    )
    return reranker


def search_collection(client, collection_name: str, query_embedding: list,
                      n_results: int) -> list[dict]:
    """Durchsucht eine einzelne ChromaDB-Collection."""
    try:
        collection = client.get_collection(name=collection_name)
    except Exception:
        return []
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"],
    )
    
    hits = []
    if results["documents"] and results["documents"][0]:
        for i, doc in enumerate(results["documents"][0]):
            meta = results["metadatas"][0][i]
            distance = results["distances"][0][i]
            # ChromaDB gibt cosine distance zurück → Similarity = 1 - distance
            similarity = 1.0 - distance
            
            hits.append({
                "text": doc,
                "metadata": meta,
                "similarity": similarity,
                "collection": collection_name,
            })
    
    return hits


def rerank_results(reranker, query: str, hits: list[dict],
                   top_k: int) -> list[dict]:
    """Re-Rankt die Ergebnisse mit dem Cross-Encoder."""
    if not hits:
        return []
    
    # Paare bilden: (Query, Dokument-Text)
    pairs = [[query, hit["text"]] for hit in hits]
    
    # Scores berechnen
    scores = reranker.compute_score(pairs, normalize=True)
    
    # Scores können als einzelner Float oder Liste zurückkommen
    if isinstance(scores, (int, float)):
        scores = [scores]
    
    # Scores zuweisen
    for hit, score in zip(hits, scores):
        hit["rerank_score"] = float(score)
    
    # Nach Re-Rank-Score sortieren und Top-K zurückgeben
    hits.sort(key=lambda x: x["rerank_score"], reverse=True)
    return hits[:top_k]


def format_result(hit: dict, index: int, raw: bool = False) -> str:
    """Formatiert ein einzelnes Suchergebnis für die Ausgabe."""
    meta = hit["metadata"]
    level = meta.get("level", "unknown")
    icon = LEVEL_ICONS.get(level, f"❓ [{level.upper()}]")
    source = meta.get("source", "unbekannt")
    category = meta.get("category", "")
    entities = meta.get("entities", "")
    
    # Score: Re-Rank wenn vorhanden, sonst Similarity
    if "rerank_score" in hit:
        score_str = f"Score: {hit['rerank_score']:.3f} (re-ranked)"
    else:
        score_str = f"Similarity: {hit['similarity']:.3f}"
    
    # Rohtext ohne Formatierung (für Pipes)
    if raw:
        text_preview = hit["text"][:1200]
        return f"--- [{level.upper()}] {source} ({score_str}) ---\n{text_preview}\n"
    
    # Formatierten Text – Header entfernen für bessere Lesbarkeit
    text = hit["text"]
    # Kontextuellen Header überspringen (erste Zeile bis \n\n)
    if "\n\n" in text:
        text = text.split("\n\n", 1)[1]
    text_preview = text[:600].strip()
    if len(text) > 600:
        text_preview += "..."
    
    lines = [f"\n{icon} {score_str}"]
    lines.append(f"   Quelle: {source}")
    
    # Metadaten-Zeile
    meta_parts = []
    if category:
        meta_parts.append(f"Kategorie: {category}")
    if entities:
        # Entitäten als [[Links]] formatieren
        entity_list = [f"[[{e.strip()}]]" for e in entities.split(",")[:5]]
        meta_parts.append(f"Entitäten: {', '.join(entity_list)}")
    if meta_parts:
        lines.append(f"   {' | '.join(meta_parts)}")
    
    # Chunk-Info
    chunk_idx = meta.get("chunk_index", "?")
    total = meta.get("total_chunks", "?")
    lines.append(f"   Chunk: {chunk_idx}/{total} ({meta.get('char_count', '?')} Zeichen)")
    
    lines.append(f'   "{text_preview}"')
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Das Orakel – Semantische Suche im Siebenwind-Archiv"
    )
    parser.add_argument("query", nargs="?", help="Suchanfrage")
    parser.add_argument("--source", choices=["quellen", "wiki", "all"],
                        default="all", help="Welche Datenbank durchsucht wird")
    parser.add_argument("--top", type=int, default=5,
                        help="Anzahl der Ergebnisse (default: 5)")
    parser.add_argument("--no-rerank", action="store_true",
                        help="Ohne Re-Ranking (schneller)")
    parser.add_argument("--raw", action="store_true",
                        help="Rohtext-Ausgabe (für Pipes)")
    args = parser.parse_args()
    
    if not args.query:
        parser.print_help()
        sys.exit(1)
    
    query = args.query
    start_time = time.time()
    
    if not args.raw:
        print("╔═══════════════════════════════════════════════════╗")
        print("║   Das Orakel – Semantische Suche                 ║")
        print("╚═══════════════════════════════════════════════════╝")
        print(f"  Query: \"{query}\"")
        print(f"  Quelle: {args.source} | Top: {args.top} | "
              f"Re-Rank: {'Nein' if args.no_rerank else 'Ja'}")
    
    # ChromaDB Client
    import chromadb
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    
    # Embedding-Modell laden
    if not args.raw:
        print("\n  🧠 Lade Modell...", end="", flush=True)
    model = load_embedding_model()
    if not args.raw:
        print(" ✅")
    
    # Query einbetten (task='retrieval.query' nutzt den Query-LoRA-Adapter)
    query_vec = model.encode(
        [query],
        task="retrieval.query",
    ).tolist()[0]
    
    # Collections durchsuchen
    collections_to_search = (
        ["quellen", "wiki"] if args.source == "all"
        else [args.source]
    )
    
    # Pre-Rerank: Mehr Ergebnisse holen, dann filtern
    pre_rerank_n = PRE_RERANK_RESULTS if not args.no_rerank else args.top
    
    all_hits = []
    for source_key in collections_to_search:
        coll_name = COLLECTION_MAP[source_key]
        hits = search_collection(client, coll_name, query_vec, pre_rerank_n)
        all_hits.extend(hits)
        if not args.raw:
            print(f"  📊 {coll_name}: {len(hits)} Treffer")
    
    if not all_hits:
        print("\n  ❌ Keine Ergebnisse gefunden.")
        print("     Tipp: Führe zuerst 'build_index.py' aus, um den Index aufzubauen.")
        sys.exit(0)
    
    # Re-Ranking
    if not args.no_rerank and len(all_hits) > 1:
        if not args.raw:
            print("  🔍 Re-Ranking...", end="", flush=True)
        reranker = load_reranker()
        all_hits = rerank_results(reranker, query, all_hits, args.top)
        if not args.raw:
            print(" ✅")
    else:
        # Nur nach Similarity sortieren und beschneiden
        all_hits.sort(key=lambda x: x["similarity"], reverse=True)
        all_hits = all_hits[:args.top]
    
    # Ergebnisse ausgeben
    search_time = time.time() - start_time
    
    if not args.raw:
        print(f"\n  ⏱️  Suchzeit: {search_time:.1f}s")
        print(f"  📋 Top-{len(all_hits)} Ergebnisse:")
    
    for i, hit in enumerate(all_hits, 1):
        print(format_result(hit, i, raw=args.raw))
    
    if not args.raw:
        print()


if __name__ == "__main__":
    main()
