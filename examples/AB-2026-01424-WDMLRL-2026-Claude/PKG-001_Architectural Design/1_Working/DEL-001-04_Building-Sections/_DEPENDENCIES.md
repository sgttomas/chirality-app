# Dependencies: DEL-001-04 Building Sections

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** 14 rows (3 ANCHOR, 11 EXECUTION; 14 ACTIVE, 0 RETIRED)
- **RegisterSchemaVersion:** v3.1

### ANCHOR Edges (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-001-04-A01 | IMPLEMENTS_NODE | SOW-0011 | Complete final architectural design for the addition | HIGH |
| DEP-001-04-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition | HIGH |
| DEP-001-04-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation across all disciplines | HIGH |

### EXECUTION Edges (11 ACTIVE)

| DependencyID | Direction | DependencyType | TargetDeliverableID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-001-04-E01 | UPSTREAM | PREREQUISITE | DEL-001-01 | Preliminary Architectural Design | HIGH |
| DEP-001-04-E02 | UPSTREAM | INTERFACE | DEL-002-04 | Structural Sections & Details | HIGH |
| DEP-001-04-E03 | UPSTREAM | PREREQUISITE | DEL-002-06 | Service Pit / Trench Structural Details | HIGH |
| DEP-001-04-E04 | UPSTREAM | INTERFACE | DEL-003-02 | HVAC Layout Plans | HIGH |
| DEP-001-04-E05 | UPSTREAM | PREREQUISITE | DEL-001-02 | Architectural Floor Plans | HIGH |
| DEP-001-04-E06 | UPSTREAM | PREREQUISITE | DEL-002-05 | Mezzanine Framing Details | HIGH |
| DEP-001-04-E07 | UPSTREAM | PREREQUISITE | DEL-002-07 | Crane Support Structure Details | HIGH |
| DEP-001-04-E08 | UPSTREAM | PREREQUISITE | DEL-008-01 | Geotechnical Investigation & Report | HIGH |
| DEP-001-04-E09 | UPSTREAM | INTERFACE | DEL-004-04 | Lighting Plans | MEDIUM |
| DEP-001-04-E10 | UPSTREAM | INTERFACE | DEL-001-11 | Architectural Specification | HIGH |
| DEP-001-04-E11 | UPSTREAM | PREREQUISITE | R-10 | Addendum 4 (precast walls, corbel crane, mezzanine railing) | HIGH |

---

## Run Notes

### Run: 2026-03-26 (R2 refresh)

**Parameters:**
- SCOPE: DEL-001-04_Building-Sections (as part of PKG-001 full refresh)
- MODE: UPDATE | STRICTNESS: CONSERVATIVE | CONSUMER_CONTEXT: NONE
- DECOMPOSITION_PATH: R2, 2026-03-26 (SCA-001)

**Extraction Decisions:**
- Pass 1: 3 ANCHOR rows confirmed. No changes.
- Pass 2: 10 prior EXECUTION rows confirmed ACTIVE; LastSeen updated to 2026-03-26.
- 1 new row: DEP-001-04-E11 (R-10 Addendum 4). Precast concrete wall assemblies, corbel-supported crane details (Q3), mezzanine railing with no perimeter walls and 10-ft forklift gate (Q6), and max 25-ft crane runway bay spacing (Q2) all directly affect building section content.

**Warnings:** None.

### Run: 2026-02-26

- MODE: UPDATE | STRICTNESS: CONSERVATIVE | CONSUMER_CONTEXT: TASK_ESTIMATING
- 13 rows extracted. No warnings.

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | R1 (2026-02-25) | None | 13 |
| 2026-03-26 | UPDATE | CONSERVATIVE | R2, SCA-001 (2026-03-26) | None | 14 |

---

## Lifecycle Summary

| Category | Count |
|---|---|
| Total rows | 14 |
| ACTIVE | 14 |
| RETIRED | 0 |

### Closure-State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 8 |
| PENDING | 6 |
