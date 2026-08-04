---
title: "Statusbericht: Forum-Ingestion und Projektbacklog"
category: Meta
created_at: 2026-08-04T16:46:00Z
status: current
epistemic: "#meta"
---

# Statusbericht: Forum-Ingestion und Projektbacklog

**Stand:** 4. August 2026

## Kurzfazit

Die Forum-Ingestion ist vom Pilotbetrieb in einen stabilen Serienprozess übergegangen. Von **201 registrierten Forumthemen** sind **60 als Volltext archiviert**. Davon sind **59 fachlich abgeschlossen**: **54 wurden in das Wiki integriert**, fünf wurden bewusst ohne Wikiänderung archiviert. Nur ein bereits volltextarchivierter Fall ist noch nicht ausgewertet. Der mengenmäßig größte Forumrest besteht damit aus **141 Metadatensätzen**, deren Volltexte noch archiviert und anschließend gesichtet werden müssen.

Parallel ist die technische Wiki-Basis stabil: Der Audit meldet keine Konsistenzprobleme, 32 erfasste Testsuiten sind grün und der Veröffentlichungsbaum weist keinen technischen Drift auf. Der größte andere Arbeitsblock ist nicht mechanisch, sondern semantisch: **624 ungelöste Linkziele**, von denen 611 Historikerentscheidungen benötigen.

## Forum-Ingestion

| Zustand | Themen | Anteil am Register |
| :--- | ---: | ---: |
| Registriert | 201 | 100,0 % |
| Volltextarchiviert | 60 | 29,9 % |
| Fachlich abgeschlossen | 59 | 29,4 % |
| In das Wiki integriert | 54 | 26,9 % |
| Geprüft, keine Wikiänderung | 5 | 2,5 % |
| Volltext offen | 1 | 0,5 % |
| Nur Metadaten vorhanden | 141 | 70,1 % |

Unter den 59 abgeschlossenen Volltexten führten **91,5 %** zu einer Wikiintegration. **8,5 %** wurden nach Prüfung bewusst nicht in neue oder bestehende Artikel übernommen. Es gibt keine Themen in den Zwischenzuständen `triage_ready`, `draft_created`, `style_review_required` oder `ready_to_finalize` und keine registrierten Fehler oder Dubletten. Die bereits archivierte Arbeitswarteschlange ist damit zu **98,3 %** abgearbeitet.

Seit dem Pilotstand mit zwei integrierten Themen ist der Bestand auf 54 Integrationen gewachsen. Der nächste vorgemerkte Metadatenkandidat ist Topic `104857`, **„Der Morgen danach“**. Vor seiner historischen Auswertung muss zunächst der Volltext archiviert werden. Der einzige bereits volltextarchivierte und noch nicht ausgewertete Fall ist Topic `31020`, **„Hintergrundexkurse“**.

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
- Die fünf neuen HTML-Dateien unter `docs/Quellen/_ARCHIV_ORIGINAL/Forum/` sind keine Buildartefakte, sondern die maßgeblichen Rohquellen der bearbeiteten Forumthemen.
- Die sachfremde unversionierte Dispatchdatei `MSG-2026-0199_yen_usd_carry_trade_dossier_recherchiert.md` gehört nicht zum Siebenwind-Arbeitsblock und bleibt außerhalb des Commits.

## Empfohlene Reihenfolge nach dem Commit

1. Aktuellen Historiker- und Statusstand pushen.
2. Forumscan auffrischen und die nächsten Metadatenkandidaten ab Topic `104857` volltextarchivieren.
3. Die beiden fertigen Historikerreviews `RESEARCH-2026-004` und `RESEARCH-2026-007` schließen.
4. `RESEARCH-2026-018` als semantische Arbeitslane für den Pages-Backlog fortsetzen.
5. Die zwei ausstehenden Newsquellen integrieren.
