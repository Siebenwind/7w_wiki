---
description: Konsistenz-Audit & Vollständigkeitsprüfung (/audit)
---

# Workflow: /audit

Dieser Workflow dient der regelmäßigen Überprüfung der Lore-Integrität und der Abarbeitung identifizierter Inkonsistenzen.

## 1. Sichtung der Berichte & Tickets
1.  **Synapse Board:** Öffne das `/System/Synapse_Board/` und prüfe auf offene Tickets mit Status `NEEDS_REVIEW`.
2.  **Legacy:** Öffne den [Konsistenzbericht 2026](file:///Users/alexandrerabe/siebenwind/7w_wiki/Logs/Konsistenzbericht_2026.md) für ältere Einträge.

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

## 2b. Automatisierte Prüfung (Skript)
- Führe `.agent/scripts/register_check.py` aus.
- Das Skript liefert eine maschinenlesbare Übersicht über:
  - Duplikate im Personenregister
  - Verwaiste Profile (Datei existiert, kein Register-Eintrag)
  - Registrierte Personen ohne Profildatei
  - Boten-Lücken (Quellen vorhanden, aber nicht integriert)
  - Index-Lücken (Dateien vorhanden, aber nicht in `Die_Chronik.md`)
- Nutze die Skript-Ausgabe als Grundlage für den Audit-Report.

## 3. Orphan-Resolution (Verwaiste Profile)
Für jedes vom Skript oder manuell identifizierte verwaiste Profil:
1. **Öffne die Datei** und prüfe den Inhalt.
2. **Provenienz prüfen:**
   - Hat die Datei ein `quelle:`-Feld im Frontmatter? → Quelle verifizieren.
   - Fehlt `quelle:`? → Inhalt gegen bekannte Boten und Kanon-Quellen abgleichen.
3. **Entscheide:**
   - **Quelle identifiziert:** Profil ins Personenregister eintragen, `quelle:` ergänzen.
   - **Quelle unklar, Inhalt plausibel:** Profil registrieren mit Status `#überlieferung` und Vermerk `[QUELLE UNKLAR]`.
   - **Inhalt nicht zuordenbar:** Eintrag im Konsistenzbericht als `[ORPHAN]` + `⚠️ Offen` loggen.

## 4. Dokumentation des Status
- Aktualisiere den Status im Bericht von `[Offen]` zu `[Fixiert]` oder `[In Arbeit]`.
- Ergänze neue Fundstellen, die während anderer Workflows (z.B. `/ask` oder `/wiki_process`) automatisch dort abgelegt wurden.

## 5. Audit-Report
- Erstelle einen datierten Audit-Report in `Logs/Audit_Report_[DATUM].md`.
- **Pflichtfeld:** Jeder Report muss im Header eine eindeutige ID (UUID) tragen:
  `**Report-ID:** [UUID aus register_check.py]`
- Der Report dokumentiert **alle Prüfergebnisse** mit konkreten Zahlen und Tabellen.
- Empfehlungen für Prozessverbesserungen werden im Report formuliert und in die betroffenen Workflows übernommen.

## 6. Synapse-Vorgabe (Melde-Modus)
Jeder Workflow MUSS bei Fund einer Inkongruenz ein Ticket auf dem Synapse-Board erstellen. Nutze dazu die Vorlage `_TEMPLATE_TICKET.md`.

## 7. Audit-Abschluss & Statistiken
- Führe den Workflow `/stats` aus, um die globalen Wiki-Werte (Ingestion-Rate, Lore-Dichte) zu aktualisieren.
- Verlinke den Audit-Report in `Die_Chronik.md` oder relevanten Registern.

## 8. Audit-Zyklen
Führe diesen Workflow wöchentlich oder nach Abschluss eines großen Ingestion-Batches aus, um die Qualität des Wikis zu sichern.

#audit #qualität #konsistenz

