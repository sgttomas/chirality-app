# R2 integration resolutions — v0.2 → v0.3 alignment

Integrator: HELP_HUMAN. Inputs: [IR1-A](reviews/IR1-A.md), [IR1-B](reviews/IR1-B.md),
[IR1-C](reviews/IR1-C.md) and [R2_CANDIDATES.md](R2_CANDIDATES.md). All three
reviews found **0 BLOCKING** and judged the set fit to merge as v0.2 drafts.
They found 23 MAJOR and 43 MINOR items, which these rulings settle.
Labels are used as in R1: SETTLED, DERIVED, INTEGRATION, PROPOSED. R1 rulings
stay in force unless amended here.

**For every MINOR item a reviewer raised:** apply the reviewer's proposed
resolution unless a ruling below contradicts it. **Read your siblings' v0.2
text** where a ruling touches a join (all files are committed at `c387730fb`).
Write only in your own `Design/` files.

## Vocabulary and policy (owner: DEL-04-01; all adopt)

- **R2-1 Fifth class value.** Its name is **no policy basis**, with a *reason*
  sub-element ∈ {omitted, unassigned, pending OI-021}. It is labeled
  INTEGRATION (from R-3.5), not SETTLED. DEL-03-01, DEL-03-02 and DEL-05-01
  replace "policy basis pending" and list five values. (IR1-A M1; IR1-B M1)
- **R2-2 Reserved operations (X-1, amended per IR1-A).** An operation that
  *performs* A4, A5, A6, A7, A10, A12 or A13 is **reserved to the person**.
  This includes an operation that changes the host's own act state. No
  faithful record is made through such an operation. A host-offered
  faithful-record operation, if any, must satisfy all of these:
  - it does not change act state;
  - it cites capture evidence;
  - it never satisfies a checkpoint;
  - it takes ordinary policy.

  Whether any host offers one is a relay question (DEP-001). DEL-04-01 P-02
  adds A10. DERIVED.
- **R2-3 Disabling external access** is also a person's setting change,
  recorded as A13. INTEGRATION: D2e names *enabling*. DEL-04-01 must not label
  disabling "adopted by D2". An agent may request it (A8).
- **R2-4 Reserved entries are always offered.** They are never withheld for a
  class reason and never reported "not exposed on this surface". An agent call
  returns **not permitted** and *offers* an A8 request; it does not record one
  automatically. "Not exposed on this surface" arises only from the
  per-surface exposure element and is **reported by the host**. The loop
  splits V-2:
  - an operation absent from the catalog edition offered to the loop is a
    loop-side **not offered** failure and is never dispatched;
  - a host-returned "not exposed" is relayed.

  DEL-04-01 changes §6 row 8, FX-35 and closes U-11. (IR1-A M2; IR1-B M4/M5)
- **R2-5 Act-declined event (X-2 amended).** The name is **act-declined event**,
  for A4, A6, A7 or A12, with capture evidence. Its checkpoint disposition is
  **resolved negatively**. Stopping a run is a separate **run-ended event**,
  and the checkpoint stays *waiting* (X-12). An act performed after the run
  ended is recorded but does not change the ended run's disposition unless
  DEL-02-03 defines resumption. DEL-04-02, DEL-04-03, DEL-05-01 and DEL-05-02
  add A12. (IR1-A M3; IR1-C IR1C-06)
- **R2-6 Default grant (X-4 amended).** Add the display state **effective
  (policy default)**:
  - It requires no A12.
  - Settings-in carries the policy-class record reference and its default,
    with no setting actor or requester.
  - "Not set" means no setting and no default.
  - A default opens the direct branch only if the policy record's default is
    *direct*; no such default exists in the first increment.

  (IR1-A M5)
- **R2-7 A12 binding (X-13 amended; PROPOSED).**
  - A12 binds to the **setting content**: classes, grant values and scope.
    The established version or the control's refusal is a relation on the act,
    not its content.
  - A later A12 **supersedes** an earlier one and does not lapse it. A
    checkpoint the earlier A12 satisfied stays *performed*, with the
    supersession shown.
  - Held for DEL-02-03 (W7): whether an A12 that the control refuses can
    count at a checkpoint. (IR1-A M4)
- **R2-8 Tool-permission settlements (X-3).** A14 is recorded only in run
  record R13. It is never in R6, never a human-act record and never a grant.
  This closes DEL-04-01 U-07 and DEL-04-03 U-10. It does not apply in
  host-loop runs.
- **R2-9 No-policy-basis wording (X-15 amended).**
  - Proposing confers no permission; any effect requires the person's A5 and
    host application.
  - Direct is **not permitted**, and an A12 that widens such a class is
    refused.
  - The REQ-004 hold on dependent production stands. Fixtures report such
    cases as **held**, never as passes.
- **R2-10 Act kind outside the list.** A recognized act kind that is outside
  a checkpoint's allowed list is **invalid**. An unrecognized name is **not
  established**. DEL-04-01 §4.1 aligns with DEL-02-01.
- **R2-11 Attribution hygiene.** Credit D2/D3 only with what they say.
  Restrictions from R-2/R2 are INTEGRATION or DERIVED. This fixes IR1-A P-04,
  IR1C-17 (LOOP A-5, PANEL §1) and "disable" (R2-3).

## Proposal, catalog and outcomes (owners: DEL-03-02, DEL-03-01)

- **R2-12 Acceptance-checkpoint constraint (X-9, amended per IR1-B/IR1-C).**
  - P §3.3's change request gains a **governing checkpoint constraint**:
    {workflow run, checkpoint name, required act A5, operation}.
  - The loop and the external adapter both carry it.
  - A direct request under the constraint is **not permitted** and names the
    constraint as the governing treatment. P §4.4 and E-2 must not say the
    change is "drafted as a proposal" by conversion.
  - Relay question: does the host receive the constraint, or evaluate its own
    copy of the declaration? An omitted constraint is indistinguishable from
    none.
  - Until host evidence exists, LOOP FX-C9, PANEL PC-24 and WD VC-11 are
    **AWAITING INPUT**. (IR1-B M2/M3; IR1-C IR1C-03)
- **R2-13 Retry vs stale (IR1-B M7).**
  - **Identity-based de-duplication precedes the basis check.** Resubmitting
    the same proposal identity returns that proposal's recorded state or
    outcome and is never refused as stale because of its own effects.
  - The per-item basis check compares the **subject content identities of the
    item's relied-on targets**, not the global revision. Applying sibling
    items of the same proposal does not stale remaining items unless they
    share targets.
  - Fix C T13.
- **R2-14 Applied outcome identifies resulting objects (IR1-B M6).** P §9 and
  C §9 add, per applied item: the created and changed object identities and
  their subject content identities after application. Consumers use these for
  subject binding and reached-when kind (c).
- **R2-15 Undo (X-5 amended).**
  - The relation name is **reverses ⟨receipt⟩** everywhere.
  - Acts bound to content the undo changes **lapse normally** (S6/V4-HI-32).
    P §4.5 is reworded.
  - DEL-04-02 shows "applied, then reversed".
  - C adds a fixture entry **OP-C10 Undo (reverse a receipt)**, class *may
    apply within granted autonomy*; its mechanism is a host input.

  (IR1-A M6)
- **R2-16 Stale after acceptance (X-8).**
  - Display: "accepted by ‹person› — not applied: refused — stale (both
    bases)". The A5 is not lapsed.
  - DEL-04-03 and PANEL narrow their open item to host evidence.
  - The checkpoint effect follows R2-18.

## Checkpoints and binding (owners: DEL-02-01 declares; DEL-05-01 evaluates)

- **R2-17 Subject class independent of reached-when (X-10, IR1C-01/05).**
  The declared **subject class** is its own element and does not depend on
  the reached-when kind. Classes:
  - change items of a named proposal;
  - named output;
  - objects changed by a named outcome;
  - **targets of the held call**, bound through the subject content
    identities of the relied-on read;
  - grant setting.

  Further rules:
  - The loop binds the *declared* subject class.
  - An A5 checkpoint must use reached-when kind (c) *proposal queued*, and its
    subject is that proposal's change items.
  - DEL-04-01 §4.2 adds the held-call targets and the grant setting as
    referents.
- **R2-18 Mixed item decisions (X-14, amended; PROPOSED).**
  - WD §4.3.7 is the proposal all files cite. LOOP C-7 and PANEL W-5f cite
    it and no longer mark it independently unresolved.
  - "Partial" is a **per-item annotation**, not a seventh disposition.
  - Items that leave without a decision are shown. A *performed* over a
    reduced subject is never shown as "all accepted".
  - DEL-03-02 supplies item-left events.
  - DEL-02-03 confirms at W7.
- **R2-19 Lapse before resume (IR1C-07).**
  - One sequence: an **act-lapsed event** is recorded, and the disposition
    returns to **waiting** ("waiting — lapsed at ‹t›").
  - After resume, re-hold belongs to DEL-02-03.
  - "Lapsed" as a standing disposition is used only for a checkpoint whose
    run has ended.
- **R2-20 Holding library, run end, capture evidence, guidance (X-11, X-12,
  X-17, X-18, as amended by IR1-C).**
  - The holding library is recorded at the listed, selected and resolved
    links. It is shown by the panel and carried in the loop's run
    association. It never takes part in identity equality. PROPOSED until W7.
  - Capture-evidence reference: relay question. Without it, no host-content
    checkpoint can be *performed*. The same need exists App-side (U-25).
  - Per-turn supplied-guidance source identity and content identity: relay
    question. Where the host cannot record it, the record says *unknown*,
    aligned with HOSTING §8.2. "Supplied ≠ adopted" applies.

## Shared fixture (owner: DEL-03-01 §10; all re-point) — X-6

- **R2-21** C-v0.3 §10 remains the only fixture catalogue and timeline.
  - C adds:
    - **OP-C10 Undo** (R2-15);
    - **OP-C11**, an entry whose class is **no policy basis** (reason:
      pending OI-021);
    - exposure values for the fixture: **exposed on all three surfaces**,
      labeled a fixture assumption, with any "not exposed" demonstration as a
      named variant;
    - a T15 grant scope expressed in the R-8 dimensions.
  - **OP-C3 stays "Examine" (A3 findings).** Where a fixture needs "host
    checks passed", C adds a host check entry.
  - Every consumer re-points to C §10 identifiers: OP-Cn, T-n, rows,
    revisions and PR-n proposals.
  - Local labels that collide with C (R-101, N-10, P-n, OP-C5 "adjust run")
    are removed. A genuinely needed local case is named `L-‹file›-n` and says
    why.
  - To allow parallel repair, consumers use the C-v0.2 §10 identifiers now
    plus the IDs fixed above (OP-C10, OP-C11). C must keep every C-v0.2 ID
    stable.

## Hosting and spike housekeeping (owner: DEL-01-01)

- **R2-22** Resolve IR1-C's HOSTING items:
  - §6.1/§6.4 consistency on `currentTime/read`;
  - cite the current PIN_SPIKE hash, which the parent edited after IR1;
  - P-01 "refines", not "contradicted";
  - retire the stale F-17;
  - VC-07 cites the committed-state note
    `generated/0.158.0/COMMITTED_STATE.md` (added by the parent for IR1C-04:
    2 OK / 2,357 not committed on the committed tree; 1,605 TS files verified
    OK from the scratch copy).

## Carried to closeout C1 (no R2 edits)

- SoW text in DEL-03-01, 03-02, 04-01, 04-02 and 04-03 still calls OI-001 and
  OI-002 open. C1 records the DECISION-1 pointer through the owning route.
- All register findings: V1 RF-* plus X-16.
