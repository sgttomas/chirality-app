# I2 ROLE lifecycle — first immutable source/API seam

2026-10-05. TASK `/root/group_a_execution/workflow_role_production`, parent
WORKING_ITEMS `/root/group_a_execution`, native descendant, no delegation;
supplied model6.1/medium. Own new role_lifecycle.rs, tests/role_lifecycle.rs and
this record only. No maintained fixtures needed. Existing role_supply/probe/
hosting/lib/App/Design/schema/Cargo files are not changed by this task. No live
supplier/model/auth/network/download/Git operation. Fresh independent review
precedes manager integration.

## Produced behaviour

- PreparedStart freezes actual common/role/composed buffers once, validating
  part counts, role/path/kind/framing, byte ranges, exact-byte/default identities
  and original source state. It holds home, full appSession/home/spawnCounter,
  actual supplier request identity/ref and supply reference before dispatch.
- Creation of a RoleBinding consumes matching generation/request/native-start
  observation **and actual sent thread/start envelope** whose developer text
  exactly equals the frozen composition. Substitute/foreign/malformed/failed
  observations refuse binding; they cannot populate the selector.
- Private immutable original buffers are not loaded from files or deserialized.
  Current-store comparisons produce per-source future-conversation notices
  only; native agentRole hints never silently change the App-selected role.
  Native observations retain metadata/source reports, not turns, transcript,
  supplier base, user config/auth or generated model prompt text.
- Binding prepares thread/resume or thread/fork with exact threadId-only params,
  no new guidance/model/policy/config override. Dispatcher-provided actual sent
  frame must match that metadata packet before accepting a native response.
  Resume retains the original binding after native same-thread verification.
  Fork additionally requires observed distinct native thread/forkedFromId and
  preserves the source's original guidance; its origin is inherited-fork/source
  supply relation, not newly supplied/adopted guidance.
- In-memory RoleBindings lookup is home+thread-bound, append-only per key and
  refuses replacement/reselection. Missing/foreign entries are Unknown.
  imported_role deliberately remains Unknown even for complete byte-perfect,
  schema-valid serialized copies; hashes/schema validity prove no historical
  App/native boundary provenance. No-role is known None, distinct from Unknown.

All serialization here is an internal evidence view, not a new adopted RS
schema/canonical method, durable registration or human act. Identity designation
is existing reviewed `chirality.app.exact-bytes.sha256/v1`; no algorithm choice
or native/host identity is invented.

## Native-history and Host integration contract

Coordinated directly with TASK `/root/group_a_execution/runtime_core_production`.
NativeHistory owns transient metadata/pages/goal/child views. It does not infer
App roles and exposes home()/generation()/selected_thread()/selection_epoch().
HistoryQuery id is **local correlation, not native RPC id**; factory and private
selection/stream epochs guard its views. Its continue_query emits threadId-only
resume; resumed_thread is a same-home/generation/thread native candidate, never
active Host registration. Manager may render RoleBindings lookup beside that
native view; no role is deserialized into NativeHistory.

Shared dispatcher must supply actual Host sent-frame/request IDs/ref and full
generation-correlated native responses, not a reconstructed purported sent
frame or local HistoryQuery id. Authentic boundary provenance and actual
write-result/current-generation enforcement stay with Host; this Rust type does
not cryptographically establish them. Binding source ref and native history
selection are kept separate. Source binding chains remain in the in-memory
owner when fork relations are used; serialized pointers cannot reconstruct
missing original supply provenance. Actual Host/history/lib/UI wiring was not
performed and requires integration after this bounded source review.

## Verification

Manager granted exclusive Cargo slot after prior lane release. Command from
app/src-tauri:

```sh
CARGO_HOME=/private/tmp/chirality-app-v4-group-a-cargo-home CHIRALITY_SKIP_CODEX=1 cargo test --offline --locked --test role_lifecycle
```

Actual session19899, exit0: **7 passed, 0 failed, 0 ignored**, final test time0.00s.
Supplier explicitly skipped; this source-inclusion target does no native/model
execution. It compiles the actual new module against the unchanged production
role_supply.rs. Warnings are unused imported role_supply helpers in this bounded
target, not new runtime findings. Cargo slot released promptly for I5 trace.

Cases: real temp-file edits leave original evidence/role unchanged and mark
future-only notices; missing current files remain notices; full generation/
home/request/result negatives; incomplete/mixed/tampered/default-source refusal;
exact resume with native role hints ignored; fork actual source relation and
original-buffer preservation; schema-shaped imported/tampered/missing objects
stay Unknown; duplicate changed-role insertion refuses; substituted outbound
guidance and guidance override on resume refuse. Invented native frames are
consumer oracles, not supplier witnesses or performed human acts.

`rustfmt --edition2021` completed on the two owned files. No broader Rust or UI
build, supplier lifetime test, model adoption or qualification claimed.

## Exact remaining requirement before persistence/wiring

This is deliberately an **in-memory App-observed seam**, not trusted cold replay.
An App restart loses trusted role lookup unless a future owning contribution
establishes original-source custody and native/home/thread reconciliation.
Readable/permission-owned/schema-valid/hash-valid JSON alone is insufficient.
Manager/storage/native owners must choose that bounded allocation and actual
provenance/reconciliation method before admitting serialized bindings as current
role state. Original App-owned instruction buffers are permitted to retain;
human-act seals, native transcripts and supplier base caches are separate and
are neither required nor fabricated here. This obligation is still open, not
satisfied by this return or removed from whole ROLE completion.

Further required receiving work: active Host/history registration, readonly UI
original-role display/future notice, fixed-role continuation as a fresh
conversation, schema-complete source/supply records and native/real lifecycle
observations. Other/no-role native carriage, child carrier/availability/limits,
actual provider/model adoption and supplier/product qualification remain within
their existing independently stated obligations. No new human checkpoint or
scope narrowing is introduced.

## Frozen candidate hashes

| Owned output | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/role_lifecycle.rs` | `77e2d02ed9867dde6c70b75fc24d27f31e1ba84bed10f5a00c867205c0af2d8f` |
| `projects/chirality-app-v4/app/src-tauri/tests/role_lifecycle.rs` | `7a7c0dfbd4dc00765eae11ec2d6baf8ffb355cdd4212ace74223f3750477c9d2` |

## Actual read source identities

Root/TASK/LOOP supplied basis retained in prior I2 evidence. This turn read selected ROLE carrier/lifetime/source/verification sections, current pin note, production composition and native-history/recovery generation interfaces; prior named method/supplier review remains selected evidence. No other role instructions activated.

| Source | SHA-256 |
|---|---|
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/ROLE_SUPPLY.md` | `b279a23a5c8d8b2170618a062b3a5ccc3ea07a1cecdfcec7c61d0320f6559ba9` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/ROLE_PIN_0.160.0.md` | `3ac68a93ec5d9a4005253295c2494cd57ff4b33039458028e41b18fab1539ce6` |
| `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-04_Additive role selection and supply/Design/role-supply-record.schema.json` | `eaa6e682aa6077f8ab89858e3f52d0e91d7117b5c03ea4c68c72ec0d95c5f639` |
| `projects/chirality-app-v4/app/src-tauri/src/role_supply.rs` | `f8ba64a1dd35a8b2652212a84481c80d6314a827b76968f9dbb6cc15cd397069` |
| `projects/chirality-app-v4/app/src-tauri/src/native_history.rs` | `c65fd6598d0d37cbeb175cb11c8f79b02ca5f3598c021115d524e2600910a9fe` |
| `projects/chirality-app-v4/app/src-tauri/src/recovery.rs` | `4aefbdc26f4956a50788a21089c650ce80a4509727105485ce91d036396d49d0` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-ROLE-PIN-0160.md` | `f495d512b8c88a61c0b19495c6368abc2de084d18c949b8214c29c1cefab1226` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V0-ROLE-SUPPLIER-CAPTURE.md` | `bfe6b2d011b85c4691d18d3e4a285a51f2bb123c1059ec6084950e81a77e344f` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-CONTENT-IDENTITY.md` | `453746e687c3cd6488eb8c57b50a19a5525b3ce0b7270cbe5f1b8c577d32b862` |

## Correlated native-result shape repair successor

Manager relayed an independent exact original-source reproduction at `role_lifecycle.rs` SHA256 `77e2d02ed9867dde6c70b75fc24d27f31e1ba84bed10f5a00c867205c0af2d8f`: **0/2 independent criteria passed**. A minimal start response without required native model/modelProvider/cwd/approvalPolicy/approvalsReviewer/sandbox was accepted as AppObserved; malformed object-valued agentRole was cached. Original producer7/7 and source/test hashes above remain historical coverage, not evidence that these defects were absent. This successor repairs the actual gates, not the independent oracles.

The module compiles all complete pinned0.160 Start/Resume/ForkParams and Response targets from the **unchanged existing embedded supplier root**, using the same Draft7/offline/target-ref approach as NativeHistory; no reduced hand validator/schema shape changes/external retrieval/fallback. Setup failure refuses binding. After schema validation, serde parses selected native thread/source/role-hint/destination fields into typed metadata; preview/turn/transcript/base/config bodies are not retained. Other selected native policy/sandbox facts remain schema-validated actual returned settings.

Positive native fixtures now use complete real protocol shapes. Original malformed/minimal negatives remain alongside individual mandatory-root/thread-field omissions and incomplete resume/fork results. The tests still verify original byte snapshots, imports Unknown, native correlation/home/full generation, future-only edits, fixed role, exact metadata requests and inherited source relations.

Role-owned fragment versus owner settings is explicit: full outgoing params are validated, exact App developer text is matched, and other native setting keys/base/config presence plus actual returned native settings are reported. Caller-owned fields are not silently dropped from the account or vetoed; raw base/config text is deliberately not cached. The account states `nativeBaseAndConfigurationPreservation: not-established-by-role-binding`. Exact developer text and schema validity establish neither untouched native base/config nor actual Host/authenticity/provider adoption. Authentic sent/received provenance/current-generation/write-result ownership remains the shared dispatcher/Host requirement. Imported complete/schema-valid binding files remain Unknown.

Same focused command, unchanged root lock/dependencies, actual session88458, exit0: **9 passed, 0 failed, 0 ignored**, time0.14s. Cargo slot released to history repair. No actual supplier/model/auth/network, shared source/schema/Design/Cargo/Git change. Exact completion output:

```text
running 9 tests
test malformed_or_mixed_source_binding_refuses_before_native_start ... ok
test substituted_outbound_guidance_or_override_on_resume_cannot_bind ... ok
test exact_resume_packet_has_no_new_role_guidance_destination_or_policy ... ok
test full_generation_and_request_correlation_are_not_name_matching ... ok
test fork_inherits_only_original_app_binding_and_native_source_relation ... ok
test native_owner_settings_are_reported_without_false_base_preservation_or_config_veto ... ok
test imported_files_missing_and_foreign_bindings_remain_unknown ... ok
test original_buffers_survive_real_file_edits_and_future_notice_only ... ok
test minimal_or_malformed_native_results_do_not_establish_app_role ... ok

test result: ok. 9 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.14s
```

Successor hashes (old candidate retained above):

| File | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/role_lifecycle.rs` | `549fe28fe8155217ac961a29bf3dfe43b9103de12ccad585f609894e411bf7b3` |
| `projects/chirality-app-v4/app/src-tauri/tests/role_lifecycle.rs` | `9c0fb4e5ad4ff4e2fed66ef4dea14edf23e32a21f9501af3c965860317f32885` |
| `projects/chirality-app-v4/app/src-tauri/resources/supplier/0.160.0/codex_app_server_protocol.schemas.json` | `7243ba241962af92ca60581f1a81808ebda4212a800f8b205f54703bcfd508c5` |

Fresh same-reviewer shape/boundary backcheck remains required before fan-in. Persistence/native reconciliation and public Host/history/UI integration remain unresolved owning contributions exactly as above.
