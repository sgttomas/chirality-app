# V1 — I1 private OAuth controller review

2026-10-05. **Bounded READY for the pure private controller before Host hooks.** No unresolved blocking finding in the assigned module/test scope. TASK `/root/group_a_execution/contract_reviewer`, parent WORKING_ITEMS `/root/group_a_execution`, delegated-harness-native, gpt-6.1-sol/medium, no delegation or model-diversity claim. This is not actual OAuth/native presentation, Host admission, Root integration or release qualification.

## Exact candidate and basis

| Candidate | SHA-256 |
|---|---|
| app/src-tauri/src/oauth_control.rs | 8096834b5eb9d73f140f585a01bd55535d4d7ec682220ca145daeecddf283060 |
| app/src-tauri/tests/oauth_control.rs | 488f4c47d0667e24b87bf940761f4f678da3b355a3646a39abc8e9dcc20d0327 |
| changes/I1-OAUTH-CONTROL.md | e4dbe2594463d6972394fa270f18a59690a83b9b65dfdcdf63b60989a452f07d |

Independently hashed all three files and read full source/tests/record. Applied software-code-review skill ee085d589c44f912d11a59eead8edac214f0343761d26b0d33e886a979888bca. Source comparison uses adopted ACCESS26659864fd1b720d51bc5bf8038311238e9d6b1775f62a4e08fd2917dba4f9ec §7.1/Q4 and HOST9839cb38310ff55045657e51f7bb7dcfcb2024eb43ec3bab364959e33e5c1e85, packet8efa4401058a74d03cd57177699e463798cff5e78d123e7b8d5f6a7642fb36a4, retained prior independent V0 and actual REC/NIR/NPTD recipient concurrence. No source amendment or new human gate.

## Supported private state and custody

Full generation Value equality, typed RPC equality, original request reference and mode bind start/write/presentation/cancel operations. Event matching uses owning full generation, increasing admitted receipt position and actual private loginId; missing/null/unmatched IDs retain distinct limits without terminal transition. Pins remain the parent's responsibility, not authenticated by their Rust shape or caller JSON. Controller is a private child API, accepts borrowed original validated result/notification subsets and has no public proof/source-pin factory.

AwaitingWrite prevents presentation and cancellation until actual Written. The private early-completion queue retains minimal matching fields, handles before-response/before-write ordering and settles only after actual Written; overflow has an explicit unknown/limit rather than invented pending presentation. Failed/unavailable write does not claim completed write. Same-ID terminal completion clears operational state and revokes presentation; other-ID/null completion does not. Actual terminal facts survive later source loss with availability limits. Teardown/drop revoke outstanding permits and clear controller-owned private state. This clears memory ownership, not supplier state or OS/browser memory.

Dismissal revokes display payload and preserves same live pending cancellation identity. Cancel intent consumes a one-attempt permit holding original ID and shared revocation state; terminal/loss before serialization invalidates it. Unknown cancel cannot become success/retry, while a later admitted matching completion can still establish terminal outcome. Adopted Q4 expressly ends operational pending control for both canceled/notFound, so the controller's common terminal Cancelled phase is compatible; Host/UI must still retain and show actual notFound versus canceled result ("Codex had no pending sign-in") from its safe correlated response, rather than invent that distinction from this phase alone.

Presentation payload/permit/control ID have no Debug/Clone/Serde/raw getters. Controller Debug uses only safe Observation. Start extraction discards unexpected result fields; completion retains success/error-present, never error text. Safe observations carry generation/typedRPC/opaque scoped pointer/enums and explicit original-control redacted/unavailable. No store, sidecar, extra writer, matcher cache, account-read cancellation inference or original-frame representation is introduced. The Host must mint safe scope/reference fields; this controller does not sanitize arbitrary fake parent pin data into authority.

Consuming borrowed native presentation is one-shot. Delivery checks revocation, current source, then revocation again before callback; native callback executes outside controller/Host/pipe locks and receives a revocation lease. Terminal/cancel/loss/drop can revoke the outstanding view. Callback must monitor the lease and clear/close the native display while active; no instantaneous scheduler/erasure guarantee is claimed. Serialization callback similarly only borrows original ID transiently. Neither callback path itself dispatches native requests or chooses account/configuration.

## Verification and required receiving consequences

Owner actual fifteen pure synthetic mock-pin/callback tests PASS is separately attributed to e4dbe record. Reviewer source/contract backcheck confirms meaningful tests for complete fullG/typedRPC/ref/mode mismatches, staging, fast terminal ordering, delivery-time recheck revocation, concurrent modal revocation, dismiss/cancel identity, uncertainty/no retry, stale cancel, null/other IDs, malformed/duplicate receipts, overflow, loss/drop and secret canaries. No suspected defect warranted a duplicate fifteen-test run; no reviewer Cargo/native/auth/home/network execution occurred.

Before actual support, Core Host must construct genuine pins only after written/correlated/schema/mode/source admission, admit original private fields before redacted reflection, own one-at-a-time pending lifecycle, serialize/dispatch original cancel pin atomically against the same live source (not a replacement lookup after confirmation), and retain actual cancel response distinctions. Root's native adapter must implement system-browser/native-modal behavior, lease monitoring and dismissal feedback, with no secret JSON/public snapshot. Those actual hooks, method-sensitive reflection redaction, native callbacks and integrated races need their separate affected review/tests. A FnOnce source check plus an atomic flag is not a proof of final pipe-write authority; Host remains final authority at dispatch. No model/auth/H-key/real-login witness is supplied by these fifteen mocks.

READY only for this frozen module's state/custody/interface before those consumers. No NativeSupplied/A15/actor/grant, account signed-out identity, run end, native policy or whole Group A completion claim. Only this assigned review written; no production/Design/schema/manifest/Git/Cargo/native/authentication/real-home/network/download/delegation operation.
