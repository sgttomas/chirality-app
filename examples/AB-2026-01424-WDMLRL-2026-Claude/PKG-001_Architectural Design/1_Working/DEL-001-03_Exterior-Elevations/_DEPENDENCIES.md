# Dependencies: DEL-001-03 Exterior Elevations

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

---

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** `Dependencies.csv` (v3.1 schema, 23 rows)
- **RegisterSchemaVersion:** v3.1

### Summary

| Category | Count |
|---|---|
| Total rows | 23 |
| ACTIVE | 23 |
| RETIRED | 0 |
| ANCHOR rows | 3 |
| EXECUTION rows | 20 |

### ANCHOR Register (3 rows)

| DependencyID | AnchorType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|
| DEP-001-03-A01 | IMPLEMENTS_NODE | SOW-0011 | Complete final architectural design for the addition | HIGH |
| DEP-001-03-A02 | TRACES_TO_REQUIREMENT | OBJ-001 | Deliver a code-compliant, fully functional maintenance shop addition | HIGH |
| DEP-001-03-A03 | TRACES_TO_REQUIREMENT | OBJ-003 | Produce complete P.Eng.-stamped IFC design documentation across all disciplines | HIGH |

### EXECUTION Register (20 rows)

| DependencyID | Direction | DependencyType | TargetDeliverableID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-001-03-E01 | UPSTREAM | PREREQUISITE | DEL-001-01 | Preliminary Architectural Design | HIGH |
| DEP-001-03-E02 | UPSTREAM | INTERFACE | DEL-001-02 | Architectural Floor Plans | HIGH |
| DEP-001-03-E03 | UPSTREAM | INTERFACE | DEL-001-04 | Building Sections | HIGH |
| DEP-001-03-E04 | UPSTREAM | INTERFACE | DEL-001-07 | Door & Window Schedule | HIGH |
| DEP-001-03-E05 | UPSTREAM | INTERFACE | DEL-001-08 | Finish Schedule | HIGH |
| DEP-001-03-E06 | UPSTREAM | INTERFACE | DEL-002-03 | Structural Framing Plans | HIGH |
| DEP-001-03-E07 | UPSTREAM | INTERFACE | DEL-002-04 | Structural Sections & Details | HIGH |
| DEP-001-03-E08 | UPSTREAM | INTERFACE | DEL-002-07 | Crane Support Structure Details | HIGH |
| DEP-001-03-E09 | UPSTREAM | INTERFACE | DEL-003-04 | Exhaust System Plans | HIGH |
| DEP-001-03-E10 | UPSTREAM | INTERFACE | DEL-005-02 | Site Grading Plan | HIGH |
| DEP-001-03-E11 | UPSTREAM | INTERFACE | DEL-006-03 | Drain & Vent Plans | HIGH |
| DEP-001-03-E12 | UPSTREAM | INTERFACE | DEL-008-01 | Geotechnical Investigation & Report | MEDIUM |
| DEP-001-03-E13 | UPSTREAM | INTERFACE | DEL-001-09 | Demolition Plans | HIGH |
| DEP-001-03-E14 | UPSTREAM | INTERFACE | DEL-001-10 | Renovation Plans | HIGH |
| DEP-001-03-E15 | UPSTREAM | PREREQUISITE | DEL-005-01 | Preliminary Civil Design | MEDIUM |
| DEP-001-03-E16 | DOWNSTREAM | HANDOVER | DEL-009-02 | Building Permit Application & Approval | HIGH |
| DEP-001-03-E17 | DOWNSTREAM | INTERFACE | DEL-009-04 | Code Compliance Register & Inspection Log | MEDIUM |
| DEP-001-03-E18 | UPSTREAM | INTERFACE | DEL-004-02 | Single-Line Diagram | MEDIUM |
| DEP-001-03-E19 | DOWNSTREAM | HANDOVER | DEL-001-05 | Interior Elevations | HIGH |
| DEP-001-03-E20 | UPSTREAM | PREREQUISITE | R-10 | Addendum 4 (precast concrete walls, folding outward overhead doors) | HIGH |

---

## Run Notes

### Run: 2026-03-26 (R2 refresh)

**Parameters:**
- SCOPE: DEL-001-03_Exterior-Elevations (as part of PKG-001 full refresh)
- MODE: UPDATE | STRICTNESS: CONSERVATIVE | CONSUMER_CONTEXT: NONE
- DECOMPOSITION_PATH: `_Decomposition/WDMLRL_Decomposition_Claude.md` (R2, 2026-03-26, SCA-001)
- ANCHOR_DOC: Datasheet.md | EXECUTION_DOC_ORDER: Specification.md, Procedure.md, Guidance.md

**Extraction Decisions:**
- Pass 1 (ANCHOR): 3 rows carried forward. All confirmed against R2 decomposition. No changes.
- Pass 2 (EXECUTION): 19 prior rows confirmed ACTIVE; LastSeen updated to 2026-03-26.
- 1 new row: DEP-001-03-E20 (R-10 Addendum 4). Precast concrete walls (Add. 2 + Add. 4) directly change exterior elevation material depiction. Folding outward overhead doors (Add. 4 Q4) change door representation on all elevation faces showing overhead doors.

**Warnings:** None.

### Run: 2026-02-26

- MODE: UPDATE | STRICTNESS: CONSERVATIVE | CONSUMER_CONTEXT: TASK_ESTIMATING
- 22 rows extracted. No warnings.

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-26 | UPDATE | CONSERVATIVE | R1 (2026-02-25) | None | 22 |
| 2026-03-26 | UPDATE | CONSERVATIVE | R2, SCA-001 (2026-03-26) | None | 23 |

---

## Lifecycle Summary

### Extraction Lifecycle
| Status | Count |
|---|---|
| ACTIVE | 23 |
| RETIRED | 0 |

### Closure Lifecycle (SatisfactionStatus)
| Status | Count |
|---|---|
| TBD | 22 |
| PENDING | 1 |
