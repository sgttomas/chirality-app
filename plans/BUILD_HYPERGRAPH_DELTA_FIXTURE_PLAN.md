# build_hypergraph Delta Fixture Plan

## Status

Deferred for later implementation.

## Role

Deferred Regression-Hardening Plan

## Relationship

`tools/aggregation/build_hypergraph.py` already supports `--prior-snapshot`
delta computation and writes a `delta` block into `hypergraph.json` plus a
"Delta vs prior run" section in `QA_Report.md`.

The current validator at
`tools/validation/validate_build_hypergraph_fixture.py` does not exercise that
path yet. The existing regression coverage is strong for deterministic graph
construction and QA findings, but it still leaves delta serialization and
delta-count correctness unguarded.

This note captures the intended follow-up so the delta path can be hardened
without reconstructing the design discussion.

## Purpose

Add a fixture-driven regression check for `--prior-snapshot` so changes to
delta computation are caught early.

The goal is not to exhaustively test every add/remove combination. The goal is
to lock the contract that:

- a valid prior snapshot is read
- node and edge additions/removals are counted correctly
- `hypergraph.json` includes the expected `delta` block
- `QA_Report.md` includes the expected "Delta vs prior run" section

## Proposed Fixture Shape

Use two related snapshot fixtures:

1. `tools/aggregation/testdata/delta_prior/Evidence/`
2. `tools/aggregation/testdata/delta_current/Evidence/`

The second fixture should differ in a small, controlled way from the first:

- one node added
- one node removed
- one hyperedge added
- one hyperedge removed

Keep the change set intentionally small so the expected delta is obvious and
easy to review.

## Suggested Assertions

Extend `tools/validation/validate_build_hypergraph_fixture.py` with one new
check function:

- run the tool on `delta_prior` to produce a prior snapshot
- run the tool on `delta_current` with `--prior-snapshot {prior_output_dir}`
- assert `hypergraph.json` contains a `delta` block
- assert:
  - `nodes_added`
  - `nodes_removed`
  - `hyperedges_added`
  - `hyperedges_removed`
    match the expected values
- assert `changes_by_type` contains the expected type-level buckets
- assert `QA_Report.md` contains the "Delta vs prior run" section and the prior
  run label

## Constraints

- No new test framework.
- Keep this inside the existing manual validator.
- Keep the fixtures small and explicit.
- Do not change tool behavior as part of the fixture addition unless a real bug
  is found.

## Verification

Primary command:

```sh
python3 tools/validation/validate_build_hypergraph_fixture.py
```

Optional inspection:

```sh
python3 tools/validation/validate_build_hypergraph_fixture.py --keep-tmp
```

Inspect the generated current run and confirm:

- `hypergraph.json` contains a `delta` block
- `QA_Report.md` contains the delta summary section
- the reported counts match the intended fixture differences

## Short Summary

The remaining delta-path blind spot should be closed by adding one paired
prior/current fixture and one validator check that proves the `--prior-snapshot`
contract works end to end.
