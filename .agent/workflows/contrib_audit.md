---
description: Review & Sanitize Community Contributions (/contrib_audit)
---

# Workflow: /contrib_audit

Dieser Workflow wird angewendet, wenn externe Nutzer Änderungen via Pull Request (PR) einreichen. Ziel ist es, die Qualität und Konformität der Beiträge sicherzustellen.

## 1. Initiale Sichtung (PR-Analyse)
1. **GitHub PR öffnen:** Schau dir den Diff der Änderungen an.
2. **Standard-Check:**
   - [ ] Hat der Artikel die korrekte YAML-Frontmatter?
   - [ ] Entspricht die H1 dem `title`?
   - [ ] Wurden absolute Pfade (`file:///`) verwendet? (Falls ja: Ablehnen oder mit `link_cleanup.py` korrigieren).
   - [ ] Wurden die korrekten Tags (`#canon`, `#bote`, etc.) verwendet?

## 2. Inhalts- & Lore-Check
1. **Faktenprüfung:** Nutze den **[Lore-Gelehrten]** Skill, um zu prüfen, ob die Änderungen dem bestehenden `#canon` widersprechen.
2. **Linguistik-Check:** Falls neue Begriffe eingeführt wurden, prüfe diese mit dem **[Linguist]** Skill.
3. **Qualitätscheck:** Entspricht der Text der geforderten "Roman-Qualität"?

## 3. Entscheidung & Integration
- **Option A: Annahme.** Merger den PR. Führe danach den `wiki_link_weaver.py` aus, um bi-direktionale Verlinkungen für den neuen Content zu erstellen.
- **Option B: Nachbesserung.** Kommentiere den PR mit spezifischen Korrekturwünschen (beziehe dich auf den `wiki_style_guide.md`).
- **Option C: Ablehnung.** Falls der Beitrag massiv dem Kanon widerspricht oder qualitativ unzureichend ist.

## 4. Abschluss
- Aktualisiere die **MASTER_TASK_LIST.md** und das **CHANGELOG.md**.
- Markiere den PR als abgeschlossen.
