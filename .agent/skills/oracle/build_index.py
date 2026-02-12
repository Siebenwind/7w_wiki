#!/usr/bin/env python3
# =============================================================================
# Das Orakel – Index Builder
# Baut zwei separate ChromaDB-Collections aus Quellen und Wiki auf.
# Nutzt jina-embeddings-v3 mit Apple MPS Beschleunigung.
# =============================================================================
"""
Usage:
    python3 build_index.py                  # Standard (MPs, Batch-Size 4)
    python3 build_index.py --cpu            # CPU erzwingen (falls MPS crasht/langsam)
    python3 build_index.py --batch-size 8   # Größere Batches (wenn RAM reicht)
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


def build_collection(client, collection_name: str, source_key: str, model, batch_size: int):
    """Baut eine einzelne ChromaDB-Collection auf."""
    config = SOURCE_CONFIG[source_key]
    files = collect_files(config["paths"])
    
    if not files:
        print(f"  ❌ Keine Dateien gefunden für '{source_key}'.")
        return 0, 0
    
    # Alte Collection löschen
    try:
        client.delete_collection(collection_name)
    except Exception:
        pass
    
    collection = client.create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}
    )
    
    all_chunks = []
    start_time = time.time()
    
    print(f"\n  📂 Verarbeite {len(files)} Dateien für '{collection_name}'...")
    
    for idx, file_info in enumerate(files, 1):
        chunks = process_file(file_info)
        
        # Fortschrittsanzeige
        elapsed = time.time() - start_time
        if idx > 1:
            avg_time = elapsed / (idx - 1)
            remaining = avg_time * (len(files) - idx)
            eta = f"~{remaining:.0f}s verbleibend"
        else:
            eta = "berechne..."
        
        bar_width = 30
        progress = idx / len(files)
        filled = int(bar_width * progress)
        bar = "━" * filled + "╺" + "─" * (bar_width - filled - 1)
        
        chunk_info = f"({len(chunks)} Chunks)" if chunks else "(übersprungen)"
        print(f"\r  [{idx}/{len(files)}] {file_info['path'].name[:40]:<40} {chunk_info:<16} "
              f"{bar} {progress*100:5.1f}% | {elapsed:.0f}s | {eta}", end="", flush=True)
        
        all_chunks.extend(chunks)
    
    print()  # Neue Zeile nach Fortschrittsbalken
    
    if not all_chunks:
        print(f"  ❌ Keine Chunks generiert.")
        return len(files), 0
    
    # Embeddings generieren
    print(f"\n  🧠 Generiere Embeddings für {len(all_chunks)} Chunks...")
    embed_start = time.time()
    
    texts = [c["text"] for c in all_chunks]
    
    # Batch-Embedding mit MPS-Beschleunigung
    # task='retrieval.passage' nutzt den passenden LoRA-Adapter
    # Batch-Size wird vom Main durchgereicht, hier hartcodiert -> Fix nötig
    # Wir übergeben jetzt batch_size an build_collection oder nutzen globales args?
    # Besser: build_collection bekommt batch_size
    embeddings = model.encode(
        texts,
        task="retrieval.passage",
        show_progress_bar=True,
        batch_size=batch_size,
    ).tolist()
    
    embed_time = time.time() - embed_start
    print(f"  ✅ Embeddings in {embed_time:.1f}s generiert "
          f"({len(all_chunks) / embed_time:.0f} Chunks/Sek)")
    
    # In ChromaDB speichern (Batches von 200)
    print(f"  💾 Speichere in ChromaDB...")
    batch_size = 200
    for i in range(0, len(all_chunks), batch_size):
        batch_end = min(i + batch_size, len(all_chunks))
        collection.add(
            ids=[c["id"] for c in all_chunks[i:batch_end]],
            embeddings=embeddings[i:batch_end],
            documents=[c["text"] for c in all_chunks[i:batch_end]],
            metadatas=[c["metadata"] for c in all_chunks[i:batch_end]],
        )
    
    total_time = time.time() - start_time
    print(f"  ✅ Collection '{collection_name}': {len(all_chunks)} Chunks "
          f"aus {len(files)} Dateien in {total_time:.1f}s")
    
    return len(files), len(all_chunks)


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
    args = parser.parse_args()
    
    print("╔═══════════════════════════════════════════════════╗")
    print("║   Das Orakel – Indexierung                       ║")
    print("╚═══════════════════════════════════════════════════╝")
    print(f"  Repo:        {REPO_ROOT}")
    print(f"  Chunk-Größe: {CHUNK_SIZE} Zeichen (~{CHUNK_SIZE // 7} Token)")
    print(f"  Modell:      {EMBEDDING_MODEL}")
    
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
    
    # ChromaDB Client
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    import chromadb
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    
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
