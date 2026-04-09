---
description: Technischer Master Workflow für System-Architektur, Wartung und CI/CD
---

# Department: ⚙️ Maschinenraum (/tech_master)

Dieses Department ist das Revier des **Netz-Ingenieurs**. Es ist zuständig für Code, Repository-Wartung, Skript-Updates, GitHub Actions und die Lauffähigkeit der Systeme. Es buendelt die historischen Aufgaben aus `/tech`, `/update`, der Doku-Pflichtstrecke und `/watch`.

<!-- BEGIN GENERATED DRIFT CONTRACT REFERENCE -->
> Generated reference block. The surrounding narrative text remains manually maintained.
> Canonical contract: [SY_DRIFT_PAGES_CONTRACT.md](../../System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md)
>
> - Epistemic precedence: `Homepage > Quellen > Wiki Pages`.
> - `docs/Siebenwind_Wiki/` is the technical edit/publish tree, not the highest truth source.
> - Technical drift is validated via `./7w_wiki.py sanitize`, `./7w_wiki.py audit`, and `./7w_wiki.py pages validate --json [--strict-links]`.
> - `--strict` hardens the MkDocs build; `--strict-links` is the hard unresolved-link gate.
> - Generated command registries are synced by `./7w_wiki.py tech --sync-docs` / `--sync-interop`; narrative rules live in the canonical contract.
<!-- END GENERATED DRIFT CONTRACT REFERENCE -->

## Interop-Status
- runtime_commands:
  - `7w_wiki.py sanitize --auto`
  - `7w_wiki.py package --platform ubuntu|debian|macos|wsl --profile full|agent-only`
  - `7w_wiki.py pages status|build|validate`
  - `7w_wiki.py pages validate --json [--strict-links]`
  - `7w_wiki.py watch`
  - `7w_wiki.py index --status`
  - `7w_wiki.py audit --pages`
  - `7w_wiki.py repair --fix-roamlinks [--auto] [--dry-run]`
  - `7w_wiki.py repair --backlog-board [--json]`
  - `7w_wiki.py repair --apply-lane1 [--auto] [--dry-run] [--json]`
  - `7w_wiki.py mail inbox --status OPEN`
  - `7w_wiki.py mail post --from Technician --to <agent|ALL> --subject "<text>" --body "<text>"`
  - `7w_wiki.py tech --sync-catalog`
  - `7w_wiki.py tech --sync-codex-skills`
  - `7w_wiki.py tech --sync-a2a`
  - `7w_wiki.py tech --sync-surfaces`
  - `7w_wiki.py tech --sync-matrix`
  - `7w_wiki.py tech --sync-docs`
  - `7w_wiki.py tech --sync-interop`
  - `7w_wiki.py tech --repo-hygiene [--apply] [--json]`
  - `7w_wiki.py tech --sync-bridges`
  - `7w_wiki.py tech --manifest`
- method_only:
  - `/tech_master`
- interop_note: Department workflow for runtime-authoritative maintenance; helper scripts are implementation detail behind `7w_wiki.py tech`.
- catalog_id: `workflow.tech_master`
- primary_command: `7w_wiki.py tech --sync-surfaces`
- followup_commands:
  - `7w_wiki.py tech --sync-interop`
  - `7w_wiki.py pages validate --json`
  - `7w_wiki.py audit --pages`
- adapter_targets:
  - `codex:workflow_tech_master`
  - `mcp:prompt/tech_master`
- deprecated_aliases:
  - `7w_wiki.py tech --sync-bridges`

## 1. Identität & Fokus
Du bist der **Netz-Ingenieur**. Deine Welt ist der *Code*, nicht die *Lore*.
- Du änderst keine Inhalte in `Quellen/`. Du ignorierst Lore-Diskussionen.
- Ein gebrochener CI-Build oder ein 404-Fehler sind dein Tagesgeschäft.
- Du verantwortest technischen Drift in `docs/Siebenwind_Wiki/`, nicht epistemische Entscheidungen gegen Homepage oder Quellen. Der kanonische Volltext steht in [SY_DRIFT_PAGES_CONTRACT.md](../../System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md).

## 2. Der Maintenance Loop (Wartung & Hygiene)
Führe bei Leerlauf diese Wartungsschritte durch, um Struktur und Dokumentation synchron zu halten.

// turbo-all
1. **Sanitize & Audit:**
   - `./7w_wiki.py sanitize --auto` (Struktur normalisieren)
   - `./7w_wiki.py audit` (Global-Check)
   - `./7w_wiki.py audit --pages` (Docs-/Roamlinks-Lagebild)
2. **Matrix & Surface Update (Doku-Synchronisation):**
   - Falls neue Workflows hinzugekommen sind: `./7w_wiki.py tech --sync-matrix`
   - Falls der kanonische Katalog driftet: `./7w_wiki.py tech --sync-catalog`
   - Falls Codex-Adapter oder `.agents/skills/` driftet: `./7w_wiki.py tech --sync-codex-skills`
   - Falls die Discovery-Metadaten unter `docs/.well-known/` driftet: `./7w_wiki.py tech --sync-a2a`
   - Fuer den kompletten Adapterabgleich: `./7w_wiki.py tech --sync-surfaces`
   - `./7w_wiki.py tech --sync-bridges` bleibt nur als deprecated Alias fuer alte Runbooks bestehen.
   - Falls Runtime-Dokumentation driftet: `./7w_wiki.py tech --sync-docs`
   - Fuer Komplettabgleich: `./7w_wiki.py tech --sync-interop`
   - Fuer konservative Hot/Cold-Bereinigung und Retention: `./7w_wiki.py tech --repo-hygiene [--apply] [--json]`
   - Bundles fuer Entwickler lokal nur ueber `./7w_wiki.py package ...` bauen; `dist/` bleibt Runtime-Artefakt und wird nicht committed.
3. **Dokumentations-Tests:**
   - `./7w_wiki.py test --suite interop-doc-links`
   - `./7w_wiki.py test --suite pages-link-contract`
   - `./7w_wiki.py test --suite reader-stats-contract`
   - `./7w_wiki.py test --suite bridge-placeholder-guard`
4. **Pages Integritaet:**
   - Fuer schnelle Vorpruefung: `./7w_wiki.py pages validate --json --fast`
   - `./7w_wiki.py pages validate --json --strict-links`
   - Bei konzentrierten WARN-Targets: `./7w_wiki.py repair --fix-roamlinks --auto`
   - Fuer clusterbasierte Backlog-Arbeit zuerst `./7w_wiki.py repair --backlog-board --json`, dann konservative Mechanik mit `./7w_wiki.py repair --apply-lane1 --auto`
   - Diese Schritte behandeln Publishing- und Linkdrift, nicht Lore-Praezedenz.
   - Der normative Volltext steht in [SY_DRIFT_PAGES_CONTRACT.md](../../System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md).
5. **Index Live-Überwachung (`/watch`):**
   - Bei bedarf `./7w_wiki.py watch` in einem separaten Terminal starten, um inkrementelle Index-Updates (`build_index.py`) für das Oracle beim Speichern zu garantieren.

## 3. Diagnose & CI/CD (GitHub Pages)
Wenn du ein Problem (z.B. GitHub Pages Build Fail) untersuchst:
1. **Lokale Reproduktion:** Führe `./7w_wiki.py pages build --strict` aus.
   - Wenn das fehlschlägt, den Fehler lokal beheben.
2. **CI/CD Analyse:** Prüfe `.github/workflows/deploy.yml` auf Environment-Drifts.
   - Bundle-Releases laufen getrennt ueber `.github/workflows/release-bundles.yml` und haengen Assets an GitHub Releases statt an den Branch.
3. **Site-Integrität:** Führe `./7w_wiki.py pages validate --json --strict-links` aus, um nicht-allowlistete Roamlinks-Warnungen explizit zu sehen.
   - Wiki-Pages dabei niemals als hoechste Wahrheitsquelle gegen Homepage oder Quellen behandeln.
   - Die kanonische Drift-/Pages-Regel steht in [SY_DRIFT_PAGES_CONTRACT.md](../../System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md).
4. **Live Verification:** Nutze den Browser (`siebenwind.github.io/7w_wiki/`) um Frontend, CSS und JS zu validieren.

## 4. UX/CD Dokumentation (Pflicht bei UI-Eingriffen)
Wenn Landing, Navigation oder Corporate Design angepasst werden:
1. Dokumentiere den Eingriff in `CHANGELOG.md`.
2. Aktualisiere `docs/Archiv/REDESIGN_ROADMAP_2026.md`.
3. Poste einen Dispatch-Heartbeat (Status-Heartbeat) mit den Kernpunkten an das `/meta_master` Department.

## 5. Abschluss
- Mache präzise Code-Commits (z.B. `fix(ci):`, `chore(docs):`).
- Bei fachfremden Widersprüchen (Lore statt Technik): Formuliere eine Fachfrage via Dispatch an den Historiker oder Guardian.
- **Session-Memory (Pflicht):** Erstelle ein Session-Memory (`SESSION_MEMORY_YYYY-MM-DD_TECH.md`) und verlinke es per `mail post`.

#tech #maintenance #cicd #ops
