# Qualitätskennzahlen richtig einordnen

Aktive Anleitung, geprüft am 21. Oktober 2026. Sie ersetzt das frühere Modell, das erzählerische Ausschmückung als Vertrauensgewinn behandelte. Maßgeblich bleibt [Homepage > Quellen > Wiki Pages](SY_DRIFT_PAGES_CONTRACT.md).

## Historisches Feld `lore_trust`

`./7w_wiki.py score <Datei>` ist **kein rein lesender Prüfbefehl**. Die Implementierung `.agent/scripts/lore_score_manager.py` berechnet einen heuristischen Startwert aus Metadaten und kann `lore_trust` in der Datei ergänzen oder anheben. Höhere vorhandene Werte bleiben erhalten. Die Heuristik prüft weder einzelne Aussagen noch die aktuelle Homepage; auch ein hoher Wert ersetzt keinen Quellenbeleg.

Den Befehl nur bei beauftragter Metadatenpflege ausführen und die Änderung prüfen. Nicht einsetzen, um eine redaktionelle Freigabe oder einen vermeintlichen Wahrheitswert zu erzeugen. Die frühere pauschale Bonusregel für Atmosphäre oder „Roman-Qualität“ gilt nicht mehr.

## LQS in Ingestion-Berichten

Das Berichtsschema bewertet Abdeckung, Tiefe, Konsistenz, Belegqualität und Unsicherheitsdisziplin. Es beschreibt die dokumentierte Bearbeitung, nicht den Wahrheitsgehalt sämtlicher Aussagen im Zielartikel. Für jede Teilwertung ist eine nachvollziehbare Begründung erforderlich; Unsicherheiten und Perspektiven bleiben sichtbar.

`ingest reports-calibrate --dry-run --json` zeigt geplante Profilkorrekturen an. Erst ein ausdrücklich beauftragtes `--apply` verändert Berichte. Eine Kalibrierung ist keine neue Quellenrecherche.

## Leserstatistik

Der Anteil aufgelöster `quelle`-Felder misst Metadatenabdeckung. Linkhäufigkeit misst Vernetzung. Beide Werte sowie LQS und `lore_trust` dürfen nicht als pauschaler Anteil belegter Aussagen oder abgeschlossener fachlicher Prüfungen bezeichnet werden.
