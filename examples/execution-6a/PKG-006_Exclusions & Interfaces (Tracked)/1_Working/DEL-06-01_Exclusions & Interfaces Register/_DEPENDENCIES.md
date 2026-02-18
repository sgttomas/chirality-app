# Dependencies: DEL-06-01 Exclusions & Interfaces Register

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register (populated by DEPENDENCIES agent)
- **Status:** COMPLETED
- **Dependencies.csv:** `Dependencies.csv` (8 rows)
- **Summary:** 2 ANCHOR + 6 EXECUTION = 8 total ACTIVE rows

### ANCHOR Edges (Tree linkage)

| DependencyID | AnchorType | TargetType | TargetRefID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-06-01-001 | IMPLEMENTS_NODE | WBS_NODE | SOW-0400 | SOW-0400 -- Pickled sand/salt storage (OUT) | HIGH |
| DEP-06-01-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | OBJ-008 | OBJ-008 -- Safe controlled DB delivery incl. change management | HIGH |

### EXECUTION Edges (DAG / information flow)

| DependencyID | Direction | DependencyType | TargetType | Target | Statement (abbreviated) | Confidence |
|---|---|---|---|---|---|---|
| DEP-06-01-003 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-01 (Site Plan, Circulation, Parking) | Site plan concept required to identify spatial interfaces | HIGH |
| DEP-06-01-004 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-01 (Integrated Design Management) | Design coordination matrix required to cross-reference interfaces | HIGH |
| DEP-06-01-005 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-01-05 (Meetings, Documentation & Change Control) | Change management process required for register integration | HIGH |
| DEP-06-01-006 | UPSTREAM | PREREQUISITE | DOCUMENT | Addendum 03 s1.2 | Governing authority for SOW-0400 exclusion | HIGH |
| DEP-06-01-007 | UPSTREAM | INTERFACE | DELIVERABLE | DEL-03-05 (Environmental Constraints, Flood Hazard) | Flood hazard constraints interface tracked in DEL-03-05 | MEDIUM |
| DEP-06-01-008 | DOWNSTREAM | HANDOVER | DELIVERABLE | DEL-01-07 (Commissioning, Training, Closeout & Warranty) | Final register included in closeout documentation package | HIGH |

## Run Notes

### Run: 2026-02-17 (initial extraction)

**Parameters:**
- MODE: UPDATE
- STRICTNESS: CONSERVATIVE
- CONSUMER_CONTEXT: NONE
- SOURCE_DOCS: AUTO (resolved to Datasheet.md, Guidance.md, Procedure.md, Specification.md)
- ANCHOR_DOC: AUTO (resolved to Datasheet.md -- contains Scope Coverage and Objective Support fields)
- EXECUTION_DOC_ORDER: AUTO (resolved to Procedure.md, Guidance.md, Specification.md)
- Decomposition: FOUND at `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md`

**Defaults applied:**
- ANCHOR_DOC selected as Datasheet.md based on presence of identification fields (Deliverable ID, Scope Coverage, Objective Support).
- EXECUTION_DOC_ORDER prioritized Procedure.md (workflow/prerequisites), then Guidance.md (considerations/functional inputs), then Specification.md (requirements/standards).
- _REFERENCES.md was read; no additional dependency rows were emitted solely from reference listings.

**Assumptions:**
- NONE. All extracted rows are evidence-based (FACT) per CONSERVATIVE strictness.

**Warnings:**
- NONE. Parent anchor check: exactly 1 IMPLEMENTS_NODE found. No integrity warnings.

**Extraction notes:**
- Pass 1 (ANCHOR): Datasheet.md "Scope Coverage: SOW-0400" and "Objective Support: OBJ-008" yielded 2 ANCHOR rows. Both validated against decomposition scope ledger and deliverable table.
- Pass 2 (EXECUTION): Procedure.md "Upstream Dependencies" table yielded 3 deliverable interfaces (DEL-03-01, DEL-01-01, DEL-01-05) + 1 document prerequisite (Addendum 03). Guidance.md C3 yielded 1 deliverable interface (DEL-03-05). Procedure.md Step D2 yielded 1 downstream handover (DEL-01-07). Total: 6 EXECUTION rows.
- Guidance.md X-002 "Upstream Dependencies and Functional Inputs" section reinforced the same 3 deliverable interfaces found in Procedure.md; no new targets identified.
- Specification.md REQ-06-01-007 and REQ-06-01-008 reinforced existing ANCHOR (OBJ-008) and EXECUTION (DEL-01-01) edges; no new targets.

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ANCHOR Active | EXECUTION Active | Total Active |
|---|---|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | FOUND (v1.0 PHASE7) | NONE | 2 | 6 | 8 |

## Lifecycle Summary

### Extraction Lifecycle
- **ACTIVE:** 8
- **RETIRED:** 0

### Closure Lifecycle (SatisfactionStatus breakdown -- ACTIVE rows only)
- **TBD:** 8
- **PENDING:** 0
- **IN_PROGRESS:** 0
- **SATISFIED:** 0
- **WAIVED:** 0
- **NOT_APPLICABLE:** 0

### By DependencyClass
- **ANCHOR:** 2 ACTIVE (1 IMPLEMENTS_NODE, 1 TRACES_TO_REQUIREMENT)
- **EXECUTION:** 6 ACTIVE (4 INTERFACE, 1 PREREQUISITE, 1 HANDOVER)

### By Direction
- **UPSTREAM:** 7
- **DOWNSTREAM:** 1
