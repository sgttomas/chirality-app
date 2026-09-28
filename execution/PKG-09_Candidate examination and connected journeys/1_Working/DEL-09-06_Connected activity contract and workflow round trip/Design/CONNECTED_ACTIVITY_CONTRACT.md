# Connected activity contract — first App/host increment
- Contribution: DEL-09-06/CA-v0.3. It supersedes CA-v0.2 (sha256 31ea3bff05865f425127009f90c070f26b97972e203b5a235791d00332d8dee1, committed at `9fc77baa3`), which superseded CA-v0.1 (sha256 685349b25981ca8333929207890514120d63753cdedd67ae0bad986fc5d45e62, `b4030fe4b`). R5 pass under R5_RESOLUTIONS.md (R5-1, R5-2, R5-4, R5-5, R5-7, R5-9, R5-10).
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001 (draft increment contract: four activities, named expressions, one complete first activity, owner/check allocation, staging, decision/input account — *not* the final operation-specific SoW, which awaits OI-021); OUT-002 (requirements on the reusable connected workflow and its source-qualified revision history — the workflow itself is not authored here); OUT-003 (design of what the V4-EXM-14 joined witness needs — designed, **not run**); OUT-004 (external contribution/evidence account; the question set is `RELAY_QUESTIONS_SWBPIPE.md`); REQ-001…REQ-008; AC-001…AC-008 through designed VER-001…VER-008
- Basis: repo 6e18505e3 (accepted basis); ScopeOfWork.md sha256 511f2c0016920cbf67476f1b8d911ed85d6cfa419e7a6b15f3c7e20457779b37; Dependencies.csv sha256 ce3218a22a8629a731a05f5d24093e9aee6660b011a63414b1589c828e4297ed (ACTIVE EXECUTION rows DEP-09-06-012…024); `P/docs/PRD.md` (sha256 657593ce12a9a6da9f8b6c66579945499d909a8b6272d919d2d14a3db4538573) §2.3, §3–3.1, V4-WF-01…06, V4-AUT-01…05, V4-EXT-01, V4-REP-01, OQ-02, OQ-11; `P/docs/HOST_INTEGRATION.md` (sha256 08c8fc7db2d74619ed47d184f44938bb06f1e2abda0a304a9e11b9230d0960da) §1, V4-HI-25, V4-HI-30…33, V4-HI-40…42, V4-HI-70/71, §11; `P/docs/EXAMINATION.md` (sha256 1b156553dec7eb103dbb1166f5c0dbe9c719d26630d2fcace26c28b3ef54ee19) §1–2, V4-EXM-14, §4; `HANDOFF_SWBPIPE_DOMAINS.md` (sha256 6e7a2f0427acdc0553bd5ea9cceaeceeff5bd82bf1165ed5930c389532e15ef4); owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (OWNER_DECISIONS.md sha256 f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e) D1–D4; R1 (sha256 2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4), R2 (sha256 77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088), R3 (sha256 202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf), R4 at `f05c7e4cd` (sha256 50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24: R4-1…R4-8, R4-13, R4-14, R4-18, R4-20); owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (OWNER_DECISIONS.md at `f05c7e4cd`, sha256 a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c: D5 settled, D6 deferred to SQ-02); `reviews/V2.md` MAJOR-1 (T15 re-point); BRIEFS.md working copy sha256 77a42f8a8c8260285b4142d3a6392a07daead16010b209139efc0d3efc60a21f ("Common brief", "Owner rulings now in force", "Wave 2 — common additions", "W9")
- Consumed inputs:
  - **v0.3 inputs (R5 pass; binding rulings R5_RESOLUTIONS.md at `8fb51f07f`, sha256 254d0b93b9959419a70c6737b07087e1db59b529adc3105a1db31f82b78dd6f1; V3-A and V3-B reviews in the same commit).** Every sibling Design file is read at commit `8fb51f07f` (the committed texts; the working-tree revisions their owners are making in parallel under R5 were not read), and body citations use these versions: DEL-03-01/C-v0.4 sha256 e929d39d3ff9515702f9bfe51dfada537e1cbd165146ec0de4ccf629c659a08c; DEL-03-02/P-v0.4 sha256 0d3960a2e6bd3520368006cdd2b1b67a1fe4eb06e23184aded9d5b98d6c5e361; DEL-04-01/ACT-POLICY-v0.4 sha256 d6da05abe790a4374df7faf225439a01dc1be734491b499d90cf00533369b03b; DEL-04-02/AS-v0.4 sha256 774728d03824397a5343412b17659feaf9b0d2ef1029b79889d13a1b421f4dab; DEL-04-03/RS-v0.4 sha256 56806b64b12a946e706ff236dd1c25fe27ac00877aac13b50ee8603aaf540199; DEL-02-01/WD-v0.4 sha256 e492ff635de972466c8a932355beeae848e1f3d3f60de7304e88963352d8e88e and WD-EX-v0.4 sha256 60ce307a25fe1f9aaad0826985e02aaa6ebd68d86a6d972b1d5a1e39b3128ca4; DEL-05-01/LOOP-v0.4 sha256 ffc3048333f3370ba09a9ce124159b94f2c80ce69b5f593bfb82cc552f95934e; DEL-05-02/PANEL-v0.4 sha256 cb71bc4bd3d8a2034cd236437670d5cd6dad10f8dfcc0d6c75b277573ce84419; DEL-01-01/HOSTING-BOUNDARY-v0.4 sha256 201ea32005dd2c9fb5281a376eb25eebfcb5a644d09a6d3bf5901aaf934c7e58; DEL-02-03/EXEC-v0.2 sha256 7f7848c0de2fdb4dc21f5adafa97f92e179bb66c9f6b04f3434d8f2342317af0; DEL-03-03/ADAPTER-v0.2 sha256 a2905dda5782d7a48fa35ef7e26b0c1517fd3bd995e3ddbba27d2426a25674bc; DEL-03-04/GUIDE-v0.1 sha256 fc96d285a3512065ede29394fe4ef4c5eafc6ccbd08213396826a0bab517afb8. R5 bumps those files (Wave-1 to v0.5, EXEC/ADAPTER to v0.3, GUIDE to v0.2) in parallel with this pass; where R5 fixes a meaning they will carry (the four hold-support values R5-1, host-held carriage R5-2, destination per turn R5-4, V-GR1 R5-7), this file states the R5 ruling directly and cites R5. The entries below are the history of earlier bases.
  - **v0.2 sweep inputs (working tree after `f05c7e4cd`; reported finished by the coordinator).** From v0.2 the short names **C**, **ACT**, **EXEC** and **ADAPTER** denote: DEL-03-01/C-v0.4 `CATALOG_AND_READ_BASIS.md` sha256 e929d39d3ff9515702f9bfe51dfada537e1cbd165146ec0de4ccf629c659a08c (FXA-1…FXA-5, e1/e2, V-ED1, LIB-A1, LIB-A2, AF-1, K-7; T15 confirmed); DEL-04-01/ACT-POLICY-v0.4 `ACT_AND_POLICY_CONTRACT.md` sha256 d6da05abe790a4374df7faf225439a01dc1be734491b499d90cf00533369b03b (§2.6 A13 capture, §4.6 hold support, §12 item 4 (e)/(f), F-15, F-16); DEL-02-03/EXEC-v0.2 `EXECUTION_COMPATIBILITY.md` sha256 7f7848c0de2fdb4dc21f5adafa97f92e179bb66c9f6b04f3434d8f2342317af0 (§2 HP-1…HP-4, HP-H; §3.6; §4.7, §4.9, §4.10; RT-11 W14 map; F-17…F-21); DEL-03-03/ADAPTER-v0.2 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` sha256 a2905dda5782d7a48fa35ef7e26b0c1517fd3bd995e3ddbba27d2426a25674bc (§3.4 model destination, §5.3, PI-2, PI-5, PI-6, XF-40…XF-42, F-15, F-17). At v0.2, DEL-02-01/WD-EX-v0.4 (sha256 60ce307a25fe1f9aaad0826985e02aaa6ebd68d86a6d972b1d5a1e39b3128ca4) was cited only for E1's OP-C12 step; at v0.3 it is cited in full.
  - **v0.1 basis (read with `git show`):**
  - **Wave-1 v0.3 at `ba0b37123`** (history: v0.1/v0.2 basis for P, AS, RS, LOOP, PANEL, WD and HOSTING; superseded by the v0.3 inputs above). The brief names `main` merge `98b1723b`, which is not present in this clone. DISPATCH.md records it as the merge of head `1c36b6d97`; every Wave-1 Design blob is identical at `ba0b37123`, `1c36b6d97` and `e20a3ae8d` (verified by blob id). Short names used below:
    - **C** = DEL-03-01/C-v0.3 `CATALOG_AND_READ_BASIS.md` sha256 ba45e7393ee0b16780f36605ddeecb95ba1f181488e36a46b4b495b69fd67c26 (§4.1, §5, §6, §8, §10 FX-PIPE-01 incl. T15 per V2 MAJOR-1);
    - **P** = DEL-03-02/P-v0.3 `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` sha256 ec0db87f239bc42e2e3e953d660ce3c4ceddf605d7b98cf1393f97a099b699cf (§3–§11);
    - **ACT** = DEL-04-01/ACT-POLICY-v0.3 `ACT_AND_POLICY_CONTRACT.md` sha256 b3748c02006f939d8cc78c6e0b0c847598a8b32d55515ae8658ad80597c98128 (§2, §4, §5, §6, §7, §12);
    - **AS** = DEL-04-02/AS-v0.3 `AUTONOMY_AND_STANDING_EXCHANGE.md` sha256 7b634137bb8402f3eaedc943dab0c5f1114b9d4433d2b94e13540ac0bf8e0514 (§3, §4, §8);
    - **RS** = DEL-04-03/RS-v0.3 `RECORD_SEMANTICS.md` sha256 925f35ca27bd7d1e71a375883ada9903267408af57312eed1ae02b47776a3528 (§3, §4 R1–R13, §6, §7);
    - **LOOP** = DEL-05-01/LOOP-v0.3 `LOOP_RECEIVING_CONTRACT.md` sha256 6b771c8027787193d536fa3507214a8cc579d6ec2f476ee880609c920b6f25c7 (§2, §6, §10, §11, §12, §13);
    - **PANEL** = DEL-05-02/PANEL-v0.3 `PANEL_RECEIVING_CONTRACT.md` sha256 4c47764d3af434c23e63dcc2c10d28f18a4a94546d63d452855c471cfe47bee9 (§3, §5, §7, §8);
    - **WD** = DEL-02-01/WD-v0.3 `WORKFLOW_DECLARATION.md` sha256 84841d9f539767b9ff7ae225fec27f0dc4ebbd2c161c41aff179bbae97f345eb (§4, §6) and **WD-EX** = DEL-02-01/WD-EX-v0.3 `EXAMPLES.md` sha256 0f1058d7f0990e766b3effc3d3de24fc16383197874cced1f5b4212419cf018d (E1, E1c, E2, E3, E4);
    - **HOSTING** = DEL-01-01/HOSTING-BOUNDARY-v0.3 `HOSTING_BOUNDARY.md` sha256 34c3383402aabe6e9347aa2f111318538c4a2a4ca85adb8fffff7e439fdde94e (§3, §6, §8.2) and PIN-SPIKE-v0.1 `PIN_SPIKE_0.158.0.md` sha256 0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115 (pin facts only).
  - **Wave-2 at `e20a3ae8d` (superseded by EXEC-v0.2 and ADAPTER-v0.2 above):** DEL-02-03/EXEC-v0.1 `EXECUTION_COMPATIBILITY.md` sha256 e0ede76ebf08003511755afc666be2466a867fd3256837ee94300cd0dfe518e8 (§2–§8, RT-11); DEL-03-03/ADAPTER-v0.1 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` sha256 58b2409ca45ceea66160eb8910ca38b76b6f335dc184eaeb0896e93cabd0a074 (§2–§10).
  - Owner decision DECISION-2 (D5, D6) replaces the v0.1 citation of `DECISIONS_PENDING_2.md` as pending.
  - SWBPIPE contributions, answers or evidence: **none received** (DEP-001). DEL-09-07, DEL-09-01, DEL-09-02, DEL-02-02, DEL-01-04: accepted SoW meaning only (outside this undertaking, D1).
- Receivers: DEL-09-07 (local host qualification V4-EXM-20…23 — shares the activity; outside this undertaking, D1); DEL-09-09 (V4-EXM-24/25; `EXTERNAL_TRACE_CASES.md`); DEL-02-03 (RT-11 evidence account consumer; §4, §8); DEL-05-01, DEL-05-02, DEL-04-03 (joined observation needs, §8); the external SWBPIPE owner via the human (OUT-004; DEP-09-06-020); the owner and App/shared owner for OI-021 (§2.5); closeout C1 (findings §12).

---

## 0. Reading this definition

**What it defines.** The *draft* increment contract for the first connected
activity (SoW OUT-001): which App/shared contributions each step uses, which
host contribution it needs, who checks what, how the work is staged without
PEC or Domains, what standing each piece of evidence has, and what the
V4-EXM-14 round-trip witness will need. It also states the requirements the
reusable connected workflow must meet (OUT-002) and keeps the external
contribution account (OUT-004).

**What it does not do.** It selects no operation, autonomy or environment:
each stays `UNRESOLVED{OI-021}`. The supports/run adjustment on FX-PIPE-01 is
a **proposed fixture only**. It authors no workflow (authoring follows the
`create-workflow` method and DEL-02-02 review/registration, later
undertaking). It runs nothing. It assigns no SWBPIPE construction. It selects
no wire field, type, transport, hash or canonicalization algorithm,
persistence, process placement or shared-component placement (OI-013, OI-014).

**Naming.** Bold element names are semantic labels, not wire names. Acts are
A1–A14 (R-1); class values are C §3.1's five; outcomes are P §9 and C §4.1;
dispositions are WD §4.3.4's six; checkpoint vocabulary is WD-v0.4's. Fixture
identifiers are C §10's (FX-PIPE-01). Local labels are `L-CA-n`, each with its
reason. External questions are `SQ-nn` from `RELAY_QUESTIONS_SWBPIPE.md`.

**Labels.** SETTLED (accepted basis or owner ruling, cited); DERIVED;
INTEGRATION (R1/R2/R3, cited); **PROPOSED (W9)** for a choice made here, open
to comparison and owner revision. Case states: DESIGNED · AWAITING INPUT
(named input) · HELD (named decision).

---

## 1. Settled distinctions relied on

| # | Distinction | Citation |
|---|---|---|
| S-1 | The first connected activity is: inspect a model, propose an adjustment, request a non-mutating check, meet an intervening edit, recover the actual outcome and receipt; it uses invented engineering material | HANDOFF; EXAMINATION §4 intro; SoW REQ-001 |
| S-2 | Exact operation, autonomy and environment are chosen by the owner via the outside SWB session with the App/shared owner, before connected-activity SoW and execution | OI-021; PRD OQ-11; SoW TBD-001 |
| S-3 | SWBPIPE implementation is the external session's; files are human-relayed; a prepared handoff is not a commitment, delivery or adoption | V4-EXT-01; HI §1, §11; SoW CLM-004, REQ-005 |
| S-4 | Execution, edit acceptance, checking, approval and professional reliance are distinct acts with their own actor and evidence; success establishes none of them | V4-HI-25; V4-AUT-03; #d3; SoW REQ-004 |
| S-5 | A declared checkpoint waits for its act even under direct autonomy | V4-HI-42; V4-WF-05; D2 |
| S-6 | Selected/resolved bytes, what was supplied, provider adoption and observed behavior are separate; registration or a portable file proves nothing | V4-EXM-14; SoW REQ-002 |
| S-7 | Initial activity requires neither PEC nor Domains; independent App work need not wait for the joined witness | SoW REQ-006; PRD §2.3/§8 |
| S-8 | Reserved to the person (App/shared contracts, first increment): A4; A5 where autonomy requires a proposal; A6; A7; A12; A13 enabling. DERIVED: A10 wherever A5 is. INTEGRATION: disabling access is also A13 | D2; R-1; R2-3 |
| S-9 | App routine tool permission is the user's own Codex setting (A14); never a reserved or professional act; hosts have no classifier mode | D3; R2-8 |
| S-10 | Checkpoint satisfaction needs attributable evidence from the capturing surface; a faithful record cites it | R-5; R2-20 |
| S-11 | Every result names its candidate, configuration and date; changed code reopens affected checks; criteria are not weakened | V4-EXM-01/03/05 |
| S-12 | **SETTLED (DECISION-2 D5):** content the App's Codex reads over the host's external channel may go to the model the person selected for that conversation, cloud included, with no App gate; a host may restrict its own channel. **INTEGRATION (DECISION-2 reading; R4-1, R5-4):** the App records the model destination **per turn** where the supplier reports it, including reroutes, keeping requested and effective destinations apart; unobserved turns are *unknown*; the run-level value is the set of destinations observed; a model switch starts no new run; the channel status shows the destination as information, never as a gate | DECISION-2 D5; R4-1; R5-4; HOSTING §8.3 |
| S-13 | How the App holds its own runs at checkpoints is `UNRESOLVED{D6}`, deferred to the SWBPIPE answer to SQ-02 — which can settle it **only for checkpoints on host operations**; App-only checkpoints stay *not enforceable* whatever SWBPIPE answers, a separate D6 follow-up for the owner (R5-10). Each checkpoint on each surface takes one of four values (R5-1): **enforced by the host loop** (embedded route; passes, subject to host evidence); **enforced on the host route** (host-held constraint evidenced by the SQ-02 answer and a candidate; passes); **not established** (awaiting SQ-02, or unagreed exposure; the check does not pass, but this is not *unsupported*); **not enforceable** (no mechanism in this increment — App-only steps, or a constraint carried only as model-supplied; workflow *unsupported*, R4-8). Only **host-held** carriage satisfies R2-12; a host loop's own evaluation of the declaration is host-held; App-assured carriage is not available (R5-2). No App hold is claimed; HP-1 and HP-2 are not adopted; run actions while a checkpoint waits are recorded as *action during hold* | DECISION-2 D6; R4-2, R4-8, R4-14; R5-1, R5-2, R5-10; EXEC §2, §3.6 |
| S-14 | Hold-machine rules adopted set-wide: a lapse after the resume point re-holds the **same** arrival ("waiting — re-held, lapsed at ‹t› after resume"; the run stops at its next action; nothing done is undone; gated outputs show standing *lapsed*; the whole scope is asked again; A5 and A12 never re-hold); an ended run is never resumed (post-end acts are shown "after run end"; continuation is a new run *continues ⟨run⟩* that inherits nothing; interruption is not run end); an act counts only if captured at or after the arrival (else "prior act not counted"; PROPOSED); an A12 counts and supersedes only when the control **established** it (refused → does not count and does not supersede; pending → *waiting*; lost confirmation → *unknown*). For an A12 checkpoint the named fixture is **C V-GR1** (R5-7): `CP-grant` of E1d arrives at r15, T15's A12 is captured after the arrival and counts, and the held call is dispatched unchanged as T16; a T15 captured before the arrival does **not** count — the owner-visible cost is that the person may have to repeat a grant change whose content is already in force (U-E4). A lapse re-holds whatever caused it, including the person's own undo; the person's undo is never recorded as *action during hold*; an undo never re-holds an A5 arrival (R5-5) | R4-3, R4-4, R4-5, R4-6; R5-5, R5-7; EXEC §4.2 HD-5, §4.5 SP-6, §4.7, §4.9, §4.10 |

---

## 2. The first connected activity

### 2.1 Four user activities and the two named expressions (AC-001; SOW-040/041)

| User activity | Its part in the first connected activity | Expression | App/shared contributions | External / other |
|---|---|---|---|---|
| **Practitioner** (engineer): model changes and checks; results/report work | Performs CA-H acts: accepts or rejects proposed items (A5/A10), marks changed rows checked (A4); may change the grant (A12) and enable external access (A13); reads the return | SWBPIPE (host UI, panel); the App for App-side acts | ACT, AS, RS, PANEL (receiving), EXEC §5 | Host act facility, views, receipts (DEP-001); the person |
| **Workflow maker** | Authors, reviews and registers the connected workflow in the App; carries it to the host; opens and refines the host's adaptation back in the App | Chirality App | WD, EXEC §6 (transfer trace); DEL-02-02 (later, D1) | Host library, adaptation (DEP-001) |
| **Application builder** | Realizes catalog entries and tools on the host's three surfaces; supplies the App's receiving side | SWBPIPE (catalog, loop, external interface); the App (adapter) | C, P, LOOP, ADAPTER, HOSTING | Host catalog, route, endpoint (DEP-001) |
| **Coordinator** | Bounds the work, relays questions and returns, records decisions and evidence, keeps the witness honest | The App manager and the human | This file; `RELAY_QUESTIONS_SWBPIPE.md`; DEL-09-07/09-09 examination | The human relays; the owner decides |

The App's standalone workflow-making loop (OBJ-001, DEL-09-02) proceeds
independently of this activity and is not reassigned here (SoW CLM-006).

### 2.2 Acting-surface variants (`UNRESOLVED{OI-021}` environment)

The accepted basis names two routes to the same host operations. Which the
first increment uses is part of the OI-021 environment choice (SQ-04 (c)).
This contract defines both, so neither is presumed.

| Variant | Agent | Surface (C §8) | Receiving contributions | Examination owner |
|---|---|---|---|---|
| **CA/E** | The host's embedded agent through the minimal loop | E | LOOP, PANEL (receiving); construction external (OI-013); the loop's model interface, endpoint/key boundary, call validation and responsiveness are asked in SQ-29…SQ-32 | DEL-09-07 (V4-EXM-20…23) |
| **CA/X** | The Chirality App's Codex through the host's external interface | X | ADAPTER, HOSTING | DEL-09-09 (V4-EXM-25) |

In both variants the person's acts on host content are captured by the host's
act facility (V4-HI-31; EXEC CAP-1). The V4-EXM-14 round trip (§8) uses the
host's run of the carried or adapted workflow, whichever variant the host run
uses; the workflow's App side always runs through stock Codex (HOSTING).

**Hold support by variant (v0.3; S-13, R5-1).** In CA/E every valid
checkpoint is **enforced by the host loop** (LOOP §2.4.4; the loop's own
evaluation of the declaration is host-held, R5-2; evidence DEP-001). In CA/X,
and in any App run:

- a checkpoint on a **host operation** (e.g. E1's `CP-accept` on OP-C4/OP-C5
  results) is **not established** until SQ-02 is answered — the check does not
  pass — and becomes **enforced on the host route** once the host-held
  constraint is evidenced by the answer and a candidate;
- a checkpoint on an **App-only step** (App content such as an A4 on AF-1, or a
  run halt after an App-side output) is **not enforceable**, so the workflow is
  **unsupported** on that surface (R4-8) whatever SWBPIPE answers — a separate
  D6 follow-up for the owner (R5-10; EXEC F-17);
- a constraint carried only as model-supplied is **not enforceable**.

The person may still start such a run (EXEC CC-3); every run action observed
while a checkpoint waits is recorded as *action during hold*. CA/X also needs the
host's A13 enablement facility with a capture-evidence reference (SQ-28);
without it the external channel stays *not enabled* (ACT §2.6, F-15). The
run's model destination is recorded per turn and shown, never gated (S-12).

### 2.3 Step map (REQ-001; AC-001)

Fixture steps are C §10.3's timeline. Host contributions name the relay
question that asks for them.

| Step | Fixture steps | What happens (semantic) | App/shared contributions used | Host contribution needed | Evidence the step yields |
|---|---|---|---|---|---|
| **CA-0 Prepare** (frame) | T1; ⟨set-1⟩; E1 ⟨rev-3⟩ selected | Workflow selected by full identity tuple; required-tool check on the acting surface; grant displayed; hold support per checkpoint on the acting surface; for CA/X the person enables external access (A13) in the host's enablement facility, and the conversation's model destination is shown and recorded, not gated | WD §6, §4.2.4; EXEC §3 (CK-1/CK-2, CR-1…CR-13), §3.6 hold support; AS §3; ADAPTER §3 (channel states, E-1…E-9), §8 S-1; HOSTING §8.2 (App supplied guidance) | Catalog edition with exposure (SQ-11); workflow listing and declared-part reading (SQ-17); A13 enablement facility with capture-evidence reference (SQ-28) and enablement behavior (SQ-13); host-side hold (SQ-02); grant presentation (SQ-05) | Compatibility report with hold support (EXEC CR-9, CR-14); grant display state; channel state and model destination; run record R1, R2, R6 |
| **CA-1 Inspect** | T3 (basis B1), T9 (B2) | Agent reads the supports table; the read carries its basis and per-row subject content identities | C §5, §6; LOOP §2.2 (FX-V1); ADAPTER §4.3 RD-1…RD-5, XF-11; RS R7 | Read results with full basis and subject identities (SQ-03, SQ-07); mapping on X (SQ-12) | Read entry with basis; standing from host result |
| **CA-2 Propose** | T5 (PR-1), T9–T10 (PR-2 queued) | Agent drafts one proposal, one item per change, citing the relied-on basis; the host validates and queues; queued ≠ applied | P §3, §4.1, §9; ACT §5.3, §6 (treatment → outcome); AS §3; LOOP §6 (FX-V2, FX-V3); ADAPTER §5, §6 (RP-3), XF-16, XF-22; WD I-7 / R2-12 constraint | Route, treatment resolution, queue acknowledgment (SQ-09); proposal identity (SQ-08); policy for the operation (SQ-05, SQ-06); constraint receipt (SQ-02) | Dispatch record with origin, grant in force, constraint; *queued* outcome |
| **CA-3 Request a non-mutating check** | T4 (OP-C3 findings), T4a (OP-C12 host check); re-examination after T12 | Agent examines (A3 findings, requester-stated limit) and/or requests the host's named check ("host checks passed/failed: ‹named checks›" with evaluated basis); neither is A4 | C OP-C3, OP-C12, §6.2; R-4 label rule; ADAPTER §4.4, XF-12; RS R10; WD §4.4 promised standing | Which check the activity uses (SQ-04 (b)); where findings are held (SQ-24) | Findings reference (A3); host check result with basis |
| **CA-4 Meet an intervening edit** | T6 (Engineer A edits S-3, r13), T7 (PR-1 refused — stale), T9 (re-draft PR-2, lineage PR-1) | The person edits the model; submission relying on B1 is refused per item with both bases; no retargeting; a re-draft is a new proposal on the new basis | C §5.3/§5.4; P §5, §6; R2-13; LOOP FX-D2; ADAPTER §7.1, §7.2, XF-14, XF-17; EXEC MX-6 (if items leave after queueing) | Per-item stale check on original inspected basis, not queue-time basis (SQ-07); no retargeting | Refusal with relied and current basis; item-left events; lineage |
| **CA-H Human acts at checkpoints** (frame, interleaved) | T11 (A5 item 1, A10 item 2); A4 on changed rows after T12; T2 independent A4; T14 lapse | The run holds at `CP-accept` (A5, kind (c) *queued*) and `CP-check` (A4 on objects changed by the applied outcome); acts are captured by the host facility; the App/loop faithfully records them citing capture evidence; an act counts only if captured at or after the arrival; a lapse after resume re-holds the same arrival; an A12 counts only when established (S-14); in App runs the hold is claimed only where hold support says it is enforced, otherwise *action during hold* is recorded (S-13) | WD §4.3; EXEC §4 (hold machine, SP-1…SP-8, MX rules), §5; ACT §2, §4; RS §6, §7; AS §4; PANEL §3.5, §5; LOOP §2.4 | Capture-evidence reference (SQ-01); content identities and resulting objects (SQ-03); constraint receipt (SQ-02); host enforcement of its reserved list (SQ-05) | Checkpoint arrivals and dispositions (RS R8); human-act records (R9) with actor ≠ recorder |
| **CA-5 Recover the actual outcome and receipt** | T12 (RC-1, resulting objects S-5, R-100), T13 (lost ack; retry same identity), V-OU1, T16–T17 (direct under ⟨set-2⟩, undo) | Application yields a receipt; a lost acknowledgment leads to seeking observation, then a retry with the same identity (on X, seek-before-resubmit is guidance to the agent; a violation is recorded as an evidence limit, ADAPTER PI-2); two sends before acknowledgment are recorded separately (PI-5); de-duplication precedes the basis check; unknown stays unknown; undo reverses a receipt | P §4.4, §4.5, §5, §7, §9; C T12–T13; LOOP §6.3 (FX-O1); ADAPTER §5.6 PI-1…PI-6, §7.3, §7.4, XF-19…XF-21, XF-40, XF-41; EXEC §4.12 RP-1…RP-8; RS R7, R11 | Durable receipts, read by identity, de-duplication order and durability (SQ-08); outcome statements and unknown (SQ-09); undo (SQ-10) | Applied association with receipt link and resulting objects; *outcome unknown* with observer; evidence limits |
| **CA-R Return** (frame) | After CA-5 | Summary of what changed (receipt references), findings, acts actually performed, and unknowns; standings never strengthened | WD §4.4–§4.6; AS §8, §9; RS §4 | Receipt and act references readable (SQ-01, SQ-09) | `summary` output (*agent-prepared*); promised-versus-observed account |

### 2.4 Operating sequence on the proposed fixture (FX-PIPE-01; invented material)

```text
CA-0  select E1 supports-adjust ⟨rev-3⟩ (host) or ⟨rev-A2⟩ (App-carried); CK-2 report
      grant ⟨set-1⟩ effective (policy default): propose        [CA/X: A13 in host facility, SQ-28; destination shown]
CA-1  T3 read OP-C1 → B1 = FX-W1/g1/r12/⟨v12⟩/⟨m-fx⟩, ⟨S-1…S-4@r12⟩
CA-3  T4 OP-C3 (limit 6 m) → findings (A3); T4a OP-C12 → "host check failed: support spacing" @r12
CA-2  T5 draft PR-1 (item 1 OP-C4 add support; item 2 OP-C5 S-3 stiffness), relying on B1
CA-4  T6 Engineer A edits S-3 (r13) → T7 submit PR-1 → both items refused — stale (B1 vs B2)
      T9 re-read (B2) → PR-2 (lineage PR-1) → T10 queued        [CP-accept arrives: waiting]
CA-H  T11 Engineer A: A5 item 1, A10 item 2 (host facility, capture evidence SQ-01)
      → CP-accept resolved negatively, "partial" (EXEC MX-5); on-mixed path: continue with item 1
CA-5  T12 host applies item 1 → RC-1; resulting objects S-5 (created), R-100 (changed)
      T13 ack lost → seek observation by identity → if never received, retry PR-2 same identity
      → host answers recorded state (RC-1; item 2 rejected); else outcome unknown (observer)
CA-3  re-examine: OP-C1 read at r14, OP-C3 → examination-report   [CP-check arrives: waiting on S-5, R-100]
CA-H  Engineer A marks S-5 and R-100 checked (A4, SQ-01) → CP-check performed
CA-R  summary: RC-1, findings, acts performed (A5 item 1, A10 item 2, A4 S-5/R-100), unknowns
```

Graduated-autonomy branch (V4-EXM-22 overlap; used by W14-04): T15 A12 →
⟨set-2⟩ (class **P-03**, grant *direct*, scope {FX-W1; {S-4}}, per C T15 and
V2 MAJOR-1) → T16 OP-C9 applied directly (RC-2, origin mark, undo route, no
acceptance) → E1c `CP-check` waits for A4 on S-4 → T17 undo RC-3 *reverses
RC-2*.

### 2.5 Decision and input account needed to finalize the increment SoW (OUT-001; TBD-001/002)

The final operation-specific increment SoW is **not** claimed. It needs:

| # | Decision or input | Owner | Point of need | Current standing |
|---|---|---|---|---|
| DI-1 | The useful operation(s), including the non-mutating check | Owner via outside SWB session with App/shared owner (OI-021); informed by SQ-04 | Before connected-activity SoW and execution | `UNRESOLVED{OI-021}`; fixture only |
| DI-2 | Permitted autonomy for it; operation-specific reserved additions | Same owners (OI-021); host names its list (V4-HI-30); SQ-05, SQ-06 | Same | D2/D3 adopted for App/shared contracts; host adoption not evidenced (DEP-001) |
| DI-3 | Exact candidate environment (host candidate, configuration, model server) and acting-surface variant (§2.2) | Same owners (OI-021); SQ-04 (c)(d), SQ-27 | Before execution | Not supplied |
| DI-4 | Host act capture and constraint receipt | SWBPIPE owner (SQ-01, SQ-02) | Before any positive checkpoint case | Not supplied |
| DI-5 | Model destination for App conversations reading host content (CA/X only) | Owner (DECISION-2 D5); host side SQ-16 | — | **Settled for the App side**: user flexibility; destination recorded and shown, not gated (S-12). Open only: whether the host restricts its own channel (SQ-16) |
| DI-6 | App-side hold points for App runs | Owner (DECISION-2 D6), deferred to the SWBPIPE answer to SQ-02 for checkpoints on host operations; App-only checkpoints need a separate owner follow-up (R5-10) | Before App-side checkpoint enforcement is claimed | `UNRESOLVED{D6}`; on X, host-operation checkpoints *not established* until SQ-02, App-only checkpoints *not enforceable* (S-13) |
| DI-7 | Multi-row A4 purpose after partial lapse (ACT U-03; EXEC U-E3) | DEL-04-01 with the owner | Before re-hold and lapse fixtures run | Open; EXEC carries it conservatively |
| DI-8 | Extension promise (not needed for the first activity; needed before any extension claim) | Owner with host contract owner (OI-003) | Before extension claim | Open; DEL-09-09 |
| DI-9 | Host A13 enablement facility with capture-evidence reference (CA/X only) | SWBPIPE owner (SQ-28) | Before any live CA/X case | Not supplied; channel stays *not enabled* meanwhile |

---

## 3. The reusable connected workflow (OUT-002; REQ-002; AC-002)

### 3.1 Requirements on the workflow (PROPOSED (W9))

The workflow is authored later under the `create-workflow` method and
reviewed/registered through DEL-02-02 (later undertaking, D1). This section
states what it must declare so that the activity and the round trip can be
examined. Meanings are WD-v0.4's.

| # | Requirement | WD locus |
|---|---|---|
| WR-1 | Full source-qualified identity {kind, origin, source root, name, revision} and derived-from; holding library recorded at listed/selected/resolved | WD §6.1; R-9; EXEC §6.2 |
| WR-2 | Declared part at a stated declaration contract version; every category declared (an undeclared category makes the check *not established*) | WD §3.4 |
| WR-3 | Assumptions stated in prose and as expected inputs with quality/basis requirements (the complete five-element read basis for host reads) | WD §4.1 |
| WR-4 | Required tools by **catalog operation identity and version**, class *host operation*; one per step of §2.3 that calls the host; necessity and fallback for optional ones; never an adapter-specific tool name | WD §4.2; ADAPTER NM-1 |
| WR-5 | Checkpoints with the closed-list act, reached-when kind, subject class, scope, purpose, actor requirement, negative/mixed path and expected act evidence; A5 only with kind (c) *queued* on that proposal's change items | WD §4.3.1, validity rules |
| WR-6 | A governing checkpoint constraint on every change request whose result an A5 checkpoint governs | WD I-7; R2-12 |
| WR-7 | Returned outputs with promised standing from the non-approval vocabulary; human-act standing only conditional on a named checkpoint | WD §4.4 |
| WR-8 | Returned evidence by reference (receipts, bases, findings, act records) | WD §4.5 |
| WR-9 | No A6 (approve) or A7 (rely) checkpoint unless the owner asks for one; reliance stays with the accountable professional outside the workflow | WD-EX E1 note; V4-AUT-05 |
| WR-11 | Hold support stated per checkpoint and acting surface, using the four values of R5-1 (EXEC §3.6). *Not enforceable* makes the workflow *unsupported* on that surface (R4-8); *not established* means the check does not pass yet. A workflow meant to run in the App declares its checkpoints on host operations (enforceable on the host route once SQ-02 is evidenced); App-only checkpoints make it unsupported there | WD §4.2.4 (R4-8); EXEC §3.6; R5-1 |
| WR-10 | Revision history kept by identity: every revision a new identity; adaptation a new identity with derived-from; no same-name rebinding | WD §6.3; EXEC §6.4, §6.6 |

### 3.2 Proposed fixture candidate

- **WF-1 = WD-EX E1 `supports-adjust`** ⟨rev-A2⟩ (App, origin *project*) and
  its host adaptation ⟨rev-3⟩ (origin *host*, derived-from ⟨rev-A2⟩). It
  already covers CA-1, CA-2, CA-4 (re-draft), CA-5 (re-examine after
  application), `CP-accept` and `CP-check`.
- **OP-C12 step (was L-CA-1).** R4-20 adopts the optional OP-C12 *Run
  support-spacing host check* at Inspect and Re-examine, with output
  `host-check-result`, into WD-EX E1 (WD-EX-v0.4, working tree, not declared
  final). L-CA-1 is retired; its label resolves to that E1 step. CA-3 can show
  the agent's findings (A3) and the host's named check side by side.
- **App-side subjects** (C-v0.4): LIB-A1 ⟨fx-proj⟩ holds ⟨rev-A2⟩/⟨rev-A3⟩;
  LIB-A2 ⟨fx-app-import⟩ is the App-side holding library for relayed host
  workflows; AF-1 is the App file for App-side act capture (EXEC CH-23).
- **WF-1c = WD-EX E1c `supports-label`** for the direct-autonomy checkpoint
  case (W14-04 (ii)).
- These are **fixture subjects**. The real workflow's operations follow DI-1.

---

## 4. Round trip App → host → App (REQ-002, REQ-003; SOW-238)

The trace meaning is EXEC §6, consumed unchanged. This contribution joins it
to host evidence; it adds no link.

| Link (EXEC §6.1) | Original ⟨rev-A2⟩ | Revised ⟨rev-3⟩ (host) | Refined ⟨rev-A3⟩ (App; EXEC local label) | Evidence owner | Host input |
|---|---|---|---|---|---|
| listed / selected / resolved | App library LIB-A1 ⟨fx-proj⟩ | host library ⟨fx-root⟩ | LIB-A1 (registered); the relayed host copy is held in LIB-A2 ⟨fx-app-import⟩ | DEL-02-02 (later); host | SQ-17, SQ-18 |
| exported / relayed / received | App → host; manifest (TR-4) | — | — | DEL-02-03; the person; host | SQ-17 |
| adapted | — | new identity, derived-from ⟨rev-A2⟩; checkpoint comparison (AD-2) | — | host | SQ-18 |
| opened / drafted / registered | — | host tuple opened read-only | draft base ⟨rev-3⟩ → registered with derived-from | DEL-02-02 (later) | — |
| supplied | App: HOSTING §8.2, with the run's model destination recorded (S-12) | host loop per turn | App: HOSTING §8.2, with model destination | DEL-01-01; host | SQ-19 |
| provider-adopted | unknown | unknown | unknown | — | — |
| observed behavior | App run records (RS) | host run records | App run records | DEL-04-03; host | SQ-19, SQ-27 |

Rules carried: each link is separate evidence; a revised identity never
inherits an original's link; acts and dispositions never carry across
identities (EXEC AD-5); history is referenced, not copied (V4-HI-71).

---

## 5. Owner and check allocation (OUT-001; AC-001, AC-008)

"Focused check" is the producing owner's own verification, in its file.
"Joined check" is the candidate-bound examination that joins contributions.

| Contribution | Producing owner | Focused check (designed) | Joined check owner | Standing now |
|---|---|---|---|---|
| Catalog and read basis (C) | DEL-03-01 | C VC-C-01…; M3-CP with P | DEL-09-07; DEL-09-09 | v0.4 draft |
| Proposal and outcomes (P) | DEL-03-02 | P VC-P-… | DEL-09-07; DEL-09-09 | v0.4 draft (v0.5 in the R5 pass) |
| Act policy (ACT) | DEL-04-01 | ACT FX-/VC- cases | DEL-09-06 (W14-04/05); DEL-09-09 (XC-09/10) | v0.4 draft; D2/D3 adopted; §2.6 A13 capture; §4.6 hold support |
| Grant display (AS) | DEL-04-02 | AS VC cases | DEL-09-07 (V4-EXM-22) | v0.4 draft (v0.5 in the R5 pass) |
| Records (RS) | DEL-04-03 | RS VC cases | DEL-09-06 (W14-05/07) | v0.4 draft (v0.5 in the R5 pass) |
| Loop receiving (LOOP) | DEL-05-01 (receiving); construction external | LOOP VC-01…09 | DEL-09-07 | v0.4 draft (v0.5 in the R5 pass) |
| Panel receiving (PANEL) | DEL-05-02 (receiving); construction external | PANEL VC-01…07 | DEL-09-07 | v0.4 draft (v0.5 in the R5 pass) |
| Declaration (WD) | DEL-02-01 | WD §13 | DEL-09-06 (W14-01…03) | v0.4 draft (v0.5 in the R5 pass) |
| Execution compatibility, hold machine, transfer trace (EXEC) | DEL-02-03 | VC-E-01…11 | DEL-09-06 (W14-*) | v0.2 draft; App-side holds `UNRESOLVED{D6}` |
| External adapter (ADAPTER) | DEL-03-03 | VC-X-01…08 | DEL-09-09 | v0.2 draft; native family only; no interposition adopted |
| Hosting boundary (HOSTING) | DEL-01-01 | HOSTING VC | DEL-09-06 (W14-08 App side) | v0.4 draft (v0.5 in the R5 pass); pin 0.158.0 (definition pin only) |
| Review, registration, drafts | DEL-02-02 | — | DEL-09-06 (W14-09) | **Not in this undertaking (D1)** |
| App act control | DEL-01-04 | — | — | **Not in this undertaking (D1)** |
| Examination infrastructure and protocol | DEL-09-01 | — | all examiners | **Not in this undertaking (D1)** |
| Local host qualification V4-EXM-20…23 | DEL-09-07 | — | DEL-09-07 | **Not in this undertaking (D1)** |
| External control; extension trace V4-EXM-24/25 | DEL-09-09 | — | DEL-09-09 | XT-v0.3 draft |
| **V4-EXM-14 joined round trip** | **DEL-09-06** | — | **DEL-09-06** | Designed (§8); not run |
| Host catalog, route, receipts, loop, panel, views, act facility, library, endpoint | SWBPIPE owner (DEP-001) | Host-owned checks (SQ-27) | Joined by DEL-09-06/07/09 | Owner-reported building; nothing received |
| Human acts A4, A5, A10, A12, A13 | The person (Engineer A in fixtures) | — | Observed, never performed, by examiners | None performed |
| OI-021, OI-003, U-03, D6 (deferred to SQ-02); D5 decided | The owner (with named co-owners) | — | — | Open, deferred or settled as stated |

---

## 6. Staging without PEC or Domains (REQ-006; AC-006)

| Stage | Content | Needs | Does not need | Output standing |
|---|---|---|---|---|
| **ST-0 Definitions** (now) | v0.3/v0.4 and v0.2 definitions; this contract; relay file; DEL-09-09 cases | Accepted basis | Any host input | *illustrative* |
| **ST-1 App-local executable fixtures** | C/P/ACT/RS/AS/WD/EXEC/ADAPTER fixture runs on test doubles; App run through stock Codex for the App side of the workflow | App construction (later undertaking); DEL-09-01 protocol | Host, OI-021 | *test-double* per file |
| **ST-2 Relay and answers** | `RELAY_QUESTIONS_SWBPIPE.md` relayed; answers recorded | The human; SWBPIPE session | PEC, Domains | Answers with custody; not delivery |
| **ST-3 Activity selection** | OI-021 decided; increment SoW finalized (DI-1…DI-3) | Owner; SQ-04/SQ-05 answers | PEC, Domains | Final increment SoW (future) |
| **ST-4 Host contributions and focused host examination** | Host candidate identified; CA/E (and/or CA/X) exercised; V4-EXM-20…23 by DEL-09-07; V4-EXM-25 by DEL-09-09 | DEP-001 contributions; SQ-01/SQ-02; SQ-28 for CA/X; person's acts | PEC, Domains | *actual host*, candidate-bound. On CA/X, host-operation checkpoints stay *not established* until SQ-02 is evidenced; App-only checkpoints stay *not enforceable* (S-13) |
| **ST-5 Joined V4-EXM-14 round trip** | §8 witness on identified App and host candidates | ST-4 plus DEL-02-02 registration (later undertaking) | PEC, Domains | Completion evidence for OUT-003 (future) |
| **Later** | Domains research/design-candidate increment; PEC coordination | Their own contracts | — | Outside this activity |

Rules: ST-1 and independent App construction never wait for ST-4/ST-5
(REQ-006). A stage's output never claims a later stage. A first-host pass is
not evidence of longer-work recovery (DEL-09-05). Each stage that depends on
an input names it; a defined contract is not treated as an available input
(AC-006).

---

## 7. Evidence standing (REQ-005, REQ-007; AC-005, AC-007)

### 7.1 Examination evidence labels (C-v0.4 mapping, consumed)

| Label | Can support |
|---|---|
| *illustrative* (CONTRACT-REVIEWED / DEFINED) | Completeness of the definition only |
| *test-double* (FIXTURE-EXECUTED / EXECUTED on a double) | That expectation on that double; nothing about the host |
| *actual host* (HOST-OBSERVED / EXECUTED on an identified candidate) | That candidate, configuration and date only |
| AWAITING INPUT / HELD / NOT-OBSERVED | Nothing; recorded as a gap |
| LIMITED (partial) | As stated in the limitation |

Replay of recorded exchanges supports seam checks (V4-EXM-02) and never
substitutes for the live joined witness or a real act. Browser evidence never
replaces required native observation (V4-EXM-04).

### 7.2 External contribution standing ladder (REQ-005; PROPOSED (W9))

Each external item holds exactly one standing, each claimed only with its
evidence:

**prepared** (App file exists) → **relayed** (delivery to the SWBPIPE session
observed) → **answered** (a returned answer, with source and custody) →
**committed** (an explicit statement of commitment by the SWBPIPE owner) →
**delivered** (an identified contribution: revision, candidate) →
**adopted** (the App receiving side records use of it, per file/version) →
**examined** (candidate-bound observation, with outcome).

Unknown custody or absent evidence is shown as such. A stated intention is
**answered**, not **committed**. Nothing moves up the ladder by inference.

---

## 8. What the V4-EXM-14 joined witness will need (OUT-003; REQ-002, REQ-003, REQ-007; AC-003, AC-004, AC-007) — designed, not run

### 8.1 Completion rule

OUT-003 is complete only when an **actual** joined round trip has run on
**identified** App and host candidates: the reviewed workflow carried to the
host, adapted/refined there, and made usable in the App, with each case below
observed and its outcome recorded as passed, failed, blocked, not run or
inconclusive. Definitions, fixtures, test-double runs, registration, partial
or unrun records, and honest absence reports do not complete it
(SoW AC-003, AC-007; VER-007). No favorable human approval is a completion
condition (REQ-007).

### 8.2 Cases

| Case | What is observed | Built on | Inputs still needed | State |
|---|---|---|---|---|
| **W14-00 Identification** | App candidate (build, stock Codex version actually used, model/server), host candidate (source revision, build, configuration), date, invented material identity | V4-EXM-01 | SQ-27 (a); App candidate (later undertaking) | AWAITING INPUT |
| **W14-01 Transfer App → host, unadapted** | exported → relayed → received links; origin *project* kept; holding library per link | EXEC RT-1, TR-1…TR-6 | SQ-17 (a), (d); DEL-02-02 registration (later) | AWAITING INPUT |
| **W14-02 Adaptation** | New host identity with derived-from; checkpoint comparison preserved/changed/removed/added; no identity or act inheritance | EXEC RT-2, RT-3, AD-1…AD-6 | SQ-18 (b), (c) | AWAITING INPUT |
| **W14-03 Required tools and unsupported capability** | Compatibility report on the host's actual edition (available tools **present**); one explicit unsupported/missing outcome observed and shown to the person, with no fabricated tool execution | EXEC MT-1, MT-3, MT-10, MT-15; TF-3/TF-4 | SQ-11; SQ-17 (b), (c) | AWAITING INPUT |
| **W14-04 Checkpoint hold under direct autonomy** | (i) A5 `CP-accept` with a direct grant for the operation's class (V-CP1): direct request *not permitted* naming the constraint; separate proposal queued; waits for A5. This depends wholly on the host route (SQ-02 (a)–(c)); it is **not** App-side hold evidence (EXEC F-19). (ii) E1c `CP-check` after direct application under ⟨set-2⟩ (T15: class P-03, scope {FX-W1; {S-4}}; counts only because the A12 was **established**, S-14): run waits for A4 on S-4; nothing releases it without A4. Run it first on the host loop (CA/E). (iii) The same workflow as an App run on X (R5-1): `CP-accept` (host operation) *not established* until SQ-02 — the check does not pass; any App-only checkpoint *not enforceable* → workflow *unsupported*; any run action while waiting recorded as *action during hold* (ADAPTER XF-42) | EXEC CH-1, CH-27, MT-2, §3.6; WD I-7; C V-CP1, T15–T16; ADAPTER XF-42 | (i) SQ-02; (ii) SQ-01, SQ-03; SQ-05; the person's A12 and A4; (iii) SQ-02 for `CP-accept`; `UNRESOLVED{D6}` owner follow-up for App-only checkpoints | AWAITING INPUT; (iii) shows the limit only |
| **W14-05 Real act, faithfully recorded; fabrication negatives** | Engineer's actual A5/A10 (T11) or A4 captured by the host facility **at or after the arrival** (S-14); App/loop record with actor ≠ recorder, bound content identity, capture-evidence reference. A4 captured before the arrival is shown "prior act not counted". App-side variant: A4 on App file AF-1 in the App act control (EXEC CH-23). Negatives: success, *queued*, receipt, A14, model text, user-input or elicitation answer (not act evidence, R4-12) → no act | EXEC CH-2, CH-20, CH-23, CH-28, CAP-6; WD-EX R-9; ADAPTER XF-31, XF-33; C AF-1 | SQ-01; an actual person performing the act on invented material (DEP-09-06-024); App act control (DEL-01-04, later) for the AF-1 variant | AWAITING INPUT |
| **W14-06 Content change after an act** | Edit to bound content → act-lapsed event. Before the resume point: "waiting — lapsed at ‹t›". After the resume point: the **same** arrival is re-held, "waiting — re-held, lapsed at ‹t› after resume"; the run stops at its next action; nothing done is undone; gated outputs (e.g. `checked-rows`) show standing *lapsed*; the person is asked again for the whole scope (S-14). After run end: *lapsed* per referent. A5 and A12 never re-hold. A lapse caused by the person's own undo (T17 analogue) re-holds the same way; that undo is never recorded as *action during hold*, and it never re-holds an A5 arrival (R5-5). History preserved; no invented current act | EXEC CH-6, CH-7, CH-10, §4.7 RH-1…RH-9; T14, T16a–T17; R5-5 | SQ-03 (b); host lapse display (SQ-23) | AWAITING INPUT (CH-8 (ii) HELD on U-03) |
| **W14-07 Interruption and replay** | Observation lost while waiting; recovery rebuilds dispositions from the record; recovered events not back-filled; held call dispatched unchanged; inspection replay issues nothing. Interruption is not run end; an ended run is never resumed — carrying work on is a new run *continues ⟨run⟩* that inherits nothing (S-14) | EXEC CH-3, CH-4, CH-5, CH-9, CH-21, RP-1…RP-8, §4.9 | SQ-09 (c); SQ-19 (c) | AWAITING INPUT |
| **W14-08 Supplied / adopted / observed** | App side: supplied guidance per thread/turn (HOSTING §8.2) and the model destination per turn where reported, requested and effective kept apart, run-level set of destinations observed (HOSTING §8.3; information only, S-12; R5-4); host side: per-turn guidance if recordable, else *unknown*; adoption *unknown*; observed behavior from run records | EXEC RT-5, CR-14 | SQ-19 (a), (b) | AWAITING INPUT |
| **W14-09 Host → App refinement usable in App** | Host revision relayed and held in LIB-A2 ⟨fx-app-import⟩, opened read-only, refined as a draft, registered in LIB-A1 with derived-from; a run of the refined identity starts with every checkpoint *not reached* and imports no act | EXEC RT-6, RT-8, HR-1…HR-7; C LIB-A1, LIB-A2 | SQ-18 (a); DEL-02-02 (later undertaking) | AWAITING INPUT (DEL-02-02) |
| **W14-10 Revision and replay history** | Several revisions and a same-name collision shown with origins and holding libraries (⟨fx-root⟩, LIB-A1, LIB-A2); replay reads the resolved revision recorded for the run | EXEC RT-7, RP-5; WD-EX E4; C LIB-A1, LIB-A2 | SQ-18 (a) | AWAITING INPUT |

### 8.3 What cannot substitute

- A test-double run, a recorded replay, or a DEL-09-07/09-09 component pass
  for any W14 case (V4-EXM-14: "a portable file or successful registration
  alone does not prove compatible execution").
- An agent-authored or conversation statement for W14-05.
- Transport acknowledgment or session de-duplication for a one-effect claim.
- A pass on an earlier candidate after the candidate changes (V4-EXM-03);
  affected cases reopen without weaker criteria (V4-EXM-05).

---

## 9. External contribution and evidence account (OUT-004; REQ-005; AC-005)

| # | Contribution needed | Supplier | Relay question | Point of need | Standing |
|---|---|---|---|---|---|
| EC-01 | Capture-evidence references for host-captured acts | SWBPIPE owner | SQ-01 | Before positive checkpoint cases | prepared |
| EC-02 | Constraint receipt or host-held declaration | SWBPIPE owner | SQ-02 | Before V-CP1 family | prepared |
| EC-03 | Subject/change-item identities; resulting objects | SWBPIPE owner | SQ-03 | Before binding/lapse cases on a host | prepared |
| EC-04 | Candidate operations, check and environment | SWBPIPE owner (input to OI-021) | SQ-04 | Before connected-activity SoW | prepared |
| EC-05 | Policy for the operation; host reserved list; adoption of treatments | SWBPIPE owner | SQ-05, SQ-06 | Before operation-policy production contracts | prepared |
| EC-06 | Basis, staleness, identity, outcomes, undo, exposure | SWBPIPE owner | SQ-07…SQ-11 | Before integrating an actionable host operation | prepared |
| EC-07 | External seam, enablement behavior, origin, locality, host restriction by model destination | SWBPIPE owner | SQ-12…SQ-16 | Before CA/X live examination | prepared |
| EC-08 | Workflow receiving, adaptation, run records, supplied guidance | SWBPIPE owner | SQ-17…SQ-20 | Before W14 host-side cases | prepared |
| EC-09 | Views, act display, findings, faithful-record operation, proxy capture | SWBPIPE owner | SQ-21…SQ-25 | Before panel receiving | prepared |
| EC-10 | One new operation for the extension trace | SWBPIPE owner | SQ-26 | Before any extension claim (DEL-09-09) | prepared |
| EC-11 | Identified candidates; host-owned checks and witnesses; relay form; actual engineer for joined witnesses | SWBPIPE owner; the person | SQ-27 | Before any candidate-bound result | prepared |
| EC-13 | A13 enablement facility with capture-evidence reference | SWBPIPE owner | SQ-28 | Before any live CA/X case | prepared |
| EC-14 | Embedded loop's model interface and fixture basis (DEP-05-01-024), endpoint/key boundary, malformed-call handling and validation order, responsiveness | SWBPIPE owner; App/shared embedded-integration owner receives or agrees the model interface | SQ-29…SQ-32 | Before loop fixtures and CA/E candidate observations | prepared |
| EC-12 | The OI-021 selection | Owner via outside SWB session with App/shared owner | — | Before connected-activity SoW | open |

"prepared" means the question exists in `RELAY_QUESTIONS_SWBPIPE.md`; relay is
**not observed**. DEP-001 standing remains *owner-reported building before
agent-action integration* — not delivery, adoption or live readiness.

---

## 10. Excluded acts and their owners (REQ-008; AC-008)

| Excluded act | Owner | This contribution's part |
|---|---|---|
| Catalog, proposal, policy, grant display, record, loop, panel, declaration, execution-compatibility, adapter and hosting construction and focused checks | DEL-03-01, DEL-03-02, DEL-04-01, DEL-04-02, DEL-04-03, DEL-05-01, DEL-05-02, DEL-02-01, DEL-02-03, DEL-03-03, DEL-01-01 (CLM-003) | Joins their meanings in §2–§4; performs none |
| Review, registration, selection policy, drafts | DEL-02-02 (later, D1) | Named in W14-01/W14-09 |
| SWB domain objects, catalog, route, receipts, views, loop, panel, act facility, library, endpoint, host execution | External SWBPIPE owner (CLM-004; DEP-001) | Questions only (relay file) |
| OI-021 operation/autonomy/environment; OI-003 extension; U-03; D6 (deferred to SQ-02); D5 (decided by the owner, DECISION-2) | The owner with named co-owners (CLM-005) | Open items recorded as open; decided items applied as decided; never decided here |
| Every human act (A4, A5, A6, A7, A10, A12, A13); professional reliance; engineering approval | The person; the accountable professional | Never performed, inferred or recorded without capture evidence |
| Standalone qualification; local host qualification; external control and extension examination; longer-work recovery; replacement packet | DEL-09-02; DEL-09-07; DEL-09-09; DEL-09-05; DEL-11-03 (CLM-006) | Coordinated through §5 and §6; not performed |
| Relay of files | The human | §4 ledger in the relay file |
| **Retained here** | **DEL-09-06**: the complete activity definition, its joining, and OUT-003 | — |

---

## 11. Interfaces

### 11.1 Expected from suppliers

| Supplier | Element | State |
|---|---|---|
| C, ACT | As cited per step in §2.3 | C-v0.4, ACT-v0.4 at `8fb51f07f`; V-GR1 per R5-7 (added by C in the R5 pass) |
| P, AS, RS, LOOP, PANEL, WD, WD-EX, HOSTING | As cited per step in §2.3 | v0.4 texts at `8fb51f07f` (R5 bumps them in parallel; R5 meanings stated directly) |
| EXEC | Compatibility report with hold support; hold machine; transfer trace; RT fixture design; RT-11 evidence account mapped to W14 | EXEC-v0.2 (working tree); RT-11 names DEL-09-06 as joined-witness owner |
| ADAPTER | Channel states; model destination; carriage assurance; XF inventory incl. XF-40…XF-42 | ADAPTER-v0.2 (working tree) |
| DEL-09-09 | V4-EXM-25 joined cases XC-*; extension trace | `EXTERNAL_TRACE_CASES.md` (this run) |
| DEL-09-07 | V4-EXM-20…23 on CA/E | Not in this undertaking |
| DEL-02-02 | Registration, drafts | Not in this undertaking |
| SWBPIPE owner | EC-01…EC-11, EC-13, EC-14 | None received |
| The owner | DI-1…DI-9 | Open, deferred (D6) or settled (D5) |

### 11.2 Provided to receivers

| Receiver | Provided |
|---|---|
| DEL-09-07 | Step map §2.3 for CA/E; staging §6; evidence ladder §7 |
| DEL-09-09 | Step map for CA/X; W14-04/05 act cases shared with XC-09/10; relay file SQ-12…SQ-16, SQ-26, SQ-28 |
| DEL-02-03 | W14 case needs against RT/CH/MT cases; confirmation that RT-11 is received as an evidence account, not a witness |
| DEL-05-01, DEL-05-02, DEL-04-03 | Joined observation needs (W14-04…W14-08) |
| SWBPIPE owner (via the human) | `RELAY_QUESTIONS_SWBPIPE.md` |
| The owner | §2.5 decision/input account |

---

## 12. Findings (reported; scope and other files unchanged)

### 12.1 v0.1 findings and their disposition

| # | v0.1 finding (short) | Disposition at v0.2 |
|---|---|---|
| F-1 | OUT-003 cannot complete in this undertaking (DEL-02-02 registration outside D1) | Carried to C1 (R4 "out-of-scope receivers") |
| F-2 | Dependencies.csv lacks deliverable-level rows | Carried to C1 (R4 register findings: W9 CA F-2) |
| F-3 | SoW still calls OI-001/OI-002 open | Carried to C1 |
| F-4 | DEL-09-07 and DEL-09-01 outside D1 | Carried to C1 (out-of-scope receivers) |
| F-5 | E1 lacks a host-named check | **Ruled by R4-20**: WD-EX E1 adopts the optional OP-C12 step; L-CA-1 retired (§3.2) |
| F-6 | W14-04 depends on host-held evaluation or an App hold point | **Ruled by DECISION-2 D6 / R4-2**: App holds deferred to SQ-02; applied in S-13, §2.2 and W14-04 (iii) |
| F-7 | T15 scope divergence (V2 MAJOR-1) | **Ruled by R4-18**; C-v0.4 confirms T15; this file already used it |
| F-8 | HANDOFF "approval" wording | Carried to C1 (R4: W9 CA F-8) |
| F-9 | Merge `98b1723b` absent from the clone | Unchanged; recorded in header |

### 12.2 New findings at v0.2

| # | Where | Finding | Proposed disposition |
|---|---|---|---|
| F-10 | EXEC-v0.2 F-17; R4-8 with DECISION-2 D6 | Until SQ-02 evidences a host-side hold, **every checkpointed workflow is *unsupported* on the App/external surface**, so the CA/X expression of the first activity (E1 on X) cannot pass its required-tool check. The first activity's checkpoint cases therefore run on the host loop (CA/E) first, and SQ-02 is on the critical path for CA/X | Present to the owner with the D6 follow-up (EXEC F-17 already proposes this); staging in §6 reflects it |
| F-11 | ACT-v0.4 F-15; SQ-28 | CA/X also depends on a host A13 enablement facility with a capture-evidence reference. Without it the channel stays *not enabled* under the App contracts, which would block V4-EXM-25 and every CA/X case | Relay SQ-28 (new); DI-9 |
| F-12 | LOOP-v0.4 G-1 | W14-04 (i) and (ii) on CA/E rely on the host loop's own evaluation of the declaration. R4-14 names four carriage-assurance values; whether a loop-derived constraint counts as *host-held* is not yet confirmed by DEL-03-02 | DEL-03-02 confirms or names the value; no change here |
| F-13 | EXEC-v0.2 F-21 | The model destination is recorded per run (R4-1). If the person switches model between turns, W14-08's supplied/observed account needs a per-turn destination or a rule that a change starts a new run | DEL-04-03 with DEL-01-01 |
| F-14 | Sweep timing | P, AS, RS, LOOP, PANEL, WD, WD-EX and HOSTING v0.4 texts were not declared final at this sweep, so this file still cites them at v0.3 (`ba0b37123`), except WD-EX-v0.4 for the OP-C12 step | Re-point at the next pass once they are final |

### 12.3 v0.2 findings and their disposition at v0.3

| # | Disposition |
|---|---|
| F-10 | **Amended by R5-1 and R5-10.** On X, host-operation checkpoints (E1's `CP-accept`) are *not established* until SQ-02 — the check does not pass, but the workflow is not "unsupported" for that reason; App-only checkpoints are *not enforceable* and make a workflow *unsupported* whatever SWBPIPE answers. The owner-visible consequence is now two items: SQ-02 for host-operation checkpoints, and a separate D6 follow-up for App-only checkpoints |
| F-11 | Stands; R5-10 states that SQ-28 gates the whole external channel |
| F-12 | **Closed by R5-2**: a host loop's own evaluation is host-held |
| F-13 | **Closed by R5-4**: destination per turn where reported; run-level set; a switch starts no new run (S-12, W14-08) |
| F-14 | **Closed by R5-9**: all siblings cited at their `8fb51f07f` versions |

### 12.4 New findings at v0.3

| # | Where | Finding | Proposed disposition |
|---|---|---|---|
| F-15 | R5-1 with the first activity | E1 (the proposed fixture workflow) has only host-operation checkpoints, so on X it is *not established* rather than *unsupported*; a real connected workflow that adds any App-side checkpoint (e.g. an A4 on an App report) would be *unsupported* on X in this increment | Keep the connected workflow's checkpoints on host operations (WR-11); raise App-only checkpoints with the D6 follow-up |
| F-16 | R5-7 V-GR1 | Under capture-after-arrival (PROPOSED), a person who set the grant just before the run reached `CP-grant` must set it again. This is a usability cost the owner should see with U-E4 | Owner decision on U-E4 |
| F-17 | R5 parallel bumps | Siblings move to v0.5/v0.3 in the same pass. This file states the R5 meanings directly, but its section citations are to the v0.4/v0.2 texts at `8fb51f07f` | Re-point at the next pass if any cited section moves |

---

## Changes from v0.2

v0.2 = CA-v0.2 (sha256 31ea3bff05865f425127009f90c070f26b97972e203b5a235791d00332d8dee1, committed at `9fc77baa3`). R5 pass under R5_RESOLUTIONS.md (commit `8fb51f07f`).

| R5 ID / source | Change |
|---|---|
| **R5-1** (V3-A MAJOR-1; V3-B MAJOR-5) | S-13, §2.2, WR-11, DI-6, ST-4, W14-04 (iii) and UNRESOLVED use the four ruled values: enforced by the host loop; enforced on the host route; not established; not enforceable. `CP-accept` on X is *not established* (awaiting SQ-02), not *unsupported*; App-only checkpoints are *not enforceable* |
| **R5-2** | S-13 and §2.2: only host-held carriage counts; a host loop's own evaluation is host-held; App-assured unavailable. F-12 closed |
| **R5-4** (V3-B m-1) | S-12 relabelled: "may flow, no gate" SETTLED by D5; "record and show", now per turn (requested vs effective, run-level set, no new run on a switch), INTEGRATION (DECISION-2 reading). W14-08 updated; F-13 closed |
| **R5-5** | S-14 and W14-06: a lapse re-holds whatever caused it, including the person's own undo; that undo is never *action during hold*; an undo never re-holds an A5 arrival |
| **R5-7** | S-14 cites C **V-GR1** for the grant-after-arrival case and its owner-visible cost; UNRESOLVED capture-after-arrival row; F-16 |
| **R5-9** | Header lists every sibling at `8fb51f07f` with sha256; body citations of P, WD, RS, AS, LOOP, PANEL, HOSTING at v0.4 and RELAY/XT at v0.3; §5 and §11.1 status rows updated; F-14 closed |
| **R5-10** (V3-B MAJOR-4) | S-13, §2.2, DI-6, UNRESOLVED: SQ-02 settles D6 only for checkpoints on host operations; App-only checkpoints are a separate D6 follow-up; F-10 amended |
| Findings | §12.3 dispositions of F-10…F-14; §12.4 new F-15…F-17 |

Identifiers kept; added F-15…F-17 and §12.3/§12.4.

---

## Changes from v0.1

v0.1 = CA-v0.1 (sha256 685349b25981ca8333929207890514120d63753cdedd67ae0bad986fc5d45e62, committed at `b4030fe4b`). Sweep A1 under R4 (commit `f05c7e4cd`) and DECISION-2.

| R4 / source | Change |
|---|---|
| DECISION-2 D5; R4-1 (guide G-4) | New S-12. D5 is no longer shown as pending: DI-5 settled for the App side (destination recorded and shown, not gated); CA-0 shows and records the model destination; W14-08 records it; UNRESOLVED keeps only the host's own-channel restriction (SQ-16) |
| DECISION-2 D6; R4-2, R4-8, R4-14 (guide G-4) | New S-13 and §2.2 "Hold support by variant": App-side holds `UNRESOLVED{D6}` deferred to SQ-02; only host-held carriage satisfies R2-12; checkpointed workflows unsupported on the App/external surface until a host-side hold is evidenced; action during hold recorded. DI-6, WR-11, ST-4, W14-04 (i)–(iii), CA-H and UNRESOLVED updated; F-10 added |
| R4-3, R4-4, R4-5, R4-6 | New S-14 with the adopted wording (re-hold of the same arrival, no resumption and *continues ⟨run⟩*, capture after arrival, A12 counted and superseding only when established); applied in CA-H, W14-04 (ii), W14-05, W14-06, W14-07 |
| ACT-v0.4 §2.6, U-04(e), F-15; R4-13 | CA-0 and §2.2: A13 only through the host's enablement facility (SQ-28); new DI-9, EC-13, F-11 |
| DEL-03-04 GUIDE-v0.1 G-3 (coordinator addendum) | §2.2 CA/E row and new EC-14 point to the new relay questions SQ-29…SQ-32 (host loop model interface, endpoint/key boundary, call validation, responsiveness) |
| ADAPTER-v0.2 PI-2, PI-5, PI-6 (F-17) | CA-5: seek-before-resubmit is guidance on X, violations recorded; two sends before acknowledgment recorded separately |
| R4-20; C-v0.4 | L-CA-1 retired (WD-EX E1 adopts the OP-C12 step); LIB-A1, LIB-A2 and AF-1 used in §3.2, §4, W14-05, W14-09, W14-10 |
| R4-18 | T15 (P-03; {FX-W1; {S-4}}) confirmed; W14-04 (ii) cites it |
| R4-12 | W14-05 negatives name user-input and elicitation answers as not act evidence |
| Inputs | Header cites C-v0.4, ACT-v0.4, EXEC-v0.2, ADAPTER-v0.2 (working tree, with sha256), R4 and DECISION-2; other Wave-1 files stay at v0.3; §5, §7.1, §11 versions updated |
| Findings | §12 split: v0.1 dispositions (12.1) and new F-10…F-14 (12.2) |

Identifiers kept: CA-0…CA-5, CA-H, CA-R, DI-1…DI-8, WR-1…WR-10, WF-1, WF-1c, ST-0…ST-5, W14-00…W14-10, EC-01…EC-12, F-1…F-9, VC-CA-01…08. Added: S-12…S-14, DI-9, WR-11, EC-13, EC-14, F-10…F-14. Retired: L-CA-1 (alias of the WD-EX E1 OP-C12 step).

---

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| `UNRESOLVED{OI-021}` operation(s), non-mutating check, autonomy, environment, acting-surface variant (DI-1…DI-3) | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution | Draft contract only; FX-PIPE-01 proposed fixture; OP-C11-dependent production HELD |
| Operation-specific reserved additions (OI-021 residue of OI-001) | Same owners; host names its list (V4-HI-30) | Before operation-policy production contracts | D2 applied to App/shared contracts only |
| Host adoption of D2/D3 and treatments (DEP-001) | SWBPIPE owner | Before any enforcement claim | Treatment behavior is receiving meaning |
| DEP-001 contributions EC-01…EC-11, EC-13, EC-14 | SWBPIPE owner via the human | Per §9 | All W14 cases AWAITING INPUT |
| Actual human acts for W14-04/05/06 (DEP-09-06-024) | The person performing them | At witness execution | Positive cases defined only |
| Host restriction of its own channel by model destination (D5 settles the App side) | SWBPIPE owner (SQ-16) | Before a live CA/X candidate is enabled | None on App gating; a host refusal is relayed |
| `UNRESOLVED{D6}` App-side run holds (deferred by the owner to SQ-02) | Owner, on the SWBPIPE SQ-02 answer for host-operation checkpoints; a separate owner follow-up for App-only checkpoints (R5-10); DEL-02-03 computes hold support | Before App-side checkpoint enforcement is claimed | On X: host-operation checkpoints *not established*, App-only checkpoints *not enforceable* (R5-1); W14-04 on the host loop first (F-10) |
| Host A13 enablement facility with capture-evidence reference | SWBPIPE owner (SQ-28) | Before any live CA/X case | CA/X channel stays *not enabled* (F-11) |
| Capture-after-arrival rule (R4-5, PROPOSED) versus counting prior acts (EXEC U-E4) | Owner | Before hold-machine fixtures run | W14-05 applies capture-after-arrival; for A12 the cost is shown by C V-GR1 (a repeated grant change whose content is already in force, R5-7) |
| U-03 multi-row A4 purpose after partial lapse | DEL-04-01 with the owner | Before re-hold/lapse fixtures run | W14-06 partial-lapse variant HELD |
| DEL-02-02 registration (later undertaking, D1) | DEL-02-02 owner | Before W14-01/W14-09 | OUT-003 cannot complete in this undertaking (F-1) |
| DEL-09-01 evidence protocol; DEL-09-07 local qualification (outside D1) | Their owners | Before candidate-bound results | Labels per C mapping only |
| `UNRESOLVED{OI-013}` / `UNRESOLVED{OI-014}` placement | Shared contract owner with SWB implementation owner; App/shared owners | Before implementation boundary contracts | No placement implied |
| `UNRESOLVED{OI-003}` extension promise | Owner with host contract owner | Before extension claim | Not part of the first activity; DEL-09-09 |
| Reusable workflow authoring and review (OUT-002 artifact) | Workflow maker with DEL-02-02 (later) under `create-workflow` | Before W14-01 | §3 requirements only; WF-1 fixture |

## Verification cases

Designed, **not run**. Passing them later shows definition completeness only;
the witness itself is §8.

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-CA-01 Scope and activity coverage | Trace §2.1–§2.3 against the DEL-09-06 row, SOW-040/041/236/237/238/240/241, OBJ-001/004/008 and decision 05 | Four user activities, two named expressions and all five activity steps (plus frame steps) mapped to contributions, owners and checks; OI-021 shown open, no final operation-specific SoW claimed | VER-001 (AC-001) |
| VC-CA-02 Workflow requirements | Check §3 against V4-WF-01…06, WD-v0.4 and WD-EX-v0.4 E1 (OP-C12 step); check WR-11 hold support | Identity, assumptions, inputs/tools, checkpoints, outputs/evidence, revision history required; incompatible/missing tools and checkpoints treated explicitly; no workflow claimed authored | VER-002 (AC-002) |
| VC-CA-03 Round trip design | Check §4 and §8 against V4-EXM-14 and EXEC §6 | Every link separate; original and revised identities kept apart; W14-00…W14-10 cover transfer, adaptation, tools, checkpoints, interruption, revision/replay, supplied/adopted/observed | VER-003 (AC-003) — design only |
| VC-CA-04 Act distinctions | Check W14-04/05/06/07 and §2.3 CA-H against V4-HI-25/31/32/42, D2, R-5, R2-20, R4-2…R4-6 and DECISION-2 | Hold under direct autonomy on the host loop, with no App hold claimed on X (unsupported, action during hold recorded); re-hold wording, no resumption, capture after arrival, A12 counted only when established; faithful record with actor ≠ recorder and capture evidence; fabrication negatives; lapse preserves history; no always-reserved list created; no favorable decision required | VER-004 (AC-004) |
| VC-CA-05 External account | Check §9 and the relay file against DEP-001, OI-021 and REQ-005 | Every external item has owner, point of need and a single standing; nothing beyond *prepared*; custody unknown shown | VER-005 (AC-005) |
| VC-CA-06 Staging | Check §6 against decision 05, PRD §2.3/§3.1/§8 and CLM-006 | No PEC/Domains prerequisite; ST-1 independent; each stage names its inputs; no stage claims a later one | VER-006 (AC-006) |
| VC-CA-07 Evidence standing | Check §7 and §8.1/§8.3 against EXAMINATION §1–2 | Candidate/configuration/date required; replay, test double and component passes cannot complete OUT-003 | VER-007 (AC-007) |
| VC-CA-08 Ownership | Check §5 and §10 one-for-one against REQ-008 and CLM-002…006 | Every excluded act has its owner; DEL-09-06 keeps joining and OUT-003; no policy decided; no shared construction assumed; no acceptance, release, replacement or reliance claimed | VER-008 (AC-008) |
