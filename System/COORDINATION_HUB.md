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
- [x] [.agent/scripts/generate_workflow_bridges.py](../.agent/scripts/generate_workflow_bridges.py) (Generiert Codex-Workflow-Bridges in `.agents/skills/`)
- [x] [.agent/config/install_profiles.json](../.agent/config/install_profiles.json) (Packaging-Profile und Ausschlussregeln fuer lokale Bundles)
- [x] [.agent/tests/suites/reader-stats-contract.json](../.agent/tests/suites/reader-stats-contract.json)
- [x] [.agent/tests/suites/interop-command-registry.json](../.agent/tests/suites/interop-command-registry.json)
- [x] [.agent/tests/suites/workflow-matrix-contract.json](../.agent/tests/suites/workflow-matrix-contract.json)
- [x] [.agent/tests/suites/tool-manifest-contract.json](../.agent/tests/suites/tool-manifest-contract.json)
- [x] [.agent/tests/suites/pages-link-contract.json](../.agent/tests/suites/pages-link-contract.json)
- [x] [.agent/tests/suites/codex-workflow-bridges.json](../.agent/tests/suites/codex-workflow-bridges.json)
- [x] [Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md](Synapse_Board/SY_DRIFT_PAGES_CONTRACT.md) (Kanonischer Drift-/Pages-Vertrag)
- [x] [.agent/config/pages_link_policy.json](../.agent/config/pages_link_policy.json) (Allowlist / planned-fix policy fuer unresolved Pages-Targets)
- [x] [.agent/data/pages_health.json](../.agent/data/pages_health.json) (runtime-generated Pages snapshot fuer Advisor und Workflow-Hygiene)
- [x] [.github/workflows/release-bundles.yml](../.github/workflows/release-bundles.yml) (Tag-basierter GitHub-Release-Build fuer Bundle-Assets; keine Repo-Versionierung der Bundles)
- [x] [.agents/skills/stats/SKILL.md](../.agents/skills/stats/SKILL.md)
- [x] [.agents/skills/session_start/SKILL.md](../.agents/skills/session_start/SKILL.md) (Generierte Codex-Workflow-Bridge)
- [x] [.agents/skills/session_takeover/SKILL.md](../.agents/skills/session_takeover/SKILL.md) (Generierte Codex-Workflow-Bridge)
- [x] [.agents/skills/session_handover/SKILL.md](../.agents/skills/session_handover/SKILL.md) (Generierte Codex-Workflow-Bridge)
- [x] [.agents/skills/workflow_tech_master/SKILL.md](../.agents/skills/workflow_tech_master/SKILL.md) (Generierte Codex-Workflow-Bridge)
- [x] [.agents/skills/workflow_test_run/SKILL.md](../.agents/skills/workflow_test_run/SKILL.md) (Generierte Codex-Workflow-Bridge)
- [x] [.agents/skills/workflow_forum_search/SKILL.md](../.agents/skills/workflow_forum_search/SKILL.md) (Generierte Codex-Workflow-Bridge)

---
*Zuletzt aktualisiert: 2026-04-08T20:46:00Z | Ref: #historian_split_after_wave2_2026_04_08*
