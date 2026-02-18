# Dependencies

**Deliverable ID:** DEL-03-01
**Tracking Mode:** DECLARED (critical dependencies only)

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
**Total ACTIVE Rows:** 17
**Total RETIRED Rows:** 0

### Summary by Class

| DependencyClass | AnchorType | Count |
|---|---|---|
| ANCHOR | IMPLEMENTS_NODE | 1 |
| ANCHOR | TRACES_TO_REQUIREMENT | 2 |
| EXECUTION | NOT_APPLICABLE | 14 |

### Summary by Direction

| Direction | Count |
|---|---|
| UPSTREAM | 10 |
| DOWNSTREAM | 7 |

### Compact Register

| DependencyID | Class | Direction | Type | TargetType | Target | Confidence |
|---|---|---|---|---|---|---|
| DEP-03-01-001 | ANCHOR | UPSTREAM | OTHER | WBS_NODE | PKG-003 / DEL-03-01 (Decomposition) | HIGH |
| DEP-03-01-002 | ANCHOR | UPSTREAM | OTHER | REQUIREMENT | SOW-0011 | HIGH |
| DEP-03-01-003 | ANCHOR | UPSTREAM | OTHER | REQUIREMENT | OBJ-004 | HIGH |
| DEP-03-01-004 | EXECUTION | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-01 Architectural Concept Package | HIGH |
| DEP-03-01-005 | EXECUTION | UPSTREAM | CONSTRAINT | DOCUMENT | RFP Section 7.1.2(1) | HIGH |
| DEP-03-01-006 | EXECUTION | UPSTREAM | CONSTRAINT | DOCUMENT | OSR (Appendix A) | HIGH |
| DEP-03-01-007 | EXECUTION | UPSTREAM | CONSTRAINT | DOCUMENT | Addendum 03 | HIGH |
| DEP-03-01-008 | EXECUTION | UPSTREAM | CONSTRAINT | DOCUMENT | Functional Program (Appendix B) | HIGH |
| DEP-03-01-009 | EXECUTION | UPSTREAM | INTERFACE | DOCUMENT | Geotechnical Report (2021, Appendix D) | MEDIUM |
| DEP-03-01-010 | EXECUTION | UPSTREAM | INTERFACE | DELIVERABLE | DEL-04-01 Building Envelope and Energy Strategy | HIGH |
| DEP-03-01-011 | EXECUTION | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-02 Civil Design Brief | HIGH |
| DEP-03-01-012 | EXECUTION | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-03 Structural Design Brief | HIGH |
| DEP-03-01-013 | EXECUTION | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-04 Mechanical Design Brief | HIGH |
| DEP-03-01-014 | EXECUTION | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-05 Electrical IT Design Brief | HIGH |
| DEP-03-01-015 | EXECUTION | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-06 Accessibility and Adaptability Narrative | HIGH |
| DEP-03-01-016 | EXECUTION | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-05-01 Architectural Durability and Maintenance | HIGH |
| DEP-03-01-017 | EXECUTION | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02 Formal Submission Package | HIGH |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

### Defaults and Paths Used

- **RUN_ROOT:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/`
- **DECOMPOSITION_PATH:** `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (located; v2.3 FINAL; read successfully)
- **SOURCE_DOCS:** AUTO -- scanned: `Datasheet.md` (ANCHOR_DOC), `Specification.md`, `Guidance.md`, `Procedure.md` (EXECUTION_DOCS)
- **ANCHOR_DOC:** `Datasheet.md` (selected by heuristic: contains "datasheet" in filename; has Identification table with decomposition reference, scope coverage, and objective alignment)
- **EXECUTION_DOC_ORDER:** `Specification.md`, `Guidance.md`, `Procedure.md` (ordered by specification > guidance > procedure workflow clarity)
- **_REFERENCES.md:** Read for target resolution (available; contains cross-reference to DEL-02-01)

### Assumptions

- Direction assignments for sibling discipline brief interfaces (DEP-03-01-011 through DEP-03-01-015) are DOWNSTREAM because Guidance.md explicitly states "the architectural sub-brief is the lead document in PKG-003 and sets the spatial framework the other briefs respond to." This represents information flow from DEL-03-01 to the sibling briefs.
- DEP-03-01-009 (Geotechnical Report) rated MEDIUM confidence because DEL-03-01 references it for site context, but the primary consumer of geotechnical data is the structural/civil design, not the architectural brief directly.

### Warnings

_No warnings._

---

## Run History

| RunDate | Mode | Strictness | DecompositionStatus | Warnings | ACTIVE_ANCHOR | ACTIVE_EXECUTION | Notes |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Located; v2.3 FINAL | None | 3 | 14 | Initial extraction. 17 total ACTIVE rows. No pre-existing CSV. |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 17 |
| RETIRED | 0 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 14 |
| NOT_APPLICABLE | 3 |

---
