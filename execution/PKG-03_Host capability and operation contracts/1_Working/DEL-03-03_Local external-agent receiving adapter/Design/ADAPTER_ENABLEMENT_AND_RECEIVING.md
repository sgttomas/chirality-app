# Adapter enablement and receiving
- Contribution: DEL-03-03/ADAPTER-v0.4. It supersedes ADAPTER-v0.3 (last changed at `c6f81a4f2` and unchanged at `94aa9181b`, file sha256 8ef2126df2b9afff0a70b36e5b4eed8492eaae0baf6563ce422d3b9d05170f5a), which superseded ADAPTER-v0.2 (sha256 a2905dda5782d7a48fa35ef7e26b0c1517fd3bd995e3ddbba27d2426a25674bc, 1,015 lines, committed at `cc58211c5`), which superseded ADAPTER-v0.1 (sha256 58b2409ca45ceea66160eb8910ca38b76b6f335dc184eaeb0896e93cabd0a074, 944 lines, `e20a3ae8d`).
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Phase (R8-1): in Phase 1 (this increment) declared workflow checkpoints are **plan guidance** (EXEC-v0.4 §2.1; WD-v0.6 §4.3.0). Neither the App nor a host's embedded loop holds a run on X. The governing checkpoint constraint, its carriage assurance (R2-12), hold support and *action during hold* are the **governance-phase definition (retained)**, stated beside a Phase-1 statement. V4-WF-05's first half is **phased to the governance layer, not withdrawn**, and is flagged for the next accepted-basis update. A13 stays a reserved act (R8-6). SWBPIPE's answers are recorded as answers about its current state, not commitments; host joins are deferred (DECISION-3)
- Serves: OUT-001 (meaning of the App-side native MCP/CLI configuration and of the receiving adapter "as needed" — definition only, no code), OUT-002 (machine-local enablement and operation-policy interface account; owner/act map; open-choice register), OUT-003 (designed, transport-neutral external consumer fixture inventory, labeled simulated); REQ-001…REQ-006; AC-001…AC-007; VER-001…VER-007
- Basis: branch base 6e18505e3; Wave-1 inputs at commit `ba0b37123`; ScopeOfWork.md sha256 5ac5db97eba3851eb5324054e5a2b38429a53e8e9c85428903432cd8d9efb1b6; `P/docs/HOST_INTEGRATION.md` (sha256 08c8fc7db2d74619ed47d184f44938bb06f1e2abda0a304a9e11b9230d0960da) §1, §2 (V4-HI-01…04), §3 (V4-HI-10…12), §4 (V4-HI-20…25), §5 (V4-HI-30…33), §6 (V4-HI-40…42), §7 (V4-HI-50…52), §11; `P/docs/PRD.md` (sha256 657593ce12a9a6da9f8b6c66579945499d909a8b6272d919d2d14a3db4538573) V4-HOST-02/03, V4-PAR-01…05, V4-AUT-03…05; `P/docs/ARCHITECTURE.md` (sha256 c3ae766ee2d660fb391b7db0aa99526f84d21421cf3a6b692ddd17e42687e533) V4-ARC-20/21; `P/docs/EXAMINATION.md` (sha256 1b156553dec7eb103dbb1166f5c0dbe9c719d26630d2fcace26c28b3ef54ee19) V4-EXM-23/24/25; SCC-CASE-002 `Case_Datasheet.md` (sha256 6acdc6c4e484ab7b46ba7d45a347961bc69b3e624bd29ef58a613ec6c66a71a6) rows M1-C, M1-P, M2-A; run `APP-V4-FIRST-INCREMENT-20260928`: `OWNER_DECISIONS.md` (Decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, sha256 f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e) D1–D4, `R1_RESOLUTIONS.md` (sha256 2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4), `R2_RESOLUTIONS.md` (sha256 77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088), `R3_RESOLUTIONS.md` (sha256 202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf), `BRIEFS.md` (sha256 58de4a2c48f651391383aecf85fa5e9073d2cc34240c37cdab216a16481c698f) "Common brief", "Owner rulings now in force", "Wave 2 — common additions", "W8"; **v0.2 additions** (read with `git show f05c7e4cd:<path>`): `R4_RESOLUTIONS.md` (sha256 50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24) R4-1, R4-2, R4-12…R4-17, R4-20 (binding; sweep A1) and `OWNER_DECISIONS.md` (sha256 a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c) with Decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` D5 (user flexibility) and D6 (deferred to the SWBPIPE answer); **v0.3 additions** (read with `git show 8fb51f07f:<path>`): `R5_RESOLUTIONS.md` (sha256 254d0b93b9959419a70c6737b07087e1db59b529adc3105a1db31f82b78dd6f1) R5-1, R5-2, R5-4, R5-5, R5-9, R5-10 (binding; final alignment pass), `reviews/V3-A.md` (sha256 f25f5af1177b7fe2a698bd4ef1e1caafa4c2ef25cfc73111f031e17c7cc21d87) m-11 and `reviews/V3-B.md` (sha256 5662fbd09025f5ad9459861370159d606fcced76b394980199e861555a1954a3) MAJOR-5, m-1, m-4, m-5, m-9 and Y-7
- Consumed inputs:
  - **R8-12 closing pass (node A6; in place, no version bump).** R8_RESOLUTIONS.md sha256 d4c3423310a857af86692d17ddfdd22fa877ee20b07c46e1ee481d1cd750e7af (R8-12: items 4–7 applied here). Current sibling versions after R8, as committed at `7a1508452` with A6's in-place R8-12 edits (their byte pins are in GUIDE-v0.3's input table): DEL-02-03/EXEC-v0.4; DEL-02-01/WD-v0.6; DEL-02-01/WD-EX-v0.6; DEL-03-01/C-v0.6; DEL-03-02/P-v0.6; DEL-03-04/GUIDE-v0.3; DEL-04-01/ACT-POLICY-v0.6; DEL-04-02/AS-v0.6; DEL-04-03/RS-v0.6; DEL-05-01/LOOP-v0.6; DEL-05-02/PANEL-v0.6; DEL-01-01/HOSTING-BOUNDARY-v0.6; DEL-01-01/PIN-SPIKE-v0.1; DEL-09-06/CA-v0.4; DEL-09-09/XT-v0.4; DEL-09-06/RELAY-v0.3. SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` and `FACTS_SQ01_SQ32.md` are unchanged (data about SWBPIPE's current state, not commitments; DECISION-3).
  - **v0.4 inputs (R8 pass, node A3, at `94aa9181b`).** R8_RESOLUTIONS.md sha256 1770c96e62caf14322811fca82ceb77eca450d3e1be8665cdbdd5550631e8d02 (R8-1…R8-11; binding); INTAKE_MAP.md (I2) sha256 3cc182955c0f3dd70efa0f1c051870229c2ccc08f36c5cf1445f2eef0dd1ea33: rows 01.9, 01.10, 01.14, 02.13, 03.9, 05.6, 06.1, 06.2, 07.8, 07.13, 08.2–08.4, 09.1, 10.3, 11.2, 12.1, 13.1, 13.2, 14.3, 15.1, 16.1, 25.2, 26.2, 28.2, X.6; Part 2 P2.10, P2.11, P2.15, P2.17, P2.18 and its §2.2 ADAPTER rows; Part 3 items 1, 2, 4, 6, 10–12; Part 4.4, 4.11; Part 5 R8-Q12 (R8 overrides I2 where they differ); BRIEFS.md sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517 ("Common rules", "A-wave"); owner decisions DECISION-3 and DECISION-4 with its clarification (OWNER_DECISIONS.md sha256 a5ccab0d39bd1cab37c5556abc9bdedd5341ce76be4712706c8c9d72d623e776); SWBPIPE's delivered answers `RELAY_ANSWERS_SWBPIPE.md` (DEL-09-06 `Design/`, #1047) sha256 6f01add3977761e42ac6b310faf72ba4fd5455e478605deb83fefb2e4d3a61c7: SQ-01…SQ-16, SQ-26, SQ-28, SQ-31, ANS §0, §2–§4 — data about SWBPIPE's current state, not commitments (DECISION-3). **Owner files read first (at `94aa9181b`):** DEL-02-03 EXEC-v0.4 `EXECUTION_COMPATIBILITY.md` sha256 d32be37797a3c367d342a2d13bbb8dd4279bc52934531d83b8c6ec8c6e7b76d4 (§2.1 PH-1…PH-10; §2.2 GV-1…GV-5; §2.3 HP-H; §3.5; §3.6 with R8-2; §3.7 CC-2; MT-14; CH-27; U-E1, U-E13, U-E23); DEL-02-01 WD-v0.6 `WORKFLOW_DECLARATION.md` sha256 fce565edfd0cee3fa4583eb292d11cce3e4121ead0cdbed31ba2fe0a52562f28 (§4.3.0 CG-1…CG-7; §4.3.1 `governed`, PROPOSED); WD-EX-v0.6 `EXAMPLES.md` sha256 950b70b2e3f7fdda9a98b13a63746b76936be490dd96cb6e47bbe6dc9c3eba3d (E8; R-5a/R-5b). DEL-03-01/C-v0.6 and DEL-03-02/P-v0.6 are revised in the same pass (node A3); body citations of C and P now point to them (identifiers unchanged). Other siblings keep the versions cited below.
  - Earlier inputs (Wave-1 texts read with `git show ba0b37123:<path>`; they remain at v0.3 bytes here. Where R4 rules a change to them, this file follows the R4 text, not v0.4 bytes, which were not available when this revision was made):
  - DEL-03-01/C-v0.3 `CATALOG_AND_READ_BASIS.md` (sha256 ba45e7393ee0b16780f36605ddeecb95ba1f181488e36a46b4b495b69fd67c26): §2–§8, §10 FX-PIPE-01;
  - DEL-03-02/P-v0.3 `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` (sha256 ec0db87f239bc42e2e3e953d660ce3c4ceddf605d7b98cf1393f97a099b699cf): §2–§11, §13;
  - DEL-04-01/ACT-POLICY-v0.3 `ACT_AND_POLICY_CONTRACT.md` (sha256 b3748c02006f939d8cc78c6e0b0c847598a8b32d55515ae8658ad80597c98128): §2.1, §4, §5.3–§5.6, §6, §8.3, §10 V-10, §13 FX-24/25/42;
  - DEL-04-02/AS-v0.3 `AUTONOMY_AND_STANDING_EXCHANGE.md` (sha256 7b634137bb8402f3eaedc943dab0c5f1114b9d4433d2b94e13540ac0bf8e0514): §2, §3, §7;
  - DEL-01-01/HOSTING-BOUNDARY-v0.3 `HOSTING_BOUNDARY.md` (sha256 34c3383402aabe6e9347aa2f111318538c4a2a4ca85adb8fffff7e439fdde94e): §1–§3, §6, §8.2; DEL-01-01/PIN-SPIKE-v0.1 `PIN_SPIKE_0.158.0.md` (sha256 0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115) §4–§6;
  - DEL-01-01 generated bundles at pin 0.158.0, read-only: `Design/generated/0.158.0/json-schema/experimental/codex_app_server_protocol.schemas.json` (sha256 aa5cb3fbcdebf833515fb42cd085a0670eb755d461037a0ad67bb72a709dcd0f), `…/codex_app_server_protocol.v2.schemas.json` (sha256 34f28a486d00fbd20e5da0b0da3422d1d6e20ec897d12b31408f87499198f458) and `_spike/inventory.txt`;
  - for joins only: DEL-02-01/WD-v0.3 `WORKFLOW_DECLARATION.md` (sha256 84841d9f539767b9ff7ae225fec27f0dc4ebbd2c161c41aff179bbae97f345eb) §4.2, §4.3.4–§4.3.6; DEL-05-01/LOOP-v0.3 `LOOP_RECEIVING_CONTRACT.md` (sha256 6b771c8027787193d536fa3507214a8cc579d6ec2f476ee880609c920b6f25c7) §1, §6, §13; DEL-04-03/RS-v0.3 `RECORD_SEMANTICS.md` (sha256 925f35ca27bd7d1e71a375883ada9903267408af57312eed1ae02b47776a3528) R5, R7, R11, R13;
  - **v0.3 current sibling texts** (read with `git show 8fb51f07f:<path>`; every body citation of a sibling now points to these versions — R5-9): DEL-03-01/C-v0.4 (sha256 e929d39d3ff9515702f9bfe51dfada537e1cbd165146ec0de4ccf629c659a08c: §4.1, §10.1 FXA-1…FXA-5, §10.4); DEL-03-02/P-v0.4 (sha256 0d3960a2e6bd3520368006cdd2b1b67a1fe4eb06e23184aded9d5b98d6c5e361: §3.3, §4.4, §9); DEL-04-01/ACT-POLICY-v0.4 (sha256 d6da05abe790a4374df7faf225439a01dc1be734491b499d90cf00533369b03b: §2.6, §4.4, §4.6, §6, FX-24/25/42/47/50); DEL-04-02/AS-v0.4 (sha256 774728d03824397a5343412b17659feaf9b0d2ef1029b79889d13a1b421f4dab); DEL-04-03/RS-v0.4 (sha256 56806b64b12a946e706ff236dd1c25fe27ac00877aac13b50ee8603aaf540199: R5, R7, R11, R13); DEL-02-01/WD-v0.4 (sha256 e492ff635de972466c8a932355beeae848e1f3d3f60de7304e88963352d8e88e: §4.2, §4.3.8); DEL-05-01/LOOP-v0.4 (sha256 ffc3048333f3370ba09a9ce124159b94f2c80ce69b5f593bfb82cc552f95934e: §2.4.4, §6.2, §6.3); DEL-01-01/HOSTING-BOUNDARY-v0.4 (sha256 201ea32005dd2c9fb5281a376eb25eebfcb5a644d09a6d3bf5901aaf934c7e58: §6.7, §6.8, §8.3); DEL-02-03/EXEC-v0.2 (sha256 7f7848c0de2fdb4dc21f5adafa97f92e179bb66c9f6b04f3434d8f2342317af0: §2 HP-1…HP-4, HP-H, §3.6, §5 CAP-1…CAP-9); DEL-09-06/RELAY-v0.2 (sha256 48dc5a1f0a875089875b3866fd7bd7e21456520529e075de2a4a162372541f65: SQ-01…SQ-32, §3); DEL-09-09/XT-v0.2 (sha256 28ff092e114f386a723ea7f19d1a6e23a3963b92b44a1383d6308d0c111077c6). R5 moves the Wave-1 files to v0.5 and EXEC/RELAY/XT to v0.3 in parallel with this revision; those texts were **not read**. Where R5 rules what they will say (hold-support values, carriage assurance), this file follows the R5 text;
  - **v0.2 additions (history; superseded by the v0.3 list above):** DEL-02-03/EXEC-v0.1 `EXECUTION_COMPATIBILITY.md` (sha256 e0ede76ebf08003511755afc666be2466a867fd3256837ee94300cd0dfe518e8, `git show e20a3ae8d`) §2 hold points HP-1…HP-3, §3.6 hold support, §5 CAP-1…CAP-9; DEL-09-06/RELAY-v0.1 `RELAY_QUESTIONS_SWBPIPE.md` (sha256 3e34575def8d1fef63b5f5e64f0f90a0984d03b8b42f61fe899dd2eab023b2d1, `git show b4030fe4b`) SQ-01…SQ-27 and its §3 source-to-question map; DEL-09-09/XT-v0.1 `EXTERNAL_TRACE_CASES.md` (sha256 8f098c79f1da28af1b461210c36cca1124a25e226e802f2203b46ce7052df8cd, `git show b4030fe4b`) XC-01…XC-12, L-XT-2, L-XT-3, finding F-4; this file's own v0.1 (above);
  - evidence only, **not a commitment**: the description of draft PR #885 "Connect a private live-control CLI to reviewed Piping operations" (head `12907f393f5ead1badfac894502895684448c6e2`, state OPEN, draft), read with `gh pr view 885` on 2026-09-28;
  - SWBPIPE endpoint contract and host contributions: **not supplied** (DEP-03-03-010, DEP-03-03-011; DEP-001).
- Receivers: DEL-09-09 (CASE-002 M2-A: OUT-001; REQ-001, REQ-002, REQ-004, REQ-008; VER-001, VER-002, VER-004, VER-008) via DEP-03-03-012 / DEP-09-09-009; DEL-03-04 (guide row "Optional external catalog access"; CLM-002; REQ-008) via DEP-03-04-007 (no DOWNSTREAM mirror in this register — F-11). DEL-09-06 (RELAY SQ mapping, §12). By join, not registered here: DEL-03-01 and DEL-03-02 (receiving comparison of C/P meanings), DEL-04-01 (V-10), DEL-02-03 (external-path hold and required-tool check), DEL-04-03 (record entries R7/R9/R11/R13), DEL-01-01 (supplier surfaces).

**Reading note.** Every element name this file defines (for example
*channel state*, *native-tool mapping*, *carriage assurance*) is a
**semantic label, not a wire name**. Supplier method and field names appear
only as **observed supplier facts at pin 0.158.0**, with the DEL-01-01
standing labels `observed`, `observed-in-generated-types`,
`published-only` and `not-observed`. They are not Chirality wire choices.
Names from PR #885 are quoted as evidence from its description only.

This definition selects **no** transport (MCP versus CLI), wire field,
JSON/TS type, authentication scheme, hash or canonicalization algorithm,
persistence, process placement or shared-component placement (TBD-007;
OI-013; OI-014). §9 registers those choices and does not make them.

---

## 0. How to read this definition

Markings follow R1/R2: **SETTLED** (accepted basis or owner ruling, cited),
**DERIVED** (follows from cited rules), **INTEGRATION** (an R1/R2/R3
integrator choice, cited), **PROPOSED** (this contribution's proposal, open to
review). Owner rulings are credited only with what they say (R2-11).
Unruled policy appears as `UNRESOLVED{OI-nnn}` and is never a permission, a
default or a pass. **OI-003** here is the App v4 open issue (the extension
promise); it is unrelated to SWBPIPE's own OI-003 (R8-7; SQ-26). Notes marked
*SWBPIPE (SQ-nn)* record SWBPIPE's delivered answers as data about its
current state (FACT on main, or DRAFT #885: unmerged, not qualified,
deferred), never as commitments (DECISION-3). Fixture subjects come from FX-PIPE-01 (C-v0.6 §10); local
subjects are named `L-ADAPTER-n` with their reason (§10.1).

Settled distinctions relied on (cited, not re-decided):

| Id | Settled distinction | Source |
|---|---|---|
| S-X1 | A host may expose its catalog to an external agent, such as the App's Codex, as an MCP server or as a CLI over its live controller. Both are built from the catalog and apply the same validation, autonomy settings and reserved acts | V4-HI-50; V4-ARC-21 |
| S-X2 | External access is **off** unless the person enables it, and it is **local to the machine** | V4-HI-52 |
| S-X3 | An external agent cannot perform an act reserved to the person. The earlier SWBPIPE no-external-apply design is historical context, not a universal v4 ruling, and v4 does not amend the host's operative policy without its receiving adoption | V4-HI-51; SoW AX-001 |
| S-X4 | One route for every change; treatment resolved on the host route at validation and again at application; loop and adapter relay intent and do not decide treatment | V4-HI-20; R-3.1 (INTEGRATION); P §2 |
| S-X5 | Runtime non-success results are C §4.1's; proposal/operation outcomes are P §9's; both adopted unchanged | R-7; C §4.1; P §9 |
| S-X6 | Reserved to the person (D2, adopted): A4, A5 where autonomy requires a proposal, A6, A7, A12, **A13 enabling external access**. DERIVED: A10 wherever A5 is. INTEGRATION (R2-3): **disabling** external access is also A13 | D2; R-1; R2-3; ACT §2.1 |
| S-X7 | App routine tool-permission and sandbox modes are the user's own Codex setting (A14); they govern tool execution only and never stand in for a reserved or professional act. INTEGRATION (R-2): no App rule answers A14 affirmatively; A14 is recorded only in R13 (R2-8) | D3; R-2; R2-8; HOSTING H9, R7–R9 |
| S-X8 | Stock, unmodified Codex App Server, owned by the App process, full published protocol, native delivery, no veto of the user's Codex configuration, no pinning of approval or sandbox policy. Definition/generation pin 0.158.0, not a qualification | V4-ARC-01; HOSTING H1, H6, H9; D4; DEP-005 |
| S-X9 | Success means it ran; queued ≠ applied; a receipt is not acceptance; one act never implies another | V4-HI-25; #d3; P S-P7/S-P8 |
| S-X10 | Checkpoints override autonomy; an A5 checkpoint forces *propose* for the operation in that run and is carried as a governing checkpoint constraint {workflow run, checkpoint name, required act A5, operation}. **Phased (R8-1; R8-11 item 2):** this binds only for **governed** checkpoints in the governance phase. In Phase 1, WD I-7 and V4-HI-42 are guidance: the agent proposes as the plan expects, the App carries no constraint, and the host's own treatment decides. D2's reserved-act half binds in both phases, enforced by the host through its operations | V4-HI-42; R-5; R2-12; ACT §4.4; R8-11 |
| S-X11 | **Model destination (D5; R4-1; R5-4).** SETTLED by DECISION-2 D5: host content read by the App's Codex through the external channel may flow to the model the person selected for the App conversation, cloud included, and the App does not gate enablement, reads or submissions on the destination. **INTEGRATION (DECISION-2 reading; R4-1, R5-4)**, not SETTLED: the App records the destination per turn where the supplier reports it (requested and effective kept separate, reroutes included, unobserved turns *unknown*), the run-level value is the set observed, and the channel status shows it as information only. A host may restrict its own channel (DEP-001); SWBPIPE does not (SQ-16). V4-HOST-02 still governs the host's embedded agent | DECISION-2 D5; R4-1; R5-4; HOSTING §8.3 |
| S-X12 | **D6 closed for Phase 1 (DECISION-4; R8-2); governance phase retained.** *Phase 1:* checkpoints are plan guidance; the App holds nothing on X, assigns no hold-support value and reports nothing *unsupported* for a hold reason; a run action after an arrival and before its act may carry the optional annotation "continued past ‹checkpoint› before ‹act›" (EXEC PH-2, PH-3, PH-7). D6 re-opens only when the governance phase is taken up. SWBPIPE answered SQ-02 on 2026-09-28: route (iv), none planned. *Governance phase (retained; formerly "D6 deferred", DECISION-2; R4-2; R5-1):* how the App holds its own runs at governed checkpoints is `UNRESOLVED{D6}`. There: per-checkpoint *hold support* takes one of the four R5-1 values (§5.3); no App hold is claimed that cannot be enforced; *action during hold* is recorded; neither interposed App code (HP-1) nor reliance on `turn/interrupt` (HP-2) is adopted; HP-3 (named-rule decline of a tool-permission request) stays a permitted best effort under D3; HP-4 (the App initiates nothing for a holding run) is applied; HP-H (a host-side hold) is not offered by SWBPIPE (SQ-02 route (iv)) | DECISION-2 D6; DECISION-4 D4-1; R4-2; R5-1; R8-1; R8-2; EXEC §2.1–§2.3, §3.6 |
| S-X13 | **Carriage assurance (R4-14; final per R5-2) — governance phase (retained; R8-1).** *Host-held*: the constraint originates on the host side — from a declaration copy or run association the host holds, evaluated by the host route, or derived by the host loop from the resolved declaration it evaluates. A constraint the host **received** and then **verified against its own copy** of the declaration is host-held; a constraint the host merely **received** from an outside caller keeps its source's assurance: *model-supplied* or *App-assured*. *App-assured* is **not available in this increment** (R4-2: no interposed App code). **Only host-held carriage satisfies R2-12** | R4-14; R5-2 |

---

## 1. Parties and the owner/act map (REQ-005; AC-006; VER-006)

This contract performs no act owned by another party. The table lists every
act or production the SoW excludes, one for one, with its actual owner.

| Act or production | Owner | This contract's part |
|---|---|---|
| Catalog and read-basis contract meaning; shared fixture | App DEL-03-01 (CLM-002) | Consumed (C-v0.6) |
| Proposal, validation and outcome contract meaning | App DEL-03-02 (CLM-002) | Consumed (P-v0.6), including constraint carriage |
| Canonical act names, class records, treatment → outcome map | App DEL-04-01 | Consumed (V-10, V-02, V-03, V-05, V-09, V-14) |
| Grant display states and standing display | App DEL-04-02 | Consumed; supplies the external-channel facts it displays |
| Human-act and run-record format | App DEL-04-03 | Supplies external-dispatch entries (R7), act references (R9), evidence limits (R11), A14 facts (R13) |
| Workflow checkpoint declaration; hold machine; required-tool check | DEL-02-01 declares; DEL-02-03 (W7) records and checks (Phase 1) and, in the governance phase, holds | Phase 1: supplies external-channel observations and the optional "continued past" annotation (§7.7). Governance phase: per-checkpoint hold-support inputs and *action during hold* observations (§5.3, §7.7); App holds `UNRESOLVED{D6}`, closed for Phase 1 (R8-2) |
| Hosting boundary; server-request register; A14 answer origins | App DEL-01-01 (with DEL-01-04/01-05 in a later undertaking, D1) | Consumes supplier facts at the pin; answers nothing |
| Joined external-control witness; extension trace | App DEL-09-09 (CLM-003) | Receives this contribution and its fixture results; never claims the joined witness |
| Integrated host guide | App DEL-03-04 | Receives §§1–9 for its external-access row |
| Endpoint/server or CLI construction; catalog implementation; domain objects and truth; validation; application; receipts; host views; offering, capturing and presenting human acts; host enablement facility | External host owner — SWBPIPE outside session (CLM-001, CLM-003) | Requirements and relay questions only (§12); no host behavior assumed |
| A13 enabling or disabling external access | The person (D2e; R2-3); stays reserved (R8-6) | Consumes its evidence; the agent may only request it (A8). SWBPIPE has no enablement facility, so no A13 is evidenced there (SQ-28) |
| A4, A5, A6, A7, A10, A12 | The person; A7 the accountable professional | Consumes captured evidence; never records one without it |
| A14 answer tool permission | The person, or the user's own Codex mode | Observes the settlement; never answers |
| OI-001 / OI-002 rulings | The owner (DECISION-1 D2/D3) | Carried as adopted through DEL-04-01 P-01/P-04 |
| `OI-021` operation-specific additions; first connected operation | Owner via the outside SWB session and App/shared owner | `UNRESOLVED{OI-021}` |
| `OI-003` (App v4 OI-003) extension promise | Owner with host contract owner | `UNRESOLVED{OI-003}`; this file supplies evidence of adapter work only |
| `OI-013` / `OI-014` placement | Shared contract owner with SWB implementation owner / App-shared contract owners | `UNRESOLVED{OI-013}` / `UNRESOLVED{OI-014}` |
| MCP-versus-CLI selection, transport, authentication, wire schemas (TBD-007) | App external-host integration owner **with** external host owner | Registered in §9; not selected |
| Professional reliance, certification, sealing, code compliance | The accountable professional | Never inferred |

---

## 2. The receiving path in outline

```text
 the person ──A13──► host external-interface enablement (host-captured; §3)
     │                              │ off ⇒ "channel not enabled" (host-reported)
     │ App-side access configuration│ on
     ▼  (person-directed; §3.2)      ▼
 App's Codex (stock App Server, pin 0.158.0; App process owns it; HOSTING)
     │ native tool use by the model: an MCP tool call, or a CLI command run
     │ through Codex command execution — one of the §9 realization families
     │    ├─ A14 tool permission (user's own Codex setting) — App-side, R13 only
     ▼
 host catalog-derived endpoint (MCP server or CLI over the live controller)
     ▼
 host's one validation/application route  ──► C §4.1 / P §9 outcome, receipt
     ▼
 App observes the native item (arguments, result, status) and records R7/R9/R11
```

Two **realization families** exist; neither is selected (§9 OC-2):

- **Native (N).** The App's Codex reaches the host endpoint through its own
  native capability: a configured MCP server whose tools the model calls
  (N-MCP), or the host CLI run through Codex command execution (N-CLI). No
  App code sits on the dispatch path; the App configures (with the person),
  observes and records.
- **Interposed (I).** App code sits on the dispatch path and forwards to the
  host endpoint: App-registered dynamic tools (I-DT; `thread/start` field
  `dynamicTools` and server request `item/tool/call`, both
  `observed-in-generated-types`, `dynamicTools` **experimental-only** at the
  pin), or an App-side local MCP proxy the App's Codex is configured to use
  (I-PX).

**When an adapter is "needed" (PROPOSED; narrowed by R4-2).** The SoW asks
for a receiving adapter "as needed". The need is precise: App code on the
dispatch path would be needed for exactly those carried elements (§5) and
holds (§5.3) that must be **App-assured** and that the host cannot hold
itself. Under D6 (S-X12) **no interposed App code is adopted** in this
increment; the interposed families stay in the §9 register as unselected
options only. **Phase 1 (R8-1):** nothing is held, so no hold needs an
element, and no App code is needed on the dispatch path; the agent follows
checkpoints as plan guidance and never adds a field the host schema lacks
(R8-10). **Governance phase (retained):** every element that R2-12 or a hold
needs for a governed checkpoint is either **host-held** or **not met**. SQ-02
was answered on 2026-09-28 with no host-held carriage or host hold (route
(iv)), so against SWBPIPE the hold support is *not enforceable* (R5-1;
R8-2), the workflow is *unsupported* on X in that phase, and no App claim
covers the gap. The realization choice stays with TBD-007's owners.

---

## 3. Enablement account (REQ-002; AC-002; SOW-184)

### 3.1 Elements (semantic)

| Element | Meaning | Supplier / evidence |
|---|---|---|
| Host enablement record | The person's A13 (enable or disable) on the host's external interface on this machine, as captured by the host's facility, with a capture-evidence reference | The host's **enablement facility** (ACT-POLICY-v0.6 §2.6, PROPOSED under R4-13; relay **SQ-28**, which gates the whole external channel, R5-10). **SWBPIPE: none** (SQ-28, answered 2026-09-28: no facility and no plan found; no reference; state not readable; disable not captured; a SWBPIPE owner decision). Enablement *behavior* (default off, *channel not enabled*, state read, disable with queued proposals) is SQ-13 |
| App-side access configuration | Whether the App's Codex is configured to reach this host's endpoint (N-MCP server entry, N-CLI availability, or I-DT/I-PX registration), with its locus (§9 OC-3) and who directed it | App, at the person's direction (PROPOSED §3.3 E-4). An **ordinary configuration change**, recorded as such; never A13 and never A13 evidence (R4-13; ACT-POLICY-v0.6 §2.6) |
| Endpoint observation | Whether the endpoint is reachable and what it reports about itself, with the observer and time | Supplier facts (§3.5) and host responses |
| Operation-level outcome | Per entry: the C §4.1 / WD §4.2.4 outcome on the external surface X | Host (catalog, exposure element 9, availability) |
| Model destination | Per turn, where the supplier reports it: the destination **requested** (provider and model the person chose) and the destination the supplier reports as **effective**, kept separate, including any re-route; an unobserved turn is *unknown*. Run-level value: the **set** of destinations observed; a destination switch starts no new run. Plus the statement that the channel adds no other destination. **Information, not a gate** | Supplier facts per HOSTING-BOUNDARY-v0.6 §8.3; App records them (RS R5 model destination) and shows them in the channel status. No-gate: SETTLED (D5). Record-and-show: INTEGRATION (DECISION-2 reading; R4-1, R5-4) |
| Locality statement | The endpoint is on this machine (local process, local socket or loopback origin) | Host endpoint contract; App observation (§3.5) |

### 3.2 Channel states

The four brief states are **channel-level summary labels**. They never replace
the distinct outcome values of C §4.1, which every request still reports.

| Channel state | Condition | What a request gets | Reporter |
|---|---|---|---|
| **disabled** | No A13 enablement is in force: never enabled, disabled by A13, or host enablement not evidenced. Sub-cases: *App-side not configured*; *host reports off* | **channel not enabled**, naming "A13 not performed" (ACT §6 row 1). An App-originated or App-interposed request is **not sent** to the host | App, when its own configuration is off (**no host request**; R4-16); host, when a request reached it and the host channel is off |
| **enabled** | Host enablement record in force (A13 evidenced) **and** App-side access configuration present **and** endpoint reachable | Each operation's own outcome (C §4.1; P §9) | Host |
| **endpoint-unavailable** | Enabled, but the endpoint is not reachable, not started, failed, needs authentication, or its tool discovery failed | No operation outcome is inferred. A submission whose transport failed after sending is **outcome unknown** (§7.4); before sending, nothing was sent | App (from supplier or transport observation), naming the observed reason |
| **operation-unavailable** (situation label) | Enabled and reachable; a particular entry is not usable now | Exactly one of: **unavailable** (precondition; reason; evaluated basis) · **not exposed on this surface** (host-reported from element 9) · **missing** (no entry in the edition; discovery finding) · **version mismatch** · **not established** (mapping unresolvable, element 9 *unagreed*, catalog unreadable) · App-side **not offered** (interposed families only, §4.5) | Host for the first two; App for the rest, each naming itself |

A further qualifier, **enablement unconfirmed**, applies when the App cannot
observe the host enablement record (for example the host exposes no read of
it). It is treated as *disabled* for App-originated requests and shown as
"unconfirmed", never as *enabled* (DERIVED from S-X2 and HOSTING H8
"silence never grants"). Against SWBPIPE there is no host enablement record
at all (SQ-28), so the state is *disabled*, sub-case "host has no A13
facility", not *unconfirmed*.

**SWBPIPE enablement (R8-6; SQ-13, SQ-28; INTEGRATION).**

- SWBPIPE's opt-in (DRAFT #885) is a launch environment variable
  (`SWBPIPE_LIVE_CONTROL=1`) plus a build feature. It is not a person's
  captured act, there is no *channel not enabled* code, and the enablement
  state cannot be read. A13 stays a reserved act (R8-1), and it is never
  evidenced on SWBPIPE, so the channel stays *disabled* (not enabled).
- When SWBPIPE's controller is off, the CLI fails as `controller_unavailable`
  (or an attachment failure; `unsupported_host` off macOS). The App reports
  that as *endpoint unavailable*, naming the reason, and the channel shows
  *disabled*. It is never relayed as host-reported *channel not enabled*.
- If the host answers a request while no A13 is evidenced (for example with
  the variable set), the exchange is recorded as observed with the evidence
  limit "host reachable without evidenced A13". It is never shown as
  *enabled* and never counted as an examination result (E-2, E-3).
- Live XF and XC host variants keep the AWAITING INPUT token, with the
  annotation "answered: not offered; host joins deferred (DECISION-3)".
- **Owner, deferred (R8-Q4b):** whether a launch environment variable the
  person sets counts as A13 evidence. Revisit when UI-SUCCESSOR resumes.

### 3.3 Enablement rules

- **E-1 A13 is the person's act (SETTLED D2e; disable INTEGRATION R2-3).**
  Enabling and disabling are performed only by the person, through the
  host's enablement facility (ACT-POLICY-v0.6 §2.6; SQ-28). An agent may **request** either (A8); a request changes
  nothing (ACT FX-42). An agent attempt to perform A13 is *not permitted*.
  SWBPIPE has no such facility (SQ-28), so A13 cannot be performed there
  and its channel stays *disabled* (R8-6).
- **E-2 Host enablement is authoritative (INTEGRATION, R4-13; DERIVED from
  S-X8).** The
  App must not patch Codex, filter its notifications, veto the user's Codex
  configuration or pin sandbox policy. The App therefore **cannot** stop the
  user's own Codex from reaching a host CLI through command execution, or from
  using an MCP server the user configured independently, or the agent from
  editing the user's Codex configuration with its file tools. Only the host's
  own refusal (*channel not enabled*) guarantees "off". The App's own
  guarantee is narrower: while the App knows the channel is disabled, **the
  App makes no host request and supplies no access configuration**, and it
  displays the state truthfully. **VER-002 reading (R4-13):** SoW AC-002
  "no host request" is read as the App's own requests; the authoritative
  "off" for agent-originated requests is the host's refusal.
- **E-3 App-side configuration is never A13 evidence (INTEGRATION, R4-13).**
  An App-side Codex configuration that an agent could write — whoever
  actually wrote it — is never A13 evidence. Without a host enablement record
  the channel stays *disabled*. A configuration observed to have been written
  by an agent (for example into the user's Codex configuration file) is
  recorded as an evidence limit (R11) (L-ADAPTER-2).
- **E-4 App-side configuration is person-directed (PROPOSED).** The App adds,
  changes or removes its access configuration only at the person's direction
  in the App interface, shows what it changed and where (§9 OC-3), and never
  on an agent's instruction. That change is an **ordinary configuration
  change**, recorded as such: it is not a second A13, and it enables nothing
  without the host enablement record (ACT-v0.4 §2.6, which closes U-X1 as
  PROPOSED under R4-13). A13 on the host's interface is captured by the
  host's enablement facility (SQ-28). An App-captured A13 would arise only
  for an App-owned external interface, which does not exist in this
  increment; its control would then follow EXEC CAP-2/CAP-3.
- **E-5 Enablement grants no autonomy (SETTLED V4-HI-52 with W-f; DERIVED).**
  Enabling changes no grant state, no class and no checkpoint. After
  enablement the external agent is governed by the **same** host grant for
  each class (for the SWB model-change class, ⟨set-1⟩ *effective (policy
  default): propose* until the person performs A12). An enablement is never
  displayed as, recorded as, or used as A12.
- **E-6 Enablement is not gated on the model destination (SETTLED D5).**
  See §3.4.
- **E-7 Machine-local (SETTLED V4-HI-52).** Only a local endpoint is a valid
  target: a local process, a local socket, or a loopback origin. A
  non-loopback origin observed for the host's server entry (§3.5) makes the
  channel **not established** for this contract, whatever the supplier
  reports.
- **E-8 Disabling during work (PROPOSED; host behavior SQ-13).** Disabling
  stops new external requests (*channel not enabled*). It withdraws nothing:
  a proposal already queued stays queued and the person can still decide it
  in the host. The App shows the last observed state with "channel since
  disabled", never *withdrawn*, *rejected* or *outcome unknown* merely
  because observation stopped (L-ADAPTER-6). SWBPIPE: the effect of
  disabling on queued proposals is not addressed; a restart expires handles
  or yields `outcome_unknown` (SQ-13).
- **E-9 No silent re-enable.** Reconnect, endpoint restart, App relaunch or
  supplier restart never restores *enabled* without a host enablement record
  in force at that time (HOSTING H8).

### 3.4 Model destination (REQ-002; V4-HOST-02; V4-EXM-23; D5; R4-1; R5-4)

- **SETTLED by DECISION-2 D5.** Content read over the channel enters the App's
  Codex conversation and may flow to the model the person selected for that
  conversation, **cloud included**. This is the person's flexibility.
- **No gating (SETTLED D5).** The App gates neither enablement nor any read
  or submission on the model destination. It imposes no local-only
  restriction.
- **Recorded and shown, as information — INTEGRATION (DECISION-2 reading;
  R4-1, R5-4), not SETTLED.**
  - Recorded **per turn** where the supplier reports it (HOSTING-BOUNDARY-v0.6 §8.3):
    the requested and the effective destination are kept separate; a
    supplier re-route is recorded; a turn whose destination is not observed
    is *unknown*.
  - The **run-level** value is the set of destinations observed during the
    run (RS R5). A destination switch during a run starts no new run.
  - The channel status shows the conversation's current destination (class
    and, as observed, provider identity) for information.
  - Neither the display nor the record is a permission or a condition.
- **No added destination.** The channel adds no other destination: no App
  relay, no App telemetry, no remote endpoint (E-7 locality still holds for
  the endpoint). Supplier-initiated traffic (for example the plugin fetch the
  W11 spike `observed`, S-F-10) is attributed to the supplier, not to the
  channel (VER-002).
- **Host restriction is host policy (DEP-001).** A host may restrict its own
  channel, for example by destination. The App does not anticipate or enforce
  such a rule; the host enforces it, and the App relays the host's refusal
  unchanged with its reporter and governing rule (SQ-16). SWBPIPE answered
  SQ-16: no restriction and no destination field, so the App states
  nothing.
- **V4-HOST-02** continues to govern the **host's embedded agent** in local
  operation (whether it is retained is pending owner clarification, R8-9). It is neither extended to App conversations nor waived.
- U-X2 stays **closed** (D5).

### 3.5 Supplier facts at 0.158.0 that bear on channel state

All facts below are `observed-in-generated-types` unless marked. None was
exercised live.

| Supplier fact | Bearing on this contract |
|---|---|
| Stable client methods `config/mcpServer/reload`, `mcpServerStatus/list`, `mcpServer/resource/read`, `mcpServer/tool/call`, `mcpServer/oauth/login`; stable notification `mcpServer/startupStatus/updated` (startup state ∈ `starting`, `ready`, `failed`, `cancelled`; failure reason `reauthenticationRequired`) | N-MCP endpoint observation and reload after a person-directed configuration change |
| Per-server status: `name`, `tools` (map of tool descriptors: `name`, `description`, `inputSchema`, `outputSchema`, `annotations`, `_meta`), `toolsError` ("Tool discovery failed and no catalog was returned"), `authStatus`, `runtimeStatus` ∈ `notStarted`, `starting`, `connected`, `authenticationRequired`, `failed`, `cancelled`, `disabled`, `httpOrigin` (null for non-HTTP transports), `serverInfo` | `connected` + tools → reachable; `failed`/`authenticationRequired`/`notStarted`/`cancelled` → *endpoint-unavailable* with that reason; `toolsError` → every entry *not established*; `httpOrigin` is the locality evidence for an HTTP server (E-7). The supplier's **`disabled` is an App-side configuration fact, never the host's A13 state** |
| Typed `Config` has **no** MCP-server element; `Config` admits additional properties; `config/value/write` and `config/batchWrite` write a key path into the user's configuration file by default; `thread/start` carries a free-form `config` object | The App-side configuration locus is open (OC-3). Whether a per-thread `config` override accepts an MCP-server entry is `not-observed`. Writing the user's shared configuration is a change to the person's own Codex configuration (E-4) |
| Thread item `mcpToolCall` {`server`, `tool`, `arguments`, `status` ∈ `inProgress`/`completed`/`failed`, `result` {`content`, `structuredContent`, `_meta`}, `error` {`message`}, `readOnlyHint`, `durationMs`}; notification `item/mcpToolCall/progress` | What the App can observe of an N-MCP dispatch and its result (§4.4, §5) |
| `ToolExposureSurface` ∈ `direct`, `deferred`, `code_mode` | Codex's model-facing presentation of a tool. **Not** the catalog's exposure element 9 (§4.2) |
| Server request `mcpServer/elicitation/request` (modes include `form` and `url`); HOSTING R9 classes it person-input, answered only by the person | An elicitation or user-input answer is **not act evidence** and never host act capture (R4-12; EXEC CAP-6); it is conversation input to the agent (§7.6, L-ADAPTER-4) |
| Server requests `item/commandExecution/requestApproval` etc. (A14); `sandbox_workspace_write.network_access` default false; `NetworkUnixSocketPermission` ∈ `allow`, `deny` | N-CLI dispatch is subject to the user's own tool permission and sandbox (D3). Whether a local-socket CLI can reach the controller from the user's sandbox is `not-observed`; the App never changes those settings (S-X8) |
| `thread/start.dynamicTools` (DynamicToolSpec: function {name, description, inputSchema, deferLoading} or namespace) **experimental-only**; server request `item/tool/call` answered with {`contentItems`, `success`}; thread item `dynamicToolCall` | I-DT is possible only with the experimental opt-in, which changes the familiar set (HOSTING S-F-05). HOSTING classifies `item/tool/call` *known-app-unsupported* unless the App registers dynamic tools (none in this increment) |
| Legacy decision form `approved_mcp_policy_amendment` exists | Whether an MCP tool call raises an A14 request at 0.158.0, and by which request kind, is `not-observed` |

---

## 4. Receiving catalog entries through the App's Codex (REQ-001; AC-001)

### 4.1 Native-tool mapping (PROPOSED element)

| Element | Meaning |
|---|---|
| Native tool reference | What the App's Codex actually invokes: an MCP server and tool name, or a CLI command form. Supplier-facing; may be constrained by the supplier's naming rules |
| Catalog operation identity and version | The DEL-03-01 entry the native tool realizes (C §3 #1) |
| Catalog edition | The edition the native surface was generated from or checked against (C §2) |
| Mapping source | Host-supplied (generated with the catalog, or declared) or unagreed. The App never derives the mapping from tool names or descriptions |

Rules:

- **NM-1** Every external dispatch record and every received result names the
  **catalog operation identity and version**, not only the native tool name.
  A workflow requirement references the catalog identity, never an
  adapter-specific tool name (WD §4.2.1).
- **NM-2** A native tool with no resolvable mapping yields **not established**
  for any requirement that depends on it; it is never reported *present*.
  SWBPIPE supplies no mapping and has no per-operation identity or version
  (SQ-12; R8-10), so every requirement on X is *not established* against it.
- **NM-3** A catalog entry exposed on X but absent from the native surface is
  a parity gap for the host's X column (C §8), reported with the edition; the
  App does not synthesize a tool for it.
- **NM-4** Whether the native surface is generated from the catalog or hand-
  built is a §8 X-column value (*unagreed*; SWBPIPE answered that its CLI is
  hand-built and narrow, SQ-12). This file's evidence of mapping work is
  **evidence for** `UNRESOLVED{OI-003}` (App v4 OI-003), not its disposition
  (SoW TBD-003).

### 4.2 What each entry must carry to the App's Codex unchanged

All nine C §3 elements reach the external surface **with the same meaning**
(C §2 invariant 2): identity and version; purpose; input schema with explicit
target identification; availability with reasons; effects; result schema with
standing; errors with effect statements; class element with its sub-elements;
exposure element 9. Open description (C §2 inv. 4): a capable consumer reads
them without Chirality software. An MCP tool descriptor or CLI help text is a
**rendering** of the entry and may not add, drop or weaken any element.

Two supplier facts must not be confused with catalog elements (PROPOSED):

- A tool's `readOnlyHint` or other annotation is a **hint**. The catalog's
  effects element governs whether an operation is a read or a change. A
  mismatch is recorded as an evidence limit and the entry's effects are used
  (L-ADAPTER-3).
- Codex's tool exposure surface (`direct`/`deferred`/`code_mode`) is **not**
  element 9. A deferred tool is still *exposed*; *not exposed on this surface*
  comes only from the host (R2-4).

Reserved entries (OP-C6, OP-C7, OP-C8) are **always described and, where
exposed, offered** on X. The App never withholds, hides or filters an exposed
entry on its own reading of its class (C §2 inv. 5; R2-4).

### 4.3 Reads: content, standing and basis

- **RD-1** A successful read over X returns the same meaningful content and
  standing marks the person sees (V4-HI-10/12; C §6.1), including currency,
  "host checks passed: ‹named checks›" each with its evaluated basis, known
  limitations, human-act evidence with actor and recorder, and lapse state.
- **RD-2** Every read carries its **basis descriptor** (workspace identity,
  generation, model revision, canonical content identity, method designation)
  and per-row **subject content identities** (C §5). A read lacking any
  element is *basis incomplete* and cannot be cited for a change. SWBPIPE
  reads carry no subject identities (SQ-03 (a)). A host read with only a
  whole-model identity is received with that identity standing for every
  covered subject (R8-4; C §5.3), and per-subject identities are recorded
  *not supplied* (an evidence limit). Such a read satisfies RD-2 and can be
  cited (R8-12 item 6; F-24). The App never computes them. On main
  SWBPIPE has no workspace identity or generation; DRAFT #885's `inspect`
  returns a basis identity (SQ-07 (a)).
- **RD-3** The App delivers the native result unchanged (HOSTING H6). The App
  display of standing takes standing from the **host result**, never from the
  model's paraphrase of it; a model summary that strengthens standing is shown
  as the agent's text, not as the host's standing (DEL-04-02 §8 applies).
- **RD-4** Lost read response: no content is invented; a re-read obtains a new
  basis (C §7). Reads have no effects, so no model *outcome unknown* applies.
- **RD-5 Basis-citation check (PROPOSED).** The App compares each change
  request's relied-on basis with the reads the agent **actually received** in
  this conversation. A cited basis not observed in a prior read is recorded
  as an evidence limit ("cited basis not observed"); in interposed families
  the App may refuse to forward it (App-side failure, never a host outcome).
  This guards against a later basis being cited in place of the relied-on one
  (REQ-004; HI §11 queue-time basis risk).

### 4.4 Non-mutating checks (REQ-001)

A declared non-mutating operation is carried like any read: OP-C3 *Examine
support spacing* yields the requester's **findings (A3)**, never "host checks
passed" and never A4; OP-C12 *Run support-spacing host check* yields "host
checks passed: support spacing" or "host check failed: support spacing", each
with its evaluated basis. Neither is refused as *stale*; if the evaluated
basis differs from a cited one, both are stated (C §5.4).

### 4.5 Mapping native results to canonical outcomes (PROPOSED rules)

- **M-1 Transport success is not an outcome.** A completed MCP call or a
  zero exit status establishes only that the endpoint answered. The outcome
  is what the **host's result states** in C §4.1 / P §9 terms.
- **M-2 Host-stated outcomes are relayed unchanged**, with their reporter
  (host) and evaluated basis: *unavailable*, *not permitted* (naming the
  governing treatment or checkpoint constraint), *channel not enabled*, *not
  exposed on this surface*, *refused — invalid / stale*, *queued*, *applied
  (receipt)*, *application error*, *error*.
- **M-3 No outcome stated.** A read without a stated result is *error* as
  observed. A submission whose result states no outcome, or whose result
  cannot be interpreted, is **outcome unknown**, observer *App*, last observed
  state *submitted*; never *queued* or *applied*.
- **M-4 Supplier-reported call failure** (for example an `mcpToolCall` item
  with status `failed` and an error message) is a **supplier/transport
  observation**, not a host refusal. For a submission it is *outcome
  unknown* (observer App, via supplier) unless the host's own result is also
  observed.
- **M-5 App-side failures are named as App-side**: *channel not enabled*
  (App's own configuration off), *not offered* (interposed families: an
  operation absent from the edition the App offered; never dispatched,
  R2-4), *not established* (mapping). None is reported as a host outcome, and
  none is labeled *not exposed*. In native families, a supplier's or host's
  response to an unknown tool or command is relayed as observed with its
  reporter, and mapped to *missing* only on a host statement.
- **M-6 A14 settles App-side.** If the person (or the user's own Codex mode)
  declines the tool execution, no host request was made; it is recorded in
  R13 only and is not a host outcome. An affirmative A14 never stands for A5,
  A13 or any other act (S-X7; HOSTING R8).
- **M-7 Received host vocabulary: SWBPIPE (R8-5, R8-6; evidence only, DRAFT
  #885 unmerged).** The received mapping is P §9.1; the rules that bear on
  this adapter are:
  - `unsupported_method` / `unsupported_change` → host-reported *not exposed
    on this surface*, relayed with reporter host, never *not permitted*;
  - `controller_unavailable`, or an attachment failure → *endpoint
    unavailable* (App-observed), never *channel not enabled*; the channel
    shows *disabled* (§3.2);
  - `rejected: validation_rejected` → *refused — invalid* at application,
    never A10; `withdrawn` / `cleared_in_review` → the item left the queue,
    "cleared by the person, no decision record", never A10 or A11;
  - `outcome_unknown` → *outcome unknown* (reporter host); `expired` →
    *refused — stale*, reason "expired";
  - `retryable` and `next_action` are recorded and never acted on as a
    treatment.

---

## 5. Dispatch carriage (R2-12; R-7; P §3.3)

### 5.1 External dispatch record

Mirrors LOOP §6.2 for the external channel. Every dispatch carries, or the
record states it lacks, each element. **Carriage assurance** (R4-14, with
the final definition of R5-2; the set-wide wording, also used by P §3.3,
ACT §4.4, WD §4.2.2 and R2-12) says how the element reached the host:

- **host-held** — the element originates on the host side: from a
  declaration copy or run association the host holds, evaluated by the host
  route, or derived by the host loop from the resolved declaration it
  evaluates (LOOP §6.2). The dispatch need not carry it;
- **model-supplied** — composed by the model as a tool argument; observed
  and compared by the App, but not guaranteed. A constraint the host merely
  **receives** in such a request stays model-supplied: receipt alone does not
  make it host-held. If the host verifies the received constraint against
  its own copy of the declaration, it is host-held (R5-2);
- **App-assured** — added or verified by App code on the dispatch path.
  **Not available in this increment** (R4-2: no interposed App code; S-X12);
- **absent** — not carried; recorded as an evidence limit (RS R11).

**Only host-held carriage satisfies R2-12** (R5-2).

| Element | Meaning | Source | Assurance required (PROPOSED) |
|---|---|---|---|
| Origin | Author type *agent*; author identity (the App's Codex seat); channel *external agent*; conversation (the Codex thread); workflow run identity; workflow identity tuple {kind, origin, source root, name, revision} (+ derived-from); holding library | P §3.3; R-9; R2-20 | Any; a host origin mark is **linked, not copied**; mismatch → evidence limit (§5.4) |
| Seat role meaning | The role meaning in force for the App seat, or *unknown* | P §3.3 | Any |
| Grant in force | Settings reference, display state and scope for the operation's class, as last observed from the host | R-8; R2-6; AS §3 | Any; the host resolves treatment itself (§5.5) |
| Requested mode | Apply directly or propose | P §2 | Any |
| **Governing checkpoint constraint** — governance phase (retained; R8-1) | {workflow run, checkpoint name, required act A5, operation} when a declared A5 checkpoint, **governed**, governs this operation's result in this run. In Phase 1 the App carries none, and the agent never adds a field the host schema lacks (R8-10) | R2-12; P §3.3; ACT §4.4; R4-14 | **Host-held only** (R5-2). Model-supplied — including a constraint the host merely received from the model's call — does not satisfy R2-12 |
| Relied-on basis | Basis descriptor(s) with method designation; per-target subject content identities | C §5.4; P §3.2 | Any, with the RD-5 check |
| Catalog edition and entry version | As offered or as mapped (§4.1) | C §2; LOOP O-3 | Any |
| Proposal identity | Minted **before** the first submission; unchanged on every retry | P §3.1; R-7; R2-13 | Model-supplied acceptable for *propose*; App-assured or host-issued for *apply directly* — host-issued only in this increment (§5.6) |
| Reason | The proposer's reason | P §3.3 | Any |
| Correlation identity | The native call identity and the Codex thread/turn identities | HOSTING H6 | Observed by the App in every family |

### 5.2 Carriage by realization family

| Element | N-MCP / N-CLI (native) | I-DT / I-PX (interposed) | With a host-held run association (any family) |
|---|---|---|---|
| Origin: conversation, workflow run, workflow identity | model-supplied (the model must be told and must copy them) | App-assured | host-held |
| Author identity | unverified (PR #885 description: controller metadata "does not claim a verified Codex/person identity") | App-assured to the endpoint; host verification still open (OC-6) | as host verifies |
| Grant in force | model-supplied or absent | App-assured (from last host read) | host-held (the host's own grant) |
| Governing checkpoint constraint | model-supplied — **insufficient** (§5.3) | App-assured | host-held |
| Relied-on basis | model-supplied; RD-5 after the fact | App-assured after RD-5 before dispatch | model-supplied or App-assured |
| Proposal identity on retry | model-supplied | App-assured | host-issued draft identity if offered (SQ-08) |
| **Adopted in this increment** | yes (whichever the host seam allows) | **no** (R4-2; register option only) | SWBPIPE: no host-held run association or constraint (SQ-02, route (iv)); DRAFT #885 issues `preview_ref` and `ticket` against a caller key, within one controller session (SQ-08) |

### 5.3 Governing checkpoint constraint (R2-12)

**Phase (R8-1; R8-11 item 2; EXEC CH-27).** GC-1, GC-3, GC-5 and the
classification by held actions are the **governance-phase definition
(retained)**, applying to governed checkpoints. **In Phase 1:** the App
carries no constraint and assigns no hold-support value. The agent follows
the declaration as plan guidance (WD I-7), proposes the operation, and never
adds a field the host schema lacks: SWBPIPE's strict preflight refuses
unknown fields, so a constraint field would be refused as `invalid_request`
(SQ-02 (a), SQ-31; R8-10). A direct request, if made, meets the host's own
treatment and is recorded as observed. Nothing is held, and nothing is
reported *not permitted* or *unsupported* on a checkpoint's account (EXEC
PH-2, PH-3). GC-2 stays true in both phases, and GC-4 records the expected
constraint in both.

- **GC-1 (SETTLED/DERIVED, ACT §4.4; governance phase).** Under the constraint the host route
  resolves *propose*. A direct request is **not permitted**, naming the
  constraint as the governing treatment, and is **never converted** into a
  proposal. The agent may submit a proposal separately; its queued items
  become the checkpoint's subject (reached-when kind (c), R2-17).
- **GC-2 An omitted constraint is indistinguishable from none (R2-12).** On
  the external channel the consequence is sharp: if the model omits it and
  requests direct application under an effective direct grant, the host would
  apply directly and the checkpoint would be bypassed (contrary to W-b).
- **Classification by held actions (R6-1).** The hold-support value is
  decided by **what the checkpoint must hold**, not by how it arrives (EXEC
  §3.6):
  - **host-held class (HS-3):** every action the checkpoint must hold is a
    **host operation** on the external channel (the governed operation, or
    the host operations after arrival until the act). The value follows the
    SQ-02 status — GC-3 for an A5 constraint, GC-5 for other host-operation
    holds;
  - **App-side class (HS-5):** at least one held action is App-side (an App
    agent turn, an App tool or harness action, an App file write or return
    step). In App runs the value is **not enforceable** (D6), whatever SQ-02
    returns;
  - host-loop holds (HS-2) and invalid declarations (HS-1: no value; the
    check is *not established*) are unchanged; multi-checkpoint precedence is
    EXEC §3.5's.
- **GC-3 Hold support for an A5 checkpoint on X (R4-14; R5-1; R5-2; R6-1) — governance phase (retained; R8-2).**
  Applies when every held action is a host operation (HS-3); if the
  checkpoint also holds any App-side action, it is *not enforceable* (HS-5).
  Only host-held carriage satisfies R2-12. The adapter supplies the carriage
  facts; DEL-02-03 computes and reports the value (EXEC §3.6, value set owned
  there and ruled by R5-1/R6-1):

  | Situation on X | Hold-support value | Requirement check |
  |---|---|---|
  | The host's SQ-02 answer shows a host-held constraint, **and** it is evidenced on an identified candidate | *enforced on the host route* | passes (host evidence, DEP-001) |
  | SQ-02 not yet answered, so whether the constraint can be host-held is unknown | **not established** | does not pass; never *unsupported*; cases AWAITING INPUT (SQ-02) |
  | SQ-02 answered and no host-held route exists, so the constraint could travel only as model-supplied (or absent) (**SWBPIPE since 2026-09-28**: SQ-02 route (iv), none planned) | **not enforceable** | *unsupported*, reason "checkpoint hold not enforceable on this surface" (R4-8) |

  Model-supplied carriage leads to *not enforceable* **only** in the last
  row, once SQ-02 has been answered with no host-held route; before that
  answer the value is *not established* (R6-5). SWBPIPE answered SQ-02 on
  2026-09-28, so for SWBPIPE the last row applies (R8-2). These are
  governance-phase values, reading the checkpoint as if declared governed
  (R8-11 item 5). A later SWBPIPE decision to plan a route is a revision
  trigger.

  *Enforced on the host route* is never assumed: it is used only after an
  SQ-02 answer **and** candidate evidence (R5-1). The v0.1 values *enforced
  before dispatch* and *held after observation* are retired.
- **GC-4** Whatever the family, the App records the constraint it expected
  (derived from the selected declaration, WD §4.2.2) beside the one observed
  in the dispatch. *Governance phase:* an omission in an App-carried run is
  an **App-side defect**, recorded as "omitted governing checkpoint
  constraint" (RS R11; P §3.3). *Phase 1:* the expected constraint is
  recorded only; where the host schema defines no element for it, the
  record carries the evidence limit "constraint not carriable on this host"
  (adopted in RS R11, R8-12 item 5; R8-10).
- **GC-5 No App hold is claimed on X (R4-2; R5-1; `UNRESOLVED{D6}`) — governance phase (retained); in Phase 1 nothing is held on X (R8-1).**
  Holding a call *before dispatch* (reached-when kind (a)) would need App
  code on the dispatch path (HP-1) or a host that holds the call (HP-H). HP-1
  is not adopted, and neither is reliance on `turn/interrupt` (HP-2). A
  named-rule decline of a tool-permission request that happens to reach the
  App (HP-3) is a permitted best effort under D3 and is never presented as a
  hold: the user's Codex mode may settle the request itself, and a decline
  is not a hold-and-release. HP-4 is applied: while a run holds, the App
  starts no turn and issues no App-initiated call for it — including an
  App-initiated `mcpServer/tool/call`, where the App is the caller (HOSTING
  §6.8) — but this does not stop actions Codex takes inside a turn already
  running. Values on X, classified by held actions (R5-1; R6-1):
  - **all held actions are host operations** (HS-3) — for example kind (a)
    before dispatch of a host operation, or host operations after arrival
    until the act: *not established* while SQ-02 is unanswered; *enforced on
    the host route* only once the host holds or refuses them and that is
    evidenced on a candidate; *not enforceable* if SQ-02 is answered with no
    host-held route — the latter applies to SWBPIPE (SQ-02 answered
    2026-09-28; R8-2);
  - **any held action is App-side** (HS-5) — an App agent turn, an App tool
    or harness action (including kind (a) on a harness capability), an App
    file write or return step, or a kind (b)/(c) run halt **whose held
    actions include any App-side step**: **not enforceable** in App runs
    whatever SWBPIPE answers (R5-10; R6-1; R7-1) — a separate D6 follow-up
    for the owner, not something SQ-02 can resolve. A run halt holding only
    host operations is HS-3, above; GC-3 covers A5, whose held action is the
    governed host operation.
  In every governance-phase case an external dispatch observed after an
  arrival while the checkpoint is *waiting* is recorded as **action during
  hold** (RS R11; R4-11) and is not prevented (§7.7). In Phase 1 it may
  carry only the optional "continued past ‹checkpoint› before ‹act›"
  annotation (EXEC PH-7).
- **V-CP1 over X.** *Phase 1:* as EXEC CH-27 (guidance; the agent proposes;
  the host's own treatment decides). *Governance phase:* *not enforceable* →
  *unsupported* (SQ-02 answered 2026-09-28: route (iv); HS-3 (c)); the
  host-held variant is a test double only (XF-25).

### 5.4 Origin

- The App records the request-side origin it observed (R7). The host's
  origin mark is **linked, not copied**; a mismatch is an evidence limit
  (P §3.3; V4-HI-71).
- Author identity over X is **unverified** until a caller-identity mechanism
  exists (OC-6; SQ-14). SWBPIPE confirms this: its DRAFT #885 controller
  assigns the origin, rejects caller-supplied author, source and acceptance
  fields, and records the caller as not verified (SQ-14). *unverified* is an explicit author-identity value
  (P §3.3 as amended by R4-15), with the matching RS R11 evidence limit. The record shows "external agent (unverified identity)"
  rather than asserting the App's Codex as the author.
- Channel is always *external agent*. The channel is attribution, never a
  route selector (P §2).

### 5.5 Grant in force

- The host holds the grant; the App holds none for host operations (R-2 D3
  bullet: the autonomy grant governs host operations only). The App reads it
  from the host for display and carriage.
- Standing at drafting and treatment at resolution are both recorded when
  they differ; the settings reference at application is **host-reported** or
  *unconfirmed* (R-3.6; R-8).
- Narrowing leaves a queued proposal unaffected; an unapplied direct request
  is re-resolved at application and becomes *not permitted* if no effective
  direct treatment remains. Widening never converts a queued proposal
  (R-3.6/3.7; ACT FX-37/38).

### 5.6 Proposal identity on retry

- **PI-1** A retry (resubmission after a lost acknowledgment or *outcome
  unknown*) carries the **same** proposal identity and unchanged content.
  The host de-duplicates by identity **before** any basis check and answers
  from the recorded state; a retry is never refused *stale* because of its
  own effects (R2-13).
- **PI-2** After *outcome unknown* the agent, following App-supplied
  guidance, **seeks observation first** — a host read of the proposal by
  identity (SQ-08; SWBPIPE DRAFT #885: `status` by `ticket`, within one
  controller session) — before any resubmission (LOOP R-d). The App observes and
  records whether that order was followed; with no App code on the dispatch
  path (S-X12) it cannot enforce it, and a resubmission without prior
  observation is recorded as an evidence limit.
- **PI-3** A re-draft is a new proposal with lineage, a new read and new
  change-item content identities; no acceptance carries over (P §5).
- **PI-4 Durability limit (evidence, PR #885; confirmed by SQ-08 (c)).** The PR description states
  that repeated submit keys recover the original result "within the same
  controller session" and that recovery "does not survive a controller
  restart". A retry after an endpoint restart may therefore be treated as a
  first receipt. Under *propose* this risks a second queued proposal, not a
  second effect without the person's A5; under *apply directly* it risks a
  second effect. PROPOSED: over X, *apply directly* relies on a host-issued
  identity (or, if interposition is ever adopted, an App-assured one) whose
  de-duplication survives endpoint restart; otherwise a post-restart retry is
  reported *outcome unknown* and the one-effect obligation is recorded as
  unevidenced (SQ-08; L-ADAPTER-5).
- **PI-5 Two submissions before any acknowledgment (R4-20; XT L-XT-2).** The
  same proposal identity sent twice before either submission is
  acknowledged: each submission is recorded separately; the App reports
  neither as *queued* until a host acknowledgment is observed; the host is
  expected to answer the second from the recorded state of the first (or
  from its in-flight state). One domain effect is shown only from domain
  evidence (model history, receipts) — otherwise "one effect unevidenced".
  If the two sends carry **different** identities (the model minted a new
  one), they are two proposals: two queued proposals under *propose*; under
  *apply directly*, a possible second effect, recorded, never hidden
  (L-ADAPTER-11).
- **PI-6 App restart during a submission (R4-20; XT L-XT-3).** If the App
  (and therefore the App-owned Codex child, HOSTING §4) restarts after a
  submission was sent and before its result was observed, the submission's
  outcome is **outcome unknown**, observer App, last observed *submitted*.
  Nothing is inferred from the relaunch. After relaunch the App reports the
  channel state afresh (E-9: no silent re-enable), and observation by
  identity (PI-2) precedes any resubmission. Custody of the in-flight native
  item across relaunch is DEL-01-02's (later undertaking, D1); until then the
  App record shows the interruption as an evidence limit (L-ADAPTER-12).

---

## 6. Same route and same policy as the host UI (REQ-003; AC-003)

- **RP-1 One route (SETTLED S-X4).** Every external change goes to the host's
  one validation/application route. The App defines no alternate mutation
  path, never applies outside the host route, and never bypasses validation
  (P §2; AC-003). Interposed families (not adopted, S-X12) would forward only; they would add carried
  elements and App-side failures and decide nothing.
- **RP-2 Equivalence.** For equivalent operation identity/version,
  arguments, relied-on basis and authority, X receives the same outcome and
  error meaning (identity and text) as H and E (P §2). The permitted
  difference is authority only, reported as *not permitted* naming the
  governing treatment, never as a different validation error.
- **RP-3 Treatment outcomes on X** (ACT §5.3, §6; consumed unchanged):

  | Situation on X | Outcome |
  |---|---|
  | A13 not performed | **channel not enabled** (§3.2) |
  | Declared catalog precondition fails | **unavailable**, same reason and evaluated basis as H and E (V4-HI-04; C §10.6) |
  | Entry not exposed on X (element 9) | **not exposed on this surface**, host-reported, relayed |
  | Direct requested without an *effective direct* treatment (policy default *propose*; unconfirmed; requested by agent; not set; refused) | **not permitted**, naming the policy record; **never converted** into a proposal |
  | Direct requested under a governing checkpoint constraint (governance phase, governed checkpoint with host-held carriage; in Phase 1 the host's own treatment decides) | **not permitted**, naming the constraint (§5.3) |
  | Operation performs A4, A5, A6, A7, A10, A12 or A13 (P-02) | **not permitted**; an A8 request is **offered**, recorded only if the agent issues it |
  | Class *no policy basis* (P-06) | direct **not permitted**; proposing available and confers no permission; A12 widening refused; dependent production **held** |
  | Class *proposal only* | *propose*; no grant widens it |
  | Effective direct grant in scope, no constraint | apply directly: receipt, origin mark, undo route, later-check route; **no acceptance recorded** |

- **RP-4 Channel-specific host restriction (evidence, PR #885).** The PR
  description states that "Apply stays in the app's human review route". If
  the host treats all external changes as proposals regardless of grant, that
  is a host policy about the channel. It must be **stated by the host** as a
  governing treatment (so a direct request is *not permitted* naming it) and
  never presented as a class value or as the grant (S-X3; SQ-06).
  **SWBPIPE (SQ-06; R8-5):** the host states no such treatment. Apply is not
  a method on X, and a request for it is refused `unsupported_method`. The
  App relays that as host-reported *not exposed on this surface*; it never
  shows a channel rule, class value or grant, and records R2-4 (a named
  rule) as not met by this host. Whether SWBPIPE's no-Apply rule is a
  channel rule or a property of its first journey is a SWBPIPE owner
  decision; the App needs nothing from it now.
- **RP-5** App-side A14 precedes any host request and is not a host outcome
  (M-6). No classifier or permission layer is added on X by the App (D3).
- **RP-6** Undo over X (OP-C10) is a change through the same route with its
  own treatment, governed by the policy record of the operation whose receipt
  it reverses (R3-4); its outcome carries *reverses ⟨receipt⟩*. SWBPIPE's
  Undo is not exposed on its CLI, and its session undo writes no receipt, so
  *reverses ⟨receipt⟩* is *not supplied* for it (SQ-10; R8-5).

---

## 7. Outcomes, acts and faithful recording (REQ-004; AC-004, AC-005)

### 7.1 Stale refusal and original basis

A submission cites the basis it relied on, unchanged from the read; the host
checks per item against the relied-on targets' subject content identities
where it supplies them, and otherwise applies its stated staleness scope,
which the App relays unchanged and never narrows (R2-13 as amended by R8-3;
SWBPIPE: the whole model, SQ-07 (d)). A stale refusal is relayed with reason, failing targets, relied-on
basis and current basis (P §5). No App component rewrites the relied-on basis
and resubmits; a re-draft is a new proposal (PI-3).

### 7.2 No retargeting

Bound targets are fixed at drafting from explicit target identification. A
later selection in any surface — including the person selecting S-4 in the
host UI while an external proposal is pending — never changes them (P §6).

### 7.3 Repeated submission

Each submission is recorded separately with only the effects actually
observed (same receipt, two receipts, or unknown). One effect per item is a
**host obligation to be evidenced** (DEP-001), not a recorded fact; transport
or session de-duplication is not evidence of one domain effect (V4-EXM-25;
PI-4).

### 7.4 Outcome unknown

Reported whenever the result of a sent step cannot be observed, attributed to
the observer that lost it — here the **App** (directly, or via a supplier
report) — with the last observed state. Never inferred applied, failed,
accepted or rejected; a later observation is reported separately and does
not back-fill (P §4.1 rule 3).

### 7.5 Human acts are never fabricated

- Success, *queued*, a receipt, an A14 answer, an A8 request, a model
  statement or an MCP elicitation answer **never** establishes A4, A5, A6,
  A7, A10, A12 or A13.
- The App reports *queued* until the host records acceptance and
  application; "accepted" only with host-captured A5 and its actor; "applied"
  only with a receipt (P §4.1).
- Execution, edit acceptance, checking, approval and reliance keep separate
  standing. An independently evidenced act (for example T2's A4 on S-2 with
  no proposal) is carried without any acceptance predecessor (SoW REQ-004;
  ACT FX-07).

### 7.6 Positive faithful recording (A9)

When a host read over X reports an actually performed act (for example T11:
A5 on PR-2 item 1 and A10 on item 2 by Engineer A, captured by the host
facility), the App may record it **faithfully**: decision actor Engineer A;
recorder the App; recording mode *faithful recording*; bound content identity
(the change-item content identity for A5/A10, the subject content identity
for A4/A6/A7) with method designation; and the host's **capture-evidence
reference**. Without that reference the record is a record shape only and
satisfies no checkpoint (R-5; R2-20; SQ-01). SWBPIPE exposes no
capture-evidence reference: its Apply receipt names no person and no time,
and does not survive restart (SQ-01). An MCP elicitation, Codex
user-input request or CLI prompt answered in the App is **not act evidence**
and never host act capture (R4-12; EXEC CAP-6); it is conversation input to
the agent (L-ADAPTER-4). Acts on host content are captured by the host facility;
the App offers no proxy control for them in this increment (EXEC CAP-1).

### 7.7 Checkpoint observation on X

For an A5 checkpoint with reached-when kind (c) *proposal queued*, the App
observes *queued* and later the host-captured item decisions through host
reads over X and passes them to DEL-02-03 (for recording in Phase 1; to the
hold machine in the governance phase). The adapter
observes and reports; it does not hold, resume or evaluate dispositions.
Dispositions use the shared vocabulary: waiting · performed · resolved
negatively · lapsed · not reached · unknown. In Phase 1 they label the
record: *waiting* means "reached; act not yet recorded", never "the run is
held" (EXEC PH-6).

**Phase 1 (R8-1).** The adapter observes arrivals and act records and passes
them to DEL-02-03 for recording. It supplies no hold-support input, and no
value is assigned. A run action observed after an arrival and before the
act that answers it may carry the optional annotation "continued past
‹checkpoint› before ‹act›" (EXEC PH-7): information, never a defect. The
person's own operations never carry it (read from R5-5). A lapse is still recorded, and
nothing re-holds (R8-11 item 1). The display never says the run is held.

**Governance phase (retained; D6 re-opens with it, R8-2).** For governed
checkpoints (`UNRESOLVED{D6}`; S-X12) the adapter:

- **supplies hold-support inputs** per checkpoint on X to DEL-02-03 (EXEC
  §3.6): the observed carriage assurance of the constraint, and whether the
  host holds before-dispatch calls (both depend on SQ-02; SWBPIPE: neither,
  SQ-02 answered 2026-09-28). Values are only
  the four of R5-1 (§5.3 GC-3, GC-5); *enforced on the host route* is never
  reported without an SQ-02 answer and candidate evidence;
- **records action during hold**: every external dispatch (and its outcome)
  observed in the run after an arrival while the checkpoint is *waiting* is
  recorded with the "action during hold" annotation (RS R11; R4-11), with
  correlation to the arrival. It is not prevented and not undone. The
  person's own operations — including the person's own undo (OP-C10) — are
  never recorded as action during hold (R5-5); a lapse they cause re-holds
  per EXEC, and an undo never re-holds an A5 arrival;
- applies R6-3's meaning of "held": under *enforced on the host route* the
  host refuses the held host operations and any other action is recorded as
  action during hold; under *not established* / *not enforceable* nothing is
  stopped and actions are recorded as action during hold;
- makes **no claim of an App hold**: the display never says the run "is
  held" on X; it says what the checkpoint waits for and lists any action
  during hold (L-ADAPTER-13).

---

## 8. Operating sequences

```text
S-1 Enable
  person performs A13 in the host facility ──► host enablement record (+capture ref)
  person directs App-side access configuration (E-4) ──► App configures (locus OC-3)
  App observes endpoint (reachable? locality?) ──► channel: enabled | endpoint-unavailable
  grant display unchanged (E-5); model destination shown for information, no gate (§3.4)
  channel usable only with a host enablement record (SQ-28); otherwise disabled
  (SWBPIPE: no facility, so disabled; controller_unavailable → endpoint unavailable; R8-6)

S-2 Inspect (read)
  model invokes native tool for OP-C1 ──[A14 per user's Codex mode]──► host read
  ◄── content + standing + basis B + subject identities (or a C §4.1 non-success)
  App records R7 (operation identity/version via §4.1 mapping, correlation, basis)

S-3 Submit a proposal
  model composes change citing B, targets, proposal identity, origin, [constraint: governance phase]
  App: RD-5 basis-citation check; GC-4 expected-constraint comparison
  ──► host route: de-duplicate → treatment → per-item basis check
  ◄── queued | refused — stale/invalid | not permitted (named) | … (P §9)
  App reports queued (never accepted); observes item decisions by later reads

S-4 Lost acknowledgment
  submission sent; no result observed ──► outcome unknown (observer App)
  seek observation (read by proposal identity) ──► recorded state reported separately
  only if never received: retry with the same identity (PI-1…PI-4)

S-5 Disable
  person performs A13 (disable) ──► host refuses new requests: channel not enabled
  App removes its configuration at the person's direction; queued proposals unaffected (E-8)
```

---

## 9. Open-choice register — MCP versus CLI and related choices (TBD-007)

Nothing here is selected. Each row names its owner and point of need. Owner
for every row unless stated: **App external-host integration owner with the
external host owner** (SoW TBD-007). Point of need unless stated: **before
the App receiving implementation depends on it, and before DEL-09-09
qualification** (CASE-002 M2-A). V4-HI-50 lets the **host** choose which
seam it offers; the App receives the seam the host selects (DEL-09-09
REQ-002).

**Observed context — draft PR #885 (evidence only; not a commitment, not
merged, not a delivered SWBPIPE contribution).** From its description at head
`12907f39`: an **opt-in local JSON CLI** over a **private Unix-socket bridge**
to the running Piping desktop controller (the host this basis calls the
Piping controller, HI §11); operations "inspects Node data, previews single
or ordered atomic `position.x` edits, submits frozen proposals to the existing
review queue, and retrieves their outcomes"; "Apply stays in the app's human
review route"; acknowledgements follow published controller state; repeated
submit keys recover the original result within the same controller session,
and recovery does not survive a controller restart; controller metadata does
not claim a verified Codex/person identity; the optional CLI is excluded from
normal desktop packaging; the isolated self-test did not launch the live
controller, and no ordinary live endpoint or actual-human witness has been
recorded. Whether its operations are catalog-derived, whether its opt-in is a
person's captured A13, and how its outcomes map to P §9 are not stated.

**SWBPIPE's answers (2026-09-28; R8-7).** PR #885 head `12907f393` is open,
unmerged and **deferred** to UI-SUCCESSOR, with the owner's bounded
live-controller activation still in force; the work graph's deferral governs
over the PR description's "reconfirmed proceeding" (ANS §0 A-2, §3 item
11). The answers settle what the description left open, as SWBPIPE's
current state: its operations are hand-built and narrow, not catalog-derived
(SQ-12); its opt-in is a launch environment variable plus a build feature,
not a person's captured A13 (SQ-13, SQ-28); and its outcomes map as P §9.1
records (SQ-09).

| Id | Choice | Options | Evidence at pin 0.158.0 and observed context | What depends on it | Owner / point of need | Relay (RELAY-v0.3) |
|---|---|---|---|---|---|---|
| OC-1 | Transport family the host offers | (a) MCP server; (b) CLI over the live controller; (c) both | MCP: stable client methods and `mcpToolCall` items (`observed-in-generated-types`). CLI: Codex command execution with A14 approval kinds (`observed-in-generated-types`). PR #885: a CLI instance (evidence only). SQ-12 (answered): SWBPIPE offers the CLI (DRAFT #885), not MCP; an MCP adapter only under the owner's modern-client condition, a SWBPIPE owner decision | §3.5 observation; §4.5 mapping; §5.2 carriage; VER-001/002 | Host owner selects with App owner agreement | SQ-12 (answered) |
| OC-2 | App realization family | N-MCP; N-CLI; I-DT; I-PX | **Interposed families not adopted in this increment (R4-2, D6)**; they stay registered options (SQ-02 answered: route (iv); D6 closed for Phase 1, R8-2). I-DT needs the experimental opt-in (`dynamicTools` experimental-only; S-F-05). I-PX is an App-side server — tension with SoW OUT-001 "without prescribing … a new server" (F-6) | Carriage assurance (§5.2), GC-3/GC-5 holds, PI-4 | App owner, after XQ-3/XQ-5 answers | SQ-02; SQ-08 |
| OC-3 | App-side configuration locus | (a) user's Codex configuration file (via `config/value/write` / `config/batchWrite`, or by the person by hand); (b) per-thread `config` on `thread/start`; (c) a Codex plugin; (d) none (N-CLI with the CLI on the person's path) | Typed `Config` has no MCP element; per-thread acceptance `not-observed`; plugin association appears in server status (`pluginId`). Writing the shared file changes the person's own Codex configuration (S-X8) | E-3, E-4, U-X1; reversibility; what "disable" removes | App owner with DEL-01-01 (and DEL-01-05 in the later undertaking) | — |
| OC-4 | Enablement loci | (a) host-side only; (b) App-side only; (c) both, host authoritative (INTEGRATION R4-13: App-side configuration never A13 evidence; host refusal is the authoritative off) | App cannot guarantee "off" App-side (S-X8). SQ-13 (answered): a launch environment variable plus a build feature, not a captured act; no *channel not enabled* code; state not readable. SQ-28: no facility | §3.2 states; AC-002 reading (R4-13); A13 capture by the host enablement facility (ACT-POLICY-v0.6 §2.6) | DEL-04-01 with owner and host owner | SQ-28 (facility and capture reference; gates the whole channel); SQ-13 (behavior) |
| OC-5 | Local transport and endpoint locality | stdio subprocess launched by Codex; loopback HTTP (`httpOrigin`); local socket (PR #885) | `httpOrigin` null for non-HTTP (`observed-in-generated-types`); sandbox effect on a local-socket CLI `not-observed`. SQ-15 (answered): a Unix domain socket and descriptor in a private directory under the system tmp directory (0700/0600); no network listener; sandbox effect not addressed | E-7 locality evidence; VER-002 | Host owner with App owner | SQ-15 |
| OC-6 | Caller authentication and identity | none (PR #885: identity not verified); local-socket permissions; a token issued at enablement; supplier OAuth (`mcpServer/oauth/login` exists; its fit for a local endpoint `not-observed`) | See left. SQ-14 (answered): a random local capability in a 0600 descriptor; up to 16 concurrent callers; identity not verified | §5.4 author identity; multiple local callers; A13 scope | Host owner with App owner | SQ-14 |
| OC-7 | Carriage mechanism for origin, constraint, grant and proposal identity | tool arguments (model-supplied); request metadata added by App code; host-held run association registered at run start; host-issued draft identity (preview step) | Whether the App can add metadata to a model-issued MCP call `not-observed`. PR #885 has a preview step and submit keys (evidence only). SQ-08: identity = caller `idempotency_key`; host `preview_ref` precedes submit. SQ-14: caller-supplied origin fields rejected. SQ-02: a constraint field would be refused as unknown | §5.1–§5.6; GC-3; PI-4 | Host owner with App owner and DEL-03-02 | SQ-02; SQ-08; SQ-14 |
| OC-8 | Native surface derivation | generated from the catalog; checked against it; hand-built | PR #885 operation set looks narrow and specific (Node data; `position.x`). SQ-12 (answered): hand-built and narrow; not generated from or checked against a catalog; no per-operation identity or version | NM-3/NM-4; C §8 X column; `OI-003` evidence | Host owner; disposition `UNRESOLVED{OI-003}` | SQ-12 |
| OC-9 | Result and outcome encoding | MCP structured content; MCP text content; CLI JSON on standard output with exit status | `McpToolCallResult` {`content`, `structuredContent`, `_meta`}; no error flag element observed in the generated result type. SQ-09 (answered): CLI JSON with named codes (M-7; P §9.1) | M-1…M-5 | Host owner with App owner and DEL-03-02 (TBD-002 mechanics) | SQ-09 |
| OC-10 | Outcome read-back by proposal identity | host read operation; none | PR #885 "retrieves their outcomes" (evidence only). SQ-08: `status` by `ticket`, within one controller session | S-4; PI-2; T13 | Host owner | SQ-08 |
| OC-11 | Checkpoint hold on X | host evaluates the declaration; App interposition; App interrupts the turn — **the last two not adopted (R4-2)**; Phase 1: no hold on X (R8-1); governance phase: `UNRESOLVED{D6}` (closed for Phase 1, R8-2), with SWBPIPE offering no host route (SQ-02). Hold-support values are the four of R5-1 only | `turn/interrupt` exists (stable) but is not relied on (R4-2); hold semantics and values are DEL-02-03's (EXEC §3.6) | GC-3, GC-5, §7.7 | DEL-02-03 (W7) with host owner | SQ-02 (answered: route (iv), none planned) |
| OC-12 | Tool-permission interplay | whatever the user's Codex setting produces | Command approvals (A14) `observed-in-generated-types`; MCP-call approval path `not-observed`; `network_access` default false | M-6; RP-5; VER-002 destination inspection | Carried unchanged (D3); App implementation owner records observations | SQ-15 |

---

## 10. Consumer fixture inventory (OUT-003) — transport-neutral, simulated

Every case below runs against a **simulated endpoint (test double)** unless a
row says otherwise; its evidence label is *illustrative* until executed and
*test-double* when executed (C-v0.6 evidence-label mapping; LOOP §12
FIXTURE-EXECUTED; PANEL EXECUTED on a test double). No case establishes host
behavior, host delivery, person enablement or the joined witness (DEL-09-09).
Each case is run once per realization family actually selected (§9 OC-2),
because carriage assurance differs; in this increment only native families
are adopted (S-X12), so interposed-family expectations are kept for the
register only. Fixture assumptions are cited as C-v0.6 **FXA-n** (FXA-1
exposure ×3; FXA-4 settings; FXA-5 `CP-accept` and `CP-check`), not FA-n; where a case depends on an unanswered
relay question it is **AWAITING INPUT**, and where it depends on an unruled
policy it is **HELD**. Where SWBPIPE answered the question "no" or "none",
the case keeps the AWAITING INPUT token with the annotation "answered: not
offered; host joins deferred (DECISION-3)", because the answer does not
supply the named input (R8-6; I2 STD-2). This applies to the live host
variants of XF-01…XF-05 (SQ-28) and to XF-18, XF-21 and XF-40. Checkpoint
cases give a Phase-1 result and a governance-phase value, reading the
fixture's checkpoints as if declared governed (R8-1; R8-11 item 5).

### 10.1 Local subjects (named per R2-21, with reasons)

| Label | What it is | Why local |
|---|---|---|
| L-ADAPTER-1 | Channel states: never enabled; enabled; endpoint stopped; endpoint needs authentication; tool discovery failed | C §10 declares no enablement fixture; A13 is not a catalog entry (C §10.2 note) |
| L-ADAPTER-2 | The agent writes an App-side access configuration for the host into the user's Codex configuration | Adapter-specific risk from S-X8 |
| L-ADAPTER-3 | OP-C9's native descriptor carries a read-only hint although its effects are a change | Native hints are adapter-specific |
| L-ADAPTER-4 | The host endpoint asks, through an MCP elicitation or CLI prompt, "accept PR-2 item 1?" | Adapter-specific act-capture risk |
| L-ADAPTER-5 | Endpoint restart between T12 and the T13 retry | PR #885 session-scoped recovery |
| L-ADAPTER-6 | Person disables external access (A13) after T10, before T11 | C has no channel event |
| L-ADAPTER-7 | Person declines the tool execution (A14) of the T7 submission | App-side A14 is outside C |
| L-ADAPTER-8 | App conversation uses a user-chosen cloud model destination | Model-destination case (D5) |
| L-ADAPTER-9 | In native carriage, the model omits the constraint in V-CP1 | Carriage-assurance case |
| L-ADAPTER-10 | The host origin mark names a different conversation than the App observed | Origin-mismatch case |
| L-ADAPTER-11 | PR-2 sent twice, with the same identity, before any acknowledgment; variant with a new identity on the second send | R4-20; aligns with DEL-09-09 XT L-XT-2 (C's T13 covers only a retry after application) |
| L-ADAPTER-12 | The App (and its Codex child) restarts after the T10 submission is sent and before its result is observed | R4-20; aligns with DEL-09-09 XT L-XT-3 (v0.1 covered endpoint restart only) |
| L-ADAPTER-13 | CP-accept waiting on PR-2's items (V-CP1 after the separate proposal queues); the model then submits OP-C9 on S-4 over X | D6 (R4-2): action during hold on X |

### 10.2 Cases

| Case | Steps / subject | Expected result | AC / VER |
|---|---|---|---|
| XF-01 Disabled, App-side off | L-ADAPTER-1 never enabled; a workflow requiring OP-C1 on X; agent attempts T3 | Channel *disabled* (reporter App); required-tool outcome *channel not enabled*; **no host request** from the App; never *unavailable* or *missing* (ACT FX-24) | AC-002 / VER-002 |
| XF-02 Disabled, host-side off | App-side configured; host enablement absent; agent attempts T3 | Host-reported **channel not enabled**, relayed with reporter host; channel *disabled*. (SWBPIPE form: no host code; `controller_unavailable` → *endpoint unavailable*, channel *disabled*; SQ-13; R8-6) | AC-002 / VER-002 |
| XF-03 Agent-written configuration | L-ADAPTER-2, host enablement absent | Channel stays *disabled*; any request → host *channel not enabled*; evidence limit recorded; not A13 (E-3) | AC-002 / VER-002 |
| XF-04 A13 requested by agent | Agent asks the person to enable; separately attempts to enable | Request: A8 offered, recorded only if issued; attempt: *not permitted* (ACT FX-42); state unchanged | AC-002, AC-005 / VER-002, VER-005 |
| XF-05 Enablement grants no autonomy | Person performs A13 at T1 | Grant display for P-03 remains *effective (policy default): propose* (⟨set-1⟩); no A12 recorded; model destination shown for information only (§3.4) | AC-002 / VER-002 |
| XF-06 Endpoint unavailable | L-ADAPTER-1 endpoint stopped; needs authentication; tool discovery failed | *endpoint-unavailable* with the observed reason; discovery failure → every entry *not established*; no operation outcome inferred; supplier `disabled` status never read as A13. (SWBPIPE reasons: `controller_unavailable`, attachment failure, `unsupported_host`) | AC-002 / VER-002 |
| XF-07 Locality | Host entry resolves to a non-loopback origin (variant) | *not established* (E-7); no request sent by the App | AC-002 / VER-002 |
| XF-08 Unavailable parity | T8 over X (C §10.6) | *unavailable*, failed precondition "current solve exists", reason R-no-current-solve, same statement, evaluated basis B2 — identical to H and E | AC-001, AC-003 / VER-001, VER-003 |
| XF-09 Not exposed | V-X1 (OP-C9 not exposed on X) | Host-reported **not exposed on this surface**, relayed (reporter host); never *missing* or *channel not enabled*. (SWBPIPE form: `unsupported_change`, M-7; R8-5) | AC-001 / VER-001 |
| XF-10 Not offered vs unknown tool | Interposed: call naming an operation absent from the offered edition. Native: model invokes an unknown tool name | Interposed: App-side *not offered*, never dispatched. Native: supplier/host response relayed with reporter; *missing* only on a host statement; never *not exposed* | AC-001 / VER-001 |
| XF-11 Read parity and basis | T3 over X | Content, subject identities ⟨S-1…S-4@r12⟩, standing and basis B1 = FX-W1/g1/r12/⟨v12⟩/⟨m-fx⟩ identical to H and E; operation identity OP-C1 v1 named via the mapping | AC-001 / VER-001 |
| XF-12 Non-mutating checks | T4 (OP-C3) and T4a (OP-C12) over X | T4: agent findings (A3), never "checked" or a host check; T4a: "host check failed: support spacing" with basis r12; neither refused stale | AC-001 / VER-001 |
| XF-13 Native hint mismatch | L-ADAPTER-3 | Catalog effects govern (change); evidence limit recorded; OP-C9 still routed as a change | AC-001 / VER-001 |
| XF-14 Stale, both bases | T5 → T6 → T7 over X | Both PR-1 items **refused — stale** per item: failing target S-3, relied B1, current B2; item-left events; no silent refresh. (Fixture per-item staleness; SWBPIPE reports whole-model staleness without failing targets, SQ-07 (d); the scope is relayed and never narrowed, R8-3) | AC-004 / VER-004 |
| XF-15 Basis-citation check | Variant of T7 in which the submission cites B2 although the agent read only B1 | Evidence limit "cited basis not observed"; interposed families may refuse to forward (App-side failure) | AC-004 / VER-004 |
| XF-16 Re-draft and queued | T9 → T10 over X | PR-2 new identity, lineage PR-1, cites B2; **queued**, reported "queued; awaiting your decision", never accepted or applied | AC-004, AC-005 / VER-004, VER-005 |
| XF-17 No retargeting | During T10, Engineer A selects S-4 in the host UI | PR-2's bound targets remain R-100, S-2, S-3 | AC-004 / VER-004 |
| XF-18 Item decisions observed | T11 → T12, observed over X | Item 1 accepted by Engineer A (host-captured A5), then applied RC-1 with resulting objects S-5, R-100; item 2 rejected (A10); A5 not lapsed by application; acts faithfully recorded with capture-evidence reference — **AWAITING INPUT** (SQ-01) for the reference — SQ-01 answered 2026-09-28: no capture-evidence reference; the Apply receipt names no person or time and does not survive restart (not offered); a SWBPIPE owner decision (PB-TBD-002; ANS §2); host joins deferred (DECISION-3). (SWBPIPE's Apply decides per batch, with no A10 record, R8-5) | AC-005 / VER-005 |
| XF-19 Retry precedence | T13 over X: acknowledgment lost; seek observation; if never received, retry with the same identity | Host answers from recorded state (item 1 applied RC-1; item 2 rejected); no stale refusal from its own effects; each submission recorded separately | AC-004 / VER-004 |
| XF-20 Lost outcome | V-OU1 over X | **outcome unknown**, observer App, last observed *accepted*; no inferred effect | AC-004 / VER-004 |
| XF-21 Restart before retry | L-ADAPTER-5 | If the host answers from a durable record: recorded state. If not: *outcome unknown*; one-effect recorded as unevidenced; under direct treatment the retry is not sent without a durable identity (PI-4) — **AWAITING INPUT** (SQ-08) — SQ-08 answered 2026-09-28: durable de-duplication not offered (session only); the durable receipt carrier is a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3) | AC-004 / VER-004 |
| XF-22 Direct without grant | OP-C4 requested directly at r13 under ⟨set-1⟩ | **not permitted**, naming P-03 policy default *propose*; never converted | AC-003 / VER-003 |
| XF-23 Direct under grant | T15 → T16 over X | Applied RC-2 with origin mark (channel external), undo route, later-check route, both settings references; **no acceptance** recorded or displayed | AC-003, AC-005 / VER-003, VER-005 |
| XF-24 Channel-level apply restriction | Variant: host states that external changes are proposal-only (RP-4) | Direct request → *not permitted* naming the host's governing treatment; displayed as a host channel rule, not as class or grant. (Variant; not SWBPIPE's behavior: SWBPIPE refuses `unsupported_method`, relayed as *not exposed on this surface*, SQ-06; R8-5) | AC-003 / VER-003 |
| XF-25 Checkpoint constraint | V-CP1 over X (FXA-5 `CP-accept`); variant with the constraint **host-held** | **Phase 1 (R8-1; EXEC CH-27):** no constraint carried or enforced; the agent proposes OP-C4 as plan guidance and adds no field the host schema lacks (R8-10); a direct request meets the host's own treatment and is recorded as observed; the requirement check is not affected by the checkpoint. **Governance phase (`CP-accept` read as if governed):** hold support **not enforceable** (SQ-02 answered 2026-09-28: route (iv)), so the workflow is *unsupported* on X. Host-held variant (test double only; not offered by SWBPIPE): **not permitted** naming {run 12, CP-accept, A5, OP-C4}; the separate proposal queues and becomes CP-accept's subject; hold support *enforced on the host route* only with an evidenced host-held route (R5-1) — Phase 1 DESIGNED; governance phase DESIGNED (test double); host variant not offered (SQ-02) | AC-003 / VER-003 |
| XF-26 Constraint only model-supplied | L-ADAPTER-9 (native carriage; SQ-02 answered with no host-held route, test-double variant); the model omits the constraint | **Phase 1:** no hold-support value; no *unsupported* for a hold reason; the omission is not a defect, because no constraint is carried (R8-1, R8-10). **Governance phase (`CP-accept` read as if governed):** model-supplied carriage does not satisfy R2-12 (R4-14; R5-2): hold support for CP-accept on X **not enforceable** (R5-1), so the workflow is *unsupported* on X ("checkpoint hold not enforceable on this surface", R4-8); if dispatched anyway, "omitted governing checkpoint constraint" evidence limit. State: DESIGNED; its precondition now holds for SWBPIPE (SQ-02 answered with no host-held route); on a host candidate **HELD** — host joins deferred (DECISION-3) | AC-003 / VER-003 |
| XF-27 Reserved entry | V-R1 over X (OP-C6 on S-1) | **not permitted** (P-02), A8 offered and not auto-recorded; entry was offered, never withheld or *not exposed* for class | AC-003, AC-005 / VER-003, VER-005 |
| XF-28 No policy basis | V-NP1 over X | Direct *not permitted*; proposal queued, confers no permission; A12 widening refused; reported **held (pending OI-021)**, never pass | AC-003 / VER-003 |
| XF-29 Narrowing in flight | ACT FX-37 over X | Queued PR-2 unaffected; unapplied direct OP-C9 request re-resolved at application → *not permitted* | AC-003 / VER-003 |
| XF-30 Accepted then stale | V-S1, observed over X | "accepted by Engineer A — not applied: refused — stale (relied B2, current ⟨B-r14′⟩)"; A5 not lapsed. (No SWBPIPE counterpart: Apply is the acceptance, so a stale Apply records no acceptance, SQ-01, SQ-23; R8-5) | AC-004, AC-005 / VER-004, VER-005 |
| XF-31 Fabrication negatives | T10 *queued*; T12 receipt RC-1; an A14 accept of the T10 submission; a model message "the engineer accepted it" | None establishes A5 or any act; each attempt to record one is non-conformant (ACT FX-01/04/05) | AC-005 / VER-005 |
| XF-32 Independent act | T2 A4 on S-2, read over X | Carried with actor, recorder, bound ⟨S-2@r12⟩, direct capture; no acceptance predecessor required; not lapsed after T6; lapsed after T14 | AC-005 / VER-005 |
| XF-33 Elicitation is not capture | L-ADAPTER-4 | Answer is conversation input to the agent, **not act evidence** (R4-12; EXEC CAP-6); never A5; host item stays *queued* until host capture | AC-005 / VER-005 |
| XF-34 A14 decline | L-ADAPTER-7 | No host request; recorded in R13 only; no host outcome; the proposal is not *refused* or *withdrawn* | AC-003 / VER-003 |
| XF-35 Disable while queued | L-ADAPTER-6 | New requests: *channel not enabled*; PR-2 stays queued in the host; App shows last observed *queued*, "channel since disabled"; never withdrawn or unknown for that reason. (SWBPIPE: no A13 facility, SQ-28; disable behavior for queued proposals not addressed, SQ-13) | AC-002 / VER-002 |
| XF-36 Data destination | L-ADAPTER-8, T3 | Read proceeds without any destination gate (D5); channel status shows destination class *user-chosen cloud* as information; run record carries the model destination (R4-1); no other destination added. Variant (not SWBPIPE's behavior: no restriction, SQ-16): the host restricts its channel by destination → the host's refusal is relayed unchanged with its rule | AC-002 / VER-002 |
| XF-37 Origin mismatch | L-ADAPTER-10 | Host mark linked, not copied; evidence limit "origin mismatch"; author identity shown unverified | AC-001 / VER-001 |
| XF-38 Undo over X | T16a → T17 observed over X | RC-2 "applied, then reversed by RC-3"; T16a A4 shown lapsed; no act erased. (SWBPIPE: Undo not exposed on the CLI; its session undo writes no receipt, SQ-10; R8-5) | AC-005 / VER-005 |
| XF-39 Generation change | Tg: read over X after restore | Bases from g1 incomparable by revision; *unknown (incomparable)*, never *unchanged* | AC-001 / VER-001 |
| XF-40 Two submissions before acknowledgment | L-ADAPTER-11 (rehearses XT XC-05 / L-XT-2) | Same identity: each submission recorded separately; neither reported *queued* before a host acknowledgment; host answers the second from recorded state; one domain effect only from domain evidence, else "one effect unevidenced". New identity on the second send: two proposals, each reported as observed; under *apply directly* a second effect is recorded, never hidden (PI-5) — **AWAITING INPUT** (SQ-08) — SQ-08 answered 2026-09-28: durable de-duplication not offered (session only); the durable receipt carrier is a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3) | AC-004 / VER-004 |
| XF-41 App restart during submission | L-ADAPTER-12 (rehearses XT XC-06 / L-XT-3) | *outcome unknown*, observer App, last observed *submitted*; channel state re-established on relaunch without silent re-enable (E-9); observation by identity precedes any resubmission; interruption recorded as an evidence limit (PI-6) — in-flight custody **AWAITING INPUT** (DEL-01-02, later undertaking, D1) | AC-004 / VER-004 |
| XF-42 Action during hold | L-ADAPTER-13 | **Phase 1 (R8-1):** the OP-C9 dispatch and its outcome are recorded, correlated to CP-accept's arrival, optionally annotated "continued past CP-accept before A5" (EXEC PH-7); never a defect; not prevented, not undone; the display never claims a hold. **Governance phase (`CP-accept` read as if governed):** the OP-C9 dispatch and its outcome are recorded as **action during hold** correlated to CP-accept's arrival; not prevented, not undone; the display never claims the run was held on X (§7.7; R4-2); HP-4: the App starts no further turn or App-initiated call for the run. State: **DESIGNED** in both phases — a recording case that needs no D6 ruling; the hold itself stays `UNRESOLVED{D6}`, closed for Phase 1 (V3-B m-9; R8-2) | AC-003 / VER-003 |

Coverage: AC-001 XF-08…13, 37, 39; AC-002 XF-01…07, 35, 36; AC-003 XF-08,
22…29, 34, 42; AC-004 XF-14…21, 30, 40, 41; AC-005 XF-04, 16, 18, 23, 27,
30…33, 38. DEL-09-09 XT rehearsal map: XC-05 → XF-19, XF-40; XC-06 → XF-19,
XF-21, XF-41; other XC rows as XT lists.
AC-006 and AC-007 are served by review of §§1, 9, 12 and this inventory
(VC-X-06, VC-X-07).

---

## 11. Interfaces expected and provided

| Direction | Counterpart | Content |
|---|---|---|
| Expect from | DEL-03-01/C-v0.6 | Nine entry elements incl. element 9; five class values; C §4.1 results with reporters and the SWBPIPE outcome mapping; read basis, subject content identities and method designation; whole-model identity receiving (R8-4); "no longer holds" rule (per item, or the host's stated scope, R8-3); §8 X column; FX-PIPE-01 |
| Expect from | DEL-03-02/P-v0.6 | Change-request elements incl. governing checkpoint constraint (governance phase) and relied-on targets; P §9 taxonomy and the §9.1 received SWBPIPE vocabulary; retry precedence; item-left events (incl. "cleared by the person, no decision record"); one route |
| Expect from | DEL-04-01/ACT-POLICY-v0.6 | A1–A14; P-01…P-06; §5.3 resolution order; §6 outcome map; V-10 external access; A13 subject |
| Expect from | DEL-04-02/AS-v0.6 | Grant display states incl. *effective (policy default)*; settings references |
| Expect from | DEL-01-01/HOSTING-BOUNDARY-v0.6 and the pin record (PIN-SPIKE-v0.1) | Supplier surfaces at 0.158.0 (§3.5); A14 origins (R7–R9); native delivery (H6) |
| Expect from | DEL-02-01 / DEL-02-03 | Checkpoint declarations (WD §4.3, with the `governed` flag, PROPOSED) and derived constraints (WD §4.2.2); Phase 1 guidance and recording (EXEC §2.1, WD §4.3.0); governance phase: hold machine and per-checkpoint hold support (EXEC §2.2, §3.6) computed from §5.3/§7.7 inputs; App holds `UNRESOLVED{D6}`, closed for Phase 1 (R8-2) |
| Expect from | DEL-09-06/RELAY-v0.3 | SQ-01…SQ-32 (this file uses SQ-01…SQ-03, SQ-06…SQ-09, SQ-11…SQ-16, SQ-28) as the single relay channel for this file's host questions (§12) |
| Expect from | External host owner (SWBPIPE) | Endpoint contract; enablement facility and its read; catalog-derived native surface and mapping; exposure on X; outcome statements; capture-evidence references; constraint receipt; identity issuance and durable de-duplication; locality; caller authentication (§12) |
| Provide to | DEL-09-09 | This account; the §10 inventory and, when executed, its candidate-bound test-double results labeled by family; the §9 register; the external requirements still missing (§12); rehearsals for XT XC-05 and XC-06 (XF-40, XF-41); never a joined-witness claim |
| Provide to | DEL-03-04 | §§1–9 for the guide's "Optional external catalog access" row |
| Provide to | DEL-04-03 | External dispatch entries (§5.1) for R7; faithfully recorded acts for R9; evidence limits for R11 (cited basis not observed; omitted constraint; origin mismatch; agent-written configuration; unverified identity; native hint mismatch; resubmission without prior observation; App-restart interruption; action during hold (governance phase) or the optional "continued past" annotation (Phase 1), with its turn initiator — person-directed / agent / App rule (R6-5); host reachable without evidenced A13 (R8-6); constraint not carriable on this host (adopted in RS R11, R8-12 item 5)); model destination per turn, run-level set observed (R5-4); A14 observations for R13 |
| Provide to | DEL-02-03 | External-channel observations (§7.7); governance phase: hold-support inputs and action during hold; required-tool outcomes on X (channel not enabled; not established; in the governance phase only, unsupported — checkpoint hold not enforceable on this surface) |
| Provide to | DEL-04-01 | Nothing open: U-X1 is closed by ACT-v0.4 §2.6; E-3/E-4 align with it |
| Provide to | DEL-01-01 | Observed MCP/dynamic-tool facts (§3.5) for the classification R4-12 assigns to HOSTING |

---

## 12. Relay questions for SWBPIPE — mapped to DEL-09-06 RELAY-v0.3

The v0.1 relay questions XQ-1…XQ-12 are consolidated, without loss, into
DEL-09-06/RELAY (v0.1 at `b4030fe4b`; cited here at **v0.3**, sha256
89b6b9c9eb14a5b356db34de202f5c8e0640707ea19524adf3fcbb01d168bdd7, read at
`816c917f0`; the SQ identifiers used here are unchanged from v0.2), which is
the single relay file
prepared for the human relay to the SWBPIPE owner (DEP-001). This file no
longer keeps its own question text; it cites the SQ identifiers. The mapping
below reproduces RELAY §3's source-to-question map for this file, plus
SQ-28, which RELAY-v0.2 added for the A13 enablement facility (R5-9).
Preparing or citing questions is not delivery, agreement or adoption.

**Answered (R8-7).** SWBPIPE answered SQ-01…SQ-32 on 2026-09-28
(`RELAY_ANSWERS_SWBPIPE.md`, #1047). The answers describe SWBPIPE's current
state; they are not commitments, and host joins are deferred (DECISION-3).
The gist column below records them for this file's questions; items SWBPIPE
marks OWNER DECISION stay open.

| v0.1 id | Subject | RELAY-v0.3 | Used here in | Answered 2026-09-28 (gist) |
|---|---|---|---|---|
| XQ-1 | Seam; catalog derivation; native-to-catalog mapping | SQ-12 | §4.1 NM-1…NM-4; OC-1, OC-8 | CLI, not MCP; hand-built and narrow; no per-operation identity or version |
| XQ-2 | Enablement: person's captured act and its capture-evidence reference; "opt-in"; channel not enabled; enablement read; disable with queued proposals | **SQ-28** (enablement facility for A13 and its capture-evidence reference; gates the whole external channel, R5-10); SQ-13 (enablement behavior) | §3.1, §3.2, E-8; OC-4; XF-01…07, XF-35 | No A13 facility (SQ-28); opt-in is a launch variable plus build feature; no *channel not enabled* code; state not readable (SQ-13) |
| XQ-3 | Constraint receipt or host-held declaration/run association; host holds before dispatch | SQ-02 | §5.3 GC-3, GC-5; §7.7; OC-7, OC-11; XF-25, XF-26, XF-42 | Route (iv), none planned; a constraint field would be refused as unknown |
| XQ-4 | Origin elements recorded and verified | SQ-14 | §5.4; OC-6; XF-37 | Controller-assigned origin; caller fields rejected; identity not verified; conversation and run not recorded |
| XQ-5 | Proposal identity minting, pre-submission availability, de-duplication order and durability, read-back | SQ-08 | §5.6 PI-1…PI-6; OC-10; XF-19, XF-21, XF-40 | Caller key, `preview_ref`, `ticket`; key lookup before basis check; session-only |
| XQ-6 | Basis descriptor, subject identities, original versus queue-time basis, per-item stale check | SQ-07; SQ-03 (a) | §4.3 RD-2, RD-5; XF-14, XF-15 | Whole-model identity and staleness; no subject identities; #885 freezes the inspected basis |
| XQ-7 | Outcome statements in P §9 / C §4.1 terms | SQ-09 | §4.5 M-1…M-7; OC-9 | Named CLI codes; mapping received per M-7 and P §9.1 |
| XQ-8 | Same grant; nature of "Apply stays in the app's human review route" | SQ-06 | §6 RP-4; XF-24 | No grants; direct external request refused `unsupported_method` |
| XQ-9 | Exposure on the external surface | SQ-11 | §4.2; XF-09 | No exposure element; one entry on the CLI; `unsupported_change` otherwise |
| XQ-10 | Captured acts with capture-evidence reference; no elicitation or prompt as act capture | SQ-01 | §7.6; XF-18, XF-33 | Only Apply is captured; no capture-evidence reference; no elicitation capture |
| XQ-11 | Data boundary — now only: does the host restrict its channel by destination, and what must the App state (D5 settles the App side) | SQ-16 | §3.4; XF-36 | No restriction; the App states nothing |
| XQ-12 | Locality; callers; sandbox reach | SQ-15; SQ-14 (callers) | E-7; OC-5, OC-6, OC-12; XF-07 | Local Unix socket, no network listener; sandbox not addressed; up to 16 callers |

Also relevant from RELAY-v0.3: SQ-04/SQ-05 (first connected activity and its
policy, `UNRESOLVED{OI-021}`) and SQ-26 (the one new operation for the
extension trace, `UNRESOLVED{OI-003}`, App v4 OI-003). SQ-04 selects nothing
(OI-021 stays open), SQ-05 records no class system and no grants, and SQ-26
records no catalog editions.

App-owner questions (not SWBPIPE): none remain. U-X1 (to DEL-04-01) is closed by ACT-v0.4 §2.6; the host side of it is SQ-28. The v0.1 question to
DEL-02-03 (U-X3) is now `UNRESOLVED{D6}`; the v0.1 question to DEL-01-01
(F-3) is ruled by R4-12; the v0.1 owner question (U-X2) is closed by D5.

---

## 13. Findings (reported; scope and other files unchanged)

### 13.1 Disposition of the v0.1 findings

| v0.1 finding | Disposition at v0.2 |
|---|---|
| F-1 "the external adapter carries it" | **Ruled by R4-14**: set-wide carriage-assurance wording; model-supplied alone does not satisfy R2-12. Applied here in §5.1, §5.3 |
| F-2 AC-002 "no host request" reading | **Ruled by R4-13** (VER-002 reading). Applied in E-2 |
| F-3 HOSTING MCP surfaces; elicitation | **Ruled by R4-12**: user-input and elicitation answers are not act evidence; HOSTING classifies the MCP config/status/call surfaces and App-initiated `mcpServer/tool/call`. Applied in §3.5, §7.6 |
| F-4 A13 App-side locus | **Ruled by R4-13** (App-side configuration never A13 evidence); the capture locus stays U-X1 with DEL-04-01. Applied in E-3, E-4 |
| F-5 ACT FX-25 wording | **Ruled by R4-17** (DEL-04-01 applies) |
| F-6 SoW OUT-001 and an App-side proxy | Moot for this increment: interposition is not adopted (R4-2). Kept in OC-2 |
| F-7 C §4.1 App reporter of *channel not enabled* | **Ruled by R4-16**. Applied in §3.2 |
| F-8 author identity *unverified* | **Ruled by R4-15**. Applied in §5.4 |
| F-9 dynamic tools and the familiar set | Stands as register context (OC-2); not adopted (R4-2) |
| F-10 SoW OI-001/OI-002 text | Carried to C1 (R4 "Carried to closeout C1") |
| F-11 register rows | Carried to C1 (R4 "Carried to closeout C1": W8 F-11) |
| F-12 no data-boundary owner | **Closed by D5** (R4-1) |

### 13.2 New findings at v0.2

- **F-13 SoW REQ-003/AC-003/VER-003 "checkpoint wait" on the external
  channel.** REQ-003 says "Workflow checkpoints retain their required human
  act" for enabled external requests, and VER-003 asks to exercise a
  "checkpoint wait". Under D6 the App claims no hold on X (GC-5); the only
  enforcement available is host-side (SQ-02), and otherwise the workflow is
  *unsupported* on X. VER-003's checkpoint case can therefore be exercised
  only as "hold support reported; action during hold recorded", not as an App
  wait. Suggest carrying this with DEL-02-03 F-10 to C1, with D6 as its home.
  *R8 note:* under the phasing, VER-003's "checkpoint wait" is a
  governance-phase case; the SoW wording that assumes the run waits is
  carried to the successor SoW route as a proposal, and no SoW is edited
  (R8-11 item 4; EXEC F-29).
- **F-14 SoW REQ-002 wording after D5.** REQ-002 asks the adapter to "carry
  the selected local/privacy data boundary without treating enablement as
  permission for another data destination". D5 settles the App side as user
  flexibility (no gate). The SoW text should point to DECISION-2 at C1; this
  design applies D5 and keeps "no added destination" (§3.4).
- **F-15 RELAY-v0.1 text predating DECISION-2.** SQ-16 still records D5 as
  "pending; not ruled" and asks whether "only App conversations using a local
  model" are allowed; SQ-02's "App assumes meanwhile" and DEL-09-09 XT XC-01
  (IN-14 "D5 pending") and XC-10 ("XF-26 HELD (U-X3; D6 pending)") likewise
  predate D5/D6 and still cite U-X2/U-X3. Suggested: SQ-16 asks only whether
  the host restricts its own channel and what, if anything, the App must
  state; XT XC-10 cites XF-26 as HELD on `UNRESOLVED{D6}`.
- **F-16 EXEC-v0.1 §3.6 "held after observation" relies on HP-2.** R4-2
  says no draft relies on `turn/interrupt`. For the external channel this
  file reports no App hold at all (§7.7). DEL-02-03 should confirm which
  hold-support values remain reachable in App runs under D6 (likely only
  *enforced on the host route*, *not enforceable* and *not established*).
- **F-17 Observation-before-resubmission is guidance only on X.** With no
  App code on the dispatch path, PI-2 (seek observation before any retry)
  cannot be enforced; the App records a violation as an evidence limit. XT
  XC-06 expects the order; its expected result should admit the recorded
  violation.

---

### 13.3 New findings at v0.3

- **F-18 (closed under R6: EXEC-v0.3 HS-3 aligned) EXEC-v0.2 §3.6 value names and mapping are superseded by R5-1.**
  EXEC-v0.2 names "host-enforced for host operations" and maps a
  model-supplied constraint to *not established*; R5-1 names *enforced on the
  host route* and maps model-supplied-only carriage to *not enforceable*.
  This file follows R5-1 (GC-3). EXEC-v0.3 is expected to align; if it does
  not, the two will disagree on XF-26.
- **F-19 (closed under R6: confirmed by EXEC-v0.3 HS-3 and R6-5) "Not established" versus "not enforceable" depends on the state of
  SQ-02, not on the carriage alone.** Before SQ-02 is answered, a checkpoint
  whose constraint can only be model-supplied today is still *not
  established* (the host might yet hold it). Only once SQ-02 is answered
  with no host-held route does it become *not enforceable*. GC-3 states this
  split; R5-1's example ("a constraint carried only as model-supplied") is
  read as the answered case. The integrator may wish to confirm this reading.
  *Applied (R8-2):* SQ-02 was answered with no host-held route, so the
  value is *not enforceable* against SWBPIPE (a governance-phase value).
- **F-20 SQ-28 gates every live external case.** Without a host enablement
  facility with a capture-evidence reference, the channel cannot be evidenced
  as enabled, so every live XF host variant and every DEL-09-09 XC case stays
  AWAITING INPUT (R5-10). No App-side substitute exists (ACT-POLICY-v0.6 §2.6).
  *Confirmed by SQ-28 (R8-6):* SWBPIPE has no facility and none is planned.
- **F-21 Per-turn destination recording depends on supplier facts not yet
  observed live** (HOSTING-BOUNDARY-v0.6 §8.3: requested and effective destination
  and `model/rerouted` are generated-type facts only; U-19 there). Until
  observed, per-turn destination entries may be *unknown*; the run-level
  set is then partial and says so.

### 13.4 New findings at v0.4 (R8)

- **F-22 Channel state and request reason can differ under R8-6.** Against
  a host with no A13 facility, a request can observe `controller_unavailable`
  (reported *endpoint unavailable*) while the channel state stays
  *disabled*. §3.2's *endpoint-unavailable* row presumes an enabled channel.
  This file records the combination (§3.2 SWBPIPE paragraph) without adding
  a channel state. **Ruled by R8-12 item 4:** the channel state (*disabled*)
  and the request outcome (*endpoint unavailable*) are different facts and
  are shown together; no new channel state is added.
- **F-23 Proposed evidence-limit labels.** "Host reachable without
  evidenced A13" (R8-6) and "constraint not carriable on this host" (I2
  R8-Q12, which R8-10 adopts only as "the agent never adds fields the host
  schema lacks") were passed to DEL-04-03 (RS R11) as labels to adopt.
  **Ruled by R8-12 item 5:** both are adopted in RS R11; the second is backed
  by R8-10's principle.
- **F-24 Whole-model identity and RD-2.** RD-2 calls a read lacking subject
  identities *basis incomplete*. Under R8-4 a whole-model identity stands
  for every covered subject, so a SWBPIPE read is citable with that identity
  and per-subject identities recorded *not supplied*. This reading follows
  R8-4; C §5.2 rule 1 is not amended here. **Ruled by R8-12 item 6:** under
  R8-4 a whole-model identity satisfies RD-2 for a host that supplies only
  that, so a SWBPIPE read can be cited (RD-2).

---

## Changes from v0.1

v0.1 = ADAPTER-v0.1 (sha256 58b2409ca45ceea66160eb8910ca38b76b6f335dc184eaeb0896e93cabd0a074, 944 lines, committed at `e20a3ae8d`). Sweep A1 under R4 (commit `f05c7e4cd`) and DECISION-2.

| R4 ID / source | Change |
|---|---|
| **R4-1** (D5; this file's F-12, U-X2) | New S-X11. §3.1 "Data-boundary statement" → **Model destination** (information, not a gate; recorded in the run record, shown in channel status). E-6 rewritten: enablement not gated on destination. §3.4 rewritten: content may flow to the selected model, cloud included; no gate; shown and recorded; no added destination; host may restrict its own channel (relayed, SQ-16); V4-HOST-02 governs the host's embedded agent. U-X2 closed; replaced by a host-input row (SQ-16). XF-05, XF-36 (no longer HELD), VC-X-02, §8 S-1 updated. F-14 (SoW wording) added |
| **R4-2** (D6; this file's U-X3, GC-3, GC-5) | New S-X12. §2 "When an adapter is needed" narrowed: no interposed App code adopted; interposed families register-only (OC-2, OC-11 annotated). §5.1/§5.2: App-assured marked not adopted; "Adopted in this increment" row added. GC-3 now routes to per-checkpoint hold support (EXEC §3.6) — *enforced on the host route* or *not enforceable* → *unsupported* (R4-8). GC-5: no App hold claimed; HP-1 and HP-2 not adopted; HP-3 best effort only; **action during hold** recorded. §7.7 extended (hold-support inputs; action during hold; no hold claim). U-X3 → `UNRESOLVED{D6}`. New L-ADAPTER-13, XF-42; XF-25, XF-26 re-expressed; §1 and §11 DEL-02-03 rows updated. F-13, F-16, F-17 added |
| **R4-13** (this file's F-2, F-4) | E-2 labeled INTEGRATION R4-13 with the VER-002 reading; E-3 rewritten: App-side configuration an agent could write is never A13 evidence; E-4: App-side A13 capture only through a control meeting EXEC CAP-2…CAP-4, locus per DEL-04-01 (U-X1). §3.1 rows, OC-4, VC-X-02 updated |
| **R4-14** (this file's F-1) | §5.1 carriage-assurance vocabulary marked INTEGRATION R4-14 (set-wide wording); constraint row: model-supplied alone does not satisfy R2-12; GC-3 cites R4-14; new S-X13; VC-X-08 updated |
| **R4-20** (DEL-09-09 XT F-4) | New L-ADAPTER-11 (two sends before any acknowledgment; aligns with XT L-XT-2) and L-ADAPTER-12 (App restart; aligns with XT L-XT-3); new PI-5, PI-6; new XF-40, XF-41; XT rehearsal map added under §10.2 coverage; VC-X-04 extended; UNRESOLVED gains App-restart custody (DEL-01-02, later) |
| R4-12 (this file's F-3) | §3.5 elicitation row and §7.6: user-input and elicitation answers are not act evidence (EXEC CAP-6); XF-33 wording |
| R4-15 (this file's F-8) | §5.4: *unverified* is an explicit author-identity value, with the RS R11 limit |
| R4-16 (this file's F-7) | §3.2 reporter column cites R4-16 |
| R4-17 (this file's F-5) | Recorded as ruled (DEL-04-01 applies) |
| R4-11 | §11 record inputs to DEL-04-03 add model destination and action during hold, plus resubmission-without-observation and App-restart limits |
| R4-8 | GC-3 and XF-26 use the *unsupported* reason "checkpoint hold not enforceable on this surface" |
| R4-19 | R3 and R4 cited in Basis; v0.2 Consumed inputs added (EXEC-v0.1, RELAY-v0.1, XT-v0.1) |
| Coordinator: RELAY SQ mapping (commit `b4030fe4b`) | §12 replaced by the XQ → SQ map (RELAY-v0.1 §3); every XQ reference in the body re-pointed to its SQ; §9 register gains a Relay column; §11 adds DEL-09-06 |
| Findings | §13 split into v0.1 dispositions (13.1) and new findings F-13…F-17 (13.2) |

Identifiers: all v0.1 identifiers kept (E-1…E-9, NM-1…NM-4, RD-1…RD-5, M-1…M-6, GC-1…GC-5, PI-1…PI-4, RP-1…RP-6, OC-1…OC-12, XF-01…XF-39, L-ADAPTER-1…10, VC-X-01…08). Added: S-X11…S-X13, PI-5, PI-6, L-ADAPTER-11…13, XF-40…XF-42, F-13…F-17. Retired: XQ-1…XQ-12 as question text (mapped to SQ), U-X2 (closed by D5), U-X3 (now `UNRESOLVED{D6}`).

---

## Changes from v0.2

v0.2 = ADAPTER-v0.2 (sha256 a2905dda5782d7a48fa35ef7e26b0c1517fd3bd995e3ddbba27d2426a25674bc, 1,015 lines, committed at `cc58211c5`). Final alignment pass under R5 (commit `8fb51f07f`) and the V3-A/V3-B reviews.

| R5 ID / source | Change |
|---|---|
| **R5-1** (V3-B MAJOR-5; this file's F-16) | Hold support uses only the four R5-1 values (*enforced by the host loop*, *enforced on the host route*, *not established*, *not enforceable*). GC-3 rewritten as a three-row table: SQ-02 answered and evidenced → *enforced on the host route*; SQ-02 unanswered (today) → *not established*; answered with no host-held route, constraint only model-supplied → *not enforceable* → *unsupported*. *Enforced on the host route* is never assumed. GC-5 rewritten: host-operation kind (a) → *not established* until SQ-02 (d); App-only checkpoints → *not enforceable* whatever SWBPIPE answers (R5-10). v0.1 values *enforced before dispatch* / *held after observation* retired (§7.7). S-X12, §2, OC-11, XF-25, XF-26, the D6 UNRESOLVED row and VC-X-03 aligned. F-18, F-19 added |
| **R5-2** (V3-B MAJOR-1, Y-1, Y-8) | §5.1 carriage assurance given its final definition: host-held = originates host-side (declaration copy or run association the host holds, or the host loop's derivation); a constraint merely **received** keeps its source's assurance; App-assured **not available** (R4-2); only host-held satisfies R2-12. S-X13, the constraint row and VC-X-08 aligned |
| **R5-4** (V3-A m-11; V3-B m-1) | Attribution relabelled: "content may flow to the selected model; no gating" = SETTLED (DECISION-2 D5); "record and show the destination" = **INTEGRATION (DECISION-2 reading)**. Recording made per turn (requested and effective separate, reroutes, unobserved turns *unknown*), run-level value = set observed, a switch starts no new run (HOSTING-v0.4 §8.3). S-X11, §3.1, §3.4, E-6, VC-X-02 updated. F-21 added |
| **R5-5** | §7.7: the person's own operations, including the person's own undo, are never recorded as action during hold; an undo never re-holds an A5 arrival |
| **R5-9** (V3-B m-4, Y-7) | SQ-13 → **SQ-28** for the A13 enablement facility and its capture-evidence reference (§3.1, OC-4, §12 map, UNRESOLVED); SQ-13 kept for enablement behavior. Body citations re-pointed to current sibling versions (C-v0.4, P-v0.4, ACT-POLICY-v0.4, AS-v0.4, RS-v0.4, WD-v0.4, LOOP-v0.4, HOSTING-v0.4, EXEC-v0.2, RELAY-v0.2, XT-v0.2); the §9 relay column and §11 cite RELAY-v0.2; verification cases name the versions actually used. Fixture assumptions cited as **FXA-n** (§10 preamble, XF-25). F-20 added |
| R5-10 (V3-B Y-9, MAJOR-4) | SQ-28 recorded as gating the whole external channel (§3.1, OC-4, VC-X-02); App-only checkpoints recorded as a separate D6 follow-up that SQ-02 cannot resolve (GC-5, D6 row) |
| V3-B m-5 | HP-4 (the App initiates nothing for a holding run, including App-initiated `mcpServer/tool/call`) and HP-H (host-side hold) added to S-X12 and GC-5 |
| V3-B m-9 | XF-42 stated **DESIGNED** (a recording case); the hold itself stays `UNRESOLVED{D6}` |
| ACT-v0.4 §2.6 (R4-13, PROPOSED by DEL-04-01) | U-X1 closed: A13 on the host interface is captured by the host's enablement facility; the App-side configuration change is an ordinary configuration change, not a second A13 (E-1, E-4, §3.1, §11, §12). The UNRESOLVED row is replaced by the SQ-28 host input |
| **R6-1** (in place; V4-A MAJOR-1/2; V4-B m-4(a)) | New "classification by held actions" bullet before GC-3: all held actions host operations → HS-3 by SQ-02 status; any App-side held action → *not enforceable* (HS-5); HS-1/HS-2 and precedence unchanged. GC-3 states it applies only when every held action is a host operation. GC-5 rewritten by held actions: a kind (b)/(c) run halt is HS-5 only when its held actions include any App-side step; a run halt holding only host operations is HS-3; GC-3 covers A5 (row corrected in place by R7-1) |
| **R6-5** (in place; V4-B m-2) | GC-3 and VC-X-03 state that model-supplied carriage → *not enforceable* only once SQ-02 is answered with no host-held route; before that, *not established*. §11 R11 action-during-hold input carries the turn initiator (person-directed / agent / App rule) |
| R6-3 (in place) | §7.7 notes what "held" means per value |
| V4-B m-4 (in place) | (b) §11 model destination per turn (R5-4); (c) F-18 and F-19 marked closed; (d) S-X13 and §5.1: a received constraint verified against the host's own copy is host-held (R5-2) |
| V4-B m-6 (in place) | §12 heading and relay citations re-pointed to **RELAY-v0.3** (sha256 89b6b9c9…, `816c917f0`); SQ identifiers unchanged |
| V4-B m-9 (confirmed) | XF-42 stays stated **DESIGNED** |
| **R7-1** (in place; V5 MAJOR-1) | GC-5 HS-5 bullet: the pre-R6 exception for a kind (b)/(c) run halt "other than an A5 constraint" is replaced by "a kind (b)/(c) run halt whose held actions include any App-side step. A run halt holding only host operations is HS-3, above; GC-3 covers A5." GC-5 now agrees with the classification bullet, its own HS-3 bullet, EXEC §3.6 HS-3, ACT `CP-L4` and AS F6d. The R6-1 row above is corrected to match. No value recomputed in V5 §3 changes; a run halt holding only host operations takes HS-3 (*not established* today), as EXEC §3.6 already states |
| Header | v0.3; supersession chain; R5, V3-A, V3-B and the current sibling texts added to Basis/Consumed inputs with hashes; R5 successors not read and noted as such |

Identifiers: all v0.2 identifiers kept. Added: F-18…F-21 (§13.3). Closed: U-X1 (by ACT-v0.4 §2.6). Retired: the v0.1 hold-support values.

---

## Changes from v0.3

v0.3 = ADAPTER-v0.3 (last changed at `c6f81a4f2`; unchanged at `94aa9181b`;
sha256 8ef2126df2b9afff0a70b36e5b4eed8492eaae0baf6563ce422d3b9d05170f5a). R8
pass (node A3). Keyed by R8 ID. Sources are I2 rows of INTAKE_MAP.md (`nn.k`,
`P2.n`, Part 2.2, Part 3/4 items); R8 overrides I2 where they differ.

| R8 ID (I2 source) | Change in v0.4 | Where |
|---|---|---|
| **R8-1** (DECISION-4 D4-1) | Phase framing: checkpoints are plan guidance in Phase 1; the constraint, carriage assurance (S-X13), GC-1/GC-3/GC-5, hold support and *action during hold* are relabelled **governance phase (retained)**, with a Phase-1 statement beside them (§5.3 phase paragraph; §7.7 Phase 1 paragraph: arrivals and acts recorded, optional "continued past ‹checkpoint› before ‹act›", no hold claimed). S-X10 and S-X12 restated. RP-3's constraint row, §5.1's constraint row, §8 S-3 and §11 marked governance phase. V4-WF-05's first half recorded as phased | Header, §0, S-X10, S-X12, S-X13, §1, §2, §5.1, §5.3, §6, §7.7, §8, §11 |
| **R8-1** (cases; P2.10, P2.11, P2.15) | XF-25, XF-26 and XF-42 take the two-part form (Phase-1 result; governance-phase value, reading `CP-accept` as if governed). XF-25: "Today: not established" → governance phase **not enforceable** → *unsupported*; state DESIGNED (test double), host variant not offered. XF-26: precondition now holds for SWBPIPE; on a host candidate HELD (DECISION-3). V-CP1 over X restated | §5.3, §10.2 |
| **R8-2** (02.13; P2.15, P2.17; §2.2 ADAPTER rows) | SQ-02's answer recorded as a governance-phase input. §2 outline: the answered case (*not enforceable*) replaces "while SQ-02 is unanswered". GC-3: "(the state today)" moves to the answered row (SWBPIPE since 2026-09-28). GC-5 HS-3 bullet: the answered case applies. The D6 row: closed for Phase 1 by DECISION-4, re-opening with the governance phase. OC-2, OC-11, U-P10 and F-19 updated; VC-X-03 two-part | §2, §5.3, §9, §13.3, UNRESOLVED, VC-X-03 |
| **R8-3** (07.8; Part 3 item 2) | §7.1 and XF-14: per-item staleness where the host supplies subject identities, otherwise the host's stated scope relayed unchanged and never narrowed (SWBPIPE: whole model) | §7.1, §10.2, §11 |
| **R8-4** (03.9; Part 3 item 3) | RD-2: a whole-model identity stands for every covered subject; per-subject identities *not supplied*; never App-computed (new F-24 on RD-2's "basis incomplete") | §4.3, §11, §13.4 |
| **R8-5** (06.1, 09.1, 10.3, 11.2; Part 3 items 1, 10; Part 4.4) | New **M-7** received SWBPIPE vocabulary (pointing to P §9.1): `unsupported_method`/`unsupported_change` → host-reported *not exposed on this surface*; `validation_rejected` → *refused — invalid* at application; `withdrawn` → item left, "cleared by the person, no decision record"; neither A10 nor A11; `outcome_unknown`, `expired`, `retryable`/`next_action` as stated. RP-4 records SWBPIPE's `unsupported_method` and R2-4 as not met. RP-6: undo not on the CLI, no receipt. XF-09, XF-24, XF-30, XF-38 annotated | §4.5, §6, §10.2 |
| **R8-6** (13.1, 13.2, 28.2; P2.18; Part 3 item 4) | A13 stays reserved. §3.1: SWBPIPE has no enablement facility. §3.2: state *disabled* ("host has no A13 facility"), not *unconfirmed*; new SWBPIPE enablement paragraph: launch variable plus build feature is not a captured act; `controller_unavailable` → *endpoint unavailable*, channel *disabled*; host answer without evidenced A13 → evidence limit; live host variants keep AWAITING INPUT with "answered: not offered; host joins deferred (DECISION-3)"; R8-Q4b deferred to the owner. E-1, E-8, §8 S-1, OC-4, XF-02, XF-06, XF-35, F-20 and the SQ-28 UNRESOLVED row updated; new F-22 | §1, §3.1–§3.3, §8, §9, §10, §13, UNRESOLVED |
| R8-7 (01.9, 01.10, 08.2–08.4, 12.1, 14.3, 15.1, 16.1, X.6; Part 3 items 11, 12; Part 4.11) | Standings move to **answered**: §12 map gains an answer-gist column; OC-1, OC-5…OC-10 evidence cells record the answers; PI-2 and PI-4 cite SQ-08; §5.4 cites SQ-14; §9 records PR #885 as deferred with the owner's activation in force. XF-18, XF-21 and XF-40 keep AWAITING INPUT with the STD-2 annotation. The SQ-16 row is closed (no restriction). Capture-evidence and proposal-identity rows re-owned to SWBPIPE owner decisions. "App v4 OI-003" qualified | §0, §1, §3.4, §4.1, §5.4, §5.6, §9, §10.2, §12, UNRESOLVED |
| **R8-10** (12.1; Part 4.7; Part 5 R8-Q12) | NM-2: SWBPIPE supplies no mapping and no per-operation identity or version, so every requirement on X is *not established* against it. Strict preflight: the agent never adds fields the host schema lacks (§2, §5.1, §5.3); GC-4's Phase-1 evidence limit "constraint not carriable on this host" carried as PROPOSED (new F-23) | §2, §4.1, §5.1, §5.3, §13.4 |
| R8-11 (items 1, 2, 4, 5) | S-X10: D2's reserved-act half binds in Phase 1 (host-enforced); its declared-checkpoint half, WD I-7 and V4-HI-42 are Phase-1 guidance. §7.7: a lapse is recorded in Phase 1 and nothing re-holds. F-13: VER-003's checkpoint-wait wording is carried to the successor SoW route as a proposal. Governance-phase values read the fixture's checkpoints as if declared governed | S-X10, §5.3, §7.7, §10, §13.2 |
| **R8-12** (items 4, 5, 6, 7; closing pass, node A6, in place) | Item 4: F-22 ruled — channel state *disabled* and request outcome *endpoint unavailable* are different facts, shown together; no new channel state (§3.2 already so). Item 5: F-23 ruled — both evidence-limit labels adopted in RS R11; GC-4 and §11 drop "PROPOSED" for "constraint not carriable on this host". Item 6: F-24 ruled — a whole-model identity satisfies RD-2 for a host that supplies only that, so a SWBPIPE read can be cited; RD-2 says so. Item 7: consumed inputs list the post-R8 sibling versions; body citations of ACT §2.6 and HOSTING §8.3 and the §11 ACT/AS/HOSTING rows name the current versions (closure history of U-X1 kept) | Header, §3.1, §3.3, §3.4, §4.3 RD-2, §5.3 GC-4, §9, §11, §13 |
| V9 N-2 — in place | §3.4 V4-HOST-02 bullet carries the "pending owner clarification (R8-9)" marker the other files carry. Wording otherwise unchanged |

Identifiers: all v0.3 identifiers kept. Added: **M-7**, F-22…F-24 (§13.4). Closed: the SQ-16 host-restriction UNRESOLVED row. Body citations of C and P re-pointed to C-v0.6 and P-v0.6 (identifiers unchanged).

---

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| TBD-007 choices OC-1…OC-12 (§9): transport family, realization family, configuration locus, enablement loci, locality, authentication, carriage mechanism, native-surface derivation, encoding, read-back, hold mechanism, tool-permission interplay | App external-host integration owner with external host owner (OC-4 with DEL-04-01; OC-11 with DEL-02-03) | Before the App receiving implementation depends on the interface, and before DEL-09-09 qualification | Nothing selected; carriage assurance and hold feasibility stated per family. SWBPIPE: CLI; any MCP adapter is a SWBPIPE owner decision (modern-client condition) |
| SQ-28 Host enablement facility for A13 and its capture-evidence reference (U-X1 closed by ACT-v0.4 §2.6, PROPOSED under R4-13) | SWBPIPE owner decision (A13 enablement facility; ANS §2). Owner, deferred (R8-Q4b): whether a person-set launch environment variable counts as A13 evidence | Before enablement implementation, VER-002 and **any** live external-channel case; when the owner resumes UI-SUCCESSOR (DECISION-3) | Without it no enablement is evidenced and the channel stays *disabled*; XF-01…XF-05 host variants **AWAITING INPUT** — SQ-28 answered 2026-09-28: no facility (not offered); a SWBPIPE owner decision (ANS §2); host joins deferred (DECISION-3) |
| `UNRESOLVED{D6}` App-side run holds on X: constraint assurance for A5 checkpoints (GC-3) and holds before dispatch (GC-5); formerly U-X3. **Closed for Phase 1** by DECISION-4 (R8-2); re-opens only when the governance phase is taken up | Owner (DECISION-2 D6; DECISION-4). SWBPIPE answered SQ-02 on 2026-09-28: route (iv), none planned (planning one is a SWBPIPE owner decision); App-only checkpoints are the same D6 follow-up (R5-10; EXEC U-E23); DEL-02-03 computes hold support | When the governance phase is taken up for a workflow that needs it; before governance-phase hold-machine fixtures on X; before XF-25/XF-26 execution on a host | Phase 1: no hold, no hold-support value, no *unsupported* for hold reasons; optional "continued past" annotation. Governance phase: no App hold claimed; host-operation checkpoints *not enforceable* against SWBPIPE (HS-3 (c)), App-only ones *not enforceable* (HS-5); action during hold recorded (XF-42 DESIGNED) |
| ~~Host channel restriction by model destination, if any (SQ-16)~~ **Closed** (R8-7): SWBPIPE answered SQ-16, no restriction; the App states nothing | — | — | None on App gating (D5). (U-X2 closed by D5) |
| U-P10 Host receipt of the governing checkpoint constraint, or host evaluation of its own declaration copy (SQ-02) — governance phase (R8-1) | Host owner with DEL-03-02, DEL-05-01, DEL-03-03 (DEP-001). SWBPIPE answered SQ-02: route (iv), none planned (a SWBPIPE owner decision) | Before the governance-phase V-CP1 / XF-25 execution on a host | Phase 1: none. Governance phase: XF-25 DESIGNED against a test double; host variant not offered (SQ-02); host joins deferred (DECISION-3) |
| Capture-evidence reference for host-captured acts (R2-20; SQ-01) | SWBPIPE owner decision (PB-TBD-002 acceptance-record storage; DEL-16-03 actor identity; ANS §2) | Before XF-18 positive case and any host-content checkpoint *performed* | Faithful records are record shapes only until then. SQ-01 answered 2026-09-28: none; XF-18 AWAITING INPUT with the STD-2 annotation |
| Proposal identity minting, pre-submission availability, de-duplication order and durability across restart (SQ-08; P U-P1) | SWBPIPE owner decision (durable receipt carrier; ANS §2) with DEL-03-02 | Before direct application over X; before XF-21 | PI-4, PI-5 PROPOSED; XF-21, XF-40 AWAITING INPUT — SQ-08 answered 2026-09-28: caller key and controller ticket, key lookup before the basis check, session-only (durable de-duplication not offered); host joins deferred (DECISION-3) |
| Caller identity verification (OC-6; SQ-14) | App owner with host owner | Before origin conformance | Author identity *unverified*. SWBPIPE (SQ-14): not verified; a local capability in a 0600 descriptor |
| Enablement read and disable behavior for queued proposals (SQ-13) | Host owner | Before XF-35 execution | E-8 PROPOSED. SWBPIPE (SQ-13): state not readable; disable behavior for queued proposals not addressed |
| Native-to-catalog mapping and derivation (OC-8; SQ-12) | Host owner with DEL-03-01 | Before AC-001 claim | NM-2: *not established* without a mapping. SWBPIPE (SQ-12): hand-built; no mapping and no per-operation identity or version (R8-10; C U-C13) |
| App restart: custody of an in-flight native item across relaunch (PI-6) | DEL-01-02 (later undertaking, D1) | Before XF-41 execution | Interruption recorded as an evidence limit; outcome unknown |
| Supplier behaviors `not-observed` at 0.158.0: per-thread MCP configuration; App-added call metadata; MCP-call A14 path; supplier behavior on MCP call failure or retry; sandbox effect on MCP stdio servers and local-socket CLIs | DEL-01-01 with App implementation owner | Before implementation; at pin re-examination (D4) | §3.5 facts are generated-type facts only |
| `UNRESOLVED{OI-003}` (App v4 OI-003; unrelated to SWBPIPE's OI-003) extension promise | Owner with host contract owner | Before claiming extension or fixing AC-007's criterion | NM-4: mapping work is evidence, not disposition |
| `UNRESOLVED{OI-021}` first connected operation, its autonomy, operation-specific additions | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and live examination | All cases on invented FX-PIPE-01; OP-C11 cases held |
| `UNRESOLVED{OI-013}` / `UNRESOLVED{OI-014}` placement (including any shared catalog-schema checker, LOOP §10.2 (b)) | Shared contract owner with SWB implementation owner / App-shared contract owners | Before structural/production allocation | No placement implied |
| Host adoption of D2, D3, P-01…P-06 and R2 treatments on X (DEP-001) | Host owner / SWBPIPE | Before any host-enforcement claim (VER-003) | All treatment behavior is receiving meaning. SWBPIPE (SQ-05): no class system, no named reserved list; every change waits for the person's Apply; autonomy is SWBPIPE owner decision OI-016 |
| Consequence vocabulary (ACT U-02) | DEL-04-01 with host policy owner | Before a consequence scope dimension is used | Fixtures use model/workspace + object set only |
| Register rows (F-11), SoW OI text (F-10), SoW REQ-002/REQ-003 wording after D5/D6 (F-13, F-14) | Register owner / closeout C1 | C1 | None on content |

---

## Verification cases

Designed, **not run**. Evidence labels per the C-v0.6 mapping. Every executed
result names the App candidate, the realization family, the endpoint
(*simulated* or an identified host candidate), the contract versions
actually used — current at this revision C-v0.6, P-v0.6, EXEC-v0.4 and
WD-v0.6, with ACT-POLICY as then current — and the policy records used
(R5-9).

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-X-01 Receiving comparison | For the selected family, run XF-08…13, 37, 39 against the simulated endpoint; compare identity/version (via mapping), availability reasons, standing, basis and subject identities with C-v0.6/P-v0.6 expectations | Every element preserved; mapping named; hints and Codex exposure never used as catalog elements; endpoint labeled simulated | VER-001 (AC-001) |
| VC-X-02 Enablement and locality | Run XF-01…07, 35, 36; inspect App configuration changes and every request destination the App makes | Read per R4-13 (SQ-28 gates every live case): "no host request" applies to the App's own requests, and the host's refusal is the authoritative off. Disabled: no App request; host *channel not enabled* relayed; App-side (including agent-written) configuration never A13 evidence and never enables; enablement leaves grant display unchanged; endpoint local; no destination added; model destination recorded per turn (requested and effective separate, reroutes, unknown turns) and shown as information, never gating (no-gate SETTLED D5; record-and-show INTEGRATION, R5-4); supplier-initiated traffic attributed to the supplier. SWBPIPE forms (R8-6): no A13 facility, so *disabled*; `controller_unavailable` → *endpoint unavailable*; a host answer without evidenced A13 → evidence limit, never *enabled* | VER-002 (AC-002) |
| VC-X-03 Same route and policy | Run XF-22…29, 34, 42 under the identified adopted records (P-01…P-06, ⟨set-1⟩, ⟨set-2⟩); inspect App code/configuration for any path that applies outside the host route | Every outcome per RP-3; no conversion; reserved entries offered; no bypass route found; checkpoint cases: in **Phase 1**, no hold-support value, no *unsupported* for a hold reason and no hold claimed, with the optional "continued past" annotation (R8-1); in the **governance phase**, hold support in the four R5-1 values only (*not enforceable* for CP-accept on X against SWBPIPE, SQ-02 answered with no host-held route (R6-5; R8-2), and for any checkpoint holding an App-side action (R6-1); *enforced on the host route* never assumed) and action during hold recorded, with no App hold claimed (D6); host-enforcement claims deferred to host evidence | VER-003 (AC-003) |
| VC-X-04 Adverse outcomes | Run XF-14…21, 30, 40, 41 with an injected intervening edit, later selection, duplicate submission (including two sends before any acknowledgment), lost acknowledgment, endpoint restart and App restart | Stale with both bases; no retarget; retry answered from recorded state; *outcome unknown* observer App; no one-effect claim from transport or session de-duplication; durable conclusions deferred to DEL-09-09 | VER-004 (AC-004) |
| VC-X-05 Acts | Run XF-04, 16, 18, 23, 27, 30…33, 38; inspect the act-mapping code/configuration | No act from success, queued, receipt, A14, A8, elicitation or model text; positive faithful record with actor ≠ recorder, bound content identity and capture-evidence reference (AWAITING INPUT until supplied); independent A4 kept without acceptance | VER-005 (AC-005) |
| VC-X-06 Documentation review | Check §1 one-for-one against SoW REQ-005 exclusions; check §§3–9 and UNRESOLVED against OI-001/002 (as ruled by DECISION-1), OI-003/013/014/021, DEP-001, TBD-007 and CLM-001…004; check D2/D3 attribution (R2-11) and markings | Every excluded act has its owner; every open item has owner, point of need and effect; no wire field, transport, common service or host-delivery claim; PR #885 cited as evidence only | VER-006 (AC-006) |
| VC-X-07 Fixture inventory and handoff | Inspect §10 for coverage of AC-001…AC-005, labels, family, contract/policy identities and evidence limits; inspect the handoff to DEL-09-09 | Full coverage (table in §10.2); every case labeled simulated, AWAITING INPUT or HELD where applicable; generated versus adapter work stated; OI-003 not settled; the joined witness left to DEL-09-09 | VER-007 (AC-007) |
| VC-X-08 Carriage assurance | For the adopted (native) family, tabulate §5.2 against an executed dispatch of XF-16, XF-19 and XF-25 (the constraint rows in the governance phase; in Phase 1 no constraint is carried and no field the host schema lacks is added) | Each element's assurance observed matches §5.2 using the R5-2 definitions; a constraint the host merely received is model-supplied; only host-held satisfies R2-12 (GC-3); App-assured never appears; any omission recorded per GC-4 | VER-003, VER-004 (AC-003, AC-004) |
