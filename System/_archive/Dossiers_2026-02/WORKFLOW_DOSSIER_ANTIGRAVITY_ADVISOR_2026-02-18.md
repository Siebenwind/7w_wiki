# Kritisches Dossier: Antigravity, Advisor und Workflow-Kommandos (2026-02-18)

## Auftrag

Klaeren, wie "Antigravity" benannt und verwendet wird, wie sich `advisor`, `start`, `takeover`, `handover`, `antigravity` und `leitpunkt` unterscheiden, und welche Verbesserungen sinnvoll sind.

## Quellenbasis

- Interne Artefakte:
  - `7w_wiki.py`
  - `.agent/scripts/advisor.py`
  - `.agent/workflows/start.md`
  - `.agent/workflows/takeover.md`
  - `.agent/workflows/handover.md`
  - `.agent/workflows/antigravity.md`
  - `.agent/workflows/leitpunkt.md`
  - `System/Synapse_Board/SY_WORKFLOW_CLI_MATRIX.md`
- Externe Referenz (Google/Gemini CLI):
  - <https://codelabs.developers.google.com/codelabs/use-agent-mode-gemini-cli>
  - Dort werden Regeln/Workflows ueber Markdown-Dateien organisiert (`global_rules.md`, `global_workflows.md`), nicht als festes eingebautes Slash-Command-System.

## Wie heisst es "dort" (Google/Gemini)?

Im Google/Gemini-CLI-Kontext heisst es typischerweise **Rules and Workflows** und wird als Datei-Setup verwaltet (`.gemini/...`, global oder projektlokal), nicht als verpflichtender, einzelner Runtime-Befehl namens `antigravity`.

## Konkrete Funktionsdifferenzen

| Befehl | Typ | Zweck | Effekt |
|---|---|---|---|
| `./7w_wiki.py advisor` | Runtime-Command | Status-Dashboard + Next-Step-Empfehlung | fuehrt echte Auswertung aus (`MASTER_TASK_LIST`, Dispatch, Audit, Quellenlage) |
| `./7w_wiki.py start` | Workflow-View | Onboarding-Anleitung | zeigt Protokoll, fuehrt keine Steps automatisch aus |
| `./7w_wiki.py takeover` | Workflow-View | Session-Adoption/Amtsuebernahme | zeigt Ritual + Checkliste |
| `./7w_wiki.py handover` | Workflow-View | Session-Abgabe/Uebergabe | zeigt Abschlussprotokoll + Pflichten |
| `./7w_wiki.py antigravity` | Workflow-View (neu) | Core-Default-Protokoll | zeigt den methodischen Kernloop |
| `./7w_wiki.py leitpunkt ...` | Runtime-Tooling | menschlichen Steueranker pruefen/pflegen | `status/check/scaffold`, optional `--strict` |

## Advisor-Analyse (konkret)

### Was `advisor` technisch tut

- liest Prioritaetsbloecke und naechsten offenen Task aus `MASTER_TASK_LIST.md`
- liest letzten Changelog-Eintrag
- zaehlt "Pending" in `Logs/INVENTUR_QUELLEN.md`
- zaehlt Dispatch-Status in `System/Synapse_Board/DISPATCH/`
- startet Konsistenzpruefung ueber `register_check.py` und wertet Problemanzahl aus
- leitet Empfehlung deterministisch ab

### Staerken

- niedrige Einstiegshuerde: ein Befehl, klares Lagebild
- priorisiert sichtbare Betriebsrisiken (Audit, Queue, Quellenstau)
- guter Session-Startpunkt fuer neue Agenten

### Kritische Grenzen

1. Audit dominiert die Empfehlungskette fast immer.  
   Folge: andere P1-Themen (z. B. Oracle-Reliability) werden leicht ueberschatten.
2. "Naechster Task" basiert auf erstem offenen Checkbox-Treffer.  
   Folge: semantisch wichtigere Aufgaben koennen nachrangig erscheinen.
3. `Pending`-Zaehlung ist rein textbasiert.  
   Folge: robust gegen Sonderfaelle nur begrenzt.
4. Kein maschinenlesbarer Output-Mode (`--json`).  
   Folge: schwerer in Automationen weiterzuverarbeiten.

## Kritische Interop-Befunde zu Workflows

1. Erwartungsproblem "Auto-Execution" vs. "Workflow-View"  
   - CLI-Kommandos `start/takeover/handover/antigravity` zeigen primar Workflow-Text.
   - Checklisten mit `// turbo` sind method hints, keine implizite Ausfuehrung im CLI.
2. Benennungsproblem "Adivor/Advisor"  
   - Der operative Status-Command heisst `advisor`.
   - Tipp-/Alias-Robustheit fehlt derzeit.
3. `/handover` Test-Gate ist zu hart gekoppelt (`audit-readiness` = 0 Probleme).  
   - In realen Umbauphasen blockiert das den Handover-Test, obwohl der Workflow selbst funktioniert.

## Bereits vorgenommene Korrekturen in dieser Iteration

- `antigravity` als eigener CLI-Befehl eingebunden (`./7w_wiki.py antigravity`)
- `antigravity`-Workflowtitel bereinigt (kein `# null` mehr)
- Matrix/Handbook klargezogen: `// turbo` als method hint, nicht stilles Auto-Run
- Maintainer-Leitpunkt konkretisiert und Strict-Policy differenziert

## Verbesserungsvorschlaege (priorisiert)

1. **Advisor um `--json` erweitern (P1)**  
   Ziel: reproduzierbare maschinenlesbare Auswertung fuer Automationen.
2. **Handover-Test entkoppeln von "0 Audit-Probleme" (P1)**  
   Ziel: Workflow-Integritaet testen statt globalen Vollgruen-Zustand erzwingen.
3. **Command-Aliase fuer Tippfehler (`adivor` -> `advisor`) (P2)**  
   Ziel: robustere UX bei manueller Bedienung.
4. **Expliziter Execute-Mode fuer Start/Takeover/Handover (P2)**  
   Beispiel: `./7w_wiki.py takeover --run-checklist`.
5. **Advisor-Empfehlungslogik gewichten (P2)**  
   Audit bleibt wichtig, aber parallel P1-Streams sichtbar machen (z. B. Oracle/Test-Stability).

## Empfehlung zur "Strict-Gruen"-Frage

- `leitpunkt check` (normal) = Tagesbetriebsgate.
- `leitpunkt check --strict` = Governance-/Release-/Handover-Gate.
- Damit bleibt Entwicklung beweglich, ohne Leitungsdisziplin aufzugeben.

