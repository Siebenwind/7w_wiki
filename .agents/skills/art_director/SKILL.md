---
name: Art Director Bridge
description: Thin wrapper for visual direction tasks. Uses workflow guidance only and keeps runtime execution on ./7w_wiki.py.
---

# Skill: Art Director (Atelier)
> **Wrapper for**: `.agent/skills/art_director/SKILL.md`

This skill handles image generation and visual consistency for the wiki.

## Usage
This skill is invoked via workflow guidance and project review tasks.
See `.agent/skills/art_director/SKILL.md` for prompt engineering guidelines.

## Standards
- **Style**: Archivum Argentum (Silverpoint / Renaissance Draft, serioes und reduziert).
- **Format**: WebP, 16:9 or 1:1.
- **Coordination**: Post status/questions via Dispatch when outputs block other agents.
