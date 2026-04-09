---
description: Deprecated compatibility alias that redirects to /start
---

# Workflow: `/antigravity` (Compatibility Alias)

## Interop-Status
- runtime_commands:
  - `7w_wiki.py antigravity`
  - `7w_wiki.py start`
- method_only:
  - `/antigravity`
- interop_note: Deprecated compatibility alias. `./7w_wiki.py antigravity` now prints a deprecation note and then shows `/start`.
- matrix_status: executable
- catalog_id: `workflow.antigravity`
- primary_command: `7w_wiki.py antigravity`
- followup_commands:
  - `7w_wiki.py start`
  - `7w_wiki.py advisor --json`
- adapter_targets:
  - `mcp:compat/antigravity`
- deprecated_aliases:
  - `/antigravity`

`/antigravity` ist kein architektonisches Zentrum mehr. Es bleibt nur als **Kompatibilitätsalias** fuer alte Runbooks, alte Agentengewohnheiten und historische Dokumentation erhalten.

## Status

1. Verwende fuer neue Sessions und neue Dokumentation immer `/start` beziehungsweise `./7w_wiki.py start`.
2. Behandle `./7w_wiki.py antigravity` als Weiterleitung, nicht als eigene Steuerungsebene.
3. Migriere neue Integrationen auf den kanonischen Kern:
   - `.agent/` fuer Authoring und Governance
   - `./7w_wiki.py` fuer Runtime
   - MCP fuer offene Laufzeit-Integration
   - `.agents/skills/` plus `.codex/config.toml` fuer den Codex-Adapter

## Historischer Hinweis

Antigravity bleibt als historischer Begriff sichtbar, damit alte Arbeitsprotokolle lesbar bleiben. Neue Prozesse, neue Tests und neue Onboarding-Hinweise referenzieren jedoch `/start`.
