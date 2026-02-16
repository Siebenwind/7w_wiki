---
uuid: 4f249a8d-33da-4cbf-9fc4-ff9df2bf8563
status: ACTIVE
updated_at: 2026-02-16T21:18:56Z
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

## Norm 2: Ausfuehrbarkeit vs. Methodik
- Nur Befehle, die in `7w_wiki.py` via `add_parser(...)` existieren, gelten als **runtime-executable**.
- Workflows ohne CLI-Entsprechung muessen als **methodisch** markiert werden.
- Jeder Department-Workflow enthaelt am Anfang einen Block:
  - `runtime_commands:` (real existierende Befehle)
  - `method_only:` (nur Prozessbeschreibung)
  - optional `method_hints_non_runtime:` (Host-Tooling/Hilfsmethoden, klar als nicht-runtime markiert)
- `method_hints_non_runtime` darf **niemals** als Ersatz fuer `runtime_commands` verwendet werden.

## Norm 3: Command Registry (Single Source)
Die operative Kommandoliste lautet aktuell:
- `advisor`, `archive`, `audit`, `check`, `handover`, `historian`, `index`, `index-pages`, `inquisition`, `mail`, `pages`, `repair`, `sanitize`, `score`, `search`, `start`, `stats`, `takeover`, `test`, `translate`, `watch`

Bei CLI-Aenderungen muss diese Liste in derselben Session synchronisiert werden.

## Norm 4: Messaging-State-Modell
Fuer Agent-zu-Agent Arbeit ist `SY_DISPATCH` verbindlich:
- Pfad: `System/Synapse_Board/DISPATCH/`
- Statuskette: `OPEN` -> `CLAIMED` -> `DONE`
- Pflichtfelder je Nachricht:
  - `id`, `uuid`, `status`, `priority`, `from_agent`, `to_agent`, `created_at`
- `to_agent: ALL` gilt als Broadcast.

## Norm 5: Artefakt-Referenzen
Workflows duerfen nur auf Artefakte verweisen, die entweder:
- existieren, oder
- explizit als `planned_artifact` markiert sind.

Nicht existente, aber als Pflicht benannte Dateien sind als **interop blocker** zu behandeln.

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

## Compliance-Checks
Bei jedem groesseren Update:
1. Scan auf `file://` in `.agent/workflows`, `.agent/instructions`, `System/`.
2. Abgleich Workflow-Kommandos gegen `7w_wiki.py`.
3. Dispatch-Queue auf offene Direktiven pruefen.
4. Interop-Testlauf ausfuehren (`./7w_wiki.py test --suite clean-client-state`, `./7w_wiki.py test --suite interop-doc-links`, `./7w_wiki.py test --suite rag-relevance-smoke`).
5. Changelog-Eintrag mit Interop-Delta erstellen.

## Beschluss
Diese Norm gilt ab sofort fuer alle neuen und ueberarbeiteten Antigravity-Artefakte.
