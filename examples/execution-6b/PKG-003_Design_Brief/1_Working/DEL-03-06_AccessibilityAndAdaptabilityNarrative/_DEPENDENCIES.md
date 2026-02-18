# Dependencies

**Deliverable ID:** DEL-03-06
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Register File:** `Dependencies.csv`
**Schema Version:** v3.1
**Total ACTIVE Rows:** 19
**Total RETIRED Rows:** 0

### Summary by Class

| DependencyClass | AnchorType | Count |
|-----------------|------------|-------|
| ANCHOR | IMPLEMENTS_NODE | 1 |
| ANCHOR | TRACES_TO_REQUIREMENT | 4 |
| EXECUTION | NOT_APPLICABLE | 14 |

### Summary by Direction

| Direction | Count |
|-----------|-------|
| UPSTREAM | 16 |
| DOWNSTREAM | 3 |

### Summary by DependencyType

| DependencyType | Count |
|----------------|-------|
| OTHER (anchors) | 5 |
| PREREQUISITE | 8 |
| INTERFACE | 4 |
| CONSTRAINT | 1 |
| HANDOVER | 1 |

### Compact Register

| DependencyID | Class | Direction | Type | TargetType | Target | Confidence |
|-------------|-------|-----------|------|------------|--------|------------|
| DEP-03-06-001 | ANCHOR | UPSTREAM | IMPLEMENTS_NODE | WBS_NODE | PKG-003 -- Design Brief | HIGH |
| DEP-03-06-002 | ANCHOR | UPSTREAM | TRACES_TO_REQ | REQUIREMENT | SOW-0014 (Adaptability narrative) | HIGH |
| DEP-03-06-003 | ANCHOR | UPSTREAM | TRACES_TO_REQ | REQUIREMENT | SOW-0015 (Accessibility narrative) | HIGH |
| DEP-03-06-004 | ANCHOR | UPSTREAM | TRACES_TO_REQ | REQUIREMENT | OBJ-004 (Design Brief: 5 pts) | HIGH |
| DEP-03-06-005 | ANCHOR | UPSTREAM | TRACES_TO_REQ | REQUIREMENT | OBJ-005 (Durability/flexibility: 15 pts) | HIGH |
| DEP-03-06-006 | EXECUTION | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-03 Structural Design Brief | HIGH |
| DEP-03-06-007 | EXECUTION | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-01 Architectural Concept Package | HIGH |
| DEP-03-06-008 | EXECUTION | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-02 Civil Site Concept Plan | HIGH |
| DEP-03-06-009 | EXECUTION | UPSTREAM | PREREQUISITE | DOCUMENT | RFP (SS7.1.3 and SS7.1.5) | HIGH |
| DEP-03-06-010 | EXECUTION | UPSTREAM | PREREQUISITE | DOCUMENT | Addendum 03 | HIGH |
| DEP-03-06-011 | EXECUTION | UPSTREAM | PREREQUISITE | DOCUMENT | Geotechnical Investigation Report | HIGH |
| DEP-03-06-012 | EXECUTION | UPSTREAM | PREREQUISITE | DOCUMENT | Site Grading Plan | MEDIUM |
| DEP-03-06-013 | EXECUTION | UPSTREAM | PREREQUISITE | DOCUMENT | Wetland Assessment | MEDIUM |
| DEP-03-06-014 | EXECUTION | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-04 Mechanical Design Brief | HIGH |
| DEP-03-06-015 | EXECUTION | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-05 Electrical/IT Design Brief | HIGH |
| DEP-03-06-016 | EXECUTION | UPSTREAM | CONSTRAINT | EXTERNAL | Alberta Building Code (edition TBD) | HIGH |
| DEP-03-06-017 | EXECUTION | DOWNSTREAM | HANDOVER | PACKAGE | PKG-003 Design Brief Assembly | HIGH |
| DEP-03-06-018 | EXECUTION | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-03 Structural Design Brief | HIGH |
| DEP-03-06-019 | EXECUTION | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-01 Architectural Design Brief | MEDIUM |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE (initial run -- no prior CSV existed)
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

### Defaults and Paths Used

| Setting | Value |
|---------|-------|
| RUN_ROOT | `/test/execution-6b/` |
| DECOMPOSITION_PATH | `/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL) |
| SOURCE_DOCS | AUTO -- scanned deliverable folder; identified: Datasheet.md, Specification.md, Procedure.md, Guidance.md |
| ANCHOR_DOC | Datasheet.md (selected by heuristic: contains "datasheet" in filename; highest anchor signal density) |
| EXECUTION_DOC_ORDER | Procedure.md, Specification.md, Guidance.md (Procedure has clearest workflow/prerequisite signal) |
| DOC_ROLE_MAP | DEFAULT heuristic applied |

### Assumptions

- ASSUM: DEL-03-03 is recorded as both UPSTREAM PREREQUISITE (information input for narrative content) and DOWNSTREAM INTERFACE (bidirectional consistency requirement). These represent distinct dependency edges -- input vs. consistency -- and are not duplicates.
- ASSUM: Document-type dependencies (RFP, Addendum 03, Geotech report, Site Grading, Wetland Assessment) are recorded as PREREQUISITE because the Procedure explicitly lists them as "Required Inputs" with status tracking.
- ASSUM: Alberta Building Code is typed as EXTERNAL/CONSTRAINT because it is an external regulatory standard that constrains the narrative content, not a project deliverable.

### Warnings

No warnings. All quality checks passed.

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|-----|------|------|------------|---------------|----------|--------------|
| 1 | 2026-02-17 | UPDATE (initial) | CONSERVATIVE | v2.3 FINAL (located) | None | 19 |

---

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 19 |
| RETIRED | 0 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|--------------------|-------|
| TBD | 7 |
| PENDING | 10 |
| SATISFIED | 2 |

**Notes:**
- SATISFIED: RFP and Addendum 03 documents are available and accessible.
- PENDING: Deliverable inputs (DEL-03-03, DEL-02-01, DEL-02-02, DEL-03-04, DEL-03-05) are TBD/not yet generated; document inputs (Geotech, Site Grading, Wetland) are available but data not yet extracted; ABC edition is TBD.
- TBD: Anchor rows and downstream handover/interface rows where satisfaction tracking is not yet applicable at this stage.
