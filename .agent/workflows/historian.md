---
layout: wiki_page
title: "Workflow: `/historian` (Der Historiker)"
category: Workflow
description: Deep lore analysis workflow for targeted reconstruction, canon checks, and contradiction resolution
---

# Workflow: `/historian` (Der Historiker)

Dieses ausfuehrbare Workflowblatt ist der fokussierte Einzelauftrag-Pfad fuer tiefe Lore-Analyse.
Es ist **kein** Default-Einstieg fuer jede neue Quelle, sondern der Runtime-Pfad fuer Faelle, die operativ nicht sauber loesbar sind, sowie fuer gezielte Fachfragen.
Fuer die groessere Department-Logik verweist es auf [lore_master.md](lore_master.md).

## Interop-Status
- runtime_commands:
  - `7w_wiki.py historian [query]`
  - `7w_wiki.py historian review --list --json`
  - `7w_wiki.py historian review --human`
  - `7w_wiki.py historian review --dossier --research-id RESEARCH-2026-XXX --json`
  - `7w_wiki.py historian review --research-id RESEARCH-2026-XXX --decision commented --reviewer Historian --role historian_comment --note "<Kommentar>" --json`
  - `7w_wiki.py historian review --approve RESEARCH-2026-XXX --note "<Begruendung>" --dry-run`
  - `7w_wiki.py historian review --return RESEARCH-2026-XXX --note "<Nacharbeit>" --dry-run`
  - `7w_wiki.py pages backlog historian --next`
  - `7w_wiki.py pages backlog historian --cluster <cluster> --dry-run --json`
  - `7w_wiki.py pages backlog historian --article <path> --resolve --json`
  - `7w_wiki.py pages backlog historian --cluster <cluster> --resolve --json`
  - `7w_wiki.py pages backlog historian --run-all --resolve --json`
  - `7w_wiki.py pages backlog historian --run-all --resolve --apply --yes --i-understand-bulk-semantics`
  - `7w_wiki.py search <query> --source wiki|quellen|all`
  - `7w_wiki.py score <file>`
  - `7w_wiki.py mail inbox --status OPEN`
  - `7w_wiki.py mail post --from Historian --to <agent|ALL> --subject "<text>" --body "<text>"`
- method_only:
  - `/lore_master`
- interop_note: `7w_wiki.py historian` shows this workflow by default; passing a query starts the Oracle-backed analysis handoff.

## 1. Auftrag klaeren
1. Lies offene Historian-Nachrichten mit `./7w_wiki.py mail inbox --status OPEN`.
2. Pruefe den strukturierten Review-Backlog mit `./7w_wiki.py historian review --list --json`.
3. Lies fuer konkrete Review-Faelle zuerst das Dossier: `./7w_wiki.py historian review --dossier --research-id RESEARCH-2026-XXX --json`.
4. Lies bei Dispatch-Auftraegen die konkrete Nachricht mit `./7w_wiki.py mail read <id>`.
5. Claime den Auftrag mit `./7w_wiki.py mail claim <id> --agent Historian`, sobald du ihn uebernimmst.
6. Pruefe zuerst, ob der Fall wirklich Historian-Charakter hat oder operativ direkt loesbar ist.

## 2. Evidenz sammeln
1. Starte mit `./7w_wiki.py search "<frage>" --source wiki`.
2. Pruefe danach `./7w_wiki.py search "<frage>" --source quellen`.
3. Konsolidiere den Delta-Check mit `./7w_wiki.py search "<frage>" --source all`.
4. Wende stets die epistemische Praezedenz an: `Homepage > Quellen > Wiki Pages`.

## 3. Historiker-Gutachten
1. Rekonstruiere die robusteste, quellengetragene Lesart.
2. Markiere verbleibende Unsicherheit explizit als `[UNGEKLAERT]` oder eskaliere question-first.
3. Wenn ein Wiki-Ziel oder Artikel geaendert wird, dokumentiere die Entscheidung knapp im Dispatch oder in einem Research-Log.
4. Route nur bei echter Kontroverse oder Kanonentscheidung an den Menschen weiter.

## 3b. Review-Haertung fuer Backlog-Abbau
1. `IN_REVIEW_HISTORIAN` bedeutet: Gutachten liegt vor; der Historian darf fachlich kommentieren, aber nicht final menschlich freigeben.
2. Menschen nutzen zuerst die Entscheidungsansicht:
   `./7w_wiki.py historian review --human`
3. Nutze fuer Historian-Kommentare:
   `./7w_wiki.py historian review --research-id RESEARCH-2026-XXX --decision commented --reviewer Historian --role historian_comment --note "<Kommentar>" --json`
4. Finales Approve/Return erfolgt menschenfreundlich ueber `--approve RESEARCH-2026-XXX --note "<Begruendung>"` oder `--return RESEARCH-2026-XXX --note "<Nacharbeit>"`; beide Befehle setzen intern `human_final`.
5. Vor Live-Ausfuehrung zuerst denselben Befehl mit `--dry-run` validieren.
6. Jeder nicht-trockene Review-Schritt schreibt ins Review-Register, aktualisiert die Archivseite und erzeugt Dispatch-Nachweis.
7. Backlog-Abbau beginnt mit `review --human`; Faelle ohne Summary oder Archivseite sind zuerst strukturell zu reparieren.

## 3c. Pages-Backlog als Historian-Clusterlane
1. `needs_historian` bedeutet: Der Fall ist nicht mechanisch sicher, aber durch den Historian clusterweise bearbeitbar.
2. Starte mit `./7w_wiki.py pages backlog historian --next`.
3. Pruefe konkrete Cluster mit `./7w_wiki.py pages backlog historian --cluster <cluster> --dry-run --json`.
4. Erzeuge semantische Entscheidungen mit `./7w_wiki.py pages backlog historian --cluster <cluster> --resolve --json` oder dateiweise mit `--article <path> --resolve --json`.
5. Schreibe semantische Entscheidungen nur mit `--resolve --apply --yes`; der Vollautomat zusaetzlich nur mit `--run-all --resolve --apply --yes --i-understand-bulk-semantics`.
6. Technische Format-/Wrapper-Cluster duerfen nur bei eindeutigem Replacement angewendet werden; semantische Cluster schreiben nur `replace`-Entscheidungen mit lokaler Evidenz.
7. Rohquellen unter `docs/Quellen` bleiben read-only und werden hoechstens als Residuen notiert.
8. Nur echte Kanon-, Praezedenz- oder Zielkonflikte werden als `needs_human` eskaliert.

## 4. Abschluss
1. Poste einen Statusbericht mit `./7w_wiki.py mail done` oder `./7w_wiki.py mail post`.
2. Nutze fuer groessere, mehrstufige Lore-Arbeit anschliessend den Department-Prozess in [lore_master.md](lore_master.md).
