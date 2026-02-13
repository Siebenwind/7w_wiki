## 2026-02-13 | Batch 19 Ingestion: Spielergeschichten

**Quellentyp:** Spielergeschichte | **Epistemik:** #perspektive

### Verarbeitete Dateien
`Der Flug der Ente..md` (Konsolidiert)
`Aus dem Liebesleben eines Dichters | Siebenwind | Ultima Online Freeshard | Siebenwind.md`
`Blutschwert | Siebenwind | Ultima Online Freeshard | Siebenwind.md`
`Briefe aus der Ferne.md`
`Das Ende der Zeit der Könige | Siebenwind | Ultima Online Freeshard | Siebenwind.md`

### 📋 Entity Manifest (Batch 19)

#### 👤 PERSONEN
| Name | Rolle/Titel | Quelle | Im Register |
|---|---|---|---|
| Tintin (Waljakov) | Schiffsbauer / Ventus-Priester | Flug der Ente | ✅ |
| Vencurius | Erzpriester des Ventus | Flug der Ente | ✅ NEU |
| Telandrion | Diener des Ignis | Flug der Ente | ✅ NEU |
| Haldur Toda | Dichter / Autor | L. eines Dichters | ✅ (Erweitert) |
| Madame Lafayette | Gönnerin | L. eines Dichters | ✅ NEU |
| Veridon (Nebelklinge) | Assassine / Bellum-Geweihter | Blutschwert | ✅ (Lore-Fix) |
| Herzog Blutschwert | Anführer Schwarze Legion | Blutschwert | ✅ NEU |
| Ilja | Kräuterfrau | Blutschwert | ✅ NEU |
| Rajka Sanseha | Schneiderin | Bri. a. d. Ferne | ✅ NEU |
| Taleris Kreytz | Magister Magus Emeritus | Bri. a. d. Ferne | ✅ NEU |
| William Mercator | Laie (Astrael) | Bri. a. d. Ferne | ✅ NEU |
| Zoran Gosh | Abt von Gofilm | Zeit d. Könige | ✅ NEU |
| Telophas v. Basarius | Eminenz / Rector | Zeit d. Könige | ✅ NEU |
| Ignaz Moravio | Hochgeweihter / Inquisitor | Zeit d. Könige | ✅ NEU |
| Hubertus Anverita | Aspirant / Agent | Zeit d. Könige | ✅ NEU |
| Calmexistus Salanus | Inquisitor / Defensor Fidei | Div. | ✅ (Ring-Lore) |

#### 🏰 ORGANISATIONEN
| Name | Typ | Quelle | Im Register |
|---|---|---|---|
| Ecclesia | Religiöse Gemeinschaft | Div. | ✅ |
| Oculus Ecclesiae | Geheimbund d. Kirche | Blutschwert | ✅ NEU |
| Schwarze Legion | Militärische Kult-Einheit | Blutschwert | ✅ NEU |
| Königliche Akademie | Bildungseinrichtung | Bri. a. d. Ferne | ✅ |
| Ring des Argionemes | Astraelitischer Geheimbund | Zeit d. Könige | ✅ NEU |
| Bruderschaft Gofilm | Mystische Astrael-Gruppe | Zeit d. Könige | ✅ NEU |

#### 🗺️ ORTE
| Name | Typ | Quelle | Wiki-Artikel |
|---|---|---|---|
| Säulenmeer | Maritime Anomalie | Flug der Ente | ✅ NEU |
| Vandrien | Region (Festland) | Blutschwert | ✅ |
| Pas | Stadt/Festung | Blutschwert | ✅ |
| Klauenberge | Gebirge | Blutschwert | ✅ |
| Hügelau | Insel | Blutschwert | ❌ STUB |

#### 🐉 BESTIARIUM
| Name | Typ | Quelle | Wiki-Artikel |
|---|---|---|---|
| Klauenwölfe | Intelligentes Wolfsvolk | Blutschwert | ✅ NEU |

### Aktionen
- **Dateisystem:** Redundante Dubletten `Der Flug der Ente1.md` und `Der Flug der Ente..3.md` gelöscht.
- **Wiki-Produktion:** Profile für `Vencurius` und `Telandrion` erstellt. Erzählseite `Der_Flug_der_Ente` und Geografieseite `Saeulenmeer` angelegt.
- **Register-Synchronisation:** Personenregister um Vencurius und Telandrion erweitert.

---

# Ingestion Log

Chronologisches Protokoll aller verarbeiteten Quellen und der daraus abgeleiteten Wiki-Änderungen.
Jeder Eintrag dokumentiert: **Wann** wurde **was** aus **welcher Quelle** extrahiert und **wohin** geschrieben.

---

### 2026-02-13 | Detail-Ingestion: Briefe aus der Ferne
**Quelle:** `Briefe aus der Ferne.md` | **Quellentyp:** Spielergeschichte | **Epistemik:** #perspektive

#### Aktionen:
- **Wiki-Produktion:** Erzählseite `Briefe_aus_der_Ferne` in `/09_Bibliothek/` angelegt.
- **Profil-Update:** `Solice_Aurora.md` um Hintergrund als Adepta und Details zur Wahrnehmung ihres Weggangs erweitert.
- **Register-Check:** Rajka Sanseha, Taleris Kreytz und William Mercator wurden im Personenregister verifiziert (bereits vorhanden).

---
### 2026-02-13 | Detail-Ingestion: Das Ende der Zeit der Könige
**Quelle:** `Das Ende der Zeit der Könige | ... .md` | **Quellentyp:** Spielergeschichte | **Epistemik:** #perspektive

#### Aktionen:
- **Wiki-Produktion:** Erzählseite `Das_Ende_der_Zeit_der_Koenige` in `/09_Bibliothek/` angelegt.
- **Register-Sync (Personen):** 10+ neue Einträge (Hubertus Anverita, Hadrian Lugado, Willibald Puckel, etc.) hinzugefügt. Zoran Gosh und Calmexistus Salanus verifiziert.
- **Register-Sync (Orga):** `Ring_des_Argionemes`, `Bruderschaft_Gofilm` und 4 Elementarmagie-Schulen (Lafays Stab, Swa, Tiefenwald, Malthust) registriert.

---
### 2026-02-14 | Detail-Ingestion: Aus dem Liebesleben eines Dichters
**Quelle:** `Aus dem Liebesleben eines Dichters | ... .md` | **Quellentyp:** Spielergeschichte | **Epistemik:** #perspektive

#### Aktionen:
- **Wiki-Produktion:** Erzählseite `Aus_dem_Liebesleben_eines_Dichters` in `/09_Bibliothek/` angelegt.
- **Profil-Update:** `Haldur_Toda.md` korrigiert (Mutter des Sohnes ist Eleonore, nicht Lafayette) und um Werke erweitert.
- **Register-Sync:** Eleonore, Erdur, Madame Lafayette, Eret und T. im Personenregister hinzugefügt.

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
