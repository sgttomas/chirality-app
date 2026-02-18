# Dependencies

**Deliverable ID:** DEL-02-04
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 12
**ANCHOR rows:** 4 (1 IMPLEMENTS_NODE, 3 TRACES_TO_REQUIREMENT)
**EXECUTION rows:** 8 (3 UPSTREAM PREREQUISITE, 1 DOWNSTREAM INTERFACE, 3 DOWNSTREAM HANDOVER, 1 UPSTREAM CONSTRAINT)
**RETIRED rows:** 0

| DependencyID | Class | AnchorType | Dir | Type | TargetType | Target | Status |
|---|---|---|---|---|---|---|---|
| DEP-02-04-ANC-01 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | PKG-002 (Conceptual Design) | ACTIVE |
| DEP-02-04-ANC-02 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | SOW-0009 (Concept design package) | ACTIVE |
| DEP-02-04-ANC-03 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | SOW-0010 (Embed program clarifications) | ACTIVE |
| DEP-02-04-ANC-04 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-003 (Proposed Conceptual Design, 20 pts) | ACTIVE |
| DEP-02-04-EXE-01 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-01 (Architectural Concept Package) | ACTIVE |
| DEP-02-04-EXE-02 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-02 (Civil/Site Concept Plan) | ACTIVE |
| DEP-02-04-EXE-03 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-03 (Structural Concept Narrative) | ACTIVE |
| DEP-02-04-EXE-04 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-02-05 (Electrical/IT Concept Narrative) | ACTIVE |
| DEP-02-04-EXE-05 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-04-02 (Mechanical Energy and Solar Readiness) | ACTIVE |
| DEP-02-04-EXE-06 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-05-03 (Mechanical Maintainability) | ACTIVE |
| DEP-02-04-EXE-07 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02 (Formal Submission Package) | ACTIVE |
| DEP-02-04-EXE-08 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | DOCUMENT | Appendix-D (2021 Geotechnical Report) | ACTIVE |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

**Defaults and Paths Used:**
- DECOMPOSITION_PATH: `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL, located automatically)
- SOURCE_DOCS: AUTO -- detected 4 source documents: `Datasheet.md`, `Guidance.md`, `Procedure.md`, `Specification.md`
- ANCHOR_DOC: `Datasheet.md` (selected by DEFAULT heuristic -- contains `datasheet` filename signal; has Identification table with deliverable identity, scope items, objectives)
- EXECUTION_DOC_ORDER: `Procedure.md`, `Specification.md`, `Guidance.md` (ordered by workflow clarity per DEFAULT heuristic)
- _REFERENCES.md: read (contains cross-references to DEL-02-01, DEL-02-05, DEL-04-02)

**Assumptions:**
- ANCHOR_DOC identification via filename heuristic (`Datasheet` pattern match). ASSUMPTION: Datasheet.md is the primary definition/traceability document.
- All source documents scanned for execution dependencies. Evidence quotes kept under 30 words.

**Warnings:**
- (none)

**Quality Check Results:**
- Schema: PASS (all required columns present; CSV parseable)
- DependencyID uniqueness: PASS (12 unique IDs)
- Evidence coverage: PASS (all ACTIVE rows have EvidenceFile and SourceRef)
- Parent anchor check: PASS (exactly 1 IMPLEMENTS_NODE row: DEP-02-04-ANC-01)
- Duplicate check: PASS (no duplicate extracted rows)
- _DEPENDENCIES.md vs Dependencies.csv count consistency: PASS (12 ACTIVE, 0 RETIRED)

---

## Run History

| Run | Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|---|
| 1 | 2026-02-17 | UPDATE | CONSERVATIVE | v2.3 FINAL (located) | none | 12 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 12 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 12 |
