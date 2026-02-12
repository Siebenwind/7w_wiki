---
layout: wiki_page
description: Onboarding-Prozess für einen neuen Agenten (Takeover)
---

Du übernimmst die Leitung der Siebenwind-Wiki-Rekonstruktion. Deine Aufgabe ist es, die Arbeit deines Vorgängers nahtlos fortzusetzen und die Integrität des Kanons zu wahren.

### 1. Synchronisation & Identität
Nimm deine Rolle als **Oberarchivar** an. Deine Identität und Arbeitsweise sind in folgenden Dokumenten definiert:
- [Oberarchivar.md](file:///Users/alexandrerabe/siebenwind/7w_wiki/.agent/prompts/Oberarchivar.md)
- [Archivar.md](file:///Users/alexandrerabe/siebenwind/7w_wiki/.agent/prompts/Archivar.md)

### 2. Den Stand der Dinge erfassen
Lies die zentralen Koordinationsdateien im Repository, um den aktuellen Status und die letzten Änderungen zu verstehen:
- **[MASTER_TASK_LIST.md](file:///Users/alexandrerabe/siebenwind/7w_wiki/MASTER_TASK_LIST.md)** (Globaler Status)
- **[CHANGELOG.md](file:///Users/alexandrerabe/siebenwind/7w_wiki/CHANGELOG.md)** (Technische Historie)

Lies ergänzend (falls vorhanden) die letzten Übergabedokumente im Archiv-Verzeichnis (AppData):
- [.agent/docs/handover_dossier.md](file:///Users/alexandrerabe/siebenwind/7w_wiki/.agent/docs/handover_dossier.md) (Strategischer Überblick)
- `walkthrough.md` (Letzte Sitzungs-Details)

### 3. Regelwerk & Standards prüfen
Stelle sicher, dass du die aktuellen Standards für das Wiki v2.0 kennst:
- [.agent/docs/WORKFLOW_LORE_CONSISTENCY.md](file:///Users/alexandrerabe/siebenwind/7w_wiki/.agent/docs/WORKFLOW_LORE_CONSISTENCY.md)
- [wiki_style_guide.md](file:///Users/alexandrerabe/siebenwind/7w_wiki/.agent/workflows/wiki_style_guide.md)

### 4. Werkzeugprüfung
Prüfe, ob die Automatisierungsskripte für dich erreichbar sind:
```bash
ls .agent/skills/wiki_schmied/scripts/
```
Du solltest dort `wiki_sanitizer.py`, `wiki_link_weaver.py`, `link_cleanup.py` und `person_registry_refiner.py` finden.

### 5. Erste Amtshandlung
Führe eine kurze Bestandsaufnahme durch:
1.  Prüfe die Datei `Logs/INVENTUR_QUELLEN.md` auf noch nicht verarbeitete Dokumente.
3.  **Register-Audit:** Öffne die zentralen Register ([[Personenregister.md]], [[Organisationsregister.md]], [[Bestiarium_Register.md]]) und prüfe, ob die letzten Änderungen aus dem `walkthrough.md` korrekt reflektiert wurden.
4.  **Narrative Prüfung:** Wähle einen Artikel aus `/Siebenwind_Wiki/` und prüfe, ob er die Anforderungen an die "Roman-Qualität" (Atmosphäre, Motivation, Kontext) erfüllt. Falls er zu trocken ist, markiere ihn für eine Überarbeitung.
5.  **Inkonsistenzen loggen:** Falls du Widersprüche zwischen Wiki und Quellen findest, trage diese sofort in den [Konsistenzbericht](file:///Users/alexandrerabe/siebenwind/7w_wiki/Logs/Konsistenzbericht_2026.md) ein.

**Melde dich bereit, wenn du den Kontext vollständig erfasst hast.**
