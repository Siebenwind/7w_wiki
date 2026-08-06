---
uuid: 0a1e2d3c-4b5a-4c6d-8e7f-102030405060
status: ACTIVE
owners:
  - Koordinator
  - Netz-Waechter
epistemic: "#meta"
---

# SY_DRIFT_PAGES_CONTRACT

Kanonischer Vertrag fuer Drift-Praevention, Pages-Integritaet und epistemische Praezedenz.

## Geltungsbereich

1. Epistemische Praezedenz ist verbindlich: `Homepage > Quellen > Wiki Pages`.
2. `docs/Siebenwind_Wiki/` ist der technische Edit- und Publishing-Baum fuer Wiki-Pages, aber nicht die hoechste Wahrheitsebene.
3. Das Wurzelverzeichnis `Siebenwind_Wiki/` ist retired; seine Wiederkehr ist ein technischer Defect, kein normaler Betriebszustand.

## Content-Contract

1. Aktive Writer duerfen kein Legacy-`layout:` mehr erzeugen.
2. Inline-Metadaten direkt nach dem H1 werden in den kanonischen `!!! info "Metadaten"`-Block ueberfuehrt.
3. Stubs bleiben nur mit Lifecycle-Feldern gueltig.
4. Temporaere Bridges sind nur mit `bridge_mode`, `bridge_target`, `bridge_ticket` und `bridge_review_until` zulaessig.
5. Neue oder reparierte Inhalte werden gegen den kanonischen Edit-Baum und nicht gegen alte Schattenbaeume bewertet.

## Pages-Integritaet

1. `./7w_wiki.py pages validate --json` ist die kanonische Site-Integritaetsprobe.
2. `./7w_wiki.py pages validate --json --strict-links` ist der harte Gate-Modus fuer nicht-allowlistete Targets.
3. `./7w_wiki.py pages validate --contract --json` ist der deterministische Contract-/CI-Modus ohne MkDocs-Build und ohne Snapshot-Schreibseitenwirkungen.
4. `./7w_wiki.py audit --pages` spiegelt denselben Site-Zustand im Audit.
5. `./7w_wiki.py repair --fix-roamlinks --auto` ist der begrenzte Reparaturpfad fuer hohe Trefferwahrscheinlichkeit.
6. Pages-Warnungen pruefen technischen Publishing-Drift; sie entscheiden keine Lore-Wahrheit gegen Homepage oder Quellen.
7. Der in `.agent/config/pages_link_policy.json` gefuehrte Ratchet ist eine Obergrenze: Ein Commit darf `unresolved_total` oder `unallowlisted_total` nicht ueber den zuletzt akzeptierten Altbestand anheben. Verringerungen werden zur neuen Zielrichtung, nicht durch neue Links wieder aufgefuellt.
8. Policy-Ausnahmen benoetigen ein gueltiges `review_until`; abgelaufene oder unlesbare Fristen machen die Pages-Pruefung rot.
9. Die lesbare Statistikseite muss Artikelzahl und Ingestion-Gesamtstand des aktuellen Publishing-Baums wiedergeben. Bei Abweichung ist `./7w_wiki.py stats` auszufuehren, bevor Pages gebaut werden.
10. `docs/index.md` enthaelt einen generierten Aktivitaetsblock. Derselbe Statistiklauf synchronisiert dort den juengsten abgeschlossenen Historikerlauf aus `CHANGELOG.md`.

## Traceability

1. Maschinenlesbare Zustandsdaten leben in `.agent/data/wiki_inventory.json` und `.agent/data/pages_health.json`.
2. Kontrollsummen, Timestamps und Klassifikationen sind Inventar-/Snapshot-Daten, keine Lore-Inhalte.
3. Read-only-Pruefungen sollen keine globalen Schreib-Side-Effects erzeugen.
4. GitHub Pages baut nur nach erfolgreichem `./7w_wiki.py pages validate --json --skip-audit`; ein blosser MkDocs-Bau ist kein ausreichender Freigabenachweis.

## Sync- und Doku-Regeln

1. Generierte Kommando- und Adapterlisten werden von `./7w_wiki.py tech --sync-*` gepflegt.
2. Manuelle Doku-Bloecke bleiben manuell und verweisen auf diesen Vertrag statt dieselben Regeln erneut auszuschreiben.
3. Wenn ein Text die volle Drift- oder Pages-Regel nicht selbst tragen muss, soll er nur auf diesen Vertrag referenzieren.

## Hinweise

- Generiert sind die Runtime-Kommandolisten und Adaptertabellen in `AGENTS.md`, `SY_INTEROP.md` und `SY_WORKFLOW_CLI_MATRIX.md`.
- Manuell sind die policy-tragenden Abschnitte in diesem Dokument, den Workflows und der Operations-Doku.
- Dieser Vertrag ist die kanonische Referenz fuer alle weiteren Doku-Konsolidierungen.
