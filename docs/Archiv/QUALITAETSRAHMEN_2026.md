---
layout: wiki_page
title: Qualitaetsrahmen 2026
category: Archiv
---

# Qualitaetsrahmen 2026

## Zweck

Dieser Rahmen beschreibt, wie das Siebenwind-Wiki in vier Schritten gepflegt wird:
Ingestion, Bewertung, Bewahrung und Forschung.
Er macht Qualitaetschecks, Verantwortlichkeiten und Review-Rhythmen transparent.

## Prozesskette

### 1) Ingestion
- Ziel: Quellen nachvollziehbar in strukturierte Wiki-Artikel ueberfuehren.
- Mindeststandard:
  - Quellenbezug vorhanden
  - strukturelle Normalisierung erfolgt
  - keine Halluzinationen, Unsicheres klar markiert
- Relevante Kommandos:
  - `./7w_wiki.py sanitize --auto`
  - `./7w_wiki.py check <pfad>`

### 2) Bewertung
- Ziel: Inhaltliche und formale Qualitaet absichern.
- Mindeststandard:
  - Lore Quality Score (LQS) erfasst
  - Stil/Lesbarkeit geprueft
  - Kanonbezug nachvollziehbar
- Relevante Kommandos:
  - `./7w_wiki.py score <datei>`
  - `./7w_wiki.py check <datei>`

### 3) Bewahrung
- Ziel: Aenderungen und Quellenlage langfristig nachvollziehbar halten.
- Mindeststandard:
  - Changelog-Eintrag
  - Session-Memory bei groesseren Serienarbeiten
  - Dispatch-Hinweis fuer Folgeagenten bei offenen Punkten
- Relevante Kommandos:
  - `./7w_wiki.py mail post --from <agent> --to <agent|ALL> --subject "<text>" --body "<text>"`

### 4) Forschung
- Ziel: Offene Lore-Fragen strukturiert klaeren.
- Mindeststandard:
  - Fragestellungen im Research Board oder Dispatch verankert
  - Quellenlage und Konflikte dokumentiert
  - laufender Erkenntnisstand auf einer publizierten Archivseite sichtbar
  - Ergebnis in Artikel und/oder Report rueckgefuehrt
- Relevante Kommandos:
  - `./7w_wiki.py search "<query>" --source wiki`
  - `./7w_wiki.py search "<query>" --source quellen`
  - `./7w_wiki.py mail post --from <agent> --to Historian --subject "<text>" --body "<text>"`

## Publikationspflicht fuer Forschung

Ab April 2026 gilt:

1. Jeder Research-Auftrag auf dem oeffentlichen Board braucht eine veroeffentlichte Zielseite in `docs/Archiv/`.
2. Sobald ein Auftrag substantielle Zwischenergebnisse hat, wird diese Seite aktualisiert.
3. Abschlussreife Ergebnisse werden zusaetzlich als Report, Dossier oder Ergebnisartikel publiziert und von der Forschungsseite aus verlinkt.
4. `Interessante Artikel` und die Startseite zeigen nicht nur Lesetipps, sondern auch aktuelle Forschungsveroeffentlichungen.

Damit bleibt Forschung fuer Leser, Maintainer und Folgeagenten an derselben Stelle sichtbar, statt nur in `Logs/`, Session-Memory oder Dispatch-Nachrichten zu leben.

## Pflichtchecks

- Link/Interop:
  - `./7w_wiki.py test --suite interop-doc-links`
- Basiszustand:
  - `./7w_wiki.py test --suite clean-client-state`
- Registerkonsistenz:
  - `./7w_wiki.py audit`
- Pages-Build:
  - `./7w_wiki.py pages build --strict`

Hinweis: Falls `pages validate` wegen bestehender Audit-Altlasten faellt, ist der Build trotzdem separat zu dokumentieren.

## Review-Rhythmus und Verantwortung

| Rhythmus | Gegenstand | Verantwortlich | Ergebnis |
|---|---|---|---|
| Woechentlich | Interop- und Linkchecks | Technician | Testreports + ggf. Reparaturticket |
| Woechentlich | Fortschritt laufender Research-Seiten | Historian | aktualisierte Archivseiten bei neuen Erkenntnissen |
| Monatlich | Rotation "Interessante Artikel" | Historian + Redaktion | aktualisierte Kurationsliste, Neuveroeffentlichungen + Changelog |
| Monatlich | Ingestion-Tracking und Score-Verteilung | Technician | aktualisierte Statistik + Dispatch-Stand |
| Quartalsweise | UX-/Navigationsreview | Technician + Herold + Coordinator | Entscheidungspaket in `docs/Archiv/REDESIGN_ROADMAP_2026.md` |

## Eskalation und Transparenz

- Bei Unklarheit gilt `/antigravity`: auditieren, dokumentieren, dann handeln.
- Kein stiller Eingriff ohne Changelog-Kontext.
- Offene Punkte werden per Dispatch adressiert, nicht nur lokal notiert.
