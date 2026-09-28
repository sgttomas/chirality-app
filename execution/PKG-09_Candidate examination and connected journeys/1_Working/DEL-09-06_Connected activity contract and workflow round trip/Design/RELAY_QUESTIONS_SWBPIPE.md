# Relay questions for the SWBPIPE owner — first connected activity
- Contribution: DEL-09-06/RELAY-v0.1
- Status: **PREPARED FOR HUMAN RELAY — not delivered.** DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted. Delivery, acknowledgment, answer, commitment and adoption: **not observed**.
- Serves: OUT-004 (human-relayed external questions and proposed interfaces; the contribution/evidence account is in `CONNECTED_ACTIVITY_CONTRACT.md` §9); REQ-005; AC-005 through designed VER-005. Also OUT-001's "decision/input account needed to finalize the exact operation-specific definition" (REQ-001, TBD-001).
- Basis: repo 6e18505e3 (accepted basis); DEL-09-06 ScopeOfWork.md sha256 511f2c0016920cbf67476f1b8d911ed85d6cfa419e7a6b15f3c7e20457779b37; `P/docs/HOST_INTEGRATION.md` (sha256 08c8fc7db2d74619ed47d184f44938bb06f1e2abda0a304a9e11b9230d0960da) §1, V4-HI-03, V4-HI-11, V4-HI-20…25, V4-HI-30…33, V4-HI-40…42, V4-HI-50…52, §11; `P/docs/EXAMINATION.md` (sha256 1b156553dec7eb103dbb1166f5c0dbe9c719d26630d2fcace26c28b3ef54ee19) §1, V4-EXM-14, §4; `P/docs/PRD.md` (sha256 657593ce12a9a6da9f8b6c66579945499d909a8b6272d919d2d14a3db4538573) V4-EXT-01, OQ-10, OQ-11; `P/execution/_Coordination/HANDOFF_SWBPIPE_DOMAINS.md` (sha256 6e7a2f0427acdc0553bd5ea9cceaeceeff5bd82bf1165ed5930c389532e15ef4, working tree; not edited); owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (OWNER_DECISIONS.md sha256 f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e) D2, D3; R1_RESOLUTIONS.md sha256 2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4; R2_RESOLUTIONS.md sha256 77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088 (R2-2, R2-12, R2-13, R2-14, R2-20); R3_RESOLUTIONS.md sha256 202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf; BRIEFS.md working copy sha256 77a42f8a8c8260285b4142d3a6392a07daead16010b209139efc0d3efc60a21f ("Common brief", "Owner rulings now in force", "Wave 2 — common additions", "W9")
- Consumed inputs (read with `git show`, not the working tree):
  - **Wave-1 v0.3 at commit `ba0b37123`.** The brief names `main` merge `98b1723b`; that object is not present in this clone. DISPATCH.md records it as the merge of head `1c36b6d97`. Every Wave-1 Design blob is identical at `ba0b37123`, `1c36b6d97` and `e20a3ae8d` (verified by blob id), so these bytes are the merged v0.3 bytes for these paths:
    - DEL-05-01/LOOP-v0.3 `LOOP_RECEIVING_CONTRACT.md` sha256 6b771c8027787193d536fa3507214a8cc579d6ec2f476ee880609c920b6f25c7 (§13 Q-1…Q-7);
    - DEL-05-02/PANEL-v0.3 `PANEL_RECEIVING_CONTRACT.md` sha256 4c47764d3af434c23e63dcc2c10d28f18a4a94546d63d452855c471cfe47bee9 (§8 Q-1…Q-9);
    - DEL-04-01/ACT-POLICY-v0.3 `ACT_AND_POLICY_CONTRACT.md` sha256 b3748c02006f939d8cc78c6e0b0c847598a8b32d55515ae8658ad80597c98128 (§12 item 4, U-04 a–d);
    - DEL-03-01/C-v0.3 `CATALOG_AND_READ_BASIS.md` sha256 ba45e7393ee0b16780f36605ddeecb95ba1f181488e36a46b4b495b69fd67c26 (§4.1, §5, §8, §10 FX-PIPE-01; U-C2, U-C3, U-C5, U-C7);
    - DEL-03-02/P-v0.3 `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` sha256 ec0db87f239bc42e2e3e953d660ce3c4ceddf605d7b98cf1393f97a099b699cf (§9, §12, U-P1…U-P10);
    - DEL-02-01/WD-v0.3 `WORKFLOW_DECLARATION.md` sha256 84841d9f539767b9ff7ae225fec27f0dc4ebbd2c161c41aff179bbae97f345eb (§4.3, U-19);
    - DEL-04-03/RS-v0.3 `RECORD_SEMANTICS.md` sha256 925f35ca27bd7d1e71a375883ada9903267408af57312eed1ae02b47776a3528 (R3, HA-7, HA-9).
  - **Wave-2 at commit `e20a3ae8d`:** DEL-02-03/EXEC-v0.1 `EXECUTION_COMPATIBILITY.md` sha256 e0ede76ebf08003511755afc666be2466a867fd3256837ee94300cd0dfe518e8 (§6.3 TR-6…TR-8, §6.7, §9.1 host row, U-E1, U-E2, U-E9, U-E11…U-E15); DEL-03-03/ADAPTER-v0.1 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` sha256 58b2409ca45ceea66160eb8910ca38b76b6f335dc184eaeb0896e93cabd0a074 (§9 OC-1…OC-12, §12 XQ-1…XQ-12, U-X2, U-X3). ADAPTER cites draft PR #885 as evidence only; this file repeats that standing and makes no network read.
  - SWBPIPE answers, commitments or contributions: **none received** (DEP-001).
- Receivers: the external SWBPIPE implementation owner, through the human (DEP-09-06-018/-019/-020, DEP-001); the App manager, who prepares the relay and records returns (CLM-004 of DEL-09-09; SoW REQ-005); every App file listed under "Depends" below, which records the answer when it returns; closeout C1, which points `HANDOFF_SWBPIPE_DOMAINS.md` to this file.

---

## 0. How to read and use this file

**What it is.** One deduplicated question set for the SWBPIPE owner. It
consolidates the questions prepared in LOOP §13 (Q-1…Q-7), PANEL §8
(Q-1…Q-9), ADAPTER §12 (XQ-1…XQ-12), ACT U-04 (a–d), EXEC's host items,
R2-20, and the OI-021 activity-definition questions in
`HANDOFF_SWBPIPE_DOMAINS.md`. §3 maps every source item to its question here.

**What it is not.** Writing it is not delivery, agreement, commitment or
adoption (SoW REQ-005; SOW-241). It asks the SWBPIPE owner for information and
choices that belong to that owner. It assigns no SWBPIPE construction, and it
does not ask the other session to rework its implementation around an
unaccepted App detail (HANDOFF). The App assumptions stated under each
question are the App's working assumptions until an answer arrives. They are
not proposals the App expects the host to adopt.

**Vocabulary.** Element names are semantic labels, not wire names. Act names
are the canonical A1–A14 (R-1). Outcome terms are P §9 and C §4.1. Fixture
references (FX-PIPE-01, OP-Cn, T-n, PR-n, RC-n, ⟨set-n⟩, V-…) are **invented
fixture subject matter** from C-v0.3 §10. They are not SWBPIPE operation
identities and do not presume SWBPIPE behavior. The SWBPIPE owner may answer
in its own terms; the App maps the answer.

**Answer handling.** Answers may be partial, and "not yet known" is a useful
answer. When an answer returns, the App manager records it in the return
ledger (§4) with its source, candidate or source revision, date and custody.
Each dependent App file then updates its own standing through its own owner.
An answer changes a case from AWAITING INPUT only when the answer supplies the
named input. A stated intention is recorded as an intention, not as delivery.

**Priority.** Questions are ordered by what they unblock (§1). P1 questions
block every *positive* checkpoint case; nothing about a human act on host
content can reach *performed* until SQ-01 is answered, and no acceptance
checkpoint can be examined under a direct grant until SQ-02 is answered.

---

## 1. Priority groups

| Group | Questions | What an answer unblocks |
|---|---|---|
| **P1 — positive checkpoint cases** | SQ-01 capture-evidence reference; SQ-02 governing checkpoint constraint; SQ-03 content identities used to bind acts | Any host-content checkpoint reaching *performed*; the acceptance-checkpoint-under-direct-grant case; subject binding for A4 on changed rows |
| **P2 — the activity itself (OI-021)** | SQ-04 first activity and environment; SQ-05 policy for the selected operation; SQ-06 direct application on the external channel | The operation-specific increment SoW; replacing fixture operations with real ones |
| **P3 — basis, outcomes and recovery** | SQ-07 basis and staleness; SQ-08 proposal identity and repeated submission; SQ-09 outcome statements and unknown; SQ-10 undo; SQ-11 exposure | Stale, duplicate, interruption and unknown cases (V4-EXM-20/25) |
| **P4 — external channel** | SQ-12 seam and derivation; SQ-13 enablement; SQ-14 origin and caller identity; SQ-15 locality and sandbox; SQ-16 data boundary | The App's Codex route (V4-EXM-25) |
| **P5 — workflow exchange** | SQ-17 receiving App workflows; SQ-18 adaptation and library identity; SQ-19 host run records and supplied guidance; SQ-20 host-side placement (informational) | The V4-EXM-14 round trip |
| **P6 — acts, views and panel** | SQ-21 faithful-record operation; SQ-22 proposal views; SQ-23 display of lapse and related standings; SQ-24 findings storage; SQ-25 App capture on host content | Panel receiving and act display |
| **P7 — extension and examination** | SQ-26 the one new operation for the extension trace; SQ-27 candidates and examination evidence | V4-EXM-24; every candidate-bound result |

---

## 2. Questions

Each question gives: the question; the App files and identifiers that depend
on it; why it matters; its point of need; what the App assumes meanwhile; and
the answer form requested.

### P1 — questions that block positive checkpoint cases

#### SQ-01 Capture-evidence reference for acts your act facility captures

- **Question.** For each act your act facility captures — A4 mark checked,
  A5 accept, A10 reject, A12 set grant, A6 approve and A7 rely where you offer
  them — and for a person's recorded decision *not* to act (act-declined
  event), do you expose a stable **capture-evidence reference**? Can the App
  read, for that act: act identity, decision actor, act kind, the bound
  content identity with its method designation, scope, purpose and time? On
  which surfaces can it be read (your UI, the embedded tools, the external
  interface)? Does it stay resolvable after a restart? Will you ever capture
  a person's act through an MCP elicitation, a CLI prompt or another
  agent-mediated question? (The App contracts ask that you do not.)
- **Depends.** WD-v0.3 I-5, §4.3.4 *performed*; EXEC-v0.1 §4.5 SP-3, CH-3,
  CH-7, CH-28, U-E12; LOOP-v0.3 §13 Q-2, FX-C1, FX-C5, FX-C8; PANEL-v0.3 §8
  Q-2, PC-07, PC-18, PC-19, PC-21; ACT-v0.3 U-04(a), FX-29; RS-v0.3 HA-7, §6.1
  "capture evidence references"; ADAPTER-v0.1 §7.6, XF-18, XF-33, XQ-10;
  `CONNECTED_ACTIVITY_CONTRACT.md` W14-04, W14-05; DEL-09-09
  `EXTERNAL_TRACE_CASES.md` XC-02, XC-09.
- **Why it matters.** A checkpoint is satisfied only by attributable evidence
  from the capturing surface (R-5, R2-20). A faithful record by the App or the
  loop is valid only as a record that cites that evidence. Without a
  reference, the engineer's real acceptance in SWBPIPE cannot be joined to the
  run, and V4-EXM-25's completed witness cannot be shown.
- **Point of need.** Before host act-recording integration; before any
  positive host-content checkpoint case or the V4-EXM-14/25 joined witness.
- **App assumes meanwhile.** No host-content checkpoint reaches *performed*;
  it stays *waiting* (or *unknown* after interruption). App-side faithful
  records are record shapes only. Positive cases are AWAITING INPUT. An
  elicitation or prompt answer is never act capture (EXEC CAP-6; ADAPTER
  L-ADAPTER-4).
- **Answer form.** A table with one row per act kind (plus act-declined):
  offered (yes/no); reference exposed (yes/no/planned); elements readable;
  surfaces; durability across restart. Plus a sample record using invented
  material, if one exists, and a yes/no on elicitation or prompt capture.

#### SQ-02 Governing checkpoint constraint: receipt or host-held declaration

- **Question.** When a workflow run declares an acceptance checkpoint (A5)
  on an operation's result, the App contracts require that the operation be
  resolved as *propose* in that run, even under a direct grant (V4-HI-42; D2).
  (a) Can your validation/application route receive a per-request
  **governing checkpoint constraint** {workflow run, checkpoint name,
  required act A5, operation} and resolve *propose* from it? (b) Or will the
  host hold its own copy of the selected workflow's declaration, or a run
  association the App registers at run start, and evaluate it itself? (c) For
  a direct request under the constraint, will the route return *not
  permitted* naming the constraint, rather than converting the request into a
  proposal? (d) For checkpoints of the kind "before dispatch of a named
  operation", will the host hold such a call itself, on the embedded and on
  the external surface? (e) What evidence would show which of these applies?
- **Depends.** R2-12; P-v0.3 §3.3, U-P10; WD-v0.3 I-7, U-19, VC-11; C-v0.3
  V-CP1; LOOP-v0.3 §13 Q-1, FX-C9; PANEL-v0.3 §8 Q-1, PC-24; ACT-v0.3 §4.4,
  U-04(c); EXEC-v0.1 §2 HP-1, §3.6 "enforced on the host route", CH-27, U-E1,
  U-E13; ADAPTER-v0.1 §5.3 GC-1…GC-5, OC-7, OC-11, XF-25, XF-26, U-X3, XQ-3;
  `CONNECTED_ACTIVITY_CONTRACT.md` W14-04.
- **Why it matters.** An omitted constraint is indistinguishable from none
  (R2-12). On the external channel the model composes the call, so an
  omission would let a direct grant bypass a declared acceptance checkpoint
  (ADAPTER GC-2). The App cannot hold a model-issued external call before
  dispatch in native realization (ADAPTER GC-5; EXEC F-10). A host-held
  evaluation would close both gaps.
- **Point of need.** Before V-CP1, LOOP FX-C9, PANEL PC-24, WD VC-11, EXEC
  CH-27 and ADAPTER XF-25 are executed; before the App fixes its realization
  family (TBD-007).
- **App assumes meanwhile.** Those cases are AWAITING INPUT. Model-supplied
  carriage alone does not satisfy R2-12 (ADAPTER GC-3, proposed to DEL-02-03).
  Kind (a) checkpoints over the external surface are *not established* in
  native realization (GC-5). The owner question on App hold points is pending
  (DECISIONS_PENDING_2 D6; not ruled).
- **Answer form.** Choose one or more of (a) per-request receipt, (b)
  host-held declaration, (c) host-held run association, (d) none planned; a
  yes/no for (c) *not permitted* naming the constraint; a yes/no for host
  holds before dispatch per surface; and the evidence you would supply.

#### SQ-03 Content identities used to bind acts

- **Question.** (a) Does every read return, per row or object, a **subject
  content identity** with its method designation, distinct from the
  read-level content identity? (b) What does each object kind's subject
  identity cover? For example, does a support's identity cover its display
  label (fixture assumption FA-2)? (c) Is an A5 bound to the content of the
  change item it accepts (operation identity and version, bound targets,
  old/new values, relied-on basis)? (d) Does an applied outcome identify the
  created and changed objects, with their subject content identities after
  application (R2-14)?
- **Depends.** C-v0.3 §5.3, U-C3, FA-2; P-v0.3 §3.1, §9 "applied (receipt)",
  U-P2; WD-v0.3 §4.3.6 SB-1…SB-3; RS-v0.3 L-1/L-2; EXEC-v0.1 SP-4, CH-1, CH-7,
  MC-2; LOOP-v0.3 §13 Q-3, FX-C1; WD-EX E1 `CP-check`; ADAPTER-v0.1 RD-2;
  HANDOFF "Domain identity and basis"; `CONNECTED_ACTIVITY_CONTRACT.md` W14-04,
  W14-06.
- **Why it matters.** An act binds to content and lapses visibly when that
  content changes (V4-HI-32). A checkpoint on "the rows the application
  changed" can bind only if the applied outcome names those rows and their
  post-application identities.
- **Point of need.** Before subject-binding and lapse fixtures run against a
  host; before the V4-EXM-14 checkpoint cases.
- **App assumes meanwhile.** Fixture assumptions FA-2/FA-3 stand, labeled.
  Resulting objects absent from a receipt are recorded "not supplied" as an
  evidence limit. Identities with different method designations are
  *unknown (incomparable)*.
- **Answer form.** Yes/no/planned for (a), (c), (d); a short scope statement
  per object kind for (b); a sample read and receipt using invented material.

### P2 — the first connected activity (OI-021)

#### SQ-04 First connected activity: operation, check and environment

- **Question.** Which useful supported model operation, and which
  non-mutating check, should the first connected activity use: inspect a
  model, propose an adjustment, request a non-mutating check, meet an
  intervening edit, and recover the actual outcome and receipt? Please name
  (a) the read, change and check operations by your catalog identity, or
  alternatives to choose from; (b) whether the check is a host-named check
  (host checks passed / failed) or the agent's examination; (c) the
  expression(s) the activity will use first: your embedded agent, the App's
  Codex through your external interface, or both; (d) the candidate
  environment (host build or source revision, configuration, model server),
  its prerequisites and current readiness, without dates you cannot support.
- **Depends.** OI-021 / PRD OQ-11 everywhere, in particular:
  `CONNECTED_ACTIVITY_CONTRACT.md` §2, §3, TBD-001; ACT-v0.3 U-01; EXEC-v0.1
  U-E17; LOOP-v0.3 and PANEL-v0.3 OI-021 rows; C-v0.3 OP-C11; DEL-09-09
  `EXTERNAL_TRACE_CASES.md` IN-10; HANDOFF "First activity", "Capability
  semantics".
- **Why it matters.** Every App fixture uses invented FX-PIPE-01 material.
  The operation-specific increment SoW cannot be finalized, and no dependent
  execution can begin, until the operation, autonomy and environment are
  chosen (SoW TBD-001; DEP-09-06-021).
- **Point of need.** Before the connected-activity SoW and execution (OI-021
  accepted point of need); before dependent implementation or live examination
  (OQ-11).
- **App assumes meanwhile.** The supports/run adjustment on FX-PIPE-01 is a
  proposed fixture only. OP-C11-dependent production is **held** (R2-9). No
  operation is selected, and independent App definition continues.
- **Answer form.** A short list of candidate operations with catalog
  identities or descriptions, one marked preferred if you have a preference;
  the expression; the environment identification; readiness in your words.
  The owner and the App/shared owner make the selection (OI-021).

#### SQ-05 Policy for the selected operation

- **Question.** For the operation(s) in SQ-04: (a) what class does your
  catalog assign (none; may apply within granted autonomy; proposal only;
  reserved to the person)? (b) Which operation-specific reserved acts do you
  add? (c) Which reserved-act list does SWBPIPE name and enforce (V4-HI-30),
  and does it include the five first-increment acts the owner ruled for the
  App/shared contracts (D2: marking work checked; accepting a proposal where
  the active autonomy requires one; engineering approval; relying on a result
  professionally; changing the autonomy grant or enabling external access)?
  (d) Will the route report the settings reference in force at application?
  (e) How do you show the grant states, including a policy default (propose)
  and a refused setting? (f) Would you take part in defining a consequence
  vocabulary for grant scope?
- **Depends.** ACT-v0.3 §7, §8.3 P-01…P-06, U-01, U-02, U-04(d); PANEL-v0.3
  §8 Q-8; AS-v0.3 §3; ADAPTER-v0.1 UNRESOLVED "host adoption"; C-v0.3 T15
  (class P-03, U-02); HANDOFF "Autonomy and human acts";
  `CONNECTED_ACTIVITY_CONTRACT.md` §2 row CA-2, W14-04.
- **Why it matters.** D2 does not show that SWBPIPE has adopted or enforces
  the list (DEP-001). The host names and enforces its own list. Graduated
  autonomy (V4-EXM-22) and the checkpoint-under-direct case need the actual
  policy for the actual operation.
- **Point of need.** Before operation-policy production contracts for the
  selected operation; before any enforcement claim.
- **App assumes meanwhile.** The SWB model-change class is *may apply within
  granted autonomy* with default *propose* (DERIVED from V4-HI-41). A
  concrete first operation is *no policy basis* (pending OI-021) until
  classed. All treatment behavior is receiving meaning, not host evidence.
- **Answer form.** Per operation: class; added reserved acts; the host's
  reserved list; yes/no on (d); a description or screenshot reference for (e);
  yes/no/later on (f).

#### SQ-06 Direct application on the external channel

- **Question.** Does an external actor use the same grant the person sets per
  class? Draft PR #885's description says "Apply stays in the app's human
  review route". Is that (a) a class assignment, (b) a rule about the
  external channel, or (c) a fixed first-increment policy? If a direct
  request arrives over the external interface, will it return *not permitted*
  naming that rule?
- **Depends.** ADAPTER-v0.1 RP-4, XF-24, XQ-8, OC-7; ACT-v0.3 §6; DEL-09-09
  `EXTERNAL_TRACE_CASES.md` XC-10.
- **Why it matters.** A channel rule must be stated by the host as a
  governing treatment. It must never be shown as a class value or as the
  person's grant (V4-HI-51; S-X3).
- **Point of need.** Before external-channel treatment cases run against a
  candidate.
- **App assumes meanwhile.** The PR #885 statement is evidence only, not a
  commitment. XF-24 is a named variant.
- **Answer form.** (a), (b) or (c), with the outcome a direct external request
  receives.

### P3 — basis, outcomes and recovery

#### SQ-07 Read basis, generation and staleness

- **Question.** (a) Does every read return the full basis descriptor —
  workspace identity, generation, model revision, canonical content identity
  and method designation? (b) What does a new generation mean, for example
  after restoring from an archive, and can bases across generations be
  compared? (c) Does a submission keep the originally inspected basis, rather
  than a queue-time basis (HI §11 risk)? (d) Is the stale check per item,
  against the relied-on targets' subject content identities, so that applying
  one item does not stale siblings with other targets (R2-13)? (e) Does
  application re-check the relied-on targets after acceptance? (f) Which
  selection or model changes invalidate a proposal?
- **Depends.** C-v0.3 §5, U-C2, U-C3, Tg; P-v0.3 §5, §12, U-P3; LOOP-v0.3 §13
  Q-6 (per-item part), FX-D2, FX-D3; ADAPTER-v0.1 RD-2, RD-5, XQ-6, XF-14,
  XF-39; EXEC-v0.1 MX-7; HANDOFF "Domain identity and basis"; DEL-09-09
  `EXTERNAL_TRACE_CASES.md` XC-03, XC-08.
- **Why it matters.** V4-EXM-25 must join the original inspected basis to the
  refusal or application. A queue-time basis would silently substitute a later
  one.
- **Point of need.** Before integrating an actionable host operation
  (HANDOFF); before stale and generation fixtures run on a host.
- **App assumes meanwhile.** The R2-13 per-item rule and the "no longer holds"
  rule are INTEGRATION rulings, labeled. Cross-generation bases are
  *unknown (incomparable)*.
- **Answer form.** Yes/no/planned per item, with a short explanation for (b)
  and (f).

#### SQ-08 Proposal identity and repeated submission

- **Question.** (a) Who mints the proposal identity (a submit key or
  equivalent), and is it available before the first submission, for example
  from a preview step? (b) Does de-duplication by that identity happen before
  the basis check, so that a retry is never refused as stale because of its
  own effects? (c) Does de-duplication survive a controller restart? (PR #885's
  description says recovery is within one controller session.) (d) Can a
  caller read a proposal's recorded state by identity? (e) What evidence will
  show one domain effect per item when the same proposal is submitted twice?
- **Depends.** R2-13; P-v0.3 §5, §7, U-P1; LOOP-v0.3 §13 Q-6, FX-O1;
  ADAPTER-v0.1 §5.6 PI-1…PI-4, OC-10, XF-19, XF-21, XQ-5; C-v0.3 T13;
  HANDOFF "Application, cancellation and recovery"; DEL-09-09
  `EXTERNAL_TRACE_CASES.md` XC-05, XC-06.
- **Why it matters.** "One effect" is a host obligation to be evidenced, not a
  recorded fact (R-7). Transport or session de-duplication is not domain
  evidence (V4-EXM-25).
- **Point of need.** Before direct application over the external channel;
  before duplicate and restart cases run.
- **App assumes meanwhile.** Each submission is recorded separately with only
  the effects observed. After a restart without durable de-duplication, a
  retry is *outcome unknown* and one-effect is unevidenced (PI-4, proposed).
- **Answer form.** Yes/no/planned per item; for (e), the domain evidence you
  can supply (for example the model history or receipt list).

#### SQ-09 Outcome statements, errors and unknown outcomes

- **Question.** (a) Does each result state its outcome in terms that map to
  the App's outcome taxonomy — unavailable, not permitted, channel not
  enabled, not exposed on this surface, refused (invalid or stale), queued,
  accepted, rejected, withdrawn, applied with receipt, application error,
  error — with the evaluated basis, distinctly from transport status? (b) Does
  an application error state its effect (none, partial with receipts,
  unknown)? (c) How does the host behave after an interruption: is the receipt
  durable, and can an unknown outcome be resolved by a later read? (d) Is a
  validation failure before queueing recorded as a refusal? (e) Is a refusal
  at application distinguished from a validation refusal in your records?
  (f) Are items of one proposal applied individually or in groups?
- **Depends.** P-v0.3 §9, U-P4, U-P5, U-P7; C-v0.3 §4.1; ADAPTER-v0.1 M-1…M-5,
  OC-9, XQ-7; EXEC-v0.1 MX-8; HANDOFF "Application, cancellation and
  recovery"; DEL-09-09 `EXTERNAL_TRACE_CASES.md` XC-06, XC-07.
- **Why it matters.** Success means only that an operation ran. The App must
  never infer acceptance, application or failure from transport success or
  silence.
- **Point of need.** Before outcome recording against a host; before
  interruption cases.
- **App assumes meanwhile.** A result without a stated outcome is *outcome
  unknown* (observer App or loop), never *queued* or *applied*.
- **Answer form.** A mapping from your result forms to the terms in (a); short
  answers to (b)–(f).

#### SQ-10 Undo and publication

- **Question.** Is there an undo route for an applied change? What can it
  reverse (one receipt, one item, a group)? Is its treatment governed by the
  policy of the operation it reverses (R3-4)? Does its receipt record that it
  reverses the earlier receipt? What does "publication" mean in SWBPIPE, and
  does it affect the standing of an applied change?
- **Depends.** R2-15; R3-4; P-v0.3 §4.5, U-P8; C-v0.3 OP-C10, T17; PANEL-v0.3
  §8 Q-4 (reversed display); ADAPTER-v0.1 RP-6, XF-38; HANDOFF "publication/
  undo".
- **Why it matters.** Acts bound to content an undo changes lapse normally.
  Direct application under a grant must offer an undo route (V4-EXM-22).
- **Point of need.** Before undo implementation and direct-application cases.
- **App assumes meanwhile.** OP-C10 semantics only; mechanism is a host input.
- **Answer form.** Yes/no per item, with a short description.

#### SQ-11 Exposure per surface and entries offered

- **Question.** Does each catalog entry state whether it is exposed on your
  human interface, embedded tools and external interface? Which entries are
  offered on the embedded and external surfaces for the first activity? Does
  the host report *not exposed on this surface* from that element, rather than
  as a missing operation or an error?
- **Depends.** R2-4; C-v0.3 §3 element 9, §8, U-C7, FA-1, V-X1; LOOP-v0.3
  §13 Q-7, FX-U3; ADAPTER-v0.1 XF-09, XQ-9; EXEC-v0.1 EV-7/EV-8, MT-5;
  WD-v0.3 §4.2.4.
- **Why it matters.** "Not exposed" must stay distinct from "missing" and from
  "channel not enabled". A narrowed extension promise would be expressed
  through this element (OI-003).
- **Point of need.** Before required-tool checks run against a host catalog.
- **App assumes meanwhile.** Every fixture entry is exposed on all three
  surfaces (FA-1, labeled). Real values stay *unagreed*.
- **Answer form.** Yes/no/planned; the first-activity entries with their
  exposure per surface.

### P4 — the external channel (App's Codex)

#### SQ-12 External seam and native surface derivation

- **Question.** For the first increment, will you offer the external seam as
  the PR #885 CLI, as an MCP server, or both? Is its operation set generated
  from, or checked against, the same catalog as your UI and embedded tools?
  Will you supply the mapping from each native tool or command to catalog
  operation identity and version?
- **Depends.** V4-HI-50; ADAPTER-v0.1 §4.1 NM-1…NM-4, OC-1, OC-8, XQ-1; C-v0.3
  §8 X column; DEL-09-09 `EXTERNAL_TRACE_CASES.md` §4, §5 (generated versus
  adapted work).
- **Why it matters.** The host selects the seam (V4-HI-50); the App receives
  it. Without a mapping, requirements on the external surface are *not
  established*. Derivation is evidence for the OI-003 extension ruling.
- **Point of need.** Before the App receiving implementation depends on the
  interface; before DEL-09-09 qualification.
- **App assumes meanwhile.** Nothing is selected (TBD-007). PR #885 is
  evidence only.
- **Answer form.** Seam choice; derivation (generated / checked / hand-built);
  yes/no/planned on the mapping.

#### SQ-13 Enablement of external access

- **Question.** Is external access off by default and enabled only by a
  person's act captured by your facility, with a capture-evidence reference?
  Is PR #885's "opt-in" that act, a build feature, or a launch flag? When
  access is off, does a caller get an explicit *channel not enabled*? Can the
  App read the current enablement state? What happens to queued external
  proposals when access is disabled?
- **Depends.** V4-HI-52; D2e; R2-3; ADAPTER-v0.1 §3.2, E-1…E-9, OC-4, XF-01…
  XF-07, XF-35, XQ-2, U-X1; C-v0.3 §4.1; DEL-09-09 `EXTERNAL_TRACE_CASES.md`
  XC-01, XC-12.
- **Why it matters.** Only the host's own refusal guarantees "off"; the App
  cannot veto the user's Codex configuration (ADAPTER E-2, F-2). Enabling or
  disabling is the person's A13.
- **Point of need.** Before enablement implementation and VER-002 of DEL-03-03
  and DEL-09-09.
- **App assumes meanwhile.** Host enablement is authoritative; App-side
  configuration alone never enables; "enablement unconfirmed" is treated as
  disabled for App-originated requests.
- **Answer form.** Yes/no/planned per item, with the disable behavior in words.

#### SQ-14 Origin and caller identity

- **Question.** Which origin elements do you record for an external
  submission (author type, identity, channel, conversation, workflow run), and
  do you verify any of them? Can the App read your origin mark to link it? How
  are callers authenticated, and can more than one local caller attach?
- **Depends.** P-v0.3 §3.3; ADAPTER-v0.1 §5.4, OC-6, XF-37, XQ-4, XQ-12
  (callers); RS-v0.3 R11.
- **Why it matters.** Origin marks are linked, not copied (V4-HI-71). Author
  identity over the external channel is *unverified* until a mechanism exists.
- **Point of need.** Before origin conformance is claimed.
- **App assumes meanwhile.** "External agent (unverified identity)".
- **Answer form.** A list of recorded origin elements with verified yes/no;
  the authentication approach; single or multiple callers.

#### SQ-15 Locality and sandbox reach

- **Question.** Is the endpoint strictly local: a local process, a local
  socket or a loopback origin? Should the App expect the user's Codex sandbox
  to need access to your socket? (The App will not change the person's
  sandbox or permission settings.)
- **Depends.** V4-HI-52; ADAPTER-v0.1 E-7, §3.5, OC-5, XF-07, XQ-12.
- **Why it matters.** A non-local endpoint makes the channel *not
  established*. A local-socket CLI may be unreachable from the user's sandbox
  without the person's own setting change.
- **Point of need.** Before enabling a live candidate.
- **App assumes meanwhile.** Local only; sandbox effect *not observed*.
- **Answer form.** Transport and locality; a yes/no on sandbox access needs.

#### SQ-16 Data boundary for content read over your external interface

- **Question.** Do you impose a rule on which model destinations may receive
  content read over your external interface? For example, are only App
  conversations using a local model allowed? Does V4-HOST-02, or another
  SWBPIPE rule, apply to the App's conversations?
- **Depends.** ADAPTER-v0.1 §3.4, U-X2, XF-36, XQ-11, F-12; owner question
  DECISIONS_PENDING_2 D5 (pending; not ruled); DEL-09-09
  `EXTERNAL_TRACE_CASES.md` IN-14.
- **Why it matters.** Enabling the channel authorizes no data destination. No
  deliverable or ruling yet owns this boundary.
- **Point of need.** Before enabling a live candidate; before destination
  inspection.
- **App assumes meanwhile.** The App shows the conversation's model
  destination class and adds no other destination; XF-36 is HELD.
- **Answer form.** None / a stated rule / a planned rule, in your words.

### P5 — workflow exchange (V4-EXM-14)

#### SQ-17 Receiving App workflows

- **Question.** (a) Can your workflow library list a workflow carried from the
  App **unadapted**, keeping its original origin (*project* or *user*) and
  source root, with your library shown as its holding library? (b) Can your
  host read the workflow's declared part (expected inputs, required tools,
  checkpoints, outputs, evidence) at the App's declaration contract version,
  and report when it cannot? (c) Who evaluates required-tool compatibility and
  checkpoint holds for host runs, and how are an unavailable capability and an
  unsupported checkpoint reported to the person? (d) What files and form do
  you need the App to relay (package plus a carriage manifest; no transport is
  assumed)?
- **Depends.** EXEC-v0.1 §6.3 TR-5, TR-6, §6.7 TF-2…TF-4, TF-7, RT-1, RT-4,
  U-E14; WD-v0.3 §3.4, §6.4; PANEL-v0.3 UNRESOLVED "which party evaluates
  required-tool outcomes in the host"; HANDOFF "Workflow exchange";
  `CONNECTED_ACTIVITY_CONTRACT.md` W14-01, W14-03.
- **Why it matters.** V4-EXM-14 carries a reviewed workflow from App to host.
  Registration or a portable file alone proves nothing. An explicit
  unsupported-capability outcome is required (SoW REQ-003).
- **Point of need.** Before App↔host round-trip conformance (HANDOFF); before
  RT host-side cases.
- **App assumes meanwhile.** Host links in the trace are AWAITING INPUT.
  Receiving limits are reported explicitly as TF-3/TF-4 outcomes.
- **Answer form.** Yes/no/planned for (a) and (b); a description for (c) and
  (d).

#### SQ-18 Adaptation, host workflows and library identity

- **Question.** (a) Which host workflows exist today, and how does the host
  show each one's identity (kind, origin, source root, name, revision),
  derived-from and holding library? (b) When the host adapts a carried
  workflow, is the result a new revision with host origin and a derived-from
  link to the original? (c) Can you relay a comparison showing which
  checkpoints were preserved, changed, removed or added? (d) Will you publish
  compatibility statements between catalog entry versions, or is version
  equality the rule?
- **Depends.** R-9; R2-20; EXEC-v0.1 §6.2 HL-1…HL-3, §6.4 AD-1…AD-6, RT-2,
  RT-3, RT-7, U-E11, U-E14; WD-v0.3 §6.4; WD-EX E3, E4; PANEL-v0.3 §8 Q-6;
  C-v0.3 U-C9; `CONNECTED_ACTIVITY_CONTRACT.md` W14-02, W14-10.
- **Why it matters.** "Checkpoint identity" across adaptation is part of
  V4-EXM-14. Adapted content must never inherit the original's identity or
  acts.
- **Point of need.** Before RT host-side cases.
- **App assumes meanwhile.** Adaptation evidence is *not observed*; version
  compatibility is equality only.
- **Answer form.** A list or sample for (a); yes/no/planned for (b)–(d).

#### SQ-19 Host run records and supplied guidance

- **Question.** (a) Can the host loop record, per turn, the source identity
  and content identity (with method designation) of each guidance input it
  supplies to the model — role, workflow, project guidance? (b) Do host run
  records name the full workflow identity that ran? (c) Can those records,
  including interruption and revision history, be relayed to the App by
  reference?
- **Depends.** R2-20; LOOP-v0.3 §13 Q-4; RS-v0.3 R2, R3; EXEC-v0.1 §6.1
  *supplied*, HR-6, RT-5, RT-8, U-E14, U-E15; HOSTING-v0.3 §8.2;
  `CONNECTED_ACTIVITY_CONTRACT.md` W14-07, W14-08.
- **Why it matters.** V4-EXM-14 keeps selected/resolved bytes, what was
  supplied, provider adoption and observed behavior separate. "Supplied ≠
  adopted".
- **Point of need.** Before host supplied-link evidence is claimed.
- **App assumes meanwhile.** Host *supplied* is **unknown**; adoption is
  unknown; history is referenced, not copied (V4-HI-71).
- **Answer form.** Yes/no/planned for each; an example record if one exists.

#### SQ-20 Host-side placement (informational)

- **Question.** For information only: where do you intend the loop, panel
  assembly, conversation persistence, the checkpoint hold machine and the
  required-tool check to live in SWBPIPE?
- **Depends.** OI-013; OI-014; LOOP-v0.3 §10.1; PANEL-v0.3 §8 Q-9; EXEC-v0.1
  U-E2.
- **Why it matters.** Placement is the SWBPIPE owner's under OI-013. The App
  supplies semantics only, and no common implementation is allocated.
- **Point of need.** Before shared/host implementation boundary contracts.
- **App assumes meanwhile.** No placement is implied.
- **Answer form.** Free text, or "not yet decided".

### P6 — acts, views and panel

#### SQ-21 Host faithful-record operation

- **Question.** Does the host offer any operation that stores an agent's
  faithful record of a person's act? If so, does it meet all four conditions:
  it does not change act state; it cites capture evidence; it never satisfies
  a checkpoint; it takes ordinary policy (R2-2)?
- **Depends.** R2-2; ACT-v0.3 U-04(b), P-02; RS-v0.3 HA-9; LOOP-v0.3 §13 Q-5;
  PANEL-v0.3 §8 Q-5.
- **Why it matters.** An operation that performs a reserved act is reserved to
  the person; no faithful record is made through one.
- **Point of need.** Before host act-recording integration.
- **App assumes meanwhile.** No such operation; App-side faithful records are
  DEL-04-03 files.
- **Answer form.** No / yes (with the four conditions answered).

#### SQ-22 Proposal views

- **Question.** Which host views show proposed change items with old and new
  values, affected objects and reason? How can the panel reference a position
  in them?
- **Depends.** V4-HI-24; PANEL-v0.3 §8 Q-3, §4; P-v0.3 §8; C-v0.3 §8
  "proposal views".
- **Why it matters.** There is no agent-private surface; proposals appear in
  the host's own views (V4-HOST-04).
- **Point of need.** Before panel receiving implementation.
- **App assumes meanwhile.** Display is defined; views are host-owned.
- **Answer form.** View names and a description of referencing.

#### SQ-23 Display of lapse, supersession, stale after acceptance and reversal

- **Question.** How does the host show: an act lapsed by a content change; a
  grant setting superseded by a later one; "accepted by ‹person› — not
  applied: refused — stale"; and "applied, then reversed"?
- **Depends.** PANEL-v0.3 §8 Q-4, §5; AS-v0.3 §3, §8; R2-7; R2-15; R2-16.
- **Why it matters.** These standings must stay visible and distinct.
- **Point of need.** Before panel receiving implementation.
- **App assumes meanwhile.** Display rules per PANEL §5 and AS §8.
- **Answer form.** A description, or "not yet designed".

#### SQ-24 Where agent examination findings are held

- **Question.** Does the host hold agent examination findings attached to rows
  or results by reference? If it stores them, is storing them a change through
  the one route?
- **Depends.** V4-EXM-21; C-v0.3 U-C5; RS-v0.3 R10; PANEL-v0.3 §8 Q-7.
- **Why it matters.** Findings are never "checked" (A4) and never a host check.
- **Point of need.** Before findings cases run against a host.
- **App assumes meanwhile.** Findings are referenced; not a change unless the
  host says so.
- **Answer form.** Where they are held; change yes/no.

#### SQ-25 Acts on host content captured through the App

- **Question.** In the first increment, will the host accept any person's
  act on host content that the App captures (a proxy control), or will every
  act on host content be captured only by your own act facility?
- **Depends.** EXEC-v0.1 §5 CAP-1, U-E9; ADAPTER-v0.1 §7.6.
- **Why it matters.** The App offers no proxy control for host-content acts
  unless the host defines one.
- **Point of need.** Before any App proxy control is offered.
- **App assumes meanwhile.** None is offered.
- **Answer form.** Host facility only / a proxy under stated conditions.

### P7 — extension and examination

#### SQ-26 The one new operation for the catalog-extension trace

- **Question.** Which one newly added catalog operation will SWBPIPE use for
  the extension trace (V4-EXM-24)? For that operation, which parts of the
  human interface, embedded tools and external interface are generated from
  the catalog, which are checked against it, and which need separate
  human-view or adapter work? Will you take part, with the owner, in the
  retain/narrow/defer decision on the original "available to all actors
  without separate work" promise (OI-003)?
- **Depends.** V4-PAR-05; V4-HI-03; OQ-10; C-v0.3 §8; ADAPTER-v0.1 NM-4, OC-8;
  DEL-09-09 `EXTERNAL_TRACE_CASES.md` §4, §5, IN-11; HANDOFF "Catalog
  extension".
- **Why it matters.** No automatic availability or maintenance saving may be
  claimed before an actual trace and an explicit disposition. The trace is
  evidence for the decision; it does not make it.
- **Point of need.** Before claiming all-actor availability without separate
  work or maintenance savings; before fixing the extension criterion.
- **App assumes meanwhile.** The trace plan uses a labeled fixture addition
  (DEL-09-09 L-XT-1). `UNRESOLVED{OI-003}`.
- **Answer form.** The operation (or "not yet chosen"); per surface: generated
  / checked / hand-built; participation yes/no.

#### SQ-27 Candidates, host examination evidence and relay of returns

- **Question.** (a) For each host contribution you relay, what identifies it:
  source revision, build, configuration, date? (b) Which host-owned checks or
  witnesses exist or are planned for the first activity (V4-EXM-20…23 kinds of
  evidence), with their limits and unresolved findings? (c) How will evidence
  and receipts be relayed to the App: files, links, custody? (d) For the
  joined witnesses (V4-EXM-14 round trip; V4-EXM-25 external controller), can
  an actual engineer perform the acceptance and checking acts on invented
  material in an identified candidate? (e) What is the next decision or input
  you need from the App side?
- **Depends.** DEP-001; SoW REQ-005, REQ-007 (DEL-09-06); REQ-001, REQ-008
  (DEL-09-09); EXEC-v0.1 TR-8, RT-11; HANDOFF "Examination" and "Return and
  delivery record"; `CONNECTED_ACTIVITY_CONTRACT.md` §8 W14-00, §9;
  DEL-09-09 `EXTERNAL_TRACE_CASES.md` §2, XC-00.
- **Why it matters.** Every result names its candidate, configuration and
  date (V4-EXM-01). A human-relayed file is never treated as an unobserved
  commitment or execution.
- **Point of need.** Before any candidate-bound connected result; before the
  fallback-replacement decision.
- **App assumes meanwhile.** DEP-001 standing is owner-reported building
  before agent-action integration. It is not delivery, adoption or live
  readiness.
- **Answer form.** A list of identified contributions with identifiers and
  limits; the relay form; yes/no/later for (d); free text for (e).

---

## 3. Source-to-question map (deduplication record)

Every source item is covered. "Merged" means the source item is fully asked
inside the named question.

| Source | Item | Question here |
|---|---|---|
| LOOP-v0.3 §13 | Q-1 constraint | SQ-02 |
| | Q-2 capture-evidence reference | SQ-01 |
| | Q-3 resulting objects | SQ-03 (d) |
| | Q-4 per-turn guidance | SQ-19 (a) |
| | Q-5 faithful-record operation | SQ-21 |
| | Q-6 de-duplication; per-item staleness | SQ-08 (b); SQ-07 (d) |
| | Q-7 exposure; entries on the embedded surface | SQ-11 |
| PANEL-v0.3 §8 | Q-1 constraint | SQ-02 |
| | Q-2 capture-evidence reference (incl. act-declined) | SQ-01 |
| | Q-3 proposal views | SQ-22 |
| | Q-4 lapse, supersession, stale after acceptance, reversal | SQ-23; SQ-10 (reversal mechanism) |
| | Q-5 faithful-record operation | SQ-21 |
| | Q-6 host workflows, identity, derived-from, holding library | SQ-18 (a) |
| | Q-7 findings | SQ-24 |
| | Q-8 reserved-act list; grant presentation | SQ-05 (c), (e) |
| | Q-9 persistence and panel assembly (informational) | SQ-20 |
| ADAPTER-v0.1 §12 | XQ-1 seam; derivation; mapping | SQ-12 |
| | XQ-2 enablement | SQ-13 |
| | XQ-3 constraint and run context | SQ-02 |
| | XQ-4 origin | SQ-14 |
| | XQ-5 proposal identity | SQ-08 |
| | XQ-6 basis | SQ-07; SQ-03 (a) |
| | XQ-7 outcomes | SQ-09 |
| | XQ-8 grant and apply | SQ-06 |
| | XQ-9 exposure | SQ-11 |
| | XQ-10 acts; no elicitation capture | SQ-01 |
| | XQ-11 data boundary | SQ-16 |
| | XQ-12 locality; callers; sandbox | SQ-15; SQ-14 (callers) |
| ACT-v0.3 U-04 | (a) capture requirement and reference | SQ-01 |
| | (b) host faithful-record operation | SQ-21 |
| | (c) constraint receipt | SQ-02 |
| | (d) adoption of P-01…P-06; settings in force at application | SQ-05 (c), (d) |
| EXEC-v0.1 host items | U-E1 host-side hold before dispatch | SQ-02 (d) |
| | U-E2 host placement of hold machine and check (OI-013) | SQ-20 |
| | U-E9 proxy control for host-content acts | SQ-25 |
| | U-E11 version compatibility statements | SQ-18 (d) |
| | U-E12 capture-evidence reference | SQ-01 |
| | U-E13 constraint receipt | SQ-02 |
| | U-E14 library receipt of other origins; adaptation evidence; holding library; run records | SQ-17; SQ-18; SQ-19 |
| | U-E15 per-turn supplied guidance | SQ-19 |
| | TR-6, TF-3, TF-4 receiving capability; declaration contract version | SQ-17 |
| | TR-7 adaptation | SQ-18 |
| | TR-8 host evidence returned by relay | SQ-27 |
| R2-20 | Holding library (host side) | SQ-18 (a); SQ-17 (a) |
| | Capture-evidence reference | SQ-01 |
| | Per-turn supplied guidance | SQ-19 |
| HANDOFF (OI-021 activity definition) | First activity | SQ-04 |
| | Domain identity and basis | SQ-07; SQ-03 |
| | Capability semantics (canonical read/action/check operations; route) | SQ-04 (a); SQ-12 |
| | Autonomy and human acts | SQ-05; SQ-01 |
| | Application, cancellation and recovery | SQ-08; SQ-09; SQ-10 |
| | Workflow exchange | SQ-17; SQ-18 |
| | Catalog extension | SQ-26 |
| | Examination | SQ-27 |
| | Return list (selected activity, references, evidence, readiness, owners, next decision) | SQ-04; SQ-27 |

**Not included, with reasons.**

- HANDOFF "Domains" section: a later increment with its own
  provider/method/receiving contributions (SoW CLM-006; PRD §8). It remains in
  HANDOFF and is not part of this first-activity relay.
- PEC: an independent optional capability, not a prerequisite (SoW REQ-006).
- App-owner questions routed inside the App project, not to SWBPIPE: ADAPTER
  U-X1 (DEL-04-01), U-X3 (DEL-02-03), F-3 (DEL-01-01); EXEC U-E3 (DEL-04-01
  with the owner), U-E4…U-E8; ACT U-03; the two pending owner questions in
  DECISIONS_PENDING_2 (D5 data boundary; D6 App hold points). SQ-16 and SQ-02
  ask only the host's side of D5 and D6.

---

## 4. Relay and return ledger (to be kept by the App manager)

The ledger records facts only when evidence exists. Nothing below has
occurred.

| Field | Current value |
|---|---|
| Prepared | 2026-09-28, DEL-09-06/RELAY-v0.1, by W9 (Type 2 TASK) |
| Relayed to the SWBPIPE session (by whom, when, what bytes) | **not observed** |
| Acknowledged | **not observed** |
| Answers received (per SQ; source, revision, date, custody) | **none** |
| Commitments stated by the SWBPIPE owner (per SQ) | **none** |
| Contributions delivered (identified revision/candidate) | **none** |
| Adopted on the App side (which file, which version) | **none** |
| Examined (candidate-bound observation) | **none** |

Per-answer record, when one arrives: SQ id; answer text or reference;
answering party; source/candidate revision; date as evidenced; custody
(how the file reached this repository); standing (**answer** ·
**stated intention** · **commitment** · **delivered contribution**);
dependent App items to update; limits. An answer is never copied into App
files as though it were an App decision.

---

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| Delivery of this file to the SWBPIPE session | The human (relay) | Before any answer can be recorded | All questions open; §4 ledger empty |
| Every SQ-01…SQ-27 answer | SWBPIPE outside implementation owner (DEP-001) | As stated per question | Dependent App cases stay AWAITING INPUT or HELD |
| `UNRESOLVED{OI-021}` selection itself | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution | SQ-04/SQ-05 inform it; they do not make it |
| `UNRESOLVED{OI-003}` extension disposition | Owner with host contract owner | Before extension claim or criterion | SQ-26 gathers evidence only |
| Pending owner decisions D5 (data boundary) and D6 (App hold points), DECISIONS_PENDING_2 | Owner | Before enabling a live candidate (D5); before App-side hold fixtures (D6) | SQ-16 and SQ-02 ask only the host side |
| Closeout pointer from HANDOFF_SWBPIPE_DOMAINS.md to this file | Closeout C1 | C1 | HANDOFF not edited here |

## Verification cases

Designed, not run.

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-R-01 Coverage | Walk every source item in LOOP §13, PANEL §8, ADAPTER §12, ACT U-04, EXEC §9.1 host row and U-E list, R2-20 and HANDOFF responsibilities table against §3 | Every item maps to at least one SQ; exclusions stated with reason | VER-005 (AC-005) |
| VC-R-02 Field completeness | Inspect each SQ | Question, dependents, why, point of need, App assumption and answer form all present | VER-005 |
| VC-R-03 Priority | Check P1 order | SQ-01 and SQ-02 first; every positive checkpoint case in EXEC, LOOP, PANEL, ADAPTER and DEL-09-06/09-09 traces to a P1 question | VER-005 |
| VC-R-04 Standing | Inspect header, §0 and §4 | "PREPARED FOR HUMAN RELAY — not delivered"; no answer, commitment, delivery or adoption claimed; PR #885 evidence-only | VER-005; VER-008 of DEL-09-06 |
| VC-R-05 No assignment | Read every question and assumption | No SWBPIPE construction assigned; no App assumption presented as a host commitment; owner decisions credited only with what they say (R2-11) | VER-008 (AC-008) |
| VC-R-06 Return handling (when answers arrive) | Record a returned answer in §4 and trace it to dependent files | Source, revision, date, custody and standing recorded; dependent cases change state only when the named input is supplied | VER-005 |
