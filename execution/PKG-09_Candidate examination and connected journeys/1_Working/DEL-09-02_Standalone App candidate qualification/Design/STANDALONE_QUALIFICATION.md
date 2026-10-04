# Standalone App candidate qualification

- **Contribution:** DEL-09-02/SQ-v0.1 (first Design file of this deliverable).
- **Status:** DRAFT DEFINITION — proposed, unsupplied, not implemented, not
  accepted. Beside it: the PROPOSED dossier schema with valid, invalid and
  rule-violation example sets, the step map `sq.step-map.json`, and a design
  prototype `prototype/check_sq.py` (not product code). No candidate exists;
  no scenario has run.
- **Run and node:** `APP-V4-DESIGN-PASS-4-20261003`, owner O-B (Type 2,
  Claude Opus 5.5), 2026-10-03. Frozen for review by RV2.
- **Serves:** OUT-001, OUT-002; REQ-001…REQ-009; designed cases for
  VER-001…VER-008 (§10).
- **Basis, pinned by current bytes** (`shasum -a 256`, 2026-10-03). Several
  supplier files are being revised in this run by O-A (A16, R23-18); under
  R23-21 item 3 each is pinned at the version this file relies on, its
  committed (`HEAD`) bytes, and the cases cited were checked unchanged in the
  new version with `git diff`:
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
    `d84c7e26f4342d261f385877ddea78a9c935c5f561b5b91602d93d9db49fe2cb`;
    NPTD-v0.2 `NATIVE_PLANS_TOOLS_DELEGATION.md`
    `6eed39dcee4acf4b8b986cdd9e09c460a8fa53571973cb5c826acce37d644a72`;
    NIR-v0.2 `NATIVE_INTERACTION_RECEIVING.md`
    `49e180907d39db3d5e6c7fedfaadf9d964aba57b328d84cca1f58fb1aec38ca0`
    (`HEAD`; NIR-v0.3 leaves the cited VC-NIR rows unchanged);
    AAC-v0.2 `APP_ACT_CONTROL.md`
    `062ce28c8a4ec0bc79fc6b6c421245057a59815df14b88fa779b61eeb98be7d7` (AAC-v0.2, the version relied on, R23-21; VC-AAC-01/-04 unchanged in AAC-v0.3);
    ACCESS-v0.2 `ACCOUNT_AND_PROVIDER_ACCESS.md`
    `7a2ad8e4a7423943ef6b1ffdbce6048d7c30c9dcc98b515e94cd623f6c041965`
    and `ACCOUNT_HOME_DECISION_RECORD.md`
    `f77f87927558ca73ab862fbe1452eaf5a0c47b6bb53b89c1419e2324ec4dad5d`;
    WD `WORKFLOW_DECLARATION.md`
    `d752810933510d0f814b87005222dc85658b08828221190f2571383bb6e07da4`;
    WR-v0.2 `WORKSPACE_AND_REGISTRATION.md`
    `c5332e9333ccb18c5b4a2a3d633e9d643362b88d0f87187c762a86b5317953c4`;
    EXEC `EXECUTION_COMPATIBILITY.md`
    `69e6e79af078980ba16d154f05b462100576908c49901634ea8d6518990a3de7`;
    ACT-POLICY-v0.9 `ACT_AND_POLICY_CONTRACT.md`
    `4ef8c0428d42fbe37be634d79296d7ec80860308345bf4826650fef1739b2229`
    (`HEAD`; cited for D2/D3 distinctions only);
    RS-v0.9 `RECORD_SEMANTICS.md`
    `a91882e74064495c5758110deae4cbc7280f3b2a12d0df8592f5238d1afd16e5`
    (`HEAD`; RS-v0.10 leaves VC-37 and VC-40 unchanged);
    HOSTING-v0.9 `HOSTING_BOUNDARY.md`
    `ce235650e8a9494c66ccd08677556e56a88983aa641b5ff22c576328bd8a93b6`.
  - Pass-4 suppliers (O-B): DEL-09-01 `EXAMINATION_PROTOCOL.md` (EXP-v0.2,
    U1 as repaired; RV confirming) `fc5b8230ec2ab81a9307bd58a573752194a859afbc28eda6bce1a12ee332a20d`;
    DEL-01-06 `PACKAGING_AND_DISTRIBUTION.md` (PKG-v0.1, frozen with this
    unit as U2; cited by section).
  - Receiver: DEL-11-03 ScopeOfWork.md
    `0177354357b07ea177491cffc2b1c75ffac578e179ba96e63e91d6ba34dcf5b6`
    (row DEP-11-03-006).
  - Rulings, cited by ID (R23-21): R23-3, R23-5, R23-7, R23-11, R23-12,
    R23-13, R23-14, R23-17, R23-19, R23-20, R23-21. Other run record:
    `OWNER_DECISIONS.md`
    `e4350f61a93edf0d2d4bfc588fcaa17ae23981baa6059617dcc430cda3008cd8`.
    Standing decisions: first-increment D2, D3, D4; pass-3 DECISION-K3 K-1,
    K-7; DECISION-L L-1, L-6, L-7; SCA-V4-003 DECISION-1 Q-5; the OI-009
    carry ("1 yes").
- **Pin basis (R23-3).** Written for either pin. All three scenarios bind to
  the candidate's one pin (`candidate.codex_pin`); a pin change is an EXP
  change that reopens every scenario. No step relies on a Codex fact that
  differs between 0.158.0 and 0.160.0; the supplier files' own pin
  statements apply to their cases.
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
- **OI-012:** 0.158.0 is the definition pin (D4); the qualification pin is
  named by HELP_HUMAN when VC returns (R23-17).
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

The machine-readable map is `sq.step-map.json`; `check_sq.py` confirms that
every cited supplier case is a designed-case row in that supplier's file
(51 citations; SQ-R6). Case ids are file-qualified (`VC-13` in WD is not
`VC-13` in RS).

### 3.1 V4-EXM-10 — run RUN-A (REQ-002; WR §6 SQ-J)

| Step | What the person and agent do | Observe (EXAMINATION V4-EXM-10) | Supplier cases joined |
|---|---|---|---|
| J-1 | From an empty project folder, plan with the agent and revise the plan | Plan revisions (plan items if plan mode is on, K-5 of pass 3) | NPTD NV-01, NV-02; WR WR-VC-01 |
| J-2 | Execute with substantive real tool use in an ordinary conversation | Tool outcomes as Codex reports them; request cards | NPTD NV-03; NIR VC-NIR-01, VC-NIR-10; RECOVERY VC-R-03 |
| J-3 | Turn the work into a workflow draft | Draft listed with content identity; hygiene | WR WR-VC-02, WR-VC-08; NIR VC-NIR-14 |
| J-4 | Try the draft in a conversation (not a run, K-7) | No run record; draft not selectable for a run | WR WR-VC-09 |
| J-5 | Review the draft | Declared inputs, tools, checkpoints, outputs, evidence; no silent overwrite or rebinding on collision | WR WR-VC-03, WR-VC-05; WD VC-13 |
| J-6 | **The person registers it** at the act control (A15) | Direct-capture record, actor ≠ recorder, bound bytes | AAC VC-AAC-01, VC-AAC-04; NIR VC-NIR-16; RS VC-37; WR WR-VC-12 |
| J-7 | Select the registered revision and run it on new inputs | Source-qualified identity; per-run supply | WR WR-VC-06; EXEC VC-E-18; RS VC-40 |
| J-8 | Refine (revision 2): draft from base, review, **register**, run on new inputs | Second registered revision; run record | WR WR-VC-01, WR-VC-12; EXEC VC-E-17 |
| J-9 | Refine again (revision 3), register, run | Third registered revision; exactly two refinements | WR WR-VC-01, WR-VC-12; EXEC VC-E-17 |

"Refines it twice" is read as two registered revisions, each run on new
inputs (WR TT-7, PROPOSED there; consistent with K-7).

### 3.2 V4-EXM-11 — inside RUN-A (REQ-004, REQ-005)

| Step | When (inside V4-EXM-10) | Action | Observe | Supplier cases joined |
|---|---|---|---|---|
| S11-1 | During J-2's tool-heavy turn | The person stops the turn | Turn ends interrupted; nothing shown done that was not observed | RECOVERY VC-R-02; NIR VC-NIR-10 |
| S11-2 | During J-7's run, with a tool-permission request waiting | Close the window; reopen | Work continued; the request is still listed; closing an observer is not stopping work | RECOVERY VC-R-01; NIR VC-NIR-05 |
| S11-3 | J-7, first request | **Deny** it on its card | Denial settled with its origin; not a human act | NIR VC-NIR-04; RECOVERY VC-R-03 |
| S11-4 | J-7, a later request | **Grant** it | Grant settled; tool success is not an act | RECOVERY VC-R-03; WD VC-28; NPTD NV-07 |
| S11-5 | During J-8, with live work and a request waiting | Quit the App (confirming the question); relaunch | Quit question lists live work; relaunch reads *quit-with-live-work*; requests rebuilt; an interrupted registration attempt reconciled | RECOVERY VC-R-06; NIR VC-NIR-11; WR WR-VC-07 |
| S11-6 | After relaunch | Continue the conversation; carry J-8 to registration | Provider vs rendered state; primary-turn completion vs active descendants; settlement vs received acknowledgment; unknown stays unknown | RECOVERY VC-R-04, VC-R-14; NPTD NV-04 |

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
  tool-permission and sandbox settings in effect, by reference (D3).
- **Material:** invented engineering material only (V4-CST-06), named in the
  candidate subject.
- **Replay where possible:** S11 distinctions that a recording can show
  (HOSTING §9.4 X-04, X-05, X-09, X-10) may be examined additionally as EXP
  rehearsals; they never stand for the native step (EXP-R3, EXP-R4).
- **Browser evidence** (EXP routes `interface_webkit`/`interface_chromium`)
  may support interface parts; it never satisfies a native step.

## 5. The dossier (OUT-002) — `sq.dossier.schema.json`

One dossier per candidate: candidate (revision, build identity, pin,
package record if any); integration owner; examiner and separation, with the
EXP review record; the three scenarios with run reference, steps (state,
EXP result record, outcome, missing input, supplier cases and their own
results where they exist) and outcome; V4-EXM-12's access modes; the
handoff to DEL-11-03; currency; date.

Rules (`check_sq.py`):

- **SQ-R1** All three scenarios, each once.
- **SQ-R2** V4-EXM-11 has V4-EXM-10's run reference.
- **SQ-R3** V4-EXM-12's three modes as in §3.3.
- **SQ-R4** A scenario's outcome is EXP-R1's aggregate of its steps, a step
  without a record counting `not-run`; it never hides a failed or blocked
  step.
- **SQ-R5** The handoff disclaims joined host witness, replacement, public
  release, retirement, professional reliance and practitioner validation.
- **SQ-R6** Every cited supplier case exists in that supplier's file.
- **SQ-R7** Each scenario's steps are exactly the step map's, in order.

## 6. States and sequence

**Dossier state** follows EXP §6.1 per step (`designed`, `awaiting_input`,
`held`, `recorded`). While the dossier is being prepared, steps may wait.
Once the runs are due on the named candidate, **every planned step gets an
EXP record** (R23-20): `not-run` if not attempted, `blocked` with its cause
if attempted and stopped, otherwise its observed outcome. A dossier handed
to DEL-11-03 has every step `recorded`; a partial dossier is handed over
with its gaps only if DEL-11-03 asks, never as qualification. A step
declared not applicable in the case definition before the run (R23-19)
would be listed apart; none of V4-EXM-10/11/12's steps is optional.

**SQ-SEQ:**
1. The integration owner names the candidate and configuration (I-13) and
   opens the dossier; the examiner checks each supplier's focused evidence
   exists (§2) and lists gaps.
2. Run RUN-A: J-1…J-9 with S11-1…S11-6 at their insertion points (§3.2),
   the person operating, the examiner recording each step as an EXP record.
3. Run RUN-B: M12-1…M12-6.
4. Validate every record (EXP rules) and the dossier (SQ rules).
5. Independent review per EXP §7 (Codex reviewer; Claude fallback with an
   observed unavailability; R23-12).
6. Hand the dossier to DEL-11-03.
7. On any change (EXP §6.2) the affected steps reopen; old results stay with
   their candidate.

## 7. Failure behaviour

| ID | Condition | Behaviour |
|---|---|---|
| SF-1 | A supplier contribution is missing | The steps that need it are `awaiting_input` with the input named; other steps may still run if the run's order allows |
| SF-2 | A step cannot proceed mid-run | That step `blocked`; steps needing its end state `not-run`, "blocked by ‹step›" (EXP F-2); the run may continue where independent |
| SF-3 | The person declines to perform an act (e.g. registration) | The step is `not-run` ("act not performed"); no act is recorded or inferred |
| SF-4 | A credentialed mode cannot be configured | M12 step `blocked` (attempted) or `not-run`; no other mode stands in |
| SF-5 | The candidate changes during the dossier | Change-impact record; affected steps reopen; the dossier's `currency` follows |
| SF-6 | Reviewer not separate | Review recorded as such; dossier not reported as independently examined |
| SF-7 | Evidence partial | `inconclusive` with its limit, never `pass` |

## 8. Return to DEL-11-03 (AC-008)

The dossier supplies scenario outcomes, evidence limits, input gaps,
affected rechecks and **v3 comparison inputs**: DEP-11-03-006 asks for "the
v3.0.1 core-loop comparison and applicable V4-EXM-10/11 observations", and
EXAMINATION §7 makes V4-EXM-10 and V4-EXM-11 the core-loop evidence. The
dossier names, per step, the v3 journey that exercised a similar thing as a
*reference for DEL-11-03's comparison* (App v3 `JOURNEY_RESULTS.md`: J04
plan revisions, J05 workflow creation and reuse, J07 three cycles with
refinement, J08 keyboard stop and continuation, J09 deny and grant). The
comparison itself is DEL-11-03's act; v3 evidence qualifies nothing in v4.

## 9. What the person must do, and what is never automated

Review and registration (J-5, J-6, J-8, J-9), answers on request cards
(S11-3, S11-4), quit and relaunch confirmation (S11-5), sign-in and key
entry (M12-1, M12-2). An agent may prepare, prompt and record; it does not
perform these (REQ-003; ACCESS §0; AAC NA-3).

## 10. Verification (designed; VER-001…VER-008)

| Case | Serves | Expected | Needs | Status 2026-10-03 |
|---|---|---|---|---|
| SQ-VC-01 V4-EXM-10 joined run | VER-001, AC-001 | J-1…J-9 recorded on one candidate; exactly two refinements | candidate; person | Not run |
| SQ-VC-02 Declared part and collision | VER-002, AC-002 | J-5 observations; no overwrite or rebinding | candidate; person | Not run |
| SQ-VC-03 Acts: positive and negatives | VER-003, AC-003 | A15 direct capture with actor ≠ recorder; A14 settlements not cited as acts; tool success, silence, timeout supply no act | candidate; person | Not run |
| SQ-VC-04 V4-EXM-11 inside the run | VER-004, AC-004 | S11-1…S11-6 at their points, same run reference | candidate; person | Not run; SQ-R2 enforced (model) |
| SQ-VC-05 Recovery distinctions | VER-005, AC-005 | S11-6 observations; unknown stays unknown | candidate; fixtures | Not run |
| SQ-VC-06 Three modes | VER-006, AC-006 | M12-1…M12-6; three modes as SQ-R3 | candidate; person; credentials (the person's) | Not run; SQ-R3 enforced (model) |
| SQ-VC-07 Dossier examined independently | VER-007, AC-007 | EXP review record; SQ-R1…R7 hold | candidate | Rules run on examples |
| SQ-VC-08 Handoff review | VER-008, AC-008 | SQ-R5; owner boundaries kept | Review | Not run |

**Prototype run** (`PYTHONDONTWRITEBYTECODE=1 python3 check_sq.py` in
`prototype/`, jsonschema 4.26.0, Draft 2020-12; reads only), 2026-10-03:
**TOTAL 72, FAIL 0** — the schema is valid; all 51 supplier case citations
of the step map are designed-case rows in their files; 2 valid dossiers pass
and break no rule; 4 invalid dossiers are rejected; 6 schema-valid
violations are each caught (SQ-R1…SQ-R6).

## 11. For the next amendment (R23-11; nothing edited here)

- TBD-002 and DEP-09-02-027: OI-009 decided (carried by the owner's
  "1 yes").
- TBD-001 and DEP-09-02-024/-025: OI-001/OI-002 ruled by D2/D3 for the first
  increment.
- TBD-003 and DEP-09-02-030: D4's definition pin.
- CLM-001 and DEP-09-02-012: name DEL-01-04's App act control as the capture
  point of registration (same admitted arc; no graph effect).
- Missing supplier-side counterparts for DEP-09-02-014 (DEL-01-06) and
  DEP-09-02-018 (DEL-04-01).
- REQ-006's wording "configured concurrently" reads with L-1 (two homes).

## 12. UNRESOLVED

| ID | Item | Owner | Point of need |
|---|---|---|---|
| U-SQ-1 | Qualification pin | HELP_HUMAN when VC returns (R23-17) | Before the run |
| U-SQ-2 | Which local model and server for M12-3 (and the agent's model in RUN-A) | Implementer, recorded as configuration (R23-17 pattern) | Before the run; a download needs the owner's yes |
| U-SQ-3 | Whether the native steps run on a package (I-6) | Integration owner | Before the run |
| U-SQ-4 | API-key protocol detail (OI-010) | App implementation owner | Before M12-2 |
| — | Placement (decided, as EXP §8.4): the dossier is `Evidence/EXP/<candidate key>/SQ-dossier.json` in DEL-09-02's folder, beside its records | — | — |

## Changes

| Version | Change |
|---|---|
| SQ-v0.1 (2026-10-03) | First Design file: step map over the suppliers' cases, V4-EXM-11 insertion points, dossier schema and rules, DEL-11-03 return; prototype 72/0 |
