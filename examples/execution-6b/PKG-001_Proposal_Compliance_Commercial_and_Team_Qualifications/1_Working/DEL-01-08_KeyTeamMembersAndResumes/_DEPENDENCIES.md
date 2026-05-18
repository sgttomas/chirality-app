# Dependencies

**Deliverable ID:** DEL-01-08
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
**Total ACTIVE rows:** 8
**Total RETIRED rows:** 0

| DependencyID | Class | AnchorType | Direction | Type | TargetType | Target | Confidence | Status |
|---|---|---|---|---|---|---|---|---|
| DEP-01-08-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | SOW-0017 | HIGH | ACTIVE |
| DEP-01-08-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-006 | HIGH | ACTIVE |
| DEP-01-08-003 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | RFP Section 7.1.7 | HIGH | ACTIVE |
| DEP-01-08-004 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-07 | HIGH | ACTIVE |
| DEP-01-08-005 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-09 | HIGH | ACTIVE |
| DEP-01-08-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | RFP 2024_004 Section 7.1.7 | HIGH | ACTIVE |
| DEP-01-08-007 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-02 | HIGH | ACTIVE |
| DEP-01-08-008 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-09 | HIGH | ACTIVE |

### Summary by Class

| DependencyClass | ACTIVE | RETIRED |
|---|---|---|
| ANCHOR | 3 | 0 |
| EXECUTION | 5 | 0 |
| **Total** | **8** | **0** |

### Summary by Direction

| Direction | Count |
|---|---|
| UPSTREAM | 7 |
| DOWNSTREAM | 1 |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

**Defaults and Paths Used:**
- DECOMPOSITION_PATH: `/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (located automatically; v2.3 FINAL)
- SOURCE_DOCS: AUTO -- discovered 4 source documents: `Datasheet.md`, `Procedure.md`, `Specification.md`, `Guidance.md`
- DOC_ROLE_MAP: DEFAULT heuristic applied
  - ANCHOR_DOC: `Datasheet.md` (matched `datasheet` pattern; contains definition/traceability fields)
  - EXECUTION_DOCS (ordered): `Procedure.md`, `Specification.md`, `Guidance.md`
- ANCHOR_DOC: `Datasheet.md` (AUTO selection)
- EXECUTION_DOC_ORDER: AUTO -- `Procedure.md` (strongest workflow/prerequisite signals), `Specification.md` (requirements/verification), `Guidance.md` (principles/considerations)
- `_REFERENCES.md`: read; used for cross-reference context (DEL-01-07, DEL-01-09)

**Decomposition Validation:**
- Decomposition located and loaded successfully (v2.3 FINAL, 2026-02-17)
- DEL-01-08 confirmed in Decomposition Section 9 under PKG-001
- SOW-0017 confirmed mapped to DEL-01-08 in Scope Ledger (Section 10)
- OBJ-006 confirmed as supporting objective

**Integrity Checks:**
- Parent anchor (IMPLEMENTS_NODE): 1 found (DEP-01-08-001 -> SOW-0017) -- PASS
- Multiple parent anchors: No -- PASS
- All ACTIVE rows have EvidenceFile and SourceRef -- PASS
- DependencyID uniqueness: 8 unique IDs -- PASS
- CSV parseable: PASS
- Enum normalization: all values canonical -- PASS
- _DEPENDENCIES.md counts match Dependencies.csv: PASS

**Assumptions Logged:**
- None. All extracted dependencies are EXPLICIT with HIGH confidence and marked as FACT in Notes.

**Warnings:** None.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) | None | 8 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 8 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| NOT_APPLICABLE | 3 (ANCHOR rows) |
| TBD | 5 (EXECUTION rows) |
