# Brief — closure run for APP-V4-SCA002-20260929 (node D1)

## Verbatim (the closure stage of the D1 brief)

> 1. **Closure:** `audit-dep-closure` SCOPE ALL over the current registers; snapshot where that workflow says; move its `_LATEST.md`.

The D1 brief also sets the write scope ("E/_Evaluation/ (closure and currency snapshots and their `_LATEST.md`)"), read-only Git, no network, and no acceptance.

## Normalized

| Field | Value |
|---|---|
| Workflow | `chirality-root:bundled:workflow:audit-dep-closure` (Root bundled library at the basis commit) |
| EXECUTION_ROOT | `projects/chirality-app-v4/execution` |
| SCOPE | `ALL`: the accepted GROUP3 inventory (41 Deliverables, 11 Packages), resolved through `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` |
| SCOPE_INVENTORY_SOURCE | `_Decomposition/checkpoint_snapshots/GROUP3-20260928T001055Z/canonical/Deliverables.csv` |
| EXEMPT_UNITS | none |
| RUN_LABEL | `APP_V4_SCA002` |
| REQUESTED_BY | HELP_HUMAN integrator (WORKING_ITEMS consultation), run `APP-V4-SCA002-20260929` |
| Filters | FILTER_ACTIVE_ONLY true; NORMALIZE_IDS true; EXECUTION × DELIVERABLE; HUB_THRESHOLD 20; MAX_CYCLES 200; INCLUDE_DECLARED true |
| PRIOR_SUMMARY | `_Evaluation/DepClosure/CLOSURE_APP_V4_BASISALIGN_2026-09-29_0855/Evidence/closure_summary.json` (DAG-002's closure) |
| UPDATE_LATEST_POINTER | true (observation pointer only; the D1 write scope names the closure `_LATEST.md`) |
| Source revision | `8cd783d8d7493fbfe663fb108449e4ceda04a00b`, working tree clean |
| Frozen manifest | 130 entries, SHA-256 `d0fc611d95ee80ba64b86ea5b0eaa1a1ba90e85e461fb18459dd8162df6a40c5` (the DAG-003 candidate `SOURCE_MANIFEST.sha256`), 32 members changed since DAG-002 |

These are DAG-001's and DAG-002's closure arguments unchanged, so the result is directly comparable with the prior snapshot.
