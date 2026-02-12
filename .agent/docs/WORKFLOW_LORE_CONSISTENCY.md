---
layout: wiki_page
title: WORKFLOW LORE CONSISTENCY
category: Sonstiges
---

# WORKFLOW LORE CONSISTENCY

**Epistemischer Status:** #perspektive

To maintain the quality and consistency of the Siebenwind Wiki while processing mass data, the following rules apply:

## 1. Wiki Style Convention (Frontmatter)

Every document in the wiki must have the following YAML frontmatter:

```yaml
---
layout: wiki_page
title: [Display Title]
category: [Persönlichkeit | Geschichte | Erzählung | Geografie | Religion | Magie]
---
```

The first level-1 heading (`# Title`) must exactly match the `title` field in the frontmatter.

## 2. Truth Hierarchy & Escalation
To distinguish between ground truth and subjective accounts, the following tiered system applies:

1.  **Lokal-Kanon (#canon):** Ordner `/Hintergrund/`. Axiomatic world laws (Absolute Truth).
2.  **Lokale Quelle (#bote, #überlieferung, #perspektive):** The specific document being integrated.
3.  **Web-Kanon (`siebenwind.de`):** Used for verification and filling gaps.
4.  **User Enquiry:** The final authority in case of irreconcilable conflicts.

**Escalation Logic:**
- Verify Local -> Verify Web -> Log as `[UNGEKLÄRT]` if inconclusive -> Ask User as last resort.

**Consistency Checks**:
1. **Axiom Check**: Does the story contradict the Götter-Kanon or Magie-Axiome?
2. **Time Check**: Use the `Time Keeper` skill to validate dates.
3. **Uncertainty Logging**: Mark unproven claims with `[UNGEKLÄRT]` and log in `Konsistenzbericht_2026.md`.

## 3. Git History

- **Batch Commits**: After processing a batch of documents (e.g., 10 stories), a git commit must be made.
- **Commit Message Pattern**: `Batch-Processing: [Count] player stories integrated. [Conflict Count] conflicts listed in /Logs.`

## 4. Bi-directional Linking

- **In Story**: Link every mentioned Entity (Entity, Place, Event) to its `/Siebenwind_Wiki/` article.
- **In Wiki**: Add a section `## Überlieferungen` (Traditions) at the bottom of the wiki article and link back to the story.
