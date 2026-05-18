# DEL-018-05_Wash-Bay-Drainage | Dependencies

## Dependency Tracking Status
**Tracking Status**: TRACKED
**Register Schema**: v3.1
**Last Run**: 2026-03-26

## Dependency Framework

### Upstream Dependencies
Dependencies that must be satisfied before this deliverable can proceed:

| Dependency ID | Description | Status | Notes |
|---------------|-------------|--------|-------|
| DEL-018-02 | Site Grading & Landscaping Complete | Pending | Drainage design depends on site grades |
| ENV-PERMIT-001 | Environmental discharge permit | Pending | May require regulatory approval |
| DRAINAGE-DESIGN-001 | Drainage system design finalized | Pending | Design plan must be approved |
| SUMP-SPEC-001 | Sump pit specification | Pending | Dimensions and capacity must be defined |

### Downstream Dependencies
Deliverables that depend on completion of this deliverable:

| Dependent ID | Description | Status | Notes |
|--------------|-------------|--------|-------|
| WASH-BAY-OPS-001 | Wash bay operational capability | Pending | Drainage system required for operations |
| ENVIRONMENTAL-001 | Environmental compliance | Pending | Proper discharge management required |

## Critical Path Assessment
- **On Critical Path**: CONDITIONAL
- **Justification**: Important for environmental compliance (OBJ-004) and operational capability; can proceed in parallel with other sitework after grading

## Dependency Management Notes
- Dependencies tracked at deliverable level within PKG-018
- Environmental regulatory requirements may be complex - recommend early engagement with regulators
- Can potentially proceed in parallel with DEL-018-03, 04, 06 after DEL-018-02 complete

## Interdependency Matrix

### Within PKG-018
- Depends on DEL-018-02 completion for grading context
- Can proceed in parallel with DEL-018-03 (Driving Surface), 04 (Pads), 06 (Utilities)
- Drainage system design must coordinate with utility placement

### Cross-Package Dependencies
- Supports environmental compliance objectives (OBJ-004)
- Manages water from facility operations
- Discharge location may relate to utility tie-ins (DEL-018-06)

---

## Extracted Dependency Register

**Total Rows**: 14 | **ACTIVE**: 14 | **RETIRED**: 0

### ANCHOR Rows (3 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-018-05-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0027b | SOW-0027b | HIGH |
| DEP-018-05-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | OBJ-001 | HIGH |
| DEP-018-05-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-004 | OBJ-004 | HIGH |

### EXECUTION Rows (11 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-018-05-004 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-018-02 Site Grading & Landscaping | HIGH | BLOCKING |
| DEP-018-05-005 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-005-02 Site Grading Plan | HIGH | BLOCKING |
| DEP-018-05-006 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-005-03 Drainage Plan | HIGH | BLOCKING |
| DEP-018-05-007 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-006-03 Drain & Vent Plans | HIGH | BLOCKING |
| DEP-018-05-008 | UPSTREAM | PREREQUISITE | DOCUMENT | Geotechnical Report (SOW-0001) | HIGH | BLOCKING |
| DEP-018-05-009 | UPSTREAM | CONSTRAINT | EXTERNAL | ENV-PERMIT-001 | MEDIUM | ADVISORY |
| DEP-018-05-010 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-011-05 Wash Bay Enclosure | HIGH | ADVISORY |
| DEP-018-05-011 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-014-04 Floor Drains & Sump Drains | HIGH | ADVISORY |
| DEP-018-05-012 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-018-06 Utility Tie-Ins | MEDIUM | INFO |
| DEP-018-05-013 | UPSTREAM | PREREQUISITE | DOCUMENT | Sump Pit Specification (SUMP-SPEC-001) | HIGH | BLOCKING |
| DEP-018-05-014 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-008-04 As-Built Survey | HIGH | INFO |

---

## Run Notes

### Run Parameters (2026-02-26)
- **MODE**: UPDATE
- **STRICTNESS**: CONSERVATIVE
- **CONSUMER_CONTEXT**: TASK_ESTIMATING
- **SOURCE_DOCS**: AUTO (resolved below)
- **ANCHOR_DOC**: Datasheet.md (selected by heuristic: filename contains "datasheet")
- **EXECUTION_DOC_ORDER**: Procedure.md, Guidance.md, Specification.md, Datasheet.md
- **DECOMPOSITION_PATH**: `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1, 2026-02-25) -- loaded and validated successfully
- **_REFERENCES.md**: Present and read; used for document pointer resolution

### Defaults Applied
- DOC_ROLE_MAP: DEFAULT heuristic applied
- ANCHOR_DOC: AUTO resolved to Datasheet.md (contains "datasheet" keyword; highest anchor-signal document with Identification table, SOW Reference, Objectives)
- EXECUTION_DOC_ORDER: AUTO resolved to Procedure.md first (contains explicit prerequisites table and step-by-step workflow), then Guidance.md (principles, considerations, conflict table), then Specification.md (requirements and verification), then Datasheet.md (physical parameters and constraints)

### Decomposition Validation
- Decomposition file located: `WDMLRL_Decomposition_Claude.md` (R1, 2026-02-25)
- DEL-018-05 confirmed in decomposition SS7 PKG-018 table: `DEL-018-05_Wash-Bay-Drainage | Wash Bay Drainage & Mud Sump | General Contractor | Construction | SOW-0027b | OBJ-001, OBJ-004`
- SOW-0027b confirmed in scope ledger: `SOW-0027b | IN | PKG-018 | DEL-018-05 | OBJ-001, OBJ-004 | FALSE | D-006 | Absorbs SOW-0047`
- OBJ-001 confirmed: "Deliver a code-compliant, fully functional maintenance shop addition..."
- OBJ-004 confirmed: "Install and commission all mechanical, plumbing, and water storage systems to operational readiness. This includes the wash bay drainage and mud sump."
- Target deliverables resolved against decomposition: DEL-018-02, DEL-005-02, DEL-005-03, DEL-006-03, DEL-011-05, DEL-014-04, DEL-018-06, DEL-008-04 -- all confirmed present in decomposition

### Assumptions and Decisions
- SUMP-SPEC-001 is recorded as a separate DOCUMENT-type prerequisite (distinct from DEL-005-02/03 general IFC dependency) because the Procedure Prerequisites table lists it as a standalone prerequisite and the Datasheet records Mud Sump Dimensions and Capacity as critical TBD parameters.
- ENV-PERMIT-001 is recorded as TargetType=EXTERNAL (not DOCUMENT) because it represents a regulatory approval/constraint, not simply a document. Confidence is MEDIUM due to conditionality uncertainty documented in Guidance CF-002 and CF-003.
- DEL-018-06 interface is recorded with EstimateImpactClass=INFO because Procedure Step 2.1 frames it as coordination ("as needed") rather than a hard gate.
- Declared downstream rows WASH-BAY-OPS-001 and ENVIRONMENTAL-001 from the original _DEPENDENCIES.md are preserved in the declared sections above but NOT re-emitted as extracted rows because they lack specific evidence of a concrete artifact/information handover in the source documents. They represent operational outcomes rather than information-flow edges.
- The Geotechnical Report is recorded as TargetType=DOCUMENT with reference to SOW-0001 because it is a specific document input, not a deliverable in the decomposition.

### Run 2026-03-26 (SCA-001 Refresh)
- **MODE**: UPDATE | **STRICTNESS**: CONSERVATIVE | **CONSUMER_CONTEXT**: NONE
- **DECOMPOSITION_PATH**: WDMLRL_Decomposition_Claude.md R2 (2026-03-26, SCA-001)
- **SCA-001 impact**: No changes to DEL-018-05 scope or dependencies. SOW-0027b unchanged in R2 decomposition. All 14 existing rows confirmed ACTIVE with LastSeen updated.
- **Warnings**: None.

### Warnings (Run 2026-02-26)
- None. Parent anchor (IMPLEMENTS_NODE) found: 1 row (DEP-018-05-001). No FLOATING_NODE or AMBIGUOUS_ANCHOR conditions.

---

## Run History

| Timestamp | Mode | Strictness | Consumer | Decomposition | Warnings | ANCHOR Active | EXECUTION Active | Total Active |
|---|---|---|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | WDMLRL_Decomposition_Claude.md (R1) | None | 3 | 11 | 14 |
| 2026-03-26 | UPDATE | CONSERVATIVE | NONE | WDMLRL_Decomposition_Claude.md R2 (SCA-001) | None | 3 | 11 | 14 |

---

## Lifecycle Summary

### Extraction Lifecycle
| Status | Count |
|---|---|
| ACTIVE | 14 |
| RETIRED | 0 |

### Closure Lifecycle (ACTIVE rows only)
| SatisfactionStatus | Count |
|---|---|
| PENDING | 9 |
| TBD | 5 |

### By DependencyClass
| Class | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 3 | 0 |
| EXECUTION | 11 | 0 |

---

## Downstream Handoff Notes

**Consumer Context: TASK_ESTIMATING**

The following observations are relevant to downstream task estimating workflows:

### Blocking Dependencies (6 rows)
These dependencies gate meaningful estimating because key scope parameters or quantities cannot be determined without them:

1. **DEP-018-05-004** (DEL-018-02 Site Grading): Drainage grades are not established until site grading is complete. Sump excavation depth and pipe invert levels depend on final grades. Estimating for earthwork quantities is blocked until grading design is available.
2. **DEP-018-05-005** (DEL-005-02 Site Grading Plan): Civil IFC drawing required for all site grading and drainage layout quantities.
3. **DEP-018-05-006** (DEL-005-03 Drainage Plan): Civil IFC drawing required for pipe routing, lengths, invert elevations, and sump connection details. Without this, pipe material quantities and trench excavation volumes cannot be estimated.
4. **DEP-018-05-007** (DEL-006-03 Drain & Vent Plans): Plumbing IFC drawing required for floor drain count, type, and connection specifications. Floor drain count is explicitly TBD in Datasheet.
5. **DEP-018-05-008** (Geotechnical Report SOW-0001): Frost depth and soil conditions required for sump burial depth, structural design, and excavation method. Without this, sump construction method (CIP vs precast) and depth cannot be confirmed.
6. **DEP-018-05-013** (SUMP-SPEC-001): Mud sump dimensions and capacity are TBD. These are the primary quantity drivers for concrete, excavation, and formwork.

### Advisory Dependencies (3 rows)
These dependencies are likely to change quantities, specifications, or procurement approach but are not hard gates:

1. **DEP-018-05-009** (ENV-PERMIT-001): Regulatory outcome may require additional treatment, overflow engineering, or containment features that would change scope and cost. Conditionality is unresolved.
2. **DEP-018-05-010** (DEL-011-05 Wash Bay Enclosure): Floor drain locations depend on wash bay enclosure progress. Pipe routing from floor drain to sump may change if drain locations shift.
3. **DEP-018-05-011** (DEL-014-04 Floor Drains & Sump Drains): Scope boundary conflict CF-001 must be resolved to determine which party provides the wash bay floor drain. This affects the estimating scope for DEL-018-05.

### Estimating Readiness Assessment
DEL-018-05 has **6 BLOCKING dependencies** unresolved. Meaningful quantity takeoff for this deliverable cannot proceed until at minimum the civil IFC drawings (DEL-005-02, DEL-005-03), plumbing IFC drawings (DEL-006-03), and geotechnical report (SOW-0001) are available. The Datasheet records 10 TBD physical parameters that depend on these inputs.

**Recommendation**: Estimating for DEL-018-05 should be flagged as NOT READY for detailed quantity takeoff. Allowance-based or parametric estimating may be used as a placeholder, noting high uncertainty on sump dimensions, pipe material/diameter, and construction method.
