---
title: "Statusbericht: Forum-Ingestion und Projektbacklog"
category: Meta
created_at: 2026-08-04T16:46:00Z
updated_at: 2026-08-04T17:15:00Z
status: current
epistemic: "#meta"
---

# Statusbericht: Forum-Ingestion und Projektbacklog

**Stand:** 4. August 2026

## Kurzfazit

Die Forum-Ingestion ist vom Pilotbetrieb in einen stabilen Serienprozess übergegangen. Von **201 registrierten Forumthemen** sind **101 als Volltext archiviert**. Davon sind **59 fachlich abgeschlossen**: **54 wurden in das Wiki integriert**, fünf wurden bewusst ohne Wikiänderung archiviert. Nach der jüngsten fehlerfreien Archivierung von 41 weiteren Themen warten **42 Volltexte auf fachliche Sichtung**. Weitere **100 Metadatensätze** müssen noch volltextarchiviert und anschließend gesichtet werden.

Parallel ist die technische Wiki-Basis stabil: Der Audit meldet keine Konsistenzprobleme, 32 erfasste Testsuiten sind grün und der Veröffentlichungsbaum weist keinen technischen Drift auf. Der größte andere Arbeitsblock ist nicht mechanisch, sondern semantisch: **624 ungelöste Linkziele**, von denen 611 Historikerentscheidungen benötigen.

## Forum-Ingestion

| Zustand | Themen | Anteil am Register |
| :--- | ---: | ---: |
| Registriert | 201 | 100,0 % |
| Volltextarchiviert | 101 | 50,2 % |
| Fachlich abgeschlossen | 59 | 29,4 % |
| In das Wiki integriert | 54 | 26,9 % |
| Geprüft, keine Wikiänderung | 5 | 2,5 % |
| Volltext fachlich offen | 42 | 20,9 % |
| Nur Metadaten vorhanden | 100 | 49,8 % |

Unter den 59 abgeschlossenen Volltexten führten **91,5 %** zu einer Wikiintegration. **8,5 %** wurden nach Prüfung bewusst nicht in neue oder bestehende Artikel übernommen. Die bereits archivierte Arbeitswarteschlange ist nach dem großen Quellenlauf zu **58,4 %** fachlich abgearbeitet. Der Archivierungslauf selbst meldete keine Fehler.

Seit dem Pilotstand mit zwei integrierten Themen ist der Bestand auf 54 Integrationen gewachsen. Der jüngste Lauf archivierte 41 neue Volltexte von Topic `48524`, **„Die wahrste Wahrheit über Orken“**, bis Topic `108896`, **„Die Geschichte von Huns Siebzehnrübl“**. Topic `104857`, **„Der Morgen danach“**, wurde wegen seiner bestehenden Dublettenentscheidung korrekt übersprungen. Der nächste zulässige Metadatenkandidat ist Topic `108636`, **„Pflicht“**. Zur offenen Sichtung gehören Topic `31020`, **„Hintergrundexkurse“**, und die 41 neu archivierten Themen.

Die maschinelle Queue-Klassifizierung über alle 201 Registereinträge weist aktuell 33 Fälle als `historian_required`, 27 als `update_existing`, 41 als `create_article` und 100 als `archive_only` aus. Diese Werte sind Routingempfehlungen; sie ersetzen nicht die fachliche Einzelfallprüfung.

## Wirkung auf das Wiki

Der aktuelle Statistiklauf erfasst:

- **1.397 Wikiartikel** mit **203.211 Wörtern** und **13.192 internen Verweisen**,
- **491 Artikel mit aufgelöster Quellenangabe**,
- **95 standardisiert erfasste Ingestion-Berichte**, alle mit vollständigen Tracking-Kernfeldern,
- **93 Berichte mit Lore Quality Score**,
- **590 Personenprofile**.

Die jüngsten Historikerläufe haben nicht nur neue Erzählungsseiten erzeugt. Bestehende Artikel wie `Falkenwall.md`, `Auenelfen.md`, `Avindhrell.md` und `Maichellis_Wanderstern.md` wurden mit höherwertigen Quellen abgeglichen, ergänzt oder von unbelegten Aussagen bereinigt.

## Andere offene Aufträge

### Historiker und Forschung

- **Vier aktive Historikerfälle:** `RESEARCH-2026-017` und `RESEARCH-2026-018` sind offen; `RESEARCH-2026-004` und `RESEARCH-2026-007` besitzen fertige Gutachten und warten auf Abschluss ihres Reviewwegs.
- **Keine menschliche Entscheidung blockiert** aktuell einen Fall.
- **Fünf Themen im Forschungsreservoir:** Ödland, Linari-Matrix, Grünland, Weiße Ära und Hardhaven-Anachronismus.

### Weitere Ingestion

- Zwei offizielle Newsquellen stehen noch auf `pending`: `2025-10-30_Kuerbisschreck.md` und `2025-12-15_Ankuendigung_Dunkeltief.md`.
- Der Forumscan ist für zwei erlaubte Boards veraltet oder fehlt. Vor einer vollständigen Restplanung sollte die Entdeckungsliste aktualisiert werden.

### Pages- und Linkbacklog

- **624** ungelöste Ziele, davon **622** nicht freigestellt.
- **611** benötigen semantische Historikerarbeit.
- **5** sind Konflikte generischer Begriffe.
- **7** besitzen eine sichere exakte und **1** eine sichere Alias-Zuordnung.
- `drift_status = PASS`; es gibt keine getrennten oder widersprüchlichen Wiki-Bäume.
- Die mechanische Reparaturlane plant derzeit keine sicheren automatischen Dateiänderungen. Der Rest ist überwiegend echte Begriffs- und Quellenarbeit.

### Koordination

Die Dispatch-Inbox weist formal 138 offene Nachrichten aus. Diese Zahl entspricht nicht 138 aktuellen Arbeitsaufträgen: Der Bestand enthält zahlreiche ältere Statusmeldungen und Session-Handover. Eine gesonderte Queue-Hygiene bleibt daher sinnvoll.

## Technischer Zustand und Commit-Hygiene

- Audit: **0 Befunde**.
- Tests: **32 PASS**, **0 FAIL** im Statistikstand.
- Pages: Build erfolgreich, `drift_status = PASS`; der bekannte semantische Linkbacklog bleibt sichtbar.
- Bridges: 85 dokumentierte Übergangsseiten, keine ohne erforderliche Ausnahme-Metadaten.
- Keine Buildausgaben sind versioniert. `site/`, virtuelle Umgebungen, Modell- und Vektorcaches, Python-Bytecode sowie `dist/` sind ignorierte Laufzeit- oder Buildpfade.
- Die 51 neuen HTML-Dateien unter `docs/Quellen/_ARCHIV_ORIGINAL/Forum/` sind keine Buildartefakte, sondern die Rohseiten der 41 bearbeiteten Forumthemen; mehrseitige Themen erzeugen mehrere HTML-Dateien.
- Die sachfremde unversionierte Dispatchdatei `MSG-2026-0199_yen_usd_carry_trade_dossier_recherchiert.md` gehört nicht zum Siebenwind-Arbeitsblock und bleibt außerhalb des Commits.

## Empfohlene Reihenfolge nach dem Commit

1. Die 42 offenen Volltexte in kleinen Historikerpaketen sichten; Topic `31020` bleibt der älteste offene Fall.
2. Den Forumscan auffrischen und danach ab Topic `108636` weitere zulässige Metadatenkandidaten volltextarchivieren.
3. Die beiden fertigen Historikerreviews `RESEARCH-2026-004` und `RESEARCH-2026-007` schließen.
4. `RESEARCH-2026-018` als semantische Arbeitslane für den Pages-Backlog fortsetzen.
5. Die zwei ausstehenden Newsquellen integrieren.
