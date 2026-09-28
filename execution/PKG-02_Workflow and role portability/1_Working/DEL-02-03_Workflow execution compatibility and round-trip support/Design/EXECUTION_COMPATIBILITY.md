# Workflow execution compatibility, checkpoint hold and round trip
- Contribution: DEL-02-03/EXEC-v0.4 (supersedes DEL-02-03/EXEC-v0.3, last changed at `c6f81a4f2` and unchanged at `bcc25624d`, file sha256 03b2fd48e14dd21ee6f29bc8e5e19221a771f788aa6c1482810b8bc0671d61e2; EXEC-v0.2 at `cc58211c5`, sha256 7f7848c0de2fdb4dc21f5adafa97f92e179bb66c9f6b04f3434d8f2342317af0; EXEC-v0.1 at `e20a3ae8d`, sha256 e0ede76ebf08003511755afc666be2466a867fd3256837ee94300cd0dfe518e8)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001 (required-tool check and checkpoint receiving behavior — definition only, no code), OUT-002 (App/host transfer and adaptation contract), OUT-003 (missing-tool, checkpoint and round-trip fixture design — none run); REQ-001…REQ-007; AC-001…AC-007 through designed VER-001…VER-007
- Phase (R8-1): in Phase 1 (this increment) declared checkpoints are **plan guidance** (§2.1). The hold machine and hold support are kept as the **governance-phase definition (retained)** (§2.2). V4-WF-05's first half is **phased to the governance layer, not withdrawn**, and is flagged for the next accepted-basis update.
- Basis: repo 6e18505e3 (accepted basis); ScopeOfWork.md sha256 9a921ba500271c441e64db2e1f34acf41c95fa7821d6dff3d8659352bb4db7fb; `P/docs/PRD.md` V4-WF-01…06, V4-AUT-03, V4-AUT-05, V4-EXE-01, V4-EXE-03, V4-REC-03, V4-REC-05; `P/docs/HOST_INTEGRATION.md` V4-HI-02, -04, -23, -25, -30…32, -40…42, -50…52, -70/71; `P/docs/EXAMINATION.md` V4-EXM-14, V4-EXM-22; `P/docs/ARCHITECTURE.md` V4-ARC-20/21; SCC-CASE-002 `Case_Datasheet.md` sha256 6acdc6c4e484ab7b46ba7d45a347961bc69b3e624bd29ef58a613ec6c66a71a6 (M1 rows naming DEL-02-03 as producer and receiver); owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (OWNER_DECISIONS.md sha256 f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e) D1–D4; owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (OWNER_DECISIONS.md at `f05c7e4cd`, sha256 a9869129…8ad2c) D5, D6; owner decisions `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3` and `-DECISION-4` with its clarification (OWNER_DECISIONS.md at `bcc25624d`, sha256 a5ccab0d39bd1cab37c5556abc9bdedd5341ce76be4712706c8c9d72d623e776): host joins deferred (D3); D4-1 phased checkpoints
- Consumed inputs:
  - **v0.4 inputs (R8 pass, node A1, at `bcc25624d`).** R8_RESOLUTIONS.md sha256 9877da0759409776ff3ac5d77cd20efb2edd9f513bdba8ce39564f650e561234 (R8-1…R8-10; binding). INTAKE_MAP.md (I2) sha256 3cc182955c0f3dd70efa0f1c051870229c2ccc08f36c5cf1445f2eef0dd1ea33: rows 01.2, 01.14, 02.1–02.3, 03.6, 11.3, 17.1, 18.1, 19.2, 20.3, 25.1, X.4, X.5; Part 2 P2.1, P2.4, P2.12, P2.13, P2.16, P2.17 and its §2.2 EXEC rows; Part 4.11. R8 overrides I2 where they differ. BRIEFS.md sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517 ("Common rules", "A-wave"). SWBPIPE's delivered answers `RELAY_ANSWERS_SWBPIPE.md` (DEL-09-06 `Design/`, #1047) sha256 6f01add3977761e42ac6b310faf72ba4fd5455e478605deb83fefb2e4d3a61c7: SQ-01, SQ-02, SQ-03, SQ-07, SQ-11, SQ-17…SQ-20, SQ-25, ANS §2–§4. These are data about SWBPIPE's current state, not commitments (DECISION-3). Sibling to follow this file in the same pass: WD-v0.6 and WD-EX-v0.6 (DEL-02-01; the `governed` flag, PROPOSED).
  - **Integration rulings.** R1_RESOLUTIONS.md sha256 2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4 (R-1…R-10); R2_RESOLUTIONS.md sha256 77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088 (R2-1…R2-21); R3_RESOLUTIONS.md sha256 202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf (R3-1…R3-4). Brief: BRIEFS.md (working copy, sha256 58de4a2c48f651391383aecf85fa5e9073d2cc34240c37cdab216a16481c698f) "Common brief", "Owner rulings now in force", "Wave 2 — common additions", "W7".
  - **v0.1 basis (historical; superseded for citation by the v0.3 block below). Wave-1 v0.3 files at commit `ba0b37123`** (read with `git show`):
    - DEL-02-01/WD-v0.3 `WORKFLOW_DECLARATION.md` sha256 84841d9f539767b9ff7ae225fec27f0dc4ebbd2c161c41aff179bbae97f345eb (§3.4, §4.2, §4.3, §4.4, §4.6, §4.7, §6, §11, §12);
    - DEL-02-01/WD-EX-v0.3 `EXAMPLES.md` sha256 0f1058d7f0990e766b3effc3d3de24fc16383197874cced1f5b4212419cf018d (E1–E7, L-WDEX-1…15);
    - DEL-03-01/C-v0.3 `CATALOG_AND_READ_BASIS.md` sha256 ba45e7393ee0b16780f36605ddeecb95ba1f181488e36a46b4b495b69fd67c26 (§2, §3, §3.1, §3.2, §4, §5.3, §5.4, §10 FX-PIPE-01);
    - DEL-03-02/P-v0.3 `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` sha256 ec0db87f239bc42e2e3e953d660ce3c4ceddf605d7b98cf1393f97a099b699cf (§3.1, §3.3, §4.1–§4.5, §5, §9, §10, §13);
    - DEL-04-01/ACT-POLICY-v0.3 `ACT_AND_POLICY_CONTRACT.md` sha256 b3748c02006f939d8cc78c6e0b0c847598a8b32d55515ae8658ad80597c98128 (§2.1–§2.5, §4, §5.4–§5.6, §12);
    - DEL-04-02/AS-v0.3 `AUTONOMY_AND_STANDING_EXCHANGE.md` sha256 7b634137bb8402f3eaedc943dab0c5f1114b9d4433d2b94e13540ac0bf8e0514 (§4 checkpoint indicator; U-09, U-11, U-13, U-14);
    - DEL-04-03/RS-v0.3 `RECORD_SEMANTICS.md` sha256 925f35ca27bd7d1e71a375883ada9903267408af57312eed1ae02b47776a3528 (§3, §4 R2/R3/R8/R9/R11/R13, §5, §6, §7 L-0…L-12, §10);
    - DEL-05-01/LOOP-v0.3 `LOOP_RECEIVING_CONTRACT.md` sha256 6b771c8027787193d536fa3507214a8cc579d6ec2f476ee880609c920b6f25c7 (§2.1, §2.3, §2.4, §6.3, §11 FX-C1…C13, §13);
    - DEL-05-02/PANEL-v0.3 `PANEL_RECEIVING_CONTRACT.md` sha256 4c47764d3af434c23e63dcc2c10d28f18a4a94546d63d452855c471cfe47bee9 (§3.2, W-5a…W-5g, PC-20…PC-29);
    - DEL-01-01/HOSTING-BOUNDARY-v0.3 `HOSTING_BOUNDARY.md` sha256 34c3383402aabe6e9347aa2f111318538c4a2a4ca85adb8fffff7e439fdde94e (§6.1 request kinds, R9, §8, §8.2); generated `json-schema/experimental/codex_app_server_protocol.v2.schemas.json` sha256 34f28a486d00fbd20e5da0b0da3422d1d6e20ec897d12b31408f87499198f458 (presence of `turn/interrupt` only).
  - DEL-02-02, DEL-01-04, DEL-02-04: accepted SoWs only (later undertaking, D1). SWBPIPE answers received 2026-09-28 (RELAY_ANSWERS_SWBPIPE.md; I2 read `64ea4e59…0689`, delivered bytes `6f01add3…61c7`, which add clarifications only, R8 delta check); no host evidence, commitment or contribution received (DEP-001).
  - **v0.2 inputs (sweep A1).**
    - R4_RESOLUTIONS.md at commit `f05c7e4cd`, sha256 50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24 (R4-1…R4-21; binding).
    - OWNER_DECISIONS.md at `f05c7e4cd`, sha256 a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c: `APP-V4-FIRST-INCREMENT-20260928-DECISION-2`, D5 (user flexibility on model destination) and D6 (App hold deferred to SWBPIPE SQ-02).
    - DEL-09-06 at commit `b4030fe4b`: CA-v0.1 `CONNECTED_ACTIVITY_CONTRACT.md` sha256 685349b25981ca8333929207890514120d63753cdedd67ae0bad986fc5d45e62 (W14-00…W14-10, DI-7); RELAY-v0.1 `RELAY_QUESTIONS_SWBPIPE.md` sha256 3e34575def8d1fef63b5f5e64f0f90a0984d03b8b42f61fe899dd2eab023b2d1 (SQ-01…SQ-27; §3 map of EXEC host items).
    - DEL-03-03/ADAPTER-v0.1 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` at `e20a3ae8d`, sha256 58b2409ca45ceea66160eb8910ca38b76b6f335dc184eaeb0896e93cabd0a074 (§5.1–§5.3 carriage assurance and GC-1…GC-5; §7.7; OC-11; U-X3; XF-25, XF-26).
    - (Historical at v0.2: C and the Wave-1 files were then unchanged from v0.3. Superseded by the v0.3 block.)
  - **v0.3 inputs (R5 pass).**
    - R5_RESOLUTIONS.md at commit `8fb51f07f`, sha256 254d0b93b9959419a70c6737b07087e1db59b529adc3105a1db31f82b78dd6f1 (R5-1…R5-10; binding). Reviews: `reviews/V3-A.md` sha256 f25f5af1177b7fe2a698bd4ef1e1caafa4c2ef25cfc73111f031e17c7cc21d87 (MAJOR-1, -3, -4; m-1, m-3, m-9, m-10, m-11, m-12; Y-3, Y-4); `reviews/V3-B.md` sha256 5662fbd09025f5ad9459861370159d606fcced76b394980199e861555a1954a3 (MAJOR-1, -4, -5; notes for V3-A's side).
    - Integrator rulings relayed by the coordinator during the pass (INTEGRATION): (a) HP-4 scope, from HOSTING-v0.5 F-22; (b) multi-checkpoint precedence and the App-only definition, from WD-v0.5 §4.3.8 / WD-EX E8.
    - **Sibling set at commit `8fb51f07f`** (working tree identical when read): WD-v0.4 `WORKFLOW_DECLARATION.md` e492ff63…d8e88e; WD-EX-v0.4 `EXAMPLES.md` 60ce307a…3128ca4 (E1–E8, E2 runs, local cases cited by content); C-v0.4 `CATALOG_AND_READ_BASIS.md` e929d39d…c659a08c (§10.1 LIB-A1, LIB-A2, AF-1, FXA-1…FXA-5; §10.4 variants incl. V-ED1); P-v0.4 0d3960a2…c5e361; ACT-POLICY-v0.4 d6da05ab…369b03b; AS-v0.4 774728d0…1f4dab; RS-v0.4 56806b64…540199; LOOP-v0.4 ffc30483…2f95934e (§2.4.4, §6.2); PANEL-v0.4 cb71bc4b…4c84419; HOSTING-v0.4 201ea320…934c7e58 (§8.3), with HOSTING-v0.5 in the working tree (sha256 873e76f693975242893f74d4243b01a48cab54a91f434fb01e37ec70fb5b0eaa; F-22, U-25 only); ADAPTER-v0.2 a2905dda…a25674bc; DEL-09-06 CA-v0.2 31ea3bff…32d8dee1 (W14-00…W14-10) and RELAY-v0.2 48dc5a1f…2541f65 (SQ-01…SQ-32).
    - **R6 micro-pass (in place, no version bump):** R6_RESOLUTIONS.md sha256 8703e85aa7324e233fab285321e277d720923d3e36e342c865917b55083cb841 (R6-1, R6-4); `reviews/V4-A.md` sha256 121deafc40c4baf0dec71f96eb449083b0d93456c2bd448f89a279951ca2eab1 (MAJOR-1, MAJOR-2; m-1, m-2, m-8). Working tree: C-v0.5 `CATALOG_AND_READ_BASIS.md` sha256 298e425804a04675346d9c3e445a0aab19bc462a75ba8d4f6f55005fca8d2364 (§10.4 **V-GR1** with GR-1…GR-3, GR-P, GR-R, GR-S); WD-EX-v0.5 `EXAMPLES.md` sha256 296875c9aba92be6a3ef86c3ce9d658a9b6ba1d102db71a12f5f0c5c44a4702f (E1c, E1d, E8). (That WD-EX hash is the pre-R6 byte state; the R6 held-actions text quoted in §3.6 is in WD-EX at `b1b7f10e…3362`, below — R7-4 m-8.)
    - **R7 repair (in place, no version bump):** R7_RESOLUTIONS.md (R7-3; R7-4 m-5, m-6, m-8) and `reviews/V5.md` (MAJOR-3; m-5, m-6, m-8). Sibling inputs read at the R7 working state: first at candidate `2f42fba02` — WD-v0.5 `WORKFLOW_DECLARATION.md` 51f4c9fd…6daa (§4.3.1 held actions, §4.3.8); WD-EX-v0.5 `EXAMPLES.md` b1b7f10e…3362 (E1, E1c, E1d, E8); C-v0.5 `CATALOG_AND_READ_BASIS.md` 298e4258…2364 (V-GR1); ADAPTER-v0.3 977d6a26…1f44 (GC-3, GC-5); GUIDE-v0.2 6afc3b90…e3a7 (§2.13, §2.14) — then with the R7 edits made in place to WD, WD-EX, C and ADAPTER in the same repair, each recorded in that file's R7 rows. The post-R7 bytes of every Design file are pinned in GUIDE's input table (R7-4 m-1).
- Receivers: DEL-03-03 (hold-support values for ADAPTER GC-3/GC-5, §3.6, governance phase); DEL-02-01 (WD confirmations and amendments requested in §11; the §2.1 Phase-1 statement and §2.2 `governed` opt-in; CASE-002 M1 workflow-contract row); DEL-05-01 (Phase 1: no host-loop hold, §2.1 PH-2; governance phase: hold-machine semantics for host loops; CASE-002 M1 execution-owner row, OUT-001/OUT-003, REQ-007, VER-008); DEL-04-03 (R8 checkpoint events and transfer records; RS §10 DEL-02-03 row; RS U-17/U-18/U-22/U-23/U-24); DEL-09-06 (local transfer/adaptation evidence account, DEP-02-03-014; VER-004/VER-007). Named but outside this undertaking (D1): DEL-02-02 (CASE-002 M1 workspace row, changed-draft return, VER-004/VER-005 of DEL-02-02). Also read by DEL-05-02 and DEL-04-02 for display of the resolved W7 items.

---

## Changes from v0.3

Keyed by R8 ID; sources are I2 rows of INTAKE_MAP.md (`nn.k`, `P2.n`, Part 2.2 and
Part 4.11 rows). R8 overrides I2 where they differ. SETTLED here means by
DECISION-3 or DECISION-4.

| R8 ID (source) | Change in v0.4 | Where |
|---|---|---|
| **R8-1** (DECISION-4 D4-1; SETTLED, framing INTEGRATION) | New **§2.1 Phase 1** stated normatively (PH-1…PH-10). Checkpoints are plan guidance, and agents manage their own pauses. Neither the App nor a host's embedded loop enforces a hold, blocks a run or reports *unsupported* for a hold reason. The required-tool check (V4-WF-04) is unchanged. Acts are recorded only when the person performs them. Reserved acts stand (DECISION-1 D2; V4-HI-30). Arrival and act may be recorded as observation. *Action during hold* becomes the optional annotation "continued past ‹checkpoint› before ‹act›" (PH-7) | §0, §1 E-B, §2.1 |
| **R8-1** (governance phase retained) | New **§2.2**. The enforcement boundary (now §2.3), the hold-support clauses of §3.5, §3.6 (four values; HS-1…HS-5 as amended by R6-1, R7-3, R8-2), the §4 hold machine (holding, re-hold, held calls), R2-12 carriage assurance and the R4-8 reason are **relabelled governance phase (retained)**. Nothing is deleted. The opt-in is a checkpoint declared **`governed`** (WD-v0.6 §4.3.1, PROPOSED): Phase 1 honours it as guidance only, and the governance phase enforces it | §2.2, §2.3, §3.5, §3.6, §3.7 CC-3, §4 phase note, HD-4, §4.7, §4.10 AR-2, §4.12 RP-4/RP-5, §4.14 |
| **R8-1** (V4-WF-05) | V4-WF-05's first half ("holds … the run waits") is **phased to the governance layer, not withdrawn**. The second half is in force (PH-4). Flagged for the next accepted-basis update, as are SoW REQ-002/AC-002 wording (new F-29) | Header, §1 E-B, §2.1 PH-10, §4.7, §11.4 |
| **R8-1** (report) | CR-8 and CR-9: in Phase 1 no hold-support value is assigned, and the checkpoints are listed as guidance. In the governance phase the values apply per governed checkpoint. §3.5's result table gives the Phase-1 rule, with the hold-support clauses marked governance phase. An invalid or not-established checkpoint declaration is reported but, in Phase 1, does not change the result (R8-2) | §3.3, §3.5, §4.14, CH-26, CH-29 |
| **R8-1** (cases) | Every MT and CH case now gives a **Phase-1 result** and a **governance-phase value** (checkpoints read as if declared governed; no fixture declares the flag). New VC-E-13 (Phase-1 semantics); VC-E-02 and VC-E-12 are two-part | §7.1, §7.2, Verification cases |
| **R8-2** (I2 R8-Q1, P2.1, P2.4, P2.12, P2.16) | SQ-02's answer "route (iv), none planned" is recorded as the **governance-phase input**. Under the retained rules HS-3 (c) → *not enforceable* against SWBPIPE. The "(today)" marker leaves HS-3 (b), and a "current state (SWBPIPE): (c)" line is added. Fixture classification, Consequences, MT-2, MT-16 and CH-27 are recomputed for the governance phase: `CP-accept` and `CP-grant` are now *not enforceable*; results stay *unsupported*, with the reasons naming both checkpoints. A later SWBPIPE decision to plan a route is a revision trigger | §3.6, MT-2, MT-16, CH-27 |
| **R8-2** (I2 R8-Q-HS4) | HS-4 no longer masks SWBPIPE entries. SQ-11 is answered (no exposure element), so once SQ-02 is answered with no host-held route, HS-3 (c) decides regardless of exposure. The value-table rows note that against SWBPIPE neither cause of *not established* now applies (this overrides I2 P2.16's "only unagreed exposure" note) | §3.6 value table, HS-4, U-E18 |
| **R8-2** (02.2, 02.3; P2.13) | HP-H standing becomes "not offered by SWBPIPE". The enforcement-boundary lead records the SQ-02 answer and D6's Phase-1 closure. The authoring advice records that no governed checkpoint is enforceable from the App on SWBPIPE's X | §2.3, §3.6 |
| **R8-2** (D6; P2.17; Part 4.11) | **D6 is closed for Phase 1** by DECISION-4 and re-opens only when the governance phase is taken up. U-E1 is restated. U-E23 re-points to it. F-17 is closed for Phase 1. Register rows (§8) are updated | UNRESOLVED U-E1, U-E23; §8; §11.2 |
| **R8-3** (I2 R8-Q2; §3 item 2) | Staleness scope: per-item where the host supplies subject identities; otherwise the host's stated scope is received and shown (SWBPIPE: whole model), never narrowed; de-duplication first is unchanged. Noted at the MX rules and CH-17 | §4.11, CH-17 |
| **R8-4** (I2 R8-Q3; 03.6) | Whole-model identity is received as every covered subject's identity: this errs toward a lapse and never misses one, and the App never computes identities. SP-4 is annotated. New U-E25 (SWBPIPE does not meet V4-HI-32; owner SWBPIPE) | §4.5 SP-4, UNRESOLVED |
| **R8-5** (I2 R8-Q-item-1, R8-Q10, R8-Q13, R8-Q15) | Outcome mapping at the MX rules and CC-2: `unsupported_method`/`unsupported_change` → host-reported *not exposed on this surface*, never *not permitted*; #885 `withdrawn` → item left, "cleared by the person, no decision record"; `validation_rejected` → *refused — invalid* at application. None of these is ever A10 or A11. Accept-and-apply is one step per batch with no A10 record. Session undo writes no receipt, so "reverses ⟨receipt⟩" is *not supplied* | §3.7 CC-2, §4.11 |
| R8-7 (X.4, X.5; 17.1, 18.1, 19.2, 25.1, 01.2; STD-2) | Standings move to **answered** where EXEC records host inputs: Consumed inputs, §9.1 host-owner row, CH-28, RT-1, RT-2, RT-4, RT-5 (STD-2 annotations keep the AWAITING INPUT token). U-E9, U-E11, U-E12, U-E14, U-E15 and U-E2 owners and effects are updated. OI-003 is qualified as "App v4 OI-003" | Header, §7.3, §9.1, §10, UNRESOLVED |
| R8-10 (I2 R8-Q12) | Strict preflight: the agent never adds fields the host schema lacks. This is recorded at CH-27 and U-E13 | CH-27, U-E13 |
| (A1, reading flagged) | PH-6 (disposition words as record labels) and PH-8 (a lapse is still recorded in Phase 1, per V4-REC-05; re-hold is governance phase) are **PROPOSED (A1)** readings of R8-1. The Phase-1 standing of I-7 / V4-HI-42 and of D2's "or a declared checkpoint" is left open as new U-E24 | §2.1, UNRESOLVED |

## Changes from v0.2

| R5 ID (source) | Change in v0.3 | Where |
|---|---|---|
| **R5-1** (V3-A MAJOR-1; V3-B MAJOR-5) | §3.6 publishes the one four-value hold-support set as ruled: *enforced by the host loop* · *enforced on the host route* · *not established* · *not enforceable*, each with its workflow-check effect. Deterministic assignment rows HS-1…HS-5. The EXEC-v0.1 values and "held after observation", and the v0.2 value "host-enforced for host operations", are retired. §3.5 gives the three-valued check result and the multi-checkpoint precedence (INTEGRATION, confirmed; WD §4.3.8, WD-EX E8). Recomputed: MT-1, MT-2 (`CP-accept` not established; `CP-check` not enforceable → unsupported), MT-8, MT-15, new MT-16, CH-1, CH-22, CH-23, CH-26, CH-27, CH-29 | §3.5, §3.6, §7 |
| R5-1 / WD-v0.5 ruling (INTEGRATION) | App-only checkpoint defined: its arrival and held actions involve no host operation (e.g. E1 `CP-check` in an App run) → *not enforceable* in App runs, whatever SQ-02 returns | §3.6 HS-5 |
| **R5-2** (Y-1, Y-8) | HP-H and §3.6 use the final carriage terms: host-held (derived from, or verified against, the host's own copy; the host loop's own evaluation); received-only keeps its source's assurance; App-assured **not available** in this increment. F-18 closed | §2, §3.6 |
| **R5-3** (Y-2) | §4.10: the declared setting content always binds; invalidity when none is named is unconditional; an A8 presents it but never changes the subject; run-dependent scope is a declared binding rule. CH-29 shows an A8 not rescuing an invalid declaration | §4.10, §4.14, CH-29 |
| **R5-4** (Y-3; V3-A m-11) | CR-14 shows the destination at report time. The run record carries the destination per turn (requested and effective separate, re-routes with their turn, unobserved → *unknown*); the run-level value is the observed set; a switch starts no new run. The record-and-show element is relabelled **INTEGRATION (DECISION-2 reading)**; "no gate" stays SETTLED (D5). F-21 and U-E22 closed | §3.3, §6.1, RT-5 |
| **R5-5** (Y-4) | RH-8 generalized: a lapse re-holds whatever caused it, including the person's own undo. The person's undo is never *action during hold*. RH-9: an undo never re-holds an A5 arrival. New CH-30 | §4.7, CH-30 |
| **R5-6** (Y-5) | The person's own edit and undo are R7 operations, not human-act records (RH-8) | §4.7 |
| **R5-7** (Y-6; V3-A MAJOR-3, MAJOR-5) | CH-12…CH-14 re-point to C **V-GR1**. T15's A12 before the arrival is **not counted** (CH-12 (iii)), and the owner-visible cost is recorded under U-E4 | CH-12…CH-14, U-E4 |
| **R5-9** (Y-7; V3-A MAJOR-4, m-1, m-3, m-12; V3-B notes) | WD-EX local cases are re-pointed **by content** to WD-EX-v0.4: MT-3 → "OP-C4 absent" [L-WDEX-13]; MT-4 → new L-EXEC-26 (no OP-C5-absent case in v0.4); MT-13 → C V-NP1; MT-14 → E7 "External access off"; CH-7 → R-4 (ii) (retires L-EXEC-10); CH-10 → R-4 (iii); CH-18 → C V-S1; CH-19 → R-6b [L-WDEX-4] (retires L-EXEC-16); CH-20 → R-9b [L-WDEX-7]. Other re-points: MT-12 → C V-ED1 (retires L-EXEC-5); L-EXEC-19 → C **AF-1**; ⟨fx-app-import⟩ → **LIB-A2**; ⟨fx-proj⟩ → **LIB-A1**; FA-n → **FXA-n**. F-15, F-20 and U-E21 closed. §9.1 cites the v0.4 set | §7, §9, header |
| **R5-10** (V3-B MAJOR-4) | F-17 restated: SQ-02 decides holds for host-operation checkpoints only; App-only checkpointed workflows stay *not enforceable* whatever SWBPIPE answers, which is a separate D6 follow-up for the owner | §3.6, §11 |
| HOSTING-v0.5 F-22 ruling (INTEGRATION) | HP-4 scope: covers only App-initiated turn starts and App-as-caller calls. A person-directed turn on a holding run is not blocked; it is carried with initiator *person-directed*; the disposition is unchanged; governed agent actions in that turn are *action during hold*. Closes HOSTING U-25 | §2 HP-4, CH-22 |
| V3-A m-9 | Display string aligned: "waiting — re-held, lapsed at ‹t› after resume" | §4.3, §4.6, §4.7 |
| V3-A m-10 | CH-28 now precedes CH-29 | §7.2 |
| **R6-1** (V4-A MAJOR-1, MAJOR-2; in place) | §3.6 restated **by held actions**: HS-3 when every held action is a host operation (value by SQ-02 status); HS-5 when any held action is App-side (*not enforceable* in App runs; conservative default when the declaration does not show the held actions); HS-1 no value (confirms F-22); HS-2 unchanged. Evaluation order HS-1, HS-2, HS-5, HS-4, HS-3, an exhaustive partition for App runs. New fixture classification table: E1c/E1d `CP-check` → HS-5 *not enforceable* in App runs. MT-2 unchanged; **MT-16 now includes E1c's `CP-check` → *unsupported***. "Each **valid** checkpoint" (V4-A m-8). New F-28 | §3.6, MT-16, VC-E-12, §11 |
| **R6-4** (V4-A m-1, m-2; in place) | Stale "being added" / "not yet in C" markers for V-GR1 removed (C-v0.5 §10.4 has it). L-EXEC-13 reason re-pointed to GR-P (pending then *lost* vs. this case's pending then *established*); L-EXEC-14 reason to GR-R (refusal before performance vs. this case's refusal after); CH-13 (i) and CH-14 cite GR-R and GR-S directly; CH-11 reason updated. F-26 closed | Header, §7, CH-11…CH-14, §9.1, §11 |
| **R7-3** (V5 MAJOR-3; INTEGRATION, option (a); in place) | HS-5 echoes WD §4.3.1: when the held-actions element is absent, an A5 checkpoint's held actions are its governed operation(s) and a kind (a) checkpoint's its held call, as §3.6 already defines; the conservative HS-5 default applies only to a kind (b)/(c) checkpoint with no held-actions element, or whose declared held actions do not show host operations only. WD-EX E8 "L-WDEX-17 with its held-actions element absent" is therefore HS-3 → *not established* today (its workflow result by §3.5 precedence: L-WDEX-17 has no other checkpoint, so *not established*). No value in the fixture classification table, MT-1, MT-2, MT-16 or V-GR1 changes | §3.6 HS-5 |
| **R7-4 m-5** (V5 m-5; in place) | §3.6 value table: "a constraint carried only as *model-supplied*" → **not enforceable** is qualified "once SQ-02 is answered with no host-held route (HS-3 (c); before that answer, *not established*)" | §3.6 |
| **R7-4 m-6** (V5 m-6; in place) | U-E23 point of need: "any App-side workflow with a kind (b)/(c) run halt" → "any workflow with a checkpoint with any App-side held action (including an App-content checkpoint)", following R6-1 (classification by held actions, not arrival) | UNRESOLVED U-E23 |
| **R7-4 m-8** (V5 m-8; in place) | Header: the R6 line notes that WD-EX `296875c9…` is the pre-R6 byte state; a new R7 line records the sibling inputs read at the R7 working state (WD, WD-EX, C, ADAPTER and GUIDE at `2f42fba02`, then with their R7 in-place edits); GUIDE pins the post-R7 bytes | Header |

## Changes from v0.1

| R4 ID (source finding) | Change in v0.2 | Where |
|---|---|---|
| R4-1 (D5; relabelled by R5-4: no gate SETTLED by DECISION-2; record and show INTEGRATION (DECISION-2 reading)) | The App run's **model destination** is recorded and shown as information only. It never gates enablement, a check or a transfer. Report element CR-14; *supplied* and *observed behavior* links name it for App runs | §3.3, §6.1, RT-5 |
| R4-2 (D6 deferred to SWBPIPE SQ-02) | HP-1 (interposed App code) and HP-2 (reliance on `turn/interrupt`) are **not adopted**. HP-3 remains a permitted best effort (D3). New HP-4: the App initiates nothing for a holding run. New HP-H: a host-side hold, pending SQ-02. App-side holds are `UNRESOLVED{D6}`. Hold support is re-valued: App-run holds without host enforcement are **not enforceable**. *Action during hold* is always recorded. U-E1 is restated as `UNRESOLVED{D6}`; U-E20 is withdrawn (nothing relies on `turn/interrupt`). F-10 is carried to C1 | §2, §3.6, §4.2 HD-4, MT-2, CH-22, UNRESOLVED |
| R4-3 (F-2) | Resume point HD-5 and re-hold RH-1…RH-9 **adopted** across the set | §4.2, §4.7 |
| R4-4 (F-4) | No resumption, post-end acts and *continues ⟨run⟩* **adopted** (PROPOSED standing kept per R4-4) | §4.9 |
| R4-5 (F-3) | SP-6 **adopted as PROPOSED**; U-E4 stays open for the owner | §4.5, UNRESOLVED |
| R4-6 (F-5) | Refused, pending and unconfirmed A12 rules and "supersedes only when established" **adopted**; U-E6 closed | §4.10 |
| R4-7 (F-1) | MX-3, MX-6 and MX-8 **adopted** into WD §4.3.7; R2-18/R3-3 **CONFIRMED** by DEL-02-03 | §4.11 |
| R4-8 (F-8) | "Checkpoint hold not enforceable on this surface" **adopted** as a WD §4.2.4 *unsupported* reason | §3.6 |
| R4-9 (F-13) | Grant-setting subject without an A8 = the setting content the declaration names. A declaration naming none is **invalid** for A12 (INTEGRATION). U-E5 closed; new case CH-29 | §4.10, §4.14, CH-29 |
| R4-10, R4-11 (F-6, F-7) | RS elements requested here are adopted into RS v0.4 by R4; the findings are closed | §11 |
| R4-12 (F-9) | Elicitation and user-input answers are not act evidence: CAP-6 **adopted**; HOSTING updated by R4 | §5 |
| R4-13 (ADAPTER F-4) | CAP-1: where A13 is captured App-side is set by DEL-04-01 (U-X1). An App-side Codex configuration an agent could write is never A13 evidence | §5 |
| R4-14 (ADAPTER F-1) | The constraint travels with a **carriage assurance**. For App runs only *host-held* counts (App-assured requires HP-1, not adopted under R4-2). Model-supplied carriage alone makes the A5 hold support *not established*. This answers ADAPTER U-X3 for GC-3 and GC-5 | §3.6, §8 |
| R4-15 (ADAPTER F-8) | Author identity may be *unverified*. A transfer's *exported* link names the exporter as observed, not as verified | §6.3 TR-4 |
| R4-19 (V2 minors) | R3 and R4 added to Consumed inputs. CH-10 already uses T16a | Header |
| R4-20 (F-15) | C at `f05c7e4cd` has no App-file subject or App-side library yet. The L-EXEC-19, ⟨fx-app-import⟩ and ⟨rev-A3⟩ local labels stay with their reasons, to be re-pointed when C adds them | §7, F-15 |
| R4-21 (F-16) | Reached-when kind (a) on a harness capability is **not holdable** in App runs pending D6; hold support reports *not enforceable*. F-16 closed | §3.6, MT-15 |
| DEL-09-06 citation request | Host-dependent items and cases cite RELAY-v0.1 SQ IDs; evidence account RT-11 maps to CA-v0.1 W14 cases | §7, §8, UNRESOLVED |
| C1 carry (R4 "Carried to closeout C1") | F-10, F-11, F-12 and U-E3 (U-03) carried to closeout C1 | §11, UNRESOLVED |

---

## 0. Reading this definition

**What it defines.** Three things this deliverable owns (SoW OUT-001, OUT-002;
WD §10 "Checkpoint hold machine, re-hold, ended-run resumption, required-tool
check, transfer"):

1. the **required-tool compatibility report** (§3);
2. **checkpoints in execution**: in Phase 1, plan guidance and recording
   (§2.1). The **checkpoint hold machine**, including interruption and
   replay (§4), is kept as the governance-phase definition (§2.2). Also
   App-side act capture (§5), which is in force in both phases;
3. the **App→host transfer and host→App refinement trace** (§6);

plus fixture design (§7) and the resolution of every item Wave-1 held for W7
(§8).

**Phases (R8-1; DECISION-4 D4-1).** **Phase 1** is this increment. In it,
declared checkpoints are plan guidance that the person and the agents manage
(§2.1). The **governance phase** is a later layer, per workflow that needs it,
for checkpoints declared `governed`. Its definitions are **retained** here
(§2.2), relabelled but not deleted. A passage marked *governance phase* is
not in force as enforcement in Phase 1.

**What it does not define.** Declaration meaning (DEL-02-01), catalog meaning
(DEL-03-01), proposal outcomes (DEL-03-02), act names and policy (DEL-04-01),
record fields (DEL-04-03), host-loop receiving (DEL-05-01), panel receiving
(DEL-05-02), registration (DEL-02-02), native act controls (DEL-01-04), the
external adapter (DEL-03-03) and the joined witness (DEL-09-06). It selects no
wire field, type, transport, hash or canonicalization algorithm, persistence,
process/thread placement or shared-component placement (OI-013, OI-014,
TBD-003, TBD-004).

**Naming.** Bold phrases are *semantic element names*, not wire names. Act
names are canonical A1–A14 (R-1). Dispositions are the six shared values
(WD §4.3.4). Class values are the five of C §3.1 (R2-1). Supplier method names
such as `turn/interrupt` are cited as observed facts about Codex 0.158.0 in
generated types (W11); citing one selects nothing.

**Labels.** SETTLED (accepted basis or owner ruling, cited), DERIVED,
INTEGRATION (R1/R2/R3/R4 integrator rulings, cited). **PROPOSED (W7)** marks a
design choice made here, open to comparison and to owner revision.
**ADOPTED (R4-n)** marks a PROPOSED (W7) rule that R4 adopted across the set,
keeping any standing R4 gives it (e.g. R4-4 and R4-5 stay PROPOSED).
`UNRESOLVED{…}` is an open owner choice, never a permission or default.
Local fixture cases are `L-EXEC-n`, each with its reason. From v0.4,
**PROPOSED (A1)** marks a reading this file adds to R8, for the integrator to
confirm. **Phase 1** and **governance phase (retained)** mark which phase a
rule belongs to (R8-1).

---

## 1. Settled distinctions this contribution relies on

| # | Distinction | Citation | Use here |
|---|---|---|---|
| E-A | The product checks a selected workflow's required tools against the current host and tells the person which are missing | V4-WF-04; SoW REQ-001 | §3 |
| E-B | At a declared checkpoint the act is requested and the run does not record it as done until the person performs it; checkpoints override autonomy. **Phased (R8-1):** "the run does not record it as done until the person performs it" is in force in Phase 1 (§2.1 PH-4). V4-WF-05's first half ("holds … the run waits") is phased to the governance layer, not withdrawn (§2.2), and flagged for the next accepted-basis update. The Phase-1 standing of "override autonomy" is U-E24 | V4-WF-05; V4-HI-42; D2 "No autonomy grant widens past … a declared checkpoint"; DECISION-4 D4-1 | §2.1, §2.2, §4 |
| E-C | Success, a queued proposal, a receipt or findings supply no human act | V4-HI-25; V4-AUT-03; WD I-2 | §4.5 |
| E-D | A human act binds to content, scope and purpose, and lapses visibly when content changes | V4-REC-05; V4-HI-32 | §4.5, §4.7 |
| E-E | Only observed events are shown as having happened; unobserved outcomes are unknown | V4-EXE-03; P §4.1 rule 3 | §4.12 |
| E-F | Source-qualified identity; no silent rebinding | V4-WF-03; WD §6 | §6 |
| E-G | App workflows can be carried into a host and adapted; host workflows can be opened and refined in the App | V4-WF-06 | §6 |
| E-H | Round trip observes selected/resolved bytes, what was supplied, provider-adopted and observed behavior separately; portability or registration alone proves nothing | V4-EXM-14 | §3.5, §6.1 |
| E-I | Reserved to the person: A4, A5 (where a proposal is required), A6, A7, A12, A13 (enabling) | D2 (SETTLED); R-1, R2-2, R2-3 | §4, §5 |
| E-J | App routine tool permission (A14) is the user's own Codex setting and never stands in for a reserved act; hosts have no classifier mode | D3 (SETTLED); R2-8 | §4.2, §5 |
| E-K | The standalone App executes through stock Codex; no other App engine or presumed common service | SoW CLM-003; V4-ARC-20 | §4.2 enforcement boundary |
| E-L | Host execution, catalog, act facility, receipts and library are the external host owner's; files are human-relayed | SoW CLM-002/003, DEP-001 | §3, §6 |

Canonical checkpoint rules consumed unchanged: the closed act list A4, A5, A6,
A7, A12 (WD §4.3.1; AP §4.1); reached-when kinds (a)/(b)/(c) and the
independent subject class with its validity rules (WD §4.3.1, R2-17, R3-1,
R3-2); independence rules I-1…I-7 (WD §4.3.3); subject binding SB-1…SB-4
(WD §4.3.6); act-declined and run-ended events (R2-5); lapse sequence before
resume (R2-19); capture-evidence requirement (R-5, R2-20); governing
checkpoint constraint (R2-12; its carriage assurance is governance phase,
R8-1).

---

## 2. Parties, execution placement and the enforcement boundary

| Concern | Owner | This contribution |
|---|---|---|
| Check meaning (outcome vocabulary, pass rule) | DEL-02-01 (WD §4.2.4) | Consumes unchanged; defines the report and evaluation order (§3) |
| Check execution for App-selected workflows and App-carried runs | DEL-02-03 | §3 |
| Check execution inside a host | Host owner; a DEL-02-03 checker only if OI-014 allocates one (PANEL §3.2) | Supplies the same meaning |
| Checkpoints in App runs | DEL-02-03 | Phase 1: guidance and recording (§2.1). Governance phase: hold machine (§2.2, §4) |
| Checkpoints in host loops | DEL-05-01 receiving; external construction; `UNRESOLVED{OI-013}`; sharing `UNRESOLVED{OI-014}` (WD §9 A-4) | Phase 1: the host's embedded loop enforces no hold either (§2.1 PH-2; DECISION-4 clarification). Governance phase: supplies the hold-machine semantics; placement not proposed |
| Act capture on host content | Host act facility (V4-HI-31); capture-evidence reference is a relay question (R2-20; DEP-001) | Consumes |
| Act capture in the App | App interface (WD I-5); control construction DEL-01-04 (later, D1); record DEL-04-03 | §5 defines requirements |
| Transfer procedure and trace | DEL-02-03 (WD U-18) | §6 |
| Draft, review, registration, selection policy | DEL-02-02 (later, D1) | Routed to, never performed |
| Joined round-trip witness | DEL-09-06 | Receives §7 evidence account |

### 2.1 Phase 1: checkpoints are plan guidance (R8-1; DECISION-4 D4-1) — normative

The phasing is SETTLED by DECISION-4 D4-1 and its clarification. The framing
below is INTEGRATION (R8-1). Two rules add a reading to R8 and are marked
**PROPOSED (A1)**.

| # | Rule (Phase 1, this increment) |
|---|---|
| **PH-1 Guidance** | A workflow's declared checkpoints are **plan guidance**. The declaration still states each checkpoint's required act, reached-when, subject class and held actions (WD §4.3.1). The person and the agent work out the plan around them, and the agents manage any pause, hold point or gate themselves |
| **PH-2 No enforcement** | Neither the App nor a host's embedded loop enforces a hold. Neither stops or blocks a run, withholds or holds a dispatch, or re-holds a run at a checkpoint. No hold is claimed. The principle applies to the host's own embedded loop (DECISION-4 clarification; R8-8 for LOOP §2.4.4) |
| **PH-3 No *unsupported* for hold reasons** | The required-tool check (V4-WF-04; §3) is unchanged. No checkpoint enters its result. The result depends on the required tools and the channel state (R8-2), together with the role and delegation reasons WD §4.2.4 already names, which are not hold reasons. No hold-support value is assigned. The reason "checkpoint hold not enforceable on this surface" (R4-8) is never reported. An invalid or not-established checkpoint declaration is reported as a declaration defect and does not change the result (§4.14) |
| **PH-4 Acts only when performed** | A human act is recorded as done **only when the person performs it**, with capture evidence from the capturing surface (V4-WF-05 second half; §4.5 SP-1…SP-8; §5; R3/R4 act-evidence rules). An agent never records a human act on the person's behalf. None of the following is ever the act: success, a queued proposal, a receipt, findings, host checks, an A14 settlement, an elicitation answer, or a conversation statement (E-C; CAP-5…CAP-7) |
| **PH-5 Reserved acts stand** | DECISION-1 D2 is unchanged. A4, A5 (where a proposal is required), A6, A7, A12 and enabling external access (A13) stay the person's (E-I). A host enforces its own list through its operations (V4-HI-30). For example, SWBPIPE's Apply is A5 in the person's hands, and enabling external access is A13 (R8-6). PH-2 removes no host refusal of an agent's attempt at a reserved operation |
| **PH-6 Recording is observation** | A checkpoint's arrival and the act that answers it may be **recorded** (RS), with the other §4.4 events: act-declined, act-lapsed, run-ended, and observation lost or recovered. This lets the person and the agent see where the plan paused and what was done. Recording is observation, not enforcement. **PROPOSED (A1):** a view that states an arrival's state from the record may use the shared disposition words (WD §4.3.4) as record labels. *Waiting* then means "reached; act not yet recorded", never "the run is held" |
| **PH-7 Continued past a checkpoint** | *Action during hold* is not a violation marker in Phase 1. A run action observed after an arrival and before the act that answers it may carry the optional plain annotation **"continued past ‹checkpoint› before ‹act›"** (R8-1). It is information: never a defect, refusal or finding |
| **PH-8 Lapse is recorded; nothing re-holds** | **PROPOSED (A1).** A performed act whose bound content changes is still recorded as lapsed: an act-lapsed event, shown against the affected referents, with outputs gated by that act showing their standing lapsed (V4-REC-05; R2-19 recording). The run is **not** re-held: re-hold (RH-2…RH-7) is governance phase. R8-1 lists "re-hold, lapse" with the retained hold machine. This file reads the *recording* of a lapse as Phase-1 observation required by V4-REC-05, and the *hold* consequences as governance phase |
| **PH-9 `governed` in Phase 1** | A checkpoint declared **`governed`** (WD-v0.6 §4.3.1, PROPOSED) is honoured in Phase 1 **only as guidance**. The flag is shown, and PH-1…PH-8 apply unchanged |
| **PH-10 V4-WF-05** | Its first half ("the product holds a workflow's declared checkpoints … the run waits") is **phased to the governance layer, not withdrawn**. Its second half is in force (PH-4). Flagged for the next accepted-basis update (R8-1; DECISION-4 "Route") |

What Phase 1 keeps from §4 is its **recording** content: identities (§4.1),
events (§4.4), which recorded act answers which arrival (§4.5), the
disposition words as record labels (§4.3, §4.6), negative decisions and paths
as recorded (§4.8), run end and continuation (§4.9), A12 control relations
(§4.10), A5 item rules (§4.11), record rebuilding and replay (§4.12, except
RP-4 and the "stays holding" clause of RP-5), and invalid-declaration
reporting (§4.14). Its **hold** content is governance phase (§2.2).

### 2.2 Governance phase: the retained definition and the `governed` opt-in (R8-1, R8-2)

| # | Rule |
|---|---|
| **GV-1 Retained, relabelled** | The following are the **governance-phase definition (retained)**. They are relabelled, not deleted: the enforcement boundary (§2.3: HP-1…HP-4, HP-H); the hold-support clauses of the check result and its precedence (§3.5); hold support (§3.6: four values, HS-1…HS-5 as amended by R6-1, R7-3 and R8-2); the hold machine's hold content (§4.2 HD-1…HD-4; re-hold §4.7 RH-2…RH-7; §4.10 AR-2; §4.12 RP-4 and RP-5's "stays holding"; §4.13 MA-3); R2-12 carriage assurance; the R4-8 *unsupported* reason (WD §4.2.4); and the LOOP §2.4.4 host-loop hold |
| **GV-2 Opt-in per checkpoint** | A workflow opts in by declaring a checkpoint **`governed`** (WD-v0.6 §4.3.1; new optional flag, PROPOSED). In the governance phase, §3.5's hold-support clauses and §3.6 apply to governed checkpoints only. A checkpoint not declared governed stays plan guidance in every phase. Not every workflow will have governance. Every workflow that needs it must be serveable by these definitions, so the declaration keeps every field they consume (WD §4.3.1) |
| **GV-3 When it applies** | Later, per workflow that needs it, when the owner calls for it (DECISION-4 D4-1). **D6** (App-side run holds) is closed for Phase 1 and re-opens then (R8-2; U-E1). Until then nothing in this file is in force as enforcement |
| **GV-4 SWBPIPE governance-phase input (R8-2)** | SQ-02 answered 2026-09-28, **route (iv), none planned** ((a) No: a constraint field would be refused as unknown; (c) No; (d) No/No; (f) No/No). Under the retained rules, a governed checkpoint whose held actions are only host operations on X is **not enforceable** against SWBPIPE (HS-3 (c); I2 R8-Q1 reading adopted for that phase). SQ-11 is answered (no exposure element; only `position.x` on X), so HS-4 does not mask SWBPIPE entries, and HS-3 (c) decides (I2 R8-Q-HS4). SWBPIPE has no host loop (SQ-20), so no *enforced by the host loop* evidence can exist for it now. SWBPIPE's "every change waits for Apply" is not host-held carriage (SQ-02 related fact; R2-12). A later SWBPIPE decision to plan a route is a **revision trigger** |
| **GV-5 Two-part statements** | Cases and consequences give the **Phase-1 result** and the **governance-phase value**. The governance-phase value reads the same checkpoints as if declared governed. No FX-PIPE-01 fixture declares the flag |

### 2.3 Enforcement boundary for App runs — governance phase (retained; R4-2)

The App runs workflows through stock Codex (E-K), and routine tool permission
is the user's own setting (E-J). How the App holds its own runs was deferred
by the owner to the SWBPIPE answer to RELAY SQ-02 (DECISION-2 D6). SWBPIPE
answered on 2026-09-28 that no host-held route exists or is planned (route
(iv)). D6 is closed for Phase 1 by DECISION-4, where no hold point is used
(§2.1 PH-2), and re-opens when the governance phase is taken up (R8-2). In
the governance phase the hold points stand as follows:

| Hold point | Mechanism (semantic) | Where it can act | Standing (governance phase) |
|---|---|---|---|
| **HP-1 Interposed App code before dispatch** | An App component in the dispatch path to the host's external surface holds the call undispatched | Kind (a) on a host operation | **Not adopted** (R4-2; D6). Kept only as the v0.1 option record |
| **HP-2 Reliance on turn interruption** | The App interrupts a running turn after observing an arrival (supplier `turn/interrupt`, generated types at 0.158.0) | Kinds (b), (c) | **Not adopted** (R4-2; D6). Nothing in this file relies on it |
| **HP-3 Named-rule decline of a tool-permission request** | While holding, an App named rule may *decline* a tool-permission request that reaches the App, with truthful origin (R-2; HOSTING R7). It never answers affirmatively | Native tools whose requests reach the App under the user's mode | **Permitted best effort** (R4-2; D3). Tools the user's mode auto-settles are not held. HP-3 never makes a hold *enforceable* |
| **HP-4 App initiates nothing for a holding run** | While a run holds, the App starts no turn of its own and issues no call as caller (e.g. `mcpServer/tool/call`, `mcpServer/resource/read`) for that run. **Scope (INTEGRATION; HOSTING-v0.5 F-22 ruling):** HP-4 covers only App-initiated turn starts and App-as-caller calls. A turn the **person** starts with their own message on a holding run is **not blocked**, because the person directs their own conversation. It is carried with initiator **person-directed**. The checkpoint disposition is unchanged: still *waiting* unless the person performs the required act through the capturing surface. Any agent action in that turn that the checkpoint governs is recorded as **action during hold**. This closes HOSTING U-25 | App-initiated actions only | PROPOSED (W7), scope INTEGRATION. App behavior, not interposition. It stops neither actions Codex takes in a running turn nor turns the person starts |
| **HP-H Host-side hold** | The host holds or refuses the run's host operations itself, through **host-held** carriage (R5-2): a constraint the host derived from its own resolved copy of the declaration, or received and verified against that copy; or a host hold before dispatch | Host operations of the run, on E and X | **Not offered by SWBPIPE** (SQ-02 answered 2026-09-28: route (iv), none planned; (a) No, (c) No, (d) No/No, (f) No/No). It would give *enforced on the host route* for host operations only if a host offered and evidenced it. It never covers App-only steps (R5-10) |

In the governance phase, a governed checkpoint that no enforcing point covers
on the acting surface is **not enforceable** there, and the check reports it
(§3.6; R4-8). Every run action observed while holding is recorded as **action
during hold** (RS R11; R4-2, R4-11). In Phase 1 neither applies: see §2.1
PH-3 and PH-7. In both phases the machine never claims a hold it did not
enforce (S-N; AX-002).

---

## 3. Required-tool compatibility report (REQ-001; AC-001; VER-001)

### 3.1 When a check is evaluated

| Occasion | Subject | Catalog edition used |
|---|---|---|
| **CK-1 Selection** — a workflow is selected or offered for a run | The selected identity tuple (WD §6.1), with holding library | The current host's current edition on the acting surface |
| **CK-2 Run start** — immediately before the run's first action | As CK-1 | The edition the run will be offered (LOOP: offered edition) |
| **CK-3 Edition change** — the host publishes a new edition while a report is shown or a run is live | As CK-1 | The new edition; the earlier report is kept, marked *not current* |
| **CK-4 Transfer** — before or after carriage into a host (§6.3), when the destination catalog is available | The carried identity | The destination edition; otherwise the report says *destination catalog not available* |

A report is evidence of one evaluation. It is never re-labelled, and a new
occasion produces a new report (E-E).

### 3.2 Inputs consumed

| Input | From | Rule |
|---|---|---|
| Declared part status; required tool references (reference, class, necessity, version compatibility, purpose, stage); compatible roles; delegation need | WD §3.4, §4.2.1–§4.2.2, §4.7 | Consumed unchanged; restriction ≠ requirement (WD §4.2.3) |
| Host identity; **catalog edition**; entries with operation identity and version | C §2, §3 #1 | Version **equality** only (C §3.2) unless the host publishes a compatibility statement (U-C9) |
| **Exposure** per surface (element 9) | C §3 #9 | Read directly at discovery; *unagreed* → not established |
| Availability preconditions, unavailable reason, evaluated basis | C §3 #4, §4.2 | Evaluated only when the check is asked for run-time readiness |
| Channel state (external access; A13) | C §4.1; V4-HI-52 | Surface-level, never per requirement |
| Acting surface and seat | App: external surface X; host: embedded surface E (C §8); seat role meaning (WD SEAT-1) | One report per acting surface |
| Harness capability inventory | DEL-01-01 (HOSTING §8; 0.158.0 inventory) | Names unresolved (WD U-08) → not established |

### 3.3 Report elements (semantic)

| # | Element | Meaning |
|---|---|---|
| CR-1 | **Report identity** | Identity of this evaluation |
| CR-2 | **Workflow identity evaluated** | Full tuple {kind, origin, source root, name, revision} + derived-from, with holding library (R-9, R2-20) |
| CR-3 | **Declared-part status** | declared · declared empty (required tools) · undeclared · not established (unreadable, newer contract version, unrecognized element in the category) (WD §3.4) |
| CR-4 | **Host and catalog edition** | Host identity; catalog edition; "catalog unreadable" if so |
| CR-5 | **Acting surface and channel state** | H / E / X; *channel not enabled* stated at this level (WD §4.2.4) |
| CR-6 | **Occasion and time** | CK-1…CK-4; when evaluated |
| CR-7 | **Per-requirement rows** | For each reference: reference; class (host operation / harness capability); necessity; purpose line; declared version(s); entry found (identity, version) or none; exposure value on the acting surface; availability result and reason with evaluated basis (only when evaluated); **outcome** (WD §4.2.4); reason |
| CR-8 | **Workflow-level result** | *unsupported* (with reason: role or delegation; or, **governance phase only**, hold not enforceable for a governed checkpoint, §3.6) or none |
| CR-9 | **Checkpoints** | **Phase 1:** each declared checkpoint listed as plan guidance (name, required act, reached-when, subject class, held actions, `governed` flag if declared), with no hold-support value (§2.1 PH-3). **Governance phase (retained):** per governed checkpoint, one R5-1 value (§3.6) and the HS row that assigned it |
| CR-10 | **Pass result** | passes · does not pass · not established (undeclared), by the WD pass rule |
| CR-11 | **Run-time holds** | Required references *present, currently unavailable*, each with reason |
| CR-12 | **Limitations** | E.g. "exposure is a fixture assumption (FXA-1)"; "version compatibility: equality only"; "destination catalog not available"; "evaluated on a test double" |
| CR-13 | **Evidence standing** | C's evidence-label mapping (illustrative / test-double / actual host) |
| CR-14 | **Model destination** (App runs on X) | The destination selected **at report time**, local or cloud, shown as information only. That host content may flow to the selected model with no gate is SETTLED by DECISION-2 (D5). Recording and showing it is **INTEGRATION (DECISION-2 reading)** (R5-4). Per-turn recording belongs to the run record (§6.1), not to the report. Never an outcome, a gate or a pass condition |

### 3.4 Evaluation order per required tool reference

Evaluated in this order; the first matching step gives the outcome.

| Step | Condition | Outcome |
|---|---|---|
| EV-1 | Declared part undeclared, unreadable, or the category is undeclared | Whole check **not established** (FB-01, FB-02, FB-05) |
| EV-2 | Element in the required-tool category unrecognized | That reference **not established**; never skipped (WD §3.4) |
| EV-3 | Class *harness capability* | **not established** until portable names exist (WD U-08) |
| EV-4 | Catalog unreadable, or reference cannot be resolved against it | **not established** (FB-06) |
| EV-5 | No entry in the edition | **missing** (FB-06) |
| EV-6 | Declared version(s) and entry version unequal, with no host compatibility statement covering them | **version mismatch** (C §3.2) |
| EV-7 | Exposure on the acting surface *unagreed* | **not established** |
| EV-8 | Exposure *not exposed on this surface* | **not exposed on this surface** |
| EV-9 | Acting surface's channel not enabled | the reference is reported under the surface-level **channel not enabled**; never *missing* or *unavailable* |
| EV-10 | Readiness asked and a precondition fails now | **present, currently unavailable** with reason and evaluated basis |
| EV-11 | Otherwise | **present** |

Class never produces *missing*, *unavailable* or *not exposed* (C §2
invariant 5; R2-4). A reserved entry is reported present when present; its
class matters at run time only (*not permitted* for an agent call, A8
offered).

### 3.5 Pass rule and person-facing statement

The pass rule is WD §4.2.4's, consumed unchanged. The **workflow check
result** is one of three values, and the first applicable row decides.

**Phase 1 (R8-1, R8-2).** No checkpoint enters the result (§2.1 PH-3). The
result depends on the required tools and the channel state, with the role and
delegation reasons of WD §4.2.4. The clauses marked *governance phase* below
do not apply.

**Governance phase (retained).** The pass rule is extended by hold support
for governed checkpoints (§3.6; R4-8, R5-1; GV-2). The **multi-checkpoint
precedence** is an integrator ruling (INTEGRATION; with WD-v0.5 §4.3.8 and
WD-EX E8), confirmed here. If any governed checkpoint on the surface is **not
enforceable**, the workflow is *unsupported*. Otherwise, if any is **not
established**, the check is *not established*. Otherwise, as to hold support,
it passes (R5-1).

| Check result | When |
|---|---|
| **does not pass** (with reasons; includes *unsupported*) | Any required reference is *missing*, *not exposed on this surface*, *version mismatch*, or on a surface whose channel is not enabled. Or the workflow is *unsupported* by role or delegation. **Governance phase only:** or *unsupported* because any governed checkpoint's hold support is **not enforceable** (R4-8) |
| **not established** | Otherwise, if the declared part is undeclared or not established, or any required reference is *not established*. **Governance phase only:** or any governed checkpoint's hold support is **not established**, or a governed checkpoint is invalid or not established (HS-1) (R5-1: never a pass, never "unsupported") |
| **passes** | Otherwise. Every required reference is *present* or *present, currently unavailable*. **Governance phase only:** and every governed checkpoint is **enforced by the host loop** or **enforced on the host route** |

Rules for what the person is told:

- **PS-1** Every required reference that blocks a pass is listed with its
  purpose line and reason (S-E).
- **PS-2** A pass is stated as "requirement check passes against ‹catalog
  edition› on ‹surface› at ‹time›". It never says "compatible", "will run" or
  "runnable" (V4-EXM-14: a portable file or registration proves nothing).
- **PS-3** A registered or selected workflow whose check does not pass stays
  registered and selectable; the report says so (VER-001 "registration
  succeeds but a requirement is unavailable").
- **PS-4** An undeclared workflow is shown "requirements undeclared — check
  not established", never "no requirements" (WD §3.4).
- **PS-5** Optional references never block; their outcomes and stated
  fallback are shown.
- **PS-6** A run-time hold (*present, currently unavailable*) is shown as a
  hold with its reason, not as missing.

### 3.6 Checkpoint hold support — governance phase (retained; value set ruled by R5-1; owner EXEC)

**Phase (R8-1).** This section is the **governance-phase definition,
retained**. It is relabelled, not deleted. In Phase 1 no hold-support value
is assigned (§2.1 PH-3). In the governance phase it applies to checkpoints
declared **governed** (§2.2 GV-2). "In this increment" below means "in the
governance phase as the hold routes now stand".

Each **valid governed** checkpoint takes **exactly one** value on each acting
surface (invalid declarations: HS-1). This is the one value set for the whole
contract set (R5-1). The EXEC-v0.1 values (*enforced before dispatch*, *held
after observation*) and the v0.2 value *host-enforced for host operations*
are **retired**.

| Value | Meaning | Workflow requirement check (governance phase) |
|---|---|---|
| **enforced by the host loop** | Embedded route (surface E): the host loop holds the run (LOOP §2.4.4). Its own evaluation of the declaration is host-held carriage (R5-2). SWBPIPE has no host loop (SQ-20), so no host evidence for it can exist now | passes (holds subject to host evidence, DEP-001) |
| **enforced on the host route** | The host holds or refuses the operation through a **host-held** constraint (R5-2), evidenced by the host's answer to SQ-02 and a candidate (HP-H). Not offered by SWBPIPE (SQ-02 route (iv)) | passes |
| **not established** | Depends on a host answer not yet given (SQ-02), or on unagreed exposure. SQ-02 was answered for SWBPIPE on 2026-09-28, so against SWBPIPE neither cause gives this value now: HS-3 (c) decides (R8-2; this overrides I2 P2.16's "only unagreed exposure" note) | *not established* (never a pass, never "unsupported") |
| **not enforceable** | No mechanism exists on this surface in this increment. This covers App-only steps with no host operation (R4-2; D6). It also covers a constraint carried only as *model-supplied* once SQ-02 is answered with no host-held route (HS-3 (c); before that answer, *not established*). SWBPIPE has answered SQ-02 (R8-2) | *unsupported* ("checkpoint hold not enforceable on this surface", R4-8) |

**Assignment rule (R6-1: by held actions).** The value is decided by **what
the checkpoint must hold**, not by how it arrives. The *held actions* are the
actions the run must not take until the act: the governed operation for an A5
constraint or a kind (a) checkpoint, and otherwise the method's steps after
the arrival up to the act. The rows are evaluated in the order HS-1, HS-2,
HS-5, HS-4, HS-3; the first match decides. For App runs, HS-3/HS-4 and HS-5
together are an **exhaustive partition**: either every held action is a host
operation, or at least one is App-side.

| # | Surface and checkpoint | Value |
|---|---|---|
| HS-1 | Any surface; the checkpoint is invalid (FB-03, FB-13, FB-16; an A12 declaration naming no setting content, R5-3) or not established (FB-04) | **No value**. The checkpoint is reported invalid / not established and never evaluated; the check result is *not established* via the declaration (§3.5). Confirmed by R6-1 (F-22) |
| HS-2 | Host run on E | **enforced by the host loop** |
| HS-5 | App run; **at least one held action is App-side**: an App agent turn (e.g. a Return or summary step), an App tool or harness action (incl. kind (a) on a harness capability, R4-21), an App file write, or any action on App content (e.g. A4 on AF-1). Also, for a kind (b)/(c) checkpoint, where the declaration has no held-actions element or its declared held actions do not show host operations only (conservative default, PROPOSED (W7); finding F-28; scope ruled by R7-3). An A5 or kind (a) checkpoint with no held-actions element does **not** take this default: its held actions are derived — the governed operation(s) for A5, the held call for kind (a) (the definition above; WD §4.3.1; INTEGRATION, R7-3) — and it is valued by what those derived held actions are: HS-4/HS-3 when they are host operations; a kind (a) on a harness capability stays HS-5 (R4-21) | **not enforceable** in App runs (D6), whatever SQ-02 returns (R5-10; F-17) |
| HS-4 | App run on X; every held action is a host operation, but one of them has unagreed exposure (element 9 *unagreed*). **Except** where SQ-02 has been answered with no host-held route: then HS-3 (c) decides regardless of exposure (R8-2; I2 R8-Q-HS4). This covers SWBPIPE, where SQ-11 is answered with no exposure element | **not established** |
| HS-3 | App run on X; **every held action is a host operation** on the external channel. Examples: the governed operation of an A5 constraint (forced *propose*); the host operation a kind (a) checkpoint holds before dispatch; the host operations after arrival until the act | Depends on the status of SQ-02 (integrator confirmation, INTEGRATION; ADAPTER-v0.3 F-18/F-19). **(a)** SQ-02 answered, and host-held carriage or a host hold evidenced on a candidate → **enforced on the host route**. **(b)** SQ-02 unanswered → **not established**. **(c)** SQ-02 answered with no host-held route, so the constraint is only model-supplied or merely received → **not enforceable** → *unsupported*. *Enforced on the host route* is **never assumed**. **Current state (SWBPIPE): (c).** SQ-02 was answered 2026-09-28: route (iv), none planned (R8-2). A later SWBPIPE decision to plan a route is a revision trigger |

**Classification of the fixture checkpoints (R6-1; R8-2).** In Phase 1 none
of these checkpoints takes a value (§2.1 PH-3). The two value columns are
governance-phase values, reading each checkpoint as if declared governed (no
fixture declares the flag; GV-5). The X column applies SWBPIPE's SQ-02 answer
to the fixture's external surface, as I2 Part 2 does.

| Checkpoint | Declared held actions (WD-EX-v0.5) | Governance phase: App run on X | Governance phase: host run on E |
|---|---|---|---|
| E1 `CP-accept` (A5, kind (c) *queued*) | The governed OP-C4/OP-C5 operations (constraint forces *propose*) | HS-3 (c) → **not enforceable** (SQ-02 answered 2026-09-28: route (iv)) | **enforced by the host loop** |
| E1 `CP-check` (A4, kind (b) on `examination-report`) | Return (an App agent step) | HS-5 → **not enforceable** | **enforced by the host loop** |
| E1c / E1d `CP-check` (A4, kind (c) on OP-C9 *applied*) | WD-EX-v0.5 E1c declares no step after the arrival except returning the result to the person. It declares no host operation to hold. In an App run that return is an App agent turn | HS-5 → **not enforceable**. This applies both to the App-side Return and, as the default, to held actions the declaration does not identify | **enforced by the host loop** |
| E1d `CP-grant` (A12, kind (a) before dispatch of OP-C9) | The OP-C9 call (a host operation) | HS-3 (c) → **not enforceable** (SQ-02 answered 2026-09-28) | **enforced by the host loop** (C V-GR1) |

Consequences, each as a Phase-1 result and a governance-phase value (R5-1,
R6-1, R8-1, R8-2):
- **E1 run from the App on X.** *Phase 1:* the requirement check passes on
  the required tools and the channel state (MT-2). `CP-accept` and
  `CP-check` are plan guidance; nothing is held; acts are recorded only when
  performed. *Governance phase:* `CP-accept` → **not enforceable** (HS-3
  (c)) and `CP-check` → **not enforceable** (HS-5). The check is therefore
  *does not pass — unsupported* ("checkpoint hold not enforceable on this
  surface: CP-accept, CP-check"). SQ-02 is answered (route (iv)), so neither
  checkpoint can be enforced from the App on SWBPIPE's X.
- **E1c run from the App on X.** *Phase 1:* the check is decided by the
  required tools and the channel state (MT-5 shows the V-X1 exposure
  variant). *Governance phase:* `CP-check` → **not enforceable** (HS-5), so
  the workflow is *unsupported*.
- **E1d run from the App on X.** *Phase 1:* the requirement check passes
  (MT-16). *Governance phase:* `CP-grant` → **not enforceable** (HS-3 (c))
  and `CP-check` → **not enforceable** (HS-5), so the result is *does not
  pass — unsupported* ("…: CP-grant, CP-check").
- **Authoring advice (governance phase).** An author who needs a governed
  checkpoint enforceable from the App keeps **all its held actions on host
  operations**, e.g. an A5 constraint, or kind (a) on a host operation (R6-1;
  WR-11 advice). It is then enforceable only on a host that offers and
  evidences a host-held route. Against SWBPIPE (SQ-02 answered: route (iv))
  this route is not available, so **no governed checkpoint is enforceable
  from the App on X**, and every such workflow run from the App on X is
  *unsupported* in the governance phase. The advice stands for a host that
  offers a host-held route (P2.13). In Phase 1 the advice does not affect the
  check.
- **E1 in the host on E.** *Phase 1:* the check passes on requirements (MT-1),
  and the host loop enforces nothing (PH-2). *Governance phase:* both
  checkpoints are **enforced by the host loop**, and the check passes on hold
  support, subject to host evidence. SWBPIPE has no host loop (SQ-20).

App-assured carriage is **not available in this increment** (R5-2; R4-2): it
needs interposed App code, which is not adopted. In the governance phase HP-3
and HP-4 apply as best effort in every App run and never change a value.
Every run action observed while a governed checkpoint waits under a value
other than *enforced by the host loop* is then recorded as **action during
hold**. In Phase 1 see PH-7 instead.

**ADAPTER GC-3/GC-5, XF-26 (U-X3 retired to `UNRESOLVED{D6}`; governance
phase).** GC-3, GC-5 and XF-26 follow HS-3 (a)–(c), so EXEC and ADAPTER
agree. The v0.2 mapping of model-supplied carriage to *not established* is
replaced: model-supplied or merely received carriage is **not enforceable**
once SQ-02 is answered without a host-held route. Before that answer the value
is **not established**, because the route is unknown, not because
model-supplied carriage is acceptable. SQ-02 was answered 2026-09-28, so the
value is *not enforceable*.

In the governance phase, this makes S-N ("unenforced limits are stated, not
implied") and V4-EXM-14's "explicit unsupported-capability outcome" hold for
checkpoints as well as for tools. In Phase 1, S-N holds because no hold is
claimed (PH-2).

### 3.7 Run-time divergence and report currency

- **CC-1** A report is bound to its catalog edition. On CK-3 the earlier
  report is marked *not current* and a new one is produced; neither is
  rewritten.
- **CC-2** Run-time results are recorded as their own events and never
  back-filled into the report: a loop-side *not offered* failure, a
  host-reported *not exposed on this surface* (relayed), *unavailable*,
  *channel not enabled*, *not permitted* (C §4.1; LOOP §2.3). A host's
  `unsupported_method` or `unsupported_change` (SWBPIPE) is relayed as
  host-reported *not exposed on this surface*, never *not permitted*. That
  host does not meet R2-4, which requires a named rule (R8-5).
- **CC-3** A run whose check did not pass may still be started by the person
  (the check informs; it grants and forbids nothing). The run record carries
  the report reference; every later failure is reported as observed.
  **Governance phase:** *unsupported* for a non-enforceable governed
  checkpoint is shown at run start, and the run's checkpoint then records
  "hold not enforceable" on every arrival. In Phase 1 there is no such
  reason (PH-3).
- **CC-4** A *no policy basis* entry (OP-C11) is *present*; dependent
  production is reported **held** (R2-9), never as a pass of that production.

### 3.8 Failure behavior

| ID | Condition | Behavior |
|---|---|---|
| CF-1 | Catalog unreadable | Whole check **not established**; reason shown |
| CF-2 | Workflow revision no longer resolvable (WD FB-08) | No report on substituted content; "selected revision not resolvable" |
| CF-3 | Evaluation interrupted | No partial pass; report absent or *not established* |
| CF-4 | Two surfaces give different outcomes | Two reports; never merged |
| CF-5 | Host publishes a compatibility statement | Cited in CR-7; equality otherwise (U-C9) |

---

## 4. Checkpoint hold machine (REQ-002, REQ-003; AC-002, AC-003; VER-002, VER-003)

**Phase (R8-1).** §4 is kept as the **governance-phase hold machine
(retained)** for governed checkpoints (§2.2 GV-1, GV-2). In Phase 1 only its
**recording** content applies (§2.1, closing paragraph). No rule here holds,
blocks or re-holds a Phase-1 run. Where a Phase-1 view states an arrival's
disposition, the word is a record label (PH-6). Rules that hold are marked
*governance phase* below.

### 4.1 Identities

| Element | Meaning |
|---|---|
| **Run identity** | The workflow run (RS R1) |
| **Checkpoint identity** | {workflow identity tuple as resolved for the run, checkpoint name}. Stable across interruption and replay (SoW REQ-002; WD §4.3.1) |
| **Arrival** | One observed reaching of a checkpoint in a run, identified by {run identity, checkpoint identity, **arrival ordinal**}. A checkpoint may arrive more than once (WD RW-4) |
| **Arrival event** | The observed event that met reached-when, with its own evidenced time (host outcome time for kind (c); output production for kind (b); the hold of the call for kind (a)) |
| **Bound subject** | The referents the declared subject class names, bound at arrival (WD §4.3.6) |
| **Performance ordinal** | Counts the satisfying acts an arrival has had (1 on first *performed*; +1 after each re-hold) |

### 4.2 What "holding" means — governance phase (retained)

HD-1…HD-4 are governance phase and apply to governed checkpoints only. In
Phase 1 no run is holding (PH-2). HD-5 (resume point) is recorded in both
phases, because the lapse labels of R2-19 use it.

- **HD-1** A run is **holding** while any current arrival is *waiting*, or a
  kind (a) call is held undispatched.
- **HD-2** While holding, the run dispatches no operation and produces no
  declared output. The agent may still explain the request and may issue an
  A8 request (LOOP §2.3); conversation is not run progress.
- **HD-3** Host lifecycle continues independently: after the person's A5 the
  host may apply an item while the run holds (V4-HI-23). That is the host's
  action, not the run's.
- **HD-4** In App runs, holding a governed checkpoint is the governance-phase
  question D6 (R4-2). D6 is closed for Phase 1 by DECISION-4 and re-opens
  with the governance phase (R8-2). The App applies HP-4 and, as a best
  effort, HP-3. It relies on HP-H only where the host has evidenced it
  (SQ-02; SWBPIPE: not offered). Every run action observed while holding is recorded as
  **action during hold**, with its reference, never hidden. The disposition
  logic of §4.3–§4.13 is unchanged: an arrival stays *waiting* whether or not
  the hold is enforced. Only the claim of a hold depends on enforcement.
- **HD-5 Resume point.** When a current arrival becomes *performed*, or
  *resolved negatively* with a proceed or return path, the first run action
  after that change is the **resume point**. It is recorded as a
  **run-resumed event** {arrival, time, first action reference}. For kind (a)
  the first action is the dispatch of the **same** held call, unchanged
  (WD RW-2). "Before resume" and "after resume" in R2-19 are measured against
  this event (ADOPTED (R4-3)).

### 4.3 States per arrival

The disposition is always one of the six shared values. Everything else is
an **annotation** (never a seventh disposition, R2-18).

| Disposition | Annotations that may accompany it |
|---|---|
| **not reached** (checkpoint-level, before any arrival) | "run ended without arrival" |
| **waiting** | requested (purpose, scope); **lapsed at ‹t›** (before resume, R2-19); **waiting — re-held, lapsed at ‹t› after resume** (§4.7); **no items remain** (§4.11); **A12 awaiting control confirmation** / **A12 refused by control: ‹reason›** (§4.10); **act on other content** (SB-2); **prior act on this subject, not counted** (§4.5 SP-6); **act order unknown**; **subject absent** (§4.7); **hold not enforceable** / **action during hold** (governance phase); **continued past ‹checkpoint› before ‹act›** (Phase 1, optional; PH-7); **run ended** |
| **performed** | performance ordinal; per-item "accepted by ‹person›" (A5); **accepted — not applied: refused — stale** or **— application error (effect …)** (§4.11); **superseded by ‹act›** (A12); **resumed at ‹t›** |
| **resolved negatively** | A10 per item or act-declined event; **partial** (A5); path taken |
| **lapsed** | Only for an arrival whose run has ended and whose performing act lapsed after the end (R2-19); per referent |
| **unknown** | Which observation was lost; last observed state |

A checkpoint's displayed disposition is that of its **current arrivals**
(§4.13); earlier arrivals remain history.

### 4.4 Events consumed

| Event | Supplier | Effect class |
|---|---|---|
| Arrival (reached-when observed) | App observation / loop (LOOP §2.4.1); host outcome (P §9) | Creates an arrival |
| Human act observed (with capture evidence) | Capturing surface; faithful record citing it (RS §6) | Candidate satisfying act |
| A10 per item; item-left event; all-items-decided | Host via P §4.3 | A5 evaluation |
| Act-declined event | Capturing surface (R2-5) | Negative |
| Act-lapsed event | Host / record reader (RS L-6) | Lapse |
| Act superseded (A12) | Control (R2-7) | Annotation |
| A12 control relation: established ⟨version⟩ / refused ⟨reason⟩ / pending | Control surface (AP §2.1 A12; AS) | A12 evaluation |
| Applied outcome with resulting objects | Host (P §9, R2-14) | Binding for "objects changed by a named outcome" |
| Observation lost / recovered | Executor (App or loop) | Unknown handling |
| Run-resumed | Executor | Resume point |
| Run-ended | Run owner (R2-5) | Finality |
| Declaration invalid / not established | Executor on reading WD | No machine |

### 4.5 Satisfaction predicate (SP)

An observed act record *a* satisfies a waiting arrival *X* with required kind
*K* iff all hold:

| # | Condition | Source |
|---|---|---|
| SP-1 | Kind of *a* is *K* | I-1 |
| SP-2 | Decision actor is the person (for A7: the accountable professional as evidenced); in faithful recording the recorder is distinct and not named as actor | I-1; HA-2 |
| SP-3 | Capture evidence from the capturing surface for this subject, with a resolvable capture-evidence reference (host act facility for host content; App interface for App content, §5; the control surface for A12). An agent-authored record, a conversation statement or an A9 record without that reference never qualifies | I-5; R-5; FB-15 |
| SP-4 | Bound content c₀ equals the current content identity of every bound referent in scope, same method designation (A5: per item, the change-item content identity). **Whole-model identity (R8-4):** where a host supplies only a whole-model identity, it is received as the identity of every subject it covers. Any model change then lapses every bound act: this errs toward reporting a lapse and never misses one. The App never computes identities itself. SWBPIPE supplies only a whole-model identity (SQ-03; U-E25) | SB-1…SB-3; RS L-1/L-2; R8-4 |
| SP-5 | Scope of *a* covers the referents (A5 evaluated per item, §4.11) | WD §4.3.1 scope |
| SP-6 | **Captured at or after the arrival event** (ADOPTED (R4-5) with standing PROPOSED; U-E4 open): ordering by a request relation where the capturing surface records one, otherwise by evidenced times. If the order cannot be established, *a* does not satisfy and *X* shows "act order unknown" | V4-REC-05 purpose binding; below |
| SP-7 | For A12: the control relation is **established** (§4.10) | ADOPTED (R4-6) |
| SP-8 | *a* is none of: act-declined event, A8, A3 findings, A14 settlement, success, receipt, host checks passed | I-2; R2-8 |

**Why SP-6.** A checkpoint requests an act *with its declared purpose and
scope* (WD §4.3.1; IR1C-14), and an act binds to its purpose (V4-REC-05). An
act captured before the arrival was not made in answer to that request, so
its purpose is not the checkpoint's. It is shown as "prior act on this
subject, not counted" so the person can repeat it knowingly. SP-6 adds no
ordering *between act kinds* (I-3 stands): it orders the act only against its
own arrival. For A5 at kind (c) *queued* SP-6 always holds, because A5 can
only follow *queued*. The alternative — counting a prior act bound to current
content — is listed in U-E4 for V2.

### 4.6 Transition table (per arrival)

| From | Event / condition | To | Also recorded |
|---|---|---|---|
| (none) | Arrival event observed | **waiting** | "checkpoint reached" with bound subject, purpose, scope; act request issued; run holds (governance phase; in Phase 1 nothing is held, PH-2) |
| (none) | Run ends, reached-when never observed | checkpoint **not reached** | Run-ended event lists it |
| (none) | Deciding observation for arrival lost | **unknown** | Last observed state |
| waiting | Act satisfying SP-1…SP-8 (A4/A6/A7/A12) | **performed** (ordinal n) | Act reference |
| waiting | A5 evaluation gives *performed* (§4.11) | **performed** | Per-item acts |
| waiting | A5 evaluation gives *resolved negatively* | **resolved negatively** | Partial annotation if mixed |
| waiting | Act-declined event on this subject (A4/A6/A7/A12) | **resolved negatively** | Declared path follows (§4.8) |
| waiting | A12 refused / pending / on other content / prior act / order unknown | waiting | Annotation (§4.3) |
| waiting | Observation of acts lost during the wait | waiting (governance phase: the run holds; §4.12) | "act observation interrupted" |
| waiting | Run ends | waiting (final) | Run-ended event (R2-5) |
| performed | Act-lapsed event **before** resume point | **waiting** "lapsed at ‹t›" | R2-19 |
| performed | Act-lapsed event **after** resume point, run live | **waiting — re-held, lapsed at ‹t› after resume** (governance phase). Phase 1: the act-lapsed event is recorded and no re-hold follows (PH-8) | §4.7 |
| performed | Later established A12 on overlapping setting | performed | "superseded by ‹act›" (R2-7) |
| performed | Run ends | performed (final) | — |
| performed (run ended) | Act-lapsed event | **lapsed** (per referent) | R2-19 |
| unknown | Deciding observation recovered | as the observation determines | Recovered event with its own time; no back-fill (§4.12) |
| any | Later act after run end | unchanged | Act recorded and shown against the bound subject (R2-5; §4.9) |
| waiting (no items remain) | New arrival of the same checkpoint | waiting (final for this arrival) | "replaced by arrival n+1" (§4.11) |

Precedence when two events are evidenced for one arrival: the first in
evidenced order decides; later decisions are recorded and shown and do not
change a decided arrival. Evidenced order that cannot be established →
**unknown** for that arrival.

### 4.7 Lapse and re-hold (resolves W7 hold: WD U-22; AP U-10; RS U-24; AS U-13; LOOP C-4; PANEL W-5e) — ADOPTED (R4-3); re-hold is governance phase (R8-1)

**Phase (R8-1).** Re-hold (RH-2…RH-7) is governance phase and applies to
governed checkpoints. In Phase 1, RH-1 applies: the act-lapsed event is
recorded and presented, and outputs gated by the lapsed act show their
standing lapsed for the affected referents. RH-8's and RH-9's rules about
**which** acts lapse and what counts as *action during hold* also apply, as
recording rules. Nothing re-holds, and the agent re-requests the act as its
plan requires (PH-8, PROPOSED (A1)).

Before resume the R2-19 sequence applies unchanged. **After resume**, while
the run is live (governance phase):

- **RH-1** The act-lapsed event is recorded and presented (always).
- **RH-2** The arrival returns to **waiting**, shown "waiting — re-held,
  lapsed at ‹t› after resume" (R4-3 wording; V3-A m-9). It is the **same** arrival (same bound referent
  identities), now requiring an act on their *current* content. It is not a
  new arrival.
- **RH-3** The run holds at its **next action boundary** (HD-2). Dispatches
  already in flight complete and are observed; nothing is recalled or undone.
  A kind (a) call already dispatched stays dispatched.
- **RH-4** Actions between the resume point and the lapse observation stay
  recorded as taken under the then-current performance. Outputs whose
  promised standing names this checkpoint as **gating checkpoint** (WD §4.4)
  show that standing lapsed for the affected referents.
- **RH-5** The act request is re-issued with the declared purpose and scope,
  identifying the lapsed referents.
- **RH-6** A satisfying act makes the arrival *performed* with the next
  performance ordinal; a new resume point follows.
- **RH-7** If the run ends while re-held, the final disposition is
  **waiting** with the run-ended event (not *lapsed*: the lapse was observed
  while the run was live).
- **RH-8 (ADOPTED, R5-5).** A lapse re-holds whatever caused it:
  - a person's edit;
  - a person's undo (OP-C10, R2-15);
  - the run's own later action (e.g. a later stage editing rows already
    marked checked).

  A person's undo or edit is the **person's own operation**: an R7 entry, not
  a human-act record (R5-6), and never a run action. It is therefore
  **never** recorded as *action during hold*. A workflow that means to change
  checked content should place the checkpoint after the change.
- **RH-9** A5 never re-holds. Applying the item does not lapse A5; a basis
  failure after A5 is the stale rule (R-6); and an undo does not lapse A5/A10
  on the reversed item (R2-15), so **an undo never re-holds an A5 arrival**
  (R5-5). Only acts bound to content the undo changes re-hold, e.g. T16a's A4
  at T17 (CH-30). A12 never re-holds: supersession is not lapse (R2-7).

**Why re-hold rather than report only (governance phase).** V4-WF-05's first
half, phased to the governance layer (R8-1), and V4-HI-42 make the run wait
for the person's act. SoW AC-002 keeps it waiting "until evidence shows
that required act actually occurred". Continuing on an act whose bound
content changed would let later work rest on an act that no longer covers
current content (V4-HI-32). RH-3/RH-4 keep history truthful without
rewriting it.

**Partial lapse (carries WD U-05c / AP U-03 / RS U-07, owner DEL-04-01 with
the Owner).** When only some referents lapse, before or after resume:

- the request covers the **whole** bound scope, with the lapsed referents
  marked;
- a new act over the whole current scope satisfies under every option of
  U-03;
- whether an act on the lapsed referents alone satisfies, with the earlier
  act still covering the unchanged referents, depends on U-03. Until it is
  ruled, such an act is recorded and shown, and the arrival stays waiting.
  Case CH-8 is **HELD** on U-03 for that variant only.

**Subject absent (RS L-4).** If a bound referent no longer exists, the
arrival is waiting with "subject absent"; no act can satisfy it. An
act-declined event resolves it negatively, or the run ends. Whether the
declaration should carry an "on subject absent" path is for DEL-02-01 (U-E7).

### 4.8 Negative decisions and paths

- **NG-1** A5: A10 per item (§4.11). A4/A6/A7/A12: act-declined event
  (R2-5). Both give **resolved negatively**; never counted as performed.
- **NG-2** The declared **on negative decision** path governs: *stop* → a
  run-ended event with cause "stopped by declared negative path"; *return to
  a named stage* → the run resumes there, and a later reaching is a new
  arrival (RW-4); *proceed on a branch* → resume point on the branch.
  Absent path → stop.
- **NG-3** A resolved-negatively arrival is final. A positive act captured
  later is recorded and shown and does not change it.
- **NG-4** A run-ended event is never a negative decision; the arrival stays
  waiting (R2-5).

### 4.9 Run end, finality and continuation (resolves W7 hold: WD U-21; AP U-10; RS U-23; AS U-11; LOOP §2.4.1; PANEL W-5b) — ADOPTED (R4-4), standing PROPOSED

- **RE-1 No resumption of an ended run.** A run with a run-ended event is
  closed. Its arrivals' dispositions are final, except the R2-19 change from
  *performed* to *lapsed* on a later lapse. This confirms R2-5's default as
  the rule.
- **RE-2 Post-end acts.** An act performed after run end is recorded
  (DEL-04-03) and shown against the ended arrival's bound subject, marked
  "after run end". It changes no disposition of the ended run.
- **RE-3 Continuation is a new run.** To carry work on, the person starts a
  new run. It may record the relation **continues ⟨run⟩** (new record
  relation, finding F-4). Nothing carries into it: no arrival, no
  disposition, no act. Its checkpoints start *not reached*; its arrivals bind
  their own referents from events observed **in the continuation**. For
  example, "objects changed by a named outcome" binds only outcomes the
  continuation itself observes. By SP-6, acts made before its arrivals
  (including RE-2 post-end acts) are shown as "prior act on this subject, not
  counted".
- **RE-4 Interruption is not run end.** Loss of observation, an App restart
  or a loop restart without a run-ended event leaves the run **interrupted**
  and resumable as the same run (§4.12). If recovery is impossible, the run
  owner records a run-ended event with cause "interruption not recovered";
  dispositions are as reconstructed, and *unknown* stays unknown.
- **RE-5 Starting a run** is not an act in R-1's list and is not reserved; the
  run record names who started it.

**Why no resumption.** An ended run's record is evidence for later
reconstruction (DEL-09-11). Reopening it would let a later act rewrite a
closed disposition, and bind an act made without the run's request to it
(V4-REC-05). A continuation keeps both runs truthful and linked.

### 4.10 A12 refused by the control (resolves W7 hold: WD U-27; AP U-13, §12 item 5; RS U-17; AS U-14; LOOP C-8, FX-C11; PANEL W-5g) — ADOPTED (R4-6); subject rule R4-9

An A12 checkpoint's subject is a grant setting (WD §4.3.6; AP §4.2), and its
purpose is that the person's setting governs the operation the run is about
to request. The act binds to setting content; the control's response is a
relation on the act (R2-7).

**Subject (R5-3, amending R4-9; INTEGRATION).**
- The **declared** setting content always binds: the classes, grant values
  and scope the checkpoint's declaration names. The declaration must always
  name it. A declaration that names none is **invalid, unconditionally**
  (§4.14; CH-29). Invalidity is a declaration-time fact reported before the
  run (§3.6 HS-1).
- An A8 may **present** that content to the person but **never changes the
  subject**.
- A run-dependent scope is declared as a **binding rule** resolved at arrival
  (e.g. "targets of the held call"). It is never chosen by an A8.
- An A12 on different setting content satisfies nothing at that checkpoint
  (SB-2), even if established.

| Control relation on the A12 | Arrival effect | Shown |
|---|---|---|
| **established ⟨settings version⟩** (display *effective*, person-set) | Counts (with SP-1…SP-6) → **performed** | A12 reference and version |
| **pending** (*set by person, not yet confirmed*) | **waiting** | "A12 awaiting control confirmation" |
| **refused ⟨reason⟩** (e.g. "no policy basis", R2-9; W-e) | **waiting**; the refused A12 does not satisfy | "A12 by ‹person› refused by control: ‹reason›" |
| confirmation observation lost (*unconfirmed*) | **unknown** until observed | Last observed state |

- **AR-1** The refused A12 remains a recorded human act (HA-5). It establishes
  nothing (AP U-13) and is never shown as the checkpoint performed.
- **AR-2** (Governance phase; in Phase 1 no call is held, PH-2.) The held
  call (kind (a)) stays undispatched while the arrival waits. The person may perform another A12 on the named setting content
  once the control can establish it (R4-9), decline (act-declined →
  *resolved negatively*), or stop the run (run-ended; stays waiting).
- **AR-3** A refused A12 does **not supersede** an earlier established A12:
  the earlier setting stays in force (finding F-5 for DEL-04-01 §2.5 and
  DEL-04-03 L-0).
- **AR-4** Counting a refused A12 would release a held call on the premise of
  a setting that is not in force. The host would still resolve treatment from
  the grant actually in force (R-3), but the record would show the person's
  setting as governing when it did not. Hence *waiting*.

### 4.11 Confirmation of WD §4.3.7 (resolves W7 hold: WD U-20; AP U-09; RS U-18; AS U-09; P §4.3; LOOP C-7; PANEL W-5f)

**CONFIRMED by DEL-02-03 (R4-7)**, all five rows as written,
including the R3-3 accepted-then-stale row. Clarifications and additions:

| # | Item situation | Arrival effect | Status |
|---|---|---|---|
| MX-1 | Per-item states considered: A5 · A10 · undecided · left (item-left event) · **unknown** (decision observation lost) | — | Addition |
| MX-2 | Any bound item undecided | **waiting** (as WD row 2), even if others are unknown | Confirms |
| MX-3 | No item undecided; at least one **unknown** | **unknown** | **Addition** (WD has no row) |
| MX-4 | All remaining items A5, at least one remaining | **performed** over the remaining items; never "all items accepted" when any left (WD rows 1 and 4) | Confirms |
| MX-5 | All remaining items decided, at least one A10 | **resolved negatively**; "partial" annotation if any A5; on-mixed path if declared (WD row 3) | Confirms |
| MX-6 | No items remain (all left) | **waiting** "no items remain". When a new arrival of the same checkpoint occurs (e.g. a re-draft queued), this arrival is closed "replaced by arrival n+1" and keeps final *waiting*. The run holds until then or run end | **Clarification** of WD row 4 |
| MX-7 | An item with A5 later refused at application (stale; R2-16) | Unchanged: the item remains a **decided** member of the subject. Annotated "accepted by ‹person› — not applied: refused — stale (relied ‹B›, current ‹B′›)" | Confirms R3-3 row |
| MX-8 | An item with A5 later meets **application error** (effect none / partial / unknown) or **outcome unknown** at application | Unchanged, annotated "accepted — not applied: application error (effect …)" or "accepted — application outcome unknown (observer …)" | **Addition** |

Consequences for the hold machine (answering P §4.3's "how the hold machine
treats that is DEL-02-03's"):

- **MC-1** MX-7/MX-8 never re-hold the A5 arrival and never trigger its
  negative or mixed path: the person's decision was positive.
- **MC-2** The declared output is not produced for that item (WD §4.6).
  Checkpoints whose reached-when is that item's applied outcome never arrive
  for it; a checkpoint binding "objects changed by a named outcome" binds
  only the objects of items actually applied (WD-EX R-14).
- **MC-3** A re-draft (new proposal identity, P §5) that reaches *queued* is a
  **new arrival** of the A5 checkpoint (RW-4). No acceptance carries over.
- **MC-4** *Performed* at an A5 arrival does not wait for application;
  application is the host's lifecycle (HD-3).

**Receiving notes (R8-3, R8-5; INTEGRATION).** These apply in both phases,
because they concern what is recorded.

- **Staleness scope (R8-3, amending R2-13).** The App applies **per-item**
  staleness where the host supplies subject identities. Otherwise it receives
  and shows the **host's stated staleness scope**. For SWBPIPE that scope is
  the whole model: any model change stales every queued proposal (SQ-07
  (d)). The App never narrows a host's scope. De-duplication still runs
  first. On such a host, one application can make every other queued item
  leave (MX-6). The "refused — stale" annotations of MX-7 show the host's
  scope ("host scope: whole model"), and failing targets are *not supplied*.
- **Outcome mapping (R8-5).** A #885 `withdrawn` (the person cleared the
  queue) is an **item-left** event, "cleared by the person, no decision
  record". A `validation_rejected` at Apply is *refused — invalid* at
  application. Neither is ever A10 or A11. On SWBPIPE, **accept and apply
  are one step**, per batch, with no A10 record. The App keeps the meanings
  of MX-1…MX-8 and records the missing counterparts: accepted-then-stale
  (MX-7) and per-item A5/A10 mixes (MX-5) have no SWBPIPE counterpart.
- **Session undo (R8-5).** SWBPIPE's session undo writes no receipt. R2-15
  and R3-4 stand, "reverses ⟨receipt⟩" is *not supplied* for SWBPIPE, and a
  lapse caused by an undo is shown from the identity change (SP-4, R8-4).

### 4.12 Interruption, recovery and replay (REQ-002 "interrupted or replayed history")

**Principle (PROPOSED (W7)).** Arrival dispositions are a function of the
recorded events: arrivals, act records, A10 and item-left events,
act-declined, act-lapsed and supersession events, control relations,
run-resumed and run-ended events, and observation-lost and recovered events.
The executor's working state is disposable. Everything needed to rebuild it
is in the run record (DEL-04-03 R7–R9, R11) and in host evidence by reference.

| # | Rule |
|---|---|
| RP-1 **Recovery (same run).** | After an interruption the executor (a) rebuilds every arrival's disposition from the record; (b) re-observes before acting: host outcomes of dispatched calls (seek observation before any resubmission, LOOP R-d; a retry keeps the proposal identity, R2-13), acts captured since the last observation, lapse state of performed acts, A12 control relations; (c) records every recovered observation as a new event with its observation time and the source's evidenced time. Nothing is back-filled (P §4.1 rule 3) |
| RP-2 **Arrivals during interruption.** | An arrival whose event occurred while observation was lost is recorded on recovery with the event's own evidenced time. SP-6 compares against that time, so an act captured after the event but before recovery counts |
| RP-3 **Unknown.** | An arrival whose deciding observation stays lost is *unknown*. It may later become waiting, performed or resolved negatively on a recovered observation, recorded as a later event. It is never shown as performed meanwhile (S-K) |
| RP-4 **Held call after recovery** (governance phase; in Phase 1 no call is held, and RP-1 (b) applies to any dispatched call). | A kind (a) call held and performed but not yet dispatched is dispatched **unchanged from the record**. If its dispatch outcome is unknown, observation is sought first; it is never re-dispatched as a new call |
| RP-5 **Declaration source.** | Recovery and replay read the declaration of the **resolved revision recorded for the run**, never the library's current content (WD C-2; FB-08). If those bytes cannot be resolved, recorded dispositions are shown as recorded, marked "declaration not resolvable — reconstruction not verified", and, in the governance phase, the run stays holding |
| RP-6 **Inspection replay** (read-only, e.g. DEL-09-11) | Rebuilds the same arrival identities and dispositions from the same record. It issues no request, dispatches nothing and records no act. Lapse shown at inspection time is labelled with its evaluation time, separate from the dispositions at run end |
| RP-7 **Re-execution** | Running the workflow again is a new run (RE-3). It inherits no arrival or act |
| RP-8 **Order ambiguity** | Events whose relative order cannot be established from evidence are reported. An arrival decided only by such an order is *unknown* (§4.6 precedence) |

### 4.13 Several checkpoints and several arrivals

- **MA-1** Several checkpoints may have current arrivals at once. In the
  governance phase the run holds while any governed arrival is waiting
  (HD-1).
- **MA-2** Arrivals of the same checkpoint coexist unless one is replaced
  (MX-6). The panel shows each current arrival with its ordinal.
- **MA-3** An arrival produced by a run action taken during a hold (possible
  only where the hold is not enforced) is recorded as a separate arrival.
  In the governance phase, the action that produced it carries the "action
  during hold" limit. In Phase 1 it may carry "continued past ‹checkpoint›
  before ‹act›" (PH-7).

### 4.14 Invalid or not-established declarations

A checkpoint that is invalid (FB-03, FB-13, FB-16, R3-2; an A12 checkpoint
whose declaration names no setting content, R4-9) or not established
(FB-04) is reported and never evaluated. The machine creates no arrivals for
it, and it is never shown *not reached* as though valid. The compatibility
report shows it, so the person sees before the run that the checkpoint
cannot be observed or held. **Phase 1:** it is reported as a declaration
defect and does not change the check result (PH-3). The agent does not treat
it as satisfied, and manages the pause at its prose position as the plan
requires (PH-1). **Governance phase:** a governed invalid checkpoint gives HS-1
(§3.6) and the check *not established* (§3.5). The run does not proceed past
the prose position as though the checkpoint were satisfied (WD FB-13).

---

## 5. App-side act capture (resolves W7 hold: WD U-25; HOSTING §6.1 "standing as act evidence") — PROPOSED (W7); CAP-6 ADOPTED (R4-12); CAP-1 amended (R4-13)

The App interface is the capturing surface for acts **in the App** (WD I-5;
AP §4.5). This section is in force in both phases (§2.1 PH-4). This section states what makes App capture evidence, so that App
runs can reach *performed* truthfully.

| # | Requirement |
|---|---|
| CAP-1 **Scope.** | App capture applies to acts on **App content**: App project files and App-side outputs, bound by file content identity (RS L-1). It also covers A12 where an App control is the control that establishes the setting. Where A13 is captured App-side is set by DEL-04-01 (U-X1; R4-13). An App-side Codex configuration that an agent could write is **never** A13 evidence, and the host's refusal is the authoritative "off". It does **not** apply to acts on host content: those are captured by the host act facility (V4-HI-31), and the App faithfully records them citing the host's capture-evidence reference (U-05b; SQ-01). The App offers no proxy control for host-content acts in this increment (U-E9; SQ-25) |
| CAP-2 **Act control.** | A dedicated App control, operated by the person, for one act kind at a time. It presents: the act kind with the R-4 wording ("mark checked" for A4; "accept" only for A5; "approve" only for A6, engineering approval; "rely" for A7; "set grant" for A12); the bound subject with its content identity; the declared scope and purpose; the actor requirement; and the arrival it answers. The same control offers the **decline** that produces an act-declined event |
| CAP-3 **Direct capture record.** | Operating the control makes a human-act record with recording mode *direct capture* and a **capture-evidence reference** {act identity, actor, act kind, bound content identity with method designation, scope, purpose, time, capturing surface "App interface", arrival reference}. The record meaning is DEL-04-03's (RS §6) |
| CAP-4 **Not operable by automation.** | No agent tool, MCP operation, App rule or supplier request can operate the control or produce its record (D2; R-2). An agent may *request* the act (A8) |
| CAP-5 **Not capture evidence: tool permission.** | An A14 settlement from any origin (the person, the user's Codex mode, an App named-rule decline) is never act evidence (D3; R2-8) |
| CAP-6 **Not capture evidence: user-input and elicitation answers.** | Answers to supplier person-input requests (at 0.158.0 `item/tool/requestUserInput`, `mcpServer/elicitation/request`; HOSTING R9) are **input to the agent**, not act evidence, even when the person gives them. Their wording is authored by the agent or an MCP server, they cannot guarantee the kind/subject/scope/purpose binding of CAP-2, and their content goes to the agent. They are conversation (WD I-5). A question the agent asks this way may be an A8 request, if it names kind, subject and purpose. The App may respond by presenting its own CAP-2 control |
| CAP-7 **Not capture evidence: conversation.** | A chat statement ("I checked it") never satisfies (I-5; FB-15) |
| CAP-8 **Person identity.** | The record names the App's person identity. How the App identifies and verifies the person is `UNRESOLVED` (U-E8). A7's "accountable professional" is recorded as the person's own statement, with an evidence limit |
| CAP-9 **Presenting is not answering.** | Showing a CAP-2 control answers no pending supplier request. The outstanding-request register rules (HOSTING §6) are unaffected |

Construction of the control is DEL-01-04's (later undertaking, D1). App-side
positive capture cases are therefore **AWAITING INPUT** (CH-23).

---

## 6. Transfer and refinement trace (REQ-004, REQ-005; AC-004, AC-005; VER-004, VER-005; WD U-18)

### 6.1 Trace links (original and revised identities)

Each link is a separate fact with its own evidence. A match at one link
establishes nothing about another (WD §6.2; V4-EXM-14).

| Link | Fact | Identity carried | Evidence owner | Absent means |
|---|---|---|---|---|
| **listed** | A library reports the workflow | Tuple + holding library | App library (DEL-02-02); host library (external) | "not listed" |
| **selected** | The person (or brief) chose a full tuple | Tuple + holding library | DEL-02-02 (App); host panel (DEL-05-02, external) | "no selection" |
| **resolved** | The tuple resolved to package bytes whose recomputed content identity **equals the revision** (method-designated) | Tuple + holding library + verification result | Resolver (App: DEL-02-03 for runs and transfer; host: external) | "revision not verified"; never substitute (FB-08) |
| **exported** (transfer) | The resolved package and a **carriage manifest** (§6.3) were prepared for carriage | Source tuple | DEL-02-03 | "not exported" |
| **relayed** (transfer) | The files were carried to the destination (human relay, DEP-001) | Source tuple | The person / relay record | "relay not evidenced" |
| **received** (transfer) | The destination library listed the carried package | Original tuple unchanged (unadapted) + destination holding library | Destination library (host: relay evidence) | "receipt not observed" |
| **adapted** | A new revision was made in the destination | **Revised** tuple (host origin, new revision) + **derived-from** = original tuple | Host (external) | — |
| **opened / drafted / registered** (host→App) | Host workflow opened read-only; refined as a draft; registered after review | Host tuple → draft base → new App tuple with derived-from = host tuple | DEL-02-02 | "draft only — not a workflow identity" |
| **supplied** | These bytes were supplied to the agent or loop, per thread/turn, with source and content identity | Tuple and content identity | App: DEL-01-01 HOSTING §8.2 via DEL-02-04, with the **model destination per turn** as HOSTING §8.3 reports it: requested and effective kept separate, re-routes recorded with their turn, *unknown* for unobserved turns (R5-4; INTEGRATION (DECISION-2 reading); information only); host: loop run association (SQ-19 (a)) | **unknown** (R2-20; U-29) |
| **provider-adopted** | The model/harness took them up | — | Usually unobservable | **unknown** (supplied ≠ adopted) |
| **observed behavior** | What runs of this identity did | Run records naming the tuple; for App runs also the run-level **set** of destinations observed. A model switch starts no new run (R5-4) | DEL-04-03 (App); host run records (external; SQ-19 (b), (c)) | "no run observed" |

Every link records whether it concerns the **original** or the **revised**
identity. A trace never lets a revised identity inherit a link observed for
the original.

### 6.2 Holding library (resolves W7 hold: WD U-24; RS U-22; R2-20 "PROPOSED until W7")

**Confirmed as ruled in R2-20** (PROPOSED (W7) confirmed), with three
precisions:

- **HL-1** The holding library is recorded at *listed*, *selected* and
  *resolved*, shown beside the origin, and carried in the loop's run
  association. It never takes part in identity equality (WD C-6).
- **HL-2** In a transfer, the *received* link records the **destination**
  holding library and the *exported* link the **source** one. A move between
  libraries without a content change creates no new identity.
- **HL-3** It is not recorded at *supplied*. Supply is identified by tuple and
  content identity, and equal revisions mean equal content wherever held. If
  the bytes supplied do not match the resolved revision, that is a revision
  defect ("revision not verified"), not a holding-library fact.

### 6.3 App → host carriage procedure (SOW-054; REQ-004) — PROPOSED (W7)

| Step | Action (semantic) | Owner | Result or failure |
|---|---|---|---|
| TR-1 | The person selects a **registered** App workflow revision to carry. Drafts are not carried: a draft has no workflow identity (DEL-02-02) | Person; DEL-02-02 selection | Source tuple |
| TR-2 | Resolve and verify the package bytes (§6.1 *resolved*) | DEL-02-03 | "revision not verified" stops the transfer |
| TR-3 | Evaluate the compatibility report against the destination catalog if available (CK-4); otherwise record "destination catalog not available" | DEL-02-03 | Report reference |
| TR-4 | Prepare the **carriage manifest**: source tuple; revision content identity and method; declaration contract version; summary of required tool references and checkpoints (name, act kind, reached-when kind, subject class); compatibility report reference; exporter as observed (a Codex-seat exporter is *unverified*, R4-15); time; **transfer identity**. No model-destination restriction is carried or implied (D5, R4-1). The package's own declared part stays the authority (WD R-3); the manifest is a convenience and never overrides it | DEL-02-03 | *exported* |
| TR-5 | The person relays the package and manifest to the host (DEP-001: files human-relayed). No transport is selected | Person | *relayed* |
| TR-6 | The host lists the package, **unadapted**, with the original tuple and its own holding library. Whether the host can read the declared part at that contract version is its receiving capability (SQ-17 (a), (b), (d)) | Host (external) | *received*, or a §6.7 outcome |
| TR-7 | Adaptation, if any, by the host (§6.4) | Host (external) | *adapted* |
| TR-8 | Host evidence (listing, adaptation, runs) returns by relay to the App and to DEL-09-06 (SQ-18, SQ-19; RELAY §4 ledger) | Person; host | Evidence references |

### 6.4 Adaptation receiving (host side, receiving meaning)

- **AD-1** Adaptation creates a new identity: origin *host*, host source root,
  new revision, derived-from = the full original tuple (WD §6.4). The
  original's history is never edited.
- **AD-2 Adaptation difference.** The trace carries a comparison of original
  and adapted declared parts: inputs, required tool references, outputs and
  evidence, and each checkpoint's name, act kind, reached-when, subject class,
  scope, purpose and negative path. Each checkpoint is **preserved**,
  **changed** (listing the changed elements), **removed** or **added**.
- **AD-3** A removed checkpoint, or a changed act kind or subject class, is
  shown as "checkpoint meaning changed". It is not prevented: the host owner
  may adapt. It is never hidden (V4-EXM-14 "checkpoint identity").
- **AD-4 Checkpoint identity across adaptation.** The adapted workflow's
  checkpoints are new checkpoint identities {adapted tuple, name}. Where a
  name is kept, the trace records **derived-from checkpoint** ⟨original
  tuple, name⟩ with the AD-2 classification.
- **AD-5 No act inheritance.** Acts and dispositions from runs of the
  original never carry to runs of the adapted workflow, and the reverse is
  also true (REQ-005: never manufacture past checkpoint acts). Each run's
  replay uses its own resolved revision (RP-5).
- **AD-6** Selections of the original are never rebound to the adaptation
  (C-2). The host library may then show a collision (E4), reported with
  holding libraries.

### 6.5 Host → App opening and refinement (SOW-055; REQ-005) — PROPOSED (W7)

| Step | Action (semantic) | Owner | Identity |
|---|---|---|---|
| HR-1 | Host workflow files are relayed to the App and listed with origin *host*, the host source root, and the App-side holding library where the copy sits | Person; DEL-02-02 listing | Host tuple unchanged |
| HR-2 | Opening is read-only and keeps the host identity (WD §6.4) | DEL-02-02 | Host tuple |
| HR-3 | Refinement is a **draft** whose **draft base** is the host tuple. A draft is not a workflow identity and cannot be selected for a run | DEL-02-02 | — |
| HR-4 | The person reviews and registers it (V4-WF-02). Registration never overwrites silently | Person; DEL-02-02 | New tuple: origin *project* or *user*, new revision, derived-from = host tuple |
| HR-5 | Return to the host is an App→host carriage (§6.3) of the new tuple. Adaptation there creates another derived-from link | As §6.3 | Chain by following derived-from links |
| HR-6 | **History.** Host run records of the host identity (relayed) are referenced from the App trace under the **host** identity. They are displayed as history and never become acts or dispositions of App runs (AD-5). Interruption/revision/replay history is preserved by reference, not copied (V4-HI-71) | DEL-02-03 trace; DEL-04-03 | — |
| HR-7 | Same-name collisions in the App library expose every origin with its holding library and never rebind (C-1, C-2) | DEL-02-02 | — |

The changed-draft return path belongs to DEL-02-02 and is not compared in this
undertaking (D1); see finding F-12.

### 6.6 Derived-from chain

`derived-from` names only the immediate parent's full tuple (WD §6.1). The
lineage is reconstructed by following the links; a broken link (parent not
resolvable) is shown as "lineage incomplete at ‹tuple›", never guessed.

### 6.7 Transfer outcomes and failure behavior

| ID | Condition | Outcome |
|---|---|---|
| TF-1 | Relayed bytes do not recompute to the claimed revision | **revision not verified**; not listed as that revision |
| TF-2 | Relay incomplete or interrupted | **not received (incomplete)**; no partial listing or registration; a new attempt keeps the same source tuple and a new transfer identity |
| TF-3 | Host cannot receive workflows from outside its library, or cannot list another origin | **receiving capability unavailable** (explicit; REQ-004) |
| TF-4 | Host cannot read the declaration contract version | **declared part not established** at the destination; the host's required-tool check is not established, and so are its checkpoint holds (governance phase) (WD §3.4) |
| TF-5 | Destination catalog lacks required tools | Reported by the CK-4 report; carriage still possible |
| TF-6 | Host adaptation evidence not relayed | *adapted* link **not observed** |
| TF-7 | Host listing drops the original origin (lists it as host origin without derived-from) | **origin not preserved** — a trace defect (R-9), reported |
| TF-8 | App-side App reads a host workflow whose declared part is at a newer contract version | Listed; declared part **not established**; opening allowed |

---

## 7. Fixture cases on FX-PIPE-01 (OUT-003 design; none run)

All material is invented fixture subject matter.
- **From C-v0.4 §10** (FX-PIPE-01): FX-W1, g1, R-100, S-1…S-5, LC-1, Engineer
  A, OP-C1…OP-C12, T1…T17 (incl. T4a, T16a), Tg, B1/B2, PR-1/PR-2,
  RC-1…RC-3, fixture assumptions **FXA-1…FXA-5**, App-side subjects
  **LIB-A1** ⟨fx-proj⟩, **LIB-A2** ⟨fx-app-import⟩ and **AF-1**
  (⟨AF-1@f1⟩/⟨AF-1@f2⟩, ⟨m-fx-file⟩), editions e1/e2, and variants V-S1,
  V-CP1, V-NP1, V-R1, V-X1, V-OU1, V-ED1.
- **V-GR1** (C-v0.5 §10.4): run 13 of E1d on E. GR-1: `CP-grant` arrives
  at r15. GR-2: T15's A12 is captured after the arrival. GR-3: the held
  OP-C9 call is dispatched unchanged as T16. Sub-variants: GR-P (pending,
  then confirmation lost), GR-R (refused by the control), GR-S (a later
  established A12 narrows the scope).
- **From WD-EX-v0.4:** E1, E1b, E1c, E1d, E3–E8, and the E2 runs.
- ⟨rev-A2⟩/⟨rev-A3⟩ are DEL-02-03's workflow revision labels (C §10.1).

WD-EX local cases are cited **by content** (run name and step), with the
WD-EX-v0.4 label in brackets (R5-9). Retired EXEC local labels are not reused:
L-EXEC-5, L-EXEC-10, L-EXEC-16 and L-EXEC-19.

Case states: **DESIGNED**, **AWAITING INPUT** (named input), **HELD** (named
decision). "HS-n" names the §3.6 assignment row.

**Two-part reading (R8-1, R8-2; GV-5).** Each case gives its **Phase-1
result**, in which checkpoints are plan guidance: nothing is held, no
hold-support value is assigned, and acts are recorded only when performed.
It also gives its **governance-phase value** (retained), reading the case's
checkpoints as if declared `governed`. No fixture declares the flag. Where a
case has no checkpoint effect, the two are the same. Governance-phase values
on X apply SWBPIPE's SQ-02 answer (HS-3 (c)), as I2 Part 2 does.

### 7.1 Missing-tool (VER-001)

| Case | Input | Phase 1: expected report (required tools and channel state) | Governance phase (retained): hold support and result | State |
|---|---|---|---|---|
| MT-1 | E1 ⟨rev-3⟩ on surface E against FX-W1's edition (WD-EX E7 "Base") | OP-C1, OP-C3, OP-C4, OP-C5 **present**; OP-C12 (optional) **present**. **passes**; PS-2 wording; limitation "FXA-1 exposure assumed". `CP-accept` and `CP-check` listed as guidance; the host loop holds nothing (PH-2) | `CP-accept` and `CP-check` **enforced by the host loop** (HS-2); passes on hold support, subject to host evidence (SWBPIPE has no host loop, SQ-20) | DESIGNED |
| MT-2 | E1 ⟨rev-A2⟩ carried unadapted, App run on X (L-EXEC-1: App-side acting surface, which C §10 does not describe as a run) | Requirements as MT-1 on X (channel enabled, as the fixture assumes). CR-14 shows the destination selected at report time (information only). **passes**; `CP-accept` and `CP-check` listed as guidance; no *unsupported* for a hold reason (PH-3) | `CP-accept` **not enforceable** (HS-3 (c): SQ-02 answered 2026-09-28, route (iv)); `CP-check` **not enforceable** (HS-5, App-only run halt). **does not pass — unsupported** ("checkpoint hold not enforceable on this surface: CP-accept, CP-check"). The person may still start the run (CC-3) | DESIGNED |
| MT-3 | **Registered but missing**: ⟨rev-A2⟩ registered in LIB-A1; OP-C4 absent from the edition (WD-EX E7 "OP-C4 absent" [L-WDEX-13]) | Registration unchanged; OP-C4 **missing** with purpose line; does not pass; "registered ≠ compatible" (PS-3) | Same (no hold-support effect) | DESIGNED |
| MT-4 | L-EXEC-26: OP-C5 absent from the edition. Needed because WD-EX-v0.4 no longer has an OP-C5-absent case (its optional-absent case is OP-C12, [L-WDEX-13b]) | OP-C5 **missing**, optional; passes on requirements; fallback shown | Same | DESIGNED |
| MT-5 | E1c `supports-label` on X with C V-X1 (OP-C9 not exposed on X) | OP-C9 **not exposed on this surface** on X → does not pass on X; passes on E | Same on requirements. Also on X: `CP-check` **not enforceable** (HS-5) → *unsupported* | DESIGNED |
| MT-6 | Workflow requiring OP-C2 at r13 (C §10.6 T8; WD-EX E7 "C §10.6 (T8)" row) | **present, currently unavailable**, reason "No current solve for LC-1 at this revision", basis B2; passes as a run-time hold | Same | DESIGNED |
| MT-7 | L-EXEC-2: E1 declares OP-C1 v1; the edition carries OP-C1 **v2** (C §10.5 hypothetical); no compatibility statement. Needed because C has no version-mismatch entry | **version mismatch**; does not pass; limitation "equality only (U-C9; SQ-18 (d); SWBPIPE: no operation versions)" | Same | DESIGNED |
| MT-8 | L-EXEC-3: E1 variant adding a required harness capability "file writing". Needed because C covers host operations only | That reference **not established** (U-08); check **not established** | Same | DESIGNED |
| MT-9 | E5 `create-workflow` (undeclared) | **not established**; selectable; never "runnable" (PS-4) | Same | DESIGNED |
| MT-10 | E6 `project-dag` in a host seat without delegation | Required tools not established; workflow **unsupported** (delegation) → does not pass | Same | DESIGNED |
| MT-11 | L-EXEC-4: MT-1 passed on the current edition; at run time the loop's offered edition lacks OP-C5. Needed to separate report time from run time | Report unchanged; run records the loop-side **not offered** failure (CC-2) | Same | DESIGNED |
| MT-12 | C **V-ED1**: E1c checked on edition **e1** (no OP-C9), then the edition addition event e1 → e2 | e1 report: OP-C9 **missing**; does not pass. After the event, the e1 report is marked *not current* and a new e2 report passes (CK-3; CC-1) | Same on requirements (E1c's `CP-check` on X: HS-5 as MT-5) | DESIGNED |
| MT-13 | Workflow requiring OP-C11 (C V-NP1; WD-EX E7 "C V-NP1" row) | **present**; passes on requirements; dependent production **held** (CC-4) | Same | HELD (R2-9; `UNRESOLVED{OI-021}`) |
| MT-14 | External access off (WD-EX E7 "External access off" row; C §4.1 reporter per R4-16) | Surface-level **channel not enabled** on X, reported by the App (own configuration off) or the host (host channel off); never missing. (SWBPIPE: no A13 facility, SQ-28; `controller_unavailable` is *endpoint unavailable*, channel *disabled*, R8-6) | Same | DESIGNED |
| MT-15 | L-EXEC-6: E1d on X in an App run whose Codex mode auto-settles native tools, with `CP-grant` kind (a) declared on a harness capability instead of OP-C9. Needed to show HS-5 for R4-21; WD-EX E8 has the analogous [L-WDEX-15] | The harness-capability reference **not established** (EV-3; U-08) → check **not established**; `CP-grant` listed as guidance | `CP-grant` hold support **not enforceable** (HS-5); workflow **unsupported** → does not pass | DESIGNED |
| MT-16 | E1d from the App on X (WD-EX E8 row "E1d from the App via X"): `CP-grant` kind (a) on host operation OP-C9, **and** E1c's `CP-check` (A4, kind (c) on OP-C9 *applied*), which E1d inherits | OP-C9 **present**; **passes**; `CP-grant` and `CP-check` listed as guidance (PH-3) | `CP-grant` **not enforceable** (HS-3 (c): SQ-02 (d) answered No/No). `CP-check` **not enforceable** (HS-5: its only declared held action is the App-side return). Precedence (§3.5): **does not pass — unsupported** ("checkpoint hold not enforceable on this surface: CP-grant, CP-check") | DESIGNED (R6-1; R8) |

### 7.2 Checkpoints: recording (Phase 1) and hold (governance phase) (VER-002, VER-003)

"Same as record" means that the governance-phase dispositions and events
apply in Phase 1 as record labels (PH-6), with nothing held. Every Phase-1
entry assumes PH-2 (no hold), PH-4 (acts only when performed) and PH-7 (an
optional "continued past ‹checkpoint› before ‹act›").

| Case | Input | Phase 1 (R8-1): recorded, not enforced | Governance phase (retained) | State |
|---|---|---|---|---|
| CH-1 **Direct autonomy, no act** | E1c in the host (E); C T15 (⟨set-2⟩ direct for {S-4}) → T16 RC-2 | RC-2 applies. The `CP-check` arrival (kind (c), applied RC-2) is recorded on S-4 (post-application identity). Neither the App nor the host loop holds the run; the agent pauses as its plan says. The A4 is recorded only when T16a is performed | Direct application proceeds; `CP-check` arrival (kind (c), applied RC-2) **waiting** on S-4 (post-application identity); run holds (**enforced by the host loop**); nothing releases it without A4 (T16a then performs it) | DESIGNED |
| CH-2 **Unrelated success** | WD-EX R-1 (PR-2 queued, T10); L-EXEC-7: while `CP-accept` waits, OP-C12 host check and another run's RC-2 are observed. Needed because C has no concurrent-run step | No success, receipt or host check is recorded as the act (I-2; PH-4). The arrival stays unanswered in the record | `CP-accept` stays **waiting**; no success, receipt or host check changes it (I-2) | DESIGNED |
| CH-3 **Interruption while waiting** | L-EXEC-8: loop observation lost after T10; T11 A5 (item 1) and A10 (item 2) captured by the host during the loss; recovery. Needed because C has no loss at T10–T11 | Same as record: recovery rebuilds the record (RP-1). The T11 A5 and A10 are recorded at recovery with their host times, with no back-fill, giving *resolved negatively*, partial | On recovery (RP-1): arrival waiting, then T11 events recorded at recovery with their host times → **resolved negatively**, partial; no back-fill | DESIGNED |
| CH-4 **Lost deciding observation** | WD-EX R-6 "interruption before queue" [L-WDEX-3], then L-EXEC-9: *queued* observed later. Needed to show unknown → waiting | Same as record: *unknown*, then the recovered *queued* is recorded as a later event | **unknown**, then a later recovered event → **waiting**; the earlier *unknown* stays in history | DESIGNED |
| CH-5 **Inspection replay** | Record of WD-EX R-2 replayed read-only after E4 step 3 (⟨rev-4⟩ registered) | Same as record (replay is read-only in both phases) | Same arrival identities and dispositions; declaration read from ⟨rev-3⟩ (RP-5); no request or dispatch | DESIGNED |
| CH-6 **Lapse before resume** | WD-EX R-4 (i) "before the loop's resume point" [on L-WDEX-1] | Same as record: act-lapsed event recorded; label *waiting — lapsed at ‹t›* | Act-lapsed event; **waiting — lapsed at ‹t›** | DESIGNED |
| CH-7 **Lapse after resume → re-hold** | WD-EX R-4 (ii) "after resume, while the agent is writing `summary`" [on L-WDEX-1]: `CP-check` bound to S-5, R-100 and S-3, performed; Engineer A edits S-3 | Act-lapsed event recorded for S-3. `checked-rows` standing shown lapsed for S-3. The run is **not** re-held (PH-8). The agent re-requests A4 as its plan requires, and a new A4 over the current scope is recorded when performed. Later actions may carry "continued past CP-check before A4" | Act-lapsed event; **waiting — re-held, lapsed at ‹t› after resume**; run holds at its next action; `checked-rows` standing shown lapsed for S-3; the request covers the whole scope with S-3 marked; a new A4 over the whole current scope → **performed** (ordinal 2) | DESIGNED |
| CH-8 **Partial lapse, narrower act** | CH-7, then an A4 on S-3 only | Recorded and shown; the arrival is not answered by the narrower act until U-03 is ruled | Recorded and shown; arrival stays **waiting** | **HELD** on U-03 (U-E3) |
| CH-9 **Run ended while waiting; post-end act; continuation** | (i) WD-EX R-12b "run end and continuation" [continuation L-WDEX-9]. (ii) L-EXEC-11: an E1b run stopped after `CP-review` arrives at T4; Engineer A then marks S-2 and S-3 checked; a continuation run *continues ⟨run⟩* re-reads and re-examines, producing `findings`. Needed to show a continuation whose checkpoint does arrive | Same as record | (i) Run 12 `CP-check` final **waiting**; post-end A4 "after run end"; continuation `CP-check` *not reached* until its own arrival. (ii) Ended `CP-review` final **waiting**; the continuation's `CP-review` binds S-2 and S-3 as read; the post-end A4s are "prior act, not counted" (SP-6); new A4s → **performed** | DESIGNED |
| CH-10 **Lapse after run end** | WD-EX R-4 (iii) "after the run ended"; WD-EX R-17 (C T16a, T17) | Same as record | **lapsed** per referent (S-3; S-4 under FXA-2) | DESIGNED |
| CH-11 **Refused A12 (no policy basis)** | L-EXEC-12: workflow `renumber-with-grant` (fixture) whose `CP-grant` declares the setting content {OP-C11's class, *direct*, {FX-W1; R-100}}, kind (a) before dispatch of OP-C11; after arrival Engineer A performs that A12 (C V-NP1). Needed because C V-GR1 GR-R leaves the refusal reason open; this case fixes it as *no policy basis* (R2-9) | Control **refused (no policy basis)** is recorded; `CP-grant` is unanswered in the record ("A12 refused by control"). No call is held by the App or loop. The host's own treatment of OP-C11 governs (direct *not permitted*, R2-9). (a) act-declined → recorded *resolved negatively*; (b) run stopped → run-ended recorded | Control **refused (no policy basis)**; `CP-grant` **waiting** "A12 refused by control"; held call not dispatched; then (a) act-declined → **resolved negatively**, or (b) run stopped → final waiting | DESIGNED; production HELD (R2-9) |
| CH-12 **A12 after arrival (V-GR1); pending then established; C order** | (i) C **V-GR1** GR-1…GR-3. (ii) L-EXEC-13: V-GR1 with the control confirmation observed after a delay and then **established**. Needed because C's **GR-P** covers pending followed by a **lost** confirmation, not by establishment. (iii) C main order: T15's A12 precedes the arrival at T16 (WD-EX R-16 (i); V-GR1 "main-order negative") | (i) T15's A12 (captured after the r15 arrival, established ⟨set-2⟩) is recorded as answering `CP-grant`, and the OP-C9 dispatch as T16 is recorded; no call was held. (ii) Pending, then established, recorded as observed. (iii) T15's A12 is recorded as a **prior act, not counted** (SP-6), and `CP-grant` stays unanswered in the record | (i) `CP-grant` **performed** by T15's A12 (captured after the r15 arrival, established ⟨set-2⟩); held OP-C9 call dispatched unchanged as T16. (ii) **waiting** "A12 awaiting control confirmation", then **performed**. GR-P itself: *waiting*, then **unknown**. (iii) T15's A12 is a **prior act, not counted** (SP-6, R5-7); `CP-grant` **waiting** for a new A12 on the declared content, even though ⟨set-2⟩ is already in force. This is the owner-visible cost under U-E4 | DESIGNED |
| CH-13 **Refused A12 does not supersede** | (i) C **GR-R** (refused at arrival: ⟨set-1⟩ stays in force). (ii) L-EXEC-14: after CH-12 (i) (performed, ⟨set-2⟩ in force), Engineer A performs a later A12 on overlapping classes that the control refuses. Needed because GR-R's refusal comes before any performance; this case shows a refusal **after** performance | Same as record: the refused A12 is recorded; it establishes nothing and supersedes nothing (R4-6) | (i) `CP-grant` **waiting** "A12 refused by control"; ⟨set-1⟩ not superseded. (ii) ⟨set-2⟩ stays in force, not superseded; `CP-grant` stays **performed** (R4-6) | DESIGNED |
| CH-14 **A12 supersession** | C **GR-S** (= WD-EX R-16 (iii)) | Same as record | **performed**, then "superseded by ‹later A12›"; not lapsed; no re-hold (RH-9) | DESIGNED |
| CH-15 **Mixed items** | LOOP FX-C5 / WD-EX R-2 (T11) | Same as record (MX-5) | MX-5: **resolved negatively**, partial (item 1 A5); on-mixed path: continue with item 1 | DESIGNED |
| CH-16 **Item left** | LOOP FX-C12 | Same as record (MX-4) | MX-4: **performed** over item 1; item 2 shown with item-left event; never "all accepted" | DESIGNED |
| CH-17 **All items left, re-draft** | L-EXEC-15: after T10, Engineer A edits S-3 before any decision; the host refuses both PR-2 items stale (item-left); the agent re-drafts a new proposal (local label L-EXEC-15-P, lineage PR-2), queued. Needed because WD-EX R-7b "all items left, replaced" [L-WDEX-16] uses A11 withdrawal, not stale refusal | Same as record (MX-6); no acceptance carried | Arrival 2 **waiting** "no items remain", closed "replaced by arrival 3"; arrival 3 waiting on L-EXEC-15-P items; no acceptance carried. (Fixture per-item staleness; on a whole-model host such as SWBPIPE any model change stales every queued item, R8-3) | DESIGNED |
| CH-18 **Accepted then stale** | C **V-S1** (= WD-EX R-14 "accepted, then stale") | Same as record (MX-7) | MX-7: disposition unchanged; item 1 annotated with both bases; `CP-check` not reached for item 1's objects | DESIGNED |
| CH-19 **Unknown item decision** | WD-EX R-6b "lost decision" [L-WDEX-4] | Same as record (MX-3) | MX-3: **unknown**; never performed or resolved negatively until item 2 is observed | DESIGNED |
| CH-20 **Prior act not counted** | WD-EX R-9b "prior act" [E1b variant L-WDEX-7]: T2's A4 on S-2 precedes `CP-review`'s arrival at T4 | Same as record: S-2's T2 A4 is shown as a prior act, not counted (SP-6) | S-2's T2 A4 shown "prior act, not counted"; waiting until A4 on S-2 and S-3 after T4 (then WD-EX R-E1b → performed) | DESIGNED (SP-6 PROPOSED; U-E4) |
| CH-21 **Held call across recovery** | LOOP FX-C8 variant L-EXEC-17: A4 performed on S-3 at B2; interruption before dispatch | No call is held (PH-2). On recovery, observation of any dispatched OP-C5 call is sought before any resubmission (RP-1 (b)). Nothing is dispatched on the machine's behalf | Recovery dispatches the same held OP-C5 call unchanged from the record; if its outcome is unknown, observation is sought and there is no new call (RP-4) | DESIGNED |
| CH-22 **App-side hold, not enforced** | L-EXEC-18: App run of E1 ⟨rev-A2⟩ on X; `CP-check` kind (b). In the same turn that produces `examination-report`, Codex also writes a file and calls OP-C1. Then the person sends a new message on the holding run. Needed because C describes no App-run turn | The arrival is recorded. Nothing is held and no hold is claimed. The person's turn is not blocked. The file write, the OP-C1 call and any agent action in the person's turn may carry "continued past CP-check before A4" (PH-7). There is no *unsupported*, and HP-3 and HP-4 are not used | Arrival **waiting**; hold support **not enforceable** (HS-5). HP-4: the App starts nothing further; the person's turn is **not blocked** and is carried with initiator *person-directed*. No interruption is relied on (HP-2 not adopted). The file write, the OP-C1 call, and any governed agent action in the person's turn are recorded as **action during hold**. HP-3 declines any permission request that reaches the App (origin in R13). No hold is claimed | DESIGNED |
| CH-23 **App-side capture** | C **AF-1** (App file in LIB-A1's project, ⟨AF-1@f1⟩): App-side workflow with an A4 checkpoint on AF-1. (i) The agent asks through a user-input request and the person answers "yes". (ii) The person marks AF-1 checked in the App act control (CAP-2). (iii) AF-1 is then edited to ⟨AF-1@f2⟩ | (i) Conversation; not an act (CAP-6). (ii) Direct capture → A4 recorded as performed (AWAITING INPUT, as governance). (iii) Act-lapsed event recorded (PH-8). No hold-support value | (i) Conversation; **waiting** (CAP-6). (ii) Direct capture with a capture-evidence reference, bound to ⟨AF-1@f1⟩ with ⟨m-fx-file⟩ → **performed**. (iii) Act-lapsed event; the RH/R2-19 sequence applies. Hold support **not enforceable** (HS-5, App content) | (i), (iii) DESIGNED; (ii) AWAITING INPUT (DEL-01-04 control; U-E8) |
| CH-24 **Subject absent** | L-EXEC-20: after CH-7's performance, S-5 is deleted before resume | Same as record: *subject absent* | Act lapsed (subject absent); **waiting "subject absent"**; only an act-declined event or run end closes it | DESIGNED (U-E7) |
| CH-25 **Tool permission during hold** | WD-EX R-15 "tool permission (App)" during a hold, plus HP-3 | A14 changes nothing in the record (S-R). HP-3 is not used | A14 changes no disposition; an App named-rule decline, if used, is recorded with truthful origin in R13 only | DESIGNED |
| CH-26 **Invalid declarations** | LOOP FX-C13; WD VC-29 variants | Reported invalid / not established as a declaration defect; no arrival recorded; the requirement-check result is **unchanged** by it (PH-3; R8-2) | Reported invalid / not established; no arrival; no hold-support value (HS-1); check **not established** | DESIGNED |
| CH-27 **Constraint forced proposal** | C V-CP1 / LOOP FX-C9 / WD VC-11; over X also ADAPTER XF-25/XF-26 | No constraint is carried or enforced by the App (R2-12 carriage assurance is governance phase). The agent, following the declaration as plan guidance (I-7), submits OP-C4 as a proposal and never adds a field the host schema lacks (R8-10). If a direct request is made, the host's own treatment decides and the outcome is recorded as observed; the App reports nothing as *not permitted* on the constraint's account. The Phase-1 standing of I-7 / V4-HI-42 is U-E24 | As those cases. Over X: **not enforceable** → unsupported (SQ-02 answered 2026-09-28: no host-held route; HS-3 (c); R5-1, R5-2, R8-2). *Enforced on the host route* would need an evidenced host-held route. If a call is dispatched with the constraint omitted, "omitted governing checkpoint constraint" is recorded (R11) | Phase 1 DESIGNED. Governance phase: over X DESIGNED (value determined); on E **AWAITING INPUT** (U-E13) — SQ-20 answered 2026-09-28: no host loop (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3) |
| CH-28 **Host capture reference absent** | WD-EX R-9 (iii) | Same as record: the act is not recorded as performed without the reference (I-5; PH-4) | **waiting** (I-5) | DESIGNED; host side **AWAITING INPUT** (SQ-01; U-05b) — SQ-01 answered 2026-09-28: no capture-evidence reference; the Apply receipt names no person or time and does not survive restart (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3) |
| CH-29 **A12 checkpoint naming no setting** | L-EXEC-25: E1d variant whose `CP-grant` declaration states no classes, grant value or scope; an A8 presents ⟨set-2⟩ at arrival. Needed for R5-3 | Reported **invalid**, unconditionally (the A8 does not supply the subject, R5-3); no arrival recorded; the requirement-check result is unchanged by it (PH-3) | Checkpoint **invalid**, unconditionally: the A8 does not supply the subject (R5-3). Reported before the run; never evaluated; check **not established** (HS-1) | DESIGNED |
| CH-30 **Person's undo re-holds; never an A5** | (i) L-EXEC-27: C T16a then T17 with E1c, but the run is still live and past its resume point when Engineer A undoes RC-2 (OP-C10 → RC-3). Needed because C's R-17 reading has the run already ended. (ii) L-EXEC-28: run 12 after WD-EX R-3; after resume Engineer A undoes the L-WDEX-1 receipt. Needed to show an undo against an A5 arrival | (i) The act-lapsed event is recorded (T16a's A4, ⟨S-4⟩ changed); the undo is recorded as the person's R7 operation; nothing re-holds (PH-8). (ii) `CP-accept`'s A5 stays recorded as performed (R2-15; RH-9); `CP-check`'s acts on S-5/S-3 are recorded lapsed, S-5 as subject absent | (i) T16a's A4 lapses (⟨S-4⟩ changed, FXA-2) → `CP-check` **waiting — re-held, lapsed at ‹t› after resume**. The undo is recorded as the person's R7 operation, **not** as action during hold (RH-8; R5-5, R5-6). (ii) `CP-accept` stays **performed**: A5 on the reversed items does not lapse (R2-15; RH-9). `CP-check`'s acts on S-5/S-3 lapse, S-5 as subject absent → re-held | DESIGNED |

### 7.3 Round trip (VER-004, VER-005)

| Case | Input | Expected trace | State |
|---|---|---|---|
| RT-1 **App→host unadapted** | E3 "carried unadapted": ⟨rev-A2⟩ exported with manifest, relayed, listed in ⟨fx-root⟩ | Links selected → resolved (verified) → exported → relayed → received; origin *project* kept; holding library LIB-A1 ⟨fx-proj⟩ at export and ⟨fx-root⟩ at receipt; no "App-origin" | DESIGNED (test double); host side **AWAITING INPUT** (SQ-17) — SQ-17 answered 2026-09-28: no workflow library or declaration reader (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3) |
| RT-2 **Adaptation preserving checkpoints** | E3 adapted ⟨rev-3⟩ | New host tuple, derived-from ⟨rev-A2⟩ tuple; AD-2: `spacing-limit` necessity changed; `CP-accept` and `CP-check` **preserved** (FXA-5), each with derived-from checkpoint | DESIGNED; host side **AWAITING INPUT** (SQ-18 (b), (c)) — SQ-18 answered 2026-09-28: no host workflows, no adaptation; operation intents carry no version (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3) |
| RT-3 **Adaptation changing a checkpoint** | L-EXEC-21: host variant ⟨rev-3x⟩ that removes `CP-check` and changes `CP-accept`'s on-negative path. Needed because E3 preserves all checkpoints | AD-2: `CP-check` **removed**, `CP-accept` **changed** (on negative decision); "checkpoint meaning changed" shown; not blocked | DESIGNED |
| RT-4 **Unsupported receiving capability** | L-EXEC-22: host library that cannot list a *project*-origin workflow (TF-3), and a variant that cannot read the declaration contract version (TF-4). Needed because C describes no receiving capability | TF-3: **receiving capability unavailable**. TF-4: listed; declared part **not established**; required-tool check **not established**, and so are holds (governance phase) | DESIGNED; host side **AWAITING INPUT** (SQ-17 (a), (b)) — SQ-17 answered 2026-09-28: no workflow library or declaration reader (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3) |
| RT-5 **Supplied / adopted / observed** | Run 12 on ⟨rev-3⟩ (C §10.1) in the host; an App run of ⟨rev-A2⟩ with a model switch between turns 2 and 3 (L-EXEC-29, needed for R5-4's per-turn rule) | Host: *supplied* **unknown** without a per-turn record; adopted **unknown**; observed from the run record. App: *supplied* from HOSTING §8.2 evidence; destination recorded per turn (requested and effective separate; any `model/rerouted` with its turn), e.g. a cloud model, with no gate. The run-level value is the set of both destinations, with no new run. Adopted **unknown** | DESIGNED; host **AWAITING INPUT** (SQ-19 (a), (b); U-29) — SQ-19 answered 2026-09-28: no host loop; its "run records" are solver analysis runs (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3) |
| RT-6 **Host→App refinement** | E3 last column: ⟨rev-3⟩ relayed to the App and held in C **LIB-A2** ⟨fx-app-import⟩; opened; draft with base ⟨rev-3⟩; registered in **LIB-A1** as ⟨rev-A3⟩ | Opening keeps host tuple; draft is not selectable; registration gives origin *project*, derived-from ⟨rev-3⟩ tuple; lineage ⟨rev-A3⟩ → ⟨rev-3⟩ → ⟨rev-A2⟩; holding library LIB-A2 at listing, LIB-A1 after registration | DESIGNED; registration is DEL-02-02's (later) |
| RT-7 **Collision without rebinding** | E4 steps 1–4; plus ⟨rev-A3⟩ registration while ⟨rev-A2⟩ holds the name in LIB-A1 | All origins with holding libraries; no rebinding; no silent overwrite (slot policy DEL-02-02, U-10) | DESIGNED |
| RT-8 **History preserved, no act inheritance** | RT-6 with run 12's history (T10–T13 `CP-accept` arrivals) | App trace references run 12 under the host tuple; a run of ⟨rev-A3⟩ starts with every checkpoint **not reached**; no act imported | DESIGNED |
| RT-9 **Revision mismatch** | L-EXEC-23: relayed files whose recomputed content identity ≠ ⟨rev-3⟩ | **revision not verified**; not listed as ⟨rev-3⟩ (TF-1) | DESIGNED |
| RT-10 **Interrupted relay** | L-EXEC-24: package partially relayed | **not received (incomplete)**; no registration; retry with a new transfer identity (TF-2) | DESIGNED |
| RT-11 **Evidence account for DEL-09-06** | All MT/CH/RT cases, joined by CA W14 cases: W14-01 ← RT-1; W14-02 ← RT-2, RT-3; W14-03 ← MT-1, MT-2, MT-3, MT-10, MT-15, MT-16; W14-04 ← CH-1, CH-27; W14-05 ← CH-2, CH-23, CH-28; W14-06 ← CH-6…CH-10, CH-30; W14-07 ← CH-3…CH-5, CH-21; W14-08 ← RT-5; W14-09 ← RT-6, RT-8; W14-10 ← RT-7 | Inventory with candidate and source versions, case states, labels (C mapping), limitations and missing external inputs (SQ IDs as cited per case); names DEL-09-06 as joined-witness owner; claims no witness | DESIGNED |

---

## 8. Resolution register for items held for W7

| Held item (sources) | Resolution | Section | Standing at v0.2 |
|---|---|---|---|
| Re-hold after a lapse following resume (WD U-22; AP U-10; RS U-24; AS U-13; LOOP C-4, FX-C3; PANEL W-5e, PC-20) | Same arrival re-held: "waiting — re-held, lapsed at ‹t› after resume"; hold at next action boundary; history kept; whole-scope request; ended while re-held → waiting | §4.2 HD-5, §4.7 | **ADOPTED (R4-3)**; partial-lapse satisfaction **carried** on U-03 (C1) |
| Resumption of an ended run; post-end acts (WD U-21; AP U-10, §2.3; RS U-23; AS U-11; LOOP §2.4.1, FX-C7b; PANEL W-5b, PC-21d; WD-EX R-12b) | No resumption; ended dispositions final (except R2-19 lapse); post-end acts shown "after run end"; continuation is a new run *continues ⟨run⟩* with nothing inherited; interruption ≠ run end | §4.9 | **ADOPTED (R4-4)**, standing PROPOSED |
| Refused A12 at a checkpoint (WD U-27, SB-4; AP U-13, §12.5; RS U-17; AS U-14; LOOP C-8, FX-C11; PANEL W-5g) | Refused → does not count, stays waiting with refusal shown; pending → waiting; unconfirmed → unknown; refused A12 does not supersede; declared setting content always binds (R5-3); A12 after arrival per V-GR1 (R5-7) | §4.10 | **ADOPTED (R4-6; R5-3)** |
| Confirmation of WD §4.3.7, mixed items and accepted-then-stale (WD U-20; R2-18; R3-3; AP U-09; RS U-18; AS U-09; P §4.3; LOOP C-7; PANEL W-5f) | **Confirmed**, with MX-3 (unknown item), MX-6 (replaced empty arrival), MX-8 (application error / unknown after A5) and MC-1…MC-4 | §4.11 | **CONFIRMED; additions ADOPTED (R4-7)** |
| Holding library (WD U-24; RS U-22; R2-20 "PROPOSED until W7"; LOOP §2.1; PANEL §3.2) | **Confirmed** as R2-20, plus HL-2 (source/destination at transfer) and HL-3 (not at *supplied*) | §6.2 | Confirmed; carried into RS by R4-11 (transfer links) |
| App-side capture (WD U-25; HOSTING §6.1, R9 "standing as act evidence") | CAP-1…CAP-9; user-input and elicitation answers are **not** act evidence; A13 locus per DEL-04-01; App control construction and person identity carried | §5 | CAP-6 **ADOPTED (R4-12)**; CAP-1 per **R4-13**; rest PROPOSED (W7); construction **carried** (DEL-01-04, later; U-E8) |
| Transfer/adaptation procedure (WD U-18) | TR-1…TR-8, AD-1…AD-6, HR-1…HR-7, TF-1…TF-8; model destination recorded, never gated (R4-1) | §6 | PROPOSED (W7); destination per turn (R5-4); host links AWAITING INPUT (SQ-17…SQ-19) |
| Hold machine (WD §4.3.4 "DEL-02-03's (W7)"; §9 A-4; LOOP §10.1) | §4. **Phase 1:** recording only (§2.1). **Governance phase (retained):** the hold machine (§2.2) | §2.1, §2.2, §4 | Disposition logic PROPOSED (W7), with R4-3…R4-7 and R5-5 adopted. Hold-support values per R5-1 (§3.6), governance phase. App-side enforcement: D6 **closed for Phase 1** (DECISION-4; R8-2), re-opens with the governance phase. SQ-02 answered (route (iv)) for host-operation checkpoints (R5-10). Host placement `UNRESOLVED{OI-013}` (SQ-20: not decided; D-58 successor a SWBPIPE owner decision), sharing `UNRESOLVED{OI-014}` |
| ADAPTER U-X3 (retired to `UNRESOLVED{D6}`): GC-3 constraint assurance, GC-5 kind (a) on X | Governance phase: GC-3 and GC-5 follow §3.6 HS-3. SQ-02 was answered 2026-09-28 with no host-held route, so → *not enforceable* (HS-3 (c)); *enforced on the host route* only with host-held carriage or a host hold evidenced | §3.6 | **Resolved** (R5-1, R5-2, R8); host side answered: none |
| Multi-row A4 purpose after partial lapse, point of need "before DEL-02-03 re-hold design" (WD U-05c; AP U-03; RS U-07; CA DI-7) | Not decided here (owner DEL-04-01 with the Owner). Carried: whole-scope request satisfies under every option; narrower-act variant HELD | §4.7 | **Carried** to C1 (R4) |
| Version ordering, point of need "before DEL-02-03 required-tool fixtures" (WD U-07; C U-C9) | Equality only; MT-7 expects *version mismatch* | §3.4 EV-6 | **Carried** (SQ-18 (d)) |
| Harness capability names, point of need "before App-side required-tool check" (WD U-08) | *not established* until named; kind (a) on them not holdable (R4-21) | §3.4 EV-3; §3.6 | **Carried** |
| Constraint receipt, point of need "before W7 host-side fixtures" (WD U-19; P U-P10) | Phase 1: no constraint carried by the App (R8-1). Governance phase: CH-27 over X *not enforceable* (SQ-02 answered: no receipt, no host copy; a constraint field is refused as unknown); on E AWAITING INPUT per STD-2 | §7.2 | **Answered** (SQ-02: none); governance phase |

---

## 9. Interfaces

### 9.1 Expected from suppliers

| Supplier | Element | State | Used in |
|---|---|---|---|
| DEL-02-01 (WD) | Declared-part status; required tool reference elements; §4.2.4 vocabulary and pass rule (with the R4-8 reason); checkpoint elements, validity rules (with R5-3, R4-21), I-1…I-8, dispositions, §4.3.7 (with R4-7), §4.3.8 hold support (R5-1); identity tuple, chain, holding library, §6.4; WD-EX E1–E8 and E2 runs | WD-v0.4 and WD-EX-v0.4 read at `8fb51f07f`; WD-EX-v0.5 E1c/E1d/E8 read in the working tree (R6); WD-v0.5 rulings relayed by the coordinator. R8: WD-v0.6 adds the Phase-1 statement and the optional **`governed`** flag (PROPOSED) after this file in the same A1 pass; sibling to confirm | §2.1, §2.2, §3, §4, §6, §7 |
| DEL-03-01 (C) | Catalog edition; entry identity/version (equality); exposure element 9; availability and reason; §4.1 results (App reporter of *channel not enabled*, R4-16); subject content identity; FX-PIPE-01 with FXA-1…FXA-5, LIB-A1, LIB-A2, AF-1, e1/e2, V-ED1, **V-GR1** with GR-P/GR-R/GR-S | C-v0.4 read at `8fb51f07f`; C-v0.5 §10.4 V-GR1 read in the working tree (R6) | §3, §4.5, §7 |
| DEL-03-02 (P) | Per-item dispositions; item-left events; all-items-decided; change-item content identity; applied outcome with resulting objects; stale and application-error outcomes; retry precedence; governing checkpoint constraint with **carriage assurance** (R5-2: host-held only in this increment); author identity possibly *unverified* (R4-15) | P-v0.4 read | §3.6, §4.4, §4.11, §4.12 |
| DEL-04-01 (ACT) | A1–A14; closed list; act-declined event; A12 binding and supersession (R4-6); grant-setting subject (R5-3); A13 capture locus (U-X1; R4-13); person's own operations as R7 entries (R5-6); U-03 ruling (pending) | ACT-v0.4 read | §4.5, §4.7, §4.10, §5 |
| DEL-04-02 (AS) | Grant display states incl. *set by person, not yet confirmed*, *unconfirmed*, *refused (reason)* | AS-v0.4 read | §4.10 |
| DEL-04-03 (RS) | Human-act record, recording mode, capture-evidence reference; events; lapse rules; R5 model destination per turn (R5-4); R7 for the person's own operations (R5-6); R8 with the R4-10/R4-11 additions; R11 action during hold | RS-v0.4 read | §4, §5, §6 |
| DEL-05-01 (LOOP) | Arrival observation (§2.4.1), binding (§2.4.2), events (§2.3), hold support in host loops (§2.4.4), dispatch record and own constraint evaluation (§6.2), retry rules (§6.3) | LOOP-v0.4 read | §3.6, §4 |
| DEL-01-01 (HOSTING) | Supplied-guidance evidence (§8.2); observed model destination per turn incl. `model/rerouted` (§8.3); request kinds and R9 (R4-12); HP-4 scope ruling from F-22 (INTEGRATION), closing HOSTING U-25 | HOSTING-v0.4 read; v0.5 F-22/U-25 read in the working tree | §2, §5, §6.1 |
| DEL-03-03 (ADAPTER) | Carriage assurance; GC-1…GC-5; §7.7 checkpoint observation on X; model destination in channel status | ADAPTER-v0.2 read; ADAPTER-v0.3 F-18/F-19 (GC-3/GC-5, XF-26 alignment) relayed by the coordinator | §3.6, CH-22, CH-27 |
| DEL-01-04 (later, D1) | App act control (CAP-2) and person identity | Not in this undertaking | §5 |
| DEL-02-02 (later, D1) | Listing, selection, draft, review, registration, slot policy | Not in this undertaking | §6.5 |
| Host owner (DEP-001), via DEL-09-06 RELAY-v0.2 | SQ-01 capture-evidence reference; SQ-02 constraint receipt and host holds (decides host-operation checkpoints only, R5-10; governance phase); SQ-04/SQ-05 first operation; SQ-11 exposure; SQ-17 receiving App workflows; SQ-18 adaptation, library identity, version statements; SQ-19 run records and supplied guidance; SQ-20 host placement; SQ-25 proxy control | Relayed; answered 2026-09-28; no commitment or contribution (RELAY §4). Answers are about SWBPIPE's current state: SQ-01 no capture-evidence reference; SQ-02 route (iv), none planned; SQ-11 no exposure element; SQ-17…SQ-19 no workflow library, adaptation, host loop or seat; SQ-20 not decided; SQ-25 host facility only, no proxy. Host joins deferred (DECISION-3) | §2, §3.6, §4, §6 |

### 9.2 Provided to receivers

| Receiver | Provided | Expected check at next comparison |
|---|---|---|
| DEL-02-01 | §2.1 Phase-1 statement (PH-1…PH-10); §2.2 governance-phase scope and the `governed` opt-in (GV-1…GV-5); the R5-1 hold-support value set and HS-1…HS-5 as governance phase (for WD §4.3.8 and WD-EX E8); §3.5 check result and precedence; R5-3 subject rule; SP-6 (R4-5, PROPOSED); AD-2 checkpoint comparison | WD/WD-EX v0.6: checkpoint guidance in Phase 1; `governed` flag with its meaning per phase; §4.2.4 R4-8 reason limited to governed checkpoints in the governance phase; VC-37, VC-43 and E8 two-part, with the same governance-phase values as MT-2, MT-15, MT-16 |
| DEL-05-01 | Phase 1: the host's embedded loop enforces no hold (PH-2). Governance phase: hold-machine semantics (§4) for host loops; the value *enforced by the host loop*; RH-8/RH-9 undo rules | LOOP §2.4.4 relabelled governance phase (R8-8); uses the R5-1 set; C-4 per RH-8 |
| DEL-04-03 | Record needs, adopted by R4-10/R4-11; per-turn destination (R5-4); person's own operations as R7 (R5-6); RS E10/VC-17 corrected by R5-8 | RS v0.5 matches §3.6, §4 and §6 |
| DEL-03-03 | Governance phase: hold-support values for X (§3.6 HS-3…HS-5; SQ-02 answered → HS-3 (c)); CH-22/CH-27 expectations in two parts | ADAPTER v0.4 GC-3, GC-5, §7.7, XF-25, XF-26 use the R5-1 set as governance phase |
| DEL-09-06 | Transfer trace (§6.1), carriage manifest meaning (§6.3), fixture design and the RT-11 W14 map; SQ citations per host item; F-17 closed for Phase 1 with D6 (R8-2) | CA v0.4: W14-03/W14-04 in two parts, matching MT-2 and MT-16 (Phase 1 passes; governance phase *unsupported*) |
| DEL-05-02, DEL-04-02 | Display meanings of the §4.3 annotations, §3.3 report and hold-support values | PANEL W-5b/e/f/g and AS §4 re-pointed |

---

## 10. Excluded acts and owners (REQ-006; AC-006)

| Excluded act | Owner | Interface here |
|---|---|---|
| Declaration and shared-allocation design | DEL-02-01 | §3.2, §4 consume |
| Review, registration, selection policy, drafts | DEL-02-02 (later, D1) | §6.5 routes |
| Catalog semantics | DEL-03-01 | §3.2 |
| Proposal and outcome semantics | DEL-03-02 | §4.11 |
| Operation-policy definition; adopted D2/D3 carriage; U-03 | DEL-04-01; the Owner for U-03 | §4.5, §4.7 |
| Record format, writer and reader | DEL-04-03 | §4, §5 needs |
| Host-loop receiving design | DEL-05-01 | §9.2 |
| External adapter construction; carriage realization | DEL-03-03 | §3.6 (carriage assurance, R4-14) |
| App act control construction | DEL-01-04 (later, D1) | §5 |
| Joined round-trip witness and external contribution record | DEL-09-06 | RT-11 |
| Host catalog, library, loop, panel, act facility, receipts, run records | External SWBPIPE owner (DEP-001) | §6.3 TR-6…TR-8 |
| Every human act (A4–A7, A10, A12, A13), professional reliance, review and registration decisions, relay of files | The person; the accountable professional | Never performed or inferred here |
| OI-013, OI-014, OI-021, App v4 OI-003 decisions | Their owners | UNRESOLVED |

Nothing here promotes a carrier into a decision actor, or implies an external
commitment (VER-006).

---

## 11. Findings

### 11.1 v0.1 findings and their R4/R5 disposition

| # | Where | Finding (v0.1, condensed) | Disposition |
|---|---|---|---|
| F-1 | WD §4.3.7, U-20 | Missing rows: unknown item decision, empty-subject closure, application error or unknown after A5 | Closed: R4-7 |
| F-2 | WD I-4; AP §4.3; RS L-12; AS §4; LOOP C-4; PANEL W-5e | After-resume branch deferred; interim display conflicted | Closed: R4-3 |
| F-3 | WD I-1; AP §4.2/§4.5; LOOP C-2, FX-C4; WD-EX R-16 | No rule relating capture time to arrival | R4-5 adopts SP-6 as PROPOSED; U-E4 open; FX-C4 and R-16 repaired by their owners |
| F-4 | WD U-21; AP §2.3; RS; LOOP; PANEL | Resumption deferral; continuation link missing | Closed: R4-4 |
| F-5 | AP §2.5; RS L-0; LOOP; PANEL W-5g | A refused later A12 would supersede | Closed: R4-6 |
| F-6 | RS R8; AS §4 | R3-1 class missing | Closed: R4-10 |
| F-7 | RS §3, R8, R11 | Record elements missing | Closed: R4-11 |
| F-8 | WD §4.2.4 | No *unsupported* reason for a checkpoint hold | Closed: R4-8 |
| F-9 | HOSTING §6.1, R9 | Elicitation standing undefined | Closed: R4-12 |
| F-10 | SoW REQ-002 vs CLM-003 | No App hold point allocated | **Carried to C1** as a SoW gap; home `UNRESOLVED{D6}` (R4-2). R8: Phase 1 needs no App hold point (PH-2); the gap belongs to the governance phase (F-29) |
| F-11 | SoW TBD-001/002; DEP-02-03-015/016 | OI-001/002 still called open | **Carried to C1** |
| F-12 | CASE-002 M1 DEL-02-02 row | Changed-draft return uncompared | **Carried to C1** (out-of-scope receiver, D1) |
| F-13 | AP §4.2 | Grant-setting referent undefined without A8 | Closed: R4-9 |
| F-14 | WD U-05c / AP U-03 | Point of need reached without ruling | **Carried to C1** as an open owner question (R4); U-E3 |
| F-15 | C §10 | No App-file subject or App library | Closed: C-v0.4 LIB-A1, LIB-A2, AF-1 (R4-20); re-pointed in v0.3 (R5-9) |
| F-16 | WD §4.3.1 kind (a) on harness capability | Not holdable in App runs | Closed: R4-21 |

### 11.2 v0.2 findings and their R5 disposition

| # | Finding (v0.2, condensed) | Disposition |
|---|---|---|
| F-17 | With D6 deferred, App-run checkpoints not covered by a host hold are *not enforceable* and the workflow *unsupported* | **Restated under R5-10.** SQ-02 can move only **host-operation** checkpoints (HS-3). App-only checkpointed workflows (HS-5; e.g. E1 `CP-check` in an App run, anything on AF-1) stay *not enforceable*, and so *unsupported*, **whatever SWBPIPE answers**. This is a separate D6 follow-up for the owner (U-E23). **R8 (v0.4): closed for Phase 1** by DECISION-4: checkpoints are guidance, and no workflow is *unsupported* for hold reasons (PH-3). It re-opens with D6 when the governance phase is taken up (R8-2) |
| F-18 | App-assured carriage needs HP-1, which is not adopted | Closed: R5-2 ("App-assured: not available in this increment") |
| F-19 | CA W14-04 (i) depends wholly on SQ-02 | Unchanged; consistent with HS-3 and MT-16. R8: SQ-02 answered (route (iv)); governance phase HS-3 (c) → *not enforceable*; Phase 1 unaffected |
| F-20 | C lacked R4-20 subjects | Closed: C-v0.4 LIB-A1/LIB-A2/AF-1 cited (R5-9) |
| F-21 | Model destination per run vs per turn | Closed: R5-4 |

### 11.3 New findings at v0.3

| # | Where | Finding | Proposed change |
|---|---|---|---|
| F-22 | R5-1 value table | Invalid or not-established declarations had no stated value | Closed: R6-1 confirms HS-1 (no value; check *not established*) |
| F-23 | R5-7 cost; CH-12 (iii) | Under SP-6 on C's main order, the person must repeat an A12 whose content (⟨set-2⟩) is already in force. The repeat is a new A12 on identical content: it supersedes the earlier one (R4-6), and the record shows two acts for one setting. This is visible friction every time a grant precedes its checkpoint | For the owner with U-E4. If SP-6 stays, DEL-04-02/DEL-05-02 may present the repeat as "re-affirm current setting". That is presentation only, and it remains an A12 |
| F-24 | RS R11 "action during hold"; HP-4 person-directed turns | An agent action in a person-directed turn is recorded as *action during hold* (HP-4 ruling). The record should show the turn's initiator, so that a governed action the person asked for in their own message is distinguishable from one the agent took unprompted. Neither changes the disposition | DEL-04-03: the R11 action-during-hold entry carries the turn initiator (HOSTING supplies *person-directed*) |
| F-25 | WD-EX-v0.4 E7 | No "optional host operation absent" case remains for OP-C5; EXEC added L-EXEC-26 | WD-EX may adopt it as a shared case, or keep the OP-C12 case as the single optional-absent example |
| F-26 | C-v0.4 at `8fb51f07f` | V-GR1 was not yet in C | Closed (R6-4): C-v0.5 §10.4 has V-GR1; CH-12…CH-14 verified against it, and the L-EXEC-13/14 reasons re-pointed to GR-P/GR-R |
| F-27 | R5-1 "enforced by the host loop" row | The value "passes" on hold support, but LOOP-v0.4 §2.4.4 still distinguishes a residual after-observation limit for kinds (b)/(c) in host loops (a turn already streaming when the loop observes the arrival). R5-1 retires "held after observation" as a value | LOOP §2.4.4 records that residual as an evidence limit (R11), not as a separate value; EXEC CR-12 lists it as a limitation |
| F-28 (R6) | WD §4.3.1 checkpoint elements; WD-EX E1c | R6-1 classifies checkpoints by **held actions**, but the declaration has no element that names them. EXEC derives them from the prose position and later steps. E1c declares no host operation after `CP-check`, so it is App-side by the conservative HS-5 default. A workflow meant to be enforceable from the App cannot currently *declare* that its held actions are host operations only | DEL-02-01: consider a declared **held actions** statement per checkpoint (or "holds: host operations only"), so that HS-3 vs HS-5 can be read from the declaration rather than inferred |

### 11.4 New findings at v0.4 (R8)

| # | Where | Finding | Proposed change |
|---|---|---|---|
| F-29 | SoW REQ-002, REQ-003, AC-002 ("keeps it waiting until evidence shows that required act actually occurred"); §1 E-B; §4.7 "Why re-hold" | The DEL-02-03 SoW wording assumes the run waits at a checkpoint. Under R8-1 that is governance phase. In Phase 1 the run is not held, and only the "not recorded as done until performed" half applies | Flag with V4-WF-05's first half for the next accepted-basis update: the SoW acceptance for Phase 1 would read "the act is not recorded as done until evidence shows it occurred" (PH-4), with the waiting clause phased to the governance layer. No SoW text is changed here |
| F-30 | WD I-7; V4-HI-42; DECISION-1 D2 "No autonomy grant widens past … a declared checkpoint"; CH-27 | R8-1 phases R2-12 carriage assurance but does not say whether I-7 (an acceptance checkpoint forces a proposal) and D2's checkpoint clause bind in Phase 1 as agent guidance only or also as host obligations | U-E24 for the integrator or the owner. Meanwhile CH-27's Phase-1 entry treats I-7 as plan guidance, with the host's own treatment governing |
| F-31 | §2.1 PH-6, PH-8 | R8-1 retains "the hold machine (HD states, re-hold, lapse)" as governance phase and lets arrival and act be recorded. It does not say whether an act's **lapse** is recorded in Phase 1, or whether disposition words may label the record | PH-6 and PH-8 are marked PROPOSED (A1): lapse recording is kept because V4-REC-05 requires acts to lapse visibly; re-hold is governance phase. For the integrator to confirm or amend |

---

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| U-E1 App-side run holds `UNRESOLVED{D6}` (DECISION-2). **Closed for Phase 1** by DECISION-4 D4-1: checkpoints are guidance, with no App or host-loop hold (R8-2). **Re-opens only when the governance phase is taken up.** For host-operation checkpoints, SWBPIPE answered **SQ-02** on 2026-09-28: route (iv), none planned (R5-10). HP-1 and HP-2 not adopted (R4-2) | The owner (DECISION-4; D6 re-opens with the governance phase); then App/shared owners (OI-014) | When the governance phase is taken up for a workflow that needs it; before any App-side positive hold case; before the App fixes its realization family | Phase 1: none (PH-2, PH-3). Governance phase: HS-3 values *not enforceable* against SWBPIPE (SQ-02 answered: none); HS-5 *not enforceable* |
| U-E23 **App-only checkpoints in App runs** (HS-5): *not enforceable* whatever SQ-02 returns (R5-10; F-17). **Re-pointed to D6 (U-E1):** closed for Phase 1, re-opens with the governance phase (R8-2) | The owner, with D6 | Before any **governed** checkpoint with any App-side held action (including an App-content checkpoint) is offered as enforced in App runs | Phase 1: none; such workflows are not *unsupported* for hold reasons (PH-3). Governance phase: such workflows are *unsupported*; runs remain possible (CC-3) with action during hold recorded |
| U-E2 Host placement of the hold machine and required-tool check `UNRESOLVED{OI-013}` / `{OI-014}` | Shared contract owner with SWB implementation owner (SQ-20); App/shared owners. SWBPIPE's successor embedded mechanism is owner decision D-58 (SQ-20, SQ-29) | Before shared/host implementation boundary contracts | Semantics supplied; no placement. SWBPIPE: not decided (SQ-20) |
| U-E3 Multi-row A4 purpose after partial lapse (WD U-05c; AP U-03; CA DI-7) | DEL-04-01 with the Owner (C1 carry) | Before re-hold and lapse fixtures run | Whole-scope request; CH-8 HELD |
| U-E4 Arrival-order rule SP-6 versus counting a prior act on current content (R4-5 keeps it open). Owner-visible cost (R5-7): the person may repeat a grant change whose content is already in force (CH-12 (iii); F-23) | The owner, with DEL-02-01 and DEL-04-01 | Before hold-machine fixtures run | SP-6 applied as ADOPTED (R4-5), standing PROPOSED |
| U-E7 "On subject absent" path in the declaration | DEL-02-01 | Next comparison | Waiting "subject absent" |
| U-E8 App person identity scheme; App act control construction | DEL-01-04 (later, D1) with DEL-04-03 | Before App capture fixtures | CH-23 (ii) AWAITING INPUT |
| U-E9 Person-attributed acts on host content through the App (proxy control) | Host owner (DEP-001), **SQ-25** (answered) | Before any App proxy is offered | None offered. SWBPIPE: host facility only, no proxy (SQ-25) |
| U-E10 Harness capability names (WD U-08) | DEL-02-01 with DEL-01-01 | Before App-side required-tool check | *not established*; not holdable (R4-21) |
| U-E11 Version compatibility statements (C U-C9; WD U-07) | Host owner with DEL-02-01, **SQ-18 (d)** (answered: no; no operation versions) | Before version fixtures against a real host | Equality only |
| U-E12 Host capture-evidence reference (WD U-05b; AP U-04a) | SWBPIPE owner decision (PB-TBD-002 acceptance-record storage; DEL-16-03 actor identity; ANS §2). SQ-01 answered: none | Before host act-recording integration | No host-content act can be recorded as performed (PH-4) |
| U-E13 Constraint receipt on the host route (WD U-19; P U-P10) — governance phase | Host owner with DEL-03-02; **SQ-02** answered 2026-09-28: route (iv), none; a constraint field would be refused as unknown (SQ-02 (a)). Planning a route is a SWBPIPE owner decision | Before CH-27's governance-phase host case | Phase 1: no constraint carried by the App; the agent never adds fields the host schema lacks (R8-10). Governance phase: **AWAITING INPUT** — SQ-02 answered: no receipt, no host copy (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3) |
| U-E14 Host library receipt of other origins, adaptation evidence with derived-from, holding library and run records (TR-6…TR-8) | SWBPIPE owner decision (a work item to receive App workflows; ANS §4). **SQ-17, SQ-18, SQ-19** answered: none | Before RT host-side cases | RT host links AWAITING INPUT (STD-2 annotations) |
| U-E15 Per-turn supplied guidance in host loops (WD U-29; LOOP Q-4) | Host owner, **SQ-19 (a)** (answered: no host loop; the D-58 successor is a SWBPIPE owner decision) | Before host supplied-link evidence | *supplied* **unknown** |
| U-E16 Physical carriage of the declared part (WD U-01) and carriage-manifest representation; revision algorithm (WD U-03) | DEL-02-01 with DEL-04-03; TBD-003 | Before OUT-002 schema and transfer code | All semantic; verification uses method designations |
| U-E17 First connected operation `UNRESOLVED{OI-021}` | Owner via outside SWB session with App/shared owner, **SQ-04, SQ-05** | Before connected-activity SoW | FX-PIPE-01 only; MT-13, CH-11 production HELD |
| U-E18 Extension promise `UNRESOLVED{OI-003}` (App v4 OI-003, the extension promise; unrelated to SWBPIPE's OI-003) and real exposure (C U-C7; WD U-23) | Owner with host contract owner; exposure **SQ-11** (answered: no exposure element; only `position.x` on X) | Before exposure claims | FXA-1 fixture assumption; unagreed exposure → HS-4 *not established* (governance phase), except where SQ-02 is answered with no host-held route, as for SWBPIPE (R8-2) |
| U-E19 Selection slot policy and host precedence (WD U-10); registration as an act (AP U-08) | DEL-02-02 (later) with DEL-02-01, DEL-04-01 | Before host-origin discovery in the App | RT-6/RT-7 registration side not exercised |
| U-E24 Phase-1 standing of WD I-7 (an acceptance checkpoint forces a proposal), V4-HI-42 and DECISION-1 D2's "or a declared checkpoint" clause: agent guidance only, or also a host obligation (F-30) | Integrator (R8 follow-up), with the owner if D2's reading is affected | Before any Phase-1 case relies on a host refusing a direct request because of a checkpoint | CH-27 Phase 1 treats I-7 as plan guidance, with the host's own treatment governing; the reserved acts themselves stand (PH-5) |
| U-E25 Per-subject content identity (V4-HI-32) not met by SWBPIPE, which supplies only a whole-model identity (SQ-03; R8-4) | SWBPIPE (PB-TBD-002 / DEL-16-03); owner notice | Before host act-binding integration | SP-4 receives the whole-model identity for every covered subject: over-lapse, never under-lapse; resulting objects beyond target ids *not supplied* |

Changed at v0.4 (R8): U-E1 closed for Phase 1 (re-opens with the governance phase); U-E23 re-pointed to it. Closed at v0.2: U-E5 (R4-9), U-E6 (R4-6). Withdrawn at v0.2: U-E20 (nothing relies on `turn/interrupt`, R4-2). Closed at v0.3: U-E21 (C-v0.4 AF-1, LIB-A1, LIB-A2; R5-9), U-E22 (per-turn destination, R5-4). HOSTING U-25 is closed by the HP-4 scope ruling (§2).

## Verification cases

Designed, **not run**. No code, fixture runner, host or act exists. Labels use
C's evidence mapping; all current states are DESIGNED, AWAITING INPUT or HELD.

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-E-01 Report completeness and outcomes | MT-1…MT-16 against §3.3, §3.4, §3.5 | Every CR element present, incl. CR-14 at report time as information only; each outcome distinct; three-valued check result with precedence; PS-2 wording; registered ≠ compatible (MT-3) | VER-001 (AC-001) |
| VC-E-02 Checkpoint under direct autonomy | CH-1, CH-2, CH-27 | Phase 1: the arrival is recorded, nothing is held, and no success, receipt, grant or host check is recorded as the act; CH-27 carries no constraint. Governance phase: waiting persists and nothing releases it; CH-27 per HS-3 (c) (SQ-02 answered) | VER-002 (AC-002) |
| VC-E-03 Interruption and replay | CH-3, CH-4, CH-5, CH-21 | Same arrival identities; recovered events not back-filled; unknown never performed; held call dispatched unchanged; replay issues nothing | VER-002 (AC-002) |
| VC-E-04 Lapse, re-hold and finality | CH-6…CH-10, CH-24, CH-30 | R2-19 before resume; re-hold after resume (R4-3; governance phase; Phase 1: lapse recorded, no re-hold, PH-8) for any cause, including the person's undo, which is never *action during hold* (R5-5); undo never re-holds A5; ended runs final and continuation inherits nothing (R4-4); subject-absent path | VER-002, VER-003 |
| VC-E-05 Act evidence and fabrication negatives | CH-20, CH-23, CH-25, CH-26, CH-28; WD VC-21/VC-22 | Only SP-satisfying acts count; conversation, elicitation answers (R4-12), A14, agent records and prior acts (R4-5) do not; decision actor ≠ recorder; AF-1 file binding with method designation | VER-003 (AC-003) |
| VC-E-06 A5 item rules | CH-15…CH-19 | MX-1…MX-8 and MC-1…MC-4 as tabulated (R4-7); never "all accepted" over a reduced subject | VER-003 |
| VC-E-07 A12 rules | CH-11…CH-14, CH-29 | V-GR1: A12 after arrival performs; T15 before arrival is not counted (R5-7); refused → waiting; pending → waiting; refused never supersedes (R4-6); declared content always binds, and naming none is invalid even with an A8 (R5-3); supersession not lapse | VER-003 |
| VC-E-08 App→host trace | RT-1…RT-5, RT-9, RT-10 | Original and revised identities kept apart; links separate; derived-from correct; holding library per HL-1…HL-3 with LIB-A1; unsupported receiving explicit; destination per turn, run-level set, no gate (R5-4); host links AWAITING INPUT with SQ IDs | VER-004 (AC-004) |
| VC-E-09 Host→App refinement | RT-6…RT-8 | Host identity kept on opening (LIB-A2); draft not selectable; registered identity in LIB-A1 derived from the host tuple; no rebinding or overwrite; history referenced, no act imported | VER-005 (AC-005) |
| VC-E-10 Ownership and open items | §2, §8, §10, UNRESOLVED against SoW CLM-001…003, REQ-006/007, TBD-001…005, DEP-001, DECISION-2, DECISION-3, DECISION-4, R5, R8 | Every excluded act has an owner; every held item resolved or carried with owner, point of need and SQ ID where host-dependent; no external commitment or joined qualification claimed | VER-006 (AC-006) |
| VC-E-11 Evidence account | RT-11 inventory for this file (EXEC-v0.4) and its source versions; W14 map | Candidate and source identities listed; states truthful; DEL-09-06 named as joined-witness owner; no witness claimed | VER-007 (AC-007) |
| VC-E-12 Hold support (R5-1) — governance phase | MT-1, MT-2, MT-15, MT-16, CH-1, CH-22, CH-23, CH-26, CH-27, CH-29 (governance-phase columns) against §2.2, §2.3, §3.5, §3.6 | Only the four R5-1 values appear, and only for checkpoints read as governed; each **valid** checkpoint gets exactly one value by held actions per HS-2…HS-5 (invalid: HS-1, no value); E1c/E1d `CP-check` *not enforceable* in App runs; MT-16 *unsupported*; *enforced on the host route* is never assumed; retired values appear nowhere; HP-1/HP-2 never enforce; HP-3/HP-4 are best effort; a person-directed turn is not blocked and its governed agent actions are *action during hold*; model-supplied carriage → *not enforceable* after SQ-02, *not established* before; SWBPIPE's SQ-02 answer gives HS-3 (c) and HS-4 does not mask it (R8-2) | VER-002, VER-006 |
| VC-E-13 Phase-1 semantics (R8-1) | MT-1…MT-16 and CH-1…CH-30 (Phase-1 columns) against §2.1 PH-1…PH-10 | No hold-support value and no *unsupported* for a hold reason appear; results depend on required tools and channel state (with role and delegation); no App or host-loop hold, block or re-hold; acts recorded only when the person performs them, never by an agent on the person's behalf; reserved acts remain the person's, with host refusals recorded as observed; arrivals and acts appear as observation; "continued past ‹checkpoint› before ‹act›" is optional and never a defect; a `governed` flag changes nothing in Phase 1 | VER-001, VER-002, VER-003, VER-006 |

Limit: passing these later would show local contract and fixture conformance
only. It would establish no host implementation, round-trip execution,
provider adoption or human act (SoW VER-007; AX-002).
