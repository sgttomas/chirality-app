# DAG-002 currency audit — APP_V4_DAG002_ACCEPTED

**Result: `CURRENT`.** No source byte has changed since DAG-002's basis. **No deliverable is `DAG pending`.**

The owner accepted DAG-002 on 2026-09-29 (OWNER_DECISIONS.md DECISION-10). That decision cleared the 15 flags raised against DAG-001 by `CURRENCY_APP_V4_BASISALIGN_2026-09-29_0856`, and this audit records the clearance.

- **Audit:** `project-dag` `currency.md` (method Stage 5, step 5), run `APP-V4-BASIS-ALIGN-20260928`, node D2, 2026-09-29.
- **Snapshot:** `CURRENCY_APP_V4_DAG002_ACCEPTED_2026-09-29_1050`. `_Evaluation/DAGCurrency/_LATEST.md` now points here.
- **Commands, exit codes and hashes:** [Tool_Run.json](Tool_Run.json). The outputs are in `Evidence/`.

## 1. The accepted version

`_DAG/_LATEST.md` is now in SPEC §11.2 form, and it parses. The registered parser (`dependency_evidence.pointer_target`) reads `Latest: DAG-002`, and `resolve_accepted_dag` loads `_DAG/DAG-002/`: 41 nodes, 124 admitted, 74 candidate and 264 excluded rows ([Evidence/pointer_check.json](Evidence/pointer_check.json)).

The pointer's header lines are:

- `Updated: 2026-09-29`
- `Acceptance: DAG-002/ACCEPTANCE_RECORD.md`
- `Completeness: FULL`
- `Basis revision: b585e5ebead38f8ece442c80cd3bec5be8363cf3`
- `Supersedes: DAG-001`

No candidate has a `REJECTION_RECORD.md`, so there is no rejected departure to report.

## 2. Manifest checks

| Check | Result |
|---|---|
| `shasum -a 256 -c MANIFEST.sha256`, run in `_DAG/DAG-002/` | **37/37 OK**, exit 0. The accepted snapshot is complete and intact |
| `shasum -a 256 -c _DAG/DAG-002/SOURCE_MANIFEST.sha256`, run in the execution root | **130/130 OK**, exit 0. All 41 `Dependencies.csv`, all 41 `_DEPENDENCIES.md` and the decomposition members equal the basis bytes |
| `shasum -a 256 -c MANIFEST.sha256`, run in `_DAG/DAG-001/` (superseded) | **61/61 OK**, exit 0. The history is unchanged |

**Inventory.** The accepted decomposition pointer, `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` (sha256 `d5d873b3…5a695ead`), still names GROUP3-20260928T001055Z. The register `canonical/Deliverables.csv` (sha256 `bcdf6f2f…415eb`) is the inventory recorded in DAG-002's `GRAPH_BASIS.md`, and it is unchanged.

## 3. Classification

**`CURRENT`.** No source bytes changed and the inventory is unchanged (currency.md step 3), so no scratch re-assembly is needed. Consumers may rely on DAG-002 within the reliance boundary in its [ACCEPTANCE_RECORD](../../../_DAG/DAG-002/ACCEPTANCE_RECORD.md).

## 4. `DAG pending` deliverables

**None.** These 15 flags are cleared by the owner's acceptance of DAG-002:

DEL-01-01, DEL-02-01, DEL-02-02, DEL-02-03, DEL-03-01, DEL-03-02, DEL-03-03, DEL-03-04, DEL-04-01, DEL-04-02, DEL-04-03, DEL-05-01, DEL-05-02, DEL-09-06 and DEL-09-09.

## 5. Analyzer cross-check

The registered closure analyzer, `tools/coordination/analyze_dep_closure.py` (sha256 `2b8de3cb…a9adc`), was run with the DAG-001/DAG-002 closure arguments and without `--output-dir`, so it wrote nothing. Its stdout is kept in [Evidence/analyzer.stdout.json](Evidence/analyzer.stdout.json).

Its `accepted_dag` section now reports:

- version `DAG-002`;
- result **`NO_DEPARTURE_FOUND`**;
- 0 `DAG pending`;
- no added or removed arcs or deliverables.

**It no longer reports `INCOMPLETE`.** That was its result under DAG-001's prose pointer (`_Evaluation/DepClosure/CLOSURE_APP_V4_BASISALIGN_2026-09-29_0855`). The whole-graph figures are unchanged: 41 nodes, 198 arcs and 6 SCCs. The raw acyclic-objective subject status is still `FAIL` because of the six characterized SCCs, as for DAG-001 and DAG-002.

This run is a cross-check, not a closure snapshot. `_Evaluation/DepClosure/_LATEST.md` was not moved.

## 6. What follows

- **The next audit is due** when a consumer relies on DAG-002 after the local files may have changed, after any `dependency-extract` run or declaration change, or after an accepted scope change. That includes **SCA-V4-002** when it is applied: its "consumes" wording for N-18, N-21, N-24 and X-1 is expected to add rows, and they would be a small departure.
- **Scope of this audit.** It establishes currency only. It does not establish satisfaction, readiness or lifecycle, and it did not modify DAG-001, DAG-002, `_DAG/_LATEST.md` or any local file.
