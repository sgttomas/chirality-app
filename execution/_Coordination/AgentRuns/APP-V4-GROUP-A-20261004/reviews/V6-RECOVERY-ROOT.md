# V6 Recovery Root consumer — independent review

2026-10-05. **Initial source verdict: no actionable findings; source suitable for controlled verification. Implementation fan-in verdict pending frozen executed backcheck.**

TASK `/root/group_a_execution_astra/recovery_root_review`, parent `/root/group_a_execution_astra`, delegated-harness-native descendant; supplied Astra/low; no descendants. Applied project `software-code-review`. Sole write is this report. No source edits, Cargo/compiler/tests, Git, supplier/native process, authentication, network, downloads or credentials used during this source review. Host permissions and parent's test hold enforced the boundary. Author's later compilation message is reported evidence, not my execution.

## Candidate and scope

Private `/private/tmp/chirality-recovery-root-01hhku68/app`; original patch SHA-256 `96c1373cf42e0a9f6c28023b4382d10adebdbf86eb7ebcf7900dbfdfecd5e714`; original author report SHA-256 `2f4704fac48341ebbc4473579658d7fab22cbb41056bcb45d6fd80195b07632d`. Independently read and hashed patch, freeze and complete source manifest: every listed source hash matches; changed set is exactly six paths. hosting.rs starts with the byte-exact reviewed baseline and only adds the authorized cfg(test) module inclusion. No repository software-workflow profile exists; scope checked directly. Maintained-source integration is not performed here.

## Findings and source reasoning

No confirmed blocking or non-blocking defect in the bounded consumer diff.

- `lib.rs:110–115` retains the actual active HomeSession Arc under a short Root try-lock. The guard ends before Host observation. It rejects busy Root and checks the original Arc against active selection after reading. It introduces no runtime/history/ledger lock or operational source lookup.
- `recovery_root_view.rs:11–29` checks selected home class and complete current generation, validates non-null generation, and checks complete generation plus App session after the owner-issued cached custody projection. Null stays null before supplier startup. The HomeSession owns a stable Host Arc; HomeRouter entries are retained and key binding refuses replacement. A historical pointer is never admitted as current execution authority.
- `Host::recovery_custody` reads Inner and pending-queue facts and uses the already cached recovery snapshot. Its view constructor clones metadata; it does not append, flush, load native History, send, or access the writer/ledger/runtime/history locks. Root holds no guard across this work. Separate snapshot calls are bounded by generation/session checks; no atomic current-execution claim is made.
- The panel keeps persisted rows, pending count, live retained facts and restart-derived events separate. It shows original execution generation/index, later metadata index/session, original per-item associations and unknown legacy correlation. It neither infers turnId from liveTurn nor transforms item-only history into restart live work. Original cross-home ledger rows remain visibly historical; current queue count remains source-specific.
- `App.tsx` keys the panel by selected class and full generation. A key change discards the old component's state; its pending promise can only update that old component. The response is also checked against the request's selected class/generation. No refresh effect/timer is introduced; refresh is person-requested. Retained successful data following a same-source read error remains labelled by its original read time and source, alongside the error.
- Native History/Continue implementation and command routes remain unchanged. The panel offers no resume/continue or human-act control. Its text separates pointer metadata from native content, operation authority and current liveness. Ledger 0.3/older-reader preservation limits accompany the consumer.

## Verification limits and next check

Inspected all four written Rust controls and the three synthetic actual-component controls. The Rust vectors cover actual Root helper to Host producer/queue/ledger/reopen, missing index, foreign source/busy Root and protected lock ownership, and mixed known/legacy pointers with separate later metadata provenance. The last vector explicitly constructs metadata and is not a supplier witness. The panel harness exercises explicit-read/foreign-home refusal/provenance labels; it is synthetic state/render inspection and does not execute actual React unmount/reconciliation or browser/native rendering. Keyed lifetime behavior is source-reviewed here.

Author initially reported parser, TypeScript, Vite and three panel controls passing. Author subsequently reports first Rust compile/four connected controls passed on unchanged bytes. Neither report substitutes for this reviewer's pending frozen executed backcheck. Prior core V6R2 READY (43 author/23 independent controls) is bounded antecedent evidence; it does not test this consumer. Native startup/loss/quit/relaunch, UI/accessibility, human recovery choices, external PI-6 association and complete REC qualification remain outside this review. Manager must retain their existing owners and required witnesses.

## Consultation provenance

Hashes identify actual files consulted, not whole-document reading. Root AGENTS was supplied in the task and checked from repository. TASK, Loop, manual entry/headings and Field Book were read; Group A graph and REC §§7/7.2 were selectively read, with source joins and core V6R2 review. No other role or reusable workflow was selected.

- `AGENTS.md`: `f96feb19d297c74e10048c506805b2fe3622c50cfefd6078f599724556113977`
- `agents/AGENT_TASK.md`: `1a13a5b00b3ce01ff8519efe6b46bcbe0cd6a5b7985e24282fa7efa2c57c8fb7`
- `projects/chirality-app-v4/loop/LOOP_INIT.md`: `c2e88f81439ed03578fee13fd7563082fefdfe11096d9134a59531eba3b985bd`
- `.agents/skills/software-code-review/SKILL.md`: `ee085d589c44f912d11a59eead8edac214f0343761d26b0d33e886a979888bca`
- `docs/alignment-manual/README.md`: `5eee30d902c57a251bf885f91bfa0481a7834ec6945c3382baf15d2e2980c63d`
- `docs/alignment-manual/CHIRALITY_AGENT_USER_MANUAL_v3.md`: `2535efe547f2368e06d965d189efc47c7c46f28c2d6fd4777b0b8cece9003fa7`
- `docs/alignment-manual/Project_Management_for_Human_Agent_Teams_Field_Book_v1.md`: `02d53a3966220001318aacf3f46e1b63b8695a098c81b20f4e3e1531b93024d3`
- `projects/chirality-app-v4/execution/_Coordination/WorkGraphs/APP-V4-GROUP-A-20261004/WORK_GRAPH.md`: `737e1934a0e7a309e5a872fa09283e036b872bc7069b757ad83d988a9c9027d2`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-02_Durable execution and request recovery/Design/EXECUTION_AND_RECOVERY.md`: `088cb70f9124e09845b27dad785009fca56674e276f11dd32ae650622bdb1856`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V6-RECOVERY-CUSTODY-CORE.md`: `c5a47cde2a1df346767459a23129e41ce81928b59a54dfcfaa65273535c511db`

Private frozen artifacts:

- `/private/tmp/chirality-recovery-root-01hhku68/freeze.json`: `2551ae8a7312c5cbd55ae28b3721477fe36592688e5e173f227c4cd8656d9d22`
- `/private/tmp/chirality-recovery-root-01hhku68/source-manifest.json`: `5dc6e30bc4757ce5e3168af94b81c8325e0c3f570bbac90f73ff4dccd96a1e44`
- `/private/tmp/chirality-recovery-root-01hhku68/baseline-manifest.json`: `f6c9019dd9846a122a109f715f7b77a4789ac6532b237fc4c715c318b180e93a`
- `/private/tmp/chirality-recovery-root-01hhku68/validation/panel-controls.mjs`: `8227def7ac4dc5cb8df4bc8f9d69232d0c979cb567adca1a03f0f360cd3df52b`
- `src-tauri/src/hosting.rs`: `2e9273784e6acc96b3898ec5981dee0f00689757aadabe3c8d771933066021d8`
- `src-tauri/src/lib.rs`: `7718c9c0b312343e31a67635189b9f9ddab3c6dfd364f2fe15a5dc02ebdb9939`
- `src-tauri/src/recovery_root_tests.rs`: `cf80bf2629ebac12dd9255f10db0e2fd14ac39507626baee8de0d7f94a3723f6`
- `src-tauri/src/recovery_root_view.rs`: `5153a23003df25a2bb514b4f89153d08124d3e09c36c4c51c992c6913e482719`
- `src/App.tsx`: `af88bb05e53c17742dea47ef525d71826f934be466039858d53aad403ea3e70b`
- `src/RecoveryCustodyPanel.tsx`: `0e18949c9689d19ff84d04bd156874ff0ed854a727effbedd9b5f5efa4290557`

## Independent frozen executable backcheck

2026-10-05. Author released the immutable executable and process lane after 56 selected author passes, with original source unchanged and no Rust repair. Independently verified CHECKED.json (`c6be1625ea8674449bc0fb3c84e1e2f694d4cae3bc56cf74931f5727fefb0944`), all 267 frozen checked/app source hashes, all eight author source/log bindings, and binary SHA-256 `203574e3c1d236d5b463d59fcfb5be2a78069ada9cf65ee5b99caa847f80b74e`.

Executed the author-built copied binary `/private/tmp/chirality-recovery-root-01hhku68/validation/checked-lib-tests` with each filter below and `--test-threads=1`, cwd frozen `checked/app/src-tauri`, `CHIRALITY_SKIP_CODEX=1` and the four named supplier/workspace environment overrides removed. No Cargo, shared target, rebuild or supplier process. Binary hash unchanged afterward. Original four Root vectors and all original core regression source bodies are unchanged from preparation.

```text
$ checked-lib-tests recovery_root_tests --test-threads=1

running 4 tests
test hosting::recovery_root_tests::recovery_root_actual_source_queue_durable_reopen_remains_pointer_only ... ok
test hosting::recovery_root_tests::recovery_root_foreign_home_generation_and_busy_root_cannot_retarget ... ok
test hosting::recovery_root_tests::recovery_root_missing_project_index_stays_memory_only_and_read_never_flushes ... ok
test hosting::recovery_root_tests::recovery_root_reopen_preserves_legacy_unknown_and_distinct_metadata_source ... ok

test result: ok. 4 passed; 0 failed; 0 ignored; 0 measured; 254 filtered out; finished in 0.13s


(exit 0, 0.84s wall time)
$ checked-lib-tests execution_custody_tests --test-threads=1

running 15 tests
test hosting::execution_custody_tests::append_failure_keeps_original_execution_rows_for_later_flush ... ok
test hosting::execution_custody_tests::cold03_exact_adopted_schema_examples_and_old_reader_boundary ... ok
test hosting::execution_custody_tests::cold03_item_completion_and_terminal_settle_only_matching_turn_tuples ... ok
test hosting::execution_custody_tests::cold03_item_only_competing_turns_and_same_labels_retain_exact_associations ... ok
test hosting::execution_custody_tests::cold03_legacy_unknown_stays_unknown_beside_live_turn_without_migration ... ok
test hosting::execution_custody_tests::delayed_older_generation_row_cannot_replace_newer_cold_observation ... ok
test hosting::execution_custody_tests::missing_index_stays_hot_only_and_status_has_no_write_effect ... ok
test hosting::execution_custody_tests::queued_facts_stay_distinct_and_context_tags_survive ... ok
test hosting::execution_custody_tests::rc1_item_only_and_competing_turn_pointers_survive_reopen_without_live_inference ... ok
test hosting::execution_custody_tests::rc3_terminal_method_with_active_status_never_revives_custody ... ok
test hosting::execution_custody_tests::separate_home_equal_labels_and_fork_provenance_remain_separate ... ok
test hosting::execution_custody_tests::source_quit_loss_and_clean_end_require_actual_live_pointer ... ok
test hosting::execution_custody_tests::source_to_durable_loss_and_restart_without_ui_poll ... ok
test hosting::execution_custody_tests::terminal_completion_and_foreign_receipts_do_not_revive_custody ... ok
test hosting::execution_custody_tests::unavailable_and_legacy_generation_projection_retains_limits_without_actions ... ok

test result: ok. 15 passed; 0 failed; 0 ignored; 0 measured; 243 filtered out; finished in 3.56s


(exit 0, 3.57s wall time)
$ checked-lib-tests app_custody --test-threads=1

running 7 tests
test hosting::conversation_transport_tests::app_custody_context_refresh_preserves_both_home_indexes_and_shared_hot_claims ... ok
test hosting::conversation_transport_tests::app_custody_named_cr7_environment_removal_uses_only_explicit_canaries ... ok
test hosting::conversation_transport_tests::app_custody_one_session_shared_actual_ledger_equal_request_ids_and_recreated_counter ... ok
test hosting::conversation_transport_tests::app_custody_retired_host_queue_survives_actual_drop_recreation_flush_and_end ... ok
test hosting::conversation_transport_tests::app_custody_retired_queue_io_failure_keeps_actual_facts_and_error_without_end_replay ... ok
test hosting::conversation_transport_tests::app_custody_shared_paused_writer_retains_source_order_and_actual_stop ... ok
test hosting::conversation_transport_tests::app_custody_unavailable_original_ledger_no_relocation_and_no_json_session_adoption ... ok

test result: ok. 7 passed; 0 failed; 0 ignored; 0 measured; 251 filtered out; finished in 1.01s


(exit 0, 1.02s wall time)
$ checked-lib-tests recovery_custody_rc2 --test-threads=1

running 1 test
test hosting::conversation_transport_tests::recovery_custody_rc2_cross_session_actual_tag_writer_keeps_new_metadata ... ok

test result: ok. 1 passed; 0 failed; 0 ignored; 0 measured; 257 filtered out; finished in 0.12s


(exit 0, 0.13s wall time)
```

**27 distinct independent passes: 4 Root consumer, 15 custody core, 7 App custody, 1 actual RC2 metadata writer.** The remaining 29 author controls are inspected execution evidence, not independent passes. First compile/check succeeded without changing sources or test criteria. These are own-code synthetic fixtures, not native supplier/UI/lifecycle witnesses.

**Final verdict: READY for bounded fan-in of the exact frozen REC Root consumer bytes. No unresolved actionable findings in this diff.** This supersedes only the initial pending-backcheck status. Preserve original-source/pointer limits and ledger 0.3 downgrade restriction. Actual integration against the receiving maintained tree, required propagation and native/UI/relaunch examinations remain manager-owned; this review does not establish complete REC qualification, lifecycle acceptance, release or the Group A gate.

Post-execution check: all 267 source hashes in both author app and frozen checked/app still match the original successor manifest. Parent separately confirmed the immutable-binary scope; no source or shared-target operation was performed.
