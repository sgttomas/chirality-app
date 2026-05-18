# Dependencies

**Deliverable ID:** DEL-01-02
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
**Total ACTIVE rows:** 22 (4 ANCHOR + 18 EXECUTION)
**Total RETIRED rows:** 0

### ANCHOR Dependencies (4 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-0102-A01 | IMPLEMENTS_NODE | WBS_NODE | PKG-001 -- Proposal Compliance Commercial and Team Qualifications | HIGH |
| DEP-0102-A02 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0001 -- Assemble compliant PDF and submit by email | HIGH |
| DEP-0102-A03 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0002 -- Letter of Offer and execution requirements | HIGH |
| DEP-0102-A04 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 -- Pass all mandatory requirements (formal compliance gate) | HIGH |

### EXECUTION Dependencies (18 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-0102-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-01 -- Compliance Matrix and Checklist | HIGH |
| DEP-0102-E02 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-03 -- Bonding and Insurance Evidence | HIGH |
| DEP-0102-E03 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-04 -- Appendix H Schedule A Pricing Summary | HIGH |
| DEP-0102-E04 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-05 -- Appendix H Schedule B Cost Breakdown | HIGH |
| DEP-0102-E05 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-07 -- Design-Build Firm Experience Profile | HIGH |
| DEP-0102-E06 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-08 -- Key Team Members and Resumes | HIGH |
| DEP-0102-E07 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-09 -- Appendix I Subtrade and Consultant List | HIGH |
| DEP-0102-E08 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-002 -- Conceptual Design | HIGH |
| DEP-0102-E09 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-003 -- Design Brief | HIGH |
| DEP-0102-E10 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-004 -- Sustainability and Energy | HIGH |
| DEP-0102-E11 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-005 -- Building Durability and Maintenance | HIGH |
| DEP-0102-E12 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-006 -- Delivery Plan | HIGH |
| DEP-0102-E13 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-007 -- Construction Methodology and Administration | HIGH |
| DEP-0102-E14 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-008 -- Commissioning Closeout and Warranty | HIGH |
| DEP-0102-E15 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-009 -- Schedule and Milestones | HIGH |
| DEP-0102-E16 | UPSTREAM | INTERFACE | DOCUMENT | RFP 2024_004 Penhold Public Services Building | HIGH |
| DEP-0102-E17 | UPSTREAM | CONSTRAINT | DOCUMENT | Addenda 01 through 03 | HIGH |
| DEP-0102-E18 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-06 -- Pricing Narrative and Assumptions | MEDIUM |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE
**Decomposition Path:** `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL, 2026-02-17)
**Decomposition Status:** Available; validation and label resolution performed successfully.

**Source Documents Scanned (AUTO):**
- `Datasheet.md` (ANCHOR_DOC -- primary anchor/definition source)
- `Procedure.md` (EXECUTION_DOC -- primary execution flow source)
- `Specification.md` (EXECUTION_DOC -- requirements and cross-references)
- `Guidance.md` (EXECUTION_DOC -- rationale and considerations)
- `_REFERENCES.md` (read-only; used for target resolution)

**Defaults Applied:**
- ANCHOR_DOC: `Datasheet.md` (selected by AUTO heuristic -- filename contains "datasheet")
- EXECUTION_DOC_ORDER: `Procedure.md`, `Specification.md`, `Guidance.md` (selected by AUTO heuristic)
- SOURCE_DOCS: All `.md` files in deliverable folder except `_DEPENDENCIES.md`, `_REFERENCES.md`, `_STATUS.md`, `_CONTEXT.md`, `_SEMANTIC.md`, `_SEMANTIC_LENSING.md`

**Integrity Checks:**
- Parent anchor (IMPLEMENTS_NODE): 1 ACTIVE row -- PASS
- DependencyID uniqueness: All 22 IDs unique -- PASS
- FromDeliverableID consistency: All rows = DEL-01-02 -- PASS
- All ACTIVE rows have EvidenceFile and SourceRef -- PASS
- All enum values canonical -- PASS
- CSV parseable -- PASS

**Warnings:** None.

**Extraction Notes:**
- DEL-01-02 is the terminal assembly deliverable for the entire proposal. It has the highest upstream prerequisite count of any deliverable in the project because it requires finalized content from all other packages (PKG-002 through PKG-009) and all other PKG-001 deliverables except itself.
- DEP-0102-E18 (DEL-01-06) is marked IMPLICIT/MEDIUM because the Procedure Pre-Condition 1 checklist does not explicitly name DEL-01-06, but the Specification In Scope statement covers "all proposal content (Sections 6-9)" which includes the pricing narrative. Marked as ASSUMPTION in Notes.
- Package-level dependencies (DEP-0102-E08 through E15) target TargetType=PACKAGE because the Procedure Pre-Condition 1 references package-equivalent content (e.g., "All conceptual design content (PKG-002 equivalent)") rather than individual deliverables within those packages.

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-02-17 | UPDATE | CONSERVATIVE | v2.3 FINAL (available) | None | 4 | 18 | 22 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 22 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 22 |
