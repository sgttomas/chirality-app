# Dependencies

**Deliverable ID:** DEL-05-02
**Tracking Mode:** DECLARED (critical dependencies only)

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Register Schema Version:** v3.1
**Total ACTIVE rows:** 11
**Total RETIRED rows:** 0

### Summary by Class

| DependencyClass | AnchorType | Count |
|-----------------|------------|-------|
| ANCHOR | IMPLEMENTS_NODE | 1 |
| ANCHOR | TRACES_TO_REQUIREMENT | 2 |
| EXECUTION | NOT_APPLICABLE | 8 |

### Summary by Direction

| Direction | Count |
|-----------|-------|
| UPSTREAM | 9 |
| DOWNSTREAM | 2 |

### Compact Register

| DependencyID | Class | Direction | Type | TargetType | Target | Confidence | Status |
|--------------|-------|-----------|------|------------|--------|------------|--------|
| DEP-05-02-001 | ANCHOR | UPSTREAM | OTHER | WBS_NODE | SOW-0013 | HIGH | ACTIVE |
| DEP-05-02-002 | ANCHOR | UPSTREAM | OTHER | REQUIREMENT | OBJ-005 | HIGH | ACTIVE |
| DEP-05-02-003 | ANCHOR | UPSTREAM | OTHER | REQUIREMENT | DEC-009 | HIGH | ACTIVE |
| DEP-05-02-004 | EXECUTION | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-03 (Structural Concept) | HIGH | ACTIVE |
| DEP-05-02-005 | EXECUTION | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-01 (Architectural Durability) | HIGH | ACTIVE |
| DEP-05-02-006 | EXECUTION | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-03 (Mechanical Maintainability) | HIGH | ACTIVE |
| DEP-05-02-007 | EXECUTION | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-05-03 (Mechanical Maintainability) | HIGH | ACTIVE |
| DEP-05-02-008 | EXECUTION | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-05-04 (Electrical Maintainability) | MEDIUM | ACTIVE |
| DEP-05-02-009 | EXECUTION | UPSTREAM | PREREQUISITE | DOCUMENT | Geotechnical Report (USG1123) | HIGH | ACTIVE |
| DEP-05-02-010 | EXECUTION | UPSTREAM | PREREQUISITE | DOCUMENT | RFP 2024_004 Section 7.1.4 | HIGH | ACTIVE |
| DEP-05-02-011 | EXECUTION | UPSTREAM | CONSTRAINT | DOCUMENT | Addendum 03 (Jul 31 2024) | HIGH | ACTIVE |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

### Defaults and Paths Used

- **RUN_ROOT:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/
- **DECOMPOSITION_PATH:** /Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md (located automatically; version v2.3 FINAL)
- **SOURCE_DOCS:** AUTO -- scanned deliverable folder; identified 4 source documents
- **DOC_ROLE_MAP:** DEFAULT heuristic applied
- **ANCHOR_DOC:** Datasheet.md (matched "datasheet" pattern; contains Identification table with SOW/OBJ references)
- **EXECUTION_DOC_ORDER:** Procedure.md, Specification.md, Guidance.md, Datasheet.md (Procedure matched "procedure" pattern for highest workflow clarity; Specification matched "spec" pattern; Guidance matched "guidance" pattern)

### Assumptions

- ASSUMPTION: DEL-05-03 interface is bidirectional (DEP-05-02-006 upstream for drainage inputs; DEP-05-02-007 downstream for sump shell outputs). Both directions supported by explicit text in Specification R-STR-13, Guidance C-005, and Procedure Step B2.
- ASSUMPTION: DEL-05-04 downstream interface (DEP-05-02-008) rated MEDIUM confidence because the information transfer (sealed penetration details) is mentioned but less explicitly structured than the DEL-05-03 sump interface.

### Warnings

_No warnings._

### Quality Check Results

- [PASS] Required columns present in Dependencies.csv.
- [PASS] DependencyID uniqueness: 11 unique IDs, 11 rows.
- [PASS] All ACTIVE rows have EvidenceFile and SourceRef populated.
- [PASS] Status and SatisfactionStatus values are canonical.
- [PASS] _DEPENDENCIES.md counts match Dependencies.csv (11 ACTIVE, 0 RETIRED).
- [PASS] No obvious duplicate extracted rows.
- [PASS] Parent anchor check: exactly 1 ACTIVE IMPLEMENTS_NODE row (DEP-05-02-001 -> SOW-0013).
- [PASS] FromDeliverableID is DEL-05-02 for all rows.
- [PASS] TargetDeliverableID populated for DELIVERABLE targets; empty for non-deliverable targets.
- [PASS] TargetRefID populated for non-deliverable targets; empty for DELIVERABLE targets.
- [PASS] Enum normalization: all Direction, DependencyClass, AnchorType, DependencyType values are canonical write-form.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|-----------|------|------------|---------------|----------|--------------|
| 2026-02-17 | UPDATE | CONSERVATIVE | Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) | None | 11 |

---

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 11 |
| RETIRED | 0 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|--------------------|-------|
| TBD | 11 |
