---
uuid: 52af70d6-90f7-4201-9374-c6cc2ce0c57e
status: ACTIVE
updated_at: 2026-02-15T00:18:00Z
epistemic: "#meta"
---

# SY_WORKFLOW_CLI_MATRIX

Zweck: Bruecke zwischen historisch gewachsenen Slash-Workflows und tatsaechlich ausfuehrbaren CLI-Kommandos.

## Runtime Commands
- `advisor`, `archive`, `audit`, `check`, `historian`, `index`, `index-pages`, `inquisition`, `mail`, `repair`, `sanitize`, `score`, `search`, `start`, `stats`, `translate`, `watch`

## Adaptermatrix

| Workflow-Slash | Status | Runtime-Adapter | Hinweis |
|---|---|---|---|
| `/start` | executable | `7w_wiki.py start` | Onboarding-Einstieg |
| `/audit` | executable | `7w_wiki.py audit` | Konsistenzpruefung |
| `/repair` | executable | `7w_wiki.py repair` | Interaktive Reparatur |
| `/historian` | executable | `7w_wiki.py historian [query]` | Lore-Analyse |
| `/stats` | executable | `7w_wiki.py stats` | Projektmetriken |
| `/ask` | method_only | `7w_wiki.py search <query> --source all` | Auskunftsmodus ueber Suche |
| `/batch` | method_only | `7w_wiki.py advisor` + manuelle Abarbeitung `INVENTUR_QUELLEN` | Batch-Prozess |
| `/check_master` | executable | `7w_wiki.py check` | Stil- & QA-Pruefung |
| `/contrib_audit` | method_only | `7w_wiki.py audit` + manuelle Review-Checks | kein eigener Parser |
| `/decide` | method_only | `7w_wiki.py mail post --to ALL ...` | Entscheidungsanforderung |
| `/docs` | method_only | `7w_wiki.py stats` + manuelle Doku-Syncs | `/docs` Workflow |
| `/handover` | method_only | `7w_wiki.py mail post --to ALL --subject "Handover" ...` | Uebergabe via Dispatch |
| `/herold` | method_only | `7w_wiki.py stats` + Changelog/README Pflege | kein eigener Parser |
| `/ingest_master` | method_only | `7w_wiki.py advisor` + `7w_wiki.py search` | Prozessrahmen |
| `/ingestion_protocol` | executable | `7w_wiki.py sanitize` / `score` | Teilweise automatisiert |
| `/lore_master` | executable | `7w_wiki.py historian <query>` | Department-Prozess |
| `/meta_master` | executable | `7w_wiki.py archive sync` | Archiv-Management |
| `/narrative_enrichment` | method_only | `7w_wiki.py historian <query>` | kein eigener Parser |
| `/researcher` | method_only | `7w_wiki.py search <query> --source all` | Recherchemodus |
| `/rvw_loop` | method_only | `7w_wiki.py search` + manuelle Schritte | kein Parser |
| `/scout` | method_only | `7w_wiki.py search` | Scouting |
| `/takeover` | method_only | `7w_wiki.py start` + `SY_INTEROP` Check | kein eigener Parser |
| `/translate` | executable | `7w_wiki.py translate` | Sprach-Parser |
| `/update` | executable | `7w_wiki.py index --rebuild` | Index-Management |
| `/watch` | executable | `7w_wiki.py watch` | Live-Watcher |
| `/wiki_process` | method_only | `ingestion_protocol` + `rvw_loop` | methodischer Rahmen |

## Regel
Neue Workflows muessen vor Aktivierung in diese Matrix eingetragen werden.
