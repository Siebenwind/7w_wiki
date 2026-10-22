# Mitarbeit am Siebenwind Wiki (Community Legacy)

Dieses Wiki ist ein Gemeinschaftsprojekt. Wir nutzen die Infrastruktur von GitHub, um Qualität und Konsistenz über Generationen von Agenten und Lore-Hütern hinweg sicherzustellen.

## 🛠️ Der Kollaborations-Flow

Wir folgen dem **Git-Flow** Prinzip für Wissensdatenbanken:

1.  **Issues**: Melde Fehler, Widersprüche oder Lücken über unsere [Issue-Templates](https://github.com/Siebenwind/7w_wiki/issues).
2.  **Pull Requests (PRs)**: 
    - Forke das Repository.
    - Erstelle einen Feature-Branch für deine Änderungen.
    - Prüfe lokal mit `./7w_wiki.py audit`. Für veröffentlichte Seiten gehören Pages-Validierung und Browser-Abnahme dazu; siehe [Betrieb der Leserseiten](Agenten/leserseiten.md).
    - Reiche den PR ein. Ein Agent oder Administrator wird die Änderungen prüfen.
3.  **Review**: Bei Widersprüchen gilt Homepage > Quellen > Wiki Pages. Ein Tag allein ist kein Prüfnachweis. Ungeklärte Aussagen bleiben gekennzeichnet.

Du brauchst keine Entwicklungsumgebung, um einen Fehler zu melden. Unter jedem Artikel führt **Fehler melden** zu einem Formular mit der Artikeladresse. Beschreibe die Beobachtung und füge nach Möglichkeit eine Quelle hinzu.

## ⚖️ Lizenzen & Rechte

Durch deine Mitarbeit erklärst du dich mit folgenden Lizenzen einverstanden:

- **Software-Komponenten**: Die Skripte (`7w_wiki.py`, Sanitizer, Indexer etc.) stehen unter der **MIT License**.
- **Lore-Inhalte**: Alle Texte, Beschreibungen und Biographien stehen unter **CC BY-NC-SA 4.0** (Attribution-NonCommercial-ShareAlike).
    - Dies stellt sicher, dass das Wissen frei bleibt, nicht kommerziell ausgebeutet wird und unter gleichen Bedingungen weitergegeben wird.

## 🎨 Stil-Richtlinien

Bitte beachte unseren [Wiki Style Guide](Siebenwind_Wiki/00_Fundament/Wiki_Style_Guide.md) für:
- Korrekte Epistemik-Tags (`#canon`, `#bote`, etc.).
- Die Verwendung von `\[\[WikiLinks\]\]`.
- Das Standard-YAML-Frontmatter.

---
*Gemeinsam bewahren wir die Chroniken von 20 Jahren Rollenspiel.*
