# Dependencies

**Deliverable ID:** DEL-06-02
**Tracking Mode:** DECLARED + EXTRACTED

## Upstream Dependencies (this deliverable depends on)

_No critical dependencies declared._

## Downstream Dependents (other deliverables depend on this)

_No critical dependents declared._

## Notes

Dependencies are human-curated. Only interface-critical dependencies are recorded here.

---

## Extracted Dependency Register

**Register file:** `Dependencies.csv`
**Schema version:** v3.1
**Total rows:** 10 (10 ACTIVE, 0 RETIRED)

### Summary by Class

| DependencyClass | AnchorType | Count |
|-----------------|------------|-------|
| ANCHOR | IMPLEMENTS_NODE | 1 |
| ANCHOR | TRACES_TO_REQUIREMENT | 3 |
| EXECUTION | NOT_APPLICABLE | 6 |
| **Total** | | **10** |

### ANCHOR Edges (Pass 1)

| DependencyID | AnchorType | TargetType | TargetName | Confidence |
|--------------|------------|------------|------------|------------|
| DEP-0602-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0018 | HIGH |
| DEP-0602-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-002 | HIGH |
| DEP-0602-003 | TRACES_TO_REQUIREMENT | DOCUMENT | RFP Section 7.1.8 | HIGH |
| DEP-0602-008 | TRACES_TO_REQUIREMENT | DOCUMENT | RFP Section 7.2 | HIGH |

### EXECUTION Edges (Pass 2)

| DependencyID | Direction | DependencyType | TargetType | TargetName | Confidence |
|--------------|-----------|----------------|------------|------------|------------|
| DEP-0602-004 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-06-01 Design Methodology Narrative | HIGH |
| DEP-0602-005 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-09-01 Detailed Project Schedule | HIGH |
| DEP-0602-006 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-09-01 Detailed Project Schedule | HIGH |
| DEP-0602-007 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-07-05 Quality Management Narrative | HIGH |
| DEP-0602-009 | UPSTREAM | CONSTRAINT | DOCUMENT | CCDC 14-2013 (Design Build Contract) | MEDIUM |
| DEP-0602-010 | UPSTREAM | CONSTRAINT | DOCUMENT | Alberta Building Code (current edition) | MEDIUM |

---

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 10 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|--------------------|-------|
| NOT_APPLICABLE | 4 |
| TBD | 6 |

---

## Run Notes

**Run date:** 2026-02-17
**Mode:** UPDATE (initial extraction; no prior Dependencies.csv)
**Strictness:** CONSERVATIVE
**Consumer context:** NONE

**Defaults and paths used:**
- DECOMPOSITION_PATH: `/test/execution-6b/_Decomposition/Penhold_PSB_Project_Decomposition_v2.md` (v2.3 FINAL, located automatically)
- ANCHOR_DOC: `Datasheet.md` (selected by heuristic: contains deliverable identification fields including Scope Item, Objective, RFP Reference)
- EXECUTION_DOC_ORDER: `Procedure.md`, `Specification.md`, `Guidance.md` (ordered by workflow clarity)
- SOURCE_DOCS (AUTO): `Datasheet.md`, `Guidance.md`, `Procedure.md`, `Specification.md`
- _REFERENCES.md: read; used to confirm cross-reference targets (DEL-06-01, DEL-09-01, DEL-07-05)

**Anchor validation (via Decomposition):**
- SOW-0018 confirmed in Decomposition Section 7 Scope Ledger: maps to PKG-006 / DEL-06-02. Label: "Provide plan for detailed design and construction documents per Section 7.1.8."
- OBJ-002 confirmed in Decomposition Section 6: "Maximize Project Delivery Plan score (10 pts)."
- DEL-06-01 confirmed in Decomposition Section 9 under PKG-006.
- DEL-09-01 confirmed in Decomposition Section 9 under PKG-009.
- DEL-07-05 confirmed in Decomposition Section 9 under PKG-007.

**Integrity check results:**
- Parent anchor (IMPLEMENTS_NODE) count: 1 -- PASS
- DependencyID uniqueness: 10 unique of 10 total -- PASS
- All ACTIVE rows have EvidenceFile and SourceRef -- PASS
- FromDeliverableID consistency (all DEL-06-02) -- PASS
- No legacy enum values requiring normalization
- CSV parseable with 29 required columns -- PASS

**Extraction notes:**
- DEL-09-01 has a bidirectional interface with DEL-06-02: DEL-06-02 produces milestone definitions (DOWNSTREAM HANDOVER, DEP-0602-005) and DEL-09-01 provides schedule dates constraining this plan (UPSTREAM INTERFACE, DEP-0602-006). Both directions recorded as separate rows.
- CCDC 14-2013 and Alberta Building Code are listed as UPSTREAM CONSTRAINT with MEDIUM confidence because both are referenced in the Specification Standards table as applicable but "not directly reviewed -- location TBD." Guidance C-005 explicitly flags the CCDC 14-2013 question.
- Specification exclusions (DEL-07-01, DEL-07-02) were reviewed but not extracted as dependencies because they represent scope boundaries, not information flow.
- Guidance P-006 references a "Design Brief" concept but this is a proposal-stage commitment, not an explicit information-flow dependency to a specific deliverable. Not extracted.

---

## Run History

| Run | Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|-----|------|------|------------|---------------|----------|--------------|
| 1 | 2026-02-17 | UPDATE | CONSERVATIVE | v2.3 FINAL (located) | None | 10 |
