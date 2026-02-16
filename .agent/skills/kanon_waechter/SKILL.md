---
layout: wiki_page
name: Kanon-Wächter (Verification)
description: Fähigkeit, Fakten gegen die offizielle Homepage zu prüfen.
---

# Kanon-Waechter (Skill)

**Epistemischer Status:** #perspektive

Dieser Skill stellt sicher, dass das Wiki dem "Live-Kanon" entspricht.

## Interop-Hinweis
- Runtime-Checks laufen primär über `./7w_wiki.py search "<Query>" --source wiki|quellen|all`.
- Externe Websuche ist nur **method hint (non-runtime)**.

## Arbeitsweise
1.  **Trigger:** Sobald eine relevante Entität (Person, Ort, Ereignis) im Scanner-Skill identifiziert wurde.
2.  **Suche (method hint, non-runtime):** Nutze Websuche mit dem Operator `site:siebenwind.de`.
    *   *Query:* `site:siebenwind.de "Name der Entität"`
3.  **Abgleich:**
    *   Findet sich der Begriff auf der Homepage? -> Als Hinweis/Ergaenzung dokumentieren.
    *   Widersprechen sich die Infos? -> Ticket auf dem Synapse-Board erstellen und nicht automatisch ueberschreiben.
    *   Kein Treffer? -> **Lokal-Datei gilt als Legacy-Kanon.**

## Ziel
Vermeidung von veralteten oder widersprüchlichen Informationen im Wiki.
