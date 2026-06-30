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
  - `7w_wiki.py historian review --dossier --research-id RESEARCH-2026-XXX --json`
  - `7w_wiki.py historian review --research-id RESEARCH-2026-XXX --decision commented --reviewer Historian --role historian_comment --note "<Kommentar>" --json`
  - `7w_wiki.py historian review --research-id RESEARCH-2026-XXX --decision approved|returned --reviewer Human --role human_final --note "<Entscheidung>" --dry-run --json`
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
2. Nutze fuer Historian-Kommentare:
   `./7w_wiki.py historian review --research-id RESEARCH-2026-XXX --decision commented --reviewer Historian --role historian_comment --note "<Kommentar>" --json`
3. Finales Approve/Return bleibt `--role human_final` vorbehalten und sollte vor Live-Ausfuehrung mit `--dry-run --json` validiert werden.
4. Jeder nicht-trockene Review-Schritt schreibt ins Review-Register, aktualisiert die Archivseite und erzeugt Dispatch-Nachweis.
5. Backlog-Abbau beginnt mit `review --list --json`; Faelle ohne Summary oder Archivseite sind zuerst strukturell zu reparieren.

## 4. Abschluss
1. Poste einen Statusbericht mit `./7w_wiki.py mail done` oder `./7w_wiki.py mail post`.
2. Nutze fuer groessere, mehrstufige Lore-Arbeit anschliessend den Department-Prozess in [lore_master.md](lore_master.md).
