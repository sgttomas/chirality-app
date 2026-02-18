# Dependencies: DEL-03-03 Pavements, Aggregate Yard Areas & Concrete Aprons

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** `Dependencies.csv` (13 rows)
- **Last Run:** 2026-02-17
- **Schema Version:** v3.1

### Summary

| Category | Count |
|----------|-------|
| ANCHOR (IMPLEMENTS_NODE) | 1 |
| ANCHOR (TRACES_TO_REQUIREMENT) | 3 |
| EXECUTION (UPSTREAM) | 8 |
| EXECUTION (DOWNSTREAM) | 1 |
| **Total ACTIVE** | **13** |
| Total RETIRED | 0 |

### Anchor Register (Tree edges)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence | Notes |
|---|---|---|---|---|---|
| DEP-03-03-A001 | IMPLEMENTS_NODE | -- | PKG-003 Site & Civil Works | HIGH | Parent package anchor |
| DEP-03-03-A002 | TRACES_TO_REQUIREMENT | SOW-0107 | Sitework surfacing | HIGH | Scope item trace |
| DEP-03-03-A003 | TRACES_TO_REQUIREMENT | SOW-0108 | Concrete aprons at overhead doors | HIGH | Scope item trace |
| DEP-03-03-A004 | TRACES_TO_REQUIREMENT | OBJ-005 | Site/civil works objective | MEDIUM | Objective trace (source marks as ASSUMPTION/best-effort) |

### Execution Register (DAG edges)

| DependencyID | Direction | Type | TargetType | Target | Statement (short) |
|---|---|---|---|---|---|
| DEP-03-03-E001 | UPSTREAM | PREREQUISITE | DOCUMENT | Geotechnical Investigation Report | Geotech report required for pavement design parameters |
| DEP-03-03-E002 | UPSTREAM | PREREQUISITE | DOCUMENT | OSR Appendix A (10.3.7, 10.3.10) | OSR surfacing/apron requirements |
| DEP-03-03-E003 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-02 Grading/Earthworks/Drainage | Finished grade levels for pavement subgrade (design phase) |
| DEP-03-03-E004 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-002 PSB (overhead door locations) | Overhead door locations for concrete apron design |
| DEP-03-03-E005 | UPSTREAM | PREREQUISITE | PACKAGE | PKG-004 Cold Storage (overhead door locations) | Cold storage overhead door locations for apron design |
| DEP-03-03-E006 | UPSTREAM | PREREQUISITE | DOCUMENT | RFP Appendix B (Equipment List) | Equipment list for ESAL and loading calculations |
| DEP-03-03-E007 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-02 Grading/Earthworks/Drainage | Rough subgrade complete (construction phase) |
| DEP-03-03-E008 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-03-04 Site Utilities | Underground utilities installed before paving |
| DEP-03-03-E009 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-03-02 Grading/Earthworks/Drainage | Surface runoff directed to DEL-03-02 drainage infrastructure |

## Run Notes

### Defaults and Paths Used
- **SOURCE_DOCS (AUTO):** Datasheet.md, Guidance.md, Procedure.md, Specification.md
- **ANCHOR_DOC (AUTO):** Datasheet.md (selected: contains Identification table with Scope Coverage, Objective Support, Package fields)
- **EXECUTION_DOC_ORDER (AUTO):** Procedure.md, Specification.md, Guidance.md
- **DECOMPOSITION_PATH:** `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` (available; used for anchor validation and target resolution)
- **_REFERENCES.md:** Available (read; used to confirm document target pointers)
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** NONE

### Assumptions and Observations
- DEP-03-03-A004 (OBJ-005): Source Datasheet marks this as "ASSUMPTION: best-effort package-heuristic mapping". Confirmed in decomposition that OBJ-005 maps to PKG-003 deliverables. Confidence set to MEDIUM.
- DEP-03-03-E008: Source Procedure says "Site servicing deliverable" without specifying a deliverable ID. Mapped to DEL-03-04 (Site Utilities Distribution & Allowance-Based Tie-Ins) based on decomposition scope alignment (SOW-0109/SOW-0110 -> DEL-03-04). Confidence set to MEDIUM.
- DEP-03-03-E004/E005: Source uses package-level references (PKG-002, PKG-004) rather than specific deliverable IDs. Recorded as TargetType=PACKAGE. Likely source deliverables noted in row Notes (DEL-02-04 for PSB doors, DEL-04-02 for cold storage doors).
- DEL-03-02 appears as target in three distinct dependency rows (E003, E007, E009) reflecting different dependency relationships: design-phase grade input, construction-phase subgrade completion, and drainage interface. These are not duplicates.
- No warnings generated.

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Available (v1.0 Phase 7) | None | 4 | 9 | 13 |

## Lifecycle Summary

| Status | Count |
|--------|-------|
| ACTIVE | 13 |
| RETIRED | 0 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|--------------------|-------|
| TBD | 12 |
| NOT_APPLICABLE | 1 |

**Note:** DEP-03-03-A001 (IMPLEMENTS_NODE) has SatisfactionStatus=NOT_APPLICABLE (structural anchor, not a closeable dependency). All execution dependencies and requirement traces are TBD (not yet assessed for satisfaction).
