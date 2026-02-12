# Projektdossier: Das Orakel (RAG-System)

**Stand:** 12.02.2026
**Version:** 1.0 (Live & Optimized)
**Architekt:** Antigravity

---

## 1. Zielsetzung
Implementierung einer lokalen, semantischen Suche für das Siebenwind-Wiki, die "verstecktes Wissen" (Implikationen, Stimmungen, Zusammenhänge) findet, das über reine Keyword-Suche nicht erreichbar ist.

## 2. Technische Architektur

### A. Die Modelle
Wir haben uns bewusst gegen Standard-Modelle (wie `all-MiniLM-L6-v2`) entschieden und für High-End-Modelle, um die Komplexität der Fantasy-Lore zu erfassen.

| Komponente | Modell | Begründung |
|------------|--------|------------|
| **Embedding** | `jinaai/jina-embeddings-v3` | **8192 Token Kontext.** Entscheidend für unsere langen Lore-Texte (> Standard 512 Token). Unterstützt LoRA-Adapter für spezifische Tasks (Query vs. Passage). |
| **Re-Ranking** | `BAAI/bge-reranker-v2-m3` | Cross-Encoder, der die Top-20 Ergebnisse nochmal tiefenprüft. Erhöht die Präzision bei subtilen Fragen massiv. |
| **Datenbank** | `ChromaDB` (Lokal) | Einfach, persistent, keine Server-Infrastruktur nötig. |

### B. Indexierungs-Strategie
- **Chunk-Größe:** 2500 Zeichen (~350-400 Wörter).
- **Overlap:** 300 Zeichen.
- **Logik:** Wir nutzen einen "Semantic Splitter" (Paragraph -> Satz), um logische Einheiten nicht zu zerreißen.
- **Metadaten:** Jedes Dokument wird automatisch getaggt (Kategorie, Entities aus Wikilinks), was Filterung erlaubt.

## 3. Critical Learnings & Hardware-Optimierung (Mac Silicon)

Das größte Learning dieses Projekts war das Verhalten von **Large Context Models auf Apple Silicon (MPS)**.

### Das Problem: MPS Memory Swapping
`jina-embeddings-v3` nutzt eine angepasste **Flash Attention** Implementierung (`xlm-roberta-flash-implementation`).
- Auf NVIDIA-Karten skaliert dies exzellent.
- Auf **Apple Metal (MPS)** führt dies bei langen Sequenzen (2500 chars) und Standard-Batch-Größen (32) zu einem **Memory Explosion**.
- **Symptom:** Der Prozess verlangsamt sich von ~30ms/Item auf ~2300ms/Item (Faktor 75!), weil der Unified Memory überläuft und das System swapped.

### Die Lösung: Aggressive Batch-Verkleinerung
Wir haben ein Auto-Tuning-Skript (`benchmark_hardware.py`) entwickelt, das empirisch die optimale Strategie ermittelt.
- **Ergebnis:** Eine **Batch-Size von 2** (oder maximal 4) ist auf einem M2 mit 16GB RAM der Sweetspot.
- **Performance:** ~0.5 Chunks/Sekunde (MPS) vs ~0.25 Chunks/Sekunde (CPU). MPS ist also immer noch **doppelt so schnell**, wenn man es nicht überlädt.

### Empfehlung für die Zukunft
Fall die Hardware wechselt oder das Modell aktualisiert wird, **immer zuerst `benchmark_hardware.py` ausführen**. Vertraue keinen Standard-Werten aus dem Internet, da "Flash Attention auf MPS" ein sich schnell änderndes Feld ist.

## 4. Dateien & Workflow
Die Intelligenz liegt in `.agent/skills/oracle/`:
- `setup.sh`: Installiert die Umgebung (User-Side, wegen Sandbox-Limitierungen).
- `config.json`: Enthält die vom Benchmark ermittelten Hardware-Parameter.
- `build_index.py` & `search.py`: Lesen diese Config automatisch.

---
*Ende des Dossiers*
