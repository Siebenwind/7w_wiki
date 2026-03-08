---
uuid: 52af70d6-90f7-4201-9374-c6cc2ce0c57e
status: ACTIVE
updated_at: 2026-02-18T01:05:00Z
epistemic: "#meta"
---

# SY_WORKFLOW_CLI_MATRIX

Zweck: Bruecke zwischen historisch gewachsenen Slash-Workflows und tatsaechlich ausfuehrbaren CLI-Kommandos.

## Runtime Commands
- `advisor`, `antigravity`, `archive`, `audit`, `check`, `handover`, `historian`, `index`, `index-pages`, `inquisition`, `leitpunkt`, `mail`, `pages`, `repair`, `sanitize`, `score`, `scout`, `search`, `start`, `stats`, `takeover`, `test`, `translate`, `watch`

## Adaptermatrix

| Workflow-Slash | Status | Runtime-Adapter | Hinweis |
|---|---|---|---|
| `/start` | executable | `7w_wiki.py start` + `7w_wiki.py mail inbox --status OPEN` + `7w_wiki.py test --suite clean-client-state` | Onboarding-Einstieg mit Dispatch- und Clean-State-Sichtung |
| `/audit` | executable | `7w_wiki.py audit` | Konsistenzpruefung |
| `/repair` | executable | `7w_wiki.py repair` oder `7w_wiki.py repair --full` | Interaktive Reparatur oder Voll-Durchlauf 1→3 (Frontmatter, Links, Source-Refs); keine Stub-/Brueckenartikel als Standard-Fix |
| `/historian` | executable | `7w_wiki.py historian [query]` | Lore-Analyse |
| `/stats` | executable | `7w_wiki.py stats` | Leserzentrierter Wiki-Kompass + Tracking-Register + maschinenlesbarer Snapshot |
| `/test_run` | executable | `7w_wiki.py test --suite clean-client-state|takeover-handover|interop-doc-links|source-link-hygiene|process-dispatch-curiosity|bridge-placeholder-guard|reader-stats-contract|all` + optional `--include-rag` / `--suite rag-relevance-smoke` / `--post-failures` | Standardisierter Interop-, Policy- und Reader-Stats-Testlauf; RAG-Smoke nur als explizite Diagnose |
| `/ask` | method_only | `7w_wiki.py search <query> --source all` | Auskunftsmodus ueber Suche |
| `/batch` | method_only | `7w_wiki.py advisor` + manuelle Abarbeitung `INVENTUR_QUELLEN` | Batch-Prozess |
| `/check_master` | executable | `7w_wiki.py check` | Stil- & QA-Pruefung |
| `/contrib_audit` | method_only | `7w_wiki.py audit` + manuelle Review-Checks | kein eigener Parser |
| `/decide` | method_only | `7w_wiki.py mail inbox --status OPEN` + `7w_wiki.py mail read <id>` + `7w_wiki.py mail claim <id> --agent <name>` + `7w_wiki.py mail done <id> --agent <name>` | Entscheidungsbearbeitung ueber Dispatch |
| `/docs` | method_only | `7w_wiki.py check` + `7w_wiki.py stats` + `7w_wiki.py pages validate` + `7w_wiki.py archive sync` | Doku- und Pages-Paritaet inkl. Build-Validierung |
| `/handover` | executable | `7w_wiki.py handover` (plus manuelle Ausfuehrung der Checklistenkommandos) | CLI zeigt Protokoll; `// turbo` ist method hint, keine implizite Auto-Execution |
| `/herold` | method_only | `7w_wiki.py stats` + Changelog/README Pflege | kein eigener Parser |
| `/ingest_master` | method_only | `7w_wiki.py advisor` + `7w_wiki.py search <query> --source wiki|quellen|all` | Prozessrahmen |
| `/ingestion_protocol` | executable | `7w_wiki.py archive sync` + `7w_wiki.py sanitize --auto` + `7w_wiki.py score <file>` | Teilweise automatisiert |
| `/lore_master` | executable | `7w_wiki.py historian <query>` | Department-Prozess |
| `/meta_master` | executable | `7w_wiki.py archive sync` | Archiv-Management |
| `/narrative_enrichment` | method_only | `7w_wiki.py historian <query>` | kein eigener Parser |
| `/researcher` | method_only | `7w_wiki.py search <query> --source all` | Recherchemodus |
| `/rvw_loop` | method_only | `7w_wiki.py search <query> --source all` + manuelle Schritte | kein Parser |
| `/scout` | executable | `7w_wiki.py scout --forum bekanntmachungen|news --pages N` | Automatisierter Forum-Deep-Scan |
| `/takeover` | executable | `7w_wiki.py takeover` (plus manuelle Ausfuehrung der Checklistenkommandos) | CLI zeigt Protokoll; `// turbo` ist method hint, keine implizite Auto-Execution |
| `/tech` | executable | `7w_wiki.py tech` | System-Wartung & DevOps (Netz-Ingenieur) |
| `/antigravity` | executable | `7w_wiki.py antigravity` | Core-Protocol als aufrufbarer Workflow-Hub |
| `/leitpunkt` | executable | `7w_wiki.py leitpunkt` / `7w_wiki.py leitpunkt status|check|scaffold` | Menschlicher Steueranker inkl. Struktur- und Reifegrad-Checks |
| `/translate` | executable | `7w_wiki.py translate` | Sprach-Parser |
| `/update` | executable | `7w_wiki.py audit` + `7w_wiki.py sanitize --auto` + `7w_wiki.py index --status` | Systempflege |
| `/watch` | executable | `7w_wiki.py watch` | Live-Watcher |
| `/wiki_process` | method_only | `ingestion_protocol` + `rvw_loop` | methodischer Rahmen |

## Regel
Neue Workflows muessen vor Aktivierung in diese Matrix eingetragen werden. 
**Auto-Update:** Um fehlende Workflows automatisch zu erfassen, fuehre aus:
`./.agent/scripts/update_matrix.py`
| `/canon_update` | TBD | TBD | Auto-detected (please update) |
| `/delegate` | TBD | TBD | Auto-detected (please update) |
| `/wiki_style_guide` | TBD | TBD | Auto-detected (please update) |
| `/qa_master` | TBD | TBD | Auto-detected (please update) |
| `/tech_master` | TBD | TBD | Auto-detected (please update) |
