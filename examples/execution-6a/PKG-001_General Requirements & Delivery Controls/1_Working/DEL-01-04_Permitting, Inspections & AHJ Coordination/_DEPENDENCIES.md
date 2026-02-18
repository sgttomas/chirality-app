# Dependencies: DEL-01-04 Permitting, Inspections & AHJ Coordination

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** `Dependencies.csv` (this folder)
- **RegisterSchemaVersion:** v3.1
- **Total rows:** 10 (ACTIVE: 10, RETIRED: 0)
- **ANCHOR rows (ACTIVE):** 3
- **EXECUTION rows (ACTIVE):** 7

### ANCHOR Edges (Tree -- Definition Traceability)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence | Notes |
|---|---|---|---|---|---|---|
| DEP-01-04-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0009 | SOW-0009 | HIGH | Parent scope item. Confirmed in decomposition. |
| DEP-01-04-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-008 | OBJ-008 | HIGH | Safe controlled DB delivery objective. Confirmed in decomposition. |
| DEP-01-04-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-005 | OBJ-005 | MEDIUM | Site/civil works objective. ASSUMPTION: best-effort package heuristic. |

### EXECUTION Edges (DAG -- Information Flow)

| DependencyID | Direction | DependencyType | TargetType | Target | Statement (summary) | Confidence |
|---|---|---|---|---|---|---|
| DEP-01-04-004 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-02 (Baseline Schedule) | Gantt schedule required to align inspection hold-points with construction milestones | HIGH |
| DEP-01-04-005 | UPSTREAM | PREREQUISITE | DELIVERABLE | DEL-01-01 (Design Management) | Conceptual design required to identify building systems and permit categories | HIGH |
| DEP-01-04-006 | UPSTREAM | CONSTRAINT | DOCUMENT | Alberta Building Code | Required to verify design compliance prior to permit submission | HIGH |
| DEP-01-04-007 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-03 (H&S Plan) | Cross-reference of inspection findings between AHJ/code regime and OHS regime | HIGH |
| DEP-01-04-008 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-04 (Site Utilities) | Utility connection coordination and permit/approval interface | MEDIUM |
| DEP-01-04-009 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-07 (Commissioning/Closeout) | Occupancy permit and SP conformance letters are required inputs for Substantial Performance package | HIGH |
| DEP-01-04-010 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-05 (Environmental/Flood Hazard) | AEP environmental approval determination depends on flood/water constraint analysis | MEDIUM |

## Run Notes

### Run: 2026-02-17

**Run parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: AUTO

**Resolved paths and defaults:**
- ANCHOR_DOC: `Datasheet.md` (AUTO resolved; contains identification/traceability fields with SOW/OBJ references)
- EXECUTION_DOC_ORDER: `Procedure.md`, `Guidance.md`, `Specification.md` (AUTO resolved)
- DECOMPOSITION_PATH: `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` (available; used for validation)
- _REFERENCES.md: present; used for document target resolution

**Decomposition validation:** Available. All anchors validated against decomposition scope ledger and objectives table. SOW-0009 confirmed mapped to DEL-01-04 under PKG-001. OBJ-008 and OBJ-005 confirmed as supported objectives.

**Warnings:** None.

**Assumptions logged:**
- DEP-01-04-003 (OBJ-005 trace): Datasheet notes ASSUMPTION for best-effort package heuristic mapping; confidence set to MEDIUM.
- DEP-01-04-008 (DEL-03-04 interface): Utility tie-in cost is a cash allowance (SOW-0110) managed by DEL-03-04; DEL-01-04 manages permits/approvals for utility connections. Direction set UPSTREAM because DEL-01-04 needs utility design information from DEL-03-04 to obtain utility permits. Confidence MEDIUM due to bidirectional nature.
- DEP-01-04-010 (DEL-03-05 interface): AEP environmental approval trigger is TBD (Lensing item C-001). Whether AEP approval is a permit requirement depends on flood/water constraint analysis managed by DEL-03-05. Confidence MEDIUM.

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ANCHOR (ACTIVE) | EXECUTION (ACTIVE) | RETIRED | Total |
|---|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Available (v1.0 Phase 7) | None | 3 | 7 | 0 | 10 |

## Lifecycle Summary

**Extraction lifecycle:**
- ACTIVE: 10
- RETIRED: 0

**Closure lifecycle (SatisfactionStatus):**
- TBD: 10
- PENDING: 0
- IN_PROGRESS: 0
- SATISFIED: 0
- WAIVED: 0
- NOT_APPLICABLE: 0

**Tree integrity:**
- Parent anchor (IMPLEMENTS_NODE): 1 -- PASS
- No warnings.
