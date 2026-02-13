# Ingestion Log

Chronologisches Protokoll aller verarbeiteten Quellen und der daraus abgeleiteten Wiki-Änderungen.
Jeder Eintrag dokumentiert: **Wann** wurde **was** aus **welcher Quelle** extrahiert und **wohin** geschrieben.

---

*Einträge werden chronologisch angehängt (neueste unten).*

## 2026-02-13 | Re-Scan: Spielergeschichten (Batch 1–18)

**Quellentyp:** Spielergeschichte | **Epistemik:** #perspektive

### Gescannte Dateien (18)
`Abweisungen.md`, `Die Nacht des Dunkeltiefs.md`, `Feuerholz für das Dunkeltief.md`, `Dunkeltief- Vänskap.md`, `Ein Abschiedsbrief.md`, `Einer Löwin Traum.md`, `Im Sumpf.md`, `Kriegstagebuch eines Soldaten.md`, `Letzte Vorbereitungen.md`, `Nebel in Brandenstein.md`, `Einsame Ladengedanken.md`, `Geschäftiges Treiben.md`, `Hannibal Thule.md`, `Prüfung und Entsagung.md`, `Ritus, Gebet und Erleuchtung.md`, `Logbuch des Kerkers.md`, `Pueppchens Flucht.md`, `Solfeister Kin.md`

### 📋 Entity Manifest (konsolidiert)

#### 👤 PERSONEN
| Name | Rolle/Titel | Quelle | Im Register |
|---|---|---|---|
| Kregor Arthax Stahlauge | Bragarim-Schützenbart / Rogal | Feuerholz | ✅ |
| William Glaron | Löwenorden-Ritter | Ein Abschiedsbrief | ✅ |
| Sorania | Kriegerin / Dienerin des Einen | Einsame Ladengedanken | ✅ |
| Markus Panscher | Gelehrter / Alchemist | Einsame Ladengedanken | ❌ NEU |
| Waldemar Delarie | Priester / Gefangener | Logbuch des Kerkers | ✅ |
| Hannibal Thule | Jugendlicher in Falkensee | Hannibal Thule | ❌ NEU |
| Kherbal | Soldat / Burg Schwingenwacht | Kriegstagebuch | ❌ NEU |
| Sandholz | Eminenz (Priester) | Letzte Vorbereitungen | ❌ NEU |
| Sandir | Person in Falkensee | Einsame Ladengedanken | ❌ NEU |
| Cardos | Person in Falkensee | Einsame Ladengedanken | ❌ NEU |
| Nurya | Person | Einsame Ladengedanken | ❌ NEU |
| Lucienne | Frau / Ehefrau | Prüfung und Entsagung | ❌ NEU |
| Hektor | Diener der Untoten | Logbuch des Kerkers | ❌ NEU |
| Gorem | Gefangener | Logbuch des Kerkers | ❌ NEU |
| Solfeister Kin | Angamon-Anhänger | Solfeister Kin | ❌ NEU |

#### 🏰 ORGANISATIONEN
| Name | Typ | Quelle | Im Register |
|---|---|---|---|
| Bragarim | Militärische Garde (Dwarschim) | Feuerholz | ✅ |
| Löwenorden | Religiöser Ritterorden | Einer Löwin Traum, Abschiedsbrief | ✅ |
| Nortraven | Kriegergemeinschaft | Dunkeltief-Vänskap | ✅ |
| Ecclesia | Religionsgemeinschaft | div. | ✅ |
| Schattenhand | Unterwelt | Ritus, Gebet | ✅ |
| Blutige Faust | Söldnertruppe | (Von gesplitterten Seelen) | ❌ NEU |
| Magister ad Sinister | Nekromantischer Rang/Orden | Geschäftiges Treiben | ❌ NEU |

#### 🐉 KREATUREN
| Name | Typ | Quelle | Im Register |
|---|---|---|---|
| Ferrin | Rattenmenschen | Im Sumpf, Vänskap | ✅ |
| Gargoyles | Geflügelte Kreaturen | Vänskap | ✅ |
| Harpyien | Geflügelte Kreaturen | Kriegstagebuch | ✅ |
| Sammler | Schlangenwesen / Diener des Einen | Vänskap | ✅ |
| Saran/Saranen | Diener des Einen | Vänskap, Logbuch | ✅ |
| Untote | Reanimierte Tote | div. | ✅ |
| Mehr'thak | Dämon / "der Erzähler" | Ritus, Gebet | ❌ NEU |

#### 🗺️ ORTE
| Name | Typ | Quelle | Wiki-Artikel |
|---|---|---|---|
| Falkensee | Stadt | div. | ✅ |
| Brandenstein | Stadt | Nebel, Pueppchens Flucht | ✅ |
| Seeberg | Stadt | Löwin Traum, Hannibal Thule | ✅ |
| Dwarschim | Zwergenfestung | Feuerholz | ✅ |
| Kesselklamm | Klamm bei Dwarschim | Feuerholz | ✅ |
| Vänskap | Nortraven-Dorf | Dunkeltief-Vänskap | ❌ NEU |
| Westhever | Nortraven-Ort | Dunkeltief-Vänskap | ❌ NEU |
| Burg Schwingenwacht | Festung | Kriegstagebuch | ❌ NEU* |
| Vandrien | Kontinent (Festland) | Prüfung und Entsagung | ❌ NEU |
| Morsanschrein | Tempel | Hannibal Thule | ❌ DETAIL |
| Wolpertinger | Taverne in Falkensee | Hannibal Thule | ❌ NEU |

*Schwingenwacht hat möglicherweise bereits einen Eintrag unter `Burg_Schwingenwacht.md`.

#### 📅 EREIGNISSE
| Name | Typ | Quelle |
|---|---|---|
| Dunkeltief-Belagerung von Vänskap | Militärkonflikt | Dunkeltief-Vänskap |
| Besetzung von Falkensee durch Knochenfürst | Besatzung | Logbuch des Kerkers |
| Putsch in Brandenstein | Politischer Umsturz | Einsame Ladengedanken |
| Zerstörung Brandensteins (gelber Nebel) | Katastrophe | Nebel in Brandenstein |

#### 🔮 KONZEPTE
| Name | Typ | Quelle |
|---|---|---|
| Monolith | Schwarzer Kristall / Sammler-Waffe | Dunkeltief-Vänskap |
| Ru'n | Magische Sprache (Nekromantie) | Geschäftiges Treiben |
| Knochenfürst | Titel / Untoter Herrscher | Logbuch des Kerkers |
| Dorayon | Zeitreferenz (Gestirn?) | Geschäftiges Treiben |

### Aktionen
- **Frontmatter-Fix:** 6 Dateien von `status: Perspektive (Level 4)` → `status: #perspektive` korrigiert
- **Register-Kandidaten (NEU):** 15 Personen, 2 Organisationen, 1 Kreatur, 5 Orte → Backlog

### Notizen
- Längere Geschichten (Khalandra, Jenseits des Walls, Aus dem Leben eines Schwarzmagiers, etc.) wurden in früheren Batches bereits detailliert verarbeitet
- Die Taverne "Wolpertinger" in Falkensee taucht in mehreren Quellen auf – Kandidat für eigenen Artikel
