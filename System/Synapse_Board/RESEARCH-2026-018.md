---
layout: wiki_page
title: "Historian-Fall: Disambiguierung generischer Begriffe Magie und index"
category: Synapse Board
id: RESEARCH-2026-018
status: OPEN_HISTORIAN
priority: 4
subject: Disambiguierung generischer Begriffe Magie und index
detected_by: Codex
reward: Pages Integrity +10 / Terminologiehaerte
---

# Historian-Fall: Disambiguierung generischer Begriffe Magie und index

## 🎯 Anlass
Der Fall entstand aus dem Pages-/Linkhygiene-Lauf nach der Statistik- und Resolver-Bereinigung am 2026-04-08. Die mechanischen Korrekturen sind weitgehend ausgeschoepft; der Restbestand besteht nun ueberwiegend aus semantischen Begriffsverwendungen, die nicht blind per Repair aufloesbar sind.

## 🔍 Operative Lage
Der Fall ist **nicht mehr rein technisch**, aber auch **noch keine Menschvorlage**. Die offenen Treffer mischen:
- `Magie` als generischer Begriff,
- `[[index]]` als Platzhalter fuer sehr unterschiedliche Inhalte (Geschichte, Ordnung, Sprache, Bibliothek, Recht, Werk, Bericht),
- einzelne Resolver-/Archivresiduen wie `WikiLinks`, die nicht ueber Inhaltsumschreibung geloest werden sollten.

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
- [ ] Disambiguierungsleitlinie fuer `Magie` als Begriff vs. kanonische Zielseiten
- [ ] Katalog fuer die haeufigsten `index`-Bedeutungen im aktiven Wiki-Bestand
- [ ] Konservative Liste: was operativ ersetzt werden darf und was als normaler Klartext stehen bleiben soll
- [ ] Keine blinde Massenersetzung; nur belastbare semantische Retargets

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
| Kategoriezeilen wie `Kategorie: [[index]] / Baronie` | Struktur-/Kategorieartefakt | Regionsartikel | Technician/Production sollte Kategoriefrontmatter reparieren; kein Lore-Retarget. |
| Rohquellen unter `docs/Quellen/` | Quellenartefakt | Bote 176/179/180/181 | Nicht direkt umschreiben, solange keine hoehere Quelle bestaetigt; Wiki-Derivate separat korrigieren. |

### Konservative Freigaben

- `[[index]]` in `Magie_Grundlagen.md` und `Magietheorie_Toran_Dur.md` darf nicht generisch bleiben; dort ist der Begriff fast durchgehend `Magie`, teils mit Ziel `[[Magie_Grundlagen]]` bzw. `[[Magietheorie_Toran_Dur]]`.
- `[[index]]` in `Linguistik_Übersicht.md` ist ueberwiegend `Sprache`/`Sprachen`; nur Run-spezifische Saetze duerfen auf `[[Die_Sprache_Run]]`.
- `[[index]]` in `Bibliotheks_Register.md` meint je nach Satz `Werke`, `Schriften` oder `Bibliothek`; hier ist Klartext meist sicherer als neue WikiLinks.
- `[[index]]` in Chronik-Indexseiten meint meist `Chronik`, `Geschichte`, `Ausgaben-Index` oder `Berichte`; Navigationsseiten nicht als lorehaltige Zielartikel behandeln.

### Nicht freigegeben

- Keine pauschale Ersetzung von `index` durch `Magie`.
- Keine neue Bridge-Seite `Magie` oder `index` ohne Lifecycle-Metadaten.
- Keine Umschreibung von `docs/Quellen/` als Teil dieser Triage.
- Keine automatische Retarget-Welle ueber die 293 betroffenen Wiki-Dateien ohne Kontextklassifikation.

## 🏛️ Menschvorlage (nur falls noetig)
Aktuell **nicht noetig**. Eine Menschvorlage entsteht nur dann, wenn der Historiker bei einzelnen Begriffen auf echte Kanonkonkurrenz oder unaufloesbare Mehrdeutigkeit zwischen belastbaren Lesarten stoesst.

---
*Aktiver Historian-Fall auf Basis groesserer fachlicher Unklarheit nach ausgeschoepfter mechanischer Reparatur.*
