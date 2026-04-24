# Session Memory: Wissenswerk 2.0 Bootstrap

**Datum:** 2026-04-24  
**Agent:** Codex  
**Fokus:** Wissenswerk-2.0-Plattformkern, Root-Vertraege, generische CLI, Provider-/RagPrep-/Design-Smokes

## Kontext
Der Nutzer hat den Plan fuer Wissenswerk 2.0 zur Umsetzung freigegeben. Der erste Schritt war gemaess Plan, den Auftrag in `MASTER_TASK_LIST.md` zu persistieren und per Dispatch zu melden. `MSG-2026-0148` dokumentiert den Start.

## Umgesetzt
- `wissenswerk.py` als generische Plattform-CLI angelegt:
  - `init`
  - `ingest --from-ragprep`
  - `wiki build`
  - `search`
  - `providers check`
  - `design lint`
  - `bot discord`
- `./7w_wiki.py wissenswerk ...` als Legacy-Kompatibilitaetsbruecke ergaenzt.
- `wissenswerk.yaml` als Siebenwind-Referenztenant mit pgvector-Default, OpenAI-kompatiblen Providerprofilen, RagPrep-Kontrakt, Auto-Apply-Policy und Bot-/Design-Konfiguration angelegt.
- `project_manifest.json` als generisches Wissenswerk-Produktmanifest angelegt; `lore_manifest.json` bleibt Legacy-Export.
- `DESIGN.md` als agentenlesbarer Designvertrag mit JSON-kompatiblem YAML-Frontmatter und Markdown-Rationale angelegt.
- `AGENTS.md`, `System/COORDINATION_HUB.md`, `CHANGELOG.md` und `.agent/config/tools.json` nachgezogen.
- `.agent/catalog/catalog.v1.json` nachgezogen und den Help-JSON-Serializer so korrigiert, dass `argparse.REMAINDER` nicht als Pflichtargument in Tool-Surfaces erscheint.
- `.agent/tests/suites/wissenswerk-contract.json` und `.agent/tests/fixtures/ragprep/sample_chunks.json` als Contract-Smoke und RagPrep-Fixture angelegt.

## Verifikation
- `python3 -m py_compile wissenswerk.py 7w_wiki.py`: PASS
- `./7w_wiki.py test --suite wissenswerk-contract --timeout 60`: PASS, 6/6
- `./7w_wiki.py test --suite tool-manifest-contract --timeout 60`: PASS
- `./7w_wiki.py test --suite catalog-contract --timeout 60`: PASS, 2/2
- `./7w_wiki.py test --suite manifest-contract --timeout 60`: PASS, 2/2
- `./7w_wiki.py test --suite clean-client-state --timeout 60`: PASS, 8/8
- `./7w_wiki.py audit --json`: PASS, `issues_found = 0`
- `./7w_wiki.py wissenswerk ingest --from-ragprep .agent/tests/fixtures/ragprep --json`: PASS, 1 Chunk / 1 Dokument, Report `Logs/Wissenswerk/2026-04-24_172253_ragprep_ingest.json`
- `./7w_wiki.py wissenswerk search Siebenwind --source wiki --top 2 --json`: PASS, lexical bootstrap hits returned

## Nachtrag: Plattformneutralitaet
Auf Nutzerhinweis wurden zusaetzlich `AGENTS.md`, die OpenAI/Codex-Dokumentation zu `AGENTS.md`, Skills, MCP und Subagents sowie die DESIGN.md-Spezifikation geprueft. Ergebnis:

- `AGENTS.md` ist ein offenes agentenuebergreifendes Format und darf nicht als Codex-exklusiver Vertrag behandelt werden.
- Codex-spezifische Skills/Plugins sind nuetzliche Adapter, aber nach aktueller Codex-Dokumentation selbst als ergaenzende Layer neben AGENTS.md, MCP und Subagents gedacht.
- DESIGN.md besteht aus maschinenlesbaren Tokens plus Markdown-Rationale und ist ebenfalls als agentenlesbarer, nicht IDE-gebundener Vertrag geeignet.

Nachgezogen:

- `AGENTS.md`: Wissenswerk als IDE-/Plattform-unabhaengiger Kern festgeschrieben; Codex, Jules, Gemini CLI, Cursor, Aider und weitere Hosts sind nur Adapterkonsumenten.
- `wissenswerk.yaml`: `interop.platform_independent = true`, kanonische offene Surfaces und Adapter-Policy ergaenzt.
- `project_manifest.json`: `platform_independence`-Block ergaenzt.
- `.agent/tests/suites/wissenswerk-contract.json`: Contract prueft Plattformneutralitaet und `host_specific_semantics_allowed = false`.
- `MASTER_TASK_LIST.md` und `CHANGELOG.md`: Plan und Historie entsprechend aktualisiert.

Zusatzverifikation:

- `python3 -m json.tool wissenswerk.yaml`: PASS
- `python3 -m json.tool project_manifest.json`: PASS
- `./7w_wiki.py test --suite wissenswerk-contract --timeout 60`: PASS, 6/6
- `./7w_wiki.py wissenswerk providers check --json`: PASS
- `./7w_wiki.py audit --json`: PASS, `issues_found = 0`

## Offene Punkte
- pgvector ist als Default-Vertrag konfiguriert, aber noch nicht an eine echte Datenbankmigration oder Embedding-Schreibpipeline angeschlossen.
- OpenAI-kompatible Provider werden lokal nur konfigurationsseitig geprueft; Netzwerk-/API-Smokes stehen aus.
- Discord ist als Adapter-Status implementiert, noch nicht als laufender Bot.
- Die generischen Rollen sind in den Root-Vertraegen dokumentiert, aber der alte Siebenwind-Katalog ist noch nicht auf vier Kernrollen migriert.

## Empfohlene naechste Schritte
1. Echte pgvector-Migration und Embedding-Write/Query-Pipeline implementieren.
2. RagPrep-Import um Auto-Apply-Artikelgenerierung und Provenance-Tabellen erweitern.
3. Siebenwind-spezifische Rollen/Skills schrittweise in Tenant-Profile verschieben.
4. Discord-Bot gegen die neue `search`-Surface produktionsfaehig anbinden.
5. Agenten-/Skill-Generierung auf ein neutrales Adapter-Zielmodell erweitern: Codex bleibt erster generierter Host, aber nicht der semantische Ursprung.
