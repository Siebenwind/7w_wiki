---
layout: wiki_page
description: Dokumentation, Verwendungsprüfung und Git-Synchronisation (/docs)
---

Dieser Workflow dient der Dokumentation der Anwendung sowie der Sicherung des Projektfortschritts mittels Git.

### 1. Dokumentations-Check
Überprüfe die zentralen Dokumentationsdateien auf Richtigkeit und Vollständigkeit:
- [README.md](README.md)
- [COORDINATION_HUB.md](System/COORDINATION_HUB.md) (**Zentrale Registrierungspflicht!**)
- [WORKFLOW_LORE_CONSISTENCY.md](WORKFLOW_LORE_CONSISTENCY.md)
- [SYNAPSEN_SYSTEM_SPEC.md](.agent/docs/SYNAPSEN_SYSTEM_SPEC.md)
- **Board Check:** Sind alle Tickets auf dem [Synapse-Board](System/Synapse_Board/) sowie den neuen Koordinations-Boards ([SY_REVIEW](System/Synapse_Board/SY_REVIEW.md), [SY_STANDARDS](System/Synapse_Board/SY_STANDARDS.md)) im korrekten Status?
- **Lore Trust Audit:** Stichprobenartige Prüfung der `lore_trust` Scores im Wiki auf Plausibilität gemäß [Score Guide](System/Synapse_Board/CORE_LORE_SCORE_GUIDE.md).
- [wiki_style_guide.md](.agent/workflows/wiki_style_guide.md)

### 2. Implementierungsverzeichnis
Dokumentiere neue Funktionen oder Änderungen an der Struktur:
- Wurden neue Skripte hinzugefügt? (Dokumentiere Zweck und Aufruf)
- Wurden Kategorien im Wiki ergänzt?

### 3. Verwendungsprüfung
Stelle sicher, dass die Anwendung (das Wiki und die Tools) wie vorgesehen genutzt wird:
- Ist die Trennung von `#canon`, `#bote` und `#perspektive` in neuen Artikeln korrekt umgesetzt?
- Wurden bi-direktionale Links via `wiki_link_weaver.py` gesetzt?

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

**Die Dokumentation sollte immer den "Live"-Zustand der Anwendung widerspiegeln.**
