# Workflow execution compatibility, checkpoint hold and round trip
- Contribution: DEL-02-03/EXEC-v0.6 (supersedes DEL-02-03/EXEC-v0.5, last changed at `c896a99d90`, file sha256 3711c55c36e4a5b637012512ee7baa856b094b3fdd48823b697feb9cb139405f; EXEC-v0.4, last changed at `f5ceef164`, file sha256 092f248682447df74e93915527930f4b90367fac46b867dad18daef3c5c608ff; EXEC-v0.3, last changed at `c6f81a4f2` and unchanged at `bcc25624d`, file sha256 03b2fd48e14dd21ee6f29bc8e5e19221a771f788aa6c1482810b8bc0671d61e2; EXEC-v0.2 at `cc58211c5`, sha256 7f7848c0de2fdb4dc21f5adafa97f92e179bb66c9f6b04f3434d8f2342317af0; EXEC-v0.1 at `e20a3ae8d`, sha256 e0ede76ebf08003511755afc666be2466a867fd3256837ee94300cd0dfe518e8)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted. Beside it (v0.6): two PROPOSED schemas with valid and invalid example instances (`compatibility-report.schema.json`, `checkpoint-record-entries.schema.json`) and a design prototype in `prototype/` (not product code; R12-3)
- Serves: OUT-001 (required-tool check and checkpoint receiving behavior — definition only, no product code; a design prototype of the check and of the current-phase recorder ran locally, §7.4), OUT-002 (App/host transfer and adaptation contract), OUT-003 (missing-tool, checkpoint and round-trip fixture design — none run); REQ-001…REQ-007; AC-001…AC-007 through designed VER-001…VER-007
- Phase (R9-1; PRD V4-WF-05 and HOST_INTEGRATION V4-HI-42 as amended by SCA-V4-001; SoW REQ-002 and AC-002 as revised; §2.1): when a run reaches a declared checkpoint, the required human act is requested, and it is recorded as done only when the person performs it, whatever the autonomy setting. Holding the run at the checkpoint until the act is performed is phased to the governance layer: in the current phase (Phase 1) a checkpoint is plan guidance that the person and the agents manage, and neither the App nor a host's embedded loop enforces a hold, blocks a run, or reports a workflow unsupported because a hold cannot be enforced. The reserved acts (V4-HI-30) still bind. The hold machine and hold support are kept as the **governance-phase definition (retained)** (§2.2).
- Basis: the accepted basis as amended by SCA-V4-001 (`_ScopeChange/SCA-V4-001_2026-09-28_2155/`) and SCA-V4-002 (`_ScopeChange/SCA-V4-002_2026-09-29_1901/`), at its current bytes (R9-5): `P/docs/PRD.md` sha256 bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd; `P/docs/ARCHITECTURE.md` sha256 317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c; `P/docs/HOST_INTEGRATION.md` sha256 d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f; `P/docs/EXAMINATION.md` sha256 471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0 (the v0.1–v0.4 passes read these four at repo 6e18505e3, before the amendments). ScopeOfWork.md sha256 0006521b9bd96ea7ec98ecc5d9e6db794ecb331440c276006b444e7ee319726d (revised by SCA-V4-001: the Purpose first sentence, the SOW-052 row, OUT-003, CLM-002, CLM-003, REQ-002, REQ-006, AC-002, AC-007, VER-002, the REQ-002 matrix evidence cell, TBD-001 and TBD-002, with TBD-006 and AX-004 added; and by SCA-V4-002: CLM-002, with AX-005 added; the v0.1–v0.4 passes read sha256 9a921ba500271c441e64db2e1f34acf41c95fa7821d6dff3d8659352bb4db7fb). Requirements relied on: `P/docs/PRD.md` V4-WF-01…06, V4-AUT-03, V4-AUT-05, V4-EXE-01, V4-EXE-03, V4-REC-03, V4-REC-05; `P/docs/HOST_INTEGRATION.md` V4-HI-02, -04, -23, -25, -30…32, -40…42, -50…52, -70/71; `P/docs/EXAMINATION.md` V4-EXM-14, V4-EXM-22; `P/docs/ARCHITECTURE.md` V4-ARC-20/21; SCC-CASE-002 `Case_Datasheet.md` current sha256 a12abfaf82c34ae1e7c10d8b553d3e1a0da4772b160e02257c0bf70edce04d5c (M1 rows naming DEL-02-03 as producer and receiver; read by the earlier passes at sha256 6acdc6c4e484ab7b46ba7d45a347961bc69b3e624bd29ef58a613ec6c66a71a6, since when only successor-observation sections were added and no line was removed); owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (OWNER_DECISIONS.md sha256 f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e) D1–D4; owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (OWNER_DECISIONS.md at `f05c7e4cd`, sha256 a9869129…8ad2c) D5, D6; owner decisions `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3` and `-DECISION-4` with its clarification (OWNER_DECISIONS.md current sha256 5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2, which also holds DECISION-5 and its confirmation; read for v0.4 at `bcc25624d`, sha256 a5ccab0d39bd1cab37c5556abc9bdedd5341ce76be4712706c8c9d72d623e776): host joins deferred (D3); D4-1 phased checkpoints; the owner's confirmation of the R8-11 item 2 reading of D2's "or a declared checkpoint" (`APP-V4-BASIS-ALIGN-20260928` DECISION-7, accepting OWNER_ITEMS O-25 "as recommended"; OWNER_DECISIONS.md sha256 ca8c4e50df1d7dddb41b875a4afe46eea4f1a1bf2491d255b7890d0d71cd254b)
- Consumed inputs:
  - **v0.6 inputs (Wave B, node B2 of run `APP-V4-DESIGN-PASS-2-20260930`; design development).** Each sha256 recomputed with `shasum -a 256` in the working tree at this node; paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/`: `R12_RESOLUTIONS.md` sha256 95f3011b436b6faa3de098059e77eac836c165e0bb98a5ed94e28918a3a749a1 (R12-1…R12-4, R12-10; binding); `BRIEFS.md` sha256 ccb4d9f036fb7ff531fffa0d309533b15cf1ebb39b0320651ed4bd5d88efc550 ("Common rules", "Wave B", row B2); `SURVEY/S1-C.md` sha256 5b60dd41a8c269902a9b360bf4cdc7c8106c464564bcc2fc1623948661c7eaa0 (§C.2, §C.5, §C.6, §C.8 items 5–9; advice, each item checked against the current text first); `OWNER_DECISIONS.md` current sha256 1dfd5bf4619b329719136b1646030e3f871fd7ffc52dbfd12265414e515aaf15 (DECISION-K1 unchanged from the A4 pin below; the file has since added the owner's model-download answer for OBS-1); R10 and R11 at the sha256 pinned below (R10-8; R11-9); `reviews/V17-A.md` (N-4) and `reviews/V17-B.md` (n-5), read for R12-10. Supplier facts at pin 0.158.0, read only in the committed generated bundles (`observed-in-generated-types`; none observed live): `DEL-01-01…/Design/generated/0.158.0/json-schema/experimental/codex_app_server_protocol.v2.schemas.json` sha256 34f28a486d00fbd20e5da0b0da3422d1d6e20ec897d12b31408f87499198f458 (ThreadItem variants; item, turn and status types) and `codex_app_server_protocol.schemas.json` sha256 aa5cb3fbcdebf833515fb42cd085a0670eb755d461037a0ad67bb72a709dcd0f (server-notification method names). Siblings by Wave A label and section (R9-5), read in the working tree at this node, while nodes B1, B3, B4, B6 and B9 edit their own files in parallel (joins are returned, not edited): HOSTING-BOUNDARY-v0.7 §6.7, §6.8, §8, §8.3, §10; PIN-SPIKE-v0.1 §4, §5; LOOP-v0.7 §2.4.0, §2.4.1; ADAPTER-v0.5 §2, §4.1, §7.7, §8, §9; WD-v0.7 §4.2, §4.3.1, §4.3.4–§4.3.6, §4.4; WD-EX-v0.7 E1, E1b–E1d, E5–E8; RS-v0.7 §3, §4, §6, §7; C-v0.7 §10.
  - **Current pins of this run's records (node A4 of run `APP-V4-DESIGN-PASS-2-20260930`; in place, no version bump; R11-3).** Each sha256 recomputed with `shasum -a 256` in the working tree at this pass; paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/`: `R9_RESOLUTIONS.md` sha256 a64e241519b7d158165a7ede0ffdd22eec0af15b6812b5300755f5f38abd59b8 (R9-1…R9-11; R9-2's second bullet as corrected by R10-1); `R10_RESOLUTIONS.md` sha256 ad3b6caa4a12660db77abc51b5c02ba70519ee46d55b40d21ee76eb3ca561796 (R10-1…R10-11); `R11_RESOLUTIONS.md` sha256 e7343b6663b6aeeb2dc506d3391f5b310088e7688d1b21e65d2ba1d8616b3615 (R11-1…R11-9, the repairs from review V17); `OWNER_DECISIONS.md` sha256 7458e9e81971676337a34280b4e8b29a7d04fce5fc202da5b9f5cf7ccd8f9ae5 (DECISION-K1). These supersede for currency the earlier pins of the same records in this header and in the change-table rows, which record the bytes read at node A1 or A3.
  - **v0.5 inputs (Wave A alignment; run `APP-V4-DESIGN-PASS-2-20260930`, node A1-C).** R9_RESOLUTIONS.md sha256 c3efe2ffa232dd9293202d4fc891eba4325afeb2e224fecdf8c1b4c5122a9d2c (R9-1…R9-11; binding). BRIEFS.md sha256 698d91d8217cee528812529fa353faac899b4bc1a5be5686552ad88dad6c469a ("Common rules", "A1 — alignment wave"). SURVEY/S1-C.md sha256 5b60dd41a8c269902a9b360bf4cdc7c8106c464564bcc2fc1623948661c7eaa0 (advice; each item was checked against its current source before editing). `reviews/V6.md` of `APP-V4-FIRST-INCREMENT-20260928` (m-7), under R9-8. Rulings in force: R1–R7 by file in `APP-V4-FIRST-INCREMENT-20260928/` (hashes in the bullets below; R7_RESOLUTIONS.md sha256 1f6ab3b2355e164f803657ceae08841af92d21a821feede3800a6df861b2a1ea) and R8_RESOLUTIONS.md at its current sha256 44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b (R8-1…R8-13; R8-13 changes nothing in this file). `_DAG/_LATEST.md` → DAG-003 (accepted 2026-09-29; `DAG-003/HANDOFF_STATE.md` read first; held candidate arcs are non-gating; satisfaction is read from the local `Dependencies.csv` and `_DEPENDENCIES.md`). SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` at its current sha256 afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74: SWBPIPE revised three lines at `a999f4ba1` after the R8 pass read 6f01add3…61c7 (the integrity-standing list under SQ-04, the evaluated-basis sentence of the outcome vocabulary, and the T9 source under SQ-27); none changes a statement this file makes. They remain data about SWBPIPE's current state, not commitments (DECISION-3). Sibling Design files are cited by version label and section only (R9-5); their byte pins are in GUIDE's input table alone. Wave A labels (R9-11): DEL-02-01/WD-v0.7; DEL-02-01/WD-EX-v0.7; DEL-03-01/C-v0.7; DEL-03-02/P-v0.7; DEL-03-03/ADAPTER-v0.5; DEL-03-04/GUIDE-v0.4; DEL-04-01/ACT-POLICY-v0.7; DEL-04-02/AS-v0.7; DEL-04-03/RS-v0.7; DEL-05-01/LOOP-v0.7; DEL-05-02/PANEL-v0.7; DEL-01-01/HOSTING-BOUNDARY-v0.7; DEL-01-01/PIN-SPIKE-v0.1; DEL-09-06/CA-v0.5; DEL-09-09/XT-v0.5; DEL-09-06/RELAY-v0.3. **Read at this pass:** WD-v0.6 whole, then as edited to WD-v0.7 in the same node (§4.2.4, §4.3.0, §4.3.1, §4.3.3); WD-EX whole; and, for the findings closed from records, RS §4 R11, LOOP §2.4.4 and ADAPTER §7.7 in the working tree (no sibling byte is pinned here). The bullets below are kept as the records of their passes.
  - **R8-12 closing pass (node A6; in place, no version bump).** R8_RESOLUTIONS.md sha256 d4c3423310a857af86692d17ddfdd22fa877ee20b07c46e1ee481d1cd750e7af (R8-12, items 1 and 7 applied here). Current sibling versions after R8, as committed at `7a1508452` with A6's in-place R8-12 edits (their byte pins are in GUIDE-v0.3's input table): DEL-02-01/WD-v0.6; DEL-02-01/WD-EX-v0.6; DEL-03-01/C-v0.6; DEL-03-02/P-v0.6; DEL-03-03/ADAPTER-v0.4; DEL-03-04/GUIDE-v0.3; DEL-04-01/ACT-POLICY-v0.6; DEL-04-02/AS-v0.6; DEL-04-03/RS-v0.6; DEL-05-01/LOOP-v0.6; DEL-05-02/PANEL-v0.6; DEL-01-01/HOSTING-BOUNDARY-v0.6; DEL-01-01/PIN-SPIKE-v0.1; DEL-09-06/CA-v0.4; DEL-09-09/XT-v0.4; DEL-09-06/RELAY-v0.3. SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` and `FACTS_SQ01_SQ32.md` are unchanged (data about SWBPIPE's current state, not commitments; DECISION-3).
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
    - **Sibling set at commit `8fb51f07f`** (working tree identical when read): WD-v0.4 `WORKFLOW_DECLARATION.md` e492ff63…d8e88e; WD-EX-v0.4 `EXAMPLES.md` 60ce307a…3128ca4 (E1–E8, E2 runs, local cases cited by content); C-v0.4 `CATALOG_AND_READ_BASIS.md` e929d39d…c659a08c (§10.1 LIB-A1, LIB-A2, AF-1, FXA-1…FXA-5; §10.4 variants incl. V-ED1); P-v0.4 0d3960a2…c5e361; ACT-POLICY-v0.4 d6da05ab…369b03b; AS-v0.4 774728d0…1f4dab; RS-v0.4 56806b64…540199; LOOP-v0.4 ffc30483…2f95934e (§2.4.4, §6.2); PANEL-v0.4 cb71bc4b…ce84419; HOSTING-v0.4 201ea320…934c7e58 (§8.3), with HOSTING-v0.5 in the working tree (sha256 873e76f693975242893f74d4243b01a48cab54a91f434fb01e37ec70fb5b0eaa; F-22, U-25 only); ADAPTER-v0.2 a2905dda…a25674bc; DEL-09-06 CA-v0.2 31ea3bff…32d8dee1 (W14-00…W14-10) and RELAY-v0.2 48dc5a1f…2541f65 (SQ-01…SQ-32).
    - **R6 micro-pass (in place, no version bump):** R6_RESOLUTIONS.md sha256 8703e85aa7324e233fab285321e277d720923d3e36e342c865917b55083cb841 (R6-1, R6-4); `reviews/V4-A.md` sha256 121deafc40c4baf0dec71f96eb449083b0d93456c2bd448f89a279951ca2eab1 (MAJOR-1, MAJOR-2; m-1, m-2, m-8). Working tree: C-v0.5 `CATALOG_AND_READ_BASIS.md` sha256 298e425804a04675346d9c3e445a0aab19bc462a75ba8d4f6f55005fca8d2364 (§10.4 **V-GR1** with GR-1…GR-3, GR-P, GR-R, GR-S); WD-EX-v0.5 `EXAMPLES.md` sha256 296875c9aba92be6a3ef86c3ce9d658a9b6ba1d102db71a12f5f0c5c44a4702f (E1c, E1d, E8). (That WD-EX hash is the pre-R6 byte state; the R6 held-actions text quoted in §3.6 is in WD-EX at `b1b7f10e…3362`, below — R7-4 m-8.)
    - **R7 repair (in place, no version bump):** R7_RESOLUTIONS.md (R7-3; R7-4 m-5, m-6, m-8) and `reviews/V5.md` (MAJOR-3; m-5, m-6, m-8). Sibling inputs read at the R7 working state: first at candidate `2f42fba02` — WD-v0.5 `WORKFLOW_DECLARATION.md` 51f4c9fd…6daa (§4.3.1 held actions, §4.3.8); WD-EX-v0.5 `EXAMPLES.md` b1b7f10e…3362 (E1, E1c, E1d, E8); C-v0.5 `CATALOG_AND_READ_BASIS.md` 298e4258…2364 (V-GR1); ADAPTER-v0.3 977d6a26…46f44 (GC-3, GC-5); GUIDE-v0.2 6afc3b90…e3a7 (§2.13, §2.14) — then with the R7 edits made in place to WD, WD-EX, C and ADAPTER in the same repair, each recorded in that file's R7 rows. The post-R7 bytes of every Design file are pinned in GUIDE's input table (R7-4 m-1).
- Receivers: DEL-03-03 (hold-support values for ADAPTER GC-3/GC-5, §3.6, governance phase); DEL-02-01 (WD confirmations and amendments requested in §11; the §2.1 Phase-1 statement and §2.2 `governed` opt-in; CASE-002 M1 workflow-contract row); DEL-05-01 (Phase 1: no host-loop hold, §2.1 PH-2; governance phase: hold-machine semantics for host loops; CASE-002 M1 execution-owner row, OUT-001/OUT-003, REQ-007, VER-008); DEL-04-03 (R8 checkpoint events and transfer records; RS §10 DEL-02-03 row; RS U-17/U-18/U-22/U-23/U-24); DEL-09-06 (local transfer/adaptation evidence account, DEP-02-03-014; VER-004/VER-007). Named but outside this undertaking (D1): DEL-02-02 (CASE-002 M1 workspace row, changed-draft return, VER-004/VER-005 of DEL-02-02). Also read by DEL-05-02 and DEL-04-02 for display of the resolved W7 items. From the live registers (R9-6; ACTIVE rows; detail in §9.2): DEL-02-01 (DEP-02-01-026); DEL-03-03 (DEP-03-03-014); DEL-03-04 (DEP-03-04-009); DEL-04-02 (DEP-04-02-017); DEL-04-03 (DEP-04-03-025); DEL-05-01 (DEP-05-01-017); DEL-05-02 (DEP-05-02-020); DEL-09-06 (DEP-09-06-013, with this deliverable's DEP-02-03-014); DEL-09-09 (DEP-09-09-023); and, outside this increment, DEL-02-02 (DEP-02-02-015), DEL-09-02 (DEP-09-02-017) and DEL-10-03 (DEP-10-03-009).

---

## Changes from v0.5

Wave B design development (run `APP-V4-DESIGN-PASS-2-20260930`, node B2),
under R12 (binding with R1–R11 and DECISION-K1). Rows carry the R12 item and
the survey item they answer (S1-C §C.8, "EXEC n"). New structure is PROPOSED
(B2) unless a row names the ruling that decides it. No governance-phase rule,
value or case result changes; no ScopeOfWork, register or basis text is
changed (needs are returned in §11.5 and the node's return file).

| R12 item (survey item) | Change in v0.6 | Where |
|---|---|---|
| R12-1 (version) | Version v0.5 → v0.6; header: status names the schemas and the prototype beside this file; new v0.6 consumed-input line (R12, BRIEFS, S1-C, OWNER_DECISIONS at current bytes, the generated 0.158.0 bundles, siblings by Wave A label and section). Earlier lines kept as records of their passes | Header |
| R12-1 states (EXEC 5; S1-C §C.2 lags 1–2, §C.5 "States") | **The current-phase recorder as its own definition**: parties and rules RC-1…RC-10 (recording required where observed; the agent requests, SETTLED by K1-1; request recorded only from a structured observation; means to act as a standing facility; lapse labels; run actions), event list CE-1…CE-19, one transition table, display meanings SH-1…SH-5. §4 stays the governance-phase overlay; §0, PH-6, the §2.1 closing paragraph and "Who requests" point to it | §0, §2.1, §2.4, §4 phase note |
| R12-10 (V17-B n-5) | **RC-4 Recording is not a reaction**: what "reacting" means under K1-1, and why writing entries and updating the record's view is not it | §2.4.1 |
| R12-1 interfaces; R12-4 (EXEC 6; S1-C §C.5 "Interfaces (1)", §C.6 D-7; arcs N-23, N-24) | **App-run reached-when table** AW-1…AW-12 per kind and native path (N-MCP, N-CLI), written against the native item kinds of the generated 0.158.0 types (HOSTING §6.7, §6.8, §10; PIN-SPIKE §4); acts and run events AE-1…AE-7; each cell that needs a live observation marked **OBS-1 pending**, with the observation list O-1…O-9. §4.4's arrival and observation rows wired to it | §2.5; §4.4 |
| R12-1 sequences (EXEC 7; S1-C §C.5 "Operating sequences", "Failure behaviour") | End-to-end sequences **SQ-A** (App run on X, A-1…A-12) and **SQ-T** (App → host transfer, T-1…T-8), each step with what fails, who reports, the record left and what follows, including failure of recording itself (A-12; CE-19 recording gap) | §2.6 |
| (EXEC 8) | App-side components by responsibility (checker, recorder, transfer tracer: inputs, outputs, receivers, never) and the OI-014 placement question prepared, not asked (R12-2 keeps it open). U-E2 notes it | §2.7; UNRESOLVED U-E2 |
| R12-1 data; R12-2 | Two PROPOSED JSON Schema 2020-12 formats beside this file, each with a valid and an invalid example: `compatibility-report.schema.json` (CR-1…CR-14; the current-phase variant cannot carry a hold value or hold reason) and `checkpoint-record-entries.schema.json` (one entry kind per CE event; consistent with RS §6 as it stands, citing human-act records by identity) | §2.4.5; §7.4; files beside this one |
| R12-3 | Design prototype in `prototype/` (Python 3 standard library): a subset JSON Schema validator, a test-double catalog from C §10, the required-tool check (§3.3–§3.6), the current-phase recorder, and a runner; ran on 2026-09-30 with every check holding | §7.4; `prototype/README.md` |
| R12-1 verification (EXEC 9; SoW VER-002, VER-003) | New cases **MT-17** and **CH-33** (L-EXEC-33: a fixture that declares `CP-accept` governed), **CH-32** (L-EXEC-32: A4, A6 and A7 kept apart, VER-003); §7.4 states what each case needs to run and whether the prototype ran it; worked report for MT-1 | §7.1, §7.2, §7.4 |
| R12-10 (R11-9) | **CH-31**: the current-phase case where an earlier act does not count, (i) content no longer current (L-EXEC-31) and (ii) another kind (L-EXEC-32). RT-11 maps it to W14-05 for node B7 | §7.2; §7.3 RT-11 |
| R12-10 (V17-A N-4) | One wording: "prior act on this subject, not counted" and "prior act, not counted" become **"prior act not counted"** (RS R8 and L-13 wording) throughout the body; history rows unchanged | §4.3, §4.5, §4.6, §4.9, §7.2 |
| R10-8 carry | AW-6 uses WD's message-output designation (node B1) on condition that it is decidable from the item and its turn; U-E27 | §2.5 AW-6; UNRESOLVED |
| Joins | §9.1 and §9.2 rows state what v0.6 takes from and gives to WD, RS, LOOP, HOSTING, ADAPTER, CA, PANEL/AS, GUIDE and DEL-01-04; new receiver row DEL-01-01 (OBS-1 list). New findings F-32…F-36; new U-E26 (OBS-1, SPIKE) and U-E27; VC-E-14…VC-E-16; VC-E-01, -11, -12, -13 extended | §9, §11.5, UNRESOLVED, Verification cases |

## Changes from v0.4

Wave A alignment (run `APP-V4-DESIGN-PASS-2-20260930`, node A1-C). Rows are
keyed by R9 ID and by the survey item they answer (S1-C §C.8, "EXEC n"; "D-n"
is a disagreement listed in S1-C §A.6 or §C.6). At node A1-C: no new design
content, no rule, value, case result or L-EXEC label changes, and no recorder
or observation mechanism is defined. Rows marked node A2 apply R10 to the
passages they name. At node A3 (DECISION-K1): SP-6 became the
SETTLED earlier-act rule for the current phase (K1-2); the R4-5 rule is kept as
SP-6F, a governance-phase option (PROPOSED); JA-1 was added in §4.7 (K1-3);
and the cases named in the K1-2 and K1-3 rows were recomputed or released.
At node A4, CH-20 gained its own local variant L-EXEC-30 (R11-2). The file
stays DRAFT: unsupplied, unimplemented and not accepted.

| R9 ID (survey item) | Change in v0.5 | Where |
|---|---|---|
| R9-5, R9-11 (EXEC 1) | Version v0.4 → v0.5. Header re-pinned: the four basis docs at their current sha256, naming SCA-V4-001 and SCA-V4-002; the current ScopeOfWork sha256 with the amendments that revised it; the SCC-CASE-002 datasheet, R8 and the intake OWNER_DECISIONS at their current sha256; BASIS-ALIGN DECISION-7 (O-25); DAG-003; the SWBPIPE answers at `afb6e063…`; siblings by version label and section only. Two mistyped abbreviations corrected (PANEL-v0.4 `…4c84419` → `…ce84419`; ADAPTER-v0.3 `…1f44` → `…46f44`). Earlier Consumed-inputs bullets are kept as records of their passes | Header |
| R9-1, R9-3 (EXEC 2) | Checkpoint wording re-pointed to PRD V4-WF-05 and HI V4-HI-42 as amended and to SoW REQ-002 and AC-002 as revised, all quoted in §2.1; the R9-1 summary sentence is used in the Phase line and E-B. The two-halves reading of V4-WF-05 and the basis-update marker are dropped. What is in force in every phase and what is phased to the governance layer are stated (PH-4, PH-10). V4-HI-42 is no longer described as guidance only: its request clause and record clause are in force, and only the hold is phased. §4.7's rationale quotes the revised AC-002 | Header, §1 E-B, §2.1 (lead, PH-4, PH-10, quotations), §4.7 |
| R9-1 (recording; SoW REQ-002) | PH-6: recording is **required where the arrival is observed** (was "may be recorded"), because REQ-002 requires that history preserve the checkpoint's identity and actual disposition. Wording only: how an App run observes an arrival and a request, and what the record then holds, is left to Wave B, and §2.1 points there | §2.1 PH-6 and closing paragraph |
| R9-1 (requester) | New paragraph after the PH table: who requests in the current phase (INTEGRATION; put to the owner in this run's decision package). The §4.6 arrival row separates the governance-phase "act request issued; run holds" from the current-phase reading | §2.1, §4.6 |
| R9-2 (EXEC 2) | R8-11 item 2 and R8-12 item 2 restated against the amended text: E-B, CH-27's current-phase entry, F-30 and U-E24 ("no A5 is forced, and none is recorded") | §1 E-B, §7.2 CH-27, §11.4 F-30, UNRESOLVED U-E24 |
| R9-4, R9-8 (EXEC 4; D-3) | PH-6 and PH-8 are marked confirmed INTEGRATION by R8-11 item 1 (F-31 closed). E-B and U-E24 cite the owner's confirmation of the R8-11 item 2 reading (BASIS-ALIGN DECISION-7, O-25) | §0 Labels, §2.1, §4.7, §11.4, UNRESOLVED |
| R9-8 (EXEC 4) | Findings closed from records: F-10 and F-11 (SoW CLM-003, TBD-001, TBD-002 as revised; DEP-02-03-015 and -016 RETIRED); F-24 (RS R11, R6-5); F-28 (WD §4.3.1 held actions); F-29 (SCA-V4-001). Dispositioned: F-25 (WD-EX keeps L-WDEX-13b alone) and F-27 (LOOP §2.4.4 states the residual limit; CR-12 lists it) | §3.3 CR-12, §11 |
| R9-6; SoW CLM-002, REQ-006, TBD-006 (EXEC 3) | Receivers line and §9.2 rebuilt from the ACTIVE register rows: DEL-03-04 and DEL-09-09 rows added; the outside consumers DEL-02-02, DEL-09-02 and DEL-10-03 added; DEP row IDs shown in §9.1 and §9.2; the §4.4 arrival supplier names DEL-03-03's observations on the external channel (SoW CLM-002, DEP-02-03-026). §10 gains the DEL-04-02 and DEL-01-01 rows. TBD-006 is cited at GV-3; AX-004 and AX-005 in the header. VC-E-10's TBD range becomes TBD-001…TBD-006 | Header, §2.2 GV-3, §4.4, §9, §10, VC-E-10 |
| R9-8 (EXEC 10; V6 m-7) | The "exhaustive partition" sentence of §3.6 is qualified: one declared, malformed case is valued by no row. Which row should value it is **not chosen here**; it is returned as an R10 candidate | §3.6 |
| (EXEC 10; D-2) | §9.1 DEL-02-01 row: the independence rules WD supplies are I-1…I-9 (was I-1…I-8). The "consumed unchanged" list in §1 still names I-1…I-7: I-8 and I-9 state this file's own SP-6 and hold-claim rule (R4-5, R4-2) | §9.1 |
| R9-9 (EXEC 10: D-1, D-4, D-5, D-6) | D-1 is answered in WD-v0.7 §4.2.4 (R5-1; R8-11 item 3); §3.5 is unchanged. **Not changed**, returned as R10 candidates: NG-2's unphased "Absent path → stop" against LOOP §2.4 (D-4); the message-form output designation LOOP §2.4.1 uses (D-5); whether §4.10's A12 rules extend to a network-destination grant (D-6) | §3.5, §4.8, §4.10 |
| R9-11 (labels) | Own and sibling version labels in §3.6, §7, §9 and VC-E-11 moved to the Wave A versions | §3.6, §7, §9, Verification cases |
| **R10-1** (node A2, in place; R9-2's second bullet corrected) | CH-27 current-phase entry: a direct application queues no proposal, so `CP-accept` (kind (c)) is **not reached**; nothing is requested by reason of an arrival that did not occur, no A5 is forced and none is recorded. "`CP-accept`'s act is still requested" is withdrawn | §7.2 CH-27 |
| **R10-7** (node A2, in place) | NG-2 "Absent path" labelled by phase: current phase, the agent follows the plan it worked out with the person; governance phase, for a governed checkpoint, stop; in both phases never recorded as if the act were positive | §4.8 NG-2 |
| R10-9 (node A2, in place) | §4.10 Subject: an operation-class grant setting only; a checkpoint on a network-destination grant is a possible later extension, PROPOSED, not defined | §4.10 |
| **R10-10** (node A2, in place) | The declared, malformed held-actions case (V6 m-7) is ruled: governance phase only, the HS-5 conservative default applies to any declared held-actions element that does not show host operations only, whatever the kind; not invalid; no new failure row; R7-3's derivation for an absent element unchanged. HS-5 row follows | §3.6 partition paragraph; HS-5 |
| R10-11 (node A2, in place) | RT-11 aligned to CA §8.2: W14-05 ← CH-2, CH-20, CH-23, CH-28; W14-06 ← CH-6…CH-8, CH-10, CH-30; W14-07 ← CH-3…CH-5, CH-9, CH-21 (CH-20 and CH-9 checked to contain what CA takes from them). CR-14 and the §6.1 *supplied* row: recording and showing the model destination is SETTLED (OWNER_ITEMS O-10; R9-4), no longer "INTEGRATION (DECISION-2 reading)". §1 "I-1…I-7" stays | §3.3 CR-14; §6.1; §7.3 RT-11 |
| R10-11 sibling citation pass (node A2, in place) | CH-30: "C's R-17 reading" → "WD-EX R-17's reading" (R-17 is a WD-EX row). U-E12: "AP U-04a" (no such ID) → "AP U-04, §12 item 4 (a)" | §7.2 CH-30; UNRESOLVED U-E12 |
| **K1-1** (node A3, in place; owner DECISION-K1 of 2026-09-30, `APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md` sha256 35d6546346907137581be7df3bed4a8ccdb4b8bc55a261ca716040d0ad9f91bc) | Who requests in the current phase: relabelled **SETTLED by DECISION-K1 K1-1** (was INTEGRATION, put to the owner in the decision package). The §4.6 arrival row cites it | §2.1; §4.6 |
| **K1-2** (node A3, in place) | SP-6 rewritten: in the current phase an earlier act counts when it is of the required kind and the content it was made on is still current, and the record cites the earlier act and its time. Capture at or after the arrival is kept only as the governance-phase option **SP-6F** (PROPOSED), which a workflow may take up. "Prior act on this subject, not counted" stays only for an earlier act whose content is no longer current or whose kind differs, or under SP-6F. Following: §4.3 annotations; §4.6 rows; RE-3 and "Why no resumption"; §4.10 *established* row; RP-2; CAP-3 arrival reference. Cases recomputed: CH-9 (ii), CH-12 (iii), CH-20 (and CH-23 (ii) actor); VC-E-05, VC-E-07. F-3 and F-23 closed; U-E4 closed | §4.3, §4.5, §4.6, §4.9, §4.10, §4.12, §5 CAP-3, §7.2, §11, UNRESOLVED, Verification cases |
| **K1-3** (node A3, in place) | **JA-1** written in §4.7: two or more acts may together answer one arrival, each citing its items; an act on the changed referents alone answers together with the earlier act for the unchanged ones. SP-5 and RH-6 follow. CH-8 released (DESIGNED, with its expected results). §8 rows, §9.1 DEL-04-01 row, §9.2 DEL-02-01 row and §10 follow; F-14 and U-E3 closed; VC-E-04 | §4.5 SP-5, §4.7, §7.2 CH-8, §8, §9.1, §10, §11, UNRESOLVED, Verification cases |
| **K1-4** (node A3, in place) | CAP-8: the App records the person's identity from what it can observe (the name set in the App, the operating-system account, the Codex account when Codex reports one), marked *identity not verified*; a verified identity is a governance-phase matter. U-E8 closed. The act control stays DEL-01-04's; where this file says DEL-01-04's contract lacks it (§9.1), it adds "proposed for DEL-01-04's contract at the next amendment (DECISION-K1 K1-4); collected at this run's closeout". The control is not designed here | §5 CAP-8; §7.2 CH-23; §8; §9.1; UNRESOLVED |
| **R11-2** (node A4, in place; V17-B B-1) | CH-20 gets its own binding: new local variant **L-EXEC-30** (the next free number; L-EXEC-5, -10, -16 and -19 stay retired), WD-EX E1b with `CP-review` binding S-2 and S-3 and T2's A4 on S-2 before the arrival at T4. WD-EX R-9b / L-WDEX-7 is no longer CH-20's input; it is cited as the related single-support case (binding S-2), whose result, *performed* by T2's A4, is consistent with CH-20 under K1-2. CH-20's expected results stand as recomputed at node A3 | §7.2 CH-20 |
| **R11-4** (node A4, in place; V17-B M-2) | The preamble of this table is scoped to node A1-C, and a sentence states what node A3 changed (SP-6 SETTLED for the current phase; the R4-5 rule kept as SP-6F, a governance-phase option; JA-1 added; the cases in the K1-2 and K1-3 rows recomputed or released) and what node A4 added (L-EXEC-30) | Preamble of this table |
| **R11-3** (node A4, in place; V17-B M-1) | Header: a new line pins this run's records at their final bytes: R9 `a64e2415…`, R10 `ad3b6caa…`, R11 `e7343b66…`, OWNER_DECISIONS `7458e9e8…`. The node A1 input line and the K1 rows keep the bytes read then | Header |

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
| **R8-12** (item 7; item 1; closing pass, node A6, in place) | **U-E24 closed in place by R8-11 item 2**: D2's reserved-act half binds in Phase 1 (host-enforced); its checkpoint half, WD I-7 and V4-HI-42 are guidance in Phase 1 and bind only for governed checkpoints in the governance phase. E-B, CH-27 and F-30 re-pointed. PH-8 marked confirmed by R8-11 item 1. Phase-1 lapse label after the resume point: **"act lapsed at ‹t›"** (item 1) in PH-8, the §4.6 disposition table and CH-7. Consumed inputs list the post-R8 sibling versions; §3.6, §7 fixture sources and §9 states refreshed (historical rows unchanged) | Header, §1 E-B, §2.1 PH-8, §3.6, §4.6, §7, CH-7, CH-27, §9, F-30, UNRESOLVED |

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
   (§2.1), with the current-phase recorder, the App-run reached-when
   evaluation, the operating sequences and the App-side components
   (§2.4–§2.7, v0.6). The **checkpoint hold machine**, including interruption and
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
confirm; the two such readings, PH-6 and PH-8, were confirmed INTEGRATION by
R8-11 item 1. **Phase 1** (the current phase) and **governance phase
(retained)** mark which phase a rule belongs to (R8-1). From v0.6,
**PROPOSED (B2)** marks a design choice added in Wave B (node B2), open to
comparison (node V18) and to owner revision, and **OBS-1 pending** marks a
cell whose design waits for the live observation OBS-1 (§2.5.3).

---

## 1. Settled distinctions this contribution relies on

| # | Distinction | Citation | Use here |
|---|---|---|---|
| E-A | The product checks a selected workflow's required tools against the current host and tells the person which are missing | V4-WF-04; SoW REQ-001 | §3 |
| E-B | When a run reaches a declared checkpoint, the required human act is requested, and it is recorded as done only when the person performs it, whatever the autonomy setting. Holding the run at the checkpoint until the act is performed is phased to the governance layer: in the current phase a checkpoint is plan guidance that the person and the agents manage, and neither the App nor a host's embedded loop enforces a hold, blocks a run, or reports a workflow unsupported because a hold cannot be enforced. The reserved acts (V4-HI-30) still bind (the R9-1 summary of the amended texts, which §2.1 quotes). **In force in every phase:** the act is requested; it is recorded as done only when the person performs it (PH-4); the reserved acts bind (PH-5). **Phased to the governance layer:** holding the run until the act (§2.2). D2's "or a declared checkpoint" clause is read by R8-11 item 2 (a reading the owner confirmed: `APP-V4-BASIS-ALIGN-20260928` DECISION-7, OWNER_ITEMS O-25), restated against the amended text by R9-2 (DERIVED; U-E24 closed): D2's "no autonomy grant widens past a reserved act" binds, and the host enforces it through its operations. For a declared checkpoint, V4-HI-42's request clause and record clause are in force whatever the autonomy setting; whether the run goes on before the act is for the person and the agents in the current phase, and the host's own treatment of its operations decides what the host does | PRD V4-WF-05 and HI V4-HI-42 as amended by SCA-V4-001; SoW REQ-002, AC-002; D2 "No autonomy grant widens past … a declared checkpoint"; DECISION-4 D4-1 | §2.1, §2.2, §4 |
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

The phasing is SETTLED by DECISION-4 D4-1 and its clarification, and is now
stated by the accepted basis and by this deliverable's ScopeOfWork: PRD
V4-WF-05 and HOST_INTEGRATION V4-HI-42 as amended by SCA-V4-001, and SoW
REQ-002, AC-002, CLM-003 and TBD-006 as revised (R9-1; the texts are quoted
after the table). The framing below is INTEGRATION (R8-1). Two rules, PH-6
and PH-8, added a reading to R8 at v0.4 (**PROPOSED (A1)**); R8-11 item 1
confirmed both (INTEGRATION).

| # | Rule (Phase 1, this increment) |
|---|---|
| **PH-1 Guidance** | A workflow's declared checkpoints are **plan guidance**. The declaration still states each checkpoint's required act, reached-when, subject class and held actions (WD §4.3.1). The person and the agent work out the plan around them, and the agents manage any pause, hold point or gate themselves |
| **PH-2 No enforcement** | Neither the App nor a host's embedded loop enforces a hold. Neither stops or blocks a run, withholds or holds a dispatch, or re-holds a run at a checkpoint. No hold is claimed. The principle applies to the host's own embedded loop (DECISION-4 clarification; R8-8 for LOOP §2.4.4) |
| **PH-3 No *unsupported* for hold reasons** | The required-tool check (V4-WF-04; §3) is unchanged. No checkpoint enters its result. The result depends on the required tools and the channel state (R8-2), together with the role and delegation reasons WD §4.2.4 already names, which are not hold reasons. No hold-support value is assigned. The reason "checkpoint hold not enforceable on this surface" (R4-8) is never reported. An invalid or not-established checkpoint declaration is reported as a declaration defect and does not change the result (§4.14) |
| **PH-4 Acts only when performed** | A human act is recorded as done **only when the person performs it**, with capture evidence from the capturing surface (the record clause of V4-WF-05 and V4-HI-42 as amended, in force in every phase; SoW REQ-002; §4.5 SP-1…SP-8; §5; R3/R4 act-evidence rules). An agent never records a human act on the person's behalf. None of the following is ever the act: success, a queued proposal, a receipt, findings, host checks, an A14 settlement, an elicitation answer, or a conversation statement (E-C; CAP-5…CAP-7) |
| **PH-5 Reserved acts stand** | DECISION-1 D2 is unchanged. A4, A5 (where a proposal is required), A6, A7, A12 and enabling external access (A13) stay the person's (E-I). A host enforces its own list through its operations (V4-HI-30). For example, SWBPIPE's Apply is A5 in the person's hands, and enabling external access is A13 (R8-6). PH-2 removes no host refusal of an agent's attempt at a reserved operation |
| **PH-6 Recording is observation** | A checkpoint's arrival and the act that answers it are **recorded** (RS) where the arrival is observed, with the other §4.4 events: act-declined, act-lapsed, run-ended, and observation lost or recovered. Recording there is required, not optional (R9-1): SoW REQ-002 requires that history "preserve the checkpoint's identity and actual disposition". The record holds the checkpoint's identity, the request where it can be identified, and the act only when the person performs it; it never says *performed* without the act. How an App run observes an arrival and a request, and what the record then holds, is defined in §2.4 (the current-phase recorder, v0.6) and §2.5 (App-run reached-when). This lets the person and the agent see where the plan paused and what was done. Recording is observation, not enforcement. **Confirmed INTEGRATION by R8-11 item 1 (PROPOSED (A1) at v0.4):** a view that states an arrival's state from the record may use the shared disposition words (WD §4.3.4) as record labels. *Waiting* then means "reached; act not yet recorded", never "the run is held" |
| **PH-7 Continued past a checkpoint** | *Action during hold* is not a violation marker in Phase 1. A run action observed after an arrival and before the act that answers it may carry the optional plain annotation **"continued past ‹checkpoint› before ‹act›"** (R8-1). It is information: never a defect, refusal or finding |
| **PH-8 Lapse is recorded; nothing re-holds** | **PROPOSED (A1); confirmed INTEGRATION by R8-11 item 1.** A performed act whose bound content changes is still recorded as lapsed: an act-lapsed event, shown against the affected referents, with outputs gated by that act showing their standing lapsed (V4-REC-05; R2-19 recording). The run is **not** re-held: re-hold (RH-2…RH-7) is governance phase. R8-1 lists "re-hold, lapse" with the retained hold machine. This file reads the *recording* of a lapse as Phase-1 observation required by V4-REC-05, and the *hold* consequences as governance phase. After the resume point the Phase-1 label is **"act lapsed at ‹t›"**: nothing says *waiting*, nothing is re-held, and a new act is recorded when performed (R8-12 item 1) |
| **PH-9 `governed` in Phase 1** | A checkpoint declared **`governed`** (WD-v0.7 §4.3.1, PROPOSED) is honoured in Phase 1 **only as guidance**. The flag is shown, and PH-1…PH-8 apply unchanged |
| **PH-10 V4-WF-05 and V4-HI-42** | As amended by SCA-V4-001 (accepted 2026-09-29), both texts state the phasing themselves; they are quoted below. **In force in every phase:** the act is requested; it is recorded as done only when the person performs it (PH-4); the reserved acts bind (PH-5). **Phased to the governance layer, not withdrawn:** holding the run until the act (§2.2). The update of the accepted basis that v0.4 awaited is done (R9-1; F-29 closed) |

What Phase 1 keeps from §4 is its **recording** content: identities (§4.1),
events (§4.4), which recorded act answers which arrival (§4.5), the
disposition words as record labels (§4.3, §4.6), negative decisions and paths
as recorded (§4.8), run end and continuation (§4.9), A12 control relations
(§4.10), A5 item rules (§4.11), record rebuilding and replay (§4.12, except
RP-4 and the "stays holding" clause of RP-5), and invalid-declaration
reporting (§4.14). Its **hold** content is governance phase (§2.2). Under
R9-1 and SoW REQ-002 this recording is required where the arrival is
observed. From v0.6 this recording content is stated on its own as the
**current-phase recorder** (§2.4), which cites these rules by ID; §4 is the
governance-phase overlay on the same arrivals.

**The texts (R9-1).**

> **PRD V4-WF-05 (as amended by SCA-V4-001).** "When a run reaches a
> workflow's declared checkpoint, the required human act is requested, and
> the run does not record the act as done until the person performs it.
> Holding the checkpoint — the run waits until the act is performed — is
> **phased to the governance layer**, not withdrawn (DEC-4): in the current
> phase, declared checkpoints are plan guidance that the person and the
> agents manage, and neither the App nor a host's embedded loop enforces a
> hold, blocks a run, or reports a workflow unsupported because a hold cannot
> be enforced. Enforced holds are applied later to the workflows that need
> them; the declared checkpoint and the definitions that enforcement needs
> are kept so that every such workflow can be served. Reserved human acts
> (§4.5) are unaffected."
>
> **HOST_INTEGRATION V4-HI-42 (as amended by SCA-V4-001).** "Autonomy does
> not override a workflow's declared checkpoints: whatever the autonomy
> setting, a checkpoint's required act is requested and recorded as done only
> when the person performs it. Holding the run at the checkpoint until then
> is phased to the governance layer (V4-WF-05): in the current phase a
> checkpoint is plan guidance that the person and the agents manage, and the
> reserved acts (V4-HI-30) still bind."
>
> **SoW REQ-002 (as revised by SCA-V4-001).** "At a declared checkpoint,
> request the required human act and record it as done only when the person
> performs it, even where the applicable operation autonomy otherwise allows
> direct application. In the current phase the checkpoint is plan guidance:
> the person and the agents manage any pause, and neither the App nor a
> host's embedded loop holds or blocks the run or reports the workflow
> unsupported because a hold cannot be enforced. Holding the run at the
> checkpoint until the act is performed is the governance-phase definition,
> retained for workflows that need it (TBD-006). Interrupted or replayed
> history must preserve the checkpoint's identity and actual disposition."
>
> **SoW AC-002 (as revised by SCA-V4-001).** "A declared checkpoint requests
> its named human act, and the act is not recorded as done — despite
> direct-operation autonomy, interruption or replay — until evidence shows
> that the required act actually occurred. In the current phase no hold is
> claimed or enforced; for a workflow that takes up the governance phase, the
> checkpoint also keeps the run waiting until that evidence."

**Who requests, in the current phase (R9-1; SETTLED by DECISION-K1 K1-1,
the owner's decision of 2026-09-30 in run `APP-V4-DESIGN-PASS-2-20260930`,
which confirmed R9-1's reading of DECISION-4's exact text).**

- The **agent carrying out the workflow** asks the person for the act when
  its work reaches the checkpoint. It does so because the declared checkpoint
  is part of the plan it was given.
- The **product's part** is: (i) to give the agent the declared checkpoint
  with the workflow; (ii) to offer the person the means to perform the act;
  (iii) to record what it observes — the checkpoint's identity, the request
  where it can be identified, and the act only when the person performs it.
  A record never says *performed* without the act.
- Neither the App nor a host's embedded loop issues the request in the
  agent's place, pauses the run, or otherwise reacts to the arrival.
- How an App run observes an arrival and a request, and what the record
  then holds, is defined in §2.4 (RC-1…RC-10) and §2.5 (v0.6). Recording
  is not a reaction (RC-4).

### 2.2 Governance phase: the retained definition and the `governed` opt-in (R8-1, R8-2)

| # | Rule |
|---|---|
| **GV-1 Retained, relabelled** | The following are the **governance-phase definition (retained)**. They are relabelled, not deleted: the enforcement boundary (§2.3: HP-1…HP-4, HP-H); the hold-support clauses of the check result and its precedence (§3.5); hold support (§3.6: four values, HS-1…HS-5 as amended by R6-1, R7-3 and R8-2); the hold machine's hold content (§4.2 HD-1…HD-4; re-hold §4.7 RH-2…RH-7; §4.10 AR-2; §4.12 RP-4 and RP-5's "stays holding"; §4.13 MA-3); R2-12 carriage assurance; the R4-8 *unsupported* reason (WD §4.2.4); and the LOOP §2.4.4 host-loop hold |
| **GV-2 Opt-in per checkpoint** | A workflow opts in by declaring a checkpoint **`governed`** (WD-v0.7 §4.3.1; optional flag, PROPOSED, R8-1). In the governance phase, §3.5's hold-support clauses and §3.6 apply to governed checkpoints only. A checkpoint not declared governed stays plan guidance in every phase. Not every workflow will have governance. Every workflow that needs it must be serveable by these definitions, so the declaration keeps every field they consume (WD §4.3.1) |
| **GV-3 When it applies** | Later, per workflow that needs it, when the owner calls for it (DECISION-4 D4-1; SoW TBD-006). **D6** (App-side run holds) is closed for Phase 1 and re-opens then (R8-2; U-E1). Until then nothing in this file is in force as enforcement |
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

### 2.4 The current-phase checkpoint recorder (Wave B; S1-C EXEC 5; R12-1)

This section is the **current-phase definition** of checkpoints in App runs,
stated on its own rather than by subtraction from §4 (S1-C §C.5 "States").
It owns one stateful thing, the **arrival as recorded**, and states its
parties, events, transitions, display and data. §4 stays the
**governance-phase overlay**: it adds hold content (HD-1…HD-4, RH-2…RH-7,
AR-2, RP-4, RP-5's "stays holding", MA-3's limit) to the same arrivals and
events, for governed checkpoints only (§2.2 GV-2). The §4 rules this section
uses are cited by ID and apply unchanged: identities (§4.1), SP-1…SP-8 with
SP-6 (§4.5), JA-1 (§4.7), NG-1…NG-4 (§4.8), RE-1…RE-5 (§4.9), the A12
control relations (§4.10), MX-1…MX-8 (§4.11), RP-1…RP-3 and RP-5…RP-8
(§4.12) and §4.14. Labels: rules restating a ruling carry it; everything
new here is **PROPOSED (B2)**.

#### 2.4.1 Parties and rules

| # | Rule |
|---|---|
| **RC-1 Scope** | App runs: the App's Codex (stock Codex; definition pin 0.158.0) acting on App content and, over the external channel X, on host content. A host's embedded loop records with LOOP §2.4 (LP-3), using the same event meanings and labels. PROPOSED (B2) |
| **RC-2 Recording is required where observed** | Every §2.4.2 event the App observes for a run is written, with the derived CE-18 labels (PH-6; R9-1, INTEGRATION; SoW REQ-002 "Interrupted or replayed history must preserve the checkpoint's identity and actual disposition"). An event the App does not observe is not written and is never inferred (E-E). A record never says *performed* without the act (PH-4) |
| **RC-3 Who requests** | The agent carrying out the workflow asks the person for the act (SETTLED by DECISION-K1 K1-1). The recorder issues no request, and nothing in the App asks in the agent's place |
| **RC-4 Recording is not a reaction** (R12-10; V17-B n-5) | DECISION-K1 K1-1 says the product "records what it observes" and does not "otherwise react to an arrival". Here **reacting** means changing, because of an arrival, what the run, the agent, the supplier, the host or the person is sent, offered or asked: issuing or re-issuing a request, pausing, interrupting or stopping a turn, declining or refusing a call, starting a turn, adding guidance, raising a prompt, dialog or notification, or making a host read. **Recording** is writing entries to the run record and updating the view of that record (SH-1…SH-5). It sends nothing to the supplier, the agent or the host, and changes nothing the run can do. The recorder consumes only observations the App already receives: the native items HOSTING §6.7 delivers unchanged, and the observations on X that DEL-03-03 passes (ADAPTER §7.7). The rule is DERIVED from K1-1; the definition of *reacting* is PROPOSED (B2) |
| **RC-5 A request is recorded only from a structured observation** | The agent's request is recorded (CE-4) only where it is a structured item the App observes: a supplier person-input request (at 0.158.0 `item/tool/requestUserInput`) or an MCP elicitation (`mcpServer/elicitation/request`) raised while an arrival is current, or a request the host records and a read over X returns. It is associated with an arrival only when exactly one arrival is current; otherwise it is recorded with "arrival association not established". The recorder never classifies agent message text as a request (RW-1; E-E). Where none is observed, the view says "no request observed", never "not requested". The answer to such a request is conversation, never the act (CAP-6). PROPOSED (B2) |
| **RC-6 Means to act, not triggered by an arrival** | The product offers the means to act (K1-1 (ii)) as a standing facility, available whether or not an arrival was recorded, because an earlier act counts (SP-6): for host content, the host's own act facility (V4-HI-31; CAP-1; no App proxy, U-E9), and the view says where the act is performed; for App content, the App act control (CAP-2; construction DEL-01-04, later; its obligation proposed for DEL-01-04's contract, DECISION-K1 K1-4). An arrival changes neither facility. PROPOSED (B2) |
| **RC-7 Which act answers** | SP-1…SP-8 decide (§4.5). An earlier act of the required kind whose content is still current counts and is cited with its capture time (SP-6; SETTLED by DECISION-K1 K1-2); two or more acts may answer together, each citing its referents (JA-1; SETTLED by DECISION-K1 K1-3). An act on the arrival's subject that does not answer is recorded with its reason (CE-6): content no longer current or another kind (shown **"prior act not counted"** when captured before the arrival; RS R8 and L-13 wording, V17-A N-4), or other content (**"act on other content"**, SB-2). A host-reported act without a capture-evidence reference is not an act record at all: no human-act record is written for it and nothing is counted (I-5; RS §6.1, HA-1; CH-28) |
| **RC-8 Lapse labels** | Before the resume point: *waiting*, **"lapsed at ‹t›"** (R2-19; both phases). After the resume point, run live: the act-lapsed event is recorded against the affected referents and labelled **"act lapsed at ‹t›"**; nothing says *waiting* and nothing re-holds (PH-8; R8-12 item 1). The recorded disposition value stays *performed* with that annotation and the lapsed referents, so no seventh value arises (R2-18) and the arrival is not reopened as *waiting*; a later act on the lapsed referents answers together with the earlier act for the unchanged ones (JA-1) and gives the next performance ordinal (RS L-12). The choice of the retained value is PROPOSED (B2) (F-34). After run end: *lapsed* per referent (R2-19) |
| **RC-9 Run actions** | A **run action** is an agent action the run takes: at 0.158.0 a native item of type `mcpToolCall`, `dynamicToolCall`, `commandExecution` with source `agent`, `fileChange`, `collabAgentToolCall`, `webSearch` or `imageGeneration`. Agent messages, reasoning and plan items are conversation, not run progress (HD-2). A `commandExecution` with source `userShell`, and every other operation of the person's own, is never a run action and never carries "continued past" (R5-5). The first run action after an arrival becomes *performed* is the resume point (HD-5; CE-11). A run action after an arrival and before its answering act may carry "continued past ‹checkpoint› before ‹act›" (PH-7; CE-12). PROPOSED (B2); the classification of item types rests on generated types only (§2.5) |
| **RC-10 Rebuildable** | Dispositions are a function of the entries (§4.12 principle). CE-18 entries are derived and can be rebuilt from the others; the executor's working state is disposable |

#### 2.4.2 Event list (current phase)

"Observed from" names the §2.5 row that decides the event in an App run.

| CE | Event | Observed from | Entry kind (schema) | Effect |
|---|---|---|---|---|
| CE-1 | Checkpoint listed at run start, with evaluability on this surface | The resolved declaration (RP-5); §2.5 AW-3, AW-4 | `checkpoint_listed` | Checkpoint *not reached*; "arrival not evaluable on this surface: ‹reason›" where so |
| CE-2 | Declaration finding (invalid / not established) | WD validity rules (§4.14) | `declaration_finding` | No arrival is ever created for it; check result unchanged (PH-3) |
| CE-3 | Arrival | §2.5 AW-1, AW-2, AW-5…AW-10 | `arrival` | Creates the arrival with ordinal, event, evidenced time, bound subject, purpose, scope, limits |
| CE-4 | Request observed | §2.5 AE-3 (RC-5) | `request_observed` | Annotation only |
| CE-5 | Act counted | §2.5 AE-1, AE-2; SP-1…SP-8 | `act_counted` (relation `after_arrival` or `earlier_act`) | Covers its referents (JA-1) |
| CE-6 | Act not counted | §2.5 AE-1, AE-2 | `act_not_counted` (reason) | Annotation (RC-7) |
| CE-7 | A5 per-item decision | P §4.3 through §2.5 AE-1 | `item_decision` | A5 evaluation (MX-1…MX-8) |
| CE-8 | Act declined | Capturing surface (R2-5) | `act_declined` | *resolved negatively* (NG-1) |
| CE-9 | A12 control relation | Control surface (§4.10) | `control_relation` | Counts only when *established* (SP-7) |
| CE-10 | Act lapsed | A changed content identity observed (§2.5 AW-10 reads; outcomes) | `act_lapsed` (before resume · after resume · after run end) | RC-8 |
| CE-11 | Run resumed | §2.5 AE-5 (RC-9) | `run_resumed` | Resume point (HD-5) |
| CE-12 | Continued past (optional) | §2.5 AE-5 (RC-9) | `continued_past` | Information only (PH-7) |
| CE-13 | Observation lost | §2.5 AW-12, AE-6 | `observation_lost` | Deciding observations become *unknown* |
| CE-14 | Observation recovered | §2.5 AE-6 | `observation_recovered` | Recovered events with their own times; no back-fill (RP-1) |
| CE-15 | Arrival replaced | MX-6 | `arrival_replaced` | Final *waiting* "replaced by arrival n+1" |
| CE-16 | Act after run end | §2.5 AE-1, AE-2 | `act_after_run_end` | Shown against the ended arrival's subject; changes nothing (RE-2) |
| CE-17 | Run ended | §2.5 AE-7 | `run_ended` | Finality (RE-1); waiting arrivals listed |
| CE-18 | Disposition label | Derived (RC-10) | `disposition` | The record label after each change |
| CE-19 | Recording gap | The recorder itself (§2.6 A-12) | `recording_gap` | States an interval in which nothing was written |

#### 2.4.3 Transition table (per arrival, current phase)

Record labels are the six shared dispositions (WD §4.3.4); *waiting* means
"reached; act not yet recorded", never "the run is held" (PH-6).

| From | Event / condition | To | Entries written |
|---|---|---|---|
| (listed) | CE-3; earlier acts do not cover the bound scope | **waiting** | `arrival`; `act_counted` (`earlier_act`) for any referents earlier acts cover; `act_not_counted` for earlier acts that do not count; `disposition` |
| (listed) | CE-3; earlier acts cover the whole bound scope (SP-6) | **performed** (ordinal 1), "by earlier act ‹act› at ‹t›" | `arrival`; one `act_counted` (`earlier_act`) per act; `disposition` |
| (listed) | Deciding observation lost for the named event (AW-12) | **unknown** | `observation_lost`; `disposition` |
| (listed) | CE-17 with no arrival observed | checkpoint **not reached** (with CE-1's evaluability limit, if any) | `run_ended` |
| waiting | CE-5 acts now cover the bound scope | **performed** (ordinal n+1); "answered by ‹n› acts" when more than one | `act_counted`; `disposition` |
| waiting | CE-5 covering part of the scope | waiting | `act_counted` (its referents) |
| waiting | CE-6 | waiting, with the RC-7 annotation | `act_not_counted`; `disposition` |
| waiting | CE-7: MX-4 / MX-5 / MX-3 / MX-6 | **performed** / **resolved negatively** (partial if mixed) / **unknown** / waiting "no items remain" | `item_decision`; `disposition` |
| waiting | CE-8 | **resolved negatively** | `act_declined`; `disposition`. The declared path is guidance the agent follows (NG-2, current phase) |
| waiting | CE-9 *pending* or *refused* | waiting, "A12 awaiting control confirmation" / "A12 refused by control: ‹reason›" | `control_relation`; `disposition` |
| waiting | CE-10 on a referent a counted act covered | waiting; that referent needs an act on its current content | `act_lapsed`; `disposition` |
| waiting | CE-12 (agent run action) | waiting | `continued_past` (optional) |
| waiting | CE-17 | waiting (final); listed in the run-ended entry | `run_ended` |
| performed | CE-10 **before** the resume point | **waiting**, "lapsed at ‹t›" | `act_lapsed` (`before_resume`); `disposition` |
| performed | CE-11: first agent run action | performed | `run_resumed` |
| performed (resumed) | CE-10 | performed, "act lapsed at ‹t›" with the lapsed referents (RC-8); nothing re-holds | `act_lapsed` (`after_resume`); `disposition` |
| performed, with lapsed referents | CE-12 | unchanged | `continued_past` (optional) |
| performed, with lapsed referents | CE-5 acts cover the lapsed referents | **performed** (ordinal n+1), "answered by ‹n› acts"; a new resume point follows | `act_counted`; `disposition` |
| performed | Later established A12 on an overlapping setting | performed, "superseded by ‹act›" | `control_relation` |
| performed | CE-17 | performed (final) | `run_ended` |
| performed (run ended) | CE-10 | **lapsed** per referent | `act_lapsed` (`after_run_end`); `disposition` |
| any (run ended) | CE-16 | unchanged, "after run end" | `act_after_run_end` |
| unknown | CE-14 with the deciding observation | as the observation determines | `observation_recovered`; entries for the recovered events; `disposition` |
| waiting ("no items remain") | New arrival of the same checkpoint | waiting (final), "replaced by arrival n+1" | `arrival_replaced` |

Precedence and order ambiguity follow §4.6 and RP-8. The prototype
(`prototype/checkpoint_recorder.py`) implements the rows exercised by CH-7,
CH-8, CH-10, CH-20 and CH-31 (§7.4).

#### 2.4.4 What the App shows (display meanings)

The display is built by the App's interface owner (DEL-01-04, later); its
meanings go to DEL-05-02 and DEL-04-02 (§9.2). PROPOSED (B2).

- **SH-1** At run start, the checkpoint list as plan guidance (CE-1): name,
  act kind, purpose, scope, the `governed` flag where declared (PH-9), and
  "arrival not evaluable on this surface: ‹reason›" where CE-1 says so.
- **SH-2** Per arrival, the label in words: *waiting* → "reached; act not yet
  recorded"; *performed* → the answering act or acts, each with its person
  (marked *identity not verified*, CAP-8), time and referents, including "by
  earlier act ‹act› at ‹t›" and "answered by ‹n› acts"; *resolved negatively*;
  *lapsed*; *unknown*, with which observation was lost; "act lapsed at ‹t›"
  after the resume point. Beside it: the bound subject with content
  identities, the purpose and scope, and the request if one was observed
  ("no request observed" otherwise).
- **SH-3** Where the act is performed (RC-6): "in the host's own view" for
  host content; the App act control for App content.
- **SH-4** Never shown: "held", "blocked", "paused" or "waiting for the
  person" as a state of the run; a hold-support value; *unsupported* for a
  hold reason; a prompt, dialog or notification raised by an arrival. The
  run's own state (for example a turn in progress or completed) is shown as
  the supplier reports it.
- **SH-5** "Continued past ‹checkpoint› before ‹act›" is shown as
  information, never as a warning or defect.

#### 2.4.5 Record entries (data)

The entries are defined by the PROPOSED schema
[`checkpoint-record-entries.schema.json`](checkpoint-record-entries.schema.json)
beside this file (JSON Schema 2020-12; R12-1, R12-2), with a valid example
(CH-7 then CH-8, produced by the prototype) and an invalid example. One entry
kind per CE event; the document is current phase only, so no hold, re-hold,
hold-support or "action during hold" entry can be expressed; the governance
overlay would add its own kinds and is not defined here.

Consistency with RS as it stands (read-only): the entries are the
per-checkpoint and per-arrival content of RS R8 and the references of RS R9.
A human act is cited by its RS §6 record identity with its kind, evidenced
capture time and capturing surface (RS §6.1 "Relations", "Order"); the
decision actor, recorder, capture-evidence references and the *identity not
verified* limit stay in the RS §6 record, which this file never writes (RS
HA-1, HA-2). The written-at order and entry identity are RS §3's common
elements. Elements RS R8 does not yet name are returned as joins (§11.5 F-35):
the observed request with its form and association, a checkpoint's
evaluability, an act not counted with its reason, the arrival event's source
and limits, and the recording gap.

---

### 2.5 App-run reached-when evaluation (counterpart of LOOP §2.4.1; S1-C EXEC 6)

The recorder evaluates each declared checkpoint's reached-when **only against
events the App observed** (WD RW-1; E-E). Two sources exist in an App run:

- the native items and notifications the App's supplier delivers unchanged
  (HOSTING §6.7), named here as the generated types at pin 0.158.0 name them
  (`observed-in-generated-types`; §0 "Naming": citing a supplier name
  selects nothing); and
- on the external channel X, the observations DEL-03-03 passes (ADAPTER
  §7.7), including its native-tool mapping (ADAPTER §4.1 NM-1) and its
  result-to-outcome mapping (ADAPTER §4.5), for **both native paths**
  (R12-4): an MCP server's tools (N-MCP) and a command-line tool that Codex
  runs (N-CLI).

No model turn has been observed at the pin (HOSTING §8.1 L-3; §10). Every
cell whose arrival event depends on the live order or content of items is
therefore marked **OBS-1 pending**: its design is PROPOSED (B2), and §2.5.3
lists exactly what OBS-1 must observe to settle it.

**Native vocabulary used (0.158.0, generated types only).** Notifications
`item/started` {item, thread, turn, `startedAtMs`} and `item/completed`
{item, thread, turn, `completedAtMs`}; `turn/completed` {thread, turn with
status *completed · interrupted · failed · inProgress*}. Thread items:
`agentMessage` {text, `phase` *commentary* or *final_answer*, which "providers
do not emit … consistently", so absent means "phase unknown"}; `mcpToolCall`
{server, tool, arguments, status *inProgress · completed · failed*, result
{content, structuredContent}, error}; `commandExecution` {command, source
*agent · userShell · unifiedExecStartup · unifiedExecInteraction*, status
*inProgress · completed · failed · declined*, exit code, aggregated output};
`fileChange` {changes {path, kind, diff}, status as `commandExecution`}.
Server requests `item/commandExecution/requestApproval` and
`item/fileChange/requestApproval` (A14), `item/tool/requestUserInput`,
`mcpServer/elicitation/request`.

#### 2.5.1 Reached-when, per kind and path

| # | Reached-when (WD §4.3.1) | Path | Arrival event in an App run | Bound subject from | Standing |
|---|---|---|---|---|---|
| **AW-1** | (a) before dispatch of a named host operation | N-MCP | `item/started` of an `mcpToolCall` item whose server and tool map to the named catalog operation through a host-supplied mapping (ADAPTER §4.1 NM-1). This is the earliest native observation of the call. The App cannot observe "before dispatch": nothing sits on the dispatch path (HP-1 not adopted; ADAPTER §2 native family). The arrival carries the limit **"arrival observed at call start; dispatch order not established"** until OBS-1 shows the order | *Targets of the held call*: the targets the call names, with the content identities of the relied-on read the call cites (WD §4.3.6); never argument text | **OBS-1 pending** (O-1, O-2, O-4) |
| **AW-2** | (a) as AW-1 | N-CLI | `item/started` of a `commandExecution` item with source `agent` whose command matches the named operation's host-supplied command form (ADAPTER §4.1). Where the person's Codex mode raises `item/commandExecution/requestApproval` first, that request is the earliest observation and the arrival is recorded at it; its answer stays an A14 settlement (R13 only; CAP-5). Same limit as AW-1 | As AW-1 | **OBS-1 pending** (O-4, O-7) |
| **AW-3** | (a) on a harness capability | App | **Not evaluable**: harness-capability names are unresolved (U-E10; EV-3). CE-1 says so; at run end the checkpoint is *not reached* with that limit | — | DESIGNED (limit) |
| **AW-4** | (a) or (c) on X with no host-supplied native-tool mapping | X | **Not evaluable** (ADAPTER NM-2). SWBPIPE supplies no mapping and no per-operation identity (SQ-12), so on its X every kind (a) and kind (c) checkpoint is not evaluable | — | DESIGNED (limit) |
| **AW-5** | (b) on an output whose form is a host change (WD §4.4) | N-MCP, N-CLI | The host outcome that produces the output, evaluated as AW-8 or AW-9 on the producing operation | Per the declared subject class | As AW-8, AW-9 |
| **AW-6** | (b) on an output whose form is a report or message to the person | App | `item/completed` of the `agentMessage` item that the declaration's message-output designation identifies (the WD element added by node B1, R10-8). The designation must be decidable from the item and its turn without reading the message's meaning (RW-1). Forms the recorder can decide at 0.158.0: **(m1)** the last completed `agentMessage` of a turn whose `turn/completed` status is *completed*; **(m2)** an `agentMessage` whose `phase` is *final_answer*; **(m3)** a declared literal marker at a fixed position, matched exactly. A model's statement that an output exists never counts. Limit: "the designation marks where the agent put the output; it does not show that the content is what the declaration describes" | *Named output*: the message item and the content identity of its text, with method designation. *Objects a named output concerns*: the objects the read or examination result the output relies on identifies (for example the OP-C3 result the findings cite), bound through their subject content identities as read (R3-1); never message text | **OBS-1 pending** (O-5, O-6). Which of m1–m3 WD admits is B1's (join) |
| **AW-7** | (b) on an output whose form is a file or document in the App project | App | `item/completed` of a `fileChange` item with status *completed* whose changes include the output's declared path | *Named output*: the file's content identity after the change (RS L-1, third source) | **OBS-1 pending** (O-8); WD §4.4 names no path element (join, F-33) |
| **AW-8** | (c) observed host outcome of a named operation (e.g. *queued*) | N-MCP | `item/completed` of the `mcpToolCall` item for the named operation whose result maps (ADAPTER §4.5) to the named outcome. Evidenced time: the host outcome time where the result carries one, otherwise `completedAtMs`, labelled supplier item time | *Change items of a named proposal*: proposal and item identities with change-item content identities from the result (P §3.1). *Objects changed by a named outcome*: the resulting objects of the applied outcome (P §9; R2-14) | **OBS-1 pending** (O-3) |
| **AW-9** | (c) as AW-8 | N-CLI | `item/completed` of the `commandExecution` item; the outcome is read from its exit code and aggregated output through the host's command-line encoding (ADAPTER OC-9; SWBPIPE: JSON with named codes, SQ-09) | As AW-8 | **OBS-1 pending** (O-7) |
| **AW-10** | (c) on an outcome that appears only in a later read (e.g. *applied (receipt)* after the person's A5 in the host) | X | The first host read result that shows the outcome. The reads observed are those the agent issues in the run, and App-origin reads only once DEL-03-03 defines them (HOSTING §6.8: no App-origin use on a host channel is defined in this increment). The recorder issues no read (RC-4). If no read shows the outcome, no arrival is recorded, and at run end the checkpoint is *not reached* with the limit "outcome not observed in this run" | As AW-8 | DESIGNED; who issues the reads is a join with ADAPTER §7.7 (F-32) |
| **AW-11** | (c) on App content | — | Not applicable: kind (c) names a host operation's outcome (WD §4.3.1) | — | — |
| **AW-12** | Any kind: the deciding observation is lost | Any | The named item never completes (`turn/completed` *interrupted* or *failed*), or the supplier exits (HOSTING §4.3): CE-13, and the arrival or the checkpoint is **unknown** (§4.6) | — | DESIGNED |

#### 2.5.2 Acts, requests, actions and run events

| # | Event | Observed as | Standing |
|---|---|---|---|
| **AE-1** | Act on host content (A4 through OP-C6, A5 and A10 through OP-C7 and OP-C8, and others the host offers) | Captured by the host act facility; observed on X through a read that returns the act with its capture-evidence reference (ADAPTER §7.7). Without the reference no human-act record is written and nothing is counted (RS §6.1, HA-1; CH-28). SWBPIPE exposes none (SQ-01), so no host-content act can be counted against it | DESIGNED |
| **AE-2** | Act on App content | Direct capture through the App act control (CAP-2, CAP-3) | AWAITING INPUT (DEL-01-04's control) |
| **AE-3** | Request (CE-4) | RC-5's structured forms | **OBS-1 optional** (O-9) |
| **AE-4** | Tool-permission settlement (A14) | The approval requests above; recorded in RS R13 only, never an act (CAP-5) | DESIGNED |
| **AE-5** | Run action (CE-11, CE-12) | `item/started` of the RC-9 item types | **OBS-1 pending** for order against act observations (O-1, O-6) |
| **AE-6** | Observation lost or recovered | HOSTING §4.3 unexpected exit; recovery through thread reads (post-restart results not observed, PIN-SPIKE P-13) | Not in OBS-1: HOSTING U-19 |
| **AE-7** | Run ended | The person's stop (V4-EXE-01) or the run owner's end. A turn's completion is not a run end | DESIGNED |

#### 2.5.3 What OBS-1 must observe for these cells

OBS-1 is one live Codex turn at pin 0.158.0, against a local model, that
calls a test tool (BRIEFS "After round 2"; DECISION-K1 K1-6; anything sent is
invented example material). For the cells above it must record, with the
supplier's own timestamps and the test double's receipt times:

- **O-1** For one model-issued call to a test-double MCP tool, the full
  sequence of notifications for that item (`item/started`, any
  `item/mcpToolCall/progress`, `item/completed`) and `turn/completed`, and
  whether `item/started` reaches the App **before** the test-double server
  receives the call (settles AW-1's limit and AE-5's order).
- **O-2** Whether the `mcpToolCall` item's server and tool equal the
  configured names, and its arguments are the model's arguments as an object
  (AW-1 mapping).
- **O-3** The completed item's result shape (content and structuredContent)
  for a normal result and for a tool-reported error, and whether such an
  error appears as status *failed* or as *completed* with error content
  (AW-8).
- **O-4** Whether an approval request is raised for the MCP call under the
  approval policy used, and where it falls in the sequence (AW-1, AW-2;
  also a HOSTING U-19 item).
- **O-5** For the turn's assistant text: how many `agentMessage` items there
  are, whether `phase` is reported by the local provider or absent, and
  whether the last `agentMessage` completes before `turn/completed` (AW-6
  m1/m2).
- **O-6** That the item identity is the same in `item/started` and
  `item/completed`, and the `turn/completed` status of a normal turn.
- **Optional, if the turn can include them without widening K1-6:** **O-7**
  a command-line test tool run through Codex command execution: the command
  field's form (argument list or shell string), source, status transitions,
  exit code and aggregated output, and the order of any approval request
  (AW-2, AW-9); **O-8** a file write: one `fileChange` item per patch or
  several, and whether paths are absolute or relative (AW-7); **O-9**
  whether the model, asked to request a person's act, uses
  `item/tool/requestUserInput` (AE-3).

When OBS-1's record exists, each "OBS-1 pending" cell is restated from it
(dated, at one version; not qualification).

---

### 2.6 Operating sequences with failure behaviour (current phase; S1-C EXEC 7)

**SQ-A — App run on X** (e.g. E1 ⟨rev-A2⟩; either native path). "Record"
is what is left in the run record (RS) or the report.

| Step | Action | By | Record | Failure: what fails · who reports · record · next |
|---|---|---|---|---|
| A-1 | Selection; CK-1 report (§3) | Person; checker | Report; RS R14 reference | Catalog unreadable (CF-1) or revision not resolvable (CF-2) · the checker · report *not established* / "selected revision not resolvable" · the person may still start the run (CC-3) or choose again |
| A-2 | Run start; CK-2 report; the recorder writes CE-1 for each checkpoint and CE-2 for each invalid one | Person; checker; recorder | Report; `checkpoint_listed`, `declaration_finding` | Declaration unreadable at the resolved revision (RP-5) · the recorder · "declaration not resolvable — reconstruction not verified" · the run may still start; no arrival can be evaluated |
| A-3 | The workflow, with its checkpoints, is supplied to the agent through the supplier's additive guidance inputs (HOSTING S-6; DEL-02-04) | App | Supplied-guidance evidence (HOSTING §8.2 → RS R3) | Evidence not observed · HOSTING · *supplied* **unknown** (R2-20) · recording of arrivals is unaffected |
| A-4 | The agent works; native items are delivered | Agent; supplier | Operation entries (RS R7) by their owners; CE-12 while an arrival waits | Notification stream lost or the supplier exits · HOSTING §4.3 · `observation_lost` · recovery as the same run (RP-1; RE-4) |
| A-5 | Reached-when met (§2.5) | Recorder | `arrival`; SP-6 entries; `disposition` | A bound referent's content identity is not obtainable (RS L-3) · the recorder · the arrival with that referent's identity "unknown (unavailable)" · no act can count for that referent until it is obtained (SP-4) |
| A-6 | The agent asks the person for the act (K1-1) | Agent | `request_observed` where structured (RC-5) | No structured request observed · — · nothing ("no request observed" is shown) · nothing follows from it |
| A-7 | The person acts: host content in the host's own view; App content in the App act control (RC-6) | Person | Human-act record (RS §6) by the capturing surface or a faithful recorder | Host offers no capture-evidence reference (SWBPIPE, SQ-01) · the recorder · no act entry (a human-act record needs one, RS §6.1, HA-1); the missing reference is an RS R11 evidence limit · the label stays *waiting*. App control not built (DEL-01-04) · — · nothing to record · label stays *waiting* |
| A-8 | The act is observed (AE-1, AE-2) | Recorder | `act_counted` / `act_not_counted` / `item_decision` / `control_relation`; `disposition` | On X no read shows it (AW-10) · — · nothing; label stays *waiting* · a later read records it with its own time. A read is lost · ADAPTER · `observation_lost`; A5 items *unknown* (MX-3) · recovery (RP-1) |
| A-9 | First agent run action after *performed* | Recorder | `run_resumed` | Relative order of the act and the action cannot be established (OBS-1 O-1) · the recorder · order reported (RP-8) · no resume point is claimed from an unestablished order |
| A-10 | A content change is observed (read or outcome) | Recorder | `act_lapsed`; `disposition` (RC-8) | Method designations differ or the identity is unavailable (RS L-2, L-3) · the recorder · lapse state *unknown (incomparable / unavailable)* · no lapse and no currency is claimed |
| A-11 | The person ends the run | Person; recorder | `run_ended` | The App exits without an end · — · none; the run is **interrupted** (RE-4) · the next start recovers the same run, or the run owner records "interruption not recovered" |
| A-12 | Recording itself fails: the run record cannot be written (for example storage unavailable or a writer error) | Recorder | — during the failure; then `recording_gap` {from, to, cause} | The App tells the person that the run record is not being written. That is a statement about the product's own recording, not a response to an arrival (RC-4); nothing is paused, stopped or refused (PH-2). Observations still held are written when writing resumes, each with its own evidenced time and after the gap entry; anything not held is not reconstructed, and deciding observations in the gap stay *unknown* (RP-3). Nothing is back-filled (RP-1) |

**SQ-T — App → host transfer** (current phase; §6.3 TR-1…TR-8). The record
is the trace (RS R2 links, each marked original or revised). In the current
phase the carriage manifest lists checkpoints as declared (name, act kind,
reached-when kind, subject class) and claims no hold support.

| Step | Action | By | Record | Failure: what fails · who reports · record · next |
|---|---|---|---|---|
| T-1 | Select a **registered** revision (TR-1) | Person; DEL-02-02 | *selected* | A draft is chosen · DEL-02-02 · "draft only — not a workflow identity" · register it first |
| T-2 | Resolve and verify (TR-2) | Transfer tracer | *resolved* with verification | Bytes do not recompute to the revision (TF-1) · tracer · "revision not verified" · the transfer stops |
| T-3 | CK-4 report against the destination catalog (TR-3) | Checker | Report reference | Destination catalog not available · checker · "destination catalog not available" · carriage continues (TF-5) |
| T-4 | Prepare the carriage manifest (TR-4) | Tracer | *exported*, with transfer identity | Manifest cannot be written · tracer · "not exported" · retry keeps the source tuple with a new transfer identity |
| T-5 | The person relays package and manifest (TR-5; DEP-001) | Person | *relayed* where the person records it | Relay incomplete (TF-2) · host listing or the person · "not received (incomplete)" · new attempt, new transfer identity |
| T-6 | The host lists it unadapted (TR-6) | Host | *received*, by relayed evidence | Receiving capability unavailable (TF-3); declared part not established at the destination (TF-4); origin not preserved (TF-7) · host evidence, relayed · the named outcome · none is hidden; SWBPIPE has no workflow library (SQ-17), so this step is AWAITING INPUT |
| T-7 | Host adaptation, if any (TR-7; §6.4) | Host | *adapted* with derived-from | Evidence not relayed (TF-6) · — · *adapted* "not observed" · — |
| T-8 | Host evidence relayed back (TR-8) | Person; host | Evidence references | Not relayed · — · links stay "not observed" · — |

---

### 2.7 App-side components (semantic responsibilities; S1-C EXEC 8)

Placement, process and sharing are not chosen (OI-013, OI-014; R12-2). The
table states what each App-side part takes, gives and never does, so that
any placement can be checked against it. PROPOSED (B2).

| Component | Inputs | Outputs | Receivers | Never |
|---|---|---|---|---|
| **Required-tool checker** (§3) | Declared part (WD §3.4, §4.2); catalog edition, entries, exposure, availability (C §2–§4); channel state (C §4.1); acting surface; occasion (§3.1) | The report (`compatibility-report.schema.json`) | RS R14 (reference); display (§9.2 DEL-05-02, DEL-04-02); DEL-09-09; the person before a run | Gates, grants or forbids a run (CC-3); rewrites a report (CC-1) |
| **Checkpoint recorder** (§2.4) | Declared checkpoints of the resolved revision (RP-5); native items (HOSTING §6.7); observations on X (ADAPTER §7.7); human-act records (RS §6); per-item decisions (P §4.3); A12 relations (ACT, AS) | Entries (`checkpoint-record-entries.schema.json`) | The RS writer (R8, R9, R11); display (§2.4.4) | Requests, pauses, interrupts, refuses, prompts or reads (RC-4); records an act without capture evidence (PH-4) |
| **Transfer tracer** (§6) | Selection (DEL-02-02); resolved bytes; the CK-4 report; relay records; host evidence by relay | Trace links; carriage manifest (TR-4) | RS R2; DEL-09-06 (RT-11) | Carries files (the person relays, DEP-001); lets a revised identity inherit a link (§6.1) |

The in-flight request register and custody across restart are DEL-01-02's
(HOSTING S-1, outside this increment); the recorder only reads what is
delivered.

**The placement question, prepared (OI-014; not asked in this pass).** Where
the App-side checker and recorder live: (a) inside the App, as local
implementations that conform to shared schemas and fixtures (this file's two
schemas and §7 cases); (b) a library shared by the App and a host's loop;
(c) a service. R12-2 keeps the choice open for the phase review and writes
each format as a schema with conformance fixtures, which every option needs.
Nothing in §2.4–§2.6 depends on the choice; a host's use of the same meanings
(LOOP §2.4) is the part the choice would affect.

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
| CR-12 | **Limitations** | E.g. "exposure is a fixture assumption (FXA-1)"; "version compatibility: equality only"; "destination catalog not available"; "evaluated on a test double"; and, for a governed checkpoint in a host loop (governance phase), the residual after-observation limit for kinds (b) and (c) that LOOP §2.4.4 states as a limit, not as a separate value (F-27) |
| CR-13 | **Evidence standing** | C's evidence-label mapping (illustrative / test-double / actual host) |
| CR-14 | **Model destination** (App runs on X) | The destination selected **at report time**, local or cloud, shown as information only. That host content may flow to the selected model with no gate is SETTLED by DECISION-2 (D5). Recording and showing it is **SETTLED**: the DECISION-2 reading confirmed by the owner (SCA-V4-001 OWNER_ITEMS O-10, accepted at `APP-V4-BASIS-ALIGN-20260928` DECISION-7; R9-4; R10-11) (R5-4). Per-turn recording belongs to the run record (§6.1), not to the report. Never an outcome, a gate or a pass condition |

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
operation, or at least one is App-side. One declared case lies outside it
(V6 m-7): an A5 or kind (a) checkpoint whose **declared** held-actions
element neither shows host operations only nor marks an App-side step. Under
WD §4.3.1's two forms that element is malformed. R10-10 rules it
(INTEGRATION; governance phase only): the HS-5 conservative default applies
to any **declared** held-actions element that does not show host operations
only, whatever the checkpoint kind. The case is not invalid (HS-1), and no
new failure row arises. R7-3's derivation for an **absent** element on an A5
or kind (a) checkpoint is unchanged. No fixture is such a case.

| # | Surface and checkpoint | Value |
|---|---|---|
| HS-1 | Any surface; the checkpoint is invalid (FB-03, FB-13, FB-16; an A12 declaration naming no setting content, R5-3) or not established (FB-04) | **No value**. The checkpoint is reported invalid / not established and never evaluated; the check result is *not established* via the declaration (§3.5). Confirmed by R6-1 (F-22) |
| HS-2 | Host run on E | **enforced by the host loop** |
| HS-5 | App run; **at least one held action is App-side**: an App agent turn (e.g. a Return or summary step), an App tool or harness action (incl. kind (a) on a harness capability, R4-21), an App file write, or any action on App content (e.g. A4 on AF-1). Also, where a kind (b)/(c) checkpoint's declaration has no held-actions element, or where any checkpoint's **declared** held-actions element, whatever its kind, does not show host operations only (conservative default, PROPOSED (W7); finding F-28; scope ruled by R7-3 and, for a declared element, by R10-10). An A5 or kind (a) checkpoint with no held-actions element does **not** take this default: its held actions are derived — the governed operation(s) for A5, the held call for kind (a) (the definition above; WD §4.3.1; INTEGRATION, R7-3) — and it is valued by what those derived held actions are: HS-4/HS-3 when they are host operations; a kind (a) on a harness capability stays HS-5 (R4-21) | **not enforceable** in App runs (D6), whatever SQ-02 returns (R5-10; F-17) |
| HS-4 | App run on X; every held action is a host operation, but one of them has unagreed exposure (element 9 *unagreed*). **Except** where SQ-02 has been answered with no host-held route: then HS-3 (c) decides regardless of exposure (R8-2; I2 R8-Q-HS4). This covers SWBPIPE, where SQ-11 is answered with no exposure element | **not established** |
| HS-3 | App run on X; **every held action is a host operation** on the external channel. Examples: the governed operation of an A5 constraint (forced *propose*); the host operation a kind (a) checkpoint holds before dispatch; the host operations after arrival until the act | Depends on the status of SQ-02 (integrator confirmation, INTEGRATION; ADAPTER-v0.3 F-18/F-19). **(a)** SQ-02 answered, and host-held carriage or a host hold evidenced on a candidate → **enforced on the host route**. **(b)** SQ-02 unanswered → **not established**. **(c)** SQ-02 answered with no host-held route, so the constraint is only model-supplied or merely received → **not enforceable** → *unsupported*. *Enforced on the host route* is **never assumed**. **Current state (SWBPIPE): (c).** SQ-02 was answered 2026-09-28: route (iv), none planned (R8-2). A later SWBPIPE decision to plan a route is a revision trigger |

**Classification of the fixture checkpoints (R6-1; R8-2).** In Phase 1 none
of these checkpoints takes a value (§2.1 PH-3). The two value columns are
governance-phase values, reading each checkpoint as if declared governed (no
fixture declares the flag; GV-5). The X column applies SWBPIPE's SQ-02 answer
to the fixture's external surface, as I2 Part 2 does.

| Checkpoint | Declared held actions (WD-EX-v0.5; unchanged in WD-EX-v0.6 and WD-EX-v0.7) | Governance phase: App run on X | Governance phase: host run on E |
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
**recording** content applies (§2.1, closing paragraph), as the
current-phase recorder (§2.4) states and cites it; §4 is the overlay that
adds hold content to the same arrivals. No rule here holds,
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
| **waiting** | requested (purpose, scope); **lapsed at ‹t›** (before resume, R2-19); **waiting — re-held, lapsed at ‹t› after resume** (§4.7); **no items remain** (§4.11); **A12 awaiting control confirmation** / **A12 refused by control: ‹reason›** (§4.10); **act on other content** (SB-2); **prior act not counted** (an earlier act whose content is no longer current or whose kind differs; under the governance-phase option SP-6F, any earlier act; §4.5); **act order unknown** (SP-6F only); **subject absent** (§4.7); **hold not enforceable** / **action during hold** (governance phase); **continued past ‹checkpoint› before ‹act›** (Phase 1, optional; PH-7); **run ended** |
| **performed** | performance ordinal; **by earlier act ‹act› at ‹t›** (an act captured before the arrival and counted, §4.5 SP-6); **answered by ‹n› acts**, each with its referents (§4.7 JA-1); per-item "accepted by ‹person›" (A5); **accepted — not applied: refused — stale** or **— application error (effect …)** (§4.11); **superseded by ‹act›** (A12); **resumed at ‹t›** |
| **resolved negatively** | A10 per item or act-declined event; **partial** (A5); path taken |
| **lapsed** | Only for an arrival whose run has ended and whose performing act lapsed after the end (R2-19); per referent |
| **unknown** | Which observation was lost; last observed state |

A checkpoint's displayed disposition is that of its **current arrivals**
(§4.13); earlier arrivals remain history.

### 4.4 Events consumed

| Event | Supplier | Effect class |
|---|---|---|
| Arrival (reached-when observed) | App observation (on the external channel it consumes DEL-03-03's observations of checkpoint arrivals and act records, SoW CLM-002, DEP-02-03-026, ADAPTER §7.7; how an App run observes an arrival is §2.5 AW-1…AW-12) / loop (LOOP §2.4.1); host outcome (P §9) | Creates an arrival |
| Human act observed (with capture evidence) | Capturing surface; faithful record citing it (RS §6) | Candidate satisfying act |
| A10 per item; item-left event; all-items-decided | Host via P §4.3 | A5 evaluation |
| Act-declined event | Capturing surface (R2-5) | Negative |
| Act-lapsed event | Host / record reader (RS L-6) | Lapse |
| Act superseded (A12) | Control (R2-7) | Annotation |
| A12 control relation: established ⟨version⟩ / refused ⟨reason⟩ / pending | Control surface (AP §2.1 A12; AS) | A12 evaluation |
| Applied outcome with resulting objects | Host (P §9, R2-14) | Binding for "objects changed by a named outcome" |
| Observation lost / recovered | Executor (App: §2.5 AW-12, AE-6; or loop) | Unknown handling |
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
| SP-5 | Scope of *a* covers the referents (A5 evaluated per item, §4.11), or *a* is one of a set of acts that together cover them, each meeting the other conditions for the referents it covers (§4.7 JA-1; DECISION-K1 K1-3) | WD §4.3.1 scope; DECISION-K1 K1-3 |
| SP-6 | **Earlier act counts (current phase; SETTLED by DECISION-K1 K1-2; U-E4 closed).** No ordering condition: an act captured before the arrival event satisfies *X* when the other conditions hold, that is, when it is of the required kind and the content it was made on is still current (SP-4; for A12, the setting it established is still in force, not superseded, R2-7). The record cites the earlier act and its capture time ("performed by earlier act ‹act› at ‹t›"). An arrival whose bound scope such acts already cover is recorded reached and *performed* at its arrival event. **SP-6F Fresh act (governance-phase option, retained; PROPOSED; formerly SP-6, R4-5):** a workflow that takes up the governance phase may require the act to be captured at or after the arrival event, ordering by a request relation where the capturing surface records one, otherwise by evidenced times; an earlier act is then shown "prior act not counted", and if the order cannot be established, *a* does not satisfy and *X* shows "act order unknown". How a workflow takes up SP-6F is not defined in this increment (SoW TBD-006) | DECISION-K1 K1-2; V4-REC-05; below |
| SP-7 | For A12: the control relation is **established** (§4.10) | ADOPTED (R4-6) |
| SP-8 | *a* is none of: act-declined event, A8, A3 findings, A14 settlement, success, receipt, host checks passed | I-2; R2-8 |

**Why SP-6 (DECISION-K1 K1-2).** The owner decided that, in the current
phase, an earlier act counts when it is of the required kind and the content
it was made on is still current. The record stays truthful because it cites
the earlier act and its time, and the act is already bound to its content,
so an edit lapses it either way (SP-4; §4.7). A grant set before its
checkpoint and still in force is not repeated (CH-12 (iii)). The label "prior
act not counted" (RS R8 and L-13 wording; V17-A N-4) stays only for an earlier act whose content
is no longer current or whose kind differs, and for any earlier act under
SP-6F. SP-6 adds no ordering *between act kinds* (I-3 stands). **SP-6F**
keeps the earlier reading (R4-5) as an option for a workflow that takes up
the governance phase: a checkpoint requests an act *with its declared purpose
and scope* (WD §4.3.1; IR1C-14), and an act captured before the arrival was
not made in answer to that request. For A5 at kind (c) *queued* the order
question never arises, because A5 can only follow *queued*.

### 4.6 Transition table (per arrival)

| From | Event / condition | To | Also recorded |
|---|---|---|---|
| (none) | Arrival event observed | **waiting** | "checkpoint reached" with bound subject, purpose, scope. Governance phase: act request issued; run holds. Current phase: nothing is held (PH-2); the agent carrying out the workflow asks for the act, and the request is recorded where it can be identified (R9-1; DECISION-K1 K1-1). An earlier act that already satisfies SP-1…SP-8 answers the arrival at once (SP-6) |
| (none) | Run ends, reached-when never observed | checkpoint **not reached** | Run-ended event lists it |
| (none) | Deciding observation for arrival lost | **unknown** | Last observed state |
| waiting | Act satisfying SP-1…SP-8 (A4/A6/A7/A12) | **performed** (ordinal n) | Act reference; for an earlier act, "by earlier act ‹act› at ‹t›" (SP-6) |
| waiting | Acts that together satisfy SP-1…SP-8 over the bound scope (JA-1) | **performed** (ordinal n) | Each act with its referents and time |
| waiting | A5 evaluation gives *performed* (§4.11) | **performed** | Per-item acts |
| waiting | A5 evaluation gives *resolved negatively* | **resolved negatively** | Partial annotation if mixed |
| waiting | Act-declined event on this subject (A4/A6/A7/A12) | **resolved negatively** | Declared path follows (§4.8) |
| waiting | A12 refused / pending / on other content / prior act not counted / order unknown (SP-6F) | waiting | Annotation (§4.3) |
| waiting | Observation of acts lost during the wait | waiting (governance phase: the run holds; §4.12) | "act observation interrupted" |
| waiting | Run ends | waiting (final) | Run-ended event (R2-5) |
| performed | Act-lapsed event **before** resume point | **waiting** "lapsed at ‹t›" | R2-19 |
| performed | Act-lapsed event **after** resume point, run live | **waiting — re-held, lapsed at ‹t› after resume** (governance phase). Phase 1: the act-lapsed event is recorded, labelled **"act lapsed at ‹t›"** (nothing says *waiting*; R8-12 item 1), and no re-hold follows (PH-8) | §4.7 |
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
plan requires (PH-8; confirmed INTEGRATION by R8-11 item 1).

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
- **RH-6** A satisfying act, or a joint answer (JA-1), makes the arrival
  *performed* with the next performance ordinal; a new resume point follows.
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

**Why re-hold rather than report only (governance phase).** In the governance
phase the run waits at the checkpoint until the person's act: that is the
holding clause of V4-WF-05 and V4-HI-42, which the amended texts phase to the
governance layer. SoW AC-002, as revised, says that "for a workflow that
takes up the governance phase, the checkpoint also keeps the run waiting
until that evidence". Continuing on an act whose bound
content changed would let later work rest on an act that no longer covers
current content (V4-HI-32). RH-3/RH-4 keep history truthful without
rewriting it.

**Partial lapse and joint answer (SETTLED by DECISION-K1 K1-3; closes WD
U-05c, AP U-03, RS U-07 and U-E3; both phases).** When only some referents
lapse, before or after resume:

- the whole bound scope is shown, with the lapsed referents marked, so the
  person sees which referents the earlier act still covers;
- **JA-1 Joint answer.** Two or more acts may together answer one arrival.
  Each meets SP-1…SP-4 and SP-6…SP-8 for the referents it covers, the set
  covers the whole bound scope (SP-5), and each cites its items. When one act
  covered several referents and only some change, a new act on the changed
  referents alone answers the arrival together with the earlier act for the
  unchanged referents. The record shows the arrival answered by the set, each
  act with its referents and time;
- a new act over the whole current scope also answers it.

Case CH-8 is released (DESIGNED).

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
  Absent path (R10-7): in the current phase the agent follows the plan it
  worked out with the person; in the governance phase, for a governed
  checkpoint, → stop. In both phases the run is never recorded as if the
  act were positive.
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
  continuation itself observes. An act made before one of its arrivals
  (including an RE-2 post-end act) is not inherited, but it counts at that
  arrival under SP-6 when it is of the required kind and its bound content
  is still current, and the record cites it with its time (DECISION-K1
  K1-2). Under SP-6F it is shown "prior act not counted".
- **RE-4 Interruption is not run end.** Loss of observation, an App restart
  or a loop restart without a run-ended event leaves the run **interrupted**
  and resumable as the same run (§4.12). If recovery is impossible, the run
  owner records a run-ended event with cause "interruption not recovered";
  dispositions are as reconstructed, and *unknown* stays unknown.
- **RE-5 Starting a run** is not an act in R-1's list and is not reserved; the
  run record names who started it.

**Why no resumption.** An ended run's record is evidence for later
reconstruction (DEL-09-11). Reopening it would let a later act rewrite a
closed disposition (V4-REC-05). A continuation keeps both runs truthful and
linked: a later act is recorded against the ended run's subject and counts
only at the continuation's own arrivals (SP-6).

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
- The subject is an **operation-class** grant setting only. A checkpoint
  cannot require a network-destination grant (ACT §2.7) in this increment;
  that is a possible later extension, PROPOSED, with no definition (R10-9).

| Control relation on the A12 | Arrival effect | Shown |
|---|---|---|
| **established ⟨settings version⟩** (display *effective*, person-set) | Counts (with SP-1…SP-6; an A12 established before the arrival counts while its setting is still in force, SP-6) → **performed** | A12 reference and version |
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
| RP-2 **Arrivals during interruption.** | An arrival whose event occurred while observation was lost is recorded on recovery with the event's own evidenced time. Under SP-6F the order is taken against that time, so an act captured after the event but before recovery counts; under SP-6 (current phase) the order does not decide |
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
| CAP-3 **Direct capture record.** | Operating the control makes a human-act record with recording mode *direct capture* and a **capture-evidence reference** {act identity, actor, act kind, bound content identity with method designation, scope, purpose, time, capturing surface "App interface", arrival reference where the act answers an arrival already reached (an earlier act has none and is cited by the arrival it answers, SP-6)}. The record meaning is DEL-04-03's (RS §6) |
| CAP-4 **Not operable by automation.** | No agent tool, MCP operation, App rule or supplier request can operate the control or produce its record (D2; R-2). An agent may *request* the act (A8) |
| CAP-5 **Not capture evidence: tool permission.** | An A14 settlement from any origin (the person, the user's Codex mode, an App named-rule decline) is never act evidence (D3; R2-8) |
| CAP-6 **Not capture evidence: user-input and elicitation answers.** | Answers to supplier person-input requests (at 0.158.0 `item/tool/requestUserInput`, `mcpServer/elicitation/request`; HOSTING R9) are **input to the agent**, not act evidence, even when the person gives them. Their wording is authored by the agent or an MCP server, they cannot guarantee the kind/subject/scope/purpose binding of CAP-2, and their content goes to the agent. They are conversation (WD I-5). A question the agent asks this way may be an A8 request, if it names kind, subject and purpose. The App may respond by presenting its own CAP-2 control |
| CAP-7 **Not capture evidence: conversation.** | A chat statement ("I checked it") never satisfies (I-5; FB-15) |
| CAP-8 **Person identity.** | The record names the person from what the App can observe: the name the person set in the App, the operating-system account, and the Codex account when Codex reports one, marked **identity not verified** (SETTLED by DECISION-K1 K1-4; U-E8 closed). A verified identity is a governance-phase matter. A7's "accountable professional" is recorded as the person's own statement, with an evidence limit |
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
| **supplied** | These bytes were supplied to the agent or loop, per thread/turn, with source and content identity | Tuple and content identity | App: DEL-01-01 HOSTING §8.2 via DEL-02-04, with the **model destination per turn** as HOSTING §8.3 reports it: requested and effective kept separate, re-routes recorded with their turn, *unknown* for unobserved turns (R5-4; recording and showing SETTLED by OWNER_ITEMS O-10, R9-4, R10-11; information only); host: loop run association (SQ-19 (a)) | **unknown** (R2-20; U-29) |
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

## 7. Fixture cases on FX-PIPE-01 (OUT-003 design; none run against a candidate; some run on the local design prototype, §7.4)

All material is invented fixture subject matter.
- **From C-v0.4 §10** (FX-PIPE-01; carried in C-v0.7 §10): FX-W1, g1, R-100, S-1…S-5, LC-1, Engineer
  A, OP-C1…OP-C12, T1…T17 (incl. T4a, T16a), Tg, B1/B2, PR-1/PR-2,
  RC-1…RC-3, fixture assumptions **FXA-1…FXA-5**, App-side subjects
  **LIB-A1** ⟨fx-proj⟩, **LIB-A2** ⟨fx-app-import⟩ and **AF-1**
  (⟨AF-1@f1⟩/⟨AF-1@f2⟩, ⟨m-fx-file⟩), editions e1/e2, and variants V-S1,
  V-CP1, V-NP1, V-R1, V-X1, V-OU1, V-ED1.
- **V-GR1** (C-v0.5 §10.4; carried in C-v0.7 §10.4): run 13 of E1d on E. GR-1: `CP-grant` arrives
  at r15. GR-2: T15's A12 is captured after the arrival. GR-3: the held
  OP-C9 call is dispatched unchanged as T16. Sub-variants: GR-P (pending,
  then confirmation lost), GR-R (refused by the control), GR-S (a later
  established A12 narrows the scope).
- **From WD-EX-v0.4** (carried in WD-EX-v0.7, with its Phase-1 and governance-phase readings): E1, E1b, E1c, E1d, E3–E8, and the E2 runs.
- ⟨rev-A2⟩/⟨rev-A3⟩ are DEL-02-03's workflow revision labels (C §10.1).

WD-EX local cases are cited **by content** (run name and step), with the
WD-EX-v0.4 label in brackets (R5-9). Retired EXEC local labels are not reused:
L-EXEC-5, L-EXEC-10, L-EXEC-16 and L-EXEC-19. v0.6 adds L-EXEC-31, L-EXEC-32
and L-EXEC-33 (the next free numbers), each with its reason.

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
| MT-17 | L-EXEC-33: E1 ⟨rev-A2g⟩, a variant of ⟨rev-A2⟩ that declares `CP-accept` **governed** (WD §4.3.1) and does not declare the flag on `CP-check`. Needed because no FX-PIPE-01 fixture declares the flag (GV-5), and SoW VER-002 exercises hold cases only for a workflow that takes up the governance phase. (i) App run on X; (ii) host run on E | (i), (ii) **passes** on the required tools and the channel state; the flag is shown on `CP-accept` (PH-9); both checkpoints listed as guidance | Only the governed checkpoint takes a value (GV-2). (i) `CP-accept` **not enforceable** (HS-3 (c)); `CP-check` stays plan guidance with no value → **does not pass — unsupported** ("checkpoint hold not enforceable on this surface: CP-accept"). (ii) `CP-accept` **enforced by the host loop** (HS-2); passes, subject to host evidence (SWBPIPE has no host loop, SQ-20) | DESIGNED; prototype ran (§7.4) |

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
| CH-7 **Lapse after resume → re-hold** | WD-EX R-4 (ii) "after resume, while the agent is writing `summary`" [on L-WDEX-1]: `CP-check` bound to S-5, R-100 and S-3, performed; Engineer A edits S-3 | Act-lapsed event recorded for S-3. `checked-rows` standing shown lapsed for S-3. Label **"act lapsed at ‹t›"** (R8-12 item 1). The run is **not** re-held (PH-8). The agent re-requests A4 as its plan requires, and a new A4 over the current scope is recorded when performed. Later actions may carry "continued past CP-check before A4" | Act-lapsed event; **waiting — re-held, lapsed at ‹t› after resume**; run holds at its next action; `checked-rows` standing shown lapsed for S-3; the request covers the whole scope with S-3 marked; a new A4 over the whole current scope → **performed** (ordinal 2) | DESIGNED |
| CH-8 **Partial lapse, narrower act** | CH-7, then an A4 on S-3 only | The A4 on S-3 is recorded. With the earlier A4 for S-5 and R-100, whose content is unchanged, it answers `CP-check`: recorded as performed, answered by two acts, each citing its referents (JA-1; DECISION-K1 K1-3) | The re-held arrival becomes **performed** (ordinal 2), answered by the earlier A4 (S-5, R-100) and the new A4 (S-3), each citing its referents (JA-1); a new resume point follows | DESIGNED (released by DECISION-K1 K1-3) |
| CH-9 **Run ended while waiting; post-end act; continuation** | (i) WD-EX R-12b "run end and continuation" [continuation L-WDEX-9]. (ii) L-EXEC-11: an E1b run stopped after `CP-review` arrives at T4; Engineer A then marks S-2 and S-3 checked; a continuation run *continues ⟨run⟩* re-reads and re-examines, producing `findings`. Needed to show a continuation whose checkpoint does arrive | Same as record | (i) Run 12 `CP-check` final **waiting**; post-end A4 "after run end"; continuation `CP-check` *not reached* until its own arrival. (ii) Ended `CP-review` final **waiting**; the continuation's `CP-review` binds S-2 and S-3 as read; the post-end A4s were made on that same, still current content and count (SP-6; DECISION-K1 K1-2): **performed** at the arrival, citing the post-end A4s and their times. Under SP-6F: the post-end A4s are "prior act not counted"; new A4s → **performed** | DESIGNED |
| CH-10 **Lapse after run end** | WD-EX R-4 (iii) "after the run ended"; WD-EX R-17 (C T16a, T17) | Same as record | **lapsed** per referent (S-3; S-4 under FXA-2) | DESIGNED |
| CH-11 **Refused A12 (no policy basis)** | L-EXEC-12: workflow `renumber-with-grant` (fixture) whose `CP-grant` declares the setting content {OP-C11's class, *direct*, {FX-W1; R-100}}, kind (a) before dispatch of OP-C11; after arrival Engineer A performs that A12 (C V-NP1). Needed because C V-GR1 GR-R leaves the refusal reason open; this case fixes it as *no policy basis* (R2-9) | Control **refused (no policy basis)** is recorded; `CP-grant` is unanswered in the record ("A12 refused by control"). No call is held by the App or loop. The host's own treatment of OP-C11 governs (direct *not permitted*, R2-9). (a) act-declined → recorded *resolved negatively*; (b) run stopped → run-ended recorded | Control **refused (no policy basis)**; `CP-grant` **waiting** "A12 refused by control"; held call not dispatched; then (a) act-declined → **resolved negatively**, or (b) run stopped → final waiting | DESIGNED; production HELD (R2-9) |
| CH-12 **A12 after arrival (V-GR1); pending then established; C order** | (i) C **V-GR1** GR-1…GR-3. (ii) L-EXEC-13: V-GR1 with the control confirmation observed after a delay and then **established**. Needed because C's **GR-P** covers pending followed by a **lost** confirmation, not by establishment. (iii) C main order: T15's A12 precedes the arrival at T16 (WD-EX R-16 (i); V-GR1 "main-order negative") | (i) T15's A12 (captured after the r15 arrival, established ⟨set-2⟩) is recorded as answering `CP-grant`, and the OP-C9 dispatch as T16 is recorded; no call was held. (ii) Pending, then established, recorded as observed. (iii) T15's A12, established ⟨set-2⟩ on the declared content and still in force, is recorded as answering `CP-grant` as an earlier act, cited with its time (SP-6; DECISION-K1 K1-2); the OP-C9 dispatch as T16 is recorded | (i) `CP-grant` **performed** by T15's A12 (captured after the r15 arrival, established ⟨set-2⟩); held OP-C9 call dispatched unchanged as T16. (ii) **waiting** "A12 awaiting control confirmation", then **performed**. GR-P itself: *waiting*, then **unknown**. (iii) `CP-grant` **performed** at its arrival by T15's A12 (an earlier act on the declared content; ⟨set-2⟩ still in force; cited with its time; SP-6); the OP-C9 call is dispatched unchanged as T16. Under SP-6F: T15's A12 is a **prior act not counted** (R5-7), and `CP-grant` **waiting** for a new A12 on the declared content | DESIGNED |
| CH-13 **Refused A12 does not supersede** | (i) C **GR-R** (refused at arrival: ⟨set-1⟩ stays in force). (ii) L-EXEC-14: after CH-12 (i) (performed, ⟨set-2⟩ in force), Engineer A performs a later A12 on overlapping classes that the control refuses. Needed because GR-R's refusal comes before any performance; this case shows a refusal **after** performance | Same as record: the refused A12 is recorded; it establishes nothing and supersedes nothing (R4-6) | (i) `CP-grant` **waiting** "A12 refused by control"; ⟨set-1⟩ not superseded. (ii) ⟨set-2⟩ stays in force, not superseded; `CP-grant` stays **performed** (R4-6) | DESIGNED |
| CH-14 **A12 supersession** | C **GR-S** (= WD-EX R-16 (iii)) | Same as record | **performed**, then "superseded by ‹later A12›"; not lapsed; no re-hold (RH-9) | DESIGNED |
| CH-15 **Mixed items** | LOOP FX-C5 / WD-EX R-2 (T11) | Same as record (MX-5) | MX-5: **resolved negatively**, partial (item 1 A5); on-mixed path: continue with item 1 | DESIGNED |
| CH-16 **Item left** | LOOP FX-C12 | Same as record (MX-4) | MX-4: **performed** over item 1; item 2 shown with item-left event; never "all accepted" | DESIGNED |
| CH-17 **All items left, re-draft** | L-EXEC-15: after T10, Engineer A edits S-3 before any decision; the host refuses both PR-2 items stale (item-left); the agent re-drafts a new proposal (local label L-EXEC-15-P, lineage PR-2), queued. Needed because WD-EX R-7b "all items left, replaced" [L-WDEX-16] uses A11 withdrawal, not stale refusal | Same as record (MX-6); no acceptance carried | Arrival 2 **waiting** "no items remain", closed "replaced by arrival 3"; arrival 3 waiting on L-EXEC-15-P items; no acceptance carried. (Fixture per-item staleness; on a whole-model host such as SWBPIPE any model change stales every queued item, R8-3) | DESIGNED |
| CH-18 **Accepted then stale** | C **V-S1** (= WD-EX R-14 "accepted, then stale") | Same as record (MX-7) | MX-7: disposition unchanged; item 1 annotated with both bases; `CP-check` not reached for item 1's objects | DESIGNED |
| CH-19 **Unknown item decision** | WD-EX R-6b "lost decision" [L-WDEX-4] | Same as record (MX-3) | MX-3: **unknown**; never performed or resolved negatively until item 2 is observed | DESIGNED |
| CH-20 **Prior act on current content** | L-EXEC-30: WD-EX E1b, T2–T4, with `CP-review` binding S-2 and S-3 as E1b declares it (the findings name the span S-2→S-3), and T2's A4 on S-2 captured before `CP-review`'s arrival at T4. Needed because WD-EX's own variant of this scenario binds S-2 only. Related single-support case: WD-EX R-9b "prior act" [E1b variant L-WDEX-7], `CP-review` binding S-2; its result (*performed* by T2's A4) is consistent with this case under SP-6 (DECISION-K1 K1-2) | Same as record | S-2's T2 A4 (⟨S-2@r12⟩, unchanged at T4) counts for S-2 as an earlier act, cited with its time (SP-6; DECISION-K1 K1-2). The arrival waits only for an A4 on the bound referents T2 does not cover (S-3): an A4 on S-3 after T4 → **performed**, answered by two acts (JA-1); an A4 on S-2 and S-3 (WD-EX R-E1b) → **performed**. Under SP-6F: T2's A4 shown "prior act not counted"; waiting until A4 on S-2 and S-3 after T4 | DESIGNED (SP-6 SETTLED by DECISION-K1 K1-2; SP-6F PROPOSED) |
| CH-21 **Held call across recovery** | LOOP FX-C8 variant L-EXEC-17: A4 performed on S-3 at B2; interruption before dispatch | No call is held (PH-2). On recovery, observation of any dispatched OP-C5 call is sought before any resubmission (RP-1 (b)). Nothing is dispatched on the machine's behalf | Recovery dispatches the same held OP-C5 call unchanged from the record; if its outcome is unknown, observation is sought and there is no new call (RP-4) | DESIGNED |
| CH-22 **App-side hold, not enforced** | L-EXEC-18: App run of E1 ⟨rev-A2⟩ on X; `CP-check` kind (b). In the same turn that produces `examination-report`, Codex also writes a file and calls OP-C1. Then the person sends a new message on the holding run. Needed because C describes no App-run turn | The arrival is recorded. Nothing is held and no hold is claimed. The person's turn is not blocked. The file write, the OP-C1 call and any agent action in the person's turn may carry "continued past CP-check before A4" (PH-7). There is no *unsupported*, and HP-3 and HP-4 are not used | Arrival **waiting**; hold support **not enforceable** (HS-5). HP-4: the App starts nothing further; the person's turn is **not blocked** and is carried with initiator *person-directed*. No interruption is relied on (HP-2 not adopted). The file write, the OP-C1 call, and any governed agent action in the person's turn are recorded as **action during hold**. HP-3 declines any permission request that reaches the App (origin in R13). No hold is claimed | DESIGNED |
| CH-23 **App-side capture** | C **AF-1** (App file in LIB-A1's project, ⟨AF-1@f1⟩): App-side workflow with an A4 checkpoint on AF-1. (i) The agent asks through a user-input request and the person answers "yes". (ii) The person marks AF-1 checked in the App act control (CAP-2). (iii) AF-1 is then edited to ⟨AF-1@f2⟩ | (i) Conversation; not an act (CAP-6). (ii) Direct capture → A4 recorded as performed (AWAITING INPUT, as governance). (iii) Act-lapsed event recorded (PH-8). No hold-support value | (i) Conversation; **waiting** (CAP-6). (ii) Direct capture with a capture-evidence reference, bound to ⟨AF-1@f1⟩ with ⟨m-fx-file⟩, actor per CAP-8 (*identity not verified*) → **performed**. (iii) Act-lapsed event; the RH/R2-19 sequence applies. Hold support **not enforceable** (HS-5, App content) | (i), (iii) DESIGNED; (ii) AWAITING INPUT (DEL-01-04 control; its obligation proposed for DEL-01-04's contract, DECISION-K1 K1-4) |
| CH-24 **Subject absent** | L-EXEC-20: after CH-7's performance, S-5 is deleted before resume | Same as record: *subject absent* | Act lapsed (subject absent); **waiting "subject absent"**; only an act-declined event or run end closes it | DESIGNED (U-E7) |
| CH-25 **Tool permission during hold** | WD-EX R-15 "tool permission (App)" during a hold, plus HP-3 | A14 changes nothing in the record (S-R). HP-3 is not used | A14 changes no disposition; an App named-rule decline, if used, is recorded with truthful origin in R13 only | DESIGNED |
| CH-26 **Invalid declarations** | LOOP FX-C13; WD VC-29 variants | Reported invalid / not established as a declaration defect; no arrival recorded; the requirement-check result is **unchanged** by it (PH-3; R8-2) | Reported invalid / not established; no arrival; no hold-support value (HS-1); check **not established** | DESIGNED |
| CH-27 **Constraint forced proposal** | C V-CP1 / LOOP FX-C9 / WD VC-11; over X also ADAPTER XF-25/XF-26 | No constraint is carried or enforced by the App (R2-12 carriage assurance is governance phase). The agent, following the declaration as plan guidance (I-7), submits OP-C4 as a proposal and never adds a field the host schema lacks (R8-10). If a direct request is made, the host's own treatment decides and the outcome is recorded as observed; the App reports nothing as *not permitted* on the constraint's account. In the current phase I-7 is plan guidance for the agent, and the host's own treatment of its operations decides what the host does. V4-HI-42's request clause and record clause are in force for a checkpoint the run reaches. If the host applies directly, no proposal is queued, so `CP-accept` (kind (c) *queued*) is **not reached**: nothing is requested by reason of an arrival that did not occur, no A5 is forced, and none is recorded; the record shows the direct application under the grant (R8-11 item 2 and R8-12 item 2, as restated by R9-2 and corrected by R10-1; U-E24 closed) | As those cases. Over X: **not enforceable** → unsupported (SQ-02 answered 2026-09-28: no host-held route; HS-3 (c); R5-1, R5-2, R8-2). *Enforced on the host route* would need an evidenced host-held route. If a call is dispatched with the constraint omitted, "omitted governing checkpoint constraint" is recorded (R11) | Phase 1 DESIGNED. Governance phase: over X DESIGNED (value determined); on E **AWAITING INPUT** (U-E13) — SQ-20 answered 2026-09-28: no host loop (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3) |
| CH-28 **Host capture reference absent** | WD-EX R-9 (iii) | Same as record: the act is not recorded as performed without the reference (I-5; PH-4) | **waiting** (I-5) | DESIGNED; host side **AWAITING INPUT** (SQ-01; U-05b) — SQ-01 answered 2026-09-28: no capture-evidence reference; the Apply receipt names no person or time and does not survive restart (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3) |
| CH-29 **A12 checkpoint naming no setting** | L-EXEC-25: E1d variant whose `CP-grant` declaration states no classes, grant value or scope; an A8 presents ⟨set-2⟩ at arrival. Needed for R5-3 | Reported **invalid**, unconditionally (the A8 does not supply the subject, R5-3); no arrival recorded; the requirement-check result is unchanged by it (PH-3) | Checkpoint **invalid**, unconditionally: the A8 does not supply the subject (R5-3). Reported before the run; never evaluated; check **not established** (HS-1) | DESIGNED |
| CH-30 **Person's undo re-holds; never an A5** | (i) L-EXEC-27: C T16a then T17 with E1c, but the run is still live and past its resume point when Engineer A undoes RC-2 (OP-C10 → RC-3). Needed because WD-EX R-17's reading has the run already ended. (ii) L-EXEC-28: run 12 after WD-EX R-3; after resume Engineer A undoes the L-WDEX-1 receipt. Needed to show an undo against an A5 arrival | (i) The act-lapsed event is recorded (T16a's A4, ⟨S-4⟩ changed); the undo is recorded as the person's R7 operation; nothing re-holds (PH-8). (ii) `CP-accept`'s A5 stays recorded as performed (R2-15; RH-9); `CP-check`'s acts on S-5/S-3 are recorded lapsed, S-5 as subject absent | (i) T16a's A4 lapses (⟨S-4⟩ changed, FXA-2) → `CP-check` **waiting — re-held, lapsed at ‹t› after resume**. The undo is recorded as the person's R7 operation, **not** as action during hold (RH-8; R5-5, R5-6). (ii) `CP-accept` stays **performed**: A5 on the reversed items does not lapse (R2-15; RH-9). `CP-check`'s acts on S-5/S-3 lapse, S-5 as subject absent → re-held | DESIGNED |
| CH-31 **Earlier act not counted (current phase; R11-9)** | (i) L-EXEC-31: a new run 14 of E1b ⟨rev-B1⟩ from the App on X after C T14 (r15): OP-C1 read at r15 and OP-C3 findings naming the span S-2→S-3, so `CP-review` binds ⟨S-2@r15⟩ and ⟨S-3@r13⟩. T2's A4 on S-2, bound ⟨S-2@r12⟩, was captured before the arrival. Needed because CH-20 shows only an earlier act that counts. (ii) L-EXEC-32 (CH-32's workflow): an A6 on ⟨AF-1@f1⟩ captured before `CP-check` (A4) and `CP-approve` (A6) arrive on the same content | (i) T2's A4 is recorded **"prior act not counted"** (content no longer current: ⟨S-2@r12⟩ ≠ ⟨S-2@r15⟩; SP-4), and `CP-review` is recorded *waiting*; an A4 on S-2 and S-3 at their current content → **performed**. (ii) At `CP-approve` the earlier A6 counts (SP-6): **performed** at the arrival, "by earlier act ‹A6› at ‹t›". At `CP-check` it is **"prior act not counted"** (another kind; SP-1, I-1, RS HA-3), and `CP-check` is recorded *waiting* | (i) Same (also under SP-6F). (ii) Under SP-6F the A6 does not count at `CP-approve` either. Hold support **not enforceable** for (ii) in App runs (HS-5: App content) | (i) DESIGNED; recorder prototype ran (§7.4). (ii) DESIGNED as a record rule; the prototype ran with a test-double App act record; App capture of the A6 AWAITING INPUT (DEL-01-04) |
| CH-32 **Checking, approval and reliance kept apart (VER-003)** | L-EXEC-32: App-side workflow `report-signoff` {workflow, project, ⟨fx-proj⟩ (LIB-A1), `report-signoff`, ⟨rev-S1⟩} whose output `supports-review-report` is C **AF-1** (file form; §2.5 AW-7), with three checkpoints on it, each kind (b), subject class *named output*: `CP-check` (A4), `CP-approve` (A6, engineering approval) and `CP-rely` (A7; actor: the accountable professional). Engineer A, in the App act control, marks AF-1 checked (A4), approves it (A6) and states reliance as the accountable professional (A7). Then AF-1 is edited to ⟨AF-1@f2⟩. Needed because no fixture declares A6 or A7 (WD-EX E1, "Not declared") and SoW VER-003 asks for independently evidenced checking, approval and reliance | Each arrival is answered only by an act of its own kind (SP-1; I-1): the A4 never answers `CP-approve` or `CP-rely`; one control operation produces one act kind (CAP-2; RS HA-3). The A7's actor is recorded as the person's own statement, with its evidence limit and *identity not verified* (CAP-8; RS HA-4). No "approved", "certified" or "sealed" standing appears (S-L). The edit lapses each act on AF-1, labelled per RC-8 by where the run is | Same dispositions. Hold support **not enforceable** for all three in App runs (HS-5: App content) → *unsupported* | Record rules DESIGNED; arrival event OBS-1 pending (AW-7; O-8); positive App capture AWAITING INPUT (DEL-01-04) |
| CH-33 **A governed checkpoint beside an ungoverned one (VER-002)** | L-EXEC-33 (MT-17) as a host run on E along C T9–T11: `CP-accept` (governed) arrives at T10 (PR-2 *queued*); at T11 Engineer A accepts item 1 (A5) and rejects item 2 (A10). `CP-check` (not governed) later arrives on the applied item's objects | Both arrivals recorded; nothing held; the `governed` flag is only shown (PH-9). `CP-accept` → *resolved negatively*, partial (MX-5) | `CP-accept`: **waiting** and the run holds (**enforced by the host loop**, HS-2) until T11, then **resolved negatively**, partial, with its on-mixed path. `CP-check` stays plan guidance in the governance phase too (GV-2): recorded as in the current phase, with no hold and no value | DESIGNED; no host evidence can exist now (SWBPIPE has no host loop, SQ-20) |

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
| RT-11 **Evidence account for DEL-09-06** | All MT/CH/RT cases, joined by CA W14 cases: W14-01 ← RT-1; W14-02 ← RT-2, RT-3; W14-03 ← MT-1, MT-2, MT-3, MT-10, MT-15, MT-16; W14-04 ← CH-1, CH-27; W14-05 ← CH-2, CH-20, CH-23, CH-28, and from v0.6 CH-31 (R11-9; CA W14-05 cites it in node B7); W14-06 ← CH-6…CH-8, CH-10, CH-30; W14-07 ← CH-3…CH-5, CH-9, CH-21 (aligned to CA §8.2 by R10-11); W14-08 ← RT-5; W14-09 ← RT-6, RT-8; W14-10 ← RT-7. MT-17, CH-32 and CH-33 (v0.6) are not yet mapped to a W14 case (for node B7) | Inventory with candidate and source versions, case states, labels (C mapping), limitations and missing external inputs (SQ IDs as cited per case); names DEL-09-06 as joined-witness owner; claims no witness | DESIGNED |

### 7.4 What each case needs to run, and the local prototype (R12-1 verification; R12-3)

| Cases | Needs to run | Local prototype (run 2026-09-30) |
|---|---|---|
| MT-1…MT-10, MT-12…MT-17 | A catalog test double built from C §10.2 with the named variants; the fixture declared parts (WD-EX E1, E1c, E1d, E5, E6 and the L-EXEC variants); SWBPIPE's SQ-02 answer applied on X | **Ran** (`prototype/required_tool_check.py`, driven by `prototype/run_all.py`): 19 case runs (MT-5 and MT-17 on two surfaces, MT-12 on two editions), each in both phases. Every current-phase result and governance-phase value matched §7.1. All 38 reports validate against `compatibility-report.schema.json`; no current-phase report carries a hold-support value or a hold reason |
| MT-11 | A loop test double that offers an edition at run time (LOOP §2.3) | Not run |
| CH-7, CH-8, CH-10, CH-20, CH-31 | A recorder test double over scripted observations (CE events of §2.4.2) | **Ran** (`prototype/checkpoint_recorder.py`): the current-phase results above held, including JA-1 (CH-8, CH-20), SP-6 counted (CH-20, CH-31 (ii)) and not counted (CH-31), the post-resume label (CH-7) and the post-end lapse (CH-10). Every entries document validates against `checkpoint-record-entries.schema.json` |
| CH-1…CH-6, CH-9, CH-11…CH-19, CH-21, CH-24…CH-26, CH-29, CH-30 | The same recorder double, plus as each case needs a P item-decision double (CH-15…CH-19), an A12 control double (CH-11…CH-14) or an interruption double (CH-3, CH-4, CH-21); the governance columns also need a hold-machine double | Not run |
| CH-22; the arrival events of CH-32; every §2.5 cell marked OBS-1 pending | The App's Codex at pin 0.158.0 with a local model and a test-double MCP tool (OBS-1) | Not run: OBS-1 pending |
| CH-23 (ii); CH-32's positive capture | DEL-01-04's act control | AWAITING INPUT |
| CH-27, CH-28 host side; CH-33 host evidence | A host (SWBPIPE's answers: none offered) | AWAITING INPUT; host joins deferred (DECISION-3) |
| RT-1…RT-10 | A transfer-tracer double with a library double; the host side by relay | Not run |
| RT-11 | The account itself | — |

**Worked report for MT-1 (current phase).** The report the prototype renders
for MT-1 is the valid example instance
[`compatibility-report.example.valid.json`](compatibility-report.example.valid.json)
beside this file. Its elements: CR-1 `MT-1/current`; CR-2 {workflow, host,
⟨fx-root⟩, `supports-adjust`, ⟨rev-3⟩}, holding library ⟨fx-root⟩; CR-3
declared; CR-4 the FX-PIPE-01 test double, edition e2, readable; CR-5
surface E, channel enabled; CR-6 CK-1 with its time; CR-7 OP-C1, OP-C3 and
OP-C4 required and OP-C12 and OP-C5 optional, each *present* (entry v1,
exposed); CR-8 none; CR-9 `CP-accept` and `CP-check` listed as guidance
with no value; CR-10 **passes**, stated "requirement check passes against e2
on E at ‹t›" (PS-2); CR-11 none; CR-12 "evaluated on a test double
(FX-PIPE-01)" and "exposure is a fixture assumption (FXA-1)"; CR-13 test
double; CR-14 none (not an App run on X). The invalid example
[`compatibility-report.example.invalid.json`](compatibility-report.example.invalid.json)
adds a hold-support value to a current-phase checkpoint, gives a requirement
the outcome "compatible" and drops CR-10; the validator rejects all three.

---

## 8. Resolution register for items held for W7

| Held item (sources) | Resolution | Section | Standing at v0.2 |
|---|---|---|---|
| Re-hold after a lapse following resume (WD U-22; AP U-10; RS U-24; AS U-13; LOOP C-4, FX-C3; PANEL W-5e, PC-20) | Same arrival re-held: "waiting — re-held, lapsed at ‹t› after resume"; hold at next action boundary; history kept; whole-scope request; ended while re-held → waiting | §4.2 HD-5, §4.7 | **ADOPTED (R4-3)**; partial-lapse satisfaction **settled** by DECISION-K1 K1-3 (JA-1) |
| Resumption of an ended run; post-end acts (WD U-21; AP U-10, §2.3; RS U-23; AS U-11; LOOP §2.4.1, FX-C7b; PANEL W-5b, PC-21d; WD-EX R-12b) | No resumption; ended dispositions final (except R2-19 lapse); post-end acts shown "after run end"; continuation is a new run *continues ⟨run⟩* with nothing inherited; interruption ≠ run end | §4.9 | **ADOPTED (R4-4)**, standing PROPOSED |
| Refused A12 at a checkpoint (WD U-27, SB-4; AP U-13, §12.5; RS U-17; AS U-14; LOOP C-8, FX-C11; PANEL W-5g) | Refused → does not count, stays waiting with refusal shown; pending → waiting; unconfirmed → unknown; refused A12 does not supersede; declared setting content always binds (R5-3); A12 after arrival per V-GR1 (R5-7) | §4.10 | **ADOPTED (R4-6; R5-3)** |
| Confirmation of WD §4.3.7, mixed items and accepted-then-stale (WD U-20; R2-18; R3-3; AP U-09; RS U-18; AS U-09; P §4.3; LOOP C-7; PANEL W-5f) | **Confirmed**, with MX-3 (unknown item), MX-6 (replaced empty arrival), MX-8 (application error / unknown after A5) and MC-1…MC-4 | §4.11 | **CONFIRMED; additions ADOPTED (R4-7)** |
| Holding library (WD U-24; RS U-22; R2-20 "PROPOSED until W7"; LOOP §2.1; PANEL §3.2) | **Confirmed** as R2-20, plus HL-2 (source/destination at transfer) and HL-3 (not at *supplied*) | §6.2 | Confirmed; carried into RS by R4-11 (transfer links) |
| App-side capture (WD U-25; HOSTING §6.1, R9 "standing as act evidence") | CAP-1…CAP-9; user-input and elicitation answers are **not** act evidence; A13 locus per DEL-04-01; person identity SETTLED by DECISION-K1 K1-4 (CAP-8); App control construction carried | §5 | CAP-6 **ADOPTED (R4-12)**; CAP-1 per **R4-13**; CAP-8 **SETTLED** (DECISION-K1 K1-4); rest PROPOSED (W7); construction **carried** (DEL-01-04, later; its obligation proposed for DEL-01-04's contract, DECISION-K1 K1-4) |
| Transfer/adaptation procedure (WD U-18) | TR-1…TR-8, AD-1…AD-6, HR-1…HR-7, TF-1…TF-8; model destination recorded, never gated (R4-1) | §6 | PROPOSED (W7); destination per turn (R5-4); host links AWAITING INPUT (SQ-17…SQ-19) |
| Hold machine (WD §4.3.4 "DEL-02-03's (W7)"; §9 A-4; LOOP §10.1) | §4. **Phase 1:** recording only (§2.1). **Governance phase (retained):** the hold machine (§2.2) | §2.1, §2.2, §4 | Disposition logic PROPOSED (W7), with R4-3…R4-7 and R5-5 adopted. Hold-support values per R5-1 (§3.6), governance phase. App-side enforcement: D6 **closed for Phase 1** (DECISION-4; R8-2), re-opens with the governance phase. SQ-02 answered (route (iv)) for host-operation checkpoints (R5-10). Host placement `UNRESOLVED{OI-013}` (SQ-20: not decided; D-58 successor a SWBPIPE owner decision), sharing `UNRESOLVED{OI-014}` |
| ADAPTER U-X3 (retired to `UNRESOLVED{D6}`): GC-3 constraint assurance, GC-5 kind (a) on X | Governance phase: GC-3 and GC-5 follow §3.6 HS-3. SQ-02 was answered 2026-09-28 with no host-held route, so → *not enforceable* (HS-3 (c)); *enforced on the host route* only with host-held carriage or a host hold evidenced | §3.6 | **Resolved** (R5-1, R5-2, R8); host side answered: none |
| Multi-row A4 purpose after partial lapse, point of need "before DEL-02-03 re-hold design" (WD U-05c; AP U-03; RS U-07; CA DI-7) | **Decided by the owner** (DECISION-K1 K1-3): an act on the changed referents alone answers the arrival together with the earlier act for the unchanged referents (JA-1); CH-8 released | §4.7 | **SETTLED** (DECISION-K1 K1-3; was carried to C1, R4) |
| Version ordering, point of need "before DEL-02-03 required-tool fixtures" (WD U-07; C U-C9) | Equality only; MT-7 expects *version mismatch* | §3.4 EV-6 | **Carried** (SQ-18 (d)) |
| Harness capability names, point of need "before App-side required-tool check" (WD U-08) | *not established* until named; kind (a) on them not holdable (R4-21) | §3.4 EV-3; §3.6 | **Carried** |
| Constraint receipt, point of need "before W7 host-side fixtures" (WD U-19; P U-P10) | Phase 1: no constraint carried by the App (R8-1). Governance phase: CH-27 over X *not enforceable* (SQ-02 answered: no receipt, no host copy; a constraint field is refused as unknown); on E AWAITING INPUT per STD-2 | §7.2 | **Answered** (SQ-02: none); governance phase |

---

## 9. Interfaces

### 9.1 Expected from suppliers

| Supplier | Element | State | Used in |
|---|---|---|---|
| DEL-02-01 (WD; DEP-02-03-009) | Declared-part status; required tool reference elements; §4.2.4 vocabulary and pass rule (with the R4-8 reason); checkpoint elements, validity rules (with R5-3, R4-21), I-1…I-9, dispositions, §4.3.7 (with R4-7), §4.3.8 hold support (R5-1); identity tuple, chain, holding library, §6.4; WD-EX E1–E8 and E2 runs | WD-v0.4 and WD-EX-v0.4 read at `8fb51f07f`; WD-EX-v0.5 E1c/E1d/E8 read in the working tree (R6); WD-v0.5 rulings relayed by the coordinator. R8: WD-v0.6 adds the Phase-1 statement and the optional **`governed`** flag (PROPOSED) after this file in the same A1 pass. Current: WD-v0.7 and WD-EX-v0.7; WD-v0.6 was read whole at this pass, including §4.3.0 and §4.3.1 as finally written, before its Wave A edit in the same node. **v0.6:** §2.5 AW-6 uses the message-output designation WD adds in Wave B (node B1; R10-8), on condition that it is decidable from the item and its turn; AW-7 needs a path designation for file outputs, which WD §4.4 does not name (F-33) | §2.1, §2.2, §3, §4, §6, §7, §2.4, §2.5 |
| DEL-03-01 (C; DEP-02-03-011) | Catalog edition; entry identity/version (equality); exposure element 9; availability and reason; §4.1 results (App reporter of *channel not enabled*, R4-16); subject content identity; FX-PIPE-01 with FXA-1…FXA-5, LIB-A1, LIB-A2, AF-1, e1/e2, V-ED1, **V-GR1** with GR-P/GR-R/GR-S | C-v0.4 read at `8fb51f07f`; C-v0.5 §10.4 V-GR1 read in the working tree (R6). Current: C-v0.7 | §3, §4.5, §7 |
| DEL-03-02 (P; DEP-02-03-025, arc N-21) | Per-item dispositions; item-left events; all-items-decided; change-item content identity; applied outcome with resulting objects; stale and application-error outcomes; retry precedence; governing checkpoint constraint with **carriage assurance** (R5-2: host-held only in this increment); author identity possibly *unverified* (R4-15) | P-v0.4 read. Current: P-v0.7 | §3.6, §4.4, §4.11, §4.12 |
| DEL-04-01 (ACT; DEP-02-03-012) | A1–A14; closed list; act-declined event; A12 binding and supersession (R4-6); grant-setting subject (R5-3); A13 capture locus (U-X1; R4-13); person's own operations as R7 entries (R5-6); U-03 decided by the owner (DECISION-K1 K1-3), carried in ACT §4.3 as the joint-answer rule | ACT-v0.4 read. Current: ACT-POLICY-v0.7 | §4.5, §4.7, §4.10, §5 |
| DEL-04-02 (AS; the supplier's row DEP-04-02-023 only, no row in this deliverable's register) | Grant display states incl. *set by person, not yet confirmed*, *unconfirmed*, *refused (reason)* | AS-v0.4 read. Current: AS-v0.7 | §4.10 |
| DEL-04-03 (RS; DEP-02-03-013) | Human-act record, recording mode, capture-evidence reference; events; lapse rules; R5 model destination per turn (R5-4); R7 for the person's own operations (R5-6); R8 with the R4-10/R4-11 additions; R11 action during hold | RS-v0.4 read. Current: RS-v0.7 (§4 R11 read at this pass: the action-during-hold entry carries the turn initiator, F-24). **v0.6:** RS-v0.7 §3, §4 R8, R9, R11, §6 and §7 read for the record entries (§2.4.5); human acts are cited by RS §6 record identity; the RS R8 elements the entries add are listed in F-35 | §4, §5, §6, §2.4 |
| DEL-05-01 (LOOP; DEP-02-03-022) | Arrival observation (§2.4.1), binding (§2.4.2), events (§2.3), hold support in host loops (§2.4.4), dispatch record and own constraint evaluation (§6.2), retry rules (§6.3) | LOOP-v0.4 read. Current: LOOP-v0.7 (§2.4.4 read at this pass: residual limits stated per kind, F-27). **v0.6:** LOOP-v0.7 §2.4.0 and §2.4.1 read; §2.4 and §2.5 are the App counterparts of LP-3 and §2.4.1 | §3.6, §4 |
| DEL-01-01 (HOSTING; DEP-02-03-023, arc N-23) | Supplied-guidance evidence (§8.2); observed model destination per turn incl. `model/rerouted` (§8.3); request kinds and R9 (R4-12); HP-4 scope ruling from F-22 (INTEGRATION), closing HOSTING U-25 | HOSTING-v0.4 read; v0.5 F-22/U-25 read in the working tree. Current: HOSTING-BOUNDARY-v0.7. **v0.6:** §6.7, §6.8, §8.3 and §10 read, with the generated 0.158.0 bundles, for the native items §2.5 names (`observed-in-generated-types` only; no model turn observed, §8.1 L-3). §2.5.3 lists what OBS-1 must observe | §2, §5, §6.1, §2.5 |
| DEL-03-03 (ADAPTER; DEP-02-03-026, arc N-24) | Carriage assurance; GC-1…GC-5; §7.7 checkpoint observation on X — its observations of checkpoint arrivals and act records on the external channel, which this slice records (SoW CLM-002); model destination in channel status | ADAPTER-v0.2 read; ADAPTER-v0.3 F-18/F-19 (GC-3/GC-5, XF-26 alignment) relayed by the coordinator. Current: ADAPTER-v0.5 (§7.7 read at this pass: it describes the A5 kind (c) case and a general current-phase rule; kinds (a) and (b) on X are covered in neither file). **v0.6:** §2.5 covers kinds (a)–(c) on X for both native paths (R12-4), using ADAPTER §4.1 NM-1/NM-2, §4.5 and OC-9, and AE-1 for host-captured acts; ADAPTER §7.7 does not say who issues the host reads that show later outcomes and host-captured acts (F-32) | §3.6, §4.4, CH-22, CH-27, §2.5 |
| DEL-01-04 (later, D1; DEP-02-03-027, arc X-1) | App act control (CAP-2) and person identity, for the App-side positive capture fixtures only (CH-23 (ii)) | Not in this undertaking. DEL-01-04 has no Design file, and its ScopeOfWork does not name an act control or a person identity: the contribution is named by DEP-02-03-027 and not yet defined by the supplier. The act control's obligation is proposed for DEL-01-04's contract at the next amendment (DECISION-K1 K1-4); collected at this run's closeout. The person identity the App records is settled by the same decision (CAP-8). **v0.6:** the control is a standing facility, available whether or not an arrival is recorded (RC-6); the display meanings are SH-1…SH-5 (§2.4.4) | §5 |
| DEL-02-02 (later, D1; DEP-02-03-010) | Listing, selection, draft, review, registration, slot policy | Not in this undertaking | §6.5 |
| Host owner (DEP-001), via DEL-09-06 RELAY-v0.2 (now RELAY-v0.3, answered) | SQ-01 capture-evidence reference; SQ-02 constraint receipt and host holds (decides host-operation checkpoints only, R5-10; governance phase); SQ-04/SQ-05 first operation; SQ-11 exposure; SQ-17 receiving App workflows; SQ-18 adaptation, library identity, version statements; SQ-19 run records and supplied guidance; SQ-20 host placement; SQ-25 proxy control | Relayed; answered 2026-09-28; no commitment or contribution (RELAY §4). Answers are about SWBPIPE's current state: SQ-01 no capture-evidence reference; SQ-02 route (iv), none planned; SQ-11 no exposure element; SQ-17…SQ-19 no workflow library, adaptation, host loop or seat; SQ-20 not decided; SQ-25 host facility only, no proxy. Host joins deferred (DECISION-3) | §2, §3.6, §4, §6 |

### 9.2 Provided to receivers

| Receiver | Provided | Expected check at next comparison |
|---|---|---|
| DEL-02-01 (DEP-02-01-026) | §2.1 Phase-1 statement (PH-1…PH-10); §2.2 governance-phase scope and the `governed` opt-in (GV-1…GV-5); the R5-1 hold-support value set and HS-1…HS-5 as governance phase (for WD §4.3.8 and WD-EX E8); §3.5 check result and precedence; R5-3 subject rule; SP-6 (SETTLED by DECISION-K1 K1-2) with the governance-phase option SP-6F (PROPOSED); JA-1 (DECISION-K1 K1-3); AD-2 checkpoint comparison | WD/WD-EX v0.7: checkpoint guidance in Phase 1; `governed` flag with its meaning per phase; §4.2.4 R4-8 reason limited to governed checkpoints in the governance phase; VC-37, VC-43 and E8 two-part, with the same governance-phase values as MT-2, MT-15, MT-16 |
| DEL-05-01 (DEP-05-01-017) | Phase 1: the host's embedded loop enforces no hold (PH-2). Governance phase: hold-machine semantics (§4) for host loops; the value *enforced by the host loop*; RH-8/RH-9 undo rules. **v0.6:** the current-phase recorder (§2.4), whose event meanings LP-3 shares, and the App-run reached-when table (§2.5) as the App counterpart of LOOP §2.4.1, including the App-side answer to LOOP's R10-8 note (AW-6) | LOOP §2.4.4 relabelled governance phase (R8-8); uses the R5-1 set; C-4 per RH-8; LOOP §2.4.1's kind (b) note can cite WD's element and EXEC AW-6 |
| DEL-04-03 (DEP-04-03-025) | Checkpoint arrival, act and lapse events and compatibility reports (§4.4, §3.3; hold events are governance phase). Record needs, adopted by R4-10/R4-11; per-turn destination (R5-4); person's own operations as R7 (R5-6); RS E10/VC-17 corrected by R5-8. **v0.6:** the checkpoint record entries (§2.4.2; `checkpoint-record-entries.schema.json`) and the report format (`compatibility-report.schema.json`), both PROPOSED | RS v0.7 matches §3.6, §4 and §6 (Phase 1 and governance phase); RS R8, R9 and R11 carry the CE entries, including the elements listed in F-35 |
| DEL-03-03 (DEP-03-03-014) | The checkpoint statement for the current phase (§2.1): on this channel a checkpoint is plan guidance and no hold is claimed. The required-tool check (§3). Governance phase: the hold machine (§4) and hold-support values for X (§3.6 HS-3…HS-5; SQ-02 answered → HS-3 (c)); CH-22/CH-27 expectations in two parts. **v0.6:** what EXEC takes as the arrival and act observations on X for each native path (§2.5 AW-1, AW-2, AW-4, AW-8…AW-10; AE-1), the consumer side of N-24 | ADAPTER v0.5 GC-3, GC-5, §7.7, XF-25, XF-26 use the R5-1 set as governance phase; ADAPTER §7.7 states who issues the reads that observe later outcomes and host-captured acts (F-32) |
| DEL-09-06 (DEP-09-06-013; DEP-02-03-014) | Transfer trace (§6.1), carriage manifest meaning (§6.3), fixture design and the RT-11 W14 map; SQ citations per host item; F-17 closed for Phase 1 with D6 (R8-2). **v0.6:** CH-31, the current-phase case in which an earlier act does not count (R11-9), for W14-05; MT-17, CH-32 and CH-33, not yet mapped | CA v0.5: W14-03/W14-04 in two parts, matching MT-2 and MT-16 (Phase 1 passes; governance phase *unsupported*); CA W14-05 cites CH-31 (node B7) |
| DEL-05-02 (DEP-05-02-020), DEL-04-02 (DEP-04-02-017) | The checkpoint recording meanings displayed in the current phase (arrival, act recorded only when performed, the act-lapsed label; §2.1, §4.3, §4.6); display meanings of the §4.3 annotations and the §3.3 report; hold-support values, which are governance phase and not a current-phase display input. **v0.6:** the display meanings SH-1…SH-5 (§2.4.4), including what is never shown | PANEL W-5b/e/f/g and AS §4 re-pointed |
| DEL-03-04 (DEP-03-04-009) | The workflow compatibility, checkpoint and transfer receiving semantics, by version label and section: §2.1, §2.2, §3, §4, §6. **v0.6:** §2.4–§2.7 and the two schemas | GUIDE's entries and completeness comparison cite EXEC-v0.5 (GUIDE is re-pinned last) |
| DEL-01-01 (no register row names this; HOSTING §6.7 names DEL-02-03 as the recorder of the native items it delivers) | **v0.6:** which native items and requests EXEC uses (§2.5, RC-9) and the OBS-1 observation list (§2.5.3) | HOSTING's OBS-1 brief (node B6) covers O-1…O-6 |
| DEL-09-09 (DEP-09-09-023) | The per-surface compatibility report (§3.3 CR-1…CR-14, §3.5) and, for the governance phase only, the hold-support values (§3.6) | XT's cases use the report per surface and keep hold support as governance phase |
| Outside this increment: DEL-02-02 (DEP-02-02-015), DEL-09-02 (DEP-09-02-017), DEL-10-03 (DEP-10-03-009) | DEL-02-02: capability and checkpoint execution and round-trip support for the standalone workspace join (§3, §4.12, §6.5). DEL-09-02: the capability and checkpoint execution contribution (§3, §4, §7); its "scoped feature evidence" is named by DEP-09-02-017 and not yet produced here (no case has been run; OUT-001 is definition only). DEL-10-03: the workflow compatibility and checkpoint receiving obligations (§2, §3, §4, §10) | Not exercised in this increment |

---

## 10. Excluded acts and owners (REQ-006; AC-006)

| Excluded act | Owner | Interface here |
|---|---|---|
| Declaration and shared-allocation design | DEL-02-01 | §3.2, §4 consume |
| Review, registration, selection policy, drafts | DEL-02-02 (later, D1) | §6.5 routes |
| Catalog semantics | DEL-03-01 | §3.2 |
| Proposal and outcome semantics | DEL-03-02 | §4.11 |
| Operation-policy definition; adopted D2/D3 carriage | DEL-04-01 (U-03 decided by the owner, DECISION-K1 K1-3) | §4.5, §4.7 |
| Grant display definition | DEL-04-02 | §4.10 (display states consumed); §9.1 |
| Supplier observation (observed stock-Codex facts) | DEL-01-01 | §2.3, §3.2, §5 CAP-6, §6.1 *supplied*; §9.1 |
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
| F-3 | WD I-1; AP §4.2/§4.5; LOOP C-2, FX-C4; WD-EX R-16 | No rule relating capture time to arrival | R4-5 adopts SP-6 as PROPOSED; U-E4 open; FX-C4 and R-16 repaired by their owners. **Closed (DECISION-K1 K1-2):** in the current phase an earlier act of the required kind on current content counts (SP-6); capture after arrival is the governance-phase option SP-6F |
| F-4 | WD U-21; AP §2.3; RS; LOOP; PANEL | Resumption deferral; continuation link missing | Closed: R4-4 |
| F-5 | AP §2.5; RS L-0; LOOP; PANEL W-5g | A refused later A12 would supersede | Closed: R4-6 |
| F-6 | RS R8; AS §4 | R3-1 class missing | Closed: R4-10 |
| F-7 | RS §3, R8, R11 | Record elements missing | Closed: R4-11 |
| F-8 | WD §4.2.4 | No *unsupported* reason for a checkpoint hold | Closed: R4-8 |
| F-9 | HOSTING §6.1, R9 | Elicitation standing undefined | Closed: R4-12 |
| F-10 | SoW REQ-002 vs CLM-003 | No App hold point allocated | **Carried to C1** as a SoW gap; home `UNRESOLVED{D6}` (R4-2). R8: Phase 1 needs no App hold point (PH-2); the gap belongs to the governance phase (F-29). **Closed (v0.5; R9-8):** SoW CLM-003, as revised by SCA-V4-001, states that in the current phase no App-side hold point is needed and that D6 re-opens with the governance phase (TBD-006) |
| F-11 | SoW TBD-001/002; DEP-02-03-015/016 | OI-001/002 still called open | **Carried to C1**. **Closed (v0.5; R9-8):** SoW TBD-001 and TBD-002, as revised by SCA-V4-001, record the DECISION-1 D2/D3 rulings; register rows DEP-02-03-015 and DEP-02-03-016 are RETIRED |
| F-12 | CASE-002 M1 DEL-02-02 row | Changed-draft return uncompared | **Carried to C1** (out-of-scope receiver, D1) |
| F-13 | AP §4.2 | Grant-setting referent undefined without A8 | Closed: R4-9 |
| F-14 | WD U-05c / AP U-03 | Point of need reached without ruling | **Carried to C1** as an open owner question (R4); U-E3. **Closed** by DECISION-K1 K1-3 (§4.7 JA-1; CH-8 released) |
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
| F-23 | R5-7 cost; CH-12 (iii) | Under SP-6 on C's main order, the person must repeat an A12 whose content (⟨set-2⟩) is already in force. The repeat is a new A12 on identical content: it supersedes the earlier one (R4-6), and the record shows two acts for one setting. This is visible friction every time a grant precedes its checkpoint | For the owner with U-E4. If SP-6 stays, DEL-04-02/DEL-05-02 may present the repeat as "re-affirm current setting". That is presentation only, and it remains an A12. **Closed** by DECISION-K1 K1-2: the grant already in force counts (CH-12 (iii)); the repeat arises only under SP-6F |
| F-24 | RS R11 "action during hold"; HP-4 person-directed turns | An agent action in a person-directed turn is recorded as *action during hold* (HP-4 ruling). The record should show the turn's initiator, so that a governed action the person asked for in their own message is distinguishable from one the agent took unprompted. Neither changes the disposition | DEL-04-03: the R11 action-during-hold entry carries the turn initiator (HOSTING supplies *person-directed*). **Closed (R9-8):** adopted by R6-5; RS §4 R11 carries the turn initiator (*person-directed* · *agent* · *App rule*) |
| F-25 | WD-EX-v0.4 E7 | No "optional host operation absent" case remains for OP-C5; EXEC added L-EXEC-26 | WD-EX may adopt it as a shared case, or keep the OP-C12 case as the single optional-absent example. **Dispositioned (v0.5):** WD-EX-v0.7 keeps the OP-C12 case [L-WDEX-13b] as its single optional-absent example (WD-EX E7); L-EXEC-26 stays this file's local case (MT-4) |
| F-26 | C-v0.4 at `8fb51f07f` | V-GR1 was not yet in C | Closed (R6-4): C-v0.5 §10.4 has V-GR1; CH-12…CH-14 verified against it, and the L-EXEC-13/14 reasons re-pointed to GR-P/GR-R |
| F-27 | R5-1 "enforced by the host loop" row | The value "passes" on hold support, but LOOP-v0.4 §2.4.4 still distinguishes a residual after-observation limit for kinds (b)/(c) in host loops (a turn already streaming when the loop observes the arrival). R5-1 retires "held after observation" as a value | LOOP §2.4.4 records that residual as an evidence limit (R11), not as a separate value; EXEC CR-12 lists it as a limitation. **Dispositioned (v0.5):** LOOP §2.4.4 states the residual limit per checkpoint kind ("stated, not a separate value"), and CR-12 now lists it |
| F-28 (R6) | WD §4.3.1 checkpoint elements; WD-EX E1c | R6-1 classifies checkpoints by **held actions**, but the declaration has no element that names them. EXEC derives them from the prose position and later steps. E1c declares no host operation after `CP-check`, so it is App-side by the conservative HS-5 default. A workflow meant to be enforceable from the App cannot currently *declare* that its held actions are host operations only | DEL-02-01: consider a declared **held actions** statement per checkpoint (or "holds: host operations only"), so that HS-3 vs HS-5 can be read from the declaration rather than inferred. **Closed (R9-8):** WD §4.3.1 has the **held actions** element (R6-1), with the R7-3 derivation when it is absent |

### 11.4 New findings at v0.4 (R8)

| # | Where | Finding | Proposed change |
|---|---|---|---|
| F-29 | SoW REQ-002, REQ-003, AC-002 as they read at v0.4, before SCA-V4-001 ("keeps it waiting until evidence shows that required act actually occurred"); §1 E-B; §4.7 "Why re-hold" | The DEL-02-03 SoW wording assumed the run waits at a checkpoint. Under R8-1 that is governance phase. In Phase 1 the run is not held, and only the record clause ("not recorded as done until performed") applies | v0.4 proposed carrying this wording to the update of the accepted basis, together with V4-WF-05: the SoW acceptance for Phase 1 would read "the act is not recorded as done until evidence shows it occurred" (PH-4), with the waiting clause phased to the governance layer. **Closed (v0.5; R9-1, R9-8):** SCA-V4-001 revised the SoW (the Purpose sentence, the SOW-052 row, OUT-003, REQ-002, AC-002, AC-007, VER-002 and the REQ-002 matrix cell; AX-004) and amended V4-WF-05 and V4-HI-42. §1 E-B, PH-10 and §4.7 now cite the current texts |
| F-30 | WD I-7; V4-HI-42; DECISION-1 D2 "No autonomy grant widens past … a declared checkpoint"; CH-27 | R8-1 phases R2-12 carriage assurance but does not say whether I-7 (an acceptance checkpoint forces a proposal) and D2's checkpoint clause bind in Phase 1 as agent guidance only or also as host obligations | **Closed by R8-11 item 2** (U-E24, closed in place; R8-12 item 7), a reading the owner confirmed (BASIS-ALIGN DECISION-7, OWNER_ITEMS O-25) and R9-2 restates against the amended text. CH-27's Phase-1 entry stands: I-7 is plan guidance, with the host's own treatment governing; V4-HI-42's request clause and record clause are in force |
| F-31 | §2.1 PH-6, PH-8 | R8-1 retains "the hold machine (HD states, re-hold, lapse)" as governance phase and lets arrival and act be recorded. It does not say whether an act's **lapse** is recorded in Phase 1, or whether disposition words may label the record | PH-6 and PH-8 are marked PROPOSED (A1): lapse recording is kept because V4-REC-05 requires acts to lapse visibly; re-hold is governance phase. For the integrator to confirm or amend. **Closed (R9-8):** R8-11 item 1 confirmed both (INTEGRATION), and PH-6 and PH-8 are marked so. R9-1 further makes PH-6's recording required where the arrival is observed |

### 11.5 New findings at v0.6 (Wave B, node B2)

| # | Where | Finding | Proposed change |
|---|---|---|---|
| F-32 | ADAPTER-v0.5 §7.7; EXEC §2.5 AW-10, AE-1 | ADAPTER §7.7 says the App observes *queued* and the host-captured item decisions "through host reads over X", but not who issues those reads. Under RC-4 the recorder issues none; HOSTING §6.8 defines no App-origin call on a host channel in this increment | DEL-03-03 states that the observations it passes come from reads the agent issues in the run, or from App-origin reads it defines with their origin; EXEC records either and issues none (join for V18) |
| F-33 | WD-v0.7 §4.4; EXEC §2.5 AW-7 | Kind (b) on a file output needs the output's path to decide which `fileChange` produced it; WD §4.4 has form and destination but no path element | DEL-02-01 adds a path (or path pattern) designation for file-form outputs, beside the message-output element of R10-8 (node B1 or later) |
| F-34 | R8-12 item 1; EXEC RC-8; RS L-12; LOOP LP-7; PANEL; AS OV-5 | After the resume point, R8-12 item 1 fixes the label ("act lapsed at ‹t›"; nothing says *waiting*) but no file states which of the six disposition values the arrival then carries | EXEC RC-8 keeps *performed* with the annotation and the lapsed referents (PROPOSED (B2)); the other files state the same or object (V18) |
| F-35 | RS-v0.7 §4 R8, R11; EXEC §2.4.5 | The record entries add elements RS R8 does not name: the observed request with its form and arrival association (RC-5); a checkpoint's evaluability on the surface (CE-1); an act not counted with its reason (RS names the label only); the arrival event's source, evidenced-time source and limits ("arrival observed at call start; dispatch order not established"; "outcome not observed in this run"; the AW-6 designation limit); and the recording gap (CE-19) | DEL-04-03 carries them in R8 (and the limits in R11), or states where they belong (join for V18) |
| F-36 | §2.5 AW-4, AE-1; SWBPIPE SQ-01, SQ-12 | Against SWBPIPE's X as it stands, no kind (a) or kind (c) checkpoint can be evaluated (no native-tool mapping or per-operation identity, SQ-12) and no host-content act can be counted (no capture-evidence reference, SQ-01). In the current phase an App run on that X can record only kind (b) arrivals on message or file outputs and acts on App content | Stated here as a consequence of SWBPIPE's current state (data, not commitments); host joins deferred (DECISION-3). No change proposed |

---

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| U-E1 App-side run holds `UNRESOLVED{D6}` (DECISION-2). **Closed for Phase 1** by DECISION-4 D4-1: checkpoints are guidance, with no App or host-loop hold (R8-2). **Re-opens only when the governance phase is taken up.** For host-operation checkpoints, SWBPIPE answered **SQ-02** on 2026-09-28: route (iv), none planned (R5-10). HP-1 and HP-2 not adopted (R4-2) | The owner (DECISION-4; D6 re-opens with the governance phase; SoW TBD-006); then App/shared owners (OI-014) | When the governance phase is taken up for a workflow that needs it; before any App-side positive hold case; before the App fixes its realization family | Phase 1: none (PH-2, PH-3). Governance phase: HS-3 values *not enforceable* against SWBPIPE (SQ-02 answered: none); HS-5 *not enforceable* |
| U-E23 **App-only checkpoints in App runs** (HS-5): *not enforceable* whatever SQ-02 returns (R5-10; F-17). **Re-pointed to D6 (U-E1):** closed for Phase 1, re-opens with the governance phase (R8-2) | The owner, with D6 | Before any **governed** checkpoint with any App-side held action (including an App-content checkpoint) is offered as enforced in App runs | Phase 1: none; such workflows are not *unsupported* for hold reasons (PH-3). Governance phase: such workflows are *unsupported*; runs remain possible (CC-3) with action during hold recorded |
| U-E2 Host placement of the hold machine and required-tool check `UNRESOLVED{OI-013}` / `{OI-014}` | Shared contract owner with SWB implementation owner (SQ-20); App/shared owners. SWBPIPE's successor embedded mechanism is owner decision D-58 (SQ-20, SQ-29) | Before shared/host implementation boundary contracts | Semantics supplied; no placement. SWBPIPE: not decided (SQ-20). App side (v0.6): the checker, recorder and transfer tracer are stated by responsibility in §2.7, where the OI-014 question is prepared; R12-2 keeps it open for the phase review |
| U-E3 *Closed (DECISION-K1 K1-3, 2026-09-30).* Multi-row A4 purpose after partial lapse (WD U-05c; AP U-03; CA DI-7) | The owner (decided) | — | **Settled.** An act on the changed referents alone answers the arrival together with the earlier act for the unchanged referents; each cites its items (§4.7 JA-1). CH-8 released |
| U-E4 *Closed (DECISION-K1 K1-2, 2026-09-30).* Arrival-order rule versus counting a prior act on current content (R4-5 kept it open; cost R5-7, F-23) | The owner (decided) | — | **Settled for the current phase.** An earlier act counts when it is of the required kind and its content is still current; the record cites it and its time (§4.5 SP-6). Capture at or after the arrival is kept as the governance-phase option SP-6F (PROPOSED), which a workflow may take up (SoW TBD-006). CH-9 (ii), CH-12 (iii) and CH-20 recomputed |
| U-E7 "On subject absent" path in the declaration | DEL-02-01 | Next comparison | Waiting "subject absent" |
| U-E8 *Closed (DECISION-K1 K1-4, 2026-09-30).* App person identity scheme; App act control construction (DEP-02-03-027, arc X-1: narrow) | The owner (decided); control construction DEL-01-04 (later, D1) | — | **Identity settled** (CAP-8): the name set in the App, the operating-system account and the Codex account when Codex reports one, marked *identity not verified*; a verified identity is a governance-phase matter. **Control:** construction stays with DEL-01-04; its obligation is proposed for DEL-01-04's contract at the next amendment (DECISION-K1 K1-4); collected at this run's closeout. CH-23 (ii) stays AWAITING INPUT on the control |
| U-E9 Person-attributed acts on host content through the App (proxy control) | Host owner (DEP-001), **SQ-25** (answered) | Before any App proxy is offered | None offered. SWBPIPE: host facility only, no proxy (SQ-25) |
| U-E10 Harness capability names (WD U-08) | DEL-02-01 with DEL-01-01 | Before App-side required-tool check | *not established*; not holdable (R4-21) |
| U-E11 Version compatibility statements (C U-C9; WD U-07) | Host owner with DEL-02-01, **SQ-18 (d)** (answered: no; no operation versions) | Before version fixtures against a real host | Equality only |
| U-E12 Host capture-evidence reference (WD U-05b; AP U-04, §12 item 4 (a)) | SWBPIPE owner decision (PB-TBD-002 acceptance-record storage; DEL-16-03 actor identity; ANS §2). SQ-01 answered: none | Before host act-recording integration | No host-content act can be recorded as performed (PH-4) |
| U-E13 Constraint receipt on the host route (WD U-19; P U-P10) — governance phase | Host owner with DEL-03-02; **SQ-02** answered 2026-09-28: route (iv), none; a constraint field would be refused as unknown (SQ-02 (a)). Planning a route is a SWBPIPE owner decision | Before CH-27's governance-phase host case | Phase 1: no constraint carried by the App; the agent never adds fields the host schema lacks (R8-10). Governance phase: **AWAITING INPUT** — SQ-02 answered: no receipt, no host copy (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3) |
| U-E14 Host library receipt of other origins, adaptation evidence with derived-from, holding library and run records (TR-6…TR-8) | SWBPIPE owner decision (a work item to receive App workflows; ANS §4). **SQ-17, SQ-18, SQ-19** answered: none | Before RT host-side cases | RT host links AWAITING INPUT (STD-2 annotations) |
| U-E15 Per-turn supplied guidance in host loops (WD U-29; LOOP Q-4) | Host owner, **SQ-19 (a)** (answered: no host loop; the D-58 successor is a SWBPIPE owner decision) | Before host supplied-link evidence | *supplied* **unknown** |
| U-E16 Physical carriage of the declared part (WD U-01) and carriage-manifest representation; revision algorithm (WD U-03) | DEL-02-01 with DEL-04-03; TBD-003 | Before OUT-002 schema and transfer code | All semantic; verification uses method designations |
| U-E17 First connected operation `UNRESOLVED{OI-021}` | Owner via outside SWB session with App/shared owner, **SQ-04, SQ-05** | Before connected-activity SoW | FX-PIPE-01 only; MT-13, CH-11 production HELD |
| U-E18 Extension promise `UNRESOLVED{OI-003}` (App v4 OI-003, the extension promise; unrelated to SWBPIPE's OI-003) and real exposure (C U-C7; WD U-23) | Owner with host contract owner; exposure **SQ-11** (answered: no exposure element; only `position.x` on X) | Before exposure claims | FXA-1 fixture assumption; unagreed exposure → HS-4 *not established* (governance phase), except where SQ-02 is answered with no host-held route, as for SWBPIPE (R8-2) |
| U-E19 Selection slot policy and host precedence (WD U-10); registration as an act (AP U-08) | DEL-02-02 (later) with DEL-02-01, DEL-04-01 | Before host-origin discovery in the App | RT-6/RT-7 registration side not exercised |
| U-E24 *Closed in place (R8-11 item 2; R8-12 item 7).* Phase-1 standing of WD I-7 (an acceptance checkpoint forces a proposal), V4-HI-42 and DECISION-1 D2's "or a declared checkpoint" clause (F-30) | Integrator (INTEGRATION, R8-11 item 2); the reading was confirmed by the owner (`APP-V4-BASIS-ALIGN-20260928` DECISION-7, OWNER_ITEMS O-25) and is restated against the amended text by R9-2 (DERIVED) | — | **Settled.** D2's "no autonomy grant widens past a reserved act" binds, and the host enforces it through its operations. For a declared checkpoint, V4-HI-42's request clause and record clause are in force whatever the autonomy setting; whether the run goes on before the act is for the person and the agents in the current phase, and the host's own treatment of its operations decides what the host does. The forced treatment of WD I-7 binds only for governed checkpoints in the governance phase. CH-27's Phase-1 entry stands; the reserved acts themselves stand (PH-5) |
| U-E25 Per-subject content identity (V4-HI-32) not met by SWBPIPE, which supplies only a whole-model identity (SQ-03; R8-4) | SWBPIPE (PB-TBD-002 / DEL-16-03); owner notice | Before host act-binding integration | SP-4 receives the whole-model identity for every covered subject: over-lapse, never under-lapse; resulting objects beyond target ids *not supplied* |
| U-E26 **OBS-1 pending cells** of §2.5 (AW-1, AW-2, AW-6…AW-9; AE-3, AE-5): the order and content of native items around a model-issued tool call at pin 0.158.0 are not observed (HOSTING §8.1 L-3) | HELP_HUMAN runs OBS-1 after round 2 of Wave B (DECISION-K1 K1-6), with DEL-01-01 (HOSTING's OBS-1 brief, node B6) | Before an App recorder implementation or an App-run CH case relies on those cells | The cells are PROPOSED (B2) with their stated limits; §2.5.3 lists O-1…O-9. **SPIKE** |
| U-E27 **Message-output designation** (R10-8): which of the forms m1–m3 (§2.5 AW-6) the declaration admits | DEL-02-01 (node B1) | Before AW-6 is relied on | AW-6 records the arrival with its designation limit; a model statement never counts |

Changed at v0.6 (Wave B, node B2): U-E26 and U-E27 opened; U-E2's App-side half now has the component responsibilities of §2.7. Changed at v0.5, node A3 (DECISION-K1): U-E3, U-E4 and U-E8 closed. Changed at v0.5 (Wave A): U-E24's settled effect is restated by R9-2; no item is opened or closed. Changed at v0.4 (R8): U-E1 closed for Phase 1 (re-opens with the governance phase); U-E23 re-pointed to it; U-E24 opened (A1) and closed in place by R8-11 item 2 (R8-12 item 7). Closed at v0.2: U-E5 (R4-9), U-E6 (R4-6). Withdrawn at v0.2: U-E20 (nothing relies on `turn/interrupt`, R4-2). Closed at v0.3: U-E21 (C-v0.4 AF-1, LIB-A1, LIB-A2; R5-9), U-E22 (per-turn destination, R5-4). HOSTING U-25 is closed by the HP-4 scope ruling (§2).

## Verification cases

Designed. No product code, host or act exists. A local design prototype
(`prototype/`, R12-3) ran the cases §7.4 marks **Ran**, on test doubles only.
Labels use C's evidence mapping; all current states are DESIGNED, AWAITING
INPUT or HELD.

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-E-01 Report completeness and outcomes | MT-1…MT-17 against §3.3, §3.4, §3.5 and `compatibility-report.schema.json` (prototype ran, §7.4) | Every CR element present, incl. CR-14 at report time as information only; each outcome distinct; three-valued check result with precedence; PS-2 wording; registered ≠ compatible (MT-3) | VER-001 (AC-001) |
| VC-E-02 Checkpoint under direct autonomy | CH-1, CH-2, CH-27 | Phase 1: the arrival is recorded, nothing is held, and no success, receipt, grant or host check is recorded as the act; CH-27 carries no constraint. Governance phase: waiting persists and nothing releases it; CH-27 per HS-3 (c) (SQ-02 answered) | VER-002 (AC-002) |
| VC-E-03 Interruption and replay | CH-3, CH-4, CH-5, CH-21 | Same arrival identities; recovered events not back-filled; unknown never performed; held call dispatched unchanged; replay issues nothing | VER-002 (AC-002) |
| VC-E-04 Lapse, re-hold and finality | CH-6…CH-10, CH-24, CH-30 | R2-19 before resume; re-hold after resume (R4-3; governance phase; Phase 1: lapse recorded, no re-hold, PH-8) for any cause, including the person's undo, which is never *action during hold* (R5-5); undo never re-holds A5; ended runs final and continuation inherits nothing (R4-4); a partial lapse is answered by an act on the changed referents together with the earlier act (JA-1; CH-8); subject-absent path | VER-002, VER-003 |
| VC-E-05 Act evidence and fabrication negatives | CH-20, CH-23, CH-25, CH-26, CH-28; WD VC-21/VC-22 | Only SP-satisfying acts count; conversation, elicitation answers (R4-12), A14, agent records and earlier acts whose content is no longer current or whose kind differs do not; an earlier act of the required kind on current content counts, cited with its time (SP-6; DECISION-K1 K1-2; under SP-6F it does not); decision actor ≠ recorder, the App actor recorded per CAP-8 (*identity not verified*); AF-1 file binding with method designation | VER-003 (AC-003) |
| VC-E-06 A5 item rules | CH-15…CH-19 | MX-1…MX-8 and MC-1…MC-4 as tabulated (R4-7); never "all accepted" over a reduced subject | VER-003 |
| VC-E-07 A12 rules | CH-11…CH-14, CH-29 | V-GR1: A12 after arrival performs; T15 before arrival counts while ⟨set-2⟩ is in force (SP-6; not counted only under SP-6F, R5-7); refused → waiting; pending → waiting; refused never supersedes (R4-6); declared content always binds, and naming none is invalid even with an A8 (R5-3); supersession not lapse | VER-003 |
| VC-E-08 App→host trace | RT-1…RT-5, RT-9, RT-10 | Original and revised identities kept apart; links separate; derived-from correct; holding library per HL-1…HL-3 with LIB-A1; unsupported receiving explicit; destination per turn, run-level set, no gate (R5-4); host links AWAITING INPUT with SQ IDs | VER-004 (AC-004) |
| VC-E-09 Host→App refinement | RT-6…RT-8 | Host identity kept on opening (LIB-A2); draft not selectable; registered identity in LIB-A1 derived from the host tuple; no rebinding or overwrite; history referenced, no act imported | VER-005 (AC-005) |
| VC-E-10 Ownership and open items | §2, §8, §10, UNRESOLVED against SoW CLM-001…003, REQ-006/007, TBD-001…TBD-006, DEP-001, DECISION-2, DECISION-3, DECISION-4, R5, R8, R9 | Every excluded act has an owner; every held item resolved or carried with owner, point of need and SQ ID where host-dependent; no external commitment or joined qualification claimed | VER-006 (AC-006) |
| VC-E-11 Evidence account | RT-11 inventory for this file (EXEC-v0.6) and its source versions; W14 map | Candidate and source identities listed; states truthful; DEL-09-06 named as joined-witness owner; no witness claimed | VER-007 (AC-007) |
| VC-E-12 Hold support (R5-1) — governance phase | MT-1, MT-2, MT-15, MT-16, MT-17, CH-33, CH-1, CH-22, CH-23, CH-26, CH-27, CH-29 (governance-phase columns) against §2.2, §2.3, §3.5, §3.6 | Only the four R5-1 values appear, and only for checkpoints read as governed; each **valid** checkpoint gets exactly one value by held actions per HS-2…HS-5 (invalid: HS-1, no value); E1c/E1d `CP-check` *not enforceable* in App runs; MT-16 *unsupported*; *enforced on the host route* is never assumed; retired values appear nowhere; HP-1/HP-2 never enforce; HP-3/HP-4 are best effort; a person-directed turn is not blocked and its governed agent actions are *action during hold*; model-supplied carriage → *not enforceable* after SQ-02, *not established* before; SWBPIPE's SQ-02 answer gives HS-3 (c) and HS-4 does not mask it (R8-2) | VER-002, VER-006 |
| VC-E-13 Phase-1 semantics (R8-1) | MT-1…MT-17 and CH-1…CH-33 (Phase-1 columns) against §2.1 PH-1…PH-10 | No hold-support value and no *unsupported* for a hold reason appear; results depend on required tools and channel state (with role and delegation); no App or host-loop hold, block or re-hold; acts recorded only when the person performs them, never by an agent on the person's behalf; reserved acts remain the person's, with host refusals recorded as observed; arrivals and acts are recorded where observed (R9-1) and appear as observation; "continued past ‹checkpoint› before ‹act›" is optional and never a defect; a `governed` flag changes nothing in Phase 1 | VER-001, VER-002, VER-003, VER-006 |
| VC-E-14 Current-phase recorder (v0.6) | CH-7, CH-8, CH-10, CH-20, CH-31 against §2.4 (RC-1…RC-10, CE-1…CE-19, the transition table) and `checkpoint-record-entries.schema.json` | Transitions and labels as tabulated; earlier acts counted or not counted with their reasons; joint answers cite their referents; after the resume point nothing says *waiting*; every entries document validates; no entry expresses a hold, and the recorder emits no request, refusal, pause or prompt (RC-4). Prototype ran (§7.4) | VER-002, VER-003 (AC-002, AC-003) |
| VC-E-15 App-run reached-when (v0.6) | §2.5 AW-1…AW-12 and AE-1…AE-7 against OBS-1's record | Each OBS-1 pending cell is restated from the record: the arrival event occurs in the order assumed, or the stated limit stays; nothing is inferred from message text. **OBS-1 pending** | VER-002 (AC-002) |
| VC-E-16 A6 and A7 kept apart (v0.6) | CH-32, CH-31 (ii) | Each act answers only its own kind; an earlier act of another kind is "prior act not counted"; the A7 actor carries its evidence limit and *identity not verified*; no certification standing | VER-003 (AC-003) |

Limit: passing these later would show local contract and fixture conformance
only. It would establish no host implementation, round-trip execution,
provider adoption or human act (SoW VER-007; AX-002).
