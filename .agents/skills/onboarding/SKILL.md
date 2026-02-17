---
name: Onboarding Bridge
description: Start-of-session bridge that runs the canonical onboarding loop through ./7w_wiki.py.
---

# Skill: Onboarding
> **Wrapper for**: `.agent/workflows/start.md`

Use this skill when starting a new agent session or taking over work.

## Usage
Run the canonical onboarding sequence:

```bash
./7w_wiki.py start
./7w_wiki.py advisor
./7w_wiki.py mail inbox --status OPEN
./7w_wiki.py test --suite clean-client-state
./7w_wiki.py audit
```

## Notes
- Runtime execution remains exclusive to `./7w_wiki.py`.
- Follow-up paths are selected from `.agent/workflows/start.md`.
- Open dispatch messages should be claimed/done according to `SY_DISPATCH` before ad-hoc work starts.
