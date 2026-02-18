# Dependencies

**Deliverable ID:** DEL-06-01
**Deliverable Name:** Design Methodology Narrative
**Package:** PKG-006 -- Delivery Plan (Design Methodology + Documents Plan)
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 17
**Total RETIRED rows:** 0

| Class | Count |
|---|---|
| ANCHOR | 3 |
| EXECUTION | 14 |

| Direction | Count |
|---|---|
| UPSTREAM | 15 |
| DOWNSTREAM | 2 |

### ANCHOR Rows (ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-0601-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0008 | HIGH |
| DEP-0601-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-002 | HIGH |
| DEP-0601-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | RFP-7.1 | HIGH |

### EXECUTION Rows (ACTIVE)

| DependencyID | Direction | Type | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-0601-004 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-06-02 (Design Documents Plan) | HIGH |
| DEP-0601-005 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-09-01 (Detailed Project Schedule) | HIGH |
| DEP-0601-006 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-07 (Firm Experience Profile) | HIGH |
| DEP-0601-007 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-08 (Key Team Members / Resumes) | HIGH |
| DEP-0601-008 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-01 (Architectural Concept Package) | MEDIUM |
| DEP-0601-009 | UPSTREAM | CONSTRAINT | DOCUMENT | RFP Section 7.1 | HIGH |
| DEP-0601-010 | UPSTREAM | CONSTRAINT | DOCUMENT | Addendum 03 | HIGH |
| DEP-0601-011 | UPSTREAM | CONSTRAINT | DOCUMENT | Addendum 01 | HIGH |
| DEP-0601-012 | UPSTREAM | PREREQUISITE | DOCUMENT | OSR (Appendix A) | MEDIUM |
| DEP-0601-013 | UPSTREAM | PREREQUISITE | DOCUMENT | Functional Program (Appendix B) | MEDIUM |
| DEP-0601-014 | UPSTREAM | PREREQUISITE | DOCUMENT | Geotechnical Report 2021 (Appendix D) | HIGH |
| DEP-0601-015 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-07-01 (Construction Methodology) | HIGH |
| DEP-0601-016 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-06 (Accessibility & Adaptability) | HIGH |
| DEP-0601-017 | UPSTREAM | CONSTRAINT | DOCUMENT | CCDC 14-2013 (Appendix J) | MEDIUM |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

**Defaults and Paths Used:**
- SOURCE_DOCS: AUTO -- scanned deliverable folder; identified 4 source documents: Datasheet.md (ANCHOR_DOC), Procedure.md, Guidance.md, Specification.md (EXECUTION_DOCS)
- ANCHOR_DOC: Datasheet.md (selected by heuristic: filename contains "datasheet")
- EXECUTION_DOC_ORDER: Procedure.md, Specification.md, Guidance.md (Procedure selected first by heuristic: filename contains "procedure")
- DECOMPOSITION_PATH: /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL)
- _REFERENCES.md: Read; used for cross-reference validation (DEL-06-02, DEL-09-01 confirmed)

**Decomposition Validation:**
- Decomposition located and loaded successfully (v2.3 FINAL, 2026-02-17)
- DEL-06-01 confirmed in Decomposition Section 9 under PKG-006
- SOW-0008 confirmed in Decomposition Section 10 Scope Ledger mapped to DEL-06-01
- OBJ-002 confirmed in Decomposition Section 6 Objectives
- All target deliverable IDs (DEL-06-02, DEL-09-01, DEL-01-07, DEL-01-08, DEL-02-01, DEL-07-01, DEL-03-06) validated against Decomposition Section 9

**Extraction Notes:**
- Pass 1 (ANCHOR): Extracted 1 IMPLEMENTS_NODE anchor (SOW-0008) and 2 TRACES_TO_REQUIREMENT anchors (OBJ-002, RFP-7.1). All explicit in Datasheet Identification table.
- Pass 2 (EXECUTION): Extracted 14 execution edges. Primary source: Procedure.md (Related Deliverables table and Required Inputs table provided 11 edges). Specification.md (R-010, R-013) provided 2 additional downstream interface edges. Datasheet.md contributed 1 CCDC 14-2013 constraint edge.
- DEL-02-01 through DEL-02-05 (Conceptual Design): Procedure states "DEL-02-01 through DEL-02-05" as a group. Recorded as single row targeting DEL-02-01 as the lead deliverable (Architectural Concept Package; Lead Architect coordinates). Confidence set to MEDIUM because the interface is "coordinate by proposal assembly" rather than a hard prerequisite.
- Addendum 02 was reviewed but explicitly states "No content impact on design methodology" (Procedure Step 2); no dependency row created.
- Reference Reports (Appendix D, E, F): Procedure lists all three but the Geotechnical Report (Appendix D) is the most critical per Guidance C-004 and DEC-013. Wetland and Environmental reports are informational context, not explicit design methodology inputs. Only Geotechnical Report extracted as a dependency (DEP-0601-014).

**Warnings:**
- None. Parent anchor present (1 IMPLEMENTS_NODE). No ambiguous anchors.

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION |
|---|---|---|---|---|---|---|---|
| 1 | 2026-02-17 | UPDATE | CONSERVATIVE | Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) | None | 3 | 14 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 17 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 17 |

---
