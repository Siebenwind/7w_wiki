#!/usr/bin/env python3
# =============================================================================
# Das Orakel – Index Builder
# Baut zwei separate ChromaDB-Collections aus Quellen und Wiki auf.
# Nutzt jina-embeddings-v3 mit Apple MPS Beschleunigung.
# =============================================================================
"""
Usage:
    python3 build_index.py                  # Inkrementell (nur neue/geänderte Dateien)
    python3 build_index.py --rebuild        # Voller Neuaufbau (löscht alten Index)
    python3 build_index.py --cpu            # CPU erzwingen
    python3 build_index.py --batch-size 8   # Größere Batches (wenn RAM reicht)
    python3 build_index.py --status         # Zeigt Index-Status ohne Änderungen
"""

import os
import re
import sys
import time
import argparse
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
    print("   .agent/skills/oracle/venv/bin/python3 .agent/skills/oracle/build_index.py")
    sys.exit(1)

# --- Pfade auflösen ---
SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent.parent  # .agent/skills/oracle -> repo root
MODEL_CACHE = REPO_ROOT / ".agent" / "data" / "models"
CHROMA_DIR = REPO_ROOT / ".agent" / "data" / "chroma_db"

os.environ["SENTENCE_TRANSFORMERS_HOME"] = str(MODEL_CACHE)
os.environ["HF_HOME"] = str(MODEL_CACHE / "huggingface")

# --- Konfiguration ---
EMBEDDING_MODEL = "jinaai/jina-embeddings-v3"

# Chunking: Forschungskonsens-Sweet-Spot für Retrieval (400-512 Token ≈ 2000-2800 Zeichen DE)
CHUNK_SIZE = 2500       # ~350 Token → optimal für deutsches Retrieval
CHUNK_OVERLAP = 300     # ~12% Overlap → wahrt Kontext an Grenzen
MIN_CHUNK_SIZE = 100    # Chunks unter 100 Zeichen werden verworfen

# Source-Konfiguration: Pfade → Collection + Level-Mapping
SOURCE_CONFIG = {
    "quellen": {
        "collection": "siebenwind_quellen",
        "paths": [
            {
                "dir": REPO_ROOT / "Quellen" / "Hintergrund",
                "level": "canon",
                "label": "🛡️ KANON"
            },
            {
                "dir": REPO_ROOT / "Quellen" / "Zeitung 7w Bote",
                "level": "chronicle",
                "label": "📜 CHRONIK"
            },
            {
                "dir": REPO_ROOT / "Quellen" / "Bibliothek Astrael",
                "level": "lore",
                "label": "📚 GELEHRSAMKEIT"
            },
            {
                "dir": REPO_ROOT / "Quellen" / "Bibliothek Toran Dur",
                "level": "lore",
                "label": "📚 GELEHRSAMKEIT"
            },
            {
                "dir": REPO_ROOT / "Quellen" / "Spielergeschichten",
                "level": "legend",
                "label": "🗣️ LEGENDE"
            },
        ]
    },
    "wiki": {
        "collection": "siebenwind_wiki",
        "paths": [
            {
                "dir": REPO_ROOT / "Siebenwind_Wiki",
                "level": "wiki",
                "label": "📖 WIKI"
            }
        ]
    }
}


# =============================================================================
# Chunking Engine
# =============================================================================

def strip_yaml_frontmatter(text: str) -> str:
    """Entfernt YAML-Frontmatter (---...---) vom Anfang des Textes."""
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            return text[end + 3:].lstrip("\n")
    return text


def extract_entities(text: str) -> list[str]:
    """Extrahiert [[Wiki-Links]] als Entitäten aus dem Text."""
    return list(set(re.findall(r'\[\[([^\]]+)\]\]', text)))


def extract_category(text: str) -> str:
    """Extrahiert die Kategorie aus dem YAML-Frontmatter."""
    match = re.search(r'^category:\s*(.+)$', text, re.MULTILINE)
    return match.group(1).strip() if match else ""


def semantic_chunking(text: str, chunk_size: int = CHUNK_SIZE,
                      overlap: int = CHUNK_OVERLAP) -> list[str]:
    """
    Semantic-Aware Chunking für narrative deutsche Texte.
    
    Strategie (Prioritätsreihenfolge):
    1. Kapitel-Grenzen (## Überschriften)
    2. Paragraph-Grenzen (\\n\\n)
    3. Satz-Grenzen ('. ')
    4. Zeichen-Fallback (nur wenn nötig)
    
    Overlap wird von der vorherigen Chunk-Endposition zurückgerechnet,
    sodass keine Information zwischen Chunks verloren geht.
    """
    if not text or len(text) < MIN_CHUNK_SIZE:
        return [text.strip()] if text and text.strip() else []
    
    chunks = []
    pos = 0
    text_len = len(text)
    
    while pos < text_len:
        # Endposition bestimmen
        end = min(pos + chunk_size, text_len)
        
        if end < text_len:
            # Suche die beste Split-Position (rückwärts vom Ende)
            best_split = _find_best_split(text, pos, end, chunk_size)
            if best_split > pos:
                end = best_split
        
        chunk = text[pos:end].strip()
        if chunk and len(chunk) >= MIN_CHUNK_SIZE:
            chunks.append(chunk)
        
        # Nächste Position: Ende minus Overlap
        # Mindestens 1 Zeichen Fortschritt, um Endlosschleifen zu vermeiden
        next_pos = max(pos + 1, end - overlap)
        
        # Wenn der verbleibende Text sehr kurz ist, brechen wir ab
        if next_pos >= text_len:
            break
        
        # Verbleibender Rest zu klein für eigenen Chunk? → zum letzten anhängen
        remaining = text_len - next_pos
        if remaining < MIN_CHUNK_SIZE and chunks:
            # Letzten Chunk erweitern
            chunks[-1] = text[pos:text_len].strip()
            break
        
        pos = next_pos
    
    return chunks


def _find_best_split(text: str, start: int, end: int, chunk_size: int) -> int:
    """
    Findet die beste Split-Position im Bereich [start, end].
    Priorisierung: Kapitel > Paragraph > Satz > Fallback
    """
    # Mindestens 60% des Chunks sollte gefüllt sein
    min_pos = start + int(chunk_size * 0.6)
    
    # 1. Kapitel-Grenze (## Überschrift) — suche rückwärts
    header_match = text.rfind('\n## ', min_pos, end)
    if header_match != -1:
        # Vor der Überschrift splitten (die Überschrift gehört zum nächsten Chunk)
        newline_before = text.rfind('\n', start, header_match)
        if newline_before > min_pos:
            return newline_before + 1
    
    # 2. Paragraph-Grenze (\n\n)
    para_break = text.rfind('\n\n', min_pos, end)
    if para_break != -1:
        return para_break + 2  # Nach dem Doppel-Newline
    
    # 3. Satz-Grenze ('. ' oder '.\n')
    # Suche rückwärts nach Satzenden
    for pattern in ['. ', '.\n', '! ', '!\n', '? ', '?\n']:
        sent_end = text.rfind(pattern, min_pos, end)
        if sent_end != -1:
            return sent_end + len(pattern)
    
    # 4. Einfacher Zeilenumbruch
    line_break = text.rfind('\n', min_pos, end)
    if line_break != -1:
        return line_break + 1
    
    # 5. Fallback: Harte Grenze
    return end


# =============================================================================
# Indexierungslogik
# =============================================================================

def collect_files(source_paths: list[dict]) -> list[dict]:
    """Sammelt alle .md und .txt Dateien aus den konfigurierten Pfaden."""
    files = []
    for source in source_paths:
        source_dir = source["dir"]
        if not source_dir.exists():
            print(f"  ⚠️  Verzeichnis nicht gefunden: {source_dir}")
            continue
        
        for filepath in sorted(source_dir.rglob("*")):
            if filepath.suffix.lower() in (".md", ".txt") and filepath.is_file():
                # _ARCHIV_ORIGINAL überspringen
                if "_ARCHIV_ORIGINAL" in str(filepath):
                    continue
                files.append({
                    "path": filepath,
                    "level": source["level"],
                    "label": source["label"],
                    "relative": str(filepath.relative_to(REPO_ROOT)),
                })
    return files


def process_file(file_info: dict) -> list[dict]:
    """Verarbeitet eine einzelne Datei und gibt Chunks mit Metadaten zurück."""
    try:
        raw_text = file_info["path"].read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError) as e:
        print(f"  ⚠️  Übersprungen (Lesefehler): {file_info['path'].name} – {e}")
        return []
    
    # Kategorie extrahieren BEVOR Frontmatter entfernt wird
    category = extract_category(raw_text)
    
    # Frontmatter entfernen
    clean_text = strip_yaml_frontmatter(raw_text)
    
    if len(clean_text.strip()) < MIN_CHUNK_SIZE:
        return []
    
    # Entitäten aus dem Gesamttext
    all_entities = extract_entities(clean_text)
    
    # Chunking
    chunks = semantic_chunking(clean_text)
    
    results = []
    filename = file_info["path"].stem
    
    for i, chunk_text in enumerate(chunks):
        # Chunk-spezifische Entitäten
        chunk_entities = extract_entities(chunk_text)
        
        # Kontextueller Header für bessere Embeddings
        header = f"Quelle: {file_info['path'].name} | Ebene: {file_info['level']}"
        if category:
            header += f" | Kategorie: {category}"
        
        enriched_text = f"{header}\n\n{chunk_text}"
        
        # Eindeutige ID (Dateiname + Chunk-Index)
        chunk_id = f"{filename}_chunk_{i:04d}"
        
        results.append({
            "id": chunk_id,
            "text": enriched_text,
            "metadata": {
                "source": file_info["relative"],
                "level": file_info["level"],
                "category": category,
                "entities": ", ".join(chunk_entities[:20]),  # Max 20 Entitäten
                "chunk_index": i,
                "total_chunks": len(chunks),
                "char_count": len(chunk_text),
            }
        })
    
    return results


def get_indexed_files(collection) -> dict[str, float]:
    """Liest alle bereits indexierten Dateien + deren mtime aus der Collection."""
    indexed = {}
    try:
        # Wir holen ALLE Metadaten, aber nur die 'source' und 'mtime' Felder
        # ChromaDB hat kein 'distinct', also holen wir alles und deduplizieren
        result = collection.get(
            include=["metadatas"],
        )
        if result and result["metadatas"]:
            for meta in result["metadatas"]:
                source = meta.get("source", "")
                mtime = meta.get("mtime", 0)
                if source and source not in indexed:
                    indexed[source] = float(mtime)
    except Exception:
        pass
    return indexed


def remove_file_chunks(collection, source_path: str):
    """Entfernt alle Chunks einer bestimmten Datei aus der Collection."""
    try:
        # ChromaDB WHERE-Filter auf Metadaten
        result = collection.get(
            where={"source": source_path},
            include=[],
        )
        if result and result["ids"]:
            collection.delete(ids=result["ids"])
            return len(result["ids"])
    except Exception:
        pass
    return 0


def build_collection(client, collection_name: str, source_key: str, model, batch_size: int, rebuild: bool = False):
    """Baut eine ChromaDB-Collection auf (inkrementell oder voll)."""
    config = SOURCE_CONFIG[source_key]
    files = collect_files(config["paths"])
    
    if not files:
        print(f"  ❌ Keine Dateien gefunden für '{source_key}'.")
        return 0, 0
    
    if rebuild:
        # Voller Neuaufbau
        try:
            client.delete_collection(collection_name)
            print(f"  🗑️  Collection '{collection_name}' gelöscht (Rebuild).")
        except Exception:
            pass
    
    collection = client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )
    
    # Bereits indexierte Dateien ermitteln
    indexed_files = get_indexed_files(collection) if not rebuild else {}
    
    # Dateien klassifizieren
    current_sources = set()
    files_to_process = []
    skipped = 0
    
    for file_info in files:
        rel_path = file_info["relative"]
        current_sources.add(rel_path)
        file_mtime = file_info["path"].stat().st_mtime
        
        if rel_path in indexed_files:
            old_mtime = indexed_files[rel_path]
            if abs(file_mtime - old_mtime) < 1.0:  # Gleiche mtime → unverändert
                skipped += 1
                continue
            else:
                # Datei geändert → alte Chunks entfernen
                removed = remove_file_chunks(collection, rel_path)
                if removed:
                    print(f"  🔄 Aktualisiert: {file_info['path'].name} ({removed} alte Chunks entfernt)")
        
        file_info["mtime"] = file_mtime
        files_to_process.append(file_info)
    
    # Gelöschte Dateien aufräumen
    deleted_sources = set(indexed_files.keys()) - current_sources
    for deleted in deleted_sources:
        removed = remove_file_chunks(collection, deleted)
        if removed:
            print(f"  🗑️  Entfernt: {deleted} ({removed} Chunks)")
    
    if not files_to_process:
        existing_count = collection.count()
        print(f"\n  ✅ '{collection_name}': Keine Änderungen. {existing_count} Chunks aktuell.")
        if skipped:
            print(f"     ({skipped} Dateien übersprungen, {len(deleted_sources)} gelöscht)")
        return len(files), existing_count
    
    print(f"\n  📂 Verarbeite {len(files_to_process)} von {len(files)} Dateien "
          f"({skipped} übersprungen, {len(deleted_sources)} gelöscht)...")
    
    # =========================================================================
    # PER-FILE PIPELINE: Chunk → Embed → Save (sofort persistent!)
    # Jede fertig verarbeitete Datei ist sofort in der DB gesichert.
    # Bei Ctrl+C geht nur die aktuelle Datei verloren.
    # =========================================================================
    start_time = time.time()
    total_new_chunks = 0
    
    for idx, file_info in enumerate(files_to_process, 1):
        # 1. Chunk
        chunks = process_file(file_info)
        
        if not chunks:
            _print_progress(idx, len(files_to_process), file_info, 0, start_time, "übersprungen")
            continue
        
        # mtime in Metadaten einfügen
        for chunk in chunks:
            chunk["metadata"]["mtime"] = file_info["mtime"]
        
        # 2. Embed (nur die Chunks dieser Datei)
        texts = [c["text"] for c in chunks]
        embeddings = model.encode(
            texts,
            task="retrieval.passage",
            show_progress_bar=False,
            batch_size=batch_size,
        ).tolist()
        
        # 3. Save (sofort in ChromaDB)
        collection.add(
            ids=[c["id"] for c in chunks],
            embeddings=embeddings,
            documents=[c["text"] for c in chunks],
            metadatas=[c["metadata"] for c in chunks],
        )
        
        total_new_chunks += len(chunks)
        _print_progress(idx, len(files_to_process), file_info, len(chunks), start_time, "gespeichert")
    
    print()  # Neue Zeile nach Fortschrittsbalken
    
    total_time = time.time() - start_time
    final_count = collection.count()
    
    if total_new_chunks > 0:
        speed = total_new_chunks / total_time if total_time > 0 else 0
        print(f"  ✅ Collection '{collection_name}': {final_count} Chunks total "
              f"(+{total_new_chunks} neu, {speed:.1f} Chunks/s) in {total_time:.1f}s")
    else:
        print(f"  ✅ '{collection_name}': Keine neuen Chunks.")
    
    return len(files), final_count


def _print_progress(idx: int, total: int, file_info: dict, n_chunks: int, 
                    start_time: float, status: str):
    """Zeigt den Fortschrittsbalken an."""
    elapsed = time.time() - start_time
    if idx > 1 and elapsed > 0:
        avg_time = elapsed / (idx - 1)
        remaining = avg_time * (total - idx)
        eta = f"~{remaining:.0f}s"
    else:
        eta = "..."
    
    bar_width = 30
    progress = idx / total
    filled = int(bar_width * progress)
    bar = "━" * filled + "╺" + "─" * (bar_width - filled - 1)
    
    chunk_info = f"({n_chunks} {status})" if n_chunks else f"({status})"
    print(f"\r  [{idx}/{total}] {file_info['path'].name[:35]:<35} {chunk_info:<20} "
          f"{bar} {progress*100:5.1f}% | {elapsed:.0f}s | ETA {eta}", end="", flush=True)


# =============================================================================
# Main
# =============================================================================

def main():
    # Config laden falls vorhanden
    config_path = SCRIPT_DIR / "config.json"
    default_device = "mps" if sys.platform == "darwin" else "cpu"
    default_batch = 4
    
    if config_path.exists():
        import json
        try:
            with open(config_path) as f:
                cfg = json.load(f)
                if "device" in cfg: default_device = cfg["device"]
                if "batch_size" in cfg: default_batch = cfg["batch_size"]
            print(f"📋 Config geladen: {default_device.upper()} (Batch: {default_batch})")
        except Exception as e:
            print(f"⚠️  Config-Fehler: {e}")

    parser = argparse.ArgumentParser(description="Das Orakel – Index Builder")
    parser.add_argument("--source", choices=["quellen", "wiki", "all"],
                        default="all", help="Welche Quelle indexiert werden soll")
    parser.add_argument("--cpu", action="store_true", help="Erzwingt CPU statt MPS")
    parser.add_argument("--batch-size", type=int, default=default_batch, 
                        help=f"Batch-Größe (Default aus Config: {default_batch})")
    parser.add_argument("--rebuild", action="store_true",
                        help="Erzwingt vollen Neuaufbau (löscht alten Index)")
    parser.add_argument("--status", action="store_true",
                        help="Zeigt nur den Index-Status an")
    args = parser.parse_args()
    
    print("╔═══════════════════════════════════════════════════╗")
    print("║   Das Orakel – Indexierung                       ║")
    print("╚═══════════════════════════════════════════════════╝")
    print(f"  Repo:        {REPO_ROOT}")
    print(f"  Chunk-Größe: {CHUNK_SIZE} Zeichen (~{CHUNK_SIZE // 7} Token)")
    print(f"  Modell:      {EMBEDDING_MODEL}")
    print(f"  Modus:       {'🔄 REBUILD (Voll)' if args.rebuild else '⚡ INKREMENTELL'}")
    
    # ChromaDB Client (wird für --status UND Indexierung gebraucht)
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    import chromadb
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    
    # Status-Modus: Nur anzeigen, nichts ändern
    if args.status:
        print("\n  📊 Index-Status:")
        for source_key in ["quellen", "wiki"]:
            coll_name = SOURCE_CONFIG[source_key]["collection"]
            try:
                coll = client.get_collection(coll_name)
                count = coll.count()
                indexed = get_indexed_files(coll)
                print(f"     {coll_name}: {count} Chunks aus {len(indexed)} Dateien")
            except Exception:
                print(f"     {coll_name}: ❌ Nicht vorhanden")
        sys.exit(0)
    
    # Modell laden
    print("\n  🧠 Lade Embedding-Modell...")
    from sentence_transformers import SentenceTransformer
    
    # Device-Logik: --cpu Flag sticht Config
    if args.cpu:
        device = "cpu"
    else:
        device = default_device
        
    print(f"  🔌 Device: {device.upper()} (Batch-Size: {args.batch_size})")

    model = SentenceTransformer(
        EMBEDDING_MODEL,
        trust_remote_code=True,
        device=device,
    )
    print(f"  ✅ Modell geladen")
    
    # Indexierung
    total_files = 0
    total_chunks = 0
    
    sources_to_build = (
        ["quellen", "wiki"] if args.source == "all"
        else [args.source]
    )
    
    for source_key in sources_to_build:
        n_files, n_chunks = build_collection(
            client,
            SOURCE_CONFIG[source_key]["collection"],
            source_key,
            model,
            args.batch_size,
            rebuild=args.rebuild,
        )
        total_files += n_files
        total_chunks += n_chunks
    
    # Zusammenfassung
    print("\n╔═══════════════════════════════════════════════════╗")
    print(f"║   ✅ Indexierung fertig!                         ║")
    print(f"║   {total_chunks:>6} Chunks aus {total_files} Dokumenten             ║")
    print(f"║   DB-Pfad: {str(CHROMA_DIR):<38} ║")
    print("╚═══════════════════════════════════════════════════╝")


if __name__ == "__main__":
    main()
