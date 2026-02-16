---
description: Department Master Workflow für die Ingestion (Quellen -> Wiki)
---

# Department: 🏛️ Lore-Archiv (INGEST)

Dieses Department ist für die Transformation von rohem Wissen in strukturierte Wiki-Artefakte verantwortlich. Es fusioniert die Workflows `/ingestion_protocol`, `/batch`, `/wiki_process` und `/rvw_loop`.

## Interop-Status
- runtime_commands:
  - `7w_wiki.py advisor`
  - `7w_wiki.py search <query> --source wiki`
  - `7w_wiki.py search <query> --source quellen`
  - `7w_wiki.py search <query> --source all`
- method_only:
  - `/ingest_master`
  - `/ingestion_protocol`
  - `/batch`
  - `/wiki_process`
  - `/rvw_loop`

## 1. Sichtung (Screening)
- [ ] **Inventur-Check**: Öffne `Logs/INVENTUR_QUELLEN.md` und wähle eine `Pending` Quelle.
- [ ] **Epistemische Klassifizierung**: Bestimme den Status (#canon, #bote, #überlieferung, #perspektive).

## 2. Durchführung (Standard-Loops)
Dieses Department koordiniert die technische Umsetzung mittels spezialisierter Sub-Workflows.

### A. Extraktion & Produktion
Nutze den [rvw_loop.md](../../.agent/workflows/rvw_loop.md) (Standard-Prozess) für:
- **Orakel-Disziplin:** Bei Unklarheiten immer alle drei Modi prüfen (`wiki`, `quellen`, `all`).
- **Zwei-Pass-Verfahren**: Pflicht bei Texten > 100 Zeilen.
- **Entity Manifest**: Vollständige Erfassung aller Entitäten.
- **Verifizierung**: Abgleich gegen Lokal-Kanon und Orakel.

### B. Ingestion-Checkliste
Nutze das [ingestion_protocol.md](../../.agent/workflows/ingestion_protocol.md) zur inhaltlichen Vollständigkeitsprüfung (Gilden, Bestiarium, Gerüchteküche).

## 3. Synchronisation & Abschluss
- [ ] **Register-Updates**: Synchronisation mit `Personenregister.md` etc.
- [ ] **Archiv-Sync**: `./7w_wiki.py archive sync` ausführen.
- [ ] **Logging**: Eintrag in `Logs/INGESTION_LOG.md`.

#ingestion #produktion #master
