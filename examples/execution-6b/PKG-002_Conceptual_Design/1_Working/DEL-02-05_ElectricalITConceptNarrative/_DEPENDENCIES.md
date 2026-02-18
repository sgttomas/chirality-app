# Dependencies

**Deliverable ID:** DEL-02-05
**Tracking Mode:** DECLARED (critical dependencies only)

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total ACTIVE rows:** 14
**Total RETIRED rows:** 0

| DependencyID | Class | AnchorType | Direction | Type | TargetType | Target | Status |
|---|---|---|---|---|---|---|---|
| DEP-0205-A01 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | PACKAGE | PKG-002 -- Conceptual Design | ACTIVE |
| DEP-0205-A02 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | WBS_NODE | SOW-0009 -- Concept design package | ACTIVE |
| DEP-0205-A03 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | WBS_NODE | SOW-0010 -- Embed program clarifications | ACTIVE |
| DEP-0205-A04 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-003 -- Maximize Conceptual Design score | ACTIVE |
| DEP-0205-E01 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-01 -- Architectural Concept Package | ACTIVE |
| DEP-0205-E02 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-04 -- Mechanical Concept Narrative | ACTIVE |
| DEP-0205-E03 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-02 -- Civil/Site Concept Plan | ACTIVE |
| DEP-0205-E04 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-03 -- Structural Concept Narrative | ACTIVE |
| DEP-0205-E05 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-03-05 -- Electrical/IT Design Brief | ACTIVE |
| DEP-0205-E06 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-04-03 -- Electrical Energy Efficiency | ACTIVE |
| DEP-0205-E07 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-05-04 -- Electrical Maintainability | ACTIVE |
| DEP-0205-E08 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | DOCUMENT | Addendum 03 (Jul 31 2024) | ACTIVE |
| DEP-0205-E09 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | DOCUMENT | RFP Section 7.1.1 -- Proposed Conceptual Design | ACTIVE |
| DEP-0205-E10 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DOCUMENT | RFP Appendix B -- Functional Program | ACTIVE |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

**Defaults used:**
- SOURCE_DOCS: AUTO -- scanned deliverable folder; identified Datasheet.md (ANCHOR_DOC), Guidance.md, Procedure.md, Specification.md (EXECUTION_DOCS)
- ANCHOR_DOC: Datasheet.md (selected by heuristic: contains "datasheet" in filename; confirmed as primary definition/traceability source)
- EXECUTION_DOC_ORDER: Procedure.md, Specification.md, Guidance.md (ordered by workflow clarity; Procedure contains explicit Prerequisites table)
- DECOMPOSITION_PATH: /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL, 2026-02-17)

**Decomposition status:** Available and validated. All anchor IDs (PKG-002, SOW-0009, SOW-0010, OBJ-003) confirmed present in decomposition. All target deliverable IDs (DEL-02-01, DEL-02-02, DEL-02-03, DEL-02-04, DEL-03-05, DEL-04-03, DEL-05-04) confirmed present in decomposition.

**_REFERENCES.md status:** Read; used to confirm cross-reference targets (DEL-02-01, DEL-02-04, DEL-04-03) and source document pointers.

**Warnings:** None.

**Assumptions:**
- DEP-0205-E06 direction set to DOWNSTREAM based on judgment that DEL-02-05 concept establishes design decisions consumed by DEL-04-03, even though Specification labels this as "lateral coordination." Marked MEDIUM confidence.

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-02-17 | UPDATE | CONSERVATIVE | Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) | None | 4 | 10 | 14 |

---

## Lifecycle Summary

| Category | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR (IMPLEMENTS_NODE) | 1 | 0 |
| ANCHOR (TRACES_TO_REQUIREMENT) | 3 | 0 |
| EXECUTION (PREREQUISITE) | 2 | 0 |
| EXECUTION (INTERFACE) | 3 | 0 |
| EXECUTION (HANDOVER) | 3 | 0 |
| EXECUTION (CONSTRAINT) | 2 | 0 |
| **Total** | **14** | **0** |

**Closure lifecycle breakdown (all ACTIVE rows):**

| SatisfactionStatus | Count |
|---|---|
| TBD | 14 |

---

*End of extracted dependency register.*
