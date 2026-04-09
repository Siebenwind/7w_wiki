# 🧭 Coordination Hub (Das Grundbuch)

**Epistemischer Status:** #meta
**Version:** 1.0 (Strikte Edition)
**UUID:** 4a2b3c4d-5e6f-7a8b-9c0d-1e2f3a4b5c6d

Dieses Dokument ist die "Single Source of Truth" für die projektinterne Koordination und Dokumentations-Integrität.

## 📜 Die Goldenen Regeln
1. **Mission-Alignment**: Erhalt des 20-jährigen Siebenwind-Erbes (Treasure Trove), geschaffen von Spielern und Stafflern.
2. **Kritische Infragestellung**: Gaps identifizieren, Fragen stellen.
3. **Silicon Inquisition**: AI-interne Zweifel im Parallel-Archiv dokumentieren.
4. **UUID & Registry**: Jedes Dokument muss hier registriert sein.
5. **Zeitstempel & Zitierpflicht**: ISO-8601 und klare Quellenangaben.

## 🏗️ Boards & Archive

| Pfad | Zweck | Admin |
|---|---|---|
| [SY_REVIEW.md](Synapse_Board/SY_REVIEW.md) | Peer-Review & Qualitätskontrolle | Departments |
| [SY_STANDARDS.md](Synapse_Board/SY_STANDARDS.md) | Archivar-Kodex & Regeln | Koordinator |
| [SY_TESTING.md](Synapse_Board/SY_TESTING.md) | Test- und Defect-Protokoll | Test-Waechter |
| [SY_BULLETIN.md](Synapse_Board/SY_BULLETIN.md) | Newsroom & Meilensteine | Herold |
| [Synapse_Board/](Synapse_Board/) | Lore-Konflikte (Synapsen) | Historiker |
| [SILICON_INQUISITION/](Synapse_Board/SILICON_INQUISITION/) | Parallel-Archiv (AI-Gedanken) | AI Only |

## 📦 Dokumenten-Register (Non-Orphan Registry)
*Jedes neue System-Dokument muss hier gelistet werden.*

- [x] [COORDINATION_HUB.md](COORDINATION_HUB.md)
- [x] [MASTER_TASK_LIST.md](../MASTER_TASK_LIST.md)
- [x] [README.md](../README.md)
- [x] [.agent/instructions/persona_ingestor.md](../.agent/instructions/persona_ingestor.md)
- [x] [.agent/instructions/persona_guardian.md](../.agent/instructions/persona_guardian.md)
- [x] [.agent/instructions/persona_historian.md](../.agent/instructions/persona_historian.md)
- [x] [.agent/instructions/persona_coordinator.md](../.agent/instructions/persona_coordinator.md)
- [x] [SY_REVIEW.md](Synapse_Board/SY_REVIEW.md)
- [x] [SY_STANDARDS.md](Synapse_Board/SY_STANDARDS.md)
- [x] [SY_TESTING.md](Synapse_Board/SY_TESTING.md)
- [x] [SILICON_INQUISITION/MANIFEST.md](Synapse_Board/SILICON_INQUISITION/MANIFEST.md)
- [x] [INQ-2026-001_Astral_Web_Doubt.md](Synapse_Board/SILICON_INQUISITION/INQ-2026-001_Astral_Web_Doubt.md)
- [x] [INQ-2026-001_Historian_Report.md](Synapse_Board/SILICON_INQUISITION/INQ-2026-001_Historian_Report.md)
- [x] [PRODUCTION_PROTOCOL.md](PRODUCTION_PROTOCOL.md)
- [x] [.agent/workflows/ingest_master.md](../.agent/workflows/ingest_master.md) (Technischer Standard / Ingestion)
- [x] [.agent/workflows/wiki_style_guide.md](../.agent/workflows/wiki_style_guide.md) (Zentrales Regelwerk)
- [x] [.agent/workflows/meta_master.md](../.agent/workflows/meta_master.md) (Menschlicher Leitpunkt Workflow & Logistik)
- [x] [.agent/scripts/leitpunkt_tool.py](../.agent/scripts/leitpunkt_tool.py) (Leitpunkt Status/Check/Scaffold)
- [x] [LORE_RESEARCH_BOARD.md](Synapse_Board/LORE_RESEARCH_BOARD.md)
- [x] [AGENT_OPERATIONS_HANDBOOK.md](AGENT_OPERATIONS_HANDBOOK.md)
- [x] [docs/Archiv/REDESIGN_ROADMAP_2026.md](../docs/Archiv/REDESIGN_ROADMAP_2026.md)
- [x] [docs/Archiv/MAINTAINER_STANDPUNKT.md](../docs/Archiv/MAINTAINER_STANDPUNKT.md)
- [x] [docs/Archiv/WORKFLOW_DOSSIER_ANTIGRAVITY_ADVISOR_2026-02-18.md](../docs/Archiv/WORKFLOW_DOSSIER_ANTIGRAVITY_ADVISOR_2026-02-18.md)
- [x] [Archivregister/ARCHIVREGISTER.md](Archivregister/ARCHIVREGISTER.md)
- [x] [Archivregister/ARCHIVREGISTER.json](Archivregister/ARCHIVREGISTER.json)
- [x] [Synapse_Board/SY_HISTORIAN_TRACEABILITY.md](Synapse_Board/SY_HISTORIAN_TRACEABILITY.md)
- [x] [Synapse_Board/RESEARCH-2026-010.md](Synapse_Board/RESEARCH-2026-010.md)
- [x] [Synapse_Board/RESEARCH-2026-018.md](Synapse_Board/RESEARCH-2026-018.md)
- [x] [Logs/Conclusions/2026-02-17_Forum_Research_Report.md](../Logs/Conclusions/2026-02-17_Forum_Research_Report.md)
- [x] [.agent/scripts/forum_scanner.py](../.agent/scripts/forum_scanner.py) (legacy runtime alias: `Scripts/forum_scanner.py`)
- [x] [.agent/scripts/research_review.py](../.agent/scripts/research_review.py) (Research-Review-Runtime fuer `./7w_wiki.py start --list-reviews|--approve|--return-for-rework|--comment`)
- [x] [.agent/data/forum_scan_register.json](../.agent/data/forum_scan_register.json) (maschinenlesbares Sichtungsregister fuer allowlistete Forums-Scans)
- [x] [Logs/Reviews/RESEARCH_REVIEW_REGISTER.md](../Logs/Reviews/RESEARCH_REVIEW_REGISTER.md) (Register fuer Forschungsfreigaben, Rueckgaben und Historian-Kommentare)
- [x] [.agent/scripts/install_tool.py](../.agent/scripts/install_tool.py) (Interner Packaging-Helper fuer Bundle-Manifeste und lokale Installationsplaene)
- [x] [.agent/scripts/package_tool.py](../.agent/scripts/package_tool.py) (Kanonischer Bundle-Builder hinter `./7w_wiki.py package`)
- [x] [.agent/scripts/sync_runtime_docs.py](../.agent/scripts/sync_runtime_docs.py) (Generiert Runtime-Command-Register fuer Governance-Dokumente)
- [x] [.agent/scripts/pages_integrity.py](../.agent/scripts/pages_integrity.py) (Geteilte Pages-/Roamlinks-Diagnostik fuer `pages`, `audit`, `repair`, `advisor`)
- [x] [.agent/catalog/catalog.v1.schema.json](../.agent/catalog/catalog.v1.schema.json) (Schema fuer den kanonischen Agentenkatalog)
- [x] [.agent/catalog/catalog.v1.json](../.agent/catalog/catalog.v1.json) (Generierter kanonischer Discovery-Katalog fuer Agents, Skills, Workflows und Surfaces)
- [x] [.agent/scripts/generate_agent_catalog.py](../.agent/scripts/generate_agent_catalog.py) (Generiert den kanonischen Discovery-Katalog aus `.agent/` und `./7w_wiki.py --help-json`)
- [x] [.agent/scripts/generate_codex_skills.py](../.agent/scripts/generate_codex_skills.py) (Generiert Codex-native Adapter-Skills in `.agents/skills/`)
- [x] [.agent/scripts/generate_a2a_agent_card.py](../.agent/scripts/generate_a2a_agent_card.py) (Generiert discovery-only Agent-Metadaten unter `docs/.well-known/agent.json`)
- [x] [.agent/scripts/generate_lore_manifest.py](../.agent/scripts/generate_lore_manifest.py) (Generiert `lore_manifest.json` als AI-agnostische Kompatibilitaetsflaeche aus dem kanonischen Katalog)
- [x] [.agent/scripts/repo_hygiene.py](../.agent/scripts/repo_hygiene.py) (Kanonischer Hot/Cold/Runtime/Build-Hygiene- und Retention-Runner hinter `./7w_wiki.py tech --repo-hygiene`)
- [x] [.agent/scripts/generate_workflow_bridges.py](../.agent/scripts/generate_workflow_bridges.py) (Deprecated Shim auf `generate_codex_skills.py`)
- [x] [.agent/scripts/generate_agent_bridges.py](../.agent/scripts/generate_agent_bridges.py) (Deprecated Shim auf `generate_codex_skills.py`)
- [x] [.agent/config/install_profiles.json](../.agent/config/install_profiles.json) (Packaging-Profile und Ausschlussregeln fuer lokale Bundles)
- [x] [.agent/config/delegation_policy.json](../.agent/config/delegation_policy.json) (Kanonische Delegationsrichtlinie fuer bounded helper tasks)
- [x] [.agent/tests/suites/reader-stats-contract.json](../.agent/tests/suites/reader-stats-contract.json)
- [x] [.agent/tests/suites/interop-command-registry.json](../.agent/tests/suites/interop-command-registry.json)
- [x] [.agent/tests/suites/workflow-matrix-contract.json](../.agent/tests/suites/workflow-matrix-contract.json)
- [x] [.agent/tests/suites/tool-manifest-contract.json](../.agent/tests/suites/tool-manifest-contract.json)
- [x] [.agent/tests/suites/pages-link-contract.json](../.agent/tests/suites/pages-link-contract.json)
- [x] [.agent/tests/suites/catalog-contract.json](../.agent/tests/suites/catalog-contract.json)
- [x] [.agent/tests/suites/adapter-surfaces-contract.json](../.agent/tests/suites/adapter-surfaces-contract.json)
- [x] [.agent/tests/suites/delegation-policy-contract.json](../.agent/tests/suites/delegation-policy-contract.json)
- [x] [.agent/tests/suites/repo-hygiene-contract.json](../.agent/tests/suites/repo-hygiene-contract.json)
- [x] [.agent/tests/suites/manifest-contract.json](../.agent/tests/suites/manifest-contract.json)
- [x] [.agent/tests/suites/source-tree-contract.json](../.agent/tests/suites/source-tree-contract.json)
- [x] [.agent/tests/suites/legacy-doc-contract.json](../.agent/tests/suites/legacy-doc-contract.json)
- [x] [.agent/tests/suites/asset-surface-contract.json](../.agent/tests/suites/asset-surface-contract.json)
- [x] [.agent/tests/suites/codex-workflow-bridges.json](../.agent/tests/suites/codex-workflow-bridges.json) (Deprecated Alias-Suite fuer `adapter-surfaces-contract`)
- [x] [Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md](Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md) (Kanonischer Drift-/Pages-Vertrag)
- [x] [.agent/config/pages_link_policy.json](../.agent/config/pages_link_policy.json) (Allowlist / planned-fix policy fuer unresolved Pages-Targets)
- [x] [.agent/data/pages_health.json](../.agent/data/pages_health.json) (runtime-generated Pages snapshot fuer Advisor und Workflow-Hygiene)
- [x] [.github/workflows/release-bundles.yml](../.github/workflows/release-bundles.yml) (Tag-basierter GitHub-Release-Build fuer Bundle-Assets; keine Repo-Versionierung der Bundles)
- [x] [.codex/config.toml](../.codex/config.toml) (Projektweite Codex-Verdrahtung fuer MCP und Adapter-Skills)
- [x] [System/_archive/README.md](_archive/README.md) (Archivhinweis fuer demotete System-Standards und historische Missions-/Sandbox-Artefakte)
- [x] [System/_archive/SYSTEM_INTEGRITY.md](_archive/SYSTEM_INTEGRITY.md) (Archivierter Altstandard des retired root-first sync models)
- [x] [System/_archive/WORKFLOW_LORE_CONSISTENCY.md](_archive/WORKFLOW_LORE_CONSISTENCY.md) (Archivierter Vorlaeufer der heutigen Drift-/Praezedenzregeln)
- [x] [System/_archive/DELEGATION_CODEX_PHASE_20.md](_archive/DELEGATION_CODEX_PHASE_20.md) (Archivierter Einzelauftrag aus der Pre-Policy-Aera)
- [x] [System/_archive/DELEGATION_STYLING_FIX.md](_archive/DELEGATION_STYLING_FIX.md) (Archivierter Styling-Einzelauftrag)
- [x] [.agents/skills/stats/SKILL.md](../.agents/skills/stats/SKILL.md)
- [x] [.agents/skills/session_start/SKILL.md](../.agents/skills/session_start/SKILL.md) (Generierter Codex-Adapter)
- [x] [.agents/skills/session_takeover/SKILL.md](../.agents/skills/session_takeover/SKILL.md) (Generierter Codex-Adapter)
- [x] [.agents/skills/session_handover/SKILL.md](../.agents/skills/session_handover/SKILL.md) (Generierter Codex-Adapter)
- [x] [.agents/skills/workflow_tech_master/SKILL.md](../.agents/skills/workflow_tech_master/SKILL.md) (Generierter Codex-Adapter)
- [x] [.agents/skills/workflow_test_run/SKILL.md](../.agents/skills/workflow_test_run/SKILL.md) (Generierter Codex-Adapter)
- [x] [.agents/skills/workflow_forum_search/SKILL.md](../.agents/skills/workflow_forum_search/SKILL.md) (Generierter Codex-Adapter)
- [x] [docs/.well-known/agent.json](../docs/.well-known/agent.json) (Discovery-only Agent-Card fuer spaetere A2A-Anbindung)

---
*Zuletzt aktualisiert: 2026-04-08T21:35:00Z | Ref: #canonical_core_mcp_codex_phase1_2026_04_08*
