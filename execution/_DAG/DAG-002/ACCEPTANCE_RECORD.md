# DAG-002 acceptance

**DAG-002 is accepted, on 2026-09-29, as the successor of DAG-001.** The decision covers **project-dag checkpoints 1 and 2** together (method: a small successor with no SCC needing a ruling). DAG-001 is superseded and stays unchanged as history in `_DAG/DAG-001/`.

## Custody and provenance

| Item | Value |
|---|---|
| Actor | The owner, Ryan |
| Date of the act | 2026-09-29 |
| Channel | The owner's answers to a structured question in the active chat of run `APP-V4-BASIS-ALIGN-20260928` |
| Transcription | By the run's recorder into `_Coordination/AgentRuns/APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md`, **DECISION-10**, committed in `87813431d364aad8800ad44aea58d50ac0d8a2e0` (file sha256 `7a1e0f1c537124fa58efbb104250160d3c7e50609162df0cfdbcbdcf1eac1f58`). Custody is that transcription, not a raw platform export |
| This record | Written by node D2 (Type 2 TASK, Claude Code subagent; no delegation) of the same run, from DECISION-10, on 2026-09-29. D2 did not witness the chat; it records the transcription as given |
| Package presented | `DAG_PREP/CHECKPOINT_C.md` (sha256 `6ff6dd965779d1e155ce33f6a30c89b61a74d0dc8f29ec4a2798372d7b21290c`) and `DAG_PREP/REVIEW_PACKET.md` (sha256 `0ebfb5f40b0491069839a3d5c1602d4e211b99fbcd44dd1a18db0d401f826475`), at commit `5f03b77967f67e82c72459964596a130181f8c16`. Both are unchanged from that commit to `87813431d` |
| Candidate presented | `_DAG/_Candidates/DAG-002/`, assembled at commit `e9dc4633b693cd8e3308a3aaa71b901262829ebb` on the frozen basis `b585e5ebead38f8ece442c80cd3bec5be8363cf3` |
| Independent review | `reviews/V12.md` (sha256 `8bc4f9412c4ad223e8227d83a200fa2ea585cdff10341ea5087bec9e450861e8`): READY FOR CHECKPOINT C, 0 BLOCKING, 3 MINOR, 6 NOTE. Copied here as `INDEPENDENT_REVIEW.md` |

## The questions and the owner's answers (exact labels)

| Question presented | Owner's answer (exact label) |
|---|---|
| Checkpoint C: accept DAG-002 (37 added arcs: 15 admitted, 22 held; six cycles unchanged; strict audit passes; review nothing blocking; releases 15 DAG-pending deliverables). Decides both project-dag checkpoints together. | "Accept DAG-002 (Recommended)" |
| Four accepted arcs not produced (N-18, N-21, N-24, X-1): how to handle? | "A: add wording in SCA-V4-002 (Recommended)" |

As transcribed, the owner then interrupted the turn and, in a new message, said "continue". Nothing had been written in between.

## What was accepted

The 33 files listed in `REVIEW_PACKET.md`, published here byte for byte. Every one was verified against the packet hashes before this record was written (33/33 OK; `shasum -a 256 -c` exit 0). `MANIFEST.sha256` covers them together with this record, `HANDOFF_STATE.md`, and the copies `REVIEW_PACKET.md` and `INDEPENDENT_REVIEW.md` (the contract's snapshot layout lists both).

| Account | DAG-001 | DAG-002 |
|---|---:|---:|
| Nodes (GROUP3-20260928T001055Z; `DeliverableNodes.csv` byte-equal) | 41 | 41 |
| Admitted arcs (`DependencyEdges.csv`) | 109 | 124 |
| Held, non-gating candidate arcs (`CandidateEdges.csv`) | 52 | 74 |
| Excluded rows (`ExcludedRows.csv`) | 242 | 264 |
| ACTIVE EXECUTION rows accounted | 403 | 462 |
| SCCs | 6 | 6, identical member sets |

- Basis: commit `b585e5ebead38f8ece442c80cd3bec5be8363cf3`; `SOURCE_MANIFEST.sha256` sha256 `6d1021f1c78fea023c2089aa29a2bc60f5ae498f56068eeddbfa376467793250` (130 entries).
- `audit_dag.py --canonical --strict` exit 0 (`Evidence/dag_audit.json`, `Evidence/Tool_Run.json`).
- Departures decided: the 37 arcs added against DAG-001 by currency audit `CURRENCY_APP_V4_BASISALIGN_2026-09-29_0856` (`Evidence/DepartureAccount.csv`), accepted as one successor. No arc was removed; no existing arc changed layer.

**Presented bytes.** The copied files keep their presentation-time wording and relative links. `GRAPH_BASIS.md` still says it is an unaccepted, not yet reviewed candidate, and `PROPOSED_LATEST.md` still carries the `{ACCEPT_DATE}` token. Those passages describe their standing when written; this record establishes the acceptance. The relative links resolve from `_DAG/_Candidates/DAG-002/`, which is kept as the candidate record. The accepted pointer written from `PROPOSED_LATEST.md` is `_DAG/_LATEST.md`, with `{ACCEPT_DATE}` = 2026-09-29.

## Qualifications carried from DAG-001

These stand unchanged. The departure did not touch their rows, arcs or warrants, and they were presented as carried forward, not re-decided (CHECKPOINT_C §3):

- **Completeness:** `FULL` for the selected semantics under `FULL_GRAPH` tracking, with the explicit unresolved-input and candidate qualifications. 41 deliverables, no exemptions.
- **Semantics and direction:** the consumer requires the supplier's stated contribution, at the stated maturity or condition, before the stated part of its own work. It does not mean whole-deliverable completion. Direction is consumer → supplier.
- **Selection rules:** SR-1…SR-7 as confirmed for DAG-001: every canonical DependencyType admitted; no cut or merge ruling; no confirmation hold; one representative per arc; every intra-SCC representative held.
- **SCCs:** the six characterized SCCs remain unresolved, held as non-gating candidates, each citing its continuing case (CASE-001; CASE-002, with CASE-004 as history; CASE-003; CASE-005; CASE-006; CASE-007). No case opens or closes. A missing input constrains the work that needs it, not every member of an SCC.
- **Maturity:** `INITIALIZED` is defined-contract maturity only. The graph promotes no `SatisfactionStatus` and no `RequiredMaturity`.
- **Obligations outside the representative:** MIRROR and SAME_ARC rows, and non-topological inputs, keep their own obligations. They are read from the live registers.
- **Tool strictness:** no strictness exception is taken.

## Disposition of the four arcs not produced (option A)

N-18 (DEL-02-01 → DEL-03-02), N-21 (DEL-02-03 → DEL-03-02), N-24 (DEL-02-03 → DEL-03-03) and X-1 (DEL-02-03 → DEL-01-04) were accepted at checkpoint A (DECISION-6), but no register row carries them. Under the owner's answer "A: add wording in SCA-V4-002 (Recommended)":

- **They are not in DAG-002.** The graph copies register rows and creates none.
- **They are routed to SCA-V4-002.** DECISION-10 widens that follow-on amendment to add "consumes" sentences, where the dependency is real, to the DEL-02-01 and DEL-02-03 SoWs for these four arcs.
- **Later rows are a new departure.** Rows extracted after that amendment will be reported by a later currency audit as a small departure, for a later successor. Until then nothing is held on their account.
- **DEL-01-04 is not DAG pending.** X-1 is in no register, so DEL-01-04 is not an endpoint of a changed arc.
- **No verdict changes.** All four would sit, held and non-gating, inside the unchanged SCC-002.

## Reliance boundary

**While DAG-002 is current**, as established by a currency audit, it may be relied on for:

- sequencing and route selection within the App v4 project;
- dependency-based blocker verdicts, read from its admitted edges. Required contributions and satisfaction are read from the live local registers.

That includes the new admitted supply through DEL-01-01 to six deliverables (C2-3) and DEL-09-06 as a consumer of eight (C2-4). Its candidate edges are non-gating. They cannot drive blocker queues, waves, schedules, dispatch readiness or readiness claims, and holding one makes no work ready.

**This acceptance does not:**

- satisfy any dependency or promote any satisfaction or maturity value;
- change any deliverable's lifecycle state;
- lift any hold;
- pass, or count toward, any gate, including the 30% gate (completed earlier under DAG-001) and the 60% gate;
- set a schedule or a dispatch order;
- close an SCC, rule on a cut or merge, or resolve an open issue;
- apply SCA-V4-002 or any other scope change.

Each of these remains a separate act, by its own owner and method.

**The acceptance clears the flag on 15 deliverables.** They were listed `DAG pending` by `CURRENCY_APP_V4_BASISALIGN_2026-09-29_0856`: DEL-01-01, DEL-02-01, DEL-02-02, DEL-02-03, DEL-03-01, DEL-03-02, DEL-03-03, DEL-03-04, DEL-04-01, DEL-04-02, DEL-04-03, DEL-05-01, DEL-05-02, DEL-09-06 and DEL-09-09. A follow-up currency audit records the clearance (`_Evaluation/DAGCurrency/_LATEST.md`).

**Currency conditions reliance.** DAG-002 carries authority only through this record and only while it is current with the local evidence (SPEC §5.4, D-GOV-49). A later departure makes the affected deliverables `DAG pending` until the owner decides. See `HANDOFF_STATE.md`.
