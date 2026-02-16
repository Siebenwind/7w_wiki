---
layout: wiki_page
description: System-Audit & Update von Skills, Agents und Workflows (/update)
---

Dieser Workflow dient der regelmäßigen Wartung und Sicherstellung, dass alle Systemkomponenten (Automatisierung, Instruktionen, Workflows) den aktuellen Projektanforderungen entsprechen.

## Interop-Status
- runtime_commands:
  - `7w_wiki.py audit`
  - `7w_wiki.py sanitize --auto`
  - `7w_wiki.py index --status`
- method_only:
  - `/update`

### 1. Skill-Audit & Cleanup
Prüfe die Skill- und Datenintegrität über den zentralen CLI-Einstieg:
- **Integrität:** Führe Audit, Sanitizer und Index-Status aus:
    ```bash
    ./7w_wiki.py audit
    ./7w_wiki.py sanitize --auto
    ./7w_wiki.py index --status
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
