# QA Report — COV_POST_SCA001

**Run Label:** POST_SCA001
**Timestamp:** 2026-03-26T17:48
**Agent:** AUDIT_DECOMP (Type 2)

## Scan Coverage

| Area | Scanned | Notes |
|---|---|---|
| Package folders (PKG-*) | 21 of 21 | All discovered and matched |
| Deliverable folders (DEL-*) | 117 of 117 | All discovered under correct parent packages |
| _CONTEXT.md files | 117 of 117 | All present |
| _STATUS.md files | 117 of 117 | All present |
| Decomposition §5 Objectives | 8 objectives parsed | OBJ-001 through OBJ-008 |
| Decomposition §6 Packages | 21 packages parsed | PKG-001 through PKG-021 |
| Decomposition §7 Deliverables | 117 deliverables parsed | Across all 21 packages |
| Decomposition §8 Scope Ledger | 92 IN-scope items parsed | SOW-0001 through SOW-0122 (with gaps per deletions/merges) |
| Decomposition §4 OUT-scope | 7 OUT items | SOW-0200 through SOW-0206 |
| Decomposition §9 Telemetry | Validated | All metrics internally consistent |

## Parse Quality

- Decomposition document fully parseable; all tables well-formed
- Two _CONTEXT.md format variants encountered (both handled):
  - Format A: `**Package:** PKG-XXX Name` (47 files — original batch)
  - Format B: `- **Package**: PKG-XXX Name` (70 files — second batch)
- Two _STATUS.md format variants encountered (both handled):
  - Format A: `**Current State:** STATE` (47 files)
  - Format B: `**Status:** STATE` (70 files)

## Limitations

- Artifact presence check (Check 6) is assessed at the folder level only; individual anticipated artifact filenames are not enumerated in the decomposition's Deliverables table (the "Covers SOW" column provides scope coverage, not filenames). All deliverable folders exist, so 100% presence is recorded for structural presence.
- Context fidelity check compares Package reference and Name; detailed field-by-field comparison of Type, Responsible, and Description was validated on a representative sample across all 21 packages.
- The SSOW (§3) contains scope items listed across subsections A through P. The Scope Ledger (§8) maps 92 unique IN-scope items; the delta from the SSOW raw item count is due to deleted/merged items documented in §4 Deleted Items.

## Methodology Notes

- No changes to methodology from prior run (PRE_SCA001)
- Same 9-check protocol applied identically
