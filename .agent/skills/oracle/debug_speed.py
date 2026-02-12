import time
import torch
from sentence_transformers import SentenceTransformer

MODEL_NAME = "jinaai/jina-embeddings-v3"

def benchmark(device, batch_size=32):
    print(f"\n🧪 Benchmarking {device.upper()} with batch_size={batch_size}...")
    try:
        model = SentenceTransformer(MODEL_NAME, trust_remote_code=True, device=device)
    except Exception as e:
        print(f"❌ Could not load on {device}: {e}")
        return

    long_text = "Dies ist ein Test " * 500  # ~2500 Zeichen
    texts = [long_text] * batch_size
    
    # Warmup
    print("   Aufwärmen...")
    model.encode(texts[:2], task="retrieval.passage")
    
    # Run
    print("   Starte Messung...")
    start = time.time()
    model.encode(texts, task="retrieval.passage", batch_size=batch_size, show_progress_bar=False)
    end = time.time()
    
    duration = end - start
    per_item = duration / batch_size
    print(f"   ✅ Dauer: {duration:.2f}s ({per_item*1000:.1f}ms/Item)")
    
if __name__ == "__main__":
    print(f"Torch Version: {torch.__version__}")
    if torch.backends.mps.is_available():
        print("MPS (Metal) is available.")
        benchmark("mps", batch_size=1)
        benchmark("mps", batch_size=32)
    else:
        print("MPS not available.")
        
    benchmark("cpu", batch_size=1)
    benchmark("cpu", batch_size=32)
