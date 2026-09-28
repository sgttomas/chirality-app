# V3-A — final bounded consistency check (policy, records, workflow, execution, loop, panel)

- Node: V3-A, run `APP-V4-FIRST-INCREMENT-20260928`. Reviewer: independent
  Type 2 (Claude Code subagent). I wrote none of the reviewed files and
  delegated nothing.
- Candidate: commit `9fc77baa3` (branch `claude/chirality-app-v4-60-percent-a41fd5`).
  The Design files were read with `git show 9fc77baa3:<path>` into a private
  scratch folder. Only read-only git was used. There was no network access.
- Scope, per BRIEFS.md "V3": DEL-04-01, DEL-04-02, DEL-04-03, DEL-02-01
  (plus EXAMPLES), DEL-02-03, DEL-05-01 and DEL-05-02. The R5 items assigned
  to me are Y-2 to Y-6. Other files (C, P, ADAPTER, GUIDE, HOSTING, CA, RELAY
  and XT) were read only where a ruling or fixture touches my scope.
- Method:
  - I read BRIEFS §V3, R5_CANDIDATES, OWNER_DECISIONS, R3 and R4 in full, and
    V2 for history.
  - I read EXEC-v0.2, WD-v0.4, WD-EX-v0.4 and ACT-v0.4 §§1–4 and §13 in full.
  - For LOOP, PANEL, AS and RS I read by section: the change tables,
    checkpoint sections, events, fixtures, findings and UNRESOLVED.
  - I read C-v0.4 §10 in full for check (b).
  - I made grep sweeps for:
    - hold-support values;
    - fixture identifiers;
    - L-WDEX labels, compared across WD-EX v0.3 (`ba0b37123`) and v0.4;
    - claim language;
    - the SETTLED labels for D5;
    - model-destination wording;
    - the A12 subject wording.
- `ls-tree` lists 17 Design paths. The brief says 16. The 17th is
  PIN_SPIKE_0.158.0.md, which is an observation record.

## Inputs (sha256)

| File | sha256 |
|---|---|
| DEL-04-01 `ACT_AND_POLICY_CONTRACT.md` (ACT-POLICY-v0.4) | d6da05ab…369b03b |
| DEL-04-02 `AUTONOMY_AND_STANDING_EXCHANGE.md` (AS-v0.4) | 774728d0…21f4dab |
| DEL-04-03 `RECORD_SEMANTICS.md` (RS-v0.4) | 56806b64…540199 |
| DEL-02-01 `WORKFLOW_DECLARATION.md` (WD-v0.4) | e492ff63…d8e88e |
| DEL-02-01 `EXAMPLES.md` (WD-EX-v0.4) | 60ce307a…128ca4 |
| DEL-02-03 `EXECUTION_COMPATIBILITY.md` (EXEC-v0.2) | 7f7848c0…317af0 |
| DEL-05-01 `LOOP_RECEIVING_CONTRACT.md` (LOOP-v0.4) | ffc30483…5934e |
| DEL-05-02 `PANEL_RECEIVING_CONTRACT.md` (PANEL-v0.4) | cb71bc4b…e84419 |
| DEL-03-01 `CATALOG_AND_READ_BASIS.md` (C-v0.4, fixture authority) | e929d39d…659a08c (full: e929d39d3ff9515702f9bfe51dfada537e1cbd165146ec0de4ccf629c659a08c) |
| R4_RESOLUTIONS.md | 50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24 |
| OWNER_DECISIONS.md | a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c |
| R5_CANDIDATES.md (untracked working file) | b47171bce9d072331799ddb33a151b2cf57dd66c2dcf5982d125ecb81b2eeb72 |
| BRIEFS.md (working copy, modified) | f0d5fcf7c345a05a6462712b5c38ab74ef3b024a1861afdad3678cc64d94bfc3 |

Full design-file hashes:

- ACT d6da05abe790a4374df7faf225439a01dc1be734491b499d90cf00533369b03b
- AS 774728d03824397a5343412b17659feaf9b0d2ef1029b79889d13a1b421f4dab
- RS 56806b64b12a946e706ff236dd1c25fe27ac00877aac13b50ee8603aaf540199
- WD e492ff635de972466c8a932355beeae848e1f3d3f60de7304e88963352d8e88e
- WD-EX 60ce307a25fe1f9aaad0826985e02aaa6ebd68d86a6d972b1d5a1e39b3128ca4
- EXEC 7f7848c0de2fdb4dc21f5adafa97f92e179bb66c9f6b04f3434d8f2342317af0
- LOOP ffc3048333f3370ba09a9ce124159b94f2c80ce69b5f593bfb82cc552f95934e
- PANEL cb71bc4bd3d8a2034cd236437670d5cd6dad10f8dfcc0d6c75b277573ce84419

Short names are those used in V2, plus EXEC for DEL-02-03. The line numbers
below refer to the files as committed at `9fc77baa3`.

## Verdict

**MERGE AS DRAFTS.**

- There are no BLOCKING residuals.
- Every file carries "DRAFT DEFINITION — proposed, unsupplied, not
  implemented, not accepted".
- No file claims implementation, qualification, host delivery or adoption, a
  performed human act, or relay delivery.
- The owner decisions are stated correctly in normative text.

There are five MAJOR residuals. All are cross-file consistency defects that
arose because the R4 sweep revised siblings concurrently:

- one hold-support vocabulary split;
- one D6 over-claim inside a fixture;
- one SP-6 violation;
- one local-label collision;
- one fixture-ordering gap. This is the Y-6 gap, and it drives the SP-6
  violation.

They should be the first items of the R5 micro-ruling sweep. MAJOR-2 is a
one-sentence repair. I recommend fixing it before merge if any edit pass
happens anyway.

Counts: **BLOCKING 0 · MAJOR 5 · MINOR 13.**

---

## 1. R4 ruling-by-ruling table (my scope)

| Ruling | Verdict | Evidence (file §, line) | Residual |
|---|---|---|---|
| R4-1 D5: record and show the destination, no gate | holds, with Y-3 open | RS R5 (l.138: "recorded per run and per change during the run"); RS D16, E12, VC-22; AS S15 (l.66), §2, F19, VC-13; EXEC CR-14 (l.202), TR-4, RT-5; ACT change row (no ACT change). No file gates on destination | Granularity (per run / per change / per turn) differs from HOSTING §8.3 → **Y-3**. The SETTLED label covers the recorder's additions → m-11 |
| R4-2 D6: hold support; no unenforceable App hold claimed; action during hold; HP-1/HP-2 not adopted; HP-3 best effort | **partial** | HP-1/HP-2 not adopted and HP-3 best effort appear in every file: EXEC §2; WD S-T, I-9, §4.3.8; ACT §4.6; LOOP HS-3; PANEL §3.2; AS §1; RS §1. *Action during hold* is carried in RS R11, LOOP §2.3, EXEC HD-4 and PANEL PC-21h. **But** the hold-support **values** split into two vocabularies, and the E1-over-X assignments contradict each other (MAJOR-1). RS E10 claims "held after observation" in an **App run** (MAJOR-2) | MAJOR-1, MAJOR-2 |
| R4-3 resume point HD-5; re-hold; A5/A12 never re-hold; interim display withdrawn | holds | EXEC HD-5, RH-1…RH-9; WD I-4; ACT §4.3; RS L-12; AS §4; LOOP C-4, FX-C3; PANEL W-5e, PC-20; WD-EX R-4. The withdrawn display is gone everywhere except the "withdrawn" notes | Punctuation of the display string differs (m-9) |
| R4-4 no resumption; "after run end"; continues ⟨run⟩; interruption ≠ run end | holds | EXEC §4.9 RE-1…RE-5; WD §4.3.4; ACT §2.3; RS §3 run finality, R1; AS §4, F16; LOOP §2.4.1, FX-C7b/C15; PANEL W-5b, PC-21d/g; WD-EX R-12b. "unless DEL-02-03 defines resumption" survives only in the historical v0.3 change rows | — |
| R4-5 capture after arrival (SP-6), PROPOSED; U-E4 open; repair LOOP FX-C4 and WD-EX R-16 | **partial** | SP-6 appears in EXEC §4.5, WD I-8, ACT §4.5, RS L-13, AS §4, LOOP C-2 and PANEL W-5c. FX-C4 is repaired onto T16a, and WD-EX R-16 (i) is repaired (T15 is a prior act). **EXEC CH-12** (l.821) still counts T15's A12 at a CP-grant arrival that, on C's order, occurs at T16. CH-13 and CH-14 depend on it | MAJOR-3 (see Y-6) |
| R4-6 A12 supersedes only when established; refused/pending/unconfirmed | holds | EXEC §4.10 AR-1…AR-4; ACT §2.5; RS L-0; AS §3, §4, F12b, F14; WD SB-4; LOOP C-8, FX-C11; PANEL W-5g, §3.6, PC-21f | — |
| R4-7 MX-3, MX-6, MX-8; R2-18/R3-3 confirmed | holds | EXEC §4.11; WD §4.3.7; ACT §4.3; LOOP C-7; PANEL W-5f; AS §4; WD-EX R-6b/R-7b/R-13b | WD's MX-8 row sits outside its table (m-10) |
| R4-8 *unsupported* reason "checkpoint hold not enforceable on this surface" | holds (meaning) | WD §4.2.4, FB-18; EXEC CR-8, §3.6; ACT §4.6; LOOP HS-4; PANEL §3.2 | The wording varies (m-4) |
| R4-9 grant-setting subject without A8 = declared content; none named → invalid | **partial** | WD §4.3.1 (l.291), FB-17; EXEC §4.10, §4.14, CH-29; LOOP §2.4.2 (l.447); PANEL W-5a; WD-EX E1d. **ACT §4.2** (l.430–432) makes invalidity conditional: "invalid if no A8 names a setting at arrival **and** its declaration names no setting content" | m-5; precedence is **Y-2** |
| R4-10 R3-1 class in RS R8 and AS §4 | holds | RS R8 (six classes); AS §4 (six classes) | — |
| R4-11 RS elements | holds | RS R1 (continues), R2 (transfer links, revision verification), R5 (destination), R8 (ordinals, annotations incl. re-held/replaced/A12 control/prior act), R11 (action during hold), R14 (report reference), §4.1 index | — |
| R4-12 elicitation and user input are not act evidence | holds | EXEC CAP-6; WD I-5, VC-42; ACT §2.6, §4.5, FX-49; RS HA-1, OF-2, E3(g); AS F10; WD-EX R-9 (iv) | — |
| R4-13 A13 locus; App-side configuration never A13 evidence | holds | ACT §2.6, FX-47; EXEC CAP-1; RS HA-1; WD §4.2.4 | — |
| R4-14 carriage assurance; model-supplied alone insufficient | holds (text) | ACT §4.4; WD §4.2.2, I-7; RS §5; AS §2; LOOP C-6; EXEC §3.6 GC-3 | ACT §4.4 and WD-EX R-5b still present *App-assured* as available (m-6; supports **Y-8**). The host-loop value name is LOOP G-1 (**Y-1**, V3-B) |
| R4-15 author identity *unverified* | holds | RS §5, R11; AS §7; EXEC TR-4 | — |
| R4-16 reporter of *channel not enabled* | holds | WD §4.2.4; ACT FX-24; RS §5 table; WD-EX E7 | — |
| R4-17 FX-25 wording | holds | ACT FX-25 | — |
| R4-18 T15 re-point | holds | ACT FX-20; AS F2; RS E7; PANEL PC-22; WD-EX R-5a/b (V-CP1), R-5c (T15/⟨set-2⟩). Labels-only local scopes are removed | — |
| R4-19 V2 minors | holds | ⟨set-2⟩, S-5, §10.7 (ACT FX-15), OF-n (RS), NW-n (LOOP), EXAMPLES OP-C10 per R3-4, RS A1/A2 aligned, LOOP six-class count, T16a used, V2 markers closed, R3/R4 cited | Citations now lag C-v0.4's FA→FXA rename (m-3) |
| R4-20 C additions; WD E1 OP-C12 | **partial** in my scope | WD-EX E1 adopts optional OP-C12 (holds). C-v0.4 §10.1 now has **LIB-A1**, **LIB-A2** and **AF-1**. EXEC (l.25, l.783, F-20, U-E21) and WD-EX (fixture table, UNRESOLVED last row) still say C lacks them and keep local labels | m-1 |
| R4-21 harness-capability kind (a) not holdable in App runs | holds | WD §4.3.1, FB-18, VC-38; EXEC §3.6, MT-15; ACT §4.6, FX-48; LOOP §2.4.4; AS F18; WD-EX E8 | — |
| R4 C1 carries | holds | EXEC F-10/F-11/F-12/F-14 carried; WD "not repaired here" row; ACT F-8/F-10 to C1 | — |

## 2. Checks (a)–(f)

**(a) Vocabulary.**

- Consistent across all eight files:
  - act names A1–A14;
  - the five class values with their reason;
  - the six dispositions;
  - the events: act-declined, act-lapsed, run-ended, run-resumed, action
    during hold, act superseded;
  - the carriage values: App-assured, host-held, model-supplied, absent.
- A10 is never "declined". "accept" appears only with A5. "approve" appears
  only with A6.
- Inconsistent: the **hold-support value set** (MAJOR-1), the *unsupported*
  reason wording (m-4), and the re-held display punctuation (m-9).

**(b) Fixture IDs.** Every OP-C, T, V-, S-, PR-, RC-, B, LC and ⟨set-n⟩
identifier cited by the eight files exists in C-v0.4 §10.

- FA-n citations resolve through C's stated alias FA-n → FXA-n (m-3).
- Local cases use L-‹file›-n with reasons. The exceptions are:
  - ACT's local CP-1, CP-3 and CP-4 (m-13);
  - EXEC's citations of **WD-EX's** local labels, which now point at
    different cases (MAJOR-4).

**(c) Claims.** None found.

- A sweep for implementation, qualification, delivery, adoption and relay
  claim language found only negations and "prepared for relay; not
  delivery" (LOOP §13, PANEL §8).
- Every "Engineer A" act is labeled fixture material.

**(d) D5 and D6.**

- D6: the normative text is faithful in all eight files. One fixture, RS
  E10 and its case VC-17, over-claims an App hold (MAJOR-2).
- D5: never used as a gate. Files label the "records and shows the
  destination" element SETTLED. OWNER_DECISIONS attributes that element to
  the recorder's reading, as a truthfulness addition (m-11).

**(e) Citations.** All eight files cite concurrently revised siblings at
their pre-sweep versions:

- C-v0.3, ACT-v0.3, EXEC-v0.1, ADAPTER-v0.1 and WD-EX-v0.3 at `f05c7e4cd`;
- WD §8 marks many elements "pending its v0.4".

That is Y-7's mechanical pass (V3-B). Two cases are **not** mechanical,
because the old citation now resolves to different content: MAJOR-4
(L-WDEX renumbering) and m-1/m-2 (C now declares things the texts say it
lacks).

**(f) R5 items Y-2…Y-6** are in §4.

---

## 3. Residuals

### MAJOR

**MAJOR-1 — Two hold-support vocabularies with conflicting assignments.**
Side to change: **EXEC** first, then WD, WD-EX, ACT, AS, RS, LOOP and
PANEL. ADAPTER and CA are also affected (V3-B scope).

- EXEC-v0.2 §3.6 (l.249–263, the owner file) re-valued hold support to:
  - *enforced by the host loop*;
  - *host-enforced for host operations* (App runs on X, HP-H evidenced);
  - *not enforceable*;
  - *not established*, which includes "(ii) HP-H awaiting SQ-02" and
    "(iii) A5 with model-supplied or absent carriage".
- WD §4.3.8 (l.510–516), WD-EX E8 (l.346–361), ACT §4.6 (l.569–573),
  AS §4 (l.151–155), RS R8 (l.142), LOOP §2.4.4 (l.594–600) and PANEL §3.2
  (l.167) all use the **EXEC-v0.1** set:
  - enforced before dispatch;
  - held after observation;
  - enforced on the host route;
  - not enforceable;
  - not established.
- The split changes results, not just names:
  - WD-EX E8 (l.355) gives E1 ⟨rev-A2⟩ via X, `CP-accept` as "**enforced on
    the host route** (…AWAITING INPUT)" and leaves the workflow result
    blank. EXEC MT-2 (l.791) gives the same fixture's `CP-accept` as "**not
    enforceable**". By EXEC §3.6 (ii)/(iii) it should instead be *not
    established*.
  - WD-EX E8 gives E1d via X, `CP-grant` (kind (a) on OP-C9) as "not
    enforceable". EXEC GC-5 (l.270) says "Kind (a) over X is *not
    established* until the host holds the call".
  - WD §4.3.8 and U-30 exempt "A5 on the host route" from *not
    enforceable* in App runs, with effect "None; AWAITING INPUT shown"
    (i.e. passes). EXEC makes the same case *not established* (does not
    pass).
  - EXEC itself is ambiguous. §3.6 says an App run is "*not enforceable* …
    whenever HP-H does not cover it", but row (ii) says "HP-H awaiting
    SQ-02" is *not established*.
- Fix:
  - EXEC publishes one value set, with a deterministic assignment per
    surface, kind and assurance.
  - Each pending-SQ-02 case maps to exactly one value.
  - The consumers re-point.
- Suggested set:
  - keep *enforced before dispatch* and *held after observation* for **host
    loops**, because LOOP needs the residual-limit distinction;
  - add *host-enforced for host operations* for App runs where HP-H is
    evidenced;
  - use *not enforceable* for no enforcing point;
  - use *not established* for an invalid declaration, awaiting SQ-02, or an
    A5 constraint that is model-supplied or absent;
  - retire *enforced on the host route*.
- EXEC F-17 (every checkpointed App workflow is *unsupported*) should be
  shown to the owner with the chosen set.

**MAJOR-2 — RS E10 and VC-17 claim an App hold that D6 leaves unresolved.**
Side to change: **RS**.

- RS E10 (l.454–466) sets "hold support in the **App run**: **held after
  observation**".
- Steps (ii) and (iv) then have the run "stop" at its next action and
  re-hold.
- In an App run, kinds (b)/(c) hold only through HP-2, which is not
  adopted. EXEC §3.6 values them *not enforceable*, and EXEC CH-22 is the
  matching case.
- This contradicts R4-2 ("never claims an App hold it cannot enforce") and
  RS's own §1 closing sentence and U-25.
- Fix, either:
  - make E10 a host-loop run on E, where *held after observation* is right;
    or
  - keep it in the App and state *not enforceable*: the workflow is
    unsupported; the arrival still records dispositions (EXEC HD-4); and
    step (ii) records action during hold with no claimed stop.
- Adjust VC-17 to match.

**MAJOR-3 — EXEC CH-12/CH-13/CH-14 violate SP-6 against C's order.** Side
to change: **EXEC**. Resolution vehicle: Y-6.

- CH-12 (l.821) uses "E1d with T15 … (L-EXEC-13: timing variant of T15)"
  and expects *performed* with "held OP-C9 call dispatched unchanged".
- A kind (a) arrival is the hold of the OP-C9 call. On C's order that hold
  happens at T16, after T15. By EXEC SP-6 (l.390), T15's A12 is a prior
  act and not counted.
- WD-EX R-16 (i) (l.257) reads the same order that way: waiting, "prior act
  … not counted".
- CH-13 (l.822) builds on CH-12. CH-14 (l.823) cites "L-WDEX-9 order", but
  in WD-EX-v0.4 L-WDEX-9 is the R-12b continuation (see MAJOR-4).
- Fix: re-point CH-12…CH-14 to the shared arrival-before-T15 variant
  proposed under Y-6, or add an explicit local arrival step.

**MAJOR-4 — EXEC cites WD-EX local labels that WD-EX-v0.4 renumbered.**
Side to change: **EXEC**. Optionally, WD-EX should also stop reusing
retired numbers.

- EXEC cites WD-EX-v0.3 L-WDEX-1…15 (header l.10). WD-EX-v0.4 renumbered
  its local cases, so six EXEC citations now point at different cases:

  | EXEC case | Cites | v0.3 meaning (intended) | v0.4 meaning (current) |
  |---|---|---|---|
  | MT-3 | L-WDEX-10 | OP-C4 absent | R-15 App tool permission |
  | MT-4 | L-WDEX-11 | OP-C5 absent | R-16 A12 variants. The v0.4 set has no "OP-C5 absent" case (L-WDEX-13b is OP-C12 absent) |
  | MT-13 | L-WDEX-14 | Workflow requiring OP-C11 | E8 App run via X |
  | MT-14 | L-WDEX-13 | External access off | OP-C4 absent |
  | CH-14 | L-WDEX-9 | R-16 order | R-12b continuation |
  | CH-18 | L-WDEX-7 | Stale after acceptance | R-9b E1b prior act |

- This is exactly the silent label collision R2-21 forbids. Re-point to:
  - WD-EX-v0.4 L-WDEX-13 (OP-C4 absent);
  - C V-NP1 / WD-EX E7 V-NP1 row (OP-C11);
  - WD-EX E7 "External access off" row;
  - C V-S1 / WD-EX R-14 (stale after acceptance);
  - WD-EX R-16 (ii)/(iii) (L-WDEX-11);
  - an EXEC-local L-EXEC-n for OP-C5 absent.

**MAJOR-5 — No shared A12-at-checkpoint fixture, so each file built its own
(Y-6).** Side to change: **C**, then the consumers.

- The positive case "A12 captured after a grant-setting arrival" exists
  six ways:
  - ACT CP-3 (l.1076, "held before T15", no L-label);
  - LOOP `L-LOOP-C11`;
  - PANEL `L-PANEL-2`;
  - WD-EX `L-WDEX-11`;
  - AS `L-AS-7`/`L-AS-8`;
  - EXEC CH-12, with no arrival step at all (MAJOR-3).
- The six do not agree on whether T15 itself is the counted act. It is in
  ACT, LOOP and PANEL, and it is not in WD-EX (i).
- Fix: see Y-6.

### MINOR

| # | Where | Residual | Side |
|---|---|---|---|
| m-1 | EXEC l.25, l.783, CH-23, RT-6, F-20, U-E21; WD-EX fixture table (⟨fx-proj⟩ row), UNRESOLVED last row | C-v0.4 §10.1 now has LIB-A1 ⟨fx-proj⟩, LIB-A2 ⟨fx-app-import⟩ and AF-1 (⟨AF-1@f1/f2⟩). The texts still say C lacks them. Re-point L-EXEC-19 → AF-1, ⟨fx-app-import⟩ → LIB-A2, ⟨fx-proj⟩ → LIB-A1. Close F-20/U-E21 | EXEC, WD-EX |
| m-2 | WD-EX framing (l.20, l.78–80); ACT §13 CP-1/CP-3 reason "C declares only CP-accept (FA-5)"; RS E10 "L-RS-5: C declares only V-CP1"; AS F6 "L-AS-4 (C declares only V-CP1)" | C-v0.4 FXA-5 now states that ⟨rev-3⟩ declares both `CP-accept` and `CP-check` (WD-EX E1). The local cases remain justified, but their stated reasons are stale | WD-EX, ACT, RS, AS |
| m-3 | All eight files | Cite C's fixture assumptions as FA-n. C-v0.4 renamed them FXA-n, with an alias. Also, WD-EX's table glosses FA-5 as "V-CP1 declares CP-accept", which no longer matches FXA-5 | All (Y-7 pass) |
| m-4 | AS §4 l.154 and F18: "checkpoint ‹name› cannot be held on this surface" (EXEC-v0.1 wording). PANEL §3.2: "checkpoint ‹name› hold not enforceable on this surface". WD: "…on this surface: ‹name›" | Align to one R4-8 string | AS, PANEL |
| m-5 | ACT §4.2 l.430–432 | A12 invalidity is made conditional on no A8 at arrival. WD FB-17, EXEC §4.14/CH-29 and LOOP §2.4.2 make it unconditional, and invalidity is a declaration-time fact reported before the run (EXEC §4.14). Make it unconditional (see Y-2) | ACT |
| m-6 | ACT §4.4 l.514 ("Only App-assured or host-held carriage satisfies R2-12"); WD-EX R-5b ("host-held or App-assured") | App-assured needs HP-1, which is not adopted. EXEC §3.6 counts only host-held. State "App-assured: not available in this increment (D6)" (**Y-8**) | ACT, WD-EX (and P per Y-8) |
| m-7 | ACT FX-50 (l.1138) | Says "the required-tool outcome for OP-C4 on X is not established … HELD on … ADAPTER U-X3". EXEC §3.6 resolved U-X3, and the value affected is `CP-accept`'s **hold support** (*not established*), not OP-C4's required-tool outcome | ACT |
| m-8 | PANEL §3.2 l.167 | Holding library still "PROPOSED until W7". EXEC §6.2 has confirmed it | PANEL |
| m-9 | EXEC §4.3, §4.6; RS R8, L-12 | "re-held — lapsed at ‹t› after resume" vs R4-3's and the other files' "waiting — re-held, lapsed at ‹t› after resume" | EXEC, RS |
| m-10 | WD §4.3.7 l.490–491; WD §11 l.804–806; EXEC §7.2 l.837–838 | The MX-8 row is separated from its table by a blank line, so it renders headerless. The FB rows are ordered 17, 18, 16. CH-29 precedes CH-28 | WD, EXEC |
| m-11 | EXEC change row R4-1; LOOP §1 item 5; AS S15; RS D16; ACT header ("D5 is settled (the model destination is recorded…)") | D5's owner text is "user flexibility". Recording and showing the destination is the recorder's reading ("for truthfulness, not as a gate") as ruled in R4-1. Label that element "R4-1 (recorder's reading of D5)" or INTEGRATION, not SETTLED. R4-1 itself uses "SETTLED by DECISION-2", so an R5 micro-ruling is the right place | HELP_HUMAN (R5), then files |
| m-12 | All eight files (headers; WD §8 supplier states; LOOP and PANEL UNRESOLVED "R4-n elements not yet in sibling text"; EXEC §9.1 "v0.4 under R4 concurrent (not read)") | Sibling citations are at pre-sweep versions, and several "pending sibling v0.4" markers can now be closed | All (**Y-7**) |
| m-13 | ACT §13 | Local fixture additions CP-1, CP-3, CP-4 and FX-Professional-P are not named L-ACT-n. CP-3's arrival-before-T15 is a local ordering with no local label | ACT (or moot under Y-6) |

---

## 4. R5 items (Y-2 … Y-6)

**Y-2 — A8-named setting vs declared setting content. Position: AGREE, with
amendment.**

Today every file gives the A8 precedence:

- WD §4.3.6 (l.447), "The setting named by an A8 at arrival …, otherwise
  the declared content";
- ACT §4.2 (l.419);
- LOOP §2.4.2 (l.447);
- PANEL W-5a;
- EXEC §4.10.

Under that rule an agent-authored request would choose what satisfies a
reserved-act checkpoint. That conflicts with purpose binding (V4-REC-05)
and with the rule that the declaration, not the agent, states what the
checkpoint asks for. Proposed ruling text:

> The **declared** setting content (classes, grant values, scope) is the
> subject of an A12 checkpoint and must always be named. A declaration
> naming none is invalid (unconditionally; FB-17). An A8 at the arrival may
> *present* that content to the person but never changes the subject. An A8
> naming different content is a separate request; an A12 performed on it
> satisfies nothing at this checkpoint (SB-2, "act on other content") but
> remains an ordinary A12 whose control relation governs the grant. Where a
> workflow needs a run-dependent scope, the declaration states it as a
> binding rule bound at arrival from observed referents (e.g. "object set =
> the targets of the held call", bound from the relied-on read as for that
> subject class), never by an A8.

- Files to change: WD §4.3.1 grant-setting row and §4.3.6 table; ACT §4.2
  table row and invalidity bullet (m-5); LOOP §2.4.2; PANEL W-5a; EXEC
  §4.10 "Subject" paragraph and AR-2.
- R4-9's first sentence is superseded.
- The binding-rule clause is my addition. Without it, a portable workflow
  could only name a concrete object set such as {S-4}, which a real
  workflow author cannot know in advance. That need is presumably why A8
  precedence was written.

**Y-3 — Model destination per run vs per turn. Position: AGREE, with
amendment.**

- HOSTING §8.3 supplies, per thread and turn, the requested provider/model,
  the supplier-reported effective one, and any `model/rerouted` event.
- RS R5 today says "per run and per change during the run". AS S15 and
  EXEC U-E22 say "per run".
- Proposed text:

> R5 records the destination **per turn** as HOSTING §8.3 supplies it
> (requested and supplier-reported effective kept separate; each re-route
> recorded with its turn), with *unknown* for any turn not observed. The
> run-level value is the **set** of destinations observed, never a single
> inferred value. A model switch or re-route between or within turns is
> neither a new run nor an event affecting any disposition. EXEC CR-14 shows
> the destination selected at report time only.

- Files: RS R5 and E12; AS S15; EXEC CR-14, F-21, U-E22 (close), RT-5.
  ADAPTER channel status and XT F-12 are V3-B's.

**Y-4 — A person's own host-side undo after resume re-holds. Position:
AGREE, with amendment.**

- ACT FX-39, AS F6/VC-10, LOOP C-4 and PANEL PC-20 already apply it.
- EXEC RH-8 names only "the run's own later action". EXEC should
  generalize RH-8:

> A lapse re-holds whatever caused it: a person's edit, a person's undo
> (OP-C10, R2-15), or the run's own later action. A person's undo is the
> person's operation (an R7 entry), not a run action, so it is never
> recorded as *action during hold*. A5/A10 on the reversed item do not lapse
> (R2-15), so an undo never re-holds an A5 arrival (RH-9); only acts bound to
> content the undo changes (e.g. T16a's A4 at T17) re-hold.

**Y-5 — A person's A1/A2 are run-record operations, not human-act records.
Position: AGREE (confirm), with one precision.**

- Consistent in ACT §2.4 (l.260–264) and RS §3/§6.1 (l.106, l.236).
- No downstream file expects a person-A1/A2 act record. I checked:
  - PANEL §5 (A1/A2 actors are agent or host; undo "Actor per its
    treatment");
  - AS §7;
  - LOOP §2.3 (decision events are A5/A10/A11 only);
  - EXEC CAP-1…CAP-9;
  - WD I-5.
- Precision to add in ACT §2.4 and RS §3:

> except where the operation **performs** a reserved act (P-02: e.g. OP-C6,
> OP-C7, OP-C8, the A12/A13 controls), whose result is the human-act record
> of that act; the R7 entry, if any, references it.

**Y-6 — Grant-setting checkpoint arrival before T15. Position: AMEND.**

- Recommend that **C add one named variant**, not a main-timeline step.
  Consumers then drop their local labels.
- A T14b step on the main timeline is the wrong vehicle:
  - Run 12 is ⟨rev-3⟩, which FXA-5 now says declares only `CP-accept` and
    `CP-check`. An arrival step would make run 12 hold at a checkpoint its
    workflow does not declare.
  - It would also turn WD-EX R-16 (i)'s correct negative reading of the
    main order ("prior act, not counted") into a contradiction.
- Proposed variant, e.g. **V-GR1** "grant checkpoint arrives before T15":
  - Branches from T14 (r15).
  - In a run of WD-EX E1d (`label-with-grant`, `CP-grant` A12, kind (a)
    before dispatch of OP-C9, declared content {P-03, *direct*, {FX-W1;
    {S-4}}}), the agent's OP-C9 call on S-4 is held, so `CP-grant`
    arrives.
  - T15's A12 is captured after the arrival. The control establishes it,
    so the arrival is *performed*.
  - The held call is dispatched unchanged (= T16, RC-2).
  - Sub-variants: pending; refused; confirmation lost; a later established
    A12 (supersession).
- Re-point:
  - ACT CP-3, FX-41, FX-46;
  - LOOP FX-C11 (drop `L-LOOP-C11`);
  - PANEL PC-21f (drop `L-PANEL-2`);
  - WD-EX R-16 (ii)–(v) (drop `L-WDEX-11`), keeping (i) as the main-order
    negative;
  - AS F14/F15;
  - EXEC CH-12…CH-14 (fixes MAJOR-3).
- Observation for the owner under U-E4/U-31, not a residual. In the
  main-order reading, SP-6 makes the person repeat an A12 whose content is
  already in force (⟨set-2⟩). That is a concrete cost of SP-6 for A12
  checkpoints and is worth showing when U-E4 is decided.

**Evidence for V3-B's items.**

- Y-7: MAJOR-4 and m-1/m-2 show the pass is not purely mechanical, because
  some old citations now resolve to different content.
- Y-8: m-6 (ACT §4.4, WD-EX R-5b).
- Y-1: LOOP G-1 is the source. My files raise no objection to the proposed
  treatment.

---

## 5. Prioritized R5 list (my scope)

1. MAJOR-1: EXEC publishes a single hold-support value set and assignment.
   WD, WD-EX, ACT, AS, RS, LOOP and PANEL re-point. Include EXEC F-17 in
   what the owner sees.
2. MAJOR-2: fix RS E10/VC-17. This is a one-sentence fix; do it before
   merge if convenient.
3. Y-6 ruling (C variant), then MAJOR-3 and MAJOR-5: re-point EXEC
   CH-12…14 and the local A12 cases.
4. MAJOR-4: re-point EXEC's L-WDEX citations.
5. Y-2 ruling, then m-5.
6. Y-3, Y-4 and Y-5 micro-rulings as amended.
7. Minors m-1…m-13, alongside the Y-7 mechanical pass.

The set is fit to merge as v0.4/v0.2 **drafts** now. None of the residuals
changes an owner ruling or creates a claim. They must be cleared before the
next comparison or before any dependent fixture is designed from these
texts.
