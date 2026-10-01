# Autonomy and Standing Exchange
- Contribution: DEL-04-02/AS-v0.8 (supersedes AS-v0.7, last changed at `c896a99d90` and unchanged at `86cafc0e1c`, sha256 7f44fbb3c2ee384795418679b8cee72f6154e042dbf48f848836e3680bdb989c; AS-v0.6, last changed at `caa4334ca1` and unchanged at `3dd7c22c73`, sha256 52d1341bb475f0a7de4b986b905e2986aa0e0a4e04e8b1783a6a83174eb6a33d; AS-v0.5, last changed at `c6f81a4f2` and unchanged at `94aa9181b`, sha256 df0e31ea7d33a3224df0b5d292d35675a55e8e325898cb28b64a1f709f7d72f0; AS-v0.4 sha256 774728d03824397a5343412b17659feaf9b0d2ef1029b79889d13a1b421f4dab at `cc58211c5`)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Phase (R8-1; R9-1): in the current phase (Phase 1) declared checkpoints are **plan guidance**: the checkpoint overlay shows arrivals and acts as observation, and no hold, hold-support value or *unsupported* for a hold reason is shown (§4; ScopeOfWork TBD-006). **In force in every phase:** the act is requested; it is recorded as done only when the person performs it; the reserved acts bind. **Phased to the governance layer:** holding the run until the act (PRD V4-WF-05 and HOST_INTEGRATION V4-HI-42 as amended by SCA-V4-001; S3). Hold support, re-hold and *action during hold* are kept as the **governance-phase definition (retained)**.
- Network-destination grants (R8-13; DECISION-5): the grant display also shows a host agent's allow list (category switches and named entries) and its in-work grants with their scopes (once, this run, always) (§3). They are the person's A12 grants, subclass network-destination grant (ACT §2.7). V4-HOST-02 is cited from the PRD as amended by SCA-V4-001, which applies DECISION-5 (S15). From v0.8 (node B5) this file also owns the **display of the destinations contacted** (§3.2), as its ScopeOfWork CLM-002 consumes the contacted-destination record "which `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5` requires to be shown"; the flow it displays is DEL-05-01/LOOP-v0.8 §5.3 (DF-1…DF-10). Recording a declined or refused request is PROPOSED (R12-10).
- Wave B (R12-1…R12-3): the settings-in element has a **PROPOSED** representation, `AS_SETTINGS_IN.schema.json` beside this file, with valid and invalid examples validated by a local prototype (`prototype/`); in-work destination-grant transitions (§3.1); the §6 exchange (identical to RS §8) carries a host agent's destination settings and contacts; what each receiver is provided and what it does on *unconfirmed* or *missing* (§12.1); the OUT-001 component structure as PROPOSED options under OI-014, none chosen (§13; R12-2).
- Serves: OUT-002 (receiving-interface contract content); OUT-001 and OUT-003 (component behaviour and fixture design only — no component or fixture exists; the prototype is not product code); REQ-001…REQ-007; AC-001…AC-007 via designed VER-001…VER-007
- Basis (re-pinned at v0.7; R9-5): the accepted basis as amended by SCA-V4-001 (`P/execution/_ScopeChange/SCA-V4-001_2026-09-28_2155/`) and SCA-V4-002 (`P/execution/_ScopeChange/SCA-V4-002_2026-09-29_1901/`), by current sha256: `P/docs/PRD.md` bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd, `P/docs/ARCHITECTURE.md` 317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c, `P/docs/HOST_INTEGRATION.md` d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f, `P/docs/EXAMINATION.md` 471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0 (of the requirement texts this file cites, V4-WF-05, V4-HI-42, V4-HI-70, V4-HOST-02, V4-EXM-22 and the ARCHITECTURE §4 host-agent properties were amended; the others are unchanged since repo `6e18505e3`, the v0.6 basis; checked with `git diff 6e18505e3 HEAD -- docs/`); ScopeOfWork.md sha256 f16ffa8a33cbfb2e78a8e916e90aff9fb44ad20adf94fe61a559a213f5564460, as revised by SCA-V4-001 (AX-004; TBD-006 added) and SCA-V4-002 (AX-005; CLM-004); owner decisions `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-4` (D4-1 phased checkpoints) and `-DECISION-5` (host-agent network destinations), `OWNER_DECISIONS.md` sha256 5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2; owner confirmations at the SCA-V4-001 checkpoint, run `APP-V4-BASIS-ALIGN-20260928`, `OWNER_DECISIONS.md` sha256 ca8c4e50df1d7dddb41b875a4afe46eea4f1a1bf2491d255b7890d0d71cd254b (DECISION-7 accepts `AMENDMENT_PACKET/OWNER_ITEMS.md`, sha256 2b90eb4a95f458e993eed69e27533aa10e31aea980fe2ec99c9c2345e6f498ef, "as recommended": O-10, O-11, O-15, O-25); accepted graph `P/execution/_DAG/_LATEST.md` (sha256 4d381ba4e87b41a83b9d0d2dc591c4bf04eacb84df0b5c27314091cd2a992f56) → DAG-003; `P/docs/PRD.md` §2.2 V4-HOST-02, §4.1 V4-WF-05, §4.3 V4-EXE-01…03, §4.5 V4-AUT-01…05, §4.6 V4-PM-06, §4.7 V4-REC-01…05; `P/docs/HOST_INTEGRATION.md` §1, V4-HI-04, V4-HI-11/12, V4-HI-20…25, V4-HI-30…33, V4-HI-40…42, V4-HI-50…52, V4-HI-70/71, §11; `P/docs/ARCHITECTURE.md` §4, V4-ARC-20; `P/docs/EXAMINATION.md` V4-EXM-21/22; `P/docs/OPERATING_METHOD.md` V4-OPS-30…32; `DECISION_BRIEF.html` d2, d3; `OWNER_DIRECTIONS.md` J, O; `SCC-CASE-002/Case_Datasheet.md` M1, M3; `_Decomposition/Open_Issues.csv` OI-001/002/013/014/021; `External_Dependencies.csv` DEP-001. Run folder `APP-V4-FIRST-INCREMENT-20260928` at commit **8fb51f07f**: `OWNER_DECISIONS.md` (DECISION-1 and DECISION-2; sha256 a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c); `R1_RESOLUTIONS.md` (2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4); `R2_RESOLUTIONS.md` (77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088); `R3_RESOLUTIONS.md` (202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf); `R4_RESOLUTIONS.md` (50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24); `R5_RESOLUTIONS.md` (254d0b93b9959419a70c6737b07087e1db59b529adc3105a1db31f82b78dd6f1); `reviews/V2.md` (75ba1dff8a0c4fa2eb294471127147cbd19a0925daf9169b32ddc88727dde6ef); `reviews/V3-A.md` (f25f5af1177b7fe2a698bd4ef1e1caafa4c2ef25cfc73111f031e17c7cc21d87); `reviews/V3-B.md` (5662fbd09025f5ad9459861370159d606fcced76b394980199e861555a1954a3); IR1-A/B/C and V1-A/B/C as cited in AS-v0.3
- **Consumed inputs for v0.8 (Wave B of run `APP-V4-DESIGN-PASS-2-20260930`, node B4; read from the working tree on commit `86cafc0e1c`; paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/`).** `BRIEFS.md` sha256 ccb4d9f036fb7ff531fffa0d309533b15cf1ebb39b0320651ed4bd5d88efc550 ("Common rules"; "Wave B — design development", row B4); `R12_RESOLUTIONS.md` sha256 95f3011b436b6faa3de098059e77eac836c165e0bb98a5ed94e28918a3a749a1 (R12-1…R12-10; binding); `OWNER_DECISIONS.md` sha256 1dfd5bf4619b329719136b1646030e3f871fd7ffc52dbfd12265414e515aaf15 (DECISION-K1, with the later model-download record; supersedes for currency the pin in the node A4 line below); `SURVEY/S1-A.md` sha256 87baa03d7cbc9b0a6b8e8543d8cd80a7d71c754da80fbfdc053c8e6ef21045f6 (§2.5, §2.8 items 4, 5, 7, 8; advice, checked against the current text); `_Decomposition/Open_Issues.csv` OI-014 ("Place shared contracts/components against actual consumer responsibilities; agree ownership before any common implementation, without presuming a common service"). Siblings by label and section (R9-5): DEL-05-01/LOOP-v0.7 §2.3, §5.1.1 NW-8…NW-16, §6.2; DEL-05-02/PANEL-v0.7 §3.6, §3.8 ND-1…ND-5; DEL-03-02/P-v0.7 §3.3; DEL-03-03/ADAPTER-v0.5 §5.5; DEL-02-03/EXEC-v0.5 §4.10. ACT-POLICY-v0.8 and RS-v0.8 were revised by this executor in the same node; §6 here and RS-v0.8 §8 are byte-identical from "**Settings-in" to the end of the section.
- **Current pins of this run's records (node A4 of run `APP-V4-DESIGN-PASS-2-20260930`; in place, no version bump; R11-3).** Each sha256 recomputed with `shasum -a 256` in the working tree at this pass; paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/`: `R9_RESOLUTIONS.md` sha256 a64e241519b7d158165a7ede0ffdd22eec0af15b6812b5300755f5f38abd59b8 (R9-1…R9-11; R9-2's second bullet as corrected by R10-1); `R10_RESOLUTIONS.md` sha256 ad3b6caa4a12660db77abc51b5c02ba70519ee46d55b40d21ee76eb3ca561796 (R10-1…R10-11); `R11_RESOLUTIONS.md` sha256 e7343b6663b6aeeb2dc506d3391f5b310088e7688d1b21e65d2ba1d8616b3615 (R11-1…R11-9, the repairs from review V17); `OWNER_DECISIONS.md` sha256 7458e9e81971676337a34280b4e8b29a7d04fce5fc202da5b9f5cf7ccd8f9ae5 (DECISION-K1). These supersede for currency the earlier pins of the same records in this header and in the change-table rows, which record the bytes read at node A1 or A3.
- Consumed inputs for v0.7 (Wave A of run `APP-V4-DESIGN-PASS-2-20260930`, node A1-A; read from the working tree on commit `3dd7c22c73`; paths under `AgentRuns/APP-V4-DESIGN-PASS-2-20260930/` unless stated): `R9_RESOLUTIONS.md` sha256 c3efe2ffa232dd9293202d4fc891eba4325afeb2e224fecdf8c1b4c5122a9d2c (R9-1…R9-11; binding); `BRIEFS.md` sha256 698d91d8217cee528812529fa353faac899b4bc1a5be5686552ad88dad6c469a ("Common rules", "A1 — alignment wave", row A1-A); `SURVEY/S1-A.md` sha256 87baa03d7cbc9b0a6b8e8543d8cd80a7d71c754da80fbfdc053c8e6ef21045f6 (advice; each item applied was checked against the current source). Rulings R1–R8, by file: `R1_RESOLUTIONS.md`…`R7_RESOLUTIONS.md` in `AgentRuns/APP-V4-FIRST-INCREMENT-20260928/`, and `R8_RESOLUTIONS.md` in `AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/` at its current sha256 44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b; they stand except where R9 amends them (R9-2 restates R8-11 item 2 and R8-12 item 2). SWBPIPE's answers, DEL-09-06 `Design/RELAY_ANSWERS_SWBPIPE.md`, at its current sha256 afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74: the v0.6 pass read the state 6f01add3…61c7; three answer lines differ between the two states (in SQ-04, SQ-09 and P7; `git diff 94aa9181b HEAD`), and none is a statement this file cites; data about SWBPIPE's current state, not commitments (DECISION-3). Sibling Design files are cited by version label and section only (R9-5), and their bytes are pinned in GUIDE's input table alone; Wave A labels (R9-11): DEL-02-03/EXEC-v0.5; DEL-02-01/WD-v0.7; DEL-02-01/WD-EX-v0.7; DEL-03-01/C-v0.7; DEL-03-02/P-v0.7; DEL-03-03/ADAPTER-v0.5; DEL-03-04/GUIDE-v0.4; DEL-04-01/ACT-POLICY-v0.7; DEL-04-03/RS-v0.7; DEL-05-01/LOOP-v0.7; DEL-05-02/PANEL-v0.7; DEL-01-01/HOSTING-BOUNDARY-v0.7; DEL-01-01/PIN-SPIKE-v0.1; DEL-09-06/CA-v0.5; DEL-09-09/XT-v0.5; DEL-09-06/RELAY-v0.3. The Wave A executors edit in parallel, so the label is cited and nothing here relies on another executor's Wave A text. ACT-POLICY-v0.7 and RS-v0.7 were revised by this executor; §6 here and RS-v0.7 §8 are byte-identical from "**Settings-in" to the end of the section. The byte pins in the consumed-input lines below are true records of what each earlier pass read; they are history, not current pins.
- Consumed inputs for the R8-13 pass: **R8-13 pass (node B1; in place, no version bump).** OWNER_DECISIONS.md sha256 5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2 (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`: V4-HOST-02, host-agent network destinations) and R8_RESOLUTIONS.md sha256 44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b (R8-13) at `1528a5033`; OWNER_DECISIONS.md in its state that adds the owner's DECISION-5 confirmation (committed with this pass); BRIEFS.md sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517 ("Common rules", "A-wave"). Revised in the same pass (node B1), versions unchanged: LOOP, PANEL, ACT, AS, RS, HOSTING, C, ADAPTER and GUIDE; their byte pins are in GUIDE-v0.3's input table.
- Consumed inputs for the R8-12 closing pass: **R8-12 closing pass (node A6; in place, no version bump).** R8_RESOLUTIONS.md sha256 d4c3423310a857af86692d17ddfdd22fa877ee20b07c46e1ee481d1cd750e7af (R8-12, items 1 and 7 applied here). Current sibling versions after R8, as committed at `7a1508452` with A6's in-place R8-12 edits (their byte pins are in GUIDE-v0.3's input table): DEL-02-03/EXEC-v0.4; DEL-02-01/WD-v0.6; DEL-02-01/WD-EX-v0.6; DEL-03-01/C-v0.6; DEL-03-02/P-v0.6; DEL-03-03/ADAPTER-v0.4; DEL-03-04/GUIDE-v0.3; DEL-04-01/ACT-POLICY-v0.6; DEL-04-03/RS-v0.6; DEL-05-01/LOOP-v0.6; DEL-05-02/PANEL-v0.6; DEL-01-01/HOSTING-BOUNDARY-v0.6; DEL-01-01/PIN-SPIKE-v0.1; DEL-09-06/CA-v0.4; DEL-09-09/XT-v0.4; DEL-09-06/RELAY-v0.3. SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` and `FACTS_SQ01_SQ32.md` are unchanged (data about SWBPIPE's current state, not commitments; DECISION-3).
- Consumed inputs for v0.6 (R8 pass, node A2), read with `git show` from commit `94aa9181b` (paths under `AgentRuns/APP-V4-SWBPIPE-INTAKE-20260928/` unless stated): `R8_RESOLUTIONS.md` sha256 1770c96e62caf14322811fca82ceb77eca450d3e1be8665cdbdd5550631e8d02 (R8-1…R8-7, R8-10, R8-11; binding); `INTAKE_MAP.md` (I2) sha256 3cc182955c0f3dd70efa0f1c051870229c2ccc08f36c5cf1445f2eef0dd1ea33 (rows 01.8, 02.9, 05.3, 10.5, 23.2, X.5; Part 2 P2.1, P2.4, P2.8, P2.16, P2.17 and its §2.2 AS rows; Part 3 items 2, 3, 10; Part 4.9–4.11; R8 overrides I2 where they differ); `BRIEFS.md` sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517 ("Common rules", "A-wave"); `OWNER_DECISIONS.md` sha256 a5ccab0d39bd1cab37c5556abc9bdedd5341ce76be4712706c8c9d72d623e776 (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3`, host joins deferred; `-DECISION-4` with its clarification, D4-1 phased checkpoints). Owner files revised first in the same pass: DEL-02-03/EXEC-v0.4 sha256 d32be37797a3c367d342a2d13bbb8dd4279bc52934531d83b8c6ec8c6e7b76d4 (§2.1 PH-1…PH-10, §2.2 GV-1…GV-5, §3.5, §3.6, §4.7, §4.11 receiving notes, §7.2); DEL-02-01/WD-v0.6 sha256 fce565edfd0cee3fa4583eb292d11cce3e4121ead0cdbed31ba2fe0a52562f28 (§4.3.0 CG-1…CG-7; §4.3.1 `governed`); WD-EX-v0.6 sha256 950b70b2e3f7fdda9a98b13a63746b76936be490dd96cb6e47bbe6dc9c3eba3d. SWBPIPE's delivered answers DEL-09-06 `Design/RELAY_ANSWERS_SWBPIPE.md` (#1047) sha256 6f01add3977761e42ac6b310faf72ba4fd5455e478605deb83fefb2e4d3a61c7 (SQ-01, SQ-02, SQ-03, SQ-05, SQ-06, SQ-07, SQ-09, SQ-10, SQ-11, SQ-13, SQ-20, SQ-23, SQ-28; ANS §2): relayed and answered 2026-09-28; data about SWBPIPE's current state, not commitments; no host evidence, commitment or contribution received (DEP-001; DECISION-3). DEL-04-01/ACT-POLICY-v0.6 and DEL-04-03/RS-v0.6 were revised concurrently by the same executor; §6 here and RS §8 are byte-identical.
- Consumed inputs (v0.5): DEL-04-02/AS-v0.4 (sha256 774728d03824397a5343412b17659feaf9b0d2ef1029b79889d13a1b421f4dab, commit cc58211c5); DEL-04-03/RS-v0.5 (revised concurrently by the same executor; its §8 is byte-identical to §6 here). Current sibling versions read from commit **8fb51f07f** with `git show` (not the working tree): DEL-02-03/EXEC-v0.2 sha256 7f7848c0de2fdb4dc21f5adafa97f92e179bb66c9f6b04f3434d8f2342317af0 (§2 HP-4/HP-H, §3.6, §4.5, §4.7, §4.10); DEL-03-01/C-v0.4 sha256 e929d39d3ff9515702f9bfe51dfada537e1cbd165146ec0de4ccf629c659a08c (§10.1 FXA-1…FXA-5; §10.3; §10.4); DEL-04-01/ACT-POLICY-v0.4 sha256 d6da05abe790a4374df7faf225439a01dc1be734491b499d90cf00533369b03b; DEL-01-01/HOSTING-BOUNDARY-v0.4 sha256 201ea32005dd2c9fb5281a376eb25eebfcb5a644d09a6d3bf5901aaf934c7e58 (§8.3); DEL-03-03/ADAPTER-v0.2 sha256 a2905dda5782d7a48fa35ef7e26b0c1517fd3bd995e3ddbba27d2426a25674bc. R6 in-place pass (no version bump): C-v0.5 `CATALOG_AND_READ_BASIS.md` sha256 a6306bd477decad22d4405fb86ca6212fb189e4865c68dbbcba90e1335be7a29 (§10.4 V-GR1, GR-1…GR-3, GR-P/GR-R/GR-S) and DEL-02-03/EXEC-v0.3 `EXECUTION_COMPATIBILITY.md` sha256 889e48819baa21ec112c4878e4e38004dcbaa9eb3645a31c24221ac116ee548e (§3.6 HS-1…HS-5, F-24), read at commit d3cebd1cc for the R6 in-place pass; R6_RESOLUTIONS.md and reviews/V4-A.md at commit c7f5513db. The R5 elements earlier marked "per R5-n" are now present in those sibling texts.
- Receivers (rebuilt from the ACTIVE register rows at v0.7; R9-6; the table is §12): CASE-002 M3 — DEL-04-03 (OUT-001/002; REQ-002; VER-001) receives settings-in (DEP-04-02-009; its own row DEP-04-03-022); DEL-04-02 compares under OUT-003; REQ-002; VER-002. The visible autonomy state (ScopeOfWork CLM-002) goes to DEL-05-01 (DEP-04-02-019; its own row DEP-05-01-025), DEL-05-02 (DEP-04-02-020; its own row DEP-05-02-019), DEL-03-02 (DEP-04-02-021), DEL-03-03 (DEP-04-02-022) and DEL-02-03 (DEP-04-02-023). Declared upstream in the consumer's own register only: DEL-03-04 (DEP-03-04-012), DEL-09-06 (DEP-09-06-031) and DEL-09-09 (DEP-09-09-022). DAG-003 admits the arcs to DEL-03-04 and DEL-09-06 and holds the others as non-gating candidates in SCC-002. No row records satisfaction. Host builder via DEL-03-04 and the external SWBPIPE owner through human relay (DEP-04-02-010) — as questions, not assignments.

## Changes from v0.7

Wave B of run `APP-V4-DESIGN-PASS-2-20260930` (node B4): design development
under R12-1…R12-3. Item IDs are the survey items of `SURVEY/S1-A.md` §2.8
("AS n") and §3.8 ("RS n"), and the R12 rulings. Every new structure is
PROPOSED unless a cited text decides it.

| Item | Change in v0.8 | Where |
|---|---|---|
| **AS 4**, **RS 6** | Decided: network-destination grants and contacts ride the §6 exchange. Settings-in carries a host agent's destination settings (model service, category switches, named entries, always-off items, in-work grants with scope and state, agent requests with their state), apart from the operation-class grants; record-out carries the R15 entries and the entry read states; the comparison covers destination settings; contacts are read by reference, not compared; declines and refusals are recorded as PROPOSED (R12-10). §6 and RS §8 stay byte-identical | §6 |
| **AS 7** | Transitions for in-work destination grants (DG-1…DG-13: requested → pending → in force → consumed / ended with run / listed → superseded; refused; unconfirmed; declined; unanswered) and failure rows for "destinations not observed", an unreadable record version and a destination report the display cannot match | new §3.1; §5 |
| **AS 5** | "Provided to receivers": for DEL-04-03, DEL-05-01, DEL-05-02, DEL-03-02, DEL-03-03 and DEL-02-03, the elements, the condition of use, and the behaviour on *unconfirmed* and on *missing*. DEP-05-01-025's "grant in force carried on each loop dispatch" is defined | new §12.1; §12 |
| **AS 8** (U-08; OI-014) | The OUT-001 component structure (K-1…K-7) with four PROPOSED options for OI-014 and what each option changes; none is chosen (R12-2) | new §13; UNRESOLVED U-08 |
| R12-1, R12-2 | Settings-in has a PROPOSED representation: JSON Schema 2020-12 `AS_SETTINGS_IN.schema.json`, two valid and three invalid examples; the RS record carries it as a `settings_version` entry | Header; §6; new files |
| R12-3 | `prototype/validate_settings_in.py` validates the examples and walks the §3.1 transitions (eight sequences, six forbidden transitions); run 2026-09-30, all held | `prototype/`; §3.1 |
| R12-5 | A15 named in §0 (not shown by the grant display) | §0 |
| R12-10 | The not-counted marking already reads "prior act not counted" (§4, §8); it gains its reason, as RS-v0.8 L-13 fixes | §4; §8 |
| Verification | New F22 and VC-19…VC-22; VC-15 coverage extended | §11; Verification cases |
| **B5** (S1-A AS 3; node B5, round 2) | Plainly stated: **DEL-04-02 owns the display of the destinations contacted**, new §3.2 (contacts with their allowing entry; declines and refusals shown apart, their recording PROPOSED; outside processes with their limits; "destinations not observed"), because this ScopeOfWork's CLM-002 and register row DEP-04-02-018 consume the contacted-destination record "which DECISION-5 requires to be shown". PANEL ND-4 receives it for a host panel. §12's closing note updated | §3.2; §12; §12.1 |
| **B5** (S1-A AS 7; LOOP-v0.8 §5.3 DF-6) | §3.1 joined to the one destination flow: DG-1 names the request call and the call it carries; DG-13 renamed *unanswered at end* (run ended); new DG-14 (turn cancelled) and DG-15 (not granted: not grantable or prompt not shown); DG-4 names the request state *not granted*. Settings-in request states follow LOOP DF-6 (pending · granted · declined · not granted · unanswered at end), identically in §6 and RS §8; `AS_SETTINGS_IN.schema.json` enum and reason element, and the prototype's walks (ten sequences, eight forbidden transitions) updated. §5 failure rows cite LOOP's DF-F rows | §3.1; §5; §6; schema; `prototype/` |
| **B5** (R12-10) | §3's *Declines* row and DG-11 keep "recording PROPOSED"; §3.2 states it for declines and refusals | §3; §3.1; §3.2 |
| **B5** (verification) | F23 and VC-23 (the contacted-destinations display); VC-19 extended | §11; Verification cases |
| RP-4: V18-1 m-10 | DG-15 starts from no state: a not-grantable or prompt-not-shown request is recorded and closed *not granted* without entering *requested* or *pending*, as LOOP-v0.8 §3.2 and PANEL ND-2 (PS-5) state; the prototype's walk starts it from no state and forbids *requested* → *not granted* for those reasons (eleven walks, nine forbidden transitions; all held) | §3.1; `prototype/validate_settings_in.py` |
| RP-4: V18-1 m-16 | `AS_SETTINGS_IN.schema.json` refuses an always-off item shown on without its A12 reference (§6 = RS §8: "each off unless an A12 turned it on"); new invalid example INV-AS-4; §6 unchanged (still identical to RS §8) | Schema; `AS_SETTINGS_IN.invalid.examples.json`; VC-22 |

## Changes from v0.6

Wave A of run `APP-V4-DESIGN-PASS-2-20260930` (node A1-A): alignment to the
amended basis and the revised ScopeOfWork under R9-1…R9-11. It adds no new
design content. Survey items are those of `SURVEY/S1-A.md` §2.

| R9 ID (survey item) | Change in v0.7 | Where |
|---|---|---|
| **R9-5**, R9-11 (AS 1; S-P1, S-P2, S-P6…S-P10) | Version v0.7. The basis is re-pinned from repo `6e18505e3` and ScopeOfWork `23a28caa…5e21` to the four basis documents by sha256, as amended by SCA-V4-001 and SCA-V4-002, and to ScopeOfWork `f16ffa8a…4460` (SCA-V4-001: TBD-006, AX-004; SCA-V4-002: AX-005). The Basis line names DECISION-4, DECISION-5 and both amendments. A new consumed-input block for v0.7 names R9, R1–R8 by file with R8 at its current sha256, SWBPIPE's answers at `afb6e063…`, `_DAG/_LATEST.md` → DAG-003, and the siblings by Wave A version label only. The earlier consumed-input lines are kept as history. Body citations of the current sibling texts move to the Wave A labels (EXEC-v0.5, WD-v0.7, C-v0.7, RS-v0.7) | Header; §0, §1, §4, §6, §11 |
| **R9-6** (AS 1; the Receivers part of AS 5; S-P11) | The Receivers line is rebuilt from the registers. New **§12**, a table of named receivers only: local rows DEP-04-02-009 and -019…023, and the consumers' rows DEP-04-03-022, DEP-05-01-025, DEP-05-02-019, DEP-03-04-012, DEP-09-06-031 and DEP-09-09-022. One contribution a register names is marked as not yet defined here. U-15 is closed | Header, §12, UNRESOLVED |
| **R9-1** (AS 2; S-P3, S-P4) | S3 quotes V4-HI-42 as amended by SCA-V4-001. The header and OV-4 drop the description of V4-WF-05 by halves and the marker that awaited a basis update. In force in every phase: the act is requested; it is recorded as done only when the person performs it; the reserved acts bind. Phased to the governance layer: holding the run until the act. OV-1 states who requests (INTEGRATION; put to the owner for confirmation) and points to EXEC (Wave B); no display of the request is defined here | Header, §1 S3, §4 OV-1, OV-4 |
| **R9-2** | S13, OV-4 and the §2 constraint bullet restate R8-11 item 2 and R8-12 item 2 against the amended text | §1 S13, §2, §4 OV-4 |
| **R9-3** | "the current phase (Phase 1)" on first use | Header |
| **R9-4** (AS 2; S-P5; survey §2.4 items classed NOW) | S15 cites V4-HOST-02 from the PRD as amended by SCA-V4-001, and its marker that awaited a basis update is removed. The model-destination reading is SETTLED (owner-confirmed: OWNER_ITEMS O-10, DECISION-7 of `APP-V4-BASIS-ALIGN-20260928`). S13's reading of D2 is owner-confirmed (O-25) | Header, §1 S13, S15, §11 F19 |
| **R9-8** (AS 6; survey §2.2 item 1) | §10: the statement that the ScopeOfWork's TBD-001/002 still read OI-001/002 as open is removed; SCA-V4-001 revised them. ScopeOfWork TBD-006 is cited for the phased hold display, and U-16's point of need follows it | Header, §1, §10, UNRESOLVED U-16 |
| **K1-1** (node A3, in place; owner DECISION-K1 of 2026-09-30, `APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md` sha256 35d6546346907137581be7df3bed4a8ccdb4b8bc55a261ca716040d0ad9f91bc) | OV-1: who requests is **SETTLED by DECISION-K1 K1-1** (was INTEGRATION, put to the owner) | §4 OV-1 |
| **K1-2** (node A3, in place) | §4 *Performed* and A12 bullets and the §8 human-acts markings: an earlier act counts in the current phase when it is of the required kind and its content is still current, shown with its time (EXEC SP-6); "prior act not counted" stays for an earlier act on content no longer current or of another kind, or under the governance-phase option (EXEC SP-6F). F16, F17, VC-03, VC-11 recomputed; U-17 closed | §4; §8; §11 F16, F17; UNRESOLVED; Verification cases |
| **K1-3** (node A3, in place) | §4 lapse bullet: after a partial lapse an act on the lapsed referents alone answers together with the earlier act for the unchanged ones (joint answer; EXEC §4.7 JA-1). U-19 closed | §4; UNRESOLVED |
| **K1-5** (node A3, in place) | §3 allow-list rows: a named destination is allowed on its own; a category switch means "allow everything in this category"; with the switch off only the named entries in it are allowed (LOOP N-OPEN-4 closed). U-21's N-OPEN-4 part closed | §3; UNRESOLVED U-21 |
| **R10-1** (node A2, in place; R9-2's second bullet corrected) | §2 constraint bullet, Phase 1: under a direct application no proposal is queued, so the A5 checkpoint (reached-when *proposal queued*) is **not reached**; nothing is requested by reason of an arrival that did not occur, no A5 is forced and none is recorded. A checkpoint the run does reach under such a grant has its act requested and is *waiting* until the person performs it. "The checkpoint's act is still requested" is withdrawn for the direct-application case | §2 |
| **R11-3** (node A4, in place; V17-A M-1) | Header: a new line pins this run's records at their final bytes: R9 `a64e2415…`, R10 `ad3b6caa…`, R11 `e7343b66…`, OWNER_DECISIONS `7458e9e8…`. The node A1 input line and the K1 rows keep the bytes read then | Header |

## Changes from v0.5

Keyed by R8 ID; sources are I2 rows of INTAKE_MAP.md (`nn.k`, `P2.n`, Part 2.2
AS rows, Part 3 items, Part 4 sections). R8 overrides I2 where they differ.
SETTLED means by DECISION-3 or DECISION-4. The owner files EXEC-v0.4 and
WD-v0.6 were revised first; this file follows them.

| R8 ID (source) | Change in v0.6 | Where |
|---|---|---|
| **R8-1** (DECISION-4 D4-1; SETTLED, framing INTEGRATION) | §4 gains a **Phase-1 overlay** (OV-1…OV-7): checkpoints shown as plan guidance; arrivals and acts shown as observation, with dispositions as record labels; no hold, hold-support value or *unsupported* for a hold reason shown; acts shown only when the person performed them; reserved acts stand; the optional "continued past ‹checkpoint› before ‹act›" replaces *action during hold*; lapse still shown, no re-hold; `governed` shown as guidance only. The §1 D6 paragraph is restated for both phases | Header, §1, §4 |
| **R8-1** (governance phase retained) | §4's hold-support bullet, *action during hold* bullet and the re-hold part of the lapse bullet are relabelled **governance phase (retained)**, each with its Phase-1 statement beside it. §2's carriage assurance and §8's *action during hold* facet likewise. Nothing is deleted | §2, §4, §8 |
| **R8-1** (V4-WF-05; S3; cases) | S3 and S13 annotated (V4-WF-05's first half phased, not withdrawn). Two-part form (Phase-1 result; governance-phase value) for **F6, F6b, F6c, F6d, F14, F18** and its variant; VC-03, VC-10, VC-16 updated; new **F20** and **VC-17** (Phase-1 semantics) | §1, §11, Verification cases |
| **R8-2** (I2 R8-Q1, R8-Q-HS4; P2.1, P2.4, P2.8, P2.16, P2.17; §2.2 AS rows) | SQ-02's answer is the **governance-phase input**. Governance-phase values: **F6d → not enforceable → requirement check *unsupported*** (was *not established*); **F14** `CP-grant` via X → *not enforceable* (was *not established*); **F18 variant** `CP-accept` → *not enforceable*. §4's *not established* value notes that neither cause now applies against SWBPIPE (overriding I2 P2.16's note), and the HS-3 sentence records "SWBPIPE: answered with none, 2026-09-28". **D6 is closed for Phase 1** (§1, §10, U-16) | §1, §4, §10, §11, UNRESOLVED |
| **R8-3** (I2 R8-Q2; Part 3 item 2) | §8 route-and-outcome facet: *refused — stale* shows the host's stated scope (SWBPIPE: "host scope: whole model"; failing targets *not supplied*), never narrowed; per item where the host supplies subject identities | §8 |
| **R8-4** (I2 R8-Q3; Part 3 item 3) | §8 human-acts facet: a whole-model identity received as every covered subject's identity lapses acts on any model change (over-lapse, never under); never App-computed | §8 |
| **R8-5** (I2 R8-Q-item-1, R8-Q10, R8-Q13, R8-Q15; 10.5, 23.2; Part 4.9) | §7: SWBPIPE's session undo writes no receipt, so "applied, then reversed by ⟨receipt⟩" is *not supplied* there (F7 annotated). §8: received host terms (`unsupported_method`/`unsupported_change` → *not exposed on this surface*; #885 `withdrawn` → item left, "cleared by the person, no decision record"; `validation_rejected` → *refused — invalid*; never A10/A11); accept and apply are one step on SWBPIPE, so the accepted-then-stale display has no SWBPIPE counterpart; SWBPIPE's lapse and stale displays (SQ-23) noted | §7, §8, §11 F7 |
| **R8-6** (SQ-13, SQ-28) | §2: A13 stays reserved; SWBPIPE has no enablement facility, so its channel stays *not enabled*; the grant display is unaffected (the channel status is DEL-03-03's) | §2 |
| R8-7 (X.5; 01.8, 05.3; Part 4.11) | Standings move to **answered**: header, S13 (SQ-05), §2 constraint (SQ-02). U-04, U-06, U-07, U-12 and U-16 owners and effects updated (SWBPIPE owner decisions PB-TBD-002 / DEL-16-03 and OI-016; SQ-05 (d), (h)). This file cites no OI-003 | Header, §1, §2, UNRESOLVED |
| R8-10 (I2 R8-Q12, R8-Q16) | §2: the agent never adds a field the host schema lacks. §3: new **grant display for a host without grants**, "host fixed treatment: every change waits for the person's Apply (host-stated)", PROPOSED and deferrable (new U-20) | §2, §3, UNRESOLVED |
| **R8-11** (A1 residuals) | Item 1: lapse shown in Phase 1 and dispositions as record labels (OV-2, OV-5). Item 2: S13's reserved-act half binds in Phase 1; its "or declared checkpoint" half is guidance in Phase 1 (S13; OV-4). Item 3: an invalid declaration is a declaration finding in Phase 1; F18's harness-capability reference keeps the check *not established* for a required-tool reason. Item 5: governance-phase values read the fixture's checkpoints as if governed (§11 lead) | §1, §4, §11 |
| (R8-9, noted) | S15: V4-HOST-02's retention is pending owner clarification (R8-9). No rule of this file changes | §1 S15 |
| **R8-12** (items 1, 7; closing pass, node A6, in place) | Item 1: OV-5 and the §4 lapse bullet add the Phase-1 label **"act lapsed at ‹t›"** for a lapse after the resume point (nothing says *waiting*; nothing re-held). Item 7: consumed inputs list the post-R8 sibling versions; §0 and §11 fixture sources note that C-v0.6 carries the C-v0.4/C-v0.5 fixture | Header, §0, §4 OV-5, §4 lapse bullet, §11 |
| **R8-13** (DECISION-5; SETTLED; the act mapping INTEGRATION; in place, no version bump) | §3 gains **network-destination grants**. The grant display shows the host agent's allow list (category switches and the named entries within each; the model service "allowed by your model choice"; the always-off items) and the in-work grants with their scopes (once, this run, always). An agent's request is shown only as a request, and a decline is never a grant. These are never merged with operation-class grants or the checkpoint indicator. §2 notes the subclass (ACT §2.7). **S15**: the V4-HOST-02 "pending owner clarification (R8-9)" marker is replaced by the revised V4-HOST-02 (DECISION-5; flagged for the next accepted-basis update). New F21, U-21 and VC-18; VC-15 coverage extended | Header, §1 S15, §2, §3, §11, UNRESOLVED, Verification cases |
| R8-13 close — in place | The owner confirmed DECISION-5 (the reading of "MCP V2"; the person-only grant stands), so the "open to the owner's correction" markers are closed. The consumed-input line is corrected: OWNER_DECISIONS.md is cited in its state that adds that confirmation, not at `1528a5033` |
| V10 S-1…S-4 — in place | The wording of the DECISION-5 confirmation is made precise (the "MCP V2" reading was confirmed; the person-only grant was not objected to and stands). The revised V4-HOST-02 is "the recorder's wording confirmed by the owner". The always-off item reads "a silent switch". ACT F-22 is updated. No rule changes |

## Changes from v0.4

The v0.3 → v0.4 change table is preserved in AS-v0.4 at commit `cc58211c5`.

| Item | Change in v0.5 |
|---|---|
| R5-1 (V3-A MAJOR-1) | §4 hold support uses the four ruled values (**enforced by the host loop** · **enforced on the host route** · **not established** · **not enforceable**) with their requirement-check consequence; retired values removed. F6 and F18 re-valued |
| R5-2 (V3-B MAJOR-1) | §2/§7: **App-assured carriage is not available in this increment**; only host-held satisfies R2-12; a constraint the host merely received keeps its source's assurance |
| R5-3 | §4 grant-setting subject: the **declared** setting content always binds; an A8 may present it but never changes it |
| R5-4 (V3-A m-11) | S15 split: "may flow; no gating" SETTLED by DECISION-2; "record per turn and show in the channel status" **INTEGRATION (DECISION-2 reading)**. F19 mentions per-turn destinations and re-routes (shown by DEL-03-03, recorded in RS R5) |
| R5-5 (Y-4) | §4 lapse: re-hold whatever caused the lapse, including the person's own undo; the person's undo is never shown as action during hold; an undo never re-holds an A5 arrival. "Run stops at its next action" conditioned on enforced hold support |
| R5-6 (Y-5) | §9 DS-6: an operation performing a reserved act shows the human-act record it produced |
| R5-7 (V3-A MAJOR-3/MAJOR-5) | F14/F15 (L-AS-7/8) re-pointed to **V-GR1** (per R5-7; C adds it); T15 before a CP-grant arrival does not count. F16 re-pointed to a V-GR1 run end (L-AS-9 kept, reason stated) |
| R5-9 (V3-A m-2, m-3, m-4, m-12) | Citations at current sibling versions (commit 8fb51f07f); FXA-n; stale "C declares only V-CP1" reasons replaced (C FXA-5 declares CP-accept and CP-check); unsupported reason aligned to the R4-8 string "checkpoint hold not enforceable on this surface: ‹name›" |
| R6-1 (in place; V4-A MAJOR-1) | §4 hold support classified by **held actions**: all host operations → HS-3 by SQ-02 status; any App-side held action → **not enforceable** in App runs. F6c classified (holds App agent turns → not enforceable); new F6d (held actions host operations only → not established while SQ-02 is unanswered) |
| R6-2 (in place; V4-A MAJOR-4, m-10) | F18 variant corrected: E1 on X has `CP-accept` *not established* and `CP-check` *not enforceable* → workflow **unsupported**; VC-03 corrected |
| R6-3 (in place; V4-A m-4) | §4: "run stops" only under *enforced by the host loop*; under *enforced on the host route* the host refuses the held host operations and other actions are *action during hold*; otherwise nothing is stopped |
| R6-4 / V4-A m-1 (in place) | Stale markers removed: V-GR1 cited from C-v0.5 (run 13; GR-1…GR-3, GR-P/GR-R/GR-S); header cites C-v0.5 and EXEC-v0.3; `CP-grant` via X *not established* (R6-2) |
| R6-5 (in place) | §4 *action during hold* shows the turn initiator (person-directed · agent · App rule) as recorded in RS R11 |
| R7 carried observation (in place; V5 §6) | F6d adds a one-line cross-reference to its DEL-04-01 counterpart ACT `CP-L4` (L-ACT-4, §4.6). No value changes |

## 0. Reading this definition

- Element and state names are **semantic, not wire names**. No field
  spelling, type, transport, persistence, placement, layout or timing
  threshold is selected (SoW REQ-006; OI-013; OI-014).
- **Act names (DEL-04-01 §2.1):** A1 propose · A2 apply · A3 examine · A4 mark
  checked · A5 accept · A6 approve · A7 rely · A8 request · A9 record · A10
  reject · A11 withdraw · A12 set grant · A13 enable external access · A14
  answer tool permission · A15 register workflow revision (R12-5; not shown
  by the grant display).
- **Labels (R-4):** unqualified "checked" means only A4; host results say
  "host checks passed: ‹named checks›"; agent work is "examination" /
  "findings"; "approval" means only A6; "tool permission" is A14; "accept" is
  A5 only.
- **Class values (R2-1):** none · may apply within granted autonomy · proposal
  only · reserved to the person (SETTLED, V4-HI-02) · **no policy basis** with
  reason ∈ {omitted, unassigned, pending OI-021} (INTEGRATION).
- **Grant value** (direct / propose) is what the person sets; **treatment** is
  what the host route resolves.
- Examples are **fixture subjects** from DEL-03-01/C-v0.4 §10 (FX-PIPE-01), carried in C-v0.7 §10.

## 1. Settled distinctions relied on

| # | Settled distinction | Citation |
|---|---|---|
| S1 | The person sets, per class of operation, direct application or proposal within a scope the person sets; visible, changeable during work, recorded with each run | V4-HI-40; V4-AUT-01 |
| S2 | Conservative defaults for consequential operations; SWB model changes default to proposal with row / multi-row / whole-batch acceptance; the person may widen | V4-HI-41 |
| S3 | "Autonomy does not override a workflow's declared checkpoints: whatever the autonomy setting, a checkpoint's required act is requested and recorded as done only when the person performs it. Holding the run at the checkpoint until then is phased to the governance layer (V4-WF-05): in the current phase a checkpoint is plan guidance that the person and the agents manage, and the reserved acts (V4-HI-30) still bind." **In force in every phase (R9-1):** the act is requested; it is recorded as done only when the person performs it; the reserved acts bind. **Phased to the governance layer:** holding the run until the act, which belongs to governed checkpoints in the governance phase | V4-HI-42 and V4-WF-05, as amended by SCA-V4-001; DECISION-4 D4-1 |
| S4 | Direct application is marked with origin, can be undone and checked later | V4-HI-22; V4-AUT-01 |
| S5 | `success` means it ran; a proposal is "queued" until the host records acceptance and application | V4-HI-25 |
| S6 | Results carry standing — current/historical, checks passed, known limitations — never presented with more confidence than the host gives | V4-HI-12; V4-AUT-02 |
| S7 | A human act binds to content and lapses visibly when it changes | V4-HI-32 |
| S8 | "accept", never "approve", for proposals | V4-HI-33 |
| S9 | No fabricated human act; faithful recording of a performed act is permitted | V4-HI-31; d3 |
| S10 | Acts are distinct; no acceptance-first chain | d3; V4-AUT-03 |
| S11 | Nothing agent-produced is shown as certified, sealed, approved or code-compliant | V4-AUT-05 |
| S12 | Every request answered or explicitly declined; silence never implies approval; unobserved outcomes are unknown | V4-EXE-02/03 |
| S13 | Reserved to the person: A4; A5 wherever autonomy requires a proposal; A6; A7; changing the grant (A12); enabling external access (A13). No grant widens past a reserved act or declared checkpoint. The host names and enforces its own list; SWBPIPE adoption is not shown. **Current phase (R8-11 item 2, restated by R9-2; the reading of D2 was confirmed by the owner: OWNER_ITEMS O-25, DECISION-7 of `APP-V4-BASIS-ALIGN-20260928`):** "no grant widens past a reserved act" binds, and the host enforces it through its operations. For a declared checkpoint, V4-HI-42's request clause and record clause are in force whatever the autonomy setting; whether the run goes on before the act is for the person and the agents, and the host's own treatment of its operations decides what the host does. Holding the run binds only for governed checkpoints in the governance phase. SWBPIPE answered SQ-05 (2026-09-28): no class system, no grants, no named reserved list; every change waits for the person's Apply; its autonomy is SWBPIPE owner decision OI-016 (an answer, not adoption) | OWNER_DECISIONS D2; V4-HI-30; DEP-001; R8-11; R9-2 |
| S14 | App routine tool-permission/sandbox modes are the user's own Codex setting per project/turn and govern tool execution only; hosts have no classifier permission mode in the first increment; the SWB default proposal mode applies | OWNER_DECISIONS D3 |
| S15 | Host content read over the external channel may flow to the App conversation's selected model, cloud included; the App does not gate on the destination. A host may restrict its own channel. PRD V4-HOST-02, as amended by SCA-V4-001 (which applies DECISION-5; R8-13), governs the host's embedded agent: "A host's agent sends data only to the model service the person selected and to destinations the person has allowed — in advance in an allow list (by category, such as web access, MCP servers or other APIs, or by named destination) or when the agent asks during its work. Nothing else is contacted: no analytics, silent provider switch or background download unless the person turns it on. Every destination contacted is recorded and shown (D-18; DEC-5)." (That the destination of an App run is recorded per turn (RS R5) and shown in DEL-03-03's channel status is **SETTLED**: the owner confirmed the reading, OWNER_ITEMS O-10, accepted at DECISION-7 of `APP-V4-BASIS-ALIGN-20260928`; R4-1/R5-4; R9-4) | OWNER_DECISIONS DECISION-2 D5; R5-4; PRD V4-HOST-02 (SCA-V4-001; DECISION-5); OWNER_ITEMS O-10 (DECISION-7) |

**Phase 1 (R8-1; DECISION-4 D4-1; ScopeOfWork TBD-006).** Declared checkpoints are plan guidance
(EXEC-v0.5 §2.1; WD-v0.7 §4.3.0). The display shows no hold, no hold-support
value and no *unsupported* for a hold reason, and it never shows an App or
host-loop hold (§4 OV-1…OV-7). App-side run holds, `UNRESOLVED{D6}`, are
**closed for Phase 1** by DECISION-4 and re-open when the governance phase is
taken up (R8-2).

**Governance phase (retained).** For checkpoints declared `governed`, the
display shows hold support (the four R5-1 values) and action during hold,
and never shows an App hold as enforced when it was not (R4-2). SQ-02 decides
holds only for checkpoints on host operations; App-only checkpoints stay
**not enforceable** whatever it answers (R5-10). SWBPIPE answered SQ-02 on
2026-09-28 with no host-held route (route (iv), none planned), so its
host-operation checkpoints are *not enforceable* too (R8-2).

## 2. Grant model received

Received from DEL-04-01 §5 and §8; this deliverable renders and exchanges it.

- **Grant** (semantic): for each operation class *k*, a **grant value**
  ∈ {direct, propose} within a **scope** *σ* (dimensions: model/workspace,
  object set, run, period, consequence — representation-neutral; R-8), set by
  the person through **A12**. The consequence vocabulary is open (U-02).
- **Governs host operations only.** Routine tool permission (A14) is the App
  user's own Codex setting (S14), never shown as a grant or an act; recorded
  only in RS R13. Hosts have none.
- **Not gated by model destination (R4-1).** Neither the grant display nor
  external-access enablement (A13) is gated by, or derives any permission
  from, where the App conversation's model runs. The destination is recorded
  (RS R5) and shown in DEL-03-03's channel status, not here.
- **Reserved.** ADOPTED by D2: A4, A5 (where autonomy requires a proposal),
  A6, A7, A12, enabling external access. DERIVED: A10 wherever A5 is; any
  operation that performs A4, A5, A6, A7, A10, A12 or A13 (R2-2). INTEGRATION:
  disabling external access is also a person's A13 (R2-3). No grant widens
  past these. Reserved entries are always offered to the agent; a call
  returns *not permitted* with an A8 **offered** (R2-4). The reserved acts
  stand in both phases (R8-1; DECISION-4). On SWBPIPE a request for Apply is
  refused `unsupported_method`, received as host-reported *not exposed on
  this surface* (R8-5; R2-4 not met by that host). A13 stays reserved;
  SWBPIPE has no enablement facility, so its channel stays *not enabled*
  (SQ-28; R8-6). The channel state is shown by DEL-03-03, not by the grant
  display.
- **Network-destination grants (R8-13; ACT §2.7).** A host's agent reaches
  a destination other than its model service only under the person's
  allow list or an in-work grant (LOOP §5.1.1). Each is an A12, subclass
  network-destination grant: person-only, never performed by an agent. It
  widens no operation class, and an operation-class grant allows no
  destination. The App's own Codex is not governed by it (HOSTING §2).
- **Model-change class** (DEL-04-01 P-03): *may apply within granted
  autonomy* (DERIVED from V4-HI-41), default *propose*, acceptance by row /
  multi-row / whole batch with the change item as unit.
- **No policy basis** (INTEGRATION; R2-9): proposing stays available but
  confers no permission; direct is *not permitted*; an A12 widening the class
  is **refused (reason: no policy basis)**. Shown "no policy basis — held
  (reason)"; fixtures report **held**.
- **Treatment resolution** is on the host route at validation and again at
  application. A direct request without an *effective* direct grant value is
  *not permitted*; never converted into a proposal.
- **Governing checkpoint constraint** (R2-12; R4-14). **Phase 1 (R8-11 item
  2 and R8-12 item 2, restated by R9-2; R8-10):** an A5 checkpoint is plan
  guidance; the agent proposes, the
  host's own treatment decides, no constraint is carried or enforced by the
  App, and the agent never adds a field the host schema lacks. Where the
  active grant lets the host apply directly, no proposal is queued, so the
  A5 checkpoint (reached-when *proposal queued*) is **not reached**: nothing
  is requested by reason of an arrival that did not occur, no A5 is forced,
  and none is recorded; the record shows the direct application under the
  person's grant. A checkpoint the run does reach under such a grant has its
  act requested and is *waiting* until the person performs it (R9-2 as
  corrected by R10-1). The display
  shows no constraint and no *not permitted* on its account. **Governance
  phase (retained), governed checkpoints:** if a declared
  checkpoint requires A5 on an operation's result, the dispatch carries
  {workflow run, checkpoint name, A5, operation} with a **carriage assurance**
  (host-held · model-supplied · absent; **App-assured is not available in this
  increment**, R5-2); a direct request under it is *not permitted* naming the
  constraint. Only **host-held** carriage — the host derived the constraint
  from its own resolved declaration copy or verified a received one against
  it, including the host loop's own evaluation — satisfies R2-12; a constraint
  the host merely received keeps its source's assurance. The display shows the constraint, its cause and its
  carriage assurance. Host receipt is a relay question (U-12). SWBPIPE
  answered SQ-02 on 2026-09-28: no receipt and no host copy (route (iv));
  its strict preflight would refuse a constraint field as unknown (SQ-02
  (a)). SWBPIPE's "every change waits for Apply" is not host-held carriage.

## 3. Grant display states

Per class and scope. Display is derived; the control (App or host) is the
authority for the current grant; the run record for what was recorded.

| State (R-8; R2-6) | Entry evidence | Shown as | Direct branch? |
|---|---|---|---|
| **effective (person-set)** | A12 record of the person's setting **and** control confirmation (control effect *established*) | Grant value and scope, "set by you" | Yes, if grant value is direct |
| **effective (policy default)** | Policy-class record with a default value; no A12; no setting actor, no requester | Default value, "policy default (‹record›)" | Only if the record's default is *direct* — none in the first increment |
| **requested by agent** | Agent A8 request; no person act | "Agent requests ‹value, σ›" beside the governing state | No |
| **set by person, not yet confirmed by control** | A12 record; control effect *pending* | "Set by you — not yet in force" | No — prior state governs |
| **unconfirmed** | Last-known value without current confirmation | Last-known value, "unconfirmed" | No |
| **not set** | No person setting and no policy default | "not set" | No |
| **refused (reason)** | A12 record; control effect *refused* (e.g. "no policy basis") | Reason beside the still-governing state | No |

Transitions: agent A8 → *requested by agent* (governing state unchanged).
Person A12 → *set by person, not yet confirmed* → confirm → *effective
(person-set)*; refuse → *refused (reason)*, prior state still governs; no
answer → remains pending, never promoted (S12). Any state → loss of
confirmation → *unconfirmed*. A later A12 on overlapping classes and scope
**supersedes** the earlier one **only when established**; a refused A12
supersedes nothing (R4-6). An operation result never moves a class to
*effective* or widens it (REQ-001).

**Host without a grant model (R8-10; PROPOSED; deferrable with the host
joins).** SWBPIPE has no classes and no grant states (SQ-05 (a), (e)). For
such a host the display shows **"host fixed treatment: every change waits for
the person's Apply (host-stated)"** as the host's statement. It never shows a
grant state, never "not set", and never *effective (policy default)*, which
needs a policy-class record (R2-6). The App's own classes and grants for that
host's operations are App/shared meaning and are not shown as the host's
(U-20).

**Network-destination grants (R8-13; DECISION-5; PROPOSED display over
SETTLED rules).** For a host whose agent contacts network destinations,
the grant display also shows the following, from the host's control
(LOOP §5.1.1; PANEL §3.8 ND-5):

| Part | Shown as |
|---|---|
| Allow list: category switches | Each category (web access, MCP servers, other APIs, …) on or off, "set by you", with its A12 reference. On means "allow everything in this category" (SETTLED by DECISION-K1 K1-5) |
| Allow list: named entries | Each named destination within its category, with its source: "allow list", or "in-work, always, ‹time›". A named entry is allowed on its own: with its category switched off, only the named entries in it are allowed (SETTLED by DECISION-K1 K1-5; LOOP N-OPEN-4 closed) |
| Model service | "Allowed by your model choice" (the selected model service and, for a chosen cloud model, its sign-in service). Not a list entry |
| Always-off items | Analytics or usage reporting; a silent switch to another model or provider; background downloads or updates. Shown off unless the person turned one on |
| In-work grants | Each grant with its scope: **once** (against its one request, until used), **this run** (with the run, until it ends) or **always** (also listed as an entry). For the destination or its category, with time and A12 reference |
| Agent requests | "Agent requests ‹destination or category, scope›" (A8), beside the governing list. Never a grant |
| Declines | Not shown as a grant state. The requesting call's outcome is "destination not allowed by the person" (PANEL ND-3). Shown with the destinations contacted, apart from contacts (§3.2); recording it as a destination entry is PROPOSED (R12-10) |

- The seven states above (*set by person, not yet confirmed by control*,
  *unconfirmed*, *refused (reason)*, and so on) apply to these grants too;
  the in-work transitions are §3.1.
  A refusal may carry the reason "not stateless MCP (2026-07-28)".
- The destination grants and the operation-class grants are shown apart.
  They never merge, with each other or with the checkpoint indicator,
  into a single "allowed" signal.
- Allow lists locked by an organization are governance phase and are not
  shown in Phase 1.

### 3.1 In-work destination grants: transitions (AS 7; PROPOSED display over SETTLED rules)

The rules are LOOP §5.1.1 (NW-11…NW-13) and ACT §2.7 (ND-A2), SETTLED by
DECISION-5 except the A12 mapping (INTEGRATION, ACT F-22). The flow these
states follow, and the request states *pending · granted · declined · not
granted · unanswered at end*, are DEL-05-01/LOOP-v0.8 §5.3 DF-5 and DF-6
(node B5): a request is *granted* once its grant is **in force** (DG-3). The table says
what the display shows and what settings-in carries at each step (§6). A
network-destination grant is never shown merged with an operation-class
grant or the checkpoint indicator.

| # | From | Event (evidence) | To | Shown as | Settings-in / record |
|---|---|---|---|---|---|
| DG-1 | — | The agent asks for a destination or category, with the scope it seeks (A8: a call to the host's destination request entry, carrying the call it needs (the carried call), LOOP-v0.8 §5.3 DF-1; LOOP "Destination request issued") | **requested** | "Agent requests ‹target, scope›" beside the governing list; only the requesting call is shown waiting (NW-12) | Agent request, state *pending*; R15 *destination requested* |
| DG-2 | requested | The person grants, once, for this run or always (A12, network-destination grant, captured by the host's control) | **pending control confirmation** | "Set by you — not yet in force" | In-work grant, state *pending control confirmation*, A12 reference; the A12 record |
| DG-3 | pending; unconfirmed | The control establishes it | **in force** | The grant with its scope, time and A12 reference, "set by you" | State *in force*; R15 *destination grant* |
| DG-4 | pending | The control refuses (e.g. "not stateless MCP (2026-07-28)") | **refused (reason)** | The reason beside the governing list; nothing is allowed | State *refused*, with the reason; the request *not granted* ("grant refused by control", LOOP DF-6); a boundary refusal, if the host records one, is PROPOSED recording (R12-10) |
| DG-5 | pending; in force | Confirmation is lost | **unconfirmed** | Last-known value, "unconfirmed"; never shown in force | State *unconfirmed* |
| DG-6 | in force (*once*) | The one requesting call contacts the destination | **consumed** | Gone from the in-work grants; the contact is shown where contacts are shown (PANEL ND-4), "in-work grant: once" | State *consumed*, with the contact; R15 *destination contacted* |
| DG-7 | in force (*once*) | The requesting call is withdrawn before it is sent | **consumed** (unused) | Gone; never reusable by another call (ND-A2) | State *consumed* |
| DG-8 | in force (*once* or *this run*) | The run ends | **ended with run** | Gone; a run that continues this one inherits nothing (R4-4) | State *ended with run* |
| DG-9 | in force (*always*) | It becomes an allow-list entry | **listed** | A named entry "in-work, always, ‹time›" in the allow list | Named entry with source *in-work, always* |
| DG-10 | listed | A later **established** list edit removes or narrows it | **superseded** | "superseded by ‹act›"; a refused edit supersedes nothing | Named entry changed; state *superseded* |
| DG-11 | requested | The person declines | no grant | Not shown as a grant; the call's outcome "destination not allowed by the person" (PANEL ND-3) | Agent request, state *declined*; the act-declined event (INTEGRATION, R2-5, R8-13); its R15 record PROPOSED (R12-10) |
| DG-12 | requested | Nobody answers | requested (unchanged) | Still pending; never granted by silence or timeout (S12) | State *pending* |
| DG-13 | requested | The run ends unanswered | no grant | Gone; the requesting call shown not sent (PANEL FD-4) | Agent request, state *unanswered at end* (cause run ended); RS `destination_request_closed` (PROPOSED) |
| DG-14 (B5) | requested | The person cancels the turn in which it was asked (LOOP F-11) | no grant | Gone | Agent request, state *unanswered at end* (cause turn cancelled); RS `destination_request_closed` |
| DG-15 (B5; RP-4) | — (no *requested* state is entered: LOOP-v0.8 §3.2) | The agent asks for a target that cannot be granted (a non-stateless MCP server; an always-off item, which only an allow-list edit turns on), or the host's control cannot show the prompt (LOOP DF-3 A-2, A-3; DF-F4) | no grant | "cannot be allowed: ‹reason›" beside the governing list (PANEL PS-5, with no PS-1 before it) | Agent request, state *not granted* (reason not grantable · prompt not shown), never *pending*; RS `destination_requested` and `destination_request_closed` |

Not transitions: an agent-written list entry is never a grant (at most an
A8, DG-1); an operation-class A12 changes no destination state (ACT ND-A1).
The walk of these transitions is checked by
`prototype/validate_settings_in.py` (ten event sequences, eight forbidden
transitions after node B5; eleven and nine after RP-4, which starts DG-15
from no state and forbids *requested* → *not granted* "not grantable or
prompt not shown"; run 2026-09-30, all held).

### 3.2 Destinations contacted: the display (v0.8, node B5; S1-A AS 3; PROPOSED display over SETTLED rules)

**Owner.** This file owns the display of the destinations a host's agent
contacted. DEL-04-02's ScopeOfWork CLM-002 says this deliverable "consumes,
from App v4 `DEL-05-01`, a host agent's network-destination allow list,
in-work destination grants and contacted-destination record, which
`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5` requires to be shown"
(register row DEP-04-02-018). DEL-05-02's ScopeOfWork names no destination
surface (PANEL F-12), so PANEL §3.8 ND-4 **receives** this display for a
host panel, as ND-5 receives §3. The rule "every destination contacted is
recorded and shown" is SETTLED (V4-HOST-02, V4-ARC-12, V4-HI-70 as
amended); the display below is PROPOSED. The flow and the record are
DEL-05-01/LOOP-v0.8 §5.3 and RS R15; this file reads them from record-out
(§6), by reference, and compares nothing about contacts.

| Part | Shown as | From (RS R15 / R11) |
|---|---|---|
| Each destination contacted | Destination; category; the allowing entry: "model choice" (with class local or cloud), "category: ‹c›", "named entry", or "in-work grant: once / this run / always, ‹time›"; time. In any model mode | `destination_contacted` |
| Declines | Apart from contacts: the requested destination, "destination not allowed by the person", time; never as a contact or a grant. Recording PROPOSED (R12-10) | `destination_declined` |
| Refusals | Apart from contacts: destination, reason (not allowed · always-off item · not stateless MCP (2026-07-28)) and stage (model request · V-D · at contact); recording PROPOSED (R12-10) | `boundary_refusal` |
| Requests that ended without a grant | The request with its state *not granted* (reason) or *unanswered at end* (cause) and "not sent" | `destination_request_closed` |
| Outside processes | The process; its declared destinations; "process network not observed" when not sandboxed; for an MCP server, "stateless revision declared, not verified". Never implies the process contacted only what it declared | `outside_process`; R11 |
| No native report | "destinations not observed", never "no destinations contacted" (§5) | R11 |

- Contacts, declines and refusals are never merged into one "allowed"
  signal, and never with the grant display (§3) or the checkpoint
  indicator.
- An App run shows none of this: its model destination is R5, shown in
  DEL-03-03's channel status (§2; §10).
- A contact that names an in-work grant the record lacks is a defect
  observation (§5), shown with the contact.


## 4. Checkpoint overlay

Display meanings of the DEL-02-03 hold machine (EXEC §4), consumed from the
record (RS R8).

**Phase 1 (R8-1; EXEC-v0.5 §2.1; WD-v0.7 §4.3.0).** The overlay shows
checkpoints as plan guidance and records as observation:

| # | Display rule (Phase 1, this increment) |
|---|---|
| **OV-1 Guidance** | A declared checkpoint is shown with its required act, subject, purpose and held actions, as the plan's expected pause. The person and the agent plan around it; the agents manage any pause themselves (EXEC PH-1). The agent carrying out the workflow asks the person for the act when its work reaches the checkpoint; the display issues no request in the agent's place (R9-1; SETTLED by DECISION-K1 K1-1). How an App run observes an arrival and a request, and what the record then holds, is defined in EXEC in Wave B; no display of that request is defined here |
| **OV-2 Record labels** | Arrivals, acts, act-declined, act-lapsed, run-resumed and run-ended events are shown as recorded. The dispositions below label the record: *waiting* means "reached; act not yet recorded", never "the run is held" (EXEC PH-6; R8-11 item 1) |
| **OV-3 No hold shown** | No hold, stop, block or re-hold is shown, for the App or a host's embedded loop. No hold-support value is shown, and no workflow is shown *unsupported* for a hold reason; the requirement check shown depends on required tools and channel state (EXEC PH-2, PH-3) |
| **OV-4 Acts as performed; reserved acts stand** | An act is shown only from a record of the person performing it, with capture evidence (V4-WF-05: "the run does not record the act as done until the person performs it"; V4-HI-42; EXEC PH-4). Reserved acts stay the person's, and a host's refusal of an agent's attempt is shown as observed (EXEC PH-5). "No grant widens past a reserved act" binds. For a declared checkpoint, V4-HI-42's request clause and record clause are in force whatever the autonomy setting, and whether the run goes on before the act is for the person and the agents (S13; R9-2). The grant display and the checkpoint indicator never merge |
| **OV-5 Lapse shown, no re-hold** | A performed act's lapse is shown (act-lapsed event; gated outputs show standing lapsed). After the resume point it reads **"act lapsed at ‹t›"**: nothing says *waiting*, and a new act is shown when performed (R8-12 item 1). No re-held annotation is shown (EXEC PH-8; R8-11 item 1) |
| **OV-6 Continued past** | A run action after an arrival and before its act may be shown with the optional plain annotation **"continued past ‹checkpoint› before ‹act›"**, with its turn initiator. It is information, never a warning, defect or refusal (EXEC PH-7). The person's own operations never carry it |
| **OV-7 `governed` and invalid declarations** | A checkpoint declared **`governed`** (WD-v0.7 §4.3.1; PROPOSED) shows the flag and is otherwise treated as guidance (EXEC PH-9). An invalid declaration is shown as a declaration finding (invalid, with its FB code), with no hold-support value (R8-11 item 3) |

The bullets below keep the full overlay. Where a bullet is marked
**governance phase (retained)**, it applies to governed checkpoints in a
later layer and is not shown in Phase 1.

- **Disposition** per current arrival (never a seventh value): **not
  reached** · **waiting** · **performed** (act ⟨ref⟩, performance ordinal) ·
  **resolved negatively** (A10, or an act-declined event for A4, A6, A7 or
  A12) · **lapsed** (only for an arrival whose run has ended) · **unknown**.
  Arrivals of the same checkpoint are shown with their **arrival ordinal**;
  earlier arrivals remain history.
- **Subject class**, shown as its own element independent of reached-when
  (R2-17; R3-1): change items of a named proposal · named output · **objects
  a named output concerns** · objects changed by a named outcome · targets of
  the held call (kind (a) only) · grant setting. An A5 checkpoint uses
  reached-when *proposal queued*; its subject is that proposal's change items.
  For a grant-setting subject the **declared** setting content always binds
  (a declaration naming none is invalid); an A8 may present that content but
  never changes the subject; a run-dependent scope is a declared binding rule
  resolved at arrival, never chosen by an A8 (R5-3).
- **Hold support — governance phase (retained), governed checkpoints only**
  (Phase 1: not shown, OV-3). On the acting surface, exactly one of the four
  R5-1 values (owner EXEC §3.6):
  - **enforced by the host loop** (embedded route; holds subject to host
    evidence, DEP-001; SWBPIPE has no host loop, SQ-20) — requirement check
    passes;
  - **enforced on the host route** (host-held constraint, evidenced by the
    SQ-02 answer and a candidate; not offered by SWBPIPE) — passes;
  - **not established** (awaiting a host answer such as SQ-02, or unagreed
    exposure; SWBPIPE has answered SQ-02 and SQ-11, so against SWBPIPE
    neither cause now gives this value, R8-2) — the check shows *not
    established*, never a pass and never *unsupported*;
  - **not enforceable** (no mechanism on this surface) — the workflow is shown
    *unsupported* ("checkpoint hold not enforceable on this surface: ‹name›",
    R4-8).

  The value is classified by what the checkpoint must **hold** (R6-1): if
  every held action is a host operation, the value follows SQ-02 (answered
  with host-held carriage evidenced → *enforced on the host route*;
  unanswered → *not established*; answered with no host-held route → *not
  enforceable* — SWBPIPE: answered with none, 2026-09-28); if any held action is App-side (an App agent turn, App tool
  or harness action, App file write or return step), an App run shows *not
  enforceable* whatever SQ-02 returns. An invalid declaration takes no value.
  What "held" means follows the value (R6-3): *enforced by the host loop* —
  the run stops at its next action; *enforced on the host route* — the host
  refuses the held host operations and any other action is shown as action
  during hold; *not established* / *not enforceable* — nothing is stopped.
  An App hold is never shown as enforced when it was not.
- **Action during hold — governance phase (retained)**: each run action not stopped by the hold of a governed checkpoint (R6-3) is shown with its reference and its **turn initiator** — person-directed · agent · App rule (RS R11; R6-5). Phase 1: the optional "continued past ‹checkpoint› before ‹act›" annotation instead (OV-6).
- **Performed** requires a human-act record of the declared kind bound to the
  subject referent, supported by **capture evidence** from the capturing
  surface. An act captured before the arrival counts when the content it was
  made on is still current, and is shown with its time (SETTLED by
  DECISION-K1 K1-2; EXEC SP-6). An earlier act on content no longer current,
  or of another kind, is shown **"prior act not counted"**, with its reason
  (the one wording, RS-v0.8 L-13; R12-10). Under the
  governance-phase option (EXEC SP-6F) only an act **captured at or after the
  arrival** counts (R4-5), any earlier act is "prior act not counted", and
  where order cannot be established, "act order unknown". A grant, success,
  A3 findings, A14 settlement or an elicitation answer never discharge it.
- **A12 checkpoint** (R4-6): *performed* only when the A12's control effect is
  *established*; *pending* → waiting "A12 awaiting control confirmation";
  *refused* → waiting "A12 refused by control: ‹reason›"; confirmation lost →
  *unknown*. A later established A12 leaves a performed arrival *performed*
  with "superseded by ‹act›". An A12 captured before the arrival — e.g. T15
  on the main timeline — counts while the setting it established is still in
  force, and is shown with its time (DECISION-K1 K1-2); under the
  governance-phase option it is "prior act not counted" (R5-7). V-GR1 is the
  after-arrival case.
- **Mixed items at an A5 checkpoint** (WD §4.3.7 confirmed by EXEC §4.11):
  each item shows A5, A10, undecided, its **item-left** event, or *unknown*;
  "partial" is a per-item annotation; a *performed* over a reduced subject is
  never "all accepted"; an arrival with no items left shows "no items remain"
  and later "replaced by arrival n+1"; an accepted item not applied shows
  "accepted — not applied: refused — stale (…)" / "— application error
  (effect …)" / "accepted — application outcome unknown (observer …)" without
  changing the disposition.
- **Lapse** (R2-19; R4-3): the performing act's lapse is shown as an
  act-lapsed event, in both phases. **Before resume** (before the arrival's
  run-resumed event): "waiting — lapsed at ‹t›". **After resume, run live —
  Phase 1** (OV-5): the act-lapsed event is shown against the affected
  referents as **"act lapsed at ‹t›"** (R8-12 item 1), gated outputs show standing **lapsed**, and no re-held
  annotation or stop is shown; a new act over the current scope is shown when
  the person performs it, and an act on the lapsed referents alone answers
  together with the earlier act for the unchanged ones (joint answer; SETTLED
  by DECISION-K1 K1-3; EXEC §4.7 JA-1). **After resume, run live — governance phase
  (retained), governed checkpoints**: the same
  arrival shows **"waiting — re-held, lapsed at ‹t› after resume"**, whatever
  caused the lapse — a person's edit, **the person's own undo**, or the run's
  own later action (R5-5). What happens follows the hold-support value
  (R6-3): *enforced by the host loop* — the run stops at its next action;
  *enforced on the host route* — the host refuses the held host operations
  and other run actions are shown as action during hold; *not established* /
  *not enforceable* — nothing is stopped and run actions are shown as action
  during hold. The person's own operations (e.g.
  the undo) are never shown as action during hold. Nothing done is undone;
  outputs whose standing names this checkpoint as gating show standing
  **lapsed** for the affected referents; the request is re-issued for the
  whole scope with lapsed referents marked, and an act on the lapsed
  referents alone answers jointly with the earlier act. **A5 and A12 never re-hold**; an
  undo never re-holds an A5 arrival. *Lapsed* as a disposition appears only
  after the run ended.
- **Run end** (R4-4): a run-ended event is shown; a waiting arrival stays
  **waiting**. Ended runs are never resumed. An act captured after the run
  ended is shown against the bound subject marked **"after run end"** and
  changes nothing. A continuation is a new run shown with its **continues
  ⟨run⟩** link; its checkpoints start *not reached*.
- **Negative**: an act-declined event → *resolved negatively*; the declared
  "on negative decision" path governs next.
- The grant display and the checkpoint indicator never merge into one
  "allowed" signal.

## 5. During-work change sequence

1. Only the person changes the grant (A12, S13). An agent may prepare or ask
   (A8): *requested by agent*; settings-in carries requester = agent, no
   setting actor, no A12 reference.
2. The person sets ‹value, σ›: A12 bound to the **setting content** (classes,
   grant values, scope); display *set by person, not yet confirmed*;
   settings-in carries requester = person, setting actor = person, setting act
   reference ⟨A12⟩.
3. Control establishes → new settings version, *effective (person-set)*;
   control effect *established* is a relation on the A12. Control refuses →
   *refused (reason)*; the refused A12 remains a recorded human act,
   establishes nothing and supersedes nothing (R4-6).
4. In flight (R-3.6; DEL-04-01 §5.5; host enforcement DEP-001): an
   already-queued proposal is unaffected; an operation not yet applied is
   re-resolved at application. Two settings references per operation: at route
   decision and in force at application (host-reported, otherwise
   *unconfirmed*).
5. Widening never converts a queued proposal into direct application or
   acceptance. Narrowing never relabels an applied change.

Failure behaviour: control unreachable → *unconfirmed*; conflicting App and
host reports → both shown, *unconfirmed*, defect observation returned; record
write fails → comparison *missing in record* (§6).

Further failure behaviour (v0.8; PROPOSED):

| Failure | Who reports it | Shown as | Next |
|---|---|---|---|
| The host's native layer reports no destinations for a host-loop run | The host (through DEL-05-01); RS R11 "destinations not observed" (LOOP-v0.8 §5.3 DF-F11) | "destinations not observed", never "no destinations contacted" and never "none allowed" (§3.2) | The allow list and in-work grants are still shown from the control |
| A request's prompt cannot be shown, or the control's confirmation of a grant is lost (LOOP DF-F4, DF-F5) | The host's control | DG-15 *not granted* ("prompt not shown"); or DG-5 *unconfirmed*, the requesting call shown waiting, never in force | Nothing is allowed on the display's word |
| The record-out's format version is refused, or read limited (RS §13.4) | The record reader | Comparison *missing in record (unreadable version ‹v›)*; or compared on known elements only, marked "read limited" | The display keeps showing the control's current grant; nothing is inferred from the unread record |
| A destination grant in force on the display has no A12 reference, or a contact names a grant the record lacks | The comparison (§6); the record reader (RS §14.2 R-7) | A defect observation; the grant is shown *unconfirmed* | Returned as a defect; never shown as allowed on the display's word |
| The destination settings and the operation-class grants arrive in one report that merges them | The comparison | Both shown apart; defect observation | Never one "allowed" signal |

## 6. Settings-in / record-out exchange with DEL-04-03 (CASE-002 M3)

Identical to DEL-04-03/RS-v0.8 §8. A data exchange, not an ordering between
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

## 7. Abstract host contribution for direct application

Per directly applied change (host implements; DEP-001; DEP-04-02-010). Not API
fields.

| Element | Meaning | Availability states shown | Never shown as |
|---|---|---|---|
| Origin reference | Host origin mark linked, compared with the request-side origin (DEL-03-02 §3.3: author type, author identity — **unverified** over the external channel until a caller-identity mechanism exists (R4-15) — seat role meaning, channel, conversation, workflow identity and run, standing at drafting, settings references, reason, governing checkpoint constraint with carriage assurance) | supplied · missing · mismatch (evidence limit) | Inferred from the App's request log; a verified identity when unverified |
| Undo route | Host-owned route to undo this change | offered · not offered · unknown | "Available" without a host-supplied route |
| Later-check route | Access for later examination or checking; implies no act (R-4) | offered · not offered · unknown | A performed A4 or A3 |
| Receipt reference | Host receipt; applied-outcome association item ↔ relied-on basis ↔ receipt ↔ resulting revision ↔ resulting objects | supplied · missing · unresolvable | A copy; an acceptance |

**Undo interaction.** The person invokes the offered route → "undo requested"
→ the undo is a change through the one route (DEL-03-02 §4.5; C OP-C10,
governed by the reversed operation's policy record, R3-4): *applied (receipt)*
with **reverses ⟨receipt⟩** · refused (reason) · application error (effect) ·
outcome unknown (observer, last observed state). Only an applied undo with its
receipt is completed; the reversed change then shows **"applied, then reversed
by ⟨receipt⟩"**. A5/A10 on the reversed item are not lapsed; acts bound to
content the undo changes lapse normally.

**SWBPIPE (SQ-10; R8-5).** SWBPIPE's undo is a session snapshot stack: it is
not an operation through the route, writes **no receipt**, and names no
reversed change. "Applied, then reversed by ⟨receipt⟩" needs a host receipt,
so there it is *not supplied*. A lapse the undo causes is still shown, from
the identity change (R8-4). Its receipts are session-only (SQ-01, SQ-09 (c)),
so a receipt reference may later be *unresolvable*.

## 8. Result standing model

Separate facets, each no stronger than received (REQ-004). No synthesized
"verified" / "approved" label.

| Facet | Values | Source | Rule |
|---|---|---|---|
| Temporal | **current** · **historical** · unknown | Host standing; read basis (DEL-03-01 §6.2) | Historical results carry their basis |
| Host checks | **"host checks passed: ‹named checks›"** or "host check failed: ‹named check›", each with evaluated basis · none reported · unknown | Host result standing (e.g. C OP-C12) | A check on an earlier basis is shown **historical**. Never "checked"; agent examination is never shown here |
| Limitations | **limited** (host-known limitations) · none reported · unknown | Host | Verbatim |
| Human acts | Act kind, actor, recorder, recording mode, and state: not lapsed · lapsed · lapsed (subject absent) · partially lapsed · matches c₀ again after observed lapse · unknown (incomparable) · unknown (unavailable) · not yet evaluated; for A12/A13: current · **superseded by ⟨act⟩** (established successors only); markings **by earlier act ‹act› at ‹t›** and **prior act not counted** (at a checkpoint; the latter for an earlier act on content no longer current or of another kind, or under the governance-phase option; DECISION-K1 K1-2), **answered by ‹n› acts** (joint answer; K1-3) and **after run end** | DEL-04-03 record-out | *Not yet evaluated* never shown as not lapsed; lapsed acts show c₀. Where the host supplies only a whole-model identity, it is the identity of every covered subject, so any model change shows the act lapsed (over-lapse, never under); never App-computed (R8-4) |
| Agent examination | A3 findings by reference (e.g. C OP-C3) | Agent | "Examination" / "findings", never a human act or host check |
| Evidence completeness | complete as stated · **missing** (named) · **unknown** (unobserved outcome, with its observer) · **action during hold** (referenced; governance phase) · *not supplied* (e.g. failing targets under a whole-model staleness scope; subject identities beyond a whole-model identity) · "host reachable without evidenced A13" (R8-6) | Record-out evidence limits | Always visible. Phase 1's "continued past ‹checkpoint› before ‹act›" is an optional annotation, not an evidence limit (OV-6) |
| Route and outcome | direct under ⟨set⟩ · proposal with per-item dispositions and actors. Outcomes per DEL-03-02 §9 / DEL-03-01 §4.1: not offered (loop-side) · unavailable · not exposed on this surface · channel not enabled (App- or host-reported) · not permitted (naming treatment, policy record or checkpoint constraint) · refused — invalid · refused — stale (relied and current bases) · queued · accepted · rejected · withdrawn · applied (receipt) · **applied, then reversed by ⟨receipt⟩** · application error (effect none / partial / unknown) · outcome unknown (observer) | DEL-03-02; record | Derived proposal state never stronger than its items; queued ≠ applied; applied ≠ accepted. Accepted then stale: **"accepted by ‹person› — not applied: refused — stale (relied ‹B›, current ‹B′›)"**, A5 not lapsed. *Refused — stale* shows the host's stated staleness scope where the host supplies no subject identities (e.g. "host scope: whole model"; failing targets *not supplied*), never narrowed; per item otherwise (R8-3) |

The person uses these facets to decide the validation warranted (V4-AUT-02);
the display makes no reliance decision.

**Received host terms and SWBPIPE counterparts (R8-3, R8-5; INTEGRATION;
SQ-01, SQ-06, SQ-07, SQ-09, SQ-23).** These display meanings stand as
App/shared meaning. What SWBPIPE currently supplies:

- `unsupported_method` / `unsupported_change` → host-reported **not exposed
  on this surface**, never *not permitted*, a class value or a grant.
- #885 `withdrawn` (the person cleared the queue) → the item left the queue,
  "cleared by the person, no decision record"; `validation_rejected` at Apply
  → **refused — invalid** at application. Neither is ever shown as A10
  *rejected* or A11 *withdrawn*.
- **Accept and apply are one step** on SWBPIPE (Apply, per batch, no A10
  record). "Accepted — not applied: refused — stale" and per-item
  accepted/rejected mixes do not arise there; a stale Apply is refused and
  records no acceptance.
- Staleness is whole-model: any model change stales every queued proposal
  (SQ-07 (d)); the display shows that scope.
- SWBPIPE's own displays (SQ-23): a stale-batch message exists; lapse wording
  and "superseded by" rows are DESIGN only; supersession does not arise (no
  grants); there is no reversal marker. These are host facts, not
  requirements on this display.

## 9. Act-distinction display rules

- **DS-1** One label per act kind; "accept" only for A5, "reject" for A10;
  "approval" only for A6 with its accountable person; "rely" for A7; "tool
  permission" for A14.
- **DS-2** Actor and recorder both shown when they differ (A9 faithful
  recording).
- **DS-3** No act displayed without a received act record with capture
  evidence. Proposal, success, grant, receipt, findings, A8 request, A14
  settlement, user-input or elicitation answers (R4-12), silence or timeout
  display as what they are.
- **DS-4** Absence of an A5 does not invalidate an independently evidenced act.
- **DS-5** An act-declined event is shown as "declined ‹act kind›", never as
  the act; a run-ended event is shown separately and resolves nothing.
- **DS-6** An operation that performs a reserved act (C OP-C6/OP-C7/OP-C8; the
  A12/A13 controls) is shown with the human-act record it produced (RS §3,
  R5-6); a person's own proposals and applications are shown as operations,
  not as human acts.

## 10. Excluded acts and owners (REQ-007)

| Act | Owner |
|---|---|
| Define/carry adopted policy (incl. DECISION-1 records) | DEL-04-01 |
| Record format, writer/reader, lapse handling | DEL-04-03 |
| Hold machine, resume point, re-hold, run finality, compatibility report | DEL-02-03 (App); DEL-05-01 receiving (host) |
| Channel status and the App conversation's model-destination display (RS R5) | DEL-03-03. The display of a host agent's destinations contacted is this file's (§3.2, v0.8) |
| Host controls, validation/application, origin marks, undo, receipts, host panel/loop; offering/recording/presenting host acts; enforcing its own reserved list and channel restrictions | Responsible host owner; SWBPIPE outside session |
| OI-001 / OI-002 (App/shared level); D5; D6 | Decided by the Owner (DECISION-1 D2/D3; DECISION-2 D5); D6 deferred by the Owner to SWBPIPE SQ-02, then closed for Phase 1 by DECISION-4 and re-opened only with the governance phase (R8-2; ScopeOfWork TBD-006; SQ-02 answered 2026-09-28: none); operation-specific additions: Owner via outside SWB session and App/shared owner (OI-021) |
| Resolve OI-013 | Shared contract owner with SWB implementation owner |
| Resolve OI-014 | App/shared contract owners |
| Set the grant (A12); enable or disable external access (A13); perform any human act | The person |
| Professional reliance; certification, sealing, approval, code-compliance statements | Accountable professional |

## 11. Fixture scenarios (designed; fixture subjects)

Identifiers are DEL-03-01/C-v0.4 §10 (commit 8fb51f07f), and C-v0.5 §10.4 V-GR1 (both carried in C-v0.7 §10) (run 13; GR-1…GR-3, GR-P/GR-R/GR-S): FX-PIPE-01, R-100
(fixture run 12), S-1…S-5, Engineer A, B1/B2, PR-1/PR-2, RC-1…RC-3,
⟨set-1⟩/⟨set-2⟩, T1–T17 and T16a, OP-C1…OP-C12, variants V-S1, V-CP1, V-NP1,
V-R1, V-X1, V-OU1. Local cases are `L-AS-n`, each saying why.

**Phase (R8-1).** Checkpoint scenarios give a **Phase-1 result** (OV-1…OV-7:
guidance, record labels, no hold or hold-support value) and, where a hold is
involved, a **governance-phase value**. The governance-phase values read the
fixture's checkpoints **as if declared governed**; no fixture declares the
flag (EXEC GV-5; R8-11 item 5).

| F | Scenario | Expected display / exchange |
|---|---|---|
| F1 | T1 ⟨set-1⟩ (C FXA-4): P-03 classes (OP-C4/C5/C9) default; OP-C11 *no policy basis*; OP-C6/7/8 reserved | P-03 **effective (policy default): propose**, P-03 reference, no setting actor; OP-C11 "no policy basis — held (pending OI-021)"; OP-C6/7/8 reserved, offered |
| F2 | T15 (R4-18): Engineer A A12 → ⟨set-2⟩: class P-03, grant value direct, scope {model/workspace FX-W1; object set {S-4}}; control confirms | *set by person, not yet confirmed* → **effective (person-set): direct** within that scope; settings-in A12 ref, then establishment evidence; record-out *match*. Per C T15, no expectation for OP-C5 on S-4 (held on U-02) |
| F3 | Agent A8 asks to widen P-03 to all of R-100 (L-AS-1: C has no A8 step) | *requested by agent*; no A12; ⟨set-2⟩ governs |
| F3b | V-NP1: Engineer A A12 widening OP-C11 to direct | **refused (reason: no policy basis)**; fixture result **held** |
| F4 | Host unreachable after T15 (L-AS-2: C has no outage step) | P-03 → *unconfirmed*; no direct branch |
| F5 | Record write for ⟨set-2⟩ fails (L-AS-3: record-side failure) | *missing in record* surfaced |
| F6 | L-AS-4 (C FXA-5 declares CP-accept and CP-check, but CP-check binds only CP-accept items' applied outcomes, and T16 is a direct application): checkpoint requires A4, subject class "objects changed by a named outcome" = T16's resulting objects (S-4), reached-when *T16 applied*; **host-loop run on E** (governance phase: hold support **enforced by the host loop**, subject to host evidence, DEP-001) | *Both phases:* arrival 1 *waiting* at T16; T16a A4 (captured after the arrival) → **performed**, ordinal 1; run-resumed event at the run's next action (before T17); T17 is Engineer A's own undo — an operation, never action during hold or continued past — and lapses T16a (act-lapsed event). *Phase 1:* the host loop holds nothing (EXEC PH-2); no hold-support value; the lapse is shown and no re-held annotation or stop is shown (OV-5). *Governance phase:* hold support **enforced by the host loop**; after T17 **"waiting — re-held, lapsed at T17 after resume"** (R5-5); the loop stops at its next action; request re-issued for S-4. (SWBPIPE has no host loop, SQ-20) |
| F6c | F6 as an **App run on X** (L-AS-4 variant; same reason); its held actions are the run's next actions, which include App agent turns | *Phase 1:* the arrival and the same dispositions are shown as record labels; no hold-support value and no *unsupported* for a hold reason; after T17 the lapse is shown, with no re-held annotation and **no stop**; later run actions may carry "continued past the checkpoint before A4" with turn initiator *agent* (OV-6). *Governance phase:* App-side held actions → hold support **not enforceable** (R6-1 HS-5) → workflow *unsupported*; after T17 the re-held annotation is shown, **no stop is shown**, and later run actions are shown as action during hold with turn initiator *agent* |
| F6d | L-AS-4 variant: the same A4 checkpoint declared to hold only host operations on S-4 until the act, App run on X | *Phase 1:* the checkpoint is guidance; the requirement check is decided by required tools and channel state; nothing is stopped; run actions before the A4 may carry "continued past the checkpoint before A4". *Governance phase:* HS-3 (c): **not enforceable** (SQ-02 answered 2026-09-28: no host-held route) → requirement check **unsupported** ("checkpoint hold not enforceable on this surface: ‹name›"; was *not established* at v0.5); nothing is stopped; run actions shown as action during hold. It would be *enforced on the host route* only with a host-held route evidenced on a candidate. Counterpart: ACT `CP-L4` (L-ACT-4, ACT §4.6), the same host-operations-only A4 on S-4 |
| F6b | V-CP1 | *Phase 1:* no constraint is carried or shown; the agent proposes OP-C4 as the declaration asks, and if a direct request is made the host's own treatment decides and is shown as observed (R8-11 item 2). *Governance phase:* direct OP-C4 → *not permitted* naming {run 12, CP-accept, A5, OP-C4} with its carriage assurance; not converted; **AWAITING INPUT** — SQ-02 answered 2026-09-28: no receipt, no host copy (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3) |
| F7 | T16 direct OP-C9 (RC-2, origin, undo route, later-check route); T17 OP-C10 → RC-3 reverses RC-2 | Four elements supplied; T16 shown **"applied, then reversed by RC-3"**. (Fixture. SWBPIPE's session undo writes no receipt, so there the reversal is *not supplied*; SQ-10, R8-5) |
| F8 | T16 with acknowledgement lost (L-AS-5: C's V-OU1 is on the proposal path) | Undo route *unknown*; outcome unknown, observer loop; settings at application *unconfirmed* |
| F9 | Standing: T1 host checks passed "equilibrium", "unit consistency" at r12; after T6 those results historical; T4 OP-C3 A3 findings; T4a OP-C12 "host check failed: support spacing" at r12; T8 OP-C2 unavailable; T2 A4 on S-2 not lapsed at r13, lapsed at T14 | Host checks with basis r12, historical at r13; T4a shown as a host check, historical later; **T4 shown only as "agent examination — findings", never "host checks passed"**; unavailable with reason; lapse with c₀ |
| F10 | Distinctions: T2 A4 plus App-agent faithful record; T5 proposal only; T16 success; T15 grant only; T4 findings; A14 answered by user's Codex mode; an elicitation answer "yes"; A4 without A5 | Actor and recorder shown; negatives show no act; A14 and elicitation are not acts or grants |
| F11 | Agent requests OP-C4 directly on R-100 under ⟨set-2⟩ (outside scope {S-4}) | *not permitted* naming ⟨set-2⟩ and P-03; no proposal created |
| F11b | V-R1 | *not permitted*, A8 offered; no automatic A8 record |
| F12 | L-AS-6 (narrowing has no C step): Engineer A A12 narrowing P-03 to propose, established, while a direct OP-C9 is not yet applied | Re-resolved at application → *not permitted*; two settings references; T15's A12 shown **superseded** |
| F12b | L-AS-6 variant: the narrowing A12 is **refused** by the control | T15's A12 **not** superseded; ⟨set-2⟩ still governs; refusal shown |
| F13 | V-S1 | "accepted by Engineer A — not applied: refused — stale (relied B2, current ⟨B-r14′⟩)"; A5 not lapsed |
| F14 | **V-GR1** (C-v0.5 §10.4, run 13 on E; governance phase *enforced by the host loop*): GR-1 CP-grant arrives at r15 (held OP-C9 call on S-4); GR-2 T15's A12 captured after the arrival, established; GR-3 held call dispatched unchanged as T16. Sub-variants GR-P, GR-R; L-AS-7 variant (decline has no C sub-variant): Engineer A declines | *Both phases (record labels):* GR-1 waiting → GR-2 **performed** → GR-3 dispatched; GR-P waiting "A12 awaiting control confirmation", then *unknown*; GR-R waiting "A12 refused by control: ‹reason›", **⟨set-1⟩** stays in force, supersedes nothing; decline → *resolved negatively*. On the main timeline T15 counts toward no arrival. *Phase 1:* no call is held by the loop or the App; the OP-C9 dispatch is shown as observed, and the host's own treatment governs (EXEC CH-12). *Governance phase:* the call stays held under GR-P and GR-R. From the App via X, `CP-grant` is **not enforceable** (HS-3 (c); SQ-02 answered 2026-09-28; was *not established* at v0.5) |
| F15 | **V-GR1 GR-S**: a later established A12 narrowing the scope | CP-grant stays *performed*, "superseded by ‹act›"; a refused later A12 supersedes nothing |
| F16 | L-AS-9 (run finality has no C step): a V-GR1 run ends while CP-grant waits; Engineer A then performs the A12; a new run starts | A12 shown "after run end", ended arrival unchanged; new run shown **continues ⟨run⟩**, checkpoints *not reached*; at its arrival the post-end A12, if the control established it and that setting is still in force, counts: *performed*, shown with its time (DECISION-K1 K1-2); under the governance-phase option it shows **"prior act not counted"** |
| F17 | L-AS-10 (R3-1 class is used by neither FXA-5 checkpoint): A4 checkpoint with subject class **objects a named output concerns** = T4a output spans (S-2, S-3); T2's A4 on S-2 | T2's A4 counts for S-2, whose content is still current, and is shown with its time; the arrival waits for an A4 on S-3, and the two acts together answer it (DECISION-K1 K1-2, K1-3). Under the governance-phase option: T2 act shown **"prior act not counted"**; arrival waits for a new A4 on S-2 and S-3 |
| F18 | Checkpoint kind (a) on a harness capability in an App run whose tools the user's mode auto-settles (R4-21); variant: an App run of **E1 on X** | *Phase 1:* no hold-support value. The requirement check is shown *not established*, because the harness-capability reference is unresolved (a required-tool matter, not a hold; R8-11 item 3; EXEC MT-15); a dispatch while waiting may carry "continued past ‹name› before ‹act›". Variant (E1 on X): the check is decided by required tools and channel state (EXEC MT-2); `CP-accept` and `CP-check` are guidance. *Governance phase:* hold support **not enforceable**; workflow shown *unsupported* ("checkpoint hold not enforceable on this surface: ‹name›"); a dispatch while waiting shown as **action during hold**. Variant: `CP-accept` **not enforceable** (HS-3 (c), SQ-02 answered 2026-09-28) and `CP-check` **not enforceable** (holds App-side Return) → the workflow is **unsupported** ("…: CP-accept, CP-check") |
| F20 | L-AS-11 (Phase-1 guidance has no C step): an App run on X with the F6d checkpoint, not `governed`. After the arrival: (a) the agent issues a further host operation; (b) the agent's record claims Engineer A's A4 without capture evidence; (c) Engineer A's A4 is captured. Variant (d): the checkpoint declared `governed` | (a) Shown as observed, optionally "continued past the checkpoint before A4" (turn initiator *agent*); never a warning, stop or *unsupported*. (b) No act shown (DS-3); the record is non-conformant. (c) **performed** shown as a record label. No hold-support value at any point. (d) Same in Phase 1, with the `governed` flag shown (OV-7) |
| F19 | DEL-03-03 L-ADAPTER-8: App conversation uses a user-chosen cloud model; external access enabled; a supplier re-route mid-run | Grant display unchanged; no gate or warning state here; per-turn requested/effective destinations and the re-route are shown in DEL-03-03's channel status and recorded in RS R5 (SETTLED: the reading confirmed by the owner, OWNER_ITEMS O-10) |
| F21 | L-AS-12 (R8-13; C has no network subjects): host-loop run; web access switched on; named MCP entry M-1; the agent asks for A-1 and Engineer A grants it for this run; a later request for A-2 is declined; the agent writes an entry for A-3 | Allow list shows web access on, M-1 as a named entry and the model service "allowed by your model choice". A-1 shown as an in-work grant, scope this run, with time and A12 reference; gone after run end. A-2 not shown as a grant (the outcome is "destination not allowed by the person"). A-3 shown at most as "Agent requests …", never a grant. Operation-class grants unchanged and shown apart |
| F23 | L-AS-14 (node B5; C has no network subjects): host-loop run E-14 (RS `RS_RECORD.valid.host-destinations.example.jsonl`): model-service contact (cloud); a V-D refusal of W-2; a request carrying its call, granted once, and the contact; MCP server M-1 with stateless evidence; M-4 refused; a request ended by a turn cancel | §3.2: the contacts with their allowing entries ("model choice", class cloud; "in-work grant: once"); the refusals apart, stage and reason shown; the turn-cancelled request "unanswered at end", not sent; M-1 with "process network not observed" and "stateless revision declared, not verified"; nothing merged with §3 |
| F22 | L-AS-13 (R8-13; C has no network subjects): host-loop run. (a) The agent asks for A-1 once; Engineer A grants; the control establishes; the call contacts A-1. (b) A grant for this run; the run ends. (c) A grant always; later Engineer A removes the entry (established). (d) A grant for M-2; the control refuses, "not stateless MCP (2026-07-28)". (e) The confirmation of a grant is lost. (f) A request nobody answers. (g) The native layer reports no destinations | (a) DG-1 → DG-2 → DG-3 → DG-6: *consumed*, the contact "in-work grant: once". (b) DG-8: *ended with run*; a continuing run inherits nothing. (c) DG-9 → DG-10: *listed*, then *superseded by ‹act›*. (d) DG-4: *refused (reason)*, nothing allowed. (e) DG-5: *unconfirmed*, never shown in force. (f) DG-12: still *requested*, never granted. (g) "destinations not observed", never "none contacted" (§5). Operation-class grants unchanged and shown apart throughout |

## 12. Receivers (from the registers; R9-6)

A table of named receivers only. It is rebuilt from the ACTIVE rows of this
deliverable's `Dependencies.csv` and of each consumer's own register. It
defines no contribution. What each receiver takes element by element, the
condition of use, and the behaviour on *unconfirmed* or *missing* are
stated in §12.1 (v0.8).

| Receiver | Local row | Receiver's own row | DAG-003 | Contribution the register names | Where this file defines it |
|---|---|---|---|---|---|
| DEL-04-03 | DEP-04-02-009 | DEP-04-03-022 | held (SCC-002) | Settings-in: the visible autonomy settings and during-work changes, passed through the record interface | §6 |
| DEL-05-01 | DEP-04-02-019 | DEP-05-01-025 | held (SCC-002) | Visible autonomy state. DEP-05-01-025: "the autonomy-grant display states and standing exchange", consumed "as the grant in force carried on each loop dispatch" | Grant display states: §3. Standing: §8. The grant in force carried on each loop dispatch: §12.1 (v0.8) |
| DEL-05-02 | DEP-04-02-020 | DEP-05-02-019 | held (SCC-002) | Visible autonomy state. DEP-05-02-019: "autonomy-grant display states and active scope definition" | §3 (states and scope); §4 (checkpoint overlay) |
| DEL-03-02 | DEP-04-02-021 | none | held (SCC-002) | Visible autonomy state | §3 (states, including *effective (policy default)*); §6 (settings versions) |
| DEL-03-03 | DEP-04-02-022 | none | held (SCC-002) | Visible autonomy state | §3 (the grant display; the channel status beside it is DEL-03-03's) |
| DEL-02-03 | DEP-04-02-023 | none | held (SCC-002) | Visible autonomy state | §3; §4 gives the display meanings of EXEC's annotations (EXEC §9.2) |
| DEL-03-04 | none | DEP-03-04-012 | admitted | "autonomy/standing and origin/undo/proposal-presentation receiving semantics" | §2–§8 (GUIDE cites §3, §4, §7 and §8) |
| DEL-09-06 | none | DEP-09-06-031 | admitted | "grant display" | §3 (CA cites §3, §4, §8 and §9) |
| DEL-09-09 | none | DEP-09-09-022 | held (SCC-002) | "grant display states for the external-route and three-channel examination" | §3 |

- A held arc is a non-gating candidate. Satisfaction is read from the live
  registers; no row records it.
- The arcs N-18, N-21, N-24 and X-1 have no end at DEL-04-02.
- Inputs are not tabled here. One is noted because a register names it:
  DEP-04-02-018 has this file consume, from DEL-05-01, the allow list, the
  in-work destination grants and the contacted-destination record. §3 and
  §3.1 show the first two; **§3.2 shows the third, and this file owns that
  display** (node B5; S1-A AS 3). PANEL ND-4 receives it for a host panel.

### 12.1 Provided to receivers (AS 5; PROPOSED)

What each receiver named in §12 is given, when it may use it, and what it
does when the grant is *unconfirmed* or the input is *missing*. Treatment is
always resolved on the host route (ACT §5.3); nothing here lets a receiver
decide treatment or widen a grant. *Missing* means no report was received;
it is never read as *not set*, which means "no person setting and no policy
default" (§3).

| Receiver (row) | Elements provided | Condition of use | On *unconfirmed* | On *missing* |
|---|---|---|---|---|
| DEL-04-03 (DEP-04-02-009) | Settings-in, per run and per change (§6), including a host agent's destination settings; PROPOSED representation `AS_SETTINGS_IN.schema.json` | Written as a `settings_version` entry in order with the operation entries (RS §13, §14.1) | Recorded with display state *unconfirmed*; never as *effective* | No entry; the comparison shows *missing in record* or *missing in display* (§6) |
| DEL-05-01 (DEP-04-02-019; DEP-05-01-025: "the grant in force carried on each loop dispatch") | **Grant in force per dispatch** (defined here): the settings version identity in force at route decision; for the operation's class its grant value, display state, scope and policy-class record reference {policy revision, record}; for a host agent's network use, the destination settings version in force (allow list and in-work grants with states) | The loop carries it on the dispatch record (LOOP §6.2) and relays intent; the host route resolves treatment. It never converts a direct request into a proposal or the reverse | The dispatch records "grant in force: unconfirmed"; no direct branch is claimed; the host's refusal, if any, is recorded as observed | The dispatch records "grant in force: not received"; no default is assumed; for destinations the native layer allows only what the host's control holds |
| DEL-05-02 (DEP-04-02-020; DEP-05-02-019: "autonomy-grant display states and active scope definition") | The seven display states with value and scope per class (§3); the destination settings and the §3.1 states; the destinations-contacted display (§3.2, node B5; PANEL ND-4); the checkpoint overlay meanings (§4); the standing facets (§8) | The panel renders the same meanings (PANEL §3.6, §3.8 ND-5); grants and the checkpoint indicator never merge | Last-known value, "unconfirmed"; no direct branch shown | "grant state not available" (PROPOSED wording); never *not set* and never a guess |
| DEL-03-02 (DEP-04-02-021) | The settings version identity and display state at route decision (P's standing at drafting), with the policy-class record reference and default for *effective (policy default)*; the settings reference at application when the host reports it | P records both references (P §3.3; RS §5); the host route decides treatment | Standing at drafting recorded *unconfirmed*; the proposal path is unaffected | "settings reference: not supplied" on the entry; never inferred |
| DEL-03-03 (DEP-04-02-022) | The grant in force for the external channel's dispatches (as for DEL-05-01, ADAPTER §5.5), shown beside, never merged with, the channel status the adapter owns | The adapter relays only (ADAPTER RD rules); the model destination never gates (§2) | Dispatch carriage "grant in force: unconfirmed" | "grant in force: not received"; the channel status is unaffected |
| DEL-02-03 (DEP-04-02-023) | The display meanings of EXEC's annotations (§4); for an A12 checkpoint, whether the setting an earlier A12 established is still in force (DECISION-K1 K1-2) | EXEC takes dispositions from the record (RS R8); the display is derived | The earlier A12 is not counted as still in force: the arrival is *unknown*, as for a lost confirmation (L-0; EXEC §4.10) — PROPOSED | As *unconfirmed* |

Declared upstream in the consumer's own register only (DEL-03-04, DEL-09-06,
DEL-09-09): the guide, CA and XT read §3, §3.1, §4, §6 and §8 as cited in
§12, with the same *unconfirmed* and *missing* behaviour as DEL-05-02.

## 13. Component structure — PROPOSED options under OI-014 (AS 8; U-08)

**Standing.** Options, not a choice. OI-014 is open: "Place shared
contracts/components against actual consumer responsibilities; agree
ownership before any common implementation, without presuming a common
service." R12-2 keeps placement open for the phase review. The components
below are functions of OUT-001, whatever their placement.

| Component | Function | Inputs → outputs |
|---|---|---|
| K-1 Grant state deriver | Derives the seven display states per class and scope, and the destination states of §3.1 | Control reports, A12 records, policy-class records → display states |
| K-2 Settings-in emitter | Hands each settings version to the record writer | K-1's states → `settings_version` entries (§6) |
| K-3 Record-out comparator | Compares displayed with recorded | Record-out, K-1's states → match · mismatch · missing in record · missing in display (§6) |
| K-4 Grant display | Shows §2–§3 and §3.1 | K-1's states |
| K-5 Checkpoint overlay | Shows §4 | Record-out (RS R8) |
| K-6 Standing facets | Shows §7–§8 | Record-out; host standing |
| K-7 Receiver feed | Supplies §12.1 to the loop, the panel, P, the adapter and EXEC | K-1's states |

| Option | What is shared | What each surface builds | For | Against |
|---|---|---|---|---|
| **CS-1 Contract only** | This definition, the two schemas (`AS_SETTINGS_IN.schema.json`; RS `RS_RECORD.schema.json`) and their conformance fixtures | The App and each host panel build K-1…K-7 themselves | No shared code; no common service presumed; the host keeps its ownership (DEP-001) | Two or more implementations kept aligned only by fixtures |
| **CS-2 Shared library for the non-visual parts** | K-1, K-2, K-3 and K-7 as one library, plus the schemas and fixtures | Each surface builds K-4…K-6; a host panel may adopt the library or implement the contract | One derivation and one comparison | Runtime coupling with host code; a host may decline it (DEP-001), leaving CS-1 for that host |
| **CS-3 App-built, host by contract** | Schemas and fixtures | The App builds K-1…K-7 for App surfaces; each host panel builds its own against the contract (PANEL is a receiving contract) | Matches the current ownership split (DEL-05-02 receiving; host builds) | As CS-1 for hosts |
| **CS-4 App-side service** | K-1, K-3, K-7 as a service in the App process that host panels query | Renderers only | One live state | Presumes a common service, which OI-014 says not to presume; couples host panels to the App's process; listed for completeness |

What every option needs, and this version supplies as PROPOSED: the
settings-in schema with valid and invalid examples, the record schema it is
carried in, the §3.1 transitions with their walk, and the F scenarios of
§11. What the choice changes: who builds K-1…K-7, where conformance evidence
comes from (a library's tests or each surface's fixture results), and which
register rows carry the components. **No option is chosen here** (R12-2).


## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| U-01 Operation-specific reserved additions and class assignments `OI-021` | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution | "No policy basis — held" for pending operations |
| U-02 Consequence vocabulary | DEL-04-01 with host policy owner | Before class assignment in DEL-03-01 | Scope slot only; OP-C5 on S-4 under ⟨set-2⟩ held |
| U-04 Host enforcement of *unconfirmed*, re-resolution at application, de-duplication | Responsible host owner (DEP-001). SWBPIPE autonomy is SWBPIPE owner decision OI-016 | Before connected integration | Display rule DERIVED; host behaviour unevidenced. SQ-05 (h): not applicable to SWBPIPE (no grants; Apply always revalidates, SQ-07 (e)) |
| U-05 Host origin, undo, later-check route, receipt, resulting objects, host-check basis `DEP-001` | SWBPIPE outside implementation session | Before corresponding connected-journey integration/examination and fallback-replacement decision | All host elements are fixture |
| U-06 Settings version in force at application | Responsible host owner (DEP-001) | Before connected integration | *unconfirmed* unless reported. SWBPIPE reports no settings reference (SQ-05 (d)) |
| U-07 Host capture requirement and capture-evidence reference. SQ-01 answered 2026-09-28: SWBPIPE exposes none | SWBPIPE owner decision (PB-TBD-002 acceptance-record storage; DEL-16-03 actor identity; ANS §2) | Before host act-recording integration | No host-content arrival reaches *performed* without it |
| U-08 Component placement / host panel assembly `OI-014`, `OI-013` | App/shared contract owners; shared contract owner with SWB implementation owner | Before structural/production contract allocation (OI-014); before shared/host implementation boundary contracts (OI-013) | OUT-001 components only "where justified". **v0.8:** the components K-1…K-7 and four PROPOSED options CS-1…CS-4 are stated in §13 for the phase review; none is chosen (R12-2) |
| U-10 Record representation for the exchange | DEL-04-03 (RS U-04) | Before writer implementation | **v0.8:** PROPOSED representations exist — settings-in `AS_SETTINGS_IN.schema.json` (here) carried in RS's `RS_RECORD.schema.json` (RS §13); not accepted |
| U-12 Host receipt or own evaluation of the governing checkpoint constraint (governance phase) | Host owner (relay SQ-02). SQ-02 answered 2026-09-28: route (iv), none planned; planning one is a SWBPIPE owner decision (ANS §2) | Before connected integration; when the owner resumes UI-SUCCESSOR (DECISION-3) | Phase 1: no constraint carried or shown (§2). Governance phase: F6b **AWAITING INPUT** — SQ-02 answered: no receipt, no host copy (not offered); host joins deferred (DECISION-3); only host-held satisfies R2-12; App-assured unavailable (R5-2) |
| U-15 CLOSED (v0.7) — register edges to DEL-03-02, DEL-05-01, DEL-05-02, DEL-03-03 and DEL-02-03 exist: DEP-04-02-019…023, ACTIVE, first seen 2026-09-29 | Register owner | — | Receivers are listed from the registers (header; §12) |
| U-16 App-side run holds `UNRESOLVED{D6}`. **Closed for Phase 1** by DECISION-4 D4-1 (R8-2); **re-opens only when the governance phase is taken up**. SWBPIPE answered SQ-02 on 2026-09-28: route (iv), none planned | The owner (DECISION-4; D6 re-opens with the governance phase) | When the governance phase is taken up for a workflow that needs it; before hold-display fixtures run (ScopeOfWork TBD-006) | Phase 1: no hold or hold-support value shown (OV-3). Governance phase: hold support (R5-1 values) and action during hold shown; HS-3 checkpoints *not enforceable* against SWBPIPE, HS-5 *not enforceable*; no unenforced hold shown as held |
| U-17 *Closed (DECISION-K1 K1-2, 2026-09-30).* SP-6 versus counting a prior act on current content (EXEC U-E4) | The owner (decided) | — | **Settled for the current phase:** an earlier act on current content counts and is shown with its time; "prior act not counted" only for content no longer current, another kind, or the governance-phase option (EXEC SP-6F) |
| U-18 Caller identity verification over the external channel (ADAPTER OC-6) | App owner with host owner | Before origin conformance | Author identity shown *unverified* |
| U-19 *Closed (DECISION-K1 K1-3, 2026-09-30).* Multi-row A4 purpose after partial lapse | The owner (decided) | — | **Settled:** an act on the lapsed referents alone answers together with the earlier act; each is shown with its referents (joint answer; EXEC §4.7 JA-1) |
| U-20 Grant display for a host without a grant model (R8-10; I2 R8-Q16) | DEL-04-02 with the integrator; PROPOSED, deferrable with the host joins | When the host joins resume (DECISION-3) | §3 "host fixed treatment" display applied as PROPOSED |
| U-21 DECISION-5 points settled by the owner's DECISION-5 confirmation (2026-09-28: the "MCP V2" reading confirmed; the person-only grant not objected to and stands) (closed for those points) (person-only grant; the reading of "MCP V2") and LOOP N-OPEN-4 (how a category switch and its named entries combine) (R8-13). **N-OPEN-4 closed by DECISION-K1 K1-5 (2026-09-30):** a named entry is allowed on its own; a switch allows the whole category | The owner (decided) | — | Switches and named entries are shown separately, each with its meaning (§3); grants shown as the person's A12 |

Closed in v0.8: none (U-08 and U-10 advanced, not closed). Closed in v0.7, node A3 (DECISION-K1): U-17 (K1-2), U-19 (K1-3), and U-21's remaining N-OPEN-4 part (K1-5). Closed in v0.7: U-15 (the register edges exist: DEP-04-02-019…023). Closed in v0.6: none (U-16 closed for Phase 1 only). Closed in v0.5: none. Closed in v0.4: U-09 (EXEC §4.11), U-11 (R4-4), U-13 (R4-3), U-14 (R4-6).
Earlier: U-03.

## Verification cases (designed; VC-19's state walk and VC-22 ran on the local prototype only, not on a candidate)

| Case | Input | Expected result | Serves |
|---|---|---|---|
| VC-01 Scope before/after change | F1, F2 | Visible grant value and scope equal the effective grant; default shown *effective (policy default)* without A12; T15 scope {FX-W1; {S-4}} | VER-001 (AC-001) |
| VC-02 Agent request, refusal, no policy basis | F3, F3b, F12b; a success in a propose class | No widening; refused A12 supersedes nothing; F3b **held** | VER-001 (AC-001) |
| VC-03 Checkpoint not discharged by autonomy | F6, F6b, F6c, F6d, F14, F17, F18, F20 | Both phases: *waiting* (a record label in Phase 1) until a capture-evidenced act (an earlier act counts on current content, shown with its time, DECISION-K1 K1-2; F17 answered jointly, K1-3); an earlier act on content no longer current is "prior act not counted"; A12 pending/refused → waiting; declined → resolved negatively; run-ended → waiting. Phase 1: no hold-support value or *unsupported* for a hold reason; F18's check *not established* for its harness-capability reference. Governance phase: App-side held actions → not enforceable → unsupported (F6c, F18); host-operation-only → **not enforceable → unsupported** (F6d; SQ-02 answered); E1 on X → **unsupported** (F18 variant); F6b AWAITING INPUT with the SQ-02 answer annotated | VER-001 (AC-001) |
| VC-04 No direct conversion; reserved entries offered | F11, F11b | *not permitted*; no proposal or A8 created automatically | VER-001 (AC-001) |
| VC-05 Settings-in / record-out match | F1, F2 | Match incl. scope, requester, setting actor, A12 or policy-record reference | VER-002 (AC-002) |
| VC-06 Missing / unconfirmed / in-flight | F4, F5, F12 | *unconfirmed*, *missing in record*; two settings references; queued proposal unchanged | VER-002 (AC-002) |
| VC-07 Origin/undo/later-check; reversal | F7 | Elements traced to fixture host evidence; "applied, then reversed by RC-3" only with RC-3 | VER-003 (AC-003) |
| VC-08 Absent host capability | F8 | Undo unknown; outcome unknown with observer | VER-003 (AC-003) |
| VC-09 Standing facets | F9, F13 | Each facet equals supplied evidence; T4 findings never shown as host checks; stale-after-accept wording | VER-004 (AC-004) |
| VC-10 Lapse after resume, including the person's undo | F6, F6c | Both phases: act-lapsed event shown; gated outputs lapsed; T17 never shown as action during hold or continued past. Phase 1: no re-held annotation and no stop. Governance phase: "waiting — re-held, lapsed at T17 after resume"; stop shown only under *enforced by the host loop* (F6), not under *not enforceable* (F6c) | VER-004 (AC-004) |
| VC-11 After run end and continuation | F16 | "after run end"; ended arrival unchanged; continues ⟨run 12⟩ shown; the post-end act counts in the new run while its setting is in force (not counted only under the governance-phase option) | VER-004 (AC-004) |
| VC-12 Act distinctions, labels, supersession | F10, F14, F15, F12/F12b | Faithful record positive; negatives show no act; labels per R-4; reserved-act operations show their act record (DS-6); T15 before arrival not counted; supersession only by established A12 | VER-005 (AC-005) |
| VC-13 Destination not a gate | F19 | Grant display and enablement unaffected by destination or re-route; no permission shown | VER-006 (AC-006) |
| VC-16 Hold-support values (governance phase) | F6, F6c, F6d, F14, F18 and its variant (governance-phase columns, read as governed) | Only the four R5-1 values, classified by held actions (R6-1); *not established* never pass or *unsupported*; *not enforceable* → *unsupported* with the R4-8 string; stop shown only under *enforced by the host loop* (R6-3); no retired value; SWBPIPE's SQ-02 answer gives HS-3 (c) (R8-2) | VER-001 (AC-001) |
| VC-17 Phase-1 overlay (R8-1) | F6, F6b, F6c, F6d, F14, F18, F20 (Phase-1 columns) against §4 OV-1…OV-7 and EXEC PH-1…PH-10 | No hold, stop, re-hold or hold-support value shown, and no *unsupported* for a hold reason; acts shown only from records of the person performing them; reserved acts remain the person's, with host refusals shown as observed; arrivals and acts shown as observation; "continued past ‹checkpoint› before ‹act›" optional and never a warning or defect; lapse still shown; `governed` flag shown and changes nothing | VER-001 (AC-001) |
| VC-14 Owner and open-choice trace | §10, UNRESOLVED | Each REQ-007 act traced; D2/D3/D5/D6 cited only for what they say; OI owners and points of need match register; no host delivery claimed | VER-006 (AC-006) |
| VC-15 Suite coverage | VC-01…VC-13 and VC-16…VC-23 | Each AC-001…AC-005 covered; results bound to an identified candidate; held and AWAITING INPUT never counted as passes | VER-007 (AC-007) |
| VC-18 Network-destination grant display (R8-13) | F21 against §3 and ACT §2.7 | Allow list and in-work grants shown with their scopes and A12 references; model service shown as allowed by the model choice; agent requests and declines never shown as grants; destination and operation-class grants shown apart | VER-001 (AC-001) |
| VC-23 Destinations-contacted display (node B5; S1-A AS 3) | F23 against §3.2, RS R15 and LOOP-v0.8 §5.3 | Every contact shown with its allowing entry, in any model mode; declines, refusals and unanswered requests shown apart, their recording marked PROPOSED; outside processes with both limits; "destinations not observed" never "none contacted"; nothing merged with §3 or the checkpoint indicator | VER-001 (AC-001) |
| VC-19 In-work destination-grant transitions (AS 7) | F22 against §3.1 DG-1…DG-15; `prototype/validate_settings_in.py` | Each sequence ends in the state §3.1 gives; forbidden transitions (a grant by timeout or by an agent-written entry; reuse of a consumed or ended grant; a refused grant becoming in force; a declined request becoming a grant) do not exist. **The state walk ran 2026-09-30 on the prototype: held** | VER-001 (AC-001) |
| VC-20 Receiver conditions (AS 5) | §12.1 against each receiver's own text (LOOP §6.2, PANEL §3.6, P §3.3, ADAPTER §5.5, EXEC §4.10) | Each receiver has elements, a condition of use and behaviour on *unconfirmed* and *missing*; *missing* is never shown as *not set*; no receiver decides treatment | VER-002 (AC-002) |
| VC-21 Destination exchange (AS 4; RS 6) | F21, F22; RS VC-38 | Settings-in carries the destination settings apart from the operation-class grants; record-out carries R15; comparison covers settings, not contacts; §6 and RS §8 identical | VER-002 (AC-002) |
| VC-22 Settings-in representation (R12-1) | `AS_SETTINGS_IN.schema.json` with its examples | Valid examples validate; INV-AS-1 (person-set without A12), INV-AS-2 (agent request with an A12 reference), INV-AS-3 (scope "forever") and INV-AS-4 (an always-off item on without an A12 reference; RP-4) fail. **Ran 2026-09-30 on the prototype: held** | VER-002 (AC-002) |
