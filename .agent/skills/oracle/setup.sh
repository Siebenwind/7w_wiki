#!/usr/bin/env bash
# =============================================================================
# Das Orakel – Setup-Skript
# ACHTUNG: Dieses Skript muss AUSSERHALB der Antigravity-Sandbox ausgeführt
# werden, da die Sandbox pip-Installationen und .pyc-Dateien blockiert.
#
# → In einem normalen macOS-Terminal ausführen!
# =============================================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
VENV_DIR="$SCRIPT_DIR/venv"
MODEL_CACHE="$REPO_ROOT/.agent/data/models"

echo "╔═══════════════════════════════════════════════════╗"
echo "║   Das Orakel – Setup (Siebenwind RAG System)     ║"
echo "╚═══════════════════════════════════════════════════╝"
echo ""

# --- 1. Python 3.12 oder 3.13 finden ---
PYTHON_BIN=""
for candidate in /opt/homebrew/bin/python3.13 /opt/homebrew/bin/python3.12 python3; do
    if command -v "$candidate" &>/dev/null; then
        PYTHON_BIN="$candidate"
        break
    fi
done
echo "🐍 Python: $($PYTHON_BIN --version)"

# --- 2. Venv erstellen ---
if [ -d "$VENV_DIR" ] && [ ! -f "$VENV_DIR/bin/activate" ]; then
    echo "⚠️  Venv Verzeichnis existiert, aber scheint defekt zu sein. Lösche..."
    rm -rf "$VENV_DIR"
fi

if [ ! -d "$VENV_DIR" ]; then
    echo "📦 Erstelle Virtual Environment..."
    "$PYTHON_BIN" -m venv "$VENV_DIR"
else
    echo "✅ Venv existiert bereits."
fi

source "$VENV_DIR/bin/activate"
PYTHON="$VENV_DIR/bin/python3"

# --- 3. Dependencies installieren ---
echo "📥 Installiere Abhängigkeiten..."
pip install --upgrade pip --quiet
pip install --quiet \
    chromadb \
    sentence-transformers \
    "transformers==4.45.2" \
    torch \
    "FlagEmbedding>=1.2" \
    einops \
    tqdm \
    watchdog

# --- 4. Modell-Cache vorbereiten ---
mkdir -p "$MODEL_CACHE"
export SENTENCE_TRANSFORMERS_HOME="$MODEL_CACHE"
export HF_HOME="$MODEL_CACHE/huggingface"

# --- 5. Modelle vorladen ---
echo ""
echo "🧠 Lade Embedding-Modell: jinaai/jina-embeddings-v3 (~1.1 GB)..."
"$PYTHON" -c "
import os
os.environ['SENTENCE_TRANSFORMERS_HOME'] = '$MODEL_CACHE'
os.environ['HF_HOME'] = '$MODEL_CACHE/huggingface'
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('jinaai/jina-embeddings-v3', trust_remote_code=True)
print('✅ Embedding-Modell geladen.')
vec = model.encode(['Testtext auf Deutsch'], task='retrieval.passage')
print(f'   Vektor-Dimension: {len(vec[0])}')
"

echo ""
echo "🔍 Lade Re-Ranker: BAAI/bge-reranker-v2-m3 (~2.3 GB)..."
"$PYTHON" -c "
import os
os.environ['HF_HOME'] = '$MODEL_CACHE/huggingface'
from FlagEmbedding import FlagReranker
reranker = FlagReranker('BAAI/bge-reranker-v2-m3', use_fp16=True)
print('✅ Re-Ranker geladen.')
score = reranker.compute_score(['Wer ist Tiamat?', 'Tiamat ist die Göttin des Lebens.'])
if isinstance(score, list):
    score = score[0]
print(f'   Test-Score: {score:.4f}')
"

echo ""
echo "╔═══════════════════════════════════════════════════╗"
echo "║   ✅ Setup abgeschlossen!                        ║"
echo "║                                                   ║"
echo "║   Nächste Schritte (in Antigravity):              ║"
echo "║   Index aufbauen:                                 ║"
echo "║     python3 .agent/skills/oracle/build_index.py   ║"
echo "║   Testsuche:                                      ║"
echo "║     python3 .agent/skills/oracle/search.py \\      ║"
echo "║       \"Wer ist Tiamat?\"                           ║"
echo "╚═══════════════════════════════════════════════════╝"
