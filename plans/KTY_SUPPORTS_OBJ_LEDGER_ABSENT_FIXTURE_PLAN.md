# KTY_SUPPORTS_OBJ Ledger-Absent Fixture Plan

## Status

Deferred for later implementation.

## Role

Deferred Regression-Hardening Plan

## Relationship

`agents/AGENT_DOMAIN_HYPERGRAPH.md` explicitly states that objective nodes and
`KTY_SUPPORTS_OBJ` edges can be emitted without ledger data when objectives are
loaded independently.

The current validator covers `KTY_SUPPORTS_OBJ` creation in the presence of
ledger rows, but it does not yet prove the ledger-absent path directly. That
independence is currently trusted from code structure rather than protected by a
fixture.

This note captures the follow-up needed to harden that contract.

## Purpose

Add a small fixture proving that:

- `discovered_objectives.csv` can create OBJECTIVE nodes without ledger rows
- `kty_supports_obj.csv` can create `KTY_SUPPORTS_OBJ` edges without ledger rows
- `LEDGER_INTEGRITY` does not appear when ledger rows are absent

## Proposed Fixture Shape

Add one new fixture:

`tools/aggregation/testdata/kty_supports_obj_no_ledger/Evidence/`

Suggested contents:

- `discovered_categories.csv`
- `discovered_knowledge_types.csv`
- `discovered_objectives.csv`
- `kty_supports_obj.csv`

Intentionally omit:

- `discovered_ledger_rows.csv`

Keep the fixture minimal:

- 1-2 categories
- 1-2 knowledge types
- 1-2 objectives
- 1 valid `KTY_SUPPORTS_OBJ` row

## Suggested Assertions

Extend `tools/validation/validate_build_hypergraph_fixture.py` with one new
check function:

- run the tool on the ledger-absent fixture
- assert:
  - `KTY_SUPPORTS_OBJ` appears in `hyperedge_counts_by_type`
  - `OBJECTIVE` appears in `node_counts_by_type`
  - `LEDGER_ROW` does not appear in `hyperedge_counts_by_type`
  - `ATOMIC_UNIT` does not appear in `node_counts_by_type`
- assert `LEDGER_INTEGRITY` is not present in PASS / WARNING / BLOCKER
- assert no unexpected warnings or blockers are emitted

## Constraints

- No new test framework.
- Keep this inside the existing validator.
- Do not add ledger rows just to satisfy unrelated assertions; the whole point
  is to exercise the ledger-absent path directly.

## Verification

Primary command:

```sh
python3 tools/validation/validate_build_hypergraph_fixture.py
```

Optional inspection:

```sh
python3 tools/validation/validate_build_hypergraph_fixture.py --keep-tmp
```

Inspect the ledger-absent run and confirm:

- `nodes.csv` contains OBJECTIVE nodes
- `hyperedges.csv` contains `KTY_SUPPORTS_OBJ`
- no `LEDGER_ROW` edges exist
- `QA_Report.md` does not include `LEDGER_INTEGRITY`

## Short Summary

The remaining ledger-absent `KTY_SUPPORTS_OBJ` blind spot should be closed with
one minimal fixture that proves objectives and support edges can be built
without any ledger participation.
