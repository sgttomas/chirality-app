# Dependencies

**Deliverable ID:** DEL-01-04
**Deliverable Name:** Appendix H - Schedule A - Pricing Summary
**Package:** PKG-001 -- Proposal Compliance, Commercial & Team Qualifications
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Total ACTIVE rows:** 13
**Total RETIRED rows:** 0

| Class | Count |
|---|---|
| ANCHOR (IMPLEMENTS_NODE) | 1 |
| ANCHOR (TRACES_TO_REQUIREMENT) | 6 |
| EXECUTION (UPSTREAM) | 5 |
| EXECUTION (DOWNSTREAM) | 1 |

### ANCHOR Dependencies (Pass 1 -- Vertical)

| DependencyID | AnchorType | TargetRefID | TargetName | Statement (short) | Confidence |
|---|---|---|---|---|---|
| DEP-0104-A001 | IMPLEMENTS_NODE | SOW-0005 | SOW-0005 | Implements SOW-0005: Complete Schedule A pricing summary | HIGH |
| DEP-0104-A002 | TRACES_TO_REQUIREMENT | OBJ-007 | OBJ-007 | Traces to OBJ-007: Competitive, compliant price package (35 pts) | HIGH |
| DEP-0104-A003 | TRACES_TO_REQUIREMENT | C-05 | C-05 | Must comply with C-05: Use Appendix H pricing template | HIGH |
| DEP-0104-A004 | TRACES_TO_REQUIREMENT | C-07 | C-07 | Must comply with C-07: Addenda acknowledgement required | HIGH |
| DEP-0104-A005 | TRACES_TO_REQUIREMENT | C-11 | C-11 | Must comply with C-11: FF&E not in base cost | HIGH |
| DEP-0104-A006 | TRACES_TO_REQUIREMENT | C-08 | C-08 | Must comply with C-08: Bond costs in proposal price | HIGH |
| DEP-0104-A007 | TRACES_TO_REQUIREMENT | C-12 | C-12 | Must comply with C-12: Site servicing cash allowance | HIGH |

### EXECUTION Dependencies (Pass 2 -- Horizontal)

| DependencyID | Direction | Type | TargetID | TargetName | Statement (short) | Confidence |
|---|---|---|---|---|---|---|
| DEP-0104-E001 | UPSTREAM | PREREQUISITE | DEL-01-05 | Schedule B - Cost Breakdown | Provides all line values (Subtotal Item 1 to Line 1-1; Additional Items to Lines 1-2 through 1-7) | HIGH |
| DEP-0104-E002 | UPSTREAM | PREREQUISITE | DEL-01-06 | Pricing Narrative and Assumptions | Assumptions and allowances must be documented before Schedule A completion | HIGH |
| DEP-0104-E003 | UPSTREAM | PREREQUISITE | DEL-01-03 | Bonding and Insurance Evidence | Bond and CCIP costs calculated and incorporated in Schedule B before flowing to Line 1-1 | HIGH |
| DEP-0104-E004 | UPSTREAM | CONSTRAINT | (DOCUMENT) | RFP Appendix H template | Schedule A must use the RFP-provided template without modification | HIGH |
| DEP-0104-E005 | UPSTREAM | CONSTRAINT | (DOCUMENT) | Addendum 03 | Constrains pricing: FF&E as additional item; site servicing allowance; Pickled Sand excluded | HIGH |
| DEP-0104-E006 | DOWNSTREAM | HANDOVER | DEL-01-02 | Formal Submission Package | Schedule A inserted into proposal PDF at Section 8 position | HIGH |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

**Defaults and paths used:**
- DECOMPOSITION_PATH: `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL, located automatically)
- SOURCE_DOCS: AUTO -- scanned deliverable folder; identified 4 source documents:
  - `Datasheet.md` (ANCHOR_DOC -- primary definition/traceability signal)
  - `Guidance.md` (EXECUTION_DOC)
  - `Procedure.md` (EXECUTION_DOC)
  - `Specification.md` (EXECUTION_DOC)
- ANCHOR_DOC: `Datasheet.md` (selected by heuristic: filename contains "datasheet")
- EXECUTION_DOC_ORDER: `Procedure.md`, `Specification.md`, `Guidance.md` (ordered by workflow clarity)
- _REFERENCES.md: read; used to confirm cross-reference targets (DEL-01-05, DEL-01-06, DEL-01-03)

**Warnings:** None.

**Observations:**
- Single parent anchor (SOW-0005) confirmed via Decomposition Scope Ledger. No ambiguity.
- All 3 upstream EXECUTION deliverable targets (DEL-01-05, DEL-01-06, DEL-01-03) are within PKG-001, confirmed in Decomposition.
- Downstream target DEL-01-02 (Formal Submission Package) is within PKG-001, confirmed in Decomposition.
- Two DOCUMENT-type constraints (RFP Appendix H template and Addendum 03) are external source documents.
- All evidence locations are explicit with file + heading references. No "location TBD" entries.

---

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Notes |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | v2.3 FINAL (located) | None | 7 | 6 | Initial extraction run. 13 total ACTIVE rows. |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 13 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 13 |

---
