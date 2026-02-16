---
uuid: 52af70d6-90f7-4201-9374-c6cc2ce0c57e
status: ACTIVE
updated_at: 2026-02-16T16:25:00Z
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
| `/docs` | method_only | `7w_wiki.py check` + `7w_wiki.py stats` + `7w_wiki.py audit` + `7w_wiki.py archive sync` | Doku- und Pages-Paritaet |
| `/handover` | method_only | `7w_wiki.py start` + `7w_wiki.py advisor` + `7w_wiki.py stats` + `7w_wiki.py audit` | Session-Uebergabe |
| `/herold` | method_only | `7w_wiki.py stats` + Changelog/README Pflege | kein eigener Parser |
| `/ingest_master` | method_only | `7w_wiki.py advisor` + `7w_wiki.py search <query> --source wiki|quellen|all` | Prozessrahmen |
| `/ingestion_protocol` | executable | `7w_wiki.py archive sync` + `7w_wiki.py sanitize --auto` + `7w_wiki.py score <file>` | Teilweise automatisiert |
| `/lore_master` | executable | `7w_wiki.py historian <query>` | Department-Prozess |
| `/meta_master` | executable | `7w_wiki.py archive sync` | Archiv-Management |
| `/narrative_enrichment` | method_only | `7w_wiki.py historian <query>` | kein eigener Parser |
| `/researcher` | method_only | `7w_wiki.py search <query> --source all` | Recherchemodus |
| `/rvw_loop` | method_only | `7w_wiki.py search <query> --source all` + manuelle Schritte | kein Parser |
| `/scout` | method_only | `7w_wiki.py advisor` + manuelle Web-Sichtung | passiver News-Scout |
| `/takeover` | method_only | `7w_wiki.py start` + `7w_wiki.py advisor` + `7w_wiki.py mail inbox` | Amtsuebergabe |
| `/translate` | executable | `7w_wiki.py translate` | Sprach-Parser |
| `/update` | executable | `7w_wiki.py audit` + `7w_wiki.py sanitize --auto` + `7w_wiki.py index --status` | Systempflege |
| `/watch` | executable | `7w_wiki.py watch` | Live-Watcher |
| `/wiki_process` | method_only | `ingestion_protocol` + `rvw_loop` | methodischer Rahmen |

## Regel
Neue Workflows muessen vor Aktivierung in diese Matrix eingetragen werden.
