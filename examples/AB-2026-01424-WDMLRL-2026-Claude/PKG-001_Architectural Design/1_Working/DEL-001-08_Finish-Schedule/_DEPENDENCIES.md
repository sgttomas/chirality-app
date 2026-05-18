# Dependencies: DEL-001-08 Finish Schedule

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** `Dependencies.csv` (v3.1 schema)
- **Total ACTIVE rows:** 13
- **ANCHOR rows:** 3
- **EXECUTION rows:** 10

### ANCHOR Edges (Tree -- Definition Traceability)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-001-08-A01 | IMPLEMENTS_NODE | SOW-0011 | Complete final architectural design for the addition | HIGH |
| DEP-001-08-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition | HIGH |
| DEP-001-08-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation across all disciplines | HIGH |

### EXECUTION Edges (DAG -- Information Flow)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-001-08-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-01 Preliminary Architectural Design | HIGH |
| DEP-001-08-E02 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-02 Architectural Floor Plans | HIGH |
| DEP-001-08-E03 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-05 Interior Elevations | HIGH |
| DEP-001-08-E04 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-06 Reflected Ceiling Plans | HIGH |
| DEP-001-08-E05 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-11 Architectural Specification | HIGH |
| DEP-001-08-E06 | UPSTREAM | INTERFACE | PACKAGE | PKG-002 Structural Design | HIGH |
| DEP-001-08-E07 | UPSTREAM | INTERFACE | PACKAGE | PKG-006 Plumbing Design | HIGH |
| DEP-001-08-E08 | UPSTREAM | CONSTRAINT | DOCUMENT | Alberta Building Code | HIGH |
| DEP-001-08-E09 | UPSTREAM | PREREQUISITE | UNKNOWN | Site Investigation Results (Old North Shop) | HIGH |
| DEP-001-08-E10 | UPSTREAM | PREREQUISITE | DOCUMENT | R-10 Addendum 4 (interior walls precast concrete, mezzanine railing) | HIGH |

## Run Notes

### Run: 2026-03-26 (R2 refresh)

**Parameters:**
- SCOPE: DEL-001-08_Finish-Schedule (as part of PKG-001 full refresh)
- MODE: UPDATE | STRICTNESS: CONSERVATIVE | CONSUMER_CONTEXT: NONE
- DECOMPOSITION_PATH: R2, 2026-03-26 (SCA-001)

**Extraction Decisions:**
- Pass 1: 3 ANCHOR rows confirmed. No changes.
- Pass 2: 9 prior EXECUTION rows confirmed ACTIVE; LastSeen updated to 2026-03-26.
- 1 new row: DEP-001-08-E10 (R-10 Addendum 4). Interior walls confirmed as precast concrete (Add. 4 Q5) -- this directly affects interior finish material selections. Precast concrete walls may require different finish treatments (sealant, paint on concrete) than framed walls. Mezzanine railing with no perimeter walls (Q6) eliminates mezzanine wall finish entries from the schedule.

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

### Closure Lifecycle (SatisfactionStatus breakdown -- ACTIVE rows only)
- **TBD:** 7
- **PENDING:** 6
