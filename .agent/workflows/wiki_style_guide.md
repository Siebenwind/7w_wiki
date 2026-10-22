---
description: Siebenwind Wiki Style Guide & Convention
---

# Wiki-Stil und Quellenbezug

Aktive Anleitung, geprüft am 21. Oktober 2026. Maßgeblich sind der [Drift-/Pages-Vertrag](../../System/Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md) und der Inhaltsvertrag in `.agent/scripts/content_contract.py`.

## Interop-Status
- runtime_commands:
  - `7w_wiki.py check`
  - `7w_wiki.py sanitize --auto`
- method_only:
  - `/wiki_style_guide`

## Quellen vor Darstellung

Die Präzedenz lautet **Homepage > Quellen > Wiki Pages**. Herkunftstags beschreiben den Belegtyp; sie ersetzen weder den Quellenvergleich noch eine Prüfung einzelner Aussagen. Ein Botenbericht oder eine persönliche Erzählung kann eine Sichtweise belegen, ohne sie zur allgemeingültigen Weltbeschreibung zu machen. Unterschiede in Zeit, Perspektive und Geltungsbereich ausdrücklich erklären. Nicht auflösbare Fragen als `[UNGEKLÄRT]` dokumentieren und über Dispatch weiterführen.

Lesbar und anschaulich schreiben, aber keine Gerüche, Motive, Gefühle oder historischen Details ergänzen, die die Quellen nicht tragen. Stil, Linkhäufigkeit und Scores erzeugen keine neue fachliche Freigabe.

## Metadaten und Überschriften

Artikel liegen unter `docs/Siebenwind_Wiki/`. Reguläre neue Artikel erhalten eine konkrete Quelle und nachvollziehbare Berichtszuordnung. Beispiel mit auszufüllenden Werten:

```yaml
---
uuid: "<UUID-v4>"
title: "<Artikeltitel>"
category: "<Kategorie>"
epistemic: "#bote"
quelle: "../../Quellen/<Unterordner>/<Datei>.md"
report_id: "<ID des Prüf- oder Ingestion-Berichts>"
updated_at: "<ISO-8601-Zeitpunkt>"
---
```

`layout` gehört nicht in neue Wikiartikel. `lore_trust` ist ein historisches, optionales Metadatenfeld und keine Freigabe. YAML-Werte mit `#` in Anführungszeichen setzen. Die H1 stimmt mit `title` überein; H2 gliedern Beschreibung, Geschichte und Quellen. Zusätzliche Felder nur mit belegtem Inhalt verwenden.

Kurze fachliche Metadaten können direkt unter der H1 als Material-Infoblock stehen:

```markdown
!!! info "Metadaten"
    **Zeitraum:** <belegter Zeitraum>
    **Zugehörigkeit:** <belegte Verbindung>
```

Ein vorhandener `report_id` benötigt eine nachvollziehbare Referenz auf den Bericht. Technische Verarbeitungshinweise gehören in Metadaten und Referenzen, nicht in die Orts- oder Personenbeschreibung.

## Gliederung und Verlinkung

Der erste Absatz erklärt ohne Vorwissen, worum es geht. Gegenwärtigen Zustand und historische Beschreibung trennen. Für Orte eignen sich Lage, heutiger Zustand und Geschichte; für Personen Wirken und belegte Beziehungen; für Ereignisse Hintergrund, Verlauf und Folgen. Überschriften nur verwenden, wenn dazu Quelleninhalt vorliegt.

- Wikiartikel mit `[[Seitenname|Lesbarer Titel]]` verlinken; keine verschachtelten WikiLinks in Anzeigetexten.
- Technische Dokumentation repo-relativ verknüpfen, keine lokalen Datei-URLs.
- Quellen über konkrete Referenzen identifizierbar halten; portable Quellpfade können als Code stehen, öffentliche Originalquellen als beschriftete Links.
- Kategorieindizes erhalten ihre redaktionellen Einleitungen zwischen den `BEGIN EDITORIAL`-/`END EDITORIAL`-Markern.
- Fehlende Links zuerst auf bestehende kanonische Ziele heben. Keine generischen Brücken als Reparaturabschluss. Temporäre Ausnahmen benötigen `bridge_mode`, `bridge_target`, `bridge_ticket` und `bridge_review_until`; überfällige Fristen nicht pauschal verlängern.

## Prüfung

`./7w_wiki.py check <Artikel>` prüft Stil und Format; `./7w_wiki.py sanitize` zeigt Vertragsabweichungen. `sanitize --auto` verändert Dateien und ist nur bei beauftragter Korrektur einzusetzen. Quellenabgleich und fachliche Redaktion bleiben zusätzlich erforderlich. Nach Abschluss Änderungen und Prüfbericht über `mail done` beziehungsweise `mail post` dokumentieren.
