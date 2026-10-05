# I3 capture label assessment — 2026-10-05

**Finding:** the general recovery-error branch overstates genuine capture-pending state. Correct that display fact at its producer; keep the storage guard and actual native capture/retry state unchanged.

TASK `/root/group_a_execution/generation_counter_disposition`, parent WORKING_ITEMS `/root/group_a_execution`, bounded read-only reassignment; sole write this report. Current App v4 LOOP re-read; inherited Root/TASK/Field Book/diagnosis context is recorded in I1-GENERATION-COUNTER-DISPOSITION. No code, Cargo, Git, network, credentials, native capture, UI action or delegation was performed for this assessment. Existing Root owner retains App/runtime/native implementation.

## Observed attempt versus source finding

Parent's `probes/NATIVE_APP_SMOKE_ATTEMPT_4.json` records actual native AX text: startup writer continuation, zero new requests, `Capture: AC-8 record pending · owning path contains symlink: /var`, and the same view limit. Supplied empty synthetic workspace used `/var/folders/.../workspace`; physical workspace was `/private/var/folders/.../workspace`. Its sourceCommit is `196914d35bb0c41630331352b2183504a65531ef`, binary SHA-256 `aba8a986afbe68dfe1a826744df47d7357ca20a4693438fedd8e2fe149b72414`. Parent performed inspection and quit only; no human-act capture was attempted. This is an observed misleading label in that bounded setup, not a newly executed successful or failed capture or normal physical-storage/recovery witness.

Current source confirms the causal path:

1. `storage.rs:38–68`: check_path rejects any symlink ancestor; lock checks it before directory creation/open. `/var` alias refusal is the intended owning-path guard. Preserve it; supply an explicitly physical workspace for a separately authorized later UI probe.
2. `act_control.rs:151–155`: new control begins with an empty native_captures map. `recover_pending` at `547–550` acquires that owning capture lock **before** flushing native captures or reading capture/pending files. A path failure therefore returns a top-level error without establishing any capture's pending state. When actual hot captures exist, this error also does not prove that none exist; their custody remains retained.
3. `runtime_session.rs:1301–1326`: continue_decision_writer maps **every top-level recovery Err** to a fabricated captureRecovery row `{state:"AC-8 record pending", writeFailure:error}`. It contains neither capture nor captureId. Separate ordinary recorder failure becomes limits. This promotion causes the wrong state in an empty workspace.
4. `lib.rs:601–615, 714–719` stores startup/explicit-command writer observations; read-only decision_view merely attaches the saved writerStatus. `App.tsx:365–388` reads that writerStatus and renders each non-recorded captureRecovery state verbatim as `Capture: ...`. The UI does not independently invent AC-8; its producer supplies it. Reads do not retry writing and last writer status is historical observation.

## Governing meaning

AAC APP_ACT_CONTROL §3 transition table AX-08/09, AX-12/13/14 (`138–146`) makes AC-8 follow **AC-3 captured / AC-4 declined** when that act's record write fails: capture evidence exists and the writer holds the entry. It is not a generic unavailable-storage state. §4.1 capture step7 (`168`) requires retained capture, entry pending, missing-in-record display and ordered late write with RS FC-1.

RS RECORD_SEMANTICS §14.1 W-0/W-1/W-2 (`1417–1419`) requires reporting write/open failure and pending **entries**, preserving their facts/order; no failed storage check creates an entry or proves an act occurred. §14.1a (`1422–1450`) distinguishes trusted original native capture retry from cold unverified files and matching-record backlink repair. Genuine running-process capture facts/provenance must survive; cold bytes cannot authorize a new human_act or become a native act claim.

Actual genuine AC-8 outputs at `act_control.rs:403–439` originate from a native capture object retained in native_captures, including the capture-publication failure form with captureId and durability not established. Later per-capture flush/recovery results remain associated with original capture facts. `cold_file_limit` (`640–641`) already uses its own unverified-file/replay-held state; it must not be relabeled genuine captured-pending. AC-7 with backlink/delay-evidence pending already has a separate visible detail (`803`; App filter388).

## Smallest correction for the existing Root owner

In **continue_decision_writer's top-level recovery Err branch only**, report a writer/recovery availability limit such as `Capture recovery unavailable: ‹cause›; pending capture status not established by this attempt`. Leave captureRecovery empty for that unknown result, rather than synthesize AC-8. Append this limit and any ordinary recorder error to the existing limits array so the requests Err branch cannot overwrite the recovery cause. Existing App.tsx already renders Writer limit rows; no broad UI redesign or format/schema change is necessary. Optional plain wording can use `Capture recovery unavailable` as the displayed label, without implying no retained captures.

Keep actual Ok(results) per-capture AC-8 rows and their capture/captureId/durability/failure details unchanged, as well as native in-memory custody, ordered retry, original time/record identity, origin hold, backlink/delay distinctions and storage protection. Do not implement a renderer-only `captureId` heuristic that can hide valid backend facts; do not clear genuine pending facts because a separate read or continuation became unavailable. Do not treat newRequestsRecordedNow0 as proof of no prior capture.

## Meaningful checks for that owner (proposed, not executed here)

| Case | Required observed display and preservation |
|---|---|
| Fresh empty control, alias/lock/storage failure | Writer/capture-recovery unavailable with exact safe cause; no AC-8 capture row, no capture/record append; guard remains refused. Both recovery and recorder causes retained if both fail. |
| Real hot native capture retained after publication or record-write failure | Original capture remains genuinely AC-8, including captureId-only/not-durable form; retry preserves original actor/content/time/order, writes at most once and retains required delay account. A later top-level storage failure says recovery unknown and does not discard its real queue. |
| No control / storage read unavailable without a capture | Existing unavailable writer/reader limits remain limits; neither manufacture capture facts nor operate a control. |
| Cold unverified or malformed capture/pending files | Original replay-held/diagnostic rows remain; no native origin promotion or new act append. |
| Stale saved writerStatus on read-only refresh | Display stays explicitly last writer observation; read does not retry or upgrade pending/unknown. A successful subsequent explicit continuation replaces the old generic error with actual results; clean recovery leaves no phantom AC-8. |
| Genuine AC-7 plus backlink or delay evidence pending | Recorded status and its narrower remaining task stay visible; do not regress it to unrecorded AC-8 or hide it. |

**Return:** bounded source defect in writer-status projection, with a scope-preserving correction for the owning Root implementation lane. No actual native capture success/failure or fixed-product witness is claimed. Parent source attempt and setup limitation remain unchanged.

## Exact inspected source seals

Paths below are relative to repository root; current bytes are an assessment basis, not a replacement for the attempt4 binary/source association.

- `projects/chirality-app-v4/loop/LOOP_INIT.md` — `c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/probes/NATIVE_APP_SMOKE_ATTEMPT_4.json` — `40c3834eb9fe9467096a49a0104502f05f805bfa152718b89a3f4f83c276fed6`
- `projects/chirality-app-v4/app/src/App.tsx` — `28a83a3485d9f4f437dc0cceb907475a3855c343b3f32fc67fa731a87733a489`
- `projects/chirality-app-v4/app/src-tauri/src/runtime_session.rs` — `e75f4457be8efb8f0e332b86c5e72b81b4ffced0fca7e4a4095f68cc1aec4d3a`
- `projects/chirality-app-v4/app/src-tauri/src/act_control.rs` — `27beab5887fc9235dc9da09e30c879be54abe8eb3d868ff10c1a4fb16a7e9fac`
- `projects/chirality-app-v4/app/src-tauri/src/storage.rs` — `ae8439c47b86a3225bf46e893bfa1159a2189d0cc8579692d468a78ea9267d77`
- `projects/chirality-app-v4/app/src-tauri/src/lib.rs` — `5707a056e3e331c6d40c123a687c03b72c960b5d77d4887fa386760e355bb3ab`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/APP_ACT_CONTROL.md` — `098875a39b33543adc8ac1d860840e7e841062ea513cbd60a601ca237ceb721b`
- `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RECORD_SEMANTICS.md` — `15266b5078ad1878dae20dc1fa2ef93723d187ce18d5fe780bd1af75c00d5f41`
