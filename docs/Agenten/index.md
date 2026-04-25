# Agent and Operations Hub

Technical area for platform-independent agent operation, workflows, and interoperability.

## Schnellstart

```bash
./wissenswerk.py doctor --json
./wissenswerk.py providers check --json
./wissenswerk.py design lint --json
./wissenswerk.py hygiene reports --json
./wissenswerk.py export plan --json
./7w_wiki.py test --suite wissenswerk-contract --timeout 60
```

## Betriebsbereiche

- [Wissenswerk overview](../Wissenswerk/index.md)
- [Interop-Leitlinien](interop.md)
- [Dispatch und Agentenkommunikation](dispatch.md)
- [Workflow- und Skill-Bruecken](workflows.md)
- [Agent Operations Handbook](../AGENT_OPERATIONS_HANDBOOK.md)

## Abgrenzung

This section is for technical editors and agent systems.

- Use `./wissenswerk.py` for generic Wissenswerk work.
- Use `./7w_wiki.py` for legacy Siebenwind operations.
- Run broad Siebenwind audit/Pages suites only for legacy content, legacy tooling, or published-site changes.
- Host-specific adapters must derive from the neutral contracts, not define their own behavior.

For reader-facing Siebenwind content, use the [Wiki start page](../Siebenwind_Wiki/index.md).
