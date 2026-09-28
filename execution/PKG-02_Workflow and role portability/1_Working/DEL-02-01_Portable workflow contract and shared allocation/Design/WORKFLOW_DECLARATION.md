# Portable workflow declaration, roles, source identity and shared allocation
- Contribution: DEL-02-01/WD-v0.5 (supersedes DEL-02-01/WD-v0.4, committed at `8fb51f07f`, file sha256 `e492ff635de972466c8a932355beeae848e1f3d3f60de7304e88963352d8e88e`; WD-v0.3 sha256 `84841d9f539767b9ff7ae225fec27f0dc4ebbd2c161c41aff179bbae97f345eb`; WD-v0.2 sha256 `c25bccc5f3ac02c84522148eeaa8a6ef0f5eb4a380686773cff45f57a448a55c`; WD-v0.1 sha256 `bacfcb71ca9585b950444c0218fdd5283f5b2f5d0c8f981411395278b286fc5e`)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001, OUT-002, OUT-003 (map version), OUT-004 (fixture design only); REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006; AC-001…AC-007 by designed verification; VER-001…VER-007 (cases designed, none run)
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 080d7f5a8e55d93c06f51e5332b53954deb03e0877b1ee49be3011e3de14a294; P/docs/PRD.md §2.2 (V4-HOST-05/06), §2.4 (V4-SHR-01…03), §4.1 (V4-WF-01…06), §4.2 (V4-ROLE-01…03), §4.3 (V4-EXE-01/03), §4.5 (V4-AUT-01…05), §4.7 (V4-REC-01…05); P/docs/ARCHITECTURE.md §1 (M-1, M-3, M-5), §4, §5 (V4-ARC-20/21); P/docs/HOST_INTEGRATION.md §1, §2 (V4-HI-02…04), §3 (V4-HI-11/12), §4 (V4-HI-20…25), §5 (V4-HI-30…33), §6 (V4-HI-40…42), §9 (V4-HI-70/71); P/docs/EXAMINATION.md V4-EXM-10, -14, -21, -22; DECISION_BRIEF.html #d2, #d3, #d5; SCC-CASE-002 Case_Datasheet M1 rows; Open_Issues.csv OI-003, OI-013, OI-014, OI-018, OI-021; owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (OWNER_DECISIONS.md sha256 `f3f8e5f31ec87006fc9ab459c6ae57d08638439c234fa959ba2605914cf81f2e`), rulings D1 (scope), D2 (OI-001), D3 (OI-002); owner decision `APP-V4-FIRST-INCREMENT-20260928-DECISION-2` (OWNER_DECISIONS.md at `f05c7e4cd`, sha256 `a9869129753631b865cbbb00a138c0f497d5ac8a4b67f5746169d1f9a668ad2c`), D5 (external-channel model destination: user flexibility) and D6 (App-side run holds deferred to SWBPIPE SQ-02). Root reuse sources read (not adopted): `workflows/WORKFLOW_TEMPLATE.md`, `workflows/*/execution.json` (66 companions surveyed), `workflows/catalog.yaml`, `workflows/catalog.schema.json`, `workflows/index.json`, `workflows/create-workflow/WORKFLOW.md`, `docs/SPEC.md` §9.1–9.8, `docs/AGENT_WORKFLOW_RUNTIME.md`.
- Consumed inputs:
  - **R6 micro-rulings (binding, applied in place, no version bump).** R6_RESOLUTIONS.md sha256 `8703e85aa7324e233fab285321e277d720923d3e36e342c865917b55083cb841` (R6-1, R6-2, R6-3, R6-4); review V4-A sha256 `121deafc40c4baf0dec71f96eb449083b0d93456c2bd448f89a279951ca2eab1` (MAJOR-1/2; m-1, m-3, m-4, m-9); DEL-02-03 EXEC-v0.3 §3.5–§3.6 read in the working tree, sha256 `b147d9862fe9e0228139c72ba13c50392dcf66930109c4357587bf97bbdebf42` (HS-1…HS-5, evaluation order HS-1, HS-2, HS-5, HS-4, HS-3; F-28). Sibling versions at `d3cebd1cc`: C-v0.5 `a6306bd4…7a29` (V-GR1, GR-1…GR-3, GR-P, GR-R, GR-S, run 13), ACT-POLICY-v0.5 `86975a90…80e7`, LOOP-v0.5 `43e039aa…01ca4`, P-v0.5 `a5ee4946…d1b7` (headers checked). (C `a6306bd4…7a29` is the pre-R6-2 byte state; the R6 state of C is `298e4258…2364`, below — R7-4 m-8.)
  - **R7 repair (in place, no version bump).** R7_RESOLUTIONS.md (R7-3; R7-4 m-5, m-8) and `reviews/V5.md` (MAJOR-3; m-5, m-8). Sibling inputs read at the R7 working state: first at candidate `2f42fba02` — EXEC-v0.3 `EXECUTION_COMPATIBILITY.md` `b147d986…bf42` (§3.5, §3.6 HS-1…HS-5 and the held-actions definition); WD-EX-v0.5 `EXAMPLES.md` `b1b7f10e…3362` (E8); C-v0.5 `CATALOG_AND_READ_BASIS.md` `298e4258…2364` (V-GR1); ACT-POLICY-v0.5 `d539b384…9293`; LOOP-v0.5 `0ec980b5…d737`; P-v0.5 `6ab94fd1…37e0` (headers checked) — then with the R7 edits made in place to EXEC, WD-EX, C and ACT in the same repair, each recorded in that file's R7 rows. The post-R7 bytes of every Design file are pinned in GUIDE's input table (R7-4 m-1).
  - **Final alignment rulings (binding).** R5_RESOLUTIONS.md at `8fb51f07f`, sha256 `254d0b93b9959419a70c6737b07087e1db59b529adc3105a1db31f82b78dd6f1`: R5-1, R5-2, R5-3, R5-7, R5-9 (others read for context). Reviews V3-A sha256 `f25f5af1177b7fe2a698bd4ef1e1caafa4c2ef25cfc73111f031e17c7cc21d87` (MAJOR-1, m-2, m-3, m-6, m-10, m-12 as they concern WD/WD-EX) and V3-B sha256 `5662fbd09025f5ad9459861370159d606fcced76b394980199e861555a1954a3` (WD-EX framing note).
  - **Current sibling texts read at `8fb51f07f`** (via `git show`): DEL-02-03 EXEC-v0.2 `EXECUTION_COMPATIBILITY.md` sha256 `7f7848c0de2fdb4dc21f5adafa97f92e179bb66c9f6b04f3434d8f2342317af0`; DEL-03-01 C-v0.4 `CATALOG_AND_READ_BASIS.md` sha256 `e929d39d3ff9515702f9bfe51dfada537e1cbd165146ec0de4ccf629c659a08c` (§10.1 FXA-1…FXA-5, LIB-A1, LIB-A2, AF-1; §10.4); DEL-04-01 ACT-POLICY-v0.4 sha256 `d6da05abe790a4374df7faf225439a01dc1be734491b499d90cf00533369b03b`; DEL-05-01 LOOP-v0.4 sha256 `ffc3048333f3370ba09a9ce124159b94f2c80ce69b5f593bfb82cc552f95934e`; DEL-03-02 P-v0.4 sha256 `0d3960a2e6bd3520368006cdd2b1b67a1fe4eb06e23184aded9d5b98d6c5e361`; DEL-09-06 CA-v0.2 sha256 `31ea3bff05865f425127009f90c070f26b97972e203b5a235791d00332d8dee1`. Elements R5 assigns to siblings' v0.5/v0.3 (e.g., C V-GR1) are cited "per R5-n; sibling to confirm".
  - **Sweep A1 rulings.** R4_RESOLUTIONS.md at `f05c7e4cd`, sha256 `50a009b2ef487bad6ef5e89b5c4493095f18f83149fcb83b00050de485032a24`: R4-2, R4-3, R4-4, R4-5, R4-6, R4-7, R4-8, R4-9, R4-12, R4-14, R4-16, R4-18, R4-19, R4-20, R4-21 (others read for context). V2 review `reviews/V2.md` sha256 `75ba1dff8a0c4fa2eb294471127147cbd19a0925daf9169b32ddc88727dde6ef` (MAJOR-1; m-3, m-8, m-9, m-12, m-13 addressed to WD/WD-EX).
  - **Sibling texts read at commit `f05c7e4cd`** (via `git show`, not the working tree): DEL-02-03 `EXECUTION_COMPATIBILITY.md` EXEC-v0.1 sha256 `e0ede76ebf08003511755afc666be2466a867fd3256837ee94300cd0dfe518e8` (§2 hold points, §3.5–§3.6, §4, §5, §6, §11 F-1…F-16); DEL-09-06 `CONNECTED_ACTIVITY_CONTRACT.md` CA-v0.1 sha256 `685349b25981ca8333929207890514120d63753cdedd67ae0bad986fc5d45e62` (§3.2 L-CA-1; F-5, F-7); DEL-03-01 `CATALOG_AND_READ_BASIS.md` C-v0.3 sha256 `ba45e7393ee0b16780f36605ddeecb95ba1f181488e36a46b4b495b69fd67c26` (§3, §4.1, §10); DEL-04-01 `ACT_AND_POLICY_CONTRACT.md` v0.3 sha256 `b3748c02006f939d8cc78c6e0b0c847598a8b32d55515ae8658ad80597c98128` (§2.1, §4.2). Elements R4 assigns to siblings' next versions are cited "per R4-n; sibling v0.4/v0.2 to confirm".
  - **Earlier integration rulings.** R2_RESOLUTIONS.md sha256 `77cfb845ec305365f12218f83f332069155de5f362139b7a6fe2bf12cdebd088` (R2-1, R2-2, R2-3, R2-4, R2-5, R2-7, R2-8, R2-9, R2-10, R2-11, R2-12, R2-13, R2-14, R2-15, R2-16, R2-17, R2-18, R2-19, R2-20, R2-21). R1_RESOLUTIONS.md sha256 `2f9c7e72aa8362624ad830377a70077b27a27bf03871f8e87811a28e6e177ec4` (R-1…R-9, in force unless amended by R2). R3_RESOLUTIONS.md sha256 `202d52c7d688382336cddb0d6c31be27969a9e667c5800b734428a090f05afbf` (R3-1, R3-2, R3-3; in-place micro-edits, no version bump).
  - **Reviews.** IR1-C.md sha256 `295e96b3f5871cdf4142df169dc8811cef0aa38e7a7eb1930b246f60f0a426b9` (all items addressed to DEL-02-01); IR1-A.md sha256 `31b3c7f8493f05ee5fed6a11208f6811d2449d8a4fe72aae6300c2850b648284` and IR1-B.md sha256 `70e4a4f6d88f475687a9fde56a566a6913081dd3dd560402c1db8996dffd2846` (items addressed to DEL-02-01). Earlier: V1-A `01811533…c04c09`, V1-C `8d46258a…94a6`.
  - **Sibling v0.2 texts read at commit `28bd00499`** (via `git show`, not the working tree): DEL-03-01 `CATALOG_AND_READ_BASIS.md` C-v0.2 sha256 `358182b18b1fe13f9af6e6f5a61c9ed57f91b6ab29ea0c9adab06fe0081d6d82` (§3, §4.1, §5, §10); DEL-04-01 `ACT_AND_POLICY_CONTRACT.md` v0.2 sha256 `e50f1fe2f5bb2e3280bc62175e5aeeaa4508eed713424d82c54536a9fb5993a9` (§2.3–§2.5, §4); DEL-05-01 `LOOP_RECEIVING_CONTRACT.md` LOOP-v0.2 sha256 `1151d432c106ed3c1980918eca9d9360116292e3b9c602ed67f4c2d6718762c9` (§2.4); DEL-03-02 `PROPOSAL_LIFECYCLE_AND_OUTCOMES.md` P-v0.2 sha256 `942c1a3ab5ad7bda865640067f0fd550d7cfd1acd8f6ee228f6906452adf8c89` (§4.3, §9). Where R2 amends these texts for v0.3, the amended element is cited "per R2-n; sibling v0.3 to confirm".
  - DEL-05-02 PANEL-v0.2 needs known through IR1-C J2/J3 (file not read). DEL-02-02, DEL-02-03, DEL-02-04: accepted SoWs only. SWBPIPE consumer needs: none received.
- Receivers: CASE-002 M1 "Workflow-contract owner" row: DEL-02-03 (OUT-001, OUT-002; REQ-001, REQ-002, REQ-004; VER-001, VER-002, VER-004; W7 in this undertaking); DEL-05-01 (OUT-001, OUT-004; REQ-005, REQ-007; VER-008); DEL-05-02 (OUT-001; REQ-001; VER-001); DEL-02-01 self-check (OUT-004; REQ-004, REQ-005; VER-004, VER-005). DEL-02-02 (OUT-001, OUT-004; REQ-005; VER-004) and DEL-02-04 (OUT-001, OUT-002; REQ-001, REQ-002, REQ-004; VER-001, VER-005) remain named receivers but are outside this undertaking per owner ruling D1. Later: DEL-03-04 (W10), DEL-09-06 (W9).

Companion: [EXAMPLES.md](EXAMPLES.md) (DEL-02-01/WD-EX-v0.5).

---

## Changes from v0.4

| R5 ID (source) | Change in v0.5 | Where |
|---|---|---|
| R5-1 (V3-A MAJOR-1; V3-B MAJOR-5) | §4.3.8 now uses the **four ruled hold-support values** owned by EXEC §3.6: *enforced by the host loop*, *enforced on the host route*, *not established*, *not enforceable*, with their check effects (pass · pass · *not established* · *unsupported*). "Enforced before dispatch" and "held after observation" retired; the v0.4 "A5 on the host route passes with AWAITING INPUT" exemption withdrawn: pending SQ-02 is *not established*. Pass rule extended. U-30 restated (App-only checkpoints *not enforceable* whatever SWBPIPE answers; SQ-02 decides host-operation checkpoints only, per R5-10). | §4.2.4, §4.3.8, I-9, U-19, U-30, VC-37 |
| R5-2 (V3-A m-6; V3-B MAJOR-1) | Carriage assurance final: **host-held** (host derived it from, or verified it against, its own resolved copy; includes the host loop's own evaluation); a constraint the host merely received keeps its source's assurance; **App-assured is not available in this increment**; only host-held satisfies R2-12. | §4.2.2, I-7, EXAMPLES R-5b |
| R5-3 (V3-A m-5; Y-2) | The **declared** setting content always binds an A12 checkpoint and must always be named; invalidity is unconditional; an A8 may present that content but never changes the subject; an A12 on different content satisfies nothing; a run-dependent scope is declared as a **binding rule resolved at arrival** (e.g., "targets of the held call"), never chosen by an A8. | §4.3.1, §4.3.6, FB-17 |
| R5-7 (V3-A MAJOR-3/5) | EXAMPLES R-16 (ii)–(v) re-pointed to C **V-GR1** (per R5-7; present in C-v0.5); **L-WDEX-11 retired, not reused**. R-16 (i) stays the main-order negative. U-31 records the owner-visible cost. | EXAMPLES, U-31, VC-32 |
| R5-9 (V3-A m-1, m-2, m-3, m-12; V3-B) | Citations re-pointed to current sibling versions (EXEC-v0.2, C-v0.4, ACT-v0.4, LOOP-v0.4, P-v0.4, CA-v0.2); FA-n → **FXA-n**; ⟨fx-proj⟩ → **LIB-A1**, plus LIB-A2 and AF-1; FXA-5 stated correctly (⟨rev-3⟩ declares `CP-accept` **and** `CP-check`); "pending its v0.4" markers closed. L-WDEX numbering kept stable (EXEC cites it). | Header, §8, U-23, EXAMPLES |
| V3-A m-10 | MX-8 row rejoined to its table; FB rows ordered 16, 17, 18. | §4.3.7, §11 |
| R6-1 (V4-A MAJOR-1/2; EXEC F-28) — in place | Hold support is decided by **held actions**, not by arrival: §4.3.8 adds the assignment rule (EXEC HS-1, HS-2, HS-5, HS-4, HS-3 in that order; HS-3 by SQ-02 status). New §4.3.1 element **held actions** (INTEGRATION), declared as "host operations only" or as listed App-side steps, with the conservative default. E1d via X includes E1c's `CP-check` → **unsupported**; E1c via X → **unsupported**. WR-11 advice stated. VC-37 updated; new VC-43. | §4.3.1, §4.3.8, VC-37, VC-43, EXAMPLES E1/E1c/E1d/E8 |
| R6-2 (V4-A m-3) — in place | EXAMPLES R-16 (iv): in V-GR1 (GR-R) the refused A12 is T15's own, so **⟨set-1⟩** stays in force. | EXAMPLES R-16 |
| R6-3 (GUIDE-v0.2 G-11) — in place, parent | I-4 re-hold sentence qualified per hold-support value (the run stops only under *enforced by the host loop*). Applied by HELP_HUMAN. |
| R6-3 (V4-A m-4) — in place | I-9 and §4.3.8 state what "held" means per value: host loop → the run stops at its next action; host route → the host refuses the held host operations, other actions are *action during hold*; not established / not enforceable → nothing is stopped, actions are *action during hold*. | I-9, §4.3.8 |
| R6-4 (V4-A m-1, m-9) — in place | Stale "pending"/"C-v0.5 to add" markers removed (V-GR1 exists in C-v0.5); §8/§9 version labels corrected to v0.5; supplier states re-pointed; VC-41 cites R4-9 and R5-3, "even with an A8 presenting a setting". | Header, §8, §9, VC-41 |
| **R7-3** (V5 MAJOR-3; INTEGRATION, option (a)) — in place | §4.3.1 *held actions*: when the element is absent, the held actions are **derived** — the governed operation(s) for an A5 checkpoint, the held call for a kind (a) checkpoint (as EXEC §3.6 defines them). The conservative default (at least one App-side step, EXEC HS-5) applies only when a kind (b)/(c) checkpoint has no held-actions element, or when its declared held actions do not show host operations only. §4.3.8 HS-5 row scoped the same way. VC-43: the L-WDEX-17 checkpoint (kind (a) `CP-grant` on OP-C9) with no held-actions element is HS-3 → **not established** today (was HS-5 → *not enforceable*); its workflow result follows EXEC §3.5 precedence with the run's other checkpoints — L-WDEX-17 has none, so **not established** today. No other value changes | §4.3.1, §4.3.8, VC-43, EXAMPLES E8 |
| **R7-4 m-5** (V5 m-5) — in place | §4.3.8 value table: "a constraint carried only as *model-supplied*" → **not enforceable** is qualified "once SQ-02 is answered with no host-held route (HS-3; before that answer, *not established*)" | §4.3.8 |
| **R7-4 m-8** (V5 m-8) — in place | Header: the R6 line notes that C `a6306bd4…` is the pre-R6-2 byte state; a new R7 line records the sibling inputs read at the R7 working state (EXEC, WD-EX, C, ACT, LOOP, P at `2f42fba02`, then with their R7 in-place edits); GUIDE pins the post-R7 bytes | Header |

## Changes from v0.3

Keyed by R4 ID and source finding. Labels as in R1–R4.

| R4 ID (source) | Change in v0.4 | Where |
|---|---|---|
| R4-2 (D6; EXEC §3.6, HP-1/HP-2) | New §4.3.8 **hold support**: every checkpoint has a per-surface hold-support value (EXEC §3.6). App-side run holds are `UNRESOLVED{D6}` pending SWBPIPE SQ-02; the declaration never implies an App hold that cannot be enforced; "action during hold" is recorded; neither interposed App code (HP-1) nor reliance on `turn/interrupt` (HP-2) is adopted. HP-3 stays a permitted best effort (D3). New settled row S-T (D6). | §2, §4.3.8, I-9, U-30 |
| R4-3 (EXEC §4.7; W7 F-2) | I-4 rewritten: resume point HD-5; a lapse after resume re-holds the **same arrival** ("waiting — re-held, lapsed at ‹t› after resume"), the run stops at its next action, nothing is undone, gated outputs show *lapsed*, the whole scope is re-requested; A5 and A12 never re-hold. The interim "performed + act-lapsed" display is withdrawn. U-22 closed. | I-4, §4.3.4, U-22 |
| R4-4 (EXEC §4.9; W7 F-4) | No resumption of an ended run; acts after run end are shown "after run end" and change nothing; continuation is a new run with a **continues ⟨run⟩** link, inheriting nothing; an interruption is not a run end. PROPOSED. U-21 closed. | §4.3.4, U-21 |
| R4-5 (EXEC SP-6; W7 F-3) | New I-8: an act counts only if captured at or after the checkpoint's arrival; earlier acts shown "prior act on this subject, not counted". PROPOSED; the owner alternative stays open as U-31 (EXEC U-E4). EXAMPLES R-16 repaired against C's T15→T16 order. | I-8, U-31, EXAMPLES R-16 |
| R4-6 (EXEC §4.10; W7 F-5) | SB-4 rewritten: an A12 counts and supersedes only when **established**; a refused A12 neither counts nor supersedes a setting in force; pending → *waiting*; lost confirmation → *unknown*. U-27 closed. | SB-4, U-27 |
| R4-7 (EXEC §4.11; W7 F-1) | §4.3.7 adds MX-3 (lost decision observation → *unknown*), MX-6 (all items left → arrival closed "replaced by arrival n+1") and MX-8 (application error or outcome unknown after A5 → unchanged, annotated). R2-18 and R3-3 **CONFIRMED** by DEL-02-03. U-20 closed. | §4.3.7, U-20 |
| R4-8 (W7 F-8) | *unsupported* gains the reason **"checkpoint hold not enforceable on this surface"** (from EXEC §3.6). | §4.2.4, §4.3.8 |
| R4-9 (W7 F-13) | A12 subject without an A8: the setting content named by the checkpoint's own declaration (classes, grant values, scope). An A12 checkpoint naming none is **invalid** (new FB-17). INTEGRATION. | §4.3.1, §4.3.6, FB-17 |
| R4-12 (W7 F-9) | I-5: answers to Codex user-input or MCP elicitation requests are **not act evidence** and never host act capture (EXEC CAP-6). U-25 narrowed to App act-control construction (EXEC §5). | I-5, U-25 |
| R4-14 (W8 F-1) | §4.2.2 no longer says "the external adapter carries". The constraint is carried with a **carriage assurance**: App-assured, host-held, model-supplied or absent; model-supplied alone does not satisfy R2-12. | §4.2.2, I-7 |
| R4-16 (W8 F-7) | *channel not enabled*: the App reports it when its own configuration is off; the host when its channel is off. | §4.2.4 |
| R4-18 (V2 MAJOR-1) | EXAMPLES R-5a/R-5b re-pointed to C V-CP1 and R-5c to C T15/⟨set-2⟩ (class P-03, scope {FX-W1; {S-4}}); local L-WDEX-2 removed. | EXAMPLES |
| R4-19 (V2 m-3, m-8, m-9, m-12, m-13) | OP-C10 class per R3-4 (governed by the reversed operation's policy record); m-8 framing stated (WD-EX runs use its own declared checkpoints; C declares only V-CP1); "C-v0.3 to add" and "to be confirmed at V2" markers closed; examples re-pointed to C-v0.3 §10 (T4a, T16a, S-5, V-S1, V-R1, V-X1, V-NP1, V-OU1); R3 and R4 added to Consumed inputs. | Header, EXAMPLES |
| R4-20 (W9 CA F-5) | E1 adopts optional OP-C12 host-check steps at Inspect and Re-examine (was DEL-09-06 L-CA-1). | EXAMPLES E1 |
| R4-21 (W7 F-16) | Reached-when kind (a) on a **harness capability** is not holdable in App runs pending D6; hold support reports *not enforceable* (new FB-18). | §4.3.1, §4.3.8, FB-18 |
| (W7 confirmations) | Holding library confirmed with HL-2/HL-3 (EXEC §6.2); transfer procedure and adaptation receiving supplied (EXEC §6.3–§6.7). U-24 and U-18 closed as PROPOSED (W7). | §6.4, U-18, U-24 |
| (EXEC U-E7) | "On subject absent" declaration path recorded as open (U-32); default is EXEC's *waiting* "subject absent". | U-32 |

## Changes from v0.2

The v0.1 → v0.2 change table is in the committed WD-v0.2 (sha256 above).

| Item | Change in v0.3 | Where |
|---|---|---|
| R2-17; IR1C-05; IR1C-01 (X-10) | **subject class** is its own element with the closed class list: change items of a named proposal · named output · objects changed by a named outcome · targets of the held call · grant setting. Binding rules per class. An A5 checkpoint must use reached-when kind (c) *queued* and subject class "change items of the named proposal" (new FB-16). "Targets of the held call" is valid only with kind (a) (IR1-C X-10 point 1, not contradicted by R2). Consumers bind the declared class, never infer it from the kind. | §4.3.1, §4.3.6, FB-16 |
| R2-18; IR1C-02 (X-14) | §4.3.7 stays the proposal all files cite. "Partial" is a per-item annotation, not a disposition. Items that leave without a decision are shown with their item-left events (supplied by DEL-03-02). A *performed* over a reduced subject is never shown as "all accepted". | §4.3.7 |
| R2-19; IR1C-07; IR1A-09 | Lapse sequence: an **act-lapsed event** is recorded; before resume the disposition returns to *waiting* ("waiting — lapsed at ‹t›"); after resume, re-hold is DEL-02-03's; *lapsed* as a standing disposition only for a checkpoint whose run has ended. | §4.3.3 I-4, §4.3.4 |
| R2-5; IR1C-08; IR1A-03, IR1A-18 (X-2, X-12) | "decline/stop event" renamed **act-declined event** (A4, A6, A7, A12; with capture evidence) → *resolved negatively*. Stopping the run is a separate **run-ended event**; a reached checkpoint stays *waiting*. An act after the run ended is recorded but does not change the ended run's disposition unless DEL-02-03 defines resumption. U-21 closed except resumption. | §4.3.3 I-6, §4.3.4, U-21 |
| R2-12; IR1C-03 (X-9) | The checkpoint-forced treatment travels as a **governing checkpoint constraint** {workflow run, checkpoint name, required act A5, operation}, carried by the loop and the external adapter in the change request (P §3.3, sibling v0.3). Direct request under it → *not permitted*, naming the constraint. VC-11 is **AWAITING INPUT** until host evidence exists. U-19 narrowed to the relay question. | §4.2.2, I-7, U-19, VC-11 |
| R2-7; IR1A-04 (X-13) | A12 binds to the **setting content** (classes, grant values, scope); a later A12 **supersedes**, not lapses; a checkpoint satisfied by the earlier A12 stays *performed* with the supersession shown. Whether a control-refused A12 can count is held for W7. U-27 narrowed. | §4.3.6 SB-4, U-27 |
| R2-20; IR1C-09 (X-11) | Holding library recorded at the *listed*, *selected* and *resolved* links; shown by the panel; carried in the loop's run association; never in identity equality; collision reports list it with each origin. PROPOSED until W7. | §6.2, §6.4 |
| R2-20 (X-17, X-18) | Capture-evidence reference and per-turn supplied-guidance identity stated as relay questions with consequences: no capture-evidence reference → no host-content checkpoint can be *performed*; no per-turn guidance record → *supplied* link *unknown*. | I-5, §6.2, U-05b, U-29 |
| R2-10; IR1C-22 | Recognized act kind outside the closed list → **invalid**; unrecognized name → **not established** (kept; DEL-04-01 aligns). | FB-03, FB-04 |
| R2-4 | Reserved entries are always offered, never reported *not exposed on this surface* for a class reason. At run time *not exposed on this surface* is reported by the host from element 9; an operation absent from the catalog edition offered to the loop is a loop-side *not offered* failure. The discovery-time requirement check still reads element 9. | §4.2.4 |
| R2-13, R2-14, R2-15, R2-16 | Binding uses the applied outcome's created/changed object identities and their post-application subject content identities (R2-14). Undo *reverses ⟨receipt⟩*; acts on content the undo changes lapse normally (R2-15). Accepted-then-stale: A5 not lapsed; item shown "accepted by ‹person› — not applied: refused — stale (both bases)"; checkpoint effect per §4.3.7 row added (R2-16). Retry de-duplicates by proposal identity before any basis check (R2-13). | §4.3.6, §4.3.7, §4.6 |
| R2-1 | Class element has five values including **no policy basis** (reason ∈ omitted, unassigned, pending OI-021); the declaration still does not restate classes. | §4.2.2 |
| R2-11 | Attribution checked: D2/D3 credited only with what they say; restrictions derived from R-2/R2 labelled DERIVED or INTEGRATION. | §2 S-Q, S-R, S-S |
| IR1C-13 | Requirement-check **pass rule** added: passes when every *required* reference is *present* or *present, currently unavailable* (the latter a run-time hold); optional references never block; undeclared stays selectable, never "runnable by check". | §4.2.4 |
| IR1C-14a/b | Purpose and scope bind with the act (V4-REC-05) and are carried with every act request at a checkpoint. | §4.3.1 |
| IR1-B B-m9 | Read-basis descriptor listed with five elements, adding the **identity method designation** (C §5.1). | §4.1 |
| R2-21; IR1C-15; IR1-B B-M8/B-M9/B-M10/B-m11 (X-6) | Examples re-pointed to C-v0.2 §10 identifiers (OP-C1…C9, T1…T17, S-1…S-4, PR-1/PR-2, RC-1…RC-3, B1/B2) plus OP-C10/OP-C11 fixed by R2-21. OP-C3 is **Examine** (A3 findings), not a host check. Fixture exposure assumed "exposed on all three surfaces" per R2-21 (C-v0.2 still shows *unagreed*). Local cases named `L-WDEX-n`. U-26 closed. | EXAMPLES |
| R3-1 (from finding F-1) | New subject class **objects a named output concerns**: objects identified in a named read/examination output, bound through their subject content identities as read. INTEGRATION. U-28 closed; E1b and VC-08 use it; new VC-36. | §4.3.1, §4.3.6, U-28, EXAMPLES E1b |
| R3-2 (from finding F-7; IR1-C X-10) | *Targets of the held call* valid only with reached-when kind (a) *before dispatch*: adopted as INTEGRATION (was cited to IR1-C only). | §4.3.1 validity rules, FB-16 |
| R3-3 (from finding F-4) | §4.3.7 accepted-then-stale row adopted as proposed: disposition unchanged, item annotated "not applied: refused — stale", output not produced for that item. PROPOSED; DEL-02-03 confirms at W7. | §4.3.7, U-20 |

Not repaired here (routed to closeout C1): V1-C RF-3 (no DOWNSTREAM rows),
RF-7 (U-08 register row), X-16.

---

## 1. Reading this definition

**What it defines.** The meaning of a portable workflow's *declared part* and
its relation to the prose method. The four roles and the single host seat as
App and host consumers receive them. Workflow source identity and the
promised-versus-observed distinction. The shared-contract responsibility map
(OUT-003), with each consumer need and each open allocation labelled.

**What it does not define.** It does not choose a wire format, field names,
where the declared part is carried, JSON or TypeScript types, a parser, a
content-identity algorithm, a transport (MCP or CLI), persistence,
process/thread placement or shared-component placement. It does not define
catalog entries (DEL-03-01), act kinds or policy (DEL-04-01), proposal
outcomes or the change request (DEL-03-02), record fields (DEL-04-03), the
checkpoint hold machine or transfer behavior (DEL-02-03), registration
(DEL-02-02), role supply (DEL-02-04), loop events (DEL-05-01) or panel
interactions (DEL-05-02).

**Naming convention.** Bold phrases such as **expected input** or
**reached-when** are *semantic element names*, not wire names, keys, headings
or type names. Act kinds use the canonical names A1–A14 (R-1; DEL-04-01 §2.1).

**Normative words.** "Shall" marks a meaning this contribution proposes.
"Settled" marks an accepted-basis distinction or an owner ruling, cited.
DERIVED / INTEGRATION / PROPOSED follow the R1/R2 labels. `UNRESOLVED{…}`
marks an open owner choice, which is neither a permission nor a default.

---

## 2. Settled distinctions this definition carries

| # | Settled distinction | Citation | Consequence for the declaration |
|---|---|---|---|
| S-A | A workflow is prose method guidance plus a declared part: expected inputs, host tools needed, checkpoints requiring a human act, returned outputs and evidence. | PRD V4-WF-01 | Five declared categories, prose retained (§3–4). |
| S-B | Workflows, skills and role guidance are ordinary open files (`WORKFLOW.md`, `SKILL.md`, `AGENTS.md`) readable by any capable harness; tool schemas stay open. | PRD V4-SHR-02; ARCH M-3 | The declared part must be readable without Chirality software (§3.2). |
| S-C | One workflow format and one set of four roles across the App and every host. | PRD V4-SHR-01, V4-ROLE-01 | No host-specific declaration dialect (§5). |
| S-D | Source-qualified identity: project, user, bundled or host-supplied; a selection is never silently rebound to a same-named workflow from another source. | PRD V4-WF-03 | Four origin classes; collisions exposed (§6). |
| S-E | The product can check that a selected workflow's required tools exist in the current host and tell the person when they do not. | PRD V4-WF-04 | Required tools are referenceable against the host catalog (§4.2). |
| S-F | At a declared checkpoint the required human act is requested; the run does not record it as done until the person performs it; checkpoints override autonomy. | PRD V4-WF-05; HI V4-HI-42 | Checkpoint hold is independent of the grant (§4.3). |
| S-G | `success` means the operation ran; a submitted proposal reports "queued" until the host records acceptance and application. | HI V4-HI-25 | Success never satisfies a checkpoint (I-2). |
| S-H | Applying a change, accepting an edit, marking work checked, engineering approval and professional reliance are distinct; agents may prepare but must not represent an unperformed human act as performed. | PRD V4-AUT-03; HI V4-HI-30/31; d3 | Each checkpoint names one act kind; evidence of one kind satisfies no other (I-1). |
| S-I | Proposals say "accept", never "approve". | HI V4-HI-33 | "Accept" wording stays with A5 only (R-1). |
| S-J | A human act binds to identified content, scope and purpose and lapses visibly when that content changes. | PRD V4-REC-05; HI V4-HI-32 | Checkpoint subjects are bound to observable referents (§4.3.6). |
| S-K | Only observed events are shown as having happened; unobserved outcomes are unknown. | PRD V4-EXE-03 | Promises are kept apart from observations (§4.6). |
| S-L | Nothing the agent produces is presented as certified, sealed, approved or code-compliant. | PRD V4-AUT-05 | Outputs cannot promise approval standing (§4.4). |
| S-M | Roles recede in hosts behind one agent seat and the selected workflow; each host carries its own workflows, skills and tools. | PRD V4-HOST-05/06 | Host seat and host origin (§5, §6). |
| S-N | Roles are supplied additively; a bounded executor does not delegate; unenforced limits are stated, not implied. | PRD V4-ROLE-02/03 | Role compatibility is declared, not claimed as enforced (§4.7, §5). |
| S-O | Shared meaning does not prescribe a common executable service; shared implementation needs a concrete repeated responsibility; placement is open. | ARCH V4-ARC-20; PRD V4-SHR-03; d2; OI-014 | Map records needs and leaves placement open (§9). |
| S-P | A run leaves a compact record linking host receipts rather than copying them. | PRD V4-REC-04; HI V4-HI-70/71 | Declared evidence is by reference (§4.5). |
| S-Q | Reserved to the person (App/shared contracts, first increment): (a) marking work checked; (b) accepting a proposal wherever the active autonomy requires a proposal; (c) engineering approval; (d) relying on a result for a professional purpose; (e) changing the autonomy grant or **enabling** external-agent access. No autonomy grant widens past a reserved act or a declared checkpoint. The host names and enforces its own list; this does not show SWBPIPE adoption (DEP-001). | Owner ruling D2 (DECISION-1) | Mapped to A4, A5, A6, A7, A12, A13. Every act a checkpoint may require is reserved (§4.3.2). |
| S-R | In the App, routine tool-permission and sandbox modes (including any classifier mode) remain the user's own Codex setting; they govern tool execution only and never stand in for a reserved or professional act. In hosts there is no classifier permission mode in the first increment; the SWB default proposal mode applies. | Owner ruling D3 (DECISION-1) | A14 never satisfies a checkpoint; a checkpoint is not a permission prompt (§4.3.2). |
| S-T | App-side run holds at checkpoints are deferred to the SWBPIPE answer to relay question SQ-02 (`UNRESOLVED{D6}`). Meanwhile: per-checkpoint hold support is carried; no App hold that cannot be enforced is claimed; action during hold is recorded; neither interposed App code nor reliance on `turn/interrupt` is adopted. | Owner decision D6 (DECISION-2), as applied by R4-2 | §4.3.8; I-9 |
| S-S | Not settled by D2/D3 but carried: A10 is reserved wherever A5 is (DERIVED, R-1); an operation that performs A4, A5, A6, A7, A10, A12 or A13 is reserved to the person (DERIVED, R2-2); disabling external access is recorded as A13 (INTEGRATION, R2-3); an acceptance checkpoint forces a proposal (DERIVED from V4-HI-42 + D2b, R-5). | R-1, R-5, R2-2, R2-3, R2-11 | Labels kept distinct from the owner rulings. |

---

## 3. The workflow package and its two parts

### 3.1 Parts

A portable workflow is one package whose entrypoint is `WORKFLOW.md` (S-B).

| Part | Job | Who reads it | Authority |
|---|---|---|---|
| **Prose method** | Explains purpose, applicability, method, branches, recovery, judgment and handoff. | People and agents. | Method guidance; it grants no permission (Root `create-workflow`, retained). |
| **Declared part** | States, in a form a product can observe, what the method expects, needs, stops for and returns. | People, agents and product consumers (requirement check, checkpoint hold, records, panel). | A declaration of expectations. It is not evidence that any expectation was met and grants no host permission. |

Both parts are required for a *declared* workflow. Where they disagree, the
consumer reports the inconsistency (FB-07) and does not silently prefer
either.

### 3.2 Readability obligations (OUT-001, OUT-002; REQ-001, REQ-002)

- **R-1** The declared part shall be readable as ordinary text by a person
  opening the package in an ordinary editor, without Chirality software,
  generated indexes or a running host (S-B).
- **R-2** Every declared element shall carry, or sit beside, a short
  human-readable statement of its meaning. An opaque reference alone, such as
  a catalog operation identity, is not enough.
- **R-3** The declared part shall live inside the package and travel with it.
  A derived index, registry or host database may reflect it but is not its
  authority.
- **R-4** Physical carriage is `UNRESOLVED` (U-01). Every option must satisfy
  R-1…R-3. OUT-002's open declared-part schema remains a required, deferred
  obligation (IR1-C §4), not a dropped one.

### 3.3 Declaration contract version

- **declaration contract version** identifies which version of this meaning
  the declared part is written against. Representation unselected.

### 3.4 Absent, partial and unrecognized declared parts

| Condition | Consumer meaning (all consumers) |
|---|---|
| No declared part (all current Root bundled workflows; any prose-only package) | The workflow is **undeclared**. It remains a readable, selectable method. Consumers report "requirements undeclared", never "no requirements". The required-tool check is **not established**, checkpoints cannot be product-held, and outputs/evidence carry no declared promise. |
| Declared part present, a category omitted | That category is **undeclared**. This differs from **declared empty** (an explicit statement that none are expected). Only "declared empty" supports "this workflow declares no checkpoints". |
| Unrecognized element or newer contract version | Preserve it unchanged and report it as unrecognized. An unrecognized element in the required-tool or checkpoint category makes the corresponding result **not established**, never a pass. |

---

## 4. Declared-part meaning

### 4.1 Expected inputs (SOW-042)

| Element | Meaning |
|---|---|
| **input name** | Local name, unique within the workflow. |
| **input meaning** | What the input is and why the method needs it. |
| **input kind** | One of: a host object or view obtained through a catalog read (see **required tool reference**); a file or document supplied to the run; a value or choice supplied by the person; an output of another identified workflow run. |
| **necessity** | Required, or optional with the effect of its absence stated. |
| **quality or basis requirement** | What must hold for the input to be usable. For a host read, the relied-on basis is DEL-03-01's read-basis descriptor (C §5.1): workspace identity, generation, model revision, canonical content identity, and the **identity method designation** of that content identity. Generation is a host lineage epoch; an intervening edit changes the model revision, not the generation. A read lacking any element is *basis incomplete* and cannot be cited as relied-on (C §5.2). Per-row **subject content identities** (C §5.3) come with the read. |
| **stage** | Where in the method the input is needed, anchored to the prose. |

An expected input is a need, not a fetched value. Whether and on what basis it
was supplied is an observation (§4.6).

### 4.2 Required tools (SOW-043, SOW-039)

#### 4.2.1 Two tool classes

| Class | What it refers to | Supplier of meaning |
|---|---|---|
| **host operation requirement** | An operation in a host's capability catalog, referenced by its operation identity. | DEL-03-01 catalog C (V4-HI-02; C §3). The reference is **opaque** here. |
| **harness capability requirement** | A capability of the agent's harness that is not a host catalog operation (e.g., file writing or native delegation in the App's Codex). | `UNRESOLVED` (U-08). |

A workflow designed for a host names host operations. An external agent (the
App's Codex through a host's MCP or CLI surface, V4-HI-50) reaches the same
catalog operations, and the declaration still references the catalog
identity, never an adapter-specific tool name.

#### 4.2.2 Elements of a required tool reference

| Element | Meaning |
|---|---|
| **tool reference** | Opaque reference to a DEL-03-01 operation identity (host class) or to a harness capability. |
| **version compatibility** | Optional. Only an exact version (or set of exact versions) can be stated, because C defines version equality only (C §3 #1, §3.2; U-07). |
| **purpose of use** | Readable: what the method uses the operation for. It does **not** restate the operation's class or treatment. Those come from the catalog entry's class element (five values incl. *no policy basis* with its reason, per R2-1), adopted policy (DEL-04-01) and the person's grant (V4-HI-40). |
| **necessity** | Required, or optional with a stated fallback or limitation. |
| **stage** | Where in the method the tool is used. |
| **governing checkpoint constraint** (derived, not authored) | If a checkpoint in the workflow requires A5 on this operation's result, every change request for this operation in the run is accompanied by the constraint {workflow run, checkpoint name, required act A5, operation} (R2-12; P §3.3), recorded with its **carriage assurance** (R4-14, final per R5-2): *host-held* (the host holds the constraint on its side, having derived it from, or verified it against, its own resolved copy of the declaration; the host loop's own evaluation is host-held), *App-assured* (App code attaches it — **not available in this increment**, since interposed App code is not adopted, R4-2), *model-supplied* (present only because the model put it in the call) or *absent*. A constraint the host merely received from an outside caller keeps its source's assurance. **Only host-held carriage satisfies R2-12.** The host route resolves treatment *propose*. The declaration does not state a treatment; the constraint is derived from its checkpoint so any carrier can compute it. Which assurance a host can give is relay question SQ-02 (U-19). |

#### 4.2.3 Requirement is not restriction

Root `execution.json` `tools.capabilities` and `tools.commands` are
**restrictions**: a ceiling that intersects outer policy ("empty restriction
lists deny rather than grant"; AGENT_WORKFLOW_RUNTIME.md). V4-WF-01 "the host
tools it needs" is a **requirement**: a floor the current host must meet.
These shall remain distinct. A consumer shall not read one as the other
(FB-05; EXAMPLES E6).

#### 4.2.4 Compatibility outcomes and pass rule (meaning only)

The check itself is DEL-02-03's (its REQ-001). This contract supplies the
vocabulary and the pass rule. Runtime non-success results *unavailable*,
*not permitted*, *channel not enabled*, *not exposed on this surface* and
*error* are C §4.1's, used unchanged.

| Outcome | Level | Meaning |
|---|---|---|
| **present** | per requirement | The operation exists in the current host's catalog edition and element 9 says *exposed* on the acting surface. |
| **missing** | per requirement | No entry in the current catalog edition. A discovery finding (C §4.1), reported with the requirement's purpose line (S-E). |
| **not exposed on this surface** | per requirement | Entry exists; element 9 says *not exposed on this surface* for the acting surface. |
| **channel not enabled** | per surface | The surface itself is off (external access not enabled; A13 not performed). Reported by the App when its own configuration is off, by the host when the host channel is off (R4-16). App-side configuration an agent could write is never A13 evidence (R4-13). Never encoded as missing or unavailable. |
| **version mismatch** | per requirement | Present, but not at a declared compatible version. |
| **present, currently unavailable** | per requirement, at run time | Present, but a precondition does not hold now; reported with the catalog's unavailable reason (V4-HI-04; C §4.2). A run-time hold, not a missing requirement. |
| **not established** | per requirement | Cannot be evaluated: undeclared, unrecognized element, catalog unreadable, reference unresolved, or element 9 value *unagreed*. Never reported as present. |
| **unsupported** | per workflow | With a stated reason: the workflow's compatible roles or delegation need cannot be met by the acting seat (§4.7, §5.3); or **"checkpoint hold not enforceable on this surface"**, naming the checkpoint, when its hold support on the acting surface is *not enforceable* (§4.3.8; R4-8). |

**Pass rule (IR1C-13).** The requirement check **passes** when every
reference whose necessity is *required* is **present** or **present,
currently unavailable**, the workflow is not **unsupported**, and no
checkpoint's hold support on the acting surface is *not established* (which
makes the check *not established*, never a pass; §4.3.8, R5-1). A *present,
currently unavailable* requirement is shown as a run-time hold with its
reason. Optional references never block a pass; their outcomes are shown. Any
required reference *missing*, *not exposed on this surface*, *version
mismatch*, *not established*, or on a surface whose channel is not enabled,
means the check does **not** pass. An undeclared workflow stays selectable and
is shown "requirements undeclared — check not established", never "runnable".

**Reporting rules (R2-4).** Reserved entries are always offered; a class
reason never makes an entry *not exposed*. At run time *not exposed on this
surface* is reported by the host from element 9; an operation absent from the
catalog edition the loop offered is the loop's *not offered* failure (never
dispatched). The discovery-time check above reads element 9 directly.

Whether a newly added operation becomes available on all three surfaces
without separate work is `UNRESOLVED{OI-003}`; the declaration never assumes
it (U-16).

### 4.3 Checkpoints requiring human acts (SOW-044; REQ-003)

#### 4.3.1 Elements

| Element | Meaning |
|---|---|
| **checkpoint name** | Stable within the workflow's revision; identifies the checkpoint across interruption, replay and adaptation (DEL-02-03 REQ-002). |
| **required act kind** | Exactly one of the closed list **A4 mark checked**, **A5 accept**, **A6 approve**, **A7 rely**, **A12 set grant** (R-1; DEL-04-01 §4.1). *Approve* is engineering approval only (V4-HI-30/33); design-candidate approval (V4-CON-05, V4-HI-65) is a separate later-increment act and cannot be required here. |
| **reached-when** | The observable arrival condition, of one of three kinds: (a) before dispatch of a named **required tool reference**; (b) on observed production of a named **declared output**; (c) on an observed host outcome of a named operation (e.g., *queued*). Meaning only; the loop evaluates it in hosts (DEL-05-01), DEL-02-03 in the App. |
| **subject class** | Its own element, independent of the reached-when kind (R2-17). Exactly one of: **change items of a named proposal**; **named output**; **objects a named output concerns** (R3-1); **objects changed by a named outcome**; **targets of the held call**; **grant setting**. Bound at run time (§4.3.6). Consumers bind the *declared* class and never infer it from the reached-when kind. |
| **position** | Where in the method the checkpoint sits, anchored to the prose. Explanation only; arrival is decided by **reached-when**. |
| **scope** | The extent of the subject covered, e.g., one item, several items or a whole proposal (V4-HI-41; acceptance unit = change item, R-6). Carried with every act request at the checkpoint and bound with the act (V4-REC-05; IR1C-14). |
| **purpose** | Why the act is requested here, in words the person reads when asked. Carried with every act request and bound with the act (V4-REC-05; IR1C-14). |
| **actor requirement** | "The person" by default; "the accountable professional" for A7 (V4-AUT-05). A class, never an identity. |
| **on negative decision** | What the method does after *resolved negatively* (A10 for A5; an act-declined event for A4, A6, A7, A12): stop, return to a named stage, or proceed on a stated branch. Absent this element, the run stops at the checkpoint. It never proceeds as if the act were positive. |
| **on mixed decision** (A5 only, optional) | What the method does when some items have A5 and some A10 (§4.3.7). Absent, the mixed case follows **on negative decision** for the rejected items; accepted items proceed through the host lifecycle. |
| **expected act evidence** | The act record expected (DEL-04-03 human-act record meaning), with its capturing surface and capture-evidence reference (I-5). A declaration, not a record. |
| **held actions** | What the run must not do until the act (INTEGRATION, R6-1; EXEC F-28). Either **"host operations only"**, naming them (e.g., the governed operation of an A5 constraint; the held call of a kind (a) checkpoint; named host operations after arrival until the act), or the **listed steps**, marking each App-side step (an App agent turn such as Return, an App tool or harness action, an App file write, an action on App content). **Derivation when absent (INTEGRATION, R7-3; EXEC §3.6):** for an **A5** checkpoint the held actions are the governed operation(s); for a **kind (a)** checkpoint they are the held call. **Conservative default:** consumers assume at least one App-side step (EXEC HS-5) only when a kind (b)/(c) checkpoint has no held-actions element, or when its declared held actions do not show host operations only (an A5 checkpoint takes the derivation above, per EXEC §3.6's definition). It decides hold support (§4.3.8). |

**Validity rules for combinations.**

| Combination | Rule |
|---|---|
| A5 | Reached-when **must** be kind (c) naming host outcome *queued* for the operation(s) whose result the checkpoint concerns, and subject class **must** be "change items of the named proposal" (that queued proposal). Any other A5 combination is invalid (FB-16) (R2-17). |
| targets of the held call | Valid only with reached-when kind (a) *before dispatch*; the held call is the one kind (a) held (INTEGRATION, R3-2; from IR1-C X-10). |
| objects changed by a named outcome | The named outcome must be an operation the workflow declares; bound when the applied outcome is observed (R2-14). |
| named output | The output must be declared in §4.4. |
| objects a named output concerns | The output must be declared in §4.4 and be a read or examination output that identifies objects (e.g., an OP-C3 findings output naming rows). Typically paired with reached-when kind (b) on that output (INTEGRATION, R3-1). |
| grant setting | For A12. The declaration **must always** name the setting content (classes, grant values, scope), and the **declared** content always binds. An A8 may present that content to the person but never changes the subject; an A12 made on different content satisfies nothing at this checkpoint. A run-dependent scope is declared as a **binding rule resolved at arrival** (e.g., scope = "targets of the held call"), never chosen by an A8. An A12 checkpoint that names no setting content is **invalid**, unconditionally (FB-17; INTEGRATION, R4-9 as amended by R5-3). |
| kind (a) on a harness capability | Declarable, but **not holdable in App runs** in this increment: hold support is *not enforceable* and the workflow is *unsupported* on that surface (FB-18; R4-21; R5-1). |

A review-only workflow can now require A4 on the rows it examined through
**objects a named output concerns** (R3-1; U-28 closed).

#### 4.3.2 What a checkpoint is and is not

- A checkpoint **names** a human act the run waits for. It does not perform,
  record or imply the act.
- Every act kind in the closed list is reserved to the person (S-Q; A12 via
  D2e). A checkpoint does not extend or narrow that list. Operation-specific
  additions for the first connected operation remain `UNRESOLVED{OI-021}`.
- A recognized act kind outside the closed list (A1 propose, A2 apply, A3
  examine, A8 request, A9 record, A10 reject, A11 withdraw, A13 enable
  external access, A14 answer tool permission) is **invalid** as a required
  act (FB-03). An unrecognized name is **not established** (FB-04) (R2-10).
  An agent's examination findings are not an A4 act (V4-EXM-21; R-4).
- A checkpoint is not a tool-permission prompt. An A14 answer, whether from the
  person or from the user's own Codex mode, never satisfies a checkpoint (S-R).
  A14 settlements are recorded only in the run record's tool-permission
  element (per R2-8), never as a human-act record.

#### 4.3.3 Independence rules

- **I-1 One kind, one evidence.** A checkpoint is satisfied only by evidence
  of its own act kind, by a qualifying actor, bound to its bound subject's
  current content. Evidence of another kind satisfies nothing here (S-H).
- **I-2 No success inference.** Operation success, a queued proposal, a
  receipt of application, host checks passed or an agent's examination
  supplies no human act (S-G; d3).
- **I-3 No synthetic ordering.** The contract imposes no rule that A5 must
  precede A4, A6 or A7. An independently evidenced act counts on its own
  evidence. A workflow may place checkpoints in a method order; that order is
  the workflow's visible declared method. The proposal lifecycle's
  accepted → applied sequence (V4-HI-23) is an operation lifecycle, not a
  checkpoint ordering rule.
- **I-4 Lapse and re-hold (R2-19; R4-3, EXEC §4.7, PROPOSED (W7)).** If
  bound content changes after the act, an **act-lapsed event** is always
  recorded and presented. The **resume point** is the first run action after
  the arrival became *performed* (or *resolved negatively* with a proceed or
  return path), recorded as a run-resumed event (EXEC HD-5). Then:
  - *before resume*: the arrival returns to **waiting** ("waiting — lapsed at
    ‹t›"); a new act on current content is needed;
  - *after resume, run live*: the **same arrival** re-holds: **waiting —
    re-held, lapsed at ‹t› after resume**. What "held" does follows the
    hold-support value (§4.3.8, R6-3): under *enforced by the host loop* the
    run stops at its next action boundary; otherwise the actions are recorded
    as *action during hold*; dispatches in flight complete and are observed; nothing done is
    undone. Outputs whose **gating checkpoint** is this one show their
    standing *lapsed* for the affected referents. The act is requested again
    for the **whole** bound scope, with the lapsed referents marked. A
    satisfying act makes the arrival *performed* again with the next
    performance ordinal. If the run ends while re-held, the final disposition
    is *waiting*;
  - *after the run has ended*: the standing disposition is **lapsed**.

  **A5 and A12 never re-hold.** Applying an accepted change item does not
  lapse its A5 (A5 binds to the change-item content identity); a basis failure
  between acceptance and application is the stale rule, not lapse (R-6). A
  later established A12 supersedes an earlier one; it does not lapse it (R2-7,
  R4-6). An undo *reverses ⟨receipt⟩* and lapses acts bound to content it
  changes, normally (R2-15). The interim "performed + act-lapsed" display is
  withdrawn (R4-3).
- **I-5 Capturing-surface evidence.** Satisfaction requires attributable act
  evidence from the **capturing surface**: the host's act facility for acts on
  host content (V4-HI-31), or the App interface for acts in the App. Faithful
  recording (A9) by any identified recorder distinct from the decision actor
  is a conformant record shape (settled; V4-AUT-03), and must cite the
  capturing surface's **capture-evidence reference** (act identity, actor, act
  kind, bound content identity, time). An agent-authored record, or a
  statement in conversation, never satisfies a checkpoint. No faithful record
  is made through an act-performing (reserved) operation (R2-2). Whether a host
  exposes a capture-evidence reference is a relay question (DEP-001; R2-20):
  without one, no host-content checkpoint can reach *performed*; it stays
  *waiting* (or *unknown* after interruption). In the App the capturing
  surface is a dedicated App act control (EXEC §5 CAP-1…CAP-9). Answers to
  Codex user-input or MCP elicitation requests are **not act evidence** and
  never host act capture, even when the person gives them (R4-12; EXEC CAP-6).
- **I-6 Negative decisions (R2-5).** For A5 the negative decision is A10
  reject, itself reserved wherever A5 is (S-S). For A4, A6, A7 and A12 a
  person's decision not to act is an **act-declined event**, with capture
  evidence; it is not an act of that kind and does not satisfy the
  checkpoint. Both give **resolved negatively**. Stopping the run is a
  separate **run-ended event**; it does not resolve a checkpoint.
- **I-7 An acceptance checkpoint forces a proposal.** If a checkpoint requires
  A5 on an operation's result, that operation's treatment in the run is
  *propose* regardless of the grant (DERIVED, R-5). The **governing checkpoint
  constraint** (§4.2.2) accompanies each change request for it, with its
  carriage assurance; only *host-held* carriage satisfies R2-12 (R5-2). A request
  to apply it directly is **not permitted**, naming the constraint as the
  governing treatment; it is never converted into a proposal (R-3.3; R2-12).
  A workflow that wants direct application under a grant followed by a human
  act declares a checkpoint on the applied result instead (A4 with subject
  class "objects changed by a named outcome").
- **I-8 Capture after arrival (R4-5; EXEC SP-6; PROPOSED (W7)).** An act
  counts toward an arrival only if it was captured **at or after** that
  arrival's event: by a request relation where the capturing surface records
  one, otherwise by evidenced times. An earlier act on the same subject is
  shown "prior act on this subject, not counted", so the person can repeat it
  knowingly; if the order cannot be established, the act does not count and
  the arrival shows "act order unknown". This orders an act only against its
  own arrival and adds no ordering between act kinds (I-3 stands). For A5 at
  kind (c) *queued* it always holds. Counting a prior act bound to current
  content is the owner alternative (U-31).
- **I-9 No unenforceable hold is claimed (R4-2; D6; R5-1; R6-3).** What
  "held" means depends on the checkpoint's hold support on the acting surface
  (§4.3.8): under *enforced by the host loop* the run stops at its next
  action; under *enforced on the host route* the host refuses the held host
  operations, and any other action is recorded as **action during hold**;
  under *not established* or *not enforceable* nothing is stopped and every
  run action taken while an arrival waits is recorded as **action during
  hold**, never hidden. Where hold support is *not enforceable* the workflow
  is *unsupported*; where it is *not established* the check is *not
  established*. If the person runs the workflow anyway, every arrival records
  its hold-support value.

#### 4.3.4 Disposition vocabulary (shared; R-5 as amended by R2-5, R2-19)

| Disposition | Meaning |
|---|---|
| **not reached** | The reached-when condition has not been observed. If the run ends without observing it, the final disposition is **not reached**, never performed. |
| **waiting** | Reached; the act is requested (with purpose and scope); the run holds where hold support allows (§4.3.8). Annotations include: "lapsed at ‹t›" (before resume); "re-held, lapsed at ‹t› after resume" (I-4); "prior act on this subject, not counted" and "act order unknown" (I-8); "A12 awaiting control confirmation" or "A12 refused by control: ‹reason›" (SB-4); "no items remain" (MX-6); "subject absent"; "hold not enforceable" / "action during hold" (I-9). If the run ends while waiting, a **run-ended event** is recorded and the final disposition stays **waiting** (R2-5). |
| **performed** | Capturing-surface evidence of the required act kind, by a qualifying actor, bound to the current content of every bound referent in scope (see §4.3.7 for reduced subjects). |
| **resolved negatively** | For A5: A10 evidence decides the bound items (fully, or with per-item annotation under §4.3.7). For A4/A6/A7/A12: an act-declined event. The **on negative decision** path governs. Never counted as performed. |
| **lapsed** | Standing disposition only for a checkpoint whose run has ended, when a performed act's bound content changed afterwards (per referent). |
| **unknown** | The observation that would decide arrival or the act was lost (e.g., interruption). Never presented as performed (S-K). |

**Run end and continuation (R4-4; EXEC §4.9; PROPOSED (W7)).** An ended run
is never resumed; its dispositions are final, except *performed* → *lapsed* on
a later lapse. An act performed after run end is recorded (DEL-04-03) and
shown against the bound subject marked **"after run end"**; it changes
nothing. To carry work on, the person starts a **new run** that may record
**continues ⟨run⟩**; it inherits no arrival, disposition or act, and its
arrivals bind only what the continuation itself observes (so I-8 shows earlier
acts as "prior act, not counted"). An interruption (lost observation, App or
loop restart) is **not** a run end: the same run is recovered (EXEC §4.12).
The hold state machine and replay are DEL-02-03's (EXEC §4).

#### 4.3.5 Reached-when evaluation rules (meaning only)

- **RW-1** Arrival is observed, never inferred from model text or prose
  stage.
- **RW-2** Kind (a) is evaluated before the named operation is dispatched;
  the call is held undispatched and, once *performed*, the **same** held call
  is dispatched unchanged (LOOP §2.4.1). Kind (b) needs the output's
  production to be observed. Kind (c) needs the named host outcome as
  reported under P §9 (e.g., *queued*, *applied (receipt)*).
- **RW-3** If a reached-when names a tool or output this workflow does not
  declare, the checkpoint is invalid (FB-13).
- **RW-4** A checkpoint may be reached more than once in a run (e.g., after a
  stale refusal and re-draft, the new proposal's *queued*). Each arrival binds
  its own referents; earlier dispositions remain history.

#### 4.3.6 Subject binding (R2-17, R-6, R2-14)

| Subject class | Bound at arrival to | Content identity the act must match |
|---|---|---|
| change items of a named proposal | The items of the proposal whose *queued* outcome was observed (by proposal and item identity) | **Change-item content identity** per item (DEL-03-02): operation identity and version, bound targets, old/new values, relied-on basis |
| named output | The produced output | The output's content identity (host-supplied, or file content identity for App files) |
| objects a named output concerns | The objects the produced read/examination output identifies (e.g., rows an OP-C3 finding names) | **Subject content identity** of each object **as read** by the read the output relies on (C §5.3/§5.4), with method designation; never the output's own content identity and never text in the output (INTEGRATION, R3-1) |
| objects changed by a named outcome | The created and changed object identities the **applied outcome** identifies (R2-14; P §9, C §3.3/§10 T12: e.g., S-5 created) | **Subject content identity** of each object **after application** (C §5.3), with method designation |
| targets of the held call | The targets the held kind (a) call names | Subject content identities of those targets **from the relied-on read the held call cites** (C §5.3/§5.4); never argument text |
| grant setting | The setting content the checkpoint's **declaration** names, with any run-dependent part resolved at arrival by its declared binding rule (R5-3); never an A8's choice | The **setting content**: classes, grant values, scope (R2-7) |

- **SB-1** Every content identity carries its identity method designation;
  identities with different designations are *unknown (incomparable)*, never
  "unchanged" (C §5.2 rule 6). Algorithms remain unselected.
- **SB-2** An act on other content, another proposal or another object set
  does not satisfy the checkpoint, even if its kind matches (VC-21).
- **SB-3** Binding by object identity is exact: an edit to one bound object
  lapses only that object's act; an unrelated edit elsewhere lapses nothing
  (C §5.3).
- **SB-4 A12 (R2-7; R4-6; EXEC §4.10, PROPOSED (W7)).** The control's
  response is a relation on the act, not its content:
  - **established ⟨settings version⟩** → the A12 counts (with I-1…I-8) and the
    arrival is **performed**;
  - **pending** (set by person, not yet confirmed) → **waiting**, "A12
    awaiting control confirmation";
  - **refused ⟨reason⟩** (e.g., no policy basis, R2-9) → **waiting**, "A12 by
    ‹person› refused by control: ‹reason›"; the refused A12 remains a
    recorded human act, establishes nothing and does **not** supersede the
    setting in force;
  - confirmation observation lost → **unknown** until observed.

  Only an **established** later A12 supersedes an earlier one; a checkpoint
  satisfied by the earlier A12 stays **performed** with "superseded by ‹act›"
  shown.

#### 4.3.7 Item-level decisions at an A5 checkpoint (PROPOSED; R2-18; confirmed by DEL-02-03, R4-7)

This is the rule LOOP C-7 and PANEL W-5f cite. The acceptance unit is the
change item (R-6). DEL-03-02 supplies per-item dispositions, the "all items
decided" indication and item-left events (P §4.3). DEL-02-03 **confirmed** all
rows and added MX-3, MX-6 and MX-8 (EXEC §4.11, PROPOSED (W7) confirmed).
Per-item states: A5 · A10 · undecided · left · **unknown** (decision
observation lost).

| Item state at evaluation | Checkpoint disposition | Per-item annotation shown |
|---|---|---|
| Every bound item has A5 on current item content | **performed** | each item "accepted by ‹person›" |
| At least one bound item has neither A5 nor A10 yet | **waiting** (even if others are unknown) | decided items show their act |
| **MX-3** No item undecided; at least one item's decision observation lost | **unknown** | which items are unknown; last observed state |
| Every remaining bound item has A5 or A10, and at least one has A10 | **resolved negatively**; **on mixed decision** governs if declared | "partial": which items A5, which A10. Accepted items keep their A5 and proceed through the host lifecycle unaffected |
| An item leaves without a decision (stale refusal, A11 withdrawal, host refusal) | Item leaves the bound subject; disposition is evaluated over the remaining items. **MX-6:** if none remain, the arrival is **waiting** "no items remain"; when a new arrival of the same checkpoint occurs (e.g., a re-draft queued), this arrival is closed "replaced by arrival n+1" with final *waiting*; otherwise it waits until run end | Each leaving item shown with its item-left event. A *performed* over a reduced subject is never shown as "all items accepted" |
| An item already decided (A5) is later refused at application (e.g., stale, R2-16) — adopted per R3-3; confirmed (MX-7) | Unchanged (the decision stands) | "accepted by ‹person› — not applied: refused — stale (relied ‹B›, current ‹B′›)"; A5 not lapsed; the declared output is not produced for that item (§4.6); a re-draft carries no acceptance |
| **MX-8** An item with A5 later meets **application error** (effect none / partial / unknown) or **outcome unknown** at application | Unchanged | "accepted — not applied: application error (effect …)" or "accepted — application outcome unknown (observer …)" |

MX-7/MX-8 never re-hold the A5 arrival and never trigger its negative or mixed
path; a checkpoint binding "objects changed by a named outcome" binds only the
objects of items actually applied; a re-draft reaching *queued* is a new
arrival with no acceptance carried over (EXEC MC-1…MC-4).

Retries de-duplicate by proposal identity before any basis check; a resubmitted
proposal returns its recorded state and is never refused stale by its own
effects. Applying sibling items does not stale remaining items unless they
share targets (R2-13).

#### 4.3.8 Hold support per checkpoint and surface (R5-1; R4-2, R4-8, R4-21; EXEC §3.6)

The declaration names checkpoints; whether a checkpoint can actually be
**held** depends on the surface running the workflow. The compatibility report
(DEL-02-03, owner of the values, EXEC §3.6) states exactly one hold-support
value per checkpoint and acting surface, and the run record carries it:

| Hold support | Meaning | Workflow requirement check |
|---|---|---|
| **enforced by the host loop** | Embedded route: the host loop holds the run (LOOP §2.4.4) | passes (holds subject to host evidence, DEP-001) |
| **enforced on the host route** | The host holds or refuses the operation through a *host-held* constraint (§4.2.2), evidenced by the host's answer to SQ-02 and a candidate | passes |
| **not established** | Depends on a host answer not yet given (SQ-02) or on unagreed exposure — e.g., in an App run through the external channel X, an A5 checkpoint whose constraint the host would have to hold, or a kind (a) checkpoint on a host operation the host would have to hold | *not established* — never a pass, never *unsupported* |
| **not enforceable** | No mechanism exists on this surface in this increment: in an App run, a checkpoint whose **held actions include an App-side step** (HS-5; App-side holds `UNRESOLVED{D6}`, neither interposed App code HP-1 nor `turn/interrupt` HP-2 adopted); a constraint carried only as *model-supplied*, once SQ-02 is answered with no host-held route (HS-3; before that answer, *not established*); kind (a) on a **harness capability** in an App run (R4-21) | *unsupported* — "checkpoint hold not enforceable on this surface: ‹name›" (R4-8) |

**Assignment by held actions (R6-1; EXEC §3.6).** The value is decided by the
checkpoint's **held actions** (§4.3.1), not by how it arrives. Rules are
evaluated in the order HS-1, HS-2, HS-5, HS-4, HS-3; the first match decides:

| # | Surface and checkpoint | Value |
|---|---|---|
| HS-1 | Invalid (FB-03, FB-13, FB-16, FB-17) or not established (FB-04) | **No value**; reported before the run, never evaluated; the check is *not established* via the declaration (EXEC F-22, confirmed by R6-1) |
| HS-2 | Host run on the embedded surface E | **enforced by the host loop** |
| HS-5 | App run; at least one held action is App-side, or (for a kind (b)/(c) checkpoint without derived held actions, §4.3.1, R7-3) the declaration does not show that every held action is a host operation | **not enforceable** (D6), whatever SQ-02 returns |
| HS-4 | App run on X; every held action is a host operation, one with unagreed exposure | **not established** |
| HS-3 | App run on X; every held action is a host operation on the external channel | By SQ-02 status: answered with host-held carriage or a host hold evidenced on a candidate → **enforced on the host route**; unanswered (today) → **not established**; answered with no host-held route → **not enforceable**. Never assumed |

**What "held" means per value (R6-3).**

| Value | At the hold |
|---|---|
| *enforced by the host loop* | The run stops at its next action |
| *enforced on the host route* | The host refuses the held host operations; any other action is recorded as *action during hold* |
| *not established* / *not enforceable* | Nothing is stopped; actions are recorded as *action during hold* |

**Workflow precedence (EXEC §3.5, INTEGRATION).** Where checkpoints differ,
any *not enforceable* makes the workflow *unsupported*; otherwise any *not
established* makes the check *not established*.

**Authoring advice (R6-1; CA WR-11).** A checkpoint that must be enforceable
from the App keeps **all its held actions on host operations** (e.g., an A5
constraint, or kind (a) on a host operation); it then becomes enforceable once
SQ-02 is evidenced. A checkpoint that holds any App-side step (e.g., Return)
stays *not enforceable* in App runs.

HP-3 (an App named-rule *decline* of a tool-permission request, never an
affirmative answer) remains a permitted best effort under D3; it does not make
a hold *enforced*. SQ-02's answer can move *not established* rows to
*enforced on the host route* for checkpoints on **host operations** only;
checkpoints holding any App-side step stay *not enforceable* whatever SWBPIPE
answers, pending the owner's D6 follow-up (R5-10; R6-1; U-30).

### 4.4 Returned outputs (SOW-045)

| Element | Meaning |
|---|---|
| **output name / meaning** | Local name and readable description. |
| **output form** | A change to host objects (always through the host's one route: proposal, or direct application under an effective direct treatment, V4-HI-20…23); a file or document; a report or message to the person; an input to another workflow. |
| **destination** | Host tables/views, the project, or the conversation. Host-changing outputs appear in the host's own views; there is no agent-private surface (V4-HOST-04). |
| **promised standing** | From the non-approval vocabulary, aligned with P §9 and R-4: *queued*; *applied (receipt)*; *agent-prepared*; *agent-examined (non-mutating)* (A3 findings, e.g., the result of an examination operation such as FX OP-C3); *host checks passed: ‹named checks›* (only where a host result names its checks, each with its evaluated basis). Never *approved*, *certified*, *sealed* or *code-compliant* (S-L). Unqualified "checked" is used only for A4. A human-act standing (e.g., *marked checked by the person*) can only be promised conditional on a named checkpoint. |
| **gating checkpoint** | Optional reference to the checkpoint whose act the promised standing depends on. |

### 4.5 Returned evidence (SOW-045)

| Element | Meaning |
|---|---|
| **evidence name / meaning** | What the evidence shows and for which output or checkpoint. |
| **evidence kind** | Host receipt reference; relied-on read-basis reference (five elements, V4-HI-11/21); evaluated basis of a non-success outcome; host result reference (with any named host checks); agent examination (A3) reference; human-act record reference (with capturing surface and capture-evidence reference); run record reference. |
| **by reference** | Host receipts, hashes and origin marks remain host-owned; declared evidence names a link, not a copy (S-P). |
| **supports** | Which output(s) or checkpoint(s) it supports. Evidence for one act supports no other (I-1). |

### 4.6 Promised versus observed (REQ-004; AC-004)

| Declared promise | Observed counterpart | Observation owner | Absent observation means |
|---|---|---|---|
| expected input | input actually supplied, with its basis | run record (DEL-04-03); read basis (DEL-03-01) | "not supplied" / "basis unknown" / "basis incomplete" |
| required tool reference | compatibility outcome and pass result (§4.2.4), then operations requested and their P §9 outcomes | DEL-02-03 check; run record | "not established" |
| checkpoint | disposition (§4.3.4), bound referents, act and event references (act-lapsed, act-declined, run-ended) | DEL-02-03 (App) / DEL-05-01 (host); DEL-04-03 | "not reached", "waiting" or "unknown", never "performed" |
| output with promised standing | produced output and actual standing per item (queued, accepted, refused — stale, applied (receipt), application error, outcome unknown …) | host; run record | "not produced", or "outcome unknown" attributed to the observer that lost observation (R-7) |
| evidence | linked receipt or record actually present | host; run record | "missing"; never a pass |

### 4.7 Compatible roles and restrictions (retained from Root)

| Element | Meaning |
|---|---|
| **compatible roles** | Which of the four roles the method is written for (Root `compatible_roles`, retained). Omission inherits compatibility; it never expands a role. |
| **tool restriction** | Optional ceiling narrowing the tools the method may use (Root `tools`, retained as a restriction, distinct from §4.2). |
| **enforcement statement** | None in the declaration. Metadata never proves enforcement. Where a harness or host cannot enforce a restriction, the consumer reports it as instruction-asserted (S-N). |

A workflow requiring delegation is compatible only with a role and seat that
can delegate. In a host seat without delegation, it is **unsupported**
(§4.2.4), never silently run without delegation.

---

## 5. The four roles and the single host seat (SOW-021, SOW-022; REQ-001; AC-001)

### 5.1 Common meaning (settled)

| Role | Meaning (V4-ROLE-01) |
|---|---|
| HELP_HUMAN | Alignment with the human |
| HELPS_HUMANS | Design |
| WORKING_ITEMS | Managed execution |
| TASK | Bounded execution; does not delegate (V4-ROLE-03) |

No fifth role: a domain expression such as the SWB Piping Designer
specializes context, tools and workflows within these roles (V4-ROLE-03).
Role guidance is supplied additively (V4-ROLE-02); supply is DEL-02-04's.

### 5.2 Expressions

| Aspect | Chirality App | Host application (e.g., SWBPIPE) |
|---|---|---|
| Role presence | Person selects a role (DEL-02-04). | Roles recede behind **one agent seat** and the selected workflow (S-M). The host need not present a role choice (REQ-001). |
| Guidance files | Product `AGENTS.md` plus role guidance. | The host's own `AGENTS.md` and `SKILL.md` (V4-HOST-06), open and readable (S-B). Distribution/adoption is `UNRESOLVED{OI-018}`. |
| Workflows | Project, user, bundled; host-origin when opened in App (V4-WF-06). | The host's own library (origin *host*); App workflows carried in unadapted keep their origin, adapted ones become host-origin (§6.4). |
| Tools | Codex native tools; host operations through an external surface (V4-HI-50). | The host's capability catalog (V4-HI-01). |
| Permission modes | Routine tool permission and sandbox are the user's own Codex setting (D3, SETTLED). | No classifier permission mode (D3, SETTLED). Host operation authority is grant plus policy, with the SWB default proposal mode (V4-HI-40/41; DERIVED, R2-11). |
| Delegation | Native delegation for roles permitted to delegate. | Host-defined; absent it, delegation-requiring workflows are **unsupported**. |

### 5.3 What the single seat must still carry

- **SEAT-1** The role meaning under which the seat operates for a run shall
  be determinable from the host's guidance and the selected workflow's
  **compatible roles**, and recorded with the run. Every dispatch carries it
  (R-7; DEL-05-01). If it cannot be determined, the record says **unknown**.
- **SEAT-2** The mapping from the host's single seat to the four role
  meanings is `UNRESOLVED` (U-09). Options: (a) the seat always runs as a
  TASK-equivalent bounded executor of the selected workflow; (b) the seat
  takes the role named by the workflow's compatible roles; (c) host guidance
  names one standing role per conversation. No option is chosen.
- **SEAT-3** Receding does not remove the distinctions: the seat's acts
  remain execution; the person's acts remain the person's (S-H, S-Q).

---

## 6. Source identity (REQ-001, REQ-004; AC-004)

### 6.1 The identity tuple (R-9)

Workflow identity is carried everywhere as {**kind**, **origin**, **source
root**, **name**, **revision**}, plus **derived-from** where applicable.

| Element | Meaning |
|---|---|
| **kind** | Workflow (distinct from skill; Root `kind`, retained). |
| **origin** | *project*, *user*, *bundled* or *host* (S-D). "App-origin" is not an origin class. |
| **source root** | Which library within the origin: the project root, the user's library, the App bundle and its release, or the host application and its library. Root `sourceRootId` meaning retained; values unselected. |
| **name** | Package name, matching its folder. |
| **revision** | Identity of the exact package content selected (all files in the package), with its identity method designation. Algorithm and multi-file canonicalization `UNRESOLVED` (U-03). A name plus origin without revision identifies a library slot, not selected content. |
| **derived-from** | For an adapted workflow: the full identity tuple of the workflow it was adapted from. Adaptation creates a new identity; it never edits the original's history. |

### 6.2 The identity chain: promised versus observed

| Link | Fact | Also recorded (R2-20) | Typical owner of evidence |
|---|---|---|---|
| **listed** | A library reports the workflow exists. | **holding library** | Discovery (DEL-02-02 App; host library) |
| **selected** | The person (or brief) chose a full identity tuple. | holding library | Selection (DEL-02-02; host panel DEL-05-02) |
| **resolved** | That identity resolved to specific revision content. | holding library | Resolver (placement open, §9) |
| **supplied** | Those bytes were supplied to the agent/loop, with per-thread/turn source identity and content identity (method-designated). | — | App: DEL-02-04 / DEL-01-01 (HOSTING §8.2); host: host loop (DEL-05-01 run association). Where the host cannot record it, **unknown** (relay question, R2-20; U-29) |
| **adopted by provider** | The model/harness took it up. Often unobservable; then **unknown**. Supplied ≠ adopted. | — | Stated as a limit |
| **observed behavior** | What the run actually did. | — | Run record (DEL-04-03); host evidence |

A matching name at two links establishes nothing about the others (AX-002).

### 6.3 Collision and rebinding rules

- **C-1** Every discovery that finds more than one origin for a name exposes
  all origins, each with its holding library (R2-20).
- **C-2** A selection holds its full identity tuple. Later discovery of a
  same-named workflow in any origin is reported as a collision and never
  rebinds the selection (S-D).
- **C-3** Only an explicit new selection by the person changes what is
  selected; that is a new selection event, not a rebinding.
- **C-4** Whether a selection follows a new revision of the same slot or
  stays pinned is a selection policy of DEL-02-02 (App) and the host; the
  chain shall make visible which occurred (U-10).
- **C-5** Where *host* sits in unqualified-name precedence is `UNRESOLVED`
  (U-10). Source-qualified selection makes precedence irrelevant to
  correctness.
- **C-6** The holding library never takes part in identity equality: two
  copies with the same tuple held in different libraries are the same
  workflow content, located twice (R2-20).

### 6.4 Carried and adapted workflows (V4-WF-06; R-9; R2-20; confirmed by DEL-02-03 EXEC §6.2, PROPOSED (W7))

| Case | Identity | Holding library |
|---|---|---|
| Carried **unadapted** into a host | Unchanged: original origin, source root, name, revision. | The host library holding the copy, recorded at listed/selected/resolved, shown by the panel beside the origin, carried in the loop's run association. |
| **Adapted** in a host | New identity: origin *host*, host source root, revised revision, **derived-from** = the original tuple. | The host library. |
| Host workflow opened and refined in the App | Opening keeps the host identity. A refinement is a draft (DEL-02-02) and, once registered, a new identity with derived-from = the host tuple. | App library where registered. |

- **HL-2** In a transfer, the *received* link records the destination holding
  library and the *exported* link the source one; a move between libraries
  without a content change creates no new identity (EXEC §6.2).
- **HL-3** The holding library is not recorded at *supplied*: supply is
  identified by tuple and content identity; supplied bytes that do not match
  the resolved revision are a revision defect ("revision not verified").
- The carriage procedure (EXEC §6.3 TR-1…TR-8, carriage manifest), adaptation
  receiving (§6.4 AD-1…AD-6, including derived-from checkpoints and "checkpoint
  meaning changed") and transfer failures (§6.7 TF-1…TF-8) are DEL-02-03's and
  consume this section unchanged.

Examples: EXAMPLES E3, E4.

---

## 7. Root conventions: keep, change or leave open

Root material is a reuse source, not v4 authority (PRD V4-CST-04; ARCH §5).

| Root convention (source) | v4 declaration | Why |
|---|---|---|
| Package = immediate folder containing `WORKFLOW.md`; name matches folder (SPEC §9.3; runtime "Workflow packages") | **Keep** | Satisfies V4-SHR-02; existing consumers read it. |
| Name rule 1–64 lowercase letters/digits in hyphen-separated segments (`catalog.schema.json`; `create-workflow`) | **Keep as reuse candidate**; confirm in OUT-004 fixtures | Source compatibility; no v4 reason to differ. |
| YAML front matter `name`, `description` (`WORKFLOW_TEMPLATE.md`) | **Keep**; declared-part carriage **open** (U-01) | Description supports selection; carriage is a representation choice. |
| Free prose body, no prescribed headings | **Keep** | V4-WF-01 retains prose. |
| Inputs, outputs, checks and human checkpoints stated only in prose | **Change**: add the declared part, keep the prose | V4-WF-01 requires an observable declared part. |
| `execution.json` `compatible_roles` | **Keep** (§4.7) | Four roles are common. |
| `execution.json` `tools.capabilities` | **Keep as restriction only**; not reused as required tools | Restriction ≠ requirement (§4.2.3). |
| `execution.json` `tools.commands` | **Leave out** of the portable declaration | Repository-specific; not portable. |
| "Metadata never proves host enforcement" | **Keep** | S-N. |
| Origins `project`/`user`/`bundled` and `sourceRootId` | **Change**: add *host*; add revision and derived-from; carried-unadapted keeps origin; holding library recorded beside identity | V4-WF-03/06; REQ-004; R-9; R2-20. |
| Unqualified precedence project → user → bundled | **Leave open** for *host* (U-10) | Not decided by the basis. |
| Source-qualified identity; no silent rebinding; all collision origins exposed | **Keep** | Same as V4-WF-03. |
| `selected-context` fingerprints | **Keep the idea** as revision; algorithm open (U-03) | Needed for promised-vs-observed. |
| Drafts in `.chirality/workflow-drafts/`, panel registration, no overwrite | **Not part of this contract**; DEL-02-02 | V4-WF-02 is DEL-02-02's. |
| `catalog.yaml` navigation, `centralWorkflowNames` | **Leave out** | Library navigation, not declaration meaning. |
| Derived `index.json` | **Keep principle**: derived, never authority | R-3 (§3.2). |
| Legacy `TaskSkill`, `legacy-methods.json` | **Leave out** | Root compatibility only. |
| Four-section role files `AGENT_<ROLE>.md` | **Leave to DEL-02-04 / OI-018** | Role-guidance structure and distribution are not this contract's. |
| Human checkpoints in Root prose (e.g., `create-workflow` review before registration) | **Change**: product-held only when declared with reached-when, subject class and act kind | Prose alone cannot be observed (RW-1). |

---

## 8. What each receiver receives from this contribution

| Receiver | Receives from WD-v0.5 | Expected check at next comparison |
|---|---|---|
| DEL-02-03 execution (EXEC-v0.2 at `8fb51f07f`; v0.3 in this pass) | §4.2 references, constraint and pass rule; §4.3 incl. subject class, validity rules, I-1…I-9, dispositions, §4.3.7, §4.3.8; §6.4 | Consumes WD-v0.5's adoption of EXEC §3.6, §4.7, §4.9, §4.10, §4.11, SP-6 unchanged |
| DEL-05-01 loop | §4.3.1 reached-when and **declared** subject class; §4.3.5; §4.3.6 binding table; §4.3.4 dispositions incl. lapse sequence and run-ended; I-5; I-7 constraint carriage; SEAT-1; §6.1–6.2 incl. holding library and supplied link | Binds declared class, not kind (IR1C-01); adds A12 to act-declined; adopts R2-19 lapse sequence; carries purpose and scope in "act requested" |
| DEL-05-02 panel | §4.2.4 outcomes and pass rule; §4.3.4 dispositions; §4.3.7 annotations and item-left display; §4.4 labels; §6.1–6.4 incl. holding library | Selection shows holding library; W-5f cites §4.3.7; purpose and scope shown |
| DEL-03-02 proposal | §4.2.2 governing checkpoint constraint; §4.3.6 use of applied-outcome object identities; §4.3.7 needs (item-left events, all-decided) | Constraint element in P §3.3; item-left events |
| DEL-04-01 policy | §4.3.1 closed list, invalid vs not established, subject classes (incl. held-call targets, grant setting) | §4.1 split; §4.2 referent list |
| DEL-02-02, DEL-02-04 (later undertaking per D1) | §3, §6, §4.6; §5 | Not exercised in this undertaking |
| DEL-02-01 self | Whole contribution | §13 cases |

Expected **from** suppliers:

| Supplier | Element | State at v0.5 (R6 in place) | Used in |
|---|---|---|---|
| DEL-04-01 | Canonical names; closed list; decision pairs; act-declined event; A12 binding, supersession and grant-setting referent; reserved-operation rule | ACT-POLICY-v0.5 at `d3cebd1cc` (header checked; R5-3 unconditional invalidity per V4-A) | §4.3 |
| DEL-02-03 | Report and hold support (§3.6); hold machine (§4): resume point, re-hold, run end, A12 control relation, MX rules, SP-6, recovery; App capture (§5); transfer (§6) | EXEC-v0.3 §3.5–§3.6 read (working tree, R6-1 revision) | §4.2.4, §4.3, §4.3.8, §6.4 |
| DEL-03-01 | Identity/version (equality); element 9 exposure; C §4.1 results; read basis (5 elements); subject content identity; FX-PIPE-01 incl. OP-C10…OP-C12, FXA-1…FXA-5, LIB-A1, LIB-A2, AF-1, editions e1/e2, named variants | C-v0.5 at `d3cebd1cc` (V-GR1 with GR-1…GR-3, GR-P, GR-R, GR-S, run 13) | §4.1, §4.2, §4.3.6, EXAMPLES |
| DEL-03-02 | P §9; change-item content identity; item dispositions, all-decided, item-left events; governing checkpoint constraint; applied-outcome object identities | P-v0.5 at `d3cebd1cc` (header checked; R5-2 per V4-A) | §4.2.2, §4.3.6, §4.3.7, §4.6 |
| DEL-04-03 | Human-act record with capturing surface, recording mode, capture-evidence reference; events (act-lapsed, act-declined, run-ended) | Not read; via IR1-A and R2 | §4.3, §4.6 |
| DEL-05-01 | Evaluation and binding; dispatch record with constraint, seat role; run association incl. holding library and supplied guidance | LOOP-v0.5 at `d3cebd1cc` (header checked; LH-n labels per R6-4) | §4.3.5, §6.2 |
| DEL-05-02 | Panel needs | Via IR1-C | §9 |
| DEL-01-01 | Supplied-guidance identity evidence (HOSTING §8.2); harness capability inventory at 0.158.0 | Via IR1-C J6 | §6.2, U-08 |
| SWBPIPE owner (external) | Host library; seat conduct; act facility and capture-evidence reference; constraint receipt or own declaration copy; per-turn guidance recording | None received; relay questions (W9) | §5, §6, I-5, I-7, U-05b, U-19, U-29 |

---

## 9. Shared contract/component responsibility map (OUT-003; REQ-005; AC-005)

Columns: consumers and need source; repeated responsibility; maintenance
rationale (d2: local implementations need conformance work; a library couples
releases; a service adds process, availability and upgrade coordination);
candidate (semantic, not a decision); confirmation (actual owner response);
placement. Reviews and comparisons are records, not owner confirmations, so
every Confirmation cell remains "None".

| # | Contract part (semantic owner) | Consumers and need source | Repeated responsibility | Maintenance rationale | Candidate | Confirmation | Placement |
|---|---|---|---|---|---|---|---|
| A-1 | Declared-part meaning (DEL-02-01) | DEL-02-03 (SoW; W7 pending); DEL-05-01 (LOOP-v0.2 §2.4 read at `28bd00499`); DEL-05-02 (PANEL-v0.2 §3.2, via IR1-C J2); DEL-02-02 (later); host loop/panel (external; none received) | Read the five categories, undeclared/empty states, reached-when and subject class | Divergent readers disagree on undeclared vs empty and on binding (IR1C-01 showed the risk) | Shared declared-part reading type(s) and parser/validator; conformance fixtures regardless | None | `UNRESOLVED{OI-014}` |
| A-2 | Workflow identity tuple, chain and holding library (DEL-02-01) | DEL-02-03; DEL-03-02 (P §3.3 origin); DEL-04-03; DEL-05-01 (run association); DEL-05-02 (PANEL §3.2, IR1C-09); DEL-02-02/02-04 (later); host library (external) | Carry the tuple and holding library; detect collisions; never rebind | Identity drift silently breaks V4-WF-03; a shared type is low-coupling | Shared workflow identity type; collision report meaning | None | `UNRESOLVED{OI-014}` |
| A-3 | Checkpoint declaration meaning (DEL-02-01) with act names (DEL-04-01) | DEL-02-03; DEL-05-01 (LOOP C-1…C-7); DEL-05-02 (PANEL W-5); DEL-04-03; host (external) | Name act kind, reached-when, subject class, validity; apply I-1…I-7; §4.3.7 | Independence rules erode locally; binding by kind vs class already diverged once | Shared checkpoint declaration type; shared negative fixtures | None | `UNRESOLVED{OI-014}` |
| A-4 | Checkpoint hold machine (DEL-02-03) | App run (DEL-02-03); host loop (DEL-05-01 receiving; external construction) | Wait/advance/lapse/unknown/re-hold/run end | Shared execution couples App and host loop lifecycles; d2 needs a concrete shared stateful responsibility first | Possibly shared; not proposed | None | `UNRESOLVED{OI-014}`; host side `UNRESOLVED{OI-013}` |
| A-5 | Compatibility outcome vocabulary and pass rule (DEL-02-01) over C identities and exposure (DEL-03-01) | DEL-02-03 (check); DEL-05-02 (PANEL §3.2, IR1C-13); DEL-02-02 (later); host (external) | Report §4.2.4 outcomes and pass truthfully | Vocabulary must match C exactly; checker code may stay local | Shared outcome vocabulary type; checker placement open | None | `UNRESOLVED{OI-014}` |
| A-6 | Role meaning and compatible roles (DEL-02-01; supply DEL-02-04) | DEL-02-04 (later); DEL-02-03; DEL-05-01 (seat role on dispatch); host seat (external) | Name four roles; read compatible roles; report unsupported | Tiny, stable meaning; cheap to share; enforcement stays per harness | Shared role identity set | None | `UNRESOLVED{OI-014}` |
| A-7 | Human-act and run record (DEL-04-03) | All above | Semantic owner is DEL-04-03 | Recorded here to keep the owner visible | Owned by DEL-04-03's allocation | n/a | DEL-04-03 / `UNRESOLVED{OI-014}` |
| A-8 | Catalog entry, exposure and read basis (DEL-03-01) | All above | Semantic owner is DEL-03-01 | As A-7 | Owned by DEL-03-01's allocation | n/a | DEL-03-01 / `UNRESOLVED{OI-014}` |
| A-9 | Host loop use of declarations (external construction; DEL-05-01 receiving) | Host loop (LOOP §2.4, §6.2, §10.1) | Parse the declared part in the host; evaluate reached-when; bind subject class; carry the governing checkpoint constraint and holding library; persist runs | Loop placement, parsing and persistence are host choices | None proposed | None | `UNRESOLVED{OI-013}` |
| A-10 | Panel workflow selection and checks (external construction; DEL-05-02 receiving) | Host panel; possibly App views (via IR1-C J2/J3) | Present selection, identity, holding library, collisions, pass result, checkpoint requests with purpose/scope and "accept" wording, shared dispositions and item annotations | Reusable components only on agreed repeated purpose (DEL-05-02 OUT-004) | Possibly shared presentational components; not proposed | None | `UNRESOLVED{OI-014}`, `UNRESOLVED{OI-013}` |
| A-11 | Catalog-schema argument checking (DEL-03-01; LOOP §10.2 candidate (b)) | DEL-05-01; host (external); external adapter (DEL-03-03) | Check call arguments against the catalog schema before host domain validation | Pointer row only: held by DEL-03-01 (C §8 map) | Held by DEL-03-01 | None | `UNRESOLVED{OI-014}` |
| A-12 | Governing checkpoint constraint element (DEL-03-02 change request; derived from DEL-02-01 declaration) | DEL-05-01 (dispatch), DEL-03-03 (adapter), host route (external) | Derive, carry and evaluate the A5 constraint consistently on every channel | An omitted constraint is indistinguishable from none (R2-12); consistency matters more than code sharing | Shared derivation rule from the declaration; carriage stays per channel | None | `UNRESOLVED{OI-014}` |

Allocation result at v0.5: every row names its consumers and open placement.
**No** common implementation or service is proposed, and no row is
represented as agreed (AC-005).

---

## 10. Excluded acts and their owners (REQ-006; AC-006)

| Act excluded from DEL-02-01 | Owner | Receiving interface in this contract |
|---|---|---|
| Catalog-semantic definition (identity, version, exposure, availability, standing, read basis, content identities, fixture catalogue) | DEL-03-01 | §4.1, §4.2, §4.3.6; EXAMPLES |
| Proposal/outcome definition (P §9, change items, change request incl. governing checkpoint constraint, item-left events, applied-outcome objects) | DEL-03-02 | §4.2.2, §4.3.6, §4.3.7, §4.4, §4.6 |
| Operation-policy definition; canonical act names; carrying adopted D2/D3 | DEL-04-01 | §4.3.1 closed list; §2 S-Q/S-R/S-S |
| Operation-specific reserved additions | Owner via outside SWB session (`UNRESOLVED{OI-021}`) | §4.3.2 |
| Human-act and run-record field definition; record implementation | DEL-04-03 | §4.3.1 expected act evidence; §4.5; §4.6; §5.3 |
| Checkpoint hold machine, re-hold, ended-run resumption, required-tool check, transfer | DEL-02-03 | §4.2.4, §4.3.4, §4.3.7, §6.4 |
| Loop receiving design (arrival observation, binding step, constraint carriage) | DEL-05-01 | §4.3.5, §4.3.6, §9 A-9, A-12 |
| Panel receiving design | DEL-05-02 | §9 A-10 |
| App workflow workspace and registration | DEL-02-02 (later undertaking, D1) | §6.3 C-4/C-5; §7 |
| Role selection and supply | DEL-02-04 (later undertaking, D1) | §5 |
| Host catalog, domain validation/application, receipts, loop, panel, tables, views, act facility and capture-evidence reference | External SWBPIPE implementation owner | §4.5; I-5; §5.2 |
| Performing marking checked, acceptance, rejection, approval, reliance, grant change, external-access change | The person; professional assertions by the accountable professional | §4.3 (declaration names, never performs) |
| Shared placement decisions | App/shared contract owners (OI-014); with SWB implementation owner (OI-013) | §9 |

---

## 11. Failure behavior (consumer-facing meaning)

| ID | Condition | Required behavior |
|---|---|---|
| FB-01 | Declared part absent or a category omitted | Report **undeclared**; never "none". |
| FB-02 | Declared part unreadable or malformed | Workflow stays a prose method; declared part **not established**; report the defect; no partial interpretation that could pass a check. |
| FB-03 | Checkpoint names a recognized act kind outside {A4, A5, A6, A7, A12}, or none | **Invalid** checkpoint; report; no execution outcome can satisfy it (R2-10). |
| FB-04 | Checkpoint names an act kind the consumer does not recognize | Preserve; **not established**; never substitute a nearby kind (R2-10). |
| FB-05 | Root `tools` restriction present, required tools undeclared | Required-tool check **not established**; restriction honored as ceiling. |
| FB-06 | Tool reference does not resolve against the current catalog | **missing** (or **not established** if the catalog is unreadable); never dropped. |
| FB-07 | Prose and declared part disagree (e.g., prose describes a human checkpoint the declared part lacks) | Report; do not auto-add or auto-remove a checkpoint. |
| FB-08 | Selected revision no longer resolvable | Report; do not substitute current same-named content; the record keeps the selected tuple. |
| FB-09 | Collision discovered after selection | Report all origins with holding libraries; keep selection (C-2). |
| FB-10 | Output promises approval, certified or unqualified "checked" standing, or labels an A3 examination "host checks passed" | Invalid element (S-L; R-4); report. |
| FB-11 | Declared evidence has no observed counterpart after the run | **missing**; never a pass. |
| FB-12 | Seat role meaning undeterminable | Record **unknown** (SEAT-1). |
| FB-13 | Reached-when names an undeclared tool or output, or is absent | Invalid checkpoint; the consumer cannot hold on it truthfully and reports it; the run does not proceed past the prose position as if the checkpoint were satisfied. |
| FB-14 | Direct application requested for an operation under a governing checkpoint constraint | **not permitted**, naming the constraint (I-7); no silent conversion to a proposal. |
| FB-15 | Only an agent-authored record, a conversation statement, or a record without a capture-evidence reference exists | Checkpoint stays **waiting** (I-5). |
| FB-16 | A5 checkpoint whose reached-when is not kind (c) *queued*, or whose subject class is not "change items of the named proposal"; or "targets of the held call" with a kind other than (a) | Invalid checkpoint (R2-17; IR1-C X-10); report. |
| FB-17 | A12 checkpoint whose declaration names no setting content | Invalid checkpoint, unconditionally, whatever an A8 at arrival presents (R4-9; R5-3). |
| FB-18 | Kind (a) on a harness capability in an App run (pending D6), or any checkpoint whose hold support on the acting surface is *not enforceable* | Workflow **unsupported** on that surface: "checkpoint hold not enforceable on this surface" (R4-8, R4-21). |

---

## 12. UNRESOLVED

| ID | Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|---|
| U-01 | Physical carriage of the declared part (front matter, delimited body section, or package companion file) | DEL-02-01, with consumer confirmation | Before OUT-002 schema and OUT-004 parser fixtures | Examples use an illustrative rendering. Options: (a) front matter (one file; long YAML); (b) delimited body section (readable; needs a stable delimiter); (c) companion file (mirrors `execution.json`; two files to keep consistent). Recommendation deferred until DEL-02-03 (W7) and DEL-05-01 parsing needs are received. |
| U-02 | Wire field names, value encodings, schema language | DEL-02-01 with consumers | Before OUT-002 schema | All names are semantic. |
| U-03 | Revision algorithm and multi-file canonicalization | DEL-02-01 with DEL-04-03 | Before revision comparison claims | Meaning defined, with identity method designation; comparison untestable. |
| U-05 | Operation-specific reserved additions: `UNRESOLVED{OI-021}` | Owner via outside SWB session with App/shared owner | Before connected-activity SoW | D2 list applies; additions not assumed. |
| U-05b | Host capture-evidence reference per act kind (relay question, R2-20) | Host owner (DEP-001), via W9 relay | Before host act-recording integration | Without it no host-content checkpoint can be *performed* (I-5). |
| U-05c | Multi-row A4 purpose after partial lapse | DEL-04-01 with Owner (DEL-04-01 U-03); carried to closeout C1 (R4) | At its point of need | The whole-scope re-request (I-4) satisfies every option; only an act on the lapsed referents alone is HELD (EXEC CH-8 (ii)). |
| U-07 | Operation version ordering or range | DEL-03-01 (C §3.2, U-C9) | Before DEL-02-03 required-tool fixtures | Exact-version equality only. |
| U-08 | Portable naming of harness capability requirements | DEL-02-01 with DEL-01-01 (0.158.0 inventory, HOSTING §8) and DEL-02-03 | Before App-side required-tool check | Class defined; names open; register row RF-7 at C1. |
| U-09 | Host single seat → role meaning mapping (options in SEAT-2) | DEL-02-01 with SWB implementation owner and DEL-02-04 | Before host role-guidance supply and host receiving fixtures | SEAT-1…3 hold for any option. |
| U-10 | Host origin in unqualified precedence; whether a selection follows new revisions | DEL-02-02 (later undertaking) with DEL-02-01 and host owner | Before host-origin discovery in App | Correctness rests on source-qualified selection. |
| U-11 | Record fields for identity tuple, holding library, seat role, checkpoint disposition and events, bound referents, capturing surface | DEL-04-03 | Next comparison | Referenced by meaning. |
| U-12 | Placement of shared parts: `UNRESOLVED{OI-014}` | App/shared contract owners | Before structural/production contract allocation | Map rows exist; no placement proposed. |
| U-13 | Host loop placement/parsing/persistence and panel assembly: `UNRESOLVED{OI-013}` | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Rows A-4, A-9, A-10. |
| U-14 | Guidance distribution/adoption: `UNRESOLVED{OI-018}` | Owner with shared/project instruction owners | Before instruction changes or dependent supply | Readability required; distribution not decided. |
| U-15 | First connected operation, autonomy and environment: `UNRESOLVED{OI-021}` | Owner via outside SWB session and App/shared owner | Before connected-activity SoW | Fixture operations are FX-PIPE-01 entries, not the selected operation. |
| U-16 | Automatic catalog extension: `UNRESOLVED{OI-003}` | Owner with host contract owner | Before claiming extension capability | Never assumed. |
| U-17 | Owner confirmations for §9 rows; SWBPIPE consumer needs | DEL-02-03, DEL-05-01, DEL-05-02, DEL-03-02 (this undertaking); DEL-02-02, DEL-02-04 (later); SWBPIPE owner via relay | Next comparison (internal); relay (external) | Every row "None". |
| U-19 | Relay question SQ-02 (R2-12, R4-14, R5-2): can the host hold the constraint (*host-held*: derived from, or verified against, its own resolved copy of the declaration), and hold host-operation checkpoints for App runs? Which evidence shows which? | Host owner (DEP-001) via W9; DEL-03-02 defines the element | Before W7 host-side fixtures and LOOP FX-C9 / PANEL PC-24 / VC-11 | I-7 holds as meaning; VC-11 **AWAITING INPUT**; host-operation checkpoints in App runs are *not established* until answered (§4.3.8). |
| U-23 | Real per-surface exposure agreement (the fixture uses C FXA-1, "exposed ×3", with variant V-X1) | DEL-03-01 (C §8 map) with host owner; `UNRESOLVED{OI-003}` | Before exposure claims | Fixture values supplied by C; real exposure open; unagreed exposure makes hold support *not established* (R5-1). |
| U-25 | Construction of the App act control and App person identity (requirements in EXEC §5 CAP-1…CAP-9) | DEL-01-04 (later undertaking, D1) with DEL-04-03 | Before App capture fixtures | Requirements supplied; App-side positive capture cases AWAITING INPUT. |
| U-30 | App-side run holds `UNRESOLVED{D6}`. SQ-02 decides only checkpoints whose held actions are all **host operations** (HS-3); checkpoints holding any **App-side** step (HS-5) stay *not enforceable* whatever SWBPIPE answers — a separate D6 follow-up for the owner (R5-10) | Owner; DEL-02-03 with DEL-03-03 for any App hold point | Before any App-run checkpoint case is claimed held | App runs: HS-3 checkpoints *not established*, HS-5 checkpoints *not enforceable*; action during hold recorded (§4.3.8, I-9). |
| U-31 | Capture-after-arrival (I-8) versus counting a prior act bound to current content (EXEC U-E4) | Owner, with DEL-02-01 and DEL-04-01 | Before hold-machine fixtures run | I-8 applied as PROPOSED (R4-5). Owner-visible cost (R5-7): SP-6 can make the person repeat a grant change whose content is already in force (EXAMPLES R-16 (i)). |
| U-32 | Whether a declaration carries an "on subject absent" path (EXEC U-E7) | DEL-02-01 | Before a subject-absent fixture runs | Default: *waiting* "subject absent"; an act-declined event resolves it or the run ends. |
| U-29 | Per-turn supplied-guidance source and content identity in host loops (relay question, R2-20) | Host owner (DEP-001) via W9; DEL-05-01 element | Before host supplied-link evidence | Where absent, *supplied* is **unknown**, never inferred from configuration. |

Closed since v0.3: U-18 (transfer procedure: EXEC §6.3–§6.7), U-20 (item rule confirmed, R4-7), U-21 (no resumption; continuation, R4-4), U-22 (re-hold, R4-3), U-24 (holding library confirmed, EXEC §6.2), U-27 (refused A12, R4-6) — each PROPOSED (W7) where EXEC marks it so.
Closed since v0.2: U-26 (fixture identifiers; now C §10 plus R2-21); U-28 (subject class for examined objects; R3-1).
Earlier closed: U-04 (names, R-1), U-06 (classifier permissions, D3).

---

## 13. Verification cases (designed, not run)

None has been executed; no parser, consumer or host exists. Inputs are the
fixture examples in EXAMPLES (FX-PIPE-01 material, invented). Labels:
DESIGNED, or **AWAITING INPUT** where a named external input is required
before the case can be run.

| Case | Serves | Input | Expected result |
|---|---|---|---|
| VC-01 Four roles and host seat | VER-001 (AC-001) | E1 read in App and host single-seat contexts | Same four role meanings; host needs no role-selection UI; seat role recorded or **unknown**. |
| VC-02 Host-owned library | VER-001 (AC-001) | E3 adapted host workflow plus host `SKILL.md`/`AGENTS.md` | Origin *host* and its source root; all files readable as text. |
| VC-03 Five categories recovered | VER-002 (AC-002) | E1 | Every input (incl. five-element basis requirement), tool reference, checkpoint (reached-when, subject class, scope, purpose), output and evidence item recovered; prose intact. |
| VC-04 Undeclared vs empty | VER-002 (AC-002) | E5; variant declaring "no checkpoints" | E5 → all **undeclared**; variant → checkpoints **declared empty**. |
| VC-05 Tool references stay opaque | VER-002 (AC-002) | E1 references vs C §3/§10 | Each compared with C OP-C1/C3/C4/C5; no wire field invented. |
| VC-06 Restriction not requirement | VER-002 (AC-002) | E6 | Required-tool check **not established**; restriction retained. |
| VC-07 Success is not an act | VER-003 (AC-003) | E2 R-1 | `CP-accept` **waiting**; items *queued*; a consumer reporting "accepted" is incompatible. |
| VC-08 Independent A4 without acceptance | VER-003 (AC-003) | E1b | `CP-review` **performed** on its own capturing-surface evidence for the examined rows; no prior A5 required (I-3). |
| VC-09 Distinct acts | VER-003 (AC-003) | E2 R-3 | `CP-accept` **performed**; `CP-check` **waiting** after arrival (I-1). |
| VC-10 Lapse sequence | VER-003 (AC-003) | E2 R-4 (i)–(iii); T14 control | (i) before resume: act-lapsed event; `CP-check` **waiting — lapsed at ‹t›**. (ii) after resume, run live: **waiting — re-held, lapsed at ‹t› after resume**; next action stopped; nothing undone; `checked-rows` standing *lapsed*; whole scope re-requested. (iii) after run end: **lapsed** for the edited object only. T14 edit to S-2 lapses nothing bound here (SB-3). A5 not lapsed by application and never re-held. |
| VC-11 Acceptance checkpoint forces proposal | VER-003 (AC-003) | E2 R-5a/R-5b (C V-CP1), R-5c (C T15–T16) | **AWAITING INPUT** (R2-12; U-19) for host-side evaluation. Designed: R-5b direct request → **not permitted** naming the constraint and its carriage assurance; nothing applied; no conversion. R-5a the agent separately submits a proposal; `CP-accept` waits. A model-supplied constraint alone does not satisfy R2-12. R-5c (E1c) direct application under ⟨set-2⟩ proceeds with origin/undo; `CP-check` waits for A4 on S-4. |
| VC-12 Closed act list | VER-003 | Variants of E1 naming A2 apply, A3 examine, A14, V4-CON-05 approval, and an unknown name | Recognized kinds → **invalid** (FB-03); unknown name → **not established** (FB-04). |
| VC-13 Collision without rebinding | VER-004 (AC-004) | E4 | All origins exposed with holding libraries; selection keeps its tuple; only explicit reselection changes it. |
| VC-14 Adapted revision | VER-004 (AC-004) | E3 adapted row | New identity with derived-from = original tuple; original unchanged. |
| VC-15 Promised vs observed | VER-004 (AC-004) | E2 R-6 | **outcome unknown** attributed to the observer; `EV-receipt` **missing**; `CP-accept` **unknown** (deciding observation lost), never performed. |
| VC-16 Reserved operations | VER-003, VER-004 | E2 R-10 | Agent call to OP-C6 → **not permitted** (reserved, DERIVED R2-2); an A8 request is *offered*, not recorded automatically (R2-4); `CP-check` stays **waiting**. |
| VC-17 Map rows name consumers | VER-005 (AC-005) | §9 | Every row has consumers, responsibility, rationale, confirmation "None" and placement; no row marked agreed. |
| VC-18 Excluded acts mapped | VER-006 (AC-006) | §10 vs SoW REQ-006 | Every excluded act with owner and interface; host-vs-person distinction present. |
| VC-19 Fixture inventory bound to candidate | VER-007 (AC-007) | WD-v0.5, WD-EX-v0.5 | Inventory VC-01…VC-43 with candidate identity (WD-v0.5, WD-EX-v0.5); all DESIGNED or AWAITING INPUT; missing inputs listed; no joined host witness claimed. |
| VC-20 Reached-when not observed | VER-003 | E2 R-7′ | `CP-accept` **not reached**; never performed. |
| VC-21 Subject binding | VER-003 | E2 R-8 | A5 on another proposal's item → `CP-accept` stays **waiting** (SB-2). |
| VC-22 Capturing surface | VER-003 | E2 R-9 (i)–(iii) | (i) agent-authored record → **waiting**. (ii) faithful App record citing the host capture-evidence reference → **performed**; recorder ≠ decision actor. (iii) host exposes no capture-evidence reference → **waiting** (I-5; U-05b). |
| VC-23 Negative decisions | VER-003 | E2 R-11, R-12 | R-11: A10 on all items → **resolved negatively**; on-negative path. R-12: act-declined event (A4) → **resolved negatively**; never performed. |
| VC-24 Mixed items | VER-003 | E2 R-2 (T11) | **resolved negatively** with per-item annotation "partial: item 1 A5, item 2 A10"; item 1 proceeds to RC-1 (§4.3.7). |
| VC-25 Exposure outcomes | VER-002 | E7 | *missing*, *not exposed on this surface*, *channel not enabled*, *not established* and *present, currently unavailable* reported distinctly; pass rule applied. |
| VC-26 Carried unadapted keeps origin | VER-004 | E3 unadapted row | Tuple unchanged; holding library recorded at listed/selected/resolved; no "App-origin" value. |
| VC-27 Stale after acceptance | VER-003 | E2 R-14 | Item shown "accepted by Engineer A — not applied: refused — stale (both bases)"; A5 not lapsed; checkpoint disposition unchanged; output not produced for that item. |
| VC-28 Tool permission is not an act | VER-003 | E2 R-15 | A14 settles tool execution only; no checkpoint disposition changes (S-R). |
| VC-29 Invalid A5 combinations | VER-003 | Variants of E1 `CP-accept`: kind (a); kind (b); subject class "objects changed by a named outcome"; held-call targets with kind (c) | Each **invalid** (FB-16). |
| VC-30 Declared class, not kind | VER-003 | E1 `CP-check` (kind (b), class "objects changed by a named outcome") | Binding uses the applied objects' post-application subject content identities, not the examination output's content (IR1C-01). |
| VC-31 Run end and continuation | VER-003 | E2 R-12b | Run-ended event; `CP-check` final **waiting**; a later A4 is shown "after run end" and changes nothing; a continuation run (*continues ⟨run⟩*) inherits nothing and shows that A4 as "prior act, not counted" at its own arrival (R4-4, I-8). |
| VC-32 A12 rules | VER-003 | E2 R-16 (i) main order; (ii)–(v) C V-GR1 (E1d) | T15's A12 precedes arrival → "prior act, not counted", **waiting**; A12 after arrival established → **performed**; later established A12 supersedes (stays performed, shown); refused A12 → **waiting**, does not supersede; pending → **waiting**; lost confirmation → **unknown** (R4-5, R4-6). |
| VC-33 Pass rule | VER-002 | E7 variants; E8 | Pass only when every required reference is present or present-currently-unavailable, the workflow is not unsupported and no hold support is *not established*; undeclared stays selectable, never "runnable". |
| VC-34 Retry de-duplication | VER-004 | E2 R-13 (T13) | Resubmission of PR-2 returns its recorded state (RC-1) and is never refused stale by its own effect; if unobservable, **outcome unknown** by the observer. |
| VC-36 Objects a named output concerns | VER-003 | E1b; E2 R-E1b′ | `CP-review` binds S-2 and S-3 (the rows the OP-C3 findings name) through their subject content identities as read at B1; an A4 on the findings output itself, or on S-1, does not satisfy it; T6's S-3 edit lapses only S-3 (R3-1). |
| VC-37 Hold support per surface | VER-001, VER-003 | EXAMPLES E8 | Embedded host run (HS-2): every checkpoint **enforced by the host loop** → passes (subject to host evidence). App run via X: E1 `CP-accept` (held: OP-C4/OP-C5) HS-3 **not established**, `CP-check` (held: Return) HS-5 **not enforceable** → **unsupported**; E1c `CP-check` HS-5 → **unsupported**; E1d `CP-grant` (held: OP-C9 call) HS-3 **not established** plus E1c's `CP-check` HS-5 → **unsupported** whatever SQ-02 returns. If run anyway, arrivals record their value and actions while waiting are "action during hold"; no App hold claimed (R5-1, R6-1, R6-3). |
| VC-43 Held actions decide the value | VER-003 | E8 variant L-WDEX-17 | A checkpoint declared with "held actions: host operations only (OP-C9)" in an App run on X → HS-3 (**not established** today; **enforced on the host route** after an evidenced SQ-02 answer); the same checkpoint with an App-side step → HS-5 **not enforceable** (R6-1; EXEC F-28); the same checkpoint with **no held-actions element** → held actions derived as the held OP-C9 call (kind (a); §4.3.1, R7-3) → HS-3 **not established** today, and its workflow result follows EXEC §3.5 precedence with the run's other checkpoints (L-WDEX-17 has none: **not established** today). |
| VC-38 Harness-capability kind (a) | VER-003 | E8 variant | Kind (a) on a harness capability in an App run → *not enforceable*, **unsupported** (FB-18; R4-21). |
| VC-39 Capture after arrival | VER-003 | E2 R-9b | A5/A4 captured before its arrival → "prior act on this subject, not counted"; order not establishable → "act order unknown"; neither counts (I-8). |
| VC-40 Mixed-item additions | VER-003 | E2 R-6b, R-7b, R-13b | MX-3 lost decision → **unknown**; MX-6 all items left (A11 withdrawal) → arrival closed "replaced by arrival n+1" at the next *queued*; MX-8 application outcome unknown after A5 (V-OU1) → disposition unchanged, annotated (R4-7). |
| VC-41 A12 without setting content | VER-003 | E1d variant | A12 checkpoint naming no setting content → **invalid**, unconditionally, even with an A8 presenting a setting (FB-17; R4-9; R5-3). |
| VC-42 Elicitation is not act evidence | VER-003 | E2 R-9 (iv) | An answer to a Codex user-input/MCP elicitation request ("yes, accept") → `CP-accept` stays **waiting** (R4-12). |
| VC-35 Undo lapses normally | VER-003 | E2 R-17 (T16a, T17) | RC-3 *reverses RC-2*; T16a's A4 bound to ⟨S-4@r16⟩ lapses (FXA-2 covers the label) per I-4. |

Limit: passing these later would show local contract/fixture conformance
only. It would not establish host implementation, round-trip execution,
adoption or any human act (SoW VER-007).
