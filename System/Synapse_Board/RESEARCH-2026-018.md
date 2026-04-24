---
layout: wiki_page
title: "Historian-Fall: Disambiguierung generischer Begriffe Magie und index"
category: Synapse Board
id: RESEARCH-2026-018
status: DONE
priority: 4
subject: Disambiguierung generischer Begriffe Magie und index
detected_by: Codex
reward: Pages Integrity +10 / Terminologiehaerte
---

# Historian-Fall: Disambiguierung generischer Begriffe Magie und index

## 🎯 Anlass
Der Fall entstand aus dem Pages-/Linkhygiene-Lauf nach der Statistik- und Resolver-Bereinigung am 2026-04-08. Die mechanischen Korrekturen sind weitgehend ausgeschoepft; der Restbestand besteht nun ueberwiegend aus semantischen Begriffsverwendungen, die nicht blind per Repair aufloesbar sind.

## 🔍 Operative Lage
Der Fall ist **fachlich abgeschlossen**. Die ursprünglichen Treffer mischten:
- `Magie` als generischer Begriff,
- index-Platzhalter fuer sehr unterschiedliche Inhalte (Geschichte, Ordnung, Sprache, Bibliothek, Recht, Werk, Bericht),
- einzelne Resolver-/Archivresiduen wie `WikiLinks`, die nicht ueber Inhaltsumschreibung geloest werden sollten.

Stand 2026-04-19: Die Semantik-Matrix liegt vor, alle exakten index-Platzhalter in `docs/Siebenwind_Wiki/` sind bereinigt, und gezielte Pruefung findet dort keine exakten Magie-, index- oder WikiLinks-Wikilinks mehr. Die verbliebenen Pages-Warnungen fuer `Magie` und `WikiLinks` haben leere `source_pages` und gehoeren damit nicht mehr in die Historian-Inhaltsarbeit, sondern in den allgemeinen Pages-/Resolver-Backlog.

## 🧭 Eskalationsklasse
- [x] historian_noetig
- [ ] human_decision_required
- [ ] thematic_backlog

## 📜 Vorhandene Anhaltspunkte (Primärquellen)
- [x] `docs/Siebenwind_Wiki/00_Fundament/Magie_Grundlagen.md`
- [x] `docs/Siebenwind_Wiki/00_Fundament/Magietheorie_Toran_Dur.md`
- [x] `docs/Siebenwind_Wiki/00_Fundament/Bibliotheks_Register.md`
- [x] `docs/Siebenwind_Wiki/00_Fundament/Linguistik_Übersicht.md`
- [x] `docs/Siebenwind_Wiki/03_Gesellschaft/Recht_Siebenwinds.md`
- [x] `docs/Siebenwind_Wiki/01_Pantheon/Astrael.md`

## 🧬 Erwartete Ergebnisse
- [x] Disambiguierungsleitlinie fuer `Magie` als Begriff vs. kanonische Zielseiten
- [x] Katalog fuer die haeufigsten `index`-Bedeutungen im aktiven Wiki-Bestand
- [x] Konservative Liste: was operativ ersetzt werden darf und was als normaler Klartext stehen bleiben soll
- [x] Keine blinde Massenersetzung; nur belastbare semantische Retargets

## 🧠 Historiker-Briefing
Der Technikerlauf hat den rein mechanischen Teil bereits reduziert (`generic_term_conflict` von 15 auf 5; `safe_alias_match` von 4 auf 2). Die verbleibenden Faelle verlangen keine neue Brueckenproduktion, sondern eine begriffliche Ordnung:
- Wann meint `Magie` die allgemeine arkane Kraft?
- Wann ist `Magie_Grundlagen`, `Magietheorie_Toran_Dur` oder eine spezifische Theorie-/Pfadseite gemeint?
- Wann ist `index` nur ein historischer Platzhalter/OCR-Artefakt?
- Wann steht `index` stellvertretend fuer einen echten Begriff wie `Geschichte`, `Recht`, `Bibliothek`, `Ordnung`, `Sprache`, `Werk`, `Wissen` oder `Chronik`?

Der Fall soll eine **arbeitsfaehige Semantik-Matrix** liefern, damit Technician/Production danach konservativ weiterreparieren koennen, ohne neue Fehlverlinkungen zu erzeugen.

## 🧭 Arbeitsmatrix 2026-04-15

Oracle/Historian konnte nicht gegen den Vektorindex laufen, weil das lokale Modell `jinaai/jina-embeddings-v3` nicht im Cache liegt und die Runtime im Offline-Modus bleibt. Die folgende Matrix ist daher eine konservative, dateigebundene Triage aus vorhandenen Board-/Backlog-Artefakten und gezielten Texttreffern, keine neue Vollsynthese.

### `Magie`

| Verwendung | Entscheidung | Operativer Umgang |
| :--- | :--- | :--- |
| Allgemeine arkane Kraft, Zauberei, magisches Wirken | Begriff `Magie` | In Fließtext bevorzugt Klartext `Magie`; nur bei explizitem Grundlagenbezug auf `[[Magie_Grundlagen]]` linken. |
| Grundlagen-/Uebersichtsartikel im Fundament | `[[Magie_Grundlagen]]` | Treffer in `docs/Siebenwind_Wiki/00_Fundament/Magie_Grundlagen.md` sind sehr wahrscheinlich auf `Magie` bzw. den Artikel selbst zu retargeten; H1/Titel duerfen nicht `index` bleiben. |
| Toran-Dur-Theorie als akademische Definition | `[[Magietheorie_Toran_Dur]]` oder Werkartikel `[[Die_Magie_(Toran_Dur)]]` | Nur retargeten, wenn der Satz explizit Toran Dur, Definition des Astralen Netzes, Flux oder das Werk "Die Magie" nennt. |
| Pfade/Schulen | spezifische Seiten wie `[[Weissmagie]]`, `[[Schwarzmagie]]`, `[[Antimagie]]`, `[[Elementarpfad]]` | Nicht auf einen generischen `Magie`-Artikel mappen, wenn der Satz bereits einen konkreten Pfad nennt. |
| Magie-Kategorie/Landingpage | `docs/Siebenwind_Wiki/05_Magie/index.md` bleibt Kategorieindex | Nicht als semantisches Ziel fuer Fließtext verwenden; nur Navigation. |

### `index`

| Kontextsignal | Wahrscheinlicher Begriff | Beispielbefund | Operativer Umgang |
| :--- | :--- | :--- | :--- |
| Fundament/Grundlagen, "Das Fundament", Axiome | Fundament/Wissen | `docs/Siebenwind_Wiki/00_Fundament/Das_Fundament.md` | Auf `Das_Fundament` oder Klartext `Fundament` normalisieren, nicht auf `index`. |
| Sprachen, Dialekte, Run, Alt-Linfan | Sprache/Sprachen | `docs/Siebenwind_Wiki/00_Fundament/Linguistik_Übersicht.md` | Auf Klartext `Sprache`/`Sprachen` oder bei konkretem Bezug `[[Die_Sprache_Run]]`. |
| Schriften, Manuskripte, Almanache, Sagenrollen | Werke/Bibliothek | `docs/Siebenwind_Wiki/00_Fundament/Bibliotheks_Register.md` | Auf Klartext `Werke`, `Schriften`, `Bibliothek` oder konkrete Werkseiten; keine Massenverlinkung. |
| Chronik, Zeitalter, Boten-Ausgaben, Ereignisberichte | Geschichte/Chronik | `docs/Siebenwind_Wiki/04_Chronik/Die_Chronik.md` | Auf `[[Geschichte]]`, `[[Die_Chronik]]` oder Klartext je nach Satz; Boten-Indizes bleiben Navigationsseiten. |
| Recht, Gericht, Akte, Exekutivgewalt, Ordnung | Recht/Ordnung | Treffer in Chronik- und Gesellschaftsartikeln | Nur retargeten, wenn Satz eindeutig juristisch ist; sonst Historian-Pruefung. |
| Magische Theorie, Wirken, Astrales Netz, Mana, Pfade | Magie | `Magie_Grundlagen`, `Magietheorie_Toran_Dur`, Werkartikel unter `03_Wissen/Werke/` | Auf Klartext `Magie` oder konkrete Magietheorie-Seite nach Kontext. |
| Kategoriezeilen wie `Kategorie: index / Baronie` | Struktur-/Kategorieartefakt | Regionsartikel | Technician/Production sollte Kategoriefrontmatter reparieren; kein Lore-Retarget. |
| Rohquellen unter `docs/Quellen/` | Quellenartefakt | Bote 176/179/180/181 | Nicht direkt umschreiben, solange keine hoehere Quelle bestaetigt; Wiki-Derivate separat korrigieren. |

### Konservative Freigaben

- index-Platzhalter in `Magie_Grundlagen.md` und `Magietheorie_Toran_Dur.md` duerfen nicht generisch bleiben; dort ist der Begriff fast durchgehend `Magie`, teils mit Ziel `Magie_Grundlagen` bzw. `Magietheorie_Toran_Dur`.
- index-Platzhalter in `Linguistik_Übersicht.md` sind ueberwiegend `Sprache`/`Sprachen`; nur Run-spezifische Saetze duerfen auf `Die_Sprache_Run`.
- index-Platzhalter in `Bibliotheks_Register.md` meinen je nach Satz `Werke`, `Schriften` oder `Bibliothek`; hier ist Klartext meist sicherer als neue WikiLinks.
- index-Platzhalter in Chronik-Indexseiten meinen meist `Chronik`, `Geschichte`, `Ausgaben-Index` oder `Berichte`; Navigationsseiten nicht als lorehaltige Zielartikel behandeln.

### Nicht freigegeben

- Keine pauschale Ersetzung von `index` durch `Magie`.
- Keine neue Bridge-Seite `Magie` oder `index` ohne Lifecycle-Metadaten.
- Keine Umschreibung von `docs/Quellen/` als Teil dieser Triage.
- Keine automatische Retarget-Welle ueber die 293 betroffenen Wiki-Dateien ohne Kontextklassifikation.

## 🏛️ Menschvorlage (nur falls noetig)
Aktuell **nicht noetig**. Eine Menschvorlage entsteht nur dann, wenn der Historiker bei einzelnen Begriffen auf echte Kanonkonkurrenz oder unaufloesbare Mehrdeutigkeit zwischen belastbaren Lesarten stoesst.

## ✅ Abschluss 2026-04-19

Der Historian-Teil von `RESEARCH-2026-018` ist erledigt. Ergebnis ist keine neue Lore-Behauptung, sondern eine belastbare Arbeitsgrenze:

- `Magie` bleibt im Fliesstext Klartext, solange kein expliziter Grundlagen-, Toran-Dur- oder Pfadbezug besteht.
- `05_Magie/index.md` bleibt eine Navigationsseite und ist kein semantisches Fliesstextziel.
- `index` wurde als Platzhalterklasse aufgeloest; die aktiven Wiki-Seiten enthalten keine exakten index-Wikilinks mehr.
- `WikiLinks` und source-page-leere Restwarnungen sind Technician-/Resolver-Arbeit, nicht Historian-Lore.
- Der verbleibende Pages-WARN (`629` unresolved / `627` unallowlisted im Contract-Lauf vom 2026-04-19) ist der allgemeine Linkbacklog und kein offener Magie/index-Fall.

---
*Abgeschlossener Historian-Fall auf Basis groesserer fachlicher Unklarheit nach ausgeschoepfter mechanischer Reparatur.*
