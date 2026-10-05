# I1 recovery later-error RT adoption — 2026-10-05

TASK `/root/group_a_execution/runtime_core_production`, parent `/root/group_a_execution`, native descendant, no delegation. Original owner scope was expanded explicitly from recovery.rs to its native_requests.rs counterpart and focused tests. Writes: those two modules and this note only. hosting.rs/lib/runtime_session/UI/Design/schemas/resources/Cargo/Git remain outside writes. Requested model/effort remains the existing launch; no new model execution, supplier process, network/auth/enrollment/key/verification action or Git operation.

## Reviewed source actually consumed

- `reviews/V0-H-RT-LATE.md`: READY HOSTING source. HOSTING RT14 is successful admitted later protocol-error write; RT09 retains failed-write/unknown. RT15 requires that later marker, actual written evidence, matching full tuple/request and open generation. Receipt RT02/03 semantics are unchanged.
- `reviews/V0-REC-RT-LINK.md`: READY receiving link. RECOVERY §3.5, RQ03 receives RT14 and RT09; RQ09 receives RT15 and existing RT12/13; RQ05 preserves written/no-ack closure; RQ08 is receipt-time only.
- Current HOSTING/RECOVERY source clauses and corrected prototype semantics were read against these reports. This is product propagation of that named pair, not a status-only completion assertion.

## Actual product adoption

`RequestRegister.prepare_error` sets private laterProtocolError only after successfully admitting a known-answerable outstanding request, permitted boundary/nonempty named-rule origin and valid native error. Native payload cannot set that marker; receipt paths do not acquire it. The marker is carried through write/resolve/close, omitted from schema-shaped public records. Failed later error writes now become settle-write-failed (RT09), while receipt error write failures remain errored (RT02/03). A written later error stays errored (RT14).

`resolved` adds acknowledgment only for the existing written answer/decline or the written marked later-error branch (RT15), after full generation/request/thread matching and closed-generation refusal. Its private acknowledgment envelope retains the source generation; schema-shaped public output remains unchanged. Failed/foreign/post-close notifications never promote uncertain writes to acknowledgment; actual supplier-resolution evidence remains separate.

`RecoveryLedger.request_summary` maps the marked written later error to RQ03, failed later write to RQ03 with settle-write-failed/write-failed/not-observed, receipt errors to RQ08, and written marked later-error acknowledgment to RQ09. Written/no-ack closure uses RQ05, unanswered closure RQ04. Source origin/full tagged tuple/request identity remain unchanged. Receiving acknowledgment guards compare actual source tuple and native request/thread, require same-generation request history and reject a new acknowledgment after request/durable closure. Already recorded pre-closure acknowledgment survives later summary/replay without a fabricated new event. No human-act, grant or stronger outcome is created.

A valid native MCP elicitation with turnId:null exposed a source/schema join: RECOVERY's optional pointer turnId is string-only. The schema was not changed; the mapper now omits that absent correlation from the ledger and retains nativeParameters.turnId:null unchanged. It never guesses an identity. Tests explicitly assert both sides. No source/schema shape/ID incompatibility required widening or a new contract; all maintained resources remain unchanged.

## Checks, failures and actual shared state

Approved cache: CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home; cwd app/src-tauri.

| Command | Actual result |
| --- | --- |
| `cargo test --offline --locked --lib recovery` | Final successful run exit0, 10 passed/0 failed/0 ignored |
| `cargo test --offline --locked --lib native_requests` | Exit0, 10 passed/0 failed/0 ignored |
| `cargo test --offline --locked --lib reviewed_later_error_adoption_tests` | Final assertion-strengthened run exit0, 3 passed/0 failed/0 ignored |
| `cargo test --offline --locked --lib later_known_request_rule_error_keeps_native_evidence_and_reports_mapping_gap` | Exit101, 0 passed/1 failed; frozen old Host oracle unwraps nonexistent recoveryPersistenceError at hosting.rs:1046:248 |

The old Host failure is an obsolete missing-mapping expectation after this reviewed source change, not evidence of a remaining product mapping gap or a fabricated fixed claim. hosting.rs was not edited. Its owner must apply the exact oracle/consumer consequence after current Host review before combined checks can be called ready. Parent was informed with the actual failure.

Initial recovery run: 9/10, handmade positive acknowledgment fixture lacked source tuple/native request context now required by the receiver. Retained its RQ09 oracle and enriched the input; actual reducer-connected cases were also added. Next run: 7/10, all three new native-valid MCP cases exposed null-turn ledger schema refusal. Repaired only pointer omission, retaining the schema/criterion, then 10/10 passed. A failed exact-text assertion insertion and a Python quoting typo made no source mutation; corrected insertion then the three affected groups passed with the additional no-guessed-turn assertions. No oracle was relaxed.

A temporary shared I1 lib/runtime_session restoration occurred during coordination. First focused executions preceded the freeze notice; no process remained active. Subsequent compilation waited for the parent's exact restoration confirmation. Final successful checks ran after that confirmation; shared drift is distinct from the real null-correlation failure. No shared source was written by this executor. Cargo slot released after the final affected pass and actual old-oracle reproduction.

New actual reducer→ledger cases cover successful named/boundary later errors, RT15 acknowledgment, foreign full tuple, failed write/resolution uncertainty, no-ack closure, post-close refusal, unchanged receipt families, person/agent/empty-rule/invalid-error refusal and byte-identical receiving refusal for forged foreign/request/post-close/failed-write acknowledgment shapes. Nullable native turn remains unaltered; no ledger turn pointer is minted. Native transport/cards/relaunch, storage qualification and whole-I1 completion remain unclaimed.

## Frozen source identities

| Origin | SHA-256 |
| --- | --- |
| `projects/chirality-app-v4/app/src-tauri/src/native_requests.rs` | `5879e6d034820e5d26c6dea1a4947ab851a39c0598aa675753ab6948e3030dbe` |
| `projects/chirality-app-v4/app/src-tauri/src/recovery.rs` | `4aefbdc26f4956a50788a21089c650ce80a4509727105485ce91d036396d49d0` |
| `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` | `b25b8e937c58e296047f36789b2b53eaa5b6599278a2ef1cc58d12dffdd19343` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V0-H-RT-LATE.md` | `128ad07c1635a5efb663350f14ba593e6188b279b9d9fca14a545c67c0fb2419` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V0-REC-RT-LINK.md` | `2e0ed798040f8a71a9f89c6ba5101f1a819a1db7d8a8716316c6fce46a8d4607` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-01_Stock Codex hosting and supplier contract/Design/HOSTING_BOUNDARY.md` | `47b8f1c6fb01e1f495099b06cd3fc10e95d03c032e8d122ede4378f28e194087` |
| `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/EXECUTION_AND_RECOVERY.md` | `9b443fbc5e7fc617e51e18c4cb8aec7af0d429bc7fefe3e0ec9e52f968aa79d1` |

## Released Host test-only consequence — 2026-10-05

Parent relayed V3-I1-INTEGRATION READY on original frozen production Host b25b8e937c58e296047f36789b2b53eaa5b6599278a2ef1cc58d12dffdd19343 and released only its obsolete missing_custody_mapping test. This successor changes that one test block, not Host production behavior or another test. The actual initial exit101/Option::unwrap failure above remains preserved. This is named source-adoption oracle maintenance, not an unexplained tolerance change or product regression repair.

The renamed `later_known_request_rule_error_records_native_settlement_in_reviewed_rq03` uses an env-cleared /bin/cat echo-only pipe to exercise the actual Host error write. The person protocol-error attempt remains refused. The real mock transport frame, schema-shaped native error/data, full H5 tuple/request ID, named origin and not-observed acknowledgment remain checked. Durable entries assert RQ01→RQ03, errored/written, exact generation/origin, no recovery mapping error, no RQ08 receipt relabel and no human_act. The native-valid nullable turn remains in parameters and yields no guessed ledger turn pointer. No supplier/model/account/network operation occurs.

Command from app/src-tauri: `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home cargo test --offline --locked --lib later_known_request_rule_error_records_native_settlement_in_reviewed_rq03`. **Exit0; 1 passed, 0 failed, 0 ignored**, 0.07s after 1.80s compile. Cargo slot released immediately to the independent reviewer. No broader tests substituted for this consequence.

Before/after byte comparison removed only the released legacy test block from each source and confirmed equality. The entire prefix before the first top-level hosting_identity_tests module also matched exactly. Thus production source and all other tests—including the reviewed generation/guidance checks—remain byte-identical to the prior Host seal. Whole-file hash necessarily changes because the released test changed.

| Seal | SHA-256 |
| --- | --- |
| Whole successor hosting.rs | 71ec04b2a67893e133d94c756a3bada17eedcc783ea82d0ffd9d16f44d1ca97a |
| Byte-identical source outside released test block | c6f18156164bd08aea4460a91e082da446f790e701180e5ed28fcb1390266f70 |
| Byte-identical production prefix | 43fc53d79b07a70374d8c902882d9f53a7e3524f986a49601a102946d1838b59 |
| Released successor test block | 09bb27e154ed118f3a6a2fc50e60718cc5258ccf5dd0226b153740eaa54d6b99 |

The outside-block boundary starts at cfg(test)/missing_custody_mapping_tests and ends immediately before cfg(test)/additive_guidance_transport_tests. Production-prefix boundary ends immediately before cfg(test)/hosting_identity_tests. Native_requests/recovery seals above remain current. This joined adoption candidate is ready for fresh independent affected backcheck; complete recovery/native/App qualification remains unclaimed.
