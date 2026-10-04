# RV-LHQ-U1 — review of DEL-09-07 LOCAL_HOST_QUALIFICATION.md (LHQ-v0.1)

- Reviewer: RV (Type 2 TASK, Claude Opus 5.5), run `APP-V4-DESIGN-PASS-4-20261003`, 2026-10-03. Method: `coordinated-knowledge-work` §3 (one question per unestablished claim; reuse valid warrants).
- Unit: `PKG-09_Candidate examination and connected journeys/1_Working/DEL-09-07_Local host candidate qualification/Design/LOCAL_HOST_QUALIFICATION.md`, sha256 `2668d95578a736b095a74b345cf625786410a43981f6e53122c5d41f19920ecc`. This matches the expected hash (`shasum -a 256`), so the reviewed bytes are the frozen bytes.
- Owner record read: `OWNERS/O-C.md` (claims 1–8, checks, open items).

## Verdict: **REPAIR**

There are 4 MAJOR findings, 8 MINOR (one of them, LHQ-R14, cross-owner) and 2 NOTE. There is no BLOCKING finding. The structure holds: the slots and binding, the CIR, the ladder, the per-step cases, the failure rows and the outcome rules can all be kept. Each MAJOR is a local repair. None of them reopens the structure.

## Findings

### LHQ-R1 — MAJOR — V4-EXM-20's verified requirements are only partly examined (claim 1; §5.1; VER-001)

- **Evidence.** `docs/EXAMINATION.md` V4-EXM-20 lists what it verifies: "*Verifies* V4-HOST-01…04, V4-PAR-01…04, V4-HI-20…25." `docs/PRD.md` V4-PAR-02 says the host's interface, embedded agent and external agent "all act through that one catalog". V4-PAR-03 says "The agent perceives the same views the person does … with the same standing marks". V4-PAR-04 says "An agent's operation passes through the same validation and the same application route as the person's, with the same outcomes and errors". `docs/HOST_INTEGRATION.md` V4-HI-20 says "Every change, by person or agent, passes through the host's one validation and application route; there is no second route for agents". The supplier contract carries this as P §2, "One route and actor parity", with its "Equivalence rule". C §10.3 T8 already fixes an "Unavailable parity" step.
- **What the file states.** No step or part of LHQ-20 names V4-PAR-01…04, V4-HI-20 or V4-HOST-03. A grep for "PAR" and "HOST-03" in the unit returns nothing, and its P citations are §4.3, §4.4, §4.5, §5 and §9, never §2. Step 20-4 has the engineer edit in the host UI, but no expected observation compares the person's route, outcomes or views with the agent's. V4-HOST-01 appears only as a precondition, and LF-3 covers it.
- **Consequence.** VER-001 checks the case plan "against … EXM V4-EXM-20…23". As written, a P20-A pass would not establish one-route and actor parity, although the scenario is meant to verify them. The CA step map does not establish parity either (CA has no V4-PAR citation), so this unit cannot rely on it.
- **Repair.** Add observations to LHQ-20 for:
  - same-route parity, for example the agent's application versus the engineer's edit at 20-4, with the same validation and outcome meanings (P §2);
  - same views and standing marks (V4-PAR-03 / V4-HI-10, at 20-2 and 20-8);
  - parity of unavailability (C T8).

  Alternatively, cite where each verified requirement is examined and mark the rest *not examined here*, with an owner.

### LHQ-R2 — MAJOR — the completeness rule lets a decline part pass on partial capture (claim 8; §5.4 completeness rule; LF-9)

- **Evidence.** R23-15 ends: "A partial capture is *inconclusive*, never *passed*." ScopeOfWork AC-006 says: "Limited or unavailable observation remains incomplete qualification." VER-006 says: "A partial capture or substitute fixture cannot pass the criterion."
- **What the file states.** §5.4: "if the capture does not cover the whole window or every host process (23-0), P23-A, P23-C and P23-D are *inconclusive*, never *passed*". P23-B is left out. P23-B is steps 23-4 and 23-5, whose evidence is "Capture (absence)". LF-9 sends a capture gap to "Completeness rule: affected parts *inconclusive*", so it inherits the omission.
- **Consequence.** "A declined request reaches no destination" is an absence claim. A capture that missed a process or an interval cannot establish it, yet P23-B could be recorded *passed* on that capture. LR-4 makes the case outcome *inconclusive* anyway, but the part result would still be citable as passed, which R23-15 forbids.
- **Repair.** Make the completeness rule cover every part whose evidence includes the capture: at least P23-A…P23-D, and P23-E as far as its observed traffic is used.

### LHQ-R3 — MAJOR — LHQ-22's checkpoint is not declared by the bound workflow (§2.1 `WF`; §5.3 preconditions, 22-3, 22-4; P22-D)

- **Evidence.** §2.1 binds `WF` → "`supports-adjust` ⟨rev-3⟩ (C §10.1; DEL-02-01 WD-EX E1)", used by "all". LHQ-22's precondition is "`WF` declaring a checkpoint whose required act is A4 on objects changed (WD-EX E1c `CP-check`)".
  - DEL-02-01 `EXAMPLES.md` §E1c identifies E1c as "{workflow, project, ⟨fx-proj⟩, `supports-label`, ⟨rev-C1⟩}: labels a support with OP-C9". Its `CP-check` is reached on "observed host outcome *applied (receipt)* of OP-C9". E1c declares no OP-C4.
  - E1's `CP-check` (EXAMPLES.md line 524) is reached on the "observed production of output `examination-report`", with subject "the objects the **applied (receipt)** outcomes of `CP-accept`'s items identify".
  - CA §2.4's graduated-autonomy branch uses E1c: "E1c `CP-check` arrives on ⟨S-4@r16⟩".
- **Consequence.** With `WF` bound as §2.1 says (E1), a direct OP-C9 application reaches no `CP-check` on the objects 22-2 changed, so step 22-4 cannot occur and P22-D cannot pass. With E1c bound instead, 22-3's `OP-GEOM` (OP-C4) is not a declared tool of the workflow. As stated, no fixture workflow satisfies the LHQ-22 preconditions together.
- **Repair.** Give LHQ-22 its own workflow slot, or a binding row (for example E1c, or E1d, with OP-C4 requested as an undeclared tool, and say how that is treated). Alternatively, add a local workflow case as was done for L-LHQ-1/2. State which arrival 22-4 expects.

### LHQ-R4 — MAJOR — LHQ-22 assumes two operation classes, but the fixture binding has one (§2.1 BR-3; 22-0, 22-1, 22-3; AC-005)

- **Evidence.**
  - DEL-04-01 ACT §8.3: "**P-03 — SWB model changes** (fixture OP-C4, OP-C5, OP-C9)".
  - C §10.2 gives OP-C9's class as "as OP-C4 (model change)".
  - C §10.3 T15 makes the grant ⟨set-2⟩ "P-03, grant value *direct*, scope {FX-W1; {S-4}}".
  - ACT FX-20: "OP-C4 on R-100 is outside scope → a direct request is *not permitted*".
  - The consequence vocabulary that could separate a "low-consequence" class is open: ACT §8.5 and U-02, "Before class assignment in DEL-03-01".
- **What the file states.** Step 22-0: "`OP-LOW` and `OP-GEOM` classes *propose*". Step 22-1: "`OP-LOW` class *direct*, scoped". BR-3 requires only that `OP-GEOM` be geometry and `OP-LOW` not be. It does not require them to be in different classes, and U-02 is not in UNRESOLVED.
- **Consequence.** On the fixture, OP-C9 is set apart from OP-C4 by grant scope, not by class. A P22-A/P22-B pass would then demonstrate scope rather than V4-EXM-22's "one class of low-consequence operation … keeps proposals for model geometry" (and V4-HI-40, "per class of operation"). If a candidate binding puts both in one class with no scope limit, 22-1's grant also admits `OP-GEOM` and 22-3 fails for a reason the case does not anticipate.
- **Repair.** In BR-3, require that the adopted policy places `OP-LOW` and `OP-GEOM` in different classes, or name scope separation as the fixture's stand-in, labelled as such. Add U-02 (with its owner and point of need) to UNRESOLVED. Reword 22-0 and 22-1 to match.

### LHQ-R5 — MINOR — the R23 pin is stale and R23-15/R23-16 are not adopted (header; F-3; §5.4)

- **Evidence.** The header pins `R23_RESOLUTIONS.md` at `793de2b2…`. The file has changed twice since: first to `eaadee6e…` (R23-15 and R23-16, "On the first frozen unit (O-C, LHQ-U1)"), and now to `e4be2c2a231e6b75449c10607c49529d23d5a2b47a950c9015a920ce1996c136` (R23-17 appended, which does not bear on DEL-09-07).
- **What the file states.** F-3 still says the stimulus reading is "PROPOSED and open to the integrator". §5.4 calls the stimuli an inference. L-LHQ-1/2 are "Returned as finding F-1/F-2".
- **Consequence.** The ruling's adoption cannot be confirmed in the file (workflow §5: adoption is checked in the returned result).
- **Repair.**
  - Re-pin R23.
  - Cite R23-15 (DERIVED) for the §5.4 stimuli, and mark them "added stimuli", as the ruling says.
  - Cite R23-16 for L-LHQ-1/2 as local additions that FX-PIPE-01 adopts at its next revision.
  - Close F-3.

### LHQ-R6 — MINOR — several CA failure rows are applied "unchanged" although their reporters are App-side (§6.1)

- **Evidence.** §6.1 applies "CAF-1, CAF-2, CAF-5…CAF-28 and CAF-31…CAF-39" unchanged. CA §2.3.1 assigns several of these rows to App-side or adapter reporters:
  - CAF-6: "HOSTING (App side, per turn)";
  - CAF-7: "HOSTING (EXEC A-3)";
  - CAF-11: "The App";
  - CAF-15: "The App (ADAPTER OM-5…OM-8)";
  - CAF-32: "The App (ADAPTER PI-2)", "not prevented on X";
  - CAF-34: "The App restarts with a submission in flight (ADAPTER PI-6)".
- **Consequence.** On CA/E the reporter is the host loop (LOOP), and CAF-6's per-turn model destination is replaced by CAF-8/R15. Applying these rows unchanged names the wrong reporter, and for CAF-32/34 it names a mechanism that does not exist on E.
- **Repair.** Exclude CAF-6, CAF-7 and CAF-34 with a reason, and restate the reporter for CAF-11, CAF-15 and CAF-32 on CA/E (the loop).

### LHQ-R7 — MINOR — the solve and lost-acknowledgement steps are out of sequence in LHQ-20 (§2.2 L-LHQ-1; 20-10…20-12; P20-A, P20-C)

- **Evidence.** C §10.3 T13: "Acknowledgment of T12 lost. Agent resubmits PR-2 …". L-LHQ-1 places the solve "after T12", and the steps run 20-10 (T12) → 20-11 (solve) → 20-12 (T13). Step 20-12 says only "an application or submission" ack is lost.
- **Consequence.** Read against the fixture, the agent would solve before it has observed the application whose acknowledgement 20-12 then loses. 20-10's "Applied with receipt(s)" and 20-12's *outcome unknown* concern the same operation, and nothing says how P20-A (20-0…20-11) is kept independent of the 20-12 stimulus.
- **Repair.** Name the operation whose acknowledgement is lost, place the solve after the recovery, and state that P20-A uses the recovered observation (or that 20-12 runs on a separate submission).

### LHQ-R8 — MINOR — LHQ-23's stimuli are not specified well enough to produce their expected observations (§5.4 23-2…23-5)

- **Evidence.**
  - 23-3 expects "Only the requesting call waited; one contact; a later request asks again". LOOP MS-16 obtains this with "while two other calls are in progress" and a later request. Neither is a stimulus in 23-3.
  - 23-2 cites MS-15, whose named entry is an MCP server, M-1. That is an outside process, so it triggers 23-7 and NW-16, while P23-E is described as *not run* "when none starts".
  - The stimuli are written as agent behaviour ("The agent asks …", "The agent's tool attempts …"). The examiner does not control that behaviour, and no failure row covers a stimulus that does not occur.
- **Consequence.** An examiner cannot reliably produce these observations. A stimulus that did not occur could be recorded as a failure.
- **Repair.**
  - Name how each stimulus is produced: the person's request, or a fixture tool with a declared destination.
  - Add the concurrent call and the second request to 23-3.
  - Say whether 23-2's entry is an MCP server.
  - Add an LF row: stimulus not produced → that step *not run*, "stimulus not produced", never *failed*.

### LHQ-R9 — MINOR — the 23-9 comparison conflicts with the stated limit for outside processes (§5.4 23-0, 23-7, 23-9)

- **Evidence.** Step 23-0 captures "every network contact by the host's process tree", which includes a child MCP server. Step 23-9 requires that "Every captured contact appears in the host's record with an allowing entry". LOOP NW-16: unless sandboxed, "the host can only decide whether to start it and record what it declares … 'process network not observed'". V4-EXM-23: such a process "is examined within that stated limit".
- **Consequence.** An unsandboxed outside process's own traffic would make 23-9, and so P23-A/P23-D, fail, contrary to the basis's stated limit.
- **Repair.** In 23-9, state how outside-process traffic is treated: it is attributed to the process and reported under 23-7, not counted against P23-A/D.

### LHQ-R10 — MINOR — LHQ-21's results standing and lapse subject are underspecified (§5.2 21-1, 21-2, 21-7)

- **Evidence.** C §10.3: T6 makes "LC-1 results become historical (no current solve at r13)", and at T8 OP-C2 is "**unavailable**, reason 'No current solve for LC-1 at this revision'". ScopeOfWork REQ-004 asks the case to preserve "current/historical standing, checks and limitations".
- **What the file states.** Step 21-1 expects "Basis B_e with content identity c_e" from `OP-RESULTS`. Step 21-2 does not require the results' standing. Step 21-7 ("Bound content changes after a recorded act") does not name the act. The A5 that 21-6 offers binds a change item. The fixture's T14 lapses T2's A4 on S-2.
- **Consequence.** On the fixture, 21-1 gets *unavailable*, not a basis. The findings' reference to results has no stated standing, and the 21-7 subject is ambiguous.
- **Repair.**
  - Expect *unavailable* or historical standing at 21-1 and 21-2 (or add a solve).
  - Require standing in 21-2.
  - Name the act and content that lapse in 21-7 (for example T2's A4 and T14).

### LHQ-R11 — MINOR — BR-4 contradicts LHQ-20's precondition (§2.1 BR-4; §5.1 preconditions)

- **Evidence.** BR-4 says that without a workflow, "LHQ-20 still runs as a conversation without a workflow run". LHQ-20's preconditions include "`WF` selected", and step 20-0 opens the run with a workflow selected.
- **Repair.** Make the precondition conditional on BR-4.

### LHQ-R14 — MINOR, cross-owner — LR-4's aggregation and LF-1's use of *blocked* differ from DEL-09-01's record rules (§6.1 LF-1; §6.2 LR-4)

This was found while reviewing O-B's EXP-v0.1 (`reviews/RV-EXP-U1.md`, EXP-R-A and EXP-R-B), and is recorded here for O-C's repair.

- **LR-4.** LR-4 excludes P22-G and P23-E from aggregation when they are *not run* because their phase or subject is absent. DEL-09-01's EXP-R1, which DEL-09-07 consumes (DEP-09-01-025), has no such exclusion. I ran the prototype's own `aggregate()` on four passing parts plus one `not-run` part, and it returns `inconclusive`. As both files stand, a conforming LHQ-22 record could never be `pass`.
- **LF-1.** LF-1 records *blocked* for a CIR element not supplied "before any case". EXP §3.1 gives `blocked` the meaning "Execution started or was attempted", and EXP §6.1 writes no record for a case awaiting input.

**Consequence and route.** The two owners' rules conflict, so this needs one ruling from HELP_HUMAN (workflow §5) before either side repairs.

### LHQ-R12 — NOTE — actor and recorder naming at 20-9

Step 20-9 says "recorder the host facility". RS §3 names the recorder for host-agent runs as the host run recording (DEP-04-03-016). The host act facility is the capturing surface (CA CA-H: "acts are captured by the host facility; the App/loop faithfully records them"). The actor-versus-recorder property holds either way, but the wording conflates capture and recording.

### LHQ-R13 — NOTE — no SWBPIPE overclaim found

- §4 leaves every HC at *answered*.
- §7 quotes the answers with their labels, and its last column is headed "relay-list candidates, prepared when host joins resume". This fits R23-14 item 3: nothing is relayed or prepared as a list.
- The "0 of 4" and "cannot pass" statements are marked as inference.

Spot checks against the data files agreed:
- SQ-01 "No person is named, and no time field": `RELAY_ANSWERS_SWBPIPE.md` line 59; `FACTS_SQ01_SQ32.md` line 94.
- SQ-05 / OI-016 OWNER DECISION: RELAY lines 134, 349.
- DEC-051 "for now": RELAY lines 254, 327.

## What was checked and how

- **Unit hash.** Recomputed: it matches the expected value.
- **Pins (mechanical; O-C's check reused).** I extracted all 20 64-hex values from the unit and matched them by `shasum -a 256` against the project's `.md` files and this run's records.
  - 19 of 20 match the file they name. These are the four basis docs; ScopeOfWork; CA, C, P, ACT, AS, RS, LOOP, PANEL, EXEC, HOSTING and GUIDE; RELAY and FACTS; S1-C.
  - The 20th, R23 at `793de2b2…`, no longer matches, because R23-15/16, and later R23-17, were appended after freeze (LHQ-R5).
  - O-C's 20/20 claim is consistent with the R23 state at freeze. The R23 file is untracked, so git cannot show its earlier bytes.
- **ScopeOfWork coverage.** I read DEL-09-07 `ScopeOfWork.md` (pinned hash confirmed) and mapped OUT-001 and the U1 parts of OUT-002, REQ-001…009, AC-001…008 and VER-001…008 to the unit.
  - OUT-002's dossier, REQ-007's dossier join, REQ-008's WebKit/Chromium/packaged evidence and AC-007 are declared as LHQ-U2 work. That deferral is stated, not hidden.
  - REQ-005 and AC-005's governance-phase hold is treated as P22-G, excluded in Phase 1. This is consistent with V4-EXM-22 as amended and with V4-HI-42.
- **Basis.** I read `docs/EXAMINATION.md` V4-EXM-20…23 and V4-EXM-31, `docs/PRD.md` V4-HOST-01…04 and V4-PAR-01…05, and `docs/HOST_INTEGRATION.md` V4-HI-10…12, 20…25, 30…33, 40…42 and 70…71, and compared each case's parts with them.
- **Interfaces, read at the pinned bytes:**
  - CA §2.2, §2.3 and §2.3.1 (CAF-1…39), §2.4 (operating sequence and graduated branch), §7.2 ladder (consumed unchanged; confirmed) and §8.4 W-R1…W-R7 (LR-1…LR-7 agree; LR-4 adds a PROPOSED exclusion of absent-phase parts, which W-R6 does not state but does not contradict);
  - C §5.1 (four elements plus method designation; the unit's 20-2 agrees), §10.2 and §10.3;
  - P §2 (for LHQ-R1);
  - ACT §7, §8.3 P-03 and §8.5 U-02, with FX-20;
  - AS §3, §3.2, §5 and §7 (display strings at 22-1, 22-6 and the CIR "host fixed treatment" match verbatim);
  - LOOP §5.1.1 NW-8…NW-16 and §5.2 MS-01…MS-27 (23-1, 23-4, 23-5 and 23-6 match their cases; LHQ-R8 and LHQ-R9 cover the rest);
  - RS §3, R11 and R15 (labels and kinds used exist, including "lost acknowledgement", `destination_declined` and record write failed / `recording_gap`);
  - WD-EX E1, E1c and E1d (for LHQ-R3);
  - EXEC RP-1 and PH-2;
  - GUIDE HC-7.3 (it names "V4-EXM-23 observation (DEL-09-07)");
  - PANEL ND-4 (it presents AS §3.2).
- **R23.**
  - R23-3: the pin basis is stated and no Codex protocol fact is relied on.
  - R23-14: privilege is asked at run time (LHQ-23 preconditions; LF-10); the A12 mapping is deferred (F-5); relay candidates only.
  - R23-15 and R23-16: adoption pending (LHQ-R5). R23-15's substance is mostly met: the stimuli do not alter LHQ-20's parts. The exception is its last sentence (LHQ-R2).

## Not checked

- The full text of S1-C Part B, beyond its hash.
- DEL-09-01's record form. It is in parallel with O-B, and the unit uses semantic labels only.
- HOSTING §9.3. The unit only names it, under R23-1.
- O-C's identifier spot-check script. I did not rerun it; I read the cited sections directly instead.
- LHQ-U2 material, which does not exist yet.
- Whether FX-PIPE-01 r-numbering stays consistent once L-LHQ-2's third item is applied (revision of T12 and T14). This is a minor fixture detail for the C owner at adoption.

## Repair confirmation (2026-10-03)

- **Repaired unit.** `LOCAL_HOST_QUALIFICATION.md` sha256 `2f648e5bb09d3727fad991fa84e6d3392d3a2a739ed3c16ad2b228cbcbfa1457`, which matches O-C's reply in `OWNERS/O-C.md`.
- **Basis.** Rulings R23-19, R23-20 and R23-21. Read from `R23_RESOLUTIONS.md`, which is now append-only and cited by ID.
- **Method.**
  - I reconstructed the frozen bytes from my first read (the reconstruction hashes to `2668d955…`, the frozen value) and diffed them against the repaired file.
  - I read every changed section. Unchanged sections were not re-reviewed.
  - Pins: I recomputed every 64-hex value in the repaired file over the project tree. 17 match their files.
  - The two that do not match are ACT `4ef8c042…` and RS `a91882e7…`. `git show cec590c5c3:…` reproduces both hashes. `git diff cec590c5c3` shows O-A's v0.10 changes to them are additive A16 rows and lists, leaving the A5/A10/A12 rows and the §6/§7/R11/R15 content this file relies on unchanged. Keeping those pins therefore conforms to R23-21 item 3.

### Verdict: **CONFIRMED — READY** (no BLOCKING or MAJOR open)

Two new items arise from the repairs: LHQ-R15 (MINOR) and LHQ-R16 (NOTE). Neither blocks.

| Finding | Status | Confirmed against |
|---|---|---|
| LHQ-R1 MAJOR | **Repaired** | §5.0 places every requirement V4-EXM-20…23 verify. P20-E covers 20-2, 20-4, 20-4a (same error identity and text, E-location-occupied, from both actors), 20-4b (C T8 unavailability parity) and 20-10, citing P §2. Its criterion row names V4-PAR-01…04, V4-HI-10, V4-HI-20 and V4-HOST-03 |
| LHQ-R2 MAJOR | **Repaired** | The §5.4 completeness rule now covers P23-A…P23-D, and P23-E as far as its traffic is used. LF-9 follows it. "A part with a failed observation is *failed* whatever the capture's completeness" is sound: an observed disallowed contact is positive evidence |
| LHQ-R3 MAJOR | **Repaired** | `WF-22` → WD-EX E1d `label-with-grant` ⟨rev-D1⟩. I checked this against EXAMPLES.md §E1d: `CP-grant` is reached before dispatch of OP-C9 with ⟨set-2⟩'s content, and E1c's `CP-check` is reached on OP-C9's *applied (receipt)*. Steps 22-1 and 22-3 now match those arrivals. Run 2 (E1) carries OP-C4. The L-2 (a) citation is LHQ-R16 |
| LHQ-R4 MAJOR | **Repaired** | BR-3 requires two classes on a candidate. Scope separation is labelled "fixture stand-in" and cannot pass P22-B. LF-16 and U-02 are in UNRESOLVED; the stated owner is close to ACT's own U-02 row ("DEL-04-01 with the host policy owner"). 22-6 cites ACT FX-20 for the stand-in |
| LHQ-R5 MINOR | **Repaired** | Rulings are cited by ID (R23-21 item 1). R23-15 is cited for the "added stimuli" and R23-16 for L-LHQ-1/2. F-1…F-3 are closed |
| LHQ-R6 MINOR | **Repaired** | §6.1 lists the unchanged, restated and not-applicable rows. CAF-6, CAF-7 and CAF-34 are excluded with reasons. CAF-11, CAF-15 and CAF-32 now name the loop as reporter. LF-14 is added. I checked the row partition: CAF-1…39 are each in exactly one list |
| LHQ-R7 MINOR | **Repaired** | 20-11 is the lost acknowledgement of 20-10's application. The solve is 20-12, after observation. P20-A excludes 20-11 and takes 20-10 directly or as recovered |
| LHQ-R8 MINOR | **Repaired** | Stimuli come from the person's request and are served by examiner-run test endpoints, with no third party. 23-3 has two concurrent calls and a later second need. 23-2's entry is "other APIs", not MCP. LF-15 records an unproduced stimulus as *not run*, never *failed* |
| LHQ-R9 MINOR | **Repaired** | 23-9 compares the host process's own contacts. Unsandboxed outside-process traffic goes under 23-7 (NW-16) |
| LHQ-R10 MINOR | **Repaired** | 21-1 expects *unavailable* (C T8) or historical results. 21-2 requires the referent's standing. 21-7 names T2's A4, lapsed by T14, with T6 as the unrelated-edit control (C T6 and T14 agree) |
| LHQ-R11 MINOR | **Repaired** | The LHQ-20 precondition allows BR-4. BR-4 states LHQ-22's needs |
| LHQ-R12 NOTE | **Adopted** | The §5 lead and 20-9 now separate capture (host act facility) from recording (host run recording, RS §3) |
| LHQ-R13 NOTE | No action needed | — |
| LHQ-R14 MINOR (R23-19, R23-20) | **Adopted**; one residue is LHQ-R15 | LR-4 follows R23-19 items 1–3: declared before the run with a reason, left out of aggregation, and an applicable part not run means no pass. P22-G and P23-E state their declarations. An undeclared outside process makes the case *inconclusive*. LR-3, LF-1, LF-2 and CI-3 use R23-20's definitions, with a record for every planned case |

### New items from the repair

- **LHQ-R15 — MINOR — two failure rows still conflict with R23-20 (§6.1 LF-10, LF-5).**
  - **LF-10.** When the person does not grant the capture privilege, LF-10 records LHQ-23 as *not run*. Under R23-20 the capture was attempted at its start (the privilege is asked for when the capture runs, R23-14) and a stated precondition stopped it, which is item 2's *blocked*, with its cause recorded.
  - **LF-5.** When the person is not available, LF-5 records the step as *not run*. When the step was reached and the act requested, this is likewise a dependency stopping an attempted step.
  - **Consequence.** The same event gets different labels in LHQ and EXP v0.2. This is a small residue of LHQ-R14's adoption.
  - **Repair.** Relabel both: *blocked* when attempted, *not run* only when never attempted.
- **LHQ-R16 — NOTE — two citations are wider than their sources.**
  - §5.0 maps V4-HI-21…25 to 20-3 and 20-5…20-10. V4-HI-22 (direct application under granted autonomy) is examined in LHQ-22 (22-2, P22-A), not in LHQ-20.
  - §5.3 cites DECISION-L L-2 (a) for chaining two workflow runs in a host loop conversation. L-2 (`APP-V4-DESIGN-PASS-3-20261001/OWNER_DECISIONS.md`) is the owner's choice for App conversations. Using it for the host's loop is an inference and should be marked as one.

## Second repair confirmation: LHQ-R15 and LHQ-R16 (2026-10-03)

**Bytes reviewed.** `LOCAL_HOST_QUALIFICATION.md` sha256 `430539276f6232f1b052346e29b6587376b8b902ab91716d7dc19cdea8166a71`, recomputed with `shasum -a 256`. It matches O-C's reply. I read only the changed rows (§5.0, §5.3 "Workflows", LF-5, LF-10, the header pin line and the changes table).

### Verdict: **CONFIRMED — READY**. LHQ-U1 has no open finding.

| Finding | Status | Confirmed against |
|---|---|---|
| LHQ-R15 MINOR | **Repaired** | LF-5 (L278): the step is *blocked* ("person not available") when it was reached and the act requested, and *not run* only when the case was never attempted; dependent parts are *not run*, "blocked by ‹step›". LF-10 (L283): LHQ-23 is *blocked* at 23-0 with its cause, "attempted at its start and a stated precondition stopped it (R23-20 item 2; R23-14 item 1)". Both now follow R23-20 |
| LHQ-R16 NOTE | **Adopted** | §5.0 lists V4-HI-21 and V4-HI-23…25 under LHQ-20, and V4-HI-22 under LHQ-22 (22-2, P22-A). §5.3 marks applying L-2 (a) to a host loop as "this file's reading, not a ruling on hosts" |

**Pins.** The header now pins EXEC, like ACT and RS, at its committed bytes (`69e6e79a…`, commit `cec590c5c3`), which equal its HEAD bytes. This is correct under R23-21 item 3, because only EXEC's L3 status line changed.

**Wording slip (no finding).** The header attributes that one-line EXEC change to "R23-18". It was made under R23-23 item 2.
