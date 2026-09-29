# Brief — closure run for APP-V4-BASIS-ALIGN-20260928 (node D1)

## Verbatim (the closure stage of the D1 brief)

> 1. **Closure.** Run `audit-dep-closure` over the accepted inventory, with SCOPE ALL and its rules, on the current registers. Write the snapshot where that workflow says.

The D1 brief also sets the write scope ("E/_Evaluation/ (closure and currency snapshots, and their `_LATEST.md`)"), read-only Git, no network, and no acceptance.

## Normalized

| Field | Value |
|---|---|
| Workflow | `chirality-root:bundled:workflow:audit-dep-closure` (Root bundled library at the basis commit) |
| EXECUTION_ROOT | `projects/chirality-app-v4/execution` |
| SCOPE | `ALL`: the accepted GROUP3 inventory (41 Deliverables, 11 Packages), resolved through `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` |
| SCOPE_INVENTORY_SOURCE | `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv` |
| EXEMPT_UNITS | none |
| RUN_LABEL | `APP_V4_BASISALIGN` |
| REQUESTED_BY | HELP_HUMAN integrator (WORKING_ITEMS consultation), run `APP-V4-BASIS-ALIGN-20260928` |
| Filters | FILTER_ACTIVE_ONLY true; NORMALIZE_IDS true; EXECUTION × DELIVERABLE; HUB_THRESHOLD 20; MAX_CYCLES 200; INCLUDE_DECLARED true |
| PRIOR_SUMMARY | `_Evaluation/DepClosure/CLOSURE_APP_V4_TARGETS_2026-09-27_2237/Evidence/closure_summary.json` (DAG-001's closure) |
| UPDATE_LATEST_POINTER | true (observation pointer only; D1 write scope names the closure `_LATEST.md`) |
| Source revision | `b585e5ebead38f8ece442c80cd3bec5be8363cf3`, working tree clean |
| Frozen manifest | 130 entries, SHA-256 `6d1021f1c78fea023c2089aa29a2bc60f5ae498f56068eeddbfa376467793250` (the DAG-002 candidate `SOURCE_MANIFEST.sha256`) |

These are DAG-001's closure arguments unchanged (SUCCESSOR_PLAN §2 step 3).
