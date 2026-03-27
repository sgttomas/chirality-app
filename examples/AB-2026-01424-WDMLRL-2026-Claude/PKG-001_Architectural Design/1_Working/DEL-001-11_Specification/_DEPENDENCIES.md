# Dependencies: DEL-001-11 Architectural Specification

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** Dependencies.csv (v3.1 schema)
- **Total rows:** 22
- **ACTIVE:** 22
- **RETIRED:** 0

### ANCHOR Rows (8 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-001-11-A01 | IMPLEMENTS_NODE | SOW-0011 | Complete final architectural design for the addition | HIGH |
| DEP-001-11-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition | HIGH |
| DEP-001-11-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |
| DEP-001-11-A04 | TRACES_TO_REQUIREMENT | SOW-0070 | Renovate 250 sq ft kitchenette area | HIGH |
| DEP-001-11-A05 | TRACES_TO_REQUIREMENT | SOW-0071 | Renovate Old North Shop mezzanine | HIGH |
| DEP-001-11-A06 | TRACES_TO_REQUIREMENT | SOW-0072 | Renovate existing washroom below mezzanine | HIGH |
| DEP-001-11-A07 | TRACES_TO_REQUIREMENT | SOW-0073 | Construct new locker/change room with laundry services | HIGH |
| DEP-001-11-A08 | TRACES_TO_REQUIREMENT | SOW-0074 | Expand washroom facilities to include urinal | HIGH |

### EXECUTION Rows (14 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-001-11-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-01 Preliminary Architectural Design | HIGH |
| DEP-001-11-E02 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-001-02 Architectural Floor Plans (representative of DEL-001-02 through DEL-001-10) | HIGH |
| DEP-001-11-E03 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-12 Structural Specification | HIGH |
| DEP-001-11-E04 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-003-07 Mechanical Specification | HIGH |
| DEP-001-11-E05 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-004-09 Electrical Specification | HIGH |
| DEP-001-11-E06 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-006-08 Plumbing Specification | HIGH |
| DEP-001-11-E07 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-005-07 Civil Specification | HIGH |
| DEP-001-11-E08 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-01 Geotechnical Investigation and Report | HIGH |
| DEP-001-11-E09 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-008-02 Preliminary Site Survey | HIGH |
| DEP-001-11-E10 | UPSTREAM | PREREQUISITE | EXTERNAL | County welding equipment specifications | HIGH |
| DEP-001-11-E11 | UPSTREAM | PREREQUISITE | EXTERNAL | Existing conditions survey -- Old North Shop | HIGH |
| DEP-001-11-E12 | UPSTREAM | CONSTRAINT | DOCUMENT | Alberta Building Code (current edition) | HIGH |
| DEP-001-11-E13 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-09 Old North Shop Demolition Plans | MEDIUM |
| DEP-001-11-E14 | UPSTREAM | PREREQUISITE | DOCUMENT | R-10 Addendum 4 (precast concrete, folding doors, corbel crane, mezzanine railing) | HIGH |

## Run Notes

### Run: 2026-03-26 (R2 refresh)

**Parameters:**
- SCOPE: DEL-001-11_Specification (as part of PKG-001 full refresh)
- MODE: UPDATE | STRICTNESS: CONSERVATIVE | CONSUMER_CONTEXT: NONE
- DECOMPOSITION_PATH: R2, 2026-03-26 (SCA-001)

**Extraction Decisions:**
- Pass 1: 8 ANCHOR rows confirmed. All SOW and OBJ targets unchanged in R2.
- Pass 2: 13 prior EXECUTION rows confirmed ACTIVE; LastSeen updated to 2026-03-26.
- 1 new row: DEP-001-11-E14 (R-10 Addendum 4). Addendum 4 introduces precast concrete walls (exterior and interior, Q5), folding outward overhead doors (Q4), corbel-supported crane on side walls (Q3), max 25-ft crane runway bay spacing (Q2), and mezzanine railing with 10-ft forklift gate and no perimeter walls (Q6). Each of these requires new or modified specification sections covering material standards, performance criteria, installation requirements, and product selection.

**Warnings:** None.

### Run: 2026-02-26
- 21 rows extracted. No warnings.

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | R1 (2026-02-25) | None | 21 |
| 2026-03-26 | UPDATE | CONSERVATIVE | R2, SCA-001 (2026-03-26) | None | 22 |

## Lifecycle Summary

### Extraction Lifecycle
- **ACTIVE:** 22
- **RETIRED:** 0

### Closure Lifecycle (SatisfactionStatus breakdown, ACTIVE rows only)
- **TBD:** 9
- **PENDING:** 13
