# DEL-005-05 Dependencies

## Upstream Dependencies

### ANCHOR: Parent Definition Node
- **SOW-0015** — Complete final civil design including site grading plan with drainage features and components (PKG-005 Civil Design)

### ANCHOR: Traced Objectives
- **OBJ-001** — Deliver a code-compliant, fully functional maintenance shop addition
- **OBJ-003** — Produce complete, P.Eng.-stamped IFC design documentation across all disciplines

### EXECUTION: Prerequisites (must be substantially complete before IFC stamp)
- **DEL-008-01** (PKG-008) — Geotechnical Investigation & Report: subgrade bearing, CBR, frost depth, soil classification, groundwater depth
- **DEL-008-02** (PKG-008) — Preliminary Site Survey: existing grade elevations, survey datum/benchmark
- **DEL-005-02** (PKG-005) — Site Grading Plan: grading intent and finished grades
- **DEL-005-03** (PKG-005) — Drainage Plan: drainage structure types and inverts
- **DEL-005-04** (PKG-005) — Driving Surface & Pad Layout Plan: pad locations and dimensions
- **DEL-005-07** (PKG-005) — Civil Specification: material specifications for cross-reference
- **DEL-005-01** (PKG-005) — Preliminary Civil Design: County approval before final IFC

### EXECUTION: Interfaces (coordination required for detail finalization)
- **PKG-006** (Plumbing Design) — Wash bay drain connection invert and mud sump pipe sizing
- **PKG-004** (Electrical Design) — Utility crossing locations for gas, electrical, communications
- **PKG-002** (Structural Design) — Civil-structural interface at foundation walls, sump drains, pad edges

### EXECUTION: Constraints
- **PKG-009** (Permitting) — Development/building permit conditions may impose grading or drainage standards
- **RFP** (AB-2026-01424-WDMLRL_RFP.pdf) — Sections 3.3.2 and 3.4 establish mandatory design requirements

## Downstream Dependencies

### EXECUTION: Handovers (this deliverable produces output consumed by)
- **PKG-018** (Sitework & Civil Construction) — IFC civil sections issued for pricing and construction
- **DEL-005-06** (PKG-005) — Civil Calculation Package: sections must be consistent with calculation outputs

## Internal Dependencies

No additional internal dependencies beyond sibling deliverables already listed above.

## External Dependencies

- **RFP** — AB-2026-01424-WDMLRL_RFP.pdf (governing contract document, sections 3.3.2 and 3.4)

## NOT_TRACKED Dependencies

- Coordination-only relationships (e.g., weekly meetings, general alignment) are not tracked per information-flow-only extraction policy.
- Structural adjacency relationships obvious from decomposition (e.g., DEL-005-05 is in PKG-005) are not duplicated as EXECUTION edges.

## Tracking Notes

Dependencies will be updated as project progresses and scope is refined.

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total ACTIVE rows:** 17
**Total RETIRED rows:** 0

| DependencyID | Class | AnchorType | Dir | Type | TargetType | Target | Status |
|---|---|---|---|---|---|---|---|
| DEP-005-05-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | SOW-0015 | ACTIVE |
| DEP-005-05-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-001 | ACTIVE |
| DEP-005-05-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-003 | ACTIVE |
| DEP-005-05-004 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-01 Geotech Report | ACTIVE |
| DEP-005-05-005 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-02 Preliminary Survey | ACTIVE |
| DEP-005-05-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-005-02 Site Grading Plan | ACTIVE |
| DEP-005-05-007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-005-03 Drainage Plan | ACTIVE |
| DEP-005-05-008 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-005-04 Driving Surface Layout | ACTIVE |
| DEP-005-05-009 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-005-07 Civil Specification | ACTIVE |
| DEP-005-05-010 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-005-01 Preliminary Civil Design | ACTIVE |
| DEP-005-05-011 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | PKG-006 Plumbing (mud sump) | ACTIVE |
| DEP-005-05-012 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | PKG-004 Electrical (utility crossings) | ACTIVE |
| DEP-005-05-013 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | PKG-002 Structural (interfaces) | ACTIVE |
| DEP-005-05-014 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | DELIVERABLE | PKG-009 Permitting | ACTIVE |
| DEP-005-05-015 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | PKG-018 Sitework Construction | ACTIVE |
| DEP-005-05-016 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-005-06 Calculation Package | ACTIVE |
| DEP-005-05-017 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | DOCUMENT | RFP (AB-2026-01424) | ACTIVE |

---

## Run Notes

**Run Date:** 2026-02-26
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** TASK_ESTIMATING
**Decomposition Path:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md
**Decomposition Status:** Available; R1 2026-02-25. Used for anchor validation and target resolution.

**Source Documents Scanned (AUTO):**
- **ANCHOR_DOC:** Datasheet.md (selected by heuristic: filename contains "datasheet")
- **EXECUTION_DOCS (ordered):** Procedure.md, Specification.md, Guidance.md
- **Supporting:** _CONTEXT.md, _REFERENCES.md (read-only reference)

**Defaults Applied:**
- SOURCE_DOCS: AUTO -- scanned Datasheet.md, Procedure.md, Specification.md, Guidance.md
- ANCHOR_DOC: AUTO -- selected Datasheet.md
- EXECUTION_DOC_ORDER: AUTO -- Procedure.md (highest workflow clarity), Specification.md, Guidance.md

**Assumptions:**
- ASSUMPTION: OBJ-001 and OBJ-003 objective anchors are based on decomposition Section 7 PKG-005 table and Datasheet identification. The Datasheet notes this is a "best-effort mapping" not confirmed at individual deliverable level.
- ASSUMPTION: DEL-005-06 downstream handover is implicit; Datasheet references it as containing "design inputs for sections" suggesting bidirectional data flow.

**Warnings:**
- None. Parent anchor (IMPLEMENTS_NODE) found: SOW-0015. Decomposition validation passed.

**Integrity Checks Passed:**
- Parent anchor count: 1 (SOW-0015) -- OK
- DependencyID uniqueness: 17 unique IDs -- OK
- All ACTIVE rows have EvidenceFile and SourceRef -- OK
- Schema columns present and CSV parseable -- OK
- Enum values canonical -- OK
- _DEPENDENCIES.md counts consistent with Dependencies.csv -- OK

**_REFERENCES.md Coverage Note:**
- _REFERENCES.md lists R-01 and R-07 only. Datasheet also cites R-04 (Appendix B Shop). Dependency rows referencing documents use source document paths as available. No dependency rows were created solely from _REFERENCES.md listings.

---

## Run History

| Run | Date | Mode | Strictness | Consumer | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|---|---|
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | TASK_ESTIMATING | R1 2026-02-25 (available) | None | 17 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 17 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| PENDING | 12 |
| TBD | 5 |

| DependencyClass | ACTIVE Count |
|---|---|
| ANCHOR | 3 |
| EXECUTION | 14 |

| EstimateImpactClass | Count |
|---|---|
| BLOCKING | 7 |
| ADVISORY | 6 |
| INFO | 3 |
| TBD | 1 |

---

## Downstream Handoff Notes

**Consumer Context: TASK_ESTIMATING**

The following observations are relevant for task estimating consumers:

1. **BLOCKING dependencies (7 rows):** DEL-005-05 has seven dependencies classified as BLOCKING for estimating readiness. The most significant are the geotechnical report (DEL-008-01) and preliminary survey (DEL-008-02), which gate all final section layer thicknesses. Without geotech data, gravel section depths, subbase requirements, and frost depth design parameters cannot be confirmed -- these directly affect material quantity estimates. The three sibling deliverable prerequisites (DEL-005-02 Grading, DEL-005-03 Drainage, DEL-005-01 Preliminary Design approval) also gate scope clarity. The downstream handover to PKG-018 is BLOCKING because construction pricing depends on receiving the IFC drawing set.

2. **ADVISORY dependencies (6 rows):** The pad layout (DEL-005-04), civil specification (DEL-005-07), plumbing interface (PKG-006), electrical/utility interface (PKG-004), structural interface (PKG-002), and permitting (PKG-009) are ADVISORY. These may change quantities or specifications but are not hard gates on preliminary estimating. They are expected to be resolved during detailed design coordination.

3. **Key unknowns for estimating:**
   - Gravel section thickness (TBD pending geotech -- affects material volume)
   - Frost depth subbase requirement (TBD pending geotech -- affects excavation depth)
   - Retaining wall inclusion/exclusion (TBD pending grading design -- potential scope add)
   - Drainage structure types (TBD pending drainage plan -- affects detail complexity)
   - Mud sump dimensions (TBD pending PKG-006 coordination -- affects excavation and concrete quantities)

4. **Stage context:** All dependencies are within the design stage. No construction-stage dependencies are present except the downstream handover to PKG-018.
