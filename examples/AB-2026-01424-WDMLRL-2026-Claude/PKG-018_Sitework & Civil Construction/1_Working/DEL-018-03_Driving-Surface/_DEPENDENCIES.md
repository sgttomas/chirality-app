# DEL-018-03_Driving-Surface | Dependencies

## Dependency Tracking Status
**Tracking Status**: TRACKED
**Register Schema**: v3.1
**Last Run**: 2026-03-26

---

## Upstream Dependencies (Declared)
Dependencies that must be satisfied before this deliverable can proceed:

| Dependency ID | Description | Status | Notes |
|---------------|-------------|--------|-------|
| DEL-018-01 | Topsoil Stripping — must precede gravel placement on all surface areas | Pending | SOW-0075; PRE-02 |
| DEL-018-02 | Site Grading & Landscaping — must precede gravel placement for correct sub-base elevation and drainage slope | Pending | SOW-0076; PRE-03 |
| DEL-005-04 | Driving Surface & Pad Layout Plan — IFC civil drawings required (HOLD POINT) | Pending | SOW-0018; PRE-01 |
| DEL-005-07 | Civil Specification — defines aggregate type, gradation, depth, compaction standard | Pending | Critical design input; PRE-01 |
| DEL-008-01 | Geotechnical Investigation — subgrade CBR informs civil design decisions | Pending | Interface; design input via PKG-005 |
| DEL-008-03 | Construction Survey — control points for layout verification | Pending | PRE-07 |
| DEL-019-04 | Construction Quality Control — QC plan must be active | Pending | PRE-06; SOW-0089 |
| SOW-0203 (External) | Owner Aggregate Supply — County/Landfill supplies gravel (OUT of Contractor scope) | Pending | Explicit scope boundary; RFP SS3.3.1 |
| DEL-005-02 | Site Grading Plan — drainage integration required | Pending | Interface; REQ-018-03-05 |
| DEL-005-03 | Drainage Plan — drainage integration required | Pending | Interface; Guidance Principle 5 |

## Downstream Dependencies (Declared)
Deliverables that depend on completion of this deliverable:

| Dependent ID | Description | Status | Notes |
|--------------|-------------|--------|-------|
| DEL-016-01 | Two 5-Tonne Overhead Cranes — stable access for crane delivery | Pending | Schedule enabler |
| PKG-017 | Building Construction — stable site access for construction traffic | Pending | Schedule enabler |
| DEL-008-04 | As-Built Survey — as-built dimensions and elevations provided | Pending | Handover |

---

## Extracted Dependency Register

**Total rows**: 15
**ANCHOR rows**: 2 (1 IMPLEMENTS_NODE, 1 TRACES_TO_REQUIREMENT)
**EXECUTION rows**: 13 (UPSTREAM: 10, DOWNSTREAM: 3)

| DependencyID | Class | AnchorType | Dir | Type | TargetType | Target | Confidence | Status |
|---|---|---|---|---|---|---|---|---|
| DEP-018-03-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | SOW-0077 | HIGH | ACTIVE |
| DEP-018-03-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | WBS_NODE | OBJ-001 | HIGH | ACTIVE |
| DEP-018-03-003 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-018-01 (Topsoil Stripping) | HIGH | ACTIVE |
| DEP-018-03-004 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-018-02 (Site Grading & Landscaping) | HIGH | ACTIVE |
| DEP-018-03-005 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-005-04 (Driving Surface & Pad Layout Plan) | HIGH | ACTIVE |
| DEP-018-03-006 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-005-07 (Civil Specification) | HIGH | ACTIVE |
| DEP-018-03-007 | EXECUTION | N/A | UPSTREAM | INTERFACE | DELIVERABLE | DEL-008-01 (Geotechnical Investigation) | MEDIUM | ACTIVE |
| DEP-018-03-008 | EXECUTION | N/A | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-03 (Construction Survey) | HIGH | ACTIVE |
| DEP-018-03-009 | EXECUTION | N/A | UPSTREAM | CONSTRAINT | DELIVERABLE | DEL-019-04 (Construction Quality Control) | MEDIUM | ACTIVE |
| DEP-018-03-010 | EXECUTION | N/A | UPSTREAM | CONSTRAINT | EXTERNAL | Owner Aggregate Supply (SOW-0203) | HIGH | ACTIVE |
| DEP-018-03-011 | EXECUTION | N/A | UPSTREAM | INTERFACE | DELIVERABLE | DEL-005-02 (Site Grading Plan) | MEDIUM | ACTIVE |
| DEP-018-03-012 | EXECUTION | N/A | UPSTREAM | INTERFACE | DELIVERABLE | DEL-005-03 (Drainage Plan) | MEDIUM | ACTIVE |
| DEP-018-03-013 | EXECUTION | N/A | DOWNSTREAM | ENABLES | DELIVERABLE | DEL-016-01 (Overhead Cranes) | MEDIUM | ACTIVE |
| DEP-018-03-014 | EXECUTION | N/A | DOWNSTREAM | ENABLES | PACKAGE | PKG-017 (Building Construction) | MEDIUM | ACTIVE |
| DEP-018-03-015 | EXECUTION | N/A | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-008-04 (As-Built Survey) | MEDIUM | ACTIVE |

---

## Run Notes

**Run Date**: 2026-02-26
**Mode**: UPDATE (initial run; no prior Dependencies.csv existed)
**Strictness**: CONSERVATIVE
**Consumer Context**: TASK_ESTIMATING

### Paths Used
- **RUN_ROOT**: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude`
- **DELIVERABLE_PATH**: `PKG-018_Sitework & Civil Construction/1_Working/DEL-018-03_Driving-Surface/`
- **DECOMPOSITION_PATH**: `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1 -- 2026-02-25; confirmed available and used for validation)

### Source Documents Scanned (AUTO)
| Doc | Role | Notes |
|---|---|---|
| Datasheet.md | ANCHOR_DOC (primary) | Contains Identification table with SOW-0077, OBJ-001; Attributes; Conditions; References |
| Specification.md | EXECUTION_DOC | Contains requirements REQ-018-03-01 through REQ-018-03-11; Verification table |
| Guidance.md | EXECUTION_DOC | Contains Principles, Considerations, Trade-offs |
| Procedure.md | EXECUTION_DOC | Contains Prerequisites PRE-01 through PRE-08; Steps; Verification V-01 through V-11 |

### Defaults Applied
- SOURCE_DOCS = AUTO: all four production documents scanned (Datasheet.md, Specification.md, Guidance.md, Procedure.md)
- ANCHOR_DOC = AUTO: selected Datasheet.md (contains `datasheet` keyword; has Identification table with explicit SOW/OBJ references)
- EXECUTION_DOC_ORDER = AUTO: Procedure.md (strongest prerequisite signal), Specification.md (requirements), Guidance.md (considerations)
- DOC_ROLE_MAP = DEFAULT

### Read-Only Inputs
- `_REFERENCES.md`: read; used to confirm R-01 and R-07 document pointers. No dependency rows emitted solely from reference listing.
- `_CONTEXT.md`: read; used to confirm deliverable identity, SOW-0077, OBJ-001.

### Decomposition Validation
- Decomposition file located and read: `WDMLRL_Decomposition_Claude.md` (R1 -- 2026-02-25)
- Confirmed DEL-018-03 exists in PKG-018 deliverable table (line 550): Name = "Gravel Driving Surface", SOW-0077, OBJ-001
- Confirmed SOW-0077 in scope ledger (line 670): IN scope, PKG-018, DEL-018-03
- All target deliverable IDs validated against decomposition deliverable tables:
  - DEL-018-01 (PKG-018, line 548), DEL-018-02 (PKG-018, line 549), DEL-005-04 (PKG-005, line 426), DEL-005-07 (PKG-005, line 429), DEL-008-01 (PKG-008, line 457), DEL-008-03 (PKG-008, line 459), DEL-019-04 (PKG-019, line 562), DEL-005-02 (PKG-005, line 424), DEL-005-03 (PKG-005, line 425), DEL-016-01 (PKG-016, line 533), DEL-008-04 (PKG-008, line 460)
- OBJ-001 confirmed in objectives table (line 302)

### Integrity Check Results
- Parent anchor check: 1 ACTIVE IMPLEMENTS_NODE row (DEP-018-03-001 -> SOW-0077). PASS.
- No FLOATING_NODE warning.
- No AMBIGUOUS_ANCHOR warning.
- All DependencyIDs unique (15/15). PASS.
- All ACTIVE rows have EvidenceFile and SourceRef. PASS.
- All enums are canonical write-form. PASS.
- FromDeliverableID = DEL-018-03 for all rows. PASS.
- TargetDeliverableID populated only for TargetType=DELIVERABLE. PASS.
- TargetRefID used for non-deliverable anchor targets (SOW-0077, OBJ-001). PASS.

### Run 2026-03-26 (SCA-001 Refresh)
- **MODE**: UPDATE | **STRICTNESS**: CONSERVATIVE | **CONSUMER_CONTEXT**: NONE
- **DECOMPOSITION_PATH**: WDMLRL_Decomposition_Claude.md R2 (2026-03-26, SCA-001)
- **SCA-001 impact**: No changes to DEL-018-03 scope or dependencies. SOW-0077 unchanged in R2 decomposition. All 15 existing rows confirmed ACTIVE with LastSeen updated.
- **Warnings**: None.

### Warnings (Run 2026-02-26)
- None.

### Assumptions Logged
- DEP-018-03-007 (DEL-008-01 Geotechnical Investigation): Dependency is indirect -- geotechnical data is a design input to PKG-005 civil design, which in turn governs this deliverable. Included because the source documents explicitly state the relationship (Datasheet References, Guidance Principle 4). Confidence = MEDIUM.
- DEP-018-03-015 (DEL-008-04 As-Built Survey): The deliverable ID DEL-008-04 is noted in the source Guidance Conflict Table as potentially ambiguous with DEL-005-04. Row preserved as stated in Procedure Step 4.4; project manager confirmation recommended.

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-02-26 | UPDATE (initial) | CONSERVATIVE | WDMLRL_Decomposition_Claude.md R1 (validated) | None | 2 | 13 | 15 |
| 2 | 2026-03-26 | UPDATE | CONSERVATIVE | WDMLRL_Decomposition_Claude.md R2 (SCA-001) | None | 2 | 13 | 15 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 15 |
| RETIRED | 0 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| PENDING | 12 |
| TBD | 3 |

Note: The 3 TBD rows are downstream dependencies (DEP-018-03-013, DEP-018-03-014, DEP-018-03-015) whose satisfaction status cannot be determined at this stage since they represent outputs from this deliverable.

---

## Downstream Handoff Notes (CONSUMER_CONTEXT = TASK_ESTIMATING)

### Estimating Readiness Assessment

This deliverable has **4 BLOCKING upstream dependencies** that gate meaningful estimating:

| DependencyID | Target | EstimateImpactClass | Rationale |
|---|---|---|---|
| DEP-018-03-005 | DEL-005-04 (Driving Surface & Pad Layout Plan) | BLOCKING | HOLD POINT. Cannot determine surface area/extent without IFC layout drawings. Quantities for gravel placement, spreading, and compaction are unknown without this input. |
| DEP-018-03-006 | DEL-005-07 (Civil Specification) | BLOCKING | Cannot determine gravel depth/thickness, aggregate type/gradation, or compaction standard without civil specification. These parameters directly govern material quantities, equipment requirements, and testing scope. |
| DEP-018-03-003 | DEL-018-01 (Topsoil Stripping) | BLOCKING | Predecessor work scope. Estimating for this deliverable may need to consider sequencing cost implications. |
| DEP-018-03-004 | DEL-018-02 (Site Grading & Landscaping) | BLOCKING | Predecessor work scope. Subgrade condition directly affects gravel placement approach. |

**Additional BLOCKING constraint:**
| DEP-018-03-010 | Owner Aggregate Supply (SOW-0203) | BLOCKING | Aggregate is Owner-supplied (OUT of Contractor scope). This affects the estimating model: Contractor estimates labour/equipment/placement only, NOT material procurement. However, Contractor must plan for aggregate receipt, staging, and incoming acceptance verification. |

### ADVISORY dependencies (may change quantities/specs):

| DependencyID | Target | EstimateImpactClass | Rationale |
|---|---|---|---|
| DEP-018-03-007 | DEL-008-01 (Geotechnical Investigation) | ADVISORY | Subgrade CBR influences design thickness; may change gravel quantities. |
| DEP-018-03-008 | DEL-008-03 (Construction Survey) | ADVISORY | Survey control points needed; minor cost impact on estimating. |
| DEP-018-03-011 | DEL-005-02 (Site Grading Plan) | ADVISORY | Drainage integration may affect surface geometry and quantities. |
| DEP-018-03-012 | DEL-005-03 (Drainage Plan) | ADVISORY | Drainage design may affect edge treatment and cross-slope requirements. |
| DEP-018-03-013 | DEL-016-01 (Overhead Cranes) | ADVISORY | Downstream consumer; may affect timing/staging but not direct cost. |
| DEP-018-03-014 | PKG-017 (Building Construction) | ADVISORY | Downstream consumer; may affect maintenance during construction costs. |

### Key Estimating Constraints
1. **Scope split**: Contractor scope is labour, equipment, and placement ONLY. Aggregate supply is Owner responsibility (SOW-0203). Estimating must reflect this split.
2. **Missing design data**: Gravel depth/thickness, aggregate gradation, compaction standard, and exact surface area extent are all TBD pending civil design (DEL-005-04, DEL-005-07). Estimating at this stage can only be parametric or allowance-based.
3. **Approximate dimensions available**: Datasheet provides one gravel pad area at approximately 60' x 130' (from conceptual drawings), but this does not represent the full driving surface extent.
4. **Incoming acceptance obligation**: Contractor must verify Owner-supplied aggregate against civil specification (REQ-018-03-07A). This adds inspection/verification labour to the estimate.
