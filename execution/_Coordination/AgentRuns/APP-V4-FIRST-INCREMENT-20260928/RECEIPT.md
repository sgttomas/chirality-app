# Receipt — APP-V4-FIRST-INCREMENT-20260928

The first undertaking of Chirality App v4's work toward the 60% gate. Owner
steering (2026-09-28): develop the technical details and interfaces for the
first App/host increment, using the accepted DAG, the local scopes and the
characterized SCCs. Graph:
[WORK_GRAPH.md](../../WorkGraphs/APP-V4-FIRST-INCREMENT-20260928/WORK_GRAPH.md).

## What landed

Version-identified **draft definitions**, at 60% level, for 14 deliverables.
They are unsupplied, unimplemented and not accepted, and sit in each
deliverable's `Design/` folder.

| Deliverable | Contribution |
|---|---|
| DEL-04-01 | ACT-POLICY-v0.5 |
| DEL-04-02 | AS-v0.5 |
| DEL-04-03 | RS-v0.5 |
| DEL-03-01 | C-v0.5 |
| DEL-03-02 | P-v0.5 |
| DEL-03-03 | ADAPTER-v0.3 |
| DEL-03-04 | GUIDE-v0.2 |
| DEL-02-01 | WD-v0.5 (+ EXAMPLES) |
| DEL-02-03 | EXEC-v0.3 |
| DEL-05-01 | LOOP-v0.5 |
| DEL-05-02 | PANEL-v0.5 |
| DEL-01-01 | HOSTING-BOUNDARY-v0.5, plus the Codex 0.158.0 PIN-SPIKE-v0.1 observation record |
| DEL-09-06 | CA-v0.3; RELAY-v0.3, 32 questions, **prepared, not delivered** |
| DEL-09-09 | XT-v0.3 |

Integration rulings R1–R7 settle the cross-file meanings. Among them:

- canonical act names A1–A14;
- the treatment → outcome map;
- checkpoint reached-when, subject class and held actions;
- content identities and acceptance binding;
- one outcome taxonomy;
- grant states;
- one hold-support value set;
- carriage assurance;
- the shared fixture FX-PIPE-01.

Each ruling is labelled SETTLED, DERIVED, INTEGRATION or PROPOSED.

## Decisions

In [OWNER_DECISIONS.md](OWNER_DECISIONS.md):

- **DECISION-1:**
  - scope Option A;
  - OI-001, five reserved acts;
  - OI-002, App routine permissions stay the user's Codex setting, and hosts
    have no classifier mode;
  - OI-012, Codex pin `0.158.0` plus the spike.
- **DECISION-2:**
  - D5, user flexibility for App conversations reading host content;
  - D6, App-side run holds deferred to the SWBPIPE answer.
- **Owner direction:** relay SWBPIPE after final review.

## PRs

- [#1039](https://github.com/sgttomas/chirality/pull/1039): Wave 1, merged
  `98b1723b`.
- [#1043](https://github.com/sgttomas/chirality/pull/1043): Wave 2 (W7–W10,
  R4–R7, V3–V6 and the C1 records), merged `df6d59e3`.
- The final PR carries this receipt, the closeout account, the MEMORY rows and
  the handoff pointer. It is recorded in the graph; its merge is established by
  Git and GitHub, not by this file.

## Checks and evidence

- **DAG currency:** DAG-001 manifests passed at start and at D0. No bound file
  changed.
- **Receiver comparisons:** V1-A/B/C.
- **Independent reviews:** IR1-A/B/C; V2; V3-A/B; V4-A/B; V5; V6. All are in
  `reviews/`. Every verdict was *merge as drafts*, with blocking items resolved
  before merge.
- **Write fences:** every agent's fence was verified by `git status`.
  Deviations (read-only git commands) are logged in [DISPATCH.md](DISPATCH.md).
- **Repository CI:** on each PR.
- **Codex 0.158.0 spike:**
  - generator output is deterministic and hashed;
  - handshake and unknown-method behaviour were observed;
  - the TS output is regenerable and not committed.

## Limits

- No product code, qualification, host delivery or adoption, human act, or
  live witness.
- The SWBPIPE relay has not been delivered. V6 confirmed RELAY-v0.3 is ready,
  so the owner's condition (after final review) is met.
- Every checkpointed workflow run from the App through the external channel is
  *unsupported* until the D6 follow-up.
- Proposed ScopeOfWork corrections (about 74), register mirror rows (about 76)
  and 40 new arcs are recorded in [closeout/](closeout/CLOSEOUT_ACCOUNT.md)
  but not applied. Applying them needs a successor route, including a
  DAG-002 departure for the arcs.
- Lifecycle is unchanged: INITIALIZED. IN_PROGRESS would be truthful.
- This undertaking does not pass the 60% gate.
