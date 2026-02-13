---
description: Dedizierter Workflow für die Verarbeitung offizieller Kanon-Dokumente (/Hintergrund/)
---

# Workflow: Kanon-Update

Dieser Workflow behandelt die Verarbeitung und Integration von **offiziellen Hintergrunddokumenten** (`/Quellen/Hintergrund/`, Epistemik: `#canon`). Er unterscheidet sich grundlegend vom Standard-RVW-Loop, weil Kanon-Dokumente **nicht verifiziert** werden müssen – sie **sind** die Wahrheit.

## Wann verwenden?
- Neue oder aktualisierte Dateien in `/Quellen/Hintergrund/`
- Homepage-Inhalte (`siebenwind.de`), die als kanonisch bestätigt wurden
- Korrektur bestehender Wiki-Artikel, die dem Kanon widersprechen

## Ablauf

### 1. Kanon-Scan
1. **Lesen:** Lies das Kanon-Dokument vollständig (`view_file`).
2. **Entity Manifest erstellen** (gemäß RVW-Loop Schritt 1.5).
3. **Zwei-Pass-Verfahren** bei Texten > 100 Zeilen.

### 2. Bestandsabgleich (Diff gegen Wiki)
Für **jede** im Manifest identifizierte Entität:

| Frage | Aktion |
|---|---|
| Existiert ein Wiki-Artikel? | → Weiter zu Schritt 3 |
| Existiert **kein** Wiki-Artikel? | → Neuen Artikel erstellen (`#canon`) |
| Existiert ein Artikel mit **anderem** epistemischen Status? | → Artikel **upgraden** (siehe unten) |

### 3. Kanon-Upgrade (Kern-Mechanismus)
Wenn ein bestehender Wiki-Artikel Informationen aus einer niedrigeren Verlässlichkeitsstufe enthält, die nun durch Kanon bestätigt werden:

```
Vorher:  **Epistemischer Status:** #bote
Nachher: **Epistemischer Status:** #canon
```

> [!IMPORTANT]
> Beim Upgrade wird der **Inhalt erweitert**, nicht ersetzt. Die bisherigen Boten-Informationen bleiben erhalten, werden aber durch den Kanon ergänzt. Die `quelle:`-Angabe im Frontmatter wird aktualisiert.

**Upgrade-Regeln:**
1. `#perspektive` → `#canon`: Nur die vom Kanon bestätigten Fakten werden übernommen. Unbestätigte Details werden auf `#perspektive` heruntergestuft oder als Fußnote behalten.
2. `#bote` → `#canon`: Der epistemische Status wird angehoben. Die Boten-Quelle wird als Sekundärreferenz beibehalten.
3. `#überlieferung` → `#canon`: Mythologische Elemente werden als „bestätigt" markiert.

### 4. Widerspruchsbehandlung
Wenn der Kanon einem bestehenden Wiki-Artikel **widerspricht**:

1. **Kanon gewinnt immer.** Der Wiki-Artikel wird korrigiert.
2. Der Widerspruch wird auf dem **Synapse-Board** als Ticket dokumentiert.
3. Falls der Widerspruch unklar ist (z.B. mehrdeutige Formulierung), wird das Ticket auf `AWAITING_USER` gesetzt.
4. **Synapse Alert:** Falls die Kanon-Änderung bestehende Tickets auf dem Board obsolet macht, schließe diese mit Verweis auf den neuen Kanon.
5. **Score Boost:** Erhöhe den `lore_trust` der betroffenen Dokumente auf 9 (Standard-Kanon).

### 5. Register-Synchronisation
- **Personenregister.md**: Neue Personen hinzufügen, bestehende Einträge ggf. mit `#canon` markieren.
- **Organisationsregister.md**: Kanon-bestätigte Organisationen markieren.
- **Bestiarium_Register.md**: Kanon-bestätigte Kreaturen markieren.

### 6. Ingestion Log
Eintrag in `Logs/INGESTION_LOG.md` mit:
- Quellentyp: **Hintergrund**
- Epistemik: **#canon**
- Alle durchgeführten Upgrades und Neuerstellungen

---
**Nutzung:** `/canon_update [Dateiname oder Ordner]`
