# Session Memory: Pages Fast And Backlog Triage

- Date: 2026-03-26
- Focus: Runtime-Telemetrie, sicherer `pages validate --fast`-Vorcheck und Vorarbeit fuer den systematischen Pages-/Bridge-Backlog-Abbau

## Context
- Drift-Praevention, Doku-Vertrag und Analyse-Caches waren bereits eingefuehrt, aber der naechste Ausbaupunkt fehlte noch:
  - `pages validate` war fuer Wiederholungslaufe noch zu intransparent.
  - `advisor` empfahl noch das unschaerfere `--strict` statt des harten Link-Gates.
  - der historische Pages-Backlog blieb gross, ohne saubere Cluster fuer die weitere Abarbeitung.
- User-Hinweis bleibt gueltig: Epistemische Praezedenz ist `Homepage > Quellen > Wiki Pages`. `docs/Siebenwind_Wiki/` ist der technische Edit- und Publish-Baum, nicht die hoechste Wahrheitsstufe.

## What Changed
- Fuehrte einen schnellen advisory Vorcheck ein:
  - `./7w_wiki.py pages validate --json --fast`
  - schneller Modus baut keine neue MkDocs-Site, schreibt keinen neuen Pages-Snapshot und nutzt bewusst nur gecachte Analysen plus den letzten Voll-Report als Fruehwarnung
  - der Output markiert das explizit ueber `mode: "fast"` und `advisory_only: true`
- Erweiterte `pages validate --json` und `audit --pages --json` um Timing-/Phasenfelder:
  - `validation_timing_ms`
  - `build.timing_ms`
  - `timings_ms` in Audit-JSON
- Haertete die Cache-Metadaten ab:
  - Cache-Outputs enthalten jetzt `hit`, `inputs_fingerprint`, `duration_ms`, `version` und `path`
  - relevante Inputs umfassen nun den Docs-Baum sowie Konfigurationsartefakte wie `mkdocs.yml` und `.agent/config/pages_link_policy.json`
- Trennte Read-only-Checks weiter von globalen Schreibpfaden:
  - kleine/scoped Contract-Checks und der schnelle Validate-Modus triggern keinen globalen Snapshot-/Inventar-Write
- Praezisierte die Runtime-Empfehlungen:
  - `advisor` verweist jetzt auf `./7w_wiki.py pages validate --json --strict-links`
  - nicht mehr auf das semantisch weichere `--strict`
- Normalisierte weitere Driftquellen in Contract- und Repair-Logik:
  - robustere Umlaut-/Alias-Normierung (`ä/ö/ü/ß`)
  - Legacy-Index-Wikilinks wie `[[03_Gesellschaft/index#...]]` werden auf kanonische Ziele gemappt
  - verschachtelte Quellenlinks und problematische Bote-Links werden aktiv in das Contract-Format ueberfuehrt
- Bereinigte einen unnötigen MkDocs-Warnpfad:
  - `mkdocs.yml` nutzt das `roamlinks` Plugin jetzt ohne die alte, nicht verstandene Option
- Dokumentierte den neuen Stand in:
  - `MASTER_TASK_LIST.md`
  - `CHANGELOG.md`
  - `.agent/workflows/tech_master.md`
  - `.agent/workflows/test_run.md`
  - `System/MCP/README.md`

## Verification
- `python3 -m py_compile 7w_wiki.py .agent/scripts/advisor.py .agent/scripts/content_contract.py .agent/scripts/pages_integrity.py .agent/scripts/pages_tool.py .agent/scripts/register_check.py .agent/scripts/repair.py`
- `./7w_wiki.py test --suite content-contract`
- `./7w_wiki.py test --suite split-brain-guard`
- `./7w_wiki.py test --suite takeover-handover`
- `./7w_wiki.py test --suite interop-doc-links`
- `./7w_wiki.py test --suite workflow-matrix-contract`
- `./7w_wiki.py test --suite tool-manifest-contract`
- `./7w_wiki.py test --suite codex-workflow-bridges`
- `./7w_wiki.py test --suite pages-link-contract`
- `./7w_wiki.py pages validate --json --skip-audit`
- `./7w_wiki.py pages validate --json --fast --skip-audit`
- `./7w_wiki.py audit --pages --json`
- `./7w_wiki.py advisor --json`

## Measured State
- Voller Pages-Validate-Lauf (`./7w_wiki.py pages validate --json --skip-audit`) ist erfolgreich, aber teuer:
  - `mode = full`
  - `advisory_only = false`
  - `build.exit_code = 0`
  - `pages_health.status = WARN`
  - `pages_health.drift_status = PASS`
  - `pages_health.unresolved_total = 774`
  - `pages_health.unallowlisted_total = 772`
  - `pages_health.last_validated_at = 2026-03-26T18:20:46Z`
  - `validation_timing_ms.total ~= 128848`
  - `build.timing_ms.mkdocs_build ~= 127450`
  - `other_warnings = 11` nach Bereinigung der Root-Doku-Archivlinks in `CHANGELOG.md` und `MASTER_TASK_LIST.md`
- Voller Audit-Lauf mit Pages-Integritaet (`./7w_wiki.py audit --pages --json`) ist ebenfalls gueltig, aber aehnlich teuer:
  - `issues_found = 1037`
  - `categories.site_integrity.issues = 785`
  - `categories.bridge_inventory.issues = 88`
  - `categories.contract_violations.issues = 75`
  - `timings_ms.total ~= 139264`
- Fazit: Der dominante Kostenblock ist weiterhin der echte MkDocs-Build. Die Analyse-Caches helfen, aber sie beseitigen nicht den Hauptanteil eines harten Voll-Gates.

## Backlog Clusters For Next Pass
- **Bridge Lifecycle**:
  - `88` invalide Bridge-Seiten, vor allem unter `docs/Siebenwind_Wiki/00_Fundament/`
  - naechster Schritt: entweder echte Zielreparatur oder saubere Lifecycle-Metadaten (`bridge_*`)
- **Alias-/Umlaut-Drift**:
  - haeufige Zielcluster: `Dämonen`, `Persönlichkeiten`, `En'Hor`, `Bürgerwehr`, `Fraomar_Arkad'Grembargh`
  - diese Targets brauchen lookup-basierte Zielangleichung statt ad-hoc Einzelfixes
- **Legacy Index / Kategorieziele**:
  - pseudo-indexartige Ziele wie `[[03_Gesellschaft/index#...]]` wurden im Contract normalisierbar gemacht, muessen aber weiterhin im Bestand konsequent ausgerollt werden
- **Bote-/Quellenpfade**:
  - der Quellenbaum mischt Unterstrich- und Leerzeichen-Dateinamen
  - `quelle:`-Felder und Bote-Referenzen sind dadurch weiter inkonsistent
  - naechster Technikschritt sollte lookup-basiert gegen reale `Quellen/`-Dateien mappen
- **Other warnings ausserhalb des Roamlink-Kerns**:
  - verbleibend sind vor allem veraltete relative Index-Links in `00_Fundament/index.md`, `01_Pantheon/*.md` und `03_Wissen/index.md`

## Notes / Risks
- `pages-link-contract` ist wieder gruen, nachdem die alte `roamlinks`-Konfigurationswarnung aus `mkdocs.yml` entfernt wurde.
- Ein frischer Voll-Validate-Lauf am Ende der Session hat den Pages-Snapshot aktualisiert; Fast-Reports haengen damit nicht mehr an dem alten Stand von `18:11:39Z`.
- Der schnelle Modus ist absichtlich nicht gate-faehig. Er dient nur zur Fruehwarnung zwischen den teuren Voll-Laufen.
- Die naechste groessere Verbesserung sollte nicht wieder nur Runtime-Arbeit sein. Der groesste Hebel liegt jetzt im clusterweisen Abbau der historischen Inhalts- und Linkschuld.
