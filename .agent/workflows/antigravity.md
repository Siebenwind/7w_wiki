---
description: Der Ur-Prozess / Default Protocol (Antigravity)
---

# Workflow: `/antigravity` (The Core Loop)

## Interop-Status
- runtime_commands:
  - `7w_wiki.py antigravity`
  - `7w_wiki.py start`
  - `7w_wiki.py advisor`
  - `7w_wiki.py audit`
  - `7w_wiki.py repair`
  - `7w_wiki.py stats`
  - `7w_wiki.py test --suite clean-client-state`
  - `7w_wiki.py mail post --from <agent> --to <agent|ALL> --subject "<text>" --body "<text>"`
- method_only:
  - `/antigravity`

Dieser Workflow ist das **Fundament** der Agenten-Interaktion. Er unterwirft den Agenten strikt der Logik der Skripte. Er ist die Antwort auf die Frage nach "Default Options".

## 1. Die Mentalität (Code is Law)
Solange dieser Workflow aktiv ist, gibst du deine kreative Freiheit auf.
- **Du bist eine Runtime Environment**, kein Autor.
- **Du exekutierst**, du interpretierst nicht.
- **Du vertraust dem Code** mehr als deiner Intuition.

## 1b. Das Gerichtsprotokoll (Eskalation)
Nutze das [JUDICIARY_LOG.md](../../Logs/JUDICIARY_LOG.md) **nur bei Eskalation (Level 3)**:
- Wenn der Kanon unklar ist.
- Wenn du eine schwerwiegende Entscheidung ohne direkte Anweisung triffst.
- Bei allen `[UNGEKLÄRT]` Fällen.
Routineaufgaben werden weiterhin nur via Git und Changelog dokumentiert.

## 2. Der Status-Check (Onboarding)
Der erste Schritt ist immer das Onboarding. Es analysiert den Status und gibt dir Handlungsoptionen.

// turbo
./7w_wiki.py start

## 3. Die Exekution
Führe **exakt** das aus, was der Advisor empfiehlt.
- Wenn er `/repair` sagt, führe `/repair` aus.
- Wenn er `/batch` sagt, führe `/batch` aus.
- Wenn er sagt "Nichts zu tun", dann generiere Statistiken (`/stats`) und melde dich beim User.

## 4. Die Sicherheits-Garantie
Solltest du jemals unsicher sein, was zu tun ist:
1.  Halte inne.
2.  Führe `./7w_wiki.py audit` aus.
3.  Lies das Ergebnis.
4.  Handle danach.

## 5. Die Dokumentations-Pflicht (No Silent Changes)
Jede relevante Aenderung wird nachvollziehbar dokumentiert.
1. Update `CHANGELOG.md` (Was, Warum, Validierung).
2. Bei UX/CD-Anpassungen:
   - `docs/Archiv/REDESIGN_ROADMAP_2026.md` aktualisieren.
   - Betroffene Skills/Workflows synchronisieren (z.B. Art Director, /herold, /tech).
3. Sessionende:
   - Session-Memory unter `Logs/Archive/SESSION_MEMORY_YYYY-MM-DD_<THEMA>.md`.
   - Pfad per `./7w_wiki.py mail post` an Folgeagenten melden.

### Aenderungsstand
- 2026-02-17: Leserfokus-Relaunch als dokumentationspflichtiger Standardfall verankert (Roadmap + Skill/Workflow-Sync + Session-Memory/Dispatch).

**Information Loss is unacceptable.**
