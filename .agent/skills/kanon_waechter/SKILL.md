---
layout: wiki_page
name: Kanon-Wächter (Verification)
description: Fähigkeit, Fakten gegen die offizielle Homepage zu prüfen.
---

# Unknown

**Epistemischer Status:** #perspektive

Dieser Skill stellt sicher, dass das Wiki dem "Live-Kanon" entspricht.

## Arbeitsweise
1.  **Trigger:** Sobald eine relevante Entität (Person, Ort, Ereignis) im Scanner-Skill identifiziert wurde.
2.  **Suche:** Nutze `search_web` mit dem Operator `site:siebenwind.de`.
    *   *Query:* `site:siebenwind.de "Name der Entität"`
3.  **Abgleich:**
    *   Findet sich der Begriff auf der Homepage? -> **Web-Kanon sticht Lokal-Datei.**
    *   Widersprechen sich die Infos? -> **Web-Kanon hat Vorrang.**
    *   Kein Treffer? -> **Lokal-Datei gilt als Legacy-Kanon.**

## Ziel
Vermeidung von veralteten oder widersprüchlichen Informationen im Wiki.
