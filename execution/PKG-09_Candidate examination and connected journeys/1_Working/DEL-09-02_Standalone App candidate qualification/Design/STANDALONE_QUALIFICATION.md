# Standalone App candidate qualification

- **Contribution:** DEL-09-02/SQ-v0.2. It supersedes SQ-v0.1 (frozen unit U3,
  file sha256 `5772038725e2dacd3939707c3fe16e064b543b9b39e4c6049fca05205a61747c`),
  repaired for review `reviews/RV2-SQ-U3.md` under R23-22 and R23-27 (see
  "Changes").
- **Status:** DRAFT DEFINITION — proposed, unsupplied, not implemented, not
  accepted. Beside it: the PROPOSED dossier schema with valid, invalid and
  rule-violation example sets, the step map `sq.step-map.json`, and a design
  prototype `prototype/check_sq.py` (not product code). No candidate exists;
  no scenario has run.
- **Run and node:** `APP-V4-DESIGN-PASS-4-20261003`, owner O-B (Type 2,
  Claude Opus 5.5), 2026-10-03. Repaired for RV2's confirmation.
- **Serves:** OUT-001, OUT-002; REQ-001…REQ-009; designed cases for
  VER-001…VER-008 (§10).
- **Basis, pinned by current bytes** (`shasum -a 256`, 2026-10-03). Several
  supplier files were revised in this run by O-A (A16, R23-18); under R23-21
  item 3 each is pinned at the version this file relies on, named with the
  commit that holds those bytes, and the cited rows were checked unchanged
  in the current working file:
  - ScopeOfWork.md `327616c5f3d816339fa48505e5c67bbd938a338e7543120d16f4ba94ac55ed8d`.
    **R23-5 re-pin:** unchanged since INIT (`ddd721a90a`); no SCA-V4-003
    block changed it, so none bears on this file. Its overtaken wording is
    followed by the current decisions (§0) and listed for the next amendment
    (R23-11).
  - `Dependencies.csv` `8da5bece8198cc1fd74394d7764b3c0f4ac019e8e359ba5e1de6a07ffbfff15a`.
  - `docs/EXAMINATION.md` `471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0`
    (§§1–3: V4-EXM-01, -03, -04, -10, -11, -12; §7); `docs/PRD.md`
    `bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd`
    (V4-APP-01/02/04, V4-WF-01…05, V4-EXE-01…04, V4-AUT-03/04,
    V4-REC-02…05, V4-CST-02/06); `docs/OPERATING_METHOD.md`
    `98836b5240ed235ec2ad38b08a9525dc9f2b366145c0736f7c70d22c1c93c5dd`
    (V4-OPS-34).
  - Suppliers' Design files (the cases the steps join; §3):
    RECOVERY-v0.2 `EXECUTION_AND_RECOVERY.md`
    `b4b6211d2be41e49f755e627283925db6424cdb290d4062b79b5c69e99378f32` (C1 re-pin, R23-21 item 4);
    NPTD-v0.2 `NATIVE_PLANS_TOOLS_DELEGATION.md`
    `64e4e26de483ce1e6742e172846e2a238f401850a416ff0744c490a4b039cfbd` (C1 re-pin, R23-21 item 4);
    **NIR-v0.3** `NATIVE_INTERACTION_RECEIVING.md`
    `aca40c0e326dae03a06fe5767c2c2e81b79600286b393bfa0dee68cc819cc6cb`
    (**adopted** under R23-21 item 3: S11-1 relies on TO-4, which v0.3
    changes for VC's Δ3 — an interrupted turn carrying `Turn.error` is still
    TO-4, Codex's message shown beside the label; the cited VC-NIR rows are
    byte-unchanged from NIR-v0.2 `49e18090…`);
    AAC-v0.2 `APP_ACT_CONTROL.md`
    `062ce28c8a4ec0bc79fc6b6c421245057a59815df14b88fa779b61eeb98be7d7`
    (AAC-v0.2 at `31d65b0be3`; the cited VC-AAC-03, -07, -08, -13 rows are
    unchanged in the current file);
    ACCESS-v0.2 `ACCOUNT_AND_PROVIDER_ACCESS.md`
    `ff7f3a2bbb18fd93923b4fe45e4e822dae7691ca606de1ea262f6c52bd862ebb` (C2 re-pin, R23-21 item 4)
    and `ACCOUNT_HOME_DECISION_RECORD.md`
    `f77f87927558ca73ab862fbe1452eaf5a0c47b6bb53b89c1419e2324ec4dad5d`;
    WD `WORKFLOW_DECLARATION.md`
    `262c9e5417cf67b56cf7c3678128ad406e8b4e2fda7057a07bebf04254ab2f31` (C1 re-pin, R23-21 item 4);
    WR-v0.2 `WORKSPACE_AND_REGISTRATION.md`
    `5ed5da8842b32b87ae68db3476192a55fc8ff151802684b10bdca16eaa8b8d8b` (C1 re-pin, R23-21 item 4);
    EXEC `EXECUTION_COMPATIBILITY.md`
    `69e6e79af078980ba16d154f05b462100576908c49901634ea8d6518990a3de7`
    (at `61e7a0afec`; VC-E-17 and VC-E-18 unchanged in the current file);
    ACT-POLICY-v0.9 `ACT_AND_POLICY_CONTRACT.md`
    `4ef8c0428d42fbe37be634d79296d7ec80860308345bf4826650fef1739b2229`
    (at `dc61150559`; cited for D2/D3 distinctions only);
    RS-v0.9 `RECORD_SEMANTICS.md`
    `a91882e74064495c5758110deae4cbc7280f3b2a12d0df8592f5238d1afd16e5`
    (at `61e7a0afec`; VC-37 and VC-40 unchanged in the current file);
    HOSTING-v0.9 `HOSTING_BOUNDARY.md`
    `5401f26d9a2a739a725771c8ce83c62ac5fa07be69b0338ee5670b9453d76d87` (C1 re-pin, R23-21 item 4).
  - Pass-4 suppliers (O-B): DEL-09-01 `EXAMINATION_PROTOCOL.md` (EXP-v0.2,
    confirmed READY by RV; U-EXP-1 closed in place) `ff0187dafd9e1f0268a19f9266914bdba64f39e0c8befdcaf20d3da7a7206a93` (C1 re-pin, R23-21 item 4);
    DEL-01-06 `PACKAGING_AND_DISTRIBUTION.md` (PKG-v0.2, repaired with this
    unit; cited by section).
  - Receiver: DEL-11-03 ScopeOfWork.md
    `0177354357b07ea177491cffc2b1c75ffac578e179ba96e63e91d6ba34dcf5b6`
    (row DEP-11-03-006).
  - Rulings, cited by ID (R23-21): R23-3, R23-5, R23-7, R23-11, R23-12,
    R23-13, R23-14, R23-15, R23-17, R23-19, R23-20, R23-21, R23-22, R23-27.
    Other run record:
    `OWNER_DECISIONS.md`
    `e4350f61a93edf0d2d4bfc588fcaa17ae23981baa6059617dcc430cda3008cd8`.
    Standing decisions: first-increment D2, D3, D4; pass-3 DECISION-K3 K-1,
    K-7; DECISION-L L-1, L-6, L-7; SCA-V4-003 DECISION-1 Q-5; the OI-009
    carry ("1 yes").
- **Pin basis (R23-3, R23-22).** Written for either pin. All three scenarios
  bind to the candidate's one pin (`candidate.codex_pin`), chosen by R23-22's
  rule when the candidate is built; a pin change is an EXP change that
  reopens every scenario. One step relies on a fact that differs between
  0.158.0 and 0.160.0: S11-1's interrupted-turn label, where VC's Δ3 lets an
  interrupted turn carry `Turn.error` at 0.160.0. S11-1 therefore relies on
  NIR-v0.3's TO-4, which covers both pins. No other step relies on a fact
  that differs; the supplier files' own pin statements apply to their
  cases.
- **Receivers:** DEL-11-03 (DEP-11-03-006, admitted).

## 0. Reading this file

**What it is.** How one identified standalone App candidate is examined
through V4-EXM-10 (create and reuse a workflow), V4-EXM-11 (interruption,
approvals and restart, inside that same run) and V4-EXM-12 (three kinds of
model access), and how the results become one dossier for DEL-11-03.

**What it is not.** It defines no feature behaviour (the suppliers' files
do), no record format of its own for results (EXP's result record is used),
no policy (D2/D3 are carried), no host witness (DEL-09-07), and no
replacement, release, retirement, practitioner validation or professional
reliance.

**Current decisions followed (R23-7), not the INIT wording.**

- **OI-009 is decided** at choice level (`Open_Issues.csv`
  RESOLVED_BY_OWNER_DECISION; DECISION-K3 K-1 with L-7): the App's Codex
  shares the person's settings, providers and MCP servers and signs in
  separately in App-owned homes. ScopeOfWork TBD-002 and DEP-09-02-027 still
  say "remains OPEN"; that wording is carried to the next amendment by the
  owner's "1 yes". This file reads OI-009 from the decision record.
- **OI-001/OI-002** are ruled for the first increment by D2/D3 (TBD-001
  reads them as open).
- **OI-012 (R23-22):** 0.158.0 stays the definition and generation pin
  (D4); 0.160.0 is checked and design-compatible; the qualification pin is
  the newest version that has passed a version-advance check when the
  candidate is built.
- **The App act control is DEL-01-04's** (SCA-V4-003 Q-5; AAC). Registration
  (J-6, J-8, J-9) is captured there.
- **K-7:** only registered revisions run; a draft is tried in an ordinary
  conversation (WR TT-2, TT-7). **L-1:** API-key conversations use a second
  App-owned home. **L-6:** no credentialed observation has been made; the
  first is this witness's own run (R23-14).

## 1. Owner and act boundary (REQ-008, REQ-009; CLM-001…CLM-004)

| Act | Actor | Here |
|---|---|---|
| Feature behaviour and focused checks | DEL-01-01…01-06, 02-01…02-03, 04-01, 04-03 (each its own) | Linked by case id (§3); never re-implemented |
| Examination support, record and review protocol | DEL-09-01 (EXP) | Used as is |
| Joined qualification and the dossier | App workflow-experience integration owner; independent candidate examiner assembles | Defined here |
| Review, registration (A15) | **The person**, at DEL-01-04's act control | Observed and cited; never performed |
| Sign-in, API-key entry | **The person** (ACCESS §0) | Observed; credentials never recorded |
| Granting or denying a tool permission (A14) | The person's answer on a request card; a routine settlement, **not a human act** (D3; WD VC-28) | Observed as a settlement, not cited as an act |
| Replacement decision | The owner (DEL-11-03 prepares) | Not claimed (SQ-R5) |

## 2. Interfaces

| ID | Input | Supplier | Arc (DAG-004) | Point of need | If absent |
|---|---|---|---|---|---|
| I-1 | Hosting/protocol, verification, recorded seams | DEL-01-01 | DEP-09-02-009, admitted | Before any step | All steps `awaiting_input` |
| I-2 | Recovery contribution and checks | DEL-01-02 | DEP-09-02-010, admitted | S11-1…S11-6 | Those steps wait |
| I-3 | Plan, tool, delegation views | DEL-01-03 | DEP-09-02-011, admitted | J-1, J-2, S11-6 | Those steps wait; plan items optional (WR J-1) |
| I-4 | Request cards, outcomes, draft view; **App act control** | DEL-01-04 | DEP-09-02-012, admitted (row names the interaction view; the act control is used too: §11) | J-2, J-3, J-6, J-8, J-9, S11-1…S11-5, M12-4 | Those steps wait |
| I-5 | Account/provider access, homes, focused checks | DEL-01-05 | DEP-09-02-013, admitted | M12-1…M12-6 | V4-EXM-12 waits |
| I-6 | Package and identity record | DEL-01-06 | DEP-09-02-014, admitted | Only if the native steps run on a package | Steps run on a development build, labelled `native_development` |
| I-7 | Workflow declaration | DEL-02-01 | DEP-09-02-015, admitted | J-5, J-7 | Those steps wait |
| I-8 | Workspace and registration | DEL-02-02 | DEP-09-02-016, admitted | J-1…J-9 | V4-EXM-10 waits |
| I-9 | Run start, per-run supply, run end | DEL-02-03 | DEP-09-02-017, admitted | J-7…J-9 | Those steps wait |
| I-10 | Adopted policy (D2/D3) | DEL-04-01 | DEP-09-02-018, admitted | J-6, S11-3/4 act classification | Settled distinctions applied from ACT as cited |
| I-11 | Act and run records | DEL-04-03 | DEP-09-02-019, admitted | J-6…J-9, S11-3/4 | Those steps wait |
| I-12 | EXP record, outcomes, routes, review | DEL-09-01 | DEP-09-02-020, admitted | Every step | No record can be written |
| I-13 | Candidate and configuration | Integration owner | DEP-09-02-022, not topological | Before the run | Dossier not opened |
| O-1 | The dossier (§5) | → DEL-11-03 | DEP-11-03-006 (admitted; DEP-09-02-021 mirror) | After the run | DEL-11-03 has no standalone evidence |

## 3. Case definitions (OUT-001; the step map)

The machine-readable map is `sq.step-map.json`: per step, the supplier
cases joined, the DEL-11-03 core-loop element, the v3 reference, the
stimuli it carries and whether it counts. `check_sq.py` confirms that every
cited supplier case is a designed-case row in that supplier's file (65
citations; SQ-R6). Case ids are file-qualified (`VC-13` in WD is not
`VC-13` in RS). The case definition, with the stimuli and preconditions
below, is declared and digested before the run (dossier `case_definition`;
R23-19, R23-27).

### 3.1 V4-EXM-10 — run RUN-A (REQ-002; WR §6 SQ-J)

| Step | What the person and agent do | Observe (EXAMINATION V4-EXM-10) | Supplier cases joined |
|---|---|---|---|
| J-1 | From an empty project folder, plan with the agent and revise the plan | Plan revisions (plan items if plan mode is on, K-5 of pass 3) | NPTD NV-01, NV-02; WR WR-VC-01 |
| J-2 | Execute with substantive real tool use in an ordinary conversation; the agent also delegates one bounded sub-task (ST-4) | Tool outcomes as Codex reports them; request cards; the delegated child | NPTD NV-03; NIR VC-NIR-01, VC-NIR-10; RECOVERY VC-R-03 |
| J-3 | Turn the work into a workflow draft | Draft listed with content identity; hygiene | WR WR-VC-02, WR-VC-08; NIR VC-NIR-14 |
| J-4 | Try the draft in a conversation (not a run, K-7) | No run record; draft not selectable for a run | WR WR-VC-09 |
| J-5 | Review the draft; the same-name entry placed in another origin (ST-2) is present | Declared inputs, tools, checkpoints, outputs, evidence; the other-origin notice (WR SP-5); nothing overwritten | WR WR-VC-03, WR-VC-05; WD VC-13 |
| J-6 | **The person registers it** at the act control (A15), after the unperformed-act negatives (ST-3) | Direct-capture record, actor ≠ recorder, bound bytes; no A15 from silence, timeout, the agent's claim or tool success | AAC VC-AAC-08, VC-AAC-13, VC-AAC-07, VC-AAC-03; NIR VC-NIR-16; RS VC-37; WR WR-VC-12, WR-VC-05 |
| J-7 | Select the registered revision (an unqualified name offers both origins, ST-2) and run it on new inputs | Source-qualified identity; no rebinding to the other origin; per-run supply | WR WR-VC-06; EXEC VC-E-18; RS VC-40 |
| J-8 | Refine (revision 2): draft from base, **try**, review, **register** (ST-3 negatives again) | Second registered revision; ST-1: J-7's selection and run record still name revision 1, whose bytes are unchanged | WR WR-VC-01, WR-VC-12, WR-VC-03; AAC VC-AAC-08, VC-AAC-13 |
| J-8R | *(added; not counted)* Run revision 2 on new inputs | Run record | EXEC VC-E-17 |
| J-9 | Refine again (revision 3): draft, try, review, register | Third registered revision; exactly two refinements | WR WR-VC-01, WR-VC-12; AAC VC-AAC-08, VC-AAC-13 |
| J-9R | *(added; not counted)* Run revision 3 | Run record | EXEC VC-E-17 |

**"Refines it twice"** is read as two **registered** revisions (K-7: only
registered revisions run, so a refinement to be used is registered). The
runs of each refinement (J-8R, J-9R) come from WR TT-7, which is PROPOSED
there and not EXAMINATION's words; they are recorded but **added and not
counted** in V4-EXM-10's outcome (RV2 SQ-R-E). WR's "try" step is kept in
J-8 and J-9.

### 3.2 V4-EXM-11 — inside RUN-A (REQ-004, REQ-005)

"During the run in V4-EXM-10" means during RUN-A as a whole (EXAMINATION
§1 uses "run" for a scenario's execution; RECOVERY VC-R-14 reads it the same
way). RECOVERY VC-R-14, DEL-01-02's own native V4-EXM-11 witness, is the
same execution and is cited at every S11 step.

**Precondition (declared before the run; D3).** The person's own
tool-permission and sandbox settings for RUN-A are ones under which Codex
asks before the tool actions J-7 uses (the setting is the person's choice,
recorded by reference). If no request arises when one is needed, the step
is `blocked` with the cause "no request raised"; it never passes.

| Step | When (inside RUN-A) | Action | Observe | Supplier cases joined |
|---|---|---|---|---|
| S11-1 | During J-2's tool-heavy turn, with the delegated child active (ST-4) | The person stops the turn | Turn ends interrupted (NIR-v0.3 TO-4, including a turn carrying `Turn.error` at 0.160.0); nothing shown done that was not observed; the child observed active is reported, not marked done | RECOVERY VC-R-02, VC-R-14; NIR VC-NIR-10 |
| S11-2 | During J-7's run, with a tool-permission request waiting | Close the window; reopen | Work continued; the request is still listed; closing an observer is not stopping work | RECOVERY VC-R-01, VC-R-14; NIR VC-NIR-05 |
| S11-3 | J-7, first request | **Deny** it on its card | Denial settled with its origin; not a human act | NIR VC-NIR-04; RECOVERY VC-R-03, VC-R-14 |
| S11-4 | J-7, a later request | **Grant** it | Grant settled; tool success is not an act | RECOVERY VC-R-03, VC-R-14; WD VC-28; NPTD NV-07 |
| S11-5 | During J-8's try conversation, while the agent's turn is live and a tool-permission request waits | Quit the App (confirming the question); relaunch | Quit question lists live work; relaunch reads *quit-with-live-work*; the waiting request rebuilt as interrupted by quit | RECOVERY VC-R-06, VC-R-14; NIR VC-NIR-11 |
| S11-6 | After relaunch | Continue **J-8's try conversation** (the one live at quit), then carry J-8 to registration | Provider vs rendered state; primary-turn completion vs the child still active (ST-4); settlement vs received acknowledgment (ST-5); unknown stays unknown | RECOVERY VC-R-04, VC-R-14; NPTD NV-04; HOSTING X-09, X-10 |

S11-5 combines only conditions the person produces together: a live turn
and a waiting request in the same conversation at quit. A registration
attempt interrupted by process loss (WR-VC-07) is not staged here; it is
WR's own fault-injection case.

V4-EXM-11's distinctions are examined at S11-6 and wherever they arise; the
dossier never reports conversation continuation as recovery of the whole
undertaking (REQ-005).

### 3.3 V4-EXM-12 — run RUN-B, same candidate (REQ-006)

| Step | Action | Observe | Supplier cases joined |
|---|---|---|---|
| M12-1 | **The person signs in** with ChatGPT in the App-owned home H-acct | Sign-in completes; account reported; no credential in App records | ACCESS VC-A01 |
| M12-2 | **The person enters an API key**; the App uses home H-key (L-1) | Key held by Codex in H-key; two homes, one process each | ACCESS VC-A02; RECOVERY VC-R-15 |
| M12-3 | Configure an identified local model server | Provider requested = reported; endpoint and model identity recorded | ACCESS VC-A03 |
| M12-4 | Open a new conversation | "No model selected" until the person chooses (DEC-4; no default) | NIR VC-NIR-12; ACCESS VC-A12 |
| M12-5 | One conversation with each mode; switch between them | Each starts; the other two stay configured and selectable | ACCESS VC-A04 |
| M12-6 | Inspect records and logs | No credential anywhere (custody scan) | ACCESS VC-A13 |

`access_modes` in the dossier names each mode's kind, home and conversation
(SQ-R3: three kinds, API key in H-key, ChatGPT in H-acct, three distinct
conversations). An unusable mode is an input gap or an observed failure,
never a substitute-mode pass (VER-006).

### 3.4 Stimuli the verification requires (R23-27)

Each is declared in the case definition before the run, carried by the
steps named, and **counts toward its scenario's outcome** (R23-27 item 2).
A condition the candidate cannot produce is supplied by its replay
counterpart, which is then **required**; if neither is possible, the
dependent step is `blocked` with that cause and never passes (R23-27 item 3;
SQ-R9).

| Id | Condition | Staged | VER | Native production | Replay counterpart |
|---|---|---|---|---|---|
| ST-1 | Revision condition: after J-8 registers revision 2, J-7's selection and run record still name revision 1, and revision 1's bytes are unchanged (WR SL-4) | J-8 | VER-002 | The run itself | — |
| ST-2 | Source collision: a same-name invented workflow placed in the user library before J-5; review lists it (WR SP-5); an unqualified name offers both (SL-3); J-7's selection does not rebind | Before J-5; observed at J-5, J-7 | VER-002 | The examiner places the entry, as declared | — |
| ST-3 | Unperformed-act negatives: (a) the act control opened and left unconfirmed past a wait; (b) the agent states the workflow is registered; (c) tool success on the draft. No A15 in any | J-6, J-8 | VER-003 | The person leaves the control open; the examiner prompts the claim; a tool uses the draft | — |
| ST-4 | A delegated child that outlives its parent turn | J-2; S11-1; observed at S11-6 | VER-005 | Needs a model route that carries Codex's delegation tools (HOSTING U-22: the local Responses route drops them), so RUN-A's model is chosen accordingly | A delegation recording where the parent completes first (NPTD NV-04); none exists yet |
| ST-5 | A lost acknowledgment: an answer written whose acknowledgment never arrives, across a process loss | S11-6 | VER-005 | Not producible on demand | **Required:** a recording captured with HOSTING §9.1's method on the candidate's pin, in X-09's form **with this condition in it** (an answer written to a server request and the process ended before any acknowledgment arrives), replayed on the supplier double with X-10's recovery read; recorded as an EXP rehearsal and cited as `recorded_replay` evidence of S11-6's part, compared with the native observation. Owner and point of need: U-SQ-6 |

A replayed condition stands as evidence for the part that needs it, not as
a native step (EXP-R4 applies to parts that need native evidence; the ST-5
part is declared as not needing it). ST-1, ST-2 and ST-3 have no replay
counterpart: they are produced natively or not at all (SQ-R9 refuses a
replay claim for them).

**Why ST-5 is a capture, not RECOVERY VC-R-04's double (RV2 SQ-R-M).**
VC-R-04 does stage exactly this condition ("a written answer whose
acknowledgment never comes"), but on RECOVERY's supplier stub, whose
behaviour beyond recorded frames is `constructed` (HOSTING §9.6 "Not
claimed"; RECOVERY §11.1 "Ran (model)"). VER-005 asks for "supported
recorded seam evidence", and R23-27's counterpart stands in for a condition
on the real supplier. So the counterpart is a recording of the real Codex at
the candidate's pin; VC-R-04's stub run stays a definition check of the
recovery rules and is cited as such. The design choice is recorded here;
the capture is U-SQ-6.

## 4. Route, configuration and evidence

- **Native route (EXP §8.1, R23-13):** every step of V4-EXM-10/11/12
  contains a person's act, a person's answer or an OS-level action, so the
  whole journey runs on route N-1 (person-operated, with the native-step
  form of EXP §8.2); every native record names the WKWebView identity.
  Steps recorded on a package use `native_packaged`; otherwise
  `native_development` (I-6).
- **Configuration per record (V4-EXM-01; EXP §4.1):** pin; Codex
  distribution identity (HOSTING §7.1); model requested and reported; model
  server kind, label and version; App-owned home; the person's
  tool-permission and sandbox settings in effect, by reference (D3; the §3.2
  precondition).
- **Material:** invented engineering material only (V4-CST-06), named in the
  candidate subject; the ST-2 entry is invented too.
- **Replay counterparts (R23-27):** ST-5's replay is required; ST-4's
  replay is required if the candidate's model route cannot delegate. Other
  recordings (HOSTING §9.4 X-04, X-05) may be examined additionally as EXP
  rehearsals; none stands for a native step (EXP-R3, EXP-R4).
- **Browser evidence** (EXP routes `interface_webkit`/`interface_chromium`)
  may support interface parts; it never satisfies a native step.

## 5. The dossier (OUT-002) — `sq.dossier.schema.json`

One dossier per candidate: the pre-run case definition (reference, sha256,
date); when the examination was opened; candidate (revision, build
identity, pin, package record if any); integration owner; examiner and
separation, with the EXP review record; the three scenarios with run
reference, steps (state per EXP §6.1, `counts`, the added reason for an
added step, EXP result record and outcome only when recorded, missing
input, stimuli with how each was produced, supplier cases, core-loop
element, v3 reference) and an outcome only once every counted step is
recorded; V4-EXM-12's access modes; the handoff to DEL-11-03 (supplies,
disclaimers, `handed_over`, `reported_as_independent`); currency; date.
Kept at `Evidence/EXP/<candidate key>/SQ-dossier.json` in DEL-09-02's
folder (EXP §8.4).

Rules (`check_sq.py`):

- **SQ-R1** All three scenarios, each once.
- **SQ-R2** V4-EXM-11 has V4-EXM-10's run reference.
- **SQ-R3** V4-EXM-12's three modes as in §3.3.
- **SQ-R4** A scenario has an outcome only when every counted step is
  recorded, and it is EXP-R1's aggregate of them; it never hides a failed or
  blocked step. Added steps (J-8R, J-9R) are never aggregated.
- **SQ-R5** The handoff disclaims joined host witness, replacement, public
  release, retirement, professional reliance and practitioner validation.
- **SQ-R6** Every cited supplier case exists in that supplier's file.
- **SQ-R7** Each scenario's steps are exactly the step map's, in order.
- **SQ-R8** Handed over as qualification only with every counted step
  recorded, every scenario's outcome and a review record; reported as
  independent only with a separate examiner and a review record.
- **SQ-R9** A recorded counted step lists every stimulus its map declares;
  a replay claim is refused for a stimulus with no replay counterpart
  (ST-1…ST-3); and a stimulus not produced (neither natively nor by replay)
  makes the step `blocked` (or `fail`, if another part failed), never
  `inconclusive` or `pass` (R23-27 item 3).
- **SQ-R10** A step's `counts` agrees with the step map.

Also checked on the step map: the seven DEL-11-03 core-loop elements are
covered; every step has a v3 reference; every stimulus declared is used;
added steps are uncounted with a reason; no A4 act-control case is joined
at a registration step; VC-R-14 is cited at every S11 step.

## 6. States and sequence

**Step states** are EXP §6.1's: `designed`, `planned`, `awaiting_input`,
`held`, `run`, `recorded`, `reopened`. `held` is only for an input held by an
unresolved owner matter, never for a held DAG arc (EXP §6.1). The
examination is **opened** when the integration owner names the candidate and
the runs are due (`examination_opened`); from then on every step is
`planned` and gets an EXP record (R23-20): `not-run` if not attempted,
`blocked` with its cause if attempted and stopped, otherwise its observed
outcome. Before that, steps may be `designed` or `awaiting_input` and carry
no outcome (schema). A changed candidate puts affected steps in `reopened`
(EXP §6.2). A step declared not applicable before the run (R23-19) would be
listed apart; none of V4-EXM-10/11/12's steps is.

**SQ-SEQ:**
1. The integration owner names the candidate and configuration (I-13); the
   examiner checks each supplier's focused evidence exists (§2), lists
   gaps, and declares the case definition with ST-1…ST-5 and the §3.2
   precondition (digested).
2. The examination is opened; all steps planned.
3. Run RUN-A: J-1…J-9R with S11-1…S11-6 at their points and the stimuli at
   theirs, the person operating, the examiner recording each step as an EXP
   record.
4. Run the required replay counterparts (ST-5; ST-4 if needed) as EXP
   rehearsals and cite them in S11-6's parts.
5. Run RUN-B: M12-1…M12-6.
6. Validate every record (EXP rules) and the dossier (SQ rules).
7. Independent review per EXP §7 (Codex reviewer; Claude fallback with an
   observed unavailability; R23-12).
8. Hand the dossier to DEL-11-03 (SQ-R8).
9. On any change (EXP §6.2) the affected steps reopen; old results stay with
   their candidate.

## 7. Failure behaviour

| ID | Condition | Behaviour |
|---|---|---|
| SF-1 | A supplier contribution is missing | Before the examination opens: the steps are `awaiting_input` with the input named. After: `not-run` with the missing input (R23-20) |
| SF-2 | A step cannot proceed mid-run | That step `blocked`; steps needing its end state `not-run`, "blocked by ‹step›" (EXP F-2); the run may continue where independent |
| SF-3 | The person declines to perform an act (e.g. registration) | The step is `not-run` ("act not performed"); no act is recorded or inferred |
| SF-4 | A credentialed mode cannot be configured | M12 step `blocked` (attempted) or `not-run`; no other mode stands in |
| SF-5 | The candidate changes during the dossier | Change-impact record; affected steps `reopened`; the dossier's `currency` follows |
| SF-6 | Reviewer not separate | Review recorded as such; `reported_as_independent: false` (SQ-R8) |
| SF-7 | Evidence partial | `inconclusive` with its limit, never `pass` |
| SF-8 | A required stimulus neither produced nor replayed | The dependent step `blocked` with that cause (R23-27; SQ-R9) |
| SF-9 | No tool-permission request arises when the step needs one | `blocked`, "no request raised" (§3.2 precondition) |

## 8. Return to DEL-11-03 (AC-008)

The dossier supplies scenario outcomes, evidence limits, input gaps,
affected rechecks, the **core-loop mapping** and **v3 comparison inputs**:
DEP-11-03-006 asks for "the v3.0.1 core-loop comparison and applicable
V4-EXM-10/11 observations", EXAMINATION §7 makes V4-EXM-10 and V4-EXM-11 the
core-loop evidence, and DEL-11-03 REQ-001 accounts individually for
planning, execution, workflow saving, reuse, approvals, interruption and
restart. Each step carries its `core_loop_element` and its `v3_reference`
(App v3 `JOURNEY_RESULTS.md`: J04 plan revisions, J02/J04 tool use, J05
workflow creation and reuse, J07 three cycles with refinement, J08 keyboard
stop and continuation, J09 deny and grant; "none recorded" where v3 has no
counterpart), in the step map and in each dossier step. The comparison
itself is DEL-11-03's act; v3 evidence qualifies nothing in v4.

## 9. What the person must do, and what is never automated

Review and registration (J-5, J-6, J-8, J-9), answers on request cards
(S11-3, S11-4), quit and relaunch confirmation (S11-5), leaving the act
control unconfirmed for ST-3, sign-in and key
entry (M12-1, M12-2). An agent may prepare, prompt and record; it does not
perform these (REQ-003; ACCESS §0; AAC NA-3).

## 10. Verification (designed; VER-001…VER-008)

| Case | Serves | Expected | Needs | Status 2026-10-03 |
|---|---|---|---|---|
| SQ-VC-01 V4-EXM-10 joined run | VER-001, AC-001 | J-1…J-9 recorded on one candidate; exactly two registered refinements; J-8R/J-9R recorded, not counted | candidate; person | Not run |
| SQ-VC-02 Revision and collision | VER-002, AC-002 | ST-1 and ST-2 produced; J-5 notice; no overwrite; J-7 not rebound; revision 1 bytes unchanged | candidate; person | Not run |
| SQ-VC-03 Acts: positive and negatives | VER-003, AC-003 | A15 direct capture with actor ≠ recorder; ST-3's silence, timeout, agent claim and tool success supply no A15; A14 settlements not cited as acts | candidate; person | Not run |
| SQ-VC-04 V4-EXM-11 inside the run | VER-004, AC-004 | S11-1…S11-6 at their points, same run reference, §3.2 precondition | candidate; person | Not run; SQ-R2 enforced (model) |
| SQ-VC-05 Recovery distinctions | VER-005, AC-005 | ST-4 natively (or its replay); ST-5 by its required replay, compared with the native observation; unknown stays unknown | candidate; recordings | Not run; SQ-R9 enforced (model) |
| SQ-VC-06 Three modes | VER-006, AC-006 | M12-1…M12-6; three modes as SQ-R3 | candidate; person; credentials (the person's) | Not run; SQ-R3 enforced (model) |
| SQ-VC-07 Dossier examined independently | VER-007, AC-007 | EXP review record; SQ-R1…R10 hold; independence only with separation and review (SQ-R8) | candidate | Rules run on examples |
| SQ-VC-08 Handoff review | VER-008, AC-008 | SQ-R5, SQ-R8; owner boundaries kept; core-loop and v3 mapping supplied | Review | Not run |

**Prototype run** (`PYTHONDONTWRITEBYTECODE=1 python3 check_sq.py` in
`prototype/`, jsonschema 4.26.0, Draft 2020-12; reads only), 2026-10-03, at
SQ-v0.2 with RV2's confirmation items: **TOTAL 114, FAIL 0** — the schema is valid; all 65 supplier case
citations of the step map are designed-case rows in their files; six
step-map checks (core-loop coverage, v3 references, stimuli declared and
used, added steps, no A4 case at registration, VC-R-14 at every S11 step);
5 valid dossiers pass and break no rule (one with an added step failing and
the scenario still passing; one with ST-4 not produced and S11-6 `blocked`);
8 invalid dossiers are rejected (incl. RV2 Q3); 12 schema-valid violations
are each caught (SQ-R1…SQ-R9, SQ-R4 and SQ-R9 three times in all; RV2 Q1,
Q2, Q4 and SQ-R-L's P-a, P-b among them).

## 11. For the next amendment (R23-11; nothing edited here)

- TBD-002 and DEP-09-02-027: OI-009 decided (carried by the owner's
  "1 yes").
- TBD-001 and DEP-09-02-024/-025: OI-001/OI-002 ruled by D2/D3 for the first
  increment.
- TBD-003 and DEP-09-02-030: D4's definition pin and R23-22's qualification
  rule.
- CLM-001 and DEP-09-02-012: name DEL-01-04's App act control as the capture
  point of registration (same admitted arc; no graph effect).
- Missing supplier-side counterparts for DEP-09-02-014 (DEL-01-06) and
  DEP-09-02-018 (DEL-04-01).
- REQ-006's wording "configured concurrently" reads with L-1 (two homes).

## 12. UNRESOLVED

| ID | Item | Owner | Point of need |
|---|---|---|---|
| U-SQ-1 | Qualification pin | **Decided by rule (R23-22):** 0.158.0 stays the definition and generation pin; 0.160.0 is checked and design-compatible; the qualification pin is the newest version that has passed a version-advance check when the candidate is built | When the candidate is built |
| U-SQ-2 | Which local model and server for M12-3, and RUN-A's model (it must carry delegation for ST-4) | Implementer, recorded as configuration (R23-17 pattern) | Before the run; a download needs the owner's yes |
| U-SQ-3 | Whether the native steps run on a package (I-6). On a development build, if DEL-01-04's SEAL-2 is implemented, J-6/J-8/J-9's act records read "capture not verifiable" (AAC §6.3: "available only to the signed App"); that limit is recorded on AC-003's evidence | Integration owner | Before the run |
| U-SQ-4 | API-key protocol detail (OI-010) | App implementation owner | Before M12-2 |
| U-SQ-5 | ST-4's replay recording (a parent completing before its child), if the chosen model route cannot delegate | DEL-01-03 / DEL-01-01 capture method | Before RUN-A |
| U-SQ-6 | ST-5's capture: a recording in X-09's form that contains an answer written to a server request and the process ended before any acknowledgment arrives, at the candidate's pin, with X-10's recovery read | DEL-01-01 (HOSTING §9.1 capture method) with DEL-01-02 (RECOVERY RQ-05, the acknowledgment-not-observed record) | Before RUN-A; without it S11-6 is `blocked` (SF-8) |
| — | Placement (decided, as EXP §8.4): the dossier is `Evidence/EXP/<candidate key>/SQ-dossier.json` in DEL-09-02's folder, beside its records | — | — |

## Changes

| Version | Change |
|---|---|
| SQ-v0.1 (2026-10-03) | First Design file: step map over the suppliers' cases, V4-EXM-11 insertion points, dossier schema and rules, DEL-11-03 return; prototype 72/0 |
| SQ-v0.2 (2026-10-03) | Repair for RV2-SQ-U3. SQ-R-A/SQ-R-B (R23-27): stimuli ST-1…ST-5 declared before the run (§3.4), counted toward their scenario; ST-5's replay required; ST-4 natively or by replay; else `blocked` (SQ-R9). SQ-R-C: J-6/J-8/J-9 join VC-AAC-08, -13 (and -07, -03 with ST-3); VC-AAC-04 dropped. SQ-R-D: NIR-v0.3 adopted for S11-1 (TO-4, Δ3); pin-basis sentence and U-SQ-1 per R23-22. SQ-R-E: J-8R/J-9R added and not counted; "try" restored. SQ-R-F: EXP §6.1 states; outcome only when recorded; `examination_opened`; handover and independence (SQ-R8). SQ-R-G: §3.2 precondition; S11-5 conditions stated; S11-6 continues J-8's try conversation. SQ-R-H: `core_loop_element` and `v3_reference` per step. SQ-R-I: U-SQ-3 states SEAL-2's effect. SQ-R-J: SQ-RV-08 for SQ-R7; VC-R-14 at every S11 step. Schema `…:0.2`, records `SQ-v0.2`. Prototype 108/0 |
| SQ-v0.2, in place (2026-10-03) | RV2 confirmation items: SQ-R-L SQ-R9 refuses a replay claim for ST-1…ST-3 and makes a not-produced stimulus `blocked` (examples SQ-RV-11, -12, SQ-EX-05); SQ-R-M ST-5's counterpart is a capture of the real Codex with the condition in it, owner and point of need U-SQ-6, reason recorded in §3.4. Prototype 114/0 |
