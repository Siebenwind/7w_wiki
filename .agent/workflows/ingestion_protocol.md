---
description: Universelles Ingestion-Protokoll für alle Quellentypen (Boten, Spielergeschichten, Bibliothek, Hintergrund)
---

# Universelles Ingestion-Protokoll

## Interop-Status
- runtime_commands:
  - `7w_wiki.py archive sync`
  - `7w_wiki.py sanitize --auto`
  - `7w_wiki.py score <file>`
- method_only:
  - `/ingestion_protocol`

Dieses Protokoll standardisiert die Erfassung **aller** Quellentypen und stellt sicher, dass keine Entitäten übersehen werden.

## Quellentyp bestimmen

> Siehe [Wiki Style Guide §3.1 (Epistemisches System)](../../.agent/workflows/wiki_style_guide.md) für Entscheidungsregeln bei Widersprüchen.

| Ordner | Quellentyp | Epistemik | Verlässlichkeit |
|---|---|---|---|
| `/Quellen/Hintergrund/` | Hintergrund | #canon | 🥇 Absolut |
| `/Quellen/Zeitung 7w Bote/` | Periodika | #bote | 🥈 Hoch |
| `/Quellen/Bibliothek/` | Bibliothek | #überlieferung | 🥉 Mittel |
| `/Quellen/Spielergeschichten/` | Spielergeschichte | #perspektive | Gering |
| `/Quellen/Forum/` | Forum | #perspektive | Gering |
| `/Quellen/News/` | News | #news | OOC |

## 2. Der Prozess (Technische Standards)
Die technische Durchführung der Ingestion folgt strikt dem **Read-Verify-Write Loop**.

> [!TIP]
> Siehe [rvw_loop.md](../../.agent/workflows/rvw_loop.md) für detaillierte Instruktionen zum Zwei-Pass-Verfahren und zur Wiki-Produktion.

## 3. Entitäts-Schema (Was muss erfasst werden?)
Stelle bei jeder Quelle sicher, dass folgende Dimensionen geprüft werden:

### A. Personen & Organisationen
- [ ] **Haupt- & Nebenakteure**: Namentliche Erwähnung inkl. Titel/Amt.
- [ ] **Gruppierungen**: Gilden, Orden, militärische Einheiten, Kulte.

### B. Geografie & Bestiarium
- [ ] **Orte**: Städte, Gebäude, Landmarken, Distanzen.
- [ ] **Kreaturen**: Flora & Fauna basierend auf Beschreibungen oder Namen.

### C. Lore & Atmosphäre (Roman-Qualität)
- [ ] **Gerüchte**: Als Listenpunkte für das Personenprofil erfassen.
- [ ] **Motivationen**: Warum handeln die Akteure so? (Basierend auf Kontext).

## 4. Output & Synchronisation

1.  **Ingestion Report**: Basierend auf `System/Templates/INGESTION_REPORT_TEMPLATE.md`. Speichern unter `Logs/Ingestion/`.
2.  **Wiki-Produktion**: Standard-Format gemäß [Wiki Style Guide](../../.agent/workflows/wiki_style_guide.md).
3.  **Archiv-Sync**: Stets `./7w_wiki.py archive sync` ausführen.
4.  **Register-Update**: `Personenregister.md`, `Organisationsregister.md`, `Bestiarium_Register.md`.

#ingestion #protokoll #qualität
