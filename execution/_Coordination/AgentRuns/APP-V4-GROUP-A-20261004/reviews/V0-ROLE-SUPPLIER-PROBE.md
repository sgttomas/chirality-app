# V0-ROLE-SUPPLIER-PROBE — source-only review

2026-10-05. Original candidate **NOT READY** at script `b19b175b5b5196c0dc429ee16524dac812b3156d63ea6d7b5b1968d407333fe6`, README `72fb2ef100e82461f92cbe83f404a80bda0be0ae821327f93d8045bb10b6199b`. Two blocking findings follow. Script changed during report preparation; successor verdict is held for a frozen return and same-reviewer backcheck. No native/provider/server/model process was executed.

Independent TASK `/root/group_a_execution/contract_reviewer`, native descendant of WORKING_ITEMS `/root/group_a_execution`, supplied Codex gpt-6.1-sol/medium; no substitution/diversity claim or delegation. Applied already-loaded software-code-review. Read full original script/README and exact composition resources; only AST parsing and pure helper/mock checks were run. Only this review written, no probe/product/Design edits, Cargo, network, auth/credentials, model or Git execution.

## Original blocking findings

**RP-1 [P1] Empty native base passes as observable preservation.** Original comparisons() line244 uses bool(base_native) and bool(role_native). Both lists may be [b""]. Pure invented baseline and active payloads with instructions:"", actual exact composition in a developer segment, and both native marker strings produced native_base_observable=true, native_base_byte_equal_to_baseline=true, passed=true. This violates README's actual nonempty supplier-base criterion. Absence of a base field correctly failed, but an empty field is equally no observable base. Require meaningful nonempty text on both sides while preserving exact byte equality; empty/absent-only evidence stays unknown and fails. Add empty instructions and empty system-segment negatives, not an omitted-baseInstructions substitute.

**RP-2 [P1] Leader exit is mistaken for process-group cleanup.** Original NativeRpc.close() lines183–198 signals the group only when the leader wait times out. An already-exited leader or normal successful stdin-close exit leaves any surviving descendants unaffected. Pure fake-process checks patched killpg (no process started) and observed zero group signals for both paths. Reader join/stderr close do not prove group termination. Always establish bounded process-group cleanup/detection independently of leader state, handle vanished groups, report unresolved cleanup/failure, and own initialization failures after spawning. Preserve local raw custody and cleanup/report truth. This is a source defect, not a witnessed real surviving supplier.

## Supported original checks and boundary

AST parse passed. Exact composition is4856 bytes, SHA256 ad560fe79f9552fef1042dd613a0274ca87babd7165bc1ecd0a278a3ada98343; common part0/3858 and HELP_HUMAN3887/969. Source hashes match reviewed common d9233f5af0393e045f0d50fe14b60ede6ec3558da625c1a0deec84fae07afc27 and role11e619e41acad799b90552dda19a3d49c4d3921bcebbce7317254a58d03e04be. This is the permitted independently checked producer-output oracle, not Rust Composition/Host/seeding execution.

Pure helper controls passed a nonempty-equal-base/complete developer composition/both-markers case and failed changed/absent-base cases; RP-1 is the missing empty-base negative. Actual provider roles/positions are retained, source-path reports remain distinct from marker presence, and omitted baseInstructions does not alone prove supplier-base preservation.

Launch source uses fresh resolved mode0700 scratch home/workspace, synthetic native markers, explicit127.0.0.1 capture-only provider, no OpenAI auth, plugins/analytics off and probe-local remote-control disable. No user configuration or auth file is copied/linked, key/token variables are omitted and no login/account method called. Inherited HOME/PATH/language/temp environment remains as shown. This is configuration, not measured/enforced network isolation. Binary pinned development hash does not qualify distribution.

Endpoint never forwards/predicts or reads/stores auth headers; raw JSON and stderr remain private scratch-local. Structural durable report contains hashes, known markers, source-path/thread/turn references and limits, not whole prompts/raw payload. Parent must retain/remove the exact named scratch under its evidence custody and not publish raw bytes. Per-request/capture waits are bounded; unexpected requests encountered by request processing get explicit fixture errors then abort. Actual native request/retry/terminal/cleanup behavior remains parent execution evidence after source repair.

Adoption remains unknown. No other role/no-role, lifetime/resume/fork/child carrier, delegation availability/enforcement, actual model behavior, authenticity or product qualification is claimed. Preserve these limits in repairs. No native or HTTP invocation was performed by author or this reviewer during source verification.

## Candidate advance

Observed script successor at preparation: cf3a26de723329e397b7159cca428d89680da5d84d06df8301a96bdee487c07d; README unchanged. This observation is not a frozen/ready verdict. Manager notified; parent execution should await repaired source backcheck. The original findings and reproduced controls above remain associated with the original b19b candidate.
