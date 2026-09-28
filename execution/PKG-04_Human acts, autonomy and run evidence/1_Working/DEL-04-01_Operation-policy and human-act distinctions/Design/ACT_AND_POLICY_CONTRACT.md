# Operation-Policy and Human-Act Contract
- Contribution: DEL-04-01/ACT-POLICY-v0.5. It supersedes ACT-POLICY-v0.4 (sha256 d6da05abe790a4374df7faf225439a01dc1be734491b499d90cf00533369b03b at `8fb51f07f`). Earlier versions: v0.3 (b3748c02…8128), v0.2 (e50f1fe2…9a9), v0.1 (e6457535…3763).
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001, OUT-002, OUT-003; REQ-001…REQ-007; VER-001…VER-009 (AC-001…AC-009)
- Basis:
  - Repo 6e18505e3; ScopeOfWork.md sha256 fc1a0503abad4196e869402b664bd76280773d197b5c77994c34e858a406f5e6.
  - `P/docs/PRD.md` §4.1 (V4-WF-02, -05), §4.3 (V4-EXE-01, -02), §4.5 (V4-AUT-01…05), §4.7 (V4-REC-05), §9 (OQ-02, OQ-11), §10.
  - `P/docs/HOST_INTEGRATION.md` §2 (V4-HI-02, -04), §3 (V4-HI-11, -12), §4 (V4-HI-20…25), §5 (V4-HI-30…33), §6 (V4-HI-40…42), §7 (V4-HI-50…52), §9 (V4-HI-70/71).
  - `P/docs/EXAMINATION.md` V4-EXM-20, -21, -22, -25, -31.
  - `P/execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/DECISION_BRIEF.html#d3` (sha256 02d38cb18041c52989d8a2a0b969e6502ce4b25eec85fb0931bbbc100c4420e8).
  - `P/conceptual/DECISIONS.md` OD-05, D-04; `P/conceptual/EXEMPLARS_AND_LESSONS.md` X-09, X-19, X-20.
  - `P/execution/_Decomposition/Open_Issues.csv` OI-001, OI-002, OI-013, OI-014, OI-021; `External_Dependencies.csv` DEP-001.
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
- Receivers:
  - From `Dependencies.csv` DEP-04-01-012…016: DEL-02-01, DEL-02-03, DEL-03-01, DEL-04-02, DEL-04-03.
  - Declared upstream in the receivers' own registers:
    - DEL-03-02 (DEP-03-02-017);
    - DEL-03-03 (DEP-03-03-008);
    - DEL-05-01 (DEP-05-01-018);
    - DEL-05-02 (DEP-05-02-008/-014/-015);
    - DEL-01-04 (DEP-01-04-011);
    - DEL-09-09 (DEP-09-09-010).
  - DEL-01-01 receives the D3 value.
  - Further declared consumers are in §10.3.
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
has adopted or enforces any value (DEP-001).

| Label | Meaning here |
|---|---|
| **SETTLED** | Stated in the accepted composite (B-ACCEPT) and cited |
| **ADOPTED** | Owner ruling `APP-V4-FIRST-INCREMENT-20260928-DECISION-1` (D2/D3), credited only with what it says (R2-11) |
| **DERIVED** | A direct consequence of settled or adopted clauses, with the derivation shown |
| **INTEGRATION** | An R1/R2 integrator choice. Reviewable, and open to owner revision. |
| **PROPOSED** | A design choice of this contribution or a sibling, open to review |
| **UNRESOLVED{…}** / relay question | An open item with owner and point of need |

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
| A8 | **request** | prepare or request a person's act | Agent | A request naming the exact act kind, subject and purpose | The request, with the requester identified | Anything. A request is never the act. | Agent-available. An A8 exists only when the agent actually issues it (R2-4). | V4-AUT-03; V4-HI-31; V4-PM-04 |
| A9 | **record** | faithful recording; direct capture | *Recorder*: the capturing surface (direct capture), or another identified party such as the host facility, the App or an agent (faithful recording). A person recording their own act is direct capture by the capturing surface. | An actually performed act of kind A4–A7, A10–A13, or an act-declined event | Reference to the act's evidence, recorder identity, and *recording mode* ∈ {direct capture, faithful recording} | The act itself. **A9 is a recording act, not a decision act**, and it never satisfies a checkpoint on its own. | Faithful recording by any identified recorder distinct from the decision actor is a conformant shape (SETTLED S3). Capture requirement: DEP-001. | SoW REQ-002; d3; V4-HI-31; R-1; R-5 |
| A10 | **reject** | reject a proposal or item; a person removing another party's proposal | The person | One or more identified change items | Host lifecycle record `rejected`, with actor | Anything beyond non-acceptance of those items | **Reserved** wherever A5 is — DERIVED (decision pair of A5; R-1) | V4-HI-23; V4-EXM-20 |
| A11 | **withdraw** | withdraw one's own proposal | The proposer only | Its own proposal | Host lifecycle record `withdrawn` | A decision on the proposal's merit | Proposer's act. It is a human-act record only when the person is the proposer. | V4-HI-23; R-1 |
| A12 | **set grant** | set or change the autonomy grant | The person | **Setting content**: operation classes, grant values and scope (§2.5, §5.4) | Capture evidence from the control surface. The version the control establishes, or the control's refusal, is a relation on the act. | That an agent's A8 established anything | **Reserved** — ADOPTED D2e | V4-AUT-01; V4-HI-40, -41 |
| A13 | **enable external access** (includes disabling) | enable or disable external-agent access | The person | The host's external interface on this machine (enablement setting) | The host enablement record captured by the host's enablement facility, with a capture-evidence reference (§2.6). App-side access configuration is never A13 evidence (R4-13). | Any grant for an operation class | Enabling: **reserved**, ADOPTED D2e. Disabling: **reserved**, INTEGRATION (R2-3). An agent may request either (A8). Off by default and local: SETTLED. | V4-HI-52 |
| A14 | **answer tool permission** | harness "approval" of tool use; routine tool permission | The person, or the user's own Codex permission mode inside the supplier | One tool-execution request | Request settlement: answered, or explicitly declined, or errored; never by silence or timeout. Recorded only in run record R13 (R2-8). | Any of A4–A7, A10, A12, A13, or a host-operation grant | ADOPTED D3: App modes are the user's Codex setting; hosts have no classifier mode. INTEGRATION (R-2): the App never answers affirmatively by rule; a decline or error is allowed only under a named rule with truthful origin. | V4-AUT-04; V4-EXE-02; D3 |

Alias exclusions (R-1):
- Design-candidate approval (V4-CON-05; V4-HI-65) is a separate act in a later
  increment. It is **not** A6.
- The word *accept* belongs to A5 alone.

Other human acts keep the attribution invariants but have no canonical name
here:
- workflow registration (V4-WF-02; U-08);
- stopping work (V4-EXE-01), which produces a run-ended event (§4.3);
- reserved coordination decisions (V4-PM-04).

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
    disposition and no act. Under the capture-after-arrival rule (§4.5), acts
    made before its arrivals are shown "prior act on this subject, not
    counted".
  - An **interruption is not a run end**. A run whose observation was lost is
    recovered as the same run (EXEC §4.12).

### 2.4 Recorded-act element meaning

This is the meaning DEL-04-03 receives. DEL-04-03 owns the format.

| Element | Meaning | Presence |
|---|---|---|
| *act kind* | One of A4, A5, A6, A7, A10, A12, A13, or A11 when the person is the proposer; or the act-declined event with its declined kind. A9 is carried as *recording mode*. A14 is never a human-act record (R2-8). | Always |
| *decision actor* | The person who actually performed the act | Always |
| *recorder* and *recording mode* | Who wrote the record; direct capture or faithful recording | Always |
| *subject content identity*, *scope*, *purpose* | What the act concerned (§2.5) | Always |
| *evidence reference* | Capture evidence from the capturing surface, linked and not copied (V4-HI-71) | Always. Without it, the record is non-conformant. |
| *lapse state* | Relative to current content (V4-HI-32). *superseded* for A12/A13. | When applicable |
| *governing policy reference* | The policy-class record and policy revision identity (§8.1) | Optional. Present when a catalog operation governed the act. |

A record is non-conformant if it names the recorder as the decision actor of
an A4–A7, A10, A12 or A13 act, or if its person-attributed act has no evidence
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
- Acceptance granularity:
  - Batch or multi-row acceptance is one A5 act listing several items, each
    bound to its own item and lapsing on its own.
  - Row-by-row acceptance is one A5 per item.
- What purpose a multi-row A4 keeps after partial lapse is an owner question
  (U-03).
- Every content identity carries its identity-method designation. The
  algorithm is unselected.
- The lapse-state vocabulary is DEL-04-03's. This contract adds
  **superseded** for A12/A13 (IR1A-13).

### 2.6 Capturing surfaces, and what is never act evidence (R4-12, R4-13)

| Act | Capturing surface | Never act evidence |
|---|---|---|
| A4, A5, A6, A7, A10 on host content | The host's act facility (V4-HI-31). The capture-evidence reference is a relay question (U-04). | An agent-authored record without that reference |
| A4, A6, A7 on App content | The App interface's act control (EXEC CAP-1…CAP-3). The control is built by DEL-01-04 in a later undertaking. | See rows below |
| A12 | The control that establishes the setting: the host's control for host operation classes; an App control only for a setting the App itself establishes (EXEC CAP-1) | An agent's A8, or any setting an agent wrote |
| **A13** (external access on the host's interface) | **The host's enablement facility.** It records the host enablement with a capture-evidence reference. The host's refusal (*channel not enabled*) is the authoritative "off" (ADAPTER E-2, F-2). | **App-side access configuration.** Examples: the user's Codex configuration file, a per-thread configuration, or a plugin setting. An agent could write any of them, so none is ever A13 or A13 evidence. The App changes that configuration only at the person's direction (ADAPTER E-4). That change is an ordinary configuration change, recorded as such. It is not a second A13, and it enables nothing without the host enablement record (ADAPTER E-3). |
| Any act | — | Answers to Codex user-input or MCP elicitation requests (EXEC CAP-6; HOSTING R9); A14 settlements from any origin (CAP-5); conversation statements (CAP-7) |

- **Standing: PROPOSED by DEL-04-01 under R4-13.** This closes ADAPTER
  U-X1 as ruled.
- **Still open:**
  - whether a given host requires its own facility to capture A13 (DEP-001,
    within U-04);
  - A13 for an App-owned external interface, which does not exist in this
    increment. If one is introduced, its App control would be the capturing
    surface under EXEC CAP-2/CAP-3.

---

## 3. Settled distinctions S1–S12 and adopted rulings

Each was checked against the cited bytes at repo 6e18505e3.

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
| S9 | Declared checkpoints override autonomy. | V4-HI-42; V4-WF-05 | §4 |
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
DEL-02-03 owns the hold machine (EXEC-v0.2 §4). This section supplies the act-policy
meaning that those three consume.

### 4.1 Acts a checkpoint may require (closed list)

A declared checkpoint requires exactly one of **A4, A5, A6, A7 or A12**
(R-1).
- A recognized act kind outside this list, or no act kind at all, makes the
  checkpoint **invalid**. Examples: A1, A2, A3, A8, A9, A10, A11, A13, A14,
  and design-candidate approval (WD FB-03; R2-10).
- An unrecognized name is preserved and reported **not established**, and is
  never matched to a nearby act kind (WD FB-04).

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
    as "waiting — lapsed at ‹t›", for a new act on current content.
  - **After resume, run live:** the **same arrival** is re-held, shown as
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
  - **Whatever causes the lapse re-holds (R5-5).** This includes the
    person's own undo. The person's undo is the person's operation and is
    never recorded as "action during hold".
  - **A5 and A12 never re-hold.**
    - Applying an item does not lapse its A5, and a basis failure is the
      stale rule.
    - An undo never re-holds an A5 arrival.
    - An A12 is superseded, not lapsed (§2.5).
  - **lapsed** as a standing disposition is used only for a checkpoint whose
    run has ended. If the run ends while re-held, the disposition stays
    *waiting* with the run-ended event (EXEC RH-7).
  - Partial lapse (only some referents) follows the whole-scope request. That
    request is valid under every option of the open owner question U-03.
- **Run ended while waiting (R2-5; R4-4).** The disposition stays
  **waiting**, with a run-ended event. The run is never resumed (§2.3). An act
  performed later is recorded, shown "after run end", and changes nothing.
- **unknown.** Observation was lost. Never shown as *performed*.

### 4.4 Acceptance-checkpoint constraint (DERIVED from V4-HI-42 + D2b; R2-12)

If a declared checkpoint requires A5 on an operation's result, that
operation's treatment in that run is **propose**, whatever the grant.

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
  evidence limit. This makes the SQ-02 option in which the host evaluates the
  declaration itself the only route to satisfaction in this increment.
- A direct request under the constraint is **not permitted**, and the outcome
  names the constraint as the governing treatment. It is never converted into
  a proposal. The agent may submit a proposal separately.
- A workflow that wants direct application followed by a person's act must
  declare A4 on the applied result instead.
- **Relay question (DEP-001).** Does the host route receive the constraint, or
  does it evaluate its own copy of the declaration? A missing constraint looks
  the same as no constraint at all. Until host evidence exists, dependent
  fixtures are **AWAITING INPUT** (FX-29; LOOP FX-C9, PANEL PC-24, WD VC-11).

### 4.5 Which evidence satisfies a checkpoint (R-5; R2-20)

- Any identified recorder distinct from the decision actor produces a
  conformant **record shape** (A9, SETTLED S3).
- **Satisfaction** requires capture evidence from the **capturing surface**:
  - the host's act facility, for acts on host content (V4-HI-31);
  - the App interface, for acts in the App (WD U-25).
- A faithful record by another recorder is valid as a record, and it must cite
  that evidence. The loop resumes on the capture evidence, never on an
  agent-authored record alone.
- **Relay question (DEP-001):** the host's capture-evidence reference.
  Without it, no host-content checkpoint can be *performed*. Any host-specific
  capture requirement is the host's (U-04).
- **Never act evidence (R4-12):**
  - answers to Codex user-input or MCP elicitation requests;
  - A14 settlements;
  - conversation statements.

  See §2.6.
- **Capture after arrival (R4-5; EXEC SP-6; PROPOSED).** An act counts toward
  an arrival only if it was captured **at or after that arrival**.
  - Order comes from a request relation where the capturing surface records
    one, and otherwise from evidenced times.
  - An earlier act on the same subject is shown **"prior act on this subject,
    not counted"**, so the person can repeat it knowingly.
  - If the order cannot be established, the act does not count and the
    arrival shows **"act order unknown"**.
  - The rule adds no ordering *between* act kinds. For an A5 arrival at kind
    (c) *queued*, it always holds.
  - The alternative, counting a prior act bound to current content, remains
    an owner question (U-14).
- For A12, the act counts only when its control relation is **established**
  (§2.5).

### 4.6 Hold support and App-side holds (R4-2; DECISION-2 D6; EXEC §2, §3.6)

- A checkpoint relied on in a run is only as strong as the surface's ability
  to hold the run. For each declared checkpoint and acting surface, the
  required-tool compatibility report states its **hold support** (EXEC §3.6).
  Each checkpoint on each surface takes exactly one of four values (R5-1):

  | Value | Meaning | Requirement check |
  |---|---|---|
  | **enforced by the host loop** | Embedded route: the host loop holds the run (LOOP §2.4.4) | Passes. Holds are subject to host evidence (DEP-001). |
  | **enforced on the host route** | The host holds or refuses the operation through a **host-held** constraint (§4.4), evidenced by the host's answer to SQ-02 and a candidate | Passes |
  | **not established** | Depends on a host answer not yet given (SQ-02), or on unagreed exposure | *not established*. Never a pass, and never "unsupported". |
  | **not enforceable** | No mechanism exists on this surface in this increment. Examples: App-only steps with no host operation (R4-2 / D6); a constraint carried only as model-supplied, once SQ-02 is answered with no host-held route (HS-3; before that answer, *not established*). | *unsupported*, reason "checkpoint hold not enforceable on this surface" (R4-8) |

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
    - answered with no host-held route → *not enforceable*.
  - **App-side class (HS-5):** at least one held action is App-side, such as
    an App agent turn, an App tool or harness action, or an App file write or
    return step. In App runs this is *not enforceable* (D6), whatever SQ-02
    returns.
  - **Invalid declarations (HS-1)** take **no value**, and the check is *not
    established*.
- **What "held" means for each value (R6-3):**

  | Value | What happens at the hold |
  |---|---|
  | *enforced by the host loop* | The run stops at its next action. |
  | *enforced on the host route* | The host refuses the held host operations. Any other action is recorded as *action during hold*. |
  | *not established* / *not enforceable* | Nothing is stopped. Actions are recorded as *action during hold*. |

- **Consequences (R5-1, R6-1).**
  - E1 run from the App through the external channel (surface X):
    - `CP-accept` → **not established**, awaiting SQ-02;
    - `CP-check` (it holds the Return step, which is App-side) → **not
      enforceable**;
    - the workflow → *unsupported*.
  - `CP-L4` (L-ACT-4) holds only host operations: the run's further host
    operations after T16 until the A4. It is therefore HS-3:
    - App run over X: *not established* until SQ-02 is answered;
    - host loop: *enforced by the host loop*.
    - A variant that also holds an App-side return step is *not enforceable*
      in App runs (FX-48(d)).
    - Counterpart in DEL-04-02: AS F6d (the L-AS-4 A4 on S-4, declared to
      hold only host operations → HS-3); AS F6c, which holds App agent
      turns, is HS-5.
  - Advice to workflow authors (WR-11): keep a checkpoint's held actions on
    host operations if the checkpoint must be enforceable from the App.
- This contract, and every consumer that cites it, **never states or implies an
  App hold that the surface cannot enforce**.
- Any run action taken while an arrival waits, and not stopped under the
  value in force, is recorded as **action during hold** with its reference.
  It is never hidden. Under every value other than *enforced by the host loop*,
  App-side actions continue and are recorded this way (R6-3).
- **App-side run holds are `UNRESOLVED{D6}`** (owner DECISION-2: "Defer to
  SWBPIPE answer"), pending SWBPIPE relay question SQ-02. Meanwhile:
  - HP-1, interposed App code holding a call before dispatch, is **not
    adopted**;
  - HP-2, reliance on supplier `turn/interrupt`, is **not adopted**;
  - HP-3, an App named-rule *decline* of a tool-permission request, remains a
    **permitted best effort** under D3 and R-2. It never answers
    affirmatively and never counts as a hold guarantee.
- A reached-when kind (a) on a **harness capability** is **not holdable** in
  App runs pending D6 (R4-21).
- In host loops, holding is the host loop's (DEL-05-01 receiving; OI-013).
  Its value is *enforced by the host loop*.
- *Enforced on the host route* for the A5 constraint awaits host evidence and
  the SQ-02 answer (§4.4; U-04). The SQ-02 answer decides holds for
  checkpoints on **host operations** only. App-only checkpointed workflows
  remain *not enforceable* whatever SWBPIPE answers. That is a separate D6
  follow-up for the owner (R5-10; F-16).
- The policy meaning of a checkpoint is unchanged by weak hold support. A
  checkpoint still overrides any grant (S9) and is still satisfied only by
  capture evidence (§4.5). Weak hold support limits what can truthfully be
  **claimed** about enforcement. It does not weaken what the act means.

---

## 5. Autonomy-grant model

### 5.1 Inputs (semantic)

| Input | Meaning | Supplier / standing |
|---|---|---|
| *operation identity* and *operation class* | The catalog operation and its host-named class | DEL-03-01 (V4-HI-01/02); host names classes (V4-HI-30) |
| *catalog human-act class* | **none** · **may apply within granted autonomy** · **proposal only** · **reserved to the person**, all SETTLED by V4-HI-02. Fifth value: **no policy basis**, with *reason* ∈ {omitted, unassigned, pending OI-021}, labeled INTEGRATION (R-3.5; R2-1). | Values from §8. OI-002 is not a class value (D3; R-2). |
| *consequence statement* | Effect, reversibility, available examination, intended delegation (d3) | Vocabulary open (U-02) |
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
| W-b | bypass a declared checkpoint or the §4.4 constraint | S9; D2 |
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

---

## 7. SWB model-change class — DERIVED class, accepted default

> The class value is **DERIVED** from V4-HI-41 "the person may widen it", so
> the class is *may apply within granted autonomy*. The default *propose* is
> **ACCEPTED** (V4-HI-41, via B-ACCEPT). Operation-specific additions are
> pending OI-021. Host adoption is **not evidenced** (DEP-001).

The policy-class record is P-03 (§8.3). In the fixture, OP-C4, OP-C5 and
OP-C9 carry it (C-v0.4 §10.2).

- Acceptance granularity:
  - Row-by-row acceptance is one A5 per change item.
  - Multi-row or whole-batch acceptance is one A5 act listing several items.
  - Each item binds and lapses on its own.
- Batch acceptance is not A4 or A6 of any row. Acceptance is not application.
- A5 and A10 on these proposals are reserved (P-01, P-01a).
- With no person setting, the grant state is **effective (policy default):
  propose** (R2-6).

**Fixture walk-through (C-v0.4 §10.3, invented material).**

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
| *policy revision identity* | Cited by consumers in their governing-policy element. This revision is DEL-04-01/ACT-POLICY-v0.5 plus its content identity; the method is unselected. |
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
| *host adoption* | Currently **unevidenced** for every record (DEP-001) |
| *consumers* | §10 |

Rules:
- No value is carried without a decision basis. Historical drafts, fixture
  expectations and pending recommendations are not bases.
- An open value names its item, owner and point of need.

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
| Not established | SWBPIPE adoption or enforcement (DEP-001); `Open_Issues.csv` rewrite (C1) |

### 8.3 Policy-class records

**P-01 — reserved acts (D2).**
- Values:
  - A4 mark checked;
  - A5 accept, where the autonomy requires a proposal;
  - A6 approve;
  - A7 rely;
  - A12 set grant;
  - A13 enabling external access.
- Catalog class: reserved to the person. Widenable: **no**, neither past these
  acts nor past a declared checkpoint.
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
| Consequence vocabulary | U-02 | DEL-04-01 with the host policy owner | Before class assignment in DEL-03-01 |
| Defaults for other consequential classes | U-06 | Host policy owner (DEP-001) | Before those classes are cataloged |
| Host capture requirements and capture-evidence reference; host faithful-record operation; checkpoint-constraint reception; host adoption of P-01…P-06 | U-04 (relay questions) | Host owner (DEP-001) | Before host act-recording integration or any enforcement claim |

---

## 9. Label rules (R-4; S7; S4)

| Word | Allowed use | Not allowed |
|---|---|---|
| **accept / reject / withdraw** | Proposal decisions (A5, A10, A11) | For A7 (use *rely*). For A10, write "rejected the item", not "declined the item". |
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
| V-01 | Canonical names A1–A14; the human-act record kinds; act-declined and run-ended events (§2) | S3, S5, S7, S11; R-1; R2-5 | DEL-04-03, DEL-02-01, DEL-04-02, DEL-05-01, DEL-05-02, DEL-01-04 |
| V-02 | Class vocabulary: four SETTLED values plus *no policy basis* with reason (INTEGRATION) | V4-HI-02; R2-1 | DEL-03-01 element 8; DEL-03-02; DEL-05-01 (five values); DEL-03-03 |
| V-03 | Resolution order §5.3, resolution point, widening bounds §5.6 | S1, S8–S10, S12; D2; R-3; R2-6, R2-9 | DEL-03-02, DEL-05-01 (relay only), DEL-02-03, DEL-04-02, DEL-03-03 |
| V-04 | Grant by A12, with scope, the seven states including *effective (policy default)*, and two settings references | V4-AUT-01; V4-HI-40; D2e; R-8; R2-6 | DEL-04-02, DEL-04-03, DEL-05-01, DEL-03-02 (standing at drafting) |
| V-05 | Outcome map §6, including offered reserved entries, host-reported *not exposed* and loop *not offered* | V4-HI-23, -25; R-3; R-7; R2-4 | DEL-03-01 §4.1; DEL-03-02 P §9; DEL-05-01; DEL-05-02; DEL-04-03; DEL-01-04 |
| V-06 | Content binding, lapse, supersession and undo (§2.5) | V4-HI-32; V4-REC-05; R-6; R2-7; R2-15 | DEL-04-03, DEL-03-01, DEL-03-02, DEL-04-02, DEL-05-02, DEL-02-01 (SB-4/U-27) |
| V-07 | Label rules §9 | V4-HI-33; R-4 | DEL-05-02, DEL-01-04, DEL-04-02, DEL-02-01, DEL-03-02, DEL-04-03 |
| V-08 | No professional standing from agent output | V4-AUT-05 | DEL-04-02, DEL-05-02, DEL-01-04, DEL-09-09 |
| V-09 | Checkpoint rules §4, including the resume point, re-hold, capture after arrival, no resumption, hold support and carriage assurance | V4-HI-42; V4-WF-05; D2; R-5; R2-10, R2-12, R2-17…R2-20; R4-2…R4-6, R4-9, R4-14 | DEL-02-01, DEL-02-03, DEL-05-01, DEL-05-02, DEL-03-02, DEL-03-03 |
| V-10 | External access: same settings and reserved acts; A13 reserved and captured by the host's enablement facility; App-side configuration never A13 evidence; *channel not enabled*. The model destination is a record and status element, not a policy value. Host content may flow to the selected model with no gating: SETTLED (DECISION-2). Recording and showing the destination per turn: INTEGRATION (DECISION-2 reading) (R5-4). | V4-HI-50…52; D2e; R2-3; R4-13 | DEL-03-03, DEL-09-09, DEL-04-03 |
| V-11 | SWB record P-03 | V4-HI-41 | DEL-03-01, DEL-03-02, DEL-04-02, DEL-04-03, DEL-05-01, DEL-05-02, DEL-09-09 |
| V-12 | A3 ≠ A4 | d3; V4-EXM-21 | DEL-05-02, DEL-04-02, DEL-04-03 |
| V-13 | A9 record shape, the capture-evidence rule, and the capturing surfaces and never-evidence list (§2.6) | S3; R-5; R2-20; R4-12, R4-13 | DEL-04-03, DEL-05-01, DEL-05-02, DEL-02-01, DEL-09-09 |
| V-14 | P-01, P-01a, P-02 | D2; DERIVED; R2-2 | DEL-03-01 (OP-C6/C7/C8), DEL-05-02 K-4, DEL-03-02, DEL-03-03, DEL-04-02, DEL-02-01, DEL-09-09 |
| V-21 | P-04 routine tool permission | D3 plus INTEGRATION | DEL-01-01, DEL-01-04, DEL-01-02, DEL-05-01 (no permission layer in hosts), DEL-05-02, DEL-04-02, DEL-04-03 |
| V-25 | A14 recorded only in R13 (not applicable in host-loop runs) | R2-8 | DEL-04-03, DEL-01-01 |

### 10.2 Values held

| # | Value | Standing | Consumers that must hold |
|---|---|---|---|
| V-20 / V-22 | Operation-specific reserved additions; first connected operation, its autonomy and environment | `UNRESOLVED{OI-021}` | DEL-03-01, DEL-05-01, DEL-05-02, DEL-09-09 |
| V-23 | Consequence vocabulary; other host defaults | U-02, U-06 | DEL-03-01, DEL-04-02 |
| V-24 | Multi-row A4 purpose after partial lapse | U-03 | DEL-04-03, DEL-04-02 |
| V-26 | App-side run holds | `UNRESOLVED{D6}` (U-D6; SWBPIPE SQ-02) | DEL-02-03, DEL-02-01, DEL-03-03, DEL-05-02 |
| V-27 | Counting a prior act captured before arrival (alternative to §4.5) | U-14 (owner) | DEL-02-03, DEL-02-01, DEL-04-03 |

### 10.3 Other declared consumers (not mapped in detail)

- DEL-01-02 (DEP-01-02-021)
- DEL-02-02 (DEP-02-02-016)
- DEL-03-04 (DEP-03-04-011)
- DEL-06-02 (DEP-06-02-009)
- DEL-09-02 (DEP-09-02-018)
- DEL-09-05 (DEP-09-05-009)
- DEL-09-12 (DEP-09-12-011)
- DEL-10-03 (DEP-10-03-013)

Of these, DEL-01-02, DEL-02-02 and DEL-09-02 are outside this undertaking
(D1). The register mirrors go to C1.

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
   the act's purpose survive for the other rows?
3. **Consequence vocabulary** (DEL-04-01 with the host policy owner, U-02).
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
5. **App-side run holds** (`UNRESOLVED{D6}`; SWBPIPE SQ-02; U-D6).
   Separately, whether prior acts captured before arrival should count; this
   is an owner question (U-14; EXEC U-E4).
6. **Workflow registration** as a canonical act (DEL-04-01 with DEL-02-02,
   later undertaking, U-08).

---

## 13. Fixture catalogue (OUT-003) — designed, not run

**Sources.** Subjects come from **C-v0.4 §10** (R2-21; R4-18; R5-9):

- **Model:** FX-PIPE-01, run 12, R-100, supports S-1…S-4 and S-5 (created at T12), Engineer A.
- **Fixture assumptions:** FXA-1…FXA-5, renamed from FA-n; the alias is kept by C (R5-9; V3-A m-3). FXA-1 exposes every entry on all three surfaces. FXA-5 states that ⟨rev-3⟩ (WD-EX E1) declares `CP-accept` (A5) and `CP-check` (A4 on objects changed by `CP-accept` items' applied outcomes).
- **App-side subjects:** LIB-A1, LIB-A2, AF-1.
- **Entries:** OP-C1…C12.
- **Timeline:** T1–T17, including T4a and T16a.
- **Proposals, receipts and settings:** PR-1/PR-2, RC-1…RC-3, ⟨set-1⟩/⟨set-2⟩.
- **Variants:** V-S1, V-CP1, V-NP1, V-R1, V-X1, V-OU1 and V-ED1, plus **V-GR1** (R5-7; present in C-v0.5 §10.4 with GR-P/GR-R/GR-S). V-GR1 is a run of WD-EX E1d in which `CP-grant` arrives at r15, T15's A12 is captured *after* the arrival, and the held OP-C9 call is then dispatched unchanged as T16.

**Local additions, named per R2-21 (V3-A m-13).** Retired labels are not reused (V3-A MAJOR-4):
- L-ACT-1 and L-ACT-3 were retired in v0.4;
- the v0.4 local checkpoint CP-3 is replaced by C's V-GR1 (R5-7).

| Label | What it is | Why it is local |
|---|---|---|
| **L-ACT-2** | A batch A5 over PR-2 items 1 and 2 | C's T11 uses a separate A5 and A10 |
| **L-ACT-4** checkpoint `CP-L4` | Requires A4. Reached-when kind (c): on the observed outcome of OP-C9 at T16. Subject class *objects changed by the named outcome*, which binds S-4. Held actions: the run's further host operations until the A4 (HS-3, R6-1). | C's `CP-check` (FXA-5) binds objects changed by `CP-accept` items. The T16 direct OP-C9 outcome is not a `CP-accept` item, so a checkpoint on a direct-branch outcome must be local. |
| **L-ACT-5** checkpoint `CP-L5` | Requires A4. Reached-when kind (b): on production of the T3 OP-C1 output. Subject class *objects a named output concerns*, which binds S-1…S-4 as read at r12 (R3-1). | For the capture-after-arrival case (R4-5). C schedules no checkpoint at T3. |
| **L-ACT-6** FX-Professional-P | An invented accountable professional | C names only Engineer A. A7 needs a professional. |
| **L-ACT-7** | A variant of `CP-grant` (V-GR1) whose reached-when kind (a) names a **harness capability** instead of OP-C9, in an App run | For hold support "not enforceable" (R4-21). C has no harness-capability entry. |

Rules for reading the table:

- Expected results are contract expectations. They establish no act.
- Host-dependent results need DEP-001 evidence.
- App-side hold enforcement is **HELD on D6** (§4.6).
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
| FX-21 | Checkpoint | CP-L4 arrives at T16. T16a: Engineer A's A4 on ⟨S-4@r16⟩, captured after arrival. | *waiting*, then *performed*, then a run-resumed event. Before T16a the agent may only request (A8). | VER-001, -006 |
| FX-22 | Reserved operation (C V-R1) | At T3 the agent calls OP-C6 on S-1, under any grant. | *not permitted*. An A8 is **offered** and recorded only if issued. No attribution to the person. | VER-004, -006 |
| FX-23 | Grant change | The agent requests widening, then attempts to set it. | The request shows as *requested by agent (A8)*. The set attempt is *not permitted* (P-01). | VER-001, -004 |
| FX-24 | External | External access is off (no A13 in the host facility). | *channel not enabled*, not *unavailable*. The reporter is the App (App configuration off) or the host (host channel off) (R4-16). | VER-004 |
| FX-25 | External | A13 is performed in the host facility. The external agent **drives T9–T10 and observes T11–T12** (R4-17). | Same lifecycle and settings as the embedded agent. A5/A10 are attributed to Engineer A. | VER-004 |
| FX-26 | Examination | T4 OP-C3. | Findings by reference. No A4 and no "host check". | VER-002 |
| FX-27 | Lapse | T2's A4 on S-2 at r12; T6 edits S-3 (control); T14 edits S-2 at r15. | Not lapsed at r13/r14. At T14 an **act-lapsed event** is recorded, and the act shows lapsed with its r12 identity. | VER-002 |
| FX-28 | Boundary | The contract asserts host enforcement without DEP-001. | Non-conformant. | VER-008 |
| FX-29 | Acceptance checkpoint (C V-CP1) | CP-accept (FXA-5) on OP-C4 results, with the V-CP1 direct grant. The agent requests OP-C4 directly. | *not permitted*, naming the constraint {run 12, CP-accept, A5, OP-C4}. Never converted. **AWAITING INPUT** (host receipt of the constraint; SQ-02). | VER-001, -006 |
| FX-30 | Negative A5 | CP-accept over PR-2 (arrival at T10, *queued*). T11: A5 on item 1, A10 on item 2. | *resolved negatively* with a *partial* annotation (WD §4.3.7; confirmed by DEL-02-03, R4-7). Item 1's A5 proceeds. Never "all accepted". | VER-002 |
| FX-31 | Act-declined | CP-L4: Engineer A declines to mark S-4 checked. | **Act-declined event** with capture evidence; *resolved negatively*; the on-negative path governs; no A4. | VER-002 |
| FX-32 | L-ACT-2 | A batch A5 over PR-2 items 1 and 2; item 1 is applied (RC-1). | One A5 act lists both items, each bound to its own change-item content identity. Item 1's A5 is not lapsed by RC-1. | VER-002, -006 |
| FX-33 | A14 origin | An App rule answers a tool permission affirmatively; separately, a named-rule decline. | The affirmative answer is non-conformant. The named decline with truthful origin is conformant and recorded in R13. | VER-004 |
| FX-34 | "checked" label | The T1 host result is labeled "Checked"; the T4 findings are labeled "agent-checked"; T4a is shown. | The first two are non-conformant: they must read "host checks passed: equilibrium, unit consistency" and "agent-examined (non-mutating)". T4a must read "host check failed: support spacing". | VER-005 |
| FX-35 | Offering reserved (C V-R1, V-X1) | (a) As V-R1. (b) A variant reports OP-C6 as *not exposed* or *unavailable* for a class reason. (c) V-X1: OP-C9, not exposed on X. | (a) *not permitted*, with an A8 offered and not auto-recorded. (b) Non-conformant. (c) The host reports *not exposed on this surface* (exposure, not class), and the adapter relays it. | VER-004 |
| FX-36 | Checkpoint evidence | The agent writes an A4 record for CP-L4 without citing host capture evidence. | Not a satisfaction. The run does not resume. | VER-002, -004 |
| FX-37 | Narrowing | PR-2 is queued (T10). After T15, a direct OP-C9 request on S-4 is in validation. Engineer A narrows ⟨set-2⟩ to *propose* (an A12 that is established). | PR-2 is unaffected. The OP-C9 request is re-resolved at application → *not permitted*, never converted. | VER-001, -006 |
| FX-38 | Widening | PR-2 is queued. Engineer A widens P-03 to *direct* (T15). | PR-2 stays a proposal. | VER-006 |
| FX-39 | Undo (C T16a/T17) | CP-L4 is performed by T16a's A4 on S-4, and the run resumes. At T17, OP-C10 RC-3 reverses RC-2 and S-4 changes. | An act-lapsed event is recorded. CP-L4 is **re-held**: "waiting — re-held, lapsed at T17 after resume" (R4-3). What the re-hold stops depends on the surface's value (§4.6, R6-3): the run stops at its next action only where it is *enforced by the host loop*. Nothing is undone. The act record is not erased. A5/A10 on a reversed item would stay bound. | VER-002 |
| FX-40 | Run ended | CP-L4 is waiting (T16a not yet done). Engineer A stops run 12, then performs T16a's A4. The person starts a new run, "continues run 12". | Run 12's CP-L4 stays *waiting* with a run-ended event. The later A4 is shown "after run end" and changes nothing. The new run inherits nothing, and its arrivals show T16a as "prior act on this subject, not counted" (R4-4). | VER-002 |
| FX-41 | Supersession (C V-GR1) | `CP-grant` is performed by T15's A12, captured after the r15 arrival and established as ⟨set-2⟩. Later: (a) an established A12 narrows P-03's scope; (b) an A12 that the control refuses. | (a) The first A12 shows *superseded by ⟨act⟩*, not lapsed; `CP-grant` stays *performed*. (b) No supersession; ⟨set-2⟩ stays in force (R4-6). | VER-001, -002 |
| FX-42 | A13 disable | The agent attempts to disable external access; separately, the agent requests it. | The attempt is *not permitted* (INTEGRATION, R2-3). The request is an A8, offered. | VER-004 |
| FX-43 | A10 operation | The agent invokes OP-C8. | *not permitted* (P-02). An A8 is offered. | VER-004 |
| FX-44 | Checkpoint list | Checkpoint variants: (i) naming A3; (ii) naming A10; (iii) naming "sign-off"; (iv) a `CP-grant` variant whose declaration names no setting content, even when an A8 at arrival presents one. | (i) and (ii) **invalid**. (iii) **not established**. (iv) **invalid**, unconditionally and before the run (R5-3; WD FB-17; WD VC-41; EXEC CH-29). | VER-001 |
| FX-45 | Capture after arrival (R4-5) | CP-L5 arrives at T3. T2's A4 on S-2 was captured before that arrival. | T2's A4 is shown "prior act on this subject, not counted". CP-L5 stays *waiting* for an A4 over S-1…S-4 captured after T3. An act whose order cannot be established → "act order unknown". PROPOSED; the owner alternative is U-14. | VER-002 |
| FX-46 | A12 control relation (C V-GR1) | At `CP-grant`, which arrived at r15 before T15, T15's A12 is (a) pending, (b) refused, or (c) has its confirmation observation lost. | (a) *waiting*, "A12 awaiting control confirmation". (b) *waiting*, "refused by control: ‹reason›"; ⟨set-1⟩ stays in force; no supersession. (c) *unknown*. | VER-001, -002 |
| FX-47 | A13 capture (R4-13) | (a) The agent writes an App-side access configuration (ADAPTER L-ADAPTER-2). (b) Engineer A directs an App-side configuration change in the App. (c) Engineer A enables access in the host's enablement facility. | (a) Not A13 and not A13 evidence; the channel stays disabled; an evidence limit is recorded. (b) An ordinary configuration change, not A13; it enables nothing alone. (c) A13, captured by the host with a capture-evidence reference, which is required (U-04e). | VER-004 |
| FX-48 | Hold support (R5-1; R4-2) | (a) L-ACT-7: an App run with `CP-grant` of kind (a) on a harness capability. (b) E1 run from the App over X. (c) An App run over X in which a run action occurs while `CP-L4` waits. (d) A `CP-L4` variant that also holds an App-side return step. | (a) *not enforceable*: the workflow is **unsupported**. (b) `CP-accept` is **not established** (awaiting SQ-02); `CP-check` holds Return, so it is *not enforceable*; the workflow is *unsupported*. (c) `CP-L4` is HS-3, so it is *not established* while SQ-02 is unanswered. Nothing is stopped; the action is recorded as **action during hold** (R6-3). (d) *not enforceable* (HS-5), whatever SQ-02 returns. App-side enforcement is **HELD on D6**. | VER-001 |
| FX-49 | Not act evidence (R4-12) | Engineer A answers an MCP elicitation "Mark S-4 checked? yes". Separately, a conversation statement: "I checked it". | Neither is A4 nor capture evidence. CP-L4 stays *waiting*. The App may present its own act control (EXEC CAP-6). | VER-002 |
| FX-50 | Carriage assurance (R5-2; R4-14) | As in V-CP1, with native carriage: the constraint is model-supplied only, and the model omits it. | Model-supplied carriage does not satisfy R2-12, and the omission is recorded as an evidence limit. `CP-accept` hold support: **not established** while SQ-02 is unanswered; **not enforceable** if the host holds no copy of the declaration (model-supplied only; R5-1). **HELD** on SQ-02. App side: `UNRESOLVED{D6}`. (The ADAPTER U-X3 citation is retired; EXEC §3.6 answered it. This is the HS-3 case for an A5 constraint.) | VER-004, -006 |
| FX-51 | Grant before arrival (R5-7) | An E1d run in which the arrival of `CP-grant` is the hold of the OP-C9 call at T16, *after* T15's A12. Compare V-GR1, where `CP-grant` arrives at r15, before T15. | Here T15's A12 is shown "prior act on this subject, not counted", and `CP-grant` stays *waiting*. This holds even though ⟨set-2⟩'s content is already in force: the person must repeat the grant change (the owner-visible cost in U-14). In V-GR1, T15 counts: *performed*, and the held call is dispatched unchanged as T16. | VER-001, -002 |
| FX-52 | A8 cannot change the subject (R5-3) | V-GR1, but the agent's A8 at arrival presents a narrower setting {P-03, *direct*, {FX-W1; {S-3}}} than the declared {FX-W1; {S-4}}. Engineer A performs an A12 on the A8's content, and the control establishes it. | The A12 is recorded and establishes its setting. It **satisfies nothing** at `CP-grant`, which stays *waiting* for an A12 on the declared content. | VER-001 |
| FX-53 | Operation records (R5-6) | (a) T2: Engineer A operates OP-C6 on S-2. (b) T6: Engineer A edits S-3 in the host UI (the person's own A2). | (a) One human-act record (A4, direct capture), and an R7 operation entry referencing it. (b) An R7 operation entry with the person as actor, and no human-act record. | VER-002 |

---

## 14. Findings (reported, scope unchanged)

- **F-1 Register asymmetry.** Five downstream rows against eighteen upstream-declared consumers (V1-A RF-02). Goes to C1.
- **F-2 Design-candidate approval.** It has no canonical name yet. One will be needed in the Domains increment.
- **F-3 A10 and A11.** Both are named by R-1. A10 is reserved by derivation, not by D2.
- **F-4 Consequence vocabulary.** Still no owner decision (U-02).
- **F-5, F-7 (closed in v0.3).**
- **F-6 D2(b) wording.** D2(b) does not address a voluntary proposal under a direct grant. S3 already makes every A5 a person's act.
- **F-8 OI rows.** OI-001 and OI-002 are ruled, but `Open_Issues.csv` still shows them open. Goes to C1.
- **F-9 (closed in v0.3).**
- **F-10 SoW wording (IR1A-20).** TBD-001/002, AC-004 and VER-004 still read OI-001/OI-002 as open. Goes to C1.
- **F-11 A13 disable is INTEGRATION.** D2e names only enabling. The owner may wish to confirm this.
- **F-12, F-13 (closed in v0.4).** V2 confirmed them against the sibling v0.3 texts (m-12).
- **F-14 Rules adopted by citation from EXEC.** EXEC-v0.2 marks these as ADOPTED by R4: re-hold (§4.7), A12 control relations (§4.10), and no resumption (§4.9, whose standing is still PROPOSED). SP-6 (capture after arrival) and App-side capture (§5) stay PROPOSED in EXEC. This contract carries each at the same standing. The §2.6 A13 ruling is PROPOSED (R4-13).
  - resume point, re-hold, capture after arrival, no resumption, A12 control relations (§2.3, §2.5, §4.3, §4.5);
  - the §2.6 A13 capture ruling.
- **F-15 (new) A13 depends on a host enablement facility.** If SWBPIPE has no enablement facility that yields a capture-evidence reference, A13 cannot be evidenced. The external channel then stays *not enabled* by this contract's reading, which is conservative but may block V4-EXM-25. Relay question U-04(e).
- **F-16 D6 leaves App-side checkpoint enforcement HELD, and App-only checkpoints can never be enforced in this increment.** Per R5-1 and R5-10, the SQ-02 answer can make checkpoints on **host operations** *enforced on the host route*. App-only checkpointed workflows remain *not enforceable*, and therefore *unsupported*, whatever SWBPIPE answers. That is a separate D6 follow-up for the owner. It affects the VER-001 checkpoint cases and V4-EXM-22 in App runs.
- **F-17 (new) Capture-after-arrival costs a repeat (R5-7).** Under SP-6, a grant change captured before its checkpoint's arrival does not count, even when its content is already in force (FX-51). The person must repeat it. This owner-visible cost is recorded under U-14 (EXEC U-E4; WD U-31).
- **F-18 (new) R5-3 reverses R4-9's A8 precedence.** The declared setting content now always binds. Consumers that implemented "A8 names the setting" (v0.4 §4.2) must change: WD, LOOP, PANEL and EXEC are listed by R5-3.
- **F-19 (new) Human-act records and R7.** The record kinds now split cleanly (R5-6): a reserved-act operation yields a human-act record referenced from R7, and the person's own A1/A2 yields an R7 entry only. DEL-04-03 should check that its R7 element carries the reference (RS R7).

---

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| U-01 `UNRESOLVED{OI-021}`: first operation, operation-specific reserved additions, its autonomy | Owner via the outside SWB session and App/shared owner | Before the connected-activity SoW and execution | No additions in P-01/P-03. A concrete first operation is *no policy basis* (pending OI-021); dependent cases are held. |
| U-02 Consequence vocabulary | DEL-04-01 with the host policy owner | Before class assignment in DEL-03-01 | Text in d3 dimensions only; OP-C5-on-S-4 under ⟨set-2⟩ held (C T15) |
| U-03 Multi-row A4 purpose after partial lapse | DEL-04-01 with the owner | At its point of need (R4 carries it) | The whole-scope re-request (§4.3) is valid under every option |
| U-04 Relay questions to the host (§12 item 4 a–f) | Host owner (DEP-001) | Before host act-recording integration, checkpoint execution, external enablement, or any enforcement claim | Host rows are receiving requirements; FX-29, FX-47(c) and FX-50 await input |
| U-05 Recorded person grant; actual performed-act evidence | The person (DEP-04-01-020, -021) | VER-001 and the VER-002 positive cases | Candidate-bound FX-09/FX-20 passes cannot run |
| U-06 Defaults for other consequential classes | Host policy owner (V4-HI-41; DEP-001) | Before those classes are cataloged | *not set* falls to rule 5 (reason unassigned) |
| U-08 Workflow registration as a canonical act | DEL-04-01 with DEL-02-02 (later undertaking, D1) | Before the DEL-02-02 definition | Not in R-1's table; not checkpoint-requirable |
| U-12 Placement of the policy representation | App/shared owners (OI-013, OI-014) | Before production allocation | Representation-neutral |
| U-D6 `UNRESOLVED{D6}` App-side run holds | Owner, deferred to the SWBPIPE SQ-02 answer (DECISION-2) | Before App-side checkpoint enforcement is claimed or fixtures run | §4.6 applies the four R5-1 values. HP-1 and HP-2 are not adopted, and App-assured carriage is unavailable. SQ-02 decides only checkpoints on host operations; App-only checkpoints stay *not enforceable* regardless (R5-10). FX-48 and FX-50 are HELD. |
| U-14 Counting a prior act captured before arrival, as an alternative to §4.5 capture-after-arrival | Owner (EXEC U-E4; WD U-31; carried by R4-5, R5-7) | Before hold-machine fixtures run | Capture-after-arrival applied as PROPOSED. Owner-visible cost: a grant change already in force must be repeated (FX-51). |

Closed:

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
| VC-001 | VER-001 / AC-001 | Compare §4, §5 and §8 with V4-AUT-01, V4-HI-22/40/42 and D2. Run FX-19…21, -23, -29, -37, -38, -41, -44, -46, -48, -51 and -52 against a recorded grant (U-05). Trace the origin, undo and later-check obligations. | Direct treatment occurs only in *effective (person-set)* direct within scope (C T15 scope). A policy default gives *propose*. Checkpoints and the §4.4 constraint (with its carriage assurance) override the grant. Hold support takes one of the four R5-1 values, and no App hold is claimed (D6). The declared grant setting binds (R5-3). Narrowing, widening, supersession and the A12 control relations follow §5.5 and §2.5. |
| VC-002 | VER-002 / AC-002 | Run FX-01…10, -26, -27, -30…32, -36, -39…41, -45, -46, -49 and -53. | Negatives are non-conformant. Independent acts are conformant without A5. Actor ≠ recorder is kept, with capture evidence. Act-declined and run-ended events are not acts. Capture after arrival, re-hold after resume and no resumption hold. Elicitation answers and conversation are never evidence. |
| VC-003 | VER-003 / AC-003 | Run FX-03, -05, -14 and -15. | No certification or approval claim for agent output. A7 is attributed only to the professional. |
| VC-004 | VER-004 / AC-004 | Compare P-01, P-01a and P-02 with DECISION-1 and their derivations, and inspect host evidence. Run FX-16…18, -22…25, -33, -35, -36, -42, -43, -47 and -50. | No agent can perform, or have attributed to it, a reserved act. Outcomes follow §6. A13 is evidenced only by the host facility. OI-021 and no-policy-basis cases are **held**. SQ-02-dependent cases are **held** or AWAITING INPUT. No host enforcement is claimed without DEP-001. |
| VC-005 | VER-005 / AC-005 | Inventory the wording in this file, §7, FX-11…13 and FX-34. | "accept" for proposals only. "approve" for A6 only. Unqualified "checked" for A4 only. "tool permission" for A14. "rejected", not "declined", for A10. |
| VC-006 | VER-006 / AC-006 | Run FX-19…22, -29, -32, -37, -38 and -50 against V4-HI-41/42/51 and D2. | Default *propose* via *effective (policy default)*. Item, multi-row and batch acceptance. Widening bounded by W-a…j. Only host-held constraint carriage satisfies R2-12; App-assured is unavailable in this increment. Local and host evidence are labeled separately. |
| VC-007 | VER-007 / AC-007 | Trace V-01…V-14, V-21 and V-25 to their bases, P-01…P-06 to DECISION-1, their derivations or INTEGRATION, and V-20…V-27 to their owners. | Every value has a basis and a standing label. D2/D3 are not over-credited. The DECISION-2 D6 deferral is carried as `UNRESOLVED{D6}`. |
| VC-008 | VER-008 / AC-008 | Compare §11 with SoW CLM-002…005 and REQ-007. Run FX-28. Read F-10. | Every excluded act is assigned to its owner. No host, adoption or act claim. |
| VC-009 | VER-009 / AC-009 | Reconcile FX-01…53 with REQ-002…006 and the matrix. When a candidate exists, run the fixtures and retain their IDs, the candidate identity, the results and the limits. | Complete coverage. Held, AWAITING INPUT, D6-held, INTEGRATION-rule results and missing host evidence are reported separately from passes. No results at v0.5. |

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
