# Master Task List: Siebenwind-Wiki-Rekonstruktion

Dieses Dokument dient als agentenübergreifendes Gedächtnis. Es trennt den **aktiven Fokus** von der **Projekthistorie** und definiert klare Standards für die Aufgabenpriorisierung.

## 📊 Status-Übersicht
- **Wiki-Standard:** v2.1 (Epistemik implementiert)
- **Ingestion-Fortschritt:** ~85% (Spielergeschichten Re-Scan läuft)
- **RAG-Status (Orakel):** Aktiv & MPS-optimiert (Hardware-Auto-Tuning aktiv)

---

## 🔴 Priorität 1: Aktueller Fokus (Kritisch / Blocker)
*Diese Aufgaben haben höchste Dringlichkeit und müssen abgeschlossen werden, bevor neue Phasen begonnen werden.*

- [x] Epistemic Status & Link-Audit (Phase 13)
- [x] Restore Wiki Consistency (Deduplication, Orphan-Fix)
- [ ] Spielergeschichten Re-Scan & Entity Integration
    - **Fortsetzung Ingestion**: Ab Batch 9 (ca. 100+ Dateien verbleibend). Ziel: Vollständige Erfassung aller Meta-Tags und Entitäten.
    - **Register-Synchronisation**: Übertragung der im `Logs/INGESTION_LOG.md` gesicherten Entitäten (u.a. [[Jassavia]], [[Veridon]], [[Zoran Gosh]]) in das [[Personenregister.md]] und [[Ortsregister.md]].
    - **Duplikat-Auflösung**: Finale Entscheidung und Bereinigung der Dateisystem-Dubletten (z.B. `Der Flug der Ente`).
- [ ] **Handover-Vorbereitung**:
    - **Link-Validierung**: Systematisches Suchen und Ersetzen von absoluten `file://` Pfaden durch relative `[[WikiLinks]]`.
    - **Sanitizer-Check**: Ausführen von `wiki_sanitizer.py` über alle neu erstellten Artikel zur Sicherstellung von v2.1 Standards.

## 🟡 Priorität 2: Inhalte & Ingestion (Operativ)
*Standardaufgaben des Archiv-Prozesses zur Erweiterung der Wissensbasis.*

- [/] **Massen-Ingestion**: Integration der verbleibenden 150+ Quellen (Status `Pending` in [[INVENTUR_QUELLEN.md]]). Fokus auf Themengebiete (z.B. Religion, Handwerk).
- [ ] **Vernetzung (Weaving)**: Überprüfung der bi-direktionalen Verlinkung. Sicherstellen, dass unter `## Überlieferungen` qualitativ hochwertige Backlinks bestehen.
- [ ] **Narrative Enrichment**: Ausbau von Stubs zu profunden Artikeln ("Roman-Qualität"). Fokus auf Motivation, Atmosphäre und Zitate.

## 🔵 Priorität 3: Qualität & Politur (Optimierung)
*Verbesserungen an System und Lore, die den Nutzwert steigern.*

- [ ] **Chronik-Konsolidierung**: Abgleich der neuen Erkenntnisse aus den Spielergeschichten mit der offiziellen [[Zeitrechnung_(Der_Sonnenzirkel).md]].
- [ ] **Feature: „Der Kartograph“**: Implementierung eines Skills zur geografischen Datenverwaltung und Reisezeiten-Berechnung.

## ⚪ Backlog / Future (Ideenspeicher)
*Langfristige Ziele ohne aktuelle Zeitplanung.*

- [ ] **Skill: „Der Herold“**: Automatisches News-Broadcasting basierend auf Wiki-Änderungen.
- [ ] **Workflow: `/map_sync`**: Visuelle Verknüpfung von Wiki-Entitäten mit einer externen Karte.
- [ ] **Workflow: `/cleanup`**: Vollautomatisierter Bot zur kontinuierlichen Pfad-Bereinigung.

---

## ✅ Historie & Abgeschlossene Meilensteine

### Phase 13: Politische Krisen (Feb 2026)
- **Boten 181-185**: Rekonstruktion des Putsches in Falkensee und der Führungskrise des Löwenordens.
- **Historiker-Audit**: Fall Benedict Rabenfels (Analyse der Korruption).
- **Register-Cleanup**: 25 Orphans saniert, 9 echte Personen-Duplikate gelöscht.

### Phase 12: Epistemik & Struktur (Feb 2026)
- **Epistemisches System**: Implementierung der 4 Säulen der Wahrheit (#canon, #bote, #perspektive, #überlieferung) im Style Guide.
- **Eskalationsmatrix**: Definition klarer Regeln zur Auflösung von Lore-Widersprüchen.
- **Wiki v2.0**: Globaler Sanitizer-Lauf über alle Artikel (YAML/H1-Sync).

### Infrastruktur & Tools (Jan/Feb 2026)
- **Das Orakel**: Einführung der semantischen Suche (RAG) auf Basis von Jina v3.
- **Automatisierung**: Scripts für Statistiken, Link-Weben und Hardware-Tuning.

---
*Zuletzt aktualisiert: 13.02.2026 durch Antigravity (Enhanced Documentation)*
