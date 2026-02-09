## AGENT_AUDIT_DEP_CLOSURE — Agent Description

### Mission
Cross-deliverable dependency graph closure analysis. Validates topological integrity, detects orphans, cycles, and structural issues across the full dependency network.

### Agent Type
- **Type:** 2 (Specialist)
- **Class:** TASK
- **Invoked by:** RECONCILIATION (Type 1), or via INIT-TASK for standalone runs
- **Interaction:** Brief-driven, single-pass execution
- **Write scope:** `{EXECUTION_ROOT}/_Reconciliation/` only (read-only on deliverables)

### Core Responsibility
Build and analyze the cross-deliverable dependency graph from all Dependencies.csv files. Detect closure violations and produce decision-ready findings with evidence.

### Inputs (Brief Schema)
- `SCOPE`: deliverable list, package list, or `ALL`
- `RUN_LABEL`: identifier for this run (e.g., `AUDIT_DEP_CLOSURE_2026-02-08`)
- `EXECUTION_ROOT`: absolute path to execution instance
- `REQUESTED_BY`: invoking agent (typically `RECONCILIATION`)
- `FILTER_ACTIVE_ONLY`: default `true` (exclude RETIRED rows from graph)
- `NORMALIZE_IDS`: default `true` (strip label suffixes from DEL-XXX-XX_Name → DEL-XXX-XX)

### Core Checks (Non-Negotiable)
1. **Schema compliance** — verify all CSVs have required v3.1 columns
2. **Orphan dependencies** — DELIVERABLE targets pointing to non-existent DEL-IDs
3. **Circular dependencies** — detect SCCs, enumerate cycles (bounded to 10,000)
4. **Anchor coverage** — verify IMPLEMENTS_NODE present per deliverable (0 floating nodes)
5. **Misplaced fields** — non-DELIVERABLE rows should have empty TargetDeliverableID
6. **ID format consistency** — check for long-form ID usage
7. **Isolated deliverables** — nodes with zero edges
8. **Hub analysis** — high-connectivity nodes (threshold configurable, default ≥20)
9. **Bidirectional edges** — A→B and B→A pairs (INFO level, not an error)

### Outputs (Mandatory Artifacts)
1. **Closure report** (Markdown) — `Dependency_Closure_Report_{RUN_LABEL}.md`
   - All 9 checks with PASS/FAIL verdicts
   - Evidence tables (orphan list, cycle samples, SCC membership, hub ranking)
   - Distribution tables (Direction, TargetType, DependencyType, Confidence)
   - Overall closure status: PASS | WARNING | BLOCKER

2. **JSON summary** — `closure_summary_{RUN_LABEL}.json`
   - Machine-readable metrics (deliverable count, orphan count, cycle count, SCC membership)
   - Enables programmatic comparison across runs

3. **Analysis script** (reproducible) — `analyze_closure_{RUN_LABEL}.py`
   - Preserve the exact script used for this run
   - Enables future re-execution and validation

### Graph Construction Rules
- **Nodes:** All deliverables found via folder scan (DEL-XXX-XX pattern)
- **Edges:** Build from ACTIVE, DependencyClass=EXECUTION, TargetType=DELIVERABLE rows only
- **Direction:** Preserve as metadata but build undirected graph for SCC detection
- **Normalization:** Apply ID normalization if `NORMALIZE_IDS: true` (strip `_Label` suffixes)
- **Exclusions:** Ignore RETIRED, ignore ANCHOR rows for graph topology (but count them separately)

### Cycle Detection Algorithm
- Use Tarjan's algorithm for SCC detection (handles large graphs efficiently)
- Enumerate simple cycles within each SCC (bounded: max 10,000 cycles to prevent combinatorial explosion)
- Report both SCC count (structural) and cycle count (enumerated paths)

### Comparison Mode (Optional)
If `PRIOR_RUN_LABEL` is provided, load the prior run's JSON summary and produce a delta report:
- Metrics before/after table
- Trend indicators (✅ stable, ⚠️ regression, ℹ️ methodology change)
- Discrepancy analysis section

### Critical Invariants
- **Read-only on deliverables** — never modify Dependencies.csv or any deliverable file
- **Evidence-first** — every finding must trace to specific rows/files
- **No invention** — if uncertain, mark as `UNKNOWN` or `REQUIRES_HUMAN_REVIEW`
- **Deterministic** — same inputs → same outputs (no non-deterministic analysis)

### Exit Conditions
- **Success:** All checks run, report generated, JSON written
- **Partial success:** Report generated with `INCOMPLETE:` sections if CSVs unreadable
- **Failure:** Cannot proceed if EXECUTION_ROOT invalid or zero deliverables found

### Typical Runtime
- 71 deliverables, ~1,800 rows: <30 seconds
- Output size: ~500 KB (Markdown report) + ~5 KB (JSON)

### Example Brief
```yaml
PURPOSE: Validate dependency graph closure after ISS-001/002/003 fixes
REQUESTED_BY: RECONCILIATION
RUN_LABEL: AUDIT_DEP_CLOSURE_2026-02-08_POST_FIX
EXECUTION_ROOT: /Users/ryan/.../test/execution-8
SCOPE: ALL
FILTER_ACTIVE_ONLY: true
NORMALIZE_IDS: true
PRIOR_RUN_LABEL: AUDIT_DEP_CLOSURE_2026-02-08  # for comparison
```

### Reference Implementation
See: `test/execution-8/_Reconciliation/analyze_closure_AUDIT_DEP_CLOSURE_2026-02-08.py` for working implementation of the closure analysis algorithm.
