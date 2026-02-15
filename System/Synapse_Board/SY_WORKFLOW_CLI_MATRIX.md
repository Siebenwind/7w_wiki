---
uuid: 52af70d6-90f7-4201-9374-c6cc2ce0c57e
status: ACTIVE
updated_at: 2026-02-15T00:18:00Z
epistemic: "#meta"
---

# SY_WORKFLOW_CLI_MATRIX

Zweck: Bruecke zwischen historisch gewachsenen Slash-Workflows und tatsaechlich ausfuehrbaren CLI-Kommandos.

## Runtime Commands
- `advisor`, `audit`, `historian`, `index`, `index-pages`, `mail`, `repair`, `search`, `start`, `stats`

## Adaptermatrix

| Workflow-Slash | Status | Runtime-Adapter | Hinweis |
|---|---|---|---|
| `/start` | executable | `7w_wiki.py start` | Onboarding-Einstieg |
| `/audit` | executable | `7w_wiki.py audit` | Konsistenzpruefung |
| `/repair` | executable | `7w_wiki.py repair` | Interaktive Reparatur |
| `/historian` | executable | `7w_wiki.py historian [query]` | Lore-Analyse |
| `/stats` | executable | `7w_wiki.py stats` | Projektmetriken |
| `/ask` | method_only | `7w_wiki.py search <query> --source all` | Auskunftsmodus ueber Suche |
| `/batch` | method_only | `7w_wiki.py advisor` + manuelle Abarbeitung `INVENTUR_QUELLEN` | Batch-Prozess, kein eigener Parser |
| `/check_master` | method_only | `7w_wiki.py audit` -> `7w_wiki.py repair` | Department-Prozess |
| `/contrib_audit` | method_only | `7w_wiki.py audit` + manuelle Review-Checks | kein eigener Parser |
| `/decide` | method_only | `7w_wiki.py mail post --to ALL ...` | Entscheidungsanforderung via Dispatch |
| `/docs` | method_only | `7w_wiki.py stats` + manuelle Doku-Syncs | kein eigener Parser |
| `/handover` | method_only | `7w_wiki.py mail post --to ALL --subject "Handover" ...` | Uebergabe via Dispatch |
| `/herold` | method_only | `7w_wiki.py stats` + Changelog/README Pflege | kein eigener Parser |
| `/ingest_master` | method_only | `7w_wiki.py advisor` + `7w_wiki.py search` | Prozessrahmen |
| `/ingestion_protocol` | method_only | `System/Templates/INGESTION_REPORT_TEMPLATE.md` | Protokoll, kein Parser |
| `/lore_master` | method_only | `7w_wiki.py historian <query>` + `7w_wiki.py search` | Department-Prozess |
| `/meta_master` | method_only | `7w_wiki.py start` + `7w_wiki.py stats` | Department-Prozess |
| `/narrative_enrichment` | method_only | `7w_wiki.py historian <query>` | kein eigener Parser |
| `/researcher` | method_only | `7w_wiki.py search <query> --source all` | Recherchemodus |
| `/rvw_loop` | method_only | `7w_wiki.py search` + manuelle Write/Verify-Schritte | kein Parser |
| `/scout` | method_only | `7w_wiki.py search` | Scouting ohne eigenen Parser |
| `/takeover` | method_only | `7w_wiki.py start` + `SY_INTEROP` Check | kein eigener Parser |
| `/translate` | method_only | Manuell/Skill-basiert | kein Parser |
| `/update` | method_only | `7w_wiki.py index --status` / `--rebuild` | kein Parser |
| `/watch` | method_only | `.agent/scripts/watcher.py` (direkt) | ausserhalb von `7w_wiki.py` |
| `/wiki_process` | method_only | `ingestion_protocol` + `rvw_loop` | methodischer Rahmen |

## Regel
Neue Workflows muessen vor Aktivierung in diese Matrix eingetragen werden.
