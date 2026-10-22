# Das Orakel: Betrieb und Suchumfang

Geprüft am 9. September 2026 gegen die Implementierung. Das Orakel unterstützt interne Recherche. Die öffentliche Wiki-Suche verwendet unabhängig davon Pagefind; siehe [Betrieb der Leserseiten](Agenten/leserseiten.md).

## Voraussetzungen und Zustand

Die Implementierung verwendet **ChromaDB**, `jinaai/jina-embeddings-v3` für Embeddings und `BAAI/bge-reranker-v2-m3` für die Nachsortierung. Die Web-Abhängigkeiten in `requirements.txt` installieren die ML-Umgebung nicht. Die derzeitige Paketliste steht nur im historischen `.agent/skills/oracle/setup.sh`; eine eigenständige fest versionierte ML-Abhängigkeitsdatei fehlt. Modellgewichte, passendes Torch und ausreichend Speicher sind erforderlich. Das historische Skript ist keine zulässige ausführbare Agentenschnittstelle.

Die bekannte Oracle-Störung wird in **MSG-2026-0245** separat verfolgt. Eine erfolgreiche Pages-Prüfung bestätigt keine funktionsfähige Oracle-Umgebung. Vor einem Wiederaufbau zuerst den Zustand prüfen:

```bash
./7w_wiki.py index --status
./7w_wiki.py --help-json
```

Der Indexstatus erzeugt auch das Archivregister unter `System/Archivregister/`. Gerätewahl und Batchgröße liegen in `.agent/config/runtime.json`; `.agent/skills/oracle/config.json` bleibt ein Legacy-Override. Ein kanonischer automatisierter Installer für die gesamte ML-Umgebung fehlt derzeit. Seine Reparatur und reproduzierbare Einrichtung gehören zum Oracle-Auftrag.

## Recherche

```bash
./7w_wiki.py search "Magiegesetze" --source wiki
./7w_wiki.py search "Alte Schlachtberichte" --source quellen
./7w_wiki.py search "Die Entwicklung der Magie" --source all
```

`wiki` durchsucht abgeleitete Artikel, `quellen` den Rohbestand, `all` beide. Bei Widersprüchen gilt **Homepage > Quellen > Wiki Pages**. Weder Trefferreihenfolge noch Tags beweisen die Wahrheit einer Aussage. Bei Ausfall die Quellen unmittelbar lesen und die Einschränkung im Forschungsbericht dokumentieren.

Ein Indexaufbau erfolgt nach reparierter Umgebung über `./7w_wiki.py index --rebuild`. Laufzeit und Speicherbedarf hängen vom Bestand und Gerät ab.
