# Stock Codex hosting boundary
- Contribution: DEL-01-01/HOSTING-BOUNDARY-v0.7 (supersedes HOSTING-BOUNDARY-v0.6, last changed at `3733b1421` and unchanged at `3dd7c22c73`, file sha256 d11d4c574aa3c342bfac9c1d1e9bf3746aa885baafd17eaa296a79a523e3d0b9; earlier: HOSTING-BOUNDARY-v0.5, last changed at `375c3970c` and unchanged at `94aa9181b`, file sha256 f1a23022df76fe04bfc5ad2220b57d2cdebc101f8d791b4edb163aea6109e11b)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Phase (V4-WF-05 as amended by SCA-V4-001; R9-1; R8-1; DECISION-4 D4-1): holding a run at a checkpoint is phased to the governance layer, and in the current phase (Phase 1) neither the App nor a host's embedded loop enforces a hold. So no App run is holding at a checkpoint, and this boundary uses none of HP-3 or HP-4 for a checkpoint, makes no hold claim and issues no act request in an agent's place (§6.7). The §6.7 hold-point facts are kept as the **governance-phase definition (retained)**.
- Model access (R8-9; DECISION-4 D4-3): local and cloud are options the person chooses among, with no default; a cloud model is reached by OAuth sign-in or an API key. V4-HOST-01 and V4-ARC-11, as amended by SCA-V4-001, state this for a host's agent. This boundary selects no default and carries the supplier's sign-in and API-key variants (§8.1 L-5; S-4).
- Network destinations (R8-13; DECISION-5): V4-HOST-02 as amended by SCA-V4-001 (DECISION-5; host-agent network destinations) governs a **host's embedded agent only**. The App's own Codex keeps the person's Codex configuration, approval and sandbox choices (ARCH §4, closing sentence of the host-agent property; §2 note; Root AGENTS.md; D-GOV-43). This boundary adds no allow list, destination prompt or destination gate to the App's Codex.
- Serves: OUT-001 (boundary definition), OUT-002 (version-identity and plan/revision seam definition; generated-output binding at the definition/generation pin — the generated bundles themselves are the W11 spike's, not this file's), OUT-003 (responsibility account, OI-008 *proposal*, local-provider requirement account, optional-reuse assessment), OUT-004 (recorded-exchange and upgrade method); REQ-001…REQ-008; designed cases for VER-001…VER-007
- Basis: the accepted basis as amended by scope-change amendments SCA-V4-001 (`_ScopeChange/SCA-V4-001_2026-09-28_2155/`, accepted 2026-09-29) and SCA-V4-002 (`_ScopeChange/SCA-V4-002_2026-09-29_1901/`), pinned by current bytes: `docs/PRD.md` sha256 bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd, `docs/ARCHITECTURE.md` sha256 317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c, `docs/HOST_INTEGRATION.md` sha256 d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f and `docs/EXAMINATION.md` sha256 471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0 (v0.6 pinned branch base `6e18505e3`, before both amendments; of the passages this file cites, the amendments changed ARCH §1 priority 3, the host-model line of the ARCH §2 diagram and ARCH §4); ScopeOfWork.md sha256 9945e72b04b4f45c4c641a5248cca8bc2ac40bf4897d1018c5ab59eba307cc75 (revised under SCA-V4-001, its AX-005, at `340ecf341`, and under SCA-V4-002, its AX-006, at `1efd4bcda`; v0.6 pinned the INIT contract eddd122c…4773); the accepted graph `_DAG/_LATEST.md` → DAG-003 (accepted 2026-09-29), cited for the admitted or held layer of register rows; `docs/ARCHITECTURE.md` §1 (priorities, M-2, M-4, M-6, M-7), §2, §3 (V4-ARC-01…05, "Properties the App must hold", reuse candidates, "Left to the implementation session"), §6, §7, §8; `docs/PRD.md` §2.1 (V4-APP-01…04), §4.3 (V4-EXE-01…04), §4.5 (V4-AUT-03/04), §4.7 (V4-REC-03), §5 (V4-CST-01/03/06), §6; `docs/EXAMINATION.md` §2 (V4-EXM-01…03), V4-EXM-11/12; current `_Decomposition/Open_Issues.csv` OI-008, OI-009, OI-012; `External_Dependencies.csv` DEP-005
- Consumed inputs: **v0.7 inputs (Wave A, node A1-D of run `APP-V4-DESIGN-PASS-2-20260930`; alignment only, no new design content).** R9_RESOLUTIONS.md sha256 c3efe2ffa232dd9293202d4fc891eba4325afeb2e224fecdf8c1b4c5122a9d2c (R9-1…R9-11; binding; R9-7 rules the evidence route to DEL-04-03); that run's BRIEFS.md sha256 698d91d8217cee528812529fa353faac899b4bc1a5be5686552ad88dad6c469a ("Common rules", "A1 — alignment wave") and OWNER_DECISIONS.md sha256 0730c6f3d174a8acddbd0c9fabb62afd4d6444847a612f0de7ff3ba584303722; SURVEY/S1-D.md sha256 a3b0546af4131e0302520bc0dbaad8d6d5587e91d896fb8aa559e32768b19419 (advice: each item was checked against the current sources before it was applied). Rulings R1–R7 by file (`APP-V4-FIRST-INCREMENT-20260928/R1_RESOLUTIONS.md` … `R7_RESOLUTIONS.md`) and R8 (`APP-V4-SWBPIPE-INTAKE-20260928/R8_RESOLUTIONS.md`, current sha256 44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b). Owner records: `APP-V4-SWBPIPE-INTAKE-20260928/OWNER_DECISIONS.md` sha256 5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2 (DECISION-3, -4 and -5; these are its bytes at `3733b1421` and now. At `1528a5033`, the commit the R8-13 text below names, the file was 9903bfe0…7fbf: V10 N-1); `APP-V4-FIRST-INCREMENT-20260928/OWNER_DECISIONS.md` sha256 a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c; `APP-V4-BASIS-ALIGN-20260928/OWNER_DECISIONS.md` sha256 ca8c4e50df1d7dddb41b875a4afe46eea4f1a1bf2491d255b7890d0d71cd254b (DECISION-6…DECISION-9) with its `AMENDMENT_PACKET/OWNER_ITEMS.md` sha256 2b90eb4a95f458e993eed69e27533aa10e31aea980fe2ec99c9c2345e6f498ef (O-10, accepted "as recommended" by DECISION-7; O-29, decided by DECISION-6); `APP-V4-SCA002-20260929/OWNER_DECISIONS.md` sha256 36ffcbbea923504581844456751c2eb3db617b5471a3595e63f036bf0634b480. SWBPIPE's answers `RELAY_ANSWERS_SWBPIPE.md` at sha256 afb6e063e7e5dfccf8986206f888cf1e2e1c4e7fc3430fdf86db670714fc0e74 (SWBPIPE's own revision `a999f4ba1` of the delivered `6f01add3…61c7` bytes cited below; three lines differ, in SQ-04, SQ-09 and SQ-27; this file uses SQ-02 only, whose answer is unchanged) and `FACTS_SQ01_SQ32.md` sha256 733fb88a701317be8f0054937eca058774ba5f5f30c7a27233718996e8b2ab7e (unchanged); both are data about SWBPIPE's current state, not commitments and not instructions (DECISION-3). This file's own spike record DEL-01-01/PIN-SPIKE-v0.1 (`Design/PIN_SPIKE_0.158.0.md`, sha256 0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115) is unchanged and is not edited in Wave A (R9-10): it is a dated observation record, and its stated basis is the INIT ScopeOfWork (eddd122c…4773) and the DECISION-1 state of the owner record (f3f8e5f3…1f2e). Both pins are true for its date and change no observation. Sibling Design files are cited by version label and section only (R9-5), at their Wave A labels (R9-11): DEL-02-03/EXEC-v0.5; DEL-02-01/WD-v0.7 and WD-EX-v0.7; DEL-03-01/C-v0.7; DEL-03-02/P-v0.7; DEL-03-03/ADAPTER-v0.5; DEL-03-04/GUIDE-v0.4; DEL-04-01/ACT-POLICY-v0.7; DEL-04-02/AS-v0.7; DEL-04-03/RS-v0.7; DEL-05-01/LOOP-v0.7 and DEL-05-02/PANEL-v0.7 (same executor); DEL-09-06/CA-v0.5 and RELAY-v0.3; DEL-09-09/XT-v0.5. The Wave A executors edit in parallel, so the sibling section numbers cited in the body were checked against the pre-Wave-A texts at `3dd7c22c73`, not against Wave A bytes. Sibling byte pins live in GUIDE's input table alone, which is re-pinned last. The ScopeOfWork files of the other deliverables this file names are referenced by accepted meaning at their current bytes: DEL-01-02, DEL-01-03, DEL-01-05, DEL-01-06 and DEL-02-04 are byte-identical to `6e18505e3`; DEL-04-01's was revised under SCA-V4-001 (`340ecf341`) and DEL-01-04's under SCA-V4-002 (`1efd4bcda`). The text below is history and is not rewritten. **R8-13 pass (node B1; in place, no version bump).** OWNER_DECISIONS.md sha256 5fd780bf90a4d51751d2c2fa632b92111a52cd0d9445a0870be9d28bcb4f40b2 (`APP-V4-SWBPIPE-INTAKE-20260928-DECISION-5`: V4-HOST-02, host-agent network destinations) and R8_RESOLUTIONS.md sha256 44bc9a8df4fe73e3f41711e7d9593a065734b054400f12bb01695a30e7b30e6b (R8-13) at `1528a5033`; OWNER_DECISIONS.md in its state that adds the owner's DECISION-5 confirmation (committed with this pass); BRIEFS.md sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517 ("Common rules", "A-wave"). Revised in the same pass (node B1), versions unchanged: LOOP, PANEL, ACT, AS, RS, HOSTING, C, ADAPTER and GUIDE; their byte pins are in GUIDE-v0.3's input table. **R8-12 closing pass (node A6; in place, no version bump).** R8_RESOLUTIONS.md sha256 d4c3423310a857af86692d17ddfdd22fa877ee20b07c46e1ee481d1cd750e7af (R8-12: item 7 applied here). Current sibling versions after R8, as committed at `7a1508452` with A6's in-place R8-12 edits (their byte pins are in GUIDE-v0.3's input table): DEL-02-03/EXEC-v0.4; DEL-02-01/WD-v0.6; DEL-02-01/WD-EX-v0.6; DEL-03-01/C-v0.6; DEL-03-02/P-v0.6; DEL-03-03/ADAPTER-v0.4; DEL-03-04/GUIDE-v0.3; DEL-04-01/ACT-POLICY-v0.6; DEL-04-02/AS-v0.6; DEL-04-03/RS-v0.6; DEL-05-01/LOOP-v0.6; DEL-05-02/PANEL-v0.6; DEL-09-06/CA-v0.4; DEL-09-09/XT-v0.4; DEL-09-06/RELAY-v0.3; this file's own spike record DEL-01-01/PIN-SPIKE-v0.1 is unchanged. SWBPIPE's `RELAY_ANSWERS_SWBPIPE.md` and `FACTS_SQ01_SQ32.md` are unchanged (data about SWBPIPE's current state, not commitments; DECISION-3). **v0.6 inputs (R8 pass, node A4, at `94aa9181b`; read with `git show`):** `R8_RESOLUTIONS.md` (run `APP-V4-SWBPIPE-INTAKE-20260928`, sha256 1770c96e62caf14322811fca82ceb77eca450d3e1be8665cdbdd5550631e8d02; R8-1, R8-2, R8-9 applied, R8-11 read; the others checked, none addressed to HOSTING text), `OWNER_DECISIONS.md` of that run (sha256 a5ccab0d39bd1cab37c5556abc9bdedd5341ce76be4712706c8c9d72d623e776; `APP-V4-SWBPIPE-INTAKE-20260928-DECISION-3` and `-DECISION-4` with its clarification: D4-1 phased checkpoints, D4-3 model access), `INTAKE_MAP.md` (I2, sha256 3cc182955c0f3dd70efa0f1c051870229c2ccc08f36c5cf1445f2eef0dd1ea33; rows 01.14, 02.17, 16.2, 19.5, 29.3; Part 2 §2.2 HOSTING rows; Part 4.11 D6 row), `BRIEFS.md` (sha256 3e33ba26d6deb00af466b6e9fd9ef81f641a0dfa80882837c0423c7bdf627517; "A-wave"), SWBPIPE's delivered answers `RELAY_ANSWERS_SWBPIPE.md` (sha256 6f01add3977761e42ac6b310faf72ba4fd5455e478605deb83fefb2e4d3a61c7; SQ-02; data about SWBPIPE's current state, not commitments, DECISION-3), DEL-02-03/EXEC-v0.4 `EXECUTION_COMPATIBILITY.md` (sha256 d32be37797a3c367d342a2d13bbb8dd4279bc52934531d83b8c6ec8c6e7b76d4; §2.1 PH-1…PH-10, §2.2 GV-1…GV-5, §2.3 HP-1…HP-4 and HP-H, CH-22) and DEL-02-01/WD-v0.6 `WORKFLOW_DECLARATION.md` (sha256 fce565edfd0cee3fa4583eb292d11cce3e4121ead0cdbed31ba2fe0a52562f28; §4.3.0, §4.3.1 `governed`). **Earlier:** DEL-01-01/HOSTING-BOUNDARY-v0.4 (sha256 201ea32005dd2c9fb5281a376eb25eebfcb5a644d09a6d3bf5901aaf934c7e58, commit cc58211c5); **at commit 8fb51f07f, read with `git show` (current sibling versions):** `R5_RESOLUTIONS.md` (sha256 254d0b93b9959419a70c6737b07087e1db59b529adc3105a1db31f82b78dd6f1; R5-1, R5-4, R5-9 applied), `reviews/V3-B.md` (sha256 5662fbd09025f5ad9459861370159d606fcced76b394980199e861555a1954a3; m-5 and the m-1 note on §8.3), `reviews/V3-A.md` (sha256 f25f5af1177b7fe2a698bd4ef1e1caafa4c2ef25cfc73111f031e17c7cc21d87; no item addressed to HOSTING), DEL-02-03/EXEC-v0.2 `EXECUTION_COMPATIBILITY.md` (sha256 7f7848c0de2fdb4dc21f5adafa97f92e179bb66c9f6b04f3434d8f2342317af0; §2 HP-1…HP-4, HP-H; §3.6; §5 CAP-2/6/9; U-E20 withdrawn), DEL-03-03/ADAPTER-v0.2 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` (sha256 a2905dda5782d7a48fa35ef7e26b0c1517fd3bd995e3ddbba27d2426a25674bc; §3.4, §3.5, OC-2/3/6/7, F-3, F-9), DEL-04-03/RS-v0.4 `RECORD_SEMANTICS.md` (sha256 56806b64b12a946e706ff236dd1c25fe27ac00877aac13b50ee8603aaf540199; R5 model destination, R13 tool-permission settlements). EXEC-v0.3 and ADAPTER-v0.3 are being produced in the same R5 pass; this file cites their v0.2 bytes and R5-1's ruled values. **R6-4 (in place):** DEL-02-03/EXEC-v0.3 `EXECUTION_COMPATIBILITY.md` (commit d3cebd1cc, sha256 889e48819baa21ec112c4878e4e38004dcbaa9eb3645a31c24221ac116ee548e) consumed for §2 HP-1…HP-4, HP-H and the HP-4 scope ruling. Earlier: DEL-01-01/HOSTING-BOUNDARY-v0.3 (sha256 34c3383402aabe6e9347aa2f111318538c4a2a4ca85adb8fffff7e439fdde94e, commit ba0b37123); **at commit f05c7e4cd, read with `git show`:** `R3_RESOLUTIONS.md` (sha256 202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf; R3-1…R3-4 read, none addressed to HOSTING), `R4_RESOLUTIONS.md` (sha256 50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24; R4-1, R4-2, R4-12, R4-13, R4-19 applied), `OWNER_DECISIONS.md` with Decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (sha256 a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c; D5, D6), DEL-02-03/EXEC-v0.1 `EXECUTION_COMPATIBILITY.md` (sha256 e0ede76ebf08003511755afc666be2466a867fd3256837ee94300cd0dfe518e8; superseded, see above), DEL-03-03/ADAPTER-v0.1 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` (sha256 58b2409ca45ceea66160eb8910ca38b76b6f335dc184eaeb0896e93cabd0a074; §3.4, §3.5, OC-3, F-3, F-9); the committed 0.158.0 JSON Schema bundle `json-schema/experimental/codex_app_server_protocol.v2.schemas.json` and `_spike/inventory.txt` (for the MCP surface and `turn/interrupt` facts in §6.7–§6.8). Earlier: DEL-01-01/HOSTING-BOUNDARY-v0.2 (sha256 16711a83fec3439d7be634f6d62512be2a87f0dec32bd84028a39425bc84007a) and v0.1 (sha256 f1da7f76f686991f67b3e974478b9b453df804839712a7e5cc24e7bc4849d728); DEL-01-01/PIN-SPIKE-v0.1 `Design/PIN_SPIKE_0.158.0.md` — **current committed revision sha256 0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115** (commit 28bd00499; the parent's post-IR1 edits: SV-02 committed-tree wording, "what the spike proposed to commit" note, git-operations statement). Earlier revisions: v0.2 of this file consumed the **pre-correction** revision sha256 3d66ad28f3fa76a19826a09a7d8269f598bb4465912b6375f74bc4d56678f3cf; IR1-C reviewed sha256 26ea0c2fae8212ca46ed2ff60ddfaef5ca28e0ed73aae2105017d7ceccb40334 (commit c387730fb). `Design/generated/0.158.0/MANIFEST.sha256` (sha256 42b95826d7bd6d58df7941da7420064ee55d54a347a2eab22eafbfa16231569e, byte-unchanged) and `Design/generated/0.158.0/COMMITTED_STATE.md` (sha256 2cb7f1d29383e68239d085186401488c5d864046475b7cf9d3bc256f85782608); run `APP-V4-FIRST-INCREMENT-20260928`: `OWNER_DECISIONS.md` (Decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1`, sha256 f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e at that time), `R1_RESOLUTIONS.md` (sha256 2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4; R-1, R-2, R-4, R-10 applied), `comparisons/V1-A.md` (sha256 01811533bf0aedad5326d1517561187682a572ae3f47c5f8b8637e48cfe04c09; D-13, D-14, RF-03), `comparisons/V1-C.md` (sha256 8d46258ad0120067f6472442de67feacba8405462b78abb8bac34be28a4a94a6; D-16, D-22, §6, AG-13…15, AB-10, RF-6), `R2_RESOLUTIONS.md` (sha256 77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088; R2-22 applied, with R2-8 and R2-11), `reviews/IR1-C.md` (sha256 295e96b3f5871cdf4142df169dc8811cef0aa38e7a7eb1930b246f60f0a426b9; IR1C-04, IR1C-18, IR1C-19, IR1C-20 addressed to HOSTING). DEL-01-02…05, DEL-01-06, DEL-02-04 and DEL-04-01 remain referenced by accepted meaning (ScopeOfWork.md at 6e18505e3); DEL-04-01 act names are used as fixed by R-1. Root D-GOV-43 is governance context only (§2). Concept-run returns T7/T11 and v3 code remain dated historical evidence.
- Receivers (R9-6: rebuilt from the ACTIVE rows of this register and of the consumers' registers; layer per `_DAG/_LATEST.md` → DAG-003; table in §8). **This register's rows:** DEL-01-02 (OUT-001; REQ-001, REQ-003, REQ-004, REQ-005, REQ-007; TBD-002) via DEP-01-01-019; DEL-01-03 (OUT-001; REQ-001, REQ-004) via DEP-01-01-020; DEL-01-04 (native request/answer interaction) via DEP-01-01-021; DEL-01-05 (OUT-004; REQ-003, REQ-007, REQ-008) via DEP-01-01-022, with DEP-01-01-024 the UPSTREAM row for its sign-in and substitution evidence (held); DEL-01-06 (distribution identity for packaging) via DEP-01-01-023. **Consumers among the first-increment deliverables, from their own registers (all six arcs admitted):** DEL-02-01 (DEP-02-01-025, N-16: harness-capability meaning; this file holds the 0.158.0 inventory, and a capability meaning beyond the inventory is named by that row and not yet defined here, §8); DEL-02-03 (DEP-02-03-023, N-23: observed supplier facts as capability information; §6.1, §6.7, §6.8, §10, R9); DEL-03-03 (DEP-03-03-013, N-B4: MCP and dynamic-tool surfaces, channel status, model destination; §6.8, §8.3); DEL-03-04 (DEP-03-04-021, N-B9: native surfaces for optional external access; §6.8); DEL-04-03 (DEP-04-03-027, N-15: supplied guidance, model and destination, tool-permission settlements, supplied to it directly, R9-7; §8.2, §8.3, R8, S-7); DEL-09-06 (DEP-09-06-032, N-C5: App-side supplied-guidance and model-destination evidence; §8.2, §8.3). **Consumers outside the first increment, from their own registers:** DEL-02-04 (DEP-02-04-010, admitted: additive guidance, seam S-6; this register has no DOWNSTREAM mirror row, F-16); DEL-06-01 (DEP-06-01-013), DEL-09-01 (DEP-09-01-019) and DEL-09-02 (DEP-09-02-009), all admitted; and the consumer-side rows of the PKG-01 receivers (DEP-01-02-018, DEP-01-03-011, DEP-01-04-007 and DEP-01-06-006 admitted; DEP-01-05-012 held; DEP-01-05-013). DEL-05-01 and DEL-05-02 (J9: guidance carriage, answer origin) have no register row to this deliverable. App implementation owner (OI-008 proposal, reference-generator choice, pin re-examination). Under owner decision D1 the standalone-App definitions DEL-01-02…05 are a later undertaking; their receiving comparisons of S-1…S-4 happen then. The arcs N-18, N-21, N-24 and X-1 have no end in DEL-01-01; X-1's supplier, DEL-01-04, is the receiver of seam S-3.

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

**Act names.** Canonical names from R-1 are used: A14 *answer tool
permission* for the supplier's tool-use prompts, and A4–A7, A12, A13 for the
acts reserved to the person by owner decision D2. Following R-4, "approval"
in this file's own prose means only A6 (engineering approval). Supplier names
that contain "approval" (for example `item/commandExecution/requestApproval`)
are quoted as supplier names and denote A14 subjects.

---

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
process (with the descendant processes the supplier itself starts) and speaks
its published JSON-RPC protocol over the child's standard input and output
(V4-ARC-01, SOW-118). The boundary is the single place where:

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
| Additive instruction inputs preserving Codex base instructions | Deliverable interface "PKG-02 supplies guidance/workflow inputs"; production is DEL-02-04 | Carried unchanged through supported inputs, with per-thread/turn content identity evidence (§8.2) |

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
  (ARC §3). Durable custody across relaunch is DEL-01-02's (§6.5).
- **H4 Verified before ready.** No receiver is told the supplier is ready
  until verification (§7.2) and the handshake (§4.2) have both succeeded.
  Frames the supplier sends before `ready` (at 0.158.0 a notification arrives
  together with the initialize response, before the client's `initialized`
  notice; SPIKE §5) are kept in received order under the new generation and
  delivered with the `ready` announcement; they are never dropped (S-F-09).
- **H5 Generation tagging.** Each spawn receives a new *generation* at spawn
  time. Every outbound request, inbound response, notification, server
  request and register entry carries its generation. Nothing from one
  generation settles, answers or is attributed to another.
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
  The account-home element remains `UNRESOLVED{OI-009}`.
- **H10 Unknown stays unknown.** When a request to the supplier was written
  but its response was never observed (exit, wait limit, write failure), its
  outcome is *unknown*, not failed and not succeeded (V4-EXE-03; ARC §3).
- **H11 The supplier is a process tree.** The supplier starts its own
  descendant processes (at 0.158.0, networked `git` fetches of a plugin
  repository on a fresh home; they were observed alive and reparented 500 ms
  after the supplier exited; SPIKE §5). Stop, restart and exit handling treat
  the supplier and its descendants as one unit; surviving descendants are
  detected and recorded, never assumed gone (S-F-06). The mechanism (process
  group or equivalent) is unselected.

## 4. Child lifecycle

### 4.1 States (semantic)

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
   generation *g*. The account-home/environment element is
   `UNRESOLVED{OI-009}` (DEL-01-05 owns the choice's integration). On a fresh
   home the supplier performs a network fetch at start (§8.1 L-4, U-18).
4. **Handshake**: send the supplier's initialize request carrying the App's
   client identity and the capabilities the App declares (at 0.158.0:
   `experimentalApi` and `requestAttestation`, both required booleans;
   optional elements include `optOutNotificationMethods`, which stays absent
   or empty per H7; SPIKE §5). Record the declared capabilities: they
   determine request classification (§6.1, S-F-05). Record the handshake
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
4. Announce `exited-unexpectedly(g)` to receivers, including DEL-01-02, which
   owns recovery of actual thread/request state from the supplier after the
   next `ready` (V4-EXE-01, DEL-01-02 REQ-005; at 0.158.0 the supplier offers
   thread resume/read/list methods, post-restart results not-observed, P-13).
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
  the choice and the observed descendant state are recorded.
- Restart never re-sends a prompt, re-answers an old request or replays a
  client request of a closed generation (V4-EXE-01).

### 4.5 Deliberate stop

A stop is an explicit act (person quits the App or chooses stop), distinct
from closing or hiding a window (V4-EXE-01, V4-EXM-11). Sequence:

1. Write the **App stop record** for *g* (actor, time, reason) — the only
   evidence that the end was deliberate (S-F-07).
2. Announce `stopping`. Outstanding register entries are either explicitly
   declined by the App with origin `app-rule:on-stop` or left to end with the
   process — a DEL-01-02 recovery decision (U-10).
3. End the supplier politely (closing its input or a termination signal; at
   0.158.0 both end the supplier within milliseconds, SPIKE §5), then
   forcefully after a grace period (value unselected), **for the whole
   process tree** (H11).
4. Record surviving descendants, if any, and their handling; enter `stopped`.
   No unattended execution after quit is promised.

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
  without gaps or duplicates (realization is DEL-01-02's, §6.5).

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
| settlement | Native answer content or explicit error/decline content; **answer origin**: `person-via-interaction` (A14 by the person, actor supplied by DEL-01-04), `app-rule:<named rule>` (decline or error only), `app-explicit-error`; plus `supplier-internal` / `resolved-by-supplier` observations (§6.2, §6.6) |
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
outputs agree on these kinds — 10 stable, 11 experimental; SPIKE §4):

| Kind (supplier name) | A-name / subject | Proposed classification |
|---|---|---|
| `item/commandExecution/requestApproval` | A14 | known-answerable |
| `item/fileChange/requestApproval` | A14 | known-answerable |
| `item/permissions/requestApproval` | A14 | known-answerable |
| `execCommandApproval`, `applyPatchApproval` (legacy v1) | A14 | known-answerable if raised (whether they are raised on the v2 surface is not-observed) |
| `item/tool/requestUserInput` | input to the agent (not A14); **not act evidence, never host act capture** (R4-12; EXEC CAP-6) | known-answerable; answered only by the person (R9) |
| `mcpServer/elicitation/request` (modes include form and URL) | as above; the prompt is authored by an MCP server or the agent | known-answerable; answered only by the person (R9) |
| `item/tool/call` (dynamic tools; `dynamicTools` is experimental-only on thread start) | App-offered tool | known-app-unsupported unless the App registers dynamic tools (none defined in this increment) |
| `account/chatgptAuthTokens/refresh` | account | known-app-unsupported unless DEL-01-05 adopts external-token login |
| `attestation/generate` | account/attestation | unfamiliar while `requestAttestation` is declared false |
| `currentTime/read` (experimental) | clock service (not A14, not a person's input) | unfamiliar unless the experimental opt-in is declared; then known-answerable by a named App rule (R9 service kind) |

### 6.2 States

```text
received ─┬─(unfamiliar)──────────────► errored(explicit error written | write-failed)
          ├─(known-app-unsupported)───► errored / declined (explicit, per kind, named rule)
          └─(known-answerable)─► outstanding ─┬─ answer ─► settling ─► answered | declined
                                              │                    └─► settle-write-failed (outcome unknown)
                                              ├─ supplier-reported resolution ─► resolved-by-supplier
                                              └─ generation closed ─► ended-unanswered(process-exit)
```

`declined` covers an explicit negative answer by the person or an explicit
App rule; the origin says which. `resolved-by-supplier`: at 0.158.0 the
stable notification `serverRequest/resolved` (thread identity, request
identity) is the candidate source (`observed-in-generated-types`; its
triggers are not-observed — U-09, S-F-12). The cause, when the supplier
reports one, is recorded as observed; it is never inferred.

### 6.3 Rules

- **R1** Every inbound server request creates exactly one entry before any
  other handling, including when no window is open and while `handshaking`.
- **R2** `unfamiliar` requests receive an explicit protocol error
  immediately; never ignored, never answered affirmatively, never queued for
  the person as if known (SOW-123; ARC §3). The error code the App uses is an
  implementation choice; for reference, the supplier's own reply to an
  unknown client method is -32600 and v3 used -32601 (S-F-16).
- **R3** `known-answerable` entries wait for an answer. No timeout, observer
  loss or reconnect produces an answer. Any automatic decline after a period
  is not defined here (U-11); the supplier's legacy decision set includes a
  native `timed_out` form, and sending it would be an App rule under U-11,
  never automatic by default.
- **R4** An entry is settled at most once: second answer → `already-settled`;
  closed generation → `generation-closed`; unknown identity →
  `no-such-request`; entry already `resolved-by-supplier` → `already-resolved`.
- **R5** Answer content must be valid for that method under the reference
  output plus supplement; otherwise `invalid-answer`, entry stays
  outstanding. At 0.158.0 the native answer forms are listed in SPIKE §6
  P-08 (for example command execution: `accept`, `acceptForSession`,
  execpolicy/network-policy amendments, `decline`, `cancel`).
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
    settles no pending supplier request (EXEC CAP-9).
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
| answer (request identity, native answer, origin, actor ref) | DEL-01-04 (person path, any valid form); named App rules per R9 (decline/error only for A14 and person-input kinds; content answers only for named service kinds such as `currentTime/read`) | `accepted-for-write` → `answered`/`declined`/`settle-write-failed`; or refusal with reason (R4/R5); an App-rule affirmative or content answer to an A14 or person-input kind is refused `origin-not-permitted` (R9) |
| explicit error (request identity, reason) | boundary (R2), named App rules | `errored` |
| read settlement and acknowledgment observation | DEL-01-02 (custody of in-flight requests; outside this increment, D1); DEL-04-03 (evidence, supplied to it directly: R9-7; S-7) | Settlement, write result, acknowledgment observation |

### 6.5 Split with DEL-01-02 (to reconcile when DEL-01-02 is defined)

DEL-01-01 defines entry meaning, classification, R1–R9, the answer write path
and generation tagging, and witnesses the unknown-request path at the
protocol seam (VER-001). DEL-01-02 owns custody across observation loss,
reconnect and relaunch, recovery of outstanding requests from supplier state,
the register's representation and persistence (DEL-01-02 TBD-002),
stop-time handling (U-10), descendant handling with the App implementation
owner (U-16) and the settlement fixtures. F-01 records the overlap; under D1
the reconciliation happens in the later undertaking that defines DEL-01-02.

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
  thread identity, turn identity; empty result) —
  `observed-in-generated-types` only. Its live effect (what stops, when, and
  what the supplier completes first) is **not observed** (U-19); no receiver
  depends on observing it, since nothing relies on it (R4-2; EXEC-v0.5 §2.3
  HP-2 "Not adopted"). If
  the App sends it for another purpose (a person's explicit stop, V4-EXE-01),
  the outcome is recorded as observed, and any action completed after the
  request is recorded as observed, never as prevented.
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
inventory; all rows are `observed-in-generated-types` unless marked, none
exercised live. "Caller" is who initiates the MCP-side effect.

| Surface (supplier name) | Kind / variant | Caller | Boundary treatment | Receiver; evidence standing |
|---|---|---|---|---|
| `mcpServerStatus/list` (optional thread identity, detail, paging); `mcpServer/startupStatus/updated` notification | Client request (stable); notification (stable) | App (read) / supplier (report) | Generic request path; native delivery (H6) | DEL-03-03 channel state. A supplier status `disabled` is an **App-side configuration fact, never A13** (R4-13) |
| `config/mcpServer/reload`; `config/value/write`, `config/batchWrite` (write a key path into the user's Codex configuration) | Client requests (stable) | App, only as **person-directed** through the owning interface (DEL-03-03 OC-3; DEL-01-05) | Carries the change and records initiator; never initiated by an App rule or on an agent's instruction (H9: the person's own Codex configuration) | App-side configuration is **never A13 evidence**; any configuration an agent could write is not act evidence (R4-13). The host's refusal is the authoritative "off" (ADAPTER) |
| `mcpServer/oauth/login`; `mcpServer/oauthLogin/completed` | Client request; notification (stable) | App, person-directed | As above; credentials stay with the supplier | DEL-01-05 / DEL-03-03 (OC-6); not an act |
| Thread item `mcpToolCall` {server, tool, arguments, status, result, error, …}; `item/mcpToolCall/progress` | Items and notification (stable) | **The agent** (model-issued call) | Native delivery only; the boundary never alters, retries or answers these calls | DEL-03-03 dispatch observation; host outcome per DEL-03-02/03-03. Whether an MCP tool call raises an A14 request at 0.158.0 is **not observed** |
| `mcpServer/tool/call` (server, thread identity, tool, arguments, `_meta`; result content, structured content, is-error, `_meta`) | Client request (stable) | **The App** | App-origin only: recorded with initiator (§5) and never presented as the agent's call. Not issued for a holding run (HP-4, §6.7). It is **never used to act as the agent**, to perform, request on the person's behalf or record any person's act (A4–A7, A12, A13), or to submit a host operation in the agent's name. No use on a host channel is defined in this increment; a use needs DEL-03-03's definition and its own origin in the host's terms. It requires a thread identity; whether the call or its result enters that thread's items or model context is **not observed** | DEL-03-03 (OC-2/OC-7); results are App-origin evidence only |
| `mcpServer/resource/read` | Client request (stable) | The App | As `mcpServer/tool/call`: App-origin read; content reaches the App, not the model, unless the App supplies it | DEL-03-03; App-origin |
| `mcpServer/elicitation/request` | Server request (stable) | MCP server / agent → person | R9 person-input kind | Not act evidence; never host act capture (R4-12) |
| `mcpServer/event/stream/start`, `…/stop`; `mcpServer/event/stream/notification` | Start/stop experimental-only; notification in the stable set | App | Not used; unfamiliar/unused unless the experimental opt-in is declared and DEL-03-03 defines a use | — |
| `item/tool/call` (dynamic tools, experimental-only registration) | Server request | Agent → App | known-app-unsupported (§6.1); choosing dynamic tools changes the familiar set for the whole App (ADAPTER F-9; S-F-05) | DEL-03-03 OC-2 |

## 7. Supplier version identity and verification

### 7.1 Version identity record (semantic)

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
| configuration identity | Launcher, arguments, environment supplied by the App | Per generation (H1) |
| verification result | `verified` / `mismatch(<element>)` / `unverifiable(<reason>)`, time, generation | — |

### 7.2 Verification rule

Verified means: observed version label equals the declared pin **and** the
distribution content identity equals the expected identity **and** the
generated-output identity names the same pin. A label alone is not
sufficient (AC-006; F-06). The handshake-reported identity is a **consistency
check only**: a version parsed from `userAgent` text must not contradict the
declared pin, but it is weaker than the label and content checks and never
substitutes for them (S-F-01). Mismatch or unverifiable → `refused`. Running
an unverified distribution for development, and its label, is U-06; it is
never labeled the pinned supplier.

Probe side effect: at 0.158.0 even the version report writes into the home
it runs against (`CODEX_HOME/tmp/arg0/…`; S-F-17). Which home the label probe
uses (the account home or a separate probe home) is part of U-03/OI-009; the
content-identity check does not execute the binary and has no such effect.

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
  Using them requires declaring the experimental opt-in (F-13).
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
| S-1 lifecycle and register | DEL-01-02 | §4 states with generation; App stop record; `unknown-no-response`; register interface §6; exit and descendant facts; receipt positions | Durable custody, reconnect/relaunch, persistence, recovery reads, settlement fixtures, descendant policy (U-16, joint) |
| S-2 version identity + plan/revision | DEL-01-03 | Version identity record with each `ready(g)`; native plan items and plan updates unchanged with generation and receipt position; generic request path for plan interactions. At 0.158.0 each plan update carries the **whole plan with no revision identity**, plan deltas must not be assumed to concatenate to the completed item, and plan mode is experimental-only (S-F-13) | Revision identity (DEL-01-03 derives it from turn/item identities and receipt positions), registry, storage, export, UI, checker (SOW-128) |
| S-3 request answering | DEL-01-04 | Register operations; refusal reasons incl. `origin-not-permitted`; settlement; supplier-internal decision notifications (§6.6) | Request cards, answer UX, attachments, outcome presentation |
| S-4 embedding and provider | DEL-01-05; DEL-03-03 (channel status); DEL-04-03 via S-7 | Carriage of supplier account methods and per-conversation provider selection (at 0.158.0 `modelProvider` on thread start and resume; `modelProvider/capabilities/read`); **observed model destination** per thread/turn (§8.3; R4-1); §8.1 account; recorded-exchange evidence per §9; the fresh-home network observation (L-4) | Sign-in (including OAuth) and API-key flows, offered as options with no default between local and cloud (DECISION-4 D4-3; R8-9); account home (OI-009), provider configuration, server-substitution checks |
| S-5 distribution identity | DEL-01-06 | Distribution content identity over the vendor tree, version label, launcher record; spike-observed signing facts (Developer ID, hardened runtime) as observations only | Packaging, signing, notarisation, relocation of the vendor tree (not-observed), distribution |
| S-6 additive guidance | DEL-02-04 (inputs from DEL-02-01/02-02) | Carriage unchanged through the supplier's supported inputs (at 0.158.0 `baseInstructions` and `developerInstructions` on thread start and resume); per-thread/turn content-identity evidence (§8.2) | Guidance composition, role files, workflow semantics, idle-boundary change policy |
| S-7 evidence | DEL-04-03, directly (R9-7; DEP-04-03-027, arc N-15); DEL-09-06 for the supplied-guidance and model-destination evidence (DEP-09-06-032, arc N-C5) | Observed facts: version identity, generation, declared capabilities, settlement with origin, supplier-internal decisions, unknown outcomes, supplied-guidance identities, observed model destination (§8.3), client-request initiators (incl. App-initiated MCP calls, §6.8). A14 settlements go only to the run record's tool-permission entries (DEL-04-03 R13), never to a human-act record or a grant (R2-8) | Record format, writer/reader, any human act. Custody of in-flight requests across observation loss and relaunch, which is DEL-01-02's separate contribution (S-1; outside this increment, D1) |

**Receivers the live registers name (R9-6; rebuilt at v0.7).** The seams
table above is unchanged except S-7. The rows below are the ACTIVE rows of
the consumers' registers, with their DAG-003 layer, and where this file
already holds what each row names. No contribution is defined by this
table.

| Receiver | Register row (arc; DAG-003 layer) | Contribution the row names | Where this file holds it |
|---|---|---|---|
| DEL-02-01 | DEP-02-01-025 (N-16; admitted) | Harness-capability meaning, so that its harness-capability requirements refer to it | The 0.158.0 inventory (SPIKE §4; `generated/0.158.0/`) is held. A capability meaning beyond the inventory is not yet defined here |
| DEL-02-03 | DEP-02-03-023 (N-23; admitted) | Observed stock-Codex supplier facts, as capability information | §6.1, §6.7, §6.8, §10, R9 |
| DEL-03-03 | DEP-03-03-013 (N-B4; admitted) | Supplier MCP and dynamic-tool surfaces and channel-status facts at 0.158.0 | §6.8; §8.3; S-4 |
| DEL-03-04 | DEP-03-04-021 (N-B9; admitted) | The supplier boundary: native surfaces for optional external access | §6.8 |
| DEL-04-03 | DEP-04-03-027 (N-15; admitted) | Observed supplier facts: supplied guidance, model and destination, tool-permission settlements | S-7, §8.2, §8.3, R8; supplied directly (R9-7) |
| DEL-09-06 | DEP-09-06-032 (N-C5; admitted) | App-side supplied-guidance and model-destination evidence | §8.2, §8.3 as definition; no evidence exists |
| DEL-02-04 (outside the first increment) | DEP-02-04-010 (admitted) | The supported native supplier receiving contract for additive role supply | S-6; §8.2 |
| DEL-06-01, DEL-09-01 (outside) | DEP-06-01-013, DEP-09-01-019 (admitted) | The selected supplier pin, before protocol generation and qualification | Pin note; §7.1; U-01 (0.158.0 is the definition and generation pin only) |
| DEL-09-02 (outside) | DEP-09-02-009 (admitted) | Supplier hosting and protocol contribution and scoped feature checks, before the joined witness | §9 method and the designed cases; nothing is qualified |
| DEL-01-02, -03, -04, -06 (outside; D1) | DEP-01-02-018, DEP-01-03-011, DEP-01-04-007, DEP-01-06-006 (admitted); this register's DEP-01-01-019, -020, -021 and -023 | The stock supplier boundary, generated types, selected identity | S-1, S-2, S-3, S-5 |
| DEL-01-05 (outside; D1) | DEP-01-05-012 (held), DEP-01-05-013; this register's DEP-01-01-022, and DEP-01-01-024 (UPSTREAM, held) | The selected protocol and pin; embedding-qualification input | S-4; §8.1 |

The 0.158.0 inventory in SPIKE §4 (170 client methods, 11 server-request
kinds, 85 notifications in the TS experimental output) is the input to
harness-capability naming owned by DEL-02-01 (V1-C AB-10); no naming is
chosen here. DEL-02-01's register row DEP-02-01-025 (arc N-16, admitted)
asks for "the harness capability meaning supplied through DEL-01-01";
its ScopeOfWork CLM-002 says DEL-01-01 "supplies the harness capability
inventory". This file holds the inventory. A capability meaning beyond the
inventory is named by DEP-02-01-025 and is **not yet defined here** (F-27;
returned as a Wave B item).

### 8.1 Local-provider requirement account (REQ-005, AC-005; to DEL-01-05)

| Requirement | Published / basis claim (dated) | At 0.158.0 (SPIKE §6) |
|---|---|---|
| L-1 Local servers act as Codex model providers chosen per conversation | V4-ARC-04; T7 (2026-09-25) | `observed-in-generated-types`: `modelProvider` on thread start and resume; `modelProvider/capabilities/read`; CLI `--oss`, `--local-provider lmstudio|ollama` is `published-only`. Per-conversation effect live: not-observed |
| L-2 Wire interface Codex requires from a provider | ARC §6: "oMLX also serves the Responses API Codex requires" | **not-observed**: provider definition form and required interface are not in the generated output; the Responses statement stays an unobserved basis claim (R-10; V1-C D-22) |
| L-3 Tool calling through the provider | ARC §6, §8 risk | not-observed (no model turn in the spike) |
| L-4 Supplier network traffic at start (named "Local-operation boundary (priority 3)" up to v0.6) | ARC §1 priority 3. As amended by SCA-V4-001 it speaks of a host's agent ("It sends data only to the selected model service and to destinations the person has allowed, and every destination contacted is recorded and shown") and states no App local-operation boundary; ARCH §4 says the host-agent property does not govern the App's own Codex. No accepted text now decides this traffic (U-18) | **observed**: with a fresh home the supplier fetched ≈24 MB from `github.com/openai/plugins` at start, with no sign-in and no turn; warm home: none seen in ~6 s; whether a setting disables it: not-observed (S-F-10; F-14; U-18) |
| L-5 Credentials | V4-ARC-04; DECISION-4 D4-3 (R8-9) | `observed-in-generated-types`: login variants incl. API key and ChatGPT account sign-in; credential store modes `file`/`keyring`/`auto`/`ephemeral`; actual storage and local-provider key need: not-observed. **Model access choice (D4-3):** local and cloud are options the person chooses among, with **no default**; a cloud model is reached by **OAuth sign-in or an API key**. V4-HOST-01, as amended by SCA-V4-001, carries D4-3 for a host's agent; for the App path, D5 already leaves the model to the person. This boundary selects no default and carries the supplier's variants unchanged. Whether the supplier's sign-in variant serves D4-3's OAuth option for a given cloud provider is not-observed. Which flows the App offers is DEL-01-05's (S-4) |
| L-6 Distinct from host loop interface | ARC §4 V4-ARC-10 | Unchanged: each interface is qualified separately (AG-14). V4-ARC-10 (D-20) stays the v4 host-loop direction (DECISION-4 D4-2; R8-8) |

An unqualified server example establishes neither supported substitution nor
provider access (REQ-005).

### 8.2 Supplied-guidance evidence (V1-C D-16, R-10)

For every client request that carries additive guidance input (at 0.158.0
the base/developer instruction elements of thread start and thread resume),
the boundary records, per thread and per turn at which it applies: the
request identity and generation, which guidance element was carried, the
**content identity of each guidance input actually carried** (algorithm
U-08), and the source identity supplied by the composing owner (DEL-02-04;
workflow identity per R-9 where applicable). The recording tap (§9.1) holds
the bytes as evidence. These records are supplied to DEL-04-03 directly
(S-7; R9-7: DEL-04-03's ScopeOfWork CLM-004 takes "observed supplier facts
(supplied guidance, model and destination, tool-permission settlements)
from `DEL-01-01`", and RS R3 and R13 name DEL-01-01 as their source in this
undertaking; DEP-04-03-027). DEL-01-02's custody of in-flight requests is a
separate contribution of a deliverable outside this increment (D1).

**Named limitation (P-15).** This evidence establishes that the input was
*supplied*. Whether the supplier *adopted* it — in particular whether resume
overrides apply to an already-loaded thread (v3 observed that 0.154 ignored
them; at 0.158.0 not-observed) — is separate evidence and is not implied.
Launch configuration identity (§7.1) is not a substitute: it is per child
start, not per thread/turn.

### 8.3 Observed model destination (R4-1, R5-4; owner decision D5)

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

The destination **class** (local or cloud) is derived from the provider
configuration the person chose (DEL-01-05), not inferred by this boundary.
Whether requested and effective values can differ in practice is not
observed (U-19). D5 concerns host content reaching the conversation's model;
it does not address the supplier's own start-up traffic (L-4, U-18).

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
  person or machine (S-F-15). A redacted fixture never claims byte identity
  with the original exchange;
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
identified local provider.

## 11. Owner / act boundary (REQ-007, REQ-008, AC-007, VER-007)

| Act | Owner | This boundary's contribution | Not performed here |
|---|---|---|---|
| Select the definition/generation pin | App implementation owner; owner decision D4 selected 0.158.0 | §7 record, §10 observations, §9.5 method | Qualification; re-examination before implementation |
| Decide Rust/TS allocation | App implementation owner (OI-008) | §12 proposal | Decision |
| Choose the reference generator output | App implementation owner (U-15) | §7.3 options | Decision |
| Durable session/request custody, reconnect, relaunch, stop | DEL-01-02 | §4, §6 interface, S-1 | Custody code, persistence, recovery |
| Plan/tool/delegation presentation | DEL-01-03 | S-2 | Views, registry, revision identity, checker |
| Request cards, answers, outcomes, attachments | DEL-01-04 | S-3 | Cards, answer UX |
| Sign-in (including OAuth), API key, local provider (options the person chooses among, no default: DECISION-4 D4-3), substitution checks | DEL-01-05 | S-4, §8.1 | Flows, configuration, substitution evidence; any sign-in, which is the person's own |
| Packaging, signing, notarisation, distribution | DEL-01-06 (terms obtained by owner, OQ-08) | S-5 | Packaging production |
| Workflow semantics / making / registration | DEL-02-01 / DEL-02-02 | S-6 carriage | Semantics, registration, capability naming |
| Additive guidance production | DEL-02-04 | S-6 carriage, §8.2 evidence | Composition |
| Operation-policy / human-act definition | DEL-04-01 (D2, D3 adopted; OI-021 additions pending) | R7–R9 origin truthfulness | Policy |
| Run/act records | DEL-04-03 | S-7 observed facts | Records |
| A14 answer tool permission | The person (via DEL-01-04), or the user's own Codex mode inside the supplier (D3 setting; origin rule R7, DERIVED per R-2/R2-11) | Register accepts and records it with supplied actor/origin; evidence to the run record's tool-permission entries only (R2-8) | Performing, inferring or answering it affirmatively by App rule |
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
live beyond the generic request path; which interface component re-attaches
after reload (DEL-01-02); how the familiar set and answer-validity rules are
derived for Rust from the chosen reference output (U-15).

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
  Reconciliation now waits for the later undertaking that defines DEL-01-02
  (D1).
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
  (ARC §8 risk "protocol drift").
- **F-14 Network at start on a fresh home (L-4).** ≈24 MB fetch from
  `github.com/openai/plugins` with no sign-in or turn; its descendants can
  outlive the supplier. Routed to the **owner** and **DEL-01-05** (OI-009: a
  separate App account home would be
  "fresh" at least once per home). Configurability not observed (U-18). Up
  to v0.6 the owner route was framed as "priority 3, local-operation
  boundary". The amended ARC §1 priority 3 speaks of a host's agent and
  states no such boundary for the App, so no accepted text now frames this
  traffic (L-4); the question to the owner stands as U-18 states it.
- **F-15 D1 defers the standalone-App receivers.** DEL-01-02…05 definitions
  are a later undertaking; seams S-1…S-4 have no receiving comparison in this
  one.
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
  conclusion drawn.
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
  DEL-04-03 and DEL-02-04 as candidate evidence.
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
  as a Wave B item.

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| U-01 Pin qualification and re-examination of 0.158.0 (D4 selected it for definition/generation only) | App implementation owner | Before implementation and qualification | 0.158.0 used as definition/generation basis; nothing qualified |
| U-02 `UNRESOLVED{OI-008}` Rust/TS division | App implementation owner | Before architecture production contracts | §12 is a proposal only |
| U-03 `UNRESOLVED{OI-009}` account home, incl. which home the label probe writes into (S-F-17) | Owner with App implementation owner (DEL-01-05) | Before account integration | Configuration-identity element open |
| U-04 *Closed by owner decision D3* (tool-permission/sandbox modes are the user's own Codex setting) | — | — | H9, R7 settled |
| U-05 Restart bound values and grace period | App implementation owner with DEL-01-02 | Before implementation | Rules defined; numbers open |
| U-06 Running an unverified distribution for development, and its label | App implementation owner | Before implementation | Default: refused as pinned supplier |
| U-07 Use of the supplier's notification opt-out (`optOutNotificationMethods`) | App implementation owner | Before implementation | Definition uses none (H7) |
| U-08 Content-identity algorithm for distribution/output/supplement/guidance records | App implementation owner (with DEL-04-03) | Before qualification records | Spike used SHA-256 as an observation method; not selected for records |
| U-09 Acknowledgment observation mechanism; `serverRequest/resolved` triggers | DEL-01-02 with this deliverable | Before settlement fixtures | Candidate source named; semantics open |
| U-10 Stop-time handling of outstanding entries | DEL-01-02 | Before recovery implementation | Both paths defined with truthful origin |
| U-11 Any automatic decline after a period (incl. the native `timed_out` form) | App implementation owner with DEL-01-02 | Before implementation | Not defined; never affirmative (R7) |
| U-12 More than one concurrent supplier child | App implementation owner | Before implementation | One active child assumed |
| U-13 Redaction policy details | App implementation owner | Before first capture | Categories extended (§9.1) |
| U-14 DEL-01-01/DEL-01-02 unknown-request split (F-01) | Both owners | When DEL-01-02 is defined (later undertaking, D1) | Proposed reading §6.5 |
| U-15 Reference generator output (O-R1/O-R2/O-R3) | App implementation owner | Before R2/R5 implementation and conformance | Options in §7.3 |
| U-16 Supplier descendant handling on stop/restart/overlap | DEL-01-02 with App implementation owner | Before lifecycle implementation | H11 requires detection and recording; policy open |
| U-17 Distribution-identity composition and launcher (wrapper vs vendor) | App implementation owner with DEL-01-06 | Before verification implementation | Both recorded; composition open |
| U-18 Supplier network fetch at start: acceptability (framed up to v0.6 as "under priority 3"; the amended priority 3 speaks of a host's agent, and no accepted text now decides this traffic, L-4); configurability (not addressed by D5, which concerns host content reaching the conversation model) | Owner with DEL-01-05 | Before any local-operation claim | Observed; no claim of local-only operation |
| U-19 Unobserved live behaviors (§10 "Still to observe") | App implementation owner (next spike; needs credential or local provider) | Before settlement fixtures, handshake implementation and qualification | Recorded as not observed |
| U-20 Partition of the 0.158.0 server-request kinds and their R9 origin classes (§6.1 proposal) | App implementation owner with DEL-01-04/01-05 | Before R2 implementation | Proposal only; R9 classes fixed as INTEGRATION, membership open |
| U-21 Supplier's `[experimental]` label on app-server/generators; dependence on experimental API (F-12, F-13) | Owner visibility; App implementation owner at pin re-examination | Before implementation | Recorded; supplier direction not reopened |
| U-22 L-2 provider wire interface (Responses) and L-3 | DEL-01-05 | Before provider qualification | Not observed |
| U-23 `UNRESOLVED{D6}` App-side run holds. SWBPIPE answered SQ-02 on 2026-09-28 with no host-held route (route (iv), none planned). **Closed for Phase 1** by DECISION-4 D4-1; re-opens when the governance phase is taken up (R8-2) | The owner (DECISION-4; D6 re-opens with the governance phase), via DEL-02-03 | When the governance phase is taken up for a workflow that needs it; before App-side hold implementation | Phase 1: no App run is holding, and no hold point is used (§6.7). Governance phase: no hold claim; `turn/interrupt` not relied upon; HP-3 and HP-4 best effort only; hold-support values per R5-1 as amended by R8-2 |
| U-24 Any App-initiated use of `mcpServer/tool/call` / `mcpServer/resource/read` on a host channel | DEL-03-03 (OC-2/OC-7) with App implementation owner | Before any such use | None defined; App-origin rules of §6.8 bind any later use |
| U-25 *Closed (R6-4)* by EXEC-v0.3 §2 HP-4 scope: person-directed turns are not blocked, carried `person-directed`, disposition unchanged, governed agent actions are action during hold | — | — | §6.7 |

## Verification cases

Designed, not qualified. "Runnable now" means the case can be executed
against 0.158.0 artifacts or a supplier double seeded from the spike
transcripts; no App candidate exists, so no case can pass a VER criterion
yet, and spike runs (SV-nn) are evidence, not passes.

| Case | Setup | Action | Expected result | Runnable now? | Serves |
|---|---|---|---|---|---|
| VC-01 Stock and unmodified | Candidate and pin | Inspect stack, distribution identity vs expected, launcher/configuration | Tauri 2/React/Vite; vendor-tree identity matches recorded; no patch; launcher and added environment recorded | Partly: SV-03 observed the binary identity; no candidate | VER-001 |
| VC-02 Pipe ownership | Candidate, turn active | Close and reopen the window | Same generation; work continues; register unchanged | No (candidate, live turn) | VER-001 |
| VC-03 Unfamiliar request | X-07 | Double sends an unfamiliar server request | Entry (R1); explicit error (R2); no affirmative answer; marked `unfamiliar` | Yes (double) | VER-001 |
| VC-04 Malformed frames | X-08 | Malformed, oversize, version-member-less frames | Malformed surfaced; version-member-less valid frames accepted (S-F-08) | Yes (double) | VER-001 |
| VC-05 Exit with outstanding work | X-09 | Kill child mid-turn | `ended-unanswered(process-exit)`; `unknown-no-response`; no grant; old answers refused `generation-closed` | No (live turn) | VER-001, VER-006 |
| VC-06 Restart bound | Constructed failures | Force failures past bound | `halted-after-repeated-failure`; explicit restart needed | Yes (double) | VER-001 |
| VC-07 Generated provenance | 0.158.0 | Regenerate both kinds/variants; check manifest; inspect supplement | Identical identities; supplement per chosen reference only | Yes. Evidence so far (`generated/0.158.0/COMMITTED_STATE.md`, IR1C-04): committed tree against the manifest **2 OK / 2,357 not committed / 0 mismatched**; the 1,605 TS files verified **OK** against the manifest from the parent's temporary scratch copy (after its deletion TS verification needs regeneration); SV-01 determinism as returned by W11. The W11 SV-02 line "1,607 OK, 752 missing" described the spike's proposed, never-committed form. Reference not chosen (U-15); no pass claimed | VER-002 |
| VC-08 Native pass-through | X-01/X-02 | Compare delivered frames to recorded | Method, ids, payload and top-level supplier elements (`emittedAtMs`) unchanged; metadata beside | Partly: X-01 side from spike transcripts | VER-002 |
| VC-09 Version identity to plan receiver | X-01/X-03 | Trace `ready(g)` record and plan updates to S-2 | Record complete; plan updates native, whole-plan, with generation/position; revision identity left to DEL-01-03 | No (plan needs live turn) | VER-003 |
| VC-10 Label-only mismatch | X-11 | Same label, different content identity | `refused` with `mismatch(distribution content identity)` | Yes | VER-003, VER-006 |
| VC-11 OI-008 review | §12 and the owner's decision | Review against ARC §3, priorities, M-6 | Decision source recorded; while OI-008 open the allocation criterion is **not met** | Review only | VER-004 |
| VC-12 Local-provider account | §8.1 | Compare claims to candidate observations | Rows labeled; L-4 observed; L-2/L-3 not observed; no substitution claimed | Partly (L-4 observed) | VER-005 |
| VC-13 Upgrade comparison | Two pins | Run §9.5 | Diffs incl. generator divergence and experimental status; no adoption | Yes, once a second pin is named | VER-006 |
| VC-14 Settlement truthfulness | X-04/X-05/X-12 | Person answers; App rule declines; App rule attempts affirmative; second answer | Origins truthful; affirmative App-rule answer to an A14 or person-input kind refused `origin-not-permitted` (R9); App-rule content answer to `currentTime/read` accepted when the opt-in is declared; `already-settled`; write failure → `settle-write-failed` | Partly (X-12 with double) | VER-001, VER-007 |
| VC-15 Act boundary review | §11, candidate statements | One-for-one review against CLM-004…006 and R-1 | Each act resolves to its owner; A14 never presented as A4–A7 or a checkpoint act; no invented sequence | Review only | VER-007 |
| VC-16 Frames during handshaking | X-01 (spike transcripts show `remoteControl/status/changed` before `initialized`) | Replay handshake | Early notification held in order under *g* and delivered at `ready`; not dropped (H4) | Yes (double) | VER-001 |
| VC-17 Deliberate stop with descendants | X-13, fresh home | Start, then deliberate stop while the plugin fetch runs | App stop record marks the end deliberate (exit code 0 not used); surviving descendants detected and recorded; handling per U-16 | Yes, with owner visibility of the network fetch | VER-001 |
| VC-18 Supplier-internal decision | X-14, user sets `auto_review` | Trigger a tool-permission decision inside Codex | No register entry for an unreceived request; notifications delivered natively; origin `supplier-internal`; never shown as the person's answer | No (live turn) | VER-001, VER-007 |
| VC-19 Supplied-guidance evidence | Thread start and resume carrying developer instructions | Inspect records per thread/turn | Content identity of each carried input recorded with request identity and generation; adoption not claimed (P-15 limitation) | No (candidate; resume needs a thread) | VER-003, VER-007 |
| VC-20 Classification by declared capabilities | Double; experimental opt-in false | Double raises `currentTime/read` and `attestation/generate` | Both `unfamiliar` → explicit error; with opt-in declared, `currentTime/read` becomes familiar | Yes (double) | VER-001, VER-002 |
| VC-21 Supplier refusal of an App request | Spike transcript (unknown client method → -32600) | Replay | Outcome `response-observed(error)`, not unknown; connection continues | Yes (transcript) | VER-001 |
| VC-22 Answer origin by kind (R9) | Double; opt-in declared | App rule attempts a content answer to `item/tool/requestUserInput`, an affirmative answer to `item/fileChange/requestApproval`, a decline of an elicitation, and a content answer to `currentTime/read` | First two refused `origin-not-permitted`; decline recorded `app-rule:<name>`; `currentTime/read` answered `app-rule:<name>`; no answer presented as a checkpoint act | Yes (double) | VER-001, VER-007 |
| VC-23 Person-input answer is not act evidence (R4-12) | Double seeded with an elicitation request on a host-content subject | Person answers "yes, accepted" in the elicitation | Settlement `person-via-interaction`; delivered as conversation input only; no human-act record, no checkpoint satisfaction, host item stays queued | Yes (double) | VER-007 |
| VC-24 MCP surface classification (R4-12) | Double; status list, startup notification, `mcpToolCall` item, App-initiated `mcpServer/tool/call` | Replay each | Status `disabled` reported as App-side configuration, never A13; agent's `mcpToolCall` delivered natively; App-initiated call recorded with App initiator, never shown as the agent's call or as any person's act | Yes (double) | VER-001, VER-007 |
| VC-25 No hold claim (R4-2; R8-1) | **Phase 1:** a run with a reached checkpoint (DEL-02-03 records the arrival); a tool-permission request reaches the App; a second tool settled by the user's mode. **Governance phase:** held run of a governed checkpoint (DEL-02-03 state), same requests | **Phase 1:** a receiver attempts an App-initiated `mcpServer/tool/call` for the run. **Governance phase:** named App rule declines the first request; a receiver then attempts an App-initiated `mcpServer/tool/call` for the run | **Phase 1:** no run is reported holding; no named-rule decline and no `run-holding` refusal is made for the checkpoint; the call is handled by the ordinary §6.8 rules; both tools are delivered natively; no hold claimed and no hold-support value carried; `turn/interrupt` not sent. **Governance phase:** decline recorded `app-rule:<name>`; the auto-settled tool is delivered natively as completed; the App-initiated call is refused `run-holding` (HP-4); no hold claimed and no hold-support value raised; `turn/interrupt` not sent for the hold | Yes (double) | VER-001, VER-007 |
| VC-26 Model destination facts (R4-1) | Thread start with a selected provider; a constructed re-route notification | Inspect S-4/S-7 facts | Requested and effective provider/model kept separate per turn; the re-route recorded on its turn; a turn with no supplier report carries *unknown*, never an earlier value; no gate on enablement; class taken from DEL-01-05's configuration | Partly (constructed re-route with a double; live start needs credential or local provider) | VER-005 |
