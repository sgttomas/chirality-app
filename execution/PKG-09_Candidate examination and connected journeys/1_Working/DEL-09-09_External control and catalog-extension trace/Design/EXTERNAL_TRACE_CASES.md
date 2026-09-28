# External control and catalog-extension trace cases
- Contribution: DEL-09-09/XT-v0.3. It supersedes XT-v0.2 (sha256 28ff092e114f386a723ea7f19d1a6e23a3963b92b44a1383d6308d0c111077c6, committed at `9fc77baa3`), which superseded XT-v0.1 (sha256 8f098c79f1da28af1b461210c36cca1124a25e226e802f2203b46ce7052df8cd, `b4030fe4b`). R5 pass under R5_RESOLUTIONS.md (R5-1, R5-2, R5-4, R5-9, R5-10).
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001 (V4-EXM-25 external control suite — case definitions and input/limitation account; **not run**), OUT-002 (V4-EXM-24 one-new-operation three-surface trace plan and comparison categories; **not run**), OUT-003 (generated-versus-adapted work account structure and the OI-003 disposition record — recorded, never performed); REQ-001…REQ-009 (definition parts); AC-001…AC-009 through designed VER-001…VER-009
- Basis: repo 6e18505e3 (accepted basis); ScopeOfWork.md sha256 082db8fa70bf0ceb8c8bf3c3a7fc4a222994858c66fdc7d9e5f16909f3ed862d; Dependencies.csv sha256 02d738c7ae0cecd809bac16f8e94d67354ac95a874bd3090ef62ed6a790ffbe2 (ACTIVE EXECUTION rows DEP-09-09-007…020); `P/docs/EXAMINATION.md` (sha256 1b156553dec7eb103dbb1166f5c0dbe9c719d26630d2fcace26c28b3ef54ee19) §1–2, V4-EXM-24, V4-EXM-25; `P/docs/HOST_INTEGRATION.md` (sha256 08c8fc7db2d74619ed47d184f44938bb06f1e2abda0a304a9e11b9230d0960da) §§1–7, §9, §11 (V4-HI-01…04, 10…12, 20…25, 30…33, 40…42, 50…52, 70/71); `P/docs/PRD.md` (sha256 657593ce12a9a6da9f8b6c66579945499d909a8b6272d919d2d14a3db4538573) V4-PAR-05, §4.4–4.5, §4.7, OQ-02, OQ-10, OQ-11; SCC-CASE-002 `Case_Datasheet.md` (sha256 6acdc6c4e484ab7b46ba7d45a347961bc69b3e624bd29ef58a613ec6c66a71a6) rows M2-A, M4-J, M4-X; owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (OWNER_DECISIONS.md sha256 f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e) D1–D3; R1 (sha256 2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4), R2 (sha256 77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088), R3 (sha256 202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf), R4 at `f05c7e4cd` (sha256 50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24: R4-1, R4-2, R4-6, R4-8, R4-12…R4-14, R4-16, R4-18, R4-20); owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (OWNER_DECISIONS.md at `f05c7e4cd`, sha256 a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c: D5 settled, D6 deferred to SQ-02); `reviews/V2.md` MAJOR-1; BRIEFS.md working copy sha256 77a42f8a8c8260285b4142d3a6392a07daead16010b209139efc0d3efc60a21f ("Common brief", "Owner rulings now in force", "Wave 2 — common additions", "W9")
- Consumed inputs:
  - **R6 micro-pass inputs (in place, no version bump):** R6_RESOLUTIONS.md sha256 8703e85aa7324e233fab285321e277d720923d3e36e342c865917b55083cb841 (R6-1, R6-4, R6-5); `reviews/V4-A.md` sha256 121deafc40c4baf0dec71f96eb449083b0d93456c2bd448f89a279951ca2eab1; `reviews/V4-B.md` sha256 1569cd15b490a07c1fda44114fd6d017f794c16dfe533c65a27d04aad02c2cfc; DEL-02-03/EXEC-v0.3 working tree sha256 b147d9862fe9e0228139c72ba13c50392dcf66930109c4357587bf97bbdebf42 (§3.5; §3.6 HS-1…HS-5 by held actions; fixture classification table; MT-2, MT-16; U-E23). Current sibling labels (not re-read in full at this pass): Wave-1 v0.5 (C-v0.5 states V-ED1's branching and V-GR1), EXEC-v0.3, ADAPTER-v0.3 (XF-42 DESIGNED), GUIDE-v0.2.
  - **v0.3 inputs (R5 pass; binding rulings R5_RESOLUTIONS.md at `8fb51f07f`, sha256 254d0b93b9959419a70c6737b07087e1db59b529adc3105a1db31f82b78dd6f1; V3-A and V3-B reviews in the same commit).** Every sibling Design file is read at commit `8fb51f07f` (the committed texts; the working-tree revisions their owners are making in parallel under R5 were not read), and body citations use these versions: DEL-03-01/C-v0.4 sha256 e929d39d3ff9515702f9bfe51dfada537e1cbd165146ec0de4ccf629c659a08c; DEL-03-02/P-v0.4 sha256 0d3960a2e6bd3520368006cdd2b1b67a1fe4eb06e23184aded9d5b98d6c5e361; DEL-04-01/ACT-POLICY-v0.4 sha256 d6da05abe790a4374df7faf225439a01dc1be734491b499d90cf00533369b03b; DEL-04-02/AS-v0.4 sha256 774728d03824397a5343412b17659feaf9b0d2ef1029b79889d13a1b421f4dab; DEL-04-03/RS-v0.4 sha256 56806b64b12a946e706ff236dd1c25fe27ac00877aac13b50ee8603aaf540199; DEL-02-01/WD-v0.4 sha256 e492ff635de972466c8a932355beeae848e1f3d3f60de7304e88963352d8e88e and WD-EX-v0.4 sha256 60ce307a25fe1f9aaad0826985e02aaa6ebd68d86a6d972b1d5a1e39b3128ca4; DEL-05-01/LOOP-v0.4 sha256 ffc3048333f3370ba09a9ce124159b94f2c80ce69b5f593bfb82cc552f95934e; DEL-05-02/PANEL-v0.4 sha256 cb71bc4bd3d8a2034cd236437670d5cd6dad10f8dfcc0d6c75b277573ce84419; DEL-01-01/HOSTING-BOUNDARY-v0.4 sha256 201ea32005dd2c9fb5281a376eb25eebfcb5a644d09a6d3bf5901aaf934c7e58; DEL-02-03/EXEC-v0.2 sha256 7f7848c0de2fdb4dc21f5adafa97f92e179bb66c9f6b04f3434d8f2342317af0; DEL-03-03/ADAPTER-v0.2 sha256 a2905dda5782d7a48fa35ef7e26b0c1517fd3bd995e3ddbba27d2426a25674bc; DEL-03-04/GUIDE-v0.1 sha256 fc96d285a3512065ede29394fe4ef4c5eafc6ccbd08213396826a0bab517afb8. R5 bumps those files (Wave-1 to v0.5, EXEC/ADAPTER to v0.3, GUIDE to v0.2) in parallel with this pass; where R5 fixes a meaning they will carry (the four hold-support values R5-1, host-held carriage R5-2, destination per turn R5-4, V-GR1 R5-7), this file states the R5 ruling directly and cites R5. The entries below are the history of earlier bases.
  - **v0.2 sweep inputs (working tree after `f05c7e4cd`; reported finished by the coordinator).** From v0.2 the short names **C**, **ACT**, **EXEC** and **ADAPTER** denote: DEL-03-01/C-v0.4 `CATALOG_AND_READ_BASIS.md` sha256 e929d39d3ff9515702f9bfe51dfada537e1cbd165146ec0de4ccf629c659a08c (FXA-1…FXA-5, editions e1/e2, **V-ED1**, §4.1 reporters, UNRESOLVED edition-addition event); DEL-04-01/ACT-POLICY-v0.4 `ACT_AND_POLICY_CONTRACT.md` sha256 d6da05abe790a4374df7faf225439a01dc1be734491b499d90cf00533369b03b (§2.6 A13 capture, §4.6, FX-47, F-15); DEL-02-03/EXEC-v0.2 `EXECUTION_COMPATIBILITY.md` sha256 7f7848c0de2fdb4dc21f5adafa97f92e179bb66c9f6b04f3434d8f2342317af0 (§2 HP-H, §3.6, MT-2, F-17, F-21); DEL-03-03/ADAPTER-v0.2 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` sha256 a2905dda5782d7a48fa35ef7e26b0c1517fd3bd995e3ddbba27d2426a25674bc (S-X11…S-X13, §3.4, PI-2, PI-5, PI-6, L-ADAPTER-11…13, XF-40…XF-42, XT rehearsal map, F-15, F-17). Same sweep: DEL-09-06/CA-v0.2 and RELAY-v0.2 (SQ-01…SQ-32).
  - **v0.1 basis (read with `git show`):**
  - **Wave-1 v0.3 at `ba0b37123`** (history: v0.1/v0.2 basis for P, RS, AS, LOOP, PANEL, WD and HOSTING; superseded by the v0.3 inputs above; blob-identical to the PR #1039 head `1c36b6d97`; the brief's merge `98b1723b` is absent from this clone): **C** DEL-03-01/C-v0.3 `CATALOG_AND_READ_BASIS.md` sha256 ba45e7393ee0b16780f36605ddeecb95ba1f181488e36a46b4b495b69fd67c26 (§3, §4.1, §5, §6, §8, §10 FX-PIPE-01, evidence-label mapping); **P** DEL-03-02/P-v0.3 sha256 ec0db87f239bc42e2e3e953d660ce3c4ceddf605d7b98cf1393f97a099b699cf (§2, §5–§11, §12); **ACT** DEL-04-01/ACT-POLICY-v0.3 sha256 b3748c02006f939d8cc78c6e0b0c847598a8b32d55515ae8658ad80597c98128 (§2, §5.3, §6, §9); **RS** DEL-04-03/RS-v0.3 sha256 925f35ca27bd7d1e71a375883ada9903267408af57312eed1ae02b47776a3528 (R7, R9, R11, §6); **AS** DEL-04-02/AS-v0.3 sha256 7b634137bb8402f3eaedc943dab0c5f1114b9d4433d2b94e13540ac0bf8e0514 (§3); **LOOP** DEL-05-01/LOOP-v0.3 sha256 6b771c8027787193d536fa3507214a8cc579d6ec2f476ee880609c920b6f25c7 (§2.2, §6, §11, §12); **PANEL** DEL-05-02/PANEL-v0.3 sha256 4c47764d3af434c23e63dcc2c10d28f18a4a94546d63d452855c471cfe47bee9 (§3.3, §4, §5); **WD** DEL-02-01/WD-v0.3 sha256 84841d9f539767b9ff7ae225fec27f0dc4ebbd2c161c41aff179bbae97f345eb (§4.2.4); **HOSTING** DEL-01-01/HOSTING-BOUNDARY-v0.3 sha256 34c3383402aabe6e9347aa2f111318538c4a2a4ca85adb8fffff7e439fdde94e (§3, §6).
  - **Wave-2 at `e20a3ae8d` (superseded by ADAPTER-v0.2 and EXEC-v0.2 above):** DEL-03-03/ADAPTER-v0.1 `ADAPTER_ENABLEMENT_AND_RECEIVING.md` sha256 58b2409ca45ceea66160eb8910ca38b76b6f335dc184eaeb0896e93cabd0a074 (§3–§10, fixture inventory XF-01…XF-39, L-ADAPTER-1…10; PR #885 cited there as evidence only); **EXEC** DEL-02-03/EXEC-v0.1 sha256 e0ede76ebf08003511755afc666be2466a867fd3256837ee94300cd0dfe518e8 (§3 EV-1…EV-11, §7.1).
  - v0.1 also read DEL-09-06/CA-v0.1 and RELAY-v0.1 (same run); v0.1's citation of `DECISIONS_PENDING_2.md` D5/D6 as pending is replaced by DECISION-2.
  - SWBPIPE catalog, endpoint, candidate, receipts or acts: **none received** (DEP-001; DEP-09-09-014). DEL-09-01 (examination infrastructure): accepted SoW meaning only, outside this undertaking (D1).
- Receivers: DEL-03-01 (trace and work evidence via DEP-03-01-030 before any extension claim; CASE-002 M4-X); the owner with the host contract owner (evidence for the OI-003 ruling, DEP-09-09-020); DEL-09-06 (joined activity; shared act cases); DEL-03-03 (which ADAPTER cases the joined suite reuses); DEL-09-01 (protocol needs, when defined); the external SWBPIPE owner through the relay file.

---

## 0. Reading this definition

**What it defines.** Designed, not-run definitions of: (1) the V4-EXM-25
external control suite — the App's Codex inspects, submits a proposal, the
engineer accepts it in SWBPIPE, and the chain is traced to the host receipt,
with stale, duplicate, interruption and unknown cases (§3); (2) the
V4-EXM-24 trace plan for one newly added catalog operation across the human,
embedded and external surfaces, with comparison categories (§4); (3) the
structure of the generated-versus-adapted work account and of the OI-003
disposition record (§5). §2 lists every input and its standing; §8 lists
every input still missing.

**What it does not do.** It executes nothing and establishes no live
connection (SoW purpose). It selects no transport (DEL-03-03 TBD-007), operation
(`UNRESOLVED{OI-021}`), or extension criterion (`UNRESOLVED{OI-003}`). It
**records** the OI-003 ruling when one is supplied and **never performs** it.
It performs no human act and constructs nothing owned elsewhere (REQ-009).

**Naming.** Element names are semantic labels, not wire names. Acts A1–A14
(R-1); outcomes P §9 / C §4.1; class values C §3.1; dispositions WD §4.3.4.
Fixture material is C §10 FX-PIPE-01 and ADAPTER §10 (L-ADAPTER-n, XF-nn).
Local labels are `L-XT-n` with reasons. `SQ-nn` are relay questions in
DEL-09-06 `RELAY_QUESTIONS_SWBPIPE.md`.

**Two kinds of case.** ADAPTER's XF cases are **focused** App-side receiving
cases against a *simulated endpoint* (test double). The XC and TR cases here
are **joined** cases: they complete only on identified App and SWBPIPE
candidates with actual host behavior and, where named, an actual person's
act. An XC case may reuse an XF case as its test-double rehearsal; the
rehearsal never completes the XC case.

---

## 1. Settled distinctions relied on

| # | Distinction | Citation |
|---|---|---|
| S-1 | The host may expose its catalog to the App's Codex as an MCP server or as a CLI over its live controller; both built from the catalog, same validation, autonomy settings and reserved acts. The host chooses the seam | V4-HI-50; SoW REQ-002 |
| S-2 | External access is off unless the person enables it, and is local to the machine | V4-HI-52 |
| S-3 | Useful parity is operation meaning, truthful standing and recovery, not identical gestures | #d4; SoW AX-001 |
| S-4 | Shared schemas, a transport, common validation, transport de-duplication or component passes do not prove the joined outcome, durable duplicate safety, extension or savings | V4-EXM-24/25; HI §11; SoW REQ-005 |
| S-5 | The original all-actor "without separate work" promise stays identified; its disposition is explicit (retain / narrow / defer); no weaker criterion is adopted silently | V4-PAR-05; V4-HI-03; OQ-10; OI-003 |
| S-6 | Execution, queued proposal, edit acceptance, checking, approval and reliance are distinct; proposal UI says *accept*; acts lapse visibly when bound content changes | V4-HI-25, 30…33; #d3; R-4 |
| S-7 | Reserved to the person (App/shared contracts): A4; A5 where autonomy requires a proposal; A6; A7; A12; A13 (enable; disable INTEGRATION). A10 wherever A5 is (DERIVED) | D2; R-1; R2-3 |
| S-8 | Every result names candidate, configuration and date; outcomes are passed / failed / blocked / not run / inconclusive; changed candidates reopen affected cases; criteria are protected | V4-EXM-01…05; EXAMINATION §1 |
| S-9 | **SETTLED (DECISION-2 D5):** content the App's Codex reads over the channel may go to the model the person selected for the conversation, cloud included, with no App gate; a host may restrict its own channel. **INTEGRATION (DECISION-2 reading; R4-1, R5-4):** the App records the model destination per turn where the supplier reports it (requested and effective kept apart; unobserved turns *unknown*; run-level value = the set observed; a switch starts no new run) and shows it in the channel status as information, never as a gate | DECISION-2 D5; R4-1; R5-4; HOSTING §8.3 |
| S-10 | App-side run holds are `UNRESOLVED{D6}`, deferred to SWBPIPE SQ-02, which settles them only for checkpoints whose every held action is a host operation; a checkpoint with any App-side held action stays *not enforceable* whatever SWBPIPE answers (R5-10; R6-1: classification by what the checkpoint must hold, not by how it arrives). Hold support takes one of four values (R5-1): *enforced by the host loop*; *enforced on the host route* (host-held constraint evidenced by SQ-02 and a candidate); *not established* (awaiting SQ-02; the check does not pass, but this is not *unsupported*); *not enforceable* (no mechanism: any App-side held action; or, once SQ-02 is answered with no host-held route, a constraint carried only as model-supplied; workflow *unsupported*, R4-8). Only host-held carriage satisfies R2-12; a received constraint keeps its source's assurance unless the host verifies it against its own declaration copy (R5-2). No App hold is claimed; run actions while a checkpoint waits are recorded as *action during hold* | DECISION-2 D6; R4-2, R4-8, R4-14; R5-1, R5-2, R5-10; EXEC §3.6 |
| S-11 | A13 is captured only by the host's enablement facility, with a capture-evidence reference; App-side configuration (which an agent could write) is never A13 evidence; the host's refusal is the authoritative "off"; the App reports *channel not enabled* when its own configuration is off, the host when its channel is off | R4-13, R4-16; ACT §2.6 |
| S-12 | An A12 counts, and supersedes an earlier setting, only when the control **established** it; a refused A12 changes nothing | R4-6; EXEC §4.10 |

---

## 2. Examination input account (REQ-001; AC-001; VER-001)

Standing uses the C evidence-label mapping and the DEL-09-06 contribution
ladder (CA §7.2). "Defined" means a definition exists; it is **not** an
available input for live examination.

| # | Input | Supplier | Needed for | Standing now |
|---|---|---|---|---|
| IN-01 | App candidate identity: build, stock Codex version actually used, model and server | App construction (later undertaking) | All XC/TR | Not available. Pin 0.158.0 is a definition pin, not qualification (D4) |
| IN-02 | SWBPIPE candidate identity and configuration | SWBPIPE owner (SQ-27) | All XC/TR | Not received |
| IN-03 | Shared candidate/date/configuration protocol; WebKit/Chromium and packaged-smoke evidence protocol | DEL-09-01 (outside D1) | §6 | Not defined in this undertaking |
| IN-04 | Catalog and read-basis contract | DEL-03-01 C-v0.4 | §3, §4 | Defined (*illustrative*) |
| IN-05 | Proposal, validation and outcome contract | DEL-03-02 P-v0.4 | §3, §4 | Defined |
| IN-06 | External receiving contribution and focused fixtures | DEL-03-03 ADAPTER-v0.2 | §3 | Defined; native family only, no interposition adopted (S-X12); family choice DEL-03-03 TBD-007 |
| IN-07 | Adopted operation policy and act distinctions | DEL-04-01 ACT-v0.4 (D2/D3; §2.6 A13; §4.6 hold support) | XC-09, XC-10; CMP-07 | Defined; host adoption not evidenced (SQ-05) |
| IN-08 | Record semantics | DEL-04-03 RS-v0.4 | XC-09; §6 | Defined |
| IN-09 | Host external seam, native surface derivation and mapping to catalog identity | SWBPIPE owner (SQ-12) | XC-01…XC-12; TR on X | Not received; PR #885 is evidence only |
| IN-10 | Selected first operation, autonomy and environment | Owner via outside SWB session with App/shared owner (OI-021; SQ-04) | Live XC | `UNRESOLVED{OI-021}` |
| IN-11 | The one newly added catalog operation, who adds it, and how the edition addition is reported | SWBPIPE owner (SQ-26) | §4 | Not received; fixture C-v0.4 V-ED1 (e1 → e2) |
| IN-12 | OI-003 disposition | Owner with host contract owner | §5.2 | `UNRESOLVED{OI-003}` |
| IN-13 | Additional essential hosts | Owner (OI-005) | Freezing wider scope | Open; SWBPIPE only |
| IN-14 | Host restriction of its own channel by model destination, if any. App side: "content may flow to the selected model, no gate" is SETTLED (DECISION-2 D5); "record and show the destination" is INTEGRATION (DECISION-2 reading; R4-1, R5-4) | SWBPIPE owner (SQ-16) | XC-01 live enablement | Not received; no restriction presumed; a refusal is relayed |
| IN-15 | Host A13 enablement facility with a capture-evidence reference; enablement behavior; the person's A13 | SWBPIPE owner (SQ-28, SQ-13); the person (DEP-09-09-015) | XC-01, XC-12 and every live XC case | Not received / not performed; without it the channel stays *not enabled* (S-11) |
| IN-16 | Capture-evidence reference for host-captured acts | SWBPIPE owner (SQ-01) | XC-02, XC-09 | Not received |
| IN-17 | Constraint receipt or host-held declaration | SWBPIPE owner (SQ-02) | XC-10 | Not received |
| IN-18 | Proposal identity, de-duplication order and durability; read by identity | SWBPIPE owner (SQ-08) | XC-05, XC-06 | Not received |
| IN-19 | Basis, generation, original-versus-queue-time basis, per-item stale rule | SWBPIPE owner (SQ-07) | XC-03, XC-08 | Not received |
| IN-20 | Outcome statements distinct from transport; errors; unknown | SWBPIPE owner (SQ-09) | XC-06, XC-07 | Not received |
| IN-21 | The engineer's actual acceptance in SWBPIPE (actor ≠ recorder) | The person (DEP-09-09-016) | XC-02 | Not performed |
| IN-22 | Embedded surface for the three-surface trace: host loop and embedded tools; App-side loop receiving | SWBPIPE owner; DEL-05-01 LOOP-v0.4 (receiving) | §4 on E | LOOP defined; host loop not received. **Not registered** in DEL-09-09 Dependencies.csv (F-2) |
| IN-23 | Host human interface and proposal views | SWBPIPE owner (SQ-22) | §4 on H; XC-02 old/new values | Not received |
| IN-24 | Exposure per surface (element 9) | SWBPIPE owner (SQ-11) | §4 CMP-04; XC-11 | Not received; FXA-1 fixture assumption |
| IN-25 | Hold support for checkpoints on X | `UNRESOLVED{D6}`: SWBPIPE SQ-02 for checkpoints whose held actions are all host operations; a separate owner follow-up for checkpoints with App-side held actions (R5-10; R6-1); DEL-02-03 computes hold support (EXEC §3.6) | XC-10 | Values per R5-1 and R6-1, for checkpoints whose every held action is a host operation: host-held constraint evidenced after SQ-02 → *enforced on the host route*; SQ-02 unanswered → *not established*; SQ-02 answered with no host-held route (e.g. model-supplied only) → *not enforceable* (*unsupported*). Any App-side held action → *not enforceable* (*unsupported*) whatever SQ-02 returns |
| IN-26 | Undo route | SWBPIPE owner (SQ-10) | CMP-14 | Not received |
| IN-27 | Origin marks and caller identity | SWBPIPE owner (SQ-14) | XC-02; CMP-12 | Not received |
| IN-28 | Locality and sandbox reach | SWBPIPE owner (SQ-15) | XC-01 | Not received |
| IN-29 | Grant display and grant states | DEL-04-02 AS-v0.4; host presentation (SQ-05 (e), (h)) | XC-10; CMP-07 | AS defined; not registered in DEL-09-09 Dependencies.csv (F-2) |

---

## 3. V4-EXM-25 external control suite (OUT-001; REQ-002…REQ-004, REQ-007, REQ-008)

### 3.1 The joined chain

The suite joins these elements, each with its own evidence, on one identified
App candidate and one identified SWBPIPE candidate. Each is **linked** to host
evidence, never copied into a replacement store (V4-HI-71).

| # | Element | Evidence owner |
|---|---|---|
| J-1 | Channel state at the time (enabled; A13 reference; locality; data destination shown) | Host facility; App observation (ADAPTER §3) |
| J-2 | The original inspected basis: workspace identity, generation, model revision, canonical content identity and method designation, plus per-row subject content identities | Host read result (C §5) |
| J-3 | The submission: proposal identity, relied-on basis (unchanged from J-2), bound targets, origin, grant in force, requested mode, constraint if any | App dispatch record (ADAPTER §5.1; RS R7) |
| J-4 | The host outcome per item: refused (stale/invalid) with both bases, or queued | Host (P §9) |
| J-5 | The engineer's act in SWBPIPE: A5 (and A10) per item, with actor, bound change-item content identity, capture-evidence reference | Host act facility (IN-16, IN-21) |
| J-6 | Application: receipt, resulting revision, resulting objects, origin mark | Host (P §9 applied association) |
| J-7 | Host views: old and new values shown for the item | Host views (IN-23) |
| J-8 | App record: faithful record of J-5 citing its reference; operation entries; evidence limits | App (RS R7, R9, R11) |

### 3.2 Cases

"Rehearsal" names the ADAPTER XF case that exercises the same meaning on a
test double. "State" is DESIGNED · AWAITING INPUT (inputs named) · HELD
(decision named).

| Case | Fixture steps | Joined observation required | Expected | Rehearsal | State | Serves |
|---|---|---|---|---|---|---|
| **XC-00 Identification** | — | IN-01, IN-02, configuration, date, invented material identity recorded before any result | Every later result cites it; a candidate change reopens affected XC cases | — | AWAITING INPUT (IN-01, IN-02, IN-03) | AC-001, AC-008 / VER-001, VER-008 |
| **XC-01 Access disabled, unavailable, enabled** | L-ADAPTER-1; T1 | (a) never enabled → App makes no host request, reports *channel not enabled* itself (R4-16); (b) App configured, host off → host-reported *channel not enabled*; (c) endpoint stopped / needs authentication → *endpoint-unavailable* with reason; (d) the person performs A13 in the host's enablement facility → *enabled*, with the host's capture-evidence reference; grant display unchanged; the conversation's model destination shown and recorded, never gating (S-9) | Channel states as ADAPTER §3.2; enablement grants no autonomy (E-5); App-side or agent-written configuration never A13 evidence and never enables (S-11); without a host capture-evidence reference the channel stays *not enabled* | XF-01…XF-07 | AWAITING INPUT (IN-09, IN-15 incl. SQ-28, IN-28); host restriction by destination, if any, relayed (IN-14, SQ-16) | AC-002 / VER-002 |
| **XC-02 Inspect → submit → accept → receipt** | T9 read (B2); T10 PR-2 submitted over X → *queued*; T11 Engineer A accepts item 1 (A5) and rejects item 2 (A10) in SWBPIPE; T12 applied → RC-1 (S-5 created, R-100 changed) | J-1…J-8 all observed; App reports *queued*, never accepted, until J-5 is read; "accepted by Engineer A" only with host-captured A5; "applied" only with RC-1; host views show old/new values; origin mark linked; the model destination recorded per turn where reported (S-9) | Chain unbroken from B2 to RC-1; A5 not lapsed by application; A10 distinct; no act from success | XF-11, XF-16, XF-18 | AWAITING INPUT (IN-16, IN-21, IN-23, IN-27; IN-10 for the real operation) | AC-003, AC-007 / VER-003, VER-007 |
| **XC-03 Intervening edit → stale** | T3 read (B1); T5 PR-1; T6 Engineer A edits S-3 (r13); T7 submit over X | Per-item *refused — stale*: failing target S-3; relied B1; current B2; reason; item-left events; the refusal compares against the **original** inspected basis, not a queue-time basis | Stale with both bases; no silent refresh; re-draft is a new proposal (T9) | XF-14, XF-15 | AWAITING INPUT (IN-19) | AC-004 / VER-004 |
| **XC-04 Later selection cannot retarget** | During T10, Engineer A selects S-4 in the host UI | PR-2's bound targets remain R-100, S-2, S-3 in the host's proposal view and at application | No retargeting | XF-17 | AWAITING INPUT (IN-23) | AC-004 / VER-004 |
| **XC-05 Duplicate submission** | T13: PR-2 resubmitted with the same identity; variant L-XT-2 (= ADAPTER L-ADAPTER-11): two submissions before any acknowledgment, including a variant where the second send carries a new identity. **Reason:** C's T13 covers only a retry after application | Each submission recorded separately; neither reported *queued* before a host acknowledgment; host answers the repeat from recorded state; **one domain effect** shown from domain evidence (model history, receipts), not from transport or session de-duplication; a new identity on the second send is two proposals, each reported as observed | One effect evidenced, or "one effect unevidenced" recorded; never a duplicate-safety pass from transport | XF-19, XF-40 | AWAITING INPUT (IN-18) | AC-004 / VER-004 |
| **XC-06 Lost acknowledgment and interruption** | T13 ack lost → seek observation by identity → if never received, retry same identity; L-ADAPTER-5 endpoint restart between T12 and T13; App restart variant L-XT-3 (= ADAPTER L-ADAPTER-12) | Actual application or refusal traced to the receipt after interruption **when observable**; retry never refused stale by its own effect; after a non-durable restart the retry is *outcome unknown* and one-effect unevidenced; after an App restart the in-flight submission is *outcome unknown* (observer App, last observed *submitted*) and the channel state is re-established without silent re-enable. **Seek-before-resubmit is guidance only on X** (ADAPTER PI-2): if the agent resubmits without first observing, the case still proceeds and the violation is **recorded as an evidence limit**, not prevented and not hidden | Original basis → outcome → receipt joined, or explicit unknown; reconnect and queue-time basis never taken as proof; any seek-before-resubmit violation recorded | XF-19, XF-21, XF-41 | AWAITING INPUT (IN-18, IN-20); App-restart custody DEL-01-02 (later, D1) | AC-004 / VER-004 |
| **XC-07 Unknown outcome** | V-OU1 over X: neither T12 nor T13 observed | *outcome unknown*, observer App, last observed *accepted*; a later observation is reported as its own event and does not back-fill | Unknown preserved; never applied/failed by inference | XF-20 | AWAITING INPUT (IN-20) | AC-004 / VER-004 |
| **XC-08 Accepted, then stale at application** | V-S1: Engineer A edits S-2 after T11 and before T12 (r14′) | "accepted by Engineer A — not applied: refused — stale (relied B2, current ⟨B-r14′⟩)"; A5 not lapsed | As R2-16 | XF-30 | AWAITING INPUT (IN-19, IN-16) | AC-004, AC-007 / VER-004, VER-007 |
| **XC-09 Acts: positive faithful record and false-attribution negatives** | (+) T11 A5 read over X and faithfully recorded (actor Engineer A; recorder App; capture-evidence reference; bound change-item identity; scope; purpose). (−) T10 *queued*; T12 receipt; an A14 answer; model text "the engineer accepted"; a user-input or elicitation answer (L-ADAPTER-4; not act evidence, R4-12); T4 findings. (±) T2 A4 on S-2 carried with no acceptance predecessor; lapsed after T14. Label: the host proposal UI says *accept*, not *approve* | Positive record conforms; every negative establishes no act; independent A4 needs no A5; lapse visible | As ACT §2, RS §6, R-4 | XF-18, XF-31, XF-32, XF-33 | Positive: AWAITING INPUT (IN-16, IN-21); negatives: DESIGNED | AC-007 / VER-007 |
| **XC-10 Same route and policy as embedded/human** | XF-22 (direct without grant at r13 under ⟨set-1⟩); XF-23 (T15 → T16: ⟨set-2⟩ class P-03 scope {FX-W1; {S-4}} per C T15; the grant is in force because the control established it, S-12; OP-C9 applied directly); XF-25 (V-CP1 constraint, host-held carriage); XF-26 (constraint only model-supplied); XF-42 (action during hold on X); XF-27 (reserved OP-C6); XF-28 (OP-C11 no policy basis); XF-24 (host channel rule variant) | Each outcome over X equals the embedded/human route's outcome for equivalent input, except authority differences reported as *not permitted* naming the treatment (ADAPTER RP-2). Hold support per R5-1: XF-25's `CP-accept` is *not established* until SQ-02 is answered, then *enforced on the host route* once the host-held constraint is evidenced; XF-26 (the variant in which SQ-02 is answered with no host-held route, so the constraint is model-supplied only) is *not enforceable* → workflow *unsupported*; before SQ-02 is answered the same case is *not established*; XF-42 records a run action taken while a checkpoint waits as *action during hold* (a recording case; the hold itself is `UNRESOLVED{D6}`); no App hold is claimed | As ADAPTER RP-3; no conversion into a proposal; reserved entries offered, never withheld | XF-22…XF-29, XF-42 | AWAITING INPUT (IN-07 host adoption, IN-17, IN-29); XF-25 AWAITING INPUT (SQ-02); XF-26 DESIGNED (expected *not enforceable*); XF-42 DESIGNED (recording case); XF-28 part HELD (R2-9; OI-021) | AC-002, AC-003 / VER-002, VER-003 |
| **XC-11 Reads, checks and unavailability compared** | T3 read over X vs E vs H (XF-11); T4 OP-C3 findings and T4a OP-C12 host check (XF-12); T8 OP-C2 unavailable (XF-08); V-X1 not exposed (XF-09) | Same meaningful content, standing, subject identities, reason and evaluated basis across routes; host-reported *not exposed* relayed | Parity of meaning (S-3); findings never "checked" | XF-08, XF-09, XF-11, XF-12 | AWAITING INPUT (IN-22, IN-23, IN-24) | AC-003 / VER-003 |
| **XC-12 Disable while queued** | L-ADAPTER-6: the person disables access after T10, before T11 | New requests *channel not enabled*; PR-2 stays queued in the host; the engineer can still decide it; App shows last observed *queued*, "channel since disabled" | Nothing withdrawn by disabling | XF-35 | AWAITING INPUT (IN-15) | AC-002 / VER-002 |

### 3.3 Completion rule for the V4-EXM-25 witness (REQ-003; AC-003)

The witness is **complete** only when, on the same identified candidates,
XC-02 is observed live with the engineer's actual acceptance (J-5) and the
host receipt (J-6), and XC-03, XC-05, XC-06 and XC-07 are observed. The
other cases may complete later with their own standing. The following never
complete it: definitions; XF rehearsals on a test double; recorded replay;
Runtime or Piping component passes; a successful tool response standing in
for J-5 or J-6; an honest absence report (SoW REQ-003, REQ-008).

**Gate.** Every live XC case needs the channel to be *enabled*, which needs
the host's A13 enablement facility with a capture-evidence reference
(SQ-28; S-11). SQ-28 therefore gates the whole suite, including the
completion cases above (R5-10).

### 3.4 Result record per case (REQ-008)

Each executed result records: case id; candidate ids (XC-00); configuration
(realization family actually used; endpoint); date; evidence label
(*test-double* for rehearsal, *actual host* for joined); outcome (**passed ·
failed · blocked · not run · inconclusive**); observations with links to host
receipts and act records; evidence limits (RS R11); and which inputs were
missing. A failed case leads to diagnosis and repair without weakening its
criterion (V4-EXM-05).

---

## 4. V4-EXM-24 one-new-operation trace plan (OUT-002; REQ-005; AC-005)

### 4.1 The operation traced

The source requires exactly **one newly added** catalog operation, traced on
an identified candidate. Which operation is the SWBPIPE owner's and the
owner's to supply (IN-11, SQ-26). Until then the plan uses:

- **C-v0.4 V-ED1 (fixture edition addition; formerly the local L-XT-1).**
  Edition **e1** is FX-PIPE-01's edition without OP-C9 *Set support label*;
  the host publishes edition **e2**, adding OP-C9 v1 as C §10.2 describes it.
  The **edition addition event** is identified by {edition e1 → e2, added
  entry OP-C9 v1, time}; it is host-reported and changes no model revision
  (C §10.4). The main timeline T1–T17 runs on e2; V-ED1 replays T1–T15 on e1
  and publishes e2 before T16, as C-v0.5 §10.4 now states.
  L-XT-1 is retired and resolves to V-ED1 (R4-20). OP-C9 suits the trace: a
  change operation with a precondition ("support exists"), a validation error
  (E-label-too-long), the SWB model-change class (P-03), an undo path
  (OP-C10), a subject-identity dependency (FXA-2: a label change lapses an A4
  on the row), and a named non-exposure variant (V-X1). Whether the host
  reports an addition as such an event is a host input (C-v0.4 UNRESOLVED;
  SQ-26).

### 4.2 Trace stages

| Stage | Content | Owner of the work observed | Evidence |
|---|---|---|---|
| TS-0 Baseline | On e1 (V-ED1 step 1), each surface reports OP-C9 **missing** (a discovery finding), never *not exposed* or *unavailable* | Host; App (EXEC EV-5) | Compatibility reports per surface (EXEC CR-7) |
| TS-1 Addition | The host adds the entry and publishes e2 (V-ED1 step 2: one host-reported edition addition event). Every change made anywhere to support it is recorded in the §5 account | SWBPIPE owner | Host source revision(s) or change records (IN-11) |
| TS-2 Discovery | Each surface discovers OP-C9 with identity/version, purpose, schema, availability, effects, result, errors, class, exposure | Host (H, E, X); App (X mapping) | Per-surface discovery records |
| TS-3 Exercise | The same scenario on each surface against the same model revision (§4.4) | Host; App (X); the person (H acts) | Case results |
| TS-4 Compare | Category-by-category comparison (§4.3) | DEL-09-09 | Comparison table |
| TS-5 Account | Generated-versus-adapted work account and disposition record (§5) | DEL-09-09 records; owner rules | §5 |

### 4.3 Comparison categories

Every comparison uses the **same model revision and the same operation
identity/version** on the three surfaces. Result values: **same meaning** ·
**differs** (a defect, with detail) · **differs by authority only** (*not
permitted* naming the governing treatment; the one permitted difference,
ADAPTER RP-2) · **not exposed** (host-reported from element 9) · **not
comparable** (reason, e.g. different basis or version) · **not observed**.

| # | Category | What is compared | Source rule |
|---|---|---|---|
| CMP-01 | Discovery and identity | Entry present after addition, absent before; identity and version | V4-HI-01/02; EXEC EV-5 |
| CMP-02 | Entry elements | All nine C §3 elements reach the surface with the same meaning; open description readable without Chirality software; renderings add or drop nothing | C §2 inv. 2, 4; ADAPTER §4.2 |
| CMP-03 | Input and target identification | Same schema; schema-invalid input rejected before domain validation | C §3; LOOP V-3 |
| CMP-04 | Exposure | Element 9 per surface; *not exposed* host-reported (V-X1) | R2-4; C §8 |
| CMP-05 | Availability and reason | Precondition failure → *unavailable*, same reason identity, statement and evaluated basis on H, E and X | V4-HI-04; C §4.2 |
| CMP-06 | Meaningful reads and standing | Reads of the affected rows before and after; standing marks; currency | V4-HI-10/12; C §6 |
| CMP-07 | Class and treatment | Under ⟨set-1⟩: propose; direct *not permitted*. Under ⟨set-2⟩ (class P-03, scope {FX-W1; {S-4}}): direct applied on S-4; direct on other supports *not permitted* | ACT §5.3, §6; C T15 |
| CMP-08 | Validation error | E-label-too-long → *refused — invalid*, same error identity and text | P §2, §9; C §4.4 |
| CMP-09 | Stale refusal | Label change relying on a basis before an intervening edit to that support → *refused — stale* with both bases | P §5; R2-13 |
| CMP-10 | Non-mutating checks | Host check and examination relevant to the operation (fixture: OP-C12 and OP-C3 on the same basis) give the same results on each surface; if the host offers a preview for the new operation, it is compared too | SoW REQ-005 |
| CMP-11 | Proposal views | Old and new label values, affected object, reason, in the host's own view for a proposal from each surface | V4-HI-24; P §8 |
| CMP-12 | Application and receipt | Receipt, resulting revision, resulting objects, origin mark per channel; direct application records no acceptance | P §9; V4-HI-23 |
| CMP-13 | Recovery | Lost acknowledgment → read by identity → same-identity retry; unknown preserved | P §5, §7; R2-13 |
| CMP-14 | Undo | OP-C10 reverses the new operation's receipt, governed by its policy record (R3-4); "applied, then reversed" | R2-15; R3-4 |
| CMP-15 | Human-act separation | Success of the new operation yields no act; an A4 on S-4 bound before the label change lapses (FXA-2); reserved entries are unaffected | V4-HI-25, 32; S-6 |

### 4.4 Case matrix (fixture scenario per category; all DESIGNED unless noted)

| Case | Scenario on each of H, E, X (same revision) | Categories | State |
|---|---|---|---|
| TR-01 | V-ED1: TS-0 on e1, the edition addition event, then TS-2 discovery on e2 | CMP-01, 02, 04 | AWAITING INPUT (IN-11, IN-22, IN-24) |
| TR-02 | OP-C9 on a support that does not exist | CMP-05 | AWAITING INPUT (IN-22, IN-23) |
| TR-03 | OP-C9 with a label that is too long; with a schema-invalid argument | CMP-03, 08 | AWAITING INPUT (IN-22, IN-23) |
| TR-04 | Propose OP-C9 on S-4 under ⟨set-1⟩; engineer accepts in the host view; application | CMP-06, 07, 11, 12 | AWAITING INPUT (IN-16, IN-21, IN-23) |
| TR-05 | Direct OP-C9 on S-4 under ⟨set-2⟩ (T15/T16); direct on S-3 under ⟨set-2⟩ | CMP-07, 12 | AWAITING INPUT (IN-07 host adoption, IN-29) |
| TR-06 | Intervening edit to S-4 between read and submission | CMP-09 | AWAITING INPUT (IN-19) |
| TR-07 | OP-C12 and OP-C3 before and after the label change | CMP-10 | AWAITING INPUT (IN-11: which checks the host relates to the operation) |
| TR-08 | Lost acknowledgment after application; retry | CMP-13 | AWAITING INPUT (IN-18, IN-20) |
| TR-09 | Undo of the label change (T17 analogue) | CMP-14, 15 | AWAITING INPUT (IN-26) |
| TR-10 | V-X1: OP-C9 not exposed on X | CMP-04 | AWAITING INPUT (IN-24); relevant to a narrowed criterion |

### 4.5 What the trace cannot establish

A completed trace is evidence for the OI-003 decision. It does not decide it,
and it establishes no maintenance or coordination saving; no saving is
measured or estimated unless actually observed (EXAMINATION §2). Common
schemas or validation alone establish neither operational integration nor
automatic extension (REQ-005).

---

## 5. Generated-versus-adapted work account and extension disposition (OUT-003; REQ-005, REQ-006; AC-005, AC-006)

### 5.1 Work account structure

One row per **surface × element** for the traced operation. Elements follow
the C §8 three-surface map, plus the App-side receiving rows.

| Column | Meaning |
|---|---|
| Surface | H (host human interface) · E (embedded tools / host loop) · X (external interface) · App-X (App receiving side, ADAPTER) |
| Element | Entry discovery · exposure · input schema · availability and reason · effects and resulting objects · result and standing · errors · class element · constraint receipt · read basis · proposal views · native mapping (X) · loop tool offering (E) · App receiving configuration (App-X) |
| Production route before addition | generated · checked · hand-built · unagreed · not observed (C §8 values) |
| Change made for the new operation | none · generated automatically · regenerated by a step · hand change · not observed |
| Other changes required? | yes · no · unknown — the evidence for a retained "without other changes" criterion |
| Contributor | The party who made the change (host owner; App owner; named deliverable) |
| Evidence | Link to the change record, source revision or build; never copied |
| Candidate and date | As XC-00 |
| Limits | What the row does not show |

Rules: every surface and element has a row, including those with "none";
"unknown" is never read as "no"; no effort, time or cost figure is entered
unless actually observed; no savings statement is made (AX-001).

### 5.2 OI-003 disposition record (recorded, never performed)

| Field | Current value |
|---|---|
| Original promise | V4-PAR-05 / V4-HI-03 (preserved original seed): adding an operation makes it available to the person, the embedded agent and the external agent without separate work |
| Current status | `UNRESOLVED{OI-003}`, owner **Owner with host contract owner**, point of need **before claiming extension capability or fixing its acceptance criterion**; PRD OQ-10 adds App/shared-contract and external host design participation |
| Ruling (when supplied) | Option (**retain** · **narrow** to identified generated surfaces · **defer** with identified staging); decision actor; date as evidenced; source record and custody; chosen surfaces or staging; supersession statement; consequences for DEL-03-01 AC-007 |
| Criterion then examined | *Retain*: TR cases show availability on all three surfaces **without other changes** and with the same availability reasons (§5.1 column "Other changes required?" all *no*). *Narrow*: exactly the chosen surfaces, with the supersession recorded and the remaining work listed. *Defer*: the staging and the evidence named by the ruling |
| While unruled | The trace and work account are reported as evidence; **no extension criterion and no pass are established**; no weaker criterion is adopted (SoW REQ-006, AC-006) |

### 5.3 Links

The account links: the TR case results (§4.4); the joined V4-EXM-25 results
that use the same operation boundary (§3), when the traced operation is the
external-control operation; and DEL-03-01's receiving row (DEP-03-01-030).

---

## 6. Evidence protocol and standing (REQ-008; AC-008)

- **Labels** follow the C mapping: *illustrative* · *test-double* · *actual
  host* · AWAITING INPUT / HELD / NOT-OBSERVED · LIMITED.
- **Provenance** is kept distinct: test definition; recorded replay
  (V4-EXM-02); static source inspection; live observation; the person's actual
  act; the host receipt. They may share one evidence set; each keeps its own
  identity and standing (SoW OUT section note).
- **Interface evidence** follows the shared WebKit/Chromium and targeted
  packaged-smoke protocol (V4-EXM-04) through DEL-09-01. DEL-09-01 is outside
  this undertaking (IN-03); until it exists, interface observations carry the
  limit "protocol not yet defined". Browser evidence never replaces a required
  native observation.
- **Rechecks.** A changed App or host candidate reopens the affected XC and TR
  cases (V4-EXM-03).
- **Host receipts** are linked, never copied into a replacement truth store.

---

## 7. Owner and act boundary (REQ-009; AC-009)

| Excluded act or production (REQ-009) | Owner | This contribution's part |
|---|---|---|
| Catalog/read-basis contract construction | App DEL-03-01 | Consumed (IN-04) |
| Proposal/outcome contract construction | App DEL-03-02 | Consumed (IN-05) |
| External receiving implementation | App DEL-03-03 | XF cases reused as rehearsals (IN-06) |
| Adopted-policy contract construction | App DEL-04-01 | Consumed (IN-07) |
| Record implementation | App DEL-04-03 | Consumed (IN-08) |
| Reusable examination harness | App DEL-09-01 (outside D1) | Protocol need recorded (IN-03) |
| Host catalog/domain mutation, validation/application, endpoint, loop/panel/views, receipts, act facility | External SWBPIPE owner (CLM-003) | Relay questions only |
| Enabling access (A13); the engineer's actual acceptance (A5) | The person | Observed and faithfully recorded, never performed |
| Engineering approval, certification, professional reliance | The accountable professional | Not required by V4-EXM-25; never inferred |
| Unresolved operation policy (OI-021 additions) | The owner with App/SWB contract owners | `UNRESOLVED{OI-021}` |
| Extension disposition | The owner with the host contract owner | Recorded in §5.2; never performed |
| Cross-session relay; handoff and dependency coordination | The human; the App manager | Through DEL-09-06 relay file |

---

## 8. Inputs still missing (consolidated)

For the V4-EXM-25 suite: IN-01, IN-02, IN-03, IN-09, IN-10, IN-14 (host
restriction by destination, if any; SQ-16), IN-15 (A13 facility and reference,
SQ-28), IN-16, IN-17, IN-18, IN-19, IN-20, IN-21, IN-23, IN-25
(`UNRESOLVED{D6}`, on SQ-02), IN-27, IN-28, and host adoption under IN-07.

For the V4-EXM-24 trace: IN-01, IN-02, IN-03, IN-11, IN-22, IN-23, IN-24,
IN-26, plus IN-16/IN-21 for the acceptance step (TR-04) and IN-18/IN-19/IN-20
for TR-06 and TR-08.

For the OI-003 disposition: IN-12 (the ruling), after the trace evidence.

For freezing any wider examination scope: IN-13 (OI-005).

No case is AWAITING only on an App definition; every AWAITING case needs at
least one external input or an App construction output from a later
undertaking.

---

## 9. Findings (reported; scope and other files unchanged)

### 9.1 v0.1 findings and their disposition

| # | v0.1 finding (short) | Disposition at v0.2 |
|---|---|---|
| F-1 | SoW still calls OI-001/OI-002 open | Carried to C1 |
| F-2 | Dependencies.csv lacks embedded-surface and other rows | Carried to C1 (R4 register findings: W9 XT F-2) |
| F-3 | DEL-09-01 outside D1 | Carried to C1 (out-of-scope receivers) |
| F-4 | No ADAPTER rehearsal for two sends before acknowledgment or an App restart | **Ruled by R4-20**: ADAPTER-v0.2 adds L-ADAPTER-11/12 and XF-40/XF-41; XC-05 and XC-06 cite them |
| F-5 | No catalog-edition addition event in C | **Ruled by R4-20**: C-v0.4 adds e1/e2 and V-ED1; §4.1 re-pointed; L-XT-1 retired |
| F-6 | "One domain effect" reading | Unchanged (reading stated) |
| F-7 | T15 divergence (V2 MAJOR-1) | **Ruled by R4-18**; C-v0.4 confirms T15 |
| F-8 | V4-EXM-25 and V4-EXM-24 comparison overlap | Unchanged; noted for DEL-09-07 |

### 9.2 New findings at v0.2

| # | Where | Finding | Proposed disposition |
|---|---|---|---|
| F-9 | ACT-v0.4 F-15; RELAY SQ-28 | Every live XC case needs the host's A13 enablement facility with a capture-evidence reference. If SWBPIPE has none, the external channel stays *not enabled* under the App contracts and V4-EXM-25 cannot run at all | Relayed as SQ-28 (new); IN-15 updated |
| F-10 | EXEC-v0.2 F-17; R4-8 with D6 | Until SQ-02 evidences a host-side hold, a workflow with checkpoints cannot pass its check on X, so XC-10's checkpoint parts can show only "unsupported; action during hold recorded". V4-EXM-25 itself declares no checkpoint, so XC-01…XC-09 are unaffected | None beyond SQ-02; visible to the owner with D6 |
| F-11 | ADAPTER-v0.2 PI-2 (F-17) | Seek-before-resubmit cannot be enforced on X; XC-06 now admits a recorded violation. REQ-004's recovery evidence is therefore partly the agent's behavior, not the App's; the joined witness must show which | Recorded in XC-06; no scope change |
| F-12 | EXEC-v0.2 F-21 | The model destination is recorded per run; a model switch between turns in an XC run would need a per-turn record or a new run | DEL-04-03 with DEL-01-01 |
| F-13 | ADAPTER-v0.2 Verification cases | Still say "Evidence labels per the C-v0.3 mapping" and cite C-v0.3/P-v0.3/ACT-v0.3 as contract versions | Minor; re-point at the next ADAPTER revision |
| F-14 | Sweep timing | P, RS, AS, LOOP, PANEL, WD and HOSTING v0.4 texts were not declared final at this sweep; this file cites them at v0.3 | Re-point at the next pass |

### 9.3 v0.2 findings and their disposition at v0.3

| # | Disposition |
|---|---|
| F-9 | Stands; R5-10 states that SQ-28 gates the whole external channel (§3.3 "Gate") |
| F-10 | **Amended by R5-1**: XC-10's A5 case is *not established* (awaiting SQ-02), not "unsupported"; only model-supplied carriage, once SQ-02 is answered with no host-held route (*not established* before that answer), or App-only checkpoints are *not enforceable* (qualified by R7-4 m-5) |
| F-11 | Stands |
| F-12 | **Closed by R5-4**: destination per turn where reported; run-level set; a switch starts no new run |
| F-13 | Stands for ADAPTER-v0.2; R5-9 assigns the re-point to ADAPTER-v0.3 |
| F-14 | **Closed by R5-9**: IN-05/07/08/22/29 and body citations re-pointed to the `8fb51f07f` versions |

### 9.4 New findings at v0.3

| # | Where | Finding | Proposed disposition |
|---|---|---|---|
| F-15 | V3-B m-9 | XF-42 was marked HELD on D6 in v0.2; it is a recording case that needs no ruling. It is now DESIGNED here; ADAPTER should state the same | ADAPTER-v0.3 |
| F-16 | V3-B m-11 | V-ED1's branching is read here as "T1–T15 on e1, e2 published before T16"; C should state it | C-v0.5 |
| F-17 | R5 parallel bumps | Siblings move to v0.5/v0.3 in the same pass; section citations here are to the `8fb51f07f` texts | Re-point at the next pass if a cited section moves |

### 9.5 R6 dispositions (in place)

| # | Disposition |
|---|---|
| F-15 | **Closed**: ADAPTER-v0.3 states XF-42 as DESIGNED, a recording case needing no D6 ruling |
| F-16 | **Closed**: C-v0.5 §10.4 states that V-ED1 replays T1–T15 on e1 and publishes e2 before T16; §4.1 cites it |
| F-17 | Partly closed: header records the current sibling labels; body section citations still refer to the `8fb51f07f` texts |

---

## Changes from v0.2

v0.2 = XT-v0.2 (sha256 28ff092e114f386a723ea7f19d1a6e23a3963b92b44a1383d6308d0c111077c6, committed at `9fc77baa3`). R5 pass under R5_RESOLUTIONS.md (commit `8fb51f07f`).

| R5 ID / source | Change |
|---|---|
| **R6-1** (V4-A MAJOR-1/2) — in place | S-10, IN-25 and UNRESOLVED classify by held actions: host-held class (every held action a host operation; value by SQ-02 status) versus App-side class (*not enforceable* whatever SQ-02 returns) |
| **R6-5** (V4-B m-1, m-2; in place) | IN-14: only "flow, no gate" SETTLED; "record and show" INTEGRATION. S-10, IN-25, XC-10 and UNRESOLVED: model-supplied → *not enforceable* only once SQ-02 is answered with no host-held route (XF-26's variant); *not established* before. TBD-007 cited as DEL-03-03's. F-15 and F-16 closed (§9.5) |
| V4-B m-6 — in place | §4.1 cites C-v0.5's own V-ED1 statement; header adds R6 inputs and current sibling labels |
| **R7-4 m-5** (V5 m-5) — in place | §9.3 F-10 disposition: "model-supplied carriage … *not enforceable*" is qualified "once SQ-02 is answered with no host-held route (*not established* before that answer)", matching S-10, IN-25 and XC-10 (R6-5). No value changes |
| **R5-1** (V3-B MAJOR-5) | S-10, IN-25, XC-10 and UNRESOLVED use the four ruled values. XF-25 → *not established* until SQ-02, then *enforced on the host route*; XF-26 (model-supplied only) → *not enforceable* (*unsupported*); XF-42 → DESIGNED recording case (V3-B m-9); F-10 amended |
| **R5-2** | S-10: only host-held carriage counts; a received constraint keeps its source's assurance unless verified against the host's own copy |
| **R5-4** (V3-B m-1) | S-9 relabelled: D5 SETTLED part vs INTEGRATION (DECISION-2 reading) record-and-show, now per turn; XC-02 updated; F-12 closed |
| **R5-9** (V3-B m-10) | IN-05 P-v0.4, IN-07 ACT-v0.4, IN-08 RS-v0.4, IN-22 LOOP-v0.4, IN-29 AS-v0.4; body citations and header at `8fb51f07f` with sha256; FXA-n throughout; F-14 closed |
| **R5-10** | S-10, IN-25, UNRESOLVED: SQ-02 settles D6 only for host-operation checkpoints; §3.3 "Gate": SQ-28 gates every live XC case |
| R5-7 | No grant-after-arrival case is used here (XF-23's T15 is a grant change outside any checkpoint), so V-GR1 is not cited |
| V3-B m-11 | §4.1 states the reading of V-ED1's branching; F-16 |
| Findings | §9.3 dispositions of F-9…F-14; §9.4 new F-15…F-17 |

Identifiers kept; added F-15…F-17 and §9.3/§9.4.

---

## Changes from v0.1

v0.1 = XT-v0.1 (sha256 8f098c79f1da28af1b461210c36cca1124a25e226e802f2203b46ce7052df8cd, committed at `b4030fe4b`). Sweep A1 under R4 (commit `f05c7e4cd`) and DECISION-2.

| R4 / source | Change |
|---|---|
| DECISION-2 D5; R4-1 (ADAPTER-v0.2 F-15; GUIDE G-4) | New S-9. IN-14 no longer "D5 pending": it asks only whether the host restricts its own channel (SQ-16). XC-01 drops the D5/U-X2 dependency and shows and records the model destination; XC-02 records it |
| DECISION-2 D6; R4-2, R4-8, R4-14 (ADAPTER-v0.2 F-15) | New S-10. IN-25 and XC-10 cite `UNRESOLVED{D6}` (not U-X3/"D6 pending"); only host-held carriage counts; XF-26 and new XF-42 HELD on D6; XF-25 AWAITING INPUT on SQ-02 |
| ACT-v0.4 §2.6, F-15; R4-13, R4-16 | New S-11. IN-15 cites SQ-28; XC-01 (d) requires the host facility's capture-evidence reference; App reporter of *channel not enabled*; F-9 |
| ADAPTER-v0.2 PI-2 (F-17) | XC-06 expected result admits a recorded seek-before-resubmit violation; F-11 |
| R4-20; ADAPTER-v0.2 L-ADAPTER-11/12, XF-40/41 | XC-05 and XC-06 cite the new rehearsals; L-XT-2 = L-ADAPTER-11, L-XT-3 = L-ADAPTER-12 |
| R4-20; C-v0.4 | §4.1 re-pointed to editions e1/e2 and **V-ED1**; L-XT-1 retired; TS-0, TS-1, TR-01 cite V-ED1; FA-n → FXA-n |
| R4-6 | New S-12; XC-10 notes the T15 A12 counts because it was established |
| R4-12 | XC-09 negatives name user-input and elicitation answers as not act evidence |
| Inputs | Header cites C-v0.4, ACT-v0.4, EXEC-v0.2, ADAPTER-v0.2 (working tree, with sha256), R4, DECISION-2, CA-v0.2 and RELAY-v0.2 |
| Findings | §9 split: v0.1 dispositions (9.1) and new F-9…F-14 (9.2) |

Identifiers kept: IN-01…IN-29, J-1…J-8, XC-00…XC-12, TS-0…TS-5, CMP-01…CMP-15, TR-01…TR-10, L-XT-2, L-XT-3, F-1…F-8, VC-T-01…09. Added: S-9…S-12, F-9…F-14. Retired: L-XT-1 (resolves to C-v0.4 V-ED1).

---

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| `UNRESOLVED{OI-003}` retain / narrow / defer | Owner with host contract owner | Before claiming extension capability or fixing its criterion | §5.2 open; no extension pass or savings |
| `UNRESOLVED{OI-021}` operation, autonomy, environment | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and live examination | All cases on FX-PIPE-01; OP-C11 cases HELD |
| OI-005 additional essential hosts | Owner | Before freezing wider examination scope | SWBPIPE only |
| DEL-03-03 TBD-007 MCP versus CLI and realization family (a DEL-03-03 SoW item, not a DEL-09-09 TBD) | App external-host integration owner with external host owner | Before App receiving implementation and qualification | XC cases run per family actually selected |
| DEP-001 host contributions IN-02, IN-09, IN-11, IN-14, IN-15…IN-20, IN-23, IN-24, IN-26…IN-28 | SWBPIPE owner via the human (SQ-nn) | Before corresponding examination | AWAITING INPUT |
| Actual acts: A13 enablement; the engineer's A5 (DEP-09-09-015/016) | The person | At live execution | XC-01 (d), XC-02 positive parts not observable |
| Host restriction of its own channel by model destination (D5 settles the App side) | SWBPIPE owner (SQ-16) | Before a live candidate is enabled | None on App gating; a refusal is relayed |
| `UNRESOLVED{D6}` App-side run holds on X (deferred by the owner to SQ-02) | Owner, on the SWBPIPE SQ-02 answer for checkpoints whose held actions are all host operations; a separate owner follow-up for checkpoints with App-side held actions (R5-10; R6-1); DEL-02-03 computes hold support | Before XC-10 checkpoint parts | XF-25 AWAITING INPUT (*not established*); XF-26 *not enforceable* only in its SQ-02-answered, no-host-held-route variant; XF-42 recording case |
| Host A13 enablement facility with capture-evidence reference | SWBPIPE owner (SQ-28) | Before any live XC case | Channel stays *not enabled* (F-9) |
| DEL-09-01 protocol (outside D1) | DEL-09-01 owner | Before candidate-bound interface evidence | §6 limit |
| Host adoption of D2/D3 and treatments | SWBPIPE owner | Before any enforcement claim (XC-10) | Receiving meaning only |

## Verification cases

Designed, **not run**. Passing them later shows definition completeness; the
witness and trace themselves are §3 and §4.

| Case | Design | Expected result | Serves |
|---|---|---|---|
| VC-T-01 Input account | Check §2 and §8 against the SoW, DEP-09-09-007…020, OI-001/002 (as ruled), OI-003/005/021 and DEP-001 | Every input has supplier, need and standing; defined contracts not treated as available inputs; owners and points of need kept | VER-001 (AC-001) |
| VC-T-02 Access cases | Check XC-01 and XC-12 against V4-HI-50…52 and ADAPTER §3 | Disabled/unavailable explicit; enablement by the person through the host facility only; App-side configuration never A13; model destination recorded and shown, never gating; same route and policy after enablement; host seam not chosen here | VER-002 (AC-002) |
| VC-T-03 Joined chain | Check §3.1, XC-02 and §3.3 against V4-EXM-25 and V4-HI-11, 20…25 | J-1…J-8 all required; engineer's actual act and receipt required; tool success never substitutes | VER-003 (AC-003) |
| VC-T-04 Adverse cases | Check XC-03…XC-08 against REQ-004 | Stale with reason and both bases; no retarget; one effect only from domain evidence; unknown preserved; transport never proof; seek-before-resubmit violations recorded, not hidden | VER-004 (AC-004) |
| VC-T-05 Trace plan | Check §4 against REQ-005 and V4-EXM-24 | Exactly one new operation; all REQ-005 categories present (CMP-01…15); same revision and operation; gaps and non-comparables kept | VER-005 (AC-005) |
| VC-T-06 Disposition | Check §5.2 against OI-003, V4-PAR-05 and REQ-006 | Original promise preserved; ruling recorded not performed; criterion per option; no pass or savings while unruled | VER-006 (AC-006) |
| VC-T-07 Acts | Check XC-09 against #d3, V4-HI-25/30…33, ACT and RS | Positive faithful record with actor ≠ recorder; negatives; accept label; lapse; no acceptance-before-checking dependency; no new reserved list | VER-007 (AC-007) |
| VC-T-08 Evidence standing | Check §3.4 and §6 against EXAMINATION §1–2 | Candidate/configuration/date; outcome values; replay/source/live/native/browser kept apart; receipts linked; rechecks on change | VER-008 (AC-008) |
| VC-T-09 Boundary | Check §7 one-for-one against REQ-009 and CLM-001…004 | Every excluded act has its owner; unresolved decisions kept with their owners; human-relayed handoffs never treated as adoption | VER-009 (AC-009) |
