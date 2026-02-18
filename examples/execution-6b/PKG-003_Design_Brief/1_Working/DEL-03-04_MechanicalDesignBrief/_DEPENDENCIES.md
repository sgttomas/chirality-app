# Dependencies

**Deliverable ID:** DEL-03-04
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
**Total ACTIVE rows:** 17
**Total RETIRED rows:** 0

### Summary by Class

| DependencyClass | AnchorType | Count |
|---|---|---|
| ANCHOR | IMPLEMENTS_NODE | 1 |
| ANCHOR | TRACES_TO_REQUIREMENT | 2 |
| EXECUTION | NOT_APPLICABLE | 14 |

### Summary by Direction

| Direction | Count |
|---|---|
| UPSTREAM | 13 |
| DOWNSTREAM | 4 |

### Compact Register

| DependencyID | Class | Direction | Type | TargetType | Target | Confidence |
|---|---|---|---|---|---|---|
| DEP-03-04-001 | ANCHOR | UPSTREAM | OTHER | WBS_NODE | SOW-0011 | HIGH |
| DEP-03-04-002 | ANCHOR | UPSTREAM | OTHER | REQUIREMENT | OBJ-004 | HIGH |
| DEP-03-04-003 | ANCHOR | UPSTREAM | OTHER | DOCUMENT | RFP Section 7.1.2(4) | HIGH |
| DEP-03-04-004 | EXECUTION | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-04 (Mechanical Concept Narrative) | HIGH |
| DEP-03-04-005 | EXECUTION | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-01 (Architectural Concept Plan) | HIGH |
| DEP-03-04-006 | EXECUTION | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-03 (Structural Concept Narrative) | HIGH |
| DEP-03-04-007 | EXECUTION | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-02 (Civil Site Concept Plan) | HIGH |
| DEP-03-04-008 | EXECUTION | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-05 (Electrical/IT Concept Narrative) | HIGH |
| DEP-03-04-009 | EXECUTION | UPSTREAM | INTERFACE | DELIVERABLE | DEL-04-02 (Mechanical Energy and Solar Readiness) | HIGH |
| DEP-03-04-010 | EXECUTION | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-03 (Mechanical Maintainability) | HIGH |
| DEP-03-04-011 | EXECUTION | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-03 (Structural Design Brief) | HIGH |
| DEP-03-04-012 | EXECUTION | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-02 (Civil Design Brief) | HIGH |
| DEP-03-04-013 | EXECUTION | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-05 (Electrical/IT Design Brief) | HIGH |
| DEP-03-04-014 | EXECUTION | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-01 (Architectural Design Brief) | MEDIUM |
| DEP-03-04-015 | EXECUTION | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-06 (Accessibility and Adaptability Narrative) | MEDIUM |
| DEP-03-04-016 | EXECUTION | UPSTREAM | CONSTRAINT | DOCUMENT | Addendum 03 | HIGH |
| DEP-03-04-017 | EXECUTION | UPSTREAM | INTERFACE | DOCUMENT | 2021 Geotechnical Investigation Report | MEDIUM |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

**Defaults and Paths Used:**
- DECOMPOSITION_PATH: `/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL)
- SOURCE_DOCS: AUTO -- scanned deliverable folder; identified 4 source documents
- ANCHOR_DOC: `Datasheet.md` (selected by heuristic: filename contains "datasheet")
- EXECUTION_DOC_ORDER: `Procedure.md`, `Guidance.md`, `Specification.md`
- _REFERENCES.md: Read; used for cross-reference validation (DEL-02-04, DEL-04-02 confirmed)

**Decomposition Status:** Available and validated. All target IDs (SOW-0011, OBJ-004, DEL-02-01 through DEL-02-05, DEL-03-01 through DEL-03-06, DEL-04-02, DEL-05-03) confirmed present in decomposition.

**Anchor Validation:**
- Parent anchor: 1 ACTIVE IMPLEMENTS_NODE row (DEP-03-04-001 -> SOW-0011) -- PASS
- Trace anchors: 2 ACTIVE TRACES_TO_REQUIREMENT rows (OBJ-004, RFP Section 7.1.2(4)) -- PASS

**Warnings:** None.

**Assumptions Logged:**
- DEL-03-03, DEL-03-02, DEL-03-05 downstream interfaces are bidirectional; the upstream counterpart is covered by DEP-03-04-006 (DEL-02-03 concept), DEP-03-04-007 (DEL-02-02 concept), DEP-03-04-008 (DEL-02-05 concept) at the concept stage. The design brief stage interfaces (DEP-03-04-011/012/013) capture the information flow from mechanical to sibling briefs. FACT basis.
- Addendum 03 constraint (DEP-03-04-016) is sourced from Specification.md R-A header and Datasheet.md conditions; treated as a single CONSTRAINT edge to avoid duplication.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | v2.3 FINAL (available) | None | 17 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 17 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 17 |
