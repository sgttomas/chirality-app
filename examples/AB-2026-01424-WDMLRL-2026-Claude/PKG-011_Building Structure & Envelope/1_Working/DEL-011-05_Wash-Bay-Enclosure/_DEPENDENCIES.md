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

### Run 2026-02-26 (Initial Extraction)

**Mode:** UPDATE | **Strictness:** CONSERVATIVE | **Consumer Context:** TASK_ESTIMATING
**Decomposition Path:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1 -- 2026-02-25) -- FOUND.
**Source Documents:** ANCHOR_DOC: Datasheet.md; EXECUTION_DOCS: Procedure.md, Specification.md, Guidance.md
**Warnings:** None.

### Run 2026-03-26 (SCA-001 Refresh)

**Mode:** UPDATE | **Strictness:** CONSERVATIVE | **Consumer Context:** NONE
**Decomposition Path:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (R2 -- 2026-03-26, SCA-001)

**SCA-001 Changes Affecting This Deliverable:**
- SOW-0027a text unchanged in substance. The wash bay enclosure scope (enclosed wash bay structure, single bay, 24' wide, motor scraper-sized, overhead door, walls, roof integration, steel plate floor) remains as previously decomposed.
- The precast concrete walls clarification (Add. 2/4) may affect wash bay wall construction type (precast vs. other) but this is a design detail captured in the IFC drawing prerequisites (DEP-011-05-E05, E06), not a new dependency edge.

**Changes Applied:**
- Updated LastSeen to 2026-03-26 on all 18 ACTIVE rows.
- No new rows added. No rows retired. No statement changes.

**Warnings:** None.

**Integrity Check Results:**
- Parent anchor (IMPLEMENTS_NODE): 1 ACTIVE row (DEP-011-05-A01 -> SOW-0027a) -- PASS
- DependencyID uniqueness: PASS (18 unique IDs)
- All ACTIVE rows have EvidenceFile + SourceRef: PASS
- FromDeliverableID consistency: PASS
- Schema version: v3.1 on all rows -- PASS

---

## Run History

| Run | Timestamp | Mode | Strictness | Consumer | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | FOUND (R1 2026-02-25) | None | 2 | 16 | 18 |
| 2 | 2026-03-26 | UPDATE | CONSERVATIVE | NONE | FOUND (R2 2026-03-26 SCA-001) | None | 2 | 16 | 18 |

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

| DependencyClass | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 2 | 0 |
| EXECUTION | 16 | 0 |
