# Dependencies: DEL-05-01 Option - Built-in Wash Bay

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** COMPLETED
- **Dependencies.csv:** `Dependencies.csv` (same folder)
- **RegisterSchemaVersion:** v3.1
- **Total rows:** 10
- **ACTIVE:** 10
- **RETIRED:** 0

### ANCHOR Edges (2 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-05-01-A01 | IMPLEMENTS_NODE | WBS_NODE | SOW-0500 | SOW-0500 - Built-in wash bay and equipment | HIGH |
| DEP-05-01-A02 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-010 | OBJ-010 - Transparent separable pricing for optional scope items | HIGH |

### EXECUTION Edges (8 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Statement (summary) | Confidence |
|---|---|---|---|---|---|---|
| DEP-05-01-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-02-03 PW Shop Bays | PW bay area layout needed for fourth bay location | HIGH |
| DEP-05-01-E02 | UPSTREAM | PREREQUISITE | DOCUMENT | RFP Appendix B | Fleet vehicle dimensions for bay sizing | HIGH |
| DEP-05-01-E03 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-02 Grading/Drainage | Drainage/effluent tie-in coordination | HIGH |
| DEP-05-01-E04 | UPSTREAM | PREREQUISITE | EXTERNAL | AEP / Town environmental | Environmental regulatory confirmation for effluent | HIGH |
| DEP-05-01-E05 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-04 Permitting/AHJ | AHJ pre-consultation for wash bay elements | MEDIUM |
| DEP-05-01-E06 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-02-05 Mechanical/Plumbing | Base bay sump and mechanical interface | MEDIUM |
| DEP-05-01-E07 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-02-05 Mechanical/Plumbing | HVAC design input memo to mechanical discipline | MEDIUM |
| DEP-05-01-E08 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-04 Site Utilities | Water supply and wastewater utility stubs | HIGH |

## Run Notes

### Run 2026-02-17 (initial extraction)

**Configuration:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: AUTO (resolved to: Datasheet.md, Guidance.md, Procedure.md, Specification.md)
- ANCHOR_DOC: AUTO (resolved to: Datasheet.md)
- EXECUTION_DOC_ORDER: AUTO (resolved to: Procedure.md, Specification.md, Guidance.md)
- DECOMPOSITION_PATH: `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` (found and used)

**Defaults applied:**
- DOC_ROLE_MAP: DEFAULT heuristic. Datasheet.md selected as ANCHOR_DOC (contains "datasheet"; has explicit Scope Item and Objective identifiers in Identification table). Procedure.md prioritized first in EXECUTION_DOC_ORDER (contains "procedure"; has explicit prerequisites and workflow steps).
- _REFERENCES.md read; used to confirm document references (OSR location, Addendum 03 location).

**Assumptions:**
- None. All extracted rows are FACT-based with explicit evidence from source documents.

**Warnings:**
- (none)

**Quality check results:**
- Schema: PASS (all required columns present; CSV parseable)
- DependencyID uniqueness: PASS (10 unique IDs)
- Evidence coverage: PASS (all ACTIVE rows have EvidenceFile + SourceRef)
- Enum normalization: PASS (all values canonical)
- Parent anchor check: PASS (exactly 1 IMPLEMENTS_NODE row: DEP-05-01-A01)
- Duplicate check: PASS (no duplicate rows)
- _DEPENDENCIES.md vs Dependencies.csv consistency: PASS (counts match)

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ANCHOR ACTIVE | EXECUTION ACTIVE | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Found (v1.0 PHASE7) | (none) | 2 | 8 | 10 |

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 10 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| TBD | 10 |
