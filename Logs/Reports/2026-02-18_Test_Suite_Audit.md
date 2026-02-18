# Test Suite Audit & Critique

**Date**: 2026-02-18
**Author**: Antigravity
**Topic**: CI/CD & Interop Test Suite Analysis

## 1. Executive Summary
The current test suite (`./7w_wiki.py test`) is **functional but fragile**. It effectively guards the "Skeleton" of the system (CLI commands, Documentation, File Existence) but fails to verify the "Brain" (AI Logic, RAG Quality).
The execution environment is tightly coupled to the **Production Filesystem**, leading to permission errors during restricted runs.

## 2. Status Quo (Run Analysis)

| Suite | Status | Focus | Notes |
| :--- | :--- | :--- | :--- |
| **`clean-client-state`** | ✅ **PASS** | CLI & Queue | Verifies `help`, `start`, `advisor`, and `mail` commands work without crashing. |
| **`interop-doc-links`** | ✅ **PASS** | Docs Hygiene | Ensures all internal markdown links in governance docs are valid. |
| **`reader-stats-contract`** | ❌ **FAIL** | Output Contract | Failed due to **PermissionError** when writing/reading `Logs/Archive`. |
| **`rag-relevance-smoke`** | ⚠️ **SKIP** | AI Quality | Disabled by default. Needs manual opt-in. |

## 3. Critique: "Are they meaningful?"

### ✅ Strengths (The "Contract")
The tests perform well as **Integration Contracts**:
-   They ensure the **CLI Interface** is stable (`./7w_wiki.py` always runs).
-   They prevent **Documentation Rot** (broken links in `AGENTS.md` are caught).
-   They guarantee **Operational Hygiene** (e.g., that Dispatch queues are readable).
*This provides a solid baseline for "System Health".*

### ❌ Weaknesses (The "Logic")
The tests are **Shallow Smoke Tests**:
-   **No Behavioral Logic**: They check *if* a command runs, not *if it produces the right answer* (e.g., does the Planner actually plan?).
-   **Environment Fragility**: The tests write to `Logs/Archive/`. This causes failures in restrictive environments. Tests should use `/tmp` or a mocked filesystem.
-   **Blind to Quality**: The `rag-relevance-smoke` suite is the only one checking *content quality*, and it is effectively unused.

## 4. Recommendations
1.  **Decouple Storage**: Modify `test_runner.py` to use a temporary directory for test artifacts, preventing permission errors.
2.  **Enable RAG Tests**: Promote `rag-relevance-smoke` to a standard suite (running on a small, controlled subset of data).
3.  **New `behavior` Suite**: Create a test suite that mocks an agent interaction (e.g., "Given a user request, does the Planner generate a valid `implementation_plan.md`?").
