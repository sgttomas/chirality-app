# Dependencies: DEL-011-03 Drive-Through Repair Bays

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- DEL-011-01 Superstructure -- Structural frame must be in place
- DEL-011-02 Steel Embedments -- Equipment attachment points must be ready
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- PKG-012 Interior Construction & Fit-Out -- Equipment installation in repair bays
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** Dependencies.csv (23 rows)
- **Schema Version:** v3.1
- **Run Date:** 2026-03-26 (last refreshed)

### Summary

| Metric | Count |
|---|---|
| Total ACTIVE rows | 23 |
| ANCHOR rows | 2 |
| EXECUTION rows | 21 |
| UPSTREAM | 15 |
| DOWNSTREAM | 8 |
| EXTRACTED origin | 22 |
| DECLARED origin | 1 |
| RETIRED rows | 0 |

### ANCHOR Edges (Tree)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-011-03-001 | IMPLEMENTS_NODE | SOW-0025 | Construct two drive-through repair bays with folding outward overhead doors (Add. 4 Q4); crane clearance constraint | HIGH |
| DEP-011-03-002 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant fully functional maintenance shop addition | HIGH |

### EXECUTION Edges -- UPSTREAM (13 rows)

| DependencyID | Type | Target | TargetName | Confidence | Impact |
|---|---|---|---|---|---|
| DEP-011-03-003 | PREREQUISITE | DEL-011-01 | Concrete Superstructure | HIGH | BLOCKING |
| DEP-011-03-004 | PREREQUISITE | DEL-011-02 | Steel Plate Floor Embedments | HIGH | BLOCKING |
| DEP-011-03-005 | PREREQUISITE | DEL-010-01 | Foundation Construction | HIGH | BLOCKING |
| DEP-011-03-006 | PREREQUISITE | DEL-009-02 | Building Permit Application & Approval | HIGH | BLOCKING |
| DEP-011-03-007 | PREREQUISITE | DEL-009-03 | Safety Code Permits | HIGH | BLOCKING |
| DEP-011-03-008 | PREREQUISITE | DEL-019-01 | Prime Contractor Designation & OH&S Program | HIGH | ADVISORY |
| DEP-011-03-009 | PREREQUISITE | DEL-002-03 | Structural Framing Plans | HIGH | BLOCKING |
| DEP-011-03-010 | PREREQUISITE | DEL-002-04 | Structural Sections & Details | HIGH | BLOCKING |
| DEP-011-03-011 | INTERFACE | DEL-002-07 | Crane Support Structure Details | HIGH | ADVISORY |
| DEP-011-03-012 | INTERFACE | DEL-002-08 | Steel Plate Embedment Plan | MEDIUM | ADVISORY |
| DEP-011-03-013 | PREREQUISITE | DEL-001-02 | Architectural Floor Plans | HIGH | BLOCKING |
| DEP-011-03-014 | PREREQUISITE | DEL-001-07 | Door & Window Schedule | HIGH | BLOCKING |
| DEP-011-03-015 | INTERFACE | DEL-008-03 | Construction Survey | MEDIUM | ADVISORY |

### EXECUTION Edges -- DOWNSTREAM (8 rows)

| DependencyID | Type | Target | TargetName | Confidence | Impact |
|---|---|---|---|---|---|
| DEP-011-03-016 | INTERFACE | DEL-013-04 | Heavy Equipment Exhaust System | HIGH | BLOCKING |
| DEP-011-03-017 | INTERFACE | DEL-014-04 | Floor Drains & Sump Drains | HIGH | BLOCKING |
| DEP-011-03-018 | INTERFACE | DEL-015-04 | Equipment Power Circuits | HIGH | ADVISORY |
| DEP-011-03-019 | INTERFACE | DEL-016-01 | Two 5-Tonne Overhead Cranes | MEDIUM | ADVISORY |
| DEP-011-03-020 | HANDOVER | DEL-020-02 | Final Inspection & CCC | HIGH | ADVISORY |
| DEP-011-03-021 | HANDOVER | DEL-008-04 | As-Built Survey | MEDIUM | INFO |
| DEP-011-03-022 | HANDOVER | DEL-021-05 | Guarantee Period Obligations | MEDIUM | INFO |
| DEP-011-03-023 | HANDOVER | PKG-012 | Interior Construction & Fit-Out | MEDIUM | ADVISORY |

---

## Run Notes

### Run 2026-02-26 -- Initial Extraction

**Inputs and Defaults:**
- SCOPE: DEL-011-03
- RUN_ROOT: /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: TASK_ESTIMATING
- DECOMPOSITION_PATH: Located (R1 2026-02-25)

**Source Documents Scanned:**
- ANCHOR_DOC: Datasheet.md
- EXECUTION_DOCS: Procedure.md, Guidance.md, Specification.md

**Warnings:** None.

### Run 2026-03-26 -- SCA-001 Refresh

**Inputs and Defaults:**
- SCOPE: DEL-011-03 (as part of PKG-011 batch)
- RUN_ROOT: /Users/ryan/ai-env/projects/chirality-app/examples/AB-2026-01424-WDMLRL-2026-Claude/
- DECOMPOSITION_PATH: _Decomposition/WDMLRL_Decomposition_Claude.md (R2 -- 2026-03-26, SCA-001)
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: AUTO (Datasheet.md, Guidance.md, Procedure.md, Specification.md)

**SCA-001 Changes Affecting This Deliverable:**
- SOW-0025 updated: "Construct two drive-through repair bays with folding outward overhead doors (24' wide bays per drawing); door type must not impede overhead crane function in open or closed position (Add. 4, Q4)"
- DEP-011-03-001 anchor statement updated to reflect folding outward door specification and crane clearance constraint.
- The crane clearance constraint (doors must not impede crane function) reinforces the existing DEP-011-03-011 (crane support structure interface) and DEP-011-03-019 (crane clearance coordination). No new rows needed.

**Changes Applied:**
- Updated LastSeen to 2026-03-26 on all 23 ACTIVE rows.
- Updated DEP-011-03-001 statement to reflect SCA-001 SOW-0025 text (folding outward doors; crane clearance).
- No new rows added. No rows retired.

**Warnings:** None.

**Quality Check Results:**
- Parent anchor check: PASS (exactly 1 ACTIVE IMPLEMENTS_NODE: DEP-011-03-001 -> SOW-0025)
- DependencyID uniqueness: PASS (23 unique IDs)
- Required columns present: PASS
- Evidence completeness: PASS (all ACTIVE rows have EvidenceFile and SourceRef)
- Schema version: PASS (all rows v3.1)
- Referential integrity: PASS (FromDeliverableID = DEL-011-03 on all rows)

---

## Run History

| Run Date | Mode | Strictness | Consumer | Decomp Status | Warnings | ACTIVE Anchor | ACTIVE Execution | Notes |
|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | Available (R1 2026-02-25) | None | 2 | 21 | Initial extraction. 23 total ACTIVE rows. |
| 2026-03-26 | UPDATE | CONSERVATIVE | NONE | Available (R2 2026-03-26 SCA-001) | None | 2 | 21 | SCA-001 refresh. SOW-0025 anchor updated (folding outward doors). |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| ACTIVE total | 23 |
| RETIRED total | 0 |
| ANCHOR (ACTIVE) | 2 |
| EXECUTION (ACTIVE) | 21 |

### Closure State Breakdown (ACTIVE EXECUTION rows)

| SatisfactionStatus | Count |
|---|---|
| PENDING | 21 |

### EstimateImpactClass Breakdown (all ACTIVE rows)

| EstimateImpactClass | Count |
|---|---|
| BLOCKING | 11 |
| ADVISORY | 8 |
| INFO | 4 |
