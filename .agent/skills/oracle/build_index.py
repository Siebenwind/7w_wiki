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
import json
import hashlib
import argparse
import uuid
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str((Path(__file__).resolve().parents[2] / "scripts")))

from content_contract import TECHNICAL_WIKI_ROOT

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
RUNTIME_CONFIG_PATH = REPO_ROOT / ".agent" / "config" / "runtime.json"
ARCHIVE_REGISTER_DIR = REPO_ROOT / "System" / "Archivregister"
ARCHIVE_REGISTER_JSON = ARCHIVE_REGISTER_DIR / "ARCHIVREGISTER.json"
ARCHIVE_REGISTER_MD = ARCHIVE_REGISTER_DIR / "ARCHIVREGISTER.md"
ARCHIVE_REGISTER_NAMESPACE = uuid.UUID("6bc810f8-2e4f-4ad0-8b19-8f0b72566b70")

os.environ["SENTENCE_TRANSFORMERS_HOME"] = str(MODEL_CACHE)
os.environ["HF_HOME"] = str(MODEL_CACHE / "huggingface")

def is_offline_runtime() -> bool:
    """Erkennt Sandboxes/Offline-Umgebungen robust."""
    return any([
        os.environ.get("ANTIGRAVITY_SANDBOX") == "true",
        os.environ.get("ANTIGRAVITY_AGENT") == "1",
        bool(os.environ.get("CODEX_SANDBOX")),
        os.environ.get("CODEX_SANDBOX_NETWORK_DISABLED") == "1",
        os.environ.get("HF_HUB_OFFLINE") == "1",
        os.environ.get("TRANSFORMERS_OFFLINE") == "1",
    ])

if is_offline_runtime():
    os.environ["HF_HUB_OFFLINE"] = "1"
    os.environ["TRANSFORMERS_OFFLINE"] = "1"

def resolve_device(device: str | None) -> str:
    """Standard-Fallback: MPS nur nutzen, wenn zur Laufzeit verfügbar und schreibberechtigt."""
    if device is None:
        device = "mps" if sys.platform == "darwin" else "cpu"
    if device != "mps":
        return device
    try:
        import torch
        if not torch.backends.mps.is_available():
            return "cpu"
        # PROBE-Check: Dürfen wir MPS schreiben? (Vermeidet mpsgraph permission errors)
        try:
            t = torch.ones(1, device="mps")
            del t
        except Exception:
            return "cpu"
        return "mps"
    except Exception:
        pass
    return "cpu"

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
                "dir": TECHNICAL_WIKI_ROOT,
                "level": "wiki",
                "label": "📖 WIKI"
            }
        ]
    }
}

REGISTER_CORPORA = [
    ("wiki", TECHNICAL_WIKI_ROOT),
    ("quellen", REPO_ROOT / "Quellen"),
    ("system", REPO_ROOT / "System"),
    ("docs", REPO_ROOT / "docs"),
]

REGISTER_EXTENSIONS = {".md", ".txt", ".json"}


# =============================================================================
# Chunking Engine
# =============================================================================

def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def to_iso(ts: float) -> str:
    return datetime.fromtimestamp(ts, tz=timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def extract_frontmatter_uuid(raw_text: str) -> str:
    """Extrahiert uuid aus YAML-Frontmatter, falls vorhanden."""
    if not raw_text.startswith("---"):
        return ""
    end = raw_text.find("\n---", 3)
    if end == -1:
        return ""
    frontmatter = raw_text[:end]
    match = re.search(r"^uuid:\s*([^\n]+)$", frontmatter, re.MULTILINE)
    return match.group(1).strip() if match else ""


def parse_inventur_progress() -> dict:
    """Liest Inventur-Status aus Logs/INVENTUR_QUELLEN.md."""
    inv_path = REPO_ROOT / "Logs" / "INVENTUR_QUELLEN.md"
    if not inv_path.exists():
        return {"total": 0, "pending": 0, "processed": 0}

    total = 0
    pending = 0
    for line in inv_path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line.startswith("|") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) < 4:
            continue
        status = cells[-1].lower()
        total += 1
        if status.startswith("pending"):
            pending += 1

    processed = max(0, total - pending)
    return {"total": total, "pending": pending, "processed": processed}


def parse_frontmatter_state(path: Path) -> dict:
    """Liest id/uuid/status aus Frontmatter, sofern vorhanden."""
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception:
        return {"id": "", "uuid": "", "status": ""}

    if not raw.startswith("---"):
        return {"id": "", "uuid": "", "status": ""}
    end = raw.find("\n---", 3)
    if end == -1:
        return {"id": "", "uuid": "", "status": ""}
    frontmatter = raw[:end]

    id_match = re.search(r"^id:\s*([^\n]+)$", frontmatter, re.MULTILINE)
    uuid_match = re.search(r"^uuid:\s*([^\n]+)$", frontmatter, re.MULTILINE)
    status_match = re.search(r"^status:\s*([^\n#]+)$", frontmatter, re.MULTILINE)
    return {
        "id": id_match.group(1).strip() if id_match else "",
        "uuid": uuid_match.group(1).strip() if uuid_match else "",
        "status": status_match.group(1).strip() if status_match else "",
    }


def collect_board_metrics() -> dict:
    """Sammelt operative Metriken für Dispatch, Research und Conflict-Boards."""
    board_root = REPO_ROOT / "System" / "Synapse_Board"
    dispatch_dir = board_root / "DISPATCH"
    inq_dir = board_root / "SILICON_INQUISITION"

    def scan(glob_pattern: str, allowed: set[str]) -> dict:
        files = sorted(board_root.glob(glob_pattern))
        status_counts = {k: 0 for k in sorted(allowed)}
        invalid = []
        missing_uuid = 0
        for file in files:
            fm = parse_frontmatter_state(file)
            status = fm["status"].upper()
            if not fm["uuid"]:
                missing_uuid += 1
            if status in allowed:
                status_counts[status] = status_counts.get(status, 0) + 1
            else:
                invalid.append(str(file.relative_to(REPO_ROOT)))
        return {
            "total": len(files),
            "status_counts": status_counts,
            "invalid_status_files": invalid,
            "missing_uuid": missing_uuid,
        }

    dispatch_files = sorted(dispatch_dir.glob("MSG-*.md")) if dispatch_dir.exists() else []
    dispatch_status = {"OPEN": 0, "CLAIMED": 0, "DONE": 0}
    dispatch_invalid = []
    dispatch_missing_uuid = 0
    for file in dispatch_files:
        fm = parse_frontmatter_state(file)
        status = fm["status"].upper()
        if not fm["uuid"]:
            dispatch_missing_uuid += 1
        if status in dispatch_status:
            dispatch_status[status] += 1
        else:
            dispatch_invalid.append(str(file.relative_to(REPO_ROOT)))

    research = scan(
        "RESEARCH-*.md",
        {
            "OPEN_HISTORIAN",
            "IN_REVIEW_HISTORIAN",
            "AWAITING_HUMAN_DECISION",
            "RESOLVED",
            "THEMATIC_BACKLOG",
            "DEFERRED",
            "PARKED",
            "DONE",
            "COMPLETED",
        },
    )
    conflicts = scan("Conflict_*.md", {"NEEDS_REVIEW", "RESEARCHING", "AWAITING_USER", "AUTO_RESOLVED", "HUMAN_RESOLVED", "RESOLVED"})

    inq_files = sorted(inq_dir.glob("*.md")) if inq_dir.exists() else []
    inq_status_counts = {}
    inq_missing_uuid = 0
    for file in inq_files:
        fm = parse_frontmatter_state(file)
        status = fm["status"].upper() if fm["status"] else "UNSPECIFIED"
        inq_status_counts[status] = inq_status_counts.get(status, 0) + 1
        if not fm["uuid"]:
            inq_missing_uuid += 1

    return {
        "dispatch": {
            "total": len(dispatch_files),
            "status_counts": dispatch_status,
            "invalid_status_files": dispatch_invalid,
            "missing_uuid": dispatch_missing_uuid,
        },
        "research": research,
        "conflicts": conflicts,
        "inquisition": {
            "total": len(inq_files),
            "status_counts": inq_status_counts,
            "missing_uuid": inq_missing_uuid,
        },
    }


def _register_record_for_file(corpus: str, path: Path) -> dict | None:
    if path.suffix.lower() not in REGISTER_EXTENSIONS or not path.is_file():
        return None

    rel = path.relative_to(REPO_ROOT)
    stat = path.stat()
    rel_str = str(rel)
    record_uuid = str(uuid.uuid5(ARCHIVE_REGISTER_NAMESPACE, rel_str))

    content_uuid = ""
    content_hash = ""
    try:
        raw = path.read_text(encoding="utf-8")
        content_uuid = extract_frontmatter_uuid(raw)
        content_hash = hashlib.sha256(raw.encode("utf-8")).hexdigest()[:16]
    except Exception:
        # Binäre/inkonsistente Dateien dürfen das Register nicht blockieren.
        content_hash = ""

    rag_source = corpus if corpus in ("wiki", "quellen") else ""
    indexable = bool(rag_source and path.suffix.lower() in {".md", ".txt"})

    return {
        "record_uuid": record_uuid,
        "filename": path.name,
        "relative_path": rel_str,
        "corpus": corpus,
        "extension": path.suffix.lower(),
        "size_bytes": stat.st_size,
        "modified_at": to_iso(stat.st_mtime),
        "content_uuid": content_uuid,
        "has_content_uuid": bool(content_uuid),
        "indexable": indexable,
        "rag_source": rag_source,
        "content_hash": content_hash,
    }


def build_archive_register(rag_progress: dict) -> tuple[dict, Path, Path]:
    """Erstellt zentrales Archivregister (JSON + Markdown Summary)."""
    records = []
    corpus_counts = {name: 0 for name, _ in REGISTER_CORPORA}

    for corpus, root in REGISTER_CORPORA:
        if not root.exists():
            continue
        for path in sorted(root.rglob("*")):
            rec = _register_record_for_file(corpus, path)
            if rec is None:
                continue
            records.append(rec)
            corpus_counts[corpus] += 1

    total_records = len(records)
    with_content_uuid = sum(1 for r in records if r["has_content_uuid"])
    uuid_coverage = (with_content_uuid / total_records * 100.0) if total_records else 0.0

    indexable_total = {
        "wiki": sum(1 for r in records if r["indexable"] and r["rag_source"] == "wiki"),
        "quellen": sum(1 for r in records if r["indexable"] and r["rag_source"] == "quellen"),
    }

    inventur = parse_inventur_progress()
    board_metrics = collect_board_metrics()

    payload = {
        "register_uuid": str(uuid.uuid4()),
        "generated_at": now_iso(),
        "repo_root": str(REPO_ROOT),
        "stats": {
            "total_records": total_records,
            "with_content_uuid": with_content_uuid,
            "uuid_coverage_pct": round(uuid_coverage, 2),
            "by_corpus": corpus_counts,
            "indexable_total": indexable_total,
            "rag_progress": rag_progress,
            "inventur_progress": inventur,
            "board_metrics": board_metrics,
        },
        "records": records,
    }

    ARCHIVE_REGISTER_DIR.mkdir(parents=True, exist_ok=True)
    ARCHIVE_REGISTER_JSON.write_text(
        json.dumps(payload, ensure_ascii=True, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    lines = []
    lines.append("---")
    lines.append("layout: wiki_page")
    lines.append("title: Archivregister")
    lines.append("category: System")
    lines.append(f"uuid: {payload['register_uuid']}")
    lines.append(f"letzter_check: {payload['generated_at']}")
    lines.append("---")
    lines.append("")
    lines.append("# Archivregister")
    lines.append("")
    lines.append("**Epistemischer Status:** #meta")
    lines.append("")
    lines.append("## Überblick")
    lines.append("")
    lines.append(f"- Datensaetze gesamt: {total_records}")
    lines.append(f"- Mit Content-UUID: {with_content_uuid} ({uuid_coverage:.2f}%)")
    lines.append(f"- Wiki indexierbar: {indexable_total['wiki']} | Quellen indexierbar: {indexable_total['quellen']}")
    lines.append("")
    lines.append("## RAG-Fortschritt")
    lines.append("")
    lines.append("| Corpus | Indexierte Dateien | Indexierbare Dateien | Coverage | Chunks | Stale Index-Eintraege |")
    lines.append("|---|---:|---:|---:|---:|---:|")
    for key in ("wiki", "quellen"):
        p = rag_progress.get(key, {})
        lines.append(
            f"| {key} | {p.get('indexed_files', 0)} | {p.get('indexable_files', 0)} | {p.get('coverage_pct', 0.0):.2f}% | {p.get('chunks', 0)} | {p.get('stale_index_entries', 0)} |"
        )
    lines.append("")
    lines.append("## Ingestion-Fortschritt (Inventur)")
    lines.append("")
    lines.append(
        f"- INVENTUR_QUELLEN: {inventur.get('processed', 0)}/{inventur.get('total', 0)} verarbeitet; Pending: {inventur.get('pending', 0)}"
    )
    lines.append("")
    lines.append("## Dispatch & Board Status")
    lines.append("")
    dispatch = board_metrics["dispatch"]
    lines.append("| Domain | Total | Status Breakdown | Missing UUID | Invalid Status Files |")
    lines.append("|---|---:|---|---:|---:|")

    def _render_status_counts(status_counts: dict) -> str:
        parts = [f"{k}={v}" for k, v in sorted(status_counts.items()) if v > 0]
        return ", ".join(parts) if parts else "-"

    lines.append(
        f"| Dispatch | {dispatch['total']} | {_render_status_counts(dispatch['status_counts'])} | {dispatch['missing_uuid']} | {len(dispatch['invalid_status_files'])} |"
    )

    for name in ("research", "conflicts", "inquisition"):
        section = board_metrics[name]
        lines.append(
            f"| {name} | {section['total']} | {_render_status_counts(section['status_counts'])} | {section.get('missing_uuid', 0)} | {len(section.get('invalid_status_files', []))} |"
        )
    lines.append("")

    if dispatch["invalid_status_files"]:
        lines.append("### Dispatch: Ungueltige Stati")
        lines.append("")
        for rel in dispatch["invalid_status_files"][:10]:
            lines.append(f"- `{rel}`")
        if len(dispatch["invalid_status_files"]) > 10:
            lines.append(f"- ... (+{len(dispatch['invalid_status_files']) - 10} weitere)")
        lines.append("")

    lines.append("## Corpus-Verteilung")
    lines.append("")
    lines.append("| Corpus | Dateien |")
    lines.append("|---|---:|")
    for corpus in ("wiki", "quellen", "system", "docs"):
        lines.append(f"| {corpus} | {corpus_counts.get(corpus, 0)} |")
    lines.append("")
    lines.append("## Pflichtfelder je Datensatz")
    lines.append("")
    lines.append("- `record_uuid` (deterministisch aus Pfad)")
    lines.append("- `filename`")
    lines.append("- `relative_path`")
    lines.append("- `content_uuid` (falls Frontmatter vorhanden)")
    lines.append("- `indexable`, `rag_source`, `modified_at`, `content_hash`")
    lines.append("")
    lines.append("## Vollregister")
    lines.append("")
    lines.append("- Siehe `System/Archivregister/ARCHIVREGISTER.json`")
    lines.append("")

    missing_uuid = [r["relative_path"] for r in records if not r["has_content_uuid"] and r["extension"] == ".md"]
    if missing_uuid:
        lines.append("## UUID-Lücken (Markdown, Top 25)")
        lines.append("")
        for rel in missing_uuid[:25]:
            lines.append(f"- `{rel}`")
        if len(missing_uuid) > 25:
            lines.append(f"- ... (+{len(missing_uuid) - 25} weitere)")
        lines.append("")

    ARCHIVE_REGISTER_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return payload, ARCHIVE_REGISTER_MD, ARCHIVE_REGISTER_JSON


def collect_rag_progress(client) -> dict:
    """Berechnet Coverage-/Chunk-Status je RAG-Quelle."""
    rag_progress: dict[str, dict] = {}
    for source_key in ("quellen", "wiki"):
        coll_name = SOURCE_CONFIG[source_key]["collection"]
        current_files = collect_files(SOURCE_CONFIG[source_key]["paths"])
        current_sources = {f["relative"] for f in current_files}
        indexable_files = len(current_sources)

        chunks = 0
        indexed_files = 0
        stale_index_entries = 0
        stale_examples: list[str] = []
        available = True
        error = ""

        try:
            coll = client.get_collection(coll_name)
            chunks = coll.count()
            indexed = get_indexed_files(coll)
            indexed_sources = set(indexed.keys())
            indexed_files = len(indexed_sources.intersection(current_sources))
            stale = sorted(indexed_sources - current_sources)
            stale_index_entries = len(stale)
            stale_examples = stale[:10]
        except Exception as e:
            available = False
            error = str(e)
            if "does not exist" not in error:
                print(f"     {coll_name}: ❌ Fehler beim Lesen: {error}")

        coverage = (indexed_files / indexable_files * 100.0) if indexable_files else 0.0
        rag_progress[source_key] = {
            "collection": coll_name,
            "available": available,
            "error": error,
            "chunks": chunks,
            "indexed_files": indexed_files,
            "indexable_files": indexable_files,
            "coverage_pct": round(coverage, 2),
            "stale_index_entries": stale_index_entries,
            "stale_examples": stale_examples,
        }
    return rag_progress


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
    
    # Content-Hash über den gesamten bereinigten Text
    content_hash = hashlib.sha256(clean_text.encode("utf-8")).hexdigest()[:16]
    
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
                "content_hash": content_hash,
            }
        })
    
    return results


def get_indexed_files(collection) -> dict[str, dict]:
    """Liest alle indexierten Dateien mit mtime und content_hash.
    
    Returns: {source_path: {"mtime": float, "hash": str, "ids": [str]}}
    """
    indexed = {}
    try:
        count = collection.count()
        if count == 0:
            return {}
            
        batch_size = 5000
        for offset in range(0, count, batch_size):
            result = collection.get(
                include=["metadatas"],
                limit=batch_size,
                offset=offset
            )
            if result and result["metadatas"]:
                for chunk_id, meta in zip(result["ids"], result["metadatas"]):
                    source = meta.get("source", "")
                    if not source:
                        continue
                    if source not in indexed:
                        indexed[source] = {
                            "mtime": float(meta.get("mtime", 0)),
                            "hash": meta.get("content_hash", ""),
                            "ids": [],
                        }
                    indexed[source]["ids"].append(chunk_id)
    except Exception as e:
        print(f"  ⚠️  Fehler beim Lesen des Index-Status: {e}")
    return indexed


def remove_file_chunks(collection, source_path: str = None, chunk_ids: list = None):
    """Entfernt Chunks aus der Collection (per Pfad oder IDs)."""
    try:
        if chunk_ids:
            collection.delete(ids=chunk_ids)
            return len(chunk_ids)
        elif source_path:
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


def update_chunk_metadata(collection, chunk_ids: list, new_source: str):
    """Aktualisiert den source-Pfad bestehender Chunks (für Renames)."""
    try:
        for chunk_id in chunk_ids:
            collection.update(
                ids=[chunk_id],
                metadatas=[{"source": new_source}],
            )
    except Exception as e:
        print(f"  ⚠️  Metadata-Update fehlgeschlagen: {e}")


def build_collection(client, collection_name: str, source_key: str, model, batch_size: int, rebuild: bool = False, target_file: str = None):
    """Baut eine ChromaDB-Collection auf (inkrementell oder voll)."""
    config = SOURCE_CONFIG[source_key]
    files = collect_files(config["paths"])
    
    if target_file:
        # Filter auf spezifische Datei
        # Wir prüfen, ob der Pfad auf die Zieldatei endet (flexibel für rel/abs Pfade)
        files = [f for f in files if str(f["path"]).endswith(target_file)]
        if not files:
            # Datei ist nicht in dieser Source (macht nichts, vielleicht in der anderen)
            return 0, 0
    
    if not files:
        if not target_file:
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
    
    # Hash-Index für Rename-Erkennung: {hash -> (source, info)}
    hash_to_source = {}
    for src, info in indexed_files.items():
        if info["hash"]:
            hash_to_source[info["hash"]] = (src, info)
    
    # Dateien klassifizieren
    current_sources = set()
    files_to_process = []
    skipped = 0
    renamed = 0
    
    for file_info in files:
        rel_path = file_info["relative"]
        current_sources.add(rel_path)
        file_mtime = file_info["path"].stat().st_mtime
        
        # Content-Hash berechnen
        try:
            raw = file_info["path"].read_text(encoding="utf-8")
            clean = strip_yaml_frontmatter(raw)
            file_hash = hashlib.sha256(clean.encode("utf-8")).hexdigest()[:16]
        except Exception:
            file_hash = ""
        
        file_info["mtime"] = file_mtime
        file_info["content_hash"] = file_hash
        
        if rel_path in indexed_files:
            old_info = indexed_files[rel_path]
            if old_info["hash"] and file_hash:
                # Beide haben Hash → Hash-Vergleich (zuverlässigste Methode)
                if old_info["hash"] == file_hash:
                    skipped += 1
                    continue
                else:
                    # Content geändert → re-index
                    removed = remove_file_chunks(collection, chunk_ids=old_info["ids"])
                    if removed:
                        print(f"  🔄 Geändert: {file_info['path'].name} ({removed} Chunks entfernt)")
                    files_to_process.append(file_info)
            else:
                # Legacy-Daten ohne Hash → Fallback auf mtime
                if abs(file_mtime - old_info["mtime"]) < 1.0:
                    skipped += 1
                    continue
                else:
                    removed = remove_file_chunks(collection, chunk_ids=old_info["ids"])
                    if removed:
                        print(f"  🔄 Geändert (mtime): {file_info['path'].name} ({removed} Chunks entfernt)")
                    files_to_process.append(file_info)
        elif file_hash and file_hash in hash_to_source:
            # Neuer Pfad, aber gleicher Content → Rename!
            old_source, old_info = hash_to_source[file_hash]
            update_chunk_metadata(collection, old_info["ids"], rel_path)
            print(f"  📝 Rename: {Path(old_source).name} → {file_info['path'].name} "
                  f"({len(old_info['ids'])} Chunks behalten)")
            renamed += 1
            current_sources.add(old_source)
            skipped += 1
        else:
            # Komplett neue Datei
            files_to_process.append(file_info)
    
    # Gelöschte Dateien aufräumen (NUR wenn wir nicht im Single-File-Modus sind)
    deleted_sources = set()
    if not target_file:
        deleted_sources = set(indexed_files.keys()) - current_sources
        for deleted in deleted_sources:
            removed = remove_file_chunks(collection, chunk_ids=indexed_files[deleted]["ids"])
            if removed:
                print(f"  🗑️  Entfernt: {Path(deleted).name} ({removed} Chunks)")
    
    if not files_to_process:
        existing_count = collection.count()
        print(f"\n  ✅ '{collection_name}': Keine Änderungen. {existing_count} Chunks aktuell.")
        if skipped or renamed:
            print(f"     ({skipped} übersprungen, {renamed} umbenannt, {len(deleted_sources)} gelöscht)")
        return len(files), existing_count
    
    print(f"\n  📂 Verarbeite {len(files_to_process)} von {len(files)} Dateien "
          f"({skipped} übersprungen, {renamed} umbenannt, {len(deleted_sources)} gelöscht)...")
    
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
        _print_progress(idx, len(files_to_process), file_info, len(chunks), 
                        start_time, total_new_chunks)
    
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
                    start_time: float, total_chunks: int):
    """Zeigt den Fortschrittsbalken an."""
    elapsed = time.time() - start_time
    throughput = total_chunks / elapsed if elapsed > 0 else 0
    
    # ETA als HH:MM:SS
    if idx > 1 and elapsed > 0:
        remaining = (elapsed / idx) * (total - idx)
        h, rem = divmod(int(remaining), 3600)
        m, s = divmod(rem, 60)
        eta = f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"
    else:
        eta = "--:--"
    
    # Vergangene Zeit
    eh, erem = divmod(int(elapsed), 3600)
    em, es = divmod(erem, 60)
    elapsed_str = f"{eh}:{em:02d}:{es:02d}" if eh else f"{em}:{es:02d}"
    
    # Kompakter Fortschrittsbalken
    bar_width = 20
    progress = idx / total
    filled = int(bar_width * progress)
    bar = "━" * filled + "╺" + "─" * max(0, bar_width - filled - 1)
    
    # Kompakte Zeile, aufgeräumt mit Leerzeichen-Padding
    line = (f"  [{idx:>{len(str(total))}}/{total}] {bar} {progress*100:5.1f}%"
            f" │ {elapsed_str} │ ETA {eta}"
            f" │ {throughput:.1f} ch/s │ Σ {total_chunks}")
    
    # Terminal-Zeile komplett überschreiben (120 Zeichen breit)
    print(f"\r{line:<120}", end="", flush=True)


# =============================================================================
# Main
# =============================================================================

def main():
    # Config laden falls vorhanden
    config_path = SCRIPT_DIR / "config.json"
    default_device = "mps" if sys.platform == "darwin" else "cpu"
    default_batch = 4
    loaded_from = []
    
    try:
        if RUNTIME_CONFIG_PATH.exists():
            with open(RUNTIME_CONFIG_PATH, encoding="utf-8") as f:
                cfg = json.load(f)
            oracle_cfg = cfg.get("oracle", {})
            if "device" in oracle_cfg:
                default_device = oracle_cfg["device"]
            if "batch_size" in oracle_cfg:
                default_batch = oracle_cfg["batch_size"]
            loaded_from.append(str(RUNTIME_CONFIG_PATH.relative_to(REPO_ROOT)))
    except Exception as e:
        print(f"⚠️  Runtime-Config {RUNTIME_CONFIG_PATH} nicht lesbar oder fehlerhaft: {e}")

    try:
        if config_path.exists():
            with open(config_path, encoding="utf-8") as f:
                cfg = json.load(f)
                if "device" in cfg: default_device = cfg["device"]
                if "batch_size" in cfg: default_batch = cfg["batch_size"]
            loaded_from.append(str(config_path.relative_to(REPO_ROOT)))
    except Exception as e:
        print(f"⚠️  Config-Pfad {config_path} nicht lesbar oder fehlerhaft (Permission oder Format): {e}")

    if loaded_from:
        print(
            f"📋 Config geladen: {default_device.upper()} (Batch: {default_batch}) "
            f"aus {', '.join(loaded_from)}"
        )

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
    parser.add_argument("--file", type=str,
                        help="Nur diese spezifische Datei aktualisieren (für Watcher)")
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
        rag_progress = collect_rag_progress(client)
        for source_key in ("quellen", "wiki"):
            p = rag_progress[source_key]
            coll_name = p["collection"]
            if p["available"]:
                print(
                    f"     {coll_name}: {p['chunks']} Chunks | "
                    f"{p['indexed_files']}/{p['indexable_files']} Dateien "
                    f"({p['coverage_pct']:.2f}% Coverage)"
                )
                if p["stale_index_entries"] > 0:
                    print(
                        f"       ⚠️  Stale Index-Eintraege: {p['stale_index_entries']} "
                        "(Dateien nicht mehr im Dateisystem)"
                    )
            elif "does not exist" in p["error"]:
                print(f"     {coll_name}: ❌ Nicht vorhanden")
            else:
                print(f"     {coll_name}: ❌ Fehler beim Lesen: {p['error']}")

        payload, md_path, json_path = build_archive_register(rag_progress)
        dispatch = payload["stats"]["board_metrics"]["dispatch"]
        print("\n  🧾 Archivregister erstellt:")
        print(f"     Markdown: {md_path.relative_to(REPO_ROOT)}")
        print(f"     JSON:     {json_path.relative_to(REPO_ROOT)}")
        print(
            "  📮 Dispatch: "
            f"OPEN={dispatch['status_counts'].get('OPEN', 0)} | "
            f"CLAIMED={dispatch['status_counts'].get('CLAIMED', 0)} | "
            f"DONE={dispatch['status_counts'].get('DONE', 0)} | "
            f"Missing UUID={dispatch['missing_uuid']}"
        )
        sys.exit(0)
    
    # Modell laden
    print("\n  🧠 Lade Embedding-Modell...")
    from sentence_transformers import SentenceTransformer
    
    # Device-Logik: --cpu Flag sticht Config
    if args.cpu:
        device = "cpu"
    else:
        device = default_device
        
    offline_mode = is_offline_runtime()
    device = resolve_device(device)
    print(f"  🔌 Device: {device.upper()} (Batch-Size: {args.batch_size})")

    model = SentenceTransformer(
        EMBEDDING_MODEL,
        trust_remote_code=True,
        device=device,
        local_files_only=offline_mode,
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
            args.batch_size, # Pass batch_size from args/config
            args.rebuild,
            args.file
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
