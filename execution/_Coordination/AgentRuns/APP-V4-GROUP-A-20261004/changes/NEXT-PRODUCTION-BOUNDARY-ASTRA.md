# Next production boundary — Astra TASK, 2026-10-05

Actual delegated-harness-native child `/root/group_a_execution_astra/next_production_boundary`, parent `/root/group_a_execution_astra`; gpt-6-astra / low as supplied in the brief. Type 2, no delegation. Read-only source inspection; sole write is this return. No Git, Cargo/tests, supplier/native/auth/credential/network action. Candidate association a515b5bf192ed097f0544869331dfb8cfce3db4d is supplied by the parent, not independently re-established with Git. Source fingerprints below bind the bytes actually inspected. No source edits or publication release are proposed here.

## Finding and dispatch recommendation

**One concrete missing production boundary is established: the App-content A4/A6/A7 standing act facility and its consuming presentation.** Dispatch it as the following two sequential bounded assignments after the parent releases the source freeze. This is I1 DEL-01-04 with I3 RS/AS consumption, not a new settings authority. The designs explicitly serve these three kinds; maintained production capture serves A16 and A15 only. This is a code gap, distinct from the later native-person witness. No second independent I1 gap was established by this bounded inspection.

Paths below are relative to `projects/chirality-app-v4`.

### Assignment 1 — App-file act offer/capture/decline core

Requirement: `AAC` lines 96–98 serves A4 “mark checked”, A6 “approve (engineering approval)”, A7 “rely (professional reliance)”; each has decline. Lines 158–169 define the complete App-content sequence, including current identity reread, capture before record, and preserved pending capture. Lines 133–151 define state transitions and prohibit automation, second capture and unpresented capture. SoW REQ-005 line60, AC-005 line69 and VER-005 line82 require independently evidenced checking/approval/reliance and fabrication negatives. SoW AX-005 line95 records the accepted SCA-V4-003 carriage; do not mistake surviving schema “PROPOSED” prose for a new permission checkpoint.

Actual maintained gap: `app/src-tauri/src/act_control.rs:1–19` declares only A16/A15; `:106–111` owns A16 offers plus separate A15 offers; `:166` composes A16, `:329` confirms its selected alternative. A4/A6/A7 currently appear in production Rust only as `ActKind` variants/person-only/checkpoint classification (`act_policy.rs:50–84`). Their offer/capture schema branches already exist (`schemas/aac.offer.schema.json:331,357,383`; capture kinds `schemas/aac.capture-evidence.schema.json:146–148`). No general file-act producer or declined-act producer is supplied.

Owner fence: AAC owner may add a dedicated file-act submodule and tests, and make bounded additions to `act_control.rs` for owning custody/retry. Keep `act_control_a15.rs`, `a15_native.rs`, WR transaction, Host/access, schemas and Design unchanged unless an exact conflict is independently demonstrated and routed. Reuse existing identity/path/record facilities (`util.rs:21`, `storage.rs:38`, `records.rs:85,123,143`) after checking their actual containment and race properties; do not add a renderer DTO that can mint an act. Host-owned file selection/identity must supply the subject. Explicit actor statement for A7 is a claim with identity/professional status unverified, not certification.

Consumer contract to return: immutable host-composed offer/reference, native presentation snapshot, native act/decline/dismiss continuation with identity/actor recheck, once-only capture, direct-capture human_act or act_declined, and existing ordered pending/retry behavior. Standing acts must work with no request/arrival; optional actual references are not invented. Preserve A15 once-only receipt and A16 original behavior. Use a private custody boundary modeled on the current hot A15 pattern where useful; a caller's `source=native` string alone is not production evidence.

Meaningful offline checks: unchanged bytes produce exact A4/A6/A7 kind/wording/actor/recorder/identity fields; explicit decline yields act_declined and dismissal yields neither; changed/removed/aliased subject and changed actor refuse capture; webview/tool/app-rule data, unpresented offers and repeated continuation cannot capture; capture-store failure creates no act, record-write failure retains the original capture for ordered retry without recapture; raw schema claims cannot enter the owning native continuation. Regression checks cover existing A15 and A16 custody/order, not a full suite merely for count. Test native continuations with bounded synthetic adapters and label them synthetic; actual human native confirmation remains Parent-only.

### Assignment 2 — Native control entry and distinct file-act reading

Starts only after assignment1's API and source review are ready. Same AAC/SoW obligations plus AAC AK-a/AK-b lines85–86 (person-opened standing facility) and AI-7 line123 (writer join). Do not implement a checkpoint engine or host act proxy.

Actual consumer gap: `app/src-tauri/src/lib.rs:708–714` exposes only `compose_a16`; `:718–761` is an alternative-based Decide native flow. `app/src/App.tsx:439` opens only “act control (decide)”, `:496` invokes that A16 composer, `:604` renders the decision-package panel, `:620–621` offers Decide. `decision_view.rs:148–149` recognizes A16 for decision semantics, and `:889` explicitly returns a decision-package view. General file acts must not be inserted into this decision-specific path by pretending they are decisions.

Owner fence: sole Root receiver owns `lib.rs`, `App.tsx`, necessary runtime_session joining; a separately owned new file-act read/presentation module and tests may be prepared against a frozen API. Keep the reviewed decision_view A16 semantics, workflow panel/transaction, transport and settings-comparison algorithm intact. Manager must coordinate actual shared writes and compilation.

Missing behavior to supply: explicit person selection of one App file/output, kind, scope/purpose and necessary actor statement; host obtains/binds selected bytes and shows the whole offer in native confirmation with distinct act/decline/dismiss choices. Standalone entry is available without decision packages or arrivals. Display resulting act versus decline, actor versus recorder, identity-not-verified and A7 statement limits, pending/recorded state, and current-content/lapse with source provenance. Reuse existing RS reader/correction mechanisms without elevating cold readable claims into native authority. Wire the standing entry into the applicable existing request/output surfaces; no arrival/event automatically opens it. Return any absent surface explicitly rather than claiming all AK-a routes from one button.

Meaningful offline checks: connected command-to-owning-core-to-record-to-view test for each kind, one decline and dismissal; stale file at native return; unchanged prior act remains distinct from unrelated acceptance/execution; current content change produces truthful lapse/comparison; missing/unverified evidence and agent approval text never create human act/professional standing; read performs no writes; no request settlement or automatic popup; existing workflow/A16 frontend routing still builds. Native UI/person act and real accessibility/control behavior require a separately scoped Parent witness on the final artifact.

## Remainder corrections and held inputs

- Older “full logout/shared-home/session closure needs consuming path” wording cannot justify new work: `runtime_session.rs:2539–2609` already assesses exact home/work, confirms, rechecks, performs scoped logout, invalidates the affected selection and rereads the same source; `lib.rs:188–193` invokes native confirmation. `lib.rs:888–897` stops each owned home and records App session end on quit. Actual OS/auth/quit/relaunch behavior remains witness work; this inspection does not certify every lifecycle edge.
- Do not dispatch App A12/A13 or general grant authority: AAC lines101–104 explicitly offer no App setting, no App-content proposal, and no App-owned external interface. Host grant/control reports and settings-at-application are host inputs; the existing settings comparison is data-only. App Codex settings stay the user's own. Missing host settings journeys cannot be filled by fabricating local grants.
- ROLE child supply remains at the named CI15 ROLE/ACCESS/current supplier fit disposition, not ready local implementation on a guessed catalog. Native workflow/A15/supply, Continue/attachments/auth/provider journeys remain Parent witnesses. Trusted cold replay remains SEAL-2 deferred. None blocks bounded hot file-act development once the manager releases the current candidate freeze.
- Publication stays held for the independently owned failed-write archive diagnosis. These assignments do not reopen valid A15/workflow/settings reviews or satisfy C1/M1/F1, Group A acceptance, or the 90% gate.

## Actual reading custody

Root AGENTS supplied in prompt (and filesystem prefix checked), TASK, Loop, current editions README, Agent User Manual headings through level3, Field Book full; manager handoff, REMAINING_WORK and current graph read selectively (large combined output truncated; no claim of exhaustive graph audit). Targeted AAC/SoW, AS and production source reads support this bounded finding. No workflow or skill body selected; no formal C1 or full eighteen-deliverable inventory.

`AAC` = `execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/APP_ACT_CONTROL.md`.
`SoW` = `execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/ScopeOfWork.md`.

Actual inspected-source SHA-256:

| Origin (repo relative) | SHA-256 |
|---|---|
| `AGENTS.md` | `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977` |
| `agents/AGENT_TASK.md` | `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7` |
| `projects/chirality-app-v4/loop/LOOP_INIT.md` | `c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd` |
| `docs/alignment-manual/README.md` | `5eee30d902c57a251bf885f91bfa0481a7834ec6945c3382baf15d2e2980c63d` |
| `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md` | `2535efe547f2368e06d965d189efc47c7c46f28c2d6fd4777b0b8cece9003fa7` |
| `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md` | `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/APP_ACT_CONTROL.md` | `098875a39b33543adc8ac1d860840e7e841062ea513cbd60a601ca237ceb721b` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/ScopeOfWork.md` | `8434cc47ec28e1397e7dae548183543567f0b5fcfdefaebc0b44bc1f709aacf3` |
| `projects/chirality-app-v4/app/src-tauri/src/act_control.rs` | `32897881a2d7ee4740dd73dcbc3107e60b225df7f028ead3666edf82fa4a82a2` |
| `projects/chirality-app-v4/app/src-tauri/src/act_policy.rs` | `96a6d9d2b9a24ca1dcf17f05e62942fb44c2331531813b0f33c87e877ca7188b` |
| `projects/chirality-app-v4/app/src-tauri/src/lib.rs` | `10ab4c415b0d3a50752a966a4e970e09b58218d815fa8055bed52d413006fc83` |
| `projects/chirality-app-v4/app/src-tauri/src/runtime_session.rs` | `05af3f76da30a02dd425d9de025c623402a2fbdfefcdfc99c5f7201590c041f6` |
| `projects/chirality-app-v4/app/src-tauri/src/decision_view.rs` | `5e8c471a65da20946c8b84d2fbbae26c4f7f7e413f5d90bd61ec3c9ac7b70e79` |
| `projects/chirality-app-v4/app/src/App.tsx` | `681428d443a9020414f0ce76f27d84f8b260714d9e3e32edfc4e79c0f80f1364` |
