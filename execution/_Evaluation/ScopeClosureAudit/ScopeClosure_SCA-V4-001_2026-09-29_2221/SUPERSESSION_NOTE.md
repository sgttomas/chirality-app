# Supersession note

**This snapshot supersedes** `_Evaluation/ScopeClosureAudit/ScopeClosure_SCA-V4-001_2026-09-29_1222/`
(node CA1, run `APP-V4-SCA002-20260929`, committed at `f5b5d0ad0`; verdict `OPEN`).

The superseded snapshot's bytes are unchanged. Its files hash as follows at
the time of this write:

| File | sha256 |
|---|---|
| `Brief.md` | `77ae8d856340db13c87974a4aea06e8bb5fd188c0ad360bb72138fe4fbc3144b` |
| `Expected_Supersession_Map.csv` | `e8e433208bce44faf3f65d43b31e48b1a3476d4d6afec554a4e5319d9ef1a801` |
| `INPUT_MANIFEST.sha256` | `769933dcb1fa6ddf3260153170c3b73278b64d866102f2d9b62cf5fba2a63a7f` |
| `QA_Report.md` | `527c2b402bb21bb274310f60965aadd0df363dc405efa209ee1c622b989430d9` |
| `Scope_Closure_IssueLog.csv` | `9fbfaa310c37615da57377349cbee525a20351c60f5f3b707537a870be42b973` |
| `Scope_Closure_Report.md` | `50b6e0437694844f5e23b38434096a7aee24d9b531749d974163ac59e4203e76` |
| `Supersession_Map_Findings.csv` | `c7312589902ad10316506093e0c700e5dcc7ec93cf66673c6233a2de073e79a1` |
| `scope_closure_summary.json` | `1093cf2162ee838102361ba602711aadfaef310fc26f6f9557f692d4be8f0dd4` |

`_LATEST.md` (previous bytes `1c3a8734a056a93b337621e7f9bc203f2162e73b7351dc0d87fd7617798bd7f4`)
moves to this snapshot.

## Reason

The CA1 verdict was `OPEN` on one determinant, ASC-ISS-001 (11 register
actions with `SupersessionBindingPresent = YES` and no `D-{ActionSeq}` row;
CRITICAL from the method table, `Assessment: UNKNOWN`, flagged for human
triage). The owner has since ruled it (option a) and SCA-V4-002 has been
accepted with the path-level rows. The other CA1 findings have been acted on
or their dispositions confirmed. The CA1 input manifest no longer matches the
tree (48 of 389 inputs changed), so a rerun was required in any case.

## What changed in inputs and evidence binding

**Owner acts and records (new since CA1):**
- `OWNER_DECISIONS.md` DECISION-2 (checkpoint A, SCA-V4-002 groups 1–2:
  "accept the remaining items as recommended"; Q-10 = ASC-ISS-001 option (a),
  Q-11 = DEL-04-01 qualifier, Q-12 = reading-rule notes, Q-13 = effective-state
  record, Q-15 = DECISION-8 confirmed as the Design re-pin deferral record).
- DECISION-3 (checkpoint B, SCA-V4-002 group 3 accepted; "ASC-ISS-001 closes
  on this acceptance, to be confirmed by a superseding audit-scope-closure
  snapshot for SCA-V4-001").
- DECISION-4 (checkpoint C, DAG-003 accepted).
- `_ScopeChange/_PostAcceptanceValidation/SCA-V4-001_20260930T010520Z_EFFECTIVE_STATE/EFFECTIVE_STATE.md`
  (sha256 `80096fe5…44d0`), the ASC-ISS-003 record.
- `_ScopeChange/SCA-V4-002_2026-09-29_1901/` with its three checkpoint
  snapshots and `_PostAcceptanceValidation/SCA-V4-002_20260930T021014Z/`.

**Supersession binding:** `SCA-V4-002/Supersession_Delta.csv`
(`8c3f1a55…3b8`) adds 17 `DL-SCA-V4-001-A{18..25,36,42,46}` rows and D-014;
`SCA-V4-002/Supersession_Map.csv` (`45502bf5…eb93`, 29 rows) is accumulated
from SCA-V4-001's map (`e8e43320…a801`, unchanged).

**Changed inputs (48 of the CA1 manifest's 389):** `docs/HOST_INTEGRATION.md`
(A17b line join); `SOFTWARE_DECOMP.md` (SCA-V4-002 Decision Log entry);
`Deliverables.csv` (DEL-04-01); `Open_Issues.csv` (OI-012 pointer);
`Consolidated_Coverage.csv` (31-row recompute); `_Decomposition/_LATEST.md`
and `checkpoint_snapshots/_LATEST_ACCEPTED.md` (reading-rule notes); five
`_CONTEXT.md` (four reading-rule lines plus DEL-04-01's qualifier and line);
9 `ScopeOfWork.md` (SCA-V4-002 REVISEs, of which 6 are SCA-V4-001 targets:
DEL-01-01, 02-01, 02-03, 03-03, 04-02, 09-07); 11 `Dependencies.csv` and
`_DEPENDENCIES.md` (SCA-V4-002 UPDATE, including the DEL-04-01/02/03
re-quoting and DEP-09-07-016); `_ScopeChange/_LATEST.md`,
`_Evaluation/DAGCurrency/_LATEST.md`, `_Evaluation/DepClosure/_LATEST.md`,
`_DAG/_LATEST.md` (DAG-003); `OWNER_DECISIONS.md` and `DISPATCH.md` of this run.
The SCA-V4-001 amendment snapshot, its three checkpoint snapshots, its first
post-acceptance validation record, the four `AMENDMENT_PACKET` files of run
`APP-V4-BASIS-ALIGN-20260928`, DAG-001 and DAG-002 are byte-unchanged.

**Evidence binding of the reruns.** The SCA-V4-001 results are re-verified at
their own commits from git (`102f09c1a` for the state CA1 saw), and the chain
to the current bytes is verified through SCA-V4-002's RV returns
(`PRIOR_CONTRACT_SHA256` equal to the SCA-V4-001 result hash) and the
`dependency-extract-20260929-sca002.md` run records.

**DAG state bound.** At the start of this node (`b99df0989`) `_DAG/_LATEST.md`
read `Latest: DAG-002` with the currency observation `DEPARTURE` (5 DAG
pending). Commit `a254be160` published DAG-003 during the run; this snapshot
binds that later state (`Latest: DAG-003`; currency `CURRENT`, no DAG pending).
