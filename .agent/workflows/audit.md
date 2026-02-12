---
description: Konsistenz-Audit & Vollständigkeitsprüfung (/audit)
---

# Workflow: /audit

Dieser Workflow dient der regelmäßigen Überprüfung der Lore-Integrität und der Abarbeitung identifizierter Inkonsistenzen.

## 1. Sichtung der Berichte
1.  Öffne den aktuellen Bericht: [Konsistenzbericht 2026](file:///Users/alexandrerabe/siebenwind/7w_wiki/Logs/Konsistenzbericht_2026.md).
2.  Filtere nach Einträgen mit dem Status **⚠️ Offen** oder **Widerspruch**.

## 2. Verifikation & Cross-Check
- Nutze den **[Lore-Gelehrten]** Skill, um die betroffenen Artikel im Wiki gegen den Kanon (`/Hintergrund/`) zu prüfen.
- **Multi-Register Check:** Validiere die Konsistenz zwischen:
  - **Personen vs. Organisationen:** Sind Gildenmeister/Vorstände korrekt verlinkt?
  - **Ereignisse vs. Chronik:** Sind alle Daten in der Chronik erfasst?
  - **Kreaturen vs. Bestiarium:** Stimmt die Klassifizierung im Register?
- **Register-Vollständigkeit:**
  - **Profile → Register:** Alle Dateien in `07_Persoenlichkeiten/` müssen einen Eintrag im `Personenregister.md` haben.
  - **Register → Profile:** Alle Einträge im Register sollten eine korrespondierende Profildatei haben.
  - **Duplikat-Scan:** Prüfe auf doppelte Einträge im Personenregister (gleicher Name, unterschiedliche Zeilen).
- **Index-Vollständigkeit:**
  - **Boten-Index:** Vergleiche `Die_Chronik.md` Archiv gegen tatsächlich vorhandene Dateien in `04_Chronik/`.
  - **Quellen-Lücken:** Vergleiche integrierte Boten gegen verfügbare Quellen in `/Quellen/Zeitung 7w Bote/`.
- Validiere, ob vorgeschlagene Aktionen bereits in EXECUTION sind.

## 3. Dokumentation des Status
- Aktualisiere den Status im Bericht von `[Offen]` zu `[Fixiert]` oder `[In Arbeit]`.
- Ergänze neue Fundstellen, die während anderer Workflows (z.B. `/ask` oder `/wiki_process`) automatisch dort abgelegt wurden.

## 4. Audit-Report
- Erstelle einen datierten Audit-Report in `Logs/Audit_Report_[DATUM].md`.
- Der Report dokumentiert **alle Prüfergebnisse** mit konkreten Zahlen und Tabellen.
- Empfehlungen für Prozessverbesserungen werden im Report formuliert und in die betroffenen Workflows übernommen.

## 5. Vollständigkeits-Vorgabe
Jeder Workflow MUSS bei Fund einer Inkongruenz folgenden Block im Bericht ergänzen:

```markdown
---
## [KATEGORIE] Titel des Konflikts
**Quelle:** [[Wiki-Link]] / [Dateipfad]
**Inhalt:** Kurze Beschreibung der Abweichung.
**Status:** ⚠️ Offen
**Aktion:** Was muss getan werden?
```

## 6. Audit-Zyklen
Führe diesen Workflow wöchentlich oder nach Abschluss eines großen Ingestion-Batches aus, um die Qualität des Wikis zu sichern.

#audit #qualität #konsistenz

