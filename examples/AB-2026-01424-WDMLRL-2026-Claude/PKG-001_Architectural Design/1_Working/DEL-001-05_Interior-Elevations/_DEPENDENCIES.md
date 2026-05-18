# Dependencies: DEL-001-05 Interior Elevations

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** Dependencies.csv (v3.1 schema; 19 rows)
- **Last Run:** 2026-03-26
- **ACTIVE rows:** 19 (3 ANCHOR + 16 EXECUTION)
- **RETIRED rows:** 0

### ANCHOR Edges (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-001-05-A01 | IMPLEMENTS_NODE | SOW-0011 | Complete final architectural design for the addition | HIGH |
| DEP-001-05-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition | HIGH |
| DEP-001-05-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |

### EXECUTION Edges (16 ACTIVE)

| DependencyID | Direction | Type | TargetType | Target | Confidence |
|---|---|---|---|---|---|
| DEP-001-05-E01 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-01 Preliminary Architectural Design | HIGH |
| DEP-001-05-E02 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-02 Architectural Floor Plans | HIGH |
| DEP-001-05-E03 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-07 Crane Support Structure Details | HIGH |
| DEP-001-05-E04 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-003-04 Exhaust System Plans | HIGH |
| DEP-001-05-E05 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-006-02 Water Distribution Plans | HIGH |
| DEP-001-05-E06 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-04 Building Sections | HIGH |
| DEP-001-05-E07 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-05 Mezzanine Framing Details | HIGH |
| DEP-001-05-E08 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-06 Service Pit / Trench Structural Details | HIGH |
| DEP-001-05-E09 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-002-08 Steel Plate Embedment Plan | MEDIUM |
| DEP-001-05-E10 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-004-05 Receptacle Layout Plans | MEDIUM |
| DEP-001-05-E11 | DOWNSTREAM | INTERFACE | DELIVERABLE | DEL-001-07 Door & Window Schedule | HIGH |
| DEP-001-05-E12 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-08 Finish Schedule | HIGH |
| DEP-001-05-E13 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-10 Old North Shop Renovation Plans | MEDIUM |
| DEP-001-05-E14 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-001-11 Architectural Specification | MEDIUM |
| DEP-001-05-E15 | UPSTREAM | CONSTRAINT | DOCUMENT | Alberta Safety Codes and applicable building codes | HIGH |
| DEP-001-05-E16 | UPSTREAM | PREREQUISITE | DOCUMENT | R-10 Addendum 4 (interior walls precast concrete, mezzanine railing) | HIGH |

## Run Notes

### Run: 2026-03-26 (R2 refresh)

**Parameters:**
- SCOPE: DEL-001-05_Interior-Elevations (as part of PKG-001 full refresh)
- MODE: UPDATE | STRICTNESS: CONSERVATIVE | CONSUMER_CONTEXT: NONE
- DECOMPOSITION_PATH: R2, 2026-03-26 (SCA-001)

**Extraction Decisions:**
- Pass 1: 3 ANCHOR rows confirmed. No changes.
- Pass 2: 15 prior EXECUTION rows confirmed ACTIVE; LastSeen updated to 2026-03-26.
- 1 new row: DEP-001-05-E16 (R-10 Addendum 4). Interior walls confirmed as precast concrete (Add. 4 Q5) -- directly changes the interior elevation surface material depiction. Mezzanine railing with no perimeter walls and 10-ft forklift gate (Q6) affects mezzanine-adjacent interior elevations.

**Warnings:** None.

### Run: 2026-02-26
- 18 rows extracted. No warnings.

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | R1 (2026-02-25) | None | 18 |
| 2026-03-26 | UPDATE | CONSERVATIVE | R2, SCA-001 (2026-03-26) | None | 19 |

## Lifecycle Summary

- **ACTIVE:** 19 (3 ANCHOR + 16 EXECUTION)
- **RETIRED:** 0

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 19 |
