---
description: Department Master Workflow für Projekt-Meta und Handover
---

# Department: 📦 Logistik (META)

Dieses Department regelt den Agenten-Alltag, die Dokumentation und den Wissenstransfer. Es fusioniert `/start`, `/takeover`, `/handover`, `/docs` und `/stats`.

## Interop-Status
- runtime_commands:
  - `7w_wiki.py start`
  - `7w_wiki.py stats`
  - `7w_wiki.py archive sync`
  - `7w_wiki.py mail post --to ALL ...`
- method_only:
  - `/meta_master`
  - `/takeover`
  - `/handover`
  - `/docs`
- method_hints_non_runtime:
  - Host-notification channel (nur als Hinweis, nicht runtime)

## 1. Onboarding (Start)
- [ ] Führe `./7w_wiki.py start` aus, um Optionen zu sehen.
- [ ] Analysiere den **Advisor-Report**.

## 2. Daily Business (Sync)
- [ ] Halte die `MASTER_TASK_LIST.md` aktuell.
- [ ] Führe regelmäßig Statistiken aus:
```bash
./7w_wiki.py stats
```

## 3. Dokumentation (Publicity)
- [ ] Aktualisiere `README.md` und `CHANGELOG.md` nach großen Meilensteinen.
- [ ] Erstelle Walkthroughs (`walkthrough.md`) für komplexe Änderungen.

## 4. Kommunikation (Decisions)
- [ ] Hole Nutzer-Entscheidungen über `/decide` ein.
- [ ] Bei Blockaden nutze runtime-seitig `./7w_wiki.py mail post --to ALL ...`.
- [ ] Host-Notifications gelten nur als method hint (non-runtime).

## 5. Handover
- [ ] Erstelle ein Übergabeprotokoll für den nächsten Agenten.
- [ ] Committe alle Änderungen mit aussagekräftigen Nachrichten.

#meta #logistik #handover #dokumentation
