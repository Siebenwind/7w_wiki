#!/usr/bin/env python3
# =============================================================================
# Das Orakel – Hardware Benchmark & Auto-Tuner
# Testet systematisch CPU vs. MPS und verschiedene Batch-Größen.
# =============================================================================
import time
import torch
import sys
from sentence_transformers import SentenceTransformer

MODEL_NAME = "jinaai/jina-embeddings-v3"
LONG_TEXT = "Dies ist ein Test " * 500  # ~2500 Zeichen (entspricht Chunk-Größe)

def run_benchmark(device, batch_size):
    print(f"   ⚙️  Teste {device.upper()} (Batch-Size: {batch_size})...", end="", flush=True)
    
    try:
        # Modell laden (jedes Mal neu, um Memory Leaks zu isolieren)
        model = SentenceTransformer(MODEL_NAME, trust_remote_code=True, device=device)
        
        # Daten vorbereiten
        texts = [LONG_TEXT] * batch_size
        
        # Warmup
        model.encode(texts[:1], task="retrieval.passage")
        
        # Messung
        start = time.time()
        model.encode(texts, task="retrieval.passage", batch_size=batch_size, show_progress_bar=False)
        duration = time.time() - start
        
        speed = batch_size / duration
        print(f" ✅ {speed:.2f} Items/s ({duration:.2f}s total)")
        return speed
        
    except RuntimeError as e:
        if "out of memory" in str(e).lower() or "mps backend" in str(e).lower():
             print(f" ❌ OOM (Zu wenig RAM)")
        else:
             print(f" ❌ Fehler: {e}")
        return 0
    except Exception as e:
        print(f" ❌ Fehler: {e}")
        return 0

def main():
    print("╔═══════════════════════════════════════════════════╗")
    print("║   Das Orakel – Hardware Benchmark                 ║")
    print("╚═══════════════════════════════════════════════════╝")
    print(f"  Test-Text: {len(LONG_TEXT)} Zeichen")
    
    results = []
    
    # 1. CPU Tests (immer sicher) -> Batch 1, 4
    print("\n🔍 CPU Benchmarks (Referenz):")
    results.append(("cpu", 1, run_benchmark("cpu", 1)))
    results.append(("cpu", 4, run_benchmark("cpu", 4)))
    
    # 2. MPS Tests (Metal) -> Batch 1, 4, 8
    if torch.backends.mps.is_available():
        print("\n🔍 MPS Benchmarks (Apple Silicon):")
        # Starte klein
        results.append(("mps", 1, run_benchmark("mps", 1)))
        results.append(("mps", 2, run_benchmark("mps", 2)))
        results.append(("mps", 4, run_benchmark("mps", 4)))
    else:
        print("\n⚠️  Kein MPS verfügbar.")

    # Gewinner ermitteln
    print("\n═══════════════════════════════════════════════════")
    if not results:
        print("❌ Keine Benchmarks erfolgreich.")
        return

    # Sortiere nach Geschwindigkeit (Items/s), absteigend
    best_config = max(results, key=lambda x: x[2] if x[2] > 0 else -1)
    device, batch, speed = best_config
    
    if speed <= 0:
        print("❌ Alle Tests fehlgeschlagen.")
        return

    print(f"🏆 GEWINNER: {device.upper()} mit Batch-Size {batch}")
    print(f"   Geschwindigkeit: ~{speed:.2f} Chunks/Sekunde")
    
    # Config schreiben
    import json
    from pathlib import Path
    
    config_path = Path(__file__).parent / "config.json"
    config = {
        "device": device,
        "batch_size": batch,
        "model_name": MODEL_NAME
    }
    
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
        
    print(f"✅ Konfiguration gespeichert in: {config_path}")
    print(f"   Du kannst jetzt einfach 'build_index.py' starten.")

if __name__ == "__main__":
    main()
