# R23 rulings — on the tranche-1 surveys (S1-A, S1-B, S1-C)

Integrator: HELP_HUMAN. R1–R22 stand. Labels as before (SETTLED, DERIVED,
INTEGRATION, PROPOSED). Owner-reserved items are not ruled here; they are in
[DECISIONS_PENDING.md](DECISIONS_PENDING.md).

- **R23-1 Examination vocabulary (S1-B SQ-2). INTEGRATION.** DEL-09-01 maps
  its examination record to HOSTING §9.3's outcome states; it does not govern
  them, because DEL-01-01 cannot consume DEL-09-01 without a cycle. No shared
  core record restructures CA §8.4 or XT §3.4 in this pass. HOSTING may align
  its own spelling later on its own authority.
- **R23-2 Cycle-safe directions (S1-A S-6; S1-B SQ-4). DERIVED** from DAG-004
  reach over both layers. A decision package reaches DEL-01-04's act control
  as a runtime value, not through a register row from DEL-06-02. Bundle
  seams are framed as DEL-02-02, 02-04 or 01-04 → DEL-01-06 ("the package
  places and signs what I ship"), never the reverse. Any proposed row is run
  through the reach script before it is proposed.
- **R23-3 Codex pin (S1-B SQ-6; node VC). INTEGRATION.** Pass-4 designs are
  written for either pin (0.158.0 or 0.160.0) where the two may differ. Each
  return names the pin basis it used. When VC returns, HELP_HUMAN names the
  boundary at which 0.160.0 facts are adopted; work done on 0.158.0 facts
  stays valid unless VC shows a changed fact it relies on.
- **R23-4 Child index (S1-A S-5). INTEGRATION.** DEL-06-01 holds any durable
  index of children; RECOVERY's ledger is unchanged.
- **R23-5 Design re-pins (SCA-V4-003 derivative closure). INTEGRATION.** An
  owner who revises a Design file re-pins it to the current ScopeOfWork hash
  after reading the SCA-V4-003 blocks that changed that ScopeOfWork, and
  says in the file which blocks bear on it. Files no pass-4 owner touches are
  re-pinned by script with the same check at the pass closeout. No separate
  re-pin undertaking.
- **R23-6 "A week later" (S1-C C4). DERIVED, revised.** The interval is
  the accepted basis's (EXAMINATION V4-EXM-31: "A week after V4-EXM-20"),
  carried into DEL-09-11's contract. Its purpose is that the reconstruction
  happens after the run's sessions and its author's working context are
  gone, so it tests whether the files and host receipts stand on their own
  (V4-PM-05; V4-REC-01…05). The design keeps the basis's wording and adds no
  calendar arithmetic of its own; the witness is scheduled so it holds up no
  other work. (The first version of this ruling added "at least seven
  calendar days"; withdrawn as an addition the basis does not make.)
- **R23-7 Overtaken ScopeOfWork wording (all three surveys). DERIVED.** The
  designs follow the current decisions (first-increment D2/D3/D4, L-6, L-7,
  DEL-01-04's App act control), not the older ScopeOfWork wording. Carrying
  that wording to the next amendment, as the owner did for DEL-09-02's
  OI-009: see R23-11.

## Rulings replacing questions first put to the owner (K-1…K-10)

The owner's direction of 2026-10-03 (OWNER_DECISIONS.md, "Scope of owner
questions") returned these to HELP_HUMAN: the established act ontology,
evidence rules and the owner's earlier decisions already settle them.

- **R23-8 A person's decision on a decision package (was K-1). DERIVED.**
  V4-PM-04 already says a reserved decision "arrive[s] as [a] decision
  package naming the exact act requested, with alternatives and
  consequences". So:
  1. The package is an A8 request (ACT §2.1), recorded as RS R16
    `act_request` (RS §13.6) with two added elements, alternatives and
    consequences. DEL-06-02 derives its view from that record (V4-PM-06).
    No new PKG-06 record and no amendment are needed for the package (this
    answers S1-A S-2).
  2. The person's decision is the act the package names. Where that is an
    existing kind (A4–A7, A10, A12, A13, A15) it is that kind, captured by
    that kind's surface.
  3. ACT §2.1 already lists "reserved coordination decisions (V4-PM-04)"
    among human acts without a canonical name. It gets one, **A16 decide**,
    as R12-5 gave A15 one: decision actor the person; subject one package
    and the alternative chosen; evidence captured by DEL-01-04's App act
    control and recorded under RS HA-1; not D2-reserved; no agent performs
    it. Which decisions are reserved does not change: that is set by the
    governing workflow or accepted instrument the package cites.
  4. The rows are added by O-A to ACT §2.1, RS §6.1/§13.6 and its schema,
    and AAC §1.2. Each is a row, not a restructure.
  5. Chat statements stay non-evidence in the product (CAP-7, HA-1).
- **R23-9 Which delegations PKG-06 records (was K-2). DERIVED.**
  1. Delegation is an agent dispatching work, by an actual mechanism (Root
    `AGENTS.md`: Chirality-managed sessions or harness-native descendants
    under D-GOV-35). In the App that is native Codex children, recorded with
    their mechanism.
  2. A conversation the person starts with "Continue as" or a fork is not
    delegation (L-2). It is recorded as a related conversation (continued
    from, forked from).
  3. Work done elsewhere appears in the work graph as an owner and a result
    (V4-PM-02), from files.
- **R23-10 DEL-09-11's reader (was K-3). DERIVED** from the contract's own
  words: "a named reader, separate from the host-run author", person or
  agent. The record names the reader and the input set supplied; for an
  agent reader, its recorded supplied context shows the separation.
- **R23-11 Overtaken ScopeOfWork wording (was K-6). DERIVED** from the
  owner's "1 yes" for DEL-09-02. The same treatment is applied: the wording
  is listed for the next amendment, which reaches the owner at its own
  checkpoints.
- **R23-12 Candidate reviewer (was K-7). SETTLED** by V4-OPS-34 as written:
  a Codex reviewer, with the Claude fallback; actual separation and model
  identity are reported.
- **R23-13 Signing and native checks (were K-4, K-5). INTEGRATION.**
  1. Technical choices. O-B makes them on the facts and records them.
  2. Signing and notarising use the owner's Apple account when a package is
    made; that is the person's act at that time, not a decision now. OI-011's
    SWB co-owner part waits with the host joins.
- **R23-14 Not decisions (were K-8…K-10).**
  1. Privileged traffic capture is a permission the host asks for when it
    runs.
  2. The A12 mapping and boundary refusals stay in the SCA-V4-003 deferred
    queue (owner item Q-9) and go with the next amendment.
  3. The SWBPIPE relay list is prepared when host joins resume.

## On the first frozen unit (O-C, LHQ-U1)

- **R23-15 Stimuli inside the V4-EXM-20 run (O-C F-3). DERIVED.**
  V4-EXM-23 verifies its properties "during V4-EXM-20". A declined request,
  a grant during work and an allowed-in-advance destination can only be
  observed if they occur in that run, so LHQ-23 adds them as named stimuli
  inside the same run (from LOOP MS cases). They are marked as added
  stimuli, and V4-EXM-20's own parts and pass conditions do not depend on
  them. A partial capture is *inconclusive*, never *passed*.
- **R23-16 Fixture gaps (O-C F-1, F-2). INTEGRATION.** The local cases
  L-LHQ-1 (a solve) and L-LHQ-2 (a third PR-2 item) stand in DEL-09-07.
  DEL-03-01's FX-PIPE-01 adopts them at its next revision; until then
  DEL-09-07 cites them as local additions.

## On O-B's first frozen unit (DEL-09-01 EXP-v0.1)

- **R23-17 Items EXP left to "the App implementation owner" (U-EXP-1, 2,
  4). INTEGRATION.** These are not owner questions (owner direction
  "Scope of owner questions").
  1. **Digest (U-EXP-4):** sha256, the digest used throughout the project's
    records. DERIVED.
  2. **Qualification pin (U-EXP-1):** HELP_HUMAN names it when VC returns
    (R23-3).
  3. **Runner and UI-automation tool names (U-EXP-2):** chosen by the
    implementer against EXP §8's definition check, and recorded as a fact
    of the result.
  4. **Where records live and the form layout (U-EXP-3):** O-B's ordinary
    decision, within OI-013/OI-014's constraint that no common service is
    presumed.

## On the early path (O-A, E-1) and RV's first reviews

- **R23-18 The early path's missing rows (O-A escalation). INTEGRATION.**
  The early path found what R23-8 had not reached: the act-request body
  lives in DEL-02-03's `checkpoint-record-entries.schema.json` (CE-4; RS
  §13.3, R14-1), CE-10's `actRef` lacks A16, and DEL-01-04's `aac.offer`
  and `aac.capture-evidence` schemas have no A16 and no place for the
  alternatives or the chosen alternative.
  1. O-A applies PR-1…PR-13 as stated in `E/proposed_rows.json`. All are
     additive, and none narrows or relaxes a check.
  2. O-A also adds A16 to the lists that do not yet name it: RS §13.3's
     table row, an RS §6.2 HA rule for A16 (as HA-10 is for A15), ACT §2.4,
     §9 labels, §10.1 V-01 and the A9 row's act list, and AAC §2's interface
     row for the runtime value from DEL-06-02.
  3. The package file is the CE-4 request body with PR-2's `form` value; no
     second shape.
  4. DEL-04-01 ScopeOfWork REQ-002 naming A16 is carried to the next
     amendment (R23-11).
- **R23-19 Parts that do not apply (RV EXP-R-A, LHQ-R14). DERIVED** from
  the rule that scope is never decided after seeing results.
  1. A part may be declared not applicable only in the case definition as
     bound to its fixture, before the run, with its reason.
  2. Aggregation leaves declared not-applicable parts out.
  3. A part declared applicable that did not run is `not-run`, and the case
     cannot pass.
  4. EXP-R1 and LHQ LR-4 both follow this.
- **R23-20 `blocked` and `not-run` (RV EXP-R-B, LHQ-R14). INTEGRATION.**
  HOSTING §9.3 names the labels without defining them.
  1. `not-run`: the case was planned for the candidate and not attempted.
  2. `blocked`: it was attempted, at its start or later, and a stated
     precondition or dependency stopped it; the cause is recorded.
  3. Every planned case gets a record, including `not-run` (DEL-09-11 REQ-4
     style: partial, failed, blocked, not-run and inconclusive results are
     recorded honestly). EXP therefore records a case blocked at its start,
     as LHQ LF-1 does. The label is INTEGRATION, not SETTLED.
- **R23-21 Shared inputs that change during the pass (RV; workflow §5).
  INTEGRATION.**
  1. **Rulings are cited by ID** (R23-n), not by the hash of this file.
     From here on this file is append-only. A changed ruling gets a new ID
     that names the one it supersedes. R23-6's revision before any citation
     stands as revised.
  2. **Shared Design files get a new version label** when a pass-4 owner
     changes them under R23-18: RS, ACT, AAC and DEL-02-03's checkpoint
     schema.
  3. **Dependents keep their pins** to the version they relied on, and that
     evidence stays valid where the change does not touch their reliance.
     An owner that relies on the new rows (A16) adopts the new version and
     says so.
  4. **At the pass closeout,** a script lists every stale sibling pin. Each
     is re-pinned after checking that the change does not touch its
     reliance; otherwise it goes back to its owner. The GUIDE pin set is
     included.

## On the version-advance check (VC)

- **R23-22 Codex pin after VC. INTEGRATION.** VC found four small additive
  or documentation-only protocol differences (Δ1…Δ4), one fork change and
  one bundled skill removed, with every relied-on behaviour unchanged in
  the reruns (`VERSION_ADVANCE_0.160.0.md`).
  1. The definition and generation pin stays 0.158.0, as the owner set it
     in first-increment D4. 0.160.0 is recorded as checked and
     design-compatible.
  2. The qualification pin (OI-012; EXP U-EXP-1) is chosen when a candidate
     is built: the newest version that has passed a version-advance check
     of this kind by then. Advancing is routine maintenance (the owner:
     "Pinning can only last so long"), so no new owner decision is needed
     unless a check finds a changed relied-on behaviour.
  3. **Carried to owners:** NIR L396 is reworded for Δ3 ("failed or
     interrupted"), with a defence for an interrupted turn that carries an
     error (O-A, with its DEL-01-04 rows). Δ1 and Δ2 are optional and are
     noted for WR SC-3, RECOVERY R-4 and ADAPTER, with no edit now. The
     dated values in OBS_3 L191 and the PIN_SPIKE/OBS records remain true
     of 0.158.0 and are not edited.
  4. **VC's deviations are accepted as recorded.** The memory pressure 4
     came after the model load and before any Codex process, as OBS-2 D-1.
     The user name reached only the loopback provider. **For later runs,**
     scratch Codex homes go under a path without the user name (for
     example `/tmp/cvx-<run>`), so that model input carries no personal
     path.

## On O-A's refreeze of E-1

- **R23-23 E-1 follow-ups. INTEGRATION.**
  1. PR-5 was written with `anyOf`/`const`/`enum` instead of `allOf`/`not`,
     so DEL-02-03's subset checker can read it. The meaning is unchanged,
     and an independent `jsonschema` run agrees. Accepted; RV checks the
     equivalence.
  2. O-A also adds A16's row to ACT §2.5 (per-kind content binding), as
     R23-18 item 2 intended, and corrects DEL-02-03
     `EXECUTION_COMPATIBILITY.md`'s stale "v0.6, unchanged at v0.7" line.
  3. The record formats (AAC 0.3, RS 0.1) are not bumped for additive rows,
     following RV21 and RS-v0.9; the Design files' version labels carry the
     change (R23-21).
  4. FX-DP1 changed only in its offer and capture files: the digest named
     in AAC-v0.3 §5.1 and the offer's key order. RR-E's account stays
     valid evidence for input set IS-FX-DP1-1, which it read. O-C's
     EP-05 and EP-11 adopt the new manifest, under a new input-set id.

## On RV's review of E-1

- **R23-24 The package file's shape. INTEGRATION. Supersedes R23-18
  item 3** (RV E1-R1). R23-18 item 3 ("the package file is the CE-4 body")
  was HELP_HUMAN's error: CE-4's `evidence` holds the package file's own
  hash, so the file cannot be that body, and the fixture's file did not
  validate against it.
  1. The package file is what the person decides on: package id, subject,
     purpose, the basis that reserves the decision, and the alternatives,
     each with its consequences. It gets its own `$def` in DEL-02-03's
     checkpoint schema, with valid and invalid examples. It holds no
     writer-supplied element and no hash of itself.
  2. The `act_request` record (the CE-4 body, PR-2's `form` value) is
     written by the recorder. It carries the requester, form, association,
     time and `evidence` (the package file's path and content identity),
     and repeats the alternatives as the file states them.
  3. DECISION_VIEW §7, RS §13.6, the fixture and O-C's EP units follow
     this. Adoption is checked in the returned files, not assumed.
  4. Affected work: E-1 (O-A) and FX-DP1. EP-05 and EP-11 (O-C) rely on
     the request record, not on the file's shape, so they re-run, not
     redesign. The RR-E account stays evidence for its input set.
- **R23-25 A second A16 on the same package (RV E1-R7).** O-A decides,
  consistently with how ACT treats repeated acts of other kinds, and states
  it. Earlier acts are never erased.

## On RV2's reviews of PKG-U2 and SQ-U3

- **R23-26 OI-011 for design (RV2 PKG-R10). INTEGRATION**, confirming
  R23-13.
  1. SIGN-1 (option B) settles the App-side signing arrangement for
     design purposes.
  2. OI-011 stays open in the Open_Issues register for its SWB co-owner
     part, which waits with the host joins, and for its record at the next
     amendment (R23-11). No executor edits the register.
- **R23-27 Conditions a scenario's own verification requires (RV2 SQ-R-A,
  SQ-R-B). DERIVED,** extending R23-15.
  1. Where a ScopeOfWork VER item requires a condition, the scenario's run
     creates it as a named stimulus, declared in the case definition before
     the run. Examples: a revision or source collision; unperformed-act
     negatives such as silence, timeout or an agent's claim; a delegated
     child that outlives its parent turn; a lost acknowledgment.
  2. Because the verification requires them, the parts that depend on them
     count toward that scenario's outcome (V4-EXM-10, V4-EXM-11). This
     differs from R23-15, where the stimuli served another examination.
  3. A condition that cannot be produced on the candidate is supplied by
     the replay counterpart, which is then required, not optional. If
     neither is possible, the part is `blocked` with its cause (R23-20). It
     never passes vacuously.

## Lifecycle

- **R23-28 Tranche-1 deliverables to IN_PROGRESS. DERIVED** from root
  SPEC §3 (`INITIALIZED → IN_PROGRESS`: "Human, WORKING_ITEMS (when
  semantic step is skipped)"). It applies to DEL-06-01, 06-02, 01-06,
  09-01, 09-02, 09-05, 09-07 and 09-11.
  1. Design work is actively under way, and HELP_HUMAN is coordinating as
     the WORKING_ITEMS function under the recorded consultation. The
     transition was made with `tools/scaffolding/write_status.sh`.
  2. It is not an owner question (owner direction "Scope of owner
     questions"). SCA-V4-003 Q-13 had put the earlier six to the owner
     only because they were moved inside an amendment checkpoint.
  3. The old `_STATUS.md` hashes appear only in historical input baselines
     and closed manifests (DAG-001, SCA-V4-001/002/003 closure inputs and
     initial-setup records). Those are verified at their own commits; a
     lifecycle file is expected to change after them, as the six SCA-V4-003
     transitions did.

## On the integration closeout (C1)

- **R23-29 C1's open items. INTEGRATION.**
  1. **GUIDE and A16.** GUIDE's M5.1 says "Canonical acts A1–A15", which the
     A16 rows have overtaken. A content edit is needed: GUIDE-v0.7 adds A16
     wherever its act lists or act-dependent rules require it, rows only.
     ACT, RS and AAC are then re-pinned, and the GUIDE pin check must end at
     25/25. Done by C2.
  2. **ACCESS.** Add the §13 register-table row already ruled in R22-7 (V22
     m-7; SCA-V4-003 block G-0105-02), then the ScopeOfWork re-pin (R23-5).
     Done by C2.
  3. **VERSION_ADVANCE §7.1** stays a dated record of the bytes VC read. C2
     adds one note line: its rows hash the working bytes at 04:04 UTC; six
     of them (AAC, ACT, RS, EXP, LHQ, TOP) are held by no commit and cannot
     be re-verified from git; the current versions are named in the R23
     rulings.
  4. **No action, recorded as limits** (workflow §6: no agreed condition
     requires them):
     - the 17 re-pinned files' `Dependencies.csv` pins and "Receivers"
       lines from before SCA-V4-003's register update;
     - PIN_SPIKE stays on its original ScopeOfWork (a dated observation,
       R9-10);
     - DOS's record-set standings omit RRM's `definition` standing (not a
       conflict);
     - an optional CA W14 narrative note for DEL-09-06's owner.

## After tranche 1

- **R23-30 Adopting D-GOV-52 in App v4; U-A9. INTEGRATION.** The owner
  approved A1 and B1 (OWNER_DECISIONS_2.md).
  1. App v4 adopts the changed Root text. ROLE-v0.2 F-R9 (the
     instruction-change notice difference) is closed by A1. The Root
     citations in HOSTING-v0.9 §2/§8.2 and ACCESS-v0.2 §9 now read against
     B1. Each file is updated at its next revision; no Design file is edited
     by this ruling.
  2. **U-A9** ("Whether the person may turn analytics back on for the App"):
     **yes**. The person can reverse the App's analytics-off session flag in
     the App. The reversal is the person's act, recorded like any other
     setting change, and never written to their `config.toml` by the App.
     This makes B1's "not a veto" fully true. ACCESS carries it at its next
     revision.
