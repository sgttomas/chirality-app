# Dependencies

**Deliverable ID:** DEL-02-03
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total ACTIVE rows:** 15
**Total RETIRED rows:** 0

### ANCHOR Dependencies (4 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-02-03-A001 | IMPLEMENTS_NODE | WBS_NODE | PKG-002 -- Conceptual Design | HIGH |
| DEP-02-03-A002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0009 -- Concept design package | HIGH |
| DEP-02-03-A003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0010 -- Embed program clarifications & special requirements | HIGH |
| DEP-02-03-A004 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-003 -- Maximize Proposed Conceptual Design score (20 pts) | HIGH |

### EXECUTION Dependencies (11 ACTIVE)

**Upstream (7 rows):**

| DependencyID | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|
| DEP-02-03-E001 | PREREQUISITE | DELIVERABLE | DEL-02-01 -- Architectural Concept Package | HIGH |
| DEP-02-03-E002 | PREREQUISITE | DELIVERABLE | DEL-02-02 -- Civil Site Concept Plan | HIGH |
| DEP-02-03-E003 | PREREQUISITE | DOCUMENT | Appendix D -- 2021 Geotechnical Investigation Report | HIGH |
| DEP-02-03-E004 | PREREQUISITE | DOCUMENT | Appendix B -- Functional Program | HIGH |
| DEP-02-03-E005 | INTERFACE | DOCUMENT | Appendix E -- Site Grading | MEDIUM |
| DEP-02-03-E006 | PREREQUISITE | DOCUMENT | Addendum 03 (Jul 31 2024) | HIGH |
| DEP-02-03-E007 | CONSTRAINT | EXTERNAL | DEC-013 -- No additional geotechnical investigation | HIGH |

**Upstream Interfaces (2 rows):**

| DependencyID | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|
| DEP-02-03-E008 | INTERFACE | DELIVERABLE | DEL-02-04 -- Mechanical Concept Narrative | HIGH |
| DEP-02-03-E009 | INTERFACE | DELIVERABLE | DEL-02-05 -- Electrical/IT Concept Narrative | MEDIUM |

**Downstream (2 rows):**

| DependencyID | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|
| DEP-02-03-E010 | HANDOVER | DELIVERABLE | DEL-05-02 -- Structural Durability and Maintenance | HIGH |
| DEP-02-03-E011 | HANDOVER | DELIVERABLE | DEL-03-03 -- Structural Design Brief | HIGH |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

**Defaults and Paths Used:**
- DECOMPOSITION_PATH: `/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL)
- SOURCE_DOCS: AUTO -- 4 documents found: Datasheet.md, Guidance.md, Procedure.md, Specification.md
- ANCHOR_DOC: Datasheet.md (selected by heuristic: filename contains "datasheet")
- EXECUTION_DOC_ORDER: Procedure.md, Guidance.md, Specification.md, Datasheet.md (Procedure selected first by heuristic: filename contains "procedure")
- _REFERENCES.md: present and read; used for cross-reference validation

**Decomposition Status:** Available. Decomposition v2.3 FINAL confirmed. DEL-02-03 identity, package assignment (PKG-002), scope items (SOW-0009, SOW-0010), and objective (OBJ-003) all validated against decomposition.

**Warnings:** None.

**Assumptions:**
- All 4 source documents (Datasheet.md, Guidance.md, Procedure.md, Specification.md) treated as in-scope for extraction.
- ANCHOR parent node resolved to PKG-002 (the package to which DEL-02-03 belongs) based on Datasheet identification table and decomposition confirmation.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | v2.3 FINAL (available) | None | 4 | 11 | 15 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 15 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| NOT_APPLICABLE | 4 (anchors) |
| TBD | 11 (execution) |

---
