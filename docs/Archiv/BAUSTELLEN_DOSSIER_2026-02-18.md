# Baustellen-Dossier 2026-02-18

## Zweck

Dieses Dossier listet die **nicht-bannerbezogenen** offenen Baustellen, priorisiert nach Betriebsrisiko und mit aktueller Evidenz.

## Status-Snapshot (2026-02-18, 00:07 CET)

- Advisor: `P1 6 | P2 3 | P3 2 | Backlog 3`
- Dispatch-Queue: `OPEN 20 | CLAIMED 1 | DONE 0`
- Audit: `373 Probleme` (`Logs/Archive/Audit_6002f680-cfe3-4f7d-be64-e5432b0edd11.txt`)
- Testlage:
  - PASS: `interop-doc-links` (`Logs/Archive/TEST_interop-doc-links_2026-02-18_000035.md`)
  - PASS: `clean-client-state` (`Logs/Archive/TEST_clean-client-state_2026-02-18_000508.md`)
  - FAIL: `takeover-handover` (`Logs/Archive/TEST_takeover-handover_2026-02-18_000242.md`)
  - FAIL: `rag-relevance-smoke` (`Logs/Archive/TEST_rag-relevance-smoke_2026-02-18_000738.md`)

## Akute Baustellen (P1)

### 1) Audit-/Link-Integritaet bleibt Gate-Blocker

- **Symptom:** `takeover-handover` faellt weiterhin auf `audit-readiness`.
- **Evidenz:** `Logs/Archive/TEST_takeover-handover_2026-02-18_000242.md`
- **Technischer Kern:** Deep WikiLink Check ist noch breit rot; aktuell 373 offene Missing-File-Faelle.
- **Naechster Schritt:** Link-Flood weiter triagieren (`./7w_wiki.py repair`) und dabei in Batches dokumentieren.

### 2) Oracle-Zuverlaessigkeit / Retrieval-Qualitaet

- **Symptom:** `rag-relevance-smoke` faellt reproduzierbar (3/4 Checks FAIL).
- **Evidenz:** `Logs/Archive/TEST_rag-relevance-smoke_2026-02-18_000738.md`
- **Konkrete Fehlbilder:** 
  - `Dunvallo_Linari.md` wird nicht als Top-Treffer geliefert.
  - `Matrixtheorie_Linari.md` wird nicht geliefert.
  - `Reagenzien_Lehre.md` wird nicht geliefert.
- **Governance-Bezug:** Offener Auftrag `MSG-2026-0015`.
- **Naechster Schritt:** Reproduzierbaren Testplan + Root-Cause + Fix/Fallback gem. Dispatch abarbeiten.

### 3) Test-Harness-Stabilitaet und Erwartungsabgleich

- **Symptom:** P1-Tasktext nennt haengende Laeufe; aktueller Stand zeigt zwar Abschlussreport, aber weiterhin fachlich FAIL.
- **Evidenz:** `MASTER_TASK_LIST.md` (P1 "Test Runner Stability") vs. aktueller Report `Logs/Archive/TEST_rag-relevance-smoke_2026-02-18_000738.md`
- **Naechster Schritt:** Tasktext praezisieren (Hang vs. Relevanz-Fail klar trennen), dann Test-Fix zielgerichtet fahren.

### 4) Ingestion 2.0 mit harter Blockade

- **Symptom:** Weiterfuehrung ist blockiert.
- **Evidenz:** `MASTER_TASK_LIST.md` P1-Eintrag "Ingestion 2.0" mit `[BLOCKED: 118 Source Missing]`.
- **Naechster Schritt:** Source-Beschaffung/Recovery fuer Bote 118 oder formale Depriorisierung mit Board-Entscheid.

## Operative Baustellen (P2/P3/Backlog)

### P2 (operativ)

- **Kanon-Abgleich Goetterverschmelzung** (`RESEARCH-2026-010/011`) - Status `DEFERRED`.
- **Massen-Ingestion verbleibender Quellen** - Status `Pending`.
- **Lore Research Board** (u. a. Angamon, Oedland) - offen.

### P3 (Qualitaet/Politur)

- **Chronik-Konsolidierung** mit `Zeitrechnung_(Der_Sonnenzirkel).md`.
- **Feature "Der Kartograph"** (geografische Skill-Erweiterung).

### Backlog (Strategisch)

- **Skill "Der Herold"** (automatisches News-Broadcasting).
- **Workflow `/map_sync`**.
- **Workflow `/cleanup`**.

## Meta-Baustelle: Dispatch-Hygiene

- In der OPEN-Queue liegen historische FAIL-Meldungen, die teils durch neuere Runs ueberholt sind (z. B. Interop inzwischen PASS).
- Empfehlung: Alte, ueberholte Statusmeldungen sammeln, in Sammelnotiz verdichten und als DONE/ersetzt markieren, um Fokus auf echte Blocker zu halten.

## Priorisierte Reihenfolge (ab jetzt)

1. Oracle-Zuverlaessigkeit (`MSG-2026-0015`) mit reproduzierbarem Nachweis stabilisieren.
2. Audit-Linkflood weiter reduzieren, bis `audit-readiness` kein Gate-Fehler mehr ist.
3. Ingestion-Blockade (Bote 118) formal aufloesen: Quelle liefern oder Task umpriorisieren.
4. Erst danach P2-Forschung und P3-Politur hochziehen.

