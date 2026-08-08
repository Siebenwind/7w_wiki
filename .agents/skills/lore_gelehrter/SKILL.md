---
name: Lore-Gelehrter (Analytik & Auskunft)
description: Fähigkeit, das gesamte Wiki-Wissen zu aggregieren, Inkonsistenzen zu finden und präzise Auskunft zu geben.
---

# Codex Skill: Lore-Gelehrter (Analytik & Auskunft)

> **Canonical skill**: `.agent/skills/lore_gelehrter/SKILL.md`
> **Marker**: Generated Codex adapter skill. Do not edit manually.

This adapter is generated from the canonical catalog. Runtime execution stays on `./7w_wiki.py`; `.agent/` remains the source of truth.

## Primary Runtime Command
`./7w_wiki.py historian <query>`

## Follow-up Commands
- `./7w_wiki.py search <query> --source all`
- `./7w_wiki.py historian review --list --json`
- `./7w_wiki.py historian review --dossier --research-id RESEARCH-2026-XXX --json`
- `./7w_wiki.py pages backlog historian --next`
- `./7w_wiki.py pages backlog historian --cluster <cluster> --dry-run --json`
- `./7w_wiki.py pages backlog historian --article <path> --resolve --json`
- `./7w_wiki.py pages backlog historian --cluster <cluster> --resolve --json`
- `./7w_wiki.py pages backlog historian --run-all --resolve --json`
- `./7w_wiki.py mail post --from Historian --to ALL --subject "<lore question>" --body "<summary>"`

## Instructions
- Use this adapter for deep lore synthesis, contradiction analysis, and evidence-backed answers.
- The Historian is an escalation and synthesis organ, not the default editor for straightforward source integration.
- Use historian review for structured Research Board review backlog before relying on ad-hoc Dispatch reading.
- Treat Pages needs_historian as a Historian-operable cluster lane; reserve needs_human for true maintainer escalation.
- Use Pages backlog --resolve for article, cluster, and run-all resolution runs; bulk semantic apply requires explicit warning acknowledgement.
- Route unresolved contradictions through Dispatch or the Synapse Board with explicit evidence.
- Every Historian run must end with a user-facing summary containing the separate headings Implementierte Neuerungen and Erkenntnisgewinn; explain content value and explicitly justify empty sections.

## References
- `.agent/skills/lore_gelehrter/SKILL.md`
- `System/Synapse_Board/LORE_RESEARCH_BOARD.md`
- `System/Templates/HISTORIAN_CLOSEOUT_TEMPLATE.md`
