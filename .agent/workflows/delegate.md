---
description: Delegiere eine Aufgabe an einen externen Agenten (CLI) zur Token-Schonung.
---

Dieser Workflow bereitet alles vor, um eine Aufgabe (z. B. Scouting, Ingestion) an eine externe CLI (Gemini, Codex, Claude) zu übergeben.

## Interop-Status
- runtime_commands:
  - `7w_wiki.py start`
  - `7w_wiki.py audit`
- method_only:
  - `/delegate`

## Schritte

1. **Vorbereitung**:
   Stelle sicher, dass die externe CLI (z. B. `gemini-cli`) im Antigravity-Terminal einsatzbereit ist.

2. **System-Kickoff**:
   Kopiere den Inhalt von [.agent/prompts/EXTERNAL_KICKOFF.md](../../.agent/prompts/EXTERNAL_KICKOFF.md) in die externe CLI, um den Agenten auf das Projekt einzunorden.
   
   > [!NOTE]
   > Ersetze `[TASK_NAME]` im Text durch den Namen deiner Aufgabe.

3. **Task-Spezifizierung**:
   Wähle den passenden Aufgaben-Prompt:
   - **Scouting/News**: Nutze [.agent/prompts/EXTERNAL_SCOUT_TASK.md](../../.agent/prompts/EXTERNAL_SCOUT_TASK.md).
   - **Andere**: Formuliere die Aufgabe basierend auf dem Kickoff-Dokument.

4. **Monitoring**:
   Überwache die Ausgaben der CLI. Da der externe Agent Zugriff auf das Verzeichnis hat, wirst du sehen, wie neue Dateien in `Quellen/` oder `Siebenwind_Wiki/` erscheinen.

5. **Re-Integration**:
   Sobald der externe Agent fertig ist, führe in Antigravity einen Audit durch:
   // turbo
   `./7w_wiki.py audit`

6. **Cleanup**:
   Lösche temporäre Arbeitsdateien des externen Agenten, falls vorhanden.
