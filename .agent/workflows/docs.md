---
layout: wiki_page
description: Dokumentation, Verwendungsprüfung und Git-Synchronisation (/docs)
---

Dieser Workflow sichert Dokumentationsqualitaet, Interop-Konsistenz und GitHub-Pages-Bereitstellung.

## Interop-Status
- runtime_commands:
  - `7w_wiki.py check`
  - `7w_wiki.py stats`
  - `7w_wiki.py audit`
  - `7w_wiki.py test --suite interop-doc-links`
  - `7w_wiki.py test --suite reader-stats-contract`
  - `7w_wiki.py pages status`
  - `7w_wiki.py pages build [--strict]`
  - `7w_wiki.py pages validate [--strict]`
  - `7w_wiki.py archive sync`
- method_only:
  - `/docs`

### 1. Dokumentations-Check
1. Pruefe `docs/` auf absolute Pfade (alles muss relativ sein!).
- [README.md](../../README.md)
- [docs/index.md](../../docs/index.md)
- [docs/Siebenwind_Wiki/index.md](../../docs/Siebenwind_Wiki/index.md)
- [docs/Agenten/index.md](../../docs/Agenten/index.md)
- [AGENTS.md](../../AGENTS.md)
- [GEMINI.md](../../GEMINI.md)
- [COORDINATION_HUB.md](../../System/COORDINATION_HUB.md) (**Zentrale Registrierungspflicht!**)
- [WORKFLOW_LORE_CONSISTENCY.md](../../System/WORKFLOW_LORE_CONSISTENCY.md)
- [SYNAPSEN_SYSTEM_SPEC.md](../../.agent/docs/SYNAPSEN_SYSTEM_SPEC.md)
- [SY_INTEROP.md](../../System/Synapse_Board/SY_INTEROP.md)
- [SY_WORKFLOW_CLI_MATRIX.md](../../System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md)
- [SY_DISPATCH.md](../../System/Synapse_Board/SY_DISPATCH.md)
- **Board Check:** Sind Tickets auf [Synapse_Board](../../System/Synapse_Board/) sowie [SY_REVIEW](../../System/Synapse_Board/SY_REVIEW.md) und [SY_STANDARDS](../../System/Synapse_Board/SY_STANDARDS.md) korrekt gepflegt?
- **Lore Trust Audit:** Stichprobe der `lore_trust` Scores gemaess [CORE_LORE_SCORE_GUIDE.md](../../System/Synapse_Board/CORE_LORE_SCORE_GUIDE.md).
- [wiki_style_guide.md](../../.agent/workflows/wiki_style_guide.md)

### 2. CLI- und Interop-Paritaet
Stelle sicher, dass Dokumentation und Runtime deckungsgleich sind:
- Vergleiche Kommandolisten in `AGENTS.md`, `README.md` und `SY_WORKFLOW_CLI_MATRIX.md` mit `./7w_wiki.py --help`.
- Pruefe kritische Optionen explizit:
  - `./7w_wiki.py search "<query>" --source wiki|quellen|all`
  - `./7w_wiki.py index --status` / `--rebuild`
  - `./7w_wiki.py inquisition --audit-only`
  - `./7w_wiki.py sanitize --auto`
  - `./7w_wiki.py archive sync`
- Wenn neue Systemdokumente entstanden sind: in `System/COORDINATION_HUB.md` registrieren.

### 3. Verwendungspruefung (Docs + Pages)
Fuehre den minimalen Qualitaetslauf aus:
```bash
./7w_wiki.py check
./7w_wiki.py stats
./7w_wiki.py test --suite reader-stats-contract
./7w_wiki.py pages validate
./7w_wiki.py archive sync
```
Pruefe danach, ob relevante Aenderungen in `docs/` und den verlinkten Quellseiten sichtbar sind.
Pruefe insbesondere, ob `Siebenwind_Wiki/10_Archiv/Wiki_Statistiken.md` die Reader-Sektionen und `Logs/Archive/STATS_SNAPSHOT_latest.json` als Maschinenoberflaeche aktuell sind.

Optional fuer harte Release-Pruefung:
```bash
./7w_wiki.py pages build --strict
```

Zielbild:
- Endnutzer-Pages (`docs/Siebenwind_Wiki/`) bleiben leserorientiert.
- Agenten- und Betriebsdoku bleibt in `docs/Agenten/` gebuendelt.
- Keine externen Blob-Spruenge aus den zentralen Agenten-Pages.

### 4. Git-Synchronisation
Sichere den aktuellen Stand:
1.  **Status prüfen:** `git status`
2.  **Dateien hinzufügen:** `git add .`
3.  **Commit erzeugen:** 
    ```bash
    git commit -m "Docs & Maintenance: System-Audit durchgeführt und Dokumentation aktualisiert."
    ```
4.  **Push:** 
    ```bash
    git push
    ```

**Die Dokumentation muss jederzeit den realen CLI- und Workflow-Stand widerspiegeln.**
