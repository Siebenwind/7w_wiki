# TASK: HOMEPAGE NEWS ARCHIVE CRAWL

Du bist als **Netz-Wächter** beauftragt, das vollständige News-Archiv der Siebenwind-Homepage zu sichten und zu archivieren.

## 📡 Ziel-URL
- [siebenwind.de/news/](https://siebenwind.de/news/) (oder die entsprechende Archiv-Sektion).

## 🛡️ Dein Kodex
- Reiner Lesezugriff (**Passiver Beobachter**).
- Extraktion aller News-Einträge der letzten Jahre (soweit erreichbar).

## 📝 Deine Arbeitsschritte
1.  **Exploration**: Navigiere zum News-Archiv und identifiziere die Struktur der Links.
2.  **Extraktion**: Für jeden relevanten News-Eintrag:
    - Extrahiere: **Titel**, **Datum**, **Autor** (falls vorhanden) und den **Volltext**.
    - Unterscheide zwischen **IC-Lore** (Geschichten aus dem Shard) und **OOC-News** (Patches, Server-Updates).
3.  **Speicherung**:
    - Erstelle für jeden Eintrag eine Datei in `Quellen/News/YYYY-MM-DD_Titel.md`.
    - Nutze Metadaten für Titel, vorhandenen Autor, Datum, Quell-URL und Abrufnachweis; kein Legacy-`layout`. `docs/Quellen/` ist die Publikationsfläche des Quellenarchivs.
4.  **Chronik-Update**:
    - Füge belegte technische Meilensteine chronologisch in `docs/Siebenwind_Wiki/04_Chronik/OOC_TIMELINE.md` ein.
    - Achte darauf, keine Duplikate zu bereits vorhandenen Einträgen zu erstellen.
5.  **Integration und Abschluss**: Archivierung ist keine automatische fachliche Integration. Übergebe IC-Material an den Ingestionsworkflow; es gilt **Homepage > Quellen > Wiki Pages**. Prüfbericht, bearbeitete Quellen, Zielartikel und offene Fragen über `mail done` oder `mail post` nachweisen.

## 🚀 Spezifischer Auftrag (Kickoff)
Durchsuche die Homepage nach allen News-Artikeln ab dem Jahr 2010. Priorisiere technische Patchnotes und große Lore-Ankündigungen wie "Dunkeltief".

**Sammle das Wissen der Gezeiten!**
