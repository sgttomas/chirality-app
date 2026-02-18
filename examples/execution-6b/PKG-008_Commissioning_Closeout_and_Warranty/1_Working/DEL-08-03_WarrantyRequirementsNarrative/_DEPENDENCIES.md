# Dependencies

**Deliverable ID:** DEL-08-03
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
**Total Rows:** 10 (all ACTIVE)

### Summary by Class

| DependencyClass | AnchorType | Count |
|-----------------|------------|------:|
| ANCHOR | IMPLEMENTS_NODE | 1 |
| ANCHOR | TRACES_TO_REQUIREMENT | 1 |
| EXECUTION | NOT_APPLICABLE | 8 |

### Summary by Direction

| Direction | Count |
|-----------|------:|
| UPSTREAM | 8 |
| DOWNSTREAM | 2 |

### Compact Register

| DependencyID | Class | Direction | Type | TargetType | Target | Confidence |
|---|---|---|---|---|---|---|
| DEP-08-03-001 | ANCHOR | UPSTREAM | OTHER | WBS_NODE | SOW-0032 | HIGH |
| DEP-08-03-002 | ANCHOR | UPSTREAM | OTHER | REQUIREMENT | OBJ-002 | HIGH |
| DEP-08-03-003 | EXECUTION | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-08-01 (Commissioning Narrative) | HIGH |
| DEP-08-03-004 | EXECUTION | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-08-02 (Deficiencies Management) | MEDIUM |
| DEP-08-03-005 | EXECUTION | UPSTREAM | CONSTRAINT | DOCUMENT | RFP Section 7.6 -- Warranty Requirements | HIGH |
| DEP-08-03-006 | EXECUTION | UPSTREAM | CONSTRAINT | DOCUMENT | Appendix J SC54-SC55 | HIGH |
| DEP-08-03-007 | EXECUTION | UPSTREAM | CONSTRAINT | DOCUMENT | CCDC 14-2013 GC 12.5 (location TBD) | MEDIUM |
| DEP-08-03-008 | EXECUTION | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-08-01 (O&M Manual warranty sections) | HIGH |
| DEP-08-03-009 | EXECUTION | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-01 (Proposal assembly) | HIGH |
| DEP-08-03-010 | EXECUTION | UPSTREAM | CONSTRAINT | DOCUMENT | RFP Section 7.5 -- Substantial Performance | HIGH |

---

## Run Notes

**Run Date:** 2026-02-17
**Mode:** UPDATE
**Strictness:** CONSERVATIVE
**Consumer Context:** NONE

**Defaults and Paths Used:**
- DECOMPOSITION_PATH: `_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (located automatically; v2.3 FINAL)
- SOURCE_DOCS: AUTO -- scanned deliverable folder; identified 4 candidate source documents
- DOC_ROLE_MAP: DEFAULT heuristic
- ANCHOR_DOC: `Datasheet.md` (selected: contains Identification table with Scope Item, Objective, and Package references)
- EXECUTION_DOC_ORDER: `Procedure.md`, `Specification.md`, `Guidance.md` (Procedure has explicit Prerequisites section; Specification has Requirements with cross-references; Guidance has Considerations with interface details)

**Extraction Notes:**
- Pass 1 (ANCHOR): Extracted 1 parent anchor (SOW-0032) and 1 requirement trace (OBJ-002) from Datasheet.md Identification table. Both confirmed against decomposition.
- Pass 2 (EXECUTION): Extracted 8 execution edges from Procedure.md (Prerequisites, Required References), Specification.md (R-09, R-10), and Datasheet.md (Conditions).
- DEP-08-03-003 (DEL-08-01 UPSTREAM): Explicit prerequisite -- "Must be drafted or at least outlined" (Procedure Prerequisites).
- DEP-08-03-004 (DEL-08-02 UPSTREAM): Softer prerequisite -- "Should be drafted or outlined" (Procedure Prerequisites). Confidence MEDIUM due to "should" vs "must."
- DEP-08-03-007 (CCDC 14-2013): Location TBD. Procedure and Specification both flag A-002: base GC 12.5 provisions not yet reviewed. Confidence MEDIUM.
- DEP-08-03-008 (DEL-08-01 DOWNSTREAM): Bidirectional relationship. DEL-08-03 defines warranty terms that must be reflected in DEL-08-01 O&M Manual warranty sections.
- DEP-08-03-009 (DEL-01-01 DOWNSTREAM): Warranty narrative is a proposal section that must be incorporated into the final proposal PDF assembled by DEL-01-01/SOW-0001.

**Warnings:** None.

**Quality Check Results:**
- All required columns present in Dependencies.csv.
- All 10 DependencyIDs unique.
- All ACTIVE rows have EvidenceFile and SourceRef populated.
- Parent anchor count = 1 (no FLOATING_NODE or AMBIGUOUS_ANCHOR warning).
- Enum values are canonical (no legacy normalization needed).
- _DEPENDENCIES.md counts consistent with Dependencies.csv.

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|-----|------|------|------------|---------------|----------|-------------:|
| 1 | 2026-02-17 | UPDATE | CONSERVATIVE | Penhold_PSB_Project_Decomposition_v2.md (v2.3 FINAL) | None | 10 |

---

## Lifecycle Summary

| Status | Count |
|--------|------:|
| ACTIVE | 10 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|--------------------|------:|
| TBD | 10 |
