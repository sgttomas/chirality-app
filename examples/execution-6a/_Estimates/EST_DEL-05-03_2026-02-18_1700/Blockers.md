# Blockers Report -- DEL-05-03 Option - Access Control

**Snapshot:** EST_DEL-05-03_2026-02-18_1700

## Summary

- **Total upstream blockers identified:** 2
- **Impact on estimate:** Estimate is producible using parametric assumptions, but zone count and detailed scope definition are blocked pending upstream deliverables.

## Blockers (by deliverable)

### DEL-05-03 Option - Access Control

| # | Dependency | Type | Target | Statement | Estimate Impact | Evidence |
|---|---|---|---|---|---|---|
| 1 | DEP-05-03-003 | PREREQUISITE | DEL-02-01 (Architectural Program) | Requires floor plan concept for zone mapping | Zone count is assumed at 10 (PP-28); actual may differ once floor plan is available. If zone count changes, estimate must be re-run. | Procedure.md > Prerequisites |
| 2 | DEP-05-03-004 | INTERFACE | DEL-02-06 (Electrical/IT) | Requires coordination for low-voltage power, conduit, network | Does not directly change pricing (costs for power circuits and IT network are excluded from DEL-05-03 per cost ownership rules), but interface details affect detailed wiring scope and may surface additional conduit or pathway costs. | Specification.md > REQ-AC-006 |

## Non-blocking Dependencies (informational)

| Dependency | Type | Target | Notes |
|---|---|---|---|
| DEP-05-03-005 | INTERFACE (DOWNSTREAM) | DEL-05-04 (Security & Cameras) | Integration is optional; access control designed as self-contained. Does not affect pricing. |
| DEP-05-03-006 | HANDOVER (DOWNSTREAM) | DEL-01-07 (Commissioning/Closeout) | Commissioning feeds into building Cx process. No pricing impact. |
| DEP-05-03-007 | CONSTRAINT (UPSTREAM) | DEL-01-01 (Design Management) | Submittal schedule constraint; no pricing impact. |
| DEP-05-03-008 | PREREQUISITE (UPSTREAM) | Functional Program (Appendix B) | Key Fob Access room designations. Used for zone concept. Available in RFP. |
| DEP-05-03-009 | PREREQUISITE (UPSTREAM) | OSR S12.3 (Access Control) | Primary requirement statement. Available in RFP. |
