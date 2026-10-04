# RV2-SQ-U3 — review of DEL-09-02 SQ-v0.1 (standalone App candidate qualification)

- **Reviewer.** RV2 (Type 2 TASK, Claude Opus 5.5), run `APP-V4-DESIGN-PASS-4-20261003`, 2026-10-03. Method: `coordinated-knowledge-work` §3.
- **Unit.** `PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-02_Standalone App candidate qualification/Design/`.
- **Hashes.** `STANDALONE_QUALIFICATION.md` is `57720387…747c`, as expected. The six other files listed in `OWNERS/O-B.md` also match (`shasum -a 256`). I reviewed the frozen bytes.
- **Basis read.**
  - DEL-09-02 ScopeOfWork (`327616c5…`, matches the pin), all of it.
  - `Dependencies.csv` rows -009, -012, -013, -014, -018, -020, -022.
  - `docs/EXAMINATION.md` V4-EXM-10, -11 and -12, and its use of "run".
  - DEL-11-03 ScopeOfWork, OUT-001 and REQ-001, and row DEP-11-03-006.
  - Every designed-case row the step map cites, read at the pinned version.
  - WR §6 SQ-J and TT-2/TT-7.
  - EXP-v0.2 §3.1, §3.2 and §6.1.
  - The NIR, AAC, RS and ACT working diffs.
  - R23-1…R23-23.

## Verdict: **REPAIR**

No BLOCKING findings. 2 MAJOR, 6 MINOR, 3 NOTE. One MAJOR (SQ-R-B) carries a cross-owner question for HELP_HUMAN.

The structure holds and should be kept:
- the three scenarios over one candidate;
- V4-EXM-11 inside RUN-A;
- the join-not-reimplement step map;
- the use of the EXP record;
- the dossier and the DEL-11-03 boundary.

The S11 insertion points are faithful (answer in SQ-R-G). What is missing is mainly the **stimuli**: conditions the ScopeOfWork's VER methods require and no step stages.

## Findings

### SQ-R-A — MAJOR — VER-002's collision condition and VER-003's unperformed-act negatives are not staged by any step (§3.1 J-5…J-9; §10 SQ-VC-02, SQ-VC-03; ScopeOfWork VER-002, VER-003)

**Evidence.**
- ScopeOfWork VER-002 asks to "Exercise a relevant revision/source-collision condition and compare before/after selection and registered content".
- VER-003 asks to "Examine a positive faithful-recording case …, then the pending/unperformed case where execution success, another act, silence or timeout cannot supply it".
- SQ J-5 only observes "no silent overwrite or rebinding on collision". It creates no collision.
- SQ-VC-02 expects "J-5 observations; no overwrite or rebinding".
- SQ-VC-03 lists the negatives, "tool success, silence, timeout supply no act", but no step in `sq.step-map.json` puts the candidate in that state.
- The cases cited at J-5 run on doubles:
  - WR-VC-03: "Library, bundle and host-listing doubles".
  - WR-VC-05: "Act-control double; on a candidate, the person" — for the positive case.

**Consequence.**
- On the candidate, "no overwrite or rebinding" would be observed with nothing that could overwrite or rebind, so the result is a vacuous pass.
- The VER-003 negatives would never be observed natively.
- AC-002 and AC-003 then rest on component doubles. The ScopeOfWork forbids that substitution: "a scripted definition or component pass cannot stand in for the joined run" (VER-001).

**Repair.**
- The run already supplies a revision condition at J-8. Add the observation that, after J-8 registers revision 2, J-7's selection and run record still name revision 1 and revision 1's bytes are unchanged (WR SL-4).
- Stage one source collision, for example a same-name entry in another origin before J-5 or J-7 (WR SP-5, SL-3). Observe the notice and that nothing rebinds.
- Stage the VER-003 negatives at J-6, J-8 or J-9:
  - the act control opened and left unconfirmed (silence / timeout);
  - the agent stating the workflow is registered;
  - tool success on the draft.
  
  In each case observe that no A15 is recorded.
- Mark these as stimuli inside RUN-A (see SQ-R-B on R23-15).

### SQ-R-B — MAJOR (cross-owner question for HELP_HUMAN) — V4-EXM-11's distinctions have no staged occasion, and the replay counterpart is optional where VER-005 says to include it (§3.2 S11-1, S11-6; §4 "Replay where possible"; ScopeOfWork SOW-196, REQ-005, VER-005)

**Evidence.**
- SOW-196 in the ScopeOfWork table covers "surviving requests/descendants and truthful unknown outcomes".
- VER-005: "Include lost or unavailable acknowledgment/outcome and surviving-descendant conditions using supported recorded seam evidence where possible; compare with the joined observation … State evidence limits if any required condition cannot be observed".
- SQ S11-6 observes "primary-turn completion vs active descendants; settlement vs received acknowledgment; unknown stays unknown". But no step of RUN-A has the agent delegate. J-2 is "substantive real tool use" only.
- The cases S11 joins assume conditions the step does not create:
  - S11-1 cites RECOVERY VC-R-02, whose setup is "A live turn with a pending request and a delegated child".
  - S11-6 cites VC-R-04, "The double raises them" (not producible natively on demand).
  - S11-6 cites NPTD NV-04, "**not observed** (OBS-2's parent waited for its child)".
- SQ §4: replays "**may** be examined additionally as EXP rehearsals".

**Consequence.** These steps are declared applicable and not optional (§6: "none of V4-EXM-10/11/12's steps is optional"). So S11-6 can only end `inconclusive`, or be marked `pass` with nothing to distinguish. The first leaves V4-EXM-11 permanently short of `pass`. The second is a vacuous pass.

**Repair.**
- Stage a delegated child in RUN-A, at S11-1 as VC-R-02 assumes, or during J-7, with the parent completing first where possible.
- Make the HOSTING §9.4 replays (X-04, X-05, X-09, X-10) a required, separately recorded rehearsal part that VER-005 compares with the native step. They are not optional.
- State, before the run, what S11-6 records when a condition does not arise natively: `inconclusive` with its limit.

**For HELP_HUMAN.**
- R23-15 settled the same pattern for DEL-09-07 only: stimuli added inside the V4-EXM-20 run, marked as added, and the scenario's own pass conditions not depending on them.
- SQ-R-A and SQ-R-B need the same treatment for RUN-A. Here, though, VER-002, VER-003 and VER-005 are this deliverable's own obligations, so whether the added stimuli condition V4-EXM-10's or V4-EXM-11's outcome is a real choice.
- Please rule whether R23-15 extends to DEL-09-02, and how the stimuli count, so that O-C's and O-B's journeys apply one rule.

### SQ-R-C — MINOR — J-6 joins the wrong act-control cases; registration at J-8 and J-9 joins none (§3.1 J-6, J-8, J-9; `sq.step-map.json`; SQ-R6)

**Evidence.**
- J-6 is "**The person registers it** at the act control (A15)". It cites "AAC VC-AAC-01, VC-AAC-04".
- At the pinned AAC-v0.2 (`git show HEAD:`), the cited rows are:
  - VC-AAC-04: "Positive capture … The person's confirmation captures **A4 at an arrival**".
  - VC-AAC-01: the offered kinds.
- The A15 cases are elsewhere:
  - VC-AAC-08 "A15 | Offered only from a current descriptor; no decline; captured, recorded, then registered";
  - VC-AAC-13 "Native confirmation … candidate | Not run", the one native A15-relevant case;
  - VC-AAC-07 (stale binding);
  - VC-AAC-03 (automation refused).
- J-8 and J-9 register too, but cite no AAC case.

**Consequence.**
- The step map joins J-6 to an A4 case. The supplier's own native check of the capture surface, VC-AAC-13, is not linked.
- SQ-R6 checks only that a cited row exists, so the prototype cannot catch this.

**Repair.**
- J-6, J-8 and J-9 → VC-AAC-08, VC-AAC-13 (and VC-AAC-07 with SQ-R-A's negatives).
- Keep VC-AAC-01 if wanted.
- Drop VC-AAC-04, or say why an A4 case bears on A15.

### SQ-R-D — MINOR — The pin-basis claim does not hold for S11-1, and U-SQ-1 does not follow R23-22 (header "Pin basis"; §0 OI-012; §12 U-SQ-1; R23-21 item 3; R23-22)

**Evidence: the pin-basis claim.**
- SQ says: "No step relies on a Codex fact that differs between 0.158.0 and 0.160.0".
- S11-1 observes "Turn ends interrupted" through NIR VC-NIR-10 ("TO-1…TO-6").
- VC found Δ3: `Turn.error` "failed or interrupted" at 0.160.0. O-A's NIR-v0.3 (`git diff HEAD`) changes TO-4 for exactly this: "An interrupted turn that carries `Turn.error` (possible at 0.160.0, Δ3) is still TO-4".
- The VC-NIR-10 row is byte-unchanged, which is what O-B checked. The rule it tests changed.

**Evidence: U-SQ-1.**
- U-SQ-1 says "HELP_HUMAN when VC returns (R23-17)".
- R23-22 item 2 now sets the qualification pin "when a candidate is built: the newest version that has passed a version-advance check", with no new decision.

**Consequence.**
- Under R23-21 item 3, the NIR change touches S11-1's reliance at any 0.160.0 or later qualification pin. R23-22 makes such a pin likely. So the NIR-v0.2 pin is not enough there.
- The U-SQ-1 owner and the point of need are stale.

**Repair.**
- Either adopt NIR-v0.3 for S11-1, saying so, or bind S11-1's reliance on NIR-v0.2 to 0.158.0 only.
- Reword the pin-basis sentence.
- Restate U-SQ-1 and §0 OI-012 per R23-22 and cite it.

### SQ-R-E — MINOR — Running each refinement makes V4-EXM-10's pass depend on runs the basis does not name. This answers O-B's question on "refines it twice" (§3.1 J-8, J-9 and the note under the table; WR TT-7)

**Evidence.**
- EXAMINATION V4-EXM-10: "reuses it on new inputs and refines it twice".
- ScopeOfWork AC-001: "new-input reuse and exactly the source-required two refinements".
- VER-001: "the new reuse inputs and each of the two refinements".
- SQ J-8: "register, run on new inputs". J-9: "register, run".
- The SQ note relies on WR TT-7 (PROPOSED): "two registered revisions, each run on new inputs".
- WR's own SQ-J has J-8 "Refine … try, review, register: revision 2", with no run, and "try" is dropped in SQ's J-8.

**Assessment.**
- Reading a refinement as a **registered revision** is sound under K-7: only registered revisions run, so a refinement that is to be used must be registered.
- Requiring each refinement to be **run** is TT-7's PROPOSED addition, not the basis's words. A failure in J-8's or J-9's run would then fail V4-EXM-10 on a condition EXAMINATION does not state. That is the kind of addition R23-6 withdrew and R23-15 fenced.

**Repair.** Either:
- label the J-8 and J-9 runs as added (they may still be recorded) and aggregate V4-EXM-10 without them; or
- cite a basis for them beyond TT-7.

Also restore WR's "try" in J-8, or say why it is omitted.

### SQ-R-F — MINOR — Dossier states and handover differ from EXP §6.1, and independence is not tied to the dossier handed over (§5; §6; SF-6; `sq.dossier.schema.json`; VER-007; CLM-004)

Scratch probes (`$TMPDIR/rv2/probe_sq.py`, importing the prototype unchanged) show four gaps.

**States.**
- Q5: the step `state` enum is `designed`, `awaiting_input`, `held`, `recorded`.
- EXP §6.1 has DESIGNED, PLANNED, AWAITING INPUT, HELD, RUN, RECORDED, REOPENED.
- SF-5 says "affected steps reopen", but there is no state for it.
- EXP §6.1 also says "Held arcs are not HELD cases", so what `held` would mean here is not stated.

**Outcome without anything planned.**
- Q4: `scenario.outcome` is required.
- SQ-EX-01 records `not-run` for three scenarios whose every step is `awaiting_input`.
- EXP §3.2 says such gap labels "are case states here, not outcomes".
- R23-20's `not-run` means "planned for the candidate and not attempted".
- §6's trigger, "once the runs are due", is not defined.

**Contradictory step accepted.** Q3: an `awaiting_input` step carrying `outcome: pass` is schema-valid with no rule fired.

**Independence and handover.**
- Q2: a dossier is accepted with no rule fired when it has:
  - every step `recorded` and `pass`;
  - every scenario `pass`;
  - `examiner.separation: not_separate`;
  - no `review_record`.
- SF-6 says such a dossier is "not reported as independently examined". But the dossier has no element that reports independence or handover, and §6's "A dossier handed to DEL-11-03 has every step `recorded`" is not checkable.
- EXP adopted `reported_as_independent` for the same reason (EXP-R-F).

**Repair.**
- Align the step states with EXP §6.1, or map them to it.
- Allow a scenario `outcome` only when its steps are planned.
- Refuse an outcome on a step that is not `recorded`.
- Add a handover element (`handed_over` / `reported_as_independent`) with rules:
  - a dossier handed over as qualification has every step recorded and a review record;
  - it has a separate examiner, or says it is not independent.

### SQ-R-G — MINOR — The S11 insertion points are faithful, but two preconditions and S11-5's state are unstated. This answers O-B's question (§3.2 S11-2…S11-6; §4)

**Answer to O-B.**
- EXAMINATION uses "run" for a scenario's execution: "the scenarios below, run against a named candidate" (§1, line 22).
- So "During the run in V4-EXM-10" means RUN-A as a whole, J-1…J-9. On that reading, S11-1 in J-2's ordinary conversation is inside it.
- The order matches the basis: stop → close/reopen → deny, grant → quit/relaunch → continue. RECOVERY VC-R-14 reads it the same way: "During V4-EXM-10's run".

**Gaps.**
1. **Approval requests depend on settings.** S11-2…S11-5 need tool-permission requests. Whether Codex asks depends on the person's own tool-permission and sandbox settings (D3). §4 records those settings "by reference" but does not state the precondition, or what is recorded if no request arises.
2. **S11-5 combines three conditions without saying how they coexist.** It reads: "During J-8, with live work and a request waiting … an interrupted registration attempt reconciled".
   - Registration is the person's act at the act control.
   - The reconciliation case cited, WR-VC-07, concerns "process loss after the store copy", which is a different moment from live agent work.
3. **The continued conversation is not named.** S11-6 says "Continue the conversation" without saying which one.

**Repair.**
- State the settings precondition and the outcome if no request arises: `blocked`, with "no request raised" as the cause.
- Split S11-5's conditions, or say how they are produced together.
- Name the conversation S11-6 continues.

### SQ-R-H — MINOR — The v3 references in §8 have no place in the dossier, and DEL-11-03's seven core-loop elements are not mapped (§8; step schema; DEL-11-03 REQ-001)

**Evidence.**
- §8 says "The dossier names, per step, the v3 journey that exercised a similar thing".
- The step schema's properties are only `missing_input`, `outcome`, `result_record`, `state`, `step` and `supplier_cases` (probe Q6). The step map carries no v3 reference.
- DEL-11-03 REQ-001, the consumer, must "account individually for planning, execution, workflow saving, reuse, approvals, interruption and restart".

**What SQ gets right.** SQ correctly leaves the comparison itself to DEL-11-03. DEP-11-03-006 reads "Consume the … dossier to produce the v3.0.1 core-loop comparison".

**Repair.** Add per-step `v3_reference` and a `core_loop_element` mapping to the step map or the schema.

### SQ-R-I — NOTE — The development-build fallback and SEAL-2 (§2 I-6; §4)

**Evidence.**
- I-6, if absent: "Steps run on a development build, labelled `native_development`".
- AAC §6.3 SEAL-2 (PROPOSED, not implemented) is "available only to the signed App".
- PKG I-4, from the same owner: "SEAL-2 unavailable on an unsigned build".

**Consequence.** If SEAL-2 is implemented, J-6, J-8 and J-9's act records on an unsigned build would read "capture not verifiable". U-SQ-3 should state this effect on AC-003 evidence.

### SQ-R-J — NOTE — Two mechanical additions

1. **SQ-R7 has no violation example.** O-B reports violations caught for SQ-R1…R6. My probe Q1 shows SQ-R7 is implemented and fires when J-1 and J-2 are swapped. Add it as `SQ-RV-07`.
2. **RECOVERY VC-R-14 is cited only at S11-6.** VC-R-14 ("Native witness (V4-EXM-11) … During V4-EXM-10's run: stop a turn, …") is DEL-01-02's own native V4-EXM-11 witness. One RUN-A serves both. Cite it at scenario level, or at every S11 step, so that DEL-01-02's case and SQ's steps are visibly the same execution.

### SQ-R-K — NOTE — What was confirmed

- **Citations.** All 51 step-map citations exist as designed-case rows: my own extraction, read at the pinned version for NIR, AAC, RS and ACT (`git show HEAD:`) and current for the others. For the O-A files, every cited row is byte-identical between `HEAD` and the working copy.
- **Pins and their R23-21 status.** RS-v0.10 and ACT-POLICY-v0.10 (`git diff HEAD`) add A16 rows only, so the A14, A15, D2 and D3 reliance is untouched.
- **EXEC.** EXEC is pinned at `69e6e79a…`, which equals `HEAD`. O-A edited its status line at 22:28 (R23-23 item 2), after the freeze. VC-E-17 and VC-E-18 are unchanged, so the pin remains valid as the version relied on.
- **Act classification.** §1's classification matches D3, WD VC-28 and ACT: A15 is a human act; A14 grant and deny are settlements.
- **DEL-11-03 boundary.** SQ-R5 and §8 keep the comparison with DEL-11-03 (REQ-006 there).
- **Route.** All N-1 is consistent with EXP §8.1 and R23-13.

## What I checked and how

**Hashes and pins.**
- I hashed all 7 frozen files.
- I checked every 64-hex value in the file by script against current files and against `HEAD` bytes of modified files:
  - 15 match current files (EXEC matched too when first checked; it now equals `HEAD` only, see SQ-R-K);
  - NIR `49e18090…`, AAC `062ce28c…`, ACT `4ef8c042…` and RS `a91882e7…` equal `HEAD`, as O-B states under R23-21;
  - EXEC: see SQ-R-K.

**Interfaces.**
- I read the full row of every cited supplier case (51) to check what it actually tests (SQ-R-B, SQ-R-C).
- For RS, ACT, NIR and AAC I used `git diff HEAD` to see what changed. The NIR TO-4 change touches S11-1 (SQ-R-D). The AAC, RS and ACT changes do not touch the cited cases.
- I read DEL-09-02's register rows. DEP-09-02-014 is "before the corresponding native packaged witness", so a development-build route is not barred.

**Basis.**
- EXAMINATION V4-EXM-10, -11 and -12.
- ScopeOfWork OUT-001/002, REQ-001…009, AC-001…008 and VER-001…008. These are mapped to §3, §5, §6, §7 and §10, with gaps in SQ-R-A, SQ-R-B and SQ-R-F.
- DEL-11-03 OUT-001 and REQ-001.

**Prototype rerun, not rebuilt.**
- `PYTHONDONTWRITEBYTECODE=1 python3 check_sq.py`: **TOTAL 72, FAIL 0**, 51 citations, as reported. No `__pycache__` was left.
- Missing assertions are added only as scratch probes, Q1–Q7 in `$TMPDIR/rv2/probe_sq.py`. Nothing was written into the unit.

**Cycles.**
- My reach script over both DAG-004 layers: DEL-09-02 reaches 20 deliverables, including DEL-01-06.
- SQ proposes no row. Its §11 items are wording carries and missing counterparts with no graph effect, so no new cycle question arises.

**60% level.** An implementer can build the dossier, the records and the sequence. What is missing:
- the stimuli and preconditions per step (SQ-R-A, SQ-R-B, SQ-R-G);
- a state model consistent with EXP (SQ-R-F);
- the v3 and core-loop mapping DEL-11-03 needs (SQ-R-H).

## Not checked

- EXP-v0.2 itself. RV confirmed it READY (`DISPATCH.md`); I checked only the elements SQ uses.
- Supplier cases' own prototypes. I did not rerun RECOVERY, NIR, AAC, WR or ACCESS prototypes.
- Whether any cited model-only case has since run on a candidate. None can have, since no candidate exists.
- The dossier example contents beyond the prototype run and my probes.

## Repair confirmation (SQ-v0.2, 2026-10-03)

### Verdict: **READY**: the repairs are confirmed

All of SQ-R-A…SQ-R-K are adopted in the returned files. I raise two new MINOR findings (SQ-R-L, SQ-R-M) and one NOTE (SQ-R-N). There is no BLOCKING or MAJOR finding.

**What I checked.**

- **Bytes.** All 7 files match O-B.md "Repairs for RV2" (`shasum -a 256`). `STANDALONE_QUALIFICATION.md` is `f18f26c5…c458`.
- **Prototype.** `PYTHONDONTWRITEBYTECODE=1 python3 check_sq.py` gives **TOTAL 108, FAIL 0** with 65 citations, as reported. No `__pycache__` was left.
- **My round-1 probes, rerun unchanged** (`$TMPDIR/rv2/probe_sq.py`):
  - Q1 fires SQ-R7, and the example set now holds it as SQ-RV-08.
  - Q2's all-pass dossier now fires SQ-R9, because its steps lack the declared stimuli. The handover and independence case is SQ-RV-09, which fires SQ-R8.
  - Q3 is schema-invalid.
  - Q4 raises KeyError, because examples no longer carry an outcome before the examination opens. That is the intended repair.
- **New probes** (`$TMPDIR/rv2/probe_sq2.py`): see SQ-R-L.
- **Citations.** I extracted all 65 cited rows myself.
  - For AAC, ACT, RS and EXEC I read each row at its pinned commit (`git show <commit>:`) and compared it with the current working file. All 65 rows exist and are unchanged.
  - The HOSTING X-09 and X-10 rows exist in §9.4.
- **Commit pins.** Each commit holds exactly the bytes cited, is the file's last change at that version, and is an ancestor of `HEAD`:
  - `31d65b0be3`: AAC `062ce28c…`
  - `dc61150559`: ACT `4ef8c042…`
  - `61e7a0afec`: RS `a91882e7…`
  - `61e7a0afec`: EXEC `69e6e79a…`
- **Other pins.**
  - NIR-v0.3 `aca40c0e…` is the current file.
  - EXP `1371ddb2…` is the current file.
  - Every other 64-hex value matches a current file, apart from the v0.1 self-reference, which equals `HEAD` `09ca67d094`.

**Per finding.**

| Finding | State | Evidence in v0.2 |
|---|---|---|
| SQ-R-A | **Confirmed** | See "SQ-R-A and SQ-R-B" below |
| SQ-R-B | **Confirmed** | See "SQ-R-A and SQ-R-B" below |
| SQ-R-C | **Confirmed** | J-6, J-8 and J-9 now join VC-AAC-08 and VC-AAC-13; J-6 also joins VC-AAC-07 and VC-AAC-03. VC-AAC-04 is gone, and the map check refuses an A4 case at a registration step |
| SQ-R-D | **Confirmed** | NIR-v0.3 is adopted. The pin-basis paragraph names S11-1's dependence on Δ3. U-SQ-1 and §0 follow R23-22 |
| SQ-R-E | **Confirmed** | J-8R and J-9R carry `counts: false` and an `added_reason`, and are never aggregated (SQ-R4, SQ-R10, SQ-EX-04). "Try" is restored in J-8 and J-9 |
| SQ-R-F | **Confirmed** | See "SQ-R-F" below |
| SQ-R-G | **Confirmed** | See "SQ-R-G" below |
| SQ-R-H | **Confirmed** | Each step carries `core_loop_element` and `v3_reference`. The map check covers DEL-11-03 REQ-001's seven core-loop elements |
| SQ-R-I | **Confirmed** | U-SQ-3 states SEAL-2's effect on AC-003 evidence |
| SQ-R-J | **Confirmed** | SQ-RV-08 exists, and VC-R-14 is cited at every S11 step (map check) |
| SQ-R-K | — | NOTE; no change was needed |

**SQ-R-A and SQ-R-B (confirmed, under R23-27).**

- §3.4 declares five stimuli in the digested pre-run case definition (`case_definition`, required by the schema):

  | Stimulus | What it stages | Where |
  |---|---|---|
  | ST-1 | Revision condition | J-8 |
  | ST-2 | Source collision, placed before J-5 | Observed at J-5 and J-7 |
  | ST-3 | Unperformed-act negatives | J-6 and J-8 |
  | ST-4 | Delegated child | Staged at J-2, stopped at S11-1, observed at S11-6 |
  | ST-5 | Lost acknowledgment, by **required** replay | S11-6 |

- The stimuli count toward their scenario (R23-27 item 2).
- **Vacuous passes.** No step can now pass without its stimulus:
  - SQ-R9 refuses a recorded counted step that omits a declared stimulus, and refuses `pass` when any stimulus is `not_produced`.
  - SF-8 makes such a step `blocked`.
  - The approval steps carry a declared settings precondition, and "no request raised" is `blocked` (SF-9).
- **ST-4 without a delegating route.** ST-4 needs a model route that carries delegation (HOSTING U-22, confirmed: "delegation tools travel in the dropped `namespace` tool"). Its replay is "none exists yet" (U-SQ-5). So S11-6 is `blocked` unless RUN-A's model can delegate, which is honest under R23-27 item 3.

**SQ-R-F (confirmed).**

- The step states are EXP §6.1's seven.
- An outcome or result record is allowed only on `recorded` steps (schema; my Q3 is now refused).
- A scenario has an outcome only once every counted step is recorded.
- `examination_opened` marks when steps become planned.
- `handed_over` and `reported_as_independent` are governed by SQ-R8.

**SQ-R-G (confirmed).**

- The settings precondition is declared before the run.
- S11-5 now combines only a live turn and a waiting request in J-8's try conversation. WR-VC-07 is not staged there, and the file says why.
- S11-6 names the conversation it continues.

### SQ-R-L — MINOR (new) — SQ-R9 accepts a replay where no replay counterpart exists, and a non-blocked outcome for a stimulus that was not produced

Probes in `$TMPDIR/rv2/probe_sq2.py`, run on valid example SQ-EX-03:

- **P-a.**
  - **Probe.** J-6 records `ST-3` as `produced: replay`, and the step passes.
  - **Result.** Schema-valid; no rule fires.
  - **Why it matters.** The step map gives ST-1, ST-2 and ST-3 no replay counterpart (`replay_counterpart: null`; §3.4 "—"), so a replay claim for them has nothing behind it. That is a pass resting on a condition that was not actually staged.
- **P-b.**
  - **Probe.** S11-6 records `ST-4` as `not_produced` (cause: the route cannot delegate) with outcome `inconclusive`, and the scenario is aggregated.
  - **Result.** Schema-valid; no rule fires.
  - **Why it matters.** R23-27 item 3 and SF-8 say the dependent part is `blocked`. Under EXP-R1 a `blocked` part makes the step `fail` or `blocked`, never `inconclusive`.

**Repair.**
- Refuse `produced: replay` when the map's `replay_counterpart` is null.
- When any stimulus is `not_produced`, require the step outcome to be `blocked` (or `fail`, if another part failed).

### SQ-R-M — MINOR (new) — ST-5's required replay does not exist yet, and its content is not shown to contain the condition

**Evidence.**
- §3.4 ST-5: "**Required:** HOSTING X-09/X-10 recordings replayed on the supplier double (RECOVERY VC-R-04)".
- HOSTING §9.4 is a "Seam regression set (designed)". Its X-09 row reads: "Child killed with one outstanding request and one un-responded client request | recorded-truncated | No (needs a live turn)".
- No such recording exists. The X-09 scenario as written (an outstanding server request plus an un-responded client request) is not the same as RECOVERY VC-R-04's "a written answer whose acknowledgment never comes", which that case produces with "The double raises them".
- ST-4's missing recording is listed as U-SQ-5. ST-5's is not listed anywhere.

**Consequence.** If X-09/X-10 is not captured before RUN-A, or does not contain a written answer whose acknowledgment never comes, S11-6 is `blocked`. That is honest under R23-27. But the dependency is not on the UNRESOLVED list, and no owner or point of need is named for it.

**Repair.**
- Add an U-SQ item for ST-5's capture: owner DEL-01-01 §9.1 capture method (with DEL-01-02), needed before RUN-A.
- Specify that the capture contains a written answer whose acknowledgment never arrives, or name VC-R-04's double fixture as the replay counterpart instead.

### SQ-R-N — NOTE — replay evidence inside a candidate record

§3.4 says a replayed condition "stands as evidence for the part that needs it … (EXP-R4 applies to parts that need native evidence; the ST-5 part is declared as not needing it)". This is consistent with R23-27 item 3 and VER-005 ("using supported recorded seam evidence where possible; compare with the joined observation"). The S11-6 record stays a `candidate` record, so EXP-R3 holds. No repair is needed. I note it because O-C's journeys may meet the same pattern.

**Not checked in this round.**
- The schema and examples beyond the prototype run and my probes.
- The supplier prototypes; none was rerun.

### Confirmation of SQ-R-L and SQ-R-M at candidate commit `d150856784` (2026-10-03)

**Verdict: READY.** SQ-R-L and SQ-R-M are adopted. Nothing is open. One NOTE (SQ-R-O) is optional.

**What I reviewed.** The committed bytes (`git show d150856784:<path>`). The working tree for `projects/chirality-app-v4` is the same as the commit.

**Hashes.**
- The five files O-B lists match at the commit, and so do the unchanged schema `16f7f232…` and invalid set `99e154f4…`.
- `STANDALONE_QUALIFICATION.md` at the commit is `3e5d0f12…8391`, not O-B's `a2ad48cf…552e`.

**The closeout changed only pin lines.**
- The closeout chain is `a2ad48cf…` →C1→ `c317a925…` →C2→ `3e5d0f12…`.
- I reversed the recorded edits in the committed file (`$TMPDIR/rv2/recon.py`):
  - the six C1 pins (RECOVERY, NPTD, WD, WR, HOSTING, EXP) and the C2 pin (ACCESS) set back to their old values;
  - the re-pin markers removed.
- The result hashes to exactly `a2ad48cf…`, so the commit adds nothing beyond those pin edits.
- Every pin names current bytes, apart from:
  - the commit pins for AAC, ACT, RS and EXEC, checked last round;
  - the v0.1 self-reference.

**Prototype.** `python3 -B check_sq.py` gives **TOTAL 114, FAIL 0**, with 65 citations. My probes `$TMPDIR/rv2/probe_sq2.py` now fire SQ-R9:
- P-a: ST-3 claimed as replayed.
- P-b: ST-4 not produced, with S11-6 left `inconclusive`.

**Per finding.**

| Finding | State | Evidence |
|---|---|---|
| SQ-R-L | **Confirmed** | SQ-R9 now refuses `produced: replay` for any stimulus whose map has no replay counterpart (ST-1…ST-3; SQ-RV-11). With a `not_produced` stimulus, SQ-R9 accepts the step only as `blocked` or `fail` (SQ-RV-12). Valid example SQ-EX-05 shows S11-6 `blocked` with ST-4 not produced |
| SQ-R-M | **Confirmed** | See below |

**SQ-R-M: the choice of capture over the double.**

What §3.4 now says:
- ST-5 and §3.4 "Why ST-5 is a capture" record the choice.
- ST-5's counterpart is a recording captured with HOSTING §9.1's method at the candidate's pin, in X-09's form. It must contain "an answer written to a server request and the process ended before any acknowledgment arrives".
- The recording is replayed with X-10's recovery read and cited as `recorded_replay` evidence beside the native observation.

The choice is sound. I checked the sources it rests on:
- HOSTING §9.6 says of the supplier double: "**Not claimed.** The double is not the supplier: every behaviour it shows beyond the recorded frames is constructed".
- RECOVERY VC-R-04 is a model-level case on that stub.
- VER-005 asks for "supported recorded seam evidence", and R23-27 item 3 has the counterpart stand in for a condition on the candidate's real supplier.

A constructed stub behaviour would only re-check the recovery rules, which VC-R-04 already does and which §3.4 keeps citing as a definition check. It would not show what the real Codex sends when an answer's acknowledgment never comes.

U-SQ-6 names the owner and the point of need, and both fit:
- **Owner.** DEL-01-01, whose §9.1 capture method and §9.4 X-09/X-10 regression set this is, together with DEL-01-02, whose RECOVERY RQ-05 row reads "a reply was written … and no acknowledgment was observed" and records `acknowledgment_not_observed`.
- **Point of need.** "Before RUN-A". Without the capture, S11-6 is `blocked` (SF-8). That is consistent with R23-27 and honest: §9.1 captures "on an identified candidate", so the capture can only follow the candidate's build, and the ST-5 part waits for it without passing vacuously.

### SQ-R-O — NOTE (optional) — producing the ST-5 capture depends on timing

The condition depends on ending the Codex process after the App writes its answer frame and before Codex's acknowledgment arrives. At 0.158.0 that acknowledgment appears as `serverRequest/resolved` (HOSTING X-14). X-09's fixture standing, "recorded-truncated", suggests a robust way to produce it: capture a full exchange and truncate it after the answer frame, recording the truncation. That way the capture does not rely on winning a race.

U-SQ-6 could say which method is used, and that a truncated recording is labelled as such and never claims byte identity (§9.1). No repair is required.
