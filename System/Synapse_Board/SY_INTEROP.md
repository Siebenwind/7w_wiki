---
uuid: 4f249a8d-33da-4cbf-9fc4-ff9df2bf8563
status: ACTIVE
updated_at: 2026-02-18T01:05:00Z
owners:
  - Koordinator
  - Netz-Waechter
epistemic: "#meta"
---

# SY_INTEROP

Verbindliche Interoperabilitaetsnorm fuer die Antigravity-Struktur (`.agent/*`) und die Laufzeit des Projekts.

## Ziel
Jeder Agent soll ohne Vorwissen sofort erkennen:
1. Welche Workflows rein methodisch sind,
2. welche Kommandos tatsaechlich ausfuehrbar sind,
3. welche Boards als verbindliche Kommunikationspfade gelten.

## Norm 1: Link- und Pfadpolitik
- In Wiki-/System-Dokumenten sind **keine absoluten `file://` Pfade** erlaubt.
- Erlaubt sind:
  - repo-relative Markdown-Links (z. B. `System/Synapse_Board/SY_REVIEW.md`),
  - `[[WikiLinks]]` fuer Wissensseiten.
- Ausnahme: Externe Webquellen (`https://...`) sind zulaessig.

## Norm 1b: Bridge-Page-Policy
- Brueckenartikel/Stub-Platzhalter sind **kein Standard-Reparaturweg**.
- Standard ist: Link auf bestehendes kanonisches Ziel reparieren oder valide Zielseite mit belegbarer Quelle erstellen.
- Falls eine temporaere Bruecke unvermeidbar ist, sind diese Felder verpflichtend:
  - `bridge_mode: temporary`
  - `bridge_target: [[...]]`
  - `bridge_ticket: MSG-...` (oder Task-ID)
  - `bridge_review_until: YYYY-MM-DD`
- Seiten mit Bridge-Markern ohne diese Felder gelten als Interop-/Qualitaetsdefect.

## Norm 2: Ausfuehrbarkeit vs. Methodik
- Nur Befehle, die in `7w_wiki.py` via `add_parser(...)` existieren, gelten als **runtime-executable**.
- Workflows ohne CLI-Entsprechung muessen als **methodisch** markiert werden.
- Jeder Department-Workflow enthaelt am Anfang einen Block:
  - `runtime_commands:` (real existierende Befehle)
  - `method_only:` (nur Prozessbeschreibung)
  - optional `method_hints_non_runtime:` (Host-Tooling/Hilfsmethoden, klar als nicht-runtime markiert)
- `method_hints_non_runtime` darf **niemals** als Ersatz fuer `runtime_commands` verwendet werden.
- Workflow-Bridges fuer Codex werden zusaetzlich ueber Metadaten im `Interop-Status` erzeugt; diese duerfen Runtime-Semantik nicht eigenmaechtig ueberschreiben.

## Norm 3: Command Registry (Single Source)
Die operative Kommandoliste lautet aktuell:

<!-- BEGIN GENERATED RUNTIME COMMAND LIST -->
- `search`
- `start`
- `test`
- `takeover`
- `handover`
- `historian`
- `repair`
- `audit`
- `index`
- `index-pages`
- `pages`
- `advisor`
- `inquisition`
- `sanitize`
- `lint`
- `score`
- `ingest`
- `translate`
- `watch`
- `package`
- `check`
- `archive`
- `mail`
- `scout`
- `tech`
- `version`
- `antigravity`
- `leitpunkt`
- `stats`
- `mcp`
<!-- END GENERATED RUNTIME COMMAND LIST -->


Bei CLI-Aenderungen muss diese Liste in derselben Session synchronisiert werden.

## Norm 4: Messaging-State-Modell
Fuer Agent-zu-Agent Arbeit ist `SY_DISPATCH` verbindlich:
- Pfad: `System/Synapse_Board/DISPATCH/`
- Statuskette: `OPEN` -> `CLAIMED` -> `DONE`
- Pflichtfelder je Nachricht:
  - `id`, `uuid`, `status`, `priority`, `from_agent`, `to_agent`, `created_at`
- `to_agent: ALL` gilt als Broadcast.
- Bei parallelen Board-Edits gilt ein Settle-Window von 30 Sekunden vor erneuter Statusmutation.
- Das Settle-Window ist zentral konfigurierbar ueber `.agent/config/runtime.json`.

## Norm 4b: Pages-Integrity-Policy
- Publizierte Site-Integritaet wird ueber `./7w_wiki.py pages validate --json` und `./7w_wiki.py audit --pages` sichtbar gemacht.
- Default-Semantik: unresolved interne Roamlinks-Ziele sind `WARN`, kein harter FAIL.
- Harter Gate-Modus ist explizit: `./7w_wiki.py pages validate --json --strict-links`.
- Erwartete Ausnahmen duerfen nur in `.agent/config/pages_link_policy.json` gepflegt werden.
- Jede Ausnahme braucht `target`, `status`, `reason`, `owner`, `review_until`.
- Laufzeit-Snapshot fuer Agenten/Advisor: `.agent/data/pages_health.json`.

## Norm 5: Artefakt-Referenzen
Workflows duerfen nur auf Artefakte verweisen, die entweder:
- existieren, oder
- explizit als `planned_artifact` markiert sind.

Nicht existente, aber als Pflicht benannte Dateien sind als **interop blocker** zu behandeln.
- Release-Bundles unter `dist/` sind Runtime-/Release-Artefakte. Sie duerfen lokal erzeugt oder als GitHub Release-Asset veroeffentlicht werden, gehoeren aber nicht in den normalen Repo-Verlauf.

## Norm 6: Onboarding-Minimum
`/start` (bzw. `7w_wiki.py start`) muss auf folgende Kernstellen verweisen:
- `System/Synapse_Board/SY_INTEROP.md`
- `System/Synapse_Board/SY_DISPATCH.md`
- `System/Synapse_Board/SY_STANDARDS.md`
- `System/COORDINATION_HUB.md`

## Norm 7: Test- und Defect-Kommunikation
- Standardisierte Interop-Tests laufen ueber `./7w_wiki.py test --suite ...`.
- Bei Test-FAILs gilt: zuerst Defect-Kommunikation (Dispatch oder Task), dann Fix.
- Verbindliche Details stehen in `System/Synapse_Board/SY_TESTING.md`.

## Norm 8: Single Script Directory Policy
- Alle operativen Skripte, Helper und Automatisierungen **muessen** im zentralen Verzeichnis `.agent/scripts/` abgelegt werden.
- Die Anlage kompetitiver Verzeichnisse (z.B. `Scripts/`, `bin/`) im Wurzelverzeichnis ist untersagt.
- Veraltete Skripte sind nach `.agent/scripts/_archive/` zu verschieben, nicht zu loeschen.
- Sonderfall `scout`: Die Discovery-Prominenz ist eine bewusste Produktentscheidung, aber der Backend-Pfad bleibt trotzdem `.agent/scripts/forum_scanner.py`.

## Norm 9: Codex-Workflow-Bridges
- Codex bekommt keine repo-definierten Slash-Kommandos.
- Stattdessen werden ausgewaehlte Workflows als duenne Wrapper in `.agents/skills/` gespiegelt.
- Diese Wrapper muessen auf `.agent/workflows/...` verweisen und duerfen Runtime-Ausfuehrung nur ueber `./7w_wiki.py` beschreiben.
- `/scout` bleibt der promoted Umbrella-Einstieg; `/forum_search` ist der spezialisierte, forum-fokussierte Arbeitsweg.

## Compliance-Checks
Bei jedem groesseren Update:
1. Scan auf `file://` in `.agent/workflows`, `.agent/instructions`, `System/`.
2. Abgleich Workflow-Kommandos gegen `7w_wiki.py`.
3. Dispatch-Queue auf offene Direktiven pruefen.
4. Interop-Testlauf ausfuehren (`./7w_wiki.py test --suite clean-client-state`, `./7w_wiki.py test --suite interop-doc-links`, optional RAG-Diagnose nur explizit via `./7w_wiki.py test --suite rag-relevance-smoke --timeout 30` oder `./7w_wiki.py test --suite all --include-rag`).
5. Pages-Contract pruefen (`./7w_wiki.py test --suite pages-link-contract`).
6. Bridge-Guard pruefen (`./7w_wiki.py test --suite bridge-placeholder-guard`).
7. Codex-Workflow-Bridge-Guard pruefen (`./7w_wiki.py test --suite codex-workflow-bridges`).
8. Reader-Stats-Guard pruefen (`./7w_wiki.py test --suite reader-stats-contract`).
9. Changelog-Eintrag mit Interop-Delta erstellen.

## Beschluss
Diese Norm gilt ab sofort fuer alle neuen und ueberarbeiteten Antigravity-Artefakte.
