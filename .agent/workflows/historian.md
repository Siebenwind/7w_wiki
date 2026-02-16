---
description: Dedizierter Workflow für tiefgreifende Lore-Analysen und Quellen-Evaluierung (/historian)
---

# Workflow: /historian (Der Pfad der Chronisten)

## Interop-Status
- runtime_commands:
  - `7w_wiki.py historian <query>`
  - `7w_wiki.py search <query> --source wiki`
  - `7w_wiki.py search <query> --source quellen`
  - `7w_wiki.py search <query> --source all`
- method_only:
  - `/historian`

Dieser Workflow wird genutzt, wenn ein komplexer Sachverhalt eine tiefere Analyse erfordert, die über ein einfaches Audit hinausgeht. Er dient der Rekonstruktion von Kausalitäten und der Auflösung von Quellenwidersprüchen.

## 1. Themen-Definition
Identifiziere den Gegenstand der Untersuchung (Person, Ort, Ereignis oder theoretisches Konzept).

## 2. Quellen-Aggregation (Sichtungsphase)
1.  **Semantische Suche (Wiki-Layer)**: `./7w_wiki.py search "[Thema]" --source wiki --top 20`.
2.  **Semantische Suche (Quellen-Layer)**: `./7w_wiki.py search "[Thema]" --source quellen --top 20`.
3.  **Semantische Suche (Gesamtabgleich)**: `./7w_wiki.py search "[Thema]" --source all --top 20`.
4.  **Register-Check**: Prüfe alle Erwähnungen im `Personenregister.md` oder `Organisationsregister.md`.
5.  **Hintergrund-Abgleich**: Suche nach Axiomen im Verzeichnis `/Hintergrund/`, die das Thema betreffen (#canon).

## 3. Epistemische Einordnung
Bewerte die gefundenen Informationen nach dem Siebenwind-Wahrheitsmodell:
- **Was ist Fundament?** (#canon)
- **Was ist Zeitzeugnis?** (#bote)
- **Was ist subjektive Sicht?** (#perspektive)

## 4. Rekonstruktion (Synthese)
Erstelle eine chronologische Abfolge der Ereignisse oder eine logische Herleitung der Theorie.
- Suche nach **Anachronismen** (z.B. Person an zwei Orten).
- Identifiziere **Motivationen** hinter Berichten (Cui bono?).

## 5. Resultat & Dokumentation
1.  **Wiki-Update**: Erweitere den betroffenen Artikel um eine Sektion `## Historische Einordnung` oder `## Analyse des Gelehrten`.
2.  **Synapse-Ticket**: Falls ein Widerspruch ungelöst bleibt, erstelle ein Ticket oder einen Forschungsauftrag im **Board**.
3.  **Kausalitäts-Update**: Verknüpfe das Ergebnis mit der globalen `Die_Chronik.md`.

## 6. Historiker-Gutachten
Jeder Abschluss eines Historiker-Workflows endet mit einer kurzen, kursiven Einordnung im Artikel, markiert mit:
> *Historiker-Gutachten: [Zusammenfassende Analyse der Quellenlage und Empfehlung für die zukünftige Lore-Fortschreibung].*

#historie #analyse #rekonstruktion #gelehrter
