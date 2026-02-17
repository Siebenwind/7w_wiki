---
name: Lektor Check Bridge
description: Thin wrapper for style and grammar verification via ./7w_wiki.py check.
---

# Skill: Lektor Check
> **Wrapper for**: `.agent/skills/lektor/SKILL.md`

Use this skill when validating writing quality and style conformity.

## Usage

```bash
./7w_wiki.py check
./7w_wiki.py audit
```

## Notes
- `check` catches language/style issues.
- `audit` confirms structural consistency after text changes.
- Route blockers and contradiction questions via Dispatch (`mail post`) to the relevant specialist.
