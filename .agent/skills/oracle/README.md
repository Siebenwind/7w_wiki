# Das Orakel – Benutzerhandbuch & Referenz

**Status:** Aktiv & Integriert (v1.0)
**Technologie:** `jina-embeddings-v3` (8k Context) + `ChromaDB` + `BGE Re-Ranker`

Das Orakel ist das semantische Suchsystem des Wikis. Es ermöglicht Agenten und Nutzern, Wissen nicht nur per Keyword, sondern per Bedeutung (Semantik) zu finden.

## 🚀 Schnellstart (TL;DR)

**Suche:**
```bash
.agent/skills/oracle/venv/bin/python3 .agent/skills/oracle/search.py "Frage"
```

**Index-Update:**
```bash
.agent/skills/oracle/venv/bin/python3 .agent/skills/oracle/build_index.py
```

**Installation:**
```bash
bash .agent/skills/oracle/setup.sh
```

---

## 📚 Befehlsreferenz (Command Cheat Sheet)

Alle Befehle werden aus dem **Root-Verzeichnis** ausgeführt.

### A. Suche (Wissen abfragen)
| Befehl | Funktion |
|--------|----------|
| `.../search.py "Frage"` | **Standard:** Sucht präzise im **Wiki** (Level 1). |
| `.../search.py "..." --source quellen` | **Tiefensuche:** Sucht in den **Rohdaten/Quellen** (Level 2). |
| `.../search.py "..." --source all` | **Alles:** Sucht in Wiki UND Quellen. |
| `.../search.py "..." --no-rerank` | **Schnell:** Ohne Re-Ranking (für grobe Scans). |
| `.../search.py "..." --top 20` | **Umfangreich:** Zeigt mehr Treffer. |

*(Pfad-Abkürzung: `.agent/skills/oracle/venv/bin/python3 .agent/skills/oracle/search.py ...`)*

### B. Indexierung (Wissen aufbauen)
Der Index wird **inkrementell** gebaut. Das System erkennt Änderungen (via Content-Hash) und Renames automatisch.

| Befehl | Funktion |
|--------|----------|
| `.../build_index.py` | **Standard:** Aktualisiert den Index (nur Neues/Geändertes). |
| `.../build_index.py --status` | **Check:** Zeigt Anzahl der Chunks im Index (ohne Änderungen). |
| `.../build_index.py --rebuild` | **Reset:** Löscht alles und baut den Index komplett neu auf. |
| `.../build_index.py --cpu` | **Safe Mode:** Erzwingt CPU-Nutzung (falls MPS instabil ist). |

*(Pfad-Abkürzung: `.agent/skills/oracle/venv/bin/python3 .agent/skills/oracle/build_index.py ...`)*

### C. System-Wartung & Tuning
| Befehl | Funktion |
|--------|----------|
| `.../benchmark_hardware.py` | **Tuning:** Misst Hardware-Speed und setzt optimale Batch-Size in `config.json`. |
| `bash .agent/skills/oracle/setup.sh` | **Install:** Richtet die Umgebung initial ein. |

### D. Konfiguration
- Zentrale Defaults: `.agent/config/runtime.json` (`oracle.device`, `oracle.batch_size`)
- Legacy/Kompatibilitaet: `.agent/skills/oracle/config.json`
- Prioritaet: CLI-Flags > lokale Oracle-Config > zentrale Runtime-Config

---

## 🏗️ Architektur & Funktionsweise

### 1. Komponenten
- **Embedding Model:** `jina-embeddings-v3`
    - *Warum?* Unterstützt 8192 Token Kontext (narrative Texte) und ist für Retrieval Tasks optimiert (LoRA-Adapter).
- **Vektor-Datenbank:** `ChromaDB` (Lokal)
    - Speichert Chunks und Embeddings persistent in `.agent/data/chroma_db/`.
- **Re-Ranker:** `BAAI/bge-reranker-v2-m3`
    - Filtert die Top-20 Vektor-Ergebnisse nochmal semantisch, um die absolute Relevanz zu erhöhen.

### 2. Daten-Pipeline
1.  **Scanning:** `build_index.py` scannt `/Siebenwind_Wiki` und `/Quellen`.
2.  **Hashing:** Erstellt SHA-256 Hashes des Text-Contents (ohne Frontmatter).
3.  **Diff:** Vergleicht mit DB-Status.
    - *Match:* Datei überspringen.
    - *Rename:* Nur Pfad in DB updaten.
    - *Change:* Alte Chunks löschen, neu embedden.
4.  **Chunking:** Text wird in 2500-Zeichen-Blöcke (mit 300 Zeichen Overlap) geteilt.
5.  **Embedding:** Berechnung auf GPU (MPS) oder CPU.
6.  **Storage:** Speichern in ChromaDB.

### 3. Wahrheitshierarchie
Das Orakel respektiert die strengen Regeln der Wissenshierarchie:
1.  **Wiki:** Kuratiertes Wissen (Priorität 1).
2.  **Quellen:** Rohdaten (Priorität 2, kann veraltet sein).

---

## 🛠️ Fehlerbehebung

- **MPS Out-of-Memory:**
    - Führe `benchmark_hardware.py` aus, um die Batch-Size zu reduzieren.
    - Oder nutze `--cpu`.
- **Index korrupt/leer:**
    - Nutze `--rebuild` für einen sauberen Neustart.
- **Permission Errors:**
    - Das System läuft in einer Sandbox. Zugriff auf System-Ordner ist blockiert. Dies ist normal und wird abgefangen.
