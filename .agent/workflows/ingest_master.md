---
description: Department Master Workflow für die Ingestion (Quellen -> Wiki)
---

# Department: 🏛️ Lore-Archiv (INGEST)

Dieses Department ist für die Transformation von rohem Wissen in strukturierte Wiki-Artefakte verantwortlich. Es fusioniert die Workflows `/ingestion_protocol`, `/batch`, `/wiki_process` und `/rvw_loop`.

## Interop-Status
- runtime_commands:
  - `7w_wiki.py advisor`
  - `7w_wiki.py search <query> --source all`
- method_only:
  - `/ingest_master`
  - `/ingestion_protocol`
  - `/batch`
  - `/wiki_process`
  - `/rvw_loop`

## 1. Sichtung (Screening)
- [ ] **Inventur-Check**: Öffne `INVENTUR_QUELLEN.md` und wähle eine `Pending` Quelle.
- [ ] **Epistemische Klassifizierung**: Bestimme den Status (#canon, #bote, #überlieferung, #perspektive).

## 2. Extraktion (Das Zwei-Pass-Verfahren)
Um 100% Detail-Tiefe zu garantieren, ist dieses Verfahren bei jedem Text > 100 Zeilen verpflichtend:

### Pass 1: Struktur-Scan
Überfliege den Text. Identifiziere Sektionen, Zeitabschnitte und Perspektiven. Erstelle eine grobe Zusammenfassung.

### Pass 2: Detail-Scan (Entity Manifest)
Extrahiere **jede** namentlich genannte oder implizite Entität.
- **Personen**: Name, Titel, Amt, Kontext.
- **Organisationen**: Gilden, Orden, militärische Einheiten.
- **Geografie**: Städte, Gebäude, Landmarken, Distanzen.
- **Bestiarium**: Flora, Fauna, magische Wesen.
- **Lore-Bits**: Bräuche, Redewendungen, Gerüchte, Kleidung.

## 3. Verifizierung (Kanon-Abgleich)
1. **Lokal-Kanon**: Prüfe gegen `/Quellen/Hintergrund/`.
2. **Web-Audit**: Nutze das **[Orakel]** (`/7w_wiki.py search`) für Ergänzungen.
3. **Konflikt-Trigger**: Bei Widersprüchen zwingend ein Ticket auf dem **Synapse Board** anlegen.

## 4. Produktion (Wiki-Schmied)
- [ ] **UUID & Frontmatter**: Generiere Metadaten. `report_id` ist Pflicht!
- [ ] **Relative Pfade**: Nutze ausschließlich relative Links zu Quellen und anderen Artikeln.
- [ ] **Roman-Qualität**: Erzeuge atmosphärische, dichte Texte ("Show, don't tell").

## 5. Synchronisation
- [ ] **Register-Updates**: Trage neue Entitäten in `Personenregister.md`, `Organisationsregister.md`, etc. ein.
- [ ] **Chronik-Update**: Verknüpfe Ereignisse mit der globalen Zeitlinie.

#ingestion #extraktion #kanon #produktion
