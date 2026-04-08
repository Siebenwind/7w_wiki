---
layout: wiki_page
title: "Department: 📜 Rüstkammer der Geschichte (/lore_master)"
category: Workflow
description: Department Master Workflow für Lore-Forschung, Narrative und Kanon-Updates
---

# Department: 📜 Rüstkammer der Geschichte (/lore_master)

Dieses Department ist zuständig für tiefgreifende Lore-Analysen, den Umgang mit Kanon-Widersprüchen, die Beantwortung von Benutzerfragen (Oracle) und die literarische Aufwertung von Wiki-Artikeln ("Roman-Qualität"). 
Es fusioniert die klassischen Workflows `/historian`, `/researcher`, `/narrative_enrichment`, `/ask` und `/canon_update`.

## Interop-Status
- runtime_commands:
  - `7w_wiki.py search <query> --source wiki|quellen|all`
  - `7w_wiki.py historian <query>`
  - `7w_wiki.py score <file>`
  - `7w_wiki.py mail inbox --status OPEN`
  - `7w_wiki.py mail post --from Historian --to <agent|ALL> --subject "<text>" --body "<text>"`
- method_only:
  - `/lore_master`

## 1. Lore-Auskunft (Das Orakel / ask)
Wenn du eine konkrete Lore-Frage beantworten oder Fakten prüfen musst:
1. **Stufe 1 (Wiki-Check):** Was gilt als verarbeiteter Kanon?
   `./7w_wiki.py search "Frage" --source wiki`
2. **Stufe 2 (Quellen-Check):** Was sagen die unstrukturierten Rohdaten?
   `./7w_wiki.py search "Frage" --source quellen`
3. **Stufe 3 (Delta-Check):** Konsolidierter Gesamtabgleich.
   `./7w_wiki.py search "Frage" --source all`
*Hinweis: Identifizierte Inkonsistenzen müssen als `[KONFLIKT]` oder `[GAP]` im `Konsistenzbericht_2026.md` vermerkt werden.*

## 2. Kanon-Updates & Widerspruchs-Lösung (Historian & Canon Update)
Wenn offizielle `#canon` Hintergrund-Dokumente verarbeitet oder alte Widersprüche gelöst werden müssen:
1. **Quellen-Aggregation:** Führe eine holistische Suche über alle Layer aus.
2. **Bestandsabgleich (Kanon-Upgrade):** 
   - Kanon gewinnt **immer**. 
   - Falls bestehende Wiki-Artikel auf niedrigeren Epistemiken (`#bote`, `#perspektive`) basieren, werte ihren Status auf `#canon` auf, aber behalte die bisherigen Infos bei (Erweiterung, nicht Ersetzung).
3. **Rekonstruktion:** Erstelle eine chronologische Abfolge der Ereignisse. Identifiziere Anachronismen (z.B. Person gleichzeitig an zwei Orten).
4. **Dokumentation:** Erstelle/Aktualisiere ein Ticket im `LORE_RESEARCH_BOARD.md` oder hinterlasse ein kursives *Historiker-Gutachten* im betroffenen Wiki-Artikel.

## 3. Narrative Anreicherung (Narrative Enrichment)
Das Wiki soll kein trockenes Datenblatt sein. Werte Artikel (vor allem von oft genannten Charakteren) auf "Roman-Qualität" (Novel-Quality) auf:
1. **Context & Deep Read:** Wühle in den Boten-Quellen nach Handlungen und Beziehungen (wer kämpft, wer verhandelt, mit wem).
2. **Atmosphäre & Motivation:** Beschreibe die Szenen und frage nach dem *Warum* (Pflichtgefühl, Gier, Angst?).
3. **Regeln:** Keine Fakten erfinden (Halluzinations-Verbot). Nur vorhandene Rohdaten extrapolieren. Nutze Zitate, falls verfügbar. Reduziere Figuren nicht auf rein technische Rollenbegriffe.
4. **Score-Boost:** Nach der Aufwertung führe `./7w_wiki.py score <file>` aus, um den `lore_trust` manuell anzupassen.

## 4. Research Board Management
- Prüfe regelmäßig das `System/Synapse_Board/LORE_RESEARCH_BOARD.md` auf aktive Historian-Faelle (`OPEN_HISTORIAN`, `IN_REVIEW_HISTORIAN`, `AWAITING_HUMAN_DECISION`).
- Erzeuge neue Historian-Faelle nur dann, wenn operative Arbeit nicht sauber loesbar ist; weisse Flecken ohne akuten Fall bleiben im Themenreservoir.
- Lege Ergebnisse als Bericht unter `Logs/Research/` ab und uebertrage sie anschließend im `Wiki-Schmied` Standard ins Wiki.
- Melde Abschluss und Erkenntnisse via Dispatch (`mail done` oder `post`).

#historie #lore #orakel #narrative
