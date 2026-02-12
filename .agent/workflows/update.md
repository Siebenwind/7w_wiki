---
layout: wiki_page
description: System-Audit & Update von Skills, Agents und Workflows (/update)
---

Dieser Workflow dient der regelmäßigen Wartung und Sicherstellung, dass alle Systemkomponenten (Automatisierung, Instruktionen, Workflows) den aktuellen Projektanforderungen entsprechen.

### 1. Skill-Audit & Cleanup
Prüfe die Python-Skripte in `.agent/skills/wiki_schmied/scripts/`:
- **Integrität:** Führe den Guardian und den Sync-Automator aus:
    ```bash
    python3 .agent/skills/wiki_schmied/scripts/wiki_integrity_guardian.py
    python3 .agent/skills/wiki_schmied/scripts/source_sync_automator.py
    ```
- **Logik-Check:** Unterstützen die Skripte die neuesten Standards (z.B. Granulares Tagging für Mixed-Source Artikel)?
- **Pfad-Check:** Sind die Pfade in den Skripten noch aktuell?

### 2. Workflow-Audit
Überprüfe alle Dateien in `.agent/workflows/`:
- **Aktualität:** Entsprechen Anweisungen in `wiki_style_guide.md` oder `wiki_process.md` noch der gelebte Praxis?
- **Redundanz:** Gibt es überlappende oder widersprüchliche Workflows?

### 3. Agent- & Prompt-Audit
Prüfe die Instruktionen des Oberarchivars:
- **Master Prompts:** Sind die Rollendefinitionen in `Oberarchivar - Master Prompt.md` noch präzise?
- **Lore-Konsistenz:** Entspricht `WORKFLOW_LORE_CONSISTENCY.md` dem aktuellen Stand des Kanons?

### 4. Anforderungs-Synchronisation
Gleiche das System mit den Projektzielen ab:
- Werden alle neuen Dokumenttypen (PDF, docx) korrekt verarbeitet?
- Ist die Portabilität des Wikis (keine absoluten Pfade) weiterhin gewährleistet?

**Nach dem Audit: Erstelle einen Bericht über notwendige Anpassungen oder bestätige die Systemintegrität.**
