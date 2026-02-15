# System Integrity & Directory Standards

## 📂 Core Directory Structure

The Siebenwind Wiki follows a strict directory hierarchy. **Do NOT delete or move these folders** without an authorized migration plan.

| Path | Purpose | Integrity Level |
| :--- | :--- | :--- |
| `Siebenwind_Wiki/` | Master Lore Content (Markdown) | **CRITICAL** |
| `Quellen/` | Source Material (Forum, News, Stories) | **CRITICAL** |
| `System/` | Configuration, Scripts, Standards | **HIGH** |
| `docs/` | Deployment Sync Folder (Buffer for MkDocs) | **EPHEMERAL** |

## 🛡️ Integrity Rules

1.  **Deployment Sync**: The `docs/` folder is a staging area. Files inside `docs/` may be deleted and replaced by a "Physical Sync" process during builds. **Do not store original work only in `docs/`**.
2.  **No Manual Deletions**: Never delete `Siebenwind_Wiki/` or `Quellen/` manually. If you encounter issues (e.g., symlink errors), allow the Agent to handle the migration to the Physical Sync model.
3.  **Source of Truth**: The root folders (`Siebenwind_Wiki/`, `Quellen/`) are the sole source of truth. The Agent will copy these to `docs/` for the MkDocs engine to process.

## 🛠️ Recovery Protocol

If folders are missing:
1.  Check Git status (`git status`).
2.  Restore via Git (`git restore <path>`).
3.  Contact the Keeper of the Lore (Agent) for realignment.
