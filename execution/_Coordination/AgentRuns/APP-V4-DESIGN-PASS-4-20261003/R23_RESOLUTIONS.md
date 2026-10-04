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

## On the tranche-2 surveys

- **R23-31 PKG-10 (S2-E).** The survey's framing correction stands: PKG-10
  is the App v4 project's own execution controls, not App product features
  (DEL-10-01…03 are DOC_UPDATE; PKG-06's row; FR-D2). The App's product
  support for these practices is PKG-06 and PKG-02.
  1. **E1-1, E2-1, E4-1 (DERIVED).** Outputs live in the existing records:
     CURRENT_EXECUTION_BASIS, the work graphs and run records, and DAG-001…004
     with their cases and currency. Each deliverable gets one thin Design
     file that maps every obligation to its record, checks it and fills
     gaps. No parallel record set is created.
  2. **E1-2 (INTEGRATION).** The "project-definition manager", "undertaking
     manager" and "dependency owner" are HELP_HUMAN in the WORKING_ITEMS
     function. O-E prepares; HELP_HUMAN writes the coordination records
     (CURRENT_EXECUTION_BASIS and the like).
  3. **E1-3 (DERIVED).** Later undertakings rely on recorded pins while the
     bytes are unchanged. A changed edition gets a deliberate re-pin record
     before reliance.
  4. **E2-2, E2-3 (DERIVED).** Practice notes follow a project-local
     convention in run records, seeded with tranche 1's recorded lessons.
  5. **E2-4, review independence (DERIVED).** V4-OPS-34 governs "identified
     candidates": its Codex-reviewer preference and Claude fallback bind
     product candidate examination (EXP §7, R23-12). For design units, the
     merge policy's independent review is met by a separate session that did
     not author the work, with its model identity reported. Pass 4's reviews
     were Claude Opus 5.5 reviewing Claude Opus 5.5 work. That is recorded
     honestly, and it is noted as an observation for the 60% discussion,
     not as a departure. EXP §7 is not generalised (SQ-E4).
  6. **E2-8 (DERIVED).** Each run's capability and check account is a short
     section of its DISPATCH or BRIEFS.
  7. **E3-1 (DERIVED).** DEL-10-03's "affected promises" are bounded to its
     nine supplier rows plus DEP-006 and OI-013, 014, 018 and 024. It
     indexes WD §9 and does not restate it (SQ-E2).
  8. **E3-2 (INTEGRATION).** Unconfirmed shared allocations (WD U-17,
     OI-014) are for the deliverable owners to confirm. The SWBPIPE half
     waits for the host joins.
  9. **E4-5 (DERIVED, as R23-28).** DEL-10-01…04 move to IN_PROGRESS when
     design starts.
  10. **SQ-E1 and SQ-E3.** An App read of a user project's DAG is not owned
      by any deliverable and is not added now. ACT-POLICY's "DEL-10-03 …
      not mapped in detail" is filled by a row when DEL-10-03 is designed,
      under R23-21.
  11. **Not changed.** The absolute home path in
      `_DAG/cases/SCC-CASE-006/Case_Contract.md` is one of the 191
      hash-bound files the redaction report left under the owner's "no
      rewrite" direction.

- **R23-32 PKG-11 and DEL-09-12 (S2-F).** No item is a question for the
  owner now. P-1…P-7 are the person's acts at their own points of need:
  - P-1 replacing v3.0.1;
  - P-2 OI-016 (App v4), the validation period and activities;
  - P-3 the owner's use and fitness judgment;
  - P-4 staged adoption and retirement;
  - P-5 public release;
  - P-6 consequential method changes;
  - P-7 OI-021.

  The design prepares each so it can be decided well. F-R1…F-R16 are ruled
  as S2-F proposed them:
  1. **F-R1:** the replacement subject is one identified candidate.
  2. **F-R2:** v3.0.1 is not rerun; the v3 reference limit is stated.
  3. **F-R3:** practitioner validation is not a replacement condition.
  4. **F-R4:** the package uses the R23-24 shape. The owner's act is
     recorded in the project's OWNER_DECISIONS form. Shared schemas are not
     changed.
  5. **F-R5:** the alternatives are own use, published replacement (also a
     release act), defer and decline.
  6. **F-R6, F-R7:** DEL-11-01 is a linked view over the existing reference,
     archive and inventory records.
  7. **F-R8:** SCC-006 is treated by SCC-CASE-007 R1 for design.
  8. **F-R9, F-R10:** a routine adoption of an instruction change is the
     receiving loop's act.
  9. **F-R11:** DEL-11-02's consumers come from DEL-10-03 (R23-31.7).
  10. **F-R12:** DEL-09-12 keeps its own observation record, not an EXP
      outcome. This also answers S-F3.
  11. **F-R13:** observations route to their owning deliverable through the
      ScopeLedger.
  12. **F-R14:** always write "OI-016 (App v4)" or "SWBPIPE OI-016".
  13. **F-R15:** missing consumer-side rows go to the next amendment after
      the reach script.
  14. **F-R16:** the App v3 and Runtime notices are recorded as "notice
      delivered; receiving decision not recorded". Their shared appendix
      names App v3's RB-SETTINGS register, which is apt for v3 and only
      loosely so for Runtime. This is recorded, not edited: the notices are
      in PR 1079.
- **R23-33 One candidate identity (S2-F S-F1). INTEGRATION.**
  1. EXP's `candidate_subject` (DEL-09-01, the examination infrastructure)
     is the canonical identity of an App candidate.
  2. SQ's `candidate` and the LHQ CIR's `app_candidate` map to it; they do
     not define it.
  3. EU-F1 exercises the mapping on real files. Any row it needs in SQ or
     LHQ is made by its owner (O-B, O-C) under R23-21, and is listed by
     O-F, not edited by O-F.

- **R23-34 PKG-07, PKG-08 and DEL-09-10 (S2-D).** No item is a question for
  the owner now. OI-026 (Domains provider allocation), starting the
  Domains-enabled increment, host-specific reserved additions (OI-021) and
  any relaxation of V4-HOST-02 are the person's acts at their own points of
  need.
  1. **H-3 (DERIVED).** One standing vocabulary, defined in DEL-07-02, with
     three facets: envelope, condition and claim tier. Only adopted +
     current + record/admitted supports reliance. DEL-07-01, DEL-08-01,
     DEL-09-10 and FV use it. It is built under SCC-CASE-005 R1, with no new
     row.
  2. **H-2 (DERIVED).** The App's first PEC question is the project-scope
     orientation within PEC's declared feeds (PEC-ORI-001/002), answered
     from the method's files. No PEC coverage of `chirality.fleet.record` is
     assumed.
  3. **H-1 (INTEGRATION).** PEC is consumed only through the person's own
     Codex MCP configuration, and the App holds no PEC client, socket or
     token. App-origin `mcpServer/tool/call` is used only after a local
     observation settles HOSTING §6.8's "not observed" point. That probe is
     O-D's, under these limits:
     - an existing scratch Codex binary (0.158.0 or VC's 0.160.0), never the
       `codex` on PATH and never `~/.codex`;
     - a scratch home under a path without the user name (R23-22.4);
     - DEL-01-01's MCP double, with no network, no sign-in, no model and no
       download.
  4. **H-4 (INTEGRATION, not as proposed).** No candidate-approval act row
     is added to ACT, RS, CE or GUIDE now. ACT §2.1 places design-candidate
     approval "in a later increment", and its subject depends on host
     specifics that wait for the joins (S-5). DEL-08-02 states the act's
     requirements in its own Design file as a PROPOSED definition. The
     shared rows are added when the Domains-enabled increment is selected.
  5. **H-5 (INTEGRATION, not as proposed).** WD §4.2.1 keeps its two tool
     classes. Under H-1, a PEC tool reaches the App as a harness capability
     (`mcpToolCall`). A Domains tool class is a question for the
     Domains-enabled increment, and DEL-08-01 notes it. S-4 is not opened.
  6. **H-6 (DERIVED).** No register rows where reach shows a cycle (S-6).
     DEL-07-02 reads fleet records as files.
  7. **H-7 (INTEGRATION).** App adoption is two facts: release-level
     adoption, recorded by the App receiving owner like the qualification
     pin (R23-22), and per-installation enablement, which is the person's own
     configuration. Neither is needed before a qualified PEC release.
  8. **H-8 (DERIVED, R23-11).** DEL-08-02's overtaken OI-001/002 wording goes
     to the next amendment. DEP-09-01-027's missing upstream row goes to the
     register owners. GUIDE M10.1/M10.2 and TBD-007…009 drop "owner-open" at
     GUIDE's next revision.
  9. **H-9 (DERIVED, R23-28).** The five deliverables move to IN_PROGRESS.
  10. **EU-D1.** Accepted as the cluster's early unit. FV's connector
      waiting cause is O-A's row (S-3), made once EU-D1 freezes the
      vocabulary; adoption is checked in O-A's returned files. DEL-08-02's
      method and act design proceeds in parallel.

- **R23-35 Binding an undertaking's basis. DERIVED. Supersedes R23-31.3.**
  1. `CURRENT_EXECUTION_BASIS.md` says: "a later undertaking or changed
     source must bind its own applicable basis before reliance". R23-31.3
     ("rely on recorded pins while the bytes are unchanged") understated
     that. The isolated reader of EB-1 (RR-EB1) found the tension.
  2. Each later undertaking writes its own short basis binding before
     reliance. It may bind by reference to the recorded pins after
     re-hashing them.
  3. This run had not done so. HELP_HUMAN has now written
     [BASIS_BINDING.md](BASIS_BINDING.md): all 9 recorded pins re-hashed and
     unchanged, plus the two methods this run selected. Tranche 1's reliance
     was on unchanged bytes, so no result changes; the gap is recorded, not
     hidden.
  4. O-E's account and DEL-10-01's later records follow R23-35.
- **R23-36 RQ-LHQ-1 (O-F, under R23-33). INTEGRATION.** The LHQ CIR gains an
  additive, optional element that maps `app_candidate` to EXP's
  `candidate_subject.app_candidate`. O-C makes it in DEL-09-07, with a new
  version label (R23-21). Until then, EU-F1 correctly reports CIR
  reconciliation as `not_established`.

- **R23-37 EU-D1's probe and departures (O-D). INTEGRATION.**
  1. **App-origin `mcpServer/tool/call` at 0.158.0, observed with the MCP
     double and no model.** The result returned to the App. The server
     received the thread id in `_meta`. No notification followed, and the
     rollout kept no trace. That settles thread items and history: "no
     entry". Whether a later turn's model input includes the call is
     inferred, not observed. It is not enough for reliance (workflow §1: no
     expansion on an unproved consequential premise).
     - PRC §7 keeps App-origin reads unused.
     - O-D may run one follow-up probe under the same limits plus a local
       model through LM Studio on loopback, as VC did: an already-present
       model, no download, no sign-in, the scratch home under /tmp, and
       LM Studio stopped afterwards.
     - If the model's input shows no trace of the call, App-origin reads
       may be used for App views. If it does, they stay unused and HOSTING
       §6.8 records why.
  2. **For DEL-01-01's owner (recorded, no edit now).** `thread/items/list`
     and `thread/read` with turns answered "not supported yet" on a thread
     with no turn. WR, RECOVERY and NPTD page with `thread/items/list`, so
     their designs must treat a thread with no turn as having no items, not
     as an error. This goes to those files' next revision.
  3. **Departures accepted (within R23-34.1).** The Domains envelope's
     "adopted" means an identified contract plus an established admission
     basis. Each facet gains an "unknown" value that is never promoted.
  4. **FV's connector waiting cause** is routed to O-A, as S-3 and R23-34.10
     set out.

- **R23-38 EB-1's early path (O-E, RR-EB1). INTEGRATION.**
  1. **Passed as an early path.** The premise under test was that the
     project's records carry its execution basis for a reader who arrives
     cold. The reader matched every critical item from the primary records
     and contradicted none. The one frozen-key miss (K7.d) was an error in
     the key: the reader reported the owner's 2026-10-04 act correctly. K3.3
     was a gap in the brief. Both are recorded in `eb1/EB1_COMPARISON.md`.
     The key stays frozen as the record of what was asked.
  2. **The account's errors were real and are repaired** (EB-v0.2). They
     come from the cause O-E names: a stale reading under a fresh hash. That
     is a practice note for DEL-10-02 — hash the bytes you actually read,
     and reread before freezing. No second cold read: the reader already
     relied on the primary records, and RV3 reviews EB-v0.2's corrections
     against them.
  3. **DEL-10-02 and DEL-10-04 may expand.**
  4. **P-E1 is withdrawn, and P-E2 is not taken.**
     `CURRENT_EXECUTION_BASIS.md` is bound by hash in 8 records and is not
     edited. EB's account is the index to each undertaking's binding.
  5. **P-E3: no retroactive bindings.** No agreed condition requires them
     (workflow §6). EB records, as an observation, that every method the
     first increment and passes 2–3 used is byte-identical then and now
     (checked by O-E with Git).

- **R23-39 Connector needs in DEL-06-01 (O-A's RF-5a). INTEGRATION.**
  DEL-06-01's reader marks an input need satisfied once its file exists
  (RF-5), so its facts would call a connector receiving record "satisfied"
  whatever its standing. That breaks CS-R2 for any reader other than FV.
  The fix is made now, not at a later revision, because the defect is in a
  shared fact that other readers consume (workflow §5). O-A adds RF-5a to
  FR-v0.1: connector needs are read by DEL-07-02's CS-R1, as FV-10 does. It
  is repaired in place, with a change note and a check in run_fleet.py.

- **R23-40 What a connector may establish (RV2 EUD1-R1, cross-owner).
  DERIVED** from V4-CON-02, V4-CON-03 and V4-HI-62. This is one disposition
  for O-D and O-A.
  1. **CS-R2 is restated.** A connector's absence or limitation never
     implies empty work, readiness, completion or permission. A relied
     record-tier claim (adopted + current + record) reports only what its
     cited record states at its pin. For example, "the work graph at S marks
     O-B1 READY" is a report of the record, not an App conclusion.
  2. **"Done"** is not a CS value. The prohibited conclusions are listed in
     CFB §3 and stated with CS-R5, and FV refers to them there.
  3. **FV.** FV's own categories derive from project files only (V4-PM-06).
     A connector need counts as satisfied only when reliance is supported
     (CS-R1, RF-5a). Satisfying a need is not readiness: an item becomes
     ready only by FV's file-based rules. FV-10's wording "never makes
     anything ready" is restated to match. Its behaviour (C1…C8) already
     does.
  4. **Routing.** O-D repairs CFB: CS-R2, the "done" pointer, a case where
     Q1 is asked at S with READY nodes and an adopted, current response, and
     EUD1-R2…R5. O-A restates FV-10's wording with RF-5a. RV2 confirms
     both, and checks adoption in the returned files.

- **R23-41 Frozen bytes are kept (RV3 process issue). INTEGRATION.**
  1. **What happened.** O-F repaired EU-F1 in place while RV3 was reviewing
     the frozen bytes. HELP_HUMAN had routed the reader's account to O-F
     without first withdrawing the unit from review. The files were
     untracked, so the frozen bytes cannot be recovered.
  2. **The rule from now on.** At each freeze HELP_HUMAN commits only that
     unit's paths, so a frozen unit is recoverable from git. A path-limited
     commit does not take in other owners' partial edits. A unit under
     review is not edited. A repair that has to start sooner withdraws the
     unit from review, and the reviewer is told.
  3. **EU-F1.** RV3's review of RP-v0.1 stands as written. RP-v0.2 is the
     unit now under review, and RV3 confirms against it.
- **R23-42 RV3's notes on EB and LHQ. INTEGRATION.**
  1. **EB2-R1.** LOOP_INIT's v4 text has a decision record:
     `APP-V4-LOOP-ENTRY-20260928.yaml` `m2_gate`. The owner asked for the
     revision, HELP_HUMAN `/root` wrote it, and it was self-merged under the
     owner-authorized PR gate. No record shows the owner reviewed the
     resulting text. EB records exactly that (EB-v0.3, with EB2-R2).
  2. **DEL-10-02 and DEL-10-04's IN_PROGRESS.** These were moved when
     PKG-10's design started with DEL-10-01's unit, not when their own design
     started. R23-31.9 read "when design starts"; the transition is
     recorded as made at the package's start. Their design is now under way
     (R23-38.3).
  3. **LHQ2-R1.** CI-5 requires the mapping to agree with the element's
     `value` where both are given. O-C makes the change.
  4. **LHQ2-R2.** DOS's pinned CIR schema goes to its owner at the
     closeout. It is not re-pinned by script, because mapped CIRs fail the
     v0.1 schema.

- **R23-43 When the replacement packet may be put to the owner (RV3
  EUF2-R1). DERIVED** from EXAMINATION §7 and DEL-11-03 AX-001.
  1. EXAMINATION §7 names the evidence presented for the replacement
     decision (V4-EXM-10/11 and V4-EXM-20 passed on the candidate). AX-001
     lets a packet "accurately report partial or adverse evidence", but it
     "cannot claim replacement qualification until both applicable
     witnesses hold".
  2. **There is one condition, and it is on the claim, not on presentation.**
     The packet may be put to the owner at any time and states plainly what
     is and is not established. It claims replacement qualification only
     when both witnesses hold. The owner's act stays separate and is the
     owner's to make on the evidence as presented. No gate on presentation
     is invented, and no permission is implied.
  3. DEL-11-03 §2 O-1, §6.3 step 5, RF-1 and P-1 are restated to this, and
     "presentation is not gated" cites AX-001's own words.

- **R23-44 Cross-owner inputs a frozen unit depends on (RV2 FV10-R2).
  INTEGRATION.**
  1. **What went wrong.** HELP_HUMAN's path-limited commit `d43665498d` took
     FV-10 and RF-5a but not the DEL-07-02 schema and O-D's example records
     they read. Those were left out because O-D was mid-repair. The unit was
     therefore not reproducible from git, and it read inputs that were live
     and unpinned.
  2. **A unit that depends on another owner's in-progress files pins
     copies.** It vendors the exact bytes it relies on into its own
     prototype fixtures, records their sha256 and source, and checks the
     hashes before use. When the supplier refreezes, the dependent owner
     re-pins deliberately (R23-21).
  3. **R23-41 is extended.** Before a path-limited commit, HELP_HUMAN checks
     that every input the unit's checks read is either inside the commit or
     already in git.

- **R23-45 EU-D1 after its reader (O-D). INTEGRATION.**
  1. **The referred item is met.** In P1 parts (a) and (c), the reader gave
     basis "both" where the key says "connector". It relied on exactly
     c1–c7 and also checked them against the files. Reliance on the
     connector is what the key tests, and checking the files as well
     takes nothing away from it. The score is 46 of 46. The key is
     unchanged.
  2. **App-origin reads (follow-up P-H1b, under R23-37.1).** DEL-01-01's
     OBS-2 provider tap, in capture-only mode on loopback, recorded exactly
     what Codex sent for the next turn. There were three message items,
     with no trace of the App-origin call and no tool-call item. This is
     direct observation of the model input, so no model was needed. App
     views may use App-origin `mcpServer/tool/call` reads.
     - Scope: Codex 0.158.0, one custom provider route, the first request of
       the next turn. It is rechecked at a version advance (R23-22).
     - The HOSTING §6.8 receiver row and the "not supported yet" note (R23-37.2)
       go to DEL-01-01 at its next revision.
  3. **OD-F1 (c9's broken anchor) was a real gap in the rules.** It was
     repaired by PR-7: a record-tier claim whose citation does not resolve
     is `unknown`. This is the same lesson as tranche 1's checker that only
     agreed with its author's accounts.

- **R23-46 Briefs recorded verbatim (RV3 UC1-R1; P-E7). DERIVED** from SPEC
  §9.8, which requires the run record to hold the launch briefs themselves,
  written by its maintainer.
  1. **This run kept summaries only.** HELP_HUMAN's DISPATCH rows
     summarised the briefs, and owners transcribed theirs. A summary loses
     fences and prohibitions.
  2. **The gap is now closed.** HELP_HUMAN has extracted every brief sent in
     this run (99) verbatim from the session transcript into
     [BRIEFS_AS_SENT.md](BRIEFS_AS_SENT.md), with home paths redacted.
     From here on, each brief is appended there at dispatch.
  3. **Owners' own records** stay as labelled transcriptions and
     cross-checks, not as the run's record of what was supplied.
  4. **UC.** UC's G-1 convention is restated to this. VER-002's second case
     is re-marked partial.
- **R23-47 Capability account wording (RV3 note).** DISPATCH's account said
  write and network limits "are instruction-only". The supportable standing
  is "not observed to be host-enforced; unknown". The host reports that its
  Bash tool runs sandboxed unless that is disabled; this was not probed. The
  line is corrected.

- **R23-48 EU-D1 confirmation notes (RV2). INTEGRATION.**
  1. **EUD1-R9: run evidence hidden by `.gitignore`.** The root `.gitignore`
     line `**/build/` excluded `D/build/` (frozen records, EXP records,
     RUN_LOG, reader input set) from every commit. HELP_HUMAN's path-limited
     commits did not notice, and R23-44's check missed ignored paths. That
     is now part of the check: before each path-limited commit, HELP_HUMAN
     runs `git status --ignored` on the unit's paths. Only `D/build/` is
     affected.
     - O-D renames it to an evidence folder that is not ignored, and
       relabels B-2 "on-disk".
     - The round-0 bytes RR-EUD1 read (input set `65700ab7…`) survive only as
       hashes. That is recorded, not reconstructed.
  2. **EUD1-R10.** The comparison checker's forbid test must not pass
     paraphrases. O-D makes K6 judge structured fields, with phrase
     matching only as a supplement, and completes P6's K5. RV2's paraphrase
     probes become cases.
  3. **EUD1-R11. R23-45.2 is narrowed to what P-H1b observed:** an
     App-origin call on a thread with no prior turn, made between turns,
     with the next turn's first request captured.
     - App views may use App-origin reads only in that situation, until a
       probe observes a thread with history and a call made during an
       active turn.
     - O-D may run that probe under the same limits. If a model is needed,
       R23-37's LM Studio terms apply.
     - The kept capture also carried the time zone and installation and
       session ids. These are redacted as HOSTING §9.1 lists.
  4. **EUD1-R12 goes to O-A.** RF-5a reads the record-level standing, so a
     claim-level `unknown` (P8) must not be hidden by a record that still
     says reliance is supported. **EUD1-R13** goes to O-D.
