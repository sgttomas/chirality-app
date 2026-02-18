# Blockers Report -- EST_DEL-04-04_2026-02-18_1500

## Summary

No unresolved blockers prevent rate-table-based estimating at this stage. All 4 execution prerequisites (DEP-04-04-004 through DEP-04-04-007) are design-phase dependencies that will need resolution before detailed design but do not block area-based rate-table estimating.

## Dependency Assessment

| DependencyID | Type | Target | Status for Estimating | Notes |
|---|---|---|---|---|
| DEP-04-04-001 | ANCHOR (implements SOW-0300) | SOW-0300 | Not a blocker | Scope anchor; confirmed. |
| DEP-04-04-002 | ANCHOR (traces to OBJ-004) | OBJ-004 | Not a blocker | Objective anchor; confirmed. |
| DEP-04-04-003 | ANCHOR (traces to SOW-0302) | SOW-0302 | Not a blocker | Requirement anchor for door opener electrical; confirmed. |
| DEP-04-04-004 | PREREQUISITE | DEL-04-01 (building configuration, heights) | Not blocking estimating | Needed for detailed design (lighting fixture heights, ventilation sizing). Rate-table estimating uses area-based rates that do not require resolved building geometry. |
| DEP-04-04-005 | PREREQUISITE | DEL-04-02 (door schedule, opener specs) | Not blocking estimating | Needed for detailed circuit design. Rate-table estimating uses ES-12 which includes door opener feeds generically. PP-14 confirms 2 overhead doors. |
| DEP-04-04-006 | INTERFACE | DEL-04-03 (floor/foundation system) | Not blocking estimating | Needed for conduit routing coordination. Rate-table estimating is independent of conduit routing details. |
| DEP-04-04-007 | PREREQUISITE (external) | Environment Canada climate normals | Not blocking estimating | Needed for ventilation sizing and condensation risk analysis. Rate-table estimating uses MS-13 area rate which assumes passive/low-energy ventilation. If climate data drives active mechanical ventilation, a rerun with updated rates may be needed. |
| DEP-04-04-008 | INTERFACE | DEL-01-04 (permitting/inspections) | Not blocking estimating | Execution-phase interface for electrical permits. |
| DEP-04-04-009 | HANDOVER (downstream) | DEL-01-07 (commissioning/closeout) | Not blocking estimating | Downstream handover of as-builts. |
