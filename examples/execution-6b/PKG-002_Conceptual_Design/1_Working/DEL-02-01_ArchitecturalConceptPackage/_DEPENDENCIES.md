# Dependencies

**Deliverable ID:** DEL-02-01
**Deliverable Name:** Architectural Concept Package
**Package:** PKG-002 -- Conceptual Design
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated in the declared sections above. Only interface-critical dependencies are recorded there. The extracted register below is machine-generated from source document analysis.

---

## Extracted Dependency Register

**Register File:** `Dependencies.csv`
**Schema Version:** v3.1
**Total Rows:** 15
**ACTIVE:** 15 | **RETIRED:** 0

### ANCHOR Dependencies (4 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetName | Confidence |
|---|---|---|---|---|
| DEP-0201-A01 | IMPLEMENTS_NODE | WBS_NODE | PKG-002 -- Conceptual Design | HIGH |
| DEP-0201-A02 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0009 -- Concept Design Package | HIGH |
| DEP-0201-A03 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0010 -- Embed Program Clarifications & Special Requirements | HIGH |
| DEP-0201-A04 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-003 -- Maximize Proposed Conceptual Design score (20 pts) | HIGH |

### EXECUTION Dependencies -- UPSTREAM (7 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetName | Confidence |
|---|---|---|---|---|
| DEP-0201-E01 | INTERFACE | DELIVERABLE | DEL-02-02 -- Civil Site Concept Plan | HIGH |
| DEP-0201-E02 | INTERFACE | DELIVERABLE | DEL-02-03 -- Structural Concept Narrative | HIGH |
| DEP-0201-E03 | INTERFACE | DELIVERABLE | DEL-02-04 -- Mechanical Concept Narrative | HIGH |
| DEP-0201-E04 | INTERFACE | DELIVERABLE | DEL-02-05 -- Electrical/IT Concept Narrative | HIGH |
| DEP-0201-E05 | PREREQUISITE | DOCUMENT | RFP Appendix A -- Owner Statement of Requirements (OSR) | HIGH |
| DEP-0201-E06 | PREREQUISITE | DOCUMENT | RFP Appendix B -- Functional Program | HIGH |
| DEP-0201-E07 | CONSTRAINT | DOCUMENT | RFP Addendum 03 (Jul 31 2024) | HIGH |

### EXECUTION Dependencies -- DOWNSTREAM (4 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetName | Confidence |
|---|---|---|---|---|
| DEP-0201-E08 | HANDOVER | DELIVERABLE | DEL-03-01 -- Architectural Design Brief | HIGH |
| DEP-0201-E09 | HANDOVER | DELIVERABLE | DEL-03-06 -- Accessibility and Adaptability Narrative | HIGH |
| DEP-0201-E10 | HANDOVER | DELIVERABLE | DEL-06-02 -- Detailed Design and Construction Docs Plan | HIGH |
| DEP-0201-E11 | HANDOVER | DELIVERABLE | DEL-01-02 -- Formal Submission Package | HIGH |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE
**Decomposition Path:** `/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL)
**Decomposition Status:** Located and loaded successfully.

**Source Documents Scanned (AUTO):**
- `Datasheet.md` -- ANCHOR_DOC (primary anchor/definition signal)
- `Procedure.md` -- EXECUTION_DOC (primary workflow/execution signal)
- `Guidance.md` -- EXECUTION_DOC (supplementary considerations and trade-offs)
- `Specification.md` -- EXECUTION_DOC (requirements and verification)

**Defaults Applied:**
- SOURCE_DOCS: AUTO -- all four source documents in deliverable folder scanned
- DOC_ROLE_MAP: DEFAULT -- Datasheet.md identified as ANCHOR_DOC; Procedure.md, Guidance.md, Specification.md as EXECUTION_DOCs
- ANCHOR_DOC: AUTO -- selected Datasheet.md (contains deliverable identification, scope items, objective alignment)
- EXECUTION_DOC_ORDER: AUTO -- Procedure.md (highest workflow clarity), Specification.md, Guidance.md

**Read-Only Inputs Used:**
- `_REFERENCES.md` -- used for cross-reference validation of DEL-02-02 through DEL-02-05 pointers
- `_CONTEXT.md` -- used for deliverable identity confirmation

**Assumptions:**
- DEL-02-02 through DEL-02-05 interfaces are classified as INTERFACE (not PREREQUISITE) because the Procedure describes them as "concurrent coordination dependencies" with iterative input exchange, not as strict blocking gates. The Procedure Upstream Dependencies section explicitly states "No formal upstream deliverables declared as blocking prerequisites."
- Appendix A and Appendix B are classified as PREREQUISITE because Procedure V-00 explicitly states "Do not proceed to Step 2 until all three prerequisite items are validated" -- this is a hard gate.
- Addendum 03 is classified as CONSTRAINT because it is described as the governing document whose values override all other sources.
- Downstream handovers to DEL-03-01, DEL-03-06, DEL-06-02, and DEL-01-02 are explicitly stated in the Procedure Handoff table with specific artifact transfers described.

**Warnings:** None.

---

## Run History

| Run Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | v2.3 FINAL (located) | None | 15 (4 ANCHOR + 11 EXECUTION) |

---

## Lifecycle Summary

| Category | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR (IMPLEMENTS_NODE) | 1 | 0 |
| ANCHOR (TRACES_TO_REQUIREMENT) | 3 | 0 |
| EXECUTION (UPSTREAM) | 7 | 0 |
| EXECUTION (DOWNSTREAM) | 4 | 0 |
| **Total** | **15** | **0** |

**Closure State Breakdown (ACTIVE rows):**
- SatisfactionStatus = TBD: 13
- SatisfactionStatus = PENDING: 2 (DEP-0201-E05 Appendix A extraction, DEP-0201-E06 Appendix B extraction -- both marked PENDING because prerequisite extraction has not been completed per source documents)

---

**End of Dependencies**
