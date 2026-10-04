# Operation-Policy and Human-Act Contract
- Contribution: DEL-04-01/ACT-POLICY-v0.11. It supersedes ACT-POLICY-v0.10 (sha256 1bf0ce8e413d2b8fb3825808e3ce50bf8c56584c8b40bdb990bc81d2863525c1, confirmed READY as part of E-1). ACT-POLICY-v0.10 superseded ACT-POLICY-v0.9 (last changed at `dc61150559`, sha256 4ef8c0428d42fbe37be634d79296d7ec80860308345bf4826650fef1739b2229). ACT-POLICY-v0.9 superseded ACT-POLICY-v0.8 (last changed at `153a7c533b` and unchanged at `ac9a68a7f2`, sha256 6fb6b9e883fa8d20da42c659de0485de0cb2a109a94c94364f16abde1dcc2b4a). ACT-POLICY-v0.8 superseded ACT-POLICY-v0.7 (last changed at `c896a99d90` and unchanged at `86cafc0e1c`, sha256 9fd34463dd7c9400f89da901543f8d41dcaad68f887264215428ad1682ad99fd). Earlier versions: v0.6 (last changed at `caa4334ca1` and unchanged at `3dd7c22c73`, sha256 6889003e6c1c2dd6d58b7145dd7955651debcc7b705a84e63aa6cd4e596e4815), v0.5 (last changed at `c6f81a4f2` and unchanged at `94aa9181b`, sha256 0057593adfde52044b70ccee1a85892754c2c9a62cf452214e94d810c6c43bd9), v0.4 (d6da05ab…b03b at `8fb51f07f`), v0.3 (b3748c02…8128), v0.2 (e50f1fe2…9a9), v0.1 (e6457535…3763).
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- **v0.11 change (R23-31.10, R23-21; run `APP-V4-DESIGN-PASS-4-20261003`, owner O-A, at O-E's request):** §10.3's DEL-10-03 row maps what DEL-10-03 RA-v0.1 reads (§2.1, §3, §8.2, §8.4). No other line changes; dependents pinned to v0.10 keep their pins (R23-21 item 3), since no rule, act or value changed.
- **v0.10 change (R23-8, R23-18, R23-21; run `APP-V4-DESIGN-PASS-4-20261003`, owner O-A):** A16 *decide*: §2.1 A16 row, A8's package elements, the A9 row's act list and the "no canonical name" list; §2.4 act kind; §2.5 binding row (R23-23); §4.1 A16 outside the closed list; §9 label "decide"; §10.1 V-01 (A1–A16); repairs RV E1-R2 and R23-25 (a later A16 on the same package). **Re-pin (R23-5):** ScopeOfWork.md sha256 2cd1dc9e542a9ee38ee0dd2a217bd717ecd960b2df009f59b4b2c562d350d862 (SCA-V4-003). Blocks read: G-0401-01…04. Bearing: G-0401-02 (REQ-002 keeps each act's actor, subject and evidence distinct and names A15 as a further person's act; A16 follows it and is not yet named there, listed for the next amendment under R23-11) and G-0401-03 (TBD-005: until a consequence vocabulary is adopted, a package's consequences are stated, not coded); G-0401-01 and -04 do not bear on these rows.
- Phase (R8-1; R9-1): in the current phase (Phase 1) declared checkpoints are **plan guidance** (§4.0). **In force in every phase:** the act is requested; it is recorded as done only when the person performs it; the reserved acts bind. **Phased to the governance layer:** holding the run until the act (PRD V4-WF-05 and HOST_INTEGRATION V4-HI-42 as amended by SCA-V4-001, quoted in §4.0; ScopeOfWork TBD-004). Hold support, re-hold, the carriage assurance of the checkpoint constraint and App-side holds are kept as the **governance-phase definition (retained)**, relabelled and not deleted (§4.3, §4.4, §4.6).
- Network-destination grant (R8-13; DECISION-5): granting a host's agent a network destination, by an allow-list edit or an in-work grant, is a **person-only act**. It is mapped as an **A12 grant change**, subclass **network-destination grant**, under D2 (e) (§2.7). An agent never performs it. The person-only grant is now in the accepted basis (PRD V4-HOST-02 and the ARCHITECTURE §4 host-agent properties, as amended by SCA-V4-001); the A12 mapping stays INTEGRATION (F-22).
- Policy-class record and act lifecycle (Wave B; R12-1…R12-3): a **PROPOSED** structure for the adopted policy-class configuration (OUT-002), `ACT_POLICY_CLASS_RECORD.schema.json` beside this file, with P-01…P-06 written as instances and validated by a local prototype (`prototype/`); one act-record lifecycle table (§2.8); the request → capture → record sequence (§4.7); A15 register workflow revision (§2.1; R12-5); a PROPOSED consequence vocabulary for the owner's phase review (§8.5). Nothing in these is accepted, and no placement is chosen (OI-013, OI-014; R12-2).
- Serves: OUT-001, OUT-002, OUT-003; REQ-001…REQ-007; VER-001…VER-009 (AC-001…AC-009). ScopeOfWork TBD-004 (added by SCA-V4-001) limits the VER-001 and VER-006 checkpoint cases to recording in the current phase (VC-001, VC-006, VC-010).
- Basis (re-pinned at v0.7; R9-5):
  - The accepted basis as amended by SCA-V4-001 (`P/execution/_ScopeChange/SCA-V4-001_2026-09-28_2155/`) and SCA-V4-002 (`P/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/`), by current sha256: `P/docs/PRD.md` bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd; `P/docs/ARCHITECTURE.md` 317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c; `P/docs/HOST_INTEGRATION.md` d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f; `P/docs/EXAMINATION.md` 471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0. Of the requirement texts this file cites, V4-WF-05, V4-HI-42, V4-HI-70, V4-EXM-22, V4-HOST-02 and V4-ARC-12 (with the host-agent properties) were amended and V4-EXM-23 was added; the others are unchanged since repo `6e18505e3`, the v0.6 basis (checked with `git diff 6e18505e3 HEAD -- docs/`).
  - ScopeOfWork.md sha256 ac043e54e396f9155e3d1b02d61ca7333350a812c7db3d5bb26c80d6fc3bb875, as revised by SCA-V4-001 (AX-005; TBD-004 added) and unchanged by SCA-V4-002.
  - `P/docs/PRD.md` §2.2 (V4-HOST-02), §4.1 (V4-WF-02, -05), §4.3 (V4-EXE-01, -02), §4.5 (V4-AUT-01…05), §4.7 (V4-REC-05), §9 (OQ-02, OQ-11), §10.
  - `P/docs/HOST_INTEGRATION.md` §2 (V4-HI-02, -04), §3 (V4-HI-11, -12), §4 (V4-HI-20…25), §5 (V4-HI-30…33), §6 (V4-HI-40…42), §7 (V4-HI-50…52), §9 (V4-HI-70/71).
  - `P/docs/ARCHITECTURE.md` §4 (V4-ARC-12 and the host-agent properties), for §2.7.
  - `P/docs/EXAMINATION.md` V4-EXM-20, -21, -22, -23, -25, -31.
  - `P/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/DECISION_BRIEF.html#d3` (sha256 02d38cb18041c52989d8a2a0b969e6502ce4b25eec85fb0931bbbc100c4420e8).
  - `P/conceptual/DECISIONS.md` OD-05, D-04; `P/conceptual/EXEMPLARS_AND_LESSONS.md` X-09, X-19, X-20.
  - `P/execution/_Decomposition/Open_Issues.csv` OI-001, OI-002, OI-013, OI-014, OI-021; `External_Dependencies.csv` DEP-001.
  - Owner decisions `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3` (host joins deferred), `-DECISION-4` with its clarification (D4-1 phased checkpoints; reserved acts stand; the principle applies to a host's embedded loop) and `-DECISION-5` (host-agent network destinations): `OWNER_DECISIONS.md`, current sha256 5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2. The v0.6 pass read DECISION-3 and DECISION-4 in its state at `94aa9181b` (sha256 a5ccab0d39bd1cab37c5556abc9bdedd5341ce76be4712706c8c9d72d623e776).
  - Owner confirmations at the amendment checkpoints: run `APP-V4-BASIS-ALIGN-20260928`, `OWNER_DECISIONS.md` sha256 ca8c4e50df1d7dddb41b875a4afe46eea4f1a1bf2491d255b7890d0d71cd254b (DECISION-7 accepts `AMENDMENT_PACKET/OWNER_ITEMS.md`, sha256 2b90eb4a95f458e993eed69e27533aa10e31aea980fe2ec99c9c2345e6f498ef, "as recommended": O-4, O-6, O-10, O-15, O-17, O-25); run `APP-V4-SCA002-20260929`, `OWNER_DECISIONS.md` sha256 36ffcbbea923504581844456751c2eb3db617b5471a3595e63f036bf0634b480 (DECISION-2 accepts its `OWNER_ITEMS.md`, sha256 1d46458c966b6cc41be361eb2ddbc75df409bcc43202aff17478b81438ca51a8: Q-5 option A).
  - Accepted graph: `P/execution/_DAG/_LATEST.md` (sha256 4d381ba4e87b41a83b9d0d2dc591c4bf04eacb84df0b5c27314091cd2a992f56) → DAG-003.
- **Consumed inputs for v0.9 (node F-C of run `APP-V4-DESIGN-PASS-3-20261001`; read from the working tree at `ac9a68a7f2`; paths under `AgentRuns/APP-V4-DESIGN-PASS-3-20261001/`; sha256 first 16 hex).** `BRIEFS.md` `316ea29325a0d450` ("F — first-increment edits"); `R17_RESOLUTIONS.md` `b0af81bcbad9bc52` (R17-6, R17-11, R17-14); `R18_RESOLUTIONS.md` `abf5eee6324647ff` (R18-1 C-01, C-21); `R19_RESOLUTIONS.md` `16930ecdcead7511` (R19-4 L-4); `OWNER_DECISIONS.md` `ea96c55710af41c9` (DECISION-K3 revised: K-7, K-8; DECISION-L L-4); `F/F0_JOINS.md` `e93608be1c6e3eb0` (§1.4 FA-01…FA-08, §1.14). `R20_RESOLUTIONS.md` `91fff5a3f6277d78`; the round-2 join lists of `D/D3.md` (J-A3, J-E2) and `D/D5.md` (J-35). New Design files by v0.2 label and section (stepped in parallel; WR was read at v0.2, AAC and NIR at v0.1, whose section numbers are cited, and F-E checks them): DEL-01-04/AAC-v0.2 §1.2, §4.2, §5.2; DEL-01-04/NIR-v0.2 §4, §8, §9; DEL-02-02/WR-v0.2 §3, §4.3, §4.6, §9. DEL-04-03/RS-v0.9 was revised by this executor in the same node (§6.1, HA-10). No policy-class record changes at v0.9, so `ACT_POLICY_CLASS_RECORD.*` and the policy revision label are unchanged (§8.1).
- **Consumed inputs for v0.8 (Wave B of run `APP-V4-DESIGN-PASS-2-20260930`, node B4; read from the working tree on commit `86cafc0e1c`; paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/`).** `BRIEFS.md` sha256 ccb4d9f036fb7ff531fffa0d309533b15cf1ebb39b0320651ed4bd5d88efc550 ("Common rules"; "Wave B — design development", row B4); `R12_RESOLUTIONS.md` sha256 95f3011b436b6faa3de098059e77eac836c165e0bb98a5ed94e28918a3a749a1 (R12-1…R12-10; binding); `OWNER_DECISIONS.md` sha256 1dfd5bf4619b329719136b1646030e3f871fd7ffc52dbfd12265414e515aaf15 (DECISION-K1, with the later model-download record; supersedes for currency the pin in the node A4 line below); `SURVEY/S1-A.md` sha256 87baa03d7cbc9b0a6b8e8543d8cd80a7d71c754da80fbfdc053c8e6ef21045f6 (§1.5, §1.8 items 7–8; advice, checked against the current text); `DECISION_BRIEF.html#d3` (sha256 02d38cb18041c52989d8a2a0b969e6502ce4b25eec85fb0931bbbc100c4420e8 as pinned above; its "Reconsider when" line names the four dimensions of §8.5); DEL-02-02 ScopeOfWork REQ-002, AC-002, AC-006 (A15, R12-5). Siblings by label and section (R9-5): DEL-03-01/C-v0.7 §3.1 (element 8); DEL-02-03/EXEC-v0.5 §2.1 PH-6, §5 CAP-1…CAP-9. AS-v0.8 and RS-v0.8 were revised by this executor in the same node.
- **Pins as of node A4 of this run's records (run `APP-V4-DESIGN-PASS-2-20260930`; in place, no version bump; R11-3; relabelled at RQ, V19-B n-1: later pins of the same records are in the Wave B input lines and in GUIDE's basis).** Each sha256 recomputed with `shasum -a 256` in the working tree at this pass; paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/`: `R9_RESOLUTIONS.md` sha256 a64e241519b7d158165a7ede0ffdd22eec0af15b6812b5300755f5f38abd59b8 (R9-1…R9-11; R9-2's second bullet as corrected by R10-1); `R10_RESOLUTIONS.md` sha256 ad3b6caa4a12660db77abc51b5c02ba70519ee46d55b40d21ee76eb3ca561796 (R10-1…R10-11); `R11_RESOLUTIONS.md` sha256 e7343b6663b6aeeb2dc506d3391f5b310088e7688d1b21e65d2ba1d8616b3615 (R11-1…R11-9, the repairs from review V17); `OWNER_DECISIONS.md` sha256 7458e9e81971676337a34280b4e8b29a7d04fce5fc202da5b9f5cf7ccd8f9ae5 (DECISION-K1). At node A4 these superseded for currency the earlier pins of the same records in this header and in the change-table rows, which record the bytes read at node A1 or A3.
- Consumed inputs for v0.7 (Wave A of run `APP-V4-DESIGN-PASS-2-20260930`, node A1-A; read from the working tree on commit `3dd7c22c73`). Paths are under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/` unless stated:
  - `R9_RESOLUTIONS.md` (sha256 c3efe2ffa232dd9293202d4fc891eba4325afeb2e224fecdf8c1b4c5122a9d2c): R9-1…R9-11 (binding). `BRIEFS.md` (sha256 698d91d8217cee528812529fa353faac899b4bc1a5be5686552ad88dad6c469a): "Common rules" and "A1 — alignment wave", row A1-A. `SURVEY/S1-A.md` (sha256 87baa03d7cbc9b0a6b8e8543d8cd80a7d71c754da80fbfdc053c8e6ef21045f6): advice; each item applied was checked against the current source.
  - Rulings R1–R8, by file: `R1_RESOLUTIONS.md`…`R7_RESOLUTIONS.md` in `AgentRuns/APP-V4-FIRST-INCREMENT-20260928/`, and `R8_RESOLUTIONS.md` in `AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/` at its current sha256 44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b. They stand except where R9 amends them: R9-2 restates R8-11 item 2 and R8-12 item 2.
  - SWBPIPE's answers, DEL-09-06 `Design/RELAY_ANSWERS_SWBPIPE.md`, at its current sha256 afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74. The v0.6 pass read the state 6f01add3…61c7; three answer lines differ between the two states (in SQ-04, SQ-09 and P7; `git diff 94aa9181b HEAD`), and none is a statement this file cites. Data about SWBPIPE's current state, not commitments (DECISION-3).
  - Sibling Design files, cited by version label and section only (R9-5); their bytes are pinned in GUIDE's input table alone. Wave A labels (R9-11): DEL-02-03/EXEC-v0.5; DEL-02-01/WD-v0.7; DEL-02-01/WD-EX-v0.7; DEL-03-01/C-v0.7; DEL-03-02/P-v0.7; DEL-03-03/ADAPTER-v0.5; DEL-03-04/GUIDE-v0.4; DEL-04-02/AS-v0.7; DEL-04-03/RS-v0.7; DEL-05-01/LOOP-v0.7; DEL-05-02/PANEL-v0.7; DEL-01-01/HOSTING-BOUNDARY-v0.7; DEL-01-01/PIN-SPIKE-v0.1; DEL-09-06/CA-v0.5; DEL-09-09/XT-v0.5; DEL-09-06/RELAY-v0.3. The Wave A executors edit in parallel, so the label is cited and nothing here relies on another executor's Wave A text; AS-v0.7 and RS-v0.7 were revised by this executor.
  - The byte pins in the consumed-input lines below are true records of what each earlier pass read. They are history, not current pins.
- Consumed inputs for the R8-13 pass: **R8-13 pass (node B1; in place, no version bump).** OWNER_DECISIONS.md sha256 5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2 (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`: V4-HOST-02, host-agent network destinations) and R8_RESOLUTIONS.md sha256 44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b (R8-13) at `1528a5033`; OWNER_DECISIONS.md in its state that adds the owner's DECISION-5 confirmation (committed with this pass); BRIEFS.md sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517 ("Common rules", "A-wave"). Revised in the same pass (node B1), versions unchanged: LOOP, PANEL, ACT, AS, RS, HOSTING, C, ADAPTER and GUIDE; their byte pins are in GUIDE-v0.3's input table.
- Consumed inputs for the R8-12 closing pass: **R8-12 closing pass (node A6; in place, no version bump).** R8_RESOLUTIONS.md sha256 d4c3423310a857af86692d17ddfdd22fa877ee20b07c46e1ee481d1cd750e7af (R8-12, items 1 and 7 applied here). Current sibling versions after R8, as committed at `7a1508452` with A6's in-place R8-12 edits (their byte pins are in GUIDE-v0.3's input table): DEL-02-03/EXEC-v0.4; DEL-02-01/WD-v0.6; DEL-02-01/WD-EX-v0.6; DEL-03-01/C-v0.6; DEL-03-02/P-v0.6; DEL-03-03/ADAPTER-v0.4; DEL-03-04/GUIDE-v0.3; DEL-04-02/AS-v0.6; DEL-04-03/RS-v0.6; DEL-05-01/LOOP-v0.6; DEL-05-02/PANEL-v0.6; DEL-01-01/HOSTING-BOUNDARY-v0.6; DEL-01-01/PIN-SPIKE-v0.1; DEL-09-06/CA-v0.4; DEL-09-09/XT-v0.4; DEL-09-06/RELAY-v0.3. SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` and `FACTS_SQ01_SQ32.md` are unchanged (data about SWBPIPE's current state, not commitments; DECISION-3).
- Consumed inputs for v0.6 (R8 pass, node A2), read with `git show` from commit `94aa9181b` (scratch copies in a private folder). Paths are under `AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/` unless stated:
  - `R8_RESOLUTIONS.md` (sha256 1770c96e62caf14322811fca82ceb77eca450d3e1be8665cdbdd5550631e8d02): R8-1…R8-7, R8-10 and R8-11 (binding). R8-11 confirms PH-6 and PH-8 and settles the Phase-1 standing of D2's checkpoint half.
  - `INTAKE_MAP.md` (I2; sha256 3cc182955c0f3dd70efa0f1c051870229c2ccc08f36c5cf1445f2eef0dd1ea33): rows 01.5, 01.6, 02.8, 03.12, 04.4, 05.1, 05.2, 06.3, 13.6, 21.1, 28.1 and X.5; Part 2 P2.1, P2.7, P2.13, P2.14, P2.16, P2.17 and P2.18, and its §2.2 ACT rows; Part 3 items 1, 3, 4 and 10; Part 4.9 and 4.11. R8 overrides I2 where they differ.
  - `BRIEFS.md` (sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517): "Common rules" and "A-wave".
  - Owner files, revised first in the same pass: DEL-02-03/EXEC-v0.4 `EXECUTION_COMPATIBILITY.md` (sha256 d32be37797a3c367d342a2d13bbb8dd4279bc52934531d83b8c6ec8c6e7b76d4): §2.1 PH-1…PH-10, §2.2 GV-1…GV-5, §2.3, §3.5, §3.6, §4.5 SP-4, §4.7, §4.11 receiving notes, §7.2, U-E24. DEL-02-01/WD-v0.6 `WORKFLOW_DECLARATION.md` (sha256 fce565edfd0cee3fa4583eb292d11cce3e4121ead0cdbed31ba2fe0a52562f28): §4.3.0 CG-1…CG-7, §4.3.1 `governed`. WD-EX-v0.6 `EXAMPLES.md` (sha256 950b70b2e3f7fdda9a98b13a63746b76936be490dd96cb6e47bbe6dc9c3eba3d).
  - SWBPIPE's delivered answers, DEL-09-06 `Design/RELAY_ANSWERS_SWBPIPE.md` (#1047; sha256 6f01add3977761e42ac6b310faf72ba4fd5455e478605deb83fefb2e4d3a61c7): SQ-01, SQ-02, SQ-03, SQ-04, SQ-05, SQ-06, SQ-07, SQ-09, SQ-10, SQ-11, SQ-13, SQ-20, SQ-21, SQ-23, SQ-28, SQ-31 and ANS §2. These are data about SWBPIPE's current state (relayed; answered 2026-09-28), not commitments. No host evidence, commitment or contribution is received (DEP-001; DECISION-3).
- Consumed inputs for v0.5, read with `git show` from commit `8fb51f07f` (the working tree was not used; scratch copies were kept in a private folder). Paths are under `AgentRuns/APP-V4-FIRST-INCREMENT-20260928/` unless stated:
  - `R5_RESOLUTIONS.md` (sha256 254d0b93b9959419a70c6737b07087e1db59b529adc3105a1db31f82b78dd6f1). This file's items are R5-1, R5-2, R5-3, R5-4 (relabel), R5-6, R5-7 and R5-9, plus the R5-5 consequence for §4.3.
  - `reviews/V3-A.md` (sha256 f25f5af1177b7fe2a698bd4ef1e1caafa4c2ef25cfc73111f031e17c7cc21d87): MAJOR-1, MAJOR-5; m-2, m-3, m-5, m-6, m-7, m-11, m-12 and m-13.
  - `reviews/V3-B.md` (sha256 5662fbd09025f5ad9459861370159d606fcced76b394980199e861555a1954a3): the FX-50/U-X3 note; the ACT U-04/U-06 coverage in RELAY.
  - Current sibling versions:
    - DEL-03-01/C-v0.4 (sha256 e929d39d3ff9515702f9bfe51dfada537e1cbd165146ec0de4ccf629c659a08c), §10: FXA-1…FXA-5 (renamed from FA-n), LIB-A1, LIB-A2, AF-1, V-ED1;
    - DEL-02-03/EXEC-v0.2 (sha256 7f7848c0de2fdb4dc21f5adafa97f92e179bb66c9f6b04f3434d8f2342317af0), §3.6 (answer to U-X3), §4.5, §4.7, §4.9, §4.10, §5;
    - DEL-03-03/ADAPTER-v0.2 (sha256 a2905dda5782d7a48fa35ef7e26b0c1517fd3bd995e3ddbba27d2426a25674bc), §3.3 E-2…E-4, §5.1–§5.3 GC-2/GC-3;
    - DEL-02-01/WD-v0.4 (sha256 e492ff635de972466c8a932355beeae848e1f3d3f60de7304e88963352d8e88e), §4.3.1 (grant-setting row), FB-17, VC-41;
    - WD-EX-v0.4 E1d `CP-grant`, as cited by R5-7.
  - V-GR1, fixed by R5-7, is present in C-v0.5 §10.4, with GR-1…GR-3 and GR-P/GR-R/GR-S (V4-A m-1; R6-4).
- Consumed inputs carried from v0.4, read from commit `f05c7e4cd`:
  - `R4_RESOLUTIONS.md` (sha256 50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24). This file owns R4-2 (hold support), R4-3, R4-4, R4-5, R4-6, R4-9, R4-13, R4-14, R4-17, R4-18 and the R4-19 minors addressed to ACT.
  - `R3_RESOLUTIONS.md` (sha256 202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf): R3-1, R3-2, R3-4, applied in v0.3 (V2 m-9).
  - `OWNER_DECISIONS.md` at `f05c7e4cd` (sha256 a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c). It carries DECISION-1 and `APP-V4-FIRST-INCREMENT-20260928-DECISION-2`. Under D5, host content may flow to the selected model with no gating; that is SETTLED. Recording and showing the model destination is **INTEGRATION (DECISION-2 reading)** (R5-4). D6 is deferred to SWBPIPE SQ-02.
  - `reviews/V2.md` (sha256 75ba1dff8a0c4fa2eb294471127147cbd19a0925daf9169b32ddc88727dde6ef): MAJOR-1 and m-4, m-6, m-7, m-9, m-11, m-12, m-13.
  - DEL-02-03/EXEC-v0.1 `EXECUTION_COMPATIBILITY.md` (sha256 e0ede76ebf08003511755afc666be2466a867fd3256837ee94300cd0dfe518e8): §2 HP-1…HP-3, §3.6, §4.2 HD-5, §4.5 SP-1…SP-8, §4.7 RH-1…RH-9, §4.9 RE-1…RE-5, §4.10 AR-1…AR-4, §4.11, §5 CAP-1…CAP-9, and findings F-2…F-5 and F-13.
  - DEL-03-03/ADAPTER-v0.1 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` (sha256 58b2409ca45ceea66160eb8910ca38b76b6f335dc184eaeb0896e93cabd0a074): §3.2, §3.3 E-1…E-9, §5.1–§5.3 carriage assurance and GC-1…GC-5, and findings F-1, F-2, F-4 (U-X1) and F-5.
  - DEL-03-01/C-v0.3 `CATALOG_AND_READ_BASIS.md` (sha256 ba45e7393ee0b16780f36605ddeecb95ba1f181488e36a46b4b495b69fd67c26): §10 FX-PIPE-01, which comprises:
    - FA-1…FA-5;
    - OP-C1…C12;
    - steps T1–T17, including T4a and T16a;
    - variants V-S1, V-CP1, V-NP1, V-R1, V-X1 and V-OU1;
    - §10.7.
- Consumed inputs carried from v0.3, read from commit `28bd00499`:
  - Owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (D2 = OI-001, D3 = OI-002): `OWNER_DECISIONS.md` as then committed (sha256 f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e).
  - `R1_RESOLUTIONS.md` (sha256 2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4).
  - `R2_RESOLUTIONS.md` (sha256 77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088). This file owns R2-1…R2-11 and the DEL-04-01 parts of R2-15…R2-21.
  - `reviews/IR1-A.md` (sha256 31b3c7f8493f05ee5fed6a11208f6811d2449d8a4fe72aae6300c2850b648284), all items addressed to DEL-04-01.
  - `reviews/IR1-B.md` §2.6 (B-M1, B-M9) and `reviews/IR1-C.md` IR1C-06, -07, -10, -22 and X-10, for items naming DEL-04-01.
  - V1-A/B/C, as in v0.2.
  - Sibling v0.2 text:
    - DEL-03-01/C-v0.2 `CATALOG_AND_READ_BASIS.md` (sha256 358182b18b1fe13f9af6e6f5a61c9ed57f91b6ab29ea0c9adab06fe0081d6d82), §2, §3.1, §4.1, §10 (shared fixture FX-PIPE-01, T1–T17, OP-C1…C9);
    - DEL-02-01/WD-v0.2 `WORKFLOW_DECLARATION.md` (sha256 c25bccc5f3ac02c84522148eeaa8a6ef0f5eb4a380686773cff45f57a448a55c), §4.3 and FB-03/FB-04.
  - Fixture IDs OP-C10 and OP-C11 were fixed by R2-21. They are defined in C-v0.3, which closes v0.3 F-13.
- Receivers (rebuilt from the ACTIVE register rows at v0.7; R9-6; the table is §10.3):
  - With a local DOWNSTREAM row in `Dependencies.csv` (DEP-04-01-012…016 and -022…027), each mirroring the consumer's own UPSTREAM row: DEL-02-01, DEL-02-03, DEL-03-01, DEL-04-02, DEL-04-03, DEL-03-02, DEL-03-03, DEL-03-04, DEL-05-01, DEL-05-02, DEL-09-09.
  - Declared upstream in the consumer's own register only:
    - DEL-09-06 (DEP-09-06-030);
    - outside the first increment: DEL-01-02 (DEP-01-02-021), DEL-01-04 (DEP-01-04-011), DEL-02-02 (DEP-02-02-016), DEL-06-02 (DEP-06-02-009), DEL-09-02 (DEP-09-02-018), DEL-09-05 (DEP-09-05-009), DEL-09-12 (DEP-09-12-011), DEL-10-03 (DEP-10-03-013).
  - DAG-003 admits all twenty arcs. Satisfaction is read from the live registers; no row records it as satisfied.
  - DEL-01-01 uses the D3 value (V-21, V-25). No register row carries that use.
  - The arcs N-18, N-21, N-24 and X-1 have no end at DEL-04-01.
  - DEL-04-01 is not a SCC-CASE-002 member.

`P` = `projects/chirality-app-v4`. Every element name in this document is a
**semantic name, not a wire name**. Examples: *act kind*, *decision actor*,
*recorder*, *recording mode*, *change-item content identity*, *treatment*,
*grant value*.

This definition selects none of the following:
- field names or types;
- transport;
- hash or canonicalization algorithm;
- persistence;
- process or shared-component placement (OI-013, OI-014).

Anything still open appears only as `UNRESOLVED{…}` or as a named relay
question. It is never a permission, a default or a pass.

---

## Changes from v0.8

Node F-C of run `APP-V4-DESIGN-PASS-3-20261001`. Row IDs are F0's
(`F/F0_JOINS.md` §1.4, §1.14) and the rulings that decide them. No rule of
this contract changes; the capturing surface and the A15 relations are
re-pointed to the designs of DEL-01-04 and DEL-02-02, and one fixture case
is added. No policy record changes.

| Row | Change in v0.9 | Where |
|---|---|---|
| **FA-01** (D3 J-A1; R17-6) | A4, A6, A7 on App content: the capturing surface is the App act control **designed in DEL-01-04/AAC-v0.2** (PROPOSED until SCA-V4-003 carries SC2-01-04-1), not "built by DEL-01-04 in a later undertaking" | §2.6 |
| **FA-02** (D3 J-A2 = D5 J-20; K-7, K-8) | A15's capturing surface is **DEL-01-04's App act control**, composed from DEL-02-02's A15 descriptor (WR-v0.2 §4.3 RB-4; AAC-v0.2 §4.2). Never evidence: "a trial in conversation (K-7: drafts are not run)" replaces "a successful trial run"; "a registration ledger line without a capture" is added; an entry recognized as a shipped revision takes no A15 (L-4) | §2.6 |
| **FA-03** (D5 J-18; D3 J-A2) | §2.1 A15: evidence from DEL-01-04's act control (K-8; R17-6) from the A15 descriptor; content "the revision identity (equal to the reviewed draft's content identity, WR ID-2) and, for a new revision, the prior revision (R17-11)"; purpose "make it available in the project library" or "… in the user library" (as AAC already says). F0's "also L112" is the v0.8 change-history row and stays as history | §2.1 |
| **FA-04** (D3 J-A3 = D5 J-19; **C-01**) | §2.5 A15 row: bound content with **reviewed draft** ⟨draft, content identity⟩ and **prior revision** ⟨workflow tuple, or none⟩, in RS-v0.9's form (C-01); WD's derived-from is not this act's relation (R17-11; C-21) | §2.5 |
| **L-4** (DECISION-L; R19-4; D3 J-A3, J-E2; D5 J-35, round 2) | One A15 may register several library entries in place, each entry's bytes and prior revision bound, as a batch A5 lists several items (RS-v0.9 §6.1 *registered entries*; WR-v0.2 §4.7, entries in ID-3's `entry:` form); an entry byte-equal to a shipped revision is recognized and takes none | §2.1; §2.5; §2.6; new FX-58 |
| **FA-05** (D3 J-A2 = D5 J-24) | §4.7 RC-3 "the App act control (DEL-01-04) for A15"; the A15 paragraph: the act control captures the A15 and the record binds the revision identity, the reviewed draft content and, for a new revision, the prior revision; the registration outcome is reported beside the act (AAC AK-f) | §4.7 |
| **FA-06** (D3 J-A4; R17-14) | §10.3 DEL-01-04 row gains its receiving side: NIR-v0.2 §8 (V-01, V-07, V-08), §4 (V-21), §9 with AS's facets (V-05); AAC-v0.2 §1.2 (V-01 act kinds and wording) | §10.3 |
| **FA-07** (D5 J-25) | §10.3 DEL-02-02 row: "§2.1 A15, §2.5, §2.6, §4.7, FX-56, FX-58 (WR-v0.2 §4.3, §9)", replacing "Not mapped in detail (U-08)" | §10.3 |
| **FA-08** (D5 J-26; F0 sweep L1651, L1947) | FX-56 (a) "at the App act control (DEL-01-04)", with reviewed draft d-12 and no prior revision; (b), (c) stand (WR P-08, P-15 run them on doubles). V-01's "A15 also DEL-02-02 (later, D1)" and U-08's owner cell refreshed; §12 item 6 and the §10.3 note likewise | §13 FX-56; §10.1 V-01; §10.3; §12; UNRESOLVED U-08 |
| Verification | New FX-58 (several entries in one act; shipped revision recognized; one entry changed after review). VC-002, VC-004 and VC-009 include it. Prototype `validate_policy.py` rerun 2026-10-02: all held | §13; Verification cases |
| RV21 (repairs from review V21 of run `APP-V4-DESIGN-PASS-3-20261001`; in place, no version step; V21-B m-9, F-E2 §4.3 row 10) | §2.6 names the amendment item as EXEC, AAC, D3 and GUIDE do: "SC2-01-04-1 as amended by SC3-01-04-1" (SC3-01-04-1 amends the pass-2 proposal for L-4 and A15, D3 §5). FA-01 above keeps the words then used. No rule, record or fixture changes; `validate_policy.py` rerun 2026-10-02: all expectations held | §2.6 |

## Changes from v0.7

Wave B of run `APP-V4-DESIGN-PASS-2-20260930` (node B4): design development
under R12-1…R12-3. Item IDs are the survey items of `SURVEY/S1-A.md` §1.8
("ACT n") and the R12 rulings. Every new structure is PROPOSED unless a
cited text decides it.

| Item | Change in v0.8 | Where |
|---|---|---|
| **ACT 7** (OUT-002; U-12) | The policy-class record gets a PROPOSED structure: a configuration {format, version, policy revision (label and content identity with method), records, decision records}; each record with a role (catalog class · treatment rule · tool-permission setting), coverage, class value, default, widenable, granularity, actors, consequence, decision basis, standing, host adoption and phase note. A catalog entry refers to a record as {policy revision label, record identity}. P-01, P-01a and P-02…P-06 are written as instances. JSON Schema 2020-12 `ACT_POLICY_CLASS_RECORD.schema.json` with the instances and three invalid records; validated by `prototype/validate_policy.py`. Placement stays open (U-12) | §8.1, §8.3; new schema and example files; `prototype/` |
| **ACT 7** | One act-record lifecycle table (captured … recorded … answering … lapsed / partially lapsed / superseded … after run end … corrected), with the per-arrival relations kept apart from the record's own states | new §2.8 |
| **ACT 7** | The request → capture → record sequence, for acts on App content, on host content, A12 and A15, with the failure behaviour at each step | new §4.7 |
| **ACT 8** (U-02) | A PROPOSED consequence vocabulary drafted from d3's four dimensions (effect · reversibility · available examination · intended delegation), for the owner's phase review. It assigns nothing: every record keeps "not assigned" while U-02 is open | new §8.5; §5.1; §10.2 V-23 |
| **R12-5** | **A15 register workflow revision** added to the act table (subject: a workflow revision; content: the revision identity and the draft it derives from; purpose: make it available in the project), with its capturing surface, binding (not lapse-evaluated) and RS record kind. Source DEL-02-02 AC-006. Not checkpoint-requirable in this increment (a possible extension, PROPOSED). U-08 closed | §2.1, §2.4, §2.5, §2.6, §4.1, §10.1 V-01, §12 item 6, §13 FX-56, UNRESOLVED |
| **R12-10** | One wording: "prior act on this subject, not counted" becomes **"prior act not counted"**, as RS-v0.8 L-13 fixes it (with its reason). History rows keep the words then used | §2.3, §4.5, §13 FX-40, FX-45, FX-51 |
| RS 5 join | AP-5 and AP-12 point to RS R16, the record element for the agent's request | §4.0 |
| **B5** (node B5, round 2; LOOP-v0.8 §5.3) | §2.7 joined to the one destination flow: the agent's request is a call to the host's destination request entry carrying the call it needs ("the requesting call" of ND-A2, ND-A3), its A8 mapping DERIVED from §2.1 as AP-12; the decline row states the result class and that recording it as a destination entry is PROPOSED (R12-10); the non-stateless row cites DF-3 A-3, DF-6 and the evidence rule DF-7. §4.7's A12 paragraph points to DF-5 and the DF-F rows | §2.7; §4.7 |
| Verification | New VC-012 (schema and instances); VC-007 traces V-29; VC-009 reconciles FX-01…57 | Verification cases |
| RP-4: V18-2 m-11 | §4.1's examples of recognized kinds outside the closed list now name A15, as its own bullet already rules (WD-v0.8 FB-03) | §4.1 |
| RQ (repairs from V19; in place, no version bump) | V19-A m-3: live citations moved to Wave B labels (LOOP-v0.8 §5.1.1; EXEC-v0.6 §2.1, §4; WD-v0.8 §4.3.0, §4.3.1; fixtures "carried in C-v0.8"); history and origin citations kept. V19-A m-5: §8.5's consequence codes renamed while PROPOSED, CE-n, CR-n, CX-n, CD-n → **CQ-E0…CQ-E5, CQ-R0…CQ-R4, CQ-X0…CQ-X4, CQ-D1…CQ-D4** (they shared EXEC's CE kinds, EXEC's CR elements and C's CX-1), in text, schema and the invalid example; no meaning changed. V19-A n-3: LC-2 cites RS FC-1 for the late write and RS §6.1 for faithful recording. V19-B n-1: the node-A4 pins bullet relabelled "as of node A4" | Header; §2.8 LC-2; §2.7; §4.0; AP-10; §7; §8.5; §13; `ACT_POLICY_CLASS_RECORD.schema.json`; `ACT_POLICY_CLASS_RECORD.invalid.examples.json` |
| G (items the closeout returned to the graph; `R16_RESOLUTIONS.md`; in place, no version bump) | **R16-1:** §2.7's *Decline* row: recording the decline as an RS R15 destination entry is SETTLED by DEL-04-03's ScopeOfWork CLM-004 ("destination declined" from DEL-05-01), correcting R12-10's first bullet (it was PROPOSED). The act-declined event stays INTEGRATION; the report to the agent, "destination not allowed by the person", is unchanged. The B5 row above is history | §2.7 |

## Changes from v0.6

Wave A of run `APP-V4-DESIGN-PASS-2-20260930` (node A1-A): alignment to the
amended basis and the revised ScopeOfWork under R9-1…R9-11. It adds no new
design content. Survey items are those of `SURVEY/S1-A.md` §1.

| R9 ID (survey item) | Change in v0.7 | Where |
|---|---|---|
| **R9-5**, R9-11 (ACT 1; A-P1, A-P2, A-P5…A-P9) | Version v0.7. The basis is re-pinned from repo `6e18505e3` and ScopeOfWork `fc1a0503…f5e6` to the four basis documents by sha256, as amended by SCA-V4-001 and SCA-V4-002, and to ScopeOfWork `ac043e54…b875` (SCA-V4-001; TBD-004 and AX-005). A new consumed-input block for v0.7 names R9, R1–R8 by file with R8 at its current sha256, SWBPIPE's answers at `afb6e063…`, `_DAG/_LATEST.md` → DAG-003, and the siblings by Wave A version label only. The earlier consumed-input lines are kept as history. Body citations of the current sibling texts move to the Wave A labels (EXEC-v0.5, WD-v0.7, LOOP-v0.7, C-v0.7) | Header; §2.7, §4, §4.0, §7, §13 |
| **R9-6** (ACT 1, ACT 5; A-P10; F-1) | Receivers are rebuilt from the registers: eleven local DOWNSTREAM rows (DEP-04-01-012…016, -022…027) and nine consumers that declare DEL-04-01 upstream in their own registers only. §10.3 becomes the receiver table by register row. DEL-03-04 and DEL-09-06 are mapped. The retired rows DEP-05-02-014 and -015 are no longer cited | Header, §10.1, §10.3 |
| **R9-1** (ACT 2; A-P3, A-P4) | V4-WF-05 and V4-HI-42 are quoted as amended by SCA-V4-001. The description of V4-WF-05 by halves and the markers that awaited a basis update are removed, and V4-HI-42 is no longer described as guidance in Phase 1. In force in every phase: the act is requested; it is recorded as done only when the person performs it; the reserved acts bind. Phased to the governance layer: holding the run until the act. F-16 cites the amended V4-EXM-22 | Header, §1 labels, §3 S9, §4.0 (lead, AP-3, AP-8, AP-11), §10.1 V-09, §14 F-16 |
| **R9-1** (ACT 3) | New **AP-12**: who requests the act at an arrival in the current phase (INTEGRATION; put to the owner for confirmation). It states the ruling and points to EXEC (Wave B) for how an arrival and a request are observed and recorded. No mechanism is defined here | §4.0 AP-12, §5.3 rule 2, VC-010 |
| **R9-2** (ACT 2) | R8-11 item 2 and R8-12 item 2 are restated against the amended text: the reserved-act clause of D2 binds; V4-HI-42's request clause and record clause are in force whatever the autonomy setting; whether the run goes on before the act is for the person and the agents; the host's own treatment of its operations decides what the host does; where the grant lets the host apply directly, no A5 is forced and none is recorded | §3 D2 reading, AP-8, §4.4, §5.3 rule 2, §5.6 W-b, P-01, P-05 |
| **R9-3** | "the current phase (Phase 1)" on first use; the label row names the accepted texts' term | Header, §1 labels |
| **R9-4** (ACT 4) | Standing labels. The R8-11 item 2 reading of D2 is SETTLED (owner-confirmed: OWNER_ITEMS O-25, DECISION-7 of `APP-V4-BASIS-ALIGN-20260928`). Recording and showing the model destination is SETTLED (O-10, DECISION-7; DEL-04-03 ScopeOfWork REQ-002). The phasing and the person-only destination grant are cited to the amended basis. The A12 mapping of §2.7 stays INTEGRATION (F-22) | §1 labels, §2.7, §3, §4.0, §10.1 V-10 |
| **R9-8** (ACT 4; survey §1.4 items classed NOW) | Findings closed by record: F-10 (the ScopeOfWork was revised), F-18 (the four consumers carry R5-3), F-19 (RS carries the reference) and F-20 (the basis was amended). F-1 and F-8 are rewritten to the current registers and to the owner's decision on `Open_Issues.csv`; §8.2 follows F-8 | §8.2, §14, UNRESOLVED |
| R9-6 (ACT 5) | New value row **V-28** for §2.7, with its consumers; VC-007 traces it | §10.1, VC-007 |
| R9-5 (ACT 6; ScopeOfWork TBD-004) | VC-006 is in two parts (the current phase limited to recording; the governance phase). VC-001 and VC-010 cite TBD-004. VC-009 reconciles FX-01…55 and reports no results at v0.7. VC-011 traces to V4-EXM-23 | Verification cases |
| R9-11 | The policy revision identity reads ACT-POLICY-v0.7 | §8.1 |
| **R10-1** (node A2, in place; R9-2's second bullet corrected) | A direct application under the grant queues no proposal, so an A5 checkpoint (kind (c) *proposal queued*) is **not reached**: nothing is requested by reason of an arrival that did not occur, no A5 is forced, and none is recorded; the record shows the direct application under the person's grant. A checkpoint the run does reach while a grant permits direct application has its act requested and is *waiting* until the person performs it. "Its act is still requested" is withdrawn for the direct-application case | §4.4, §5.6 W-b, §8.3 P-05 |
| **K1-1** (node A3, in place; owner DECISION-K1 of 2026-09-30, `APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md` sha256 35d6546346907137581be7df3bed4a8ccdb4b8bc55a261ca716040d0ad9f91bc) | AP-12 relabelled **SETTLED by DECISION-K1 K1-1** (was INTEGRATION, put to the owner); the §4.0 lead says so. V-09 cites it | §4.0 lead, AP-12; §10.1 V-09 |
| **K1-2** (node A3, in place) | §4.5: in the current phase an earlier act counts when it is of the required kind and the content it was made on is still current; the record cites it and its time (EXEC SP-6). Capture at or after the arrival is kept only as a governance-phase option (EXEC SP-6F, PROPOSED). "Prior act on this subject, not counted" stays for an earlier act whose content is no longer current or whose kind differs, or under that option. §2.3 continuation, V-09, V-27, §12 item 5, F-14, F-17, L-ACT-5's reason and VC-002 follow; U-14 closed; FX-40, FX-45, FX-51 recomputed | §2.3; §4.5; §10.1; §10.2; §12; §13; §14; UNRESOLVED; Verification cases |
| **K1-3** (node A3, in place) | §4.3: the joint-answer rule (two or more acts may together answer one arrival; each cites its items; after a partial lapse a new act on the changed items alone answers together with the earlier act for the unchanged items; EXEC §4.7 JA-1). §2.5, V-24, §10.3 DEL-09-06 row and §12 item 2 follow; U-03 closed | §2.5; §4.3; §10.2; §10.3; §12; UNRESOLVED |
| R10-9 (node A2, in place) | Beside ND-A1: a checkpoint's *grant setting* subject is an operation-class A12 only; a checkpoint on a network-destination grant is a possible later extension, PROPOSED, not defined | §2.7 ND-A1 |
| **R11-1** (node A4, in place; V17-A B-1) | AP-5: a checkpoint's arrival, the request where it can be identified and the act that answers it (with the other events listed) are **recorded** where the arrival is observed; recording there is required, not optional (R9-1; DEL-02-03 SoW REQ-002; EXEC PH-6), and is observation, not enforcement. Was "may be recorded", which contradicted EXEC PH-6 and R9-1 | §4.0 AP-5 |
| R11-7 (node A4, in place; V17-A m-3) | AP-12: "Its request is an A8 (§2.1; DERIVED)". The A8 mapping is this contract's own derivation from §2.1; DECISION-K1 K1-1 decides who asks and what the product does, not the act kind | §4.0 AP-12 |
| R11 notes, V17-A N-2 (node A4, in place) | §4.5: capture evidence for acts in the App cites EXEC §5 (CAP-1…CAP-9; CAP-8 for the person's identity) instead of WD U-25, which DECISION-K1 K1-4 closed | §4.5 |
| **R11-3** (node A4, in place; V17-A M-1) | Header: a new line pins this run's records at their final bytes: R9 `a64e2415…`, R10 `ad3b6caa…`, R11 `e7343b66…`, OWNER_DECISIONS `7458e9e8…`. The node A1 input line and the K1 rows keep the bytes read then | Header |

## Changes from v0.5

Keyed by R8 ID; sources are I2 rows of INTAKE_MAP.md (`nn.k`, `P2.n`, Part 2.2
ACT rows, Part 3 items, Part 4 sections). R8 overrides I2 where they differ.
SETTLED here means by DECISION-3 or DECISION-4. The owner files EXEC-v0.4 and
WD-v0.6 were revised first; this file follows them.

| R8 ID (source) | Change in v0.6 | Where |
|---|---|---|
| **R8-1** (DECISION-4 D4-1; SETTLED, framing INTEGRATION) | New **§4.0 Phase 1** (AP-1…AP-11), mirroring EXEC PH-1…PH-10 and WD CG-1…CG-7: checkpoints are plan guidance; no App or host-loop hold, block or re-hold; no hold-support value and no *unsupported* for a hold reason; acts are recorded **only when the person performs them**; **reserved acts stand**, host-enforced through its operations; arrival and act are recorded as observation; *action during hold* becomes the optional annotation "continued past ‹checkpoint› before ‹act›"; a `governed` flag is guidance only. New label row for the phases | Header, §1, §4.0 |
| **R8-1** (governance phase retained) | Hold-support passages are recast as **governance phase (retained)**, with the Phase-1 statement beside them: §4.3's re-hold consequences, §4.4's carriage assurance and *not permitted* outcome, and §4.6 (retitled). Nothing is deleted. §4.5's "the loop resumes" is split into the both-phase recording rule and the governance-phase resume | §4.3, §4.4, §4.5, §4.6 |
| **R8-1** (V4-WF-05; S9) | V4-WF-05's first half is phased to the governance layer, not withdrawn (AP-11). S9 and W-b are annotated. New F-20 flags S9, D2's checkpoint half and V4-WF-05 for the next accepted-basis update | Header, §3 S9, §5.6 W-b, §4.0, §14 F-20 |
| **R8-1** (cases) | Two-part form (Phase-1 result; governance-phase value): §4.6 Consequences for E1 over X and **`CP-L4`**; **FX-48** (a)–(d); **FX-50**; FX-29, FX-36, FX-39; FX-21 annotated. New **FX-54** (Phase-1 guidance, the continued-past annotation, an agent's fabricated A4, a reserved operation refused, `governed` in Phase 1) and **VC-010**. VC-001, VC-002, VC-009 updated | §4.6, §13, Verification cases |
| **R8-2** (I2 R8-Q1, R8-Q-HS4; P2.1, P2.7, P2.13, P2.14, P2.16; §2.2 ACT rows) | SQ-02's answer (route (iv), none planned) is recorded as the **governance-phase input**. Governance-phase values: E1 `CP-accept` → **not enforceable** (was *not established*); **`CP-L4` App run over X → not enforceable → workflow *unsupported*** (was *not established*); FX-48 (b), (c); FX-50 → *not enforceable* (the "HELD on SQ-02" marker is removed). §4.6 value table: the *not established* row notes that neither cause now applies against SWBPIPE (R8-2 overrides I2 P2.16's note), and HS-4 no longer masks SWBPIPE entries. Authoring advice records that no governed checkpoint is enforceable from the App on SWBPIPE's X. **D6 is closed for Phase 1** and re-opens with the governance phase (§4.6, §10.2 V-26, §12 item 5, U-D6) | §4.6, §10.2, §12, §13, UNRESOLVED |
| **R8-3** (I2 R8-Q2; Part 3 item 2) | §2.5: staleness is per item where the host supplies subject identities; otherwise the host's stated scope (SWBPIPE: whole model) is received and shown, never narrowed; de-duplication first is unchanged | §2.5 |
| **R8-4** (I2 R8-Q3; 03.12; Part 3 item 3) | §2.5: a whole-model identity is received as every covered subject's identity (over-lapse, never under-lapse); never App-computed. SWBPIPE's Apply binding (SQ-03 (c)) noted. New **U-15** (V4-HI-32 not met by SWBPIPE; owner SWBPIPE) | §2.5, UNRESOLVED |
| **R8-5** (I2 R8-Q-item-1, R8-Q10, R8-Q13, R8-Q15; 01.6, 06.3; Part 4.9) | New §6 received-terms table: `unsupported_method`/`unsupported_change` → host-reported *not exposed on this surface*, never *not permitted*; #885 `withdrawn` → item left, "cleared by the person, no decision record"; `validation_rejected` → *refused — invalid*; none is ever A10 or A11. Rows 6–8 do not arise on SWBPIPE's X, and R2-4 is recorded as not met (new F-21). §2.5 and §7: accept and apply are one step per batch on SWBPIPE, with no A10 record; session undo writes no receipt, so "reverses ⟨receipt⟩" is *not supplied* | §2.5, §6, §7, §14 F-21 |
| **R8-6** (SQ-13, SQ-28; I2 R8-Q4, R8-Q4b; 13.6, 28.1; P2.18) | §2.6: A13 stays reserved. SWBPIPE has no enablement facility, so its channel stays *not enabled*; `controller_unavailable` → *endpoint unavailable*, channel *disabled*; host answers without evidenced A13 → evidence limit. FX-24 and FX-47(c) annotated (FX-47(c) keeps AWAITING INPUT). F-15 confirmed by SQ-28. The launch-environment-variable question is recorded as deferred owner item **U-16** and §12 item 7 | §2.6, §6, §12, §13, §14 F-15, UNRESOLVED |
| R8-7 (X.5; 01.5, 05.1, 05.2, 02.8; Part 4.11) | Standings move to **answered**: header, §1, §2.6 (SQ-01), §3 D2 note (SQ-05), §4.4 and §4.5 relay bullets (SQ-02, SQ-01), §7 quote block and §8.1 *host adoption* (SQ-05), §12 item 4 (all six answered). U-01, U-04, U-06 and §8.4 owners and effects updated (SWBPIPE owner decisions PB-TBD-002 / DEL-16-03, OI-016, host-held route, A13 facility; point of need "when the owner resumes UI-SUCCESSOR"). No text of this file cites OI-003, so no qualification was needed | Header, §1, §2.6, §3, §4.4, §4.5, §7, §8.1, §8.4, §12, UNRESOLVED |
| R8-10 (I2 R8-Q12) | §4.4: the agent never adds a field the host's schema lacks; an expected constraint not carriable is recorded as "constraint not carriable on this host" (governance phase) | §4.4 |
| **R8-11** (A1 residuals) | Item 1: lapse recording in Phase 1 and disposition words as record labels are **confirmed** (AP-5, AP-7; §4.3). Item 2: D2's "no grant widens past a reserved act" binds in Phase 1 and the host enforces it; its "or a declared checkpoint" half, WD I-7 and V4-HI-42 are guidance in Phase 1 (§3 D2 note, AP-8, §5.3 rule 2, P-01, P-05). Item 3: an invalid declaration is a declaration finding in Phase 1 (AP-9); a harness-capability reference stays *not established* for a required-tool reason (§4.6; FX-48 (a)). Item 5: governance-phase values read the fixture's checkpoints as if governed (§4.0, §4.6, §13 rules) | §3, §4.0, §4.3, §4.6, §5.3, §8.3, §13 |
| **R8-12** (items 1, 7; closing pass, node A6, in place) | §4.3: the Phase-1 lapse after resume is labelled **"act lapsed at ‹t›"** (nothing says *waiting*; nothing re-held). Consumed inputs list the post-R8 sibling versions; §7 and §13 fixture sources note that C-v0.6 carries the C-v0.4/C-v0.5 fixture. No rule or value changes | Header, §4.3, §7, §13 |
| **R8-13** (DECISION-5; the person-only grant SETTLED; the act mapping INTEGRATION; in place, no version bump) | New **§2.7 Network-destination grant**. Granting a host's agent a network destination, by an allow-list edit (a category switch, a named destination, or turning on an always-off item) or by an in-work grant scoped once / this run / always, is a person-only act. It is mapped as an **A12 grant change**, subclass **network-destination grant**, under D2 (e), which already reserves changing the autonomy grant. An agent never performs it: its request is an A8, and a decline is an act-declined event of kind A12, reported to the agent as "destination not allowed by the person". A non-stateless MCP server cannot be the subject of a grant. The §2.1 A12 row, the §2.6 A12 row and the §3 D2 note are annotated. New local label L-ACT-8, **FX-55**, F-22, U-17 and **VC-011** | Header, §2.1, §2.6, §2.7, §3, §13, §14, UNRESOLVED, Verification cases |
| R8-13 close — in place | The owner confirmed DECISION-5 (the reading of "MCP V2"; the person-only grant stands), so the "open to the owner's correction" markers are closed. The consumed-input line is corrected: OWNER_DECISIONS.md is cited in its state that adds that confirmation, not at `1528a5033` |
| V10 S-1…S-4 — in place | The wording of the DECISION-5 confirmation is made precise (the "MCP V2" reading was confirmed; the person-only grant was not objected to and stands). The revised V4-HOST-02 is "the recorder's wording confirmed by the owner". The always-off item reads "a silent switch". ACT F-22 is updated. No rule changes |

## Changes from v0.4

| R5 item (source) | How addressed in v0.5 |
|---|---|
| R5-1 (V3-A MAJOR-1; V3-B MAJOR-5) | §4.6 uses the four ruled hold-support values: *enforced by the host loop*, *enforced on the host route*, *not established* and *not enforceable*. The five EXEC-v0.1 values are retired. The E1-over-X consequence is stated: `CP-accept` is *not established* and App-only checkpoints are *not enforceable*. FX-48 and FX-50 are revised. |
| R5-2 (Y-1, Y-8; V3-A m-6; V3-B MAJOR-1) | §4.4 defines **host-held** (derived from, or verified against, the host's own resolved copy; the host loop's evaluation counts). A constraint the host merely received keeps its source's assurance. **App-assured is not available in this increment** (R4-2). Only host-held carriage satisfies R2-12. |
| R5-3 (Y-2; V3-A m-5) | In §4.2 the declared setting content always binds. An A8 may present it but never changes the subject. A run-dependent scope is a declared binding rule. A declaration naming no setting content is **invalid unconditionally**, before the run. FX-44 is revised and FX-52 added. R4-9's A8 precedence is superseded (F-18). |
| R5-4 (V3-A m-11) | Header and V-10: "host content may flow to the selected model; no gating" is SETTLED (DECISION-2). "Record and show the destination" is **INTEGRATION (DECISION-2 reading)**. |
| R5-5 (Y-4; consequence) | §4.3: whatever causes a lapse re-holds, including the person's own undo. The person's undo is never "action during hold". An undo never re-holds an A5 arrival. |
| R5-6 (Y-5) | §2.4: an operation that performs a reserved act (OP-C6/C7/C8; the A12 and A13 controls) produces the human-act record, and the R7 entry references it. A person's own A1/A2 remain R7 operations only. FX-53 added; F-19. |
| R5-7 (Y-6; V3-A MAJOR-3, MAJOR-5) | The local CP-3 is replaced by C's **V-GR1** (E1d `CP-grant` arriving at r15, before T15). FX-41 and FX-46 are re-pointed. FX-51 is added: T15 before arrival does **not** count, and the person must repeat the grant change (U-14; F-17). |
| R5-9 (Y-7; V3-A m-3, m-7, m-12; V3-B) | FX-50 no longer cites the retired ADAPTER U-X3. FA-n becomes **FXA-n**. Citations move to C-v0.4, EXEC-v0.2, ADAPTER-v0.2 and WD-v0.4, with hashes in the header. |
| V3-A m-2 | The local checkpoint reason no longer says "C declares only CP-accept". It now explains why a direct-branch checkpoint is local, since FXA-5 declares `CP-accept` and `CP-check`. |
| V3-A m-13 | Local fixture additions are named: L-ACT-4 (`CP-L4`, formerly CP-1), L-ACT-5 (`CP-L5`, formerly CP-4), L-ACT-6 (FX-Professional-P) and L-ACT-7 (harness-capability variant of `CP-grant`). The retired L-ACT-1 and L-ACT-3 are not reused. |
| R5-10 (relay; consequence) | §4.6 and F-16: SQ-02 decides holds only for checkpoints on host operations. App-only checkpoints remain *not enforceable* (D6 follow-up for the owner). |
| R6-1 (V4-A MAJOR-1/2; in place, no version bump) | §4.6 classifies hold support by **held actions**: HS-2 host loop; HS-3 host operations only, valued by SQ-02 status; HS-5 any App-side held action, *not enforceable* in App runs; HS-1 invalid, no value. E1 `CP-check` → *not enforceable*. `CP-L4` holds host operations only, so it is HS-3 (*not established* over X; *enforced by the host loop* on E). FX-48 gains (c) and (d). |
| R6-3 (V4-A minor; in place) | §4.6 gains a table of what "held" means per value, and the action-during-hold bullet is aligned: under any value other than *enforced by the host loop*, App-side actions continue and are recorded. |
| R6-4 (V4-A m-1, m-9; in place) | FX-44 cites WD VC-41 and EXEC CH-29 (EXEC has no VC-41). The "not yet in C" and "C will add" markers for V-GR1 are removed (present in C-v0.5 §10.4). The §8.1 policy revision identity now reads ACT-POLICY-v0.5. |
| R7-4 m-4 (V5 m-4; in place) | §4.3 lapse bullet "after resume, run live": "the run stops at its next action boundary" is qualified per R6-3. The run stops only where the value is *enforced by the host loop*; under *enforced on the host route* the held host operations are refused; otherwise nothing is stopped and the action is recorded as *action during hold* (§4.6). |
| R7-4 m-5 (V5 m-5; in place) | §4.6 value table: "a constraint carried only as model-supplied" → *not enforceable* is qualified "once SQ-02 is answered with no host-held route (HS-3; before that answer, *not established*)". |
| R7 carried observation (V5 §6; in place) | §4.6 `CP-L4` bullet adds a one-line cross-reference to its DEL-04-02 counterpart AS F6d (and notes that AS F6c, holding App agent turns, is HS-5). No value changes. |
| R7-4 m-4 (V5 m-4 class; integrator, in place) | FX-39 re-hold wording is qualified per R6-3 in the same way as §4.3. No value changes. |

## Changes from v0.3

| R4 item (source finding) | How addressed in v0.4 |
|---|---|
| R4-2 (DECISION-2 D6; EXEC §3.6, HP-1…HP-3) | New §4.6 *Hold support*. Every checkpoint relied on in an App run carries per-checkpoint hold support (EXEC §3.6). This contract never states or implies an App hold that the surface cannot enforce, and it records **action during hold**. It adopts neither HP-1 (interposed App code) nor HP-2 (`turn/interrupt`). HP-3, a named-rule decline, stays a permitted best effort under D3. App-side run holds are `UNRESOLVED{D6}` (U-D6), pending SWBPIPE SQ-02. R4-21: a harness-capability reached-when kind (a) is not holdable in App runs. |
| R4-3 (EXEC §4.7; W7 F-2) | §4.3 adopts EXEC's resume point (HD-5 run-resumed event) and re-hold. A lapse after resume re-holds the **same arrival**, displayed "waiting — re-held, lapsed at ‹t› after resume". The run stops at its next action, nothing done is undone, gated outputs show standing *lapsed*, and the request covers the whole scope. A5 and A12 never re-hold. The interim "performed + act-lapsed" display is withdrawn. U-10 is closed. PROPOSED (EXEC). |
| R4-4 (EXEC §4.9; W7 F-4) | §2.3: an ended run is never resumed. Acts after the end are shown "after run end" and change nothing. Continuation is a new run carrying **continues ⟨run⟩**, which inherits nothing. An interruption is not a run end. The phrase "unless DEL-02-03 defines resumption" is removed. PROPOSED. |
| R4-5 (EXEC SP-6; W7 F-3) | New §4.5 rule: an act counts toward a checkpoint only if it was captured at or after that checkpoint's arrival. Earlier acts are shown "prior act on this subject, not counted", and an order that cannot be established is shown "act order unknown". PROPOSED. U-E4 stays open for the owner (U-14). New FX-45. |
| R4-6 (EXEC §4.10; W7 F-5) | §2.5: an A12 supersedes only when it is **established**. A refused A12 neither counts nor supersedes. A pending A12 leaves the checkpoint *waiting*, and a lost confirmation makes it *unknown*. U-13 is closed. FX-41 is revised and FX-46 is added. |
| R4-9 (W7 F-13) | §4.2 grant-setting referent. The setting named by an A8, if any. Otherwise the setting content named in the checkpoint's own declaration: the classes, grant values and scope it states. A declaration that names none is **invalid** for A12. INTEGRATION. |
| R4-12 (W7 F-9; W8 F-3) | §4.5 and new §2.6: answers to Codex user-input or MCP elicitation requests, and conversation statements, are never act evidence (EXEC CAP-6, CAP-7; HOSTING R9). |
| R4-13 (W8 F-4; ADAPTER U-X1) | New §2.6 *A13 capture*. A13 on the host's external interface is captured by the **host's enablement facility**, and the host's refusal is the authoritative "off". The App-side access configuration is a person-directed App configuration change (ADAPTER E-4). It is **not A13 and never A13 evidence**, because an agent could write it. An App control would capture A13 only if it were the control that establishes an App-owned setting (EXEC CAP-1). ADAPTER U-X1 is closed as ruled here (PROPOSED). The host capture requirement stays DEP-001. |
| R4-14 (W8 F-1) | §4.4: the constraint is carried with a **carriage assurance**: App-assured, host-held, model-supplied or absent. Model-supplied carriage alone does not satisfy R2-12. The sentence "the loop and the external adapter both carry it" is replaced. |
| R4-17 (W8 F-5) | FX-25 now reads "drives T9–T10, observes T11–T12". |
| R4-18 (V2 MAJOR-1) | FX-20 is re-pointed to C T15: class P-03, grant value *direct*, scope {FX-W1; {S-4}}, ⟨set-2⟩. The labels-only local scope is removed. FX-21, FX-29, FX-37 and FX-41 are aligned with it. |
| R4-19 m-4 | §2.4: A1 and A2 performed by the person are recorded as **operations** in the run record, with the person as actor. They are not human-act records. RS aligns. |
| R4-19 m-6, m-7, m-13 | FX-15 now cites C **§10.7**. L-ACT-1, L-ACT-3 and the local S-4 cases are replaced by C's own entries: V-S1 (FX-06), **T16a** (FX-39), V-CP1 (FX-29), V-NP1 (FX-16), V-R1 (FX-22, FX-35), V-X1 (FX-35), T4a/OP-C12 (FX-34) and S-5 (FX-08). All fixtures cite C-v0.3 §10. |
| R4-19 m-9 | R3 and R4 are added to Consumed inputs, with hashes. |
| R4-19 m-11 | §2.3: the run-ended event's actor is the person who stops the work, or the observed end. The reporter may be the loop or the App. |
| R4-19 m-12 | F-12 and F-13 are closed as confirmed by V2. |
| R4-1 (D5) | No ACT change. The model destination is a run-record and channel-status element owned by DEL-04-03 and DEL-03-03, and it is not a policy value. Noted in §10.1 V-10. The attribution was relabeled in v0.5 (R5-4). |

## Changes from v0.2

| R2 / IR1 item | How addressed in v0.3 |
|---|---|
| R2-1; IR1A-01; IR1-B B-M1; IR1C-10 | The fifth class value is **no policy basis**, with a *reason* ∈ {omitted, unassigned, pending OI-021}. It is labeled INTEGRATION (R-3.5). The four V4-HI-02 values are labeled SETTLED (§5.1, §8.1). |
| R2-2; IR1A-08; X-1 | Reserved-operation rule restated as **perform**, not "perform or record", and A10 added (§5.3 rule 3, P-02). The conditions on a host-offered faithful-record operation are stated, and that question is routed to DEP-001. F-7 is closed. |
| R2-3; IR1A-16 | Disabling external access is also A13. It is labeled INTEGRATION, and only *enabling* is credited to D2e (§2.1, P-01). |
| R2-4; IR1A-02, -10, -21 | Reserved entries are always offered. An invocation returns *not permitted* and **offers** an A8 request; nothing is recorded automatically. *Not exposed on this surface* comes only from the host's exposure element. The loop reports its own *not offered*. §6 row 8 and FX-35 rewritten; U-11 closed. |
| R2-5; IR1A-03; IR1C-06; X-2 | **Act-declined event** for A4/A6/A7/A12, with elements and capture evidence. Its disposition is *resolved negatively*. Stopping work is a separate **run-ended event**, and the checkpoint stays *waiting* (§2.3, §4.3; FX-31, FX-40). |
| R2-6; IR1A-05; X-4 | New grant state **effective (policy default)**, which needs no A12. *not set* = no setting and no default. §5.3 rule 7 and FX-19 fixed. |
| R2-7; IR1A-04, -13; X-13 | A12 binds to the **setting content**. The established version, or a refusal by the control, is a relation on the act. A later A12 **supersedes** an earlier one and does not lapse it. A checkpoint that the superseded act performed stays *performed*. *superseded* added to the lapse-state vocabulary. A refused A12 at a checkpoint is held for DEL-02-03 (U-13). F-9 is closed into §2.5. |
| R2-8; X-3; IR1A-21 | A14 settlements are recorded only in run record R13. They never appear in R6, as a human-act record or as a grant. U-07 is closed; V-25 moves to the carried values. |
| R2-9; X-15 | Wording of rule 5 / P-06: proposing confers no permission; direct application is *not permitted*; an A12 that widens such a class is refused; the REQ-004 hold stands. Fixtures report these cases as **held**. F-5 is closed as confirmed. |
| R2-10; IR1C-22 | §4.1: a recognized act kind outside the list is **invalid** (WD FB-03). An unrecognized name is **not established** (WD FB-04). |
| R2-11; IR1A-16 | Attribution hygiene. P-04 credits D3 only with what D3 says; the App-rule restriction is labeled INTEGRATION (R-2). A13 disable is labeled INTEGRATION. The derived rules keep their DERIVED labels. |
| R2-12; IR1C-03 | §4.4: the **governing checkpoint constraint** travels with the change request. A direct request made under the constraint is *not permitted* and names it; it is never "drafted as a proposal". Relay question routed to DEP-001. Affected fixtures are **AWAITING INPUT** (FX-29). |
| R2-14 | §4.2: "objects changed by a named outcome" binds to the per-item resulting object identities that the applied outcome reports. |
| R2-15; IR1A-06 | §2.5: undo (a receipt that *reverses ⟨receipt⟩*) lapses acts bound to content it changes in the normal way. It does not lapse A5/A10 on the reversed item. OP-C10 Undo is used in FX-39. |
| R2-16 | FX-06 display: "accepted by ‹person› — not applied: refused — stale (both bases)". The A5 is not lapsed. |
| R2-17; IR1C-05; X-10 | §4.2: the subject class is independent of the reached-when kind. Referents now include **targets of the held call** and the **grant setting**. An A5 checkpoint uses kind (c) *proposal queued*. |
| R2-18 | §4.3: mixed item decisions cite WD §4.3.7 (PROPOSED). "Partial" is a per-item annotation. U-09 narrowed to DEL-02-03 confirmation. |
| R2-19; IR1A-09; IR1C-07 | §4.3: one lapse sequence. An **act-lapsed event** is recorded and the disposition returns to *waiting* ("waiting — lapsed at ‹t›"). After resume, re-hold belongs to DEL-02-03. *lapsed* as a standing disposition is used only when the run has ended. |
| R2-20 | §4.5: the capture-evidence reference is a relay question. Without it, no host-content checkpoint can be *performed*. The App-side equivalent is WD U-25. |
| R2-21; IR1A-07; IR1-B B-M9 | §7 and §13 re-pointed to C-v0.2 §10: FX-PIPE-01, T1–T17, PR-1/PR-2, RC-1…RC-3, OP-C1…C9, plus OP-C10/OP-C11. The v0.1/v0.2 meaning of OP-C5 is dropped (it is now "Set support stiffness"). OP-X1 is removed. Local cases are named `L-ACT-n` with reasons. |
| IR1A-12 | A9 recorder list no longer includes "the person"; self-recording is *direct capture* by the capturing surface. §2.4 adds A13 to the non-conformance list. Human-act record kinds exclude A9, which is carried as a recording mode, and A14. |
| IR1A-14 | The grant's direct/propose value is called the **grant value**. *Treatment* is kept for the §5.2 outcomes. |
| IR1A-17 | FX-16: the person's A12 widening of a no-policy-basis class is **refused (reason: no policy basis)**. |
| IR1A-18 | Run ended while waiting: covered in §4.3 and FX-40. |
| IR1A-20 | Finding F-10: SoW TBD-001/002, AC-004 and VER-004 wording predates DECISION-1 (routed to C1). |
| R3-1 (in place, no version bump) | §4.2 adds the subject class **objects a named output concerns**, bound through the subject content identities as read. This lets a review-only workflow require A4 on the rows it examined. INTEGRATION. |
| R3-2 (in place) | §4.2: *targets of the held call* is valid only with reached-when kind (a) *before dispatch*. Any other kind makes the checkpoint invalid. INTEGRATION. |
| R3-4 (in place) | §5.3 and P-03: an undo (OP-C10) is governed by the policy record and grant state of the operation whose receipt it reverses. It has no class of its own. The §8.3 fixture note for OP-C10 is updated to match. INTEGRATION. |

The "Changes from v0.1" table at the end of this file is kept as history.
Where it conflicts with this table, this table governs.

---

## 1. Purpose and reading

This contract gives consumers one meaning for:

- what an agent may do directly, what it must propose, and what only the
  person may do;
- which act happened, who performed it, what it concerned, and what evidence
  supports it.

It carries the owner's rulings D2 and D3 as adopted policy records. It performs
no human act and implements no host facility. It does not claim that SWBPIPE
has adopted or enforces any value (DEP-001). SWBPIPE's answers to the relay
questions were relayed and answered on 2026-09-28 (RELAY §4). They are noted
where they bear on a rule. They are answers about SWBPIPE's current state, not
commitments or contributions, and host joins are deferred (DECISION-3; R8-7).

| Label | Meaning here |
|---|---|
| **SETTLED** | Stated in the accepted composite (B-ACCEPT), as amended by SCA-V4-001 and SCA-V4-002, and cited; or a reading the owner confirmed at an amendment checkpoint, cited to that item (R9-4) |
| **ADOPTED** | Owner ruling `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (D2/D3), credited only with what it says (R2-11) |
| **DERIVED** | A direct consequence of settled or adopted clauses, with the derivation shown |
| **INTEGRATION** | An R1/R2 integrator choice. Reviewable, and open to owner revision. |
| **PROPOSED** | A design choice of this contribution or a sibling, open to review |
| **UNRESOLVED{…}** / relay question | An open item with owner and point of need |
| **Phase 1** / **governance phase (retained)** | Which phase a checkpoint rule belongs to (R8-1). Phase 1 is this increment: "the current phase" of the accepted texts (R9-3). A passage marked *governance phase* is kept as the definition a later layer will enforce for checkpoints declared `governed`; it is not in force as enforcement in Phase 1 |

---

## 2. Acts — canonical names, actor, subject, evidence

**Rule.**
- Evidence of one act kind never establishes another.
- The absence of one act kind does not, by itself, invalidate an independently
  evidenced act of another kind (REQ-002; AX-002).
- Acts are never promoted automatically into other acts, and there is no
  universal acceptance prerequisite.

### 2.1 Canonical names and alias map (R-1)

Every consumer uses the canonical name. An alias in the basis maps to its
canonical name.

| ID | Canonical name | Aliases in the basis | Decision actor | Subject | Supporting evidence | Does **not** establish | Policy standing | Basis |
|---|---|---|---|---|---|---|---|---|
| A1 | **propose** | draft/submit a proposal | Agent (embedded or external) or the person | One proposal of one or more change items against a cited read basis | Host proposal record with origin and relied-on basis; lifecycle state | Acceptance, application, checking, approval, reliance | Agent-available | V4-HI-21, -23, -24, -25; d3 |
| A2 | **apply** | execute an operation; direct application | The person; an agent under an effective direct treatment; the host route after acceptance | The operation invocation and its effect on identified objects | Host receipt, origin mark and observed outcome per DEL-03-02 P §9 (R-7), including the resulting object identities (R2-14) | That anyone accepted, checked, approved or relied | Governed by treatment (§5) | V4-HI-20, -22, -23, -25, -71 |
| A3 | **examine** | agent check, examination, findings | Agent | Identified rows, results or models, by read basis | Findings attached by reference; no table change | A4, A5, A6, A7 | Agent-available | d3; V4-EXM-21 |
| A4 | **mark checked** | marking work checked | The person | Identified host rows/objects or App file content, with scope and purpose | Capture evidence from the capturing surface (§4.5), bound to subject content identity | A5, A6, A7 | **Reserved** — ADOPTED D2a | V4-AUT-03; V4-HI-30, -32; V4-REC-05; X-20 |
| A5 | **accept** | accept an edit; accept a proposed edit | The person | One or more identified **change items** (§2.5) | Capture evidence listing the items; labeled "accept" | A6, A4, A2 | **Reserved** wherever the active autonomy requires a proposal — ADOPTED D2b | V4-HI-23, -25, -33, -41; d3 |
| A6 | **approve** | engineering approval (V4-HI-30/33) | The accountable person | Identified engineering content or design | A separate attributable approval record | A7 or any certification | **Reserved** — ADOPTED D2c | V4-HI-30, -33 |
| A7 | **rely** | professional reliance; "accepting professional reliance" (d3; V4-CON-05) | The accountable professional only | A result relied on for a stated professional purpose | The professional's own attributable statement | Anything about agent output | **Reserved** — ADOPTED D2d; SETTLED V4-AUT-05, V4-HI-30 | V4-AUT-05; X-09 |
| A8 | **request** | prepare or request a person's act | Agent | A request naming the exact act kind, subject and purpose. A **decision package** (V4-PM-04) is an A8 that also names **alternatives** and **consequences** (R23-8; RS §13.6) | The request, with the requester identified | Anything. A request is never the act. | Agent-available. An A8 exists only when the agent actually issues it (R2-4). | V4-AUT-03; V4-HI-31; V4-PM-04 |
| A9 | **record** | faithful recording; direct capture | *Recorder*: the capturing surface (direct capture), or another identified party such as the host facility, the App or an agent (faithful recording). A person recording their own act is direct capture by the capturing surface. | An actually performed act of kind A4–A7, A10–A13, A16 (pass 4, R23-18), or an act-declined event | Reference to the act's evidence, recorder identity, and *recording mode* ∈ {direct capture, faithful recording} | The act itself. **A9 is a recording act, not a decision act**, and it never satisfies a checkpoint on its own. | Faithful recording by any identified recorder distinct from the decision actor is a conformant shape (SETTLED S3). Capture requirement: DEP-001. | SoW REQ-002; d3; V4-HI-31; R-1; R-5 |
| A10 | **reject** | reject a proposal or item; a person removing another party's proposal | The person | One or more identified change items | Host lifecycle record `rejected`, with actor | Anything beyond non-acceptance of those items | **Reserved** wherever A5 is — DERIVED (decision pair of A5; R-1) | V4-HI-23; V4-EXM-20 |
| A11 | **withdraw** | withdraw one's own proposal | The proposer only | Its own proposal | Host lifecycle record `withdrawn` | A decision on the proposal's merit | Proposer's act. It is a human-act record only when the person is the proposer. | V4-HI-23; R-1 |
| A12 | **set grant** | set or change the autonomy grant; allow a network destination, or grant one during work (subclass **network-destination grant**, R8-13) | The person | **Setting content**: operation classes, grant values and scope (§2.5, §5.4). For the network-destination subclass: the allow-list content, or an in-work grant with its scope (§2.7) | Capture evidence from the control surface. The version the control establishes, or the control's refusal, is a relation on the act. | That an agent's A8 established anything | **Reserved** — ADOPTED D2e | V4-AUT-01; V4-HI-40, -41 |
| A13 | **enable external access** (includes disabling) | enable or disable external-agent access | The person | The host's external interface on this machine (enablement setting) | The host enablement record captured by the host's enablement facility, with a capture-evidence reference (§2.6). App-side access configuration is never A13 evidence (R4-13). | Any grant for an operation class | Enabling: **reserved**, ADOPTED D2e. Disabling: **reserved**, INTEGRATION (R2-3). An agent may request either (A8). Off by default and local: SETTLED. | V4-HI-52 |
| A14 | **answer tool permission** | harness "approval" of tool use; routine tool permission | The person, or the user's own Codex permission mode inside the supplier | One tool-execution request | Request settlement: answered, or explicitly declined, or errored; never by silence or timeout. Recorded only in run record R13 (R2-8). | Any of A4–A7, A10, A12, A13, or a host-operation grant | ADOPTED D3: App modes are the user's Codex setting; hosts have no classifier mode. INTEGRATION (R-2): the App never answers affirmatively by rule; a decline or error is allowed only under a named rule with truthful origin. | V4-AUT-04; V4-EXE-02; D3 |
| A15 | **register workflow revision** (R12-5) | register a workflow; explicit registration of a reviewed draft | The person | **A workflow revision**, or several library entries registered in place in one act, each bound to its own reviewed bytes and prior revision, as a batch A5 lists several items (DECISION-L L-4; WR-v0.2 §4.7). Content: the revision identity (equal to the reviewed draft's content identity, WR ID-2) and, for a new revision, the prior revision (R17-11). Purpose: make it available in the project library, or in the user library (for several entries: "make them available …", wording "register workflow revisions", WR ME-3) | Capture evidence from **DEL-01-04's App act control** (AAC-v0.2 §4.2; K-8; R17-6), composed from DEL-02-02's A15 descriptor (WR-v0.2 §4.3 RB-4), bound to the exact reviewed bytes; recorded per RS-v0.9 §6.1 HA-10 | That any other revision is registered; that the revision was examined, checked or approved; any A4–A7 | The person's act (V4-WF-02: "a draft until the person reviews it and registers it explicitly"). INTEGRATION (R12-5): recorded as a human act with an RS record kind. Not a D2 reserved act; no grant covers it and no agent performs it (S3). Not checkpoint-requirable in this increment (§4.1) | V4-WF-02; DEL-02-02 REQ-002, AC-006; R12-5 |
| A16 | **decide** (R23-8; pass 4) | decide a reserved coordination decision; choose an alternative of a decision package (V4-PM-04) | The person | **One decision package** (an A8 recorded as RS R16 `act_request` with its alternatives and consequences; an App file bound by its file content identity) and **the alternative chosen**, which must be one the package names. Scope and purpose as the package states them | Capture evidence from **DEL-01-04's App act control** (AAC-v0.3 §1.2), bound to the package file's content identity; the package reaches the control as a runtime value (R23-2); recorded per RS-v0.10 §6.1 under HA-1 and HA-11, citing the request. The package file's shape is DEL-02-03 `$defs/decisionPackageFile` (R23-24) | That the chosen alternative was carried out (A2), examined (A3), checked (A4), accepted (A5), approved (A6) or relied on (A7); any act the package does not name; that the decision was reserved (the workflow or accepted instrument the package cites says that) | The person's act (V4-PM-04). INTEGRATION (R23-8): recorded as a human act with an RS record kind. Not a D2 reserved act; no grant covers it and no agent performs it (S3). A package naming an existing kind (A4–A7, A10, A12, A13, A15) is decided by that kind, not A16. No act-declined event: the person closes the control or chooses an alternative the package offers. **A later A16 on the same package** is a new decision by the person that supersedes the earlier one for current standing, as a later established A12 supersedes an earlier one (L-0, R23-25); both stay recorded, and actions taken under the earlier decision stay recorded as taken under it. A **correction** of a mis-recorded A16 is a new entry naming it (RS OF-5), not a new decision. Not checkpoint-requirable in this increment (§4.1) | V4-PM-04; V4-AUT-03; V4-HI-31; R23-8 |

Alias exclusions (R-1):
- Design-candidate approval (V4-CON-05; V4-HI-65) is a separate act in a later
  increment. It is **not** A6.
- The word *accept* belongs to A5 alone.
- Registering a workflow revision (A15) is not *accept*, *approve* or
  *mark checked*, and a draft's review is not A15 (DEL-02-02 REQ-002).

Other human acts keep the attribution invariants but have no canonical name
here:
- workflow registration now has one: A15 (R12-5; U-08 closed);
- stopping work (V4-EXE-01), which produces a run-ended event (§4.3);
- reserved coordination decisions (V4-PM-04) now have one: A16 *decide* (R23-8).

### 2.2 Direct application is never acceptance

When an effective direct treatment lets an agent apply a change, the act is
A2. It is never recorded as A5. SETTLED S3 means an agent is never the
decision actor of A4–A7. D2(b) reserves A5 wherever the autonomy requires a
proposal. Wherever A5 is performed at all, only the person performs it
(finding F-6).

### 2.3 Decision pairs, act-declined events and run-ended events (R2-5)

| Required act | Positive | Negative | Standing of the negative |
|---|---|---|---|
| A5 | accept | A10 reject | An act, recorded per item |
| A4, A6, A7, A12 | the act | **act-declined event** | A recorded event. It is **not** an act of that kind and never satisfies anything that requires the act. |

- **Act-declined event** elements:
  - actor (the person);
  - declined act kind;
  - bound subject;
  - time;
  - capture evidence from the capturing surface. Faithful recording is a
    permitted record shape (§4.5).

  The event never records the declined act as performed. The name keeps it
  distinct from an A14 settlement `declined` (HOSTING §6), and from A10,
  which is recorded as "rejected the item", not "declined".
- **Run-ended event.** Stopping work (V4-EXE-01) is a separate action. It is
  not a decline.
  - Actor: the person who stops the work, or the observed end (for example
    "stopped by declared negative path" or "interruption not recovered",
    EXEC RE-4). The reporter may be the loop or the App (V2 m-11).
  - A checkpoint that is waiting when the run ends stays **waiting**, with a
    run-ended event.
  - A person who wants both declines, then stops, and both events are
    recorded.
- **No resumption of an ended run (R4-4; EXEC RE-1…RE-4; PROPOSED).**
  - An ended run is never resumed.
  - An act performed after its run has ended is recorded and shown against
    the bound subject, marked **"after run end"**. It changes no disposition
    of the ended run. The one exception is R2-19: *performed* becomes *lapsed*
    on a later lapse.
  - Continuing the work means starting a **new run**, which may carry the
    relation **continues ⟨run⟩**. The new run inherits nothing: no arrival, no
    disposition and no act. An act made before one of its arrivals counts
    there when it is of the required kind and its content is still current,
    and is cited with its time (§4.5; DECISION-K1 K1-2); under the
    governance-phase option of §4.5 it is shown "prior act not counted".
  - An **interruption is not a run end**. A run whose observation was lost is
    recovered as the same run (EXEC §4.12).

### 2.4 Recorded-act element meaning

This is the meaning DEL-04-03 receives. DEL-04-03 owns the format.

| Element | Meaning | Presence |
|---|---|---|
| *act kind* | One of A4, A5, A6, A7, A10, A12 (with its subclass), A13, A15, A16 (*decide*; R23-8), or A11 when the person is the proposer; or the act-declined event with its declined kind. A9 is carried as *recording mode*. A14 is never a human-act record (R2-8). | Always |
| *decision actor* | The person who actually performed the act | Always |
| *recorder* and *recording mode* | Who wrote the record; direct capture or faithful recording | Always |
| *subject content identity*, *scope*, *purpose* | What the act concerned (§2.5) | Always |
| *evidence reference* | Capture evidence from the capturing surface, linked and not copied (V4-HI-71) | Always. Without it, the record is non-conformant. |
| *lapse state* | Relative to current content (V4-HI-32). *superseded* for A12/A13. | When applicable |
| *governing policy reference* | The policy-class record and policy revision identity (§8.1) | Optional. Present when a catalog operation governed the act. |

A record is non-conformant if it names the recorder as the decision actor of
an A4–A7, A10, A12, A13 or A15 act, or if its person-attributed act has no evidence
reference.

**A1 and A2 performed by the person (R4-19 m-4).** These are recorded as
**operations** in the run record, with the person as actor: the requested
operation, its origin and its outcome. They are **not** human-act records.
Proposing and applying are not judgments (§2.1), and the operation's receipt
is its evidence. DEL-04-03 aligns its act-kind list with this section.

**Operations that perform a reserved act (R5-6).** Some operations produce
the **human-act record** of the act they perform. Examples:
- OP-C6, OP-C7 and OP-C8, operated by the person through the host's act
  facility;
- the A12 control and the A13 host enablement facility.

The run record's R7 operation entry for such an invocation **references** that
human-act record. The act is recorded once, as a human act, and the operation
entry points to it.

### 2.5 Content binding, lapse and supersession (S6; R-6; R2-7; R2-15)

| Act | Bound content (c₀ source) | Change rule |
|---|---|---|
| A5, A10 | **Change-item content identity** (DEL-03-02): operation identity and version, bound targets, old/new values, relied-on basis | See the notes on A5 and A10 below. |
| A4, A6, A7 on host content | **Subject content identity** (DEL-03-01 §5.3), per object or row, host-supplied | Per subject. A change to a bound row lapses the act for that row; an unrelated edit does not. An **undo** that changes a bound row lapses the act in the normal way (R2-15; V4-HI-32). |
| A4, A6, A7 on App files | File content identity (DEL-04-03) | Per file or scope |
| A12 | **Setting content**: classes, grant values, scope | PROPOSED (R2-7, R4-6). Not lapse-evaluated. See the A12 notes below. |
| A13 | Enablement setting content | PROPOSED. Superseded only by a later A13 that the host's enablement facility establishes. No lapse. |
| A15 | **Revision identity** of the registered workflow revision (= the reviewed content identity, WR ID-2), with **reviewed draft** ⟨draft, content identity⟩ and **prior revision** ⟨workflow tuple, or none for a first revision⟩ (R17-11; RS-v0.9 §6.1, form per R18-1 C-01); for several entries in one act, each entry with its own (L-4). WD's *derived-from* is not this act's relation (C-21) | PROPOSED. Not lapse-evaluated and never superseded: a revision's identity does not change, and a changed definition is a new revision that needs its own A15 (DEL-02-02 AC-002). An earlier A15 never carries over to a new revision (DEL-02-02 VER-002) |
| A16 | **Package file content identity** (an App file, DEL-04-03), with the **act request** decided and the **alternative chosen** (R23-8; RS-v0.10 §6.1, HA-11) | PROPOSED. Lapse-evaluated as an App file (RS L-1, L-6): a package changed after the decision lapses the A16 visibly. A revised package is a new request that needs its own A16; an earlier A16 never carries over. A later A16 on the same unchanged package supersedes the earlier one (§2.1 A16 row; R23-25). Not superseded by another kind's act |

**A12 and the control relation (R4-6; EXEC §4.10 AR-1…AR-4).** The control's
response is a relation on the act. It is not the act's content.

| Control relation on the A12 | Supersedes an earlier setting? | Effect at an A12 checkpoint |
|---|---|---|
| **established ⟨settings version⟩** | Yes. It supersedes an earlier A12 on overlapping classes and scope, and the record shows *superseded by ⟨act⟩*. | Counts toward *performed*, subject to §4.5 |
| **pending** (set by the person, not yet confirmed) | No | **waiting**, "A12 awaiting control confirmation" |
| **refused ⟨reason⟩** (e.g. "no policy basis") | **No.** The earlier established setting stays in force. | **waiting**, "A12 by ‹person› refused by control: ‹reason›"; the refused A12 does not count |
| confirmation observation lost (*unconfirmed*) | Not until it is observed | **unknown** |

- A refused A12 remains a recorded human act that establishes nothing.
- A checkpoint that an earlier established A12 performed stays *performed*,
  with any later supersession shown.
- Operations are governed by the grant state in force at route decision and at
  application.

Notes:
- A5 and A10 are evaluated per item.
  - Applying the accepted item does not lapse the acceptance.
  - A basis failure between acceptance and application falls under the stale
    rule (DEL-03-02 U-P3). It is not a lapse. The display is "accepted by
    ‹person› — not applied: refused — stale (both bases)" (R2-16).
  - Undoing the applied item (a receipt that *reverses ⟨receipt⟩*) does not
    lapse A5 or A10 on that item (R2-15).
  - A re-draft is a new proposal. The earlier acceptance does not carry over.
  - **Staleness scope (R8-3, amending R2-13; INTEGRATION).** The stale rule
    is applied per item where the host supplies subject identities.
    Otherwise the App receives and shows the host's stated staleness scope,
    and never narrows it. For SWBPIPE that scope is the whole model: any
    model change stales every queued proposal (SQ-07 (d)). De-duplication
    still runs first.
- **SWBPIPE counterparts (R8-5; INTEGRATION; SQ-01, SQ-09, SQ-10, SQ-23).**
  These meanings stand as App/shared meaning. On SWBPIPE:
  - **accept and apply are one step**, per batch: the person's **Apply** is
    A5 and application together, and there is no A10 record. A stale Apply
    is refused and records no acceptance, so the R2-16 display
    "accepted — not applied: refused — stale" does not arise there;
  - per-item A5/A10 and mixed items have no counterpart;
  - its **session undo** writes no receipt, so "reverses ⟨receipt⟩" is *not
    supplied*. A lapse the undo causes is still shown, from the identity
    change (R8-4).
- **Whole-model identity (R8-4; INTEGRATION).** Where a host supplies only a
  whole-model identity, the App receives it as the subject content identity
  of **every** subject it covers, with the host's method designation and
  scope. Any model change then lapses every act bound through it: this errs
  toward reporting a lapse and never misses one. The App never computes an
  identity itself. SWBPIPE supplies only a whole-model hash (SQ-03 (a)), so
  it does not yet meet V4-HI-32's per-subject identity (U-15). Its Apply
  binds the operation id, a claimed whole-model hash and per-field
  before-values (SQ-03 (c)), which partly matches the change-item content
  identity.
- Acceptance granularity:
  - Batch or multi-row acceptance is one A5 act listing several items, each
    bound to its own item and lapsing on its own.
  - Row-by-row acceptance is one A5 per item.
- After a partial lapse a multi-row A4 keeps its purpose for the unchanged
  rows: a new act on the changed rows alone answers a checkpoint together
  with it (SETTLED by DECISION-K1 K1-3; §4.3; U-03 closed).
- Every content identity carries its identity-method designation. The
  algorithm is unselected.
- The lapse-state vocabulary is DEL-04-03's. This contract adds
  **superseded** for A12/A13 (IR1A-13).

### 2.6 Capturing surfaces, and what is never act evidence (R4-12, R4-13)

| Act | Capturing surface | Never act evidence |
|---|---|---|
| A4, A5, A6, A7, A10 on host content | The host's act facility (V4-HI-31). The capture-evidence reference is a relay question (U-04). | An agent-authored record without that reference |
| A4, A6, A7 on App content | The App interface's act control (EXEC CAP-1…CAP-3), designed in DEL-01-04/AAC-v0.2 (§1.2, §4.1; PROPOSED until SCA-V4-003 carries SC2-01-04-1 as amended by SC3-01-04-1, D3 §5): one kind at a time, from a native confirmation only the person can operate, never raised by an arrival (R17-6) | See rows below |
| A12 | The control that establishes the setting: the host's control for host operation classes; an App control only for a setting the App itself establishes (EXEC CAP-1). For a network-destination grant: the host's allow-list control or its in-work prompt (§2.7) | An agent's A8, or any setting an agent wrote, including an agent-written allow-list entry |
| **A13** (external access on the host's interface) | **The host's enablement facility.** It records the host enablement with a capture-evidence reference. The host's refusal (*channel not enabled*) is the authoritative "off" (ADAPTER E-2, F-2). | **App-side access configuration.** Examples: the user's Codex configuration file, a per-thread configuration, or a plugin setting. An agent could write any of them, so none is ever A13 or A13 evidence. The App changes that configuration only at the person's direction (ADAPTER E-4). That change is an ordinary configuration change, recorded as such. It is not a second A13, and it enables nothing without the host enablement record (ADAPTER E-3). |
| **A15** (register workflow revision; R12-5) | **DEL-01-04's App act control**, operated by the person, composed from DEL-02-02's A15 descriptor and bound to the exact reviewed bytes (K-8; AAC-v0.2 §4.2; WR-v0.2 §4.3 RB-4, RB-5). Several library entries may be registered in one act, each entry's bytes bound (L-4). Recorded per RS-v0.9 §6.1 HA-10 | Draft creation; a trial in conversation (K-7: drafts are not run); an agent's recommendation; a review of other content; a registration of an earlier revision; a file an agent wrote into a workflow catalog; a registration ledger line without a capture (DEL-02-02 REQ-002, AC-006). An entry byte-equal to a shipped revision is recognized as that revision and takes no A15 (the release registered it; WR LS-5; L-4) |
| Any act | — | Answers to Codex user-input or MCP elicitation requests (EXEC CAP-6; HOSTING R9); A14 settlements from any origin (CAP-5); conversation statements (CAP-7) |

- **Standing: PROPOSED by DEL-04-01 under R4-13.** This closes ADAPTER
  U-X1 as ruled.
- **SWBPIPE, host content (SQ-01, 2026-09-28).** Only A5 is captured, as
  **Apply**, which is acceptance and application in one step. There is no
  A10 record. A4 exists only as DESIGN. A6 and A7 are not software acts. No
  capture-evidence reference is exposed, so no SWBPIPE-content checkpoint
  can be *performed*, and a faithful record has no reference to cite (§4.5;
  R2-20). The Apply receipt names no person or time and does not survive a
  restart. Durable storage and actor identity are SWBPIPE owner decisions
  (PB-TBD-002; DEL-16-03).
- **SWBPIPE, A13 (R8-6; INTEGRATION; SQ-13, SQ-28).** A13 stays a reserved
  act (§4.0). SWBPIPE has no enablement facility, and none is planned; its
  opt-in is a launch environment variable plus a build feature, which is not
  a captured act. So A13 cannot be evidenced there, and its external channel
  stays *not enabled* (a SWBPIPE owner decision; ANS §2). SWBPIPE has no
  *channel not enabled* code: `controller_unavailable` is reported as
  *endpoint unavailable*, and the channel shows *disabled*. If the host
  answers while no A13 is evidenced, the evidence limit "host reachable
  without evidenced A13" is recorded, and the channel is never shown
  *enabled*. Whether a launch environment variable that the person sets
  counts as A13 evidence is an owner question, deferred to when UI-SUCCESSOR
  resumes (R8-6; U-16). Live cases against SWBPIPE wait for the host joins
  (DECISION-3).
- **Still open:**
  - whether a given host requires its own facility to capture A13 (DEP-001,
    within U-04). SWBPIPE (SQ-28, 2026-09-28): no facility exists or is
    planned, as above;
  - A13 for an App-owned external interface, which does not exist in this
    increment. If one is introduced, its App control would be the capturing
    surface under EXEC CAP-2/CAP-3.

### 2.7 Network-destination grant — A12 subclass (R8-13; DECISION-5)

**Standing.**
- **SETTLED by DECISION-5:** the agent asks, only the person grants, and
  the agent never grants itself a destination. This point is
  settled by the owner's DECISION-5 confirmation (2026-09-28: the "MCP V2" reading confirmed; the person-only grant not objected to and stands).
  It is now in the accepted basis, as amended by SCA-V4-001: PRD V4-HOST-02,
  and the ARCHITECTURE §4 host-agent properties ("the agent may ask for a
  destination during its work, and only the person grants it") (R9-4).
- **INTEGRATION (R8-13):** the mapping to A12 with the subclass
  *network-destination grant*. D2 (e) already reserves changing the
  autonomy grant.

The network rules themselves are LOOP-v0.8 §5.1.1 (NW-8…NW-16). From
v0.8 (node B5) the flow they run in is DEL-05-01/LOOP-v0.8 §5.3, the one
account that this section, AS, RS, PANEL, C, P and ADAPTER cite (DF-1…DF-10).

| Element | Meaning |
|---|---|
| Act | **A12 set grant**, subclass **network-destination grant** |
| Decision actor | The person only. Never an agent |
| The agent's request (v0.8, node B5; PROPOSED) | The A8 is a call to the host's **destination request entry** (C-v0.8 §3.4; LOOP §5.3 DF-1) naming the target, purpose and scope sought, and carrying the call that needs the destination (the **carried call**). **The requesting call** of ND-A2 and ND-A3 is that request together with the call it carries; a request with scope *once* must carry one. The mapping "its request is an A8" is DERIVED from §2.1, as AP-12 labels it |
| Forms | (a) **Allow-list edit**: switching a category (web access, MCP servers, other APIs, …) on or off; adding or removing a named destination; turning on an always-off item (analytics or usage reporting, a silent switch to another model or provider, background downloads or updates). (b) **In-work grant** answering an agent's A8 destination request, scoped **once**, **this run** or **always**, for the destination or its category |
| Subject (setting content) | The category or named destination and the scope. For an in-work grant, also the requesting call and its run |
| Evidence | Capture evidence from the host's allow-list control or in-work prompt, with its time and its source (allow list or in-work); recorded per RS R15 |
| Decline | An **act-declined event** of kind A12 (§2.3), reported to the agent as **"destination not allowed by the person"** (the request call's result, TL-2 class 2; LOOP §5.3 DF-6). Not a grant. It is also recorded as an RS R15 destination entry (`destination_declined`): DEL-04-03's ScopeOfWork CLM-004 names "destination declined" among the events the record format receives from DEL-05-01 (SETTLED by CLM-004; R16-1, correcting R12-10). The act-declined event itself is INTEGRATION (R2-5, R8-13) |
| Never evidence | The agent's A8 request; silence or timeout; model text; a tool success; an agent-written list entry or configuration |
| Outside this act | The selected model service and its sign-in service, allowed by the person's model choice (LOOP NW-9), which is the person's own setting change (LOOP NW-4), not a list edit. The App's own Codex configuration, approval and sandbox choices (A14; D3; HOSTING §2) |
| Non-stateless MCP | A server that does not follow the stateless MCP revision 2026-07-28 cannot be the subject of a grant (DECISION-5). An A12 naming one is refused, reason "not stateless MCP (2026-07-28)"; the request ends *not granted* ("not grantable"), without a grant choice (LOOP §5.3 DF-3 A-3, DF-6). What evidences that a server follows the revision is LOOP §5.3 DF-7 (PROPOSED) |

- ND-A1. A network-destination grant widens no operation class and no
  reserved act. An operation-class A12 grants no destination (A-1: the
  evidence of one act never establishes another). Conversely, a declared
  checkpoint's *grant setting* subject is an operation-class A12 only (WD
  §4.3.1, §4.3.6; EXEC §4.10): a checkpoint cannot require a
  network-destination grant in this increment. Such a checkpoint is a
  possible later extension, PROPOSED, with no definition (R10-9).
- ND-A2. Scope:
  - *once* is consumed by the one requesting call;
  - *this run* ends with the run, and a continuing run inherits nothing
    (R4-4);
  - *always* adds an allow-list entry, which a later established list
    edit supersedes (§2.5).
- ND-A3. Only the requesting call waits for the person (LOOP NW-12). This
  wait is not a checkpoint hold, and §4.0 is unaffected.
- ND-A4. Phase 1 covers the person's allow list and in-work grants. Allow
  lists locked by an organization are governance phase. They would be a
  policy, not the person's act, and are not defined here.
- ND-A5. No host offers this control today. SWBPIPE has no embedded agent
  (SQ-20, SQ-29), and nothing here is claimed of it (DECISION-3).

### 2.8 Act-record lifecycle (ACT 7; PROPOSED as one table; the rules it gathers keep their own standing)

One table for what §2.3, §2.5, §4.3 and §4.5 say about an act record over
time. The first column is the state of the act and its record. How an act
stands **at a given arrival** is a relation, not a state of the act, and is
listed below the table. RS-v0.8 §3 gives the states of a written entry
(written, corrected, partial, …); §6.1 and §7 there give the record elements.

| # | State | Entered when (evidence) | Kinds | Leaves to | RS entry (§13) |
|---|---|---|---|---|---|
| LC-1 | **requested** — no act yet | The agent's A8 is identified (AP-12) | A4–A7, A10, A12, A13, A15 | LC-2 when the person acts; LC-D when the person declines; stays while nobody acts, never a grant or act by silence (S12) | `act_request` (R16) |
| LC-2 | **captured, not yet recorded** | The person operates the capturing surface (§2.6); capture evidence exists there | All | LC-3 when written. If the write fails, the writer reports it and writes the entry later in order, followed by "record write failed" (RS §14.3 FC-1); the capture evidence still exists, so another recorder can also record the act faithfully, citing it (RS §6.1, recording mode *faithful recording*) | — |
| LC-3 | **recorded, current** | A human-act record is written: direct capture by the surface, or faithful recording citing the same capture evidence (A9) | All | LC-4, LC-5 (content-bound acts); LC-6 (A12, A13); LC-8. A15 stays here (§2.5) | `human_act` |
| LC-3a | A12 **control relation** | The control's report: *pending* · *established ⟨settings version⟩* · *refused ⟨reason⟩* · *unconfirmed* (§2.5) | A12 (both subclasses) | *established* → LC-6 only by a later established A12; *refused* establishes and supersedes nothing | the next `settings_version` naming the A12 |
| LC-4 | **lapsed** · **partially lapsed** · **lapsed (subject absent)** | The bound content is observed changed (act-lapsed event, both phases) | A4, A6, A7; A5 and A10 per item (never by applying or undoing that item) | "matches c₀ again after observed lapse" (L-11), keeping the lapse visible; never silently back to LC-3 | `act_lapsed` |
| LC-5 | **unknown (incomparable)** · **unknown (unavailable)** · *not yet evaluated* | The method differs, c₁ cannot be obtained, or no evaluation yet | Content-bound acts | LC-3 or LC-4 when evaluated. *Not yet evaluated* is never shown as current | `act_lapsed` (unknown states); nothing for *not yet evaluated* |
| LC-6 | **superseded by ⟨act⟩** | A later A12 (or A13) on overlapping classes and scope is **established** | A12, A13 | — (a checkpoint it performed stays *performed*) | derived from settings versions |
| LC-7 | **after run end** (a marking) | Captured after its run's run-ended event | All | Stays; it changes nothing in the ended run and may count at a later run's arrival where current (§4.5) | relation on `human_act` |
| LC-8 | **corrected** | A later record of the same kind names it in *corrects*, with a reason (OF-5) | All | — (both stay readable) | `corrects` |
| LC-D | **declined** — an event, not an act | The person declines at the surface (act-declined event, §2.3) | A4, A6, A7, A12 (A5's negative is A10, an act) | — (satisfies nothing that requires the act) | `act_declined` |

**At an arrival (relations, not states):** *performed* by this act ·
"by earlier act ‹act› at ‹t›" (§4.5) · "answered by ‹n› acts" (joint answer,
§4.3) · **"prior act not counted"** with its reason (content no longer
current · another act kind · captured before arrival under the
governance-phase option) · "act on other content" · "act order unknown"
(governance-phase option only). One act may stand differently at two
arrivals.


---

## 3. Settled distinctions S1–S12 and adopted rulings

Each was checked against the cited bytes at repo 6e18505e3. At v0.7, S9 is
re-quoted from the basis as amended by SCA-V4-001 (header Basis); the other
cited requirement lines are unchanged since that commit.

| ID | Settled distinction | Citation | Consequence |
|---|---|---|---|
| S1 | Graduated autonomy per kind of operation. The agent proposes or applies directly within a scope the person sets, with origin, undo and later checking. | V4-AUT-01; V4-HI-22, -40; D-04 | §5; direct application carries origin, undo route and later-check route |
| S2 | Every result's standing is visible. | V4-AUT-02; V4-HI-12; X-19 | No presentation stronger than the evidence |
| S3 | Agents may prepare checking, acceptance and reliance decisions. They must not represent an act as performed when it was not. Faithful recording of a performed act is allowed, with actor ≠ recorder. | V4-AUT-03; V4-HI-31; d3; SoW REQ-002 | A1/A8 permitted; fabrication prohibited; A9 is a record shape |
| S4 | No agent output is presented as certified, sealed, approved or code-compliant. | V4-AUT-05; X-09 | A7 is never inferred |
| S5 | `success` means the operation ran. It never means acceptance; a proposal stays queued until acceptance and application are recorded. | V4-HI-23, -25 | A2 ≠ A5 |
| S6 | A human act binds to its content, scope and purpose, and lapses visibly when that content changes. | V4-HI-32; V4-REC-05; X-20 | §2.5 |
| S7 | Proposals say "accept", never "approve". | V4-HI-33 | §9 |
| S8 | Conservative defaults. SWB model changes default to proposal with row, multi-row or batch acceptance; the person may widen. | V4-HI-41 | §7 |
| S9 | "Autonomy does not override a workflow's declared checkpoints: whatever the autonomy setting, a checkpoint's required act is requested and recorded as done only when the person performs it. Holding the run at the checkpoint until then is phased to the governance layer (V4-WF-05): in the current phase a checkpoint is plan guidance that the person and the agents manage, and the reserved acts (V4-HI-30) still bind." | V4-HI-42 and V4-WF-05, as amended by SCA-V4-001 | §4. **In force in every phase (R9-1):** the act is requested; it is recorded as done only when the person performs it; the reserved acts bind. **Phased to the governance layer:** holding the run until the act. Whether the run goes on before the act is for the person and the agents in the current phase, and the host's own treatment of its operations decides what the host does (R9-2; §4.0) |
| S10 | External agents use the same catalog, validation, settings and reserved acts, and cannot perform reserved acts. Access is off unless enabled, and local. | V4-HI-50…52 | §5.3 rules 1, 3, 4 |
| S11 | Agent examination is its own activity and need not modify the model. | d3; V4-EXM-21 | A3 ≠ A4 |
| S12 | Shared access does not transfer decision rights. | PRD §4.5; OD-05 | Parity never gives an agent A4–A7 |

**Adopted rulings (DECISION-1), credited only with what they say (R2-11):**

- **D2 (OI-001), first increment, App/shared contracts.** The following are
  reserved to the person:
  - (a) marking work checked;
  - (b) accepting a proposal wherever the active autonomy requires a proposal;
  - (c) engineering approval;
  - (d) relying on a result for a professional purpose;
  - (e) changing the autonomy grant or *enabling* external-agent access.

  No grant widens past a reserved act or a declared checkpoint. The host names
  and enforces its own list (V4-HI-30). Operation-specific additions come with
  OI-021. Host adoption is not shown (DEP-001).

  **Network-destination grant (R8-13; INTEGRATION).** Granting a host's
  agent a network destination, by an allow-list edit or an in-work grant
  (DECISION-5), is a change of the autonomy grant under (e). It is
  recorded as A12, subclass network-destination grant (§2.7).

  **Current-phase reading (R8-11 item 2, restated by R9-2).** SETTLED as a
  reading of D2: the owner confirmed it (OWNER_ITEMS O-25, accepted at
  DECISION-7 of `APP-V4-BASIS-ALIGN-20260928`). The restatement against the
  amended V4-HI-42 is DERIVED (R9-2). "No grant widens past a reserved act"
  **binds**, and the host enforces it through its operations (DECISION-4:
  reserved acts stand). For a declared checkpoint, V4-HI-42's request clause
  and record clause are in force whatever the autonomy setting; whether the
  run goes on before the act is for the person and the agents in the current
  phase, and the host's own treatment of its operations decides what the host
  does. WD I-7 (the acceptance-checkpoint constraint, §4.4) is plan guidance
  in the current phase. Holding the run binds only for governed checkpoints
  in the governance phase.

  **SWBPIPE (SQ-05, 2026-09-28).** SWBPIPE has no class system, no grants and
  no named reserved list. Every change requires the person's Apply, which is
  hard-coded. Its engineer-only Checked mark is DESIGN; approval and reliance
  are not software acts; enabling external access is a launch environment
  variable, not a captured act. Its own autonomy is SWBPIPE owner decision
  OI-016. This is an answer, not adoption (R8-7).
- **D3 (OI-002).** In the App, routine tool-permission and sandbox modes,
  including classifier-based modes, remain the user's own Codex setting per
  project and turn. They govern tool execution only and never stand in for a
  reserved or professional act. Hosts have no classifier permission mode in
  the first increment; the SWB default proposal mode applies.
- **Not from D2/D3.** The following restrictions come from elsewhere and are
  labeled accordingly:
  - A10 reserved: DERIVED (R-1).
  - Operations that perform reserved acts are reserved: DERIVED (R2-2).
  - Disabling external access is A13: INTEGRATION (R2-3).
  - No affirmative App rule for A14: INTEGRATION (R-2).

**Historical, not ruled.** The original-seed V4-HI-30 "at least" list and the
V4-AUT-04 prior drafting default remain historical (AX-001). d3's treatment
table is a proposed interpretation only.

---

## 4. Checkpoints (R-5; R2-5, R2-10, R2-12, R2-17…R2-20; R4-2…R4-6, R4-9, R4-14)

DEL-02-01 declares checkpoints (WD §4.3). DEL-05-01 evaluates them in hosts.
DEL-02-03 owns the hold machine (EXEC-v0.6 §4). This section supplies the act-policy
meaning that those three consume.

### 4.0 Phase 1: checkpoints are plan guidance (R8-1; DECISION-4 D4-1)

The phasing is SETTLED: PRD V4-WF-05 and HOST_INTEGRATION V4-HI-42 as amended
by SCA-V4-001, which applies DECISION-4 D4-1 and its clarification, and
ScopeOfWork TBD-004. The framing of the rules below beyond those texts is
INTEGRATION (R8-1, R8-11; R9-1, R9-2), except who requests the act (AP-12),
which is SETTLED by DECISION-K1 K1-1. The execution rules are EXEC-v0.6 §2.1
(PH-1…PH-10) and §2.2 (GV-1…GV-5); the declaration side is WD-v0.8 §4.3.0
(CG-1…CG-7). This contract states what they mean for acts and policy.

**The amended texts (quoted; R9-1).**

- PRD V4-WF-05: "When a run reaches a workflow's declared checkpoint, the
  required human act is requested, and the run does not record the act as
  done until the person performs it. Holding the checkpoint — the run waits
  until the act is performed — is **phased to the governance layer**, not
  withdrawn (DEC-4): in the current phase, declared checkpoints are plan
  guidance that the person and the agents manage, and neither the App nor a
  host's embedded loop enforces a hold, blocks a run, or reports a workflow
  unsupported because a hold cannot be enforced. Enforced holds are applied
  later to the workflows that need them; the declared checkpoint and the
  definitions that enforcement needs are kept so that every such workflow can
  be served. Reserved human acts (§4.5) are unaffected."
- HOST_INTEGRATION V4-HI-42: "Autonomy does not override a workflow's declared
  checkpoints: whatever the autonomy setting, a checkpoint's required act is
  requested and recorded as done only when the person performs it. Holding the
  run at the checkpoint until then is phased to the governance layer
  (V4-WF-05): in the current phase a checkpoint is plan guidance that the
  person and the agents manage, and the reserved acts (V4-HI-30) still bind."
- **In force in every phase:** the act is requested; it is recorded as done
  only when the person performs it; the reserved acts bind. **Phased to the
  governance layer:** holding the run until the act.

| # | Rule (Phase 1, this increment) |
|---|---|
| **AP-1 Guidance** | A declared checkpoint is **plan guidance**. The declaration still states its required act, reached-when, subject class and held actions (§4.1, §4.2). The person and the agent plan around it, and the agents manage any pause, hold point or gate themselves (EXEC PH-1) |
| **AP-2 No enforcement** | Neither the App nor a host's embedded loop holds, blocks or re-holds a run at a checkpoint. No hold is claimed, no hold-support value is assigned, and no workflow is reported *unsupported* for a hold reason (EXEC PH-2, PH-3). The required-tool check is unchanged |
| **AP-3 Acts only when performed** | A human act is recorded as done **only when the person performs it**, with capture evidence from the capturing surface (§4.5; V4-WF-05: "the run does not record the act as done until the person performs it"; V4-HI-42; EXEC PH-4). An agent never records a human act on the person's behalf. §2, §4.1, §4.2 and §4.5 are in force in both phases |
| **AP-4 Reserved acts stand** | DECISION-1 D2 is unchanged: A4, A5 (where a proposal is required), A6, A7, A12 and enabling external access (A13) stay the person's, with A10 (DERIVED) and P-02. A host enforces its own list through its operations (V4-HI-30; EXEC PH-5). For example, SWBPIPE's Apply is A5 in the person's hands, and enabling external access is A13 (R8-6). "No grant widens past a reserved act" binds (§3, R8-11 item 2) |
| **AP-5 Recording is observation** | A checkpoint's arrival, the request where it can be identified, the act that answers it, and the act-declined, act-lapsed, run-resumed and run-ended events are **recorded** (DEL-04-03) where the arrival is observed. Recording there is required, not optional (R9-1; DEL-02-03 SoW REQ-002; EXEC PH-6), so the person and the agent can see where the plan paused and what was done. The request's record element is RS-v0.8 R16 (PROPOSED representation); where no request can be identified the arrival says "request not identified". Recording is observation, not enforcement. The dispositions of §4.3 may label that record: *waiting* then means "reached; act not yet recorded", never "the run is held" (EXEC PH-6; confirmed by R8-11 item 1) |
| **AP-6 Continued past a checkpoint** | *Action during hold* is not a violation marker in Phase 1. A run action observed after an arrival and before the act that answers it may carry the optional plain annotation **"continued past ‹checkpoint› before ‹act›"**. It is information: never a defect, refusal or finding (EXEC PH-7). The person's own operations never carry it |
| **AP-7 Lapse is recorded; nothing re-holds** | A performed act whose bound content changes is still recorded as lapsed, with an act-lapsed event, and outputs it gated show their standing lapsed (V4-REC-05; §2.5). This is record truthfulness, not enforcement. Re-hold is governance phase only (EXEC PH-8; confirmed by R8-11 item 1) |
| **AP-8 Checkpoint clause of D2** | For a declared checkpoint, V4-HI-42's request clause and record clause are in force whatever the autonomy setting (AP-3, AP-12). Whether the run goes on before the act is for the person and the agents in the current phase, and the host's own treatment of its operations decides what the host does (R9-2, restating R8-11 item 2). WD I-7 (the acceptance-checkpoint constraint, §4.4) is plan guidance in the current phase: the agent proposes where the declaration calls for an A5. Holding the run binds only for governed checkpoints in the governance phase |
| **AP-9 Invalid declarations** | A checkpoint declaration that is invalid (§4.1, §4.2) is reported as a **declaration finding**, invalid with its FB code. In Phase 1 it gives no hold-support value and does not make the workflow *not established* (R8-11 item 3) |
| **AP-10 `governed`** | A checkpoint declared **`governed`** (WD-v0.8 §4.3.1; PROPOSED) is honoured in Phase 1 **only as guidance** (EXEC PH-9) |
| **AP-11 V4-WF-05 and V4-HI-42** | The amended texts are quoted above. Their request clause and record clause are in force in every phase (AP-3, AP-12), and the reserved acts bind (AP-4). Only holding the run until the act is **phased to the governance layer, not withdrawn** (EXEC PH-10) |
| **AP-12 Who requests** | SETTLED by DECISION-K1 K1-1 (the owner's decision of 2026-09-30 in run `APP-V4-DESIGN-PASS-2-20260930`, confirming R9-1's reading of DECISION-4's text). The **agent carrying out the workflow** asks the person for the act when its work reaches the checkpoint, because the declared checkpoint is part of the plan it was given. Its request is an A8 (§2.1; DERIVED). The product's part is: (i) to give the agent the declared checkpoint with the workflow; (ii) to offer the person the means to perform the act; (iii) to record what it observes: the checkpoint's identity, the request where it can be identified, and the act only when the person performs it. A record never says *performed* without the act. Neither the App nor a host's embedded loop issues the request in the agent's place, pauses the run, or otherwise reacts to the arrival. How an App run observes an arrival and a request is defined in EXEC in Wave B; the record element is RS-v0.8 R16, and §4.7 gives the sequence from request to record; this contract defines no observation mechanism |

**Governance phase (retained).** These are relabelled, not deleted: the
re-hold consequences of a lapse (§4.3), the carriage assurance and
*not permitted* outcome of the checkpoint constraint (§4.4), and hold support
with App-side holds (§4.6). A later layer applies them per workflow that
needs them, to checkpoints declared `governed` (EXEC GV-1…GV-3). Every
workflow that needs governance must be serveable by them, so this contract
keeps every element they consume. Where cases below give a governance-phase
value, they read the fixture's checkpoints **as if declared governed**; no
fixture declares the flag (EXEC GV-5; R8-11 item 5).

### 4.1 Acts a checkpoint may require (closed list)

A declared checkpoint requires exactly one of **A4, A5, A6, A7 or A12**
(R-1).
- A recognized act kind outside this list, or no act kind at all, makes the
  checkpoint **invalid**. Examples: A1, A2, A3, A8, A9, A10, A11, A13, A14,
  A15 (below), and design-candidate approval (WD FB-03; R2-10).
- An unrecognized name is preserved and reported **not established**, and is
  never matched to a nearby act kind (WD FB-04).
- **A15** (register workflow revision) is outside the list in this
  increment: no workflow declares a checkpoint requiring it (R12-5). A
  checkpoint requiring A15 is recorded as a possible later extension,
  PROPOSED, with no definition.
- **A16** (decide) is outside the list likewise (R23-8, pass 4): a decision
  package is requested by an A8 and decided at the act control, not at a
  checkpoint; no checkpoint may require A16 in this increment.

### 4.2 Reached-when, subject class and binding (R2-17)

- **Reached-when** is one observable condition. Only its meaning is declared.
  It is one of three kinds:
  - (a) before dispatch of a named required-tool reference;
  - (b) on observed production of a named declared output;
  - (c) on an observed host outcome of a named operation.

  If the run ends without observing it, the disposition is **not reached**.
- **Subject class** is a separate declared element. It does not depend on the
  reached-when kind. The loop binds the *declared* class and never infers it.
  The subject referents are:

  | Subject class | Bound referent | Content-identity source |
  |---|---|---|
  | change items of a named proposal | Proposal and item identities | Change-item content identity |
  | named declared output | The output produced in this run | Output's content identity (file or host) |
  | **objects a named output concerns** (R3-1, INTEGRATION) | The objects identified in a named read or examination output, for example the rows an examination covered | Subject content identities as read in that output |
  | objects changed by a named outcome | The created and changed object identities reported per applied item (R2-14) | Subject content identity after application |
  | **targets of the held call** — valid only with reached-when kind (a) *before dispatch* (R3-2, INTEGRATION) | Targets named by the held call | Subject content identities from the relied-on read the call cites, never from argument text |
  | **grant setting** | The setting content named in the checkpoint's **declaration**: the classes, grant values and scope. A run-dependent scope is declared as a binding rule resolved at arrival, for example "targets of the held call". An A8 may present this content but never changes the subject (R5-3, INTEGRATION; supersedes R4-9's A8 precedence). | A12 setting content (§2.5) |

- An **A5 checkpoint** must use reached-when kind (c) *proposal queued*. Its
  subject is that proposal's change items. Any other A5 combination is invalid
  (DEL-02-01 declares this).
- The subject class *targets of the held call* is valid only with
  reached-when kind (a) *before dispatch*. Declaring it with kind (b) or
  kind (c) makes the checkpoint invalid (R3-2).
- The subject class *objects a named output concerns* lets a review-only
  workflow require A4 on the rows it examined. The act binds to those rows'
  subject content identities as read (R3-1).
- An A12 checkpoint whose declaration names no setting content is
  **invalid**, unconditionally (R5-3; fixes V3-A m-5). This is decided when
  the declaration is read, before any run, and is reported before the run
  (WD FB-17; EXEC §4.14). An A12 made on setting content different from the
  declared content satisfies nothing at that checkpoint.
- The satisfying act must be bound to the same referent's content. An act on
  other content does not satisfy the checkpoint, even if its kind matches.
  This includes an A12 on different setting content.

### 4.3 Dispositions, negatives, lapse and run end

The vocabulary is shared: **waiting · performed · resolved negatively · lapsed
· not reached · unknown** (WD §4.3.4).

In Phase 1 these words are **record labels** (AP-5): they state what the
record shows, and nothing is held. The re-hold consequences in the lapse
bullet below are **governance phase (retained)**.

- **performed.** Capture evidence of the required kind, bound to the current
  content of the bound subject (§4.5).
- **resolved negatively.**
  - For A5: A10 on the subject's items.
  - For A4, A6, A7 or A12: an **act-declined event** (§2.3).

  The declaration's "on negative decision" path governs. A negative never
  counts as *performed*.
- **Mixed item decisions** (A5). Each item carries its own A5 or A10, or
  neither while it is still queued. The disposition rule is WD §4.3.7
  (PROPOSED; R2-18), which this contract adopts by citation:
  - "Partial" is a **per-item annotation**, not a seventh disposition.
  - Items that leave without a decision (stale, A11, host refusal) are shown.
  - A *performed* over a reduced subject is never shown as "all accepted".
  - DEL-03-02 supplies item-left events.
  - DEL-02-03 has **confirmed** the rule (R4-7; EXEC §4.11) and added:
    - MX-3: a lost decision observation gives *unknown*;
    - MX-6: when every item has left, the arrival closes "replaced" at the
      next arrival;
    - MX-8: an application error or an unknown outcome after A5 leaves the
      disposition unchanged, with an annotation.
- **Resume point (R4-3; EXEC HD-5).** When an arrival becomes *performed*, or
  *resolved negatively* with a proceed or return path, the first run action
  after that change is the **resume point**. It is recorded as a
  **run-resumed event**. "Before resume" and "after resume" are measured
  against this event.
- **Lapse (R2-19; R4-3; EXEC §4.7).** Lapse can happen at any time after
  performance, and an **act-lapsed event** is always recorded and presented.
  - **Before the run resumes:** the disposition returns to **waiting**, shown
    as "waiting — lapsed at ‹t›", for a new act on current content. This is
    recorded in both phases.
  - **After resume, run live — Phase 1 (AP-7; EXEC PH-8; R8-11 item 1):**
    the act-lapsed event is recorded and presented against the affected
    referents, labelled **"act lapsed at ‹t›"** (nothing says *waiting*;
    R8-12 item 1), and outputs gated by the act show their standing **lapsed**.
    The run is **not** re-held. The agent re-requests the act as its plan
    requires, and a new act over the current scope is recorded when the
    person performs it. The person's own undo or edit is recorded as the
    person's operation and never carries "continued past ‹checkpoint› before
    ‹act›".
  - **After resume, run live — governance phase (retained), governed
    checkpoints:** the **same arrival** is re-held, shown as
    "waiting — re-held, lapsed at ‹t› after resume".
    - What the re-hold stops depends on the hold-support value (R6-3;
      §4.6). Under *enforced by the host loop* the run stops at its **next
      action boundary**; under *enforced on the host route* the host refuses
      the held host operations and any other action is recorded as *action
      during hold*; under *not established* or *not enforceable* nothing is
      stopped and actions are recorded as *action during hold*. Actions in
      flight complete and are observed. Nothing done is recalled or undone.
    - Actions taken between the resume point and the lapse stay recorded.
      Outputs whose promised standing names this checkpoint as gating show
      standing **lapsed** for the affected referents.
    - The act request is issued again for the **whole bound scope**, with the
      lapsed referents marked.
    - A satisfying act makes the arrival *performed* with the next performance
      ordinal, and a new resume point follows.
    - The interim "performed + act-lapsed event" display is withdrawn.
  - **Whatever causes the lapse re-holds (R5-5; governance phase).** This
    includes the person's own undo. The person's undo is the person's
    operation and is never recorded as "action during hold".
  - **A5 and A12 never re-hold** (governance phase), and in both phases an
    undo never lapses A5 or A10 on the reversed item.
    - Applying an item does not lapse its A5, and a basis failure is the
      stale rule.
    - An undo never re-holds an A5 arrival.
    - An A12 is superseded, not lapsed (§2.5).
  - **lapsed** as a standing disposition is used only for a checkpoint whose
    run has ended. If the run ends while re-held, the disposition stays
    *waiting* with the run-ended event (EXEC RH-7).
  - Partial lapse (only some referents): the whole bound scope is shown with
    the lapsed referents marked. **Joint answer (SETTLED by DECISION-K1 K1-3;
    EXEC §4.7 JA-1; U-03 closed):** two or more acts may together answer one
    arrival, and each cites its items. When one act covered several items
    and only some change, a new act on the changed items alone answers the
    checkpoint together with the earlier act for the unchanged items. A new
    act over the whole scope also answers it. This holds in both phases.
- **Run ended while waiting (R2-5; R4-4).** The disposition stays
  **waiting**, with a run-ended event. The run is never resumed (§2.3). An act
  performed later is recorded, shown "after run end", and changes nothing.
- **unknown.** Observation was lost. Never shown as *performed*.

### 4.4 Acceptance-checkpoint constraint (DERIVED from V4-HI-42 + D2b; R2-12)

If a declared checkpoint requires A5 on an operation's result, that
operation's treatment in that run is **propose**, whatever the grant.

**Phase 1 (AP-8; R8-11 item 2 and R8-12 item 2, restated by R9-2; R8-10).**
This rule is **plan guidance**: the
agent submits the operation as a proposal, as the declaration asks, and the
host's own treatment decides. Where the active grant lets the host apply
directly, no proposal arises and the host may apply. An A5 checkpoint, whose
reached-when is kind (c) *proposal queued* (§4.2), is then **not reached**:
nothing is requested by reason of an arrival that did not occur, no A5 is
forced, and none is recorded. The record shows the direct application under
the person's grant (R9-2 as corrected by R10-1). V4-HI-42's request clause
applies to a checkpoint the run reaches: where a checkpoint of any kind is
reached while a grant permits direct application, its act is requested and
its disposition is *waiting* ("reached; act not yet recorded") until the
person performs it. The App carries and enforces no constraint,
and reports nothing as *not permitted* on the constraint's account. The agent
never adds a field that the host's schema lacks (R8-10): SWBPIPE's strict
preflight refuses unknown fields (SQ-02 (a), SQ-31). On SWBPIPE every change
waits for the person's Apply in any case (SQ-05), but that is the host's
fixed treatment, **not** host-held carriage (SQ-02 related fact; R2-12). The
rest of this section is the **governance-phase definition (retained)** for
governed checkpoints.

- The change request carries a **governing checkpoint constraint**:
  {workflow run, checkpoint name, required act A5, operation} (DEL-03-02
  P §3.3).
- **Carriage assurance (R4-14, final per R5-2; ADAPTER §5.1–§5.3).** The
  constraint reaches the host route with one of four assurances:
  - **host-held**: the constraint is held on the host side. Either the host
    derived it from its own resolved copy of the declaration, or it received
    the constraint and verified it against that copy. The host loop's own
    evaluation (LOOP §6.2) is host-held.
  - **model-supplied**: composed by the model as a tool argument.
  - **App-assured**: added or verified by App code on the dispatch path. **Not
    available in this increment**, because interposed App code (HP-1) is not
    adopted (R4-2).
  - **absent**.

  A constraint the host merely **received** from an outside caller keeps its
  source's assurance, model-supplied or App-assured.

  **Only host-held carriage satisfies R2-12.** A model-supplied constraint
  does not: an omission would let a direct request pass (ADAPTER GC-2,
  GC-3). An expected constraint that was not carried is recorded as an
  evidence limit; where the host's schema has no element for it, the limit
  reads "constraint not carriable on this host" (R8-10). This makes the
  SQ-02 option in which the host evaluates the declaration itself the only
  route to satisfaction as the hold routes now stand. SWBPIPE does not offer
  it (SQ-02 answered 2026-09-28: route (iv), none planned).
- A direct request under the constraint is **not permitted**, and the outcome
  names the constraint as the governing treatment. It is never converted into
  a proposal. The agent may submit a proposal separately.
- A workflow that wants direct application followed by a person's act must
  declare A4 on the applied result instead.
- **Relay question (DEP-001).** Does the host route receive the constraint, or
  does it evaluate its own copy of the declaration? A missing constraint looks
  the same as no constraint at all. Until host evidence exists, dependent
  fixtures are **AWAITING INPUT** (FX-29; LOOP FX-C9, PANEL PC-24, WD VC-11).
  **Answered 2026-09-28 (SQ-02):** neither; route (iv), none planned, and a
  constraint field would be refused as an unknown field (SQ-02 (a)). The
  answer does not supply the input, so FX-29 keeps the AWAITING INPUT token
  with that annotation; planning a route is a SWBPIPE owner decision (ANS
  §2), and host joins are deferred (DECISION-3).

### 4.5 Which evidence satisfies a checkpoint (R-5; R2-20)

- Any identified recorder distinct from the decision actor produces a
  conformant **record shape** (A9, SETTLED S3).
- **Satisfaction** requires capture evidence from the **capturing surface**:
  - the host's act facility, for acts on host content (V4-HI-31);
  - the App interface, for acts in the App (EXEC §5, CAP-1…CAP-9; CAP-8 for the person's identity).
- A faithful record by another recorder is valid as a record, and it must cite
  that evidence. An act is recorded as performed on the capture evidence,
  never on an agent-authored record alone (both phases; AP-3). In the
  governance phase the loop also resumes only on it.
- **Relay question (DEP-001):** the host's capture-evidence reference.
  Without it, no host-content checkpoint can be *performed*. Any host-specific
  capture requirement is the host's (U-04). **Answered 2026-09-28 (SQ-01):**
  SWBPIPE exposes none (§2.6); storage and actor identity are SWBPIPE owner
  decisions (PB-TBD-002; DEL-16-03).
- **Never act evidence (R4-12):**
  - answers to Codex user-input or MCP elicitation requests;
  - A14 settlements;
  - conversation statements.

  See §2.6.
- **Earlier acts (SETTLED by DECISION-K1 K1-2; EXEC SP-6; U-14 closed).** In
  the current phase an act captured before the arrival counts toward it when
  it is of the required kind and the content it was made on is still current
  (for A12, its established setting is still in force).
  - The record cites the earlier act and its time.
  - An earlier act whose content is no longer current, or whose kind
    differs, is shown **"prior act not counted"**, recorded with that
    reason. This is the one wording of the label (R12-10; RS-v0.8 L-13):
    the reasons are *content no longer current*, *another act kind* and
    *captured before arrival (governance-phase option)*.
  - The rule adds no ordering *between* act kinds.
  - **Governance-phase option (retained; PROPOSED; EXEC SP-6F; formerly
    this rule, R4-5).** A workflow that takes up the governance phase may
    require a fresh act, counted only if captured **at or after the
    arrival**, ordered by a request relation where the capturing surface
    records one, and otherwise by evidenced times. Under it any earlier act
    is shown "prior act not counted", and an act whose
    order cannot be established does not count ("act order unknown").
- For A12, the act counts only when its control relation is **established**
  (§2.5).

### 4.6 Hold support and App-side holds — governance phase (retained; R4-2; R8-1, R8-2; DECISION-2 D6; EXEC §2.2, §2.3, §3.6)

**Phase 1 (AP-2; EXEC PH-2, PH-3).** No hold-support value is assigned, no
hold is claimed, and no workflow is reported *unsupported* for a hold
reason. The requirement check depends on the required tools and the channel
state. Checkpoints are listed as guidance, and "continued past ‹checkpoint›
before ‹act›" replaces *action during hold* (AP-6). **The rest of this
section is the governance-phase definition, retained**: it is relabelled, not
deleted, and applies to checkpoints declared `governed` (EXEC GV-1, GV-2).

- A governed checkpoint relied on in a run is only as strong as the
  surface's ability to hold the run. For each governed checkpoint and acting
  surface, the required-tool compatibility report states its **hold
  support** (EXEC §3.6). Each takes exactly one of four values (R5-1):

  | Value | Meaning | Requirement check (governance phase) |
  |---|---|---|
  | **enforced by the host loop** | Embedded route: the host loop holds the run (LOOP §2.4.4). SWBPIPE has no host loop (SQ-20), so no host evidence for it can exist now | Passes. Holds are subject to host evidence (DEP-001). |
  | **enforced on the host route** | The host holds or refuses the operation through a **host-held** constraint (§4.4), evidenced by the host's answer to SQ-02 and a candidate. Not offered by SWBPIPE (SQ-02 route (iv)) | Passes |
  | **not established** | Depends on a host answer not yet given (SQ-02), or on unagreed exposure. SQ-02 was answered for SWBPIPE on 2026-09-28, and SQ-11 is answered, so against SWBPIPE neither cause gives this value now: HS-3 (c) decides (R8-2; EXEC §3.6) | *not established*. Never a pass, and never "unsupported". |
  | **not enforceable** | No mechanism exists on this surface as the hold routes now stand. Examples: App-only steps with no host operation (R4-2 / D6); a constraint carried only as model-supplied, once SQ-02 is answered with no host-held route (HS-3; before that answer, *not established*). SWBPIPE has answered SQ-02 (R8-2) | *unsupported*, reason "checkpoint hold not enforceable on this surface" (R4-8) |

  The EXEC-v0.1 values "enforced before dispatch" and "held after
  observation", and the interim value "host-enforced for host operations",
  are retired.
- **Classification by held actions (R6-1; EXEC §3.6 HS-1…HS-5).** The value
  is decided by **what the checkpoint must hold**, not by how it arrives:
  - **Host loop (HS-2):** *enforced by the host loop*.
  - **Host-held class (HS-3):** every held action is a host operation on the
    external channel, such as the governed operation, or the host operations
    after arrival until the act. The value follows SQ-02:
    - answered, with host-held carriage evidenced on a candidate → *enforced
      on the host route*;
    - unanswered → *not established*;
    - answered with no host-held route → *not enforceable*. **SWBPIPE:
      answered with no host-held route, 2026-09-28** (route (iv), none
      planned). A later SWBPIPE decision to plan a route is a revision
      trigger.
  - **Exposure (HS-4):** a held host operation with unagreed exposure gives
    *not established*, except where SQ-02 is answered with no host-held
    route; then HS-3 (c) decides. So HS-4 does not mask SWBPIPE entries
    (R8-2; SQ-11 answered: no exposure element).
  - **App-side class (HS-5):** at least one held action is App-side, such as
    an App agent turn, an App tool or harness action, or an App file write or
    return step. In App runs this is *not enforceable* (D6), whatever SQ-02
    returns.
  - **Invalid declarations (HS-1)** take **no value**, and in the governance
    phase the check is *not established*. In Phase 1 an invalid declaration
    is a declaration finding only (AP-9).
- **What "held" means for each value (R6-3):**

  | Value | What happens at the hold |
  |---|---|
  | *enforced by the host loop* | The run stops at its next action. |
  | *enforced on the host route* | The host refuses the held host operations. Any other action is recorded as *action during hold*. |
  | *not established* / *not enforceable* | Nothing is stopped. Actions are recorded as *action during hold*. |

- **Consequences, each as a Phase-1 result and a governance-phase value (R5-1,
  R6-1, R8-1, R8-2).** The governance-phase values read the fixture's
  checkpoints as if declared governed (R8-11 item 5).
  - **E1 run from the App through the external channel (surface X).**
    *Phase 1:* the requirement check is decided by the required tools and
    the channel state (EXEC MT-2). `CP-accept` and `CP-check` are guidance;
    nothing is held; the A5 and A4 are recorded only when the person
    performs them. *Governance phase:*
    - `CP-accept` → **not enforceable** (HS-3 (c); SQ-02 answered
      2026-09-28: route (iv));
    - `CP-check` (it holds the Return step, which is App-side) → **not
      enforceable** (HS-5);
    - the workflow → *unsupported* ("checkpoint hold not enforceable on this
      surface: CP-accept, CP-check").
  - **`CP-L4` (L-ACT-4)** holds only host operations: the run's further host
    operations after T16 until the A4. *Phase 1:* `CP-L4` is guidance. Its
    arrival at T16 and the A4 at T16a are recorded when observed. A run
    action after the arrival and before the A4 may carry "continued past
    CP-L4 before A4". Neither the App nor a host loop holds the run, and the
    workflow is not *unsupported* for a hold reason. *Governance phase:*
    - App run over X: **not enforceable** (HS-3 (c); SQ-02 answered
      2026-09-28) → workflow **unsupported** (was *not established* at v0.5;
      I2 P2.7);
    - host loop: *enforced by the host loop* (SWBPIPE has no host loop,
      SQ-20);
    - a variant that also holds an App-side return step is *not
      enforceable* in App runs (FX-48 (d)).
    - Counterpart in DEL-04-02: AS F6d (the L-AS-4 A4 on S-4, declared to
      hold only host operations → HS-3); AS F6c, which holds App agent
      turns, is HS-5.
  - **Advice to workflow authors (WR-11; governance phase).** Keep a governed
    checkpoint's held actions on host operations if it must be enforceable
    from the App. It is then enforceable only on a host that offers and
    evidences a host-held route. Against SWBPIPE (SQ-02 answered: route
    (iv)) no governed checkpoint is enforceable from the App on X, and every
    such workflow run from the App on X is *unsupported* in the governance
    phase. The advice stands for a host that offers a host-held route (I2
    P2.13). In Phase 1 the advice does not affect the check.
- This contract, and every consumer that cites it, **never states or implies an
  App hold that the surface cannot enforce**. In Phase 1 no hold is stated at
  all.
- In the governance phase, any run action taken while an arrival of a
  governed checkpoint waits, and not stopped under the value in force, is
  recorded as **action during hold** with its reference. It is never hidden.
  Under every value other than *enforced by the host loop*, App-side actions
  continue and are recorded this way (R6-3). In Phase 1 the optional
  annotation of AP-6 applies instead.
- **App-side run holds (`UNRESOLVED{D6}`).** D6 is **closed for Phase 1** by
  DECISION-4, where no hold point is used, and **re-opens when the
  governance phase is taken up** (R8-2; U-D6). For the governance phase:
  - HP-1, interposed App code holding a call before dispatch, is **not
    adopted**;
  - HP-2, reliance on supplier `turn/interrupt`, is **not adopted**;
  - HP-3, an App named-rule *decline* of a tool-permission request, remains a
    **permitted best effort** under D3 and R-2. It never answers
    affirmatively and never counts as a hold guarantee.
- A reached-when kind (a) on a **harness capability** is **not holdable** in
  App runs as the hold routes now stand (R4-21; governance phase). In Phase 1
  such a workflow's check is *not established* for a required-tool reason:
  the harness-capability reference is unresolved (WD U-08; EXEC U-E10,
  MT-15; R8-11 item 3), not a hold.
- In host loops, holding is the host loop's in the governance phase
  (DEL-05-01 receiving; OI-013), with the value *enforced by the host loop*.
  In Phase 1 a host's embedded loop enforces no hold either (EXEC PH-2;
  DECISION-4 clarification).
- **SQ-02 answered (R8-2).** SWBPIPE answered on 2026-09-28: no host-held
  route; *enforced on the host route* is not available against SWBPIPE (§4.4;
  U-04). This is the **governance-phase input**. The SQ-02 answer decides
  holds only for checkpoints on **host operations**; App-only checkpointed
  workflows remain *not enforceable* in the governance phase whatever
  SWBPIPE answers (R5-10; F-16).
- The policy meaning of a checkpoint's **act** is unchanged by phase or by
  weak hold support: it is still satisfied only by capture evidence (§4.5)
  and still reserved to the person (AP-4). In the governance phase a governed
  checkpoint also overrides any grant (S9). Weak hold support limits what can
  truthfully be **claimed** about enforcement. It does not weaken what the
  act means.

### 4.7 Request → capture → record (ACT 7; PROPOSED sequence over SETTLED rules)

The rules are settled elsewhere: who asks (AP-12, DECISION-K1 K1-1), what
counts as evidence (§2.6, §4.5), earlier acts (K1-2), the joint answer
(K1-3), the person's identity (K1-4). This is the order in which they apply,
with the failure behaviour at each step. The record entries are RS-v0.8 §13.
Nothing here holds a run in Phase 1.

| Step | What happens | What can fail | Who reports it | Record left | What happens next |
|---|---|---|---|---|---|
| **RC-1 Arrival** | The run's work meets the checkpoint's reached-when; the executor observes it (EXEC; LOOP §2.4.1). If an earlier act of the required kind on still-current content already covers the bound scope, the arrival is *performed* by it at once (§4.5) | The event is not observed; observation is lost | The executor (observer) | Not observed: nothing, and the disposition is *not reached*. Lost: *unknown* | Otherwise RC-2 |
| **RC-2 Request** | The agent carrying out the workflow asks the person for the act (A8), naming kind, subject and purpose (AP-12). The product does not ask in its place | The request cannot be identified; the agent does not ask | — | Identified: `act_request` (R16). Not identified: the arrival says "request not identified" — an absence, not a defect | The arrival is *waiting* (a record label in Phase 1) until RC-4 |
| **RC-3 Means** | The product offers the person the capturing surface for the kind (§2.6): the App act control (EXEC CAP-2; DEL-01-04 AAC-v0.2) for App content and for A15; the host's act facility for host content; the host's control for A12 | No surface exposes capture evidence (SWBPIPE: none, SQ-01) | The App, from the host's answer | "no capture-evidence reference" stays a limit; no host-content act can be recorded as performed | The person may still act at the host; the App records only what it can cite |
| **RC-4 Act or decline** | The person performs the act, or declines. The capture evidence holds the actor (identity from what the App observes, "identity not verified", K1-4), kind, bound content identity with method, scope, purpose, time and the arrival where known (EXEC CAP-3) | The control is closed without an act; an answer arrives through a supplier input or elicitation request (never evidence, CAP-6); the act is made on other content | The capturing surface; the App for the input answer | Nothing; or an act on other content, recorded and satisfying nothing ("act on other content") | The App may present its own control (CAP-6). A decline gives an act-declined event and *resolved negatively* |
| **RC-5 Record** | The writer records the act (direct capture) or another recorder records it faithfully citing the same evidence (A9); the disposition changes: *performed*, with "by earlier act" or "answered by ‹n› acts" where they apply; for A12, per its control relation (§2.5) | The write fails (RS FC-1); two recorders (RS FC-3); the A12 control is *pending*, *refused* or loses confirmation | The writer; the reader; the control | Late write with "record write failed"; one act with two records; *waiting* "A12 awaiting control confirmation" / "A12 refused by control: ‹reason›"; *unknown* | Display compares *missing in record* until written |
| **RC-6 Afterwards** | The first run action after *performed* is the resume point (run-resumed event). Later changes of bound content lapse the act (§4.3; Phase 1: "act lapsed at ‹t›", nothing re-held) | A referenced source becomes unresolvable at read (RS FC-8) | The reader | The label stays as recorded, with the limit; never recomputed to *waiting* | The agent re-requests as its plan requires; a new act gets the next performance ordinal |

**A15** runs RC-2…RC-5 with no arrival: the agent may ask the person to
register a revision (A8); DEL-01-04's App act control captures the A15
(AAC-v0.2 §4.2); the record binds the revision identity, the reviewed draft
content and, for a new revision, the prior revision (R17-11), or each entry
of a several-entry act (L-4). The registration that follows is DEL-02-02's;
its outcome is reported beside the act, which stands even when registration
did not complete (AAC AK-f; WR RB-8). **A12
network-destination grants** follow LOOP §5.1.1 instead (NW-11…NW-13): only
the requesting call waits, which is not a checkpoint hold. From v0.8 its
steps and failure rows are LOOP §5.3 DF-5 (Q-1…Q-9) and DF-F1…DF-F12: the
request (RC-2) is the destination request entry call; the means (RC-3) is
the host's in-work prompt; an unanswered request ends *unanswered at end*
at the run's end or the turn's cancel and is never a grant.

---

## 5. Autonomy-grant model

### 5.1 Inputs (semantic)

| Input | Meaning | Supplier / standing |
|---|---|---|
| *operation identity* and *operation class* | The catalog operation and its host-named class | DEL-03-01 (V4-HI-01/02); host names classes (V4-HI-30) |
| *catalog human-act class* | **none** · **may apply within granted autonomy** · **proposal only** · **reserved to the person**, all SETTLED by V4-HI-02. Fifth value: **no policy basis**, with *reason* ∈ {omitted, unassigned, pending OI-021}, labeled INTEGRATION (R-3.5; R2-1). | Values from §8. OI-002 is not a class value (D3; R-2). |
| *consequence statement* | Effect, reversibility, available examination, intended delegation (d3) | Vocabulary open (U-02); a PROPOSED vocabulary is drafted for the owner's phase review in §8.5 and assigns nothing |
| *grant state* for the class | **effective (person-set)** · **effective (policy default)** · requested by agent (A8) · set by person, not yet confirmed · unconfirmed · not set · refused (reason). Each state carries a **grant value** (direct/propose) and a scope. | DEL-04-02 (R-8; R2-6) |
| *host default* | The policy-class record's default for a consequential class | §8.3 P-03; others U-06 |
| *checkpoint state* | Whether a declared checkpoint applies, the act it requires, and any governing checkpoint constraint | DEL-02-01; DEL-02-03; DEL-05-01; P §3.3 |
| *actor* | The person, the embedded agent or an external agent | Host route |
| *external enablement* | A13 state on this machine | The person; the host |

### 5.2 Treatments

| Treatment | Meaning |
|---|---|
| **execute** | Run with no associated human act (for example a read or A3); the result carries its standing |
| **apply directly** | A2 through the host's one route, with origin, relied-on basis, undo route and later-check route |
| **propose** | The V4-HI-23 lifecycle; queued until acceptance and application are recorded |
| **request the person's act** | The agent may only request (A8); the person performs the act through the capturing surface |

### 5.3 Resolution order for an agent actor

Treatment is resolved on the **host route**, at validation and again at
application. The loop and the adapter relay intent and do not decide treatment
(R-3.1, INTEGRATION). The first matching rule applies.

1. **External actor, A13 not performed (access off)** → *channel not enabled*.
   SETTLED S10; V4-HI-52.
2. **Declared checkpoint.**
   - At a checkpoint: *request the person's act* (S9).
   - An A5 checkpoint constraint on this operation forces *propose* (§4.4).
   - **Phase 1 (AP-8, AP-12; R9-1, R9-2):** the checkpoint's required act is
     requested in every phase, by the agent carrying out the workflow
     (AP-12), and is recorded as done only when the person performs it. On
     the host route rule 2 is plan guidance for the agent: the host's own
     treatment of its operations decides what the host does, and a declared
     checkpoint creates no host obligation. Rule 2 binds on the host route for
     governed checkpoints in the governance phase. Rules 1 and 3–8 are
     unchanged, and rule 3 (reserved acts) binds in both phases (AP-4).
3. **The operation performs A4, A5, A6, A7, A10, A12 or A13** → *request the
   person's act*. The operation's class is *reserved to the person*
   (P-02, DERIVED from S3 and D2; R2-2). "Perform" includes creating or
   changing the host's own act state, for example a row's checked state or an
   item's acceptance disposition. Faithful recording is never done through
   such an operation.
4. **Catalog class = reserved to the person** → *request the person's act*.
   ADOPTED D2; S10. Operation-specific additions are pending OI-021.
5. **Catalog class = no policy basis** (reason omitted, unassigned or pending
   OI-021) → INTEGRATION (R-3.5; R2-9):
   - Proposing (A1) remains available because proposing is agent-available
     for any change (S3). It confers **no permission**. The proposal itself
     changes nothing. Any effect requires the person's reserved A5 and
     application through the host route.
   - Direct application is **not permitted**.
   - An A12 that tries to widen the class is **refused (reason: no policy
     basis)**.
   - REQ-004's hold on **production** stands. Nothing that depends on the
     value proceeds until the decision: no policy configuration, class
     assignment, permission-policy implementation or connected integration.
   - Records and displays show "no policy basis — held (‹reason›)".
   - Fixtures report such cases as **held**, never as passes.
6. **Catalog class = proposal only** → *propose*; no grant can widen it.
7. **Catalog class = may apply within granted autonomy** (R2-6):
   - **effective (person-set)** with grant value *direct* and the operation
     inside the scope → *apply directly*.
   - **effective (policy default)** → the policy-class record's default
     applies. This is *propose* for P-03. A default opens the direct branch
     only if the record's default is *direct* with a decision basis, and no
     such record exists in the first increment.
   - Requested by agent, set but not confirmed, unconfirmed or refused → no
     direct branch. *propose* is available, and a direct request is *not
     permitted*.
   - **not set** (no setting and no default) → treated as rule 5, reason
     *unassigned* (U-06).
8. **Catalog class = none** → *execute*. DERIVED caution: an effectful
   operation assigned "none" needs its own decision basis.

**Undo (R3-4, INTEGRATION).** An undo (fixture OP-C10) reverses a receipt.
It is resolved by rules 1–8 using the **policy-class record of the operation
whose receipt it reverses**, including that operation's grant state and scope.
It has no class of its own. Examples:
- undoing an OP-C9 application under an effective direct grant for the OP-C9
  class may be applied directly;
- undoing a P-03 application with only the policy default in force is
  *propose*;
- undoing the effect of a reserved operation is *request the person's act*.

For the **person** as actor, the same route and validation apply. Agent grants
do not gate the person's operations. A person performing A12 or A13 is the
reserved act itself.

### 5.4 Person-set scope and grant states (R-8; R2-6)

- The grant has a **scope** element. Its dimensions are representation-
  neutral, for example model or workspace, object set, run, period and
  consequence.
- The **grant value** *propose* (the person keeps proposals, as in V4-EXM-22)
  is different from the catalog class *proposal only*. The person can widen
  the first but not the second.
- **effective (person-set)** requires A12 evidence and confirmation by the
  control. A person-set state without A12 is a defect.
- **effective (policy default)** requires no A12. Settings-in carries the
  policy-class record reference and its default, with no setting actor and no
  requester.
- Settings-in carries **requester** and **setting actor** separately. An
  agent-originated change is *requested by agent (A8)*.
- Two settings references are recorded per operation:
  - the reference at the route decision;
  - the reference in force at application, as the host reports it, or
    otherwise *unconfirmed*.

  When the standing at drafting differs from the treatment at resolution,
  both are recorded. A later change never re-labels an earlier operation.

### 5.5 Changes during work (R-3.6, R-3.7; host enforcement DEP-001)

- **Narrowing:**
  - An already-queued proposal is unaffected.
  - An operation not yet applied is re-resolved at application. A direct
    request that no longer has an effective direct treatment is *not
    permitted* and is never converted.
- **Widening** never converts a queued proposal into direct application.
- **Supersession.** A later A12 supersedes the earlier one (§2.5).

### 5.6 Widening rule

The person widens the grant by performing A12. A widened grant cannot:

| # | Cannot | Basis |
|---|---|---|
| W-a | make an agent the decision actor of A4–A7, A10, A12 or A13, or fabricate a human act | S3, S4; D2; R-1 |
| W-b | bypass a declared checkpoint or the §4.4 constraint | S9; D2. In every phase a widened grant never records or substitutes the checkpoint's act, which is requested when the run reaches the checkpoint (V4-HI-42; ScopeOfWork TBD-004; R10-1). The hold and the §4.4 constraint bind for governed checkpoints in the governance phase (R9-2) |
| W-c | authorize a reserved act or operation for any agent | D2; S10; REQ-006 |
| W-d | convert a **proposal only** class | V4-HI-02 |
| W-e | apply to a **no policy basis** class. That A12 is refused. | REQ-004; R2-9 |
| W-f | enable external access. That is A13. | V4-HI-52; D2e |
| W-g | confer professional standing | S4 |
| W-h | drop the origin, undo and later-check obligations | S1; V4-HI-22 |
| W-i | convert a queued proposal | R-3.7 |
| W-j | affect routine tool permission (A14) | D3 |

---

## 6. Treatment → runtime outcome map (R-3; R2-4)

Runtime non-success outcomes use DEL-03-01 §4.1. Proposal and operation
outcomes use DEL-03-02 P §9 (R-7).

| # | Situation | Runtime outcome | Also |
|---|---|---|---|
| 1 | External actor; A13 not performed | **channel not enabled** | Never *unavailable* |
| 2 | Failed catalog precondition | **unavailable**, with the same reason for H, E and X | Only this case |
| 3 | Treatment *execute* | Result with standing | — |
| 4 | Treatment *apply directly* | P §9: one of: <ul><li>applied with receipt and resulting objects (R2-14);</li><li>refused with reason;</li><li>application error with effect statement;</li><li>outcome unknown, attributed to the observer</li></ul> | Origin, basis, both settings references |
| 5 | Treatment *propose* | P §9 lifecycle: queued → accepted (A5) / rejected (A10) / withdrawn (A11) / stale → applied with receipt | "Queued" until recorded (S5) |
| 6 | Direct requested without an effective direct treatment (rules 5 and 7, §5.5) or under a §4.4 constraint | **not permitted**, naming the governing treatment, policy-class record or checkpoint constraint | Never silently converted. The agent may submit a proposal separately. |
| 7 | Treatment *request the person's act* (rules 2–4) | **not permitted**, naming the governing record | An A8 request is **offered**. An A8 exists only if the agent actually issues it, with the requester identified (R2-4). |
| 8 | Reserved-class entry | **Always offered** where the entry is exposed. An agent invocation is handled as row 7. | Never withheld for a class reason. Never reported as *not exposed on this surface*, *unavailable* or *missing* because of its class (R2-4; C §2 invariant 5). |
| 9 | Entry not exposed on the acting surface (the host's per-surface exposure element) | **not exposed on this surface**, reported by the host | Exposure is not a policy consequence |
| 10 | Operation absent from the catalog edition offered to the loop | Loop-side **not offered** failure; never dispatched (DEL-05-01) | Distinct from row 9 |
| 11 | Any other failure | **error** | Evaluated basis on every non-success |

A host refusal on validation is *refused* (an A2 outcome). It is never A10.

**Received host terms (R8-5; INTEGRATION; SQ-05, SQ-06, SQ-09, SQ-13).**

| SWBPIPE term | Received as | Never |
|---|---|---|
| `unsupported_method` / `unsupported_change` | Host-reported **not exposed on this surface** (row 9's outcome), relayed | *not permitted*; a class value; a grant |
| #885 `withdrawn` (the person cleared the queue) | An **item-left** event, "cleared by the person, no decision record" | A10 or A11 |
| `validation_rejected` at Apply | **refused — invalid** at application | A10 |
| `controller_unavailable` (no *channel not enabled* code exists) | **endpoint unavailable**; the channel shows *disabled* (R8-6; §2.6) | *channel not enabled* reported by the host |

- Against SWBPIPE's external channel X, rows 6–8 do not arise as written.
  There is no direct mode and no Apply method, and a request for Apply is
  refused `unsupported_method` (SQ-06). R2-4 (reserved entries always
  offered, and *not permitted* naming a rule) is recorded as **not met** by
  this host (DEP-001). It is not repaired App-side, and the App never
  presents SWBPIPE's no-Apply rule as a class value or grant.
- Whether that no-Apply rule is a channel rule or a first-journey property is
  a SWBPIPE owner decision (SQ-06). The App needs nothing from it now.

---

## 7. SWB model-change class — DERIVED class, accepted default

> The class value is **DERIVED** from V4-HI-41 "the person may widen it", so
> the class is *may apply within granted autonomy*. The default *propose* is
> **ACCEPTED** (V4-HI-41, via B-ACCEPT). Operation-specific additions are
> pending OI-021. Host adoption is **not evidenced** (DEP-001).
> SWBPIPE (SQ-05, 2026-09-28): no class system and no grants; every change
> requires the person's Apply (hard-coded). The App's DERIVED class and
> default stand as App/shared meaning; the host's own autonomy is SWBPIPE
> owner decision OI-016.

The policy-class record is P-03 (§8.3). In the fixture, OP-C4, OP-C5 and
OP-C9 carry it (C-v0.4 §10.2; carried in C-v0.8).

- Acceptance granularity:
  - Row-by-row acceptance is one A5 per change item.
  - Multi-row or whole-batch acceptance is one A5 act listing several items.
  - Each item binds and lapses on its own.
- Batch acceptance is not A4 or A6 of any row. Acceptance is not application.
  On SWBPIPE the person's Apply is acceptance and application in one step,
  per batch, with no A10 record (SQ-01, SQ-09). The App keeps the distinction
  as meaning and records the missing counterparts (R8-5; §2.5).
- A5 and A10 on these proposals are reserved (P-01, P-01a).
- With no person setting, the grant state is **effective (policy default):
  propose** (R2-6).

**Fixture walk-through (C-v0.4 §10.3, carried in C-v0.8; invented material).**

| Step | Rev | What happens | Treatment, act or outcome |
|---|---|---|---|
| T3 | r12 | The agent reads OP-C1 and gets basis B1 | — |
| T5 | — | The agent drafts PR-1 relying on B1:<br>item 1 adds a guide support at 4.2 m on R-100 (OP-C4);<br>item 2 sets S-3 stiffness to 2.0e6 N/m (OP-C5 "Set support stiffness") | *propose*, effective (policy default) |
| T6 | r13 | Engineer A makes an intervening edit | — |
| T7 | r13 | PR-1 is submitted | Refused — stale (B1 relied, B2 current) |
| T9 | r13 | PR-2 is re-drafted, with lineage from PR-1 | A new proposal |
| T10 | r13 | PR-2 | Queued |
| T11 | r13 | Engineer A acts on the items: accepts item 1 (OP-C7) and rejects item 2 (OP-C8) | A5 on item 1; A10 on item 2 |
| T12 | r14 | The host applies item 1 | Receipt RC-1; the A5 on item 1 is not lapsed |

The run record shows:
- A1 by the agent;
- A5 and A10 by Engineer A, recorded by the host facility (direct capture), or
  faithfully by the agent citing the host's evidence;
- A2 through the host route, with RC-1 referenced.

It shows no A4, A6 or A7.

---

## 8. Policy representation (OUT-002)

### 8.1 Policy-class record — element meaning

| Element | Meaning |
|---|---|
| *policy revision identity* | Cited by consumers in their governing-policy element. This revision is DEL-04-01/ACT-POLICY-v0.8 plus its content identity; the method is unselected. ACT-POLICY-v0.9 changed no policy record, so the policy revision label stays v0.8 and the instance file is unchanged (node F-C). |
| *class identity* | A host-named operation class (V4-HI-30), or an act-defined class (P-02) |
| *covered operations* | Catalog operation identities and versions (DEL-03-01) |
| *consequence statement* | d3 dimensions (U-02) |
| *catalog human-act class* | none / may apply within granted autonomy / proposal only / reserved to the person (SETTLED V4-HI-02) / **no policy basis** + *reason* (INTEGRATION) |
| *default grant value* | For "may apply" classes; used by *effective (policy default)* |
| *widenable* | yes (bounded by §5.6) / no |
| *acceptance granularity* | Where proposals apply |
| *actors covered* | The person, the embedded agent, external agents (V4-HI-50) |
| ***decision basis*** | Identity, decision actor, recorder, date and custody of the fixing requirement or decision. For open values: the item, its owner and its point of need. |
| *decision standing* | settled-by-basis \| **adopted decision** \| DERIVED \| accepted default (host adoption unevidenced) \| INTEGRATION \| PROPOSED \| `UNRESOLVED{…}` |
| *host adoption* | Currently **unevidenced** for every record (DEP-001). SWBPIPE's answers (SQ-05, 2026-09-28: no class system, no grants, no named reserved list) are answers, not adoption (R8-7) |
| *consumers* | §10 |

Rules:
- No value is carried without a decision basis. Historical drafts, fixture
  expectations and pending recommendations are not bases.
- An open value names its item, owner and point of need.

**PROPOSED structure (ACT 7; R12-1, R12-2; U-12 stays open for placement).**
The adopted policy-class configuration (OUT-002) is one document per policy
revision: `ACT_POLICY_CLASS_RECORD.schema.json` beside this file (JSON
Schema 2020-12, `$id` `urn:chirality:app-v4:del-04-01:policy-class-record:0.1`).

| Part | Elements (Chirality's own names; no host field is selected) |
|---|---|
| Configuration | `format` "chirality.act.policy"; `formatVersion`; `policyRevision` {label "DEL-04-01/ACT-POLICY-vX.Y", content identity {method, value}}; `records`; `decisionRecords` (§8.2) |
| Record | `recordId` (P-nn[a]); `title`; `recordRole` — **catalog class** (requires a class identity, a human-act class and *widenable*), **treatment rule** (requires a treatment; carries no class value: P-05), or **tool-permission setting** (requires the setting's owner; never a class value: P-04); `classIdentity` {host-named operation class · act-defined class, name}; `coveredOperations` or `coveredActs`, with a coverage rule; `humanActClass` (the five values) and its no-policy-basis reason; `defaultGrantValue`; `widenable`; `acceptanceGranularity`; `actorsCovered`; `consequence` (§8.5; "not assigned" while U-02 is open, or "not applicable" for an act class); `decisionBasis` (identity with part and standing, or an open item with owner and point of need); `decisionStanding`; `openItems`; `hostAdoption` {unevidenced · evidenced, note}; `phase` {current phase, governance phase}; `undoRule`; `conditions` |
| Reference from a consumer | {policy revision label, record identity}, e.g. {"DEL-04-01/ACT-POLICY-v0.8", "P-03"}: DEL-03-01 element 8's policy record reference, RS §6.1's governing policy reference, AS settings-in's policy-class record reference. A consumer that cites a revision other than the one in force keeps its citation and shows the revision it cites; it is never silently re-pointed, and a value that differs between the two revisions is shown as from the cited one |

The instances are in `ACT_POLICY_CLASS_RECORD.valid.example.json` (P-01,
P-01a, P-02…P-06, and DECISION-1 as a decision record); three records that
must fail are in `ACT_POLICY_CLASS_RECORD.invalid.examples.json` (no
decision basis; a class value on the tool-permission setting; a consequence
value outside the vocabulary). `prototype/validate_policy.py` validates them
and also checks that record identities are unique and that every record
*reserved to the person* is not widenable. Run 2026-09-30 (Python 3.13.7):
all held (`WAVE_B/B4.md`).

### 8.2 Decision record — DECISION-1

| Element | Value |
|---|---|
| Identity | `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` |
| Decision actor | The owner (Ryan) |
| Recorder | HELP_HUMAN (Claude Code session). Faithful recording, actor ≠ recorder. |
| Date | 2026-09-28 |
| Custody | The owner's answers to a structured chat question, transcribed. Not a platform export; no platform timestamp. |
| Source | `OWNER_DECISIONS.md` (sha256 f3f8e5f3…81f2e); package `DECISIONS_PENDING.md` at `8d3c66542` |
| Scope | First increment, App/shared contracts |
| Not established | SWBPIPE adoption or enforcement (DEP-001). `Open_Issues.csv` keeps OI-001 and OI-002 OPEN, with a pointer to DECISION-1 D2/D3, by the owner's decision (F-8) |

### 8.3 Policy-class records

The records below are also written as data, in the PROPOSED structure of
§8.1 (`ACT_POLICY_CLASS_RECORD.valid.example.json`). Where the two differ,
this text governs and the example is repaired.

**P-01 — reserved acts (D2).**
- Values:
  - A4 mark checked;
  - A5 accept, where the autonomy requires a proposal;
  - A6 approve;
  - A7 rely;
  - A12 set grant;
  - A13 enabling external access.
- Catalog class: reserved to the person. Widenable: **no**, neither past these
  acts nor past a declared checkpoint. In the current phase the reserved-act
  clause binds; for a declared checkpoint the request clause and record
  clause of V4-HI-42 are in force and only the hold is phased (R9-2; §3).
- Standing: **adopted decision** (DECISION-1 D2(a)–(e)).
  - The host names and enforces its own list.
  - Additions: `UNRESOLVED{OI-021}`.
  - A13 *disabling*: INTEGRATION (R2-3), not D2.

**P-01a — A10 reject.**
- Reserved to the person wherever A5 is. Not widenable.
- Standing: **DERIVED** (decision pair; R-1).

**P-02 — operations that perform reserved acts.**
- Covers any catalog operation whose effect is to *perform*, through the
  capturing surface, A4, A5, A6, A7, A10, A12 or A13. This includes creating
  or changing the host's own act state. Fixture examples: OP-C6, OP-C7,
  OP-C8; DEL-05-02 K-4.
- Catalog class: reserved to the person. Not widenable.
- Standing: **DERIVED** from S3 and D2 (R2-2).
- No faithful record is made through such an operation. App-side A9 records
  are DEL-04-03 files. A host-offered faithful-record operation, if any
  exists, must meet all of these:
  - it does not change act state;
  - it cites capture evidence;
  - it carries mode *faithful recording*;
  - it never satisfies a checkpoint;
  - it takes ordinary policy (*no policy basis* until assigned).
- Whether any host offers one is a DEP-001 relay question.

**P-03 — SWB model changes** (fixture OP-C4, OP-C5, OP-C9).
- Class: host-named. Catalog class: may apply within granted autonomy.
- Default grant value: *propose*.
- Widenable: yes, by A12, bounded by §5.6.
- Standing:
  - class **DERIVED** from V4-HI-41;
  - default **accepted** (V4-HI-41; the owner's direction of 2026-09-17; B-ACCEPT);
  - A5/A10 reserved (P-01, P-01a);
  - additions: `UNRESOLVED{OI-021}`;
  - host adoption unevidenced.
- Undo: an undo of a receipt produced under P-03 is governed by P-03 and by
  the grant state in force for the reversed operation's class (R3-4,
  INTEGRATION; §5.3). The same rule applies to undoing an operation governed
  by any other record.

**P-04 — routine tool permission (A14).**
- App: the user's own Codex tool-permission and sandbox modes per project and
  turn, including classifier-based modes, carried unchanged. Hosts: no
  classifier permission mode.
- Catalog class: none — this is never a class value. It is not governed by
  the autonomy grant, which governs host operations only.
- Standing:
  - **Adopted decision**: DECISION-1 D3 covers the content above.
  - **INTEGRATION** (R-2): the App never answers A14 affirmatively by rule;
    a decline or error is allowed only under a named rule with truthful
    origin.
  - **INTEGRATION** (R2-8): recorded only in run record R13.

**P-05 — acceptance-checkpoint constraint.**
- Applies to an operation whose result a declared checkpoint requires A5 on.
  The class is unchanged; the treatment is per run.
- Treatment: *propose*. Not widenable.
- Standing: **DERIVED** from V4-HI-42 + D2b (R-5); constraint element per
  R2-12.
- Phase: plan guidance in Phase 1, where the host's own treatment of its
  operations decides what the host does. Where the active grant lets the
  host apply directly, no proposal is queued, so the A5 checkpoint (kind (c)
  *proposal queued*) is **not reached**: nothing is requested by reason of
  an arrival that did not occur, no A5 is forced, and none is recorded; the
  record shows the direct application under the person's grant (AP-8; R9-2
  as corrected by R10-1). A checkpoint the run does reach under such a grant
  has its act requested and stays *waiting* until the person performs it
  (§4.4). It binds for governed
  checkpoints in the governance phase, with R2-12 carriage assurance (§4.4).

**P-06 — no-policy-basis treatment.**
- Applies to classes with reason omitted, unassigned or pending OI-021.
- Catalog class: no policy basis. *propose* is available; direct is not
  permitted. Not widenable: an A12 is refused.
- Standing: **INTEGRATION** (R-3.5; R2-1, R2-9). The REQ-004 production hold
  stands, and fixtures report such cases as **held**.

Fixture-only class assignments are not policy records:
- OP-C10 Undo: governed by the policy record of the operation whose receipt
  it reverses (R3-4). In FX-39 this is the OP-C9 class, P-03, under the T15
  grant.
- OP-C11: *no policy basis*, reason pending OI-021 (R2-21).
- Reads: *none* (C §3.1 rule 6).

### 8.4 Values still open

| Value | Open item | Owner | Point of need |
|---|---|---|---|
| Operation-specific reserved additions; class of the first connected operation | `UNRESOLVED{OI-021}` | Owner via the outside SWB session and App/shared owner | Before the connected-activity SoW |
| Consequence vocabulary (PROPOSED draft for review: §8.5) | U-02 | DEL-04-01 with the host policy owner | Before class assignment in DEL-03-01 |
| Defaults for other consequential classes | U-06 | SWBPIPE owner decision OI-016 (ANS §2); host policy owner generally (DEP-001) | Before those classes are cataloged |
| Host capture requirements and capture-evidence reference; host faithful-record operation; checkpoint-constraint reception; host adoption of P-01…P-06; A13 enablement facility | U-04 (relay questions; answered 2026-09-28: none offered) | SWBPIPE owner decisions (ANS §2) | When the owner resumes UI-SUCCESSOR (DECISION-3); before host act-recording integration or any enforcement claim |

### 8.5 Consequence vocabulary — PROPOSED for the owner's phase review (ACT 8; U-02)

**Standing.** A PROPOSED draft, not a decision. d3 names the four things
whose change reopens an autonomy treatment ("Reconsider when: consequences,
reversibility, available examination or the human's intended delegation
change"). This drafts one value set per dimension so that the owner has
something concrete to review at the phase review. It assigns no value to any
record (every §8.3 record says "not assigned" or "not applicable"), sets no
default and opens no direct branch. The grant scope's consequence dimension
(§5.4) stays a slot, and OP-C5 on S-4 under ⟨set-2⟩ stays held (C T15).
The values are also the PROPOSED enumerations of the schema's consequence
statement (§8.1).

| Dimension (d3) | Code | Value | Meaning | Fixture illustration (invented) |
|---|---|---|---|---|
| **Effect** | CQ-E0 | no domain change | Reads and examinations | OP-C1, OP-C3 |
| | CQ-E1 | App-side only | App files or App outputs only | an edit of AF-1 |
| | CQ-E2 | queued proposal only | Nothing changes until the person accepts and the host applies | OP-C4 under *propose* |
| | CQ-E3 | domain change, bounded objects | Changes named objects | OP-C9 on S-4 |
| | CQ-E4 | domain change, model-wide | Changes structure or the whole model | none in the fixture |
| | CQ-E5 | effect outside the host | Sends data or starts a process beyond the host | a network destination (governed separately by §2.7) |
| **Reversibility** | CQ-R1 | host undo with receipt | The host's undo route writes a receipt that reverses the change | OP-C10, RC-3 reverses RC-2 |
| | CQ-R2 | host undo without receipt | Reversible, but no receipt names the reversal | SWBPIPE's session undo (SQ-10) |
| | CQ-R3 | reversed only by a further change | No undo route; another change can restore | — |
| | CQ-R4 | not reversible | — | — |
| | CQ-R0 | not stated | The host states nothing | — |
| **Available examination** | CQ-X1 | host checks available on the result | The host can check the result (host checks, named) | OP-C12 |
| | CQ-X2 | agent examination only | Only an agent's findings (A3) | OP-C3 |
| | CQ-X3 | the person's examination only | Only the person can examine it | — |
| | CQ-X4 | none before reliance | No examination is available before the result is relied on | — |
| | CQ-X0 | not stated | — | — |
| **Intended delegation** | CQ-D1 | the person decides each item | Row-by-row A5 | T11 |
| | CQ-D2 | the person decides the batch | Multi-row or whole-batch A5 | SWBPIPE's Apply (per batch) |
| | CQ-D3 | agent applies within scope; the person checks later | Direct application with a later A4 on the result (S1's "later checking") | T16, T16a |
| | CQ-D4 | agent applies within scope; no follow-up act expected | Direct application alone | — |

**If adopted,** a policy-class record's consequence statement would carry one
value per dimension; a grant's scope could name a set of values (for example
"CQ-E3 with CQ-R1"); and the conservative default *propose* would stand
whatever the values (V4-HI-41). Nothing here makes an operation reserved or
unreserved: that stays D2's and OI-021's.

**Questions for the owner's phase review:** (1) the four dimensions as
named; (2) each value set; (3) whether intended delegation belongs in the
operation's record or only in the person's grant; (4) whether CQ-E5 belongs
here or stays with §2.7 alone. Owner: DEL-04-01 with the host policy owner
(U-02). Point of need: before class assignment in DEL-03-01.

---

## 9. Label rules (R-4; S7; S4)

| Word | Allowed use | Not allowed |
|---|---|---|
| **accept / reject / withdraw** | Proposal decisions (A5, A10, A11) | For A7 (use *rely*). For A10, write "rejected the item", not "declined the item". |
| **decide** | A16 only: the person's choice of one alternative of a decision package (R23-8) | For an act the package names that has its own word (accept, mark checked, approve, rely, register); for an agent's recommendation |
| **approve / approval** | A6 only | On proposals. For harness tool-use prompts (these are **tool permission**, A14). For design-candidate approval. |
| **checked / Checked** (unqualified) | A4 only | For host checks (write "host checks passed: ‹named checks›", each with its evaluated basis). For agent work (write "examination" / "findings"; "agent-examined (non-mutating)"). |
| **declined** | An A14 settlement (HOSTING §6); the **act-declined event** (§2.3), by its full name | As a name for A10 |
| **later-check route** | Access for later examination or checking | Any implication that an act occurred |
| **certified, sealed, approved, code-compliant** | The accountable professional's own statement | Agent output standing |

---

## 10. Value → decision → consumer map

### 10.1 Values carried

| # | Value | Basis (standing) | Consumers |
|---|---|---|---|
| V-01 | Canonical names A1–A16; the human-act record kinds; act-declined and run-ended events (§2); the act-record lifecycle (§2.8) | S3, S5, S7, S11; R-1; R2-5; A15: V4-WF-02 and R12-5 (INTEGRATION); A16: V4-PM-04 and R23-8 (INTEGRATION) | DEL-04-03, DEL-02-01, DEL-04-02, DEL-05-01, DEL-05-02, DEL-01-04 (AAC-v0.2, NIR-v0.2); A15 also DEL-02-02 (WR-v0.2); A16 also DEL-01-04 (AAC-v0.3), DEL-02-03 (CE-4 schema 0.7) and DEL-06-02 (DV-v0.1) |
| V-02 | Class vocabulary: four SETTLED values plus *no policy basis* with reason (INTEGRATION) | V4-HI-02; R2-1 | DEL-03-01 element 8; DEL-03-02; DEL-05-01 (five values); DEL-03-03 |
| V-03 | Resolution order §5.3, resolution point, widening bounds §5.6 | S1, S8–S10, S12; D2; R-3; R2-6, R2-9 | DEL-03-02, DEL-05-01 (relay only), DEL-02-03, DEL-04-02, DEL-03-03 |
| V-04 | Grant by A12, with scope, the seven states including *effective (policy default)*, and two settings references | V4-AUT-01; V4-HI-40; D2e; R-8; R2-6 | DEL-04-02, DEL-04-03, DEL-05-01, DEL-03-02 (standing at drafting) |
| V-05 | Outcome map §6, including offered reserved entries, host-reported *not exposed* and loop *not offered* | V4-HI-23, -25; R-3; R-7; R2-4 | DEL-03-01 §4.1; DEL-03-02 P §9; DEL-05-01; DEL-05-02; DEL-04-03; DEL-01-04 |
| V-06 | Content binding, lapse, supersession and undo (§2.5) | V4-HI-32; V4-REC-05; R-6; R2-7; R2-15 | DEL-04-03, DEL-03-01, DEL-03-02, DEL-04-02, DEL-05-02, DEL-02-01 (SB-4/U-27) |
| V-07 | Label rules §9 | V4-HI-33; R-4 | DEL-05-02, DEL-01-04, DEL-04-02, DEL-02-01, DEL-03-02, DEL-04-03 |
| V-08 | No professional standing from agent output | V4-AUT-05 | DEL-04-02, DEL-05-02, DEL-01-04, DEL-09-09 |
| V-09 | Checkpoint rules §4: in Phase 1, plan guidance with the act requested by the agent (AP-12), acts recorded only when performed, reserved acts standing and lapse recorded (§4.0); the resume point, earlier acts counted on current content (§4.5; capture after arrival kept as a governance-phase option), the joint answer (§4.3) and no resumption in both phases; re-hold, hold support and carriage assurance as the governance-phase definition (retained) | V4-HI-42 and V4-WF-05 as amended by SCA-V4-001 (the hold phased to the governance layer); D2; R-5; R2-10, R2-12, R2-17…R2-20; R4-2…R4-6, R4-9, R4-14; R8-1, R8-2, R8-11; R9-1, R9-2; DECISION-K1 K1-1…K1-3 | DEL-02-01, DEL-02-03, DEL-05-01, DEL-05-02, DEL-03-02, DEL-03-03 |
| V-10 | External access: same settings and reserved acts; A13 reserved and captured by the host's enablement facility; App-side configuration never A13 evidence; *channel not enabled*. The model destination is a record and status element, not a policy value. Host content may flow to the selected model with no gating: SETTLED (DECISION-2). Recording and showing the destination per turn: SETTLED. The owner confirmed the reading (OWNER_ITEMS O-10, accepted at DECISION-7 of `APP-V4-BASIS-ALIGN-20260928`), and DEL-04-03 ScopeOfWork REQ-002 requires "model used with its observed destination per turn" (R5-4; R9-4). SWBPIPE: no A13 facility (SQ-28); `controller_unavailable` → *endpoint unavailable*, channel *disabled* (R8-6; §2.6). | V4-HI-50…52; D2e; R2-3; R4-13; R8-6 | DEL-03-03, DEL-09-09, DEL-04-03 |
| V-11 | SWB record P-03 | V4-HI-41 | DEL-03-01, DEL-03-02, DEL-04-02, DEL-04-03, DEL-05-01, DEL-05-02, DEL-09-09 |
| V-12 | A3 ≠ A4 | d3; V4-EXM-21 | DEL-05-02, DEL-04-02, DEL-04-03 |
| V-13 | A9 record shape, the capture-evidence rule, and the capturing surfaces and never-evidence list (§2.6) | S3; R-5; R2-20; R4-12, R4-13 | DEL-04-03, DEL-05-01, DEL-05-02, DEL-02-01, DEL-09-09 |
| V-14 | P-01, P-01a, P-02 | D2; DERIVED; R2-2 | DEL-03-01 (OP-C6/C7/C8), DEL-05-02 K-4, DEL-03-02, DEL-03-03, DEL-04-02, DEL-02-01, DEL-09-09 |
| V-21 | P-04 routine tool permission | D3 plus INTEGRATION | DEL-01-01, DEL-01-04, DEL-01-02, DEL-05-01 (no permission layer in hosts), DEL-05-02, DEL-04-02, DEL-04-03 |
| V-25 | A14 recorded only in R13 (not applicable in host-loop runs) | R2-8 | DEL-04-03, DEL-01-01 |
| V-29 | PROPOSED structure of the policy-class record and the consumer reference {policy revision label, record identity} (§8.1; `ACT_POLICY_CLASS_RECORD.schema.json`) | PROPOSED (R12-1, R12-2); placement U-12 open | DEL-03-01 (element 8), DEL-04-03 (§6.1 governing policy reference), DEL-04-02 (settings-in), DEL-03-02, DEL-05-01 |
| V-30 | The request → capture → record sequence (§4.7) | PROPOSED order over SETTLED rules (DECISION-K1 K1-1, K1-2, K1-4) | DEL-02-03, DEL-04-03, DEL-05-01, DEL-05-02 |
| V-28 | Network-destination grant: a person-only A12, subclass network-destination grant, with its forms, scopes, decline wording, never-evidence list and stateless-MCP rule (§2.7) | The person-only grant: SETTLED (DECISION-5; PRD V4-HOST-02 and the ARCHITECTURE §4 host-agent properties, as amended by SCA-V4-001). The A12 mapping: INTEGRATION (R8-13; F-22) | DEL-05-01 (LOOP §5.1.1), DEL-05-02 (PANEL §3.8), DEL-04-02 (AS §3), DEL-04-03 (RS R15, R9), DEL-03-04 |

DEL-03-04 (the guide) integrates this contract by section, and DEL-09-06
consumes V-03, V-05 and V-10. Both are mapped in §10.3 and are not repeated in
every row above.

### 10.2 Values held

| # | Value | Standing | Consumers that must hold |
|---|---|---|---|
| V-20 / V-22 | Operation-specific reserved additions; first connected operation, its autonomy and environment | `UNRESOLVED{OI-021}` | DEL-03-01, DEL-05-01, DEL-05-02, DEL-09-09 |
| V-23 | Consequence vocabulary (a PROPOSED draft for the owner's phase review, §8.5; not assigned); other host defaults | U-02, U-06 | DEL-03-01, DEL-04-02 |
| V-24 | Multi-row A4 purpose after partial lapse — *no longer held:* settled by DECISION-K1 K1-3 and carried in §4.3 (joint answer) | U-03 (closed) | DEL-04-03, DEL-04-02 |
| V-26 | App-side run holds (governance phase) | `UNRESOLVED{D6}` (U-D6): closed for Phase 1 by DECISION-4; re-opens with the governance phase (R8-2) | DEL-02-03, DEL-02-01, DEL-03-03, DEL-05-02 |
| V-27 | Counting a prior act captured before arrival — *no longer held:* settled for the current phase by DECISION-K1 K1-2 and carried in §4.5; capture after arrival is the governance-phase option | U-14 (closed) | DEL-02-03, DEL-02-01, DEL-04-03 |

### 10.3 Receivers by register row (R9-6)

Rebuilt at v0.7 from the ACTIVE rows of this deliverable's `Dependencies.csv`
and of each consumer's own register. Every arc below is admitted by DAG-003.
Every row states RequiredMaturity INITIALIZED, except DEP-03-03-008 (TBD);
no row records satisfaction. This table defines no contribution; it names
where the values of §10.1 and §10.2 go.

| Consumer | Consumer's own row | Local mirror row | Mapped here |
|---|---|---|---|
| DEL-02-01 | DEP-02-01-018 | DEP-04-01-012 | §10.1, §10.2 |
| DEL-02-03 | DEP-02-03-012 | DEP-04-01-013 | §10.1, §10.2 |
| DEL-03-01 | DEP-03-01-024 | DEP-04-01-014 | §10.1, §10.2 |
| DEL-04-02 | DEP-04-02-007 | DEP-04-01-015 | §10.1, §10.2 |
| DEL-04-03 | DEP-04-03-021 | DEP-04-01-016 | §10.1, §10.2 |
| DEL-03-02 | DEP-03-02-017 | DEP-04-01-022 | §10.1 |
| DEL-03-03 | DEP-03-03-008 | DEP-04-01-023 | §10.1, §10.2 |
| DEL-03-04 | DEP-03-04-011 | DEP-04-01-024 | The guide integrates and checks this contract by section (GUIDE cites §2–§9): V-01…V-14, V-21 and V-28 |
| DEL-05-01 | DEP-05-01-018 | DEP-04-01-025 | §10.1, §10.2 |
| DEL-05-02 | DEP-05-02-008 | DEP-04-01-026 | §10.1, §10.2 |
| DEL-09-09 | DEP-09-09-010 | DEP-04-01-027 | §10.1, §10.2 |
| DEL-09-06 | DEP-09-06-030 | none | V-03, V-05 and V-10, and V-24 (settled by DECISION-K1 K1-3; CA cites §5.3, §6, §2.6 and U-03) |
| DEL-01-02 | DEP-01-02-021 | none | §10.1 (V-21) |
| DEL-01-04 | DEP-01-04-011 | none | §10.1 (V-01, V-05, V-07, V-08, V-21). Receiving side: NIR-v0.2 §8 act presentation (V-01, V-07, V-08), §4 request cards (V-21), §9 with AS's standing facets (V-05); AAC-v0.2 §1.2 act kinds and wording (V-01) |
| DEL-02-02 | DEP-02-02-016 | none | §2.1 A15, §2.5, §2.6, §4.7, FX-56, FX-58 (WR-v0.2 §4.3, §9) |
| DEL-06-02 | DEP-06-02-009 | none | Not mapped in detail |
| DEL-09-02 | DEP-09-02-018 | none | Not mapped in detail |
| DEL-09-05 | DEP-09-05-009 | none | Not mapped in detail |
| DEL-09-12 | DEP-09-12-011 | none | Not mapped in detail |
| DEL-10-03 | DEP-10-03-013 | none | RA-v0.1 (run `APP-V4-DESIGN-PASS-4-20261003`, committed at `caed56b8ea`; entry S-6) reads, by section: §2.1, the acts with their decision actor, subject and supporting evidence; §3, the settled distinctions S1–S12; §8, the policy representation, namely DECISION-1's reserved acts (§8.2) and the values still open (§8.4). This contract shapes nothing for it and takes nothing from it (R23-31.10). ACT's ScopeOfWork names no DEL-10-03 receiver and this register holds no mirror row; that is RA F-RA1, for the next amendment |

- The last eight consumers are not among the fourteen first-increment
  deliverables. Of them, DEL-01-02, DEL-01-04 and DEL-02-02 have Design files
  from run `APP-V4-DESIGN-PASS-3-20261001` (RECOVERY-v0.2, AAC-v0.2,
  NIR-v0.2, WR-v0.2; PROPOSED, not built); DEL-09-02 is outside this
  undertaking (D1).
- DEL-01-01 uses V-21 and V-25 (§10.1). No row in either register carries
  that use.
- Whether this register should mirror the nine consumers without a local
  row is a register matter (F-1). It is returned by Wave A, not decided here.

---

## 11. Boundary accounting (REQ-007, VER-008)

| Act or production | Owner | This contract's part |
|---|---|---|
| OI-001 and OI-002 rulings | The owner (DECISION-1) | Carry them as P-01 and P-04 |
| OI-021 and operation-specific additions | Owner via the outside SWB session and App/shared owner | Hold (U-01) |
| Performing A4–A7, A10, A12, A13; answering A14 | The person, the accountable professional (A7), or the user's Codex mode (A14) | Meanings and fixtures only |
| Capture as the capturing surface; host act facilities, route, receipts, origin and undo, catalog; enforcement of the D2 list | External SWBPIPE owner (CLM-003; DEP-001) | Requirements and relay questions; no host evidence claimed |
| Checkpoint declaration; hold machine | DEL-02-01; DEL-02-03 | Supply §4 |
| Catalog schema, subject content identity, §4.1 outcomes, exposure, shared fixture | DEL-03-01 | Supply V-02, V-05, V-11, V-14 |
| Proposal lifecycle, change-item content identity, checkpoint constraint, P §9 | DEL-03-02 | Supply V-03, V-05, V-06, V-09 |
| External receiving adapter | DEL-03-03 | Supply V-10; relay-only rule |
| Autonomy and standing UI, grant states | DEL-04-02 | Supply V-04, V-08 |
| Record format, lapse comparison, R13 | DEL-04-03 | Supply V-01, V-06, V-13, V-25 |
| Loop and panel receiving | DEL-05-01, DEL-05-02 | Supply V-03, V-05, V-07, V-09 |
| Hosting boundary and tool-permission answers | DEL-01-01 | Supply V-21, V-25 |
| Certification, sealing, professional approval, code compliance | Accountable professional (CLM-005) | Prohibit inference |
| Placement of the policy representation | App/shared owners (OI-013, OI-014) | Representation-neutral |

This contract's existence claims none of the following:
- host implementation;
- adoption;
- enforcement;
- external evidence;
- performance of any person's act.

---

## 12. Remaining owner, design and relay questions

1. **OI-021** (owner via the outside SWB session). What is the first concrete
   operation? Which operation-specific reserved additions and which autonomy
   apply to it?
2. **Multi-row A4 after partial lapse** (DEL-04-01 with the owner, U-03). Does
   the act's purpose survive for the other rows? **Decided** by DECISION-K1
   K1-3 (2026-09-30): yes; a new act on the changed rows alone answers the
   checkpoint together with the earlier act (§4.3).
3. **Consequence vocabulary** (DEL-04-01 with the host policy owner, U-02).
   A PROPOSED draft with four questions for the owner's phase review is in
   §8.5.
4. **Relay questions to the SWBPIPE owner** (DEP-001, U-04):
   - (a) The capture requirement per reserved act, and the capture-evidence
     reference (R2-20).
   - (b) Whether any host operation stores an agent's faithful record, and if
     so, that it meets the P-02 conditions (R2-2).
   - (c) Whether the host route receives the governing checkpoint constraint
     or evaluates its own copy of the declaration (R2-12).
   - (d) Adoption and enforcement of P-01…P-06, and the settings reference in
     force at application.
   - (e) Whether the host has an enablement facility that captures A13 with a
     capture-evidence reference (§2.6; R4-13).
   - (f) SQ-02: whether the host receives the checkpoint constraint and can
     hold a run itself. The D6 ruling depends on this answer.

   **Answered by SWBPIPE on 2026-09-28** (relayed; answers about its current
   state, not commitments; host joins deferred, DECISION-3):
   - (a) SQ-01: no capture-evidence reference; the Apply receipt names no
     person or time and is session-only. Storage and actor identity are
     SWBPIPE owner decisions (PB-TBD-002; DEL-16-03).
   - (b) SQ-21: no faithful-record operation.
   - (c), (f) SQ-02: route (iv), none planned; no host-held route and no
     host loop (SQ-20). Planning one is a SWBPIPE owner decision.
   - (d) SQ-05: no class system, no grants, no named reserved list, no
     settings reference; every change waits for Apply. Autonomy is SWBPIPE
     owner decision OI-016.
   - (e) SQ-28: no enablement facility, none planned (§2.6).
5. **App-side run holds** (`UNRESOLVED{D6}`; U-D6): **closed for Phase 1**
   by DECISION-4, and re-opened when the governance phase is taken up (R8-2).
   Separately, whether prior acts captured before arrival should count was
   decided by DECISION-K1 K1-2: in the current phase they count on current
   content (§4.5; U-14 and EXEC U-E4 closed).
6. **Workflow registration** as a canonical act (DEL-04-01 with DEL-02-02,
   U-08). **Decided** by R12-5: A15 register workflow revision (§2.1), not
   checkpoint-requirable in this increment; captured by DEL-01-04's App act
   control and registered by DEL-02-02 (K-8; AAC-v0.2, WR-v0.2).
7. **Launch environment variable as A13 evidence** (owner; deferred, R8-6,
   U-16): whether a launch environment variable the person sets counts as
   A13 evidence. Revisit when UI-SUCCESSOR resumes.

---

## 13. Fixture catalogue (OUT-003) — designed, not run

**Sources.** Subjects come from **C-v0.4 §10**, carried in C-v0.8 §10 (R2-21; R4-18; R5-9; R8-12 item 7):

- **Model:** FX-PIPE-01, run 12, R-100, supports S-1…S-4 and S-5 (created at T12), Engineer A.
- **Fixture assumptions:** FXA-1…FXA-5, renamed from FA-n; the alias is kept by C (R5-9; V3-A m-3). FXA-1 exposes every entry on all three surfaces. FXA-5 states that ⟨rev-3⟩ (WD-EX E1) declares `CP-accept` (A5) and `CP-check` (A4 on objects changed by `CP-accept` items' applied outcomes).
- **App-side subjects:** LIB-A1, LIB-A2, AF-1.
- **Entries:** OP-C1…C12.
- **Timeline:** T1–T17, including T4a and T16a.
- **Proposals, receipts and settings:** PR-1/PR-2, RC-1…RC-3, ⟨set-1⟩/⟨set-2⟩.
- **Variants:** V-S1, V-CP1, V-NP1, V-R1, V-X1, V-OU1 and V-ED1, plus **V-GR1** (R5-7; present in C-v0.5 §10.4 with GR-P/GR-R/GR-S, and carried in C-v0.8). V-GR1 is a run of WD-EX E1d in which `CP-grant` arrives at r15, T15's A12 is captured *after* the arrival, and the held OP-C9 call is then dispatched unchanged as T16.

**Local additions, named per R2-21 (V3-A m-13).** Retired labels are not reused (V3-A MAJOR-4):
- L-ACT-1 and L-ACT-3 were retired in v0.4;
- the v0.4 local checkpoint CP-3 is replaced by C's V-GR1 (R5-7).

| Label | What it is | Why it is local |
|---|---|---|
| **L-ACT-2** | A batch A5 over PR-2 items 1 and 2 | C's T11 uses a separate A5 and A10 |
| **L-ACT-4** checkpoint `CP-L4` | Requires A4. Reached-when kind (c): on the observed outcome of OP-C9 at T16. Subject class *objects changed by the named outcome*, which binds S-4. Held actions: the run's further host operations until the A4 (HS-3, R6-1). | C's `CP-check` (FXA-5) binds objects changed by `CP-accept` items. The T16 direct OP-C9 outcome is not a `CP-accept` item, so a checkpoint on a direct-branch outcome must be local. |
| **L-ACT-5** checkpoint `CP-L5` | Requires A4. Reached-when kind (b): on production of the T3 OP-C1 output. Subject class *objects a named output concerns*, which binds S-1…S-4 as read at r12 (R3-1). | For the earlier-act case (R4-5; DECISION-K1 K1-2). C schedules no checkpoint at T3. |
| **L-ACT-6** FX-Professional-P | An invented accountable professional | C names only Engineer A. A7 needs a professional. |
| **L-ACT-7** | A variant of `CP-grant` (V-GR1) whose reached-when kind (a) names a **harness capability** instead of OP-C9, in an App run | For hold support "not enforceable" (R4-21). C has no harness-capability entry. |
| **L-ACT-8** destinations A-1 and M-2 (R8-13) | A-1: an API destination in the category "other APIs". M-2: a configured MCP server that does not follow the stateless MCP revision 2026-07-28 | C's fixture has no network subjects (LOOP §5.2 uses local labels too) |
| **L-ACT-9** workflow revisions rev-4, rev-5 and draft d-12 of `supports-adjust` (R12-5); library entries `row-review` and `span-check` registered in place (v0.9; L-4) | Invented revision, draft and entry identities for A15 | C's fixture has no workflow registration |

Rules for reading the table:

- Expected results are contract expectations. They establish no act.
- Host-dependent results need DEP-001 evidence.
- **Phase (R8-1).** Checkpoint cases are read in Phase 1 (§4.0): dispositions
  are record labels, nothing is held, and no hold-support value is assigned.
  Where a case states a hold, a re-hold, *action during hold* or a
  hold-support value, that part is the **governance-phase value**, reading
  the checkpoint as if declared governed (no fixture declares the flag; R8-11
  item 5). App-side hold enforcement is governance phase; D6 is closed for
  Phase 1 (§4.6).
- Order checks follow C's order (R4-5; R5-7):
  - in V-GR1, `CP-grant` arrives at r15, before T15;
  - on the main timeline, run 12 (⟨rev-3⟩) declares no `CP-grant`;
  - `CP-L4` arrives at T16, before T16a.

| ID | Group | Case | Expected result | VER |
|---|---|---|---|---|
| FX-01 | Fabrication | At T10 the agent records A5 on PR-2 item 1 by Engineer A, without capture evidence. | Non-conformant (fabricated attribution). | VER-002, -004 |
| FX-02 | Fabrication | The T4 OP-C3 findings are recorded as A4 by Engineer A. | Non-conformant. A3 stays A3. | VER-002 |
| FX-03 | Fabrication | The agent writes A6 "approved", or A7, for its own output. | Non-conformant (S3, S4, P-01). | VER-002, -003 |
| FX-04 | Success-only | At T10 the UI shows "accepted" for PR-2. | Non-conformant. It must show "queued". | VER-002 |
| FX-05 | Success-only | RC-1 (T12) is presented as acceptance, checking or approval. | Non-conformant. RC-1 supports A2 only. | VER-002, -003 |
| FX-06 | Stale after acceptance (C V-S1) | T11 A5 on item 1; S-2 is edited before T12; application is refused as stale. | The A5 is kept and not lapsed. Display: "accepted by Engineer A — not applied: refused — stale (relied B2, current ⟨B-r14′⟩)" (R2-16). | VER-002 |
| FX-07 | Independent act | T2: A4 on S-2, captured by the host facility; no proposal involved. | Conformant. The absence of A5 does not invalidate it. | VER-002 |
| FX-08 | Independent act | T11 A5 on item 1; after T12, a second person performs A4 on **S-5** (created at T12). | Both acts are kept, each with its own actor. | VER-002 |
| FX-09 | Faithful recording | The agent records the T11 acts: actor Engineer A, recorder agent, mode faithful recording, citing the host capture evidence. | Conformant record shape. The capture requirement is the host's (DEP-001). A candidate-bound pass needs actual evidence (DEP-04-01-021). | VER-002 |
| FX-10 | Faithful recording | As FX-09, but the actor is the agent, or there is no evidence reference. | Non-conformant. | VER-002 |
| FX-11 | Labels | Controls read "Accept", "Accept selected items", "Accept all" and "Reject". | Conformant. | VER-005 |
| FX-12 | Labels | A proposal control or status reads "Approve" or "Approved", or an A10 is shown as "declined". | Non-conformant. | VER-005 |
| FX-13 | Labels | A separately evidenced A6 is labeled "approve"; A7 is labeled "rely". | Conformant. | VER-005 |
| FX-14 | Standing | An agent result is displayed "code-compliant" or "certified". | Non-conformant. | VER-003 |
| FX-15 | Standing | A7 by FX-Professional-P on OP-C2 results at r14 (C **§10.7**). | Conformant. Not inferred from A2–A6. | VER-003 |
| FX-16 | No policy basis (C V-NP1) | OP-C11: (a) Engineer A performs an A12 granting *direct*; (b) the agent requests direct; (c) the agent proposes. | (a) **refused (reason: no policy basis)**. (b) *not permitted*. (c) Queued, with no permission conferred. All are reported **held (pending OI-021)**. | VER-004, -007, -009 |
| FX-17 | No policy basis | An entry omits the class element. | Class *no policy basis*, reason *omitted*; otherwise as FX-16; **held**. | VER-004, -007 |
| FX-18 | Classifier | (a) Host: a classifier mode auto-permits OP-C4. (b) App: the user's Codex mode auto-permits a tool call. | (a) Non-conformant (D3). (b) Conformant as A14, recorded in R13 only. | VER-004 |
| FX-19 | Default | T5/T10 under ⟨set-1⟩ (FXA-4). | Grant state **effective (policy default): propose** (P-03). Item, multi-row and batch acceptance are offered. Host conformance needs DEP-001. | VER-006 |
| FX-20 | Widened (C T15, R4-18) | T15: Engineer A performs A12 → ⟨set-2⟩: P-03, *direct*, scope {FX-W1; {S-4}}. The control confirms. T16: the agent applies OP-C9 on S-4. | *effective (person-set)* → apply directly. RC-2 carries origin, basis, undo route and later-check route; both settings references are recorded. OP-C4 on R-100 is outside scope → a direct request is *not permitted*. OP-C5 on S-4: no expectation (held on U-02, as in C T15). | VER-001, -006 |
| FX-21 | Checkpoint | CP-L4 arrives at T16. T16a: Engineer A's A4 on ⟨S-4@r16⟩, captured after arrival. | *waiting*, then *performed*, then a run-resumed event (record labels in Phase 1). Before T16a the agent may only request (A8); it can never perform the A4 (AP-4). Phase 1: nothing is held, and a run action before T16a may carry "continued past CP-L4 before A4". | VER-001, -006 |
| FX-22 | Reserved operation (C V-R1) | At T3 the agent calls OP-C6 on S-1, under any grant. | *not permitted*. An A8 is **offered** and recorded only if issued. No attribution to the person. | VER-004, -006 |
| FX-23 | Grant change | The agent requests widening, then attempts to set it. | The request shows as *requested by agent (A8)*. The set attempt is *not permitted* (P-01). | VER-001, -004 |
| FX-24 | External | External access is off (no A13 in the host facility). | *channel not enabled*, not *unavailable*. The reporter is the App (App configuration off) or the host (host channel off) (R4-16). (SWBPIPE has no such code: its `controller_unavailable` is *endpoint unavailable*, and the channel shows *disabled*; R8-6.) | VER-004 |
| FX-25 | External | A13 is performed in the host facility. The external agent **drives T9–T10 and observes T11–T12** (R4-17). | Same lifecycle and settings as the embedded agent. A5/A10 are attributed to Engineer A. | VER-004 |
| FX-26 | Examination | T4 OP-C3. | Findings by reference. No A4 and no "host check". | VER-002 |
| FX-27 | Lapse | T2's A4 on S-2 at r12; T6 edits S-3 (control); T14 edits S-2 at r15. | Not lapsed at r13/r14. At T14 an **act-lapsed event** is recorded, and the act shows lapsed with its r12 identity. | VER-002 |
| FX-28 | Boundary | The contract asserts host enforcement without DEP-001. | Non-conformant. | VER-008 |
| FX-29 | Acceptance checkpoint (C V-CP1) | CP-accept (FXA-5) on OP-C4 results, with the V-CP1 direct grant. The agent requests OP-C4 directly. | *Governance phase:* *not permitted*, naming the constraint {run 12, CP-accept, A5, OP-C4}. Never converted. **AWAITING INPUT** (host receipt of the constraint; SQ-02) — SQ-02 answered 2026-09-28: route (iv), no receipt and no host copy (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3). *Phase 1:* the agent, following the declaration as guidance, proposes OP-C4 and adds no field the host lacks; if a direct request is made, the host's own treatment decides and the outcome is recorded as observed (AP-8; R8-10). | VER-001, -006 |
| FX-30 | Negative A5 | CP-accept over PR-2 (arrival at T10, *queued*). T11: A5 on item 1, A10 on item 2. | *resolved negatively* with a *partial* annotation (WD §4.3.7; confirmed by DEL-02-03, R4-7). Item 1's A5 proceeds. Never "all accepted". | VER-002 |
| FX-31 | Act-declined | CP-L4: Engineer A declines to mark S-4 checked. | **Act-declined event** with capture evidence; *resolved negatively*; the on-negative path governs; no A4. | VER-002 |
| FX-32 | L-ACT-2 | A batch A5 over PR-2 items 1 and 2; item 1 is applied (RC-1). | One A5 act lists both items, each bound to its own change-item content identity. Item 1's A5 is not lapsed by RC-1. | VER-002, -006 |
| FX-33 | A14 origin | An App rule answers a tool permission affirmatively; separately, a named-rule decline. | The affirmative answer is non-conformant. The named decline with truthful origin is conformant and recorded in R13. | VER-004 |
| FX-34 | "checked" label | The T1 host result is labeled "Checked"; the T4 findings are labeled "agent-checked"; T4a is shown. | The first two are non-conformant: they must read "host checks passed: equilibrium, unit consistency" and "agent-examined (non-mutating)". T4a must read "host check failed: support spacing". | VER-005 |
| FX-35 | Offering reserved (C V-R1, V-X1) | (a) As V-R1. (b) A variant reports OP-C6 as *not exposed* or *unavailable* for a class reason. (c) V-X1: OP-C9, not exposed on X. | (a) *not permitted*, with an A8 offered and not auto-recorded. (b) Non-conformant. (c) The host reports *not exposed on this surface* (exposure, not class), and the adapter relays it. | VER-004 |
| FX-36 | Checkpoint evidence | The agent writes an A4 record for CP-L4 without citing host capture evidence. | Not a satisfaction: the A4 is not recorded as performed (AP-3). Governance phase: the run does not resume. | VER-002, -004 |
| FX-37 | Narrowing | PR-2 is queued (T10). After T15, a direct OP-C9 request on S-4 is in validation. Engineer A narrows ⟨set-2⟩ to *propose* (an A12 that is established). | PR-2 is unaffected. The OP-C9 request is re-resolved at application → *not permitted*, never converted. | VER-001, -006 |
| FX-38 | Widening | PR-2 is queued. Engineer A widens P-03 to *direct* (T15). | PR-2 stays a proposal. | VER-006 |
| FX-39 | Undo (C T16a/T17) | CP-L4 is performed by T16a's A4 on S-4, and the run resumes. At T17, OP-C10 RC-3 reverses RC-2 and S-4 changes. | *Both phases:* an act-lapsed event is recorded. Nothing is undone. The act record is not erased. A5/A10 on a reversed item would stay bound. T17 is Engineer A's own operation and never carries a hold or continued-past annotation. *Phase 1:* nothing re-holds; the agent re-requests the A4 as its plan requires (AP-7). *Governance phase:* CP-L4 is **re-held**: "waiting — re-held, lapsed at T17 after resume" (R4-3). What the re-hold stops depends on the surface's value (§4.6, R6-3): the run stops at its next action only where it is *enforced by the host loop*. | VER-002 |
| FX-40 | Run ended | CP-L4 is waiting (T16a not yet done). Engineer A stops run 12, then performs T16a's A4. The person starts a new run, "continues run 12". | Run 12's CP-L4 stays *waiting* with a run-ended event. The later A4 is shown "after run end" and changes nothing. The new run inherits no arrival or disposition. At its arrivals, T16a's A4 counts for S-4 where S-4 is bound and its content is unchanged, cited with its time (§4.5; DECISION-K1 K1-2); under the governance-phase option it shows "prior act not counted" (R4-4). | VER-002 |
| FX-41 | Supersession (C V-GR1) | `CP-grant` is performed by T15's A12, captured after the r15 arrival and established as ⟨set-2⟩. Later: (a) an established A12 narrows P-03's scope; (b) an A12 that the control refuses. | (a) The first A12 shows *superseded by ⟨act⟩*, not lapsed; `CP-grant` stays *performed*. (b) No supersession; ⟨set-2⟩ stays in force (R4-6). | VER-001, -002 |
| FX-42 | A13 disable | The agent attempts to disable external access; separately, the agent requests it. | The attempt is *not permitted* (INTEGRATION, R2-3). The request is an A8, offered. | VER-004 |
| FX-43 | A10 operation | The agent invokes OP-C8. | *not permitted* (P-02). An A8 is offered. | VER-004 |
| FX-44 | Checkpoint list | Checkpoint variants: (i) naming A3; (ii) naming A10; (iii) naming "sign-off"; (iv) a `CP-grant` variant whose declaration names no setting content, even when an A8 at arrival presents one. | (i) and (ii) **invalid**. (iii) **not established**. (iv) **invalid**, unconditionally and before the run (R5-3; WD FB-17; WD VC-41; EXEC CH-29). | VER-001 |
| FX-45 | Earlier act (R4-5; DECISION-K1 K1-2) | CP-L5 arrives at T3. T2's A4 on S-2 was captured before that arrival. | T2's A4, on S-2 content still current at T3, counts for S-2 and is cited with its time. CP-L5 stays *waiting* for an A4 covering S-1, S-3 and S-4; with it the arrival is answered by two acts (joint answer, §4.3). Under the governance-phase option: T2's A4 is "prior act not counted"; CP-L5 waits for an A4 over S-1…S-4 captured after T3; an act whose order cannot be established → "act order unknown". | VER-002 |
| FX-46 | A12 control relation (C V-GR1) | At `CP-grant`, which arrived at r15 before T15, T15's A12 is (a) pending, (b) refused, or (c) has its confirmation observation lost. | (a) *waiting*, "A12 awaiting control confirmation". (b) *waiting*, "refused by control: ‹reason›"; ⟨set-1⟩ stays in force; no supersession. (c) *unknown*. | VER-001, -002 |
| FX-47 | A13 capture (R4-13) | (a) The agent writes an App-side access configuration (ADAPTER L-ADAPTER-2). (b) Engineer A directs an App-side configuration change in the App. (c) Engineer A enables access in the host's enablement facility. | (a) Not A13 and not A13 evidence; the channel stays disabled; an evidence limit is recorded. (b) An ordinary configuration change, not A13; it enables nothing alone. (c) A13, captured by the host with a capture-evidence reference, which is required (U-04e) — **AWAITING INPUT**: SQ-28 answered 2026-09-28: SWBPIPE has no facility, none planned (not offered), so (c) cannot occur there; a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3). | VER-004 |
| FX-48 | Hold support (R5-1; R4-2; R8-1, R8-2) | (a) L-ACT-7: an App run with `CP-grant` of kind (a) on a harness capability. (b) E1 run from the App over X. (c) An App run over X in which a run action occurs while `CP-L4` waits. (d) A `CP-L4` variant that also holds an App-side return step. | **Phase 1** (§4.0): no hold-support value in any variant, and no *unsupported* for a hold reason. (a) The check is *not established* because the harness-capability reference is unresolved (a required-tool matter, R8-11 item 3). (b) The check is decided by required tools and channel state. (c) Nothing is held; the action may carry "continued past CP-L4 before A4". (d) As (c). **Governance phase** (read as governed): (a) *not enforceable* (HS-5): the workflow is **unsupported**. (b) `CP-accept` **not enforceable** (HS-3 (c); SQ-02 answered 2026-09-28) and `CP-check` *not enforceable* (holds Return, HS-5); the workflow is *unsupported*. (c) `CP-L4` is HS-3 (c): **not enforceable** (SQ-02 answered with no host-held route), so the workflow is *unsupported*; nothing is stopped, and the action is recorded as **action during hold** (R6-3). (d) *not enforceable* (HS-5), whatever SQ-02 returns. App-side holds: D6 re-opens with the governance phase. | VER-001 |
| FX-49 | Not act evidence (R4-12) | Engineer A answers an MCP elicitation "Mark S-4 checked? yes". Separately, a conversation statement: "I checked it". | Neither is A4 nor capture evidence. CP-L4 stays *waiting*. The App may present its own act control (EXEC CAP-6). | VER-002 |
| FX-50 | Carriage assurance (R5-2; R4-14) | As in V-CP1, with native carriage: the constraint is model-supplied only, and the model omits it. | **Phase 1:** no constraint is carried or enforced by the App, and no hold-support value is assigned; the agent adds no field the host lacks (R8-10). **Governance phase** (read as governed): model-supplied carriage does not satisfy R2-12, and the omission is recorded as an evidence limit. `CP-accept` hold support: **not enforceable** (SQ-02 answered 2026-09-28: the host holds no copy of the declaration; model-supplied only; HS-3 (c)), so the workflow is *unsupported*. App side: `UNRESOLVED{D6}`, re-opened with the governance phase. (The ADAPTER U-X3 citation is retired; EXEC §3.6 answered it. This is the HS-3 case for an A5 constraint.) | VER-004, -006 |
| FX-51 | Grant before arrival (R5-7) | An E1d run in which the arrival of `CP-grant` is the hold of the OP-C9 call at T16, *after* T15's A12. Compare V-GR1, where `CP-grant` arrives at r15, before T15. | Here T15's A12, on the declared content with ⟨set-2⟩ still in force, counts: `CP-grant` is *performed* at its arrival, citing T15's A12 and its time, and the OP-C9 call proceeds as T16 (§4.5; DECISION-K1 K1-2). Under the governance-phase option, T15's A12 is "prior act not counted" and `CP-grant` stays *waiting* until the grant change is repeated. In V-GR1, T15 counts as well: *performed*, and the held call is dispatched unchanged as T16. | VER-001, -002 |
| FX-52 | A8 cannot change the subject (R5-3) | V-GR1, but the agent's A8 at arrival presents a narrower setting {P-03, *direct*, {FX-W1; {S-3}}} than the declared {FX-W1; {S-4}}. Engineer A performs an A12 on the A8's content, and the control establishes it. | The A12 is recorded and establishes its setting. It **satisfies nothing** at `CP-grant`, which stays *waiting* for an A12 on the declared content. | VER-001 |
| FX-53 | Operation records (R5-6) | (a) T2: Engineer A operates OP-C6 on S-2. (b) T6: Engineer A edits S-3 in the host UI (the person's own A2). | (a) One human-act record (A4, direct capture), and an R7 operation entry referencing it. (b) An R7 operation entry with the person as actor, and no human-act record. | VER-002 |
| FX-54 | Phase-1 guidance (R8-1; §4.0) | An App run over X, `CP-L4` declared (not `governed`). `CP-L4` arrives at T16. Before T16a: (a) the agent issues a further host operation; (b) the agent writes an A4 record naming Engineer A, with no capture evidence; (c) the agent invokes OP-C6 on S-4. Then (d) T16a's A4 is captured by the host facility. Variant (e): the same checkpoint declared `governed`. | (a) Recorded normally; it may carry "continued past CP-L4 before A4"; not a defect, refusal or finding, and not *action during hold*. (b) Non-conformant; no A4 is recorded as performed (AP-3). (c) *not permitted*, with an A8 offered (P-02; AP-4): reserved acts stand. (d) The A4 is recorded as performed; the arrival's record label becomes *performed*. No hold-support value and no *unsupported* for a hold reason appear at any point. (e) Same in Phase 1: the flag is shown and honoured only as guidance (AP-10). | VER-001, -002, -004 |
| FX-55 | Network-destination grant (R8-13; §2.7; L-ACT-8) | A host-loop run. (a) Engineer A switches web access on in the allow list. (b) The agent asks for A-1; Engineer A grants it once, then for this run, then always for "other APIs" (three variants). (c) Engineer A declines the request. (d) The agent writes an allow-list entry for A-1 itself. (e) Engineer A tries to allow M-2. | (a) An A12 network-destination grant (allow-list edit) with capture evidence. (b) An A8, then an A12 network-destination grant per variant, each with its scope, time and source "in-work"; *once* is consumed by the one call, *this run* ends with the run, *always* becomes a list entry. (c) An act-declined event of kind A12; the agent receives "destination not allowed by the person". (d) Not an act; the list is unchanged; at most an A8. (e) Refused, reason "not stateless MCP (2026-07-28)". No operation-class grant changes in any variant (ND-A1). | VER-002, -004 |
| FX-56 | Workflow registration (R12-5; L-ACT-9) | (a) Engineer A registers revision rev-4 of `supports-adjust`, reviewed as draft d-12, at the App act control (DEL-01-04; AAC-v0.2 §4.2). (b) The agent reports "rev-4 is ready and registered" with no control operated. (c) The definition changes to rev-5 and the agent carries rev-4's registration forward. (d) A declared checkpoint names A15. | (a) An A15 human act, direct capture, bound to rev-4's revision identity (= d-12's reviewed content identity), with reviewed draft d-12 and no prior revision (the first revision in the project library's slot; WD's derived-from is not this act's relation, C-21), purpose "make it available in the project library" (RS-v0.9 HA-10; act-log record 1). (b) No act (§2.6); rev-4 stays a draft. (c) rev-5 is a draft until its own A15; the earlier A15 does not carry over. (d) **invalid** in this increment (§4.1) | VER-002, -004 |
| FX-58 | Several entries in one act (DECISION-L L-4; L-ACT-9; v0.9) | (a) Two workflows already in the project library without a registration record (WR LS-2) are reviewed and registered in place in one act. (b) A third entry is byte-equal to a shipped revision. (c) As (a), but one entry changes after review | (a) One A15, direct capture, binding each entry's bytes: registered entries in order, each with its reviewed content and no prior revision (RS-v0.9 act-log record 4). (b) Recognized as the shipped revision (origin *bundled*, registered by the release, WR LS-5); no A15. (c) Nothing is captured; review again (K-8; AAC AK-c). Expectations (b) and (c) follow WR-v0.2 and AAC-v0.2 (PROPOSED) | VER-002, -004 |
| FX-57 | Policy-class record structure (ACT 7; §8.1) | The P-01…P-06 instances and the three invalid records, validated by `prototype/validate_policy.py` | The instances validate; each invalid record fails for its stated reason; identities are unique; no reserved record is widenable. **Ran 2026-09-30 on the prototype: held** | VER-007 |

---

## 14. Findings (reported, scope unchanged)

- **F-1 Register asymmetry.** Eleven local DOWNSTREAM rows (DEP-04-01-012…016, -022…027) now mirror eleven of the twenty consumers that declare DEL-04-01 upstream (§10.3; V1-A RF-02). The nine without a local mirror row are DEL-09-06 and eight deliverables outside the first increment. DAG-003 admits all twenty arcs from the consumers' rows, so the asymmetry gates nothing. Whether this register should mirror the nine is a register matter, returned by Wave A and not decided here.
- **F-2 Design-candidate approval.** It has no canonical name yet. One will be needed in the Domains increment.
- **F-3 A10 and A11.** Both are named by R-1. A10 is reserved by derivation, not by D2.
- **F-4 Consequence vocabulary.** Still no owner decision (U-02).
- **F-5, F-7 (closed in v0.3).**
- **F-6 D2(b) wording.** D2(b) does not address a voluntary proposal under a direct grant. S3 already makes every A5 a person's act.
- **F-8 OI rows.** OI-001 and OI-002 are ruled for the first increment by DECISION-1. `Open_Issues.csv` keeps both rows OPEN by the owner's decision (OWNER_ITEMS Q-5, option A, accepted at DECISION-2 of `APP-V4-SCA002-20260929`), and their Consequence field points to DECISION-1 D2/D3 (SCA-V4-001; OWNER_ITEMS O-17). Settled; nothing is pending.
- **F-9 (closed in v0.3).**
- **F-10 SoW wording (IR1A-20) (closed at v0.7).** The ScopeOfWork was revised by SCA-V4-001: TBD-001, TBD-002, AC-004 and VER-004 now name DECISION-1 D2/D3 and leave only OI-021 open (ScopeOfWork sha256 ac043e54…b875).
- **F-11 A13 disable is INTEGRATION.** D2e names only enabling. The owner may wish to confirm this.
- **F-12, F-13 (closed in v0.4).** V2 confirmed them against the sibling v0.3 texts (m-12).
- **F-14 Rules adopted by citation from EXEC.** EXEC-v0.2 marks these as ADOPTED by R4: re-hold (§4.7), A12 control relations (§4.10), and no resumption (§4.9, whose standing is still PROPOSED). SP-6 (capture after arrival) and App-side capture (§5) stay PROPOSED in EXEC. This contract carries each at the same standing. (Node A3: DECISION-K1 K1-2 settled SP-6 as the earlier-act rule for the current phase; capture after arrival is EXEC SP-6F, a governance-phase option.) The §2.6 A13 ruling is PROPOSED (R4-13). From v0.6, re-hold is governance phase (R8-1; EXEC-v0.4 §4.7); the other rules apply in both phases as recording rules.
  - resume point, re-hold, capture after arrival, no resumption, A12 control relations (§2.3, §2.5, §4.3, §4.5);
  - the §2.6 A13 capture ruling.
- **F-15 (new) A13 depends on a host enablement facility.** If SWBPIPE has no enablement facility that yields a capture-evidence reference, A13 cannot be evidenced. The external channel then stays *not enabled* by this contract's reading, which is conservative but may block V4-EXM-25. Relay question U-04(e). **Confirmed by SQ-28 (2026-09-28):** SWBPIPE has no facility and none is planned, so V4-EXM-25 cannot run against SWBPIPE until its owner adds one (a SWBPIPE owner decision; host joins deferred, DECISION-3; R8-6).
- **F-16 D6 leaves App-side checkpoint enforcement HELD, and App-only checkpoints can never be enforced in this increment.** Per R5-1 and R5-10, the SQ-02 answer can make checkpoints on **host operations** *enforced on the host route*. App-only checkpointed workflows remain *not enforceable*, and therefore *unsupported*, whatever SWBPIPE answers. That is a separate D6 follow-up for the owner. It affects the VER-001 checkpoint cases and V4-EXM-22 in App runs. **R8 disposition:** in Phase 1 checkpoints are guidance, so no workflow is *unsupported* for a hold reason, and D6 is closed for Phase 1 (DECISION-4; R8-2). In the governance phase, SQ-02 was answered with no host-held route, so host-operation checkpoints on SWBPIPE's X are also *not enforceable* (§4.6). The amended V4-EXM-22 (SCA-V4-001) says the same of the examination: "stopping the run at the checkpoint is examined only for a workflow that takes up the governance phase (V4-WF-05)".
- **F-20 (v0.6; closed at v0.7) Wording of S9, D2 and V4-WF-05.** At v0.6 this finding asked that the accepted wording of S9, of D2's checkpoint clause and of V4-WF-05 be brought into line with the phasing (EXEC F-29). Closed by record: SCA-V4-001 amended V4-WF-05 and V4-HI-42 (accepted 2026-09-29), and the owner confirmed the R8-11 item 2 reading of D2 (OWNER_ITEMS O-25; DECISION-7 of `APP-V4-BASIS-ALIGN-20260928`). S9, §3, AP-8 and AP-11 now cite the amended texts (R9-1, R9-2). DECISION-1 is not rewritten.
- **F-21 (new, v0.6) R2-4 not met by SWBPIPE.** SWBPIPE refuses a request for Apply on X as `unsupported_method` and names no rule (SQ-06), so R2-4's *not permitted* naming a rule has no SWBPIPE occasion. It is recorded, not repaired App-side (§6; R8-5).
- **F-17 (new) Capture-after-arrival costs a repeat (R5-7).** Under SP-6, a grant change captured before its checkpoint's arrival does not count, even when its content is already in force (FX-51). The person must repeat it. This owner-visible cost is recorded under U-14 (EXEC U-E4; WD U-31). **Closed** by DECISION-K1 K1-2: in the current phase FX-51's grant counts; the repeat arises only under the governance-phase option.
- **F-18 (closed at v0.7) R5-3 reverses R4-9's A8 precedence.** The declared setting content now always binds. Consumers that implemented "A8 names the setting" (v0.4 §4.2) had to change: WD, LOOP, PANEL and EXEC are listed by R5-3. Closed by record: all four carry the rule (WD §4.3.1, grant setting; EXEC §4.10, subject; LOOP §2.4, grant setting; PANEL §3.5, grant setting), as read in their texts at commit `3dd7c22c73`.
- **F-19 (closed at v0.7) Human-act records and R7.** The record kinds now split cleanly (R5-6): a reserved-act operation yields a human-act record referenced from R7, and the person's own A1/A2 yields an R7 entry only. Closed by record: RS carries the reference (RS §3, human-act record; RS §5, entry elements).
- **F-22 (new; R8-13) Destination grants under D2 (e).** D2 (e) names "changing the autonomy grant". DECISION-5 makes a network-destination grant person-only, and R8-13 maps it to A12 under (e) by INTEGRATION. DECISION-5 point 3 (the person-only grant) stands, and U-17 is closed. The A12 mapping stays INTEGRATION; the owner may revisit it at any time.

---

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| U-01 `UNRESOLVED{OI-021}`: first operation, operation-specific reserved additions, its autonomy | Owner via the outside SWB session and App/shared owner. SWBPIPE's own autonomy is SWBPIPE owner decision OI-016 | Before the connected-activity SoW and execution | No additions in P-01/P-03. A concrete first operation is *no policy basis* (pending OI-021); dependent cases are held. SQ-04 answered: no selection (owner decision) |
| U-02 Consequence vocabulary | DEL-04-01 with the host policy owner; the owner at the phase review | Before class assignment in DEL-03-01 | A PROPOSED draft in d3's four dimensions (§8.5), assigned to no record; OP-C5-on-S-4 under ⟨set-2⟩ held (C T15) |
| U-03 *Closed (DECISION-K1 K1-3, 2026-09-30).* Multi-row A4 purpose after partial lapse | The owner (decided) | — | **Settled:** the joint answer (§4.3; EXEC §4.7 JA-1) |
| U-04 Relay questions to the host (§12 item 4 a–f). **Answered 2026-09-28** (SQ-01, SQ-02, SQ-05, SQ-21, SQ-28): none offered | Host owner (DEP-001). For SWBPIPE the residue is SWBPIPE owner decisions (ANS §2): (a) PB-TBD-002 acceptance-record storage and DEL-16-03 actor identity; (c)/(f) a host-held checkpoint route; (d) OI-016 autonomy; (e) an A13 enablement facility | When the owner resumes UI-SUCCESSOR (DECISION-3); before host act-recording integration, governance-phase checkpoint execution, external enablement, or any enforcement claim | Host rows are receiving requirements. (a), (c), (e) answered: none offered. FX-29 and FX-47(c) keep the AWAITING INPUT token with that annotation. FX-50's governance-phase value is determined (*not enforceable*). U-04(d): SWBPIPE reports no settings reference |
| U-05 Recorded person grant; actual performed-act evidence | The person (DEP-04-01-020, -021) | VER-001 and the VER-002 positive cases | Candidate-bound FX-09/FX-20 passes cannot run |
| U-06 Defaults for other consequential classes | SWBPIPE owner decision OI-016 (ANS §2); host policy owner generally (V4-HI-41; DEP-001) | Before those classes are cataloged | *not set* falls to rule 5 (reason unassigned). SWBPIPE: no class system; every change waits for Apply (SQ-05) |
| U-08 *Closed (R12-5, 2026-09-30).* Workflow registration as a canonical act | The integrator (R12-5); captured by DEL-01-04's App act control, registered by DEL-02-02 (K-8; AAC-v0.2, WR-v0.2) | — | **A15 register workflow revision** (§2.1, §2.5, §2.6); not checkpoint-requirable in this increment (§4.1) |
| U-12 Placement of the policy representation | App/shared owners (OI-013, OI-014) | Before production allocation | A PROPOSED structure exists (§8.1) as a schema with conformance fixtures, which every placement needs; no placement is chosen (R12-2) |
| U-D6 `UNRESOLVED{D6}` App-side run holds. **Closed for Phase 1** by DECISION-4 D4-1 (R8-2): checkpoints are guidance, with no App or host-loop hold. **Re-opens only when the governance phase is taken up.** For host-operation checkpoints SWBPIPE answered SQ-02 on 2026-09-28: route (iv), none planned | The owner (DECISION-4; D6 re-opens with the governance phase) | When the governance phase is taken up for a workflow that needs it; before any App-side checkpoint enforcement is claimed | Phase 1: none (§4.0). Governance phase: §4.6 applies the four R5-1 values; HS-3 checkpoints are *not enforceable* against SWBPIPE (SQ-02 answered: none), and App-only checkpoints stay *not enforceable* regardless (R5-10). HP-1 and HP-2 are not adopted, and App-assured carriage is unavailable. FX-48 and FX-50 are DESIGNED, with determined governance-phase values |
| U-14 *Closed (DECISION-K1 K1-2, 2026-09-30).* Counting a prior act captured before arrival, as an alternative to §4.5 capture-after-arrival | The owner (decided; EXEC U-E4; WD U-31) | — | **Settled for the current phase:** an earlier act of the required kind on current content counts, cited with its time (§4.5). Capture after arrival is kept as a governance-phase option. FX-40, FX-45 and FX-51 recomputed. |
| U-15 Per-subject content identity (V4-HI-32) not met by SWBPIPE, which supplies only a whole-model identity (SQ-03; R8-4; EXEC U-E25) | SWBPIPE (PB-TBD-002 / DEL-16-03); owner notice | Before host act-binding integration | §2.5: the whole-model identity is received as every covered subject's identity; over-lapse, never under-lapse; never App-computed |
| U-16 Whether a launch environment variable the person sets counts as A13 evidence (R8-6; I2 R8-Q4b) | The owner (deferred) | When UI-SUCCESSOR resumes | Not A13 evidence meanwhile; SWBPIPE's channel stays *not enabled* (§2.6) |
| U-17 CLOSED — DECISION-5 points settled by the owner's DECISION-5 confirmation (2026-09-28: the "MCP V2" reading confirmed; the person-only grant not objected to and stands): the person-only grant (point 3), and the reading of "MCP V2" as the stateless MCP revision 2026-07-28 (R8-13) | The owner | Before §2.7 is relied on for implementation | §2.7 applied as recorded; the A12 mapping is INTEGRATION (F-22) |

Closed:

- **v0.8, node B4:** U-08 (R12-5).
- **v0.7, node A3 (DECISION-K1):** U-03 (K1-3) and U-14 (K1-2).
- **v0.7:** no UNRESOLVED item. Findings F-10, F-18, F-19 and F-20 are closed by record (§14).
- **v0.6:** none. U-D6 is closed for Phase 1 only.
- **v0.2:**
  - v0.1 U-01/U-02 (DECISION-1);
  - U-08 scope (R-8);
  - U-09 in-flight (R-3.6);
  - U-10 batch (R-6).
- **v0.3:**
  - U-07 (R2-8);
  - U-11 (R2-4).
- **v0.4:**
  - U-09, mixed items: confirmed by DEL-02-03 (R4-7);
  - U-10, re-hold and resumption: R4-3, R4-4;
  - U-13, refused A12: R4-6;
  - ADAPTER U-X1, the A13 locus: R4-13, §2.6.

## Verification cases

These are designed, not run. Each is bound to this file's revision when executed.

| Case | Serves | Procedure | Expected result |
|---|---|---|---|
| VC-001 | VER-001 / AC-001 | Compare §4, §5 and §8 with V4-AUT-01, V4-HI-22/40/42 and D2. Run FX-19…21, -23, -29, -37, -38, -41, -44, -46, -48, -51 and -52 against a recorded grant (U-05). Trace the origin, undo and later-check obligations. Include FX-54. | Direct treatment occurs only in *effective (person-set)* direct within scope (C T15 scope). A policy default gives *propose*. Phase 1 (ScopeOfWork TBD-004 limits the checkpoint cases to recording): checkpoints are guidance, no hold-support value or hold is stated, and no workflow is *unsupported* for a hold reason; reserved acts stay the person's (§4.0). Governance phase: governed checkpoints and the §4.4 constraint (with its carriage assurance) override the grant, and hold support takes one of the four R5-1 values, with SWBPIPE's X *not enforceable* (R8-2). The declared grant setting binds (R5-3). Narrowing, widening, supersession and the A12 control relations follow §5.5 and §2.5. |
| VC-002 | VER-002 / AC-002 | Run FX-01…10, -26, -27, -30…32, -36, -39…41, -45, -46, -49, -53, -54 and -58. | Negatives are non-conformant. Independent acts are conformant without A5. Actor ≠ recorder is kept, with capture evidence. Act-declined and run-ended events are not acts. An earlier act on current content counts, cited with its time (§4.5; DECISION-K1 K1-2), and no resumption holds. A lapse is recorded in both phases; re-hold after resume only in the governance phase. Elicitation answers and conversation are never evidence. |
| VC-003 | VER-003 / AC-003 | Run FX-03, -05, -14 and -15. | No certification or approval claim for agent output. A7 is attributed only to the professional. |
| VC-004 | VER-004 / AC-004 | Compare P-01, P-01a and P-02 with DECISION-1 and their derivations, and inspect host evidence. Run FX-16…18, -22…25, -33, -35, -36, -42, -43, -47, -50 and -58 (b). | No agent can perform, or have attributed to it, a reserved act. Outcomes follow §6, with SWBPIPE's terms received as in the §6 table (never A10, A11 or *not permitted*). A13 is evidenced only by the host facility; SWBPIPE has none (SQ-28). OI-021 and no-policy-basis cases are **held**. Cases whose host input was answered "none" keep AWAITING INPUT with the answer annotated. No host enforcement is claimed without DEP-001. |
| VC-005 | VER-005 / AC-005 | Inventory the wording in this file, §7, FX-11…13 and FX-34. | "accept" for proposals only. "approve" for A6 only. Unqualified "checked" for A4 only. "tool permission" for A14. "rejected", not "declined", for A10. |
| VC-006 | VER-006 / AC-006 | Run FX-19…22, -29, -32, -37, -38 and -50 against V4-HI-41/42/51 and D2. | *Both phases:* default *propose* via *effective (policy default)*. Item, multi-row and batch acceptance. Widening bounded by W-a…j. Local and host evidence are labeled separately. *Phase 1 (ScopeOfWork TBD-004):* the checkpoint cases (FX-21, FX-29, FX-50) are limited to recording: the act is requested, it is recorded only when the person performs it, and a widened grant never records or substitutes it; no constraint is carried or enforced by the App and no hold is claimed (§4.0, §4.4). *Governance phase:* only host-held constraint carriage satisfies R2-12; App-assured is unavailable in this increment. |
| VC-007 | VER-007 / AC-007 | Trace V-01…V-14, V-21, V-25, V-28, V-29 and V-30 to their bases, P-01…P-06 to DECISION-1, their derivations or INTEGRATION, and V-20…V-27 to their owners. | Every value has a basis and a standing label. D2/D3 are not over-credited. V-28 is credited to DECISION-5 and the amended basis for the person-only grant, and to R8-13 (INTEGRATION) for the A12 mapping. D6 is carried as `UNRESOLVED{D6}`, closed for Phase 1 and re-opened with the governance phase (DECISION-4; R8-2). |
| VC-008 | VER-008 / AC-008 | Compare §11 with SoW CLM-002…005 and REQ-007. Run FX-28. Read F-10. | Every excluded act is assigned to its owner. No host, adoption or act claim. |
| VC-009 | VER-009 / AC-009 | Reconcile FX-01…58 with REQ-002…006 and the matrix. When a candidate exists, run the fixtures and retain their IDs, the candidate identity, the results and the limits. | Complete coverage. Held, AWAITING INPUT, governance-phase-only, INTEGRATION-rule results and missing host evidence are reported separately from passes. Phase-1 results and governance-phase values are reported separately. No candidate results at v0.9; FX-57 ran on the local prototype only. |
| VC-010 | VER-001, -002, -004 / AC-001, -002, -004 (ScopeOfWork TBD-004) | Run FX-54 and the Phase-1 parts of FX-21, -29, -36, -39, -48 and -50 against §4.0 AP-1…AP-12 and EXEC PH-1…PH-10. | No hold, block, re-hold or hold-support value; the request for the act, where made, is the agent's A8 and is never issued by the App or a host loop in its place (AP-12); no *unsupported* for a hold reason; acts recorded only when the person performs them, never by an agent on the person's behalf; reserved acts refused to the agent and offered as A8; arrivals and acts appear as observation; "continued past ‹checkpoint› before ‹act›" is optional and never a defect; lapse still recorded; a `governed` flag changes nothing in Phase 1. |
| VC-011 | VER-002, -004 / AC-002, -004 | Run FX-55 against §2.7 and LOOP §5.1.1 NW-8…NW-13. Trace the expected result to EXAMINATION V4-EXM-23 (added by SCA-V4-001). | Every destination grant is the person's A12 (network-destination grant) with capture evidence, scope, time and source. No agent grants itself a destination, and an agent-written entry is not an act. A decline is an act-declined event reported as "destination not allowed by the person". A non-stateless MCP server cannot be granted. No operation-class grant changes. These are the act-policy parts of V4-EXM-23 ("destinations the person allowed, in advance or when the agent asked during its work"; a declined request "is reported to the agent as "destination not allowed by the person""). Observing the host's network traffic is the examination's work, not this contract's. |
| VC-012 | VER-007 / AC-007 (ACT 7, ACT 8; R12-1) | Validate `ACT_POLICY_CLASS_RECORD.schema.json` against the valid configuration and the invalid records (FX-57); compare each §8.3 record with its instance; check that no instance assigns a consequence value while U-02 is open | Every instance validates and every invalid record fails for its stated reason; the text and the instances agree (the text governs where they differ); every consequence is "not assigned" or "not applicable". **Ran 2026-09-30 on the prototype (schema and instances): held.** The text-to-instance comparison was done by reading and is not scripted |

---

## Changes from v0.1 (history, from v0.2)

These rows record the v0.1 → v0.2 changes and are superseded where the v0.2 →
v0.3 table says so.

| V1 item | How addressed in v0.2 |
|---|---|
| V1-A D-01, D-17, D-18, D-20; V1-C D-17 | Canonical names and alias map; A9 as a recording act; closed checkpoint list |
| V1-A D-02; V1-B D-08 | SWB class DERIVED, with default propose (P-03) |
| V1-A D-03 | Reserved class for act-performing operations (P-02). Amended in v0.3 by R2-2. |
| V1-A D-04, D-05, D-08 | Outcome map; *channel not enabled*; host-route resolution; in-flight rule |
| V1-A D-06, D-07; V1-B D-12 | Requester and setting actor separate; A12 evidence; grant scope |
| V1-A D-09; V1-C D-07 | Acceptance checkpoint forces propose. Amended in v0.3 by R2-12. |
| V1-A D-10; V1-C D-03 | Decision pairs; negative events. Renamed in v0.3 by R2-5. |
| V1-A D-11, D-21; V1-C D-06 | Record shape vs capture-evidence satisfaction |
| V1-A D-12; V1-B D-15 | "checked" label rule |
| V1-A D-13, D-14 | A14 origin; DEL-01-01 consumer |
| V1-A D-15, D-16, D-19, D-22, D-23, D-24, D-25; V1-B D-01, D-10, D-23 | Withdraw vs reject; refusal ≠ A10; governing policy reference; grant value vs class; OI-002 not a class; per-item binding |
| V1-A AB-01…AB-10; V1-B X-09, X-10; V1-C AB-01, AB-06, D-05 | Unconfirmed grant; registration held; lapse; A14 location; policy revision identity; D2/D3 records; per-item facts; reserved offering. Offering amended in v0.3 by R2-4. |
| R-9 | Shared fixture adopted. Fully re-pointed in v0.3 by R2-21. |
