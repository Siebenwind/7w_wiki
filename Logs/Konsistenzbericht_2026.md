# Konsistenzbericht 2026

**Status:** Aktiv
**Letzte Prüfung:** 2026-02-17
**Verantwortlich:** Inquisition & Archiv

## 🚨 Analyse: GitHub vs. Lokal Audit
*Erkenntnisse aus dem `Logs/Github/260127_Logs_from_Action_Built` Vergleich.*

| Metrik | Lokal (`repair.py`) | GitHub (`mkdocs build`) | Differenz |
|---|---|---|---|
| **Fehleranzahl** | 1.568 | 19.349 | +17.781 |
| **Prüfungstiefe** | Regex (Naiv) | MkDocs (Strict + Plugins) | MkDocs valider |
| **Hauptfehler** | Fehlende Dateien | Unresolved References | Identisch |

### Ursachen für die Differenz
1.  **EzLinks Resolver:** Das GitHub-Plugin `mkdocs-ezlinks-plugin` versucht, `[[Dinge]]` aufzulösen. Wenn es scheitert, wirft es eine Warnung. Unser lokales Skript prüft nur grob auf Existenz.
2.  **Striktheit:** MkDocs validiert JEDEN Link, auch in Footern, Headern und komplexen Verschachtelungen.
3.  **Phantom-Links:** Viele Links verweisen auf nicht existierende "Stubs" oder falsch geschriebene Dateinamen (Case-Sensitivity!).

### Empfohlene Maßnahmen
1.  **Stub-Generierung (Massive Fix):** Erstellung leerer "Stub"-Dateien für die Top-1000 fehlenden Begriffe (mit Tag `#stub`).
2.  **Mapping-Korrektur:** `repair.py` muss intelligenter werden und das `ezlinks` Verhalten simulieren (Case-Insensitive Suche).
3.  **Ignore-List:** Bewusstes Ignorieren von reinen "Flavor-Text" Links, die nicht aufgelöst werden müssen.

## 🛡️ Offene Konsistenz-Probleme
*Hier werden Inkonsistenzen zwischen Artikeln, unklare Zeitlinien oder widersprüchliche Lore-Aussagen protokolliert.*

| ID | Eintrag | Art | Beschreibung | Status |
|---|---|---|---|---|
| K-001 | GitHub 404 | Tech | Deployment wirft 404 wegen fehlendem `.nojekyll`. | ✅ Behoben (Pending Push) |
| K-002 | 19k Dead Links | Inhalt | Massive Anzahl toter Wiki-Links in älteren Artikeln. | 🔴 Offen |
| K-003 | Handover Link-Check Regression | Interop | `test --suite all` meldet in `interop-doc-links` einen defekten Link in `.agent/workflows/handover.md` (`../...`). | 🔴 Offen |
| K-004 | Audit Gate Regression | Betrieb | `./7w_wiki.py audit` liefert 1184 Probleme (u.a. `Mirila_Mik_Honigzopf` Duplikat, fehlendes `Althea_Danea` Profil, breite Missing-File-WikiLinks). | 🔴 Offen |

## ✅ Gelöste Probleme
*Archiv der behobenen Inkonsistenzen.*

| ID | Eintrag | Lösung | Datum |
|---|---|---|---|
| T-001 | Absolute Pfade | Workflows | Entfernung aller `file://` Referenzen aus Workflows. | 2026-02-17 |
