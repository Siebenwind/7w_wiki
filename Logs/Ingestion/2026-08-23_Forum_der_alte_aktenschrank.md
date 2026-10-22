---
uuid: 8053aad8-fece-4169-855a-766ade8028ae
title: Ingestion Forum 106975 – Der alte Aktenschrank
created_at: "2026-08-23T22:45:00Z"
report_id: 8053aad8-fece-4169-855a-766ade8028ae
status: completed
---
# 📥 Ingestion Report: Forum – Der alte Aktenschrank

## Metadaten

- **Quelle**: `docs/Quellen/Forum/Geschichten_aus_dem_Spiel/undated_der_alte_aktenschrank.md`
- **Primärziel**: `docs/Siebenwind_Wiki/07_Persoenlichkeiten/Maichellis_Wanderstern.md`
- **Ausgewertet von**: Ingestor / Scanner + quellenkritischer Vergleich
- **Auswertungszeitpunkt (UTC)**: 2026-08-23T22:45:00Z
- **Workflow**: `/ingest_master`
- **Dispatch-Referenzen**: `MSG-2026-0228`, `MSG-2026-0246`, `MSG-2026-0252`
- **Quellentyp**: `#forum #perspektive`, abgeglichen mit `#bote`
- **Dry-Run**: erfolgreich; `forum-draft --apply` scheiterte reproduzierbar, manueller Read-Verify-Write-Pfad
- **Review-Status**: COMPLETED
- **Report-ID**: 8053aad8-fece-4169-855a-766ade8028ae

## Quellenbefund

Zwanzig Beiträge bündeln Maichellis Wanderstern zugeschriebene Marschallberichte, fragmentarische Tagebuchtexte und spätere Rückblicke. Die Sammlung ist nachträglich gerahmt und unterschiedlich belastbar. Datierte Einsatzberichte sind stärker als innere Monologe, bleiben ohne unabhängige Bestätigung aber Forumüberlieferung.

## Entity-Manifest

- **Personen:** Maichellis Wanderstern; Lazalantin; Leaniel Mondlicht; Myrandhir; Larinda Karntus; Hormtosh Wuchthammer; Celedelair; Lucy; Volandur; Custodias; Helfric von Wallenburg; weitere Soldaten, Geweihte und Expeditionsteilnehmer.
- **Organisationen:** Brandensteiner Militär und Marine; Kirche der Viere; Ordo Morsan; Ritterschaft; Nortraven; Akademien; Echsenverbände.
- **Kreaturen:** Il'yatin, Gran und weitere Dämonen; Blutkreaturen; Fischmenschen; Lindwürmer; Elementare; Untote.
- **Orte:** Brandenstein, Finsterwangen, Seeberg, Westhever, Dunquell, Avindhrell, Falkensee, Claiomhs Wacht, Splitterfelsen, Winzerinsel und Ras Altanin.
- **Ereignisse:** Dämonennotstand 28 n.H.; Spähritte und Evakuierungsplanung; Drogenermittlung; Fall Westhevers; Lindwurmabwehr; Ras-Altanin-Expedition.
- **Zeitpunkte:** 7., 8. und 13. Querlar 28 n.H.; weitere teilweise datierte Berichte bis zur Lindwurmkrise um 30 n.H.

## Kollisions- und Quellenvergleich

- Exakte Suche bestätigt `Maichellis_Wanderstern.md` als bestehendes Ziel. Die dokumentierte Runtimeoption `repair --check-collision` fehlt und wurde als `MSG-2026-0249` gemeldet.
- Bote 190 bestätigt den Fall Westhevers und den „Brecher“ als nortravisches Schiff, nicht als Siedlung.
- Die Boten 191, 193 und 194 stützen die Lindwurmkrise; Bote 194 bestätigt die Ras-Altanin-Expedition unter Wandersterns Kommando.
- Die Zuordnung der roten Lindwürmer zwischen Forumbericht und Bote 194 bleibt ungeklärt. Die Forumform „Helfric von Wallenstein“ wurde wegen der höherwertigen Botenform **Helfric von Wallenburg** nicht übernommen.

## Entscheidung und Ergebnis

- **Aktion:** bestehende Personenseite um eine quellenkritische Aktenchronik erweitert.
- **Belastbar übernommen:** Amtsarbeit, militärische Koordination, Ermittlungs- und Expeditionsrolle sowie die durch Boten bestätigten Ereigniskerne.
- **Nicht kanonisiert:** Dämonenfähigkeiten, Anschuldigungen, Motive, offene Kausalitäten und eine nicht gesicherte Lindwurmzuordnung.
- **Historian-Frage:** `MSG-2026-0246`; die Synthese bleibt bis zu einer Antwort bewusst konservativ.
- **Menschliche Eskalation:** nein.

## Raw HTML

- `docs/Quellen/_ARCHIV_ORIGINAL/Forum/Geschichten_aus_dem_Spiel/106975.html`

---
*Report-ID: 8053aad8-fece-4169-855a-766ade8028ae*
