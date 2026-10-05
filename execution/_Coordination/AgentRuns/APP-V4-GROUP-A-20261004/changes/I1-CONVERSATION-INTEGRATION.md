# I1 operational text/interrupt App integration — bounded source/test unit

2026-10-05. TASK `/root/group_a_execution/runtime_integration`, parent `/root/group_a_execution`, delegated-harness-native descendant, supplied gpt-6.1-sol/medium, no descendants. Writes: lib.rs/App.tsx/runtime_session.rs, new tests/conversation_integration.rs and this note. No Host/Core/Design/schema/dependency/auth/model/network/Git/instruction writes. Consumes completed V3-I1-LEDGER-STARTUP READY and the original-owner I1-CONVERSATION-R1 terminal-repaired frozen APIs; Core same-reviewer backcheck is manager-owned. No source release is inferred before its actual review return.

## Command and identity boundary

`conversation_send_text(generation, threadId, text)` and `conversation_interrupt(generation, threadId, turnId)` are registered Tauri commands. They accept only the complete owning tuple, already observed native IDs and plain text; no actor/origin/role/base/model/provider/permission/sandbox/collaboration override input. Production closures call only frozen `Host.turn_start_text` / `Host.turn_interrupt` with those same arguments.

The shared real command helpers validate full H5 through the existing generation_ref validator, ready/current tuple and native thread presence in Host.threads. Text is sent unchanged, including Unicode/newlines/leading/trailing whitespace; only empty text refuses. Nothing frames it as a workflow/role amendment or adds attachments/settings. Host repeats authoritative current-generation/native-ID checks inside its scoped sender before the actual pipe write and checks the tuple after response.

Interrupt additionally requires a same-generation/thread/turn native inProgress observation that has not ended and has **no terminalEventObserved marker**. A contradictory inProgress payload with terminalEventObserved=true never grants live eligibility. Existing bound pending-written/acknowledged interrupt records refuse duplicate interruption; native error/unknown state are shown as the core actually records them. Each helper calls its transport operation at most once and never mutates received state or retries.

## Actual App path and outcome display

The conversation panel offers only current-generation native threads and explicitly selected observed live turns. A retained stale selection is shown as unavailable and both controls disable until the person selects a current target. Send text retains draft on actual command error and clears it on native command response. A separate view-refresh error does not turn an already acknowledged text command into a failed send or silently duplicate the draft. The UI dispatches no automatic send/interrupt retry; post-operation refresh asks only host_status, not reserved-act recorder continuation.

An interrupt response is labelled acknowledgment, never turn end, rollback, run end or a human_act. Observed conversationTurns and turnInterruptRequests retain their complete generation/source/receipt/native data and linked client write/wait/outcome record. The literal old “model turn not exercised” message is removed; actual modelTurnEvidence protocol records and the explicit provider/model-not-established standing are shown. Protocol receipt or a mock result is not a provider prediction/qualification claim.

The Core terminal-repair contribution is visible without rewriting native evidence. The UI treats terminalEventObserved independently of payload status, shows a contradictory snapshot limit if such a snapshot reaches it, and renders every returned inconsistencyLimits value verbatim with its full generation/thread/turn namespace. Open full native turn records and the existing all-frame journal preserve raw/unknown fields and the incoming late frame reference. Repaired Core retains its original terminal reading while preserving later conflicting frames and per-observation diagnostics; this consumer supplies no alternative interpretation or restored live state.

This connects the existing explicit model/provider/role entry to ordinary turn text, native activity and request cards, their exact answer path and reviewed App ledger startup. Native notifications supply outcomes; request receipt/settlement remains the existing register's custody. Interrupt acknowledgment declines or answers no waiting request. Attachments, turn steering, Plan controls, history/resume/fork/relaunch, multi-home/full stop/quit/run-tag records, userVerification device proof, protected capture/SEAL-2 and trusted human-act cold replay remain separate unfinished contributions.

## Source reading and exact checks

Read frozen Host API/known-thread/turn lifecycle/scoped sender/snapshot code and I1-CONVERSATION.md including the original missing completed→started case and named successor. NIR §5.1 TO states, §5.2 distinct stop operations and §5.6 text composition, RECOVERY DEF-3 and stop/observer boundaries supplement the retained Root/TASK/v4 LOOP basis. Original Core 7/17 passes did not cover terminal revival; author repaired it, reports 9 conversation/19 Host passes, and froze fbe61326… source for its actual same-reviewer backcheck. This unit claims only its own checks below, not an independent Core test rerun or final Core verdict.

Manager-granted serialized command: `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home cargo test --offline --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml --test conversation_integration --test runtime_integration --test recovery_startup --test external_observation_integration`. Compile/command exit 0; **5/5 conversation** (0.06 s), **10/10 I1** (0.17 s), **6/6 startup** (0.07 s), **4/4 I4** (0.12 s); 0 failed/ignored. Slot released immediately after completion.

Five new tests invoke the actual shared command helpers with explicitly mock transport callbacks: selected full tuple/exact Unicode/text and unchanged response; malformed/scalar/foreign/stale/unloaded/empty refusal without transport; write/wait/native errors returned once, no state mutation and acknowledgment not ending progress; ended/lost/foreign/duplicate and exact contradictory terminal-flag snapshots rejected; stitched ordinary text helper→synthetic native activity/request reducer→view→pointer-only scratch ledger, then separate native interrupted/error observation. The error remains associated with interrupted status. This is typed helper/consumer integration, not actual Tauri command invocation or live model behavior. No supplier process/stock provider/model turn/native window/auth/account/network/download was run. Unique scratch ledger artifacts are removed.

Actual ConversationPanel transient SSR, using explicit synthetic initial hook values and stub native IPC, exits 0: current selection Send/live Interrupt controls, selected native model/provider display, acknowledgment disables repeat without ending progress, terminal contradiction refusal, verbatim Core limit/raw evidence, stale-selection refusal and truthful protocol/model standing. No event handler/native dispatch is exercised by static rendering. Frontend tsc --noEmit and diff-check exit 0. Shared source is frozen after these checks; no further shared edits until actual independent review completion.

## Remaining witness and adoption boundaries

A focused independent complete App glue review and the Core same-reviewer actual return are required before fan-in/release. Physical native entry/typing/interrupt/request-card/ledger journey, native IPC/window effects, provider/model/supplier qualification and filesystem crash/power-loss behavior remain unclaimed. The code is a usable ordinary text/interrupt walking path; this note does not complete full NIR/RECOVERY/Group A, pass a gate, create human acceptance or release a product. Earlier I1/I4/ledger reports/snapshots remain historical and unchanged.

## Frozen conversation consumer

| Project-relative file | SHA-256 |
|---|---|
| `app/src-tauri/src/lib.rs` | `e88f133c46805d9085c496d966d23ff411f70ac303b2f81df1a387b01270e2cd` |
| `app/src-tauri/src/runtime_session.rs` | `c96db03894b242f78a7029b5e04063f639fb02dc13b0c8de59de4b3e9e0e88b9` |
| `app/src/App.tsx` | `3e509ea07de283fc4dfd9ca8ea67d1196457a165bbc3e247990fb02dcec3f672` |
| `app/src-tauri/tests/conversation_integration.rs` | `14710dba817269dd23cd9aa96a8281686944b7636758144d9bcc7162a0242694` |
| `app/src-tauri/tests/runtime_integration.rs` | `18ed6496863eb76cc950c96e162ddb955139a92d776a313c3a9e7a4591195ee2` |
| `app/src-tauri/tests/recovery_startup.rs` | `778562fa9f550014753e6b31b91e05eae2c1b8925ac007fcb3f7a3a100b69a78` |
| `app/src-tauri/tests/external_observation_integration.rs` | `1a59b14714d7be5a200d2848a0b15b71c8f71dea27b330659e2741548221eae8` |

## Named read-source origins

| Repository-relative origin | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` | `fbe61326d878fc92d7301773e38e0781dbaca6f98eb46ba87df06b80b6991510` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I1-CONVERSATION.md` | `95085b185a0758d466b5b42cf6e0ae190f703f709ba26f7c3b83cbe251547081` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V3-I1-LEDGER-STARTUP.md` | `2b7737680ed1a66ff4266cc51156ae6268c9697bfe9da0aa7cbf7bb7b186cf47` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/NATIVE_INTERACTION_RECEIVING.md` | `f9794dcc24d55b813b760daa0f120d9fc53c4893282e907b550e60cdb085ab7a` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/EXECUTION_AND_RECOVERY.md` | `9b443fbc5e7fc617e51e18c4cb8aec7af0d429bc7fefe3e0ec9e52f968aa79d1` |
