---
description: Systematische Behebung von Audit-Befunden und Register-Inkonsistenzen (/repair)
---

Dieser Workflow dient der gezielten Abarbeitung von Problemen, die durch den `/audit` Workflow oder den Befehl `./7w_wiki.py audit` identifiziert wurden.

## Interop-Status
- runtime_commands:
  - `7w_wiki.py audit`
  - `7w_wiki.py repair`
  - `7w_wiki.py search <query> --source wiki|quellen|all`
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

## 4. Remediation: Fehlende Profile (kanonisch, kein Stub-Shortcut)
Für Personen, die im Register stehen, aber keine Datei in `07_Persoenlichkeiten/` haben:
1. **Alias- und Zielprüfung zuerst (Pflicht):**
   - Suche nach existierenden Zielseiten via `./7w_wiki.py search "<Name>" --source wiki`.
   - Falls ein kanonisches Ziel bereits existiert (abweichender Dateiname/Casing/Alias), repariere den Register-Link auf das bestehende Ziel statt neue Datei anzulegen.
2. **Nur bei belastbarer Quelle neue Seite erstellen:**
   - Nutze den **[Wiki-Schmied]** Skill für einen vollwertigen Artikel mit `quelle:` als relativem Pfad und Pflichtsektionen.
   - Keine Minimalseiten mit Einzeiler als Endzustand.
3. **Keine Brückenartikel als Standard-Fix:**
   - Formulierungen wie „Brueckenartikel zur Stabilisierung bestehender WikiLinks“ gelten als Defect, nicht als Abschluss.
   - Wenn Evidenz fehlt: Fall als offene Frage per `./7w_wiki.py mail post` an Spezialisten dispatchen.
4. **Temporäre Ausnahme nur mit Ablaufmetadaten:**
   - Nur wenn ein Linkbruch akut geblockt werden muss, darf temporär markiert werden mit:
     - `bridge_mode: temporary`
     - `bridge_target: [[Kanonisches_Ziel_oder_TODO]]`
     - `bridge_ticket: MSG-YYYY-NNNN` (oder Task-ID)
     - `bridge_review_until: YYYY-MM-DD`
   - Ohne diese Felder ist die Seite audit-pflichtig als Hygiene-Fehler.

## 5. Remediation: Verwaiste Profile (Orphans)
Für Dateien, die existieren, aber nicht im Register stehen:
1. **Validierung:** Prüfe, ob die Person bereits unter einem anderen Namen im Register steht (Alias-Check).
2. **Integration:** Füge die Person mit einem Link zur Datei in das `Personenregister.md` ein.
3. **Löschung:** Falls die Datei ein Duplikat eines existierenden Profils ist, führe den Inhalt zusammen und lösche die verwaiste Datei.

## 6. Abschlussprüfung
- Führe `./7w_wiki.py audit` erneut aus.
- Das Ergebnis sollte **"✅ Keine Duplikate"** und **"✅ Alle Profile registriert"** zeigen.
- Prüfe zusätzlich, dass keine neuen Bridge-/Placeholder-Seiten ohne Ausnahme-Metadaten entstanden sind.
- Dokumentiere die durchgeführten Korrekturen im [Konsistenzbericht 2026](../../Logs/Konsistenzbericht_2026.md).

#repair #maintenance #qualität
