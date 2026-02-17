---
description: Systematische Behebung von Audit-Befunden und Register-Inkonsistenzen (/repair)
---

Dieser Workflow dient der gezielten Abarbeitung von Problemen, die durch den `/audit` Workflow oder den Befehl `./7w_wiki.py audit` identifiziert wurden.

## Interop-Status
- runtime_commands:
  - `7w_wiki.py audit`
  - `7w_wiki.py repair`
- method_only:
  - `/repair`

## 1. Vorbereitung
- Führe den `/audit` Workflow aus oder starte `./7w_wiki.py audit`.
- Sichte den aktuellen Audit-Report (z.B. in `Logs/Audit_Report_[DATUM].md`).

## 2. Automatisierte Reparaturen (Skripte)
// turbo
1. **Frontmatter & Links:** Führe das Repair-Skript aus, um strukturelle Fehler zu beheben:
   ```bash
   ./7w_wiki.py repair
   ```
   - Wähle Option `1`, um fehlendes Frontmatter zu ergänzen.
   - Wähle Option `2`, um tote Links zu identifizieren und manuell im Editor zu fixen.
   - Wähle Option `3`, um Casing, Redirects und malformed Links automatisch zu reparieren.

## 3. Register-Konsolidierung (Deduplizierung)
- Bei **Duplikaten** im Personenregister:
  - Identifiziere die Zeilen-IDs im `Personenregister.md`.
  - Führe die Informationen (Rollen, Quellen, Zeiträume) in einem Eintrag zusammen.
  - Lösche den redundanten Eintrag.

## 4. Remediation: Fehlende Profile (Stubs)
Für Personen, die im Register stehen, aber keine Datei in `07_Persoenlichkeiten/` haben:
1. Nutze den **[Wiki-Schmied]** Skill, um eine standardisierte Stub-Datei zu erstellen.
2. Mindestinhalt für einen Stub:
   - Frontmatter (layout, title, category, quelle, status).
   - Titelzeile (`# Name`).
   - Sektion `## Beschreibung` (Einzeiler basierend auf Register-Rolle).
   - Sektion `## Referenzen` mit Link zur `quelle`.

## 5. Remediation: Verwaiste Profile (Orphans)
Für Dateien, die existieren, aber nicht im Register stehen:
1. **Validierung:** Prüfe, ob die Person bereits unter einem anderen Namen im Register steht (Alias-Check).
2. **Integration:** Füge die Person mit einem Link zur Datei in das `Personenregister.md` ein.
3. **Löschung:** Falls die Datei ein Duplikat eines existierenden Profils ist, führe den Inhalt zusammen und lösche die verwaiste Datei.

## 6. Abschlussprüfung
- Führe `./7w_wiki.py audit` erneut aus.
- Das Ergebnis sollte **"✅ Keine Duplikate"** und **"✅ Alle Profile registriert"** zeigen.
- Dokumentiere die durchgeführten Korrekturen im [Konsistenzbericht 2026](../../Logs/Konsistenzbericht_2026.md).

#repair #maintenance #qualität
