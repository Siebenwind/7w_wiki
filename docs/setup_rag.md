# Das Orakel: Setup & Nutzung des RAG Systems

Das "Orakel" ist die semantische Suchmaschine der Siebenwind Lore Engine. Es basiert auf **RAG (Retrieval Augmented Generation)** und ermöglicht es, Fragen an das Wiki zu stellen, statt nur nach Stichworten zu suchen.

## 🛠️ Technologie-Stack
- **Embeddings:** `jinaai/jina-embeddings-v3` (Optimiert für Semantic Search).
- **Reranker:** `BAAI/bge-reranker-v2-m3` (Präzise Nachsortierung der Ergebnisse).
- **Vektor-Store:** Lokal (FAISS oder HNSW via `chromadb` / `lancethree` - *Implementierungsabhängig*).
- **Interface:** CLI (`7w_wiki.py`).

## 🚀 Installation & Setup

### 1. Umgebung vorbereiten
Das Orakel benötigt Python 3.10+ und einige schwergewichtige ML-Bibliotheken. Wir empfehlen die Nutzung des bereitgestellten Virtual Environments.

```bash
# Im Root-Verzeichnis
pip install -r requirements.txt
```

### 2. Index initialisieren
Bevor du suchen kannst, muss das Wissen "gelernt" (indiziert) werden. Dieser Prozess liest alle Markdown-Dateien, chunked sie in Abschnitte und berechnet die Vektoren.

```bash
# Baut den Index komplett neu auf
./7w_wiki.py index --rebuild
```
*Dauer: Je nach Hardware 2-10 Minuten für das gesamte Wiki.*

### 3. Status prüfen
Überprüfe, ob der Index bereit ist:

```bash
./7w_wiki.py index --status
```

---

## 🔮 Nutzung (The Oracle)

Die Suche erfolgt über das Unified CLI Tool `7w_wiki.py`.

### Einfache Frage
Stelle eine Frage in natürlicher Sprache.

```bash
./7w_wiki.py search "Wer gründete den Löwenorden?"
```

### Quellen-Filter
Du kannst die Suche auf bestimmte Bereiche einschränken:

```bash
# Nur im offiziellen Wiki suchen (Höchste Kanon-Treue)
./7w_wiki.py search "Magiegesetze" --source wiki

# Nur in den Quellen suchen (Historische Forschung)
./7w_wiki.py search "Alte Schlachtberichte" --source quellen
```

### Historiker-Modus
Für tiefe Analysen gibt es den Historiker-Modus, der eine breitere Suche durchführt und die Ergebnisse synthetisiert:

```bash
./7w_wiki.py historian "Die Entwicklung der Magie über die Jahrhunderte"
```

---

## ⚠️ Troubleshooting

**Fehler: `No module named 'torch'`**
Stelle sicher, dass du das Virtual Environment aktiviert hast oder die Requirements installiert sind.

**Fehler: `Index not found`**
Führe `./7w_wiki.py index --rebuild` aus.

**Falsche Ergebnisse?**
Die Qualität hängt von der Granularität der Wiki-Artikel ab. Lange, unstrukturierte Texte sind schwerer zu durchsuchen. Nutze den `/audit` Workflow, um die Struktur zu verbessern.
