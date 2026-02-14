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

# --- Pfade auflösen ---
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent
MODEL_CACHE = REPO_ROOT / ".agent" / "data" / "models"

# --- Umgebungsvariablen (MÜSSEN vor den Modell-Imports gesetzt werden) ---
os.environ["SENTENCE_TRANSFORMERS_HOME"] = str(MODEL_CACHE)
os.environ["HF_HOME"] = str(MODEL_CACHE / "huggingface")
os.environ["HF_HUB_CACHE"] = str(MODEL_CACHE / "huggingface" / "hub")
os.environ["XDG_CACHE_HOME"] = str(MODEL_CACHE / "xdg_cache")
os.environ["TOKENIZERS_PARALLELISM"] = "false" # Warnung unterdrücken

# --- Pfade für Imports ---
# (Path-Setup für relative Imports falls nötig)
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

# --- Pfade ---
CHROMA_DIR = REPO_ROOT / ".agent" / "data" / "chroma_db"

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


def load_embedding_model(device: str = None):
    """Lädt das Embedding-Modell."""
    if device is None:
        device = "mps" if sys.platform == "darwin" else "cpu"
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer(
        EMBEDDING_MODEL,
        trust_remote_code=True,
        device=device,
    )
    return model


def load_reranker(device: str = None):
    """Lädt den Cross-Encoder Re-Ranker."""
    if device is None:
        device = "mps" if sys.platform == "darwin" else "cpu"
    from FlagEmbedding import FlagReranker
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


def search(query: str, top_k: int = 5, source: str = "all", use_reranker: bool = True, device: str = None):
    """Führt die Suche aus."""
    if device is None:
        device = "mps" if sys.platform == "darwin" else "cpu"

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    
    # Embedding generieren
    # Wir laden das Modell kurzfristig (oder cachen es, wenn wir als Service laufen würden)
    # Für CLI ist Laden pro Call okay (Jina v3 lädt schnell genug, ~2s)
    model = load_embedding_model(device)
    query_embedding = model.encode(
        [query],
        task="retrieval.query",
        prompt_name="retrieval.query",
    ).tolist()[0]
    
    # Collections durchsuchen
    collections_to_search = (
        ["quellen", "wiki"] if source == "all"
        else [source]
    )
    
    # Pre-Rerank: Mehr Ergebnisse holen, dann filtern
    pre_rerank_n = PRE_RERANK_RESULTS if use_reranker else top_k
    
    all_hits = []
    for source_key in collections_to_search:
        coll_name = COLLECTION_MAP[source_key]
        hits = search_collection(client, coll_name, query_embedding, pre_rerank_n)
        all_hits.extend(hits)
    
    if not all_hits:
        return []
    
    # Re-Ranking
    if use_reranker and len(all_hits) > 1:
        reranker = load_reranker(device)
        all_hits = rerank_results(reranker, query, all_hits, top_k)
    else:
        # Nur nach Similarity sortieren und beschneiden
        all_hits.sort(key=lambda x: x["similarity"], reverse=True)
        all_hits = all_hits[:top_k]
    
    return all_hits


def main():
    # Config laden falls vorhanden
    config_path = SCRIPT_DIR / "config.json"
    default_device = "mps" if sys.platform == "darwin" else "cpu"
    
    try:
        if config_path.exists():
            import json
            with open(config_path) as f:
                cfg = json.load(f)
                if "device" in cfg: default_device = cfg["device"]
    except Exception as e:
        # Fallback to default device if permission or other errors occur
        pass

    parser = argparse.ArgumentParser(
        description="Das Orakel – Semantische Suche im Siebenwind-Archiv"
    )
    parser.add_argument("query", help="Suchanfrage")
    parser.add_argument("--top", type=int, default=20,
                        help="Anzahl Ergebnisse")
    parser.add_argument("--source", choices=["wiki", "quellen", "all"],
                        default="wiki", help="Welche Datenbank durchsucht wird (Default: wiki)")
    parser.add_argument("--re-rank", action=argparse.BooleanOptionalAction, default=True,
                        help="Re-Ranking aktivieren/deaktivieren")
    parser.add_argument("--raw", action="store_true",
                        help="Gibt nur Raw-Text zurück")
    parser.add_argument("--cpu", action="store_true", help="Erzwingt CPU")
    args = parser.parse_args()
    
    if args.cpu:
        default_device = "cpu"
        
    query = args.query
    start_time = time.time()
    
    if not args.raw:
        print("╔═══════════════════════════════════════════════════╗")
        print("║   Das Orakel – Semantische Suche                 ║")
        print("╚═══════════════════════════════════════════════════╝")
        print(f"  Query: \"{query}\"")
        print(f"  Quelle: {args.source} | Top: {args.top} | "
              f"Re-Rank: {'Nein' if not args.re_rank else 'Ja'}")
    
    if not args.raw:
        print("\n  🧠 Lade Modell...", end="", flush=True)
        
    start_time = time.time()
    
    # Suche ausführen
    results = search(args.query, top_k=args.top, source=args.source, 
                     use_reranker=args.re_rank, device=default_device)
                     
    if not args.raw:
        print(" ✅")
        
    if not results:
        if not args.raw:
            print("\n  ❌ Keine Ergebnisse gefunden.")
            print("     Tipp: Führe zuerst 'build_index.py' aus, um den Index aufzubauen.")
        sys.exit(0)
    
    # Ergebnisse ausgeben
    search_time = time.time() - start_time
    
    if not args.raw:
        print(f"\n  ⏱️  Suchzeit: {search_time:.1f}s")
        print(f"  📋 Top-{len(results)} Ergebnisse:")
    
    for i, hit in enumerate(results, 1):
        # Raw-Flag an formatter durchreichen
        print(format_result(hit, i, raw=args.raw))
    
    if not args.raw:
        print()


if __name__ == "__main__":
    main()
