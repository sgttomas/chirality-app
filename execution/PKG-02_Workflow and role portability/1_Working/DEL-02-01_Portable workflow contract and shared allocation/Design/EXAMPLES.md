# Portable workflow declaration — readable examples
- Contribution: DEL-02-01/WD-EX-v0.9 (companion to DEL-02-01/WD-v0.9, `WORKFLOW_DECLARATION.md`, and to its schema `workflow-declaration.schema.json`; supersedes WD-EX-v0.8, last changed at `153a7c533b`, file sha256 `275ea54d32cd8f487ec9a0f017aaa33b01ee43c79d7a675b53a7652c3519e2fd`; WD-EX-v0.7, last changed at `c896a99d90`, file sha256 `b2b554d815503deab076b737a96b353ca279fa50b1ed578b94bf6a1c059727d9`; WD-EX-v0.6, last changed at `f5ceef164`, file sha256 `8d60ed7850e6935b8410217c8867c59554c7de9aec28c60514e88ff5f0cff36e`; WD-EX-v0.5, last changed at `c6f81a4f2` and unchanged at `bcc25624d`, file sha256 `67e2d8ed187ad7f2134592f4f9ec744d9af33c49882d772648d42c340f531d42`; WD-EX-v0.4 committed at `8fb51f07f`, file sha256 `60ce307a25fe1f9aaad0826985e02aaa6ebd68d86a6d972b1d5a1e39b3128ca4`; WD-EX-v0.3 sha256 `0f1058d7f0990e766b3effc3d3de24fc16383197874cced1f5b4212419cf018d`; WD-EX-v0.2 sha256 `50b7600de8503f51f440e5947ebd4ea7a559781e2497d5d880a8d683f7a9c43e`; WD-EX-v0.1 sha256 `69ac3dbfc5f97e2982418b918996df9b4a6abc674588c627e3e96fb4c133d55a`)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Phase (R9-1; PRD V4-WF-05 and HOST_INTEGRATION V4-HI-42 as amended by SCA-V4-001; WD §4.3.0): when a run reaches a declared checkpoint, the required human act is requested, and it is recorded as done only when the person performs it, whatever the autonomy setting. Holding the run at the checkpoint until the act is performed is phased to the governance layer: in the current phase (Phase 1) a checkpoint is plan guidance that the person and the agents manage, and neither the App nor a host's embedded loop enforces a hold, blocks a run, or reports a workflow unsupported because a hold cannot be enforced. The reserved acts (V4-HI-30) still bind. So the examples' checkpoints are **plan guidance** in the current phase. Where an example shows a hold, it is the **governance-phase** reading (retained), with each checkpoint read as if declared `governed`; no fixture declares the flag (WD U-33 closed).
- Serves: OUT-001, OUT-002 (explanatory examples, and at v0.8 the normative rendering of E1 and E1d in the PROPOSED carriage, WD §3.5); OUT-004 (fixture subjects; at v0.8 also conformance instances read by the design prototype `prototype/wdproto.py`, which is not product code); REQ-001, REQ-002, REQ-003, REQ-004; VER-001…VER-004, VER-007
- Basis: the accepted basis as amended by SCA-V4-001 (`_ScopeChange/SCA-V4-001_2026-09-28_2155/`) and SCA-V4-002 (`_ScopeChange/SCA-V4-002_2026-09-29_1901/`), at its current bytes (R9-5): PRD.md sha256 bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd; ARCHITECTURE.md sha256 317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c; HOST_INTEGRATION.md sha256 d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f; EXAMINATION.md sha256 471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0 (the v0.1–v0.6 passes read these at repo 6e18505e3, before the amendments). ScopeOfWork.md sha256 ef360edf28f5f463ae961495e04e566ab9ec9d56c0a4fd4f35e67b87adb82f17 (revised by SCA-V4-001 and SCA-V4-002; the v0.1–v0.6 passes read sha256 080d7f5a8e55d93c06f51e5332b53954deb03e0877b1ee49be3011e3de14a294). Requirements relied on: PRD V4-WF-01…06, V4-HOST-05/06, V4-AUT-01/03/05, V4-EXE-01/03; HOST_INTEGRATION V4-HI-11, V4-HI-20…25, V4-HI-30…33, V4-HI-40…42, V4-HI-70/71; DECISION_BRIEF #d3, #d5; owner decisions `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (D2, D3) and `-DECISION-2` (D5, D6; OWNER_DECISIONS.md at `f05c7e4cd` sha256 `a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c`); Root `workflows/WORKFLOW_TEMPLATE.md`, `workflows/create-workflow/WORKFLOW.md`, `workflows/project-dag/execution.json`
- **v0.9 inputs (design pass 3, run `APP-V4-DESIGN-PASS-3-20261001`, node F-D).** As WD-v0.9's v0.9 inputs line (the same files at the same sha256: `BRIEFS.md` `316ea293…`, `F/F0_JOINS.md` `e93608be…` §1.7 FX-01, FX-02 and §1.14, `R17_RESOLUTIONS.md` `b0af81bc…` R17-11, `R19_RESOLUTIONS.md` `16930ecd…`, `OWNER_DECISIONS.md` `ea96c557…` K-6…K-8, L-4). WR-v0.2 (§2.2 ID-1, §4.1 SP-3, SP-6, DS-1…DS-3, §4.4 SL-2) and AAC-v0.2 (§4.1, §4.2) are cited at the v0.2 labels being written in parallel, by section as numbered at v0.1. No fixture block, declared part or L-WDEX label changes, so the prototype's byte-for-byte comparisons are unaffected.
- **v0.8 inputs (Wave B, node B1 of run `APP-V4-DESIGN-PASS-2-20260930`).** Each sha256 recomputed with `shasum -a 256` in the working tree at this pass; paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/`: `R12_RESOLUTIONS.md` sha256 95f3011b436b6faa3de098059e77eac836c165e0bb98a5ed94e28918a3a749a1 (R12-1…R12-3, R12-5, R12-10); `BRIEFS.md` sha256 ccb4d9f036fb7ff531fffa0d309533b15cf1ebb39b0320651ed4bd5d88efc550 ("Common rules", "Wave B", row B1); `OWNER_DECISIONS.md` sha256 1dfd5bf4619b329719136b1646030e3f871fd7ffc52dbfd12265414e515aaf15 (DECISION-K1); `SURVEY/S1-C.md` sha256 5b60dd41a8c269902a9b360bf4cdc7c8106c464564bcc2fc1623948661c7eaa0 (§B.8 items 2–4). Companion WD-v0.8 (§3.5–§3.7, §4.2.5, §4.3.1, §4.4, §6.1). Siblings by label and section, read in the working tree while other Wave B nodes edit them: ACT-POLICY-v0.7 §2.1 (A6, A7), §2.6, §13 (L-ACT-6); C-v0.7 §10.1–§10.4, §10.7; EXEC-v0.5 §4.5, §4.7, §5. Root `workflows/create-workflow/WORKFLOW.md` and `workflows/project-dag/` (`WORKFLOW.md`, `execution.json`) read at HEAD `86cafc0e1c`, unchanged since `6e18505e3` (`git diff --stat` empty). The prototype's command, date and output are recorded in `WAVE_B/B1.md`.
- **Pins as of node A4 of this run's records (run `APP-V4-DESIGN-PASS-2-20260930`; in place, no version bump; R11-3; relabelled at RQ, V19-B n-1: later pins of the same records are in the Wave B input lines and in GUIDE's basis).** Each sha256 recomputed with `shasum -a 256` in the working tree at this pass; paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/`: `R9_RESOLUTIONS.md` sha256 a64e241519b7d158165a7ede0ffdd22eec0af15b6812b5300755f5f38abd59b8 (R9-1…R9-11; R9-2's second bullet as corrected by R10-1); `R10_RESOLUTIONS.md` sha256 ad3b6caa4a12660db77abc51b5c02ba70519ee46d55b40d21ee76eb3ca561796 (R10-1…R10-11); `R11_RESOLUTIONS.md` sha256 e7343b6663b6aeeb2dc506d3391f5b310088e7688d1b21e65d2ba1d8616b3615 (R11-1…R11-9, the repairs from review V17); `OWNER_DECISIONS.md` sha256 7458e9e81971676337a34280b4e8b29a7d04fce5fc202da5b9f5cf7ccd8f9ae5 (DECISION-K1). At node A4 these superseded for currency the earlier pins of the same records in this header and in the change-table rows, which record the bytes read at node A1 or A3.
- Consumed inputs: **v0.7 (Wave A alignment; run `APP-V4-DESIGN-PASS-2-20260930`, node A1-C):** R9_RESOLUTIONS.md sha256 `c3efe2ffa232dd9293202d4fc891eba4325afeb2e224fecdf8c1b4c5122a9d2c` (R9-1…R9-11; binding); BRIEFS.md sha256 `698d91d8217cee528812529fa353faac899b4bc1a5be5686552ad88dad6c469a` ("Common rules", "A1 — alignment wave"); SURVEY/S1-C.md sha256 `5b60dd41a8c269902a9b360bf4cdc7c8106c464564bcc2fc1623948661c7eaa0` (advice, checked against current sources); `reviews/V6.md` of `APP-V4-FIRST-INCREMENT-20260928` (m-5), applied under R9-8. Rulings in force: R1–R7 by file (hashes below; R7_RESOLUTIONS.md sha256 `1f6ab3b2355e164f803657ceae08841af92d21a821feede3800a6df861b2a1ea`) and R8_RESOLUTIONS.md at its current sha256 `44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b` (R8-1…R8-13; R8-13 changes nothing here). Owner decisions: DECISION-3 and DECISION-4 in the intake OWNER_DECISIONS.md at its current sha256 `5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2` (it also holds DECISION-5); `APP-V4-BASIS-ALIGN-20260928` DECISION-7 (OWNER_ITEMS O-25), OWNER_DECISIONS.md sha256 `ca8c4e50df1d7dddb41b875a4afe46eea4f1a1bf2491d255b7890d0d71cd254b`. SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` at its current sha256 `afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74` (three lines revised by SWBPIPE at `a999f4ba1` after the R8 pass read `6f01add3…61c7`; none changes a statement this file makes; data about SWBPIPE's current state, not commitments). Sibling Design files are cited by version label and section only (R9-5; byte pins are in GUIDE's input table alone), at their Wave A labels (R9-11): WD-v0.7 (this file's companion); EXEC-v0.5; C-v0.7; P-v0.7; ADAPTER-v0.5; GUIDE-v0.4; ACT-POLICY-v0.7; AS-v0.7; RS-v0.7; LOOP-v0.7; PANEL-v0.7; HOSTING-BOUNDARY-v0.7; PIN-SPIKE-v0.1; CA-v0.5; XT-v0.5; RELAY-v0.3. C §10 was read directly at this pass in the working tree (§10.1–§10.4: every identifier in the fixture table below is present there). The blocks that follow are kept as the records of their passes. **R8-12 closing pass (node A6; in place, no version bump):** R8_RESOLUTIONS.md sha256 d4c3423310a857af86692d17ddfdd22fa877ee20b07c46e1ee481d1cd750e7af (R8-12, items 1 and 7 applied here). Current sibling versions after R8, as committed at `7a1508452` with A6's in-place R8-12 edits (their byte pins are in GUIDE-v0.3's input table): DEL-02-03/EXEC-v0.4; DEL-03-01/C-v0.6; DEL-03-02/P-v0.6; DEL-03-03/ADAPTER-v0.4; DEL-03-04/GUIDE-v0.3; DEL-04-01/ACT-POLICY-v0.6; DEL-04-02/AS-v0.6; DEL-04-03/RS-v0.6; DEL-05-01/LOOP-v0.6; DEL-05-02/PANEL-v0.6; DEL-01-01/HOSTING-BOUNDARY-v0.6; DEL-01-01/PIN-SPIKE-v0.1; DEL-09-06/CA-v0.4; DEL-09-09/XT-v0.4; DEL-09-06/RELAY-v0.3. SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` and `FACTS_SQ01_SQ32.md` are unchanged (data about SWBPIPE's current state, not commitments; DECISION-3). WD-v0.6 is this file's companion. **v0.6 (R8 pass, node A1, at `bcc25624d`):** R8_RESOLUTIONS.md sha256 `9877da0759409776ff3ac5d77cd20efb2edd9f513bdba8ce39564f650e561234` (R8-1…R8-5, R8-7); INTAKE_MAP.md (I2) sha256 `3cc182955c0f3dd70efa0f1c051870229c2ccc08f36c5cf1445f2eef0dd1ea33` (rows 01.6, 02.5, 03.8, 10.5; Part 2 P2.1, P2.4–P2.6, P2.13, P2.17 and its §2.2 WD-EX rows; Part 3 item 2); owner decisions DECISION-3 and DECISION-4 (OWNER_DECISIONS.md at `bcc25624d`, sha256 `a5ccab0d39bd1cab37c5556abc9bdedd5341ce76be4712706c8c9d72d623e776`); SWBPIPE's delivered answers `RELAY_ANSWERS_SWBPIPE.md` sha256 `6f01add3977761e42ac6b310faf72ba4fd5455e478605deb83fefb2e4d3a61c7` (data about SWBPIPE's current state, not commitments); EXEC-v0.4 (working tree, sha256 `d32be37797a3c367d342a2d13bbb8dd4279bc52934531d83b8c6ec8c6e7b76d4`; §2.1, §2.2, §3.6, §7) and WD-v0.6 (this pass; §4.3.0, §4.3.1 `governed`, §4.3.8). Earlier: R5_RESOLUTIONS.md at `8fb51f07f` sha256 `254d0b93b9959419a70c6737b07087e1db59b529adc3105a1db31f82b78dd6f1` (R5-1, R5-2, R5-3, R5-7, R5-9); reviews V3-A sha256 `f25f5af1177b7fe2a698bd4ef1e1caafa4c2ef25cfc73111f031e17c7cc21d87` (MAJOR-1, MAJOR-3/4/5 as they touch WD-EX; m-1, m-2, m-3, m-6) and V3-B sha256 `5662fbd09025f5ad9459861370159d606fcced76b394980199e861555a1954a3` (change-table note). **Shared fixture as read at the R5 pass (carried in C-v0.6 §10):** DEL-03-01 C-v0.4 §10 at `8fb51f07f` (`CATALOG_AND_READ_BASIS.md` sha256 `e929d39d3ff9515702f9bfe51dfada537e1cbd165146ec0de4ccf629c659a08c`): FXA-1…FXA-5, LIB-A1, LIB-A2, AF-1, editions e1/e2, V-CP1 etc.; V-GR1 in C-v0.5 at `d3cebd1cc` (sha256 `a6306bd477decad22d4405fb86ca6212fb189e4865c68dbbcba90e1335be7a29`; run 13, GR-1…GR-3, GR-P, GR-R, GR-S). **R6 (in place, no version bump):** R6_RESOLUTIONS.md sha256 `8703e85aa7324e233fab285321e277d720923d3e36e342c865917b55083cb841` (R6-1, R6-2, R6-3, R6-4); V4-A sha256 `121deafc40c4baf0dec71f96eb449083b0d93456c2bd448f89a279951ca2eab1` (MAJOR-2; m-1, m-3); EXEC-v0.3 §3.6 (working tree, sha256 `b147d9862fe9e0228139c72ba13c50392dcf66930109c4357587bf97bbdebf42`). **Siblings at `8fb51f07f` (R5 pass; now EXEC-v0.4 and CA-v0.4):** EXEC-v0.2 sha256 `7f7848c0de2fdb4dc21f5adafa97f92e179bb66c9f6b04f3434d8f2342317af0`; CA-v0.2 sha256 `31ea3bff05865f425127009f90c070f26b97972e203b5a235791d00332d8dee1`. Earlier: R4_RESOLUTIONS.md at `f05c7e4cd` sha256 `50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24` (R4-2, R4-3, R4-4, R4-5, R4-6, R4-7, R4-9, R4-12, R4-14, R4-18, R4-19, R4-20, R4-21); reviews/V2.md sha256 `75ba1dff8a0c4fa2eb294471127147cbd19a0925daf9169b32ddc88727dde6ef` (MAJOR-1; m-3, m-8, m-9, m-12, m-13); R3_RESOLUTIONS.md sha256 `202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf` (R3-1, R3-3, R3-4); R2_RESOLUTIONS.md sha256 `77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088`; R1_RESOLUTIONS.md sha256 `2f9c7e72…77ec4`; IR1-A/B/C (items addressed to DEL-02-01). **Shared fixture:** DEL-03-01 C-v0.3 §10 FX-PIPE-01, read at `f05c7e4cd` (`CATALOG_AND_READ_BASIS.md` sha256 `ba45e7393ee0b16780f36605ddeecb95ba1f181488e36a46b4b495b69fd67c26`). **Siblings read at `f05c7e4cd`:** DEL-02-03 EXEC-v0.1 (`EXECUTION_COMPATIBILITY.md` sha256 `e0ede76ebf08003511755afc666be2466a867fd3256837ee94300cd0dfe518e8`); DEL-09-06 CA-v0.1 (`CONNECTED_ACTIVITY_CONTRACT.md` sha256 `685349b25981ca8333929207890514120d63753cdedd67ae0bad986fc5d45e62`, §3.2 L-CA-1). P §4.3/§9 terms as in P-v0.2/v0.3 (unchanged for these uses).
- Receivers: as WD-v0.9, its Receivers line and §8 (R9-6): DEL-02-03, DEL-05-01, DEL-05-02, DEL-03-02, DEL-03-03, DEL-03-04, DEL-09-06, DEL-02-01 OUT-004 self-check; DEL-02-02 and DEL-02-04, outside the first increment (D1) and designed in design pass 3 (WR-v0.2, ROLE-v0.2); outside this increment DEL-08-02, DEL-09-02 and DEL-10-03

## Changes from v0.8

First-increment edits of design pass 3 (run `APP-V4-DESIGN-PASS-3-20261001`,
node F-D). Rows carry the F0 row ID (`F/F0_JOINS.md` §1.7, §1.14). No
example value, disposition, fixture block or L-WDEX label changes; the
fixtures' declared parts keep the contract version value `WD-v0.8` (WD-v0.9
§3.3). The file stays DRAFT: unsupplied, unimplemented and not accepted.

| Row | Change in v0.9 | Where |
|---|---|---|
| (version) | WD-EX-v0.8 → WD-EX-v0.9, companion to WD-v0.9; v0.9 inputs; Receivers line: DEL-02-02 and DEL-02-04 designed in design pass 3; the rendering note says the carriage and the value `WD-v0.8` are unchanged | Header; rendering note |
| **FX-01** (D5 J-10; K-6; R17-11) | E3: the refinement registers in LIB-A1 as the next revision of `supports-adjust`, ⟨rev-A3⟩, revision 2 of the slot (WR-v0.2 SP-3, DS-2), derived-from the host tuple ⟨rev-3⟩ (its draft base, SP-6); its prior revision ⟨rev-A2⟩ is named by the A15 record, not by derived-from (R17-11). The last column's origin, source root and holding library distinguish the opened host copy (LIB-A2) from ⟨rev-A3⟩ (LIB-A1), as CA §3.2 and §4 already do | E3 |
| **FX-02** (D5 J-11) | E4 step 3: App side pinned on ⟨rev-3⟩, ⟨rev-4⟩ shown as newer, following it a new selection event (WR SL-2, PROPOSED); host side open (U-10). UNRESOLVED U-10 row follows | E4; UNRESOLVED |
| **§1.14 sweep** (L10, L948, L1259 of v0.8) | Receivers line (L10); E1e's "which DEL-01-04 builds later" (L948) → designed in AAC-v0.2, not built; U-25's "construction DEL-01-04 (later)" (L1259) → designed, not built. E1's introduction names ⟨rev-A2⟩ as revision 1 of its slot, registered by A15 at the act control (K-6, K-8). No meaning changes | Header; E1; E1e; UNRESOLVED |
| (L-WDEX-33a) | The row notes that its reading is unchanged at WD-v0.9: `WD-v0.9` is the document label, not a declared-part value | E9 |
| (verification) | "Inputs for WD-v0.9 §13"; inventory WD-EX-v0.9; UNRESOLVED points to WD-v0.9 §12 | Verification cases; UNRESOLVED |

## Changes from v0.7

Wave B design development (run `APP-V4-DESIGN-PASS-2-20260930`, node B1;
R12-1). Rows carry the survey item (S1-C §B.8, "WD-EX n"; S1-C §A.8, "WD n")
or the ruling. No L-WDEX label is reused or renumbered; new labels start at
L-WDEX-18. No E2 or E8 disposition changes. The file stays DRAFT: unsupplied,
unimplemented and not accepted.

| Item | Change | Where |
|---|---|---|
| R12-1 (version) | WD-EX-v0.7 → WD-EX-v0.8, companion to WD-v0.8 | Header |
| WD-EX 2; WD 5 (U-01, U-02) | E1 is rendered in the PROPOSED carriage (WD §3.5): a complete `WORKFLOW.md` whose declared part is the `workflow-declaration` block. That rendering is the fixture; the tables stay as explanation. E1's prose now names the designating line of each message output, and its headings drop the "[checkpoint …]" suffixes so that stage and position names equal the headings (the section text names each checkpoint). E1d is rendered the same way; E1b's and E1e's declared parts are given as JSON. The prototype compares each with its fixture: byte for byte (E1, E1d) or as parsed JSON (E1b, E1e) | Rendering note; E1; E1b; E1d; E1e |
| R12-10 (R10-8); WD 7 | Message-form outputs carry a **designating line** (WD §4.4 OP-1…OP-6): E1 `examination-report`, `host-check-result` and `summary`; E1b `findings`; E1e `load-findings`. `CP-check`'s reached-when kind (b) on `examination-report` is observable as declared. E1's `checked-rows` has the form *human-act standing* (WD §3.6) | E1, E1b, E1e |
| WD 5 | Required tool references carry local names (WD §4.2.2), shown in E1's tools table | E1 |
| WD-EX 3 (S1-C §B.2) | New **E1e** `supports-approve` with an **A6** checkpoint (`CP-approve`, on an App file) and an **A7** checkpoint (`CP-rely`, by the accountable professional); new run readings **E2b** (R-18, R-19). Local cases L-WDEX-39…L-WDEX-41 stand in for the capture that C §10 does not provide | E1e; E2b |
| WD-EX 4 (S1-C §B.2, §B.5) | E1e declares a **harness-capability requirement** (`write-package`, capability `file-change`, WD §4.2.5), an input of kind **file supplied to the run** (`design-criteria`, AF-1) and one of kind **output of another identified workflow run** (`review-findings`, E1b's `findings`). New **E9**: the `governed` yes / absent / unrecognized variants (VC-45) and the other declaration variants, with the readings the prototype produced | E1e; E9 |
| WD 6 (U-08) | E8 L-WDEX-15 names its capability `shell-command` (WD §4.2.5, PROPOSED). Its values do not change: the reference stays *not established* until EXEC EV-3 has a presence rule | E8 |
| WD 9, WD 10; R12-10 (SP-6F) | E9 shows the reading order, duplicate names (FB-20), dangling references (FB-13, FB-21), `fresh act required` (L-WDEX-27a/b) and `on subject absent` (L-WDEX-28) | E9 |
| (E5, E6) | The readings of E5 and E6 in the carriage are stated, each read by the prototype from the real Root bytes, with E5's "declared empty" variant (VC-04) and E6 rendered as a v4 package | E5; E6 |
| R12-1 (verification) | Verification table: rows for the rendered examples, E1e, E9 and E5/E6 in the carriage, each saying whether the prototype ran its declaration part | Verification cases |
| (UNRESOLVED) | U-01 and U-02 restated as PROPOSED at WD-v0.8, with consumer confirmation pending; U-08 PROPOSED at the pin; U-32 decided (PROPOSED) | UNRESOLVED |
| **R14-6** (V18-2 M-2; repair node RP-3, in place, no version bump) | The outcome token in E1's and E1d's declared parts is P's `applied` (was `applied_receipt`), with WD's schema, valid example, E1d fixture and prototype in the same repair; the rendered E1 and E1d still equal the prototype's rendering byte for byte | E1, E1d |
| V18-2 m-7 (R12-10) | "Prior act not counted" in the one wording of RS L-13 with its reason (governance-phase option: *captured before arrival*) in R-9b, R-12b, R-16 and R-19 (v); the R4-5 history row keeps its wording | E2, E2b |
| V18-2 m-2 | New variant L-WDEX-42: E1e's file output without `path` | E9 |
| V18-2 n-2 | E1e cites EXEC CH-32 (`report-signoff`), the other fixture for the same VER-003 separation | E1e |
| RQ (repairs from V19; in place, no version bump) | V19-B n-1: the node-A4 pins bullet relabelled "as of node A4", so it does not claim currency | Header |
| G (items the closeout returned to the graph; `R16_RESOLUTIONS.md` R16-3; in place, no version bump) | Follows EXEC-v0.6's EV-3 made active per group at node G (closeout C1-A G-2): E1e's harness-capability row, L-WDEX-15's E8 row and the U-08 row now say EXEC's presence rule exists (EV-3a) and that, with no signal read, the reference stays *not established*; no example value changes | E1e; E8 L-WDEX-15; UNRESOLVED U-08 |

## Changes from v0.6

Wave A alignment (run `APP-V4-DESIGN-PASS-2-20260930`, node A1-C). Rows are
keyed by R9 ID and by the survey item they answer (S1-C §B.8, "WD-EX n"). At
node A1-C: no example, value, disposition or L-WDEX label changes. Rows marked
node A2 apply R10 to the passages they name. At node A3 (DECISION-K1): SP-6
became the SETTLED earlier-act rule for the current phase (EXEC SP-6; WD I-8;
K1-2); the R4-5 rule is kept as EXEC SP-6F, a governance-phase option
(PROPOSED); R-4 (ii) uses the joint answer (EXEC §4.7 JA-1; K1-3); and R-9b,
R-12b and R-16 (i) were recomputed. The file stays DRAFT: unsupplied,
unimplemented and not accepted.

| R9 ID (survey item) | Change |
|---|---|
| R9-5, R9-11 (WD-EX 1) | Version v0.6 → v0.7, companion to WD-v0.7. Header re-pinned: the four basis docs at their current sha256, naming SCA-V4-001 and SCA-V4-002; the current ScopeOfWork sha256; R8 and the intake OWNER_DECISIONS at their current sha256; the SWBPIPE answers at `afb6e063…`; siblings by version label and section only. The earlier Consumed-inputs blocks are kept as records of their passes |
| R9-1, R9-3 (WD-EX 1) | Phase line re-worded with the R9-1 summary of PRD V4-WF-05 and HI V4-HI-42 as amended. The two-halves reading and the basis-update marker are dropped (WD U-33 closed) |
| R9-2 (WD-EX 1) | R-5a and R-5b, current-phase readings: `CP-accept`'s act is still requested; no A5 is forced, and none is recorded by reason of a direct application (R8-11 item 2 and R8-12 item 2 as restated by R9-2; V4-HI-42 as amended). No disposition changes |
| R9-5 (WD-EX 1) | Fixture reference table re-pointed to C §10 as read directly at this pass (C-v0.7 by label); the V-GR1 source and the framing paragraph no longer name superseded C versions |
| R9-8 (WD-EX 5; V6 m-5) | E8 note: the A5-precedence clause is stated, "(an A5 checkpoint takes the derivation, EXEC §3.6)". No value changes |
| (WD-EX 5; EXEC F-25) | Dispositioned: L-WDEX-13b (OP-C12 absent) stays this file's single optional-absent example. EXEC's L-EXEC-26 (OP-C5 absent) is not adopted as a shared case, and no L-WDEX label is added |
| R9-6 | Receivers line follows WD-v0.7's rebuilt line |
| R9-11 (labels) | E1's fixture declaration contract version label, the UNRESOLVED lead and the verification rows moved to WD-v0.7 / WD-EX-v0.7 |
| **R10-1** (node A2, in place; R9-2's second bullet corrected) | R-5a Phase 1: `CP-accept` is reached when the proposal queues, and its act is then requested ("still requested" dropped). R-5b Phase 1: if the host applies directly nothing is queued, so `CP-accept` is not reached; nothing is requested by reason of an arrival that did not occur, no A5 is forced and none is recorded. No disposition column changes |
| **K1-2** (node A3, in place; owner DECISION-K1 of 2026-09-30, `APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md` sha256 35d6546346907137581be7df3bed4a8ccdb4b8bc55a261ca716040d0ad9f91bc) | An earlier act counts in the current phase when it is of the required kind and its content is still current, cited with its time (WD I-8 as rewritten; EXEC SP-6); capture after arrival stays only as the governance-phase option (EXEC SP-6F). Recomputed: R-9b (was *waiting*, now *performed*), R-12b's continuation reading, R-16 (i) (was *waiting*, now *performed*; the held call no longer waits). E2 lead sentence, E1 `CP-check` expected evidence, U-31 closed, verification row for E1d/R-16 |
| **K1-3** (node A3, in place) | R-4 (ii): an A4 on S-3 alone answers `CP-check` together with the earlier A4 for S-5 and R-100 (WD I-4 joint answer; EXEC §4.7 JA-1). U-05c closed |
| **K1-4** (node A3, in place) | U-25 closed: person identity recorded as observed and marked *identity not verified* (EXEC CAP-8); the act control stays DEL-01-04's, its obligation proposed for DEL-01-04's contract at the next amendment |
| **R11-4** (node A4, in place; V17-B M-2) | The preamble of this table is scoped to node A1-C; it now says that rows marked node A2 apply R10, and states what node A3 changed (SP-6 SETTLED for the current phase; the R4-5 rule kept as SP-6F, a governance-phase option; R-4 (ii) uses the joint answer; R-9b, R-12b and R-16 (i) recomputed). Preamble of this table |
| **R11-3** (node A4, in place; V17-B M-1) | Header: a new line pins this run's records at their final bytes: R9 `a64e2415…`, R10 `ad3b6caa…`, R11 `e7343b66…`, OWNER_DECISIONS `7458e9e8…`. The node A1 input line and the K1 rows keep the bytes read then. Header |

## Changes from v0.5

Keyed by R8 ID; sources are I2 rows of INTAKE_MAP.md. R8 overrides I2 where
they differ. L-WDEX numbering is unchanged.

| R8 ID (source) | Change |
|---|---|
| **R8-1** (DECISION-4 D4-1) | New framing: in Phase 1 the fixture checkpoints are plan guidance (WD §4.3.0). Hold readings in E2 (R-4 (ii), R-5a/R-5b, R-16 (i)/(ii)) and E8 are marked **governance phase (retained)**, reading each checkpoint as if declared `governed`; no fixture declares the flag. *Action during hold* becomes, in Phase 1, the optional "continued past ‹checkpoint› before ‹act›". V4-WF-05's first half is **phased to the governance layer, not withdrawn** (flagged, WD U-33) |
| **R8-1**, **R8-2** (02.5; P2.1, P2.4, P2.5, P2.6, P2.13) | **E8** is restated in two parts. **Phase 1:** checkpoints are guidance, and results depend on the required tools and channel state (E1, E1c, E1d and L-WDEX-17 via X pass; L-WDEX-15 is *not established* on its harness-capability reference). **Governance phase:** SQ-02 answered 2026-09-28 (route (iv)) gives HS-3 (c) → `CP-accept` and `CP-grant` *not enforceable*. E1 and E1d via X stay *unsupported*, with reasons naming both checkpoints. **L-WDEX-17 and its held-actions-absent variant change *not established* → *unsupported*.** The closing paragraph records that no governed checkpoint is enforceable from the App on SWBPIPE's X |
| **R8-2** (02.5; STD-2; P2.17) | R-5a/R-5b: the AWAITING INPUT token is kept, with the SQ-02 and SQ-20 annotation, and Phase 1 is noted. UNRESOLVED U-30 and U-19 are restated (D6 closed for Phase 1) |
| **R8-3** (Part 3 item 2) | R-7: note on whole-model staleness (SWBPIPE) |
| **R8-4** (03.8) | E1c FXA-2 note: fixture assumption; SWBPIPE has no per-object identity (SQ-03) |
| **R8-5** (01.6, 10.5) | R-14: no SWBPIPE counterpart (accept and apply are one step). R-17: SWBPIPE undo writes no receipt, so "reversed by ⟨receipt⟩" is *not supplied* there |
| R8-7 (01.1) | R-9 (iii): SQ-01 answered: no capture-evidence reference |
| **R8-12** (items 1, 7; closing pass, node A6, in place) | R-4 (ii) Phase 1: the lapse after resume is labelled **"act lapsed at ‹t›"** (nothing says *waiting*). R-5a cites R8-11 item 2 (WD U-34 closed). Consumed inputs list the post-R8 sibling versions; the R5-pass fixture and sibling citations are marked as read then (C-v0.6 §10 carries the fixture). No example, value or L-WDEX label changes |
| (VCs; labels) | Verification rows re-pointed to WD-v0.6, with the E8 row in two parts; inventory WD-EX-v0.6. E1's fixture declaration contract version label is now WD-v0.6, and no checkpoint declares `governed`. The "---" separator before UNRESOLVED is fixed, so the last E8 paragraph no longer renders as a heading |

## Changes from v0.4

L-WDEX numbering is kept stable from v0.4 (EXEC cites it); retired labels are
not reused.

| R5 ID (source) | Change |
|---|---|
| R5-1 (V3-A MAJOR-1) | E8 rewritten with the four ruled hold-support values and their check effects: E1 ⟨rev-3⟩ embedded → *enforced by the host loop* (passes); E1 via X → `CP-accept` *not established* (SQ-02), `CP-check` *not enforceable* (App-only) → **unsupported**; E1d via X → `CP-grant` *not established*; harness-capability kind (a) → *not enforceable*. |
| R5-2 (V3-A m-6) | R-5b no longer presents App-assured as available: the constraint is *host-held* by the host loop's own evaluation in run 12; App-assured is not available in this increment; only host-held satisfies R2-12. |
| R5-3 | E1d states that its declared setting content always binds and that an A8 cannot change it; R-16 notes an A12 on different content satisfies nothing. |
| R5-7 (V3-A MAJOR-3/5) | R-16 (ii)–(v) re-pointed to C **V-GR1** (per R5-7; present in C-v0.5); **L-WDEX-11 retired**. R-16 (i) stays the main-order negative. |
| R5-9 (V3-A m-1, m-2, m-3; V3-B) | FA-n → **FXA-n**; ⟨fx-proj⟩ is **LIB-A1** (plus LIB-A2, AF-1 listed); FXA-5 glossed correctly (⟨rev-3⟩ declares `CP-accept` **and** `CP-check`, from E1); framing paragraph corrected; the v0.4 change-table statement "C §10 declares only V-CP1's CP-accept" is superseded by this row; UNRESOLVED "App-side library" row closed; citations re-pointed to C-v0.4, EXEC-v0.2, CA-v0.2. |
| R6-1 (V4-A MAJOR-2; EXEC F-28) — in place | Every checkpoint now declares its **held actions** (WD §4.3.1). E8 re-classified by held actions (EXEC HS-1, HS-2, HS-5, HS-4, HS-3): E1 via X unchanged (**unsupported**); new E1c row (`CP-check` holds Return → HS-5 → **unsupported**); E1d via X now includes E1c's `CP-check` → **unsupported** whatever SQ-02 returns (was "not established"). New L-WDEX-17 variant for WD VC-43 (new label; existing numbering unchanged). |
| R6-2 (V4-A m-3) — in place | R-16 (iv): in V-GR1's GR-R the refused A12 is T15's own, so **⟨set-1⟩** stays in force (⟨set-2⟩ never takes effect). R-16 (ii)/(iii)/(v) cite GR-1…GR-3, GR-S, GR-P. |
| R6-3 — in place | E8 states what "held" means per value (run stops only under *enforced by the host loop*). |
| R6-4 (V4-A m-1) — in place | "C-v0.5 to add" markers removed; V-GR1 cited in C-v0.5. |
| **R7-3** (V5 MAJOR-3; INTEGRATION, option (a)) — in place | E8 row "L-WDEX-17 with its held-actions element absent": `CP-grant` (kind (a)) has its held actions **derived** as the held OP-C9 call (WD §4.3.1), so it is HS-3 → today **not established** (was HS-5 default → *not enforceable* → *unsupported*). Its workflow result follows EXEC §3.5 precedence with the run's other checkpoints: L-WDEX-17 has none, so today **not established**; after an evidenced SQ-02 answer with a host-held route it passes; answered with none, **unsupported**. A note after the "held" paragraph states the derivation and the scope of the HS-5 default. No other E8 value changes |

## Changes from v0.3

Earlier change tables are in the committed WD-EX-v0.3 and v0.2 (hashes above).

| R4 ID (source) | Change |
|---|---|
| R4-18 (V2 MAJOR-1) | R-5a/R-5b re-pointed to C **V-CP1**; R-5c to C **T15/⟨set-2⟩** (class P-03, scope {FX-W1; {S-4}}). Local L-WDEX-2 and the "C's T15 covers labels only" statement removed. |
| R4-19 (V2 m-3) | OP-C10 class per R3-4: governed by the policy record of the operation whose receipt it reverses. |
| R4-19 (V2 m-8) | Framing stated: the E2 runs read the host workflow ⟨rev-3⟩ **as WD-EX declares it** (E1's checkpoints kept by adaptation). C §10 itself declares only V-CP1's `CP-accept` (FA-5); the meanings agree. |
| R4-19 (V2 m-12, m-13) | Re-pointed to C-v0.3 §10: FA-1…FA-5, OP-C10…OP-C12, T4a, T12's S-5, T16a, V-S1, V-CP1, V-NP1, V-R1, V-X1, V-OU1. "C-v0.3 to add" markers and the *unagreed ×3* divergence row closed. L-WDEX-1 kept (reason stated); L-WDEX-2 and the v0.3 local cases now covered by C (V-S1, V-R1, V-X1, V-NP1, V-OU1) removed; remaining local cases renumbered, each with its reason. |
| R4-20 (W9 CA F-5) | E1 adopts **optional OP-C12** host-check steps at Inspect and Re-examine and an output `host-check-result` (was DEL-09-06 L-CA-1). |
| R4-3 | R-4 shows the re-hold after resume and the withdrawn interim display. |
| R4-4 | R-12b shows "after run end" and a continuation run. |
| R4-5 | R-16 repaired against C's T15→T16 order (T15's A12 precedes the arrival: "prior act, not counted"); new R-9b. |
| R4-6 | R-16 covers established, pending, refused and lost-confirmation A12. |
| R4-7 | New R-6b (MX-3), R-7 (MX-6 "replaced"), R-13b (MX-8 via V-OU1). |
| R4-9 | E1d names its setting content (⟨set-2⟩ content); a variant naming none is invalid. |
| R4-2, R4-8, R4-21 | New **E8**: hold support per checkpoint and surface, App runs *not enforceable* pending D6; harness-capability kind (a). |
| R4-12 | R-9 (iv): elicitation answer is not act evidence. |
| R4-14 | R-5b records the constraint's carriage assurance. |

**Everything below is fixture subject material.** FX-PIPE-01, its rows,
values, people, revisions and runs are invented (C §10). Nothing here is a
SWBPIPE operation, catalog identity, receipt, human act or the selected first
connected operation (`UNRESOLVED{OI-021}`).

**Rendering note (v0.8).** E1 and E1d are rendered in the carriage that
WD-v0.8 §3.5 proposes: the declared part is the JSON block with the info
string `workflow-declaration` in `WORKFLOW.md`, valid against
`workflow-declaration.schema.json` (WD §3.6). That rendering is the fixture.
The Markdown tables beside it explain the same content and are not a second
declaration. Carriage and schema are PROPOSED, with consumer confirmation
pending (WD U-01, U-02). A line `<!-- wd-proto:… -->` marks a block that
`prototype/wdproto.py` compares with its fixture; it does not render.
Revisions such as ⟨rev-A2⟩ are labels for content identities whose algorithm
is unselected (WD U-03). At WD-EX-v0.9 the carriage, the schema and the
declared parts are unchanged: their contract version value stays `WD-v0.8`
(WD-v0.9 §3.3).

**Fixture references (C §10, read directly at v0.7 as C-v0.7; FXA-n were FA-n in C-v0.3).**

| Label | Meaning | Source |
|---|---|---|
| FXA-1 | Every entry exposed on H, E and X (fixture assumption); non-exposure only via V-X1 | C §10.1 |
| FXA-2 | A support row's subject content identity covers location, type, stiffness **and display label** | C §10.1 |
| FXA-3 / FXA-4 / FXA-5 | Relied-on targets of an added support; ⟨set-1⟩ (P-03, *effective (policy default)*, propose) and ⟨set-2⟩ (after T15); **⟨rev-3⟩'s declaration is WD-EX E1: `CP-accept` and `CP-check`** (run 12 carries the governing checkpoint constraint on OP-C4/OP-C5; V-CP1 isolates the direct-grant conflict) | C §10.1 |
| OP-C1 v1 / OP-C2 v1 | Read supports table / Read sustained-load results | C §10.2 |
| OP-C3 v1 | Examine support spacing — requester's **findings (A3)**, never "host checks passed" | C §10.2 |
| OP-C4 v1 / OP-C5 v1 / OP-C9 v1 | Add support / Set support stiffness / Set support label — class P-03, *may apply within granted autonomy* (DERIVED), default propose | C §10.2 |
| OP-C6 / OP-C7 / OP-C8 | Mark row checked (A4) / Accept items (A5) / Reject items (A10) — reserved to the person; the host act facility | C §10.2 |
| OP-C10 v1 | Undo (reverse a receipt); **governed by the policy record of the operation whose receipt it reverses** (R3-4) | C §10.2 |
| OP-C11 v1 | Renumber nodes; class **no policy basis** (reason pending OI-021) | C §10.2 |
| OP-C12 v1 | Run support-spacing **host check** ("host checks passed/failed: support spacing", evaluated basis) | C §10.2 |
| T1…T17, T4a, T16a, Tg | Timeline r12…r17 in g1; B1 = r12, B2 = r13; PR-1 (stale at T7, both items), PR-2 (lineage PR-1); RC-1 at T12 (S-5 created), RC-2 at T16, RC-3 reverses RC-2 at T17 | C §10.3 |
| V-S1, V-CP1, V-NP1, V-R1, V-X1, V-OU1, V-ED1 | Named variants | C §10.4 |
| V-GR1 (GR-1…GR-3, GR-P, GR-R, GR-S) | Run 13 of E1d on E: `CP-grant` arrives at r15 when the OP-C9 call on S-4 is held; T15's A12 is captured after the arrival; the held call is then dispatched unchanged as T16. GR-P pending then lost; GR-R refused at arrival (⟨set-1⟩ stays in force); GR-S a later established A12 narrowing | C §10.4 |
| `supports-adjust` ⟨rev-3⟩, run 12 | The host-origin workflow and run in C §10.1 | C §10.1; here the adaptation of E1 (E3) |
| LIB-A1 ⟨fx-proj⟩ / LIB-A2 ⟨fx-app-import⟩ / AF-1 | App project workflow library (holds ⟨rev-A2⟩); App-side holding library for relayed host workflows; App file "supports-review report" ⟨AF-1@f1⟩ | C §10.1 (App-side fixture subjects) |

**Framing (V2 m-8; V3-A m-2).** E2 reads runs of ⟨rev-3⟩ as WD-EX declares
it: the adaptation keeps E1's `CP-accept` and `CP-check`. C §10.1 FXA-5 states
the same declaration for ⟨rev-3⟩, so C and WD-EX agree; V-CP1 isolates the
direct-grant conflict and V-GR1 (R5-7) the grant checkpoint of E1d.

---

## E1 — App-authored workflow `supports-adjust` (the origin of C's host workflow)

Authored in the Chirality App, reviewed and registered in the project library
(registration is DEL-02-02's; shown only as the resulting identity: revision 1
of LIB-A1's slot `supports-adjust`, registered by the person's A15 at
DEL-01-04's act control, bound to the reviewed bytes; K-6, K-8; WR-v0.2 §4.1,
§4.3; AAC-v0.2 §4.2).

**Identity.** {kind *workflow*, origin *project*, source root ⟨fx-proj⟩ (LIB-A1), name
`supports-adjust`, revision ⟨rev-A2⟩}; derived-from *none*. Its host
adaptation is C §10.1's ⟨rev-3⟩ (E3). In WD-EX-v0.4 the fixture content of
⟨rev-A2⟩ includes the optional OP-C12 steps (R4-20; formerly DEL-09-06
L-CA-1).

**`WORKFLOW.md` — rendered in the PROPOSED carriage (normative for this
fixture; WD §3.5).**

<!-- wd-proto:E1.WORKFLOW.md -->
````markdown
---
name: supports-adjust
description: On one piping run with a support-spacing exceedance, examine the
  spacing (and, where the host offers it, run the host's spacing check),
  propose support changes as one proposal with one item per change, wait for
  the engineer to accept or reject each item, re-examine after application,
  and ask the engineer to mark the changed support rows checked.
---
# Adjust supports for a spacing exceedance

Use this when the engineer names a run and a spacing limit, and wants an
exceedance resolved by adding supports or changing support stiffness.

## Inspect
Read the run's supports table on the current model revision and keep its read
basis. Examine the support spacing against the stated limit. Your findings are
an examination, not the engineer's Checked mark and not a host check. If the
host offers its named support-spacing check, run it too and report its result
as the host states it, in a message whose first line is
`## Host spacing check — supports-adjust`. If neither shows an exceedance,
stop and say so.

## Propose
Draft one proposal, one change item per support added or changed, showing old
and new values, affected rows and why, relying on the basis you read. It is
queued until the engineer accepts or rejects each item; never describe it as
approved. If the host refuses it as stale, re-read and re-draft a new
proposal on the current basis; never retarget the old one.

## Wait for acceptance
Checkpoint `CP-accept`. The engineer accepts or rejects each item in the
host's own proposal view. If all items are rejected, return to Propose once
with the engineer's reason, or stop if they ask. If some are accepted and some
rejected, continue with the accepted items and report the rejected ones.

## Re-examine
After the host applies the accepted items, re-read the supports table,
examine the spacing again and, where offered, re-run the host check. Report
your findings and the host result by reference in one message whose first
line is `## Examination report — supports-adjust`.

## Ask for the Checked mark
Checkpoint `CP-check`. Ask the engineer to mark the support rows the
application changed as checked, in the host. If they decline, stop and
report.

## Return
Summarize what changed (receipt references), your findings, any host check
result, which acts the engineer performed, and what is unknown, in a message
whose first line is `## Summary — supports-adjust`.

## Declared part
The block below is this workflow's declared part (DEL-02-01 WD-v0.8 §3.5). It
states what the method expects, needs, stops for and returns. It grants no
permission, and it is not evidence that anything happened.

```workflow-declaration
{
  "declaration_contract_version": "WD-v0.8",
  "expected_inputs": [
    {
      "name": "run",
      "meaning": "The run the engineer wants resolved (for example R-100).",
      "kind": "person_supplied",
      "necessity": "required",
      "basis_requirement": "One run in the workspace.",
      "stages": ["Inspect"]
    },
    {
      "name": "spacing-limit",
      "meaning": "The spacing limit to examine against.",
      "kind": "person_supplied",
      "necessity": "required",
      "basis_requirement": "Stated with units.",
      "stages": ["Inspect"]
    },
    {
      "name": "supports-table",
      "meaning": "The current supports on the run.",
      "kind": "host_read",
      "read_through": "read-supports",
      "necessity": "required",
      "basis_requirement": "A complete five-element read basis (C §5.1) and per-row subject content identities (C §5.3).",
      "stages": ["Inspect", "Re-examine"]
    }
  ],
  "required_tools": [
    {
      "name": "read-supports",
      "class": "host_operation",
      "operation": "OP-C1",
      "versions": ["v1"],
      "purpose": "Read the supports on the run.",
      "necessity": "required",
      "stages": ["Inspect", "Re-examine"]
    },
    {
      "name": "examine-spacing",
      "class": "host_operation",
      "operation": "OP-C3",
      "versions": ["v1"],
      "purpose": "Examine the support spacing against the limit (the agent's A3 findings).",
      "necessity": "required",
      "stages": ["Inspect", "Re-examine"]
    },
    {
      "name": "host-spacing-check",
      "class": "host_operation",
      "operation": "OP-C12",
      "versions": ["v1"],
      "purpose": "Run the host's named support-spacing check.",
      "necessity": "optional",
      "fallback": "Examination only; report \"host check not run\".",
      "stages": ["Inspect", "Re-examine"]
    },
    {
      "name": "add-support",
      "class": "host_operation",
      "operation": "OP-C4",
      "versions": ["v1"],
      "purpose": "Propose added supports.",
      "necessity": "required",
      "stages": ["Propose"]
    },
    {
      "name": "set-stiffness",
      "class": "host_operation",
      "operation": "OP-C5",
      "versions": ["v1"],
      "purpose": "Propose support stiffness changes.",
      "necessity": "optional",
      "fallback": "Propose added supports only.",
      "stages": ["Propose"]
    }
  ],
  "checkpoints": [
    {
      "name": "CP-accept",
      "required_act": "A5",
      "reached_when": {
        "kind": "host_outcome",
        "tools": ["add-support", "set-stiffness"],
        "outcome": "queued"
      },
      "subject": {"class": "change_items_of_named_proposal"},
      "position": "Wait for acceptance",
      "scope": "Per change item; one A5 may list several items.",
      "purpose": "The engineer decides whether each support change goes into the model.",
      "actor": "the_person",
      "on_negative_decision": {
        "path": "return_to_stage",
        "stage": "Propose",
        "explanation": "All items rejected: return to Propose once with the engineer's reason, otherwise stop."
      },
      "on_mixed_decision": {
        "path": "proceed_on_branch",
        "branch": "Continue with the accepted items and report the rejected ones."
      },
      "expected_act_evidence": {
        "capturing_surface": "host_act_facility",
        "description": "The host's act record of A5 or A10 per item (OP-C7, OP-C8 capture) with its capture-evidence reference."
      },
      "held_actions": {
        "form": "host_operations_only",
        "tools": ["add-support", "set-stiffness"]
      }
    },
    {
      "name": "CP-check",
      "required_act": "A4",
      "reached_when": {"kind": "output_produced", "output": "examination-report"},
      "subject": {
        "class": "objects_changed_by_named_outcome",
        "tools": ["add-support", "set-stiffness"],
        "outcome": "applied"
      },
      "position": "Ask for the Checked mark",
      "scope": "The objects the applied items created or changed.",
      "purpose": "The engineer records their own checking of the changed supports.",
      "actor": "the_person",
      "on_negative_decision": {"path": "stop", "explanation": "Stop and report."},
      "expected_act_evidence": {
        "capturing_surface": "host_act_facility",
        "description": "The host's act record of A4 per object (OP-C6 capture) with its capture-evidence reference, bound to each object's post-application subject content identity. An earlier A4 counts while that content is current, cited with its time (WD I-8)."
      },
      "held_actions": {
        "form": "listed_steps",
        "steps": [{"step": "Return", "app_side": true}]
      }
    }
  ],
  "returned_outputs": [
    {
      "name": "adjustment",
      "meaning": "The support changes.",
      "form": "host_change",
      "destination": "Host supports table, through the host's proposal route.",
      "promised_standing": ["queued", "applied (receipt) per accepted item"],
      "gating_checkpoint": "CP-accept",
      "produced_by": {
        "tools": ["add-support", "set-stiffness"],
        "outcome": "applied"
      }
    },
    {
      "name": "examination-report",
      "meaning": "Spacing findings after application, citing the OP-C3 results and the OP-C1 basis by reference.",
      "form": "message",
      "destination": "The conversation.",
      "promised_standing": ["agent-examined (non-mutating)"],
      "designating_line": "## Examination report — supports-adjust",
      "relies_on": ["read-supports", "examine-spacing"]
    },
    {
      "name": "host-check-result",
      "meaning": "The host's named spacing check, before and after, by reference (optional; produced only where the host offers the check).",
      "form": "message",
      "destination": "The conversation; the result itself stays in the host results view.",
      "promised_standing": [
        "as the host states it: host checks passed: support spacing, or host check failed: support spacing, each with its evaluated basis"
      ],
      "designating_line": "## Host spacing check — supports-adjust",
      "relies_on": ["host-spacing-check"]
    },
    {
      "name": "checked-rows",
      "meaning": "The engineer's A4 on the changed rows.",
      "form": "human_act_standing",
      "destination": "Host supports table.",
      "promised_standing": [
        "marked checked by the person, conditional on CP-check; shown lapsed for affected rows after a lapse (WD I-4)"
      ],
      "gating_checkpoint": "CP-check"
    },
    {
      "name": "summary",
      "meaning": "What changed, which acts the engineer performed, and what is unknown.",
      "form": "message",
      "destination": "The conversation.",
      "promised_standing": ["agent-prepared"],
      "designating_line": "## Summary — supports-adjust"
    }
  ],
  "returned_evidence": [
    {
      "name": "EV-basis",
      "meaning": "The relied-on read basis (for example B1, B2).",
      "kind": "read_basis_reference",
      "supports": ["adjustment"]
    },
    {
      "name": "EV-receipt",
      "meaning": "The host receipt per applied item, as a link, not a copy.",
      "kind": "host_receipt_reference",
      "supports": ["adjustment"]
    },
    {
      "name": "EV-exam",
      "meaning": "The OP-C3 result (A3 findings) with its evaluated basis.",
      "kind": "examination_reference",
      "supports": ["examination-report"]
    },
    {
      "name": "EV-host-check",
      "meaning": "The OP-C12 result with its evaluated basis (T4a).",
      "kind": "host_result_reference",
      "supports": ["host-check-result"]
    },
    {
      "name": "EV-accept-act",
      "meaning": "Human-act records, A5 or A10 per item, with capture-evidence references.",
      "kind": "human_act_record_reference",
      "supports": ["CP-accept"]
    },
    {
      "name": "EV-checked-act",
      "meaning": "Human-act records, A4 per object, with capture-evidence references.",
      "kind": "human_act_record_reference",
      "supports": ["CP-check"]
    }
  ],
  "compatible_roles": ["TASK", "WORKING_ITEMS"]
}
```
````

**The declared part explained (the same content as the block above, in
tables).** *Declaration contract version:* WD-v0.8 (fixture; no checkpoint
declares `governed`).

*Expected inputs*

| input name | meaning | kind | necessity | quality/basis requirement | stage |
|---|---|---|---|---|---|
| `run` | The run the engineer wants resolved (e.g., R-100) | person-supplied choice | required | One run in the workspace | Inspect |
| `spacing-limit` | The spacing limit to examine against | person-supplied value | required | Stated with units | Inspect |
| `supports-table` | Current supports on the run | host read via OP-C1 | required | Complete five-element read basis; per-row subject content identities | Inspect, Re-examine |

*Required tools*

| tool (local name → reference) | class | purpose of use | necessity | version compatibility | stage |
|---|---|---|---|---|---|
| `read-supports` → OP-C1 | host operation | read supports on the run | required | v1 | Inspect, Re-examine |
| `examine-spacing` → OP-C3 | host operation | examine spacing against the limit (A3 findings) | required | v1 | Inspect, Re-examine |
| `host-spacing-check` → OP-C12 | host operation | run the host's named "support spacing" check | optional (fallback: examination only; report "host check not run") | v1 | Inspect, Re-examine |
| `add-support` → OP-C4 | host operation | propose added supports. **Governing checkpoint constraint** {run, `CP-accept`, A5, OP-C4}, recorded with its carriage assurance (WD §4.2.2) | required | v1 | Propose |
| `set-stiffness` → OP-C5 | host operation | propose stiffness changes. Constraint {run, `CP-accept`, A5, OP-C5} | optional (fallback: propose added supports only) | v1 | Propose |

OP-C6/OP-C7/OP-C8 are not required tools: they are the person's act facility
and reserved to the person.

*Checkpoints*

| checkpoint | act | reached-when | subject class | scope | purpose | actor | on negative decision | on mixed decision | expected act evidence |
|---|---|---|---|---|---|---|---|---|---|
| `CP-accept` | A5 accept | (c) observed host outcome *queued* for the proposal this run submits with OP-C4/OP-C5 items | change items of the named proposal (that queued proposal) | per item; one A5 may list several items | engineer decides whether each support change goes into the model | the person | all items A10: return to Propose once, else stop | continue with accepted items; report rejected items | host act record (OP-C7/OP-C8 capture) with capture-evidence reference, captured at or after arrival |
| `CP-check` | A4 mark checked | (b) observed production of output `examination-report` | objects changed by a named outcome: the objects the **applied (receipt)** outcomes of `CP-accept`'s items identify | those objects | engineer records their own checking of the changed supports | the person | act-declined event: stop and report | — | host act record (OP-C6 capture) with capture-evidence reference, bound to each object's post-application subject content identity; an act captured before the arrival counts while that content is current, cited with its time (WD I-8; DECISION-K1 K1-2) |

*Held actions (WD §4.3.1; R6-1):* `CP-accept` — **host operations only**: the
governed OP-C4/OP-C5 change requests (derived from the A5 constraint).
`CP-check` — listed steps: **Return** (an App agent step in App runs; in the
host, a step of the host loop).

*Governed (WD §4.3.1, PROPOSED):* not declared for either checkpoint. In
Phase 1 both are plan guidance (WD §4.3.0). Hold readings below read them as
if declared `governed` (governance phase).

Not declared: A6 *approve* (engineering approval) and A7 *rely*. Reliance on
the model belongs to the accountable professional outside this workflow
(V4-AUT-05).

*Returned outputs*

| output | meaning | form | destination | promised standing | gating checkpoint |
|---|---|---|---|---|---|
| `adjustment` | the support changes | host change via proposal (V4-HI-23) | host supports table | *queued*; per accepted item *applied (receipt)* after host application | `CP-accept` |
| `examination-report` | spacing findings after application | report citing OP-C3 results and the OP-C1 basis by reference | conversation + host results view | *agent-examined (non-mutating)* — A3 findings | — |
| `host-check-result` (optional) | the host's named spacing check, before and after | host result by reference (OP-C12) | host results view | as the host states it: "host checks passed: support spacing" or "host check failed: support spacing", each with evaluated basis | — |
| `checked-rows` | the engineer's A4 on the changed rows | human-act standing | host supports table | *marked checked by the person*, conditional on `CP-check`; shown *lapsed* for affected rows if `CP-check` re-holds (WD I-4) | `CP-check` |
| `summary` | what changed, acts performed, unknowns | message | conversation | *agent-prepared* | — |

*Designating lines (WD §4.4 OP-1…OP-6):* `examination-report` "## Examination
report — supports-adjust"; `host-check-result` "## Host spacing check —
supports-adjust"; `summary` "## Summary — supports-adjust". `checked-rows` has
the form *human-act standing* and names its gating checkpoint (WD §3.6).
`adjustment` names its production: the *applied (receipt)* outcomes of
`add-support` and `set-stiffness` (WD §4.4).

*Returned evidence*

| evidence | kind | supports |
|---|---|---|
| `EV-basis` | relied-on read basis (e.g., B1, B2) | `adjustment` |
| `EV-receipt` | host receipt reference per applied item (link, not copy) | `adjustment` |
| `EV-exam` | OP-C3 result reference (A3 findings) with evaluated basis | `examination-report` |
| `EV-host-check` | OP-C12 result reference with evaluated basis (T4a) | `host-check-result` |
| `EV-accept-act` | human-act record references, A5/A10 per item, with capture-evidence references | `CP-accept` only |
| `EV-checked-act` | human-act record references, A4 per object, with capture-evidence references | `CP-check` only |

*Compatible roles:* TASK, WORKING_ITEMS (fixture choice; host seat per WD §5
and U-09). *Tool restriction:* none declared.

## E1b — Review-only workflow (demonstrates I-3)

{workflow, project, ⟨fx-proj⟩, `spacing-review`, ⟨rev-B1⟩}. Method: read
OP-C1, examine with OP-C3, produce output `findings`, and ask the engineer to
mark the examined rows checked. No proposal is ever made.

| checkpoint | act | reached-when | subject class | on negative decision |
|---|---|---|---|---|
| `CP-review` | A4 mark checked | (b) observed production of `findings` | objects a named output concerns: the rows `findings` identifies, bound through their subject content identities as read (R3-1) | act-declined event: stop |

Along T3–T4 the findings name the span S-2→S-3, so `CP-review` binds S-2 and
S-3 through ⟨S-2@r12⟩ and ⟨S-3@r12⟩ from B1 (R3-1, INTEGRATION). *Held
actions:* listed step **Return** (App-side in App runs).

*Declared part (WD-v0.8 carriage; the content of its `workflow-declaration`
block):*

<!-- wd-proto:E1b.declaration -->
```json
{
  "declaration_contract_version": "WD-v0.8",
  "required_tools": [
    {
      "name": "read-supports",
      "class": "host_operation",
      "operation": "OP-C1",
      "versions": ["v1"],
      "purpose": "Read the supports on the run.",
      "necessity": "required",
      "stages": ["Inspect"]
    },
    {
      "name": "examine-spacing",
      "class": "host_operation",
      "operation": "OP-C3",
      "versions": ["v1"],
      "purpose": "Examine the support spacing against the limit (the agent's A3 findings).",
      "necessity": "required",
      "stages": ["Inspect"]
    }
  ],
  "checkpoints": [
    {
      "name": "CP-review",
      "required_act": "A4",
      "reached_when": {"kind": "output_produced", "output": "findings"},
      "subject": {"class": "objects_named_output_concerns", "output": "findings"},
      "position": "Ask for the Checked mark",
      "scope": "The rows the findings name.",
      "purpose": "The engineer records their own checking of the rows the examination covered.",
      "actor": "the_person",
      "on_negative_decision": {"path": "stop", "explanation": "Stop and report."},
      "expected_act_evidence": {
        "capturing_surface": "host_act_facility",
        "description": "The host's act record of A4 per row (OP-C6 capture), bound to each row's subject content identity as read."
      },
      "held_actions": {
        "form": "listed_steps",
        "steps": [{"step": "Return", "app_side": true}]
      }
    }
  ],
  "returned_outputs": [
    {
      "name": "findings",
      "meaning": "The spacing findings, naming the rows examined.",
      "form": "message",
      "destination": "The conversation.",
      "promised_standing": ["agent-examined (non-mutating)"],
      "designating_line": "## Spacing findings — spacing-review",
      "relies_on": ["read-supports", "examine-spacing"]
    }
  ]
}
```

`findings` is a message output with its designating line, and it names the
read and examination it relies on, which the subject class *objects a named
output concerns* needs (WD §4.3.1, §4.4).

## E1c — Direct application with a later A4 (supports R-5c)

{workflow, project, ⟨fx-proj⟩, `supports-label`, ⟨rev-C1⟩}: labels a support
with OP-C9. **No** A5 checkpoint, so OP-C9 carries no governing checkpoint
constraint and its treatment follows the grant in force.

| checkpoint | act | reached-when | subject class |
|---|---|---|---|
| `CP-check` | A4 mark checked | (c) observed host outcome *applied (receipt)* of OP-C9 | objects changed by a named outcome (the OP-C9 receipt) |

*Held actions:* the only step after arrival is returning the result to the
person — listed step **Return** (App-side in App runs). E1c declares no host
operation to hold after arrival.

By FXA-2 a support's subject content identity covers its display label, so an
A4 bound after the label change lapses when the label changes again (R-17).
This is a fixture assumption: SWBPIPE has no per-object identity (SQ-03), and
its whole-model identity is received for every subject (R8-4).

## E1d — Grant checkpoint (supports R-16)

{workflow, project, ⟨fx-proj⟩, `label-with-grant`, ⟨rev-D1⟩}: as E1c —
including E1c's `CP-check` and its held actions (Return) — plus

| checkpoint | act | reached-when | subject class | declared setting content (R4-9) |
|---|---|---|---|---|
| `CP-grant` | A12 set grant | (a) before dispatch of OP-C9 | grant setting | class P-03; grant value *direct*; scope {model/workspace FX-W1; object set {S-4}} (the content of ⟨set-2⟩) |

The declared setting content always binds (R5-3): an A8 may present it to
Engineer A but never changes the subject, and an A12 made on different content
satisfies nothing at `CP-grant`. *Held actions of `CP-grant`:* **host
operations only** — the held OP-C9 call (kind (a)). A variant of `CP-grant` naming no setting
content is **invalid**, unconditionally (WD FB-17).

**`WORKFLOW.md` — rendered in the PROPOSED carriage (normative for this
fixture; WD §3.5).** E1c's `CP-check` appears here as part of E1d; E1c's own
package declares the same `label-support` tool and `CP-check` without
`CP-grant`. E1d declares no inputs, outputs or evidence, so those three
categories read as **undeclared** (WD §3.4; prototype S-3a).

<!-- wd-proto:E1d.WORKFLOW.md -->
````markdown
---
name: label-with-grant
description: Label one support with a new display label, directly under a
  grant the engineer sets for that support, then ask the engineer to mark the
  labelled row checked.
---
# Label a support under a grant

Use this when the engineer wants one support relabelled without a proposal.

## Label
Checkpoint `CP-grant`. Before you label the support, the engineer sets the
grant this workflow declares: class P-03, grant value direct, on FX-W1 for
that support only. You may show the engineer that setting; you never choose a
different one. Then label the support directly.

## Ask for the Checked mark
Checkpoint `CP-check`. After the host applies the label, ask the engineer to
mark the labelled row checked, in the host. If they decline, stop and report.

## Return
Report the receipt reference, which acts the engineer performed, and what is
unknown.

## Declared part
The block below is this workflow's declared part (DEL-02-01 WD-v0.8 §3.5). It
states what the method expects, needs, stops for and returns. It grants no
permission, and it is not evidence that anything happened.

```workflow-declaration
{
  "declaration_contract_version": "WD-v0.8",
  "required_tools": [
    {
      "name": "label-support",
      "class": "host_operation",
      "operation": "OP-C9",
      "versions": ["v1"],
      "purpose": "Set one support's display label.",
      "necessity": "required",
      "stages": ["Label"]
    }
  ],
  "checkpoints": [
    {
      "name": "CP-grant",
      "required_act": "A12",
      "reached_when": {"kind": "before_dispatch", "tool": "label-support"},
      "subject": {
        "class": "grant_setting",
        "setting": {
          "classes": ["P-03"],
          "grant_value": "direct",
          "scope": {"workspace": "FX-W1", "objects": ["S-4"]}
        }
      },
      "position": "Label",
      "scope": "The declared setting content: class P-03, grant value direct, on FX-W1, object set {S-4} (the content of ⟨set-2⟩).",
      "purpose": "The engineer decides whether the agent may label S-4 directly, without a proposal.",
      "actor": "the_person",
      "on_negative_decision": {
        "path": "stop",
        "explanation": "Stop and report that no grant was set."
      },
      "expected_act_evidence": {
        "capturing_surface": "grant_control",
        "description": "The host control's record of the A12, established with its settings version, bound to the declared setting content."
      },
      "held_actions": {"form": "host_operations_only", "tools": ["label-support"]}
    },
    {
      "name": "CP-check",
      "required_act": "A4",
      "reached_when": {
        "kind": "host_outcome",
        "tools": ["label-support"],
        "outcome": "applied"
      },
      "subject": {
        "class": "objects_changed_by_named_outcome",
        "tools": ["label-support"],
        "outcome": "applied"
      },
      "position": "Ask for the Checked mark",
      "scope": "The support the label change changed.",
      "purpose": "The engineer records their own checking of the relabelled support.",
      "actor": "the_person",
      "on_negative_decision": {"path": "stop", "explanation": "Stop and report."},
      "expected_act_evidence": {
        "capturing_surface": "host_act_facility",
        "description": "The host's act record of A4 (OP-C6 capture) with its capture-evidence reference, bound to the support's post-application subject content identity."
      },
      "held_actions": {
        "form": "listed_steps",
        "steps": [{"step": "Return", "app_side": true}]
      }
    }
  ]
}
```
````

## E1e — A6 and A7 checkpoints, two further input kinds and a harness capability (new at v0.8)

{workflow, project, ⟨fx-proj⟩ (LIB-A1), `supports-approve`, ⟨rev-E1⟩};
derived-from *none*. A local fixture (L-WDEX-39…L-WDEX-41 below): C §10
declares no workflow that requires A6 or A7, and FX-PIPE-01 has no operation
that captures either act (C §10.2: OP-C6 A4, OP-C7 A5, OP-C8 A10). Method:
take the findings of a completed E1b run and the engineer's criteria file;
read the supports; write an approval package into the App project for the
engineer's **engineering approval (A6)**; read the sustained-load results and
report them for the **accountable professional's reliance (A7)**. The two
checkpoints are independent (WD I-3): neither act is needed before the other,
and neither satisfies the other (I-1). EXEC's case CH-32 (L-EXEC-32,
workflow `report-signoff`) is a second fixture for the same VER-003
separation, written in parallel; the two do not conflict (V18-2 n-2).

*Declared part (WD-v0.8 carriage; the content of its `workflow-declaration`
block):*

<!-- wd-proto:E1e.declaration -->
```json
{
  "declaration_contract_version": "WD-v0.8",
  "expected_inputs": [
    {
      "name": "review-findings",
      "meaning": "The findings of a completed run of spacing-review (E1b), naming the rows examined.",
      "kind": "workflow_output",
      "source_workflow": {
        "origin": "project",
        "source_root": "LIB-A1",
        "name": "spacing-review",
        "revision": "rev-B1",
        "output": "findings"
      },
      "necessity": "required",
      "stages": ["Gather"]
    },
    {
      "name": "design-criteria",
      "meaning": "The engineer's supports-review report file in the App project (AF-1), supplied to the run.",
      "kind": "file_supplied",
      "necessity": "required",
      "basis_requirement": "The file's content identity is recorded when it is supplied (⟨AF-1@f1⟩).",
      "stages": ["Gather"]
    },
    {
      "name": "run",
      "meaning": "The run whose supports are to be approved (for example R-100).",
      "kind": "person_supplied",
      "necessity": "required",
      "stages": ["Gather"]
    }
  ],
  "required_tools": [
    {
      "name": "read-supports",
      "class": "host_operation",
      "operation": "OP-C1",
      "versions": ["v1"],
      "purpose": "Read the supports on the run.",
      "necessity": "required",
      "stages": ["Gather"]
    },
    {
      "name": "read-loads",
      "class": "host_operation",
      "operation": "OP-C2",
      "versions": ["v1"],
      "purpose": "Read the sustained-load results for LC-1.",
      "necessity": "required",
      "stages": ["Report loads"]
    },
    {
      "name": "write-package",
      "class": "harness_capability",
      "capability": "file-change",
      "purpose": "Write the approval package file into the App project.",
      "necessity": "required",
      "stages": ["Prepare"]
    }
  ],
  "checkpoints": [
    {
      "name": "CP-approve",
      "required_act": "A6",
      "reached_when": {"kind": "output_produced", "output": "approval-package"},
      "subject": {"class": "named_output", "output": "approval-package"},
      "position": "Ask for approval",
      "scope": "The approval package file as written.",
      "purpose": "The engineer gives or withholds engineering approval of the support arrangement the package describes.",
      "actor": "the_person",
      "on_negative_decision": {
        "path": "stop",
        "explanation": "Stop and report that approval was not given."
      },
      "expected_act_evidence": {
        "capturing_surface": "app_act_control",
        "description": "The App act control's record of A6 on the file's content identity, with its capture-evidence reference (EXEC §5; the control is DEL-01-04's)."
      },
      "held_actions": {
        "form": "listed_steps",
        "steps": [{"step": "Return", "app_side": true}]
      }
    },
    {
      "name": "CP-rely",
      "required_act": "A7",
      "reached_when": {"kind": "output_produced", "output": "load-findings"},
      "subject": {
        "class": "objects_named_output_concerns",
        "output": "load-findings"
      },
      "position": "Ask for reliance",
      "scope": "The sustained-load result rows the load findings name, as read.",
      "purpose": "The accountable professional decides whether to rely on these sustained-load results for the support design.",
      "actor": "the_accountable_professional",
      "on_negative_decision": {
        "path": "stop",
        "explanation": "Stop and report that reliance was not given."
      },
      "expected_act_evidence": {
        "capturing_surface": "host_act_facility",
        "description": "The host's act record of A7 by the accountable professional, bound to each result row's subject content identity as read, with its capture-evidence reference."
      },
      "held_actions": {
        "form": "listed_steps",
        "steps": [{"step": "Return", "app_side": true}]
      }
    }
  ],
  "returned_outputs": [
    {
      "name": "approval-package",
      "meaning": "A file describing the support arrangement and the findings it answers, for the engineer's approval.",
      "form": "file",
      "path": "reports/supports-approval.md",
      "destination": "The App project.",
      "promised_standing": ["agent-prepared"]
    },
    {
      "name": "load-findings",
      "meaning": "The sustained-load results for LC-1, with their read basis and the rows they concern, by reference.",
      "form": "message",
      "destination": "The conversation.",
      "promised_standing": ["agent-prepared"],
      "designating_line": "## Load findings — supports-approve",
      "relies_on": ["read-loads"]
    }
  ],
  "returned_evidence": [
    {
      "name": "EV-approve-act",
      "meaning": "The human-act record of A6 with its capture-evidence reference.",
      "kind": "human_act_record_reference",
      "supports": ["CP-approve"]
    },
    {
      "name": "EV-rely-act",
      "meaning": "The human-act record of A7 by the accountable professional.",
      "kind": "human_act_record_reference",
      "supports": ["CP-rely"]
    },
    {
      "name": "EV-loads-basis",
      "meaning": "The relied-on read basis of the load results.",
      "kind": "read_basis_reference",
      "supports": ["load-findings"]
    }
  ],
  "compatible_roles": ["TASK", "WORKING_ITEMS"]
}
```

| What it shows | Element | Note |
|---|---|---|
| Input of kind **output of another identified workflow run** | `review-findings` | Names E1b's workflow identity and its output `findings`. Which run supplied it, and on what basis, is an observation (WD §4.6), not declared |
| Input of kind **file supplied to the run** | `design-criteria` | AF-1 ⟨AF-1@f1⟩ (C §10.1 App-side fixture subject); its content identity is recorded when it is supplied |
| **Harness-capability requirement** | `write-package`, capability `file-change` (WD §4.2.5, PROPOSED, pin 0.158.0) | The check reads it as *present* only where the acting harness is the App's Codex at the pin and its HCG-A03 availability signal is read (EXEC EV-3, EV-3a: the rule is active for `file-change`; WD §4.2.5 HC-4); otherwise *not established*; never *missing* |
| **A6** checkpoint on App content | `CP-approve`: kind (b) on the file output `approval-package`; subject class *named output* (the file's content identity) | Captured by the App act control (EXEC §5 CAP-1…CAP-3), which DEL-01-04 designs (AAC-v0.2 §4.1, PROPOSED until SCA-V4-003) and has not built, so positive App capture stays AWAITING INPUT (WD U-25). The person's identity is recorded as observed, *identity not verified* (DECISION-K1 K1-4) |
| **A7** checkpoint on host content | `CP-rely`: kind (b) on the message output `load-findings`; subject class *objects a named output concerns* (the LC-1 result rows as read by `read-loads`); actor *the accountable professional* | Captured by a fixture host act facility (L-WDEX-39); the professional is FX-Professional-P (L-WDEX-40) |

Local cases:

- **L-WDEX-39** A fixture host act facility that captures A6 and A7 with
  capture-evidence references. Needed because C §10.2 has no A6 or A7 capture
  operation. On SWBPIPE, A6 and A7 are not software acts (ACT §2.6, from
  SQ-01), so neither checkpoint can be *performed* on SWBPIPE content.
- **L-WDEX-40** FX-Professional-P, an invented accountable professional, as
  ACT §13 L-ACT-6; C names only Engineer A.
- **L-WDEX-41** A test double of the App act control for A6 on App content
  (EXEC CAP-1…CAP-3), standing in for DEL-01-04's control. Readings that
  depend on it are designed, not claimed.

---

## E2 — Run readings along the FX-PIPE-01 timeline

The runs read ⟨rev-3⟩ (E3) in FX-W1, run 12, with Engineer A, in the host
(embedded loop), unless another workflow or surface is named. "Observed"
facts are C's timeline or a named variant; local cases are `L-WDEX-n` with a
reason. Dispositions use WD §4.3.4; outcomes P §9. An act captured before its
arrival counts when it is of the required kind and the content it was made on
is still current, and is cited with its time (WD I-8; DECISION-K1 K1-2);
capture after arrival is only a governance-phase option (EXEC SP-6F). **Phase (R8-1):** dispositions are
record labels in Phase 1 (WD §4.3.0). Where a row shows a hold (the run stops,
a held call stays undispatched, a re-hold, *not permitted* on a constraint's
account), that is the **governance-phase** reading, with the checkpoint read
as governed. In Phase 1 nothing is held, and an action after an arrival may
carry "continued past ‹checkpoint› before ‹act›".

| Run | Steps | Invented observed facts | `CP-accept` | `CP-check` | `adjustment` | Incompatible reading exposed |
|---|---|---|---|---|---|---|
| R-1 success only | T10 | PR-2 validated → *queued*; no act record | waiting (arrival 2, bound to PR-2 items 1, 2) | not reached | items 1, 2 *queued* | "accepted" or "applied" inferred from success (I-2) |
| R-2 mixed | T11–T12, then re-examination | Engineer A accepts item 1 (OP-C7; A5) and rejects item 2 (OP-C8; A10); host applies item 1 → RC-1 (r14), S-5 created, R-100 changed; agent re-reads OP-C1, runs OP-C3 → `examination-report` | **resolved negatively**, annotated "partial: item 1 A5, item 2 A10"; on-mixed path: continue with item 1 | waiting; bound to S-5 and R-100 via ⟨S-5@r14⟩, ⟨R-100@r14⟩ | item 1 *applied (RC-1)*; item 2 *rejected* | showing `CP-accept` as performed or "all accepted"; withholding item 1's application |
| R-3 both accepted | L-WDEX-1 (variant of T11: one A5 lists items 1 and 2 — needed because C's T11 rejects item 2) | Host applies both → receipt L-WDEX-1-RC changing S-5 (created) and S-3 | **performed** (A5 not lapsed by application) | waiting; bound to S-5, R-100 and S-3 | items 1, 2 *applied* | `CP-check` treated as satisfied by acceptance (I-1) |
| R-4 lapse and re-hold | L-WDEX-1 continued; T14 as control | Engineer A marks the bound rows checked (OP-C6; A4) → `CP-check` performed. Then Engineer A edits S-3: (i) before the loop's resume point; (ii) after resume, while the agent is writing `summary`; (iii) after the run ended. Control: T14 edits S-2 (not bound here) | performed (never re-held, R4-3) | (i) **waiting — lapsed at ‹t›**; (ii) **waiting — re-held, lapsed at ‹t› after resume** (governance phase; Phase 1: the act-lapsed event is recorded and labelled **act lapsed at ‹t›** (R8-12 item 1), `checked-rows` shows *lapsed* for S-3, and nothing re-holds or stops): the run stops at its next action, `summary` drafting done so far stays recorded, `checked-rows` shows *lapsed* for S-3, the A4 is requested again for the whole scope with S-3 marked, and an A4 on S-3 alone answers `CP-check` together with the earlier A4 for S-5 and R-100, each citing its referents (WD I-4 joint answer; DECISION-K1 K1-3); (iii) **lapsed** for S-3 only; control: unchanged | applied | carrying A4 onto edited S-3; the withdrawn "performed + act-lapsed" display; undoing actions already taken; re-holding `CP-accept` |
| R-5a forced proposal | C V-CP1 | Variant T15 grants *direct* for P-03 on R-100 and its supports; `CP-accept` declared (FXA-5). After R-5b's refusal the agent submits OP-C4 as a proposal | waiting on the queued proposal | not reached | *queued* | direct application under the grant (D2: no grant widens past a declared checkpoint) — governance phase **AWAITING INPUT** (U-19) — SQ-02 answered 2026-09-28: route (iv), no host-held constraint; SQ-20: no host loop (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3). Phase 1: the agent proposes as plan guidance; `CP-accept` is reached when the proposal queues, and its act is requested and is recorded only when Engineer A performs it (V4-HI-42 as amended; WD I-7; R8-11 item 2 as restated by R9-2, WD U-34 closed; R10-1) |
| R-5b direct request | C V-CP1 | The agent requests OP-C4 directly in run 12; constraint {run 12, `CP-accept`, A5, OP-C4} recorded as *host-held* (the host loop's own evaluation of ⟨rev-3⟩'s declaration, R5-2). App-assured carriage is not available in this increment; a *model-supplied* constraint alone would not satisfy R2-12 | not reached (nothing queued) | not reached | **not permitted**, naming the governing checkpoint constraint; nothing applied | silent conversion into a proposal (R-3.3; R2-12) — governance phase **AWAITING INPUT** (U-19) — SQ-02 answered 2026-09-28: route (iv), no host-held constraint; SQ-20: no host loop (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3). Phase 1: no constraint is carried; the host's own treatment decides and is recorded; if the host applies directly, nothing is queued, so `CP-accept` is not reached: nothing is requested by reason of an arrival that did not occur, no A5 is forced, and none is recorded (WD FB-14; R8-12 item 2 as restated by R9-2 and corrected by R10-1) |
| R-5c direct then A4 | C T15–T16, T16a, with E1c | ⟨set-2⟩: P-03 *direct*, scope {FX-W1; {S-4}}, effective. Agent applies OP-C9 directly (S-4 label "G-4") → RC-2, origin mark, undo route. T16a: Engineer A marks S-4 checked | — (none declared) | waiting from RC-2's *applied* outcome; **performed** by T16a (captured after arrival) | *applied (RC-2)*, direct under ⟨set-2⟩ | treating the direct application or RC-2 as A4 |
| R-6 interruption before queue | L-WDEX-3 (C has no loss before *queued*) | PR-2 submitted; the loop loses observation before any host outcome | **unknown** (the deciding observation was lost) | not reached | **outcome unknown**, reporter: the loop | reporting queued, applied or failed without observation (S-K) |
| R-6b lost decision | L-WDEX-4 (variant of T11: item 1 A5 observed; item 2's decision observation lost) | Host later reports nothing observable for item 2 | **unknown** (MX-3), item 2 annotated unknown | not reached | item 1 accepted; item 2 last observed *queued* | resolving the checkpoint from item 1 alone |
| R-7 stale then re-draft | T5–T10 | PR-1 relies on B1; T6 edit of S-3 (r13); T7 PR-1 both items **refused — stale** (relied B1, current B2); T9 PR-2 (lineage PR-1); T10 PR-2 *queued* | PR-1 never reached *queued*, so no arrival until T10; arrival at T10 binds PR-2's items | not reached | PR-1 refused — stale; PR-2 *queued* | retargeting PR-1; binding `CP-accept` to PR-1. (Fixture per-item staleness; on a whole-model host such as SWBPIPE any model change stales every queued proposal, R8-3) |
| R-7b all items left, replaced | L-WDEX-16 (C has no withdrawal of a queued proposal): after T10 the agent withdraws PR-2 (A11) before any decision, re-reads and submits a new proposal (local label L-WDEX-16-P) that is *queued* | Arrival 2 (PR-2): both items leave → **waiting** "no items remain"; at the new *queued*, arrival 2 is closed "replaced by arrival 3" (final *waiting*) and arrival 3 binds the new items (MX-6) | not reached | PR-2 withdrawn; new proposal *queued* | treating arrival 2 as resolved or performed; carrying any decision across proposals |
| R-7′ run ends early | L-WDEX-5 (run stops after T7) | Run-ended event before any re-draft | **not reached** | not reached | PR-1 refused — stale | reporting `CP-accept` as satisfied |
| R-8 wrong subject | L-WDEX-6 (a second proposal outside this run) | After T10, Engineer A accepts an item of the L-WDEX-6 proposal | waiting | not reached | PR-2 *queued* | counting an A5 on other content (SB-2) |
| R-9 capturing surface | T11 | (i) The agent writes "Engineer A accepted item 1". (ii) Engineer A's A5/A10 captured by the host facility (OP-C7/OP-C8) with a capture-evidence reference; the App faithfully records it, citing that reference. (iii) As (ii), but the host exposes no capture-evidence reference. (iv) The App's Codex asks through an MCP elicitation "accept item 1?" and Engineer A answers yes | (i) waiting; (ii) resolved negatively as R-2; (iii) waiting (U-05b; SQ-01 answered: SWBPIPE exposes no capture-evidence reference); (iv) waiting | — | as R-2 in (ii) | (i) resuming on an agent-authored record; (iii) resuming without capture evidence (I-5); (iv) treating an elicitation answer as A5 (R4-12) |
| R-9b prior act | T2 with E1b variant L-WDEX-7 (`CP-review` binding S-2) | T2's A4 on S-2 (r12) was captured before `CP-review` arrives at T4 | — | `CP-review` (binding S-2): **performed** by T2's A4, an earlier act on ⟨S-2@r12⟩, which is still current at T4; the record cites T2's A4 and its time (I-8; DECISION-K1 K1-2). Under the governance-phase option (EXEC SP-6F): S-2 "prior act not counted — captured before arrival (governance-phase option)"; **waiting** until a new A4 after arrival; if T2's order against the arrival cannot be established, "act order unknown" | — | requiring a repeat of T2's A4 on unchanged content in the current phase; counting it once S-2's content has changed |
| R-10 reserved call | C V-R1 | The agent calls OP-C6 on S-1 | — | — | — | OP-C6 by the agent → **not permitted** (reserved, P-02); an A8 request is *offered*, not recorded unless issued (R2-4); treating the attempt as A4, *not exposed* or *unavailable* |
| R-11 all rejected | L-WDEX-8 (variant of T11 rejecting both items) | A10 on items 1 and 2 | **resolved negatively**; on-negative path: return to Propose once (a later *queued* is a new arrival) | not reached | items *rejected* | counting A10 as performed |
| R-12 act declined | after R-2 | Engineer A declines to mark the bound rows checked → act-declined event with capture evidence | as R-2 | **resolved negatively** (not an A4); on-negative path: stop | as R-2 | recording the decline as A4 |
| R-12b run end and continuation | after R-2; continuation L-WDEX-9 | Engineer A stops the run while `CP-check` waits → run-ended event. Later Engineer A marks S-5 checked. Then Engineer A starts a new run that records *continues ⟨run 12⟩* | as R-2 | run 12: final **waiting** with run-ended event; the later A4 shown **"after run end"**, changing nothing. Continuation: `CP-check` *not reached* until its own arrival; there the earlier A4 counts for S-5 if S-5 is bound and its content is still the one the A4 was made on, cited with its time, and any other bound referent needs a new A4 (I-8; DECISION-K1 K1-2; under the governance-phase option it is "prior act not counted — captured before arrival (governance-phase option)") | as R-2 | resuming run 12; carrying any arrival or disposition into the continuation |
| R-13 retry | T13 | Acknowledgment of RC-1 lost; agent resubmits PR-2 (same identity) | unchanged | unchanged | de-duplicated by identity first: the repeat reports RC-1, never refused stale by its own effect; if unobservable, **outcome unknown** by the observer (R2-13) | a second application; a stale refusal caused by RC-1 |
| R-13b application outcome lost | C V-OU1 | Neither T12 nor T13 report observed | unchanged (decided), item 1 annotated "accepted — application outcome unknown (observer loop)" (MX-8) | not reached for item 1's objects | item 1 **outcome unknown**, last observed *accepted* | re-holding `CP-accept`; inferring application |
| R-14 accepted, then stale | C V-S1 | After T11, Engineer A edits S-2 before T12 (r14′); item 1 (relies on S-2) refused at application — stale | unchanged (decided; MX-7) | not reached for item 1's objects (no applied outcome) | item 1 "accepted by Engineer A — not applied: refused — stale (relied B2, current ⟨B-r14′⟩)"; A5 not lapsed | calling this a lapse of A5; showing item 1 as applied or merely "accepted". (No SWBPIPE counterpart: its A5 is Apply, one step with application, R8-5) |
| R-15 tool permission (App) | L-WDEX-10 (App-side run through the external surface) | The user's Codex mode auto-answers a tool permission (A14) for a shell command | unchanged | unchanged | unchanged | treating A14 as any checkpoint act (D3) |
| R-16 A12 rules | (i) E1d on C's main order T15–T16; (ii)–(v) C **V-GR1** run 13 (R5-7; L-WDEX-11 retired): (ii) GR-1…GR-3, (iii) GR-S, (iv) GR-R, (v) GR-P | (i) **C order:** T15's A12 (⟨set-2⟩) is captured before `CP-grant` arrives when the agent is about to dispatch OP-C9 at T16. (ii) V-GR1: `CP-grant` arrives at r15; T15's A12, with the declared setting content, is captured after the arrival and the control **establishes** it. (iii) V-GR1 sub-variant: a later established A12 narrows the scope. (iv) V-GR1 sub-variant: the A12 is **refused** by the control. (v) V-GR1 sub-variant: the A12 is **pending**, then its confirmation observation is lost. (vi) An A12 on content other than the declared setting content | — | `CP-grant`: (i) **performed** by T15's A12, an earlier act on the declared setting content with ⟨set-2⟩ still in force, cited with its time (I-8; DECISION-K1 K1-2); the OP-C9 call is dispatched unchanged as T16 (Phase 1: the dispatch is recorded). Under the governance-phase option (EXEC SP-6F): **waiting**, "prior act not counted — captured before arrival (governance-phase option)", and the held OP-C9 call stays undispatched. (ii) **performed**; the held call is dispatched unchanged (Phase 1: the dispatch is recorded). (iii) stays **performed**, "superseded by ‹act›". (iv) **waiting**, "A12 refused by control: ‹reason›"; the refused A12 is T15's own, so ⟨set-2⟩ never takes effect and **⟨set-1⟩** stays in force (R6-2). (v) **waiting** "awaiting control confirmation", then **unknown**. (vi) **waiting** (SB-2; R5-3) | (i), (ii): RC-2 as T16 | requiring T15's A12 to be repeated while ⟨set-2⟩ is in force (current phase; U-31 closed by DECISION-K1 K1-2); counting or superseding with a refused A12; letting an A8 change the subject |
| R-17 undo | T16–T17 with E1c | T16a: Engineer A marks S-4 checked after RC-2; run ends; T17 undo RC-3 *reverses RC-2* (OP-C10, governed by P-03 per R3-4) | — | **lapsed** (run ended; FXA-2 covers the label) | RC-2 applied, then reversed by RC-3 | treating the undo as leaving the A4 intact (R2-15). (SWBPIPE undo writes no receipt, so "reversed by ⟨receipt⟩" is *not supplied* there; the lapse shows from the identity change, R8-5) |
| R-E1b independent A4 | E1b, T3–T4 | OP-C1 read (B1); OP-C3 findings name S-2→S-3; `findings` produced; Engineer A marks S-2 and S-3 checked in the host (OP-C6 capture) after the arrival | — | `CP-review` **performed** | — | requiring a prior A5 (I-3) |
| R-E1b′ binding | E1b, T3–T6 (L-WDEX-12: variant marking only the findings, then T6) | (i) Engineer A marks the `findings` output checked, not the rows. (ii) After R-E1b, T6 edits S-3 before the run resumes | — | (i) `CP-review` **waiting** (wrong referent, SB-2); (ii) act-lapsed event for S-3 → **waiting — lapsed at ‹t›**; S-2 still bound | — | binding to the output's own content; lapsing S-2 on an S-3 edit |

## E2b — Run readings for E1e: A6 and A7 (new at v0.8)

An App run of E1e from LIB-A1 through the external surface X, with Engineer A
and FX-Professional-P, on C's timeline after T13 (r14), with the hypothetical
r14 solve of C §10.7 (LC-1 results current at r14). Current phase:
dispositions are record labels (WD §4.3.0) and nothing is held.

| Run | Invented observed facts | `CP-approve` (A6) | `CP-rely` (A7) | Incompatible reading exposed |
|---|---|---|---|---|
| R-18 (i) approval | The agent writes `reports/supports-approval.md` ⟨pkg@p1⟩ (an observed completed file write) → arrival; Engineer A performs A6 on ⟨pkg@p1⟩ in the App act control (L-WDEX-41) | **performed** (A6 by Engineer A; identity recorded as observed, *identity not verified*) | — | treating the file's production as approval |
| R-18 (ii) fabricated approval | After the arrival the agent's message says "the package is approved"; no act record | **waiting** | — | agent text as A6 (S-L; ACT FX-03). An output promising *approved* is invalid (FB-10; E9 L-WDEX-29) |
| R-18 (iii) wrong kind | Engineer A marks S-2 and S-3 checked in the host (OP-C6; A4) | **waiting** (I-1) | — | A4 standing in for A6 |
| R-18 (iv) declined | Engineer A declines approval in the control → act-declined event with capture evidence | **resolved negatively**; on-negative path: stop | not reached | recording the decline as A6 |
| R-18 (v) lapse | After (i) and before the resume point, the agent rewrites the package ⟨pkg@p2⟩ | act-lapsed event; **waiting — lapsed at ‹t›** (I-4) | — | carrying A6 onto ⟨pkg@p2⟩ |
| R-19 (i) reliance | The agent reads OP-C2 for LC-1 at r14 and completes a message whose first line is "## Load findings — supports-approve" → arrival, binding the LC-1 result rows as read; FX-Professional-P performs A7 through the fixture facility (L-WDEX-39) | — | **performed** | treating the agent's report as reliance |
| R-19 (ii) wrong actor | Engineer A, not evidenced as the accountable professional, performs A7 | — | **waiting** (actor requirement; EXEC SP-2) | anyone's A7 counting |
| R-19 (iii) wrong kind | FX-Professional-P performs A6 on the result rows | — | **waiting** (I-1) | approval standing in for reliance |
| R-19 (iv) agent claim | The agent's message says "these results are reliable for design" | — | **waiting** | agent text as A7 (S-L; V4-AUT-05) |
| R-19 (v) earlier act | FX-Professional-P's A7 on the r14 rows was captured before the arrival, and the rows are unchanged | — | **performed** by that earlier act, cited with its time (I-8; DECISION-K1 K1-2). Only if `CP-rely` also declared `governed` and `fresh_act_required`, in the governance phase (EXEC SP-6F): "prior act not counted — captured before arrival (governance-phase option)", **waiting** | requiring a repeat on unchanged content in the current phase |
| R-19 (vi) message without its line | The agent reports the loads in a message whose first line is not the designating line | — | **not reached**; `load-findings` "not produced" (WD §4.4 OP-1; §4.6) | inferring production from message content (RW-1) |

No SWBPIPE counterpart exists for either act (L-WDEX-39); host joins are
deferred (DECISION-3).

---

## E3 — Carried into a host, unadapted and adapted

E1 is carried into the fixture host's workflow library ⟨fx-root⟩ by the
DEL-02-03 carriage procedure (EXEC §6.3 TR-1…TR-8).

| | Original in App project | Carried **unadapted** | **Adapted** (C §10.1) | Reopened in App after refinement |
|---|---|---|---|---|
| kind | workflow | workflow | workflow | workflow |
| origin | project | **project** (unchanged, R-9) | **host** | host while opened (opening does not change it); the registered refinement ⟨rev-A3⟩ is **project** |
| source root | ⟨fx-proj⟩ | ⟨fx-proj⟩ | ⟨fx-root⟩ | ⟨fx-root⟩ while opened; ⟨fx-proj⟩ (LIB-A1) for ⟨rev-A3⟩ |
| name | `supports-adjust` | same | same | same |
| revision | ⟨rev-A2⟩ | ⟨rev-A2⟩ (recomputed on receipt; else "revision not verified", EXEC TF-1) | ⟨rev-3⟩ | a refinement is a DEL-02-02 draft, with no identity, until reviewed and registered by A15 (K-8). Its lineage reaches ⟨rev-A2⟩ through ⟨rev-3⟩, so it registers in LIB-A1 as the next revision of `supports-adjust`: **⟨rev-A3⟩**, revision 2 of the slot (K-6; WR-v0.2 SP-3, DS-2); ⟨rev-A2⟩ stays. The host copy stays ⟨rev-3⟩ |
| derived-from | none | none | {workflow, project, ⟨fx-proj⟩, `supports-adjust`, ⟨rev-A2⟩} | ⟨rev-A3⟩: {workflow, host, ⟨fx-root⟩, `supports-adjust`, ⟨rev-3⟩}, its draft base (WR-v0.2 SP-6). Its prior revision ⟨rev-A2⟩ is named by the A15 record with the reviewed draft content, never by derived-from (R17-11) |
| holding library (listed/selected/resolved; not identity; confirmed EXEC §6.2) | ⟨fx-proj⟩ | ⟨fx-root⟩ (received link); ⟨fx-proj⟩ at the exported link | ⟨fx-root⟩ | the opened host copy: LIB-A2 ⟨fx-app-import⟩; ⟨rev-A3⟩: LIB-A1 ⟨fx-proj⟩ (CA §3.2, §4) |

Adaptation in ⟨rev-3⟩ (fixture): `spacing-limit` becomes optional with the
fallback "use the host project's stated limit"; the prose refers to the
host's own proposal view by name. Checkpoint names, act kinds, reached-when
conditions and subject classes are unchanged, so each is **preserved** with a
derived-from checkpoint link (EXEC AD-2, AD-4). Runs of ⟨rev-A2⟩ and ⟨rev-3⟩
never share acts or dispositions (EXEC AD-5).

---

## E4 — Same-name collision in the host library

After E3, ⟨fx-root⟩ holds two workflows named `supports-adjust`: the unadapted
copy {…, project, ⟨fx-proj⟩, …, ⟨rev-A2⟩} and the adapted {…, host,
⟨fx-root⟩, …, ⟨rev-3⟩}.

| Step | Discovery shows | Selection holds | Required consumer behavior |
|---|---|---|---|
| 1 | Two entries, each with origin and holding library ⟨fx-root⟩; collision reported | Engineer A explicitly selects host ⟨rev-3⟩ | Both origins listed with holding library (C-1); the panel shows "project-origin, held in ⟨fx-root⟩" for the copy. |
| 2 | A user-library copy ⟨rev-U1⟩ appears in the App | unchanged | Three origins listed; no rebinding despite Root ordering (C-2, C-5). |
| 3 | The host library registers ⟨rev-4⟩ of the host workflow | ⟨rev-3⟩ selected. App side: the selection stays pinned on ⟨rev-3⟩; ⟨rev-4⟩ is shown as newer, and following it is a new selection event (WR-v0.2 SL-2, PROPOSED). Host side: whether a host run follows ⟨rev-4⟩ is the host's policy, open (U-10) | The chain shows which revision was resolved and supplied (C-4); replay reads the revision recorded for the run (EXEC RP-5). |
| 4 | Engineer A explicitly reselects the project-origin copy | {…, project, ⟨fx-proj⟩, …, ⟨rev-A2⟩}, held in ⟨fx-root⟩ | New selection event, not a rebinding (C-3). Identity equality ignores the holding library (C-6). |

---

## E5 — A Root prose-only workflow read under v4 (real bytes, repo 6e18505e3)

Root's bundled `create-workflow` has front matter `name`/`description`,
prose, and no `execution.json` or declared part.

| Category | Reading |
|---|---|
| Expected inputs, outputs, evidence | **undeclared** |
| Required tools | **undeclared** → check **not established**; selectable, never "runnable" by check |
| Checkpoints | **undeclared**. The prose's human review before registration is not product-held: it has no reached-when, subject class or act kind. A consumer may report the prose (FB-07 style) but shall not synthesize a checkpoint. |
| Identity | {workflow, bundled, `chirality-root`, `create-workflow`, revision per U-03} |

**Reading in the carriage (WD-v0.8; prototype S-5).** The real
`create-workflow/WORKFLOW.md` has no `workflow-declaration` block, so every
category is **undeclared** (WD §3.5 CR-4; FB-01) and no checkpoint is
synthesized from the prose. Variant (VC-04): the same bytes followed by a
block declaring `"checkpoints": []` read as checkpoints **declared empty**,
with the other four categories **undeclared**.

---

## E6 — Root restriction misread as requirement (negative fixture)

Root `workflows/project-dag/execution.json` (repo 6e18505e3) declares
`compatible_roles: [WORKING_ITEMS]` and `tools.capabilities: [read, write,
bash, delegate_agent, report_coordination_notice, send_agent_update,
ack_agent_update]`.

| Reading | Verdict |
|---|---|
| "The workflow requires these seven tools; check them against the host" | **Incompatible.** They are a restriction ceiling, not V4-WF-01 required host tools (WD §4.2.3). |
| "Required tools undeclared; restriction retained; compatible role WORKING_ITEMS; a host seat without delegation reports **unsupported**" | **Compatible** (FB-05; WD §4.7). |

**Reading in the carriage (WD-v0.8; prototype S-6).** The real `project-dag`
package has no block: required tools **undeclared** (FB-05), the restriction
retained as a ceiling (seven names), and compatible role WORKING_ITEMS from
`execution.json`. Rendered as a v4 package (its `WORKFLOW.md` followed by a
block carrying `compatible_roles` and `tool_restriction` taken from
`execution.json`), the reading is the same: `tool_restriction` never feeds
`required_tools`, which stays **undeclared**. Where a block's
`compatible_roles` differ from the package's `execution.json`, the roles are
**not established** (WD FB-22).

---

## E7 — Compatibility outcomes and the pass rule (FXA-1 base)

| Case | Situation | Outcome per requirement | Pass? |
|---|---|---|---|
| Base | E1 ⟨rev-3⟩ on the embedded surface: OP-C1, OP-C3, OP-C4, OP-C5, OP-C12 exposed (FXA-1) | all **present** | passes on requirements (hold support: E8) |
| L-WDEX-13 (no C entry is absent) | OP-C4 absent from the catalog edition | OP-C4 **missing** | does not pass (required) |
| L-WDEX-13b | OP-C12 absent | OP-C12 **missing** | passes (optional; "host check not run" shown) |
| C V-X1 | E1c on the external surface X: OP-C9 element 9 = *not exposed on this surface* | OP-C9 **not exposed on this surface** | does not pass on X; unaffected on E |
| C §10.6 (T8) | A workflow requiring OP-C2, checked at r13 | OP-C2 **present, currently unavailable** ("No current solve for LC-1 at this revision", basis B2) | passes; shown as a run-time hold with the reason |
| External access off | Any workflow on X while A13 is not performed: the App reports **channel not enabled** if its own configuration is off, the host if the host channel is off (R4-16) | **channel not enabled** for every requirement on X | does not pass on X; never shown as missing |
| C V-NP1 | A workflow requiring OP-C11 (*no policy basis*, pending OI-021) | OP-C11 **present**; direct is *not permitted*, proposing confers no permission (R2-9) | passes the requirement check; dependent production reported **held** |
| E5 reading | Root prose-only package | **not established** (undeclared) | selectable; never "runnable" by check |

**Optional-absent case (EXEC F-25; dispositioned at v0.7).** L-WDEX-13b
(OP-C12 absent) stays this file's single optional-absent example. EXEC's
L-EXEC-26 (OP-C5 absent; EXEC MT-4) is not adopted as a shared case: it stays
an EXEC local case, and no L-WDEX label is added.

---

## E8 — Checkpoints per surface: Phase 1 and governance phase (R5-1; R6-1; R6-3; R8-1; R8-2)

**Phase 1 (R8-1; WD §4.3.0; EXEC §2.1).** Every checkpoint below is plan
guidance. No hold-support value is assigned, no workflow is *unsupported* for
a hold reason, neither the App nor the host loop holds anything, and acts are
recorded only when the person performs them. The requirement check depends on
the required tools and the channel state. Rows via X assume FXA-1 and an
enabled channel. With external access off, every row via X does not pass, on
channel state (E7 "External access off").

**Governance phase (retained; WD §4.3.8; EXEC §3.6).** Each checkpoint is read
as if declared `governed` (no fixture declares the flag). The compatibility
report assigns hold support by the checkpoint's **held actions** (WD §4.3.1),
evaluating HS-1, HS-2, HS-5, HS-4, HS-3 in that order. Workflow precedence
(EXEC §3.5): any *not enforceable* → **unsupported**; otherwise any *not
established* → **not established**. On X the values apply SWBPIPE's SQ-02
answer (2026-09-28: route (iv), none planned → HS-3 (c)), as EXEC does.

| Workflow / surface | Checkpoint (held actions) | Phase 1: checkpoint · requirement check | Governance phase: rule → hold support | Governance phase: workflow requirement check |
|---|---|---|---|---|
| E1 ⟨rev-3⟩, embedded host loop (E) | `CP-accept` (OP-C4/OP-C5) | guidance · **passes** (E7 Base); the host loop holds nothing | HS-2 → **enforced by the host loop** (its own evaluation of the constraint is *host-held*) | **passes** (holds subject to host evidence, DEP-001; SWBPIPE has no host loop, SQ-20) |
| | `CP-check` (Return) | guidance | HS-2 → **enforced by the host loop** | |
| E1 ⟨rev-A2⟩ run from the App via X (L-WDEX-14) | `CP-accept` (host operations only: OP-C4/OP-C5) | guidance · **passes** | HS-3 (c) → **not enforceable** (SQ-02 answered 2026-09-28: no host-held route) | **unsupported** — "checkpoint hold not enforceable on this surface: CP-accept, CP-check" |
| | `CP-check` (Return, App-side) | guidance | HS-5 → **not enforceable** (D6; neither HP-1 nor HP-2 adopted) | |
| E1c from the App via X | `CP-check` (Return, App-side) | guidance · **passes** | HS-5 → **not enforceable** | **unsupported** |
| E1d from the App via X | `CP-grant` (host operations only: the held OP-C9 call) | guidance · **passes** | HS-3 (c) → **not enforceable** (SQ-02 answered 2026-09-28) | **unsupported** — "…: CP-grant, CP-check" |
| | `CP-check` (Return, App-side; from E1c) | guidance | HS-5 → **not enforceable** | |
| L-WDEX-15: a workflow whose checkpoint is kind (a) before a Codex **harness capability** (e.g., `shell-command`, WD §4.2.5, PROPOSED), App run | that checkpoint (an App harness action) | guidance · **not established** (the harness-capability reference: its name is PROPOSED at WD-v0.8; EXEC EV-3's rule for `shell-command` is active, but this example reads no thread-start signal, as EXEC MT-15) | HS-5 → **not enforceable** (R4-21) | **unsupported** (WD FB-18) |
| L-WDEX-17 (E1d variant with no `CP-check`, needed to show HS-3 alone): `CP-grant` only, App run via X | `CP-grant` (host operations only: OP-C9) | guidance · **passes** | HS-3 (c): **not enforceable** (SQ-02 answered 2026-09-28: no host-held route). It would be *enforced on the host route* only if a host offered and evidenced one | **unsupported** — "checkpoint hold not enforceable on this surface: CP-grant" (was *not established* in v0.5) |
| L-WDEX-17 with its held-actions element absent | `CP-grant` (undeclared; derived as the held OP-C9 call, kind (a); WD §4.3.1, R7-3) | guidance · **passes** | HS-3 (c): **not enforceable**, as above | By EXEC §3.5 precedence with the run's other checkpoints: L-WDEX-17 has none, so **unsupported** (was *not established* in v0.5). Were it combined with E1c's `CP-check`, as in E1d, the result would be the same, *unsupported* |

**What "held" means.** *Phase 1:* nothing is held. If Engineer A runs E1 from
the App, a file Codex writes after `CP-check` arrives and before the A4 may
carry "continued past CP-check before A4". That is information, not a
defect. *Governance phase (R6-3):* under *enforced by the host loop* the run
stops at its next action. Under *enforced on the host route* the host refuses
the held host operations, and any other action is recorded as *action during
hold*. Under *not established* or *not enforceable* nothing is stopped: each
arrival records its value, and, for example, a file Codex writes while
`CP-check` waits is recorded as **action during hold**. HP-3 (an App
named-rule *decline* of a tool-permission request) may be used as a best
effort under D3; it never makes a hold *enforced*.

When the held-actions element is absent, an A5 checkpoint's held actions are
derived as its governed operation(s), and a kind (a) checkpoint's as its held
call. The HS-5 default applies only to a kind (b)/(c) checkpoint with no
held-actions element (an A5 checkpoint takes the derivation, EXEC §3.6), or
to one whose declared held actions do not show host operations only (WD
§4.3.1; R7-3; V6 m-5).

In the governance phase, SQ-02's answer moves HS-3 rows only. Checkpoints
holding an App-side step (Return) stay *not enforceable* (R5-10). An author who
needs App enforceability keeps a governed checkpoint's held actions on host
operations (R6-1; CA WR-11). Against SWBPIPE (SQ-02 answered: route (iv)) no
host-held route is available, so **no governed checkpoint is enforceable from
the App on X in this increment**, and every such workflow run from the App on
X is *unsupported* in the governance phase. The advice stands for a host that
offers a host-held route. In Phase 1 none of this affects the check.

---

## E9 — Declaration variants and their readings (new at v0.8; WD §3.7)

Each variant changes one thing in E1, E1d or the carriage. The reading is
WD §3.7's, of the declaration only: no run is implied. `prototype/wdproto.py
selftest` produced exactly these readings on 2026-09-30 (S-7; WAVE_B/B1.md; L-WDEX-42 and the rerun after the RP-3 repair: WAVE_B/RP-3.md).

| Label | Change | Reading (WD §3.7) | Case |
|---|---|---|---|
| L-WDEX-18a, 18e, 18b, 18c | E1 `CP-check` `required_act` "A2", "A3", "A14", "A15" | **invalid** (FB-03). A15 is ACT's PROPOSED "register workflow revision" (R12-5), a recognized act outside the closed list | VC-12 |
| L-WDEX-18d | E1 `CP-check` `required_act` "approve-design" | **not established** (FB-04) | VC-12 |
| L-WDEX-19a, 19b | E1 `CP-accept` reached-when kind (a) on `add-support`; kind (b) on `summary` | **invalid** (FB-16) | VC-29 |
| L-WDEX-19c | E1 `CP-accept` subject "objects changed by a named outcome" | **invalid** (FB-16) | VC-29 |
| L-WDEX-19d | E1 `CP-check` subject "targets of the held call", kind (b) | **invalid** (FB-16; R3-2) | VC-29 |
| L-WDEX-20 | E1d `CP-grant` subject without `setting` | **invalid** (FB-17) | VC-41 |
| L-WDEX-21a, 21b, 21c | E1d `CP-grant` with `"governed": "yes"`; without `governed`; with `"governed": "maybe"` | recognized and governed; recognized and not governed; recognized, with governance **not established** and the value preserved (FB-19). In the current phase all three are guidance with identical results | VC-45 |
| L-WDEX-22 | E1 with a second checkpoint named `CP-check` | both **invalid** (FB-20) | VC-48 |
| L-WDEX-23 | E1 `CP-check` reached-when names output `final-report`, which is not declared | **invalid** (FB-13) | VC-48 |
| L-WDEX-24 | E1 `examination-report` without its designating line | the output **not established** (malformed); `CP-check`, whose reached-when names it, **not established** (§3.4) | VC-49 |
| L-WDEX-25 | E1 `CP-check` with an extra member `"priority": "high"` | **not established** (§3.4); preserved | VC-48 |
| L-WDEX-26 | E1 `CP-check` held actions `{"form": "some"}` | checkpoint recognized; its held actions do not show host operations only, so the governance-phase conservative default applies (R10-10); no failure row | VC-43 |
| L-WDEX-27a | E1d `CP-grant` with `governed` and `fresh_act_required` both "yes" | recognized. Governance phase: EXEC SP-6F applies to its arrivals. Current phase: shown; SP-6 records | VC-51 |
| L-WDEX-27b | E1d `CP-grant` with `fresh_act_required` "yes" and no `governed` | recognized; shown with a note that it has no effect in any phase (WD FA-3) | VC-51 |
| L-WDEX-28 | E1 `CP-check` with `on_subject_absent` returning to Re-examine | recognized; dispositions unchanged (EXEC §4.7: *waiting* "subject absent") | VC-52 |
| L-WDEX-29 | E1 `adjustment` also promising "approved" | the output **invalid** (FB-10) | VC-48 |
| L-WDEX-30 | E1 `EV-basis` supports `nothing-here` | the evidence **not established** (FB-21) | VC-48 |
| L-WDEX-31 | E1 plus a required tool with capability `gpu-compute` | that reference **not established** (§3.4; WD §4.2.5 HC-5) | VC-50 |
| L-WDEX-32 | E1 plus a top-level member `x_note` | preserved and reported; categories unaffected | VC-48 |
| L-WDEX-33a, 33b | E1 with contract version "WD-v0.9"; with "WD-v0.7" | declared part **not established**, preserved (§3.3). Unchanged at WD-v0.9: the document label moved, the declared-part value stays `WD-v0.8` (WD §3.3) | VC-48 |
| L-WDEX-34 | E1 block with the member `checkpoints` twice | **FB-02**: declared part not established | VC-46 |
| L-WDEX-35 | E1 `WORKFLOW.md` with a second `workflow-declaration` block | **FB-02**: nothing read | VC-46 |
| L-WDEX-36 | A `workflow-declaration` block quoted inside a four-backtick fence | not read: no declared part (CR-2) | VC-46 |
| L-WDEX-37 | E1 `summary` given `examination-report`'s designating line | both outputs **not established** (FB-20, DN-4); `CP-check` **not established** | VC-49 |
| L-WDEX-38 | E1 `summary` made a workflow-input output and named by `CP-check`'s kind (b) | `CP-check` **invalid** (FB-13) | VC-49 |
| L-WDEX-42 | E1e `approval-package` (a file output) without `path` (RP-3 repair) | the output **not established** (FB-02); `CP-approve`, whose kind (b) names it, **not established** (§3.4; WD §3.7 VO-5) | VC-48 |

The schema's invalid example instance (`workflow-declaration.invalid.example.json`)
is read element by element, not rejected whole: `read-supports` and
`write-report` **not established**; `CP-check` **invalid** (FB-03, with FB-19
and the unrecognized reached-when kind also reported); `summary` **not
established**; compatible roles **not established** (prototype S-8).

---

## UNRESOLVED

Same register as WD-v0.9 §12. Items that shape these examples:

| item | owner | point of need | effect on these examples |
|---|---|---|---|
| U-01/U-02 carriage and representation: **PROPOSED at WD-v0.8** (WD §3.5, §3.6) | DEL-02-01, with consumer confirmation (DEL-02-03, DEL-05-01, DEL-05-02) | the next comparison (V18) | E1 and E1d are rendered in the proposed carriage; the tables explain them |
| U-08 harness capability names: **PROPOSED at WD-v0.8**, scoped to pin 0.158.0 (WD §4.2.5) | DEL-02-01 with DEL-01-01 and DEL-02-03 | before the App-side required-tool check | E1e `file-change` and L-WDEX-15 `shell-command` read as recognized names; presence follows EXEC EV-3 and EV-3a (node G): with no signal read, *not established* |
| U-32 on subject absent: **decided at WD-v0.8 (PROPOSED)** | DEL-02-01 | — | L-WDEX-28 |
| U-03 revision algorithm | DEL-02-01 with DEL-04-03 | before revision comparisons | ⟨rev-A2⟩, ⟨rev-3⟩ are labels |
| U-30 App-side holds `UNRESOLVED{D6}`: **closed for Phase 1** (DECISION-4; R8-2), re-opens with the governance phase; SQ-02 decides host-operation checkpoints only (R5-10) and is answered (route (iv)) | Owner (DECISION-4; D6 re-opens with the governance phase) | when the governance phase is taken up; before any governed App-run hold is claimed | E8 Phase 1: guidance, no values. Governance phase: App-only rows *not enforceable*, host-operation rows *not enforceable* (SQ-02 answered 2026-09-28) |
| U-19 host-held constraint on the host route for App runs (SQ-02; answered: route (iv), none) | SWBPIPE owner decision to plan any route (ANS §2); DEL-03-02 element | before governance-phase host-side fixtures | R-5a/R-5b governance phase **AWAITING INPUT** (STD-2 annotation); E8 governance phase: App `CP-accept` and `CP-grant` *not enforceable*; Phase 1: guidance |
| U-05b capture-evidence reference (SQ-01 answered: none) | SWBPIPE owner decision (PB-TBD-002; DEL-16-03) | before host act-recording integration | R-9 (iii) stays waiting |
| U-31 capture after arrival vs counting prior acts — *closed by DECISION-K1 K1-2 (2026-09-30)* | The owner (decided) | — | R-9b, R-12b and R-16 (i) count an earlier act on current content, cited with its time (I-8); capture after arrival is the governance-phase option (EXEC SP-6F) |
| U-05c multi-row A4 purpose after partial lapse — *closed by DECISION-K1 K1-3 (2026-09-30)* | The owner (decided) | — | R-4: an A4 on the lapsed rows alone answers together with the earlier A4 (WD I-4 joint answer) |
| U-25 App act control construction — *closed as a decision by DECISION-K1 K1-4 (2026-09-30)* | The owner (decided); construction DEL-01-04 (designed in AAC-v0.2; not built) | before App capture fixtures (control) | Person identity recorded as observed, *identity not verified* (EXEC CAP-8); the control's obligation proposed for DEL-01-04's contract at the next amendment; App-side positive capture still not shown |
| U-09 host seat role mapping | DEL-02-01 with SWB owner and DEL-02-04 | before host role guidance | E1 compatible roles are a fixture choice |
| U-10 precedence and revision following | DEL-02-02 with host owner | before host-origin discovery | App side PROPOSED (WR-v0.2 SL-2, SL-3): E4 step 3 pinned on ⟨rev-3⟩; its host side left open |
| U-15 / U-05 `UNRESOLVED{OI-021}` | owner via outside SWB session | before connected-activity SoW | FX-PIPE-01 entries are not the selected operation; OP-C11's reason cites it |

## Verification cases

These examples are inputs for WD-v0.9 §13. None has been run against a consumer
or a host. Rows marked *(prototype)* had their declaration part read by
`prototype/wdproto.py` on 2026-09-30 (WD §13.1; WAVE_B/B1.md), and again at
WD-EX-v0.9 on 2026-10-02 (62 checks, 62 passed; a later run failed only
S-11's group count after HOSTING added a group; WD §13.1).

| Example | Used by | Expected result summary | VER |
|---|---|---|---|
| E1 | VC-01, VC-03, VC-05, VC-29, VC-30 | Categories incl. subject class and optional OP-C12 recovered; references compared to C §10; invalid A5 variants rejected; `CP-check` binds applied objects | VER-001, VER-002, VER-003 |
| E1b | VC-08, VC-36 | A4 performed without any A5; binding to the examined rows | VER-003 |
| E1c + E2 R-5a/b/c | VC-11 | Phase 1: guidance, no constraint carried. Governance phase: AWAITING INPUT (host side) for V-CP1 (SQ-02 answered: none); R-5c designed on T15–T16a | VER-003 |
| E1d + E2 R-16 (main order and V-GR1) | VC-32, VC-41 | Earlier A12 on current content counts (main order); established/pending/refused/lost; supersession; other-content A12; FB-17 variant | VER-003 |
| E2 R-1, R-2, R-3, R-4, R-6, R-6b, R-7, R-7b, R-7′, R-8, R-9, R-9b, R-10, R-11, R-12, R-12b, R-13, R-13b, R-14, R-15, R-17 | VC-07, VC-24, VC-09, VC-10, VC-15, VC-40, VC-20, VC-40, VC-20, VC-21, VC-22/VC-42, VC-39, VC-16, VC-23, VC-23, VC-31, VC-34, VC-40, VC-27, VC-28, VC-35 | Only evidenced acts counted; shared dispositions, annotations and events as tabulated; unknown stays unknown | VER-003, VER-004 |
| E3 | VC-02, VC-14, VC-26 | Unadapted keeps origin; adapted has derived-from; holding library separate | VER-001, VER-004 |
| E4 | VC-13 | No rebinding; all origins with holding library | VER-004 |
| E5 | VC-04 | All categories undeclared; no synthesized checkpoint | VER-002 |
| E6 | VC-06 | Restriction not read as requirement | VER-002 |
| E7 | VC-25, VC-33 | Distinct outcomes; pass rule | VER-002 |
| E8 | VC-37, VC-38, VC-43, VC-44, VC-45 | Phase 1: guidance, no values, results on required tools and channel state (L-WDEX-15 *not established*); no hold claimed. Governance phase (read as governed): values by held actions; embedded passes; E1, E1c, E1d and L-WDEX-17 (both) via X **unsupported** (SQ-02 answered → HS-3 (c)); no App hold claimed | VER-001, VER-003 |
| E1, E1d rendered; E1b, E1e JSON *(prototype)* | VC-03, VC-46, VC-47 | One block extracted and parsed; round trip equal; valid against the schema; Python and node readers agree | VER-002 |
| E1e + E2b R-18, R-19 | VC-50, VC-53, VC-54, VC-55 | A6 and A7 counted only from their own kind, actor and capturing surface; both input kinds and the harness capability read *(prototype: declaration part)* | VER-002, VER-003 |
| E9 *(prototype)* | VC-12, VC-29, VC-41, VC-45, VC-48, VC-49, VC-51, VC-52 | Readings as tabulated in E9 | VER-002, VER-003 |
| E5, E6 in the carriage *(prototype)* | VC-04, VC-06 | As E5 and E6 | VER-002 |
| Inventory | VC-19 | Examples identified by WD-EX-v0.9 (declared parts at `WD-v0.8`, WD §3.3); all DESIGNED, AWAITING INPUT or HELD, with the declaration parts the prototype ran | VER-007 |
