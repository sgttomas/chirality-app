# Dependencies: DEL-001-07 Door & Window Schedule

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** Dependencies.csv (v3.1 schema, 13 rows)
- **Summary:**
  - **ANCHOR rows:** 3 ACTIVE
  - **EXECUTION rows:** 10 ACTIVE
  - **RETIRED rows:** 0

### ANCHOR Edges (Tree -- Definition Traceability)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-001-07-A01 | IMPLEMENTS_NODE | SOW-0011 | Complete final architectural design for the addition | HIGH |
| DEP-001-07-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition | HIGH |
| DEP-001-07-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |

### EXECUTION Edges (DAG -- Information Flow)

| DependencyID | Direction | DependencyType | TargetType | TargetID | TargetName | Confidence |
|---|---|---|---|---|---|---|
| DEP-001-07-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-01 | Preliminary Architectural Design | HIGH |
| DEP-001-07-E02 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-02 | Architectural Floor Plans | HIGH |
| DEP-001-07-E03 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-004-03 | Power Distribution Plans | HIGH |
| DEP-001-07-E04 | UPSTREAM | CONSTRAINT | EXTERNAL | -- | Camrose County Equipment Fleet Dimensions | HIGH |
| DEP-001-07-E05 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-03 | Structural Framing Plans | HIGH |
| DEP-001-07-E06 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-003-02 | HVAC Layout Plans | HIGH |
| DEP-001-07-E07 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-009-04 | Code Compliance Register & Inspection Log | MEDIUM |
| DEP-001-07-E08 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-004-06 | Panel Schedules | HIGH |
| DEP-001-07-E09 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-001-11 | Architectural Specification | MEDIUM |
| DEP-001-07-E10 | UPSTREAM | PREREQUISITE | DOCUMENT | R-10 | Addendum 4 (folding outward overhead doors per Q4) | HIGH |

## Run Notes

### Run: 2026-03-26 (R2 refresh)

**Parameters:**
- SCOPE: DEL-001-07_Door-Window-Schedule (as part of PKG-001 full refresh)
- MODE: UPDATE | STRICTNESS: CONSERVATIVE | CONSUMER_CONTEXT: NONE
- DECOMPOSITION_PATH: R2, 2026-03-26 (SCA-001)

**Extraction Decisions:**
- Pass 1: 3 ANCHOR rows confirmed. No changes.
- Pass 2: 9 prior EXECUTION rows confirmed ACTIVE; LastSeen updated to 2026-03-26.
- 1 new row: DEP-001-07-E10 (R-10 Addendum 4). Addendum 4 Q4 specifies overhead doors must be "folding outward" type that does not impede overhead crane function in open or closed position. This directly changes the door type specification for the two drive-through repair bay overhead doors and the wash bay overhead door in the door schedule. This is a material change to SOW-0025 that was not present in the R1 decomposition.

**Warnings:** None.

### Run: 2026-02-26
- 12 rows extracted. No warnings.

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | R1 (2026-02-25) | None | 12 |
| 2026-03-26 | UPDATE | CONSERVATIVE | R2, SCA-001 (2026-03-26) | None | 13 |

## Lifecycle Summary

### Extraction Lifecycle
- **ACTIVE:** 13 (3 ANCHOR + 10 EXECUTION)
- **RETIRED:** 0

### Closure Lifecycle (SatisfactionStatus breakdown)
- **TBD:** 13
