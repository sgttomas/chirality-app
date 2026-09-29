# Connected activity contract — first App/host increment
- Contribution: DEL-09-06/CA-v0.4. It supersedes CA-v0.3 (sha256 67dde29553325271cc3e3a08591177e6628a659966b13b4bbd93920cdf7d0aa5, last changed at `c6f81a4f2` and unchanged at `94aa9181b`), which superseded CA-v0.2 (sha256 31ea3bff05865f425127009f90c070f26b97972e203b5a235791d00332d8dee1, committed at `9fc77baa3`), which superseded CA-v0.1 (sha256 685349b25981ca8333929207890514120d63753cdedd67ae0bad986fc5d45e62, `b4030fe4b`). R8 pass (A-wave, node A5) under R8_RESOLUTIONS.md (R8-1…R8-7, R8-10, R8-11); earlier R5 pass under R5_RESOLUTIONS.md (R5-1, R5-2, R5-4, R5-5, R5-7, R5-9, R5-10).
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Phase (R8-1; DECISION-4 D4-1): in Phase 1 (this increment) a workflow's declared checkpoints are **plan guidance** (EXEC-v0.4 §2.1 PH-1…PH-10; WD-v0.6 §4.3.0). Neither the App nor a host's embedded loop holds a run, and no workflow is *unsupported* for a hold reason. The hold machine and hold support are kept as the **governance-phase definition (retained)** (EXEC-v0.4 §2.2 GV-1…GV-5), for checkpoints declared **`governed`** (WD-v0.6 §4.3.1, PROPOSED). V4-WF-05's first half is **phased to the governance layer, not withdrawn**, and is flagged for the next accepted-basis update. Host joins are deferred (DECISION-3): nothing here claims a SWBPIPE join, witness or adoption.
- Serves: OUT-001 (draft increment contract: four activities, named expressions, one complete first activity, owner/check allocation, staging, decision/input account — *not* the final operation-specific SoW, which awaits OI-021); OUT-002 (requirements on the reusable connected workflow and its source-qualified revision history — the workflow itself is not authored here); OUT-003 (design of what the V4-EXM-14 joined witness needs — designed, **not run**); OUT-004 (external contribution/evidence account; the question set is `RELAY_QUESTIONS_SWBPIPE.md`); REQ-001…REQ-008; AC-001…AC-008 through designed VER-001…VER-008
- Basis: repo 6e18505e3 (accepted basis); ScopeOfWork.md sha256 511f2c0016920cbf67476f1b8d911ed85d6cfa419e7a6b15f3c7e20457779b37; Dependencies.csv sha256 ce3218a22a8629a731a05f5d24093e9aee6660b011a63414b1589c828e4297ed (ACTIVE EXECUTION rows DEP-09-06-012…024); `P/docs/PRD.md` (sha256 657593ce12a9a6da9f8b6c66579945499d909a8b6272d919d2d14a3db4538573) §2.3, §3–3.1, V4-WF-01…06, V4-AUT-01…05, V4-EXT-01, V4-REP-01, OQ-02, OQ-11; `P/docs/HOST_INTEGRATION.md` (sha256 08c8fc7db2d74619ed47d184f44938bb06f1e2abda0a304a9e11b9230d0960da) §1, V4-HI-25, V4-HI-30…33, V4-HI-40…42, V4-HI-70/71, §11; `P/docs/EXAMINATION.md` (sha256 1b156553dec7eb103dbb1166f5c0dbe9c719d26630d2fcace26c28b3ef54ee19) §1–2, V4-EXM-14, §4; `HANDOFF_SWBPIPE_DOMAINS.md` (sha256 6e7a2f0427acdc0553bd5ea9cceaeceeff5bd82bf1165ed5930c389532e15ef4); owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (OWNER_DECISIONS.md sha256 f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e) D1–D4; R1 (sha256 2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4), R2 (sha256 77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088), R3 (sha256 202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf), R4 at `f05c7e4cd` (sha256 50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24: R4-1…R4-8, R4-13, R4-14, R4-18, R4-20); owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (OWNER_DECISIONS.md at `f05c7e4cd`, sha256 a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c: D5 settled, D6 deferred to SQ-02); `reviews/V2.md` MAJOR-1 (T15 re-point); BRIEFS.md working copy sha256 77a42f8a8c8260285b4142d3a6392a07daead16010b209139efc0d3efc60a21f ("Common brief", "Owner rulings now in force", "Wave 2 — common additions", "W9")
- Consumed inputs:
  - **R8-12 closing pass (node A6; in place, no version bump).** R8_RESOLUTIONS.md sha256 d4c3423310a857af86692d17ddfdd22fa877ee20b07c46e1ee481d1cd750e7af (R8-12, items 1 and 7 applied here). Current sibling versions after R8, as committed at `7a1508452` with A6's in-place R8-12 edits (their byte pins are in GUIDE-v0.3's input table): DEL-02-03/EXEC-v0.4; DEL-02-01/WD-v0.6; DEL-02-01/WD-EX-v0.6; DEL-03-01/C-v0.6; DEL-03-02/P-v0.6; DEL-03-03/ADAPTER-v0.4; DEL-03-04/GUIDE-v0.3; DEL-04-01/ACT-POLICY-v0.6; DEL-04-02/AS-v0.6; DEL-04-03/RS-v0.6; DEL-05-01/LOOP-v0.6; DEL-05-02/PANEL-v0.6; DEL-01-01/HOSTING-BOUNDARY-v0.6; DEL-01-01/PIN-SPIKE-v0.1; DEL-09-09/XT-v0.4; DEL-09-06/RELAY-v0.3. SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` and `FACTS_SQ01_SQ32.md` are unchanged (data about SWBPIPE's current state, not commitments; DECISION-3).
  - **v0.4 inputs (R8 pass, A-wave node A5; every sibling read with `git show` at `94aa9181b`).** R8_RESOLUTIONS.md sha256 1770c96e62caf14322811fca82ceb77eca450d3e1be8665cdbdd5550631e8d02 (R8-1…R8-11; binding). INTAKE_MAP.md (I2) sha256 3cc182955c0f3dd70efa0f1c051870229c2ccc08f36c5cf1445f2eef0dd1ea33: rows 01.11, 02.14, 03.10, 04.1–04.3, 05.8, 06.6, 07.11, 08.7, 09.7, 10.6, 12.3, 16.4, 17.4, 18.5, 19.6, 20.5, 23.3, 24.3, 26.5, 27.1, 27.2, 27.7, 28.3, 29.4, X.1, X.4; Part 2 P2.1, P2.4, P2.13, P2.16–P2.18 and its §2.2 CA rows; Part 3 items 2–6, 10, 12; Part 4.1, 4.5–4.9, 4.11. R8 overrides I2 where they differ. BRIEFS.md sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517 ("Common rules", "A-wave"). OWNER_DECISIONS.md sha256 a5ccab0d39bd1cab37c5556abc9bdedd5341ce76be4712706c8c9d72d623e776 (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3`: host joins deferred; `-DECISION-4` with its clarification: D4-1 phased checkpoints, D4-2, D4-3). Owner files already revised: DEL-02-03/EXEC-v0.4 `EXECUTION_COMPATIBILITY.md` sha256 d32be37797a3c367d342a2d13bbb8dd4279bc52934531d83b8c6ec8c6e7b76d4 (§2.1 PH-1…PH-10, §2.2 GV-1…GV-5, §2.3, §3.6, MT-2, MT-15, MT-16, §7.2 CH cases, U-E1, U-E23…U-E25); DEL-02-01/WD-v0.6 `WORKFLOW_DECLARATION.md` sha256 fce565edfd0cee3fa4583eb292d11cce3e4121ead0cdbed31ba2fe0a52562f28 (§4.3.0 CG-1…CG-7, §4.3.1 incl. the `governed` element); DEL-02-01/WD-EX-v0.6 `EXAMPLES.md` sha256 950b70b2e3f7fdda9a98b13a63746b76936be490dd96cb6e47bbe6dc9c3eba3d (E1, E1c, E1d, E8). SWBPIPE's delivered answers `RELAY_ANSWERS_SWBPIPE.md` (this folder, #1047) sha256 6f01add3977761e42ac6b310faf72ba4fd5455e478605deb83fefb2e4d3a61c7: A-1, A-2, SQ-01…SQ-05, SQ-07…SQ-10, SQ-13, SQ-16…SQ-20, SQ-23, SQ-24, SQ-26…SQ-29, ANS §2–§4. These are data about SWBPIPE's current state, not commitments (DECISION-3). Other sibling Design files are being revised in parallel in the same A-wave and were not re-read; their citations below stay at the versions named in the earlier blocks.
  - **R6 micro-pass inputs (in place, no version bump):** R6_RESOLUTIONS.md sha256 8703e85aa7324e233fab285321e277d720923d3e36e342c865917b55083cb841 (R6-1, R6-4, R6-5); `reviews/V4-A.md` sha256 121deafc40c4baf0dec71f96eb449083b0d93456c2bd448f89a279951ca2eab1; `reviews/V4-B.md` sha256 1569cd15b490a07c1fda44114fd6d017f794c16dfe533c65a27d04aad02c2cfc; DEL-02-03/EXEC-v0.3 working tree sha256 b147d9862fe9e0228139c72ba13c50392dcf66930109c4357587bf97bbdebf42 (§3.5; §3.6 HS-1…HS-5 by held actions; fixture classification table; MT-2, MT-16; U-E23). Sibling labels current at the R6 pass (not re-read in full then; superseded for currency by the R8-12 line above): Wave-1 v0.5 (C-v0.5 states V-ED1's branching and V-GR1), EXEC-v0.3, ADAPTER-v0.3 (XF-42 DESIGNED), GUIDE-v0.2.
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
  - SWBPIPE answers received 2026-09-28 (`RELAY_ANSWERS_SWBPIPE.md`; I2 read `64ea4e59…0689`, delivered bytes `6f01add3…61c7`, which add clarifications only, R8 delta check); no host evidence, commitment or contribution received (DEP-001). DEL-09-07, DEL-09-01, DEL-09-02, DEL-02-02, DEL-01-04: accepted SoW meaning only (outside this undertaking, D1).
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
dispositions are WD §4.3.4's six; checkpoint vocabulary is WD-v0.4's (carried in
WD-v0.6), with WD-v0.6 §4.3.0 (Phase 1: plan guidance) and its optional `governed` element
(R8-1). In Phase 1 the dispositions label the record only: *waiting* means
"reached; act not yet recorded", never "the run is held" (EXEC-v0.4 PH-6,
PROPOSED (A1); confirmed by R8-11 item 1). Fixture
identifiers are C §10's (FX-PIPE-01). Local labels are `L-CA-n`, each with its
reason. External questions are `SQ-nn` from `RELAY_QUESTIONS_SWBPIPE.md`.

**Labels.** SETTLED (accepted basis or owner ruling, cited); DERIVED;
INTEGRATION (R1/R2/R3, cited); **PROPOSED (W9)** for a choice made here, open
to comparison and owner revision. Case states: DESIGNED · AWAITING INPUT
(named input) · HELD (named decision). Where SWBPIPE's answer does not supply
the named input, the case keeps AWAITING INPUT and is annotated "SQ-nn
answered 2026-09-28: ‹gist›; a SWBPIPE owner decision (ANS §2); host joins
deferred (DECISION-3)" (I2 STD-2; R8-6). An answer moves a case only when it
supplies the named input.

---

## 1. Settled distinctions relied on

| # | Distinction | Citation |
|---|---|---|
| S-1 | The first connected activity is: inspect a model, propose an adjustment, request a non-mutating check, meet an intervening edit, recover the actual outcome and receipt; it uses invented engineering material | HANDOFF; EXAMINATION §4 intro; SoW REQ-001 |
| S-2 | Exact operation, autonomy and environment are chosen by the owner via the outside SWB session with the App/shared owner, before connected-activity SoW and execution | OI-021; PRD OQ-11; SoW TBD-001 |
| S-3 | SWBPIPE implementation is the external session's; files are human-relayed; a prepared handoff is not a commitment, delivery or adoption | V4-EXT-01; HI §1, §11; SoW CLM-004, REQ-005 |
| S-4 | Execution, edit acceptance, checking, approval and professional reliance are distinct acts with their own actor and evidence; success establishes none of them | V4-HI-25; V4-AUT-03; #d3; SoW REQ-004 |
| S-5 | **Governance phase (retained):** a declared checkpoint waits for its act even under direct autonomy. **Phase 1 (R8-1, R8-11 item 2):** D2's "no autonomy grant widens past a reserved act" binds, and the host enforces it through its operations; its "or a declared checkpoint" half, WD I-7 and V4-HI-42 are **plan guidance**, and the host's own treatment decides. They bind only for governed checkpoints in the governance phase. V4-WF-05's second half is in force: an act is recorded as done only when the person performs it | V4-HI-42; V4-WF-05; D2; DECISION-4 D4-1; R8-1; R8-11 |
| S-6 | Selected/resolved bytes, what was supplied, provider adoption and observed behavior are separate; registration or a portable file proves nothing | V4-EXM-14; SoW REQ-002 |
| S-7 | Initial activity requires neither PEC nor Domains; independent App work need not wait for the joined witness | SoW REQ-006; PRD §2.3/§8 |
| S-8 | Reserved to the person (App/shared contracts, first increment): A4; A5 where autonomy requires a proposal; A6; A7; A12; A13 enabling. DERIVED: A10 wherever A5 is. INTEGRATION: disabling access is also A13 | D2; R-1; R2-3 |
| S-9 | App routine tool permission is the user's own Codex setting (A14); never a reserved or professional act; hosts have no classifier mode | D3; R2-8 |
| S-10 | Checkpoint satisfaction needs attributable evidence from the capturing surface; a faithful record cites it | R-5; R2-20 |
| S-11 | Every result names its candidate, configuration and date; changed code reopens affected checks; criteria are not weakened | V4-EXM-01/03/05 |
| S-12 | **SETTLED (DECISION-2 D5):** content the App's Codex reads over the host's external channel may go to the model the person selected for that conversation, cloud included, with no App gate; a host may restrict its own channel. **INTEGRATION (DECISION-2 reading; R4-1, R5-4):** the App records the model destination **per turn** where the supplier reports it, including reroutes, keeping requested and effective destinations apart; unobserved turns are *unknown*; the run-level value is the set of destinations observed; a model switch starts no new run; the channel status shows the destination as information, never as a gate | DECISION-2 D5; R4-1; R5-4; HOSTING §8.3 |
| S-13 | **Phase 1 (this increment; SETTLED by DECISION-4 D4-1, framing R8-1).** Declared checkpoints are **plan guidance**. The person and the agent work out the plan around them, and the agents manage any pause, hold point or gate themselves. Neither the App nor a host's embedded loop enforces a hold, blocks a run or reports a workflow *unsupported* because a hold cannot be enforced; no hold-support value is assigned, and the required-tool check depends only on the required tools and the channel state (EXEC-v0.4 PH-1…PH-3; R8-2). A checkpoint's arrival and the act that answers it may be recorded as observation (PH-6). A run action after an arrival and before its act may carry the optional annotation "continued past ‹checkpoint› before ‹act›" (PH-7). Acts are recorded only when the person performs them, and the reserved acts stand (PH-4, PH-5). A checkpoint declared `governed` is honoured only as guidance (PH-9). **D6 is closed for Phase 1** by DECISION-4 and re-opens only when the governance phase is taken up (R8-2). **Governance phase (retained; EXEC-v0.4 §2.2 GV-1…GV-5; for governed checkpoints).** How the App holds its own runs is `UNRESOLVED{D6}`. Each governed checkpoint on each surface takes one of four values (R5-1): **enforced by the host loop** (embedded route; passes, subject to host evidence); **enforced on the host route** (host-held constraint evidenced by the SQ-02 answer and a candidate; passes); **not established** (a host answer not yet given, or unagreed exposure; the check does not pass, but this is not *unsupported*); **not enforceable** (no mechanism — any App-side held action; or, with SQ-02 answered with no host-held route, a checkpoint whose held actions are host operations but whose constraint is only model-supplied or merely received; workflow *unsupported*, R4-8). Classification is by what the checkpoint must hold, not by how it arrives (R6-1). Only **host-held** carriage satisfies R2-12; a host loop's own evaluation of the declaration is host-held; App-assured carriage is not available (R5-2). **SWBPIPE governance-phase input (R8-2):** SQ-02 was answered 2026-09-28, route (iv), none planned, so a governed checkpoint holding only host operations on X is **not enforceable** against SWBPIPE (HS-3 (c)); SQ-11 is answered (no exposure element), so HS-4 does not mask SWBPIPE entries, and against SWBPIPE neither cause of *not established* now applies. A later SWBPIPE decision to plan a route is a revision trigger. HP-1 and HP-2 are not adopted; in that phase run actions while a governed checkpoint waits are recorded as *action during hold* | DECISION-2 D6; DECISION-4 D4-1; R4-2, R4-8, R4-14; R5-1, R5-2, R5-10; R8-1, R8-2; EXEC-v0.4 §2.1, §2.2, §3.6 |
| S-14 | **Phase 1 (R8-1; R8-11 item 1; EXEC-v0.4 §2.1 and PH-8).** The recording content of these rules continues: a performed act whose bound content changes is **recorded as lapsed** (an act-lapsed event, shown against the affected referents; gated outputs show standing *lapsed*), because record truthfulness requires it (V4-REC-05); nothing re-holds, and the agent asks again as its plan requires. Which recorded act answers which arrival (capture at or after the arrival; "prior act not counted"), A12 counting only when **established**, run end and *continues ⟨run⟩*, and the rule that interruption is not run end all stay as record rules. Disposition words may label records. **Governance phase (retained; the re-hold and "run stops" clauses below apply only to governed checkpoints in that phase):** Hold-machine rules adopted set-wide: a lapse after the resume point re-holds the **same** arrival ("waiting — re-held, lapsed at ‹t› after resume"; the run stops at its next action only where hold support is *enforced by the host loop* — otherwise the held host operations are refused (*enforced on the host route*) or the action is recorded as *action during hold* (R6-3); nothing done is undone; gated outputs show standing *lapsed*; the whole scope is asked again; A5 and A12 never re-hold); an ended run is never resumed (post-end acts are shown "after run end"; continuation is a new run *continues ⟨run⟩* that inherits nothing; interruption is not run end); an act counts only if captured at or after the arrival (else "prior act not counted"; PROPOSED); an A12 counts and supersedes only when the control **established** it (refused → does not count and does not supersede; pending → *waiting*; lost confirmation → *unknown*). For an A12 checkpoint the named fixture is **C V-GR1** (R5-7): `CP-grant` of E1d arrives at r15, T15's A12 is captured after the arrival and counts, and the held call is dispatched unchanged as T16; a T15 captured before the arrival does **not** count — the owner-visible cost is that the person may have to repeat a grant change whose content is already in force (U-E4). A lapse re-holds whatever caused it, including the person's own undo; the person's undo is never recorded as *action during hold*; an undo never re-holds an A5 arrival (R5-5) | R4-3, R4-4, R4-5, R4-6; R5-5, R5-7; R8-1; R8-11 item 1; EXEC §4.2 HD-5, §4.5 SP-6, §4.7, §4.9, §4.10; EXEC-v0.4 PH-6, PH-8 |

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

**SWBPIPE's current state (answers of 2026-09-28; SQ-04 (c), SQ-20; I2 04.2,
Part 3 item 6).** SWBPIPE has no live agent and no embedded loop exists or is
selected, so CA/E has no SWBPIPE counterpart now. Its recorded embedded
direction ("embedded Runtime", RUNTIME-ADOPT; D-58) predates D-20; this
contract keeps the v4 loop (V4-ARC-10) and that update is SWBPIPE's to make
when UI-SUCCESSOR resumes (DECISION-4 D4-2; R8-8). For CA/X, SWBPIPE's
records name a development Codex controller over the CLI (DRAFT #885,
unmerged and deferred) as the first caller, not the App's Codex; naming the
App's Codex as a caller is deferred by DECISION-3.

**Phase 1 (this increment; S-13; EXEC-v0.4 §2.1).** On both variants the
workflow's checkpoints are plan guidance. The host loop on CA/E enforces no
hold (PH-2), and on CA/X no checkpoint enters the requirement check: E1, E1c
and E1d via X are decided by their required tools and the channel state (E1
and E1d **pass** on the fixture, whose channel is assumed enabled: EXEC-v0.4
MT-2, MT-16 Phase-1 entries). Against SWBPIPE the channel state is *not enabled* (SQ-28, below),
so no CA/X case can run against it now. Arrivals and acts are recorded as
observation, and acts only when the person performs them (PH-4, PH-6).

**Hold support by variant — governance phase (retained; S-13, R5-1, R8-2).**
The values below read the fixture's checkpoints **as if declared governed**;
no FX-PIPE-01 fixture declares the flag (EXEC-v0.4 GV-5; R8-11 item 5). In
CA/E every valid governed checkpoint is **enforced by the host loop** (LOOP
§2.4.4; the loop's own evaluation of the declaration is host-held, R5-2;
evidence DEP-001; SWBPIPE has no host loop, SQ-20). In CA/X, and in any App
run:

The value is decided by **what the checkpoint must hold**, not by how it
arrives (R6-1; EXEC-v0.4 §3.6):

- if **every held action is a host operation** (HS-3) — e.g. the governed
  operation of E1's `CP-accept` (OP-C4/OP-C5), or the OP-C9 call E1d's
  `CP-grant` holds before dispatch — the value is **not enforceable**:
  SQ-02 was answered on 2026-09-28 with no host-held route (route (iv), none
  planned; HS-3 (c)). *Enforced on the host route* would need a host-held
  route evidenced on a candidate; *not established* (HS-3 (b)) applies only
  while a host's SQ-02 answer is not yet given;
- if **any held action is App-side** (HS-5) — an App agent turn such as a
  Return or summary step, an App tool or harness action, an App file write,
  or any action on App content such as an A4 on AF-1; also, by default, for a
  kind (b)/(c) checkpoint with no held-actions element or whose declared held
  actions do not show host operations only (an A5 or kind (a) checkpoint
  without the element takes its governed operation(s) or held call as its
  held actions; WD §4.3.1, R7-3) —
  the value is **not enforceable**, so the workflow is **unsupported** on that
  surface (R4-8) whatever SWBPIPE answers — with D6, which re-opens with the
  governance phase (R5-10; R8-2; EXEC U-E1, U-E23).

**Governance-phase values for the fixture workflows via X** (EXEC-v0.4 §3.6
fixture classification, MT-2, MT-16; I2 P2.1, P2.4). **E1:** `CP-accept` →
*not enforceable* (HS-3 (c): SQ-02 answered) and `CP-check` → *not
enforceable* (HS-5: it arrives on the App agent's `examination-report` and
holds the Return step), so E1 is *unsupported* ("checkpoint hold not
enforceable on this surface: CP-accept, CP-check"). **E1c:** `CP-check` holds
only the return of the result to the person, an App agent turn → *not
enforceable* (HS-5) → *unsupported*. **E1d:** `CP-grant` → *not enforceable*
(HS-3 (c): SQ-02 (d) answered No/No) and `CP-check` → *not enforceable*
(HS-5) → *unsupported* ("…: CP-grant, CP-check"). SQ-02 is answered, so
neither kind of checkpoint can be enforced from the App on SWBPIPE's X in
that phase. On the embedded route (CA/E) all of these would be *enforced by
the host loop*, subject to host evidence that cannot exist for SWBPIPE now
(SQ-20). Combined, **no governed checkpoint could be examined as enforced
against SWBPIPE on either surface** as its answers stand (I2 Part 4.6; F-18).

In the governance phase the person may still start such a run (EXEC CC-3),
and every run action observed while a governed checkpoint waits is recorded
as *action during hold*. In Phase 1 there is no hold, and such an action may
carry only the optional annotation "continued past ‹checkpoint› before ‹act›"
(PH-7).

**Channel (both phases; SQ-28, R8-6).** CA/X needs the host's A13 enablement
facility with a capture-evidence reference. SWBPIPE answered SQ-28 on
2026-09-28: no facility exists or is planned (its opt-in is a launch
environment variable plus a build feature, not a captured act; SQ-13), so the
external channel stays *not enabled* against SWBPIPE (ACT §2.6, F-15). A13
stays a reserved act (R8-1). SWBPIPE's `controller_unavailable` is reported
as *endpoint unavailable*, and the channel shows *disabled*. If the host
answers while no A13 is evidenced, an evidence limit is recorded. Whether a
launch environment variable the person sets counts as A13 evidence is an
owner question deferred to when UI-SUCCESSOR resumes (R8-6, R8-Q4b). The
run's model destination is recorded per turn and shown, never gated (S-12).

### 2.3 Step map (REQ-001; AC-001)

Fixture steps are C §10.3's timeline. Host contributions name the relay
question that asks for them.

| Step | Fixture steps | What happens (semantic) | App/shared contributions used | Host contribution needed | Evidence the step yields |
|---|---|---|---|---|---|
| **CA-0 Prepare** (frame) | T1; ⟨set-1⟩; E1 ⟨rev-3⟩ selected | Workflow selected by full identity tuple; required-tool check on the acting surface; grant displayed; checkpoints listed as plan guidance (Phase 1, PH-3; hold support per governed checkpoint only in the governance phase, S-13); for CA/X the person enables external access (A13) in the host's enablement facility (SWBPIPE has none, SQ-28: CA/X cannot be enabled against it), and the conversation's model destination is shown and recorded, not gated | WD §6, §4.2.4, §4.3.0; EXEC §3 (CK-1/CK-2, CR-1…CR-13), §2.1, §3.6 hold support (governance phase); AS §3; ADAPTER §3 (channel states, E-1…E-9), §8 S-1; HOSTING §8.2 (App supplied guidance) | Catalog edition with exposure (SQ-11); workflow listing and declared-part reading (SQ-17); A13 enablement facility with capture-evidence reference (SQ-28) and enablement behavior (SQ-13); host-side hold (SQ-02); grant presentation (SQ-05). SWBPIPE answered (2026-09-28): no exposure element (SQ-11); no workflow library or declaration reader (SQ-17); no A13 facility, opt-in by launch environment variable (SQ-28, SQ-13); no host-held route, route (iv) (SQ-02; governance-phase input); no class system or grant states (SQ-05) | Compatibility report (EXEC CR-9, CR-14; checkpoints as guidance in Phase 1, hold support per governed checkpoint in the governance phase); grant display state; channel state and model destination; run record R1, R2, R6 |
| **CA-1 Inspect** | T3 (basis B1), T9 (B2) | Agent reads the supports table; the read carries its basis and per-row subject content identities. Where a host supplies only a whole-model identity (SWBPIPE, SQ-03), that identity is received as the identity of every subject it covers; the App never computes identities (R8-4) | C §5, §6; LOOP §2.2 (FX-V1); ADAPTER §4.3 RD-1…RD-5, XF-11; RS R7 | Read results with full basis and subject identities (SQ-03, SQ-07); mapping on X (SQ-12) | Read entry with basis; standing from host result |
| **CA-2 Propose** | T5 (PR-1), T9–T10 (PR-2 queued) | Agent drafts one proposal, one item per change, citing the relied-on basis; the host validates and queues; queued ≠ applied | P §3, §4.1, §9; ACT §5.3, §6 (treatment → outcome); AS §3; LOOP §6 (FX-V2, FX-V3); ADAPTER §5, §6 (RP-3), XF-16, XF-22; WD I-7 (plan guidance in Phase 1, R8-11 item 2) / R2-12 constraint (governance phase); the agent never adds fields the host schema lacks (R8-10) | Route, treatment resolution, queue acknowledgment (SQ-09); proposal identity (SQ-08); policy for the operation (SQ-05, SQ-06); constraint receipt (SQ-02: answered, none; a constraint field would be refused as unknown) | Dispatch record with origin, grant in force, constraint; *queued* outcome |
| **CA-3 Request a non-mutating check** | T4 (OP-C3 findings), T4a (OP-C12 host check); re-examination after T12 | Agent examines (A3 findings, requester-stated limit) and/or requests the host's named check ("host checks passed/failed: ‹named checks›" with evaluated basis); neither is A4 | C OP-C3, OP-C12, §6.2; R-4 label rule; ADAPTER §4.4, XF-12; RS R10; WD §4.4 promised standing | Which check the activity uses (SQ-04 (b): answered, no selection; candidates listed in DI-1); where findings are held (SQ-24: answered, not stored on main; DESIGN only) | Findings reference (A3); host check result with basis |
| **CA-4 Meet an intervening edit** | T6 (Engineer A edits S-3, r13), T7 (PR-1 refused — stale), T9 (re-draft PR-2, lineage PR-1) | The person edits the model; submission relying on B1 is refused with both bases — per item where the host supplies subject identities; otherwise in the host's stated staleness scope, which the App shows and never narrows (SWBPIPE: whole model, so any model change stales every queued proposal; R8-3); de-duplication still runs first; no retargeting; a re-draft is a new proposal on the new basis | C §5.3/§5.4; P §5, §6; R2-13; LOOP FX-D2; ADAPTER §7.1, §7.2, XF-14, XF-17; EXEC MX-6 (if items leave after queueing) | Per-item stale check on original inspected basis, not queue-time basis (SQ-07); no retargeting (SWBPIPE: whole-model staleness; original basis frozen only in DRAFT #885, unmerged and deferred; SQ-07 (c), (d)) | Refusal with relied and current basis; item-left events; lineage |
| **CA-H Human acts at checkpoints** (frame, interleaved) | T11 (A5 item 1, A10 item 2); A4 on changed rows after T12; T2 independent A4; T14 lapse | **Phase 1:** `CP-accept` (A5, kind (c) *queued*) and `CP-check` (A4 on objects changed by the applied outcome) are plan guidance; their arrivals may be recorded, and nothing is held (S-13). **Both phases:** acts are captured by the host facility; the App/loop faithfully records them citing capture evidence, and only when the person performs them; an act counts only if captured at or after the arrival; a lapse is recorded; an A12 counts only when established (S-14). **Governance phase (governed checkpoints):** the run holds on E; in App runs the hold is claimed only where hold support says it is enforced, otherwise *action during hold* is recorded; a lapse after resume re-holds the same arrival (S-13, S-14). SWBPIPE's A5 is **Apply**, acceptance and application in one step per batch, with no A10 record (R8-5) | WD §4.3; EXEC §4 (hold machine, SP-1…SP-8, MX rules), §5; ACT §2, §4; RS §6, §7; AS §4; PANEL §3.5, §5; LOOP §2.4 | Capture-evidence reference (SQ-01: answered, none; the Apply receipt names no person or time and is session-only); content identities and resulting objects (SQ-03: whole-model identity only); constraint receipt (SQ-02: none); host enforcement of its reserved list (SQ-05: no named list; every change waits for Apply) | Checkpoint arrivals and dispositions (RS R8); human-act records (R9) with actor ≠ recorder |
| **CA-5 Recover the actual outcome and receipt** | T12 (RC-1, resulting objects S-5, R-100), T13 (lost ack; retry same identity), V-OU1, T16–T17 (direct under ⟨set-2⟩, undo) | Application yields a receipt; a lost acknowledgment leads to seeking observation, then a retry with the same identity (on X, seek-before-resubmit is guidance to the agent; a violation is recorded as an evidence limit, ADAPTER PI-2); two sends before acknowledgment are recorded separately (PI-5); de-duplication precedes the basis check; unknown stays unknown; undo reverses a receipt (where the host's undo writes none, as SWBPIPE's session undo does, "reverses ⟨receipt⟩" is *not supplied*, R8-5) | P §4.4, §4.5, §5, §7, §9; C T12–T13; LOOP §6.3 (FX-O1); ADAPTER §5.6 PI-1…PI-6, §7.3, §7.4, XF-19…XF-21, XF-40, XF-41; EXEC §4.12 RP-1…RP-8; RS R7, R11 | Durable receipts, read by identity, de-duplication order and durability (SQ-08); outcome statements and unknown (SQ-09); undo (SQ-10). SWBPIPE answered: DRAFT #885 de-duplication and `status` within one controller session only (SQ-08); receipts session-only, `outcome_unknown` resolvable only within that session (SQ-09 (c)); session undo, not through the route, no receipt (SQ-10) | Applied association with receipt link and resulting objects; *outcome unknown* with observer; evidence limits |
| **CA-R Return** (frame) | After CA-5 | Summary of what changed (receipt references), findings, acts actually performed, and unknowns; standings never strengthened | WD §4.4–§4.6; AS §8, §9; RS §4 | Receipt and act references readable (SQ-01, SQ-09) (SWBPIPE: receipts session-only; no act references; SQ-01, SQ-09 (c)) | `summary` output (*agent-prepared*); promised-versus-observed account |

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

**Reading the sequence (R8).** In Phase 1, "waiting" above is a record label
("reached; act not yet recorded"), never "the run is held" (S-13; PH-6), and
"waits for A4" means the agent's plan pauses for it. The sequence is a
fixture. Against SWBPIPE's answers several steps have no counterpart, and the
App keeps its meanings and records the missing counterparts (R8-5; I2
Part 4.9): SWBPIPE's A5 is **Apply**, per batch and atomic, with acceptance
and application in one step and no A10 record, so T11's per-item A5/A10 and
the *partial* disposition have no SWBPIPE counterpart; its #885 `withdrawn`
(the person cleared the queue) is an item leaving "cleared by the person, no
decision record", and `validation_rejected` at Apply is *refused — invalid*
at application — neither is ever A10 or A11; its undo is a session snapshot
with no receipt, so T17's "reverses RC-2" is *not supplied*; it has no grant
states, so ⟨set-2⟩ and T16's direct application have no counterpart (SQ-05).

### 2.5 Decision and input account needed to finalize the increment SoW (OUT-001; TBD-001/002)

The final operation-specific increment SoW is **not** claimed. It needs:

| # | Decision or input | Owner | Point of need | Current standing |
|---|---|---|---|---|
| DI-1 | The useful operation(s), including the non-mutating check | Owner via outside SWB session with App/shared owner (OI-021); informed by SQ-04 | Before connected-activity SoW and execution | `UNRESOLVED{OI-021}`; fixture only. **Stays open** (R8-10). SQ-04 answered 2026-09-28: no selection (an owner decision with the App/shared owner). Candidate operations recorded from SWBPIPE's answer: on main, 27 change kinds through one engine route (`operation_applier`); reads (model read; DRAFT #885 `inspect`); checks (validate-only preview; mechanics solve with host-named integrity standing; user rule checks); DRAFT #885 wires only Node `position.x` set_field on X (single and ordered atomic batch). SWBPIPE has no per-operation identity or version (SQ-12), so FX-PIPE-01's operations are not SWBPIPE catalog identities |
| DI-2 | Permitted autonomy for it; operation-specific reserved additions | Same owners (OI-021); host names its list (V4-HI-30); SQ-05, SQ-06 | Same | D2/D3 adopted for App/shared contracts. Host: no class system, no grants, no named reserved list; every change waits for the person's Apply (SQ-05); SWBPIPE's autonomy is its owner decision OI-016. A grant display for a host without grants, "host fixed treatment: every change waits for Apply", is PROPOSED and deferrable (R8-10) |
| DI-3 | Exact candidate environment (host candidate, configuration, model server) and acting-surface variant (§2.2) | Same owners (OI-021); SQ-04 (c)(d), SQ-27 | Before execution | Answered (SQ-04 (c)(d), 2026-09-28): SWBPIPE's first expression is a development Codex controller over the CLI, then an embedded agent later; the App's Codex is not named (DECISION-3 defers naming it). Environment: macOS only; DRAFT PR #885 (head `12907f393`) unmerged and **deferred** to UI-SUCCESSOR, with the owner's live-controller activation still in force; `SWBPIPE_LIVE_CONTROL=1`, CLI feature `live-control-cli`; no date. No candidate is supplied |
| DI-4 | Host act capture and constraint receipt | SWBPIPE owner (SQ-01, SQ-02) | Before any positive checkpoint case | Answered (SQ-01, SQ-02, 2026-09-28): no capture-evidence reference (the Apply receipt names no person or time and does not survive restart); no host-held route (route (iv); governance-phase input). Acceptance-record storage and actor identity are SWBPIPE owner decisions (PB-TBD-002; DEL-16-03; ANS §2) |
| DI-5 | Model destination for App conversations reading host content (CA/X only) | Owner (DECISION-2 D5); host side SQ-16 | — | App side: "content may flow to the selected model, no gate" is **SETTLED** (DECISION-2 D5); "record and show the destination" is **INTEGRATION** (DECISION-2 reading; R4-1, R5-4) (S-12). Host side answered (SQ-16, 2026-09-28): no restriction; the App need state nothing |
| DI-6 | App-side hold points for App runs | Owner (DECISION-2 D6; DECISION-4 D4-1). SWBPIPE answered SQ-02 on 2026-09-28 with no host-held route (route (iv)); D6 is **closed for Phase 1** and re-opens with the governance phase (R8-2; EXEC U-E1, U-E23) | When the governance phase is taken up for a workflow that needs it; before App-side checkpoint enforcement is claimed | Phase 1: none needed; no App or host-loop hold, no *unsupported* for a hold reason (S-13). Governance phase: `UNRESOLVED{D6}`; on X, host-operation checkpoints *not enforceable* (SQ-02 answered: none; HS-3 (c)), App-only checkpoints *not enforceable* (HS-5), so E1 on X is *unsupported* (EXEC-v0.4 MT-2 governance-phase value) |
| DI-7 | Multi-row A4 purpose after partial lapse (ACT U-03; EXEC U-E3) | DEL-04-01 with the owner | Before re-hold and lapse fixtures run | Open; EXEC carries it conservatively |
| DI-8 | Extension promise (not needed for the first activity; needed before any extension claim) | Owner with host contract owner (App v4 OI-003) | Before extension claim | Open; DEL-09-09. SQ-26 answered 2026-09-28: not chosen; SWBPIPE has no catalog editions and no edition-addition event. This is App v4 OI-003, distinct from SWBPIPE's own OI-003 (R8-7) |
| DI-9 | Host A13 enablement facility with capture-evidence reference (CA/X only) | SWBPIPE owner decision (A13 enablement facility; ANS §2) | When the owner resumes UI-SUCCESSOR (DECISION-3); before any live CA/X case | Answered (SQ-28, 2026-09-28): no facility exists or is planned; the channel stays *not enabled*; `controller_unavailable` reported as *endpoint unavailable* (R8-6). Whether a person-set launch environment variable counts as A13 evidence: owner, deferred (R8-Q4b) |

---

## 3. The reusable connected workflow (OUT-002; REQ-002; AC-002)

### 3.1 Requirements on the workflow (PROPOSED (W9))

The workflow is authored later under the `create-workflow` method and
reviewed/registered through DEL-02-02 (later undertaking, D1). This section
states what it must declare so that the activity and the round trip can be
examined. Meanings are WD-v0.4's, carried in WD-v0.6 (with its Phase-1
statement, §4.3.0).

| # | Requirement | WD locus |
|---|---|---|
| WR-1 | Full source-qualified identity {kind, origin, source root, name, revision} and derived-from; holding library recorded at listed/selected/resolved | WD §6.1; R-9; EXEC §6.2 |
| WR-2 | Declared part at a stated declaration contract version; every category declared (an undeclared category makes the check *not established*) | WD §3.4 |
| WR-3 | Assumptions stated in prose and as expected inputs with quality/basis requirements (the complete five-element read basis for host reads) | WD §4.1 |
| WR-4 | Required tools by **catalog operation identity and version**, class *host operation*; one per step of §2.3 that calls the host; necessity and fallback for optional ones; never an adapter-specific tool name. SWBPIPE has no capability catalog: no per-operation identity or version (SQ-12, SQ-18 (e)), so WR-4 references cannot resolve against it (EXEC EV-4 *not established*; R8-10) | WD §4.2; ADAPTER NM-1; R8-10 |
| WR-5 | Checkpoints with the closed-list act, reached-when kind, subject class, scope, purpose, actor requirement, negative/mixed path, expected act evidence and held actions; A5 only with kind (c) *queued* on that proposal's change items. In Phase 1 these are plan guidance (WD-v0.6 §4.3.0). A checkpoint that will need governance may be declared **`governed`** (WD-v0.6 §4.3.1; optional, PROPOSED); the fields stay declared either way, because the governance phase consumes them. An invalid checkpoint declaration is a declaration finding (invalid, with its FB code): it gives no hold-support value and, in Phase 1, does not make the workflow *not established* (R8-11 item 3) | WD §4.3.0, §4.3.1, validity rules; R8-1; R8-11 |
| WR-6 | A governing checkpoint constraint on every change request whose result an A5 checkpoint governs. **Phase 1:** I-7 is plan guidance; the agent submits a proposal as its plan says, and the host's own treatment decides (R8-11 item 2). The agent never adds a field the host schema lacks (R8-10): SWBPIPE's strict preflight would refuse a constraint field as unknown (SQ-02 (a), SQ-31), so WR-6 applies where the host defines the element. **Governance phase:** carriage per R2-12 for governed checkpoints | WD I-7; R2-12; R8-10; R8-11 |
| WR-7 | Returned outputs with promised standing from the non-approval vocabulary; human-act standing only conditional on a named checkpoint | WD §4.4 |
| WR-8 | Returned evidence by reference (receipts, bases, findings, act records) | WD §4.5 |
| WR-9 | No A6 (approve) or A7 (rely) checkpoint unless the owner asks for one; reliance stays with the accountable professional outside the workflow | WD-EX E1 note; V4-AUT-05 |
| WR-11 | **Phase 1:** no hold support is stated or assigned; checkpoints never make the workflow *unsupported* (EXEC-v0.4 PH-3; WD-v0.6 CG-3). **Governance phase (retained), for governed checkpoints:** hold support stated per checkpoint and acting surface, using the four values of R5-1 (EXEC §3.6). *Not enforceable* makes the workflow *unsupported* on that surface (R4-8); *not established* means the check does not pass yet. If a governed checkpoint must be enforceable from the App, **keep every action it holds on host operations** (it can then become *enforced on the host route* on a host that offers and evidences a host-held route); a checkpoint that holds any App-side action (an App agent turn such as Return, an App tool, App content) makes the workflow unsupported there, however it arrives (R6-1). Against SWBPIPE (SQ-02 answered: route (iv)) this route is not available, so no governed checkpoint is enforceable from the App on X; the advice stands for a host that offers a host-held route (I2 P2.13; R8-2) | WD §4.2.4 (R4-8), §4.3.0, §4.3.1; EXEC-v0.4 §2.1, §3.6; R5-1; R6-1; R8-1; R8-2 |
| WR-10 | Revision history kept by identity: every revision a new identity; adaptation a new identity with derived-from; no same-name rebinding | WD §6.3; EXEC §6.4, §6.6 |

### 3.2 Proposed fixture candidate

- **WF-1 = WD-EX E1 `supports-adjust`** ⟨rev-A2⟩ (App, origin *project*) and
  its host adaptation ⟨rev-3⟩ (origin *host*, derived-from ⟨rev-A2⟩). It
  already covers CA-1, CA-2, CA-4 (re-draft), CA-5 (re-examine after
  application), `CP-accept` and `CP-check`.
- **OP-C12 step (was L-CA-1).** R4-20 adopts the optional OP-C12 *Run
  support-spacing host check* at Inspect and Re-examine, with output
  `host-check-result`, into WD-EX E1 (WD-EX-v0.4, working tree, not declared
  final then; carried in WD-EX-v0.6). L-CA-1 is retired; its label resolves to that E1 step. CA-3 can show
  the agent's findings (A3) and the host's named check side by side.
- **App-side subjects** (C-v0.4; carried in C-v0.6): LIB-A1 ⟨fx-proj⟩ holds ⟨rev-A2⟩/⟨rev-A3⟩;
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

**SWBPIPE (SQ-17…SQ-19, answered 2026-09-28; R8-10).** SWBPIPE has no
workflow library, reader or declaration parser, and no host runs ("workflow"
in its product code means a user journey); its run records are solver
analysis records. The host columns above therefore have no SWBPIPE
counterpart now, and **OUT-003's round trip cannot complete against
SWBPIPE** until a SWBPIPE work item receives App workflows (ANS §4). This is
recorded; it decides nothing.

---

## 5. Owner and check allocation (OUT-001; AC-001, AC-008)

"Focused check" is the producing owner's own verification, in its file.
"Joined check" is the candidate-bound examination that joins contributions.

| Contribution | Producing owner | Focused check (designed) | Joined check owner | Standing now |
|---|---|---|---|---|
| Catalog and read basis (C) | DEL-03-01 | C VC-C-01…; M3-CP with P | DEL-09-07; DEL-09-09 | v0.6 draft (R8) |
| Proposal and outcomes (P) | DEL-03-02 | P VC-P-… | DEL-09-07; DEL-09-09 | v0.6 draft (R8) |
| Act policy (ACT) | DEL-04-01 | ACT FX-/VC- cases | DEL-09-06 (W14-04/05); DEL-09-09 (XC-09/10) | v0.6 draft (R8); D2/D3 adopted; §2.6 A13 capture; §4.6 hold support (governance phase under R8-1) |
| Grant display (AS) | DEL-04-02 | AS VC cases | DEL-09-07 (V4-EXM-22) | v0.6 draft (R8) |
| Records (RS) | DEL-04-03 | RS VC cases | DEL-09-06 (W14-05/07) | v0.6 draft (R8) |
| Loop receiving (LOOP) | DEL-05-01 (receiving); construction external | LOOP VC-01…09 | DEL-09-07 | v0.6 draft (R8): Phase 1 §2.4.0; host-loop hold governance phase |
| Panel receiving (PANEL) | DEL-05-02 (receiving); construction external | PANEL VC-01…07 | DEL-09-07 | v0.6 draft (R8) |
| Declaration (WD) | DEL-02-01 | WD §13 | DEL-09-06 (W14-01…03) | v0.6 draft (R8): Phase-1 guidance §4.3.0; optional `governed` flag (PROPOSED) |
| Execution compatibility, hold machine, transfer trace (EXEC) | DEL-02-03 | VC-E-01…13 | DEL-09-06 (W14-*) | v0.4 draft (R8): Phase 1 §2.1 (checkpoints are guidance); hold machine and §3.6 retained as the governance phase (§2.2); D6 closed for Phase 1 |
| External adapter (ADAPTER) | DEL-03-03 | VC-X-01…08 | DEL-09-09 | v0.4 draft (R8); native family only; no interposition adopted |
| Hosting boundary (HOSTING) | DEL-01-01 | HOSTING VC | DEL-09-06 (W14-08 App side) | v0.6 draft (R8); pin 0.158.0 (definition pin only) |
| Review, registration, drafts | DEL-02-02 | — | DEL-09-06 (W14-09) | **Not in this undertaking (D1)** |
| App act control | DEL-01-04 | — | — | **Not in this undertaking (D1)** |
| Examination infrastructure and protocol | DEL-09-01 | — | all examiners | **Not in this undertaking (D1)** |
| Local host qualification V4-EXM-20…23 | DEL-09-07 | — | DEL-09-07 | **Not in this undertaking (D1)** |
| External control; extension trace V4-EXM-24/25 | DEL-09-09 | — | DEL-09-09 | XT-v0.4 draft (R8) |
| **V4-EXM-14 joined round trip** | **DEL-09-06** | — | **DEL-09-06** | Designed (§8); not run |
| Host catalog, route, receipts, loop, panel, views, act facility, library, endpoint | SWBPIPE owner (DEP-001) | Host-owned checks (SQ-27) | Joined by DEL-09-06/07/09 | Owner-reported building before agent-action integration; SWBPIPE answers (2026-09-28): no live agent in the product (A-1); agent-facing work (UI-SUCCESSOR) deferred by the owner; draft PR #885 unmerged and deferred, with the owner's live-controller activation still in force (A-2). Answers received; no commitment or contribution; host joins deferred (DECISION-3) |
| Human acts A4, A5, A10, A12, A13 | The person (Engineer A in fixtures) | — | Observed, never performed, by examiners | None performed |
| OI-021, App v4 OI-003, U-03, D6 (SQ-02 answered: none; closed for Phase 1 by DECISION-4, re-opens with the governance phase); D5 decided; phased checkpoints (DECISION-4 D4-1) | The owner (with named co-owners) | — | — | Open, closed for Phase 1, or settled as stated |

---

## 6. Staging without PEC or Domains (REQ-006; AC-006)

| Stage | Content | Needs | Does not need | Output standing |
|---|---|---|---|---|
| **ST-0 Definitions** (now) | v0.3/v0.4 and v0.2 definitions; this contract; relay file; DEL-09-09 cases | Accepted basis | Any host input | *illustrative* |
| **ST-1 App-local executable fixtures** | C/P/ACT/RS/AS/WD/EXEC/ADAPTER fixture runs on test doubles; App run through stock Codex for the App side of the workflow | App construction (later undertaking); DEL-09-01 protocol | Host, OI-021 | *test-double* per file |
| **ST-2 Relay and answers** | `RELAY_QUESTIONS_SWBPIPE.md` relayed; answers recorded | The human; SWBPIPE session | PEC, Domains | Answers with custody; not delivery. Reached: answers received 2026-09-28 (RELAY §4) |
| **ST-3 Activity selection** | OI-021 decided; increment SoW finalized (DI-1…DI-3) | Owner; SQ-04/SQ-05 answers (received: no selection; candidates in DI-1) | PEC, Domains | Final increment SoW (future) |
| **ST-4 Host contributions and focused host examination** | Host candidate identified; CA/E (and/or CA/X) exercised; V4-EXM-20…23 by DEL-09-07; V4-EXM-25 by DEL-09-09 | DEP-001 contributions; SQ-01/SQ-02; SQ-28 for CA/X; person's acts | PEC, Domains | *actual host*, candidate-bound. **Phase 1:** checkpoints are guidance; results depend on required tools and the channel state. Against SWBPIPE the CA/X channel stays *not enabled* (no A13 facility, SQ-28) and there is no host loop for CA/E (SQ-20), so ST-4 cannot start against SWBPIPE as its answers stand; host joins are deferred (DECISION-3). **Governance phase (governed checkpoints):** on CA/X host-operation checkpoints are *not enforceable* (SQ-02 answered: none) and App-only checkpoints (including E1's `CP-check`) *not enforceable*, so every such workflow on CA/X is *unsupported* (S-13; EXEC-v0.4 MT-2) |
| **ST-5 Joined V4-EXM-14 round trip** | §8 witness on identified App and host candidates | ST-4 plus DEL-02-02 registration (later undertaking) | PEC, Domains | Completion evidence for OUT-003 (future) |
| **Later** | Domains research/design-candidate increment; PEC coordination | Their own contracts | — | Outside this activity |

Rules: ST-1 and independent App construction never wait for ST-4/ST-5
(REQ-006). A stage's output never claims a later stage. A first-host pass is
not evidence of longer-work recovery (DEL-09-05). Each stage that depends on
an input names it; a defined contract is not treated as an available input
(AC-006).

---

## 7. Evidence standing (REQ-005, REQ-007; AC-005, AC-007)

### 7.1 Examination evidence labels (C-v0.4 mapping, carried in C-v0.6; consumed)

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

SWBPIPE has no workflow library (SQ-17), so no host side of the V4-EXM-14
round trip exists until a SWBPIPE work item creates one (ANS §4). OUT-003
therefore cannot complete against SWBPIPE as its answers stand (R8-10), in
addition to F-1. Host joins are deferred (DECISION-3).

**Phase reading of the cases (R8-1).** In Phase 1 the checkpoint cases
(W14-03, W14-04, W14-06) are observed as **recording** cases: arrivals,
acts performed by the person, lapses, and the optional "continued past
‹checkpoint› before ‹act›" annotation. Nothing is held. Their hold parts are
the **governance-phase definition (retained)**, observed only for governed
checkpoints when that phase is taken up; the fixture's checkpoints are read
as if governed (EXEC-v0.4 GV-5; R8-11 item 5).

### 8.2 Cases

| Case | What is observed | Built on | Inputs still needed | State |
|---|---|---|---|---|
| **W14-00 Identification** | App candidate (build, stock Codex version actually used, model/server), host candidate (source revision, build, configuration), date, invented material identity | V4-EXM-01 | SQ-27 (a) (answered: SWBPIPE identifies contributions by commit and merge SHA, hosted CI run ids, the DEC-025 local sweep, T9 byte identity and native witness records with SHA256SUMS); App candidate (later undertaking) | AWAITING INPUT — SQ-27 answered 2026-09-28: an identification scheme, but no candidate identified; LIVE-HUMAN witness blocked and deferred; host joins deferred (DECISION-3) |
| **W14-01 Transfer App → host, unadapted** | exported → relayed → received links; origin *project* kept; holding library per link | EXEC RT-1, TR-1…TR-6 | SQ-17 (a), (d); DEL-02-02 registration (later) | AWAITING INPUT — SQ-17 answered 2026-09-28: no workflow library, reader or declaration parser (not offered); a work item to receive App workflows is a SWBPIPE owner decision (ANS §4); host joins deferred (DECISION-3) |
| **W14-02 Adaptation** | New host identity with derived-from; checkpoint comparison preserved/changed/removed/added; no identity or act inheritance | EXEC RT-2, RT-3, AD-1…AD-6 | SQ-18 (b), (c) | AWAITING INPUT — SQ-18 answered 2026-09-28: no host workflows, no adaptation (not offered); a SWBPIPE owner decision (ANS §4); host joins deferred (DECISION-3) |
| **W14-03 Required tools and unsupported capability** | Compatibility report on the host's actual edition (available tools **present**); one explicit unsupported/missing outcome observed and shown to the person, with no fabricated tool execution | EXEC-v0.4 MT-1, MT-2, MT-3, MT-10, MT-15, MT-16; TF-3/TF-4. The App-route values must match MT-2 and MT-16 in both parts. **Phase 1:** E1 and E1d via X pass on their required tools and the channel, with checkpoints listed as guidance; MT-15 stays *not established* for its unresolved harness-capability reference (U-08), a required-tool matter, not a hold (R8-11 item 3). **Governance phase:** E1 via X *unsupported* (`CP-accept` *not enforceable*, HS-3 (c); `CP-check`, HS-5) and E1d via X *unsupported* (`CP-grant` *not enforceable*, HS-3 (c); `CP-check`, HS-5) | SQ-11; SQ-17 (b), (c) | AWAITING INPUT — SQ-11 answered 2026-09-28: no exposure element, one entry on X (Node `position.x`), no E surface; SQ-17: no workflow library or declaration reader (not offered); SWBPIPE owner decisions (ANS §2, §4); host joins deferred (DECISION-3) |
| **W14-04 Checkpoint under direct autonomy** (hold parts: governance phase, retained) | **Phase 1 (recording; R8-1):** (i′) V-CP1 input: the agent, following I-7 as plan guidance, submits a separate proposal; if a direct request is made, the host's own treatment decides and the outcome is recorded as observed; nothing is reported *not permitted* on the constraint's account (EXEC-v0.4 CH-27 Phase 1; R8-11 item 2). (ii′) E1c `CP-check` after direct application under ⟨set-2⟩: the arrival on S-4 is recorded; neither the App nor the host loop holds the run; the A4 is recorded only when the person performs it (EXEC-v0.4 CH-1 Phase 1). (iii′) E1 as an App run on X: the check is decided by the required tools and the channel (MT-2 Phase 1); nothing is *unsupported* for a hold reason; later run actions may carry "continued past ‹checkpoint› before ‹act›" (PH-7). **Governance phase (governed checkpoints; the fixture's read as if governed):** (i) A5 `CP-accept` with a direct grant for the operation's class (V-CP1): direct request *not permitted* naming the constraint; separate proposal queued; waits for A5. This depends wholly on the host route (SQ-02 (a)–(c)); SWBPIPE answered (a) No, (c) No, so (i) has no SWBPIPE host route on X, and there is no SWBPIPE host loop on E (SQ-20); it is **not** App-side hold evidence (EXEC F-19). (ii) E1c `CP-check` after direct application under ⟨set-2⟩ (T15: class P-03, scope {FX-W1; {S-4}}; counts only because the A12 was **established**, S-14): run waits for A4 on S-4; nothing releases it without A4. Run it first on the host loop (CA/E). (iii) E1 as an App run on X (EXEC-v0.4 MT-2): `CP-accept` → *not enforceable* (HS-3 (c): SQ-02 answered); `CP-check` App-only (HS-5) → *not enforceable* → the workflow is **unsupported**; any run action while waiting recorded as *action during hold* (ADAPTER XF-42) | EXEC-v0.4 §2.1, CH-1, CH-27, MT-2, §3.6; WD I-7, §4.3.0; C V-CP1, T15–T16; ADAPTER XF-42 | (i) SQ-02 (answered: none); (ii) SQ-01, SQ-03; SQ-05 (answered: no grant states, so ⟨set-2⟩ has no SWBPIPE counterpart); the person's A12 and A4; (iii) none (values determined); D6 re-opens with the governance phase (EXEC U-E1, U-E23) | AWAITING INPUT — SQ-01, SQ-02, SQ-03, SQ-05 and SQ-20 answered 2026-09-28: no capture-evidence reference, no host-held route, whole-model identity only, no grants, no host loop (not offered); SWBPIPE owner decisions (ANS §2); host joins deferred (DECISION-3). (iii) shows the limit only |
| **W14-05 Real act, faithfully recorded; fabrication negatives** | In force in Phase 1 (PH-4). Engineer's actual A5/A10 (T11; on SWBPIPE only A5 exists, as Apply per batch, with no A10 record, R8-5) or A4 captured by the host facility **at or after the arrival** (S-14); App/loop record with actor ≠ recorder, bound content identity, capture-evidence reference. A4 captured before the arrival is shown "prior act not counted". App-side variant: A4 on App file AF-1 in the App act control (EXEC CH-23). Negatives: success, *queued*, receipt, A14, model text, user-input or elicitation answer (not act evidence, R4-12) → no act | EXEC CH-2, CH-20, CH-23, CH-28, CAP-6; WD-EX R-9; ADAPTER XF-31, XF-33; C AF-1 | SQ-01; an actual person performing the act on invented material (DEP-09-06-024); App act control (DEL-01-04, later) for the AF-1 variant | AWAITING INPUT — SQ-01 answered 2026-09-28: no capture-evidence reference; the Apply receipt names no person or time and does not survive restart, even in DRAFT #885 (not offered); PB-TBD-002 and DEL-16-03 are SWBPIPE owner decisions (ANS §2); host joins deferred (DECISION-3) |
| **W14-06 Content change after an act** | **Phase 1 (R8-11 item 1; PH-8):** edit to bound content → act-lapsed event recorded against the affected referents; label "waiting — lapsed at ‹t›" before the resume point, and **"act lapsed at ‹t›"** after it (nothing says *waiting*; R8-12 item 1), while the arrival's act is not yet re-performed; gated outputs (e.g. `checked-rows`) show standing *lapsed*; nothing re-holds; the agent asks again as its plan requires; history preserved. **Governance phase (retained; re-hold clauses):** Edit to bound content → act-lapsed event. Before the resume point: "waiting — lapsed at ‹t›". After the resume point: the **same** arrival is re-held, "waiting — re-held, lapsed at ‹t› after resume"; the run stops at its next action where hold support is *enforced by the host loop* (the host-loop case) — otherwise the held host operations are refused (*enforced on the host route*) or the action is recorded as *action during hold* (R6-3); nothing done is undone; gated outputs (e.g. `checked-rows`) show standing *lapsed*; the person is asked again for the whole scope (S-14). After run end: *lapsed* per referent. A5 and A12 never re-hold. A lapse caused by the person's own undo (T17 analogue) re-holds the same way; that undo is never recorded as *action during hold*, and it never re-holds an A5 arrival (R5-5). History preserved; no invented current act | EXEC-v0.4 CH-6, CH-7, CH-10, §4.7 RH-1…RH-9; T14, T16a–T17; R5-5 | SQ-03 (b) (answered: no per-object identity; the whole-model identity is received for every covered subject, so any model change lapses every bound act — over-lapse, never under, R8-4); host lapse display (SQ-23: answered, DESIGN only) | AWAITING INPUT — SQ-03 and SQ-23 answered 2026-09-28: no per-object identity, lapse wording DESIGN only (not offered); SWBPIPE owner decisions (ANS §2); host joins deferred (DECISION-3) (CH-8 (ii) HELD on U-03) |
| **W14-07 Interruption and replay** | Observation lost while waiting; recovery rebuilds dispositions from the record; recovered events not back-filled; held call dispatched unchanged; inspection replay issues nothing. Interruption is not run end; an ended run is never resumed — carrying work on is a new run *continues ⟨run⟩* that inherits nothing (S-14) | EXEC CH-3, CH-4, CH-5, CH-9, CH-21, RP-1…RP-8, §4.9 | SQ-09 (c); SQ-19 (c) | AWAITING INPUT — SQ-09 (c) answered 2026-09-28: no durable receipt, `outcome_unknown` resolvable only within the controller session; SQ-19 (c): no host loop or host runs (not offered); SWBPIPE owner decisions (ANS §2); host joins deferred (DECISION-3) |
| **W14-08 Supplied / adopted / observed** | App side: supplied guidance per thread/turn (HOSTING §8.2) and the model destination per turn where reported, requested and effective kept apart, run-level set of destinations observed (HOSTING §8.3; information only, S-12; R5-4); host side: per-turn guidance if recordable, else *unknown*; adoption *unknown*; observed behavior from run records | EXEC RT-5, CR-14 | SQ-19 (a), (b) | AWAITING INPUT — SQ-19 answered 2026-09-28: no host loop, no host run records or supplied guidance (not offered); the D-58 successor is a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3) |
| **W14-09 Host → App refinement usable in App** | Host revision relayed and held in LIB-A2 ⟨fx-app-import⟩, opened read-only, refined as a draft, registered in LIB-A1 with derived-from; a run of the refined identity starts with every checkpoint *not reached* and imports no act | EXEC RT-6, RT-8, HR-1…HR-7; C LIB-A1, LIB-A2 | SQ-18 (a); DEL-02-02 (later undertaking) | AWAITING INPUT (DEL-02-02) — SQ-18 (a) answered 2026-09-28: no host workflows (not offered); a SWBPIPE owner decision (ANS §4); host joins deferred (DECISION-3) |
| **W14-10 Revision and replay history** | Several revisions and a same-name collision shown with origins and holding libraries (⟨fx-root⟩, LIB-A1, LIB-A2); replay reads the resolved revision recorded for the run | EXEC RT-7, RP-5; WD-EX E4; C LIB-A1, LIB-A2 | SQ-18 (a) | AWAITING INPUT — SQ-18 (a) answered 2026-09-28: no host workflows (not offered); a SWBPIPE owner decision (ANS §4); host joins deferred (DECISION-3) |

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
| EC-01 | Capture-evidence references for host-captured acts | SWBPIPE owner | SQ-01 | Before positive checkpoint cases | **answered** 2026-09-28 (SQ-01: only Apply (A5) is captured; no capture-evidence reference; the receipt names no person or time and is session-only); not a commitment, delivery or adoption |
| EC-02 | Constraint receipt or host-held declaration | SWBPIPE owner | SQ-02 | Before V-CP1 family | **answered** 2026-09-28 (SQ-02: route (iv), none planned; a constraint field would be refused as unknown; governance-phase input (R8-2)); not a commitment, delivery or adoption |
| EC-03 | Subject/change-item identities; resulting objects | SWBPIPE owner | SQ-03 | Before binding/lapse cases on a host | **answered** 2026-09-28 (SQ-03: whole-model identity only; no per-row or per-object identity); not a commitment, delivery or adoption |
| EC-04 | Candidate operations, check and environment | SWBPIPE owner (input to OI-021) | SQ-04 | Before connected-activity SoW | **answered** 2026-09-28 (SQ-04: no selection (owner decision); candidates recorded in DI-1); not a commitment, delivery or adoption |
| EC-05 | Policy for the operation; host reserved list; adoption of treatments | SWBPIPE owner | SQ-05, SQ-06 | Before operation-policy production contracts | **answered** 2026-09-28 (SQ-05, SQ-06: no class system, grants or named reserved list; every change waits for Apply; a direct request over DRAFT #885 is refused `unsupported_method`); not a commitment, delivery or adoption |
| EC-06 | Basis, staleness, identity, outcomes, undo, exposure | SWBPIPE owner | SQ-07…SQ-11 | Before integrating an actionable host operation | **answered** 2026-09-28 (SQ-07…SQ-11: whole-model staleness; DRAFT #885 identity, de-duplication and `status` within one controller session; named outcome codes, with `outcome_unknown`; session undo without receipt; no exposure element); not a commitment, delivery or adoption |
| EC-07 | External seam, enablement behavior, origin, locality, host restriction by model destination | SWBPIPE owner | SQ-12…SQ-16 | Before CA/X live examination | **answered** 2026-09-28 (SQ-12…SQ-16: the CLI in DRAFT #885, hand-built, not MCP; opt-in is a launch environment variable plus a build feature; caller identity not verified; strictly local; no restriction by model destination); not a commitment, delivery or adoption |
| EC-08 | Workflow receiving, adaptation, run records, supplied guidance | SWBPIPE owner | SQ-17…SQ-20 | Before W14 host-side cases | **answered** 2026-09-28 (SQ-17…SQ-20: no workflow library, adaptation, host loop or host run records; placement not decided); not a commitment, delivery or adoption |
| EC-09 | Views, act display, findings, faithful-record operation, proxy capture | SWBPIPE owner | SQ-21…SQ-25 | Before panel receiving | **answered** 2026-09-28 (SQ-21…SQ-25: no faithful-record operation; host views show old/new values without stable external references; lapse display DESIGN only; findings not stored on main; acts through the host facility only, no proxy); not a commitment, delivery or adoption |
| EC-10 | One new operation for the extension trace | SWBPIPE owner | SQ-26 | Before any extension claim (DEL-09-09) | **answered** 2026-09-28 (SQ-26: not chosen; no catalog editions or edition-addition event); not a commitment, delivery or adoption |
| EC-11 | Identified candidates; host-owned checks and witnesses; relay form; actual engineer for joined witnesses | SWBPIPE owner; the person | SQ-27 | Before any candidate-bound result | **answered** 2026-09-28 (SQ-27: contributions identified by commit/merge SHA, CI run ids, DEC-025 sweep, T9 and witness records with SHA256SUMS; no relay form agreed; LIVE-HUMAN deferred; nothing needed from the App side); not a commitment, delivery or adoption |
| EC-13 | A13 enablement facility with capture-evidence reference | SWBPIPE owner | SQ-28 | Before any live CA/X case | **answered** 2026-09-28 (SQ-28: no facility exists or is planned; the channel stays *not enabled*); not a commitment, delivery or adoption |
| EC-14 | Embedded loop's model interface and fixture basis (DEP-05-01-024), endpoint/key boundary, malformed-call handling and validation order, responsiveness | SWBPIPE owner; App/shared embedded-integration owner receives or agrees the model interface | SQ-29…SQ-32 | Before loop fixtures and CA/E candidate observations | **answered** 2026-09-28 (SQ-29…SQ-32: no model interface, endpoint configuration, key custody or loop; engine strict preflight; the solve is a background job with poll and cancel); not a commitment, delivery or adoption |
| EC-12 | The OI-021 selection | Owner via outside SWB session with App/shared owner | — | Before connected-activity SoW | open |

"answered" means SWBPIPE's answer about its current state was received
(RELAY §4: relayed 2026-09-28, recorded from the owner's statement; answers
delivered in #1047, `RELAY_ANSWERS_SWBPIPE.md` sha256 `6f01add3…61c7`). It is
not a commitment, delivery, adoption or examination (§7.2), and items SWBPIPE
marks OWNER DECISION stay open (ANS §2). DEP-001 standing remains
*owner-reported building before agent-action integration*; SWBPIPE answers
(2026-09-28): no live agent in the product (A-1); agent-facing work
(UI-SUCCESSOR) deferred by the owner; draft PR #885 unmerged and **deferred**,
with the owner's live-controller activation still in force (A-2). Not
delivery, adoption or live readiness. Host joins are deferred (DECISION-3).

---

## 10. Excluded acts and their owners (REQ-008; AC-008)

| Excluded act | Owner | This contribution's part |
|---|---|---|
| Catalog, proposal, policy, grant display, record, loop, panel, declaration, execution-compatibility, adapter and hosting construction and focused checks | DEL-03-01, DEL-03-02, DEL-04-01, DEL-04-02, DEL-04-03, DEL-05-01, DEL-05-02, DEL-02-01, DEL-02-03, DEL-03-03, DEL-01-01 (CLM-003) | Joins their meanings in §2–§4; performs none |
| Review, registration, selection policy, drafts | DEL-02-02 (later, D1) | Named in W14-01/W14-09 |
| SWB domain objects, catalog, route, receipts, views, loop, panel, act facility, library, endpoint, host execution | External SWBPIPE owner (CLM-004; DEP-001) | Questions only (relay file) |
| OI-021 operation/autonomy/environment; App v4 OI-003 extension; U-03; D6 (SQ-02 answered: none; closed for Phase 1 by DECISION-4, re-opens with the governance phase); D5 (decided by the owner, DECISION-2); the governance phase itself (DECISION-4 D4-1) | The owner with named co-owners (CLM-005) | Open items recorded as open; decided items applied as decided; never decided here |
| Every human act (A4, A5, A6, A7, A10, A12, A13); professional reliance; engineering approval | The person; the accountable professional | Never performed, inferred or recorded without capture evidence |
| Standalone qualification; local host qualification; external control and extension examination; longer-work recovery; replacement packet | DEL-09-02; DEL-09-07; DEL-09-09; DEL-09-05; DEL-11-03 (CLM-006) | Coordinated through §5 and §6; not performed |
| Relay of files | The human | §4 ledger in the relay file |
| **Retained here** | **DEL-09-06**: the complete activity definition, its joining, and OUT-003 | — |

---

## 11. Interfaces

### 11.1 Expected from suppliers

| Supplier | Element | State |
|---|---|---|
| C, ACT | As cited per step in §2.3 | Cited at `8fb51f07f` (v0.4); V-GR1 from C-v0.5 (R5-7). Current: C-v0.6 and ACT-POLICY-v0.6 (R8-12 item 7) |
| P, AS, RS, LOOP, PANEL, WD, WD-EX, HOSTING | As cited per step in §2.3 | Cited at `8fb51f07f` (v0.4); R5/R6 meanings stated directly. WD and WD-EX read at v0.6 (`94aa9181b`) for §4.3.0, §4.3.1 and E1/E1c/E1d/E8; the others were revised in the same R8 pass and were not re-read by A5. Current: P, AS, RS, LOOP, PANEL, WD, WD-EX and HOSTING-BOUNDARY at v0.6 (R8-12 item 7) |
| EXEC | Compatibility report (Phase 1: checkpoints as guidance; governance phase: hold support); hold machine (governance phase, retained); transfer trace; RT fixture design; RT-11 evidence account mapped to W14 | EXEC-v0.4 at `94aa9181b` (§2.1, §2.2, §3.6, MT-2, MT-15, MT-16, CH-1, CH-27 read at this pass); RT-11 names DEL-09-06 as joined-witness owner. U-E24 closed in place by R8-11 item 2 (R8-12) |
| ADAPTER | Channel states; model destination; carriage assurance; XF inventory incl. XF-40…XF-42 | Cited at v0.2. Current: ADAPTER-v0.4 (R8-12 item 7; F-22…F-24 ruled by R8-12 items 4–6) |
| DEL-09-09 | V4-EXM-25 joined cases XC-*; extension trace | `EXTERNAL_TRACE_CASES.md` XT-v0.4 |
| DEL-09-07 | V4-EXM-20…23 on CA/E | Not in this undertaking |
| DEL-02-02 | Registration, drafts | Not in this undertaking |
| SWBPIPE owner | EC-01…EC-11, EC-13, EC-14 | Answers received 2026-09-28 (§9: *answered*); no commitment, contribution or adoption; host joins deferred (DECISION-3) |
| The owner | DI-1…DI-9 | Open, closed for Phase 1 (D6, DECISION-4) or settled (D5) |

### 11.2 Provided to receivers

| Receiver | Provided |
|---|---|
| DEL-09-07 | Step map §2.3 for CA/E; staging §6; evidence ladder §7 |
| DEL-09-09 | Step map for CA/X; W14-04/05 act cases shared with XC-09/10; relay file SQ-12…SQ-16, SQ-26, SQ-28 |
| DEL-02-03 | W14 case needs against RT/CH/MT cases; confirmation that RT-11 is received as an evidence account, not a witness |
| DEL-05-01, DEL-05-02, DEL-04-03 | Joined observation needs (W14-04…W14-08) |
| SWBPIPE owner (via the human) | `RELAY_QUESTIONS_SWBPIPE.md`; the note that SWBPIPE's embedded plan predates D-20 goes in `HANDOFF_SWBPIPE_DOMAINS.md` (R8-8; not edited here) |
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
| F-10 | **Amended by R5-1 and R5-10.** On X, host-operation checkpoints (E1's `CP-accept`) are *not established* until SQ-02 — the check does not pass; such a checkpoint alone does not make a workflow "unsupported"; App-only checkpoints are *not enforceable* and make a workflow *unsupported* whatever SWBPIPE answers. The owner-visible consequence is now two items: SQ-02 for host-operation checkpoints, and a separate D6 follow-up for App-only checkpoints |
| F-11 | Stands; R5-10 states that SQ-28 gates the whole external channel |
| F-12 | **Closed by R5-2**: a host loop's own evaluation is host-held |
| F-13 | **Closed by R5-4**: destination per turn where reported; run-level set; a switch starts no new run (S-12, W14-08) |
| F-14 | **Closed by R5-9**: all siblings cited at their `8fb51f07f` versions |

### 12.4 New findings at v0.3

| # | Where | Finding | Proposed disposition |
|---|---|---|---|
| F-15 | R5-1 with the first activity; EXEC-v0.3 §3.6 HS-5, MT-2, U-E23 | E1 (the proposed fixture workflow) is **unsupported** on X whatever SQ-02 returns: its `CP-check` arrives on the App agent's `examination-report` and holds the Return step, so it is App-only (HS-5) → *not enforceable*; only `CP-accept` is *not established*. The first connected activity's App-route expression therefore cannot pass its check with E1 as written. (Corrected in place from v0.3 as first issued, which said E1 on X was merely *not established*.) | Where a checkpoint must be enforceable on X, keep **every action it holds** on host operations (WR-11, R6-1); changing only its arrival (e.g. to the host outcome *applied (receipt)*) does not help while it still holds an App-side Return step. Route checkpoints with App-side held actions to the owner's D6 follow-up (EXEC U-E23) |
| F-16 | R5-7 V-GR1 | Under capture-after-arrival (PROPOSED), a person who set the grant just before the run reached `CP-grant` must set it again. This is a usability cost the owner should see with U-E4 | Owner decision on U-E4 |
| F-17 | R5 parallel bumps | Siblings move to v0.5/v0.3 in the same pass. This file states the R5 meanings directly, but its section citations are to the v0.4/v0.2 texts at `8fb51f07f` | Re-point at the next pass if any cited section moves |

### 12.5 R6 dispositions (in place)

| # | Disposition |
|---|---|
| F-15 | Remedy corrected by R6-1: held actions decide the value, so only moving a checkpoint's held actions onto host operations can make it enforceable from the App; E1c/E1d via X are unsupported too (§2.2) |
| F-17 | Partly closed: §5 and §11.1 status rows re-pointed to the current labels (Wave-1 v0.5, EXEC/ADAPTER v0.3). Body section citations still refer to the `8fb51f07f` texts; no cited section was found moved in the R6 check of EXEC §3.6 |

### 12.6 R8 dispositions (v0.4)

| # | Disposition |
|---|---|
| F-1 | Stands, with a second reason (R8-10; I2 Part 4.8): SWBPIPE has no workflow library, declaration reader or host runs (SQ-17…SQ-19), so OUT-003's round trip cannot complete against SWBPIPE until a SWBPIPE work item receives App workflows (ANS §4) |
| F-10 | **Phase 1 (R8-1):** moot. No checkpoint makes a workflow *unsupported*, so the CA/X expression is decided by its required tools and the channel state. **Governance phase:** SQ-02 was answered with no host-held route, so the v0.2 finding holds again for SWBPIPE: every governed checkpointed workflow is *unsupported* on the App/external surface. Its host-loop fallback (CA/E first) is not available against SWBPIPE either, which has no host loop (SQ-20; F-18) |
| F-11 | **Confirmed by SQ-28** (2026-09-28): no facility exists or is planned; the CA/X channel stays *not enabled* against SWBPIPE (R8-6). The owner question whether a person-set launch environment variable counts as A13 evidence is deferred (R8-Q4b) |
| F-15 | **Phase 1:** E1 on X is not *unsupported* for a hold reason (PH-3). **Governance phase:** as stated, now with `CP-accept` also *not enforceable* (SQ-02 answered; I2 P2.1). The WR-11 remedy (keep held actions on host operations) stands for a host that offers a host-held route; against SWBPIPE (route (iv)) no governed checkpoint is enforceable from the App on X (I2 P2.13) |
| F-16 | Stands: capture-after-arrival is a record rule that continues in Phase 1 (which recorded act answers which arrival), so the owner-visible cost stays with U-E4 |
| F-17 | **Status rows closed (R8-12 item 7).** §5 and §11.1 status rows and the §0, §3, §7.1 and VC-CA-02 body citations name the post-R8 versions; step citations in §2.3 still name the `8fb51f07f` texts and were not re-verified section by section against the post-R8 versions (the R6 check found no moved section) |

### 12.7 New findings at v0.4

| # | Where | Finding | Proposed disposition |
|---|---|---|---|
| F-18 | SQ-02 with SQ-20; I2 Part 4.6 | Against SWBPIPE as its answers stand, **no governed checkpoint could be examined as enforced on either surface**: X has no host-held route (route (iv)) and E has no host loop. In Phase 1 this blocks nothing, because checkpoints are guidance | Owner-facing consequence recorded with D6, for when the governance phase is taken up; a SWBPIPE decision to plan a route or a loop is a revision trigger |
| F-19 | SQ-03; R8-4 | SWBPIPE supplies only a whole-model identity, so V4-HI-32 (per-subject identity) is not met. Received as every covered subject's identity, it lapses every bound act on any model change (over-lapse, never under) | Owner notice; UNRESOLVED row (owner SWBPIPE: PB-TBD-002 / DEL-16-03) |
| F-20 | SQ-04 (c); DECISION-3; I2 Part 3 item 6 | SWBPIPE records name a development Codex controller over the CLI as the first caller, not the App's Codex. Every CA/X case depends on that naming (deferred by DECISION-3) as well as on an A13 facility (SQ-28) | Recorded; no new owner decision now |
| F-21 | SQ-01, SQ-09, SQ-10; R8-5 | SWBPIPE's Apply is acceptance and application in one step, per batch, with no A10 record; Clear discards without record; undo writes no receipt. W14-05's per-item A5/A10, the *partial* disposition of T11 and "reverses ⟨receipt⟩" have no SWBPIPE counterpart | App meanings kept; missing counterparts recorded (§2.4 reading note) |
| F-22 | DECISION-4 D4-1; R8-1; DEL-09-06 SoW REQ-003 ("A declared checkpoint waits for its required human act even under direct autonomy"), AC-004 ("holds a declared checkpoint …"), VER-004 | This SoW wording assumes the run waits at a checkpoint. Under R8-1 that is governance phase; in Phase 1 only the faithful-record half applies. W14-04 now designs both parts | Flag with V4-WF-05's first half for the next accepted-basis update (as EXEC F-29 does for DEL-02-03); no SoW text is changed here |

---

## Changes from v0.3

v0.3 = CA-v0.3 (sha256 67dde29553325271cc3e3a08591177e6628a659966b13b4bbd93920cdf7d0aa5, last changed at `c6f81a4f2`). R8 pass (A-wave, node A5) under R8_RESOLUTIONS.md at `94aa9181b`, following EXEC-v0.4 and WD/WD-EX-v0.6. Keyed by R8 ID; sources are I2 rows of INTAKE_MAP.md (`nn.k`, `P2.n`, Part 2.2, Part 3 and Part 4 items). R8 overrides I2 where they differ. SETTLED here means by DECISION-3 or DECISION-4.

| R8 ID (I2 source) | Change in v0.4 | Where |
|---|---|---|
| **R8-1** (DECISION-4 D4-1; SETTLED, framing INTEGRATION) | Phase 1 stated beside every hold passage: checkpoints are plan guidance; no App or host-loop hold; no *unsupported* for a hold reason; acts recorded only when the person performs them; reserved acts stand; arrivals and acts recorded as observation; "continued past ‹checkpoint› before ‹act›" replaces *action during hold* in Phase 1. The hold material (S-13 governance part, S-14 re-hold, §2.2 hold support, WR-11, W14-04, W14-06 hold clauses) is **relabelled governance phase (retained), not deleted**. WR-5 names the optional `governed` flag (WD-v0.6, PROPOSED). V4-WF-05's first half is phased, not withdrawn; SoW REQ-003/AC-004/VER-004 wording flagged (F-22) | Header, §0, S-5, S-13, S-14, §2.2, CA-0, CA-H, §2.4 note, WR-5, WR-11, ST-4, §8.1, W14-03, W14-04, W14-06, §12.7 F-22, VC-CA-02, VC-CA-04 |
| **R8-2** (P2.1, P2.4, P2.13, P2.16, P2.17; 02.14) | SQ-02's answer (route (iv), none planned) recorded as the **governance-phase input**: HS-3 (c) → *not enforceable* against SWBPIPE; `CP-accept` and `CP-grant` move from *not established* to *not enforceable*; E1, E1c, E1d via X stay *unsupported* in that phase, with reasons naming both checkpoints. HS-4 does not mask SWBPIPE entries (SQ-11 answered). Phase 1 changes no workflow result for hold reasons. D6 closed for Phase 1 and re-opens with the governance phase. The WR-11 advice is recorded as unavailable against SWBPIPE | S-13, §2.2, DI-6, WR-11, ST-4, W14-03, W14-04, §5 row, §10 row, §12.6 F-10/F-15, UNRESOLVED D6 row |
| **R8-3** (07.11; Part 3 item 2) | Staleness: per item where the host supplies subject identities; otherwise the host's stated scope is received and shown (SWBPIPE: whole model), never narrowed; de-duplication first unchanged | CA-4 (both cells) |
| **R8-4** (03.10; Part 3 item 3) | Whole-model identity received as every covered subject's identity (over-lapse, never under); never App-computed. SWBPIPE does not meet V4-HI-32: new F-19 and UNRESOLVED row (owner SWBPIPE) | CA-1, W14-06, §12.7 F-19, UNRESOLVED |
| **R8-5** (01.11, 08.7, 09.7, 10.6; Part 3 item 10; Part 4.9) | Outcome mapping recorded: Apply = accept and apply in one step per batch, no A10 record; #885 `withdrawn` = cleared by the person, no decision record; `validation_rejected` = *refused — invalid* at application; neither is A10 or A11; session undo writes no receipt, so "reverses ⟨receipt⟩" is *not supplied*. App meanings kept | CA-H, CA-5, CA-R, §2.4 note, W14-05, §12.7 F-21 |
| **R8-6** (28.3, 13.x; P2.18; Part 3 item 4) | SQ-28: no A13 facility, so the CA/X channel stays *not enabled* against SWBPIPE; A13 stays reserved; `controller_unavailable` reported as *endpoint unavailable*, channel *disabled*; host answering without evidenced A13 → evidence limit; R8-Q4b (launch environment variable as A13 evidence) deferred to the owner | §2.2 "Channel", CA-0, DI-9, ST-4, §12.6 F-11, UNRESOLVED |
| **R8-7** (X.1, X.4, 27.1, 27.2, 27.7; STD-1, STD-2, STD-5; Part 3 items 11, 12) | Standings move to **answered**: EC-01…EC-11, EC-13, EC-14 and VC-CA-05; consumed-inputs line; ST-2 reached; W14 states keep AWAITING INPUT with the STD-2 annotation. DEP-001 text follows STD-5, with PR #885 deferred and the owner's activation still in force. OI-003 qualified as "App v4 OI-003" | Header, §0, DI-8, §5, §9, §10, §11.1, W14-00…W14-10, UNRESOLVED, VC-CA-05 |
| **R8-8** (04.2, 20.5; DECISION-4 D4-2) | CA/E keeps the v4 loop (V4-ARC-10); note that SWBPIPE's embedded direction predates D-20 and is SWBPIPE's to update when UI-SUCCESSOR resumes; the HANDOFF note is routed, not edited here | §2.2 "SWBPIPE's current state", §11.2 |
| **R8-10** (04.1, 12.3, 17.4; Part 4.1, 4.7, 4.8; R8-Q12, R8-Q16) | OI-021 stays open, with the candidate operations recorded (DI-1). No capability catalog on SWBPIPE (WR-4 cannot resolve). No host workflow library: OUT-003's round trip cannot complete against SWBPIPE (§4, §8.1, F-1). Strict preflight: the agent never adds fields the host schema lacks (CA-2, WR-6). Grant display for a host without grants noted as PROPOSED (DI-2) | DI-1, DI-2, CA-2, WR-4, WR-6, §4, §8.1, §12.6 F-1, UNRESOLVED |
| **R8-11** (items 1, 2, 3, 5) | Lapse recording continues in Phase 1 and disposition words may label records; re-hold is governance phase only (S-14, W14-06). D2's reserved-act clause binds in Phase 1; its checkpoint half, I-7 and V4-HI-42 are guidance (S-5, WR-6, W14-04). An invalid checkpoint declaration is a declaration finding, not *not established*, in Phase 1; MT-15 stays *not established* for its harness-capability reference (WR-5, W14-03). Governance-phase values read the fixture's checkpoints as if governed (§2.2, §8.1) | S-5, S-14, WR-5, WR-6, §2.2, §8.1, W14-03, W14-04, W14-06 |
| DECISION-3 (host joins deferred) | Nothing claims a SWBPIPE join, witness or adoption; points of need for SWBPIPE owner decisions move to "when the owner resumes UI-SUCCESSOR"; the caller naming stays deferred (F-20); new F-18 records that no governed checkpoint could be examined as enforced against SWBPIPE on either surface | Header, §2.2, DI-3, DI-9, ST-4, §8.1, §12.7, UNRESOLVED |
| **R8-12** (items 1, 7; closing pass, node A6, in place) | Item 1: W14-06's Phase-1 lapse after the resume point is labelled **"act lapsed at ‹t›"** (nothing says *waiting*; nothing re-held); before resume "waiting — lapsed at ‹t›" stays. Item 7: consumed inputs list the post-R8 sibling versions (the R6-pass labels are marked superseded for currency); §5 standings, §11.1 states and §0/§3/§7.1/VC-CA-02 body citations name the post-R8 versions (earlier readings kept); F-17's R6 disposition is completed (§12.6) | Header, §0, §3.1, §3.2, §5, §7.1, §11.1, §12.6, W14-06, VC-CA-02 |

Identifiers kept. Added: §12.6, §12.7, F-18…F-22. No identifier retired.

---

## Changes from v0.2

v0.2 = CA-v0.2 (sha256 31ea3bff05865f425127009f90c070f26b97972e203b5a235791d00332d8dee1, committed at `9fc77baa3`). R5 pass under R5_RESOLUTIONS.md (commit `8fb51f07f`).

| R5 ID / source | Change |
|---|---|
| **R5-1** (V3-A MAJOR-1; V3-B MAJOR-5) | S-13, §2.2, WR-11, DI-6, ST-4, W14-04 (iii) and UNRESOLVED use the four ruled values: enforced by the host loop; enforced on the host route; not established; not enforceable. `CP-accept` on X is *not established* (awaiting SQ-02), not *unsupported*; App-only checkpoints are *not enforceable* |
| **R6-1** (V4-A MAJOR-1/2) — in place | §2.2 restated by held actions (host-held class vs App-side class, with the SQ-02 status mapping); E1c and E1d via X also unsupported, E1d's `CP-grant` alone not established (EXEC-v0.3 MT-16); S-13 reworded; WR-11 advice is now "keep a checkpoint's held actions on host operations if it must be enforceable from the App"; F-15 remedy corrected |
| **R6-4** (V4-A m-11) — in place | W14-03 cites MT-2 and MT-16 and requires matching values |
| **R6-5** (V4-B m-1, m-2) — in place | DI-5: only "flow, no gate" SETTLED; "record and show" INTEGRATION. S-13 and §2.2: model-supplied → *not enforceable* only once SQ-02 is answered with no host-held route |
| **R7-4 m-4** (V5 m-4) — in place | S-14 and W14-06: "the run stops at its next action" is qualified per R6-3. The run stops only where hold support is *enforced by the host loop*; otherwise the held host operations are refused (*enforced on the host route*) or the action is recorded as *action during hold*. W14-06 remains a host-loop-first case |
| **R7-3** (V5 MAJOR-3; INTEGRATION) — in place | §2.2 HS-5 bullet: the conservative default is scoped to a kind (b)/(c) checkpoint with no held-actions element, or whose declared held actions do not show host operations only; an A5 or kind (a) checkpoint without the element takes its derived held actions (WD §4.3.1; EXEC §3.6 HS-5). No value stated in CA changes |
| V4-B m-6, m-7, m-9 — in place | §5 and §11.1 status rows re-pointed (F-17 partly closed); header adds the R6 inputs; CA-H says "on E; in App runs only as hold support allows". In-place byte states of CA-v0.3: `3bf6653c9d23e01673f75b4f217e77cbe7df380645d5a65e9c1dc9674d37d1a4` at `d3cebd1cc`; `28a5cb8010e9c5e8445c397a5e3584a31ee850c390639c4fbce57b007fb14ce4` at `816c917f0`/`c7f5513db`; this R6 state is recorded by the coordinator at commit |
| **R5-1 (EXEC-v0.3 alignment)** — in-place fix, no version bump | Per EXEC-v0.3 (commit `d3cebd1cc`, sha256 889e48819baa21ec112c4878e4e38004dcbaa9eb3645a31c24221ac116ee548e) §3.5, §3.6 HS-5, MT-2 and U-E23: E1's `CP-check` in an App run is App-only → *not enforceable*, so **E1 via X is unsupported whatever SQ-02 returns**; `CP-accept` alone is *not established*. Corrected §2.2 (new paragraph), ST-4, W14-04 (iii), DI-6, UNRESOLVED D6 row, F-10 disposition and F-15 (which had said E1 on X was merely *not established*). WR-11's recommendation (keep checkpoints on host operations) is kept; App-only checkpoints route to the owner's D6 follow-up (EXEC U-E23). The R5-1 row above is superseded on this point |
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
| `UNRESOLVED{OI-021}` operation(s), non-mutating check, autonomy, environment, acting-surface variant (DI-1…DI-3) | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution | Draft contract only; FX-PIPE-01 proposed fixture; OP-C11-dependent production HELD. Stays open (R8-10); SQ-04 answered with no selection; candidate operations recorded in DI-1 |
| Operation-specific reserved additions (OI-021 residue of OI-001) | Same owners; host names its list (V4-HI-30) | Before operation-policy production contracts | D2 applied to App/shared contracts only |
| Host adoption of D2/D3 and treatments (DEP-001) | SWBPIPE owner; its autonomy is SWBPIPE owner decision OI-016 (ANS §2) | Before any enforcement claim | Treatment behavior is receiving meaning. SWBPIPE (SQ-05): no class system, grants or named reserved list; every change waits for Apply |
| DEP-001 contributions EC-01…EC-11, EC-13, EC-14 | SWBPIPE owner via the human. Answers received 2026-09-28 (§9 *answered*). What remains are SWBPIPE owner decisions (ANS §2): UI-SUCCESSOR and the App's Codex as a caller, OI-016 autonomy, the durable receipt carrier, PB-TBD-002 / DEL-16-03, the Checked-mark tranche, an MCP adapter, the D-58 successor, DEC-051, a host-held checkpoint route, an A13 facility; and a work item to receive App workflows (ANS §4) | when the owner resumes UI-SUCCESSOR (DECISION-3); then per §9 | All W14 cases AWAITING INPUT, with the STD-2 annotation; host joins deferred (DECISION-3) |
| Actual human acts for W14-04/05/06 (DEP-09-06-024) | The person performing them | At witness execution | Positive cases defined only |
| `UNRESOLVED{D6}` App-side run holds | Owner (DECISION-2 D6; DECISION-4 D4-1). SWBPIPE answered SQ-02 on 2026-09-28: route (iv), none planned. **Closed for Phase 1** by DECISION-4; re-opens only when the governance phase is taken up (R8-2; EXEC U-E1, U-E23); DEL-02-03 computes hold support | When the governance phase is taken up for a workflow that needs it; before App-side checkpoint enforcement is claimed | Phase 1: none (checkpoints are guidance; no *unsupported* for a hold reason). Governance phase: on X, host-operation checkpoints *not enforceable* (HS-3 (c)) and App-only checkpoints *not enforceable* (HS-5), so E1 on X is *unsupported* (EXEC-v0.4 MT-2); the host-loop fallback (F-10) has no SWBPIPE counterpart (SQ-20; F-18) |
| Host A13 enablement facility with capture-evidence reference | SWBPIPE owner decision (A13 enablement facility; ANS §2). SQ-28 answered: none exists or is planned | when the owner resumes UI-SUCCESSOR (DECISION-3); before any live CA/X case | CA/X channel stays *not enabled* (F-11; R8-6) |
| Whether a launch environment variable the person sets counts as A13 evidence (R8-Q4b) | Owner, deferred (R8-6) | When UI-SUCCESSOR resumes | None now; A13 is never evidenced on SWBPIPE meanwhile |
| Capture-after-arrival rule (R4-5, PROPOSED) versus counting prior acts (EXEC U-E4) | Owner | Before hold-machine fixtures run | W14-05 applies capture-after-arrival; for A12 the cost is shown by C V-GR1 (a repeated grant change whose content is already in force, R5-7) |
| U-03 multi-row A4 purpose after partial lapse | DEL-04-01 with the owner | Before re-hold/lapse fixtures run | W14-06 partial-lapse variant HELD |
| DEL-02-02 registration (later undertaking, D1) | DEL-02-02 owner | Before W14-01/W14-09 | OUT-003 cannot complete in this undertaking (F-1); nor against SWBPIPE, which has no workflow library (SQ-17; R8-10) |
| Per-subject content identity (V4-HI-32) not met by SWBPIPE, which supplies only a whole-model identity (R8-4; F-19) | SWBPIPE (PB-TBD-002 / DEL-16-03); owner notice | Before host act-binding integration | Whole-model identity received for every covered subject; over-lapse, never under |
| V4-WF-05's first half and DEL-09-06 SoW REQ-003 / AC-004 / VER-004 hold wording, phased to the governance layer (R8-1; F-22) | Owner, at the next accepted-basis update | Next accepted-basis update | Phase 1 cases designed as recording cases; hold parts retained as governance phase |
| Host joins deferred: DEL-09-06 joined witness, SWBPIPE-side examination, naming the App's Codex as a caller (DECISION-3; F-20) | Owner | when the owner resumes UI-SUCCESSOR (DECISION-3) | Nothing here claims a join, witness or adoption |
| DEL-09-01 evidence protocol; DEL-09-07 local qualification (outside D1) | Their owners | Before candidate-bound results | Labels per C mapping only |
| `UNRESOLVED{OI-013}` / `UNRESOLVED{OI-014}` placement | Shared contract owner with SWB implementation owner; App/shared owners | Before implementation boundary contracts | No placement implied |
| `UNRESOLVED{OI-003}` extension promise (App v4 OI-003; unrelated to SWBPIPE's own OI-003, SQ-26) | Owner with host contract owner | Before extension claim | Not part of the first activity; DEL-09-09 |
| Reusable workflow authoring and review (OUT-002 artifact) | Workflow maker with DEL-02-02 (later) under `create-workflow` | Before W14-01 | §3 requirements only; WF-1 fixture |

Closed at v0.4: "Host restriction of its own channel by model destination" (SWBPIPE owner, SQ-16): answered 2026-09-28, no restriction; the App need state nothing (DI-5).

## Verification cases

Designed, **not run**. Passing them later shows definition completeness only;
the witness itself is §8.

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-CA-01 Scope and activity coverage | Trace §2.1–§2.3 against the DEL-09-06 row, SOW-040/041/236/237/238/240/241, OBJ-001/004/008 and decision 05 | Four user activities, two named expressions and all five activity steps (plus frame steps) mapped to contributions, owners and checks; OI-021 shown open, no final operation-specific SoW claimed | VER-001 (AC-001) |
| VC-CA-02 Workflow requirements | Check §3 against V4-WF-01…06, WD-v0.6 (§4.3.0, §4.3.1; checkpoint vocabulary as at WD-v0.4) and WD-EX-v0.6 E1 (OP-C12 step); check WR-5, WR-6 and WR-11 in both phases | Identity, assumptions, inputs/tools, checkpoints, outputs/evidence, revision history required; incompatible/missing tools and checkpoints treated explicitly; checkpoints are plan guidance in Phase 1, with hold support stated only for governed checkpoints in the governance phase (WD-v0.6 §4.3.0; R8-1); no workflow claimed authored | VER-002 (AC-002) |
| VC-CA-03 Round trip design | Check §4 and §8 against V4-EXM-14 and EXEC §6 | Every link separate; original and revised identities kept apart; W14-00…W14-10 cover transfer, adaptation, tools, checkpoints, interruption, revision/replay, supplied/adopted/observed | VER-003 (AC-003) — design only |
| VC-CA-04 Act distinctions | Check W14-04/05/06/07 and §2.3 CA-H against V4-HI-25/31/32/42, D2, R-5, R2-20, R4-2…R4-6, DECISION-2, DECISION-4 D4-1 and R8-1/R8-11 | Phase 1: no hold and no *unsupported* for a hold reason; arrivals, performed acts and lapses recorded; "continued past ‹checkpoint› before ‹act›" only as an optional annotation. Governance phase (retained): hold under direct autonomy on the host loop, with no App hold claimed on X (unsupported, action during hold recorded); re-hold wording, no resumption, capture after arrival, A12 counted only when established; faithful record with actor ≠ recorder and capture evidence; fabrication negatives; lapse preserves history; no always-reserved list created; no favorable decision required | VER-004 (AC-004) |
| VC-CA-05 External account | Check §9 and the relay file against DEP-001, OI-021 and REQ-005 | Every external item has owner, point of need and a single standing; nothing beyond *answered*; no commitment, delivery or adoption; custody unknown shown | VER-005 (AC-005) |
| VC-CA-06 Staging | Check §6 against decision 05, PRD §2.3/§3.1/§8 and CLM-006 | No PEC/Domains prerequisite; ST-1 independent; each stage names its inputs; no stage claims a later one | VER-006 (AC-006) |
| VC-CA-07 Evidence standing | Check §7 and §8.1/§8.3 against EXAMINATION §1–2 | Candidate/configuration/date required; replay, test double and component passes cannot complete OUT-003 | VER-007 (AC-007) |
| VC-CA-08 Ownership | Check §5 and §10 one-for-one against REQ-008 and CLM-002…006 | Every excluded act has its owner; DEL-09-06 keeps joining and OUT-003; no policy decided; no shared construction assumed; no acceptance, release, replacement or reliance claimed | VER-008 (AC-008) |
