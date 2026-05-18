# Coordination Record

**Project:** Town of Penhold -- Public Services Building (PSB)
**Decomposition:** Penhold_PSB_Project_Decomposition_FINAL_v1.0_PHASE7.md
**Established:** 2026-02-17

**Representation:** Declared critical dependencies
**Dependency tracking mode:** DECLARED
**External schedule / coordination artifact:** N/A
**Default maturity threshold (if computing blockers):** INITIALIZED

## Dependency Rules

- **Mode:** DECLARED -- only interface-critical dependencies are recorded in-file; humans manage the rest.
- **Blocker computation:** computed only from declared edges in deliverable-local dependency registers.
- **Preferred register format:** Dependencies.csv (when DEPENDENCIES pipeline is run); _DEPENDENCIES.md as human-readable view.
- **Default threshold:** a dependency is considered "met" when the upstream deliverable reaches INITIALIZED or higher.
- **Dependency curation:** human-curated (ORCHESTRATOR does not auto-generate dependency edges without human acceptance).
- **Dependency proposals:** DISABLED -- operator will curate dependencies directly as a later work process. ORCHESTRATOR will not propose candidates.

## Confirmation Log

| Phase | Date | Decision | Status |
|---|---|---|---|
| 1.1 | 2026-02-17 | Decomposition ingested (6 PKG, 31 DEL) | CONFIRMED |
| 1.2 | 2026-02-17 | Coordination representation: Declared critical dependencies | CONFIRMED |
| 1.3 | 2026-02-17 | Dependency rules: threshold=INITIALIZED, format=_DEPENDENCIES.md (later Dependencies.csv), no auto-proposals | CONFIRMED |

## Scope Summary

| Metric | Count |
|---|---|
| Packages | 6 |
| Deliverables | 31 |
| Scope Items (IN) | 77 |
| Scope Items (OUT) | 1 |
| Objectives | 10 |
| Open Issues | 4 |

## Notes (human-owned)

- Coordination is managed by the operator through declared critical dependencies only.
- Blockers are advisory: computed from declared edges, not from a complete graph.
- The operator manages all other sequencing decisions externally.
