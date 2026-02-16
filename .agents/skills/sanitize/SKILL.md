---
name: Sanitize Bridge
description: Thin wrapper for structural normalization tasks via ./7w_wiki.py sanitize.
---

# Skill: Sanitize
> **Wrapper for**: `.agent/workflows/check_master.md`

Use this skill for layout and frontmatter normalization passes.

## Usage

```bash
./7w_wiki.py sanitize --auto
./7w_wiki.py audit
```

## Notes
- Apply sanitizer first, then verify consistency with audit.
- Keep edits additive and preserve existing workflow semantics.
