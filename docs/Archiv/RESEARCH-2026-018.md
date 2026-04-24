---
layout: wiki_page
title: RESEARCH-2026-018 - Disambiguierung generischer Begriffe Magie und index
category: Archiv
status: resolved
letzter_check: 2026-04-19
---

# RESEARCH-2026-018 - Disambiguierung generischer Begriffe Magie und index

## Forschungsfrage
Wie sollen die verbleibenden generischen Begriffe `Magie` und `index` im aktiven Wiki-Bestand sauber verstanden und konservativ aufgeloest werden, ohne neue Fehlverlinkungen zu erzeugen?

## Fokus
- Terminologie
- Disambiguierung
- Pages-Linkhygiene
- Produktionsfaehige Semantik

## Status
**Fachlich abgeschlossen.** Der Fall entstand aus der Pages-/Repair-Arbeit nach ausgeschoepfter mechanischer Linkbereinigung und wurde ohne Menschvorlage geloest.

## Erwartetes Ergebnis
Eine belastbare Arbeitsmatrix fuer `Magie`- und `index`-Verwendungen, mit der spaetere Technik-/Produktionslaeufe nur noch klar abgesicherte Retargets anfassen.

## Arbeitsmatrix 2026-04-15

Der Oracle-Lauf konnte nicht gegen den lokalen Vektorindex arbeiten, weil das Embedding-Modell nicht im Cache liegt und die Runtime offline bleibt. Diese Matrix ist deshalb eine konservative Triage aus vorhandenen Backlog-Artefakten und gezielten Dateitreffern.

### `Magie`

| Verwendung | Entscheidung | Umgang |
| :--- | :--- | :--- |
| Allgemeine arkane Kraft oder Zauberei | Begriff `Magie` | Im Fliesstext meist Klartext; nur bei Grundlagenbezug auf [[Magie_Grundlagen]] linken. |
| Grundlagenartikel im Fundament | [[Magie_Grundlagen]] | Titel/H1 und klare Selbstbezuege duerfen nicht `index` bleiben. |
| Akademische Toran-Dur-Definition | [[Magietheorie_Toran_Dur]] oder [[Die_Magie_(Toran_Dur)]] | Nur bei explizitem Bezug auf Toran Dur, Flux, Astrales Netz oder das Werk. |
| Konkrete Pfade/Schulen | konkrete Pfad- oder Theorieseiten | Kein generischer Retarget, wenn der Satz bereits eine Schule nennt. |
| Kategorie-Landingpage | `05_Magie/index.md` | Nur Navigation, kein semantisches Fliesstextziel. |

### `index`

| Kontextsignal | Wahrscheinlicher Begriff | Umgang |
| :--- | :--- | :--- |
| Fundament, Axiome, Grundlagen | Fundament/Wissen | `Das_Fundament` oder Klartext, nicht `index`. |
| Sprache, Dialekt, Run, Alt-Linfan | Sprache/Sprachen | Klartext oder bei Run-Bezug [[Die_Sprache_Run]]. |
| Schriften, Manuskripte, Almanache | Werke/Bibliothek | Klartext `Werke`, `Schriften`, `Bibliothek` oder konkrete Werkseiten. |
| Chronik, Zeitalter, Boten-Ausgaben | Geschichte/Chronik | [[Die_Chronik]], [[Geschichte]] oder Klartext nach Satzkontext. |
| Recht, Gericht, Akte, Ordnung | Recht/Ordnung | Nur bei eindeutig juristischem Satz retargeten. |
| Astrales Netz, Mana, Pfade, magisches Wirken | Magie | Klartext `Magie` oder konkrete Magietheorie-Seite. |
| Kategoriezeilen und Navigationsartefakte | Strukturmetadatum | Technician/Production, nicht Lore-Retarget. |
| Rohquellen | Quellenartefakt | Nicht direkt umschreiben. |

### Freigabegrenze

Freigegeben ist nur kontextklare Korrektur. Nicht freigegeben sind pauschale Ersetzungen von index-Platzhaltern, neue Bridge-Seiten fuer `Magie` oder `index`, sowie Umschreibungen von Rohquellen.

## Abschluss 2026-04-19

Die Historian-Frage ist erledigt: Die Semantik-Matrix trennt `Magie` als allgemeinen Begriff von Grundlagen-, Toran-Dur- und Pfadbezug; `05_Magie/index.md` bleibt reine Navigation; `index` wurde als Platzhalterklasse fuer aktive Wiki-Seiten ausgeraeumt. Gezielte Pruefung findet in `docs/Siebenwind_Wiki/` keine exakten Magie-, index- oder WikiLinks-Wikilinks mehr.

Der verbleibende Pages-WARN ist allgemeiner Linkbacklog. Restwarnungen fuer `Magie` oder `WikiLinks` ohne `source_pages` gehoeren in den Resolver-/Technician-Track, nicht in weitere Historian-Inhaltsarbeit.

---
**Siehe auch:** [[Magie_Grundlagen]], [[Research_Board]]
