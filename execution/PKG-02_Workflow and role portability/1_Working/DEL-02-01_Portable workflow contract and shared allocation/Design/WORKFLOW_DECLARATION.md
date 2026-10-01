# Portable workflow declaration, roles, source identity and shared allocation
- Contribution: DEL-02-01/WD-v0.8 (supersedes DEL-02-01/WD-v0.7, last changed at `c896a99d90`, file sha256 `a02f5d59b475763a0ee49ed649a9f00fae361057a5bfa42d6e0d00b21a6b070a`; WD-v0.6, last changed at `f5ceef164`, file sha256 `43a9962f025de384e1cdaedea9a648da74e20216476a04f2394cfa3851f47eb9`; WD-v0.5, last changed at `c6f81a4f2` and unchanged at `bcc25624d`, file sha256 `e55d69cbd25922efa5c25f3349c60dbdaaa7cb3e30ef14c9482fddeb18d76c66`; WD-v0.4 committed at `8fb51f07f`, file sha256 `e492ff635de972466c8a932355beeae848e1f3d3f60de7304e88963352d8e88e`; WD-v0.3 sha256 `84841d9f539767b9ff7ae225fec27f0dc4ebbd2c161c41aff179bbae97f345eb`; WD-v0.2 sha256 `c25bccc5f3ac02c84522148eeaa8a6ef0f5eb4a380686773cff45f57a448a55c`; WD-v0.1 sha256 `bacfcb71ca9585b950444c0218fdd5283f5b2f5d0c8f981411395278b286fc5e`)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Phase (R9-1; PRD V4-WF-05 and HOST_INTEGRATION V4-HI-42 as amended by SCA-V4-001; §4.3.0): when a run reaches a declared checkpoint, the required human act is requested, and it is recorded as done only when the person performs it, whatever the autonomy setting. Holding the run at the checkpoint until the act is performed is phased to the governance layer: in the current phase (Phase 1) a checkpoint is plan guidance that the person and the agents manage, and neither the App nor a host's embedded loop enforces a hold, blocks a run, or reports a workflow unsupported because a hold cannot be enforced. The reserved acts (V4-HI-30) still bind. The checkpoint fields are all kept, and the optional **`governed`** flag (PROPOSED, R8-1) marks the checkpoints a later **governance phase** will enforce. Hold support (§4.3.8) is the governance-phase definition, retained.
- Serves: OUT-001, OUT-002 (at v0.8 with a PROPOSED carriage, §3.5, and schema, `workflow-declaration.schema.json`, §3.6), OUT-003 (map version), OUT-004 (fixture design; at v0.8 also conformance instances and a design prototype, `prototype/`, which is not product code); REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006; AC-001…AC-007 by designed verification; VER-001…VER-007 (cases designed, none run)
- Basis: the accepted basis as amended by SCA-V4-001 (`_ScopeChange/SCA-V4-001_2026-09-28_2155/`) and SCA-V4-002 (`_ScopeChange/SCA-V4-002_2026-09-29_1901/`), at its current bytes (R9-5): P/docs/PRD.md sha256 bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd; P/docs/ARCHITECTURE.md sha256 317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c; P/docs/HOST_INTEGRATION.md sha256 d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f; P/docs/EXAMINATION.md sha256 471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0 (the v0.1–v0.6 passes read these four at repo 6e18505e3, before the amendments). ScopeOfWork.md sha256 ef360edf28f5f463ae961495e04e566ab9ec9d56c0a4fd4f35e67b87adb82f17 (revised by SCA-V4-001: CLM-002, CLM-003, REQ-002, REQ-003, REQ-006, VER-003 and TBD-003, with TBD-004 and AX-005 added; and by SCA-V4-002: CLM-002, with AX-006 added; the v0.1–v0.6 passes read sha256 080d7f5a8e55d93c06f51e5332b53954deb03e0877b1ee49be3011e3de14a294). Sections and requirements relied on: P/docs/PRD.md §2.2 (V4-HOST-05/06), §2.4 (V4-SHR-01…03), §4.1 (V4-WF-01…06), §4.2 (V4-ROLE-01…03), §4.3 (V4-EXE-01/03), §4.5 (V4-AUT-01…05), §4.7 (V4-REC-01…05); P/docs/ARCHITECTURE.md §1 (M-1, M-3, M-5), §4, §5 (V4-ARC-20/21); P/docs/HOST_INTEGRATION.md §1, §2 (V4-HI-02…04), §3 (V4-HI-11/12), §4 (V4-HI-20…25), §5 (V4-HI-30…33), §6 (V4-HI-40…42), §9 (V4-HI-70/71); P/docs/EXAMINATION.md V4-EXM-10, -14, -21, -22; DECISION_BRIEF.html #d2, #d3, #d5; SCC-CASE-002 Case_Datasheet M1 rows; Open_Issues.csv OI-003, OI-013, OI-014, OI-018, OI-021; owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (OWNER_DECISIONS.md sha256 `f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e`), rulings D1 (scope), D2 (OI-001), D3 (OI-002); owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (OWNER_DECISIONS.md at `f05c7e4cd`, sha256 `a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c`), D5 (external-channel model destination: user flexibility) and D6 (App-side run holds deferred to SWBPIPE SQ-02); owner decisions `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3` and `-DECISION-4` with its clarification (OWNER_DECISIONS.md current sha256 `5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2`, which also holds DECISION-5 and its confirmation; read for v0.6 at `bcc25624d`, sha256 `a5ccab0d39bd1cab37c5556abc9bdedd5341ce76be4712706c8c9d72d623e776`): host joins deferred; D4-1 phased checkpoints; the owner's confirmation of the R8-11 item 2 reading of D2's "or a declared checkpoint" (`APP-V4-BASIS-ALIGN-20260928` DECISION-7, accepting OWNER_ITEMS O-25 "as recommended"; OWNER_DECISIONS.md sha256 `ca8c4e50df1d7dddb41b875a4afe46eea4f1a1bf2491d255b7890d0d71cd254b`). Root reuse sources read (not adopted): `workflows/WORKFLOW_TEMPLATE.md`, `workflows/*/execution.json` (66 companions surveyed), `workflows/catalog.yaml`, `workflows/catalog.schema.json`, `workflows/index.json`, `workflows/create-workflow/WORKFLOW.md`, `docs/SPEC.md` §9.1–9.8, `docs/AGENT_WORKFLOW_RUNTIME.md`.
- Consumed inputs:
  - **v0.8 inputs (Wave B design development; run `APP-V4-DESIGN-PASS-2-20260930`, node B1).** Each sha256 recomputed with `shasum -a 256` in the working tree at this pass; paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/`: `R12_RESOLUTIONS.md` sha256 95f3011b436b6faa3de098059e77eac836c165e0bb98a5ed94e28918a3a749a1 (R12-1…R12-3, R12-5, R12-10; binding); `BRIEFS.md` sha256 ccb4d9f036fb7ff531fffa0d309533b15cf1ebb39b0320651ed4bd5d88efc550 ("Common rules", "Wave B", row B1); `OWNER_DECISIONS.md` sha256 1dfd5bf4619b329719136b1646030e3f871fd7ffc52dbfd12265414e515aaf15 (DECISION-K1 and the later records); `SURVEY/S1-C.md` sha256 5b60dd41a8c269902a9b360bf4cdc7c8106c464564bcc2fc1623948661c7eaa0 (§A.4–§A.8, §B.8; advice, each item checked against the current text first). R9–R11 as pinned in the next bullet. Siblings by version label and section (R9-5), read in the working tree while the other Wave B nodes edit them, so no sibling byte is pinned: HOSTING-BOUNDARY-v0.7 §8 (receivers table and closing paragraph) and PIN-SPIKE-v0.1 §4 (inventory; experimental-only fields); LOOP-v0.7 §2.4, §2.4.1 (the R10-8 note); EXEC-v0.5 §3.2–§3.4 (EV-3), §4.5 (SP-6, SP-6F), §4.7 ("Subject absent"), §4.12 RP-5, §4.14, §6.3 TR-4, §6.7 TF-4, TF-8; ACT-POLICY-v0.7 §2.1 (A6, A7), §2.6, §4.2, §13 L-ACT-6; C-v0.7 §3, §10.1–§10.4, §10.7; P-v0.7 §9. The generated supplier schema, which is an artifact and not a Design file, is pinned: `DEL-01-01…/Design/generated/0.158.0/json-schema/experimental/codex_app_server_protocol.v2.schemas.json` sha256 34f28a486d00fbd20e5da0b0da3422d1d6e20ec897d12b31408f87499198f458 (`ThreadItem` with 19 item kinds; `CollabAgentTool`; `MessagePhase`); the session's regenerated stable output under the scratch folder `codex-0.158.0/gen/` (`inventory.txt`; `schema-stable/run1`) was read, read-only, and lists the same 19 item kinds, so each kind used in §4.2.5 is in the stable output. Root `workflows/create-workflow/WORKFLOW.md` and `workflows/project-dag/` read at HEAD `86cafc0e1c`; unchanged since `6e18505e3` (`git diff --stat` empty). The prototype's command, date and output are recorded in `WAVE_B/B1.md`.
  - **RP-3 repair inputs (repair node RP-3 of run `APP-V4-DESIGN-PASS-2-20260930`; in place, no version bump).** Each sha256 recomputed with `shasum -a 256` in the working tree; paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/`: `R14_RESOLUTIONS.md` sha256 c6a603303693f50e24ea27fcbc9f381a297434e4182f023fbcee941073623576 (R14-5, R14-6, R14-8 N-18; binding); `R13_RESOLUTIONS.md` sha256 d0385313660e5820258b4089372313f382afcebc57d37265389274ca470a8d3a (R13-6); `BRIEFS.md` sha256 e3f98d1c8449292965dd244a0f2821b221bcd0f3b0294e592f73b8eaaaaf6321 ("RP — repairs from V18", row RP-3); `comparisons/V18-2.md` sha256 0b00e79b161bcdf1e83a3a207d71114e316421e3cdf2ed5231901c14b85fbdb7 (M-1, M-2, m-2, m-5, m-7, m-9…m-13); `comparisons/V18-4.md` sha256 078113d7055ba75849ed3b78166103067397e51143c650515239d73d3cdcc6ed (J10, m-8). Siblings by label and section, read in the working tree while the other repair nodes edit them: HOSTING-BOUNDARY-v0.8 §6.1, §8.4 and its RP-3 §10.1 (same repair node); P-v0.8 §3.1, §3.4, §3.5 PM-6, §4.1, §4.3, §4.6, §9, §13 and `proposal_state.schema.json`; EXEC-v0.6 schemas (spellings, §3.6 table). The return file is `WAVE_B/RP-3.md`.
  - **Current pins of this run's records (node A4 of run `APP-V4-DESIGN-PASS-2-20260930`; in place, no version bump; R11-3).** Each sha256 recomputed with `shasum -a 256` in the working tree at this pass; paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/`: `R9_RESOLUTIONS.md` sha256 a64e241519b7d158165a7ede0ffdd22eec0af15b6812b5300755f5f38abd59b8 (R9-1…R9-11; R9-2's second bullet as corrected by R10-1); `R10_RESOLUTIONS.md` sha256 ad3b6caa4a12660db77abc51b5c02ba70519ee46d55b40d21ee76eb3ca561796 (R10-1…R10-11); `R11_RESOLUTIONS.md` sha256 e7343b6663b6aeeb2dc506d3391f5b310088e7688d1b21e65d2ba1d8616b3615 (R11-1…R11-9, the repairs from review V17); `OWNER_DECISIONS.md` sha256 7458e9e81971676337a34280b4e8b29a7d04fce5fc202da5b9f5cf7ccd8f9ae5 (DECISION-K1). These supersede for currency the earlier pins of the same records in this header and in the change-table rows, which record the bytes read at node A1 or A3.
  - **v0.7 inputs (Wave A alignment; run `APP-V4-DESIGN-PASS-2-20260930`, node A1-C).** R9_RESOLUTIONS.md sha256 `c3efe2ffa232dd9293202d4fc891eba4325afeb2e224fecdf8c1b4c5122a9d2c` (R9-1…R9-11; binding). BRIEFS.md sha256 `698d91d8217cee528812529fa353faac899b4bc1a5be5686552ad88dad6c469a` ("Common rules", "A1 — alignment wave"). SURVEY/S1-C.md sha256 `5b60dd41a8c269902a9b360bf4cdc7c8106c464564bcc2fc1623948661c7eaa0` (advice; each item was checked against its current source before editing). Rulings in force: R1–R7 by file in `APP-V4-FIRST-INCREMENT-20260928/` (hashes in the bullets below; R7_RESOLUTIONS.md sha256 `1f6ab3b2355e164f803657ceae08841af92d21a821feede3800a6df861b2a1ea`) and R8_RESOLUTIONS.md at its current sha256 `44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b` (R8-1…R8-13; R8-13 changes nothing in this file). `_DAG/_LATEST.md` → DAG-003 (accepted 2026-09-29; `DAG-003/HANDOFF_STATE.md` read first; held candidate arcs are non-gating; satisfaction is read from the local `Dependencies.csv` and `_DEPENDENCIES.md`). SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` at its current sha256 `afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74`: SWBPIPE revised three lines at `a999f4ba1` after the R8 pass read `6f01add3…61c7` (the integrity-standing list under SQ-04, the evaluated-basis sentence of the outcome vocabulary, and the T9 source under SQ-27); none changes a statement this file makes. They remain data about SWBPIPE's current state, not commitments (DECISION-3). Sibling Design files are cited by version label and section only (R9-5); their byte pins are in GUIDE's input table alone. Wave A labels (R9-11): DEL-02-03/EXEC-v0.5; DEL-03-01/C-v0.7; DEL-03-02/P-v0.7; DEL-03-03/ADAPTER-v0.5; DEL-03-04/GUIDE-v0.4; DEL-04-01/ACT-POLICY-v0.7; DEL-04-02/AS-v0.7; DEL-04-03/RS-v0.7; DEL-05-01/LOOP-v0.7; DEL-05-02/PANEL-v0.7; DEL-01-01/HOSTING-BOUNDARY-v0.7; DEL-01-01/PIN-SPIKE-v0.1; DEL-09-06/CA-v0.5; DEL-09-09/XT-v0.5; DEL-09-06/RELAY-v0.3. **Read directly at this pass** for the §8 supplier states (working tree, while the other Wave A edits were in progress; no sibling byte is pinned here): RS §4 (R2, R5a, R8, R9, R11, R14), §6.1, §7 L-12, §10; PANEL §3.2, §3.5, §6; LOOP §2.4, §2.4.0, §2.4.1, §2.4.2, §6.2, §10.1, §10.2; P §3.1, §3.3, §4.3, §9, §13; HOSTING §8 (closing paragraph), §8.2; ADAPTER §5.1, §5.3, §7.7 (for the DEL-03-03 receiver row). The bullets below are kept as the records of their passes.
  - **R8-12 closing pass (node A6; in place, no version bump).** R8_RESOLUTIONS.md sha256 d4c3423310a857af86692d17ddfdd22fa877ee20b07c46e1ee481d1cd750e7af (R8-12, items 1 and 7 applied here). Current sibling versions after R8, as committed at `7a1508452` with A6's in-place R8-12 edits (their byte pins are in GUIDE-v0.3's input table): DEL-02-03/EXEC-v0.4; DEL-03-01/C-v0.6; DEL-03-02/P-v0.6; DEL-03-03/ADAPTER-v0.4; DEL-03-04/GUIDE-v0.3; DEL-04-01/ACT-POLICY-v0.6; DEL-04-02/AS-v0.6; DEL-04-03/RS-v0.6; DEL-05-01/LOOP-v0.6; DEL-05-02/PANEL-v0.6; DEL-01-01/HOSTING-BOUNDARY-v0.6; DEL-01-01/PIN-SPIKE-v0.1; DEL-09-06/CA-v0.4; DEL-09-09/XT-v0.4; DEL-09-06/RELAY-v0.3. SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` and `FACTS_SQ01_SQ32.md` are unchanged (data about SWBPIPE's current state, not commitments; DECISION-3).
  - **v0.6 inputs (R8 pass, node A1, at `bcc25624d`).** R8_RESOLUTIONS.md sha256 `9877da0759409776ff3ac5d77cd20efb2edd9f513bdba8ce39564f650e561234` (R8-1…R8-5, R8-7, R8-10; binding). INTAKE_MAP.md (I2) sha256 `3cc182955c0f3dd70efa0f1c051870229c2ccc08f36c5cf1445f2eef0dd1ea33`: rows 01.1, 02.4, 03.4, 09.3, 11.4, 12.3, 17.2, 19.1, 31.4; Part 2 P2.1, P2.4, P2.5, P2.6, P2.13, P2.16, P2.17 and its §2.2 WD rows; Part 3 items 2, 3, 10, 12; Part 4.11. R8 overrides I2 where they differ. BRIEFS.md sha256 `3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517` ("A-wave"). SWBPIPE's delivered answers `RELAY_ANSWERS_SWBPIPE.md` (DEL-09-06, #1047) sha256 `6f01add3977761e42ac6b310faf72ba4fd5455e478605deb83fefb2e4d3a61c7`: data about SWBPIPE's current state, not commitments (DECISION-3). **Owner file read first:** DEL-02-03 EXEC-v0.4 `EXECUTION_COMPATIBILITY.md` in the working tree after the A1 edit, sha256 `d32be37797a3c367d342a2d13bbb8dd4279bc52934531d83b8c6ec8c6e7b76d4` (§2.1 PH-1…PH-10; §2.2 GV-1…GV-5; §2.3; §3.5; §3.6 with R8-2; §4.5 SP-4; §4.11 receiving notes).
  - **R6 micro-rulings (binding, applied in place, no version bump).** R6_RESOLUTIONS.md sha256 `8703e85aa7324e233fab285321e277d720923d3e36e342c865917b55083cb841` (R6-1, R6-2, R6-3, R6-4); review V4-A sha256 `121deafc40c4baf0dec71f96eb449083b0d93456c2bd448f89a279951ca2eab1` (MAJOR-1/2; m-1, m-3, m-4, m-9); DEL-02-03 EXEC-v0.3 §3.5–§3.6 read in the working tree, sha256 `b147d9862fe9e0228139c72ba13c50392dcf66930109c4357587bf97bbdebf42` (HS-1…HS-5, evaluation order HS-1, HS-2, HS-5, HS-4, HS-3; F-28). Sibling versions at `d3cebd1cc`: C-v0.5 `a6306bd4…7a29` (V-GR1, GR-1…GR-3, GR-P, GR-R, GR-S, run 13), ACT-POLICY-v0.5 `86975a90…80e7`, LOOP-v0.5 `43e039aa…01ca4`, P-v0.5 `a5ee4946…d1b7` (headers checked). (C `a6306bd4…7a29` is the pre-R6-2 byte state; the R6 state of C is `298e4258…2364`, below — R7-4 m-8.)
  - **R7 repair (in place, no version bump).** R7_RESOLUTIONS.md (R7-3; R7-4 m-5, m-8) and `reviews/V5.md` (MAJOR-3; m-5, m-8). Sibling inputs read at the R7 working state: first at candidate `2f42fba02` — EXEC-v0.3 `EXECUTION_COMPATIBILITY.md` `b147d986…bf42` (§3.5, §3.6 HS-1…HS-5 and the held-actions definition); WD-EX-v0.5 `EXAMPLES.md` `b1b7f10e…3362` (E8); C-v0.5 `CATALOG_AND_READ_BASIS.md` `298e4258…2364` (V-GR1); ACT-POLICY-v0.5 `d539b384…9293`; LOOP-v0.5 `0ec980b5…d737`; P-v0.5 `6ab94fd1…37e0` (headers checked) — then with the R7 edits made in place to EXEC, WD-EX, C and ACT in the same repair, each recorded in that file's R7 rows. The post-R7 bytes of every Design file are pinned in GUIDE's input table (R7-4 m-1).
  - **Final alignment rulings (binding).** R5_RESOLUTIONS.md at `8fb51f07f`, sha256 `254d0b93b9959419a70c6737b07087e1db59b529adc3105a1db31f82b78dd6f1`: R5-1, R5-2, R5-3, R5-7, R5-9 (others read for context). Reviews V3-A sha256 `f25f5af1177b7fe2a698bd4ef1e1caafa4c2ef25cfc73111f031e17c7cc21d87` (MAJOR-1, m-2, m-3, m-6, m-10, m-12 as they concern WD/WD-EX) and V3-B sha256 `5662fbd09025f5ad9459861370159d606fcced76b394980199e861555a1954a3` (WD-EX framing note).
  - **Current sibling texts read at `8fb51f07f`** (via `git show`): DEL-02-03 EXEC-v0.2 `EXECUTION_COMPATIBILITY.md` sha256 `7f7848c0de2fdb4dc21f5adafa97f92e179bb66c9f6b04f3434d8f2342317af0`; DEL-03-01 C-v0.4 `CATALOG_AND_READ_BASIS.md` sha256 `e929d39d3ff9515702f9bfe51dfada537e1cbd165146ec0de4ccf629c659a08c` (§10.1 FXA-1…FXA-5, LIB-A1, LIB-A2, AF-1; §10.4); DEL-04-01 ACT-POLICY-v0.4 sha256 `d6da05abe790a4374df7faf225439a01dc1be734491b499d90cf00533369b03b`; DEL-05-01 LOOP-v0.4 sha256 `ffc3048333f3370ba09a9ce124159b94f2c80ce69b5f593bfb82cc552f95934e`; DEL-03-02 P-v0.4 sha256 `0d3960a2e6bd3520368006cdd2b1b67a1fe4eb06e23184aded9d5b98d6c5e361`; DEL-09-06 CA-v0.2 sha256 `31ea3bff05865f425127009f90c070f26b97972e203b5a235791d00332d8dee1`. Elements R5 assigns to siblings' v0.5/v0.3 (e.g., C V-GR1) are cited "per R5-n; sibling to confirm".
  - **Sweep A1 rulings.** R4_RESOLUTIONS.md at `f05c7e4cd`, sha256 `50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24`: R4-2, R4-3, R4-4, R4-5, R4-6, R4-7, R4-8, R4-9, R4-12, R4-14, R4-16, R4-18, R4-19, R4-20, R4-21 (others read for context). V2 review `reviews/V2.md` sha256 `75ba1dff8a0c4fa2eb294471127147cbd19a0925daf9169b32ddc88727dde6ef` (MAJOR-1; m-3, m-8, m-9, m-12, m-13 addressed to WD/WD-EX).
  - **Sibling texts read at commit `f05c7e4cd`** (via `git show`, not the working tree): DEL-02-03 `EXECUTION_COMPATIBILITY.md` EXEC-v0.1 sha256 `e0ede76ebf08003511755afc666be2466a867fd3256837ee94300cd0dfe518e8` (§2 hold points, §3.5–§3.6, §4, §5, §6, §11 F-1…F-16); DEL-09-06 `CONNECTED_ACTIVITY_CONTRACT.md` CA-v0.1 sha256 `685349b25981ca8333929207890514120d63753cdedd67ae0bad986fc5d45e62` (§3.2 L-CA-1; F-5, F-7); DEL-03-01 `CATALOG_AND_READ_BASIS.md` C-v0.3 sha256 `ba45e7393ee0b16780f36605ddeecb95ba1f181488e36a46b4b495b69fd67c26` (§3, §4.1, §10); DEL-04-01 `ACT_AND_POLICY_CONTRACT.md` v0.3 sha256 `b3748c02006f939d8cc78c6e0b0c847598a8b32d55515ae8658ad80597c98128` (§2.1, §4.2). Elements R4 assigns to siblings' next versions are cited "per R4-n; sibling v0.4/v0.2 to confirm".
  - **Earlier integration rulings.** R2_RESOLUTIONS.md sha256 `77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088` (R2-1, R2-2, R2-3, R2-4, R2-5, R2-7, R2-8, R2-9, R2-10, R2-11, R2-12, R2-13, R2-14, R2-15, R2-16, R2-17, R2-18, R2-19, R2-20, R2-21). R1_RESOLUTIONS.md sha256 `2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4` (R-1…R-9, in force unless amended by R2). R3_RESOLUTIONS.md sha256 `202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf` (R3-1, R3-2, R3-3; in-place micro-edits, no version bump).
  - **Reviews.** IR1-C.md sha256 `295e96b3f5871cdf4142df169dc8811cef0aa38e7a7eb1930b246f60f0a426b9` (all items addressed to DEL-02-01); IR1-A.md sha256 `31b3c7f8493f05ee5fed6a11208f6811d2449d8a4fe72aae6300c2850b648284` and IR1-B.md sha256 `70e4a4f6d88f475687a9fde56a566a6913081dd3dd560402c1db8996dffd2846` (items addressed to DEL-02-01). Earlier: V1-A `01811533…cfe04c09`, V1-C `8d46258a…94a6`.
  - **Sibling v0.2 texts read at commit `28bd00499`** (via `git show`, not the working tree): DEL-03-01 `CATALOG_AND_READ_BASIS.md` C-v0.2 sha256 `358182b18b1fe13f9af6e6f5a61c9ed57f91b6ab29ea0c9adab06fe0081d6d82` (§3, §4.1, §5, §10); DEL-04-01 `ACT_AND_POLICY_CONTRACT.md` v0.2 sha256 `e50f1fe2f5bb2e3280bc62175e5aeeaa4508eed713424d82c54536a9fb5993a9` (§2.3–§2.5, §4); DEL-05-01 `LOOP_RECEIVING_CONTRACT.md` LOOP-v0.2 sha256 `1151d432c106ed3c1980918eca9d9360116292e3b9c602ed67f4c2d6718762c9` (§2.4); DEL-03-02 `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` P-v0.2 sha256 `942c1a3ab5ad7bda865640067f0fd550d7cfd1acd8f6ee228f6906452adf8c89` (§4.3, §9). Where R2 amends these texts for v0.3, the amended element is cited "per R2-n; sibling v0.3 to confirm".
  - DEL-05-02 PANEL-v0.2 needs known through IR1-C J2/J3 (file not read). DEL-02-02, DEL-02-03, DEL-02-04: accepted SoWs only. SWBPIPE answers received 2026-09-28 (RELAY_ANSWERS_SWBPIPE.md, above); no SWBPIPE consumer needs, commitment or contribution received (DEP-001). (This line records the earlier passes. At v0.7 PANEL is read directly: first bullet.)
- Receivers: CASE-002 M1 "Workflow-contract owner" row: DEL-02-03 (OUT-001, OUT-002; REQ-001, REQ-002, REQ-004; VER-001, VER-002, VER-004; W7 in this undertaking); DEL-05-01 (OUT-001, OUT-004; REQ-005, REQ-007; VER-008); DEL-05-02 (OUT-001; REQ-001; VER-001); DEL-02-01 self-check (OUT-004; REQ-004, REQ-005; VER-004, VER-005). DEL-02-02 (OUT-001, OUT-004; REQ-005; VER-004) and DEL-02-04 (OUT-001, OUT-002; REQ-001, REQ-002, REQ-004; VER-001, VER-005) remain named receivers but are outside this undertaking per owner ruling D1. From the live registers (R9-6; ACTIVE rows; detail in §8): DEL-02-03 (DEP-02-03-009); DEL-03-02 (DEP-03-02-027); DEL-03-03 (DEP-02-01-027); DEL-03-04 (DEP-03-04-008); DEL-05-01 (DEP-05-01-016); DEL-05-02 (DEP-05-02-005); DEL-09-06 (DEP-09-06-025); and, outside this increment, DEL-02-02 (DEP-02-02-014), DEL-02-04 (DEP-02-04-011), DEL-08-02 (DEP-08-02-006), DEL-09-02 (DEP-09-02-015) and DEL-10-03 (DEP-10-03-008).

Companion: [EXAMPLES.md](EXAMPLES.md) (DEL-02-01/WD-EX-v0.8). Beside this file (PROPOSED, R12-1, R12-2): the schema [workflow-declaration.schema.json](workflow-declaration.schema.json) with its conformance instances [workflow-declaration.valid.example.json](workflow-declaration.valid.example.json) (E1) and [workflow-declaration.invalid.example.json](workflow-declaration.invalid.example.json), and the design prototype [prototype/](prototype/README.md) (not product code, R12-3).

---

## Changes from v0.7

Wave B design development (run `APP-V4-DESIGN-PASS-2-20260930`, node B1;
R12-1). Rows carry the survey item (S1-C §A.8, "WD n"; "D-n" as in S1-C §A.6)
or the ruling. Every new structure is PROPOSED unless a cited ruling decides
it. No existing rule, value or expected result changes; the new elements are
optional, except the designating line of a message-form output. The file
stays DRAFT: unsupplied, unimplemented and not accepted.

| Item | Change in v0.8 | Where |
|---|---|---|
| R12-1 (version) | WD-v0.7 → WD-v0.8 | Header |
| WD 5 (U-01; S1-C §A.4, §A.5) | **Carriage** PROPOSED: one fenced block with the info string `workflow-declaration` in `WORKFLOW.md`, holding JSON. The three options are weighed; rules CR-1…CR-7 | §3.2 R-4; new §3.5; §7 |
| WD 5 (U-02); R12-1, R12-2 | **Representation** PROPOSED: JSON with Chirality's own snake_case field names; schema `workflow-declaration.schema.json` (JSON Schema 2020-12) beside this file, with a valid (E1) and an invalid conformance instance; the element-to-field map. Contract version value `WD-v0.8` | §1; §3.3; new §3.6 |
| WD 9 (S1-C §A.5) | **Reading order** VO-1…VO-10 with its precedence; name rules DN-1…DN-4; new FB-20, FB-21 and FB-22; FB-02, FB-13 and FB-19 widened | new §3.7; §11 |
| R12-1 (states, sequences) | Reading states and re-read triggers; operating sequence OS-1…OS-10 with the failure at each step | new §3.8, §3.9 |
| WD 5 (U-03, its semantic part) | Revision **file set and canonicalization** RV-1…RV-5; the algorithm stays open | §6.1; §12 U-03 |
| WD 5 (S1-C §A.5, interfaces, point 4) | Required tool references carry a **tool local name**, by which checkpoints, inputs, outputs and held actions refer to them | §4.2.2 |
| WD 6 (U-08; D-9) | Ten **harness capability names**, PROPOSED and scoped to Codex pin 0.158.0, each with its meaning and its basis in the generated schema; rules HC-1…HC-6; a delegation need is declared as `agent-delegation` | §4.2.1; new §4.2.5; §4.7 |
| WD 7; R12-10 (R10-8; D-5) | Output **production** element: a host-change output names its producing outcome, a file output its path, and a message output its **designating line** (OP-1…OP-6), the element LOOP §2.4.1's note waits for. New output element **relies on**, which the subject class "objects a named output concerns" needs. The output form **human-act standing** is made explicit (E1 `checked-rows`) | §4.4; §4.3.1; §4.3.5 RW-2 |
| R12-10 (A3 carry; EXEC SP-6F) | New checkpoint element **fresh act required** (PROPOSED): together with `governed`, it takes up EXEC SP-6F for that checkpoint in the governance phase; rules FA-1…FA-5. I-8's sentence that no such element is defined is replaced | §4.3.1; §4.3.3 I-8 |
| WD 10 (U-32) | Decided: an optional checkpoint element **on subject absent** (PROPOSED), plan guidance only; it changes no disposition (EXEC §4.7) | §4.3.1; §12 U-32 |
| (§4.1) | Input kinds named as values; a host read names the tool it is read through; an output of another workflow run names that workflow and its output | §4.1 |
| (joins) | §8 states what each receiver newly receives at v0.8 | §8 |
| R12-1 (verification) | VC-46…VC-56 added; VC-19's inventory re-pointed; new §13.1 states what each case needs to run and what the prototype ran on 2026-09-30 | §13 |
| (UNRESOLVED) | U-01, U-02 and U-08 PROPOSED, with consumer confirmation pending; U-03 narrowed to the algorithm; U-32 decided | §12 |
| **R14-5** (V18-2 M-1, m-10; repair node RP-3, in place, no version bump) | §4.2.5 gains a column naming the HOSTING §8.4 group each harness capability name resolves to at 0.158.0, with the group members the name does not rely on; new HC-7 (group mapping). HOSTING's grouping of the three disputed members stands: `functionCallOutput` (HCG-A06) and `mcpServer/elicitation/request` (HCG-A07) leave HC-6's "not named" list, and `thread/shellCommand` stays an App-origin client method in HCG-A02; no WD name would then mean something its group does not offer, so nothing is returned. HC-4 reads presence through the mapping; §4.2.1 cites HOSTING §8.4 | §4.2.1; §4.2.5; §8; U-08; VC-50 |
| **R14-6** (V18-2 M-2; V18-4 m-8) | The outcome token `applied_receipt` becomes P's `applied`, in the text, the schema enum, the valid example, the E1d fixture, EXAMPLES and the prototype together; the rule says WD follows the outcome owner (P-v0.8 `item_state`) | §3.6; schema `host_outcome`; `workflow-declaration.valid.example.json`; `prototype/fixtures/E1d.declaration.json`; `prototype/wdproto.py`; WD-EX |
| **R14-8 N-18** (V18-4 J10, m-8) | WD cites P-v0.8's five contributions to arc N-18 with their sections and schema members: change-item content identity (§3.1, §3.4, PM-6), per-item dispositions (§4.1, §4.6 PT-1…PT-19), all-items-decided (§4.3, DS-4), item-left events (§4.3; explicit in P's schema per R14-8), applied outcomes with resulting objects (§9); the P-state to item-state mapping is written out | §4.3.6; §4.3.7; §8 |
| **R13-6** (V18-2 m-13, n-5) | The `mcp-tool-call` row records the OBS-1 observation at 0.158.0 (MCP tools offered as a `namespace` tool, dropped on the local Responses route) as a limit of that route, citing HOSTING §10.1 | §4.2.5 |
| V18-2 m-2 | A file output must name its `path` (schema `if form = file then required path`); without it the output is not established and a kind (b) checkpoint on it is not established (VO-5); new variant L-WDEX-42 | §3.6; §3.7 VO-5; schema `returned_output`; VC-48 |
| V18-2 m-5 | §3.6 states WD's tokens as the declared part's canonical spellings and gives the one-to-one mapping to EXEC's and RS's spellings; reports need the tool local name | §3.6 |
| V18-2 m-7 (R12-10; V17-A N-4) | "Prior act not counted" in the one wording of RS L-13, with its reason, in live text (FA-1, I-8, §4.3.4, run end, VC-31, VC-32, VC-39); change-table history rows keep their wording | §4.3.1; §4.3.3; §4.3.4; §13 |
| V18-2 m-9 | New `$defs/workflow_identity` in the schema (origin `host`, never "host-supplied"; derived-from a nested tuple), with conformance instances in `prototype/fixtures/workflow-identity.examples.json` | §3.6; schema; U-02; VC-47 |
| V18-2 m-11 | A15 (register workflow revision, PROPOSED in ACT) named among the recognized kinds outside the closed list | §4.3.2 |
| V18-2 m-12 | HC-6 follows HOSTING §6.1's wording for an MCP elicitation (prompt authored by an MCP server or the agent) | §4.2.5 HC-6 |
| (verification) | Prototype rerun after the repair: 62 checks, 62 passed (new S-10 identity instances, S-11 name-to-group mapping against HOSTING §8.4, L-WDEX-42) | §13.1; `prototype/` |

## Changes from v0.6

Wave A alignment (run `APP-V4-DESIGN-PASS-2-20260930`, node A1-C). Rows are
keyed by R9 ID and by the survey item they answer (S1-C §A.8, "WD n"; "D-n" is
a disagreement listed in S1-C §A.6 or §C.6). At node A1-C: no new design
content, and no rule, value, label or expected result changes. Rows marked
node A2 apply R10 to the passages they name. At node A3 (DECISION-K1): SP-6
became the SETTLED earlier-act rule for the current phase (EXEC SP-6; I-8;
K1-2); the R4-5 rule is kept as EXEC SP-6F, a governance-phase option
(PROPOSED); the joint answer (EXEC §4.7 JA-1) was added to I-4 (K1-3); and
VC-31, VC-32 and VC-39 were recomputed. The file stays DRAFT: unsupplied,
unimplemented and not accepted.

| R9 ID (survey item) | Change in v0.7 | Where |
|---|---|---|
| R9-5, R9-11 (WD 1) | Version v0.6 → v0.7. Header re-pinned: the four basis docs at their current sha256, naming SCA-V4-001 and SCA-V4-002; the current ScopeOfWork sha256 with the amendments that revised it; R8 at its current sha256 (R8-1…R8-13); the intake OWNER_DECISIONS at its current sha256; BASIS-ALIGN DECISION-7 (O-25); DAG-003; the SWBPIPE answers at `afb6e063…`; siblings by version label and section only. V1-A abbreviation corrected (`…c04c09` → `…cfe04c09`). Earlier Consumed-inputs bullets are kept as records of their passes | Header |
| R9-1, R9-3 (WD 2) | Checkpoint wording re-pointed to PRD V4-WF-05 and HI V4-HI-42 as amended, quoted in §4.3.0; the R9-1 summary sentence is used in the Phase line and S-F. The two-halves reading of V4-WF-05 and the basis-update marker are dropped. What is in force in every phase and what is phased to the governance layer are stated. V4-HI-42 is no longer described as guidance only: its request clause and record clause are in force, and only the hold is phased. U-33 closed | Header, §2 S-F, §4.3.0 (lead, CG-4, CG-7), §12 U-33 |
| R9-1 (requester; recording) | New paragraph after CG-7: who requests in the current phase (INTEGRATION; put to the owner in this run's decision package). Recording is required where the arrival is observed: "may be recorded" is reworded in CG-6, in the reached-when element and in RW-2. The observation mechanism is EXEC's, in Wave B; none is stated here | §4.3.0, §4.3.1, §4.3.5 RW-2 |
| R9-2 (WD 2) | R8-11 item 2 and R8-12 item 2 restated against the amended text: I-7's closing sentences, FB-14, VC-11 and U-34 ("no A5 is forced, and none is recorded") | §4.3.3 I-7, §11 FB-14, §12 U-34, §13 VC-11 |
| R9-4 | S-F and U-34 cite the owner's confirmation of the R8-11 item 2 reading (BASIS-ALIGN DECISION-7, OWNER_ITEMS O-25) and its restatement by R9-2 (DERIVED) | §2 S-F, §12 U-34 |
| R9-8 (WD 8, D-3) | Standing labels follow rulings already made: I-4 is ADOPTED (R4-3); SB-4 is ADOPTED (R4-6); PH-6 and PH-8, cited in CG-6, are confirmed INTEGRATION (R8-11 item 1). I-8, run end and §6.4 stay PROPOSED (R4-5, R4-4; R9-4) | §4.3.0 CG-6, §4.3.3 I-4, §4.3.6 SB-4 |
| R5-1, R8-11 item 3 (WD 8, D-1) | Pass-rule paragraph: a required reference *not established* gives the check result *not established*, stated beside the "does not pass" sentence, as EXEC §3.5 has it. No rule changes | §4.2.4 |
| SoW REQ-002, CLM-002 (WD 3) | §4.2.1: harness-capability meaning is supplied through DEL-01-01 (was `UNRESOLVED`). The names stay open (U-08) | §4.2.1, §12 U-08 |
| R9-6; SoW CLM-002, REQ-006, TBD-004 (WD 3) | Receivers line and §8 receiver table rebuilt from the ACTIVE register rows: DEL-03-03, DEL-03-04 and DEL-09-06 rows added; the outside consumers DEL-08-02, DEL-09-02 and DEL-10-03 added; DEP row IDs shown. §10 gains the DEL-03-03 carriage row, and its DEL-02-03 row cites TBD-004 | Header, §8, §10 |
| (WD 4) | RS, PANEL, LOOP, P and HOSTING read directly. "Not read", "via IR1-C" and "header checked" in the §8 supplier states and in §9 A-1 and A-10 are replaced by section citations. U-11 closed (RS). U-17's internal half becomes a confirm-or-object request | §8, §9 A-1, A-10, §12 U-11, U-17 |
| R9-9 (WD 8: D-4, D-5, D-6; V6 m-7) | **Not changed**, returned as R10 candidates: the unphased "on negative decision" row against LOOP §2.4; the message-form output designation that LOOP §2.4.1 uses; whether an A12 checkpoint may require a network-destination grant; which rule values a declared, malformed held-actions element on an A5 or kind (a) checkpoint | §4.3.1, §4.4 |
| R9-11 (labels) | Own and sibling version labels in §8, §9 and VC-19 moved to the Wave A versions | §8, §9, §13 VC-19 |
| **R10-1** (node A2, in place; R9-2's second bullet corrected) | I-7's closing sentences, FB-14 and VC-11: a direct application queues no proposal, so the A5 checkpoint is **not reached**; nothing is requested by reason of an arrival that did not occur, no A5 is forced and none is recorded. A checkpoint reached under such a grant has its act requested and is *waiting*. "The checkpoint's act is still requested" is withdrawn for the direct-application case | §4.3.3 I-7; §11 FB-14; §13 VC-11 |
| **R10-7** (node A2, in place) | "On negative decision", element absent, labelled by phase as LOOP §2.4 has it: current phase, the agent follows the plan it worked out with the person; governance phase, for a governed checkpoint, the run stops at the checkpoint; in both phases the run is never recorded as if the act were positive | §4.3.1 |
| R10-9 (node A2, in place) | A checkpoint's "grant setting" is an operation-class grant only; a checkpoint on a network-destination grant is a possible later extension, PROPOSED, not defined | §4.3.1 validity rules; §4.3.6 |
| R10-10 (node A2, in place) | Held-actions conservative default: governance phase only; applies to any **declared** held-actions element that does not show host operations only, whatever the checkpoint kind. R7-3's derivation for an absent element is unchanged; no new failure row | §4.3.1 held actions |
| R10-11 (node A2, in place) | §8 DEL-09-06 row lists the examples CA uses: E1, E1c, E1d, E8 (was E1, E3) | §8 |
| **K1-1** (node A3, in place; owner DECISION-K1 of 2026-09-30, `APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md` sha256 35d6546346907137581be7df3bed4a8ccdb4b8bc55a261ca716040d0ad9f91bc) | Who requests in the current phase: relabelled **SETTLED by DECISION-K1 K1-1** (was INTEGRATION, put to the owner) | §4.3.0 |
| **K1-2** (node A3, in place) | I-8 rewritten: in the current phase an earlier act counts when it is of the required kind and the content it was made on is still current, and the record cites it and its time (EXEC SP-6); capture at or after arrival is kept only as a governance-phase option (EXEC SP-6F, PROPOSED). "Prior act on this subject, not counted" stays for an earlier act whose content is no longer current or whose kind differs, or under that option. §4.3.4 *waiting* and *performed* rows and the run-end paragraph follow; U-31 closed; VC-31, VC-32, VC-39 recomputed; §8 DEL-02-03 row | §4.3.3 I-8; §4.3.4; §8; §12 U-31; §13 |
| **K1-3** (node A3, in place) | I-4: two or more acts may together answer one arrival, each citing its items; after a partial lapse an act on the lapsed referents alone answers together with the earlier act for the unchanged ones (EXEC §4.7 JA-1). *Performed* row follows. U-05c closed | §4.3.3 I-4; §4.3.4; §12 U-05c and closing note |
| **K1-4** (node A3, in place) | U-25 closed: the App records the person's identity from what it can observe, marked *identity not verified* (EXEC CAP-8); a verified identity is governance phase. The act control's construction stays DEL-01-04's; its obligation is proposed for DEL-01-04's contract at the next amendment (DECISION-K1 K1-4) | §12 U-25 |
| **R11-4** (node A4, in place; V17-B M-2) | The preamble of this table is scoped to node A1-C; it now says that rows marked node A2 apply R10, and states what node A3 changed (SP-6 SETTLED for the current phase; the R4-5 rule kept as SP-6F, a governance-phase option; the joint answer added to I-4; VC-31, VC-32, VC-39 recomputed) | Preamble of this table |
| **R11-3** (node A4, in place; V17-B M-1) | Header: a new line pins this run's records at their final bytes: R9 `a64e2415…`, R10 `ad3b6caa…`, R11 `e7343b66…`, OWNER_DECISIONS `7458e9e8…`. The node A1 input line and the K1 rows keep the bytes read then | Header |

## Changes from v0.5

Keyed by R8 ID; sources are I2 rows of INTAKE_MAP.md. R8 overrides I2 where
they differ. SETTLED means by DECISION-3 or DECISION-4. The owner file EXEC-v0.4
was revised first; this file follows it.

| R8 ID (source) | Change in v0.6 | Where |
|---|---|---|
| **R8-1** (DECISION-4 D4-1; SETTLED, framing INTEGRATION) | New **§4.3.0**: in Phase 1 checkpoint declarations are **plan guidance**. The person and the agent plan around them, and the agents manage their own pauses. Neither the App nor a host's embedded loop enforces a hold or reports *unsupported* for a hold reason. Acts are recorded only when the person performs them, and reserved acts stand. Arrival and act may be recorded as observation. *Action during hold* becomes the optional annotation "continued past ‹checkpoint› before ‹act›". Mirrors EXEC-v0.4 §2.1 | §4.3.0, S-F, S-T |
| **R8-1** (fields kept; `governed`) | Every §4.3.1 field is kept, because every workflow that needs governance must be serveable. New optional element **`governed`** (PROPOSED), with its meaning in each phase: in Phase 1, guidance only; in the governance phase, the checkpoint is held on the acting surface per §4.3.8, its hold support enters the check, and the R4-8 reason can apply. Absent means not governed, which is guidance in every phase. New FB-19 for an unrecognized value | §4.3.1, §11 FB-19 |
| **R8-1** (§4.2.4) | The *unsupported* reason "checkpoint hold not enforceable on this surface" applies **only to governed checkpoints in the governance phase**. The pass rule's hold-support clause is marked governance phase; in Phase 1 no checkpoint enters the pass rule | §4.2.4, §3.4 |
| **R8-1** (governance phase retained) | §4.3.8 (hold support; HS-1…HS-5; what "held" means; precedence), I-4's re-hold branch, I-7's constraint carriage, I-9, RW-2's held call, FB-13's "does not proceed", FB-14 and FB-18 are **relabelled governance phase (retained)**, each with a Phase-1 statement beside it. Nothing is deleted | §4.2.2, I-4, I-7, I-9, §4.3.4, §4.3.5, §4.3.8, §11 |
| **R8-1** (V4-WF-05) | V4-WF-05's first half is **phased to the governance layer, not withdrawn**, and flagged for the next accepted-basis update (new U-33). S-F is annotated | Header, S-F, §4.3.0, U-33 |
| **R8-1** (VCs) | **VC-37** and **VC-43** take the two-part Phase-1 / governance-phase form; VC-10 (ii), VC-11, VC-33 and VC-38 likewise. New VC-44 (Phase-1 guidance semantics) and VC-45 (`governed` flag). VC-19 inventory re-pointed to v0.6 | §13 |
| **R8-2** (P2.1, P2.4–P2.6, P2.16, P2.17; I2 R8-Q-HS4) | Governance-phase values recomputed with SWBPIPE's SQ-02 answer (route (iv), none planned) → HS-3 (c) *not enforceable*. The "(today)" marker is removed. HS-4 no longer masks SWBPIPE entries (SQ-11 answered). U-19 and U-30 are restated. **D6 is closed for Phase 1** and re-opens with the governance phase. The closing paragraph of §4.3.8 is updated | §4.3.8, U-19, U-30 |
| **R8-2** (P2.13) | Authoring advice: against SWBPIPE no governed checkpoint is enforceable from the App on X; the advice stands for a host that offers a host-held route | §4.3.8 |
| **R8-3** (Part 3 item 2) | §4.3.7 closing: per-item staleness where the host supplies subject identities; otherwise the host's stated scope (SWBPIPE: whole model) is received and shown, never narrowed; de-duplication first is unchanged | §4.3.7 |
| **R8-4** (03.4; Part 3 item 3) | SB-3: a whole-model identity is received as every covered subject's identity. This errs toward a lapse and never misses one; the App never computes identities. SWBPIPE binds only to the whole-model identity (new U-35) | §4.3.6, U-35 |
| **R8-5** (09.3; Part 3 item 10) | §4.3.7: #885 `withdrawn` is an item leaving, "cleared by the person, no decision record", and never A10 or A11. Accept-and-apply is one step per batch on SWBPIPE, so per-item A5/A10 and mixed-item rows have no SWBPIPE counterpart; the meanings are kept | §4.3.7 |
| R8-7 (01.1, 11.4, 12.3, 19.1, 31.4; Part 3 item 12; Part 4.11) | Standings moved to **answered**: header, §8 SWBPIPE row, U-05b (SQ-01), U-23 (SQ-11), U-09 (SQ-19 (d)). OI-003 is qualified as "App v4 OI-003". Notes added: §4.2.1 (SQ-12, no per-operation identity); I-7 (SQ-02 (a), SQ-31, strict preflight, R8-10) | Header, §4.2.1, §4.2.4, I-7, §8, §12 |
| R8-10 (I2 R8-Q12) | The agent never adds a field the host's schema lacks. The expected constraint is recorded App-side ("constraint not carriable on this host") | §4.2.2, I-7 |
| (A1, flagged) | New U-34: the Phase-1 standing of I-7 / V4-HI-42 and of D2's "or a declared checkpoint" clause (EXEC U-E24). The disposition words as record labels and lapse recording in Phase 1 follow EXEC PH-6 and PH-8 (PROPOSED (A1)) | §4.3.0, §12 |
| **R8-12** (items 1, 7; closing pass, node A6, in place) | **U-34 closed in place by R8-11 item 2** (with EXEC U-E24): D2's reserved-act half binds in Phase 1 (host-enforced); its checkpoint half, I-7 and V4-HI-42 are guidance in Phase 1 and bind only for governed checkpoints in the governance phase. I-7, S-F, FB-14 and VC-11 re-pointed. PH-6/PH-8 confirmed by R8-11 item 1. Phase-1 lapse after resume labelled **"act lapsed at ‹t›"** (item 1) in I-4, the *waiting* annotations and VC-10. Consumed inputs list the post-R8 sibling versions; §8 supplier states name the current versions (earlier readings kept) | Header, §2 S-F, §4.3.3 I-4, I-7, §4.3.4, §8, §11 FB-14, §13 VC-10, VC-11, UNRESOLVED |

## Changes from v0.4

| R5 ID (source) | Change in v0.5 | Where |
|---|---|---|
| R5-1 (V3-A MAJOR-1; V3-B MAJOR-5) | §4.3.8 now uses the **four ruled hold-support values** owned by EXEC §3.6: *enforced by the host loop*, *enforced on the host route*, *not established*, *not enforceable*, with their check effects (pass · pass · *not established* · *unsupported*). "Enforced before dispatch" and "held after observation" retired; the v0.4 "A5 on the host route passes with AWAITING INPUT" exemption withdrawn: pending SQ-02 is *not established*. Pass rule extended. U-30 restated (App-only checkpoints *not enforceable* whatever SWBPIPE answers; SQ-02 decides host-operation checkpoints only, per R5-10). | §4.2.4, §4.3.8, I-9, U-19, U-30, VC-37 |
| R5-2 (V3-A m-6; V3-B MAJOR-1) | Carriage assurance final: **host-held** (host derived it from, or verified it against, its own resolved copy; includes the host loop's own evaluation); a constraint the host merely received keeps its source's assurance; **App-assured is not available in this increment**; only host-held satisfies R2-12. | §4.2.2, I-7, EXAMPLES R-5b |
| R5-3 (V3-A m-5; Y-2) | The **declared** setting content always binds an A12 checkpoint and must always be named; invalidity is unconditional; an A8 may present that content but never changes the subject; an A12 on different content satisfies nothing; a run-dependent scope is declared as a **binding rule resolved at arrival** (e.g., "targets of the held call"), never chosen by an A8. | §4.3.1, §4.3.6, FB-17 |
| R5-7 (V3-A MAJOR-3/5) | EXAMPLES R-16 (ii)–(v) re-pointed to C **V-GR1** (per R5-7; present in C-v0.5); **L-WDEX-11 retired, not reused**. R-16 (i) stays the main-order negative. U-31 records the owner-visible cost. | EXAMPLES, U-31, VC-32 |
| R5-9 (V3-A m-1, m-2, m-3, m-12; V3-B) | Citations re-pointed to current sibling versions (EXEC-v0.2, C-v0.4, ACT-v0.4, LOOP-v0.4, P-v0.4, CA-v0.2); FA-n → **FXA-n**; ⟨fx-proj⟩ → **LIB-A1**, plus LIB-A2 and AF-1; FXA-5 stated correctly (⟨rev-3⟩ declares `CP-accept` **and** `CP-check`); "pending its v0.4" markers closed. L-WDEX numbering kept stable (EXEC cites it). | Header, §8, U-23, EXAMPLES |
| V3-A m-10 | MX-8 row rejoined to its table; FB rows ordered 16, 17, 18. | §4.3.7, §11 |
| R6-1 (V4-A MAJOR-1/2; EXEC F-28) — in place | Hold support is decided by **held actions**, not by arrival: §4.3.8 adds the assignment rule (EXEC HS-1, HS-2, HS-5, HS-4, HS-3 in that order; HS-3 by SQ-02 status). New §4.3.1 element **held actions** (INTEGRATION), declared as "host operations only" or as listed App-side steps, with the conservative default. E1d via X includes E1c's `CP-check` → **unsupported**; E1c via X → **unsupported**. WR-11 advice stated. VC-37 updated; new VC-43. | §4.3.1, §4.3.8, VC-37, VC-43, EXAMPLES E1/E1c/E1d/E8 |
| R6-2 (V4-A m-3) — in place | EXAMPLES R-16 (iv): in V-GR1 (GR-R) the refused A12 is T15's own, so **⟨set-1⟩** stays in force. | EXAMPLES R-16 |
| R6-3 (GUIDE-v0.2 G-11) — in place, parent | I-4 re-hold sentence qualified per hold-support value (the run stops only under *enforced by the host loop*). Applied by HELP_HUMAN. |
| R6-3 (V4-A m-4) — in place | I-9 and §4.3.8 state what "held" means per value: host loop → the run stops at its next action; host route → the host refuses the held host operations, other actions are *action during hold*; not established / not enforceable → nothing is stopped, actions are *action during hold*. | I-9, §4.3.8 |
| R6-4 (V4-A m-1, m-9) — in place | Stale "pending"/"C-v0.5 to add" markers removed (V-GR1 exists in C-v0.5); §8/§9 version labels corrected to v0.5; supplier states re-pointed; VC-41 cites R4-9 and R5-3, "even with an A8 presenting a setting". | Header, §8, §9, VC-41 |
| **R7-3** (V5 MAJOR-3; INTEGRATION, option (a)) — in place | §4.3.1 *held actions*: when the element is absent, the held actions are **derived** — the governed operation(s) for an A5 checkpoint, the held call for a kind (a) checkpoint (as EXEC §3.6 defines them). The conservative default (at least one App-side step, EXEC HS-5) applies only when a kind (b)/(c) checkpoint has no held-actions element, or when its declared held actions do not show host operations only. §4.3.8 HS-5 row scoped the same way. VC-43: the L-WDEX-17 checkpoint (kind (a) `CP-grant` on OP-C9) with no held-actions element is HS-3 → **not established** today (was HS-5 → *not enforceable*); its workflow result follows EXEC §3.5 precedence with the run's other checkpoints — L-WDEX-17 has none, so **not established** today. No other value changes | §4.3.1, §4.3.8, VC-43, EXAMPLES E8 |
| **R7-4 m-5** (V5 m-5) — in place | §4.3.8 value table: "a constraint carried only as *model-supplied*" → **not enforceable** is qualified "once SQ-02 is answered with no host-held route (HS-3; before that answer, *not established*)" | §4.3.8 |
| **R7-4 m-8** (V5 m-8) — in place | Header: the R6 line notes that C `a6306bd4…` is the pre-R6-2 byte state; a new R7 line records the sibling inputs read at the R7 working state (EXEC, WD-EX, C, ACT, LOOP, P at `2f42fba02`, then with their R7 in-place edits); GUIDE pins the post-R7 bytes | Header |

## Changes from v0.3

Keyed by R4 ID and source finding. Labels as in R1–R4.

| R4 ID (source) | Change in v0.4 | Where |
|---|---|---|
| R4-2 (D6; EXEC §3.6, HP-1/HP-2) | New §4.3.8 **hold support**: every checkpoint has a per-surface hold-support value (EXEC §3.6). App-side run holds are `UNRESOLVED{D6}` pending SWBPIPE SQ-02; the declaration never implies an App hold that cannot be enforced; "action during hold" is recorded; neither interposed App code (HP-1) nor reliance on `turn/interrupt` (HP-2) is adopted. HP-3 stays a permitted best effort (D3). New settled row S-T (D6). | §2, §4.3.8, I-9, U-30 |
| R4-3 (EXEC §4.7; W7 F-2) | I-4 rewritten: resume point HD-5; a lapse after resume re-holds the **same arrival** ("waiting — re-held, lapsed at ‹t› after resume"), the run stops at its next action, nothing is undone, gated outputs show *lapsed*, the whole scope is re-requested; A5 and A12 never re-hold. The interim "performed + act-lapsed" display is withdrawn. U-22 closed. | I-4, §4.3.4, U-22 |
| R4-4 (EXEC §4.9; W7 F-4) | No resumption of an ended run; acts after run end are shown "after run end" and change nothing; continuation is a new run with a **continues ⟨run⟩** link, inheriting nothing; an interruption is not a run end. PROPOSED. U-21 closed. | §4.3.4, U-21 |
| R4-5 (EXEC SP-6; W7 F-3) | New I-8: an act counts only if captured at or after the checkpoint's arrival; earlier acts shown "prior act on this subject, not counted". PROPOSED; the owner alternative stays open as U-31 (EXEC U-E4). EXAMPLES R-16 repaired against C's T15→T16 order. | I-8, U-31, EXAMPLES R-16 |
| R4-6 (EXEC §4.10; W7 F-5) | SB-4 rewritten: an A12 counts and supersedes only when **established**; a refused A12 neither counts nor supersedes a setting in force; pending → *waiting*; lost confirmation → *unknown*. U-27 closed. | SB-4, U-27 |
| R4-7 (EXEC §4.11; W7 F-1) | §4.3.7 adds MX-3 (lost decision observation → *unknown*), MX-6 (all items left → arrival closed "replaced by arrival n+1") and MX-8 (application error or outcome unknown after A5 → unchanged, annotated). R2-18 and R3-3 **CONFIRMED** by DEL-02-03. U-20 closed. | §4.3.7, U-20 |
| R4-8 (W7 F-8) | *unsupported* gains the reason **"checkpoint hold not enforceable on this surface"** (from EXEC §3.6). | §4.2.4, §4.3.8 |
| R4-9 (W7 F-13) | A12 subject without an A8: the setting content named by the checkpoint's own declaration (classes, grant values, scope). An A12 checkpoint naming none is **invalid** (new FB-17). INTEGRATION. | §4.3.1, §4.3.6, FB-17 |
| R4-12 (W7 F-9) | I-5: answers to Codex user-input or MCP elicitation requests are **not act evidence** and never host act capture (EXEC CAP-6). U-25 narrowed to App act-control construction (EXEC §5). | I-5, U-25 |
| R4-14 (W8 F-1) | §4.2.2 no longer says "the external adapter carries". The constraint is carried with a **carriage assurance**: App-assured, host-held, model-supplied or absent; model-supplied alone does not satisfy R2-12. | §4.2.2, I-7 |
| R4-16 (W8 F-7) | *channel not enabled*: the App reports it when its own configuration is off; the host when its channel is off. | §4.2.4 |
| R4-18 (V2 MAJOR-1) | EXAMPLES R-5a/R-5b re-pointed to C V-CP1 and R-5c to C T15/⟨set-2⟩ (class P-03, scope {FX-W1; {S-4}}); local L-WDEX-2 removed. | EXAMPLES |
| R4-19 (V2 m-3, m-8, m-9, m-12, m-13) | OP-C10 class per R3-4 (governed by the reversed operation's policy record); m-8 framing stated (WD-EX runs use its own declared checkpoints; C declares only V-CP1); "C-v0.3 to add" and "to be confirmed at V2" markers closed; examples re-pointed to C-v0.3 §10 (T4a, T16a, S-5, V-S1, V-R1, V-X1, V-NP1, V-OU1); R3 and R4 added to Consumed inputs. | Header, EXAMPLES |
| R4-20 (W9 CA F-5) | E1 adopts optional OP-C12 host-check steps at Inspect and Re-examine (was DEL-09-06 L-CA-1). | EXAMPLES E1 |
| R4-21 (W7 F-16) | Reached-when kind (a) on a **harness capability** is not holdable in App runs pending D6; hold support reports *not enforceable* (new FB-18). | §4.3.1, §4.3.8, FB-18 |
| (W7 confirmations) | Holding library confirmed with HL-2/HL-3 (EXEC §6.2); transfer procedure and adaptation receiving supplied (EXEC §6.3–§6.7). U-24 and U-18 closed as PROPOSED (W7). | §6.4, U-18, U-24 |
| (EXEC U-E7) | "On subject absent" declaration path recorded as open (U-32); default is EXEC's *waiting* "subject absent". | U-32 |

## Changes from v0.2

The v0.1 → v0.2 change table is in the committed WD-v0.2 (sha256 above).

| Item | Change in v0.3 | Where |
|---|---|---|
| R2-17; IR1C-05; IR1C-01 (X-10) | **subject class** is its own element with the closed class list: change items of a named proposal · named output · objects changed by a named outcome · targets of the held call · grant setting. Binding rules per class. An A5 checkpoint must use reached-when kind (c) *queued* and subject class "change items of the named proposal" (new FB-16). "Targets of the held call" is valid only with kind (a) (IR1-C X-10 point 1, not contradicted by R2). Consumers bind the declared class, never infer it from the kind. | §4.3.1, §4.3.6, FB-16 |
| R2-18; IR1C-02 (X-14) | §4.3.7 stays the proposal all files cite. "Partial" is a per-item annotation, not a disposition. Items that leave without a decision are shown with their item-left events (supplied by DEL-03-02). A *performed* over a reduced subject is never shown as "all accepted". | §4.3.7 |
| R2-19; IR1C-07; IR1A-09 | Lapse sequence: an **act-lapsed event** is recorded; before resume the disposition returns to *waiting* ("waiting — lapsed at ‹t›"); after resume, re-hold is DEL-02-03's; *lapsed* as a standing disposition only for a checkpoint whose run has ended. | §4.3.3 I-4, §4.3.4 |
| R2-5; IR1C-08; IR1A-03, IR1A-18 (X-2, X-12) | "decline/stop event" renamed **act-declined event** (A4, A6, A7, A12; with capture evidence) → *resolved negatively*. Stopping the run is a separate **run-ended event**; a reached checkpoint stays *waiting*. An act after the run ended is recorded but does not change the ended run's disposition unless DEL-02-03 defines resumption. U-21 closed except resumption. | §4.3.3 I-6, §4.3.4, U-21 |
| R2-12; IR1C-03 (X-9) | The checkpoint-forced treatment travels as a **governing checkpoint constraint** {workflow run, checkpoint name, required act A5, operation}, carried by the loop and the external adapter in the change request (P §3.3, sibling v0.3). Direct request under it → *not permitted*, naming the constraint. VC-11 is **AWAITING INPUT** until host evidence exists. U-19 narrowed to the relay question. | §4.2.2, I-7, U-19, VC-11 |
| R2-7; IR1A-04 (X-13) | A12 binds to the **setting content** (classes, grant values, scope); a later A12 **supersedes**, not lapses; a checkpoint satisfied by the earlier A12 stays *performed* with the supersession shown. Whether a control-refused A12 can count is held for W7. U-27 narrowed. | §4.3.6 SB-4, U-27 |
| R2-20; IR1C-09 (X-11) | Holding library recorded at the *listed*, *selected* and *resolved* links; shown by the panel; carried in the loop's run association; never in identity equality; collision reports list it with each origin. PROPOSED until W7. | §6.2, §6.4 |
| R2-20 (X-17, X-18) | Capture-evidence reference and per-turn supplied-guidance identity stated as relay questions with consequences: no capture-evidence reference → no host-content checkpoint can be *performed*; no per-turn guidance record → *supplied* link *unknown*. | I-5, §6.2, U-05b, U-29 |
| R2-10; IR1C-22 | Recognized act kind outside the closed list → **invalid**; unrecognized name → **not established** (kept; DEL-04-01 aligns). | FB-03, FB-04 |
| R2-4 | Reserved entries are always offered, never reported *not exposed on this surface* for a class reason. At run time *not exposed on this surface* is reported by the host from element 9; an operation absent from the catalog edition offered to the loop is a loop-side *not offered* failure. The discovery-time requirement check still reads element 9. | §4.2.4 |
| R2-13, R2-14, R2-15, R2-16 | Binding uses the applied outcome's created/changed object identities and their post-application subject content identities (R2-14). Undo *reverses ⟨receipt⟩*; acts on content the undo changes lapse normally (R2-15). Accepted-then-stale: A5 not lapsed; item shown "accepted by ‹person› — not applied: refused — stale (both bases)"; checkpoint effect per §4.3.7 row added (R2-16). Retry de-duplicates by proposal identity before any basis check (R2-13). | §4.3.6, §4.3.7, §4.6 |
| R2-1 | Class element has five values including **no policy basis** (reason ∈ omitted, unassigned, pending OI-021); the declaration still does not restate classes. | §4.2.2 |
| R2-11 | Attribution checked: D2/D3 credited only with what they say; restrictions derived from R-2/R2 labelled DERIVED or INTEGRATION. | §2 S-Q, S-R, S-S |
| IR1C-13 | Requirement-check **pass rule** added: passes when every *required* reference is *present* or *present, currently unavailable* (the latter a run-time hold); optional references never block; undeclared stays selectable, never "runnable by check". | §4.2.4 |
| IR1C-14a/b | Purpose and scope bind with the act (V4-REC-05) and are carried with every act request at a checkpoint. | §4.3.1 |
| IR1-B B-m9 | Read-basis descriptor listed with five elements, adding the **identity method designation** (C §5.1). | §4.1 |
| R2-21; IR1C-15; IR1-B B-M8/B-M9/B-M10/B-m11 (X-6) | Examples re-pointed to C-v0.2 §10 identifiers (OP-C1…C9, T1…T17, S-1…S-4, PR-1/PR-2, RC-1…RC-3, B1/B2) plus OP-C10/OP-C11 fixed by R2-21. OP-C3 is **Examine** (A3 findings), not a host check. Fixture exposure assumed "exposed on all three surfaces" per R2-21 (C-v0.2 still shows *unagreed*). Local cases named `L-WDEX-n`. U-26 closed. | EXAMPLES |
| R3-1 (from finding F-1) | New subject class **objects a named output concerns**: objects identified in a named read/examination output, bound through their subject content identities as read. INTEGRATION. U-28 closed; E1b and VC-08 use it; new VC-36. | §4.3.1, §4.3.6, U-28, EXAMPLES E1b |
| R3-2 (from finding F-7; IR1-C X-10) | *Targets of the held call* valid only with reached-when kind (a) *before dispatch*: adopted as INTEGRATION (was cited to IR1-C only). | §4.3.1 validity rules, FB-16 |
| R3-3 (from finding F-4) | §4.3.7 accepted-then-stale row adopted as proposed: disposition unchanged, item annotated "not applied: refused — stale", output not produced for that item. PROPOSED; DEL-02-03 confirms at W7. | §4.3.7, U-20 |

Not repaired here (routed to closeout C1): V1-C RF-3 (no DOWNSTREAM rows),
RF-7 (U-08 register row), X-16.

---

## 1. Reading this definition

**What it defines.** The meaning of a portable workflow's *declared part* and
its relation to the prose method. The four roles and the single host seat as
App and host consumers receive them. Workflow source identity and the
promised-versus-observed distinction. The shared-contract responsibility map
(OUT-003), with each consumer need and each open allocation labelled.

**What it proposes at v0.8, and what it does not define.** It PROPOSES
where the declared part is carried (§3.5), its JSON representation with
Chirality's own field names and a JSON Schema (§3.6), and the order in which
a consumer reads it (§3.7), with consumer confirmation pending (U-01, U-02).
It does not choose a host or supplier wire format, TypeScript or other
language types, a parser implementation, a content-identity algorithm
(U-03), a transport (MCP or CLI), persistence, process/thread placement or
shared-component placement. It does not define
catalog entries (DEL-03-01), act kinds or policy (DEL-04-01), proposal
outcomes or the change request (DEL-03-02), record fields (DEL-04-03), the
checkpoint hold machine or transfer behavior (DEL-02-03), registration
(DEL-02-02), role supply (DEL-02-04), loop events (DEL-05-01) or panel
interactions (DEL-05-02).

**Naming convention.** Bold phrases such as **expected input** or
**reached-when** are *semantic element names*, not wire names, keys, headings
or type names. Their JSON field names at v0.8 are listed in §3.6. Act kinds use the canonical names A1–A14 (R-1; DEL-04-01 §2.1).

**Normative words.** "Shall" marks a meaning this contribution proposes.
"Settled" marks an accepted-basis distinction or an owner ruling, cited.
DERIVED / INTEGRATION / PROPOSED follow the R1/R2 labels. `UNRESOLVED{…}`
marks an open owner choice, which is neither a permission nor a default.

---

## 2. Settled distinctions this definition carries

| # | Settled distinction | Citation | Consequence for the declaration |
|---|---|---|---|
| S-A | A workflow is prose method guidance plus a declared part: expected inputs, host tools needed, checkpoints requiring a human act, returned outputs and evidence. | PRD V4-WF-01 | Five declared categories, prose retained (§3–4). |
| S-B | Workflows, skills and role guidance are ordinary open files (`WORKFLOW.md`, `SKILL.md`, `AGENTS.md`) readable by any capable harness; tool schemas stay open. | PRD V4-SHR-02; ARCH M-3 | The declared part must be readable without Chirality software (§3.2). |
| S-C | One workflow format and one set of four roles across the App and every host. | PRD V4-SHR-01, V4-ROLE-01 | No host-specific declaration dialect (§5). |
| S-D | Source-qualified identity: project, user, bundled or host-supplied; a selection is never silently rebound to a same-named workflow from another source. | PRD V4-WF-03 | Four origin classes; collisions exposed (§6). |
| S-E | The product can check that a selected workflow's required tools exist in the current host and tell the person when they do not. | PRD V4-WF-04 | Required tools are referenceable against the host catalog (§4.2). |
| S-F | When a run reaches a declared checkpoint, the required human act is requested, and it is recorded as done only when the person performs it, whatever the autonomy setting. Holding the run at the checkpoint until the act is performed is phased to the governance layer: in the current phase a checkpoint is plan guidance that the person and the agents manage, and neither the App nor a host's embedded loop enforces a hold, blocks a run, or reports a workflow unsupported because a hold cannot be enforced. The reserved acts (V4-HI-30) still bind (the R9-1 summary of the amended texts, which §4.3.0 quotes; U-33 closed). | PRD V4-WF-05 and HI V4-HI-42 as amended by SCA-V4-001; DECISION-4 D4-1 | Current phase (Phase 1): checkpoints are plan guidance (§4.3.0). **In force in every phase:** the act is requested; it is recorded as done only when the person performs it; the reserved acts bind. **Phased to the governance layer:** holding the run until the act; there the checkpoint hold is independent of the grant (§4.3.8). D2's "or a declared checkpoint" clause is read by R8-11 item 2 (a reading the owner confirmed: `APP-V4-BASIS-ALIGN-20260928` DECISION-7, OWNER_ITEMS O-25), restated against the amended text by R9-2 (DERIVED; U-34 closed): D2's "no autonomy grant widens past a reserved act" binds. For a declared checkpoint, V4-HI-42's request clause and record clause are in force whatever the autonomy setting; whether the run goes on before the act is for the person and the agents in the current phase, and the host's own treatment of its operations decides what the host does. |
| S-G | `success` means the operation ran; a submitted proposal reports "queued" until the host records acceptance and application. | HI V4-HI-25 | Success never satisfies a checkpoint (I-2). |
| S-H | Applying a change, accepting an edit, marking work checked, engineering approval and professional reliance are distinct; agents may prepare but must not represent an unperformed human act as performed. | PRD V4-AUT-03; HI V4-HI-30/31; d3 | Each checkpoint names one act kind; evidence of one kind satisfies no other (I-1). |
| S-I | Proposals say "accept", never "approve". | HI V4-HI-33 | "Accept" wording stays with A5 only (R-1). |
| S-J | A human act binds to identified content, scope and purpose and lapses visibly when that content changes. | PRD V4-REC-05; HI V4-HI-32 | Checkpoint subjects are bound to observable referents (§4.3.6). |
| S-K | Only observed events are shown as having happened; unobserved outcomes are unknown. | PRD V4-EXE-03 | Promises are kept apart from observations (§4.6). |
| S-L | Nothing the agent produces is presented as certified, sealed, approved or code-compliant. | PRD V4-AUT-05 | Outputs cannot promise approval standing (§4.4). |
| S-M | Roles recede in hosts behind one agent seat and the selected workflow; each host carries its own workflows, skills and tools. | PRD V4-HOST-05/06 | Host seat and host origin (§5, §6). |
| S-N | Roles are supplied additively; a bounded executor does not delegate; unenforced limits are stated, not implied. | PRD V4-ROLE-02/03 | Role compatibility is declared, not claimed as enforced (§4.7, §5). |
| S-O | Shared meaning does not prescribe a common executable service; shared implementation needs a concrete repeated responsibility; placement is open. | ARCH V4-ARC-20; PRD V4-SHR-03; d2; OI-014 | Map records needs and leaves placement open (§9). |
| S-P | A run leaves a compact record linking host receipts rather than copying them. | PRD V4-REC-04; HI V4-HI-70/71 | Declared evidence is by reference (§4.5). |
| S-Q | Reserved to the person (App/shared contracts, first increment; stands under DECISION-4): (a) marking work checked; (b) accepting a proposal wherever the active autonomy requires a proposal; (c) engineering approval; (d) relying on a result for a professional purpose; (e) changing the autonomy grant or **enabling** external-agent access. No autonomy grant widens past a reserved act or a declared checkpoint. The host names and enforces its own list; this does not show SWBPIPE adoption (DEP-001). | Owner ruling D2 (DECISION-1) | Mapped to A4, A5, A6, A7, A12, A13. Every act a checkpoint may require is reserved (§4.3.2). |
| S-R | In the App, routine tool-permission and sandbox modes (including any classifier mode) remain the user's own Codex setting; they govern tool execution only and never stand in for a reserved or professional act. In hosts there is no classifier permission mode in the first increment; the SWB default proposal mode applies. | Owner ruling D3 (DECISION-1) | A14 never satisfies a checkpoint; a checkpoint is not a permission prompt (§4.3.2). |
| S-T | App-side run holds at checkpoints were deferred to the SWBPIPE answer to relay question SQ-02 (`UNRESOLVED{D6}`). SWBPIPE answered on 2026-09-28: route (iv), none planned. **D6 is closed for Phase 1 by DECISION-4 D4-1:** checkpoints are plan guidance that the agents manage themselves; neither the App nor a host's embedded loop enforces a hold or reports *unsupported* for a hold reason; reserved acts stand; acts are recorded only when performed. D6 re-opens when the governance phase is taken up. In that phase: per-checkpoint hold support is carried for governed checkpoints; no App hold that cannot be enforced is claimed; action during hold is recorded; neither interposed App code nor reliance on `turn/interrupt` is adopted. | Owner decisions D6 (DECISION-2), as applied by R4-2; D4-1 (DECISION-4), as applied by R8-1, R8-2 | §4.3.0; §4.3.8; I-9 |
| S-S | Not settled by D2/D3 but carried: A10 is reserved wherever A5 is (DERIVED, R-1); an operation that performs A4, A5, A6, A7, A10, A12 or A13 is reserved to the person (DERIVED, R2-2); disabling external access is recorded as A13 (INTEGRATION, R2-3); an acceptance checkpoint forces a proposal (DERIVED from V4-HI-42 + D2b, R-5). | R-1, R-5, R2-2, R2-3, R2-11 | Labels kept distinct from the owner rulings. |

---

## 3. The workflow package and its two parts

### 3.1 Parts

A portable workflow is one package whose entrypoint is `WORKFLOW.md` (S-B).

| Part | Job | Who reads it | Authority |
|---|---|---|---|
| **Prose method** | Explains purpose, applicability, method, branches, recovery, judgment and handoff. | People and agents. | Method guidance; it grants no permission (Root `create-workflow`, retained). |
| **Declared part** | States, in a form a product can observe, what the method expects, needs, stops for and returns. | People, agents and product consumers (requirement check, checkpoint guidance and recording, and, in the governance phase, checkpoint hold; records; panel). | A declaration of expectations. It is not evidence that any expectation was met and grants no host permission. |

Both parts are required for a *declared* workflow. Where they disagree, the
consumer reports the inconsistency (FB-07) and does not silently prefer
either.

### 3.2 Readability obligations (OUT-001, OUT-002; REQ-001, REQ-002)

- **R-1** The declared part shall be readable as ordinary text by a person
  opening the package in an ordinary editor, without Chirality software,
  generated indexes or a running host (S-B).
- **R-2** Every declared element shall carry, or sit beside, a short
  human-readable statement of its meaning. An opaque reference alone, such as
  a catalog operation identity, is not enough.
- **R-3** The declared part shall live inside the package and travel with it.
  A derived index, registry or host database may reflect it but is not its
  authority.
- **R-4** Physical carriage is PROPOSED at v0.8 (§3.5; U-01): one fenced
  block in `WORKFLOW.md`. Each option was weighed against R-1…R-3. OUT-002's
  open declared-part schema is `workflow-declaration.schema.json` (§3.6;
  PROPOSED).

### 3.3 Declaration contract version

- **declaration contract version** identifies which version of this meaning
  the declared part is written against. Its value is the contract label,
  `WD-v0.8` at this version (PROPOSED; §3.6). No representation existed
  before v0.8, so no earlier value is readable. A consumer reads a declared
  part only at a version it knows; any other value is preserved, reported,
  and makes the declared part **not established** (§3.4; §3.7 VO-3; EXEC
  CR-3, TF-4, TF-8). A later version states its own compatibility with
  earlier readers; none is assumed.

### 3.4 Absent, partial and unrecognized declared parts

| Condition | Consumer meaning (all consumers) |
|---|---|
| No declared part (all current Root bundled workflows; any prose-only package) | The workflow is **undeclared**. It remains a readable, selectable method. Consumers report "requirements undeclared", never "no requirements". The required-tool check is **not established**, checkpoints cannot be product-held, and outputs/evidence carry no declared promise. |
| Declared part present, a category omitted | That category is **undeclared**. This differs from **declared empty** (an explicit statement that none are expected). Only "declared empty" supports "this workflow declares no checkpoints". |
| Unrecognized element or newer contract version | Preserve it unchanged and report it as unrecognized. An unrecognized element in the required-tool or checkpoint category makes the corresponding result **not established**, never a pass. For a checkpoint, that result is the checkpoint's own reading. In Phase 1 it does not change the requirement-check result; in the governance phase a governed checkpoint so affected makes the check *not established* (§4.3.0, §4.3.8 HS-1). |

### 3.5 Carriage of the declared part (PROPOSED at v0.8; U-01; S1-C WD 5)

**Options weighed.** Each satisfies R-1 (it is text). They differ as follows.

| Option | For | Against |
|---|---|---|
| (a) Front matter: the declared part as YAML between the `---` lines at the top of `WORKFLOW.md` | One file; Root already has front matter (`name`, `description`) | Nested structure in YAML needs a YAML parser, which neither the Python nor the node standard library has (R12-3 allows no install), and YAML's implicit typing reads some values in ways an author does not intend. A long header pushes the method below it. Root consumers that read `name` and `description` from the front matter would meet large structured values they do not expect |
| (b) **A delimited body section in `WORKFLOW.md`**: one fenced code block with a reserved info string, holding JSON | One file travels with the package (R-3), including a single-file package. The agent that reads `WORKFLOW.md` receives the declared part with the prose, which is the product's part (i) under DECISION-K1 K1-1 ("give the agent the declared checkpoint with the workflow"), with no second file to supply. Prose and declared part are reviewed in one diff. JSON is read by every language's standard library, and the block shows as a code block in any Markdown viewer (R-1) | Needs an exact delimiter rule, including a rule for quoted examples (CR-1…CR-4). JSON has no comments, so R-2 is met by the `meaning` and `purpose` members and by the prose around the block. A change to the declared part changes the prose file; that costs nothing, because the revision covers every file of the package anyway (§6.1) |
| (c) A companion file (for example `declaration.json` beside Root's `execution.json`) | The simplest parse; mirrors Root's `execution.json` | Two files to keep consistent. A person or harness given only `WORKFLOW.md` does not see the declared part, so every supply must name both files, and a single-file package becomes two. The Root precedent is a *restriction* file, and a requirement file beside it invites the misreading E6 guards against (§4.2.3) |

**Choice: (b), PROPOSED**, for the reasons in its row. The prototype
(`prototype/wdproto.py`, R12-3) renders E1 and E1d in it and reads them back,
reads the real Root packages E5 and E6, and a second extractor in node's
standard library gives the same JSON for E1 (WD-EX E1, E1d, E5, E6; §13.1).
The JSON document of §3.6 is the same whatever the carriage: moving to (c)
later would change only CR-1…CR-4, not the schema or anything a consumer
does after VO-2.

**Carriage rules (PROPOSED).**

- **CR-1 The block.** The declared part is the content of the fenced code
  block in `WORKFLOW.md` whose opening line has at most three leading spaces,
  a fence of three or more backticks (or tildes), and the info string
  `workflow-declaration` alone (surrounding whitespace ignored). The block
  ends at the first later line that has at most three leading spaces, the same
  fence character at least as many times, and nothing else but whitespace; if
  there is none, at the end of the file (CommonMark's fenced-block rule).
- **CR-2 Top level only.** A block inside another fenced block (for example
  an example quoted in documentation, as in WD-EX) is not read. A fence line
  must start at most three spaces from the margin, so a fence inside a block
  quote or an indented list item is not recognized either.
- **CR-3 Front matter.** The front matter (the lines between a first line
  `---` and the next line `---`) is skipped when the block is sought. It keeps
  Root's `name` and `description` only (§7).
- **CR-4 Exactly one.** No block: the workflow is **undeclared** (FB-01).
  Two or more: the declared part is malformed and none of them is read
  (FB-02).
- **CR-5 Content.** The block's content is UTF-8 JSON text (RFC 8259) whose
  top level is one object (§3.6). Line endings are normalized for reading
  only; the revision reads the bytes as stored (§6.1 RV-3).
- **CR-6 Layout.** Layout inside the block is free: any JSON text with the
  same content is read the same. Authors are advised to put the block last,
  under a heading "Declared part" with a sentence saying what it is and that
  it grants nothing (WD-EX E1).
- **CR-7 Method first.** The prose remains the method (§3.1) and names
  whatever the agent must do that the product observes, for example a message
  output's designating line (§4.4 OP-6). The agent receives the prose and the
  block together when it reads the file.

### 3.6 Representation and schema (PROPOSED at v0.8; U-02; R12-1, R12-2)

The declared part is one JSON object described by
[workflow-declaration.schema.json](workflow-declaration.schema.json) (JSON
Schema draft 2020-12), beside this file, with the conformance instances
[workflow-declaration.valid.example.json](workflow-declaration.valid.example.json)
(E1) and
[workflow-declaration.invalid.example.json](workflow-declaration.invalid.example.json)
(nine structural errors). The names are Chirality's own, with snake_case
members like the other Wave B schemas of this run; no host or supplier wire
field is selected (R12-1). The schema states the form a conformant author
writes. It fixes shape and vocabulary; combinations and references are the
reading steps of §3.7. A consumer never rejects a whole document for an
element's failure (§3.7 VO-5).

| Semantic element (section) | JSON member |
|---|---|
| declaration contract version (§3.3) | `declaration_contract_version` |
| the five categories (§4.1–§4.5) | `expected_inputs`, `required_tools`, `checkpoints`, `returned_outputs`, `returned_evidence`. Member omitted: **undeclared**; empty array: **declared empty** (§3.4) |
| expected input (§4.1): input name, meaning, input kind, necessity (with the effect of absence), quality or basis requirement, stage | `name`, `meaning`, `kind` (`host_read`, `file_supplied`, `person_supplied`, `workflow_output`), `necessity` (with `absence_effect`), `basis_requirement`, `stages`; for a host read `read_through` (the tool); for another run's output `source_workflow` |
| required tool reference (§4.2.2): tool local name, tool reference, version compatibility, purpose of use, necessity (with fallback), stage | `name`, `class` (`host_operation` or `harness_capability`) with `operation` (C's operation identity, opaque) or `capability` (§4.2.5), `versions`, `purpose`, `necessity` (with `fallback`), `stages`. The governing checkpoint constraint is derived, so it has no member |
| checkpoint (§4.3.1): checkpoint name, required act kind, reached-when, subject class, position, scope, purpose, actor requirement, on negative decision, on mixed decision, on subject absent, expected act evidence, held actions, governed, fresh act required | `name`, `required_act`, `reached_when` (`kind`: `before_dispatch` (a) with `tool`; `output_produced` (b) with `output`; `host_outcome` (c) with `tools` and `outcome`), `subject` (`class` with `output`, or `tools` and `outcome`, or `setting`), `position`, `scope`, `purpose`, `actor` (`the_person`, `the_accountable_professional`), `on_negative_decision`, `on_mixed_decision`, `on_subject_absent` (each `path`: `stop`, `return_to_stage` with `stage`, `proceed_on_branch` with `branch`), `expected_act_evidence` (`capturing_surface`, `description`), `held_actions` (`form`: `host_operations_only` with `tools`, or `listed_steps` with `steps` each marked `app_side`), `governed`, `fresh_act_required` |
| returned output (§4.4): name, meaning, output form, destination, promised standing, gating checkpoint, production, relies on | `name`, `meaning`, `form` (`host_change`, `file`, `message`, `workflow_input`, `human_act_standing`), `destination`, `promised_standing`, `gating_checkpoint`, and for production `produced_by` (host change), `path` (file) or `designating_line` (message), required for its form (a file output without `path` is not established, VO-5); `relies_on` |
| returned evidence (§4.5) | `name`, `meaning`, `kind`, `supports` |
| compatible roles, tool restriction (§4.7) | `compatible_roles`, `tool_restriction` (`capabilities`) |

- **Values owned elsewhere.** `required_act` uses DEL-04-01's canonical codes
  (A4, A5, A6, A7, A12). `operation` and `versions` carry DEL-03-01's
  operation identity and version as C writes them (C §3 element 1, §3.2;
  opaque here). `outcome` carries P §9's outcome names as tokens: `queued`,
  `accepted`, `rejected`, `withdrawn`, `applied` (P §9 *applied (receipt)*),
  `refused_invalid`, `refused_stale`, `application_error`. **WD follows the
  outcome owner:** each token is the value P-v0.8 writes for that outcome in
  `proposal_state.schema.json` (`$defs/item_state`), and where P's schema
  writes an outcome differently, WD's text, schema and fixtures change
  together to P's spelling (R14-6; V18-2 M-2; until the RP-3 repair WD wrote
  `applied_receipt`, which P's schema does not offer). Whether a kind (c)
  checkpoint may name P's further states *applied, then reversed* or
  *outcome unknown* is not stated at v0.8; the enum excludes them.
- **Spellings across the design set (V18-2 m-5; PROPOSED).** The tokens of
  `workflow-declaration.schema.json` are the canonical spellings of the
  declared part. A consumer schema that spells a member otherwise states its
  mapping to these members; every mapping known at this repair is one to
  one (V18-2 ran WD's declarations through EXEC's checker with it):

  | Element | WD token | EXEC-v0.6 spelling (both schemas) | RS |
  |---|---|---|---|
  | reached-when kind | `before_dispatch`, `output_produced`, `host_outcome` | `a`, `b`, `c` | words of §4.3.1 |
  | capturing surface | `host_act_facility`, `app_act_control`, `grant_control` | `host_act_facility`, `app_interface`, `control_surface` | words |
  | subject class | `change_items_of_named_proposal`, `named_output`, `objects_named_output_concerns`, `objects_changed_by_named_outcome`, `targets_of_held_call`, `grant_setting` | the §4.3.1 words, spaced | words |
  | disposition (§4.3.4) | not a declared-part member | the §4.3.4 words, spaced ("not reached"), which RS's entry kinds share (R14-1) | the same words |
  | workflow identity (§6.1) | `$defs/workflow_identity` | `identity` (derived-from a string) | camelCase (`sourceRoot`) |

  A reference to a required tool is by its **tool local name** (§4.2.2); a
  consumer that reports per reference needs that name as well as the
  operation identity, since two references may name one operation.
- **Workflow identity (V18-2 m-9; PROPOSED).** The schema's
  `$defs/workflow_identity` writes the §6.1 tuple, with `derived_from` as a
  nested tuple, never a string. It is not a member of the declared part; a
  consumer schema that carries a workflow identity references it or states
  its mapping to it. Origin is one of `project`, `user`, `bundled`, `host`
  (S-D); "host-supplied" is not a value.
- **Human-act standing.** §4.4's sentence that a human-act standing "can only
  be promised conditional on a named checkpoint" is carried as the output
  form `human_act_standing`, which requires `gating_checkpoint` (E1
  `checked-rows`). The standing is produced by the person's act, never by
  the agent.

### 3.7 Reading order and names (PROPOSED at v0.8; S1-C WD 9)

Every consumer reads a declared part in this order (VO-1…VO-10). All steps
run and every finding is reported. An element's **reading** is
*recognized*, *invalid* (with its FB code) or *not established* (with its FB
code or §3.4), and it is set by the first step that fails it, in the order
VO-5, VO-6, VO-7, VO-8. An element that is invalid or not established
creates no arrival and is never evaluated (EXEC §4.14); the other elements
of its category are read.

| Step | What is read | Failure → reading |
|---|---|---|
| **VO-1 Locate** | The block (CR-1…CR-4) | None → **undeclared** (FB-01). Several → declared part not established (FB-02) |
| **VO-2 Parse** | JSON text | Not JSON, or any object with a duplicate member name → declared part not established (FB-02). JSON parsers differ on duplicate names, so the reader must detect them rather than take the last |
| **VO-3 Envelope and version** | Top-level object; `declaration_contract_version` | Not an object, or no string version → FB-02. A version the reader does not know → preserved, reported, declared part **not established** (§3.3) |
| **VO-4 Categories** | Each of the five members | Omitted → **undeclared**. `[]` → **declared empty**. Not an array → that category not established (FB-02). An unrecognized top-level member → preserved and reported; no category changes (§3.4) |
| **VO-5 Elements** | Each element against its schema definition | Name missing or ill-formed → not established (FB-02). Checkpoint `required_act`: a recognized act kind outside the closed list, or none → **invalid** (FB-03); an unrecognized name → not established (FB-04). Checkpoint `reached_when` absent → **invalid** (FB-13). A file output without `path`, like a message output without its designating line, fails its shape → not established (FB-02), so a checkpoint whose reached-when or subject names it is not established at VO-7, never recognized (V18-2 m-2). An unrecognized member or value → not established, preserved (§3.4). Any other shape failure → not established (FB-02). **Exceptions:** `governed` or `fresh_act_required` with an unrecognized value → FB-19, and the checkpoint is otherwise read; `held_actions` malformed → the checkpoint is read and its held actions do not show host operations only, so the governance-phase conservative default applies (R10-10; no failure row) |
| **VO-6 Names** | DN-1…DN-4 below | FB-20 |
| **VO-7 References** | Each name an element uses | A checkpoint's `reached_when` or `subject` naming an undeclared element → **invalid** (FB-13); naming an element that is itself not established → the checkpoint is **not established** (§3.4). Naming the wrong kind of element → **invalid** (FB-13): a `host_outcome` kind or an "objects changed by a named outcome" subject naming a harness capability; kind (b) on a host-change output without `produced_by`, or on a workflow-input or human-act-standing output; "objects a named output concerns" on an output without `relies_on`. Any other reference (an input's `read_through`, an output's `gating_checkpoint`, `produced_by` or `relies_on`, evidence `supports`) naming an undeclared or unusable element, or evidence `supports` naming both an output and a checkpoint → that element not established (FB-21). `held_actions` of form host operations only naming anything other than a declared host operation → the governance-phase conservative default (R10-10) |
| **VO-8 Combinations** | §4.3.1 validity rules; §4.4 labels | FB-16 (A5; held-call targets with a kind other than (a)); FB-17 (A12 without setting content; a grant-setting subject on another act); FB-10 (promised standing) |
| **VO-9 Flags and notes** | `governed`, `fresh_act_required`; anchors | `fresh_act_required` without `governed` → shown, with a note (FA-3). A7 with an actor other than the accountable professional → a note (§4.3.1 actor requirement). A stage or position that is not a prose heading → a note (information only; FB-07 is not applied automatically) |
| **VO-10 Root companion** | A Root `execution.json` in the package | Required tools undeclared while a restriction is present → FB-05. Declared `compatible_roles` differing from `execution.json`'s → FB-22 |

**Names.**

- **DN-1** A local name is unique within its category. The same name may be
  used in different categories, because every reference says which category
  it names.
- **DN-2** Two or more elements with one name in one category are all
  reported (FB-20). Checkpoints so named are **invalid**; other elements are
  **not established**.
- **DN-3** A reference to a duplicated name is a reference to an element that
  is not established (VO-7).
- **DN-4** Designating lines are unique among a workflow's message outputs
  (§4.4 OP-5). Outputs that share one are not established (FB-20).

### 3.8 Reading states and re-reads (R12-1)

This contract owns no run-time state: the checkpoint hold and recording
machine is DEL-02-03's (EXEC §4), and the run record is DEL-04-03's. A
reading is a function of two things: the bytes of the package revision read,
and the contract versions the reader knows. Two readers that follow §3.5 and
§3.7 give the same reading; the prototype's two extractors agree on E1
(§13.1).

| From | Event | To | Record left |
|---|---|---|---|
| not read | A consumer reads the resolved revision (EXEC CK-1…CK-4; the host loop; the panel) | read: *declared* with element readings, *undeclared*, or *not established* | The consumer's report cites the revision and the contract version (EXEC CR-2, CR-3, CR-7, CR-9) |
| read | The same revision is read again by a reader of the same version | the same reading | None new |
| read | A new revision is selected (C-3) | a new reading of the new revision | A new report; the earlier one is kept, never relabelled (EXEC §3.1) |
| read: *not established* (version) | The reader is upgraded to know that version | a new reading | A new report; the earlier one is kept |
| read | Recovery or replay of a run | the reading of the revision recorded for the run, never the library's current content (EXEC RP-5) | If those bytes cannot be resolved: "declaration not resolvable — reconstruction not verified" (EXEC RP-5) |

### 3.9 Operating sequence: from package to run (R12-1)

| Step | What happens | Who | Fails when | Reported by; record | Then |
|---|---|---|---|---|---|
| OS-1 Author | `WORKFLOW.md` is written with its prose and block | The person, with an agent; App drafts are DEL-02-02's (later) | The block is not valid against the schema | The author's tooling, if any (not defined here) | Registration |
| OS-2 Register | The draft becomes a revision with an identity tuple (§6.1); registration is a recorded human act, A15 (R12-5; ACT, PROPOSED) | DEL-02-02 (later); a host library for host workflows | The package holds a non-regular entry: revision not established (RV-2) | DEL-02-02 | Listing |
| OS-3 Select | The person selects a full identity tuple (C-2) | The person; DEL-02-02; the panel | A collision (FB-09) | Discovery; selection record | Resolve |
| OS-4 Resolve | The revision's bytes are resolved | The resolver (placement open, §9) | Not resolvable (FB-08) | The consumer; the record keeps the selected tuple | Stop |
| OS-5 Read | VO-1…VO-10 | Each consumer, or a shared reader (placement open, OI-014) | FB-01, FB-02, FB-03, FB-04, FB-13, FB-16, FB-17, FB-19…FB-22; §3.4 | The consumer's report | The readings go on to the check and the run |
| OS-6 Check | The required-tool check (EXEC §3) | DEL-02-03 (App); the host | Outcomes of §4.2.4 | The compatibility report | The person decides whether to run |
| OS-7 Supply | The agent is given `WORKFLOW.md` (prose and block together) with its role guidance | App: DEL-02-04 and HOSTING §8.2; host: the host loop | The supplied bytes differ from the resolved revision: "revision not verified" (HL-3) | The supplied-guidance record (HOSTING §8.2; RS) | Run |
| OS-8 Run | The agent follows the method and asks the person for each checkpoint's act when its work reaches the checkpoint (DECISION-K1 K1-1) | The agent; the person | — | — | — |
| OS-9 Observe | Arrivals, productions (§4.4), acts, lapses | DEL-02-03 (App); DEL-05-01 (host) | An observation is lost: *unknown* | The run record (DEL-04-03) | Recovery (EXEC §4.12) |
| OS-10 Carry | Transfer to a host with the carriage manifest, which summarizes the block and never overrides it (EXEC TR-4) | DEL-02-03; the person | The host cannot read the contract version (EXEC TF-4) | The transfer record | Host listing |

---

## 4. Declared-part meaning

### 4.1 Expected inputs (SOW-042)

| Element | Meaning |
|---|---|
| **input name** | Local name, unique within the workflow. |
| **input meaning** | What the input is and why the method needs it. |
| **input kind** | One of: a host object or view obtained through a catalog read (see **required tool reference**); a file or document supplied to the run; a value or choice supplied by the person; an output of another identified workflow run. |
| **input source** (v0.8; PROPOSED) | For a host read: the required tool reference it is read through, by its local name (§4.2.2). For an output of another workflow run: that workflow's identity (origin, source root, name, and optionally revision; §6.1) and the output's local name in it; which run supplied it, and on what basis, is an observation (§4.6). For a file: nothing is declared beyond the meaning; the file and its content identity are recorded when it is supplied (DEL-04-03). |
| **necessity** | Required, or optional with the effect of its absence stated. |
| **quality or basis requirement** | What must hold for the input to be usable. For a host read, the relied-on basis is DEL-03-01's read-basis descriptor (C §5.1): workspace identity, generation, model revision, canonical content identity, and the **identity method designation** of that content identity. Generation is a host lineage epoch; an intervening edit changes the model revision, not the generation. A read lacking any element is *basis incomplete* and cannot be cited as relied-on (C §5.2). Per-row **subject content identities** (C §5.3) come with the read. |
| **stage** | Where in the method the input is needed, anchored to the prose. |

An expected input is a need, not a fetched value. Whether and on what basis it
was supplied is an observation (§4.6).

### 4.2 Required tools (SOW-043, SOW-039)

#### 4.2.1 Two tool classes

| Class | What it refers to | Supplier of meaning |
|---|---|---|
| **host operation requirement** | An operation in a host's capability catalog, referenced by its operation identity. | DEL-03-01 catalog C (V4-HI-02; C §3). The reference is **opaque** here. |
| **harness capability requirement** | A capability of the agent's harness that is not a host catalog operation (e.g., file writing or native delegation in the App's Codex). | Supplied through DEL-01-01 (SoW REQ-002, CLM-002; DEP-02-01-025, arc N-16): its harness capability inventory (HOSTING §8, closing paragraph, which points to PIN-SPIKE §4) and, from HOSTING-BOUNDARY-v0.8, its capability account by group, HCG-A01…A17 (HOSTING §8.4), which gives each group's meaning, availability signals and standing. HOSTING supplies the meaning and chooses no names. The portable names are PROPOSED here at v0.8, scoped to Codex pin 0.158.0, and each resolves to one HOSTING §8.4 group (§4.2.5 HC-7; R14-5; U-08). |

A workflow designed for a host names host operations. An external agent (the
App's Codex through a host's MCP or CLI surface, V4-HI-50) reaches the same
catalog operations, and the declaration still references the catalog
identity, never an adapter-specific tool name.

**Note (R8-10; SQ-12, SQ-18 (e)).** SWBPIPE has no capability catalog with
per-operation identity or version. Against it, host operation requirement
references cannot resolve, so the check reports them **not established**
(EXEC EV-4). This records SWBPIPE's current state and changes no rule here.

#### 4.2.2 Elements of a required tool reference

| Element | Meaning |
|---|---|
| **tool local name** (v0.8; PROPOSED) | Local name, unique among the workflow's required tool references (§3.7 DN-1). Checkpoints, inputs, outputs and held actions refer to the tool by it. |
| **tool reference** | Opaque reference to a DEL-03-01 operation identity (host class) or to a harness capability, by its name (§4.2.5). |
| **version compatibility** | Optional. Only an exact version (or set of exact versions) can be stated, because C defines version equality only (C §3 #1, §3.2; U-07). |
| **purpose of use** | Readable: what the method uses the operation for. It does **not** restate the operation's class or treatment. Those come from the catalog entry's class element (five values incl. *no policy basis* with its reason, per R2-1), adopted policy (DEL-04-01) and the person's grant (V4-HI-40). |
| **necessity** | Required, or optional with a stated fallback or limitation. |
| **stage** | Where in the method the tool is used. |
| **governing checkpoint constraint** (derived, not authored) | If a checkpoint in the workflow requires A5 on this operation's result, every change request for this operation in the run is accompanied by the constraint {workflow run, checkpoint name, required act A5, operation} (R2-12; P §3.3), recorded with its **carriage assurance** (R4-14, final per R5-2): *host-held* (the host holds the constraint on its side, having derived it from, or verified it against, its own resolved copy of the declaration; the host loop's own evaluation is host-held), *App-assured* (App code attaches it — **not available in this increment**, since interposed App code is not adopted, R4-2), *model-supplied* (present only because the model put it in the call) or *absent*. A constraint the host merely received from an outside caller keeps its source's assurance. **Only host-held carriage satisfies R2-12.** The host route resolves treatment *propose*. The declaration does not state a treatment; the constraint is derived from its checkpoint so any carrier can compute it. Which assurance a host can give is relay question SQ-02 (U-19). SWBPIPE answered route (iv), none: an extra constraint field would be refused as unknown (SQ-02 (a)). **Phase (R8-1):** carriage assurance is governance phase and applies to a **governed** A5 checkpoint. In Phase 1 the App carries and enforces no constraint; the agent follows I-7 as plan guidance. **Strict preflight (R8-10):** the agent never adds a field the host's schema lacks. Where the host defines no such element, the expected constraint is recorded App-side with the evidence limit "constraint not carriable on this host". |

#### 4.2.3 Requirement is not restriction

Root `execution.json` `tools.capabilities` and `tools.commands` are
**restrictions**: a ceiling that intersects outer policy ("empty restriction
lists deny rather than grant"; AGENT_WORKFLOW_RUNTIME.md). V4-WF-01 "the host
tools it needs" is a **requirement**: a floor the current host must meet.
These shall remain distinct. A consumer shall not read one as the other
(FB-05; EXAMPLES E6).

#### 4.2.4 Compatibility outcomes and pass rule (meaning only)

The check itself is DEL-02-03's (its REQ-001). This contract supplies the
vocabulary and the pass rule. Runtime non-success results *unavailable*,
*not permitted*, *channel not enabled*, *not exposed on this surface* and
*error* are C §4.1's, used unchanged.

| Outcome | Level | Meaning |
|---|---|---|
| **present** | per requirement | The operation exists in the current host's catalog edition and element 9 says *exposed* on the acting surface. |
| **missing** | per requirement | No entry in the current catalog edition. A discovery finding (C §4.1), reported with the requirement's purpose line (S-E). |
| **not exposed on this surface** | per requirement | Entry exists; element 9 says *not exposed on this surface* for the acting surface. |
| **channel not enabled** | per surface | The surface itself is off (external access not enabled; A13 not performed). Reported by the App when its own configuration is off, by the host when the host channel is off (R4-16). App-side configuration an agent could write is never A13 evidence (R4-13). Never encoded as missing or unavailable. |
| **version mismatch** | per requirement | Present, but not at a declared compatible version. |
| **present, currently unavailable** | per requirement, at run time | Present, but a precondition does not hold now; reported with the catalog's unavailable reason (V4-HI-04; C §4.2). A run-time hold, not a missing requirement. |
| **not established** | per requirement | Cannot be evaluated: undeclared, unrecognized element, catalog unreadable, reference unresolved, or element 9 value *unagreed*. Never reported as present. |
| **unsupported** | per workflow | With a stated reason: the workflow's compatible roles or delegation need cannot be met by the acting seat (§4.7, §5.3); or **"checkpoint hold not enforceable on this surface"**, naming the checkpoint, when its hold support on the acting surface is *not enforceable* (§4.3.8; R4-8). **The hold reason applies only to a checkpoint declared `governed`, in the governance phase** (§4.3.0, §4.3.1; R8-1). In Phase 1 it is never reported. |

**Pass rule (IR1C-13).** The requirement check **passes** when every
reference whose necessity is *required* is **present** or **present,
currently unavailable**, and the workflow is not **unsupported**. **Governance
phase only:** also, no governed checkpoint's hold support on the acting surface
is *not established*, which makes the check *not established*, never a pass
(§4.3.8, R5-1). **Phase 1:** no checkpoint enters the pass rule, and the
result depends on the required tools and the channel state, with the role and
delegation reasons above (R8-2; §4.3.0). A *present,
currently unavailable* requirement is shown as a run-time hold with its
reason. Optional references never block a pass; their outcomes are shown. Any
required reference *missing*, *not exposed on this surface*, *version
mismatch*, *not established*, or on a surface whose channel is not enabled,
means the check does **not** pass. In EXEC §3.5's three check results, a
required reference that is *not established*, with no other blocking
condition, gives the result *not established* (never a pass, never
*unsupported*); the other conditions give *does not pass* (R5-1; R8-11
item 3). An undeclared workflow stays selectable and
is shown "requirements undeclared — check not established", never "runnable".

**Reporting rules (R2-4).** Reserved entries are always offered; a class
reason never makes an entry *not exposed*. At run time *not exposed on this
surface* is reported by the host from element 9; an operation absent from the
catalog edition the loop offered is the loop's *not offered* failure (never
dispatched). The discovery-time check above reads element 9 directly.

Whether a newly added operation becomes available on all three surfaces
without separate work is `UNRESOLVED{OI-003}` (App v4 OI-003, the extension
promise; unrelated to SWBPIPE's OI-003); the declaration never assumes it
(U-16).

#### 4.2.5 Harness capability names (PROPOSED at v0.8; scoped to Codex pin 0.158.0; U-08)

DEL-01-01 supplies the inventory (HOSTING §8; PIN-SPIKE §4) and the
capability meaning, as an account by capability group (HOSTING §8.4), and
chooses no names; DEL-02-01 names the capabilities (SoW REQ-002, CLM-002;
DEP-02-01-025). Each name below is a portable meaning. The third column is
the evidence at pin 0.158.0 for what the name covers in the App's Codex,
read from the committed generated schema (`ThreadItem` item kinds, server
requests) and PIN-SPIKE §4 (experimental-only fields). Every item kind cited
is in the stable generator output as well as the experimental one (header,
v0.8 inputs). The last column (added by the RP-3 repair; R14-5) names the
HOSTING §8.4 group the name resolves to at the pin, and the members of that
group the name does not itself rely on; HOSTING owns the grouping (HC-7).

| Name | Meaning (what the method needs the harness to do) | Basis at 0.158.0 | Standing at the pin | HOSTING §8.4 group at 0.158.0 (R14-5) |
|---|---|---|---|---|
| `shell-command` | Run a command in a shell in the workspace | Item kind `commandExecution`; server requests `item/commandExecution/requestApproval` and the legacy `execCommandApproval` | Stable | **HCG-A02**. Also in the group, not relied on by the name: the client method `thread/shellCommand`, which the App calls (its items carry source `userShell`, and the generated description says it runs unsandboxed), the experimental `thread/backgroundTerminals/list`, `thread/backgroundTerminals/clean`, `thread/backgroundTerminals/terminate`, and the notifications `item/commandExecution/outputDelta`, `item/commandExecution/terminalInteraction` |
| `file-change` | Create, edit, move or delete files in the workspace | Item kind `fileChange`; server requests `item/fileChange/requestApproval` and the legacy `applyPatchApproval` | Stable | **HCG-A03**. Also in the group: the notifications `turn/diff/updated`, `item/fileChange/outputDelta`, `item/fileChange/patchUpdated` |
| `web-search` | Search the web or open a web page | Item kind `webSearch` (actions search, open page, find in page) | Stable | **HCG-A10**. The generated `WebSearchAction` also has `other`, beside the three actions named |
| `agent-delegation` | Start, instruct, wait for and close subordinate agents | Item kinds `collabAgentToolCall` (tools `spawnAgent`, `sendInput`, `resumeAgent`, `wait`, `closeAgent`, `sendMessage`, `followupTask`, `interruptAgent`, `listAgents`) and `subAgentActivity` | Item kinds stable; `multiAgentMode` on thread and turn start is experimental-only (PIN-SPIKE §4) | **HCG-A08**. The nine tool values named equal the generated `CollabAgentTool` enum |
| `mcp-tool-call` | Call a tool of an MCP server configured in the harness | Item kind `mcpToolCall` | Stable | **HCG-A05**. Also in the group, not relied on by the name: MCP resources (`mcpServer/resource/read`) and the client methods the App calls (`mcpServer/tool/call`, `mcpServer/oauth/login`, `config/mcpServer/reload`, `mcpServerStatus/list`, the experimental event stream). **Observed at the pin (R13-6; HOSTING §10.1):** on the local route of OBS-1 (a Responses provider, LM Studio 0.4.16) Codex offered the MCP tools as one `namespace` tool, which the server dropped, so no MCP tool reached the model. On that route at this pin the name is not served; this is a limit of that route, not of MCP generally |
| `dynamic-tool-call` | Call a tool the client supplies to the thread | Item kind `dynamicToolCall`; server request `item/tool/call` | Item kind stable; supplying tools (`dynamicTools` on thread start) is experimental-only (PIN-SPIKE §4) | **HCG-A06**, including the item kind `functionCallOutput` (the output item of such a call; not named on its own, HC-6) |
| `person-input-request` | Ask the person a structured question during a turn | Server request `item/tool/requestUserInput` | Stable. An answer is never act evidence (I-5; EXEC CAP-6) | **HCG-A07**, including the server request `mcpServer/elicitation/request` (an MCP server's elicitation relayed to the person; its prompt is authored by an MCP server or the agent, HOSTING §6.1) and the experimental `thread/increment_elicitation`, `thread/decrement_elicitation`. No answer in the group is act evidence (I-5) |
| `image-view` | Look at a local image | Item kind `imageView` | Stable | **HCG-A11**, shared with `image-generation`. The group's availability signal (`imageGeneration` of the provider capabilities) bears on `image-generation` only |
| `image-generation` | Generate an image | Item kind `imageGeneration` | Stable | **HCG-A11**, shared with `image-view` |
| `plan-update` | Keep a visible plan of the work | Item kind `plan`; notification `turn/plan/updated` | Stable; plan mode (`collaborationMode`) is experimental-only (PIN-SPIKE §4) | **HCG-A09**. Also in the group: `item/plan/delta` and the experimental `collaborationMode/list` |

- **HC-1 Portable, pin-scoped evidence.** The names are the requirement's
  meaning. The basis column holds only at pin 0.158.0. Another pin, or
  another harness, is mapped to the same names in its own supplier account
  (HOSTING's, for the App's Codex); no mapping is assumed.
- **HC-2 Host operations are not harness capabilities.** A host operation
  reached through an MCP server or a command-line tool is a host operation
  requirement (§4.2.1) and is never declared as `mcp-tool-call`.
- **HC-3 Delegation.** A workflow that needs delegation declares a required
  `agent-delegation` capability (§4.7).
- **HC-4 Presence.** Whether a capability is *present* for a check is
  decided by DEL-02-03's check (EXEC EV-3) from the acting harness's supplier
  account (HOSTING §8.4), through the name-to-group mapping of HC-7 (R14-5).
  Until EXEC states that rule, a harness capability reference stays **not
  established** in the check, never *missing* (joins, §8). An observed limit
  of a route (the `mcp-tool-call` row) is a fact that rule reads; it changes
  no name.
- **HC-5 Unrecognized names.** A name not in this table is **not
  established** (§3.4); nothing is guessed from its spelling.
- **HC-6 Not named.** Item kinds that are not capabilities a method
  requires are not named: `agentMessage`, `userMessage`, `reasoning`
  (HCG-A01), `hookPrompt` (A15), `sleep` (A14), the review-mode items (A12)
  and `contextCompaction` (A13). Two members this rule listed until the RP-3
  repair now follow HOSTING's grouping (R14-5): `functionCallOutput` is the
  output item of a call in HCG-A06, reached through `dynamic-tool-call`, and
  is not named on its own; an MCP server's elicitation
  (`mcpServer/elicitation/request`) is in HCG-A07, reached through
  `person-input-request`, and its prompt is authored by an MCP server or the
  agent (HOSTING §6.1, wording followed; V18-2 m-12). Either way an answer
  to it is never act evidence (I-5). Client methods the App itself calls (for
  example `thread/shellCommand`, `command/exec`, `fs/*`) are the App's
  actions, not the agent's capabilities, whichever group HOSTING places them
  in (HC-7).
- **HC-7 Group mapping (R14-5; PROPOSED; closes the join of V18-2 M-1).**
  Each name resolves at pin 0.158.0 to exactly one HOSTING §8.4 Part A group,
  as the last column states; two names may share a group (`image-view`,
  `image-generation`). HOSTING owns the supplier facts and the grouping:
  where a group holds members a name does not rely on, they stay in the
  group and are listed beside the name, and none of them gives the name a
  meaning the group does not offer, so no member is returned (the three
  checked by name: `functionCallOutput`, `mcpServer/elicitation/request`,
  `thread/shellCommand`). A client method in a Part A group is a call the
  App makes (HOSTING §5 records its initiator) and does not by itself show
  the agent's capability. Groups no name reaches: HCG-A01, A12, A13, A15
  (HC-6), and A04 (permission requests, A14 subjects), A14 (waiting and the
  experimental clock request), A16 (memory) and A17 (realtime voice), which
  a workflow cannot require in this increment. At another pin the mapping
  is re-checked with HOSTING's §9.5 upgrade comparison. The prototype checks
  every supplier name cited in the table against HOSTING §8.4 (§13.1, S-11).

### 4.3 Checkpoints requiring human acts (SOW-044; REQ-003)

#### 4.3.0 Phase 1: checkpoint declarations are plan guidance (R8-1; DECISION-4 D4-1)

The phasing is SETTLED by DECISION-4 D4-1 and its clarification, and is now
stated by the accepted basis: PRD V4-WF-05 and HOST_INTEGRATION V4-HI-42 as
amended by SCA-V4-001, quoted below, with SoW REQ-003 and TBD-004 (R9-1). The
framing of CG-1…CG-7 is INTEGRATION (R8-1). The execution side is EXEC-v0.5
§2.1 (PH-1…PH-10) and §2.2 (GV-1…GV-5); this contract consumes DEL-02-03's
statement of the current phase and does not define it (SoW TBD-004;
DEP-02-01-026). Rules CG-1…CG-7 state the declaration side.

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

**In force in every phase (R9-1):** the act is requested; it is recorded as
done only when the person performs it; the reserved acts bind. **Phased to
the governance layer:** holding the run until the act.

- **CG-1 Guidance.** In Phase 1 (this increment) a declared checkpoint is
  **plan guidance**. It tells the person and the agent where the method
  expects a human act, which act, on what subject, for what purpose, and what
  should not happen before it. The person and the agent work out the plan
  around it, and the agents manage any pause, hold point or gate themselves.
- **CG-2 Fields kept.** Every §4.3.1 element stays, including required act,
  reached-when, subject class, scope, purpose, actor, negative and mixed
  paths, expected act evidence and held actions, and so do the validity rules.
  Not every workflow will have governance, but every workflow that needs it
  must be serveable by what is built. The governance phase consumes these
  fields, so they are declared now.
- **CG-3 No enforcement.** Neither the App nor a host's embedded loop
  enforces a hold, blocks a run, or re-holds a run at a checkpoint (EXEC
  PH-2). A checkpoint never makes a workflow *unsupported* in Phase 1. No
  checkpoint enters the requirement-check result, which depends on the
  required tools and the channel state (§4.2.4; R8-2).
- **CG-4 Acts only when performed.** A human act is recorded as done only
  when the person performs it, with capturing-surface evidence (I-1, I-2,
  I-5, I-8). An agent never records a human act on the person's behalf
  (the record clause of V4-WF-05 and V4-HI-42 as amended, in force in every
  phase; EXEC PH-4).
- **CG-5 Reserved acts stand.** Every act a checkpoint may require remains
  reserved to the person (S-Q; §4.3.2), and a host enforces its own list
  through its operations (V4-HI-30). The phasing removes no host refusal.
- **CG-6 Recording is observation.** A checkpoint's arrival and the act that
  answers it are recorded where the arrival is observed (R9-1: recording is
  required there, not optional), with the act-declined, act-lapsed and
  run-ended events, so the person and the agent can see where the plan paused
  and what was done. Recording is observation, not enforcement; how an App
  run observes an arrival is EXEC's to define (Wave B). The dispositions of
  §4.3.4 may label that record (EXEC PH-6; confirmed INTEGRATION by R8-11
  item 1): *waiting* then means "reached; act not yet recorded", never
  "the run is held". *Action during hold* is not a violation marker. A run
  action after an arrival and before its act may carry the optional
  annotation **"continued past ‹checkpoint› before ‹act›"**. A performed
  act's lapse is still recorded, and nothing re-holds (I-4; EXEC PH-8;
  confirmed INTEGRATION by R8-11 item 1).
- **CG-7 Governance phase (retained).** A later layer, per workflow that needs
  it, enforces checkpoints declared **`governed`** (§4.3.1). §4.3.8 (hold
  support), I-4's re-hold branch, I-7's constraint carriage, I-9, RW-2's held
  call and FB-13, FB-14 and FB-18 are its definition. They are **retained and
  relabelled, not deleted**. Holding the run at the checkpoint until the act
  is performed is **phased to the governance layer, not withdrawn** (V4-WF-05
  as amended; U-33 closed).

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
  then holds, is defined in EXEC in Wave B. This contract states the ruling
  and points there.

#### 4.3.1 Elements

| Element | Meaning |
|---|---|
| **checkpoint name** | Stable within the workflow's revision; identifies the checkpoint across interruption, replay and adaptation (DEL-02-03 REQ-002). |
| **required act kind** | Exactly one of the closed list **A4 mark checked**, **A5 accept**, **A6 approve**, **A7 rely**, **A12 set grant** (R-1; DEL-04-01 §4.1). *Approve* is engineering approval only (V4-HI-30/33); design-candidate approval (V4-CON-05, V4-HI-65) is a separate later-increment act and cannot be required here. |
| **reached-when** | The observable arrival condition, of one of three kinds: (a) before dispatch of a named **required tool reference**; (b) on observed production of a named **declared output** (as the output's production element says, §4.4; for a message, its designating line); (c) on an observed host outcome of a named operation (e.g., *queued*). Meaning only; the loop evaluates it in hosts (DEL-05-01), DEL-02-03 in the App. Phase 1: the arrival is recorded where it is observed (R9-1). Governance phase: it is also held (§4.3.8). |
| **subject class** | Its own element, independent of the reached-when kind (R2-17). Exactly one of: **change items of a named proposal**; **named output**; **objects a named output concerns** (R3-1); **objects changed by a named outcome**; **targets of the held call**; **grant setting**. Bound at run time (§4.3.6). Consumers bind the *declared* class and never infer it from the reached-when kind. |
| **position** | Where in the method the checkpoint sits, anchored to the prose. Explanation only; arrival is decided by **reached-when**. |
| **scope** | The extent of the subject covered, e.g., one item, several items or a whole proposal (V4-HI-41; acceptance unit = change item, R-6). Carried with every act request at the checkpoint and bound with the act (V4-REC-05; IR1C-14). |
| **purpose** | Why the act is requested here, in words the person reads when asked. Carried with every act request and bound with the act (V4-REC-05; IR1C-14). |
| **actor requirement** | "The person" by default; "the accountable professional" for A7 (V4-AUT-05). A class, never an identity. |
| **on negative decision** | What the method does after *resolved negatively* (A10 for A5; an act-declined event for A4, A6, A7, A12): stop, return to a named stage, or proceed on a stated branch. Absent this element (R10-7): in the current phase the agent follows the plan it worked out with the person; in the governance phase, for a governed checkpoint, the run stops at the checkpoint. In both phases the run is never recorded as if the act were positive. |
| **on mixed decision** (A5 only, optional) | What the method does when some items have A5 and some A10 (§4.3.7). Absent, the mixed case follows **on negative decision** for the rejected items; accepted items proceed through the host lifecycle. |
| **expected act evidence** | The act record expected (DEL-04-03 human-act record meaning), with its capturing surface and capture-evidence reference (I-5). A declaration, not a record. |
| **held actions** | What the run must not do until the act (INTEGRATION, R6-1; EXEC F-28). Either **"host operations only"**, naming them (e.g., the governed operation of an A5 constraint; the held call of a kind (a) checkpoint; named host operations after arrival until the act), or the **listed steps**, marking each App-side step (an App agent turn such as Return, an App tool or harness action, an App file write, an action on App content). **Derivation when absent (INTEGRATION, R7-3; EXEC §3.6):** for an **A5** checkpoint the held actions are the governed operation(s); for a **kind (a)** checkpoint they are the held call. **Conservative default (governance phase only):** consumers assume at least one App-side step (EXEC HS-5) when a kind (b)/(c) checkpoint has no held-actions element (an A5 checkpoint takes the derivation above, per EXEC §3.6's definition), and when any **declared** held-actions element does not show host operations only, whatever the checkpoint kind (R10-10; no new failure row). In Phase 1 it is guidance: what the agent's plan should not do before the act. In the governance phase it decides hold support (§4.3.8). |
| **governed** (optional; PROPOSED, R8-1) | Whether the checkpoint opts in to the **governance phase**. Values: **yes**, or absent (not governed). **Phase 1:** honoured only as guidance. The flag is shown with the checkpoint, and §4.3.0 applies unchanged: no hold, no hold-support value, no *unsupported* for a hold reason (EXEC PH-9). **Governance phase:** a governed checkpoint is held on the acting surface according to its hold-support value (§4.3.8; EXEC §3.6). That value enters the requirement check, and the *unsupported* reason "checkpoint hold not enforceable on this surface" can apply (§4.2.4; R4-8). A checkpoint without the flag stays plan guidance in every phase. A workflow that declares a checkpoint governed must declare every element the governance phase consumes, or rely on the stated derivations (held actions). An unrecognized value is preserved and reported (FB-19). Representation: `"governed": "yes"` (§3.6) |
| **on subject absent** (optional; v0.8; PROPOSED; U-32 decided) | What the method does when a bound referent no longer exists (EXEC §4.7 "Subject absent"): stop, return to a named stage, or proceed on a stated branch. It changes no disposition: the arrival stays *waiting* "subject absent", closed only by an act-declined event or run end (EXEC CH-24). Current phase: guidance for the agent's plan. Governance phase, governed checkpoint: the arrival stays as EXEC defines it, and the path says what the method does once the person has declined. Absent: EXEC's default applies unchanged |
| **fresh act required** (optional; v0.8; PROPOSED; R12-10, EXEC SP-6F) | Whether the checkpoint takes up the governance-phase option of I-8. Values: **yes**, or absent. **FA-1** It takes effect only for a checkpoint also declared `governed`, in the governance phase: EXEC SP-6F then applies to its arrivals (an earlier act is shown "prior act not counted — captured before arrival (governance-phase option)"; where the order cannot be established, "act order unknown"). **FA-2** Current phase: shown with the checkpoint, and guidance to the agent that the method wants a fresh act; the record applies SP-6, so an earlier act of the required kind on current content counts and is cited with its time (DECISION-K1 K1-2). **FA-3** Declared without `governed`: shown, with a note that it has no effect in any phase. **FA-4** An unrecognized value is preserved and reported (FB-19). **FA-5** For A5 at kind (c) *queued* the order question never arises (EXEC §4.5) |

**Validity rules for combinations.**

| Combination | Rule |
|---|---|
| A5 | Reached-when **must** be kind (c) naming host outcome *queued* for the operation(s) whose result the checkpoint concerns, and subject class **must** be "change items of the named proposal" (that queued proposal). Any other A5 combination is invalid (FB-16) (R2-17). |
| targets of the held call | Valid only with reached-when kind (a) *before dispatch*; the held call is the one kind (a) held (INTEGRATION, R3-2; from IR1-C X-10). |
| objects changed by a named outcome | The named outcome must be an operation the workflow declares; bound when the applied outcome is observed (R2-14). |
| named output | The output must be declared in §4.4. With reached-when kind (b) on it, the output must have an observable production (§4.4): not a workflow-input or human-act-standing output, and a host-change output must name its production (FB-13). |
| objects a named output concerns | The output must be declared in §4.4 and be a read or examination output that identifies objects (e.g., an OP-C3 findings output naming rows). Typically paired with reached-when kind (b) on that output (INTEGRATION, R3-1). At v0.8 the output shows this by naming the reads or examinations it **relies on** (§4.4); without them the checkpoint is invalid (FB-13). |
| grant setting | For A12. The declaration **must always** name the setting content (classes, grant values, scope), and the **declared** content always binds. An A8 may present that content to the person but never changes the subject; an A12 made on different content satisfies nothing at this checkpoint. A run-dependent scope is declared as a **binding rule resolved at arrival** (e.g., scope = "targets of the held call"), never chosen by an A8. An A12 checkpoint that names no setting content is **invalid**, unconditionally (FB-17; INTEGRATION, R4-9 as amended by R5-3). The setting content is an **operation-class** grant only: a checkpoint cannot require a network-destination grant (ACT §2.7) in this increment; that is a possible later extension, PROPOSED, with no definition (R10-9). |
| kind (a) on a harness capability | Declarable. **Governance phase, governed checkpoint:** **not holdable in App runs** as hold routes now stand; hold support is *not enforceable* and the workflow is *unsupported* on that surface (FB-18; R4-21; R5-1). Phase 1: guidance like any checkpoint (§4.3.0). |

A review-only workflow can now require A4 on the rows it examined through
**objects a named output concerns** (R3-1; U-28 closed).

#### 4.3.2 What a checkpoint is and is not

- A checkpoint **names** a human act the plan pauses for (Phase 1: guidance;
  governance phase, if governed: the run waits). It does not perform, record
  or imply the act.
- Every act kind in the closed list is reserved to the person (S-Q; A12 via
  D2e). A checkpoint does not extend or narrow that list. Operation-specific
  additions for the first connected operation remain `UNRESOLVED{OI-021}`.
- A recognized act kind outside the closed list (A1 propose, A2 apply, A3
  examine, A8 request, A9 record, A10 reject, A11 withdraw, A13 enable
  external access, A14 answer tool permission, and A15 register workflow
  revision, PROPOSED in ACT per R12-5) is **invalid** as a required act
  (FB-03; V18-2 m-11). An unrecognized name is **not established** (FB-04) (R2-10).
  An agent's examination findings are not an A4 act (V4-EXM-21; R-4).
- A checkpoint is not a tool-permission prompt. An A14 answer, whether from the
  person or from the user's own Codex mode, never satisfies a checkpoint (S-R).
  A14 settlements are recorded only in the run record's tool-permission
  element (per R2-8), never as a human-act record.

#### 4.3.3 Independence rules

- **I-1 One kind, one evidence.** A checkpoint is satisfied only by evidence
  of its own act kind, by a qualifying actor, bound to its bound subject's
  current content. Evidence of another kind satisfies nothing here (S-H).
- **I-2 No success inference.** Operation success, a queued proposal, a
  receipt of application, host checks passed or an agent's examination
  supplies no human act (S-G; d3).
- **I-3 No synthetic ordering.** The contract imposes no rule that A5 must
  precede A4, A6 or A7. An independently evidenced act counts on its own
  evidence. A workflow may place checkpoints in a method order; that order is
  the workflow's visible declared method. The proposal lifecycle's
  accepted → applied sequence (V4-HI-23) is an operation lifecycle, not a
  checkpoint ordering rule.
- **I-4 Lapse and re-hold (R2-19; EXEC §4.7, ADOPTED by R4-3).** If
  bound content changes after the act, an **act-lapsed event** is always
  recorded and presented. The **resume point** is the first run action after
  the arrival became *performed* (or *resolved negatively* with a proceed or
  return path), recorded as a run-resumed event (EXEC HD-5). Then:
  - *before resume*: the arrival returns to **waiting** ("waiting — lapsed at
    ‹t›"); a new act on current content is needed (on the lapsed referents
    alone, when the earlier act still covers the others; joint answer below);
  - *after resume, run live* (**governance phase**, governed checkpoint; in
    Phase 1 the act-lapsed event is recorded, labelled **"act lapsed at ‹t›"**
    (nothing says *waiting*; R8-12 item 1), gated outputs show *lapsed*, and
    nothing re-holds, per §4.3.0 CG-6 and EXEC PH-8): the **same arrival**
    re-holds: **waiting — re-held, lapsed at ‹t› after resume**. What "held" does follows the
    hold-support value (§4.3.8, R6-3): under *enforced by the host loop* the
    run stops at its next action boundary; otherwise the actions are recorded
    as *action during hold*; dispatches in flight complete and are observed; nothing done is
    undone. Outputs whose **gating checkpoint** is this one show their
    standing *lapsed* for the affected referents. The act is requested again
    for the **whole** bound scope, with the lapsed referents marked. A
    satisfying act, or a joint answer, makes the arrival *performed* again
    with the next performance ordinal. If the run ends while re-held, the
    final disposition is *waiting*;
  - *after the run has ended*: the standing disposition is **lapsed**.

  **Joint answer (SETTLED by DECISION-K1 K1-3; EXEC §4.7 JA-1; U-05c
  closed).** Two or more acts may together answer one arrival; each cites its
  items. When one act covered several referents and only some change, a new
  act on the changed referents alone answers the checkpoint together with the
  earlier act for the unchanged referents. This holds in both phases.

  **A5 and A12 never re-hold.** Applying an accepted change item does not
  lapse its A5 (A5 binds to the change-item content identity); a basis failure
  between acceptance and application is the stale rule, not lapse (R-6). A
  later established A12 supersedes an earlier one; it does not lapse it (R2-7,
  R4-6). An undo *reverses ⟨receipt⟩* and lapses acts bound to content it
  changes, normally (R2-15). The interim "performed + act-lapsed" display is
  withdrawn (R4-3).
- **I-5 Capturing-surface evidence.** Satisfaction requires attributable act
  evidence from the **capturing surface**: the host's act facility for acts on
  host content (V4-HI-31), or the App interface for acts in the App. Faithful
  recording (A9) by any identified recorder distinct from the decision actor
  is a conformant record shape (settled; V4-AUT-03), and must cite the
  capturing surface's **capture-evidence reference** (act identity, actor, act
  kind, bound content identity, time). An agent-authored record, or a
  statement in conversation, never satisfies a checkpoint. No faithful record
  is made through an act-performing (reserved) operation (R2-2). Whether a host
  exposes a capture-evidence reference is a relay question (DEP-001; R2-20):
  without one, no host-content checkpoint can reach *performed*; it stays
  *waiting* (or *unknown* after interruption). In the App the capturing
  surface is a dedicated App act control (EXEC §5 CAP-1…CAP-9). Answers to
  Codex user-input or MCP elicitation requests are **not act evidence** and
  never host act capture, even when the person gives them (R4-12; EXEC CAP-6).
- **I-6 Negative decisions (R2-5).** For A5 the negative decision is A10
  reject, itself reserved wherever A5 is (S-S). For A4, A6, A7 and A12 a
  person's decision not to act is an **act-declined event**, with capture
  evidence; it is not an act of that kind and does not satisfy the
  checkpoint. Both give **resolved negatively**. Stopping the run is a
  separate **run-ended event**; it does not resolve a checkpoint.
- **I-7 An acceptance checkpoint forces a proposal.** If a checkpoint requires
  A5 on an operation's result, that operation's treatment in the run is
  *propose* regardless of the grant (DERIVED, R-5). The **governing checkpoint
  constraint** (§4.2.2) accompanies each change request for it, with its
  carriage assurance; only *host-held* carriage satisfies R2-12 (R5-2). A request
  to apply it directly is **not permitted**, naming the constraint as the
  governing treatment; it is never converted into a proposal (R-3.3; R2-12).
  A workflow that wants direct application under a grant followed by a human
  act declares a checkpoint on the applied result instead (A4 with subject
  class "objects changed by a named outcome"). **Phase (R8-1):** the
  constraint's carriage and the host's *not permitted* on its account are
  governance phase (a governed A5 checkpoint). In Phase 1 the agent follows
  I-7 as plan guidance: it proposes, and never requests direct application
  of that operation. The host's own treatment governs any request. The agent
  never adds a field the host's schema lacks (R8-10); SWBPIPE refuses unknown
  fields (SQ-02 (a), SQ-31). In the current phase I-7 is plan guidance for
  the agent, and the host's own treatment of its operations decides what the
  host does; the forced treatment binds only for governed checkpoints in the
  governance phase. V4-HI-42's request clause and record clause are in force
  whatever the autonomy setting for a checkpoint the run reaches. Where the
  active grant lets the host apply directly, no proposal is queued, so the A5
  checkpoint (kind (c) *queued*) is **not reached**: nothing is requested by
  reason of an arrival that did not occur, no A5 is forced, and none is
  recorded; the record shows the direct application under the person's
  grant. A checkpoint of any kind that the run does reach while a grant
  permits direct application has its act requested and is *waiting* until
  the person performs it (R8-11 item 2 and R8-12 item 2, as restated by R9-2
  and corrected by R10-1; U-34 closed).
- **I-8 Earlier acts (SETTLED by DECISION-K1 K1-2; EXEC SP-6; U-31
  closed).** In the current phase an act captured before the arrival counts
  toward it when it is of the required kind and the content it was made on is
  still current (I-1, SB-1…SB-3); the record cites the earlier act and its
  time. An earlier act whose content is no longer current, or whose kind
  differs, is shown "prior act not counted", with its reason, *content no
  longer current* or *another act kind* (the one wording of RS L-13; R12-10).
  This adds no
  ordering between act kinds (I-3 stands). **Governance-phase option
  (retained; PROPOSED; EXEC SP-6F; formerly this rule, R4-5):** a workflow
  that takes up the governance phase may require a fresh act, counted only if
  captured **at or after** the arrival's event (by a request relation where
  the capturing surface records one, otherwise by evidenced times); under it
  any earlier act is shown "prior act not counted — captured before arrival (governance-phase option)", and an
  act whose order cannot be established does not count and the arrival shows
  "act order unknown". A checkpoint takes up this option by declaring
  **fresh act required** together with `governed` (§4.3.1 FA-1…FA-5;
  PROPOSED at v0.8, R12-10).
- **I-9 No unenforceable hold is claimed (R4-2; D6; R5-1; R6-3; R8-1).**
  **Phase 1:** no hold is claimed or enforced for any checkpoint. A run action
  taken after an arrival and before its act may carry the optional annotation
  "continued past ‹checkpoint› before ‹act›", which is never a defect (§4.3.0
  CG-6). **Governance phase (retained), governed checkpoints:** what
  "held" means depends on the checkpoint's hold support on the acting surface
  (§4.3.8): under *enforced by the host loop* the run stops at its next
  action; under *enforced on the host route* the host refuses the held host
  operations, and any other action is recorded as **action during hold**;
  under *not established* or *not enforceable* nothing is stopped and every
  run action taken while an arrival waits is recorded as **action during
  hold**, never hidden. Where hold support is *not enforceable* the workflow
  is *unsupported*; where it is *not established* the check is *not
  established*. If the person runs the workflow anyway, every arrival records
  its hold-support value.

#### 4.3.4 Disposition vocabulary (shared; R-5 as amended by R2-5, R2-19)

| Disposition | Meaning |
|---|---|
| **not reached** | The reached-when condition has not been observed. If the run ends without observing it, the final disposition is **not reached**, never performed. |
| **waiting** | Reached; the act is requested (with purpose and scope). Phase 1: a record label, "reached; act not yet recorded"; nothing is held (§4.3.0). Governance phase: the run holds where hold support allows (§4.3.8). Annotations include: "lapsed at ‹t›" (before resume); "re-held, lapsed at ‹t› after resume" (I-4, governance phase; in Phase 1 a lapse after resume is labelled "act lapsed at ‹t›" instead, R8-12 item 1); "prior act not counted", with one reason: *content no longer current*, *another act kind*, or *captured before arrival (governance-phase option)* for any earlier act under that option (the one wording of RS L-13; R12-10; a display may add the reason after a dash) and "act order unknown" (that option only) (I-8); "A12 awaiting control confirmation" or "A12 refused by control: ‹reason›" (SB-4); "no items remain" (MX-6); "subject absent"; "hold not enforceable" / "action during hold" (I-9, governance phase); "continued past ‹checkpoint› before ‹act›" (Phase 1, optional). If the run ends while waiting, a **run-ended event** is recorded and the final disposition stays **waiting** (R2-5). |
| **performed** | Capturing-surface evidence of the required act kind, by a qualifying actor, bound to the current content of every bound referent in scope (see §4.3.7 for reduced subjects), from one act or from several acts that together cover the scope, each citing its referents (I-4 joint answer). An act captured before the arrival counts on current content and is cited with its time (I-8). |
| **resolved negatively** | For A5: A10 evidence decides the bound items (fully, or with per-item annotation under §4.3.7). For A4/A6/A7/A12: an act-declined event. The **on negative decision** path governs. Never counted as performed. |
| **lapsed** | Standing disposition only for a checkpoint whose run has ended, when a performed act's bound content changed afterwards (per referent). |
| **unknown** | The observation that would decide arrival or the act was lost (e.g., interruption). Never presented as performed (S-K). |

**Run end and continuation (R4-4; EXEC §4.9; PROPOSED (W7)).** An ended run
is never resumed; its dispositions are final, except *performed* → *lapsed* on
a later lapse. An act performed after run end is recorded (DEL-04-03) and
shown against the bound subject marked **"after run end"**; it changes
nothing. To carry work on, the person starts a **new run** that may record
**continues ⟨run⟩**; it inherits no arrival, disposition or act, and its
arrivals bind only what the continuation itself observes. An earlier act,
including a post-end act, counts at a continuation's arrival when it is of the
required kind and its bound content is still current, and is cited with its
time (I-8; DECISION-K1 K1-2); under the governance-phase option it is shown
"prior act not counted — captured before arrival (governance-phase option)". An interruption (lost observation, App or
loop restart) is **not** a run end: the same run is recovered (EXEC §4.12).
The hold state machine and replay are DEL-02-03's (EXEC §4; Phase 1 recording only, EXEC §2.1; hold content governance phase, EXEC §2.2).

#### 4.3.5 Reached-when evaluation rules (meaning only)

- **RW-1** Arrival is observed, never inferred from model text or prose
  stage.
- **RW-2** Kind (a) is evaluated before the named operation is dispatched.
  In the governance phase (governed checkpoint), the call is held
  undispatched and, once *performed*, the **same** held call is dispatched
  unchanged (LOOP §2.4.1). In Phase 1 the arrival is recorded where it is
  observed (R9-1), and nothing is held. Kind (b) needs the output's
  production to be observed as its production element says (§4.4): for a
  message, a completed agent message carrying its designating line
  (OP-1…OP-6); for a file, the observed completed write of its path; for a
  host change, the named host outcome. Kind (c) needs the named host outcome
  as reported under P §9 (e.g., *queued*, *applied (receipt)*).
- **RW-3** If a reached-when names a tool or output this workflow does not
  declare, the checkpoint is invalid (FB-13).
- **RW-4** A checkpoint may be reached more than once in a run (e.g., after a
  stale refusal and re-draft, the new proposal's *queued*). Each arrival binds
  its own referents; earlier dispositions remain history.

#### 4.3.6 Subject binding (R2-17, R-6, R2-14)

| Subject class | Bound at arrival to | Content identity the act must match |
|---|---|---|
| change items of a named proposal | The items of the proposal whose *queued* outcome was observed (by proposal and item identity) | **Change-item content identity** per item (DEL-03-02; P-v0.8 §3.1, §3.4, assigned by the host, §3.5 PM-6; schema `proposal_state.schema.json` `item.change_item_content_identity` with `identity_method`): operation identity and version, bound targets, old/new values, relied-on basis |
| named output | The produced output | The output's content identity (host-supplied; file content identity for App files; for a message, the content identity of the completed message text, §4.4 OP-3) |
| objects a named output concerns | The objects the produced read/examination output identifies (e.g., rows an OP-C3 finding names) | **Subject content identity** of each object **as read** by the read the output relies on (C §5.3/§5.4), with method designation; never the output's own content identity and never text in the output (INTEGRATION, R3-1) |
| objects changed by a named outcome | The created and changed object identities the **applied outcome** identifies (R2-14; P-v0.8 §9 applied association, schema `applied.resulting_objects`, which may be "not supplied"; C §3.3/§10 T12: e.g., S-5 created) | **Subject content identity** of each object **after application** (C §5.3), with method designation. Where P records the resulting objects as not supplied, or an object without its subject content identity (optional in P's schema), the binding is *unknown* for it, never assumed |
| targets of the held call | The targets the held kind (a) call names | Subject content identities of those targets **from the relied-on read the held call cites** (C §5.3/§5.4); never argument text |
| grant setting | The setting content the checkpoint's **declaration** names, with any run-dependent part resolved at arrival by its declared binding rule (R5-3); never an A8's choice | The **setting content**: classes, grant values, scope (R2-7); an operation-class grant only, never a network-destination grant (R10-9) |

- **SB-1** Every content identity carries its identity method designation;
  identities with different designations are *unknown (incomparable)*, never
  "unchanged" (C §5.2 rule 6). Algorithms remain unselected.
- **SB-2** An act on other content, another proposal or another object set
  does not satisfy the checkpoint, even if its kind matches (VC-21).
- **SB-3** Binding by object identity is exact: an edit to one bound object
  lapses only that object's act; an unrelated edit elsewhere lapses nothing
  (C §5.3). **Whole-model identity (R8-4):** where a host supplies only a
  whole-model identity, it is received as the identity of every subject it
  covers. Any model change then lapses every bound act: this errs toward
  reporting a lapse and never misses one. The App never computes identities.
  Against SWBPIPE, subject binding can bind only to the whole-model identity
  (SQ-03 (a); U-35).
- **SB-4 A12 (R2-7; EXEC §4.10, ADOPTED by R4-6).** The control's
  response is a relation on the act, not its content:
  - **established ⟨settings version⟩** → the A12 counts (with I-1…I-8) and the
    arrival is **performed**;
  - **pending** (set by person, not yet confirmed) → **waiting**, "A12
    awaiting control confirmation";
  - **refused ⟨reason⟩** (e.g., no policy basis, R2-9) → **waiting**, "A12 by
    ‹person› refused by control: ‹reason›"; the refused A12 remains a
    recorded human act, establishes nothing and does **not** supersede the
    setting in force;
  - confirmation observation lost → **unknown** until observed.

  Only an **established** later A12 supersedes an earlier one; a checkpoint
  satisfied by the earlier A12 stays **performed** with "superseded by ‹act›"
  shown.

#### 4.3.7 Item-level decisions at an A5 checkpoint (PROPOSED; R2-18; confirmed by DEL-02-03, R4-7)

This is the rule LOOP C-7 and PANEL W-5f cite. The acceptance unit is the
change item (R-6). DEL-03-02 supplies per-item dispositions, the "all items
decided" indication and item-left events (P §4.3). At P-v0.8 (arc N-18;
DEP-02-01-029; R14-8) they are: per-item states and decisions in P §4.1 and
§4.6 PT-1…PT-19, schema `item.state` (14 values) and `item.decision` {A5,
A10, A11}; the all-items-decided indication in §4.3 and §4.6 DS-4, schema
`derived_state.all_items_decided`; item-left events {proposal, item, cause,
time, evaluated basis} in §4.3, which R14-8 makes explicit in P's schema
(node RP-2) where it was derivable only from `item.state`. Mapping to the
item states below: *accepted* → A5; *rejected* → A10; *queued* →
undecided; *refused — stale*, *refused — invalid*, *refused — not
permitted*, *withdrawn* or *left queue* without a decision → left;
*outcome unknown* on a deciding observation → unknown. DEL-02-03 **confirmed** all
rows and added MX-3, MX-6 and MX-8 (EXEC §4.11, PROPOSED (W7) confirmed).
Per-item states: A5 · A10 · undecided · left · **unknown** (decision
observation lost).

| Item state at evaluation | Checkpoint disposition | Per-item annotation shown |
|---|---|---|
| Every bound item has A5 on current item content | **performed** | each item "accepted by ‹person›" |
| At least one bound item has neither A5 nor A10 yet | **waiting** (even if others are unknown) | decided items show their act |
| **MX-3** No item undecided; at least one item's decision observation lost | **unknown** | which items are unknown; last observed state |
| Every remaining bound item has A5 or A10, and at least one has A10 | **resolved negatively**; **on mixed decision** governs if declared | "partial": which items A5, which A10. Accepted items keep their A5 and proceed through the host lifecycle unaffected |
| An item leaves without a decision (stale refusal, A11 withdrawal, host refusal) | Item leaves the bound subject; disposition is evaluated over the remaining items. **MX-6:** if none remain, the arrival is **waiting** "no items remain"; when a new arrival of the same checkpoint occurs (e.g., a re-draft queued), this arrival is closed "replaced by arrival n+1" with final *waiting*; otherwise it waits until run end | Each leaving item shown with its item-left event. A *performed* over a reduced subject is never shown as "all items accepted" |
| An item already decided (A5) is later refused at application (e.g., stale, R2-16) — adopted per R3-3; confirmed (MX-7) | Unchanged (the decision stands) | "accepted by ‹person› — not applied: refused — stale (relied ‹B›, current ‹B′›)"; A5 not lapsed; the declared output is not produced for that item (§4.6); a re-draft carries no acceptance |
| **MX-8** An item with A5 later meets **application error** (effect none / partial / unknown) or **outcome unknown** at application | Unchanged | "accepted — not applied: application error (effect …)" or "accepted — application outcome unknown (observer …)" |

MX-7/MX-8 never re-hold the A5 arrival and never trigger its negative or mixed
path; a checkpoint binding "objects changed by a named outcome" binds only the
objects of items actually applied; a re-draft reaching *queued* is a new
arrival with no acceptance carried over (EXEC MC-1…MC-4).

Retries de-duplicate by proposal identity before any basis check; a resubmitted
proposal returns its recorded state and is never refused stale by its own
effects. Applying sibling items does not stale remaining items unless they
share targets, **where the host supplies subject identities** (R2-13 as
amended by R8-3). Otherwise the App receives and shows the host's stated
staleness scope, never narrowing it. For SWBPIPE the scope is the whole
model: any model change stales every queued proposal (SQ-07 (d)), so its
items leave the bound subject as stale.

**Host outcome mapping (R8-5).** A host clearing of the queue by the person
without a decision record, such as SWBPIPE #885 `withdrawn`, is an item
leaving, "cleared by the person, no decision record". A `validation_rejected`
at Apply is *refused — invalid* at application. Neither is ever A10 or A11.
On SWBPIPE, Apply accepts and applies a batch atomically in one step, and
Clear discards without a record (SQ-09, SQ-01). The per-item A5/A10 and
mixed-item rows above have no SWBPIPE counterpart; their meanings are kept.

#### 4.3.8 Hold support per checkpoint and surface — governance phase (retained; R5-1; R4-2, R4-8, R4-21; EXEC §3.6)

**Phase (R8-1).** This subsection is the **governance-phase definition,
retained**. It is relabelled, not deleted. In Phase 1 no hold-support value is
assigned and no checkpoint is held (§4.3.0; EXEC PH-3). In the governance
phase it applies to checkpoints declared **`governed`** (§4.3.1; EXEC GV-2).
"In this increment" below means "in the governance phase as the hold routes
now stand".

The declaration names checkpoints; whether a governed checkpoint can actually
be **held** depends on the surface running the workflow. The compatibility
report (DEL-02-03, owner of the values, EXEC §3.6) states exactly one
hold-support value per governed checkpoint and acting surface, and the run
record carries it:

| Hold support | Meaning | Workflow requirement check (governance phase) |
|---|---|---|
| **enforced by the host loop** | Embedded route: the host loop holds the run (LOOP §2.4.4). SWBPIPE has no host loop (SQ-20) | passes (holds subject to host evidence, DEP-001) |
| **enforced on the host route** | The host holds or refuses the operation through a *host-held* constraint (§4.2.2), evidenced by the host's answer to SQ-02 and a candidate. Not offered by SWBPIPE (SQ-02 route (iv)) | passes |
| **not established** | Depends on a host answer not yet given (SQ-02) or on unagreed exposure. Examples: in an App run through the external channel X, an A5 checkpoint whose constraint the host would have to hold, or a kind (a) checkpoint on a host operation the host would have to hold. SQ-02 was answered for SWBPIPE on 2026-09-28, so against SWBPIPE neither cause gives this value now: HS-3 (c) decides (R8-2) | *not established* — never a pass, never *unsupported* |
| **not enforceable** | No mechanism exists on this surface in this increment. In an App run: a checkpoint whose **held actions include an App-side step** (HS-5; App-side holds are D6, and neither interposed App code HP-1 nor `turn/interrupt` HP-2 is adopted); a constraint carried only as *model-supplied*, once SQ-02 is answered with no host-held route (HS-3; before that answer, *not established*; SWBPIPE has answered); kind (a) on a **harness capability** (R4-21) | *unsupported* — "checkpoint hold not enforceable on this surface: ‹name›" (R4-8) |

**Assignment by held actions (R6-1; EXEC §3.6).** The value is decided by the
checkpoint's **held actions** (§4.3.1), not by how it arrives. Rules are
evaluated in the order HS-1, HS-2, HS-5, HS-4, HS-3; the first match decides:

| # | Surface and checkpoint | Value |
|---|---|---|
| HS-1 | Invalid (FB-03, FB-13, FB-16, FB-17) or not established (FB-04) | **No value**; reported before the run, never evaluated; the check is *not established* via the declaration (EXEC F-22, confirmed by R6-1) |
| HS-2 | Host run on the embedded surface E | **enforced by the host loop** |
| HS-5 | App run; at least one held action is App-side, or (for a kind (b)/(c) checkpoint without derived held actions, §4.3.1, R7-3) the declaration does not show that every held action is a host operation | **not enforceable** (D6), whatever SQ-02 returns |
| HS-4 | App run on X; every held action is a host operation, one with unagreed exposure. **Except** where SQ-02 is answered with no host-held route: then HS-3 (c) decides regardless of exposure (R8-2; SWBPIPE: SQ-11 answered, no exposure element) | **not established** |
| HS-3 | App run on X; every held action is a host operation on the external channel | By SQ-02 status: answered with host-held carriage or a host hold evidenced on a candidate → **enforced on the host route**; unanswered → **not established**; answered with no host-held route (**SWBPIPE, 2026-09-28**: route (iv), none planned) → **not enforceable**. Never assumed. A later SWBPIPE decision to plan a route is a revision trigger |

**What "held" means per value (R6-3; governance phase).**

| Value | At the hold |
|---|---|
| *enforced by the host loop* | The run stops at its next action |
| *enforced on the host route* | The host refuses the held host operations; any other action is recorded as *action during hold* |
| *not established* / *not enforceable* | Nothing is stopped; actions are recorded as *action during hold* |

In Phase 1 nothing is stopped for any checkpoint, and actions may carry
"continued past ‹checkpoint› before ‹act›" (§4.3.0 CG-6).

**Workflow precedence (EXEC §3.5, INTEGRATION; governance phase).** Where
governed checkpoints differ, any *not enforceable* makes the workflow
*unsupported*; otherwise any *not established* makes the check *not
established*.

**Authoring advice (R6-1; CA WR-11; governance phase).** A governed checkpoint
that must be enforceable from the App keeps **all its held actions on host
operations**, e.g. an A5 constraint, or kind (a) on a host operation. It is
then enforceable only on a host that offers and evidences a host-held route. A
checkpoint that holds any App-side step (e.g. Return) stays *not enforceable*
in App runs. Against SWBPIPE (SQ-02 answered: route (iv)) no host-held route
is available, so **no governed checkpoint is enforceable from the App on X in
this increment**, and every such workflow run from the App on X is
*unsupported* in the governance phase. The advice stands for a host that
offers a host-held route. In Phase 1 the advice does not affect the check.

HP-3 (an App named-rule *decline* of a tool-permission request, never an
affirmative answer) remains a permitted best effort under D3 in the
governance phase; it does not make a hold *enforced*. SQ-02 was answered on
2026-09-28 with no host-held route, so in the governance phase HS-3 rows are
*not enforceable* against SWBPIPE. Checkpoints holding any App-side step stay
*not enforceable* (R5-10; R6-1; U-30). **D6 is closed for Phase 1** by
DECISION-4 and re-opens when the governance phase is taken up (R8-2).

### 4.4 Returned outputs (SOW-045)

| Element | Meaning |
|---|---|
| **output name / meaning** | Local name and readable description. |
| **output form** | A change to host objects (always through the host's one route: proposal, or direct application under an effective direct treatment, V4-HI-20…23); a file or document; a report or message to the person; an input to another workflow; a human-act standing, produced only by the person's act at its gating checkpoint (made explicit at v0.8, §3.6). |
| **destination** | Host tables/views, the project, or the conversation. Host-changing outputs appear in the host's own views; there is no agent-private surface (V4-HOST-04). |
| **promised standing** | From the non-approval vocabulary, aligned with P §9 and R-4: *queued*; *applied (receipt)*; *agent-prepared*; *agent-examined (non-mutating)* (A3 findings, e.g., the result of an examination operation such as FX OP-C3); *host checks passed: ‹named checks›* (only where a host result names its checks, each with its evaluated basis). Never *approved*, *certified*, *sealed* or *code-compliant* (S-L). Unqualified "checked" is used only for A4. A human-act standing (e.g., *marked checked by the person*) can only be promised conditional on a named checkpoint. |
| **gating checkpoint** | Optional reference to the checkpoint whose act the promised standing depends on. Required for a human-act standing. |
| **production** (v0.8; PROPOSED; R10-8) | How the output's production is observed. A host change: the host outcome of named operations that produces it (for example *applied (receipt)*). A file: its path relative to the project; produced when a completed write of that path is observed. A message: its **designating line** (OP-1…OP-6 below). An input to another workflow or a human-act standing has no production of its own that a checkpoint could observe. |
| **relies on** (v0.8; PROPOSED) | Optional: the read or examination tools whose results the output reports, by local name. Required for the subject class "objects a named output concerns" (§4.3.1), whose binding uses the subject content identities as read by those reads (§4.3.6). |

**Designating a message as a declared output (PROPOSED at v0.8; R10-8;
S1-C WD 7).** LOOP §2.4.1 counts "a completed agent message the declaration
designates as that output" for reached-when kind (b); this is the
designating element.

- **OP-1** A message-form output declares a **designating line**, an exact
  text. The output is produced when a *completed* agent message is observed
  whose first non-empty line, with surrounding whitespace removed, equals
  that text (every character, case included).
- **OP-2** Only a completed message counts. Streamed fragments, an
  unfinished message, reasoning, a plan and tool output never do. Which
  harness event is "a completed agent message" is DEL-02-03's in App runs
  (at pin 0.158.0 the completed item of kind `agentMessage`; EXEC's App-side
  table, Wave B node B2) and DEL-05-01's in host loops (the completed
  assistant message).
- **OP-3** The message is the output. Its content identity is that of the
  completed message text, which the subject class "named output" binds
  (§4.3.6). A statement elsewhere that the output exists is not its
  production (RW-1).
- **OP-4** Each completed message carrying the line is a production. A
  checkpoint on the output arrives each time (RW-4), and each arrival binds
  its own message.
- **OP-5** A workflow's message outputs have distinct designating lines
  (§3.7 DN-4; FB-20).
- **OP-6** The prose names the line, so the agent knows to write it (CR-7);
  the product never adds, removes or rewrites it. A message without the
  line is not the output, and the output stays "not produced" (§4.6).

*Why a line and not a supplier field.* At pin 0.158.0 an `agentMessage`
item carries an optional `phase` (commentary or final answer), and the
generated schema itself says providers "do not emit this consistently". It
could not tell apart several outputs of one run, and it is a supplier field,
which this contract does not select (R12-1).

### 4.5 Returned evidence (SOW-045)

| Element | Meaning |
|---|---|
| **evidence name / meaning** | What the evidence shows and for which output or checkpoint. |
| **evidence kind** | Host receipt reference; relied-on read-basis reference (five elements, V4-HI-11/21); evaluated basis of a non-success outcome; host result reference (with any named host checks); agent examination (A3) reference; human-act record reference (with capturing surface and capture-evidence reference); run record reference. |
| **by reference** | Host receipts, hashes and origin marks remain host-owned; declared evidence names a link, not a copy (S-P). |
| **supports** | Which output(s) or checkpoint(s) it supports. Evidence for one act supports no other (I-1). |

### 4.6 Promised versus observed (REQ-004; AC-004)

| Declared promise | Observed counterpart | Observation owner | Absent observation means |
|---|---|---|---|
| expected input | input actually supplied, with its basis | run record (DEL-04-03); read basis (DEL-03-01) | "not supplied" / "basis unknown" / "basis incomplete" |
| required tool reference | compatibility outcome and pass result (§4.2.4), then operations requested and their P §9 outcomes | DEL-02-03 check; run record | "not established" |
| checkpoint | disposition (§4.3.4), bound referents, act and event references (act-lapsed, act-declined, run-ended) | DEL-02-03 (App) / DEL-05-01 (host); DEL-04-03 | "not reached", "waiting" or "unknown", never "performed" |
| output with promised standing | produced output and actual standing per item (queued, accepted, refused — stale, applied (receipt), application error, outcome unknown …) | host; run record | "not produced", or "outcome unknown" attributed to the observer that lost observation (R-7) |
| evidence | linked receipt or record actually present | host; run record | "missing"; never a pass |

### 4.7 Compatible roles and restrictions (retained from Root)

| Element | Meaning |
|---|---|
| **compatible roles** | Which of the four roles the method is written for (Root `compatible_roles`, retained). Omission inherits compatibility; it never expands a role. |
| **tool restriction** | Optional ceiling narrowing the tools the method may use (Root `tools`, retained as a restriction, distinct from §4.2). |
| **enforcement statement** | None in the declaration. Metadata never proves enforcement. Where a harness or host cannot enforce a restriction, the consumer reports it as instruction-asserted (S-N). |

A workflow requiring delegation is compatible only with a role and seat that
can delegate. In a host seat without delegation, it is **unsupported**
(§4.2.4), never silently run without delegation. At v0.8 the need is
declared as a required harness capability `agent-delegation` (§4.2.5 HC-3).
Where the declared part states compatible roles and a Root `execution.json`
in the same package states others, the roles are not established (FB-22).

---

## 5. The four roles and the single host seat (SOW-021, SOW-022; REQ-001; AC-001)

### 5.1 Common meaning (settled)

| Role | Meaning (V4-ROLE-01) |
|---|---|
| HELP_HUMAN | Alignment with the human |
| HELPS_HUMANS | Design |
| WORKING_ITEMS | Managed execution |
| TASK | Bounded execution; does not delegate (V4-ROLE-03) |

No fifth role: a domain expression such as the SWB Piping Designer
specializes context, tools and workflows within these roles (V4-ROLE-03).
Role guidance is supplied additively (V4-ROLE-02); supply is DEL-02-04's.

### 5.2 Expressions

| Aspect | Chirality App | Host application (e.g., SWBPIPE) |
|---|---|---|
| Role presence | Person selects a role (DEL-02-04). | Roles recede behind **one agent seat** and the selected workflow (S-M). The host need not present a role choice (REQ-001). |
| Guidance files | Product `AGENTS.md` plus role guidance. | The host's own `AGENTS.md` and `SKILL.md` (V4-HOST-06), open and readable (S-B). Distribution/adoption is `UNRESOLVED{OI-018}`. |
| Workflows | Project, user, bundled; host-origin when opened in App (V4-WF-06). | The host's own library (origin *host*); App workflows carried in unadapted keep their origin, adapted ones become host-origin (§6.4). |
| Tools | Codex native tools; host operations through an external surface (V4-HI-50). | The host's capability catalog (V4-HI-01). |
| Permission modes | Routine tool permission and sandbox are the user's own Codex setting (D3, SETTLED). | No classifier permission mode (D3, SETTLED). Host operation authority is grant plus policy, with the SWB default proposal mode (V4-HI-40/41; DERIVED, R2-11). |
| Delegation | Native delegation for roles permitted to delegate. | Host-defined; absent it, delegation-requiring workflows are **unsupported**. |

### 5.3 What the single seat must still carry

- **SEAT-1** The role meaning under which the seat operates for a run shall
  be determinable from the host's guidance and the selected workflow's
  **compatible roles**, and recorded with the run. Every dispatch carries it
  (R-7; DEL-05-01). If it cannot be determined, the record says **unknown**.
- **SEAT-2** The mapping from the host's single seat to the four role
  meanings is `UNRESOLVED` (U-09). Options: (a) the seat always runs as a
  TASK-equivalent bounded executor of the selected workflow; (b) the seat
  takes the role named by the workflow's compatible roles; (c) host guidance
  names one standing role per conversation. No option is chosen.
- **SEAT-3** Receding does not remove the distinctions: the seat's acts
  remain execution; the person's acts remain the person's (S-H, S-Q).

---

## 6. Source identity (REQ-001, REQ-004; AC-004)

### 6.1 The identity tuple (R-9)

Workflow identity is carried everywhere as {**kind**, **origin**, **source
root**, **name**, **revision**}, plus **derived-from** where applicable.

| Element | Meaning |
|---|---|
| **kind** | Workflow (distinct from skill; Root `kind`, retained). |
| **origin** | *project*, *user*, *bundled* or *host* (S-D). "App-origin" is not an origin class. |
| **source root** | Which library within the origin: the project root, the user's library, the App bundle and its release, or the host application and its library. Root `sourceRootId` meaning retained; values unselected. |
| **name** | Package name, matching its folder. |
| **revision** | Identity of the exact package content selected (all files in the package), with its identity method designation. Algorithm and multi-file canonicalization `UNRESOLVED` (U-03). A name plus origin without revision identifies a library slot, not selected content. |
| **derived-from** | For an adapted workflow: the full identity tuple of the workflow it was adapted from. Adaptation creates a new identity; it never edits the original's history. |

**Revision: file set and canonicalization (PROPOSED at v0.8; the semantic
part of U-03).**

- **RV-1** The file set is every regular file beneath the package folder, at
  any depth: `WORKFLOW.md`, and any companion, resource or other file.
  Nothing is excluded.
- **RV-2** A symbolic link or any other non-regular entry makes the revision
  **not established** ("package contains a non-regular entry"); it is not
  followed.
- **RV-3** Each file is taken as its bytes as stored, with no line-ending,
  encoding or whitespace normalization. A checkout that converts line endings
  yields another revision, truthfully.
- **RV-4** Each file is identified by its path relative to the package
  folder, with `/` separators, in UTF-8, and the files are ordered by those
  bytes.
- **RV-5** Empty folders are not part of the revision. The digest algorithm,
  its framing and its identity method designation stay open (U-03, with
  DEL-04-03 and HOSTING U-08). The prototype's `proto-sha256-list-0` is an
  illustration, not a selection.

A consequence: operating-system files left in a package folder (for example
`.DS_Store`) change the revision. Whether registration refuses them is
DEL-02-02's.

### 6.2 The identity chain: promised versus observed

| Link | Fact | Also recorded (R2-20) | Typical owner of evidence |
|---|---|---|---|
| **listed** | A library reports the workflow exists. | **holding library** | Discovery (DEL-02-02 App; host library) |
| **selected** | The person (or brief) chose a full identity tuple. | holding library | Selection (DEL-02-02; host panel DEL-05-02) |
| **resolved** | That identity resolved to specific revision content. | holding library | Resolver (placement open, §9) |
| **supplied** | Those bytes were supplied to the agent/loop, with per-thread/turn source identity and content identity (method-designated). | — | App: DEL-02-04 / DEL-01-01 (HOSTING §8.2); host: host loop (DEL-05-01 run association). Where the host cannot record it, **unknown** (relay question, R2-20; U-29) |
| **adopted by provider** | The model/harness took it up. Often unobservable; then **unknown**. Supplied ≠ adopted. | — | Stated as a limit |
| **observed behavior** | What the run actually did. | — | Run record (DEL-04-03); host evidence |

A matching name at two links establishes nothing about the others (AX-002).

### 6.3 Collision and rebinding rules

- **C-1** Every discovery that finds more than one origin for a name exposes
  all origins, each with its holding library (R2-20).
- **C-2** A selection holds its full identity tuple. Later discovery of a
  same-named workflow in any origin is reported as a collision and never
  rebinds the selection (S-D).
- **C-3** Only an explicit new selection by the person changes what is
  selected; that is a new selection event, not a rebinding.
- **C-4** Whether a selection follows a new revision of the same slot or
  stays pinned is a selection policy of DEL-02-02 (App) and the host; the
  chain shall make visible which occurred (U-10).
- **C-5** Where *host* sits in unqualified-name precedence is `UNRESOLVED`
  (U-10). Source-qualified selection makes precedence irrelevant to
  correctness.
- **C-6** The holding library never takes part in identity equality: two
  copies with the same tuple held in different libraries are the same
  workflow content, located twice (R2-20).

### 6.4 Carried and adapted workflows (V4-WF-06; R-9; R2-20; confirmed by DEL-02-03 EXEC §6.2, PROPOSED (W7))

| Case | Identity | Holding library |
|---|---|---|
| Carried **unadapted** into a host | Unchanged: original origin, source root, name, revision. | The host library holding the copy, recorded at listed/selected/resolved, shown by the panel beside the origin, carried in the loop's run association. |
| **Adapted** in a host | New identity: origin *host*, host source root, revised revision, **derived-from** = the original tuple. | The host library. |
| Host workflow opened and refined in the App | Opening keeps the host identity. A refinement is a draft (DEL-02-02) and, once registered, a new identity with derived-from = the host tuple. | App library where registered. |

- **HL-2** In a transfer, the *received* link records the destination holding
  library and the *exported* link the source one; a move between libraries
  without a content change creates no new identity (EXEC §6.2).
- **HL-3** The holding library is not recorded at *supplied*: supply is
  identified by tuple and content identity; supplied bytes that do not match
  the resolved revision are a revision defect ("revision not verified").
- The carriage procedure (EXEC §6.3 TR-1…TR-8, carriage manifest), adaptation
  receiving (§6.4 AD-1…AD-6, including derived-from checkpoints and "checkpoint
  meaning changed") and transfer failures (§6.7 TF-1…TF-8) are DEL-02-03's and
  consume this section unchanged.

Examples: EXAMPLES E3, E4.

---

## 7. Root conventions: keep, change or leave open

Root material is a reuse source, not v4 authority (PRD V4-CST-04; ARCH §5).

| Root convention (source) | v4 declaration | Why |
|---|---|---|
| Package = immediate folder containing `WORKFLOW.md`; name matches folder (SPEC §9.3; runtime "Workflow packages") | **Keep** | Satisfies V4-SHR-02; existing consumers read it. |
| Name rule 1–64 lowercase letters/digits in hyphen-separated segments (`catalog.schema.json`; `create-workflow`) | **Keep as reuse candidate**; confirm in OUT-004 fixtures | Source compatibility; no v4 reason to differ. |
| YAML front matter `name`, `description` (`WORKFLOW_TEMPLATE.md`) | **Keep**, with `name` and `description` only; the declared part is carried in the body (§3.5, PROPOSED at v0.8) | Description supports selection; structured content in the front matter would need a YAML parser and would meet Root consumers that expect two strings (§3.5 option (a)). |
| Free prose body, no prescribed headings | **Keep** | V4-WF-01 retains prose. |
| Inputs, outputs, checks and human checkpoints stated only in prose | **Change**: add the declared part, keep the prose | V4-WF-01 requires an observable declared part. |
| `execution.json` `compatible_roles` | **Keep** (§4.7) | Four roles are common. |
| `execution.json` `tools.capabilities` | **Keep as restriction only**; not reused as required tools | Restriction ≠ requirement (§4.2.3). |
| `execution.json` `tools.commands` | **Leave out** of the portable declaration | Repository-specific; not portable. |
| "Metadata never proves host enforcement" | **Keep** | S-N. |
| Origins `project`/`user`/`bundled` and `sourceRootId` | **Change**: add *host*; add revision and derived-from; carried-unadapted keeps origin; holding library recorded beside identity | V4-WF-03/06; REQ-004; R-9; R2-20. |
| Unqualified precedence project → user → bundled | **Leave open** for *host* (U-10) | Not decided by the basis. |
| Source-qualified identity; no silent rebinding; all collision origins exposed | **Keep** | Same as V4-WF-03. |
| `selected-context` fingerprints | **Keep the idea** as revision; algorithm open (U-03) | Needed for promised-vs-observed. |
| Drafts in `.chirality/workflow-drafts/`, panel registration, no overwrite | **Not part of this contract**; DEL-02-02 | V4-WF-02 is DEL-02-02's. |
| `catalog.yaml` navigation, `centralWorkflowNames` | **Leave out** | Library navigation, not declaration meaning. |
| Derived `index.json` | **Keep principle**: derived, never authority | R-3 (§3.2). |
| Legacy `TaskSkill`, `legacy-methods.json` | **Leave out** | Root compatibility only. |
| Four-section role files `AGENT_<ROLE>.md` | **Leave to DEL-02-04 / OI-018** | Role-guidance structure and distribution are not this contract's. |
| Human checkpoints in Root prose (e.g., `create-workflow` review before registration) | **Change**: product-observed only when declared with reached-when, subject class and act kind (Phase 1: guidance and recording; product-held only if also declared `governed`, in the governance phase) | Prose alone cannot be observed (RW-1). |

---

## 8. What each receiver receives from this contribution

| Receiver | Receives from WD-v0.8 (as at v0.7; the additions of v0.8 are in the next table) | Expected check at next comparison |
|---|---|---|
| DEL-02-03 execution (EXEC-v0.5; DEP-02-03-009) | §4.2 references, constraint and pass rule; §4.3 incl. §4.3.0 Phase-1 guidance, the `governed` flag, subject class, validity rules, I-1…I-9, dispositions, §4.3.7, §4.3.8 (governance phase); §6.4 | EXEC §2.1/§2.2 and WD §4.3.0/§4.3.1 `governed` agree; WD's adoption of EXEC §3.6, §4.7, §4.9, §4.10, §4.11 unchanged; SP-6 as settled by DECISION-K1 K1-2 (with SP-6F) and §4.7 JA-1 (K1-3) followed in I-8 and I-4 |
| DEL-05-01 loop (DEP-05-01-016) | §4.3.0 (Phase 1: the host loop enforces no hold); §4.3.1 reached-when, `governed` and **declared** subject class; §4.3.5; §4.3.6 binding table; §4.3.4 dispositions incl. lapse sequence and run-ended; I-5; I-7 constraint carriage; SEAT-1; §6.1–6.2 incl. holding library and supplied link | Binds declared class, not kind (IR1C-01); adds A12 to act-declined; adopts R2-19 lapse sequence; carries purpose and scope in "act requested" |
| DEL-05-02 panel (DEP-05-02-005) | §4.2.4 outcomes and pass rule; §4.3.4 dispositions; §4.3.7 annotations and item-left display; §4.4 labels; §6.1–6.4 incl. holding library | Selection shows holding library; W-5f cites §4.3.7; purpose and scope shown |
| DEL-03-02 proposal (DEP-03-02-027) | §6.1 identity tuple, for proposal origin; §4.3.1 required act, subject class and reached-when; §4.2.2 governing checkpoint constraint (governance phase); §4.3.6 use of applied-outcome object identities; §4.3.7 item rule and its needs (item-left events, all-decided) | Constraint element in P §3.3; item-left events |
| DEL-03-03 adapter (DEP-02-01-027; SoW CLM-002) | The declared checkpoint constraints, for carriage on the external channel in the governance phase: §4.2.2 governing checkpoint constraint with its carriage assurance; I-7; §9 A-12. In the current phase no constraint is carried (§4.3.0) | ADAPTER §5.1 and §5.3 cite WD §4.2.2 and I-7; §7.7 keeps recording apart from holding |
| DEL-03-04 guide (DEP-03-04-008) | The portable workflow, four-role and shared-allocation receiving semantics, by version label and section: §3–§6, §9, §10, §12 | GUIDE's workflow entries and completeness comparison cite WD-v0.8 (GUIDE is re-pinned last) |
| DEL-09-06 connected activity (DEP-09-06-025) | Portable declaration, identity and revision meaning: §3, §4, §6 (with §6.4 carried and adapted workflows); EXAMPLES E1, E1c, E1d, E8, as CA uses them (R10-11) | CA's workflow round-trip cases use the identity tuple and the declared-part meaning unchanged |
| DEL-04-01 policy | §4.3.1 closed list, invalid vs not established, subject classes (incl. held-call targets, grant setting) | §4.1 split; §4.2 referent list. No ACTIVE register row names DEL-04-01 as a consumer of this contract: the registered join runs the other way (DEP-02-01-018; DEP-04-01-012). The row is kept as a cross-check of the mirrored lists |
| DEL-02-02 (DEP-02-02-014), DEL-02-04 (DEP-02-04-011) (later undertaking per D1) | §3, §6, §4.6; §5 | Not exercised in this undertaking |
| Outside this increment: DEL-08-02 (DEP-08-02-006), DEL-09-02 (DEP-09-02-015), DEL-10-03 (DEP-10-03-008) | DEL-08-02: the portable method meanings (§3, §4). DEL-09-02: the workflow declarations for the V4-EXM-10 examination (§3–§6). DEL-10-03: the workflow, role and checkpoint semantics (§4.3, §5) and the shared allocation (§9). The "evidence" of DEP-08-02-006 and the "scoped feature evidence" of DEP-09-02-015 are named by those rows and not yet defined or produced here: OUT-004 is designed only, and no case has been run (§13) | Not exercised in this increment |
| DEL-02-01 self | Whole contribution | §13 cases |

**New at v0.8 for receivers and suppliers (joins; each side confirms or
objects at the next comparison, V18).**

| Other side | What changes at v0.8 | What that side now needs |
|---|---|---|
| DEL-02-03 EXEC | Carriage and reading order (§3.5–§3.7) replace "representation unselected"; the contract version value (§3.3); FB-20…FB-22; harness capability names (§4.2.5); output production and the designating line (§4.4 OP-1…OP-6); `fresh act required` (§4.3.1 FA-1…FA-5); `on subject absent`; tool local names | §3.2 and EV-1, EV-2 read per §3.7; EV-3 needs a presence rule for the §4.2.5 names, read through the group mapping of HC-7 with HOSTING §8.4's availability signals and observed route limits (HC-4; R14-5); the App-side reached-when table maps OP-2's "completed agent message" to the 0.158.0 item (Wave B node B2); SP-6F cites FA-1 as its take-up element in place of "not defined in this increment (TBD-006)"; §4.7 "Subject absent" cites the element (U-E7); TR-4's manifest fields can be taken from §3.6's members; TF-4 and TF-8 read "contract version" as §3.3's value; §4.14 lists FB-20 (invalid) and FB-21 |
| DEL-05-01 LOOP | §4.4 OP-1…OP-6 answer the R10-8 note in LOOP §2.4.1; the loop reads the JSON block (§3.5) | §2.4.1 kind (b) cites OP-1…OP-6 and drops the note; LP-9's declaration findings include FB-20…FB-22; the §2.4 element table gains `on subject absent` and `fresh act required` |
| DEL-05-02 PANEL | Element readings with their FB codes (§3.7), including FB-20…FB-22 | §3.2 shows the element readings |
| DEL-01-01 HOSTING | Harness capability names (§4.2.5), each with the item kinds it maps at 0.158.0 and, from the RP-3 repair, the HOSTING §8.4 group it resolves to (HC-7; R14-5) | HOSTING closes F-27 by citing §4.2.5's group column (R14-5). HOSTING's grouping of `functionCallOutput`, `mcpServer/elicitation/request` and `thread/shellCommand` stands; WD follows it (HC-6) |
| DEL-03-01 C | `operation` and `versions` carry C's identity and version as C writes them (§3.6) | Where C's own schema writes identity or version other than as a string, the tool reference follows C |
| DEL-03-02 P | `outcome` tokens for P §9's names (§3.6), now P-v0.8's own `item_state` spellings (`applied`; R14-6) | Nothing further for the tokens. WD cites P-v0.8's contributions to arc N-18 (§4.3.6, §4.3.7, and the supplier row below; R14-8); P makes item-left events explicit in its schema (R14-8, node RP-2) |
| DEL-04-01 ACT | FB-03 treats A1…A15 as recognized codes (A15 per R12-5) | ACT confirms A15's code when it adds it |
| DEL-04-03 RS | The revision file set (§6.1 RV-1…RV-5); element readings and FB codes a record may cite | The revision's identity method designation stays with U-03 |
| DEL-03-04 GUIDE | WD-v0.8 and WD-EX-v0.8 by label | GUIDE re-pins last (node B8) |
| DEL-09-06 CA | E1's and E1d's checkpoints are unchanged; both are now rendered in the carriage | Nothing required |

Expected **from** suppliers:

| Supplier | Element | State at v0.5 (R6 in place); DEL-02-03 and SWBPIPE rows updated at v0.6; current sibling versions added by R8-12 item 7; at v0.7 the labels are the Wave A versions (R9-5, R9-11) and the RS, PANEL, LOOP, P and HOSTING states come from direct reading | Used in |
|---|---|---|---|
| DEL-04-01 | Canonical names; closed list; decision pairs; act-declined event; A12 binding, supersession and grant-setting referent; reserved-operation rule | ACT-POLICY-v0.5 at `d3cebd1cc` (header checked; R5-3 unconditional invalidity per V4-A). Current: ACT-POLICY-v0.7 (DEP-02-01-018) | §4.3 |
| DEL-02-03 | Phase-1 statement (§2.1) and governance-phase scope (§2.2); report and hold support (§3.6, governance phase); hold machine (§4): resume point, re-hold, run end, A12 control relation, MX rules, SP-6, recovery; App capture (§5); transfer (§6) | EXEC-v0.4 read in the working tree after its A1 edit (sha256 `d32be377…76d4`); U-E24 closed in place by R8-11 item 2 (R8-12). Current: EXEC-v0.5 (DEP-02-01-026: its statement of the current phase, §2.1, and, for the governance phase, its hold-support values, §3.6; consumed and not defined here, SoW TBD-004) | §4.2.4, §4.3.0, §4.3, §4.3.8, §6.4 |
| DEL-03-01 | Identity/version (equality); element 9 exposure; C §4.1 results; read basis (5 elements); subject content identity; FX-PIPE-01 incl. OP-C10…OP-C12, FXA-1…FXA-5, LIB-A1, LIB-A2, AF-1, editions e1/e2, named variants | C-v0.5 at `d3cebd1cc` (V-GR1 with GR-1…GR-3, GR-P, GR-R, GR-S, run 13). Current: C-v0.7 (DEP-02-01-017) | §4.1, §4.2, §4.3.6, EXAMPLES |
| DEL-03-02 | P §9; change-item content identity; item dispositions, all-decided, item-left events; governing checkpoint constraint; applied-outcome object identities | **At the RP-3 repair (R14-8, arc N-18; DEP-02-01-029, held):** P-v0.8, read directly: change-item content identity §3.1, §3.4, host-assigned §3.5 PM-6 (`item.change_item_content_identity`, `identity_method`); per-item dispositions §4.1, §4.6 PT-1…PT-19 (`item.state`, `item.decision`); all-items-decided §4.3, §4.6 DS-4 (`derived_state.all_items_decided`); item-left events §4.3 (cause, time, evaluated basis; explicit in P's schema per R14-8, node RP-2); applied outcomes with resulting objects §9 (`applied.resulting_objects`, or "not supplied"); outcome tokens `proposal_state.schema.json` `$defs/item_state` (§3.6; R14-6); P §13 "Provide to DEL-02-01". All five contributions are offered (V18-4 J10). Earlier: P-v0.5 at `d3cebd1cc` (header checked; R5-2 per V4-A). P-v0.7, read directly at the v0.7 pass: §3.1 (change-item content identity), §3.3 (governing checkpoint constraint and carriage assurance, governance phase), §4.3 (per-item dispositions, all-items-decided indication, item-left events with their causes), §9 (outcomes; applied-outcome association with resulting objects), §13 ("Provide to DEL-02-01 / DEL-02-03") (DEP-02-01-029, arc N-18) | §4.2.2, §4.3.6, §4.3.7, §4.6 |
| DEL-04-03 | Human-act record with capturing surface, recording mode, capture-evidence reference; events (act-lapsed, act-declined, run-ended) | Read directly at this pass (earlier passes: via IR1-A and R2). Current: RS-v0.7: §4 R2 (identity tuple, holding library, transfer links), R5a (seat role), R8 (checkpoints and arrivals: dispositions, ordinals, bound referents, events, annotations), R9, R14; §6.1 (human-act record: recorder, recording mode, capture evidence references); §7 L-12; §10 DEL-02-01 row (DEP-02-01-019). U-11 closed | §4.3, §4.6 |
| DEL-05-01 | Evaluation and binding; dispatch record with constraint, seat role; run association incl. holding library and supplied guidance | LOOP-v0.5 at `d3cebd1cc` (header checked; LH-n labels per R6-4). Current: LOOP-v0.7, read directly at this pass: §2.4 element table (the loop consumes the full §4.3.1 set), §2.4.0 LP-1…LP-10, §2.4.1 reached-when evaluation, §2.4.2 binding by declared subject class, §6.2 dispatch record, §10.1–§10.2 (DEP-02-01-020) | §4.3.5, §6.2 |
| DEL-05-02 | Panel needs | Read directly at this pass (earlier passes: via IR1-C J2/J3). Current: PANEL-v0.7: §3.2 workflow selection (identity, holding library, declared checkpoints, §4.2.4 outcomes, runnable rule), §3.5 W-5a…W-5g (W-5f cites §4.3.7), §6 allocation account (DEP-02-01-021) | §9 |
| DEL-01-01 | Supplied-guidance identity evidence (HOSTING §8.2); harness capability inventory at 0.158.0; capability account by group (HOSTING §8.4) | **At the RP-3 repair (R14-5):** HOSTING-BOUNDARY-v0.8 §8.4 (HCG-A01…A17 with meanings, availability signals and standing) is the meaning the names resolve to (§4.2.5 HC-7), with its OBS-1 and OBS-1b observations (HOSTING §10.1; R13-6). Earlier: read directly at the v0.7 pass (earlier passes: via IR1-C J6). Current: HOSTING-BOUNDARY-v0.7: §8 closing paragraph (the 0.158.0 inventory of PIN-SPIKE §4 is the input to harness-capability naming; HOSTING chooses no names) and §8.2 (DEP-02-01-025, arc N-16). The inventory is supplied. At v0.8 the harness capability names and their meanings as portable requirements are PROPOSED here (§4.2.5), scoped to pin 0.158.0; HOSTING's per-capability account is expected to key on them (joins above) | §4.2.1, §4.2.5, §6.2, U-08 |
| SWBPIPE owner (external) | Host library; seat conduct; act facility and capture-evidence reference; constraint receipt or own declaration copy; per-turn guidance recording | Relayed; **answered** 2026-09-28 (RELAY_ANSWERS_SWBPIPE.md, read at `6f01add3…`; current `afb6e063…`, R9-5): SQ-01 no capture-evidence reference; SQ-02 route (iv), none planned; SQ-11 no exposure element; SQ-12 no per-operation identity; SQ-17/SQ-18 no workflow library or adaptation; SQ-19 no host loop and no seat concept. These are answers about SWBPIPE's current state, not commitments, contributions or adoption; host joins deferred (DECISION-3) | §5, §6, I-5, I-7, U-05b, U-19, U-29 |

---

## 9. Shared contract/component responsibility map (OUT-003; REQ-005; AC-005)

Columns: consumers and need source; repeated responsibility; maintenance
rationale (d2: local implementations need conformance work; a library couples
releases; a service adds process, availability and upgrade coordination);
candidate (semantic, not a decision); confirmation (actual owner response);
placement. Reviews and comparisons are records, not owner confirmations, so
every Confirmation cell remains "None".

| # | Contract part (semantic owner) | Consumers and need source | Repeated responsibility | Maintenance rationale | Candidate | Confirmation | Placement |
|---|---|---|---|---|---|---|---|
| A-1 | Declared-part meaning (DEL-02-01) | DEL-02-03 (SoW; EXEC-v0.5 §3.2, §4); DEL-05-01 (LOOP-v0.7 §2.4, §2.4.1, §2.4.2; first read as LOOP-v0.2 at `28bd00499`); DEL-05-02 (PANEL-v0.7 §3.2; earlier passes via IR1-C J2); DEL-02-02 (later); host loop/panel (external; none received) | Read the five categories, undeclared/empty states, reached-when and subject class | Divergent readers disagree on undeclared vs empty and on binding (IR1C-01 showed the risk) | Shared declared-part reading type(s) and parser/validator; conformance fixtures regardless. At v0.8 the schema and its conformance instances exist (§3.6; R12-2) and serve any placement | None | `UNRESOLVED{OI-014}` |
| A-2 | Workflow identity tuple, chain and holding library (DEL-02-01) | DEL-02-03; DEL-03-02 (P §3.3 origin); DEL-04-03; DEL-05-01 (run association); DEL-05-02 (PANEL §3.2, IR1C-09); DEL-02-02/02-04 (later); host library (external) | Carry the tuple and holding library; detect collisions; never rebind | Identity drift silently breaks V4-WF-03; a shared type is low-coupling | Shared workflow identity type; collision report meaning | None | `UNRESOLVED{OI-014}` |
| A-3 | Checkpoint declaration meaning (DEL-02-01) with act names (DEL-04-01) | DEL-02-03; DEL-05-01 (LOOP C-1…C-7); DEL-05-02 (PANEL W-5); DEL-04-03; host (external) | Name act kind, reached-when, subject class, validity; apply I-1…I-7; §4.3.7 | Independence rules erode locally; binding by kind vs class already diverged once | Shared checkpoint declaration type; shared negative fixtures | None | `UNRESOLVED{OI-014}` |
| A-4 | Checkpoint hold machine (DEL-02-03). Phase 1: recording only; hold content governance phase (EXEC §2.1, §2.2) | App run (DEL-02-03); host loop (DEL-05-01 receiving; external construction) | Wait/advance/lapse/unknown/re-hold/run end (holds: governance phase) | Shared execution couples App and host loop lifecycles; d2 needs a concrete shared stateful responsibility first | Possibly shared; not proposed | None | `UNRESOLVED{OI-014}`; host side `UNRESOLVED{OI-013}` |
| A-5 | Compatibility outcome vocabulary and pass rule (DEL-02-01) over C identities and exposure (DEL-03-01) | DEL-02-03 (check); DEL-05-02 (PANEL §3.2, IR1C-13); DEL-02-02 (later); host (external) | Report §4.2.4 outcomes and pass truthfully | Vocabulary must match C exactly; checker code may stay local | Shared outcome vocabulary type; checker placement open | None | `UNRESOLVED{OI-014}` |
| A-6 | Role meaning and compatible roles (DEL-02-01; supply DEL-02-04) | DEL-02-04 (later); DEL-02-03; DEL-05-01 (seat role on dispatch); host seat (external) | Name four roles; read compatible roles; report unsupported | Tiny, stable meaning; cheap to share; enforcement stays per harness | Shared role identity set | None | `UNRESOLVED{OI-014}` |
| A-7 | Human-act and run record (DEL-04-03) | All above | Semantic owner is DEL-04-03 | Recorded here to keep the owner visible | Owned by DEL-04-03's allocation | n/a | DEL-04-03 / `UNRESOLVED{OI-014}` |
| A-8 | Catalog entry, exposure and read basis (DEL-03-01) | All above | Semantic owner is DEL-03-01 | As A-7 | Owned by DEL-03-01's allocation | n/a | DEL-03-01 / `UNRESOLVED{OI-014}` |
| A-9 | Host loop use of declarations (external construction; DEL-05-01 receiving) | Host loop (LOOP §2.4, §6.2, §10.1) | Parse the declared part in the host; evaluate reached-when; bind subject class; carry the governing checkpoint constraint and holding library; persist runs | Loop placement, parsing and persistence are host choices | None proposed | None | `UNRESOLVED{OI-013}` |
| A-10 | Panel workflow selection and checks (external construction; DEL-05-02 receiving) | Host panel; possibly App views (PANEL-v0.7 §3.2, §3.5, §6; earlier passes via IR1-C J2/J3) | Present selection, identity, holding library, collisions, pass result, checkpoint requests with purpose/scope and "accept" wording, shared dispositions and item annotations | Reusable components only on agreed repeated purpose (DEL-05-02 OUT-004) | Possibly shared presentational components; not proposed | None | `UNRESOLVED{OI-014}`, `UNRESOLVED{OI-013}` |
| A-11 | Catalog-schema argument checking (DEL-03-01; LOOP §10.2 candidate (b)) | DEL-05-01; host (external); external adapter (DEL-03-03) | Check call arguments against the catalog schema before host domain validation | Pointer row only: held by DEL-03-01 (C §8 map) | Held by DEL-03-01 | None | `UNRESOLVED{OI-014}` |
| A-12 | Governing checkpoint constraint element (DEL-03-02 change request; derived from DEL-02-01 declaration); carriage is governance phase (R8-1) | DEL-05-01 (dispatch), DEL-03-03 (adapter), host route (external) | Derive, carry and evaluate the A5 constraint consistently on every channel | An omitted constraint is indistinguishable from none (R2-12); consistency matters more than code sharing | Shared derivation rule from the declaration; carriage stays per channel | None | `UNRESOLVED{OI-014}` |

Allocation result at v0.7: every row names its consumers and open placement.
**No** common implementation or service is proposed, and no row is
represented as agreed (AC-005).

---

## 10. Excluded acts and their owners (REQ-006; AC-006)

| Act excluded from DEL-02-01 | Owner | Receiving interface in this contract |
|---|---|---|
| Catalog-semantic definition (identity, version, exposure, availability, standing, read basis, content identities, fixture catalogue) | DEL-03-01 | §4.1, §4.2, §4.3.6; EXAMPLES |
| Proposal/outcome definition (P §9, change items, change request incl. governing checkpoint constraint, item-left events, applied-outcome objects) | DEL-03-02 | §4.2.2, §4.3.6, §4.3.7, §4.4, §4.6 |
| Operation-policy definition; canonical act names; carrying adopted D2/D3 | DEL-04-01 | §4.3.1 closed list; §2 S-Q/S-R/S-S |
| Operation-specific reserved additions | Owner via outside SWB session (`UNRESOLVED{OI-021}`) | §4.3.2 |
| Human-act and run-record field definition; record implementation | DEL-04-03 | §4.3.1 expected act evidence; §4.5; §4.6; §5.3 |
| External-channel constraint carriage (governance phase) | DEL-03-03 | §4.2.2 (the constraint and its carriage assurance are derived here; carrying it on the external channel is not); I-7; §9 A-12 |
| Checkpoint hold machine, re-hold, ended-run resumption, required-tool check, transfer; the statement of the current checkpoint phase and, for the governance phase, the hold-support values (SoW TBD-004) | DEL-02-03 | §4.2.4, §4.3.0, §4.3.4, §4.3.7, §4.3.8, §6.4 |
| Loop receiving design (arrival observation, binding step, constraint carriage) | DEL-05-01 | §4.3.5, §4.3.6, §9 A-9, A-12 |
| Panel receiving design | DEL-05-02 | §9 A-10 |
| App workflow workspace and registration | DEL-02-02 (later undertaking, D1) | §6.3 C-4/C-5; §7 |
| Role selection and supply | DEL-02-04 (later undertaking, D1) | §5 |
| Host catalog, domain validation/application, receipts, loop, panel, tables, views, act facility and capture-evidence reference | External SWBPIPE implementation owner | §4.5; I-5; §5.2 |
| Performing marking checked, acceptance, rejection, approval, reliance, grant change, external-access change | The person; professional assertions by the accountable professional | §4.3 (declaration names, never performs) |
| Shared placement decisions | App/shared contract owners (OI-014); with SWB implementation owner (OI-013) | §9 |

---

## 11. Failure behavior (consumer-facing meaning)

| ID | Condition | Required behavior |
|---|---|---|
| FB-01 | Declared part absent or a category omitted | Report **undeclared**; never "none". |
| FB-02 | Declared part unreadable or malformed: not JSON; a duplicate member name; more than one declaration block (§3.5 CR-4); no object envelope or no contract version (§3.7 VO-1…VO-3) | Workflow stays a prose method; declared part **not established**; report the defect; no partial interpretation that could pass a check. An element that alone is malformed is not established by itself, and the rest is read (§3.7 VO-5). |
| FB-03 | Checkpoint names a recognized act kind outside {A4, A5, A6, A7, A12}, or none | **Invalid** checkpoint; report; no execution outcome can satisfy it (R2-10). |
| FB-04 | Checkpoint names an act kind the consumer does not recognize | Preserve; **not established**; never substitute a nearby kind (R2-10). |
| FB-05 | Root `tools` restriction present, required tools undeclared | Required-tool check **not established**; restriction honored as ceiling. |
| FB-06 | Tool reference does not resolve against the current catalog | **missing** (or **not established** if the catalog is unreadable); never dropped. |
| FB-07 | Prose and declared part disagree (e.g., prose describes a human checkpoint the declared part lacks) | Report; do not auto-add or auto-remove a checkpoint. |
| FB-08 | Selected revision no longer resolvable | Report; do not substitute current same-named content; the record keeps the selected tuple. |
| FB-09 | Collision discovered after selection | Report all origins with holding libraries; keep selection (C-2). |
| FB-10 | Output promises approval, certified or unqualified "checked" standing, or labels an A3 examination "host checks passed" | Invalid element (S-L; R-4); report. |
| FB-11 | Declared evidence has no observed counterpart after the run | **missing**; never a pass. |
| FB-12 | Seat role meaning undeterminable | Record **unknown** (SEAT-1). |
| FB-13 | Reached-when names an undeclared tool or output, or is absent; or the reached-when or subject names an element of the wrong kind (§3.7 VO-7; §4.3.1 validity rules) | Invalid checkpoint; the consumer cannot observe or hold on it truthfully and reports it. Governance phase (governed): the run does not proceed past the prose position as if the checkpoint were satisfied. Phase 1: reported; the agent does not treat it as satisfied and manages the pause (§4.3.0). |
| FB-14 | Direct application requested for an operation under a governing checkpoint constraint | Governance phase (governed A5 checkpoint, host-held carriage): **not permitted**, naming the constraint (I-7); no silent conversion to a proposal. Phase 1: no constraint is carried; the host's own treatment of its operations decides; the outcome is recorded as observed. If the host applies directly, no proposal is queued and the A5 checkpoint is **not reached**: nothing is requested by reason of an arrival that did not occur, no A5 is forced, and none is recorded (I-7; R8-11 item 2 and R8-12 item 2, as restated by R9-2 and corrected by R10-1; U-34 closed). |
| FB-15 | Only an agent-authored record, a conversation statement, or a record without a capture-evidence reference exists | Checkpoint stays **waiting** (I-5). |
| FB-16 | A5 checkpoint whose reached-when is not kind (c) *queued*, or whose subject class is not "change items of the named proposal"; or "targets of the held call" with a kind other than (a) | Invalid checkpoint (R2-17; IR1-C X-10); report. |
| FB-17 | A12 checkpoint whose declaration names no setting content | Invalid checkpoint, unconditionally, whatever an A8 at arrival presents (R4-9; R5-3). |
| FB-18 | Governance phase, governed checkpoint: kind (a) on a harness capability in an App run, or any checkpoint whose hold support on the acting surface is *not enforceable* | Workflow **unsupported** on that surface: "checkpoint hold not enforceable on this surface" (R4-8, R4-21). Phase 1: never *unsupported* for this reason (§4.3.0). |
| FB-19 | `governed` or `fresh act required` present with an unrecognized value (PROPOSED, R8-1; R12-10) | Preserve and report (§3.4). Phase 1: guidance, as for any checkpoint. Governance phase: the checkpoint's governance (or its take-up of SP-6F) is **not established**, never assumed either way; it is reported before the run. |
| FB-20 | Two or more elements with one local name in one category, or two message outputs with one designating line (PROPOSED, v0.8; §3.7 DN-1…DN-4) | Report every such element. Checkpoints so named are **invalid**; other elements are **not established**; a reference to any of them is to an element not established. |
| FB-21 | A reference outside a checkpoint's reached-when and subject names an undeclared or unusable element (an input's read-through tool; an output's gating checkpoint, production tools or relied-on tools; evidence `supports`), or evidence `supports` names both an output and a checkpoint (PROPOSED, v0.8) | That element is **not established**; report. |
| FB-22 | The declared part's compatible roles differ from a Root `execution.json` in the same package (PROPOSED, v0.8) | Report both. Compatible roles are **not established**, so the role part of the check is not established: never a pass, and never *unsupported* on that ground. |

---

## 12. UNRESOLVED

| ID | Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|---|
| U-01 | Physical carriage of the declared part | DEL-02-01, with consumer confirmation | Consumer confirmation at the next comparison (V18) | **PROPOSED at v0.8** (§3.5): one fenced block `workflow-declaration` in `WORKFLOW.md`, holding JSON; the options are weighed there. The prototype renders and reads E1, E1d, E5 and E6 in it (§13.1). DEL-02-03, DEL-05-01 and DEL-05-02 confirm or object; until then it is not settled. |
| U-02 | Field names, value encodings, schema language | DEL-02-01 with consumers | As U-01 | **PROPOSED at v0.8** (§3.6): JSON, snake_case members, JSON Schema 2020-12 (`workflow-declaration.schema.json`). Values owned by C (operation identity, version) and P (outcome names) follow their owners; the outcome tokens are P-v0.8's `item_state` spellings (R14-6). The identity tuple is `$defs/workflow_identity` (§3.6). |
| U-03 | Revision algorithm, framing and method designation | DEL-02-01 with DEL-04-03 (and HOSTING U-08) | Before revision comparison claims | Meaning defined, with identity method designation. The file set and canonicalization are stated at v0.8 (§6.1 RV-1…RV-5); with the algorithm open, comparison is untestable except by the prototype's illustration. |
| U-05 | Operation-specific reserved additions: `UNRESOLVED{OI-021}` | Owner via outside SWB session with App/shared owner | Before connected-activity SoW | D2 list applies; additions not assumed. |
| U-05b | Host capture-evidence reference per act kind (relay question, R2-20) | SWBPIPE owner decision (PB-TBD-002; DEL-16-03 actor identity; ANS §2) | Before host act-recording integration | Without it no host-content checkpoint can be *performed* (I-5). SQ-01 answered: no durable reference; no person identity or time, even in DRAFT #885. |
| U-05c | *Closed (DECISION-K1 K1-3, 2026-09-30).* Multi-row A4 purpose after partial lapse | The owner (decided; was DEL-04-01 with Owner, DEL-04-01 U-03, carried to C1) | — | **Settled.** An act on the lapsed referents alone answers the checkpoint together with the earlier act for the unchanged referents; each cites its items (I-4 joint answer; EXEC §4.7 JA-1). EXEC CH-8 released. |
| U-07 | Operation version ordering or range | DEL-03-01 (C §3.2, U-C9) | Before DEL-02-03 required-tool fixtures | Exact-version equality only. |
| U-08 | Portable naming of harness capability requirements | DEL-02-01 with DEL-01-01 (0.158.0 inventory, HOSTING §8) and DEL-02-03 | Before App-side required-tool check | Class defined. The supplier of meaning is DEL-01-01 (SoW REQ-002; §4.2.1). **Names PROPOSED at v0.8** (§4.2.5), scoped to Codex pin 0.158.0, each resolved to one HOSTING §8.4 group (HC-7; R14-5); presence in the check is EXEC's, through that mapping (HC-4). Register row DEP-02-01-025 answers V1-C RF-7. |
| U-09 | Host single seat → role meaning mapping (options in SEAT-2) | DEL-02-01 with SWB implementation owner and DEL-02-04 | Before host role-guidance supply and host receiving fixtures | SEAT-1…3 hold for any option. SWBPIPE: no seat concept; its UX design has one agent panel, the likely counterpart; not decided (SQ-19 (d); R8-8). |
| U-10 | Host origin in unqualified precedence; whether a selection follows new revisions | DEL-02-02 (later undertaking) with DEL-02-01 and host owner | Before host-origin discovery in App | Correctness rests on source-qualified selection. |
| U-11 | *Closed at v0.7 (R9-8; record: RS, read directly).* Record fields for identity tuple, holding library, seat role, checkpoint disposition and events, bound referents, capturing surface | DEL-04-03 | — | **Supplied as meaning.** RS-v0.7 §4 R2 (identity tuple; holding library at listed, selected and resolved), R5a (seat role), R8 (disposition per arrival, events, bound referents with their content identities), R9; §6.1 (recorder, recording mode, capture evidence references from the capturing surface). RS's elements are semantic; record fields stay RS's (U-02 at v0.8 covers the declared part only). |
| U-12 | Placement of shared parts: `UNRESOLVED{OI-014}` | App/shared contract owners | Before structural/production contract allocation | Map rows exist; no placement proposed. |
| U-13 | Host loop placement/parsing/persistence and panel assembly: `UNRESOLVED{OI-013}` | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Rows A-4, A-9, A-10. |
| U-14 | Guidance distribution/adoption: `UNRESOLVED{OI-018}` | Owner with shared/project instruction owners | Before instruction changes or dependent supply | Readability required; distribution not decided. |
| U-15 | First connected operation, autonomy and environment: `UNRESOLVED{OI-021}` | Owner via outside SWB session and App/shared owner | Before connected-activity SoW | Fixture operations are FX-PIPE-01 entries, not the selected operation. |
| U-16 | Automatic catalog extension: `UNRESOLVED{OI-003}` (App v4 OI-003; unrelated to SWBPIPE's OI-003) | Owner with host contract owner | Before claiming extension capability | Never assumed. |
| U-17 | Owner confirmations for §9 rows; SWBPIPE consumer needs | DEL-02-03, DEL-05-01, DEL-05-02, DEL-03-02 (this undertaking); DEL-02-02, DEL-02-04 (later); SWBPIPE owner via relay | Next comparison (internal); relay (external) | Every row "None". Internal half, as a request: DEL-02-03, DEL-05-01, DEL-05-02 and DEL-03-02 are each asked to **confirm or object**, per §9 row that names them, at the next comparison. Their Design files state what they consume (EXEC §9.1 DEL-02-01 row; LOOP §2.4, §10.1; PANEL §3.2, §6; P §13); that is a record, not an owner confirmation. The SWBPIPE half waits with the host joins (DECISION-3). |
| U-19 | Relay question SQ-02 (R2-12, R4-14, R5-2): can the host hold the constraint (*host-held*: derived from, or verified against, its own resolved copy of the declaration), and hold host-operation checkpoints for App runs? Which evidence shows which? **Answered 2026-09-28: route (iv), none planned**; a constraint field would be refused as unknown (SQ-02 (a)) | SWBPIPE owner decision to plan any route (ANS §2); DEL-03-02 defines the element | Before governance-phase host-side fixtures and LOOP FX-C9 / PANEL PC-24 / VC-11 | Phase 1: I-7 holds as plan guidance; no constraint carried by the App. Governance phase: VC-11 **AWAITING INPUT** — SQ-02 answered: no receipt, no host copy (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3). Host-operation checkpoints in App runs are *not enforceable*: SQ-02 answered 2026-09-28, none (§4.3.8). |
| U-23 | Real per-surface exposure agreement (the fixture uses C FXA-1, "exposed ×3", with variant V-X1) | DEL-03-01 (C §8 map) with host owner; `UNRESOLVED{OI-003}` (App v4 OI-003) | Before exposure claims | Fixture values supplied by C; real exposure open; in the governance phase unagreed exposure makes hold support *not established* (R5-1), except where SQ-02 is answered with no host-held route (R8-2). SWBPIPE: no exposure element (SQ-11). |
| U-25 | *Closed (DECISION-K1 K1-4, 2026-09-30).* Construction of the App act control and App person identity (requirements in EXEC §5 CAP-1…CAP-9) | The owner (decided); construction DEL-01-04 (later undertaking, D1) | — | **Identity settled:** the App records the name set in the App, the operating-system account and the Codex account when Codex reports one, marked *identity not verified*; a verified identity is a governance-phase matter (EXEC CAP-8). **Control:** construction stays with DEL-01-04; its obligation is proposed for DEL-01-04's contract at the next amendment (DECISION-K1 K1-4); collected at this run's closeout. App-side positive capture cases stay AWAITING INPUT on the control. |
| U-30 | App-side run holds `UNRESOLVED{D6}`. **Closed for Phase 1** by DECISION-4 D4-1 (R8-2); re-opens only when the governance phase is taken up. SQ-02 decides only checkpoints whose held actions are all **host operations** (HS-3), and SWBPIPE answered it (route (iv)); checkpoints holding any **App-side** step (HS-5) stay *not enforceable* whatever SWBPIPE answers (R5-10) | Owner (DECISION-4; D6 re-opens with the governance phase); DEL-02-03 with DEL-03-03 for any App hold point | When the governance phase is taken up; before any governed App-run checkpoint case is claimed held | Phase 1: none (§4.3.0). Governance phase, App runs: HS-3 checkpoints *not enforceable* (SQ-02 answered 2026-09-28, none), HS-5 checkpoints *not enforceable*; action during hold recorded (§4.3.8, I-9). |
| U-31 | *Closed (DECISION-K1 K1-2, 2026-09-30).* Capture-after-arrival (I-8) versus counting a prior act bound to current content (EXEC U-E4) | The owner (decided) | — | **Settled for the current phase:** an earlier act of the required kind on current content counts, cited with its time (I-8; EXEC SP-6). Capture after arrival is kept as a governance-phase option (EXEC SP-6F, PROPOSED). EXAMPLES R-9b, R-12b and R-16 (i) recomputed. |
| U-32 | *Decided at v0.8 (PROPOSED).* Whether a declaration carries an "on subject absent" path (EXEC U-E7) | DEL-02-01 | — | Yes: the optional element **on subject absent** (§4.3.1), plan guidance. The disposition stays *waiting* "subject absent"; an act-declined event resolves it or the run ends. |
| U-29 | Per-turn supplied-guidance source and content identity in host loops (relay question, R2-20) | Host owner (DEP-001) via W9; DEL-05-01 element | Before host supplied-link evidence | Where absent, *supplied* is **unknown**, never inferred from configuration. |
| U-33 | *Closed at v0.7 (R9-1; R9-8).* The phasing of V4-WF-05's hold (DECISION-4 D4-1; R8-1) awaited an update of the accepted basis | Owner | — | **Done.** SCA-V4-001 (accepted 2026-09-29; `_ScopeChange/SCA-V4-001_2026-09-28_2155/`) amended PRD V4-WF-05, HOST_INTEGRATION V4-HI-42 and EXAMINATION V4-EXM-22. §4.3.0 quotes the first two. In force in every phase: the act is requested; it is recorded as done only when the person performs it; the reserved acts bind. Phased to the governance layer: holding the run until the act. |
| U-34 | *Closed in place (R8-11 item 2; R8-12 item 7; with EXEC U-E24).* Phase-1 standing of I-7 (an acceptance checkpoint forces a proposal), V4-HI-42 and DECISION-1 D2's "or a declared checkpoint" clause (EXEC F-30) | Integrator (INTEGRATION, R8-11 item 2); the reading was confirmed by the owner (`APP-V4-BASIS-ALIGN-20260928` DECISION-7, OWNER_ITEMS O-25) and is restated against the amended text by R9-2 (DERIVED) | — | **Settled.** D2's "no autonomy grant widens past a reserved act" binds, and the host enforces it through its operations. For a declared checkpoint, V4-HI-42's request clause and record clause are in force whatever the autonomy setting; whether the run goes on before the act is for the person and the agents in the current phase, and the host's own treatment of its operations decides what the host does. The forced treatment of I-7 binds only for governed checkpoints in the governance phase. I-7 and FB-14 read as plan guidance in the current phase; reserved acts stand (§4.3.0 CG-5). |
| U-35 | Per-subject content identity (V4-HI-32) not met by SWBPIPE, which supplies only a whole-model identity (SQ-03; R8-4; EXEC U-E25) | SWBPIPE (PB-TBD-002 / DEL-16-03); owner notice | Before host act-binding integration | SB-3 note: the whole-model identity is received for every covered subject, so acts over-lapse and never under-lapse. |

Closed since v0.3: U-18 (transfer procedure: EXEC §6.3–§6.7), U-20 (item rule confirmed, R4-7), U-21 (no resumption; continuation, R4-4), U-22 (re-hold, R4-3), U-24 (holding library confirmed, EXEC §6.2), U-27 (refused A12, R4-6) — each PROPOSED (W7) where EXEC marks it so.
Decided at v0.8 (PROPOSED): U-32. Closed at v0.7, node A3 (DECISION-K1): U-05c (K1-3), U-25 (K1-4), U-31 (K1-2). Closed since v0.2: U-26 (fixture identifiers; now C §10 plus R2-21); U-28 (subject class for examined objects; R3-1).
Earlier closed: U-04 (names, R-1), U-06 (classifier permissions, D3).

---

## 13. Verification cases (designed, not run)

None has been executed against a consumer or a host, and no product parser
exists; at v0.8 a design prototype read the declaration part of some cases
(§13.1). Inputs are the
fixture examples in EXAMPLES (FX-PIPE-01 material, invented). Labels:
DESIGNED, or **AWAITING INPUT** where a named external input is required
before the case can be run.

| Case | Serves | Input | Expected result |
|---|---|---|---|
| VC-01 Four roles and host seat | VER-001 (AC-001) | E1 read in App and host single-seat contexts | Same four role meanings; host needs no role-selection UI; seat role recorded or **unknown**. |
| VC-02 Host-owned library | VER-001 (AC-001) | E3 adapted host workflow plus host `SKILL.md`/`AGENTS.md` | Origin *host* and its source root; all files readable as text. |
| VC-03 Five categories recovered | VER-002 (AC-002) | E1 | Every input (incl. five-element basis requirement), tool reference, checkpoint (reached-when, subject class, scope, purpose), output and evidence item recovered; prose intact. |
| VC-04 Undeclared vs empty | VER-002 (AC-002) | E5; variant declaring "no checkpoints" | E5 → all **undeclared**; variant → checkpoints **declared empty**. |
| VC-05 Tool references stay opaque | VER-002 (AC-002) | E1 references vs C §3/§10 | Each compared with C OP-C1/C3/C4/C5; no wire field invented. |
| VC-06 Restriction not requirement | VER-002 (AC-002) | E6 | Required-tool check **not established**; restriction retained. |
| VC-07 Success is not an act | VER-003 (AC-003) | E2 R-1 | `CP-accept` **waiting**; items *queued*; a consumer reporting "accepted" is incompatible. |
| VC-08 Independent A4 without acceptance | VER-003 (AC-003) | E1b | `CP-review` **performed** on its own capturing-surface evidence for the examined rows; no prior A5 required (I-3). |
| VC-09 Distinct acts | VER-003 (AC-003) | E2 R-3 | `CP-accept` **performed**; `CP-check` **waiting** after arrival (I-1). |
| VC-10 Lapse sequence | VER-003 (AC-003) | E2 R-4 (i)–(iii); T14 control | (i) before resume: act-lapsed event; `CP-check` **waiting — lapsed at ‹t›**. (ii) after resume, run live: *Phase 1:* act-lapsed event recorded, labelled **act lapsed at ‹t›** (R8-12 item 1); `checked-rows` standing *lapsed*; nothing re-held or stopped; the agent re-requests as its plan requires. *Governance phase (governed):* **waiting — re-held, lapsed at ‹t› after resume**; next action stopped; nothing undone; `checked-rows` standing *lapsed*; whole scope re-requested. (iii) after run end: **lapsed** for the edited object only. T14 edit to S-2 lapses nothing bound here (SB-3). A5 not lapsed by application and never re-held. |
| VC-11 Acceptance checkpoint forces proposal | VER-003 (AC-003) | E2 R-5a/R-5b (C V-CP1), R-5c (C T15–T16) | *Phase 1:* no constraint carried by the App; the agent proposes as plan guidance (I-7); a direct request, if made, is decided by the host's own treatment and recorded as observed; if the host applies directly, no proposal is queued, so `CP-accept` is **not reached**: nothing is requested by reason of an arrival that did not occur, no A5 is forced, and none is recorded (R8-11 item 2 and R8-12 item 2, as restated by R9-2 and corrected by R10-1; U-34 closed). *Governance phase (governed `CP-accept`):* **AWAITING INPUT** (R2-12; U-19) for host-side evaluation — SQ-02 answered 2026-09-28: no receipt, no host copy (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3). Designed: R-5b direct request → **not permitted** naming the constraint and its carriage assurance; nothing applied; no conversion. R-5a the agent separately submits a proposal; `CP-accept` waits. A model-supplied constraint alone does not satisfy R2-12. R-5c (E1c) direct application under ⟨set-2⟩ proceeds with origin/undo; `CP-check` waits for A4 on S-4. |
| VC-12 Closed act list | VER-003 | Variants of E1 naming A2 apply, A3 examine, A14, V4-CON-05 approval, and an unknown name | Recognized kinds → **invalid** (FB-03); unknown name → **not established** (FB-04). |
| VC-13 Collision without rebinding | VER-004 (AC-004) | E4 | All origins exposed with holding libraries; selection keeps its tuple; only explicit reselection changes it. |
| VC-14 Adapted revision | VER-004 (AC-004) | E3 adapted row | New identity with derived-from = original tuple; original unchanged. |
| VC-15 Promised vs observed | VER-004 (AC-004) | E2 R-6 | **outcome unknown** attributed to the observer; `EV-receipt` **missing**; `CP-accept` **unknown** (deciding observation lost), never performed. |
| VC-16 Reserved operations | VER-003, VER-004 | E2 R-10 | Agent call to OP-C6 → **not permitted** (reserved, DERIVED R2-2); an A8 request is *offered*, not recorded automatically (R2-4); `CP-check` stays **waiting**. |
| VC-17 Map rows name consumers | VER-005 (AC-005) | §9 | Every row has consumers, responsibility, rationale, confirmation "None" and placement; no row marked agreed. |
| VC-18 Excluded acts mapped | VER-006 (AC-006) | §10 vs SoW REQ-006 | Every excluded act with owner and interface; host-vs-person distinction present. |
| VC-19 Fixture inventory bound to candidate | VER-007 (AC-007) | WD-v0.8, WD-EX-v0.8 | Inventory VC-01…VC-56 with candidate identity (WD-v0.8, WD-EX-v0.8); all DESIGNED or AWAITING INPUT, with the declaration parts the prototype ran (§13.1); missing inputs listed; no joined host witness claimed. |
| VC-20 Reached-when not observed | VER-003 | E2 R-7′ | `CP-accept` **not reached**; never performed. |
| VC-21 Subject binding | VER-003 | E2 R-8 | A5 on another proposal's item → `CP-accept` stays **waiting** (SB-2). |
| VC-22 Capturing surface | VER-003 | E2 R-9 (i)–(iii) | (i) agent-authored record → **waiting**. (ii) faithful App record citing the host capture-evidence reference → **performed**; recorder ≠ decision actor. (iii) host exposes no capture-evidence reference → **waiting** (I-5; U-05b). |
| VC-23 Negative decisions | VER-003 | E2 R-11, R-12 | R-11: A10 on all items → **resolved negatively**; on-negative path. R-12: act-declined event (A4) → **resolved negatively**; never performed. |
| VC-24 Mixed items | VER-003 | E2 R-2 (T11) | **resolved negatively** with per-item annotation "partial: item 1 A5, item 2 A10"; item 1 proceeds to RC-1 (§4.3.7). |
| VC-25 Exposure outcomes | VER-002 | E7 | *missing*, *not exposed on this surface*, *channel not enabled*, *not established* and *present, currently unavailable* reported distinctly; pass rule applied. |
| VC-26 Carried unadapted keeps origin | VER-004 | E3 unadapted row | Tuple unchanged; holding library recorded at listed/selected/resolved; no "App-origin" value. |
| VC-27 Stale after acceptance | VER-003 | E2 R-14 | Item shown "accepted by Engineer A — not applied: refused — stale (both bases)"; A5 not lapsed; checkpoint disposition unchanged; output not produced for that item. |
| VC-28 Tool permission is not an act | VER-003 | E2 R-15 | A14 settles tool execution only; no checkpoint disposition changes (S-R). |
| VC-29 Invalid A5 combinations | VER-003 | Variants of E1 `CP-accept`: kind (a); kind (b); subject class "objects changed by a named outcome"; held-call targets with kind (c) | Each **invalid** (FB-16). |
| VC-30 Declared class, not kind | VER-003 | E1 `CP-check` (kind (b), class "objects changed by a named outcome") | Binding uses the applied objects' post-application subject content identities, not the examination output's content (IR1C-01). |
| VC-31 Run end and continuation | VER-003 | E2 R-12b | Run-ended event; `CP-check` final **waiting**; a later A4 is shown "after run end" and changes nothing; a continuation run (*continues ⟨run⟩*) inherits no arrival or disposition; at its own arrival that A4 counts for any bound referent whose content is still the one it was made on, cited with its time, and any other bound referent needs a new act (R4-4, I-8; under the governance-phase option it is "prior act not counted — captured before arrival (governance-phase option)"). |
| VC-32 A12 rules | VER-003 | E2 R-16 (i) main order; (ii)–(v) C V-GR1 (E1d) | T15's A12 precedes arrival, ⟨set-2⟩ still in force → **performed** by that earlier act, cited with its time (I-8; under the governance-phase option: "prior act not counted — captured before arrival (governance-phase option)", **waiting**); A12 after arrival established → **performed**; later established A12 supersedes (stays performed, shown); refused A12 → **waiting**, does not supersede; pending → **waiting**; lost confirmation → **unknown** (R4-5, R4-6). |
| VC-33 Pass rule | VER-002 | E7 variants; E8 | *Phase 1:* pass when every required reference is present or present-currently-unavailable and the workflow is not unsupported (role, delegation); no checkpoint enters the result. *Governance phase:* also no governed checkpoint's hold support is *not established*, and none is *not enforceable*. Undeclared stays selectable, never "runnable". |
| VC-34 Retry de-duplication | VER-004 | E2 R-13 (T13) | Resubmission of PR-2 returns its recorded state (RC-1) and is never refused stale by its own effect; if unobservable, **outcome unknown** by the observer. |
| VC-36 Objects a named output concerns | VER-003 | E1b; E2 R-E1b′ | `CP-review` binds S-2 and S-3 (the rows the OP-C3 findings name) through their subject content identities as read at B1; an A4 on the findings output itself, or on S-1, does not satisfy it; T6's S-3 edit lapses only S-3 (R3-1). |
| VC-37 Checkpoints per surface: Phase 1 and governance phase | VER-001, VER-003 | EXAMPLES E8 | **Phase 1 (R8-1):** no hold-support value on any surface; E1 on E and E1, E1c and E1d via X pass on required tools and channel state (FXA-1, channel enabled); no *unsupported* for a hold reason; no hold by the App or the host loop; acts recorded only when performed; actions after an arrival may carry "continued past ‹checkpoint› before ‹act›". **Governance phase (checkpoints read as governed):** embedded host run (HS-2): every checkpoint **enforced by the host loop** → passes (subject to host evidence; SWBPIPE has no host loop, SQ-20). App run via X: E1 `CP-accept` (held: OP-C4/OP-C5) HS-3 (c) **not enforceable** (SQ-02 answered 2026-09-28), `CP-check` (held: Return) HS-5 **not enforceable** → **unsupported** ("…: CP-accept, CP-check"); E1c `CP-check` HS-5 → **unsupported**; E1d `CP-grant` (held: OP-C9 call) HS-3 (c) **not enforceable** plus E1c's `CP-check` HS-5 → **unsupported** ("…: CP-grant, CP-check"). If run anyway, arrivals record their value and actions while waiting are "action during hold"; no App hold claimed (R5-1, R6-1, R6-3, R8-2). |
| VC-43 Held actions decide the value (governance phase) | VER-003 | E8 variant L-WDEX-17 | **Phase 1 (R8-1):** in every variant the held actions are plan guidance only; no value is assigned; the check passes on required tools and channel state (OP-C9 present). **Governance phase (`CP-grant` read as governed):** declared with "held actions: host operations only (OP-C9)" in an App run on X → HS-3 (c) **not enforceable** (SQ-02 answered, no host-held route); *enforced on the host route* only with a host-held route evidenced → workflow **unsupported** ("checkpoint hold not enforceable on this surface: CP-grant"). The same checkpoint with an App-side step → HS-5 **not enforceable** (R6-1; EXEC F-28). The same checkpoint with **no held-actions element** → held actions derived as the held OP-C9 call (kind (a); §4.3.1, R7-3) → HS-3 (c) **not enforceable**, and its workflow result follows EXEC §3.5 precedence with the run's other checkpoints (L-WDEX-17 has none: **unsupported**). |
| VC-38 Harness-capability kind (a) | VER-003 | E8 variant | *Phase 1:* the harness-capability reference is *not established* (U-08), so the check is *not established*; no hold reason. *Governance phase (governed):* kind (a) on a harness capability in an App run → *not enforceable*, **unsupported** (FB-18; R4-21). |
| VC-39 Earlier acts | VER-003 | E2 R-9b | An A4 captured before its arrival on content still current counts, cited with its time; an earlier act on content no longer current or of another kind → "prior act not counted" with that reason (I-8). Under the governance-phase option: any earlier act → "prior act not counted — captured before arrival (governance-phase option)"; order not establishable → "act order unknown"; neither counts. |
| VC-40 Mixed-item additions | VER-003 | E2 R-6b, R-7b, R-13b | MX-3 lost decision → **unknown**; MX-6 all items left (A11 withdrawal) → arrival closed "replaced by arrival n+1" at the next *queued*; MX-8 application outcome unknown after A5 (V-OU1) → disposition unchanged, annotated (R4-7). |
| VC-41 A12 without setting content | VER-003 | E1d variant | A12 checkpoint naming no setting content → **invalid**, unconditionally, even with an A8 presenting a setting (FB-17; R4-9; R5-3). |
| VC-42 Elicitation is not act evidence | VER-003 | E2 R-9 (iv) | An answer to a Codex user-input/MCP elicitation request ("yes, accept") → `CP-accept` stays **waiting** (R4-12). |
| VC-35 Undo lapses normally | VER-003 | E2 R-17 (T16a, T17) | RC-3 *reverses RC-2*; T16a's A4 bound to ⟨S-4@r16⟩ lapses (FXA-2 covers the label) per I-4. |
| VC-44 Phase-1 guidance semantics | VER-002, VER-003 | E1, E1c, E1d, E2 runs, E8 (Phase-1 columns) | Every checkpoint is read with all §4.3.1 fields; no hold-support value appears; no workflow is *unsupported* for a hold reason; no App or host-loop hold, block or re-hold; acts recorded only when the person performs them, never by an agent on the person's behalf; reserved operations stay the person's and host refusals are recorded as observed; arrivals, acts and lapses appear as observation; "continued past ‹checkpoint› before ‹act›" is optional and never a defect (§4.3.0; R8-1). |
| VC-45 `governed` flag | VER-002, VER-003 | Variants of E1d: `CP-grant` with `governed: yes`; absent; an unrecognized value | Phase 1: all three are plan guidance with identical results (flag shown). Governance phase: `yes` → hold support per §4.3.8 enters the check; absent → guidance, no value; unrecognized → preserved and reported, governance **not established** (FB-19). |
| VC-46 Carriage extraction | VER-002 (AC-002) | WD-EX E1, E1d rendered; E9 L-WDEX-34…L-WDEX-36 | One block read and parsed; the round trip equals the fixture; two blocks → FB-02; a duplicate member → FB-02; a quoted block is not read; the Python and node extractors give the same JSON (§3.5). |
| VC-47 Schema and conformance instances | VER-002 (AC-002) | `workflow-declaration.valid.example.json`, `workflow-declaration.invalid.example.json`; E1b, E1d, E1e | The valid instances validate; the invalid one fails with its nine errors and is read element by element, not rejected whole (§3.6, §3.7). The identity definition `$defs/workflow_identity` accepts the valid instances of `prototype/fixtures/workflow-identity.examples.json` and rejects each invalid one with its named error (RP-3 repair). |
| VC-48 Reading order and names | VER-002 | E9 L-WDEX-22, -23, -25, -29, -30, -32, -33a/b, -42 | Readings as §3.7 states: FB-20; FB-13; §3.4; FB-10; FB-21; top-level member preserved; unknown version not established. A file output without `path` (L-WDEX-42): the output not established (FB-02) and the kind (b) checkpoint on it not established (VO-5, VO-7; RP-3 repair). |
| VC-49 Message designation | VER-002, VER-003 | E1 `examination-report`; E9 L-WDEX-24, -37, -38; WD-EX E2b R-19 (vi) | Declaration: a message output without its line, or sharing one, is not established, and a checkpoint on it is not established; kind (b) on a workflow-input output is invalid. Run: production is observed only from a completed message whose first non-empty line is the declared line (OP-1…OP-4). |
| VC-50 Harness capability names | VER-002 | WD-EX E1e `write-package`; E9 L-WDEX-31; E8 L-WDEX-15 | A §4.2.5 name is read; an unrecognized name is not established; in the check a harness capability stays *not established* until EXEC EV-3 has a presence rule (HC-4). Each name resolves to the one HOSTING §8.4 group its row names, and every supplier name the row cites is a member of that group (HC-7; R14-5). |
| VC-51 Fresh act required | VER-003 | E9 L-WDEX-27a, -27b; WD-EX E2b R-19 (v) | Declaration read as FA-1…FA-3. Run: current phase, SP-6 (an earlier act on current content counts); governance phase with `governed`, SP-6F. |
| VC-52 On subject absent | VER-003 | E9 L-WDEX-28 with EXEC CH-24 | Declaration read; the arrival stays *waiting* "subject absent" whatever path is declared. |
| VC-53 A6 checkpoint | VER-003 (AC-003) | WD-EX E1e `CP-approve`; E2b R-18 | Performed only on A6 evidence from its capturing surface, bound to the current file content; agent text, an A4 or a decline never performs it; a rewrite of the file lapses it. App capture AWAITING INPUT (the act control, DEL-01-04). |
| VC-54 A7 checkpoint | VER-003 (AC-003) | WD-EX E1e `CP-rely`; E2b R-19 | Performed only by A7 of the accountable professional; another actor, an A6 or agent text never performs it; an earlier A7 on unchanged rows counts (I-8). |
| VC-55 Input kinds | VER-002 | WD-EX E1e | `design-criteria` (file supplied) and `review-findings` (the output `findings` of E1b's workflow) read with their sources (§4.1). |
| VC-56 Revision file set | VER-004 | WD-EX E1 rendered as a package | RV-1…RV-5: stable over re-reads; any byte change changes it; a symbolic link makes it not established. The digest is an illustration (U-03). |

Limit: passing these later would show local contract/fixture conformance
only. It would not establish host implementation, round-trip execution,
adoption or any human act (SoW VER-007).

### 13.1 What each case needs to run, and what the prototype ran (R12-1)

The design prototype [`prototype/wdproto.py`](prototype/README.md) (R12-3;
not product code) was run on 2026-09-30 as `python3 wdproto.py selftest`,
with Python 3.13.7 and node v24.5.0: 54 checks, 54 passed. The command and
its full output are in `WAVE_B/B1.md` of this run. After the RP-3 repair
(R14-5, R14-6; V18-2 m-2, m-9) it was rerun on 2026-09-30 with the outcome
token `applied` in the schema and fixtures together, the new L-WDEX-42, the
identity instances (S-10) and the name-to-group check against HOSTING §8.4
(S-11): 62 checks, 62 passed (`WAVE_B/RP-3.md`). The prototype reads
declarations only; it runs no check, arrival or act.

| Cases | Needs to run | At v0.8 |
|---|---|---|
| VC-03, VC-04, VC-06 (declaration verdicts), VC-46, VC-47, VC-48, VC-55, VC-56 | The declaration reader and the schema | **Ran** (prototype S-1…S-10) |
| VC-12, VC-29, VC-41 | The reader, for the declaration verdict | **Ran** (S-7), except VC-12's V4-CON-05 variant, which has no act code to write |
| VC-45, VC-49, VC-50 (with S-11, the group mapping), VC-51, VC-52 | The reader for the declaration part; for the run part, EXEC's recording machine (App) or a LOOP test double (host) driven by C §10's timeline | Declaration part **ran** (S-4, S-7); run part DESIGNED |
| VC-05 | The reader, and C's catalog fixture (§10.2) as data | References read as opaque strings (**ran**); the comparison with C's entries waits for C's catalog instance (Wave B) |
| VC-07…VC-11, VC-15, VC-16, VC-20…VC-24, VC-27, VC-28, VC-30…VC-32, VC-34…VC-36, VC-39, VC-40, VC-42, VC-53, VC-54 | EXEC's recording machine or a LOOP test double over C §10's timeline, with an act-capture double (a host act facility; for App content the App act control, DEL-01-04's, AWAITING INPUT) | DESIGNED |
| VC-25, VC-33, VC-37, VC-38, VC-43, VC-44 | EXEC's compatibility report over a catalog-edition double (C) | DESIGNED |
| VC-01, VC-02, VC-13, VC-14, VC-26 | Library and selection doubles (DEL-02-02, later) and a host library (external) | DESIGNED |
| VC-17, VC-18, VC-19 | Inspection of this file | Inspection (VC-19's inventory updated at v0.8) |
| VC-11 (governance phase, host side) | SWBPIPE host evidence | AWAITING INPUT (U-19) |
