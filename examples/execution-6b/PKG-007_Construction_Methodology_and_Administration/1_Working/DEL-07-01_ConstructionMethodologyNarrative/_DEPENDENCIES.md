# Dependencies

**Deliverable ID:** DEL-07-01
**Deliverable Name:** Construction Methodology Narrative
**Package:** PKG-007 -- Construction Methodology & Administration
**Tracking Mode:** DECLARED + EXTRACTED

---

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here. Extracted dependencies below supplement this section.

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total ACTIVE rows:** 15
**Total RETIRED rows:** 0

### Summary by Class

| DependencyClass | AnchorType | Count |
|---|---|---|
| ANCHOR | IMPLEMENTS_NODE | 1 |
| ANCHOR | TRACES_TO_REQUIREMENT | 2 |
| EXECUTION | NOT_APPLICABLE | 12 |

### Summary by Direction

| Direction | Count |
|---|---|
| UPSTREAM | 12 |
| DOWNSTREAM | 3 |

### Compact Register

| DependencyID | Class | Direction | Type | TargetType | Target | Confidence |
|---|---|---|---|---|---|---|
| DEP-07-01-001 | ANCHOR | UPSTREAM | OTHER | WBS_NODE | PKG-007 | HIGH |
| DEP-07-01-002 | ANCHOR | UPSTREAM | OTHER | REQUIREMENT | SOW-0019 | HIGH |
| DEP-07-01-003 | ANCHOR | UPSTREAM | OTHER | REQUIREMENT | OBJ-002 | HIGH |
| DEP-07-01-004 | EXECUTION | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-02 Civil Site Concept Plan | HIGH |
| DEP-07-01-005 | EXECUTION | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-10-02 Site Conditions and Due Diligence Summary | HIGH |
| DEP-07-01-006 | EXECUTION | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-09-01 Detailed Project Schedule | HIGH |
| DEP-07-01-007 | EXECUTION | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-07-03 Subconsultant Approach Narrative | HIGH |
| DEP-07-01-008 | EXECUTION | UPSTREAM | PREREQUISITE | DOCUMENT | RFP Section 7.2 | HIGH |
| DEP-07-01-009 | EXECUTION | UPSTREAM | PREREQUISITE | DOCUMENT | Appendix J -- Supplementary Conditions | HIGH |
| DEP-07-01-010 | EXECUTION | UPSTREAM | PREREQUISITE | DOCUMENT | RFP Addenda 01-03 | HIGH |
| DEP-07-01-011 | EXECUTION | UPSTREAM | PREREQUISITE | DOCUMENT | RFP Section 7.3 | MEDIUM |
| DEP-07-01-012 | EXECUTION | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-07-02 Construction Administration Narrative | HIGH |
| DEP-07-01-013 | EXECUTION | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-07-04 Meetings and Reporting Narrative | HIGH |
| DEP-07-01-014 | EXECUTION | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-07-05 Quality Management Narrative | HIGH |
| DEP-07-01-015 | EXECUTION | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-05 Schedule B Cost Breakdown | MEDIUM |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

**Defaults and Paths Used:**
- DECOMPOSITION_PATH: `/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (located; v2.3 FINAL)
- SOURCE_DOCS: AUTO -- scanned deliverable folder; identified 4 source documents:
  - `Datasheet.md` (ANCHOR_DOC)
  - `Guidance.md` (EXECUTION_DOC)
  - `Procedure.md` (EXECUTION_DOC)
  - `Specification.md` (EXECUTION_DOC)
- ANCHOR_DOC: `Datasheet.md` (heuristic match: contains `datasheet` in filename; confirms identification fields and scope/objective alignment)
- EXECUTION_DOC_ORDER: `Procedure.md`, `Guidance.md`, `Specification.md` (Procedure contains Prerequisites table with explicit required inputs; Guidance contains cross-references; Specification contains requirements traceability)
- _REFERENCES.md: read; used for cross-reference context but no additional dependencies sourced solely from it

**Assumptions:**
- None. All extracted rows are grounded in explicit statements from source documents.

**Warnings:**
- (none)

**Extraction Notes:**
- Pass 1 (ANCHOR): Identified 1 parent anchor (PKG-007) and 2 trace anchors (SOW-0019, OBJ-002) from Datasheet.md Identification table. All confirmed against Decomposition Section 9 and Scope Ledger.
- Pass 2 (EXECUTION): Identified 12 execution edges from Procedure Prerequisites table, Procedure Steps, Guidance Cross-References, Guidance Considerations, and Specification scope boundary statements.
- Several additional cross-references were noted in Guidance P-004 (DEL-02-02 mentioned at line 374) but these were already captured via the Procedure Prerequisites table and were not duplicated.
- Guidance P-004 also mentions DEL-10-02 at the cross-reference level; this is captured as DEP-07-01-005 via the Procedure Prerequisites table.
- The relationship to the Alberta OH&S Act was not extracted as a dependency row because it is a regulatory standard (not an information flow / artifact transfer between project entities). It is captured in Specification Standards table.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION |
|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) | (none) | 3 | 12 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 15 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 15 |

---
