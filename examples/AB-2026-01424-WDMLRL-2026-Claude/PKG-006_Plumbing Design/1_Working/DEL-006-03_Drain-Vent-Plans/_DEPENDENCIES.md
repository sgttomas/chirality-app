# Deliverable Dependencies: DEL-006-03

**Deliverable ID:** DEL-006-03
**Name:** Drain & Vent Plans
**Package:** PKG-006 -- Plumbing Design

---

## Declared Upstream Dependencies

*(Human-owned section. List manually declared upstream dependencies here.)*

- None declared.

## Declared Downstream Dependencies

*(Human-owned section. List manually declared downstream dependencies here.)*

- None declared.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 19
**ANCHOR rows:** 4 (1 IMPLEMENTS_NODE, 3 TRACES_TO_REQUIREMENT)
**EXECUTION rows:** 15 (10 UPSTREAM, 5 DOWNSTREAM)

### ANCHOR Dependencies (Tree Edges)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-006-03-001 | IMPLEMENTS_NODE | SOW-0016 | Complete final plumbing design | HIGH |
| DEP-006-03-002 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant fully functional maintenance shop addition | HIGH |
| DEP-006-03-003 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |
| DEP-006-03-004 | TRACES_TO_REQUIREMENT | OBJ-004 | Plumbing and water systems operational readiness | HIGH |

### EXECUTION Dependencies -- UPSTREAM (Information flows TO this deliverable)

| DependencyID | DependencyType | TargetDeliverableID | TargetName | EstimateImpactClass | Confidence |
|---|---|---|---|---|---|
| DEP-006-03-005 | PREREQUISITE | DEL-001-02 | Architectural Floor Plans | ADVISORY | HIGH |
| DEP-006-03-006 | PREREQUISITE | DEL-002-02 | Foundation Plan | ADVISORY | HIGH |
| DEP-006-03-013 | PREREQUISITE | DEL-002-03 | Structural Framing Plans | ADVISORY | HIGH |
| DEP-006-03-007 | PREREQUISITE | DEL-008-01 | Geotechnical Investigation and Report | BLOCKING | HIGH |
| DEP-006-03-008 | INTERFACE | DEL-005-02 | Site Grading Plan | ADVISORY | HIGH |
| DEP-006-03-014 | INTERFACE | DEL-005-03 | Drainage Plan | ADVISORY | HIGH |
| DEP-006-03-009 | PREREQUISITE | DEL-006-06 | Plumbing Fixture Schedule | BLOCKING | HIGH |
| DEP-006-03-015 | INTERFACE | DEL-001-06 | Reflected Ceiling Plans | ADVISORY | MEDIUM |
| DEP-006-03-016 | INTERFACE | DEL-006-02 | Water Distribution Plans | ADVISORY | MEDIUM |
| DEP-006-03-017 | INTERFACE | DEL-006-04 | Cistern and Pump Details | ADVISORY | MEDIUM |

### EXECUTION Dependencies -- DOWNSTREAM (Information flows FROM this deliverable)

| DependencyID | DependencyType | Target | TargetName | EstimateImpactClass | Confidence |
|---|---|---|---|---|---|
| DEP-006-03-010 | HANDOVER | DEL-006-05 | Septic System Details | ADVISORY | MEDIUM |
| DEP-006-03-018 | HANDOVER | DEL-006-01 | Preliminary Plumbing Design | INFO | MEDIUM |
| DEP-006-03-011 | HANDOVER | PKG-014 | Plumbing and Water Systems Installation | ADVISORY | HIGH |
| DEP-006-03-012 | HANDOVER | PKG-009 | Permitting and Regulatory Compliance | INFO | HIGH |
| DEP-006-03-019 | INTERFACE | DEL-008-04 | As-Built Survey | INFO | MEDIUM |

---

## Run Notes

**Run Date:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** TASK_ESTIMATING

### Paths and Defaults Used

| Parameter | Value | Resolution |
|---|---|---|
| RUN_ROOT | `PKG-006_Plumbing Design/1_Working/DEL-006-03_Drain-Vent-Plans` | Provided by invoker |
| DECOMPOSITION_PATH | `_Decomposition/WDMLRL_Decomposition_Claude.md` | Provided by invoker; validated present |
| SOURCE_DOCS | AUTO | Resolved to: Datasheet.md, Guidance.md, Procedure.md, Specification.md |
| DOC_ROLE_MAP | DEFAULT | Applied default heuristics |
| ANCHOR_DOC | AUTO | Resolved to: Datasheet.md (contains `datasheet` in filename; highest-confidence anchor signal) |
| EXECUTION_DOC_ORDER | AUTO | Resolved to: Procedure.md, Specification.md, Guidance.md (Procedure has strongest workflow/prerequisite signals) |
| _REFERENCES.md | Present | Used for document pointer resolution |

### Decomposition Validation

Decomposition document located and validated. The following identifiers were confirmed:
- SOW-0016: Confirmed in Scope Ledger, maps to PKG-006 / DEL-006-02 thru DEL-006-08
- OBJ-001, OBJ-003, OBJ-004: Confirmed in Objectives section (§5)
- DEL-001-02, DEL-001-06: Confirmed in PKG-001 deliverables
- DEL-002-02, DEL-002-03: Confirmed in PKG-002 deliverables
- DEL-005-02, DEL-005-03: Confirmed in PKG-005 deliverables
- DEL-006-01, DEL-006-02, DEL-006-04, DEL-006-05, DEL-006-06: Confirmed in PKG-006 deliverables
- DEL-008-01, DEL-008-04: Confirmed in PKG-008 deliverables
- PKG-009, PKG-014: Confirmed in Packages section (§6)

### Assumptions and Warnings

- No warnings generated. All integrity checks passed.
- Single IMPLEMENTS_NODE anchor confirmed (SOW-0016).
- The existing register (from prior run) contained 12 rows. This run added 7 new rows (DEP-006-03-013 through DEP-006-03-019) for dependencies that were present in source documents but not previously extracted.
- DEP-006-03-006 was previously mapped to "Structural Floor Plan / Slab Design" targeting DEL-002-02. The Procedure prerequisites table lists "DEL-002-02, DEL-002-03" together. This run retains the DEL-002-02 row and adds a separate DEL-002-03 row (DEP-006-03-013) since the Procedure explicitly names both deliverables.
- DEP-006-03-008 was previously mapped to DEL-005-02. The Procedure prerequisites table lists "DEL-005-02, DEL-005-03" together. This run retains the DEL-005-02 row and adds a separate DEL-005-03 row (DEP-006-03-014).
- DEP-006-03-006 TargetName updated from "Structural Floor Plan / Slab Design" to "Foundation Plan" to match decomposition canonical name for DEL-002-02.
- DEP-006-03-008 TargetName updated from "Civil Grading Plan" to "Site Grading Plan" to match decomposition canonical name for DEL-005-02.

### Edges Not Extracted (with rationale)

- **Structural/Architectural/Mechanical/Civil coordination** (Procedure Step 3.3, Specification REQ-006-03-030): The Procedure lists a general multi-discipline coordination review. Where specific deliverables were named (DEL-001-02, DEL-002-02, DEL-002-03, DEL-005-02, DEL-005-03, DEL-001-06), dedicated rows were created. The generic "confirm no conflicts with mechanical equipment or ductwork" statement was not extracted because no specific deliverable or artifact transfer is named -- this is coordination, not information flow.
- **Applicable codes / Alberta Safety Codes** (Procedure prerequisites): These are external regulatory standards, not deliverable-to-deliverable information flow. Not extracted as dependency rows.
- **Existing building drainage information** (Procedure prerequisite for SOW-0072 renovation): The Procedure notes this data is TBD and must be obtained via field investigation. No deliverable source is identified. Not extracted because no specific deliverable target exists.
- **DEL-006-07 (Plumbing Calculation Package)**: Pipe sizing calculations are produced as part of DEL-006-03 work but are a separate deliverable. No explicit information flow dependency is stated from DEL-006-03 to DEL-006-07 in the source documents. Not extracted.

---

## Run History

| Run # | Date | Mode | Strictness | Consumer | Decomp Status | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | Prior run (no metadata recorded) | None | 4 | 8 |
| 2 | 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | Validated | None | 4 | 15 |

---

## Lifecycle Summary

| Metric | Count |
|---|---|
| Total rows | 19 |
| ACTIVE | 19 |
| RETIRED | 0 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 19 |
| PENDING | 0 |
| IN_PROGRESS | 0 |
| SATISFIED | 0 |
| WAIVED | 0 |
| NOT_APPLICABLE | 0 |

---

## Downstream Handoff Notes

**Consumer Context:** TASK_ESTIMATING

### Estimating-Critical Dependencies

The following UPSTREAM dependencies are classified as **BLOCKING** for task estimating purposes -- scope or key quantities cannot be established without these inputs:

1. **DEP-006-03-007** -- DEL-008-01 (Geotechnical Investigation and Report): Frost depth data is the key input for determining minimum burial depth of exterior drain lines and the mud sump connection. Without this data, pipe lengths and insulation requirements for below-grade drain runs cannot be estimated.

2. **DEP-006-03-009** -- DEL-006-06 (Plumbing Fixture Schedule): Fixture unit load data from this schedule is required before pipe sizing can commence (Procedure Step 2.3 verification gate). Without fixture counts and types, drain pipe sizes and vent pipe sizes cannot be determined, which directly affects material quantities.

### Advisory Dependencies

The following UPSTREAM dependencies are classified as **ADVISORY** -- they are likely to change quantities, specs, or approach but are not hard gates for estimating:

- **DEP-006-03-005** (DEL-001-02): Architectural floor plans define fixture locations and room dimensions. Changes may shift drain routing and pipe lengths.
- **DEP-006-03-006** (DEL-002-02): Foundation plan provides slab constraints affecting sleeve locations and below-slab routing.
- **DEP-006-03-013** (DEL-002-03): Structural framing plans provide service pit geometry and additional slab coordination data.
- **DEP-006-03-008** (DEL-005-02): Site grading plan affects whether gravity drain to mud sump and septic is achievable or pumping is needed.
- **DEP-006-03-014** (DEL-005-03): Drainage plan provides additional exterior grade context.
- **DEP-006-03-015** (DEL-001-06): Reflected ceiling plans affect vent stack roof penetration locations.
- **DEP-006-03-016** (DEL-006-02): Water distribution plans affect trap primer design and cross-system coordination.
- **DEP-006-03-017** (DEL-006-04): Cistern/pump details affect water supply system integration.

### Downstream Handoffs Relevant to Estimating

- **DEP-006-03-010** (DEL-006-05 Septic Details): Drain routing data is an input to septic system design. Septic estimating may be blocked if drain connection point is not established.
- **DEP-006-03-011** (PKG-014 Installation): IFC drawings are the primary construction document for the plumbing installer. Installation estimating requires at minimum preliminary drain/vent layouts.
