# Dependencies: DEL-001-10 Old North Shop Renovation Plans

## Coordination (human-owned)
- **Mode:** TRACKED
- **Notes:** Dependency register extracted by DEPENDENCIES agent. Coordination representation confirmed via extraction from source documents.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

---

## Extracted Dependency Register

**Status:** POPULATED
**Dependencies.csv:** 18 rows (18 ACTIVE, 0 RETIRED)
**Schema Version:** v3.1

### ANCHOR Dependencies (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-001-10-A01 | IMPLEMENTS_NODE | SOW-0070, SOW-0071, SOW-0072, SOW-0073, SOW-0074 | Renovate Old North Shop (all renovation scope) | HIGH |
| DEP-001-10-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition | HIGH |
| DEP-001-10-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation | HIGH |

### EXECUTION Dependencies -- UPSTREAM (12 ACTIVE)

| DependencyID | Type | TargetType | Target | Confidence |
|---|---|---|---|---|
| DEP-001-10-E01 | CONSTRAINT | DELIVERABLE | DEL-001-01 Preliminary Architectural Design | HIGH |
| DEP-001-10-E02 | PREREQUISITE | DELIVERABLE | DEL-001-09 Old North Shop Demolition Plans | HIGH |
| DEP-001-10-E03 | INTERFACE | DELIVERABLE | DEL-001-02 Architectural Floor Plans | MEDIUM |
| DEP-001-10-E06 | INTERFACE | DELIVERABLE | DEL-001-11 Architectural Specification | HIGH |
| DEP-001-10-E07 | INTERFACE | PACKAGE | PKG-002 Structural Design | HIGH |
| DEP-001-10-E08 | INTERFACE | PACKAGE | PKG-006 Plumbing Design | HIGH |
| DEP-001-10-E09 | INTERFACE | PACKAGE | PKG-003 Mechanical Design | MEDIUM |
| DEP-001-10-E10 | INTERFACE | PACKAGE | PKG-004 Electrical Design | HIGH |
| DEP-001-10-E12 | PREREQUISITE | EXTERNAL | Existing Conditions Field Survey | HIGH |
| DEP-001-10-E13 | CONSTRAINT | EXTERNAL | County Preliminary Design Approval | HIGH |
| DEP-001-10-E14 | CONSTRAINT | EXTERNAL | Alberta Building Code Edition Confirmation from AHJ | MEDIUM |
| DEP-001-10-E15 | PREREQUISITE | EXTERNAL | Mandatory Site Meeting Attendance | HIGH |

### EXECUTION Dependencies -- DOWNSTREAM (3 ACTIVE)

| DependencyID | Type | TargetType | Target | Confidence |
|---|---|---|---|---|
| DEP-001-10-E04 | HANDOVER | DELIVERABLE | DEL-001-07 Door & Window Schedule | HIGH |
| DEP-001-10-E05 | HANDOVER | DELIVERABLE | DEL-001-08 Finish Schedule | HIGH |
| DEP-001-10-E11 | HANDOVER | PACKAGE | PKG-017 Existing Building Renovation | HIGH |

---

## Run Notes

### Run: 2026-03-26 (R2 refresh)

**Parameters:**
- SCOPE: DEL-001-10_Renovation-Plans (as part of PKG-001 full refresh)
- MODE: UPDATE | STRICTNESS: CONSERVATIVE | CONSUMER_CONTEXT: NONE
- DECOMPOSITION_PATH: R2, 2026-03-26 (SCA-001)

**Extraction Decisions:**
- Pass 1: 3 ANCHOR rows confirmed. SOW-0070 through SOW-0074 unchanged in R2.
- Pass 2: 15 prior EXECUTION rows confirmed ACTIVE; LastSeen updated to 2026-03-26.
- No new rows added. R2 changes (precast concrete walls, folding outward doors, mezzanine railing) apply to the new addition, not to the Old North Shop renovation scope.

**Warnings:** None.

### Run: 2026-02-26
- 18 rows extracted. No warnings.

## Run History

| Run Date | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | R1 (2026-02-25) | None | 18 |
| 2026-03-26 | UPDATE | CONSERVATIVE | R2, SCA-001 (2026-03-26) | None | 18 |

---

## Lifecycle Summary

| Metric | Count |
|---|---|
| Total rows | 18 |
| ACTIVE | 18 |
| RETIRED | 0 |

### SatisfactionStatus Breakdown (ACTIVE rows)

| Status | Count |
|---|---|
| TBD | 3 |
| PENDING | 15 |
