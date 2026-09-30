# DAG-003 currency audit — APP_V4_DAG003_ACCEPTED

**Result: `CURRENT`.** No source byte has changed since DAG-003's basis. **No deliverable is `DAG pending`.**

The owner accepted DAG-003 on 2026-09-29 (OWNER_DECISIONS.md DECISION-4, covering project-dag checkpoints 1 and 2). That decision cleared the 5 flags raised against DAG-002 by `CURRENCY_APP_V4_SCA002_2026-09-29_2057`, and this audit records the clearance.

- **Audit:** `project-dag` `currency.md` (method Stage 5, step 5), run `APP-V4-SCA002-20260929`, node D2, 2026-09-29.
- **Snapshot:** `CURRENCY_APP_V4_DAG003_ACCEPTED_2026-09-29_2218`. `_Evaluation/DAGCurrency/_LATEST.md` now points here.
- **Commands, exit codes and hashes:** [Tool_Run.json](Tool_Run.json). The outputs are in `Evidence/`.

## 1. The accepted version

`_DAG/_LATEST.md` was written at publication from the candidate's `PROPOSED_LATEST.md` with `{ACCEPT_DATE}` = 2026-09-29 (sha256 `4d381ba4…992f56`). It is in SPEC §11.2 form and it parses: the registered parser (`dependency_evidence.pointer_target`) reads `Latest: DAG-003`, and `resolve_accepted_dag` loads `_DAG/DAG-003/`: 41 nodes, 124 admitted, 78 candidate and 263 excluded rows ([Evidence/pointer_check.json](Evidence/pointer_check.json)).

The pointer's header lines are:

- `Updated: 2026-09-29`
- `Acceptance: DAG-003/ACCEPTANCE_RECORD.md`
- `Completeness: FULL`
- `Basis revision: 8cd783d8d7493fbfe663fb108449e4ceda04a00b`
- `Supersedes: DAG-002`

No candidate has a `REJECTION_RECORD.md`, so there is no rejected departure to report.

## 2. Manifest checks

| Check | Result |
|---|---|
| `shasum -a 256 -c MANIFEST.sha256`, run in `_DAG/DAG-003/` | **37/37 OK**, exit 0. The accepted snapshot is complete and intact: the 33 presented files, `ACCEPTANCE_RECORD.md`, `HANDOFF_STATE.md`, `INDEPENDENT_REVIEW.md` and `REVIEW_PACKET.md` |
| `shasum -a 256 -c _DAG/DAG-003/SOURCE_MANIFEST.sha256`, run in the execution root | **130/130 OK**, exit 0. All 41 `Dependencies.csv`, all 41 `_DEPENDENCIES.md`, all 41 `ScopeOfWork.md` and the decomposition members equal the basis bytes |
| `shasum -a 256 -c MANIFEST.sha256`, run in `_DAG/DAG-002/` (superseded) | **37/37 OK**, exit 0. The history is unchanged |
| `shasum -a 256 -c MANIFEST.sha256`, run in `_DAG/DAG-001/` (superseded) | **61/61 OK**, exit 0. The history is unchanged |

**Inventory.** The accepted decomposition pointer, `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` (sha256 `6ef9c0ba…afabb`, the same bytes DAG-003's source manifest binds), still names GROUP3-20260928T001055Z. The register `canonical/Deliverables.csv` (sha256 `bcdf6f2f…415eb`) is the inventory recorded in DAG-003's `GRAPH_BASIS.md`, and it is unchanged.

## 3. Classification

**`CURRENT`.** No source bytes changed and the inventory is unchanged (currency.md step 3), so no scratch re-assembly is needed. Consumers may rely on DAG-003 within the reliance boundary in its [ACCEPTANCE_RECORD](../../../_DAG/DAG-003/ACCEPTANCE_RECORD.md) and read it as its [HANDOFF_STATE](../../../_DAG/DAG-003/HANDOFF_STATE.md) directs.

## 4. `DAG pending` deliverables

**None.** These 5 flags are cleared by the owner's acceptance of DAG-003:

DEL-01-04, DEL-02-01, DEL-02-03, DEL-03-02 and DEL-03-03.

Their release changes no ready or blocked verdict: the four arcs they gained (N-18, N-21, N-24, X-1) are held inside SCC-002, and DAG-003's admitted layer is DAG-002's. Their blockers are read from that admitted layer, as before.

## 5. Analyzer cross-check

The registered closure analyzer, `tools/coordination/analyze_dep_closure.py` (sha256 `2b8de3cb…a9adc`), was run with the DAG-001/DAG-002/DAG-003 closure arguments and without `--output-dir`, so it wrote nothing. Its stdout is kept in [Evidence/analyzer.stdout.json](Evidence/analyzer.stdout.json).

Its `accepted_dag` section now reports:

- version `DAG-003`;
- result **`NO_DEPARTURE_FOUND`**;
- 0 `DAG pending`;
- no added or removed arcs or deliverables.

This is the result the candidate's `Evidence/successor_currency_precheck.json` predicted in scratch. The prior run against DAG-002 (`CURRENCY_APP_V4_SCA002_2026-09-29_2057`) reported `DEPARTURE` with the same 4 arcs and 5 pending deliverables; that departure is now decided. The whole-graph figures are as at that audit: 41 nodes, 202 arcs (124 admitted and 78 held) and 6 SCCs of sizes 2/13/2/3/2/2. The raw acyclic-objective subject status is still `FAIL` because of the six characterized SCCs, as for DAG-001 and DAG-002. Four hubs at threshold 20: DEL-02-01, DEL-02-03, DEL-04-01 and DEL-04-03, as the handoff records.

This run is a cross-check, not a closure snapshot. `_Evaluation/DepClosure/_LATEST.md` was not moved.

## 6. What follows

- **The next audit is due** when a consumer relies on DAG-003 after the local files may have changed, after any `dependency-extract` run or declaration change, or after an accepted scope change or decomposition revision. The pending SCA-V4-002 and SCA-V4-001 `audit-scope-closure` snapshots read this version and change none of its sources; they are not, by themselves, a reason to audit.
- **Scope of this audit.** It establishes currency only. It does not establish satisfaction, readiness or lifecycle, and it did not modify DAG-001, DAG-002, DAG-003, `_DAG/_LATEST.md` or any local file.
