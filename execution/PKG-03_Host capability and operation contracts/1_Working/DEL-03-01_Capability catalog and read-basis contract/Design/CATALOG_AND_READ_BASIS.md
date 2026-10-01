# Capability catalog and read-basis contract
- Contribution: DEL-03-01/C-v0.8 (supersedes DEL-03-01/C-v0.7, last changed at `c896a99d90` and unchanged at `86cafc0e1c`, file sha256 eaf16b82b4250c56446544dd97a65baf064091d196013fb28abda40d543e010c; C-v0.7 superseded DEL-03-01/C-v0.6, last changed at `caa4334ca1` and unchanged at `3dd7c22c73`, file sha256 8282c003024e54708f3b9842e04b6b0dc8c4e1c496027afae582eb6387675ce4; C-v0.6 superseded DEL-03-01/C-v0.5, last changed at `c6f81a4f2` and unchanged at `94aa9181b`, file sha256 72ac4f0f853213f9778d69c4b3eb84d6b19d1bab80a147d98b7bc5068bb0eacf)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Phase (R8-1; R9-1): in the current phase (Phase 1), this increment, declared workflow checkpoints are **plan guidance** (EXEC-v0.6 §2.1; WD-v0.8 §4.3.0). The checkpoint-constraint and hold-support statements in this file are the **governance-phase definition (retained)**, stated beside a Phase-1 statement. V4-WF-05 and V4-HI-42 are cited as amended by SCA-V4-001 (accepted 2026-09-29): in force in every phase, the required human act is requested, it is recorded as done only when the person performs it, and the reserved acts bind; holding the run until the act is **phased to the governance layer, not withdrawn** (§0). SWBPIPE's answers are recorded as answers about its current state, not commitments; host joins are deferred (DECISION-3)
- Serves: OUT-001 (catalog and read-basis schema meaning; at v0.8 also three PROPOSED JSON Schemas beside this file, R12-1), OUT-002 (three-surface responsibility map skeleton), OUT-003 (designed contract fixtures, the shared fixture catalogue and, at v0.8, the simulated host SH-1, §10.8); REQ-001–REQ-007; AC-001–AC-008; VER-001–VER-008
- Wave B (run APP-V4-DESIGN-PASS-2-20260930, node B3; v0.8): design development under R12 (R12_RESOLUTIONS.md sha256 95f3011b436b6faa3de098059e77eac836c165e0bb98a5ed94e28918a3a749a1: R12-1…R12-4, R12-9), for S1-B items C 4, 5, 6 and 8 (SURVEY/S1-B.md sha256 eae76ecf9e941bb841fbc3a655a8e887c7684b8d47ef7728f4809992b0b6587d §1.5, §1.8), under BRIEFS.md sha256 ccb4d9f036fb7ff531fffa0d309533b15cf1ebb39b0320651ed4bd5d88efc550 ("Common rules", "Wave B", row B3), with OWNER_DECISIONS.md sha256 1dfd5bf4619b329719136b1646030e3f871fd7ffc52dbfd12265414e515aaf15 (DECISION-K1; K1-6 prototypes) and R10_RESOLUTIONS.md R10-5. P-v0.8 and ADAPTER-v0.6 were developed in the same node; other siblings are cited at their Wave A labels (below) because they were being edited in parallel. New files beside this one: `catalog.schema.json`, `edition_change_event.schema.json`, `read_result.schema.json`, their `*.example-valid*.json` / `*.example-invalid*.json` instances, and `prototype/` (SH-1 and the checks; its README states that it is not product code). **Repair RP-2 (same run, in place, no version step):** R14_RESOLUTIONS.md sha256 c6a603303693f50e24ea27fcbc9f381a297434e4182f023fbcee941073623576 (R14-7, R14-8; binding) with R13_RESOLUTIONS.md sha256 d0385313660e5820258b4089372313f382afcebc57d37265389274ca470a8d3a (R13-1) and the four receiver comparisons `comparisons/V18-1.md`…`V18-4.md` (sha256 prefixes fb07e07c66c1, 0b00e79b161b, 68a067e26af7, 078113d7055b), under BRIEFS.md sha256 e3f98d1c8449292965dd244a0f2821b221bcd0f3b0294e592f73b8eaaaaf6321 ("RP", row RP-2); siblings are named at their Wave B labels where a repair row says so
- Basis (re-pinned in Wave A, R9-5; each sha256 below recomputed with `shasum -a 256` on 2026-09-30, working tree at `3dd7c22c73`): the accepted basis as amended by SCA-V4-001 (accepted 2026-09-29) and SCA-V4-002 (in these four files, HOST_INTEGRATION line layout only) — `P/docs/HOST_INTEGRATION.md` (sha256 d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f) §§1–3, §5 V4-HI-30–33, §6 V4-HI-40–42 (V4-HI-42 amended), §7, §10 item 3, §11; `P/docs/PRD.md` (sha256 bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd) V4-HOST-02 and V4-WF-05 (both amended; cited in §4.1 and §0), V4-HOST-03, V4-EXT-01, V4-PAR-01–05, V4-AUT-03–05, V4-SHR-02, §9 OQ-02/OQ-10/OQ-11; `P/docs/ARCHITECTURE.md` (sha256 317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c) V4-ARC-20–21; `P/docs/EXAMINATION.md` (sha256 471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0) V4-EXM-20/21/24/25; ScopeOfWork.md sha256 9ada531b59a6efc007c273f131a8d51df390994ef5f379b1d523d635d3849449 (revised under SCA-V4-001, its AX-004: OUT-001, CLM-002, REQ-002, REQ-004, VER-004 and TBD-001); DECISION_BRIEF #d2/#d3/#d4/#d5; the accepted graph `_DAG/_LATEST.md` → DAG-003 (accepted 2026-09-29); SCC-CASE-002 Case_Datasheet rows M1-C, M3-CP, M4-X (sha256 a12abfaf82c34ae1e7c10d8b553d3e1a0da4772b160e02257c0bf70edce04d5c; additions only since the state pinned below); owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (OWNER_DECISIONS.md sha256 a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c, the state that also carries DECISION-2; the DECISION-1 text is unchanged) D2/D3. At v0.6 this line pinned repo 6e18505e3, ScopeOfWork.md 179a6d355d84dba915daddd746d9d62eb7c8ef483e68122a096dfbde6f6b3b84, HOST_INTEGRATION.md 08c8fc7d…60da and Case_Datasheet 6acdc6c4…a71a6, each true at `6e18505e3`, and OWNER_DECISIONS.md f3f8e5f3…81f2e, true at `be8bb46dd3` (history). Rulings, by file: R1_RESOLUTIONS.md (sha256 2f9c7e72…7ec4) R-1–R-9; R2_RESOLUTIONS.md (sha256 77cfb845…d088) R2-1–R2-21; R3_RESOLUTIONS.md (sha256 202d52c7…afbf) R3-4; R4_RESOLUTIONS.md at `f05c7e4cd` (sha256 50a009b2…2a24) R4-1, R4-13, R4-16, R4-18–R4-20; R5_RESOLUTIONS.md at `8fb51f07f` (sha256 254d0b93…d6f1) R5-1, R5-2, R5-4, R5-7, R5-9; R6_RESOLUTIONS.md (sha256 8703e85aa7324e233fab285321e277d720923d3e36e342c865917b55083cb841) R6-2, R6-4, R6-5; R7_RESOLUTIONS.md (sha256 1f6ab3b2355e164f803657ceae08841af92d21a821feede3800a6df861b2a1ea) R7-4; R8_RESOLUTIONS.md (APP-V4-SWBPIPE-INTAKE-20260928; sha256 44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b) R8-1…R8-13; R9_RESOLUTIONS.md (APP-V4-DESIGN-PASS-2-20260930; sha256 a64e241519b7d158165a7ede0ffdd22eec0af15b6812b5300755f5f38abd59b8) R9-1…R9-11, with that run's R10_RESOLUTIONS.md (sha256 ad3b6caa4a12660db77abc51b5c02ba70519ee46d55b40d21ee76eb3ca561796) R10-1…R10-11, R11_RESOLUTIONS.md (sha256 e7343b6663b6aeeb2dc506d3391f5b310088e7688d1b21e65d2ba1d8616b3615) R11-1…R11-9 and OWNER_DECISIONS.md (sha256 7458e9e81971676337a34280b4e8b29a7d04fce5fc202da5b9f5cf7ccd8f9ae5) DECISION-K1 (these four recomputed with `shasum -a 256` at node A4, R11-3, at their final bytes; the R9_RESOLUTIONS.md pin in the node A1 input line below records the bytes A1 read) (R1…R5 pins recomputed: current); reviews V3-A (sha256 f25f5af1…1d87) and V3-B (sha256 5662fbd0…54a3) minors addressed to C; OWNER_DECISIONS DECISION-2 D5 (via R4-1); review V2 (sha256 75ba1dff…e6ef) m-5, m-8, m-12; comparisons V1-A (01811533…4c09), V1-B (09eebfe0…1cae), V1-C (8d46258a…94a6); reviews IR1-A (31b3c7f8…8284), IR1-B (70e4a4f6…2846), IR1-C (295e96b3…26b9)
- Consumed inputs: **Wave A inputs (run APP-V4-DESIGN-PASS-2-20260930, node A1-B; v0.7).** R9_RESOLUTIONS.md sha256 c3efe2ffa232dd9293202d4fc891eba4325afeb2e224fecdf8c1b4c5122a9d2c (R9-1…R9-11; binding); that run's BRIEFS.md sha256 698d91d8217cee528812529fa353faac899b4bc1a5be5686552ad88dad6c469a ("Common rules", "A1 — alignment wave"); SURVEY/S1-B.md sha256 eae76ecf9e941bb841fbc3a655a8e887c7684b8d47ef7728f4809992b0b6587d (advice; each item was checked against the current source before it was applied); the amended basis documents and the revised ScopeOfWork.md as pinned in Basis; SCA-V4-001 AMENDMENT_PACKET/OWNER_ITEMS.md sha256 2b90eb4a95f458e993eed69e27533aa10e31aea980fe2ec99c9c2345e6f498ef items O-4, O-10 and O-25, accepted "as recommended" (APP-V4-BASIS-ALIGN-20260928 OWNER_DECISIONS.md sha256 ca8c4e50df1d7dddb41b875a4afe46eea4f1a1bf2491d255b7890d0d71cd254b, DECISION-7); this deliverable's `Dependencies.csv` and the consumers' registers (ACTIVE rows, read 2026-09-30, for the Receivers line; R9-6); `_DAG/DAG-003/HANDOFF_STATE.md`. SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` is cited at sha256 afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74 (current; three lines differ from the 6f01add3…61c7 state read for v0.6, below) and `FACTS_SQ01_SQ32.md` at sha256 733fb88a701317be8f0054937eca058774ba5f5f30c7a27233718996e8b2ab7e; both are data about SWBPIPE's current state, not commitments (DECISION-3). Sibling Design files are cited by version label and section only (R9-5), at their Wave A versions (R9-11): DEL-02-03/EXEC-v0.5; DEL-02-01/WD-v0.7; DEL-02-01/WD-EX-v0.7; DEL-03-02/P-v0.7; DEL-03-03/ADAPTER-v0.5; DEL-03-04/GUIDE-v0.4; DEL-04-01/ACT-POLICY-v0.7; DEL-04-02/AS-v0.7; DEL-04-03/RS-v0.7; DEL-05-01/LOOP-v0.7; DEL-05-02/PANEL-v0.7; DEL-01-01/HOSTING-BOUNDARY-v0.7; DEL-01-01/PIN-SPIKE-v0.1; DEL-09-06/CA-v0.5; DEL-09-09/XT-v0.5; DEL-09-06/RELAY-v0.3. P and ADAPTER were aligned in the same node. The other siblings were edited in parallel by other Wave A nodes, so their Wave A bytes were not read here; the sections this pass compared were read at the preceding versions (RS-v0.6 §6.1 and §7; ACT-POLICY-v0.6 §8.1). Sibling byte pins live in GUIDE's input table alone. **Earlier passes (history; true as recorded at each pass, not re-pinned in Wave A).** **R8-13 pass (node B1; in place, no version bump).** R8_RESOLUTIONS.md sha256 44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b (R8-13) at `1528a5033`, and OWNER_DECISIONS.md sha256 5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2 (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`: V4-HOST-02, host-agent network destinations) in its later state that adds the owner's DECISION-5 confirmation (committed with that pass; the sentence was reordered at v0.7 per V10 N-1, no value changed); BRIEFS.md sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517 ("Common rules", "A-wave"). Revised in the same pass (node B1), versions unchanged: LOOP, PANEL, ACT, AS, RS, HOSTING, C, ADAPTER and GUIDE; their byte pins are in GUIDE-v0.3's input table. **R8-12 closing pass (node A6; in place, no version bump).** R8_RESOLUTIONS.md sha256 d4c3423310a857af86692d17ddfdd22fa877ee20b07c46e1ee481d1cd750e7af (R8-12: item 7 applied here; item 3 confirmed). Current sibling versions after R8, as committed at `7a1508452` with A6's in-place R8-12 edits (their byte pins are in GUIDE-v0.3's input table): DEL-02-03/EXEC-v0.4; DEL-02-01/WD-v0.6; DEL-02-01/WD-EX-v0.6; DEL-03-02/P-v0.6; DEL-03-03/ADAPTER-v0.4; DEL-03-04/GUIDE-v0.3; DEL-04-01/ACT-POLICY-v0.6; DEL-04-02/AS-v0.6; DEL-04-03/RS-v0.6; DEL-05-01/LOOP-v0.6; DEL-05-02/PANEL-v0.6; DEL-01-01/HOSTING-BOUNDARY-v0.6; DEL-01-01/PIN-SPIKE-v0.1; DEL-09-06/CA-v0.4; DEL-09-09/XT-v0.4; DEL-09-06/RELAY-v0.3. SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` and `FACTS_SQ01_SQ32.md` are unchanged (data about SWBPIPE's current state, not commitments; DECISION-3). **v0.6 inputs (R8 pass, node A3, at `94aa9181b`).** R8_RESOLUTIONS.md sha256 1770c96e62caf14322811fca82ceb77eca450d3e1be8665cdbdd5550631e8d02 (R8-1…R8-11; binding); INTAKE_MAP.md (I2) sha256 3cc182955c0f3dd70efa0f1c051870229c2ccc08f36c5cf1445f2eef0dd1ea33: rows 01.6, 02.6, 03.1, 03.2, 04.4, 05.7, 07.1–07.5, 08.1, 09.3, 09.4, 10.2, 11.1, 12.2, 13.3, 16.7, 18.2, 19.7, 21.1, 22.2, 24.1, 26.1; Part 2 P2.1, P2.4 and its §2.2 C rows; Part 3 items 2–5, 9, 12; Part 4.1, 4.3, 4.7, 4.9, 4.11 (R8 overrides I2 where they differ); BRIEFS.md sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517 ("Common rules", "A-wave"); owner decisions DECISION-3 and DECISION-4 with its clarification (OWNER_DECISIONS.md sha256 a5ccab0d39bd1cab37c5556abc9bdedd5341ce76be4712706c8c9d72d623e776); SWBPIPE's delivered answers `RELAY_ANSWERS_SWBPIPE.md` (DEL-09-06 `Design/`, #1047) sha256 6f01add3977761e42ac6b310faf72ba4fd5455e478605deb83fefb2e4d3a61c7: SQ-01…SQ-13, SQ-16, SQ-18…SQ-24, SQ-26, SQ-28, SQ-31, ANS §2–§3 — data about SWBPIPE's current state, not commitments (DECISION-3). **Owner files read first (at `94aa9181b`):** DEL-02-03 EXEC-v0.4 `EXECUTION_COMPATIBILITY.md` sha256 d32be37797a3c367d342a2d13bbb8dd4279bc52934531d83b8c6ec8c6e7b76d4 (§2.1 PH-1…PH-10; §2.2 GV-1…GV-5; §3.4 EV-4; §3.5; §3.6; §3.7 CC-2; §4.5 SP-4; §4.11 receiving notes; MT-2, MT-14, MT-16, CH-17, CH-27); DEL-02-01 WD-v0.6 `WORKFLOW_DECLARATION.md` sha256 fce565edfd0cee3fa4583eb292d11cce3e4121ead0cdbed31ba2fe0a52562f28 (§4.3.0 CG-1…CG-7; §4.3.1 `governed`, PROPOSED); WD-EX-v0.6 `EXAMPLES.md` sha256 950b70b2e3f7fdda9a98b13a63746b76936be490dd96cb6e47bbe6dc9c3eba3d (E8; the governance-phase reading "as if declared governed"). DEL-03-02/P-v0.6 is co-revised in the same pass (node A3). Earlier: at `8fb51f07f`, DEL-02-01/WD-EX `EXAMPLES.md` (sha256 60ce307a…28ca4: E1d `label-with-grant` and R-16) for V-GR1; the EXEC-v0.2, ADAPTER-v0.2 and XT-v0.2 texts were **not** read for this pass (their v0.1 texts, below, remain the recorded basis; V3-B Y-7 note); DEL-03-02/P-v0.5 (co-revised in this pass). Earlier: Wave-2 sibling texts read from commit `f05c7e4cd` — DEL-02-03/EXEC-v0.1 `EXECUTION_COMPATIBILITY.md` (sha256 e0ede76e…18e8: F-15, CH-23, RT-6–RT-8), DEL-03-03/ADAPTER-v0.1 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` (sha256 58b2409c…a074: F-1, F-2, F-4, F-7, F-8), DEL-09-09/XT-v0.1 `EXTERNAL_TRACE_CASES.md` (sha256 8f098c79…f1df: §4.1 L-XT-1, F-5), DEL-02-01/WD-EX-v0.3 `EXAMPLES.md` (sha256 0f1058d7…d018d: E1 checkpoint table); DEL-03-02/P-v0.4 (co-revised in the A1 sweep); earlier: DEL-03-02/P-v0.3 (co-revised: change-item content identity, canonical outcome taxonomy, applied-outcome association with resulting objects, retry precedence, item-left events, M3-CP return); sibling v0.2 texts read from commit `28bd00499` where an R2 ruling touches a join — DEL-04-01/ACT-POLICY-v0.2 `ACT_AND_POLICY_CONTRACT.md` (sha256 e50f1fe2…93a9: §2.1 act names, §5.1–§5.3 class vocabulary and resolution order, §6 outcome map, §8.1 decision-standing values, §8.3 records), DEL-04-03/RS-v0.2 `RECORD_SEMANTICS.md` (sha256 56a3f839…1c69: §7 L-1–L-12 and lapse states), DEL-05-01/LOOP-v0.2 `LOOP_RECEIVING_CONTRACT.md` (sha256 1151d432…62c9: §6.2 dispatch record, §12 evidence labels), DEL-02-01/WD-v0.2 `WORKFLOW_DECLARATION.md` (sha256 c25bccc5…a55c: §4.3.7, §4.4 promised standing), DEL-05-02/PANEL-v0.2 (sha256 0a8a0dbe…a700; evidence-label lines only), DEL-04-02/AS-v0.2 (F9 row only, grep); SWBPIPE host catalog: not supplied (DEP-03-01-025)
- Receivers (rebuilt at v0.7 from the ACTIVE rows of this register and of the consumers' registers, as read 2026-09-30; R9-6. A row names a required contribution, not its delivery. The bracketed OUT/REQ/VER tags are carried from v0.6 unchanged): DEL-02-01 [OUT-002; REQ-002; VER-002] — open capability-catalog tool descriptors for required-tool declarations (DEP-02-01-017) — and PKG-02 at package level (DEP-03-01-022); DEL-02-03 [OUT-001; REQ-001; VER-001] — catalog semantics for required-tool checks (DEP-02-03-011); DEL-03-02 [OUT-001, OUT-002; REQ-003; VER-004] — operation identity and the original relied-on read basis (DEP-03-02-016; mirror DEP-03-01-023); DEL-03-03 [OUT-001, OUT-003; REQ-001; VER-001] — catalog/read-basis definitions and availability/read-standing expectations (DEP-03-03-006); DEL-03-04 — the definition and the §8 map, for the integrated guide (DEP-03-04-005); DEL-04-02 — read-basis and standing facets (DEP-04-02-016); DEL-04-03 — subject content identities and method designations (DEP-04-03-023); DEL-05-01 [OUT-001, OUT-002; REQ-003; VER-004] — "the adopted capability-catalog/read-basis schemas and catalog identity" for loop argument validation (DEP-05-01-014): the schemas are named by that row and not yet defined here (this file gives semantic meanings only; OUT-001, TBD-003), and the catalog identity is the catalog edition (§2; PROPOSED); DEL-05-02 [OUT-001, OUT-003; REQ-001; VER-001] — catalog/read-basis meaning (DEP-05-02-006); DEL-09-06 — catalog/read-basis meanings for the connected activity (DEP-09-06-027); DEL-09-09 [OUT-001, OUT-002; REQ-001, REQ-005; VER-001, VER-005] — the contract, the operation/model basis and the responsibility map (DEP-09-09-007); outside the 14 first-increment deliverables, DEL-10-03 — catalog/read-basis obligations for the shared responsibility account (DEP-10-03-011). The two joins that C-v0.6 called unregistered (DEL-04-03, DEL-04-02; V1-B RF-04/RF-05) are registered on the consumer side. This register carries DOWNSTREAM rows only for PKG-02 (022) and DEL-03-02 (023); the other supplier-side mirror rows are deferred (DAG-003 HANDOFF open matters). By join, with no register row: DEL-04-01 (fixture re-pointing); every file citing the §10 shared fixture catalogue (R-9; R2-21). Arcs N-18, N-21, N-24 and X-1 do not touch this deliverable

## 0. How to read this definition

This is the 60% semantic definition of one host capability catalog and of
the basis every read describes. It fixes meanings, states, sequences, failure
behavior and verification cases. It does **not** select wire field names,
JSON/TypeScript types, MCP versus CLI transport, a hash or canonicalization
algorithm, persistence, process placement or shared-component placement
(TBD-003; OI-014; DEP-03-01-028). Every element name in this file is a
**semantic label**, not a wire name. Where a meaning depends on a host fact
not yet supplied (DEP-03-01-025), it is marked as a host input.

**Schemas and the simulated host (Wave B; R12-1…R12-4; PROPOSED).** Three
formats this file owns are also written as JSON Schema (draft 2020-12)
beside it: `catalog.schema.json` (a catalog edition as discovered, §2.1,
§3, §3.4, §3.5), `edition_change_event.schema.json` (§2.1 CI-4) and
`read_result.schema.json` (§4.1, §4.2, §5.1, §6.1–§6.4). Each has valid and
invalid example instances. The schemas are conformance fixtures of the
semantic meanings, which every placement option needs (R12-2). Their
property names are Chirality's semantic labels in `snake_case`. They do not
select a host or supplier wire field, a transport, a hash or
canonicalization algorithm (identities stay opaque strings) or a placement
(OI-014); "does not select JSON types" above therefore means no **wire**
type is selected. The one simulated host, **SH-1**, is specified in §10.8
and cited by P, ADAPTER and XT (R12-4).

Unruled policy appears only as `UNRESOLVED{OI-nnn}`. It is never a
permission, a default or a pass. Values marked **DERIVED** follow from cited
rules; **INTEGRATION** values are R1/R2 integrator choices open to owner
revision; **PROPOSED** values are this contribution's proposals. Owner
rulings are credited only with what they say (R2-11).

**Phase (V4-WF-05 and V4-HI-42 as amended by SCA-V4-001, SETTLED; DECISION-4
D4-1; R8-1; R9-1).** This file summarizes the amended texts in the R9-1
wording:

> When a run reaches a declared checkpoint, the required human act is requested, and it is recorded as done only when the person performs it, whatever the autonomy setting. Holding the run at the checkpoint until the act is performed is phased to the governance layer: in the current phase a checkpoint is plan guidance that the person and the agents manage, and neither the App nor a host's embedded loop enforces a hold, blocks a run, or reports a workflow unsupported because a hold cannot be enforced. The reserved acts (V4-HI-30) still bind.

In force in every phase: the act is requested; it is recorded as done only
when the person performs it; the reserved acts bind (EXEC PH-4, PH-5).
Phased to the governance layer: holding the run until the act (EXEC
PH-1…PH-3). The required-tool check is unchanged.

**Who requests, in the current phase (R9-1; SETTLED by DECISION-K1 K1-1,
the owner's decision of 2026-09-30 confirming R9-1's reading of DECISION-4).** The agent carrying out the
workflow asks the person for the act when its work reaches the checkpoint.
The product gives the agent the declared checkpoint with the workflow,
offers the person the means to perform the act, and records what it
observes: the checkpoint's identity, the request where it can be
identified, and the act only when the person performs it. Neither the App
nor a host's embedded loop issues the request in the agent's place, pauses
the run, or otherwise reacts to the arrival. How an App run observes an
arrival and a request, and what the record then holds, is defined in
EXEC-v0.6 §2.4–§2.5; this file states the ruling and adds no mechanism.

Hold support, the governing checkpoint constraint and its carriage assurance
(R2-12) are the **governance-phase definition, retained** (EXEC GV-1), for
checkpoints declared **`governed`** (WD-v0.8 §4.3.1, PROPOSED). Where this
file states a checkpoint case, it gives the Phase-1 result and the
governance-phase value. The governance-phase values read the fixture's
checkpoints as if they were declared governed; no fixture declares the flag
(R8-11 item 5; EXEC GV-5).

**SWBPIPE answers (R8; DECISION-3).** Notes marked *SWBPIPE (SQ-nn)* record
SWBPIPE's delivered answers as data about its current state, with their
SWBPIPE standing where it matters (FACT, DRAFT #885, DESIGN). They are not
commitments, deliveries or adoption, and host joins stay deferred. **OI-003**
in this file is the App v4 open issue (the extension promise); it is
unrelated to SWBPIPE's own OI-003 (R8-7; SQ-26).

Settled distinctions relied on here (cited, not re-decided):

| Id | Settled distinction | Source |
|---|---|---|
| S-C1 | One catalog describes every operation a person can perform, reads and changes alike | V4-HI-01; V4-PAR-01 |
| S-C2 | Human interface, embedded agent and external agent act through that one catalog; equal UI gestures are unnecessary, equal meaning and standing are essential | V4-PAR-02; V4-HOST-03; #d4 |
| S-C3 | Unavailable to the person ⇒ unavailable to the agent, with the same reason | V4-HI-04 |
| S-C4 | Every read returns its basis; a later action cites the basis it relied on; the basis is checked on every change | V4-HI-11; HI §10 item 3 |
| S-C5 | Results carry standing; an agent never presents more confidence than the host gives | V4-HI-12; V4-PAR-03 |
| S-C6 | Operation success means it ran; execution, checking, acceptance, approval and professional reliance are separate acts | V4-HI-25; V4-AUT-03; #d3 |
| S-C7 | Agents never record a human act as performed when it was not; faithful recording (A9) of an actual act is a conformant record shape | V4-HI-31; SoW REQ-005; R-5 |
| S-C8 | A human act binds to the content it concerns and lapses visibly when that content changes | V4-HI-32 |
| S-C9 | The all-actor/no-separate-work extension promise is preserved and undecided | V4-PAR-05; V4-HI-03; App v4 OI-003 |
| S-C10 | Reserved to the person (App/shared contracts, first increment), **adopted** by D2: A4 mark checked; A5 accept wherever the active autonomy requires a proposal; A6 approve; A7 rely; A12 changing the autonomy grant; A13 enabling external-agent access. No grant widens past a reserved act or a declared checkpoint. **Current phase (R8-11 item 2 as restated by R9-2, DERIVED; the R8-11 reading was confirmed by the owner at SCA-V4-001 OWNER_ITEMS O-25):** D2's "no autonomy grant widens past a reserved act" binds, and the host enforces it through its operations. For a declared checkpoint, V4-HI-42's request clause and record clause are in force whatever the autonomy setting; whether the run goes on before the act is for the person and the agents in the current phase, and the host's own treatment of its operations decides what the host does. A forced *propose* (§3.1 rule 3) and a hold apply only to governed checkpoints in the governance phase. The host names and enforces its own list; host adoption is not evidenced (SWBPIPE, SQ-05: no named reserved list; every change waits for the person's Apply). **DERIVED**: A10 reject is reserved wherever A5 is (R-1). **INTEGRATION**: disabling external access is also a person's A13 (R2-3) | D2; R-1; R2-3; V4-HI-30; V4-HI-42; DEP-001; R8-11; R9-2 |
| S-C11 | **Adopted** by D3: App routine tool-permission and sandbox modes remain the user's own Codex setting per project/turn, govern tool execution only (A14) and never stand in for a reserved or professional act; hosts have no classifier permission mode in the first increment; the SWB default proposal mode applies. The App-side restriction on answering A14 is R-2 INTEGRATION, not D3 | D3; R-2; R2-11; V4-HI-41 |

Act names used below are the canonical R-1 names (A1 propose … A14 answer
tool permission), as carried by DEL-04-01 §2.1, with A15 register workflow
revision (R12-5; ACT-POLICY-v0.8 §2.1), a person's act that no checkpoint
may require in this increment and that no catalog entry of this file
performs.

## 1. Parties and what this contract does not do

| Party | Contribution relevant here |
|---|---|
| App/shared capability-contract owner (DEL-03-01) | This semantic definition, the responsibility map, contract fixtures, the shared fixture catalogue (§10) and the simulated host SH-1 (§10.8; a test double serving several deliverables, like §10, not SoW scope) |
| Host owner (SWBPIPE outside session for the first host) | Actual catalog, domain objects and truth, tables/results/diagnostics, content identities, exposure, availability evaluation, validation/application, receipts, host UI and the offering/capture/recording of human acts (CLM-001) |
| DEL-03-02 | Proposal, validation and outcome meaning; canonical outcome taxonomy (P §9); consumes §§3–7 here |
| DEL-04-01 | Canonical act names, class vocabulary and records (D2/D3; P-01…P-06), treatment → outcome map; carried into §3 element 8 |
| DEL-04-02 | Autonomy grant display states and standing display; consumes §6 |
| DEL-04-03 | Content-bound human-act and run-record format. It consumes §5 content identities and method designations (DEP-04-03-023), and it supplies the act field set and lapse vocabulary that §6.2 carries as standing, which this contract consumes and does not define (SoW CLM-002 as revised under SCA-V4-001; DEP-03-01-031) |
| DEL-03-03 / DEL-05-01 / DEL-05-02 | External, embedded and panel receiving; they consume, not redefine, these meanings |
| DEL-09-09 | Extension trace (V4-EXM-24) and joined external witness (V4-EXM-25) |
| The person | Every actual human act |

REQ-007 exclusions are preserved: this contract builds no host catalog,
computes no domain result, validates or applies nothing, produces no receipt
and performs no human act.

## 2. The catalog as a whole

| Semantic element | Meaning | Source / status |
|---|---|---|
| Host identity | Which host application publishes the catalog | V4-HI-01 |
| Catalog edition | An identity for the whole set of entries as published at one time, so a consumer can say which catalog it generated from, offered from or checked against. The one semantic name for this element; DEL-05-01 "catalog identity" maps to it (V1-C D-27) | **PROPOSED**; not a V4-HI-02 field. Serves VER-002/VER-006 candidate recording (F-C6) |
| Entries | One entry per operation a person can perform (reads and changes) | V4-HI-01/02 |

Catalog invariants:

1. **Completeness.** Every operation available to the person in the host
   interface has an entry — including undo (§10 OP-C10) and any host check a
   person can run. An operation reachable by a person but absent from the
   catalog is a parity defect, not an agent restriction (S-C1).
2. **One meaning.** Each surface (§8) presents an entry's meaning without
   changing it. A surface may add rendering (labels, layout, gesture); it may
   not add, drop or weaken preconditions, effects, errors, standing or class.
3. **Operation identity ≠ read basis ≠ content identity.** Entry
   identity/version describe *what the operation is*. The read basis (§5)
   describes *which state a particular read observed*. Subject content
   identities (§5.3) identify *individual objects/rows* within that state.
   None substitutes for another.
4. **Open description (PROPOSED, V1-C AB-09).** Entries, their purpose text
   and their input/result/error schemas are readable by any capable consumer
   without Chirality-specific software, as the external interface already
   requires (V4-HI-50; V4-ARC-21). V4-SHR-02 states this for workflows and
   skills only; its extension to catalog descriptors is proposed (F-C9).
5. **Class never implies exposure (SoW REQ-002; R2-4; IR1-B B-M4).** Exposure is element 9,
   a host-declared per-surface fact independent of class. Class alone never
   produces *unavailable*, *missing* or *not exposed on this surface*.
   **Reserved entries are always described and, where exposed, offered**;
   they are never withheld for a class reason. An agent call to a reserved
   entry returns **not permitted** and *offers* an A8 request; no A8 is
   recorded unless the agent actually issues it (IR1A-10). Loops and adapters
   never withhold an exposed entry on their own reading of its class (LOOP
   TL-5).

**SWBPIPE's current state (R8-10; record only).** SWBPIPE has no capability
catalog in this sense. It has one engine route with 27 change kinds, no
per-operation identity or version (operation intents carry no operation
version; there is one engine crate version), no catalog editions and no
edition-addition event, and no per-surface exposure element. Its external
CLI (DRAFT #885) is hand-built and narrow, and is neither generated from nor
checked against a catalog (SQ-04, SQ-11, SQ-12, SQ-18 (e), SQ-26).
SWBPIPE's current state therefore does not meet V4-HI-02. Consequence: WD
required-tool references, which name a catalog identity and version, cannot
resolve against SWBPIPE, so each gives *not established* (EXEC §3.4 EV-4).
No App rule changes. The owner notice is U-C13.

### 2.1 The catalog as an interface (PROPOSED; S1-B C 5; R12-1)

Through C-v0.7 the catalog was a set of meanings and "discover entry" one
line of the §7 diagram. Here it is something a consumer calls. The
elements are semantic; `catalog.schema.json` and
`edition_change_event.schema.json` give their PROPOSED form.

| Id | Interface element | Request | Result | Reporter |
|---|---|---|---|---|
| CI-1 | **Discover catalog** | The surface the consumer acts on (H, E or X) | One **catalog edition**: host identity; edition identity; previous edition where the host reports one; completeness (*complete*, or *partial* with the unreadable entries named); the basis profile (CI-3); the entries, each with all nine §3 elements and the §3.4 sub-elements | Host |
| CI-2 | **Read entry** | Operation identity, and a version where the consumer holds one | The entry as CI-1 gives it, in the edition the host now publishes, with that edition's identity | Host |
| CI-3 | **Basis profile** (part of CI-1) | — | Which read-basis elements the host supplies: workspace identity, generation, model revision and canonical content identity, each *supplied* or *not supplied*; subject content identity *per subject*, *whole model only* (R8-4) or *not supplied*; and the host's staleness scope: *per item on relied-on targets*, *whole model*, or *host-stated other* with its statement (R8-3) | Host |
| CI-4 | **Edition-change event** | Host-initiated, or read as "events since ⟨edition⟩" | {host identity; from edition; to edition; entries added; entries removed; entries changed (identity, from version, to version, whether exposure changed); time; reporter *host*}. Moved here from fixture variant V-ED1 | Host |
| CI-5 | **Offering record** (consumer side) | — | {consumer; surface; edition offered from; entries offered; time}. A loop or the App offers only entries of the edition it holds. Loop-side *not offered* (§4.1) is judged against this record | The consumer: the host loop (DEL-05-01) or the App (DEL-03-03) |

Edition identity (PROPOSED):

- **EI-1** An edition identity names one published set of entries of one
  host. Two editions are the same only when host identity and edition
  identity are both equal. A consumer never infers sameness from equal entry
  lists: it computes no identity (the R8-4 principle).
- **EI-2** A host publishes a new edition identity whenever an entry is
  added or removed, an entry's version changes (§3 element 1), or an element 9
  value changes. The CI-4 event reports what changed.
- **EI-3** A new edition changes no model revision; the catalog is not model
  content (V-ED1 (2)).
- **EI-4** Every consumer record that relies on the catalog names the
  edition: the offering record, the required-tool report (EXEC-v0.6 §3.3),
  the external dispatch record (ADAPTER-v0.6 §5.1) and the loop dispatch
  (LOOP-v0.8 §6.2). DEP-05-01-014's "catalog identity" is the edition
  identity.
- **EI-5** A run is never moved silently to a new edition. A request
  prepared on an entry version keeps it (§7, first failure row); the consumer
  re-discovers before its next offering.

### 2.2 Edition states (PROPOSED)

Per edition, at the host:

| From | Event | To | Reporter |
|---|---|---|---|
| — | The host publishes the edition | published (current) | Host |
| published (current) | The host publishes a later edition (CI-4) | superseded | Host |
| superseded | — | superseded (final; still citable as history) | — |

Per consumer and host, the edition the consumer holds:

| From | Event | To | Record left | Next |
|---|---|---|---|---|
| none | CI-1 returns edition e | held current (e) | Offering record naming e (CI-5) | Offer entries of e |
| held current (e) | CI-4 observed: e → e′ | held superseded (e by e′) | The event | Re-discover (CI-1) before the next offering; requests already prepared keep their entry versions |
| held current (e) | CI-1 returns e′ ≠ e and no CI-4 was observed | held superseded (e by e′) | "Edition changed without an observed event" | As above |
| held current (e) | Discovery fails (CF-1) | held unknown (e) | The failure, with its reporter | Nothing is offered as current from e; requirements *not established* |
| held superseded or held unknown | CI-1 returns e″ | held current (e″) | New offering record | — |

### 2.3 Catalog-level failure behaviour (PROPOSED)

| Id | Situation | What fails | Who reports | Record left | What happens next |
|---|---|---|---|---|---|
| CF-1 | The catalog cannot be read (for example the supplier reports that tool discovery failed, ADAPTER-v0.6 §3.5) | Discovery | The consumer that observed it, naming itself (the App via the supplier, or the loop) | Discovery failure with its reason | Every entry and every required-tool reference on that surface is *not established* (EXEC EV-4; ADAPTER §3.2). Nothing is offered. Nothing is *missing* |
| CF-2 | The catalog is partial: the host names entries it could not describe | Those entries | Host | Edition with completeness *partial* and the unreadable entries | The other entries are usable; references to the unreadable ones are *not established*, never *missing* |
| CF-3 | The host has no catalog (SWBPIPE today, §2 note; U-C13) | Every catalog reference | The consumer (EXEC EV-4) | "No catalog: native surface only" | Native tools may be used as native tools, and every requirement on them is *not established* (ADAPTER NM-2). They are never offered or recorded as catalog entries, and no edition is recorded |
| CF-4 | A call names an entry absent from the edition offered | That call | Loop or App (loop-side *not offered*, §4.1) | The loop-side failure | Never dispatched |
| CF-5 | A read lacks a basis element | Citation of that read | The consumer | *basis incomplete* (§5.2 rule 1); except, under R13-1, a read whose only missing elements are workspace identity and generation that the host declares it does not supply: that read is citable, with the evidence limit "basis lineage not supplied" | *Basis incomplete*: not cited for a change. The R13-1 exception: cited with the limit, and comparisons across lineages read *unknown (incomparable)* |

## 3. Catalog entry meaning (REQ-002; V4-HI-02; SOW-157–164)

Each entry carries the eight V4-HI-02 semantic elements plus the exposure
element (SoW REQ-002 as revised under SCA-V4-001: "host-declared exposure
per consumer surface, independent of class"; R-9). Element names are
semantic.

| # | Semantic element | Meaning | Must distinguish | Scope row |
|---|---|---|---|---|
| 1 | Operation identity and operation version | Stable identifier for the operation, and a version that changes when any other element's meaning changes | Identity stays stable across versions; version is not model revision. Only version **equality** is defined (§3.2) | SOW-157 |
| 2 | Purpose | Plain statement of what the operation does, readable by a person and an agent alike; the same text reaches every surface | Purpose is descriptive, not a permission or a claim of result quality | SOW-158 |
| 3 | Input schema | Arguments, their meanings, units where applicable, and which argument identifies the target objects | Target identification is explicit (§4.3); a UI selection is *one way* a person supplies it, not a hidden input | SOW-159 |
| 4 | Availability | Named preconditions, each with an unavailable reason (§4) | Unavailable ≠ error ≠ empty success ≠ not permitted ≠ not exposed. See §4.4 for precondition vs validation error | SOW-160, SOW-166 |
| 5 | Effects | Kinds of objects the operation changes, or *none* | *None* ⇒ read (includes non-mutating examinations and host checks); any effect ⇒ change, routed through DEL-03-02 | SOW-161 |
| 6 | Result schema including standing | What a successful execution returns, and the standing elements (§6) that accompany it | Result ≠ acceptance; standing is part of the result | SOW-162, SOW-169 |
| 7 | Errors | Every error the operation can return, each with a stable error identity and meaning, including an effect statement (none / partial / unknown) | Error ≠ unavailable. An error at validation is P §9 *refused — invalid*; during application it is *application error*; one whose effect is unobservable routes to *outcome unknown* | SOW-163 |
| 8 | Human-act / autonomy class | §3.1 | — | SOW-164 |
| 9 | Exposure per surface | For each of H, E, X (§8): *exposed*, *not exposed on this surface*, or *unagreed*. Host-declared | Independent of class (§2 inv. 5). *Not exposed on this surface* ≠ *missing* ≠ *channel not enabled*. Tied to OI-003 | SoW REQ-002; R-9; V1-C D-09 |

### 3.1 Class element (element 8)

| Sub-element | Meaning |
|---|---|
| Class value | One of five (R2-1): **none**; **may apply within granted autonomy**; **proposal only**; **reserved to the person** — the four V4-HI-02 values (vocabulary SETTLED by V4-HI-02) — and **no policy basis** (SoW REQ-002 as revised under SCA-V4-001: "represent an operation without an adopted class explicitly (no policy basis)"; named by R-3.5/R2-1) |
| No-policy-basis reason | Present only with *no policy basis*: **omitted** (no class stated), **unassigned** (stated but no policy record), or **pending OI-021** (operation-specific addition awaited under `UNRESOLVED{OI-021}`) |
| Policy record reference | The DEL-04-01 policy-class record (e.g. P-01…P-06) and its policy revision identity, citing its decision basis (for D2/D3: `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`) (V1-A AB-07) |
| Value standing | Mirrors DEL-04-01 §8.1 *decision standing* (IR1-B B-m12): settled-by-basis · adopted decision · DERIVED · accepted default (host adoption unevidenced) · INTEGRATION · PROPOSED · `UNRESOLVED{…}` (ACT-POLICY-v0.8 §8.1 lists PROPOSED; it was missing from this list through C-v0.6) |
| Consequence statement | The operation's consequence in DEL-04-01's consequence vocabulary. Vocabulary not yet defined: `UNRESOLVED` (DEL-04-01 U-02 with host policy owner) |
| Host adoption | Whether the host has adopted and enforces this value. Not evidenced for SWBPIPE (DEP-001); the host names and enforces its own list (V4-HI-30). SWBPIPE (SQ-05): no class system and no grants; every change requires the person's Apply (hard-coded); its autonomy is SWBPIPE owner decision OI-016. The class values here stay App/shared meaning |

Class rules:

1. **Act-performing operations are reserved (R2-2, DERIVED).** An operation
   that *performs* A4, A5, A6, A7, A10, A12 or A13 — including one that
   changes the host's own act state — is **reserved to the person** (S-C7 +
   D2; DEL-04-01 P-02 with A10 added). No faithful record (A9) is made
   through such an operation. A host-offered faithful-record operation, if
   any, must: not change act state; cite capture evidence; never satisfy a
   checkpoint; take ordinary policy. Whether any host offers one is a DEP-001
   relay question (U-C11).
2. **SWB model changes (DERIVED, R-2; DEL-04-01 P-03).** Class **may apply
   within granted autonomy**, derived from V4-HI-41 "the person may widen
   it", with the accepted default setting **propose**. Operation-specific
   additions are pending `OI-021`. Not SWBPIPE adoption (DEP-001).
3. **Acceptance checkpoints force proposal (R-5; R2-12) — governance phase
   (retained; R8-1).** For a **governed** checkpoint whose constraint is
   carried **host-held** (P §3.3), whatever the class and grant, an
   operation whose result the checkpoint requires A5 on is treated *propose*
   for that run; a direct request is *not permitted*, naming the governing
   checkpoint constraint (P §3.3, §4.4). **Phase 1 (R8-11 item 2 and
   R8-12 item 2, as restated by R9-2; EXEC CH-27):** WD I-7 is plan
   guidance. The agent proposes such an operation and never adds a field
   the host schema lacks (R8-10). A direct request, if made, meets the
   host's own treatment, and nothing is reported *not permitted* on the
   constraint's account. When the active grant lets the host apply
   directly, no proposal arises and the host may apply. An A5 checkpoint
   whose reached-when is *proposal queued* is then **not reached**:
   nothing is requested by reason of an arrival that did not occur, no A5
   is forced, and none is recorded; the record shows the direct
   application under the person's grant (R9-2 as corrected by R10-1).
   V4-HI-42's request clause applies to a checkpoint the run reaches: where
   a checkpoint of any kind is reached while a grant permits direct
   application, its act is requested and its disposition is *waiting*
   ("reached; act not yet recorded") until the person performs it. SWBPIPE
   resolves every change
   reached externally as a proposal awaiting the person's Apply (SQ-02
   related fact; SQ-05); that is a property of its route, not host-held
   carriage (R2-12).
4. **No policy basis (R2-1, R2-9; DEL-04-01 P-06, INTEGRATION).** Direct
   application is **not permitted**; proposing is available but confers no
   permission — any effect requires the person's A5 and host application. An
   A12 that would widen such a class to direct is **refused** (reason: no
   policy basis). Dependent production stays held (SoW REQ-004 hold); fixtures
   report such cases as **held**, never as passes.
5. **Routine tool permission is not a class value.** A14 and App Codex
   permission/sandbox modes govern App-side tool execution only (S-C11).
   `OI-002` is not a class value; hosts have no classifier mode (D3; V1-A
   D-23).
6. **Reads and host checks.** Non-mutating reads, examinations and host
   checks carry class **none** in the fixtures as a fixture assumption
   (value standing: INTEGRATION for fixtures only); the host's adopted
   assignment governs. DEL-04-01 §5.3 rule 8 cautions that *none* does not by
   itself imply no effect.

### 3.2 Version compatibility (V1-C AB-08, PROPOSED)

Only version equality is defined. No ordering or range is implied by a
version value. A consumer requiring version *v* accepts only *v* unless the
host publishes an explicit **compatibility statement** for the entry (e.g.
"v3 accepts arguments and yields results meaningful to v2 consumers"). The
statement is host-authored; whether hosts provide one is U-C9.

### 3.3 Change-entry extras (for DEL-03-02)

| Semantic element | Meaning |
|---|---|
| Relied-basis requirement | The change must cite the basis it relied on (S-C4); DEL-03-02 defines how |
| Old/new value reporting | Which attributes of affected objects the host view will show as old and new (V4-HI-24), so the proposal can carry them |
| Subject content identity availability | Whether affected objects expose subject content identities (§5.3), which DEL-03-02 change-item content identities, the per-item basis check (R2-13 as amended by R8-3) and DEL-04-03 lapse rely on. A host that supplies only a whole-model identity is received per §5.3 (R8-4) |
| Resulting-object reporting | Whether the applied outcome identifies created/changed objects and their post-application subject content identities (R2-14; P §9) |

### 3.4 Two entry sub-elements (PROPOSED; S1-B C 4)

The nine elements stay nine. Two sub-elements are added:

- **Element 6, named host checks.** The names of the host checks the
  entry's result can carry. Only a check named here appears in a result as
  "host checks passed: ‹name›" or "host check failed: ‹name›" (§6.2). The
  fixture entries: OP-C1 and OP-C2 name `equilibrium` and `unit
  consistency`; OP-C12 names `support spacing`; OP-C3 names none, because
  its result is the requester's findings (A3). OP-C3 and OP-C12 now differ
  in the entry, not only in fixture prose.
- **Element 3, accepts a requested basis.** Whether the entry admits an
  earlier basis as an argument, which makes a requested historical read
  (§6.4). The default is *no*. In SH-1 (§10.8) OP-C1 says *yes*.

Two more are added by node B5 (v0.8; PROPOSED), for a host's agent's
network destinations. The one account of that flow is DEL-05-01/LOOP-v0.8
§5.3 (DF-1…DF-10), which ACT, AS, RS, PANEL, P and ADAPTER also cite.

- **Element 5, external-contact declaration.** An entry that reaches a
  network destination for a host's agent declares it: the destination
  **category** (web access · MCP servers · other APIs · …; the list is
  open, DECISION-5); the **destination form**, *fixed* (the named
  destinations) or *from argument* (the argument whose value names the
  destination; for web access and other APIs its origin is the destination,
  LOOP DF-2); and, where an outside process serves the entry, **that
  process** (for an MCP server, its server identity). The category is the
  host's declaration, never the agent's. An entry without the declaration
  declares no network contact. The loop checks a declared destination at
  **V-D**, after V-3 and before dispatch (LOOP DF-4). An MCP server's tools
  reach a host's agent only as entries of this catalog with this
  declaration: the catalog stays the one tool source (V4-ARC-13; LOOP G-13).
- **Entry kind *destination request*** (the **destination request entry**). The host supplies, on the embedded
  surface (element 9: *exposed* on E only), one entry through which its
  agent asks the person for a network destination: the agent's A8 (ACT
  §2.7). Class *none*; effects *none*; no external-contact declaration; it
  contacts nothing and changes no host object. Its arguments: target
  category; target destination (optional: absent asks for the whole
  category); purpose; scope sought (once · this run · always); and the
  **carried call** (value kind *carried call*: the operation reference and
  argument text of one call to an entry with an external-contact
  declaration), required for scope *once*. Its result is an interim notice
  and then one deferred result (LOOP DF-5, DF-6; §4.1). `catalog.schema.json`
  carries both (`entry_kind`; `effects.external_contact`); examples
  `catalog.example-valid-2.json` (a web fetch, an MCP-served entry and the
  request entry) and `catalog.example-invalid-2.json` (a request entry that
  declares contact; a *from argument* declaration without its argument).
  Since the RP-2 repair (V18-3 m-15, R-7) the schema also refuses a request
  entry exposed on H or X, or one without a carried-call argument, and
  `catalog.example-invalid-3.json` shows these two together with a
  CX-1 breach (§3.5).

### 3.5 Required elements and cardinality (PROPOSED; S1-B C 6)

`catalog.schema.json` and `read_result.schema.json` carry this in full. In
summary:

| Structure | Required, exactly one | Required, zero or more | Optional | Conditional |
|---|---|---|---|---|
| Catalog edition (§2.1 CI-1) | Host identity; edition; completeness; basis profile | Entries | Previous edition | Unreadable entries (one or more) exactly when completeness is *partial* |
| Entry (§3) | Operation identity; operation version; purpose; input (the argument list, and "accepts a requested basis"); effects kind; result (content kinds, one or more); class; exposure for each of H, E and X | Arguments; preconditions (element 4); errors (element 7); named host checks (§3.4) | Compatibility statement (§3.2); entry kind (§3.4, node B5); external-contact declaration (§3.4, node B5) | Effects kind *change* requires affected object kinds (one or more) and whether resulting objects are reported. An external-contact declaration requires its category and form, and the destinations (*fixed*) or the argument (*from argument*). Entry kind *destination request* requires class *none*, effects *none*, no declaration (node B5), exposure *exposed* on E and not on H or X, and an argument of value kind *carried call* (RP-2) |
| Class (element 8, §3.1) | Class value; value standing; host adoption | — | Consequence statement (empty until DEL-04-01 U-02) | *No policy basis* requires its reason and has no policy record; every other value requires the policy record reference and has no reason |
| Basis descriptor (§5.1) | Each of the five elements, as a value or as an explicit *not supplied* marker (*host declares none* or *omitted*); an element is never left out | — | — | — |
| Unavailable reason (§4.2) | Reason identity; statement; failed precondition; evaluated basis | — | Remedy | — |
| Standing (§6.2) | Currency | Host checks; known limitations; human-act evidence | Agent findings | — |

**Conformance rules beyond the schema (PROPOSED; RP-2, V18-3 R-7 and n-3).**
A JSON Schema cannot compare one property with another, so these are
stated here and checked by `prototype/validate_all.py` on every catalog
instance (examples and SH-1 documents):

- **CX-1** An external-contact declaration of form *from argument* names an
  argument of the same entry.

**Class of OP-C10 (V18-3 n-2; NOTE, recorded, not resolved).** OP-C10's class
follows the policy record of the operation whose receipt it reverses (R3-4),
so it is a property of each request, not one value of the entry. The class
element (§3.1) and `catalog.schema.json` have no form for it. SH-1 does not
implement OP-C10 (§10.8), so nothing relies on one yet; the form is left to
the next development of the class element.

## 4. Availability and non-success results (REQ-003; V4-HI-02/04; SOW-160, SOW-166)

### 4.1 Distinct non-success results (canonical with P §9)

A request can end, before or instead of execution, in one of the following.
They must never be encoded as one another, and none may be encoded as a
successful empty result. Every one carries the **evaluated basis** where the
host evaluated one (V1-B D-21). DEL-03-02 P §9 carries the proposal/outcome
extensions; DEL-04-03, DEL-05-01 and DEL-05-02 adopt both unchanged (R-7;
**as of C-v0.5 / P-v0.5, carried in C-v0.7 / P-v0.7**; C-v0.8 adds the two
destination rows below and P-v0.8 two §9 rows). DEL-04-03 receives the two
destination rows as its R15 destination entries, not as R7 operation
outcomes (RS-v0.8 §4 R15: *boundary refusal*, *destination request closed*,
*destination declined*); RS §5 is to say so (V18-1 m-8).

| Result | Reporter | Meaning | Carries |
|---|---|---|---|
| **Unavailable** | Host | A declared catalog precondition (element 4) does not hold for this basis and these arguments. The **only** result subject to HI-04 parity | Failed precondition identity; unavailable reason (4.2); evaluated basis |
| **Not permitted** | Host | Available and exposed, but the resolved treatment forbids the requested mode for this actor: a reserved act (S-C10); direct application requested without an *effective direct* treatment (never silently converted into a proposal); a *no policy basis* class requested directly; or, **governance phase only** (R8-1), a governed checkpoint's host-held constraint forcing *propose* (R2-12) | Governing treatment (policy record reference, or, in the governance phase, the checkpoint constraint); evaluated basis. For a reserved act (or, in the governance phase, a checkpoint wait): an A8 request is *offered*, not recorded automatically. Never phrased as unavailability; never cites a classifier (S-C11) |
| **Channel not enabled** | **App**, from its own external-access configuration being off, with no host request made; **host**, when the host's channel is off (R4-16). A host refusal is the authoritative "off" (R4-13) | The whole channel is off: external access off unless the person enables it (V4-HI-52); A13 not performed | Channel state and reporter; no operation evaluated. App-side configuration is never A13 evidence (R4-13). **SWBPIPE (SQ-09, SQ-13, SQ-28; R8-6):** no host *channel not enabled* code and no A13 facility. Its off state appears as `controller_unavailable` or an attachment failure, received as *endpoint unavailable* (DEL-03-03 channel state), never as host-reported *channel not enabled*; the channel shows *disabled*, because A13 is never evidenced |
| **Not exposed on this surface** | **Host-reported** from the per-surface exposure element 9 (R2-4); relayed by loop/adapter | The entry exists in the catalog edition and element 9 says it is not exposed on the acting surface | Entry identity; surface; exposure value. A loop or adapter **relays** a host-returned *not exposed*, naming the host as reporter; it never originates it. The loop-side *not offered* failure is separate (below). **SWBPIPE (SQ-06, SQ-11; R8-5):** no exposure element; its `unsupported_method` and `unsupported_change` refusals are relayed as host-reported *not exposed on this surface*, never *not permitted*. R2-4 (a named rule) is recorded as not met by this host |
| **Error** | Host | Evaluation started and a declared error occurred (element 7) | Error identity and meaning; effect statement; evaluated basis |
| **Destination not allowed** (v0.8, node B5; PROPOSED) | **Native layer** of the host, at V-D (before dispatch) or at contact (DEL-05-01/LOOP-v0.8 §5.3 DF-4); for a destination request not granted, the native layer or the host's control | The destination a call declares is not allowed for the host's agent (LOOP DF-3), or a destination request ended *not granted*. The call is **not dispatched** (at V-D) or its contact is not sent | Destination and category; reason (not allowed · always-off item · not stateless MCP (2026-07-28) · grant refused by control · prompt not shown). For reason *not allowed*, a destination request is *offered* (LOOP DF-6), never made in the agent's place. Not *not permitted* (no treatment is involved) and not *unavailable* |
| **Destination not allowed by the person** (v0.8, node B5; wording SETTLED by DECISION-5 and V4-EXM-23) | **Host's control** | The person declined the agent's destination request; the carried call is not sent | The request; the act-declined event of kind A12 (ACT §2.7). Recording it as a destination entry (`destination_declined`) is SETTLED by DEL-04-03's ScopeOfWork CLM-004, which names "destination declined" among the events the record format receives from DEL-05-01 (R16-1, correcting R12-10). The *destination not allowed* row above is not a decline: recording its refusals, made without the person declining (`boundary_refusal`; `destination_request_closed`), stays PROPOSED (R16-1; LOOP-v0.8 DF-8) |

A destination request call first receives an **interim notice**, "waiting
for the person's answer" (a loop state, not a result), and then exactly one
of the results above or a class 3 or 4 outcome of its carried call (LOOP
§5.3 DF-6; node B5).

Loop- and adapter-side failures are not host results (R2-4): a call naming an
operation **absent from the catalog edition offered** to the loop is a
loop-side **not offered** failure and is never dispatched (DEL-05-01 V-2).
*Missing* (no entry in the catalog edition) is a discovery finding (DEL-02-01
required-tool outcome). Neither is labeled *not exposed*.

A denial by the App user's own Codex tool permission (A14) is App-side tool
execution and is not a host outcome (S-C11).

Treatment is resolved on the **host route**, at validation and again at
application (R-3 point 1). A loop or adapter relays the actor's intent and
any governing checkpoint constraint, with that constraint's carriage
assurance (P §3.3; R4-14), and does not decide treatment. Relaying the
constraint is governance phase (R8-1). In Phase 1 the App carries no
constraint, and an agent never adds a field the host schema lacks (R8-10):
SWBPIPE's strict preflight refuses unknown fields (SQ-02 (a), SQ-31).

**SWBPIPE outcome mapping (R8-5, R8-6; INTEGRATION).** SWBPIPE's results are
received as follows; the proposal-side mapping is P §9.

- `unsupported_method` / `unsupported_change` → host-reported *not exposed
  on this surface* (above), never *not permitted*.
- `controller_unavailable`, or an attachment failure → *endpoint
  unavailable*, with the channel shown *disabled* (above).
- `rejected: validation_rejected` at Apply → *refused — invalid* at
  application. DRAFT #885 `withdrawn` → the item left the queue, "cleared by
  the person, no decision record" (P §9). Neither is ever A10 or A11.
- If the host answers a request while no A13 is evidenced, the answer is
  recorded as observed with an evidence limit ("host reachable without
  evidenced A13"). It is never shown as *enabled* (R8-6; DEL-03-03 E-2,
  E-3). Whether a launch environment variable the person sets counts as A13
  evidence is an owner question, deferred until UI-SUCCESSOR resumes (R8-6,
  I2 R8-Q4b).

**Model destination (R4-1; R5-4).** **SETTLED by DECISION-2 (D5):** host
content read by the App's Codex through the external channel may flow to the
App conversation's selected model, cloud included, and the App does not gate
enablement on the destination. **SETTLED (the DECISION-2 reading that the
owner confirmed: SCA-V4-001 OWNER_ITEMS O-10, accepted "as recommended" at
APP-V4-BASIS-ALIGN-20260928 DECISION-7; R9-4):** the App records the
destination **per turn**, and DEL-03-03 shows it in the channel status as
information only. **INTEGRATION (R5-4), unchanged:** it is recorded where
the supplier reports it, including reroutes, keeping requested and
effective destinations separate (unobserved turns: *unknown*); the
run-level value is the set observed, and a switch starts no new run
(DEL-04-03). The destination changes no §4.1 result and no §6 standing. A host may
restrict its own channel (DEP-001); SWBPIPE answered that it does not, so
the App need state nothing (SQ-16). V4-HOST-02, as amended by SCA-V4-001
(DEC-5: the text recorded in DECISION-5, R8-13), governs the host's
embedded agent, not the App's external channel:

> A host's agent sends data only to the model service the person selected and to destinations the person has allowed — in advance in an allow list (by category, such as web access, MCP servers or other APIs, or by named destination) or when the agent asks during its work. Nothing else is contacted: no analytics, silent provider switch or background download unless the person turns it on. Every destination contacted is recorded and shown.

It changes no §4.1 result and no §6 standing. Its rules are LOOP-v0.8
§5.1.1, and the flow is LOOP-v0.8 §5.3; the two "destination not
allowed" rows above are its results for a host's agent (node B5).

### 4.2 Unavailable reason

| Semantic element | Meaning |
|---|---|
| Reason identity | Stable identity for the reason, shared across channels |
| Reason statement | Person-readable text; the same text reaches every channel |
| Failed precondition | Which declared precondition failed |
| Remedy (optional) | What would make it available, stated as a meaning (e.g. "a load case must be identified"), with any gesture phrasing as surface rendering only |
| Evaluated basis | The read basis (§5) against which availability was evaluated |

V4-HI-02's example reason ("Select a load case in the model tree first") is
phrased as a UI gesture (F-C4). For channel parity the precondition is
expressed in operation meaning; the gesture is one surface's remedy text.
Fixtures state remedies as meanings (IR1-B B-m11).

### 4.3 Selection-dependent preconditions

A person often satisfies a target precondition by selecting in the host UI;
an agent supplies the same target through the input schema. Both evaluate the
same precondition. The resolved target becomes part of the request; a later
selection never changes it (DEL-03-02 no-retargeting).

### 4.4 Precondition versus validation error (IR1-B B-m6)

- A condition declared as an element-4 **precondition** yields **unavailable**
  when it fails, with HI-04 parity across channels. It is evaluated before
  execution and may be evaluated at offering time (historical thereafter).
- A condition declared as an element-7 **error** raised by host validation
  yields **refused — invalid** (P §9), with its error identity.
- The host decides which conditions are preconditions and which are
  validation errors, per entry; the catalog makes the choice visible. The
  same condition is never both. Fixture: OP-C4 "location on run" is a
  precondition; "location occupied" is a validation error.

## 5. Read basis and content identities (REQ-004; V4-HI-11/32; SOW-167)

### 5.1 Read basis descriptor

Every read result carries one basis descriptor with four elements plus the
method designation of its content identity. Semantic labels only.

| Element | Meaning (contract level) | Host input still needed |
|---|---|---|
| Workspace identity | Which host workspace/project the read observed | Host's workspace identity scheme |
| Generation | A **host lineage epoch**: revisions are comparable only within one generation (e.g. a restore, re-import or reopen that starts a new lineage yields a new generation). An ordinary intervening edit does **not** change generation; it changes model revision (R-9) | Host definition (U-C2) |
| Model revision | The revision of the model within that generation that the read observed. Every intervening edit advances it | Host revision scheme |
| Canonical content identity | An identity of the content actually read, by a host canonicalization, so equal content yields equal identity independent of presentation | Algorithm and canonicalization unselected (TBD-003); scope of the read-level identity is a host input (U-C3) |
| Identity method designation | Names the method that produced the content identity, so two identities can be judged comparable (same method) or incomparable | Designation scheme unselected; values host-supplied (R-6; V1-B D-03) |

### 5.2 Rules

1. **All elements, every read.** A read lacking any element is *basis
   incomplete* and cannot be cited as a relied-on basis. Historical reads
   carry the historical revision's basis. **Exception (R13-1, INTEGRATION;
   B3's option B as ruled).** A read that lacks workspace identity or
   generation is citable only when the host declares that it supplies no
   workspace identity or generation, in its basis profile (§2.1 CI-3) or in
   a documented host statement, and the read marks the element *host
   declares none* (§3.5). Such a read carries the evidence limit **"basis
   lineage not supplied"**, recorded by the consumer (ADAPTER-v0.6 §4.6
   OM-9; RS R11), and every comparison across lineages reads *unknown
   (incomparable)* (rule 6). A read that simply omits an element the host
   does supply (*omitted*), or lacks any other element, stays *basis
   incomplete*. R8-12 item 6's whole-model identity reading (§5.3) sits
   inside this rule. ADAPTER RD-2 says the same (R13-1). SH-1 exercises the
   case (§10.8, profile *no lineage*).
2. **Basis ≠ operation identity** (§2 invariant 3).
3. **Basis is observed, not chosen.** A consumer never fills in, updates or
   copies a later basis over it.
4. **Every non-success result** carries the basis it was evaluated against
   when the host evaluated one (§4.1).
5. **Multi-view reads.** A read returning several views states whether they
   share one basis; if not, each view carries its own descriptor.
6. **Comparability.** Two content identities are comparable only when their
   method designations are the same (or the host states them comparable).
   Otherwise a consumer reports *unknown (incomparable)* (DEL-04-03 L-2),
   never *unchanged* or *changed*.

### 5.3 Subject content identity (SoW REQ-004; R-6; V1-B D-02)

- Each object/row in a read result carries a **subject content identity**:
  host-supplied, per subject, with its method designation.
- It is distinct from the read-level canonical content identity. An edit to
  one row changes that row's subject identity and the read-level identity,
  but not other rows' subject identities.
- Uses:
  - DEL-04-03 L-1 c₁ for acts on host rows/objects (A4, A6, A7); A5/A10 use
    DEL-03-02's change-item content identity (R-6);
  - the **per-item basis check** (R2-13): DEL-03-02 compares the subject
    content identities of an item's relied-on targets, not the global model
    revision, where the host supplies them; otherwise the host's stated
    staleness scope applies (R8-3; §5.4);
  - **checkpoint subject binding** (R2-17): a subject of class "targets of
    the held call" binds through the subject content identities of the
    relied-on read the held call cites, never through argument text;
  - **resulting objects** of an applied item (R2-14; P §9): post-application
    subject content identities of created and changed objects.
- This is how V4-HI-32's "a row's content hash" is received. Which
  attributes a subject identity covers (e.g. whether a support row's identity
  covers its display label) is a host input (U-C3); the fixtures state their
  assumption (§10.1).
- **Whole-model identity (SoW REQ-004 as revised under SCA-V4-001; R8-4).** A host's whole-model
  identity is received as the subject content identity of **every** subject
  it covers, with the host's method designation and scope. Any model change
  then changes every covered subject's identity, so acts bound on such a
  host lapse, and items stale, on any model change. This errs toward
  reporting a lapse and never misses one. The App never computes identities
  itself, from host reads or otherwise: an App-computed identity would be
  App-assured, not host evidence. Resulting objects beyond the target ids a
  host reports are *not supplied* (P §9).
- **SWBPIPE (SQ-03).** No read returns a per-row or per-object identity. The
  only identity is a whole-model hash (sha256 over the RFC 8785 canonical
  JSON of the model payload). SWBPIPE's current state therefore does not
  meet V4-HI-32's per-subject identity (U-C12, an owner notice). An Apply is
  bound by operation id, a claimed whole-model hash and per-field
  before-values: close to the change-item content identity (P §3.1), but
  not the same. FXA-2 and FXA-3 have no SWBPIPE counterpart.

### 5.4 Citing the relied-on basis in a later action (SOW-168)

- A later action (a change submitted through DEL-03-02, or a non-mutating
  examination that relies on a prior read) carries a **relied-on basis
  reference**: the basis descriptor(s) of the read(s) it actually relied on,
  unchanged, together with the subject content identities of the relied-on
  targets.
- The reference points back to a read; it is never recomputed at queue time,
  at acceptance or at application. A host may additionally record the basis
  it observed later as a **separate** element; it never replaces the
  relied-on reference.
- An action relying on several reads cites each. Which cited bases must
  still hold is U-C4.
- **"No longer holds" (R2-13 as amended by R8-3; INTEGRATION).**
  - **Per item, where the host supplies subject identities.** For a change
    item, the basis no longer holds when a subject content identity of one
    of the item's relied-on targets differs from the current one. A global
    revision advance alone does not stale an item. The **own-effect case**,
    applying sibling items of the same proposal, does not stale remaining
    items unless they share targets.
  - **Otherwise, the host's stated scope.** Where the host does not supply
    subject identities, the App receives and shows the **host's stated
    staleness scope**, and never narrows it. For SWBPIPE the scope is the
    whole model: any model commit (edit, apply, undo, redo, project open or
    create) stales every queued proposal, so applying one proposal stales
    the others; selection changes do not stale (SQ-07 (d), (f)). A stale
    refusal is then shown as "refused — stale (host scope: whole model;
    relied ⟨basis⟩, current ⟨basis⟩); failing targets not supplied" (P §5).
  - **De-duplication first (unchanged).** A resubmission of an identity the
    host already holds is answered from its recorded state before any basis
    check (P §5, §7). SWBPIPE's DRAFT #885 runs its key lookup before the
    basis check, within one controller session (SQ-08 (b), (c)).
  - Host confirmation of the per-item rule and of subject-identity scope
    remains U-C3.
- **Non-mutating operations citing a basis (PROPOSED, V1-B X-07).** A read,
  examination or host check is never refused as *stale*, because nothing is
  applied. Its result carries the basis it was evaluated on. If that differs
  from the cited relied-on basis, the result states both and its standing is
  *historical relative to the cited basis* or *current*, as applicable. Host
  confirmation: U-C10.
- The catalog exposes this association to DEL-03-02 (DEP-03-01-023). Stale
  refusal, re-draft and application behavior belong to DEL-03-02 and are
  *received* here for the M3-CP comparison (§9; DEP-03-01-026).

Receiving risk (HI §11, SWBPIPE at `e548d4cf`): the observed piping
controller path uses a queue-time basis that differs from the original
external inspection basis. Carried unchanged into integration, it would
substitute a later basis for the relied-on one, contrary to rule 3 and
REQ-004. This is a risk for the joined witness (DEL-09-09), not an
assignment to the host. SWBPIPE (SQ-07 (c)): the risk is confirmed for
main's offline intake, which captures the basis at queue time. DRAFT #885
freezes the inspected basis at preview and keeps it at submit, which would
retire the risk if merged and qualified; it is unmerged and deferred (ANS
§3 item 5).

## 6. Read results and standing (REQ-003, REQ-005; V4-HI-10/12; SOW-069, SOW-169)

### 6.1 Read result content

A successful read returns the same meaningful content the person sees for the
same operation and basis: tables, results and diagnostics, with the same
standing marks (V4-HI-10; V4-PAR-03). Presentation may differ; content,
diagnostics and standing may not be filtered, summarized upward or omitted
for an agent channel. An empty table is a successful read with zero rows
*and* its basis, distinct from every §4.1 result.

**Content model (PROPOSED; S1-B C 4; `read_result.schema.json`).**

| Element | How many | Meaning |
|---|---|---|
| Read result | 1 | Outcome *success*; operation identity and version; edition (§2.1); surface; basis (§5.1); one or more views; standing (§6.2); a requested basis only on a requested historical read (§6.4) |
| View | 1 or more | View identity; tables, results and diagnostics (each zero or more); findings where the entry's result declares them; its own basis only when it does not share the read's (§5.2 rule 5) |
| Table | 0 or more per view | Table identity; meaning; columns (one or more); rows (zero or more) |
| Column | 1 or more per table | Column identity; meaning; unit, or none; value kind (number, text, boolean, identity, enumeration) |
| Row | 0 or more per table | The subject it describes, with its subject content identity, method designation and identity scope (*per subject*, or *whole model* under R8-4, §5.3); its cells by column identity |
| Result value | 0 or more per view | Result identity; meaning; value; unit; the subject it concerns |
| Diagnostic | 0 or more per view | Diagnostic identity; severity (information, warning, error); statement; one or more attachments. A diagnostic is the host's statement; it is never an A3 finding and never a host check |
| Finding (A3) | 0 or more | Finding identity; author (the requester, or an agent); statement; one or more attachments. Never "host checks passed" and never A4 (§6.2) |
| Attachment | 1 or more per diagnostic or finding | What it attaches to (read, view, table, row, cell, result or subject) and the reference |
| Host check | in standing | Check name, declared by the entry (§3.4); verdict (passed, failed); evaluated basis; exceedances as attachments |

Rules:

- **RR-1** The person's view of the same operation and basis and the agent's
  result carry the same tables, rows, results, diagnostics and standing
  (V4-HI-10). Presentation may differ; nothing is dropped.
- **RR-2** A diagnostic or finding attached to a row stays attached to that
  subject; it never moves up to the table or the read.
- **RR-3** Units belong to the column or the result value, not to the cell
  text.
- **RR-4** A result the host cannot express in this model is not
  summarized to fit: the read is an *error* with its error identity
  (element 7).

### 6.2 Standing elements

Label rule (R-4): unqualified "checked" means only A4 *mark checked*. Host
results say **"host checks passed: ‹named checks›"**, and only a host check
(a host-defined, named check, e.g. §10 OP-C12) produces one. Agent work is
**examination / findings** (A3), including requester-parameterized
operations such as OP-C3. "Approval" means only A6.

| Semantic element | Meaning | Must not be strengthened by |
|---|---|---|
| Currency | **current** (describes the workspace's present revision) or **historical** (an earlier revision or superseded result) | Presenting a historical result as current; dropping currency |
| Host checks passed | Each named host check the result passed, **with the basis it was evaluated on**. A check evaluated on an earlier basis is shown as historical | Collapsing to "checked"; implying checks not run; showing an old-basis check as current; presenting A3 findings as a host check |
| Known limitations | Host-stated limitations (e.g. solver assumptions, incomplete inputs) | Omitting or softening limitations in an agent summary |
| Human-act evidence (faithfully carried) | References to actual human acts the host has recorded on this content, carried with the whole DEL-04-03 act field set of RS-v0.8 §6.1, which this contract consumes and does not define or subset (SoW CLM-002; DEP-03-01-031; R10-3). Examples of those fields: act kind (RS "Act kind": the R-1 act name), decision actor (the person), recorder, recording mode (direct capture / faithful recording, A9), bound subject, scope, purpose, bound content identity (c₀ with method designation), lapse state, evidence references and evidence limits (V1-B D-16) | Inventing an act; showing a lapsed act as current; attributing an agent finding to the person; showing a row-scoped act as covering a whole table |
| Lapse state | DEL-04-03 §7 vocabulary, consumed and not defined here (SoW CLM-002; DEP-03-01-031; RS-v0.8 §7): not lapsed · lapsed · lapsed (subject absent) · partially lapsed · matches c₀ again after observed lapse · unknown (incomparable) · unknown (unavailable) · not yet evaluated; and for A12/A13, which are not lapse-evaluated, **current · superseded** (RS §7 L-0 and its lapse-state line; supersession is R2-7, PROPOSED; C-v0.6 listed only *superseded*). *Not yet evaluated* never renders as *not lapsed* (V1-B D-14; IR1A-13; IR1-B B-m1) | — |
| Act-declined and run-ended events | An **act-declined event** (A4, A6, A7 or A12, with capture evidence) is carried as an event, never as an act; a **run-ended event** is separate (R2-5) | Rendering a decline as the act, or as a rejection (A10 is A5's pair) |
| Agent findings (A3) | Findings authored by an agent, attached by reference (V4-EXM-21), with the agent as author. Where they are held (host-stored, which may be a change, or message content) is U-C5 | Rendering a finding as checked, approved or "host checks passed" |

Rules:

1. A success value establishes execution only (S-C6).
2. One human act never implies another; no synthetic prerequisite is
   introduced (SoW REQ-005).
3. A faithfully carried act keeps the person as decision actor; the recorder
   is shown separately. Satisfaction of a checkpoint needs attributable
   evidence from the capturing surface (R-5); a carried record cites it.
4. When the bound content changes, the act is shown lapsed (S-C8), judged by
   the subject content identity (§5.3), not by the model revision. An undo
   that changes bound content lapses the act like any other change (R2-15).
   Against a host that supplies only a whole-model identity, any model
   change lapses every bound act (§5.3; R8-4). Recording a lapse is record
   truthfulness and continues in Phase 1; re-hold after a lapse is
   governance phase (R8-11 item 1). SWBPIPE's session undo writes no
   receipt, so a lapse it causes is observed from the identity change, and
   "reverses ⟨receipt⟩" is *not supplied* for it (SQ-10; R8-5).
5. Nothing is presented as certified, sealed, approved or code-compliant
   (V4-AUT-05).

### 6.3 Currency transitions (PROPOSED; S1-B C 5)

Currency is stated by the host when it answers the read, and it changes
only on an observed event.

- **CU-1** A result is **current** while the workspace's present basis has
  the same workspace identity, generation and model revision as the result's
  basis. Any observed revision advance, generation change or workspace change
  makes it **historical**. Currency is revision-level: a change to what was
  read is not required (after T6 the T3 supports table, read at r12, is
  historical, although the rows for S-1, S-2 and S-4 did not change).
- **CU-2** Whether the content is still the same after an advance is a
  separate, derived statement ("content unchanged since r12"), made only
  where content identities of the same method are equal (§5.2 rule 6). It
  never relabels the result current.
- **CU-3** A consumer that has observed nothing since the read shows
  "current as of ‹read time›", never plain *current*.

| From | Event | To | Observed by | Record left |
|---|---|---|---|---|
| current (host-stated at the read) | A later read, host report or event shows a later model revision in the same generation | historical | The consumer | The later basis beside the result |
| current | A generation or workspace change is observed | historical; basis incomparable | The consumer | Comparisons give *unknown (incomparable)* (§5.2 rule 6) |
| current | Nothing observed since the read | current as of ‹read time› | — | — |
| historical | — | historical (final; a later read is a new result) | — | — |
| (requested historical read, §6.4) | — | historical from the start | Host | The requested basis and the basis read |

A host check follows the same rule: a check evaluated on an earlier basis
is shown historical (§6.2).

### 6.4 Historical reads (PROPOSED; S1-B C 5; OUT-003 "current and historical reads")

Two meanings are kept apart:

- **HR-1 Aged result.** A result obtained as current that has become
  historical (§6.3). Nothing is requested; its standing changes.
- **HR-2 Requested historical read.** A read whose request names an earlier
  basis. It is offered only where the entry says it accepts a requested
  basis (§3.4). The result carries the requested basis and the basis
  actually read, currency *historical* (unless the requested basis is the
  present one), and the standing as it stood at that basis where the host
  holds it. If the host does not hold that basis, the result is
  *unavailable*, reason "the requested earlier basis is not held"; the
  present content is never relabelled as the past.
- **HR-3** A historical result may be cited as a relied-on basis. A change
  citing it meets the ordinary stale rule (§5.4), so it is refused stale
  where its relied-on targets changed since.
- *SWBPIPE (SQ-07 (h)), record only:* computed results are cleared on any
  model change, and no historical read is described.

## 7. Operation sequences (catalog view)

```text
discover entry (identity, version, purpose, schemas, availability, class, exposure)
  → request read (arguments)          → unavailable | not permitted | channel not enabled
                                        | not exposed on this surface (host) | error   (each with evaluated basis)
  → read result (content, standing, BASIS B, subject content identities)
  → [consumer reasoning; no host state]
  → request change citing relied-on basis B, relied-on target identities, any checkpoint constraint (governance phase)
       (DEL-03-02 route) host de-duplicates by proposal identity, resolves treatment, checks basis
       (per item where the host supplies subject identities; otherwise the host's stated scope, R8-3)
       → P §9 outcomes (refused — stale cites B and current basis;
          applied associates proposal/item, B, receipt, resulting revision, resulting objects)
```

Failure behavior at catalog seams:

| Situation | Required behavior |
|---|---|
| Entry version changed between offering/discovery and request | The request carries the entry version it was prepared for. A host-side mismatch is reported as an element 7 error meaning (U-C6), not re-interpreted. A loop may pre-screen for a catalog-edition change before dispatch; that is reported as loop-side, not as a host outcome (V1-C D-13) |
| Call names an operation absent from the edition offered | Loop-side *not offered*; never dispatched (R2-4) |
| Read returns without full basis | Consumers mark it *basis incomplete* and do not cite it for a change |
| Lost read response | No content is invented; the consumer re-reads and obtains a new basis. Reads have no effects, so no model outcome-unknown applies |
| Availability evaluated earlier than the request | Availability is re-evaluated at request; the earlier evaluation is historical |

### 7.1 Operating sequences with failure behaviour (PROPOSED; S1-B C 5; R12-1)

Each step names what can fail, who reports it, the record left and what
happens next. "Consumer" is the host loop on E (DEL-05-01) or the App on X
(DEL-03-03); on H the host's own interface does the same.

**SQ-C1 Discovery and offering, per surface.**

| Step | What can fail | Reporter | Record left | Next |
|---|---|---|---|---|
| 1 Consumer calls CI-1 on its surface | Endpoint not reachable (X: *endpoint unavailable*, ADAPTER §3.2); channel off (*channel not enabled*); catalog unreadable (CF-1); partial (CF-2); no catalog (CF-3) | The consumer, naming itself; the host for *channel not enabled* and *partial* | Discovery record: the edition, or the failure with its reason | On failure nothing is offered, and requirements are *not established* |
| 2 Consumer reads the basis profile (CI-3) | Profile not supplied | The consumer | "Basis profile not supplied" | Each read is judged by its own descriptor (§5.2 rule 1) |
| 3 Consumer maps entries to its native surface and offers them (CI-5) | An entry cannot be mapped (ADAPTER NM-2) | The consumer | Offering record naming the edition; unmapped entries *not established* | — |
| 4 Required-tool check against the edition (EXEC-v0.6 §3.4) | Entry *missing*; *not exposed on this surface* (element 9) | EXEC's evaluator | Compatibility report naming the edition (EI-4) | Per EXEC |

On E the host loop does steps 1–3 for its own tool offering (LOOP). On X
the App's Codex discovers natively; the App records steps 1–3 from what it
observes (ADAPTER-v0.6 §4.1, §4.6, §8 S-6).

**SQ-C2 Edition change during a run.**

| Step | What can fail | Reporter | Record left | Next |
|---|---|---|---|---|
| 1 The host publishes e′ and reports CI-4 | The event is not observed | — | None yet; the consumer still holds e | The next CI-1 shows e′: held superseded, "without an observed event" (§2.2) |
| 2 The consumer marks e superseded and re-discovers | Discovery fails | The consumer | The event; the failure | held unknown (§2.2); as CF-1 |
| 3 Requests already prepared on e keep their entry versions | The host reports a version mismatch (element 7 meaning, U-C6) | Host | The error | The drafter prepares a new request on e′ |
| 4 New offering from e′ | An entry was removed in e′; a later call to it | Loop or App | Offering record for e′; loop-side *not offered* | Never dispatched |

**SQ-C3 Current read.**

| Step | What can fail | Reporter | Record left | Next |
|---|---|---|---|---|
| 1 Request: entry, version, arguments | A §4.1 non-success | Host (App for its own *channel not enabled*) | The result with its evaluated basis | Relayed unchanged |
| 2 Result returned | The basis lacks an element | The consumer | *basis incomplete* (CF-5) | Not cited for a change |
| 3 Response delivered | The response is lost | The consumer | "Read response lost" | Re-read for a new basis; nothing invented (§7) |
| 4 Consumer records the read | — | — | DEL-04-03 R7 entry with the observed basis | — |

**SQ-C4 Requested historical read.**

| Step | What can fail | Reporter | Record left | Next |
|---|---|---|---|---|
| 1 Consumer checks that the entry accepts a requested basis (§3.4) | It does not | The consumer | — | No such request is made |
| 2 Request names the earlier basis | The host does not hold it | Host | *unavailable*, "the requested earlier basis is not held" | — |
| 3 Result | — | Host | The requested basis, the basis read, currency *historical* | Cited only as HR-3 allows |

**SQ-C5 Reliance on several reads.**

| Step | What can fail | Reporter | Record left | Next |
|---|---|---|---|---|
| 1 A change cites each relied-on read (§5.4) | A cited basis was never received by the agent | The App (ADAPTER RD-5) | Evidence limit "cited basis not observed" | Recorded; in native families not prevented |
| 2 The host checks each cited basis (per item on targets, or its stated scope) | One no longer holds | Host | *refused — stale* naming every cited basis and the current one | Re-draft (P §5) |
| 3 Which cited bases must still hold | Undecided (U-C4) | — | — | The host's check decides; the App shows every cited basis |

**SQ-C6 Generation change.**

| Step | What can fail | Reporter | Record left | Next |
|---|---|---|---|---|
| 1 The host starts a new lineage (restore, re-import): g1 → g2 | — | Host | The new generation in every later basis | — |
| 2 The consumer observes a g2 basis | — | The consumer | Every g1 result historical, basis incomparable (§6.3); lapse and stale comparisons *unknown (incomparable)* (DEL-04-03 L-2) | — |
| 3 A change cites a g1 basis | — | Host | *refused — stale*, or a host rejection across generations (SWBPIPE #885 rejects cross-workspace reuse, SQ-07 (b)) | Re-draft; nothing is recomputed. The host's definition stays U-C2 |

## 8. Three-surface responsibility map — skeleton (OUT-002; REQ-006; SOW-072, SOW-165)

Surfaces: **H** = host human interface; **E** = embedded-agent tools (host
loop, received by DEL-05-01/05-02); **X** = external interface (host-built
MCP server or CLI over the live controller, V4-HI-50/V4-ARC-21; App side
received by DEL-03-03).

Cell values: **generated**, **checked**, **hand-built**, **unagreed**. No
generation or check route has been agreed with the host owner, so every cell
is **unagreed**; the *candidate* column records what #d4 and V4-HI-03 suggest
examining, not a selection. The fixture's assumed exposure (§10) does not
change this map: the map is about real host agreement.

| Catalog element / concern | H | E | X | Candidate to examine | Producing owner | Receiving point |
|---|---|---|---|---|---|---|
| Entry discovery (identity, version, purpose, open description) | unagreed | unagreed | unagreed | generated for E and X | Host owner | DEL-05-01 tool offering; DEL-03-03 native tool inspection; PKG-02 tool descriptors (DEP-03-01-022) |
| Catalog-level interface (§2.1: edition identity, edition-change event, basis profile; added at v0.8) | unagreed | unagreed | unagreed | one host producer for all three surfaces | Host owner | DEL-05-01 offering; DEL-03-03 discovery (§4.6); DEL-02-03 report (EI-4); DEL-09-09 V-ED1 trace |
| Exposure per surface (element 9) | unagreed | unagreed | unagreed | declared per entry | Host owner | DEL-02-01 required-tool outcome; DEL-05-01; DEL-03-03 |
| Input schema / argument checking | unagreed | unagreed | unagreed | generated or checked for E and X | Host owner | DEL-05-01 REQ-003 (catalog schema before domain validation) |
| Loop-side catalog-schema argument checking (DEL-05-01 candidate (b)) | — | unagreed | — | question held: shared checker or per-host (V1-C D-28) | UNRESOLVED{OI-013}/{OI-014} | DEL-05-01; DEL-10-03 |
| Availability + reason | unagreed | unagreed | unagreed | checked on all three (parity rule) | Host owner | DEL-05-02 panel; DEL-03-03 |
| Effects / affected objects / resulting objects | unagreed | unagreed | unagreed | generated metadata | Host owner | DEL-03-02 target binding and applied association |
| Result content + standing | unagreed | unagreed | unagreed | H hand-built views; E/X checked against H meaning | Host owner | DEL-05-02; DEL-04-02; DEL-09-09 VER-002 |
| Errors | unagreed | unagreed | unagreed | generated identities, hand-built texts | Host owner | DEL-03-02 outcome taxonomy |
| Class element | unagreed | unagreed | unagreed | carried from DEL-04-01 records | DEL-04-01 → host | DEL-04-02; DEL-03-03; DEL-05-01 |
| Governing checkpoint constraint (receipt on the host route) — governance phase (R8-1) | unagreed | unagreed | unagreed | per-request carriage or host-held declaration (relay, R2-12) | Host owner with DEL-03-02 | DEL-05-01 §6.2; DEL-03-03 |
| Read basis, subject content identities, method designation | unagreed | unagreed | unagreed | one host producer for all three | Host owner | DEL-03-02; DEL-04-03 L-1/L-2 |
| Proposal views (old/new/objects/reason) | unagreed (host's own views, V4-HI-24) | n/a (agent drafts) | n/a | host-owned presentation; generation route open | Host owner | DEL-03-02 view receiving (DEP-03-02-024) |
| Shared types / components carrying the above | — | — | — | UNRESOLVED{OI-014} | App/shared contract owners | DEL-10-03 account |

DEL-09-09's generated and adapted work account is tied to these rows cell
by cell (XT-v0.6 §5.1.1); an observed route never changes an agreed cell
there (V18-4 n-2).

**SWBPIPE's answers against this map (R8-10; answers, not agreement).** The
cells record agreement with the host owner, and none exists, so they stay
*unagreed* (DECISION-3 defers the host joins). SWBPIPE's answers describe its
current state: on X, entry discovery is hand-built and narrow, with no
per-operation identity or version, and is neither generated from nor checked
against a catalog (SQ-12); there is no exposure element (SQ-11) and no
embedded surface E (SQ-11, SQ-19); there is no governing-constraint receipt
(SQ-02: route (iv), a governance-phase input); the read identity is
whole-model, with no subject content identities (SQ-03, SQ-07); and the
host's batch review shows each step as field, before and after (SQ-22).

Extension promise (App v4 OI-003; S-C9): the original promise that a new catalog
operation becomes available to the person and both agents **without separate
work** is preserved and **not claimed**. Its disposition — retain, narrow to
defined generated surfaces, or defer — is `UNRESOLVED{OI-003}`, owned by the
owner with the host contract owner (DEP-03-01-027). Per-surface exposure
(element 9) is where a narrowed promise would be expressed; its real values
stay *unagreed* until the ruling. The evidence route is DEL-09-09's
V4-EXM-24 trace (DEP-03-01-030; CASE-002 M4-X), using fixture V-ED1. No automatic availability or
maintenance saving is advertised and no narrower criterion is selected.
SWBPIPE has no catalog editions and no edition-addition event (SQ-26), so the
V-ED1 trace has no SWBPIPE counterpart now; SWBPIPE's participation in the
OI-003 decision is a SWBPIPE owner decision.

## 9. Proposal input this catalog needs, and the M3-CP return

Co-developed with DEL-03-02/P-v0.8 (original SCC-CASE-004 pair, carried in
CASE-002; co-revised in the R8 pass and aligned in the same Wave A node). Both files had one author through R1 and R2; C↔P agreement is not
independent evidence (IR1-B note).

**Forward (C → P, DEP-03-01-023 / DEP-03-02-016).** C supplies: operation
identity and version; input schema including target identification; effects;
errors with effect statements; the §4.1 results; the read basis descriptor
with method designation; subject content identities; exposure; and the
relied-on basis reference meaning (§5.4).

**Proposal input C needs from P** (compared at V1; repaired at R1 and R2):

| Needed from DEL-03-02 | P-v0.8 locus |
|---|---|
| Relied-on basis reference carried unchanged from drafting through outcome, with relied-on target identities | P §3.2 |
| Stale refusal reporting the relied-on and current bases, with reason and evaluated basis; per-item check on target identities where the host supplies them, otherwise the host's stated scope (R8-3) | P §5, §9 |
| Re-draft as a separately identified proposal citing the new basis, with lineage | P §5 |
| Retry precedence: identity-based de-duplication before the basis check | P §5, §7 |
| **Applied-outcome association** per item: proposal/item identity, relied-on basis, host receipt reference, resulting revision, and **resulting objects** — created and changed object identities with their post-application subject content identities and method designation, or "not supplied" as an evidence limit (R2-14). Whether the host receipt *itself* carries these is a host observation, not assumed (V1-B D-22) | P §9, §11 |
| Target binding fixed at drafting | P §6 |
| Change-item content identity built from C elements | P §3.1 |

**Return (P → C, M3-CP, DEP-03-01-026).** Distinct from the forward handoff:
DEL-03-02 supplies designed refusal/application behavior and the C/P
read-then-action comparison with an intervening edit (P-v0.8 §11). DEL-03-01
uses it only to compare the basis elements across read, proposal, refusal,
re-draft and applied outcome (VC-C-04). AC-004/VER-004 cannot be claimed
complete until an actual, candidate-bound return exists (V1-B X-08). The
DEL-03-02 register still lacks the DOWNSTREAM mirror of DEP-03-01-026 (V1-B
RF-08; C1-B M-02-1; a deferred supplier-side mirror row, DAG-003 HANDOFF
open matters).

**The return run on SH-1 (v0.8; S1-B C 8; P-v0.8 §11).** The comparison was
run once on the simulated host SH-1 (§10.8) on 2026-09-30, over both native
paths: T3 → T5 → T6 → T7 → T9 → T10 → T11 → T12 → T13. All five basis elements
were compared at every step: PR-1's reference equals B1 at T5 and in the T7
refusal (relied r12, current r13, failing target S-3); PR-2's reference
equals B2 (r13) at T10, in the T12 association (RC-1, r14, S-5 created,
R-100 changed) and at the T13 retry, which was answered from recorded state
with no stale refusal. Evidence label *test-double*. It was **not** bound to
an App candidate, so it is not the candidate-bound return AC-004 and VER-004
ask for, and AC-004 stays held.

## 10. Shared fixture catalogue — FX-PIPE-01 (R-9; R2-21)

This section is the **one** invented fixture catalogue and revision timeline
for the Wave-1 definitions. Other files cite its entries and steps; a
genuinely needed local case is named `L-‹file›-n` and says why. All material
is **invented fixture subject matter**. Labels (OP-C…, S-…, T…, V-…, PR-…,
RC-…, ⟨set-n⟩) are fixture labels, not operation identities, wire names or
SWBPIPE commitments. No SWBPIPE catalog has been supplied. Owning this shared
fixture is an R1/R2 integration assignment serving several deliverables; it
does not extend DEL-03-01's SoW scope (IR1-B §5). Every C-v0.2 identifier is
kept stable; v0.3 only adds identifiers.

### 10.1 Model and fixture assumptions

FX-PIPE-01: workspace **FX-W1**, generation **g1**. One run **R-100** between
nozzles N-1 and N-2; supports **S-1 … S-4** (S-2 and S-3 rigid at start);
sustained load case **LC-1**. Person: **Engineer A** (invented). Agent: the
host's single agent seat (fixture; SWBPIPE has no seat concept, and its one
agent panel is the likely counterpart; SQ-19 (d); R8-8). Workflow: `supports-adjust` (invented; identity per
DEL-02-01 §6.1: kind *workflow*, origin *host*, source root ⟨fx-root⟩, name
`supports-adjust`, revision ⟨rev-3⟩), run **12**.

Catalog editions: the main timeline T1–T17 runs on edition **e2** (entries
OP-C1…OP-C12). Edition **e1** is e2 without OP-C9; the addition is variant
V-ED1 (§10.4) (R4-20; adopts DEL-09-09 L-XT-1's e1/e2).

Conversation: run 12's conversation is **K-7** (V2 §3; used by P E-1).

App-side fixture subjects (R4-20; DEL-02-03 F-15). These are App content,
not host content, and have no catalog entry:

| ID | What | Identity | Use |
|---|---|---|---|
| **LIB-A1** | App project workflow library ⟨fx-proj⟩ (origin *project*) — the library in which App-registered revisions such as ⟨rev-A2⟩/⟨rev-A3⟩ hold the name `supports-adjust` | Library identity ⟨fx-proj⟩ | Collision and registration cases (EXEC RT-6/RT-7) |
| **LIB-A2** | App-side **holding library** ⟨fx-app-import⟩ for host workflows relayed to the App (R2-20 holding library; non-identity) | Library identity ⟨fx-app-import⟩ | Host→App transfer (EXEC RT-6) |
| **AF-1** | App file "supports-review report" in the App project of LIB-A1 (`reports/supports-review.md`, invented) | File content identity ⟨AF-1@f1⟩, method ⟨m-fx-file⟩ (DEL-04-03 L-1 third source) | App-side A4 capture (EXEC CH-23); lapse on file edit (⟨AF-1@f2⟩) |

Workflow revision labels ⟨rev-A2⟩/⟨rev-A3⟩ remain DEL-02-03's (they are
workflow identities, not fixture subjects).

Fixture assumptions (labeled; host inputs in reality). **FXA-n** was **FA-n**
in C-v0.3 (renamed per V2 m-5; R4-19). DEL-04-03 has since renamed its own
rules to OF-1…OF-9, so no collision remains either way (V3-B m-6). Cite
**FXA-n** (R5-9); a C-v0.3 citation of FA-n resolves to FXA-n:

- **FXA-1 Exposure.** Every entry is **exposed on H, E and X** (fixture
  assumption, R2-21). Non-exposure is demonstrated only by named variant V-X1.
  SWBPIPE (SQ-11): no exposure element; one entry is offered on its CLI (Node
  `position.x`), and it has no embedded surface.
- **FXA-2 Subject identity scope.** A support row's subject content identity
  covers its location, type, stiffness **and display label**. A run's subject
  identity covers its geometry, not its supports' attributes. No SWBPIPE
  counterpart (SQ-03 (b)): SWBPIPE has no per-object identity, and its
  whole-model identity is received for every subject (§5.3; R8-4).
- **FXA-3 Relied-on targets.** Adding a support between two supports relies on
  those two supports (their subject identities) and on the run. No SWBPIPE
  counterpart: its staleness is whole-model (SQ-07 (d); R8-3).
- **FXA-4 Settings.** ⟨set-1⟩: for the SWB model-change class (DEL-04-01
  P-03), display state **effective (policy default)**, grant value *propose*,
  no setting actor (R2-6). ⟨set-2⟩: after T15.
- **FXA-5 Checkpoints (V2 m-8).** The fixture workflow ⟨rev-3⟩'s declaration
  is DEL-02-01 WD-EX E1: `CP-accept` (A5; reached-when kind (c) *queued* for
  the proposal the run submits with OP-C4/OP-C5 items; subject: its change
  items) and `CP-check` (A4; subject: objects changed by `CP-accept` items'
  applied outcomes). Run 12 runs on the embedded surface E.
  **Phase 1 (R8-1; R9-1; EXEC PH-1…PH-7):** both checkpoints are plan guidance.
  Nothing is held, no hold-support value is assigned, and the requirement
  check is decided by the required tools and the channel state (run from
  the App through X, it *passes*: EXEC MT-2). Each checkpoint's required
  act is requested — in the current phase by the agent carrying out the
  workflow (R9-1; SETTLED by DECISION-K1 K1-1) — and is recorded as done only when the person performs
  it; arrivals and acts are recorded as observation.
  **Governance phase (retained; the values read the checkpoints as if
  declared `governed`, which ⟨rev-3⟩ does not declare; R8-11 item 5):** on
  E, the host loop's own evaluation of this declaration makes the governing
  checkpoint constraint on OP-C4/OP-C5 requests **host-held** (P §3.3;
  R5-2), and each checkpoint's hold support is **enforced by the host loop**
  (R5-1; subject to host evidence, DEP-001; SWBPIPE has no host loop,
  SQ-20). Run from the App through X, `CP-accept` is **not enforceable**
  (HS-3 (c): SQ-02 answered 2026-09-28, route (iv), none planned) and
  `CP-check` is **not enforceable** (its held Return is App-side, HS-5), so
  that run is **unsupported** (EXEC MT-2; R6-1, R6-4, R8-2). On the main
  timeline (recorded dispositions, in both phases; EXEC PH-6),
  `CP-accept` arrives at T10 (PR-1 was never queued) and, after T11, is
  *resolved negatively* with a partial annotation (item 1 A5, item 2 A10;
  R2-18, WD §4.3.7). `CP-check`'s arrival and act are not scheduled on C's
  timeline. ⟨rev-3⟩ declares **no** `CP-grant`, so no grant-setting checkpoint
  occurs on the main timeline; V-GR1 carries that case. V-CP1 isolates the
  direct-grant conflict.

### 10.2 Entries

| Fixture | Purpose | Inputs | Availability (precondition → reason) | Effects | Result + standing | Errors (effect) | Class (§3.1) | Exposure H/E/X |
|---|---|---|---|---|---|---|---|---|
| OP-C1 v1 "Read supports table" | Lists supports on a run with type, location, stiffness, label | run | run exists → "Run not found in this workspace" | none | supports table with a subject content identity per row; currency; host checks passed (with basis); limitations | E-invalid-run (none) | none — fixture assumption | exposed ×3 (FXA-1) |
| OP-C2 v1 "Read sustained-load results" | Stresses and support loads for a load case | run, load case | a load case is identified → "A load case must be identified"; a current solve exists → "No current solve for LC-1 at this revision" | none | results table; currency; host checks passed each with evaluated basis; limitation "linear supports assumed" | E-unknown-load-case (none) | none — fixture assumption | exposed ×3 |
| OP-C3 v1 "Examine support spacing" (non-mutating) | Lists spans exceeding a **requester-stated** limit, for the requester's examination | run, spacing limit | run exists | none | exceedance list as the requester's **findings (A3)**, with evaluated basis; never "host checks passed" (the limit is the requester's) | E-invalid-limit (none) | none — fixture assumption; findings are not A4 | exposed ×3 |
| OP-C4 v1 "Add support" | Adds a support at a location on a run | run, location, type | run exists; location on run → "Location is not on run R-100" (precondition, §4.4) | supports table, R-100 | applied association with **resulting objects** (new support identity and its subject identity) | E-location-occupied (validation → refused — invalid; none); E-apply-interrupted (unknown) | may apply within granted autonomy — DERIVED (P-03); default propose; OI-021 additions pending; host adoption not evidenced | exposed ×3 |
| OP-C5 v1 "Set support stiffness" | Changes a support's stiffness | support, stiffness | support exists | support row | applied association with resulting objects | E-invalid-stiffness (none) | as OP-C4 | exposed ×3 |
| OP-C6 v1 "Mark row checked" | Performs the person's A4 on a row's content | row | row exists | host act state on row | act captured, bound to the row's subject content identity | E-row-changed (none) | **reserved to the person** — DERIVED (R2-2; D2a) | exposed ×3 |
| OP-C7 v1 "Accept proposal items" | Performs the person's A5 on one or more change items | proposal, items | items queued | proposal item dispositions | A5 captured, bound to each item's change-item content identity | E-item-not-queued (none) | **reserved to the person** — DERIVED (R2-2; D2b) | exposed ×3 |
| OP-C8 v1 "Reject proposal items" | Performs the person's A10 | proposal, items | items queued | proposal item dispositions | A10 captured | E-item-not-queued (none) | **reserved to the person** — DERIVED (R2-2; R-1 A10) | exposed ×3 |
| OP-C9 v1 "Set support label" | Changes a support's display label (low consequence) | support, label | support exists | support row (label) | applied association with resulting objects | E-label-too-long (none) | as OP-C4 (model change) | exposed ×3; variant V-X1: not exposed on X |
| **OP-C10 v1 "Undo (reverse a receipt)"** (new, R2-15) | Reverses the change recorded by a receipt, through the one route | receipt | receipt exists and is reversible → "Receipt cannot be reversed" | objects changed by the reversed receipt | applied association with relation **reverses ⟨receipt⟩** and resulting objects | E-reverse-conflict (none) | governed by the **policy record of the operation whose receipt it reverses** (e.g. reversing RC-2 from OP-C9 → P-03: may apply within granted autonomy, default propose) — R3-4 (INTEGRATION; DEL-04-01 states it under P-03); undo mechanism a host input (U-P8) | exposed ×3 |
| **OP-C11 v1 "Renumber nodes"** (new, R2-21) | Renumbers node labels on a run | run, scheme | run exists | node labels on R-100 | applied association | E-invalid-scheme (none) | **no policy basis** (reason: **pending OI-021**) — INTEGRATION (R2-1) | exposed ×3 |
| **OP-C12 v1 "Run support-spacing host check"** (new, R2-21) | Runs the host's named check "support spacing" with host-defined limits | run | a current model basis exists | none | "host checks passed: support spacing" or "host check failed: support spacing" with exceedances, each with evaluated basis | E-check-unavailable (none) | none — fixture assumption | exposed ×3 |

Grant changes (A12) and enabling/disabling external access (A13) are person
acts on host/App controls, not fixture catalog entries here; they are
reserved (S-C10).

### 10.3 Timeline (one revision sequence, generation g1)

Content identities are opaque: ⟨v12⟩ is a read-level identity at r12,
⟨S-2@r12⟩ a subject identity; method designation ⟨m-fx⟩ throughout.

| Step | Revision | Event | Fixture uses |
|---|---|---|---|
| T1 | r12 | State: S-1…S-4 on R-100; LC-1 solved at r12 (host checks passed: "equilibrium", "unit consistency", evaluated at r12). Settings ⟨set-1⟩ (FXA-4) | Baseline |
| T2 | r12 | Engineer A marks row S-2 checked (OP-C6; A4), bound to ⟨S-2@r12⟩, direct capture by host facility | Standing; lapse later |
| T3 | r12 | Agent reads OP-C1 → basis **B1** = FX-W1/g1/r12/⟨v12⟩/⟨m-fx⟩, with ⟨S-1…S-4@r12⟩ | Read basis |
| T4 | r12 | Agent runs OP-C3 with limit 6 m: span S-2→S-3 exceeds it (A3 findings, basis B1) | Agent findings |
| T4a | r12 | Agent runs OP-C12: "host check failed: support spacing" (span S-2→S-3), evaluated at r12 | Host check (named) |
| T5 | — | Agent drafts **PR-1** relying on B1: item 1 add guide support at 4.2 m on R-100 (OP-C4; relied-on targets R-100, S-2, S-3 per FXA-3); item 2 S-3 stiffness rigid → 2.0e6 N/m (OP-C5; relied-on target S-3) | Proposal draft |
| T6 | r13 | Engineer A edits S-3 stiffness in the host UI (intervening edit). ⟨S-3⟩ changes; ⟨S-2@r12⟩ unchanged; LC-1 results become historical (no current solve at r13) | Intervening edit; unrelated-edit control for T2 |
| T7 | r13 | Agent submits PR-1 → both items **refused — stale** (each relies on ⟨S-3@r12⟩): relied B1, current **B2** = FX-W1/g1/r13/⟨v13⟩/⟨m-fx⟩, reason "S-3 changed since r12" | Stale refusal (per-item check, R2-13; fixture: SWBPIPE's scope is the whole model, R8-3) |
| T8 | r13 | Any channel requests OP-C2 for LC-1 → **unavailable**, reason "No current solve for LC-1 at this revision", evaluated basis B2 | Unavailable parity |
| T9 | r13 | Agent re-reads OP-C1 (B2) and drafts **PR-2** (lineage PR-1, stale): item 1 add support (old: none; targets R-100, S-2, S-3 at r13); item 2 S-3 stiffness (old: value at r13) → 2.0e6 N/m | Re-draft |
| T10 | r13 | PR-2 validated → **queued** | Queued ≠ applied |
| T11 | r13 | Engineer A accepts item 1 (OP-C7; A5 bound to item-1 change-item content identity) and rejects item 2 (OP-C8; A10) | Item-level acts |
| T12 | r14 | Host applies item 1 → receipt **RC-1**; applied association PR-2 / item 1 / B2 / RC-1 / r14 / resulting objects: **S-5 created** ⟨S-5@r14⟩, R-100 changed ⟨R-100@r14⟩. A5 on item 1 is **not** lapsed by its application | Applied; resulting objects; no lapse on application |
| T13 | r14 | Acknowledgment of T12 lost. Agent resubmits PR-2 (same proposal identity). The host de-duplicates by identity **before** any basis check and reports the recorded state: item 1 applied RC-1, item 2 rejected (R2-13). If the loop cannot observe that report either → **outcome unknown** (observer: loop), last observed state *accepted* | Retry precedence; one effect |
| T14 | r15 | Engineer A edits S-2 stiffness → T2's A4 on S-2 **lapsed** (⟨S-2⟩ changed) | Lapse |
| T15 | r15 | Engineer A performs A12 → ⟨set-2⟩: SWB model-change class (P-03), grant value *direct*, **scope** {model/workspace: FX-W1; object set: {S-4}} (R-8 dimensions). Host control confirms → display state **effective, direct**. Because OP-C5 shares class P-03, this grant would also admit OP-C5 on S-4 directly; a consequence dimension could exclude it, but its vocabulary is open (U-02), so no fixture expectation is set for OP-C5 on S-4 under ⟨set-2⟩ (held on U-02) | Grant change (reserved act); R-8 scope |
| T16 | r16 | Agent applies OP-C9 directly (label S-4 "G-4") under ⟨set-2⟩ → receipt RC-2, origin mark, undo route; no acceptance recorded | Direct branch |
| T16a | r16 | Engineer A marks row S-4 checked (OP-C6; A4), bound to ⟨S-4@r16⟩ | Act on content the undo will change |
| T17 | r17 | Engineer A reverses RC-2 via OP-C10 → receipt RC-3, relation **reverses RC-2**; S-4 label restored. T16a's A4 **lapsed** (⟨S-4⟩ changed, FXA-2). RC-2's standing: "applied, then reversed by RC-3" | Undo; lapse by undo (R2-15) |
| Tg | g2/r1 | (Separate branch) Workspace restored from an archive: new generation g2. Any basis from g1 is incomparable by revision; lapse and stale evaluation under generation change is U-C2 | Generation change |

### 10.4 Named variants

| Variant | Branches from | Event | Expected |
|---|---|---|---|
| **V-S1** Stale after acceptance | T11 | Engineer A edits S-2 before T12 (branch revision r14′) | Item 1 (relies on S-2) **refused — stale** at application; A5 not lapsed; display "accepted by Engineer A — not applied: refused — stale (relied B2, current ⟨B-r14′⟩)" (R2-16). No SWBPIPE counterpart: its A5 is Apply, which applies at once, and a stale Apply is refused with no acceptance recorded (SQ-01, SQ-23; R8-5) |
| **V-CP1** Acceptance checkpoint vs direct grant | A variant of T15 granting *direct* for P-03 with scope {model/workspace: FX-W1; object set: R-100 and its supports}, plus FXA-5 | Agent requests OP-C4 directly in run 12 | **Phase 1 (R8-11 item 2 and R8-12 item 2, as restated by R9-2; EXEC CH-27):** the App carries and enforces no constraint. The agent, following the declaration as plan guidance, proposes OP-C4 and never adds a field the host schema lacks (R8-10). A direct request, if made, meets the host's own treatment and is recorded as observed; nothing is reported *not permitted* on the constraint's account. If the host applies it directly (the variant grant allows that), no proposal arises, so `CP-accept` (reached-when kind (c) *proposal queued*, FXA-5) is **not reached**: nothing is requested by reason of an arrival that did not occur, no A5 is forced, and none is recorded; the record shows the direct application under the variant grant (R9-2 as corrected by R10-1). **Governance phase (retained; `CP-accept` read as if declared governed):** **not permitted**, naming the governing checkpoint constraint {run 12, CP-accept, A5, OP-C4}; the agent may then submit a proposal separately, whose items become CP-accept's subject (R2-12). Status: Phase 1 DESIGNED. Governance phase **AWAITING INPUT** (host receipt of the constraint, relay) — SQ-02 answered 2026-09-28: route (iv), no receipt and no host copy, and a constraint field would be refused as unknown (SQ-02 (a)); SQ-20: no host loop (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3) |
| **V-NP1** No policy basis | T9 | Agent requests OP-C11 directly; then proposes it; Engineer A attempts A12 granting direct for OP-C11's class | Direct → **not permitted** (no policy basis, pending OI-021); proposal → queued, confers no permission; A12 → **refused (reason: no policy basis)**; dependent production reported **held** (R2-9) |
| **V-R1** Reserved entry call | T3 | Agent calls OP-C6 on S-1 | **not permitted** (reserved to the person, P-02) with an A8 request *offered*; no A8 recorded unless issued; never *not exposed* or *unavailable* |
| **V-X1** Not exposed | T16 | External agent (X) calls OP-C9 where element 9 = not exposed on X | Host returns **not exposed on this surface**; the adapter relays it (reporter: host). If X's channel is off instead: **channel not enabled**. (SWBPIPE form: `unsupported_change`, relayed as host-reported *not exposed on this surface*, R8-5) |
| **V-OU1** Lost outcome | T12 | Neither T12 nor T13 report observed | **outcome unknown**, observer loop, last observed *accepted*; no inferred effect |
| **V-GR1** Grant checkpoint arrives before T15 (R5-7) | T14 (r15), replacing T15–T16 in a separate **run 13** of WD-EX **E1d** — workflow {workflow, project, ⟨fx-proj⟩ (LIB-A1), `label-with-grant`, ⟨rev-D1⟩}, carried unadapted, declaring `CP-grant` (A12; reached-when kind (a) *before dispatch of OP-C9*; subject: the declared setting content {class P-03; grant value *direct*; scope {model/workspace FX-W1; object set {S-4}}} = the content of ⟨set-2⟩) — on surface **E**, hold support **enforced by the host loop** (governance phase; SWBPIPE has no host loop, SQ-20) | **GR-1** (r15, settings ⟨set-1⟩): the agent's OP-C9 call (S-4 label "G-4") is held before dispatch → `CP-grant` **arrives**. **GR-2**: Engineer A performs T15's A12 with exactly the declared content, captured **after** the arrival; the control establishes ⟨set-2⟩. **GR-3**: the held call is dispatched unchanged = **T16** (r16, RC-2, direct under ⟨set-2⟩, origin mark, undo route, no acceptance). Sub-variants: **GR-P** pending, then the confirmation observation is lost; **GR-R** refused by the control; **GR-S** a later established A12 narrowing the scope | GR-1: `CP-grant` *waiting*. GR-2: `CP-grant` **performed** (captured after the arrival; EXEC SP-6). GR-3: T16 as on the main timeline. GR-P: *waiting* "awaiting control confirmation", then **unknown**; the call stays held. GR-R: *waiting* "A12 refused by control: ‹reason›"; ⟨set-1⟩ stays in force, not superseded (R4-6). GR-S: stays *performed*, "superseded by ‹act›" (R2-7). **Main order (DECISION-K1 K1-2):** had `CP-grant` arrived only at T16 after T15's A12, that A12 — on the declared content, with ⟨set-2⟩ still in force — counts: `CP-grant` is **performed** at the arrival, citing T15's A12 and its time (EXEC SP-6; WD-EX R-16 (i)); run 12 is unaffected because ⟨rev-3⟩ declares no `CP-grant`. Under the governance-phase option (EXEC SP-6F) that A12 would be a **prior act not counted**, and the person would repeat a grant change whose content is already in force (U-E4/U-31, closed for the current phase). **Phases (R8-1, R8-2).** The run on E above is the **governance-phase** reading (retained; `CP-grant` read as if declared governed, R8-11 item 5): holding the call and the hold-support value are governance phase. **Phase 1:** nothing is held (EXEC PH-2); GR-1's arrival is recorded before the OP-C9 dispatch, the dispatch proceeds as the agent's plan decides, and the dispositions above label the record (EXEC PH-6); the A12 is requested (in the current phase by the agent carrying out the workflow, R9-1; SETTLED by DECISION-K1 K1-1) and is recorded only when the person performs it. **From the App via X.** *Phase 1:* the requirement check passes on the required tools and the channel state (EXEC MT-16). *Governance phase:* `CP-grant` (kind (a) on host operation OP-C9) is **not enforceable** (EXEC HS-3 (c): SQ-02 answered 2026-09-28; WD-EX E8; R8-2), and E1d's `CP-check` is *not enforceable* (HS-5), so the run via X is *unsupported* (EXEC MT-16) |
| **V-ED1** Catalog-edition addition (R4-20; DEL-09-09 L-XT-1) | Replays T1–T15 on edition **e1** (no OP-C9) and publishes e2 before T16 (V3-B m-11) | (1) Each surface looks for OP-C9 on e1. (2) The host publishes **e2**, adding OP-C9 v1 as §10.2 describes it — the **edition addition event**, identified by {edition e1 → e2, added entry OP-C9 v1, time}. (3) Each surface rediscovers. (4) T16 proceeds on e2 | (1) OP-C9 **missing** on every surface (discovery finding) — never *not exposed* or *unavailable*. (2) One event, host-reported; no model revision change (the catalog is not model content). (3) Full entry per §3 on each surface, exposure per FXA-1. Whether any surface needed separate work is DEL-09-09's account (App v4 OI-003); nothing here claims automatic availability. (No SWBPIPE counterpart: no catalog editions and no edition-addition event, SQ-26). Since v0.8 the event is the catalog interface element §2.1 CI-4, and V-ED1 runs on SH-1 (§10.8) |

**SWBPIPE counterparts of the main timeline (R8-3, R8-4, R8-5; answers about
SWBPIPE's current state, not commitments; the fixture is unchanged).**

- **T7:** staleness is whole-model, and no failing targets are named (SQ-07
  (d)).
- **T11:** the person's A5 is Apply: per batch, atomic, accepting and
  applying in one step, with no A10 record. Clear discards a batch without
  a record (SQ-01, SQ-09 (b), (f)). Per-item A5/A10 decisions and mixed
  items have no counterpart.
- **T12:** the outcome names target ids, per-field diffs and the new
  whole-model hash, with no post-application per-object identity (SQ-03
  (d)).
- **T13:** in DRAFT #885, de-duplication by the caller's key precedes the
  basis check, within one controller session only (SQ-08 (b), (c)).
- **T15–T16:** there are no grants and no direct application (SQ-05,
  SQ-06).
- **T17:** undo is a session snapshot, not an operation through the route,
  and writes no receipt (SQ-10).

### 10.5 Read basis vs operation identity

| Read | Operation (identity/version) | Basis |
|---|---|---|
| T3 | OP-C1 v1 | FX-W1 / g1 / r12 / ⟨v12⟩ / ⟨m-fx⟩ |
| T9 | OP-C1 v1 (same operation) | FX-W1 / g1 / r13 / ⟨v13⟩ / ⟨m-fx⟩ — different basis |
| hypothetical | OP-C1 **v2** (entry revised) | FX-W1 / g1 / r13 / ⟨v13⟩ — different operation version, same basis |

### 10.6 Unavailable example (T8, three channels)

Person (H), embedded agent (E) and external agent (X) each request OP-C2 for
LC-1 at r13. Expected on all three: *unavailable*; failed precondition
"current solve exists"; reason identity R-no-current-solve; same statement;
evaluated basis B2. Not acceptable: an empty results table, a generic error,
or the r12 result without historical currency. If X's channel is off, X
instead gets *channel not enabled* (a separate case).

### 10.7 Standing example (T4a, T12–T14)

OP-C2 after a new solve at r14 (hypothetical): currency current; host checks
passed "equilibrium", "unit consistency" evaluated at r14; limitation
"linear supports assumed". T4a's "host check failed: support spacing" is
shown historical (r12). Row S-2 at r14 carries T2's A4 (actor Engineer A,
recorded by host, direct capture, bound ⟨S-2@r12⟩): **not lapsed** (T6 edited
S-3 only). At r15 (T14) it is shown **lapsed**. T4's findings are shown as
agent findings (A3), never as checked or as a host check.

### 10.8 SH-1, the simulated host (the one test double; R12-4; PROPOSED)

The verification cases of C, P, ADAPTER and XT presume a test double
(VC-C-02…05; P §11; ADAPTER §10 "simulated endpoint"; XT). It is specified
**once, here**; the other files cite this section and do not define their
own. SH-1 is a local prototype, not product code and not a model of any real
host: `prototype/simhost.py` beside this file (Python 3 standard library),
with its driver `prototype/run_fixture.py` and README. Everything run on it
carries the evidence label *test-double* (the mapping under Verification
cases) and establishes nothing about SWBPIPE or any other host.

**What it is.** One host state (a state file) holding a part of FX-PIPE-01:
workspace FX-W1, generation g1, run R-100 with supports S-1…S-4, load case
LC-1 solved at r12, settings ⟨set-1⟩, edition e2 (or e1 for V-ED1). One host
core answers every request, so the same state is observable through either
path.

| Aspect | SH-1 |
|---|---|
| **MCP-tool path** (N-MCP) | A local process speaking newline-delimited JSON-RPC 2.0 on its standard input and output, with the methods `initialize`, `tools/list` and `tools/call`. `tools/list` renders one tool per catalog entry, with a host-supplied mapping to operation identity, version and edition, plus four interface tools: `read-catalog` and `read-edition-events` (§2.1 CI-1, CI-4) and `submit-proposal` and `observe-proposal` (P-v0.8 §3.5). A `tools/call` result carries the host document as structured content and as text |
| **Command-line path** (N-CLI) | The same host core as a command: `catalog`, `events`, `call ‹operation› --json ‹arguments›`, `submit --json ‹proposal›`, `observe ‹proposal identity›`. It writes one host document as JSON on standard output. Exit status 0 means a host document was produced, whatever its outcome; a non-zero status with no document means the endpoint was not reached (ADAPTER-v0.6 §4.6 OM-4) |
| Host documents | Follow the PROPOSED schemas: `catalog.schema.json`, `edition_change_event.schema.json`, `read_result.schema.json` (here) and `proposal_state.schema.json` (P). A change request follows `proposal.schema.json` (P) |
| Person and host controls | Separate commands that no agent path reaches, standing for the host's own interface: A13 enable or disable (fixture acts by the scripted person Engineer A, recorded in the double's own facility with a capture reference), edit a subject, accept or reject an item (A5, A10), set a direct grant (A12, ⟨set-2⟩), publish edition e2, stop or start the endpoint; and the host's own step "apply accepted items" (P-v0.8 §3.5 PM-5). None is App act capture |
| Profiles | *full* (every basis element supplied) and *no lineage* (the basis profile declares no workspace identity and no generation; reads mark both *host declares none*), for the case R13-1 rules (§5.2 rule 1) |
| Implements | OP-C1 (with a requested historical read, §6.4), OP-C2, OP-C3, OP-C4, OP-C5, OP-C6…OP-C8 (reserved: *not permitted*, A8 offered), OP-C9 (e2 only), OP-C12; the proposal route with de-duplication by proposal identity before any basis check, per-item staleness on relied-on target identities, identity conflict, observation by identity, direct application under ⟨set-2⟩; host-reported *channel not enabled* while A13 is not in force |
| Does not implement | OP-C10 undo, OP-C11, checkpoint declarations (checkpoint cases are exercised only as the observations ADAPTER passes on), restart of the double's own records, timing and concurrency. Also absent, as its consumers found (CA-v0.6 F-26; XT-v0.6 F-25; V18-4 m-10): an H or E surface (only X's two paths; exposure is declared per entry but no H or E request is served); a person control for A4; a whole-model identity and staleness profile (the SWBPIPE form, R8-3, R8-4); an origin mark on the applied association; a session-scoped (non-durable) de-duplication and receipt profile; host views and UI selection; OP-C9's precondition and label validation. Consumers record the parts that need these *not run*; adding them as profiles is a candidate for SH-1's next development, not done here |
| Names | The tool names (fixture labels), command words, the `_meta` key `sh1/catalog` and the identity method ⟨m-sh1⟩ (a truncated sha256 over sorted JSON) are the double's own. They select no host wire field, transport or identity algorithm (TBD-003; ADAPTER TBD-007) |

**Run of 2026-09-30 (node B3).** Command: `python3 run_fixture.py --out
"$TMPDIR/b3-sh1-run"` in `prototype/`, then `validate_all.py --run`, and the
P and ADAPTER prototypes on the same run directory. Result: 21 of 21 checks
passed; 34 native items and 30 host documents were recorded, and all 30
documents and the 6 change requests validated against the schemas. The full
output is in `WAVE_B/B3.md`. Cases run:

| Case | Path | Observed on SH-1 |
|---|---|---|
| XF-02 (channel off, host side) | both | Host-reported *channel not enabled* on both paths, channel state *disabled* |
| CI-1 discovery | both | The same edition e2 and entries on both paths |
| T3 (VC-C-02 on X's two paths) | both | Identical read documents: basis B1 = FX-W1/g1/r12/⟨sh1:…⟩/⟨m-sh1⟩, subject identities per row |
| T4, T4a | CLI, MCP | Requester's findings (A3); "host check failed: support spacing" with its evaluated basis |
| T6 → T7 | CLI | Both PR-1 items *refused — stale* per item: failing target S-3, relied B1 (r12), current r13 |
| T8 | MCP | *unavailable*, R-no-current-solve, evaluated basis r13 |
| T9 → T10 | CLI, MCP | PR-2 (lineage PR-1) *queued*, 2 items |
| T11 | person; CLI observation | Item 1 *accepted* (A5), item 2 *rejected* (A10); derived state *mixed* |
| T12 | host; MCP observation | Item 1 *applied*, RC-1, r14, S-5 created, R-100 changed; A5 kept |
| T13 | MCP (response dropped), then CLI | Lost acknowledgement; observation by identity returns the recorded state (2 submissions); the retry is answered from recorded state (3 submissions, RC-1), never stale |
| P §3.5 PM-2, PM-3 | CLI, MCP | *not known to host*; same identity with different content → *identity conflict*, no effect |
| V-R1; OP-C4 requested directly under ⟨set-1⟩ (ADAPTER XF-22, run at r14) | MCP, CLI | *not permitted*, A8 offered; *not permitted* naming P-03 ⟨set-1⟩ *propose* |
| §6.4 HR-2 | MCP | Requested read at r12: currency *historical*, basis r12 |
| T15 → T16 (ADAPTER XF-23) | CLI | Direct under ⟨set-2⟩: *applied*, RC-2, branch direct, no decision recorded |
| ADAPTER XF-06 | both | Endpoint stopped: the command exits 69 with no host document; the MCP process does not start |
| V-ED1 | CLI, MCP | OP-C9 *missing* on e1; one host-reported CI-4 event e1 → e2 adding OP-C9 v1; rediscovery shows it |
| R12-9 case (ruled by R13-1) | CLI | Profile *no lineage*: the basis profile and the read both mark workspace identity and generation *host declares none* |
| VC-C-04 | — | No step rewrites a relied-on reference (all five elements compared) |

**Rerun at the RP-2 repair (2026-09-30).** Same commands, output under
`$TMPDIR`: 22 of 22 checks passed (the 21 above, and one more: the R13-1
rule classifies the *no lineage* read as citable with "basis lineage not
supplied", a read *omitting* workspace identity on the full profile as
*basis incomplete*, and the T3 read as citable); the printout gives that
one rule in place of B3's two options (V18-3 n-5). 34 native items and 30
host documents; all validated. The double's recorded states now carry the
explicit item-left event on each item that left (P-v0.8 §4.3; the two PR-1
items at T7) and the capture time of each host-captured A5 and A10
(P-v0.8 §9). Full output in `WAVE_B/RP-2.md`. Evidence label *test-double*.

## Changes from v0.7

v0.7 = C-v0.7 (last changed at `c896a99d90`; unchanged at `86cafc0e1c`;
sha256 eaf16b82b4250c56446544dd97a65baf064091d196013fb28abda40d543e010c).
Wave B of run APP-V4-DESIGN-PASS-2-20260930 (node B3): design development
under R12. Keyed by R12 ID and by the S1-B survey item (file 1, §1.8). Every
new structure is PROPOSED (R12-1).

| R12 ID / survey item | Change in v0.8 | Where |
|---|---|---|
| R12-1; S1-B C 5 | The catalog as an interface: discover (CI-1), read entry (CI-2), basis profile (CI-3), edition-change event (CI-4, moved here from fixture variant V-ED1), offering record (CI-5); edition identity rules EI-1…EI-5; two edition transition tables (host and consumer-held); catalog-level failures CF-1…CF-5, including an unreadable, partial or absent catalog and a read lacking basis elements | §2.1–§2.3; §10.4 V-ED1 |
| S1-B C 4 | Read-result content model: element table (view, table, column, row, result value, diagnostic, finding, attachment, host check) and RR-1…RR-4. Entry sub-elements: named host checks (element 6) and "accepts a requested basis" (element 3) | §6.1; §3.4 |
| S1-B C 5 | Currency transitions CU-1…CU-3 with a table; historical reads HR-1…HR-3 (an aged result versus a requested historical read) | §6.3; §6.4 |
| R12-1; S1-B C 5 | Operating sequences SQ-C1…SQ-C6 (discovery and offering per surface, edition change during a run, current read, requested historical read, reliance on several reads, generation change), each step with its failure, reporter, record and next step | §7.1 |
| R12-1, R12-2; S1-B C 6 | Required elements and cardinality for the catalog edition, entry, class, basis descriptor, unavailable reason and standing. Three PROPOSED JSON Schemas beside this file, each with valid and invalid instances; §0 states that they select no wire field | §0; §3.5; `catalog.schema.json`, `edition_change_event.schema.json`, `read_result.schema.json` |
| R12-3, R12-4; S1-B C 8 | SH-1, the one simulated host, specified here for both native paths (MCP-tool and command-line) and cited by P, ADAPTER and XT; runnable prototype in `prototype/`; run once on 2026-09-30 (21 of 21 checks). The M3-CP comparison ran on it (test-double; not bound to an App candidate, so AC-004 stays held) | §10.8; §9; VC-C-04; VC-C-09; VC-C-10 |
| R12-9 (R10-5) | §5.2 rule 1's note points to node B3's ruling proposal; the basis profile (CI-3) and the explicit *not supplied* marker (§3.5) are the structures both options need; both texts stand until R13 | §5.2; §2.1; UNRESOLVED U-C14 |
| — | §1: DEL-03-01's row names SH-1. §8: a row for the catalog-level interface, *unagreed* | §1; §8 |
| — | Header: v0.8; a Wave B line with the inputs read; the Serves line names the schemas and SH-1 | Header |
| **B5** (node B5, round 2; S1-D LOOP item 5, the tool subject) | §3.4 gains the **external-contact declaration** (element 5) and the entry kind **destination request**, so destination-reaching tools are catalog entries and no second tool source is needed (LOOP-v0.8 §5.3 DF-1, G-13); §3.5 cardinality follows; §4.1 gains **destination not allowed** (native layer) and **destination not allowed by the person** (host's control), with the interim notice stated as not a result. `catalog.schema.json`: `entry_kind`, `effects.external_contact`, value kind `carried_call` (additive); new `catalog.example-valid-2.json` and `catalog.example-invalid-2.json`; `prototype/validate_all.py` rerun: all checks passed | §3.4; §3.5; §4.1; schema and examples |
| **R14-7** (RP-2, in place; R13-1; V18-3 M-3, V18-4 M-4) | R13-1 applied: §5.2 rule 1 states the ruled exception (citable only when the host declares it supplies no workspace identity or generation; limit "basis lineage not supplied"; comparisons across lineages *unknown (incomparable)*; an omitted element stays *basis incomplete*), replacing the note that both texts stand; CF-5 follows; U-C14 closed; the `read_result.schema.json` `not_supplied` description states the rule; §10.8 profile row and run table name R13-1 | §5.2; §2.3 CF-5; UNRESOLVED U-C14; `read_result.schema.json`; §10.8 |
| V18-3 n-5 (RP-2) | `run_fixture.py` prints the one ruled rule in place of B3's options A and B, and adds a check of it (three reads classified); rerun 22 of 22 | `prototype/run_fixture.py`; §10.8; VC-C-10 |
| V18-3 m-15, R-7, n-3 (RP-2) | The destination request entry's "*exposed* on E only" and its carried-call argument are now refused by `catalog.schema.json` when absent (`contains` added to the validator subset); conformance rule **CX-1** (a *from argument* declaration names an argument of its entry) stated in §3.5 and checked by `validate_all.py`, which also reruns V18-3's three mutations (each now rejected); new `catalog.example-invalid-3.json` | §3.4; §3.5; `catalog.schema.json`; `prototype/schema_subset.py`, `validate_all.py`, README |
| V18-3 n-2 (RP-2; NOTE) | OP-C10's class has no form in the class element or the schema; recorded in §3.5, not resolved (SH-1 does not implement OP-C10) | §3.5 |
| V18-4 m-10 (RP-2) | §10.8 "Does not implement" lists what CA F-26 and XT F-25 found missing from SH-1; no profile added | §10.8 |
| P-v0.8 join (RP-2; R14-8 N-18, V18-3 M-1) | SH-1's recorded states carry the explicit item-left event on each item that left and the capture time of each host-captured A5/A10, as P-v0.8 §4.3 and §9 now define them | `prototype/simhost.py`; §10.8 |
| V18-1 m-1 (RP-2) | V-GR1: "prior act, not counted" → "prior act not counted" (RS L-13 wording) | §10.4 V-GR1 |
| V18-1 m-5 (RP-2) | A15 named beside the act names: a person's act no checkpoint may require and no entry here performs | §0 |
| V18-1 m-8, V18-3 n-1 (RP-2) | §4.1 says C-v0.8 and P-v0.8 added rows and that DEL-04-03 receives the two destination rows as R15 entries, not R7 outcomes (RS §5 to say so); EI-4 cites EXEC-v0.6 §3.3 and LOOP-v0.8 §6.2; §6.2 cites RS-v0.8 §6.1 and §7; §0 cites EXEC-v0.6 §2.4–§2.5 for the App-run mechanism | §0; §2.1 EI-4; §4.1; §6.2 |
| V18-4 n-2 (RP-2; NOTE) | §8 cites XT-v0.6 §5.1.1, the account tied to its rows | §8 |
| — (RP-2) | Header: the repair's inputs (R14, R13, V18-1…V18-4, BRIEFS) pinned on the Wave B line. VC-C-09 and VC-C-10 record the rerun | Header; Verification cases |
| RQ (repairs from V19; in place, no version bump) | V19-A m-5: §6.1's read-result rules renamed RC-1…RC-4 → **RR-1…RR-4** while PROPOSED, so they no longer share the fixture's receipt identities RC-1…RC-3 in this file; no meaning changed. V19-A m-3: live citations moved to Wave B labels (Phase line EXEC-v0.6 §2.1 and WD-v0.8 §4.3.0; WD-v0.8 §4.3.1; ACT-POLICY-v0.8 §8.1; LOOP-v0.8 §5.1.1; EXEC-v0.6 §3.4); history citations kept | Header; §0; §3.1; §4.1; §6.1; §7; this table |
| RV20 (final review V20-A B-1; brief from HELP_HUMAN for node RV20 of run `APP-V4-DESIGN-PASS-2-20260930`; in place, no version bump) | **R16-1 carried into §4.1:** the "destination not allowed by the person" row now reads recording it as a destination entry (`destination_declined`) SETTLED by DEL-04-03's ScopeOfWork CLM-004 (R16-1, correcting R12-10), as RS §4 R15, ACT §2.7, AS §3 and LOOP-v0.8 DF-8 already state; recording the *destination not allowed* row's refusals, made without the person declining, stays PROPOSED (LOOP-v0.8 DF-8). No schema, example or prototype change | §4.1 |

No fixture identifier is re-meant and no FX-PIPE-01 value changes. New
identifiers: CI-1…CI-5, EI-1…EI-5, CF-1…CF-5, RR-1…RR-4, CU-1…CU-3,
HR-1…HR-3, SQ-C1…SQ-C6, SH-1, VC-C-09, VC-C-10, U-C14, U-C15, and at the
RP-2 repair CX-1 (U-C14 closed there). The catalog
edition (§2) stays PROPOSED. Not done here: S1-B C items 1–3 and 7 belong to
Wave A or to other nodes; no host wire field, hash or canonicalization
algorithm, placement or §8 cell value is chosen.

## Changes from v0.6

v0.6 = C-v0.6 (last changed at `caa4334ca1`; unchanged at `3dd7c22c73`; sha256
8282c003024e54708f3b9842e04b6b0dc8c4e1c496027afae582eb6387675ce4). Wave A of
run APP-V4-DESIGN-PASS-2-20260930 (node A1-B): alignment to the amended basis
and the revised ScopeOfWork under R9. No new design content. Keyed by R9 ID
and by the S1-B survey item (file 1).

| R9 ID / survey item | Change in v0.7 | Where |
|---|---|---|
| R9-11 | C-v0.6 → C-v0.7. Still DRAFT: unsupplied, unimplemented, not accepted | Header |
| R9-5 (S1-B 1.1 pins 2–6, 13, 15–18; 1.8 item 1) | Basis re-pinned: the four basis documents at their current sha256, naming SCA-V4-001 and SCA-V4-002; ScopeOfWork.md at its current sha256, naming AX-004; DAG-003; the current Case_Datasheet and OWNER_DECISIONS states; R6…R9 added to the rulings. The v0.6 pins are kept as history. Consumed inputs gain a Wave A paragraph (siblings by label only; RELAY_ANSWERS at `afb6e063…`), and the earlier passes are marked as history | Header |
| V10 N-1 | The R8-13 consumed-input sentence is reordered so that only R8_RESOLUTIONS.md is placed at `1528a5033`. No value changed | Header |
| R9-1, R9-3 (S1-B 1.1 pin 20; 1.3) | "V4-WF-05's first half" and "flagged for the next accepted-basis update" are dropped. The phase statement cites V4-WF-05 and V4-HI-42 as amended and uses the R9-1 summary: the request for the act and its recording are in force in every phase, and only the hold is phased. First use reads "the current phase (Phase 1)" | Header, §0 |
| R9-1 (who requests; INTEGRATION) | §0 states the ruling (the agent requests; the product gives the declaration, offers the means and records what it observes) and points to EXEC, Wave B, for the mechanism. FXA-5 and V-GR1 now say that the act is requested | §0; §10.1 FXA-5; §10.4 V-GR1 |
| R9-2, R9-4 (R8-11 item 2; OWNER_ITEMS O-25) | S-C10 restated: D2's reserved-act sentence binds; V4-HI-42's request clause and record clause are in force; whether the run goes on before the act is for the person and the agents | S-C10 |
| R9-2 (R8-12 item 2) | Class rule 3 and V-CP1, Phase 1: on a direct application the checkpoint's act is still requested, no A5 is forced and none is recorded, and the disposition stays *act not performed* | §3.1 rule 3; §10.4 V-CP1 |
| R9-1 (S1-B 1.1 pin 21) | §4.1: the "flagged" marker on V4-HOST-02 is replaced by "as amended by SCA-V4-001". The quotation is unchanged and matches PRD V4-HOST-02 word for word | §4.1 |
| R9-4 (OWNER_ITEMS O-10) | §4.1 model destination: "the App records the destination per turn and shows it" is SETTLED with that citation; the R5-4 detail stays INTEGRATION | §4.1 |
| R9-4 (S1-B 1.2 item 5; 1.8 item 2) | The revised SoW is cited where it now states the rule, and the INTEGRATION label is dropped there: REQ-002 for the exposure element, its independence from class and the explicit *no policy basis* value; REQ-004 for subject content identities and the whole-model identity. Class rule 4's treatment (R2-9) and the §5.4 staleness rule (R2-13, R8-3) keep INTEGRATION | §2 inv. 5; §3; §3.1; §5.3 |
| R9-6 (S1-B 1.2 items 2, 3; 1.6) | Receivers line rebuilt from the ACTIVE register rows, with row IDs and DEL-03-04, DEL-09-06 and DEL-10-03 added; the "unregistered join" notes are removed; DEP-05-01-014's schemas are marked "not yet defined here". §1's DEL-04-03 row and §9's mirror note follow the registers | Header; §1; §9 |
| S1-B 1.8 item 3 (1.6 rows DEP-03-01-024, -031) | §6.2 says "act kind" as RS does, states that the act field set and lapse vocabulary are consumed (SoW CLM-002; DEP-03-01-031), names the RS §6.1 elements this file does not list, and gives the A12/A13 states as "current · superseded". §3.1 value standing adds PROPOSED, as ACT §8.1 has it | §3.1; §6.2 |
| S1-B 1.1 pin 22; 1.2 item 6 | "as of C-v0.5 / P-v0.5" now adds "carried in C-v0.7 / P-v0.7"; U-C8 names the current ACT version | §4.1; UNRESOLVED |
| R9-8 (S1-B 1.4 C23, C24; 1.8 item 7) | UNRESOLVED: the register row is restated against the current registers; the SoW-text row is closed (SCA-V4-001) | UNRESOLVED |
| R9-5, R9-11 | Body citations of siblings name the Wave A labels (P-v0.7, WD-v0.7, LOOP-v0.7, EXEC-v0.5, ACT-POLICY-v0.7, RS-v0.7) | Header, §0, §3.1, §4.1, §6.2, §9, VC-C-04 |
| **R10-1** (node A2, in place; R9-2's second bullet corrected) | Class rule 3 and V-CP1, Phase 1: a direct application queues no proposal, so `CP-accept` (kind (c) *proposal queued*) is **not reached**; nothing is requested by reason of an arrival that did not occur, no A5 is forced and none is recorded; the record shows the direct application under the grant. A checkpoint reached under such a grant has its act requested and is *waiting*. "Act not performed" as a disposition and "its act is still requested" are withdrawn | §3.1 rule 3; §10.4 V-CP1 |
| **R10-3** (node A2, in place) | §6.2 "Human-act evidence" carries the whole RS-v0.7 §6.1 act field set, consumed and not subset; the listed fields are examples. The "at least" list and the Wave B note on the remaining RS fields are removed | §6.2 |
| R10-5 (node A2, in place) | §5.2 rule 1 gains a note pointing at ADAPTER-v0.5 §4.3 RD-2 and at R10-5: a read lacking workspace identity or generation is decided in Wave B (node B3). Both texts stand | §5.2 rule 1 |
| **K1-1** (node A3, in place; owner DECISION-K1 of 2026-09-30, `APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md` sha256 35d6546346907137581be7df3bed4a8ccdb4b8bc55a261ca716040d0ad9f91bc) | §0: who requests is **SETTLED by DECISION-K1 K1-1** (was INTEGRATION, put to the owner) | §0 |
| **K1-2** (node A3, in place) | V-GR1 recomputed: GR-2 counts on the earlier-act rule too; the main order (T15's A12 before a `CP-grant` arrival at T16) now gives **performed** by T15's A12, cited with its time (EXEC SP-6), not "prior act, not counted" (kept only under the governance-phase option EXEC SP-6F). The SP-6-cost UNRESOLVED row is closed; VC-C-05 follows | §10.4 V-GR1; UNRESOLVED; VC-C-05 |
| **R11-4** (node A4, in place; V17-A m-1) | The closing sentence below this table is marked "at node A1-B", and a sentence states what node A3 changed: SP-6 is the SETTLED earlier-act rule; the R4-5 rule is kept as SP-6F (governance-phase option); JA-1 added in EXEC; V-GR1's main order and VC-C-05 recomputed; the SP-6-cost UNRESOLVED row closed | Closing sentence of this table |
| R11 notes, V17-A N-1 (node A4, in place) | FXA-5 and V-GR1: the requester citation "(R9-1)" gains "SETTLED by DECISION-K1 K1-1", as §0 already says | §10.1 FXA-5; §10.4 V-GR1 |
| **R11-3** (node A4, in place; V17-A M-1) | Basis line: this run's records pinned at their final bytes: R9 `a64e2415…` (was `c3efe2ff…`), R10 `ad3b6caa…` and R11 `e7343b66…` added, OWNER_DECISIONS `7458e9e8…` (DECISION-K1) added | Header |

At node A1-B: no fixture identifier is added, removed or re-meant, and no fixture value changes. No UNRESOLVED identifier is added. Closed: the SoW-text row. PROPOSED items stay PROPOSED (R9-4): the catalog edition (§2), *superseded* for A12/A13 (R2-7) and SP-6 (R4-5) are unchanged in standing. At node A3 (DECISION-K1): SP-6 became the SETTLED earlier-act rule for the current phase (EXEC SP-6; K1-2); the R4-5 rule is kept as EXEC SP-6F, PROPOSED, a governance-phase option; the joint answer JA-1 was added in EXEC §4.7 (K1-3); V-GR1's main-order result and VC-C-05 were recomputed; and the SP-6-cost UNRESOLVED row was closed.

## Changes from v0.5

v0.5 = C-v0.5 (last changed at `c6f81a4f2`; unchanged at `94aa9181b`; sha256
72ac4f0f853213f9778d69c4b3eb84d6b19d1bab80a147d98b7bc5068bb0eacf). Keyed by R8
ID. Sources are I2 rows of INTAKE_MAP.md (`nn.k`, `P2.n`, Part 2.2 and Part
3/4 items); R8 overrides I2 where they differ.

| R8 ID (I2 source) | Change in v0.6 | Where |
|---|---|---|
| **R8-1** (DECISION-4 D4-1) | Phase framing added: Phase-1 checkpoints are plan guidance; the governing checkpoint constraint, its carriage and hold support are the **governance-phase definition (retained)**, for checkpoints declared `governed` (WD-v0.6 §4.3.1). Class rule 3 and the §4.1 *not permitted* constraint clause are relabelled governance phase, with a Phase-1 statement beside them (EXEC CH-27). The constraint relay in §4.1 and the §7 diagram, and the §8 constraint row, are marked governance phase. V4-WF-05's first half is recorded as phased, not withdrawn | Header, §0, §3.1 rule 3, §4.1, §7, §8 |
| **R8-1** (cases; P2.1, P2.4) | FXA-5, V-CP1 and V-GR1 take the two-part form: the **Phase-1 result** (guidance; nothing held; check decided by required tools and channel state, EXEC MT-2, MT-16; dispositions label the record) and the **governance-phase value** | §10.1 FXA-5; §10.4 V-CP1, V-GR1; VC-C-05 |
| **R8-2** (02.6; P2.1, P2.4; §2.2 C rows) | SQ-02's answer (route (iv), none planned) recorded as a governance-phase input. FXA-5: `CP-accept` via X **not established** → **not enforceable** (HS-3 (c)); V-GR1: `CP-grant` via X **not established** → **not enforceable**. Both X runs stay *unsupported* in the governance phase; no Phase-1 result changes for a hold reason. V-CP1's status keeps AWAITING INPUT for the governance phase with the STD-2 annotation (SQ-02, SQ-20) | §10.1 FXA-5; §10.4 V-CP1, V-GR1; UNRESOLVED constraint row |
| **R8-3** (07.1, 07.2, 07.6; Part 3 items 2, 5) | R2-13 as amended: per-item staleness where the host supplies subject identities; otherwise the host's stated scope is received and shown, never narrowed (SWBPIPE: whole model); de-duplication first unchanged (SQ-08 (b) noted). Receiving-risk paragraph annotated (queue-time basis confirmed on main; DRAFT #885 would retire it). T7, FXA-3, §9 and the §5.3 uses bullet follow | §3.3, §5.3, §5.4, §7, §9, §10.1, §10.3, U-C3 |
| **R8-4** (03.1, 03.2; Part 3 item 3; Part 4.3) | Whole-model identity received as every covered subject's identity: over-lapse, never under; never App-computed; resulting objects beyond target ids *not supplied*. SWBPIPE recorded as not meeting V4-HI-32 (new U-C12, owner SWBPIPE, PB-TBD-002 / DEL-16-03). §6.2 rule 4 notes lapse on any model change; FXA-2 has no counterpart | §3.3, §5.3, §6.2, §10.1, UNRESOLVED |
| **R8-5** (09.3, 09.4, 11.1; Part 3 items 1, 10; Part 4.9) | Outcome mapping: `unsupported_method`/`unsupported_change` → host-reported *not exposed on this surface*, never *not permitted*, with R2-4 recorded as not met; `validation_rejected` → *refused — invalid* at application; #885 `withdrawn` → item left, "cleared by the person, no decision record"; neither A10 nor A11. Accept-and-apply, per-batch Apply, no A10 record and session undo without receipt recorded as SWBPIPE counterparts (V-S1, T11, T17) | §4.1, §6.2, §10.4 |
| **R8-6** (09.4, 13.3; Part 3 item 4) | §4.1 *channel not enabled*: SWBPIPE has no such code and no A13 facility; `controller_unavailable` → *endpoint unavailable*, channel *disabled*; a host answer without evidenced A13 → evidence limit; R8-Q4b (launch environment variable as A13 evidence) deferred to the owner | §4.1 |
| R8-7 (Part 3 item 12; 16.7; Part 4.11) | "App v4 OI-003" qualified (§0 note, S-C9, §8, V-ED1, UNRESOLVED). The model-destination UNRESOLVED row is **closed**: SWBPIPE answered SQ-16 with no restriction | §0, S-C9, §4.1, §8, §10.4, UNRESOLVED |
| R8-8 (19.7; Part 3 item 9) | "The host's single agent seat" marked a fixture; SWBPIPE's one agent panel noted as the likely counterpart | §10.1 |
| **R8-10** (04.4, 12.2, 18.2, 26.1; Part 4.1, 4.7) | **No capability catalog on SWBPIPE** recorded: no per-operation identity or version, no editions, no exposure element, hand-built CLI; WD required-tool references cannot resolve against it (EXEC EV-4 → *not established*); new U-C13 (owner notice). §8 cells stay *unagreed*: the map records agreement, so I2 12.2's proposed X-column value is recorded as a SWBPIPE answer beneath the map instead. Strict preflight: the agent never adds fields the host schema lacks. OI-021 stays open, with SWBPIPE's candidates recorded | §2, §3.1, §4.1, §8, UNRESOLVED |
| R8-11 (items 1, 2, 5) | S-C10: the reserved-act half of D2 binds in Phase 1 (host-enforced); its declared-checkpoint half, WD I-7 and V4-HI-42 are guidance in Phase 1. Lapse recording continues in Phase 1; re-hold is governance phase. Governance-phase fixture values are stated to read the checkpoints as if declared governed | S-C10, §0, §3.1 rule 3, §6.2, §10.1, §10.4 |
| R8-7 (answered standings; 03.1, 04.4, 07.3–07.5, 11.1, 18.2, 21.1, 24.1, 26.1; Part 4.11) | SWBPIPE answers added to UNRESOLVED effects (U-C2, U-C4, U-C5, U-C6, U-C7, U-C9, U-C10, U-C11; host adoption; OI-021; V-ED1), FXA-1, §3.1 host adoption and the §10.4 counterparts paragraph, each as an answer about SWBPIPE's current state (DECISION-3) | §3.1, §10.1, §10.4, UNRESOLVED |
| **R8-12** (items 3, 7; closing pass, node A6, in place) | Item 3 confirmed: the §8 map cells stay *unagreed* (SWBPIPE described its state and agreed to nothing) and the note beneath the map is kept — no edit. Item 7: consumed inputs list the post-R8 sibling versions | Header |
| V9 N-2 — in place | §4.1 V4-HOST-02 sentence carries the "pending owner clarification (R8-9)" marker. Wording otherwise unchanged |
| **R8-13** (DECISION-5; SETTLED; in place, no version bump) | §4.1: the V4-HOST-02 "pending owner clarification (R8-9)" marker is replaced by the revised V4-HOST-02 in the recorder's wording confirmed by the owner (DECISION-5), flagged for the next accepted-basis update. It governs the host's embedded agent, not the external channel, and changes no §4.1 result or §6 standing | Header, §4.1 |
| R8-13 close — in place | The owner confirmed DECISION-5 (the reading of "MCP V2"; the person-only grant stands), so the "open to the owner's correction" markers are closed. The consumed-input line is corrected: OWNER_DECISIONS.md is cited in its state that adds that confirmation, not at `1528a5033` |
| V10 S-1…S-4 — in place | The wording of the DECISION-5 confirmation is made precise (the "MCP V2" reading was confirmed; the person-only grant was not objected to and stands). The revised V4-HOST-02 is "the recorder's wording confirmed by the owner". The always-off item reads "a silent switch". ACT F-22 is updated. No rule changes |

No fixture identifier is added, removed or re-meant; the fixture's own values (FX-PIPE-01) are unchanged. New UNRESOLVED identifiers: **U-C12**, **U-C13**. Closed: the model-destination host-restriction row.

## Changes from v0.4

v0.4 = C-v0.4 (committed; unchanged at `8fb51f07f`).

| R5 / V3 item | Change |
|---|---|
| **R5-7** (V3-A MAJOR-3, MAJOR-5) | §10.4 new named variant **V-GR1** (run 13 of WD-EX E1d on E; GR-1…GR-3; sub-variants GR-P, GR-R, GR-S; main-order negative; SP-6 cost). Main timeline unchanged; FXA-5 states ⟨rev-3⟩ declares no `CP-grant` |
| **R5-1** | FXA-5 and V-GR1 use the four hold-support values: run 12 and V-GR1 on E **enforced by the host loop**; `CP-accept` via X **not established** (SQ-02); `CP-grant` via X **not established** (HS-3 on OP-C9 while SQ-02 is unanswered; corrected by R6-2) |
| **R5-2** | FXA-5: the host loop's own evaluation makes run 12's constraint **host-held** |
| **R5-4** (V3-B m-1) | §4.1 model-destination note split: "may flow; no gating" SETTLED by DECISION-2 (D5); record/show per turn (requested vs effective; unknown turns; run-level set; no new run on switch) labeled **INTEGRATION (DECISION-2 reading)** |
| **R5-9** (V3-B Y-7, m-6, m-11; V3-A m-3) | §4.1 "as of C-v0.5 / P-v0.5"; §9 and VC-C-04 cite P-v0.5; FXA note updated (DEL-04-03 now OF-n; cite FXA-n); V-ED1 stated to replay T1–T15 on e1 and publish e2 before T16; header states EXEC/ADAPTER/XT v0.2 texts were not read this pass |
| R6-2 (V4-B MAJOR-1; V4-A MAJOR-3; in place, no version bump; R6_RESOLUTIONS sha256 8703e85a…b841) | V-GR1 and the R5-1 row: `CP-grant` via X is **not established** (HS-3 on OP-C9 while SQ-02 is unanswered), not "not enforceable" |
| R6-4 (V4-B m-3; in place) | FXA-5 names `CP-check` (not enforceable via X, HS-5) as well as `CP-accept`; the X run is unsupported. No stale "pending"/"to add" markers found in C (remaining "pending" words are OI-021 and A12 states) |
| R6-5 (in place) | C states no "model-supplied → not enforceable" rule; nothing to change |
| **R7-4 m-3** (V5 m-3; in place, no version bump) | V-GR1 last sentence adds "; E1d's `CP-check` is *not enforceable*, so the run via X is *unsupported* (EXEC MT-16)". This completes the R5-1 and R6-2 rows above, which give `CP-grant` via X only: run 13 inherits E1c's `CP-check` (HS-5), so the workflow result via X is *unsupported* whatever SQ-02 returns. No value changes (V5 §3) |

New fixture identifiers: **V-GR1**, GR-1, GR-2, GR-3, GR-P, GR-R, GR-S, run 13. Every other ID unchanged; removed: none.

## Changes from v0.3

v0.3 = C-v0.3 (committed; unchanged at `f05c7e4cd`, including the R3-4 in-place edit).

| R4 / source item | Change |
|---|---|
| R4-1 (DECISION-2 D5) | §4.1 model-destination note: recorded and shown, not gated; changes no result or standing |
| R4-13 (ADAPTER F-2, F-4) | §4.1: App-side configuration never A13 evidence; host refusal is the authoritative "off" |
| R4-14 (ADAPTER F-1) | §4.1: relayed constraint carries its carriage assurance (defined in P §3.3) |
| R4-16 (ADAPTER F-7) | §4.1 *channel not enabled* reporter: App (own configuration off, no host request) or host (host channel off) |
| R4-18 (V2 MAJOR-1) | T15 unchanged and confirmed as the one grant fixture (class P-03, scope {FX-W1; {S-4}}, ⟨set-2⟩); consumers re-point |
| R4-19 / V2 m-5 | Fixture assumptions renamed **FA-n → FXA-n** (alias kept) to end the collision with DEL-04-03 FA-1…FA-9 |
| R4-19 / V2 m-8 | FXA-5: the fixture workflow ⟨rev-3⟩ declares `CP-accept` and `CP-check` (WD-EX E1); CP-accept arrival T10, resolution after T11 |
| R4-19 / V2 m-12 | Nothing in C to close (C's own notes already satisfied) |
| V2 §3 ("conversation K-7") | K-7 declared as run 12's conversation |
| **R4-20** (EXEC F-15) | App-side subjects **LIB-A1** ⟨fx-proj⟩, **LIB-A2** ⟨fx-app-import⟩ (holding library), **AF-1** App file with file content identity |
| **R4-20** (XT F-5) | Editions **e1**/**e2** named; edition-addition variant **V-ED1**; §8 extension route cites it |

New fixture identifiers: LIB-A1, LIB-A2, AF-1 (⟨AF-1@f1⟩, ⟨AF-1@f2⟩, ⟨m-fx-file⟩), e1, e2, V-ED1, K-7. Renamed: FA-1…FA-5 → FXA-1…FXA-5 (alias). Every other existing ID unchanged; removed: none.

## Changes from v0.2

v0.2 = C-v0.2 (sha256 358182b1…6d82, 577 lines, committed at `c387730fb`).

| R2 / IR1 item | Change |
|---|---|
| R2-1; IR1-A IR1A-01; IR1-B B-M1; IR1-C IR1C-10 | Fifth class value renamed **no policy basis** with reason sub-element {omitted, unassigned, pending OI-021}; five values listed; fifth marked INTEGRATION |
| IR1-B B-m12 | Value standing mirrors DEL-04-01 §8.1 (adds settled-by-basis, INTEGRATION) |
| R2-2; IR1A-08 | Class rule 1: operations that *perform* A4–A7, A10, A12, A13 (incl. act-state changes) reserved; no faithful record through them; host faithful-record operation conditions and relay question (U-C11) |
| R2-3; R2-11; IR1A-16 | S-C10/S-C11 credit D2/D3 only with what they say; disabling A13 INTEGRATION; App A14 restriction attributed to R-2 |
| R2-4; IR1-B B-M4, B-M5, X-7; IR1C-11; IR1A-02, IR1A-10 | §2 inv. 5: class never implies exposure; reserved entries always offered; A8 *offered*, not auto-recorded. §4.1: reporter column; *not exposed* reported by host only and relayed; loop-side *not offered* named |
| R2-9; IR1A-17 | Class rule 4: no-policy-basis wording; A12 widening refused; fixtures report held (V-NP1) |
| R2-12 | Class rule 3 and §4.1 *not permitted* name the governing checkpoint constraint; §8 map row for its host receipt; V-CP1 |
| R2-13; IR1-B B-M7 | §5.4 "no longer holds" = per-item subject-identity check on relied-on targets; own-effect case named; dedup precedes basis check; T7 per-item; **T13 fixed** |
| R2-14; IR1-B B-M6 | §3.3 resulting-object reporting; §5.3 use; §9 forward table adds resulting objects; T12 names S-5 created |
| R2-15; IR1A-06; IR1-B X-5 | **OP-C10 Undo** added; §2 inv. 1 names undo; §6.2 rule 4 undo lapses changed content; T16a/T17 lapse demonstration; relation "reverses" |
| R2-5; IR1A-03 | §6.2 act-declined and run-ended events carried as events |
| R2-7; IR1A-13; IR1-B B-m1 | Lapse vocabulary adds "matches c₀ again after observed lapse" and *superseded* (A12/A13) |
| R2-17; IR1-C X-10 | §5.3 held-call targets bound through relied-on subject identities |
| R2-21; IR1-B X-6, B-M8, B-M10, B-m10; IR1-C IR1C-15 | §10: all v0.2 IDs kept; fixture assumptions FXA-1…FXA-5 (exposure = exposed ×3 as fixture assumption; §8 map stays unagreed); **OP-C11** no-policy-basis entry; **OP-C12** host check entry; OP-C3 stays Examine (A3) and clarified; T4a; T15 scope in R-8 dimensions (model/workspace + object set, compatible with DEL-04-02/04-03 aligners) with OP-C5-on-S-4 held on U-02; named settings ⟨set-1⟩/⟨set-2⟩; named variants V-S1, V-CP1, V-NP1, V-R1, V-X1, V-OU1; local-label rule `L-‹file›-n`; SoW-scope note |
| R2-6 | FXA-4 ⟨set-1⟩ = effective (policy default), no setting actor |
| R2-16; IR1-B X-8 | V-S1 display wording |
| IR1-B B-m6 | §4.4 precondition vs validation error rule |
| IR1-B B-m5 | One evidence-label mapping published (Verification cases) |
| IR1-B B-m11 | §4.2 fixtures state remedies as meanings |
| IR1-B §5 SoW fidelity | §10 states the shared fixture is an integration assignment, not SoW scope |
| Commit read rule | Sibling v0.2 texts read from `28bd00499`; hashes in header |
| R3-4 (R3_RESOLUTIONS.md sha256 202d52c7…afbf; in-place edit, no version bump) | OP-C10 class now cites the policy record of the operation whose receipt it reverses (INTEGRATION); closes W3 finding F-R2-4 |
| Coordinator R2 notes (DEL-04-02/03 aligner items) | §4.1 reporter of *not exposed* stated as host-reported from element 9, relayed by loop/adapter, separate from loop-side *not offered*; T15 scope reduced to model/workspace + object set for compatibility with the DEL-04-02/03 fixtures |

Fixture identifiers added: OP-C10, OP-C11, OP-C12, T4a, T16a, S-5 (created at
T12), ⟨set-1⟩, ⟨set-2⟩, FXA-1…FXA-5, V-S1, V-CP1, V-NP1, V-R1, V-X1, V-OU1.
Changed meaning (IDs stable): T7 (explicitly per-item), T13 (dedup before
basis check), T15 (scope in R-8 dimensions), OP-C3 (result wording), all
entries' exposure (exposed ×3 by FXA-1). Removed: none.

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| `UNRESOLVED{OI-021}` operation-specific reserved additions; first connected operation, autonomy, environment | Owner via outside SWB session and App/shared owner | Before connected SoW / live examination | Classes for OP-C4/C5/C9 carry "OI-021 additions pending"; OP-C11 is *no policy basis (pending OI-021)*; all examples invented. Stays open (R8-10): SWBPIPE selects nothing (SQ-04); its candidates (27 change kinds; DRAFT #885's Node `position.x` set_field; validate-only preview; solve integrity standing; user rule checks) are not FX-PIPE-01 identities |
| `UNRESOLVED{OI-003}` (App v4 OI-003; unrelated to SWBPIPE's OI-003) retain / narrow / defer extension promise | Owner with host contract owner (DEP-03-01-027); trace from DEL-09-09 (DEP-03-01-030) | Before claiming extension or fixing AC-007 criterion | Map (§8) stays *unagreed*; promise preserved, not claimed. SWBPIPE has no catalog editions (SQ-26); its participation is a SWBPIPE owner decision |
| `UNRESOLVED{OI-014}` shared contract/component placement | App/shared contract owners | Before structural/production allocation | Map rows for shared types and loop-side checking left open |
| `UNRESOLVED{OI-013}` per-host loop placement (loop-side argument checking) | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary | §8 row held as a question |
| Host adoption of D2 list, D3 rule and R2 treatments | Host owner / SWBPIPE (DEP-001) | Before host conformance | Class values are App/shared; host adoption "not evidenced". SWBPIPE (SQ-05): no class system, no named reserved list; every change waits for the person's Apply; autonomy is SWBPIPE owner decision OI-016 |
| Consequence vocabulary (DEL-04-01 U-02) | DEL-04-01 with host policy owner | Before class assignment for connected operations; before a consequence scope dimension is used | §3.1 consequence statement empty; T15 scope uses model/workspace + object set only; OP-C5 on S-4 under ⟨set-2⟩ held on U-02 |
| U-C1 Serialization, content-identity algorithm, method-designation scheme, catalog/schema placement, adapter realization (TBD-003) | App/shared capability-contract owner with host/consumer owners (DEP-03-01-028) | Before dependent schema implementation/conformance | All element names semantic; identities opaque |
| U-C2 Host definition of generation; lapse/stale under generation change and restore | Host owner (DEP-03-01-025) with DEL-04-03 | Before basis conformance, lapse display criteria | Tg fixture only. SWBPIPE DRAFT #885: a new workspace id and generation on a published-project change; cross-workspace reuse rejected; archive restore not addressed (SQ-07 (b)) |
| U-C3 Host confirmation of the per-item stale rule (R2-13 as amended by R8-3) and subject-identity scope (FXA-2/FXA-3 assumed in fixtures) | Host owner with DEL-03-02 / DEL-03-01 | Before stale behavior and lapse conformance | Contract rule fixed as INTEGRATION; R8-3 adds the host's stated scope where no subject identities are supplied. SWBPIPE answered: whole-model identity and whole-model staleness only (SQ-03, SQ-07 (d)); per-item host behavior unevidenced |
| U-C4 Multi-read reliance: which cited bases must hold | Host owner with DEL-03-02 | Before stale implementation | §5.4 requires citing each. SWBPIPE: no multi-read reliance concept (SQ-07 (g)) |
| U-C5 Where agent findings are held; whether host-stored findings are a change | Host owner | Before V4-EXM-21 fixture binding | OP-C3 findings requester-authored. SWBPIPE: no findings storage on main; DESIGN agent cards held by reference; whether storing a finding is a change is undecided (SQ-24) |
| U-C6 Host behavior on entry-version mismatch | Host owner | Before adapter implementation | §7 requires explicit error meaning. SWBPIPE: no per-entry versions; one engine crate version (SQ-12, SQ-18 (e)) |
| U-C7 Actual host catalog, tables, diagnostics, availability, exposure, content identities | Host owner / SWBPIPE (DEP-03-01-025; DEP-001) | Before host conformance claim | Examples invented; exposure assumed (FXA-1). SWBPIPE: no exposure element, and "not exposed" arrives as `unsupported_change` / `unsupported_method` (SQ-11); no capability catalog (U-C13) |
| U-C8 Actual M3-CP executable return (V1-B X-08); reconciliation with DEL-04-01 (ACT-POLICY-v0.7 at Wave A; this row named v0.3 through C-v0.6) | DEL-03-02; DEL-04-01 | V2 comparison; AC-004 closure | AC-004 held |
| U-C9 Whether hosts publish version compatibility statements | Host owner with DEL-02-01 | Before DEL-02-03 required-tool fixtures | Equality only until then. SWBPIPE: none (SQ-18 (d)) |
| U-C10 Host confirmation of non-mutating basis handling (§5.4) | Host owner | Before V4-EXM-21 binding | PROPOSED rule only. SWBPIPE: solve and rule checks run on the current model, results are cleared on any change, and there is no cited-versus-evaluated basis statement (SQ-07 (h)) |
| U-C11 Whether any host offers a faithful-record operation meeting R2-2's conditions (relay) | Host owner (DEP-001) | Before host act-recording integration | None assumed in fixtures. SWBPIPE: none (SQ-21) |
| Governing-checkpoint-constraint receipt on the host route (relay, R2-12) — governance phase (R8-1) | Host owner with DEL-03-02. SWBPIPE: SQ-02 answered 2026-09-28, route (iv), none planned; planning one is a SWBPIPE owner decision (ANS §2) | Before the governance-phase V-CP1 / LOOP FX-C9 / PANEL PC-24 / WD VC-11 execution | Phase 1: none; the App carries no constraint (R8-10). Governance phase: V-CP1 AWAITING INPUT — SQ-02 answered: no receipt and no host copy (not offered); host joins deferred (DECISION-3) |
| *Closed (DECISION-K1 K1-2, 2026-09-30).* SP-6 cost at grant checkpoints: the person may repeat a grant change whose content is already in force (V-GR1 main order) | The owner (decided; U-E4 / U-31) | — | In the current phase the earlier A12 counts while ⟨set-2⟩ is in force (EXEC SP-6); the cost arises only under the governance-phase option EXEC SP-6F |
| ~~Host restriction of its own external channel by model destination (R4-1)~~ **Closed** (R8-7): SWBPIPE answered SQ-16, no restriction, so the App states nothing | — | — | None on meaning; App records/shows destination only |
| Host confirmation that a catalog-edition addition is reported as an identified event (V-ED1) | Host owner / SWBPIPE (IN-11, SQ-26) | Before DEL-09-09 TS-1 | V-ED1 is a fixture; SWBPIPE has no catalog editions and no edition-addition event (SQ-26) |
| U-C12 Per-subject content identity (V4-HI-32) not met by SWBPIPE, which supplies only a whole-model identity (SQ-03; R8-4) | SWBPIPE owner (PB-TBD-002 / DEL-16-03); owner notice | Before host act-binding and lapse integration | §5.3 receives the whole-model identity for every covered subject: over-lapse, never under; resulting objects beyond target ids *not supplied*. SWBPIPE's DESIGN Checked mark carries a row-content hash, so per-row identity may arrive with that tranche (a SWBPIPE owner decision) |
| U-C13 No capability catalog on SWBPIPE: no per-operation identity or version, no editions, no exposure element; hand-built CLI (SQ-11, SQ-12, SQ-18 (e), SQ-26; R8-10) | SWBPIPE owner; owner notice | When the owner resumes UI-SUCCESSOR (DECISION-3); before any required-tool check or V-ED1 trace against SWBPIPE | Record only; no App rule changes. WD required-tool references cannot resolve against SWBPIPE (EXEC EV-4 → *not established*) |
| Register (restated at v0.7 against the registers as read 2026-09-30). Now registered: the C → DEL-04-02 and C → DEL-04-03 joins, on the consumer side (DEP-04-02-016, DEP-04-03-023); and DEP-03-01-031 here (UPSTREAM, the DEL-04-03 act field set and lapse vocabulary; SCA-V4-001). Still absent: DEL-03-02's DOWNSTREAM mirror of DEP-03-01-026; this register's DOWNSTREAM mirrors for DEL-02-01, DEL-02-03, DEL-03-03, DEL-03-04, DEL-04-02, DEL-04-03, DEL-05-01, DEL-05-02, DEL-09-06, DEL-09-09 and DEL-10-03; DEP-03-01-022 still names PKG-02 at package level (V1-B RF-04/05/08; V1-C RF-1; C1-B M-01-1…M-01-8, M-02-1) | Register owners, through `dependency-extract` (DAG-003 HANDOFF open matter "Deferred supplier-side mirror rows") | At the next register refresh; no arc waits on it | None on content. No register is written in Wave A (R9-10) |
| ~~SoW text (REQ-002, TBD-001) still calls OI-001/OI-002 open~~ **Closed** (R9-8): REQ-002 and TBD-001 were revised under SCA-V4-001 (AX-004) and now record the D2/D3 ruling; OI-021 and DEP-001 stay open there | — | — | None. This design applies DECISION-1, as the SoW now does |
| ~~U-C14 A read lacking workspace identity or generation: citable or *basis incomplete* (R10-5; R12-9)~~ **Closed** by R13-1 (RP-2 repair) | — | — | §5.2 rule 1 states the ruled rule: citable only when the host declares it supplies neither, with the limit "basis lineage not supplied"; an omitted element stays *basis incomplete*. SH-1's *no lineage* profile exercises it (§10.8) |
| U-C15 Host adoption of the catalog-level interface (§2.1 CI-1…CI-4, the basis profile, edition identity rules) | Host owner (DEP-03-01-025) | Before host conformance and before DEL-09-09's V-ED1 trace | PROPOSED meanings, exercised on SH-1 only. SWBPIPE: no catalog, no editions and no event (U-C13; SQ-26) |

## Verification cases

Designed. **Run at v0.8, on the simulated host SH-1 only (§10.8; label
*test-double*):** VC-C-04 (without an App candidate), VC-C-09 and VC-C-10,
and the X-path part of VC-C-02 and VC-C-03. The rest are not run.
**Evidence-label mapping** (one mapping, owned here per V1-B D-19 / IR1-B
B-m5):

| C/P label | DEL-05-01 LOOP §12 | DEL-05-02 PANEL | Can support |
|---|---|---|---|
| *illustrative* | CONTRACT-REVIEWED | DEFINED | Completeness of the definition only |
| *test-double* | FIXTURE-EXECUTED | EXECUTED (on a test double, with configuration and date) | The expectation holds for that double; nothing about the host |
| *actual host* | HOST-OBSERVED | EXECUTED on an identified host candidate | That candidate only |
| (no evidence) | NOT-OBSERVED | AWAITING INPUT (named input) / HELD (named decision) | Nothing; recorded as a gap |
| (partial) | — | LIMITED | As stated in the limitation |

Fixture steps and variants refer to §10.3–§10.4.

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-C-01 Entry field coverage | For OP-C1…C12 and a real host entry when supplied, check the nine §3 elements, §3.1 sub-elements and §3.3 extras against V4-HI-02, SOW-157–164, R-2, R2-1, R2-2 | Every element present; class shows adopted/DERIVED/INTEGRATION value with policy record reference, or *no policy basis* with reason; OP-C6/C7/C8 reserved; OP-C11 no policy basis (pending OI-021); no OI-002 value; value standing from the §8.1 list; exposure values present | VER-001 |
| VC-C-02 Cross-channel read parity | OP-C1 at T3 via H, E, X; compare content, subject identities, diagnostics, standing | Identical meaning and standing; mismatches listed; evidence labeled per the mapping; type match alone does not close a consumer claim | VER-002 |
| VC-C-03 Non-success parity and separation | T8 on H, E, X; V-R1; V-X1; V-NP1 direct; a loop call to an operation absent from the offered edition | T8: same *unavailable*, reason, evaluated basis B2 on all three; V-R1 → *not permitted* + A8 offered (not recorded); V-X1 → host-reported *not exposed*, relayed; channel off → *channel not enabled* with its reporter (App from own configuration, no host request; or host); V-NP1 → *not permitted*; absent operation → loop-side *not offered*, never dispatched, never labeled *not exposed*; none is an empty success. SWBPIPE-form variants follow §4.1: `unsupported_change` → host-reported *not exposed*; `controller_unavailable` → *endpoint unavailable* with the channel *disabled* (R8-5, R8-6) | VER-003 |
| VC-C-04 Read-to-action basis trace (M3-CP receiver) | T3 → T5 → T6 → T7 → T9 → T10 → T11 → T12 → T13 using P-v0.8 §11; run on SH-1 at v0.8 (§9, §10.8) | All elements incl. method designation at every read; PR-1 reference = B1 throughout; T7 refuses both items per-item with B1 and B2; PR-2 new identity citing B2; T12 association PR-2/item 1/B2/RC-1/r14 with resulting objects S-5, R-100; T13 answered from recorded state (no stale refusal from its own effect); whether RC-1 itself carries B2 recorded as a host observation; no step rewrites a reference | VER-004 |
| VC-C-05 Standing, attribution and lapse | T2, T4, T4a, T6, T12, T14, T16a, T17; V-GR1 GR-1…GR-3, GR-P, GR-R, GR-S | T2 A4 carried with full act fields; not lapsed after T6; lapsed after T14; A5 on item 1 not lapsed by T12; T16a A4 lapsed by the T17 undo; T4 findings never shown as checked or host check; T4a "host check failed: support spacing" with its basis, historical after r12; no act inferred from success; V-GR1: A12 counted when established, whether captured after the arrival (GR-2) or before it while ⟨set-2⟩ is in force (main order; EXEC SP-6, DECISION-K1 K1-2); refused/pending A12 supersedes nothing. V-GR1 is walked in both phases: in Phase 1 the dispositions label the record and nothing is held; the governance-phase reading holds the call (R8-1) | VER-005 |
| VC-C-06 Responsibility map review | Walk §8 against H/E/X, CLM-001–003 and receiving rows (PKG-02, DEL-03-02, DEL-04-01, DEL-04-02, DEL-04-03) | Each cell valued; no *generated/checked* without a conformance route; fixture exposure (FXA-1) not used as map evidence; host implementation external | VER-006 |
| VC-C-07 Extension treatment | Compare §8 extension text and element 9 with V4-PAR-05, V4-HI-03, #d4, OI-003, V4-EXM-24; walk V-ED1 | Promise stated; `UNRESOLVED{OI-003}` with owner; trace route via DEL-09-09; no automatic availability/savings; real exposure values *unagreed*; V-ED1 yields *missing* on e1 and full discovery on e2, with no availability claim | VER-007 |
| VC-C-09 Schemas and instances (v0.8) | Run `prototype/validate_all.py`: check that each of the eight PKG-03 schemas uses only the validator's keyword subset; validate every valid and invalid instance; with `--run`, validate every SH-1 host document and change request | Every schema within the subset; valid instances pass and invalid ones fail with the stated error; every host document validates; conformance rule CX-1 (§3.5) holds on every catalog instance; the three V18-3 R-7 mutations are rejected. **Run 2026-09-30: all passed (8 schemas, 22 instances, 30 host documents, 6 change requests). Rerun at RP-2, 2026-09-30: all passed (8 schemas, 27 instances, 3 mutations rejected, 30 host documents, 6 change requests)** | VER-001 |
| VC-C-10 SH-1 over both paths (v0.8) | Run `prototype/run_fixture.py`: the §10.8 case list over the MCP-tool and command-line paths | Each case as §10.8's table states; the two paths give identical host documents for the same request. **Run 2026-09-30: 21 of 21 checks passed (test-double). Rerun at RP-2: 22 of 22 (the R13-1 rule added)** | VER-002 (X paths only), VER-003, VER-004 |
| VC-C-08 Boundary and open-input audit | Check each REQ-007 exclusion and each UNRESOLVED row; check DERIVED/INTEGRATION/PROPOSED markings against R1/R2; check D2/D3 attribution (R2-11) | Every excluded act maps to its owner; each open input has owner, point of need, effect; no host delivery, SWBPIPE adoption or joined qualification claimed; no rule credited to D2/D3 beyond their text | VER-008 |
