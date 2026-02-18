# Dependencies

**Deliverable ID:** DEL-01-09
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 11
**Total RETIRED rows:** 0

| Class | Count |
|-------|------:|
| ANCHOR | 4 |
| EXECUTION | 7 |

| DependencyID | Class | AnchorType | Dir | Type | TargetType | Target | Status |
|---|---|---|---|---|---|---|---|
| DEP-01-09-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | PKG-001 | ACTIVE |
| DEP-01-09-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | SOW-0007 | ACTIVE |
| DEP-01-09-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-006 | ACTIVE |
| DEP-01-09-004 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | C-06 | ACTIVE |
| DEP-01-09-005 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-07 | ACTIVE |
| DEP-01-09-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-08 | ACTIVE |
| DEP-01-09-007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | RFP Appendix I Template | ACTIVE |
| DEP-01-09-008 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | DOCUMENT | Addendum 03 | ACTIVE |
| DEP-01-09-009 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02 | ACTIVE |
| DEP-01-09-010 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-07-03 | ACTIVE |
| DEP-01-09-011 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | OSR (RFP Appendix A) | ACTIVE |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

**Defaults and Paths Used:**
- RUN_ROOT: /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/
- DECOMPOSITION_PATH: /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL, 2026-02-17)
- SOURCE_DOCS: AUTO -- scanned deliverable folder; identified Datasheet.md (ANCHOR_DOC), Guidance.md, Procedure.md, Specification.md (EXECUTION_DOCS)
- ANCHOR_DOC: Datasheet.md (selected by heuristic: contains "datasheet" in filename)
- EXECUTION_DOC_ORDER: Procedure.md, Specification.md, Guidance.md (ordered by workflow clarity)
- _REFERENCES.md: present and used for target resolution
- Dependencies.csv: created new (no prior file)

**Assumptions:**
- ASSUMPTION: DEP-01-09-010 direction set to DOWNSTREAM because DEL-01-09 is the authoritative team roster and DEL-07-03 must align with it, not the reverse. The Specification R-12 states "Ensure consistency between scope assignments in Appendix I and the subconsultant approach described in DEL-07-03" which implies Appendix I is the authoritative source.

**Warnings:**
- None.

**Quality Check Results:**
- Schema check: PASS -- all required columns present, CSV parseable
- DependencyID uniqueness: PASS -- 11 unique IDs
- Evidence check: PASS -- all ACTIVE rows have EvidenceFile and SourceRef
- Parent anchor check: PASS -- exactly 1 IMPLEMENTS_NODE row (DEP-01-09-001)
- _DEPENDENCIES.md consistency: PASS -- counts match CSV (11 ACTIVE, 0 RETIRED)
- Duplicate check: PASS -- no obvious duplicate rows

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|-----|------|------|------------|---------------|----------|-------------:|
| 1 | 2026-02-17 | UPDATE | CONSERVATIVE | Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) | None | 11 |

---

## Lifecycle Summary

| Status | Count |
|--------|------:|
| ACTIVE | 11 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|--------------------|------:|
| TBD | 11 |
