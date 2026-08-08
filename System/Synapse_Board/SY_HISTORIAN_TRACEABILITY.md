---
uuid: ff785c14-880c-4b2b-b674-c561e04a9ac7
status: ACTIVE
updated_at: 2026-08-05T12:55:00Z
owners:
  - Historiker
  - Koordinator
  - Netz-Waechter
epistemic: "#meta"
---

# SY_HISTORIAN_TRACEABILITY

Zweck: Historikerfaehige Rueckverfolgbarkeit fuer Status, letzte Durchsicht, Ingestion-Stand und agentenbezogene Bearbeitung.

## Zielbild

Ein `status`-Lauf soll nicht nur technische Zahlen liefern, sondern auch:

1. Letzte fachliche Durchsicht je Artefakt.
2. Ingestion-Status entlang der Quelle -> Wiki-Kette.
3. Wer hat wann relevant eingegriffen (Agent + Evidenz).
4. Welche Aussage ist gesichert, welche ist nur Indiz.

## Historiker-Fragen (Pflicht)

Fuer jede relevante Datei/Entitaet muessen diese Fragen beantwortbar sein:

1. Wann wurde sie zuletzt geaendert?
2. Durch wen (technisch) und durch welchen Agenten (operativ)?
3. War die letzte Aenderung Ingestion, Review, Konfliktloesung oder kosmetisch?
4. Wann war die letzte qualifizierte Durchsicht?
5. In welchem Board-/Dispatch-Kontext geschah die Aenderung?

## Datenquellen (Standardloesung, interoperabel)

Nur bestehende Artefakte verwenden, keine Parallelwahrheiten:

- Git-Historie (Commit-Zeit, Author, Diff-Pfade)
- Dispatch (`System/Synapse_Board/DISPATCH/MSG-*.md`)
- Research/Conflict/Inquisition-Boards (`System/Synapse_Board/`)
- Test- und Audit-Reports (`Logs/Archive/`)
- Ingestion-Inventur und Ingestion-Reports (`Logs/INVENTUR_QUELLEN.md`, `Logs/Ingestion/`)
- Archivregister (`System/Archivregister/ARCHIVREGISTER.json`)

## Message- und Board-Faehigkeiten (Historiker-Sicht)

| Domain | Struktur | Kann beantworten | Grenzen |
|---|---|---|---|
| Dispatch | `id`, `uuid`, `status`, `from_agent`, `to_agent`, Zeitstempel | Auftrag, Claim, Abschluss, Verantwortlichkeit | Kein Dateidiff |
| Research | Ticketstatus (`OPEN_HISTORIAN`...`RESOLVED`, `THEMATIC_BACKLOG`) + Fachkontext | Historian-Lage, Prioritaet, Ergebnispfad | Kein commit-genauer Touch |
| Conflict | Konfliktstatus + Historiker-Opinion | warum eine Korrektur erfolgte | technische Aenderung nur indirekt |
| Inquisition | Forschungs-/Theorieakte | Hypothesenstand, Abschlussgrad | nicht automatisch kanonisch |
| Audit/Test Reports | pass/fail + Zeitpunkt | Systemgesundheit je Lauf | kein semantischer Inhaltsentscheid |

## Normiertes Historiker-Datenmodell

Pro Entitaet (Datei oder Lore-Objekt) werden folgende Felder gefuehrt:

- `entity_uuid`: stabile ID (aus Frontmatter oder Register)
- `relative_path`
- `domain`: `wiki|quellen|system|docs`
- `ingestion_status`: `PENDING|IN_PROGRESS|DONE|REVIEW_REQUIRED|UNKNOWN`
- `last_ingestion_at`
- `last_ingestion_agent`
- `last_review_at`
- `last_review_agent`
- `last_review_ref` (Dispatch-/Ticket-/Report-Link)
- `last_touch_at` (git)
- `last_touch_actor` (git author)
- `last_touch_agent` (abgeleitet aus Dispatch/Report/Commit-Konvention)
- `touch_relevance`: `LOW|MEDIUM|HIGH`
- `confidence`: `0.0..1.0`
- `evidence_refs`: Liste repo-relativer Evidenzen

## Ableitungsregeln (wichtig fuer Rueckschluesse)

1. `last_touch_*` kommt primaer aus Git.
2. `last_review_*` kommt primaer aus Review-/Dispatch-/Conflict-Artefakten.
3. `last_ingestion_*` kommt primaer aus Ingestion-Reports und Inventurstatus.
4. `last_touch_agent` darf nur gesetzt werden, wenn mindestens eine Evidenz vorliegt:
   - Claim/Done in Dispatch mit Bezug zur Entitaet, oder
   - Ingestion-/Test-/Audit-Report mit Agentenangabe und Dateireferenz.
5. Ohne belastbare Evidenz: Agentenfeld leer lassen und `confidence` absenken.

## Status-Ausgabe fuer Historiker

Der Status soll aus zwei Perspektiven kommen:

1. Systemweit:
   - Coverage, UUID-Luecken, stale Index
   - Board-Lage (Dispatch/Research/Conflict/Inquisition)
   - Ingestion-Fortschritt (processed/pending)
2. Entitaetsfokussiert:
   - Letzte Durchsicht, letzter relevanter Eingriff, Evidenzkette
   - Delta seit letzter Durchsicht (welche Dateien seitdem veraendert wurden)

## Abschlussrueckmeldung fuer Historiker-Durchlaeufe

Jeder Historiker-Durchlauf endet mit einer nutzergerichteten Zusammenfassung nach `System/Templates/HISTORIAN_CLOSEOUT_TEMPLATE.md`. Zwei klar getrennte Abschnitte sind verbindlich:

1. `Implementierte Neuerungen`: Was wurde angelegt, erweitert, korrigiert oder entfernt, und welchen inhaltlichen Nutzen hat dies fuer das Wiki?
2. `Erkenntnisgewinn`: Welche historischen oder lorebezogenen Einsichten kamen hinzu, welche Annahmen wurden korrigiert oder differenziert, und welche Unsicherheiten bleiben offen?

Reine Mengen- oder Dateilisten genuegen nicht. Falls keine Implementierung oder kein Erkenntnisgewinn entstand, muss der jeweilige Pflichtabschnitt dies nachvollziehbar begruenden. Offene Punkte, Pruefstatus, Dispatch-Abschluss und Session-Memory sind zulaessige Ergaenzungen, aber kein Ersatz.

## Geplante Artefakte

1. `System/Archivregister/HISTORIAN_LEDGER.json`
   - Vollstaendige strukturierte Historiker-Metadaten pro Entitaet.
2. `System/Archivregister/HISTORIAN_STATUS.md`
   - Lesbare Zusammenfassung mit Top-Risiken und offenen Durchsichten.

Hinweis: Beide Artefakte werden im gleichen Lauf erzeugt wie `index --status`, um Drift zu vermeiden.

## Interop- und Kompatibilitaetsregeln

1. Runtime bleibt `./7w_wiki.py`.
2. Keine proprietaeren Board-Formate; bestehende Frontmatter-Felder weiterverwenden.
3. Keine Sonderpfade; nur repo-relative Referenzen.
4. Kompatibel mit Antigravity/Jules/Codex durch dokumentierte, standardisierte Felder.

## Umsetzungsphasen

1. Phase 1 (MVP)
   - Historikerfelder als Ableitung im Statuslauf erzeugen.
   - Fehlende Evidenzen sichtbar markieren.
2. Phase 2
   - Relevanzklassifikation (`LOW|MEDIUM|HIGH`) auf Basis Eventtyp.
   - Delta-Ansicht seit letzter Durchsicht.
3. Phase 3
   - Historiker-Query-Ansicht (z. B. "zeige alles ohne qualifizierte Durchsicht > 90 Tage").

## Testkonzept

Neue Suite: `historian-traceability-smoke`

- Case 1: Statuslauf erzeugt `HISTORIAN_LEDGER.json` und `HISTORIAN_STATUS.md`.
- Case 2: Mindestens ein Dispatch-Eintrag wird korrekt als Evidenz referenziert.
- Case 3: Mindestens ein Ingestion-Report wird korrekt in `last_ingestion_*` gespiegelt.
- Case 4: Bei fehlender Evidenz bleibt `last_touch_agent` leer (kein Raten).

## Entscheidungskriterium (Done)

Das Konzept gilt als umgesetzt, wenn ein Historiker fuer eine beliebige Datei in einem Lauf beantworten kann:

1. letzter relevanter Agenteneingriff,
2. letzte qualifizierte Durchsicht,
3. aktueller Ingestion-Status,
4. belastbare Evidenzpfade fuer alle Aussagen.
