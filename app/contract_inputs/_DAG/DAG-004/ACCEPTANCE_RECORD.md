# DAG-004 acceptance

**DAG-004 is accepted, on 2026-10-03, as the successor of DAG-003.** The decision covers **project-dag checkpoints 1 and 2** together. No SCC needed a ruling; only the ten added arcs and their consequences were reopened, and everything else carries forward from DAG-003. DAG-003 is superseded and stays unchanged as history in `_DAG/DAG-003/`, as do DAG-002 and DAG-001.

## Custody and provenance

| Item | Value |
|---|---|
| Actor | The owner |
| Date of the act | 2026-10-03 (local time America/Denver) |
| Channel | The owner's chat message to HELP_HUMAN in run `APP-V4-SCA003-20261002`, after HELP_HUMAN presented the candidate, the currency departure and review V25 in chat |
| Transcription | `_Coordination/AgentRuns/APP-V4-SCA003-20261002/OWNER_DECISIONS.md`, **DECISION-3** (checkpoint K3), committed in `ad16b789ec78971ee909de7c7d14c10dfde2d37d` (file sha256 `7f1c49cd469c8224ccd1fae8f3f5afae0405e0f0a27aea991287e73a7131389d`). Custody is that transcription, not a raw platform export |
| This record | Written by node D2 (Type 2 TASK, Claude Code subagent; no delegation) of the same run, from DECISION-3, on 2026-10-03. D2 did not witness the chat; it records the transcription as given |
| Package presented | `DAG_PREP/CHECKPOINT_C.md` (sha256 `710de58450fafb866df8bdb05ba7455e382d66d9235e3ce92b291b583eb45f9b`) and `DAG_PREP/REVIEW_PACKET.md` (sha256 `af4a77d0cde37da704abebc03eac2fae28e9c13f56f25b1a274b95aaf21dcd5b`), committed in `4ca22437f7df6f907a20a083efc5913eff3eff8c`. `DAG_PREP/` is unchanged from that commit to `ad16b789ec` |
| Candidate presented | Staged at `_Coordination/AgentRuns/APP-V4-SCA003-20261002/DAG_PREP/DAG-004/` (the D1 write fence kept it out of `_DAG/`), assembled on the frozen basis `75764184b99ab006cd46c1d1c328cf7d5c4d0c8d` (clean tree). At publication it was copied byte for byte to `_DAG/_Candidates/DAG-004/` (the candidate record) and to this folder |
| Independent review | `reviews/V25.md` (sha256 `b0d5f45e66a37b12743be0ea11b9642716524a36879f81d6c39785b4ace93a9f`, committed in `6358ce132d72dfefdadfd07990846bb0ffd6a63e`): READY FOR CHECKPOINT C, 0 BLOCKING, 0 MAJOR, 4 MINOR (m-1…m-4), 2 observations. Copied here at publication as `INDEPENDENT_REVIEW.md` (V25 m-4) |

## The decision (exact)

> I accept DAG-004.

**Effects as transcribed** (CHECKPOINT_C §8 as recommended, with V25's notes):

1. DAG-004 is accepted as the single successor to DAG-003 for the ten links (project-dag checkpoints 1 and 2 together).
2. The handoff records the four new sequencing waits (DEL-01-04, 02-02, 02-03, 03-03), the route re-examination list (a light check, V25 O-1), X-1's narrow scope, the DEL-09-06 guard, V25 m-1 (the DEL-05-01 → DEL-01-05 representative row is information-only, for the register owners), V25 m-2 (hub growth) and the carried obligations.
3. The integrator moves the staged files to their method homes and writes the pointers at publication. `INDEPENDENT_REVIEW.md` is added at publication (V25 m-4).
4. The DEL-01-03 absolute TargetLocation is repaired after acceptance.

## What was accepted

The 33 files listed in `REVIEW_PACKET.md`, published here byte for byte. Each was verified against the packet hashes before this record was written: 33/33 OK, and the same 33 paths in the staged folder, `_DAG/_Candidates/DAG-004/` and this folder. `MANIFEST.sha256` covers them together with this record, `HANDOFF_STATE.md`, and the copies `REVIEW_PACKET.md` and `INDEPENDENT_REVIEW.md` (the same layout as DAG-002 and DAG-003).

| Account | DAG-003 | DAG-004 |
|---|---:|---:|
| Nodes (GROUP3-20260928T001055Z; `DeliverableNodes.csv` byte-equal to DAG-001…003) | 41 | 41 |
| Admitted arcs (`DependencyEdges.csv`) | 124 | 129 (DAG-003's 124 arcs plus NR-05, NR-07, NR-01, NR-02, NR-04) |
| Held, non-gating candidate arcs (`CandidateEdges.csv`) | 78 | 83 (+ NR-08, NR-09, NR-4, R2-04-03-e, R20-10, all in SCC-002) |
| Excluded rows (`ExcludedRows.csv`) | 263 | 355 |
| ACTIVE EXECUTION rows accounted | 465 | 567 |
| SCCs | 6 | 6, identical member sets |

- Basis: commit `75764184b99ab006cd46c1d1c328cf7d5c4d0c8d`. `SOURCE_MANIFEST.sha256` has sha256 `03aa668b88cb1cb32e1d26a15fb64afdf85e0af6fbb61ec89f833eaf5893a8ef`: 130 entries, the same paths as DAG-001…003, with 59 members changed since DAG-003's basis.
- `audit_dag.py --canonical --strict` exits 0 (`Evidence/dag_audit.json`, `Evidence/Tool_Run.json`); V25 reproduced it independently.
- Departures decided: the 10 arcs added against DAG-003 by currency audit `_Evaluation/DAGCurrency/CURRENCY_APP_V4_SCA003_2026-10-03_1937` (`Evidence/DepartureAccount.csv`), accepted as one successor. No arc was removed and no existing arc changed layer. Seven existing arcs changed representative under SR-6 (`Evidence/MirrorAssessment.md`).

**Presented bytes.** The copied files keep their presentation-time wording:

- `GRAPH_BASIS.md`, `ASSEMBLY_RUN.md` and `SOURCE_BASIS.json` still describe an unaccepted, unreviewed candidate staged in `DAG_PREP/`, and cite the closure and currency snapshots at their staged paths.
- `PROPOSED_LATEST.md` still carries the `{ACCEPT_DATE}` token.

Those passages describe their standing when written. This record establishes the acceptance, and V25 is the review they awaited. The two snapshots now also sit, byte-identical, at `_Evaluation/DepClosure/CLOSURE_APP_V4_SCA003_2026-10-03_1936/` and `_Evaluation/DAGCurrency/CURRENCY_APP_V4_SCA003_2026-10-03_1937/`. The accepted pointer, `_DAG/_LATEST.md`, was written from `PROPOSED_LATEST.md` with `{ACCEPT_DATE}` = 2026-10-03.

## Qualifications carried from DAG-003

These stand unchanged and were presented as carried forward, not re-decided (CHECKPOINT_C §3):

- **Completeness:** `FULL` for the selected semantics under `FULL_GRAPH` tracking, with the explicit unresolved-input and candidate qualifications. 41 deliverables, no exemptions.
- **Semantics and direction:** the consumer requires the supplier's stated contribution, at the stated maturity or condition, before the stated part of its own work. It does not mean whole-deliverable completion. Direction is consumer → supplier.
- **Selection rules:** SR-1…SR-7 as confirmed for DAG-001: every canonical DependencyType admitted; no cut or merge ruling; no confirmation hold; one representative per arc; every intra-SCC representative held.
- **SCCs:** the six characterized SCCs remain unresolved and held as non-gating candidates, each citing its continuing case (CASE-001; CASE-002, with CASE-004 as history; CASE-003; CASE-005; CASE-006; CASE-007). No case opens or closes. CASE-002's evidence update for the five held arcs is drafted (`DAG_PREP/CASE-002_EVIDENCE_UPDATE.proposed.md`) and goes through `scc-resolution-case` separately; this version cites the case by reference only.
- **Maturity:** `INITIALIZED` is defined-contract maturity only. The graph promotes no `SatisfactionStatus` and no `RequiredMaturity`.
- **Obligations outside the representative:** MIRROR and SAME_ARC rows, and non-topological inputs, keep their own obligations, read from the live registers.
- **DEL-01-01 as supplier and DEL-09-06 as consumer**, with the DEL-09-06 reverse-arc guard as a standing note. The guard held.
- **Tool strictness:** no strictness exception is taken.

## Reliance boundary

**While DAG-004 is current**, as established by a currency audit, it may be relied on for:

- sequencing and route selection within the App v4 project;
- dependency-based blocker verdicts, read from its admitted edges. Required contributions and satisfaction are read from the live local registers.

New with DAG-004: **DEL-01-04, DEL-02-02, DEL-02-03 and DEL-03-03 read admitted blockers from DEL-01-03 and DEL-01-05, or from DEL-01-02, for the stated parts of their work only** (`HANDOFF_STATE.md`). Candidate edges, including the five added here, are non-gating. They cannot drive blocker queues, waves, schedules, dispatch readiness or readiness claims, and holding one makes no work ready.

**This acceptance does not:**

- satisfy any dependency or promote any satisfaction or maturity value;
- change any deliverable's lifecycle state (SCA-V4-003 Q-13 was a separate act);
- lift any hold;
- pass, or count toward, any gate;
- set a schedule or a dispatch order;
- close an SCC, rule on a cut or merge, or resolve an open issue;
- close SCA-V4-003 or its predecessors; their `audit-scope-closure` snapshots are separate acts;
- repair the DEL-01-03 absolute TargetLocation. Effect 4 routes that to the register owner after acceptance.

**The acceptance clears the flag on 11 deliverables** that `CURRENCY_APP_V4_SCA003_2026-10-03_1937` listed as `DAG pending`: DEL-01-02, DEL-01-03, DEL-01-04, DEL-01-05, DEL-02-01, DEL-02-02, DEL-02-03, DEL-02-04, DEL-03-03, DEL-04-02 and DEL-04-03. A follow-up currency audit records the clearance (`_Evaluation/DAGCurrency/_LATEST.md`).

**Currency conditions reliance.** DAG-004 carries authority only through this record and only while it is current with the local evidence (SPEC §5.4, D-GOV-49). A later departure makes the affected deliverables `DAG pending` until the owner decides. The repair of DEL-01-03's TargetLocation will change bytes that this version binds. The audit after that repair is expected to read `CURRENT_WITH_EVIDENCE_DRIFT`, not `DEPARTURE`, if no arc changes. See `HANDOFF_STATE.md`.
