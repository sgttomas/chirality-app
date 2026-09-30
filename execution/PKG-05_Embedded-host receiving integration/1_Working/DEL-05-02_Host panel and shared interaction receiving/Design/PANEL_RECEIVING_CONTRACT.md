# Host panel and shared interaction receiving contract
- Contribution: DEL-05-02/PANEL-v0.7 (supersedes DEL-05-02/PANEL-v0.6, last changed at `caa4334ca` and unchanged at `3dd7c22c73`, file sha256 dd71e11dbe0d9872727524aef69ef80ba118980533148c2aa7453d1176165658; earlier: PANEL-v0.5, last changed at `c6f81a4f2` and unchanged at `94aa9181b`, file sha256 ac47abf0974d5d68386ca713f09fc1478b205545754e8c93c74993977173ebb4; PANEL-v0.4 sha256 cb71bc4b…e84419 at `8fb51f07f`)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Phase (V4-WF-05 and V4-HI-42 as amended by SCA-V4-001; R9-1; R8-1; DECISION-4 D4-1 and clarification): when a run reaches a declared checkpoint, the required human act is requested, and it is recorded as done only when the person performs it, whatever the autonomy setting. Holding the run at the checkpoint until the act is performed is phased to the governance layer: in the current phase (Phase 1) a checkpoint is plan guidance that the person and the agents manage, and neither the App nor a host's embedded loop enforces a hold, blocks a run, or reports a workflow unsupported because a hold cannot be enforced. The reserved acts (V4-HI-30) still bind. So in the current phase the panel shows declared checkpoints as **plan guidance**, shows the agent's request for the act when it is issued (R9-1; §3.5 W-5a), and records each arrival and the act that answers it as **observation** (§3.5). It shows no hold-support value and claims no hold. The hold-support display (§3.2) and the hold parts of §3.5 are kept as the **governance-phase definition (retained)**, not deleted.
- Model access (R8-9; DECISION-4 D4-3): the model setting indicator offers local and cloud as options with **no default**, and a cloud model is reached by **OAuth sign-in or an API key** (§3.1; LOOP-v0.7 §5.1; V4-HOST-01 as amended by SCA-V4-001).
- Network destinations (R8-13; DECISION-5): the panel adds the allow-list settings surface, the in-work request prompt with its scopes (once, this run, always) and the destinations-contacted display (§3.8; PC-30…PC-37). §3.1 and §3.8 cite V4-HOST-02 as amended by SCA-V4-001. Where §3.8 stands against this deliverable's ScopeOfWork is recorded in §3.8 and F-12; the scope question is returned to the owner, and no ScopeOfWork is changed.
- Serves: OUT-001, OUT-002, OUT-003, OUT-004 (conditional state only); REQ-001–REQ-006; AC-001–AC-007; VER-001–VER-007 (all of DEL-05-02)
- Basis: the accepted basis as amended by scope-change amendments SCA-V4-001 (`_ScopeChange/SCA-V4-001_2026-09-28_2155/`, accepted 2026-09-29) and SCA-V4-002 (`_ScopeChange/SCA-V4-002_2026-09-29_1901/`), pinned by current bytes: P/docs/PRD.md sha256 bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd, P/docs/ARCHITECTURE.md sha256 317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c, P/docs/HOST_INTEGRATION.md sha256 d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f and P/docs/EXAMINATION.md sha256 471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0 (v0.6 pinned repo `6e18505e3`, before both amendments); ScopeOfWork.md sha256 beb9c66c38161cbb00d1040e294aa9dfd04af953f9bf539121fcda44356dc82c (revised under SCA-V4-001, its AX-004, at `340ecf341`; v0.6 pinned the INIT contract 5c554956…40cb); the accepted graph `_DAG/_LATEST.md` → DAG-003 (accepted 2026-09-29), cited for the admitted or held layer of register rows; P/docs/PRD.md §2.2 V4-HOST-01/02/04/05/06 (V4-HOST-02 added at v0.7: §3.8 rests on it), §3.1 V4-EXT-01, §4.1 V4-WF-03–06, §4.5 V4-AUT-01–05, §4.7 V4-REC-01/03/05, §5 V4-CST-05, §9 OQ-02/OQ-11; P/docs/ARCHITECTURE.md §3 (V4-ARC-05, reuse candidates), §4, §5 V4-ARC-20; P/docs/HOST_INTEGRATION.md §1, V4-HI-02/04, V4-HI-10–12, V4-HI-20–25, V4-HI-30–33, V4-HI-40–42, V4-HI-70/71, §10 item 7; P/docs/EXAMINATION.md V4-EXM-01–03, V4-EXM-20–23 (V4-EXM-23 added at v0.7: it examines §3.8's content); DECISION_BRIEF.html (sha256 02d38cb1…c4420e8; v0.6 mistyped the suffix as 4c420e8) d2, d3, d5; APP-V4-CLARIFICATION-20260927/DIRECTION.md; SCC-CASE-002 Case_Datasheet M1/M4 rows; Open_Issues OI-013/014/021; External_Dependencies DEP-001; run folder OWNER_DECISIONS.md (sha256 f3f8e5f3…cf81f2e; decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, D2 and D3), R1_RESOLUTIONS.md (2f9c7e72…e177ec4), R2_RESOLUTIONS.md (77cfb845…cdebd088), comparisons/V1-A.md (01811533…e04c09), comparisons/V1-C.md (8d46258a…4a94a6), reviews/IR1-A.md (31b3c7f8…0b648284), reviews/IR1-B.md (70e4a4f6…2846), reviews/IR1-C.md (295e96b3…a426b9); run folder at commit `f05c7e4cd`: OWNER_DECISIONS.md (a9869129…68ad2c; adds `APP-V4-FIRST-INCREMENT-20260928-DECISION-2`, D5 and D6), R3_RESOLUTIONS.md (202d52c7…afbf), R4_RESOLUTIONS.md (50a009b2…032a24), reviews/V2.md (75ba1dff…6ef); run folder at commit `8fb51f07f`: R5_RESOLUTIONS.md (254d0b93…dd6f1), reviews/V3-A.md (f25f5af1…21d87), reviews/V3-B.md (5662fbd0…954a3); run `APP-V4-SWBPIPE-INTAKE-20260928` at commit `94aa9181b`: OWNER_DECISIONS.md (sha256 a5ccab0d39bd1cab37c5556abc9bdedd5341ce76be4712706c8c9d72d623e776; decisions `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3` (host joins deferred) and `-DECISION-4` with its clarification (D4-1 phased checkpoints; D4-2 loop and panel keep V4-ARC-10; D4-3 model access)); P/docs/ARCHITECTURE.md V4-ARC-10 and `conceptual/DECISIONS.md` D-20 as cited there
- Consumed inputs:
  - **v0.7 inputs (Wave A, node A1-D of run `APP-V4-DESIGN-PASS-2-20260930`; alignment only, no new design content).** R9_RESOLUTIONS.md sha256 c3efe2ffa232dd9293202d4fc891eba4325afeb2e224fecdf8c1b4c5122a9d2c (R9-1…R9-11; binding); that run's BRIEFS.md sha256 698d91d8217cee528812529fa353faac899b4bc1a5be5686552ad88dad6c469a ("Common rules", "A1 — alignment wave") and OWNER_DECISIONS.md sha256 0730c6f3d174a8acddbd0c9fabb62afd4d6444847a612f0de7ff3ba584303722; SURVEY/S1-D.md sha256 a3b0546af4131e0302520bc0dbaad8d6d5587e91d896fb8aa559e32768b19419 (advice: each item was checked against the current sources before it was applied). Rulings R1–R7 by file (`APP-V4-FIRST-INCREMENT-20260928/R1_RESOLUTIONS.md` … `R7_RESOLUTIONS.md`) and R8 (`APP-V4-SWBPIPE-INTAKE-20260928/R8_RESOLUTIONS.md`, current sha256 44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b). Owner records: `APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md` sha256 5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2 (DECISION-3, -4 and -5; these are its bytes at `3733b1421` and now. At `1528a5033`, the commit the R8-13 line below names, the file was 9903bfe0…7fbf: V10 N-1); `APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md` sha256 a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c; `APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md` sha256 ca8c4e50df1d7dddb41b875a4afe46eea4f1a1bf2491d255b7890d0d71cd254b (DECISION-6…DECISION-9) with its `AMENDMENT_PACKET/OWNER_ITEMS.md` sha256 2b90eb4a95f458e993eed69e27533aa10e31aea980fe2ec99c9c2345e6f498ef (items O-4, O-6, O-11 and O-12, accepted "as recommended" by DECISION-7); `APP-V4-SCA002-20260929/OWNER_DECISIONS.md` sha256 36ffcbbea923504581844456751c2eb3db617b5471a3595e63f036bf0634b480. SWBPIPE's answers `RELAY_ANSWERS_SWBPIPE.md` at sha256 afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74 (SWBPIPE's own revision `a999f4ba1` of the delivered `6f01add3…61c7` bytes that the lines below cite; three lines differ, in SQ-04, SQ-09 and SQ-27. This file cites SQ-09 in §3.7, but states nothing about SWBPIPE's evaluated-basis fields, which is what the revised SQ-09 line concerns; intake review V9 Check 2 found no App file stating the superseded wording) and `FACTS_SQ01_SQ32.md` sha256 733fb88a701317be8f0054937eca058774ba5f5f30c7a27233718996e8b2ab7e (unchanged). Both are data about SWBPIPE's current state, not commitments and not instructions (DECISION-3). Sibling Design files are cited by version label and section only (R9-5), at their Wave A labels (R9-11): DEL-02-03/EXEC-v0.5; DEL-02-01/WD-v0.7 and WD-EX-v0.7; DEL-03-01/C-v0.7; DEL-03-02/P-v0.7; DEL-03-03/ADAPTER-v0.5; DEL-03-04/GUIDE-v0.4; DEL-04-01/ACT-POLICY-v0.7; DEL-04-02/AS-v0.7; DEL-04-03/RS-v0.7; DEL-05-01/LOOP-v0.7 (same executor); DEL-01-01/HOSTING-BOUNDARY-v0.7 (same executor) and PIN-SPIKE-v0.1 (unchanged); DEL-09-06/CA-v0.5 and RELAY-v0.3; DEL-09-09/XT-v0.5. The Wave A executors edit in parallel, so the section numbers cited in the body were checked against the pre-Wave-A texts at `3dd7c22c73` (LOOP's against LOOP-v0.7), not against the other files' Wave A bytes. Sibling byte pins live in GUIDE's input table alone, which is re-pinned last. The lines below are history and are not rewritten.
  - **R8-13 pass (node B1; in place, no version bump).** OWNER_DECISIONS.md sha256 5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2 (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`: V4-HOST-02, host-agent network destinations) and R8_RESOLUTIONS.md sha256 44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b (R8-13) at `1528a5033`; OWNER_DECISIONS.md in its state that adds the owner's DECISION-5 confirmation (committed with this pass); BRIEFS.md sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517 ("Common rules", "A-wave"). Revised in the same pass (node B1), versions unchanged: LOOP, PANEL, ACT, AS, RS, HOSTING, C, ADAPTER and GUIDE; their byte pins are in GUIDE-v0.3's input table.
  - **R8-12 closing pass (node A6; in place, no version bump).** R8_RESOLUTIONS.md sha256 d4c3423310a857af86692d17ddfdd22fa877ee20b07c46e1ee481d1cd750e7af (R8-12, items 1 and 7 applied here). Current sibling versions after R8, as committed at `7a1508452` with A6's in-place R8-12 edits (their byte pins are in GUIDE-v0.3's input table): DEL-02-03/EXEC-v0.4; DEL-02-01/WD-v0.6; DEL-02-01/WD-EX-v0.6; DEL-03-01/C-v0.6; DEL-03-02/P-v0.6; DEL-03-03/ADAPTER-v0.4; DEL-03-04/GUIDE-v0.3; DEL-04-01/ACT-POLICY-v0.6; DEL-04-02/AS-v0.6; DEL-04-03/RS-v0.6; DEL-05-01/LOOP-v0.6; DEL-01-01/HOSTING-BOUNDARY-v0.6; DEL-01-01/PIN-SPIKE-v0.1; DEL-09-06/CA-v0.4; DEL-09-09/XT-v0.4; DEL-09-06/RELAY-v0.3. SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` and `FACTS_SQ01_SQ32.md` are unchanged (data about SWBPIPE's current state, not commitments; DECISION-3).
  - **v0.6 inputs (R8 pass, node A4, at `94aa9181b`; read with `git show`).**
    - R8_RESOLUTIONS.md sha256 1770c96e62caf14322811fca82ceb77eca450d3e1be8665cdbdd5550631e8d02 (R8-1…R8-11; binding).
    - INTAKE_MAP.md (I2) sha256 3cc182955c0f3dd70efa0f1c051870229c2ccc08f36c5cf1445f2eef0dd1ea33: rows 01.4, 02.12, 04.4, 05.5, 10.4, 17.3, 18.4, 20.2, 21.1, 22.1, 23.1, 24.2, X.4, X.5; Part 2 §2.1 closing paragraph and §2.2 PANEL rows; Part 3 items 1, 2, 7, 9, 10; Part 4.9, 4.10, 4.11. R8 overrides I2 where they differ.
    - BRIEFS.md sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517 ("Common rules", "A-wave").
    - SWBPIPE's delivered answers `RELAY_ANSWERS_SWBPIPE.md` (DEL-09-06 `Design/`, #1047) sha256 6f01add3977761e42ac6b310faf72ba4fd5455e478605deb83fefb2e4d3a61c7: SQ-01, SQ-02, SQ-05, SQ-07, SQ-09, SQ-10, SQ-18…SQ-24, SQ-28, ANS §2–§4. These are data about SWBPIPE's current state, not commitments (DECISION-3).
    - Owner files revised first in this pass: DEL-02-03/EXEC-v0.4 `EXECUTION_COMPATIBILITY.md` sha256 d32be37797a3c367d342a2d13bbb8dd4279bc52934531d83b8c6ec8c6e7b76d4 (§2.1 PH-1…PH-10, §2.2 GV-1…GV-5, §3.3 CR-8/CR-9, §4 phase notes, §7.2) — *read*; DEL-02-01/WD-v0.6 `WORKFLOW_DECLARATION.md` sha256 fce565edfd0cee3fa4583eb292d11cce3e4121ead0cdbed31ba2fe0a52562f28 (§4.3.0, §4.3.1 `governed`, §5.3 SEAT-1…SEAT-3) — *read*.
    - DEL-05-01/LOOP-v0.6 is revised in the same pass by this executor (§2.4.0, §2.4.4, §5.1, §6.4).
  - **Prior version (v0.5 pass).** DEL-05-02/PANEL-v0.4, sha256 cb71bc4b…e84419, at commit `8fb51f07f`.
  - **Sibling versions current at commit `8fb51f07f`** (superseded for currency by the R8-12 line above) (`git show`; R5-9):
    - DEL-02-03/EXEC-v0.2 (7f7848c0…42317af0): §3.5–§3.6, §4, §6.2 — *read* (hold-support values superseded by R5-1);
    - DEL-03-01/C-v0.4 (e929d39d…659a08c): §10.1 (FXA-1…FXA-5, LIB-A1/A2, AF-1), §10.3, §10.4 — *read*;
    - DEL-02-01/WD-v0.4 (e492ff63…d8e88e): §4.2.4 (R4-8 string), §4.3 — *read*; WD-EX-v0.4 (60ce307a…128ca4) E1d — *read*;
    - DEL-03-02/P-v0.4 (0d3960a2…c5e361); DEL-04-01/ACT-POLICY-v0.4 (d6da05ab…b03b); DEL-04-02/AS-v0.4 (774728d0…f4dab); DEL-04-03/RS-v0.4 (56806b64…40199) — cited for currency;
    - DEL-09-06/RELAY-v0.2 (48dc5a1f…41f65) §3 coverage map — *read*: Q-1 → SQ-02; Q-2 → SQ-01; Q-3 → SQ-22; Q-4 → SQ-23, SQ-10; Q-5 → SQ-21; Q-6 → SQ-18 (a); Q-7 → SQ-24; Q-8 → SQ-05 (c), (e); Q-9 → SQ-20.
  - **Sibling versions current at `c7f5513db` (R6-4; in place; superseded for currency by the R8-12 line above):** EXEC-v0.3 889e4881…ee548e; C-v0.5 a6306bd4…be7a29 (V-GR1 present); P-v0.5 a5ee4946…cd1b7 (§3.3 per R5-2 present); WD-v0.5 32acdd27…45e7c9; WD-EX-v0.5 296875c9…4702f; ACT-POLICY-v0.5 86975a90…5380e7; AS-v0.5 c49be8bb…729e1; RS-v0.5 37bc586e…c27ea; ADAPTER-v0.3 c9195851…225cff4; HOSTING-v0.5 873e76f6…b0eaa; RELAY-v0.3 89b6b9c9…68bdd7. EXEC-v0.3 §3.6 (HS-1…HS-5; R6-1) is *read*; the rest are cited for currency. R6_RESOLUTIONS.md 8703e85a…cb841 and reviews/V4-A.md 121deafc…eab1 are *read*.
  - **DEL-05-01/LOOP-v0.5.** Co-drafted by this executor (v0.5 pass).
  - **DEP-001.** SWBPIPE answers received 2026-09-28 (RELAY_ANSWERS_SWBPIPE.md; I2 read `64ea4e59…0689`, delivered bytes `6f01add3…61c7`, which add clarifications only, R8 delta check); no host panel/view evidence, commitment or contribution received (DEP-001). D6 (App-side holds) is closed for Phase 1 by DECISION-4 and re-opens with the governance phase (R8-2).
- Receivers (R9-6: rebuilt from the ACTIVE rows of the consumers' registers and of this register; layer per `_DAG/_LATEST.md` → DAG-003): among the first-increment deliverables, DEL-02-01 (DEP-02-01-021, held: host-panel consumer requirements; §3, §6), DEL-03-04 (DEP-03-04-015, admitted: panel and shared-interaction receiving requirements, for the guide; the file as a whole), DEL-09-06 (DEP-09-06-017, admitted: panel receiving requirements, for the connected activity; the file as a whole) and DEL-05-01 (DEP-05-01-020, held: the panel receiving needs and meaning at the loop boundary, for its allocation account. Named by DEP-05-01-020; not yet defined here as a list: the needs appear only in the "Consumed definitions" cells of §3.1–§3.3 and in §3.8's references to LOOP NW-8…NW-16. Returned as a Wave B item); outside the first increment, DEL-10-03 (DEP-10-03-016, admitted: host-panel receiving and conformance obligations, for the shared account; §3, §6, §7); the DEL-09-06 relay file (§8 questions) and the external SWBPIPE owner through App-manager preparation and human file relay (DEP-05-02-018, this register's DOWNSTREAM row); DEL-05-02 itself for OUT-003 (VER-002, VER-003, VER-005) and OUT-002/OUT-004 (VER-004, VER-006). CASE-002 M1 named DEL-02-01 (OUT-003; REQ-005; VER-005) and DEL-05-01 (OUT-004; REQ-005; VER-007). Inputs, from this register's ACTIVE rows: DEP-05-02-005 (DEL-02-01), -006 (DEL-03-01), -007 (DEL-03-02), -009 (DEL-04-03), -010 (DEL-05-01), -019 (DEL-04-02) and -020 (DEL-02-03), all held, and -008 (DEL-04-01), admitted; the supplier-side rows DEP-04-01-026, DEP-04-02-020 and DEP-04-03-030 name three of the same exchanges. The arcs N-18, N-21, N-24 and X-1 have no end in DEL-05-02

## 0. How to read this definition

- **Behaviour contract, not layout.** The following are the host owner's:
  - layout;
  - visual design;
  - table and view construction;
  - assembly (SoW CLM-001; ARCH §4; `UNRESOLVED{OI-013}`).
- **Semantic names only.** No wire fields, component names or types are
  selected. The same applies to persistence and placement (OI-013, OI-014).
- **Standing labels.**
  - **SETTLED**: accepted basis, DECISION-1 or DECISION-2, or
    `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3` / `-DECISION-4` / `-DECISION-5`, credited
    only with what it says (R2-11).
  - **DERIVED**, **INTEGRATION** (R-n … R9-n) and **PROPOSED** are used as
    in LOOP-v0.7 §0. From v0.7 (R9-4), SETTLED also labels a reading the
    owner confirmed at an amendment checkpoint, cited to its owner item.
  - `UNRESOLVED{…}` is never a permission, a default or a pass.
- **Phases (R8-1; R9-1; R9-3; EXEC-v0.5 §2.1–§2.2; LOOP-v0.7 §2.4.0).**
  **Phase 1** is the accepted texts' "current phase" (this increment):
  checkpoints are plan guidance, and nothing holds. The
  **governance phase** is a later layer, per workflow that needs it, for
  checkpoints declared **governed** (WD-v0.7 §4.3.1, PROPOSED). Display
  rules that show a hold, a hold-support value or a stopped run are marked
  *governance phase (retained)*. They are relabelled, never deleted, and a
  Phase-1 statement stands beside them. Checkpoint cases give a **Phase-1
  result** and a **governance-phase value**; the governance-phase value
  reads the fixture's checkpoints as if declared governed (R8-11 item 5).
- **SWBPIPE answers (DECISION-3).** Where this file cites an SQ answer, it is
  SWBPIPE's answer about its current state. It is not a commitment,
  delivery, adoption or host evidence. Host joins are deferred.
- **Act names and labels.** Canonical A1–A14 (ACT §2.1). Unqualified
  "checked" means only A4. "Approval" means only A6. Agent work is
  "examination findings". Host results read "host checks passed: ‹named
  checks›" (R-4).
- **Fixture.** Cases cite **FX-PIPE-01** (C-v0.4 §10, carried in C-v0.7 §10) identifiers:
  - workspace FX-W1, generation g1, run R-100, nozzles N-1/N-2, supports
    S-1…S-4, load case LC-1, Engineer A;
  - workflow `supports-adjust` (origin host, ⟨fx-root⟩, ⟨rev-3⟩);
  - operations OP-C1…OP-C9;
  - timeline T1–T17 and Tg; bases B1/B2; proposals PR-1/PR-2; receipts
    RC-1…RC-3.

  The C-v0.3 additions used here are:
  - OP-C10 Undo, OP-C11 (*no policy basis*, pending OI-021) and OP-C12
    (host check);
  - T4a and T16a; S-5 (created at T12);
  - ⟨set-1⟩ (P-03 *effective (policy default)* propose) and ⟨set-2⟩ (T15:
    P-03 direct, scope {FX-W1; {S-4}});
  - FXA-1…FXA-5 (FXA-1: exposed on all three surfaces; C-v0.4 renamed FA-n
    to FXA-n, R5-9); FXA-5: ⟨rev-3⟩ declares `CP-accept` and `CP-check`;
  - named variant **V-GR1** (R5-7): the grant-change-after-arrival run.
  - variants V-S1, V-CP1, V-NP1, V-R1, V-X1 and V-OU1. The v0.2 labels R-101/R-102, S-7…S-9 and "support-adjust" are
  removed. Where a case needs a second workflow, it is a local label
  `L-PANEL-n`, and the case says why. Nothing selects the first connected
  operation (`UNRESOLVED{OI-021}`).

## Changes from v0.6

Wave A of run `APP-V4-DESIGN-PASS-2-20260930` (node A1-D): alignment to the
amended basis and the revised ScopeOfWork, under R9. It adds no new design
content, and every rule not named below is unchanged. Rows are keyed by R9
ID and by the survey item (S1-D, PANEL §8) each change answers.

| R9 ID / survey item | Change in v0.7 | Where |
|---|---|---|
| R9-11 | Version v0.6 → v0.7. Status stays DRAFT: unsupplied, unimplemented and not accepted | Header |
| R9-5; S1-D PANEL item 1 | Header re-pinned: the four basis documents by current sha256, naming SCA-V4-001 and SCA-V4-002; ScopeOfWork `beb9c66c…c82c` (v0.6 pinned the INIT contract `5c554956…40cb`); `_DAG/_LATEST.md` → DAG-003; R9 with the run's briefs, survey and owner record; R8 at its current hash; the owner records of the two amendment runs; SWBPIPE's answers at `afb6e063…0e74` with V9's finding; siblings by Wave A label and section only. V4-HOST-02 and V4-EXM-23 are added to the Basis line, because §3.8 rests on them. The DECISION_BRIEF suffix is corrected (`…c4420e8`). The OWNER_DECISIONS pin `5fd780bf…` is tied to its commit `3733b1421` (V10 N-1). History lines are not rewritten | Header |
| R9-1, R9-3; S1-D PANEL item 3 | Checkpoint wording moved onto the amended V4-WF-05 and V4-HI-42, using the R9-1 summary. The "first half … flagged for the next accepted-basis update" marker is dropped from live text. W-5a gains the **act request**: in force in every phase; in the current phase the agent carrying out the workflow asks (R9-1, INTEGRATION), the panel shows the request when issued, and neither the App nor the loop issues it in the agent's place | Header, §0, §3.1, §3.2, §3.5 (lead, W-5a), VC-03 |
| R9-2 | R8-11 item 2 and R8-12 item 2 restated: under an effective direct grant no A5 is forced and none is shown; the checkpoint's act is still requested, and no act is shown performed unless the person performs it | §3.3 "Direct autonomy and checkpoints", §7 PC-24 |
| R9-4; S1-D PANEL item 2 | §3.1, §3.8 and the header cite V4-HOST-01 and V4-HOST-02 as amended; the "flagged" markers on them are dropped. §3.8 names the accepted texts that now carry DECISION-5 | Header, §3.1, §3.8 |
| R9-8; S1-D PANEL item 2 | Closed with their records: F-3 and the §3.6 line on DEL-04-02 (SoW CLM-002, REQ-006; DEP-05-02-019); F-4 (SoW P/OQ-11 paragraph; DEP-05-02-016); F-5 (SoW TBD-003; DEP-05-02-011); F-9; the UNRESOLVED rows on V4-WF-05, V4-HOST-01, V4-HOST-02 and the DEL-04-02 consumption. The rows are kept and marked CLOSED, not deleted | §3.6, Findings, UNRESOLVED |
| S1-D PANEL item 4 | §3.8's standing against DEL-05-02's ScopeOfWork is recorded: the ScopeOfWork does not name the network-destination surfaces. The scope question is returned to the owner (F-12); no ScopeOfWork and no §3.8 rule is changed | §3.8, Findings, UNRESOLVED |
| S1-D PANEL item 6 | §5 act table gains the row for the A12 network-destination grant and its decline. PC-30…PC-37 and ND-4 cite the amended V4-EXM-23 and V4-HI-70 | §3.8 ND-4, §5, §7 |
| R9-6; S1-D PANEL item 6 | Receivers line rebuilt from the live registers, with row IDs and DAG-003 layer, including DEL-03-04, DEL-09-06 and DEL-10-03. DEP-05-01-020's contribution is marked "not yet defined here" (F-13) | Header, Findings |
| R9-5 | Body citations of sibling files carry the Wave A labels (LOOP-v0.7, EXEC-v0.5, WD-v0.7, C-v0.7, P-v0.7, ACT-POLICY-v0.7, AS-v0.7) | §0, §1, §3.1, §3.2, §3.5, §3.8, §7, §8, UNRESOLVED, Verification cases |
| Not applied | S1-D PANEL items 5, 7 and 8 are Wave B or the integrator's and were not started | — |

## Changes from v0.5

Keyed by R8 ID. Sources are I2 rows of INTAKE_MAP.md (`nn.k`, `X.n`, Part 2,
Part 3 items, Part 4). R8 overrides I2 where they differ. SETTLED here means
by DECISION-3 or DECISION-4.

| R8 ID (source) | Change in v0.6 | Where |
|---|---|---|
| **R8-1** (DECISION-4 D4-1 and clarification; SETTLED, framing INTEGRATION) | Phase-1 statement added to §3.5: the panel shows checkpoints as **plan guidance** and records arrival and act as **observation**; nothing shown is a hold; dispositions label the record. *Action during hold* becomes the optional annotation **"continued past ‹checkpoint› before ‹act›"** (§3.1). Acts are shown only when performed, and reserved acts stand (W-6) | Header, §0, §3.1, §3.5, §5 |
| **R8-1** (governance phase retained) | **The hold-support display (§3.2) is recast as governance phase (retained)**, with a Phase-1 "checkpoints as plan guidance" bullet beside it: no hold-support value, no hold claimed, no *unsupported* for a hold reason; the `governed` flag and held actions are shown. Also relabelled, not deleted: "held at checkpoint", "action during hold", the R4-8 reason, W-5d "run stopped", W-5e re-hold, and the §3.3 constraint display | §3.1, §3.2, §3.3, §3.5 W-5a/b/d/e |
| **R8-1** (V4-WF-05) | First half phased, not withdrawn; flagged for the next accepted-basis update | Header, UNRESOLVED |
| **R8-1** (cases) | **PC-03c, PC-19, PC-19b, PC-20, PC-21…PC-21i and PC-24 are two-part**: Phase-1 result and governance-phase value. PC-03c and PC-21f: the call is shown dispatched, not held. PC-21h: "continued past" in place of action during hold. PC-24 Phase 1: the host outcome under the grant is shown; no constraint enforced (R8-11 item 2) | §7 |
| **R8-2** (02.12; P2.17; Part 2 §2.1 closing paragraph) | PC-24's governance-phase value keeps AWAITING INPUT with the STD-2 annotation. §3.2 governance values note SQ-02/SQ-11 answered (HS-3 (c) → *not enforceable* against SWBPIPE; HS-4 no longer masking). D6 row: closed for Phase 1, re-opens with the governance phase | §3.2, §7 PC-24, present-state note, UNRESOLVED |
| **R8-3** (Part 3 item 2) | Staleness scope shown as the host states it where no subject identities exist (SWBPIPE: whole model), never narrowed | §3.7 PN-3 |
| **R8-4** (Part 3 item 3) | Whole-model identity shown as each subject's identity; errs toward a lapse | §3.7 PN-4 |
| **R8-5** (Part 3 items 1, 10; Part 4.9; 10.4) | `unsupported_method`/`unsupported_change` → host-reported *not exposed on this surface*; #885 `withdrawn` → "cleared by the person, no decision record"; `validation_rejected` → *refused — invalid* at application; never A10/A11. Accept = apply per batch; session undo gives no "reversed by ⟨receipt⟩" | §3.1, §3.3 Undo row, §3.7 PN-1/PN-2 |
| **R8-6** | A13 reserved; SWBPIPE has no enablement facility; `controller_unavailable` → *endpoint unavailable*, channel *disabled* | §3.7 PN-6 |
| **R8-7** (X.4, X.5; 01.4, 05.5, 18.4, 20.2, 24.2) | Standings move to **answered**: Consumed inputs, §8 (with gists), DEP-001 row (Q-2 answered: no reference) | Header, §8, UNRESOLVED |
| **R8-8** (DECISION-4 D4-2; SETTLED; Part 3 items 7, 9) | V4-ARC-10 (D-20) **kept**. **Note for SWBPIPE**: its embedded direction ("embedded Runtime", RUNTIME-ADOPT; D-58) predates D-20 and should be updated to the v4 loop when UI-SUCCESSOR resumes; SWBPIPE's to act on. **SEAT-1…SEAT-3 kept**; SWBPIPE's single agent panel noted as the likely counterpart | §1, §8, UNRESOLVED |
| **R8-9** (DECISION-4 D4-3; SETTLED) | Model setting indicator: local chosen; cloud signed in (OAuth); cloud key supplied; cloud no credential; unconfigured. **No default.** No credential content. PC-03b revised; PC-03e added. V4-HOST-01 wording flagged (F-9). V4-HOST-02 wording unchanged, marked **owner clarification pending (R8-9)** in §3.1 | Header, §3.1, §7, Findings, UNRESOLVED |
| **R8-10** (Part 4.10; 17.3) | Grant display for a host without grants: "Host fixed treatment: every change waits for Apply" (PROPOSED; may be deferred). Required-tool evaluation in the host: SWBPIPE not decided | §3.2, §3.6, §3.7 PN-5, UNRESOLVED |
| **R8-11** (items 1–3, 5) | Item 1: lapse shown in Phase 1, re-hold governance phase (W-5e; PC-20). Item 2: no constraint enforced in Phase 1 (§3.3; PC-24). Item 3: invalid declarations shown as a finding only in Phase 1 (§3.2). Item 5: governance-phase values read as if governed (§0, §3.2, §7) | §3.2, §3.3, §3.5, §7 |
| I2 22.1, 23.1 (SQ-22, SQ-23; A rows) | §4 note: SWBPIPE views show old/new values but no stable external reference; references *not supplied*. §5 W-7: SWBPIPE's stale batch message; lapse wording DESIGN; no supersession, accepted-then-stale or reversal marker | §4, §5 |
| **R8-12** (items 1, 7; closing pass, node A6, in place) | Item 1 (F-10 ruled): in Phase 1 a lapse after the resume point reads **"act lapsed at ‹t›"**; nothing says *waiting* and nothing is re-held; a new act is shown when performed. Before resume, "waiting — lapsed at ‹t›" (both phases); governance-phase re-hold keeps "waiting — re-held, lapsed at ‹t› after resume". Changed in W-5e and PC-20. Item 7: consumed inputs list the post-R8 sibling versions (the older sibling blocks are marked as superseded for currency); §0 fixture source, §8 RELAY citation and VC-01's consumed versions refreshed | Header, §0, §3.5 W-5e, §7 PC-20, §8, Findings, Verification cases |
| **R8-13** (DECISION-5; SETTLED; the act mapping INTEGRATION; in place, no version bump) | New **§3.8 Network destinations**: ND-1 the allow-list settings surface (category switches and named entries; the model service "allowed by your model choice"; the always-off items; MCP servers only if they follow the stateless MCP revision 2026-07-28; "always" entries with their source); ND-2 the in-work request prompt (scopes once / this run / always, for the destination or its category; decline; only the requesting call waits; never granted by silence); ND-3 the decline wording "destination not allowed by the person"; ND-4 the destinations-contacted display (any model mode; the allowing grant or entry; outside processes with "process network not observed"); ND-5 the grant display. The §3.1 V4-HOST-02 "owner clarification pending (R8-9)" marker is replaced by the revised V4-HOST-02 (DECISION-5; flagged for the next accepted-basis update). §1 permission layer: the destination prompt is not a tool-permission prompt. New **PC-30…PC-37**, F-11 and UNRESOLVED rows; VC-01 and VC-05 extended | Header, §0, §1, §3.1, §3.8, §7, Findings, UNRESOLVED, Verification cases |
| R8-13 close — in place | The owner confirmed DECISION-5 (the reading of "MCP V2"; the person-only grant stands), so the "open to the owner's correction" markers are closed. The consumed-input line is corrected: OWNER_DECISIONS.md is cited in its state that adds that confirmation, not at `1528a5033` |
| V10 S-1…S-4 — in place | The wording of the DECISION-5 confirmation is made precise (the "MCP V2" reading was confirmed; the person-only grant was not objected to and stands). The revised V4-HOST-02 is "the recorder's wording confirmed by the owner". The always-off item reads "a silent switch". ACT F-22 is updated. No rule changes |

## Changes from v0.4

| Item | Change (section) |
|---|---|
| R5-1 (V3-A MAJOR-1) | §3.2 shows hold support in the **four ruled values** (*enforced by the host loop*, *enforced on the host route*, *not established*, *not enforceable*), each with its requirement-check effect. Host-panel runs are *enforced by the host loop*. The EXEC-v0.1 values are retired |
| R5-3 (Y-2) | W-5a: the **declared** setting content always binds, and a declaration naming none is invalid unconditionally. An A8 may present the content but never changes the subject |
| R5-7 (V3-A MAJOR-3/5) | PC-21f re-pointed to C named variant **V-GR1**; `L-PANEL-2` dropped. PC-21i: T15 before the arrival is "prior act, not counted". F-7 closed |
| R5-9; V3-A m-3, m-4, m-8, m-12 | FA-n → FXA-n. Unsupported reason aligned to WD's string "checkpoint hold not enforceable on this surface: ‹name›". Holding library marked confirmed (EXEC §6.2). Sibling versions at `8fb51f07f` cited. The R4-n UNRESOLVED row is closed. §8 maps Q-n to RELAY-v0.2 SQ numbers |
| R5-5 | W-5e: a lapse caused by the person's own undo re-holds like any lapse. The undo is never shown as *action during hold*. An undo never re-holds an A5 arrival |
| R6-1 (in place) | §3.2: invalid declarations take **no value** (check *not established*). App-run checkpoints are classified by held actions (EXEC-v0.3 HS-3/HS-5). R6-3 per-value meaning of "held" is shown |
| R6-4 (in place; V4-A m-1) | EXEC-v0.3 and the current sibling versions cited. "R5 elements not yet in sibling text" markers removed |
| R5-4 | No PANEL text credited D5 with recording or showing the destination, so no relabel is needed (checked) |
| R7-4 m-5 (V5 m-5 class; integrator, in place) | §3.2 *not enforceable* example "a constraint carried only as model-supplied" is qualified "once SQ-02 is answered with no host-held route (before that answer, *not established*)" (R6-5). No value changes. |

## Changes from v0.3

| Item | Change (section) |
|---|---|
| R4-2 (D6 deferred; DECISION-2); R4-8 | §3.2 shows **hold support** per declared checkpoint (EXEC §3.6 values) and the *unsupported* reason **"checkpoint hold not enforceable on this surface"**. §3.1 tool activity shows **action during hold**. The panel never claims a hold that is not enforced. App-side holds are `UNRESOLVED{D6}`. Host-loop runs hold via the loop (LOOP §2.4.4) |
| R4-3 (EXEC §4.7) | W-5e is rewritten: "waiting — lapsed at ‹t›" before resume; after resume the **same arrival is re-held**, shown "waiting — re-held, lapsed at ‹t› after resume"; the request is re-issued for the whole scope; A5 and A12 never re-hold. The interim "performed + act-lapsed" display is withdrawn. PC-20 is repaired |
| R4-4 (EXEC §4.9; PROPOSED) | W-5b: **no resumption** of an ended run. Later acts are shown **"after run end"** and change nothing. A continuation run shows **"continues ⟨run⟩"** and inherits nothing. An interruption is shown "interrupted", not ended. PC-21d is repaired; PC-21g added |
| R4-5 (SP-6; PROPOSED) | W-5c: acts captured before the arrival are shown **"prior act on this subject, not counted"**; an unestablishable order is shown "act order unknown". PC-19 is repaired onto T16a; PC-19b shows T2 as a prior act |
| R4-6 (EXEC §4.10) | W-5g and §3.6: a later A12 supersedes **only when established**. A refused A12 does not count and supersedes nothing; pending → *waiting*; lost confirmation → *unknown*. PC-21f is repaired |
| R4-7 (EXEC §4.11) | W-5f cites WD §4.3.7 **as confirmed by DEL-02-03**, with MX-3 (*unknown*), MX-6 ("replaced by arrival n+1") and MX-8 (application error or unknown after A5 annotated) |
| R4-9 | W-5a: the grant-setting subject is the setting named by an A8, otherwise by the declaration. A declaration naming none is shown *invalid* |
| R4-11 | Arrival ordinal and performance ordinal shown with each current arrival (EXEC MA-2) |
| R4-18 (V2 MAJOR-1) | PC-22 re-pointed to C **T15/⟨set-2⟩**: class **P-03**, scope {FX-W1; {S-4}}. T16 OP-C9 on S-4 is direct; OP-C4 on R-100 is outside the scope; OP-C5 on S-4 is held on U-02 |
| R4-19 m-12, m-13; R3/R4 inputs | V2 markers closed (§7 and the UNRESOLVED last row). Fixtures cite C-v0.3. Header cites R3, R4, V2 and DECISION-2. PC-29 uses T16a |

## Changes from v0.2

| Item | Change (section) |
|---|---|
| R2-1 | Class shown with five values including **no policy basis** (reason); *not permitted* displays name it (§3.3, PC-28) |
| R2-2; IR1A-08 | K-4 is restated as *performs*, including A10. The faithful-record operation conditions are a relay question (§3.4, §8) |
| R2-3 | External access enable/disable shown as the person's A13 (disable: INTEGRATION) (§5) |
| R2-4; IR1C-11 | Rejection kinds: loop-side **not offered** (before host validation); host-reported **not exposed on this surface** shown as a host outcome. Reserved entries: *not permitted* with A8 **offered** (§3.1, §3.3, K-4) |
| R2-5; IR1C-06; IR1A-03 | **Act-declined event** for A4, A6, A7 and A12 with capture evidence. It is separate from the **run-ended** event (W-5d, §5) |
| R2-6 | Grant state **effective (policy default)** added (§3.6) |
| R2-7 (PROPOSED) | A12 supersession shown. A refused A12 at a checkpoint is held for W7 (§3.5 W-5g, §5) |
| R2-9 | No-policy-basis wording. An A12 widening such a class is shown *refused (reason: no policy basis)*. Cases HELD (§3.6, PC-28) |
| R2-11; IR1C-17 | §1 attribution: no classifier mode is SETTLED (D3). No separate routine tool-permission layer is DERIVED |
| R2-12 | PC-24 is **AWAITING INPUT**. The not-permitted display names the governing checkpoint constraint (§3.3) |
| R2-13 | A resubmission shows the proposal's recorded state or outcome, never "stale" because of its own effects (§3.3, PC-10b) |
| R2-14 | Applied items show the resulting objects (created and changed identities) that bound checks refer to (§3.3) |
| R2-15 | Undo shown as "applied, then reversed by ⟨receipt⟩". Acts on changed content lapse normally (§3.3, PC-29) |
| R2-16; IR1-B X-8/B-m2/B-m13; IR1A-11 | **Stale after acceptance** display: "accepted by ‹person› — not applied: refused — stale (relied ‹B›, current ‹B′›)". The A5 is not lapsed. The open item is narrowed to host evidence (§3.3, PC-09b) |
| R2-17 | Checkpoint subject shown by its declared subject class (§3.5 W-5a) |
| R2-18; IR1C-02 | W-5f cites **WD §4.3.7**. "Partial" is a per-item annotation. Items that leave are shown. "All accepted" is never shown over a reduced subject |
| R2-19; IR1A-09 | Lapse before resume: "waiting — lapsed at ‹t›". *Lapsed* is a standing disposition only for ended runs (W-5e) |
| R2-20 (X-11, X-12, X-17); IR1C-08, IR1C-09 | Holding library shown beside origin and never part of identity equality. Run-end *waiting*, and the post-run act rule. The capture-evidence reference is a relay question (§3.2, W-5b, §8) |
| R2-21; IR1C-15; IR1-B B-M9/B-M10/B-m10 | All cases re-pointed to FX-PIPE-01. PC-22 uses OP-C9 (T15 scope) against OP-C4 geometry (§7) |
| IR1C-12 | **"Held at checkpoint (not dispatched)"** tool-activity state (§3.1) |
| IR1C-13 | "Runnable" rule restated in WD outcome terms: the requirement check *passes*, or a run-time hold (§3.2) |
| IR1C-14b | Checkpoint **purpose** and **scope** shown with every act request (W-5a) |
| IR1-B B-m8 | §3.3 origin adds seat role meaning and the two settings references |
| IR1-B B-m5 | Accounting states mapped to C's evidence labels (§7) |
| R3-1 (R3_RESOLUTIONS sha256 202d52c7…afbf; in place, no version bump) | W-5a lists subject classes, including **objects a named output concerns** (INTEGRATION) |
| R3-2 (in place) | W-5a: *targets of the held call* shown only with reached-when kind (a) (INTEGRATION) |

Changes from v0.1 are recorded in PANEL-v0.2 at commit `c387730fb`.

## 1. Scope

A host presents the agent through a panel for **conversation, workflow
selection, the proposal queue and checks**. The agent's work appears in the
host's own tables and views; there is no agent-private surface (V4-HOST-04,
SETTLED). The panel is where the person talks with the agent, selects its
method and decides. Results live in host objects shown in host views.

- Roles recede behind a single agent seat and the selected workflow
  (V4-HOST-05, SETTLED). Role selection is not a panel interaction.
  SEAT-1…SEAT-3 (WD §5.3) are kept (R8-8). SWBPIPE has no seat concept. Its
  UX design has one agent panel (Conversation, Proposals, Checks and
  Accepted tabs), the likely counterpart of the single seat (SQ-19 (d); not
  decided).
- **The v4 direction is kept (R8-8; DECISION-4 D4-2; SETTLED).** This
  contract and LOOP remain the App's receiving contracts for a host panel
  over a host loop under V4-ARC-10, the minimal Chirality loop recorded as
  D-20. **Note for SWBPIPE:** its recorded embedded direction ("embedded
  Runtime", RUNTIME-ADOPT; successor under D-58) predates D-20, and should
  be updated to the v4 loop when the owner resumes UI-SUCCESSOR. That update
  is **SWBPIPE's to make** (LOOP-v0.7 §1). Panel assembly and persistence
  are not decided in SWBPIPE (SQ-20).
- **Permission layer** (R2-11):
  - *No classifier permission mode in hosts; the SWB default proposal mode
    applies*: **SETTLED** (D3).
  - *No separate routine tool-permission prompts in the panel. Host
    operation authority is the person's grant plus adopted policy, resolved
    on the host route*: **DERIVED** from D3 with V4-HI-40/41.
  - Nothing the panel shows stands in for a reserved or professional act.
  - The in-work destination prompt (§3.8) is not a tool-permission prompt.
    It presents the agent's A8 request for the person's A12
    network-destination grant (R8-13; ACT §2.7).

## 2. Definitions used by the receiving rules

| Term | Meaning |
|---|---|
| Host object | A domain object the host owns and stores (run R-100, supports S-1…S-4, load case LC-1). Domain truth stays in the host store (V4-REC-01; V4-CST-05) |
| Domain table | A host view of domain values. An examination never changes it (V4-EXM-21) |
| Host view | A table, view, diagnostic or result display the host gives the person (V4-HI-10) |
| Panel | The host-assembled surface for the four interactions. It lists, summarizes, links and offers host decisions. It holds no domain truth |
| Agent-private result surface | Any place where agent results or proposed changes are visible **only** outside host views, or differ from them. Prohibited (V4-HOST-04; SOW-020) |
| Alternate mutation route | Any path to host objects that bypasses the one validation/application route. Prohibited (V4-HI-20) |
| Findings location | Where A3 findings are held. Either (a) agent message content with references, or (b) host-held findings. `UNRESOLVED{C U-C5}` with the host owner |
| Reference | A pointer to a host object, view position, proposal, change item, receipt or record, followable into the host view. The panel shows references, not copies |

Panel content rules (PROPOSED):

- P-1. Everything shown about an agent result or a proposed change is
  reachable in a host view with the same content. For findings, the rows and
  results they reference must be reachable. Whether the finding text is
  there depends on the findings location.
- P-2. Summaries are allowed ("PR-2: 2 items on R-100"). The authoritative
  old and new values are shown in host views (V4-HI-24, SETTLED).
- P-3. The only mutation path is submission to the host route. Decision
  controls (accept, reject, mark checked, grant change) are host-offered and
  host-captured acts (§5).

## 3. The four interactions, plus checkpoints and grant

### 3.1 Conversation

| Aspect | Receiving requirement |
|---|---|
| Person does | Writes; reads; follows references; cancels a turn |
| Panel presents | <ul><li>**Message stream** with speaker (LOOP §2.1). Completion standing: streaming, complete, truncated, interrupted, cancelled or failed.</li><li>**Tool activity** (LOOP §2.3):<ul><li>requested;</li><li>**rejected before host validation**, with the kind: unparseable/truncated, **not offered**, schema, or offer out of date;</li><li>**held at checkpoint (not dispatched)**, naming the checkpoint (IR1C-12) — **governance phase only**; in Phase 1 no call is held (LOOP §2.4.0);</li><li>**Phase 1 (R8-1):** the optional plain annotation **"continued past ‹checkpoint› before ‹act›"** on a run action observed after an arrival and before the act that answers it, with its reference. Information only, never a defect or violation (LOOP LP-4; EXEC PH-7);</li><li>**action during hold** (**governance phase**, retained): a dispatch or output that the loop observed after an arrival event of a governed checkpoint (e.g. a call already in flight), with its reference, never hidden (LOOP §2.4.4; R4-2);</li><li>dispatched;</li><li>host outcome in P §9 terms, including a **host-reported *not exposed on this surface*** (SWBPIPE term mapping: §3.7);</li><li>*outcome unknown*, with reporter and last observed state.</li></ul></li><li>**A8 requests**, shown only when issued, with requester, purpose and scope. At a declared checkpoint the agent's A8 is the request for the required act (V4-WF-05 as amended; R9-1; §3.5 W-5a).</li><li>**Model setting indicator** (LOOP-v0.7 §5.1; R8-9; V4-HOST-01 as amended): local chosen; cloud chosen, signed in (OAuth); cloud chosen, key supplied; cloud chosen, no credential; unconfigured (no choice made). There is **no default** between local and cloud, only options the person chooses among. No credential content (key or sign-in) is shown. Destinations follow LOOP NW-2 and §5.1.1 under **V4-HOST-02 as amended by SCA-V4-001** (DECISION-5; R8-13).</li><li>**"Model request refused at boundary"**.</li><li>**Network destinations (R8-13):** the in-work destination request prompt, declines and the destinations contacted, as §3.8 defines them.</li></ul> |
| Host objects/results | References only. Basis and standing as given (V4-HI-11/12), e.g. B1 at T3 |
| Consumed definitions | LOOP messages, events and settings; C basis and standing; P §9; DEL-04-03 conversation reference |
| Responsible | App/shared: this requirement. Host owner: assembly and persistence (`UNRESOLVED{OI-013}`) |
| Must not | Present prose as a host result. Show a rejected or held call as executed. Show success as acceptance. Show an A8 request as the act. In Phase 1, show any call as held or the run as stopped at a checkpoint. Show an agent's destination request, or an agent-written allow-list entry, as a grant (§3.8) |
| Unresolved | OI-013; DEP-05-01-024 (via LOOP) |

### 3.2 Workflow selection

| Aspect | Receiving requirement |
|---|---|
| Person does | Chooses the workflow for a run; sees what it needs, where the method expects the person's acts, and why |
| Panel presents | <ul><li>**Identity**: {kind, origin, source root, name, revision} + derived-from (WD §6.1). An unadapted carried workflow keeps its origin. A host adaptation is a new host-origin identity with derived-from. There is no "App-origin".</li><li>**Holding library** beside the origin for any carried workflow, so that a *project*-origin workflow held in a host library is legible. It **never takes part in identity equality**. Collision reports list the holding library with each origin (R2-20; WD §6.4; **confirmed by EXEC §6.2**).</li><li>**Declared checkpoints**: name; required act (A4, A5, A6, A7 or A12); reached-when; subject class; scope; **purpose**; negative path; held actions; the **governed** flag where declared (WD-v0.7 §4.3.1, PROPOSED).</li><li>**Required tools**, each with its WD §4.2.4 outcome: *present*; *missing*; *not exposed on this surface*; *version mismatch*; *present, currently unavailable* (with reason); *channel not enabled*; *not established* (with reason). Each is shown with its **necessity** (required, or optional with the stated effect).</li><li>**Workflow-level states** (WD §3.4, §4.7): *declared*; *declared empty*; *requirements undeclared*; *unsupported* (with reason; the reason **"checkpoint hold not enforceable on this surface: ‹name›"**, R4-8, in WD's wording, is **governance phase only** and never shown in Phase 1).</li><li>**Checkpoints as plan guidance (Phase 1; R8-1; V4-WF-05 as amended).** Each declared checkpoint is shown as guidance: where the method expects the act, which act, on what subject, for what purpose, and what the plan should not do before it (held actions, shown as guidance). **No hold-support value is shown**, no hold is claimed, and no workflow is shown *unsupported* for a hold reason (EXEC PH-3, CR-8/CR-9). A **governed** flag is shown and honoured only as guidance (PH-9). An invalid or not-established checkpoint declaration is shown as a **declaration finding** (invalid, with its FB code; or not established), and does not change the requirement-check display (R8-11 item 3).</li><li>**Hold support — governance phase (retained; R5-1, R6-1, R8-1).** For checkpoints declared governed, once the owner takes the governance phase up, per declared checkpoint and acting surface, in exactly one of the **four values ruled in R5-1**:<ul><li>*enforced by the host loop*: embedded route, the host loop holds (LOOP §2.4.4); the check passes, with holds subject to host evidence (DEP-001);</li><li>*enforced on the host route*: the host holds or refuses the operation through a host-held constraint, evidenced by SQ-02 and a candidate; the check passes;</li><li>*not established*: depends on a host answer not yet given (SQ-02) or on unagreed exposure; shown *not established*, never a pass and never "unsupported". Against SWBPIPE neither cause now applies: SQ-02 and SQ-11 are answered (R8-2);</li><li>*not enforceable*: no mechanism on this surface in this increment (App-side held actions under D6; a constraint carried only as model-supplied, once SQ-02 is answered with no host-held route — before that answer, *not established*); the workflow is *unsupported* with the R4-8 reason.</li></ul>Invalid or not-established governed declarations take **no value**; they are shown invalid / not established, and the check is *not established* (EXEC HS-1, §4.14; R6-1). An App-run governed checkpoint is classified by **what it must hold**: all held actions are host operations → the value follows SQ-02 (*enforced on the host route* / *not established* / *not enforceable*; against SWBPIPE, route (iv) gives *not enforceable*, R8-2); any App-side held action → *not enforceable* (D6) (EXEC HS-3/HS-5; R6-1). What "held" means per value is shown (R6-3): *enforced by the host loop* → the run stops at its next action; *enforced on the host route* → the host refuses held host operations, and other actions are shown as *action during hold*; *not established* / *not enforceable* → nothing is stopped, and actions are shown as *action during hold*. Host-panel runs are *enforced by the host loop* (SWBPIPE has no host loop, SQ-20, so no such evidence can exist for it now). Residual limits are shown, including **action during hold**. The panel never shows a hold as enforced when it is not. App-side holds remain `UNRESOLVED{D6}`: closed for Phase 1 by DECISION-4, re-opening with the governance phase (R8-2). These values read the fixture's checkpoints as if governed (R8-11 item 5).</li></ul> |
| Runnable rule (IR1C-13) | The panel shows the **requirement check passes** only when every reference whose necessity is *required* is *present* or *present, currently unavailable*. The latter is shown as a **run-time hold** with its reason, not as missing. Any other outcome for a required reference means the check does not pass, and the reason is shown. A workflow with *requirements undeclared* stays **selectable**, labeled "requirements undeclared — check not established". It is never labeled runnable-by-check or "no requirements". *Unsupported* is shown with its reason |
| Host objects/results | The run is associated with the selected identity tuple (V4-HI-70) |
| Consumed definitions | WD declaration, identity, §4.2.4 and §3.4 vocabulary; C exposure element 9; ACT act names; DEL-04-03 run record |
| Responsible | App/shared: this requirement. Host owner: assembly, host workflows, evaluation of outcomes |
| Must not | Silently rebind a selection. Collapse *not established*, *not exposed* or *currently unavailable* into present/absent. Show a failed check as a pass |
| Unresolved | Which party evaluates outcomes in the host; a DEL-02-03 checker is relevant only if OI-014 allocates one. SWBPIPE: not decided (SQ-17 (c), SQ-20) |

### 3.3 Proposal queue

| Aspect | Receiving requirement |
|---|---|
| Person does | Reviews proposed changes in host tables. Accepts item by item, several items, or a batch (V4-HI-41). Rejects. Opens objects |
| Panel presents | <ul><li>Per proposal: reference; **per change item**: objects, old/new values (in host views), reason, current disposition; stale indication; lineage for a re-draft (PR-2 ← PR-1, T9).</li><li>Proposal state **derived from items, never stronger** (P §4.3).</li><li>**Origin** (P §3.3): author type; seat; **seat role meaning** (or unknown); channel; conversation; workflow identity tuple; run; standing at drafting (grant display state); **settings reference at route decision**; **settings reference at application** (host-reported, or *unconfirmed*); reason (IR1-B B-m8).</li><li>Relied-on basis.</li><li>Outcomes per P §9 and C §4.1 unchanged: queued; accepted (A5, actor); rejected (A10, actor); withdrawn (A11); applied with receipt and branch (direct under grant / after acceptance) with **resulting objects** (created and changed identities, R2-14); application error (effect none/partial/unknown); refused — invalid; refused — stale (both bases); unavailable; not permitted (naming governing treatment, policy record, or **governing checkpoint constraint** (governance phase), and the class value including **no policy basis (reason)**); channel not enabled; not exposed on this surface (host-reported); error; outcome unknown (reporter, last observed state).</li><li>Every non-success shows the evaluated basis. Decision wording is **accept**, never approve (V4-HI-33, SETTLED).</li></ul> |
| Stale after acceptance (R2-16) | An accepted item refused stale at application is shown as **"accepted by ‹person› — not applied: refused — stale (relied ‹B›, current ‹B′›)"**. The A5 is **not lapsed** and stays bound to its item content. The item's state is never "accepted" alone, nor "applied". A re-draft shows no carried acceptance. The checkpoint effect follows W-5f |
| Resubmission (R2-13) | A resubmission of the same proposal identity shows that proposal's recorded state or outcome, e.g. PR-2 item 1 applied with RC-1 at T13. It is never shown as stale because of its own effects |
| Undo (R2-15) | An applied change later undone shows **"applied, then reversed by ⟨receipt⟩"** (T16 RC-2, reversed by RC-3 at T17). Acts bound to content the undo changed are shown lapsed, as for any change. SWBPIPE's session undo writes no receipt, so "reversed by ⟨receipt⟩" is *not supplied* there (R8-5; SQ-10; §3.7) |
| Host objects/results | Proposed items appear in host tables as proposed (V4-EXM-20). Applied changes carry receipts and origin marks (V4-HI-22/71) |
| Acceptance unit | The change item (P §3.1 rules 1–3). A batch is one A5 listing items, each item-bound, with per-item lapse. Applying an accepted item does not lapse the A5 |
| Direct autonomy and checkpoints | Direct application shows only in an *effective* grant state whose value is direct (R-8; R2-6), with origin, undo route and later-examination route (P §4.4). **Phase 1 (R8-1; R8-11 item 2 as restated by R9-2):** no governing checkpoint constraint is carried as enforcement. The host's own treatment decides a direct request, and the panel shows the host outcome as reported. A declared A5 checkpoint is shown as guidance for the agent's plan, which proposes instead. If the host applies directly under the grant, no A5 is forced and none is shown; the checkpoint's act is still requested, and the checkpoint shows no act performed unless the person performs it (R9-2). **Governance phase (retained; R2-12):** under a governed A5 checkpoint, a direct request shows **not permitted**, naming the **governing checkpoint constraint**. It never appears as a silently created proposal |
| Consumed definitions | P lifecycle, §9, identities, lineage, stale, no retargeting, one effect (host obligation), undo; C basis; ACT names, wording and treatment map; DEL-04-03 act record and lapse |
| Responsible | App/shared: this requirement. Host owner: tables/views, route, treatment, receipts, capture of A5/A10 (HI §1) |
| Must not | Show queued as applied, or accepted as applied before the receipt. Call a host refusal "rejected". Re-draft or retarget from the panel: a re-draft is the agent's new proposal with lineage. Show a proposal state stronger than its items. Use "approve" |
| Unresolved | Host evidence that application re-checks the basis (DEP-001; P U-P3, narrowed per R2-16). Proposal identity and duplicate mechanics (TBD-002). SWBPIPE term mapping and staleness scope: §3.7 |

### 3.4 Checks

| Subject | Actor | Panel label and presentation | Host objects/results | Consumed |
|---|---|---|---|---|
| A3 examine (e.g. OP-C3 at T4, span S-2→S-3 exceeds the limit) | Agent | "Examination findings", referencing rows/results and the read basis (B1). Standing: agent findings | Domain tables unchanged. Location per §2 | C basis/standing; U-C5; LOOP E-5; DEL-04-03 |
| Host check results (e.g. T1 "equilibrium", "unit consistency" at r12) | Host | "Host checks passed: ‹named checks›", each with its evaluated basis. Currency is shown (LC-1 historical at r13, T6) | Host results | C standing |
| A4 mark checked (e.g. T2 on S-2) | Person (D2a, SETTLED); host act facility captures it | "Checked by Engineer A", with bound subject content (⟨S-2@r12⟩) and state | Content-bound act record | ACT A4; DEL-04-03 |

Rules:

- K-1. Findings are never shown as A4 or A6. "Checked" is used only for A4
  (R-4).
- K-2. An examination changes no domain table. PC-12 compares before and
  after.
- K-3. An A4 lapses visibly when its bound content changes, at any time
  after performance. T14 (S-2 edited at r15) lapses T2's A4. T6 (S-3 edited)
  does not.
- K-4. An operation that **performs** A4, A5, A6, A7, A10, A12 or A13 has
  class **reserved to the person** (R2-2, DERIVED; D2 SETTLED for the acts).
  Examples are OP-C6, OP-C7 and OP-C8.
  - Reserved entries are always offered (R2-4). An agent call shows *not
    permitted*, and an A8 request is **offered**. An A8 is shown only if the
    agent issues one.
  - No faithful record is made through a reserved operation. A host
    faithful-record operation, if any, meets the four R2-2 conditions (§8
    Q-5).
  - Host adoption of the list is DEP-001. Hosts have no classifier mode
    (D3).

### 3.5 Declared checkpoints in the panel

This section consumes LOOP-v0.7 §2.4 (with §2.4.0 and §2.4.4), EXEC-v0.5
§2.1, §2.2 and §4, WD-v0.7 §4.3 and ACT §4.

**Phase 1 (V4-WF-05 and V4-HI-42 as amended by SCA-V4-001; R9-1; R8-1;
DECISION-4 D4-1 and clarification).** The panel shows
declared checkpoints as **plan guidance**, and records each arrival and the
act that answers it as **observation** (LOOP §2.4.0 LP-3; EXEC PH-6). The
host loop enforces no hold in Phase 1, so nothing the panel shows is a hold,
and the panel never shows a run as stopped or held at a checkpoint. The
disposition words label the record: *waiting* reads "reached; act not yet
recorded", never "the run is held" (PH-6; confirmed INTEGRATION by R8-11
item 1). *Action during hold* is not shown in Phase 1. A run action after an
arrival and before the act may carry the optional plain annotation
**"continued past ‹checkpoint› before ‹act›"** (PH-7). The required act is
requested at the checkpoint, by the agent carrying out the workflow (W-5a;
R9-1). Acts are shown as
performed only when the person performed them (PH-4), and reserved acts
stand (PH-5). W-5a…W-5g apply in Phase 1 as recording and display rules,
except the parts marked **governance phase**: the re-hold in W-5e, the
loop-followed path and "run stopped" in W-5d, and any held call. These are
retained for governed checkpoints once the governance phase is taken up.

- W-5a. **Reached.**
  - Shown only when the loop reports that the reached-when condition was
    observed.
  - The display shows: the required act kind; the observed event; the bound
    subject by its **declared subject class** (R2-17) and content
    identities; the declared **purpose** and **scope** (IR1C-14b); the
    actor requirement.
  - The subject classes shown are:
    - change items of a named proposal;
    - named output;
    - objects changed by a named outcome;
    - **objects a named output concerns** (R3-1), e.g. the rows OP-C3
      examined at T4, shown with their subject content identities as read;
    - targets of the held call, shown only with reached-when kind (a)
      (R3-2). In Phase 1 "the held call" names the call whose dispatch met
      reached-when; it is not held;
    - grant setting: the **declared** setting content (classes, grant
      values, scope). It always binds. A declaration that names none is
      shown *invalid* before the run, unconditionally (R5-3). An A8 may
      present that content but never changes the subject. An A12 made on
      different content is shown as recorded and satisfying nothing at this
      checkpoint.
  - Each current arrival is shown with its **arrival ordinal**, and a
    performed arrival with its **performance ordinal** (EXEC §4.1, MA-2;
    R4-11). Earlier arrivals remain history.
  - Never inferred from stage or model text.
  - **Act request (in force in every phase: V4-WF-05 and V4-HI-42 as
    amended. Who requests: R9-1, INTEGRATION).** When the run reaches the
    checkpoint, the required act is requested. In the current phase the
    agent carrying out the workflow asks the person for it, because the
    declared checkpoint is part of the plan it was given. Its request is
    an A8, shown only when issued, with the declared purpose and scope
    (§3.1; LOOP §2.4.0 LP-5). The host offers the person the means to
    perform the act: the host-offered, host-captured control (P-3; §5).
    The panel shows the arrival, the request where the loop reports one,
    and the act only when the person performs it (W-5c). Neither the App
    nor the host's embedded loop issues the request in the agent's place,
    and the panel shows no request that was not issued.
- W-5b. **Dispositions, run end and continuation** (EXEC §4.9; R4-4,
  PROPOSED).
  - The vocabulary is *waiting* · *performed* · *resolved negatively* ·
    *lapsed* · *not reached* · *unknown*. Everything else is an annotation
    (EXEC §4.3).
  - At run end:
    - *not reached* if the condition was never observed;
    - *unknown* if the observation was lost;
    - **waiting** if the arrival was reached but not performed, or was
      re-held (governance phase), shown with the **run-ended** event and
      never as performed (R2-5; RH-7).
  - **An ended run is never resumed.** An act the person performs after the
    run ended is shown against the bound subject marked **"after run end"**.
    It changes no disposition.
  - A **continuation** is a new run shown with **"continues ⟨run⟩"**. It
    inherits no arrival, disposition or act, and its checkpoints start *not
    reached*.
  - An **interruption** is shown "interrupted" (not ended). The run is
    resumed as the same run, and recovered observations are shown with
    their own times (EXEC RE-4, §4.12).
- W-5c. **Clearing.**
  - *Performed* only on capturing-surface evidence of the specified kind, on
    the bound subject content.
  - A faithful record (A9) citing that evidence may be shown as a record
    (W-2). It never clears a checkpoint by itself.
  - Without a host capture-evidence reference (§8 Q-2), no host-content
    checkpoint can show *performed*.
  - **Captured at or after the arrival** (SP-6; R4-5, PROPOSED). An act
    captured before the arrival is shown **"prior act on this subject, not
    counted"**, so the person can repeat it knowingly. An order that cannot
    be established is shown "act order unknown", and the act does not count.
    Alternative U-E4 stays open for the owner.
- W-5d. **Negative decisions** (R2-5).
  - For A5 the negative is A10.
  - For A4, A6, A7 and A12 it is an **act-declined event**, captured by the
    host act facility. It is not an act of the declined kind.
  - The disposition is *resolved negatively*. **Phase 1:** the declared
    negative path is shown as guidance for the agent's plan; nothing is
    stopped by the loop (LOOP LP-8). **Governance phase:** the panel shows
    the declared negative path taken, or "run stopped".
  - Stopping the work is a separate **run-ended** event. A checkpoint
    waiting at that moment stays *waiting*.
- W-5e. **Lapse (both phases) and re-hold (governance phase)** (R2-19; EXEC
  §4.7; R4-3, PROPOSED (W7); R8-1; R8-11 item 1).
  - An **act-lapsed event** is always shown.
  - The resume point is shown as a **run-resumed** event (EXEC HD-5).
  - **Phase 1:** after a lapse past the resume point the arrival reads
    **"act lapsed at ‹t›"**: nothing says *waiting*, and a new act is shown
    when performed (R8-12 item 1). Outputs gated
    by this checkpoint show standing *lapsed* for the affected referents.
    **Nothing is re-held and nothing stops**; the agent re-requests the act
    as its plan requires (LOOP LP-7).
  - **Before resume** (both phases), the disposition reads **"waiting —
    lapsed at ‹t›"**, and a new act on current content is needed.
  - **After resume — governance phase (retained):** while the run is live,
    the **same arrival is re-held**. It reads **"waiting — re-held, lapsed
    at ‹t› after resume"**, with the lapsed referents marked.
    - The run stops at its next action; nothing done is undone.
    - Outputs gated by this checkpoint show standing *lapsed* for the
      affected referents.
    - The act request is re-issued for the **whole** scope.
  - **A5 and A12 never re-hold** (governance phase). The rules on which
    acts lapse (A12 is superseded, not lapsed; applying an accepted item
    does not lapse its A5) apply in both phases as recording rules.
  - *Lapsed* appears as a standing disposition only when the lapse occurs
    after the run has ended. If the run ends while re-held (governance
    phase), it shows *waiting* (RH-7).
  - The v0.3 interim "performed + act-lapsed" display is withdrawn.
  - A lapse caused by the person's own undo (OP-C10) is shown like any other
    lapse. In the governance phase it re-holds like any other lapse. The
    undo is never shown as *action during hold*, nor in Phase 1 annotated
    "continued past". An undo never re-holds an A5 arrival (R5-5).
- W-5f. **Mixed item decisions at an A5 checkpoint** follow **WD §4.3.7, as
  confirmed by DEL-02-03** (EXEC §4.11; R2-18; R4-7):
  - all remaining bound items have A5 → *performed* over them (MX-4);
  - any item undecided → *waiting* (MX-2);
  - none undecided, at least one item's decision observation lost →
    *unknown* (MX-3);
  - all remaining items decided, at least one A10 → *resolved negatively*,
    with a per-item **partial** annotation (MX-5).
  - Items that left without a decision (stale, A11, host refusal) are shown
    with their event.
  - If no items remain, the arrival shows "waiting — no items remain". A new
    arrival closes it as **"replaced by arrival n+1"** (MX-6).
  - An item accepted and then refused stale, or meeting an application error
    or *outcome unknown* at application, leaves the disposition unchanged.
    It shows "accepted — not applied: …" (MX-7, MX-8).
  - A *performed* over a reduced subject is **never** shown as "all
    accepted".
  - Example: FX-PIPE-01 T11 (item 1 A5, item 2 A10) gives *resolved
    negatively (partial: item 1 accepted)*.
- W-5g. **A12 checkpoints** (R2-7, PROPOSED; EXEC §4.10; R4-6).
  - The subject is the setting content (classes, grant values, scope).
  - The control's response is shown:
    - **established** → the arrival counts (*performed*), with the A12 and
      settings version;
    - **pending** → *waiting*, "A12 awaiting control confirmation";
    - **refused** → *waiting*, "A12 by ‹person› refused by control:
      ‹reason›". The refused A12 does not count.
    - confirmation lost → *unknown*.
  - A later A12 supersedes an earlier one **only when established**. A
    refused or pending A12 supersedes nothing, and the earlier setting stays
    in force.
  - A checkpoint the earlier A12 performed stays *performed*, with the
    supersession shown.

### 3.6 Active autonomy grant (DEL-04-02; R-8; R2-6)

The grant is shown per class and scope, from DEL-04-02 §3 with R2-6 applied:

| State | Shown as | Direct branch? |
|---|---|---|
| effective (person-set) | Grant value and scope; A12 reference | Yes, if the value is direct |
| **effective (policy default)** | "Default: ‹value› (policy ‹record›)". No A12, no setting actor | Only if the policy default is *direct*. None is in the first increment (SWB default *propose*) |
| requested by agent | "Agent requests ‹value, scope›", beside the effective value | No |
| set by person, not yet confirmed by control | "Set by you — not yet in force" | No; the prior effective value governs |
| unconfirmed | Last-known value labeled "unconfirmed" | No |
| not set | "not set" (no setting and no default) | No |
| refused (reason) | Reason beside the still-effective value. Includes **"refused — no policy basis"** for an A12 widening a *no policy basis* class (R2-9) | No |

- Grant changes are A12, reserved (D2e). An agent's change is shown only as
  a request (A8).
- A refused A12 is shown as refused. It never replaces the displayed
  effective setting, and "superseded" is shown only on an established later
  A12 (R4-6).
- The grant display and the checkpoint indicator never merge into a single
  "allowed" signal (DEL-04-02 §4).
- This consumption is in this SoW's CLM-002 and REQ-006 since SCA-V4-001
  (owner item O-11), and in the register as DEP-05-02-019 (F-3, closed).
- A host with no grant model (SWBPIPE): §3.7 PN-5.

### 3.7 Receiving notes from SWBPIPE's answers (R8-3, R8-4, R8-5, R8-6, R8-10)

These notes say how the panel would present SWBPIPE's current terms. They
rest on SWBPIPE's answers about its current state (SQ-01, SQ-05, SQ-07,
SQ-09, SQ-10, SQ-13, SQ-28). They are not host evidence, and host joins are
deferred (DECISION-3). No SWBPIPE panel is assembled or selected (SQ-20).

- PN-1 **Outcome mapping (R8-5).**
  - `unsupported_method` / `unsupported_change` are shown as host-reported
    *not exposed on this surface*, never *not permitted*. R2-4 (a named
    rule) is recorded as not met by this host.
  - DRAFT #885 `withdrawn` (the person cleared the queue) is shown as the
    item leaving the queue, "cleared by the person, no decision record".
    It is never shown as A11 "withdrawn by ‹proposer›", nor as A10.
  - `validation_rejected` at Apply is shown as *refused — invalid* at
    application, never as A10 "rejected by ‹person›".
- PN-2 **Accept = apply (R8-5).** On SWBPIPE, acceptance and application are
  one step (Apply), per batch, with no A10 record. The panel keeps the App's
  meanings (§3.3, §5) and records the missing counterparts:
  accepted-then-stale (R2-16), per-item A5/A10 and mixed items do not arise
  there. Session undo writes no receipt, so "reversed by ⟨receipt⟩" is *not
  supplied*.
- PN-3 **Staleness scope (R8-3).** Where the host supplies subject
  identities, staleness is per item (§3.3). Otherwise the panel shows the
  **host's stated staleness scope** and never narrows it. For SWBPIPE this
  is the whole model: any model change stales every queued proposal, e.g.
  "refused — stale (host scope: whole model; relied ‹B›, current ‹B′›)".
  De-duplication first is unchanged.
- PN-4 **Whole-model identity (R8-4).** Bound subjects on a host that
  supplies only a whole-model identity are shown with that identity as each
  subject's content identity. Lapses then show on any model change: this
  errs toward a lapse and never misses one. The panel computes no identity.
- PN-5 **Grant display for a host without grants (R8-10; PROPOSED; may be
  deferred).** The grant area shows "Host fixed treatment: every change
  waits for Apply" (host-stated), never a grant state and never "not set".
- PN-6 **Enablement (R8-6).** A13 stays a reserved act. SWBPIPE has no
  enablement facility (SQ-28), so the external channel stays *not
  enabled*, and A13 cannot be evidenced there. SWBPIPE's
  `controller_unavailable` is shown as *endpoint unavailable*, with the
  channel *disabled*. The external channel's own display is DEL-03-03's.

### 3.8 Network destinations of the host's agent (DECISION-5; R8-13)

The panel presents the person's controls and records for LOOP-v0.7 §5.1.1
(NW-8…NW-16). The rules are **SETTLED by DECISION-5**, and are now carried
by the accepted basis as amended by SCA-V4-001: PRD V4-HOST-02, ARCH
V4-ARC-12 and the ARCH §4 host-agent property. V4-EXM-23 as amended
examines them. Two points are
settled by the owner's DECISION-5 confirmation (2026-09-28: the "MCP V2" reading confirmed; the person-only grant not objected to and stands): the person-only grant, and the reading of "MCP
V2" as the stateless MCP revision 2026-07-28. The act mapping is
**INTEGRATION** (R8-13; ACT §2.7). No display wording or layout is chosen
(§0).

These displays concern the host's embedded agent only. The App's own Codex
keeps the person's Codex configuration, approval and sandbox choices
(ARCH §4, closing sentence of the host-agent property; HOSTING §2). The
App's external-channel destination is DEL-03-03's.

**Standing against this deliverable's ScopeOfWork (v0.7; survey S1-D; a
scope question returned to the owner).** DEL-05-02's ScopeOfWork
(`beb9c66c…c82c`) does not name these surfaces:

- the word "destination" does not occur in it;
- its AX-004 applies DECISION-1, DECISION-3 and DECISION-4, not DECISION-5;
- its scope items are SOW-019 and SOW-020. The scope item that carries
  "every destination contacted is recorded and shown" is SOW-017, assigned
  to DEL-05-01 (`_Decomposition/ScopeLedger.csv`).

§3.8 stands here as the panel's receiving of DEL-05-01's loop events and
destination rules (LOOP §2.3, §5.1.1), under CLM-002 ("`DEL-05-01`
supplies loop messages/tools/events/checkpoints and receiving
requirements") and REQ-001. That is this file's reading; the ScopeOfWork
does not say it. Whether DEL-05-02's contract should name the
network-destination surfaces is for the owner (F-12; UNRESOLVED). No
ScopeOfWork is changed here, and no §3.8 rule is changed.

| Surface | Receiving requirement |
|---|---|
| **ND-1 Allow-list settings** | <ul><li>A **category switch** per category (web access, MCP servers, other APIs, …), and the **named destinations** within each category.</li><li>The selected model service, and for a chosen cloud model its sign-in service, shown as **"allowed by your model choice"**. They change only with the model setting (§3.1; LOOP NW-9).</li><li>The **always-off items** (analytics or usage reporting; a silent switch to another model or provider; background downloads or updates), shown off unless the person turned them on.</li><li>MCP servers are offered only if they follow the stateless MCP revision 2026-07-28. A server that does not is never offered as a choice. Where the host lists it, it is shown only with the reason "not stateless MCP (2026-07-28)".</li><li>Entries that came from an in-work grant scoped **always** show that source and its time.</li><li>Every edit is the person's A12 network-destination grant, captured by the host's control. An agent-written entry is never shown as a grant.</li></ul> |
| **ND-2 In-work request prompt** | <ul><li>Shown when the agent asks (A8): the requester, the destination or its category, the purpose, the requesting call and the scope sought.</li><li>Choices: grant **once**, grant **for this run** or grant **always**, each for the destination or its category; or **decline**.</li><li>Only the requesting call is shown waiting. Other activity continues and is shown as usual.</li><li>An unanswered prompt stays pending. It is never granted by timeout or silence.</li><li>A non-stateless MCP server is offered no grant choice. The prompt shows "cannot be allowed: not stateless MCP (2026-07-28)".</li></ul> |
| **ND-3 Decline** | The requesting call's outcome reads **"destination not allowed by the person"**, as reported to the agent. Nothing is added to the list |
| **ND-4 Destinations contacted** | <ul><li>Every destination contacted, in any model mode, with its category and the grant or list entry that allowed it: "model choice", "category: ‹category›", "named entry", or "in-work grant: once / this run / always, ‹time›".</li><li>Declines and boundary refusals, shown apart from contacts.</li><li>Each outside process (an MCP server or other) with its declared destinations and, when it is not sandboxed, **"process network not observed"**. The panel never implies that the process contacted only what it declared.</li><li>References, not copies, to the run record (RS R15; V4-HI-70 as amended: "for a host's agent, each network destination contacted").</li></ul> |
| **ND-5 Grant display** | Network-destination grants appear with the active grant (§3.6) as AS §3 defines them: the allow list, and the in-work grants with their scopes. They never merge with operation-class grants or checkpoint indicators into a single "allowed" signal |
| Responsible | App/shared: these requirements. Host owner: the control, capture, native enforcement and assembly (`UNRESOLVED{OI-013}`) |
| Must not | Show an agent's request as a grant. Show a grant the person did not make. Show any call but the requesting one as waiting for a grant. Hide a destination contacted. Offer a non-stateless MCP server |

**Phasing.** Phase 1 is the list above. Allow lists locked by an
organization and enforced sandboxing of outside processes are governance
phase (later), not defined here (LOOP §5.1.1).

## 4. Host tables and views: no agent-private surface

| Rule | Source | Rejection case |
|---|---|---|
| H-1 Agent results and proposed changes appear in host tables/views | V4-HOST-04; SOW-020 (SETTLED) | PC-13 |
| H-2 Per change item, host views show old/new values, objects, reason, origin, item state, stale indication | V4-HI-24; P §8 | PC-06 negative variant |
| H-3 Findings reference host rows/results and standing; domain tables unchanged; location per §2 | V4-EXM-21; C U-C5 | PC-12 |
| H-4 No alternate mutation route | V4-HI-20 (SETTLED) | PC-14 |
| H-5 No invented domain truth; references kept | V4-HI-71; V4-CST-05 | PC-15 |
| H-6 Agent reads show the same views and standing marks | V4-HI-10; V4-PAR-03 | PC-02 |

SWBPIPE (SQ-22; I2 22.1): its views show old and new values per field
(Batch review, Operation ledger, Diff preview), but offer no stable external
reference to a position in them. Panel references to host view positions are
*not supplied* until one exists. This is an answer about SWBPIPE's current
state, not host evidence.

## 5. Acts, wording and lapse

| Act / event | Actor | Capture / recorder | Panel wording | Never inferred from |
|---|---|---|---|---|
| A2 apply (direct under grant) | Agent within an effective direct grant; host applies | Host (origin mark, undo) | "applied by agent under grant" (T16) | — |
| Undo (OP-C10) | Actor per its treatment | Host | "applied, then reversed by ⟨receipt⟩" (T17) | — |
| A1 propose → queued | Agent | Host | "queued" (T10) | Success |
| A5 accept (per item) | Person (D2b) | Host act facility; A9 as record shape | "accepted by Engineer A" (T11 item 1) | Success, queueing, receipt |
| A10 reject | Person | Host act facility | "rejected by Engineer A" (T11 item 2) | A host refusal |
| A11 withdraw | Proposer | Host | "withdrawn by ‹proposer›" | — |
| A2 apply (after acceptance) | Host | Host | "applied" + receipt (T12 RC-1) | Acceptance alone |
| A3 examine | Agent | Host / record | "examination findings" (T4) | — |
| A4 mark checked | Person (D2a) | Host act facility; A9 as record shape | "checked by Engineer A" + bound content (T2) | Findings, success, acceptance |
| A6 approve | Person (D2c) | Host act facility; A9 as record shape | "approved by ‹person›" | Agent output (V4-AUT-05) |
| A7 rely | Accountable professional (D2d) | Host act facility; A9 as record shape | Recorded act only | Other acts |
| Act-declined event | Person (A4/A6/A7/A12 not performed) | Host act facility | "declined ‹act› — ‹subject›" | — |
| Run-ended event | Loop or person stop | Loop | "run ended (‹cause›)" | — |
| A8 request | Agent | Loop/record | "‹act› requested by agent", only when issued | Performance; automatic creation |
| A12 set grant | Person (D2e) | Host | "grant set by Engineer A" (T15, ⟨set-2⟩); "superseded by ‹act›" only for an established later A12; "refused by control: ‹reason›" | An agent request |
| A12 network-destination grant, and its decline (R8-13; ACT §2.7; LOOP §9; row added at v0.7) | Person | Host control | As §3.8 ND-1…ND-3 define: the grant with its scope (once · this run · always) and its source; a decline reads "destination not allowed by the person" and is an act-declined event of kind A12. No other wording is chosen (§0) | An agent's request (A8), an agent-written list entry, a timeout or silence |
| A13 external access | Person. Enable: D2e (SETTLED). Disable: INTEGRATION (R2-3) | Host/App | "external access enabled/disabled by ‹person›" | An agent request |

Rules:

- W-1. Proposal decisions say **accept**, never approve (V4-HI-33). The word
  "approval" is used only for A6.
- W-2. **Record presentation.**
  - For any recorded act, the panel shows the **actor** (the person), the
    **recorder**, the **recording mode** (direct capture or faithful
    recording) and the **capture-evidence reference** (V4-HI-31; ACT §2.4).
  - A record without capture evidence is shown as "record without capture
    evidence". It has no act standing and clears nothing (W-5c).
  - Unperformed acts are never presented.
  - A host capture requirement per act kind is DEP-001.
- W-3. **Content binding and lapse.**
  - Binding: A5/A10 to the change-item content identity; A4/A6/A7 to the
    subject content identity; A12 to the setting content (PROPOSED).
  - Lapse is shown at any time after performance. A12 is superseded, not
    lapsed.
  - Stale after acceptance is not a lapse (R2-16).
- W-4. No act proves another. There is no acceptance-first rule
  (SoW REQ-003).
- W-5. Checkpoints are presented per §3.5.
- W-6. D2 reserved acts are SETTLED for App/shared contracts, and hosts have
  no classifier mode (D3). Still open: OI-021 additions and host adoption
  (DEP-001). Phase 1 changes none of this: reserved acts stand, and acts are
  shown only when performed (R8-1).
- W-7. **SWBPIPE displays (SQ-23; I2 23.1).** A stale batch message exists.
  Lapse wording is DESIGN only. Supersession (no grants) and
  accepted-then-stale (Apply is the acceptance) do not arise. There is no
  reversal marker. Term mapping: §3.7.

## 6. Reusable-component allocation account (OUT-002) and conditional OUT-004

| Candidate responsibility | Possible consumers | Repeated? | Agreement | Standing |
|---|---|---|---|---|
| Act, lapse and supersession presentation (actor, recorder, recording mode, capture evidence) | SWBPIPE host panel; App standing/act display (DEL-04-02 OUT-001) | Plausible | None | Proposed candidate |
| Grant display state and scope presentation, including policy default | SWBPIPE host panel; App autonomy display (DEL-04-02) | Plausible | None | Proposed candidate |
| Workflow identity, holding library and required-tool outcome presentation | SWBPIPE host panel; App workflow experience (DEL-02-02, later undertaking per D1) | Plausible | None | Proposed candidate (WD §9 map) |
| Proposal item-disposition presentation | SWBPIPE panel; later hosts (OI-005). The App has no host queue | Not established | None | Not proposed |
| Tool-activity presentation | SWBPIPE panel. The App presents Codex items natively (V4-ARC-05) | Not established | None | Not proposed |
| Conversation rendering | SWBPIPE panel. The App is Codex-native | Not established | None | Not proposed |

**OUT-004 conditional state.** No reusable panel component is selected,
agreed or implemented (SoW AC-006). v3 interface pieces (ARCH §3) are optional
reuse sources.

**Host construction boundary.** The following stay with the external host
owner (SoW CLM-001; HI §1):

- host panel assembly and layout;
- tables and views;
- domain construction;
- conversation persistence;
- treatment resolution;
- act capture.

| Open issue | Owner | Point of need | What it holds here |
|---|---|---|---|
| OI-013 | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Panel assembly; host/common construction boundary |
| OI-014 | App/shared contract owners | Before structural/production allocation | Whether any candidate becomes shared, and where |

## 7. Receiving case inventory (OUT-003)

All cases are **DESIGNED — UNEXECUTED**: no host candidate exists (DEP-001).
The sibling v0.3 elements were confirmed by V2; R4 elements follow
R4_RESOLUTIONS. A missing input is not a
pass (SoW VER-005).

Accounting states (IR1-B B-m5; mapping owned by C):

| State | Meaning |
|---|---|
| DEFINED | Corresponds to C *illustrative* |
| EXECUTED (test double) | Corresponds to C *test-double* |
| EXECUTED (candidate) | Corresponds to C *actual host*, with configuration and date (V4-EXM-01) |
| LIMITED | Executed with stated gaps |
| AWAITING INPUT | Waiting for a named input |
| HELD | Waiting for a named decision; never a pass |

**Checkpoint cases are two-part (R8-1, R8-2).** PC-03c, PC-19, PC-19b,
PC-20, PC-21…PC-21i and PC-24 give the **Phase-1 result** (recorded, not
enforced; §3.5) and the **governance-phase value** (retained). The
governance-phase value reads the fixture's checkpoints as if declared
governed; no FX-PIPE-01 fixture declares the flag (R8-11 item 5). "Both
phases" means the display rule is the same in each, with dispositions as
record labels in Phase 1.

| Case | Interaction | Stimulus (FX-PIPE-01) | Expected result | Inputs needed | Serves |
|---|---|---|---|---|---|
| PC-01 | Conversation | T3 agent reads OP-C1 for R-100 | Reply references host rows S-1…S-4; basis B1 and standing as given | C, LOOP, host views | VER-001/002 |
| PC-02 | Conversation | Agent reads OP-C2 LC-1 results at r13 after T6 | Shown historical, never current (V4-HI-12) | C, host | VER-002 |
| PC-03 | Conversation | Loop rejects a truncated call (LOOP MC-1) | "Rejected before host validation: truncated" | LOOP, DEP-05-01-024 | VER-001 |
| PC-03b | Conversation | Setting "cloud chosen, no credential" (no key and no sign-in) | Indicator; "model request refused at boundary"; no credential content | LOOP §5, host | VER-001 |
| PC-03e | Conversation | Settings in turn: "cloud chosen, signed in (OAuth)"; then "unconfigured" (R8-9) | Signed-in state shown with no credential content. Unconfigured is shown "no choice made", with no default applied and no request made | LOOP §5.1 (MS-02, MS-12), host | VER-001 |
| PC-03c | Conversation | Kind (a) checkpoint on an OP-C5 call (LOOP FX-C8) | **Phase 1:** the arrival is shown; the call is shown **dispatched**, not held, and may carry "continued past ‹checkpoint› before A4". **Governance phase:** "Held at checkpoint (not dispatched)", naming the checkpoint | LOOP | VER-001 |
| PC-03d | Conversation | Call to a name absent from the offered edition; separately, host returns *not exposed* for an OP-C2 variant | First: "rejected before host validation: not offered". Second: host outcome "not exposed on this surface" | LOOP, C, host | VER-001 |
| PC-04 | Workflow selection | `supports-adjust` (origin host, ⟨rev-3⟩), plus a local **`L-PANEL-1`**: a same-named workflow with origin *project*, carried unadapted into the host library. A second workflow is needed for the collision, and FX-PIPE-01 has one | Both shown with the full tuple. `L-PANEL-1` shows **holding library** = host library, beside origin *project*. The collision lists both. The selection binds to the chosen tuple; the holding library does not affect equality | WD, host library | VER-001 |
| PC-05 | Workflow selection | `supports-adjust` requires OP-C1 (*present*), OP-C4 (*present*) and OP-C2 (*present, currently unavailable* at T8); `L-PANEL-1` has *requirements undeclared* | The first workflow's requirement check **passes**, with a run-time hold on OP-C2 ("No current solve for LC-1 at this revision"). `L-PANEL-1` is selectable, "requirements undeclared — check not established" | WD, C, host | VER-001 |
| PC-05b | Workflow selection | Named exposure variant: OP-C4 not exposed on the embedded surface | Required reference *not exposed on this surface*; check does not pass; reason shown | WD, C | VER-001 |
| PC-06 | Proposal queue | T10 PR-2 queued: item 1 new support on R-100 (OP-C4); item 2 S-3 stiffness (OP-C5) | Items with old/new, objects, reason, origin (incl. seat role meaning, settings references) and item state in host tables. State derived. Negative variant: values only in the panel → fail | P, C, host | VER-002 |
| PC-07 | Proposal queue | T11: Engineer A accepts item 1, rejects item 2; T12 applies item 1 | "Accept" wording. Item 1 A5 then applied (RC-1) with **resulting objects** (new support identity). Item 2 rejected (A10, actor). State never stronger than items | P, host, actual acts | VER-002/003 |
| PC-07b | Proposal queue | Variant: Engineer A accepts both PR-2 items as one batch | One A5 listing two items, each item-bound; per-item lapse possible | P, DEL-04-03 | VER-003 |
| PC-08 | Proposal queue | T10 submission reports success | "Queued", not applied or accepted | P | VER-003 |
| PC-09 | Proposal queue | T7: PR-1 relies on B1 (r12); T6 edited S-3 (r13) | "Refused — stale" with B1 and B2. T9 PR-2 shown as the agent's **new** proposal with lineage to PR-1. No panel re-draft or retarget | P, C, host | VER-002 |
| PC-09b | Proposal queue | Variant: item 1 of PR-2 accepted, then S-3 edited before application | "Accepted by Engineer A — not applied: refused — stale (relied B2, current ‹B′›)". A5 not lapsed; state not "accepted" or "applied" (R2-16) | P, host | VER-002/003 |
| PC-10 | Proposal queue | T13: acknowledgment of T12 lost and unobservable | "Outcome unknown", reporter and last observed state | P, LOOP | VER-002 |
| PC-10b | Proposal queue | T13: resubmission of PR-2 with the same identity | Recorded outcome shown (item 1 applied, RC-1). Never "stale" because of its own effect (R2-13) | P, host | VER-002 |
| PC-11 | Proposal queue | Any proposal decision control | "Accept"; any "approve" fails | P, ACT | VER-003 |
| PC-12 | Checks | T4: agent examines spacing with OP-C3 | Findings reference rows and B1. Domain tables identical before and after. Labeled "examination findings", never "checked" | C, LOOP, host, U-C5 | VER-002/003 |
| PC-12b | Checks | T1 host checks at r12 | "Host checks passed: equilibrium, unit consistency", evaluated at r12; historical after T6 | C | VER-003 |
| PC-13 | Rejection | Agent result visible only in the panel | Fails H-1 | Host | VER-002 |
| PC-14 | Rejection | Panel control writes outside the host route | Fails H-4 | Host | VER-002 |
| PC-15 | Rejection | Panel shows a value the host store lacks | Fails H-5 | Host | VER-002 |
| PC-16 | Acts | Model text: "Engineer A checked S-2" | No act presented | LOOP, DEL-04-03 | VER-003 |
| PC-17 | Acts | Success, queueing or receipt only | No A4–A7 presented | P, ACT | VER-003 |
| PC-18 | Acts (positive) | T2: Engineer A marks S-2 checked via the host facility; also recorded by another recorder | Actor, recorder, recording mode, capture-evidence reference, bound ⟨S-2@r12⟩ | DEL-04-03, host capture, **actual act** (DEP-05-02-017) | VER-003 |
| PC-18b | Acts (negative) | An agent-authored record of that A4 with no capture evidence | "Record without capture evidence"; no standing; clears nothing | DEL-04-03 | VER-003 |
| PC-19 | Acts (positive) | Checkpoint A4 arriving at T16 on OP-C9's applied outcome (subject S-4); T16a: Engineer A marks S-4 checked, after the arrival, with no A5 anywhere | **Both phases:** *performed* by A4; no acceptance prerequisite; SP-6 holds | DEL-04-03, actual act | VER-003 |
| PC-19b | Acts (prior) | A checkpoint arriving at T4 on "objects a named output concerns" (OP-C3 findings on S-2); T2's A4 on S-2 predates it | **Both phases:** T2 shown "prior act on this subject, not counted" (SP-6). **Phase 1:** the arrival reads *waiting* ("act not yet recorded"); nothing is stopped. **Governance phase:** arrival waiting, run held | EXEC, DEL-04-03 | VER-003 |
| PC-20 | Lapse | T2/T6/T14 on S-2; and the FX-PIPE-01 T16a/T17 sequence (undo lapses the A4 on S-4) | **Both phases:** T2's A4 is unchanged after T6 and **lapsed** after T14. T16a's A4 is lapsed at T17. At a checkpoint, after run end: *lapsed*. **Phase 1:** at a live checkpoint, before resume "waiting — lapsed at ‹t›", after resume **"act lapsed at ‹t›"** (R8-12 item 1); gated outputs lapsed; **not re-held**. **Governance phase:** before resume, "waiting — lapsed at ‹t›"; after resume, "waiting — re-held, lapsed at ‹t› after resume", with the request re-issued for the whole scope | DEL-04-03, host, EXEC | VER-003 |
| PC-21 | Checkpoint | Declared A4 checkpoint, reached-when *applied* for PR-2, subject class "objects changed by a named outcome" | **Both phases:** reached at T12; subject = the new support from RC-1; purpose and scope shown; shown *performed* only on host-captured A4 on that content. **Phase 1:** shown as guidance; *waiting* reads "act not yet recorded"; the run is not shown stopped. **Governance phase:** the run holds until then | WD, DEL-02-03, LOOP | VER-003 |
| PC-21b | Checkpoint | The same run stopped before T12 | **Both phases:** *not reached* at run end | LOOP | VER-003 |
| PC-21c | Checkpoint | A6 checkpoint; Engineer A declines | **Both phases:** act-declined event; *resolved negatively*. **Phase 1:** declared path shown as guidance. **Governance phase:** declared path taken | WD, ACT | VER-003 |
| PC-21d | Checkpoint | PC-21 reached, then the run ended without the act; Engineer A marks S-5 checked afterwards | **Both phases:** *waiting* with the run-ended event. The later A4 is shown "after run end" against S-5, and the disposition is unchanged; the run is never resumed | LOOP, EXEC | VER-003 |
| PC-21g | Checkpoint | A new run of `supports-adjust` recording **continues ⟨run 12⟩** | **Both phases:** shown "continues ⟨run 12⟩". Checkpoints start *not reached*. PC-21d's post-end act is "prior act on this subject, not counted" at the new arrival | LOOP, EXEC, DEL-04-03 | VER-003 |
| PC-21h | Checkpoint | Kind (c) checkpoint on PR-2 queued (T10); an OP-C1 read already in flight is observed afterwards | **Phase 1:** arrival shown; the read may carry **"continued past ‹checkpoint› before A5"**; nothing is shown stopped (LOOP FX-C14). **Governance phase:** arrival *waiting*; the read is shown **action during hold** | LOOP §2.4.0, §2.4.4 | VER-003 |
| PC-21e | Checkpoint | A5 checkpoint, reached-when *PR-2 queued*; T11 | **Both phases:** *resolved negatively*, partial: item 1 accepted (WD §4.3.7) | WD, P | VER-003 |
| PC-21f | Checkpoint | C named variant **V-GR1** (R5-7): run of WD-EX E1d (`label-with-grant`; `CP-grant` A12; kind (a) before dispatch of OP-C9; declared content {P-03, *direct*, {FX-W1; {S-4}}}), branching from T14. The OP-C9 call on S-4 meets reached-when, `CP-grant` arrives at r15, and T15's A12 is captured after the arrival. Sub-variants: control refuses; pending; confirmation lost; later established A12 on an overlapping scope | **Phase 1:** the arrival is shown; the OP-C9 call is shown **dispatched, not held** (the host's treatment under ⟨set-1⟩ reports *not permitted*, FX-V3 shape; LOOP FX-C11). T15's established A12 is shown answering `CP-grant` (*performed*). Refused → "refused by control", earlier setting kept. Pending → *waiting*. Lost → *unknown*. Later established A12 → "superseded by ‹act›", still *performed*. No call is shown held. **Governance phase:** established → *performed*, and the held call is shown dispatched as T16. Refused → *waiting* "refused by control", earlier setting kept. Pending → *waiting*. Lost → *unknown*. Later established A12 → "superseded by ‹act›", still *performed* | ACT, AS, EXEC, C V-GR1 | VER-003 |
| PC-21i | Checkpoint | Main timeline order: T15's A12 captured before a `CP-grant` arrival | **Both phases:** T15 shown "prior act on this subject, not counted", though ⟨set-2⟩ is in force. **Phase 1:** the arrival reads "act not yet recorded"; nothing is held. **Governance phase:** the person is asked to perform A12 again before the run proceeds (owner-visible cost, U-E4; R5-7) | EXEC SP-6 | VER-003 |
| PC-22 | Autonomy | C T15: Engineer A performs A12 → **⟨set-2⟩**: class **P-03** (shared by OP-C4, OP-C5, OP-C9), grant value direct, scope {model/workspace FX-W1; object set {S-4}}; control confirms. Before T15, ⟨set-1⟩ (*effective (policy default)* propose) | Grant display per class and scope: *effective (person-set)*, direct, {FX-W1; {S-4}}. T16 OP-C9 on S-4 applied directly with origin and undo. An OP-C4 on R-100 is outside the scope and goes to the queue; a direct request is *not permitted*. OP-C5 on S-4 is held on U-02, so no expectation is set | P, ACT, DEL-04-02, host | VER-003 |
| PC-23 | Policy-dependent | Operation-specific reserved addition for the first connected operation | **HELD** `UNRESOLVED{OI-021}` | Owner decision | VER-003 |
| PC-24 | Checkpoint vs grant | A5 checkpoint on OP-C4's result; grant effective direct; agent requests direct | **Phase 1** (R8-11 item 2 as restated by R9-2; LOOP FX-C9): no constraint is carried as enforcement; the host outcome under the person's effective direct grant is shown as reported (a direct application, if the host applies it, with origin and undo route); the A5 checkpoint is shown as guidance, and it is not reached if nothing is queued. Its act is still requested; no A5 is forced, and none is shown; the checkpoint shows no act performed unless the person performs it (R9-2; the disposition wording is LOOP G-9, an R10 candidate). DEFINED. **Governance phase:** *not permitted*, naming the governing checkpoint constraint; no silent proposal. **AWAITING INPUT** (R2-12; host constraint handling, §8 Q-1) — SQ-02 answered 2026-09-28: no host loop and no host-held evaluation; route (iv) (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3) | P, ACT, host | VER-003 |
| PC-25 | Grant | Agent requests widening OP-C4; separately, Engineer A sets a change not yet confirmed | "Agent requests …" (A8), grant unchanged; "Set by you — not yet in force"; neither enables direct | DEL-04-02, host | VER-003 |
| PC-26 | Proposal queue | Tg: restore to g2 after a proposal citing B1 | Refusal with both bases; meaning per U-C2 | C, P, host | VER-002 |
| PC-27 | Reserved operation | Agent calls OP-C6 on S-2 | *Not permitted*, naming reserved class and policy record; A8 offered, shown only if issued; no A4 | C, ACT, host | VER-003 |
| PC-28 | No policy basis | Agent requests OP-C11 direct; Engineer A attempts A12 widening it | *Not permitted* "no policy basis (pending OI-021)". Proposal possible, with no effect until A5 and application. A12 shown *refused — no policy basis*. **HELD** (R2-9) | ACT, DEL-04-02 | VER-003 |
| PC-29 | Undo | T17: Engineer A undoes RC-2 via OP-C10 (governed by P-03, R3-4) | "Applied, then reversed by RC-3". T16a's A4 on S-4 is shown lapsed (⟨S-4⟩ changed, FXA-2) | P, host | VER-002 |
| PC-30 | Network destinations | Local chosen; web access off; MCP servers off, with named entry M-1 (stateless 2026-07-28); always-off items off (LOOP MS-15) | Allow list per ND-1: switches, named entry M-1, the model service "allowed by your model choice", always-off items off | LOOP §5.1.1, host control | VER-001 |
| PC-31 | Network destinations | The agent writes an allow-list entry, or its message claims a grant (LOOP MS-22) | No grant shown; list unchanged; at most "Agent requests ‹destination›" (A8) | LOOP, ACT §2.7 | VER-003 |
| PC-32 | Network destinations | In-work request for API destination A-1 while other calls run; the person grants **once** (LOOP MS-16) | Prompt per ND-2 with the three scopes and decline. Only the requesting call shown waiting, then dispatched. The grant is shown with scope once and is not added to the list. ND-4 shows the contact with "in-work grant: once" | LOOP, ACT §2.7, RS R15 | VER-001/003 |
| PC-33 | Network destinations | As PC-32, granted **for this run** (LOOP MS-17) | Grant shown in force for the run; gone after run end and in a continuing run | LOOP, AS §3 | VER-001 |
| PC-34 | Network destinations | As PC-32, granted **always** for the category "other APIs" (LOOP MS-18) | The category "other APIs" shown switched on in the allow list, with source "in-work" and its time | LOOP, AS §3 | VER-001 |
| PC-35 | Network destinations | As PC-32, the person declines (LOOP MS-19) | Call outcome "destination not allowed by the person"; nothing added; the decline shown apart from contacts | LOOP, RS R15 | VER-001/003 |
| PC-36 | Network destinations | Configured MCP server M-2 does not follow the stateless revision 2026-07-28; the agent asks for it (LOOP MS-20) | M-2 not offered on the list; the prompt offers no grant and shows "cannot be allowed: not stateless MCP (2026-07-28)" | LOOP NW-10 | VER-001 |
| PC-37 | Network destinations | Cloud chosen, signed in. A turn contacts the model service, web destination W-1 (category on) and A-1 (in-work, always); unsandboxed M-1 declares D-1 (LOOP MS-12, MS-14, MS-18, MS-21) | ND-4 lists each with its category and allowing entry ("model choice", "category: web access", "in-work grant: always, ‹t›"); M-1 with declared D-1 and "process network not observed" | LOOP, RS R15, R11 | VER-001/002 |

Present state: every case is DEFINED or AWAITING INPUT, except PC-23 and PC-28
(HELD). PC-24's Phase-1 result is DEFINED; its governance-phase value is
AWAITING INPUT on host constraint evidence, with the STD-2 annotation.
PC-19b, PC-20, PC-21d, PC-21f, PC-21g and PC-21i rest on EXEC-v0.5 §4, which is
PROPOSED (W7). Their Phase-1 results rest on EXEC-v0.5 §2.1 (PH-6 and PH-8,
confirmed by R8-11 item 1). PC-30…PC-37 (R8-13) are DEFINED; no host
control exists to execute them (DEP-001). They present what V4-EXM-23, as
amended by SCA-V4-001, examines: destinations allowed in advance or when
the agent asked, a declined request reported as "destination not allowed by
the person", every destination contacted recorded and shown, and an
unsandboxed outside process within its stated limit. LOOP-v0.7 adds the
disallowed-destination case MS-23; its panel display is ND-4's "boundary
refusals, shown apart from contacts", and no PC case is added for it in
Wave A.

## 8. Concrete questions prepared for the external host owner

These are prepared for App-manager preparation and human relay (SoW CLM-005;
DEP-05-02-018). Writing them is not delivery, agreement or adoption. W9 owns
the relay file. They are shared with LOOP-v0.7 §13 where marked. RELAY-v0.2
§3 (kept as relayed in RELAY-v0.3 §3; answered, RELAY §4) relays them as SQ-02, SQ-01, SQ-22, SQ-23/SQ-10, SQ-21, SQ-18 (a),
SQ-24, SQ-05 (c)/(e) and SQ-20 (Q-1…Q-9 in order).

**Standing: answered (R8-7).** The questions were relayed and answered on
2026-09-28 (`RELAY_ANSWERS_SWBPIPE.md`, delivered sha256 `6f01add3…61c7`;
current bytes `afb6e063…0e74` after SWBPIPE's own revision, header;
RELAY §4). The answers describe SWBPIPE's current state. They are not
commitments, delivery, adoption or host evidence (DECISION-3), and host
joins are deferred. The questions below are kept as prepared. Gists:

- Q-1 (SQ-02): route (iv), none planned. There is no host loop or host-held
  evaluation. Governance-phase input only (R8-2).
- Q-2 (SQ-01): no capture-evidence reference. Only Apply is captured; its
  receipt names no person or time and does not survive restart.
- Q-3 (SQ-22): old and new values per field in Batch review, Operation
  ledger and Diff preview; no stable external reference (§4 note).
- Q-4 (SQ-23, SQ-10): a stale batch message exists; lapse wording is DESIGN;
  supersession and accepted-then-stale do not arise; no reversal marker;
  undo is a session snapshot with no receipt (§5 W-7).
- Q-5 (SQ-21): no.
- Q-6 (SQ-18 (a)): no host workflows.
- Q-7 (SQ-24): no findings storage on main; agent cards are DESIGN; whether
  storing a finding is a change is not decided.
- Q-8 (SQ-05 (c), (e)): no named reserved list and no grant states; every
  change requires Apply (§3.7 PN-5).
- Q-9 (SQ-20): not decided. The recorded direction predates D-20 (§1 note;
  R8-8).

- **Q-1** (LOOP Q-1; R2-12). Does your route receive and honour a
  per-request governing checkpoint constraint? Or does it evaluate its own
  copy of the declaration? How would the panel see which?
- **Q-2** (LOOP Q-2; R2-20). For A4, A5, A10, A12 (and A6/A7 where
  offered), and for act-declined events, does your act facility expose a
  stable capture-evidence reference, citing act identity, actor, kind, bound
  content identity and time?
- **Q-3.** Which host views show proposed change items with old and new
  values? How does the panel reference a position in them?
- **Q-4.** How does the host show lapse, supersession (A12), stale after
  acceptance, and "applied, then reversed"?
- **Q-5** (LOOP Q-5; R2-2). Does the host offer any faithful-record
  operation? Does it meet the four R2-2 conditions?
- **Q-6.** Which host workflows exist? How does the host show identity,
  derived-from and holding library?
- **Q-7.** Does the host hold agent examination findings, and does storing
  them count as a change (C U-C5)?
- **Q-8.** Which reserved-act list does the host name and enforce (V4-HI-30;
  D2)? How does it present the grant states, including *effective (policy
  default)* and *refused — no policy basis*?
- **Q-9.** What conversation persistence and panel assembly are intended
  (OI-013)? This question is informational.

## Findings

- F-1 (retained). One executor drafted both LOOP and PANEL, and the same
  executor revised both at v0.6. IR1-C J3 found no hidden divergence at
  v0.2. The v0.6 pair needs the same independent check. The v0.7 alignment
  edits to the pair were again made by one executor (A1-D), so the same
  holds for v0.7.
- F-2 (closed at v0.2; retained for trace). Required-tool vocabulary is
  consumed from DEL-02-01. A DEL-02-03 checker matters only under OI-014.
- F-3 (closed at v0.7 by SCA-V4-001 and the register update; R9-8). §3.6
  consumes DEL-04-02. At v0.6 DEL-04-02 was not in this SoW's CLM-002 or
  register (V1-C RF-4; V1-A RF-05). The revised SoW names it in CLM-002
  ("`DEL-04-02` supplies autonomy-grant display states and active scope")
  and REQ-006 (owner item O-11), and the register row is DEP-05-02-019.
- F-4 (closed at v0.7 by SCA-V4-001; R9-8). OQ-11 and OI-021 are the same
  matter: the revised SoW's P/OQ-11 paragraph says "tracked as OI-021", and
  the register row is DEP-05-02-016.
- F-5 (closed at v0.7 by SCA-V4-001; R9-8; the dependence itself stands,
  R2-20). The panel depends on a host capture-evidence reference (Q-2).
  The revised SoW's TBD-003 names it ("a stable capture-evidence reference
  for each host-captured act (RELAY SQ-01)"), under the DEP-001 row
  DEP-05-02-011.
- F-6 (new). The R2-4 wording "not exposed … reported by the host" means a
  host-returned *not exposed* is shown as a host outcome, while a name the
  loop never offered shows as a pre-validation rejection. IR1C-11 had
  proposed a loop-reported class-1 *not exposed*. R2-4 governs, and this file
  follows R2-4.
- F-7 (closed by R5-7). A12-at-checkpoint cases use C named variant V-GR1.
- F-8 (retained; v0.6 disposition). The host panel's hold-support display
  depends on the host loop's actual hold behaviour. Host evidence is
  DEP-001, and the related App-side question is SQ-02/D6. v0.6: the display
  is governance phase only (R8-1). SQ-02 is answered (route (iv)), and D6 is
  closed for Phase 1 (R8-2).
- F-9 (closed at v0.7 by SCA-V4-001; R9-8). PANEL's basis cites V4-HOST-01.
  At v0.6 its "by default … API key" wording had been revised by DECISION-4
  D4-3 but not yet in the accepted text. V4-HOST-01 now reads "There is no
  default between them; they are options the person chooses among", which
  is what the model setting indicator (§3.1) shows.
- F-10 (new, v0.6; lapse label ruled by R8-12 item 1). The Phase-1 display
  words ("act not yet recorded", "continued past ‹checkpoint› before ‹act›")
  are this file's application of EXEC PH-6…PH-8. The lapse label at a live
  checkpoint after the resume point was "waiting — lapsed at ‹t›" at A4; the
  integrator ruled it **"act lapsed at ‹t›"** (nothing says *waiting*;
  nothing re-held), now used in W-5e and PC-20. Before resume the label
  stays "waiting — lapsed at ‹t›". No UI wording or layout is chosen (§0).
- F-11 (new; R8-13). §1's "no separate routine tool-permission prompts in
  the panel" still holds beside §3.8. The in-work destination prompt
  presents an agent's A8 for the person's A12 network-destination grant
  (ACT §2.7), not a tool permission. Only the requesting call waits (LOOP
  NW-12); this is not a checkpoint hold, so Phase 1's "nothing holds"
  (§3.5) is unaffected.
- F-12 (new, v0.7; survey S1-D; returned to the owner). §3.8, PC-30…PC-37
  and F-11 define the panel's network-destination surfaces. DEL-05-02's
  ScopeOfWork does not name them (§3.8, "Standing against this
  deliverable's ScopeOfWork"). The choice is the owner's: a later
  ScopeOfWork amendment gives DEL-05-02 the display of destinations, or
  §3.8 stays as PANEL's receiving of DEL-05-01's "recorded and shown"
  obligation with the ScopeOfWork unchanged. Nothing is changed here.
- F-13 (new, v0.7; R9-6). DEP-05-01-020 asks this deliverable for the
  panel receiving needs at the loop boundary. This file does not yet state
  them as a list (header, Receivers). Returned as a Wave B item.

## UNRESOLVED

| Item | Owner | Point of need | Effect |
|---|---|---|---|
| OI-013 panel assembly, host/common boundary, persistence | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Behaviour only |
| OI-014 shared placement | App/shared contract owners | Before structural/production allocation | §6 candidates unagreed; OUT-004 conditional |
| OI-021 / OQ-11 first connected activity; operation-specific reserved additions; OP-C11 class | Owner via outside SWB session and App/shared owner (OQ-11: App manager, human and external SWBPIPE owner) | Before connected-activity SoW and execution / live examination | PC-23, PC-28 HELD |
| DEP-001 host panel/views, act capture (Q-2), constraint handling (Q-1), treatment, list adoption | SWBPIPE outside implementation session. Q-1…Q-9 answered 2026-09-28 (§8); SWBPIPE owner decisions listed in ANS §2 remain open | Before corresponding integration/examination and fallback-replacement decision; when the owner resumes UI-SUCCESSOR (DECISION-3) | All PC unexecuted. PC-24's governance-phase value AWAITING INPUT (STD-2 annotation); its Phase-1 result DEFINED. Q-2 answered (SQ-01): no reference, so no host-content checkpoint can show *performed* on SWBPIPE (W-5c) |
| DEP-05-02-017 actual human acts for positive cases | Person performing the act | When PC-07, PC-18, PC-19 and PC-21 execute | Defined only |
| C U-C5 findings location | DEL-03-01 with host owner | Before PC-12 execution | P-1/H-3 apply to referenced rows |
| Hold machine confirmation (EXEC-v0.5 §4, PROPOSED (W7)): re-hold, no resumption, SP-6, refused A12, MX rules | DEL-02-03, at the next integration review | Before dependent panel implementation | W-5b/c/e/f/g follow it as proposed. Its hold content is governance phase (R8-1); Phase 1 uses its recording content |
| U-E4 alternative to SP-6 (counting prior acts) | Owner | Before hold-machine implementation | W-5c follows SP-6. Owner-visible cost (governance phase): PC-21i (repeat an A12 already in force; R5-7). In Phase 1 nothing is held |
| U-03 multi-row A4 purpose after partial lapse | DEL-04-01 with Owner | At its point of need | W-5e requests the whole scope |
| D6 App-side run holds | The owner (DECISION-4): closed for Phase 1; re-opens with the governance phase (R8-2). SWBPIPE answered SQ-02 on 2026-09-28: route (iv), none planned | When the governance phase is taken up; before App-side hold implementation | The panel never claims an App hold. Phase 1: no hold anywhere (§3.5) |
| CLOSED at v0.7 (SCA-V4-001, accepted 2026-09-29; R9-8) — V4-WF-05 and V4-HI-42 now state the phasing themselves: the hold is phased to the governance layer; the request and the record clauses are in force (R8-1; R9-1; DECISION-4 D4-1) | Owner | — | §3.2 and §3.5 cite the amended texts; hold displays are governance phase |
| Who requests the act at a checkpoint in the current phase (R9-1, INTEGRATION) | Owner, for confirmation in the decision package of run `APP-V4-DESIGN-PASS-2-20260930` | Before the first-increment design is relied on | W-5a states the integrator's reading: the agent carrying out the workflow asks, and the panel shows the request when issued |
| Scope of §3.8 against DEL-05-02's ScopeOfWork (F-12) | Owner | When DEL-05-02's ScopeOfWork is next amended, or at the phase review | §3.8 stands as PANEL's receiving of DEL-05-01's surfaces; no ScopeOfWork changed |
| Governance phase taken up (R8-1) | Owner, per workflow that needs it (DECISION-4 D4-1) | When a workflow needs enforced checkpoints | The §3.2 hold-support display and the governance-phase parts of §3.5 apply to governed checkpoints only then |
| CLOSED at v0.7 (SCA-V4-001; R9-8) — V4-HOST-01 now states no default and OAuth sign-in or an API key (DECISION-4 D4-3; R8-9) | Owner | — | §3.1 indicator cites the amended text (F-9, closed) |
| CLOSED at v0.7 (SCA-V4-001; R9-8) — the revised V4-HOST-02 (DECISION-5; R8-13) is the accepted text | Owner | — | §3.1 and §3.8 cite it (P/docs/PRD.md `bb6e786f…49bd`) |
| CLOSED — DECISION-5 points settled by the owner's DECISION-5 confirmation (2026-09-28: the "MCP V2" reading confirmed; the person-only grant not objected to and stands): the person-only grant (point 3); the reading of "MCP V2" as the stateless MCP revision 2026-07-28 | Owner | Before §3.8 is relied on for implementation | ND-1 and ND-2 applied as recorded |
| LOOP N-OPEN-4 (category switch and named entries; an open owner question, not ruled: LOOP NW-8) and N-OPEN-5 (stateless MCP evidence) | As LOOP UNRESOLVED | Before PC-30, PC-34 and PC-36 execute | ND-1 shows switches and entries separately; unevidenced MCP servers are not offered (PROPOSED) |
| SWBPIPE embedded direction predates D-20 (R8-8; DECISION-4 D4-2) | SWBPIPE (its to act on) | When the owner resumes UI-SUCCESSOR | None on this contract; note in §1 |
| Grant display for a host without grants (R8-10; §3.7 PN-5) | Integrator | When host joins resume | PROPOSED; may be deferred |
| Host evidence that application re-checks the basis (P U-P3, narrowed) | Host owner (DEP-001) | Before PC-09b execution | Display defined |
| Which party evaluates required-tool outcomes in the host | Host owner; DEL-02-03 only under OI-014 | Before PC-05 execution | Vocabulary consumed. SWBPIPE: not decided (SQ-17 (c), SQ-20) |
| CLOSED at v0.7 (SCA-V4-001 and the register update; R9-8) — DEL-04-02 consumption (F-3) | — | — | SoW CLM-002 and REQ-006 name DEL-04-02; register row DEP-05-02-019 |
| Consequence vocabulary | DEL-04-01 with host policy owner | Before class assignment | Classes as supplied |
| R2-n sibling v0.3 elements | — | — | **Confirmed by V2**. T15 re-pointed per R4-18 |
| (closed, R6-4) Sibling elements pending | — | — | V-GR1 (C-v0.5) and the R5-1 values (EXEC-v0.3) are present at `c7f5513db`. No pending sibling element remains |

## Verification cases

These are designed, not run.

| Case | Procedure | Expected | Serves |
|---|---|---|---|
| VC-01 | Trace §3.1–§3.6 and §3.8 (R8-13; to LOOP §5.1.1, V4-HOST-02 as amended and DECISION-5; its standing against the ScopeOfWork is F-12) to V4-HOST-04/SOW-019 and to the consumed definitions (at their Wave A labels C-v0.7, P-v0.7, WD-v0.7, ACT-POLICY-v0.7 and AS-v0.7, with EXEC-v0.5 and LOOP-v0.7; plus R2-n) | All four interactions, plus checkpoints and grant. Consumed definitions named with versions; missing inputs visible | VER-001 |
| VC-02 | Review §2, §4 and PC-06/09/09b/10/10b/12–15/26/29 against V4-HI-10–25 and V4-EXM-20/21. On a candidate, observe them | H-1…H-6 each have a positive or rejection case. Stale-after-accept, resubmission and undo displays hold | VER-002 |
| VC-03 | Review §3.2 (checkpoints as guidance; hold support), §3.3–§3.7, §5 and PC-03c/07/07b/08/11/12b/16–25/27/28 against HI, AUT, D2/D3, ACT/AS, EXEC-v0.5 §2.1/§2.2/§3.6/§4 with R5-1/R6-1/R8-1/R8-2/R9-1/R9-2, and LOOP-v0.7 §2.4.0 | **Phase 1:** checkpoints shown as guidance; the agent's request for the required act shown when issued, and none shown that was not issued (W-5a); no hold-support value, held call or stopped run shown; no *unsupported* for a hold reason; "continued past" only as an optional annotation; acts shown only when performed; reserved acts stand; invalid declarations a finding only. **Both phases:** "Accept" wording; actor, recorder and capture evidence; act-declined vs run-ended; SP-6 "prior act not counted"; "after run end" and continuation; MX rules; A12 supersedes only when established; declared A12 setting binds; no-policy-basis HELD. **Governance phase:** re-hold after resume and after the person's undo; hold support in the four R5-1 values; values read as if governed | VER-003 |
| VC-04 | Compare §6 with the anticipated artifacts, the Clarification, V4-ARC-20 and OI-013/014 | Candidates name consumers or "not established"; none agreed; host construction external | VER-004 |
| VC-05 | Account for PC-01…PC-37 (including sub-cases) in the §7 states | One state each; no missing input counted as a pass | VER-005 |
| VC-06 | Inspect OUT-004 | Conditional; no component | VER-006 |
| VC-07 | Review SoW REQ-006 exclusions against §3 "Responsible", §6 and §8 | Each act kept with its owner; nothing performed or claimed here | VER-007 |
