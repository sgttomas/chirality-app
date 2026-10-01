# Minimal-loop and model receiving contract
- Contribution: DEL-05-01/LOOP-v0.8 (supersedes DEL-05-01/LOOP-v0.7, last changed at `c896a99d90`, file sha256 6f1778e6b39f3bff76a6e577ad34da5332c83cc05b5507ead810a08a6039ff24; earlier: LOOP-v0.6, last changed at `caa4334ca` and unchanged at `3dd7c22c73`, file sha256 246f4636166c67250f73862de586afef3cad91ba538272880a80c2fd657a5767; earlier: LOOP-v0.5, last changed at `375c3970c` and unchanged at `94aa9181b`, file sha256 0ec980b53c4dd473b365f7e8407593a218023ad2277da7680694c852808bd737; LOOP-v0.4 sha256 ffc30483…95934e at `8fb51f07f`)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Phase (V4-WF-05 and V4-HI-42 as amended by SCA-V4-001; R9-1; R8-1; DECISION-4 D4-1 and clarification): when a run reaches a declared checkpoint, the required human act is requested, and it is recorded as done only when the person performs it, whatever the autonomy setting. Holding the run at the checkpoint until the act is performed is phased to the governance layer: in the current phase (Phase 1) a checkpoint is **plan guidance** that the person and the agents manage, and neither the App nor a host's embedded loop **enforces a hold**, blocks a run, or reports a workflow unsupported because a hold cannot be enforced. The reserved acts (V4-HI-30) still bind (§2.4.0). In the current phase the agent carrying out the workflow asks for the act (R9-1; SETTLED by DECISION-K1 K1-1; §2.4.0 LP-5). The host-loop hold (§2.4.4, LH-0…LH-4) and the hold content of §2.4.1–§2.4.3 are kept as the **governance-phase definition (retained)**, not deleted.
- Model access (V4-HOST-01 and V4-ARC-11 as amended by SCA-V4-001; R8-9; DECISION-4 D4-3): a cloud model is reached by **OAuth sign-in or an API key**, and there is **no default** between local and cloud, only options the person chooses among (§5.1). V4-HOST-02 is cited **as amended by SCA-V4-001** (DECISION-5; R8-13; §5.1 NW-2).
- Network destinations (V4-HOST-02, V4-ARC-12 and the ARCH §4 host-agent property as amended by SCA-V4-001; R8-13; DECISION-5): the host's embedded agent sends data only to the selected model service and to destinations the person allows, by a two-level allow list or by an in-work grant scoped once, this run or always. MCP servers are allowed only if they follow the stateless MCP revision 2026-07-28. An always-off list applies, and every destination contacted is recorded and shown in any model mode (§5.1.1 NW-8…NW-16; MS-14…MS-27). Phase 1 and the governance phase are split per DECISION-4's principle. From v0.8 (node B5) §5.3 is the **one account of the destination flow** (DF-1…DF-10) that ACT, AS, RS, PANEL, C, P and ADAPTER cite; recording a declined or refused request is PROPOSED everywhere (R12-10).
- Model interface for fixtures (R12-8; v0.8): the fixtures and the malformed-call rules are written against **FB-CC-1, a published Chat Completions reference, labelled "fixture basis, not a product selection"** (§4.1). DEL-05-01 REQ-002 forbids selecting a product protocol version before its basis exists, so DEP-05-01-024 stays open for the product; FB-CC-1 selects no provider, server, model or version for any host.
- Serves: OUT-001, OUT-002, OUT-003, OUT-004; REQ-001–REQ-007; AC-001–AC-009; VER-001–VER-009 (all of DEL-05-01)
- Basis: the accepted basis as amended by scope-change amendments SCA-V4-001 (`_ScopeChange/SCA-V4-001_2026-09-28_2155/`, accepted 2026-09-29) and SCA-V4-002 (`_ScopeChange/SCA-V4-002_2026-09-29_1901/`), pinned by current bytes: P/docs/PRD.md sha256 bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd, P/docs/ARCHITECTURE.md sha256 317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c, P/docs/HOST_INTEGRATION.md sha256 d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f and P/docs/EXAMINATION.md sha256 471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0 (v0.6 pinned repo `6e18505e3`, before both amendments); ScopeOfWork.md sha256 9b2379a14e2c9da4310f62e72d83a6e7506ef37f70c4a38b41d76908bca985ed (revised under SCA-V4-001, its AX-004, at `340ecf341`; v0.6 pinned the INIT contract 6fbbb580…b568); the accepted graph `_DAG/_LATEST.md` → DAG-003 (accepted 2026-09-29), cited for the admitted or held layer of register rows; P/docs/PRD.md §2.2 V4-HOST-01/02/03/04, §4.1 V4-WF-03/05, §4.5 V4-AUT-01/03/04/05, §4.7 V4-REC-03/04/05, §6, §9 OQ-02/OQ-11; P/docs/ARCHITECTURE.md §3 (V4-ARC-01/04), §4 (V4-ARC-10–14, host-agent properties), §5 V4-ARC-20, §6; P/docs/HOST_INTEGRATION.md §1, V4-HI-02/04, V4-HI-10–12, V4-HI-20–25, V4-HI-30–33, V4-HI-40–42, §8.1 closing paragraph, V4-HI-70/71; P/docs/EXAMINATION.md V4-EXM-01–03, V4-EXM-20–23; DECISION_BRIEF.html (sha256 02d38cb1…c4420e8; v0.6 mistyped the suffix as 4c420e8) d2, d3, d5; APP-V4-CLARIFICATION-20260927/DIRECTION.md; SCC-CASE-002 Case_Datasheet M1/M4 rows; Open_Issues OI-003/013/014/021; External_Dependencies DEP-001; run folder OWNER_DECISIONS.md (sha256 f3f8e5f3…cf81f2e; decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, D2 and D3), R1_RESOLUTIONS.md (sha256 2f9c7e72…e177ec4), R2_RESOLUTIONS.md (sha256 77cfb845…cdebd088), comparisons/V1-A.md (01811533…e04c09), comparisons/V1-C.md (8d46258a…4a94a6), reviews/IR1-A.md (31b3c7f8…0b648284), reviews/IR1-B.md (70e4a4f6…2846), reviews/IR1-C.md (295e96b3…a426b9); run folder at commit `f05c7e4cd`: OWNER_DECISIONS.md (sha256 a9869129…68ad2c; adds `APP-V4-FIRST-INCREMENT-20260928-DECISION-2`, D5 and D6), R3_RESOLUTIONS.md (202d52c7…afbf), R4_RESOLUTIONS.md (50a009b2…032a24), reviews/V2.md (75ba1dff…6ef); run folder at commit `8fb51f07f`: R5_RESOLUTIONS.md (254d0b93…dd6f1), reviews/V3-A.md (f25f5af1…21d87), reviews/V3-B.md (5662fbd0…954a3); run `APP-V4-SWBPIPE-INTAKE-20260928` at commit `94aa9181b`: OWNER_DECISIONS.md (sha256 a5ccab0d39bd1cab37c5556abc9bdedd5341ce76be4712706c8c9d72d623e776; decisions `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3` (host joins deferred) and `-DECISION-4` with its clarification (D4-1 phased checkpoints; D4-2 loop and panel keep V4-ARC-10; D4-3 model access)); P/docs/ARCHITECTURE.md V4-ARC-10/11/12 and `conceptual/DECISIONS.md` D-20 as cited there
- Consumed inputs:
  - **v0.8 inputs, node B5 (Wave B round 2 of run `APP-V4-DESIGN-PASS-2-20260930`; destination sections, §4 for R12-11; no version bump).** Paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/`, sha256 recomputed with `shasum -a 256` at this pass: `BRIEFS.md` fc17f9b8dcaa6b74329a94ed511f9413424a025f402d86958e240c6104a3102e (round-2 row B5); `R12_RESOLUTIONS.md` 5cf5f574bd736b3c656dc4b739b0491366710d8bd9a4b2fa7f7a085129e097f2 (R12-10, R12-11); `OWNER_DECISIONS.md` 1d63ce114a9c3736275cd16949cff0ba532b910da48ae280d4cdc440f8d51056 (DECISION-K1 K1-5, K1-6; the host-loop model interface direction); `SURVEY/S1-D.md` a3b0546a…9419 and `SURVEY/S1-A.md` 87baa03d…45f6 (LOOP item 5; PANEL items 5, 7; AS items 3, 7); `WAVE_B/B4.md` 1c6129fb…7162 (§5 element names), `WAVE_B/B9.md` 4dc8f55c…ac71, `WAVE_B/B3.md` 39c9949a…cebc, `WAVE_B/B2.md` 429db7a8…2044; `reviews/V17b.md` 0efdd6cb…00ef8 (m-1, m-2, n-1); the intake run's `OWNER_DECISIONS.md` 5fd780bf…40b2 (DECISION-5). Starting text: LOOP-v0.8 as left by node B9 (sha256 30671b5181395ca6be4cca6b26d5c410ef68420aa3b12dc360342c997f739d88). The published MCP specification, revision 2026-07-28, read-only (K1-6; G-15). Siblings edited in the same node: ACT-POLICY-v0.8, AS-v0.8, RS-v0.8, PANEL-v0.8, C-v0.8, P-v0.8, ADAPTER-v0.6 (destination sections only).
  - **v0.8 inputs (Wave B, node B9 of run `APP-V4-DESIGN-PASS-2-20260930`; design development).** Paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/`, sha256 recomputed with `shasum -a 256` at this pass: `R12_RESOLUTIONS.md` 95f3011b436b6faa3de098059e77eac836c165e0bb98a5ed94e28918a3a749a1 (R12-1…R12-3, R12-7, R12-8; binding); `BRIEFS.md` ccb4d9f036fb7ff531fffa0d309533b15cf1ebb39b0320651ed4bd5d88efc550 ("Common rules", "Wave B — design development", round-1 row B9); `OWNER_DECISIONS.md` 1dfd5bf4619b329719136b1646030e3f871fd7ffc52dbfd12265414e515aaf15 (DECISION-K1, K1-6 for the specification fetch); `SURVEY/S1-D.md` a3b0546af4131e0302520bc0dbaad8d6d5587e91d896fb8aa559e32768b19419 (LOOP §5 and §8 items 7 and 8; advice, checked against the current text). Starting text: LOOP-v0.7 as merged by PR-1 (above). The fixture basis FB-CC-1 is the published OpenAI OpenAPI specification, `openapi.yaml` of https://github.com/openai/openai-openapi (branch `main`), sha256 976053bfe228984127c1c4def7cb9fe0810252adbd8c41651812f68beb6426ad, retrieved read-only on 2026-09-30 (§4.1; K1-6). Sibling Design files are cited at their Wave A labels, because the other Wave B nodes edit them in parallel: P-v0.7 §3.1 rule 5; ACT-POLICY-v0.7 §2.7; RS-v0.7 R15; HOSTING-BOUNDARY-v0.7 §8.3; PANEL-v0.8 (same executor, node B9). Node B5 (round 2) develops the destination sections (§5.1.1, the destination request) after this node.
  - **Pins as of node A4 of this run's records (run `APP-V4-DESIGN-PASS-2-20260930`; in place, no version bump; R11-3; relabelled at RQ, V19-B n-1: later pins of the same records are in the Wave B input lines and in GUIDE's basis).** Each sha256 recomputed with `shasum -a 256` in the working tree at this pass; paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/`: `R9_RESOLUTIONS.md` sha256 a64e241519b7d158165a7ede0ffdd22eec0af15b6812b5300755f5f38abd59b8 (R9-1…R9-11; R9-2's second bullet as corrected by R10-1); `R10_RESOLUTIONS.md` sha256 ad3b6caa4a12660db77abc51b5c02ba70519ee46d55b40d21ee76eb3ca561796 (R10-1…R10-11); `R11_RESOLUTIONS.md` sha256 e7343b6663b6aeeb2dc506d3391f5b310088e7688d1b21e65d2ba1d8616b3615 (R11-1…R11-9, the repairs from review V17); `OWNER_DECISIONS.md` sha256 7458e9e81971676337a34280b4e8b29a7d04fce5fc202da5b9f5cf7ccd8f9ae5 (DECISION-K1). At node A4 these superseded for currency the earlier pins of the same records in this header and in the change-table rows, which record the bytes read at node A1 or A3.
  - **v0.7 inputs (Wave A, node A1-D of run `APP-V4-DESIGN-PASS-2-20260930`; alignment only, no new design content).** R9_RESOLUTIONS.md sha256 c3efe2ffa232dd9293202d4fc891eba4325afeb2e224fecdf8c1b4c5122a9d2c (R9-1…R9-11; binding); that run's BRIEFS.md sha256 698d91d8217cee528812529fa353faac899b4bc1a5be5686552ad88dad6c469a ("Common rules", "A1 — alignment wave") and OWNER_DECISIONS.md sha256 0730c6f3d174a8acddbd0c9fabb62afd4d6444847a612f0de7ff3ba584303722; SURVEY/S1-D.md sha256 a3b0546af4131e0302520bc0dbaad8d6d5587e91d896fb8aa559e32768b19419 (advice: each item was checked against the current sources before it was applied). Rulings R1–R7 by file (`APP-V4-FIRST-INCREMENT-20260928/R1_RESOLUTIONS.md` … `R7_RESOLUTIONS.md`) and R8 (`APP-V4-SWBPIPE-INTAKE-20260928/R8_RESOLUTIONS.md`, current sha256 44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b). Owner records: `APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md` sha256 5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2 (DECISION-3, -4 and -5; these are its bytes at `3733b1421` and now. At `1528a5033`, the commit the R8-13 line below names, the file was 9903bfe0…7fbf: V10 N-1); `APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md` sha256 a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c; `APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md` sha256 ca8c4e50df1d7dddb41b875a4afe46eea4f1a1bf2491d255b7890d0d71cd254b (DECISION-6…DECISION-9) with its `AMENDMENT_PACKET/OWNER_ITEMS.md` sha256 2b90eb4a95f458e993eed69e27533aa10e31aea980fe2ec99c9c2345e6f498ef (items O-4, O-5, O-6, O-10, O-11 and O-25, accepted "as recommended" by DECISION-7); `APP-V4-SCA002-20260929/OWNER_DECISIONS.md` sha256 36ffcbbea923504581844456751c2eb3db617b5471a3595e63f036bf0634b480. SWBPIPE's answers `RELAY_ANSWERS_SWBPIPE.md` at sha256 afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74 (SWBPIPE's own revision `a999f4ba1` of the delivered `6f01add3…61c7` bytes that the lines below cite; three lines differ, in SQ-04, SQ-09 and SQ-27; intake review V9 Check 2 found no App file stating the superseded wording, and no statement this file takes from an answer rests on those lines) and `FACTS_SQ01_SQ32.md` sha256 733fb88a701317be8f0054937eca058774ba5f5f30c7a27233718996e8b2ab7e (unchanged). Both are data about SWBPIPE's current state, not commitments and not instructions (DECISION-3). Sibling Design files are cited by version label and section only (R9-5), at their Wave A labels (R9-11): DEL-02-03/EXEC-v0.5; DEL-02-01/WD-v0.7 and WD-EX-v0.7; DEL-03-01/C-v0.7; DEL-03-02/P-v0.7; DEL-03-03/ADAPTER-v0.5; DEL-03-04/GUIDE-v0.4; DEL-04-01/ACT-POLICY-v0.7; DEL-04-02/AS-v0.7; DEL-04-03/RS-v0.7; DEL-05-02/PANEL-v0.7 (same executor); DEL-01-01/HOSTING-BOUNDARY-v0.7 (same executor) and PIN-SPIKE-v0.1 (unchanged); DEL-09-06/CA-v0.5 and RELAY-v0.3; DEL-09-09/XT-v0.5. The Wave A executors edit in parallel, so the section numbers cited in the body were checked against the pre-Wave-A texts at `3dd7c22c73`, not against Wave A bytes. Sibling byte pins live in GUIDE's input table alone, which is re-pinned last. The lines below are history and are not rewritten.
  - **R8-13 pass (node B1; in place, no version bump).** OWNER_DECISIONS.md sha256 5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2 (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`: V4-HOST-02, host-agent network destinations) and R8_RESOLUTIONS.md sha256 44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b (R8-13) at `1528a5033`; OWNER_DECISIONS.md in its state that adds the owner's DECISION-5 confirmation (committed with this pass); BRIEFS.md sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517 ("Common rules", "A-wave"). Revised in the same pass (node B1), versions unchanged: LOOP, PANEL, ACT, AS, RS, HOSTING, C, ADAPTER and GUIDE; their byte pins are in GUIDE-v0.3's input table.
  - **R8-12 closing pass (node A6; in place, no version bump).** R8_RESOLUTIONS.md sha256 d4c3423310a857af86692d17ddfdd22fa877ee20b07c46e1ee481d1cd750e7af (R8-12, items 1 and 7 applied here). Current sibling versions after R8, as committed at `7a1508452` with A6's in-place R8-12 edits (their byte pins are in GUIDE-v0.3's input table): DEL-02-03/EXEC-v0.4; DEL-02-01/WD-v0.6; DEL-02-01/WD-EX-v0.6; DEL-03-01/C-v0.6; DEL-03-02/P-v0.6; DEL-03-03/ADAPTER-v0.4; DEL-03-04/GUIDE-v0.3; DEL-04-01/ACT-POLICY-v0.6; DEL-04-02/AS-v0.6; DEL-04-03/RS-v0.6; DEL-05-02/PANEL-v0.6; DEL-01-01/HOSTING-BOUNDARY-v0.6; DEL-01-01/PIN-SPIKE-v0.1; DEL-09-06/CA-v0.4; DEL-09-09/XT-v0.4; DEL-09-06/RELAY-v0.3. SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` and `FACTS_SQ01_SQ32.md` are unchanged (data about SWBPIPE's current state, not commitments; DECISION-3).
  - **v0.6 inputs (R8 pass, node A4, at `94aa9181b`; read with `git show`).**
    - R8_RESOLUTIONS.md sha256 1770c96e62caf14322811fca82ceb77eca450d3e1be8665cdbdd5550631e8d02 (R8-1…R8-11; binding). R8-11 confirms EXEC PH-6/PH-8 and rules the Phase-1 standing of D2's checkpoint clause, WD I-7 and V4-HI-42.
    - INTAKE_MAP.md (I2) sha256 3cc182955c0f3dd70efa0f1c051870229c2ccc08f36c5cf1445f2eef0dd1ea33: rows 01.3, 02.11, 03.7, 04.4, 07.7, 08.5, 11.5, 19.4, 20.1, 21.1, 29.1, 30.1, 31.1, 32.1, X.4, X.5; Part 2 §2.1 closing paragraph and §2.2 LOOP rows; Part 3 items 2, 3, 7, 8, 9; Part 4.6, 4.11. R8 overrides I2 where they differ.
    - BRIEFS.md sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517 ("Common rules", "A-wave").
    - SWBPIPE's delivered answers `RELAY_ANSWERS_SWBPIPE.md` (DEL-09-06 `Design/`, #1047) sha256 6f01add3977761e42ac6b310faf72ba4fd5455e478605deb83fefb2e4d3a61c7: SQ-01, SQ-02, SQ-03, SQ-07, SQ-08, SQ-11, SQ-19…SQ-21, SQ-28…SQ-32, ANS §2–§4. These are data about SWBPIPE's current state, not commitments (DECISION-3).
    - Owner files revised first in this pass: DEL-02-03/EXEC-v0.4 `EXECUTION_COMPATIBILITY.md` sha256 d32be37797a3c367d342a2d13bbb8dd4279bc52934531d83b8c6ec8c6e7b76d4 (§2.1 PH-1…PH-10, §2.2 GV-1…GV-5, §4 phase notes, §4.7, §4.8, §4.14, §7.2 CH-cases) — *read*; DEL-02-01/WD-v0.6 `WORKFLOW_DECLARATION.md` sha256 fce565edfd0cee3fa4583eb292d11cce3e4121ead0cdbed31ba2fe0a52562f28 (§4.3.0 CG-1…CG-7, §4.3.1 `governed`, §5.3 SEAT-1…SEAT-3) — *read*.
    - Prior version: LOOP-v0.5 (above). DEL-05-02/PANEL-v0.6 is revised in the same pass by this executor.
  - **Prior version (v0.5 pass).** DEL-05-01/LOOP-v0.4, sha256 ffc30483…95934e, at commit `8fb51f07f`.
  - **Sibling versions current at commit `8fb51f07f`** (superseded for currency by the R8-12 line above) (`git show`; R5-9). Joins re-read are marked *read*; the others are cited for version currency:
    - DEL-02-03/EXEC-v0.2 `EXECUTION_COMPATIBILITY.md` 7f7848c0…42317af0: §3.6 (hold support, superseded in values by R5-1), §4 (hold machine), §6.2 (holding library confirmed) — *read*;
    - DEL-03-01/C-v0.4 `CATALOG_AND_READ_BASIS.md` e929d39d…659a08c: §10.1 (FXA-1…FXA-5, LIB-A1/A2, AF-1), §10.3, §10.4 — *read*;
    - DEL-03-02/P-v0.4 `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` 0d3960a2…c5e361: §3.3 carriage assurance (to be amended per R5-2) — *read*;
    - DEL-02-01/WD-v0.4 `WORKFLOW_DECLARATION.md` e492ff63…d8e88e and WD-EX-v0.4 `EXAMPLES.md` 60ce307a…128ca4 (E1d `label-with-grant`) — *read* at §4.2.4, §4.3;
    - DEL-04-01/ACT-POLICY-v0.4 d6da05ab…b03b; DEL-04-02/AS-v0.4 774728d0…f4dab; DEL-04-03/RS-v0.4 56806b64…40199 (continues ⟨run⟩ present); DEL-03-03/ADAPTER-v0.2 a2905dda…674bc; DEL-01-01/HOSTING-BOUNDARY-v0.4 201ea320…c7e58;
    - DEL-09-06/RELAY-v0.2 `RELAY_QUESTIONS_SWBPIPE.md` 48dc5a1f…41f65: §3 coverage map (this file's Q-1…Q-7 → SQ-02, SQ-01, SQ-03 (d), SQ-19 (a), SQ-21, SQ-08 (b)/SQ-07 (d), SQ-11; §5/§7/§8 items → SQ-29…SQ-32) — *read*.
  - **Sibling versions current at `c7f5513db` (R6-4; in place; superseded for currency by the R8-12 line above):** EXEC-v0.3 889e4881…ee548e; C-v0.5 a6306bd4…be7a29 (V-GR1 present); P-v0.5 a5ee4946…cd1b7 (§3.3 per R5-2 present); WD-v0.5 32acdd27…45e7c9; WD-EX-v0.5 296875c9…4702f; ACT-POLICY-v0.5 86975a90…5380e7; AS-v0.5 c49be8bb…729e1; RS-v0.5 37bc586e…c27ea; ADAPTER-v0.3 c9195851…225cff4; HOSTING-v0.5 873e76f6…b0eaa; RELAY-v0.3 89b6b9c9…68bdd7. EXEC-v0.3 §3.6 (HS-1…HS-5; R6-1) is *read*; the rest are cited for currency. R6_RESOLUTIONS.md 8703e85a…cb841 and reviews/V4-A.md 121deafc…eab1 are *read*.
  - **DEL-05-02/PANEL-v0.5.** Co-drafted by this executor (v0.5 pass).
  - **Missing inputs.** DEP-05-01-024 has an UNKNOWN supplier and is not supplied. SWBPIPE answers received 2026-09-28 (RELAY_ANSWERS_SWBPIPE.md; I2 read `64ea4e59…0689`, delivered bytes `6f01add3…61c7`, which add clarifications only, R8 delta check); no host evidence, commitment or contribution received (DEP-001). D6 (App-side holds) is closed for Phase 1 by DECISION-4 and re-opens with the governance phase (R8-2).
- Receivers (R9-6: rebuilt from the ACTIVE rows of the consumers' registers and of this register; layer per `_DAG/_LATEST.md` → DAG-003; table in §10.4): among the first-increment deliverables, DEL-02-01 (DEP-02-01-020, held), DEL-02-03 (DEP-02-03-022, held), DEL-03-04 (DEP-03-04-014, admitted), DEL-04-02 (DEP-04-02-018, held), DEL-04-03 (DEP-04-03-028, held), DEL-05-02 (DEP-05-02-010, held), DEL-09-06 (DEP-09-06-016, admitted) and DEL-09-09 (DEP-09-09-021, held); outside the first increment, DEL-08-01 (DEP-08-01-008, admitted) and DEL-10-03 (DEP-10-03-015, admitted); the DEL-09-06 relay file (§13 questions) and the external SWBPIPE owner through App-manager preparation and human file relay (SoW TBD-003; this register has no DOWNSTREAM relay row, and DEP-05-01-021 is its UPSTREAM row for DEP-001 host evidence); DEL-05-01 itself for OUT-003 when host evidence arrives. CASE-002 M1/M4 named DEL-02-01 (OUT-001, OUT-003; REQ-002, REQ-005; VER-005) and DEL-05-02 (OUT-001, OUT-003; REQ-001, REQ-005; VER-001, VER-005). The arcs N-18, N-21, N-24 and X-1 have no end in DEL-05-01

## 0. How to read this definition

- **Semantic names only.** Names such as "call correlation identity",
  "catalog edition", "entry version", "subject content identity", "grant in
  force" or "governing checkpoint constraint" are semantic element names. They
  are not wire fields or types. The following are not selected:
  - transport;
  - protocol version;
  - hash or canonicalization algorithm;
  - persistence;
  - thread or process placement;
  - shared-component placement (OI-013, OI-014, DEL-03-01 TBD-003,
    DEL-03-02 TBD-002).
- **Standing labels.**
  - **SETTLED:** accepted basis or owner decision
    `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` / `-DECISION-2`, or
    `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3` / `-DECISION-4` / `-DECISION-5`, credited
    only with what it says (R2-11). From v0.7 (R9-4): also a reading the
    owner confirmed at an amendment checkpoint, cited to its owner item.
  - **DERIVED:** follows from cited rules.
  - **INTEGRATION:** an integrator ruling (R-n / R2-n … R9-n).
  - **PROPOSED:** this file's own proposal.
  - `UNRESOLVED{…}` is never a permission, a default or a pass.
- **Phases (R8-1; R9-1; R9-3; EXEC-v0.5 §2.1–§2.2).** **Phase 1** is the
  accepted texts' "current phase" (this increment):
  checkpoints are plan guidance and nothing holds (§2.4.0). The
  **governance phase** is a later layer, per workflow that needs it, for
  checkpoints declared **governed** (WD-v0.7 §4.3.1, PROPOSED). Rules that
  hold, stop, block or re-hold a run are marked *governance phase
  (retained)*. They are relabelled, never deleted, and a Phase-1 statement
  stands beside them. Checkpoint cases give a **Phase-1 result** and a
  **governance-phase value**. The governance-phase value reads the fixture's
  checkpoints as if declared governed; no FX-PIPE-01 fixture declares the
  flag (R8-11 item 5; EXEC GV-5).
- **Identifier note (R8-7).** OI-003 in this file's Basis line is the App v4
  open issue (the extension promise). It is unrelated to SWBPIPE's OI-003.
- **SWBPIPE answers (DECISION-3).** Where this file cites an SQ answer, it is
  SWBPIPE's answer about its current state. It is not a commitment,
  delivery, adoption or host evidence, and it moves no case out of AWAITING
  INPUT unless it supplies the named input. Host joins are deferred.
- **Act names.** DEL-04-01 canonical names A1–A15 (ACT-POLICY-v0.8 §2.1;
  A15 *register workflow revision*, R12-5, is an App act that no checkpoint
  may require in this increment and that no host-loop event carries, §9). Unqualified
  "checked" means only A4. "Approval" means only A6 (R-4).
- **Fixture.** Cases use the shared fixture **FX-PIPE-01** of DEL-03-01/C-v0.4
  §10 (carried in C-v0.7 §10), and cite its identifiers (re-pointed from C-v0.2 per V2 m-13). The
  fixture contents:
  - workspace FX-W1, generation g1;
  - run R-100 between nozzles N-1/N-2;
  - supports S-1…S-4;
  - load case LC-1;
  - Engineer A;
  - workflow `supports-adjust` (origin *host*);
  - entries OP-C1…OP-C9;
  - timeline T1–T17 and Tg;
  - bases B1 (r12) and B2 (r13);
  - proposals PR-1, PR-2;
  - receipts RC-1…RC-3.

  C-v0.3 additions used here:
  - **OP-C10 Undo**, **OP-C11** (class *no policy basis*, reason *pending
    OI-021*) and **OP-C12** (host check);
  - steps **T4a** and **T16a**; the created support **S-5**;
  - settings **⟨set-1⟩** (P-03 *effective (policy default)* propose) and
    **⟨set-2⟩** (T15: P-03 direct, scope {FX-W1; {S-4}});
  - fixture assumptions **FXA-1…FXA-5** (FXA-1: exposed on all three
    surfaces; C-v0.4 renamed FA-n to FXA-n, R5-9);
  - App-side subjects LIB-A1, LIB-A2 and AF-1 (not used by host-loop
    cases);
  - named variant **V-GR1** (R5-7): the grant-change-after-arrival run.
  - named variants V-S1, V-CP1, V-NP1, V-R1, V-X1 and V-OU1.

  This file's model/endpoint rules are labeled **NW-1…NW-16** (NW-8…NW-16
  added in place by R8-13), not N-n,
  because N-1/N-2 are C's nozzles (V2 m-5).

  The v0.2 labels that collided with C (R-101, R-102, N-10…N-40, S-7…) are
  removed. The following cases keep **local labels `L-LOOP-n`**, because
  FX-PIPE-01 has no subject for them:
  - parse-level cases (MC);
  - endpoint cases (MS);
  - responsiveness cases (RS).

  None of this selects the first connected operation
  (`UNRESOLVED{OI-021}`).
- **Model-interface basis for fixtures (R12-8; v0.8).** Parse-level and
  stream fixtures are written against **FB-CC-1**, a published Chat
  Completions reference, labelled **"fixture basis, not a product
  selection"** (§4.1). Where §4.1 or §7 names a member of that reference
  (for example `finish_reason` or `index`), it is cited to locate the
  passage relied on; it is not this contract's element name, and no wire
  field is selected. Rules written from FB-CC-1 are PROPOSED. OBS-1
  observed the four points on one local OpenAI-compatible server
  (DEL-01-01 `OBS_1_0.158.0.md` §10, Part C), and §4.1's "OBS-1" column
  records it beside them; one observation at one server version is not
  qualification, so the rules stay PROPOSED (R13-6; RP-4).
- **Schemas and prototypes (R12-1…R12-3; v0.8).** `LOOP_TOOL_CALL.schema.json`
  (JSON Schema 2020-12, PROPOSED) sits beside this file with a valid and an
  invalid example. `prototype/` holds a standard-library script that
  assembles streamed tool-call fragments written from FB-CC-1 into complete
  calls and checks each record against the schema (§7.3). Node B5 adds
  `LOOP_DESTINATION_REQUEST.schema.json` (PROPOSED; a valid and an invalid
  example) for a destination request as the loop holds it (§5.3 DF-5,
  DF-6), and `prototype/destination_flow.py`, which runs the destination
  flow on a scripted native layer and control (§5.3 DF-10). Prototypes are
  not product code.
- **Who builds what.** This contract states what the App/shared side needs
  from a host loop and how that is checked. The SWBPIPE loop, native layer,
  parser, persistence, panel and treatment enforcement belong to the external
  host owner (SoW CLM-001; HI §1; ARCH §4).

## Changes from v0.7

Wave B of run `APP-V4-DESIGN-PASS-2-20260930` (node B9): design
development under R12. Rows are keyed by R12 item and by the survey item
(S1-D, LOOP §8) each change answers. Every new structure is PROPOSED unless
its row names the ruling that decides it. The network-destination items
(S1-D LOOP item 5; the refusal-recording labels and LP-5's label of R12-10)
are node B5's, round 2, and were not started by node B9; node B5's rows
carry the ID "B5" (no further version step).

| Item | Change in v0.8 | Where |
|---|---|---|
| R12-1 | Version v0.7 → v0.8. Status stays DRAFT: unsupplied, unimplemented and not accepted. Header pins the Wave B inputs | Header |
| R12-8 | **Fixture basis FB-CC-1**, labelled "fixture basis, not a product selection": the published OpenAI OpenAPI specification, with URL, retrieval date (2026-09-30), sha256 of the bytes relied on and the passages quoted by line. The four representation points (fragmented calls, termination reasons, several calls per response, "no arguments") written from it, each with the inference marked where the reference is silent and an OBS-1 column left pending. The three open representation rows of §4 are closed **as PROPOSED**; a fourth row ("no arguments") is added. DEP-05-01-024 stays open for a product | Header, §0, §1 consequence 2, §2.2, §4, §4.1, §4.2, §10.1, §10.3, UNRESOLVED |
| R12-8 (malformed-call rules) | §7 rewritten in FB-CC-1's representation: MC-1 (length: every call of the response truncated), MC-2 (no termination reason), MC-4 widened (custom item, deprecated form, no identity), MC-6 closed as PROPOSED (`{}` is "no arguments"; absent or empty text is malformed), new MC-10…MC-13. New §7.1 assembly rules R-F1…R-F5 | §7, §7.1 |
| R12-7 (T-OPEN-1 / MC-8; INTEGRATION) | MC-8: the valid calls are handled on their own and the malformed call gets its own refusal, per P-v0.7 §3.1 rule 5; PROPOSED until the fixture basis is observed. `T-OPEN-1` closed; G-3 answered on the App side; U-P9's malformed-sibling part noted as ruled | §7 MC-8, Findings G-3, UNRESOLVED |
| R12-7 (N-OPEN-1; DERIVED) | `N-OPEN-1` closed: "user-controlled local" is a class label (local or cloud) in the destination record, not a gate. **MS-11 released** with an expected result | §5.1, §5.2 MS-11, UNRESOLVED, VC-01 |
| S1-D LOOP item 8 (failure rows) | New §3.1: failure behaviour at each step of the turn sequence (F-1…F-13): undelivered input, model setting, boundary refusal, destination record not writable, model interface failure, stream end, length and filter, V-1…V-3, host route unreachable, run-record write failure, turn cancel with calls dispatched, no panel or a delivery gap, lost outcome. New event "tool call not dispatched: turn cancelled"; model interface failure evidence under FB-CC-1; E-6 event ordinal and E-7 delivery-is-not-recording | §2.3, §3, §3.1 |
| S1-D LOOP item 8 (state summary) | New §3.2: transition tables for workflow run, turn and tool call; for the destination request, the **states only** (pending, granted by scope, declined, not grantable, unanswered at end), with transitions left to node B5 | §3.2 |
| R12-1, R12-2 (data) | New schema `LOOP_TOOL_CALL.schema.json` (JSON Schema 2020-12; PROPOSED) with a valid and an invalid example; described in §7.2 | §2.2, §7.2; `LOOP_TOOL_CALL.*.json` |
| R12-3 (prototype) | `prototype/`: a standard-library assembler of streamed tool-call fragments written from FB-CC-1, 19 stream fixtures, and a schema-subset validator. Result recorded (19/19 as expected; examples valid / invalid as intended) | §7.3, §11, VC-05; `prototype/` |
| R12-1 (verification) | §11 names FB-CC-1 as the fixtures' model-interface basis and lists the stream fixtures with the prototype's result; VC-03 and VC-05 updated | §11, Verification cases |
| Findings | G-11 (what FB-CC-1 does and does not state; the two choices this file makes) and G-12 (failure rules returned for joining) added | Findings |
| B5 (S1-D LOOP item 5) | New **§5.3, the one account of the destination flow**: DF-1 tool subject (host catalog entries with an external-contact declaration, and the host's destination request entry; no second tool source, G-13); DF-2 destination identity; DF-3 the allow rule with K1-5 as ordered steps A-1…A-7; DF-4 the three check points, with **V-D** after V-3 and before dispatch; DF-5 the in-work request Q-1…Q-9; DF-6 request states and their results in TL-2's classes; DF-8 record elements; DF-9 display owners; DF-10 verification; failure rows DF-F1…DF-F12 | §5.3 |
| B5 | TL-1 names destination-reaching entries; TL-2 class 2 gains "destination not allowed" and "destination not allowed by the person"; TL-3 names the interim notice. §3 sequence shows V-D and the check at contact; F-4 and F-11 joined; §3.2 gives the destination request's transitions (B9's states kept; *not grantable* becomes a reason of *not granted*) and the turn state *awaiting destination answer*. §6 gains the V-D row and O-1's note | §2.2; §3; §3.1; §3.2; §6 |
| B5 (R12-10) | Recording a declined or refused request is labelled PROPOSED in §2.3 (declined, refused at boundary), NW-13, NW-15, MS-06, MS-19, MS-20, MS-23 and E-4, answering V17b m-1 and n-1 (n-1's DERIVED reading is not taken: R12-10 rules PROPOSED). LP-5's A8 mapping labelled DERIVED from ACT §2.1 (V17b m-2) | §2.3; §2.4.0 LP-5; §5.1.1; §5.2 |
| B5 (N-OPEN-5) | Stateless MCP evidence from the published revision 2026-07-28 (DF-7: SE-1…SE-3; limit "stateless revision declared, not verified"); `N-OPEN-5` closed as PROPOSED; N-OPEN-3 narrowed; G-15 records the source | §5.1; §5.3 DF-7; Findings; UNRESOLVED |
| B5 (R12-11) | §4: one statement that the loop reaches its model through one model-interface boundary, so a second interface (Responses API the likely one) can be added without restructuring; nothing selected | §4 |
| B5 (verification) | MS-24…MS-27 and FX-N24…N27; MS-23's result class stated (G-10 closed on it); VC-01 extended; VC-10 new. Schema `LOOP_DESTINATION_REQUEST.schema.json` with a valid and an invalid example; prototype `prototype/destination_flow.py` | §5.2; §11; Verification cases; new files |
| B5 (joins) | §9 A-5, §10.1 and §10.4 name the owners (AS §3.2 for the contacted-destinations display, G-14) | §9; §10.1; §10.4; Findings |
| **RP-4: R14-7 / R13-5** (V18-1 m-14; V18-3 m-21) | §5.3 states R13-5: the carried call waits for the person's answer; that wait is the grant being sought, not a checkpoint hold, so DECISION-4 does not bear on it; other work continues; the person may end the turn and the request closes *unanswered at end*. NW-12 and G-8 cite it | §5.1.1 NW-12; §5.3; Findings G-8 |
| **RP-4: R14-7 / R13-6** (V18-3 m-20) | §4.1's OBS-1 column takes OBS-1 Part C's four observed points (C1–C3 on LM Studio 0.4.16+2, `qwen/qwen3.5-9b`, 2026-09-30) beside FB-CC-1's reference, as observation, not qualification; rules unchanged and PROPOSED. §4.2 notes the reasoning member seen outside FB-CC-1. Prototype fixtures OBS1-C1…OBS1-C3 reproduce the observed shapes (22/22). The OBS-1 UNRESOLVED row closed; "until OBS-1" wording replaced | §0; §4; §4.1; §4.2; §7; MC-8; §7.3; §11; Findings G-3, G-11; UNRESOLVED; VC-05; `prototype/fixtures/stream_fixtures.json`, `prototype/README.md`, `prototype/assemble_tool_calls.py` (docstring) |
| **RP-4: R14-1** (V18-1 B-1) | New E-8: each checkpoint event the loop emits, with its EXEC-v0.6 §2.4.2 counterpart (CE-1…CE-19); the RS entry kind is the one RS-v0.8 §13.3 states for that CE kind. E-4 points to it | §2.3 E-4, E-8 |
| RP-4: V18-1 m-1; V18-2 m-7 (R12-10) | "prior act on this subject, not counted" → **"prior act not counted"** with its reason, in live text; history rows keep the old words | §2.3; §2.4.1; §2.4.3 C-2; §11 FX-C4b, FX-C11b, FX-C15 |
| RP-4: V18-1 m-5 | A15 named (R12-5): not a host-loop act, not checkpoint-requirable | §0; §9 |
| RP-4: V18-1 m-10 | A not-grantable or prompt-not-shown request is recorded and closed *not granted* without entering *pending*; an already-allowed request raises and records no request (returned to RS for R15's text); AS DG-15 and PANEL PS-5 follow | §3.2; §5.3 DF-5 Q-3 |
| RP-4: V18-1 m-11 | F-2's refusal recorded as `boundary_refusal` at stage *model request*; RS has no reason value for it (returned) | §3.1 F-2 |
| RP-4: V18-1 m-12 | E-6's ordinal is not carried by the run record; F-10 cites RS §14.1 W-1 and W-2 | §2.3 E-6; §3.1 F-10 |
| RP-4: V18-1 m-15 | §6.2 "Grant in force" cites AS-v0.8 §12.1, with "unconfirmed", "not received" and the destination settings version | §6.2 |
| RP-4: V18-1 M-5 (R14-3) | §7's report to the record names the loop-side refusal values RS R7 is to carry | §7 |
| RP-4: V18-2 m-6 | WD-v0.8 taken up: OP-1…OP-6 for kind (b), with what a "completed assistant message" is in a host loop (PROPOSED); `on subject absent`, `fresh act required`; tool local names and output production; FB-20…FB-22 in LP-9; message content identity for "named output" | §2.4; §2.4.0 LP-9; §2.4.1; §2.4.2; §3.2 |
| RP-4: V18-3 m-10 | The operation reference is stated as a C operation identity of the offered edition, one element with the destination request's `operationReference` | §2.2; §7.2 |
| RP-4: V18-3 m-11 | P-v0.8 taken up: *refused — identity conflict* and *not known to host* in TL-2; minting party and handles on the dispatch record; R-d follows PM-4 and SQ-P6; MC-8 cites P-v0.8 | §2.2 TL-2; §6.2; §6.3; §7 MC-8; UNRESOLVED |
| RP-4: V18-3 m-16 | The catalog edition is held as C-v0.8 §2.2 states, with CI-4; the pre-screen compares with the edition held current | §2.2; §2.3 |
| RX (residual sweep; RP-1 return §4) | E-4 and E-8 cite RS-v0.8 §13.3.1, which maps this section's events to RS kinds; E-8's interruption row names `observation_lost` / `observation_recovered` | §2.3 E-4, E-8 |
| RX (RP-4 return §3; V18-1 m-11) | F-2: RS now carries the reason *no credential*; the unconfigured case ("no model chosen") has no RS reason and no destination, and is returned | §3.1 F-2 |
| R15-1 (node B8; RX #41) | F-2 split in two: (a) unconfigured is **run not started — no model selected**, a run that does not start rather than a refusal at the network boundary, recorded on RS's run-start element (RS-v0.8 §4 R1, `run_opened` `notStarted`) with the loop's configuration state at start as evidence and no destination entry; (b) a cloud model with no credential stays `boundary_refusal`, reason *no credential*. MS-02's expected result and evidence say the same; "observed absence" is kept as its evidence wording | §3.1 F-2; §5.2 MS-02 |
| RQ (repairs from V19; in place, no version bump) | **V19-B B-1, V19-A m-7 (R15-1, F-18):** §3.2's turn-table row is split: no model selected starts no turn (F-2 (a)), no credential is *failed* (F-2 (b)). **V19-B m-4 (PROPOSED):** the workflow-run table opens a host-loop run, and writes `run_opened`, at its first turn start; a first turn with no model selected writes `run_opened` with `notStarted` and nothing more (a final *not started* state); in a live run nothing is written for such a message. F-2 (a) says the same. V19-A n-1: DF-9 labels AS's display ownership DERIVED. V19-B n-1: the node-A4 pins bullet relabelled. V19-B n-7: the prototype README says that `schema_subset.py` exits 1 by design when given an invalid example | §3.1 F-2; §3.2; §5.3 DF-9; Header; `prototype/README.md` |
| C0 (closeout; V19b m-1; in place, no version bump) | **V19b m-1 (PROPOSED):** a first turn with a cloud model and no credential opens the run live before its `boundary_refusal` (stage *model request*, reason *no credential*), so the refusal is recorded on an opened run with its workflow identity tuple; the run stays live. The §3.2 workflow-run table's first row names the case; F-2 (b) and the turn table's no-credential row point to it. Consistent with R15-1: only no model selected is *not started*. RS, PANEL RI-4 and the schemas unchanged | §3.1 F-2; §3.2 |

## Changes from v0.6

Wave A of run `APP-V4-DESIGN-PASS-2-20260930` (node A1-D): alignment to the
amended basis and the revised ScopeOfWork, under R9. It adds no new design
content, and every rule not named below is unchanged. Rows are keyed by R9
ID and by the survey item (S1-D, LOOP §8) each change answers.

| R9 ID / survey item | Change in v0.7 | Where |
|---|---|---|
| R9-11 | Version v0.6 → v0.7. Status stays DRAFT: unsupplied, unimplemented and not accepted | Header |
| R9-5; S1-D LOOP item 1 | Header re-pinned: the four basis documents by current sha256, naming SCA-V4-001 and SCA-V4-002; ScopeOfWork `9b2379a1…85ed` (v0.6 pinned the INIT contract `6fbbb580…b568`); `_DAG/_LATEST.md` → DAG-003; R9 with the run's briefs, survey and owner record; R8 at its current hash; the owner records of the two amendment runs; SWBPIPE's answers at `afb6e063…0e74` with V9's finding; siblings by Wave A label and section only. The DECISION_BRIEF suffix is corrected (`…c4420e8`). The OWNER_DECISIONS pin `5fd780bf…` is tied to its commit `3733b1421` (V10 N-1). History lines are not rewritten | Header |
| R9-1, R9-3; S1-D LOOP items 2 and 3 | Checkpoint wording moved onto the amended V4-WF-05 and V4-HI-42, using the R9-1 summary. "First half / second half" and the "flagged for the next accepted-basis update" markers are dropped from live text. LP-5 now states both clauses in force: the act is **requested**, and it is recorded only when performed. Who requests (the agent carrying out the workflow) is stated as R9-1, INTEGRATION; neither the App nor the loop issues the request in the agent's place. LP-1 points to LP-5. The "A8 request issued" event says that at a checkpoint it is the required request | Header, §0, §2.3, §2.4 lead, §2.4.0 (lead, LP-1, LP-2, LP-5), VC-08 |
| R9-2 | R8-11 item 2 restated. V4-HI-42 is no longer "guidance in Phase 1": its request clause and record clause are in force, and only the hold is phased. C-6 and FX-C9 say "no A5 is forced, and none is recorded". FX-C9 carries R9-2's *act not performed* beside this file's *not reached* (G-9, returned as an R10 candidate) | §2.4.0 LP-6, §2.4.3 C-1 and C-6, §11 FX-C9, Findings |
| R9-4; S1-D LOOP item 2 | Labels after the amendments. NW-1, NW-2 and NW-3 cite the amended V4-HOST-01, V4-ARC-11, V4-HOST-02 and V4-ARC-12; the two "Accepted-basis note" passages are removed, and NW-2's quote now ends with the accepted text's "(D-18; DEC-5)". NW-5, NW-7 and the §5.1.1 enforcement bullet become SETTLED by the accepted text. NW-6 is SETTLED for the interface's script only, and its wider list stays PROPOSED: the survey proposed relabelling all of NW-6, but V4-ARC-12 and the SoW state the script only. NW-4 and the outside-process start rule stay PROPOSED. §1 consequence 5 "record and show" becomes SETTLED (owner item O-10). LP-6 cites owner item O-25 | §1, §5.1, §5.1.1 |
| S1-D LOOP item 2 | E-4 cites the amended V4-HI-70. §5.2 cites the amended V4-EXM-23 for MS-14…MS-23 | §2.3 E-4, §5.2 |
| R9-8; S1-D LOOP item 2 | Closed with their records: the three UNRESOLVED rows on V4-HOST-02, V4-HOST-01/V4-ARC-11 and V4-WF-05 (SCA-V4-001); G-6 (SoW REQ-001 and AC-001 revised); the §10.1 "Register gap (C1)" cell (DEP-05-01-025) | §10.1, Findings, UNRESOLVED |
| R9-6; S1-D LOOP item 4 | Receivers line rebuilt from the live registers, with row IDs and DAG-003 layer. §10.3 gains each supplier's register row and a row for DEP-01-05-014. New §10.4 lists the receivers, including DEL-08-01 and DEL-10-03 outside the first increment. Where a register names a contribution a file does not yet hold, the row says so (G-10) | Header, §10.3, §10.4, Findings |
| S1-D LOOP item 4 (revised SoW) | MS-23 added, a disallowed-destination case (SoW AC-001). §11 inventory extended to FX-N14…N23 for the destination fixtures OUT-002 names. VC-01 traces to the amended texts and names "the grants in force" (SoW VER-001). VC-04 and VC-09 lose their stale clauses | §5.2, §11, Verification cases |
| S1-D LOOP item 6 (the N-OPEN-4 note only); V10 N-4 | N-OPEN-4 is stated as an open owner question, with its interim reading and the two options. MS-15 is marked as resting on the interim reading. N-OPEN-1 and N-OPEN-4 are **not** ruled, and MS-11 stays held | §5.1, §5.1.1 NW-8, §5.2 MS-15, UNRESOLVED |
| R9-5 | Body citations of sibling files carry the Wave A labels (EXEC-v0.5, WD-v0.7, C-v0.7, P-v0.7, ACT-POLICY-v0.7, AS-v0.7, RS-v0.7, PANEL-v0.7). Commit qualifiers on sibling standings are dropped | §0, §2.4, §2.4.0, §2.4.4, §10.1, §10.3, §11, UNRESOLVED, Verification cases |
| Not applied | S1-D LOOP items 5, 7, 8 and 9, and the rulings of N-OPEN-1 and N-OPEN-4 in item 6, are Wave B or the integrator's and were not started | — |
| **R10-1** (node A2, in place; R9-2's second bullet corrected) | C-6 and FX-C9: under a direct application the A5 checkpoint is **not reached**; nothing is requested by reason of an arrival that did not occur, no A5 is forced and none is recorded. FX-C9 carries one wording; G-9 and its open-item row are closed | §2.4.3 C-6; §11 FX-C9; Findings G-9; open items |
| R10-8 (node A2, in place) | §2.4.1 kind (b): the sentence stands, with a note that WD does not yet define the element designating a message as a declared output (Wave B, nodes B1 and B2) | §2.4.1 |
| R10-11 sibling citation pass (node A2, in place) | §2.4.2: "even if the kind matches (WD SB-3)" → "WD SB-2" (SB-2 is the other-content rule; SB-3 is exact binding) | §2.4.2 |
| **K1-1** (node A3, in place; owner DECISION-K1 of 2026-09-30, `APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md` sha256 35d6546346907137581be7df3bed4a8ccdb4b8bc55a261ca716040d0ad9f91bc) | Header Phase line, §2.4.0 lead and LP-5: who requests is **SETTLED by DECISION-K1 K1-1** (was INTEGRATION, put to the owner); the UNRESOLVED row on it is closed | Header; §2.4.0; UNRESOLVED |
| **K1-2** (node A3, in place) | C-2: in the current phase an earlier act counts when it is of the required kind and its content is still current, relayed with its time (EXEC SP-6); capture after arrival is kept as the governance-phase option (EXEC SP-6F). §2.3 annotations, LP-5, §2.4.1 continuation follow. FX-C4b, FX-C11b and FX-C15 recomputed; VC-08 follows; U-E4 closed | §2.3; §2.4.0 LP-5; §2.4.1; §2.4.3 C-2; §11; UNRESOLVED; Verification cases |
| **K1-3** (node A3, in place) | C-4 partial lapse: an act on the lapsed referents alone answers together with the earlier act (joint answer; EXEC §4.7 JA-1); U-03 closed and the variant released | §2.4.3 C-4; UNRESOLVED |
| **K1-5** (node A3, in place) | NW-8: a named destination is allowed on its own; a category switch means "allow everything in this category"; with the switch off only the named entries in it are allowed. `N-OPEN-4` closed (§5.1, UNRESOLVED). MS-15 and MS-18 recomputed: expected results unchanged, now resting on the settled rule | §5.1; §5.1.1 NW-8; §5.2 MS-15, MS-18; UNRESOLVED |
| A2 finding 1 (node A3, in place) | TL-1: "DEL-03-01 F-R2-2", which exists nowhere, is replaced by what the sentence relies on: C-v0.7 §4.1, the *not exposed on this surface* row (a loop or adapter relays a host-returned *not exposed*, naming the host as reporter, and never originates it) and the loop-side *not offered* paragraph after the table (R2-4). The v0.6-era history row that names F-R2-2 is left as a record | §2.2 TL-1 |
| **R11-5** (node A4, in place; V17-B M-3) | NW-5 is labelled DERIVED from V4-HOST-01 (the person chooses; no default) and from the always-off item of V4-HOST-02 and ARCH §4; SETTLED only for "no silent switch unless the person turns it on" (was SETTLED as a whole). The §5.1.1 enforcement bullet stays SETTLED by V4-ARC-12 for recording every destination contacted; "records the refusal" is marked PROPOSED, because V4-EXM-23 says a declined request is reported to the agent and no accepted text says the refusal is recorded; NW-15's "refusals are recorded too" carries the same PROPOSED mark, so the two statements agree. The rules themselves are unchanged | §5.1 NW-5; §5.1.1 (enforcement bullet, NW-15) |
| **R11-3** (node A4, in place; V17-B M-1) | Header: a new line pins this run's records at their final bytes: R9 `a64e2415…`, R10 `ad3b6caa…`, R11 `e7343b66…`, OWNER_DECISIONS `7458e9e8…`. The node A1 input line and the K1 rows keep the bytes read then | Header |

## Changes from v0.5

Keyed by R8 ID. Sources are I2 rows of INTAKE_MAP.md (`nn.k`, `X.n`, Part 2,
Part 3 items, Part 4.11). R8 overrides I2 where they differ. SETTLED here
means by DECISION-3 or DECISION-4.

| R8 ID (source) | Change in v0.6 | Where |
|---|---|---|
| **R8-1** (DECISION-4 D4-1 and clarification; SETTLED, framing INTEGRATION) | New **§2.4.0 Phase 1 in the host loop** (LP-1…LP-10). Checkpoints are plan guidance, and the host's own embedded loop **enforces no hold**: no held call, no stop, no re-hold, no hold-support value, no *unsupported* for a hold reason. Arrival and act are recorded as observation, and dispositions label the record. Acts are recorded only when performed, and reserved acts stand. *Action during hold* becomes the optional annotation "continued past ‹checkpoint› before ‹act›". A "which rules are which" list sorts §2.4.1–§2.4.4 by phase | Header, §0, §2.4, §2.4.0 |
| **R8-1** (governance phase retained) | **§2.4.4 (host-loop hold, LH-0…LH-4) recast as governance phase (retained)**, with the Phase-1 statement beside it. Also relabelled, not deleted: §2.4.1's hold/stop column, C-1's stop, C-4's re-hold, C-5's loop-followed path, C-6 (R2-12 carriage), C-8's held call, the "call held at checkpoint" and "action during hold" events, and "held at checkpoint" in TL-3, §3 and §4. The `governed` flag (WD-v0.6 §4.3.1, PROPOSED) and held actions are added to the consumed elements | §2.2 TL-3, §2.3, §2.4, §2.4.1, §2.4.3, §2.4.4, §3, §4 |
| **R8-1** (V4-WF-05) | V4-WF-05's first half is **phased to the governance layer, not withdrawn**; the second half is in force (LP-5). Flagged for the next accepted-basis update | Header, §2.4, UNRESOLVED |
| **R8-1** (cases) | **FX-C1…FX-C15 are two-part**: Phase-1 result and governance-phase value. FX-C8, FX-C11 and FX-C14: the call is dispatched, not held, and may carry the "continued past" annotation. FX-C9 Phase 1: no constraint enforced; the host's own treatment decides (R8-11 item 2) | §11 |
| **R8-2** (02.11; P2.17; Part 2 §2.1 closing paragraph) | §2.4.4 A5 row and FX-C9's governance-phase value keep AWAITING INPUT with the STD-2 annotation (SQ-02 answered: no host loop or host-held evaluation, route (iv)). The App-run row records HS-3 (c) → *not enforceable* against SWBPIPE and HS-4 no longer masking. LH-3 and the D6 row: D6 is closed for Phase 1 and re-opens with the governance phase | §2.4.3 C-6, §2.4.4, §11 FX-C9, UNRESOLVED |
| **R8-3** (Part 3 item 2; 07.7) | Staleness scope: per-item where the host supplies subject identities; otherwise the host's stated scope, never narrowed (SWBPIPE: whole model). De-duplication first unchanged | §6.3 R-c, §6.4 RN-1, FX-C12, UNRESOLVED |
| **R8-4** (Part 3 item 3; 03.7) | A whole-model identity is received as every covered subject's identity: errs toward a lapse, never misses one, never computed by the loop. SWBPIPE does not meet V4-HI-32 | §6.4 RN-2, §13 |
| **R8-5** (Part 3 items 1, 10) | SWBPIPE term mapping: `unsupported_method`/`unsupported_change` → host-reported *not exposed on this surface*, never *not permitted*; #885 `withdrawn` → item left, "cleared by the person, no decision record"; `validation_rejected` → *refused — invalid* at application; never A10/A11. Accept-and-apply is one step per batch; session undo gives no "reverses ⟨receipt⟩" | §2.2 TL-2, §6.4 RN-3, §9 A-6 |
| **R8-6** | A13 stays reserved; SWBPIPE has no enablement facility (SQ-28) | §9 A-6 |
| **R8-7** (X.4, X.5; 01.3, 08.5, 11.5, 19.4, 32.1) | Standings move to **answered**: Consumed inputs, §10.1/§10.3, §13 (with gists), DEP-001 row. OI-003 qualified as App v4 OI-003. The relayed §13 questions are kept as prepared | Header, §0, §10, §13, UNRESOLVED |
| **R8-8** (DECISION-4 D4-2; SETTLED; 20.1, 29.1; Part 3 items 7, 9) | V4-ARC-10 (D-20) is **kept**; new consequence 6. **Note for SWBPIPE**: its recorded embedded direction ("embedded Runtime", RUNTIME-ADOPT; D-58) predates D-20 and should be updated to the v4 loop when UI-SUCCESSOR resumes. That update is SWBPIPE's to make. **SEAT-1…SEAT-3 kept**; SWBPIPE's single agent panel noted as the likely counterpart. The host-loop hold is relabelled governance phase (R8-1) | §1, §2.1, §10.1, UNRESOLVED |
| **R8-9** (DECISION-4 D4-3; SETTLED; 30.1; Part 3 item 8) | Model access: a cloud model is reached by **OAuth sign-in or an API key**; **no default** between local and cloud. §5.1 states revised (local chosen; cloud signed in; cloud key supplied; cloud no credential; unconfigured), NW-1 revised, NW-3…NW-6 extended to the sign-in credential, MS-02/04/07/08 revised, MS-12 (OAuth) and MS-13 (agent asks to sign in) added. V4-HOST-01/V4-ARC-11 wording and SoW REQ-001/AC-001 flagged (G-6). **V4-HOST-02 wording unchanged, marked "owner clarification pending (R8-9)"** in the header, §1 consequence 5, NW-2, MS-01, MS-06, the N-OPEN row and a new UNRESOLVED row. SWBPIPE DEC-051 recorded as a note, not a conflict (this overrides I2 30.1's conflict framing) | Header, §1, §2.1, §2.3, §3, §5, §10.1, §11, VC-01, VC-02, Findings, UNRESOLVED |
| **R8-10** (31.1; 04.4) | Strict preflight: the agent never adds fields the host schema lacks (C-6 Phase 1; §6.4 RN-4). OI-021 stays open, with candidates recorded. T-OPEN-1 notes SQ-31 | §2.4.3 C-6, §6.4, UNRESOLVED |
| **R8-11** (items 1–3, 5) | Item 1: lapse recorded in Phase 1, re-hold governance phase (LP-7; C-4). Item 2: D2's reserved-act half binds; its "or a declared checkpoint" half, WD I-7 and V4-HI-42 are guidance in Phase 1 (LP-6; C-1; C-6). Item 3: invalid declarations are a finding only in Phase 1 (LP-9; FX-C13). Item 5: governance-phase values read as if governed (§0, §2.4.4, §11). Item 4 (EXEC SoW) is not this file's; LOOP's own SoW wording is G-6 | §2.4.0, §2.4.3, §2.4.4, §11, Findings |
| **R8-12** (items 1, 7; closing pass, node A6, in place) | Item 1 (G-7 ruled): in Phase 1 a lapse after the resume point is recorded as **"act lapsed at ‹t›"**; nothing says *waiting* and nothing is re-held; a new act is recorded when performed. Before resume the label stays "waiting — lapsed at ‹t›" (both phases); the governance-phase re-hold keeps "waiting — re-held, lapsed at ‹t› after resume". Changed in C-4's phase note, §2.4.0 and FX-C3 (ii); G-7 closed. Item 7: consumed inputs list the post-R8 sibling versions; §10.1 and §10.3 standings refreshed from the v0.5 / `c7f5513db` citations to the post-R8 versions; §0 and §11 fixture sources and §13's RELAY citation name the current carriers | Header, §0, §2.4.0, §2.4.3 C-4, §10.1, §10.3, §11, §13, FX-C3, Findings |
| V9 N-1 — in place | §2.4 "on negative decision" row: the "Absent" consequence is labelled by phase (Phase 1 per LP-8; governance phase for governed checkpoints). No rule changes |
| **R8-13** (DECISION-5; SETTLED; the act mapping INTEGRATION; in place, no version bump) | V4-HOST-02 is read as **revised by DECISION-5**. The owner's revised text is quoted at NW-2 and flagged for the next accepted-basis update. Every "owner clarification pending (R8-9)" marker is retired: header, §1 consequence 5, NW-2, the §5.1 SWBPIPE note, MS-01, MS-06, the N-OPEN row, the V4-HOST-02 UNRESOLVED row and VC-01. New **§5.1.1** (NW-8…NW-16) covers: the two-level allow list; the model service always allowed; MCP only if it follows the stateless MCP revision 2026-07-28; in-work requests scoped once / this run / always, with only the requesting call waiting; the decline outcome "destination not allowed by the person"; the always-off list; every destination recorded and shown in any model mode; the outside-process limit ("process network not observed"); and the Phase-1 / governance-phase split. Also new: §2.3 destination events and an E-4 item; the §9 A12 row and A-5 (the destination request is not a tool-permission prompt); the §10.1 networking row; **MS-14…MS-22** (allow-list hits by category and by named entry, an in-work grant for each scope, a decline, a non-stateless MCP server refused, an outside process with its network not observed, and an agent self-grant refused). MS-01 and MS-06 are re-based on the revised text. N-OPEN-2 and N-OPEN-3 are annotated, and N-OPEN-4 and N-OPEN-5 added. New G-8 and UNRESOLVED rows | Header, §0, §1, §2.3, §5.1, §5.1.1, §5.2, §9, §10.1, Findings, UNRESOLVED, VC-01 |
| R8-13 close — in place | The owner confirmed DECISION-5 (the reading of "MCP V2"; the person-only grant stands), so the "open to the owner's correction" markers are closed. The consumed-input line is corrected: OWNER_DECISIONS.md is cited in its state that adds that confirmation, not at `1528a5033` |
| V10 S-1…S-4 — in place | The wording of the DECISION-5 confirmation is made precise (the "MCP V2" reading was confirmed; the person-only grant was not objected to and stands). The revised V4-HOST-02 is "the recorder's wording confirmed by the owner". The always-off item reads "a silent switch". ACT F-22 is updated. No rule changes |

## Changes from v0.4

| Item | Change (section) |
|---|---|
| R5-1 (V3-A MAJOR-1; V3-B MAJOR-5) | §2.4.4 uses the **four ruled hold-support values**. Every checkpoint on the embedded route is **enforced by the host loop**, with residual limits stated per kind. The EXEC-v0.1 values "enforced before dispatch", "held after observation" and "enforced on the host route" (as a host-loop value) are retired. Harness-capability and App-only cases are **not enforceable** in App runs |
| R5-2 (V3-B MAJOR-1; closes G-1) | C-6: the host loop's own evaluation is **host-held**. App-assured is not available in this increment. Only host-held carriage satisfies R2-12 |
| R5-3 (V3-A m-5; Y-2) | §2.4.2 grant setting: the **declared** setting content always binds, and a declaration naming none is invalid, unconditionally. An A8 may present the content but never changes the subject. An A12 on different content satisfies nothing |
| R5-4 (V3-A m-11) | §1 item 5 relabeled. "Host content may flow to the selected model; no gating" is SETTLED by DECISION-2. "Record and show the destination" is **INTEGRATION (DECISION-2 reading)**. §2.1 notes per-turn model-setting records, and that a switch starts no new run |
| R5-5 | C-4: a lapse re-holds whatever caused it, including the person's own undo. The person's undo is never *action during hold*. An undo never re-holds an A5 arrival |
| R5-7 (V3-A MAJOR-3/5; closes G-2) | FX-C11 re-pointed to C named variant **V-GR1**; `L-LOOP-C11` dropped. T15 before the arrival does **not** count (FX-C11b). The owner-visible cost of SP-6 is recorded under U-E4 |
| R6-1 (in place; V4-A m-5) | §2.4.4: invalid or not-established declarations take **no value** (EXEC HS-1/F-22), and the check is *not established*. App-run checkpoints are classified by **held actions** (HS-3 host-operation class by SQ-02 status; HS-5 any App-side held action → *not enforceable*). R6-3: at the hold, the run stops at its next action |
| R6-4 (in place; V4-A m-1, m-6, m-7) | LOOP-local HS-0…HS-4 renamed **LH-0…LH-4** throughout. G-5 closed. EXEC-v0.3 and the other current sibling versions cited. The "R5 elements not yet in sibling text" markers are removed. §10.1/§10.3 standing text updated |
| R5-9 (V3-A m-3, m-8, m-12) | Current sibling versions cited. FA-n → **FXA-n**. Holding library marked confirmed (EXEC §6.2). The UNRESOLVED row "R4-n elements not yet in sibling text" is closed. §13 cites RELAY-v0.2 SQ numbers |

## Changes from v0.3

| Item | Change (section) |
|---|---|
| R4-2 (D6 deferred; DECISION-2) | New **§2.4.4 Hold support in host loops**, using EXEC §3.6 values:<ul><li>kind (a): *enforced before dispatch*;</li><li>kinds (b)/(c): *held after observation*, with **action during hold** recorded;</li><li>A5 constraint: *enforced on the host route*, AWAITING INPUT.</li></ul>App-side holds remain `UNRESOLVED{D6}`, and this contract claims none. It adopts neither HP-1 nor HP-2. A new "action during hold" event is added (§2.3) |
| R4-3 (EXEC §4.7; W7 F-2) | C-4 is rewritten:<ul><li>resume point = **run-resumed event** (HD-5);</li><li>a lapse after resume **re-holds the same arrival**, shown "waiting — re-held, lapsed at ‹t› after resume";</li><li>the run stops at its next action boundary, and nothing is undone;</li><li>gated outputs show *lapsed*;</li><li>the request is re-issued for the whole scope;</li><li>A5 and A12 never re-hold.</li></ul>The interim "performed + act-lapsed" display is withdrawn. A run-resumed event is added (§2.3). FX-C3 is repaired |
| R4-4 (EXEC §4.9; W7 F-4; PROPOSED) | **No resumption of an ended run.** Acts after the run ended are shown "after run end" and change nothing. Continuation is a new run carrying **continues ⟨run⟩**, which inherits nothing. An interruption is not a run end. Affected: §2.1 (continuation link), §2.4.1, the run-ended event and FX-C7b; FX-C15 added |
| R4-5 (SP-6; EXEC §4.5; W7 F-3; PROPOSED) | C-2 adds: an act counts only if captured **at or after the arrival**. Earlier acts are "prior act on this subject, not counted", and an unestablishable order gives "act order unknown". FX-C4 is repaired onto T16a (captured after the arrival at T16). FX-C4b shows T2 as a prior act not counted. FX-C11 order is made explicit. U-E4 stays open |
| R4-6 (EXEC §4.10; W7 F-5) | C-8 is rewritten: a later A12 **supersedes only when established**. A refused A12 neither counts nor supersedes, pending leaves the checkpoint *waiting*, and a lost confirmation gives *unknown*. The "Act superseded" event is restricted accordingly. FX-C11 gains refused, pending and unconfirmed variants |
| R4-7 (EXEC §4.11; W7 F-1) | C-7 cites WD §4.3.7 as **confirmed by DEL-02-03**, with MX-3 (lost decision observation → *unknown*), MX-6 (all items left → "replaced by arrival n+1") and MX-8 (application error or unknown after A5 → unchanged, annotated) |
| R4-9 (W7 F-13; INTEGRATION) | §2.4.2 grant-setting row: without an A8, the subject is the setting content named by the declaration. A declaration naming none is **invalid** for A12 |
| R4-11 (W7 F-7) | §2.3/E-4: events supply arrival and performance ordinals, run-resumed, re-held/replaced annotations, the A12 control effect, "prior act not counted", continues ⟨run⟩ and action during hold (RS format is DEL-04-03's) |
| R4-14 (W8 F-1) | C-6: the constraint is carried with a **carriage assurance**. In a host loop it is derived from the resolved declaration the loop evaluates, and is never model-supplied. The value name is per P §3.3 (R4-14); finding G-1 |
| R4-1 (D5, SETTLED by DECISION-2) | §1 consequence 5: D5 concerns the App's external channel. V4-HOST-02 still governs this loop |
| R4-21 | §2.4.4: kind (a) on a harness capability does not arise in host loops. For App runs it is not holdable pending D6 (EXEC §3.6) |
| R4-19 m-2 | The v0.2 change table's R2-17 row count is corrected (six classes with R3-1) |
| R4-19 m-5 | Model/endpoint rules renamed **NW-1…NW-7** (§5.1, VC-02) |
| R4-19 m-12 | V2 markers closed: §0, the consumed-input list, §10.1/§10.3 and the UNRESOLVED last row now read "confirmed by V2" (T15 re-pointed per R4-18) |
| R4-19 m-13; R4-18 | Fixtures re-pointed to **C-v0.3 §10**. FX-V3/V4 cite ⟨set-1⟩/⟨set-2⟩ and class P-03 with scope {FX-W1; {S-4}}. FX-UNDO cites T16a lapse at T17 |
| R4-19 (R3/R4 in Consumed inputs) | Header Basis and Consumed inputs cite R3, R4, V2, DECISION-2 and sibling hashes at `f05c7e4cd` |

## Changes from v0.2

| Item | Change (section) |
|---|---|
| R2-1; IR1A-01; IR1-B B-M1; IR1C-10 | Five class values, including **no policy basis** with a *reason* sub-element ∈ {omitted, unassigned, pending OI-021}, labeled INTEGRATION. The v0.2 "four values" statement is removed (§2.2) |
| R2-2; IR1A-08 | The reserved-operation rule is restated as *performs* A4, A5, A6, A7, A10, A12 or A13 (act state). A host-offered faithful-record operation is a relay question (§2.2, §13) |
| R2-3 | Disabling external access is a person's setting change recorded as A13 (INTEGRATION) (§9) |
| R2-4; IR1A-02, IR1A-10; IR1-B B-M5; IR1C-11 | The V-2 split replaces v0.2's "exposed" filter: loop-side **not offered** vs host-reported **not exposed on this surface** (relayed). Reserved entries are always offered. A8 is *offered*, not recorded automatically (§2.2 TL-1, TL-5; §6) |
| R2-5; IR1A-03; IR1C-06; X-2 | Name is **act-declined event**, for A4, A6, A7 and A12, with capture evidence. It is separate from the run-ended event (§2.3, C-5) |
| R2-6; IR1A-05 | Grant state **effective (policy default)** added to the carried grant states. A default opens direct only when the policy default is *direct*; none exists in the first increment (O-6) |
| R2-7 (PROPOSED) | A12 checkpoint subject = setting content. A later A12 supersedes and does not lapse. A refused A12 at a checkpoint is held for W7 (§2.4.2, C-8) |
| R2-8 | A14/R13 is not applicable in host-loop runs (§9 A-5) |
| R2-9; IR1-A X-15 | No-policy-basis wording is applied. Fixtures report such cases as **held** (O-4, FX-NP1) |
| R2-10 | An act kind outside the checkpoint list is *invalid*; an unrecognized name is *not established* (§2.4) |
| R2-11; IR1C-17 | D3 attribution corrected in A-5 and §1 (SETTLED vs DERIVED) |
| R2-12; IR1C-03; IR1-B X-9 | **Governing checkpoint constraint** {workflow run, checkpoint name, required act A5, operation} is carried on dispatch. A direct request is *not permitted*, naming the constraint. Relay question added. FX-C9 is AWAITING INPUT (C-6, §6.2, §13) |
| R2-13 | Identity-based de-duplication precedes the basis check. The per-item basis check uses the subject content identities of the item's relied-on targets (§6.3; FX-O1) |
| R2-14; IR1-B (resulting objects) | Applied outcome carries the resulting objects and their post-application subject content identities. They are used for subject binding and reached-when kind (c) (TL-4, §2.4.2) |
| R2-15 | Undo reported as applied, with **reverses ⟨receipt⟩**. Acts on content the undo changes lapse normally (§2.3; FX-UNDO) |
| R2-17; IR1C-01, IR1C-05 | The loop binds the **declared subject class**, independent of the reached-when kind. There were five subject classes at R2-17; with R3-1 there are six (count corrected per V2 m-2). The A5 declaration rule (kind (c) *proposal queued*) is consumed (§2.4.1–§2.4.2) |
| R2-18; IR1C-02 | C-7 cites **WD §4.3.7** (proposed). "Partial" is a per-item annotation. Item-left events are shown. "All accepted" is never claimed over a reduced subject |
| R2-19; IR1C-07; IR1A-09 | Lapse before resume: an **act-lapsed event** is recorded and the disposition returns to *waiting* ("waiting — lapsed at ‹t›"). *Lapsed* as a standing disposition is used only when the run has ended (C-4) |
| R2-20 (X-11, X-12, X-17, X-18); IR1C-08; IR1A-18 | <ul><li>The holding library is carried in the run association and never enters identity equality.</li><li>A reached, unperformed checkpoint stays *waiting* at run end, with a run-ended event. A post-run act does not change the ended run's disposition.</li><li>Relay questions: capture-evidence reference; per-turn supplied-guidance source and content identity (*unknown* where not recordable)</li></ul> (§2.1, §2.4.1, §13) |
| R2-21; IR1C-15; IR1-B B-M9/B-M10 | All fixtures re-pointed to C-v0.2 §10 identifiers plus OP-C10/OP-C11. Colliding labels removed. Local `L-LOOP-n` only where needed, with the reason (§0, §5.2, §7, §8, §11) |
| IR1C-14a | The declared-checkpoint element set now includes scope, purpose, actor requirement, on mixed decision and expected act evidence. The "act requested" event carries purpose and scope (§2.4, §2.3) |
| IR1C-16; IR1-B B-m7 | MC-8 adopts P §3.1 rule 5: separate proposals unless a call explicitly names the proposal it extends (§7) |
| IR1-B B-m5 | Evidence-label mapping to C's *illustrative / test-double / actual host* (§12) |
| IR1-B B-m6 | FX-D1 re-pointed to the element-7 error E-location-occupied (*refused — invalid*). The precondition "location on run" gives *unavailable* (FX-D1b) |
| IR1-B B-m11 | FX-U2 re-pointed to C T8 (OP-C2 "No current solve for LC-1 at this revision"). No UI gesture is used |
| IR1-A X-15 label | O-4's no-policy-basis rule is labeled INTEGRATION (R-3.5) |
| R3-1 (R3_RESOLUTIONS sha256 202d52c7…afbf; in place, no version bump) | Subject class **objects a named output concerns** added to §2.4.2 (INTEGRATION) |
| R3-2 (in place) | *Targets of the held call* is valid only with reached-when kind (a). Any other combination is invalid and reported, not evaluated (§2.4.2; INTEGRATION) |
| DEL-03-01 F-R2-2 check (in place) | Confirmed: the loop never labels an entry it did not offer *not exposed*. Element-9 exclusions surface loop-side only as **not offered**. Made explicit in TL-1 |

Changes from v0.1 are recorded in LOOP-v0.2 at commit `c387730fb`.

## 1. Position: host loop versus the App's Codex path

The host loop and the App's harness are different model interfaces. They
are never merged (SoW REQ-002; ARCH §§3, 4, 6; PRD §6).

| Aspect | Chirality App (not this contract) | Host embedded loop (this contract) |
|---|---|---|
| Agent runtime | Stock Codex App Server, owned by the App process (V4-ARC-01). Definition pin 0.158.0 (D4) | Minimal Chirality agent loop in the host (V4-ARC-10) |
| Model interface | Codex's published protocol. ARCH §6 records a dated assumption that local providers serve the Responses API that Codex requires. It is **unobserved** on an identified candidate (HOSTING L-2/P-11 as quoted in V1-C D-22) | OpenAI-compatible Chat Completions with tool calls (V4-ARC-10) |
| Credentials | Held by Codex (V4-ARC-04) | Held by the host native layer, outside the interface script (V4-ARC-12): an API key, or the credential of an OAuth sign-in (DECISION-4 D4-3; §5.1) |
| Tools and permission | Codex tools. Routine tool permission and sandbox modes are the user's own Codex setting (D3, SETTLED) | Host catalog entries offered as tools (V4-ARC-13). **No classifier permission mode** (D3, SETTLED). No separate routine tool-permission layer (DERIVED from D3 with V4-HI-40/41; §9 A-5) |
| Replaceability | Harness pinned and upgraded deliberately (V4-CST-03) | Loop replaceable behind the four-subject boundary in §2 (V4-ARC-14) |

Consequences:

1. A local server that serves both interfaces does not join them.
2. The App's Codex protocol types are not the host loop's types. The loop's
   detailed representation for a product waits for DEP-05-01-024. Its
   fixtures are written against FB-CC-1, a fixture basis and not a product
   selection (§4.1; R12-8).
3. PRD §6 excludes a Chirality-owned loop for the App. The minimal loop has
   **host consumers only**. SWBPIPE is the only identified one; OI-005 is
   open (§10).
4. Pi is a possible later replacement behind §2. It is not a current
   dependency (V4-ARC-14).
5. D5 (DECISION-2) concerns the **App's** external channel (DEL-03-03) only.
   - That host content read by the App's Codex may flow to the App
     conversation's selected model, cloud included, with no gating, is
     **SETTLED** by DECISION-2.
   - Recording and showing that destination is **SETTLED**: the owner
     confirmed the R5-4 reading of DECISION-2 (SCA-V4-001 OWNER_ITEMS O-10,
     accepted "as recommended", DECISION-7; R9-4).
   - §5 continues to govern this loop. Its model-access options follow
     DECISION-4 D4-3 (OAuth sign-in or API key; no default; R8-9).
     V4-HOST-02 **as amended by SCA-V4-001** (DECISION-5; R8-13; §5.1
     NW-2, §5.1.1) governs this
     loop's agent only. The App's own Codex keeps the person's Codex
     configuration, approval and sandbox choices (ARCH §4, closing sentence
     of the host-agent property; HOSTING §2).
6. **The v4 direction is kept (R8-8; DECISION-4 D4-2; SETTLED).** This
   contract and PANEL remain the App's receiving contracts for a host loop
   under V4-ARC-10, the minimal Chirality loop recorded as D-20.

**Note for SWBPIPE (R8-8; DECISION-4 D4-2).** SWBPIPE's recorded embedded
direction, a later "embedded Runtime" adoption (RUNTIME-ADOPT; successor
under D-58), **predates D-20**, and should be updated to the v4 loop when
the owner resumes UI-SUCCESSOR. That update is **SWBPIPE's to make**; this
contract changes nothing on SWBPIPE's behalf. SWBPIPE's answers record the
current state: no embedded loop or model interface exists or is selected
(SQ-20, SQ-29), and the successor embedded mechanism is a SWBPIPE owner
decision (D-58). The same note goes in the SWBPIPE handoff
(`HANDOFF_SWBPIPE_DOMAINS.md`), which is not edited here.

## 2. The replaceable boundary: four subjects

A replacement loop (Pi's libraries, another library or a rewrite) conforms
when it preserves these meanings. Its code shape does not matter.

### 2.1 Messages and run association

| Semantic element | Meaning | Consumed from |
|---|---|---|
| Conversation identity | The conversation the message belongs to. Stable while it exists | DEL-04-03 (V4-HI-70) |
| Speaker kind | One of: person; agent; tool result; supplied guidance | This contract; guidance source DEL-02-01 |
| Content | Text or structured content. For the agent: streamed increments plus a completed form | This contract |
| Completion standing | Streaming, complete, truncated, interrupted, cancelled or failed | This contract |
| Workflow identity (run association) | {kind, origin, source root, name, revision} plus derived-from (V4-WF-03). Origin class is one of project, user, bundled or host. An unadapted carried workflow keeps its origin. A host adaptation is a new host-origin identity with derived-from. Example: FX-PIPE-01 `supports-adjust`: kind *workflow*, origin *host*, ⟨fx-root⟩, revision ⟨rev-3⟩ | WD §6.1 |
| Holding library | For a carried workflow, the host library that holds the copy actually read, at the listed, selected and resolved links. **It never takes part in identity equality** | WD §6.4; R2-20; **confirmed by EXEC §6.2** (HL-1…HL-3) |
| Run identity | The workflow run, if any | DEL-04-03 |
| Continuation link | For a run started to carry on an ended run: **continues ⟨run⟩**. It inherits nothing: no arrival, disposition or act. An interruption is not a run end, and the interrupted run is resumed as the same run (EXEC §4.9 RE-3/RE-4; R4-4, PROPOSED) | DEL-04-03 RS (per R4-4/R4-11) |
| Seat role meaning | The role meaning the single seat carries for this run, or **unknown**. SEAT-1…SEAT-3 are kept (R8-8). SWBPIPE has no seat concept; the one agent panel in its UX design is the likely counterpart of the single seat (SQ-19 (d); not decided) | WD SEAT-1; P §3.3 |
| Supplied-guidance identity | Per turn, for each guidance input actually supplied to the model (workflow files, `SKILL.md`, `AGENTS.md`): its **source identity** (origin and name, or the workflow identity tuple) and its **content identity** with method designation. Where the host cannot record it, the value is **unknown** and is never inferred from configuration. Supplied ≠ adopted: whether the model took it up is not observed | R2-20; WD §6.2 *supplied* link; aligned with HOSTING §8.2 |
| Model configuration reference | The model setting in force, recorded **per turn** (§5). A person's switch of setting is a recorded change within the run; it starts no new run (aligned with R5-4). Never contains a key or a sign-in credential | DEL-04-03 "model used" |

Loop obligations:

- M-1. Preserve the order and speaker of every message.
- M-2. A partial message that ends without completion is truncated,
  interrupted, cancelled or failed, never complete.
- M-3. The conversation store is operational state. It is never the
  authority for a human act (V4-REC-03, SETTLED).
- M-4. Persistence belongs to the host owner (`UNRESOLVED{OI-013}`). Only a
  citable conversation identity is required.
- M-5. Supplied guidance is recorded as actually supplied per turn, or as
  *unknown*. It is never recorded from launch configuration. The host's
  capability to record it is a relay question (§13 Q-4).

### 2.2 Tools

| Semantic element | Meaning | Consumed from |
|---|---|---|
| Catalog edition | Identity of the adopted catalog state from which offerings were made. The loop holds it as C-v0.8 §2.2 states (*held current* · *held superseded* · *held unknown*): after a CI-4 edition-change event, or a discovery that returns another edition, the next model request offers the new edition, and calls already prepared keep their entry versions (C §2.2; SQ-C2). Nothing is offered as current from an edition held unknown (C CF-1) (v0.8, RP-4; V18-3 m-16) | C §2, §2.1 CI-4, §2.2; one name on both sides |
| Tool offering | One catalog entry with all C elements 1–9:<ol><li>identity and entry version</li><li>purpose</li><li>input schema</li><li>availability and unavailable reason, as evaluated at offering (historical; re-evaluated at request)</li><li>effects</li><li>result schema with standing</li><li>errors with effect statements</li><li>class element (§3.1 sub-elements)</li><li>per-surface exposure</li></ol> | C §3, §3.1 |
| Tool call | Call correlation identity; position in the model response; operation reference (a C operation identity of the offered edition; the entry version is the one that edition offers, O-3; v0.8, RP-4); argument text; parse state (§7). The received record after V-1 and V-2 is `LOOP_TOOL_CALL.schema.json` (PROPOSED; §7.2) | This contract. Representation: for fixtures, FB-CC-1 (§4.1, fixture basis, not a product selection); for a product, DEP-05-01-024 |
| Schema-conformant call | Parsed completely and conforming to the input schema of the named entry version in the offered edition. **Not** P's lifecycle state *validated* | This contract |
| Tool result | One of four classes (TL-2) | P §9 and C §4.1, unchanged (R-7) |

**Class element** (C §3.1, with R2-1 applied; five values):

| Value | Standing | Loop meaning |
|---|---|---|
| none | V4-HI-02 | Execute, e.g. reads. For FX-PIPE-01 reads and OP-C3, this is a fixture assumption |
| may apply within granted autonomy | V4-HI-02. For SWB model changes: DERIVED from V4-HI-41, default setting *propose* (C rule 2) | The host route resolves direct or propose from the grant state (ACT §5.3 rule 7) |
| proposal only | V4-HI-02 | Propose only; no grant widens it |
| reserved to the person | V4-HI-02. D2 lists the reserved acts (SETTLED). The operation rule is DERIVED (R2-2): an operation that **performs** A4, A5, A6, A7, A10, A12 or A13, including one that changes the host's own act state, is reserved | The agent receives *not permitted*, and an A8 request is **offered** (TL-5) |
| **no policy basis** | INTEGRATION (R2-1, from R-3.5), with *reason* ∈ {omitted, unassigned, pending OI-021} | Direct is **not permitted**. Proposing remains available but confers no permission, and any effect requires the person's A5 and host application. An A12 widening such a class is refused. Dependent production is held (REQ-004; R2-9) |

Every value carries the DEL-04-01 policy-class record reference and its
revision (C §3.1). Host adoption of any value is **not evidenced** (DEP-001).
The host names and enforces its own list (V4-HI-30). OI-002 is not a class
value (D3).

**Faithful-record operation** (R2-2). No faithful record is made through a
reserved operation. Any host-offered faithful-record operation must satisfy
all of the following:

- it does not change act state;
- it cites capture evidence;
- it never satisfies a checkpoint;
- it takes ordinary policy.

Whether any host offers one is §13 Q-5.

Loop obligations:

- TL-1. **Offering.** The loop offers every entry of the catalog edition
  that the host supplies for the embedded surface.
  - The loop never withholds an entry on its own reading of class or
    exposure (R2-4). Reserved entries are always offered.
  - If the host supplies an edition that already omits entries excluded by
    element 9 for the embedded surface, a call naming such an entry is a
    loop-side **not offered** failure (V-2). The loop never labels an entry
    it did not offer *not exposed on this surface*. That label appears only
    when the host returns it, and the loop relays it naming the host as
    reporter (C-v0.7 §4.1: the *not exposed on this surface* row, "relays
    a host-returned *not exposed*, naming the host as reporter; it never
    originates it", and the loop-side *not offered* paragraph after the
    table; R2-4).
  - An operation unavailable to the person is unavailable to the agent, with
    the same reason (V4-HI-04, SETTLED).
  - The loop never invents a tool without a catalog entry.
  - **Destination-reaching entries** (v0.8, node B5; PROPOSED). A tool
    that reaches a network destination is a host catalog entry with an
    **external-contact declaration**, and the agent's in-work request is a
    call to the host's **destination request entry** (C-v0.8 §3.4; §5.3
    DF-1). The loop reads no tool list from an MCP server or any other
    source: there is one tool source, the host's catalog (G-13).
  - Availability shown at offering is historical. It is re-evaluated at
    request on the host route (C §7).
- TL-2. **Four tool-result classes**, never collapsed:
  1. **Loop-side failure, not dispatched:** §6 V-1 parse, V-2 *not
     offered*, V-3 schema, or the optional edition pre-screen.
  2. **Host non-success outcome:** unavailable; not permitted; channel not
     enabled; **not exposed on this surface** (host-reported, relayed);
     refused — invalid; refused — stale; **refused — identity conflict**
     (P-v0.8 §9, §3.5 PM-3; v0.8, RP-4); error; application error;
     **destination not allowed** (reason; reported by the native layer at
     V-D; not dispatched) and **destination not allowed by the person** (a
     decline; reported by the host's control) (v0.8, node B5; PROPOSED;
     C-v0.8 §4.1; §5.3 DF-6).
  3. **Host outcome:** success (ran); queued; accepted; rejected; withdrawn;
     applied with receipt; and, for an observation of a proposal by its
     identity (P-v0.8 §3.5 PM-4), the recorded state or **not known to
     host** with the host's de-duplication scope (P §9: an observation
     result, never a refusal; v0.8, RP-4).
  4. **Dispatched, outcome not observed:** *outcome unknown*, reporter = the
     loop, with the last observed state.

  How SWBPIPE's reported terms map into these classes is in §6.4 (R8-5).
- TL-3. Lifecycle meaning is preserved (V4-HI-25, SETTLED).
  - The loop never rewrites queued as applied, or applied as accepted.
  - It never rewrites refused as rejected; "rejected" is only A10 (R-7).
  - "Held at checkpoint" (§2.4.1 kind a; governance phase) is a loop state.
    It is not a result class of the call. In Phase 1 no call is held.
  - The **interim notice** "waiting for the person's answer on ‹target›"
    returned for a destination request call is also a loop state, not a
    result class; the call's one result follows as its deferred outcome
    (§5.3 DF-5, DF-6; v0.8, node B5; PROPOSED).
- TL-4. **Basis and resulting objects.** Reads return their basis and
  standing (V4-HI-11/12):
  - the basis: workspace identity, generation, model revision, canonical
    content identity and method designation (C §5.1);
  - per-object **subject content identities** where the host supplies them
    (C §5.3).

  Applied outcomes carry the applied-outcome association (P §9). Per R2-14
  (P §9, confirmed by V2), they also carry the **created and changed object
  identities with their post-application subject content identities**. The
  loop passes all of these through unchanged. A later call cites the basis
  it relied on.
- TL-5. **Reserved entries and A8** (R2-4; IR1A-10).
  - An agent call to a reserved entry is dispatched like any other. The
    host route returns **not permitted**, naming the governing treatment and
    the policy record, and *offers* an A8 request.
  - The loop records no A8 automatically. An A8 exists only when the agent
    actually issues one, with the requester identified (§2.3).
  - A failed call is never turned into a request put to the person.

### 2.3 Events

Each event states its **subject**, **actor**, **reporter** and
**evidence**. An event is evidence of what the loop observed. It is never
itself a human act.

| Event meaning (semantic) | Subject | Actor / reporter | Evidence it may carry |
|---|---|---|---|
| Turn started / completed / cancelled / failed | Conversation turn | Person or agent / loop | Message references |
| Model stream progress | Agent message | Model / loop | Partial content ("streaming" only) |
| Model request refused at boundary | Model request | Host native layer | Refused destination, or "no credential" (no key and no sign-in); never credential content |
| **Destination contacted** (R8-13) | Network request of the host's agent, or of an outside process the host observes | Host native layer | Destination; category; the grant or list entry that allowed it ("model choice" for the model service); time. Never content, never credential content (NW-15) |
| **Destination request issued** (R8-13) | Destination or category | Agent (requester) / loop | A8: destination or category; purpose; scope sought; the requesting call's correlation identity (the call to the destination request entry) and the call it carries, if any (v0.8, §5.3 DF-1, DF-5). Only that call waits (NW-12) |
| **Destination grant observed** (R8-13) | Allow-list entry or in-work grant | Person (A12, subclass network-destination grant); the host's control records | Scope (once · this run · always); destination or category; time; source (allow list · in-work); capture evidence (ACT §2.7) |
| **Destination declined** (R8-13) | Requested destination | Person; the host's control records | "destination not allowed by the person", as reported to the agent; time; the requesting call. An act-declined event of kind A12 (ACT §2.3, §2.7). **Recording the decline as a destination entry is PROPOSED** (R12-10): V4-EXM-23 says the decline is reported to the agent, and no accepted text says it is recorded |
| **Destination refused at boundary** (R8-13) | Network request, or a call at V-D | Host native layer | Destination; category; stage (model request · V-D · at contact; v0.8); reason (not allowed · always-off item · not stateless MCP (2026-07-28)); the call, where there is one; nothing sent. **Recording the refusal is PROPOSED** (R11-5; R12-10): V4-ARC-12 records destinations contacted |
| **Destination request ended** (v0.8, node B5; PROPOSED) | A pending destination request | Loop, or the host's control | State *not granted* (reason: not grantable · grant refused by control · prompt not shown) or *unanswered at end* (cause: run ended · turn cancelled); the carried call not sent (§5.3 DF-5, DF-6) |
| **Outside process started** (R8-13) | MCP server or other outside process | Host | Process identity; declared destinations; sandboxed or not; the evidence limit "process network not observed" when not sandboxed (NW-16); for an MCP server, its stateless evidence SE-1…SE-3 and the limit "stateless revision declared, not verified" (v0.8; §5.3 DF-7) |
| Model interface failure | Model request | Model server or transport / loop | Termination reason. Under FB-CC-1 an error has no termination-reason value: it is a transport or service error, or a stream that ends with no termination reason (§4.1 point 2; v0.8) |
| **Tool call not dispatched: turn cancelled** (v0.8; PROPOSED) | Tool call not yet dispatched when the person cancelled the turn | Loop | Correlation identity where received; "not dispatched: turn cancelled". Calls already dispatched are not recalled (§3.1 step F-11) |
| Tool call received | Tool call | Model / loop | Correlation identity; operation reference; parse state |
| Tool call rejected: unparseable or truncated | Tool call | Loop | Parse state and reason; "not dispatched" |
| Tool call rejected: not offered | Tool call | Loop | Operation reference; catalog edition; "not dispatched" |
| Tool call rejected: schema | Tool call | Loop | Edition, entry version, schema reason; "not dispatched" |
| Offer out of date (optional edition pre-screen) | Tool call | Loop | Offered edition vs the edition held current (C-v0.8 §2.2); "not dispatched; re-offer" |
| Call held at checkpoint (**governance phase**) | Schema-conformant call | Loop | Checkpoint name; "held, not dispatched" (§2.4.1 kind a). Never emitted in Phase 1, where no call is held (§2.4.0) |
| Tool call dispatched | Schema-conformant call | Loop | Dispatch record (§6.2) |
| Host outcome | Operation or proposal | Host | P §9 outcome unchanged: item dispositions, last observed state, evaluated basis on every non-success, both bases on stale, applied-outcome association with resulting objects (R2-14), **reverses ⟨receipt⟩** for an undo (R2-15) |
| Outcome not observed | Dispatched call | Loop (observer) | Last observed state; "outcome unknown" |
| Proposal decision relayed | Proposal items | Person (A5, A10) or proposer (A11); host records | Capture evidence reference; per-item change-item content identity |
| Item left subject | Bound change item | Host | Stale refusal, A11 or host refusal, per item (from DEL-03-02 item-left events, R2-18) |
| Examination findings | A3 examination | Agent | References to rows/results; read basis examined; "agent findings" (E-5) |
| Checkpoint reached | Declared checkpoint | Loop | Checkpoint name; **arrival ordinal**; the observed event that met reached-when, with its evidenced time; bound subject referents and content identities; **purpose** and **scope** |
| Checkpoint disposition changed | Declared arrival | Loop | New disposition; **performance ordinal**; evidence reference; annotations (EXEC §4.3): per-item partial, re-held, replaced, by earlier act ‹act› at ‹t›, answered by ‹n› acts, prior act not counted, act order unknown (governance-phase option only), A12 control effect, hold not enforceable. In Phase 1 the disposition is a **record label** (EXEC PH-6; R8-11 item 1): *waiting* means "reached; act not yet recorded", never "the run is held". The *re-held* and *hold not enforceable* annotations are governance phase |
| A8 request issued | Act kind and subject | Agent (requester) | Request text; purpose and scope (at a checkpoint: the declared ones). At a declared checkpoint the agent's A8 is the request V4-WF-05 requires (R9-1; §2.4.0 LP-5) |
| Human act observed | Actual act | Person (actor); capturing surface records | Capture evidence reference with capture time; recorder; recording mode; bound content. Annotated "by earlier act ‹act› at ‹t›" where it answers a later arrival, "prior act not counted" with its reason (content no longer current · another act kind · captured before arrival (governance-phase option); RS-v0.8 L-13; R12-10), or "after run end" where applicable (R4-4, R4-5; DECISION-K1 K1-2) |
| **Act-declined event** | A4, A6, A7 or A12 not performed | Person; capturing surface records | Declined act kind; bound subject; time; capture evidence (R2-5). Not an act of that kind |
| Act lapsed | Performed act | Host reports the change | Changed content identity; time (any time after performance) |
| Act superseded | Earlier established A12 | Person (later A12), **only once the control establishes it** | Superseding act reference and settings version (R4-6). A refused or pending A12 supersedes nothing |
| Grant change observed | Autonomy grant | Person (A12), host records | Display state per R-8/R2-6; A12 evidence if person-set |
| **Run-resumed event** | Workflow run | Loop | Arrival; time; first action reference (for kind (a), the dispatch of the same held call). Resume point for "before/after resume" (EXEC HD-5; R4-3). Recorded in both phases (EXEC §4.2) |
| **Continued past ‹checkpoint› before ‹act›** (Phase 1) | Run action | Loop | Optional plain annotation on a run action observed after an arrival and before the act that answers it, with its reference (R8-1; EXEC PH-7). Information only: never a defect, refusal, finding or violation marker |
| **Action during hold** (**governance phase**, retained) | Run action | Loop | A dispatch or output observed after an arrival event of a governed checkpoint but before the loop acted on it (e.g. a call already in flight), with its reference. Recorded, never hidden (EXEC HD-4, MA-3; R4-2). Not used in Phase 1, where the annotation above replaces it |
| Run interrupted / observation recovered | Workflow run | Loop | Loss and recovery of observation, each with observation time and the source's evidenced time. Not a run end (EXEC RE-4, §4.12) |
| **Run ended** | Workflow run | Loop | Cause: model ended, person stopped, declared negative path, failure, or "interruption not recovered". Every declared checkpoint's arrivals and dispositions: *not reached*, *waiting*, *unknown*, *performed*, *resolved negatively*, or *lapsed* (only as a standing disposition after end, R2-19). Unknown outcomes stay unknown. **Final**: an ended run is never resumed (R4-4) |

Loop obligations:

- E-1. Emit only what was observed or done. An absent observation stays
  absent (SoW AC-009).
- E-2. Human-act, act-declined and proposal-decision events relay
  host-captured records. They never come from model text, success, queue
  position or a receipt (V4-HI-25/31, V4-AUT-03, SETTLED).
- E-3. References are carried, not copies (V4-HI-71, SETTLED).
- E-4. The events cover the run-record inventory (V4-HI-70), plus the hold
  elements of R4-11:
  - workflow identity and holding library;
  - conversation;
  - autonomy settings (grant events plus the grant in force per dispatch);
  - operations and outcomes;
  - receipt references;
  - human acts and act-declined events;
  - model used;
  - supplied guidance;
  - arrival and performance ordinals;
  - run-resumed events;
  - replaced annotations, and re-held annotations (governance phase);
  - the A12 control effect;
  - "by earlier act ‹act› at ‹t›", "answered by ‹n› acts" and "prior act not counted";
  - in Phase 1, the optional "continued past ‹checkpoint› before ‹act›"
    annotation; in the governance phase, action during hold;
  - destinations contacted, destination grants and declines, and outside
    processes with their declared destinations (V4-HI-70 as amended: "for
    a host's agent, each network destination contacted"; R8-13; RS R15);
    destination requests and how each ended, and boundary refusals (v0.8,
    §5.3 DF-8; the recording of declines and refusals PROPOSED, R12-10);
  - continues ⟨run⟩.

  The field mapping is DEL-04-03's (RS-v0.8 §13.3; §13.3.1 maps this
  section's events to RS kinds; R14-1). E-8 lists the checkpoint events
  with their counterparts.
- E-5. Findings reach the panel in one of two ways:
  - (a) as agent message content with references;
  - (b) as a host outcome, if the host holds findings (`UNRESOLVED{C U-C5}`).

  An examination (A3, e.g. OP-C3 at T4) never changes domain tables. Its
  result is never labeled "checked" (R-4).
- E-6. **Event ordinal** (v0.8; PROPOSED; S1-D LOOP item 8). Each event
  carries an ordinal, contiguous within the conversation and never reused,
  so that a receiver can see a gap and ask for the events from a given
  ordinal (PANEL-v0.8 FD-3). The ordinal orders delivery; it is not an
  evidenced time, and it does not replace the arrival and performance
  ordinals of §2.4. It is the loop's, kept with the conversation's events
  for replay (operational state, M-3); the run record does not carry it,
  and the record's own order is RS's (`seq`, RS-v0.8 §13.2, §14.1 W-1)
  (v0.8, RP-4; V18-1 m-12).
- E-7. **Delivery is not recording** (v0.8; PROPOSED). An event that cannot
  be delivered to the panel is still written to the run record, and the
  failure changes nothing in the run. With no panel attached the loop
  continues; nothing is recorded as shown to the person, and nothing the
  person must answer through the host's control is taken as answered
  (§3.1 steps F-9, F-10).
- E-8. **Checkpoint events and the record (R14-1, INTEGRATION; v0.8, RP-4).**
  RS-v0.8 is the one record container. EXEC-v0.6 §2.4.2 defines the bodies
  of the checkpoint entry kinds CE-1…CE-19, and **RS-v0.8 §13.3 states the
  RS entry kind that carries each** (the mapping is RS's; R14-1). A host
  loop records the same checkpoint facts as an App run, so each checkpoint
  event the loop emits names its CE counterpart below, and its RS entry
  kind is the one RS §13.3 gives that CE kind (RS §13.3.1 states the same
  mapping from this section's events). The loop defines no
  checkpoint entry kind of its own, and the spellings are RS's (disposition
  words spaced as WD §4.3.4; performance ordinal from 1; annotations as
  RS's structured objects; R14-1).

  | Event the loop emits (§2.3; §3.2) | EXEC-v0.6 §2.4.2 counterpart | Note |
  |---|---|---|
  | Workflow run started, with its declared checkpoints listed as guidance (§3.2 workflow run) | CE-1 | Evaluability on the embedded surface: every reached-when kind is evaluated against the loop's own observations (§2.4.1) |
  | Declaration finding (LP-9) | CE-2 | With the FB code |
  | Checkpoint reached | CE-3 | Event source: the loop's observation (a dispatch, a host outcome, a completed assistant message) with its evidenced time |
  | A8 request issued, at a declared checkpoint | CE-4 | Form: the host-loop A8 event, associated with the current arrival (RS R16 `act_request`) |
  | Human act observed, answering the arrival or "by earlier act ‹act› at ‹t›"; "answered by ‹n› acts" | CE-5 | Relation *after arrival* or *earlier act*; each act with its referents (K1-3) |
  | Human act observed, "prior act not counted" with its reason | CE-6 | |
  | Proposal decision relayed; item left subject | CE-7 | Per item: A5, A10, left (with its cause), unknown |
  | Act-declined event | CE-8 | |
  | Grant change observed; act superseded (the A12 control relation) | CE-9 | |
  | Act lapsed | CE-10 | Before resume · after resume · after run end |
  | Run-resumed event | CE-11 | |
  | Continued past ‹checkpoint› before ‹act› | CE-12 | Optional; the loop is its one writer in a host loop |
  | Run interrupted; observation recovered | CE-13; CE-14 | Recorded as `observation_lost` / `observation_recovered` (RS §13.3.1) |
  | Checkpoint disposition changed to "replaced by arrival n+1" | CE-15 | |
  | Human act observed, "after run end" | CE-16 | |
  | Run ended | CE-17 | `by`: the person for cause "person stopped"; otherwise the loop as observer, with the cause (model ended · declared negative path · failure · interruption not recovered) |
  | Checkpoint disposition changed | CE-18 | |
  | Run record write failure (§3.1 F-10) | CE-19 | RS's "record write failed" limit, written in RS's order (R14-1) |
  | Call held at checkpoint; action during hold (governance phase) | — | Never emitted in Phase 1 (§2.4.0) |

  The destination events map to RS R15 (§5.3 DF-8). The operation events
  (tool call dispatched, host outcome, outcome not observed, the loop-side
  rejections of §7) map to RS R7.

### 2.4 Checkpoints

A checkpoint is a declared point where the method expects a specified human
act (WD §4.3). V4-WF-05 and V4-HI-42, as amended by SCA-V4-001 (SETTLED),
say (R9-1 summary): when a run reaches a declared checkpoint, the required
human act is requested, and it is recorded as done only when the person
performs it, whatever the autonomy setting. Holding the run at the
checkpoint until the act is performed is phased to the governance layer: in
the current phase a checkpoint is plan guidance that the person and the
agents manage, and neither the App nor a host's embedded loop enforces a
hold, blocks a run, or reports a workflow unsupported because a hold cannot
be enforced. The reserved acts (V4-HI-30) still bind.

- **In force in every phase:** the act is requested; it is recorded as done
  only when the person performs it; the reserved acts bind.
- **Phased to the governance layer:** holding the run until the act.

Who requests in the current phase is §2.4.0 LP-5 (R9-1). The loop consumes
the full WD §4.3.1 element set (IR1C-14a). From WD-v0.8 (v0.8, RP-4): a
required tool is referred to by its **tool local name** (WD §4.2.2), and an
output names its **production** (WD §4.4: a host outcome, a file path, or a
message's designating line, OP-1…OP-6), which reached-when kind (b) reads
(§2.4.1).

| Declared element (WD §4.3.1) | Loop use |
|---|---|
| checkpoint name | Identity across interruption and replay |
| required act kind | One of A4, A5, A6, A7, A12. A recognized kind outside the list makes the checkpoint **invalid**. An unrecognized name is **not established** (R2-10). The loop evaluates neither case and reports it |
| reached-when | Kind (a), (b) or (c) (§2.4.1). Arrival only |
| subject (class) | Bound independently of reached-when (§2.4.2; R2-17) |
| scope | Extent of the subject covered (items, rows). Carried on the act request |
| purpose | Carried on the act request, and bound with the act (V4-REC-05) |
| actor requirement | "The person"; for A7, "the accountable professional". A class, not an identity |
| on negative decision | Path after A10 or an act-declined event. Absent: in Phase 1 the agent follows the plan it worked out with the person (LP-8); in the governance phase (governed checkpoints) the run stops at the checkpoint |
| on mixed decision (A5, optional) | Per WD §4.3.7 |
| expected act evidence | The act record and its capturing surface |
| held actions | Phase 1: guidance on what the agent's plan should not do before the act. Governance phase: what the loop holds (§2.4.4) |
| **governed** (optional; PROPOSED, WD-v0.7 §4.3.1) | Shown with the checkpoint. Phase 1: honoured only as guidance (EXEC PH-9). Governance phase: the loop holds governed checkpoints per §2.4.4. An unrecognized value is preserved and reported (WD FB-19) |
| **on subject absent** (optional; PROPOSED, WD-v0.8 §4.3.1; v0.8, RP-4) | Phase 1: guidance for the agent's plan. It changes no disposition: the arrival stays *waiting* "subject absent" until an act-declined event or the run's end (EXEC §4.7; CH-24). Governance phase: as EXEC defines it |
| **fresh act required** (optional; PROPOSED, WD-v0.8 §4.3.1 FA-1…FA-5; v0.8, RP-4) | Shown with the checkpoint. Phase 1: guidance only; the record applies SP-6 (C-2; FA-2). Governance phase, declared with `governed`: EXEC SP-6F applies to its arrivals (FA-1). Without `governed` it has no effect in either phase (FA-3) |

Dispositions (shared): **waiting · performed · resolved negatively · lapsed ·
not reached · unknown**. Everything else is an annotation (EXEC §4.3). In
Phase 1 they label the record (§2.4.0 LP-3).

The hold-machine semantics are **EXEC-v0.5 §4** (DEL-02-03, PROPOSED (W7)).
In Phase 1 only its **recording** content applies (EXEC §2.1, closing
paragraph); its **hold** content is governance phase (EXEC §2.2 GV-1). In
host loops the loop realizes whichever applies (EXEC §2). Construction and
placement are external (`UNRESOLVED{OI-013}`), and sharing is
`UNRESOLVED{OI-014}`. Arrivals are identified by {run, checkpoint, **arrival
ordinal**}. A checkpoint may arrive more than once (WD RW-4), and each
arrival binds its own referents.

#### 2.4.0 Phase 1 in the host loop (R8-1, R8-8, R8-11; DECISION-4 D4-1 and clarification) — normative

The phasing and its application to a host's own embedded loop are SETTLED by
DECISION-4 D4-1 and its clarification ("the principle should also apply to
a host's own embedded loop"), and are now stated by V4-WF-05 and V4-HI-42 as
amended by SCA-V4-001. The framing is INTEGRATION (R8-1); who requests the
act is SETTLED by DECISION-K1 K1-1 (R9-1). These rules
are this contract's statement of EXEC-v0.5 §2.1 (PH-1…PH-10) and WD-v0.7
§4.3.0 (CG-1…CG-7) for host loops.

| # | Rule (Phase 1, this increment) |
|---|---|
| **LP-1 Guidance** | A declared checkpoint is **plan guidance** (PH-1; CG-1; V4-WF-05 as amended). The person and the agent work out the plan around it, and the agent manages any pause, hold point or gate itself, for example by not continuing until the person has acted, where its plan says so. The request for the act is LP-5 |
| **LP-2 No host-loop hold** | The host's embedded loop **enforces no hold** (PH-2). It holds no call, withholds no dispatch, does not stop acting on a run at an arrival, and never re-holds. No hold is claimed. No hold-support value is assigned, and no workflow is *unsupported* for a hold reason (PH-3; V4-WF-05 as amended). The required-tool check (V4-WF-04) is unchanged |
| **LP-3 Observation** | The loop still evaluates reached-when **only against observed events** (§2.4.1) and records "checkpoint reached" with the arrival ordinal, the bound subject by its declared subject class (§2.4.2), purpose and scope. It also records act-declined, act-lapsed, run-resumed, run-ended and observation lost or recovered. Recording is observation, not enforcement (PH-6). The shared dispositions label the record: *waiting* means "reached; act not yet recorded", never "the run is held" (PH-6; confirmed INTEGRATION by R8-11 item 1) |
| **LP-4 Continued past** | A run action observed after an arrival and before the act that answers it may carry the optional plain annotation **"continued past ‹checkpoint› before ‹act›"** (PH-7). It is information, never a defect, refusal or finding |
| **LP-5 Act requested; recorded only when performed** | In force in every phase (V4-WF-05 as amended: "the required human act is requested, and the run does not record the act as done until the person performs it"; V4-HI-42; PH-4). **Requested (R9-1; SETTLED by DECISION-K1 K1-1, the owner's decision of 2026-09-30 confirming R9-1's reading of DECISION-4's text).** The agent carrying out the workflow asks the person for the act when its work reaches the checkpoint, because the declared checkpoint is part of the plan it was given. Its request is an A8 (§2.3 "A8 request issued", with the declared purpose and scope; TL-5; **DERIVED** from ACT §2.1, as ACT AP-12 labels the same mapping: DECISION-K1 K1-1 decides who asks, not the act kind; R12-10, V17b m-2). The product's part is: to give the agent the declared checkpoint with the workflow; to offer the person the means to perform the act (the host act facility, ACT §4.5; PANEL §3.5); and to record what it observes: the checkpoint's identity and arrival (LP-3), the request where it can be identified, and the act only when the person performs it. Neither the App nor the host's embedded loop issues the request in the agent's place, pauses the run, or otherwise reacts to the arrival (LP-2). Where no request is observed the record shows none (E-1). **Recorded only when performed.** C-2 applies unchanged: an act is recorded as performed only on capturing-surface evidence of the specified kind, bound to the current content; an act captured before the arrival counts on that current content and is cited with its time (SP-6; DECISION-K1 K1-2). Model text, success, a queued proposal, a receipt, findings, an A8 request or an agent-authored record is never the act |
| **LP-6 Reserved acts stand** | DECISION-1 D2 is unchanged (PH-5; R8-1). A4, A5 (where a proposal is required), A6, A7, A12 and enabling external access (A13) stay the person's, and the host enforces its own list through its operations (V4-HI-30). TL-5 applies: a reserved entry returns *not permitted* with an A8 offered. **R8-11 item 2 as restated by R9-2 (DERIVED; the owner confirmed the R8-11 reading of D2, SCA-V4-001 OWNER_ITEMS O-25, DECISION-7):** D2's "no autonomy grant widens past a reserved act" binds, enforced by the host. For a declared checkpoint, V4-HI-42's request clause and record clause are in force whatever the autonomy setting; whether the run goes on before the act is for the person and the agents in the current phase, and the host's own treatment of its operations decides what the host does. So no governing checkpoint constraint is carried as enforcement in Phase 1 (C-6) |
| **LP-7 Lapse recorded; nothing re-holds** | A performed act whose bound content changes is still recorded as lapsed: an act-lapsed event against the affected referents, with gated outputs showing their standing lapsed (V4-REC-05; R2-19 recording). The run is not re-held, and the agent re-requests the act as its plan requires (PH-8; confirmed INTEGRATION by R8-11 item 1). Re-hold (C-4 after resume) is governance phase |
| **LP-8 Negative decisions and paths** | A10 or an act-declined event is recorded as *resolved negatively* (C-5). The declared *on negative decision* or *on mixed decision* path is guidance the agent follows in its plan; the loop does not stop the run for it (EXEC §2.1 keeps §4.8 as recorded) |
| **LP-9 Invalid declarations** | An invalid or not-established checkpoint declaration is reported as a **declaration finding** (invalid, with its FB code, WD-v0.8 §3.7's FB-20…FB-22 included; or not established). No arrival is created, no hold-support value is given, and it does not make the workflow *not established* (R8-11 item 3; EXEC §4.14) |
| **LP-10 `governed` in Phase 1** | A checkpoint declared **governed** is shown with its flag and treated only as guidance: LP-1…LP-9 apply unchanged (PH-9) |

**Which rules are which.** In Phase 1 the following apply as recording and
binding rules:

- §2.4.1: evaluation against observed events only, never-met, run-end,
  continuation and interruption rules;
- §2.4.2 in full;
- §2.4.3: C-2, C-3, C-4's recording (the act-lapsed event, the "waiting —
  lapsed at ‹t›" label before resume and the "act lapsed at ‹t›" label after
  it (R8-12 item 1), gated outputs, which acts lapse), C-5's recording,
  C-7 (MX rules as record labels) and C-8's control relations.

The following are **governance phase (retained)**:

- §2.4.1's "Governance phase" column (hold the call; stop acting);
- C-1's stop;
- C-4's re-hold;
- C-5's loop-followed path;
- C-6 (the governing checkpoint constraint, R2-12 carriage assurance);
- C-8's held call (AR-2);
- §2.4.4 in full (the host-loop hold, LH-0…LH-4).

SWBPIPE has **no host loop** (SQ-20). No host-loop evidence of either phase
can exist for it now, and host joins are deferred (DECISION-3).

#### 2.4.1 Reached-when evaluation by the loop

The loop evaluates each declared checkpoint's reached-when **only against
events it observed** (E-1; WD RW-1). It never uses model text, prose stage or
the model's claims.

| Kind | Evaluated when | Phase 1 (R8-1): on match | Governance phase (retained): on match |
|---|---|---|---|
| (a) before dispatch of a named required-tool reference | After a call to that operation passes V-1 to V-3, and before dispatch | Record the arrival, then dispatch the call as usual. Nothing is held. If the act is not yet recorded, the dispatch may carry "continued past ‹checkpoint› before ‹act›" (LP-4). "The held call" names the call whose dispatch met reached-when (subject class *targets of the held call*) | Hold the schema-conformant call undispatched. Emit "call held at checkpoint". Return to the model a tool result saying the run is held (a loop state, not a failure). After *performed*, dispatch the **same** held call unchanged. A different call is a new call, and the act does not carry to it |
| (b) observed production of a named declared output | An observed event establishes the output: a host outcome producing it, or a completed agent message the declaration designates as that output. A model statement that it exists does not count. *Designation (WD-v0.8 §4.4 OP-1…OP-6; v0.8, RP-4):* a message is the output when its first non-empty line, trimmed, equals the declared designating line. OP-2's "completed assistant message" in a host loop is (PROPOSED) the assistant content of a model response that terminated *stop* or *tool calls* (complete under FB-CC-1, §4.1 point 2), whether or not that response also carried tool calls; content of a response cut off (*length*), filtered or interrupted never counts, and whitespace-only content has no non-empty line (OBS-1 C1 observed such content beside a call, §4.1). Each such message is a production, and the checkpoint arrives each time (OP-4; WD RW-4) | Record the arrival. Nothing is stopped | Stop acting on the run |
| (c) observed host outcome of a named operation, e.g. *proposal queued* | The host outcome for that operation matches the named outcome | Record the arrival. Nothing is stopped | Stop acting on the run |

On a match the loop emits "checkpoint reached" with purpose, scope and the
bound subject, and labels the arrival *waiting*. In Phase 1 nothing is
stopped (LP-2). In the governance phase the loop stops acting on the run
(C-1).

**Never met, run end, continuation and later acts** (WD §4.3.4; R2-5,
R2-20; EXEC §4.9; R4-4, PROPOSED):

- If the run ends without the condition having been observed, the checkpoint
  is **not reached**.
- If the deciding observation was lost (for example, kind (c) with *outcome
  unknown* for the named operation), the arrival is **unknown**.
- If the checkpoint was reached but the act was never performed, or was
  re-held (RH-7; governance phase), it stays **waiting** at run end. The
  run-ended event lists it. It is never performed or satisfied.
- **An ended run is never resumed.** Its dispositions are final, except for
  the R2-19 change from *performed* to *lapsed* on a later lapse.
- A person's act performed **after** the run ended is recorded as a human
  act. It is relayed against the ended arrival's bound subject, marked
  **"after run end"**, and changes no disposition.
- **Continuation is a new run** carrying **continues ⟨run⟩**. It inherits
  no arrival, disposition or act. Its checkpoints start *not reached*.
  Its arrivals bind only referents observed in the continuation. An earlier
  act (including a post-end act) counts at its arrival when it is of the
  required kind and its content is still current, and is cited with its
  time (SP-6; DECISION-K1 K1-2); under the governance-phase option (EXEC
  SP-6F) it is "prior act not counted" (reason: captured before arrival
  (governance-phase option)).
- **An interruption is not a run end** (EXEC RE-4). The run is resumed as
  the same run. Before acting, the loop re-observes and records each
  recovered observation as a new event; nothing is back-filled (EXEC
  RP-1…RP-5). Governance phase: a held kind (a) call is dispatched unchanged
  from the record. Phase 1: no call is held, and observation of any
  dispatched call is sought before any resubmission (EXEC CH-21).
  If recovery is impossible, a run-ended event with cause "interruption not
  recovered" is recorded.
- Stopping a run is a **run-ended event**. It is not an act-declined event
  (R2-5).

#### 2.4.2 Subject binding: the declared subject class (R2-17)

The loop binds the **declared subject class**. It never infers the class
from the reached-when kind (IR1C-01). The reached-when event provides arrival
and the referents the class names.

| Declared subject class (R2-17) | Bound referents and content identity |
|---|---|
| Change items of a named proposal | Proposal and item identities, and each item's **change-item content identity** (P §3.1) |
| Named output | The output and its content identity (host-supplied; file content identity for App files; for a message output, the content identity of the completed message text, WD-v0.8 §4.4 OP-3) |
| Objects changed by a named outcome | The created and changed object identities in that outcome's applied-outcome association, with their **post-application subject content identities** (R2-14; C §5.3) |
| **Objects a named output concerns** (R3-1, INTEGRATION) | The objects identified in a named read or examination output (e.g. the rows OP-C3 examined at T4), bound through their **subject content identities as read** in that output's basis (C §5.3). Lets a review-only workflow require A4 on the rows it examined |
| Targets of the held call (**valid only with reached-when kind (a)**, R3-2, INTEGRATION) | The targets the held call names, bound through the **subject content identities of the relied-on read** that the call cites (C §5.3/§5.4). Argument text is never used. Declared with any other reached-when kind, the checkpoint is invalid, and the loop reports it without evaluating it |
| Grant setting (A12) | The **declared setting content**: classes, grant values and scope, as the checkpoint's declaration names it. It **always binds**. A declaration that names no setting content is **invalid**, unconditionally, and is reported before the run (R5-3; EXEC §4.14). An A8 may present that content but never changes the subject. An A12 made on different content is recorded and satisfies nothing at this checkpoint. A run-dependent scope is declared as a binding rule resolved at arrival (e.g. "targets of the held call"), never chosen by an A8 (R2-7, PROPOSED; R5-3) |

- **A5 declaration rule** (R2-17): an A5 checkpoint uses reached-when kind
  (c) *proposal queued* for the operation whose result it concerns. Its
  subject is that proposal's change items. Any other A5 combination is
  invalid in the declaration (DEL-02-01), and the loop reports it.
- An act on other content, another proposal or another row set does not
  satisfy the checkpoint, even if the kind matches (WD SB-2).

#### 2.4.3 Loop obligations

Each obligation is marked by phase where the phases differ (§2.4.0).

- C-1. **Governance phase (retained).** At a reached governed checkpoint
  the loop stops acting on the run. No grant widens past a reserved act or
  a declared checkpoint (D2, SETTLED; V4-HI-42). **Phase 1 (R8-11 item 2 as
  restated by R9-2, DERIVED):** the loop does not stop. D2's "no autonomy
  grant widens past a reserved act" binds, and the host enforces it through
  its operations. For a declared checkpoint, V4-HI-42's request clause and
  record clause are in force whatever the autonomy setting; whether the run
  goes on before the act is for the person and the agents (LP-5, LP-6).
- C-2. (Both phases.) **Performed** requires capturing-surface evidence of the specified
  act kind, by a qualifying actor, bound to the current content of every
  bound referent in scope. The capturing surface is the host act facility
  for host content (ACT §4.5).
  - A faithful record (A9) citing that evidence is a valid record shape.
    Alone it never satisfies the checkpoint.
  - None of these satisfies it: model text, success, findings, an A8
    request, an agent-authored record, or another act kind.
  - Without a capture-evidence reference from the host (§13 Q-2), no
    host-content checkpoint can become *performed*. It stays *waiting*, or
    *unknown* after interruption.
  - **Earlier acts** (SP-6; EXEC §4.5; SETTLED by DECISION-K1 K1-2; U-E4
    closed). In the current phase an act captured before the arrival counts
    toward it when it is of the required kind and the content it was made
    on is still current. The loop relays it as answering the arrival, citing
    the earlier act and its time.
    - An earlier act whose content is no longer current, or whose kind
      differs, is relayed as **"prior act not counted"**, with its reason
      (content no longer current · another act kind; RS-v0.8 L-13).
    - SP-6 adds no ordering between act kinds (C-3 stands).
    - **Governance-phase option (EXEC SP-6F; retained; PROPOSED; formerly
      this rule, R4-5).** A workflow that takes up the governance phase may
      require a fresh act, counted only if captured at or after the
      arrival's event, ordered by a request relation where the capturing
      surface records one, otherwise by evidenced times. Under it any
      earlier act is relayed "prior act not counted" (reason: captured
      before arrival (governance-phase option)), and
      where the order cannot be established: **"act order unknown"**, and
      the act does not count.
- C-3. There is no synthetic ordering. For example, A5 is not required
  before A4 (WD I-3).
- C-4. **Lapse and re-hold** (R2-19; EXEC §4.7; R4-3, PROPOSED (W7)).
  - **Phase (R8-1; R8-11 item 1).** In Phase 1 the act-lapsed event is
    recorded and presented. Gated outputs show their standing lapsed for
    the affected referents. Before the resume point the arrival's label
    returns to *waiting — lapsed at ‹t›*. After it, the lapse is recorded as
    **"act lapsed at ‹t›"**: nothing says *waiting*, and a new act is
    recorded when performed (R8-12 item 1).
    Nothing re-holds, and the agent re-requests the act as its plan
    requires (LP-7). The "After resume … re-held" bullet with its
    sub-bullets (except the gated-output rule, which applies in both
    phases), the "If the run ends while re-held" bullet, and the sentence
    "A lapse re-holds whatever caused it" are **governance phase
    (retained)**, as is "A5 and A12 never re-hold". The rules on which
    acts lapse (A12 is superseded, not lapsed; applying an accepted item
    does not lapse its A5; the person's undo lapses acts normally and is
    never *action during hold*, nor in Phase 1 annotated "continued past")
    apply in both phases as recording rules (EXEC §4.7 phase note).
  - Whenever the host reports that bound content changed after the act, the
    loop records an **act-lapsed event**.
  - The **resume point** is the first run action after the arrival became
    *performed*, or *resolved negatively* with a proceed or return path. It
    is recorded as a **run-resumed event** (EXEC HD-5). For kind (a), the
    first action is the dispatch of the same held call.
  - **Before resume**, the disposition returns to **waiting**, shown as
    "waiting — lapsed at ‹t›". A new act on current content is needed.
  - **After resume, while the run is live, the same arrival is re-held**
    (RH-1…RH-8). It shows **"waiting — re-held, lapsed at ‹t› after
    resume"**. It is the same arrival with the same referents, now requiring
    an act on their current content.
    - The loop stops at its **next action boundary**. Dispatches already in
      flight complete and are observed; nothing is recalled or undone.
    - Actions taken between resume and the lapse observation stay recorded.
      Outputs whose promised standing names this checkpoint as gating show
      that standing *lapsed* for the affected referents.
    - The act request is re-issued for the **whole** declared scope, with the
      lapsed referents marked.
    - A satisfying act makes the arrival *performed* with the next
      performance ordinal, and a new resume point follows.
  - **A5 and A12 never re-hold** (RH-9). Applying an accepted item does not
    lapse A5; a basis failure after A5 is stale, not lapse (P §4.2). A12 is
    superseded, not lapsed.
  - If the run ends while re-held, the final disposition is **waiting** with
    the run-ended event (RH-7). *Lapsed* as a standing disposition appears
    only when the lapse occurs after the run has ended.
  - The v0.3 interim display "performed + act-lapsed event" is withdrawn.
  - An undo (OP-C10) that changes bound content lapses acts normally
    (R2-15), for example T16a's A4 at T17. **A lapse re-holds whatever
    caused it, including the person's own undo** (RH-8 generalized, R5-5).
    The person's undo is never recorded as *action during hold*. An undo
    never re-holds an A5 arrival.
  - **Partial lapse** (some referents only): the whole scope is shown with
    the lapsed referents marked. **Joint answer (SETTLED by DECISION-K1
    K1-3; EXEC §4.7 JA-1; U-03 closed):** an act on the lapsed referents
    alone answers the arrival together with the earlier act for the
    unchanged referents; two or more acts may together answer one arrival,
    and each cites its items. The loop relays each with its referents.
- C-5. **Negative decisions** (R2-5).
  - For A5, the negative decision is A10 (per item).
  - For A4, A6, A7 and A12, it is an **act-declined event** carrying capture
    evidence. That event is not an act of the declined kind.
  - Either case gives the disposition **resolved negatively**.
  - **Governance phase:** the declared *on negative decision* path is then
    followed; if none is declared, the run stops (EXEC NG-2). **Phase 1:**
    the disposition is recorded, and the declared path is guidance the
    agent follows in its plan; the loop does not stop the run for it
    (LP-8).
- C-6. **Governing checkpoint constraint** (R2-12; carriage per R4-14 and
  R5-2) — **governance phase (retained; R8-1)**.
  - **Phase 1 (R8-1; R8-11 item 2 as restated by R9-2; R8-10).** No
    constraint is carried as
    enforcement. The host's own treatment (grant and policy; V4-HI-30,
    V4-HI-40/41) decides a direct request, and the loop relays the outcome
    as observed (EXEC CH-27 Phase 1). The agent, following an A5
    checkpoint as plan guidance (WD I-7), proposes rather than requests
    direct application. It never adds a field the host's schema lacks
    (R8-10; strict preflight). If the host applies directly under the
    grant, no proposal is queued, so the A5 checkpoint (kind (c) *queued*)
    is **not reached**: nothing is requested by reason of an arrival that
    did not occur, no A5 is forced, and none is recorded; the record shows
    the direct application under the person's grant. A checkpoint the run
    does reach under such a grant has its act requested (LP-5) and is
    *waiting* until the person performs it (R9-2 as corrected by R10-1).
    The bullets below apply to governed
    checkpoints in the governance phase.
  - Where a declared checkpoint requires A5 on an operation's result, every
    dispatch of that operation in that run carries the constraint
    {workflow run identity, checkpoint name, required act A5, operation
    reference}, with its **carriage assurance** (P §3.3).
  - **The host loop's own evaluation is host-held** (R5-2). The loop derives
    the constraint from the resolved declaration it evaluates, never from
    model output.
  - A constraint the host merely **received** from an outside caller keeps
    its source's assurance (*model-supplied* or *App-assured*).
    *App-assured* is not available in this increment. **Only host-held
    carriage satisfies R2-12.**
  - The host route resolves *propose*. A direct request is **not
    permitted**, naming the constraint as the governing treatment. It is
    never converted into a proposal.
  - The loop does not decide treatment (R-3.1).
  - An omitted constraint is indistinguishable from none at the host. The
    omission is a loop defect and an evidence limit (§13 Q-1 → RELAY
    SQ-02). SQ-02 was answered 2026-09-28: route (iv), none planned; an
    extra constraint field would be refused as unknown; SWBPIPE has no host
    loop (SQ-20). SWBPIPE's "every change waits for Apply" is not
    host-held carriage (R2-12; EXEC GV-4).
- C-7. (Both phases; record labels in Phase 1.) **Mixed item decisions** at
  an A5 checkpoint follow **WD §4.3.7, as confirmed by DEL-02-03** (EXEC
  §4.11; R4-7):
  - every remaining bound item has A5 → *performed* over the remaining
    items (MX-4);
  - any item undecided → *waiting* (MX-2);
  - no item undecided and at least one item's decision observation lost →
    *unknown* (MX-3);
  - all remaining items decided, at least one A10 → *resolved negatively*,
    with a per-item **partial** annotation if some items have A5 (MX-5).
  - **Items that leave** without a decision (stale, A11, host refusal) are
    relayed with their event.
  - If no items remain, the arrival stays *waiting* "no items remain". A new
    arrival (e.g. a re-draft queued) closes it as **"replaced by arrival
    n+1"** (MX-6).
  - An item with A5 later refused stale, meeting an application error, or
    with *outcome unknown* at application leaves the disposition
    **unchanged**. It is annotated "accepted — not applied: …" (MX-7, MX-8;
    R3-3). It never re-holds and never triggers the negative path.
  - A *performed* over a reduced subject is never reported as "all
    accepted" (R2-18).
- C-8. **A12 checkpoints** (R2-7, PROPOSED; EXEC §4.10; R4-6).
  - The act binds to setting content (§2.4.2). The control's response is a
    relation on the act:

    | Control relation | Arrival effect |
    |---|---|
    | **established ⟨settings version⟩** | Counts (with SP-1…SP-6) → *performed* |
    | **pending** (set by person, not yet confirmed) | *waiting*, "A12 awaiting control confirmation" |
    | **refused ⟨reason⟩** (e.g. "no policy basis") | *waiting*. The refused A12 does **not** count, and "A12 by ‹person› refused by control: ‹reason›" is shown |
    | confirmation lost (*unconfirmed*) | *unknown* until observed |

  - **A later A12 supersedes an earlier one only when it is established.** A
    refused or pending A12 supersedes nothing, and the earlier setting stays
    in force (AR-3).
  - A checkpoint an earlier A12 performed stays *performed*, with any
    supersession shown.
  - A refused A12 remains a recorded human act that establishes nothing
    (AR-1). Governance phase: a held kind (a) call stays undispatched while
    the arrival waits (AR-2). Phase 1: no call is held; the control
    relations above label the record.

#### 2.4.4 Hold support in host loops — governance phase (retained; R4-2, R5-1, R8-1, R8-8)

**Phase 1 (R8-1, R8-8; DECISION-4 D4-1 and clarification).** The host loop
**does not enforce holds**. No checkpoint receives a hold-support value, no
workflow is *unsupported* for a hold reason, LH-0's holding of sibling calls
does not apply, and the compatibility report lists checkpoints as guidance
(EXEC CR-8/CR-9; §2.4.0 LP-2). Everything below in this section is the
**governance-phase definition, retained and relabelled, not deleted**
(EXEC GV-1). It applies to checkpoints declared **governed** (WD-v0.7
§4.3.1; EXEC GV-2) once the owner takes the governance phase up. SWBPIPE has
no host loop (SQ-20), so no *enforced by the host loop* evidence can exist
for it now (EXEC GV-4).

In the governance phase the host loop controls its own dispatch, so it
holds a run itself (EXEC §2 "hold machine in host loops"). Hold support takes
exactly one of the **four values ruled in R5-1**:
- enforced by the host loop;
- enforced on the host route;
- not established;
- not enforceable.

| Checkpoint (embedded route) | Hold support | Residual limit (stated, not a separate value) |
|---|---|---|
| Kind (a) on a host catalog operation | **enforced by the host loop**: the loop holds the schema-conformant call (§2.4.1) | None for the held call. Other calls already in flight are recorded as *action during hold* |
| Kinds (b)/(c) | **enforced by the host loop**: on the arrival event the loop dispatches nothing further and produces no declared output (HD-1/HD-2) | A dispatch or output issued between the arrival event and the loop's observation of it is recorded as **action during hold**, never hidden (HD-4; MA-3) |
| A5 checkpoint (kind (c) *queued*; host-held constraint, C-6) | **enforced by the host loop** (the loop stops after *queued*; the host route resolves *propose* from the host-held constraint) | Host evidence that the route honours the constraint: AWAITING INPUT (§13 Q-1 → SQ-02; DEP-001) — SQ-02 answered 2026-09-28: no host loop and no host-held evaluation; route (iv), none planned (SQ-20) (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3) |
| Invalid or not established declaration | **No value** (EXEC HS-1; F-22; R6-1): reported as invalid / not established and never evaluated. For a governed checkpoint the workflow check is *not established* (EXEC §4.14). Phase 1: a declaration finding only; the check result is unchanged by it (R8-11 item 3; LP-9) | — |
| Kind (a) on a harness capability; App-only steps | Does not arise in host loops (§1). In App runs a governed checkpoint is classified by **what it must hold** (R6-1; EXEC HS-3/HS-5): if every held action is a host operation, the value follows SQ-02 (*enforced on the host route* / *not established* / *not enforceable*); if any held action is App-side, *not enforceable* (D6: closed for Phase 1, re-opens with the governance phase). Against SWBPIPE, SQ-02 is answered with route (iv), so HS-3 (c) gives *not enforceable*; SQ-11 is answered, so HS-4 does not mask SWBPIPE entries (R8-2; EXEC GV-4). These values read the fixture's checkpoints as if governed (R8-11 item 5) | — |

In the governance phase the workflow requirement check passes for
*enforced by the host loop*, with holds subject to host evidence (DEP-001).
At the hold, the run stops at its next action (R6-3). The retired v0.4
values "enforced before dispatch" and "held after observation" are replaced
by the residual limits above. "Enforced on the host route" is not a
host-loop value; it applies to App runs over surface X under SQ-02 (EXEC,
R5-1).

LH-0…LH-4 are governance phase (retained).

- LH-0. Sibling calls in the same model response that are not yet
  dispatched when an arrival is observed are **not dispatched**. The model
  receives "held at checkpoint" results for them. Only calls already
  dispatched count as *action during hold* (see MC-8, T-OPEN-1).
- LH-1. While holding, the agent may still explain the request and issue an
  A8 request. Conversation is not run progress (HD-2).
- LH-2. Host lifecycle continues independently. For example, after the
  person's A5 the host may apply an item while the run holds (HD-3).
- LH-3. **App-side holds are not this contract's.** How the App holds its own
  runs is `UNRESOLVED{D6}` (DECISION-2). SWBPIPE answered SQ-02 on
  2026-09-28 with route (iv), none planned. D6 is closed for Phase 1 by
  DECISION-4 and re-opens with the governance phase (R8-2). This contract
  never claims an App hold. It adopts neither interposed App code
  (HP-1) nor reliance on `turn/interrupt` (HP-2). HP-3, a named-rule decline
  of a tool-permission request, is App-side and does not arise in host loops
  (§9 A-5).
- LH-4. In the governance phase the compatibility report (EXEC §3) shows
  each governed checkpoint's hold support before the run. In Phase 1 it
  lists the checkpoints as guidance, with no value (EXEC CR-8/CR-9). The
  panel shows either (PANEL §3.2).

## 3. Operating sequence (one turn)

The steps below are semantic. Their placement is owner-selected
(`UNRESOLVED{OI-013}`).

```text
person message ─► request (messages + offerings of edition K + supplied guidance, identities recorded)
   ─► native layer: destination check; credential if cloud (API key or OAuth sign-in) (§5) ─► model server
   ◄─ streamed content and/or tool calls, then termination reason
for each tool call:
   V-1 parse ── fail ─► class 1, not dispatched
   V-2 operation in offered edition K? ── no ─► class 1 "not offered", not dispatched
   V-3 input schema ── fail ─► class 1, not dispatched
   V-D destination check (native layer; entries with an external-contact
       declaration, and a destination request's carried call; §5.3 DF-4 (b))
       ── not allowed ─► class 2 "destination not allowed", not dispatched
       ── destination request ─► interim notice; only the carried call waits
          until the person answers (DF-5), then its outcome as the deferred result
   [kind (a) checkpoint on this operation?] ─► record arrival; Phase 1: dispatch continues
                                              (governance phase: hold call)
   dispatch with dispatch record (§6.2) ─► host route V-4/V-5
      (every contact the host then makes passes the native layer: DF-4 (c))
   ◄─ host outcome (class 2/3, incl. relayed "not exposed") or none (class 4)
   [kinds (b)/(c) match?] ─► record arrival; subject bound per declared class
                             (governance phase: stop acting on the run)
run end ─► run-ended event with every checkpoint disposition
```

In Phase 1 every checkpoint step records and never holds (§2.4.0). The
wait of a destination request's carried call is not a checkpoint hold
(NW-12; G-8).

The person's message, turn cancel, run stop and workflow selection reach
the loop as the panel's return inputs (PANEL-v0.8 §3.9). Decisions the
person makes through the host's control (A4, A5, A10, A12, including
network-destination grants, and A13) do not come from the panel as inputs;
the loop receives the host's capture record (E-2).

### 3.1 Failure behaviour at each step (v0.8; S1-D LOOP item 8; R12-1)

PROPOSED unless a cited rule decides it. "Record" is the run record
(DEL-04-03's format); every event also carries its E-6 ordinal. None of
these rules is a checkpoint hold: in Phase 1 nothing holds for a checkpoint
(§2.4.0), and F-10's pause concerns a record that cannot be written.

| # | Step | What fails | Who reports | Record left | What happens next |
|---|---|---|---|---|---|
| F-1 | Person input reaches the loop | The return input is not delivered | Panel (PANEL-v0.8 §3.9, outcome *not delivered*) | None: no turn started | The person resubmits. The panel never shows an undelivered message as sent |
| F-2 | Model setting check | (a) Unconfigured: no model chosen. (b) Cloud chosen with no credential | Native layer | (a) **Run not started — no model selected** (R15-1, DERIVED: V4-HOST-01 gives the person options with no default, so with no model selected no turn can start). This is a run that does not start, not a refusal at the network boundary: no destination exists to refuse, so no `boundary_refusal` and no other destination entry is written. It is recorded on RS's run-start element with that cause (RS-v0.8 §4 R1; §13.3.1; `run_opened` with `notStarted`), and its evidence is the loop's own configuration state at start (MS-02, "observed absence"). This is at a run's first turn, where `run_opened` is written; in a live run nothing is written for the message (§3.2; RQ). (b) "Model request refused at boundary" (no credential content), recorded as `boundary_refusal` at stage *model request*, reason *no credential* (RS-v0.8 §4 R15, §13.3.1; V18-1 m-11); turn failed. At a run's first turn the run is opened live before the refusal, so the refusal is recorded on an opened run (§3.2 workflow-run table; C0; V19b m-1) | (a) No turn starts; a notice asks the person to choose (MS-02). (b) No request is made (MS-04). In both, nothing falls back (NW-5), and only the person chooses or signs in (NW-4) |
| F-3 | Native-layer destination check on the model request | The request names a destination other than the selected model service (MS-05) | Native layer | Refusal event; turn failed | Setting unchanged; no fallback (NW-5) |
| F-4 | Native layer records the contact | The destination record cannot be written | Native layer | The refusal, when it can be written (recording PROPOSED, R12-10) | The request is **not sent** (fail closed), because every destination contacted is recorded (V4-ARC-12 as amended). For the model request: turn failed. For a tool call's contact: the host outcome as reported. Joined to §5.1.1 at v0.8: §5.3 DF-4 (c), DF-F2 |
| F-5 | Model server and transport | Unreachable server, rejected or expired credential, service error before any stream | Model server or transport / loop | Model interface failure (termination reason "error"; §4.1 point 2); turn failed | No switch between local and cloud (MS-08, MS-09) |
| F-6 | Stream | Ends with no termination reason, or the transport fails mid-stream | Loop | Model interface failure; the agent message *interrupted*; every call of that response *interrupted* (MC-2) | Turn failed. Nothing is dispatched from the response |
| F-7 | Stream | Termination "length" or "content filter" | Loop | Agent message *truncated* (length) or *failed* (content filter); every call of the response rejected (MC-1, MC-11) | Class 1 results go to the model; the turn continues with the next model request, or completes if the response had no calls |
| F-8 | V-1…V-3 per call | Parse, offering or schema failure | Loop | Per §7: three reports (model, events, record) | Each call is judged on its own; the other calls of the response go on (MC-8; R12-7) |
| F-9 | Dispatch to the host route | The route is unreachable, or delivery is not confirmed | Loop (observer) | Class 4 *outcome unknown*, last observed state "dispatch attempted; host route unreachable" | The loop seeks observation before any resubmission (§6.3 R-d); a resubmission keeps the proposal identity (R-a) |
| F-10 | Run record write | The record does not accept a write | Loop | Events already emitted; the failure itself is written once the record accepts writes, as RS's "record write failed" limit (RS-v0.8 §14.1 W-2; E-8, CE-19). A write is done only when RS §14.1 W-1 says so: one complete line appended and synced (v0.8, RP-4) | The loop makes **no further dispatch** until a dispatch can be recorded: a call that cannot be recorded is not made (V4-HI-70 inventory; E-4). If the record cannot be restored, the run ends with cause *failure* and the run-ended event is written when the record returns. This pause is a failure rule, not a checkpoint hold |
| F-11 | Turn cancel (RS-3) | — (the person cancels) | Person (panel return input) / loop | Turn cancelled; undispatched calls "not dispatched: turn cancelled" (§2.3); dispatched calls keep their outcomes | Nothing dispatched is recalled or undone. Outcomes are observed and recorded, or become class 4. A destination request still pending ends *unanswered at end* (turn cancelled); its carried call is not sent (§5.3 DF-5 Q-9, DF-F6) |
| F-12 | Event delivery to the panel | No panel attached, or a delivery gap | Loop / panel | Every event stays in the record (E-7) | The panel detects the gap by ordinal and asks from the last ordinal it holds (PANEL-v0.8 FD-3). The run is unaffected |
| F-13 | Host outcome observation | Lost after dispatch | Loop (observer) | Class 4 with the last observed state | As F-9. A kind (c) arrival deciding on that outcome is *unknown* (§2.4.1) |

### 3.2 State summary (v0.8; S1-D LOOP item 8; R12-1)

One table per stateful thing this contract owns. States marked *governance
phase* never arise in Phase 1. PROPOSED unless a cited rule decides it.

**Workflow run.**

| From | Event | To | Record |
|---|---|---|---|
| — | First turn starts (PANEL-v0.8 §3.9 RI-1) under a workflow selected for a run (RI-4), model setting usable, or cloud chosen with no credential (the run opens live and its first turn fails, F-2 (b)) | live | `run_opened`: run identity; workflow identity tuple; holding library; continues ⟨run⟩ if any (R4-4). A host-loop run is opened, and `run_opened` written, when its first turn starts, not at the selection (RQ; V19-B m-4; PROPOSED). With no credential the run is opened first (`run_opened`, then RS-v0.8 §14.1's run-start entries), so the turn's `boundary_refusal` at stage *model request*, reason *no credential*, is recorded on an opened run; the run stays live, and the person may sign in or supply a key and send again in the same run. Only a run with no model selected is *not started* (R15-1; next row) (C0; V19b m-1; PROPOSED) |
| — | First turn would start, but no model is selected (F-2 (a); MS-02) | not started (final) | `run_opened` with `notStarted`: **run not started — no model selected**, with the loop's configuration state at start as evidence, and nothing more: no turn, no destination entry, no `run_ended` (R15-1; RS-v0.8 §4 R1, §13.3.1). A later start after the person chooses a model is a new run |
| live | Observation lost | interrupted | Run interrupted (EXEC RE-4) |
| interrupted | Observation recovered | live | Observation recovered; re-observed events, nothing back-filled (EXEC RP-1…RP-5) |
| interrupted | Recovery impossible | ended | Run ended, cause "interruption not recovered" |
| live | Model ended; person stopped (PANEL return input); declared negative path (governance phase); failure (F-10) | ended | Run ended with cause and every checkpoint disposition (§2.3) |
| live | Arrival at a governed checkpoint (*governance phase*) | held | Checkpoint reached; the loop stops acting on the run (C-1, §2.4.4) |
| held | Act performed, or negative decision with a path (*governance phase*) | live | Run resumed (EXEC HD-5) |
| ended | Anything | ended (final) | Later acts recorded "after run end" (R4-4) |

**Turn** (one person message and the model requests it leads to).

| From | Event | To | Record |
|---|---|---|---|
| — | Person message received, model setting usable | awaiting model | Turn started; model setting in force (§2.1) |
| — | Person message received, no model selected (unconfigured) | (no turn) | F-2 (a): no turn starts; a notice asks the person to choose (MS-02); not a boundary refusal, and no destination entry. At a run's first turn the run is recorded **run not started — no model selected** (workflow-run table above); in a live run nothing is written for the message and the run stays live (RQ; R15-1; PROPOSED) |
| — | Person message received, cloud chosen with no credential | failed | F-2 (b): `boundary_refusal` at stage *model request*, reason *no credential*. At a run's first turn the run is opened live first (workflow-run table above; C0) |
| awaiting model | Refusal at boundary or model interface failure | failed | F-3…F-5 |
| awaiting model | First streamed increment | streaming | Model stream progress |
| streaming | Termination *stop* or *length* with no tool calls, and no destination request of this turn pending (v0.8, node B5) | completed | Agent message *complete* or *truncated* |
| streaming | Termination *content filter* with no tool calls | failed | Agent message *failed* (F-7) |
| streaming | Termination *tool calls*, or *length* / *content filter* with calls | running tool calls | Tool calls received (§7) |
| streaming | Stream ends with no termination reason | failed | F-6 |
| running tool calls | Every call of the response has a result of class 1–4, or an interim notice for a pending destination request (§5.3 DF-5 Q-5) | awaiting model | Results returned by correlation identity. Assistant text in a response that terminated *tool calls* is complete at that termination (§2.4.1 kind (b); v0.8, RP-4) |
| streaming | Termination *stop* with no tool calls while a destination request of this turn is pending (v0.8, node B5) | awaiting destination answer | The turn does not complete (DF-5 Q-5) |
| awaiting destination answer | The request is answered (granted and in force, declined or not granted) | awaiting model | The deferred outcome is sent with the next model request (DF-5 Q-7, Q-8) |
| awaiting destination answer | Run ends | failed | The request ends *unanswered at end* (DF-F7); turn recorded as ended by the run's end |
| any but completed, cancelled, failed (including awaiting destination answer) | Person cancels | cancelled | F-11; a pending destination request ends *unanswered at end* (DF-F6) |

**Tool call.**

| From | Event | To | Record |
|---|---|---|---|
| — | First fragment at a position | receiving | — |
| receiving | Response terminates (§4.1 point 2) | received, or rejected (V-1) | Tool call received; MC-1, MC-2, MC-10…MC-13 as they apply |
| received | V-1 parse, V-2 offering, V-3 schema | schema-conformant, or rejected | §6, §7; class 1 on rejection |
| schema-conformant | Kind (a) arrival (*governance phase*, governed checkpoint) | held at checkpoint | Call held (§2.4.1) |
| schema-conformant | V-D (§5.3 DF-4 (b)): destination not allowed, direct call | rejected at V-D | Class 2 "destination not allowed" with reason; not dispatched; `boundary_refusal` (recording PROPOSED) |
| schema-conformant | V-D: the carried call of a pending destination request (v0.8, node B5) | waiting for destination answer | NW-12: only this call waits. V-D sits after V-3 and before the kind (a) step and dispatch (§6) |
| waiting for destination answer | Grant in force (DF-5 Q-7) | schema-conformant, V-D passed | Then dispatched as usual |
| waiting for destination answer | Declined, not granted, or unanswered at end | not dispatched: destination request ended | DF-5 Q-8, Q-3/Q-7, Q-9 |
| schema-conformant (V-D passed or not needed), or held | Dispatch | dispatched | Dispatch record (§6.2) |
| dispatched | Host outcome observed | outcome observed | Class 2 or 3 |
| dispatched | Observation lost, or route unreachable | outcome unknown | Class 4 (F-9, F-13); a later observation is recorded as a new event (R-d) |
| receiving, received, schema-conformant, held or waiting | Person cancels the turn | not dispatched: turn cancelled | §2.3 (F-11) |

**Destination request** (v0.8, node B5; PROPOSED over the SETTLED rules
NW-11…NW-13; the account is §5.3 DF-5, DF-6). One request per call to the
destination request entry. B9's state names are kept; *not grantable* is
now a reason of *not granted*.

| From | Event | To | Record (RS R15) | Result of the request call |
|---|---|---|---|---|
| — | Request call passes V-1…V-3 and the target is already allowed | (no request raised) | — (nothing is recorded as a destination request; the carried call's contact is `destination_contacted` under its allowing entry) | The carried call's outcome, or class 3 "already allowed" |
| — | Target not grantable (A-3; an always-off item) | **not granted** ("not grantable") | `destination_requested`; `destination_request_closed` | Class 2 "destination not allowed" (reason) |
| — | Request recorded and prompt shown | **pending** | `destination_requested` | Interim notice |
| — | Prompt cannot be shown (DF-F4) | **not granted** ("prompt not shown") | `destination_requested`; `destination_request_closed` | Class 2 "destination not allowed" (prompt not shown) |
| pending | Person grants and the control establishes the grant | **granted** (once · this run · always) | `human_act` (A12); `destination_grant` | Deferred: the carried call's outcome, or class 3 "granted: ‹scope›" |
| pending | Person grants and the control refuses | **not granted** ("grant refused by control: ‹reason›") | `human_act` (A12, refused by control); `destination_request_closed` | Deferred: class 2 "destination not allowed" (reason) |
| pending | Person declines | **declined** | `act_declined` (A12); `destination_declined` (PROPOSED recording) | Deferred: class 2 "destination not allowed by the person" |
| pending | Run ends, or the person cancels the turn | **unanswered at end** | `destination_request_closed` | None (never a grant by silence, NW-13) |
| pending | No answer yet | pending (unchanged) | — | — |

**No *pending* before *not granted* (v0.8, RP-4; V18-1 m-10; PROPOSED).** A
request that is not grantable, or whose prompt cannot be shown, is recorded
(`destination_requested`) and closed *not granted* in the same step: it
never enters *pending*, no prompt state precedes it (PANEL ND-2 PS-5), and
settings-in carries it with the state *not granted* only (AS §3.1 DG-15). An
already-allowed request raises no request (Q-3); the record shows the
contact under its allowing entry. RS R15's "each destination requested" is
read here as each request raised (returned to RS for its text).

Checkpoint dispositions (§2.4) and grant states (O-6) are defined where
they are and are not repeated here.

## 4. Minimal Chat Completions capability

| Capability | Why | Settled or open |
|---|---|---|
| Submit an ordered conversation and tool offerings | Messages, tools | Settled need (V4-ARC-10) |
| Receive assistant content incrementally | §8; panel | Settled need |
| Receive tool calls (correlation identity, name, argument text, possibly fragmented) | Tools; §7 | Need settled. Fragment representation: written from FB-CC-1 (§4.1 point 1), PROPOSED; product representation DEP-05-01-024 |
| Termination reason that distinguishes complete, length-truncated and error | §7 | Need settled. Representation: written from FB-CC-1 (§4.1 point 2), PROPOSED; product DEP-05-01-024 |
| Return a tool result for a correlation identity, including "held at checkpoint" (governance phase) | Tools; §2.4.1 (a) | Settled need |
| Several tool calls per response | §7 MC-8 | Written from FB-CC-1 (§4.1 point 3), PROPOSED; handling ruled by R12-7 (INTEGRATION). Product DEP-05-01-024 |
| "No arguments" (a call to an entry with an empty input schema) | §7 MC-6 | Written from FB-CC-1 (§4.1 point 4), PROPOSED; product DEP-05-01-024 |

No provider, server, model or version is selected. ARCH §6 names are dated
assumptions. The three representation rows that v0.7 left open are closed
**as PROPOSED** from FB-CC-1 below (R12-8). OBS-1 has since observed all
four points on one local server (§4.1, OBS-1 column; R13-6). The rows stay
PROPOSED: one observation at one server version is not qualification, and
DEP-05-01-024 is still open for a product.

**One model-interface boundary (R12-11; INTEGRATION, on the owner's
direction of 2026-09-30 to keep Chat Completions for the host loop).** The
loop reaches its model through one model-interface boundary: the
capabilities in the table above cross it (an ordered conversation and tool
offerings go out; streamed content, tool calls and a termination reason
come back; a tool result goes out by correlation identity), and nothing
else in the loop depends on how an interface represents them. V4-ARC-10's
OpenAI-compatible Chat Completions interface is the one interface behind
the boundary (V4-ARC-10 stands, not amended). A second interface, the
Responses API being the likely one, can be added later behind the same
boundary without restructuring the loop. This statement selects nothing:
no second interface, provider, server, model or version.

### 4.1 Fixture basis FB-CC-1 — fixture basis, not a product selection (R12-8; v0.8)

**What FB-CC-1 is.** A published Chat Completions reference that this
contract's fixtures and malformed-call rules are written against. It is
labelled **"fixture basis, not a product selection"**: DEL-05-01 REQ-002
forbids selecting a product protocol version before its basis exists, and
DEP-05-01-024 (the product's model-interface basis) stays UNKNOWN (§10.3).
FB-CC-1 selects no provider, server, model or version for any host, and no
host is claimed to follow it.

**Source and retrieval (read-only; DECISION-K1 K1-6; brief B9).**

| Item | Value |
|---|---|
| Text relied on | The published OpenAI OpenAPI specification, `openapi.yaml`, repository https://github.com/openai/openai-openapi (default branch `main`, as the GitHub repository record reported at retrieval) |
| URL fetched | https://raw.githubusercontent.com/openai/openai-openapi/main/openapi.yaml |
| Retrieved | 2026-09-30, 17:53 UTC (`curl`, HTTP 200, 3,895,612 bytes) |
| sha256 of the bytes relied on | 976053bfe228984127c1c4def7cb9fe0810252adbd8c41651812f68beb6426ad (`openapi: 3.1.0`; `info.version: 2.3.0`). The `master` branch returned byte-identical content at the same time |
| Branch head at retrieval | 36a1ed5e96952caf44480de72da1a3cb74e69966, committed 2026-09-30T17:47:20Z (GitHub API). The branch moves; the sha256 above identifies the text |
| Not relied on | The HTML reference https://platform.openai.com/docs/api-reference/chat returned HTTP 403 to a read-only fetch on 2026-09-30, so the specification behind it is the text relied on. The `manual_spec` branch (`openapi: 3.0.0`, same `info.version`) carries the same passages quoted below; it is not the basis |

Member names such as `finish_reason` or `index` below are the reference's
own, quoted to locate the passage (§0). Line numbers are those of the bytes
pinned above.

**The four representation points.**

| # | Point | What the reference says (short quotes; schema; line) | What FB-CC-1 establishes, and what it does not | Receiving rule (PROPOSED) | OBS-1 (local OpenAI-compatible server) |
|---|---|---|---|---|---|
| 1 | Fragmented (streamed) tool calls | `ChatCompletionStreamResponseDelta` is "A chat completion delta generated by streamed model responses." (L41805); its `tool_calls` items are `ChatCompletionMessageToolCallChunk`, whose only required member is `index` (`required: - index`, L41043–41044); `id`, `type`, `function.name` and `function.arguments` are optional in a chunk | A streamed call arrives as fragments correlated by their position in the response; any fragment may lack the identity, the name or an argument piece. The reference does not say in words that argument pieces are concatenated: that is an **inference** from `arguments` being a string in each chunk with only `index` required | R-F1…R-F4 (§7.1): join fragments by position; append argument text in arrival order, never repaired (MC-9); identity and name from the fragment that carries them; a conflicting later fragment is MC-10; a fragment with no position rejects the response's calls (MC-13) | **Observed (C1):** the call came in **two** fragments at position 0: first the identity, type and name with argument text `""`, then the whole argument text (`{"key":"EX-1"}`) as one piece. The identity was a numeric string. Consistent with R-F1…R-F4 (the empty first piece appends nothing). Not observed: argument text split over several fragments; a later fragment repeating the identity or name (MC-10) |
| 2 | Termination (finish) reasons | `finish_reason` enum `stop`, `length`, `tool_calls`, `content_filter`, `function_call` (L43466–43471 complete response; L43653–43659 streamed, where it may also be `null`). "`length` if the maximum number of tokens specified in the request was reached"; "`tool_calls` if the model called a tool" (L43451–43462). `function_call` is marked deprecated | *Complete* = `stop` or `tool_calls`; *length-truncated* = `length`; content omitted by a filter = `content_filter`. **No value names an error**: an error is a transport or service failure, or a stream that ends with no reason (every chunk `null`). The deprecated `function_call` form is outside the fixture basis | §7 MC-1 (length: every call of the response truncated), MC-2 (no reason: interrupted), MC-11 (content filter), MC-4 (deprecated form); §3.1 F-5…F-7 | **Observed (C1–C3):** the last chunk had an empty delta and `finish_reason` `tool_calls`, followed by `data: [DONE]`; every other chunk had `finish_reason` `null`. Not observed: `stop` beside calls, `length`, `content_filter`, an error, or a stream ending with no reason |
| 3 | Several tool calls in one response | The message's tool calls are "The tool calls generated by the model, such as function calls." (an array, L41045–41047); the request member `parallel_tool_calls` is "Whether to enable [parallel function calling] … during tool use.", `default: true` (L55894–55899). Choices "Can be more than one if `n` is greater than 1." (L43438) | A response may carry several calls, in order, and by default the service may produce them. Several *choices* arise only with `n` above 1 | Each call is judged on its own (MC-8; R12-7). Fixtures request one choice; a chunk for a second choice is outside the basis (MC-12). Position order is kept (M-1) | **Observed (C2):** two calls in one response at positions 0 and 1, each in the two-fragment pattern; position 0 completed before position 1 began; one final `tool_calls`. Not observed: interleaved fragments (FX-V1i); a malformed sibling, so MC-8 stays PROPOSED (R12-7); a second choice |
| 4 | How "no arguments" is expressed | A complete call's `function.arguments` is a required string, "as generated by the model in JSON format" (`ChatCompletionMessageToolCall`, L40980–41011); "Note that the model does not always generate valid JSON" (L41005). For a tool: "Omitting `parameters` defines a function with an empty parameter list." (L50720) | An entry may have an empty parameter list, and argument text is always JSON text. The reference does **not** state the text the model sends for an empty list. **Inference:** "no arguments" is argument text that parses to a JSON object with no members (`{}`) | MC-6: `{}` parses and goes on to V-3 against the entry's input schema; absent or empty text is malformed and is **never** coerced to no arguments (ARCH §4; SOW-142) | **Observed (C3):** for a tool whose parameters are an empty object the argument text sent was **`{}`** (not `""`, not null), with `finish_reason` `tool_calls`. Agrees with the MC-6 inference |

**The OBS-1 column (R13-6; observation, not qualification; v0.8, RP-4).**
Source: DEL-01-01 `OBS_1_0.158.0.md` §10, Part C (sha256 `85707703e97b…`
as read at this pass): three streamed requests (C1, C2, C3) to
`POST /v1/chat/completions` on LM Studio 0.4.16+2 serving `qwen/qwen3.5-9b`
(4-bit MLX, context 24576), with invented content, on 2026-09-30, under
DECISION-K1 K1-6. It was not a Codex turn and observed no host; the raw
streams stay in the observer's scratch folder and are not committed. Each
cell is one server at one version. A difference between the observation and
FB-CC-1 is recorded as observed and does not silently change a rule; none
was found on the four points. Two things outside FB-CC-1 were also seen:
reasoning streamed first as `delta.reasoning_content`, and whitespace-only
`delta.content` beside a call (§4.2). The three observed shapes are
reproduced as prototype fixtures OBS1-C1…OBS1-C3, with FX-PIPE-01 entries
in place of the observed tool names (§7.3).

### 4.2 Where FB-CC-1 stops

- It covers the loop's receiving of one model response. The request side
  (how offerings and tool results are sent) is used only as §4's needs.
- It says nothing about hosts, native layers or destinations (§5).
- A custom tool call (another item kind in the same array) and the
  deprecated `function_call` form are outside the fixture basis and are
  rejected as MC-4.
- Members outside it (v0.8, RP-4; PROPOSED). OBS-1 saw `delta.reasoning_content`
  stream before the content and calls (§4.1). Reasoning is neither a tool
  call nor the agent message's content: the assembly reads it as neither
  (§7.1), and it never counts as a completed message for a declared output
  (WD-v0.8 §4.4 OP-2). How a product records it is DEP-05-01-024's.

## 5. Model selection, destination and key boundary

### 5.1 Settings (semantic)

| State | Meaning |
|---|---|
| Local chosen | The person chose a user-controlled local model server, and it is configured |
| Cloud chosen, signed in (OAuth) | The person chose a cloud model and completed an OAuth sign-in (DECISION-4 D4-3) |
| Cloud chosen, key supplied | The person chose a cloud model and supplied an API key |
| Cloud chosen, no credential | No key and no sign-in. No request may be made |
| Unconfigured | The person has not chosen. No request may be made. There is **no default** and no fallback |

- **SETTLED.**
  - NW-1 (revised at v0.6 by DECISION-4 D4-3; R8-9): local and cloud are
    **options the person chooses among; there is no default** between them.
    A cloud model is reached by **OAuth sign-in or an API key**.
    The accepted V4-HOST-01, as amended by SCA-V4-001, reads: "A host's
    agent runs on a model the person chooses: a model server the user
    controls, or a cloud model reached by OAuth sign-in or an API key.
    There is no default between them; they are options the person chooses
    among (D-18; DEC-4)." V4-ARC-11 as amended says the same ("local or
    cloud, as the person chooses, with no default"), and the DEL-05-01 SoW
    REQ-001 and AC-001 carry this wording since SCA-V4-001 (G-6, closed).
  - NW-2 (revised in place by DECISION-5; R8-13): the host's agent sends
    data only to the selected model service and to destinations the person
    has allowed (§5.1.1). The accepted V4-HOST-02, as amended by SCA-V4-001
    (the recorder's wording of DECISION-5, confirmed by the owner), reads:

    > A host's agent sends data only to the model service the person selected and to destinations the person has allowed — in advance in an allow list (by category, such as web access, MCP servers or other APIs, or by named destination) or when the agent asks during its work. Nothing else is contacted: no analytics, silent provider switch or background download unless the person turns it on. Every destination contacted is recorded and shown (D-18; DEC-5).

    The accepted text carries no "in local operation" qualifier: NW-2 and
    NW-15 hold in any model mode (ARCH §4: "every destination contacted is
    recorded and shown, in any model mode").
  - NW-3: requests go through the native layer, which enforces the endpoint
    and holds the credential outside the script (V4-ARC-12 as amended by
    SCA-V4-001: the native layer "holds any key or sign-in credential
    outside the interface's script").
- **PROPOSED at v0.6; from v0.7 each rule carries its own label (R9-4).**
  - NW-4 (PROPOSED): settings change only by the person's act, including
    choosing
    local or cloud, signing in or out, and supplying or removing a key. An
    agent may ask (A8) but never initiates or completes a sign-in, and never
    changes the setting.
  - NW-5 (DERIVED from V4-HOST-01, under which local and cloud are "options
    the person chooses among" with no default between them, and from the
    always-off item of V4-HOST-02 and ARCH §4, which keep "a silent switch
    to another model or provider" off unless the person turns it on, NW-14;
    SETTLED only for "no silent switch unless the person turns it on"):
    there is no automatic switch between local and
    cloud on a
    failure, in either direction. With no default, there is nothing to fall
    back to.
  - NW-6 (SETTLED for the interface's script: V4-ARC-12 as amended; SoW
    REQ-001 and AC-002. PROPOSED for the rest of the list, which no
    accepted text states): no credential (API key or sign-in credential)
    ever appears in
    script memory, messages, events, records, the panel or errors.
  - NW-7 (SETTLED: V4-ARC-12 as amended, the native layer "allows only the
    selected model service and the destinations the person has allowed,
    records every destination contacted"; SoW AC-002): the native layer is
    the enforcement point.
- **Ruled (v0.8).**
  - `N-OPEN-1`, what counts as a "user-controlled local" endpoint: **closed
    by R12-7 (DERIVED from V4-HOST-01 and V4-HOST-02 as amended).** The
    model service the person selected is allowed whether it is local or
    cloud (NW-1, NW-9), so "user-controlled local" is a **class label** in
    the destination record, not a gate: the record of a model-service
    contact carries the class **local** or **cloud** as the person's model
    choice states it (§5.1 states), in the same way HOSTING-BOUNDARY-v0.7
    §8.3 derives the App's destination class from the provider
    configuration the person chose. The loop and the native layer never
    infer the class from the address, and never refuse a selected service
    because of where it runs. MS-11 is released.
- **Open.**
  - `UNRESOLVED{N-OPEN-2}`: cloud-chosen destinations, including the sign-in
    endpoints an OAuth flow contacts. From R8-13 the sign-in service is
    allowed by the person's model choice (NW-9); which endpoints it
    comprises stays open.
  - `UNRESOLVED{N-OPEN-3}`: tool-caused traffic (e.g. a later Domains query).
    From R8-13 it is governed by the allow list and in-work grants
    (NW-8…NW-13). From v0.8 (node B5) the traffic an entry **declares** in
    its external-contact declaration is the agent's and passes V-D (§5.3
    DF-1, DF-4); traffic a host operation makes without declaring it is
    refused at contact unless allowed (DF-F8). Whether undeclared traffic
    of a host operation counts as the agent's stays open. Not a permission.
  - `N-OPEN-4` (R8-13), how a category switch and the named entries within
    it combine: **closed by DECISION-K1 K1-5** (2026-09-30). The rule is at
    NW-8.
  - `N-OPEN-5` (R8-13), the evidence that an MCP server follows the
    stateless MCP revision 2026-07-28 (NW-10): **closed at v0.8 as
    PROPOSED** (node B5, from the published revision, K1-6): SE-1…SE-3 of
    §5.3 DF-7, with the evidence limit "stateless revision declared, not
    verified". PROPOSED until the owner or integrator accepts it.

**SWBPIPE (SQ-29, SQ-30; R8-9).** SWBPIPE has no model interface, endpoint
configuration or key custody (`api_key` appears only as a redaction key
name). Its successor embedded mechanism is a SWBPIPE owner decision under
D-58. SWBPIPE DEC-051 (open residency: an owner-configured provider, cloud
included, with no app-side guard "for now") is **compatible with D4-3 on
choice**. It is recorded here as a note, not a conflict (R8-9). Under
V4-HOST-02 as amended (DECISION-5; R8-13), DEC-051's provider choice
corresponds to the person's model choice (NW-9). DEC-051 says nothing of
other destinations, and SWBPIPE has no embedded agent today (SQ-20,
SQ-29), so there is nothing to compare. §5.1.1 is for SWBPIPE to take up
when the owner resumes UI-SUCCESSOR; no SWBPIPE behaviour is claimed
(DECISION-3).

#### 5.1.1 Network destinations of the host's agent (DECISION-5; R8-13)

**Standing.** The rules below are **SETTLED by DECISION-5** unless labelled
otherwise, and are now carried by the accepted basis as amended by
SCA-V4-001: PRD V4-HOST-02, ARCH V4-ARC-12 and the ARCH §4 host-agent
property (SCA-V4-001 OWNER_ITEMS O-6). Two points are settled by the owner's DECISION-5 confirmation (2026-09-28: the "MCP V2" reading confirmed; the person-only grant not objected to and stands): the
person-only grant (NW-11), and the recorder's reading of the owner's "MCP
V2" as the **stateless MCP revision 2026-07-28** (NW-10). The mapping of a
grant to an act (A12, subclass *network-destination grant*) is
**INTEGRATION** (R8-13; ACT §2.7). DECISION-5 governs a host's embedded
agent only. The App's own Codex keeps the person's Codex configuration,
approval and sandbox choices (ARCH §4, closing sentence of the host-agent
property; HOSTING §2; D-GOV-43).

| Element (semantic) | Meaning |
|---|---|
| Category switch | One per category. DECISION-5's examples are web access, MCP servers and other APIs; the category list is open. On or off, set only by the person |
| Named destination | A destination the person allowed by name within a category |
| Model service | The model service the person selected and, for a chosen cloud model, its sign-in service. Allowed by the person's model choice (§5.1 states), not by a list entry |
| In-work grant | A destination, or its category, that the person granted when the agent asked during its work, with its scope: **once**, **this run** or **always** |
| Always-off item | Analytics or usage reporting; a silent switch to another model or provider; background downloads or updates. Off unless the person turns it on |
| Outside process | An MCP server or other process the host starts for the agent, with the destinations it declares |

- **SETTLED (DECISION-5).**
  - NW-8 **Allow list, two levels.** The person allows destinations in
    advance by category switch, and by named destination within each
    category. Every edit is the person's act (ACT §2.7). A destination is
    allowed when its category is switched on, when it is a named entry,
    when an in-work grant in force covers it, or when it is the model
    service (NW-9). **How the two levels combine (SETTLED by DECISION-K1
    K1-5; `N-OPEN-4` closed):** a named destination is allowed on its own;
    a category switch means "allow everything in this category"; with the
    switch off, only the named entries in that category are allowed. This
    follows the owner's "by category … or by named destination" (now
    V4-HOST-02's words); ARCH §4 as amended says "a category switch … and
    named destinations within each category". Switching a category off
    does not suspend its named entries (MS-15).
  - NW-9 **Model service always allowed.** The selected model service, and
    its sign-in service for a chosen cloud model, are allowed by the
    person's model choice. Changing that choice is the NW-4 setting
    change, not a list edit.
  - NW-10 **MCP only if stateless.** An MCP server is allowed only if it
    follows the stateless MCP revision 2026-07-28. A server that does not
    is not offered and cannot be allowed, by list or by in-work grant.
    (PROPOSED: a server whose conformance is not evidenced is treated as
    not following it; the evidence is §5.3 DF-7, SE-1…SE-3, closing
    `N-OPEN-5` as PROPOSED at v0.8.)
  - NW-11 **In-work request; only the person grants.** When the agent
    needs a destination that is not allowed, it asks: an A8 request naming
    the destination or category, its purpose and the scope sought. Only
    the person grants, as an A12 network-destination grant (ACT §2.7). The
    agent never grants itself a destination and never edits the list. A
    grant is scoped, for the destination or its category:
    - **once**: the one requesting call;
    - **this run**: until the run ends (a run that continues it inherits
      nothing, R4-4);
    - **always**: it becomes an allow-list entry.
  - NW-12 **Only the requesting call waits.** The requesting call is not
    sent until the person answers. The agent continues its other work,
    and no other call waits. This wait is not a checkpoint hold: it is the
    same in Phase 1 and the governance phase, and §2.4 is unaffected. It is
    the grant being sought, so DECISION-4 does not bear on it (R13-5; §5.3
    DF-5).
  - NW-13 **Decline.** A decline is reported to the agent as
    **"destination not allowed by the person"**. The call is not sent.
    The decline is recorded as an act-declined event of kind A12 (ACT
    §2.7; INTEGRATION, R2-5, R8-13), and **recording it as a destination
    entry is PROPOSED** (R12-10: V4-EXM-23 says a decline is reported to
    the agent; no accepted text says it is recorded). An unanswered request
    stays pending and is never treated as a grant (DERIVED from V4-EXE-02;
    AS S12); at the run's end or the turn's cancel it ends *unanswered at
    end* (§5.3 DF-6).
  - NW-14 **Always off unless the person turns it on:**
    - analytics or usage reporting;
    - a silent switch to another model or provider (compare NW-5);
    - background downloads or updates.

    Turning one on is an allow-list edit (NW-8).
  - NW-15 **Record and show.** Every destination contacted is recorded and
    shown, **in any model mode**: per request, the destination, its
    category and the grant or list entry that allowed it (RS R15; PANEL
    §3.8). Grants are recorded too; recording declines and refusals is
    PROPOSED (R11-5; R12-10), as in NW-13 and the enforcement bullet
    below. The display of the destinations contacted is AS §3.2 (§5.3
    DF-9). The accepted
    V4-HOST-02 carries no "in local operation" qualifier (SCA-V4-001).
  - NW-16 **Outside processes: the limit, stated plainly.** An MCP server
    or other outside process can make its own network calls. Unless it is
    sandboxed, the host can only decide whether to start it and record
    what it declares. The host records each such process with its
    declared destinations and, when it is not sandboxed, the evidence
    limit **"process network not observed"** (RS R11, R15). Nothing
    claims that the process contacted only what it declared.
- **SETTLED by V4-ARC-12 as amended (R9-4; PROPOSED at v0.6), except the
  part marked PROPOSED (R11-5).**
  - The native layer is the enforcement point for NW-8…NW-15 (NW-7). It
    refuses a request to a destination that is neither allowed nor under
    an in-work request, and it records every destination contacted
    (V4-ARC-12: the native layer "allows only the selected model service
    and the destinations the person has allowed, records every destination
    contacted"; NW-15). **PROPOSED:** it also records the refusal (case
    MS-23). V4-EXM-23 says a declined request is reported to the agent;
    no accepted text says the refusal is recorded. Where and in what order
    the native layer decides is §5.3 DF-3 and DF-4 (v0.8, PROPOSED).
- **PROPOSED.**
  - Starting an outside process is decided by the allow list: the process
    itself must be allowed (for MCP, a stateless server per NW-10).
- **Phasing (DECISION-4's principle, as DECISION-5 applies it).**
  - **Phase 1 (this increment):** the allow list (categories and named
    entries), in-work requests with scopes, nothing hidden, record and
    show (NW-8…NW-16).
  - **Governance phase (later; named here, not defined):** allow lists
    locked by an organization, and enforced sandboxing of MCP servers and
    other outside processes. Until then NW-16's evidence limit applies to
    every unsandboxed outside process.

### 5.2 Case matrix

These are endpoint-level local cases, labeled `L-LOOP-MS-n`, because
FX-PIPE-01 has no network subjects. From v0.8 (node B5) MS-14…MS-27 run
through the one destination flow of §5.3 (DF-3 allowing step, DF-4 check
point, DF-6 request state); MS-24…MS-27 are new. MS-14…MS-23 are the host-agent
destination cases that V4-EXM-23, as amended by SCA-V4-001, examines:
destinations allowed in advance or when the agent asked during its work; a
declined request reported as "destination not allowed by the person";
nothing else contacted; every destination contacted recorded and shown;
and an unsandboxed outside process examined within its stated limit.

| Case | Setting / stimulus | Expected | Evidence for a host claim |
|---|---|---|---|
| MS-01 | Local chosen; nothing else allowed; the person asks for an OP-C1 read of R-100 | Only the configured local server is contacted, and the contact is recorded and shown with "model choice" as its allowing entry (NW-2, NW-9, NW-15; V4-HOST-02 as amended, DEC-5) | Observed destinations with configuration (V4-EXM-01/23) |
| MS-02 | Unconfigured (no choice made) | No request; a notice asks the person to choose; no default is applied; no fallback. The run is recorded as **run not started — no model selected**, with no destination entry (R15-1; F-2 (a); RS-v0.8 §4 R1, `run_opened` with `notStarted`) | Observed absence: the loop's own configuration state at start (R15-1) |
| MS-03 | Cloud chosen, key supplied | Chosen endpoint via the native layer; key not visible to script | Native trace; script inspection |
| MS-04 | Cloud chosen, no credential (no key and no sign-in) | No request; failure reported | Observed absence |
| MS-05 | Model output asks for another endpoint | Refused; setting unchanged; event | Setting before/after |
| MS-06 | Local or cloud chosen (any model mode); analytics not turned on; a test-double library attempts a telemetry request (`L-LOOP-MS-06`) | Refused by the native layer (DF-3 A-2, "always-off item"; DF-4 (c)); nothing sent (NW-2, NW-14; V4-HOST-02 as amended, DEC-5). The refusal recorded as `boundary_refusal` (**recording PROPOSED**, R11-5, R12-10: no accepted text says a refusal is recorded) | Native refusal plus capture |
| MS-07 | Script attempts to read the key or the sign-in credential | Not available | Script inspection |
| MS-08 | Cloud authentication error: key rejected, or sign-in expired or revoked | Reported without credential content; no switch to local; only the person signs in again or supplies a key | Error, event, record |
| MS-09 | Local server unreachable | Failure; no cloud switch | Destinations; event |
| MS-10 | Person switches cloud → local | Only local afterwards; change attributed to the person | Destinations; setting record |
| MS-11 | "Local" endpoint on another machine: the person chose "local" and configured a model server they control on another machine of their network (released at v0.8 by R12-7) | Contacted as the selected model service through the native layer; recorded and shown with allowing entry "model choice" and class **local**, as the person's choice states it. No gate on where the server runs; no class inferred from its address; no fallback if it is unreachable (MS-09) (NW-1, NW-9, NW-15; R12-7) | Native trace; destination record with class; setting record |
| MS-12 | Cloud chosen, signed in (OAuth) (R8-9) | Chosen endpoint via the native layer; the sign-in credential is not visible to script; the sign-in itself was the person's act | Native trace; script inspection; setting record |
| MS-13 | The agent asks to switch to cloud, or to sign in (R8-9; NW-4) | Shown as the agent's request only; no sign-in started; setting unchanged | Setting before/after; event |
| MS-14 | Allow-list hit by category (R8-13): web access switched on; the agent's tool fetches web destination W-1; local or cloud chosen | Contacted through the native layer. Recorded and shown with destination W-1, category web access and allowing entry "category: web access" (NW-8, NW-15) | Native trace; destination record; panel display |
| MS-15 | Allow-list hit by named entry (R8-13): MCP servers switched off; named entry M-1, a server that follows the stateless MCP revision 2026-07-28 | M-1 started and contacted; recorded with the named entry as its allowing entry (NW-8, NW-10, NW-15). This expectation follows NW-8 as settled by DECISION-K1 K1-5 (`N-OPEN-4` closed; V10 N-4); it is unchanged from the interim reading | Native trace; destination record |
| MS-16 | In-work grant, **once** (R8-13): API destination A-1 is not allowed; the agent asks (A8, scope sought: once) while two other calls are in progress; the person grants once | Only the requesting call waited; the other calls ran meanwhile. The one request to A-1 is sent; a later request to A-1 asks again. Recorded: the A8, the grant (scope once, time, source in-work) and the contact (NW-11, NW-12, NW-15) | Event order; destination record; human-act record |
| MS-17 | In-work grant, **this run** (R8-13): as MS-16, granted for this run | A-1 allowed until the run ends. After run end, and in a run that continues it, A-1 is not allowed (NW-11) | Event order; destination record |
| MS-18 | In-work grant, **always** (R8-13): as MS-16, granted always, for the category "other APIs" | The category "other APIs" is switched on in the allow list, with source "in-work" and its time; later requests in that category need no request, the switch allowing everything in the category (NW-8 as settled by DECISION-K1 K1-5; NW-11) | Allow list before/after; human-act record |
| MS-19 | Decline (R8-13): as MS-16, the person declines | Nothing sent to A-1; the request call's deferred outcome is class 2 "destination not allowed by the person" (DF-6); its other work continued; request state *declined*; the act-declined event of kind A12 recorded, and the `destination_declined` entry (**recording PROPOSED**, R12-10) (NW-12, NW-13) | Agent-visible result; destination record |
| MS-20 | Non-stateless MCP server refused (R8-13): configured server M-2 does not follow the stateless MCP revision 2026-07-28; the agent asks for it | M-2 has no stateless evidence (DF-7: its discovery answer lists no 2026-07-28, or it answers as a legacy server); not offered on the allow list; the destination request ends *not granted* ("not grantable", DF-3 A-3) with class 2 "destination not allowed" (not stateless MCP (2026-07-28)); not started; nothing sent; refusal recorded "not stateless MCP (2026-07-28)" (**recording PROPOSED**, R12-10) (NW-10) | Allow-list surface; native refusal; record |
| MS-21 | Outside process, network not observed (R8-13): allowed stateless MCP server M-1, not sandboxed, declares destination D-1 | M-1 started; declared destination D-1 recorded; evidence limit "process network not observed"; no claim that M-1 contacted only D-1 (NW-16) | Process record; declared destinations |
| MS-22 | Agent self-grant (R8-13): the agent writes an allow-list entry, or its model text states a grant | Refused; list unchanged; at most shown as the agent's request (A8); never a grant (NW-11) | List before/after; event |
| MS-23 | Disallowed destination (added at v0.7 for SoW AC-001's "a disallowed-destination case"): web access switched off; no named entry and no in-work grant covers web destination W-2; the agent's tool attempts W-2 without asking | Refused by the native layer at V-D (DF-3 A-7, "not allowed"; DF-4 (b)); nothing sent; the call receives class 2 "destination not allowed" (reason not allowed; reporter native layer; not dispatched), which offers a destination request (DF-6; TL-2, closed at v0.8). "Destination refused at boundary" recorded with reason "not allowed", stage V-D (§2.3; NW-7, NW-15; **recording PROPOSED**, R11-5, R12-10: V4-ARC-12 records destinations contacted). The agent may then ask (NW-11; MS-24) | Native refusal; destination record |
| MS-24 | Request with a carried call (v0.8, node B5): after MS-23 the agent calls the destination request entry for W-2 (web access), scope once, carrying its fetch of W-2, while a read of R-100 runs | Interim notice for the request call; only the carried fetch waits; the read completes. The person grants once; the control establishes it; the carried fetch passes V-D (A-6) and is dispatched unchanged; its outcome is the request call's deferred outcome; the grant is consumed. Recorded: `destination_requested`, the A12, `destination_grant` (once, in-work), `destination_contacted` ("in-work grant: once") (DF-5 Q-1…Q-7) | Event order; destination record; human-act record |
| MS-25 | Unanswered at end (v0.8, node B5): as MS-24, but the person cancels the turn while the request is pending; separately, the run ends while it is pending | No grant; the carried fetch not sent; no deferred outcome; request state *unanswered at end* (turn cancelled · run ended); `destination_request_closed` recorded; the prompt no longer offers choices (PANEL FD-4) (DF-5 Q-9; DF-F6, DF-F7; NW-13) | Event order; destination record |
| MS-26 | Stateless evidence (v0.8, node B5): (a) MCP server M-1 answers the host's discovery request with supported versions including 2026-07-28, and the host sends it only per-request metadata of that revision; (b) M-3 answers discovery with an error that is not a modern error (a legacy server); (c) HTTP server M-4 answers with a session identifier | (a) M-1 may be allowed; its `outside_process` entry carries SE-1, SE-2 and the limit "stateless revision declared, not verified". (b), (c) not stateless: not offered, not grantable, not started; entries they serve refused at V-D "not stateless MCP (2026-07-28)" (DF-7; DF-F10) | Discovery exchange; process record |
| MS-27 | Prompt and control failures (v0.8, node B5): (a) the host's control cannot show the prompt; (b) the person grants and the control refuses the grant; (c) the control's confirmation is lost after the person grants | (a) *not granted* ("prompt not shown"), class 2 "destination not allowed"; (b) *not granted* ("grant refused by control: ‹reason›"), class 2; the refused A12 recorded, establishing nothing (AS DG-4); (c) the carried call not sent while the grant is *unconfirmed*; the request stays pending (DF-F4, DF-F5; AS DG-5) | Control trace; destination record; settings-in |

### 5.3 The destination flow — one account (v0.8, node B5; S1-D LOOP item 5)

This is the one account of a host agent's network destinations that ACT,
AS, RS, PANEL, C, P and ADAPTER cite. Its elements are named **DF-1…DF-10**
and its failure rows **DF-F1…DF-F12**. The rules of §5.1.1 (NW-8…NW-16)
stand; this section says how they run. Every structure here is
**PROPOSED** unless a cited text or ruling decides it. Recording a declined
or refused request is PROPOSED everywhere (R12-10): V4-HI-70 and V4-ARC-12
record destinations **contacted**, and V4-EXM-23 says a declined request
"reaches no destination and is reported to the agent", not that it is
recorded.

**DF-1 Tool subject: host catalog entries, not a second tool source.**
A tool that reaches a network destination is a **host catalog entry**
(V4-ARC-13, SETTLED; TL-1: "The loop never invents a tool without a catalog
entry"). Two things are added to the entry, both PROPOSED in C-v0.8 §3.4:

- The **external-contact declaration** (a sub-element of element 5,
  effects): the destination category (web access · MCP servers · other
  APIs · …); the destination form, *fixed* (the named destinations) or
  *from argument* (the argument whose value names the destination); and,
  where an outside process serves the entry, that process (for an MCP
  server, its server identity, DF-2). An entry without the declaration
  declares no network contact; traffic a host operation makes without
  declaring it stays `UNRESOLVED{N-OPEN-3}` and is refused at contact
  (DF-4 (c)) unless allowed.
- The **destination request entry**, an entry kind the host supplies on the
  embedded surface wherever it offers an entry with an external-contact
  declaration. Class *none*; effects *none*; it contacts nothing and
  changes no host object. Its input: the **target** (a destination or a
  category), the **purpose**, the **scope sought** (once · this run ·
  always) and, optionally, the **carried call**: the operation reference
  and argument text of one call to an entry with an external-contact
  declaration. A request with scope *once* must carry a call (ACT ND-A2:
  *once* is consumed by the one requesting call).

A call to the destination request entry is the agent's **A8 destination
request** (NW-11; ACT §2.7); **the requesting call** of NW-12 is that call
together with the call it carries. An MCP server's tools reach the agent
only as host catalog entries whose declaration names the server: the loop
never reads an MCP server's own tool list. So no second tool source is
needed, and V4-ARC-13's "Tools from the host's capability catalog" holds
(finding G-13).

**DF-2 Destination identity.** A destination is the pair {category,
destination name}, both taken from the entry's external-contact declaration
(and, for the *from argument* form, from the schema-conformant argument
value), never from model text. The destination name is:

| Category (open list) | Destination name |
|---|---|
| Web access; other APIs | The origin: scheme, host and port. Path and query are not part of the identity |
| MCP servers | The server identity: for a local (stdio) server, the launch identity the host configured; for a remote server, its endpoint origin |
| Model service (not a list category; NW-9) | The endpoints of the person's model choice; for a chosen cloud model, its sign-in service (which endpoints: `UNRESOLVED{N-OPEN-2}`) |

Matching is equality of the pair. No wildcard or pattern is defined in
Phase 1. The same origin declared under two categories is two
destinations. The category is the host's declaration, never the agent's.

**DF-3 The allow rule (NW-8 with DECISION-K1 K1-5; NW-9, NW-10, NW-14).**
The native layer decides a pair (c, d) against the settings in force, in
this order; the first step that applies decides:

| Step | Condition | Result, and the allowing entry recorded |
|---|---|---|
| A-1 | d is the selected model service or its sign-in service | Allowed: "model choice", with the class local or cloud (NW-9; R12-7) |
| A-2 | The traffic is an always-off item (analytics or usage reporting; a silent switch to another model or provider; a background download or update) | Allowed only if the person turned that item on; otherwise refused, reason "always-off item", whatever the category switch says (NW-14; the order is DERIVED from V4-HOST-02, "Nothing else is contacted … unless the person turns it on") |
| A-3 | c is MCP servers and d has no stateless evidence (DF-7) | Refused, reason "not stateless MCP (2026-07-28)"; **not grantable** (NW-10) |
| A-4 | A named entry (c, d) is in the allow list | Allowed: "named entry". A named entry is allowed on its own, whatever its category switch (SETTLED, K1-5) |
| A-5 | The category switch c is on | Allowed: "category: c" ("allow everything in this category", SETTLED, K1-5) |
| A-6 | An in-work grant **in force** (AS §3.1 DG-3) covers d or c: *once* only for its carried call; *this run* within the same run | Allowed: "in-work grant: ‹scope›, ‹time›". An *always* grant has become a named entry or a switch (AS DG-9) and is found at A-4 or A-5 |
| A-7 | None of the above | Refused, reason "not allowed" |

Only the person's A12 changes the settings A-2…A-6 read (ACT §2.7); an
*unconfirmed*, *pending* or *refused* grant allows nothing (AS §3.1).

**DF-4 Where the check sits.** Three points, each decided by the native
layer (NW-7; V4-ARC-12):

- (a) **Model request.** Before any model request (§3; F-2, F-3). Only A-1
  applies.
- (b) **V-D, the destination check of a call** (§6). After V-3 and before
  the kind (a) checkpoint step and dispatch, for a call to an entry with an
  external-contact declaration and for the carried call of a destination
  request. A call that fails V-1, V-2 or V-3 never reaches V-D, so nothing
  is refused or asked for a call that could not have run. V-D sits after
  V-3 because the destination is known only from a schema-conformant call,
  and before dispatch because "a declined request reaches no destination"
  (V4-EXM-23) and the requesting call "is not sent until the person
  answers" (NW-12).
- (c) **At contact.** Every network request the host makes for its agent
  (a dispatched operation, an outside process being started, the model
  request) passes the native layer, which applies DF-3 again, writes the
  contact (RS R15 `destination_contacted`) **before** sending, and does
  not send if it cannot write it (F-4; DF-F2), or refuses (RS
  `boundary_refusal`, stage *at contact*, recording PROPOSED). A refusal at
  contact after dispatch reaches the agent as the host outcome the host
  reports (class 2 *error* or *application error* with its effect
  statement).

**DF-5 The in-work request, step by step** (NW-11…NW-13; ACT §2.7; AS §3.1).

| Step | What happens | Record (RS R15) | Failure |
|---|---|---|---|
| Q-1 | The agent calls the destination request entry (its A8): target, purpose, scope sought, carried call | — | — |
| Q-2 | The loop runs V-1…V-3 on the request call and, against its own entry, on the carried call | — | Class 1 for the request call; nothing is asked |
| Q-3 | The native layer applies DF-3 to the target (and to the carried call's destination). Already allowed: no prompt and no request recorded (§3.2); the carried call goes on to dispatch and its outcome is the request call's result, or class 3 "already allowed" without a carried call. Not grantable (A-3; an always-off item, which only an allow-list edit turns on): state *not granted*, reason "not grantable" | `destination_requested`; `destination_request_closed` (*not granted*) | — |
| Q-4 | Otherwise the loop records the request and the host's control shows the prompt (PANEL ND-2). State **pending** | `destination_requested` | DF-F3, DF-F4 |
| Q-5 | The loop returns to the model, for the request call, an **interim notice**: "waiting for the person's answer on ‹target›" (a loop state, not a result class, as TL-3 states for a held call). Only the carried call waits; the agent's other calls go on (NW-12). A turn whose request is still pending does not complete: after the model's last response it waits in *awaiting destination answer* (§3.2) | — | — |
| Q-6 | The person answers through the host's control, never through a panel input (PANEL §3.9): a grant (A12, network-destination grant, once · this run · always, for the destination or its category) or a decline (act-declined event of kind A12) | `human_act` or `act_declined` (R9); `destination_grant` once the control establishes it | DF-F5 |
| Q-7 | **Granted** and the grant **in force**: the carried call passes V-D (A-6) and is dispatched unchanged; its host outcome (class 2, 3 or 4) is the request call's **deferred outcome**. With no carried call, the deferred outcome is class 3 "granted: ‹scope›". A grant the control refuses: *not granted*, reason "grant refused by control: ‹reason›" (AS DG-4) | `destination_contacted` at contact; `destination_request_closed` (*not granted*) on refusal | DF-F2, DF-F8 |
| Q-8 | **Declined**: nothing is sent; the deferred outcome is class 2 **"destination not allowed by the person"** (reporter: the host's control) | `destination_declined` (recording PROPOSED, R12-10) | — |
| Q-9 | **Unanswered at end**: the run ends, or the person cancels the turn (F-11), while the request is pending. No grant; the carried call is not sent; no result is delivered, because no further model request follows in that turn. Never a grant by silence (NW-13) | `destination_request_closed` (*unanswered at end*) | — |

**The wait, and ending the turn (R13-5; INTEGRATION; v0.8, RP-4).** The
call that needs the destination (the carried call) waits for the person's
answer. That wait is the grant being sought (V4-HOST-02: "when the agent
asks during its work"), not a checkpoint hold, so DECISION-4 does not bear
on it (NW-12; ACT ND-A3; G-8). The loop may continue other work in the
turn: the agent's other calls go on (Q-5). The person may end the turn
while the request is pending; the request then closes **unanswered at end**
(cause turn cancelled; Q-9, DF-F6): no grant is made and the carried call is
not sent. The run's end closes it the same way (cause run ended; DF-F7).

The deferred outcome is delivered with the next model request of the same
turn as a message of speaker kind *tool result* naming the request call's
correlation identity (§2.1). FB-CC-1 has no member for a second result to
a call already answered: this representation is an **inference**, PROPOSED,
for the product left to DEP-05-01-024 (G-13).

**DF-6 Request states and TL-2.** A destination request is in exactly one
state: **pending** → **granted** (once · this run · always) · **declined** ·
**not granted** (reason: not grantable · grant refused by control · prompt
not shown) · **unanswered at end** (cause: run ended · turn cancelled).
Transitions are §3.2; the grant that answers a request has its own states
(AS §3.1). The request call receives the interim notice (not a result
class) and then **at most one** result, always in TL-2's four classes:

| Request outcome | Result of the request call | TL-2 class | Reporter |
|---|---|---|---|
| Granted, with a carried call | The carried call's host outcome, or *outcome unknown* | 2, 3 or 4 | Host / loop (observer) |
| Granted, no carried call | "granted: ‹scope›" | 3 | Host's control |
| Declined | "destination not allowed by the person" | 2 | Host's control |
| Not granted | "destination not allowed" with the reason | 2 | Native layer or host's control |
| Unanswered at end | None (the turn or run is over); the carried call's tool-call state is "not dispatched: destination request unanswered" | — | Loop |

A **direct call** that fails V-D gets class 2 **"destination not allowed"**
with its reason (not allowed · always-off item · not stateless MCP
(2026-07-28)), reporter the native layer, not dispatched. Where the reason
is "not allowed" the result says that the agent may ask (a destination
request is *offered*, as TL-5 offers an A8); nothing is asked in the
agent's place (NW-11). Both "destination not allowed" results are C-v0.8
§4.1 rows.

**DF-7 Evidence that an MCP server is stateless (closes `N-OPEN-5` as
PROPOSED).** Source: the published MCP specification, revision 2026-07-28
(https://modelcontextprotocol.io/specification/2026-07-28, source files at
https://github.com/modelcontextprotocol/modelcontextprotocol,
`docs/specification/2026-07-28/`, commit
`046fa30efd374370afb87ef830bd788eac5f217e`, the `main` head at retrieval;
read-only, 2026-09-30 18:42 UTC; DECISION-K1 K1-6). Passages relied on
(sha256 of each source file in G-15):

- `basic/index.mdx`, Statelessness: "all the information needed to process
  a request is contained in the request itself"; servers "**MUST NOT** rely
  on prior requests over the same connection to establish context".
- `server/discover.mdx`: "Servers **MUST** implement it"; the result's
  `supportedVersions` lists "Protocol versions the server supports"; and
  "`serverInfo` is self-reported … Clients … **SHOULD NOT** rely on it for
  security decisions."
- `basic/versioning.mdx`: "Legacy: protocol versions that establish a
  session with an `initialize` handshake (`2025-11-25` and earlier)"; a
  dual-era server serves "a request carrying modern per-request `_meta`
  … statelessly according to this revision".
- `basic/transports/stdio.mdx`, Backward Compatibility: a probe answered by
  "any other error, or does not respond within a reasonable timeout" means
  "the server is legacy".
- `basic/transports/streamable-http.mdx`: a server of this revision, sent
  an `Mcp-Session-Id`, should "ignore it, and do not mint or echo session
  IDs".

What LOOP accepts as evidence, per server configuration (DF-2 identity):

- **SE-1** The host's own `server/discover` request to that server returns a
  result whose supported versions include `2026-07-28` (or a modern
  unsupported-version error whose supported list includes it).
- **SE-2** The host speaks to that server only with per-request metadata of
  revision 2026-07-28 and never sends `initialize`, so a dual-era server is
  served statelessly (versioning.mdx).
- **SE-3** On HTTP, no response from that server carries a session
  identifier; one that does is counter-evidence, and the server is treated
  as not following the revision.

Not evidence: the server's self-reported name or version, its
documentation, a configuration flag, or the agent's word. A probe that
fails, times out or answers as a legacy server gives *not stateless*. The
evidence is recorded with its time on the `outside_process` entry (RS R15)
and re-probed when the server's configuration changes or a later request
fails the assumption (the specification says clients "SHOULD cache the
result for the lifetime of the server process (stdio) or origin (HTTP)").
**The limit, stated plainly:** SE-1…SE-3 show that the server declares and
speaks the stateless revision; they do not show that it keeps no state
between requests. The record carries the evidence limit **"stateless
revision declared, not verified"** (RS R11). A server without SE-1 and SE-2
is refused at A-3.

**DF-8 Record elements (RS-v0.8 R15, R11; `RS_RECORD.schema.json`).**
`destination_requested` (Q-3, Q-4); `destination_grant` (Q-6);
`destination_contacted` (DF-4 (c)), with the model service's class local or
cloud (A-1); `destination_declined` (Q-8; recording PROPOSED);
`boundary_refusal` with its stage (model request · V-D · at contact) and
reason (recording PROPOSED); `destination_request_closed` (Q-3, Q-7, Q-9;
PROPOSED element); `outside_process` with its stateless evidence (DF-7);
the R11 limits "process network not observed", "destinations not observed"
and "stateless revision declared, not verified". Settings-in carries the
allow list, in-work grants and requests with the DF-6 states (AS §6 = RS
§8). The loop's events (§2.3) map to these entry kinds (RS §13.3).

**DF-9 Displays, and who owns them.**

| Display | Owner of the display meaning | Host-panel receiving |
|---|---|---|
| Allow list, in-work grants and their states | DEL-04-02: AS §3, §3.1 | PANEL §3.8 ND-1, ND-5 |
| **Destinations contacted** (with declines and refusals shown apart) | **DEL-04-02: AS §3.2** (DERIVED), because DEL-04-02's ScopeOfWork CLM-002 consumes "a host agent's … contacted-destination record, which `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5` requires to be shown" (register row DEP-04-02-018) | PANEL §3.8 ND-4, presenting AS §3.2 as ND-5 presents AS §3 |
| The in-work prompt and its states | PANEL §3.8 ND-2 (prompt states PS-1…PS-6 over DF-6) | — (the prompt is the host's control; PANEL states what the panel must present) |
| Decline wording | ACT §2.7 ("destination not allowed by the person") | PANEL ND-3 |

The rules and the record are this file's (§5.1.1) and RS R15. Whether
DEL-05-02's ScopeOfWork should name the panel's destination surfaces stays
the owner's question (PANEL F-12); nothing here changes a ScopeOfWork.

**DF-10 Verification.** MS-14…MS-27 (§5.2) are the cases. The prototype
`prototype/destination_flow.py` runs DF-3, DF-4 (b), DF-5 and DF-6 on a
scripted native layer and control, emits RS entries and checks them
against `RS_RECORD.schema.json`, and checks the loop's request records
against `LOOP_DESTINATION_REQUEST.schema.json` (§11; VC-10).

**Failure rows.**

| # | Step | What fails | Who reports | Record left | What happens next |
|---|---|---|---|---|---|
| DF-F1 | V-D | The native layer cannot read the settings in force, or only an *unconfirmed* grant would allow | Native layer | `boundary_refusal` (stage V-D, reason "not allowed"); recording PROPOSED | Refused (fail closed); class 2 "destination not allowed" |
| DF-F2 | At contact | The contact record cannot be written | Native layer | The refusal, when it can be written | Not sent (F-4); the operation's outcome as the host reports it; for the model request, turn failed |
| DF-F3 | Q-4 | The request record cannot be written | Loop | None until the record accepts writes | No prompt is raised; F-10 applies (no further dispatch until a dispatch can be recorded) |
| DF-F4 | Q-4 | The host's control cannot show the prompt (no control, no panel attached) | Host's control / loop | `destination_request_closed` (*not granted*, "prompt not shown") | Class 2 "destination not allowed", reason "prompt not shown"; nothing is granted |
| DF-F5 | Q-6 | The control's confirmation of a grant is lost (AS DG-5, *unconfirmed*) | Host's control | Grant state *unconfirmed* in settings-in | The carried call is not sent; the request stays pending until the grant is in force, the run ends or the turn is cancelled |
| DF-F6 | Q-5 | The turn is cancelled while pending | Person (panel return input) / loop | `destination_request_closed` (*unanswered at end*, turn cancelled) | F-11; nothing sent |
| DF-F7 | Q-5 | The run ends while pending | Loop | `destination_request_closed` (*unanswered at end*, run ended) | Nothing sent; PANEL FD-4 |
| DF-F8 | DF-4 (c) | The dispatched operation reaches a destination it did not declare | Native layer | `boundary_refusal` (stage at contact); recording PROPOSED | Not sent; the host outcome as reported; `UNRESOLVED{N-OPEN-3}` for whether such traffic is the agent's |
| DF-F9 | Outside process start | The process is not sandboxed | Host | `outside_process`; R11 "process network not observed" | Started if allowed; nothing claims it contacted only what it declared (NW-16) |
| DF-F10 | DF-7 | Discovery fails, a legacy answer, or a session identifier appears | Host | `outside_process` evidence "not stateless"; `boundary_refusal` reason "not stateless MCP (2026-07-28)" | Server not started; entries it serves refused at V-D; not grantable |
| DF-F11 | Record of contacts | The native layer reports no destinations for the run | Host (through the loop) | R11 "destinations not observed" | Shown as that limit, never as "no destinations contacted" (AS §3.2) |
| DF-F12 | Deferred outcome | The model interface fails before the deferred outcome is delivered | Loop | The outcome stays recorded; model interface failure | Turn failed (F-5, F-6); the outcome is not re-sent in another turn |

## 6. Validation order, treatment and dispatch

SETTLED: catalog-schema checking comes before the host's validation
(V4-ARC-13), and there is one route (V4-HI-20). INTEGRATION (R-3.1):
treatment is resolved on the host route at validation and again at
application. The loop relays intent.

| Step | Check | By | On failure |
|---|---|---|---|
| V-1 | Parse completeness (§7) | Loop | Class 1 "malformed/truncated" |
| V-2 | The named operation is an entry of the catalog edition offered to the loop | Loop | Class 1 **not offered** (R2-4). Never dispatched |
| V-3 | Input schema of the offered entry version | Loop | Class 1 "schema" |
| **V-D** (v0.8, node B5; PROPOSED) | Destination check, for a call to an entry with an external-contact declaration and for a destination request's carried call: DF-3 against the settings in force (§5.3 DF-4 (b)) | Host native layer, consulted by the loop before dispatch | Class 2 **destination not allowed** (reason), not dispatched; or, for a carried call, the call waits for the person's answer (NW-12; DF-5) |
| V-4 | Host validation: exposure on this surface; availability re-evaluated; preconditions; basis currency; entry version; domain rules | Host route | Class 2: **not exposed on this surface** (host-reported, relayed); unavailable (declared precondition, HI-04 parity); refused — invalid (element-7 error); refused — stale (both bases); error, including entry-version mismatch (C element 7, U-C6) |
| V-5 | Treatment and application or proposal | Host route | Class 2 *not permitted* (naming the treatment, the policy record or the governing checkpoint constraint); application error (effect none/partial/unknown); or a class 3 outcome |

### 6.1 Receiving requirements

- O-1. V-3 always runs before V-4. A call that fails V-1 to V-3 never reaches
  V-D or V-4. V-D runs after V-3 and before dispatch, so V-4 never sees a
  call to a destination that is not allowed (v0.8; §5.3 DF-4).
- O-2. A schema-conformant call is not validation, application or a human act
  (SoW REQ-003).
- O-3. The dispatch carries the catalog edition and entry version offered.
  An optional pre-screen may report "offer out of date" on the loop side.
  An entry-version mismatch is a host error (C element 7; U-C6).
- O-4. Treatment → outcome map, consumed from ACT §6 (INTEGRATION, R-3;
  R2-4):
  - direct without an effective direct treatment → *not permitted*, never
    converted;
  - reserved → *not permitted*, and an A8 request is offered;
  - **no policy basis** → direct *not permitted*, proposing available
    (INTEGRATION, R-3.5). Proposing confers no permission. Any effect
    requires A5 and host application. Dependent production stays held
    (REQ-004; R2-9);
  - widening never converts a queued proposal.
- O-5. Standing at drafting (the grant in force carried on dispatch) and the
  host-reported treatment at resolution (validation, application) are both
  recorded when they differ (R-3.6).
  - Narrowing leaves a queued proposal unaffected.
  - An unapplied operation is re-resolved at application (DEP-001).
- O-6. **Grant states carried** (R-8; R2-6):
  - effective (person-set);
  - **effective (policy default)**;
  - requested by agent;
  - set by person, not yet confirmed by control;
  - unconfirmed;
  - not set;
  - refused (reason).

  The direct branch applies only in an *effective* state whose grant value
  is direct. *Effective (policy default)* opens direct only if the policy
  record's default is *direct*; no such default exists in the first increment
  (the SWB default is *propose*). The host route decides; the loop carries.

### 6.2 Dispatch record (every dispatch)

| Element | Meaning |
|---|---|
| Origin | Author type (agent); author identity (seat); channel (embedded); conversation; run identity; workflow identity tuple; holding library (V4-HI-21; P §3.3) |
| Seat role meaning | Per §2.1, or *unknown* |
| Grant in force | As AS-v0.8 §12.1 defines it for DEP-05-01-025: the settings version identity in force at route decision; for the operation's class its grant value, display state (O-6), scope and policy-class record reference; for a call with an external-contact declaration, the destination settings version in force. As last observed: "grant in force: unconfirmed" when the control's confirmation is lost, "grant in force: not received" when no report arrived; no default is assumed (AS §12.1; v0.8, RP-4) |
| Requested mode | Apply directly or propose, as the call or the entry's meaning expresses it |
| Governing checkpoint constraint | Per C-6, where applicable (R2-12) |
| Relied-on basis | As cited, with method designations; per-target subject content identities |
| Catalog edition and entry version | O-3 |
| Proposal identity | The existing identity for a resubmission (§6.3); otherwise per DEL-03-02. With it, the party that minted it (*proposer-minted* or *host-minted*, P-v0.8 §3.5 PM-1) and any host handles associated with it (PM-2), never in its place (v0.8, RP-4) |
| Reason | The proposer's reason (P §3.3) |
| Correlation identity | The model's call identity |

### 6.3 Retry, resubmission and re-draft

- R-a. **Retry keeps the proposal identity** (R-7; P §3.1). A resubmission,
  whether by the loop after a transport failure or by the agent citing the
  proposal identity, carries the same identity and unchanged content. The
  loop never mints a new identity for a retry.
- R-b. **De-duplication precedes the basis check** (R2-13, INTEGRATION).
  - A resubmission of a known proposal identity returns that proposal's
    recorded state or outcome, e.g. the applied association with RC-1 at
    T13.
  - It is never refused as stale because of its own effects.
  - One effect per identity is a host obligation to be evidenced (DEP-001,
    §13 Q-6). Each submission is recorded with only observed effects.
- R-c. **Per-item basis check** (R2-13, as amended by R8-3). Where the host
  supplies subject identities, staleness compares the **subject content
  identities of the item's relied-on targets**, not the global revision.
  Applying sibling items of the same proposal does not make remaining items
  stale unless they share targets. Where the host supplies no subject
  identities, the loop receives and relays the **host's stated staleness
  scope** and never narrows it. For SWBPIPE that scope is the whole model:
  any model change stales every queued proposal (SQ-07 (d)). De-duplication
  first (R-b) is unchanged. The host rule is still U-C3.
- R-d. **After outcome unknown**, the loop seeks observation before
  resubmitting. It observes the proposal by its identity (P-v0.8 §3.5
  PM-4) and follows P §4.7 SQ-P6's order: a recorded state is reported
  separately and needs no resubmission; *not known to host* within the
  host's de-duplication scope allows a retry with the same identity and
  content; outside the scope, or with no scope stated, one effect stays
  unevidenced, and under *apply directly* there is no retry (v0.8, RP-4).
  Representation and encoding stay DEL-03-02 TBD-002.
- R-e. **A re-draft is a new proposal** with lineage, a fresh read and new
  change-item content identities, as for T9's PR-2 relative to PR-1. No
  acceptance carries over, and there is no retarget (V4-HI-23).

### 6.4 Receiving notes from SWBPIPE's answers (R8-3, R8-4, R8-5, R8-10)

These notes say how this contract would receive SWBPIPE's current terms.
They rest on SWBPIPE's answers about its current state (SQ-03, SQ-07,
SQ-09…SQ-11, SQ-31). They are not host evidence, and host joins are
deferred (DECISION-3). SWBPIPE has no loop today (SQ-20).

- RN-1 **Staleness scope (R8-3).** Per §6.3 R-c: the host's stated scope is
  received and shown, never narrowed. SWBPIPE's scope is the whole model.
- RN-2 **Whole-model identity (R8-4).** A host's whole-model identity is
  received as the subject content identity of **every** subject it covers
  (TL-4; §2.4.2). This errs toward reporting a lapse and never misses one.
  The loop never computes identities itself. Resulting objects beyond
  target ids are *not supplied*. SWBPIPE does not yet meet V4-HI-32
  (per-subject identity); owner notice, SWBPIPE (PB-TBD-002 / DEL-16-03).
- RN-3 **Outcome mapping (R8-5)**, within TL-2:

  | SWBPIPE term | Received as | Never |
  |---|---|---|
  | `unsupported_method` / `unsupported_change` | Class 2 host-reported *not exposed on this surface*, relayed naming the host as reporter. R2-4 (a named rule) is recorded as not met by this host | *not permitted* |
  | DRAFT #885 `withdrawn` (the person cleared the queue) | Item left the queue, "cleared by the person, no decision record" (item-left event) | A10 or A11 |
  | `validation_rejected` at Apply | *refused — invalid* at application | A10 or A11 |

  Accept and apply are one step on SWBPIPE (Apply), per batch, with no A10
  record. The loop keeps the App's meanings of A5, A10 and A2 (§9) and
  records the missing counterparts. Session undo writes no receipt, so
  "reverses ⟨receipt⟩" is *not supplied* for SWBPIPE (R2-15 and R3-4
  stand; FX-UNDO).
- RN-4 **Strict preflight (R8-10).** The agent never adds a field the host's
  schema lacks. SWBPIPE refuses unknown or missing parameters
  (`invalid_request`) before simulation (SQ-31). This agrees with §7's
  "never coerced; never repaired".

## 7. Malformed and truncated tool calls

SETTLED: truncated or malformed calls are reported failures, never executed as
empty arguments (ARCH §4; SOW-142). These are parse-level local cases,
`L-LOOP-MC-n`, because FX-PIPE-01 has no model-output subjects. From v0.8
each condition is stated in the representation of FB-CC-1 (§4.1; fixture
basis, not a product selection). Every rule below is PROPOSED unless marked
otherwise (R12-7, R12-8). OBS-1's observation of one local server
(§4.1) changes none of them (R13-6).

| ID | Condition (FB-CC-1 representation) | Expected handling | Fixture (§11) |
|---|---|---|---|
| MC-1 | The response ends with termination reason `length` (§4.1 point 2) while any call is in it | Every call of that response fails "truncated", including a call whose text happens to parse, because the response was cut off; not dispatched; three reports. (A per-call reading, dispatching calls whose text parses, was considered and not taken: the model's response is incomplete) | FX-M1, FX-M1b |
| MC-2 | The stream ends with no termination reason, or the transport fails mid-stream | Every call of that response fails "interrupted"; not dispatched; model interface failure (§3.1 F-6) | FX-M2 |
| MC-3 | Complete response; the assembled argument text is not JSON | Failure "malformed" for that call only | FX-M3 |
| MC-4 | Parses, but not the required structured form: the argument JSON is not an object; the item is not a function tool call (e.g. a custom tool call); the deprecated `function_call` form or termination; or no correlation identity was received | Failure "malformed". Where no correlation identity exists, the model result cannot be addressed to the call: only the event stream and the run record receive the report | FX-M4, FX-M4b, FX-M4c |
| MC-5 | Operation reference missing, empty, or not in the offered edition | V-2 **not offered**; not dispatched | FX-M5 |
| MC-6 | "No arguments" (§4.1 point 4). **Closed at v0.8 as PROPOSED:** argument text that parses to an object with no members (`{}`) is a complete call and goes on to V-3 against the entry's input schema. Argument text absent or empty is malformed | Never coerced to empty arguments (SETTLED, ARCH §4) | FX-M6a, FX-M6b, FX-M6c |
| MC-7 | Two calls at different positions share a correlation identity | Failure for both (PROPOSED; uniqueness is within one response) | FX-M7 |
| MC-8 | Several calls in one response, one of them malformed | **R12-7 (INTEGRATION; `T-OPEN-1` closed):** the valid calls are handled on their own, each through V-2, V-3 and dispatch on its own validation; the malformed call gets its own refusal result (class 1) for its correlation identity. This is P-v0.8 §3.1 rule 5 applied to a malformed sibling: each call of a response is its own unit, and **grouping follows rule 5**: sibling calls form separate proposals, unless a call explicitly names an existing proposal it extends; that is the drafter's choice, not a loop merge. OBS-1 observed several well-formed calls in one response (§4.1 point 3) but no malformed sibling, so the rule stays PROPOSED (R12-7). In the governance phase LH-0 is unchanged: siblings not yet dispatched when an arrival is observed are held (§2.4.4) | FX-M8 |
| MC-9 | The loop "repairs" incomplete text | Prohibited. A re-issued call is a new call | FX-M3 (no repair) |
| MC-10 | A later fragment at the same position carries a different correlation identity, name or tool type (new at v0.8) | Failure "malformed" for that call | FX-M10 |
| MC-11 | Termination reason `content_filter` (new at v0.8) | Every call of that response fails "filtered"; not dispatched; the agent message *failed* (§3.1 F-7) | FX-M11 |
| MC-12 | A chunk for a second choice (new at v0.8). Fixtures request one choice (§4.1 point 3) | Outside the fixture basis: every call of the response fails "malformed"; nothing is taken from either choice | FX-M12 |
| MC-13 | A fragment with no position (new at v0.8) | It cannot be attributed to a call: every call of the response fails "malformed" | FX-M13 |

Reports go to three recipients:

1. the model (class 1 result, by correlation identity where one exists);
2. the event stream / panel ("tool call rejected", "not dispatched");
3. the run record (requested; "not executed: rejected before host
   validation", with the rejection kind: *truncated*, *interrupted*,
   *malformed*, *filtered*, *not offered*, *schema* or *offer out of
   date*; for F-11, "not dispatched: turn cancelled"). These are the
   loop-side refusals RS R7 carries (R14-3; RS states the values; v0.8,
   RP-4).

Dispatch observation: zero host-route calls for a rejected correlation
identity. FX-V1 is the valid comparison.

### 7.1 Assembly rules under FB-CC-1 (v0.8; PROPOSED)

- R-F1. Fragments of one call are joined by their **position in the
  response** (FB-CC-1 `index`, the only member a streamed tool-call chunk
  requires; §4.1 point 1).
- R-F2. Argument pieces are appended in arrival order. The assembled text is
  kept exactly as received and is never repaired (MC-9).
- R-F3. The correlation identity, the operation reference and the tool type
  are taken from the fragment that carries them. A later fragment at the
  same position that carries a different value is MC-10.
- R-F4. The termination reason decides the response before any call is
  judged: `stop` or `tool_calls` → each call is judged on its own (MC-3…MC-8,
  MC-10); `length` → MC-1; `content_filter` → MC-11; `function_call`
  (deprecated) → MC-4; none → MC-2. A fragment with no position (MC-13) or a
  second choice (MC-12) rejects every call of the response.
- R-F5. The loop never dispatches a call before its response has
  terminated: a call is judged only once the termination reason is known
  (tool-call state *receiving*, §3.2).

### 7.2 The received tool call record (schema; v0.8; PROPOSED)

`LOOP_TOOL_CALL.schema.json` (JSON Schema 2020-12, beside this file) gives
one record per call after V-1 and V-2: model-interface basis label;
position in the response; call correlation identity; operation reference (a C operation identity of the offered edition; the
same element as `operationReference` in `LOOP_DESTINATION_REQUEST.schema.json`,
whose names follow RS's style because its elements pass into RS R15 entries;
v0.8, RP-4); argument text as received; parsed argument object (only when the text
parsed to an object); parse state (*complete*, *truncated*, *interrupted*,
*malformed*, *filtered*); the response's termination (*tool-calls*, *stop*,
*length-truncated*, *content-filtered*, *deprecated-function-call*,
*ended-without-reason*); and a rejection {step V-1 or V-2, case MC-n,
reason, dispatched = false}, or none. A record with no rejection must have
parse state *complete*, an argument object, a correlation identity and an
operation reference; it then goes on to V-3 on its own (R12-7). The names
are Chirality's own; no wire field is selected. Examples:
`LOOP_TOOL_CALL.example.valid.json` (FX-V1's call) and
`LOOP_TOOL_CALL.example.invalid.json` (a truncated call with no rejection,
which the schema refuses).

### 7.3 Prototype (R12-3; v0.8)

`prototype/assemble_tool_calls.py` (Python 3 standard library; not product
code; README in `prototype/`) reads the stream fixtures in
`prototype/fixtures/stream_fixtures.json`, written in FB-CC-1's chunk shape
with invented content on FX-PIPE-01 identifiers, applies R-F1…R-F5 and
MC-1…MC-13, and checks every output record against
`LOOP_TOOL_CALL.schema.json` with `prototype/schema_subset.py` (a validator
for the schema subset used; its keyword list is in its header).

Run on 2026-09-30, command `python3 assemble_tool_calls.py` in `prototype/`
(Python 3.13.7): **19/19 fixtures gave the expected result**, and every
record validated against the schema. The same validator gives
`LOOP_TOOL_CALL.example.valid.json` VALID and
`LOOP_TOOL_CALL.example.invalid.json` INVALID (oneOf matched no branch).
This shows the rules are consistent and executable on FB-CC-1-shaped
input. Rerun at RP-4 (2026-09-30, same command) with three added fixtures,
OBS1-C1…OBS1-C3, in the shapes OBS-1 observed (§4.1; reasoning and
whitespace content deltas included, observed tool names replaced by
FX-PIPE-01 entries): **22/22 as expected**, every record valid. That
shows the assembly accepts what one local server sent; it does not show
that model servers in general emit FB-CC-1's shapes, and no loop is built;
the §12 standing of the MC cases is unchanged.

## 8. Responsiveness: observation protocol (no numeric thresholds)

SETTLED: the loop does not block the host interface; long parsing and
streaming run off the main thread where needed (ARCH §4). Placement is the
host owner's (`UNRESOLVED{OI-013}`). No threshold is set
(`UNRESOLVED{R-OPEN-1}`).

| ID | Load | Concurrent interaction |
|---|---|---|
| RS-1 | A long model stream (`L-LOOP-RS-1`; no FX-PIPE-01 subject) | Scroll and select in the OP-C1 supports table for R-100; open the LC-1 results view; type in a host field |
| RS-2 | A large read result (`L-LOOP-RS-2`: a large invented model. FX-PIPE-01's four supports are too small, hence the divergence) | The same interactions, during parse and result handling |
| RS-3 | Stream in progress | Cancel. It takes effect, and the interface stays usable |
| RS-4 | Stream during host work (e.g. a new solve of LC-1) | Interact with independent views |

Each observation records:

- the candidate;
- the configuration and date (V4-EXM-01);
- the environment;
- the owner's placement choice;
- each interaction and its account (usable, degraded, blocked or not
  observed);
- any host measurement, as observed;
- limitations.

Verdict form: "continued usability observed for X on candidate Y".

## 9. Distinct acts at the loop boundary

| Act | Actor | What the loop may emit | Never |
|---|---|---|---|
| A1 propose | Agent or person | Dispatch; "queued" | Acceptance |
| A2 apply (direct under grant) | Agent within an effective direct grant; host applies | "applied", branch *direct under grant*, receipt, origin, undo route, later-examination route (T16, RC-2) | Acceptance, checking, approval |
| A2 apply (after acceptance) | Host | "applied", branch *after acceptance*, receipt (T12, RC-1) | Approval |
| Undo (OP-C10) | Actor per its treatment; host applies | "applied", **reverses ⟨receipt⟩** (T17, RC-3 reverses RC-2) | Erasure of earlier records |
| A3 examine | Agent | "examination findings" (T4) | "Checked" |
| A4 mark checked | Person (D2a, SETTLED) | Relayed "human act observed" (T2) | Creation by the agent; inference from findings |
| A5 accept | Person where autonomy requires a proposal (D2b, SETTLED); per item | Relayed decision (T11 item 1) | Inference from success, queue or receipt |
| A6 approve | Person (D2c, SETTLED) | Relayed act only | Any agent statement of approval (V4-AUT-05) |
| A7 rely | Accountable professional (D2d, SETTLED) | Relayed act only | Inference from another act |
| A8 request | Agent | "A8 request issued", only when issued | Performance; automatic creation |
| A9 record | Identified recorder, actor ≠ recorder | Recording mode on relayed acts | Checkpoint satisfaction alone |
| A10 reject | Person wherever A5 is reserved | Relayed with actor (T11 item 2) | "Rejected" for a host refusal |
| A11 withdraw | Proposer | Relayed with actor | — |
| A12 set grant | Person (D2e, SETTLED). Includes the **network-destination grant** subclass (INTEGRATION, R8-13; ACT §2.7) | "Grant change observed" (T15); supersession (R2-7); "destination grant observed" and "destination declined" (§2.3) | A grant change or a destination grant from an A8 |
| A13 enable/disable external access | Person. Enabling: D2e, SETTLED. Disabling as A13: INTEGRATION (R2-3) | Not a loop event (external channel). An agent may request it (A8) | — |
| A14 tool permission | App only | Not applicable in host-loop runs. R13 is not applicable (R2-8) | — |
| A15 register workflow revision (R12-5; v0.8, RP-4) | Person, in the App (ACT-POLICY-v0.8 §2.1; DEL-02-02) | Nothing: not a host-loop act, and no checkpoint may require it in this increment (ACT §4.1) | Inference from a workflow's selection or use |

- A-1. Evidence of one act never establishes another.
- A-2. An agent may request (A8) and prepare. It never records an act as
  performed (V4-HI-31).
- A-3. Relayed acts carry actor, recorder, recording mode and a
  capture-evidence reference. Only capture evidence satisfies a checkpoint.
- A-4. Still open:
  - operation-specific reserved additions (`UNRESOLVED{OI-021}`);
  - host adoption and capture requirements (DEP-001).
- A-5. **Permission layer** (R2-11 attribution):
  - *No classifier permission mode in hosts; the SWB default proposal mode
    applies*: **SETTLED** (D3).
  - *No separate routine tool-permission layer in the host loop. Host
    operation authority is the person's grant plus adopted policy, resolved
    on the host route*: **DERIVED** from D3 with V4-HI-40/41.
  - The loop presents no tool-permission prompts. Nothing in the loop stands
    in for a reserved or professional act.
  - The in-work destination request (§5.1.1 NW-11) is not a
    tool-permission prompt. It is the agent's A8, answered by the person's
    A12 network-destination grant (R8-13; ACT §2.7). From v0.8 the A8 is a
    call to the host's destination request entry (§5.3 DF-1, DF-5).
- A-6. **Phase 1 changes no act rule (R8-1).** The acts above, their actors
  and the reserved list are the same in both phases (LP-5, LP-6). SWBPIPE
  terms map per §6.4 RN-3. A13 stays a reserved act; SWBPIPE has no
  enablement facility, so A13 cannot be evidenced there (SQ-28; R8-6).

## 10. Owner-allocation and open-choice account (OUT-004)

### 10.1 Responsibility map

| Responsibility | This DEL-05-01 | Other App-v4 owner | External host (SWBPIPE) | Open issue / point of need | Standing |
|---|---|---|---|---|---|
| Loop receiving requirements, fixtures, cases | Owns | — | Receives through relay | — | v0.8 draft |
| Loop construction, placement, parsing, persistence | Excluded; requires outcomes only | — | Owns and selects | OI-013 | Owner-reported building (DEP-001); SWBPIPE answers (2026-09-28): no live agent in the product (A-1); agent-facing work (UI-SUCCESSOR) deferred by the owner; draft PR #885 unmerged and deferred (A-2). No embedded loop exists or is selected (SQ-20, SQ-29) |
| Panel assembly | Excluded | DEL-05-02 (receiving) | Owns | OI-013 | Open |
| Native networking, endpoint, credential (key or OAuth sign-in); allow list, in-work destination prompt and destination record (R8-13) | Excluded; defines §5 cases (§5.1.1) and the destination flow (§5.3, v0.8) | ACT §2.7 (act); AS §3, §3.1 (grant display) and §3.2 (destinations-contacted display, v0.8; §5.3 DF-9); RS R15 (record); C §3.4 (external-contact declaration; destination request entry) and §4.1 (the two "destination not allowed" results); PANEL §3.8 (receiving) | Owns | N-OPEN-2…3 (N-OPEN-1 closed by R12-7; N-OPEN-4 by DECISION-K1 K1-5; N-OPEN-5 closed as PROPOSED at v0.8, §5.3 DF-7) | Answered 2026-09-28: none exists (SQ-29, SQ-30 (a)); not host evidence. The DECISION-5 rules are not relayed (host joins deferred, DECISION-3) |
| Treatment resolution, exposure evaluation, de-duplication | Excluded; relays | ACT (policy), C/P | Host route | DEP-001; §13 | Not received |
| Catalog, read basis, exposure, fixture | Consumes | DEL-03-01 | Implements | TBD-003 | C-v0.7 (V-GR1 present; R8-12 item 7) |
| Proposal and outcomes | Consumes | DEL-03-02 | Route, receipts | TBD-002 | P-v0.7 (carriage assurance per R5-2, governance phase per R8-1; R8-12 item 7) |
| Declarations | Consumes | DEL-02-01 | Host workflows | OI-014; OI-013 | WD-v0.7 (§4.3.0 Phase 1; `governed` flag PROPOSED) |
| Hold machine | Phase 1: evaluates reached-when and records (§2.4.0). Governance phase: realizes EXEC §4's hold content in host loops (§2.4.4) | DEL-02-03 (EXEC-v0.5 §2.1, §2.2, §4, PROPOSED (W7)) | Host construction | OI-013; OI-014; D6 (App side; closed for Phase 1) | EXEC-v0.5 |
| Act policy | Consumes | DEL-04-01 | Enforces own list; offers and captures acts | OI-021; consequence vocabulary | ACT-POLICY-v0.7 (R8-12 item 7) |
| Grant display states | Carries | DEL-04-02 | Controls | None: the register row is DEP-05-01-025 (2026-09-29 extraction; SoW CLM-002) | AS-v0.7 (R8-12 item 7) |
| Record format | Consumes | DEL-04-03 | Receipts, acts | — | RS-v0.7 (R8-12 item 7) |
| Model-interface basis | Receives or agrees. For its own fixtures it names FB-CC-1, a fixture basis and not a product selection (§4.1; R12-8) | — | Unknown | DEP-05-01-024 (UNKNOWN) | Product basis not supplied. SWBPIPE: none exists or is selected; the successor under D-58 is a SWBPIPE owner decision (SQ-29) |
| Host evidence | Receives, audits | Joined witness DEL-09-06 (deferred, DECISION-3) | Supplies | DEP-001 | Not received. SWBPIPE answers received 2026-09-28 are answers about its current state, not evidence |
| Common loop implementation | Not allocated | OI-014 owners | — | OI-014/013 | No agreed repeated responsibility |
| Human acts | None | — | Offers, captures, presents | — | Person only |

### 10.2 Common-implementation assessment

- The App runs no Chirality loop, so SWBPIPE is the one identified consumer
  (OI-005 open).
- Two candidate repeated parts exist, for OI-014 consideration only:
  - (a) parse completeness;
  - (b) catalog-schema checking, which might also serve DEL-03-03 (C holds
    this as a question).
- **No repeated responsibility is established. No common loop is proposed.**

### 10.3 Required inputs and standing

The supplier column names this register's ACTIVE row and its DAG-003 layer
(R9-6). Held arcs are candidate arcs and gate nothing.

| Input | Supplier (register row; DAG-003 layer) | Standing at v0.7 (Wave A labels, R9-11) |
|---|---|---|
| Entry elements 1–9; five class values; edition; exposure; basis; subject identities; FX-PIPE-01 | DEL-03-01 (DEP-05-01-014; held) | C-v0.7 (V-GR1 present) |
| Outcomes; identities; constraint; resulting objects; de-duplication; carriage assurance | DEL-03-02 (DEP-05-01-015; held) | P-v0.7 (carriage assurance per R5-2; governance phase per R8-1) |
| Checkpoint elements; subject classes; §4.3.7; identity tuple; holding library; Phase 1 and `governed` | DEL-02-01 (DEP-05-01-016; held) | WD-v0.7 (§4.3.0 CG-1…CG-7; `governed` PROPOSED) |
| Phase 1 (PH-1…PH-10); hold machine; resume point; re-hold; no resumption; SP-6; refused A12; MX rules; recovery | DEL-02-03 (DEP-05-01-017; held) | EXEC-v0.5 (PROPOSED (W7)); Phase 1 per §2.1; hold values governance phase per §2.2 (R5-1, R6-1, R8-2) |
| Act names; decline; treatment map; reserved operations | DEL-04-01 (DEP-05-01-018; admitted) | ACT-POLICY-v0.7 |
| Grant states incl. policy default | DEL-04-02 (DEP-05-01-025; held) | AS-v0.7 |
| Record inventory | DEL-04-03 (DEP-05-01-019; held) | RS-v0.7 |
| Panel needs | DEL-05-02 (DEP-05-01-020; held) | PANEL-v0.7, same executor. Named by DEP-05-01-020; PANEL does not yet define the needs as a list (PANEL header, Receivers) |
| Local-server capability requirements and qualification limits | DEL-01-05, outside the first increment (DEP-01-05-014, a DOWNSTREAM row of the supplier's register; admitted; this register has no mirror row) | Not supplied, and not consumed by this file. DEL-01-05 is a later undertaking (D1) |
| Model interface | UNKNOWN (DEP-05-01-024) | Not supplied for a product. Fixtures use FB-CC-1, fixture basis, not a product selection (§4.1; R12-8) |
| Host candidate and evidence | SWBPIPE (DEP-001; DEP-05-01-021) | Answered 2026-09-28 (RELAY §4); no candidate, evidence, commitment or contribution received; host joins deferred (DECISION-3) |

The supplier-side rows DEP-04-01-025, DEP-04-02-019 and DEP-04-03-029 name
the same exchanges from the supplier's register.

### 10.4 Receivers and register rows (R9-6)

Rebuilt at v0.7 from the ACTIVE rows of the consumers' registers. No
contribution is defined here; the last column says where this file already
holds what the row names.

| Receiver | Register row (DAG-003 layer) | Contribution the row names | Where this file holds it |
|---|---|---|---|
| DEL-02-01 | DEP-02-01-020 (held) | Minimal-loop consumer requirements, for the portable contract and the allocation map | §2.4 element table; §10.1–§10.3 |
| DEL-02-03 | DEP-02-03-022 (held) | Checkpoint arrival observation, subject binding and loop events | §2.4.1, §2.4.2, §2.3, §2.4.0 |
| DEL-03-04 | DEP-03-04-014 (admitted) | Minimal-loop and model receiving requirements, for the guide | The file as a whole, cited by label and section |
| DEL-04-02 | DEP-04-02-018 (held; R8-A) | A host agent's allow list, in-work destination grants and contacted-destination record | §5.1.1 (NW-8, NW-11, NW-15); §2.3 destination events; §5.3 DF-6 (request states), DF-8 (record), DF-9 (AS §3.2 owns the contacted-destinations display) |
| DEL-04-03 | DEP-04-03-028 (held; R8-B) | Destination contacted, destination grant and destination declined events | §2.3; E-4; §5.3 DF-8 (entry kinds, including `destination_request_closed`, v0.8) |
| DEL-05-02 | DEP-05-02-010 (held) | Loop messages, tools, events, checkpoints and receiving requirements | §2.1–§2.4, §5.1, §5.1.1 |
| DEL-09-06 | DEP-09-06-016 (admitted) | Loop and model receiving requirements, for the connected activity | The file as a whole |
| DEL-09-09 | DEP-09-09-021 (held; N-C6) | The embedded-loop receiving contribution for the embedded surface of the three-channel trace | §2–§9 as definition; no host evidence exists |
| DEL-08-01 (outside the first increment) | DEP-08-01-008 (admitted) | Embedded-integration receiving requirements, and the host-agent destination constraint a Domains query must be compatible with | §5.1.1; N-OPEN-3 names tool-caused traffic "e.g. a later Domains query" and leaves it open |
| DEL-10-03 (outside the first increment) | DEP-10-03-015 (admitted) | Host-loop and native-network receiving and conformance obligations, for the shared account | §5, §10, §12 |
| External SWBPIPE owner | No DOWNSTREAM row in this register (closeout R5-1-3; a register matter). Route: SoW TBD-003 | The §13 questions, relayed through DEL-09-06's relay file | §13 |

## 11. Fixture inventory (OUT-002, designed)

Every fixture names its catalog basis and its model-interface basis. The
catalog basis is C-v0.4 FX-PIPE-01 (`8fb51f07f`), plus V-GR1 per R5-7, both
carried in C-v0.7 §10. The model-interface basis of the fixtures is
**FB-CC-1, fixture basis, not a product selection** (§4.1; R12-8); the
product basis DEP-05-01-024 stays UNKNOWN. The parse-level fixtures FX-M
and the stream variants of FX-V1 are written as FB-CC-1 streams in
`prototype/fixtures/stream_fixtures.json` and ran on the §7.3 prototype
(parse step only; 19/19 as expected, 2026-09-30; 22/22 at RP-4 with
OBS1-C1…OBS1-C3, the shapes OBS-1 observed, §4.1). The other fixtures remain
case designs. Fixture exposure is "exposed on all
three surfaces" (a fixture assumption, R2-21) unless a variant is named.

**Checkpoint fixtures (FX-C) are two-part (R8-1, R8-2; EXEC GV-5).** Each
gives the **Phase-1 result** (recorded, not enforced; §2.4.0) and the
**governance-phase value** (retained). The governance-phase value reads the
fixture's checkpoints **as if declared governed**; no FX-PIPE-01 fixture
declares the flag (R8-11 item 5). "Both phases" means the recording rule is
the same in each, with dispositions as record labels in Phase 1 (LP-3).

| Fixture | FX-PIPE-01 subject | Input | Expected result | Serves |
|---|---|---|---|---|
| FX-V1 | T3: OP-C1 read of R-100 | Schema-conformant call | Dispatched; basis B1 with subject content identities per row | VER-004/005 |
| FX-V2 | T9–T10: PR-2 (item 1 via OP-C4 add support; item 2 via OP-C5 S-3 stiffness), relying on B2 | Schema-conformant call | Dispatched; "queued"; no acceptance event | VER-004/008 |
| FX-V3 | OP-C9 label S-4, requested direct **before** T15, under ⟨set-1⟩ (P-03 *effective (policy default)*, grant value propose) | Direct request | *Not permitted* (O-6); not converted | VER-004/008 |
| FX-V4 | T16: OP-C9 label S-4 "G-4" under ⟨set-2⟩ (T15: P-03 direct, scope {FX-W1; {S-4}}, effective) | Direct request | Applied, branch *direct under grant*, RC-2, origin mark, undo route; no acceptance. An OP-C4 on R-100 is outside the scope, so a direct request for it is *not permitted*. OP-C5 on S-4 is held on U-02 (C T15) | VER-004/008 |
| FX-S1 | OP-C5 stiffness given as text | Schema-invalid | Rejected at V-3 | VER-004 |
| FX-S2 | OP-C4 with the location missing | Schema-invalid | Rejected at V-3 | VER-004 |
| FX-D1 | OP-C4 at an occupied location on R-100 | Element-7 error | *Refused — invalid* (E-location-occupied) with evaluated basis | VER-004 |
| FX-D1b | OP-C4 at a location not on R-100 | Declared precondition | *Unavailable* "Location is not on run R-100" (HI-04 parity) | VER-004 |
| FX-D2 | T7: PR-1 relying on B1 (r12) after T6 (S-3 edited, r13) | Stale | *Refused — stale*, with B1 and B2; re-draft is PR-2 with lineage (T9) | VER-004 |
| FX-D3 | Tg: generation g2 after restore | Lineage change | Refusal reporting both bases; meaning per U-C2 | VER-004 |
| FX-U1 | A name absent from the offered edition | Not offered | Class 1 at V-2; not dispatched | VER-005 |
| FX-U2 | T8: OP-C2 for LC-1 at r13 | Unavailable | *Unavailable* "No current solve for LC-1 at this revision", evaluated B2 | VER-004 |
| FX-U3 | Named variant: OP-C2 not exposed on the embedded surface | Host exposure | Dispatched; host returns *not exposed on this surface*, relayed as class 2 | VER-004 |
| FX-R1 | Agent calls OP-C6 on S-2 | Reserved entry | *Not permitted*, naming reserved class and policy record; A8 offered, not recorded unless issued; no A4 | VER-008 |
| FX-R2 | Agent calls OP-C7 to accept PR-2 item 1 | Reserved entry | *Not permitted*; no A5 | VER-008 |
| FX-NP1 | OP-C11 (no policy basis, pending OI-021) requested direct; then proposed | Class no policy basis | Direct *not permitted*; proposal queues with no effect until A5 and application. **Case state HELD** (R2-9) | VER-004 |
| FX-O1 | T13: acknowledgment of T12 lost; resubmit PR-2 with the same identity | Retry | De-duplication returns the recorded outcome (RC-1). Never stale for its own effects. If unobservable: class 4, reporter loop | VER-005/009 |
| FX-UNDO | T17: OP-C10 undo RC-2 (governed by P-03, the policy record of the reversed operation, R3-4) | Undo | Applied RC-3 **reverses RC-2**. T16a's A4 on S-4 lapses (⟨S-4⟩ changed, FXA-2) | VER-008 |
| FX-V1s, FX-V1i | FX-V1's read as an FB-CC-1 stream: one call in four fragments; two calls whose fragments interleave | Streamed call | Each assembled *complete* and passed on to V-3 (§7.1). Prototype: as expected | VER-005 |
| FX-M1, M1b, M2, M3, M4, M4b, M4c, M5, M6a, M6b, M6c, M7, M8, M10, M11, M12, M13 | MC-1…MC-13 (`L-LOOP-MC-n`) as FB-CC-1 streams (§7 table, fixture column; MC-9 is shown by FX-M3). FX-M8 is R12-7's case: three calls, the middle one malformed | Malformed | As §7. Prototype: each as expected (§7.3) | VER-005 |
| FX-N1…N27 | MS-01…MS-27 (`L-LOOP-MS-n`) | Settings (N1…N13); destinations allowed, requested and disallowed (N14…N23; SoW OUT-002); the request with a carried call, unanswered at end, stateless evidence and prompt or control failures (N24…N27; v0.8, node B5) | As §5.2. The destination flow of FX-N14…N27 ran on the §5.3 DF-10 prototype `prototype/destination_flow.py` (scripted native layer and control; not a loop; results in VC-10) | VER-001/002 |
| FX-C1 | Checkpoint A4; reached-when (c) *applied* for PR-2; subject class "objects changed by a named outcome" | Kind (c) | **Phase 1:** arrival recorded; subject = objects created or changed by RC-1 (new support), by post-application subject content identities (R2-14); label *waiting* ("act not yet recorded"); nothing stopped; recorded *performed* only on host-captured A4 on those. **Governance phase:** waiting, and the run holds; performed only on host-captured A4 on those | VER-008 |
| FX-C2 | The same checkpoint; model text claims it was checked | Assertion | **Both phases:** no act recorded; still *waiting* (LP-5). Governance phase: the run stays held | VER-008 |
| FX-C3 | FX-C1 performed; then S-5 is edited, (i) before the resume point and (ii) after it with the run live; (iii) variant: the run has ended | Lapse | **Phase 1:** (i) and (ii) act-lapsed event recorded; label (i) "waiting — lapsed at ‹t›", (ii) **"act lapsed at ‹t›"** (R8-12 item 1); gated outputs show standing lapsed; **not re-held**; the agent re-requests the act as its plan requires (LP-7; R8-11 item 1). (iii) *lapsed* (standing). **Governance phase:** (i) act-lapsed event, then "waiting — lapsed at ‹t›". (ii) **Re-held**: "waiting — re-held, lapsed at ‹t› after resume"; stops at next action boundary; nothing undone; request re-issued for the whole scope. (iii) *lapsed* (standing). If the run ends while re-held: *waiting* (RH-7) | VER-008 |
| FX-C4 | Checkpoint A4, reached-when (c) *applied* for OP-C9 (T16, RC-2), subject class "objects changed by a named outcome" (S-4 ⟨S-4@r16⟩); T16a A4 on S-4 captured after the arrival; no A5 anywhere (direct branch) | Independent act | **Both phases:** *performed* on its own evidence. No acceptance prerequisite (C-3). SP-6 holds (T16a after T16) | VER-008 |
| FX-C4b | Same shape with a checkpoint arriving at T4 (subject "objects a named output concerns", OP-C3 findings on S-2/S-3); T2's A4 on S-2 predates it | Prior act | **Both phases:** T2's A4, on ⟨S-2@r12⟩ still current at T4, counts for S-2 and is relayed with its time (SP-6; DECISION-K1 K1-2); the arrival is answered once an A4 on S-3 is added, the two acts together (joint answer; K1-3), or by an A4 on S-2 and S-3. Phase 1: until then the record shows the arrival unanswered for S-3; nothing stopped. Governance phase: the arrival waits for S-3. Under the governance-phase option (EXEC SP-6F): T2 is "prior act not counted" (captured before arrival (governance-phase option)), and only an A4 captured after T4 answers | VER-008 |
| FX-C5 | A5 checkpoint, reached-when (c) *PR-2 queued* (T10); subject PR-2 change items; T11 accept item 1, reject item 2 | Mixed | **Both phases:** *resolved negatively*, **partial** annotation (item 1 A5) per WD §4.3.7. Phase 1: the *on mixed decision* path, if declared, is guidance for the agent's plan (LP-8). Governance phase: the loop follows it | VER-008 |
| FX-C6 | A6 checkpoint; the person declines | Act-declined | **Both phases:** *resolved negatively*; no A6. Phase 1: the negative path is guidance (LP-8). Governance phase: the loop follows it | VER-008 |
| FX-C6b | A12 checkpoint; the person declines | Act-declined | **Both phases:** *resolved negatively* | VER-008 |
| FX-C7 | Checkpoint reached-when (c) *queued*; run stopped before any proposal | Never met | **Both phases:** *not reached* at run end | VER-008 |
| FX-C7b | Checkpoint reached and waiting; run ended; the person performs the act afterwards | Post-run act | **Both phases:** run-ended event with *waiting*. The later act is shown "after run end" against the subject; the ended run's disposition is unchanged, and it is never resumed (R4-4) | VER-008 |
| FX-C8 | Checkpoint A4, reached-when (a) before dispatch of OP-C5; subject class "targets of the held call" | Kind (a) | **Phase 1:** arrival recorded when the OP-C5 call passes V-3; subject = S-3 by its subject content identity in the relied-on read B2; the call is **dispatched, not held**, and may carry "continued past ‹checkpoint› before A4" (LP-4). A host-captured A4 on that content, when performed, is recorded and answers the arrival. **Governance phase:** call held. Subject as above. After host-captured A4 on that content, the same held call is dispatched | VER-008 |
| FX-C9 | A5 checkpoint on OP-C4's result (C V-CP1 shape; `CP-accept` per FXA-5); grant effective direct; direct requested | Constraint | **Phase 1** (R8-11 item 2 as restated by R9-2; C-6): no constraint is carried as enforcement. The host's own treatment decides the direct request under the effective direct grant, and the loop relays the outcome as observed. If the host applies directly, no proposal is queued, so the A5 checkpoint (kind (c) *queued*) is not reached, and the record shows the direct application under the person's grant. Nothing is requested by reason of an arrival that did not occur, no A5 is forced, and none is recorded (R9-2 as corrected by R10-1; G-9 closed). Following the checkpoint as guidance, the agent's plan proposes instead. DESIGNED. **Governance phase:** dispatch carries the governing checkpoint constraint; *not permitted* naming it. **AWAITING INPUT** (R2-12; §13 Q-1) — SQ-02 answered 2026-09-28: no host loop and no host-held evaluation; route (iv) (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3) | VER-008 |
| FX-C10 | Agent-authored A9 of an A4, with no capture evidence | Record only | **Both phases:** no act recorded; checkpoint stays *waiting* | VER-008 |
| FX-C11 | C named variant **V-GR1** (R5-7): a run of WD-EX E1d (`label-with-grant`; `CP-grant` requires A12; reached-when kind (a) before dispatch of OP-C9; declared content {P-03, *direct*, {FX-W1; {S-4}}}), branching from T14 (r15). The agent's OP-C9 call on S-4 meets reached-when, so `CP-grant` arrives at r15; T15's A12 is captured **after** the arrival; the control establishes it | A12 at the arriving call | **Phase 1:** the arrival is recorded and the OP-C9 call is **dispatched, not held**. Requested direct under ⟨set-1⟩, the host's treatment answers *not permitted* (FX-V3 shape). The dispatch may carry "continued past CP-grant before A12". T15's A12 (captured after the arrival, established) is recorded as answering `CP-grant` (*performed*). A re-issued OP-C9 call is a new call (T16 shape under ⟨set-2⟩). Sub-variants label the record as below, with no call held. **Governance phase:** *performed* (SP-6 holds; established). The held call is dispatched unchanged as T16 (RC-2). Sub-variants: **pending** → *waiting*; **refused** → *waiting* "A12 refused by control: ‹reason›", call stays held, earlier setting not superseded; confirmation lost → *unknown*; a later **established** A12 on an overlapping scope → "superseded by ‹act›", checkpoint stays *performed* | VER-008 |
| FX-C11b | Main timeline order: T15's A12 captured **before** a `CP-grant` arrival (any run declaring CP-grant that arrives after T15) | Prior act | **Both phases:** T15's A12, on the declared content with ⟨set-2⟩ still in force, counts: the arrival is *performed*, citing T15 and its time (SP-6; DECISION-K1 K1-2). Phase 1: recorded so; nothing is held. Governance phase: the run proceeds without a repeated A12. Under the governance-phase option (EXEC SP-6F): T15 is "prior act not counted" (captured before arrival (governance-phase option)), and the person must perform A12 again before the run proceeds (R5-7) | VER-008 |
| FX-C12 | FX-C5 variant: item 2 refused stale before a decision; item 1 A5 | Item left | **Both phases:** item 2 left with its event; *performed* over a reduced subject, **never** "all accepted". On SWBPIPE any model change would stale every queued item (whole-model scope, R8-3) | VER-008 |
| FX-C13 | Declaration with required act A10 (recognized, not allowed); a declaration with an unrecognized act name | Invalid / not established | **Phase 1:** reported as a declaration finding (*invalid*, with its FB code / *not established*); not evaluated; no arrival; the workflow check result is unchanged by it (R8-11 item 3). **Governance phase:** reported *invalid* / *not established*; not evaluated (R2-10); no value; check *not established* (EXEC §4.14) | VER-008 |
| FX-C14 | Kind (c) checkpoint on *PR-2 queued* (T10). In the same model response the agent also issued an OP-C1 read that the loop dispatched before observing the queued outcome | Continued past / action during hold | **Phase 1:** arrival recorded. The OP-C1 dispatch may carry "continued past ‹checkpoint› before A5" with its reference (LP-4). Nothing is stopped, and later dispatches follow the agent's plan. **Governance phase:** arrival waits. The OP-C1 dispatch is recorded as **action during hold** with its reference; nothing further is dispatched (§2.4.4) | VER-008 |
| FX-C15 | The run of FX-C7b ended; Engineer A starts a new run of `supports-adjust` recording **continues ⟨run 12⟩** | Continuation | **Both phases:** new run's checkpoints start *not reached*; no arrival or disposition is inherited. At the new arrival the post-end act counts for the bound referents whose content is still the one it was made on, cited with its time (SP-6; DECISION-K1 K1-2); under the governance-phase option (EXEC SP-6F) it is "prior act not counted" (captured before arrival (governance-phase option)) | VER-008 |

## 12. Evidence standing labels

| LOOP label | C/P label (IR1-B B-m5; mapping owned by C) | Can support |
|---|---|---|
| CONTRACT-REVIEWED | illustrative | Completeness of the expectation |
| FIXTURE-EXECUTED | test-double | The expectation on that double only |
| HOST-OBSERVED | actual host | That candidate only |
| NOT-OBSERVED | (none) | Nothing; recorded as a gap |
| HELD | (case state) | Nothing. A decision is pending (e.g. FX-NP1, R2-9) |

Owner-reported construction (DEP-001) is none of these.

## 13. Relay questions prepared (for W9; not delivery)

These questions are consolidated in RELAY-v0.2 §3 (kept as relayed in
RELAY-v0.3 §3; answered, RELAY §4): Q-1 → SQ-02; Q-2 → SQ-01;
Q-3 → SQ-03 (d); Q-4 → SQ-19 (a); Q-5 → SQ-21; Q-6 → SQ-08 (b), SQ-07 (d);
Q-7 → SQ-11. §5, §7 and §8 open items map to SQ-29…SQ-32 (R5-9).

These are prepared for App-manager preparation and human relay to the SWBPIPE
owner (DEP-001; DEP-05-01-021). Writing them is not delivery, agreement or
adoption.

**Standing: answered (R8-7).** The questions were relayed and answered on
2026-09-28 (`RELAY_ANSWERS_SWBPIPE.md`, delivered sha256 `6f01add3…61c7`;
current bytes `afb6e063…0e74` after SWBPIPE's own revision, header;
RELAY §4). The answers describe SWBPIPE's current state. They are not
commitments, delivery, adoption or host evidence (DECISION-3), and host
joins are deferred. The questions below are kept as prepared. Gists:

- Q-1 (SQ-02): route (iv), none planned. There is no host loop or
  host-held evaluation (SQ-20), and an extra constraint field would be
  refused as unknown. Governance-phase input only (R8-2).
- Q-2 (SQ-01): no capture-evidence reference. Apply's receipt names no
  person or time and does not survive restart.
- Q-3 (SQ-03 (d)): partly. Target ids and a new whole-model hash; no
  post-application per-object identities (R8-4; §6.4 RN-2).
- Q-4 (SQ-19 (a)): no host loop, so no per-turn guidance records.
- Q-5 (SQ-21): no.
- Q-6 (SQ-08 (b), SQ-07 (d)): DRAFT #885 looks up the idempotency key
  before the basis check. Staleness is whole-model (R8-3; §6.3 R-c).
- Q-7 (SQ-11): no exposure element. "Not exposed" is reported as
  `unsupported_change` / `unsupported_method` (R8-5; §6.4 RN-3).
- §5, §7 and §8 open items: SQ-29 and SQ-30 (none; §5.1 note); SQ-31 (no
  loop; engine-side strict preflight); SQ-32 (placement not decided; the
  solve runs as a background job with poll and cancel).

- **Q-1 (R2-12).** Can your validation/application route receive a
  per-request **governing checkpoint constraint** and resolve *propose* from
  it? Or does the host evaluate its own copy of the selected workflow's
  declaration? What evidence will show which? An omitted constraint is
  indistinguishable from none.
- **Q-2 (R2-20; X-17).** For each act your act facility captures (A4, A5,
  A10, A12, and A6/A7 where offered), does it expose a stable
  **capture-evidence reference**? The reference would cite act identity,
  actor, act kind, bound content identity and time. Without one, no
  host-content checkpoint can become *performed*.
- **Q-3 (R2-14).** Does an applied outcome identify the created and changed
  objects, with their post-application subject content identities?
- **Q-4 (R2-20; X-18).** Can the host loop record, per turn, the source
  identity and content identity (with method designation) of each guidance
  input it supplies? Where it cannot, the record says *unknown*.
- **Q-5 (R2-2).** Does the host offer any faithful-record operation? If so,
  does it meet the four R2-2 conditions?
- **Q-6 (R2-13).** Does the host de-duplicate by proposal identity before the
  basis check, and compare per-item target subject content identities for
  staleness?
- **Q-7 (R2-4).** Does the host report *not exposed on this surface* from its
  exposure element? Which entries does it supply to the embedded surface?

## Findings

- **G-1 (closed by R5-2).** A host loop's own evaluation of the declaration is
  *host-held*. C-6 is aligned.
- **G-2 (closed by R5-7).** A12-at-checkpoint fixtures use C named variant
  V-GR1. `L-LOOP-C11` is dropped.
- **G-3 (answered on the App side at v0.8; relayed as SQ-31).** Undispatched sibling calls are held,
  not run, during a hold (LH-0; governance phase). T-OPEN-1 is closed by
  R12-7: each call of a response is handled on its own, and a malformed
  sibling gets its own refusal (MC-8, PROPOSED; OBS-1 observed no malformed sibling, §4.1). LH-0 is
  unchanged. SWBPIPE has not decided (SQ-31).
- **G-4 (retained).** One executor drafted LOOP and PANEL, and the same
  executor revised both at v0.6, so the v0.6 pair needs an independent
  check. The v0.7 alignment edits to the pair were again made by one
  executor (A1-D), so the same holds for v0.7.
- **G-5 (closed, R6-4).** EXEC-v0.3 HS-3 (c) gives model-supplied carriage
  *not enforceable* after SQ-02 and *not established* only before, matching
  R5-1. (v0.6: governance phase; SQ-02 is now answered, so HS-3 (c) applies
  against SWBPIPE, R8-2.)
- **G-6 (closed at v0.7 by SCA-V4-001; R9-8).** At v0.6 the DEL-05-01 SoW
  REQ-001 and AC-001 still assumed the V4-HOST-01 wording that DECISION-4
  D4-3 revises. SCA-V4-001 revised them (SoW AX-004; ScopeOfWork.md
  `9b2379a1…85ed`): REQ-001 now reads "local and cloud models as options the
  person chooses among, with no default: a user-controlled local model
  server, or a cloud model reached by OAuth sign-in or an API key", and
  AC-001 "the person's choice between local and cloud models with no
  default, cloud access by OAuth sign-in or an API key". V4-HOST-01 and
  V4-ARC-11 were amended with them.
- **G-7 (closed, R8-12 item 1).** The Phase-1 lapse label after the resume
  point was "waiting — lapsed at ‹t›" at A4. The integrator ruled it
  **"act lapsed at ‹t›"**: nothing says *waiting* and nothing is re-held;
  a new act is recorded when performed. C-4's phase note, §2.4.0 and FX-C3
  (ii) now use it, as do EXEC PH-8/CH-7, RS L-12, AS OV-5 and PANEL W-5e.
- **G-8 (new; R8-13).** Two Phase-1 statements need care beside §5.1.1.
  - "The loop presents no tool-permission prompts" (A-5) still holds. The
    in-work destination request is an A8 answered by an A12
    network-destination grant, not a tool permission (A14 does not arise
    in host loops).
  - "Nothing holds" in Phase 1 (§2.4.0) concerns checkpoints. NW-12's
    wait is the one requesting call awaiting the person's grant; it holds
    no run and no other call. R13-5 states the reading: the wait is the
    grant being sought, not a checkpoint hold, so DECISION-4 does not bear
    on it (§5.3; v0.8, RP-4).
- **G-9 (new, v0.7; R9-2; closed by R10-1).** R9-2 said that
  in the FX-C9 case "the checkpoint's disposition stays *act not performed*
  unless the person performs it". §2.4 has six shared dispositions and none
  is called *act not performed*. Under §2.4.1 an A5 checkpoint with
  reached-when kind (c) *proposal queued* is *not reached* when the host
  applies directly and nothing is queued. FX-C9 carries both wordings. No
  text decides whether "act not performed" is a plain description of *not
  reached*, or whether the direct application should count as an arrival
  (then *waiting*), which would change a reached-when rule owned by
  DEL-02-01 and DEL-02-03. **Closed by R10-1:** the checkpoint is *not
  reached*; nothing is requested by reason of an arrival that did not
  occur, no A5 is forced, and none is recorded. FX-C9 now carries that one
  wording.
- **G-10 (new, v0.7; R9-6).** The rebuilt §10.3 and §10.4 follow the live
  registers. Three things are returned, not decided here:
  - DEP-05-01-020 names DEL-05-02's panel needs; PANEL does not yet define
    them as a list (Wave B).
  - MS-23's refusal has no stated place among TL-2's result classes
    (Wave B, with the destination interface). **Closed at v0.8 (node
    B5):** class 2 "destination not allowed" (TL-2; §5.3 DF-6).
  - This register has no DOWNSTREAM relay row and no mirror of
    DEP-01-05-014 (closeout R5-1-3 and R5-1-2; register matters).

- **G-11 (new, v0.8; R12-8).** FB-CC-1 closes §4's representation rows
  only as PROPOSED. Three of its readings are inferences, not statements of
  the reference, and are marked so in §4.1: that argument pieces are
  concatenated in order; that "no arguments" is `{}`; and that an error has
  no termination-reason value. Two choices are this file's, not the
  reference's: MC-1 rejects every call of a length-truncated response
  (§7), and MC-12 rejects a response with a second choice. OBS-1 recorded
  what one local server does on each point (§4.1): `{}` for no arguments,
  one argument piece per call (consistent with ordered concatenation), a
  final `tool_calls`; it showed no error stream, so the third inference
  stays unobserved (v0.8, RP-4).
- **G-12 (new, v0.8; S1-D LOOP item 8).** Two failure rules of §3.1 touch
  other owners and are returned for joining: F-4 (the request is not sent
  when the destination record cannot be written) belongs with §5.1.1 and
  RS R15 (node B5; **joined at v0.8**: §5.3 DF-4 (c), DF-F2); F-10 (no further dispatch while the run record cannot
  be written) needs DEL-04-03's statement of when a record write is
  complete. E-6's event ordinal is new and is consumed by PANEL-v0.8 FD-3.
- **G-13 (new, v0.8; node B5; S1-D §5 structural choice 1).** Destination-
  reaching tools needed a home in the tools subject. They are host catalog
  entries with an external-contact declaration, and the agent's in-work
  request is a call to a host-supplied destination request entry (§5.3
  DF-1; C-v0.8 §3.4). A second tool source (an MCP server's own tool list
  read by the loop) would have needed a counterpart of TL-1, V-2 and the
  class element and would sit against V4-ARC-13; it is not needed and not
  used. Two consequences are recorded, both PROPOSED: the loop treats the
  destination request entry by its kind (it validates the carried call,
  returns an interim notice and later a deferred outcome), and the deferred
  outcome's representation is an inference from FB-CC-1, which has no
  member for a second result to a call already answered (DEP-05-01-024 for
  a product; OBS-1 does not cover it).
- **G-14 (new, v0.8; node B5; S1-A AS 3).** The contacted-destinations
  display is DEL-04-02's (AS §3.2), because DEL-04-02's ScopeOfWork CLM-002
  consumes the contacted-destination record "which DECISION-5 requires to
  be shown" (DEP-04-02-018). PANEL ND-4 receives it for a host panel. The
  §10.1 row said "AS §3 (display)" since R8-13; AS now holds it (§5.3
  DF-9). DEL-05-02's ScopeOfWork still names no destination surface (PANEL
  F-12, the owner's).
- **G-15 (new, v0.8; node B5; K1-6).** The stateless MCP evidence (§5.3
  DF-7) rests on the published revision 2026-07-28, read-only on
  2026-09-30 at 18:42 UTC from
  https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/046fa30efd374370afb87ef830bd788eac5f217e/docs/specification/2026-07-28/
  (the `main` head, committed 2026-09-28T22:50:34Z; the rendered page
  https://modelcontextprotocol.io/specification/2026-07-28 returned HTTP
  200 and was not relied on). sha256 of the files relied on:
  `basic/index.mdx` 03586b10e3214c55478293f1199fffb0bbf95bbef5df3d6a8378e860697bd63f;
  `basic/versioning.mdx` bc02f271700bdecd88034f2d7801eb09110a71d65876487378d94e48dfeb90dc;
  `server/discover.mdx` 3fe1f5b5f1528014216b1e49cc3363b3c689c36bcb80a6957ddca6a04cea409c;
  `basic/transports/stdio.mdx` 6fd49766c40dc093d1f5993ab584bad0a06cbb496c2d3019c50f8fe3c8171e57;
  `basic/transports/streamable-http.mdx` 22574bf11e004068493787203ce92be1162107cad717bcb805a15780d4fa69c9.
  The evidence rule is this file's (PROPOSED), not the specification's:
  the specification defines the revision and the discovery request, and
  says nothing of how a host proves a server's conformance.

## UNRESOLVED

| Item | Owner | Point of need | Effect |
|---|---|---|---|
| *Closed at v0.8 (RP-4; R13-6).* OBS-1: an observation of a local OpenAI-compatible server on the four FB-CC-1 points (§4.1; R12-8) | OBS-1 (Part C, run 2026-09-30) | — | §4.1's OBS-1 column holds the observation (DEL-01-01 `OBS_1_0.158.0.md` §10). It is one server at one version: §4's rows and MC-1…MC-13 stay PROPOSED, and DEP-05-01-024 stays open for a product |
| OI-013 loop placement, parsing, persistence, panel assembly | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Outcomes only |
| OI-014 shared placement | App/shared contract owners | Before structural/production allocation | No common loop |
| DEP-05-01-024 model interface and representation (for a product) | UNKNOWN supplier; App/shared embedded-integration owner receives or agrees | At conformance use | Fixtures use FB-CC-1, fixture basis, not a product selection (§4.1; R12-8); §4's representation rows, MC-6 and MC-8 are PROPOSED from it; OBS-1 observed the four points on one local server (§4.1) and changed none of them. No product basis is selected. SWBPIPE: no model interface exists or is selected; the successor under SWBPIPE D-58 is an owner decision (SQ-20, SQ-29) |
| DEP-001 host evidence, including Q-1…Q-7 | SWBPIPE outside implementation session. Q-1…Q-7 answered 2026-09-28 (§13); SWBPIPE owner decisions listed in ANS §2 remain open | Before corresponding integration/examination and fallback-replacement decision; when the owner resumes UI-SUCCESSOR (DECISION-3) | All host conformance NOT-OBSERVED. FX-C9's governance-phase value AWAITING INPUT (STD-2 annotation); its Phase-1 result DESIGNED |
| OI-021 first connected operation; operation-specific reserved additions; OP-C11 class | Owner via outside SWB session and App/shared owner | Before connected SoW and execution | FX-NP1 HELD; fixtures invented. OI-021 stays open; SWBPIPE's candidates are recorded (SQ-04; R8-10) |
| Consequence vocabulary | DEL-04-01 with host policy owner | Before class assignment | Classes as supplied |
| Hold machine confirmation (EXEC-v0.5 §4, PROPOSED (W7)): resume point, re-hold, no resumption, refused A12, MX rules | DEL-02-03, at the next integration review | Before dependent host-loop implementation | C-4, C-7, C-8 and §2.4.1 adopted as proposed. Their hold content is governance phase (R8-1); Phase 1 uses their recording content (§2.4.0) |
| C U-C5 findings location | DEL-03-01 with host owner | Before E-5 route (b) is used | E-5 conditional |
| C U-C3 / R2-13 staleness rule host confirmation | Host owner with DEL-03-01/03-02 | Before FX-D2/FX-O1 execution | §6.3 R-c meaning only. R2-13 amended by R8-3: host scope where no subject identities; SWBPIPE: whole model (SQ-07 (d)) |
| C U-C6 entry-version mismatch | Host input | Before FX-D-series execution | O-3 |
| U-P1 / TBD-002 resubmission mechanics; U-P9 sibling grouping | DEL-03-02 with DEL-05-01 and host owner | Before FX-O1 | Meaning given by P-v0.8 §3.5 PM-4 and §4.7 SQ-P6 (§6.3 R-d; v0.8, RP-4); mechanics open. The malformed-sibling part of U-P9 (= T-OPEN-1) is ruled by R12-7 (MC-8); the grouping mechanics stay with DEL-03-02 |
| N-OPEN-1 (**closed at v0.8 by R12-7**: a class label local or cloud in the destination record, not a gate; MS-11 released); N-OPEN-2/3 endpoints, cloud destinations (including OAuth sign-in endpoints), tool traffic; N-OPEN-4 how a category switch and its named entries combine (**closed by DECISION-K1 K1-5**, 2026-09-30: a named entry is allowed on its own; a switch allows the whole category; NW-8); N-OPEN-5 the evidence that an MCP server follows the stateless revision 2026-07-28 (R8-13; **closed at v0.8 as PROPOSED**: §5.3 DF-7, SE-1…SE-3, with the limit "stateless revision declared, not verified") | App/shared embedded-integration owner with SWBPIPE owner (N-OPEN-4 decided by the owner). SWBPIPE DEC-051 is recorded as a note, not a conflict (R8-9) | Before endpoint and destination cases are finalized | MS-11 released (R12-7). NW-8 states the settled rule for N-OPEN-4 (MS-15, MS-18 follow it), and NW-10 treats unevidenced conformance as not following (PROPOSED); DF-7 says what evidences conformance (MS-26). N-OPEN-3 narrowed: declared traffic is the agent's (§5.3 DF-1, DF-F8) |
| CLOSED at v0.7 (SCA-V4-001, accepted 2026-09-29; R9-8) — the revised V4-HOST-02 (DECISION-5; R8-13) is the accepted text | Owner | — | NW-2 quotes the accepted text (P/docs/PRD.md `bb6e786f…49bd`); §5.1.1 cites it with V4-ARC-12 and ARCH §4 |
| CLOSED — DECISION-5 points settled by the owner's DECISION-5 confirmation (2026-09-28: the "MCP V2" reading confirmed; the person-only grant not objected to and stands): the person-only grant (point 3); the recorder's reading of "MCP V2" as the stateless MCP revision 2026-07-28 | Owner | Before §5.1.1 is relied on for implementation | NW-10 and NW-11 applied as recorded |
| Network-destination governance phase: allow lists locked by an organization; enforced sandboxing of MCP servers and other outside processes (DECISION-5) | Owner, when taken up | When a host needs it | Not defined here. In Phase 1, NW-16's evidence limit applies |
| CLOSED at v0.7 (SCA-V4-001; R9-8) — V4-HOST-01 and V4-ARC-11 now state no default and OAuth sign-in or an API key (DECISION-4 D4-3; R8-9) | Owner | — | NW-1 quotes the amended V4-HOST-01. SoW REQ-001 and AC-001 were revised with it (G-6, closed) |
| CLOSED at v0.7 (SCA-V4-001; R9-8) — V4-WF-05 and V4-HI-42 now state the phasing themselves: the hold is phased to the governance layer; the request and the record clauses are in force (R8-1; R9-1; DECISION-4 D4-1) | Owner | — | §2.4 lead and §2.4.0 cite the amended texts; the host-loop hold is governance phase (§2.4.4) |
| *Closed (DECISION-K1 K1-1, 2026-09-30).* Who requests the act at a checkpoint in the current phase (R9-1) | The owner (decided) | — | LP-5 states the settled rule: the agent carrying out the workflow asks. How an App run observes an arrival and a request is DEL-02-03's (EXEC, Wave B) |
| CLOSED (R10-1) — FX-C9 disposition wording, *act not performed* against *not reached* (G-9) | Integrator | — | FX-C9 and PANEL PC-24 say *not reached* |
| Governance phase taken up (R8-1) | Owner, per workflow that needs it (DECISION-4 D4-1) | When a workflow needs enforced checkpoints | §2.4.4 and the governance-phase columns apply to governed checkpoints only then |
| SWBPIPE embedded direction ("embedded Runtime", RUNTIME-ADOPT; D-58) predates D-20 (R8-8; DECISION-4 D4-2) | SWBPIPE (its to act on) | When the owner resumes UI-SUCCESSOR | None on this contract; note in §1 |
| *Closed at v0.8 (R12-7, INTEGRATION).* T-OPEN-1 valid siblings beside a malformed call | Integrator (ruled) | — | MC-8: the valid calls are handled on their own; the malformed call gets its own refusal (P-v0.8 §3.1 rule 5). PROPOSED; OBS-1 observed no malformed sibling (§4.1). SWBPIPE: not decided (no loop; SQ-31) |
| R-OPEN-1 quantitative responsiveness | Owner, if wanted | Before any numeric criterion | None set (SQ-32: SWBPIPE's solve is a background job with poll and cancel) |
| Seat role mapping (U-09) | DEL-02-01 with SWB owner and DEL-02-04 | Before record fixtures | *unknown* allowed. SEAT-1…SEAT-3 kept (R8-8). SWBPIPE: no seat concept; its one agent panel is the likely counterpart (SQ-19 (d)); not decided |
| Holding library (U-24) | Confirmed by EXEC §6.2 (HL-1…HL-3) | — | Carried (§2.1) |
| R2-n sibling v0.3 elements | — | — | **Confirmed by V2** (reviews/V2.md). T15 re-pointed per R4-18 |
| D6 App-side run holds | The owner (DECISION-4): closed for Phase 1; re-opens with the governance phase (R8-2). SWBPIPE answered SQ-02 on 2026-09-28: route (iv), none planned | When the governance phase is taken up; before App-side hold implementation | Not this contract's. Phase 1: no hold anywhere (§2.4.0). §2.4.4 LH-3 claims no App hold |
| *Closed (DECISION-K1 K1-2, 2026-09-30).* U-E4 SP-6 alternative (count prior acts bound to current content) | The owner (decided) | — | In the current phase an earlier act on current content counts, cited with its time (C-2; EXEC SP-6); FX-C4b, FX-C11b and FX-C15 recomputed. Capture after arrival is kept as the governance-phase option (EXEC SP-6F) |
| *Closed (DECISION-K1 K1-3, 2026-09-30).* U-03 multi-row A4 purpose after partial lapse | The owner (decided) | — | C-4: an act on the lapsed referents alone answers jointly with the earlier act (EXEC §4.7 JA-1); the variant is released |
| (closed, R6-4) Sibling elements pending | — | — | V-GR1 (C-v0.5), the R5-1 values (EXEC-v0.3) and P §3.3 (P-v0.5) are present at `c7f5513db`. No pending sibling element remains |

## Verification cases

These are designed, not run.

| Case | Procedure | Expected result | Serves |
|---|---|---|---|
| VC-01 | Trace §5.1 (including §5.1.1 and, from v0.8, §5.3) and MS-01…MS-27 to PRD V4-HOST-01/02 and ARCH V4-ARC-11/12 as amended by SCA-V4-001 (DECISION-4 D4-3; DECISION-5) | Every rule traced; no default between local and cloud; OAuth sign-in and API key both covered; two-level allow list with the model service always allowed; MCP only if stateless (2026-07-28); in-work scopes once / this run / always, only the requesting call waiting; decline "destination not allowed by the person"; a disallowed destination refused (MS-23); always-off list; every destination recorded and shown in any model mode; outside processes carry "process network not observed"; one destination flow (§5.3): V-D after V-3 and before dispatch, request states and results in TL-2's classes, the recording of declines and refusals marked PROPOSED (R12-10); MS-11 released: the model service's class local or cloud is a label, not a gate (R12-7); host observations NOT-OBSERVED, and any later host observation identifies the configuration, the grants in force and the observed destinations (SoW VER-001) | VER-001 |
| VC-02 | Inspect NW-3/NW-6/NW-7 and MS-03/06/07/08/12 against V4-ARC-12 | Native layer is the enforcement point; neither key nor sign-in credential reaches the script; labels applied | VER-002 |
| VC-03 | Review §1, §2 and §4 (with §4.1) | Four subjects; the App path is distinct (Responses API unobserved); FB-CC-1 labelled "fixture basis, not a product selection" with URL, retrieval date, sha256 and the passages relied on; its four points PROPOSED with the inferences marked; DEP-05-01-024 open for a product; Pi excluded; D3 attribution per R2-11 | VER-003 |
| VC-04 | Review §6 and the FX-V/S/D/U/NP fixtures against C-v0.7 §4.1 and P-v0.7 §9 | V-2 split holds; "not exposed" only host-reported; five class values; O-1…O-6 hold; FX-D1/D1b distinguish invalid from unavailable; FX-D2 is a revision within g1 | VER-004 |
| VC-05 | Run the §7.3 prototype on the FX-M and FX-V1 streams (parse step, FB-CC-1); exercise FX-M, FX-V1, FX-U1 and FX-O1 against a loop test double once a loop and C's simulated host exist | Prototype: every fixture as expected and every record valid against `LOOP_TOOL_CALL.schema.json` (2026-09-30: 19/19; at RP-4, 22/22 with the OBS-1 shapes). Loop double: zero dispatch for rejected calls; each valid sibling of a malformed call handled on its own (R12-7); de-duplication before the basis check; class 4 reporter is the loop | VER-005 |
| VC-06 | Review §8. On host observations, check candidate, configuration and placement | No threshold; results limited to observed scenarios | VER-006 |
| VC-07 | Compare §10 with SoW CLM-001/002/003, REQ-006, OI-013/014, DEP-001 and the Clarification | Every excluded act has its owner; no common construction allocated | VER-007 |
| VC-08 | Review §2.3, §2.4 (incl. §2.4.0), §9 and FX-C1…C15 (incl. FX-C11 on V-GR1 and FX-C11b), FX-R1/R2 and FX-UNDO against EXEC-v0.5 §2.1, §2.2 and §4, WD-v0.7 §4.3, ACT, P and AS | **Phase 1:** no hold, stop or re-hold anywhere; no hold-support value; no *unsupported* for a hold reason; the required act requested by the agent, never by the loop (LP-5); arrivals and acts recorded as observation; "continued past" only as an optional annotation; acts only when performed; reserved acts stand; lapses recorded; invalid declarations a finding only. **Both phases:** declared subject class bound, including the declared A12 setting (R5-3); reached-when observed-only; SP-6 earlier acts counted on current content with their time (DECISION-K1 K1-2; SP-6F ordering only under the governance-phase option); joint answer after a partial lapse (K1-3); no resumption; act-declined for A4/A6/A7/A12; MX rules; A12 supersedes only when established. **Governance phase:** re-hold after resume and after the person's undo; hold support in the four R5-1 values; constraint host-held; values read as if governed | VER-008 |
| VC-10 (v0.8, node B5) | Run `prototype/destination_flow.py` (§5.3 DF-10) on FX-N14…N27; validate its RS entries against `RS_RECORD.schema.json` and its request records against `LOOP_DESTINATION_REQUEST.schema.json`; check each element named in §5.3 against its counterpart in ACT §2.7, AS §3–§3.2 and §6, RS R15 and §13.3, PANEL §3.8, C §3.4 and §4.1 | Every case gives the §5.2 result; every entry and record valid; the invalid examples refused; no element named on one side only. 2026-09-30: see §11 and the prototype README | VER-001 |
| VC-09 | Audit every claim for a §12 label and an exact identity. (The v0.3 clause on auditing R4-n elements against sibling text was closed at v0.5, change row R5-9) | No HOST-OBSERVED claim without candidate evidence; HELD and AWAITING cases not counted as passes | VER-009 |
