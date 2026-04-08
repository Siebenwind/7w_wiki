---
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
- `[[Magie]]` als generischer Begriff,
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

## 🏛️ Menschvorlage (nur falls noetig)
Aktuell **nicht noetig**. Eine Menschvorlage entsteht nur dann, wenn der Historiker bei einzelnen Begriffen auf echte Kanonkonkurrenz oder unaufloesbare Mehrdeutigkeit zwischen belastbaren Lesarten stoesst.

---
*Aktiver Historian-Fall auf Basis groesserer fachlicher Unklarheit nach ausgeschoepfter mechanischer Reparatur.*
