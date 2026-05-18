# Dependencies: DEL-01-06 Site Supervision, Logistics & Housekeeping

## Coordination (human-owned)
- **Mode:** DECLARED
- **Notes:** See _Coordination/_COORDINATION.md for project-level coordination record.

## Upstream (I need these before I can proceed) -- human-owned declarations
- No upstream dependencies declared yet.

## Downstream (These need me) -- human-owned declarations
- No downstream dependencies declared yet.

## Extracted Dependency Register

- **Status:** POPULATED
- **Dependencies.csv:** `Dependencies.csv` (8 rows; 8 ACTIVE, 0 RETIRED)
- **Schema Version:** v3.1
- **Summary:** 4 ANCHOR rows (1 IMPLEMENTS_NODE, 3 TRACES_TO_REQUIREMENT) + 4 EXECUTION rows (2 PREREQUISITE, 1 INTERFACE, 1 HANDOVER)

### ANCHOR Edges (Tree -- vertical traceability)

| DependencyID | AnchorType | TargetType | TargetRefID / TargetName | Confidence |
|---|---|---|---|---|
| DEP-0106-001 | IMPLEMENTS_NODE | WBS_NODE | DEL-01-06_Site-Supervision-and-Logistics node in PKG-001 | HIGH |
| DEP-0106-002 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0010 | HIGH |
| DEP-0106-003 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0111 | HIGH |
| DEP-0106-004 | TRACES_TO_REQUIREMENT | REQUIREMENT | SOW-0112 | HIGH |

### EXECUTION Edges (DAG -- information flow)

| DependencyID | Direction | DependencyType | TargetDeliverableID | TargetName | Confidence |
|---|---|---|---|---|---|
| DEP-0106-005 | UPSTREAM | PREREQUISITE | DEL-01-02 | Baseline Schedule, Updates & Reporting | HIGH |
| DEP-0106-006 | UPSTREAM | PREREQUISITE | DEL-03-01 | Site Plan, Circulation, Parking & Operational Layout | HIGH |
| DEP-0106-007 | UPSTREAM | INTERFACE | DEL-01-03 | Health & Safety (Prime Contractor) Plan | HIGH |
| DEP-0106-008 | DOWNSTREAM | HANDOVER | DEL-01-07 | Commissioning, Training, Closeout & Warranty | HIGH |

## Run Notes

- **Run date:** 2026-02-17
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** NONE
- **SOURCE_DOCS:** AUTO (resolved to: Datasheet.md, Guidance.md, Procedure.md, Specification.md)
- **ANCHOR_DOC:** AUTO (resolved to: Datasheet.md -- contains `datasheet` keyword; highest-confidence anchor candidate)
- **EXECUTION_DOC_ORDER:** AUTO (resolved to: Procedure.md, Guidance.md, Specification.md -- Procedure contains `procedure` keyword, highest workflow clarity)
- **DECOMPOSITION_PATH:** `_Decomposition/Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md` (found and used for validation)
- **_REFERENCES.md:** Read; contains pointer to RFP 2024_004 in _Sources/. No additional document targets resolved from references.

### Defaults and assumptions applied
- ANCHOR_DOC selected by heuristic: Datasheet.md (contains explicit deliverable identification, scope item coverage, and objective mapping).
- EXECUTION_DOC_ORDER selected by heuristic: Procedure.md first (richest prerequisite/workflow signal), then Guidance.md (considerations/interfaces), then Specification.md (requirements/out-of-scope boundaries).
- All anchor identifiers validated against decomposition Phase 5 deliverable table and Phase 6 scope ledger.
- Deliverable target IDs resolved against decomposition (DEL-01-02, DEL-01-03, DEL-01-07, DEL-03-01 all confirmed present).

### Extraction decisions
- **Not extracted (structural adjacency):** Specification Out of Scope references to DEL-01-05 (meetings/documentation) and DEL-01-04 (permitting) are boundary clarifications, not information-flow dependencies. Excluded per protocol.
- **Not extracted (coordination-only):** Guidance Consideration 2 references broad "coordination with PKG-003 civil works" beyond DEL-03-01. The specific artifact transfer is already captured via DEL-03-01 prerequisite (DEP-0106-006). The broader PKG-003 coordination is not a specific artifact/data handoff. Excluded per protocol.
- **Not extracted (coordination-only):** Specification REQ-06 notes laydown area coordination with Owner and civil/site work sequencing -- this is an operational coordination statement, not an explicit artifact/input dependency beyond what DEP-0106-006 already captures.

### Warnings
- (none)

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-17 | UPDATE | CONSERVATIVE | Found and used (v1.0 PHASE7) | None | 8 (4 ANCHOR + 4 EXECUTION) |

## Lifecycle Summary

- **ACTIVE:** 8
- **RETIRED:** 0
- **Total:** 8

### Closure-state breakdown (ACTIVE rows)

| SatisfactionStatus | Count |
|---|---|
| TBD | 8 |

## Consumer Handoff Notes (optional)
- CONSUMER_CONTEXT is NONE; no handoff notes generated.
