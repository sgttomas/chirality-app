# Patch Plan — AUDIT_NEW_AGENTS_2026-03-29_1930

**Run:** AUDIT_NEW_AGENTS_2026-03-29_1930
**Date:** 2026-03-29
**Auditor:** AUDIT_AGENTS (Type 2 Task)

---

## Overview

This document provides minimal, targeted patches to address issues found during audit. Patches are **optional enhancements**, not mandatory fixes. All three agents are production-ready without these patches.

**Patch Status:** Optional (INFO-level and WARNING-level improvements; no blockers)

---

## Prioritized Edit Sequence

1. **OPTIONAL PATCH 1:** AGENT_AUDIT_GOVERNANCE.md — Standardize evidence excerpt length to "≤25 words" (affects 1 line; priority: LOW)
2. **OPTIONAL PATCH 2:** AGENT_AUDIT_SCOPE_CLOSURE.md — Add amendment snapshot recency validation (affects Pass 0; priority: MEDIUM)

---

## Patch Details

---

### OPTIONAL PATCH 1: AGENT_AUDIT_GOVERNANCE.md

**Issue ID:** INFO-001
**Severity:** INFO (stylistic)
**File:** AGENT_AUDIT_GOVERNANCE.md
**Current state:** Line 73 specifies evidence excerpt length as "≤30 words"
**Target state:** Standardize to "≤25 words" for consistency with canon and other agents

#### Rationale

The canonical rubric (AUDIT_AGENT.md line 19) and AGENT_HELPS_HUMANS.md define evidence excerpts as "≤25 words." While both specifications are sufficiently conservative, standardizing to "≤25 words" across all agents improves consistency and clarity.

#### Minimal Fix

**File:** `AGENT_AUDIT_GOVERNANCE.md`
**Line:** 73
**Section:** Non-negotiable invariants

**Current text:**
```
- **K-PROV-1** — Every finding must cite the specific file, section, and relevant excerpt (≤30 words).
```

**Replacement text:**
```
- **K-PROV-1** — Every finding must cite the specific file, section, and relevant excerpt (≤25 words).
```

**Diff format:**
```diff
--- a/agents/AGENT_AUDIT_GOVERNANCE.md
+++ b/agents/AGENT_AUDIT_GOVERNANCE.md
@@ -70,1 +70,1 @@
- **K-PROV-1** — Every finding must cite the specific file, section, and relevant excerpt (≤30 words).
+ **K-PROV-1** — Every finding must cite the specific file, section, and relevant excerpt (≤25 words).
```

#### Implementation Notes

- Only 1 line modified
- No behavioral change (≤25 is slightly more strict than ≤30, but well within acceptable range)
- Improves consistency across agent suite
- Estimated effort: 30 seconds
- Risk level: NONE

#### Acceptance Criteria

After patch:
- Line 73 should read "≤25 words" (not "≤30 words")
- No other text in file should change
- File should remain valid markdown

---

### OPTIONAL PATCH 2: AGENT_AUDIT_SCOPE_CLOSURE.md

**Issue ID:** WARNING-001
**Severity:** WARNING (process enhancement)
**File:** AGENT_AUDIT_SCOPE_CLOSURE.md
**Current state:** Pass 0 preconditions (lines 79–89) validate basic amendment snapshot metadata but do not check timestamp freshness
**Target state:** Add explicit freshness validation step

#### Rationale

Line 56 declares "Amendment record is authoritative," implying the amendment snapshot is current. However, if an amendment was issued long ago and closure audit is run months later, the snapshot metadata may be stale. Adding an explicit freshness check in Pass 0 preconditions would prevent false-negative audit conclusions.

**Risk addressed:** MEDIUM (Low in practice because RECONCILIATION typically invokes closure audits immediately after amendments, but explicit check is safer)

#### Minimal Fix

**File:** `AGENT_AUDIT_SCOPE_CLOSURE.md`
**Location:** PROTOCOL section, Pass 0, after line 88
**Section:** Preconditions

**Insert new validation step after current line 88:**

```markdown
5b. Verify amendment snapshot recency:
    - Determine amendment date from the snapshot's `Brief.md` or folder timestamp.
    - If amendment date is more than 7 days before the audit date:
      - Record an ADVISORY finding: "Amendment snapshot is older than 7 days; closure audit may be incomplete if downstream remediation was deferred."
      - Continue with audit (do not halt).
    - If amendment date is in the future (clock skew):
      - Record an ERROR finding: "Amendment snapshot timestamp is in the future; cannot audit."
      - Halt with `FAILED_INPUTS`.
```

#### Diff format

```diff
--- a/agents/AGENT_AUDIT_SCOPE_CLOSURE.md
+++ b/agents/AGENT_AUDIT_SCOPE_CLOSURE.md
@@ -86,7 +86,19 @@
 5. Locate the decomposition document (`DECOMPOSITION_PATH` from brief or discovered from `{EXECUTION_ROOT}/_Decomposition/`).
 6. Determine `DECOMP_VARIANT` from the brief or auto-detect from folder naming conventions.

+5b. Verify amendment snapshot recency:
+    - Determine amendment date from the snapshot's `Brief.md` or folder timestamp.
+    - If amendment date is more than 7 days before the audit date:
+      - Record an ADVISORY finding: "Amendment snapshot is older than 7 days; closure audit may be incomplete if downstream remediation was deferred."
+      - Continue with audit (do not halt).
+    - If amendment date is in the future (clock skew):
+      - Record an ERROR finding: "Amendment snapshot timestamp is in the future; cannot audit."
+      - Halt with `FAILED_INPUTS`.
+
 If preconditions fail, halt with `FAILED_INPUTS` and report what is missing.
```

#### Implementation Notes

- Add ~12 lines of instruction text
- No behavioral change to existing passes
- New optional advisory finding type (does not affect closure status)
- Improves robustness without breaking compatibility
- Estimated effort: 2 minutes
- Risk level: NONE (purely additive; no modifications to existing logic)

#### Acceptance Criteria

After patch:
- Pass 0 should include explicit freshness validation (5b)
- Freshness check should record ADVISORY finding if amendment is >7 days old
- Freshness check should record ERROR and halt if amendment is in future
- Existing preconditions (lines 79–88) should remain unchanged
- All subsequent passes should remain unchanged
- File should remain valid markdown

---

## Alternative Approaches (not recommended)

### Alternative A1: Stricter excerpt length (≤20 words)

For PATCH 1, could reduce excerpt length to "≤20 words" for even tighter constraints.

**Trade-off:** ≤20 may be too strict and force agent implementers to spend effort summarizing longer excerpts. ≤25 is a good balance.

**Recommendation:** Do NOT apply A1. Stick with "≤25 words" minimal fix.

### Alternative A2: Reject scope-closure audits >N days after amendment

For PATCH 2, could make the 7-day threshold strict (halt audit rather than warn).

**Trade-off:** Strict timeout might prevent legitimate late-run audits that happen after long remediation periods. ADVISORY finding is better.

**Recommendation:** Do NOT apply A2. ADVISORY finding is appropriate; allows audit to proceed while flagging potential staleness.

---

## Consolidation / Single-Source-of-Truth Review

**No consolidation needed.** All three agents conform to the canon (AGENT_HELPS_HUMANS.md). No rules need to be centralized or duplicate definitions removed.

**Minor standardization opportunity:** Excerpt length specification ("≤25 words" vs "≤30 words") could be rationalized across agents, but canon does not prohibit per-agent variation.

---

## Integration Testing Notes

After applying patches:

1. **PATCH 1 verification:** Grep agents/ for "excerpt.*≤[0-9]* words" and confirm all instances now use "≤25 words"
   ```
   grep -n "excerpt.*≤" agents/AGENT_*.md
   ```
   Expected: All instances should show "≤25 words"

2. **PATCH 2 verification:** Confirm AGENT_AUDIT_SCOPE_CLOSURE.md Pass 0 includes freshness check
   ```
   grep -A5 "5b. Verify amendment snapshot recency" agents/AGENT_AUDIT_SCOPE_CLOSURE.md
   ```
   Expected: New section should be present with ADVISORY/ERROR handling

---

## Deployment Notes

**Patches are safe to apply:**
- PATCH 1: Stylistic only; no impact on agent behavior
- PATCH 2: Additive only; no breaking changes to existing logic

**Patches can be applied in any order** (independent edits).

**Patches do NOT require:**
- Version bump (unless implementing all outstanding patches in a release)
- Canon file update (canon allows per-agent specification variation)
- Re-audit after patch (patches address audit findings; no new issues introduced)

---

## Summary

| Patch | File | Change | Effort | Risk | Recommended |
|---|---|---|---|---|---|
| 1 | AGENT_AUDIT_GOVERNANCE.md | Change "≤30 words" to "≤25 words" | 30 sec | NONE | OPTIONAL |
| 2 | AGENT_AUDIT_SCOPE_CLOSURE.md | Add amendment freshness check (Pass 0) | 2 min | NONE | OPTIONAL |

**Total effort if all patches applied:** ~3 minutes
**Total risk:** NONE (both patches are non-breaking; purely additive or stylistic)

---

**Patch plan prepared by:** AUDIT_AGENTS
**Date:** 2026-03-29 19:30
**Status:** Ready for review and optional application
