# Record Semantics
- Contribution: DEL-04-03/RS-v0.8 (supersedes RS-v0.7, last changed at `c896a99d90` and unchanged at `86cafc0e1c`, sha256 1ccefbb2948d3c500b3692638a3d4e0c6c9da9a29f9b3e7ea6e8185173dbece9; RS-v0.6, last changed at `caa4334ca1` and unchanged at `3dd7c22c73`, sha256 96b1aeeb120be597c4f35eea13f6a60ce20783e555c918521aacee38c5bcf666; RS-v0.5, last changed at `c6f81a4f2` and unchanged at `94aa9181b`, sha256 2939eb092839a5d6984c984a2aedcb6308f1776276314a79fa1e8edc67c36398; RS-v0.4 sha256 56806b64b12a946e706ff236dd1c25fe27ac00877aac13b50ee8603aaf540199 at `cc58211c5`)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Phase (R8-1; R9-1): in the current phase (Phase 1) declared checkpoints are **plan guidance**. The record keeps arrivals, acts and lapses as **observation**, records an act only when the person performed it, and records no hold, re-hold or hold-support value (element R8). **In force in every phase:** the act is requested; it is recorded as done only when the person performs it; the reserved acts bind. **Phased to the governance layer:** holding the run until the act (PRD V4-WF-05 and HOST_INTEGRATION V4-HI-42 as amended by SCA-V4-001; §1). Hold support, re-hold and *action during hold* are kept as the **governance-phase definition (retained)**.
- Network destinations (R8-13; DECISION-5): element **R15** records, for a host's agent, each destination contacted (destination, category, and the grant or list entry that allowed it), each destination grant (scope, time, source) and each destination requested; a decline and a boundary refusal are recorded too, and that recording is **PROPOSED** (R12-10: V4-HI-70 and V4-ARC-12 record destinations contacted; V4-EXM-23 reports a decline to the agent; no accepted text says a decline or refusal is recorded). An outside process is recorded with its declared destinations and, when it is not sandboxed, the evidence limit "process network not observed" (R11). V4-HOST-02 is cited from the PRD as amended by SCA-V4-001, which applies DECISION-5 (D16). R15 is within the ScopeOfWork inventory (REQ-002, CLM-002) and V4-HI-70 as amended. From v0.8 (node B5) R15's elements follow the one destination flow of DEL-05-01/LOOP-v0.8 §5.3 (DF-1…DF-10): a request carries its call, ends in one of the DF-6 states (`destination_request_closed` for *not granted* and *unanswered at end*), a refusal names its stage, a model-service contact its class local or cloud, and an MCP server its stateless evidence with the R11 limit "stateless revision declared, not verified".
- Record format (Wave B; R12-1…R12-3): a **PROPOSED** format, `RS_RECORD.schema.json` beside this file, with valid and invalid example instances and writer and reader sequences with their failure behaviour (§13, §14), backed by a local prototype in `prototype/` that writes records and reads them back (§15). Nothing in it is accepted, and no placement, path, identity algorithm or canonicalization is chosen (OI-013, OI-014; DEL-03-01 TBD-003; R12-2).
- Serves: OUT-001 and OUT-004 (definition content; OUT-001's format PROPOSED in §13); OUT-002 and OUT-003 (behaviour and fixture design only — the writer and reader in `prototype/` are a prototype, not product code, and no fixture has run against a candidate); REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006; AC-001…AC-007 via designed VER-001…VER-006
- Basis (re-pinned at v0.7; R9-5): the accepted basis as amended by SCA-V4-001 (`P/execution/_ScopeChange/SCA-V4-001_2026-09-28_2155/`) and SCA-V4-002 (`P/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/`), by current sha256: `P/docs/PRD.md` bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd, `P/docs/ARCHITECTURE.md` 317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c, `P/docs/HOST_INTEGRATION.md` d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f, `P/docs/EXAMINATION.md` 471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0 (of the requirement texts this file cites, V4-WF-05, V4-HI-42, V4-HI-70, V4-HOST-02, V4-EXM-22 and the ARCHITECTURE §4 host-agent properties were amended; the others are unchanged since repo `6e18505e3`, the v0.6 basis; checked with `git diff 6e18505e3 HEAD -- docs/`); ScopeOfWork.md sha256 ceecddbb67a86f744b413bb08b08c27017a82ebee8500f7600faf8d880fbaa47, as revised by SCA-V4-001 (AX-004: CLM-002, CLM-004, REQ-002, REQ-005, TBD-001) and unchanged by SCA-V4-002; owner decisions `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` (D4-1 phased checkpoints) and `-DECISION-5` (host-agent network destinations), `OWNER_DECISIONS.md` sha256 5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2; owner confirmations at the SCA-V4-001 checkpoint, run `APP-V4-BASIS-ALIGN-20260928`, `OWNER_DECISIONS.md` sha256 ca8c4e50df1d7dddb41b875a4afe46eea4f1a1bf2491d255b7890d0d71cd254b (DECISION-6: the arc N-12 is not proposed and N-15 is kept; DECISION-7 accepts `AMENDMENT_PACKET/OWNER_ITEMS.md`, sha256 2b90eb4a95f458e993eed69e27533aa10e31aea980fe2ec99c9c2345e6f498ef, "as recommended": O-10, O-14, O-25); accepted graph `P/execution/_DAG/_LATEST.md` (sha256 4d381ba4e87b41a83b9d0d2dc591c4bf04eacb84df0b5c27314091cd2a992f56) → DAG-003; `P/docs/PRD.md` §2.2 V4-HOST-02, §4.1 V4-WF-05, §4.3 V4-EXE-01…03, §4.5 V4-AUT-01…05, §4.6 V4-PM-06, §4.7 V4-REC-01…05, §10; `P/docs/HOST_INTEGRATION.md` §1, V4-HI-04, V4-HI-11/12, V4-HI-20…25, V4-HI-30…33, V4-HI-40…42, V4-HI-50…52, V4-HI-70/71, §11; `P/docs/ARCHITECTURE.md` §4, V4-ARC-20; `P/docs/EXAMINATION.md` V4-EXM-21/22/31; `P/docs/OPERATING_METHOD.md` V4-OPS-30…32; `DECISION_BRIEF.html` d2, d3; `OWNER_DIRECTIONS.md` J, O; `SCC-CASE-002/Case_Datasheet.md` M1, M2, M3, M3-CP; `_Decomposition/Open_Issues.csv` OI-001/002/013/014/021; `External_Dependencies.csv` DEP-001. Run folder `APP-V4-FIRST-INCREMENT-20260928` at commit **8fb51f07f**: `OWNER_DECISIONS.md` (DECISION-1 and DECISION-2; sha256 a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c); `R1_RESOLUTIONS.md` (2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4); `R2_RESOLUTIONS.md` (77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088); `R3_RESOLUTIONS.md` (202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf); `R4_RESOLUTIONS.md` (50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24); `R5_RESOLUTIONS.md` (254d0b93b9959419a70c6737b07087e1db59b529adc3105a1db31f82b78dd6f1); `reviews/V2.md` (75ba1dff8a0c4fa2eb294471127147cbd19a0925daf9169b32ddc88727dde6ef); `reviews/V3-A.md` (f25f5af1177b7fe2a698bd4ef1e1caafa4c2ef25cfc73111f031e17c7cc21d87); `reviews/V3-B.md` (5662fbd09025f5ad9459861370159d606fcced76b394980199e861555a1954a3); IR1-A/B/C and V1-A/B/C as cited in RS-v0.3
- **Current pins of this run's records (node A4 of run `APP-V4-DESIGN-PASS-2-20260930`; in place, no version bump; R11-3).** Each sha256 recomputed with `shasum -a 256` in the working tree at this pass; paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/`: `R9_RESOLUTIONS.md` sha256 a64e241519b7d158165a7ede0ffdd22eec0af15b6812b5300755f5f38abd59b8 (R9-1…R9-11; R9-2's second bullet as corrected by R10-1); `R10_RESOLUTIONS.md` sha256 ad3b6caa4a12660db77abc51b5c02ba70519ee46d55b40d21ee76eb3ca561796 (R10-1…R10-11); `R11_RESOLUTIONS.md` sha256 e7343b6663b6aeeb2dc506d3391f5b310088e7688d1b21e65d2ba1d8616b3615 (R11-1…R11-9, the repairs from review V17); `OWNER_DECISIONS.md` sha256 7458e9e81971676337a34280b4e8b29a7d04fce5fc202da5b9f5cf7ccd8f9ae5 (DECISION-K1). These supersede for currency the earlier pins of the same records in this header and in the change-table rows, which record the bytes read at node A1 or A3.
- **Consumed inputs for v0.8 (Wave B of run `APP-V4-DESIGN-PASS-2-20260930`, node B4; read from the working tree on commit `86cafc0e1c`; paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/` unless stated).** `BRIEFS.md` sha256 ccb4d9f036fb7ff531fffa0d309533b15cf1ebb39b0320651ed4bd5d88efc550 ("Common rules"; "Wave B — design development", row B4); `R12_RESOLUTIONS.md` sha256 95f3011b436b6faa3de098059e77eac836c165e0bb98a5ed94e28918a3a749a1 (R12-1…R12-10; binding); `R10_RESOLUTIONS.md` sha256 ad3b6caa4a12660db77abc51b5c02ba70519ee46d55b40d21ee76eb3ca561796 (R10-6); `OWNER_DECISIONS.md` sha256 1dfd5bf4619b329719136b1646030e3f871fd7ffc52dbfd12265414e515aaf15 (DECISION-K1, with the later model-download record; this supersedes for currency the pin in the node A4 line above); `SURVEY/S1-A.md` sha256 87baa03d7cbc9b0a6b8e8543d8cd80a7d71c754da80fbfdc053c8e6ef21045f6 (§3.5, §3.8 items 5–8; advice, checked against the current text). Sibling texts read for the joins, cited by label and section (R9-5): DEL-03-03/ADAPTER-v0.5 §5.6 PI-2 and PI-6, §8, §11 (the two evidence limits of R10-6); DEL-05-01/LOOP-v0.7 §2.3 and §5.1.1 (destination events); DEL-05-02/PANEL-v0.7 §3.8 ND-4; DEL-02-03/EXEC-v0.5 §2.1 PH-6, §4.5 SP-6/SP-6F, §5 CAP-1…CAP-9; DEL-02-02 ScopeOfWork REQ-002, AC-002, AC-006 (A15, R12-5). ACT-POLICY-v0.8 and AS-v0.8 were revised by this executor in the same node; §8 here and AS-v0.8 §6 are byte-identical from "**Settings-in" to the end of the section. Other Wave B executors edit other files in parallel; nothing here relies on their Wave B text.
- Consumed inputs for v0.7 (Wave A of run `APP-V4-DESIGN-PASS-2-20260930`, node A1-A; read from the working tree on commit `3dd7c22c73`; paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/` unless stated): `R9_RESOLUTIONS.md` sha256 c3efe2ffa232dd9293202d4fc891eba4325afeb2e224fecdf8c1b4c5122a9d2c (R9-1…R9-11; binding); `BRIEFS.md` sha256 698d91d8217cee528812529fa353faac899b4bc1a5be5686552ad88dad6c469a ("Common rules", "A1 — alignment wave", row A1-A); `SURVEY/S1-A.md` sha256 87baa03d7cbc9b0a6b8e8543d8cd80a7d71c754da80fbfdc053c8e6ef21045f6 (advice; each item applied was checked against the current source); `AgentRuns/APP-V4-BASIS-ALIGN-20260928/DAG_PREP/ARC_ANALYSIS.md` §3.3 (the RS §10 DEL-03-02 cell). Rulings R1–R8, by file: `R1_RESOLUTIONS.md`…`R7_RESOLUTIONS.md` in `AgentRuns/APP-V4-FIRST-INCREMENT-20260928/`, and `R8_RESOLUTIONS.md` in `AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/` at its current sha256 44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b; they stand except where R9 amends them (R9-2 restates R8-11 item 2 and R8-12 item 2). SWBPIPE's answers, DEL-09-06 `Design/RELAY_ANSWERS_SWBPIPE.md`, at its current sha256 afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74: the v0.6 pass read the state 6f01add3…61c7; three answer lines differ between the two states (in SQ-04, SQ-09 and P7; `git diff 94aa9181b HEAD`), and none is a statement this file cites; data about SWBPIPE's current state, not commitments (DECISION-3). Sibling Design files are cited by version label and section only (R9-5), and their bytes are pinned in GUIDE's input table alone; Wave A labels (R9-11): DEL-02-03/EXEC-v0.5; DEL-02-01/WD-v0.7; DEL-02-01/WD-EX-v0.7; DEL-03-01/C-v0.7; DEL-03-02/P-v0.7; DEL-03-03/ADAPTER-v0.5; DEL-03-04/GUIDE-v0.4; DEL-04-01/ACT-POLICY-v0.7; DEL-04-02/AS-v0.7; DEL-05-01/LOOP-v0.7; DEL-05-02/PANEL-v0.7; DEL-01-01/HOSTING-BOUNDARY-v0.7; DEL-01-01/PIN-SPIKE-v0.1; DEL-09-06/CA-v0.5; DEL-09-09/XT-v0.5; DEL-09-06/RELAY-v0.3. The Wave A executors edit in parallel, so the label is cited and nothing here relies on another executor's Wave A text. ACT-POLICY-v0.7 and AS-v0.7 were revised by this executor; §8 here and AS-v0.7 §6 are byte-identical from "**Settings-in" to the end of the section. The byte pins in the consumed-input lines below are true records of what each earlier pass read; they are history, not current pins.
- Consumed inputs for the R8-13 pass: **R8-13 pass (node B1; in place, no version bump).** OWNER_DECISIONS.md sha256 5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2 (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`: V4-HOST-02, host-agent network destinations) and R8_RESOLUTIONS.md sha256 44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b (R8-13) at `1528a5033`; OWNER_DECISIONS.md in its state that adds the owner's DECISION-5 confirmation (committed with this pass); BRIEFS.md sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517 ("Common rules", "A-wave"). Revised in the same pass (node B1), versions unchanged: LOOP, PANEL, ACT, AS, RS, HOSTING, C, ADAPTER and GUIDE; their byte pins are in GUIDE-v0.3's input table.
- Consumed inputs for the R8-12 closing pass: **R8-12 closing pass (node A6; in place, no version bump).** R8_RESOLUTIONS.md sha256 d4c3423310a857af86692d17ddfdd22fa877ee20b07c46e1ee481d1cd750e7af (R8-12: items 1 and 7 applied here; item 5 confirmed). Current sibling versions after R8, as committed at `7a1508452` with A6's in-place R8-12 edits (their byte pins are in GUIDE-v0.3's input table): DEL-02-03/EXEC-v0.4; DEL-02-01/WD-v0.6; DEL-02-01/WD-EX-v0.6; DEL-03-01/C-v0.6; DEL-03-02/P-v0.6; DEL-03-03/ADAPTER-v0.4; DEL-03-04/GUIDE-v0.3; DEL-04-01/ACT-POLICY-v0.6; DEL-04-02/AS-v0.6; DEL-05-01/LOOP-v0.6; DEL-05-02/PANEL-v0.6; DEL-01-01/HOSTING-BOUNDARY-v0.6; DEL-01-01/PIN-SPIKE-v0.1; DEL-09-06/CA-v0.4; DEL-09-09/XT-v0.4; DEL-09-06/RELAY-v0.3. SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` and `FACTS_SQ01_SQ32.md` are unchanged (data about SWBPIPE's current state, not commitments; DECISION-3).
- Consumed inputs for v0.6 (R8 pass, node A2), read with `git show` from commit `94aa9181b` (paths under `AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/` unless stated): `R8_RESOLUTIONS.md` sha256 1770c96e62caf14322811fca82ceb77eca450d3e1be8665cdbdd5550631e8d02 (R8-1…R8-7, R8-10, R8-11; binding); `INTAKE_MAP.md` (I2) sha256 3cc182955c0f3dd70efa0f1c051870229c2ccc08f36c5cf1445f2eef0dd1ea33 (rows 01.7, 02.10, 03.5, 14.4, 19.3, 21.1, 24.2, X.5; Part 2 P2.4, P2.9, P2.17 and its §2.2 RS rows; Part 3 items 2, 3, 4, 10; Part 4.9, 4.11; R8 overrides I2 where they differ); `BRIEFS.md` sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517 ("Common rules", "A-wave"); `OWNER_DECISIONS.md` sha256 a5ccab0d39bd1cab37c5556abc9bdedd5341ce76be4712706c8c9d72d623e776 (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3`, host joins deferred; `-DECISION-4` with its clarification, D4-1 phased checkpoints). Owner files revised first in the same pass: DEL-02-03/EXEC-v0.4 sha256 d32be37797a3c367d342a2d13bbb8dd4279bc52934531d83b8c6ec8c6e7b76d4 (§2.1 PH-1…PH-10, §2.2 GV-1…GV-5, §3.5, §3.6, §4.3, §4.5 SP-4, §4.6, §4.7, §4.11 receiving notes, §7.2); DEL-02-01/WD-v0.6 sha256 fce565edfd0cee3fa4583eb292d11cce3e4121ead0cdbed31ba2fe0a52562f28 (§4.3.0 CG-1…CG-7; §4.3.1 `governed`); WD-EX-v0.6 sha256 950b70b2e3f7fdda9a98b13a63746b76936be490dd96cb6e47bbe6dc9c3eba3d. SWBPIPE's delivered answers DEL-09-06 `Design/RELAY_ANSWERS_SWBPIPE.md` (#1047) sha256 6f01add3977761e42ac6b310faf72ba4fd5455e478605deb83fefb2e4d3a61c7 (SQ-01, SQ-02, SQ-03, SQ-06, SQ-07, SQ-08, SQ-09, SQ-10, SQ-11, SQ-13, SQ-23, SQ-28; ANS §2): relayed and answered 2026-09-28; data about SWBPIPE's current state, not commitments; no host evidence, commitment or contribution received (DEP-001; DECISION-3). DEL-04-01/ACT-POLICY-v0.6 and DEL-04-02/AS-v0.6 were revised concurrently by the same executor; §8 here and AS §6 are byte-identical.
- Consumed inputs (v0.5): DEL-04-03/RS-v0.4 (sha256 56806b64b12a946e706ff236dd1c25fe27ac00877aac13b50ee8603aaf540199, commit cc58211c5). Current sibling versions read from commit **8fb51f07f** with `git show` (not the working tree): DEL-02-03/EXEC-v0.2 `EXECUTION_COMPATIBILITY.md` sha256 7f7848c0de2fdb4dc21f5adafa97f92e179bb66c9f6b04f3434d8f2342317af0 (§2 HP-4/HP-H, §3.3 CR-14, §3.6, §4.5, §4.7, §4.9, §4.10); DEL-03-01/C-v0.4 `CATALOG_AND_READ_BASIS.md` sha256 e929d39d3ff9515702f9bfe51dfada537e1cbd165146ec0de4ccf629c659a08c (§10.1 FXA-1…FXA-5, LIB-A1/A2, AF-1; §10.3; §10.4); DEL-04-01/ACT-POLICY-v0.4 `ACT_AND_POLICY_CONTRACT.md` sha256 d6da05abe790a4374df7faf225439a01dc1be734491b499d90cf00533369b03b (§2.4); DEL-01-01/HOSTING-BOUNDARY-v0.4 `HOSTING_BOUNDARY.md` sha256 201ea32005dd2c9fb5281a376eb25eebfcb5a644d09a6d3bf5901aaf934c7e58 (§8.3); DEL-03-03/ADAPTER-v0.2 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` sha256 a2905dda5782d7a48fa35ef7e26b0c1517fd3bd995e3ddbba27d2426a25674bc. R6 in-place pass (no version bump): C-v0.5 `CATALOG_AND_READ_BASIS.md` sha256 a6306bd477decad22d4405fb86ca6212fb189e4865c68dbbcba90e1335be7a29 (§10.4 V-GR1, GR-1…GR-3, GR-P/GR-R/GR-S) and DEL-02-03/EXEC-v0.3 `EXECUTION_COMPATIBILITY.md` sha256 889e48819baa21ec112c4878e4e38004dcbaa9eb3645a31c24221ac116ee548e (§3.6 HS-1…HS-5, F-24), read at commit d3cebd1cc for the R6 in-place pass; R6_RESOLUTIONS.md and reviews/V4-A.md at commit c7f5513db. The R5 elements earlier marked "per R5-n" (V-GR1, the R5-1 values, P §3.3 carriage) are now present in those sibling texts. DEL-04-02/AS-v0.5 was revised concurrently by the same executor; §8 here and its §6 are byte-identical.
- Receivers: CASE-002 M1 — DEL-02-01 (OUT-001/002; REQ-003; VER-003), DEL-02-03 (OUT-001/002; REQ-003; VER-003), DEL-04-02 (OUT-001/002; REQ-002/004; VER-002/004), DEL-05-01 (OUT-001/004; REQ-005/007; VER-008), DEL-05-02 (OUT-001/003; REQ-001/003; VER-001/003); DEL-01-04 and DEL-02-02 are outside this undertaking (D1). CASE-002 M3 — DEL-04-02 (OUT-001/003; REQ-002/004/005; VER-002/004/005). Rebuilt from the ACTIVE register rows at v0.7 (R9-6; the table is §10.1). `Dependencies.csv` DOWNSTREAM rows: DEP-04-03-011…013 (PKG-02, PKG-03, PKG-06; package rows), -014 (DEL-04-02), -015 (DEL-09-11), -016 (external host run recording), -029 (DEL-05-01), -030 (DEL-05-02), -031 (DEL-09-06) and -032 (DEL-09-09). Declared upstream in the consumer's own register only: DEL-02-01 (DEP-02-01-019), DEL-02-03 (DEP-02-03-013), DEL-03-01 (DEP-03-01-031), DEL-03-04 (DEP-03-04-013), DEL-01-04 (DEP-01-04-012), DEL-02-02 (DEP-02-02-017), DEL-06-01 (DEP-06-01-008), DEL-06-02 (DEP-06-02-010), DEL-09-02 (DEP-09-02-019), DEL-09-05 (DEP-09-05-010) and DEL-10-03 (DEP-10-03-014). DEL-03-03 is a registered supplier (DEP-04-03-026: external dispatch entries), not a receiver. No row records satisfaction.

## Changes from v0.7

Wave B of run `APP-V4-DESIGN-PASS-2-20260930` (node B4): design development
under R12-1…R12-3. Item IDs are the survey items of `SURVEY/S1-A.md` §3.8
("RS n") and §2.8 ("AS n"), and the R12 rulings. Every new structure is
PROPOSED unless a cited text decides it (R12-1).

| Item | Change in v0.8 | Where |
|---|---|---|
| **RS 8** (R12-1, R12-2; U-04) | A PROPOSED record format: append-only logs of entries, one per run and writer, with the common identity elements of §3 as entry elements, one entry kind per inventory element, a format-version rule (same major: read, newer minor read limited; other major or format: refused), identities as opaque tokens with method designations, and relations known later written as their own entries. JSON Schema 2020-12 `RS_RECORD.schema.json` with three valid example logs and nine invalid entries. Placement, path, identity algorithm and canonicalization stay unselected | Header; §0; new §13 |
| **RS 7** | Writer sequence W-0…W-3 and reader sequence R-1…R-8, each step with what fails, who reports it, what record is left and what happens next; failure cases FC-1…FC-9 (write failure, partial entry, two recorders, unknown version, correction, sequence gap, nonconformant entry, unresolvable reference, App restart); a record-state table | new §14; §3 |
| **RS 5** | Decided: an act request and a destination request are record elements. New **R16 Act requests** (entry kind `act_request`), recorded where the request can be identified (ACT AP-5; EXEC PH-6; DECISION-K1 K1-1); its absence is the explicit "request not identified" on the arrival, never a defect. R15 gains **destination requested**. How an App run identifies a request stays EXEC's (node B2) | §1; §3; §4 R8, R15, R16; §4.4; §13.6 |
| **RS 6**, **AS 4** | The §8 exchange (identical to AS-v0.8 §6) now carries a host agent's destination settings in settings-in (allow list, always-off items, in-work grants with scope and state, agent requests) and R15 in record-out (contacts, grants, requests, declines and refusals, outside processes, "destinations not observed"); the comparison covers destination settings; contacts are read from the record, not compared; an unreadable or newer record version is stated in the comparison | §8 |
| **R12-5** | **A15 register workflow revision** is a human-act record kind: subject a workflow revision; bound content its revision identity; relation the draft it derives from; purpose "make it available in the project"; not lapse-evaluated (a changed definition is a new revision needing its own A15); a checkpoint cannot require it in this increment. U-08 closed | §0; §3; §6.1; §6.2 HA-10; §7 L-0; UNRESOLVED |
| **R12-10** (V17-A N-4) | One wording: the record label is **"prior act not counted"**, recorded with one reason — *content no longer current*, *another act kind*, or *captured before arrival (governance-phase option)*. Other wordings ("prior act on this subject, not counted"; "prior act, not counted") are retired; the schema refuses them | §7 L-13; §13.3 |
| **R12-10** (first bullet) | Where a destination request is declined or refused, its recording is labelled PROPOSED; no accepted text is claimed for it | Header; §4 R15; §8; §13 |
| **R12-9**, R10-6 | The two ADAPTER evidence limits ("resubmission without prior observation"; "App-restart interruption") are placed against the writer and failure sequences (FC-9 and §14.3), and a ruling proposal with both passages is returned in `WAVE_B/B4.md` for R13. Both texts stay until then; R11 is unchanged | §10; §14.3; UNRESOLVED U-31 |
| R12-3 | A local prototype (`prototype/`; Python 3 standard library) validates the ACT, AS and RS schemas against their examples, round-trips each example log through a writer and reader, and runs FC-1…FC-7. Command, date and result in §15 | new §15 |
| **B5** (node B5, round 2; LOOP-v0.8 §5.3) | R15 joined to the one destination flow: *destination requested* carries the call it carries (required for scope once, ACT ND-A2); new PROPOSED element **destination request closed** (`destination_request_closed`: *not granted* with reason, or *unanswered at end* with cause; LOOP DF-6); *boundary refusal* gains its stage (model request · V-D · at contact) and category; *destination contacted* gains the model service's class local or cloud (R12-7, N-OPEN-1; B9 join 2); *outside process* gains the stateless evidence SE-1…SE-3 (LOOP DF-7), and R11 the limit "stateless revision declared, not verified". Settings-in request states follow LOOP DF-6 (pending · granted · declined · not granted · unanswered at end), identically in §8 and AS §6. Schema: one kind and four optional elements added in place in format 0.1, which the §13.4 rule would call a minor step; no 0.1 writer exists, so no version step is taken (R13 may rule). New example log `RS_RECORD.valid.host-destinations.example.jsonl` (12 entries, written by LOOP's prototype) and INV-RS-10, INV-RS-11; the host-run example's two requests now name their carried calls. Recording declines and refusals stays PROPOSED (R12-10) | Header; §4 R11, R15; §4.4; §8; §13; §13.3; §13.5; §14.1; §15; VC-30, VC-38; schema and examples |
| Verification | VC-02 checks R1–R16. New VC-31…VC-38 (format round trip; write failure and partial entry; two recorders; versions; correction; request element; A15; destination exchange); VC-31…VC-35 ran on the prototype. VC-24 coverage extended | Verification cases |

## Changes from v0.6

Wave A of run `APP-V4-DESIGN-PASS-2-20260930` (node A1-A): alignment to the
amended basis and the revised ScopeOfWork under R9-1…R9-11. It adds no new
design content. Survey items are those of `SURVEY/S1-A.md` §3.

| R9 ID (survey item) | Change in v0.7 | Where |
|---|---|---|
| **R9-5**, R9-11 (RS 1; R-P1, R-P2, R-P6…R-P10) | Version v0.7. The basis is re-pinned from repo `6e18505e3` and ScopeOfWork `74d42c38…40c1` to the four basis documents by sha256, as amended by SCA-V4-001 and SCA-V4-002, and to ScopeOfWork `ceecddbb…aa47` (SCA-V4-001; AX-004). A new consumed-input block for v0.7 names R9, R1–R8 by file with R8 at its current sha256, SWBPIPE's answers at `afb6e063…`, `_DAG/_LATEST.md` → DAG-003, and the siblings by Wave A version label only. The earlier consumed-input lines are kept as history. Body citations of the current sibling texts move to the Wave A labels (EXEC-v0.5, WD-v0.7, C-v0.7, AS-v0.7) | Header; §0, §1, §4 R8, §8, §12 |
| **R9-6** (RS 1, RS 3; R-P11) | The Receivers line is rebuilt from the registers, and new **§10.1** lists receivers and suppliers by register row. §10: a DEL-09-09 row is added; the DEL-03-02 cell is restated ("P's outcomes are recorded under §5"; the arc N-12 was not proposed); the DEL-03-03 cell is marked the same way (N-B8); the DEL-09-06 and DEL-05-02 cells are widened to what those files cite. Two evidence limits that ADAPTER names for R11 are marked as not yet defined here; no ruling decides them, so both texts stand (R9-9) | Header, §10, §10.1 |
| **R9-1** (RS 2; R-P3) | §1 cites V4-WF-05 and V4-HI-42 as amended by SCA-V4-001. The description of V4-WF-05 by halves and the marker that awaited a basis update are removed. §1 states who requests the act and what the product records (INTEGRATION; put to the owner for confirmation) and points to EXEC (Wave B). No record element for the request is defined here | Header, §1 |
| **R9-2** | D14 restates R8-11 item 2 against the amended text | §1 D14 |
| **R9-3** | "the current phase (Phase 1)" on first use | Header |
| **R9-4** (RS 2; R-P4, R-P5; survey §3.4 items classed NOW) | R15 is no longer marked an addition: it is within the ScopeOfWork inventory (REQ-002, CLM-002) and V4-HI-70 as amended. R5's destination and D16 lose the label "INTEGRATION (DECISION-2 reading)": ScopeOfWork REQ-002 requires the destination per turn, and the owner confirmed the reading (OWNER_ITEMS O-10, DECISION-7 of `APP-V4-BASIS-ALIGN-20260928`). D16 cites V4-HOST-02 from the PRD as amended, and its marker that awaited a basis update is removed. VC-02 checks R1–R15 | Header, §1 D16, §4 lead, R5, R15, VC-02 |
| **R9-8** (RS 4; survey §3.2 item 1) | §11: the statement that the ScopeOfWork's TBD-001 still reads OI-001/OI-002 as open is removed; SCA-V4-001 revised it. R8-12 item 5 was checked: R11 lists both evidence-limit labels ("host reachable without evidenced A13"; "constraint not carriable on this host"), so no edit was needed | §11 |
| R9-7 | Checked, no edit: R3, R5, R13 and the §10 DEL-01-01 row take the observed supplier facts from DEL-01-01 directly, as ScopeOfWork CLM-004 and DEP-04-03-027 state | — |
| **R10-2** (node A2, in place) | "Constraint not carriable on this host" loses its "governance phase" restriction in R11 and U-19: a record fact in either phase; in the current phase it says the expected constraint could not be carried and was recorded only (ADAPTER GC-4, P §3.3); it bears on a hold-support value only in the governance phase | §4 R11, UNRESOLVED U-19 |
| **K1-1** (node A3, in place; owner DECISION-K1 of 2026-09-30, `APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md` sha256 35d6546346907137581be7df3bed4a8ccdb4b8bc55a261ca716040d0ad9f91bc) | §1: who requests is **SETTLED by DECISION-K1 K1-1** (was INTEGRATION, put to the owner) | §1 |
| **K1-2** (node A3, in place) | L-13 rewritten: in the current phase an earlier act counts when it is of the required kind and its content is still current, and the record cites it and its time (EXEC SP-6); capture after arrival is kept as a governance-phase option (EXEC SP-6F). R8 annotations and §6.1 relations gain "by earlier act ‹act› at ‹t›"; "prior act not counted" stays for content no longer current, another kind, or that option. §10 DEL-02-03 row; E7, E10 (i), E11 and VC-17 recomputed; U-26 closed | §4 R8; §6.1; §7 L-13; §10; §12; UNRESOLVED; Verification cases |
| **K1-3** (node A3, in place) | L-7: a partially lapsed multi-row A4 keeps its purpose for the unchanged rows; a new act on the changed rows alone answers a checkpoint together with it (EXEC §4.7 JA-1). R8 gains "answered by ‹n› acts". E4 and VC-09 follow; U-07 closed | §4 R8; §7 L-7; §12 E4; UNRESOLVED; Verification cases |
| **K1-4** (node A3, in place) | §6.1 *Decision actor* and *Evidence limits*: for App-captured acts the App names the person from what it observes (the name set in the App, the operating-system account, the Codex account when Codex reports one), marked **identity not verified**; a verified identity is a governance-phase matter. U-28 closed; §10.1 X-1 note: the act control's obligation is proposed for DEL-01-04's contract at the next amendment | §6.1; §10.1; UNRESOLVED |
| R10-6 (node A2, in place) | The §10 DEL-03-03 note on the two ADAPTER evidence limits R11 does not list now says they are carried to Wave B, node B4 (was: "no ruling decides them"). Both texts stay | §10 |
| R11-6 (node A4, in place; V17-A m-2) | E10 (i) and VC-17 add the governance-phase reading under EXEC SP-6F, as E7 and E11 already do: T2's A4 is "prior act not counted" and the arrival waits for an A4 on S-2 and S-3 captured after T4a. The current-phase results are unchanged | §12 E10; Verification cases VC-17 |
| **R11-3** (node A4, in place; V17-A M-1) | Header: a new line pins this run's records at their final bytes: R9 `a64e2415…`, R10 `ad3b6caa…`, R11 `e7343b66…`, OWNER_DECISIONS `7458e9e8…`. The node A1 input line and the K1 rows keep the bytes read then | Header |

## Changes from v0.5

Keyed by R8 ID; sources are I2 rows of INTAKE_MAP.md (`nn.k`, `P2.n`, Part 2.2
RS rows, Part 3 items, Part 4 sections). R8 overrides I2 where they differ.
SETTLED means by DECISION-3 or DECISION-4. The owner files EXEC-v0.4 and
WD-v0.6 were revised first; this file follows them.

| R8 ID (source) | Change in v0.6 | Where |
|---|---|---|
| **R8-1** (DECISION-4 D4-1; SETTLED, framing INTEGRATION) | §1 states Phase 1: arrivals, acts and lapses are recorded as **observation**; an act is recorded **only when the person performed it**; no hold, re-hold or hold-support value and no *unsupported* for a hold reason is recorded; reserved acts stand (D14). New elements (§4.2): the **`governed`** flag in R8 and the optional Phase-1 annotation **"continued past ‹checkpoint› before ‹act›"**, which replaces *action during hold* in Phase 1 and is never an R11 limit (OE-8) | Header, §1, §4 R8, §4.2, §5 |
| **R8-1** (governance phase retained) | R8's hold support, R11's *action during hold*, R14's per-checkpoint hold support, §5's carriage assurance, OE-8's *during hold* flag and L-12's re-hold are relabelled **governance phase (retained)**, each with its Phase-1 statement. Nothing is deleted | §4, §5, §7 L-12 |
| **R8-1** (cases) | Two-part form (Phase-1 record; governance-phase value): **E7** (V-GR1 via X), **E10** (i)–(vii) rewritten, E6 annotated. VC-17, VC-26, VC-28 updated; new **VC-29** (Phase-1 record semantics); VC-24 coverage extended | §12, Verification cases |
| **R8-2** (I2 R8-Q1, R8-Q-HS4; P2.4, P2.9, P2.17; §2.2 RS rows) | SQ-02's answer is the **governance-phase input**. Governance-phase values: **E7** V-GR1 `CP-grant` via X → **not enforceable** (was *not established*); **E10 (vii)** → **not enforceable → *unsupported*** (was *not established*); VC-17 (vii) and VC-28 follow. R8's *not established* value notes that neither cause applies against SWBPIPE now, and HS-3 records "SWBPIPE: answered with none, 2026-09-28". **D6 is closed for Phase 1** (§1, §10, §11, U-25) | §1, §4 R8, §10, §11, §12, UNRESOLVED |
| **R8-3** (I2 R8-Q2; Part 3 item 2) | *refused — stale* records affected items, or the host's stated **staleness scope** where the host supplies no subject identities (SWBPIPE: whole model; failing targets *not supplied*, R11), never narrowed; OE-4 notes the scope; de-duplication first is unchanged | §4 R11, §5 outcome table, OE-4 |
| **R8-4** (I2 R8-Q3; 03.5; Part 3 item 3) | L-1: a whole-model identity is received as every covered subject's identity (over-lapse, never under), never App-computed; "subject identities not supplied" is an R11 limit; *applied (receipt)* resulting objects may be *not supplied* beyond target ids. L-11 and U-12 note SQ-03 (e). New **U-29** (V4-HI-32 not met by SWBPIPE; owner SWBPIPE) | §4 R11, §5, §7 L-1, L-11, UNRESOLVED |
| **R8-5** (I2 R8-Q-item-1, R8-Q10, R8-Q13, R8-Q15; Part 4.9) | Outcome table: `unsupported_method`/`unsupported_change` → *not exposed on this surface* (never *not permitted*); `validation_rejected` → *refused — invalid*; #885 `withdrawn` → item-left event "cleared by the person, no decision record"; never A10/A11. OE-6: receiptless session undo → *reverses ⟨receipt⟩* *not supplied*. OE-7: accept and apply are one step on SWBPIPE, so it does not arise there. VC-16 updated | §5, VC-16 |
| **R8-6** (SQ-13, SQ-28; I2 R8-Q4) | *channel not enabled* row: SWBPIPE has no such code; `controller_unavailable` is *endpoint unavailable*, the channel stays *disabled*. New R11 limit "host reachable without evidenced A13" | §4 R11, §5 |
| R8-7 (X.5; 01.7, 21.1, 14.4, 19.3, 24.2; Part 4.11) | Standings move to **answered**: header, §6.1 capture evidence (SQ-01), §10 external host row (answers summarised; no commitment or contribution). U-11 owner → SWBPIPE owner decision (PB-TBD-002; DEL-16-03); U-15 and U-19 effects updated. I2 rows 14.4, 19.3, 21.1 and 24.2 (RS R11, R2/R3/R5a, HA-9, R10) need no edit. This file cites no OI-003 | Header, §6.1, §10, UNRESOLVED |
| R8-10 (I2 R8-Q12) | New R11 limit "constraint not carriable on this host" (governance phase): the agent never adds a field the host schema lacks | §4 R11, U-19 |
| **R8-11** (A1 residuals) | Item 1: lapse recording in Phase 1 and dispositions as record labels (R8, L-12). Item 2: D14's reserved-act half binds in Phase 1; its checkpoint half is guidance. Item 3: an invalid declaration is recorded as a declaration finding in Phase 1 (R8). Item 5: governance-phase values read the fixture's checkpoints as if governed (E10) | §1 D14, §4 R8, §7 L-12, §12 E10 |
| (R8-9, noted) | D16: V4-HOST-02's retention is pending owner clarification (R8-9). No rule of this file changes | §1 D16 |
| **R8-12** (items 1, 5, 7; closing pass, node A6, in place) | Item 1: L-12's Phase-1 lapse after resume is labelled **"act lapsed at ‹t›"** (nothing says *waiting*; a new act is recorded when performed); E10 (iv) and VC-17 follow. Item 5 confirmed: R11 already carries both evidence-limit labels ("host reachable without evidenced A13"; "constraint not carriable on this host") — no edit. Item 7: consumed inputs list the post-R8 sibling versions; §0 and §12 fixture sources note that C-v0.6 carries the C-v0.4/C-v0.5 fixture | Header, §0, §7 L-12, §12 E10, VC-17 |
| V9 N-5 — in place | E7 Phase-1 result says "passes on required tools and channel state", matching the siblings |
| **R8-13** (DECISION-5; SETTLED; the act mapping INTEGRATION; in place, no version bump) | New element **R15 Network destinations of a host's agent** — addition. It records: **destination contacted** (per request: destination, category, and the allowing grant or list entry, in any model mode); **destination grant** (scope once / this run / always, time, source list or in-work, with a reference to the A12 network-destination grant record, ACT §2.7); **destination declined** (the act-declined event of kind A12 and the outcome "destination not allowed by the person"); boundary refusals; and each **outside process** with its declared destinations. R11 gains the evidence limits **"process network not observed"** (an outside process that is not sandboxed) and "destinations not observed". New §4.3, E13, U-30 and VC-30; VC-24 coverage extended. **D16**: the V4-HOST-02 "pending owner clarification (R8-9)" marker is replaced by the revised V4-HOST-02 (DECISION-5; flagged for the next accepted-basis update) | Header, §1 D16, §4 R11, R15, §4.3, §12 E13, UNRESOLVED, Verification cases |
| R8-13 close — in place | The owner confirmed DECISION-5 (the reading of "MCP V2"; the person-only grant stands), so the "open to the owner's correction" markers are closed. The consumed-input line is corrected: OWNER_DECISIONS.md is cited in its state that adds that confirmation, not at `1528a5033` |
| V10 S-1…S-4 — in place | The wording of the DECISION-5 confirmation is made precise (the "MCP V2" reading was confirmed; the person-only grant was not objected to and stands). The revised V4-HOST-02 is "the recorder's wording confirmed by the owner". The always-off item reads "a silent switch". ACT F-22 is updated. No rule changes |

## Changes from v0.4

The v0.3 → v0.4 change table is preserved in RS-v0.4 at commit `cc58211c5`.

| Item | Change in v0.5 |
|---|---|
| R5-1 (V3-A MAJOR-1) | R8 hold support uses the four ruled values: **enforced by the host loop** · **enforced on the host route** · **not established** · **not enforceable**. EXEC-v0.1's "enforced before dispatch" and "held after observation" are retired. The workflow requirement consequence is recorded with the value (*not established* is never a pass and never *unsupported*; *not enforceable* → *unsupported*) |
| R5-2 (V3-B MAJOR-1) | §5 carriage assurance: **host-held** covers host derivation or host verification against its own declaration copy (and the host loop's own evaluation); a constraint the host only received keeps its source's assurance; **App-assured is not available in this increment**; only host-held satisfies R2-12 |
| R5-4 (V3-A m-11; Y-3) | R5 records the model destination **per turn** (requested and effective kept separate; reroutes with their turn; unobserved turns *unknown*); the run-level value is the **set** observed; a switch starts no new run. D16 split: "may flow; no gating" SETTLED by DECISION-2; "record and show" relabelled **INTEGRATION (DECISION-2 reading)**. E12 and VC-22 updated |
| R5-5 (Y-4) | L-12: a lapse re-holds whatever caused it, including the person's own undo; OE-8 and R11: the person's own operations are never *action during hold*; an undo never re-holds an A5 arrival. E6 extended |
| R5-6 (Y-5) | §3 and §5: an operation that performs a reserved act (OP-C6/C7/C8, the A12/A13 controls) produces the human-act record, and its R7 entry references it; the person's A1/A2 stay R7 operations. E1 and E2 cite it |
| R5-7 (V3-A MAJOR-3/MAJOR-5; Y-6) | E7 and VC-13 re-pointed to **V-GR1** (per R5-7; C adds it): CP-grant arrives at r15, T15's A12 is captured after the arrival, the held OP-C9 call is dispatched unchanged as T16; sub-variants pending, refused, confirmation lost, later established A12. On the main timeline T15 is before any CP-grant arrival and does **not** count. L-RS-3 removed. L-13 notes the owner-visible cost |
| R5-8 (V3-A MAJOR-2) | E10 and VC-17: "held after observation" and "run stops" removed. The App run shows hold support **not enforceable** (App-only checkpoint → workflow *unsupported*) and records dispositions and **action during hold** with no claimed stop; a host-operation variant over X shows **not established** (awaiting SQ-02) |
| R5-9 (V3-A m-2, m-3, m-12) | Citations re-pointed to current sibling versions (EXEC-v0.2, C-v0.4, ACT-v0.4, HOSTING-v0.4, ADAPTER-v0.2) at commit 8fb51f07f; C fixture assumptions cited **FXA-n**; stale "C declares only V-CP1" reasons replaced (C FXA-5 declares CP-accept **and** CP-check); E1 uses FXA-5's CP-accept arrival; App-side subjects LIB-A1/LIB-A2/AF-1 used where relevant (VC-27) |
| V3-A m-9 | Annotation string unified: **"waiting — re-held, lapsed at ‹t› after resume"** (R8, L-12) |
| R6-1 (in place; V4-A MAJOR-1) | Hold support is classified by the checkpoint's **held actions**: all host operations → HS-3, valued by SQ-02 status (enforced on the host route · not established · not enforceable); any App-side held action → **not enforceable** in App runs (HS-5). R8 states the rule; E10 CP-row-check classified (holds App agent turns → not enforceable) and variant (vii) (holds only a host operation → not established while SQ-02 is unanswered) |
| R6-3 (in place; V4-A m-4) | L-12, OE-8 and R11: the run **stops** only under *enforced by the host loop*; under *enforced on the host route* the host refuses the held host operations and every other run action is *action during hold*; under *not established* / *not enforceable* nothing is stopped and actions are *action during hold* |
| R6-5 (in place; V4-A m-13; EXEC F-24) | R11 *action during hold* carries the **turn initiator**: person-directed · agent · App rule |
| R6-4 / V4-A m-1 (in place) | Stale markers removed: V-GR1 is cited from C-v0.5 (run 13; GR-1…GR-3, GR-P/GR-R/GR-S) instead of "per R5-7; C adds it"; header cites C-v0.5 and EXEC-v0.3. R6-2: V-GR1's `CP-grant` via X is *not established* (HS-3, SQ-02 unanswered) |
| R7-4 m-3 (in place; V5 m-3) | E7 (V-GR1 via X) adds "; E1d's `CP-check` is *not enforceable*, so the run via X is *unsupported* (EXEC MT-16)". Run 13 inherits E1c's `CP-check` (HS-5), so the workflow result via X is *unsupported* whatever SQ-02 returns. No value changes (V5 §3) |

## 0. Reading this definition

- Element names in §1–§12 are **semantic names, not wire names**. §13
  PROPOSES a serialization, element spellings and types for review (R12-1;
  U-04); it is not accepted. No file path, persistence location, transport,
  hash or canonicalization algorithm, process placement or shared-component
  placement is selected (SoW TBD-002; OI-013; OI-014; DEL-03-01 TBD-003;
  R12-2), and no wire field of a host or supplier is selected.
- `⟨…⟩` is an opaque identity token. Equal tokens stand for "the designated
  identity method reports the same identity".
- **Act names (DEL-04-01 §2.1):** A1 propose · A2 apply · A3 examine · A4 mark
  checked · A5 accept · A6 approve (engineering approval only) · A7 rely · A8
  request · A9 record · A10 reject · A11 withdraw · A12 set grant · A13 enable
  external access · A14 answer tool permission · **A15 register workflow
  revision** (R12-5; ACT-POLICY-v0.8 §2.1). A9 is a recording act; A14 is
  never a human-act record (R2-8).
- **Class values (DEL-04-01 §8.1; R2-1):** none · may apply within granted
  autonomy · proposal only · reserved to the person (SETTLED, V4-HI-02) · **no
  policy basis**, with reason ∈ {omitted, unassigned, pending OI-021}
  (INTEGRATION).
- **Reserved to the person.** ADOPTED by D2: A4; A5 wherever the active
  autonomy requires a proposal; A6; A7; A12; enabling external access (A13).
  DERIVED: A10 wherever A5 is; operations that perform any of these (R2-2).
  INTEGRATION: disabling external access is also a person's A13 (R2-3). The SWB
  model-change class (DEL-04-01 P-03) is *may apply within granted autonomy*
  (DERIVED), default *propose*. Operation-specific additions await OI-021.
  Host adoption is not shown (DEP-001).
- **Grant value** (direct / propose) is what the person sets; **treatment** is
  what the host route resolves.
- Examples are **fixture subjects** from DEL-03-01/C-v0.4 §10 (FX-PIPE-01), carried in C-v0.7 §10.

## 1. Settled distinctions relied on

| # | Settled distinction | Citation |
|---|---|---|
| D1 | Workflow definitions, the person's decisions and accepted records are ordinary files in the user's project or workspace | V4-REC-02 |
| D2 | A harness session store is operational, not the authority for any human act; coordination views are derived and rebuildable | V4-REC-03; V4-PM-06 |
| D3 | Host domain truth stays in the host's own store | V4-REC-01 |
| D4 | Host receipts, hashes and origin marks evidence what changed; the run record links them and does not copy them | V4-HI-71; V4-REC-04 |
| D5 | `success` means it ran; a submitted proposal is "queued" until the host records acceptance and application | V4-HI-25 |
| D6 | Proposal lifecycle drafted → validated → queued → accepted → applied (receipt), with rejected / withdrawn / stale, and outcome unknown | V4-HI-23 |
| D7 | Only observed events are shown as having happened; an unobserved outcome is unknown | V4-EXE-03; V4-EXM-31 |
| D8 | A human act binds to the content it concerns and lapses visibly when that content changes | V4-HI-32; V4-REC-05 |
| D9 | "accept", never "approve", for proposals | V4-HI-33 |
| D10 | No fabricated human act; faithful recording of an actually performed act is permitted | V4-HI-31; V4-AUT-03; d3 |
| D11 | Acts are distinct subjects; evidence of one establishes none of the others; no acceptance-first chain | d3; V4-AUT-03 |
| D12 | Nothing agent-produced is presented as certified, sealed, approved or code-compliant | V4-AUT-05 |
| D13 | Git history and reviewed pull requests are primary change records | V4-OPS-31 |
| D14 | Reserved to the person (first increment, App/shared): mark checked; accept where autonomy requires a proposal; engineering approval; reliance; changing the grant or enabling external access. No grant widens past a reserved act or declared checkpoint. The host names and enforces its own list. **Current phase (R8-11 item 2, restated by R9-2; the reading of D2 was confirmed by the owner: OWNER_ITEMS O-25, DECISION-7 of `APP-V4-BASIS-ALIGN-20260928`):** "no grant widens past a reserved act" binds, and the host enforces it through its operations. For a declared checkpoint, V4-HI-42's request clause and record clause are in force whatever the autonomy setting; whether the run goes on before the act is for the person and the agents, and the host's own treatment of its operations decides what the host does. Holding the run binds only for governed checkpoints in the governance phase | OWNER_DECISIONS D2; V4-HI-30; R8-11; R9-2 |
| D15 | App routine tool-permission and sandbox modes are the user's own Codex setting per project/turn; they govern tool execution only and never stand in for a reserved or professional act. Hosts have no classifier permission mode in the first increment | OWNER_DECISIONS D3 |
| D16 | Host content read by the App's Codex through the external channel may flow to the App conversation's selected model, cloud included; the App does not gate on the model destination. A host may restrict its own channel (DEP-001); PRD V4-HOST-02, as amended by SCA-V4-001 (which applies DECISION-5; R8-13), governs the host's embedded agent: "A host's agent sends data only to the model service the person selected and to destinations the person has allowed — in advance in an allow list (by category, such as web access, MCP servers or other APIs, or by named destination) or when the agent asks during its work. Nothing else is contacted: no analytics, silent provider switch or background download unless the person turns it on. Every destination contacted is recorded and shown (D-18; DEC-5)." Its record is R15 (ScopeOfWork REQ-002 and CLM-002; V4-HI-70 as amended). (That the App **records** the destination per turn and shows it in the channel status is **SETTLED**: ScopeOfWork REQ-002 requires "model used with its observed destination per turn", and the owner confirmed the reading, OWNER_ITEMS O-10, accepted at DECISION-7 of `APP-V4-BASIS-ALIGN-20260928`; R4-1/R5-4; R9-4) | OWNER_DECISIONS DECISION-2 D5; R5-4; PRD V4-HOST-02 (SCA-V4-001; DECISION-5); ScopeOfWork REQ-002; OWNER_ITEMS O-10 (DECISION-7) |

**Phase 1 (R8-1; DECISION-4 D4-1).** Declared checkpoints are plan guidance
(EXEC-v0.5 §2.1; WD-v0.7 §4.3.0). This format records a checkpoint's
arrivals, the acts that answer them, and act-declined, act-lapsed,
run-resumed and run-ended events as **observation**, not enforcement. It
records an act only when the person performed it (V4-HI-42 as amended by
SCA-V4-001: "recorded as done only when the person performs it"; V4-WF-05),
and records no hold, re-hold or hold-support value and no *unsupported* for a
hold reason. The agent carrying out the workflow asks the person for the act
when its work reaches the checkpoint. The product's part is to record what
it observes: the checkpoint's identity, the request where it can be
identified, and the act only when the person performs it. A record never
says *performed* without the act (R9-1; SETTLED by DECISION-K1 K1-1). The
record element for the request is **R16** (§4; PROPOSED representation,
§13.6): an identified request is recorded as an act request; where none can
be identified, the arrival says "request not identified", an explicit
absence that is never a defect. How an App run observes an arrival and
identifies a request is EXEC's (DEL-02-03, Wave B node B2); the element
itself is defined here. A run action after an arrival and before its act may carry the
optional annotation "continued past ‹checkpoint› before ‹act›" (R8-1).
App-side run holds, `UNRESOLVED{D6}`, are **closed for Phase 1** by
DECISION-4 and re-open when the governance phase is taken up (R8-2).

**Governance phase (retained).** For checkpoints declared `governed`, this
format records hold support with the four R5-1 values and action during
hold; it never records an App hold as enforced when it was not (R4-2). SQ-02
decides holds only for checkpoints on host operations; App-only checkpoints
stay **not enforceable** whatever it answers (R5-10). SWBPIPE answered SQ-02
on 2026-09-28 with no host-held route (route (iv), none planned), so its
host-operation checkpoints are *not enforceable* too (R8-2).

## 2. Ordinary-file authority rules

(Renamed OF-n in v0.4; C §10.1 cites its fixture assumptions as FXA-n.)

| Rule | Statement | Serves |
|---|---|---|
| OF-1 | The authority for "person P performed act K on content C for purpose U" is an **act record** in an ordinary project/workspace file together with the evidence it references. Nothing else supplies a missing act. | REQ-001, REQ-003; AC-001 |
| OF-2 | Harness session content, transcripts, agent memory, derived views, search indexes, PEC projections, A14 settlements and user-input/elicitation answers may **locate** evidence. Their assertion that an act occurred creates none. | REQ-001; D2; D15; R4-12 |
| OF-3 | Host domain truth, receipts, hashes and origin marks stay with the host. A record holds **references** plus what is needed to resolve and compare them: reference, claimed identity, identity method designation, resolution status. Never a substitute copy. | REQ-002; D3, D4 |
| OF-4 | Workflow definitions and accepted records remain owned by their producing deliverables; this format supplies the act and run records that refer to them. | REQ-001, REQ-005 |
| OF-5 | A written act record is not edited to change actor, act kind, bound content, scope or purpose. A correction is a new record naming the corrected one; both remain readable. Supersession of A12/A13 (L-0) is a relation, not an edit. (Proposed; the mechanism is PROPOSED in §14.1 W-3: a new entry of the same kind carrying *corrects* and a reason.) | REQ-003, REQ-004 |
| OF-6 | Git history is the primary change record for the files (D13); records cite a repository revision where their own revision matters. | AX-003 |
| OF-7 | Each record identifies its **format version** and **record kind**; a reader refuses or limits an unknown version (PROPOSED rule: §13.4, §14.2 R-3). | OUT-001 |
| OF-8 | The **recorder** is always identified and is never the decision actor merely by having written the record. A person's own act captured in a surface is *direct capture* by that surface, not self-recording. | REQ-003; D10 |
| OF-9 | App runs keep records with the user's project/workspace; host-agent runs keep records with the host project (V4-HI-70). Path and host persistence are not selected (U-05, U-06). | REQ-001, REQ-005 |

## 3. Record kinds and identity

| Record kind | Authority for | Produced by |
|---|---|---|
| Run record | That a workflow run occurred with the identified workflow, conversation, model and destination, settings, requested operations and observed outcomes, linking host evidence | App writer (OUT-002) for App runs; host run recording (external owner, DEP-04-03-016) for host-agent runs, in the shared meaning |
| Human-act record | That an identified person performed A4, A5, A6, A7, A10, A12, A13 or **A15** (register workflow revision; R12-5), or A11 when the person is the proposer, on identified content, scope and purpose, with capture evidence (ACT §2.4). A person's own proposals (A1) and applications (A2) are R7 operation entries with author type *person*, not human-act records. An operation that **performs a reserved act** (C OP-C6/OP-C7/OP-C8; the A12/A13 controls) produces the human-act record of that act, and its R7 entry, if any, references it (R5-6) | A recorder: capturing surface, App, host facility, or an agent performing A9 |
| **Act request** (R16; PROPOSED representation, §13.6) | That an identified agent asked the person for an identified act kind on an identified subject and purpose (A8), where the request can be identified. Never the act; satisfies nothing (HA-1) | The writer observing the request (App: DEL-02-03 observation; host: the loop's "A8 request issued" event) |
| **Act-declined event** | That a person decided **not** to perform a required A4, A6, A7 or A12 on an identified subject, with capture evidence (R2-5). Not an act of that kind; satisfies nothing that requires the act | Same recorders |
| **Act-lapsed event** | That a performed act was observed lapsed at ‹t›, with c₀/c₁ (R2-19) | Record reader/writer on evaluation |
| **Run-resumed event** | The resume point of an arrival: {arrival, time, first action reference} — the first run action after the arrival became *performed* or *resolved negatively* with a proceed/return path (EXEC HD-5; R4-3) | Executor (App: DEL-02-03; host: loop) |
| **Run-ended event** | That the run stopped (V4-EXE-01): who stopped it (the person, or the observer reporting an end), cause (e.g. "stopped by declared negative path", "interruption not recovered"), and which arrivals were then *waiting* (R2-5; EXEC RE-4) | Run writer |
| Decision / accepted record | A PKG-06 or workflow-owned record an act record may cite | Its owning deliverable |

Common identity elements: *record identity*, *record kind*, *format version*,
*recorder identity*, *recording context* (App, or host identity),
*written-at order*, *corrects* (optional).

**Run finality (R4-4; EXEC §4.9; PROPOSED).** A run with a run-ended event is
closed and never resumed. Its arrival dispositions are final, except the
R2-19 change from *performed* to *lapsed* on a later lapse. An act performed
after the run ended is recorded and marked **"after run end"**; it changes no
disposition of the ended run. Continuation is a **new run** whose run record
carries **continues ⟨run⟩**; nothing carries into it (no arrival, disposition
or act). An interruption without a run-ended event is not a run end.

**Record states (PROPOSED; RS 7; R12-1).** The state of a written entry as a
reader finds it, not the state of what it records (lapse, supersession and
dispositions stay as §6, §7 and R8 define them). No transition edits a
written entry (OF-5).

| State | Entered when | Left when | What a reader shows |
|---|---|---|---|
| **pending write** | The writer accepted the entry and has not yet written it (W-1), or a write failed (W-2) | Written → *written*; the writer ends without writing it → never in the record (the failure is reported, FC-1) | Nothing: it is not in the record. The display compares *missing in record* (§8) |
| **written** | One complete line was appended and synced (W-1) | A later entry names it in *corrects* → *corrected* | The entry |
| **corrected** | A later entry of the same kind names it in *corrects*, with a reason (W-3) | Never (a correction may itself be corrected) | Both entries; this one marked "corrected by ⟨entry⟩"; derived state uses the latest correction |
| **partial** | A line was torn by an interrupted write (FC-2) | Never | "partial entry (not read)"; the bytes are kept; the writer's next open records "partial entry not recovered" |
| **read limited** | Its format version has the known major and a newer minor (R-3) | A reader that knows that minor reads it → *written* | Known elements; unknown elements and kinds shown as present and unread |
| **refused** | Its format name or major version is not known (R-3) | A reader that knows it | "unreadable version ‹v›"; nothing inferred from it |
| **nonconformant** | It fails the schema or a reader rule (R-4, R-7) | A correction that conforms → the original is *corrected* | Shown with the rule it breaks; never used for a disposition or a count |

## 4. Run-record inventory

Every element named in REQ-002 / SOW-186 / V4-HI-70 is present. "Required"
means present as a value or as an explicit absence statement; *not
applicable* is allowed only with its reason. Elements marked **addition** go
beyond the SoW inventory and name their source. R15 and the R5 destination
are within the inventory since SCA-V4-001 (ScopeOfWork REQ-002 and CLM-002;
V4-HI-70 as amended), so they are not marked (R9-4).

| # | Element (semantic) | Meaning | Supplier | Absent / unknown handling |
|---|---|---|---|---|
| R1 | Run identity | Stable identity of this run, distinct from conversation, proposal and operation identities; **who started it** (EXEC RE-5); **continues ⟨run⟩** where this run continues an ended one — **addition** (R4-4) | Record writer | Required; *continues* absent unless recorded |
| R2 | Workflow identity as observed | {kind, origin, source root, name, revision} + derived-from; promised vs observed separate. Trace links as separate facts (EXEC §6.1): *listed*, *selected*, *resolved* with **revision verification** outcome (recomputed content identity equals the revision, or "revision not verified"); holding library at listed/selected/resolved, never in identity equality (EXEC §6.2, confirmed). **Transfer links** — exported, relayed, received, adapted — with transfer identity and **carriage-manifest reference**, each marked original or revised identity — **addition** (R4-11) | DEL-02-01 §6.1; DEL-02-03 §6 | "revision not verified", "relay not evidenced", "receipt not observed" stay explicit; a revised identity never inherits a link of the original |
| R3 | Supplied guidance identity and limits — **addition** (R-10; R2-20) | Per thread and turn, source identity and content identity (with method) of each guidance input supplied; "supplied ≠ adopted" | DEL-01-01 (App); host loop (relay) | *unknown* where not recordable |
| R4 | Conversation reference | Reference to the harness conversation/session | Harness | Reference only — operational, not authority |
| R5 | Model used and **model destination** | Model identity and serving endpoint class as observed, separate from configured. **Destination** (ScopeOfWork REQ-002: "model used with its observed destination per turn"; the reading was confirmed by the owner, OWNER_ITEMS O-10; R4-1, R5-4): recorded **per turn** where the supplier reports it (HOSTING §8.3) — the **requested** provider/model and the supplier-reported **effective** one kept separate, each **re-route** recorded with its turn, destination class (local model server / user-chosen cloud) from the person's provider configuration; a turn not observed is *unknown*. The **run-level value is the set** of destinations observed, never a single inferred value. A model switch or re-route starts no new run and affects no disposition. Covers host content read over the external channel. Information only — never a gate, never a permission | DEL-01-01 HOSTING §8.3; DEL-05-01; DEL-03-03 | "Requested X; effective unknown" and unobserved turns are valid |
| R5a | Seat role meaning — **addition** (R-7) | The role meaning in force for the acting seat | DEL-05-01 / DEL-02-01 | *unknown* where not determinable |
| R6 | Autonomy settings | Every settings version in force, requested or refused for the run: scope; per-class grant value and class value; display state (§8 list); requester; setting actor; A12 act reference for person-set states; policy-class record reference and default for *effective (policy default)*; establishment evidence or refusal reason | DEL-04-02 settings-in (§8); DEL-04-01 | Never shown effective without its evidence |
| R7 | Requested operations | One entry per submission, read, examination, or loop-side refusal (§5) | Loop/adapter trace; DEL-03-01; DEL-03-02; DEL-03-03 external dispatch entries | Required per request made |
| R8 | Checkpoints and arrivals | Per declared checkpoint: required act kind (closed list A4, A5, A6, A7, A12; outside → *invalid*; unrecognized → *not established*); **subject class** (own element, R2-17/R3-1): change items of a named proposal · named output · **objects a named output concerns** · objects changed by a named outcome · targets of the held call (kind (a) only) · grant setting; the **`governed`** flag where declared (WD-v0.7 §4.3.1; PROPOSED) — **addition** (R8-1); **hold support — governance phase (retained), governed checkpoints only; none recorded in Phase 1 (R8-1)** — on the acting surface, one of the four R5-1 values (owner EXEC §3.6): **enforced by the host loop** (embedded route; host evidence DEP-001) · **enforced on the host route** (host-held constraint, evidenced by SQ-02 and a candidate) · **not established** (awaiting a host answer or unagreed exposure; against SWBPIPE neither cause now applies, SQ-02 and SQ-11 being answered, R8-2; the workflow requirement check is *not established*, never a pass and never *unsupported*) · **not enforceable** (no mechanism on this surface; workflow *unsupported*) — **addition** (R4-2; R5-1). The value is classified by the checkpoint's **held actions** (R6-1): if every held action is a host operation (HS-3), SQ-02 answered with host-held carriage evidenced → *enforced on the host route*, unanswered → *not established*, answered with no host-held route → *not enforceable* (SWBPIPE: answered with none, 2026-09-28); if any held action is App-side (App agent turn, App tool/harness action, App file write or return step), in App runs → *not enforceable* (HS-5, D6); host loop → *enforced by the host loop*; an invalid declaration takes **no value** (HS-1; governance phase: check *not established*; Phase 1: recorded as a declaration finding, invalid with its FB code, which does not change the check, R8-11 item 3); governing checkpoint constraint issued with its carriage assurance (governance phase). **Per arrival** (EXEC §4.1): **arrival ordinal**, arrival event and its evidenced time, bound subject referents and their content identities, **request observation** (R16: *request recorded* with its reference, or *request not identified* — an explicit absence, never a defect; PROPOSED, §13.6) — **addition** (RS 5), disposition (waiting · performed · resolved negatively · lapsed · not reached · unknown; record labels in Phase 1, where *waiting* means "reached; act not yet recorded", R8-11 item 1), **performance ordinal**, satisfying act / A10 / act-declined references, per-item decisions (A5 · A10 · undecided · left · unknown) with *partial* annotation and item-left events, annotations (lapsed at ‹t›; **waiting — re-held, lapsed at ‹t› after resume** (governance phase); **replaced by arrival n+1**; **A12 awaiting control confirmation**; **A12 refused by control: ‹reason›**; **by earlier act ‹act› at ‹t›** (L-13); **answered by ‹n› acts**, each with its referents (L-7); **prior act not counted**, with its reason (content no longer current · another act kind · captured before arrival (governance-phase option); the one wording, L-13, R12-10); act order unknown (that option only); act on other content; subject absent; hold not enforceable (governance phase); **continued past ‹checkpoint› before ‹act›** (Phase 1, optional, R8-1); **after run end**), run-resumed events, act-lapsed events, run-ended event if the run ended while waiting | DEL-02-01 declares; DEL-02-03 hold machine (App); DEL-05-01 (host) | Not observed → *not reached*. Run ended while waiting → stays *waiting* with run-ended event |
| R9 | Human acts | References to human-act records (including A15, R12-5), act-declined events and act-lapsed events | §6 | None created without capture evidence |
| R10 | Agent examination findings | References to A3 findings (e.g. C OP-C3) | Agent output | Never "host checks passed" (that is a host check, e.g. C OP-C12), never A4. Host-stored findings through a change operation are also R7 (U-14) |
| R11 | Evidence limits | Lost acknowledgement; missing receipt; unresolvable reference; origin mismatch; omitted governing checkpoint constraint; constraint carried only model-supplied; **unverified caller identity** (R4-15); cited basis not observed; agent-written configuration; native hint mismatch (DEL-03-03); **host reachable without evidenced A13** (R8-6); **constraint not carriable on this host** (R8-10; a record fact in either phase: in the current phase it says that the expected governing constraint could not be carried and was recorded only, ADAPTER GC-4 and P §3.3; it bears on a hold-support value only in the governance phase; R10-2); **subject identities not supplied** beyond a whole-model identity (R8-4) and **failing targets not supplied** under a host's whole-model staleness scope (R8-3); **action during hold** (governance phase, governed checkpoints; in Phase 1 the optional R8-1 annotation "continued past ‹checkpoint› before ‹act›" is used instead and is not an evidence limit) — each **run** action taken while an arrival was waiting and not stopped by the hold (every run action under *not established* / *not enforceable*; under *enforced on the host route*, every action other than the refused host operations), with its reference and its **turn initiator** — *person-directed* · *agent* · *App rule* (R4-2; R6-3; R6-5; EXEC HD-4, F-24); the person's own operations (e.g. an undo) are never action during hold (R5-5); **process network not observed** for an outside process that is not sandboxed, and **destinations not observed** where the host's native layer reports none (R8-13; R15); **stateless revision declared, not verified** for an MCP server allowed on the evidence of LOOP-v0.8 §5.3 DF-7 (node B5; PROPOSED); unobserved adoption; **record write failed**, **partial entry not recovered** and **recorders disagree** — the record's own completeness limits, written by the writer (§14.1 W-0, W-2) or found by the reader (§14.2 R-8) — **addition**, PROPOSED (RS 7). ADAPTER's "resubmission without prior observation" and "App-restart interruption" are not listed: a ruling proposal is with the integrator (R12-9; U-31; §14.3 FC-9) | Record writer; DEL-03-03; DEL-02-03; host native layer (R15) | Required |
| R12 | Record identity elements | §3 common elements | Record writer | Required |
| R13 | Tool-permission settlements (A14) — **addition** (D3; R2-8) | Each tool-permission request and its settlement origin: the person via interaction; the user's own Codex mode inside the supplier; an App named-rule decline or explicit error (INTEGRATION: the App never answers affirmatively by rule) | DEL-01-01 observed facts in this undertaking; DEL-01-02 later (D1) | **Only here**. *Not applicable* in host-loop runs (D3) |
| R14 | Compatibility-report reference — **addition** (R4-11; EXEC §3.3) | Reference to each required-tool compatibility report evaluated for the run (report identity CR-1, occasion, pass result CR-10, per-checkpoint hold support CR-9 — governance phase; in Phase 1 checkpoints are listed as guidance) | DEL-02-03 | "no report evaluated" stays explicit |
| R15 | Network destinations of a host's agent (ScopeOfWork REQ-002 and CLM-002; V4-HI-70 and PRD V4-HOST-02 as amended by SCA-V4-001; R8-13; DECISION-5) | Host-loop runs, in any model mode. **Destination contacted**, per request: destination; category; the grant or list entry that allowed it ("model choice" for the model service and its sign-in service; "category: ‹c›"; a named entry; an in-work grant with its scope); time; for the model service, the class **local** or **cloud** as the person's model choice states it (R12-7; B5). **Destination grant**: scope (once · this run · always); destination or category; time; source (allow list · in-work); reference to the A12 human-act record, subclass network-destination grant (R9; ACT §2.7). **Destination requested** — **addition** (RS 5; LOOP §2.3 "Destination request issued"): requester; destination or category; purpose; scope sought; the requesting call (the call to the host's destination request entry) and the call it carries, required for scope once (B5; LOOP-v0.8 §5.3 DF-1). **Destination request closed** — **addition**, PROPOSED (B5; LOOP DF-6): the request; state *not granted* (reason: not grantable · grant refused by control · prompt not shown) or *unanswered at end* (cause: run ended · turn cancelled); the carried call not sent; time. **Destination declined** (recording PROPOSED, R12-10: V4-EXM-23 says the decline is reported to the agent, and no accepted text says it is recorded; the act-declined event is INTEGRATION, R2-5 and R8-13): destination; time; the requesting call; reference to the act-declined event of kind A12; the outcome reported to the agent, "destination not allowed by the person". **Boundary refusal** (recording PROPOSED, R11-5, R12-10): destination; category; stage (model request · V-D · at contact; B5, LOOP DF-4); reason (not allowed · always-off item · not stateless MCP (2026-07-28)); the call, where there is one. **Outside process**: identity; declared destinations; sandboxed or not; when not sandboxed, the R11 limit **"process network not observed"**; for an MCP server, its stateless evidence (discovery lists 2026-07-28; per-request metadata only; no session identifier seen; LOOP DF-7) and the R11 limit "stateless revision declared, not verified" (B5). Information and evidence only, never a permission | Host native layer and control, through DEL-05-01 events (LOOP §2.3, §5.1.1); DEL-04-01 §2.7 | Required in host-loop runs. Where the native layer reports none: "destinations not observed" (R11). *Not applicable* in App runs, whose model destination is R5; DECISION-5 does not govern the App's own Codex (HOSTING §2) |
| R16 | **Act requests** — **addition** (RS 5; representation PROPOSED, §13.6) | Each request an agent makes of the person for an act (A8), where it can be identified: requester; act kind; subject; purpose; scope; the arrival it serves, if any; how it was identified; a reference (not a copy) to the message or event that carried it; time. At a declared checkpoint the agent's A8 is the request V4-WF-05 requires (DECISION-K1 K1-1; ACT AP-12); recording it where it can be identified is required (ACT AP-5, R11-1; EXEC PH-6). A request never satisfies anything and is never shown as the act (HA-1). Destination requests are R15 | DEL-02-03 (App: how a request is identified, Wave B node B2); DEL-05-01 (host: "A8 request issued", LOOP §2.3); DEL-03-03 (a not-permitted outcome after which an A8 is issued) | Where no request is identified, the arrival carries "request not identified" (R8); never a defect of the run |

### 4.1 Elements added in v0.4 (R4-11)

| Element | Home |
|---|---|
| Arrival ordinal; performance ordinal | R8 (per arrival) |
| Run-resumed event | §3, R8 |
| Re-held and replaced annotations | R8 |
| A12 control effect (established · pending · refused · unconfirmed) | R8 annotations; §6.1 relations; L-0 |
| "Prior act not counted" | R8; L-13 |
| Continues ⟨run⟩ | R1; §3 run finality |
| Action during hold (governance phase from v0.6; Phase 1 uses the R8-1 "continued past" annotation) | R11 |
| Transfer links; revision verification | R2 |
| Compatibility-report reference | R14 |
| Model destination | R5 |

### 4.2 Elements added in v0.6 (R8)

| Element | Home |
|---|---|
| `governed` flag (where declared) | R8 |
| "continued past ‹checkpoint› before ‹act›" (Phase 1, optional) | R8 annotations; R7 entry |
| Host reachable without evidenced A13; constraint not carriable on this host; subject identities not supplied; failing targets not supplied | R11 |

### 4.3 Elements added by R8-13 (in place)

| Element | Home |
|---|---|
| Destination contacted; destination grant; destination declined; boundary refusal; outside process with declared destinations | R15 |
| Process network not observed; destinations not observed | R11 |
| A12 network-destination grant records; act-declined events of kind A12 for a declined destination | R9 (§6) |

### 4.4 Elements added in v0.8 (Wave B, node B4)

| Element | Home | Standing |
|---|---|---|
| Act requests | R16 | Element required where identified (ACT AP-5; EXEC PH-6); representation PROPOSED |
| Request observation per arrival (*request recorded* · *request not identified*) | R8 | PROPOSED |
| Destination requested | R15 | PROPOSED element over LOOP's "Destination request issued" event |
| Destination request closed; the carried call; boundary-refusal stage; model-service class; MCP stateless evidence (node B5, LOOP-v0.8 §5.3) | R15 | PROPOSED |
| Stateless revision declared, not verified (node B5) | R11 | PROPOSED |
| A15 register workflow revision | R9; §6.1 | Act kind INTEGRATION (R12-5); record elements PROPOSED |
| Record write failed; partial entry not recovered; recorders disagree | R11 | PROPOSED |
| Record states (pending write · written · corrected · partial · read limited · refused · nonconformant) | §3 | PROPOSED |
| "Prior act not counted" reason (content no longer current · another act kind · captured before arrival (governance-phase option)) | R8; L-13 | Wording fixed under R12-10; the reason element PROPOSED |

## 5. Operation entries and outcome evidence

**Entry elements (semantic).** Operation identity and version (DEL-03-01);
**request-side origin** per DEL-03-02 §3.3: author type (person / agent),
author identity (the person, or the agent seat instance; over the external
channel **unverified** until a caller-identity mechanism exists, R4-15),
seat role meaning, channel, conversation, workflow identity (R2), workflow
run, standing at drafting, settings reference at route decision, settings
reference at application (host-reported, otherwise *unconfirmed*), reason,
and, in the governance phase, the **governing checkpoint constraint** {workflow run, checkpoint name,
required act A5, operation} with its **carriage assurance** ∈ {host-held,
model-supplied, absent; App-assured is **not available in this increment**}
(R2-12; R4-14; R5-2). Host-held means the host derived the constraint from its
own resolved declaration copy or verified a received one against it
(including the host loop's own evaluation); a constraint the host only
received keeps its source's assurance. Only host-held satisfies R2-12;
model-supplied or absent is an R11 limit; **host origin-mark reference**
(linked; mismatch → R11); **relied-on basis**; **observed basis** for reads
and examinations; **evaluated basis** on every non-success; route (direct /
proposal); treatment at resolution where it differs from standing at drafting;
**proposal identity**, lineage, per-item **change-item content identity**;
item dispositions with actors; **outcome**; receipt references; **resulting
objects** (R2-14); standing received; **submission ordinal**; **reverses
⟨receipt⟩ (entry ⟨ref⟩)** for an undo; **observer** for outcome unknown;
whether the action was taken **during hold** (R11; governance phase) or, in Phase 1, carries the optional **continued past ‹checkpoint› before ‹act›** annotation (R8-1); for an operation that performs a reserved act, the **reference to the human-act record** it produced (R5-6).

**Outcome vocabulary** is DEL-03-02 §9 and DEL-03-01 §4.1, adopted unchanged
(R-7), with R2/R4 amendments:

| Outcome as recorded | Minimum evidence referenced | Actor / observer | May NOT be inferred from |
|---|---|---|---|
| not offered (loop-side, never dispatched) | Operation absent from the catalog edition offered to the loop (R2-4) | Loop | Any host response |
| unavailable | Failed precondition, reason, evaluated basis (HI-04 parity) | Host | Channel off; a class reason |
| not exposed on this surface | Host-declared per-surface exposure element, relayed (R2-4); or a host-reported refusal of the method or change, e.g. SWBPIPE `unsupported_method` / `unsupported_change` (R8-5; R2-4 then recorded as not met by that host) | Host (relayed by loop/adapter) | *unavailable*, *missing*, *channel not enabled*, *not permitted*, or a class reason |
| channel not enabled | External access off; A13 not performed | **App** when its own configuration is off; **host** when the host channel is off (R4-16). SWBPIPE has no such code: its `controller_unavailable` is recorded as *endpoint unavailable* (App-observed), and the channel stays *disabled* because A13 is never evidenced there (SQ-13, SQ-28; R8-6) | *unavailable* |
| not permitted | Governing treatment and policy record — or the governing checkpoint constraint — and evaluated basis. Reserved entry: an A8 is **offered**; an A8 record exists only if issued (R2-4). Never converted into a proposal | Host route | A class reason rendered as unavailable or not exposed |
| error | Error identity, evaluated basis, effect statement | Host | — |
| drafted / validated | Host validation result (validated) with treatment and settings reference | Proposer (A1) / host | Agent assertion |
| refused — invalid | Host validation refusal with catalog error; includes SWBPIPE `validation_rejected` at Apply (R8-5) | Host | — (never "rejected", never A10) |
| refused — stale | Reason; relied-on and current bases; affected items, or the host's stated **staleness scope** where the host supplies no subject identities (e.g. SWBPIPE "whole model"; failing targets *not supplied*, R11) (R8-3) | Host | Local comparison alone; a retry's own effects (R2-13); an App-narrowed scope |
| queued | Host acknowledgement | Host | Transport completion |
| accepted (per item) | A5 human-act record bound to the item's change-item content identity | Person (A5) | Success, receipt, agent statement |
| rejected (per item) | A10 human-act record | Person (A10) | Host refusal; silence |
| withdrawn | A11 record | Proposer (A11) | A person removing another's proposal (A10); a host's queue clearing (SWBPIPE #885 `withdrawn`, recorded as an item-left event "cleared by the person, no decision record", never A10 or A11; R8-5) |
| applied (receipt) | Applied-outcome association: proposal/item, relied-on basis, receipt, resulting revision, branch, resulting objects with post-application subject identities (or *not supplied* beyond target ids, e.g. SWBPIPE: target ids, per-field diffs and the new whole-model hash, SQ-03 (d); R8-4) | Host | `success`, queued, accepted |
| application error | Error identity; effect *none* / *partial* (receipt references) / *unknown* (→ overlay) | Host | Any unstated effect |
| outcome unknown (overlay) | Observation gap; last observed state | The observer that lost observation | — |
| success (operation ran) | Result reference and observed basis | Host | Any human act |

Rules. **OE-1** Transport success, a tool-call return, source resolution or a
resolvable receipt *reference* never upgrades an outcome. **OE-2** A re-draft
after *refused — stale* is a new entry with a new proposal identity and
lineage. **OE-3** Each submission is its own entry, recording only the effects
actually observed; "one effect per proposal identity" is a host obligation
(DEP-001), not a recorded fact. **OE-4** A retry keeps the same proposal
identity; identity de-duplication precedes the basis check, and the retry
entry records what the host returned; it is never recorded as *refused —
stale* because of the proposal's own effects (R2-13). The staleness scope is
per item where the host supplies subject identities; otherwise the host's
stated scope is recorded (SWBPIPE: whole model), never narrowed (R8-3). **OE-5** A derived
proposal state is never stronger than its items. **OE-6** An undo is a change
through the one route with its own entry; *undone* is *applied (receipt)* with
**reverses ⟨receipt⟩ (entry ⟨ref⟩)**; it erases no act record; A5/A10 on the
reversed item are not lapsed; acts bound to subject content the undo changes
lapse under §7 (R2-15). Where the host's undo writes no receipt (SWBPIPE's
session undo, SQ-10), *reverses ⟨receipt⟩* is recorded *not supplied*, and a
lapse it causes is recorded from the identity change (R8-5, R8-4). **OE-7** Accepted then refused stale: both the A5
record and the *refused — stale* entry are present; A5 not lapsed; item not
applied (R2-16). On SWBPIPE accept and apply are one step per batch, with no
A10 record, so OE-7 does not arise there (SQ-01, SQ-23; R8-5). **OE-8**
**Phase 1:** a **run** action taken after an arrival and before the act that
answers it is recorded normally and may carry the optional annotation
"continued past ‹checkpoint› before ‹act›" with its turn initiator; it is
information, never a defect or evidence limit (R8-1). **Governance phase
(retained), governed checkpoints:** a **run** action taken while an arrival
was waiting and not stopped by the hold (R6-3) is recorded normally **and**
flagged *during hold* with its turn initiator (R11). In both phases an
arrival it produces is a separate arrival (EXEC MA-3), and the person's own
operations (proposals, applications, undo) are never flagged or annotated
(R5-5).

## 6. Human-act record

### 6.1 Elements (semantic)

| Element | Meaning | Required |
|---|---|---|
| Act identity | Identity of this record | Yes |
| Act kind | A4, A5, A6, A7, A10, A12, A13, A15, or A11 when the person is the proposer (ACT §2.4). Never A1/A2 (R7 entries), A9 (carried by recording mode) or A14 (R13 only). For A12, its subclass: operation-class grant or network-destination grant (ACT §2.7) | Yes |
| Act class | As applicable: "reserved to the person" for A4, A6, A7, A12, A13 (D2; disabling A13 INTEGRATION) and for A5/A10 where the active autonomy requires a proposal; for acts through a catalog operation, that operation's class from the DEL-04-01 policy-class record, including *no policy basis* with reason; for A15, "the person's act (V4-WF-02)" (R12-5; not a D2 reserved act) | As applicable |
| Governing policy reference | Policy-class record and policy revision identity (DEL-04-01 §8.1); DECISION-1 for D2/D3 | With act class |
| Decision actor | The person who performed the act. For acts the App captures, the person as the App observes them: the name the person set in the App, the operating-system account, and the Codex account when Codex reports one, marked **identity not verified** (SETTLED by DECISION-K1 K1-4; EXEC CAP-8; U-28 closed). A verified identity is a governance-phase matter | Yes |
| Recorder | Capturing surface, App, host facility, or agent | Yes |
| Recording mode (sub-element of A9) | *direct capture* or *faithful recording* (cites capture evidence) | Yes |
| Bound subject | Change item(s) (A5/A10); host row/object (A4/A6/A7); App file; setting content (A12/A13); a workflow revision (A15) | Yes |
| Bound content c₀ with method m₀ | A5/A10: change-item content identity; A4/A6/A7 on host content: subject content identity; App files: file content identity; A12/A13: the setting content (classes, grant values, scope); A15: the revision identity (its content identity, with method; R12-5) | Yes, or "not obtainable" → lapse permanently *unknown* |
| Scope | Change-item identities; row/object identities; setting scope | Yes |
| Purpose | What the act was for; at a checkpoint, the arrival's declared purpose it answers | Yes |
| Capture evidence references | From the capturing surface (host act facility; App interface per EXEC CAP-1…CAP-9; control surface for A12), each with resolution status. SWBPIPE exposes none (SQ-01, 2026-09-28; U-11) | At least one; without it the record is non-conformant |
| Evidence limits | What the evidence does not show (e.g. for App-captured acts, **identity not verified**: the actor is named from the App name, the operating-system account and any Codex account reported, not from a verified identity; EXEC CAP-8; DECISION-K1 K1-4) | Yes |
| Relations | Run, operation entry, arrival answered (if any; an earlier act counted at a later arrival is cited by it with its capture time, L-13; several acts answering one arrival each name it, L-7), workflow, decision record; for A12: **control effect** — established ⟨settings version⟩ · pending · refused ⟨reason⟩ · unconfirmed (R4-6); **superseded by ⟨act⟩** (L-0); **after run end** where captured after the run's run-ended event; the **act request** it answers, where recorded (R16); for A15, **derived from ⟨draft⟩**, the draft identity the revision derives from (R12-5; required for A15) | As applicable; no required prior act |
| Order | Capture time as evidenced; request relation to an arrival where the capturing surface records one | Yes |
| Lapse evaluation | Latest state with compared c₀/c₁ and m₀/m₁ (§7); derived. Not evaluated for A12/A13 | Derived |

### 6.2 Rules

- **HA-1** Written only from capture evidence that the person performed the
  act. Not such evidence: a proposal, success, grant, receipt, A3 findings, A8
  request, A14 settlement, silence, timeout, a chat statement, **an answer to a
  supplier user-input or MCP elicitation request** (R4-12; EXEC CAP-6), or
  **App-side configuration an agent could write** (never A13 evidence, R4-13).
- **HA-2** Decision actor and recorder are separate elements. A record naming
  the recorder as decision actor of A4–A7, A10, A12 or A13 is non-conformant.
- **HA-3** One record, one act kind. A5 never produces A4, A6 or A7. An
  independently evidenced act is recordable without any A5.
- **HA-4** A6 and A7 name the accountable person and scope only as evidenced;
  no certification label. A6 is engineering approval only.
- **HA-5** A12 and A13 are human-act records; R6 references A12. An agent's A8
  request creates no A12.
- **HA-6** Act class is carried, never computed here. *No policy basis* is
  shown "no policy basis — held (reason)".
- **HA-7** Faithful recording (A9) by any identified recorder distinct from
  the decision actor is a conformant record shape. It satisfies a checkpoint
  only through the capture evidence it cites (R-5; EXEC SP-3).
- **HA-8** For A5 the negative decision is A10; for A4, A6, A7 or A12 an
  act-declined event. Stopping the run is a separate run-ended event.
- **HA-9** No faithful record is made through a catalog operation that
  performs a reserved act (R2-2). App-side A9 records are DEL-04-03 files. A
  host-offered faithful-record operation, if any, must not change act state,
  must cite capture evidence, never satisfies a checkpoint and takes ordinary
  policy; whether any host offers one is a relay question.
- **HA-10 A15 register workflow revision (R12-5; DEL-02-02 REQ-002, AC-002,
  AC-006; record elements PROPOSED).** Written only from capture evidence of
  the person's explicit registration at the registration control
  (DEL-02-02's, a later undertaking, D1). Bound subject: the workflow
  revision; bound content: its revision identity with method; relation:
  *derived from ⟨draft⟩*; purpose: "make it available in the project".
  Draft creation, a successful trial, an agent's recommendation, a review of
  other content or a registration of an earlier revision is not evidence of
  it. A changed definition is a new revision and needs its own A15; an
  earlier A15 never carries over. No checkpoint may require A15 in this
  increment (ACT §4.1).

## 7. Content binding and lapse comparison rule

Notation: *S* bound subject; *c₀*, *m₀* bound content identity and method
designation; *c₁*, *m₁* the current identity of the same subject and scope.

| Step | Rule |
|---|---|
| L-0 | **A12/A13 are not lapse-evaluated.** A later A12 on overlapping classes and scope **that the control establishes** supersedes the earlier one; the record shows *superseded by ⟨act⟩*. A **refused** later A12 supersedes nothing: the earlier established setting stays in force. A **pending** A12 leaves an A12 arrival *waiting* ("A12 awaiting control confirmation"); a refused one leaves it *waiting* ("A12 refused by control: ‹reason›"); a lost confirmation makes it *unknown* (R4-6; EXEC §4.10). A checkpoint the earlier established A12 performed stays *performed*, with the supersession shown. Same rule for a later A13 on the same interface. **A15 is not lapse-evaluated either (R12-5; PROPOSED):** its subject is one revision, whose identity does not change; a changed definition is a new revision that needs its own A15 (DEL-02-02 AC-002), and a later A15 on another revision supersedes nothing. |
| L-1 | Obtain c₁ for exactly the bound subject and scope from one of three sources: change-item content identity (DEL-03-02) for A5/A10; subject content identity (DEL-03-01 §5.3) for A4/A6/A7 on host content; file content identity for App files. Never the workspace generation or model revision. **Whole-model identity (R8-4; INTEGRATION):** where a host supplies only a whole-model identity, it is received as the subject content identity of every subject it covers, with the host's method designation and scope; any model change then lapses every act bound through it (over-lapse, never under), and "subject identities not supplied" is an R11 limit. The App never computes an identity itself. SWBPIPE supplies only a whole-model hash (SQ-03 (a); U-29). |
| L-2 | Compare method designations. m₁ ≠ m₀ or comparability not shown → **unknown (incomparable)**. |
| L-3 | c₁ not obtainable → **unknown (unavailable)**. |
| L-4 | S no longer exists → **lapsed (subject absent)**. |
| L-5 | c₁ = c₀ → **not lapsed**. |
| L-6 | c₁ ≠ c₀ → **lapsed**, retaining c₀, scope and purpose; an act-lapsed event is recorded. |
| L-7 | Multi-element scope: evaluate per element. A batch A5 lapses per item. A multi-row A4 with some rows changed is **partially lapsed**; it keeps its purpose for the unchanged rows: a new act on the changed rows alone answers a checkpoint together with it, each citing its rows (SETTLED by DECISION-K1 K1-3; EXEC §4.7 JA-1; U-07 closed). |
| L-8 | Lapse never deletes or edits the act record. |
| L-9 | Host-presented lapse is linked where supplied; an App/host disagreement is shown and is an R11 limit. |
| L-10 | Applying an accepted change item does not lapse its A5. A basis failure between A5 and application is *refused — stale* (OE-7). An undo does not lapse A5/A10 on the reversed item; acts bound to subject content the undo changes lapse under L-6. |
| L-11 | Content returning to c₀ after an observed lapse is shown "matches c₀ again after observed lapse", keeping the lapse interval visible; effect is U-12. (SWBPIPE: the same content gives the same whole-model hash, while its DRAFT #885 revision still advances; SQ-03 (e).) |
| L-12 | **Checkpoint effect of a lapse (R4-3; EXEC HD-5, §4.7).** The **resume point** is the arrival's run-resumed event, recorded in both phases. *Before resume* (both phases): act-lapsed event recorded; the arrival returns to **waiting**, "lapsed at ‹t›". *After resume, run live — Phase 1 (R8-1; EXEC PH-8; R8-11 item 1; R8-12 item 1):* the act-lapsed event is recorded against the affected referents and labelled **"act lapsed at ‹t›"** (nothing says *waiting*); outputs whose promised standing names this checkpoint as gating show standing **lapsed**; **no re-hold** is recorded and nothing is stopped; the person's own operation that caused it is recorded as such; a later satisfying act is recorded with the next performance ordinal. *After resume, run live — governance phase (retained), governed checkpoints*: act-lapsed event recorded; the **same** arrival (same referents) returns to **waiting**, "waiting — re-held, lapsed at ‹t› after resume" — whatever caused the lapse: a person's edit, **the person's own undo** (an R7 operation, never action during hold), or the run's own later action (R5-5); what "held" means follows the hold-support value (R6-3): under *enforced by the host loop* the run stops at its next action boundary; under *enforced on the host route* the host refuses the held host operations and every other run action is recorded as action during hold; under *not established* or *not enforceable* nothing is stopped and run actions are recorded as action during hold; nothing already done is undone; actions between resume and lapse stay recorded as taken under the earlier performance; outputs whose promised standing names this checkpoint as gating show standing **lapsed** for the affected referents; the act request is re-issued for the **whole** bound scope with lapsed referents marked; a satisfying act gives the next performance ordinal. If the run ends while re-held, the final disposition is **waiting** with the run-ended event. *After the run ended*: the disposition becomes **lapsed** per referent. **A5 and A12 never re-hold** (L-10; L-0); in particular an undo never re-holds an A5 arrival (R5-5). |
| L-13 | **Earlier acts (SETTLED by DECISION-K1 K1-2; EXEC SP-6; U-26 closed).** In the current phase an act captured before an arrival counts toward it when it is of the required kind and the content it was made on is still current (for A12, its established setting still in force); the record cites the earlier act and its capture time ("by earlier act ‹act› at ‹t›"). An earlier act on content no longer current, or of another kind, is recorded and shown **"prior act not counted"**. This adds no order between act kinds. **One wording (R12-10; V17-A N-4):** the record label is exactly **"prior act not counted"**, recorded with one reason — *content no longer current*, *another act kind*, or *captured before arrival (governance-phase option)* — and a display may add the reason after a dash ("prior act not counted — content no longer current"). "Prior act on this subject, not counted" and "prior act, not counted" are retired wordings of the same label; the PROPOSED schema refuses them (§13.3). **Governance-phase option (retained; PROPOSED; EXEC SP-6F; formerly this rule, R4-5):** a workflow that takes up the governance phase may require the act to be captured at or after the arrival's event — by a request relation where the capturing surface records one, otherwise by evidenced times; any earlier act is then "prior act not counted", and if the order cannot be established, "act order unknown" and the act does not count. |

Lapse states: not lapsed · lapsed · lapsed (subject absent) · partially
lapsed · matches c₀ again after observed lapse · unknown (incomparable) ·
unknown (unavailable) · not yet evaluated. For A12/A13: current · superseded.
For A15: not lapse-evaluated (L-0).
*Not yet evaluated* never renders as *not lapsed*.

## 8. Settings-in / record-out exchange with DEL-04-02 (CASE-002 M3)

Identical in DEL-04-02/AS-v0.8 §6. A data exchange, not an ordering between
human acts and not a second authority.

**Settings-in (DEL-04-02 → DEL-04-03 writer), per run and per change:** run
identity; settings version identity; **scope** (representation-neutral
dimensions, e.g. model/workspace, object set, run, period, consequence); per
operation class — **grant value** (direct / propose) and **class value**
(DEL-04-01 policy-class record reference; for *no policy basis*, its reason);
display state (effective (person-set) · effective (policy default) ·
requested by agent · set by person, not yet confirmed by control ·
unconfirmed · not set · refused (reason)); **requester** (person; agent via
A8; *none — policy default*); **setting actor** (the person, only where an
A12 exists; *none — policy default*); **setting act reference** (A12 record)
— or, for *effective (policy default)*, the **policy-class record reference
and its default value** in its place; **establishment evidence** (control
confirmation) or refusal reason; order relative to operation entries; source
of control (App or host).

**Destination settings of a host's agent (DECISION-5; ACT §2.7; carried
with the settings version, apart from the operation-class grants and never
merged with them):** the model service and, for a chosen cloud model, its
sign-in service, marked "allowed by your model choice"; each **category
switch** (on or off) with its display state and A12 reference; each **named
entry** with its category, its source (allow list · in-work, always), its
A12 reference and display state; the **always-off items**, each off unless
an A12 turned it on; each **in-work grant** with its destination or
category, scope (once · this run · always), state (pending control
confirmation · in force · consumed · ended with run · listed · superseded ·
refused (reason) · unconfirmed; AS §3.1), A12 reference and the request it
answers; and each **agent request** still open or resolved in the run, with
the scope sought and its state (pending · granted · declined · not
granted · unanswered at end, with its reason or cause; DEL-05-01/LOOP-v0.8
§5.3 DF-6). *Not applicable* for the App's own Codex, whose
model destination is R5. PROPOSED representation: DEL-04-02's
`AS_SETTINGS_IN.schema.json`, carried in the record as the body of a
`settings_version` entry (RS §13).

**Record-out (DEL-04-03 reader → DEL-04-02), per run:** record identity and
format version, and the read state of every entry that is not *written*
(read limited · refused · partial · nonconformant; RS §3 record states);
continues ⟨run⟩ where present; recorded settings versions
with the fields above; per operation entry the two settings references,
route, treatment at resolution, governing checkpoint constraint with carriage
assurance, outcome, item dispositions with actors, receipt/origin references,
resulting objects, *reverses* relations (or *not supplied* where the host
writes no undo receipt), evaluated/relied/current bases, the optional
*continued past ‹checkpoint› before ‹act›* annotation (Phase 1) and the
*during hold* flag (governance phase); human-act records, act-declined events and act-lapsed
events with actor, recorder, recording mode, kind, act class, bound subject,
scope, purpose, c₀/c₁ with method designations, lapse or supersession state,
A12 control effect, *after run end* marking and capture evidence references
with resolution status; act requests (R16) and each arrival's request
observation; checkpoint arrivals with subject class, the
`governed` flag where declared, hold support (governance phase, governed
checkpoints only; none in Phase 1), arrival and performance ordinals,
disposition as a record label, annotations, run-resumed and run-ended events;
evidence limits. For a host's agent, the **R15 entries**: destinations
contacted, each with its category and the grant or entry that allowed it;
destination grants with scope, time, source and A12 reference; destination
requests with the call each carries, and how each request ended (LOOP-v0.8
§5.3 DF-6); declines and boundary refusals (their recording PROPOSED: V4-EXM-23
reports a decline to the agent, and no accepted text says it is recorded;
R12-10); outside processes with their declared destinations; and the limits
"process network not observed" and "destinations not observed".

**Comparison (DEL-04-02)** per settings version: displayed vs recorded →
*match* · *mismatch* · *missing in record* · *missing in display*. Mismatch is
shown to the person and returned as a defect observation. The record is
authoritative for what was recorded; the control for the current grant; the
display is derived. Neither side auto-corrects the other. A person-set state
without an A12 reference, or an *effective (policy default)* state without a
policy-class record reference, is a defect, not an established setting.
Destination settings are compared the same way, entry by entry (switches,
named entries, always-off items, in-work grants with their states); a named
entry or an in-work grant shown in force without an A12 reference is a
defect, not a grant. Destinations contacted are not compared: they are read
from the record and shown by reference where they are displayed (PANEL
ND-4). A record-out whose version is refused gives *missing in record
(unreadable version ‹v›)* for every settings version; one read limited is
compared on its known elements only and says "read limited". "Destinations
not observed" is shown as that limit, never as "no destinations contacted".

## 9. Evidence references

Each reference carries: evidence kind (receipt, content identity, origin
mark, capture evidence, commit, supplier settlement, compatibility report,
carriage manifest), claimed identity, identity method designation where
applicable, and resolution status at write (resolved / unresolvable / not
supplied) and at read. "Resolved" means the source was found with the claimed
identity; it does not make the referenced change or act more than the source
states (OE-1).

## 10. Consumer and host interface

| Consumer | Consumes (meaning) | Supplies back | Held part / limit |
|---|---|---|---|
| DEL-02-01 | Act names; R8 subject classes and dispositions; R2 | Workflow identity; checkpoint reached-when, subject class, §4.3.7 mixed-item rule | Closed act list A4/A5/A6/A7/A12 |
| DEL-02-03 | R8 arrivals and events; R16 act requests (how an App run identifies one is EXEC's, Wave B node B2); R2 transfer links; R11 action during hold; R14 | Hold machine (§4), resume point, re-hold, finality and continuation, refused-A12 effect, SP-6, compatibility reports, transfer trace, App capture requirements (CAP-1…CAP-9) | D6 (U-25; closed for Phase 1, re-opens with the governance phase); SP-6 settled by DECISION-K1 K1-2 (U-26 closed), with the governance-phase option SP-6F |
| DEL-03-01 | R7 identity/basis; c₁ for A4/A6/A7 | Subject content identity; method designation; exposure element; shared fixture §10 | Algorithm unselected |
| DEL-03-02 | Nothing before its own work: P's outcomes are recorded under §5. No arc DEL-03-02 → DEL-04-03 is registered (N-12 was not proposed: DECISION-6 of `APP-V4-BASIS-ALIGN-20260928`; ARC_ANALYSIS §3.3) | §9 outcomes; change-item content identity; origin incl. constraint and author identity (may be unverified); resulting objects; item-left events | One-effect mechanism unselected |
| DEL-03-03 | Nothing before its own work: these name where the adapter's evidence lands — R5 destination; R7 external entries; R9; R11; R13. No arc DEL-03-03 → DEL-04-03 is registered (N-B8 was not proposed) | External dispatch entries; model destination class; evidence limits (cited basis not observed, omitted constraint, origin mismatch, agent-written configuration, unverified identity, native hint mismatch); A14 observations | Caller identity verification (U-27). ADAPTER §11 also names two evidence limits for R11 that R11 does not list ("resubmission without prior observation"; "App-restart interruption"): not yet defined here. Both texts stay. Wave B node B4 placed them against the record's writer and failure sequences (§14.3 FC-9) and returned a ruling proposal with both passages (`WAVE_B/B4.md`; R12-9); the integrator rules in R13 (U-31) |
| DEL-04-02 | Record-out (§8), including R15 and the read state of entries (v0.8) | Settings-in (§8), including a host agent's destination settings (v0.8; PROPOSED representation `AS_SETTINGS_IN.schema.json`) | Executable M3 trace needs a candidate writer/reader; the §15 prototype exercises the PROPOSED format only |
| DEL-05-01 | R3/R4/R5/R5a/R7/R8/R15/R16 meanings; the §13 entry kinds its events map to (LOOP E-4: "the field mapping is DEL-04-03's") | Observer-attributed unknown; origin, seat role, grant in force, constraint per dispatch (governance phase); loop-side *not offered*; host-loop hold support (governance phase; in Phase 1 a host loop enforces no hold, EXEC PH-2); run-resumed/run-ended; "A8 request issued" and "Destination request issued" events (R16, R15) | — |
| DEL-05-02 | Act, act-declined, lapse, supersession, annotation display meanings; R15 network destinations and the R11 limit "process network not observed" (PANEL §3.8 ND-4) | — | — |
| DEL-01-01 | R3, R5, R13 meanings | Supplied-guidance identities; per-turn requested/effective model and re-routes (HOSTING §8.3); A14 settlement origin (observed facts) | Pin 0.158.0 is definition only; whether requested and effective can differ is not observed (HOSTING U-19) |
| DEL-09-06 | Records of actual content-bound acts and the run record (DEP-09-06-015): R2 transfer links; R7 operation entries; R8 checkpoints and arrivals; R10 findings; §6 human-act records; the §4 inventory for the return (as CA §2.3 cites them) | Joined round-trip evidence | Host links AWAITING INPUT |
| DEL-09-09 | R7 external dispatch entries; R9 and §6 faithful act records; R11 evidence limits (XT IN-08: J-3, J-8, XC-09) | — | — |
| PKG-06 (DEL-06-01/06-02) | Act records; actor ≠ recorder; lapse | Decision records as act subjects | Coordination recorder never becomes actor |
| DEL-09-11 | Complete records for the week-later reconstruction (inspection replay, EXEC RP-6) | — | This format does not perform the witness |
| DEL-01-02, DEL-01-04, DEL-02-02, DEL-02-04 | R3/R4/R7/R13; act display; review/registration, recorded as **A15** (R12-5; HA-10); App act control | Observation evidence; role bytes; the registration control that captures A15; App capture control | Outside this undertaking (D1) |
| External host run recording (DEP-04-03-016; DEP-001) | §§3–9 | Receipts, origin marks, subject content identities, capture evidence and reference, lapse, per-operation settings version, constraint receipt, per-turn guidance, host holds (SQ-02; governance phase), channel restrictions on destination | Adoption unclaimed; OI-013 placement. SWBPIPE answered 2026-09-28 (relayed; no commitment or contribution, RELAY §4): no capture-evidence reference (SQ-01), no host-held route (SQ-02), whole-model identity only (SQ-03), whole-model staleness (SQ-07), session-only receipts (SQ-09), receiptless session undo (SQ-10), no A13 facility (SQ-28) |

### 10.1 Receivers and suppliers by register row (R9-6)

Rebuilt at v0.7 from the ACTIVE rows of this deliverable's `Dependencies.csv`
and of the other deliverables' registers. "Held" is a non-gating candidate
arc in SCC-002. Satisfaction is read from the live registers; no row records
it. The table defines no contribution.

| Receiver | This register's row | Receiver's own row | DAG-003 | §10 row |
|---|---|---|---|---|
| DEL-02-01 | none | DEP-02-01-019 | held | yes |
| DEL-02-03 | none | DEP-02-03-013 | held | yes |
| DEL-03-01 | none | DEP-03-01-031 | held | yes |
| DEL-03-04 | none | DEP-03-04-013 | admitted | no: named by DEP-03-04-013; the guide's consumption is not yet stated here |
| DEL-04-02 | DEP-04-03-014 | DEP-04-02-008 | held | yes |
| DEL-05-01 | DEP-04-03-029 | DEP-05-01-019 | held | yes |
| DEL-05-02 | DEP-04-03-030 | DEP-05-02-009 | held | yes |
| DEL-09-06 | DEP-04-03-031 | DEP-09-06-015 | admitted | yes |
| DEL-09-09 | DEP-04-03-032 | DEP-09-09-011 | held | yes (added at v0.7) |
| DEL-09-11 | DEP-04-03-015 | DEP-09-11-005 | admitted | yes |
| DEL-06-01, DEL-06-02 | DEP-04-03-013 (package row, PKG-06) | DEP-06-01-008, DEP-06-02-010 | admitted | yes (PKG-06) |
| DEL-01-04, DEL-02-02 | none | DEP-01-04-012, DEP-02-02-017 | held | yes (outside this undertaking, D1) |
| DEL-09-02, DEL-09-05, DEL-10-03 | none | DEP-09-02-019, DEP-09-05-010, DEP-10-03-014 | admitted | no: named by those rows; not yet stated here |
| PKG-02, PKG-03 | DEP-04-03-011, -012 (package rows) | — | not deliverable arcs | by deliverable, above |
| External host run recording | DEP-04-03-016 | — (DEP-001) | not a project arc | yes |

| Supplier | This register's row | Supplier's own row | DAG-003 | Contribution the register names |
|---|---|---|---|---|
| DEL-04-01 | DEP-04-03-021 | DEP-04-01-016 | admitted | Act kinds and classes |
| DEL-04-02 | DEP-04-03-022 | DEP-04-02-009 | held | Settings-in |
| DEL-03-01 | DEP-04-03-023 | none | held | Subject content identities and method designations |
| DEL-03-02 | DEP-04-03-024 | DEP-03-02-019 | held | Operation outcomes, change-item content identities and receipt links |
| DEL-02-03 | DEP-04-03-025 | none | held | Checkpoint arrival, act and lapse events, and compatibility reports; hold events are retained for the governance phase |
| DEL-03-03 | DEP-04-03-026 | none | held | External dispatch entries |
| DEL-01-01 | DEP-04-03-027 | none | admitted | Observed supplier facts: supplied guidance, model and destination, tool-permission settlements |
| DEL-05-01 | DEP-04-03-028 | none | held | A host agent's network-destination events: destination contacted, destination grant, destination declined |
| DEL-01-02 | none | DEP-01-02-020 | admitted | Compact observation evidence, observed events and outcome gaps (a later undertaking, D1; U-20) |
| DEL-02-04 | none | DEP-02-04-012 | held | Role-specific source identity, supplied bytes and enforcement-limit evidence (outside this undertaking) |

The arcs N-18, N-21, N-24 and X-1 have no end at DEL-04-03. X-1's
contribution (DEL-01-04's App act control and person identity) was U-28,
closed by DECISION-K1 K1-4: the person identity the App records is settled
(§6.1); the act control's construction stays with DEL-01-04, and its
obligation is proposed for DEL-01-04's contract at the next amendment
(DECISION-K1 K1-4); collected at this run's closeout.

## 11. Excluded acts and owners (REQ-006)

OI-001/OI-002 were decided at App/shared level by the Owner in DECISION-1
(D2, D3); D5 by the Owner in DECISION-2; D6 was deferred by the Owner to the
SWBPIPE answer (SQ-02), and is closed for Phase 1 by DECISION-4, re-opening
only with the governance phase (R8-2; SQ-02 answered 2026-09-28: none). Operation-specific additions remain with the Owner via
the outside SWB session and App/shared owner (OI-021; ScopeOfWork TBD-001 as
revised by SCA-V4-001).
Defining and carrying policy — DEL-04-01. Autonomy/standing UI — DEL-04-02.
Hold machine and transfer — DEL-02-03. Reconstruction witness — DEL-09-11.
Host domain changes, receipts, storage, host run recording, host enforcement
of its reserved list and its own channel restrictions — responsible host owner
(SWBPIPE outside session). Performing any human act — the person. Professional
reliance and certification — the accountable professional. This format
faithfully records evidenced acts; it performs none.

## 12. Examples (fixture subjects — invented; no act was performed)

All identifiers are DEL-03-01/C-v0.4 §10 (commit 8fb51f07f; carried in C-v0.7 §10): FX-PIPE-01,
FX-W1, g1, run R-100 (fixture run 12, conversation K-7), supports S-1…S-4 and
S-5 (created at T12), Engineer A, workflow `supports-adjust` (origin *host*,
⟨fx-root⟩, ⟨rev-3⟩, declaring `CP-accept` and `CP-check` per FXA-5), bases
B1/B2, PR-1/PR-2, RC-1…RC-3, ⟨set-1⟩/⟨set-2⟩, T1–T17 and T16a, variants V-S1,
V-CP1, V-NP1, V-R1, V-X1, V-OU1, V-ED1, fixture assumptions FXA-1…FXA-5,
App-side subjects LIB-A1, LIB-A2, AF-1. **V-GR1** is
cited from C-v0.5 §10.4 (run 13; GR-1…GR-3; GR-P, GR-R, GR-S). Local cases are `L-RS-n`, each saying why.

**E1 — Stale, re-draft, per-item decisions, application (T3–T12).** T3 OP-C1
→ B1. T5 PR-1 relies on B1 (item 1 OP-C4, item 2 OP-C5). T6 Engineer A edits
S-3 (r13). T7 both items **refused — stale** (relied B1, current B2). T9 PR-2
(lineage PR-1) on B2; T10 queued — `CP-accept` **arrives** (FXA-5; PR-1 was
never queued). T11 Engineer A operates OP-C7: it performs the reserved act
and produces ⟨act:1⟩ **A5** on item 1 (host facility, direct capture, c₀
⟨ci:PR-2/1⟩ ⟨m-fx⟩, "reserved to the person (D2b)"); the OP-C7 R7 entry
references ⟨act:1⟩ (R5-6). OP-C8 likewise produces ⟨act:2⟩ **A10** on item 2.
`CP-accept` → **resolved negatively**, *partial* (item 1 A5, item 2 A10).
T12 applied item 1: RC-1, r14, resulting objects {**S-5** created ⟨S-5@r14⟩;
R-100 changed ⟨R-100@r14⟩}. ⟨act:1⟩ stays **not lapsed**. `CP-check` is not
scheduled on C's timeline.

**E2 — Faithful recording (T2).** OP-C6 by Engineer A produces the host's own
direct-capture record (capture ⟨cap:T2⟩; R5-6). The App agent writes ⟨act:3⟩: A4, recorder App agent, faithful recording, c₀
⟨S-2@r12⟩, evidence ⟨cap:T2⟩. Conformant as shape; an App file, not a catalog
operation.

**E3 — Negatives.** (a) T5 PR-1 drafted only → no act. (b) T4 OP-C3 → R7
*success* and R10 findings, never "host checks passed"; T4a OP-C12 is the host
check ("host check failed: support spacing"). (c) T15 grant alone → no act on
content. (d) Transcript "Engineer A approved" → nothing; R11. (e) Codex
tool-permission prompt answered by the user's mode → R13. (f) **V-R1** agent
calls OP-C6 → *not permitted*, A8 offered; no automatic A8. (g) An answer to a
supplier elicitation "yes, mark it checked" → not act evidence (R4-12).

**E4 — Lapse and control (T2, T6, T14).** T6 edits S-3 → ⟨act:3⟩ not lapsed.
T14 edits S-2 → lapsed, act-lapsed event, c₀ retained. **L-RS-1** (C has only
single-row A4s) — A4 on S-1 and S-2 at r12; T14 → partially lapsed; an A4 on
S-2 alone would answer a checkpoint together with the earlier act for S-1
(L-7; DECISION-K1 K1-3).

**E5 — Retry and unknown (T13; V-OU1).** Resubmitting PR-2: the host reports
the recorded state (item 1 applied RC-1, item 2 rejected) → second entry
records that; never *refused — stale*. V-OU1: neither report observed →
*outcome unknown*, observer loop, last observed *accepted*.

**E6 — Direct and undo (T15–T17, T16a).** T16 OP-C9 applied directly (S-4
label "G-4"): RC-2; settings at route decision ⟨set-2⟩, at application
host-reported or *unconfirmed*. T16a Engineer A A4 on S-4, c₀ ⟨S-4@r16⟩. T17
OP-C10 → RC-3 **reverses RC-2** (entry T16); T16a's A4 **lapsed** (label
restored; subject identity covers the label per C FXA-2). T17 is Engineer A's
own R7 operation: never *action during hold*. If T16a had performed a
checkpoint arrival after its resume point (DEL-04-02 F6), T17's lapse is
recorded against that arrival in both phases. In the governance phase it
**re-holds** that arrival (R5-5); in Phase 1 nothing re-holds (R8-1). It would
never re-hold an A5 arrival.

**E7 — Grant change (T15; V-GR1).** Main timeline: ⟨act:5⟩ **A12** at T15
(produced by the host control, R5-6): bound setting content {class P-03,
grant value direct, scope {model/workspace FX-W1; object set {S-4}}}; control
effect **established ⟨set-2⟩**; no expectation for OP-C5 on S-4 (held on
U-02). Run 12 (⟨rev-3⟩) declares no `CP-grant`, so T15 counts toward no
arrival. **V-GR1** (C-v0.5 §10.4, run 13 on surface E; governance phase: hold support *enforced by the host loop*): a run of WD-EX E1d in which `CP-grant` (A12,
kind (a) before dispatch of OP-C9, declared content {P-03, direct, {FX-W1;
{S-4}}}) arrives at r15 when the OP-C9 call on S-4 is held; T15's A12 is
captured **after** the arrival → control establishes it → arrival
*performed*; the held call is dispatched unchanged as T16. Sub-variants:
GR-P *pending* → waiting "A12 awaiting control confirmation", then *unknown* when the confirmation observation is lost, the call staying held; GR-R *refused* → waiting
"A12 refused by control: ‹reason›", ⟨act:5⟩ supersedes nothing and **⟨set-1⟩** stays in force; GR-S a later
**established** A12 narrowing the scope → ⟨act:5⟩ *superseded*, arrival stays
*performed* with the supersession shown. **Phase 1:** these are record
labels; no call is held by the loop or the App, the OP-C9 dispatch is
recorded as observed, and no hold-support value is recorded; the
requirement check via X passes on required tools and channel state (EXEC MT-16, CH-12).
**Governance phase:** the call stays held under GR-P and GR-R; from the App
via X, `CP-grant` hold support is **not enforceable** (HS-3 (c) on OP-C9;
SQ-02 answered 2026-09-28; was *not established* at v0.5); E1d's `CP-check`
is *not enforceable*, so the run via X is *unsupported* (EXEC MT-16). An A12
captured before the arrival counts while the setting it established is still
in force, cited with its time (L-13; DECISION-K1 K1-2); it is "prior act not
counted" only under the governance-phase option.

**E8 — Stale after acceptance (V-S1).** After T11, S-2 edited before T12
(r14′) → *refused — stale* (relied B2, current ⟨B-r14′⟩); ⟨act:1⟩ present,
not lapsed; item 1 not applied.

**E9 — No policy basis (V-NP1).** OP-C11 direct → *not permitted* (no policy
basis, pending OI-021); proposal → queued, confers no permission; A12
widening → refused (reason: no policy basis); fixture result **held**.

**E10 — Checkpoints, arrivals and hold (L-RS-5: C FXA-5 declares `CP-accept`
and `CP-check`, neither with the R3-1 subject class).** App run of a workflow
on surface X (App conversation, host reads over the external channel).
Checkpoint *CP-row-check* requires A4, subject class **objects a named output
concerns** = the spans named in T4a's OP-C12 output (S-2, S-3), reached-when
*on production of that output*. Its held actions are the run's next actions,
which include App agent turns (e.g. the agent's drafting of PR-1 at T5 in the
App conversation). Each step gives the **Phase-1 record** and, where a hold is
involved, the **governance-phase value**, reading *CP-row-check* as if
declared `governed` (no fixture declares the flag; R8-11 item 5).

- **Phase 1 (R8-1).** No hold-support value is recorded, and the requirement
  check is decided by required tools and channel state. (i) Arrival 1 at
  T4a is recorded. T2's A4 on S-2, whose content is still current, counts
  for S-2 and is cited with its time; the arrival stays unanswered for S-3
  (L-13; DECISION-K1 K1-2). Under the governance-phase option (EXEC SP-6F), T2's A4 is "prior act not counted" and the arrival waits for an A4 on S-2 and S-3 captured after T4a.
  (ii) The agent's next dispatch (T5 drafting PR-1) proceeds → R7 entry,
  optionally annotated "continued past CP-row-check before A4" with turn
  initiator *agent*; no R11 limit, no stop. (iii) Engineer A performs A4 on
  S-2 and S-3 (host capture; App faithful record) → *performed* (record
  label), performance ordinal 1; run-resumed event at the next run action.
  (iv) T6 edits S-3 → act-lapsed event recorded for S-3, labelled "act
  lapsed at T6" (R8-12 item 1); the gated standing shows lapsed; **no
  re-hold** is recorded (L-12). (v) Variant: Engineer A
  declines → act-declined event → *resolved negatively*. (vi) Variant: nobody
  acts and the run ends → run-ended event; arrival stays **waiting**.
  (vii) Variant: a kind (a) checkpoint whose only held action is a host
  operation over X → recorded the same way, with no hold-support value.
- **Governance phase (retained).** App-side held actions, so hold support is
  **not enforceable** in the App run (R6-1 HS-5; D6), whatever SQ-02 returns,
  and the workflow requirement check reports *unsupported* (reason:
  checkpoint hold not enforceable on this surface: CP-row-check). The arrival
  is still recorded (EXEC HD-4). (ii) The T5 dispatch is flagged *during
  hold*, R11 "action during hold", turn initiator *agent*; no stop is
  claimed. (iv) Arrival 1 **"waiting — re-held, lapsed at T6 after
  resume"**; no stop is recorded; later run actions are flagged *during
  hold*. (vii) HS-3 (c): **not enforceable** — SQ-02 was answered on
  2026-09-28 with no host-held route; the requirement check is
  *unsupported* (was *not established* at v0.5); nothing is stopped; action
  during hold is recorded. It would be *enforced on the host route* only with
  an evidenced host-held route (the host would refuse that operation; other
  run actions would be action during hold).

**E11 — After run end and continuation (L-RS-6: run finality has no C step).**
After E10 (vi), Engineer A performs A4 on S-2/S-3 → recorded, marked **"after
run end"**; the ended run's arrival stays *waiting*. A new run starts with
**continues ⟨run 12⟩**; its CP-row-check starts *not reached*; when it
arrives, the post-end A4 counts if S-2's and S-3's content is unchanged since
that A4: *performed*, citing it and its time (L-13; DECISION-K1 K1-2). Under
the governance-phase option it is **"prior act not counted"**.

**E12 — Model destination (D16; DEL-03-03 L-ADAPTER-8).** An App run whose
conversation requested a user-chosen cloud model reads OP-C1 over the external
channel. R5 records per turn: turn 1 requested = effective = cloud model M1;
turn 2 a supplier re-route M1 → M2 recorded with its turn; turn 3 not observed
→ *unknown*. Run-level value: the set {M1, M2, unknown}. No gate, no new run,
no grant change, no act.

**E13 — Network destinations in a host-loop run (R8-13; L-RS-7: C has no
network subjects).** Cloud chosen and signed in; web access switched on;
named MCP entry M-1 (stateless 2026-07-28), not sandboxed, declaring D-1.
- Turn 1 contacts the model service → R15 contact, allowing entry "model
  choice".
- The agent's tool fetches W-1 → R15 contact W-1, category web access,
  allowing entry "category: web access".
- The agent asks for A-1 (A8), and Engineer A grants it once → an R9 A12
  record (network-destination grant), an R15 grant (once, time, in-work)
  and one R15 contact.
- A later request for A-2 is declined → an act-declined event (A12) and
  an R15 decline, "destination not allowed by the person" (its recording
  PROPOSED, R12-10).
- M-1 is started → an R15 outside process with declared D-1, and the R11
  limit "process network not observed".

No operation-class grant changes (R6), and no act is recorded beyond the
two acts of the person.

## 13. Record format — PROPOSED (RS 8; R12-1, R12-2; U-04)

**Standing.** PROPOSED by DEL-04-03 in Wave B. Nothing here is accepted. The
format is written as a schema with conformance fixtures, which every
placement option needs (R12-2); no placement, path, persistence location,
identity algorithm or canonicalization is chosen (OI-013, OI-014, U-05,
U-16; DEL-03-01 TBD-003). Element spellings are Chirality's own; no wire
field of a host or supplier is selected.

| File (beside this one) | What it is |
|---|---|
| `RS_RECORD.schema.json` | JSON Schema 2020-12, `$id` `urn:chirality:app-v4:del-04-03:rs-record:0.1`: one record entry, its common header and one body per kind. A `settings_version` body is DEL-04-02's `AS_SETTINGS_IN.schema.json` (`urn:chirality:app-v4:del-04-02:settings-in:0.1`), referenced by `$id` |
| `RS_RECORD.valid.host-run.example.jsonl` | 20 entries: a host-loop run (E13's destinations with an in-work grant, a decline, an unsandboxed process and a refusal; `CP-L4` with the agent's request and the person's A4) |
| `RS_RECORD.valid.app-run.example.jsonl` | 20 entries: an App run over X (E10 (i)–(iv) in the current phase: an earlier act counted for S-2, the request, a faithful record of the A4 on S-3, the joint answer, resume, lapse "act lapsed at T6", a correction; R3, R10, R13, R14 entries) |
| `RS_RECORD.valid.act-log.example.jsonl` | 3 entries outside any run: an A15 registration, an App-file A4 on AF-1 and its lapse |
| `RS_RECORD.valid.host-destinations.example.jsonl` (node B5) | 12 entries of host-loop run E-14, written by DEL-05-01's `prototype/destination_flow.py` (LOOP-v0.8 §5.3): a model-service contact with class *cloud*; a V-D refusal; a request carrying its call, granted once, and the contact; an MCP server with stateless evidence and both limits; a legacy-answering server refused; a request ended *unanswered at end* by a turn cancel |
| `RS_RECORD.invalid.examples.json` | 11 entries that must fail, each with its reason (INV-RS-10, INV-RS-11 added by node B5) |

### 13.1 Unit of storage

| Option | Unit | For | Against |
|---|---|---|---|
| **S-A (PROPOSED)** | One append-only log per run and writer, one entry per line (JSON Lines, UTF-8, each line ended by a line feed), plus one act log per writer for acts captured outside any run | A written entry is never rewritten (OF-5); a torn write damages at most the last line; each writer's order is its own; an ordinary text file that version control can diff (OF-6, D13) | A run view joins several logs; the reader merges them |
| S-B | One document per run, rewritten at each change | One file to read | Rewrites earlier content; a failed rewrite can lose the whole run record; conflicts with OF-5 |
| S-C | One file per entry | No torn lines | Many files; order needs a separate index |
| S-D | One log per workspace for all runs | One stream | Runs contend for one file; large files |

A **writer** is the component that appends: the App writer (App runs, acts
the App interface captures, an App agent's faithful records) and the host's
run recording (host-loop runs; DEP-04-03-016). A **recorder** (RS §3; OF-8)
is who recorded the fact an entry states; one writer may append entries of
several recorders (for a host-loop run: the loop, the native layer, the
control and the act facility, as the loop's events report them, LOOP §2.3).
Where the host facility and the App each record the same act (E2), they
write to their own logs; the reader joins them (§14.2 R-8).

### 13.2 Entry header (the common identity elements of §3)

| §3 element | Entry element | PROPOSED form |
|---|---|---|
| Record identity | `recordId` | Opaque token `rec:…`, minted by the writer, unique across its logs; how it is minted is unselected |
| Record kind | `kind` | One of the kinds in §13.3 |
| Format version | `format`, `formatVersion` | `chirality.rs.record`, "major.minor" (§13.4) |
| Recorder identity | `recorder` | {role, identity}; role ∈ App writer · App interface (capturing surface) · host facility · host control · host loop · host native layer · agent |
| Recording context | `context` | {surface App or host; host identity} |
| Written-at order | `seq`, `writtenAt` | `seq` counts 1, 2, 3… per log and is taken only by a successful write; `writtenAt` is the writer's clock (representation unselected). Order across logs is only as evidenced |
| — | `observedAt` | The time of the observed event where it differs from the write (a late write, FC-1) |
| Corrects (optional) | `corrects`, `correctionReason` | Both or neither |
| Run | `runId` | Opaque `run:…`; absent in an act log |

### 13.3 Entry kinds

| Inventory element | Entry kind(s) |
|---|---|
| R1, R2, R4, R5a; declared checkpoints listed as guidance | `run_opened` |
| R3 | `supplied_guidance` |
| R5 | `model_turn` (per turn: requested, effective, re-route, destination class) |
| R6 | `settings_version` (body: DEL-04-02's settings-in, §8) |
| R7 | `operation_entry` (format 0.1 carries the core of §5: operation, author type and identity with *verified*, channel, route, outcome, settings at route and at application, proposal, related evidence, human-act reference, *reverses*, observer, last observed state, *continued past*; the other §5 elements are carried as evidence references until a later minor version) |
| R8 | `checkpoint_arrival`, `disposition_change` (annotations, among them **"prior act not counted"** with its reason, the only accepted spelling), `run_resumed`, `run_ended` |
| R9, §6 | `human_act` (A4, A5, A6, A7, A10, A11, A12 with subclass, A13, A15), `act_declined`, `act_lapsed` |
| R10 | `examination_findings` |
| R11 | `evidence_limit` |
| R12 | the entry header (§13.2) |
| R13 | `tool_permission_settlement` |
| R14 | `compatibility_report_ref` |
| R15 | `destination_requested`, `destination_grant`, `destination_contacted`, `destination_declined` and `boundary_refusal` (both PROPOSED recording, R12-10), `destination_request_closed` (PROPOSED element, node B5), `outside_process` |
| R16 | `act_request` |

### 13.4 Identities, versions and relations written later

- **Content identities** are {method, value, scope}; *method* is the
  designation that L-2 compares, never an algorithm this format chooses. "Not
  obtainable" is its own form with a reason (L-3).
- **Version rule (OF-7).** Same major and a known or older minor: read. Same
  major and a newer minor: **read limited** — known elements are used,
  unknown elements and kinds are shown as present and unread, and nothing is
  inferred from them. Another major, or another format name: **refused**,
  "unreadable version ‹v›". A minor step adds optional elements or kinds; a
  major step changes a meaning or removes or requires an element. A log may
  carry more than one minor version after an upgrade; each entry states its
  own.
- **Relations known later are their own entries**, since nothing written is
  edited: an A12's control effect by the next `settings_version` naming it
  (its establishment or refusal); supersession derived by the reader from
  established settings versions (L-0); lapse by `act_lapsed`; a disposition
  by `disposition_change`; a correction by an entry naming it in *corrects*.

### 13.5 What the schema refuses and what the reader checks

The schema refuses, among other things: an act without capture evidence; A14
as a human-act record; an A15 without *derived from*; an A12 without its
subclass; an in-work destination grant without scope and request; a
correction without a reason; a decline reported in other words than
"destination not allowed by the person"; a destination request with scope
once that carries no call, and a closed request without its reason or
cause (node B5); any not-counted wording other than
"prior act not counted" with a reason; a person-set settings version without
an A12 reference. The reader checks what the schema subset cannot express
(§14.2 R-5…R-8): sequence gaps; a correction that changes the kind; a
recorder named as the decision actor (HA-2); an unsandboxed outside process
without "process network not observed"; a contact naming an in-work grant
that is not in the record; records of one capture that disagree.

### 13.6 Requests as record elements (RS 5)

**Decided here (PROPOSED representation):** an agent's request for a
person's act is a record element, **R16** (`act_request`), and a host
agent's destination request is an R15 element (`destination_requested`).

- **Why.** ACT AP-5 (R11-1) and EXEC PH-6 require the record to hold "the
  request where it can be identified", and DECISION-K1 K1-1 has the product
  record what it observes. Without an element, that requirement had no
  home (survey §3.5).
- **Identified by** (PROPOSED values; how an App run observes them is EXEC's,
  Wave B node B2): an agent message that names the act kind, subject and
  purpose; a supplier input request that names them (the answer to it is
  never act evidence, EXEC CAP-6); the host loop's "A8 request issued" event
  (LOOP §2.3); an A8 the agent issues after a *not permitted* outcome
  offered one (R2-4).
- **Absent.** Where no request is identified, the arrival's request
  observation is "request not identified". That is an explicit absence, not
  a defect: the agent may have asked in words the App could not identify.
- **Never the act.** A request satisfies nothing, is never shown as the act,
  and creates no A12 (HA-1, HA-5). Under the governance-phase option SP-6F a
  recorded request relation is what orders an act after an arrival (L-13).

## 14. Writer and reader sequences, with failure behaviour (RS 7; PROPOSED)

### 14.1 Writer

**What is written when.**

| Observed event | Entry | Supplier |
|---|---|---|
| Run start | `run_opened`, then `settings_version` (settings-in) | Executor (App: DEL-02-03; host: DEL-05-01); DEL-04-02 |
| Each settings change, agent request for a setting, control report | `settings_version` | DEL-04-02 settings-in |
| Each turn's model, and supplied guidance | `model_turn`, `supplied_guidance` | DEL-01-01 (App); host loop |
| Each operation request, read, examination or loop-side refusal | `operation_entry`; `examination_findings` | DEL-03-01, DEL-03-02, DEL-03-03, DEL-05-01 |
| Tool-permission settlement (App runs) | `tool_permission_settlement` | DEL-01-01 observed facts |
| Checkpoint reached | `checkpoint_arrival` (request observation as then known) | DEL-02-03 (App); DEL-05-01 (host) |
| Request identified | `act_request` (R16); `destination_requested` (R15) | DEL-02-03; DEL-05-01 |
| Act captured | `human_act` (direct capture by the capturing surface; faithful recording by another recorder citing the same capture evidence) | App interface (EXEC CAP-3); host facility or control; App agent (A9) |
| Decline captured | `act_declined` (and, for a destination, `destination_declined`, PROPOSED) | Capturing surface |
| A destination request ends not granted, or unanswered at the run's end or the turn's cancel (LOOP-v0.8 §5.3 DF-6) | `destination_request_closed` (PROPOSED) | DEL-05-01 (host loop or control) |
| Disposition changes; resume point; run end | `disposition_change`; `run_resumed`; `run_ended` | Executor |
| Bound content observed changed | `act_lapsed` | Writer on evaluation (§14.2 R-8) |
| Destination contacted, granted, refused; outside process started | `destination_contacted` (written before sending; not sent if it cannot be written, LOOP F-4), `destination_grant`, `boundary_refusal` (PROPOSED recording; with its stage), `outside_process` (with stateless evidence for an MCP server) | Host native layer and control, through DEL-05-01 |
| A limit observed | `evidence_limit` | The observer |

| Step | What happens | What can fail | Who reports it | Record left | What happens next |
|---|---|---|---|---|---|
| **W-0 Open** | Opens the log for (run, writer); takes the next `seq` after the last entry; if the last line is unterminated, terminates it (never truncates or edits) and appends "partial entry not recovered" | The log cannot be read or written | The writer, to its caller (the App or host run recording) | Nothing new | Entries are held as *pending write* (W-2); the display compares *missing in record* (§8) |
| **W-1 Append** | Completes the header, validates the entry against the schema, then writes one line in one write and syncs it; `seq` advances only on success | (a) The entry is nonconformant. (b) The write fails | (a) and (b): the writer, to its caller, naming the entry | (a) Nothing: a nonconformant entry is never written as a best effort. (b) Nothing yet | (a) The caller corrects its input or records the limit it can. (b) W-2 |
| **W-2 Late write** | At the next append or retry, writes the pending entries in their order, then an `evidence_limit` "record write failed" naming them; each keeps its `observedAt` | The writer stops before the pending entries are written | The caller already holds the failure report | The entries are not in the record | The display shows *missing in record*; a later run cannot back-fill them |
| **W-3 Correct** | Appends a new entry of the same kind naming the corrected one in `corrects`, with a reason | A correction of another kind, or without a reason | Schema (reason) and reader (kind), §13.5 | The correction is nonconformant and changes nothing | The corrected entry stays readable, marked "corrected by ⟨entry⟩" |

### 14.2 Reader

| Step | What happens | Failure and what the reader shows |
|---|---|---|
| **R-1 Collect** | Gathers every log naming the run, and the act logs holding acts the run cites (where the logs live is OI-014's, U-05) | A cited act not found: "unresolvable reference" (§9), never *performed* |
| **R-2 Parse** | One entry per line | A torn last line: "partial entry at end (not read)"; any other unreadable line: "unreadable line ‹n›" |
| **R-3 Version** | §13.4 rule | Newer minor: *read limited*; another major or format: *refused* |
| **R-4 Schema** | Validates each entry | *nonconformant*, with the rule; never used for a disposition or count |
| **R-5 Sequence** | Checks `seq` per log | Duplicates or a gap: "entries missing (sequence gap ‹a›..‹b›)" |
| **R-6 Corrections** | Builds "corrected by" | A correction of another kind: nonconformant |
| **R-7 Reader rules** | HA-2; outside-process limit; grant references | Each breach: nonconformant, with the rule |
| **R-8 Assemble** | Groups act records by capture evidence (one act, however many records; direct capture governs, HA-7); latest disposition per arrival; each A12's control effect from the latest settings version naming it; lapse: c₁ is obtained for the record-out, so lapse is evaluated on read as well as on the writer's events — until c₁ is obtained the state is *not yet evaluated* (never *not lapsed*); resolution status at read for every evidence reference (§9) | Records of one capture that disagree on kind, subject or content: "recorders disagree", and the act is shown only as far as they agree; the reader writes nothing (a lapse found on read is written by the writer, if one is running, as `act_lapsed`) |

### 14.3 Failure cases

| Case | Situation | Behaviour | Record left | Prototype |
|---|---|---|---|---|
| FC-1 | A write fails | Reported to the caller; the entry is held and written later in order, followed by "record write failed" | Complete, with the delay stated | Ran |
| FC-2 | An interrupted write tears the last line | Reader: "partial entry at end"; writer on reopen: terminates it and records "partial entry not recovered" | The torn bytes are kept, unread | Ran |
| FC-3 | Two recorders record one act (E2: host facility and App faithful record) | One act; direct capture governs; a disagreement is "recorders disagree" | Both records | Ran |
| FC-4 | An entry of an unknown version | Newer minor: read limited. Other major or format: refused | Unchanged | Ran |
| FC-5 | A correction | Both readable; derived state uses the correction; kind cannot change | Both | Ran |
| FC-6 | An entry is lost outside the writer | "entries missing (sequence gap)" | As found | Ran |
| FC-7 | A nonconformant entry is offered, or found | The writer refuses to write it; the reader flags one it finds | Nothing written; or the entry flagged | Ran |
| FC-8 | A referenced source becomes unresolvable after the write (e.g. SWBPIPE's receipts are session-only, SQ-09) | Resolution status at read "unresolvable"; what was recorded stays as recorded — a disposition already *performed* is not recomputed to *waiting* — and the record-out states the limit | Unchanged | Designed, not run |
| FC-9 | The App restarts during a run with a submission in flight (ADAPTER PI-6), or the agent resubmits without first observing by identity (ADAPTER PI-2) | The in-flight submission stays *outcome unknown*, observer App (W-0 on relaunch opens the same run log; an interruption is not a run end, EXEC §4.12). How the two conditions are recorded — as R11 limits, as reader-derived observations, or both — is proposed to the integrator (R12-9; `WAVE_B/B4.md`); until R13, R11 does not list them and both ADAPTER texts stand | As R13 rules | Designed, not run |

## 15. Local prototype (R12-3)

`prototype/` holds a prototype, not product code (its README says so):
`minischema.py` (a JSON Schema 2020-12 validator for a declared keyword
subset; any other keyword fails the schema load), `record_store.py` (the W-0…W-3
writer and R-1…R-8 reader) and `run_prototype.py`. Python 3 standard
library only; nothing installed; no network.

- **Command** (2026-09-30, Python 3.13.7, macOS): `python3 -B
  run_prototype.py "$TMPDIR/b4-proto"` in `prototype/`.
- **Observed result:** the three schemas (ACT, AS, RS) loaded under the
  subset check; every valid example validated and every invalid example
  failed for its stated reason (ACT 1 + 3, AS 2 + 3, RS 3 logs + 9 entries);
  each valid RS log written through the writer and read back gave identical
  entries and identical bytes (20, 20 and 3 entries); FC-1…FC-7 held as
  §14.3 states. 37 checks passed, none failed; exit status 0. The console
  output is recorded in `WAVE_B/B4.md`.
- **Node B5 rerun** (2026-09-30, same command with `"$TMPDIR/b5-rsproto2"`):
  the fourth valid log `RS_RECORD.valid.host-destinations.example.jsonl`
  (12 entries) validated and round-tripped with identical entries and
  bytes; INV-RS-10 and INV-RS-11 failed for their stated reasons; every
  earlier check held; "RESULT: all expectations held". The log itself was
  produced by DEL-05-01's `prototype/destination_flow.py --emit`, which
  also validates each entry it writes (LOOP-v0.8 §5.3 DF-10).
- **Not shown:** FC-8 and FC-9; any placement; any identity algorithm;
  concurrency between two writers on one log (S-A gives each writer its own
  log); a candidate writer or reader.

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| U-01 Operation-specific reserved additions `OI-021` | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution | Class may be *no policy basis (pending OI-021)*; fixtures held |
| U-02 Consequence vocabulary | DEL-04-01 with host policy owner | Before class assignment in DEL-03-01 | Scope dimension "consequence" is a slot; OP-C5 on S-4 under ⟨set-2⟩ held |
| U-04 Serialization, field names, identity algorithms, record-identity form, carriage-manifest representation | DEL-04-03 with DEL-03-01 (TBD-003) and DEL-02-01 | Before OUT-001 CONFIG and writer implementation | **v0.8:** serialization, element spellings, unit of storage, record-identity form (opaque token) and version rule PROPOSED in §13, for review; identity algorithms and the carriage-manifest representation stay open. L-2 depends on method designations only |
| U-05 App record location | DEL-04-03 with OI-014 owners | Before writer implementation | "Ordinary files" only |
| U-06 Host persistence/placement `OI-013` | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Host recording follows meaning only |
| U-07 *Closed (DECISION-K1 K1-3, 2026-09-30).* Purpose of a multi-row A4 after partial lapse | The owner (decided) | — | **Settled:** the act keeps its purpose for unchanged rows; a new act on the changed rows alone answers together with it (L-7; EXEC §4.7 JA-1) |
| U-08 *Closed (R12-5, 2026-09-30).* Workflow review/registration as act kind | The integrator (R12-5); the registration control stays DEL-02-02's (later, D1) | — | **A15 register workflow revision** is a human-act record kind (§6.1, HA-10); a checkpoint cannot require it in this increment |
| U-09 Host evidence that application re-checks the basis after acceptance | Host owner (DEP-001) | Before connected integration | OE-7 records both entries |
| U-11 Host capture requirement per act kind; capture-evidence reference. SQ-01 answered 2026-09-28: SWBPIPE exposes none; its Apply receipt names no person or time and is session-only | SWBPIPE owner decision (PB-TBD-002 acceptance-record storage; DEL-16-03 actor identity; ANS §2); host owner generally (DEP-001) | Before host act-recording integration | No host-content arrival reaches *performed* without it |
| U-12 Content returning to c₀ after observed lapse | Host owner (U-C2) with DEL-04-03 | Before lapse display criteria are fixed | L-11 keeps lapse visible. SWBPIPE: same content ⇒ same whole-model hash; DRAFT #885 revision still advances (SQ-03 (e)) |
| U-14 Host-stored findings as a change operation | Host owner | Before V4-EXM-21 fixture binding | R10 may also need R7 |
| U-15 Host receipts, origin marks, subject identities, resulting objects, lapse, per-operation settings version, de-duplication `DEP-001` | SWBPIPE outside implementation session | Before corresponding connected-journey integration/examination and fallback-replacement decision; host joins deferred (DECISION-3) | All host evidence is fixture. SWBPIPE answered 2026-09-28 (SQ-03, SQ-07, SQ-08, SQ-09, SQ-10): whole-model identity only; resulting objects as target ids and diffs; within-session de-duplication and receipts only (DRAFT #885); receiptless session undo |
| U-16 Reader/writer placement `OI-014` | App/shared contract owners | Before structural/production contract allocation | No common service assumed |
| U-19 Host receipt or own evaluation of the governing checkpoint constraint (governance phase) | Host owner (relay SQ-02). SQ-02 answered 2026-09-28: none (route (iv)); planning a route is a SWBPIPE owner decision (ANS §2) | Before connected integration; when the owner resumes UI-SUCCESSOR (DECISION-3) | Phase 1: no constraint recorded as carried. In either phase, "constraint not carriable on this host" is recorded where the host schema has no element (R8-10): in the current phase it says that the expected constraint could not be carried and was recorded only (ADAPTER GC-4, P §3.3); it bears on a hold-support value only in the governance phase (R10-2). Governance phase: only host-held satisfies R2-12; App-assured unavailable (R5-2); model-supplied or absent is an R11 limit |
| U-20 R13 feed beyond DEL-01-01 observed facts | DEL-01-02 (later, D1) | DEL-01-02 definition | R13 fed by DEL-01-01 only |
| U-21 Host-loop per-turn guidance identities | Host owner (relay) | Before connected integration | R3 *unknown* where absent |
| U-25 App-side run holds `UNRESOLVED{D6}`. **Closed for Phase 1** by DECISION-4 D4-1 (R8-2); **re-opens only when the governance phase is taken up**. SWBPIPE answered SQ-02 on 2026-09-28: route (iv), none planned | The owner (DECISION-4; D6 re-opens with the governance phase) | When the governance phase is taken up for a workflow that needs it; before App-side hold fixtures | Phase 1: no hold or hold-support value recorded (§1). Governance phase: R8 hold support (R5-1 values) and R11 action during hold recorded; HS-3 checkpoints *not enforceable* against SWBPIPE, HS-5 *not enforceable*; no unenforced hold recorded as held |
| U-26 *Closed (DECISION-K1 K1-2, 2026-09-30).* SP-6 versus counting a prior act on current content (EXEC U-E4) | The owner (decided) | — | **Settled for the current phase:** L-13 counts an earlier act on current content and cites it; capture after arrival is the governance-phase option (EXEC SP-6F) |
| U-27 Caller identity verification over the external channel (ADAPTER OC-6) | App owner with host owner | Before origin conformance | Author identity *unverified*; R11 limit |
| U-28 *Closed (DECISION-K1 K1-4, 2026-09-30).* App person identity scheme and App act control (EXEC U-E8) | The owner (decided); control construction DEL-01-04 (later, D1) | — | **Identity settled** (§6.1 *Decision actor*): the name set in the App, the operating-system account and the Codex account when reported, marked *identity not verified*; a verified identity is governance phase. **Control:** stays with DEL-01-04; its obligation is proposed for DEL-01-04's contract at the next amendment (DECISION-K1 K1-4) |
| U-29 Per-subject content identity (V4-HI-32) not met by SWBPIPE, which supplies only a whole-model identity (SQ-03; R8-4; EXEC U-E25) | SWBPIPE (PB-TBD-002 / DEL-16-03); owner notice | Before host act-binding integration | L-1 receives the whole-model identity for every covered subject: over-lapse, never under-lapse; resulting objects beyond target ids *not supplied* |
| U-30 DECISION-5 points settled by the owner's DECISION-5 confirmation (2026-09-28: the "MCP V2" reading confirmed; the person-only grant not objected to and stands) (closed for those points) (the person-only grant; the reading of "MCP V2"); the host's native destination report (DEP-001) (R8-13) | The owner; host owner (DEP-001) | Before R15 writer implementation; before host-loop destination cases execute | R15 defined as recorded; without a native report, "destinations not observed" (R11) |

| U-31 ADAPTER's two evidence limits "resubmission without prior observation" and "App-restart interruption" (ADAPTER §5.6 PI-2, PI-6, §11; R10-6) | The integrator (R13), on the proposal in `WAVE_B/B4.md` (R12-9) | Before the second review of this pass (V19) | R11 does not list them; §14.3 FC-9 states the behaviour that holds either way (the submission stays *outcome unknown*, observer App) |

Closed in v0.8, node B4: U-08 (R12-5). Closed in v0.7, node A3 (DECISION-K1): U-07 (K1-3), U-26 (K1-2), U-28 (K1-4). Closed in v0.6: none (U-25 closed for Phase 1 only). Closed in v0.5: none. Closed in v0.4: U-17 (R4-6; EXEC §4.10), U-18 (EXEC §4.11 confirmed), U-22
(EXEC §6.2 confirmed), U-23 (R4-4), U-24 (R4-3). Earlier: U-03, U-10, U-13.

## Verification cases (designed; VC-31…VC-35 ran on the local prototype only, not on a candidate)

| Case | Input (fixture subject) | Expected result | Serves |
|---|---|---|---|
| VC-01 Authority | E1; transcript and derived view claim an A5 on PR-2 item 2 | Only ⟨act:1⟩/⟨act:2⟩; the claim creates no act | VER-001 (AC-001) |
| VC-02 Inventory completeness | E1 run (App) and a host-loop run | R1–R16 each value, explicit absence, or *not applicable* with reason (R13 in a host-loop run; R15 in an App run; R16 absent only as "request not identified" on the arrival) | VER-001 (AC-002) |
| VC-03 Link not copy | E1 with RC-1 | Reference, claimed identity, method, resolution status only | VER-001 (AC-002) |
| VC-04 Faithful recording | E2 | A4, recorder App agent, faithful recording, capture evidence cited | VER-002 (AC-003) |
| VC-05 Fabrication negatives | E3 (a)–(g) | No act records; (d) R11; (e) R13 only; (f) no automatic A8; (g) not act evidence | VER-002 (AC-003) |
| VC-06 Independent act | Engineer A marks own edit checked, no proposal | A4 recorded; no A5 required | VER-002 (AC-003) |
| VC-07 Row lapse and control | E4 | T6 not lapsed; T14 lapsed with act-lapsed event | VER-003 (AC-004) |
| VC-08 Incomparable / unavailable | E2 with m₁ ≠ m₀; host unreachable | *unknown (incomparable)*; *unknown (unavailable)* | VER-003 (AC-004) |
| VC-09 Model-row partial lapse | L-RS-1 | Partially lapsed (S-2); the act keeps its purpose for S-1, and an A4 on S-2 alone answers jointly with it (L-7; DECISION-K1 K1-3) | VER-003 (AC-004) |
| VC-10 Acceptance survives application | E1 | ⟨act:1⟩ not lapsed after T12 | VER-003 (AC-004) |
| VC-11 Undo lapses row-bound act | E6 (T16a, T17) | T16a A4 lapsed; RC-3 reverses RC-2 | VER-003 (AC-004) |
| VC-12 Restore after lapse | E4, then S-2 restored | "matches c₀ again after observed lapse" | VER-003 (AC-004) |
| VC-13 A12 at a checkpoint and supersession (V-GR1) | E7 main timeline and V-GR1 sub-variants | Main: T15 counts toward no arrival; V-GR1: captured after arrival → performed, held call dispatched unchanged as T16; pending/refused → waiting; lost → unknown; later established A12 → superseded, arrival stays performed; refused A12 supersedes nothing | VER-003 (AC-004) |
| VC-14 Retry vs stale | E5 | Retry entry records the host's report or unknown with observer; never stale from own effect | VER-004 (AC-005) |
| VC-15 Stale after acceptance | E8 | A5 not lapsed; *refused — stale* with both bases | VER-004 (AC-005) |
| VC-16 Outcome vocabulary | Not offered; T8 unavailable; V-X1 not exposed; channel not enabled (App-reported and host-reported); V-R1, V-NP1, V-CP1 not permitted; refused — invalid; T7 stale; application error; A10; A11 | Each distinct with evidence and actor/observer; host refusal never "rejected". Received host terms (R8-5): `unsupported_method`/`unsupported_change` → *not exposed on this surface*, never *not permitted*; #885 `withdrawn` → item left, "cleared by the person, no decision record"; `validation_rejected` → *refused — invalid*; none ever A10/A11; `controller_unavailable` → *endpoint unavailable*, channel *disabled* (R8-6); *refused — stale* with the host's scope where it supplies no subject identities (R8-3) | VER-004 (AC-005) |
| VC-17 Checkpoint arrivals and hold support | E10 (i)–(vii) | **Phase 1:** arrival recorded; T2's A4 counts for S-2 as an earlier act, cited with its time (L-13); under the governance-phase option (EXEC SP-6F), T2's A4 is "prior act not counted" and the arrival waits for an A4 on S-2 and S-3 captured after T4a; the T5 dispatch recorded with the optional continued-past annotation, no R11 limit, no stop; performed with ordinal; act-lapsed event labelled "act lapsed at T6" and no re-hold; resolved negatively; waiting + run-ended; (vii) no hold-support value; no *unsupported* for a hold reason anywhere. **Governance phase** (read as governed): classified by held actions (R6-1): App agent turns held → **not enforceable** → *unsupported*; action during hold in R11 with turn initiator and **no stop claimed**; "waiting — re-held, lapsed at T6 after resume"; (vii) host operation only → **not enforceable** → *unsupported* (SQ-02 answered) | VER-002 (AC-003) |
| VC-18 Lapse before resume | E10 with T6 before the run-resumed event | "waiting — lapsed at T6"; no re-hold annotation | VER-003 (AC-004) |
| VC-19 No policy basis | E9 | *not permitted*; A12 refused; **held**, not pass | VER-004 (AC-005) |
| VC-20 Grant change | E7; an A8 alone; ⟨set-1⟩ default | A12 referenced from R6; A8 → "requested by agent"; default → policy-class record, no A12 | VER-002 (AC-003) |
| VC-21 After run end and continuation | E11 | Post-end act marked "after run end"; ended disposition unchanged; new run carries continues ⟨run 12⟩ and inherits nothing | VER-004 (AC-005) |
| VC-22 Destination per turn and unverified caller | E12; an external dispatch with unverified author identity | Per-turn requested/effective kept separate; re-route with its turn; unobserved turn *unknown*; run-level set; no gate, no new run; author identity *unverified*, R11 limit | VER-001 (AC-002) |
| VC-23 Transfer and revision links | A carried unadapted workflow and a host adaptation (EXEC §6.1) | Links recorded separately; revised identity inherits none; "revision not verified" explicit | VER-001 (AC-002) |
| VC-26 Person's undo lapses the act, never action during hold | E6 with the DEL-04-02 F6 arrival | Both phases: act-lapsed event; T17 recorded as the person's operation, never flagged *during hold* or annotated continued past. Phase 1: no re-hold. Governance phase: re-held after resume; an A5 arrival is never re-held by an undo | VER-003 (AC-004) |
| VC-27 Reserved-act operation and App file | E1 OP-C7/OP-C8; an App-captured A4 on C AF-1 (⟨AF-1@f1⟩, then edited to ⟨AF-1@f2⟩) | Human-act records produced by the reserved-act operation and referenced from R7; AF-1 act bound by file content identity lapses on edit | VER-002 (AC-003) |
| VC-28 Hold-support values (governance phase) | E10 (App-side held actions; host-operation-only variant), read as governed; a host-loop run; an invalid declaration | Only the four R5-1 values, recorded only for governed checkpoints in the governance phase; classified by held actions (R6-1); *not established* never a pass or *unsupported*; *not enforceable* → *unsupported*; host-operation-only over SWBPIPE's X → *not enforceable* (R8-2); invalid declaration takes no value; no retired value | VER-005 (AC-006) |
| VC-29 Phase-1 record semantics (R8-1) | E6, E7, E10 (Phase-1 parts); an agent-written A4 claim without capture evidence; a checkpoint declared `governed` | No hold, re-hold or hold-support value recorded; no *unsupported* for a hold reason; acts recorded only from capture evidence of the person's performance (the agent's claim creates none); arrivals and acts recorded as observation, with dispositions as record labels; "continued past ‹checkpoint› before ‹act›" optional and never an R11 limit; lapse recorded; the `governed` flag recorded and changing nothing in Phase 1; an invalid declaration recorded as a declaration finding only | VER-002 (AC-003) |
| VC-30 Network destinations (R8-13) | E13; a variant with no native destination report; an agent-written allow-list entry | Every contact carries destination, category and allowing grant or entry; grants carry scope, time, source and an A12 reference; the decline carries the act-declined reference and "destination not allowed by the person"; the unsandboxed process carries "process network not observed"; without a native report, "destinations not observed"; the agent-written entry creates no grant and no act. From v0.8 (node B5): the host-destinations log (E-14) and LOOP MS-24…MS-27: a request carries its call; a closed request its state with reason or cause; a refusal its stage; a model-service contact its class; an MCP server its stateless evidence and the limit "stateless revision declared, not verified". Ran on LOOP's prototype (not a candidate) | VER-001 (AC-002) |
| VC-31 Format round trip (RS 8) | The three valid example logs of §13, through the prototype writer and reader (§15) | Each validates; written and read back, entries and bytes are identical. **Ran 2026-09-30 on the prototype: held** (not a candidate result) | VER-001 (AC-002) |
| VC-32 Write failure and torn entry (RS 7) | FC-1, FC-2 | Failure reported to the caller; the entry written late in order with "record write failed"; no sequence gap; a torn line kept unread, terminated on reopen and recorded as "partial entry not recovered". **Ran on the prototype: held** | VER-001 (AC-002) |
| VC-33 Two recorders (RS 7; E2) | FC-3 | One act counted once; direct capture governs; a disagreement gives "recorders disagree". **Ran on the prototype: held** | VER-002 (AC-003) |
| VC-34 Unknown version (OF-7) | FC-4 | Newer minor read limited; other major or format refused; nothing inferred. **Ran on the prototype: held** | VER-001 (AC-002) |
| VC-35 Correction (OF-5) | FC-5; INV-RS-7 | Both readable; "corrected by"; a correction without a reason or of another kind is nonconformant. **Ran on the prototype: held** | VER-003 (AC-004) |
| VC-36 Request element (RS 5) | The two example runs (a request recorded, then answered); an arrival with no identified request; an act record whose only evidence is the request | R16 recorded with its reference; "request not identified" is an absence, not a defect; a request never satisfies an arrival | VER-002 (AC-003) |
| VC-37 A15 (R12-5) | The act-log example; INV-RS-3; a changed definition registered under an earlier A15 | A15 bound to the revision identity with *derived from*; without *derived from* nonconformant; the earlier A15 does not carry to the new revision; not lapse-evaluated | VER-002 (AC-003) |
| VC-38 Destination exchange (RS 6, AS 4) | E13; the host-run example; its settings version | Settings-in carries switches, named entries, always-off items, in-work grants and requests with the LOOP-v0.8 §5.3 DF-6 states; record-out carries the R15 entries; declines and refusals recorded as PROPOSED; contacts read by reference, not compared; "destinations not observed" never shown as none contacted | VER-001 (AC-002) |
| VC-24 Coverage inventory | VC-01…VC-23 and VC-26…VC-38 against AC-001…AC-005 | Each AC has ≥1 positive and ≥1 negative case; held/AWAITING INPUT never counted as pass; distinct from DEL-09-11 | VER-005 (AC-006) |
| VC-25 Owner trace | §10, §11, UNRESOLVED | Each REQ-005 consumer and REQ-006 excluded act traced; D2/D3/D5/D6 cited only for what they say; no delivery/adoption asserted | VER-006 (AC-007) |
