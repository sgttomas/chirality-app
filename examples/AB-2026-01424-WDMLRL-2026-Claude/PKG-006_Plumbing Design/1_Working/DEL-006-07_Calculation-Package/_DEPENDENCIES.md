# Deliverable Dependencies: DEL-006-07

**Deliverable ID:** DEL-006-07
**Name:** Plumbing Calculation Package
**Package:** PKG-006 -- Plumbing Design

## Declared Upstream Dependencies

- Document inter-deliverable relationships as they emerge
- Track blockers and sequencing requirements
- Update as project progresses

## Declared Downstream Dependencies

_(None declared. See Extracted Dependency Register below for extracted downstream edges.)_

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total ACTIVE rows:** 16
**Total RETIRED rows:** 0

### ANCHOR Edges (3 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence | Status |
|---|---|---|---|---|---|
| DEP-006-07-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0016 | HIGH | ACTIVE |
| DEP-006-07-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-003 -- P.Eng.-stamped IFC documentation | HIGH | ACTIVE |
| DEP-006-07-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-004 -- Mechanical/plumbing/water systems operational readiness | HIGH | ACTIVE |

### EXECUTION Edges -- UPSTREAM (7 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | Confidence | SatisfactionStatus | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-006-07-004 | PREREQUISITE | DELIVERABLE | DEL-006-06 -- Plumbing Fixture Schedule | HIGH | PENDING | BLOCKING |
| DEP-006-07-005 | PREREQUISITE | DELIVERABLE | DEL-001-02 -- Architectural Floor Plans | MEDIUM | PENDING | BLOCKING |
| DEP-006-07-006 | PREREQUISITE | DELIVERABLE | DEL-008-01 -- Geotechnical Investigation and Report | MEDIUM | PENDING | ADVISORY |
| DEP-006-07-007 | CONSTRAINT | DOCUMENT | R-01 -- RFP | HIGH | SATISFIED | INFO |
| DEP-006-07-008 | CONSTRAINT | DOCUMENT | R-06 -- Appendix B (Plumbing) | HIGH | SATISFIED | INFO |
| DEP-006-07-009 | CONSTRAINT | DOCUMENT | National Plumbing Code of Canada (NPC) | MEDIUM | PENDING | BLOCKING |
| DEP-006-07-016 | CONSTRAINT | EXTERNAL | Alberta Safety Codes Officer -- Plumbing permit requirements | HIGH | PENDING | BLOCKING |

### EXECUTION Edges -- DOWNSTREAM (6 ACTIVE)

| DependencyID | DependencyType | TargetType | Target | Confidence | SatisfactionStatus | EstimateImpactClass |
|---|---|---|---|---|---|---|
| DEP-006-07-010 | HANDOVER | DELIVERABLE | DEL-006-02 -- Water Distribution Plans | HIGH | TBD | ADVISORY |
| DEP-006-07-011 | HANDOVER | DELIVERABLE | DEL-006-03 -- Drain and Vent Plans | HIGH | TBD | ADVISORY |
| DEP-006-07-012 | HANDOVER | DELIVERABLE | DEL-006-04 -- Cistern and Pump Details | HIGH | TBD | ADVISORY |
| DEP-006-07-013 | HANDOVER | DELIVERABLE | DEL-006-05 -- Septic System Details | HIGH | TBD | ADVISORY |
| DEP-006-07-014 | HANDOVER | DELIVERABLE | DEL-006-08 -- Plumbing Specification | HIGH | TBD | ADVISORY |
| DEP-006-07-015 | INTERFACE | PACKAGE | PKG-009 -- Safety Code Permit Application | HIGH | TBD | ADVISORY |

---

## Run Notes

**Run Date:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** TASK_ESTIMATING

### Paths and Defaults Used

| Setting | Value | Resolution |
|---|---|---|
| RUN_ROOT | `PKG-006_Plumbing Design/1_Working/DEL-006-07_Calculation-Package` | Provided by invoker |
| DECOMPOSITION_PATH | `_Decomposition/WDMLRL_Decomposition_Claude.md` | Provided by invoker; file exists and was read successfully |
| SOURCE_DOCS | AUTO | Resolved to: Datasheet.md, Specification.md, Procedure.md, Guidance.md |
| ANCHOR_DOC | AUTO | Resolved to: Datasheet.md (contains Identification table with SOW Reference and Objectives fields) |
| EXECUTION_DOC_ORDER | AUTO | Resolved to: Procedure.md (primary -- contains Prerequisites and Steps), Guidance.md (secondary -- contains Purpose and Considerations), Specification.md (tertiary -- contains Requirements and SOW Traceability) |
| DOC_ROLE_MAP | DEFAULT | Datasheet.md matched ANCHOR_DOC pattern; Procedure.md and Guidance.md matched EXECUTION_DOC patterns; Specification.md matched ANCHOR_DOC pattern (secondary) |
| _REFERENCES.md | Present | Read for document location resolution (R-01, R-06 paths confirmed as _Sources/) |

### Warnings

_(None)_

### Assumptions and Decisions

1. **DEL-001-02 vs DEL-001-01 target resolution:** Procedure.md lists "DEL-001-01 or DEL-001-02 (Architectural Design)" as the source for the architectural floor plan prerequisite. DEL-001-02 (Architectural Floor Plans) was selected as the primary target because it is the more specific artifact for room dimensions and occupancy data. Marked as ASSUMPTION in row notes.
2. **NPC as external document dependency:** The National Plumbing Code of Canada is listed as a required reference in Procedure.md but is not a project deliverable. Recorded as `TargetType=DOCUMENT` with `SatisfactionStatus=PENDING` because the specific edition is TBD.
3. **Safety Codes Officer as external dependency:** The permit requirements and code edition confirmation are gated on an external authority. Recorded as `TargetType=EXTERNAL` with `SatisfactionStatus=PENDING`.
4. **Scope exclusions not recorded as dependencies:** Specification.md mentions PKG-002 (structural), PKG-003 (mechanical), PKG-004 (electrical), PKG-005 (civil) as exclusions. These are scope boundaries, not information-flow dependencies, and are not recorded.
5. **Co-development relationship with DEL-006-06:** The fixture schedule and calculation package are described as "co-developed." This is recorded as an UPSTREAM PREREQUISITE from the perspective of DEL-006-07 (it needs fixture data). The reciprocal edge would be recorded in DEL-006-06's own register.
6. **Extension columns populated:** `EstimateImpactClass` and `ConsumerHint` are populated for EXECUTION rows per CONSUMER_CONTEXT=TASK_ESTIMATING. BLOCKING is assigned to prerequisites/constraints that gate meaningful estimating (fixture schedule, architectural floor plan, NPC edition, Safety Codes Officer confirmation). ADVISORY is assigned to the geotech report (conditional) and all downstream handovers (which affect downstream estimating scope). INFO is assigned to available documents (R-01, R-06).

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | WDMLRL_Decomposition_Claude.md (available; validated) | None | 16 (3 ANCHOR + 13 EXECUTION) |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 16 |
| RETIRED | 0 |

### Closure Status Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 9 |
| PENDING | 5 |
| SATISFIED | 2 |

### By DependencyClass

| DependencyClass | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 3 | 0 |
| EXECUTION | 13 | 0 |

---

## Downstream Handoff Notes (TASK_ESTIMATING)

This section provides guidance for downstream estimating workflows consuming this dependency register.

### Estimating-Critical Dependencies (BLOCKING)

The following upstream dependencies are classified as BLOCKING for estimating readiness. Until these are resolved, meaningful scope and quantity estimation for DEL-006-07 may be incomplete:

1. **DEP-006-07-004 -- DEL-006-06 (Plumbing Fixture Schedule):** The fixture schedule is co-developed with the calculation package. Fixture counts directly determine water demand analysis, supply sizing, and drainage sizing. Without it, pipe sizes and pump selections cannot be finalized.

2. **DEP-006-07-005 -- DEL-001-02 (Architectural Floor Plans):** Room dimensions and building occupancy count are needed for NPC fixture unit calculations. Without occupancy data, water demand and septic loading calculations are based on assumptions.

3. **DEP-006-07-009 -- NPC (National Plumbing Code):** The specific NPC edition is TBD. Code edition determines sizing tables, methods, and compliance criteria. All code-based sizing references remain ASSUMPTION until the edition is confirmed.

4. **DEP-006-07-016 -- Alberta Safety Codes Officer:** Permit requirements and applicable code edition confirmation are gated on this external authority. The code compliance matrix (Step 8 of Procedure.md) cannot be finalized without this input.

### Estimating-Advisory Dependencies (ADVISORY)

The following dependencies are classified as ADVISORY -- they are likely to influence quantities, specifications, or procurement approach but are not hard gates:

5. **DEP-006-07-006 -- DEL-008-01 (Geotechnical Investigation):** Conditional on authority requirements for septic siting. May not be required for a shallow holding tank installation.

6. **DEP-006-07-010 through DEP-006-07-014 -- Downstream IFC drawings and specification:** These consume the calculation package outputs. Changes in the calculation package will propagate to pipe sizes, equipment selections, and specifications shown on drawings.

7. **DEP-006-07-015 -- PKG-009 (Safety Code Permit):** The calculation package is submitted as part of the permit application. Permit timeline depends on calculation package completion.

### Estimating Scope Notes

- The calculation package itself is a design-phase engineering effort. Estimating the production effort requires understanding: (a) the number of calculation sub-domains (9 identified in Datasheet.md); (b) the number of TBD parameters requiring resolution (at least 5 conflict table items); (c) the P.Eng. review and QA/QC cycle.
- Several design parameters are TBD (bulk water fill pump flow rate, simultaneous demand factor, oil/water separator requirement, occupancy count). These are documented in the source documents' Conflict Tables (CFT-001 through CFT-003) and affect the scope of engineering effort.
