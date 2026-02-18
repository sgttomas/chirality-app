# Dependencies

**Deliverable ID:** DEL-03-03
**Deliverable Name:** Structural Design Brief
**Package:** PKG-003 -- Design Brief
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 15
**Total RETIRED rows:** 0

| Class | Count |
|-------|-------|
| ANCHOR | 5 |
| EXECUTION | 10 |

### ANCHOR Rows (5 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-03-03-001 | IMPLEMENTS_NODE | WBS_NODE | PKG-003 -- Design Brief | HIGH |
| DEP-03-03-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0011 | HIGH |
| DEP-03-03-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0014 | HIGH |
| DEP-03-03-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-004 | HIGH |
| DEP-03-03-005 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-005 | HIGH |

### EXECUTION Rows (10 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-03-03-006 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-03 Structural Concept Narrative | HIGH |
| DEP-03-03-007 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-02 Civil Site Concept Plan | HIGH |
| DEP-03-03-008 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-01 Architectural Design Brief | HIGH |
| DEP-03-03-009 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-04-02 Mechanical Energy and Solar Readiness | HIGH |
| DEP-03-03-010 | UPSTREAM | PREREQUISITE | DOCUMENT | Geotechnical Investigation Report (USG1123) | HIGH |
| DEP-03-03-011 | UPSTREAM | PREREQUISITE | DOCUMENT | RFP + Addenda (01/02/03) | HIGH |
| DEP-03-03-012 | UPSTREAM | CONSTRAINT | EXTERNAL | Owner Equipment List / Clearance Dimensions | MEDIUM |
| DEP-03-03-013 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-03-06 Accessibility and Adaptability Narrative | HIGH |
| DEP-03-03-014 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-05-02 Structural Durability and Maintenance | HIGH |
| DEP-03-03-015 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02 Formal Submission Package | HIGH |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

**Defaults and Paths Used:**
- DECOMPOSITION_PATH: `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL, located automatically)
- ANCHOR_DOC: `Datasheet.md` (selected by heuristic: contains deliverable identification, scope items, objectives, RFP references)
- EXECUTION_DOC_ORDER: `Procedure.md`, `Specification.md`, `Guidance.md` (Procedure contains explicit prerequisites and steps; Specification contains requirements; Guidance contains considerations and trade-offs)
- SOURCE_DOCS: `Datasheet.md`, `Specification.md`, `Procedure.md`, `Guidance.md` (AUTO: all non-generated .md files in deliverable folder excluding dependency/reference/context/status/semantic artifacts)
- _REFERENCES.md: read and used to resolve document pointers

**Decomposition Status:** Available. v2.3 FINAL. All anchor targets validated against decomposition.

**Assumptions:**
- Equipment clearance dimensions (DEP-03-03-012) are marked MEDIUM confidence because the source document itself notes the equipment list details are TBD from Owner or manufacturer data.
- OBJ-005 trace (DEP-03-03-005) is included because the Datasheet explicitly states "supporting evidence for OBJ-005" even though OBJ-004 is the primary objective.

**Warnings:** None.

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|-----|------|------|------------|---------------|----------|-------------|
| 1 | 2026-02-17 | UPDATE | CONSERVATIVE | v2.3 FINAL (available) | None | 15 (5 ANCHOR + 10 EXECUTION) |

---

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 15 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|--------------------|-------|
| TBD | 15 |

---
