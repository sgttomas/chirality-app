# Stock Codex hosting boundary

**SUP1 current supplier basis (proposed controlled adoption):** owner-authorized
development/definition pin 0.160.0; §7.0/generated/0.160.0 govern maintained
identity. Historical 0.158.0 evidence below remains dated; qualification absent.
- Contribution: DEL-01-01/HOSTING-BOUNDARY-v0.9 (supersedes HOSTING-BOUNDARY-v0.8, last changed at `891242377f` and unchanged at `e4e14d6ae6`, file sha256 3cf0381c42358fec4a2088ab3886e14b66d6d2020482c72e195fda068a6d78b1; earlier: HOSTING-BOUNDARY-v0.7, last changed at `c896a99d90` and unchanged at `86cafc0e1c`, file sha256 dcf67efc00682967150e5ce094c3961c00248475e8883001cf7045c8b477a865; earlier: HOSTING-BOUNDARY-v0.6, last changed at `3733b1421` and unchanged at `3dd7c22c73`, file sha256 d11d4c574aa3c342bfac9c1d1e9bf3746aa885baafd17eaa296a79a523e3d0b9; HOSTING-BOUNDARY-v0.5, last changed at `375c3970c` and unchanged at `94aa9181b`, file sha256 f1a23022df76fe04bfc5ad2220b57d2cdebc101f8d791b4edb163aea6109e11b)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Phase (V4-WF-05 as amended by SCA-V4-001; R9-1; R8-1; DECISION-4 D4-1): holding a run at a checkpoint is phased to the governance layer, and in the current phase (Phase 1) neither the App nor a host's embedded loop enforces a hold. So no App run is holding at a checkpoint, and this boundary uses none of HP-3 or HP-4 for a checkpoint, makes no hold claim and issues no act request in an agent's place (§6.7). The §6.7 hold-point facts are kept as the **governance-phase definition (retained)**.
- Model access (R8-9; DECISION-4 D4-3): local and cloud are options the person chooses among, with no default; a cloud model is reached by OAuth sign-in or an API key. V4-HOST-01 and V4-ARC-11, as amended by SCA-V4-001, state this for a host's agent. This boundary selects no default and carries the supplier's sign-in and API-key variants (§8.1 L-5; S-4).
- Network destinations (R8-13; DECISION-5): V4-HOST-02 as amended by SCA-V4-001 (DECISION-5; host-agent network destinations) governs a **host's embedded agent only**. The App's own Codex keeps the person's Codex configuration, approval and sandbox choices (ARCH §4, closing sentence of the host-agent property; §2 note; Root AGENTS.md; D-GOV-43). This boundary adds no allow list, destination prompt or destination gate to the App's Codex.
- Serves: OUT-001 (boundary definition), OUT-002 (version-identity and plan/revision seam definition; generated-output binding at the definition/generation pin — the generated bundles themselves are the W11 spike's, not this file's), OUT-003 (responsibility account, OI-008 *proposal*, local-provider requirement account, optional-reuse assessment), OUT-004 (recorded-exchange and upgrade method); REQ-001…REQ-008; designed cases for VER-001…VER-007
- Basis: the accepted basis as amended by scope-change amendments SCA-V4-001 (`_ScopeChange/SCA-V4-001_2026-09-28_2155/`, accepted 2026-09-29) and SCA-V4-002 (`_ScopeChange/SCA-V4-002_2026-09-29_1901/`), pinned by current bytes: `docs/PRD.md` sha256 bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd, `docs/ARCHITECTURE.md` sha256 317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c, `docs/HOST_INTEGRATION.md` sha256 d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f and `docs/EXAMINATION.md` sha256 471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0 (v0.6 pinned branch base `6e18505e3`, before both amendments; of the passages this file cites, the amendments changed ARCH §1 priority 3, the host-model line of the ARCH §2 diagram and ARCH §4); ScopeOfWork.md sha256 bbc81a8d31eeacab3497acf297c8c6eeac7b2f6febda5381f332ec14b8f65d02 (SCA-V4-003 revision; re-pinned at pass-4 closeout C1 under R23-5, was `9945e72b…cc75`; SCA-V4-003 blocks read: G-0101-01…04, none requiring a change to this file's design text); earlier revisions of the contract: (revised under SCA-V4-001, its AX-005, at `340ecf341`, and under SCA-V4-002, its AX-006, at `1efd4bcda`; v0.6 pinned the INIT contract eddd122c…4773); the accepted graph `_DAG/_LATEST.md` → DAG-003 (accepted 2026-09-29), cited for the admitted or held layer of register rows; `docs/ARCHITECTURE.md` §1 (priorities, M-2, M-4, M-6, M-7), §2, §3 (V4-ARC-01…05, "Properties the App must hold", reuse candidates, "Left to the implementation session"), §6, §7, §8; `docs/PRD.md` §2.1 (V4-APP-01…04), §4.3 (V4-EXE-01…04), §4.5 (V4-AUT-03/04), §4.7 (V4-REC-03), §5 (V4-CST-01/03/06), §6; `docs/EXAMINATION.md` §2 (V4-EXM-01…03), V4-EXM-11/12; current `_Decomposition/Open_Issues.csv` OI-008, OI-009, OI-012; `External_Dependencies.csv` DEP-005
- **v0.9 inputs (node F-A of run `APP-V4-DESIGN-PASS-3-20261001`; first-increment edits after the pass-3 design nodes).** Each sha256 recomputed with `shasum -a 256` in the working tree at this node (HEAD `e4e14d6ae6`); paths under `AgentRuns/APP-V4-DESIGN-PASS-3-20261001/`: `BRIEFS.md` sha256 316ea29325a0d45004ffd59c1b142d2e9f5c371ac765bce7c4b94898a57788d7 ("Common rules", "F — first-increment edits"); `F/F0_JOINS.md` sha256 e93608be1c6e3eb03e6194f3c6f415e3171492f9828b0fd80b4dccb81fe47dd9 (§1.1 rows FH-01…FH-44, §1.14, §2, §7.7); `R17_RESOLUTIONS.md` sha256 b0af81bcbad9bc52fddc99119c42a19019a9b174677d5b92a0a2f5c8b4f8e198 (R17-3, R17-8, R17-9, R17-14); `R18_RESOLUTIONS.md` sha256 abf5eee6324647ff9f126603ff189a21f847d5887f20e24e540fd9a6b4c0bd30 (R18-1…R18-9); `R19_RESOLUTIONS.md` sha256 16930ecdcead75118ee264bc78d3a7c4824212323cb9895b9a3c15478122a12c (R19-1…R19-8; **where an F0 row conflicts with R19, R19 is applied**, and the change table says so); `OWNER_DECISIONS.md` sha256 ea96c55710af41c94afe3721f8881bf5edc5bbfc9ad4d0d9ff68e20ca808e015 (DECISION-K3 as revised; DECISION-L L-1…L-7); `DECISIONS_PENDING_2.md` sha256 0ecbf87aae8d4350c6615ccf051e8808c828b285271574b6a48f4c6937b74f9b (read for the L options and the visibility list); `R20_RESOLUTIONS.md` sha256 516d0fe0d3cddb1ef98266e30b37f53067e94e467ad08313df6557a79f1fb1c3 (R20-3, R20-6 read for §8.2); the round-2 sections of `D/D1.md`, `D/D2.md`, `D/D4.md`, `D/D6.md` (§R2.3 join changes, applied at the coordinator's message). This file's own observation records, read and not edited: `OBS_2_0.158.0.md` sha256 61cc34ffb811eb270542042ce4cfdc195efb0c5be4b89dbbe73eb9b99e104ac0 and `OBS_3_0.158.0.md` sha256 554ac4451d11282450e3ec4a4192448adf67bda6a07820f84a698716c806a843 (§10.2, §10.3); `OBS_1_0.158.0.md` and `PIN_SPIKE_0.158.0.md` unchanged at the pins above. The pass-3 Design files of DEL-01-02…05, DEL-02-02 and DEL-02-04 are being stepped to v0.2 in parallel with this node; they are cited by their **v0.2 labels** and section only (RECOVERY-v0.2, NPTD-v0.2, NIR-v0.2, AAC-v0.2, ACCESS-v0.2, ACCOUNT-HOME-RECORD-v0.2, WR-v0.2, ROLE-v0.2), the section numbers as read in their working text at this node, to be checked by node F-E; their bytes are pinned in GUIDE's input table, which is re-pinned last. Reading note for owner names: by DECISION-L L-7 the App implementation owner is the Owner; this file keeps the role name "App implementation owner" where it names a point of decision.
- **RP-3 repair inputs (repair node RP-3 of run `APP-V4-DESIGN-PASS-2-20260930`; in place, no version bump).** Each sha256 recomputed with `shasum -a 256` in the working tree; paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/`: `R14_RESOLUTIONS.md` sha256 c6a603303693f50e24ea27fcbc9f381a297434e4182f023fbcee941073623576 (R14-5; R14-7's R13-6 item for HOSTING); `R13_RESOLUTIONS.md` sha256 d0385313660e5820258b4089372313f382afcebc57d37265389274ca470a8d3a (R13-6); `BRIEFS.md` sha256 e3f98d1c8449292965dd244a0f2821b221bcd0f3b0294e592f73b8eaaaaf6321 ("RP — repairs from V18", row RP-3); `comparisons/V18-2.md` sha256 0b00e79b161bcdf1e83a3a207d71114e316421e3cdf2ed5231901c14b85fbdb7 (M-1, m-10, m-13); `comparisons/V18-3.md` sha256 68a067e26af7557b6d1cf1f2d7c2816a9f81dd451d8a95d8f48bdaf72e7261e1 (m-17, m-20); `comparisons/V18-1.md` sha256 fb07e07c66c1a0a3fb7c2d58e1595d2a40ffc0ff9a7913a3bdbe2a70655dec5f (m-13: RS's side of U-27; nothing changed here); `WAVE_B/OBS-1.md` sha256 622c86113a19900d550a6e868480719ea3e2628753cc7b3fb7d98084042626e9; `WAVE_B/OBS-1b.md` sha256 5eb680de32e225da2f1bd799a3282776292467cfed01b448a2f5c177238d5079; `DECISIONS_PENDING.md` sha256 f1e968fe9cc0d40a78841c61834c0e075409949c6b52e6f08dd70f2221d6a73e (Part 3) and `OWNER_DECISIONS.md` sha256 b2fa81871cbf44b978894c8d0512c66d55a66e3c50db21df56e00ddbf651e05b (DECISION-K1: "Parts 3 and 4 stand as presented"). This file's own record `OBS_1_0.158.0.md` (with the OBS-1b addendum) sha256 7b984b541edca0b14534d29115e77642c587a32f830bdf25a94a7ecca882cc43 (its current bytes, re-pinned at node H after node G's redaction of §B.7; was 85707703e97b4fd5ea4332785aae83f96850bedacad5219c8827c41297c26182 as read at RP-3) is read, not edited. Siblings by label and section: DEL-02-01/WD-v0.8 §4.2.5 (same repair node); EXEC-v0.6 AE-6, AW-12; ADAPTER-v0.6 CT-9, CT-10, S-7, S-8. The return file is `WAVE_B/RP-3.md`.
- **Pins as of node A4 of this run's records (run `APP-V4-DESIGN-PASS-2-20260930`; in place, no version bump; R11-3; relabelled at RQ, V19-B n-1: later pins of the same records are in the Wave B input lines and in GUIDE's basis).** Each sha256 recomputed with `shasum -a 256` in the working tree at this pass; paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/`: `R9_RESOLUTIONS.md` sha256 a64e241519b7d158165a7ede0ffdd22eec0af15b6812b5300755f5f38abd59b8 (R9-1…R9-11; R9-2's second bullet as corrected by R10-1); `R10_RESOLUTIONS.md` sha256 ad3b6caa4a12660db77abc51b5c02ba70519ee46d55b40d21ee76eb3ca561796 (R10-1…R10-11); `R11_RESOLUTIONS.md` sha256 e7343b6663b6aeeb2dc506d3391f5b310088e7688d1b21e65d2ba1d8616b3615 (R11-1…R11-9, the repairs from review V17); `OWNER_DECISIONS.md` sha256 7458e9e81971676337a34280b4e8b29a7d04fce5fc202da5b9f5cf7ccd8f9ae5 (DECISION-K1). At node A4 these superseded for currency the earlier pins of the same records in this header and in the change-table rows, which record the bytes read at node A1 or A3.
- **v0.8 inputs (Wave B, node B6 of run `APP-V4-DESIGN-PASS-2-20260930`; design development).** Each sha256 recomputed with `shasum -a 256` in the working tree at this node; paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/`: `BRIEFS.md` sha256 ccb4d9f036fb7ff531fffa0d309533b15cf1ebb39b0320651ed4bd5d88efc550 ("Common rules", "Wave B — design development", round 1 row B6); `R12_RESOLUTIONS.md` sha256 95f3011b436b6faa3de098059e77eac836c165e0bb98a5ed94e28918a3a749a1 (R12-1…R12-3 binding; R12-4 and R12-8 read for OBS-1); `OWNER_DECISIONS.md` sha256 1dfd5bf4619b329719136b1646030e3f871fd7ffc52dbfd12265414e515aaf15 (DECISION-K1 including K1-6, and the model-download record with its recorder's correction); `SURVEY/S1-D.md` sha256 a3b0546af4131e0302520bc0dbaad8d6d5587e91d896fb8aa559e32768b19419 (HOSTING §4, §5 and §8 items 4–7; PIN_SPIKE §8); R9, R10 and R11 at the pins of the line above. Evidence read: the committed 0.158.0 JSON Schema bundles, `_spike/inventory.txt` and the eight redacted transcripts `generated/0.158.0/_spike/transcripts/*.jsonl` (all unchanged; `MANIFEST.sha256` unchanged); the spike's scratch material in the session scratchpad (`…/scratchpad/codex-0.158.0/`), read only: its eight unredacted handshake transcripts carry the same send and receive frames as the committed copies once the spike's own redaction is applied (8/8, by script, recorded in the node's return), and its TS output confirmed the three TS-only client methods and two TS-only notifications. The Codex binary was **not** run in this node; strings in the binary were read without executing it (F-28). DEL-02-03's current working text (node B2, in progress: its §2.5 reached-when table and §2.5.3 OBS-1 list O-1…O-9) and DEL-03-03 ADAPTER-v0.5 §3.5, §9 and UNRESOLVED were read for the OBS-1 brief. `PIN_SPIKE_0.158.0.md` is unchanged and not edited (R9-10). Produced beside this file: three PROPOSED schemas `hosting.lifecycle-event.schema.json`, `hosting.client-request-record.schema.json`, `hosting.server-request-entry.schema.json` and the local prototype `prototype/` (§9.6); the OBS-1 brief is `WAVE_B/OBS-1_BRIEF.md` in the run folder.
- Consumed inputs: **v0.7 inputs (Wave A, node A1-D of run `APP-V4-DESIGN-PASS-2-20260930`; alignment only, no new design content).** R9_RESOLUTIONS.md sha256 c3efe2ffa232dd9293202d4fc891eba4325afeb2e224fecdf8c1b4c5122a9d2c (R9-1…R9-11; binding; R9-7 rules the evidence route to DEL-04-03); that run's BRIEFS.md sha256 698d91d8217cee528812529fa353faac899b4bc1a5be5686552ad88dad6c469a ("Common rules", "A1 — alignment wave") and OWNER_DECISIONS.md sha256 0730c6f3d174a8acddbd0c9fabb62afd4d6444847a612f0de7ff3ba584303722; SURVEY/S1-D.md sha256 a3b0546af4131e0302520bc0dbaad8d6d5587e91d896fb8aa559e32768b19419 (advice: each item was checked against the current sources before it was applied). Rulings R1–R7 by file (`APP-V4-FIRST-INCREMENT-20260928/R1_RESOLUTIONS.md` … `R7_RESOLUTIONS.md`) and R8 (`APP-V4-SWBPIPE-INTAKE-20260928/R8_RESOLUTIONS.md`, current sha256 44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b). Owner records: `APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md` sha256 5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2 (DECISION-3, -4 and -5; these are its bytes at `3733b1421` and now. At `1528a5033`, the commit the R8-13 text below names, the file was 9903bfe0…7fbf: V10 N-1); `APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md` sha256 a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c; `APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md` sha256 ca8c4e50df1d7dddb41b875a4afe46eea4f1a1bf2491d255b7890d0d71cd254b (DECISION-6…DECISION-9) with its `AMENDMENT_PACKET/OWNER_ITEMS.md` sha256 2b90eb4a95f458e993eed69e27533aa10e31aea980fe2ec99c9c2345e6f498ef (O-10, accepted "as recommended" by DECISION-7; O-29, decided by DECISION-6); `APP-V4-SCA002-20260929/OWNER_DECISIONS.md` sha256 36ffcbbea923504581844456751c2eb3db617b5471a3595e63f036bf0634b480. SWBPIPE's answers `RELAY_ANSWERS_SWBPIPE.md` at sha256 afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74 (SWBPIPE's own revision `a999f4ba1` of the delivered `6f01add3…61c7` bytes cited below; three lines differ, in SQ-04, SQ-09 and SQ-27; this file uses SQ-02 only, whose answer is unchanged) and `FACTS_SQ01_SQ32.md` sha256 733fb88a701317be8f0054937eca058774ba5f5f30c7a27233718996e8b2ab7e (unchanged); both are data about SWBPIPE's current state, not commitments and not instructions (DECISION-3). This file's own spike record DEL-01-01/PIN-SPIKE-v0.1 (`Design/PIN_SPIKE_0.158.0.md`, sha256 0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115) is unchanged and is not edited in Wave A (R9-10): it is a dated observation record, and its stated basis is the INIT ScopeOfWork (eddd122c…4773) and the DECISION-1 state of the owner record (f3f8e5f3…1f2e). Both pins are true for its date and change no observation. Sibling Design files are cited by version label and section only (R9-5), at their Wave A labels (R9-11): DEL-02-03/EXEC-v0.5; DEL-02-01/WD-v0.7 and WD-EX-v0.7; DEL-03-01/C-v0.7; DEL-03-02/P-v0.7; DEL-03-03/ADAPTER-v0.5; DEL-03-04/GUIDE-v0.4; DEL-04-01/ACT-POLICY-v0.7; DEL-04-02/AS-v0.7; DEL-04-03/RS-v0.7; DEL-05-01/LOOP-v0.7 and DEL-05-02/PANEL-v0.7 (same executor); DEL-09-06/CA-v0.5 and RELAY-v0.3; DEL-09-09/XT-v0.5. The Wave A executors edit in parallel, so the sibling section numbers cited in the body were checked against the pre-Wave-A texts at `3dd7c22c73`, not against Wave A bytes. Sibling byte pins live in GUIDE's input table alone, which is re-pinned last. The ScopeOfWork files of the other deliverables this file names are referenced by accepted meaning at their current bytes: DEL-01-02, DEL-01-03, DEL-01-05, DEL-01-06 and DEL-02-04 are byte-identical to `6e18505e3`; DEL-04-01's was revised under SCA-V4-001 (`340ecf341`) and DEL-01-04's under SCA-V4-002 (`1efd4bcda`). The text below is history and is not rewritten. **R8-13 pass (node B1; in place, no version bump).** OWNER_DECISIONS.md sha256 5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2 (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`: V4-HOST-02, host-agent network destinations) and R8_RESOLUTIONS.md sha256 44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b (R8-13) at `1528a5033`; OWNER_DECISIONS.md in its state that adds the owner's DECISION-5 confirmation (committed with this pass); BRIEFS.md sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517 ("Common rules", "A-wave"). Revised in the same pass (node B1), versions unchanged: LOOP, PANEL, ACT, AS, RS, HOSTING, C, ADAPTER and GUIDE; their byte pins are in GUIDE-v0.3's input table. **R8-12 closing pass (node A6; in place, no version bump).** R8_RESOLUTIONS.md sha256 d4c3423310a857af86692d17ddfdd22fa877ee20b07c46e1ee481d1cd750e7af (R8-12: item 7 applied here). Current sibling versions after R8, as committed at `7a1508452` with A6's in-place R8-12 edits (their byte pins are in GUIDE-v0.3's input table): DEL-02-03/EXEC-v0.4; DEL-02-01/WD-v0.6; DEL-02-01/WD-EX-v0.6; DEL-03-01/C-v0.6; DEL-03-02/P-v0.6; DEL-03-03/ADAPTER-v0.4; DEL-03-04/GUIDE-v0.3; DEL-04-01/ACT-POLICY-v0.6; DEL-04-02/AS-v0.6; DEL-04-03/RS-v0.6; DEL-05-01/LOOP-v0.6; DEL-05-02/PANEL-v0.6; DEL-09-06/CA-v0.4; DEL-09-09/XT-v0.4; DEL-09-06/RELAY-v0.3; this file's own spike record DEL-01-01/PIN-SPIKE-v0.1 is unchanged. SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` and `FACTS_SQ01_SQ32.md` are unchanged (data about SWBPIPE's current state, not commitments; DECISION-3). **v0.6 inputs (R8 pass, node A4, at `94aa9181b`; read with `git show`):** `R8_RESOLUTIONS.md` (run `APP-V4-SWBPIPE-INTAKE-20260928`, sha256 1770c96e62caf14322811fca82ceb77eca450d3e1be8665cdbdd5550631e8d02; R8-1, R8-2, R8-9 applied, R8-11 read; the others checked, none addressed to HOSTING text), `OWNER_DECISIONS.md` of that run (sha256 a5ccab0d39bd1cab37c5556abc9bdedd5341ce76be4712706c8c9d72d623e776; `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3` and `-DECISION-4` with its clarification: D4-1 phased checkpoints, D4-3 model access), `INTAKE_MAP.md` (I2, sha256 3cc182955c0f3dd70efa0f1c051870229c2ccc08f36c5cf1445f2eef0dd1ea33; rows 01.14, 02.17, 16.2, 19.5, 29.3; Part 2 §2.2 HOSTING rows; Part 4.11 D6 row), `BRIEFS.md` (sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517; "A-wave"), SWBPIPE's delivered answers `RELAY_ANSWERS_SWBPIPE.md` (sha256 6f01add3977761e42ac6b310faf72ba4fd5455e478605deb83fefb2e4d3a61c7; SQ-02; data about SWBPIPE's current state, not commitments, DECISION-3), DEL-02-03/EXEC-v0.4 `EXECUTION_COMPATIBILITY.md` (sha256 d32be37797a3c367d342a2d13bbb8dd4279bc52934531d83b8c6ec8c6e7b76d4; §2.1 PH-1…PH-10, §2.2 GV-1…GV-5, §2.3 HP-1…HP-4 and HP-H, CH-22) and DEL-02-01/WD-v0.6 `WORKFLOW_DECLARATION.md` (sha256 fce565edfd0cee3fa4583eb292d11cce3e4121ead0cdbed31ba2fe0a52562f28; §4.3.0, §4.3.1 `governed`). **Earlier:** DEL-01-01/HOSTING-BOUNDARY-v0.4 (sha256 201ea32005dd2c9fb5281a376eb25eebfcb5a644d09a6d3bf5901aaf934c7e58, commit cc58211c5); **at commit 8fb51f07f, read with `git show` (current sibling versions):** `R5_RESOLUTIONS.md` (sha256 254d0b93b9959419a70c6737b07087e1db59b529adc3105a1db31f82b78dd6f1; R5-1, R5-4, R5-9 applied), `reviews/V3-B.md` (sha256 5662fbd09025f5ad9459861370159d606fcced76b394980199e861555a1954a3; m-5 and the m-1 note on §8.3), `reviews/V3-A.md` (sha256 f25f5af1177b7fe2a698bd4ef1e1caafa4c2ef25cfc73111f031e17c7cc21d87; no item addressed to HOSTING), DEL-02-03/EXEC-v0.2 `EXECUTION_COMPATIBILITY.md` (sha256 7f7848c0de2fdb4dc21f5adafa97f92e179bb66c9f6b04f3434d8f2342317af0; §2 HP-1…HP-4, HP-H; §3.6; §5 CAP-2/6/9; U-E20 withdrawn), DEL-03-03/ADAPTER-v0.2 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` (sha256 a2905dda5782d7a48fa35ef7e26b0c1517fd3bd995e3ddbba27d2426a25674bc; §3.4, §3.5, OC-2/3/6/7, F-3, F-9), DEL-04-03/RS-v0.4 `RECORD_SEMANTICS.md` (sha256 56806b64b12a946e706ff236dd1c25fe27ac00877aac13b50ee8603aaf540199; R5 model destination, R13 tool-permission settlements). EXEC-v0.3 and ADAPTER-v0.3 are being produced in the same R5 pass; this file cites their v0.2 bytes and R5-1's ruled values. **R6-4 (in place):** DEL-02-03/EXEC-v0.3 `EXECUTION_COMPATIBILITY.md` (commit d3cebd1cc, sha256 889e48819baa21ec112c4878e4e38004dcbaa9eb3645a31c24221ac116ee548e) consumed for §2 HP-1…HP-4, HP-H and the HP-4 scope ruling. Earlier: DEL-01-01/HOSTING-BOUNDARY-v0.3 (sha256 34c3383402aabe6e9347aa2f111318538c4a2a4ca85adb8fffff7e439fdde94e, commit ba0b37123); **at commit f05c7e4cd, read with `git show`:** `R3_RESOLUTIONS.md` (sha256 202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf; R3-1…R3-4 read, none addressed to HOSTING), `R4_RESOLUTIONS.md` (sha256 50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24; R4-1, R4-2, R4-12, R4-13, R4-19 applied), `OWNER_DECISIONS.md` with Decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (sha256 a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c; D5, D6), DEL-02-03/EXEC-v0.1 `EXECUTION_COMPATIBILITY.md` (sha256 e0ede76ebf08003511755afc666be2466a867fd3256837ee94300cd0dfe518e8; superseded, see above), DEL-03-03/ADAPTER-v0.1 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` (sha256 58b2409ca45ceea66160eb8910ca38b76b6f335dc184eaeb0896e93cabd0a074; §3.4, §3.5, OC-3, F-3, F-9); the committed 0.158.0 JSON Schema bundle `json-schema/experimental/codex_app_server_protocol.v2.schemas.json` and `_spike/inventory.txt` (for the MCP surface and `turn/interrupt` facts in §6.7–§6.8). Earlier: DEL-01-01/HOSTING-BOUNDARY-v0.2 (sha256 16711a83fec3439d7be634f6d62512be2a87f0dec32bd84028a39425bc84007a) and v0.1 (sha256 f1da7f76f686991f67b3e974478b9b453df804839712a7e5cc24e7bc4849d728); DEL-01-01/PIN-SPIKE-v0.1 `Design/PIN_SPIKE_0.158.0.md` — **current committed revision sha256 0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115** (commit 28bd00499; the parent's post-IR1 edits: SV-02 committed-tree wording, "what the spike proposed to commit" note, git-operations statement). Earlier revisions: v0.2 of this file consumed the **pre-correction** revision sha256 3d66ad28f3fa76a19826a09a7d8269f598bb4465912b6375f74bc4d56678f3cf; IR1-C reviewed sha256 26ea0c2fae8212ca46ed2ff60ddfaef5ca28e0ed73aae2105017d7ceccb40334 (commit c387730fb). `Design/generated/0.158.0/MANIFEST.sha256` (sha256 42b95826d7bd6d58df7941da7420064ee55d54a347a2eab22eafbfa16231569e, byte-unchanged) and `Design/generated/0.158.0/COMMITTED_STATE.md` (sha256 2cb7f1d29383e68239d085186401488c5d864046475b7cf9d3bc256f85782608); run `APP-V4-FIRST-INCREMENT-20260928`: `OWNER_DECISIONS.md` (Decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, sha256 f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e at that time), `R1_RESOLUTIONS.md` (sha256 2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4; R-1, R-2, R-4, R-10 applied), `comparisons/V1-A.md` (sha256 01811533bf0aedad5326d1517561187682a572ae3f47c5f8b8637e48cfe04c09; D-13, D-14, RF-03), `comparisons/V1-C.md` (sha256 8d46258ad0120067f6472442de67feacba8405462b78abb8bac34be28a4a94a6; D-16, D-22, §6, AG-13…15, AB-10, RF-6), `R2_RESOLUTIONS.md` (sha256 77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088; R2-22 applied, with R2-8 and R2-11), `reviews/IR1-C.md` (sha256 295e96b3f5871cdf4142df169dc8811cef0aa38e7a7eb1930b246f60f0a426b9; IR1C-04, IR1C-18, IR1C-19, IR1C-20 addressed to HOSTING). DEL-01-02…05, DEL-01-06, DEL-02-04 and DEL-04-01 remain referenced by accepted meaning (ScopeOfWork.md at 6e18505e3); DEL-04-01 act names are used as fixed by R-1. Root D-GOV-43 is governance context only (§2). Concept-run returns T7/T11 and v3 code remain dated historical evidence.
- Receivers (R9-6: rebuilt from the ACTIVE rows of this register and of the consumers' registers; layer per `_DAG/_LATEST.md` → DAG-003; table in §8). **This register's rows:** DEL-01-02 (OUT-001; REQ-001, REQ-003, REQ-004, REQ-005, REQ-007; TBD-002) via DEP-01-01-019; DEL-01-03 (OUT-001; REQ-001, REQ-004) via DEP-01-01-020; DEL-01-04 (native request/answer interaction) via DEP-01-01-021; DEL-01-05 (OUT-004; REQ-003, REQ-007, REQ-008) via DEP-01-01-022, with DEP-01-01-024 the UPSTREAM row for its sign-in and substitution evidence (held); DEL-01-06 (distribution identity for packaging) via DEP-01-01-023. **Consumers among the first-increment deliverables, from their own registers (all six arcs admitted):** DEL-02-01 (DEP-02-01-025, N-16: harness-capability meaning; this file holds the 0.158.0 inventory, and a capability meaning beyond the inventory is named by that row and not yet defined here, §8); DEL-02-03 (DEP-02-03-023, N-23: observed supplier facts as capability information; §6.1, §6.7, §6.8, §10, R9); DEL-03-03 (DEP-03-03-013, N-B4: MCP and dynamic-tool surfaces, channel status, model destination; §6.8, §8.3); DEL-03-04 (DEP-03-04-021, N-B9: native surfaces for optional external access; §6.8); DEL-04-03 (DEP-04-03-027, N-15: supplied guidance, model and destination, tool-permission settlements, supplied to it directly, R9-7; §8.2, §8.3, R8, S-7); DEL-09-06 (DEP-09-06-032, N-C5: App-side supplied-guidance and model-destination evidence; §8.2, §8.3). **Consumers outside the first increment, from their own registers:** DEL-02-04 (DEP-02-04-010, admitted: additive guidance, seam S-6; this register has no DOWNSTREAM mirror row, F-16); DEL-06-01 (DEP-06-01-013), DEL-09-01 (DEP-09-01-019) and DEL-09-02 (DEP-09-02-009), all admitted; and the consumer-side rows of the PKG-01 receivers (DEP-01-02-018, DEP-01-03-011, DEP-01-04-007 and DEP-01-06-006 admitted; DEP-01-05-012 held; DEP-01-05-013). DEL-05-01 and DEL-05-02 (J9: guidance carriage, answer origin) have no register row to this deliverable. App implementation owner (OI-008 proposal, reference-generator choice, pin re-examination). Under owner decision D1 the standalone-App definitions DEL-01-02…05 were left to a later undertaking; run `APP-V4-DESIGN-PASS-3-20261001` started them (with DEL-02-02 and DEL-02-04), and from v0.9 their Design files make the receiving comparisons: S-1 RECOVERY-v0.2 §1 (reconciliation with §6.5) and §4.2 (consumed) (DEL-01-02), S-2 NPTD-v0.2 §2 (DEL-01-03), S-3 NIR-v0.2 §4–§6 with AAC-v0.2 (DEL-01-04), S-4 ACCESS-v0.2 §19 (DEL-01-05), S-6 ROLE-v0.2 §5 (DEL-02-04), and the workflow run-start supply of WR-v0.2 §16 (DEL-02-02; §8.2) (F-15 closed). The arcs N-18, N-21, N-24 and X-1 have no end in DEL-01-01; X-1's supplier, DEL-01-04, is the receiver of seam S-3.

**Reading note.** Element names defined by this file (for example *request
identity*, *generation*, *version identity record*) are **semantic** names,
not wire fields, types, files or persistence choices. Supplier method, field
and value names appear where they are **observed supplier facts at 0.158.0**
from the W11 spike record (cited as `SPIKE §n` / `S-F-nn`); they are
supplier facts, not Chirality wire choices. Standing labels follow the spike:
`observed`, `observed-in-generated-types`, `published-only`, `not-observed`.

**Pin.** Owner decision D4 selected Codex **0.158.0** as the
**definition/generation pin** for this undertaking. It is not a
qualification (DEP-005), and it is re-examined before implementation starts.
0.154.0 (v3 pin) and 0.156.1 / 0.157.1 (dated upstream reports) remain
historical evidence only.

**Version rule (R19-5; from v0.9).** Codex changes significantly between
versions, so a pin lasts only so long. Every statement in this file that
rests on a supplier fact names the version it was seen at (here 0.158.0,
with the OBS records' local pairing where they are the source). Where Codex
reports a capability at run time, the App reads it rather than inferring it
from the version: at 0.158.0 for example the request's `availableDecisions`
(R5), `Model.multiAgentVersion` and the provider's `namespaceTools` (§8.4
HCG-A08), `experimentalFeature/list`, `config/read` with its layers,
`skills/list`, and `instructionSources` on thread start (§8.2). A
version-advance check (regenerate the types, diff, rerun the OBS harnesses
under `prototype/obs1/`, `obs2/`, `obs3/`, list the statements affected) is
proposed as a later node; its scheduling is open (§9.5).

**Act names.** Canonical names from R-1 are used: A14 *answer tool
permission* for the supplier's tool-use prompts, and A4–A7, A12, A13 for the
acts reserved to the person by owner decision D2. Following R-4, "approval"
in this file's own prose means only A6 (engineering approval). Supplier names
that contain "approval" (for example `item/commandExecution/requestApproval`)
are quoted as supplier names and denote A14 subjects.

---

## Changes from v0.8

Node F-A of run `APP-V4-DESIGN-PASS-3-20261001`: first-increment edits after
the pass-3 design nodes, D round 2, OBS-2 and OBS-3. Rows are keyed by the
F0 row (F/F0_JOINS.md §1.1, §1.14) and the ruling. Where an F0 row conflicts
with R19, **R19 is applied** and the row says so. Every boundary rule of
v0.8 stands except where a row says otherwise; new structures are PROPOSED
unless a row names the deciding text.

| Row / ruling | Change in v0.9 | Where |
|---|---|---|
| FH-44; §1.14 (L13) | Version v0.8 → v0.9; v0.9 inputs line; Receivers line names the pass-3 Design files that make the S-1…S-4 and S-6 receiving comparisons. Status stays DRAFT | Header |
| R19-5 | Version rule: supplier facts name their version; runtime reads preferred over version inference; version-advance check proposed as a later node | Header "Version rule"; §9.5 |
| DECISION-L L-1; R19-4; R18-1 C-20; FH-06, FH-31 | One child per App-owned home; H5 generation identity {App session, App-owned home, spawn counter}; §4 states per home; U-12 gains the per-home dimension (report only, R17-2) | §1; H5; §4.1; U-12 |
| FH-01; R17-3; R18-1 C-12; D1 H-1 | §4.5 and the §4.6 stop row cite DEF-5a (RECOVERY-v0.2 §2), reached by a confirmed quit (DEF-6) or DEL-01-04's Stop/Restart Codex, per home; DEF-3 and DEF-4 never stop the process; the process group ends at a deliberate stop (OBS-2 §11) | §4.5; §4.6; H11 |
| FH-02 | §4.5 step 2: no App decline at stop or quit; entries end `ended-unanswered(process-exit)`; U-10 closed | §4.5; U-10 |
| R18-7 G-5; D1 H-9 | §4.5 step 3 states Codex 0.158.0's graceful-stop history note (closing input writes "the user interrupted … on purpose"; a kill writes nothing; both read back `interrupted`); the App's label comes from its own record (RECOVERY-v0.2 §5 SQ-Q) | §4.5 |
| FH-03; R17-9 | R3: no App rule declines a waiting request after any period; `timed_out` never sent; U-11 closed | §6.3 R3; U-11 |
| FH-04 | §6.5 reconciled (RECOVERY-v0.2 §1); U-14 and F-01 closed | §6.5; F-01; U-14 |
| FH-05; R18-1 C-03; D1 H-10; D2 J-3 withdrawn | Observer re-attachment: per-generation journal replay (OA-01) or snapshot + Codex history with a gap marker (OA-02); a closed generation's events are not re-read; §12's "which component re-attaches" answered | §4.6 observe row; §5 Order; §12 |
| FH-07; D1 H-6 | U-09 narrowed (closed for the `turn/interrupt` before-reply trigger); U-16 cites RECOVERY-v0.2 §6's PROPOSED policy | §6.2; §6.2.1; U-09; U-16; §4.4 |
| FH-08; FH-38; §1.14 (L985, L986) | "Outside this increment, D1" pointers re-pointed to RECOVERY, NPTD, NIR/AAC, ACCESS, ROLE (v0.2 labels); DEL-02-04 receivers row notes the mirror row is still a register proposal | H3; §6.4; §8 S-1, S-7; §8 receivers table |
| FH-09 | §6.7 HP-2: live effect observed at OBS-2 (O-1, O-3); the App sends it for DEF-3 and the quit interrupts with a stop request written first (RECOVERY-v0.2 §3.4) | §6.7 |
| FH-10; K-1; R18-6; L-3; R18-3; D4 FH-10, FH-14 | §4.2 step 3: spawn with `CODEX_HOME=<App-owned home>`; `config.toml` (and, by R18-6, `AGENTS.md` and `skills/`) linked to the person's; observed at OBS-2 O-6; fallback not needed at 0.158.0; session flags carry analytics off and, only in the fallback, `plugins = false`; plugins follow the person's setting; no internal environment variable and no credential variable passed; no workflow in any skill root (R19-7) | §4.2 step 3; H9 |
| FH-11; K-5; C-05 | §4.2 step 4: `experimentalApi: true` recorded per generation (NPTD-v0.2 §4 EX-2); `explicitGatewayOauth: true` (PROPOSED, ACCESS-v0.2 Q-1); what needs the opt-in at OBS-2. F0's premise note applied: the edit lands at §4.2 step 4 **and** F-13 | §4.2 step 4; §7.3; F-13 |
| FH-12 | Configuration identity adds the home, the linked files' targets and the session flags; never a credential | §7.1 |
| FH-13 | Label probe uses the separate probe home H-probe | §7.2 |
| FH-14 | H9: the account-home element is decided (K-1); carriers per element | H9 |
| FH-15 | §6.1 partition: DEL-01-04's answer path and decline forms per kind (NIR-v0.2 §4.1, §4.3); `account/chatgptAuthTokens/refresh` known-app-unsupported (ACCESS-v0.2 CR-9); U-20 narrowed | §6.1; U-20 |
| FH-16 | RT-08 guard names the negative forms per kind (incl. the PROPOSED empty answer map and empty grant) or `submittedAs` *decline*; `cancel` observed as decline + interrupt | §6.2.1 RT-08 guard and note |
| FH-17 | Secret answer values not kept readable after the reply is written: redaction marker in the entry. **Schema changed** (`secretValuesPresent`, `redaction`, conditional rule); two new fixtures | §6.1 settlement; `hosting.server-request-entry.schema.json`; `prototype/fixtures/` |
| FH-18; R18-1 C-10 | Actor reference: a string "person:‹name›/‹OS account›/‹Codex account› (identity not verified)" from AAC-v0.2 §7 sources; Codex account in RS's `codexAccount` form; plan type not part of it. **Schema changed** (`actorRef` pattern); one new invalid fixture | §6.1 settlement; schema; `prototype/fixtures/` |
| FH-19; R18-7 G-1; D4 FH-19 | S-1…S-4 receiving sides cited; F-15 closed for every seam, S-4 by ACCESS-v0.2 §19 | §8 seams; F-15; header |
| FH-20 | §11 rows point to RECOVERY, NPTD, NIR/AAC, ACCESS, WR, ROLE (meaning unchanged) | §11 |
| FH-21; R18-5 | R9 person-input bullet cites AAC-v0.2 and NIR-v0.2 LB-4 (an "Open the App act control" entry, never pre-filled) | §6.3 R9 |
| FH-22 | U-26: DEL-01-04 accepts the refusal order and gives each reason words (NIR-v0.2 §4.4) | U-26 |
| FH-23 | §6.8 configuration writes: explicit `filePath`, `expectedVersion`, no credential; writes through the link not observed | §6.8 |
| FH-24; L-1; L-6 | §8.1 L-5: flows offered and not offered; the key in H-key (no longer waiting on U-A1); no sign-in observed | §8.1 L-5 |
| FH-25 | §8.3: class from the access entry kind | §8.3 |
| FH-26 | §9.1 redaction categories: account-method credentials and URLs, error texts, email; secret answers; provider-bound installation and thread/session/turn ids; time zone; skill paths (OBS-3) | §9.1; U-13 |
| FH-27; L-3 | F-14: per App-owned home and only with plugins on; `plugins = false` stops the fetch (O-7) | F-14 |
| FH-28 | F-18 under K-1 | F-18 |
| FH-29; R18-3 (C-25); L-3 | §8.1 L-4 and U-18: K-12 decided; O-7 fills which setting stops which connection; plugins follow the person; the internal environment variable is not used; the remote-control loop shown as observed (no socket without sign-in) | §8.1 L-4; U-18 |
| FH-30 | U-03 closed at choice level; M4/M5 and writes through the link stay open | U-03 |
| FH-32 | U-22 and F-31 extended: delegation tools travel in the dropped `namespace` tool (O-4); carried into ACCESS-v0.2 §11 CH-2 | §8.1 L-3; U-22; F-31 |
| FH-33; R18-1 C-04, C-05; D2 J-2 | HCG-A08's signal replaced: `Model.multiAgentVersion` ≠ `disabled` and provider `namespaceTools`; `features.multi_agent = false` reads missing; not established otherwise; delegation not labelled experimental; adapter-observed child facts (`multiAgentMode` is "@deprecated Ignored" on thread and turn start in the 0.158.0 bundle, checked) | §8.4 HCG-A08 |
| R18-7 G-3; D2 J-10 (in part) | Goals placed in §8.4: the model's goal tools beside HCG-B04's goal methods and notifications; **no new Part A group** (D2 J-10 asked for one): a group with no App Server member adds nothing to the account, and DEL-02-01's check S-11 (VC-31) expects 27 groups, so a new group needs F-D's change first | §8.4 |
| FH-34; D6 FH-34 | F-20: consumed by ROLE-v0.2 §4.3; child-role facts observed through the adapter; `instructionSources` only `[]` seen | F-20 |
| FH-35; D2 J-4 | VC-09 cites NPTD-v0.2 §5.2 RV-1, RV-2; plan mode yields only a `plan` item (O-8); S-2 and HCG-A09 note it | VC-09; §8 S-2; §8.4 HCG-A09 |
| FH-36; **R19 wins over F0** | S-6: role guidance only as `developerInstructions` on `thread/start`; resume and fork accept and ignore it; `baseInstructions` never set; a workflow is a text element of the run-start `turn/start`, composed by DEL-02-02 (R19-7). F0's "on … resume must read accepted, not applied" is applied; F0's idle-point policy is replaced by "role fixed for the conversation's life; edits reach new conversations" (L-2, R19-3) | §8 S-6; §2 table |
| FH-37; **R19 wins over F0**; D6 FH-37 | §8.2 carriers table at 0.158.0. F0 asked to add `thread/fork` and `collaborationMode` developer text as carriers: under R19-8 a fork **ignores** new instructions (OBS-3 W-6, W-6b), so it is listed as accepted-not-applied and the App sends none; under R19-7 neither `collaborationMode` developer text nor `thread/settings/update` is used for workflows (recorded if ever non-null). Role-guidance evidence at thread start only; workflow run-start text recorded with DEL-02-02's source identity, checked against `thread/read` by the composing owner; `skill` and `mention` inputs recorded as not used (R19-7); the run-end line (R20-3) and the handoff summary (R20-6) noted; P-15's open half observed | §8.2 |
| FH-39; D6 FH-39 | Per-thread role configuration limited to additive `agents.<ROLE>.*`; never `features.*`, `agents.enabled`, `agents.max_depth`, approval or sandbox; the observed honouring used the home `config.toml`, and the App's own carrier is not observed (ROLE-v0.2 CR-1a, U-R3) | §8.2 |
| FH-40 | No change (record only): DEL-02-02's supply to DEL-02-04 is superseded by R19-7 (DEL-02-02 composes run-start text itself); S-6 names DEL-02-02 | — |
| FH-41 | New §10.2 (OBS-2, OB2-1…OB2-11, with the adapter and S-9 standing notes) and §10.3 (OBS-3, OB3-1…OB3-7); §10's still-to-observe note; U-19 narrowed | §10; §10.2; §10.3; U-19 |
| FH-42 | §4.4 "Recovery reads": `thread/read` before resume; no re-raise; `deprecationNotice` on full reads; prefer `thread/turns/list`, `thread/items/list` | §4.4; §4.3 step 4 |
| FH-43 | RT-10 provoked live (O-3): `serverRequest/resolved` after `turn/completed`; late answer ignored | §6.2; §6.2.1 RT-10 guard |
| R19-8; OBS-3; new finding | F-33 "Accepted is not applied" | §13 |
| Prototype | Rerun: 35/35 pass (model), exit 0; no program file changed; three new entry-schema fixtures | §9.6; VC-28 |
| RX (residual sweep of run `APP-V4-DESIGN-PASS-3-20261001`; in place, no version step) | D3 round-2 J-H11 (supports FH-43): R4 states why `already-resolved` matters (OBS-2 O-3: Codex silently ignores an answer after its own resolution; NIR-v0.2 §4.4 CS-6). D5 round-2 J-28 (FH-40): §8.2's composing owners named per carrier (DEL-02-04 role guidance; DEL-02-02 the run-start text and run-end line, with its supply check). Citations of WR-v0.2's "run-start supply" now give WR-v0.2 §16 (§16.2 composition and TX-5, §16.6 supply check) | Header Receivers line; §2 table; §6.3 R4; §8 S-6; §8.2; §11; F-15 |
| RV21 (repairs from review V21 of run `APP-V4-DESIGN-PASS-3-20261001`; in place, no version step; R21-1; V21-B M-1, m-5, m-6, m-8, m-9 rows 9 and 11) | **M-1:** HCG-A08 states the receivers' reading order of R21-1 (`namespaceTools` false reads missing), matching NPTD-v0.2 §7.1, EXEC EV-3a and WD §4.2.5; the signals are unchanged. **m-5:** §4.2 step 3: the session flags carry the K-12 settings and, if ROLE U-R3 selects `-c` flags as the child-role carrier, the additive `agents.<ROLE>.*` entries of §8.2 (was "only the K-12 traffic settings"). **m-6:** §8.4 goals note cites "NPTD-v0.2 §6.4; §9 TA-5". **m-8:** seam S-1's receiving side cites RECOVERY-v0.2 §1 (reconciliation with §6.5) and §4.2 (consumed), in the Receivers line, §8 S-1 and F-15 (was "§1 (receiving comparison)"). **m-9 row 9:** §6.1's decline-form sentence names RT-08 as this file's §6.2.1 row, not NIR's. **m-9 row 11:** §6.7 HP-2 cites EXEC-v0.7 §2.3 (HP-2 unchanged there); "the group set WD-v0.8 §4.2.5 resolves against" (§8.4 goals note) is kept, deliberately the v0.8 set | §4.2 step 3; §6.1; §6.7; §8 S-1; §8.4 HCG-A08 and goals note; §13 F-15; Receivers line |
| C0 (closeout of run `APP-V4-DESIGN-PASS-3-20261001`; in place, no version step; R21-6; V21b-B n-1) | §8.2 table, run-start text element row: the per-run supply evidence is "checked against Codex's history" read with `thread/items/list` (§4.4 "Recovery reads"; WR-v0.2 §16.6 SC-3; R21-4), not "against `thread/read`"; the "Applied at 0.158.0?" cell keeps OBS-3 W-4's observation, labelled as made through `thread/read`, with `thread/items/list`'s return of the same item labelled observed-in-generated-types. The FH-37 row above ("checked against `thread/read` by the composing owner") keeps its words as history; the §4.4, §8.4, §10 and §13 mentions of `thread/read` are observations or method inventory, unchanged. No boundary rule changes; prototype rerun 2026-10-02: `run_cases.py` TOTAL 35, FAIL 0 (`closeout/C0.md`) | §8.2 |

## Changes from v0.7

Wave B of run `APP-V4-DESIGN-PASS-2-20260930` (node B6): design development
under R12. Every boundary rule of v0.7 stands. New structures are
**PROPOSED** unless a row says an accepted text or ruling decides them.
Rows are keyed by the survey item (S1-D, HOSTING §8) and the R12 item they
answer.

| Survey item / R12 ID | Change in v0.8 | Where |
|---|---|---|
| R12-1 | Version v0.7 → v0.8. Status stays DRAFT: unsupplied, unimplemented and not accepted | Header |
| S1-D HOSTING 4; F-27 | **Harness-capability account at 0.158.0**: the 19 supplier item kinds, 11 server-request kinds, 170 client methods, the client notification and 85 notifications, each placed in exactly one capability group (HCG-A01…A17 agent capabilities, HCG-B01…B10 hosting and management surfaces), each with its variant and standing label; a meaning and the availability signals the generated types show for each agent capability. The group labels are this file's; portable capability names stay DEL-02-01's (WD U-08). Completeness checked by the prototype | §8.4; §8 closing paragraph and DEL-02-01 row; F-27 |
| S1-D HOSTING 5; R12-1 (interfaces, states, sequences) | **Lifecycle operations table** and failure behaviour of the start and stop sequences step by step; **lifecycle transition table** LT-01…LT-23 | §4.6, §4.7 |
| S1-D HOSTING 5; R12-1 | **Client-request path operations table** and **client-request record transitions** CR-01…CR-08; new PROPOSED outcome `refused-not-sent` with reasons `not-ready` and (governance phase only, HP-4) `run-holding` | §5.1, §5.2 |
| R12-1 (states) | **Register transition table** RT-01…RT-13; PROPOSED order of the §6.4 refusal reasons; PROPOSED reading of `serverRequest/resolved` after a written reply as an acknowledgment observation (U-09 stays open); R1 applied while handshaking (entry at receipt, delivery at `ready`) | §6.2.1; §6.4; U-09 |
| R12-1 (data); R12-2 | Three **PROPOSED schemas** (JSON Schema 2020-12) for formats this file defined only as element meanings: lifecycle event (§4.7, with the §7.1 version identity record), client-request record (§5), server-request register entry (§6.1). Valid and invalid conformance fixtures; placement not chosen (R12-2) | `hosting.*.schema.json`; `prototype/fixtures/`; §9.6 |
| S1-D HOSTING 6; R12-3 | **Supplier double** seeded from the eight recorded spike transcripts, with an executable model of this file's rules, run locally for the cases this file marks runnable with a double (VC-03, VC-04, VC-06, VC-08 part, VC-10, VC-14 part, VC-16, VC-20…VC-26) and for new checks VC-27…VC-30. All give the expected result against the model; no VER criterion is passed | `prototype/`; §9.6; Verification cases |
| R12-1 (verification) | Each designed case states what it needs and, where it ran, what it produced | Verification cases |
| S1-D HOSTING 6 (VC-26) | PROPOSED per-turn reading of the effective model destination, exercised by the double | §8.3; U-27 |
| S1-D HOSTING 7 | The next observation, **OBS-1** (one live Codex turn at 0.158.0 against a local LM Studio model, calling a test tool; DECISION-K1 K1-6), is briefed in `WAVE_B/OBS-1_BRIEF.md`, with two test-double tools in `prototype/`. §10 and U-19 say which still-to-observe items it covers | §10; U-19; `prototype/obs1_*.py` |
| New findings | F-28 (binary strings on local providers; OBS-1 risk), F-29 (the prototype's validity reference is the committed JSON Schema bundle; U-15 not chosen), F-30 (dispatch order and the reached-when table) | §13 |
| New UNRESOLVED | U-26 (refusal order and `refused-not-sent`), U-27 (per-turn effective destination reading) | UNRESOLVED |
| **R13-6** (V18-2 m-13; V18-3 m-20; repair node RP-3, in place, no version bump) | New **§10.1**: OBS-1 and OBS-1b as dated observations at pin 0.158.0 (LM Studio 0.4.16, one model; not qualification), OB-1…OB-12: the `namespace` tool dropped on the local Responses route and its consequence for App users on that route (no host MCP tools); the command-line path observed; the approval-setting quirk; `serverRequest/resolved` observed; the start-up traffic to chatgpt.com and github.com with analytics off and no sign-in, against U-18 and the start-up item the owner left for the phase review. Carried into §8.1 L-2, L-3, L-4; §8.3; §6.2.1 acknowledgment reading; §6.3 R5; §6.8; §7.3; §10's list; F-30; new F-31, F-32; U-09, U-18, U-19, U-22, U-27; VC-12, VC-26 | §6.2.1; §6.3; §6.8; §7.3; §8.1; §8.3; §10; §10.1; §13; UNRESOLVED; Verification cases |
| **R14-5** (V18-2 M-1, m-10) | F-27 **closed** by citing WD-v0.8 §4.2.5's group column (HC-7). The grouping of `functionCallOutput` (HCG-A06), `mcpServer/elicitation/request` (HCG-A07) and `thread/shellCommand` (HCG-A02) stands, with notes: client methods in Part A groups are App-origin calls; the three members annotated in the meaning table; nothing returned. New VC-31 (run by DEL-02-01's prototype) | §8 receivers table and closing paragraph; §8.4; F-27; Verification cases |
| V18-3 m-20 (inference) | HCG-A05's availability signals add `namespaceTools` (provider capabilities), with the observed route limit | §8.4 |
| V18-3 m-17 | Lifecycle receivers: DEL-02-03 (EXEC AE-6, AW-12) and DEL-03-03 (ADAPTER CT-9, CT-10, S-7, S-8) are told of an unexpected exit and a stop, beside DEL-01-02 and DEL-04-03 | §4.3 step 4; §4.6; §4.7 LT-12, LT-23 |
| (verification) | Prototype rerun after the repair: `python3 run_cases.py`, 35 results, all as expected (`prototype/results/RUN_2026-09-30_RP-3.txt`) | `prototype/results/` |
| RX (residual sweep; RP-1 return §4) | §6.8 names the required-tool check's catalog read as an App-origin read (ADAPTER-v0.6 §7.7; EXEC-v0.6 §3), recorded with initiator App; its carrying surface is left open, and a use of `mcpServer/tool/call` for it stays under U-24 | §6.8 |
| RQ (repairs from V19; in place, no version bump) | V19-A m-2 (carried here for consistency with OB-1 and the OBS record): L-3 and F-31 state what OBS-1 observed (LM Studio logged the `namespace` tool type as unsupported; no MCP tool reached the model) and label "Codex offered them as a `namespace` tool" the record's inference, as OB-1 already does. V19-B n-1: the node-A4 pins bullet relabelled. No prototype file changed | Header; §8.1 L-3; F-31 |
| C0 (closeout; V19b m-4; in place, no version bump) | §6.8's preamble no longer says no surface was exercised live: `mcpServerStatus/list` and `mcpServer/startupStatus/updated` were observed live at OBS-1 (§10.1 OB-10; one local route; not qualification), and the first row is marked *Observed (OBS-1)* with what was seen. No prototype file changed | §6.8 |
| H (current pins; brief "H" of run `APP-V4-DESIGN-PASS-2-20260930`; in place, no version bump) | The header's pin of this file's own record `OBS_1_0.158.0.md` is brought to its current bytes, `7b984b54…cc43`, after node G's redaction of the rollout file name in §B.7 (R16-3); the RP-3 value `85707703…6182` is kept beside it as read then. No body text, case or prototype changed | Header (RP-3 inputs line) |

## Changes from v0.6

Wave A of run `APP-V4-DESIGN-PASS-2-20260930` (node A1-D): alignment to the
amended basis and the revised ScopeOfWork, under R9. It adds no new design
content, and every boundary rule is unchanged. Rows are keyed by R9 ID and by
the survey item (S1-D, HOSTING §8) each change answers.

| R9 ID / survey item | Change in v0.7 | Where |
|---|---|---|
| R9-11 | Version v0.6 → v0.7. Status stays DRAFT: unsupplied, unimplemented and not accepted | Header |
| R9-5; S1-D HOSTING item 1 | Header re-pinned: the four basis documents by current sha256, naming SCA-V4-001 and SCA-V4-002; ScopeOfWork `9945e72b…cc75` (v0.6 pinned the INIT contract `eddd122c…4773`); `_DAG/_LATEST.md` → DAG-003; R9 with the run's briefs, survey and owner record; R8 at its current hash; the owner records of the two amendment runs; SWBPIPE's answers at `afb6e063…0e74`; siblings by Wave A label and section only. The statement on the other deliverables' ScopeOfWork files is corrected (DEL-04-01's and DEL-01-04's were revised). The OWNER_DECISIONS pin `5fd780bf…` is tied to its commit `3733b1421` (V10 N-1). History text is not rewritten | Header |
| R9-10; S1-D PIN_SPIKE item 2 | `PIN_SPIKE_0.158.0.md` is not edited. The header states its standing: PIN-SPIKE-v0.1 unchanged; its basis is the INIT ScopeOfWork and the DECISION-1 state of the owner record | Header |
| S1-D HOSTING item 1 | The body citation "EXEC-v0.2 HP-2" is re-pointed to EXEC-v0.5 §2.3, and the other live EXEC, LOOP citations carry the Wave A labels (R9-5) | §2, §6.7 |
| R9-1, R9-3 | §6.7's Phase-1 statement cites the amended V4-WF-05 and says that the required act is requested by the agent carrying out the workflow; this boundary issues no request in the agent's place, and how an App run observes an arrival and a request is DEL-02-03's (EXEC, Wave B). No hold-point fact changes | Header, §6.7 |
| R9-4; S1-D HOSTING item 2 | The §2 scope note cites the amended ARCH §4 sentence that now states the scope ("This property governs a host's embedded agent; …"). §8.3 "record and show" becomes SETTLED (owner item O-10). L-5, F-24 and F-25 cite V4-HOST-01 and V4-HOST-02 as amended | §2, §8.1 L-5, §8.3, F-24, F-25 |
| S1-D HOSTING item 2 | L-4, F-14 and U-18 are restated against the amended ARCH §1 priority 3, which now speaks of a host's agent and states no App local-operation boundary. The observation is unchanged; which accepted requirement, if any, governs the supplier's own start-up traffic stays the owner's question (U-18) | §2, §8.1 L-4, F-14, U-18 |
| R9-7; S1-D HOSTING item 3 | The evidence route to DEL-04-03 is direct: §6.4, S-7 and §8.2 no longer say "through DEL-01-02". DEL-01-01's own ScopeOfWork was checked first and states no route. DEL-01-02's custody of in-flight requests is named as a separate contribution of a deliverable outside this increment | §6.4, §8 S-7, §8.2, F-26 |
| R9-6; S1-D HOSTING item 3 | Receivers line rebuilt from the live registers, with row IDs, arc labels and DAG-003 layer. S-7 names DEL-04-03 and DEL-09-06. A table of the receivers the registers name follows the seams table. For DEP-02-01-025 the 0.158.0 inventory is held, and a capability meaning beyond it is marked "not yet defined here" (F-27). F-07 and F-16 are updated | Header, §8, F-07, F-16, F-27 |
| Not applied | S1-D HOSTING items 4, 5, 6 and 7 are Wave B and were not started | — |
| **K1-1** (node A3, in place; owner DECISION-K1 of 2026-09-30, `APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md` sha256 35d6546346907137581be7df3bed4a8ccdb4b8bc55a261ca716040d0ad9f91bc) | §6.7: who requests is **SETTLED by DECISION-K1 K1-1** (was INTEGRATION) | §6.7 |
| **R11-3** (node A4, in place; V17-B M-1) | Header: a new line pins this run's records at their final bytes: R9 `a64e2415…`, R10 `ad3b6caa…`, R11 `e7343b66…`, OWNER_DECISIONS `7458e9e8…`. The node A1 input line and the K1 rows keep the bytes read then | Header |

## Changes from v0.5

Keyed by R8 ID. Sources are I2 rows of INTAKE_MAP.md. R8 overrides I2 where
they differ. SETTLED here means by DECISION-3 or DECISION-4.

| R8 ID (source) | Change in v0.6 | Where |
|---|---|---|
| **R8-1** (DECISION-4 D4-1; SETTLED, framing INTEGRATION) | §6.7 gains a **Phase-1 statement**: checkpoints are plan guidance; no App run is holding; no `run-holding` refusal, HP-3 decline or `turn/interrupt` is used for a checkpoint; no hold claim; the boundary delivers the native items from which DEL-02-03 records arrivals, acts and the optional "continued past ‹checkpoint› before ‹act›" annotation. The existing HP-1…HP-4 and HP-H facts are **recast as governance phase (retained)**, not deleted. VC-25 is two-part | Header, §6.7, VC-25 |
| **R8-2** (02.17; Part 4.11; STD-4 as overridden by R8-2) | §6.7 lead records SQ-02 answered 2026-09-28 with no host-held route (route (iv)), and D6 **closed for Phase 1** by DECISION-4, re-opening with the governance phase. HP-H: "(pending SQ-02)" → "not offered by SWBPIPE (SQ-02 route (iv))". U-23 restated (owner and effect) | §6.7, U-23 |
| **R8-9** (DECISION-4 D4-3; SETTLED) | Model access: a cloud model is reached by **OAuth sign-in or an API key**; **no default** between local and cloud. HOSTING had no "local by default" text (checked). L-5 records the choice and the supplier's sign-in and API-key variants; S-4 and §11 name OAuth sign-in with the API key; F-24 added. **V4-HOST-02 is not cited in this file**, so no pending mark is needed here (it is marked in LOOP-v0.6) | Header, §8 S-4, §8.1 L-5, §11, F-24 |
| **R8-8** (DECISION-4 D4-2) | L-6: the host-loop interface stays V4-ARC-10 (D-20), qualified separately | §8.1 L-6 |
| **R8-7** | Consumed inputs updated. No OI-003 citation exists in this file (checked) | Header |
| R8-3…R8-6, R8-10, R8-11 | Not addressed to HOSTING text. I2 01.14 (R9: elicitation never capture) and 16.2 (§8.3) confirm current text; 19.5 (§8.2) and 29.3 (§9) have no effect. §6.8's rule that supplier status `disabled` is never A13 evidence agrees with R8-6. No change | — |
| **R8-12** (item 7; closing pass, node A6, in place) | Consumed inputs list the post-R8 sibling versions. Item 1's lapse label and items 3–6 are not addressed to HOSTING text (checked). No change to the boundary | Header |
| **R8-13** (DECISION-5; SETTLED; in place, no version bump) | §2 gains the **DECISION-5 scope note**: DECISION-5 governs host agents only; the App's own Codex keeps the person's Codex configuration, approval and sandbox choices, and this boundary adds no allow list, destination prompt or destination gate to it. U-18 (the supplier's own start-up fetch) is not settled by DECISION-5. F-25 records that this file now cites V4-HOST-02, only to scope it out; F-24's "cites neither" held before R8-13. No boundary rule changes | Header, §2, F-25 |
| R8-13 close — in place | The owner confirmed DECISION-5 (the reading of "MCP V2"; the person-only grant stands), so the "open to the owner's correction" markers are closed. The consumed-input line is corrected: OWNER_DECISIONS.md is cited in its state that adds that confirmation, not at `1528a5033` |

## Changes from v0.4

| R5 ID / source finding | Change in v0.5 |
|---|---|
| R5-9 (V3-B m-5; Y-7) | §6.7 and §10 stop citing EXEC U-E20 (withdrawn in EXEC-v0.2); the v0.3 change row notes the withdrawal. §6.7 adds **HP-4** (the App initiates nothing for a holding run: no App-initiated turn start and no App-initiated `mcpServer/tool/call` / `mcpServer/resource/read`, refused `run-holding`) and names HP-H as the host's; §6.8's App-initiated call row cites HP-4; VC-25 extended; U-23 updated; new U-25 and F-22 on the person's own messages |
| R5-9 (current sibling versions) | Consumed inputs cite EXEC-v0.2, ADAPTER-v0.2 and RS-v0.4 at 8fb51f07f; the v0.1 sibling citations are marked superseded. EXEC and ADAPTER v0.3 are in the same pass (not consumed) |
| R5-1 | §6.7: any hold-support statement uses only R5-1's four values; this boundary changes no value; App-only checkpoints stay *not enforceable*; no retired EXEC-v0.1 value is used |
| R5-4 (V3-B m-1; V3-A m-11) | §8.3 keeps per-turn destination facts, requested and effective separate, re-routes on their turn, unobserved turns *unknown*; run-level set and "switch starts no new run" left to DEL-04-03. Attribution split: "flow to the selected model, no gate" SETTLED by DECISION-2; "record and show" INTEGRATION (DECISION-2 reading). Per-turn `model` on turn start noted; F-23; VC-26 updated |
| R6-4 (in place, no version bump) | EXEC-v0.3 §2 HP-4 scope settles person-directed turns; §6.7 HP-4 bullet cites EXEC-v0.3 (commit d3cebd1cc, sha256 889e48819baa21ec112c4878e4e38004dcbaa9eb3645a31c24221ac116ee548e); U-25 and F-22 closed; R6_RESOLUTIONS.md sha256 8703e85aa7324e233fab285321e277d720923d3e36e342c865917b55083cb841 (working copy) |
| V3-A | No item addressed to HOSTING |
| V3-B other minors | None other than m-5 (and the m-1 note, which confirmed §8.3) addressed to HOSTING |

## Changes from v0.3

| R4 ID / source finding | Change in v0.4 |
|---|---|
| R4-12 (W7 EXEC F-9; W8 ADAPTER F-3) | R9 and §6.1: answers to Codex user-input and MCP elicitation requests are **not act evidence and never host act capture** (EXEC CAP-6); the "standing open" wording is removed. New **§6.8** classifies the MCP status, configuration, OAuth, agent-call, App-initiated `mcpServer/tool/call` / `mcpServer/resource/read`, elicitation, event-stream and dynamic-tool surfaces from the committed 0.158.0 bundle; the App-initiated call is App-origin and never used to act as the agent or for any person's act. §5 client-request records gain an **initiator** element. VC-23, VC-24; U-24; F-19 |
| R4-13 (W8 F-4) | §6.8: supplier status `disabled` and any App-side configuration (agent-writable) are never A13 evidence |
| R4-2 (D6 deferred, DECISION-2) | New **§6.7**: App run holds `UNRESOLVED{D6}` (U-23); `turn/interrupt` (HP-2) recorded as `observed-in-generated-types` only and **not relied upon**; HP-3 named-rule decline stays a permitted best effort under D3; HP-1 not adopted; the boundary makes no hold claim. §10 still-to-observe extended (then citing EXEC-v0.1 U-E20, since withdrawn in EXEC-v0.2; that citation is removed in v0.5). VC-25 |
| R4-1 (D5, DECISION-2) | New **§8.3** observed model destination (requested, supplier-reported effective, re-route) supplied per thread/turn to DEL-04-03 and DEL-03-03 without gating; class from DEL-01-05's configuration. S-4, S-7 updated; VC-26; F-20, F-21; U-18 note |
| R4-19 (V2 m-13) | Consumed inputs now list R3 (no HOSTING item) and R4, DECISION-2, EXEC-v0.1 and ADAPTER-v0.1 with hashes at f05c7e4cd |
| Other | None of R4-3…R4-11, R4-14…R4-18, R4-20, R4-21 is addressed to HOSTING; no change |

## Changes from v0.2

| Source item | Change in v0.3 |
|---|---|
| R2-22 / IR1C-18 | §6.1 table, new rule **R9** (answer origin by kind: A14 → R7; person-input kinds answered with content only by the person, App rules may only decline/error; named service kinds such as `currentTime/read` answerable by a named App rule), §6.4 answer row, VC-14 and new VC-22 made consistent; "standing as act evidence" for user-input/elicitation stays open (WD U-25, W7); U-20 extended |
| R2-22 / IR1C-19 | Header cites the current committed PIN_SPIKE revision (0e090a4c…b115) and records that v0.2 consumed the pre-correction revision (3d66ad28…f3cf) and IR1-C reviewed 26ea0c2f…0334 |
| R2-22 / IR1C-19 | F-17 retired (the spike's stale row was corrected by the parent) |
| R2-22 / IR1C-20 | §10 rebuilt on the spike's two vocabularies (standing; verdict consistent / refines / contradicts); P-01 is **refines**, as the spike says; no verdict reclassified |
| R2-22 / IR1C-04 | VC-07 and §7.3 cite `generated/0.158.0/COMMITTED_STATE.md` (sha256 2cb7f1d2…2608): committed tree 2 OK / 2,357 not committed / 0 mismatched; 1,605 TS files OK from the scratch copy; the W11 SV-02 figure is labeled as describing the never-committed proposed form; manifest `# COMMITTED` comment noted as superseded |
| R2-11 | D3 attribution narrowed: §2 row, H9, R7 and §11 separate what D3 says (modes are the user's own Codex setting; tool execution only; never stand in for a reserved or professional act) from the R-2 restrictions (grant governs host operations only; no App-rule affirmative A14), marked DERIVED/INTEGRATION |
| R2-8 | R8, S-7 and §11: A14 settlements reach evidence only as run-record tool-permission entries (DEL-04-03 R13), never a human-act record or a grant; App runs only |
| IR1C-21 | Addressed to PIN_SPIKE, not this file; the parent's git-operations correction is reflected only through the cited revision |
| Other | "R1–R8" references updated to R1–R9 (§6.5, §12) |

## Changes from v0.1

| Source item | Change in v0.2 |
|---|---|
| D4 (owner) / R-10 / V1-C §6 row 9 | Pin 0.158.0 stated in header, §7.1, §10, U-01 as definition/generation pin, not qualification; "version-independent" dropped from title |
| D3 (owner) / R-2 D3 bullet / R-10 / V1-A D-13 / V1-C §6 row 8 | §2 row, H9, R7, U-04, F-09 rewritten: tool-permission and sandbox modes (including supplier classifier/reviewer modes) are the user's own Codex setting, carried unchanged; the DEL-04-01/04-02 autonomy grant governs host operations only; no App rule answers A14 affirmatively; App decline/error only under a named rule with truthful origin; U-04 closed |
| V1-A D-14 / R-10 | R7, §6.1 origin set and new §6.6: affirmative A14 answers come only from the person (via DEL-01-04) or from the user's own Codex mode inside the supplier; new origin value `supplier-internal` |
| V1-A RF-03 | Resolved by the D-13 repair (constraint now D3 via DEL-01-05/01-04; existing rows suffice); no register edit here (register findings go to C1) |
| R-1 / R-4 | A-names used throughout; "approval request" → "tool-permission request (A14)"; §11 rows use A-names; R8 restated |
| D2 (owner) / V1-C §6 row 8 | R7's OI-001 clause becomes D2: no automatic answer stands for a reserved act; A14 answers are not reserved acts |
| V1-C D-16 / R-10 | New §8.2: per-thread/per-turn content identity of each guidance input actually carried; S-6/S-7 updated; P-15 is a named limitation (supplied ≠ provider-adopted) |
| V1-C D-22 / R-10 | L-2 (Responses interface) stays **not-observed**: the spike did not observe it (§8.1) |
| V1-C AB-10 | §10 notes the 0.158.0 method/request inventory as the input to harness-capability naming; no naming chosen here (DEL-02-01 owns) |
| V1-C RF-6 | DEL-02-04 added to Receivers; missing register row routed to C1 (F-16) |
| AG-13…AG-15 (V1-C agreements) | Retained unchanged (R8, L-6, S-6) |
| S-F-01 | §7.1/§7.2: handshake identity = user agent, home, platform family, platform OS; no version element; user-agent version parse is a consistency check only |
| S-F-02 | §7.1, H1, S-5: distribution identity over the executed vendor tree; launcher record (wrapper vs vendor, added environment) |
| S-F-03 | §7.3 reference-output options O-R1…O-R3 for the App implementation owner (U-15); generated-schema identity names generator kind and variant; §6.1, §9.3 cite the chosen reference |
| S-F-04 | §7.3: supplement narrows; experimental status only by variant diff; no initial entries at 0.158.0 |
| S-F-05 | §6.1: familiar set = reference output × capabilities declared at handshake |
| S-F-06 | New H11; §4.3–§4.5: stop and restart cover the supplier's descendant processes; overlap with a running sync (U-16) |
| S-F-07 | §4.3/§4.5: exit status never classifies an end; "deliberate" comes only from the App's stop record |
| S-F-08 | §5, H6: parser does not require the JSON-RPC version member on inbound frames; top-level supplier elements such as `emittedAtMs` are native content |
| S-F-09 | H4, §4.1, §4.2: generation assigned at spawn; frames received while handshaking are kept in order and delivered at `ready`, never dropped |
| S-F-10 | §8.1 L-4 now **observed** (fresh-home plugin fetch); routed to the owner and DEL-01-05 (F-14, U-18) |
| S-F-11 | §6.6 supplier-internal decisions (`approvalsReviewer`), origin `supplier-internal`; `timed_out` native form noted under U-11 |
| S-F-12 | §6.2: `serverRequest/resolved` named as the candidate source of `resolved-by-supplier`; semantics not-observed (U-09) |
| S-F-13 | S-2: plan updates carry the whole plan with no revision identity; DEL-01-03 derives revision identity |
| S-F-14 | H7/U-07: the concrete opt-out facility exists (`optOutNotificationMethods`) and is not used |
| S-F-15 | §9.1: redaction adds host name, installation identifier, absolute home path |
| S-F-16 | R2 and §5: supplier's own unknown-client-method reply is -32600 with id echoed; the App's code for unfamiliar server requests stays an implementation choice |
| S-F-17 | §7.2: the version-label probe writes into the home it runs against (U-03, OI-009) |
| S-F-18 | F-12: the supplier labels `app-server` and both generators `[experimental]`; routed to owner visibility and pin re-examination (U-21) |
| Parent re-selection (SPIKE §4) | §7.3: generated TS is not committed (regenerated deterministically against the manifest); JSON Schema experimental bundles + manifest + `_spike/` are committed |
| Verification | VC-01…VC-15 carry a "runnable now?" note; VC-16…VC-21 added; none claims qualification |

## 1. What this boundary is

The App's main process owns one stock, unmodified Codex App Server child
process **per App-owned Codex home** (with the descendant processes the
supplier itself starts) and speaks its published JSON-RPC protocol over each
child's standard input and output (V4-ARC-01, SOW-118). From v0.9 there may
be more than one such home (DECISION-L L-1: a second App-owned home for
API-key conversations; ACCESS-v0.2 §3, §4 K2-1); every rule below holds per
home, and nothing of one home's child settles, answers or is attributed to
another's (H5; U-12). The boundary is the single place where:

1. the supplier distribution is identified and verified before it is trusted
   as the pinned supplier (SOW-099, SOW-128, SOW-135);
2. the child is started, handshaken, observed, restarted and deliberately
   stopped (§4);
3. protocol frames are exchanged, correlated and delivered in native form to
   receivers (§5; V4-ARC-05, V4-APP-04, M-2);
4. every server-initiated request is registered and answered, explicitly
   declined or explicitly errored (§6; V4-EXE-02, ARC §3 properties);
5. generated protocol output and the small experimental supplement are bound
   to the pin they came from (§7; SOW-121).

It is **not** the place where durable recovery, request cards, plan views,
account flows, packaging, workflow semantics, guidance composition, operation
policy or human acts are produced (§11; REQ-007, REQ-008).

```text
  Interface (webview; React+Vite)            ── observes; composes; presents
        │  receiver interfaces (semantic; transport inside Tauri unselected)
  Main process (Rust; Tauri 2)                ── owns the boundary below
   ┌──────────────────────────────────────────────────────────────────────┐
   │ Distribution identity & verification (§7) → Child lifecycle (§4)     │
   │ Frame exchange & correlation (§5)      → Native delivery to receivers │
   │ Server-request register interface (§6) ← A14 answers via DEL-01-04    │
   │ Recording tap for fixtures and guidance evidence (§8.2, §9)          │
   └──────────────────────────────────┬───────────────────────────────────┘
                                      │ published JSON-RPC over stdio
                     stock Codex App Server 0.158.0 (definition pin), unmodified
                                      │ supplier-started descendants (e.g. git)
```

The Rust/TypeScript division drawn above is the fixed invariant only (ARC §3
properties). Everything further is the OI-008 proposal in §12.

## 2. Governance context and its v4 standing

Root D-GOV-43 (v3 App, ruled 2026-09-11) and Root `AGENTS.md` state a stance
for the App: stock App Server owned by the App's host process, full published
protocol, every server request answered, no filtering of Codex notifications,
no veto of the user's Codex configuration, no pinning of approval or sandbox
policy, no patched supplier; the A2 supplement adds "unfamiliar notifications
inspectable, unfamiliar server requests answered explicitly without implying
approval". Checked against the v4 basis and the owner's rulings:

| D-GOV-43 element | v4 basis | Standing in this definition |
|---|---|---|
| Stock, unmodified, published interface | V4-CST-03, V4-ARC-01, M-2, M-4, SOW-099 | Settled; invariant H1 |
| Host-process ownership of child/session/requests | ARC §3 properties, V4-EXE-01 | Settled; H2, H3, H11 |
| Every server request answered; unknown → explicit error | ARC §3 properties, V4-EXE-02, SOW-123 (DEL-01-02) | Settled; register rules R1–R3 |
| Native items, no translated vocabulary | V4-ARC-05, V4-APP-04, PRD §6, ARC §7 | Settled; H6 |
| No notification filtering; unfamiliar notifications inspectable | Consistent with M-2; not stated as a v4 prohibition | **Definition choice** (H7); the supplier facility exists at 0.158.0 and is not used; open to the App implementation owner (U-07) |
| Approval/sandbox policy is the user's choice per project/turn | **Owner decision D3** (OI-002), first increment | **Settled by ruling.** In the App, routine tool-permission and sandbox modes, including any classifier-based mode, are the user's own Codex setting per project/turn, carried unchanged. They govern tool execution only and never stand in for a reserved or professional act. DERIVED/INTEGRATION, not D3 text (R2-11): the DEL-04-01/04-02 autonomy grant governs host operations only, and no App rule answers A14 affirmatively (R-2 D3 bullet) |
| Additive instruction inputs preserving Codex base instructions | Deliverable interface "PKG-02 supplies guidance/workflow inputs"; production is DEL-02-04 (role guidance) and, from v0.9, DEL-02-02 (a workflow's run-start text, WR-v0.2 §16; R19-7) | Carried unchanged through supported inputs, with per-thread/turn content identity evidence (§8.2); `baseInstructions` is never set (R17-8) |

**DECISION-5 scope note (R8-13; in the accepted basis since SCA-V4-001).**
V4-HOST-02, as amended for DECISION-5, governs a
**host's embedded agent**: an allow list, in-work destination grants, MCP
only if stateless, an always-off list, and every destination recorded and
shown (LOOP-v0.7 §5.1.1). It governs host agents only. The amended ARCH §4
host-agent property states the scope itself: "This property governs a
host's embedded agent; the App's own Codex keeps the person's Codex
configuration, approval and sandbox choices."

- The App's own Codex keeps the person's Codex configuration, approval and
  sandbox choices (ARCH §4 as amended; Root `AGENTS.md`; D-GOV-43; D3). DECISION-5 does not veto
  them, and this boundary adds no allow list, destination prompt or
  destination gate to the App's Codex.
- The App's per-turn model destination stays as recorded in §8.3 (D5; the
  record-and-show reading of R5-4 is owner-confirmed, §8.3).
- The supplier's own start-up fetch (U-18) is not settled by DECISION-5,
  which concerns host agents, nor by the amended ARCH §1 priority 3, which
  now speaks of a host's agent (§8.1 L-4).

## 3. Invariants (hold in every state and every candidate)

- **H1 Stock supplier.** The child is the identified, unmodified stock
  distribution. The App never patches, replaces or injects code into the
  supplier binary or the sibling executables it runs. The launcher (the npm
  wrapper or the vendor binary directly), the arguments and the environment
  the App supplies — including environment the wrapper itself adds (at 0.158.0
  `CODEX_MANAGED_PACKAGE_ROOT`, `CODEX_MANAGED_BY_NPM`; SPIKE §3) — are
  recorded as the configuration identity (§7.1), so "unmodified" is
  inspectable (VER-001; S-F-02).
- **H2 Single owner of the pipe.** Only the main process writes to the child's
  input and reads its output. Interface processes never hold the pipe; losing
  or reloading a window never writes to, closes or signals the child
  (V4-EXE-01).
- **H3 Custody location.** The protocol session and the outstanding
  server-request register live in the main process for the child's lifetime
  (ARC §3). Durable custody across relaunch is DEL-01-02's (§6.5;
  RECOVERY-v0.2 §3.5, §5, §7).
- **H4 Verified before ready.** No receiver is told the supplier is ready
  until verification (§7.2) and the handshake (§4.2) have both succeeded,
  or the explicit CC-H development route LT-24 and handshake have succeeded
  with `supplierStanding: unverified-development` shown to every receiver.
  Frames the supplier sends before `ready` (at 0.158.0 a notification arrives
  together with the initialize response, before the client's `initialized`
  notice; SPIKE §5) are kept in received order under the new generation and
  delivered with the `ready` announcement; they are never dropped (S-F-09).
- **H5 Generation tagging.** Each spawn receives a new *generation* at spawn
  time. Every outbound request, inbound response, notification, server
  request and register entry carries its generation. Nothing from one
  generation settles, answers or is attributed to another. **Generation
  identity (v0.9; R18-1 C-20 with R19-4 L-1):** {App session, App-owned
  home, spawn counter}, so a generation is unique across App sessions
  (RECOVERY-v0.2 §6, F-R6: the ledger outlives the process) and across the
  App's homes (each home has its own child, U-12). PROPOSED form; the
  semantic element stays one identity. CC-H candidate representation is
  `{appSession, home, spawnCounter}` in every boundary record and envelope;
  `home` is a stable App-owned identity, never a credential or filesystem path.
  The counter alone is valid only inside a cache scoped to one session/home;
  exported records never rely on an implicit container for the other elements.
- **H6 Native delivery.** Well-formed notifications, responses and server
  requests reach receivers with the supplier's own method, identifiers,
  payload **and any other top-level supplier elements** (at 0.158.0 the
  notification timestamp `emittedAtMs`; SPIKE §5) unchanged, in received
  order. Boundary metadata (generation, receipt position, classification)
  travels beside the native frame, never merged into or replacing it (S-F-08).
- **H7 No silent loss.** The boundary does not use the supplier's
  notification-suppression facility (at 0.158.0 the handshake capability
  `optOutNotificationMethods`; S-F-14) — definition choice, U-07. Unfamiliar
  notifications are delivered, marked unfamiliar and inspectable. Malformed
  or oversize frames are counted **and** surfaced with generation and
  position; they are never silently discarded (F-05).
- **H8 Silence never grants.** No timeout, silence, observer loss, reconnect,
  restart or process exit is ever turned into a grant or an affirmative answer
  (V4-EXE-02).
- **H9 Carries, does not decide (D3).** Tool-permission, sandbox and
  supplier review-routing settings (at 0.158.0 including `approvalsReviewer`
  = `user` | `auto_review` | `guardian_subagent`; S-F-11) are the user's own
  Codex setting per project/turn (owner decision D3). The boundary carries
  exactly what the person set through the owning interface (DEL-01-05 for
  settings; DEL-01-04 for answers) and defines none of it. The DEL-04-01/04-02
  autonomy grant governs host operations only and is not consulted for A14
  (R-2; DERIVED from D3, attribution per R2-11).
  The account-home element is **decided** (v0.9; DECISION-K3 K-1, option C;
  ACCOUNT-HOME-RECORD-v0.2 §3): each App-owned home shares the person's
  configuration through a link to their `config.toml` and keeps its own
  sign-in. Carriers per element: the person's settings, including approval
  and sandbox, and their plugin setting (L-3), reach the App's Codex through
  the link unchanged; the App's K-12 traffic settings travel in the App
  child's session flags (analytics off; `plugins = false` only in the
  fallback when the person's setting is off; §4.2 step 3; ACCESS-v0.2 §9); a
  setting the supplier refuses is shown as refused, never "fixed" by the
  App (F-32).
- **H10 Unknown stays unknown.** When a request to the supplier was written
  but its response was never observed (exit, wait limit, write failure), its
  outcome is *unknown*, not failed and not succeeded (V4-EXE-03; ARC §3).
- **H11 The supplier is a process tree.** The supplier starts its own
  descendant processes (at 0.158.0, networked `git` fetches of a plugin
  repository on a fresh home; they were observed alive and reparented 500 ms
  after the supplier exited; SPIKE §5). Stop, restart and exit handling treat
  the supplier and its descendants as one unit; surviving descendants are
  detected and recorded, never assumed gone (S-F-06). The mechanism (process
  group or equivalent) is unselected. At OBS-2 (0.158.0; §10.2 OB2-11) a
  plugin `git ls-remote` child was still running when the supplier exited
  about 0.7 s after spawn and was re-parented; so a deliberate stop ends the
  whole process group (§4.5 step 3; U-16 as RECOVERY-v0.2 §6 proposes).

## 4. Child lifecycle

### 4.1 States (semantic)

The states, tables and operations of §4 hold **per App-owned home** (v0.9;
L-1; U-12): each home's child has its own state and generations, and a stop
or restart names the home it applies to.

| State | Meaning | Receivers may |
|---|---|---|
| `absent` | No child for this App run | Request start (person/App startup) |
| `verifying` | Distribution identity being checked (§7.2) | Observe |
| `refused` | Verification failed or was unverifiable; child not started as the pinned supplier | Read the reason; not send requests |
| `spawning` | Process tree being created with recorded launcher/arguments/environment; generation *g* assigned | Observe |
| `handshaking` | Initialize exchange in progress; early frames of *g* are held in order (H4) | Observe |
| `ready` | Verified and handshaken; generation *g* active; held frames delivered | Send requests; answer server requests |
| `exited-unexpectedly` | Child ended with no App stop record for *g*; generation closed | Read exit facts; see §4.3 |
| `restart-waiting` | Waiting before the next start attempt (and for §4.4 descendant rule) | Observe; request deliberate stop |
| `halted-after-repeated-failure` | Restart bound reached; no further automatic start | Read failure history; request an explicit restart |
| `stopping` | Deliberate stop requested by a person (quit/stop); stop record written | Observe |
| `stopped` | Deliberately stopped; generation closed; descendant outcome recorded | Request start |

### 4.2 Operating sequence: start

1. **Resolve** the supplier distribution the App candidate declares as its
   pinned supplier, and the launcher (U-17; location is a packaging concern,
   DEL-01-06).
2. **Verify** it (§7.2). Mismatch or unverifiable → `refused` with a reason;
   no child is started as the pinned supplier.
3. **Spawn** with the recorded launcher/argument/environment set; assign
   generation *g*. **Account home (v0.9; DECISION-K3 K-1, option C;
   ACCOUNT-HOME-RECORD-v0.2 §3, §4; ACCESS-v0.2 §3):** the child is spawned
   with `CODEX_HOME=<App-owned home>`, one child per home (H-acct; H-key
   only when the person has added an API key, DECISION-L L-1). The home's
   `config.toml` is a symbolic link to the person's configuration file, so
   the person's settings are shared and each home keeps its own sign-in.
   *Observed at OBS-2 (0.158.0; O-6 M1; §10.2 OB2-8):* the linked file is
   read as the home's user layer (named by the App home's path, content the
   person's); `account/read` reports the App home's own account (none in the
   observation); the person's file was not written. `-c` overrides also
   work and form a `sessionFlags` layer (a copy; O-6 M2); `--profile` is
   refused for `app-server` (M3). The fallback (each App home keeps its own
   configuration, option A) is not needed at 0.158.0. Separate
   authentication storage per home rests on the default credential store
   (`file`) and is an inference: no credential was observed (M4, M5;
   DECISION-L L-6). By R18-6 (PROPOSED in ACCESS-v0.2 §3 and ROLE-v0.2) the
   person's global `AGENTS.md` and `skills/` are linked the same way, so
   Codex's native discovery in the App matches the person's Codex; the App
   writes nothing into a linked skills root and places no workflow in any
   discovered skill root (R19-7). The App's own session flags carry the
   K-12 traffic settings ACCESS-v0.2 §9 names (analytics off; and
   `plugins = false` only in the fallback with its own configuration when
   the person's plugin setting is off) and, if ROLE U-R3 selects `-c`
   session flags as the child-role carrier, the additive
   `agents.<ROLE>.*` entries of §8.2; never a credential (CR-7, CR-8); the
   child's environment carries no credential variable (CR-7). Plugins follow
   the person's own setting (DECISION-L L-3): under the link Codex reads the
   person's own `[features] plugins`, so the App adds nothing; when it is off
   the start-up plugin connections stop, and when it is on (the 0.158.0
   default, OBS-2 O-7 v0) they happen and are shown and recorded (§8.1 L-4).
   The setting is read at run time (`config/read` layers). The internal
   environment variable that stops the remote-control loop is not used and
   is not passed to the child (R18-3; ACCESS-v0.2 §9). On a fresh home with
   plugins on, the supplier performs a network fetch at start (§8.1 L-4,
   U-18).
4. **Handshake**: send the supplier's initialize request carrying the App's
   client identity and the capabilities the App declares (at 0.158.0:
   `experimentalApi` and `requestAttestation`, both required booleans;
   optional elements include `optOutNotificationMethods`, which stays absent
   or empty per H7; SPIKE §5). **Declared values (v0.9):** under K-5 the
   App declares `experimentalApi: true`, recorded per generation, and
   DEL-01-03 reads the declared value per generation (NPTD-v0.2 §4 EX-2).
   At OBS-2 (0.158.0; §10.2) plan mode (`collaborationMode` on `turn/start`)
   and `remoteControl/status/read` needed the opt-in; delegation did not
   (stable feature `multi_agent`). The App also declares
   `explicitGatewayOauth: true` (PROPOSED by ACCESS-v0.2 §6 Q-1; in the
   0.158.0 types it replaces "automatic browser authorization" for the
   gateway runtime), so no gateway browser authorization starts without the
   person's act. `requestAttestation` stays false. Record the declared
   capabilities: they determine request classification (§6.1, S-F-05).
   Record the handshake
   response (at 0.158.0: `userAgent`, `codexHome`, `platformFamily`,
   `platformOs`) in the version identity record (§7.1). Send the
   `initialized` notice (whether it is *required* is not-observed, U-19).
   Frames received meanwhile are held (H4). Handshake refused or no response
   within the wait limit → the process tree is stopped (§4.5 mechanics),
   *g* is closed without becoming `ready`, and the failure counts toward the
   restart bound. A second initialize is never sent on the same generation
   (the supplier answers "Already initialized"; SPIKE §5).
5. **Ready**: announce `ready(g)` with the version identity record and the
   declared capabilities, then deliver held frames in order.

### 4.3 Operating sequence: unexpected exit

"Unexpected" means: the child's end was observed and there is **no App stop
record** for *g*. Exit status is never used to classify the end: at 0.158.0
closing input and a termination signal both give exit code 0 with no signal
(SPIKE §5; S-F-07).

1. Close generation *g*; record exit facts (exit status/signal as observed,
   last receipt position, malformed-frame count, bounded redacted diagnostic
   output) and the surviving-descendant check (H11).
2. Every **client→supplier request** of *g* with no observed response gets
   outcome `unknown-no-response` (H10).
3. Every **outstanding register entry** of *g* moves to
   `ended-unanswered(process-exit)` (§6.2). It is never answered afterwards
   and never recorded as answered by a person.
4. Announce `exited-unexpectedly(g)` to receivers, including DEL-02-03 (EXEC
   AE-6: observation lost and recovered), DEL-03-03 (ADAPTER CT-10, S-8:
   endpoint facts and in-flight submissions) and DEL-01-02, which
   owns recovery of actual thread/request state from the supplier after the
   next `ready` (V4-EXE-01, DEL-01-02 REQ-005; at 0.158.0 the supplier offers
   thread resume/read/list methods, P-13; post-restart results are now
   observed at one pairing, OBS-2 O-2, §4.4 "Recovery reads").
5. Enter `restart-waiting` unless the restart bound is reached, in which case
   enter `halted-after-repeated-failure`.

### 4.4 Restart rules

- Restart is automatic but **bounded**: a growing delay between attempts and
  a maximum number of failures within a window, then halt until an explicit
  person-initiated restart. Numbers are implementation choices (U-05); v3's
  1–30 s / 5 in 180 s are historical only.
- Every restart re-runs verification (§7.2); a changed distribution is
  detected, not assumed.
- **Descendant overlap.** Before starting generation *g+1* on the same home,
  the boundary checks for surviving descendants of *g* (H11). Whether it waits
  for them, ends them, or starts alongside them (the supplier uses its own
  lock on the plugin sync, `.tmp/plugins.sync.lock`, SPIKE S-F-06) is U-16;
  the choice and the observed descendant state are recorded. v0.9:
  RECOVERY-v0.2 §6 proposes that after an unexpected exit survivors are
  recorded and shown to the person with a person's action to end them, the
  App does not end them by rule, and *g+1* starts alongside after an overlap
  wait (TEST VALUE); at a deliberate stop the whole tree is ended (§4.5).
- Restart never re-sends a prompt, re-answers an old request or replays a
  client request of a closed generation (V4-EXE-01).
- **Recovery reads (v0.9; OBS-2 O-2, 0.158.0; §10.2 OB2-3).** In a new
  process `thread/read` works before `thread/resume` (the thread reads back
  `notLoaded`); a turn live at the stop reads back `interrupted` after a
  graceful stop and after a kill alike, so the supplier's status does not
  tell a quit from a crash (the App's stop record does, S-F-07). A request
  pending at the stop is **not** raised again on resume and no resolution is
  sent for it. `thread/read {includeTurns: true}` and `thread/resume`
  without `excludeTurns` each produced a `deprecationNotice` (full-history
  hydration deprecated in favour of `thread/turns/list` and
  `thread/items/list`), so recovery reads prefer those (RECOVERY-v0.2 §5
  R-4; NPTD-v0.2 §12). The reads are App-initiated, initiator
  `app-rule:recovery-read`; resume is `person-directed` (RECOVERY-v0.2 §6).

### 4.5 Deliberate stop

A deliberate stop is **DEF-5a, stopping the Codex process** (v0.9; R17-3;
the definitions are DEL-01-02's, RECOVERY-v0.2 §2). It is reached only by a
confirmed App quit (DEF-6: with live work the App asks first, K-4) or by the
person's explicit "Stop Codex" or "Restart Codex" (offered by DEL-01-04,
each asking first with live work; R18-1 C-12; NIR-v0.2 §5.2). With several
App-owned homes, a quit stops each home's child; "Stop Codex" and "Restart
Codex" name the home they apply to (L-1). Interrupting a turn is DEF-3
(`turn/interrupt`), which never stops the process; ending a workflow run is
DEF-4 (DEL-02-03), which this boundary neither performs nor records.
Closing, hiding or reloading a window is DEF-1, not a stop (V4-EXE-01,
V4-EXM-11). An unexpected end is DEF-5b (§4.3). Sequence:

1. Write the **App stop record** for *g* (actor, time, reason) — the only
   evidence that the end was deliberate (S-F-07).
2. Announce `stopping`. Outstanding register entries are **left to end with
   the process** (`ended-unanswered(process-exit)`, RT-11); there is no App
   decline at stop or quit (v0.9; RECOVERY-v0.2 §6 U-10; R17-9). At a quit
   the question has listed them first (K-4), and interrupting each live turn
   first (DEF-3, cause *quit*) lets the supplier resolve them itself, which
   is recorded as `resolved-by-supplier` (RT-10; observed at OBS-2 O-3,
   0.158.0). At OBS-2 (O-2) a pending request was not raised again after a
   restart and resume and no resolution was sent for it, so the
   `ended-unanswered` end is final.
3. End the supplier politely (closing its input or a termination signal; at
   0.158.0 both end the supplier within milliseconds, SPIKE §5; OBS-2 O-2:
   closing input with a live turn and a pending request, exit 0 in about
   21 ms), then forcefully after a grace period (value unselected), **for
   the whole process tree** (H11): the process group is ended, since a
   plugin `git` child started near spawn can outlive the supplier (OBS-2
   §11; U-16 as RECOVERY-v0.2 §6 proposes). *Observed at OBS-2 (0.158.0,
   O-2):* on a stop by closing input with a live turn, Codex writes into the
   thread's history a user-role marker saying the user interrupted the
   previous turn on purpose (with an aborted tool output), so after a quit
   the model's next turn reads the quit as the person's interrupt; a kill
   writes nothing; both read back `interrupted`. The App's own record says
   "interrupted by quit" or, for Stop/Restart Codex, cause `codex-stop`, and
   recovery shows the note from the App's own record; the App never parses
   or edits Codex's history (RECOVERY-v0.2 §3.4, §5 SQ-Q; R18-7 G-5; shown
   to the owner in DECISIONS_PENDING_2's visibility list). Whether
   `turn/interrupt` writes such a note is not observed.
4. Record surviving descendants, if any, and their handling; enter `stopped`.
   No unattended execution after quit is promised.

### 4.6 Lifecycle operations offered to receivers (PROPOSED, v0.8; R12-1)

Semantic operations; the receiver-facing transport stays unselected (§1).
Each lifecycle event is one record of `hosting.lifecycle-event.schema.json`
(PROPOSED; §9.6), naming its row of the §4.7 table.

| Operation | Caller | Accepted in | Result | Failure behaviour |
|---|---|---|---|---|
| start | The person, or App start-up (actor `app-startup`) | `absent`, `stopped`; `refused` only on the person's explicit start | Events LT-01…LT-09; `ready(g)` with the version identity record and the declared capabilities, or `refused` with the verification result | Verification mismatch or unverifiable → `refused`, no child (LT-05); spawn or handshake failure → counted toward the restart bound (LT-07, LT-08, LT-10, LT-11). A start asked for in any other state changes nothing and the current state is reported |
| stop (home, actor, reason) | The person, through DEF-5a (v0.9; RECOVERY-v0.2 §2): a confirmed App quit (DEF-6) or the person's "Stop Codex" / "Restart Codex" (DEL-01-04, R18-1 C-12). Never a turn interrupt (DEF-3), a run end (DEF-4) or a window event (DEF-1) | Every state except `absent`, `stopped` and `refused` | The stop record first, then `stopping` → `stopped` with exit facts and the descendant outcome (LT-17…LT-23); with no child, `stopped` directly (LT-20…LT-22). A restart is this stop followed by start | The polite end is ignored → the whole tree is ended after the grace period and `forcedAfterGrace` is recorded; surviving descendants are recorded, never assumed gone (H11); outstanding entries end `ended-unanswered(process-exit)`, with no App decline (RECOVERY-v0.2 §6 U-10) |
| explicit restart | The person | `halted-after-repeated-failure` | LT-16, then verification and a new generation as for start | As start |
| observe lifecycle (from a position) | DEL-01-02 (custody), DEL-01-03 (the `ready(g)` record, S-2), DEL-04-03 (evidence, S-7), DEL-02-03 (EXEC AE-6, AW-12: observation lost or recovered at supplier exit and restart), DEL-03-03 (ADAPTER CT-9, CT-10, S-7, S-8: channel status and in-flight submissions across supplier restart) | Any state | Lifecycle events in order | Observer loss loses nothing within a generation: the main process keeps a bounded in-memory journal per generation and replays it from the observer's position (RECOVERY-v0.2 §3.3 OA-01); a position outside the journal or in a **closed** generation gets a snapshot plus Codex history reads with a gap marker (OA-02). A closed generation's events are not re-readable; views rebuild from Codex history (v0.9; R18-1 C-03). Each window's observer re-attaches; the main process holds the journal (RECOVERY-v0.2 §4.1) |
| read version identity and verification result | DEL-01-03, DEL-01-06, DEL-04-03 | After a verification | §7.1 record; §7.2 result | `unverifiable(<reason>)` is itself a result, never a pass |

**Failure at each step of the start and stop sequences** (§4.2, §4.5):

| Step | What can fail | Who reports it, to whom | Record left | What happens next |
|---|---|---|---|---|
| 1 Resolve | Distribution or launcher not found | The boundary, to the starter | LT-05 with `unverifiable(<reason>)` | `refused` |
| 2 Verify | Label, content identity or output pin differ; the probe fails | The boundary, to the starter and DEL-04-03 | LT-05 with `mismatch(<element>)` or `unverifiable(<reason>)` | `refused`; only the person's explicit start tries again (LT-03) |
| 3 Spawn | The process cannot be created | The boundary, to DEL-01-02 | LT-07 or LT-08 `spawn-failed` with the failure count | `restart-waiting`, or `halted-after-repeated-failure` at the bound |
| 4 Handshake | Error response; no response within the wait limit; the child ends | The boundary, to DEL-01-02 | LT-10 or LT-11 `handshake-failed` with the failure and the count; the tree is stopped; the generation is closed (its client requests `unknown-no-response`, its entries `ended-unanswered`); frames held from it are delivered marked as from a generation that never became ready (never dropped, H4) | As step 3 |
| 5 Ready | — | The boundary, to every receiver | LT-09 with the version identity record | Held frames delivered in received order |
| After ready | The child ends with no stop record, whatever its exit status (S-F-07) | The boundary, to DEL-01-02, DEL-04-03, DEL-02-03 and DEL-03-03 | LT-12 with exit facts and the closed-generation counts; LT-13 or LT-14 | `restart-waiting` or `halted-after-repeated-failure` |
| Stop 1–4 | The tree outlives the grace period | The boundary, to DEL-01-02 and DEL-04-03 | LT-23 with `forcedAfterGrace`, descendant count and handling | `stopped` |

### 4.7 Lifecycle transition table (PROPOSED, v0.8; R12-1)

States are §4.1's. "Bound" is the restart bound of §4.4 (numbers U-05).
Every row writes one lifecycle event record; the column "Also recorded"
lists what that record carries beyond the transition itself.

| ID | From | Event | Guard | To | Also recorded | Told to |
|---|---|---|---|---|---|---|
| LT-01 | `absent` | start-requested | — | `verifying` | actor | observers |
| LT-02 | `stopped` | start-requested | — | `verifying` | actor | observers |
| LT-03 | `refused` | start-requested | the person's explicit start | `verifying` | actor | observers |
| LT-04 | `verifying` | verification-passed | `verified` | `spawning` | verification result | observers |
| LT-24 | `verifying` | development-start-authorized | explicit development option; `unverifiable`; observed label present; no known mismatch | `spawning` | unchanged verification result; `supplierStanding: unverified-development`; reason "U-06 development run: unverified distribution, not the pinned supplier" | starter; all receivers; DEL-04-03 |
| LT-05 | `verifying` | verification-failed | `mismatch`, or `unverifiable` without LT-24 guard | `refused` | verification result with element or reason | starter; DEL-04-03 |
| LT-06 | `spawning` | spawned | — | `handshaking` | new generation *g*; configuration identity | observers |
| LT-07 | `spawning` | spawn-failed | bound not reached | `restart-waiting` | failure; failure count | DEL-01-02 |
| LT-08 | `spawning` | spawn-failed | bound reached | `halted-after-repeated-failure` | failure; failure count | DEL-01-02; the person |
| LT-09 | `handshaking` | handshake-completed | initialize response observed; `initialized` sent | `ready` | version identity record; declared capabilities | every receiver (`ready(g)`) |
| LT-10 | `handshaking` | handshake-failed | bound not reached | `restart-waiting` | failure; count; closed-generation counts | DEL-01-02 |
| LT-11 | `handshaking` | handshake-failed | bound reached | `halted-after-repeated-failure` | as LT-10 | DEL-01-02; the person |
| LT-12 | `ready` | child-ended-without-stop-record | no App stop record for *g* | `exited-unexpectedly` | exit facts; closed-generation counts | DEL-01-02; DEL-04-03; DEL-02-03; DEL-03-03 |
| LT-13 | `exited-unexpectedly` | exit-recorded | bound not reached | `restart-waiting` | failure count | DEL-01-02 |
| LT-14 | `exited-unexpectedly` | exit-recorded | bound reached | `halted-after-repeated-failure` | failure count | DEL-01-02; the person |
| LT-15 | `restart-waiting` | restart-delay-elapsed | — | `verifying` | — | observers |
| LT-16 | `halted-after-repeated-failure` | explicit-restart-requested | the person | `verifying` | actor; the failure count restarts, and the earlier failures stay in the record | observers |
| LT-17 | `ready` | stop-requested | — | `stopping` | actor; stop record | observers |
| LT-18 | `handshaking` | stop-requested | — | `stopping` | actor; stop record | observers |
| LT-19 | `spawning` | stop-requested | — | `stopping` | actor; stop record | observers |
| LT-20 | `verifying` | stop-requested | no child | `stopped` | actor; stop record | observers |
| LT-21 | `restart-waiting` | stop-requested | no child | `stopped` | actor; stop record | observers |
| LT-22 | `halted-after-repeated-failure` | stop-requested | no child | `stopped` | actor; stop record | observers |
| LT-23 | `stopping` | tree-ended | the child and its descendants ended, or forced after the grace period | `stopped` | exit facts; descendant outcome; closed-generation counts | DEL-01-02; DEL-04-03; DEL-02-03; DEL-03-03 |

Not in the table, and so refused as transitions: any automatic start from
`halted-after-repeated-failure` or `refused`; any end classified as
deliberate without a stop record; a second initialize on a generation (§4.2
step 4). A child that ends while `stopping` is the LT-23 end (the stop
record exists). The original 23 rows were exercised by the prototype (VC-27).
CC-H adds LT-24; its offline case is reported separately in CC-H.

## 5. Frame exchange and correlation

- **Framing.** At 0.158.0: one JSON object per newline-terminated line on
  standard output (`observed`). Supplier frames **omit** the JSON-RPC version
  member; the parser must not require it. Notifications carry a top-level
  `emittedAtMs` beside method and parameters (declared in the TS output's
  notification envelope, not in the JSON Schema notification shape); it is
  native content (H6; S-F-08). Outbound frames in the spike carried the
  version member and were accepted; whether its omission is accepted outbound
  is not-observed. Diagnostic output on the error stream (0 bytes in every
  spike run) is captured, bounded, redacted and never parsed as protocol.
- **Classification of each inbound frame:** response (correlates to one
  outstanding client request of the same generation), notification, server
  request (has an identity, expects an answer), or malformed. An
  uncorrelated response is surfaced, not dropped.
- **Client requests.** Each outbound request records: generation, request
  identity, method, **initiator** (`person-directed` via an owning interface,
  `app-rule:<name>`, or `receiver:<deliverable>` for the generic request path;
  §6.8), send position, write result (`written` / `write-failed`), outcome
  (`response-observed(result|error)` / `unknown-no-response`) and, for
  requests carrying additive guidance, the carried-content identities
  (§8.2). A wait limit ends *waiting*, not the
  outcome (H10; F-04).
- **Supplier refusal of an App request.** At 0.158.0 an unknown client
  method is answered with error code -32600 ("Invalid request: unknown
  variant …"), the id echoed and the accepted method list in the message —
  also before initialization; the connection continues (SPIKE §5). This is
  `response-observed(error)`: a definite refusal, not unknown.
- **Order.** Receivers get inbound frames in received order with a
  per-generation receipt position (semantic) that supports re-attachment
  without gaps or duplicates (realization is DEL-01-02's, §6.5: a bounded
  in-memory journal per generation, replayed from the position, RECOVERY-v0.2
  §3.3 OA-01; otherwise a snapshot and Codex history reads with a gap
  marker, OA-02; a closed generation is not replayed, R18-1 C-03).

### 5.1 Client-request path: operations (PROPOSED, v0.8; R12-1)

Each client request is one record of `hosting.client-request-record.schema.json`
(PROPOSED; §9.6).

| Operation | Caller | Result | Failure behaviour |
|---|---|---|---|
| send (method, parameters, initiator) | The person through an owning interface (`person-directed`; DEL-01-02…05); named App rules (`app-rule:<name>`); receivers (`receiver:<deliverable>`, e.g. DEL-03-03 for App-initiated MCP calls, §6.8) | Record `pending`, then `response-observed-result`, `response-observed-error` or `unknown-no-response` | Not `ready` → `refused-not-sent(not-ready)`, nothing written (PROPOSED); governance phase only, a run DEL-02-03 reports holding → `refused-not-sent(run-holding)` for an App-initiated turn start or MCP call (HP-4, §6.7); the write fails → `write-failed`, outcome `unknown-no-response` (H10); the supplier answers an error → `response-observed-error`, a definite refusal (for example -32600, SPIKE §5) |
| end waiting (record, limit) | The caller | `waitingEnded` is recorded | The outcome stays `pending` until a response arrives or the generation closes (H10; F-04) |
| read record | The caller; DEL-04-03 (S-7) | The record with initiator and carried-guidance identities (§8.2) | — |
| (inbound) uncorrelated response | The boundary | Surfaced as `uncorrelated-response` with generation and position | Never dropped and never attributed to a request |

### 5.1.1 Attachment submission association (CC-H-ATTACHMENT-CORRELATION)

For an attachment-bearing `turn/start` or `turn/steer`, the owning NIR source
first preserves its complete immutable ordered per-attachment supply records.
The host then reserves the native RPC identity and persists this optional
client-custody field **before actual scoped pipewrite**:
`submissionAssociation {submissionRef, threadId, supplyRefs, expectedTurnId?}`.
The App-only `submission:<opaque unique token>` is not a native turn ID;
`supplyRefs` is the exact immutable ordered unique list of owning NIR record
references, each with original `turnRef = submissionRef`. Full H5 generation,
RPC identity and method come from the containing client record; they are not
duplicated in the association. `expectedTurnId` is present exactly for steer
and must equal the observed target actually sent; association thread must
match the native request's `threadId`. This is pointer-only existing custody,
not a new transcript, payload/base cache, upload, ledger/RS kind or wire field.

Before association persistence or pipewrite, resolve all supplyRefs to the
complete prepared NIR list, validate thread/target/order/unique token and
current ready generation. Persistence failure (including partial or unreadable
binding) sends **nothing**; partial supply preparation never makes input sent.
The same transient native input composition goes to the pipe; association
metadata never enters native params. On cancellation before dispatch or
changed generation/pipe after preparation, send nothing. Reservation consumes
an RPC identifier but is not supplier acceptance; never reuse/resend it.

The prewrite record is `prepared-not-sent`, `writeResult: not-attempted`,
reserved nonnull request identity and no send position. This names the fact
at that observation point, not a permanent claim after a crash: on cold read,
a prepared-only record with unavailable later write/journal evidence gives
unknown/unavailable dispatch, never proof that native send did not happen and
never permission to retry. Actual observed no-attempt/cancellation can be shown
as not sent; a written frame proves written only, not provider adoption.
After the pipe attempt, existing pending/written or write-failed/unknown
outcomes apply. Ending waiting, view loss or reload never automatically sends.

`resolve_submission(submissionRef)` is a pointer resolver over existing custody
and NIR sources: exact association/full generation/request/method/thread,
write/outcome observations and limits, plus native turn reference only if
observed through the matching result. For turn/start, use that response's
`turn.id`; thread context comes from the original request association (the
0.160.0 response need not repeat threadId); any actually reported contradictory
thread fails correlation. For steer, use matched `turnId` only when it equals
the actual expectedTurnId. Wrong namespace/RPC, malformed/missing/error result,
conflicting thread/target or unavailable native evidence stays uncorrelated/
unknown with cause. No proximity, latest-turn, matching-text or thread-only
inference. Original association, supplyRefs and NIR turnRef never change;
multiple submissions to one native turn remain distinct. Replies stay in the
existing native evidence stream, not copied into attachment records. Explicit
new send mints a new submission token with prior uncertainty visible.

### 5.2 Client-request record transitions (PROPOSED, v0.8; R12-1)

| ID | From | Event | To |
|---|---|---|---|
| CR-01 | — | send in `ready`, written | `pending` |
| CR-02 | — | send in `ready`, write fails | `unknown-no-response` (write result `write-failed`) |
| CR-03 | — | send in any other state | `refused-not-sent(not-ready)` |
| CR-04 | — | governance phase: App-initiated turn start or MCP call for a holding run | `refused-not-sent(run-holding)` |
| CR-05 | `pending` | response with a result, same generation and identity | `response-observed-result` |
| CR-06 | `pending` | response with an error | `response-observed-error` |
| CR-07 | `pending` | the generation closes (exit, handshake failure, stop) | `unknown-no-response` |
| CR-08 | `pending` | the caller's wait limit | `pending` (`waitingEnded`) |
| CR-09 | — | complete ordered NIR supply refs resolved; reserve RPC; preserve pointer association before pipewrite | `prepared-not-sent` (`not-attempted`, no send position) |
| CR-10 | `prepared-not-sent` | same ready generation/pipe; actual native frame write succeeds | `pending` (`written`) |
| CR-11 | `prepared-not-sent` | actual native write fails | `unknown-no-response` (`write-failed`) |
| CR-12 | `prepared-not-sent` | preparation persistence failure, observed cancellation or generation/pipe changes before write | `prepared-not-sent`; no native write, actual no-attempt cause/limits preserved by owning observer |


## 6. Outstanding server-request register — interface

### 6.1 Entry meaning (semantic elements)

| Element | Meaning |
|---|---|
| request identity | Supplier-assigned identity as received (opaque) |
| generation | Generation of the child that raised it |
| method | Supplier method as received |
| classification | `known-answerable` (presented for an answer), `known-app-unsupported` (known kind the App does not serve; explicit error or explicit decline per kind), `unfamiliar` (not in the **familiar set**) |
| subject references | Thread / turn / item / call references as provided, unchanged |
| native parameters | Payload unchanged |
| receipt position | Per-generation position (H5) |
| state | See 6.2 |
| settlement | Native answer content or explicit error/decline content; **answer origin**: `person-via-interaction` (A14 by the person, actor supplied by DEL-01-04), `app-rule:<named rule>` (decline or error only), `app-explicit-error`; plus `supplier-internal` / `resolved-by-supplier` observations (§6.2, §6.6). **Actor reference (v0.9; DECISION-K1 K1-4; R18-1 C-10):** a string "person:‹name set in the App›/‹OS account›/‹Codex account› (identity not verified)", formed by DEL-01-04 from the sources of AAC-v0.2 §7 (NIR-v0.2 §4.5), never inferred by this boundary; the Codex account element is the account DEL-01-05 reports for the home that runs the conversation (the reported email, or "ChatGPT account (no email reported)"; ACCESS-v0.2 §8); plan type is not part of it. It is the same identity RS records as an object (RS `person`); this boundary keeps the string form. **Secret values (v0.9; NIR-v0.2 §4.5 SE-1…SE-3):** when an answer carries values for a question marked `isSecret` (the submission's `secretValuesPresent`), the values are written to the supplier and then **not kept readable**: once the reply is written or its write has failed, the entry's settlement keeps a redaction marker naming the question identities in place of the native content. DEL-01-02's persistence follows the same rule |
| reply write result | `written` / `write-failed` / `not-attempted` |
| acknowledgment observation | `observed(<what>)` / `not-observed` / `not-observable-at-pin`. Writing a reply is not an acknowledgment (ARC §3; DEL-01-02 REQ-004) |

**Familiar set (S-F-05).** The familiar set is the server-request methods of
the **reference generator output** (U-15, §7.3) **as limited by the
capabilities declared at handshake**. At 0.158.0: `currentTime/read` exists
only in the experimental variant, and `attestation/generate` is tied to the
`requestAttestation` capability. A kind whose capability the App did not
declare is `unfamiliar` for that generation.

**Server-request kinds at 0.158.0 and a proposed partition** (PROPOSAL for
the App implementation owner with DEL-01-04/01-05, U-20; the two generator
outputs agree on these kinds — 10 stable, 11 experimental; SPIKE §4). From
v0.9 both co-owners have answered: DEL-01-04 states the answer path per kind
(NIR-v0.2 §4.1: a card for each known-answerable kind, an information line
for the others) and the decline form per kind (NIR-v0.2 §4.3 DM-1…DM-6; this file's
§6.2.1 RT-08); DEL-01-05 does not adopt external-token login (ACCESS-v0.2 §7 CR-9),
so `account/chatgptAuthTokens/refresh` stays known-app-unsupported with an
explicit error. U-20 is narrowed to the App implementation owner's
confirmation:

| Kind (supplier name) | A-name / subject | Proposed classification |
|---|---|---|
| `item/commandExecution/requestApproval` | A14 | known-answerable |
| `item/fileChange/requestApproval` | A14 | known-answerable |
| `item/permissions/requestApproval` | A14 | known-answerable |
| `execCommandApproval`, `applyPatchApproval` (legacy v1) | A14 | known-answerable if raised (whether they are raised on the v2 surface is not-observed) |
| `item/tool/requestUserInput` | input to the agent (not A14); **not act evidence, never host act capture** (R4-12; EXEC CAP-6) | known-answerable; answered only by the person (R9) |
| `mcpServer/elicitation/request` (modes include form and URL) | as above; the prompt is authored by an MCP server or the agent | known-answerable; answered only by the person (R9) |
| `item/tool/call` (dynamic tools; `dynamicTools` is experimental-only on thread start) | App-offered tool | known-app-unsupported unless the App registers dynamic tools (none defined in this increment) |
| `account/chatgptAuthTokens/refresh` | account | known-app-unsupported: DEL-01-05 does not adopt external-token login (ACCESS-v0.2 §7 CR-9); explicit error by a named rule (NIR-v0.2 §4.1) |
| `attestation/generate` | account/attestation | unfamiliar while `requestAttestation` is declared false |
| `currentTime/read` (experimental) | clock service (not A14, not a person's input) | unfamiliar unless the experimental opt-in is declared; then known-answerable by a named App rule (R9 service kind) |

### 6.2 States

```text
received ─┬─(unfamiliar)──────────────► errored(explicit error written | write-failed)
          ├─(known-app-unsupported)───► errored / declined (explicit, per kind, named rule)
          └─(known-answerable)─► outstanding ─┬─ answer/error ─► settling ─► answered | declined | errored
                                              │                    └─► settle-write-failed (outcome unknown)
                                              ├─ supplier-reported resolution ─► resolved-by-supplier
                                              └─ generation closed ─► ended-unanswered(process-exit)
```

`declined` covers an explicit negative answer by the person or an explicit
App rule; the origin says which. `resolved-by-supplier`: at 0.158.0 the
stable notification `serverRequest/resolved` (thread identity, request
identity) is the source. *Observed at OBS-2 (0.158.0, O-3; §10.2 OB2-2;
v0.9):* with an approval request held unanswered, a client
`turn/interrupt` (sent by the observation harness) ended the turn (`turn/completed`, status `interrupted`)
and `serverRequest/resolved` for that request arrived **after**
`turn/completed`, with no answer from the client; a later answer to that
identity was silently ignored (no error, no notification); the command
item never received `item/completed` and is absent from history. So
`turn/interrupt` is one observed before-reply trigger of RT-10 (U-09
narrowed); other triggers are not observed. The cause, when the supplier
reports one, is recorded as observed; it is never inferred (the
notification carries none at 0.158.0).

#### 6.2.1 Register transition table (PROPOSED, v0.8; R12-1)

Each entry is one record of `hosting.server-request-entry.schema.json`
(PROPOSED; §9.6). The rules R1–R9 decide the guards.

| ID | From | Event | Guard | To | Recorded |
|---|---|---|---|---|---|
| RT-01 | — | server-request-received | any inbound server request, in any state including `handshaking` (R1) | `received` | identity, generation, method, subject references, native parameters, receipt position |
| RT-02 | `received` | classified-unfamiliar | not in the familiar set of *g* (§6.1) | `errored` | explicit error content, origin `app-explicit-error`, reply write result (R2) |
| RT-03 | `received` | classified-known-app-unsupported | known kind the App does not serve (§6.1 partition) | `errored` | explicit error by a named rule, origin `app-rule:<name>`. §6.2 also admits a decline where a kind has a decline form; the generated answer forms of the three such kinds at 0.158.0 carry none |
| RT-04 | `received` | classified-known-answerable | — | `outstanding` | classification; R9 origin class |
| RT-05 | `outstanding` | answer-refused | R4, R5 or R9 refuses the answer | `outstanding` | the refusal reason, returned to the caller |
| RT-06 | `outstanding` | answer-accepted-for-write | — | `settling` | settlement content and origin |
| RT-07 | `settling` | reply-written-affirmative-or-content | write succeeded | `answered` | reply write result `written` |
| RT-08 | `settling` | reply-written-negative | write succeeded; the answer is a negative form of its kind (v0.9, NIR-v0.2 §4.3: `decline`, `cancel`; legacy `denied`, `abort`; elicitation `decline`, `cancel`; PROPOSED empty answer map for `item/tool/requestUserInput` and empty grant for `item/permissions/requestApproval`), or the submission says `submittedAs` *decline* | `declined` | reply write result `written` |
| RT-09 | `settling` | reply-write-failed | — | `settle-write-failed` | outcome unknown (H10) |
| RT-10 | `outstanding` | supplier-reported-resolution | `serverRequest/resolved` for this identity and generation before any reply (observed after `turn/interrupt` at OBS-2 O-3, 0.158.0) | `resolved-by-supplier` | source and cause as reported (U-09) |
| RT-11 | `outstanding` | generation-closed | exit, handshake failure or stop (§4.3, §4.5) | `ended-unanswered` | end cause `process-exit` |
| RT-12 | `answered` | supplier-reported-resolution | after the written reply | `answered` | acknowledgment observation `observed(serverRequest/resolved after the written reply)` |
| RT-13 | `declined` | supplier-reported-resolution | after the written reply | `declined` | as RT-12 |
| RT-14 | `settling` | reply-written-protocol-error | later error of an outstanding `known-answerable` request, accepted through R9/§6.4, valid explicit boundary origin or nonempty named App rule; error frame write succeeded | `errored` | native error and exact origin; reply write result `written`; acknowledgment initially `not-observed`; no human-act record |
| RT-15 | `errored` | supplier-reported-resolution | RT-14 later-error branch only; successful reply write; subsequent `serverRequest/resolved` matching full H5 generation and request before generation closure | `errored` | acknowledgment observation `observed(serverRequest/resolved after the written reply)`; no new settlement/act |


**Order of the refusal reasons (PROPOSED; U-26).** When several apply, the
first in this order is returned: `no-such-request`, `generation-closed`,
`already-resolved`, `already-settled`, `origin-not-permitted`,
`invalid-answer`. Identity and generation are checked before state, and
who may answer before what the answer says.

**Acknowledgment reading (PROPOSED; U-09 narrowed at v0.9).** RT-12 and RT-13
read a `serverRequest/resolved` that follows the App's written reply as an
acknowledgment observation, not as `resolved-by-supplier`. Writing a reply
is still not an acknowledgment (§6.1). OBS-1b observed it once after a
written reply, 8 ms after the answer and before the item continued
(§10.1 OB-4), which is consistent with this reading. The trigger before any
reply (RT-10) is now observed for `turn/interrupt` (OBS-2 O-3; §6.2), and
DEL-01-02 adopts this reading (RECOVERY-v0.2 §6 U-09: with no notification
before the generation closes, *not-observed*). The reading stays PROPOSED
until a candidate confirms it.

**Negative answers and the turn (v0.9; OBS-2 §5.1, 0.158.0).** A negative
answer may do more than decline: on the stock pairing a `cancel` answer to a
command approval ended the item `declined` **and** the turn `interrupted`
(decline plus interrupt), as the supplier's own description of `cancel`
says. The boundary records the answer as `declined` (RT-08) and delivers the
turn's end natively; the label is DEL-01-04's (NIR-v0.2 §4.2 LB-1, §4.3
DM-1) and the turn outcome's cause DEL-01-02's (R18-1 C-13).

### 6.3 Rules

- **R1** Every inbound server request creates exactly one entry before any
  other handling, including when no window is open and while `handshaking`.
- **R2** `unfamiliar` requests receive an explicit protocol error
  immediately; never ignored, never answered affirmatively, never queued for
  the person as if known (SOW-123; ARC §3). The error code the App uses is an
  implementation choice; for reference, the supplier's own reply to an
  unknown client method is -32600 and v3 used -32601 (S-F-16).
- **R3** `known-answerable` entries wait for an answer. No timeout, observer
  loss or reconnect produces an answer. **No App rule declines a waiting
  request after any period, and the native `timed_out` form of the legacy
  decision set is never sent** (v0.9; R17-9 "a pending request waits";
  RECOVERY-v0.2 §6 U-11; NIR-v0.2 §4.2 FO-3). A supplier's own resolution
  of a waiting request is `resolved-by-supplier` (RT-10), never an answer.
- **R4** An entry is settled at most once: second answer → `already-settled`;
  closed generation → `generation-closed`; unknown identity →
  `no-such-request`; entry already `resolved-by-supplier` → `already-resolved`.
  The last refusal is what keeps the person's view honest: at 0.158.0 Codex
  silently ignores an answer written after its own resolution, with no
  error and no notification (observed, OBS-2 O-3; §6.2), so without the
  register's refusal an answer would look sent and go nowhere. DEL-01-04
  withdraws the answer controls on `resolved-by-supplier` (NIR-v0.2 §4.4
  CS-6) and shows the refusal's words if an answer races it (v0.9 at RX;
  D3 round-2 J-H11).
- **R5** Answer content must be valid for that method under the reference
  output plus supplement; otherwise `invalid-answer`, entry stays
  outstanding. At 0.158.0 the native answer forms are listed in SPIKE §6
  P-08 (for example command execution: `accept`, `acceptForSession`,
  execpolicy/network-policy amendments, `decline`, `cancel`). A request may
  offer fewer: under approval policy `untrusted`, OBS-1b observed
  `availableDecisions` = `accept`, `acceptWithExecpolicyAmendment`, `cancel`
  only (§10.1 OB-5). An answer the request does not offer is not shown valid
  by the generated types alone; its effect is not observed.
- **R6** A known request with no current observer stays `outstanding`; it is
  not refused for lack of a window (F-02).
- **R7 Truthful origin for A14.** SETTLED by D3: tool-permission and
  sandbox modes are the user's own Codex setting and govern tool execution
  only. DERIVED/INTEGRATION (R-2 D3 bullet, R-10; attribution per R2-11):
  affirmative A14 answers come only from the person through DEL-01-04
  (origin `person-via-interaction`, actor as supplied) or from the user's own
  Codex mode inside the supplier (origin `supplier-internal`, §6.6); **no App
  rule answers an A14 request affirmatively**; an App decline or error is
  permitted only under a named rule recorded as `app-rule:<name>`. SETTLED by
  D2 with D3: no automatic answer stands for a reserved act (A4, A5, A6, A7,
  A12, A13), and A14 answers are not reserved acts. The register never
  records an App rule's answer as the person's act and never infers an
  actor.
- **R8 A14 is tool-execution permission only.** The supplier's decision
  forms are native answer content, not collapsed. An A14 answer of any kind
  governs tool execution within the supplier; it never stands in for A5
  *accept*, A4 *mark checked*, A6 *approve*, A7 *rely* or a checkpoint act
  (D3 "never stand in for a reserved or professional act"; V4-AUT-03,
  V4-AUT-04; AG-13). A14 settlements reach the evidence path as run-record
  tool-permission entries only — never a human-act record, never a grant
  (R2-8; DEL-04-03 R13; App runs only).
- **R9 Answer origin by kind (IR1C-18; INTEGRATION).** Every
  `known-answerable` kind belongs to exactly one origin class:
  - **A14 kinds** (tool-permission requests): R7.
  - **Person-input kinds** (`item/tool/requestUserInput`,
    `mcpServer/elicitation/request` at 0.158.0): answered with content only
    by the person via DEL-01-04 (`person-via-interaction`); a named App rule
    may only decline or error. **Answers are not act evidence and are never
    host act capture** (R4-12; EXEC §5 CAP-6): they are conversation input
    to the agent, even when the person gives them, and never satisfy a
    checkpoint, never record A4–A7, A12 or A13, and never stand for an act on
    host content. An agent question asked this way may be an A8 request; the
    App may answer it by presenting its own act control (EXEC CAP-2), which
    settles no pending supplier request (EXEC CAP-9). v0.9: that control is
    AAC-v0.2 (PROPOSED); every question card offers a plain entry "Open the
    App act control", never pre-filled from an arrival and never opened by
    itself (NIR-v0.2 §4.2 LB-4); when the person opens it from an arrival
    row, the person opened it, not the product (R18-5).
  - **Named service kinds** (at 0.158.0 only `currentTime/read`, when the
    experimental opt-in is declared): may be answered with content by a
    named App rule (`app-rule:<name>`); they carry no person's decision.

  An affirmative or content answer from an App rule to an A14 or
  person-input kind is refused `origin-not-permitted`. Adding a kind to the
  service class is a recorded App implementation choice (U-20).

### 6.4 Register operations offered to receivers (semantic)

| Operation | Caller | Result |
|---|---|---|
| observe entries (current + changes, from a position) | DEL-01-02, DEL-01-04 | Entries and state changes in order |
| list outstanding (by generation / thread) | DEL-01-02, DEL-01-04 | Current outstanding entries |
| answer (request identity, native answer, origin, actor ref) | DEL-01-04 (person path, any valid form); named App rules per R9 (decline/error only for A14 and person-input kinds; content answers only for named service kinds such as `currentTime/read`) | `accepted-for-write` → `answered`/`declined`/`errored` (later RT-14 error)/`settle-write-failed`; or refusal with reason (R4/R5); an App-rule affirmative or content answer to an A14 or person-input kind is refused `origin-not-permitted` (R9) |
| explicit error (request identity, native error, exact origin, full generation) | boundary (R2), named App rules under R9; never person/agent origin | Receipt-time classification remains RT-02/RT-03; for a listed outstanding known-answerable request, accepted through RT-06 then RT-14 `errored` only if written, or RT-09 `settle-write-failed`/unknown if write failed; refusal leaves prior state unchanged |
| (v0.8) refusal order | — | When several refusal reasons apply, §6.2.1 fixes which one is returned (PROPOSED; U-26) |
| read settlement and acknowledgment observation | DEL-01-02 (custody of in-flight requests; RECOVERY-v0.2 §3.5 RQ, §7); DEL-04-03 (evidence, supplied to it directly: R9-7; S-7) | Settlement, write result, acknowledgment observation |

**CC-H-RT-LATE exact receiving join (2026-10-05; proposed technical repair).**
R9 already permits a later named App-rule/boundary protocol error; RT-14
makes its successful write distinct from receipt classification. The boundary
validates request/full H5 namespace, state, origin and native error before
RT-06; refused origin, empty rule name, invalid error, stale generation or
settled request writes nothing and leaves prior state unchanged. No arbitrary
person/agent-origin error authority is introduced. Record native error and
exact origin unchanged; written error is not the person's content answer,
reserved act, checkpoint satisfaction or `human_act`.

RECOVERY RQ-03 receives RT-14 (listed request, later error: closed/errored/
written) or RT-09 (closed/settle-write-failed/write-failed, outcome unknown),
not RQ-08. RT-15 supplies its subsequent acknowledgment to RQ-09. RT-15
never acknowledges a failed write, RT-02/RT-03 receipt error, wrong generation
or a closed generation. A written later error with no observed acknowledgment
at generation closure reaches RECOVERY RQ-05 `acknowledgment_not_observed`;
this is custody evidence, not a new successful settlement. RT-02/RT-03 and
RECOVERY RQ-08 keep their receipt-time behavior. RT-12/RT-13 keep existing
answer/decline guards. Existing server-entry schema admits errored error
settlements and failed writes; no shape/id change needed.

### 6.5 Split with DEL-01-02 (reconciled at v0.9)

DEL-01-01 defines entry meaning, classification, R1–R9, the answer write path
and generation tagging, and witnesses the unknown-request path at the
protocol seam (VER-001). DEL-01-02 owns custody across observation loss,
reconnect and relaunch, recovery of outstanding requests from supplier state,
the register's representation and persistence (DEL-01-02 TBD-002),
stop-time handling (U-10), descendant handling with the App implementation
owner (U-16) and the settlement fixtures. F-01 recorded the overlap.
**Reconciled:** DEL-01-02's Design file accepts this split as written
(RECOVERY-v0.2 §1; §6 "U-14 / F-01 … DERIVED"); U-14 and F-01 are closed.

### 6.6 Decisions made inside the supplier (S-F-11, D3)

When the user's Codex setting routes tool-permission decisions to the
supplier's own reviewer (at 0.158.0 `approvalsReviewer` = `auto_review` or
the legacy `guardian_subagent`; notifications `item/autoApprovalReview/*`;
method `thread/approveGuardianDeniedAction`; all `observed-in-generated-types`,
live behavior not-observed), a decision may be made without any request
reaching the App. The boundary:

- delivers those supplier notifications natively (H6) and does not create a
  register entry for a request it never received;
- where a registered request is later resolved by the supplier, records
  `resolved-by-supplier` with the supplier's reported cause;
- lets receivers present such a decision with origin `supplier-internal`
  (A14 under the user's own Codex mode, D3), distinct from
  `person-via-interaction` and `app-rule`.

It never presents a supplier-internal decision as the person's answer.

### 6.7 Run holds and the supplier (R4-2; D6 closed for Phase 1 by DECISION-4; governance phase retained, R8-1)

**Phase 1, the current phase (V4-WF-05 as amended by SCA-V4-001; R8-1;
R9-1; DECISION-4 D4-1; EXEC-v0.5 §2.1).** A workflow's declared
checkpoints are plan guidance, and the agents manage any pause themselves.
Neither the App nor a host's embedded loop enforces a hold (V4-WF-05), so
no App run is holding (PH-2). The required act is requested by the agent
carrying out the workflow (R9-1; SETTLED by DECISION-K1 K1-1); this boundary issues no
request in the agent's place. How an App run observes an arrival and a
request is DEL-02-03's, defined in EXEC (Wave B). So, for a checkpoint, this
boundary:

- refuses nothing with reason `run-holding`;
- makes no HP-3 named-rule decline;
- sends no `turn/interrupt`;
- claims no hold and carries no hold-support value.

It delivers, unchanged, the native items and notifications from which
DEL-02-03 records arrivals, acts and the optional annotation "continued past
‹checkpoint› before ‹act›" (PH-6, PH-7; EXEC CH-22 Phase 1). The person's
explicit stop (V4-EXE-01) is unaffected. Named-rule declines for any other
purpose remain governed by R7 and R9, as before.

**Governance phase (retained; EXEC-v0.5 §2.2, §2.3).** App-side run holds
at governed checkpoints are `UNRESOLVED{D6}` (DECISION-2). SWBPIPE answered
SQ-02 on 2026-09-28 with no host-held route (route (iv), none planned). D6
is closed for Phase 1 by DECISION-4 and re-opens when the governance phase
is taken up (R8-2). The hold machine, its hold points (EXEC-v0.5 §2.3:
HP-1…HP-4, HP-H) and the hold-support value of each governed checkpoint
(EXEC §3.6, values ruled by R5-1, as amended by R8-2) are DEL-02-03's. In
that phase this boundary supplies only these facts and limits:

- **HP-2 `turn/interrupt`.** A stable client method at 0.158.0 (parameters:
  thread identity, turn identity; empty result). Up to v0.8 its live effect
  was not observed. *Observed at OBS-2 (0.158.0, one pairing; O-1, O-3;
  §10.2):* the empty result came in about 21 ms; `turn/completed` with
  status `interrupted` followed; two deltas arrived after the request and
  before its result; an open item never received `item/completed` and is
  not kept in history; a pending approval was resolved by the supplier
  (RT-10). For a hold nothing relies on it, and no receiver depends on it
  (R4-2; EXEC-v0.7 §2.3 HP-2 "Not adopted"). The App sends it for another
  purpose: the person's interrupt of a turn (DEF-3) and the interrupts of a
  confirmed quit (DEF-6), each with a stop request written first
  (RECOVERY-v0.2 §2, §3.4 SR). The outcome is recorded as observed, and any
  action completed after the request is recorded as observed, never as
  prevented.
- **HP-3 named-rule decline.** While a run is held, an App named rule may
  *decline* a tool-permission request that reaches the App (R7), with origin
  `app-rule:<name>`. This is a permitted **best effort** under D3: requests
  that the user's own Codex mode settles inside the supplier (§6.6) never
  reach the App and are not held; a decline is never an affirmative answer
  and never a hold guarantee.
- **HP-4 the App initiates nothing for a holding run** (EXEC-v0.3 §2 HP-4,
  now EXEC-v0.5 §2.3, governance phase; including its scope ruling; first
  proposed in EXEC-v0.2). For a run DEL-02-03 reports as holding, the boundary
  accepts no App-initiated start of a turn and no App-initiated call for that
  run — in particular no `mcpServer/tool/call` or `mcpServer/resource/read`
  where the App is the caller (§6.8) — and records any such attempt as
  refused with reason `run-holding`. This is App behavior, not interposition:
  it does not stop anything Codex does inside a turn already running, which
  is delivered natively and recorded by DEL-02-03 as action during hold.
  Requests from the person's own explicit acts (for example an explicit
  stop, V4-EXE-01) are not blocked by it. **Person-directed turns**
  (settled by EXEC-v0.3 (commit d3cebd1cc, sha256 889e48819baa21ec112c4878e4e38004dcbaa9eb3645a31c24221ac116ee548e) §2 HP-4 scope, INTEGRATION): a turn the person
  starts with their own message on a holding run is **not blocked**; the
  boundary carries it with initiator `person-directed`; the checkpoint
  disposition is unchanged; any governed agent action in that turn is
  *action during hold* (recorded by DEL-02-03). The boundary never presents
  such a turn as a hold.
- **HP-1 interposed App code** in the supplier's dispatch path is not
  adopted (R4-2). Nothing in this boundary sits between the supplier and its
  own tool dispatch.
- **HP-H host-side hold** is the host's. It is **not offered by SWBPIPE**
  (SQ-02 route (iv), answered 2026-09-28). This boundary neither provides
  nor observes it beyond delivering native tool-call items and results.
- The boundary makes **no hold claim** and changes no hold-support value.
  Where this file mentions hold support it uses R5-1's four values only:
  *enforced by the host loop*, *enforced on the host route*, *not
  established*, *not enforceable*. Nothing in §6.7 raises an App-only
  checkpoint above *not enforceable*; HP-3 and HP-4 are best effort in every
  App run. It delivers the native items and notifications from which
  DEL-02-03 records "action during hold".

### 6.8 MCP surfaces at 0.158.0 (R4-12; ADAPTER F-3)

Classified from the committed 0.158.0 JSON Schema bundle and the spike
inventory; all rows are `observed-in-generated-types` unless marked.
`mcpServerStatus/list` and `mcpServer/startupStatus/updated` (first row,
marked *Observed (OBS-1)*) were observed live at OBS-1 (§10.1 OB-10;
`OBS_1_0.158.0.md` §5, §7, A-1; one local route, one model; not
qualification). The `mcpToolCall` row states what OBS-1 did not observe.
No other surface of this table was exercised live (C0; V19b m-4). "Caller"
is who initiates the MCP-side effect.

| Surface (supplier name) | Kind / variant | Caller | Boundary treatment | Receiver; evidence standing |
|---|---|---|---|---|
| `mcpServerStatus/list` (optional thread identity, detail, paging); `mcpServer/startupStatus/updated` notification | Client request (stable); notification (stable) | App (read) / supplier (report) | Generic request path; native delivery (H6) | DEL-03-03 channel state. A supplier status `disabled` is an **App-side configuration fact, never A13** (R4-13). *Observed (OBS-1)*: before any thread, `mcpServerStatus/list {}` listed the configured server with `runtimeStatus` null and no startup notification; on a thread, `mcpServer/startupStatus/updated` went `starting` → `ready`, and a thread-scoped list showed `connected` (OBS record A-1, §7; §10.1 OB-10) |
| `config/mcpServer/reload`; `config/value/write`, `config/batchWrite` (write a key path into the user's Codex configuration) | Client requests (stable) | App, only as **person-directed** through the owning interface (DEL-03-03 OC-3; DEL-01-05) | Carries the change and records initiator; never initiated by an App rule or on an agent's instruction (H9: the person's own Codex configuration). v0.9: DEL-01-05 writes with an explicit `filePath` and `expectedVersion` and never writes a credential (ACCESS-v0.2 §6 Q-8, §7 CR-8). Under K-1 the App home's `config.toml` is a link to the person's file; whether a write through the link lands in the person's file is not observed at 0.158.0 (OBS-2 UNRESOLVED; inference: it would) | App-side configuration is **never A13 evidence**; any configuration an agent could write is not act evidence (R4-13). The host's refusal is the authoritative "off" (ADAPTER) |
| `mcpServer/oauth/login`; `mcpServer/oauthLogin/completed` | Client request; notification (stable) | App, person-directed | As above; credentials stay with the supplier | DEL-01-05 / DEL-03-03 (OC-6); not an act |
| Thread item `mcpToolCall` {server, tool, arguments, status, result, error, …}; `item/mcpToolCall/progress` | Items and notification (stable) | **The agent** (model-issued call) | Native delivery only; the boundary never alters, retries or answers these calls | DEL-03-03 dispatch observation; host outcome per DEL-03-02/03-03. Whether an MCP tool call raises an A14 request at 0.158.0 is **not observed**: on the local Responses route of OBS-1 no MCP tool reached the model (`namespace` tool dropped; §10.1 OB-1), so no such item was produced |
| `mcpServer/tool/call` (server, thread identity, tool, arguments, `_meta`; result content, structured content, is-error, `_meta`) | Client request (stable) | **The App** | App-origin only: recorded with initiator (§5) and never presented as the agent's call. Not issued for a holding run (HP-4, §6.7). It is **never used to act as the agent**, to perform, request on the person's behalf or record any person's act (A4–A7, A12, A13), or to submit a host operation in the agent's name. No use on a host channel is defined in this increment; a use needs DEL-03-03's definition and its own origin in the host's terms. It requires a thread identity; whether the call or its result enters that thread's items or model context is **not observed** | DEL-03-03 (OC-2/OC-7); results are App-origin evidence only |
| `mcpServer/resource/read` | Client request (stable) | The App | As `mcpServer/tool/call`: App-origin read; content reaches the App, not the model, unless the App supplies it | DEL-03-03; App-origin |
| `mcpServer/elicitation/request` | Server request (stable) | MCP server / agent → person | R9 person-input kind | Not act evidence; never host act capture (R4-12) |
| `mcpServer/event/stream/start`, `…/stop`; `mcpServer/event/stream/notification` | Start/stop experimental-only; notification in the stable set | App | Not used; unfamiliar/unused unless the experimental opt-in is declared and DEL-03-03 defines a use | — |
| `item/tool/call` (dynamic tools, experimental-only registration) | Server request | Agent → App | known-app-unsupported (§6.1); choosing dynamic tools changes the familiar set for the whole App (ADAPTER F-9; S-F-05) | DEL-03-03 OC-2 |

**The required-tool check's catalog read (RX; ADAPTER-v0.6 §7.7; EXEC-v0.6
§3).** The App's required-tool compatibility check reads a host's catalog
edition, and that read is **App-origin**: it is the only App-origin host read
in this increment (ADAPTER §7.7), it is recorded with initiator App (§5), it
is never presented as the agent's call, and it shows no checkpoint outcome.
Which supplier surface carries it (the tool descriptors of
`mcpServerStatus/list`, an App-origin `mcpServer/tool/call` of the host's
catalog read, or on the command-line path the host's catalog command run by
the App) is not chosen here; a use of `mcpServer/tool/call` for it needs
DEL-03-03's definition (U-24).

## 7. Supplier version identity and verification

### 7.0 Current maintained supplier identity (SUP1; proposed adoption)

Owner direction in `APP-V4-GROUP-A-20261004/OWNER_DECISIONS.md` advances the
development/definition pin to **0.160.0**. This supersedes the active D4
0.158.0 declaration; dated 0.158.0 tables, exchanges and observation files
below retain their historical meaning. The new generated reference package
is [`generated/0.160.0/COMMITTED_STATE.md`](generated/0.160.0/COMMITTED_STATE.md),
with exact identities in `SUPPLIER_IDENTITY.json` and all four-variant native
generation manifest. Independent SUP1 review precedes product propagation.

| Maintained element | Current value / standing |
|---|---|
| Declared development/definition pin | `0.160.0`, owner-authorized SUP1 |
| Observed version label | `codex-cli 0.160.0` (fresh scratch probe) |
| Expected development main-binary identity | SHA-256 `112fae7a5a1223e673c8a1791d32338f37df8b527ff1159bb8adac6c4dbf1b4b`; main binary identity only, not a qualified full distribution |
| Generated output identity | 0.160.0; TS/JSON, stable/experimental, no formatter; repeat runs byte-identical; complete manifest in generated package |
| Expected qualified distribution identity | Not established; full executable distribution/App candidate qualification still owed |
| Development standing | LT-24 `unverified-development` unless §7.2's actual three-part verification basis is established; main-binary hash alone cannot yield LT-04 |

The four additive/documentation changes and unchanged supplier seams are
recorded in `COMPARISON.json`. `mcpServerStatus/list` gains optional
`serverName`; native carriage accepts it without requiring its use. Cursor
anchors widen the item paging request; returned string cursor consumers keep
their existing path. `Turn.error` may accompany failed or interrupted turns;
`tooManyDenials` is another native error value, not a new policy or authority.
No new absent-from-both-generator element is established. Original reference
choice U-15 and required qualification remain with their current owner.

### 7.1 Historical 0.158.0 version identity record (semantic; retained)

| Element | Source | At 0.158.0 (SPIKE §3, §5) |
|---|---|---|
| declared pin | App candidate's pin record | `0.158.0` (D4: definition/generation; not qualification) |
| observed version label | Binary's own version report | Text `codex-cli 0.158.0` (`observed`) |
| distribution content identity | Per-file content identities of the vendor tree the supplier executes: main binary and siblings (at 0.158.0 `bin/codex`, `bin/codex-code-mode-host`, `codex-path/rg`, bundled `zsh` and voice resources); composition U-17; algorithm recorded with each value (U-08) | Spike-observed SHA-256 of `bin/codex` 788a818fbb9596869c7a487554507cb8bdca17584b8671112b23f9e225ba35c8; siblings per SPIKE §3. These are spike observations; they become the *expected* identity only when recorded by a qualification of the pin |
| expected distribution content identity | Recorded when the pin is qualified | Not yet recorded (no qualification) |
| launcher record | Wrapper or vendor binary; environment the launcher adds | Wrapper adds `CODEX_MANAGED_PACKAGE_ROOT`, `CODEX_MANAGED_BY_NPM=1`; both launchers gave the same handshake (`observed`) |
| handshake-reported identity | Initialize response elements | `userAgent`, `codexHome`, `platformFamily`, `platformOs`; **no version element**; the version appears only inside `userAgent` text after the client's own name (S-F-01) |
| declared capabilities | What the App declared at handshake | Recorded per generation (§4.2 step 4) |
| generated-output identity | Pin + generator kind (TS / JSON Schema) + variant (stable / experimental) + formatter use + output manifest identity | Four variants, byte-deterministic; manifest sha256 42b95826…69e over 2,359 files (SPIKE §4) |
| supplement identity | Content identity and version of the supplement | Empty at 0.158.0 (no entries; §7.3) |
| configuration identity | Launcher, arguments, environment supplied by the App; from v0.9 also the App-owned home's identity (H-acct, H-key; §4.2 step 3), the state and targets of the linked files (`config.toml`, `AGENTS.md`, `skills/`), and the K-12 session flags the App passed (ACCESS-v0.2 §9). **Never a credential** (ACCESS-v0.2 §7 CR-7, CR-8): no key, token or credential environment variable is ever part of it | Per generation (H1) |
| verification result | `verified` / `mismatch(<element>)` / `unverifiable(<reason>)`, time, generation | — |

### 7.2 Verification rule

Verified means: observed version label equals the declared pin **and** the
distribution content identity equals the expected identity **and** the
generated-output identity names the same pin. A label alone is not
sufficient (AC-006; F-06). The handshake-reported identity is a **consistency
check only**: a version parsed from `userAgent` text must not contradict the
declared pin, but it is weaker than the label and content checks and never
substitutes for them (S-F-01). Mismatch → `refused`. Unverifiable →
`refused` except the explicit LT-24 development option: an observed version
label is required and every available comparison must show no mismatch.
LT-24 retains `unverifiable(reason)` and labels the generation, ready
announcement, diagnostics and version display `unverified-development`,
with "U-06 development run: unverified distribution, not the pinned supplier".
This option is never enabled by absence of qualification evidence, does not
qualify a pin, and grants no production or release reliance. Its startup option
name and storage are implementation choices. U-06 is resolved by CC-H, subject
to independent review; original qualification obligations remain open.

Probe side effect: at 0.158.0 even the version report writes into the home
it runs against (`CODEX_HOME/tmp/arg0/…`; S-F-17). The label probe uses a
separate App-owned **probe home**, H-probe, which is never an account home
(v0.9; ACCESS-v0.2 §3; K-1); the content-identity check does not execute the
binary and has no such effect.

### 7.3 Generated output, reference choice and supplement (SOW-121, REQ-002)

- Output is produced by the supplier's own generators (at 0.158.0
  `codex app-server generate-ts` / `generate-json-schema`, each with an
  `--experimental` variant; both labeled `[experimental]` by the supplier —
  F-12) and is never edited by hand. Generation was byte-deterministic at
  0.158.0 (SPIKE §4, SV-01).
- **Committed form (parent re-selection, SPIKE §4;
  `generated/0.158.0/COMMITTED_STATE.md`).** The two JSON Schema
  experimental bundles, `MANIFEST.sha256`, `_spike/` and `COMMITTED_STATE.md`
  are committed under `Design/generated/0.158.0/` (about 1.9 MB). Not
  committed: both TS trees (1,605 files) and the other 752 JSON Schema files;
  all are regenerated with `_spike/generate.sh` at the pin and verified
  against the manifest. The manifest is byte-unchanged; its `# COMMITTED`
  comment describes the spike's *proposed* form and is superseded by
  `COMMITTED_STATE.md`. Where committed TS types live is decided with the App
  implementation when it starts.
- **Reference output — options for the App implementation owner (U-15;
  S-F-03).** At 0.158.0 the two generators disagree: the TS output has three
  client methods (`getAuthStatus`, `getConversationSummary`,
  `gitDiffToRemote`) and two notifications (`rawResponse/completed`,
  `rawResponseItem/completed`) that the JSON Schema output lacks, and only TS
  declares the `emittedAtMs` envelope element. The running server accepts
  exactly the 170 TS client methods. Server-request kinds agree.

  | Option | Reference | Consequence |
  |---|---|---|
  | O-R1 | TS experimental output | Matches the server's accepted client set and the envelope; not committed, so conformance depends on regeneration + manifest check |
  | O-R2 | JSON Schema experimental bundles | Committed and machine-readable (suits a build-time method list for the Rust side, §12); five elements plus `emittedAtMs` need supplement entries |
  | O-R3 | Union with per-element provenance | Complete; divergence itself becomes a recorded, diffed artifact at each upgrade |

  The choice changes notification-familiarity marking and client-request
  conformance, **not** server-request classification at 0.158.0.
  Drafting observation (non-binding): O-R3 matches how the O-1 proposal would
  use both outputs. The App implementation owner decides.
- **Experimental status** is determined only by diffing the stable and
  experimental variants of the chosen reference, never from doc comments (at
  0.158.0 `item/plan/delta` says "EXPERIMENTAL" but is stable; S-F-04).
  Experimental-only elements the App needs at 0.158.0 include plan
  collaboration mode on turn start, `collaborationMode/list`,
  `thread/settings/update`, `dynamicTools` and `availableDecisions` (SPIKE §4).
  Using them requires declaring the experimental opt-in (F-13). v0.9: of
  these the App uses plan mode (K-5; NPTD-v0.2 §4); `thread/settings/update`
  is not used for workflows (R19-7), and no dynamic tool is registered. Observed at
  OBS-1b: an approval request carried `availableDecisions` although the
  client declared `experimentalApi` false (§10.1 OB-5). So a client that has
  not opted in may still receive an experimental-only element in a server
  request at this pin; the element's classification stays the variant
  diff's, and receivers must not treat its presence as the opt-in.
- **Supplement.** Narrowed to (a) elements absent from the chosen reference
  output (for O-R2: the five TS-only elements and `emittedAtMs`) and (b) any
  field observed in a recorded exchange but absent from both outputs. Each
  entry names its pin and its evidence (a recorded live exchange or the
  other generator's output). At 0.158.0 the spike found **no** field absent
  from both outputs; the supplement is empty unless O-R2 is chosen.
- The main process needs at minimum the familiar server-request set and the
  answer-validity rules (R2/R5); how much of the type set the Rust side
  carries is part of OI-008 (§12).

## 8. Seams to receivers

| Seam | Receiver | Supplied by this boundary | Not supplied here |
|---|---|---|---|
| S-1 lifecycle and register | DEL-01-02 | §4 states with generation; App stop record; `unknown-no-response`; register interface §6; exit and descendant facts; receipt positions | Durable custody, reconnect/relaunch, persistence, recovery reads, settlement fixtures, descendant policy (U-16, joint). **Receiving side (v0.9):** RECOVERY-v0.2 §1 (reconciliation with §6.5), §4.2 (consumed), §2 (DEF-1…DEF-7), §3.3–§3.5, §5, §7 |
| S-2 version identity + plan/revision | DEL-01-03 | Version identity record with each `ready(g)`; native plan items and plan updates unchanged with generation and receipt position; generic request path for plan interactions. At 0.158.0 each plan update carries the **whole plan with no revision identity**, plan deltas must not be assumed to concatenate to the completed item, and plan mode is experimental-only (S-F-13). At OBS-2 (0.158.0, O-8) plan mode produced one `plan` item streamed by `item/plan/delta`, no `turn/plan/updated`, and persisted on later turns until the default mode was sent | Revision identity (DEL-01-03 derives it from turn/item identities and receipt positions), registry, storage, export, UI, checker (SOW-128). **Receiving side (v0.9):** NPTD-v0.2 §2, §5.2 RV-1, RV-2 |
| S-3 request answering | DEL-01-04 | Register operations; refusal reasons incl. `origin-not-permitted`; settlement; supplier-internal decision notifications (§6.6) | Request cards, answer UX, attachments, outcome presentation. **Receiving side (v0.9):** NIR-v0.2 §4 (cards, decline forms, card states over §6.2.1), §5 (turn outcomes, the three stop operations), §6 (attachments); AAC-v0.2 (the App act control, PROPOSED) |
| S-4 embedding and provider | DEL-01-05; DEL-03-03 (channel status); DEL-04-03 via S-7 | Carriage of supplier account methods and per-conversation provider selection (at 0.158.0 `modelProvider` on thread start and resume; `modelProvider/capabilities/read`); **observed model destination** per thread/turn (§8.3; R4-1); §8.1 account; recorded-exchange evidence per §9; the start-up network observation (L-4); spawn per App-owned home (§4.2 step 3) | Sign-in (including OAuth) and API-key flows, offered as options with no default between local and cloud (DECISION-4 D4-3; R8-9); provider configuration, server-substitution checks. The account home is decided (K-1; ACCOUNT-HOME-RECORD-v0.2). **Receiving side (v0.9):** ACCESS-v0.2 §19 (receiving comparison, R18-7 G-1), §3, §4, §9 |
| S-5 distribution identity | DEL-01-06 | Distribution content identity over the vendor tree, version label, launcher record; spike-observed signing facts (Developer ID, hardened runtime) as observations only | Packaging, signing, notarisation, relocation of the vendor tree (not-observed), distribution |
| S-6 additive guidance | DEL-02-04 for role guidance; DEL-02-02 for a workflow's run-start text (v0.9; R19-7) | Carriage unchanged through the supplier's supported inputs; per-thread/turn content-identity evidence (§8.2). **v0.9 (R17-8, R19-1, R19-7, R19-8; OBS-2 O-5, OBS-3 W-6, at 0.158.0):** role guidance travels only as `developerInstructions` on `thread/start`, where it is applied; `baseInstructions` is never set. On `thread/resume` and on `thread/fork` the same element is **accepted and not applied** (silently ignored), so it is not a carrier of changed guidance. A workflow is supplied per run as a **text element of the `turn/start` that starts the run**, composed by DEL-02-02 with framing lines naming the workflow and revision; the boundary carries it as any turn input and records it (§8.2) | Guidance composition and role files (ROLE-v0.2 §5.1); the role is fixed for the conversation's life and edits reach new conversations (DECISION-L L-2, R19-3; ROLE-v0.2 §3.1 SL-8, §4.4); workflow semantics (WR-v0.2), run-start composition and framing (WR-v0.2 §16.2; supply check §16.6), run start (DEL-02-03) |
| S-7 evidence | DEL-04-03, directly (R9-7; DEP-04-03-027, arc N-15); DEL-09-06 for the supplied-guidance and model-destination evidence (DEP-09-06-032, arc N-C5) | Observed facts: version identity, generation, declared capabilities, settlement with origin, supplier-internal decisions, unknown outcomes, supplied-guidance identities, observed model destination (§8.3), client-request initiators (incl. App-initiated MCP calls, §6.8). A14 settlements go only to the run record's tool-permission entries (DEL-04-03 R13), never to a human-act record or a grant (R2-8) | Record format, writer/reader, any human act. Custody of in-flight requests across observation loss and relaunch, which is DEL-01-02's separate contribution (S-1; RECOVERY-v0.2 §3.5, §5, §7, §8.2) |

**Receivers the live registers name (R9-6; rebuilt at v0.7).** The seams
table above is unchanged except S-7. The rows below are the ACTIVE rows of
the consumers' registers, with their DAG-003 layer, and where this file
already holds what each row names. No contribution is defined by this
table.

| Receiver | Register row (arc; DAG-003 layer) | Contribution the row names | Where this file holds it |
|---|---|---|---|
| DEL-02-01 | DEP-02-01-025 (N-16; admitted) | Harness-capability meaning, so that its harness-capability requirements refer to it | The 0.158.0 inventory (SPIKE §4; `generated/0.158.0/`) and, from v0.8, the capability account §8.4: every supplier surface placed in one capability group with a meaning, availability signals and standing labels (PROPOSED). Portable names stay DEL-02-01's; WD-v0.8 §4.2.5 names the group each portable name resolves to (HC-7; R14-5), which closes F-27 |
| DEL-02-03 | DEP-02-03-023 (N-23; admitted) | Observed stock-Codex supplier facts, as capability information | §6.1, §6.7, §6.8, §10, R9 |
| DEL-03-03 | DEP-03-03-013 (N-B4; admitted) | Supplier MCP and dynamic-tool surfaces and channel-status facts at 0.158.0 | §6.8; §8.3; S-4 |
| DEL-03-04 | DEP-03-04-021 (N-B9; admitted) | The supplier boundary: native surfaces for optional external access | §6.8 |
| DEL-04-03 | DEP-04-03-027 (N-15; admitted) | Observed supplier facts: supplied guidance, model and destination, tool-permission settlements | S-7, §8.2, §8.3, R8; supplied directly (R9-7) |
| DEL-09-06 | DEP-09-06-032 (N-C5; admitted) | App-side supplied-guidance and model-destination evidence | §8.2, §8.3 as definition; no evidence exists |
| DEL-02-04 (outside the first increment; Design file ROLE-v0.2) | DEP-02-04-010 (admitted) | The supported native supplier receiving contract for additive role supply | S-6; §8.2. The supplier-side mirror row is still a register proposal (pass-2 closeout C1-B R-11-1; F-16) |
| DEL-06-01, DEL-09-01 (outside) | DEP-06-01-013, DEP-09-01-019 (admitted) | The selected supplier pin, before protocol generation and qualification | Pin note; §7.1; U-01 (0.158.0 is the definition and generation pin only) |
| DEL-09-02 (outside) | DEP-09-02-009 (admitted) | Supplier hosting and protocol contribution and scoped feature checks, before the joined witness | §9 method and the designed cases; nothing is qualified |
| DEL-01-02, -03, -04 (Design files RECOVERY-v0.2, NPTD-v0.2, NIR-v0.2 with AAC-v0.2); DEL-01-06 (outside; no Design file) | DEP-01-02-018, DEP-01-03-011, DEP-01-04-007, DEP-01-06-006 (admitted); this register's DEP-01-01-019, -020, -021 and -023 | The stock supplier boundary, generated types, selected identity | S-1, S-2, S-3, S-5 |
| DEL-01-05 (Design files ACCESS-v0.2, ACCOUNT-HOME-RECORD-v0.2) | DEP-01-05-012 (held), DEP-01-05-013; this register's DEP-01-01-022, and DEP-01-01-024 (UPSTREAM, held) | The selected protocol and pin; embedding-qualification input | S-4; §8.1 |

The 0.158.0 inventory in SPIKE §4 (170 client methods, 11 server-request
kinds, 85 notifications in the TS experimental output) is the input to
harness-capability naming owned by DEL-02-01 (V1-C AB-10); no naming is
chosen here. DEL-02-01's register row DEP-02-01-025 (arc N-16, admitted)
asks for "the harness capability meaning supplied through DEL-01-01";
its ScopeOfWork CLM-002 says DEL-01-01 "supplies the harness capability
inventory". This file holds the inventory. Up to v0.7 a capability meaning
beyond the inventory, named by DEP-02-01-025, was **not yet defined here**
(F-27). From v0.8, §8.4 gives that meaning as a capability account grouped by
capability; the portable names stay DEL-02-01's. Since the RP-3 repair
(R14-5), DEL-02-01's WD-v0.8 §4.2.5 states, in its group column, the one
§8.4 group each of its ten portable names resolves to at 0.158.0, and this
file's grouping stands where the two read a member differently (§8.4,
"Members WD reads differently"); F-27 is closed.

### 8.1 Local-provider requirement account (REQ-005, AC-005; to DEL-01-05)

| Requirement | Published / basis claim (dated) | At 0.158.0 (SPIKE §6) |
|---|---|---|
| L-1 Local servers act as Codex model providers chosen per conversation | V4-ARC-04; T7 (2026-09-25) | `observed-in-generated-types`: `modelProvider` on thread start and resume; `modelProvider/capabilities/read`; CLI `--oss`, `--local-provider lmstudio|ollama` is `published-only`. Per-conversation effect live: not-observed |
| L-2 Wire interface Codex requires from a provider | ARC §6: "oMLX also serves the Responses API Codex requires" | **not-observed** in the spike: provider definition form and required interface are not in the generated output (R-10; V1-C D-22). **Observed at one pair (OBS-1, OBS-1b; §10.1 OB-8):** a custom provider with `wire_api = "responses"` worked against LM Studio 0.4.16's `/v1/responses`, streamed; the server ignored `prompt_cache_key` and `include` and turned the developer role into system. Not qualification |
| L-3 Tool calling through the provider | ARC §6, §8 risk | not-observed in the spike. **Observed at one pair (§10.1 OB-1, OB-2):** a flat function tool (`exec_command`) was called through LM Studio 0.4.16's Responses interface; MCP tools were **not** delivered: LM Studio logged "Ignoring unsupported tool type(s): namespace." and the MCP test tool never reached the model (that Codex offered them as that `namespace` tool is the record's inference, OB-1). Consequence at this pin: on such a route a host's MCP tools are unusable (F-31). **OBS-2 (0.158.0, O-4; §10.2 OB2-4):** the pass-through tap showed that Codex's delegation tools also travel only inside a `namespace` tool (`multi_agent_v1`), which LM Studio 0.4.16 drops, so on that route delegation is unavailable too; no configuration found sends them as flat functions. Carried into ACCESS-v0.2 §11 CH-2 |
| L-4 Supplier network traffic at start (named "Local-operation boundary (priority 3)" up to v0.6) | ARC §1 priority 3. As amended by SCA-V4-001 it speaks of a host's agent ("It sends data only to the selected model service and to destinations the person has allowed, and every destination contacted is recorded and shown") and states no App local-operation boundary; ARCH §4 says the host-agent property does not govern the App's own Codex. No accepted text now decides this traffic (U-18) | **observed**: with a fresh home the supplier fetched ≈24 MB from `github.com/openai/plugins` at start, with no sign-in and no turn; warm home: none seen in ~6 s; whether a setting disables it: not-observed (S-F-10; F-14; U-18). **OBS-1 and OBS-1b (§10.1 OB-9):** with `[analytics] enabled = false` and no sign-in, start-up also contacted chatgpt.com (a remote-control loop and a featured-plugins request answered 401) and synced the plugin repository again (a full fetch on a home not fully synced; `git ls-remote` only on the next run). Analytics off does not stop it. **K-12 decided (v0.9; DECISION-K3 revised; ACCESS-v0.2 §9):** the App turns off whatever Codex's **settings** allow, shows the rest in its network view and records it. **OBS-2 (0.158.0, O-7; §10.2 OB2-9) fills the App-action column:** `[features] plugins = false` stops both start-up connections seen (the featured-plugins request to chatgpt.com and the plugin-repository check or fetch from github.com, including a fresh home's ≈24 MB fetch); `remote_plugin`, `apps` and `remote_control` (a `removed` feature) do not. Plugins follow the person's own setting (DECISION-L L-3), read through the link: off → the connections stop (the App adds `plugins = false` only in the fallback with its own configuration); on → they happen, per App-owned home, and are shown and recorded. The remote-control loop is stopped by no setting; only an internal environment variable stops it, which is not a setting and is not used (R18-3); without sign-in it opened no socket at OBS-2 (local work only), and with sign-in it is not observed (DECISION-L L-6). The network view shows it so. Codex does not report its own connections in its event stream; the App learns them from a per-pin expected list and its own observation of the process tree's sockets (ACCESS-v0.2 §9) |
| L-5 Credentials | V4-ARC-04; DECISION-4 D4-3 (R8-9) | `observed-in-generated-types`: login variants incl. API key and ChatGPT account sign-in; credential store modes `file`/`keyring`/`auto`/`ephemeral`; actual storage and local-provider key need: not-observed. **Model access choice (D4-3):** local and cloud are options the person chooses among, with **no default**; a cloud model is reached by **OAuth sign-in or an API key**. V4-HOST-01, as amended by SCA-V4-001, carries D4-3 for a host's agent; for the App path, D5 already leaves the model to the person. This boundary selects no default and carries the supplier's variants unchanged. Whether the supplier's sign-in variant serves D4-3's OAuth option for a given cloud provider is not-observed. Which flows the App offers is DEL-01-05's (S-4). **v0.9 (ACCESS-v0.2 §2, §6, §7):** offered: ChatGPT sign-in in the browser (`chatgpt`), device-code sign-in (`chatgptDeviceCode`), and an API key (`apiKey`), the key in its own App-owned home H-key (K2-1, adopted by DECISION-L L-1). Not offered: `chatgptAuthTokens` (external tokens, CR-9), `amazonBedrock*`, gateway OAuth. No sign-in or API-key flow is observed (DECISION-L L-6) |
| L-6 Distinct from host loop interface | ARC §4 V4-ARC-10 | Unchanged: each interface is qualified separately (AG-14). V4-ARC-10 (D-20) stays the v4 host-loop direction (DECISION-4 D4-2; R8-8) |

An unqualified server example establishes neither supported substitution nor
provider access (REQ-005).

### 8.2 Supplied-guidance evidence (V1-C D-16, R-10)

For every client request that carries additive guidance input (at 0.158.0
the developer instruction element of thread start, and the other carriers
in the table below; from v0.9 also the text element of a workflow's
run-start turn), the boundary records, per thread and per turn at which it applies: the
request identity and generation, which guidance element was carried, the
**content identity of each guidance input actually carried** (algorithm
U-08), and the source identity supplied by the composing owner (DEL-02-04
for role guidance; DEL-02-02 for a workflow's run-start text and the
run-end line, with the workflow identity per R-9; WR-v0.2 §16.2). The recording tap (§9.1) holds
the bytes as evidence. These records are supplied to DEL-04-03 directly
(S-7; R9-7: DEL-04-03's ScopeOfWork CLM-004 takes "observed supplier facts
(supplied guidance, model and destination, tool-permission settlements)
from `DEL-01-01`", and RS R3 and R13 name DEL-01-01 as their source in this
undertaking; DEP-04-03-027). DEL-01-02's custody of in-flight requests is a
separate contribution (RECOVERY-v0.2 §3.5, §7).

**Carriers at 0.158.0 and what each does (v0.9; R17-8, R19-1, R19-7,
R19-8; OBS-2 O-4a, O-5, O-5b; OBS-3 W-1…W-6).** The source identity of
every record below is the one the composing owner supplies: the ROLE supply
record for role guidance (ROLE-v0.2 §6.1), the registered revision for a
workflow (WR-v0.2 §16.2, its `run_text` record).

| Carrier (supplier element) | Applied at 0.158.0? | Use in the App | What this boundary records |
|---|---|---|---|
| `developerInstructions` on `thread/start` | Yes (OBS-2 O-5: the thread's developer text reached every model request) | **Role guidance** (product guidance + the conversation's role), composed by DEL-02-04 (ROLE-v0.2 §5.1); fixed for the conversation's life (DECISION-L L-2) | Request identity, generation, element, content identity, source identity. Role-guidance supply evidence is recorded **at thread start only** |
| `baseInstructions` on thread start, resume or fork | — | **Never set** (R17-8; Codex's base instructions preserved) | A request carrying it is a finding, not supply |
| `developerInstructions` on `thread/resume` | **No**: accepted without error and silently ignored, for a loaded thread and for one the resume loads; nothing reports it (OBS-2 O-5) | **The App sends none** (ROLE-v0.2 §5.2, §5.5): relaunch keeps the start supply; changed role guidance reaches new conversations only (R19-3; ROLE-v0.2 §4.4) | If one is ever sent, it is recorded as *supplied, not applied at 0.158.0* |
| `developerInstructions` and `config.developer_instructions` on `thread/fork` | **No**: accepted and ignored; the fork keeps the source's developer text and history and gets a new thread identity with `forkedFromId` (OBS-3 W-6, W-6b) | **The App sends none.** A fork is a same-role copy only, recorded by DEL-02-04 as `inherited` from its source (ROLE-v0.2 F-1); "Continue as ‹role›" is a new conversation with its own `thread/start` guidance and a handoff summary the source conversation's agent drafts in a visible turn and the person edits before sending (R19-8, R20-6); this boundary carries those turns as ordinary turns | The `thread/fork` request record; no guidance element carried |
| A **text element of the `turn/start` that starts a workflow run** | Yes: the bytes reached the model as the user's text, and Codex's history returns them (observed through `thread/read` at 0.158.0, OBS-3 W-4; `thread/items/list` returns the same `ThreadItem`, observed-in-generated-types, WR-v0.2 U-WR-14) | **Workflow supply per run** (R19-1, R19-7): the registered revision's exact bytes framed by App-written lines naming the workflow and revision and, when chaining, saying the previous run ended (framing WR-FRAME-1, PROPOSED in WR-v0.2 §16.2; R19-2). When a run ends and no run starts with the next turn, that turn is prefixed with one App-written line saying the run ended (R20-3; worded by DEL-02-02, WR-v0.2 §16.2 TX-5) | The `turn/start` request record with the content identity of that text element and the source identity DEL-02-02 supplies. The App's per-run supply evidence (bytes and content identity, checked against Codex's history: `thread/items/list`, §4.4 "Recovery reads", WR-v0.2 §16.6 SC-3; R21-4) is the composing owner's, through the generic request path (R19-7; WR-v0.2 §16.6 `supply_check`; RS R3) |
| `turn/start` input `{type: "skill", name, path}` | Only for a `SKILL.md` of a discovered skill at its canonical path (then injected as a separate user message); otherwise accepted and silently ignored, with no error (OBS-3 W-1) | **Not used** for workflows (R19-7: a recorded alternative); the App places no workflow in any discovered skill root | If sent, recorded; a silently ignored input is never shown as supply |
| `turn/start` input `{type: "mention", …}` | No content reached the model for a file or a skill (OBS-3 W-3) | Not used | — |
| experimental `collaborationMode.settings.developer_instructions` on `turn/start` or `thread/settings/update` | Yes, **added**: a developer message is appended at each change and every earlier one stays in history; it persists across turns and a supplier restart; in plan mode a non-null value replaces the mode's built-in text (OBS-2 O-5b; OBS-3 W-5) | Not used for workflows or role supply (R19-7; ROLE-v0.2 §5.2). Plan mode is composed by DEL-01-04 with a null value (R18-1 C-06; NPTD-v0.2 §5.4) | Any non-null value is recorded as a guidance input with its content identity |
| thread `config` keys `agents.<ROLE>.description`, `agents.<ROLE>.config_file` | Yes for a delegated child, *observed through the OBS-2 adapter, not stock behaviour* (R18-9), with the `agents.*` keys in the home's `config.toml`: the role is offered as `agent_type`, recorded as `agentRole`, and the role file's `developer_instructions` **replace** the parent's for that child (OBS-2 O-4a). Under K-1 that file is the person's and is never written by role supply, so the App's carrier (per-thread `config` on `thread/start`, or `-c` session flags) is **not observed** (ROLE-v0.2 CR-1a, U-R3) | Additive child roles only, composed as product guidance + that role (R18-4; ROLE-v0.2 §5.3) | The carried `agents.*` entries and the content identity of each role file the App supplies |
| thread `config` keys `instructions`, `developer_instructions` | Not observed on `thread/start` (on `thread/fork`, ignored: OBS-3 W-6b) | Never (ROLE-v0.2 §5.2: one carrier only) | — |

**Per-thread `config` from role supply (v0.9; ROLE-v0.2 §5.2, §5.3; K-10;
H9).** The only configuration the App supplies for roles is the additive
`agents.<ROLE>.description` and `agents.<ROLE>.config_file`, and only for
role names the person's own configuration does not define. Its carrier
(per-thread `config` on `thread/start`, or `-c` session flags) is not yet
observed to be honoured; OBS-2 O-4a saw the keys honoured only from the
home's `config.toml`, which under K-1 is the person's file and is never
written for this (ROLE-v0.2 CR-1a, U-R3). It never sends
`features.*`, `agents.enabled`, `agents.max_depth`, or approval or sandbox
keys: the person's Codex configuration is not overridden (Root `AGENTS.md`;
K-10 "stated, not enforced"). A child spawned without an `agent_type` is not
observed; its guidance is stated as unknown, not as inherited (R18-4).

`instructionSources` on the thread-start response reports the instruction
files Codex itself found (with R18-6 these may include the person's global
`AGENTS.md` through the link); it is recorded as Codex reports it
(ROLE-v0.2 §4.3). At OBS-2 and OBS-3 every value was `[]` (no `AGENTS.md`
in the scratch working folders).

**Named limitation (P-15).** This evidence establishes that the input was
*supplied*. Whether the supplier *adopted* it is separate evidence and is
not implied. At 0.158.0 P-15's open half is now observed: resume and fork
overrides are ignored (OBS-2 O-5; OBS-3 W-6), as v3 observed of resume at
0.154. Launch configuration identity (§7.1) is not a substitute: it is per
child start, not per thread/turn.

### 8.3 Observed model destination (R4-1, R5-4; owner decision D5)

**CC-H thread-start disclosure.** Model contact can precede a turn: CI-8
records an observation at 0.158.0 of Responses websocket prewarm on
`thread/start` with Codex's default provider and no credentials (401).
ACCESS §9 displays this as `phase: thread-start`, `purpose: model`; it is
not a turn or evidence of prompt content. Requested and supplier-reported
thread destinations remain distinct. The boundary adds no destination veto,
provider override, approval/sandbox mandate or default.

Attribution (R5-4; V3-B m-1):

- **SETTLED by DECISION-2 (D5):** host content read through the external
  channel may flow to whatever model the person selected for the App
  conversation, cloud included; there is no gate on the destination.
- **SETTLED (the owner confirmed this reading of DECISION-2: SCA-V4-001
  OWNER_ITEMS O-10, accepted "as recommended", DECISION-7; R9-4; labelled
  INTEGRATION up to v0.6, R5-4):** the App **records** the model
  destination (DEL-04-03 RS R5) and **shows** it in the channel status
  (DEL-03-03), as information only.

This boundary supplies the facts **per turn** where the supplier reports
them, with thread, generation and receipt position, keeping requested and
effective values separate (R5-4):

- the provider and model the App **requested** (carried from the person's
  choice through DEL-01-05; at 0.158.0 `modelProvider` and model on thread
  start/resume, and a per-turn `model` on turn start — stable,
  `observed-in-generated-types`; no per-turn provider element);
- the provider and model the supplier **reports as effective** (at 0.158.0
  the thread start/resume responses carry `model` and `modelProvider`,
  `observed-in-generated-types`);
- any supplier **re-route** (at 0.158.0 the stable notification
  `model/rerouted` {thread, turn, from-model, to-model, reason},
  `observed-in-generated-types`; provider-model fallback is an
  experimental-only thread-start element, not requested by this boundary).

A turn for which no supplier report was observed carries destination
**unknown**; the boundary never fills it from an earlier turn. The
run-level value (the set of destinations observed) and the rule that a
switch starts no new run are DEL-04-03's (R5-4); this boundary supplies only
per-turn facts. At 0.158.0 the turn object itself carries no model element,
so a per-turn *effective* value is observed only through the thread-level
report plus any re-route (not observed live, U-19).

**Per-turn reading (PROPOSED, v0.8; U-27; exercised by VC-26 against the
double).** A turn's *effective* value is recorded only from a supplier
report that names that turn (at 0.158.0, a `model/rerouted` notification
with its turn identity). The thread-level report of thread start or resume
is recorded at thread scope, beside the turns, and is not copied into any
turn. A turn with no report naming it carries *unknown*, even when an
earlier turn or the thread has a value. Whether DEL-04-03 derives a turn's
destination from the thread-level report is DEL-04-03's (RS R5).

The destination **class** (local or cloud) is derived from the provider
configuration the person chose (DEL-01-05), not inferred by this boundary.
From v0.9 DEL-01-05 derives it from the kind of access entry the
conversation uses (ACCESS-v0.2 §2): `chatgpt-account` and `api-key` →
`user-chosen cloud`; `local-provider` → `local model server` (RS R5 values
unchanged).
Whether requested and effective values can differ in practice is not
observed (U-19). OBS-1 and OBS-1b observed them equal at thread start, no
`model/rerouted`, and no model element on the turn (§10.1 OB-7; F-23). D5 concerns host content reaching the conversation's model;
it does not address the supplier's own start-up traffic (L-4, U-18).

### 8.4 Harness-capability account at 0.158.0 (PROPOSED, v0.8; DEP-02-01-025, arc N-16; F-27)

This account gives the capability *meaning* DEL-02-01's register row
DEP-02-01-025 asks this deliverable to supply: every surface of the pin's
generated protocol output placed in one capability group, with what the
group lets the agent's harness do, the signals the generated types show for
its availability, and each member's standing. It is built from the
committed JSON Schema bundles (`generated/0.158.0/json-schema/experimental/`),
`_spike/inventory.txt` for the stable and experimental variants, the TS
output for the five TS-only names (SPIKE §4) and the running server's own
list of accepted client methods (its recorded -32600 message, SPIKE §5).

- **Names.** The group labels HCG-A01…A17 and HCG-B01…B10 are this file's
  grouping labels. They are not portable capability names: those are
  DEL-02-01's (WD U-08). A portable name can resolve to one or more groups at
  a named pin; at 0.158.0 each of WD's ten names resolves to exactly one
  Part A group, as WD §4.2.5's group column and HC-7 state (R14-5). At
  another pin the §9.5 upgrade comparison re-checks the account and that
  mapping.
- **Part A** holds the agent's capabilities: what the harness can do inside a
  turn, visible as supplier item kinds or server requests. **Part B** holds
  the hosting and management surfaces the App drives. A harness-capability
  requirement in a workflow (WD §4.2) refers to Part A.
- **Standing labels** (the spike's, SPIKE §6): every member is
  `observed-in-generated-types` unless marked **(obs)**, `observed` live in
  the spike. The names of all 170 client methods were also *accepted* by the
  running server (they are the list its -32600 message gave; SPIKE §5): that
  name acceptance is `observed`, their behaviour is not. The CLI's local
  provider flags (`--oss`, `--local-provider`) are `published-only` and are
  not App Server surfaces. Nothing here is qualified (DEP-005).
- **Variant marks:** none = in the stable and the experimental output of both
  generators; **(exp)** = experimental-only (present only with the
  `--experimental` variant, usable only with the experimental opt-in, F-13);
  **(TS)** = in the TS output only (U-15). All 19 item kinds are stable and
  their elements are the same in both variants.
- **Counts, each member in exactly one group:** 19 item kinds, 11
  server-request kinds, 170 client methods, 85 notifications. The one client
  notification, `initialized` **(obs)**, belongs to HCG-B01. Checked by the
  prototype (VC-30).

**Part A — agent capabilities**

| Group | Supplier item kinds | Server-request kinds | Client methods | Notifications |
|---|---|---|---|---|
| **HCG-A01** Messages and reasoning | `userMessage`, `agentMessage`, `reasoning` | — | — | `item/agentMessage/delta`, `item/reasoning/summaryTextDelta`, `item/reasoning/summaryPartAdded`, `item/reasoning/textDelta` |
| **HCG-A02** Shell command execution | `commandExecution` | `item/commandExecution/requestApproval`, `execCommandApproval` | `thread/shellCommand`, `thread/backgroundTerminals/clean` (exp), `thread/backgroundTerminals/list` (exp), `thread/backgroundTerminals/terminate` (exp) | `item/commandExecution/outputDelta`, `item/commandExecution/terminalInteraction` |
| **HCG-A03** File changes | `fileChange` | `item/fileChange/requestApproval`, `applyPatchApproval` | — | `turn/diff/updated`, `item/fileChange/outputDelta`, `item/fileChange/patchUpdated` |
| **HCG-A04** Permission requests and review routing (A14 subjects) | — | `item/permissions/requestApproval` | `thread/approveGuardianDeniedAction`, `permissionProfile/list` | `item/autoApprovalReview/started`, `item/autoApprovalReview/completed`, `autoApprovalReview/strictReviewRequired`, `guardianWarning` |
| **HCG-A05** MCP server tools and resources | `mcpToolCall` | — | `mcpServer/oauth/login`, `config/mcpServer/reload`, `mcpServerStatus/list`, `mcpServer/resource/read`, `mcpServer/event/stream/start` (exp), `mcpServer/event/stream/stop` (exp), `mcpServer/tool/call` | `item/mcpToolCall/progress`, `mcpServer/oauthLogin/completed`, `mcpServer/startupStatus/updated`, `mcpServer/event/stream/notification` |
| **HCG-A06** App-offered (dynamic) tools | `dynamicToolCall`, `functionCallOutput` | `item/tool/call` | — | — |
| **HCG-A07** Input from the person to the agent | — | `item/tool/requestUserInput`, `mcpServer/elicitation/request` | `thread/increment_elicitation` (exp), `thread/decrement_elicitation` (exp) | — |
| **HCG-A08** Native delegation (sub-agents) | `collabAgentToolCall`, `subAgentActivity` | — | — | — |
| **HCG-A09** Planning | `plan` | — | `collaborationMode/list` (exp) | `turn/plan/updated`, `item/plan/delta` |
| **HCG-A10** Web search | `webSearch` | — | — | — |
| **HCG-A11** Images | `imageView`, `imageGeneration` | — | — | — |
| **HCG-A12** Review mode | `enteredReviewMode`, `exitedReviewMode` | — | `review/start` | — |
| **HCG-A13** Context compaction | `contextCompaction` | — | `rollout/compress` (exp), `thread/compact/start` | `thread/compacted` |
| **HCG-A14** Time: waiting and clock | `sleep` | `currentTime/read` (exp) | — | — |
| **HCG-A15** Hooks | `hookPrompt` | — | `hooks/list` | `hook/started`, `hook/completed` |
| **HCG-A16** Memory | — | — | `thread/memoryMode/set` (exp), `memory/status` (exp), `memory/reset` (exp) | — |
| **HCG-A17** Realtime voice | — | — | `thread/realtime/start` (exp), `thread/realtime/appendAudio` (exp), `thread/realtime/appendText` (exp), `thread/realtime/appendSpeech` (exp), `thread/realtime/stop` (exp), `thread/realtime/listVoices` (exp) | `thread/realtime/started`, `thread/realtime/itemAdded`, `thread/realtime/item/started`, `thread/realtime/item/transcript/delta`, `thread/realtime/item/completed`, `thread/realtime/transcript/delta`, `thread/realtime/transcript/done`, `thread/realtime/outputAudio/delta`, `thread/realtime/sdp`, `thread/realtime/error`, `thread/realtime/closed` |

**Meaning and availability signals of the Part A groups** (supplier terms;
availability signals are elements of the generated types, not observed
behaviour):

| Group | What the harness does | Availability signals in the generated types |
|---|---|---|
| HCG-A01 | Receives the person's messages; produces the agent's messages and reasoning | Always present in a turn. `agentMessage` carries an optional `phase` (commentary or final answer) |
| HCG-A02 | Runs shell commands in the thread's working directory, under the person's sandbox and approval settings (H9, D3); a command may raise an A14 request. The client method `thread/shellCommand` in this group is the App's own call (its items carry source `userShell`; the generated description says it runs unsandboxed), never the agent's action | Approval policy and sandbox on thread and turn start (the person's own setting). Whether the legacy `execCommandApproval` is raised on the v2 surface: not observed (§6.1). **Observed once (OBS-1b; §10.1 OB-2, OB-3):** a model-issued command item with source `agent` at start and `unifiedExecStartup` at completion, shell-wrapped, after one `item/commandExecution/requestApproval` |
| HCG-A03 | Writes files by patches; a change may raise an A14 request | As HCG-A02 |
| HCG-A04 | Asks for further permissions; the supplier's own reviewer may decide (§6.6) | `approvalsReviewer` on thread and turn start |
| HCG-A05 | Calls tools and reads resources of MCP servers configured for the thread. The client methods in this group (`mcpServer/tool/call`, `mcpServer/resource/read` and the configuration methods) are App-origin calls (§6.8) | `mcpServerStatus/list`: servers, tools, runtime status (§6.8; ADAPTER §3.5). Added at the RP-3 repair (R13-6): `modelProvider/capabilities/read` → `namespaceTools`, which, on the evidence of OBS-1, bears on whether the provider can receive MCP tools at all, since Codex 0.158.0 offered them to a Responses provider as a `namespace` tool (inference from the record, not a stated meaning of the element). **Observed limit of one route (§10.1 OB-1):** on LM Studio 0.4.16 through the Responses interface no MCP tool reached the model |
| HCG-A06 | Calls tools the App registers on the thread; the App answers `item/tool/call`. `functionCallOutput` is the output item of such a call (name, namespace, output), not a capability of its own | `dynamicTools` on thread start (experimental-only); `modelProvider/capabilities/read` → `namespaceTools` (see HCG-A05). None is registered in this increment (§6.1) |
| HCG-A07 | Asks the person a question, or relays an MCP server's elicitation (its prompt is authored by an MCP server or the agent, §6.1); the answer goes to the agent and is never act evidence (R9) | Not stated in the generated types. The tool `request_user_input` was offered to the model in both OBS-1 runs and not used (§10.1) |
| HCG-A08 | Starts and messages sub-agent threads (native delegation) | **v0.9 (R18-1 C-04, C-05; replaces v0.8's `multiAgentMode` signal, which the 0.158.0 types mark "@deprecated Ignored"):** delegation is available when `Model.multiAgentVersion` (on `model/list`; `disabled`, `v1`, `v2`) is not `disabled` **and** the provider accepts `namespace` tools (`modelProvider/capabilities/read` → `namespaceTools`, as HCG-A05); an effective `features.multi_agent = false`, when `config/read` shows it, reads missing (`config/read` shows no `features` unless set); a signal that cannot be read leaves availability *not established* (NPTD-v0.2 §7.1). Receivers read the three signals in R21-1's order: `disabled` → missing; `features.multi_agent = false` → missing; `namespaceTools` false → missing; any of the three not read → not established; otherwise present (NPTD-v0.2 §7.1, the reference; EXEC-v0.7 EV-3a; WD-v0.9 §4.2.5). Read at run time (R19-5). Delegation is a **stable** surface: its items are stable and the gating feature `multi_agent` is stable and on by default at 0.158.0 (OBS-2 O-4, O-8), so it carries no "experimental" label; only plan mode does (C-05). *Observed through the OBS-2 adapter, not stock behaviour (R18-9):* `collabAgentToolCall` items `spawnAgent`, `sendInput`, `wait` with `receiverThreadIds` and `agentsStates`; child notifications on the same connection with the child's thread identity and **no `thread/started`**; the child readable by `thread/read` with `parentThreadId`, `agentRole`, `agentNickname`; children absent from `thread/list`, present in `thread/loaded/list`. So receivers recognize a child from the parent's completed `spawnAgent` `receiverThreadIds`, never from `thread/started` or `thread/list` (RECOVERY-v0.2 F-R10; NPTD-v0.2 §7.4; ROLE-v0.2 CR-5). With `multi_agent_v2` the tool namespace is `collaboration` with a different tool set (OBS-2 §6.1). On LM Studio 0.4.16 delegation never reaches the model (§8.1 L-3) |
| HCG-A09 | Keeps and updates a plan; plan mode is a collaboration mode | Plan item and plan notifications stable; plan mode through `collaborationMode` on turn start (experimental-only; S-F-13). *Observed at OBS-2 (0.158.0, O-8):* one `plan` item via `item/plan/delta`, no `turn/plan/updated`, no `update_plan` tool; plan mode persists on later turns until the default mode is sent explicitly (DEL-01-04 composes it, R18-1 C-06) |
| HCG-A10 | Searches the web | `modelProvider/capabilities/read` → `webSearch`; web-search mode `disabled`, `cached`, `indexed` or `live` in configuration |
| HCG-A11 | Views local images; generates images | `modelProvider/capabilities/read` → `imageGeneration` |
| HCG-A12 | Reviews changes in a review mode | `review/start` |
| HCG-A13 | Compacts the conversation context | `thread/compact/start`; an automatic compaction token limit in configuration |
| HCG-A14 | Waits (sleep tool); asks the App for the current time | `currentTime/read` only with the experimental opt-in (§6.1) |
| HCG-A15 | Runs configured hooks, which may add prompt fragments | `hooks/list` |
| HCG-A16 | Keeps memories across threads | `thread/memoryMode/set`, `memory/status` (experimental-only) |
| HCG-A17 | Holds a realtime voice conversation | Experimental-only methods |

**Goals (v0.9; R18-7 G-3; NPTD-v0.2 §6.4).** Every tool list captured at
OBS-2 (0.158.0) offered the model three goal tools, `get_goal`,
`create_goal` and `update_goal`, and a resume produced the notification
`thread/goal/cleared`. The tools are model-facing tools inside a turn, not
App Server surfaces; no item kind exists for them at 0.158.0, and whether a
goal tool call yields an item is not observed (NPTD-v0.2 U-P9). They are
placed with the thread-goal surface already in HCG-B04 (`thread/goal/set`,
`get`, `clear`; `thread/goal/updated`, `thread/goal/cleared`), which is the
App's own access to the same goal; no Part A group is added, so the counts
above and the group set WD-v0.8 §4.2.5 resolves against are unchanged. A
Codex goal status is never a run end, checkpoint or act (NPTD-v0.2 §6.4;
§9 TA-5). DEL-01-03 shows the goal line as a native group without translation;
this boundary delivers it natively (H6).

**Client methods in Part A.** A client method listed in a Part A group
(for example `thread/shellCommand`, `mcpServer/tool/call`, `review/start`,
`thread/compact/start`) is a call the App makes into that capability: it is
App-origin, its initiator is recorded (§5), and it does not by itself show
what the agent's harness can do. It is grouped by the capability it touches.

**Members WD reads differently (R14-5; V18-2 M-1, m-10; F-27 closed).** This
file owns the supplier facts and the grouping, and WD-v0.8 §4.2.5 follows it
(HC-6, HC-7). The three members V18-2 found read differently stay where they
are: `functionCallOutput` in HCG-A06, reached by WD's `dynamic-tool-call`;
`mcpServer/elicitation/request` in HCG-A07, reached by `person-input-request`;
`thread/shellCommand` in HCG-A02 as an App-origin client method, reached by
`shell-command` only as a member of the group. None makes a WD name mean
something its group does not offer, so nothing is returned. Which of a
group's signals and observations bear on a name's presence is DEL-02-03's
rule (EXEC EV-3, R14-5).

**Part B — hosting and management surfaces**

| Group | Supplier item kinds | Server-request kinds | Client methods | Notifications |
|---|---|---|---|---|
| **HCG-B01** Handshake, diagnostics and supplier messages | — | — | `initialize` (obs), `server/diagnostics` (exp), `mock/experimentalMethod` (exp), `feedback/upload` | `error`, `warning`, `deprecationNotice`, `configWarning` |
| **HCG-B02** Thread lifecycle and history | — | — | `thread/start`, `thread/resume`, `thread/fork`, `thread/archive`, `thread/delete`, `thread/unsubscribe`, `thread/unarchive`, `thread/revert`, `thread/list`, `thread/search` (exp), `thread/searchOccurrences` (exp), `thread/loaded/list`, `thread/read`, `thread/turns/list`, `thread/items/list`, `thread/inject_items`, `thread/timeline/list` (exp), `getConversationSummary` (TS) | `thread/started`, `thread/status/changed`, `thread/archived`, `thread/deleted`, `thread/unarchived`, `thread/closed`, `thread/reverted` |
| **HCG-B03** Turn control and item lifecycle | — | — | `turn/start`, `turn/settings/update` (exp), `turn/steer`, `turn/interrupt` | `thread/tokenUsage/updated`, `turn/started`, `turn/completed`, `item/started`, `item/completed`, `serverRequest/resolved`, `turn/moderationMetadata`, `rawResponse/completed` (TS), `rawResponseItem/completed` (TS) |
| **HCG-B04** Thread organisation (names, goals, queue, attachments, projects, sections) | — | — | `thread/name/set`, `thread/goal/set`, `thread/goal/get`, `thread/goal/clear`, `thread/queue/add` (exp), `thread/queue/list` (exp), `thread/queue/update` (exp), `thread/queue/delete` (exp), `thread/queue/reorder` (exp), `thread/queue/start` (exp), `thread/metadata/update`, `thread/attachment/add`, `thread/attachment/list`, `thread/attachment/remove`, `thread/section/move`, `project/list` (exp), `project/read` (exp), `project/create` (exp), `project/import` (exp), `project/update` (exp), `project/move` (exp), `project/delete` (exp), `threadSection/list`, `threadSection/create`, `threadSection/update`, `threadSection/delete` | `thread/name/updated`, `thread/attachment/updated`, `thread/goal/updated`, `thread/goal/cleared`, `thread/queue/changed`, `project/changed`, `thread/project/updated` |
| **HCG-B05** Models and providers | — | — | `model/list`, `modelProvider/capabilities/read` | `model/rerouted`, `model/verification`, `modelProvider/authRecoveryStarted`, `modelProvider/authRecoveryCompleted`, `model/safetyBuffering/updated` |
| **HCG-B06** Accounts, sign-in and usage | — | `account/chatgptAuthTokens/refresh`, `attestation/generate` | `userVerification/status` (exp), `userVerification/enroll` (exp), `userVerification/delete` (exp), `userVerification/verify` (exp), `userVerification/cancel` (exp), `account/gatewayOAuth/read`, `account/gatewayOAuth/login`, `account/gatewayOAuth/cancel`, `account/login/start`, `account/bedrock/discover` (exp), `account/bedrock/setup` (exp), `account/login/cancel`, `account/logout`, `account/rateLimits/read`, `account/rateLimitResetCredit/consume`, `account/usage/read`, `account/workspaceMessages/read`, `account/sendAddCreditsNudgeEmail`, `account/read`, `getAuthStatus` (TS) | `account/updated`, `account/gatewayOAuth/changed`, `account/rateLimits/updated`, `account/login/completed` |
| **HCG-B07** Configuration, settings and sandbox setup | — | — | `thread/settings/update` (exp), `experimentalFeature/list`, `experimentalFeature/enablement/set`, `windowsSandbox/setupStart`, `windowsSandbox/readiness`, `config/read`, `externalAgentConfig/detect`, `externalAgentConfig/import`, `externalAgentConfig/import/recordHistory`, `externalAgentConfig/import/readHistories`, `config/value/write`, `config/batchWrite`, `configRequirements/read` | `thread/settings/updated`, `externalAgentConfig/import/progress`, `externalAgentConfig/import/completed`, `windows/worldWritableWarning`, `windowsSandbox/setupCompleted` |
| **HCG-B08** App-side file, process and search access (the App as caller) | — | — | `fs/readFile`, `fs/writeFile`, `fs/createDirectory`, `fs/getMetadata`, `fs/readDirectory`, `fs/remove`, `fs/copy`, `fs/watch`, `fs/unwatch`, `command/exec`, `command/exec/write`, `command/exec/terminate`, `command/exec/resize`, `process/spawn` (exp), `process/writeStdin` (exp), `process/kill` (exp), `process/resizePty` (exp), `gitDiffToRemote` (TS), `fuzzyFileSearch`, `fuzzyFileSearch/sessionStart` (exp), `fuzzyFileSearch/sessionUpdate` (exp), `fuzzyFileSearch/sessionStop` (exp) | `command/exec/outputDelta`, `process/outputDelta`, `process/exited`, `fs/changed`, `fuzzyFileSearch/sessionUpdated`, `fuzzyFileSearch/sessionCompleted` |
| **HCG-B09** Extensions: skills, plugins, marketplaces, apps | — | — | `skills/list`, `skills/extraRoots/set`, `marketplace/add`, `marketplace/remove`, `marketplace/upgrade`, `plugin/list`, `plugin/search` (exp), `plugin/installed`, `plugin/reconcile`, `plugin/read`, `plugin/skill/read`, `plugin/share/save`, `plugin/share/updateTargets`, `plugin/share/list`, `plugin/share/checkout`, `plugin/share/delete`, `app/read`, `app/list`, `app/installed`, `skills/config/write`, `plugin/install`, `plugin/uninstall` | `skills/changed`, `app/list/updated` |
| **HCG-B10** Remote control and environments | — | — | `remoteControl/enable` (exp), `remoteControl/disable` (exp), `remoteControl/status/read` (exp), `remoteControl/pairing/start` (exp), `remoteControl/pairing/status` (exp), `remoteControl/client/list` (exp), `remoteControl/client/revoke` (exp), `environment/add` (exp), `environment/info` (exp), `environment/status` (exp) | `thread/environment/connected`, `thread/environment/disconnected`, `remoteControl/status/changed` (obs) |

Where the App uses Part B surfaces, their treatment is this file's:
handshake and diagnostics §4.2, §5; threads and turns through the generic
request path §5.1 (with guidance evidence §8.2 and destination facts §8.3);
models and providers §8.1, §8.3; accounts and configuration are DEL-01-05's
(S-4; §6.8 for MCP configuration, which is person-directed only); the App-side
file, process and search access of HCG-B08 is App-origin and never the
agent's action (the initiator is recorded, §5).

## 9. Recorded-exchange fixture method (M-7, V4-EXM-02, REQ-006)

### 9.1 Capture

A recording tap at the main-process stdio boundary records, for one
controlled scenario on an identified candidate:

- each frame in both directions, unchanged, with direction, generation,
  receipt/send position and a relative time offset;
- capture metadata: version identity record (§7.1), declared capabilities,
  App candidate identity, scenario name, provider kind, the tool-permission
  and sandbox settings actually in effect (the user's own, H9), date
  (V4-EXM-01);
- a redaction record. Categories: credentials, tokens, account identifiers,
  personal paths **and, from the 0.158.0 stream, the host name
  (`serverName`), installation identifier, absolute home path and the
  client's own identity text inside `userAgent`** where it identifies a
  person or machine (S-F-15). **From v0.9 (ACCESS-v0.2 §7 CR-2, CR-4;
  NIR-v0.2 §4.5 SE-3; OBS-2 §11; OBS-3 §9; all at 0.158.0):** the
  `account/login/start` parameters `apiKey`, `accessToken`,
  `secretAccessKey`, `sessionToken` and the response elements `authUrl`,
  `verificationUrl`, `userCode` are replaced by a redaction marker before
  anything is written; supplier error texts from account methods are
  redacted as text; the `account/read` `email` is an identity category;
  answer values to questions marked `isSecret` are never kept (§6.1);
  every model request carries the installation identifier and the thread,
  session and turn identifiers to the provider (`client_metadata`, and
  the `x-codex-turn-metadata` header at OBS-3), and the host's time zone is
  in every model input (`<environment_context>`), so a captured provider
  exchange carries these categories too; a skill injected by Codex carries
  the skill file's absolute path to the model (OBS-3 W-1). A redacted
  fixture never claims byte identity with the original exchange;
- invented engineering material only (V4-CST-06); fixture subjects labeled.

Live capture runs are few and deliberate; each needs the owner's credential
or a local provider, and is itself recorded. A capture on a fresh home causes
the L-4 network fetch; record it.

### 9.2 Fixture standing labels

`recorded`, `recorded-truncated`, `mutated`, `constructed`. The W11 spike
transcripts (`_spike/transcripts/`, 8, redacted) are `recorded` spike
recordings of verify-less start/handshake/stop; they are **not** X-01
fixtures (no App candidate, no §7.2 step) but may seed a supplier double.

### 9.3 Replay and comparison

- **Supplier-double replay** exercises the App seam against recorded
  supplier→App frames, comparing App→supplier frames semantically
  (identities correlated by position; declared volatile elements — times
  including `emittedAtMs`, generated identities — excluded from equality but
  preserved in delivery).
- **Schema conformance**: every recorded frame is validated against the
  **chosen reference output** (U-15) plus supplement of its pin; frames valid
  only under the other generator's output are reported as generator
  divergence, not as failures.
- **Outcome labels** per case: `pass`, `fail`, `blocked`, `not-run`,
  `inconclusive`, bound to candidate + pin (V4-EXM-03).

### 9.4 Seam regression set (designed)

| ID | Scenario | Fixture standing | Runnable at 0.158.0 without credentials? |
|---|---|---|---|
| X-01 | Verify → spawn → handshake → `ready` (incl. pre-`initialized` notification) | recorded | Yes, once an App candidate exists (spike SV-04 shows the supplier side) |
| X-02 | Conversation start with a selected provider; one turn | recorded | No (credential or local provider) |
| X-03 | Plan created, then revised in a later turn | recorded | No |
| X-04 | Tool-permission request (A14) answered affirmatively by the person | recorded | No |
| X-05 | Same kind explicitly declined | recorded | No |
| X-06 | User-input / elicitation request answered | recorded | No |
| X-07 | Unfamiliar server request (incl. `currentTime/read` without opt-in) | mutated | Yes, with a double seeded from spike transcripts |
| X-08 | Malformed and oversize frames; frames without the version member | constructed | Yes, with a double |
| X-09 | Child killed with one outstanding request and one un-responded client request | recorded-truncated | No (needs a live turn) |
| X-10 | Restart after X-09; recovery read of actual state | recorded | No |
| X-11 | Version label matches, content identity differs | constructed | Yes |
| X-12 | Answer for a closed generation; second answer; App-rule affirmative refused | constructed | Yes, with a double |
| X-13 | Fresh-home start and deliberate stop with supplier descendants alive | recorded | Yes, but causes the L-4 network fetch (owner visibility) |
| X-14 | Supplier-internal decision (`auto_review`) and `serverRequest/resolved` | recorded | No |

### 9.5 Deliberate-upgrade comparison procedure (SOW-100, REQ-006, VER-006)

1. Name the current qualified pin *p* (none yet; 0.158.0 is the
   definition/generation pin) and the candidate *p′*; nothing is adopted by
   running this procedure.
2. Obtain *p′* from its published distribution; record its version identity
   (§7.1), including the distribution tree and launcher.
3. Generate **both generator kinds in both variants** at *p′*; record
   identities and a manifest; confirm determinism by generating twice.
4. Structural diff *p* → *p′* per kind and variant: methods, server-request
   kinds, notifications, fields; experimental status by variant diff; the
   generator-divergence set; the server's own accepted-method list (from its
   unknown-method error). Mark each change against the §8 seams as
   `consumed` / `not consumed`.
5. Re-examine the supplement: entries now generated → remove; entries whose
   element vanished or changed → incompatibility.
6. Validate *p* recordings against *p′* reference output; record expected
   and unexpected conformance failures.
7. Capture the §9.4 set at *p′* (live runs limited to those needed).
8. Semantic diff of *p* vs *p′* recordings; run App seam replay on *p′*.
9. Run the selected-version check (§7.2) on the candidate.
10. Record *p*, *p′*, candidate, every result and every unresolved
    incompatibility. The App implementation owner decides adoption; *p*
    stays in force until then.

**Version-advance check (v0.9; R19-5; PROPOSED as a later node, scheduling
open).** Before *p′* is used even for definition, steps 3–4 and 6 are run,
the local observation harnesses (`prototype/obs1/`, `obs2/`, `obs3/`) are
rerun at *p′* within the limits their briefs set, and every statement of
this file and its receivers that names *p* as its version is listed as
affected. Runtime reads (the version rule, header) are re-checked rather
than carried forward.

### 9.6 Supplier double, boundary model and schemas (PROPOSED, v0.8; R12-1…R12-3)

**What exists.** `Design/prototype/` holds a local prototype, run with the
Python 3 standard library only, no package installed and no network. It is
not product code, not an App candidate and not the §12 O-1 proposal
realized (its README says so). It has three parts:

- **Supplier double** (`supplier_double.py`, `double_scenarios.py`). A child
  process that speaks newline-delimited JSON on its standard input and
  output as the supplier did in the spike. It replays the supplier frames of
  the eight committed, redacted spike transcripts (fixture standing
  `recorded`, §9.2): the initialize response and the notification sent
  before `initialized`, the -32600 unknown-method error with its list of 170
  accepted methods, the "Already initialized" error, no reply to an unknown
  notification, exit code 0 at end of input and on a termination signal. A
  recorded frame whose identity or method name must change is labelled
  `mutated`. Everything a scenario adds (server requests, items, malformed
  lines, exits) is labelled `constructed`; every constructed or mutated
  frame is checked against the committed bundle.
- **Boundary model** (`boundary_model.py`). An executable model of this
  file's rules (H1–H11, §4, §5, §6 with R1–R9, §8.3) that drives the double
  as the App side would. Numbers the file leaves open (U-05 bound and
  delays, grace period, wait limit, frame-size limit, the App's error code
  for unfamiliar requests) are marked TEST VALUE. A case that passes shows
  that the rules run end to end as written; it passes no VER criterion
  (§9.3 labels apply with the model as the "candidate").
- **Schemas and fixtures.** `hosting.lifecycle-event.schema.json`,
  `hosting.client-request-record.schema.json` and
  `hosting.server-request-entry.schema.json` (JSON Schema 2020-12, beside
  this file) turn the element meanings of §4.7 and §7.1, §5 and §6.1 into
  PROPOSED formats. Names are Chirality's own; supplier methods, identities
  and payloads are carried as data; no wire field is selected. Each has a
  valid and an invalid fixture in `prototype/fixtures/`; placement stays
  open (R12-2). `jsonschema_subset.py` validates the keyword subset the
  schemas and the generated bundles use (listed in its header).

**Run of 2026-09-30** (`python3 run_cases.py` in `Design/prototype/`;
output in `prototype/results/RUN_2026-09-30.txt`): every case and check gave
its expected result against the model (the count and each line are in the
results file and in the node's return). Cases run: VC-03, VC-04, VC-06,
VC-08 (X-01 side), VC-10 (constructed identity), VC-14 (X-12 part), VC-16,
VC-20, VC-21, VC-22, VC-23, VC-24, VC-25, VC-26 (constructed re-route),
VC-27…VC-30, the seed-fidelity checks (each of the eight transcripts
replayed byte for byte) and two deliberate-stop checks. Not run: VC-07
(needs the generators, that is, running the Codex binary), and every case
marked "No" (live turn, candidate or credential).

**Rerun at v0.9 (node F-A, 2026-10-02).** `PYTHONDONTWRITEBYTECODE=1
python3 run_cases.py` in `Design/prototype/` (Python 3.13.7, Darwin 25.6.0
arm64): **35 results, 35 pass (model), exit 0**, the same 35 cases as the
RP-3 run. VC-27 compares the §4.7 and §6.2.1 tables of this file with the
model (only guard text changed in RT-08 and RT-10, which the check does not
compare); VC-30 parses §8.4 (no member added or moved);
SCHEMA-records validates the 258 model records against the revised entry
schema. No prototype program file was changed; the output is quoted in the
node's return (`F/F-A.md`), not written into `results/`. The revised entry
schema (FH-17, FH-18) has three new fixtures beside the two the run uses:
`server-request-entry.secret-redacted.valid.json` (valid),
`server-request-entry.secret-kept.invalid.json` (invalid: missing
redaction) and `server-request-entry.actor-form.invalid.json` (invalid:
actor pattern), checked with `jsonschema_subset.py` by a scratch script; the
two original fixtures keep their results. DEL-01-04's prototype (read-only
run at this node) validated every register entry it produced against the
revised schema (its check R-16 passed).

**OBS-1 test doubles.** `obs1_mcp_double.py` (a minimal stdio MCP server
with one invented tool, logging receipt times) and `obs1_cli_tool.py` (a
command-line tool printing one invented JSON result) are the test tools of
the OBS-1 brief (`WAVE_B/OBS-1_BRIEF.md` in the run folder). The run above
checks them locally without Codex.

**Not claimed.** The double is not the supplier: every behaviour it shows
beyond the recorded frames is constructed from the generated types and
this file's assumptions. Whether the supplier behaves as the constructed
frames do is what OBS-1 and later captures observe.

## 10. Pin spike observations at 0.158.0 (W11) and what remains

Two vocabularies, both taken from the spike record (SPIKE §6; IR1C-20).
**Standing** at 0.158.0: `observed` (seen live), `observed-in-generated-types`,
`published-only`, `not-observed`. **Verdict vs v0.1**: **consistent**,
**refines** (v0.1 holds but needs a named element), **contradicts** (a v0.1
statement did not match the pin). Verdicts are the spike's own; none is
reclassified here.

| Item | Standing at 0.158.0 | Spike verdict vs v0.1 | Treatment in this file |
|---|---|---|---|
| P-01 Distribution identity | observed | **refines** §7.1 | Identity covers the executed vendor tree (S-F-02) → §7.1 |
| P-02 Standalone run | observed (partial); relocation not-observed | **refines** H1 | Launcher record (H1, §7.1); relocation → DEL-01-06 |
| P-03 Generation | observed (deterministic) | **refines** §7.1 | Generator kind + variant in identity (§7.1) |
| P-04 Inventory | observed / observed-in-generated-types | **contradicts** (single generated set) | Reference options §7.3 (U-15) |
| P-05 Handshake | observed | **contradicts** (handshake version identity); **refines** §4.1/§4.2 | No version element; consistency check only (§7.2); pre-`initialized` frames rule (H4) |
| P-06 Experimental opt-in | observed-in-generated-types; runtime gating not-observed | **consistent**; **refines** §7.3 | Supplement narrowed; status by variant diff; classification by declared capabilities (§6.1, §7.3) |
| P-07 Framing, stderr, input close, signals, opt-out facility | observed | **refines** §5; **contradicts** §4.3 (exit facts) and §4.5 ("terminate the child"); **consistent** H7/U-07 | §4.3–§4.5, H11 (S-F-06, S-F-07); §5, H6 (S-F-08) |
| P-08 Answer forms | observed-in-generated-types; error reply to a known kind and never-answered not-observed | **consistent** R8; **refines** R3/U-11 and origin set | R5 cites forms; `timed_out` under U-11; §6.6; live behavior U-19 |
| P-09 Supplier-reported resolution | observed-in-generated-types (`serverRequest/resolved`); semantics not-observed | **refines** §6.2, F-10, U-09 | Named candidate source (§6.2) |
| P-10 Plan items and revision | observed-in-generated-types; live not-observed | **refines** S-2 | Whole plan per update, no revision identity |
| P-11 Provider selection | observed-in-generated-types / published-only; L-2 not-observed | **consistent** (L-1; F-08 confirmed) | L-2 stays unobserved |
| P-12 Account methods | observed-in-generated-types; storage not-observed | **consistent** | S-4; feeds OI-009/OI-010 at DEL-01-05 |
| P-13 Thread resume/read/list; subagent items | observed-in-generated-types; post-restart not-observed | **consistent** | §4.3 step 4; DEL-01-02/01-03 inputs |
| P-14 Home reads/writes | observed | **refines** §7.2, U-03 | Probe side effect (S-F-17) |
| P-15 Additive instruction inputs | observed-in-generated-types; resume-override effect not-observed | **consistent** | §8.2 named limitation |
| L-4 | observed | **changes** the row from not-observed to observed (spike's wording) | §8.1; F-14; U-18 |

**Still to observe (next spike, App implementation owner; U-19):** whether
`initialized` is required and how a known method before initialize is
treated; runtime gating of experimental elements without the opt-in; the
supplier's handling of an error reply to a known request kind and of a
never-answered request; `serverRequest/resolved` triggers; supplier-internal
review decisions live; plan revision request live; post-restart thread
reads; resume-override adoption; per-conversation provider effect and L-2/L-3
with an identified local server; whether the plugin fetch (L-4) is
configurable; relocation of the vendor tree (DEL-01-06); outbound frames
without the version member; the live effect of `turn/interrupt` (HP-2; not
relied upon, and no receiver depends on it); whether an MCP tool call raises an A14 request
and by which kind; whether an App-initiated `mcpServer/tool/call` enters the
thread's items or model context; per-thread MCP configuration; whether
requested and effective model/provider can differ. Live items need the owner's credential or an
identified local provider. **v0.9:** OBS-2 and OBS-3 (§10.2, §10.3) observed
at one local pairing: the live effect of `turn/interrupt`; a before-reply
`serverRequest/resolved` (after an interrupt) and a never-answered request
across a stop; post-restart thread reads; resume-override adoption (ignored)
and fork-override adoption (ignored); the start-up traffic's
configurability; runtime gating of plan mode and of `remoteControl/status/read`
by the opt-in. U-19 lists what remains.

**v0.8: OBS-1.** The brief for one live turn at 0.158.0 against a local LM
Studio model (DECISION-K1 K1-6) is `WAVE_B/OBS-1_BRIEF.md` in run
`APP-V4-DESIGN-PASS-2-20260930`. It is written to observe, from the list
above: the order and content of items around a model-issued MCP tool call
and whether it raises an A14 request; the requested and effective model and
provider, and any re-route; the L-2 wire interface Codex uses against the
local server and L-3 tool calling; `serverRequest/resolved` if a request is
raised; optionally a command-line tool run and per-thread MCP configuration.
Relocation, post-restart reads, resume-override adoption and the plugin
fetch's configurability are not in it. OBS-1 ran, and OBS-1b ran the
command-line turn; their observations are §10.1. Of the list above, these
are now observed at one pair: L-2 and L-3 (partly), per-thread MCP
configuration, `serverRequest/resolved` after a written reply, and
requested against effective model and provider at thread start. Still to
observe: the rest of the list, including the MCP tool-call item order and
whether it raises an A14 request, which the local Responses route could not
show (OB-1).

### 10.1 OBS-1 and OBS-1b at 0.158.0 (dated observations; R13-6; RP-3 repair)

Record: `OBS_1_0.158.0.md` beside this file (OBS-1 §1–§11; the OBS-1b
addendum §B.1–§B.7), not edited here. **Standing:** observed on 2026-09-30
at one pair: the Codex 0.158.0 vendor binary (sha256 as SPIKE §3), LM Studio
0.4.16+2 on loopback, one local model (`qwen/qwen3.5-9b`), a custom provider
with `wire_api = "responses"`, the approval and sandbox settings the record
names, invented material only. Every answer to a supplier request came from
the observation harness (origin `observation-harness`), never a person's
act. Not qualification of the pin, the provider or the model (DEP-005); no
App candidate was involved. The labels OB-n are this section's.

| ID | Observation (record section) | Bearing on this file |
|---|---|---|
| OB-1 MCP tools on the local Responses route | Codex sent the model request as `POST /v1/responses`; LM Studio logged "Ignoring unsupported tool type(s): namespace." and the configured MCP test tool never reached the model. The model's two attempted calls were skipped by the server, and no `mcpToolCall` item was produced (OBS-1 §5, §6 S-8). In OBS-1b, with no MCP server, a `namespace` tool was still dropped; its content is not in the log (§B.3). The record's reading (inference): Codex 0.158.0 offers MCP tools to a Responses provider as a `namespace` tool, consistent with the provider capability `namespaceTools` in the generated types | **An observed limit of that route, not of MCP generally** (R13-6). **Consequence for App users at this pin:** where the person's conversation runs on such a local route (a Responses provider that does not accept `namespace` tools, as LM Studio 0.4.16), the App user cannot use a host's MCP tools: neither the agent's MCP tool calls (HCG-A05; WD `mcp-tool-call`) nor a host's operations offered through its MCP server (ADAPTER's MCP path) reach the model. The command-line path was not so limited (OB-2). HCG-A05's availability signals now name `namespaceTools` (§8.4). F-31 |
| OB-2 Command-line path | The model called the flat function tool `exec_command`; Codex raised one `item/commandExecution/requestApproval`; after the harness accepted it, the command ran in the read-only sandbox and exited 0. The item's `command` was the shell-wrapped `/bin/zsh -lc '<cmd>'` and `commandActions` [{`unknown`, the bare command}]; `source` was `agent` at `item/started` and `unifiedExecStartup` at `item/completed` (one item); there were no output-delta frames; `aggregatedOutput` was the tool's stdout line with its newline; the model received the stdout inside `exec_command`'s text envelope (§B.3, §B.6 O-7, A-7) | L-3 positive for a flat function tool at this pair. HCG-A02 observed live once. A receiver that classifies a command item reads its `source` at `item/started` (R14-4: ADAPTER OM-1, EXEC AW-2); this boundary delivers both frames unchanged (H6) |
| OB-3 Order around an approval | `thread/status/changed` [waitingOnApproval] → `item/started` (inProgress) → the approval request, received after `item/started` although its `startedAtMs` is 9 ms earlier → the answer → `serverRequest/resolved` → `thread/status/changed` [] → the command runs → `item/completed` (§B.3; O-7) | An item is announced in progress while its approval is pending. The register entry is created at receipt (R1) whatever the item state; the order is a supplier behaviour delivered as received (H6; F-30) |
| OB-4 `serverRequest/resolved` | Observed once, {threadId, requestId}, 8 ms after the written accept and before the item continued (§B.6 U-09) | Consistent with the RT-12 reading (acknowledgment observation after a written reply, §6.2.1). The trigger before any reply (RT-10) is not observed; U-09 narrows and stays open |
| OB-5 Approval setting quirk | `approval_policy = "untrusted"` in the configuration file was refused at start-up ("`approval_policy = "untrusted"` is no longer supported; remove this setting"; exit before answering `initialize`, 81 bytes on stderr, no network). The generated `AskForApproval` still lists `untrusted`, and `thread/start` accepted it and reported it back (§B.2, D-B1). Under it the request's `availableDecisions` were `accept`, `acceptWithExecpolicyAmendment` and `cancel`: no `decline`, no `acceptForSession` (§B.3). `availableDecisions`, experimental-only in the generated types, arrived with `experimentalApi` false | The person's approval setting (H9) can be refused by the supplier through one carrier and accepted through another. The boundary carries what the person set and records the refusal as observed: an exit before `initialize` is answered is a handshake failure (§4.6 step 4; LT-10, LT-11), never a reason to change the setting. R5 and §7.3 note the request-level decisions and the element seen without the opt-in. F-32 |
| OB-6 Sandbox after approval | The approved command still ran inside the read-only sandbox; its connect to a local Unix socket was denied (kernel `deny(1) network-outbound`), and the listener saw no connection (§B.6 A-7) | An A14 answer did not lift the sandbox under `untrusted`; sandbox and approval stay the person's settings (H9, D3). Reaching a local socket from a sandboxed command is ADAPTER's design question (OC-5) |
| OB-7 Model and provider | Requested and reported model and provider were equal at thread start; no `model/rerouted`; the turn object has no model element (OBS-1 §9; §B.6) | F-23 confirmed live; U-27's thread-scope reading stands (§8.3) |
| OB-8 Provider wire interface | The Responses interface of LM Studio 0.4.16 worked, streamed; the server ignored `prompt_cache_key` and `include` and turned the developer role into system; a fallback-metadata `warning` came before the turn/start response (OBS-1 §5, §9) | L-2 observed at this pair (§8.1); consistent with F-28's strings |
| OB-9 Start-up traffic | Before any thread, in both runs, with `[analytics] enabled = false` and no sign-in: a remote-control loop to `https://chatgpt.com/backend-api/` ("remote control requires ChatGPT authentication"; Codex's local log records the installation id and host name beside it, and whether they were sent is not observed); a featured-plugins request to chatgpt.com answered **401**; the plugin sync of `github.com/openai/plugins` (a full fetch overlapping the first 25 s of the OBS-1 turn on a home that was not fully synced; `git ls-remote` only in OBS-1b). No sign-in request reached the client; during the turns the only model traffic was loopback (OBS-1 §8; §B.5) | L-4 widened: the start-up traffic is not limited to a fresh home and is not stopped by the analytics setting. **Against U-18:** no accepted text decides this traffic, and the supplier's start-up fetch is an item the owner left for the phase review (DECISIONS_PENDING.md Part 3, which stands under DECISION-K1). This file records it and decides nothing |
| OB-10 Per-thread MCP configuration | A dotted-key `config` on `thread/start` added an MCP server to that thread only, visible only through a thread-scoped `mcpServerStatus/list`; the global list showed `runtimeStatus` null (OBS-1 §7, A-1, A-6) | Observed (removed from §10's list). Its use is ADAPTER's (OC-3); configuration writes stay person-directed (§6.8) |
| OB-11 Model context | Codex put the host's IANA time zone into the model's context in both runs (OBS-1 §5; §B.3) | A supplier fact for the redaction categories (§9.1) and DEL-01-05; recorded, not decided |
| OB-12 Process tree | stderr 0 bytes on the runs that started; `git` descendants during the plugin sync; exit within milliseconds at end of input, no survivors 500 ms later (OBS-1 §8; §B.5) | Consistent with H11 at these exits |

Not observed by either run: a model-issued MCP tool call, its item order and
whether it raises an A14 request (O-1…O-4); `serverRequest/resolved` before
any reply; the effect of an answer the request does not offer; the live
effect of `turn/interrupt`; post-restart reads; resume-override adoption.
(v0.9: several of these were observed by OBS-2, §10.2; this section keeps
OBS-1's record as it stood.)

### 10.2 OBS-2 at 0.158.0 (dated observations; v0.9, FH-41)

Record: `OBS_2_0.158.0.md` beside this file, not edited here. **Standing:**
observed on 2026-10-01 at one pairing: the Codex 0.158.0 vendor binary
(sha256 as SPIKE §3), LM Studio 0.4.16+2 on loopback, one model
(`qwen/qwen3.5-9b`), scratch homes with no credential, invented material
only. Every answer to a supplier request came from the observation harness
(origin `observation-harness`), never a person's act. Not qualification
(DEP-005); no App candidate. **O-4, O-4a and O-4b were observed only through
a loopback adapter that flattened Codex's `namespace` tools for LM Studio;
they are cited as "observed through an adapter (OBS-2), not stock
behaviour"** (R18-9). The record notes a stop condition (S-9, memory
pressure) hit during O-4a and the run's continuation; the observations
after it stand with that note (R18-9; DISPATCH). Labels OB2-n are this
section's.

| ID | Observation (record section) | Bearing on this file |
|---|---|---|
| OB2-1 `turn/interrupt` (O-1, §4) | Empty result in about 21 ms; `thread/status/changed` idle; `turn/completed` status `interrupted`; two deltas after the request and before its result; the open `reasoning` item never got `item/completed` and is not in history; Codex closed the provider stream | §6.7 HP-2; G-4: an item opened and never completed settles "not completed (turn ended)" in the receivers (NPTD, NIR, RECOVERY; R18-7); this boundary delivers what arrives (H6) |
| OB2-2 Supplier resolution before a reply (O-3, §5.1) | With an approval held, `turn/interrupt` → `turn/completed` `interrupted`, then `serverRequest/resolved` for the request; a later answer silently ignored; the command item never completed and is absent from history. Side observation: a `cancel` answer ended the item `declined` and the turn `interrupted` | RT-10 provoked (§6.2); U-09 narrowed; §6.2.1 "Negative answers and the turn" |
| OB2-3 Stop, restart, resume (O-2, §5.2) | Stop by closing input: exit 0 in about 21 ms; kill: signal 9. After both: `thread/read` before resume works (`notLoaded`); the turn `interrupted`; the pending request **not** raised again and no resolution sent; no model request on resume; a graceful stop writes a "user interrupted … on purpose" marker into history; `deprecationNotice` on full reads | §4.4 "Recovery reads"; §4.5 steps 2, 3; RECOVERY-v0.2 §5 |
| OB2-4 Delegation on the stock pairing (O-4, §6.1) | Delegation tools travel only in a `namespace` tool (`multi_agent_v1`), dropped by LM Studio 0.4.16; no configuration sends them flat; `[features] multi_agent = false` removes them; `multi_agent_v2` gives namespace `collaboration` with other tools; `agents.<role>` adds `agent_type` to `spawn_agent` | §8.1 L-3; §8.4 HCG-A08; F-31; U-22 |
| OB2-5 Delegation through the adapter (O-4, O-4a, §6.2) | `collabAgentToolCall` `spawnAgent`, `sendInput`, `wait`; child frames on the same connection, no `thread/started`; child readable with `parentThreadId`, `agentRole`, `agentNickname`, `source.subAgent`; children not in `thread/list`, in `thread/loaded/list`; the role file's `developer_instructions` replace the parent's for the child; the child had no delegation tools at default depth | §8.2 table; §8.4 HCG-A08; F-20 |
| OB2-6 Task guidance against delegation (O-4b) | A parent told "you do not delegate" delegated anyway; recorded and shown in full | K-10 "stated, not enforced" (ROLE-v0.2 §6.3); this boundary delivers the items |
| OB2-7 Resume with changed developer text (O-5, §7) | `developerInstructions` on `thread/resume` accepted and ignored, loaded or not; nothing reports it. O-5b: `collaborationMode.settings.developer_instructions` on `turn/start` applied, **added** to the thread's own text | §8 S-6; §8.2 table and P-15 |
| OB2-8 Account home mechanism (O-6, §9) | Linked `config.toml`: the App home reads the person's values as its user layer and reports its own account; `-c` overrides form `sessionFlags`; `--profile` refused for `app-server`; the shared file not written; separate credential storage not distinguishable without a credential | §4.2 step 3; H9; U-03 |
| OB2-9 Start-up traffic (O-7, §10) | `plugins = false` stops both start-up connections, cold or warm; `remote_plugin`, `apps`, `remote_control` do not; the remote-control loop stops only with an internal environment variable and opened no socket without sign-in; no non-loopback socket during turns | §8.1 L-4; U-18; F-14 |
| OB2-10 Plan mode (O-8, §8) | One `plan` item via `item/plan/delta`; no `turn/plan/updated`, no `update_plan` tool; plan mode persists until the default is sent; developer text still sent beside the plan text; `remoteControl/status/read` and plan mode need the opt-in | §4.2 step 4; §8 S-2; §8.4 HCG-A09; VC-09 |
| OB2-11 Process exit and content (§11) | A plugin `git ls-remote` child outlived a stop made about 0.7 s after spawn and was re-parented; every model request's `client_metadata` carried the installation identifier and thread, session and turn identifiers; the host time zone in every model input; no user path in any model input | H11; §4.5 step 3; §9.1 |

Not observed by OBS-2: an interrupt while an `agentMessage` streams; the
remote-control loop when signed in; a shared home with a separate credential
store (M4, M5); writes through a linked `config.toml`; whether plan mode's
precedence over developer text is real or this model's adherence; a child
spawned without an `agent_type`; an interrupt cascading to a child.

### 10.3 OBS-3 at 0.158.0 (dated observations; v0.9; R19-6, R19-7, R19-8)

Record: `OBS_3_0.158.0.md` beside this file, not edited here. **Standing:**
observed on 2026-10-02 at the same pairing as OBS-2, with `plugins = false`
in every home and the model run one prediction at a time; no adapter; no
stop condition hit; no supplier request arrived. Not qualification. Labels
OB3-n are this section's.

| ID | Observation (record section) | Bearing on this file |
|---|---|---|
| OB3-1 `skill` input (W-1, §3) | Honoured only for a `SKILL.md` of a skill Codex has discovered (home root, or a root set by `skills/extraRoots/set`), at its canonical path; then injected as a separate user-role `<skill>` message with the file's bytes and absolute path. Any other path or shape (including `WORKFLOW.md`, a non-canonical spelling, a missing file) is accepted and **silently ignored**, with no error. Every discovered skill is advertised in every request's skills block. An extra root is not kept across a supplier restart | §8.2 table (not used for workflows, R19-7); §9.1 (path disclosure) |
| OB3-2 Chaining in one conversation (W-2, W-2b, §4) | Run B started after a line saying run A ended: the model followed B and dropped A; nothing is removed from history; the injected bytes are fixed in the rollout at the turn's start | §8.2 (supply is per run; history keeps earlier runs' text) |
| OB3-3 `mention` input (W-3, §5) | Accepted; nothing reached the model for a file or a skill | §8.2 table |
| OB3-4 Text input (W-4, §6) | The workflow's bytes as a text element reached the model as the user's text; `thread/read` returns the full bytes | §8 S-6; §8.2 table (the R19-7 route) |
| OB3-5 Experimental settings update (W-5, §7) | `thread/settings/update` with developer text: a developer message appended at each change, earlier ones kept and resent; persists across turns and restart; in plan mode a non-null value replaces the mode's built-in text | §8.2 table (not used for workflows, R19-7) |
| OB3-6 Fork (W-6, W-6b, §8) | `thread/fork` with new `developerInstructions` (or `config.developer_instructions`): accepted and ignored; the fork carries the source's developer text and history, gets a new thread identity with `forkedFromId`, keeps the source's turn identities, and references the source's rollout rather than copying it; `thread/list` shows `forkedFromId` null | §8 S-6; §8.2 table (R19-8); U-19 (whether deleting a source breaks its forks) |
| OB3-7 Content sent (§9) | Base instructions, the thread's developer text, the skills block, a permissions block and `<environment_context>` (working folder, shell, date, time zone); installation and thread, session, turn identifiers in `client_metadata` and the `x-codex-turn-metadata` header; no non-loopback socket with plugins off | §9.1 |

## 11. Owner / act boundary (REQ-007, REQ-008, AC-007, VER-007)

| Act | Owner | This boundary's contribution | Not performed here |
|---|---|---|---|
| Select the definition/generation pin | App implementation owner; owner decision D4 selected 0.158.0 | §7 record, §10 observations, §9.5 method | Qualification; re-examination before implementation |
| Decide Rust/TS allocation | App implementation owner (OI-008) | §12 proposal | Decision |
| Choose the reference generator output | App implementation owner (U-15) | §7.3 options | Decision |
| Durable session/request custody, reconnect, relaunch, stop | DEL-01-02 (RECOVERY-v0.2) | §4, §6 interface, S-1 | Custody code, persistence, recovery |
| Plan/tool/delegation presentation | DEL-01-03 (NPTD-v0.2) | S-2 | Views, registry, revision identity, checker |
| Request cards, answers, outcomes, attachments | DEL-01-04 (NIR-v0.2 §4–§6; the App act control AAC-v0.2) | S-3 | Cards, answer UX |
| Sign-in (including OAuth), API key, local provider (options the person chooses among, no default: DECISION-4 D4-3), substitution checks | DEL-01-05 (ACCESS-v0.2; ACCOUNT-HOME-RECORD-v0.2) | S-4, §8.1 | Flows, configuration, substitution evidence; any sign-in, which is the person's own |
| Packaging, signing, notarisation, distribution | DEL-01-06 (terms obtained by owner, OQ-08) | S-5 | Packaging production |
| Workflow semantics / making / registration | DEL-02-01 / DEL-02-02 (WR-v0.2; run-start text WR-v0.2 §16) | S-6 carriage of the run-start text (R19-7), §8.2 evidence | Semantics, registration, run-start composition and framing, capability naming |
| Additive guidance production | DEL-02-04 (ROLE-v0.2) | S-6 carriage at thread start, §8.2 evidence | Composition |
| Operation-policy / human-act definition | DEL-04-01 (D2, D3 adopted; OI-021 additions pending) | R7–R9 origin truthfulness | Policy |
| Run/act records | DEL-04-03 | S-7 observed facts | Records |
| A14 answer tool permission | The person (via DEL-01-04's request cards, NIR-v0.2 §4), or the user's own Codex mode inside the supplier (D3 setting; origin rule R7, DERIVED per R-2/R2-11) | Register accepts and records it with supplied actor/origin; evidence to the run record's tool-permission entries only (R2-8) | Performing, inferring or answering it affirmatively by App rule |
| A4 mark checked, A5 accept, A6 approve, A7 rely, A12 set grant, A13 enable external access | The person (reserved, D2) | None; no A14 answer or App rule stands for any of them (R7, R8) | All |
| Supplier engine, credentials, published protocol | OpenAI Codex (DEP-005) | Consumes as published | Any modification |

No act in this table is a prerequisite for another unless its owner's own
contract says so; no universal acceptance-before-checking or
acceptance-before-reliance sequence is implied (AG-02).

## 12. PROPOSAL for OI-008 — Rust/TypeScript division

**Label: proposal by the DEL-01-01 drafting task for the App implementation
owner, who decides (OI-008, SOW-131, REQ-004). Nothing here is selected.**
Evaluation order: maintainability, then functionality, then local
models/privacy (V4-CST-01, AX-001); few mainstream stacks, no
release-candidate frameworks (M-6, SOW-101).

| Option | Main process (Rust) | Interface (TypeScript) | Assessment |
|---|---|---|---|
| **O-1 Rust envelope core** | Verification, spawn, process-tree lifecycle (H11), framing, correlation, generation tagging, register (§6) with R1–R9, unfamiliar-request errors, recording tap, guidance-identity evidence. Payloads opaque except envelope elements and the familiar server-request set with answer-validity rules | Composes typed requests with generated TS types + supplement through one generic request path; presents native items; submits A14 answers via register operations | One payload type set in the language that consumes payloads; Rust small and payload-agnostic, so schema drift lands mostly in TS; invariants held in Rust. At 0.158.0 the committed JSON Schema bundles suit a build-time familiar-set list for Rust; the process-tree handling found by the spike fits a Rust owner. **Recommended** |
| O-2 Rust fully typed | As O-1 plus typed payloads, orchestration and composition in Rust | Presentation only | Two generated type sets or derived TS; more Rust touched on every schema change (170 client methods at 0.158.0) |
| O-3 Rust pipe relay, TS protocol client | Spawn and byte relay only | JSON-RPC client, correlation, register in the webview | **Violates** ARC §3 (register lost on reload, V4-EXE-01). Set aside |
| O-4 Node helper in main process | Rust spawns Node running ported v3 client code | Presentation | Adds a runtime and process, resembles the excluded v3 service (V4-ARC-03, M-6). Set aside |

**Open within O-1:** where thread/turn orchestration and guidance carriage
live beyond the generic request path; how the familiar set and
answer-validity rules are derived for Rust from the chosen reference output
(U-15). Which interface component re-attaches after reload is answered by
DEL-01-02 (v0.9): each window's observer re-attaches from its position and
the main process holds the per-generation journal (RECOVERY-v0.2 §3.3, §4.1;
PROPOSED placement under R17-5).

**Optional-reuse assessment (REQ-004, AC-004, ARC §3 reuse candidates).**
v3 code is evidence of behavior, not qualified v4 material.

| v3 source (historical) | Reuse as | Receiving-contract gaps to close |
|---|---|---|
| `chirality-runtime/packages/daemon/src/codex-app-server-client.ts` | Behavior specification for the O-1 port | F-02…F-05; timeouts → unknown; must not require the version member (S-F-08); no process-tree handling (S-F-06) |
| `codex-supervisor.ts` server-request routing and answer/cancel shapes | Behavior reference for R2/R5/R8 | 0.154-era shapes; re-derive from 0.158.0 output (new `item/permissions/requestApproval`, `currentTime/read`); F-02 |
| `app-owned-composition.ts` version assertion; `chirality-app-dev/frontend/scripts/verify-codex-pin.mjs` | Behavior reference for §7.2 | Label-only (F-06); single binary, not vendor tree (S-F-02) |
| `chirality-runtime/packages/core/src/native-plan-registry.ts` | DEL-01-03's decision | Tied to v3 vocabulary/admission model; 0.158.0 plan updates carry no revision identity |
| Translation into Chirality event names; socket/daemon; Next routes | Not selected (ARC §3, §7) | — |

## 13. Findings

- **F-01 Overlap on the unknown-request error** (DEL-01-01 REQ-001/AC-001/
  VER-001 vs DEL-01-02 OUT-001/REQ-004). Proposed reading in §6.5.
  **Closed at v0.9:** DEL-01-02 accepts the split as written (RECOVERY-v0.2
  §1, §6; §6.5).
- **F-02 v3 conflated "no live turn" with "unknown"** (answered known
  requests with method-not-found). R6 forbids carrying this over.
- **F-03 v3 swallowed reply write failures.** v4 records
  `settle-write-failed`.
- **F-04 v3 turned client-request timeouts into engine-unavailable
  rejections.** For a mutating request that is an unknown outcome (H10).
- **F-05 v3 dropped malformed/oversize frames after counting them.** H7.
- **F-06 v3 version check compared the label only.** §7.2 adds distribution
  content identity; the spike shows the supplier executes sibling binaries,
  widening the identity to the vendor tree.
- **F-07 Receivers.** DEL-01-01 is not a CASE-002 member; receivers from
  `Dependencies.csv` plus J9 (V1-C). From v0.7 the Receivers line also
  follows the consumers' registers (R9-6).
- **F-08 Wire names in the accepted basis.** V4-ARC-04's per-thread provider
  element is confirmed present at 0.158.0 (`modelProvider`, P-11); still a
  supplier fact, not a Chirality representation.
- **F-09 D-GOV-43 vs v4 basis — resolved in part.** Owner decision D3 now
  settles the tool-permission/sandbox element for the first increment (§2).
  "No notification filtering" remains a definition choice (U-07).
- **F-10 Acknowledgment observability.** `serverRequest/resolved` exists at
  0.158.0; its triggers are not observed (U-09).
- **F-11 No gap** in the SoW obligations for this definition.
- **F-12 The supplier labels its embedding surface experimental.** At
  0.158.0 `codex --help` lists `app-server [experimental]` and both
  generators are `[experimental]` (S-F-18). ARC §6 assumes the App Server
  protocol "stays published and supported for embedding". Routed to owner
  visibility and to the pin re-examination under D4 (U-21); it does not
  reopen the chosen supplier direction (ARC §3) but bears on the
  maintainability priority and DEP-005.
- **F-13 App-required features are experimental-only at 0.158.0** (plan
  collaboration mode, thread settings update, dynamic tools, available
  decisions). The App must declare the experimental opt-in to use plan mode;
  the supplement narrows but upgrade exposure to experimental churn widens
  (ARC §8 risk "protocol drift"). **v0.9:** under K-5 the App declares
  `experimentalApi: true` and records it per generation (§4.2 step 4;
  NPTD-v0.2 §4 EX-2). At OBS-2 (0.158.0) plan mode and
  `remoteControl/status/read` needed the opt-in and delegation did not
  (stable feature `multi_agent`), so only plan mode is labelled
  "experimental" (R18-1 C-05). `thread/settings/update` is not used for
  workflows (R19-7).
- **F-14 Network at start on a fresh home (L-4).** ≈24 MB fetch from
  `github.com/openai/plugins` with no sign-in or turn; its descendants can
  outlive the supplier. Routed to the **owner** and **DEL-01-05** (OI-009: a
  separate App account home would be
  "fresh" at least once per home). Configurability not observed (U-18). Up
  to v0.6 the owner route was framed as "priority 3, local-operation
  boundary". The amended ARC §1 priority 3 speaks of a host's agent and
  states no such boundary for the App, so no accepted text now frames this
  traffic (L-4); the question to the owner stands as U-18 states it.
  **v0.9:** the separate App account home is decided (K-1), and with
  DECISION-L L-1 there is one per App-owned home (H-acct; H-key when a key is
  added), so the fresh-home fetch happens at most once per home, and only
  with plugins on. At OBS-2 (0.158.0, O-7; v1, v8) `[features] plugins =
  false` stopped the fresh-home fetch and the warm `ls-remote`, and the
  featured-plugins request; plugins follow the person's own setting
  (DECISION-L L-3; §8.1 L-4).
- **F-15 D1 defers the standalone-App receivers.** DEL-01-02…05 definitions
  are a later undertaking; seams S-1…S-4 have no receiving comparison in this
  one. **Closed at v0.9, per seam:** S-1 by RECOVERY-v0.2 §1 (reconciliation with §6.5) and §4.2 (consumed) (DEL-01-02),
  S-2 by NPTD-v0.2 §2 (DEL-01-03), S-3 by NIR-v0.2 §4–§6 with AAC-v0.2
  (DEL-01-04), S-4 by ACCESS-v0.2 §19 (DEL-01-05; R18-7 G-1). S-6 has its
  receiver in ROLE-v0.2 §5 (DEL-02-04) and, for a workflow's run-start text,
  WR-v0.2 §16 (DEL-02-02; R19-7).
- **F-16 Register rows.** No DEL-01-01 → DEL-02-04 DOWNSTREAM row (V1-C
  RF-6); with R7 repaired per V1-A D-13 the existing rows suffice for D3
  (RF-03). Both went to closeout C1; not edited here. v0.7: the arc is now
  represented from the consumer's side (DEP-02-04-010, admitted in
  DAG-003). This register still has no DOWNSTREAM mirror row; DAG-003's
  HANDOFF_STATE lists "Deferred supplier-side mirror rows" with the
  register owners.
- **F-17 Retired in v0.3.** The stale spike UNRESOLVED row it reported was
  corrected by the parent (spike revision 26ea0c2f…0334 and later; current
  0e090a4c…b115 marks it RESOLVED by the re-selection) (IR1C-19).
- **F-18 `~/.codex` changed during the spike window** (SPIKE §1), with
  attribution to the spike not established and a separate person-owned Codex
  process present. Relevant to OI-009 (shared vs separate home); no
  conclusion drawn. **v0.9:** under K-1 (option C) the App's Codex runs in
  App-owned homes; the person's home is written by the App only through a
  person-directed configuration write (§6.8; ACCESS-v0.2 §6), and OBS-2
  (O-6) found the person's stand-in file unchanged by every case.
- **F-19 App-initiated MCP calls are thread-bound (0.158.0).** The
  generated `mcpServer/tool/call` parameters **require** a thread identity.
  An App-origin call therefore names a conversation whose model and history
  may or may not see it (not observed). This is why §6.8 forbids using it to
  act as the agent and defines no host-channel use; DEL-03-03 OC-2/OC-7
  should weigh it before choosing any App-side realization that calls MCP
  tools itself.
- **F-20 Supplier-reported effective settings exist at 0.158.0.** Thread
  start/resume responses report the effective `model`, `modelProvider`,
  `approvalPolicy`, `approvalsReviewer`, `sandbox` and `instructionSources`
  (`observed-in-generated-types`). They could serve R4-1 (effective
  destination) and possibly the P-15 "adopted" question (instruction
  sources). They are not relied upon until observed live (U-19); routed to
  DEL-04-03 and DEL-02-04 as candidate evidence. **v0.9:** DEL-02-04
  consumes `instructionSources` as Codex's own report (ROLE-v0.2 §4.3); at
  OBS-2 and OBS-3 (0.158.0) it was `[]` in every case (no `AGENTS.md` in the
  scratch working folders), so its content is still not observed. Child-role
  facts now seen through the OBS-2 adapter (§10.2 OB2-5): `Thread.parentThreadId`,
  `Thread.agentRole`, `Thread.agentNickname` and
  `source.subAgent.thread_spawn.agent_role` on the child's `thread/read`.
  Neither resume nor fork changes the developer text (§8.2).
- **F-22 Closed (R6-4, in place).** The HP-4 scope question (person's own
  messages on a holding run) is settled by EXEC-v0.3 §2 HP-4: not blocked,
  carried `person-directed`, disposition unchanged, governed agent actions
  are *action during hold* (§6.7).
- **F-23 Per-turn effective destination is indirect at 0.158.0.** Turn
  start carries a per-turn `model` (stable) but no provider element, and the
  turn object reports no model. A per-turn *effective* value is therefore
  the thread-level report plus any `model/rerouted` notification; R5-4's
  "where the supplier reports it" applies, and other turns are *unknown*
  rather than inferred. Routed to DEL-04-03 (RS R5).
- **F-21 D5 does not settle U-18.** The owner's flexibility ruling covers
  host content reaching the conversation's model. The supplier's own
  fresh-home plugin fetch (L-4) is a separate matter for the owner with
  DEL-01-05.
- **F-24 D4-3 and this boundary (v0.6; R8-9).** DECISION-4 D4-3 (cloud by
  OAuth sign-in or API key; no default between local and cloud) revises the
  host-agent basis, V4-HOST-01 (applied to the accepted text by SCA-V4-001).
  This file described no "local by default"
  rule for the App (checked), and it cites neither V4-HOST-01 nor
  V4-HOST-02. D4-3 is recorded at L-5, S-4 and §11 for DEL-01-05. D4-3 does
  not settle U-18 either: the supplier's own start-up fetch is not a model
  destination the person chose.
- **F-25 V4-HOST-02 cited only to scope it out (R8-13).** From R8-13 this
  file cites V4-HOST-02, as amended by SCA-V4-001 for DECISION-5, only in
  the §2 scope
  note, which says it does not govern the App's Codex. F-24's statement
  that the file cites neither V4-HOST-01 nor V4-HOST-02 held until R8-13.
  From v0.7, L-5 and the header also name V4-HOST-01, again only as the
  host-agent text.
- **F-26 Evidence route to DEL-04-03 (v0.7; R9-7).** Up to v0.6, §6.4, S-7
  and §8.2 said the observed facts reach DEL-04-03 "through DEL-01-02".
  DEL-04-03's ScopeOfWork (CLM-004), its register row DEP-04-03-027 (arc
  N-15, kept by the owner: SCA-V4-001 OWNER_ITEMS O-29, DECISION-6) and RS
  take them from DEL-01-01 directly. DEL-01-01's own ScopeOfWork was checked
  and states no route (CLM-004 gives DEL-01-02 durable sessions and
  outstanding-request recovery; CLM-005 gives DEL-04-03 the content-bound
  records). The three passages now say "directly". This register has no
  DOWNSTREAM row to DEL-04-03; that is a register matter, returned.
- **F-27 Harness-capability meaning (v0.7; R9-6).** DEL-02-01's register
  row DEP-02-01-025 (arc N-16, admitted) expects "the harness capability
  meaning supplied through DEL-01-01", and its ScopeOfWork CLM-002 says
  DEL-01-01 "supplies the harness capability inventory". This file supplies
  the 0.158.0 inventory and assigns the naming to DEL-02-01 (§8, closing
  paragraph). Neither this file nor WD defines the capabilities (WD U-08).
  §8 marks a meaning beyond the inventory "not yet defined here". Returned
  as a Wave B item. **v0.8:** §8.4 supplies the meaning as a capability
  account (PROPOSED); the names stay DEL-02-01's. The finding stays open
  until DEL-02-01 states which groups its portable names resolve to (a
  join for node V18). **Closed at the RP-3 repair (R14-5):** WD-v0.8
  §4.2.5 now names, in its group column and rule HC-7, the one §8.4 group
  each of its ten portable names resolves to at 0.158.0 (HCG-A02, A03, A05,
  A06, A07, A08, A09, A10, and A11 for two names), and follows this file's
  grouping of the three members V18-2 found read differently (§8.4,
  "Members WD reads differently").
- **F-28 Strings in the 0.158.0 binary bear on OBS-1 (v0.8).** The vendor
  binary in the spike's scratch install was read as bytes, not executed.
  Its strings include: "`wire_api = "chat"` is no longer supported … set
  `wire_api = "responses"` in your provider config"; "Local LM Studio server
  (default port 1234)"; the environment names `CODEX_OSS_BASE_URL` and
  `CODEX_OSS_PORT`; the built-in provider names `ollama` and `lmstudio`;
  "Successfully downloaded model" and "Failed to execute '… get --yes …'"
  in the LM Studio module, near the default model name `openai/gpt-oss-20b`.
  Standing: strings in the binary, **not observed behaviour**. They suggest
  that Codex needs the Responses interface from a local provider (bearing
  on L-2, U-22) and that its local-provider path can ask LM Studio to
  download a model. The OBS-1 brief treats both as risks with stop
  conditions.
- **F-29 The prototype's validity reference (v0.8).** The boundary model
  checks answer validity (R5) and the double's constructed frames against
  the committed JSON Schema experimental bundle because it is the committed
  machine-readable output. That is a prototype convenience, **not** a choice
  of the reference output (U-15 stays open): under it the two TS-only
  notifications would be marked unfamiliar, and the three TS-only client
  methods are absent.
- **F-30 Dispatch order and the reached-when table (v0.8).** DEL-02-03's
  App-run reached-when table (EXEC, node B2) takes `item/started` of a tool
  item as the earliest native observation of a call and marks the order
  against the tool's own receipt "OBS-1 pending". This boundary delivers
  items in received order (H6) and sits on no dispatch path (HP-1 not
  adopted), so the order is a supplier behaviour to observe, not one this
  file can supply. OBS-1 O-1 records it with the test tool's receipt time.
  **Observed for the command-line path (OBS-1b; §10.1 OB-3):** the command
  item is started, and announced in progress, before its approval request is
  received, and the tool runs only after the answer and the
  `serverRequest/resolved`; the item's `source` changes from `agent` to
  `unifiedExecStartup` between start and completion (OB-2). The MCP path
  stays unobserved (OB-1).
- **F-31 MCP tools on a local Responses route (RP-3 repair; R13-6).** At
  0.158.0, against LM Studio 0.4.16 through the Responses interface, LM
  Studio logged the `namespace` tool type as unsupported and no MCP tool
  reached the model (§10.1 OB-1); that Codex offered the MCP tools as that
  `namespace` tool is the record's inference, not an observation. An observation of that route, not
  of MCP generally. Consequence at this pin: an App user on such a route
  cannot use a host's MCP tools; the command-line path still works (OB-2).
  Routed to DEL-01-05 (provider choice and its account, S-4), DEL-03-03
  (the MCP path) and DEL-02-03 (presence of `mcp-tool-call`, WD HC-4); the
  provider capability `namespaceTools` is the element to observe on another
  route. Whether a setting makes Codex send flat function tools to such a
  provider, or another local server accepts `namespace` tools, is not
  observed (U-19). **v0.9 (OBS-2 O-4, 0.158.0):** the delegation tools also
  travel only inside a `namespace` tool, so on such a route delegation is
  unavailable as well (K-5's "views absent" applies to every LM
  Studio-served conversation at this pin); no configuration tried at OBS-2
  sends them as flat functions.
- **F-32 The approval setting through two carriers (RP-3 repair; R13-6).**
  At 0.158.0 the supplier refused `approval_policy = "untrusted"` in its
  configuration file at start-up, while the generated types still list the
  value and `thread/start` accepted and reported it (§10.1 OB-5). Under it a
  command approval request offered no `decline`. The boundary carries the
  person's setting unchanged (H9) and records a start-up refusal as a
  handshake failure; which carrier the App uses for the person's setting is
  DEL-01-05's (S-4). The answer a person may give is the one the request
  offers (R5).
- **F-33 Accepted is not applied (v0.9; OBS-2, OBS-3 at 0.158.0).** Several
  inputs are accepted without error and have no effect, and nothing in the
  protocol reports that: `developerInstructions` on `thread/resume` (O-5)
  and on `thread/fork` (W-6), `config.developer_instructions` on
  `thread/fork` (W-6b), a `skill` input whose path is not a discovered
  skill's canonical path (W-1), and a `mention` input for a file or skill
  (W-3). A response without error is therefore never evidence that an
  input took effect. This boundary records such inputs as *supplied* (§8.2)
  and never shows them as applied; the model-facing effect is read from
  history (`thread/read`) or a provider-side observation, not inferred
  (R19-5: re-checked at each version).

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| U-01 Qualification of the maintained supplier/App candidate (SUP1 owner advances development/definition pin to 0.160.0; historical D4 0.158.0 retained) | App implementation owner | Before qualification reliance | 0.160.0 adopted for definition/development under reviewed SUP1 propagation; expected qualified distribution identity and product qualification still absent |
| U-02 `UNRESOLVED{OI-008}` Rust/TS division | App implementation owner | Before architecture production contracts | §12 is a proposal only |
| U-03 ~~`UNRESOLVED{OI-009}`~~ account home, incl. which home the label probe writes into (S-F-17). **Closed at choice level (v0.9)** by DECISION-K3 K-1 (option C) and DECISION-L L-1: App-owned homes sharing the person's configuration by a link, each with its own sign-in; a separate probe home (ACCOUNT-HOME-RECORD-v0.2; ACCESS-v0.2 §3) | Owner with App implementation owner (DEL-01-05) | Before account integration | Mechanism observed for configuration sharing (OBS-2 O-6 M1, M2; §4.2 step 3). Still open: separation of credentials with a credential present (M4, M5; not observed under DECISION-L L-6), and writes through the link |
| U-04 *Closed by owner decision D3* (tool-permission/sandbox modes are the user's own Codex setting) | — | — | H9, R7 settled |
| U-05 Restart bound values and grace period | App implementation owner with DEL-01-02 | Before implementation | Rules defined; numbers open |
| U-06 Running an unverified distribution for development, and its label | CC-H candidate LT-24; independent review pending | Before product propagation | Explicit unverified-development route; mismatch refused; no pin qualification |
| U-07 Use of the supplier's notification opt-out (`optOutNotificationMethods`) | App implementation owner | Before implementation | Definition uses none (H7) |
| U-08 Content-identity algorithm for distribution/output/supplement/guidance records | App implementation owner (with DEL-04-03) | Before qualification records | Spike used SHA-256 as an observation method; not selected for records |
| U-09 Acknowledgment observation mechanism; `serverRequest/resolved` triggers | DEL-01-02 with this deliverable | Before settlement fixtures | Candidate source named; semantics open. v0.8: the PROPOSED reading of §6.2.1 (after a written reply it is an acknowledgment observation; before any reply, `resolved-by-supplier`) is exercised against the double. OBS-1b observed the notification once, 8 ms after a written accept (§10.1 OB-4), consistent with the reading. **v0.9: narrowed.** The RT-12 reading is adopted by DEL-01-02 (RECOVERY-v0.2 §6 U-09); the before-reply trigger is observed for `turn/interrupt` (OBS-2 O-3; §6.2), so that trigger is closed. Open: other before-reply triggers, and whether every kind is followed by a notification after a reply (for *not-observable-at-pin*) |
| U-10 Stop-time handling of outstanding entries. **Closed (v0.9)** by RECOVERY-v0.2 §6 U-10: no App decline at stop or quit; entries end `ended-unanswered(process-exit)` (§4.5 step 2) | DEL-01-02 | — | Consistent with OBS-2 O-2 (no re-raise, no resolution sent) |
| U-11 Any automatic decline after a period (incl. the native `timed_out` form). **Closed (v0.9)**: none; `timed_out` is never sent (R17-9; RECOVERY-v0.2 §6 U-11; R3) | — | — | R3 |
| U-12 More than one concurrent supplier child | App implementation owner | Before implementation | Up to v0.8: one active child assumed. **v0.9 (DECISION-L L-1; R19-4; report only, R17-2):** one child per App-owned home (H-acct; H-key when the person adds an API key); generation, register and thread are keyed by home (H5); DEL-01-02's DEF-5/DEF-6, quit, Stop Codex and Restart Codex apply to each home's child, and each conversation's recovery reads go to its own home (RECOVERY-v0.2 §2; V2-1); H-probe runs only the label probe and is not a hosted child; K-12 start-up traffic happens per home. The concurrency of two homes' children beyond that (for example a shared resource lock) is not observed |
| U-13 Redaction policy details | App implementation owner | Before first capture | Categories extended (§9.1; v0.9 adds the account-method elements, secret answers, the provider-bound identifiers and time zone, and skill paths) |
| U-14 DEL-01-01/DEL-01-02 unknown-request split (F-01). **Closed (v0.9)**: RECOVERY-v0.2 §1 accepts §6.5 as written | Both owners | — | §6.5 |
| U-15 Reference generator output (O-R1/O-R2/O-R3) | App implementation owner | Before R2/R5 implementation and conformance | Options in §7.3 |
| U-16 Supplier descendant handling on stop/restart/overlap | DEL-01-02 with App implementation owner | Before lifecycle implementation | H11 requires detection and recording. **v0.9:** policy PROPOSED in RECOVERY-v0.2 §6 (the whole tree ended at a deliberate stop; after an unexpected exit, survivors recorded and shown with a person's action to end them, not ended by rule; overlap wait a TEST VALUE), still with the App implementation owner. OBS-2 §11 shows why a deliberate stop ends the process group (H11) |
| U-17 Distribution-identity composition and launcher (wrapper vs vendor) | App implementation owner with DEL-01-06 | Before verification implementation | Both recorded; composition open |
| U-18 Supplier network fetch at start: acceptability (framed up to v0.6 as "under priority 3"; the amended priority 3 speaks of a host's agent, and no accepted text now decides this traffic, L-4); configurability (not addressed by D5, which concerns host content reaching the conversation model) | Owner with DEL-01-05 | Before any local-operation claim; the supplier's start-up fetch is left for the phase review (DECISIONS_PENDING.md Part 3, standing under DECISION-K1) | Observed; no claim of local-only operation. OBS-1 and OBS-1b (§10.1 OB-9): with analytics off and no sign-in, start-up also contacts chatgpt.com (remote control; featured plugins, 401) and syncs github.com/openai/plugins on a warm home. **v0.9: decided for the App** by DECISION-K3 K-12 (as revised) with DECISION-L L-3 and R18-3: the App turns off what Codex's settings allow, plugins follow the person's own setting, the remote-control loop is shown (no internal environment variable is used), and the network view shows and records the rest (ACCESS-v0.2 §9). OBS-2 O-7 filled which setting stops which connection (§8.1 L-4). Still open: the update check (`check_for_update_on_startup` not tested), and the remote-control loop when signed in |
| U-19 Unobserved live behaviors (§10 "Still to observe") | App implementation owner (next spike; needs credential or local provider) | Before settlement fixtures, handshake implementation and qualification | Recorded as not observed. v0.8: OBS-1 is briefed for a subset (§10 note; `WAVE_B/OBS-1_BRIEF.md`). OBS-1 and OBS-1b observed part of it at one pair (§10.1); the MCP tool-call items remain unobserved because the local Responses route dropped the MCP tools (OB-1; F-31). **v0.9: narrowed** by OBS-2 and OBS-3 (§10.2, §10.3). What remains: an interrupt while an `agentMessage` streams; the remote-control loop when signed in; a shared home with a separate credential store (M4, M5); writes through a linked `config.toml`; a model-issued MCP tool call and whether it raises an A14 request; delegation on a stock pairing that accepts `namespace` tools, a child without an `agent_type`, and an interrupt reaching a child; whether deleting a fork's source breaks the fork; whether a skill disabled by `skills/config/write` is still injected by a `skill` input; plus the v0.8 items not touched (whether `initialized` is required, relocation, outbound frames without the version member, requested against effective model when they could differ) |
| U-20 Partition of the 0.158.0 server-request kinds and their R9 origin classes (§6.1 proposal) | App implementation owner with DEL-01-04/01-05 | Before R2 implementation | Proposal; R9 classes fixed as INTEGRATION. **v0.9: narrowed** to the App implementation owner's confirmation: DEL-01-04 states the answer path and decline form per kind (NIR-v0.2 §4.1, §4.3), DEL-01-05 confirms `account/chatgptAuthTokens/refresh` as known-app-unsupported (ACCESS-v0.2 §7 CR-9) |
| U-21 Supplier's `[experimental]` label on app-server/generators; dependence on experimental API (F-12, F-13) | Owner visibility; App implementation owner at pin re-examination | Before implementation | Recorded; supplier direction not reopened |
| U-22 L-2 provider wire interface (Responses) and L-3 | DEL-01-05 | Before provider qualification | Observed at one pair, not qualified (§10.1 OB-1, OB-2, OB-8): Responses to LM Studio 0.4.16 works; flat function tools work; MCP tools are not delivered on that route (F-31). **v0.9:** carried into ACCESS-v0.2 §11 CH-1…CH-3; OBS-2 O-4 adds that the delegation tool set travels in the same dropped `namespace` tool, so delegation is unavailable on that route too (§8.1 L-3; F-31) |
| U-23 `UNRESOLVED{D6}` App-side run holds. SWBPIPE answered SQ-02 on 2026-09-28 with no host-held route (route (iv), none planned). **Closed for Phase 1** by DECISION-4 D4-1; re-opens when the governance phase is taken up (R8-2) | The owner (DECISION-4; D6 re-opens with the governance phase), via DEL-02-03 | When the governance phase is taken up for a workflow that needs it; before App-side hold implementation | Phase 1: no App run is holding, and no hold point is used (§6.7). Governance phase: no hold claim; `turn/interrupt` not relied upon; HP-3 and HP-4 best effort only; hold-support values per R5-1 as amended by R8-2 |
| U-24 Any App-initiated use of `mcpServer/tool/call` / `mcpServer/resource/read` on a host channel | DEL-03-03 (OC-2/OC-7) with App implementation owner | Before any such use | None defined; App-origin rules of §6.8 bind any later use |
| U-26 Order of the register refusal reasons and the client-request outcome `refused-not-sent(not-ready)` (§6.2.1, §5.1; PROPOSED at v0.8) | App implementation owner with DEL-01-04 (answer path) and DEL-01-02 (custody) | Before R4 and client-request implementation | Proposed and exercised against the double; not decided. **v0.9:** DEL-01-04 accepts the order and gives each reason words for the person (NIR-v0.2 §4.4 RT-05 row); the App implementation owner's decision remains |
| U-27 Per-turn effective destination reading: a turn's effective value only from a report naming that turn; the thread-level report kept at thread scope (§8.3; PROPOSED at v0.8) | DEL-04-03 (RS R5) with this deliverable | Before the model-destination record is implemented | Proposed and exercised against the double (VC-26); OBS-1 and OBS-1b observed the thread-level report live (requested = reported; no turn element; no re-route; §10.1 OB-7) |
| U-25 *Closed (R6-4)* by EXEC-v0.3 §2 HP-4 scope: person-directed turns are not blocked, carried `person-directed`, disposition unchanged, governed agent actions are action during hold | — | — | §6.7 |

## Verification cases

Designed, not qualified. "Runnable now" means the case can be executed
against 0.158.0 artifacts or a supplier double seeded from the spike
transcripts; no App candidate exists, so no case can pass a VER criterion
yet, and spike runs (SV-nn) are evidence, not passes. From v0.8, "Ran … pass (model)"
means the case ran on this machine against the supplier double, with the
boundary model of §9.6 standing in for the App side: it is evidence that the
rules run as written, not a VER pass.

| Case | Setup | Action | Expected result | Runnable now? | Serves |
|---|---|---|---|---|---|
| VC-01 Stock and unmodified | Candidate and pin | Inspect stack, distribution identity vs expected, launcher/configuration | Tauri 2/React/Vite; vendor-tree identity matches recorded; no patch; launcher and added environment recorded | Partly: SV-03 observed the binary identity; no candidate | VER-001 |
| VC-02 Pipe ownership | Candidate, turn active | Close and reopen the window | Same generation; work continues; register unchanged | No (candidate, live turn) | VER-001 |
| VC-03 Unfamiliar request | X-07 | Double sends an unfamiliar server request | Entry (R1); explicit error (R2); no affirmative answer; marked `unfamiliar` | Yes (double). **Ran 2026-09-30 (§9.6): pass (model)**: entry at receipt, `unfamiliar`, explicit error written; no affirmative answer | VER-001 |
| VC-04 Malformed frames | X-08 | Malformed, oversize, version-member-less frames | Malformed surfaced; version-member-less valid frames accepted (S-F-08) | Yes (double). **Ran 2026-09-30 (§9.6): pass (model)**: four malformed frames (not JSON, not an object, unclassifiable, oversize) counted and surfaced with generation and position; valid frames without the version member accepted | VER-001 |
| VC-05 Exit with outstanding work | X-09 | Kill child mid-turn | `ended-unanswered(process-exit)`; `unknown-no-response`; no grant; old answers refused `generation-closed` | No (live turn) | VER-001, VER-006 |
| VC-06 Restart bound | Constructed failures | Force failures past bound | `halted-after-repeated-failure`; explicit restart needed | Yes (double). **Ran 2026-09-30 (§9.6): pass (model)**: three handshake failures → `halted-after-repeated-failure`; explicit restart → `ready`; an exit after `ready` with exit code 0 and no stop record → `exited-unexpectedly`, pending request `unknown-no-response`, entry `ended-unanswered`, automatic restart | VER-001 |
| VC-07 Generated provenance | 0.158.0 | Regenerate both kinds/variants; check manifest; inspect supplement | Identical identities; supplement per chosen reference only | Yes. Evidence so far (`generated/0.158.0/COMMITTED_STATE.md`, IR1C-04): committed tree against the manifest **2 OK / 2,357 not committed / 0 mismatched**; the 1,605 TS files verified **OK** against the manifest from the parent's temporary scratch copy (after its deletion TS verification needs regeneration); SV-01 determinism as returned by W11. The W11 SV-02 line "1,607 OK, 752 missing" described the spike's proposed, never-committed form. Reference not chosen (U-15); no pass claimed | VER-002 |
| VC-08 Native pass-through | X-01/X-02 | Compare delivered frames to recorded | Method, ids, payload and top-level supplier elements (`emittedAtMs`) unchanged; metadata beside | Partly: X-01 side from spike transcripts. **Ran 2026-09-30 (§9.6): pass (model)** for the X-01 side: delivered frame byte-identical to the recording, `emittedAtMs` included, metadata beside. X-02 needs a live turn (OBS-1) | VER-002 |
| VC-09 Version identity to plan receiver | X-01/X-03 | Trace `ready(g)` record and plan updates to S-2 | Record complete; plan updates native, whole-plan, with generation/position; revision identity is DEL-01-03's (v0.9: NPTD-v0.2 §5.2 RV-1 plan-item revision, RV-2 checklist revision) | No (plan needs live turn). v0.9: at OBS-2 (0.158.0, O-8) plan mode produced a `plan` item via `item/plan/delta` and no `turn/plan/updated`, so only the RV-1 surface was seen; observation, not a run of this case | VER-003 |
| VC-10 Label-only mismatch | X-11 | Same label, different content identity | `refused` with `mismatch(distribution content identity)` | Yes. **Ran 2026-09-30 (§9.6): pass (model)** with a constructed identity (the binary was not run): `refused` with `mismatch(distribution content identity)`, no child | VER-003, VER-006 |
| VC-11 OI-008 review | §12 and the owner's decision | Review against ARC §3, priorities, M-6 | Decision source recorded; while OI-008 open the allocation criterion is **not met** | Review only | VER-004 |
| VC-12 Local-provider account | §8.1 | Compare claims to candidate observations | Rows labeled; L-4 observed; L-2/L-3 not observed; no substitution claimed | Partly (L-4 observed). At the RP-3 repair: L-2 and L-3 observed at one pair, MCP tools not delivered on that route (§10.1; F-31); L-4 widened by OB-9. Still no candidate and no substitution claim | VER-005 |
| VC-13 Upgrade comparison | Two pins | Run §9.5 | Diffs incl. generator divergence and experimental status; no adoption | Yes, once a second pin is named | VER-006 |
| VC-14 Settlement truthfulness | X-04/X-05/X-12 | Person answers; App rule declines; App rule attempts affirmative; second answer | Origins truthful; affirmative App-rule answer to an A14 or person-input kind refused `origin-not-permitted` (R9); App-rule content answer to `currentTime/read` accepted when the opt-in is declared; `already-settled`; write failure → `settle-write-failed` | Partly (X-12 with double). **Ran 2026-09-30 (§9.6): pass (model)** for `invalid-answer`, `origin-not-permitted`, the person's answer, `already-settled`, App-rule decline, `already-resolved`, `no-such-request`, `settle-write-failed` and `generation-closed`. X-04 and X-05 need a live turn | VER-001, VER-007 |
| VC-15 Act boundary review | §11, candidate statements | One-for-one review against CLM-004…006 and R-1 | Each act resolves to its owner; A14 never presented as A4–A7 or a checkpoint act; no invented sequence | Review only | VER-007 |
| VC-16 Frames during handshaking | X-01 (spike transcripts show `remoteControl/status/changed` before `initialized`) | Replay handshake | Early notification held in order under *g* and delivered at `ready`; not dropped (H4) | Yes (double). **Ran 2026-09-30 (§9.6): pass (model)**; also two server requests sent before `initialized`: entries at receipt (R1), unfamiliar one errored at once, delivery at `ready` in order | VER-001 |
| VC-17 Deliberate stop with descendants | X-13, fresh home | Start, then deliberate stop while the plugin fetch runs | App stop record marks the end deliberate (exit code 0 not used); surviving descendants detected and recorded; handling per U-16 | Yes, with owner visibility of the network fetch | VER-001 |
| VC-18 Supplier-internal decision | X-14, user sets `auto_review` | Trigger a tool-permission decision inside Codex | No register entry for an unreceived request; notifications delivered natively; origin `supplier-internal`; never shown as the person's answer | No (live turn) | VER-001, VER-007 |
| VC-19 Supplied-guidance evidence | Thread start carrying developer instructions; a workflow run-start `turn/start` text element (v0.9); a resume or fork carrying developer instructions | Inspect records per thread/turn | Content identity of each carried input recorded with request identity, generation and source identity; adoption not claimed (P-15 limitation); a resume or fork override recorded as *supplied, not applied at 0.158.0* (§8.2; F-33) | No (candidate; resume needs a thread). OBS-2 O-5 and OBS-3 W-4, W-6 observed the supplier side at one pairing | VER-003, VER-007 |
| VC-20 Classification by declared capabilities | Double; experimental opt-in false | Double raises `currentTime/read` and `attestation/generate` | Both `unfamiliar` → explicit error; with opt-in declared, `currentTime/read` becomes familiar | Yes (double). **Ran 2026-09-30 (§9.6): pass (model)**, and with `requestAttestation` declared: `attestation/generate` familiar, known-app-unsupported, explicit error by a named rule | VER-001, VER-002 |
| VC-21 Supplier refusal of an App request | Spike transcript (unknown client method → -32600) | Replay | Outcome `response-observed(error)`, not unknown; connection continues | Yes (transcript). **Ran 2026-09-30 (§9.6): pass (model)**: -32600 → `response-observed(error)`; the connection continued | VER-001 |
| VC-22 Answer origin by kind (R9) | Double; opt-in declared | App rule attempts a content answer to `item/tool/requestUserInput`, an affirmative answer to `item/fileChange/requestApproval`, a decline of an elicitation, and a content answer to `currentTime/read` | First two refused `origin-not-permitted`; decline recorded `app-rule:<name>`; `currentTime/read` answered `app-rule:<name>`; no answer presented as a checkpoint act | Yes (double). **Ran 2026-09-30 (§9.6): pass (model)** | VER-001, VER-007 |
| VC-23 Person-input answer is not act evidence (R4-12) | Double seeded with an elicitation request on a host-content subject | Person answers "yes, accepted" in the elicitation | Settlement `person-via-interaction`; delivered as conversation input only; no human-act record, no checkpoint satisfaction, host item stays queued | Yes (double). **Ran 2026-09-30 (§9.6): pass (model)**: no human-act record kind is emitted | VER-007 |
| VC-24 MCP surface classification (R4-12) | Double; status list, startup notification, `mcpToolCall` item, App-initiated `mcpServer/tool/call` | Replay each | Status `disabled` reported as App-side configuration, never A13; agent's `mcpToolCall` delivered natively; App-initiated call recorded with App initiator, never shown as the agent's call or as any person's act | Yes (double). **Ran 2026-09-30 (§9.6): pass (model)** | VER-001, VER-007 |
| VC-25 No hold claim (R4-2; R8-1) | **Phase 1:** a run with a reached checkpoint (DEL-02-03 records the arrival); a tool-permission request reaches the App; a second tool settled by the user's mode. **Governance phase:** held run of a governed checkpoint (DEL-02-03 state), same requests | **Phase 1:** a receiver attempts an App-initiated `mcpServer/tool/call` for the run. **Governance phase:** named App rule declines the first request; a receiver then attempts an App-initiated `mcpServer/tool/call` for the run | **Phase 1:** no run is reported holding; no named-rule decline and no `run-holding` refusal is made for the checkpoint; the call is handled by the ordinary §6.8 rules; both tools are delivered natively; no hold claimed and no hold-support value carried; `turn/interrupt` not sent. **Governance phase:** decline recorded `app-rule:<name>`; the auto-settled tool is delivered natively as completed; the App-initiated call is refused `run-holding` (HP-4); no hold claimed and no hold-support value raised; `turn/interrupt` not sent for the hold | Yes (double). **Ran 2026-09-30 (§9.6): pass (model)** in both parts; `turn/interrupt` never sent | VER-001, VER-007 |
| VC-26 Model destination facts (R4-1) | Thread start with a selected provider; a constructed re-route notification | Inspect S-4/S-7 facts | Requested and effective provider/model kept separate per turn; the re-route recorded on its turn; a turn with no supplier report carries *unknown*, never an earlier value; no gate on enablement; class taken from DEL-01-05's configuration | Partly (constructed re-route with a double; live start needs credential or local provider). **Ran 2026-09-30 (§9.6): pass (model)** for the constructed re-route under the §8.3 per-turn reading (U-27); the live part is OBS-1's: thread-level requested = reported, no re-route, no turn element (§10.1 OB-7) | VER-005 |
| VC-27 Lifecycle and register transition tables (v0.8) | Double; a scenario for every row | Drive every row of §4.7 and §6.2.1 | Every row is reached; the model refuses any transition outside the tables | Yes (double). **Ran 2026-09-30 (§9.6): pass (model)**: 23/23 LT rows, 13/13 RT rows; the tables in this file equal the model's | VER-001 |
| VC-28 Record formats (v0.8) | The three PROPOSED schemas, their fixtures and the records the model emits | Validate | Valid fixtures valid; invalid fixtures invalid (each for its stated reason); every emitted record valid | Yes. **Ran 2026-09-30: pass (model)**. Rerun at v0.9 (2026-10-02): pass (model), with the revised entry schema; its three new fixtures (secret values redacted, valid; secret values kept, invalid; actor form, invalid) give their stated results (§9.6) | VER-001, VER-003 |
| VC-29 Double fidelity (v0.8) | The eight committed transcripts | Replay each transcript's App frames against the double seeded from it, then against the double seeded from `A-bin-freshhome` | Supplier frames byte-identical and exit code 0; across seeds equal except `emittedAtMs`; constructed and mutated frames valid against the committed bundle | Yes. **Ran 2026-09-30: pass** (8/8 byte-identical; cross-seed equal) | VER-001, VER-002 |
| VC-30 Capability account completeness (v0.8; §8.4) | Committed bundles, `_spike/inventory.txt`, the recorded accepted-method list, the five TS-only names | Parse §8.4 | Each of 19 item kinds, 11 server-request kinds, 170 client methods and 85 notifications in exactly one group; variant and (obs) marks match the sources. The (obs) marks stay the spike's; OBS-1 and OBS-1b observations are in §10.1, not in the marks | Yes. **Ran 2026-09-30: pass**; rerun at the RP-3 repair: pass | OUT-002; DEP-02-01-025 |
| VC-31 Name-to-group mapping (RP-3 repair; R14-5) | WD-v0.8 §4.2.5 and this §8.4 | Resolve each portable name's group and every supplier name its row cites | Each of WD's ten names resolves to one Part A group; every cited supplier name that §8.4 places in a group is a member of that group | Yes. **Ran 2026-09-30: pass**, as DEL-02-01's prototype check S-11 (`wdproto.py selftest`), which reads this file | OUT-002; DEP-02-01-025 |
