# DAG-004 currency audit — APP_V4_DAG004_ACCEPTED

**Result: `CURRENT`.** No source byte has changed since DAG-004's basis. **No deliverable is `DAG pending`.**

The owner accepted DAG-004 on 2026-10-03 (`_Coordination/AgentRuns/APP-V4-SCA003-20261002/OWNER_DECISIONS.md` DECISION-3, covering project-dag checkpoints 1 and 2). That decision cleared the 11 flags raised against DAG-003 by `CURRENCY_APP_V4_SCA003_2026-10-03_1937`. This audit records the clearance.

- **Audit:** `project-dag` `currency.md` (method Stage 5, step 5), run `APP-V4-SCA003-20261002`, node D2, 2026-10-03 20:12 MDT.
- **Snapshot:** `CURRENCY_APP_V4_DAG004_ACCEPTED_2026-10-03_2012`. `_Evaluation/DAGCurrency/_LATEST.md` now points here. The departure audit `CURRENCY_APP_V4_SCA003_2026-10-03_1937` was staged in the run's `DAG_PREP/` under D1's write fence. It was placed beside this snapshot at publication, byte-identical to the review packet's hashes. It is history and was never the pointer target.
- **Commands, exit codes and hashes:** [Tool_Run.json](Tool_Run.json). The outputs are in `Evidence/`.

## 1. The accepted version

`_DAG/_LATEST.md` was written at publication from the candidate's `PROPOSED_LATEST.md` with `{ACCEPT_DATE}` = 2026-10-03 (sha256 `b9353a41…f55d4ca2d`). It is in SPEC §11.2 form and it parses. The registered parser (`dependency_evidence.pointer_target`) reads `Latest: DAG-004`. `resolve_accepted_dag` then loads `_DAG/DAG-004/`: 41 nodes, 129 admitted, 83 candidate and 355 excluded rows ([Evidence/pointer_check.json](Evidence/pointer_check.json)).

The pointer's header lines are:

- `Updated: 2026-10-03`
- `Acceptance: DAG-004/ACCEPTANCE_RECORD.md`
- `Completeness: FULL`
- `Basis revision: 75764184b99ab006cd46c1d1c328cf7d5c4d0c8d`
- `Supersedes: DAG-003`

No candidate has a `REJECTION_RECORD.md`, so there is no rejected departure to report.

## 2. Manifest checks

| Check | Result |
|---|---|
| `shasum -a 256 -c MANIFEST.sha256`, run in `_DAG/DAG-004/` | **37/37 OK**, exit 0. The accepted snapshot is complete and intact: the 33 presented files, `ACCEPTANCE_RECORD.md`, `HANDOFF_STATE.md`, `INDEPENDENT_REVIEW.md` and `REVIEW_PACKET.md` |
| `shasum -a 256 -c _DAG/DAG-004/SOURCE_MANIFEST.sha256`, run in the execution root | **130/130 OK**, exit 0 |
| `shasum -a 256 -c MANIFEST.sha256` in `_DAG/DAG-003/`, `_DAG/DAG-002/` and `_DAG/DAG-001/` (superseded) | **37/37, 37/37 and 61/61 OK**, exit 0. The history is unchanged |

**Inventory.** The accepted decomposition pointer `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` (sha256 `6ef9c0ba…afabb`, the bytes DAG-004's source manifest binds) still names GROUP3-20260928T001055Z. Its `canonical/Deliverables.csv` (sha256 `bcdf6f2f…415eb`) is unchanged.

## 3. Classification

**`CURRENT`.** No source bytes changed and the inventory is unchanged (currency.md step 3). Consumers may rely on DAG-004 within the reliance boundary in `_DAG/DAG-004/ACCEPTANCE_RECORD.md`, and should read it as `_DAG/DAG-004/HANDOFF_STATE.md` directs.

## 4. `DAG pending` deliverables

**None.** The owner's acceptance of DAG-004 cleared these 11 flags:

DEL-01-02, DEL-01-03, DEL-01-04, DEL-01-05, DEL-02-01, DEL-02-02, DEL-02-03, DEL-02-04, DEL-03-03, DEL-04-02 and DEL-04-03.

On release, DEL-01-04, DEL-02-02, DEL-02-03 and DEL-03-03 read the five new admitted arcs as blockers, but only for the stated parts of their work: NR-05 and NR-07, NR-04, NR-01 and NR-02. The other seven read the same blockers as under DAG-003.

## 5. Analyzer cross-check

The registered closure analyzer, `tools/coordination/analyze_dep_closure.py` (sha256 `2b8de3cb…a9adc`), was run with the project closure arguments and without `--output-dir`, so it wrote nothing. Its stdout is kept in [Evidence/analyzer.stdout.json](Evidence/analyzer.stdout.json).

Its `accepted_dag` section reports:

- version `DAG-004`;
- result **`NO_DEPARTURE_FOUND`**;
- 0 `DAG pending`;
- no added or removed arcs or deliverables.

This is the result the candidate's `Evidence/successor_currency_precheck.json` predicted, and V25 reproduced in scratch. The whole-graph figures are:

- 41 nodes and 212 arcs (129 admitted and 83 held);
- 6 SCCs of sizes 2/13/2/3/2/2;
- 4 hubs at threshold 20.

The raw acyclic-objective subject status is still `FAIL` because of the six characterized SCCs, as for every earlier version. This run is a cross-check, not a closure snapshot. The latest closure snapshot is `CLOSURE_APP_V4_SCA003_2026-10-03_1936`, which `_Evaluation/DepClosure/_LATEST.md` now names.

## 6. What follows

**The next audit is due** in any of these cases:

- a consumer relies on DAG-004 after the local files may have changed;
- any `dependency-extract` run or declaration change, including the accepted repair of DEL-01-03's absolute TargetLocation (DECISION-3 effect 4). After that repair, the audit is expected to read `CURRENT_WITH_EVIDENCE_DRIFT` unless an arc changes;
- an accepted scope change or decomposition revision.

**Scope of this audit.** It establishes currency only. It does not establish satisfaction, readiness or lifecycle. It did not modify DAG-001…004, `_DAG/_LATEST.md`, any case or any local file.
