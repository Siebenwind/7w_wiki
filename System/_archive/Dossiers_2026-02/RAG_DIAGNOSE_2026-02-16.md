# RAG Diagnosebericht (2026-02-16)

## Kontext
- Anlass: wiederholte Oracle-`search`-Fehler in Sandbox-Laufzeit.
- Scope: Ursachenanalyse, Interop-sicherer Fix, Benchmark, Systemstatus.

## Beobachtete Fehlerbilder
1. Netzwerkfehler beim Laden von Modell-Metadaten:
   - `NameResolutionError` auf `huggingface.co` (`modules.json`, `config_sentence_transformers.json`, `README.md`).
2. Device-Fehler bei Modellinitialisierung:
   - `RuntimeError: The MPS backend is supported on MacOS 14.0+`.

## Reproduzierte Laufzeit-Umgebung
- `CODEX_SANDBOX=seatbelt`
- `CODEX_SANDBOX_NETWORK_DISABLED=1`
- Oracle-Venv vorhanden: `.agent/skills/oracle/venv/bin/python3`
- Torch-MPS-Check in dieser Laufzeit:
  - `torch.backends.mps.is_built() = True`
  - `torch.backends.mps.is_available() = False`

## Root Cause
1. **Offline-Erkennung nicht interop-robust genug**
   - Oracle-Code prüfte nur auf `ANTIGRAVITY_*`-Variablen.
   - In dieser Laufzeit waren stattdessen `CODEX_SANDBOX*` gesetzt.
   - Folge: `local_files_only=False` trotz Netzsperre, dadurch wiederholte HuggingFace-HEAD-Requests.
2. **Kein Standard-Device-Fallback**
   - Default auf `mps` unter macOS ohne Availability-Guard.
   - Folge: RuntimeError statt sauberem CPU-Fallback.

## Umgesetzte Fixes (interop-konform, additiv)
### 1) Offline/Sandbox-Erkennung erweitert
- Datei: `.agent/skills/oracle/search.py`
- Datei: `.agent/skills/oracle/build_index.py`
- Maßnahmen:
  - Neue Funktion `is_offline_runtime()` mit Checks auf:
    - `ANTIGRAVITY_SANDBOX`, `ANTIGRAVITY_AGENT`
    - `CODEX_SANDBOX`, `CODEX_SANDBOX_NETWORK_DISABLED`
    - `HF_HUB_OFFLINE`, `TRANSFORMERS_OFFLINE`
  - Bei Offline-Runtime:
    - `HF_HUB_OFFLINE=1`
    - `TRANSFORMERS_OFFLINE=1`
  - Modell-Ladepfade nutzen dann `local_files_only=True`.

### 2) Standard-Device-Resolution ergänzt
- Datei: `.agent/skills/oracle/search.py`
- Datei: `.agent/skills/oracle/build_index.py`
- Maßnahmen:
  - Neue Funktion `resolve_device(...)`.
  - `mps` wird nur verwendet, wenn `torch.backends.mps.is_available()`.
  - Sonst automatischer Fallback auf `cpu`.

## Interoperabilitäts-Hinweis
- Antigravity-Kompatibilität wurde **nicht** entfernt.
- Bestehende `ANTIGRAVITY_*`-Checks bleiben erhalten; `CODEX_*` wurde nur ergänzend hinzugefügt.
- Ergebnis: gleiche Standardlogik funktioniert in beiden Runtimes (Antigravity + Codex).

## RAG Systemstatus
Ausgabe von `./7w_wiki.py index --status`:
- Modell: `jinaai/jina-embeddings-v3`
- Chunk-Größe: `2500`
- `siebenwind_quellen`: `60151` Chunks aus `289` Dateien
- `siebenwind_wiki`: `31700` Chunks aus `158` Dateien

## Such-Benchmark (seriell, jeweils 1 Request)
Messmethode:
- `/usr/bin/time -p ./7w_wiki.py search --source all "<query>"`
- plus interne Suchzeit aus Oracle-Ausgabe

Ergebnisse:
1. Query `Sheddja`
   - Oracle Suchzeit: `48.3s`
   - Wall-Clock (`time -p`): `52.35s`
2. Query `Dunvallo Linari`
   - Oracle Suchzeit: `48.1s`
   - Wall-Clock (`time -p`): `52.98s`
3. Query `Astrael`
   - Oracle Suchzeit: `53.6s`
   - Wall-Clock (`time -p`): `59.12s`

## Ergebnis
- Netzwerk-Fehlerklasse behoben (keine HF-Resolver-Retry-Schleife mehr).
- Device-Fehlerklasse behoben (MPS -> CPU-Fallback wenn nicht verfügbar).
- RAG-Status ist konsistent lesbar, Suche läuft wieder durch.

## Benchmark-Run: `rag-relevance-smoke` (seriell, 3 Läufe)
Messmethode:
- `./7w_wiki.py test --suite rag-relevance-smoke`
- Auswertung aus den generierten Reports (Case-Laufzeiten aus dem Runner).

Reports:
1. `Logs/Archive/TEST_rag-relevance-smoke_2026-02-16_230008.md`
2. `Logs/Archive/TEST_rag-relevance-smoke_2026-02-16_230207.md`
3. `Logs/Archive/TEST_rag-relevance-smoke_2026-02-16_230350.md`

Status:
- Alle drei Läufe: `PASS=1 | FAIL=3 | SKIP=0`
- Relevanz-Checks schlagen stabil fehl (Dunvallo/Matrixtheorie/Reagenzien).

Laufzeit-Statistik (3 Läufe):
- Suite-Summe: `109.13s`, `101.73s`, `97.86s` -> Mittel `102.91s`
- Suite-Mittel pro Case: `27.28s`, `25.43s`, `24.47s` -> Mittel `25.73s`

Case-Mittelwerte:
- `rag-status`: `10.82s`
- `rag-q-dunvallo`: `32.58s`
- `rag-q-matrix`: `29.52s`
- `rag-q-reagenzien`: `29.98s`

Interpretation:
- Performance ist reproduzierbar (ca. 98-109s pro Lauf).
- Relevanz ist aktuell nicht ausreichend stabil fuer die gesetzten Zieltreffer in `--source wiki`.
