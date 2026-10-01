# Proposal, validation and outcome contract
- Contribution: DEL-03-02/P-v0.8 (supersedes DEL-03-02/P-v0.7, last changed at `c896a99d90` and unchanged at `86cafc0e1c`, file sha256 b2b67e656081e41364031c067ca8272240d1f80730e09da262d7d05fbcca6b6e; P-v0.7 superseded DEL-03-02/P-v0.6, last changed at `f5ceef164a` and unchanged at `3dd7c22c73`, file sha256 410fb289e16177e11190db45be37e02b5d82ebf7a9fcff8676e938bb23a51af9; P-v0.6 superseded DEL-03-02/P-v0.5, last changed at `375c3970c` and unchanged at `94aa9181b`, file sha256 6ab94fd10166cf78cda014a2f28ebf4726ce9f82a1c2f180044093b4bbb137e0)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Phase (R8-1; R9-1): in the current phase (Phase 1), this increment, declared workflow checkpoints are **plan guidance** (EXEC-v0.5 §2.1; WD-v0.7 §4.3.0). The governing checkpoint constraint, its carriage assurance (R2-12) and hold support are the **governance-phase definition (retained)**, stated beside a Phase-1 statement. V4-WF-05 and V4-HI-42 are cited as amended by SCA-V4-001 (accepted 2026-09-29): in force in every phase, the required human act is requested, it is recorded as done only when the person performs it, and the reserved acts bind; holding the run until the act is **phased to the governance layer, not withdrawn** (§0). SWBPIPE's answers are recorded as answers about its current state, not commitments; host joins are deferred (DECISION-3)
- Serves: OUT-001 (proposal, relied-on basis, origin, governing checkpoint constraint, change-item content identity and outcome schema meaning; at v0.8 also two PROPOSED JSON Schemas beside this file, R12-1), OUT-002 (lifecycle, one route, actor parity, host ownership and receiving interfaces), OUT-003 (designed contract fixtures); REQ-001–REQ-013; AC-001–AC-014; VER-001–VER-014
- Wave B (run APP-V4-DESIGN-PASS-2-20260930, node B3; v0.8): design development under R12 (R12_RESOLUTIONS.md sha256 95f3011b436b6faa3de098059e77eac836c165e0bb98a5ed94e28918a3a749a1: R12-1…R12-4), for S1-B items P 4, 5 and 7 (SURVEY/S1-B.md sha256 eae76ecf9e941bb841fbc3a655a8e887c7684b8d47ef7728f4809992b0b6587d §2.5, §2.8), under BRIEFS.md sha256 ccb4d9f036fb7ff531fffa0d309533b15cf1ebb39b0320651ed4bd5d88efc550 ("Common rules", "Wave B", row B3) and OWNER_DECISIONS.md sha256 1dfd5bf4619b329719136b1646030e3f871fd7ffc52dbfd12265414e515aaf15 (DECISION-K1 K1-6). SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` SQ-07…SQ-09 re-read at sha256 afb6e063… (data, not commitments). C-v0.8 and ADAPTER-v0.6 were developed in the same node; other siblings are cited at their Wave A labels. New files beside this one: `proposal.schema.json`, `proposal_state.schema.json`, their example instances, and `prototype/` (the §4.6 table and derived-state rule as executable checks; not product code). The simulated host is DEL-03-01's SH-1 (C-v0.8 §10.8), cited, not redefined. **Repair RP-2 (same run, in place, no version step):** R14_RESOLUTIONS.md sha256 c6a603303693f50e24ea27fcbc9f381a297434e4182f023fbcee941073623576 (R14-6, R14-8; binding), with R12_RESOLUTIONS.md R12-7 and the four receiver comparisons `comparisons/V18-1.md`…`V18-4.md` (sha256 prefixes fb07e07c66c1, 0b00e79b161b, 68a067e26af7, 078113d7055b), under BRIEFS.md sha256 e3f98d1c8449292965dd244a0f2821b221bcd0f3b0294e592f73b8eaaaaf6321 ("RP", row RP-2); siblings are named at their Wave B labels where a repair row says so
- Basis (re-pinned in Wave A, R9-5; each sha256 below recomputed with `shasum -a 256` on 2026-09-30, working tree at `3dd7c22c73`): the accepted basis as amended by SCA-V4-001 (accepted 2026-09-29) and SCA-V4-002 (in these four files, HOST_INTEGRATION line layout only) — `P/docs/HOST_INTEGRATION.md` (sha256 d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f) §1, §§3–5 (V4-HI-11, V4-HI-20–25, V4-HI-30–33), §6 V4-HI-40–42 (V4-HI-42 amended), §7 V4-HI-50–52, §9 V4-HI-70–71 (V4-HI-70 amended), §10, §11; `P/docs/PRD.md` (sha256 bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd) V4-WF-05 (amended; cited in §0), V4-PAR-04, V4-AUT-01–05, V4-REC-01, V4-CST-05/06, §9 OQ-02/OQ-11; `P/docs/ARCHITECTURE.md` (sha256 317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c) V4-ARC-20; `P/docs/EXAMINATION.md` (sha256 471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0) V4-EXM-20/22/25 (V4-EXM-22 amended); ScopeOfWork.md sha256 3560915142ebfbf3fa7197008ea3b0660584665c9d86260b22b550c5c2354d0f (revised under SCA-V4-001, its AX-004: OUT-001, CLM-003, REQ-004, REQ-008, REQ-012, AC-009, AC-013 and TBD-001); DECISION_BRIEF #d2/#d3/#d4/#d5; the accepted graph `_DAG/_LATEST.md` → DAG-003 (accepted 2026-09-29); SCC-CASE-002 Case_Datasheet rows M1-P, M3-CP (sha256 a12abfaf82c34ae1e7c10d8b553d3e1a0da4772b160e02257c0bf70edce04d5c; additions only since the state pinned below); owner decisions `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` D2/D3 and DECISION-2 D5/D6 (OWNER_DECISIONS.md sha256 a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c, the state that carries both; the DECISION-1 text is unchanged). At v0.6 this line pinned repo 6e18505e3, ScopeOfWork.md 42328987c71dd243323805faf2634067cca0113b81ca93d4d129193b2a71128a, HOST_INTEGRATION.md 08c8fc7d…60da and Case_Datasheet 6acdc6c4…a71a6, each true at `6e18505e3`, and OWNER_DECISIONS.md f3f8e5f3…81f2e, true at `be8bb46dd3` (history). Rulings, by file: R1_RESOLUTIONS.md (sha256 2f9c7e72…7ec4) R-1–R-9; R2_RESOLUTIONS.md (sha256 77cfb845…d088) R2-1–R2-21; R3_RESOLUTIONS.md (sha256 202d52c7…afbf) R3-3, R3-4; R4_RESOLUTIONS.md at `f05c7e4cd` (sha256 50a009b2…2a24) R4-3–R4-7, R4-12–R4-15, R4-19; R5_RESOLUTIONS.md at `8fb51f07f` (sha256 254d0b93…d6f1) R5-1, R5-2, R5-5, R5-6, R5-9; R6_RESOLUTIONS.md (sha256 8703e85aa7324e233fab285321e277d720923d3e36e342c865917b55083cb841) R6-1, R6-5; R7_RESOLUTIONS.md (sha256 1f6ab3b2355e164f803657ceae08841af92d21a821feede3800a6df861b2a1ea; it rules nothing in this file); R8_RESOLUTIONS.md (APP-V4-SWBPIPE-INTAKE-20260928; sha256 44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b) R8-1…R8-12; R9_RESOLUTIONS.md (APP-V4-DESIGN-PASS-2-20260930; sha256 a64e241519b7d158165a7ede0ffdd22eec0af15b6812b5300755f5f38abd59b8) R9-1…R9-11, with that run's R10_RESOLUTIONS.md (sha256 ad3b6caa4a12660db77abc51b5c02ba70519ee46d55b40d21ee76eb3ca561796) R10-1…R10-11, R11_RESOLUTIONS.md (sha256 e7343b6663b6aeeb2dc506d3391f5b310088e7688d1b21e65d2ba1d8616b3615) R11-1…R11-9 and OWNER_DECISIONS.md (sha256 7458e9e81971676337a34280b4e8b29a7d04fce5fc202da5b9f5cf7ccd8f9ae5) DECISION-K1 (these four recomputed with `shasum -a 256` at node A4, R11-3, at their final bytes; the R9_RESOLUTIONS.md pin in the node A1 input line below records the bytes A1 read) (R1…R5 pins recomputed: current); reviews V3-A (sha256 f25f5af1…1d87) and V3-B (sha256 5662fbd0…54a3) items addressed to P; OWNER_DECISIONS DECISION-2 D5/D6 (via R4-1/R4-2); review V2 (sha256 75ba1dff…e6ef) m-3, m-9, m-11; comparisons V1-A (01811533…4c09), V1-B (09eebfe0…1cae), V1-C (8d46258a…94a6); reviews IR1-A (31b3c7f8…8284), IR1-B (70e4a4f6…2846), IR1-C (295e96b3…26b9)
- Consumed inputs: **Wave A inputs (run APP-V4-DESIGN-PASS-2-20260930, node A1-B; v0.7).** R9_RESOLUTIONS.md sha256 c3efe2ffa232dd9293202d4fc891eba4325afeb2e224fecdf8c1b4c5122a9d2c (R9-1…R9-11; binding); that run's BRIEFS.md sha256 698d91d8217cee528812529fa353faac899b4bc1a5be5686552ad88dad6c469a ("Common rules", "A1 — alignment wave"); SURVEY/S1-B.md sha256 eae76ecf9e941bb841fbc3a655a8e887c7684b8d47ef7728f4809992b0b6587d (advice; each item was checked against the current source before it was applied); the amended basis documents and the revised ScopeOfWork.md as pinned in Basis; R8_RESOLUTIONS.md at its current sha256 44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b (R8-13, added after the state pinned below, rules nothing in this file) and the intake OWNER_DECISIONS.md at its current sha256 5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2 (DECISION-3, DECISION-4 and its clarification unchanged; DECISION-5 appended); SCA-V4-001 AMENDMENT_PACKET/OWNER_ITEMS.md sha256 2b90eb4a95f458e993eed69e27533aa10e31aea980fe2ec99c9c2345e6f498ef items O-4 and O-25, accepted "as recommended" (APP-V4-BASIS-ALIGN-20260928 OWNER_DECISIONS.md sha256 ca8c4e50df1d7dddb41b875a4afe46eea4f1a1bf2491d255b7890d0d71cd254b, DECISION-7); this deliverable's `Dependencies.csv` and the consumers' registers (ACTIVE rows, read 2026-09-30, for the Receivers line and §13; R9-6); `_DAG/DAG-003/HANDOFF_STATE.md`. SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` is cited at sha256 afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74 (current; three lines differ from the 6f01add3…61c7 state read for v0.6, below) and `FACTS_SQ01_SQ32.md` at sha256 733fb88a701317be8f0054937eca058774ba5f5f30c7a27233718996e8b2ab7e; both are data about SWBPIPE's current state, not commitments (DECISION-3). Sibling Design files are cited by version label and section only (R9-5), at their Wave A versions (R9-11): DEL-02-03/EXEC-v0.5; DEL-02-01/WD-v0.7; DEL-02-01/WD-EX-v0.7; DEL-03-01/C-v0.7; DEL-03-03/ADAPTER-v0.5; DEL-03-04/GUIDE-v0.4; DEL-04-01/ACT-POLICY-v0.7; DEL-04-02/AS-v0.7; DEL-04-03/RS-v0.7; DEL-05-01/LOOP-v0.7; DEL-05-02/PANEL-v0.7; DEL-01-01/HOSTING-BOUNDARY-v0.7; DEL-01-01/PIN-SPIKE-v0.1; DEL-09-06/CA-v0.5; DEL-09-09/XT-v0.5; DEL-09-06/RELAY-v0.3. C and ADAPTER were aligned in the same node. The other siblings were edited in parallel by other Wave A nodes, so their Wave A bytes were not read here; the sections this pass compared were read at the preceding versions (RS-v0.6 §4 R11, §7 and §10; AS-v0.6 §3). Sibling byte pins live in GUIDE's input table alone. **Earlier passes (history; true as recorded at each pass, not re-pinned in Wave A).** **R8-12 closing pass (node A6; in place, no version bump).** R8_RESOLUTIONS.md sha256 d4c3423310a857af86692d17ddfdd22fa877ee20b07c46e1ee481d1cd750e7af (R8-12: item 7 applied here). Current sibling versions after R8, as committed at `7a1508452` with A6's in-place R8-12 edits (their byte pins are in GUIDE-v0.3's input table): DEL-02-03/EXEC-v0.4; DEL-02-01/WD-v0.6; DEL-02-01/WD-EX-v0.6; DEL-03-01/C-v0.6; DEL-03-03/ADAPTER-v0.4; DEL-03-04/GUIDE-v0.3; DEL-04-01/ACT-POLICY-v0.6; DEL-04-02/AS-v0.6; DEL-04-03/RS-v0.6; DEL-05-01/LOOP-v0.6; DEL-05-02/PANEL-v0.6; DEL-01-01/HOSTING-BOUNDARY-v0.6; DEL-01-01/PIN-SPIKE-v0.1; DEL-09-06/CA-v0.4; DEL-09-09/XT-v0.4; DEL-09-06/RELAY-v0.3. SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` and `FACTS_SQ01_SQ32.md` are unchanged (data about SWBPIPE's current state, not commitments; DECISION-3). **v0.6 inputs (R8 pass, node A3, at `94aa9181b`).** R8_RESOLUTIONS.md sha256 1770c96e62caf14322811fca82ceb77eca450d3e1be8665cdbdd5550631e8d02 (R8-1…R8-11; binding); INTAKE_MAP.md (I2) sha256 3cc182955c0f3dd70efa0f1c051870229c2ccc08f36c5cf1445f2eef0dd1ea33: rows 01.6, 02.7, 03.3, 05.4, 07.2, 07.6, 08.1, 09.2, 09.3, 10.1, 14.1, 14.2, 22.2, 31.2; Part 2.2 P rows; Part 3 items 1, 2, 5, 10, 11, 12; Part 4.9, 4.11; Part 5 R8-Q12 (R8 overrides I2 where they differ); BRIEFS.md sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517 ("Common rules", "A-wave"); owner decisions DECISION-3 and DECISION-4 with its clarification (OWNER_DECISIONS.md sha256 a5ccab0d39bd1cab37c5556abc9bdedd5341ce76be4712706c8c9d72d623e776); SWBPIPE's delivered answers `RELAY_ANSWERS_SWBPIPE.md` (DEL-09-06 `Design/`, #1047) sha256 6f01add3977761e42ac6b310faf72ba4fd5455e478605deb83fefb2e4d3a61c7: SQ-01…SQ-10, SQ-13, SQ-14, SQ-20, SQ-23, SQ-28, SQ-31, ANS §2–§3 — data about SWBPIPE's current state, not commitments (DECISION-3). **Owner files read first (at `94aa9181b`):** DEL-02-03 EXEC-v0.4 `EXECUTION_COMPATIBILITY.md` sha256 d32be37797a3c367d342a2d13bbb8dd4279bc52934531d83b8c6ec8c6e7b76d4 (§2.1 PH-1…PH-10; §2.2 GV-1…GV-5; §2.3; §3.6; §3.7 CC-2; §4.5 SP-4; §4.11 receiving notes; CH-17, CH-27); DEL-02-01 WD-v0.6 `WORKFLOW_DECLARATION.md` sha256 fce565edfd0cee3fa4583eb292d11cce3e4121ead0cdbed31ba2fe0a52562f28 (§4.3.0 CG-1…CG-7; §4.3.1 `governed`, PROPOSED; §4.3.7); WD-EX-v0.6 `EXAMPLES.md` sha256 950b70b2e3f7fdda9a98b13a63746b76936be490dd96cb6e47bbe6dc9c3eba3d (R-5a/R-5b). DEL-03-01/C-v0.6 is co-revised in the same pass (node A3). Earlier: DEL-03-01/C-v0.5 (co-revised in the R5 pass: FXA-5 hold support and host-held note, V-GR1); the EXEC-v0.2, ADAPTER-v0.2 and XT-v0.2 texts were **not** read for this pass — R5 fixes their meanings used here (V3-B Y-7 note). Earlier: Wave-2 sibling texts read from commit `f05c7e4cd` — DEL-03-03/ADAPTER-v0.1 (sha256 58b2409c…a074: F-1, F-3, F-8), DEL-02-03/EXEC-v0.1 (sha256 e0ede76e…18e8: §4.7 resume/re-hold, MX-3/MX-6/MX-8 confirmation, CAP-1…9), DEL-09-09/XT-v0.1 (sha256 8f098c79…f1df: L-XT-1); DEL-03-01/C-v0.5 (co-revised in this sweep: §4.1 channel reporters and model-destination note, §10 FXA-n, K-7, V-ED1); earlier: DEL-03-01/C-v0.3 (co-revised: §3 elements incl. exposure, §3.1 five class values, §4.1 results with reporters, §4.4 precondition vs validation error, §5 basis, subject content identities and per-item "no longer holds" rule, §10 FX-PIPE-01 incl. OP-C10–C12 and variants); sibling v0.2 texts read from commit `28bd00499` where an R2 ruling touches a join — DEL-04-01/ACT-POLICY-v0.2 (sha256 e50f1fe2…93a9: §2.1–§2.5, §5.1–§5.5, §6, §8.3), DEL-04-03/RS-v0.2 (sha256 56a3f839…1c69: §5 outcome entries, OE-6, §7), DEL-05-01/LOOP-v0.2 (sha256 1151d432…62c9: §6.2 dispatch record incl. checkpoint constraint, §6.3 retry, MC-8), DEL-02-01/WD-v0.2 (sha256 c25bccc5…a55c: §4.3.7 item-level rule, §4.4 promised standing); DEL-04-02 grant display states by R-8/R2-6 meaning; host facilities (route, views, receipts, act capture, constraint receipt): not supplied (DEP-03-02-023)
- Receivers (rebuilt at v0.7 from the ACTIVE rows of this register and of the consumers' registers, as read 2026-09-30; R9-6. A row names a required contribution, not its delivery. The bracketed OUT/REQ/VER tags are carried from v0.6 unchanged): DEL-04-02 [OUT-001, OUT-002; REQ-003–005; VER-003–005] — standing and direct-autonomy origin semantics (DEP-03-02-018; consumer row DEP-04-02-015); DEL-04-03 [OUT-001, OUT-002, OUT-004; REQ-002, REQ-003, REQ-005; VER-001, VER-004, VER-006] — operation outcomes, change-item content identities and host receipt links (DEP-03-02-019; consumer row DEP-04-03-024); DEL-03-03 [OUT-001, OUT-003; REQ-001, REQ-004; VER-001, VER-004] — this same operation contract for the external channel (DEP-03-02-020; consumer row DEP-03-03-007); DEL-03-04 — the responsibility map (DEP-03-02-021; consumer row DEP-03-04-006); DEL-09-09 [OUT-001; REQ-001, REQ-004; VER-001, VER-004] — contract fixtures and outcome expectations (DEP-03-02-022; consumer row DEP-09-09-008); DEL-03-01 [OUT-001, OUT-003; REQ-001, REQ-004; VER-004] — the M3-CP return (consumer row DEP-03-01-026; no mirror in this register); DEL-05-01 [OUT-001, OUT-003; REQ-003, REQ-007; VER-008] — proposal, validation and outcome meaning at the loop boundary (consumer row DEP-05-01-015); DEL-05-02 [OUT-001, OUT-003; REQ-001–003; VER-001–003] — proposal, validation and outcome meaning for the panel (consumer row DEP-05-02-007); DEL-02-01 — change-item content identities, per-item dispositions, the all-items-decided indication, item-left events and applied-outcome object identities (consumer row DEP-02-01-029; arc N-18); DEL-02-03 — the same, plus applied outcomes with their resulting objects (consumer row DEP-02-03-025; arc N-21); DEL-09-06 — proposal and outcome meanings for the connected activity (consumer row DEP-09-06-028); outside the 14 first-increment deliverables, DEL-10-03 — proposal, validation and outcome obligations for the shared responsibility account (consumer row DEP-10-03-012); the external host's proposal-view receiving (DEP-03-02-024). The governing checkpoint constraint semantics that v0.6 listed for DEL-02-01 / DEL-02-03 are governance-phase content (§3.3, §4.4) and no consumer row names them. Arcs N-24 and X-1 do not touch this deliverable

## 0. How to read this definition

This is the 60% semantic definition of how a change, by a person or an
agent, is proposed or applied through a host, and how its outcome is
reported. Element names are **semantic labels, not wire names**. No
proposal-identity representation, content-identity method, schema encoding,
duplicate-effect mechanism, outcome-recovery mechanism, storage engine,
transport field, retry budget or retention interval is selected (TBD-002;
DEP-03-02-026), and no component placement (OI-014; DEP-03-02-025). Unruled
policy appears only as `UNRESOLVED{OI-nnn}`. **DERIVED**, **INTEGRATION** and
**PROPOSED** markings follow R1/R2; owner rulings are credited only with what
they say (R2-11).

**Schemas and the simulated host (Wave B; R12-1…R12-4; PROPOSED).**
`proposal.schema.json` gives the PROPOSED form of a change request (§3) and
`proposal_state.schema.json` that of the recorded state a host returns to a
submission or to an observation by identity (§3.5, §4.6, §9). Each has valid
and invalid instances. Their property names are Chirality's semantic labels:
they select no identity representation, encoding, transport field or
de-duplication mechanism (TBD-002), and no placement (OI-014). Identities are
opaque strings. The proposal route is exercised on the one simulated host,
SH-1, specified in C-v0.8 §10.8 and cited here (R12-4).

§9 is the **canonical outcome taxonomy** for proposals and operations
(R-7). DEL-04-03, DEL-05-01 and DEL-05-02 adopt it and C §4.1 (as of
C-v0.5; carried in C-v0.7, with C-v0.8's two destination rows) unchanged. Fixtures use the shared catalogue FX-PIPE-01 (C-v0.8 §10); step
labels T… and variants V-… refer to it.

**Phase (V4-WF-05 and V4-HI-42 as amended by SCA-V4-001, SETTLED; DECISION-4
D4-1; R8-1; R9-1).** This file summarizes the amended texts in the R9-1
wording:

> When a run reaches a declared checkpoint, the required human act is requested, and it is recorded as done only when the person performs it, whatever the autonomy setting. Holding the run at the checkpoint until the act is performed is phased to the governance layer: in the current phase a checkpoint is plan guidance that the person and the agents manage, and neither the App nor a host's embedded loop enforces a hold, blocks a run, or reports a workflow unsupported because a hold cannot be enforced. The reserved acts (V4-HI-30) still bind.

In force in every phase: the act is requested; it is recorded as done only
when the person performs it; the reserved acts bind (EXEC PH-4, PH-5).
Phased to the governance layer: holding the run until the act (EXEC
PH-1…PH-3).

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

The governing checkpoint constraint (§3.3),
its carriage assurance and the treatment it forces (§4.4), and hold support
are the **governance-phase definition, retained** (EXEC GV-1), for
checkpoints declared **`governed`** (WD-v0.7 §4.3.1, PROPOSED). Where this
file states such a case, it gives the Phase-1 result and the
governance-phase value; the governance-phase values read the fixture's
checkpoints as if they were declared governed (R8-11 item 5; EXEC GV-5).
Nothing in this file's outcome taxonomy (§9) changes by phase.

**SWBPIPE answers (R8; DECISION-3).** Notes marked *SWBPIPE (SQ-nn)* record
SWBPIPE's delivered answers as data about its current state (FACT on main,
or DRAFT #885: unmerged, not qualified, deferred). They are not commitments,
deliveries or adoption. **OI-003** here is the App v4 open issue; it is
unrelated to SWBPIPE's own OI-003 (R8-7).

Settled distinctions relied on (cited, not re-decided):

| Id | Settled distinction | Source |
|---|---|---|
| S-P1 | Every change passes through the host's one validation and application route; no second route for agents | V4-HI-20; V4-PAR-04 |
| S-P2 | An agent's change carries origin (author type, conversation, workflow run) and the basis it relied on | V4-HI-21 |
| S-P3 | Under granted autonomy the agent may apply directly: origin-marked, undoable, checkable later | V4-HI-22; V4-AUT-01 |
| S-P4 | Otherwise a proposal: drafted → validated → queued → accepted → applied (receipt), with rejected / withdrawn / stale, and outcome unknown when unobservable | V4-HI-23 |
| S-P5 | Stale is refused with reason and may be re-drafted on the current basis; later selection never retargets; submitting the same proposal twice has one effect | V4-HI-23 |
| S-P6 | Host views show old and new values, affected objects and why | V4-HI-24 |
| S-P7 | `success` means it ran, never that a person accepted anything; a submitted proposal reports queued until the host records acceptance and application | V4-HI-25 |
| S-P8 | Queued ≠ applied; applied edit ≠ engineering approval; a receipt records the operation outcome, not an act of acceptance | #d3 |
| S-P9 | Acceptance of a proposed edit is not engineering approval; the interface says "accept", never "approve", for proposals | V4-HI-33 |
| S-P10 | Agents never record a human act as performed when it was not; faithful recording (A9) is a conformant record shape | V4-HI-31; V4-AUT-03; R-5 |
| S-P11 | A human act binds to content and lapses visibly when content changes | V4-HI-32 |
| S-P12 | Domain truth and validation stay in the host; Chirality never presents agent output as the host's accepted result | V4-REC-01; V4-CST-05 |
| S-P13 | Autonomy does not override a workflow's declared checkpoints: "whatever the autonomy setting, a checkpoint's required act is requested and recorded as done only when the person performs it" (V4-HI-42 as amended by SCA-V4-001). No grant widens past a reserved act or a declared checkpoint (D2). **Current phase (R8-11 item 2 as restated by R9-2, DERIVED; the R8-11 reading was confirmed by the owner at SCA-V4-001 OWNER_ITEMS O-25):** D2's "no autonomy grant widens past a reserved act" binds, and the host enforces it through its operations. For a declared checkpoint, V4-HI-42's request clause and record clause are in force whatever the autonomy setting; whether the run goes on before the act is for the person and the agents in the current phase, and the host's own treatment of its operations decides what the host does. A forced *propose* (§4.4) and a hold apply only to governed checkpoints in the governance phase | V4-HI-42; V4-WF-05; D2; R8-11; R9-2 |
| S-P14 | **Adopted** (D2): A4 mark checked, A5 accept wherever the active autonomy requires a proposal, A6 approve, A7 rely, A12 changing the autonomy grant and A13 enabling external-agent access are reserved to the person. **DERIVED**: A10 reject is reserved wherever A5 is (R-1). **INTEGRATION**: disabling external access is also a person's A13 (R2-3). The host names and enforces its own list; SWBPIPE adoption is not evidenced. SWBPIPE (SQ-05): no named reserved list; every change waits for the person's Apply, which is A5 in the person's hands | D2; R-1; R2-3; V4-HI-30; DEP-001 |
| S-P15 | **Adopted** (D3): App routine tool-permission/sandbox modes (A14) remain the user's own Codex setting, govern tool execution only and never stand in for a reserved or professional act; hosts have no classifier permission mode; the SWB default proposal mode applies. A14 is recorded only in run record R13 (R2-8, INTEGRATION) | D3; R2-8; V4-HI-41 |

## 1. Host authority map (REQ-002, REQ-013; VER-003, VER-014)

| Facility | Owner | This contract's role |
|---|---|---|
| Domain objects, store and truth | Host owner (SWBPIPE outside session) | None; reads through DEL-03-01 |
| Validation, de-duplication, treatment resolution and the one application route | Host owner | Defines the receiving meaning of its outcomes |
| Receipts, origin marks, undo | Host owner | Refers to them; never manufactures one |
| Proposal views (old/new/objects/reason) | Host owner | Supplies the information the views need (§8; DEP-03-02-024) |
| Offering, capturing, recording and presenting human acts | Host owner (facility); the person (the act) | Consumes captured acts as evidence; never creates one |
| Catalog, read basis, content identities, exposure | DEL-03-01 | Consumed (§3.2) |
| Act names, class records, treatment → outcome map | DEL-04-01; residual policy: owner with App/SWB contract owners | Consumed |
| Grant display states and settings versions | DEL-04-02 (R-8; R2-6) | Supplied: origin and direct-autonomy semantics; consumes settings references |
| Human-act and run-record format | DEL-04-03 | Supplied: outcomes, receipt links, change-item content identity, item-left events |
| Workflow identity; checkpoint declaration; hold machine | DEL-02-01 (declares); DEL-05-01 (evaluates in hosts); DEL-02-03 (Phase 1: recording, EXEC §2.1; governance phase: hold machine and hold-support values, EXEC §2.2, §3.6) | Consumed in origin; governing checkpoint constraint element supplied (§3.3; governance phase) |
| External receiving adapter | DEL-03-03 (host owns endpoint) | Supplied: this same contract, including constraint carriage assurance |
| Integrated host guide | DEL-03-04 | Supplied: §1 and §13 |
| Joined external witness, extension trace | DEL-09-09 | Supplied: fixtures and outcome expectations |

A host-accepted result exists only where the host has recorded the relevant
act. Agent output without that record retains its actual standing
(*drafted*, *queued*, *finding*), never *accepted* (SOW-091). A host refusal
is never a person's rejection (§4.1).

## 2. One route and actor parity (REQ-001; SOW-070)

- Person, embedded agent and external agent submit changes to the **same**
  host validation/application route. The channel is attribution (§3.3), never
  a route selector.
- **Treatment is resolved on the host route** at validation and again at
  application (R-3 point 1). The loop (DEL-05-01) and, where one is on the
  dispatch path, an App adapter (DEL-03-03; none adopted in this increment, R5-2) relay the actor's intent —
  *propose* or *apply directly* — and, in the governance phase, any
  governing checkpoint constraint with its carriage assurance (§3.3); they
  do not decide treatment.
- **Equivalence rule.** For equivalent operation identity/version, arguments,
  relied-on basis and applicable authority, every channel receives the same
  outcome and the same error meaning (identity and text).
- **Permitted difference is authority only** (grant, reserved acts, class,
  checkpoint constraint). It is reported as *not permitted* naming the
  governing treatment — policy-class record (C-v0.8 §3.1) or governing
  checkpoint constraint — never as a different validation error. Per the R-3
  map and R2:
  - a request to apply directly without an *effective direct* treatment →
    *not permitted*; it is never silently converted into a proposal
    (INTEGRATION; for the external channel, now also DEL-03-03 SoW
    REQ-003 as revised under SCA-V4-001);
  - **governance phase (retained; R8-1):** a request to apply directly under
    a governed checkpoint's host-held constraint → *not permitted*, naming
    the constraint (R2-12). In Phase 1 the host's own treatment decides, and
    nothing is reported *not permitted* on a checkpoint's account (R8-11
    item 2; EXEC CH-27);
  - a request to perform a reserved act (S-P14) as the person → *not
    permitted*, with an A8 request *offered*; an A8 exists only if the agent
    actually issues it, with the requester identified (IR1A-10);
  - a *no policy basis* class (C-v0.8 §3.1) → direct *not permitted*; a
    proposal is available but confers no permission — any effect requires the
    person's A5 and host application (R2-1, R2-9, INTEGRATION).
- A denial by the App user's Codex tool permission (A14) happens App-side
  before any host request and is not a host outcome (S-P15).
- **A host that offers no method (R8-5).** SWBPIPE has no direct mode and no
  external Apply. A direct external request is refused `unsupported_method`
  (SQ-06). That refusal is relayed as host-reported *not exposed on this
  surface*, never *not permitted*, and R2-4 (a named rule) is recorded as not
  met by this host. The App never presents the host's no-Apply rule as a
  class value or a grant.
- No fixture or adapter may define an alternate agent mutation path, bypass
  validation, or apply outside the host route (AC-002).
- Person-origin changes use the same route and yield the same basis check
  and outcome meanings; whether a person's direct edit is represented as a
  proposal is host practice.

## 3. Change request elements (OUT-001; REQ-003; SOW-170)

### 3.1 Identities and the acceptance unit

| Semantic element | Meaning |
|---|---|
| Proposal identity | Stable identity of *this* proposal from drafting onward; the unit for one-effect (§7). A **retry** (resubmission after a lost acknowledgment or *outcome unknown*) keeps the same identity and unchanged content (R-7; V1-C AB-05). A **re-draft** receives a new identity (§5). Who mints it, how host handles relate to it, and how it is observed: §3.5 |
| Lineage | For a re-draft: the identity of the proposal it replaces and why (e.g. stale) |
| Change items | One or more items, each with its own item identity within the proposal |
| **Change-item content identity** | An identity of the item's content: operation identity and version, bound targets, old values, new values and the relied-on basis (with relied-on target identities). Method unselected; carries a method designation (C-v0.8 §5.1) (SoW OUT-001 as revised under SCA-V4-001; R-6) |

Rules (R-6):

1. **Acceptance unit = change item.** Row-by-row acceptance is one A5 per
   item. Batch or multi-row acceptance is one A5 act listing several items,
   each bound to its own change-item content identity, with per-item lapse
   (V4-HI-41).
2. **A5 and A10 bind to the change-item content identity**, not to model
   rows. Any change to an item's content (including a re-derived old value)
   is a different item content; an acceptance never carries to it.
3. **Applying the accepted item does not lapse the acceptance.** The item's
   content identity is unchanged by its own application.
4. **A host view row** presents one or more change items. The row is
   presentation; decisions are per item (V1-B D-10).
5. **Sibling drafts (PROPOSED; aligned with LOOP MC-8, IR1-B B-m7, IR1C-16).**
   Several tool calls in one model response each form their own proposal.
   The loop never merges sibling calls into one proposal; items come only from
   one call's arguments. A call that explicitly names an existing proposal it
   extends is the drafter's choice, not a loop merge. A response in which
   one of several tool calls is malformed: the valid calls are handled on
   their own and the malformed one receives its own refusal result; LOOP
   adopts this rule (R12-7, INTEGRATION; LOOP-v0.8 §7 MC-8), PROPOSED until
   the loop's fixture basis is observed. Remaining grouping mechanics:
   U-P9.

### 3.2 Consumed catalog meaning (from DEL-03-01/C-v0.8)

| Element | From C | Rule here |
|---|---|---|
| Operation identity and version | C §3 #1 | The version the request was prepared for; not re-interpreted |
| Arguments | C §3 #3 | Checked against the catalog input schema before host domain validation (DEL-05-01 REQ-003) |
| Bound targets / affected objects | C §3 #3, #5 | Fixed at drafting (§6) |
| **Relied-on basis reference** | C §5.4 | The basis descriptor(s) — workspace identity, generation, model revision, canonical content identity, method designation — of the read(s) actually relied on, and the **subject content identities of each item's relied-on targets**; carried unchanged to every outcome; never replaced by a queue-time or application-time basis, which may be recorded as a separate element |
| Errors, §4.1 results, exposure | C §3 #7, §4.1, #9 | Reused as outcome reasons (§9); no separate vocabulary. Precondition vs validation error per C §4.4 |

This contract defines no separate basis authority (CLM-003).

### 3.3 Origin, attribution and governing constraint

| Semantic element | Meaning | Source |
|---|---|---|
| Author type | person or agent | V4-HI-21 |
| Author identity | The person, or the agent seat instance; or **unverified** where the host cannot verify the caller (e.g. over the external channel). *Unverified* is never presented as a verified person or agent; DEL-04-03 R11 records it as an evidence limit. SWBPIPE records the caller's identity as not verified (SQ-14) | V4-HI-21; V4-HOST-05; R4-15 |
| Seat role meaning | The role meaning in force for the seat, or *unknown* if it cannot be determined | DEL-02-01 SEAT-1 |
| Channel | host interface, embedded agent, external agent | V4-PAR-02 (attribution only) |
| Conversation | Conversation the agent change came from | V4-HI-21 |
| Workflow identity | {kind, origin, source root, name, revision} plus derived-from where adapted. An unadapted carried workflow keeps its original origin; host adaptation creates a new identity with host origin and derived-from. "App-origin" is not an origin class | SoW CLM-003 (DEP-03-02-027); R-9; DEL-02-01 §6.1 |
| Workflow run identity | The run within that workflow. SWBPIPE records neither the conversation nor the workflow run (SQ-14): the App records both App-side and links them by the host's request id | V4-HI-21; V4-HI-70 |
| Standing at drafting | DEL-04-02 grant display state — **effective (person-set)** · **effective (policy default)** · requested by agent · set by person, not yet confirmed · unconfirmed · not set · refused (reason) — with **grant value** (direct / propose) and scope, as known when drafted | R-8; R2-6; R-3 point 6 |
| Settings reference at route decision | The DEL-04-02 settings version identity (or, for *effective (policy default)*, the policy-class record reference and its default) used when the host resolved treatment at validation | R-8; R2-6 |
| Settings reference at application | The settings version in force at application, **host-reported**; otherwise *unconfirmed* | R-8 |
| **Governing checkpoint constraint** — governance phase (retained; R8-1) | Present when a **governed** workflow checkpoint requires A5 on this operation's result: {workflow run identity, checkpoint name, required act A5, operation identity}. Absent otherwise. In Phase 1 the App carries none, and the agent never adds a field the host schema lacks (R8-10) | SoW OUT-001 and CLM-003 (governance phase only); R2-12; R8-1 |
| **Constraint carriage assurance** — governance phase (retained) | How the constraint reached the host route. **Host-held**: the constraint is held on the host side — derived from the host's own resolved copy of the declaration or run association, or received and then verified against that copy; the **host loop's own evaluation (DEL-05-01 §6.2) is host-held** (the host loop is host-built, OI-013). **App-assured**: App code on the dispatch path adds it from the declaration; **not available in this increment** — no interposed App code is adopted (R4-2; D6, closed for Phase 1, R8-2). **Model-supplied**: the model composed it into the call, as in native external realization. **Absent**. A constraint the host merely **received** from an outside caller keeps its source's assurance (model-supplied or App-assured). **Only host-held carriage satisfies R2-12**; the host may record other carriage but does not rely on it | R4-14; R5-2 |
| Reason | Why the change is proposed, in the proposer's words | V4-HI-24 |

Origin and constraint are preserved through submission, every lifecycle
transition and outcome reporting; every dispatch carries origin, seat role
meaning, the grant in force and (governance phase) any governing checkpoint
constraint with its carriage assurance (R-7; R2-12; R4-14). The App-side request origin is recorded by DEL-04-03; the **host
origin mark** is linked, not copied, and a mismatch between the two is an
evidence limit (V4-HI-71; V1-B D-17).

**Constraint authority limit (R2-12; IR1-B X-9; R4-14).** A dispatch-carried
constraint is supplied by the actor's side, so the host cannot tell an
omitted constraint from none. Only *host-held* carriage supports the R2-12
treatment (R5-2); with *model-supplied* or *absent* carriage an omission can
only be recorded afterwards.

- **Phase 1 (R8-1; R8-11 item 2; R8-10).** No hold-support value is
  assigned, and the App carries no constraint. The agent follows the
  declaration as plan guidance and never adds a field the host schema
  lacks. SWBPIPE's batch preflight accepts exact objects only, so a
  constraint sent as a request field would be refused as `invalid_request`
  rather than honoured (SQ-02 (a), SQ-31). The constraint the declaration
  implies may be recorded App-side (DEL-03-03 GC-4). Where the host schema
  defines no element for it, that record carries the evidence limit
  "constraint not carriable on this host" (I2 R8-Q12; adopted in RS R11 by
  R8-12 item 5, backed by R8-10; applied here under R9-8).
- **Governance phase (retained; R8-1, R8-2).** For hold support, a governed
  checkpoint whose held actions are host operations and whose constraint is
  only model-supplied is **not established** while SQ-02 is unanswered, and
  **not enforceable** once SQ-02 is answered with no host-held route (R6-1,
  R6-5; EXEC HS-3). **SWBPIPE answered SQ-02 on 2026-09-28 with no host-held
  route** (route (iv), none planned), so against SWBPIPE the value is **not
  enforceable** (HS-3 (c)). A later SWBPIPE decision to plan a route is a
  revision trigger. On the embedded surface the host loop's own evaluation
  is host-held, but SWBPIPE has no host loop (SQ-20). On the external surface
  R2-12 depends on the host holding the declaration itself. Relay question
  (DEP-001, U-P10), answered by SWBPIPE with none: does the host route
  receive the per-request constraint, or evaluate its own copy of the
  selected workflow's declaration? If a host uses its own copy, the dispatch
  element is still carried for record comparison where the host schema
  defines it. Where a caller-side constraint is omitted although the
  declaration contains it, the omission is recorded as an evidence limit
  (DEL-04-03 R11).

### 3.4 Change item content

| Semantic element | Meaning |
|---|---|
| Item identity | Identity within the proposal |
| Operation | Catalog operation identity and version (C §3 #1) |
| Affected object | Identity of the object changed (bound target); for a creation, a description (the host assigns the identity, reported as a resulting object, §9) |
| Relied-on targets | The objects whose state the item relies on, with their subject content identities from the relied-on read (used by the per-item basis check, §5) |
| Attribute | What of the object changes (or *created* / *removed*) |
| Old value | Value as of the relied-on basis |
| New value | Proposed value |
| Item reason | Optional item-specific reason |
| Change-item content identity | §3.1; assigned by the host (§3.5 PM-6) |

### 3.5 Proposal identity and observation (interface meaning; PROPOSED; S1-B P 4)

This fixes meanings only. Representation, encoding, de-duplication
enforcement and recovery mechanics stay open (TBD-002; U-P1).

- **PM-1 Who mints the identity.** The proposal identity is minted once,
  before the first submission, by one party, and the record names which:
  - *proposer-minted* (the default): the drafter mints it at drafting — the
    agent through its host loop (LOOP-v0.7 §6.3 R-a) or through the App's
    Codex (ADAPTER-v0.6 §5.6 PI-1);
  - *host-minted*: where a host offers a step before submission that issues
    an identity (a draft or preview step), the proposer takes that identity
    and uses it for the submission and every retry.

  Either way exactly one proposal identity exists. A re-draft receives a new
  one (§5).
- **PM-2 Host handles.** A host may issue handles of its own for the
  proposal (a preview reference, a ticket, a receipt). Each is an
  **associated handle**: {kind, value, the scope within which it is valid},
  reported by the host beside the proposal identity. A handle never replaces
  the proposal identity in a record. An observation made by handle is
  recorded against the proposal identity the host associates with it.
  *SWBPIPE (SQ-08; data, not commitments):* DRAFT #885's caller-supplied
  `idempotency_key` is received as a proposer-minted identity; its
  `preview_ref` and `ticket` are handles valid within one controller session.
- **PM-3 Same identity, different content.** A submission that reuses a
  recorded proposal identity with different content is **refused — identity
  conflict** (§9): no effect, the recorded proposal's state unchanged, the
  recorded and submitted content identities both reported. It is not a
  retry, not a re-draft and not stale. The run record carries it as an
  entry with that outcome. SWBPIPE #885's `idempotency_conflict` is received
  as it (§9.1).
- **PM-4 Observation by identity.** A named read of the route, **observe
  proposal**, by proposal identity or by an associated handle. It returns
  either the **recorded state** — per-item states with their actors,
  refusals and applied associations; the associated handles; the
  de-duplication scope; the number of submissions the host recorded under
  this identity; the derived state (§4.6); the observation time; the current
  basis — or **not known to host**, with the de-duplication scope and, where
  the host can state it, the time from which its records cover. Observation
  is a read: it has no effect, is never refused stale and is never counted
  as a submission. *Not known to host* shows that a submission never arrived
  only where the host's stated scope covers the time it was sent; otherwise
  it shows nothing, and the outcome stays *unknown*.
- **PM-5 De-duplication scope.** The host states the scope within which it
  evidences de-duplication by identity: *durable*, *host session*, *time
  window* or *not stated*. Outside it, a resubmission may be treated as a
  first receipt; any second queued proposal or second effect is recorded as
  observed (§7), with the evidence limit "de-duplication scope exceeded"
  where the end of the scope was observed (for example a host restart).
  SWBPIPE #885: host session (SQ-08 (c)).
- **PM-6 Change-item content identity is host-assigned.** The host assigns
  each item's change-item content identity at first receipt and reports it
  in the recorded state; A5 and A10 bind to that value (§3.1 rule 2). A value
  computed on the proposer's side is not host evidence and is not what an act
  binds to.
- **PM-7 Application after acceptance is a host step.** After the person's
  A5, the host applies the accepted item through its route (A2), at
  acceptance or at a later host step, as the host practises (U-P7). No agent
  or App request triggers it. An agent call asking the host to apply an item
  is an ordinary change request with its own treatment. SWBPIPE: Apply
  accepts and applies in one step (SQ-01).

The sequence after *outcome unknown* is §4.7 SQ-P6. SH-1 exercises PM-2,
PM-3 and PM-4 (C-v0.8 §10.8). `proposal_state.schema.json` gives the
PROPOSED form of the recorded state, *not known to host* and the identity
conflict.

## 4. Lifecycle (REQ-004, REQ-005, REQ-011; SOW-171, SOW-172, SOW-178)

### 4.1 Proposal states (outside an effective direct treatment)

```text
drafted ─► validated ─► queued ─► accepted ─► applied (receipt)
   │           │           ├─► rejected   (A10, the person)
   │           │           ├─► withdrawn  (A11, the proposer)
   │           │           └─► refused — stale  (a relied-on target no longer holds)
   │           │  accepted ─► refused — stale (target fails before application; §4.2)
   │           │  accepted ─► application error (effect: none | partial | unknown)
   └─► refused — invalid / stale / not permitted  (before queueing; stays drafted)
overlay: any submitted step whose outcome cannot be observed ─► outcome unknown (observer-attributed)
later: applied ─► applied, then reversed by ⟨receipt⟩ (§4.5)
```

States and dispositions are **per change item** (SoW REQ-004 as revised
under SCA-V4-001); the proposal state is derived (§4.3).

| State / disposition | Meaning | Entered by (actor) | Evidence |
|---|---|---|---|
| drafted | Proposal composed with operation, arguments, targets, relied-on basis and targets, origin, any constraint, items | Proposer (A1) | Proposal content |
| validated | Host validation found it valid against the relied-on basis; treatment resolved | Host | Host validation outcome with treatment and settings reference |
| queued | Submitted and held by the host for the person's decision | Host (on proposer's submission) | Host queue acknowledgment |
| accepted | The person accepted the item ("accept", S-P9) | **The person (A5)**; host captures | Host-captured A5 bound to the change-item content identity |
| applied (receipt) | The host applied the accepted item through its one route | Host | Applied-outcome association (§9) incl. **receipt** reference and resulting objects |
| rejected | The person rejected the item. **Only A10** (SoW REQ-004); a person removing another's proposal is A10 (R-1) | **The person (A10)**; host captures | Host-captured A10 |
| withdrawn | The proposer withdrew its own proposal before application | **The proposer (A11)** | Host record |
| refused — stale / invalid / not permitted | Host refused on its route; not a person's act (SoW REQ-004: a host refusal is *refused*, not rejected) | Host | Refusal with reason, evaluated basis; for stale both bases and the failing targets; for not permitted the governing treatment |
| application error | A declared error raised during application | Host | Error identity (C §3 #7) and effect statement: *none*, *partial* (with receipt references), or *unknown* (→ overlay) |
| outcome unknown (overlay) | Result of a sent step cannot be observed | **The observer that lost observation** — loop, App adapter or host — attributed to it (R-7) | Absence of observation; last observed state |

Reporting rules:

1. A submitted proposal reports **queued** until the host records acceptance
   and application (S-P7). A successful *submit* is reported as queued, never
   as accepted or applied.
2. **Accepted alone is not applied.** *Applied* is reported only with a host
   receipt reference (REQ-011).
3. **Outcome unknown** is reported whenever the outcome cannot be observed,
   including when execution may have occurred; it is never inferred to be
   applied, failed, rejected or accepted. A later observation is reported
   separately with its own basis and does not back-fill the earlier report.
   Recovery mechanics are unselected (TBD-002).
4. Accepted, rejected and withdrawn are always relayed with their actor
   (A5/A10/A11) (R-7). A host refusal, or a host-review clear with no
   decision record, is never relayed as *rejected* or *withdrawn* (R8-5;
   §4.2).

### 4.2 Transitions beyond the drawn source lifecycle

| Case | Contract handling | Status |
|---|---|---|
| Validation fails before queueing | *refused — invalid* with the catalog error; stays *drafted*; no queue entry | PROPOSED; host confirmation U-P4 |
| Stale detected at validation | *refused — stale* (§5) | Follows HI §10 item 3 |
| A relied-on target no longer holds after *accepted*, before *applied* | *refused — stale* at application under the stale rule (§5), **not** model-row lapse (R-6). The recorded A5 stays bound to its unchanged item content and is **not lapsed**; the item is not applied; a re-draft is a new item content, so the A5 does not carry. **Display (R2-16):** "accepted by ‹person› — not applied: refused — stale (relied ‹B›, current ‹B′›)"; the item's derived state is never "accepted" alone, nor "applied". Checkpoint effect per §4.3 (fixture V-S1) | R-6, R2-16 (INTEGRATION); host behavior evidence DEP-001 (U-P3) |
| Withdrawal before queueing | Discarding a draft; no host record required | PROPOSED |
| Queue cleared by the person in host review, with no decision record (SWBPIPE DRAFT #885 `withdrawn` / `cleared_in_review`; SQ-05 (g), SQ-09) | **Item-left** event, cause "cleared by the person, no decision record" (§4.3). Never A10 (no rejection was recorded) and never A11 (the proposer did not withdraw) | The mapping is INTEGRATION (R8-5); "never read as A10 or A11" is SoW REQ-004 as revised under SCA-V4-001 |
| Engine refusal at the person's Apply (SWBPIPE DRAFT #885 `rejected: validation_rejected`; SQ-09 (e)) | *refused — invalid* at application, with the host's code; never A10 | INTEGRATION (R8-5) |
| Treatment narrowed while in flight | Already-queued proposal unaffected; a not-yet-applied operation is re-resolved at application (R-3 point 6) | INTEGRATION; host enforcement DEP-001 |
| Treatment widened while in flight | Never converts a queued proposal into direct application or an acceptance (R-3 point 7) | INTEGRATION |

**SWBPIPE (SQ-01, SQ-23; R8-5).** The host's A5 is Apply, which accepts and
applies in one step, per batch, with no A10 record. A stale Apply is refused
and records no acceptance, so *accepted — not applied: refused — stale* does
not arise on SWBPIPE. The App keeps that meaning (R2-16) and records that it
has no SWBPIPE counterpart; V-S1 (C §10.4), DEL-03-03 XF-30 and XT XC-08
remain App receiving cases.

### 4.3 Item-level acceptance, item-left events and derived state (V4-HI-41; V4-EXM-20; R2-18)

- Each change item carries its own disposition.
- The proposal's reported state is derived and never stronger than its
  items, e.g. "PR-2: item 1 accepted and applied (RC-1); item 2 rejected".
- Whether accepted items are applied separately or in one host application
  is a host input (U-P7). One-effect (§7) holds per item and per proposal.
- **Item-left events (R2-18).** When an item leaves the queue without a
  person's decision, this contract supplies an **item-left event**:
  {proposal identity, item identity, cause ∈ {refused — stale, refused —
  invalid, refused — not permitted (re-resolution at application), withdrawn
  (A11), cleared by the person with no decision record (R8-5)}, time,
  evaluated basis}. An item refused after an A5 (V-S1) is **not**
  an item-left case — it had a decision — but its per-item annotation shows
  "accepted — not applied: refused — stale".
  **The event is explicit in the schema (RP-2; R14-8 N-18; V18-4 m-7):**
  `proposal_state.schema.json` carries it on the item that left as
  `item_left` {cause, time, evaluated basis where the host evaluated one},
  required exactly when the item left (refused before any A5, withdrawn, or
  cleared with no decision record) and refused on any other item, with the
  cause matching the item's state; and as a document of its own,
  `item_left_event` {proposal identity, item identity, cause, time,
  evaluated basis}, for a consumer that receives the event rather than a
  recorded state. The five causes are the schema's `left_cause` values
  `refused_stale`, `refused_invalid`, `refused_not_permitted`, `withdrawn`,
  `cleared_by_person_no_decision_record`. A consumer no longer derives the
  event from the item's state.
- **All items decided** indication: true when every bound item has A5, A10 or
  an item-left event (`derived_state.all_items_decided`; DS-4).
- For a checkpoint requiring A5 on a proposal, the mapping of these data to
  checkpoint dispositions (in Phase 1, labels on the record, EXEC PH-6) is
  **WD §4.3.7**, confirmed by DEL-02-03 (R4-7;
  R5-9). "Partial" is a per-item annotation, never a seventh disposition; a
  *performed* over a reduced subject is never presented as "all items
  accepted" (R2-18). Confirmed by DEL-02-03 (R4-7), with WD §4.3.7 MX-3 (a
  lost decision observation → *unknown*), MX-6 (every item left → the arrival
  is closed "replaced" by the next arrival) and MX-8 (application error or
  *outcome unknown* after A5 → disposition unchanged, annotated). A performed
  A5 checkpoint stays performed when an accepted item is later refused stale;
  the declared output is then not produced, with an annotation (R3-3). A5
  never re-holds after resume (R4-3); re-hold is governance phase in any
  case (R8-11 item 1).
- **SWBPIPE (SQ-01, SQ-09 (b), (f); R8-5).** Apply applies a batch
  atomically, and Clear discards queued batches without a record. Per-item
  A5/A10 decisions (C T11), mixed-item dispositions (R2-18, WD §4.3.7) and
  A10 records have no SWBPIPE counterpart. The App keeps these meanings and
  records the missing counterparts; it never synthesizes a per-item decision
  from a batch Apply beyond what the host's receipt names.

### 4.4 Direct-autonomy branch (V4-HI-22; S-P3)

Entry condition (R-8; R2-6): the host resolves, at validation, that the
DEL-04-02 display state for the operation class and scope is **effective
(person-set) with grant value direct**, or **effective (policy default)
whose policy-record default is direct** — no such default exists in the
first increment — and (governance phase) that **no host-held governing
checkpoint constraint** applies. SWBPIPE has no direct branch: it has no
grants, and every change waits for the person's Apply (SQ-05, SQ-06). Every other state (requested by agent; set by person, not yet
confirmed; unconfirmed; not set; refused; class *no policy basis*) leaves the
direct branch closed, and a direct request is *not permitted* (§2). A
person-set grant requires A12 act evidence (D2).

```text
drafted ─► validated (treatment: direct) ─► applied (receipt, origin mark, undo route, later-check route)
                ├─► refused — invalid | stale | not permitted
                └─► application error (effect statement)
overlay: unobservable ─► outcome unknown (observer-attributed)
```

- No *queued* or *accepted* state exists and **no acceptance is recorded or
  implied**. Reports never say "accepted" for a direct application.
- The application carries origin (§3.3) including both settings references
  (at route decision; at application, host-reported or *unconfirmed*),
  relied-on basis, receipt, resulting objects, origin mark, undo route and
  later-check route (access for later examination or checking; implies no
  act, R-4). These are abstract host contributions, host-owned.
- The basis check applies exactly as for proposals.
- **Acceptance checkpoint constraint (R-5; R2-12, DERIVED from D2b and
  from the hold that V4-HI-42 and V4-WF-05, as amended, phase to the
  governance layer) — governance phase (retained; R8-1).** *Phase 1
  (R8-11 item 2 and R8-12 item 2, as restated by R9-2; EXEC CH-27):* WD
  I-7 is plan guidance, and V4-HI-42's request clause and record clause
  are in force: the checkpoint's A5 is requested, and it is recorded as
  done only when the person performs it. The agent proposes the operation
  as the plan expects; a direct request, if made, meets the host's own
  treatment, and nothing is reported *not permitted* on the checkpoint's
  account. When the active grant lets the host apply directly, no proposal
  arises and the host may apply. An A5 checkpoint whose reached-when is
  *proposal queued* is then **not reached**: nothing is requested by reason
  of an arrival that did not occur, no A5 is forced, and none is recorded;
  the record shows the direct application under the person's grant (R9-2
  as corrected by R10-1). V4-HI-42's request clause applies to a checkpoint
  the run reaches: where a checkpoint of any kind is reached while a grant
  permits direct application, its act is requested and its disposition is
  *waiting* ("reached; act not yet recorded") until the person performs it. *Governance phase:* when a governed checkpoint's
  constraint applies with **host-held**
  carriage (R5-2; model-supplied or absent carriage is not relied on) — the
  host route resolves *propose* for that operation in that run. A request to
  **apply directly** is **not permitted**, naming the constraint as the
  governing treatment; it is **never converted** into a proposal (R-3.3). The
  proposer may then submit a proposal separately; that proposal's queued
  items become the checkpoint's subject (reached-when kind (c) *proposal
  queued*, R2-17). A checkpoint requiring A4 on applied rows does not force
  proposal; in the governance phase the run holds after application for the
  A4 **where hold support allows**. Until host evidence of host-held
  evaluation exists on the acting surface, the governance-phase fixtures
  exercising this (V-CP1; LOOP FX-C9; PANEL PC-24; WD VC-11) are AWAITING
  INPUT (U-P10) — SQ-02 answered 2026-09-28: route (iv), no receipt and no
  host copy (not offered); SQ-20: no host loop; a SWBPIPE owner decision
  (ANS §2); host joins deferred (DECISION-3).
- **Other checkpoints.** *Phase 1 (R8-1; R9-1; EXEC PH-2):* no checkpoint
  holds the run. The required act is requested — in the current phase by
  the agent carrying out the workflow (R9-1; SETTLED by DECISION-K1 K1-1) — and is recorded as done
  only when the person performs it; the arrival and the person's act are
  recorded as observation.
  *Governance phase (retained):* any other governed checkpoint holds the run
  for the person's act (S-P13) **where hold support allows**. Hold support
  takes one of four values per checkpoint and surface (R5-1; DEL-02-03 EXEC
  §3.6): *enforced by the host loop*; *enforced on the host route*
  (host-held constraint, evidenced via SQ-02); *not established*; *not
  enforceable* — assigned by what the checkpoint must hold, not by how it
  arrives (R6-1). Against SWBPIPE, a checkpoint holding only host operations
  on X is *not enforceable* (HS-3 (c); SQ-02 answered with route (iv)), and
  one holding any App-side action is *not enforceable* (HS-5). App-run holds
  (D6) are closed for Phase 1 and re-open only when the governance phase is
  taken up (R8-2; EXEC U-E1); nothing is ever claimed as held that is not
  enforced.

### 4.5 Undo (R2-15)

- An undo is a **change through the one route** (§2) via the catalog's undo
  operation (C-v0.8 OP-C10): its own origin, its own relied-on basis and
  basis check, its own treatment — governed by the policy record of the
  operation whose receipt it reverses (R3-4, INTEGRATION) — its own outcome and its own receipt.
- Its applied outcome carries the relation **reverses ⟨receipt⟩**, naming the
  reversed change's receipt; the run record additionally links the reversed
  entry. It may equally be *refused*, meet an *application error* or be
  *outcome unknown*.
- **Acts and undo.** An undo erases no act record. An A5/A10 on the reversed
  change item keeps its binding and is **not lapsed** by the undo, because its
  item content is unchanged. Acts bound to subject content that the undo
  changes (e.g. an A4 on the applied row) **lapse under the ordinary rule**
  (V4-HI-32; DEL-04-03 L-6) — fixture T16a/T17.
- The reversed item's standing shows "applied, then reversed by ⟨receipt⟩".
  Undo route availability, scope and mechanism are host-owned (U-P8).
- **SWBPIPE session undo (SQ-10; R8-5).** SWBPIPE's undo is a session stack
  of whole-model snapshots. It is not an operation through the route, writes
  no receipt, does not reference the reversed change and is not governed by
  operation policy. R2-15 and R3-4 stand as App meaning. For SWBPIPE,
  "reverses ⟨receipt⟩" is *not supplied*, and a lapse an undo causes is
  shown from the identity change (R8-4; C §5.3).
- **Undo and holds (R5-5) — governance phase for re-hold (R8-11 item 1).**
  *Phase 1:* a lapse caused by an undo, including the person's own undo, is
  recorded like any other lapse (V4-REC-05; EXEC PH-8), and nothing
  re-holds. *Governance phase:* such a lapse re-holds a governed checkpoint
  like any other lapse (DEL-02-03 RH-8). In both phases the person's undo is
  never recorded as "action during hold" or "continued past ‹checkpoint›",
  and an undo never re-holds an A5 arrival (A5 binds to the unchanged item
  content).

### 4.6 Per-item transitions and the derived proposal state (PROPOSED; S1-B P 5; R12-1)

States and dispositions are per item (§4.1). One row per transition; "item
left" marks the §4.3 item-left event, which the recorded state carries on
the item as `item_left` (RP-2). `prototype/proposal_states.py` beside
this file holds the same table as executable rules.

| Id | From | Event | Actor | To | Record |
|---|---|---|---|---|---|
| PT-1 | — | Drafting | Proposer (A1) | drafted | Proposal content |
| PT-2 | drafted | Validation passes, treatment *direct* | Host | validated | Validation outcome with treatment and settings reference |
| PT-3 | drafted or validated | Validation passes, treatment *propose*; the host acknowledges queueing | Host | queued | Queue acknowledgment |
| PT-4 | drafted | Validation fails with a catalog error | Host | refused — invalid | Refusal with error identity; item left |
| PT-5 | drafted | A relied-on target no longer holds at first receipt | Host | refused — stale | Both bases; failing targets or the host's scope; item left |
| PT-6 | drafted | Treatment forbids the requested mode | Host | refused — not permitted | Governing treatment; item left |
| PT-7 | validated | Direct application | Host | applied | Applied association, branch *direct under grant* |
| PT-8 | validated | A declared error during direct application | Host | application error | Error identity; effect *none*, *partial* (with receipts) or *unknown* |
| PT-9 | queued | A5 | The person | accepted | Host-captured act |
| PT-10 | queued | A10 | The person | rejected | Host-captured act |
| PT-11 | queued | A11 | The proposer | withdrawn | Host record; item left |
| PT-12 | queued | A relied-on target no longer holds (a host re-check, or its whole-model scope) | Host | refused — stale | As PT-5; item left |
| PT-13 | queued | The person clears the queue with no decision record | Host | left the queue | Cause "cleared by the person, no decision record"; item left (R8-5) |
| PT-14 | accepted | Application (§3.5 PM-7) | Host | applied | Applied association, branch *after acceptance*; A5 kept |
| PT-15 | accepted | A relied-on target no longer holds before application | Host | refused — stale | "accepted — not applied: refused — stale"; A5 kept and not lapsed; not an item-left case (§4.2; R2-16) |
| PT-16 | accepted | A declared error during application | Host | application error | As PT-8; A5 kept |
| PT-17 | applied | The receipt is reversed by an undo (§4.5) | Host | applied, then reversed | Both receipts |
| PT-18 | any state after sending | The result of a sent step is not observed | The observer | outcome unknown (overlay; the recorded state does not change) | Observer; last observed state |
| PT-19 | outcome unknown | A later observation (§3.5 PM-4) | The observer | the observed state, reported separately | Does not back-fill |

Every other transition is refused. In particular a queued item is never
applied without A5; a direct application is never *accepted*; and rejected,
withdrawn, left, refused and application-error items are final (a re-draft
is a new proposal, §5). *Applied* is final except for PT-17.

**Derived proposal state.**

- **DS-1** The proposal's state is the list of its items' states. A one-word
  summary is given only when every item is in the same state; otherwise the
  summary is *mixed* and the report lists the items ("PR-2: item 1 applied
  (RC-1); item 2 rejected").
- **DS-2** The count of items per state goes with the summary.
- **DS-3** The proposal is *open* while any item is drafted, validated,
  queued or accepted.
- **DS-4** *All items decided* holds when every item has an A5 or an A10 or
  carries an item-left event (§4.3).
- **DS-5** No report names a state for the whole proposal that some item
  does not have: never "accepted" or "applied" while any item is otherwise.

**Validation of some items only.**

- **VP-1** A host that validates per item may queue some items of one
  proposal and refuse others at the same submission. Each item takes its own
  transition (PT-3 to PT-6); the refused ones leave.
- **VP-2** A host that validates a proposal as a whole refuses every item
  with the same reason and names the failing items where it knows them.
  SWBPIPE's batches are atomic (SQ-09 (b)).
- **VP-3** The App relays either. It never infers partial queueing, and it
  never regroups items.

### 4.7 Operating sequences with failure behaviour (PROPOSED; S1-B P 5; R12-1)

The main flow is §11 (T3–T13). These are the sequences that had none. Each
step names what can fail, who reports it, the record left and what happens
next.

**SQ-P1 Withdrawal (A11).**

| Step | What can fail | Reporter | Record left | Next |
|---|---|---|---|---|
| 1 The proposer asks the host to withdraw its queued proposal | The items are no longer queued (decided, left or applied) | Host | The host's refusal | Nothing changes |
| 2 The host records A11 per item (PT-11) | The result is not observed | The observer | *outcome unknown* (PT-18) | Observe by identity (PM-4) |
| 3 Item-left events, cause *withdrawn* | — | Host | §4.3 item-left events | A checkpoint maps them per WD §4.3.7 |

Before queueing, withdrawal is discarding a draft, with no host record (§4.2).

**SQ-P2 Application after acceptance.**

| Step | What can fail | Reporter | Record left | Next |
|---|---|---|---|---|
| 1 The person performs A5 on an item; the host captures it (PT-9) | The host exposes no capture-evidence reference | Host | The act, as a record shape only (§10; R2-20) | — |
| 2 The host applies it (PM-7; PT-14) | A relied-on target changed (PT-15) | Host | "accepted — not applied: refused — stale"; A5 kept | A re-draft; the A5 does not carry to new item content |
| 3 | A declared error (PT-16) | Host | Error identity and effect | SQ-P4 when the effect is *partial* |
| 4 The agent learns the result by observation (PM-4) | The observation is lost | The observer | *outcome unknown* | Observe again |

**SQ-P3 Failure on the direct branch.**

| Step | What can fail | Reporter | Record left | Next |
|---|---|---|---|---|
| 1 A direct request under an effective direct grant | The treatment is no longer direct (narrowed in flight, R-3 point 6) | Host | *refused — not permitted* (PT-6), naming the treatment; never converted into a proposal | The proposer may submit a proposal separately |
| 2 Validation | Stale or invalid (PT-5, PT-4) | Host | The refusal | Re-draft |
| 3 Application | A declared error (PT-8) | Host | Error identity and effect; for *partial*, the receipts of what was applied | SQ-P4 |
| 4 The result reaches the proposer | Lost | The observer | *outcome unknown* | SQ-P6 |

**SQ-P4 After an application error with partial effect.**

- The item stays *application error*, effect *partial*, with the receipts of
  what was applied. That is final: it never becomes *applied* and never
  returns to *queued*.
- What was applied is a real change. Acts bound to content it changed lapse
  in the ordinary way (§4.5). Its receipts are reversed only by an undo
  through the route (OP-C10; §4.5), a separate change with its own treatment.
- Completing the intended change is a re-draft from a new read (§5); no
  acceptance carries over.
- A checkpoint's disposition stays as it was, annotated (WD §4.3.7 MX-8).
- SWBPIPE has no partial application; its batches are atomic (SQ-09 (b)).

**SQ-P5 Two queued proposals that share a target.**

- Where the host supplies subject identities, applying an item of one
  proposal changes the shared target's identity, so the other proposal's
  items that rely on it become stale (PT-12, or PT-15 if already accepted).
  Its items that do not rely on it are unaffected.
- Under a whole-model staleness scope, any application stales every other
  queued proposal (SWBPIPE, SQ-07 (d)).
- Nothing is merged, reordered or retargeted (§6). The order of application
  is the host's.

**SQ-P6 After outcome unknown.**

| Step | What can fail | Reporter | Record left | Next |
|---|---|---|---|---|
| 1 A submission's result is not observed (PT-18) | — | The observer (loop or App) | *outcome unknown*, with the last observed state | Step 2; never a blind retry (LOOP R-d; ADAPTER PI-2) |
| 2 Observe by identity (PM-4) | The observation is lost too | The observer | Still *unknown* | Repeat later |
| 3a The recorded state is returned | — | Host | Reported separately (PT-19) | No resubmission is needed |
| 3b *Not known to host*, and the host's scope covers the time of sending | — | Host | The observation | Retry with the same identity and content: a first receipt, checked like one |
| 3c *Not known to host* outside the scope, or the scope not stated | — | Host | The observation; one effect unevidenced | Under *propose*, retry with the same identity. Under *apply directly*, no retry unless the identity is held durably by the host (ADAPTER PI-4) |
| 4 The retry is answered | Answered from recorded state (de-duplication first, §5), or *identity conflict* (PM-3) if the content differs | Host | Each submission recorded separately (§7) | — |

SH-1 ran SQ-P6 once (T13 with the response dropped, then observation, then
a retry; C-v0.8 §10.8).

## 5. Stale refusal, re-draft and retry (REQ-006; SOW-173; R2-13)

- **Precedence (R2-13, INTEGRATION; unchanged by R8-3).** On any submission
  the host first **de-duplicates by proposal identity**. If the host already holds the
  identity (queued, decided, applied or refused), it returns that proposal's
  recorded per-item state or outcome; it does not re-validate, and a
  resubmission is **never refused as stale because of its own effects**. Only
  a first receipt, and application of a not-yet-applied item, undergo the
  basis check. SWBPIPE DRAFT #885 runs its key lookup before the basis
  check, so a retry recovers its ticket even after its own commit; the same
  key with different content returns `idempotency_conflict` (SQ-08 (b)),
  received as *refused — identity conflict* (§3.5 PM-3).
- **Trigger (R2-13 as amended by R8-3; INTEGRATION).**
  - *Per item, where the host supplies subject identities.* A change item is
    stale when a **subject content identity of one of its relied-on
    targets** differs from the current one at the check (validation, queue,
    or application). A global revision advance alone does not stale an
    item; applying sibling items of the same proposal does not stale
    remaining items unless they share targets.
  - *Otherwise, the host's stated scope.* The App receives and shows the
    host's stated staleness scope and never narrows it or re-evaluates it
    per item. SWBPIPE's trigger is any model revision change: any commit
    (edit, apply, undo, redo, project open or create) stales every queued
    proposal, so one application makes every other queued item leave
    (SQ-07 (d), (f)). The engine additionally checks per-field
    before-values.
  - A generation change makes revision comparison impossible and is handled
    under U-C2. Host confirmation of the per-item rule and of
    subject-identity scope: U-C3.
- **Refusal content.** *refused — stale*; reason (what changed, where known);
  failing targets, or, on a host with a stated scope, that scope with
  "failing targets not supplied" (R8-3); **relied-on basis** (unchanged);
  **current basis** (evaluated basis); affected items. SWBPIPE's stale
  refusals are `OP-STALE-BEFORE-VALUE` and `OP-CLAIMED-MODEL-HASH-MISMATCH` on
  main, and `stale_basis` or `expired` in DRAFT #885 (SQ-09 (a)).
- **No silent refresh.** No host or consumer rewrites the relied-on basis and
  proceeds.
- **Re-draft.** Only as a **separately identified** proposal: new proposal
  identity, lineage to the stale one, a new relied-on basis and target
  identities from a new read, re-derived old values, new change-item content
  identities, fresh validation. No acceptance carries over.
- **Retry is not re-draft.** A retry resubmits the same proposal identity and
  content without a new read. If the host holds the identity, the recorded
  state is returned (precedence above). If the host never received the first
  submission, the retry is a first receipt and is checked like one.

## 6. No retargeting (REQ-007; SOW-174)

- Bound targets and affected objects are fixed at drafting from explicit
  target identification (C §4.3), including a person's selection resolved at
  drafting.
- A later selection change in any surface never changes a proposal's bound
  targets, items or reported affected objects. A change of intended target is
  a new proposal.

## 7. Repeated submission → one effect (REQ-008; SOW-175)

- **Obligation.** Submitting the same proposal identity more than once,
  including a retry after a lost acknowledgment, produces at most one
  application effect per item. This is a **host obligation to be evidenced**
  (DEP-001), not a recorded fact (SoW REQ-008 as revised under SCA-V4-001;
  R-7).
- **Precedence.** Identity-based de-duplication precedes the basis check
  (§5; R2-13).
- **Recording.** Each submission is recorded separately, referencing the same
  proposal identity, with only the effects actually observed (the same
  receipt, two receipts, or unknown) (R-7).
- **Testable form.** Effect count observed in the host model/receipts for the
  proposal identity equals 0 or 1 per item; a repeat reports the existing
  state (queued, applied with the *same* receipt, etc.).
- **Mechanism unselected** (TBD-002). Shared validation or transport
  deduplication is not evidence of a one-domain-effect outcome (V4-EXM-25).
- **Scope (§3.5 PM-5).** One effect is evidenced only within the host's
  stated de-duplication scope. A resubmission outside it is recorded with
  what was observed, and the obligation is recorded as unevidenced for it.
- **Unobservable repeat.** Report *outcome unknown* (observer-attributed); do
  not infer one effect or zero.
- A re-draft is a different proposal and not a repeat.

## 8. Host proposal-view information (REQ-009; SOW-176)

The host shows, in its own tables/views (V4-HI-24; V4-HOST-04: no
agent-private surface), for each proposal and item:

| Information | Supplied by this contract | Presented by |
|---|---|---|
| Old value (as of relied-on basis) | §3.4 | Host |
| New value | §3.4 | Host |
| Affected objects; which items a view row presents | §3.4; §3.1 rule 4 | Host |
| Why (reason) | §3.3 / §3.4 | Host |
| Origin (author, seat role, conversation, workflow identity and run) | §3.3 | Host |
| Current disposition per item, with actor for A5/A10/A11, and per-item annotations (e.g. accepted — not applied: refused — stale) | §4 | Host |
| Stale indication with current value where it differs; failing targets | §5 | Host |
| Lineage for a re-draft | §3.1 | Host |
| Item-left events | §4.3 | Host |

Presentation, receipts and the acceptance control are host-owned
(DEP-03-02-024). The control says "accept", never "approve" (S-P9). A live UI
witness is host-owned evidence.

## 9. Canonical outcome taxonomy (R-7; REQ-005, REQ-010, REQ-011; SOW-172, SOW-177, SOW-178)

Every non-success outcome carries the **evaluated basis** where the host
evaluated one. Outcomes apply per change item where items exist. Reporter
rules for non-success results follow C-v0.8 §4.1.

| Outcome | Meaning | Carries | Establishes | Does **not** establish |
|---|---|---|---|---|
| unavailable | Catalog precondition failed (C §4.1, §4.4) | Reason, failed precondition, evaluated basis | Nothing executed | — |
| not permitted | Treatment forbids the requested mode (R-3; R2-12) | Governing treatment (policy record or checkpoint constraint), evaluated basis; A8 request *offered* for reserved acts | Nothing executed | — |
| channel not enabled | External access off (V4-HI-52); A13 not performed | Channel state | Nothing evaluated | — |
| not exposed on this surface | Host-reported: entry not exposed on the acting surface (C §3 #9); relayed by loop/adapter | Entry, surface | Nothing evaluated | — |
| refused — invalid | Host validation refused with a catalog error | Error identity, evaluated basis | Nothing applied | — |
| refused — stale | A relied-on target no longer holds | Reason, failing targets, relied-on basis, current (evaluated) basis | Nothing applied | — |
| queued | Host holds the item for the person's decision | Host acknowledgment | Submission received | Acceptance, application |
| accepted | Host captured the person's A5 on the item | Actor, act reference, item content identity; capture time as the host records it, else *not supplied by host* (RP-2; `act_ref.captured_at`) | That act by that person on that item content | Application, checking, approval, reliance |
| rejected | Host captured the person's A10 | Actor, act reference; capture time as for *accepted* | That rejection | — |
| withdrawn | Proposer withdrew (A11) | Actor | That withdrawal | — |
| applied (receipt) | Host applied the item. **Applied-outcome association**: proposal/item identity, relied-on basis, receipt reference, resulting revision, **resulting objects** (created and changed object identities with their post-application subject content identities and method designation, or "not supplied" as an evidence limit, R2-14; SWBPIPE supplies `target_ref`, per-field diffs and the new whole-model hash, with created objects only as the target ids of `create_*` operations and no post-application per-object identity, SQ-03 (d), R8-4); a resulting object without its subject content identity or method has them *not supplied* (the consumer records that and computes none, R14-8 N-21); branch *after acceptance* or *direct under grant* (with settings references); relation *reverses ⟨receipt⟩* for an undo | Association | Execution, resulting revision and the reported resulting objects | Acceptance (direct branch), checking, approval, reliance |
| applied, then reversed by ⟨receipt⟩ | Standing of an applied item whose change was later reversed (§4.5) | Both receipts | Both executions | That any act on it lapsed or survived — evaluated per act (§4.5) |
| application error | Declared error during application | Error identity; effect *none* / *partial* (receipt references) / *unknown* | What the effect statement states | Any unstated effect |
| outcome unknown | Result unobservable | Observer, last observed state | Only the last observed state | Applied, failed, accepted or rejected |
| refused — identity conflict (PROPOSED, v0.8) | A submission reused a recorded proposal identity with different content (§3.5 PM-3) | Proposal identity; recorded and submitted content identities | That the submission had no effect and changed nothing recorded | A retry, a re-draft, staleness, or anything about the recorded proposal's items |
| not known to host (PROPOSED, v0.8; observation result) | An observation by identity found no record (§3.5 PM-4) | Proposal identity; the host's de-duplication scope and, where stated, since when its records cover | That the host holds no record within its stated scope | That the submission never arrived, unless the scope covers the time it was sent |
| error (read/examination/host check) | Declared error in a non-mutating operation (C §4.1) | Error identity, evaluated basis | — | — |
| success (operation) | The operation ran (S-P7) | Result | Execution | Any human act |

**Network destinations of a host's agent (v0.8, node B5; PROPOSED).** The
two results *destination not allowed* and "destination not allowed by the person"
are C-v0.8 §4.1 rows, reported by the host's native layer or
control, not proposal outcomes; the one account of that flow is
DEL-05-01/LOOP-v0.8 §5.3. For a proposal submission whose entry carries an
external-contact declaration (C §3.4): the declared destination is checked
at V-D before the submission is dispatched, so a submission that is refused
there is never queued and has no proposal state; a contact the host makes
only at application passes the native layer then, and a refusal at that
point is an **application error** with its effect statement (LOOP §5.3
DF-4 (c)). The waiting of a destination request's carried call is not a
proposal state and changes no item disposition.

Item-left events (§4.3) accompany the refusal/withdrawal outcomes of items
that leave without an A5; the schema carries them explicitly (§4.3).

**Tokens (RP-2; R14-6; V18-2 M-2).** In the schemas the per-item outcomes
of this table are the `item_state` values of `proposal_state.schema.json`,
and consumers use them unchanged: queued `queued`; accepted `accepted`;
applied (receipt) **`applied`**; applied, then reversed
`applied_then_reversed`; rejected `rejected`; withdrawn `withdrawn`;
refused — stale `refused_stale`; refused — invalid `refused_invalid`;
not permitted (a proposal item) `refused_not_permitted`; application error
`application_error`; outcome unknown `outcome_unknown`; the queue cleared
with no decision record `left_queue` (§9.1); and before submission
`drafted`, `validated`. *Refused — identity conflict* and *not known to
host* are document kinds (`identity_conflict`, `not_known_to_host`), not
item states. No other token (for example `applied_receipt`) is P's. Whether the host receipt *itself* carries the relied-on basis or the
resulting objects is a host observation recorded at comparison (C-v0.8
VC-C-04), not assumed.

### 9.1 Received host vocabulary: SWBPIPE (R8-5; evidence only)

SWBPIPE's terms are received as follows. The first rows are **INTEGRATION
(R8-5)**. The rest are SWBPIPE's own mapping (SQ-09 (a)), received as the
host states it. Main terms are FACT; #885 terms are DRAFT #885 (unmerged,
deferred). Nothing here is a SWBPIPE commitment (DECISION-3).

| SWBPIPE term | App term | Condition |
|---|---|---|
| `unsupported_method` / `unsupported_change` | host-reported **not exposed on this surface** | Never *not permitted*. R2-4 (a named rule) is recorded as not met by this host (R8-5) |
| #885 `withdrawn` / `cleared_in_review` (the person cleared the queue) | **item left**, "cleared by the person, no decision record" (§4.2, §4.3) | Never A10, never A11 (R8-5) |
| #885 `rejected: validation_rejected` at Apply | **refused — invalid** at application | Never A10 (R8-5) |
| Apply (the person's review-and-apply) | **accepted** and **applied (receipt)** in one step, per batch | No separate *accepted* state and no A10 record; the missing counterparts are recorded (R8-5) |
| Session undo | — | Writes no receipt; "reverses ⟨receipt⟩" is *not supplied* (R8-5; §4.5) |
| `controller_unavailable`, or an attachment failure | *endpoint unavailable* (DEL-03-03), channel *disabled* | Never host-reported *channel not enabled*; SWBPIPE has no such code (R8-6) |
| main `blocked`; #885 `invalid_request` | *refused — invalid* | Before queueing, nothing is queued (SQ-09 (d)) |
| main `OP-STALE-BEFORE-VALUE`, `OP-CLAIMED-MODEL-HASH-MISMATCH`; #885 `stale_basis`, `expired` | *refused — stale* | Host scope: whole model (§5; R8-3) |
| #885 `queued` | *queued* | Only after the controller observes publication |
| main `applied_to_session_model`; #885 `committed` | *applied (receipt)* | Main's receipt is session-only; #885's is readable by `status` within one controller session (SQ-01, SQ-08 (c)) |
| #885 `outcome_unknown` | *outcome unknown* | Reporter host; a later `status` read is reported separately |
| #885 `idempotency_conflict` | *refused — identity conflict* (§3.5 PM-3) | PROPOSED at v0.8; the key is received as a proposer-minted identity (PM-2) |
| #885 `status` by `ticket` | **observe proposal** by an associated handle (§3.5 PM-4) | Within one controller session (SQ-08 (d)); outside it, the result shows nothing about arrival (PM-4, PM-5) |
| #885 `busy`, `capacity`, `not_ready`, `unauthorized`, `wrong_app`, `wrong_workspace`, `internal_error`, others | as the host states each (*unavailable*, *not permitted* or *error*) | `retryable` and `next_action` are recorded, never acted on as a treatment |

## 10. Execution versus human acts (REQ-010, REQ-012; SOW-177; #d3)

Canonical act names (R-1; DEL-04-01 §2.1).

| Subject | Actor | Evidence required | Never inferred from |
|---|---|---|---|
| A1 propose (draft/submit) | Agent or person | Proposal content; host queue acknowledgment | — |
| A2 apply (validation/application) | Host route on the actor's request | Validation outcome; receipt | — |
| Direct application under grant | Agent within an effective direct treatment and no governing constraint | Receipt, origin mark, settings references | — and it implies no A5 |
| A3 examine | Agent | Findings by reference | — and it is never A4 or a host check |
| A4 mark checked (reserved) | The person | Host-captured act bound to subject content identity | Findings, success, acceptance |
| A5 accept (reserved where a proposal is required) | The person | Host-captured act bound to change-item content identity | Success, submit, queue, application, agent report |
| A10 reject (reserved wherever A5 is) | The person | Host-captured act | Absence of acceptance; host refusal |
| A11 withdraw | The proposer | Host record | — |
| A6 approve (reserved) | The person/accountable professional | Its own record | A5 (S-P9) |
| A7 rely (reserved) | Accountable professional | Its own record | Any of the above |
| A8 request | Agent | Request record, only when actually issued | — it establishes nothing; a failed call is not an A8 |
| A9 record (faithful recording) | Recorder ≠ decision actor | Reference to the capturing surface's evidence of the act | — it never satisfies a checkpoint by itself (R-5); never made through a reserved act-performing operation (R2-2) |
| A12 set grant (reserved) | The person | Control act evidence, bound to the setting content (classes, grant values, scope); a later **established** A12 **supersedes** an earlier one (R2-7, PROPOSED) | Agent request (A8) |
| A13 enable / disable external access (reserved; disable INTEGRATION) | The person | Control act evidence. SWBPIPE has no enablement facility (SQ-28), and its launch environment variable is not a captured act (SQ-13), so no A13 is evidenced there, and a host answer in that state is recorded with the evidence limit "host reachable without evidenced A13" (C §4.1; adopted in RS R11 by R8-12 item 5; R9-8); whether a person-set variable could count is deferred to the owner (R8-6) | Agent request (A8) |
| Act-declined event (A4, A6, A7, A12) | The person | Capture evidence of the decision not to act | — it is not the act and not A10 (R2-5) |
| Run-ended event | The person stopping the run, or an observed end; **reporter**: the loop (V2 m-11) | Run record | — the checkpoint stays *waiting* (R2-5). An ended run is never resumed; acts after the end are shown "after run end" and change nothing; continuation is a new run with **continues ⟨run⟩**, inheriting nothing (R4-4, PROPOSED). An interruption is not a run end |
| A14 answer tool permission | Person or the user's own Codex mode | App-side R13 record only (R2-8) | — never a professional act, A5 or a grant |
| A15 register workflow revision (R12-5) | The person | Its own human-act record (ACT-POLICY-v0.8 §2.1; RS) | — not a change through this route and never required by a checkpoint in this increment |

Rules: one act never establishes another; no synthetic prerequisite between
acts is introduced; checkpoint satisfaction requires attributable evidence
from the capturing surface — the host's act facility for acts on host content
(R-5). Whether a particular host exposes a capture-evidence reference is a
DEP-001 relay question (R2-20); SWBPIPE exposes none (SQ-01), and its
acceptance-record storage is SWBPIPE owner decision PB-TBD-002. Answers to Codex user-input or MCP
elicitation requests are **not act evidence** and never host act capture
(R4-12). In the current phase an act captured before a checkpoint's arrival
counts toward it when it is of the required kind and the content it was made
on is still current, and is cited with its time (EXEC SP-6; DECISION-K1
K1-2); an earlier act on content no longer current, or of another kind, is
shown "prior act not counted". Counting only acts captured at or after the
arrival is kept as a governance-phase option (EXEC SP-6F; R4-5, PROPOSED). A refused or pending A12 supersedes nothing and does not count
(R4-6). A person's own A1/A2 are run-record (R7) operations, not human-act
records; an operation that performs a reserved act (OP-C6/C7/C8, the A12/A13
controls) produces the human-act record, and its R7 entry references it
(R5-6). Operation-specific reserved additions await `UNRESOLVED{OI-021}`.

## 11. M3-CP read-then-action comparison design (return to DEL-03-01)

This is the distinct return retained from SCC-CASE-004 (CASE-002 M3-CP;
DEP-03-01-026). It supplies DEL-03-01 with designed refusal/application
behavior and a comparison plan; DEL-03-01 compares basis elements only.
Steps are the FX-PIPE-01 timeline (C-v0.8 §10.3).

| Step | Action | Basis observed | Proposal reference | Expected P behavior |
|---|---|---|---|---|
| T3 | Agent reads supports table (OP-C1) | B1 = FX-W1/g1/r12/⟨v12⟩/⟨m-fx⟩ with ⟨S-1…S-4@r12⟩ | — | — |
| T5 | Agent drafts PR-1: item 1 add support (OP-C4; targets R-100, S-2, S-3); item 2 S-3 stiffness (OP-C5; target S-3) | — | PR-1 relies on B1 and target identities | drafted; items bound; change-item content identities include B1 |
| T6 | Engineer A edits S-3 (intervening edit) | r13 (same generation g1) | PR-1 still relies on B1 | — |
| T7 | Agent submits PR-1 | host evaluates B2 = …/g1/r13/⟨v13⟩ | B1 | first receipt → per-item check: both items **refused — stale** (⟨S-3⟩ changed): reason, failing target S-3, relied B1, current B2; item-left events for both |
| T9 | Agent re-reads; drafts PR-2 (lineage PR-1, stale) | B2 | PR-2 relies on B2 | new proposal identity; old values and target identities at r13; new item content identities |
| T10 | Submit PR-2 | B2 | B2 | validated → **queued** (not applied) |
| T11 | Engineer A accepts item 1 (A5), rejects item 2 (A10) | — | B2 | item 1 accepted (bound to its item content identity); item 2 rejected |
| T12 | Host applies item 1 | resulting r14 | B2 | **applied**: association PR-2 / item 1 / B2 / RC-1 / r14 / resulting objects S-5 created, R-100 changed; A5 not lapsed |
| T13 | Acknowledgment lost; agent retries PR-2 (same identity) | — | B2 | host de-duplicates **before** any basis check: returns recorded state (item 1 applied RC-1; item 2 rejected); second submission recorded separately; no stale refusal from its own effect. If unobservable: **outcome unknown** (observer: loop), last observed *accepted* |

**Comparison DEL-03-01 performs (C VC-C-04):** for each basis element and the
method designation, compare the value at read (T3, T9), in the proposal
reference (T5, T9), in the refusal (T7: relied and current), and in the
applied-outcome association (T12). Expected: PR-1's reference equals B1 at
every step; the refusal shows B1 and B2 distinctly; PR-2 references B2 only;
the association references B2, r14 and the resulting objects; T13 returns
recorded state; no step rewrites a reference; whether RC-1 itself carries B2
is recorded as a host observation. T7's per-item refusal is the fixture's; on
a host with a whole-model scope, such as SWBPIPE, the refusal names the host
scope and no failing target (§5; R8-3).

**Evidence labels:** per the C-v0.8 mapping — *illustrative* (this table),
*test-double*, *actual host* (candidate-bound SWBPIPE observation, DEL-09-09).
The first executable return is a candidate-bound test-double observation; it
is not host evidence (V1-B X-08).

**Run on SH-1 (v0.8; S1-B P 7; R12-4).** The table above was run once on the
simulated host SH-1 (C-v0.8 §10.8), on 2026-09-30, over both native paths:
T7 by the command line, T10 and T12's observation by the MCP-tool path, T13
with the MCP response dropped, then observation and retry by the command
line. Observed: at T7 both PR-1 items *refused — stale*, failing target S-3,
relied B1 (r12), current r13; at T10 PR-2 *queued* with lineage PR-1; after
T11 item 1 *accepted* (A5) and item 2 *rejected* (A10), derived state
*mixed*; at T12 item 1 *applied*, RC-1, r14, S-5 created and R-100 changed,
A5 kept; at T13 the observation returned the recorded state with two
submissions and the retry was answered from recorded state (three
submissions, RC-1), with no stale refusal. No step rewrote a relied-on
reference (all five basis elements compared). `prototype/proposal_states.py
--check` found every observed item-state change reachable in §4.6 and every
reported derived state equal to DS-1…DS-4. Label *test-double*; not bound to
an App candidate, so this is not yet the candidate-bound return (C-v0.8 §9;
AC-004 of DEL-03-01 stays held).

## 12. Receiving risks from SWBPIPE source limits (HI §11, `e548d4cf`)

Recorded as risks for receiving and the joined witness, not host assignments.
SWBPIPE's answers (2026-09-28) update them as noted; they are answers about
its current state, not commitments. DRAFT PR #885 is open, unmerged and
**deferred** to UI-SUCCESSOR, with the owner's live-controller activation
still in force; the work graph's deferral governs over the PR description
(ANS §0 A-2, §3 item 11; R8-7):

| Observed limit | Risk to this contract | Where checked |
|---|---|---|
| Queue-time basis differs from original external inspection basis | Stale check against a queue-time basis would silently substitute a later basis (violates §3.2, §5). SWBPIPE (SQ-07 (c)): true of main's offline intake; DRAFT #885 freezes the inspected basis at preview and keeps it at submit, which would retire the risk if merged and qualified | DEL-09-09 VER-004; VC-P-04/07 against actual host |
| No durable exactly-once domain outcome established; runtime transport is not a joined live mutation path | §7 one-effect and §5 precedence not evidenced by transport dedup or shared validation. SWBPIPE (SQ-08 (c)): DRAFT #885's associations live only in the running controller; a restart expires handles or yields `outcome_unknown`; durable de-duplication is a SWBPIPE owner decision (durable receipt carrier) | DEL-09-09 VER-008; VC-P-09 |
| Stronger frozen-review checks not assumed for every route | Validation parity (§2) may differ by route | VC-P-02 against actual host |
| Workflow resolution ≠ provider adoption | Origin's workflow identity may not reflect adopted behavior | DEL-04-03 record comparison |

Later mainline or external-session changes need a targeted applicability
check before reliance (HI §11).

## 13. Interfaces provided and expected

Row identifiers are the ACTIVE register rows as read on 2026-09-30 (R9-6).
"Consumer row" and "supplier row" mark a row held only in the other
deliverable's register. A row names a contribution, not its delivery.

| Direction | Counterpart | Content |
|---|---|---|
| Expect from | DEL-03-01/C-v0.8 (DEP-03-02-016) | §3.2 elements; §3.1 five class values; §4.1 results and reporters; §4.4; content identities and method designation; "no longer holds" rule (per item, or the host's stated scope, R8-3); whole-model identity receiving (R8-4); exposure; FX-PIPE-01 incl. OP-C10 undo |
| Expect from | DEL-04-01 (DEP-03-02-017) | A1–A15 names (A15, R12-5, not checkpoint-requirable); class records P-01…P-06 with revision identity; treatment → outcome map; act-declined event; residual `UNRESOLVED{OI-021}` additions |
| Expect from | DEL-04-02 (supplier row DEP-04-02-021; no UPSTREAM row in this register) | Grant display states incl. *effective (policy default)*; grant value and scope per class; settings version identities |
| Expect from | DEL-02-01 (DEP-03-02-027) | Workflow identity; checkpoint declarations (required act, subject class, reached-when); §4.3.7 item rule |
| Expect from | Host owner (DEP-03-02-023) | Route, de-duplication, treatment resolution, constraint receipt (U-P10), validation outcomes, receipts, resulting objects, origin marks, undo route, views, captured acts with capture-evidence references, settings version at application, stale rule confirmation (U-C3), generation meaning (U-C2), one-effect evidence |
| Provide to | DEL-04-02 (DEP-03-02-018) | Direct-branch entry condition and origin semantics (§4.4); standing per outcome (§9) incl. "applied, then reversed" and accepted-then-stale display |
| Provide to | DEL-04-03 (DEP-03-02-019) | Canonical §9 taxonomy; per-submission recording and precedence (§5, §7); applied association with resulting objects; change-item content identity for A5/A10 lapse (L-1); origin and constraint (§3.3); act/evidence table (§10); undo relation *reverses ⟨receipt⟩* (§4.5); item-left events (§4.3). At v0.8: two §9 rows (*refused — identity conflict*; *not known to host*), the minting party and host handles (§3.5 PM-1, PM-2), the host-assigned change-item content identity (PM-6), the evidence limit "de-duplication scope exceeded" (PM-5). At the RP-2 repair: the item-left event as an explicit schema element (§4.3) and the host's capture time on A5/A10 (§9) |
| Provide to | DEL-03-03 (DEP-03-02-020) | This contract unchanged for the external channel; constraint carriage assurance (§3.3, governance phase; only host-held satisfies R2-12; App-assured not available in this increment); *unverified* author identity; *channel not enabled* (App or host reporter), relayed *not exposed*, *not permitted*; the received SWBPIPE vocabulary (§9.1). At v0.8: identity minting and host handles (§3.5 PM-1, PM-2), observation by identity and *not known to host* (PM-4), the de-duplication scope (PM-5), *refused — identity conflict* (PM-3), the per-item table (§4.6) and SQ-P6; the two schemas |
| Provide to | DEL-05-01 (consumer row DEP-05-01-015) | §9 unchanged except the two v0.8 rows; observer-attributed *outcome unknown*; retry keeps identity and precedence; origin, seat role, grant in force and constraint on every dispatch; sibling-draft rule (§3.1 rule 5). At v0.8: the mechanism-free meaning LOOP R-d waits on — observation by identity (§3.5 PM-4) and the order of SQ-P6 — and *refused — identity conflict* |
| Provide to | DEL-05-02 (consumer row DEP-05-02-007) | Per-item dispositions with actors and annotations, lineage, stale indication, item-left events, "accept" wording (§8). At v0.8 (named at the RP-2 repair; V18-3 m-12): the two §9 rows *refused — identity conflict* and *not known to host*; the derived proposal state DS-1…DS-5, in particular *mixed* given with the item list (DS-1) and never a state some item lacks (DS-5); the meanings of proposal identity, handles and observation (§3.5 PM-1…PM-4), whose mechanics stay TBD-002 |
| Provide to | DEL-02-01 (consumer row DEP-02-01-029; arc N-18) / DEL-02-03 (consumer row DEP-02-03-025; arc N-21) | The five contributions the rows name, each in text and schema (`proposal_state.schema.json`; confirmed at the RP-2 repair, R14-8): (1) change-item content identities — §3.1, §3.4, host-assigned at first receipt (§3.5 PM-6); `item.change_item_content_identity` with `identity_method`; (2) per-item dispositions — §4.1, §4.6 PT-1…PT-19; `item.state` (the §9 tokens) and `item.decision` {A5, A10, A11} with its capture time where the host records one; (3) the all-items-decided indication — §4.3, DS-4; `derived_state.all_items_decided`; (4) item-left events — §4.3; `item.item_left` and the standalone `item_left_event` {proposal, item, cause, time, evaluated basis}; (5) applied outcomes with their resulting objects — §9; `item.applied.resulting_objects`, each object's subject content identity and method, or *not supplied* (absent on the object, or `not_supplied` for the list). Tokens per §9 "Tokens" (`applied`, R14-6). For interrupted or replayed history (DEL-02-03): PT-18/PT-19, PM-4, PM-5 and SQ-P6. Governance phase only, and named by no register row: governing constraint semantics and the *not permitted* outcome (§4.4) |
| Provide to | DEL-03-04 (DEP-03-02-021) | §1 authority map and this table |
| Provide to | DEL-09-09 (DEP-03-02-022) | §11 scenario, §12 risks, VC-P cases and expected outcomes |
| Provide to | DEL-03-01 (consumer row DEP-03-01-026) | M3-CP return (§11) |
| Provide to | Host proposal views (DEP-03-02-024) | §8 information |
| Provide to | DEL-09-06 (consumer row DEP-09-06-028) | Proposal and outcome meanings for the connected activity: this contract unchanged (§§2–10). Nothing specific to DEL-09-06 is defined here |
| Provide to | DEL-10-03, outside the 14 first-increment deliverables (consumer row DEP-10-03-012) | Proposal, validation and outcome obligations for the shared responsibility account: §1 and this table |

## 14. Examples (FX-PIPE-01 fixture subjects)

All material is **invented** and taken from the shared catalogue (C-v0.8
§10), except the rows marked SWBPIPE, which use SWBPIPE's answered terms. Labels are fixture labels, not identities, wire names or SWBPIPE
commitments.

**E-1 PR-2 in the host view after T10:**

| Row | Item | Object | Attribute | Old (at r13) | New | Why | Origin | Disposition |
|---|---|---|---|---|---|---|---|---|
| new support | 1 | new support on R-100 at 4.2 m (targets R-100, S-2, S-3) | created | — | guide support | Span S-2→S-3 exceeds 6 m (T4 findings; T4a host check failed: support spacing) | agent seat (role: host agent), conversation K-7, workflow {workflow, host, ⟨fx-root⟩, supports-adjust, ⟨rev-3⟩} run 12 | queued |
| S-3 | 2 | S-3 | stiffness | value at r13 (Engineer A's T6 edit) | 2.0e6 N/m | Reduce thermal restraint | same | queued |

**E-2 Truthful reports:**

| Situation | Correct report | Incorrect report |
|---|---|---|
| T10 submit succeeded | "PR-2 queued (2 items); awaiting your decision" | "PR-2 applied" / "accepted" |
| After T11, before T12 | "Item 1 accepted by Engineer A, not yet applied; item 2 rejected by Engineer A" | "Item 1 applied"; "item 2 refused" |
| T12 | "Item 1 applied, receipt RC-1, now r14; created support S-5" | "Item 1 approved" |
| T13 retry answered | "PR-2 already processed: item 1 applied (RC-1); item 2 rejected" | "PR-2 refused — stale" |
| T16 direct application of OP-C9 under ⟨set-2⟩ | "Applied under your grant (settings ⟨set-2⟩); origin-marked; undo available" | "Accepted" |
| T13 not observable | "Outcome unknown (observed by loop); last observed: accepted" | "Applied" or "failed" |
| OP-C4 requested directly at r13 under ⟨set-1⟩ | "Not permitted: add support requires a proposal under your current settings (policy default: propose)" | Silent conversion to a proposal; "unavailable" |
| V-CP1, Phase 1 (R8-1; R8-11 item 2 and R8-12 item 2, as restated by R9-2): the agent follows CP-accept as plan guidance | "Add support proposed (queued, 1 item); checkpoint CP-accept in run 12 expects your acceptance". A direct request, if made anyway, is reported as the host's own outcome; if the host applies it under the grant, the report says so and shows CP-accept as not reached, because no proposal was queued: nothing is requested by reason of an arrival that did not occur, no A5 is forced and none is recorded (R9-2 as corrected by R10-1) | "Not permitted: checkpoint CP-accept…" (no constraint is carried or enforced in Phase 1); "Accepted" |
| V-CP1, governance phase (CP-accept governed; host-held constraint): OP-C4 requested directly under a direct grant while CP-accept (run 12, A5) applies | "Not permitted: checkpoint CP-accept in run 12 requires your acceptance of this change; it must be proposed" — the agent may then submit a proposal, which queues and becomes CP-accept's subject | "Drafted as a proposal"; "Applied; checkpoint waiting" |
| V-S1 | "Item 1 accepted by Engineer A — not applied: refused — stale (relied B2, current ⟨B-r14′⟩)" | "Item 1 accepted" alone; "item 1 applied"; "acceptance lapsed" |
| V-NP1 proposal of OP-C11 | "Renumber nodes proposed (queued). This operation has no policy basis yet (pending OI-021); proposing grants nothing" | "Renumber nodes permitted" |
| T17 undo of RC-2 | "Label change RC-2 reversed by RC-3; your check mark on S-4 (T16a) has lapsed because S-4 changed" | "RC-2 deleted"; "check mark still current" |
| SWBPIPE: the person clears the queue (#885 `withdrawn`) | "The proposal left the queue: cleared by you in review; no decision was recorded" | "Rejected by you"; "Withdrawn by the agent" |
| SWBPIPE: a direct external request (`unsupported_method`) | "Not exposed on this surface (host-reported: unsupported_method)" | "Not permitted"; "Proposal required by your grant" |
| SWBPIPE: the person's Apply fails validation (#885 `rejected: validation_rejected`) | "Refused — invalid at application: ‹host code›" | "Rejected by you" |

## Changes from v0.7

v0.7 = P-v0.7 (last changed at `c896a99d90`; unchanged at `86cafc0e1c`;
sha256 b2b67e656081e41364031c067ca8272240d1f80730e09da262d7d05fbcca6b6e).
Wave B of run APP-V4-DESIGN-PASS-2-20260930 (node B3): design development
under R12. Keyed by R12 ID and by the S1-B survey item (file 2, §2.8).
Every new structure is PROPOSED (R12-1).

| R12 ID / survey item | Change in v0.8 | Where |
|---|---|---|
| S1-B P 4 | Proposal identity and observation as interface meaning: who mints (PM-1), host handles (PM-2), same identity with different content (PM-3, new §9 row *refused — identity conflict*), observation by identity with *not known to host* (PM-4, new §9 row), de-duplication scope (PM-5), host-assigned change-item content identity (PM-6), application after acceptance as a host step (PM-7). §9.1 receives `idempotency_conflict` and `status` by `ticket` | §3.5; §3.1; §3.4; §5; §7; §9; §9.1; U-P1 |
| R12-1; S1-B P 5 | Per-item transition table PT-1…PT-19; derived proposal state DS-1…DS-5; validation of some items only VP-1…VP-3 | §4.6 |
| R12-1; S1-B P 5 | Operating sequences with failure behaviour: withdrawal (SQ-P1), application after acceptance (SQ-P2), direct-branch failure (SQ-P3), partial application error (SQ-P4), two proposals sharing a target (SQ-P5), after outcome unknown (SQ-P6) | §4.7 |
| R12-1, R12-2 | `proposal.schema.json` and `proposal_state.schema.json`, each with valid and invalid instances; §0 states that they select no wire field | §0; files beside |
| R12-3, R12-4; S1-B P 7 | The M3-CP table run on SH-1 (C-v0.8 §10.8, cited, not redefined) over both paths; `prototype/proposal_states.py` checks the run against §4.6 | §11; VC-P-15; VC-P-16 |
| — | §13: DEL-03-03, DEL-05-01 and DEL-04-03 rows name what v0.8 adds | §13 |
| — | Header: v0.8; a Wave B line; the Serves line names the schemas | Header |
| **B5** (node B5, round 2; LOOP-v0.8 §5.3) | §9 note: the two "destination not allowed" results are C-v0.8 §4.1 rows, not proposal outcomes; a submission refused at V-D is never queued; a refusal at contact during application is an *application error*; a carried call's wait is no proposal state. No §9 row and no identifier changes | §9 |
| **R14-8 N-18** (RP-2, in place; V18-4 m-7 (a)) | Item-left events made explicit in `proposal_state.schema.json`: `item_left` {cause, time, evaluated basis} on the item that left, required exactly when it left and with the cause matching its state, refused on any other item; a standalone `item_left_event` document kind; `left_cause` enumerates all five causes. SH-1 emits them; `proposal_states.py --check` verifies them; new examples `proposal_state.example-valid-3.json` and `-invalid-2.json`. §13 states the five contributions DEL-02-01 and DEL-02-03 receive, each with its text and schema locus | §4.3; §4.6; §13; schema, examples, prototype |
| **R14-6**, V18-2 M-2, V18-4 m-8 (RP-2) | §9 "Tokens": the §9 outcomes as the schema's `item_state` tokens, `applied` for *applied (receipt)*; identity conflict and not known to host as document kinds; `applied_receipt` is not P's | §9 |
| V18-3 M-1; R14-4 (RP-2; supplier side) | `act_ref.captured_at`: the capture time as the host records it, absent meaning *not supplied by host*; §9 *accepted* and *rejected* carry it; the valid example and SH-1 carry it | §9; schema; example |
| R14-8 N-21; V18-4 m-7 (c) (RP-2) | §9: a resulting object without its subject content identity or method has them *not supplied*; the schema description says so | §9; schema |
| V18-3 m-13 (RP-2) | §3.1 rule 5 and U-P9: the malformed-sibling part is ruled by R12-7 (LOOP adopts the rule; PROPOSED until observed); U-P9 narrowed | §3.1; UNRESOLVED U-P9 |
| V18-3 m-12 (RP-2) | §13 "Provide to DEL-05-02" names the two v0.8 §9 rows, DS-1…DS-5 (*mixed* with the item list) and §3.5 PM-1…PM-4 | §13 |
| V18-1 m-5 (RP-2) | A15 added to §10's act table (not a change through this route; never checkpoint-required) and to "Expect from DEL-04-01" (A1–A15) | §10; §13 |
| V18-2 m-9 (RP-2) | `proposal.schema.json` workflow identity `origin` limited to WD §6.1's project, user, bundled, host | schema |
| V18-3 n-1 (RP-2) | Body citations of C re-pointed to C-v0.8 (§0, §2, §3.1, §3.2 heading, §4.5, §9, §11, §13, §14, verification cases); §0 cites EXEC-v0.6 §2.4–§2.5 for the App-run mechanism | Body |
| — (RP-2) | Header: the repair's inputs pinned on the Wave B line; VC-P-15 and VC-P-16 record the rerun | Header; Verification cases |
| V18-2 m-9 (RX, residual sweep) | `proposal.schema.json`: the workflow identity's `derived_from` is the full identity tuple (`$ref` to this schema's `workflow_identity`), as WD-v0.8 §6.1 and its `workflow_identity` state, never a string. No example carries it; nothing else changes | schema |

New identifiers: PM-1…PM-7, PT-1…PT-19, DS-1…DS-5, VP-1…VP-3, SQ-P1…SQ-P6,
VC-P-15, VC-P-16, and the §9 rows *refused — identity conflict* and *not
known to host*; at the RP-2 repair the schema elements `item_left`,
`item_left_event` and `act_ref.captured_at` (no new identifier in the text). No existing identifier is removed or re-meant, and the rest of
§9 is unchanged. Not done here: S1-B P items 1–3 and 6 (Wave A or other
nodes); no identity representation, encoding or de-duplication mechanism is
chosen (TBD-002).

## Changes from v0.6

v0.6 = P-v0.6 (last changed at `f5ceef164a`; unchanged at `3dd7c22c73`; sha256
410fb289e16177e11190db45be37e02b5d82ebf7a9fcff8676e938bb23a51af9). Wave A of
run APP-V4-DESIGN-PASS-2-20260930 (node A1-B): alignment to the amended basis
and the revised ScopeOfWork under R9. No new design content. Keyed by R9 ID
and by the S1-B survey item (file 2).

| R9 ID / survey item | Change in v0.7 | Where |
|---|---|---|
| R9-11 | P-v0.6 → P-v0.7. Still DRAFT: unsupplied, unimplemented, not accepted | Header |
| R9-5 (S1-B 2.1 pins 2–6, 8, 10, 11, 13, 14; 2.8 item 1) | Basis re-pinned: the four basis documents at their current sha256, naming SCA-V4-001 and SCA-V4-002; ScopeOfWork.md at its current sha256, naming AX-004; DAG-003; the current Case_Datasheet and OWNER_DECISIONS states; R6, R8 and R9 added to the rulings. The v0.6 pins are kept as history. Consumed inputs gain a Wave A paragraph (siblings by label only; R8 and the intake OWNER_DECISIONS at their current sha256; RELAY_ANSWERS at `afb6e063…`), and the earlier passes are marked as history | Header |
| R9-1, R9-3 (S1-B 2.1 pin 16; 2.3) | "V4-WF-05's first half" and "flagged for the next accepted-basis update" are dropped. The phase statement cites V4-WF-05 and V4-HI-42 as amended and uses the R9-1 summary: the request for the act and its recording are in force in every phase, and only the hold is phased. First use reads "the current phase (Phase 1)" | Header, §0 |
| R9-1 (who requests; INTEGRATION) | §0 states the ruling and points to EXEC, Wave B, for the mechanism. §4.4 "Other checkpoints" now says that the act is requested | §0; §4.4 |
| R9-1, R9-2, R9-4 (R8-11 item 2; OWNER_ITEMS O-25; S1-B 2.3 (a), (b)) | S-P13 opens with the amended V4-HI-42 ("Autonomy does not override a workflow's declared checkpoints", quoted), not "Workflow checkpoints override autonomy". D2's reserved-act sentence binds; V4-HI-42's request clause and record clause are in force; whether the run goes on before the act is for the person and the agents | S-P13 |
| R9-1, R9-2 (R8-12 item 2; S1-B 2.3 (c)) | §4.4 acceptance-checkpoint bullet: the derivation is re-grounded on D2b and the hold that the amended texts phase to the governance layer; "V4-HI-42 and WD I-7 are guidance" is replaced by the request and record clauses in force. On a direct application the checkpoint's act is still requested, no A5 is forced and none is recorded, and the disposition stays *act not performed*. E-2's V-CP1 Phase-1 row follows | §4.4; §14 E-2 |
| R9-8 (R8-12 item 5; S1-B 2.4 P18; 2.8 item 3) | "constraint not carriable on this host" is no longer PROPOSED: adopted in RS R11. The second adopted label, "host reachable without evidenced A13", is named where P states that no A13 is evidenced | §3.3; §10 A13 row |
| R9-4 (S1-B 2.2; 2.8 item 2) | The revised SoW is cited where it now states the rule: REQ-004 (per change item; *rejected* only A10; a host refusal is *refused*; a host's own term is never read as A10 or A11), REQ-008 and AC-009 (one effect per item as a host obligation; a second effect recorded, not hidden), OUT-001 and CLM-003 (change-item content identity; workflow identity; the constraint only in the governance phase). The R8-5 mappings keep INTEGRATION | §2; §3.1; §3.3; §4.1; §4.2; §7; VC-P-09 |
| R9-6 (S1-B 2.2 item 2; 2.6) | Receivers line rebuilt from the ACTIVE register rows, with row IDs, arcs N-18 and N-21, and DEL-09-06 and DEL-10-03 added. §13 carries the row IDs, names the N-18 / N-21 contributions and gains rows for DEL-09-06 and DEL-10-03 | Header; §13 |
| S1-B 2.6 (DEP-03-02-018); 2.8 item 6 | §3.3 names the first grant display state "effective (person-set)", as AS §3 and §4.4 do | §3.3 |
| R9-8 (S1-B 2.4 P16, P17, P26; 2.8 item 6) | UNRESOLVED: the register row is restated against the current registers; the SoW-text row is closed (SCA-V4-001). VC-P-14 names the boundary-owner checker, which exists, follows VER-014's wording and records one tool observation | UNRESOLVED; VC-P-14 |
| R9-5, R9-11 | Body citations of siblings name the Wave A labels (C-v0.7, WD-v0.7, EXEC-v0.5) | Header, §0, §2, §3, §4.5, §9, §11, §13, §14, VC |
| **R10-1** (node A2, in place; R9-2's second bullet corrected) | §4.4 acceptance-checkpoint bullet and E-2's V-CP1 Phase-1 row: a direct application queues no proposal, so the A5 checkpoint (*proposal queued*) is **not reached**; nothing is requested by reason of an arrival that did not occur, no A5 is forced and none is recorded. A checkpoint reached under such a grant has its act requested and is *waiting*. The report shows CP-accept as not reached, not as "requested and not performed" | §4.4; §14 E-2 |
| **K1-1** (node A3, in place; owner DECISION-K1 of 2026-09-30, `APP-V4-DESIGN-PASS-2-20260930/OWNER_DECISIONS.md` sha256 35d6546346907137581be7df3bed4a8ccdb4b8bc55a261ca716040d0ad9f91bc) | §0: who requests is **SETTLED by DECISION-K1 K1-1** (was INTEGRATION, put to the owner) | §0 |
| **K1-2** (node A3, in place) | §10: in the current phase an earlier act counts when it is of the required kind and its content is still current, cited with its time (EXEC SP-6); "prior act not counted" stays for content no longer current, another kind, or the governance-phase option (EXEC SP-6F) | §10 |
| **R11-4** (node A4, in place; V17-A m-1) | The closing sentence below this table is marked "at node A1-B", and a sentence states what node A3 changed: SP-6 is the SETTLED earlier-act rule; capture at or after arrival (R4-5) is now EXEC SP-6F, a governance-phase option; JA-1 added in EXEC; §10 restated | Closing sentence of this table |
| R11 notes, V17-A N-1 (node A4, in place) | §4.4 "Other checkpoints": the requester citation "(R9-1)" gains "SETTLED by DECISION-K1 K1-1", as §0 already says | §4.4 |
| **R11-3** (node A4, in place; V17-A M-1) | Basis line: this run's records pinned at their final bytes: R9 `a64e2415…` (was `c3efe2ff…`), R10 `ad3b6caa…` and R11 `e7343b66…` added, OWNER_DECISIONS `7458e9e8…` (DECISION-K1) added | Header |

At node A1-B: no identifier is added or removed; §9's taxonomy is unchanged. Closed: the SoW-text row. PROPOSED items stay PROPOSED (R9-4): U-P4 (validation failure before queueing), withdrawal before queueing, the sibling-draft rule (§3.1 rule 5; U-P9), A12 supersession (R2-7), capture at or after arrival (R4-5) and no resumption of an ended run (R4-4) are unchanged in standing. At node A3 (DECISION-K1): SP-6 became the SETTLED earlier-act rule for the current phase (EXEC SP-6; K1-2), and capture at or after arrival (the R4-5 rule) is now EXEC SP-6F, PROPOSED, a governance-phase option; the joint answer JA-1 was added in EXEC §4.7 (K1-3); §10 was restated to follow.

## Changes from v0.5

v0.5 = P-v0.5 (last changed at `375c3970c`; unchanged at `94aa9181b`; sha256
6ab94fd10166cf78cda014a2f28ebf4726ce9f82a1c2f180044093b4bbb137e0). Keyed by R8
ID. Sources are I2 rows of INTAKE_MAP.md (`nn.k`, Part 2.2, Part 3/4 items);
R8 overrides I2 where they differ.

| R8 ID (I2 source) | Change in v0.6 | Where |
|---|---|---|
| **R8-1** (DECISION-4 D4-1) | Phase framing added. The governing checkpoint constraint, its carriage assurance, the treatment it forces and hold support are relabelled **governance phase (retained)**, with a Phase-1 statement beside each: no constraint carried by the App, no hold, nothing *not permitted* on a checkpoint's account; the host's own treatment decides. V4-WF-05's first half recorded as phased, not withdrawn. §9's taxonomy is unchanged by phase | Header, §0, §1, §2, §3.3, §4.4, §13 |
| **R8-2** (02.7; Part 2.2 P rows) | §3.3 authority limit in two parts. Governance phase: SQ-02 answered 2026-09-28 with no host-held route (route (iv), none planned), so model-supplied-only carriage against SWBPIPE is **not enforceable** (HS-3 (c)) — this replaces "*not established* while SQ-02 is unanswered" for SWBPIPE; a later decision to plan a route is a revision trigger. §4.4 hold-support bullet gives SWBPIPE's governance-phase values, and D6 is recorded closed for Phase 1. V-CP1-family fixtures stay governance-phase AWAITING INPUT with the STD-2 annotation. U-P10 restated | §3.3, §4.4, UNRESOLVED U-P10 |
| **R8-3** (07.6; Part 3 items 2, 5) | §5 Trigger: R2-13 as amended — per item where the host supplies subject identities, otherwise the host's stated scope, never narrowed (SWBPIPE: whole model); de-duplication first unchanged and confirmed for DRAFT #885 (SQ-08 (b)). Refusal content admits "failing targets not supplied". §11 and §12 row 1 annotated | §5, §11, §12, §13, UNRESOLVED |
| **R8-4** (03.3; Part 4.3) | Applied-outcome association: SWBPIPE supplies target ids, diffs and the new whole-model hash; resulting objects beyond target ids *not supplied*. Undo lapse shown from the identity change | §4.5, §9, U-P2 |
| **R8-5** (01.6, 05.4, 09.2, 09.3, 10.1; Part 3 items 1, 10; Part 4.9) | Outcome mapping: new §9.1 received-vocabulary table; `unsupported_method`/`unsupported_change` → host-reported *not exposed on this surface*, never *not permitted*, R2-4 recorded as not met (§2); #885 `withdrawn` → item left, "cleared by the person, no decision record", with a new item-left cause and §4.2 row; `validation_rejected` → *refused — invalid* at application (new §4.2 row); neither is A10 or A11. Accept-and-apply per batch with no A10 record, and accepted-then-stale not arising, recorded (§4.2, §4.3). Session undo writes no receipt: "reverses ⟨receipt⟩" *not supplied* (§4.5). E-2 gains three SWBPIPE rows | §2, §4.1–§4.5, §9, §9.1, §14 |
| **R8-6** (Part 3 item 4) | §10 A13 row: SWBPIPE has no enablement facility; the launch environment variable is not a captured act; R8-Q4b deferred to the owner. §9.1: `controller_unavailable` → *endpoint unavailable*, channel *disabled* | §9.1, §10 |
| R8-7 (Part 3 items 11, 12; Part 4.11) | Answered standings: SWBPIPE answers recorded in U-P1…U-P8 and U-C2/U-C3/U-C4 effects; U-P1's durable de-duplication and U-P2's capture-evidence storage point to SWBPIPE owner decisions. PR #885 recorded as deferred with the owner's activation in force (§12). "App v4 OI-003" qualified | §0, §10, §12, UNRESOLVED |
| **R8-10** (02.7; Part 5 R8-Q12) | Strict preflight: the agent never adds fields the host schema lacks (SWBPIPE refuses unknown fields, SQ-02 (a), SQ-31). I2 R8-Q12's evidence limit "constraint not carriable on this host" carried as PROPOSED | §3.3 |
| R8-11 (items 1, 2, 5) | S-P13: D2's reserved-act half binds in Phase 1 (host-enforced); its declared-checkpoint half, WD I-7 and V4-HI-42 are Phase-1 guidance. Lapse recording continues in Phase 1 and re-hold is governance phase (§4.3, §4.5). Governance-phase values read the fixture's checkpoints as if declared governed (§0) | S-P13, §0, §4.3, §4.4, §4.5 |
| R8-7 (14.1, 14.2) | §3.3 author identity: SWBPIPE records identity as not verified (SQ-14). SWBPIPE records neither conversation nor workflow run, so the App records them App-side and links by request id | §3.3 |
| **R8-12** (item 7; closing pass, node A6, in place) | Consumed inputs list the post-R8 sibling versions; §0's reference to C §4.1 names C-v0.6 (the list is carried unchanged) | Header, §0 |

Identifiers: new subsection **§9.1**; new item-left cause "cleared by the person, no decision record"; two new §4.2 rows; four new E-2 rows. No identifier removed. C references re-pointed from C-v0.5 to C-v0.6 where C is consumed (the fixture itself is unchanged).

## Changes from v0.4

v0.4 = P-v0.4 (committed; unchanged at `8fb51f07f`).

| R5 / V3 item | Change |
|---|---|
| **R5-2** (V3-B MAJOR-1, Y-1, Y-8) | §3.3 carriage assurance redefined: host-held includes the host loop's own evaluation and received-then-verified constraints; received-only keeps its source's assurance; App-assured not available in this increment (R4-2); only host-held satisfies R2-12. Host loop removed from App-assured. §2, §4.4, §13, U-P10, VC-P-04 aligned |
| **R5-1** (V3-B m-3) | §4.4 hold statements qualified "where hold support allows"; four hold-support values; App-only/App-run holds `UNRESOLVED{D6}` |
| **R5-5** | §4.5 undo and holds: undo lapse re-holds; the person's undo is never "action during hold"; never re-holds an A5 arrival |
| **R5-6** | §10 rules: person's own A1/A2 are R7 operations; reserved-act operations produce the human-act record referenced by R7 |
| **R5-9** (V3-B m-2, Y-7) | §4.3 and §1 "confirms at W7" → confirmed by DEL-02-03; UNRESOLVED mixed-item row closed; C citations → C-v0.5; header states EXEC/ADAPTER/XT v0.2 not read |
| R5-4 | Not applicable: P states no destination text |
| R6-1, R6-5 (V4-B m-2 context; in place, no version bump; R6_RESOLUTIONS sha256 8703e85a…b841) | §3.3 authority limit: model-supplied-only carriage gives *not established* while SQ-02 is unanswered, *not enforceable* only after SQ-02 is answered with no host-held route; §4.4 hold-support values assigned by held actions |
| R6-2, R6-4 | No P text affected; no stale markers found |

## Changes from v0.3

v0.3 = P-v0.3 (committed; unchanged at `f05c7e4cd`).

| R4 / source item | Change |
|---|---|
| **R4-14** (ADAPTER F-1) | §3.3 new element **constraint carriage assurance** {App-assured, host-held, model-supplied, absent}; model-supplied alone does not satisfy R2-12; §2, §1, §13, VC-P-04 and U-P10 no longer say "the external adapter carries" |
| **R4-15** (ADAPTER F-8) | §3.3 author identity may be **unverified**; RS R11 evidence limit named |
| R4-3, R4-7 (EXEC §4.7, F-1) | §4.3 cites DEL-02-03's confirmation with MX-3/MX-6/MX-8; A5 never re-holds |
| R4-4 (EXEC F-4) | §10 run-ended row: no resumption of an ended run; *continues ⟨run⟩* |
| R4-5, R4-6 (EXEC F-3, F-5) | §10 rules: capture after arrival; A12 supersedes only when established |
| R4-12 (EXEC F-9; ADAPTER F-3) | §10 rules: elicitation/user-input answers are not act evidence |
| **R4-19** / V2 m-3 | §4.5 and U-P8 cite **R3-4**; U-P8 narrowed to mechanism and availability |
| R4-19 / V2 m-9 | R3 and R4 hashes added to the header |
| R4-19 / V2 m-11 | Run-ended actor = the person or an observed end; reporter = the loop |
| R4-19 / V2 m-12 | Nothing in P to close |
| V2 §3 ("conversation K-7") | K-7 now declared in C-v0.4 §10.1 |
| C-v0.4 | References to C re-pointed from v0.3 to v0.4 (IDs unchanged; FXA-n rename does not affect P) |

## Changes from v0.2

v0.2 = P-v0.2 (sha256 942c1a3a…8c89, 575 lines, committed at `c387730fb`).

| R2 / IR1 item | Change |
|---|---|
| R2-1, R2-9; IR1-A IR1A-01; IR1-B B-M1 | "policy basis pending" → **no policy basis** (C §3.1 five values); proposing confers no permission; §2, §4.4, E-2 V-NP1 |
| R2-2 | §10 A9 row: never through a reserved act-performing operation |
| R2-3, R2-11; IR1A-16 | S-P14/S-P15 credit D2/D3 only with their text; disabling A13 INTEGRATION |
| R2-4; IR1A-10 | §2 A8 *offered*, not auto-recorded; §9 *not exposed* host-reported and relayed |
| R2-5; IR1A-03 | "declined the item" → A10 "rejected"; §10 act-declined and run-ended events |
| R2-6 | §3.3 *effective (policy default)* state and default-basis settings reference; §4.4 default opens direct only if the record's default is direct |
| R2-7 | §10 A12 binds to setting content; supersession |
| R2-8 | S-P15, §10 A14 recorded only in R13 |
| **R2-12**; IR1-B B-M2, B-M3, X-9; IR1-C IR1C-03 | §3.3 **governing checkpoint constraint** element {run, checkpoint, A5, operation}, carried by loop and external adapter; authority limit and relay question (U-P10); §4.4 and E-2 reworded: direct request → *not permitted* naming the constraint, never "drafted as a proposal" |
| **R2-13**; IR1-B B-M7 | §5/§7 precedence: identity-based de-duplication before basis check; per-item check on relied-on target subject identities; sibling applications do not stale unless shared targets; §3.4 relied-on targets; T13 corrected in §11 and E-2 |
| **R2-14**; IR1-B B-M6 | §9 applied association adds resulting objects; §3.4 creation affected object; E-2 T12 |
| **R2-15**; IR1-A IR1A-06; IR1-B X-5 | §4.5 reworded: relation *reverses ⟨receipt⟩*; A5/A10 on reversed item not lapsed; acts on changed subject content lapse normally; OP-C10; §9 "applied, then reversed" standing |
| **R2-16**; IR1-B X-8, B-m2, B-m13 | §4.2 accepted-then-stale display wording; U-P3 narrowed to host evidence; V-S1 |
| **R2-18**; IR1-C X-14 | §4.3 **item-left events**; all-items-decided; "partial" annotation; WD §4.3.7 cited as the rule; performed A5 checkpoint after stale refusal |
| R2-17 | §4.4 proposal items become the checkpoint subject via reached-when kind (c) |
| R2-20 | §10 capture-evidence reference relay |
| R2-21 | Fixtures re-pointed to C-v0.3 §10 incl. T4a, T16a, variants V-CP1, V-S1, V-NP1 |
| IR1-A IR1A-14 | "grant value" used for direct/propose of a grant; "treatment" for route resolution |
| IR1-B B-m7; IR1-C IR1C-16 | §3.1 rule 5 aligned with LOOP MC-8 |
| IR1-B B-m4, B-m8 | Naming confirmed ("refused — stale", "observer"; seat role separate) — no change needed |
| Commit read rule | Sibling v0.2 texts read from `28bd00499`; hashes in header |
| Coordinator R2 notes (DEL-04-02/03 aligner items) | §5 retry text no longer says a retry is refused stale like any submission (identity de-dup first, R2-13); §4.4 entry condition reads "effective (person-set) direct, or effective (policy default) whose policy-record default is direct" (R2-6) |

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| `UNRESOLVED{OI-021}` operation-specific reserved additions; first connected operation, autonomy, environment | Owner via outside SWB session and App/shared owner | Before connected SoW/execution | Classes for connected operations may gain reserved additions; OP-C11 stays *no policy basis*; §11/§14 invented only |
| Host adoption and enforcement of D2, D3 and R2 treatments | Host owner / SWBPIPE (DEP-001) | Before host conformance | All treatment and act behavior is receiving meaning. SWBPIPE (SQ-05): no class system, no grants, no named reserved list; every change waits for the person's Apply; autonomy is SWBPIPE owner decision OI-016 |
| `UNRESOLVED{OI-003}` (App v4 OI-003; unrelated to SWBPIPE's OI-003) extension promise | Owner with host contract owner | Before extension claim | Not decided here; route parity (§2) required regardless |
| `UNRESOLVED{OI-014}` shared contract/component placement | App/shared contract owners (DEP-03-02-025) | Before structural/production allocation | No placement implied |
| U-P1 Proposal identity and change-item content identity representation, encoding, de-duplication enforcement, outcome-recovery mechanics (TBD-002). **Narrowed at v0.8:** the interface meaning — who mints, host handles, observation by identity, identity conflict, de-duplication scope, host-assigned item content identity — is PROPOSED in §3.5; the mechanism stays open | Relevant contract and host owners (DEP-03-02-026); durable de-duplication across restart: SWBPIPE owner decision (durable receipt carrier; ANS §2) | Before dependent implementation | §3.1, §3.5, §5, §7 obligations testable, and exercised on SH-1 (C-v0.8 §10.8); mechanisms open. SWBPIPE DRAFT #885: caller-supplied `idempotency_key`, controller `preview_ref` and `ticket`; key lookup before the basis check; not durable across restart (SQ-08) |
| U-P2 Actual host route, views, receipts, resulting-object reporting, act capture and capture-evidence references, settings version at application | Host owner / SWBPIPE (DEP-03-02-023) | When integration/witness relies on them | Settings reference at application *unconfirmed* until host-reported; resulting objects may be "not supplied". SWBPIPE: target ids and diffs only (SQ-03 (d)); no capture-evidence reference, and acceptance-record storage is SWBPIPE owner decision PB-TBD-002 (SQ-01) |
| U-P3 (narrowed) Host evidence that application re-checks relied-on targets after acceptance | Host owner (DEP-001) | Before application-path conformance | Contract rule fixed (R-6, R2-16). SWBPIPE: Apply re-runs full engine validation against the claimed hash (SQ-07 (e)); as Apply is the acceptance, accepted-then-stale does not arise there (R8-5) |
| U-P4 Validation failure before queueing: state treatment | Host owner | Before adapter implementation | PROPOSED: refused, stays drafted; confirmed by SWBPIPE (SQ-09 (d)) |
| U-P5 Host refusal at application: whether the host distinguishes it from validation refusal in its records | Host owner | Before outcome recording | Refusals never recorded as A10. SWBPIPE DRAFT #885 distinguishes `validation_rejected` at Apply (SQ-09 (e)), received as *refused — invalid* at application (R8-5) |
| U-P6 Operation-specific withdraw/reject rules beyond R-1 | Host owner (V4-HI-30); OI-021 for the connected operation | Before withdrawal implementation | A11 proposer-only; A10 reserved wherever A5 is. SWBPIPE: no withdraw or reject operation; #885 `withdrawn` is the person clearing the queue, received as item left (R8-5); SWBPIPE autonomy is owner decision OI-016 |
| U-P7 Item application grouping | Host owner | Before application-path implementation | Item-level dispositions defined. SWBPIPE: one batch is one application and one undo checkpoint; atomic (SQ-09 (b), (f)) |
| U-P8 Undo mechanism and availability (OP-C10). Treatment is settled: governed by the policy record of the operation whose receipt it reverses (R3-4, INTEGRATION) | Host owner | Before undo implementation | §4.5 semantics; treatment per R3-4. SWBPIPE: session snapshot undo, not through the route, no receipt, not policy-governed; "reverses ⟨receipt⟩" *not supplied*; acts bound to content it changes still lapse, observed from the model identity (SQ-10; R8-5) |
| U-P9 Sibling-draft grouping mechanics (= LOOP T-OPEN-1). **Narrowed at RP-2:** the malformed-sibling part is ruled by R12-7 (LOOP adopts §3.1 rule 5: valid calls handled on their own, the malformed one refused on its own) | DEL-05-01 with DEL-03-02 and host owner | Before the loop's fixture basis is observed (LOOP MC-8) | §3.1 rule 5 PROPOSED; the R12-7 part INTEGRATION, PROPOSED until observed |
| U-P10 Host receipt of the governing checkpoint constraint, or host evaluation of its own declaration copy (relay, R2-12; SWBPIPE SQ-02); which carriage assurances a host can distinguish (R4-14); only host-held satisfies R2-12 (R5-2) — governance phase (R8-1) | Host owner with DEL-03-02, DEL-05-01, DEL-03-03 (DEP-001). SWBPIPE answered SQ-02 on 2026-09-28: route (iv), none planned; planning one is a SWBPIPE owner decision (ANS §2). D6 is closed for Phase 1 and re-opens with the governance phase (R8-2) | Before the governance-phase V-CP1 / LOOP FX-C9 / PANEL PC-24 / WD VC-11 execution | Phase 1: none; the App carries no constraint (R8-10). Governance phase: those fixtures AWAITING INPUT — SQ-02 answered: no receipt, no host copy (not offered); host joins deferred (DECISION-3); omitted constraint indistinguishable from none |
| ~~Mixed item decisions → checkpoint disposition~~ **Closed**: WD §4.3.7 confirmed by DEL-02-03 (R4-7; R5-9) | — | — | P supplies item data and item-left events |
| U-C2 / U-C3 / U-C4 / U-C12 (shared with DEL-03-01) generation; host confirmation of the per-item stale rule and subject-identity scope; multi-read reliance; per-subject identity not met by SWBPIPE | Host owner with DEL-03-01/DEL-03-02; U-C12 SWBPIPE owner (PB-TBD-002 / DEL-16-03) | Before stale implementation | Contract rule fixed as INTEGRATION (R2-13 as amended by R8-3: the host's stated scope where no subject identities are supplied). SWBPIPE: whole-model identity and staleness only (SQ-03, SQ-07 (d)); new generation per published-project change (SQ-07 (b)); no multi-read reliance concept (SQ-07 (g)) |
| Register (restated at v0.7 against the registers as read 2026-09-30). Now registered: DEP-03-02-027 here (UPSTREAM, DEL-02-01 workflow identity and checkpoint declarations; SCA-V4-001); DEL-02-01's and DEL-02-03's consumption of this contract as DEP-02-01-029 (arc N-18) and DEP-02-03-025 (arc N-21) (SCA-V4-002). Still absent: the DOWNSTREAM mirror of DEP-03-01-026; DOWNSTREAM mirrors to DEL-05-01, DEL-05-02, DEL-02-01, DEL-02-03, DEL-09-06 and DEL-10-03; an UPSTREAM row for DEL-04-02's visible autonomy state (supplier row DEP-04-02-021 only; DAG-003 HANDOFF, V12 F6: advice). SatisfactionStatus is TBD on this register's execution rows where other registers use PENDING (V1-B RF-06/08/09; V1-C RF-2; C1-B M-02-1…M-02-4) | Register owners, through `dependency-extract` (DAG-003 HANDOFF open matters) | At the next register refresh; no arc waits on it | None on content. No register is written in Wave A (R9-10) |
| ~~SoW text (AC-013, TBD-001) still calls OI-001/OI-002 open~~ **Closed** (R9-8): REQ-012, AC-013 and TBD-001 were revised under SCA-V4-001 (AX-004) and now record the D2/D3 ruling; OI-021 and DEP-001 stay open there | — | — | None. This design applies DECISION-1, as the SoW now does |

## Verification cases

Designed. **Run at v0.8, on SH-1 only (C-v0.8 §10.8; label *test-double*):**
VC-P-15, VC-P-16, and the parts of VC-P-07, VC-P-09 and VC-P-12 that §11's
run covers; the rest are not run. Evidence labels per the C-v0.8 mapping
(*illustrative* / *test-double* / *actual host*, with LOOP and PANEL
equivalents; unchanged since C-v0.7). Steps and variants refer to FX-PIPE-01
(C-v0.8 §10.3–§10.4).

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-P-01 Coverage | Map §§1–13 to the twelve scope rows (SOW-070, 090, 091, 170–178), V4-HI-20–25, C-v0.8 elements, R-1–R-9 and R2-1–R2-21 | Every scope row covered; every representation choice named as open with owner; DERIVED/INTEGRATION/PROPOSED markings match R1/R2 | VER-001 |
| VC-P-02 Channel parity | Same OP-C4 proposal, arguments, basis, authority via person, embedded, external; plus invalid (E-location-occupied), stale, direct-without-grant and V-CP1 variants | One route identity; identical outcome/error meanings; direct-without-grant → *not permitted* on every channel naming the governing treatment, never converted; V-CP1 in the governance phase → *not permitted* naming the constraint, and in Phase 1 → the host's own treatment, reported as observed (R8-1) | VER-002 |
| VC-P-03 Host authority / no upgraded result | T10 with no A5 captured | Reported *queued*; never *accepted*; domain truth only in host | VER-003 |
| VC-P-04 Origin, constraint and basis preservation | Trace PR-2 from T9 to T12; V-CP1 dispatch | Author type, seat role, channel, conversation, full workflow identity and run, standing at drafting, both settings references, relied basis B2 and target identities identical at every step; governance phase: V-CP1 on E has host-held carriage (host loop evaluation), and a model-supplied-only V-CP1 variant via X is not relied on for treatment and is recorded as such; Phase 1: no constraint is carried by the App and no field the host schema lacks is added; no case is labeled App-assured; an external caller the host cannot verify shows author identity *unverified* | VER-004 |
| VC-P-05 Lifecycle branches + direct case | T10→T11→T12; item 2 rejected; a withdrawn proposal; T7 stale; T16 direct; a direct request under *unconfirmed* and under *effective (policy default)*; SWBPIPE-form variants (a queue cleared by the person; `validation_rejected` at Apply) | Each disposition with actor and evidence; applied carries association with resulting objects; T16 records no acceptance; unconfirmed / policy default (propose) → direct *not permitted*; a cleared queue → item left, "cleared by the person, no decision record"; `validation_rejected` → *refused — invalid* at application; neither is A10 or A11 (§9.1) | VER-005 |
| VC-P-06 Unknown outcomes | (a) V-OU1; (b) a submission whose application is not established; (c) application error with effect *unknown* | All report *outcome unknown*, attributed to the observer, with last observed state; no inferred success, failure or act | VER-006 |
| VC-P-07 Stale, re-draft, stale-after-accept | T5–T9; V-S1; a host-scope variant (whole model) | T7 per-item refusal with failing target S-3, B1, B2, item-left events (host-scope variant: the scope shown, "failing targets not supplied", never narrowed, R8-3); PR-2 new identity and lineage citing B2; V-S1 → *refused — stale* at application, A5 not lapsed, display per §4.2, no carry to re-draft | VER-007 |
| VC-P-08 No retargeting | Draft PR-2; person selects S-4; submit and inspect | Bound targets and affected objects remain R-100/S-2/S-3 | VER-008 |
| VC-P-09 One effect and precedence | T13 retry (same identity) at r14; variant with two host receipts observed; variant where the first submission never reached the host | T13 answered from recorded state, never stale from its own effect; each submission recorded separately; one effect → same RC-1; two receipts → both recorded (host obligation failed, not hidden; SoW AC-009 as revised under SCA-V4-001); never-received first → treated as first receipt; no global exactly-once claim | VER-009 |
| VC-P-10 Host view info | Inspect E-1 against V4-HI-24 and §8 | Old, new, affected objects and targets, row/item mapping, reason, origin, per-item disposition and annotations, lineage, item-left events present; host named as producer | VER-010 |
| VC-P-11 Execution vs acts | T12 success; T16 direct; T17 undo with T16a; separately evidenced A4, A6, A7 cases; an act-declined event | Success asserts execution only; T17 lapses T16a's A4 but not T11's A5; declined event never recorded as the act; A9 records cite capturing-surface evidence; none inferred from another | VER-011 |
| VC-P-12 Queued/accepted/applied/unknown reporting | T10; after T11; T12; T13; V-S1 | queued; "accepted, not yet applied" with actor; applied with association; T13 recorded state; V-S1 "accepted — not applied: refused — stale" — compared against host records | VER-012 |
| VC-P-13 Policy interface | Review §§2, 3.3, 4.4, 9, 10 against CLM-004, #d3, D2/D3, R-2/R-3/R-5, R2-1–R2-12; V-NP1 | Routine tool permission (A14), direct application, A5 and other acts distinct; reserved acts per D2; constraint → not permitted; no policy basis → proposal confers nothing, A12 widening refused, dependent production *held*; no blanket approval policy | VER-013 |
| VC-P-15 Schemas (v0.8) | DEL-03-01's `prototype/validate_all.py`: `proposal.schema.json` and `proposal_state.schema.json` within the keyword subset; their valid instances pass and invalid ones fail; every change request and recorded state of an SH-1 run validates | **Run 2026-09-30: passed** (2 schemas, 5 instances; 6 change requests and all recorded states of the run). **Rerun at RP-2, 2026-09-30: passed** (2 schemas, 7 instances, including `proposal_state.example-valid-3.json`, a standalone item-left event, and `-invalid-2.json`, an item refused at first receipt without its event; 6 change requests and all recorded states) | VER-001 |
| VC-P-16 Transition table and derived state (v0.8) | `prototype/proposal_states.py --check ‹SH-1 run›`: ten legal sequences end in the expected state; five illegal ones are refused; every item-state change SH-1 reported is reachable in §4.6; every derived state it reported equals DS-1…DS-4; since RP-2, every item that left carries its explicit item-left event (§4.3) with the matching cause, and no other item does | **Run 2026-09-30: passed** (10 legal, 5 illegal, 8 recorded-state documents). **Rerun at RP-2, 2026-09-30: passed** (10 legal, 5 illegal, 5 item-left conformance cases; 8 recorded-state documents, 2 item-left events, each with cause and time, none misplaced) | VER-005, VER-012 |
| VC-P-14 Boundary audit | Check REQ-013 exclusions one-for-one against §1 and §13; run the registered boundary-owner checker (`tools/scope_of_work/check_boundary_owner_resolution.py`) and manually resolve any NOT_CHECKABLE or NO_CITED_CLAIM result (SoW VER-014). The checker exists, so the "when available" of P-v0.6 is dropped. One tool observation is recorded (Wave A, 2026-09-30, on ScopeOfWork.md `35609151…4d0f`): 1 boundary requirement checked, 0 unresolved owners, 0 NOT_CHECKABLE, 0 NO_CITED_CLAIM, exit 0. The one-for-one review against §1 and §13 is not run | Each excluded act resolves to its owner; twelve scope rows retained; no sibling/external completion or SWBPIPE adoption claimed | VER-014 |
