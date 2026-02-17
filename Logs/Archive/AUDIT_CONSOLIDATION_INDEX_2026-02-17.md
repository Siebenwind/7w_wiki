---
uuid: 5b883361-6fbe-4183-b3fc-2ac8fa897925
status: ACTIVE
created_at: 2026-02-17T22:48:00Z
epistemic: "#meta"
---

# Audit Consolidation Index (2026-02-17)

Ziel: Redundante Audit-/Test-Artefakte in `Logs/Archive` konsolidierbar machen, ohne Verlaufsdaten zu verlieren.

## Bestand

- Audit-Rohreports (`Audit_*.txt`): 275
- Test-Reports (`TEST_*.md`): 87
- Audit-Hash-Cluster (normalisiert, `Report-ID` ignoriert): 21
- Test-Hash-Cluster (normalisiert, dynamische Metadaten ignoriert): 6

## Merge-Strategie (empfohlen)

1. Pro Hash-Cluster genau **eine** Canonical-Datei behalten (neueste im Cluster).
2. Alle weiteren Cluster-Mitglieder als `superseded` im Archivregister markieren (nicht löschen).
3. Für Tests: je Suite/Zustand nur letzte Wiederholung als Canonical.
4. Tages-/Meilensteinberichte (`Audit_Report_YYYY-MM-DD.md`) als narrative Artefakte beibehalten.

## Audit-Cluster (Top 10)

| Gruppe | Duplikate | Canonical | Beispiel (früh) | Empfehlung |
|---|---:|---|---|---|
| A1 | 147 | `Audit_fd424536-4657-4dd0-a124-fc7dc8683225.txt` | `Audit_000d5e17-c66b-4393-8d13-b010185b97b7.txt` | Massencluster, auf 1 Canonical reduzieren |
| A2 | 18 | `Audit_e79cceb0-3f2b-4287-a652-6b0bd333b4c0.txt` | `Audit_01056f07-0b80-4da8-b3eb-0d1e4e2ea2f7.txt` | Wiederholte gleichartige Audits |
| A3 | 13 | `Audit_fcc6f1c2-1945-4d64-8621-747804cf12a7.txt` | `Audit_111346ec-3f38-4a0d-b7a0-098d2b81a290.txt` | Wiederholte Kurzläufe |
| A4 | 8 | `Audit_fc1242af-447b-4ad9-bdf4-66362de3b5e0.txt` | `Audit_18b6bcae-5f86-4ae2-accf-7b92f03ae6ea.txt` | Ein Cluster genügt |
| A5 | 6 | `Audit_c6f58e86-50f6-438d-8020-912fc88ef14e.txt` | `Audit_00611260-9c28-4eaa-af82-0020e6fa2ace.txt` | Konsolidieren |
| A6 | 6 | `Audit_ced302b8-2a7c-46c1-b5fd-c0052b79e23f.txt` | `Audit_44812545-34aa-452e-bb9a-bdcfb2bb1323.txt` | Konsolidieren |
| A7 | 6 | `Audit_d0ec1205-8312-4531-9c5b-c66636b272bb.txt` | `Audit_012c705a-dded-408c-be21-145bd0f9ff11.txt` | Konsolidieren |
| A8 | 5 | `Audit_b490e8f1-31e0-4992-88b5-25c689175d96.txt` | `Audit_22d5fbc3-f504-4563-a90d-4ce3b33fa8f1.txt` | Konsolidieren |
| A9 | 5 | `Audit_d322ddab-5ff0-47fd-bc0c-b910c4b95a50.txt` | `Audit_4f661674-ee08-486e-b35a-38068c9df420.txt` | Konsolidieren |
| A10 | 3 | `Audit_ad552ed1-7986-4bae-836b-4d83757a9489.txt` | `Audit_61b21a3f-29a3-4fba-9c09-b8eddd7d6470.txt` | Konsolidieren |

## Test-Cluster (identische Wiederholungen)

| Gruppe | Duplikate | Canonical | Empfehlung |
|---|---:|---|---|
| T1 | 8 | `TEST_interop-doc-links_2026-02-17_180351.md` | ältere identische FAIL-Läufe zusammenführen |
| T2 | 8 | `TEST_interop-doc-links_2026-02-17_223752.md` | identische PASS-Läufe auf Canonical reduzieren |
| T3 | 6 | `TEST_interop-doc-links_2026-02-17_222514.md` | identische FAIL-Läufe reduzieren |
| T4 | 5 | `TEST_clean-client-state_2026-02-16_223157.md` | identische PASS-Läufe reduzieren |
| T5 | 5 | `TEST_interop-doc-links_2026-02-16_222658.md` | identische FAIL-Läufe reduzieren |
| T6 | 4 | `TEST_takeover-handover_2026-02-16_222658.md` | identische PASS-Läufe reduzieren |

## Backlinks (gesetzt)

- Task/Plan-Backlink:
  - `MASTER_TASK_LIST.md` (P1 Audit Regression Triage) -> diese Konsolidierungsakte.
- Changelog-Backlink:
  - `CHANGELOG.md` (2026-02-17.08 / Validiert) -> diese Konsolidierungsakte.
- Session-Memory-Backlink:
  - `Logs/Archive/SESSION_MEMORY_2026-02-17_TECH_TRACKING.md` (offene Punkte) -> diese Konsolidierungsakte.

## Referenzanalyse: Skills / Workflows / Agenten

Direkte Verweise auf **konkrete** redundante Dateien (`Audit_<UUID>.txt`, `TEST_<suite>_<timestamp>.md`) wurden geprüft.

- Skills (`.agent/skills`, `.agents/skills`): keine direkten File-IDs gefunden.
- Workflows (`.agent/workflows`): keine direkten File-IDs gefunden.
- Persona-Instruktionen (`.agent/instructions`): keine direkten File-IDs gefunden.

Direkte Verweise existieren derzeit in:

- `MASTER_TASK_LIST.md` (spezifischer Audit-Report)
- `CHANGELOG.md` (spezifische Test-/Audit-Reports)
- Dispatch-Messages unter `System/Synapse_Board/DISPATCH/` (spezifische Test-Report-Pfade)

## Nächster Schritt

- Optionalen `archive consolidate`-Befehl in `7w_wiki.py` ergänzen:
  - generiert diese Indexdatei,
  - markiert Superseded-Dateien im Register,
  - erzeugt pro Cluster eine kurze Metadatei `Cluster_<ID>.md`.
