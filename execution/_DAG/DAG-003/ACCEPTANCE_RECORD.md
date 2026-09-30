# DAG-003 acceptance

**DAG-003 is accepted, on 2026-09-29, as the successor of DAG-002.** The decision covers **project-dag checkpoints 1 and 2** together (method: a small successor with no SCC needing a ruling; only the four held arcs were reopened, everything else carries forward from DAG-002). DAG-002 is superseded and stays unchanged as history in `_DAG/DAG-002/`, as does DAG-001 in `_DAG/DAG-001/`.

## Custody and provenance

| Item | Value |
|---|---|
| Actor | The owner, Ryan |
| Date of the act | 2026-09-29 |
| Channel | The owner's answer to a structured question in the active chat of run `APP-V4-SCA002-20260929` |
| Transcription | By the run's recorder into `_Coordination/AgentRuns/APP-V4-SCA002-20260929/OWNER_DECISIONS.md`, **DECISION-4**, committed in `b99df098946d7877e2bef55ced21a7b707a9213f` (file sha256 `36ffcbbea923504581844456751c2eb3db617b5471a3595e63f036bf0634b480`). Custody is that transcription, not a raw platform export |
| This record | Written by node D2 (Type 2 TASK, Claude Code subagent; no delegation) of the same run, from DECISION-4, on 2026-09-29. D2 did not witness the chat; it records the transcription as given |
| Package presented | `DAG_PREP/CHECKPOINT_C.md` (sha256 `f8f63e80cdb46e62ca35d25fbd527589c55dba4da95d8410692abfce664061b9`) and `DAG_PREP/REVIEW_PACKET.md` (sha256 `6536ef45b2ca73f396521086b39dfa4b1648fc951e18ba7faaccd47776544481`), at commit `b547125dbe87f5890f70cb1b6d4f0650f5db0b6e`. Both are unchanged from that commit to `b99df0989` |
| Candidate presented | `_DAG/_Candidates/DAG-003/`, assembled on the frozen basis `8cd783d8d7493fbfe663fb108449e4ceda04a00b` (clean tree) and committed in `b547125dbe87f5890f70cb1b6d4f0650f5db0b6e` |
| Independent review | `reviews/V15.md` (sha256 `641efdd3f37521884956ecc0c9444851efc2c0d766128da60801f2108aaa7983`, committed in `e995b329d69424f25a65f7a679166d95ff4c8759`): READY FOR CHECKPOINT C, 0 BLOCKING, 5 non-blocking observations (O-1…O-5). Copied here as `INDEPENDENT_REVIEW.md` (V15 O-3) |

## The question and the owner's answer (exact label)

| Question presented | Owner's answer (exact label) |
|---|---|
| Checkpoint C: accept DAG-003 (four held arcs N-18, N-21, N-24, X-1 added; admitted layer and six cycles unchanged; strict audit passes; review nothing blocking; releases 5 DAG-pending deliverables). Decides both project-dag checkpoints together. | "Accept DAG-003 (Recommended)" |

## What was accepted

The 33 files listed in `REVIEW_PACKET.md`, published here byte for byte. Every one was verified against the packet hashes before this record was written (33/33 OK; the candidate folder, the packet and this folder hold the same 33 paths, and every hash is equal). `MANIFEST.sha256` covers them together with this record, `HANDOFF_STATE.md`, and the copies `REVIEW_PACKET.md` and `INDEPENDENT_REVIEW.md` (the contract's snapshot layout lists both; the same layout as DAG-002).

| Account | DAG-002 | DAG-003 |
|---|---:|---:|
| Nodes (GROUP3-20260928T001055Z; `DeliverableNodes.csv` byte-equal to DAG-001's and DAG-002's) | 41 | 41 |
| Admitted arcs (`DependencyEdges.csv`) | 124 | 124, the same arc set and the same 124 representative rows |
| Held, non-gating candidate arcs (`CandidateEdges.csv`) | 74 | 78 |
| Excluded rows (`ExcludedRows.csv`) | 264 | 263 |
| ACTIVE EXECUTION rows accounted | 462 | 465 |
| SCCs | 6 | 6, identical member sets |

- Basis: commit `8cd783d8d7493fbfe663fb108449e4ceda04a00b`; `SOURCE_MANIFEST.sha256` sha256 `d0fc611d95ee80ba64b86ea5b0eaa1a1ba90e85e461fb18459dd8162df6a40c5` (130 entries, the same paths as DAG-001 and DAG-002; 32 members changed since DAG-002's basis).
- `audit_dag.py --canonical --strict` exit 0 (`Evidence/dag_audit.json`, `Evidence/Tool_Run.json`).
- Departures decided: the 4 held arcs added against DAG-002 by currency audit `CURRENCY_APP_V4_SCA002_2026-09-29_2057` (`Evidence/DepartureAccount.csv`), accepted as one successor. No arc was removed; no admitted arc was added; no existing arc changed layer or representative.

**Presented bytes.** The copied files keep their presentation-time wording and relative links. `GRAPH_BASIS.md` still says it is an unaccepted candidate not yet independently reviewed, `ASSEMBLY_RUN.md` still lists the review and publication as not done, `SOURCE_BASIS.json` still records the standing as an unaccepted candidate, and `PROPOSED_LATEST.md` still carries the `{ACCEPT_DATE}` token. Those passages describe their standing when written; this record establishes the acceptance, and V15 is the review they awaited. The relative links resolve from `_DAG/_Candidates/DAG-003/`, which is kept as the candidate record. The accepted pointer written from `PROPOSED_LATEST.md` is `_DAG/_LATEST.md`, with `{ACCEPT_DATE}` = 2026-09-29.

## Qualifications carried from DAG-002

These stand unchanged. The departure did not touch their rows, arcs or warrants, and they were presented as carried forward, not re-decided (CHECKPOINT_C §3; DAG-002's ACCEPTANCE_RECORD "Qualifications carried from DAG-001"):

- **Completeness:** `FULL` for the selected semantics under `FULL_GRAPH` tracking, with the explicit unresolved-input and candidate qualifications. 41 deliverables, no exemptions. The inventory pointer `_LATEST_ACCEPTED.md` changed bytes (the B-06a reading-rule note) but names the same GROUP3 snapshot; that is evidence drift bound by this version's manifest, not an inventory change.
- **Semantics and direction:** the consumer requires the supplier's stated contribution, at the stated maturity or condition, before the stated part of its own work. It does not mean whole-deliverable completion. Direction is consumer → supplier.
- **Selection rules:** SR-1…SR-7 as confirmed for DAG-001 and carried by DAG-002: every canonical DependencyType admitted; no cut or merge ruling; no confirmation hold; one representative per arc; every intra-SCC representative held.
- **SCCs:** the six characterized SCCs remain unresolved, held as non-gating candidates, each citing its continuing case (CASE-001; CASE-002, with CASE-004 as history; CASE-003; CASE-005; CASE-006; CASE-007). No case opens or closes; CASE-002 gained the four arcs as evidence only. A missing input constrains the work that needs it, not every member of an SCC.
- **Maturity:** `INITIALIZED` is defined-contract maturity only. The graph promotes no `SatisfactionStatus` and no `RequiredMaturity`.
- **Obligations outside the representative:** MIRROR and SAME_ARC rows, and non-topological inputs, keep their own obligations. They are read from the live registers.
- **DEL-01-01 as supplier and DEL-09-06 as consumer** (DAG-002 C2-3 and C2-4), with the DEL-09-06 reverse-arc guard as a standing note. The guard held: no reverse row appeared.
- **Tool strictness:** no strictness exception is taken.

## The four arcs now in the held layer

DAG-002's acceptance recorded N-18, N-21, N-24 and X-1 as accepted at its checkpoint A but produced by no register row, and routed them to SCA-V4-002 under the owner's option A. SCA-V4-002 (DECISION-2, Q-4 "Keep all four"; DECISION-3) supplied the "consumes" sentences, `dependency-extract` extracted one consumer-side row each, and currency audit `CURRENCY_APP_V4_SCA002_2026-09-29_2057` reported them as the departure. This acceptance decides that departure:

| Arc | Consumer → supplier | Representative | Layer |
|---|---|---|---|
| N-18 | DEL-02-01 → DEL-03-02 | DEP-02-01-029 (INITIALIZED / PENDING) | held, SCC-002; reciprocal with N-B3 (DEP-03-02-027) |
| N-21 | DEL-02-03 → DEL-03-02 | DEP-02-03-025 (INITIALIZED / TBD) | held, SCC-002 |
| N-24 | DEL-02-03 → DEL-03-03 | DEP-02-03-026 (INITIALIZED / TBD) | held, SCC-002; reciprocal with N-27 (DEP-03-03-014) |
| X-1 | DEL-02-03 → DEL-01-04 | DEP-02-03-027 (INITIALIZED / TBD) | held, SCC-002; narrow scope (the App-side positive capture fixtures only) |

- **All four sit inside the unchanged 13-member SCC-002** and are held under SR-7, citing SCC-CASE-002. They are non-gating.
- **No verdict changes.** The admitted layer is byte-for-byte DAG-002's arc set, so acceptance changes no ready or blocked verdict for any deliverable. It records the four contributions as live obligations inside CASE-002, read from the registers.
- **The reciprocal pairs are two arcs each, not mirrors:** each direction carries a different contribution.
- **N-12 and N-B8 remain absent** by the predecessor's DECISION-6, a register-level decision and not an SR-4 cut.

## Reliance boundary

**While DAG-003 is current**, as established by a currency audit, it may be relied on for:

- sequencing and route selection within the App v4 project;
- dependency-based blocker verdicts, read from its admitted edges. Required contributions and satisfaction are read from the live local registers.

That includes, unchanged from DAG-002, the admitted supply through DEL-01-01 to six deliverables and DEL-09-06 as a consumer of eight. Its candidate edges, including the four added here, are non-gating. They cannot drive blocker queues, waves, schedules, dispatch readiness or readiness claims, and holding one makes no work ready. In particular, holding X-1 does not make DEL-02-03's App-side positive capture fixtures ready; they wait for DEL-01-04, a later undertaking.

**This acceptance does not:**

- satisfy any dependency or promote any satisfaction or maturity value;
- change any deliverable's lifecycle state;
- lift any hold;
- pass, or count toward, any gate, including the 30% gate (completed earlier under DAG-001) and the 60% gate;
- set a schedule or a dispatch order;
- close an SCC, rule on a cut or merge, or resolve an open issue;
- close SCA-V4-002 or SCA-V4-001; their `audit-scope-closure` snapshots are separate acts.

Each of these remains a separate act, by its own owner and method.

**The acceptance clears the flag on 5 deliverables.** They were listed `DAG pending` by `CURRENCY_APP_V4_SCA002_2026-09-29_2057`: DEL-01-04, DEL-02-01, DEL-02-03, DEL-03-02 and DEL-03-03. A follow-up currency audit records the clearance (`_Evaluation/DAGCurrency/_LATEST.md`).

**Currency conditions reliance.** DAG-003 carries authority only through this record and only while it is current with the local evidence (SPEC §5.4, D-GOV-49). A later departure makes the affected deliverables `DAG pending` until the owner decides. See `HANDOFF_STATE.md`.
