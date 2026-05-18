# Decomposition Coverage Report

**Run Label:** PRE_SCA001
**Date:** 2026-03-26
**Decomposition:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1 -- 2026-02-25)
**Variant:** PROJECT
**Scope:** ALL
**Requested By:** SCOPE_CHANGE

---

## Check Summary

| Check | Name | Verdict | Issues |
|-------|------|---------|--------|
| 1 | Forward Coverage -- Packages | **PASS** | 0 |
| 2 | Forward Coverage -- Deliverables | **PASS** | 0 |
| 3 | Reverse Coverage -- Folders | **PASS** | 0 |
| 4 | ID Consistency | **PASS** | 0 |
| 5 | Context Fidelity | **PASS** | 0 |
| 6 | Artifact Presence | **PASS** | 0 |
| 7 | Objective Mapping | **PASS** | 0 |
| 8 | Ledger Integrity | **PASS** | 0 |
| 9 | Lifecycle Distribution | **PASS** | 0 |
| -- | Telemetry Consistency (supplemental) | **WARNING** | 1 |

**Overall: WARNINGS** (0 BLOCKERs, 1 WARNING, 0 INFOs)

---

## Check 1 -- Forward Coverage: Packages

All 21 packages declared in §6 have corresponding `PKG-{ID}_*` folders under EXECUTION_ROOT.

| PackageID | Name | Folder Found | Folder Path |
|-----------|------|-------------|-------------|
| PKG-001 | Architectural Design | YES | `PKG-001_Architectural Design/` |
| PKG-002 | Structural Design | YES | `PKG-002_Structural Design/` |
| PKG-003 | Mechanical Design | YES | `PKG-003_Mechanical Design/` |
| PKG-004 | Electrical Design | YES | `PKG-004_Electrical Design/` |
| PKG-005 | Civil Design | YES | `PKG-005_Civil Design/` |
| PKG-006 | Plumbing Design | YES | `PKG-006_Plumbing Design/` |
| PKG-007 | Landscape Architectural Design | YES | `PKG-007_Landscape Architectural Design/` |
| PKG-008 | Geotechnical Investigation & Surveying | YES | `PKG-008_Geotechnical Investigation & Surveying/` |
| PKG-009 | Permitting & Regulatory Compliance | YES | `PKG-009_Permitting & Regulatory Compliance/` |
| PKG-010 | Foundation Construction | YES | `PKG-010_Foundation Construction/` |
| PKG-011 | Building Structure & Envelope | YES | `PKG-011_Building Structure & Envelope/` |
| PKG-012 | Interior Construction & Fit-Out | YES | `PKG-012_Interior Construction & Fit-Out/` |
| PKG-013 | Mechanical & HVAC Installation | YES | `PKG-013_Mechanical & HVAC Installation/` |
| PKG-014 | Plumbing & Water Systems Installation | YES | `PKG-014_Plumbing & Water Systems Installation/` |
| PKG-015 | Electrical & Low-Voltage Installation | YES | `PKG-015_Electrical & Low-Voltage Installation/` |
| PKG-016 | Crane & Lifting Equipment | YES | `PKG-016_Crane & Lifting Equipment/` |
| PKG-017 | Existing Building Renovation (Old North Shop) | YES | `PKG-017_Existing Building Renovation (Old North Shop)/` |
| PKG-018 | Sitework & Civil Construction | YES | `PKG-018_Sitework & Civil Construction/` |
| PKG-019 | Construction Management & OH&S | YES | `PKG-019_Construction Management & OH&S/` |
| PKG-020 | Commissioning & Closeout | YES | `PKG-020_Commissioning & Closeout/` |
| PKG-021 | Bonding, Insurance & Warranty | YES | `PKG-021_Bonding, Insurance & Warranty/` |

**Verdict: PASS** -- 21/21 packages found (100%).

---

## Check 2 -- Forward Coverage: Deliverables

All 117 deliverables declared in §7 have corresponding `DEL-{ID}_*` folders under their respective package's `1_Working/` directory.

Deliverable counts by package:

| PackageID | Declared | Found |
|-----------|----------|-------|
| PKG-001 | 11 | 11 |
| PKG-002 | 12 | 12 |
| PKG-003 | 7 | 7 |
| PKG-004 | 9 | 9 |
| PKG-005 | 7 | 7 |
| PKG-006 | 8 | 8 |
| PKG-007 | 4 | 4 |
| PKG-008 | 4 | 4 |
| PKG-009 | 4 | 4 |
| PKG-010 | 1 | 1 |
| PKG-011 | 7 | 7 |
| PKG-012 | 3 | 3 |
| PKG-013 | 6 | 6 |
| PKG-014 | 6 | 6 |
| PKG-015 | 5 | 5 |
| PKG-016 | 1 | 1 |
| PKG-017 | 4 | 4 |
| PKG-018 | 6 | 6 |
| PKG-019 | 4 | 4 |
| PKG-020 | 3 | 3 |
| PKG-021 | 5 | 5 |
| **TOTAL** | **117** | **117** |

**Verdict: PASS** -- 117/117 deliverables found (100%).

---

## Check 3 -- Reverse Coverage: Folders

All 21 PKG folders and all 117 DEL folders in the filesystem correspond to entries in the decomposition document. No orphan folders found.

**Verdict: PASS** -- 0 orphan partition folders, 0 orphan deliverable folders.

---

## Check 4 -- ID Consistency

For all 117 matched deliverable pairs, the normalized ID extracted from the folder name matches the DeliverableID in the decomposition document. Normalization rule: strip the `_{description}` suffix after the `DEL-XXX-YY` prefix.

Example: `DEL-005-01_Preliminary-Design` -> `DEL-005-01` matches §7 entry `DEL-005-01_Preliminary-Design`.

No ID mismatches found.

**Verdict: PASS** -- 0 ID mismatches.

---

## Check 5 -- Context Fidelity

All 117 deliverable folders contain a `_CONTEXT.md` file. Representative sampling across all 21 packages confirmed that key fields (Name, Package, Type, Responsible Party) are consistent with their §7 declarations. No substantially divergent descriptions were found.

**Verdict: PASS** -- 117/117 _CONTEXT.md files present, sampled fields match.

---

## Check 6 -- Artifact Presence

For PROJECT_DECOMP, the standard four-document set is checked:
- `Datasheet.md`
- `Specification.md`
- `Guidance.md`
- `Procedure.md`

All 117 deliverable folders contain all 4 standard documents.

**Verdict: PASS** -- 468/468 expected standard artifacts present (4 per deliverable x 117 deliverables).

---

## Check 7 -- Objective Mapping

All 8 objectives from §5 have at least one supporting deliverable with an existing folder:

| ObjectiveID | Statement (truncated) | Supporting Deliverables (count) | All Folders Exist |
|-------------|----------------------|-------------------------------|------------------|
| OBJ-001 | Deliver a code-compliant maintenance shop... | 90+ | YES |
| OBJ-002 | Complete all work on or before Dec 31, 2026 | 15+ | YES |
| OBJ-003 | Produce complete P.Eng.-stamped IFC design... | 60+ | YES |
| OBJ-004 | Install and commission mechanical/plumbing systems... | 20+ | YES |
| OBJ-005 | Install and commission electrical/low-voltage systems... | 15+ | YES |
| OBJ-006 | Deliver within negotiated stipulated price... | 8+ | YES |
| OBJ-007 | Maintain safe site operations... | 6+ | YES |
| OBJ-008 | Satisfy bonding/insurance/warranty obligations... | 5 | YES |

No objectives are unsupported. No objectives are supported only by RETIRED deliverables (all are SEMANTIC_READY).

**Verdict: PASS** -- 8/8 objectives have active supporting deliverables.

---

## Check 8 -- Ledger Integrity

The Scope Ledger (§8) contains 91 IN-scope items. Each references a valid PackageID (confirmed against Check 1) and valid DeliverableID(s) (confirmed against Check 2).

No ledger rows reference non-existent packages or deliverables. No TBD mappings found.

**Verdict: PASS** -- 91/91 scope items reference valid entities.

---

## Check 9 -- Lifecycle Distribution

| Lifecycle State | Count | Percentage |
|----------------|-------|-----------|
| SEMANTIC_READY | 117 | 100.0% |
| OPEN | 0 | 0.0% |
| INITIALIZED | 0 | 0.0% |
| IN_PROGRESS | 0 | 0.0% |
| CHECKING | 0 | 0.0% |
| ISSUED | 0 | 0.0% |
| RETIRED | 0 | 0.0% |
| UNKNOWN | 0 | 0.0% |

All 117 deliverables are in SEMANTIC_READY state. This is consistent with a project that has completed initial scaffolding and semantic lens generation but has not yet begun detailed engineering work.

**Verdict: PASS** -- No unexpected lifecycle states.

---

## Supplemental Finding: Telemetry Count Mismatch

**Severity: WARNING**

The decomposition document §9 (Coverage & Telemetry) states:
> `DeliverableCount: 111`

However, the actual count of deliverables enumerated across all package tables in §7 is **117**. This is an internal inconsistency in the decomposition document. The 6-deliverable discrepancy may be due to a calculation error when the document was produced.

**Decomposition Reference:** §9, `DeliverableCount` row
**Evidence:** Manual count of all deliverable rows in §7 tables = 117; filesystem folder count = 117.

---

## What to Fix for a Cleaner Rerun

1. **Update §9 DeliverableCount** from `111` to `117` in the decomposition document to resolve the telemetry mismatch warning.

No other corrective actions are needed. The decomposition and filesystem are fully synchronized.
