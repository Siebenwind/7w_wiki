#!/usr/bin/env bash
# =============================================================================
# Das Orakel – Setup-Skript
# Erstellt ein isoliertes Python-venv und installiert alle Abhängigkeiten.
# Modelle werden persistent unter .agent/data/models/ gecacht.
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
MODEL_CACHE="$REPO_ROOT/.agent/data/models"
PYTHON_BIN="/opt/homebrew/bin/python3.12"

echo "╔═══════════════════════════════════════════════════╗"
echo "║   Das Orakel – Setup (Siebenwind RAG System)     ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

# --- 1. Python prüfen ---
if [ ! -x "$PYTHON_BIN" ]; then
    echo "⚠️  Python 3.12 nicht gefunden unter $PYTHON_BIN"
    echo "   Versuche system python3..."
    PYTHON_BIN="$(which python3)"
fi
echo "🐍 Python: $($PYTHON_BIN --version)"

# --- 2. Venv erstellen ---
if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Erstelle Virtual Environment..."
    "$PYTHON_BIN" -m venv "$VENV_DIR"
else
    echo "✅ Venv existiert bereits."
fi

# Aktivieren
source "$VENV_DIR/bin/activate"

# --- 3. Dependencies installieren ---
echo "📥 Installiere Abhängigkeiten..."
pip install --upgrade pip --quiet
pip install --quiet \
    chromadb \
    sentence-transformers \
    torch \
    "FlagEmbedding>=1.2" \
    einops \
    tqdm

# --- 4. Modell-Cache vorbereiten ---
mkdir -p "$MODEL_CACHE"
export SENTENCE_TRANSFORMERS_HOME="$MODEL_CACHE"
export HF_HOME="$MODEL_CACHE/huggingface"

# --- 5. Modelle vorladen ---
echo ""
echo "🧠 Lade Embedding-Modell: jinaai/jina-embeddings-v3 (~1.1 GB)..."
python3 -c "
import os
os.environ['SENTENCE_TRANSFORMERS_HOME'] = '$MODEL_CACHE'
os.environ['HF_HOME'] = '$MODEL_CACHE/huggingface'
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('jinaai/jina-embeddings-v3', trust_remote_code=True, device='mps')
print('✅ Embedding-Modell geladen.')
# Schnelltest
vec = model.encode(['Testtext auf Deutsch'], task='retrieval.passage')
print(f'   Vektor-Dimension: {len(vec[0])}')
"

echo ""
echo "🔍 Lade Re-Ranker: BAAI/bge-reranker-v2-m3 (~2.3 GB)..."
python3 -c "
import os
os.environ['HF_HOME'] = '$MODEL_CACHE/huggingface'
from FlagEmbedding import FlagReranker
reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True, device='mps')
print('✅ Re-Ranker geladen.')
# Schnelltest
score = reranker.compute_score(['Wer ist Tiamat?', 'Tiamat ist die Göttin des Lebens.'])
print(f'   Test-Score: {score:.4f}')
"

echo ""
echo "╔═══════════════════════════════════════════════════╗"
echo "║   ✅ Setup abgeschlossen!                        ║"
echo "║                                                   ║"
echo "║   Nächste Schritte:                               ║"
echo "║   1. Index aufbauen:                              ║"
echo "║      $VENV_DIR/bin/python3 \\                      ║"
echo "║        $SCRIPT_DIR/build_index.py                 ║"
echo "║   2. Testsuche:                                   ║"
echo "║      $VENV_DIR/bin/python3 \\                      ║"
echo "║        $SCRIPT_DIR/search.py \"Wer ist Tiamat?\"   ║"
echo "╚═══════════════════════════════════════════════════╝"
