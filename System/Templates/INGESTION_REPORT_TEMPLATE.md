# 📥 Ingestion Report: [DATEINAME / BATCH]

## Metadaten
- **Auswertungs-ID**: [UUID-v4]
- **Quelle**: [Relativer Pfad zur Urquelle]
- **Dokument-Fingerprint**: [optional: SHA1/SHA256 der Quelle]
- **Ausgewertet von**: [Agentenname]
- **Auswertungszeitpunkt (UTC)**: [ISO-8601 mit `Z`]
- **Workflow/Skill**: [`/ingestion_protocol`, `/batch`, Skillname]
- **Dispatch-Referenz**: [MSG-YYYY-NNNN | `N/A`]
- **Quellentyp**: [#canon | #bote | #überlieferung | #perspektive]
- **Lore-Score (LQS)**: 0.0/10
- **Quality-Profil (A/T/K/B/U)**: 0/0/0/0/0
- **Review-Status**: [IN_PROGRESS | COMPLETED | NEEDS_REVIEW]

## 📊 Lore Quality Score (LQS)
| Kriterium | Score (0-5) | Notiz |
|---|---|---|
| **A: Abdeckung** | 0 | Vollständigkeit der Entitäts-Extraktion |
| **T: Tiefe** | 0 | Motivation, Atmosphäre, Kausalität |
| **K: Kanon-Konsistenz** | 0 | Widerspruchsfreiheit zum Bestandskanon |
| **B: Belegqualität** | 0 | Präzision und Nachvollziehbarkeit der Quellenbezüge |
| **U: Unsicherheitsdisziplin** | 0 | Offene Punkte sauber als `[UNGEKLÄRT]` / Frage markiert |
| **Rohscore (0-25)** | **0** | Summe A+T+K+B+U |
| **Gesamt (LQS 0-10)** | **0.0/10** | `round(Rohscore * 10 / 25, 1)` |

> Bewertungsregel: Nur mit Notiz je Kriterium bewerten. Bei fehlender Evidenz max. `2`.

## 📋 Extraktions-Ergebnisse

### 👤 Personen
| Name | Status | Ziel-Datei | Confidence | Notiz |
|---|---|---|---|---|
| [Name] | [NEU/UPDATE] | [[Wiki_Link]] | [0-10] | [Kurzer Kontext] |

### 🏰 Organisationen
| Name | Status | Ziel-Datei | Confidence | Notiz |
|---|---|---|---|---|
| [Name] | [NEU/UPDATE] | [[Wiki_Link]] | [0-10] | [Zweck/Typ] |

### 🗺️ Orte / 🐉 Bestiarium / 🔮 Konzepte
| Name | Kategorie | Status | Wiki-Link | Notiz |
|---|---|---|---|---|
| [Name] | [Ort/Wesen/...] | [NEU/UPDATE] | [[Wiki_Link]] | [Details] |

## 🧠 Lore-Audit & Narrative Highlights
- **Wichtigste Erkenntnisse**: [Was lernt die Engine Neues über die Welt?]
- **Inkonsistenzen**: [Gefundene Widersprüche & deren (geplante) Auflösung]
- **Highlight**: [Besonders wertvolle "Insel-Lore" für das Narrative Enrichment]
- **Offene Fragen an Spezialisten**: [Falls vorhanden: Historian/Guardian/Technician + Dispatch-ID]

---
*Report-ID: [UUID-v4]*
*Tracking-Hinweis: Nach Abschluss `./7w_wiki.py stats` ausführen, damit das zentrale Register aktualisiert wird.*
