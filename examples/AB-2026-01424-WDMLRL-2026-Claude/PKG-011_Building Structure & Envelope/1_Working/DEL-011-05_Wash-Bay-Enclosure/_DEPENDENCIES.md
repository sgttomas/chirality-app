# Dependencies: DEL-011-05 Wash Bay Enclosure

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- DEL-011-01 Superstructure -- Structural support for wash bay must be in place
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- PKG-013 MEP Systems -- Drainage and plumbing systems depend on enclosure completion
- Dependencies coordinated externally by humans.

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total Rows:** 18 (ACTIVE: 18, RETIRED: 0)
**ANCHOR Rows:** 2 | **EXECUTION Rows:** 16
**UPSTREAM:** 12 | **DOWNSTREAM:** 6

### ANCHOR Dependencies

| DependencyID | AnchorType | TargetRefID / TargetName | Confidence | Evidence |
|---|---|---|---|---|
| DEP-011-05-A01 | IMPLEMENTS_NODE | SOW-0027a | HIGH | Datasheet > Identification > SOW Reference |
| DEP-011-05-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | HIGH | Datasheet > Identification > Objective Supported |

### EXECUTION Dependencies -- UPSTREAM (inputs to this deliverable)

| DependencyID | Type | Target | TargetType | Confidence | EstimateImpact |
|---|---|---|---|---|---|
| DEP-011-05-E01 | PREREQUISITE | DEL-011-01 Concrete Superstructure | DELIVERABLE | HIGH | BLOCKING |
| DEP-011-05-E02 | PREREQUISITE | DEL-010-01 Foundation Construction | DELIVERABLE | HIGH | BLOCKING |
| DEP-011-05-E03 | PREREQUISITE | DEL-002-08 Steel Plate Embedment Plan | DELIVERABLE | HIGH | BLOCKING |
| DEP-011-05-E04 | PREREQUISITE | DEL-009-02 Building Permit | DELIVERABLE | HIGH | BLOCKING |
| DEP-011-05-E05 | PREREQUISITE | PKG-001 Architectural Design -- IFC Drawings | PACKAGE | HIGH | BLOCKING |
| DEP-011-05-E06 | PREREQUISITE | PKG-002 Structural Design -- IFC Drawings | PACKAGE | HIGH | BLOCKING |
| DEP-011-05-E07 | INTERFACE | PKG-006 Plumbing Design -- Drain Locations and Floor Slope | PACKAGE | HIGH | BLOCKING |
| DEP-011-05-E08 | INTERFACE | PKG-005 Civil Design -- Floor Drainage Slope | PACKAGE | MEDIUM | ADVISORY |
| DEP-011-05-E09 | INTERFACE | PKG-015 Electrical Installation -- Conduit Coordination | PACKAGE | HIGH | ADVISORY |
| DEP-011-05-E15 | CONSTRAINT | RFP -- IFC Drawing Requirement (P.Eng.-stamped) | DOCUMENT | HIGH | BLOCKING |

### EXECUTION Dependencies -- DOWNSTREAM (outputs from this deliverable)

| DependencyID | Type | Target | TargetType | Confidence | EstimateImpact |
|---|---|---|---|---|---|
| DEP-011-05-E10 | HANDOVER | DEL-018-05 Wash Bay Drainage and Mud Sump | DELIVERABLE | HIGH | BLOCKING |
| DEP-011-05-E11 | HANDOVER | DEL-015-02 Lighting Installation | DELIVERABLE | HIGH | ADVISORY |
| DEP-011-05-E12 | HANDOVER | DEL-015-04 Equipment Power Circuits | DELIVERABLE | MEDIUM | ADVISORY |
| DEP-011-05-E13 | INTERFACE | DEL-011-07 Mezzanine Structure and Stairs | DELIVERABLE | HIGH | BLOCKING |
| DEP-011-05-E14 | HANDOVER | DEL-008-04 As-Built Survey | DELIVERABLE | MEDIUM | INFO |
| DEP-011-05-E16 | INTERFACE | PKG-013 Mechanical and HVAC Installation | PACKAGE | MEDIUM | ADVISORY |

---

## Run Notes

**Run Date:** 2026-02-26
**MODE:** UPDATE
**STRICTNESS:** CONSERVATIVE
**CONSUMER_CONTEXT:** TASK_ESTIMATING
**DECOMPOSITION_PATH:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1 -- 2026-02-25) -- FOUND and used for anchor validation and target resolution.

**Source Documents Scanned (AUTO resolution):**
- **ANCHOR_DOC:** `Datasheet.md` (matched heuristic: `datasheet`)
- **EXECUTION_DOCS (ordered):**
  1. `Procedure.md` (matched heuristic: `procedure`)
  2. `Specification.md` (matched heuristic: `spec`)
  3. `Guidance.md` (matched heuristic: `guidance`)

**Read-Only Inputs Used:**
- `_REFERENCES.md` -- used for document pointer resolution (R-01, R-04 confirmed)
- `_CONTEXT.md` -- used for deliverable identity confirmation

**Defaults Applied:**
- SOURCE_DOCS=AUTO: all four source documents in deliverable folder scanned
- DOC_ROLE_MAP=DEFAULT: Datasheet.md identified as ANCHOR_DOC; Procedure.md, Specification.md, Guidance.md identified as EXECUTION_DOCS
- ANCHOR_DOC=AUTO: resolved to Datasheet.md (contains SOW Reference and Objective Supported fields)
- EXECUTION_DOC_ORDER=AUTO: Procedure.md first (explicit prerequisites table), then Specification.md (requirements), then Guidance.md (considerations)

**Warnings:** None.

**Integrity Check Results:**
- Parent anchor (IMPLEMENTS_NODE): 1 ACTIVE row (DEP-011-05-A01 -> SOW-0027a) -- PASS
- DependencyID uniqueness: PASS (18 unique IDs)
- All ACTIVE rows have EvidenceFile + SourceRef: PASS
- FromDeliverableID consistency: PASS (all rows = DEL-011-05)
- CSV parseability: PASS (31 columns, 18 data rows)
- Schema version: v3.1 on all rows -- PASS
- Enum normalization: all values canonical -- PASS
- _DEPENDENCIES.md counts consistent with Dependencies.csv: PASS

**Assumptions Logged:**
- None. All extracted rows are CONSERVATIVE/EXPLICIT -- no ASSUMPTION-grade rows emitted.

**Observations for Estimating Consumer:**
- 7 UPSTREAM dependencies are marked BLOCKING: these represent hard gates on construction start (superstructure, foundation, embedment plan, building permit, architectural IFC, structural IFC, plumbing design coordination).
- 1 UPSTREAM CONSTRAINT (IFC drawing requirement) is a contractual hard gate reinforcing E05/E06.
- 2 DOWNSTREAM dependencies are marked BLOCKING: DEL-018-05 (drainage) and DEL-011-07 (mezzanine) cannot proceed without this deliverable's outputs.
- Key estimating risk: multiple TBD specifications (door height, steel plate dimensions, wall material, floor drainage slope) depend on IFC drawings that do not yet exist. Estimating should treat these as scope-uncertainty items.

---

## Run History

| Run | Timestamp | Mode | Strictness | Consumer | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | FOUND (R1 2026-02-25) | None | 2 | 16 | 18 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 18 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| PENDING | 16 |
| NOT_APPLICABLE | 2 |
| TBD | 0 |

| DependencyClass | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 2 | 0 |
| EXECUTION | 16 | 0 |

---

## Downstream Handoff Notes

**Consumer Context:** TASK_ESTIMATING

**Blocking Dependencies for Estimating Readiness (EstimateImpactClass = BLOCKING):**

UPSTREAM blockers (7 execution + 1 constraint):
1. **DEP-011-05-E01** -- DEL-011-01 Concrete Superstructure must be in place. Estimating must account for superstructure completion as a predecessor activity.
2. **DEP-011-05-E02** -- DEL-010-01 Foundation Construction must be complete at wash bay location. Foundation is a predecessor to superstructure, creating a chain: Foundation -> Superstructure -> Wash Bay Enclosure.
3. **DEP-011-05-E03** -- DEL-002-08 Steel Plate Embedment Plan must be issued. Without this plan, steel plate dimensions/material/anchorage are TBD -- scope quantities for steel plates cannot be finalized.
4. **DEP-011-05-E04** -- DEL-009-02 Building Permit must be obtained. Administrative prerequisite that gates all construction.
5. **DEP-011-05-E05** -- PKG-001 Architectural IFC Drawings required. Wall construction type, door height, and layout details are TBD until IFC is issued.
6. **DEP-011-05-E06** -- PKG-002 Structural IFC Drawings required. Structural framing, mezzanine support details, and steel plate specifications are TBD until IFC is issued.
7. **DEP-011-05-E07** -- PKG-006 Plumbing Design must confirm drain sleeve locations and floor drainage slope. This information gates formwork layout and the concrete pour.
8. **DEP-011-05-E15** -- Contractual constraint: all construction must follow P.Eng.-stamped IFC drawings (RFP S3.3.2).

DOWNSTREAM blockers (2 execution):
1. **DEP-011-05-E10** -- DEL-018-05 Wash Bay Drainage and Mud Sump depends on enclosure providing drain sleeves and wall penetrations.
2. **DEP-011-05-E13** -- DEL-011-07 Mezzanine Structure and Stairs depends on structural provisions installed at wash bay walls.

**Advisory Dependencies (may affect quantities/specs):**
- DEP-011-05-E08 (Civil design -- floor drainage slope)
- DEP-011-05-E09 (Electrical coordination -- conduit locations)
- DEP-011-05-E11 (Lighting installation depends on enclosure)
- DEP-011-05-E12 (Equipment power circuits depend on conduit stubs)
- DEP-011-05-E16 (Mechanical/HVAC depends on roof blockouts)

**Key Scope Uncertainty Items for Estimating:**
- Overhead door height: TBD (ASSUMPTION 16-20 ft; pending IFC)
- Steel plate dimensions, thickness, material grade: TBD (pending DEL-002-08)
- Wall construction material: TBD (pending IFC -- concrete tilt-up / CMU / steel-stud unknown)
- Wash bay clear ceiling height: TBD (pending structural design for mezzanine above)
- Floor drainage slope: TBD (pending PKG-006 plumbing design)
