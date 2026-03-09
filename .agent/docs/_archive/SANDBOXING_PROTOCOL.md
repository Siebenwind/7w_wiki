# Protokoll: Lore-Integrität & Sandboxing (v1.0)

Dieses Protokoll definiert die Regeln für Testläufe und Simulationen, um sicherzustellen, dass die Wissensbasis (#canon, #bote) und die Primärquellen niemals verunreinigt werden.

## 1. Das "Sandbox"-Prinzip
Testläufe finden ausschließlich in isolierten Umgebungen statt:

- **Tickets:** Test-Tickets müssen das Präfix `TEST_` tragen (z.B. `Conflict_TEST_001.md`).
- **Dateien:** Änderungen an Wiki-Artikeln während eines Tests werden nicht direkt gespeichert, sondern als ".tmp" oder in einem speziellen `/System/Sandbox/` Verzeichnis abgelegt.
- **Git-Protection:** Während eines Testlaufs sind automatische `git push` Befehle untersagt.

## 2. Der Simulation-Modus (Dry Run)
Bevor der Historiker oder Archivar eine "echte" Korrektur vornimmt, muss er:

1.  **Draft-Modus:** Die geplante Änderung im Ticket (`RESOLVED` Sektion) dokumentieren, anstatt die Zieldatei zu überschreiben.
2.  **User-Freigabe:** Bei Test-Tickets ist eine explizite Bestätigung durch den User erforderlich (`AWAITING_USER`), bevor die Sandbox verlassen wird.

## 3. Rollback-Verfahren
Jeder Testlauf muss spurlos entfernbar sein:

- **Cleanup-Befehl:** Nach Abschluss eines Tests müssen alle `TEST_` Dateien gelöscht werden.
- **Git-Reset:** Falls versehentlich Dateien geändert wurden, wird mittels `git checkout -- [Pfad]` der Originalzustand wiederhergestellt.

## 4. Kennzeichnung von Testdaten
Falls Testdaten generiert werden müssen (z.B. ein fiktiver Widerspruch), müssen diese am Anfang und Ende des Textes mit folgenden Tags umschlossen sein:
`>>> TESTDATEN START >>>`
...
`<<< TESTDATEN ENDE <<<`

---
**Status:** Aktiv | **Gültigkeit:** Für alle Agenten-Testläufe.
