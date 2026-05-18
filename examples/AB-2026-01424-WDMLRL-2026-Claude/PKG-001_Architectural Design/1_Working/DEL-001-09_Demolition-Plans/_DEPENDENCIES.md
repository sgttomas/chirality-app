# Dependencies: DEL-001-09 Old North Shop Demolition Plans

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** `Dependencies.csv` (v3.1, 15 rows, 15 ACTIVE / 0 RETIRED)
- **Summary:** 3 ANCHOR + 12 EXECUTION edges.

### ANCHOR Edges (3 ACTIVE)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-001-09-A01 | IMPLEMENTS_NODE | SOW-0070; SOW-0071; SOW-0072 | Renovate Old North Shop (kitchenette, mezzanine, washroom) | HIGH |
| DEP-001-09-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition and associated renovations | HIGH |
| DEP-001-09-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation across all disciplines | HIGH |

### EXECUTION Edges -- UPSTREAM (7 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetName | Confidence |
|---|---|---|---|---|
| DEP-001-09-E01 | PREREQUISITE | DELIVERABLE | DEL-001-01 Preliminary Architectural Design | HIGH |
| DEP-001-09-E03 | PREREQUISITE | EXTERNAL | Old North Shop Field Survey Data | HIGH |
| DEP-001-09-E04 | PREREQUISITE | EXTERNAL | Old North Shop Existing As-Built Drawings | MEDIUM |
| DEP-001-09-E05 | INTERFACE | PACKAGE | PKG-002 Structural Engineering -- Mezzanine Coordination | HIGH |
| DEP-001-09-E06 | INTERFACE | PACKAGE | PKG-003/004/006 MEP Disciplines -- Demolition Scope Split | HIGH |
| DEP-001-09-E07 | CONSTRAINT | EXTERNAL | Hazardous Materials Assessment | HIGH |
| DEP-001-09-E08 | PREREQUISITE | DOCUMENT | R-04 Appendix B -- Shop Conceptual Floor Plan | HIGH |

### EXECUTION Edges -- DOWNSTREAM (5 ACTIVE)

| DependencyID | DependencyType | TargetType | TargetName | Confidence |
|---|---|---|---|---|
| DEP-001-09-E02 | HANDOVER | DELIVERABLE | DEL-001-10 Old North Shop Renovation Plans | HIGH |
| DEP-001-09-E09 | HANDOVER | DELIVERABLE | DEL-017-01 Kitchenette Renovation | HIGH |
| DEP-001-09-E10 | HANDOVER | DELIVERABLE | DEL-017-02 Old North Shop Mezzanine Renovation | HIGH |
| DEP-001-09-E11 | HANDOVER | DELIVERABLE | DEL-017-03 Washroom Renovation & Expansion | HIGH |
| DEP-001-09-E12 | ENABLES | DELIVERABLE | DEL-009-02 Building Permit Application & Approval | HIGH |

---

## Run Notes

### Run: 2026-03-26 (R2 refresh)

**Parameters:**
- SCOPE: DEL-001-09_Demolition-Plans (as part of PKG-001 full refresh)
- MODE: UPDATE | STRICTNESS: CONSERVATIVE | CONSUMER_CONTEXT: NONE
- DECOMPOSITION_PATH: R2, 2026-03-26 (SCA-001)

**Extraction Decisions:**
- Pass 1: 3 ANCHOR rows confirmed. No changes. SOW-0070, SOW-0071, SOW-0072 unchanged in R2 decomposition.
- Pass 2: 12 prior EXECUTION rows confirmed ACTIVE; LastSeen updated to 2026-03-26.
- No new rows added. R2 changes (precast concrete walls, folding outward doors, mezzanine railing) apply to the new addition, not to the Old North Shop demolition scope. Demolition plans address the existing building interior, which is unaffected by these addenda.

**Warnings:** None.

### Run: 2026-02-26
- 15 rows extracted. No warnings.

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | R1 (2026-02-25) | None | 15 |
| 2026-03-26 | UPDATE | CONSERVATIVE | R2, SCA-001 (2026-03-26) | None | 15 |

---

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 15 |
| RETIRED | 0 |

### Closure State Breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 14 |
| SATISFIED | 1 |

**Note:** DEP-001-09-E08 (R-04 Appendix B) is marked SATISFIED because the document is confirmed available.
