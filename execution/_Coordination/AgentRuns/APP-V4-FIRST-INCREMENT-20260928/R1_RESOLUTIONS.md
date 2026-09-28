# R1 integration resolutions — Wave-1 v0.1 → v0.2

Integrator: HELP_HUMAN (graph maintainer). Inputs: [V1-A](comparisons/V1-A.md),
[V1-B](comparisons/V1-B.md), [V1-C](comparisons/V1-C.md) and
[OWNER_DECISIONS.md](OWNER_DECISIONS.md). These resolutions settle
cross-file disagreements that the Wave-1 definitions and the accepted basis
already allow. They are integration rulings within the definition scope. They
are not owner policy acts, and they select no wire representation. Each is
marked **SETTLED** (basis or owner ruling), **DERIVED** (follows from cited
rules) or **INTEGRATION** (a design choice by the integrator; reviewable at IR1
and open to owner revision). Repairers apply them. A repairer who finds one
wrong returns a finding and does not diverge.

Where a V1 comparison proposes a resolution not contradicted below, the
repairer applies it. The numbered rulings take precedence.

## R-1 Canonical act names (owner: DEL-04-01) — resolves V1-A D-01, D-17, D-18, D-20

| ID | Canonical name | Basis aliases mapped to it | Notes |
|---|---|---|---|
| A1 | propose | draft/submit a proposal | Agent or person |
| A2 | apply | execute an operation; direct application | Operation outcome, not a judgment |
| A3 | examine | agent check, examination, findings | Never "checked" (R-4) |
| A4 | mark checked | marking work checked | Reserved (D2a) |
| A5 | accept | accept an edit; accept a proposed edit; acceptance of a proposed edit | Reserved where autonomy requires a proposal (D2b); bound to change-item content (R-6) |
| A6 | approve | engineering approval (V4-HI-30/33) | Reserved (D2c). **Not** V4-CON-05/HI-65 design-candidate approval, which is a separate later-increment act outside this increment |
| A7 | rely | professional reliance; accepting professional reliance (d3, V4-CON-05 wording) | Reserved (D2d); "accept" wording stays with A5 only |
| A8 | request | prepare or request a person's act | Agent-available; establishes nothing |
| A9 | record | faithful recording (actor ≠ recorder) | **A recording act by the recorder, not a decision act.** It never satisfies a checkpoint by itself. The sub-element *recording mode* ∈ {direct capture, faithful recording} |
| A10 | reject | reject a proposal or proposed item; person removing another's proposal | Decision pair of A5; DERIVED: reserved to the person wherever A5 is |
| A11 | withdraw | withdraw one's own proposal | Proposer only |
| A12 | set grant | set or change the autonomy grant | Reserved (D2e); recorded as a human act |
| A13 | enable external access | enable/disable external-agent access | Reserved (D2e) |
| A14 | answer tool permission | harness "approval" of tool use; routine permission | Governed by D3; never a professional act |

Every consumer uses these names. Checkpoints may require A4, A5, A6, A7 or A12
(closed list, DERIVED from V1-A D-20). Unrecognized names remain "not
established" (DEL-02-01 FB-04).

## R-2 Owner rulings in the policy representation (owner: DEL-04-01) — SETTLED

- DEL-04-01 §6 "adopted decisions" carries D2 and D3 as adopted records citing
  `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`. The blanket
  `UNRESOLVED{OI-001/002}` statements across all files are narrowed to what
  remains open: operation-specific additions (OI-021); consequence vocabulary
  (DEL-04-01 with host policy owner); multi-row A4 purpose after partial lapse
  (owner question, owner: DEL-04-01 with Owner); host capture requirements
  (DEP-001).
- A catalog operation whose effect is to perform or record A4–A7, A12 or A13
  as the person's act carries class **reserved to the person** (DERIVED from S3
  and D2). DEL-03-01 OP-C6 "Mark row checked" and DEL-05-02 K-4 carry it.
- The SWB model-change class value is **may apply within granted autonomy**,
  marked DERIVED from V4-HI-41 "the person may widen it", with the accepted
  default setting of *propose*. OI-021 additions are pending. DEL-03-01
  OP-C4/C5, DEL-04-02, DEL-04-03 and DEL-05-01 cite the DEL-04-01 record
  instead of blanket UNRESOLVED.
- D3: App routine tool-permission and sandbox modes are the user's own Codex
  setting and are carried unchanged. The DEL-04-01/04-02 autonomy grant governs
  **host operations only**. No App rule answers a tool-permission request
  affirmatively. An App explicit decline or error is permitted only under a
  named rule with truthful origin. Hosts have no classifier mode. `OI-002` is
  removed as a class value everywhere (V1-A D-23).

## R-3 Treatment → runtime outcome (owner: DEL-04-01; consumers cite) — V1-A D-04, D-05, D-08

1. Treatment is resolved on the **host route** at validation and again at
   application (V4-HI-20/22/40). The loop and the external adapter relay the
   actor's intent and do not decide treatment. INTEGRATION
2. Runtime non-success outcomes use DEL-03-01 §4.1 unchanged:
   - **unavailable**: failed catalog precondition, HI-04 parity only;
   - **channel not enabled**: external access off, A13 not performed;
   - **not permitted**: treatment forbids the requested mode, naming the
     governing treatment and policy record;
   - **error**.
3. A request to apply directly without an effective *direct* treatment →
   **not permitted**. It is never silently converted into a proposal.
   INTEGRATION
4. *Request the person's act* at runtime → **not permitted**, plus an A8
   request.
5. A class with **no policy basis** → direct not permitted, propose available
   (conservative default, V4-HI-41). INTEGRATION
6. Record both the standing **at drafting** and the treatment **at resolution**
   (validation; application) when they differ. The in-flight effect of
   narrowing a grant is DEL-04-01 policy plus host enforcement (DEP-001):
   - an already-queued proposal is unaffected;
   - an operation not yet applied is re-resolved at application.

   INTEGRATION
7. Widening a grant never converts a queued proposal into direct application.

## R-4 Label rule for "checked" (owner: DEL-04-01) — V1-A D-12, V1-B D-15

- Unqualified "checked" / "Checked" is reserved for **A4**.
- Host results say **"host checks passed: ‹named checks›"**, each check with
  its evaluated basis.
- Agent work is **"examination" / "findings"** (A3). DEL-02-01 "agent-checked"
  becomes "agent-examined (non-mutating)".
- "Later-check route" means access for later examination or checking and
  implies no act.
- "Approval" in UI or records means only A6. Harness tool-use prompts are
  "tool permission" (A14).

## R-5 Checkpoints (owners: DEL-02-01 declares; DEL-05-01 evaluates in hosts; DEL-02-03 owns hold machine at W7) — V1-A D-09/D-10, V1-C D-01…D-07

- **Reached-when (resolves V1-C D-01 BLOCKING).** Each checkpoint declares an
  observable *reached-when* condition, as meaning only, of one of these kinds:
  - before dispatch of a named required-tool reference;
  - on observed production of a named declared output;
  - on an observed host outcome of a named operation (e.g. proposal queued).

  The prose position stays as explanation. If the run ends without the
  condition being observed, the checkpoint is reported **not reached**, never
  satisfied. DERIVED from LOOP E-1.
- **Subject binding.** The checkpoint's subject is bound at run time to an
  observable referent: the proposal/change items, the output, or the rows
  produced. The satisfying act must be bound to that same referent's content.
- **Dispositions (shared vocabulary):** waiting · performed · resolved
  negatively · lapsed · not reached · unknown. For A5, the negative decision is
  A10 (reject). For A4/A6/A7, a person's decision not to act is a recorded
  **decline/stop event**. It is not an act of that kind and does not satisfy
  the checkpoint; the declaration's "on negative decision" path governs what
  happens next. Lapse may occur **at any time** after performance. Re-hold is
  owned by DEL-02-03.
- **Acceptance checkpoint forces proposal (DERIVED from V4-HI-42 + D2b).** If
  a checkpoint requires A5 on an operation's result, that operation's
  treatment is *propose* regardless of the grant. DEL-02-01 E2 R-5/VC-11 are
  rewritten accordingly, or changed to require A4 on applied rows.
- **Which evidence satisfies a checkpoint (V1-A D-11, V1-C D-06).** Faithful
  recording (A9) by any identified recorder distinct from the decision actor
  is a conformant record shape (S3, settled). Satisfaction requires
  attributable act evidence from the **capturing surface**:
  - the host's act facility for acts on host content (V4-HI-31);
  - the App interface for acts in the App.

  A faithful record by another recorder is valid as a record and must cite
  that evidence. The loop resumes on that evidence, not on an agent-authored
  record alone. Any host-specific capture requirement is the host's (DEP-001).

## R-6 Content identities and acceptance binding — V1-B D-01/D-02/D-03/D-10 (BLOCKING)

- **DEL-03-01 adds:**
  - **subject content identity**: per object/row in a read result,
    host-supplied, distinct from the read-basis canonical content identity;
  - **identity method designation**: accompanies every content identity at
    basis and subject level.

  The algorithm stays unselected, and scope is a host input (U-C2/U-C3).
- **DEL-03-02 adds a change-item content identity:** operation identity and
  version, bound targets, old/new values, and relied-on basis.
  - A5 binds to the change-item content identity. Applying the accepted item
    does **not** lapse the acceptance.
  - A basis failure between acceptance and application falls under the stale
    rule (U-P3), not model-row lapse.
- **Acceptance unit = change item.** Row-by-row acceptance is one A5 per item.
  Batch or multi-row acceptance is one A5 act listing several items, each
  item-bound, with per-item lapse (V4-HI-41).
- **DEL-04-03 L-1 has three c₁ sources:**
  - change-item content identity (DEL-03-02) for A5/A10;
  - subject content identity (DEL-03-01) for acts on host rows/objects (A4,
    A6, A7);
  - file content identity for App files.

  L-2 compares method designations. RS E1 and VC-09 are restated. VC-09
  becomes an A4 on rows with a subsequent row edit, for the model-row partial
  lapse.

## R-7 Outcome vocabulary (owner: DEL-03-02 §9; consumers adopt unchanged) — V1-B D-04/D-05/D-09, V1-A D-16/D-24, V1-C D-11/D-12

- P §9 is the canonical proposal/operation outcome taxonomy. Add
  **application error** (with an effect statement: none / partial / unknown).
  A host refusal on validation is a **refused** outcome; "rejected" is only
  A10.
- DEL-04-03, DEL-05-01 and DEL-05-02 adopt P §9 and C §4.1 unchanged,
  including:
  - item dispositions;
  - last observed state;
  - both bases on stale refusal;
  - the evaluated basis on every non-success;
  - accepted / rejected / withdrawn relayed with actor (A5/A10/A11).
- **Outcome unknown** is reported by whoever lost observation: the loop, the
  App adapter or the host. It is attributed to that observer.
- Duplicate submission (DEL-04-03 OE-3): record each submission separately
  with only the effects actually observed. "One effect" is a host obligation
  to be evidenced (DEP-001), not a recorded fact.
- A retry keeps the same proposal identity (V1-C AB-05). Every dispatch
  carries origin, seat role meaning and the grant in force (V1-C AB-02…04).

## R-8 Autonomy grant and the M3 exchange (owners: DEL-04-02, DEL-04-03) — V1-A D-06/D-07, V1-B D-06/D-07/D-11/D-12/D-13

- **Grant display states:**
  - effective;
  - requested by agent (A8; no person act);
  - set by person, not yet confirmed by control;
  - unconfirmed;
  - not set;
  - refused (reason).
- The grant has a **scope** element. Its dimensions are representation-neutral
  (e.g. model/workspace, object set, run, period, consequence). This closes
  DEL-04-01 U-08.
- Settings-in carries **requester** and **setting actor** separately. A
  person-set state requires A12 act evidence (D2e). The direct branch applies
  only in the **effective** direct state.
- Two settings references are recorded per operation:
  - at route decision (validation);
  - in force at application, host-reported; otherwise **unconfirmed**.
- Record-out adds, for the display:
  - bound subject;
  - c₀/c₁;
  - recording mode;
  - evidence references;
  - act class;
  - checkpoint events.

## R-9 Identity, generation and fixtures — V1-C D-09/D-10/D-14, V1-B D-20

- Workflow identity is carried everywhere as {kind, origin, source root, name,
  revision} (+ derived-from). The P, LOOP and PANEL "identity/version" elements
  are replaced by it.
  - A workflow carried unadapted keeps its original origin.
  - Host adaptation creates a new identity with host origin and derived-from.
  - "App-origin" is not an origin class.
- **Generation** is a host lineage epoch (U-C2). An intervening edit changes
  the **model revision**. Fix LOOP FX-D2.
- **Exposure vs channel:** an operation not exposed on a surface is reported as
  *not exposed on this surface*, distinct from *missing* and from *channel not
  enabled*. DEL-03-01 adds a per-entry, per-surface exposure element (the value
  may be "unagreed").
- **Shared fixture:** DEL-03-01 §10 owns the one invented fixture catalogue and
  timeline. The model identity is **FX-PIPE-01**. Other files cite its
  entries; where a fixture must diverge, they say why.

## R-10 Hosting boundary (DEL-01-01) — V1-A D-13/D-14, V1-C D-16, D4

- Apply R-2's D3 bullet to H9, R7, §2, U-04 and F-09. A14 affirmative answers
  come only from the person, or from the user's own Codex mode inside the
  supplier.
- D4: header, §10 and U-01 state pin `0.158.0` (owner decision). Incorporate
  W11 observations from `Design/PIN_SPIKE_0.158.0.md`, marking each
  observed / not observed / contradicted.
- Supplied-guidance evidence records the identity (content identity) of each
  guidance input actually supplied, per thread and turn, not only the launch
  configuration (V1-C D-16).
- Responses-API statements stay unobserved unless W11 observed them.

## Register findings

V1-A RF-01…05, V1-B's nine and V1-C RF-1…9 are **not** repaired in R1. They go
to closeout C1 and the D0 currency check. A relationship that is genuinely new,
as opposed to a missing mirror row, is routed through `project-dag` departure.
