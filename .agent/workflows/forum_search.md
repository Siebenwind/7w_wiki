---
layout: wiki_page
title: "Workflow: `/forum_search` (Forum-Quellenjagd)"
category: Workflow
description: Systematische Forum-Quellensuche fuer neue ingestierbare Quellen (/forum_search)
---

# Workflow: `/forum_search` (Forum-Quellenjagd)

## Interop-Status
- runtime_commands:
  - `7w_wiki.py scout --forum bekanntmachungen --pages 3`
  - `7w_wiki.py scout --forum news --pages 3`
  - `7w_wiki.py scout --forum geschichten --pages 5`
  - `7w_wiki.py mail post --from Scout --to Ingestor --subject "<source lead>" --body "<summary>"`
- method_only:
- matrix_status: executable
- runtime_adapter: `7w_wiki.py scout --forum <allowlisted-board> --pages N`
- interop_note: Spezialisierter Betriebsweg fuer forum-basierte Quellenjagd; der promoted Umbrella-Workflow `/scout` bleibt fuer breitere Discovery zustaendig.
- catalog_id: `workflow.forum_search`
- primary_command: `7w_wiki.py scout --forum bekanntmachungen --pages 3`
- followup_commands:
  - `7w_wiki.py scout --forum news --pages 3`
  - `7w_wiki.py scout --forum geschichten --pages 5`
  - `7w_wiki.py mail post --from Scout --to Ingestor --subject "<source lead>" --body "<summary>"`
- adapter_targets:
  - `codex:workflow_forum_search`
  - `mcp:prompt/forum_search`
- deprecated_aliases:

Dieser Workflow dient der gezielten Suche nach **neuen ingestierbaren Quellen** in den Legacy-Foren. Er ist enger gefasst als `/scout`: keine Homepage-Sichtung, kein allgemeines Web-Monitoring, sondern Board-fokussierte Quellenjagd.

## 1. Gültige Boards

Aktuell sind nur diese Scopes freigegeben:
- `bekanntmachungen`
- `news`
- `geschichten`

Standard: Scanne zuerst `bekanntmachungen`, danach bei Bedarf `news` oder `geschichten`.
Standard-Tiefe: `--pages 3`, fuer Geschichten-Boards `--pages 5`

## 2. Suchdurchlauf

1. Führe `./7w_wiki.py scout --forum bekanntmachungen --pages 3` aus.
2. Prüfe die gelisteten Titel/Topic-IDs gegen bestehende Quellen unter:
   - `Quellen/Forum/Bekanntmachungen/`
   - `Quellen/Forum/Newsticker/`
   - `docs/Quellen/Forum/Geschichten_aus_dem_Spiel/`
3. Wiederhole den Lauf bei Bedarf für `news` oder `geschichten`.
4. Markiere einen Treffer nur dann als **neuen Quellenkandidaten**, wenn:
   - kein gleichwertiger Quelldatensatz bereits in `Quellen/Forum/...` vorhanden ist,
   - der Titel nicht nur ein Dublett mit leicht abweichender Schreibweise ist,
   - der Fund inhaltlich über bloße UI-/Forenrauschsignale hinausgeht.
5. Geschichten-Funde werden zunaechst nur als forumnahe Rohquelle archiviert; keine direkte Voll-Ingestion im Scout-Schritt.
6. Route nur dann an Historian oder Mensch weiter, wenn Eskalationskriterien greifen:
   - groessere fachliche Unklarheit
   - fehlende Zweitstuetze fuer starke Behauptungen
   - Quellenwiderspruch oder Kanonkorrektur
   - konkurrierende belastbare Lesarten

## 3. Hand-off und Routing

Wenn neue Quellenkandidaten gefunden wurden:
1. Fasse Board, Topic-ID, Titel und Relevanz in einem kurzen Dispatch zusammen.
2. Sende `./7w_wiki.py mail post --from Scout --to Ingestor --subject "<source lead>" --body "<summary>"`.
3. Wenn der Fund operativ nicht sauber loesbar ist, route question-first an Historian; nur echte Kontroversen gehen weiter an den Menschen.

## 4. Wann stattdessen `/scout`?

Route zu `/scout`, wenn die Aufgabe breiter ist als Forum-Quellensuche:
- Homepage-/News-Sichtung
- Nicht-Forum-Webquellen
- Allgemeine externe Reconnaissance

## 5. Abschluss

- Keine Interaktion mit dem Forum, nur passive Sichtung.
- Keine Quelle direkt als integriert behandeln; `/forum_search` produziert Leads, nicht fertige Ingests.
- Bei verdächtigen Doppeln erst Dispatch-Frage, dann Ingestion.

#forum #discovery #quellen #scout
