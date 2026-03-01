# Dependencies: DEL-004-02 Single-Line Diagram

## Coordination (human-owned)
- **Mode:** NOT_TRACKED
- **Notes:** Coordination representation pending -- to be confirmed by human via ORCHESTRATOR.

## Upstream (I need these before I can proceed) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Downstream (These need me) -- human-owned declarations
- Dependencies coordinated externally by humans.

## Extracted Dependency Register

- **Status:** COMPLETE
- **Dependencies.csv:** Present (v3.1 schema)
- **Total ACTIVE rows:** 18
- **ANCHOR rows:** 3 (1 IMPLEMENTS_NODE, 2 TRACES_TO_REQUIREMENT)
- **EXECUTION rows:** 15

| DependencyID | Class | Direction | Type | Target | Confidence |
|---|---|---|---|---|---|
| DEP-004-02-A01 | ANCHOR | UPSTREAM | OTHER | SOW-0014 (WBS_NODE) | HIGH |
| DEP-004-02-A02 | ANCHOR | UPSTREAM | OTHER | OBJ-003 (REQUIREMENT) | HIGH |
| DEP-004-02-A03 | ANCHOR | UPSTREAM | OTHER | OBJ-005 (REQUIREMENT) | HIGH |
| DEP-004-02-E01 | EXECUTION | UPSTREAM | PREREQUISITE | DEL-004-01 Preliminary Electrical Design | HIGH |
| DEP-004-02-E02 | EXECUTION | UPSTREAM | INTERFACE | DEL-003-05 Mechanical Equipment Schedule | HIGH |
| DEP-004-02-E03 | EXECUTION | UPSTREAM | INTERFACE | DEL-001-02 Architectural Floor Plans | HIGH |
| DEP-004-02-E04 | EXECUTION | UPSTREAM | INTERFACE | DEL-001-07 Door and Window Schedule | MEDIUM |
| DEP-004-02-E05 | EXECUTION | UPSTREAM | PREREQUISITE | DEL-016-01 Two 5-Tonne Overhead Cranes | HIGH |
| DEP-004-02-E06 | EXECUTION | UPSTREAM | PREREQUISITE | Utility service voltage and capacity (EXTERNAL) | HIGH |
| DEP-004-02-E07 | EXECUTION | UPSTREAM | INTERFACE | DEL-004-08 Electrical Calculation Package | HIGH |
| DEP-004-02-E08 | EXECUTION | DOWNSTREAM | HANDOVER | DEL-004-03 Power Distribution Plans | HIGH |
| DEP-004-02-E09 | EXECUTION | DOWNSTREAM | HANDOVER | DEL-004-06 Panel Schedules | HIGH |
| DEP-004-02-E10 | EXECUTION | DOWNSTREAM | HANDOVER | PKG-015 Electrical and Low-Voltage Installation | HIGH |
| DEP-004-02-E11 | EXECUTION | UPSTREAM | INTERFACE | DEL-002-07 Crane Support Structure Details | MEDIUM |
| DEP-004-02-E12 | EXECUTION | UPSTREAM | PREREQUISITE | CEC edition confirmation (EXTERNAL) | HIGH |
| DEP-004-02-E13 | EXECUTION | DOWNSTREAM | HANDOVER | DEL-004-05 Receptacle Layout Plans | HIGH |
| DEP-004-02-E14 | EXECUTION | DOWNSTREAM | HANDOVER | PKG-013 Mechanical and HVAC Installation | MEDIUM |
| DEP-004-02-E15 | EXECUTION | DOWNSTREAM | HANDOVER | PKG-018 Sitework and Civil Construction | MEDIUM |

## Run Notes

- **Run date:** 2026-02-26
- **MODE:** UPDATE
- **STRICTNESS:** CONSERVATIVE
- **CONSUMER_CONTEXT:** TASK_ESTIMATING
- **DECOMPOSITION_PATH:** /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Decomposition/WDMLRL_Decomposition_Claude.md (R1, 2026-02-25)
- **SOURCE_DOCS:** AUTO -- scanned: Datasheet.md, Specification.md, Guidance.md, Procedure.md
- **ANCHOR_DOC:** Datasheet.md (selected by heuristic: filename contains "datasheet")
- **EXECUTION_DOC_ORDER:** Procedure.md, Specification.md, Guidance.md (ordered by workflow clarity heuristic)
- **Read-only inputs consulted:** _REFERENCES.md, _CONTEXT.md
- **Decomposition status:** Available and validated. All deliverable IDs and package IDs confirmed against decomposition Section 7 tables.
- **Warnings:** None
- **Parent anchor check:** 1 IMPLEMENTS_NODE found (SOW-0014) -- PASS

### Changes from prior run

- **DEP-004-02-E05:** Updated TargetType from EXTERNAL to DELIVERABLE (DEL-016-01, PKG-016). Procedure Prerequisites explicitly references "DEL-016-01 (Two 5-Tonne Overhead Cranes)" as the source for crane electrical specifications. Resolved against decomposition.
- **DEP-004-02-E12 (NEW):** CEC edition confirmation extracted from Procedure Prerequisites ("Canadian Electrical Code CSA C22.1 -- applicable edition") and Specification REQ-SLD-011 (gating action for design). UPSTREAM PREREQUISITE, EXTERNAL.
- **DEP-004-02-E13 (NEW):** DEL-004-05 Receptacle Layout Plans extracted from Procedure Step 8.4 (explicit final consistency check) and Datasheet Construction section. DOWNSTREAM HANDOVER.
- **DEP-004-02-E14 (NEW):** PKG-013 extracted from Procedure Step 10.1 (explicit formal transmittal of IFC SLD). DOWNSTREAM HANDOVER.
- **DEP-004-02-E15 (NEW):** PKG-018 extracted from Procedure Step 10.1 (explicit formal transmittal of IFC SLD for utility tie-in coordination). DOWNSTREAM HANDOVER.

## Run History

| Timestamp | Mode | Strictness | Decomposition | Warnings | ACTIVE Count |
|---|---|---|---|---|---|
| 2026-02-26T00:00:00Z | UPDATE | CONSERVATIVE | Available | None | 14 |
| 2026-02-26T12:00:00Z | UPDATE | CONSERVATIVE | Available (R1, 2026-02-25) | None | 18 |

## Lifecycle Summary

- **ACTIVE:** 18
- **RETIRED:** 0
- **SatisfactionStatus breakdown:** TBD=9, PENDING=9, SATISFIED=0

### Closure-state detail

| SatisfactionStatus | Count | DependencyIDs |
|---|---|---|
| TBD | 9 | A01, A02, A03, E08, E09, E10, E13, E14, E15 |
| PENDING | 9 | E01, E02, E03, E04, E05, E06, E07, E11, E12 |

**Note:** TBD includes anchors (A01, A02, A03 -- not actionable for closure) and downstream handovers (E08, E09, E10, E13, E14, E15 -- satisfaction depends on IFC SLD completion). PENDING items are upstream inputs/prerequisites not yet received.

## Downstream Handoff Notes

**CONSUMER_CONTEXT: TASK_ESTIMATING**

Key estimating-relevant dependencies for DEL-004-02 Single-Line Diagram:

### BLOCKING (6 rows)

These dependencies gate meaningful estimating of the SLD because scope or key quantities are unknown without them:

| DependencyID | Target | Rationale |
|---|---|---|
| DEP-004-02-E01 | DEL-004-01 Preliminary Electrical Design | County approval gates IFC; SLD scope may change based on County feedback. |
| DEP-004-02-E02 | DEL-003-05 Mechanical Equipment Schedule | Mechanical equipment electrical ratings (MUA, heating, exhaust) are required inputs for load inventory; unknown loads affect service sizing. |
| DEP-004-02-E05 | DEL-016-01 Two 5-Tonne Overhead Cranes | Crane electrical specifications (motor ratings, locked-rotor current) are potentially the dominant demand factor; TBD on SLD. |
| DEP-004-02-E06 | Utility service voltage and capacity (EXTERNAL) | System voltage selection (120/208V vs. 347/600V) fundamentally changes SLD architecture, panel ratings, and all downstream sizing. |
| DEP-004-02-E07 | DEL-004-08 Electrical Calculation Package | Load calculation determines main service size, MDP bus rating, and sub-panel sizing -- all core SLD content. Iterative relationship. |
| DEP-004-02-E12 | CEC edition confirmation (EXTERNAL) | Code edition determines applicable demand factors, circuit sizing rules, and compliance requirements for all SLD content. |

### ADVISORY (6 rows)

These dependencies affect design detail and quantities but do not hard-gate estimating:

| DependencyID | Target | Rationale |
|---|---|---|
| DEP-004-02-E03 | DEL-001-02 Architectural Floor Plans | Floor plan dimensions affect sub-panel placement and voltage drop calculations; conceptual dimensions (130' x 100') are available. |
| DEP-004-02-E04 | DEL-001-07 Door and Window Schedule | Overhead door quantity and motor ratings affect dedicated circuit count; relatively minor portion of total load. |
| DEP-004-02-E08 | DEL-004-03 Power Distribution Plans | Downstream consistency requirement; affects estimating only if power plans reveal routing constraints. |
| DEP-004-02-E09 | DEL-004-06 Panel Schedules | Downstream consistency requirement; panel schedule detail follows SLD. |
| DEP-004-02-E11 | DEL-002-07 Crane Support Structure Details | Structural crane support informs crane power routing; secondary to crane spec itself (E05). |
| DEP-004-02-E13 | DEL-004-05 Receptacle Layout Plans | Downstream consistency requirement; receptacle layout follows SLD hierarchy. |

### INFO (3 rows)

Informational context; low likelihood of changing estimating totals:

| DependencyID | Target | Rationale |
|---|---|---|
| DEP-004-02-E10 | PKG-015 Electrical and Low-Voltage Installation | Downstream handover of IFC SLD to electrical contractor. Informational for design estimating. |
| DEP-004-02-E14 | PKG-013 Mechanical and HVAC Installation | Downstream transmittal for mechanical electrical awareness. |
| DEP-004-02-E15 | PKG-018 Sitework and Civil Construction | Downstream transmittal for utility tie-in coordination. |
