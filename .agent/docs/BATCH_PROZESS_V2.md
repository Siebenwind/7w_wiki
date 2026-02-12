# Protokoll: Batch-Prozess v2.0 (Siebenwind Wiki)

Dieses Dokument definiert den verbindlichen Standard für die Ingestion und Verarbeitung von Quellen im Siebenwind Wiki. Ziel ist eine hohe Datenqualität, narrative Tiefe ("Roman-Qualität") und lückenlose Vernetzung.

## 1. Vorbereitungsphase (Inventory)
- Jede neue Quelle muss in `Logs/INVENTUR_QUELLEN.md` erfasst werden.
- Epistemischer Status der Quelle prüfen (#canon, #bote, #perspektive).

## 2. Analysephase (Multi-Kategorie Extraktion)
Jedes Dokument wird systematisch nach folgenden Kategorien durchsucht:
1. **Personen:** Namen, Titel, Rollen, Schicksale.
2. **Geografie:** Orte, Gebäude, Landschaften, Wetterphänomene.
3. **Organisationen:** Gilden, Bünde, Orden, Familienhäuser.
4. **Ereignisse:** Schlachten, Feste, politische Umwälzungen, Naturkatastrophen.

## 3. Schreibphase (Produktion)
### Narrative Standards
- **Immersiv:** Umgebung (Gerüche, Kälte, Stimmung) einbeziehen.
- **Kontext:** Motivationen und soziale Auswirkungen beschreiben.
- **Keine Stubs:** Jeder Artikel muss einen Mindestgehalt an Information bieten.

### Quellen-Präsenz (Wiki-Stil)
Jeder Artikel endet zwingend mit der Sektion `## Überlieferungen & Quellen`.
- Verwendung eines GitHub-Style Alerts (`> [!NOTE]`).
- Angabe der Primärquelle mit Datum (innerweltlich).
- Direkte Zitate sind erwünscht und müssen als solche markiert sein.

## 4. Vernetzungsphase (Link Weaver)
- **Bi-direktionale Links:** Jede Verlinkung zu einem anderen Artikel sollte (wo sinnvoll) einen Backlink erzeugen.
- **Register-Synchronisation:** 
  - Personen -> `00_Fundament/Personenregister.md`
  - Organisationen -> `00_Fundament/Organisationsregister.md`
  - Ereignisse -> `04_Chronik/Ereignisregister.md`
- **Sicherheits-Append:** Beim Hinzufügen zu Registern müssen Ankerzeilen verwendet werden, um Datenverlust zu vermeiden.

## 5. Verifikationsphase (Audit)
- Prüfung auf "Orphans" (verwaiste Artikel).
- Prüfung auf tote Links.
- Eintragung von Inkonsistenzen in den `Logs/Konsistenzbericht_2026.md`.

---
*Status: Gültig ab 13.02.2026*
