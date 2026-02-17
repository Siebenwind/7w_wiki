---
description: Department Master Workflow für Qualitätssicherung und Konsistenz
---

# Department: 🔍 Inquisition (CHECK)

Dieses Department überwacht die Integrität des Wikis und bannt "Link-Dämonen". Es fusioniert `/audit`, `/repair`, `/watch` und `/update`.

## Interop-Status
- runtime_commands:
  - `7w_wiki.py audit`
  - `7w_wiki.py repair`
  - `7w_wiki.py index --status`
- method_only:
  - `/check_master`
  - `/watch`
  - `/update`
  - `/contrib_audit`

## 1. Überwachung (Watch)
- [ ] Regelmäßige Prüfung der `Personenregister.md` auf "Broken Links" (unbesetzte Profile).
- [ ] Scan auf absolute Pfade (`file://`), die gegen relative Wiki-Links getauscht werden müssen.

## 2. Audit-Zyklus (Audit)
Führe das System-Audit aus:
```bash
./7w_wiki.py audit
```
- [ ] Identifikation von Duplikaten und verwaisten Dateien.
- [ ] Prüfung der YAML-Frontmatter Konsistenz.
- [ ] Bridge-/Placeholder-Hygiene prüfen (keine generischen Brueckenartikel ohne Ausnahme-Metadaten).

## 3. Bereinigung (Repair)
Nutze den interaktiven Repair-Modus für Batch-Fixes:
```bash
./7w_wiki.py repair
```

## 4. Community-Review (Sanitize)
- [ ] Prüfung von Community-Beiträgen (`/contrib_audit`) auf Stil-Einhaltung (Art Director, Lektor).

## 5. Eskalation
Inkonsistenzen, die nicht automatisiert lösbar sind, werden als `JUDICIAL_LOG` Eintrag oder Synapse-Ticket dokumentiert.

#audit #repair #konsistenz #qualität
