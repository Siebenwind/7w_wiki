---
description: Policy-driven delegation contract for bounded helper tasks; main-agent judgment stays local.
---

Dieser Workflow beschreibt die **Delegationspolitik**, nicht einen Freibrief fuer freie Fremd-Agenten. Hauptentscheidungen zu Architektur, Kanon, Integrationsrichtung und finaler Antwort bleiben beim aktiven Hauptagenten.

## Interop-Status
- runtime_commands:
  - `7w_wiki.py start`
  - `7w_wiki.py audit`
- method_only:
  - `/delegate`
- interop_note: Delegation ist policy-driven und host-abhaengig. Die kanonische Konfiguration liegt in `.agent/config/delegation_policy.json`; Ausuebung ist optional.

## Grundsatz

1. Delegation ist nur fuer **kleine, klar umrissene Nebenaufgaben** gedacht.
2. Default-Profile sind billig und konservativ:
   - Read-only Survey/Verify: `gpt-5.4-mini` mit `low`
   - Bounded Coding: `gpt-5.3-codex` mit `low`
3. Kein Default-`xhigh`.
4. Kein offenes "Agent spawns agent" ohne Task-Class, Scope und Rueckgabeformat.

## Task-Klassen

- `read_survey`
- `search_inventory`
- `doc_summary`
- `verification_pass`
- `test_repro`
- `bounded_code_change`

Jede Klasse definiert:
- Schreibrecht oder Read-only
- Parallel-Sicherheit
- erlaubte Modellprofile
- Rueckgabeformat

## Pflichtfelder fuer eine Delegation

1. `task_class`
2. `objective`
3. `expected_output`
4. `allowed_paths`
5. `disallowed_paths`
6. `write_allowed`
7. `recommended_profile`
8. `acceptance_check`
9. `handoff_format`

## Rueckfuehrung

Nach jeder delegierten Nebenaufgabe gilt:

1. Ergebnisse pruefen.
2. `./7w_wiki.py audit` oder die passende fokussierte Validierung laufen lassen.
3. Hauptagent integriert oder verwirft das Ergebnis explizit.

## Aktueller Status

Die kanonische Delegationsrichtlinie liegt in:
- `.agent/config/delegation_policy.json`

Dieses Repository beschreibt Delegation bereits als Policy. Ob ein Host tatsaechlich Subagenten ausuebt, bleibt eine Host-Entscheidung.
