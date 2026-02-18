# Dependencies

**Deliverable ID:** DEL-01-01
**Deliverable Name:** Compliance Matrix and Checklist
**Package:** PKG-001 -- Proposal Compliance, Commercial & Team Qualifications
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated in the declared sections above. The extracted register below is machine-generated from source document analysis.

---

## Extracted Dependency Register

**Schema Version:** v3.1
**Total ACTIVE rows:** 17
**Total RETIRED rows:** 0

### Summary by Class

| DependencyClass | AnchorType | Count |
|-----------------|------------|-------|
| ANCHOR | IMPLEMENTS_NODE | 1 |
| ANCHOR | TRACES_TO_REQUIREMENT | 2 |
| EXECUTION | NOT_APPLICABLE | 14 |

### Summary by Direction

| Direction | Count |
|-----------|-------|
| UPSTREAM | 16 |
| DOWNSTREAM | 1 |

### Compact Register

| DependencyID | Class | AnchorType | Dir | Type | TargetType | Target | Confidence | Status |
|-------------|-------|------------|-----|------|------------|--------|------------|--------|
| DEP-01-01-001 | ANCHOR | IMPLEMENTS_NODE | UP | OTHER | WBS_NODE | PKG-001 | HIGH | ACTIVE |
| DEP-01-01-002 | ANCHOR | TRACES_TO_REQ | UP | OTHER | REQUIREMENT | SOW-0003 | HIGH | ACTIVE |
| DEP-01-01-003 | ANCHOR | TRACES_TO_REQ | UP | OTHER | REQUIREMENT | OBJ-001 | HIGH | ACTIVE |
| DEP-01-01-004 | EXECUTION | N/A | UP | PREREQUISITE | DOCUMENT | RFP Base Document | HIGH | ACTIVE |
| DEP-01-01-005 | EXECUTION | N/A | UP | PREREQUISITE | DOCUMENT | Addendum 01 | HIGH | ACTIVE |
| DEP-01-01-006 | EXECUTION | N/A | UP | PREREQUISITE | DOCUMENT | Addendum 02 | HIGH | ACTIVE |
| DEP-01-01-007 | EXECUTION | N/A | UP | PREREQUISITE | DOCUMENT | Addendum 03 | HIGH | ACTIVE |
| DEP-01-01-008 | EXECUTION | N/A | UP | PREREQUISITE | DOCUMENT | Decomposition v2 | HIGH | ACTIVE |
| DEP-01-01-009 | EXECUTION | N/A | DOWN | HANDOVER | DELIVERABLE | DEL-01-02 (Formal Submission Package) | HIGH | ACTIVE |
| DEP-01-01-010 | EXECUTION | N/A | UP | PREREQUISITE | DELIVERABLE | DEL-01-03 (Bonding & Insurance) | HIGH | ACTIVE |
| DEP-01-01-011 | EXECUTION | N/A | UP | INTERFACE | DELIVERABLE | DEL-01-04 (Schedule A) | HIGH | ACTIVE |
| DEP-01-01-012 | EXECUTION | N/A | UP | INTERFACE | DELIVERABLE | DEL-01-05 (Schedule B) | MEDIUM | ACTIVE |
| DEP-01-01-013 | EXECUTION | N/A | UP | INTERFACE | DELIVERABLE | DEL-01-09 (Appendix I) | MEDIUM | ACTIVE |
| DEP-01-01-014 | EXECUTION | N/A | UP | CONSTRAINT | REQUIREMENT | C-01 (PDF <= 15 MB) | HIGH | ACTIVE |
| DEP-01-01-015 | EXECUTION | N/A | UP | CONSTRAINT | REQUIREMENT | C-02 (Section order) | HIGH | ACTIVE |
| DEP-01-01-016 | EXECUTION | N/A | UP | CONSTRAINT | REQUIREMENT | C-07 (Addenda acknowledgement) | HIGH | ACTIVE |
| DEP-01-01-017 | EXECUTION | N/A | UP | CONSTRAINT | REQUIREMENT | C-10 (Pickled sand excluded) | HIGH | ACTIVE |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE
**Decomposition Path:** `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL, located successfully)
**Source Documents (AUTO):**
- ANCHOR_DOC: `Datasheet.md` (selected by heuristic: contains "datasheet" in filename + deliverable identification/scope/objective fields)
- EXECUTION_DOC_ORDER: `Procedure.md`, `Specification.md`, `Guidance.md` (ordered by workflow clarity)
- Additional read-only input: `_REFERENCES.md`, `_CONTEXT.md`

**Defaults applied:**
- SOURCE_DOCS=AUTO: scanned all .md files in deliverable folder excluding `_DEPENDENCIES.md`, `_STATUS.md`, `_SEMANTIC_LENSING.md`, `_SEMANTIC.md`
- ANCHOR_DOC=AUTO: selected `Datasheet.md`
- EXECUTION_DOC_ORDER=AUTO: `Procedure.md` (prerequisites/steps), `Specification.md` (requirements/cross-refs), `Guidance.md` (principles/considerations)

**Assumptions:**
- ASSUMPTION: Cross-references from Specification.md to PKG-002 through PKG-010 deliverables are verification/tracking relationships at the package level. Under CONSERVATIVE strictness, only the strongest explicit artifact-transfer edges (to sibling DEL-01-0x deliverables with specific verification actions in Procedure Step 6) are extracted as EXECUTION rows. The package-level tracking references are not extracted as individual dependency rows because they represent the compliance matrix's general tracking function rather than specific artifact transfers.
- ASSUMPTION: OBJ-001 is treated as a TRACES_TO_REQUIREMENT anchor rather than an EXECUTION edge because it represents traceability to a definition-layer objective, not an information-flow prerequisite.

**Warnings:** None.

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|-----|------|------|------------|---------------|----------|--------------|
| 1 | 2026-02-17 | UPDATE | CONSERVATIVE | v2.3 FINAL (located) | None | 17 |

---

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 17 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|-------------------|-------|
| TBD | 14 |
| NOT_APPLICABLE | 3 |

**Breakdown:**
- ANCHOR rows (3): all `SatisfactionStatus=NOT_APPLICABLE` (anchors are traceability links, not closeable)
- EXECUTION rows (14): all `SatisfactionStatus=TBD` (5 PREREQUISITE-document, 1 PREREQUISITE-deliverable, 2 INTERFACE, 1 HANDOVER, 4 CONSTRAINT, 1 PREREQUISITE-decomposition)

---

## Downstream Handoff Notes

_Not applicable (CONSUMER_CONTEXT=NONE)._
