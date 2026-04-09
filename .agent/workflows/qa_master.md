---
description: Universeller Master Workflow für Konsistenz, Links und Qualitätssicherung
---

# Department: 🔍 Die Inquisition (/qa_master)

Dieses Department überwacht die Integrität des Wikis, bannt "Link-Dämonen" und bewertet Community-Beiträge. Es vereint die Prozesse für Auditierung, interaktive Reparatur und Beitragsprüfung.

<!-- BEGIN GENERATED DRIFT CONTRACT REFERENCE -->
> Generated reference block. The surrounding narrative text remains manually maintained.
> Canonical contract: [SY_DRIFT_PAGES_CONTRACT.md](../../System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md)
>
> - Epistemic precedence: `Homepage > Quellen > Wiki Pages`.
> - `docs/Siebenwind_Wiki/` is the technical edit/publish tree, not the highest truth source.
> - Technical drift is validated via `./7w_wiki.py sanitize`, `./7w_wiki.py audit`, and `./7w_wiki.py pages validate --json [--strict-links]`.
> - Deterministic contract/CI checks use `./7w_wiki.py pages validate --contract --json`.
> - `--strict` hardens the MkDocs build; `--strict-links` is the hard unresolved-link gate.
> - Generated command registries are synced by `./7w_wiki.py tech --sync-docs` / `--sync-interop`; narrative rules live in the canonical contract.
<!-- END GENERATED DRIFT CONTRACT REFERENCE -->

## Interop-Status
- runtime_commands:
  - `7w_wiki.py audit`
  - `7w_wiki.py audit --pages`
  - `7w_wiki.py repair [--full]`
  - `7w_wiki.py repair --fix-roamlinks [--auto] [--dry-run]`
  - `7w_wiki.py sanitize --auto`
  - `7w_wiki.py test --suite clean-client-state`
  - `7w_wiki.py test --suite pages-contract-mode-contract`
  - `7w_wiki.py test --suite root-tree-retirement-contract`
  - `7w_wiki.py stats`
  - `7w_wiki.py mail inbox --status OPEN`
  - `7w_wiki.py mail post --from Guardian --to <agent|ALL> --subject "<text>" --body "<text>"`
- method_only:
  - `/qa_master`

## 1. Überwachung & Audit-Zyklus
Das Audit ist der Ausgangspunkt der QA.
Der normative Drift-/Pages-Volltext steht in [SY_DRIFT_PAGES_CONTRACT.md](../../System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md).
// turbo
1. Führe das globale Audit aus:
   ```bash
   ./7w_wiki.py audit
   ```
   Wenn das Problem auf der Webseite sichtbar ist, immer zusätzlich:
   ```bash
   ./7w_wiki.py audit --pages
   ```
2. Analysiere die Ausgabe. Identifiziere:
   - Duplikate im Register.
   - Verwaiste Profile (Datei da, aber nicht im Register).
   - Registrierte Personen ohne Profildatei (Missing Files).
   - Technischen Drift (Layout, Split-Brain, Frontmatter, Pages).
   - Epistemischen Drift (Homepage/Quellen widersprechen Wiki-Pages).
3. Öffne `Logs/Konsistenzbericht_2026.md` und `/System/Synapse_Board/` für offene QA/Conflict-Tickets.

## 2. Die Reparatur (Repair Loop)
Nutze die automatisierten Tools anstatt manuell Dateien zu patchen.

### A. Automatisierte Reparatur
// turbo
Führe das Reparaturprogramm aus:
```bash
./7w_wiki.py repair
```
Nutze im Menü:
- `1` für fehlendes Frontmatter
- `2` für defekte Links (tote Verweise identifizieren)
- `3` für Casing, Redirects und Formatierungsfehler (Smart Link Repair)
*(Hinweis: `./7w_wiki.py repair --full` macht dies non-interaktiv).*

### B. Manuelle Register-Deduplizierung
Wenn `audit` redundante Registereinträge findet:
1. Identifiziere die Zeilen-IDs (z.B. im `Personenregister.md`).
2. Führe die Historien der zwei Einträge clever zusammen.
3. Lösche den redundanten Eintrag.

### C. Resolution: Verwaiste Links & Bridge-Hygiene
Wenn ein Link auf eine nicht (mehr) existierende Seite zeigt:
1. **Alias-Check [PFLICHT]:** Prüfe mit `./7w_wiki.py search "<Name>" --source wiki` ob die Seite nur umbenannt wurde. Wenn ja, repariere den Link.
2. **Brücken-Verbot:** Erstelle NIEMALS sinnlose "Stub"- oder "Placeholder"-Artikel nur um einen Link zu reparieren. Formulierungen wie "Brückenartikel zur Stabilisierung" sind ein Defect.
3. **Erlaubte Ausnahme:** Wenn ein Link temporär geblockt werden muss, darf die Seite ausnahmsweise angelegt werden, MUSS aber folgende Metadaten im Frontmatter tragen:
   - `bridge_mode: temporary`
   - `bridge_target: [[Kanonisches_Ziel]]`
   - `bridge_ticket: MSG-YYYY-NNNN`
   - `bridge_review_until: YYYY-MM-DD`
4. **Pages-/Roamlinks-Reparatur:** Wenn Links im publizierten `docs/` Build brechen, nutze `./7w_wiki.py repair --fix-roamlinks --auto` fuer aggressive, aber begrenzte Korrekturen auf exakte/casing/alias/high-confidence Single-Candidate Matches.
   Repariere dabei keine Fakten stillschweigend gegen Homepage oder Quellen.

## 3. Community Review (Contrib Audit)
Wenn User oder externe Systeme Inhalte einreichen (z.B. PRs):
1. **Frontend-Check:**
   - Korrektes YAML-Frontmatter? Keine absoluten Pfade (`file:///`)?
2. **Lore-Check (Faktencheck):**
   - Prüfe Fakten in dieser Reihenfolge: Homepage, Quellen, bestehende Wiki-Pages. Nutze bei Zweifeln eine Dispatch-Frage an den `/lore_master`.
3. **Integration:** 
   - Bei Annahme ausführen: `./7w_wiki.py sanitize --auto` und `./7w_wiki.py archive sync`.
   - Verweise bei Bedarf auf [SY_DRIFT_PAGES_CONTRACT.md](../../System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md) statt die Regeln erneut auszuschreiben.

## 4. Abschluss & Dokumentation
1. Führe `./7w_wiki.py audit` erneut aus. Ziel: `✅ Keine Duplikate`, `✅ Alle Profile registriert`.
2. Führe `./7w_wiki.py test --suite bridge-placeholder-guard` aus.
3. Führe `./7w_wiki.py test --suite pages-contract-mode-contract` aus.
4. Pruefe bei Pages-/Navigationsaenderungen optional `./7w_wiki.py test --suite pages-full-smoke`.
5. Führe `./7w_wiki.py stats` aus, um die Dashboard-Metriken zu erneuern.
6. Mache einen präzisen Git-Commit (z.B. `fix(lore): resolved 5 orphan links and deductive deduplication`).
7. Schließe offene QA-Tickets via Dispatch (`mail done`).
