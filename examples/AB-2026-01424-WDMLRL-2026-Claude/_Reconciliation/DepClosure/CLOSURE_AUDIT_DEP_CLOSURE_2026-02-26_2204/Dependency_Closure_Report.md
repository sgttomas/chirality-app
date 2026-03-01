# Dependency Closure Report — AUDIT_DEP_CLOSURE

- Snapshot: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/_Reconciliation/DepClosure/CLOSURE_AUDIT_DEP_CLOSURE_2026-02-26_2204`
- Execution root: `/Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude`
- Scope: `ALL`
- Overall verdict: **BLOCKER**

## Check Verdicts

- Schema compliance: PASS
- Orphan dependencies: BLOCKER
- Circular dependencies (SCCs): WARNING
- Anchor coverage (IMPLEMENTS_NODE): PASS
- Misplaced fields: PASS
- ID format consistency / normalization: INFO
- Isolated deliverables: PASS
- Hub analysis (degree ≥ 20): INFO
- Bidirectional pairs: INFO

## Key Metrics

- Orphan deps (TargetDeliverableID not found): 2
- Cyclic SCCs: 1
- Isolated deliverables: 0
- Missing anchors: 0
- Misplaced-field rows: 0

## Evidence Files

- `Evidence/coverage.csv`
- `Evidence/orphans.csv` (if any)
- `Evidence/scc_summary.csv` and `Evidence/cycles_sample.csv` (if any)
- `Evidence/isolated_deliverables.csv` (if any)
- `Evidence/hubs.csv` (if any)
- `Evidence/bidirectional_pairs.csv` (if any)
- `Dependency_Closure_IssueLog.csv` (worklist)

## Top Issues (≤10)

- BLOCKER Orphan dependencies: ORPHAN::DEL-018-06::DEL-003::DEP-018-06-010 — /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-018_Sitework & Civil Construction/1_Working/DEL-018-06_Utility-Tieins/Dependencies.csv:11 (DependencyID=DEP-018-06-010)
- BLOCKER Orphan dependencies: ORPHAN::DEL-018-06::DEL-004::DEP-018-06-009 — /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-018_Sitework & Civil Construction/1_Working/DEL-018-06_Utility-Tieins/Dependencies.csv:10 (DependencyID=DEP-018-06-009)
- WARNING Circular dependencies: CYCLE::SCC-001 — /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-001_Architectural Design/1_Working/DEL-001-03_Exterior-Elevations/Dependencies.csv:23 (DependencyID=DEP-001-03-E19); /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-001_Architectural Design/1_Working/DEL-001-05_Interior-Elevations/Dependencies.csv:15 (DependencyID=DEP-001-05-E11); /Users/ryan/ai-env/projects/chirality-project-test/test/AB-2026-01424-WDMLRL-2026-Claude/PKG-001_Architectural Design/1_Working/DEL-001-03_Exterior-Elevations/Dependencies.csv:8 (DependencyID=DEP-001-03-E04)

## Recommended Next Actions

- Fix orphan TargetDeliverableID references (see `Evidence/orphans.csv`), then rerun closure.
- Review cyclic SCCs (see `Evidence/scc_summary.csv`) and decide: bundle as iterative sets or adjust dependency directions/types.
