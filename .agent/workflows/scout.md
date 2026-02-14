---
description: Web-Scouting für News und Shard-Updates (/scout)
---

# Workflow: `/scout` (Netz-Wache)

Dieser Workflow dient der regelmäßigen Prüfung der Siebenwind-Homepage auf neue Nachrichten und technische Updates.

## Schritte

### 1. Aufklärung
- Öffne `https://www.siebenwind.de`.
- Prüfe den Bereich "Aktuell auf Siebenwind".
- Vergleiche die neuesten Titel mit dem Stand in `04_Chronik/OOC_TIMELINE.md`.

### 2. Extraktion
- Wenn neue News vorhanden: Extrahiere den Volltext.
- Nutze `browser_subagent` falls Bilder oder komplexe Tabellen vorhanden sind.
- Nutze `read_url_content` für reinen Text.

### 3. Formatierung
- Erstelle eine neue Datei in `/Quellen/News/[YYYY-MM-DD]_[TITEL].md`.
- Füge den Standard-YAML-Header ein.
- Stelle sicher, dass das Markdown sauber formatiert ist (H2 für Untertitel, korrekte Listen).

### 4. Integration
- **OOC**: Ergänze den Eintrag in `[[OOC_TIMELINE]]`.
- **IC**: Informiere den User über neue Ingestions-Bedürfnisse.

## Beispiel Meta-Daten
```yaml
---
source: https://www.siebenwind.de/...
title: Frohe Weihnachten
date: 2025-12-24
type: News
epistemic: #news
---
```
