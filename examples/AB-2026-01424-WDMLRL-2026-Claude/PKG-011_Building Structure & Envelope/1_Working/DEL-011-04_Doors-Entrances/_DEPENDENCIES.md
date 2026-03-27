# Dependencies: DEL-011-04 Entrance/Exit Doors

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- DEL-011-01 Superstructure -- Structural openings must be framed and ready
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- PKG-012 Interior Construction & Fit-Out -- Interior access depends on operational doors
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** Dependencies.csv (7 rows, 7 ACTIVE, 0 RETIRED)
- **Schema Version:** v3.1

### ANCHOR Edges (2 ACTIVE)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-011-04-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0026 | HIGH |
| DEP-011-04-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-001 | HIGH |

### EXECUTION Edges (5 ACTIVE)

| DependencyID | Direction | DependencyType | TargetType | Target | Confidence | EstimateImpact |
|---|---|---|---|---|---|---|
| DEP-011-04-003 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-07 Door & Window Schedule | HIGH | BLOCKING |
| DEP-011-04-004 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-001-11 Architectural Specification | HIGH | BLOCKING |
| DEP-011-04-005 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-011-01 Concrete Superstructure | HIGH | BLOCKING |
| DEP-011-04-006 | DOWNSTREAM | ENABLES | PACKAGE | PKG-012 Interior Construction & Fit-Out | HIGH | ADVISORY |
| DEP-011-04-007 | UPSTREAM | INTERFACE | PACKAGE | PKG-015 Electrical & Low-Voltage Installation | MEDIUM | ADVISORY |

## Run Notes

### Run 2026-02-26 (Initial Extraction)

**Mode:** UPDATE | **Strictness:** CONSERVATIVE | **Consumer Context:** TASK_ESTIMATING
**Decomposition Path:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (R1, 2026-02-25) -- located and validated.
**Source Documents:** ANCHOR_DOC: Datasheet.md; EXECUTION_DOCS: Procedure.md, Guidance.md, Specification.md
**Warnings:** None.

### Run 2026-03-26 (SCA-001 Refresh)

**Mode:** UPDATE | **Strictness:** CONSERVATIVE | **Consumer Context:** NONE
**Decomposition Path:** `_Decomposition/WDMLRL_Decomposition_Claude.md` (R2 -- 2026-03-26, SCA-001)

**SCA-001 Changes Affecting This Deliverable:**
- SOW-0026 text unchanged in decomposition ("Install separate entrance/exit doors for the addition"). No addendum changes directly affect entrance/exit door scope.
- Note: The _CONTEXT.md for DEL-011-04 mentions "folding outward type per Addendum 4, Q4" but this pertains to overhead repair bay doors (SOW-0025 / DEL-011-03), not entrance/exit pedestrian doors (SOW-0026). No dependency changes warranted.

**Changes Applied:**
- Updated LastSeen to 2026-03-26 on all 7 ACTIVE rows.
- No new rows added. No rows retired. No statement changes.

**Warnings:** None.

## Run History

| Run | Date | Mode | Strictness | Decomp Status | Warnings | ACTIVE Anchors | ACTIVE Execution | Total ACTIVE |
|---|---|---|---|---|---|---|---|---|
| 1 | 2026-02-26 | UPDATE | CONSERVATIVE | Located (R1 2026-02-25) | None | 2 | 5 | 7 |
| 2 | 2026-03-26 | UPDATE | CONSERVATIVE | Located (R2 2026-03-26 SCA-001) | None | 2 | 5 | 7 |

## Lifecycle Summary

| Status | Count |
|---|---|
| ACTIVE | 7 |
| RETIRED | 0 |

| SatisfactionStatus | Count |
|---|---|
| NOT_APPLICABLE | 2 |
| PENDING | 4 |
| TBD | 1 |
