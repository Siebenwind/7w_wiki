# 📜 SY_STANDARDS (Archivar-Kodex)

**UUID:** b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e

Hier werden alle verbindlichen Verfahrensempfehlungen, Ingestion-Standards und technischen Normen für das Siebenwind-Wiki dokumentiert.

## 🛠 Aktuelle Standards

### Standard 2026-001: Die Goldene Dokumentationspflicht
- **UUID**: Jedes neue Dokument (Wiki, Report, Board-Ticket) braucht eine UUID-v4.
- **Zeitstempel**: ISO-8601 (YYYY-MM-DDTHH:MM:SSZ) ist zwingend.
- **Zitate**: Zitate aus Quellen müssen in Blockquotes stehen, gefolgt von der Quellen-Referenz.
- **Mission**: Fokus auf das kollektive Erbe von Spielern und Stafflern.

### Standard 2026-003: Silicon Inquisition (Parallel-Archiv)
- **Zweck**: Dokumentation AI-interner Zweifel und proaktiver Lore-Aufbau.
- **Tagging**: Hypothesen müssen mit `#user_speculation` oder `#ai_theory` markiert sein.
- **Administration**: Rein AI-gesteuert, aber für den User (Mensch) transparent lesbar.

### Standard 2026-004: Archiv-Hygiene (Changelog)
- **Sortierung**: Das Changelog (`CHANGELOG.md`) wird strikt in **umgekehrt chronologischer** Reihenfolge geführt.
- **Struktur**: Nutzung von `<details>` Tags für alle historischen Einträge, um die Scannability zu erhalten.
- **Aktualität**: Der Header muss das Format `[YYYY-MM-DD.Version]` enthalten.

## 📠 Interface-Spezifikation (Nutzung der Boards)

| Board | Aktion durch Agent | Erwartetes Ergebnis |
|---|---|---|
| **SY_REVIEW** | Ticket erstellen bei Abschluss komplexer Ingestions. | Zweitmeinung durch anderen Agenten. |
| **SY_STANDARDS** | Vorschlag neuer Regeln/Skripte einreichen. | Dokumentation der Evolution des Systems. |
| **SY_INTEROP** | Verbindliche Interoperabilitätsnorm für Workflows/CLI/Boards pflegen. | Reduzierte Onboarding-Reibung und weniger Drift. |
| **SY_WORKFLOW_CLI_MATRIX** | Workflow-zu-CLI Adapter und Ausführbarkeit pflegen. | Klare Brücke zwischen Doktrin und Runtime. |
| **PRODUCTION_PROTOCOL** | Persistente Ablage von Schlussfolgerungen, Ideen, Artworks und Dossiers. | Keine flüchtigen Ergebnisse, volle Nachvollziehbarkeit. |
| **SY_DISPATCH** | Agent-zu-Agent Auftraege senden, claimen und abschliessen. | Nachvollziehbare Multi-Agent-Koordination. |
| **SY_BULLETIN** | Zusammenfassung von Meilensteinen posten. | Übersicht für den User (Highlight-Reel). |
| **Synapse-Board** | Lore-Konflikte (Level-1/2) melden. | Entscheidungsgrundlage für den User. |
| **Inquisition** | Kritische Fragen & Lore-Gaps dokumentieren. | Wissensaufbau im Verborgenen. |

## ⚖️ Mensch-KI-Dialektik (Zuständigkeit)
- **Mensch (Rank 0)**: Letzte Instanz für Kanon (#canon), Vision und strategische Prioritäten.
- **KI (Partner)**: Analyse, Strukturierung, Konsistenzprüfung und kreative Lore-Konstruktion in "weißen Flecken".

---
*Änderungen an diesem Dokument müssen über den Koordinator (Logistik) laufen.*
