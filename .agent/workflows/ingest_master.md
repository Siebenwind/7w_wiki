---
layout: wiki_page
title: "Department: 🏛️ Lore-Archiv (/ingest_master)"
category: Workflow
description: Universeller Master Workflow für Ingestion (Quellen -> Wiki)
---

# Department: 🏛️ Lore-Archiv (/ingest_master)

Dieser Workflow definiert den einzigen autorisierten Prozess, um rohes Wissen (HTML, DOCX, PDF, MD) aus dem `/Quellen/`-Verzeichnis in strukturierte Wiki-Artikel unter `docs/Siebenwind_Wiki/` zu ueberfuehren.

Er kombiniert Lese-, Verifikations- und Schreibprozesse (Read-Verify-Write) und garantiert, dass keine Entitäten übersehen werden.

## Interop-Status
- runtime_commands:
  - `7w_wiki.py advisor`
  - `7w_wiki.py search <query> --source wiki|quellen|all`
  - `7w_wiki.py repair --check-collision "<Name>"`
  - `7w_wiki.py ingest <file>`
  - `7w_wiki.py ingest forum-queue --json`
  - `7w_wiki.py ingest forum-inspect --source <quellen-md> --json`
  - `7w_wiki.py ingest forum-draft --source <quellen-md> --action update|create --target <wiki-md> --dry-run|--apply --json`
  - `7w_wiki.py ingest forum-finalize --source <quellen-md> --target <wiki-md> --report <report-md> --status integrated --json`
  - `7w_wiki.py ingest reports-calibrate --dry-run|--apply --json`
  - `7w_wiki.py mail inbox --status OPEN`
  - `7w_wiki.py mail post --from Ingestor --to <agent|ALL> --subject "<text>" --body "<text>"`
  - `7w_wiki.py archive sync`
- method_only:
  - `/ingest_master`
- interop_note: Method workflow for ingestion discipline; dispatch stays mandatory via inbox, question-first escalation, and status heartbeats.

## 1. Sichtung & Klassifizierung (Screening)
// turbo
1. Öffne die [INVENTUR_QUELLEN.md](../../Logs/INVENTUR_QUELLEN.md) und wähle eine Datei mit Status "Pending".
   - Wenn du noch keine Quelle hast und gezielt neue Forenquellen finden musst, starte mit `/forum_search`.
2. Bestimme die Epistemik (Wahrheitsgehalt):
   - `/Quellen/Hintergrund/` -> `#canon` (🥇 Absolut)
   - `/Quellen/Zeitung 7w Bote/` -> `#bote` (🥈 Hoch)
   - `/Quellen/Bibliothek/` -> `#überlieferung` (🥉 Mittel)
   - `/Quellen/Spielergeschichten/` -> `#perspektive` (Gering)
3. Prüfe das `/System/Synapse_Board/` auf offene Konflikt- oder Historian-Faelle zum Thema.
4. **Pre-Flight Check (Kollisionsprüfung):**
   Führe `./7w_wiki.py repair --check-collision "Geplanter_Name"` aus, um Duplikate zu vermeiden.

## 2. Ingestion: Der "Read-Verify-Write" Loop

### A. Lesen & Verstehen
Lies den Quelltext. Achte auf Charakter-Motivationen, soziales Gefüge und Atmosphäre (Roman-Qualität).

> **Lange Texte (> 100 Zeilen): Zwei-Pass-Verfahren (PFLICHT)**
> 1. Pass (Struktur-Scan): Text überfliegen, Kapitel und Perspektivenwechsel identifizieren und zusammenfassen.
> 2. Pass (Detail-Scan): Jede Sektion einzeln lesen und das **Entity Manifest** befüllen. Achte besonders auf beiläufig erwähnte Entitäten.

### B. Das Entity Manifest (Pflicht-Scan)
Erstelle für den Chat ein Checklisten-Manifest (*Personen, Organisationen, Kreaturen, Orte, Ereignisse, Zeitpunkte*). 
Gleiche JEDE gefundene Entitaet sofort gegen die aktuellen Wiki-Register ab (z.B. mittels `rg -n "<Entity>" Quellen docs/Siebenwind_Wiki` oder dem Orakel).
Nutze das **Orakel (`./7w_wiki.py search`)** bei Unklarheiten. 

### C. Verifikation (Eskalationsmatrix)
1. **Lokal-Kanon (`#canon`)**: Ist Gesetz.
2. **Quell-Integrität**: Plausibilität innerhalb der Quelle.
3. **Web-Verifikation**: Falls nötig, manuelle Suche auf *siebenwind.de*.
4. **Operativ zuerst**: Wenn die Quelle ohne Streit und ohne groessere Unklarheit verarbeitbar ist, direkt ingestieren oder korrigieren.
5. **Historian nur bei Bedarf**: Route question-first an Historian, wenn groessere fachliche Unklarheit, fehlende Zweitstuetze oder Synthese ueber mehrere Quellenlagen noetig wird.
6. **Mensch nur bei echter Kontroverse**: Nur direkter Quellenwiderspruch, Kanonkorrektur oder konkurrierende belastbare Lesarten gehen an den Menschen.
7. **Fragen statt Raten**: Niemals blind ueberschreiben; `[UNGEKLAERT]` ist erlaubt, wenn keine Eskalation noetig ist.

## 3. Die Produktion (Wiki-Schmied)

Fuer archivierte Forumquellen ist der Runtime-Pfad agentisch:
1. `./7w_wiki.py ingest forum-queue --json` zeigt den Arbeitsvorrat und die empfohlene Aktion.
2. `./7w_wiki.py ingest forum-inspect --source <quellen-md> --json` prueft Zielkandidaten und Risiken.
3. Bei sauberer Lage erstellt oder aktualisiert der Wiki-Schmied einen Draft mit:
   - `forum-draft --action update --target <bestehender artikel> --apply`
   - `forum-draft --action create --target <neuer artikel> --apply`
4. Der Draft ist erst produktionsreif, wenn `./7w_wiki.py check <zielartikel>` und bei Bedarf `./7w_wiki.py lint <zielartikel> --fix` bestanden sind.
5. Der Artikelkoerper wird vor Abschluss in Wiki-Ton gebracht. Quellenkarten-Sprache, sichtbare Archiv-/Registerhinweise und generische Kanonisierungs-Boilerplates sind kein finaler Artikelstil.
6. `forum-finalize` schreibt Registerstatus, Report-Verweis und Integrationsnachweis. Bei `--status integrated` blockiert die Runtime Wiki-Ziele, wenn Pflicht-Frontmatter, H1-Abgleich oder Forum-Ton-Gate fehlschlagen. Nur begruendete Ausnahmefaelle duerfen `--allow-draft-finalize` nutzen.

Neue Wiki-Artikel sind erlaubt, wenn die Quelle volltextarchiviert ist, kein kanonischer Zielartikel existiert, der Gegenstand eigenstaendig genug ist und der Artikel ohne erfundene Lore geschrieben werden kann. Forumquellen behalten eine niedrige epistemische Markierung (`#forum`, `#perspektive`). Menschliche Pruefung ist nur bei echter Kanonentscheidung, unloesbarem Widerspruch oder niedriger Evidenz erforderlich.

Historian-Regel fuer `Geschichten aus dem Spiel`: Die archivierte Metaquelle `docs/Quellen/Forum/Geschichten_aus_dem_Spiel/undated_zweck_dieses_forums.md` dokumentiert, dass dieses Forum seit dem 11. Maerz 2015 fuer tatsaechlich geschehene Spielereignisse vorgesehen ist; rein fiktive Geschichten sollten in einem getrennten Forum stehen. Das hebt einzelne Forumtexte nicht auf #canon, erlaubt aber eine operative Erstannahme als gespielte Ereignisueberlieferung, solange keine hoeherwertige Quelle widerspricht.

Stilregel fuer Forum-Drafts: Der Artikelkoerper bleibt im Wiki-Ton. Technische Hinweise wie "archivierte Forumquelle", Raw-HTML-Status oder Registerlogik gehoeren in Frontmatter, Referenzen und Ingestion-Report, nicht in die Beschreibung. Im Fliesstext werden niedrigere Quellenlagen als "Erzaehlueberlieferung", "weitere Ueberlieferung" oder mit sachlicher Distanz formuliert; die epistemische Markierung bleibt ueber Metadaten sichtbar.

### Forum-Ingestion CLI-Referenz

```bash
./7w_wiki.py ingest forum-queue --json [--status fulltext_archived|integrated] [--limit N]
./7w_wiki.py ingest forum-inspect --source docs/Quellen/Forum/.../<datei>.md --json
./7w_wiki.py ingest forum-draft --source docs/Quellen/Forum/.../<datei>.md --action update --target docs/Siebenwind_Wiki/.../<ziel>.md --dry-run --json
./7w_wiki.py ingest forum-draft --source docs/Quellen/Forum/.../<datei>.md --action create --target docs/Siebenwind_Wiki/.../<neuer_artikel>.md --apply --json
./7w_wiki.py ingest forum-finalize --source docs/Quellen/Forum/.../<datei>.md --target docs/Siebenwind_Wiki/.../<ziel>.md --report Logs/Ingestion/<report>.md --status integrated --json
./7w_wiki.py ingest reports-calibrate --dry-run --json
```

Status- und Aktionswerte:
- `metadata_only`: nur Metadatenquelle vorhanden; zuerst `scout --archive-fulltext` nutzen.
- `fulltext_archived`: Volltext und Raw HTML vorhanden; bereit fuer `forum-inspect`.
- `update_existing`: vorhandener Zielartikel ist wahrscheinlich.
- `create_article`: eigenstaendige Neuanlage ist moeglich.
- `historian_required`: erst agentische Historikerpruefung.
- `human_escalation_required`: nur bei echter Kanonentscheidung.
- `draft_created`: Zielartikel wurde technisch erstellt, ist aber noch nicht produktionsreif.
- `style_review_required`: Lektor-/Wiki-Ton-Gate ist noch offen.
- `ready_to_finalize`: Stil- und Strukturpruefung sind bestanden; `forum-finalize` kann laufen.
- `integrated`: Quelle ist mit Zielseite und Ingestion-Report abgeschlossen.

Nutze die Ingest-Pipeline fuer den technischen Abschluss des bearbeiteten Quelldokuments:
```bash
./7w_wiki.py ingest "docs/Quellen/Zielordner/Datei.md"
```
Diese Pipeline erledigt derzeit:
1. **Linting & Styling:** Wendet den Wiki Style Guide an.
2. **Archive Sync:** Repariert die Index-Symlinks.
3. **Global Audit:** Prüft das Wiki auf Register-Konsistenz.

Wichtig: Ein dokumentierter `--move-to`-Automatismus ist aktuell nicht Runtime-real. Neue oder geaenderte Wiki-Artikel unter `docs/Siebenwind_Wiki/Zielordner` muessen nach dem Read-Verify-Write-Verfahren gezielt erstellt oder aktualisiert werden; die Quelle bleibt der nachvollziehbare Beleg, nicht automatisch kanonisierte Lore.

## 4. Abschluss & Register-Synchronisation
Nach dem `--ingest`:
1. **Register nachziehen**: Fuer Forumquellen erledigt `forum-finalize` das Quellenregister; fachliche Register wie `Personenregister.md` oder Organisationsseiten werden nur aktualisiert, wenn der neue Inhalt dies verlangt.
2. **Logging [PFLICHT]**: Erstelle in `Logs/Ingestion/` einen Tracking-Report oder nutze den von `forum-draft --apply` erzeugten Report.
   - Trage Metadaten ein: `Auswertungs-ID`, `Ausgewertet von`, `Auswertungszeitpunkt`.
3. **Score-Kalibrierung**: Wenn der Audit `score_cluster` meldet, nutze `./7w_wiki.py ingest reports-calibrate --dry-run --json` und danach `--apply`.
4. **Dispatch-Heartbeat [PFLICHT bei langen Läufen]**: Nach 3-5 Quellen oder bei Blockern einen kurzen Statusbericht via `./7w_wiki.py mail post` senden.
5. **Dashboard-Aktualisierung**: Aktualisiere lesbare Statusflaechen nur dann, wenn sichtbarer Archivbestand oder Veroeffentlichungen geaendert wurden.
6. **Inventar Update**: `Logs/INVENTUR_QUELLEN.md` bleibt fuer Altbestand relevant; fuer Forumquellen ist `.agent/data/forum_scan_register.json` der operative Status.
7. **Git Commit**: Committe die Arbeit präzise (`Wiki-Processing: [Dateiname] integriert`).

#ingestion #produktion #master
