---
description: Deep lore analysis workflow for targeted reconstruction, canon checks, and contradiction resolution
---

# Workflow: `/historian` (Der Historiker)

Dieses ausfuehrbare Workflowblatt ist der fokussierte Einzelauftrag-Pfad fuer tiefe Lore-Analyse.
Es dient als Runtime-Einstieg fuer konkrete Forschungsfragen und verweist fuer die groessere Department-Logik auf [lore_master.md](lore_master.md).

## Interop-Status
- runtime_commands:
  - `7w_wiki.py historian [query]`
  - `7w_wiki.py search <query> --source wiki|quellen|all`
  - `7w_wiki.py score <file>`
  - `7w_wiki.py mail inbox --status OPEN`
  - `7w_wiki.py mail post --from Historian --to <agent|ALL> --subject "<text>" --body "<text>"`
- method_only:
  - `/lore_master`
- interop_note: `7w_wiki.py historian` shows this workflow by default; passing a query starts the Oracle-backed analysis handoff.

## 1. Auftrag klaeren
1. Lies offene Historian-Nachrichten mit `./7w_wiki.py mail inbox --status OPEN`.
2. Lies die konkrete Nachricht mit `./7w_wiki.py mail read <id>`.
3. Claime den Auftrag mit `./7w_wiki.py mail claim <id> --agent Historian`, sobald du ihn uebernimmst.

## 2. Evidenz sammeln
1. Starte mit `./7w_wiki.py search "<frage>" --source wiki`.
2. Pruefe danach `./7w_wiki.py search "<frage>" --source quellen`.
3. Konsolidiere den Delta-Check mit `./7w_wiki.py search "<frage>" --source all`.
4. Wende stets die epistemische Praezedenz an: `Homepage > Quellen > Wiki Pages`.

## 3. Historiker-Gutachten
1. Rekonstruiere die robusteste, quellengetragene Lesart.
2. Markiere verbleibende Unsicherheit explizit als `[UNGEKLAERT]` oder eskaliere question-first.
3. Wenn ein Wiki-Ziel oder Artikel geaendert wird, dokumentiere die Entscheidung knapp im Dispatch oder in einem Research-Log.

## 4. Abschluss
1. Poste einen Statusbericht mit `./7w_wiki.py mail done` oder `./7w_wiki.py mail post`.
2. Nutze fuer groessere, mehrstufige Lore-Arbeit anschliessend den Department-Prozess in [lore_master.md](lore_master.md).
