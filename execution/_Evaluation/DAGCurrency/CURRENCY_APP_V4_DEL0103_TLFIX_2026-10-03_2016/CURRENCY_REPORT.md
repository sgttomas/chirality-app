# DAG-004 currency audit — APP_V4_DEL0103_TLFIX

**Result: `CURRENT_WITH_EVIDENCE_DRIFT`.** Two source files changed since DAG-004's basis. Both belong to DEL-01-03's register. The admitted and candidate arc sets, the SCCs, the representatives and the inventory are unchanged. **No deliverable is `DAG pending`.** Consumers keep relying on DAG-004 for blockers.

- **Trigger:** the accepted repair of DEL-01-03's absolute TargetLocation values (`_Coordination/AgentRuns/APP-V4-SCA003-20261002/OWNER_DECISIONS.md`, DECISION-3 effect 4). The repair ran through `dependency-extract` UPDATE (record `_run_records/dependency-extract-20261004-fx.md` in DEL-01-03). DAG-004's `HANDOFF_STATE.md` ("When to audit") calls for an audit after such a run.
- **Audit:** `project-dag` `resources/currency.md`, run `APP-V4-SCA003-20261002`, node FX, 2026-10-03 20:16 MDT.
- **Snapshot:** `CURRENCY_APP_V4_DEL0103_TLFIX_2026-10-03_2016`. `_Evaluation/DAGCurrency/_LATEST.md` now points here. The previous audit, `CURRENCY_APP_V4_DAG004_ACCEPTED_2026-10-03_2012` (`CURRENT`), is now history.
- **Commands, exit codes and hashes:** [Tool_Run.json](Tool_Run.json). The outputs are in `Evidence/`.

## 1. The accepted version

`_DAG/_LATEST.md` (sha256 `b9353a41…f55d4ca2d`, unchanged) is in SPEC §11.2 form. The registered parser reads `Latest: DAG-004`. `resolve_accepted_dag` loads `_DAG/DAG-004/` with 41 nodes, 129 admitted, 83 candidate and 355 excluded rows ([Evidence/pointer_check.json](Evidence/pointer_check.json)). No candidate folder has a `REJECTION_RECORD.md`, so there is no rejected departure to report.

## 2. Manifest checks

| Check | Result |
|---|---|
| `shasum -a 256 -c MANIFEST.sha256`, run in `_DAG/DAG-004/` | **37/37 OK**, exit 0 |
| `shasum -a 256 -c _DAG/DAG-004/SOURCE_MANIFEST.sha256`, run in the execution root | **128/130 OK**, exit 1. The two FAILED members are DEL-01-03's `Dependencies.csv` and `_DEPENDENCIES.md` |
| `MANIFEST.sha256` in `_DAG/DAG-003/`, `DAG-002/` and `DAG-001/` (superseded) | **37/37, 37/37 and 61/61 OK**, exit 0 |

**Inventory.** `_Decomposition/checkpoint_snapshots/_LATEST_ACCEPTED.md` (sha256 `6ef9c0ba…afabb`, the bytes the source manifest binds) still names GROUP3-20260928T001055Z. Its `canonical/Deliverables.csv` is unchanged.

## 3. What changed

| File | Change |
|---|---|
| DEL-01-03 `Dependencies.csv` | TargetLocation in DEP-01-03-001…014 only. The prefix `/Users/…/.codex/worktrees/077c/chirality/` was removed, which leaves the `projects/chirality-app-v4/execution/…` form the other 40 registers use. No other cell changed; LastSeen was not refreshed, by brief |
| DEL-01-03 `_DEPENDENCIES.md` | One Run History entry appended |

## 4. Scratch re-application (currency.md step 4)

[Evidence/reapply_selection.py](Evidence/reapply_selection.py) re-applies SR-1…SR-7 to the live registers as a scratch assembly. It is adapted from the SCA003 audit's script, with DAG-004 as the comparison base. The result is in [Evidence/reapplication_result.json](Evidence/reapplication_result.json):

- 567 ACTIVE EXECUTION rows: 359 with deliverable targets and 208 non-topological;
- **212 arcs: 129 admitted and 83 candidate.** Against DAG-004: 0 added, 0 removed, 0 layer changes;
- **6 SCCs**, the same member sets as DAG-004;
- **0 representative changes;**
- **drift on existing representatives:** `TargetLocation` only, on DEP-01-03-011 (DEL-01-03 → DEL-01-01) and DEP-01-03-012 (DEL-01-03 → DEL-01-02). Both are admitted. DAG-004's `DependencyEdges.csv` keeps the former absolute value, as the handoff says;
- **rows outside the arc representatives:** DEP-01-03-013 (MIRROR) and DEP-01-03-014 (NOT_TOPOLOGICAL) changed in the same field. The ten ANCHOR rows (001…010) are not graph rows;
- **strict audit** of the scratch edges (`tools/coordination/audit_dag.py --canonical`): exit 0, 0 findings, 212 edges, 6 SCCs.

**Guards** carried in DAG-004's `HANDOFF_STATE.md` still hold:

- R17-10: DEL-01-02 reaches DEL-01-01, 01-05 and 04-01; DEL-01-03 reaches those and DEL-01-02;
- DEL-04-01 has no supplier;
- no tested guard arc is present (N-12, N-B8, NR-03, NR-06, NR-10, E-1, K-11, E-5, K-7, K-6);
- DEL-09-06 reaches the same 20 deliverables and is consumed only by DEL-03-04 and DEL-09-07.

## 5. Classification

**`CURRENT_WITH_EVIDENCE_DRIFT`** (currency.md table). Bytes changed, but the admitted and candidate arc sets, the SCCs and the inventory did not. No successor is needed.

- Rely on DAG-004 for blockers.
- Read the changed field, TargetLocation, from the live DEL-01-03 register.
- DAG-004's copies of DEP-01-03-011 and -012 (and its evidence copies of -013 and -014) keep the former absolute value. They are accepted history and are not edited.

## 6. `DAG pending` deliverables

**None.**

## 7. Analyzer cross-check

The registered closure analyzer `tools/coordination/analyze_dep_closure.py` (sha256 `2b8de3cb…a9adc`) was run with the project closure arguments and without `--output-dir`, so it wrote nothing.

- **Accepted-DAG comparison:** `accepted_dag` reports DAG-004, **`NO_DEPARTURE_FOUND`**, 0 `DAG pending`, and no added or removed arcs or deliverables.
- **Whole graph:** 41 nodes, 212 arcs, 6 SCCs (sizes 2/13/2/3/2/2), 4 hubs at threshold 20. The raw acyclic-objective subject status is `FAIL` on the six characterized SCCs, as for every version.
- **Output unchanged:** before redaction, its stdout was byte-identical to the previous audit's (sha256 `d54b2ae7…960601d`). The analyzer does not read TargetLocation.
- **Redaction:** the kept [Evidence/analyzer.stdout.json](Evidence/analyzer.stdout.json) has `<repository root>/` in place of the absolute repository root in `accepted_dag.path` and `accepted_dag.pointer`. No other byte changed. The raw hash is in Tool_Run.json.

## 8. Scope

- **What it establishes:** currency only. It does not establish satisfaction, readiness or lifecycle.
- **What it did not modify:** DAG-001…004, `_DAG/_LATEST.md`, any case or any local file.
- **When the next audit is due:** the triggers in DAG-004's `HANDOFF_STATE.md`.
