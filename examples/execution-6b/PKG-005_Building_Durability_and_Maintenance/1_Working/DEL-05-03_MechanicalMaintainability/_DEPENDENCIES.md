# Dependencies

**Deliverable ID:** DEL-05-03
**Deliverable Name:** Mechanical Maintainability
**Package:** PKG-005 -- Building Durability & Maintenance
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated above. Only interface-critical dependencies are recorded in the declared sections. The extracted register below is machine-generated from source document analysis.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 11
**Total RETIRED rows:** 0

| DependencyID | Class | AnchorType | Direction | Type | TargetType | Target | Confidence | Status |
|---|---|---|---|---|---|---|---|---|
| DEP-05-03-001 | ANCHOR | IMPLEMENTS_NODE | UPSTREAM | OTHER | WBS_NODE | SOW-0013 | HIGH | ACTIVE |
| DEP-05-03-002 | ANCHOR | TRACES_TO_REQUIREMENT | UPSTREAM | OTHER | REQUIREMENT | OBJ-005 | HIGH | ACTIVE |
| DEP-05-03-003 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-04 (Mechanical Concept Narrative) | HIGH | ACTIVE |
| DEP-05-03-004 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-04-02 (Mechanical Energy and Solar Readiness) | HIGH | ACTIVE |
| DEP-05-03-005 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-08-01 (Commissioning Training Closeout) | HIGH | ACTIVE |
| DEP-05-03-006 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-01 (Architectural Durability) | MEDIUM | ACTIVE |
| DEP-05-03-007 | EXECUTION | NOT_APPLICABLE | UPSTREAM | INTERFACE | DELIVERABLE | DEL-05-02 (Structural Durability) | MEDIUM | ACTIVE |
| DEP-05-03-008 | EXECUTION | NOT_APPLICABLE | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-05-04 (Electrical Maintainability) | MEDIUM | ACTIVE |
| DEP-05-03-009 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | DOCUMENT | RFP 2024_004 | HIGH | ACTIVE |
| DEP-05-03-010 | EXECUTION | NOT_APPLICABLE | UPSTREAM | CONSTRAINT | DOCUMENT | Addendum 03 (Jul 31 2024) | HIGH | ACTIVE |
| DEP-05-03-011 | EXECUTION | NOT_APPLICABLE | UPSTREAM | PREREQUISITE | DOCUMENT | 2021 Geotechnical Report | HIGH | ACTIVE |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| **ACTIVE** | 11 |
| **RETIRED** | 0 |
| **ANCHOR rows** | 2 |
| **EXECUTION rows** | 9 |
| **UPSTREAM** | 9 |
| **DOWNSTREAM** | 2 |
| **HIGH confidence** | 9 |
| **MEDIUM confidence** | 2 |
| **SatisfactionStatus: TBD** | 7 |
| **SatisfactionStatus: PENDING** | 2 |
| **SatisfactionStatus: (not yet assessed)** | 2 |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

**Decomposition Path:** `/Users/ryan/ai-env/projects/chirality-app-test/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL, located automatically)

**Source Documents Scanned (AUTO):**
- `Datasheet.md` -- ANCHOR_DOC (primary anchor/definition signal; contains Identification, Attributes, Conditions, Construction, References)
- `Procedure.md` -- EXECUTION_DOC (primary execution signal; contains Prerequisites table with explicit upstream dependencies)
- `Specification.md` -- EXECUTION_DOC (secondary execution signal; contains Scope, Requirements R-MEL-01 through R-MEL-14, Documentation Cross-References)
- `Guidance.md` -- EXECUTION_DOC (tertiary execution signal; contains Principles, Considerations, Trade-offs, Conflict Table)

**Reference Document Used:**
- `_REFERENCES.md` -- Used to confirm cross-references to DEL-02-04 and DEL-04-02

**Defaults Applied:**
- SOURCE_DOCS: AUTO (4 source documents detected; excluded _DEPENDENCIES.md, _REFERENCES.md, _CONTEXT.md, _STATUS.md, _SEMANTIC.md, _SEMANTIC_LENSING.md)
- ANCHOR_DOC: Datasheet.md (selected by heuristic: filename contains "datasheet")
- EXECUTION_DOC_ORDER: Procedure.md, Specification.md, Guidance.md (selected by heuristic: procedure > specification > guidance)

**Assumptions:**
- DEL-05-06 and DEL-05-08 interface rows with DEL-05-01/DEL-05-02 are classified as UPSTREAM because architectural and structural decisions constrain mechanical access provisions. DEL-05-04 interface is DOWNSTREAM because mechanical generator/ATS information flows to electrical maintainability.
- SatisfactionStatus for DEL-02-04 and DEL-04-02 prerequisites set to PENDING because both are noted as "not yet produced" in source documents.

**Warnings:** None.

**Quality Check Results:**
- Schema check: PASS (all required columns present; CSV parseable)
- DependencyID uniqueness: PASS (11 unique IDs)
- Evidence presence: PASS (all ACTIVE rows have EvidenceFile and SourceRef)
- Parent anchor check: PASS (exactly 1 IMPLEMENTS_NODE row: DEP-05-03-001 -> SOW-0013)
- Enum normalization: PASS (all values canonical)
- _DEPENDENCIES.md consistency: PASS (counts match CSV)
- Duplicate check: PASS (no obvious duplicates)

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE ANCHOR | ACTIVE EXECUTION | Notes |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-02-17 | UPDATE | CONSERVATIVE | v2.3 FINAL (located) | None | 2 | 9 | Initial extraction. 11 total ACTIVE rows. No RETIRED rows. |
