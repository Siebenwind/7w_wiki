# Siebenwind Lore Engine

Das zentrale Archiv der Siebenwind-Welt. Fokus auf Quellentreue, Konsistenzprüfung und semantische Vernetzung.

## Projekt-Übersicht

Dieses Wiki dient als technischer Knotenpunkt für die Rekonstruktion und Bewahrung der Siebenwind-Lore. Es konsolidiert über 20 Jahre In-Game-Geschichte, Bote-Archive und Spieler-Interaktionen in einem einheitlichen Markdown-Format.

---

## Architektur & Komponenten

| Komponente | Funktion | Dokumentation |
| :--- | :--- | :--- |
| **Ingestion** | Verarbeitung von Boten & Quellen | [Wiki-Inhalte](Siebenwind_Wiki/index.md) |
| **Orakel** | Semantische RAG-Suche | [Setup RAG](setup_rag.md) |
| **Integrity** | Konsistenz-Audit (Trias Politica) | [Architektur](architecture.md) |
| **Status** | Aktuelle Meilensteine | [Master Task List](MASTER_TASK_LIST.md) |

---

## Nutzung & CLI

Die Lore-Engine wird primär über das `7w_wiki.py` Tool gesteuert:

```bash
# Suche im Lore-Bestand
./7w_wiki.py search "Thema"

# Audit der Register
./7w_wiki.py audit
```

---

## Projekt-Metadaten
- **Entwicklung:** LeCorbeau & Siebenwind Gemeinschaft
- **Dokumentation:** [CHANGELOG.md](CHANGELOG.md) | [CONTRIBUTING.md](CONTRIBUTING.md)
- **Lizenzen:** Code (MIT), Inhalte (CC BY-NC-SA 4.0)

*Stand: 2026 | LeCorbeau & Siebenwind*
