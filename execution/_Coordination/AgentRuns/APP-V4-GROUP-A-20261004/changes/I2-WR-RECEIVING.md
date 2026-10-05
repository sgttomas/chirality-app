# I2 WR receiving — first record/framing producer unit

2026-10-05. TASK `/root/group_a_execution/workflow_role_production`, parent WORKING_ITEMS `/root/group_a_execution`, supplied gpt-6.1-sol/medium; no delegation. Own workflow_workspace additions, exact reviewed WR mirror/map, new authorized tests/workflow_receiving.rs and this record. Parser db4ead/20target7b6e, manifest/lock and all shared runtime/Host/lib/App/instructions/Design sources remain frozen. No native/auth/model/credential/network/archive/Git operation.

Reviewed input: V0-WR-TEXT-METHOD-ADOPTION READY package e62fc33c842bcacc191258c5b2b6b2fce1f99fad0e32c9441a5c559402edf58a / bd61f48ca97eba9c7665b31ff7506672f18152d57a20b0ffd361a168750af989 / schema cfd6d3e252b72247d8e1ad0ced3b43b119c5785935002d493407757bd57066e9 / prototype303474582a5192909b7f60e0108009d47efe77fd0477f1ec3c88f00b80fd9c62 / controls c5853f53421fc82cc07728b49b1d406eb3e860c15290367d2797542c57229b24 / fixture1b791948fbae6c68fe7b5f6273a310ccf8723294e5e46df025a44341034a6c2e. Deliberately mirror exactly schema cfd6 and update SOURCE_MAP to that actual canonical reviewed source; prior I2 association is historical, not silently overwritten evidence. The original schema/examples/prototypes are not edited.

## Real producer API and caller contracts

`RunScope` requires separate run, conversation, selected home/full generation, source-root, holding-library label, selection ref and physical revision-store path. Source-root must match original tuple; generation validates full appSession/home/spawnCounter/home identity. Home/source/holding/conversation/run remain distinct. Before preparation, the production Selection.verify_store compares the real holding tree's complete all-file revision to immutable selected content; edited/missing content refuses rather than silently substituting another same-named definition.

`PreparedRunText::start(&Selection,RunScope,folder_label,Option<&OwnerRunEnd>)` emits exact WR-FRAME-1 and schema-complete run_text, preserving body bytes (including CRLF), tuple/holding/source evidence, other-file digests, separately scoped stored-body and composed-text exact-byte identities, start origin/selection relation and owner-end chain. The prepared object exposes readonly text/record/scope and turn_params that places the person's input in a separate native text element. It establishes **preparation only**, not a native active run or supplier/model adoption.

`OwnerRunEnd` is the owning EXEC/RECOVERY callback contract, never an agent-marker/quit/turn-interrupt inference. Matching home/conversation/run/workflow is required for end_notice; successor-end causes use chain line instead of separate notice, and the earlier run cannot equal the new run. End notice is a separate schema-complete text record. These API callback facts and selection/admission refs must be supplied by their real owners; arbitrary caller JSON/schema equality cannot prove a person's selection, A15, registration/shipping, run start/end or source authority. Holding-label/source-root namespace admission remains the library owner's fact; physical bytes equality alone proves neither shipping nor registration.

`compare_observed_text` is deliberately a **pure content comparison**: returns actual observed exact-byte identity and comparison limits, checks methods before values, never value-falls back across differing methods. Same-method full-text equality does not independently compare a different body/package scope; same-method wrapper differences may separately compare exact body bytes. Historical/unknown expected body methods remain incomparable if fallback is needed. It does not emit supply_check or call equality a native verification.

## Actual native receiver prerequisite / no proof DTO

The provisional public ScopedItemsPage data carrier and proposed arbitrary-page supply emitter were removed before runnable freeze. No public/native-provenance DTO or test proof constructor remains. The source-produced run_text can be used later by actual Core/native-history dispatch, but its existence/schema validity cannot establish NativeSupplied/active/A15.

Coordinated with runtime_core_production and runtime_integration. NativeHistory now has a private borrowed accepted_items_observation(query) with query/owner instance/selection epoch/stream revision/stream/page, refusing foreign/stale/error/closed state. That observation alone is still not authenticity because public receive is read-only admission. Original Core owner must mint a private nonserde AcceptedNativeItemsPage only by joining actual written/current-open source-bound HistoryDispatch/RPC/ref/sent query/full generation/exact result with current NativeHistory same accepted query/stream/home/conversation/turn/cursor/page. Immediate transient borrowed consumption plus current-source validity is required; no transcript duplication.

Manager explicitly extended the original owning fence for that genuine capability and cfg(test) joined fixtures; Core mint remains pending independent integration/review. WR cannot emit schema-complete supply_check verified/incomparable states from reconstructed native DTOs. Implement that consumer only after exact private capability returns; source/schema validity is not actual Host/authenticity proof. No fake A15/registration/active grant is substituted while waiting.

## Actual bounded checks

Exclusive manager-granted target: `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home CARGO_NET_OFFLINE=true CHIRALITY_SKIP_CODEX=1 cargo test --offline --locked --test workflow_receiving`, app/src-tauri cwd, session65055, exit0: **5 passed, 0 failed, 0 ignored**, time0.23s. Cargo released immediately. No reflex rerun of frozen parser20 solely for this new disjoint producer. Warnings are source-included unused helper methods and existing unconsumed native-history capability while integration is pending; no broad cleanup/source edits.

The maintained fake release/selection admission is labelled an invented test double through existing typed seam, not an actual shipping manifest/A15. Real private temp holding copies exercise full production byte comparison and changed binary-resource refusal; test-owned copies are cleaned with worker-local guards. Tests exercise exact body/composed scope separation and schema output, original tuple/other-file digest/native turn separation, legacy/unknown method mismatch, body fallback method guard, explicit end/chain matching, bad home/G/source/ref and altered holding bytes. Owner-run end fixtures prove reducer/producer behavior only, not an actual Recovery/native run end.

Exact result:

```text
running 5 tests
test actual_holding_revision_tamper_refuses_preparation_without_silent_rebind ... ok
test home_generation_source_and_identity_omissions_cannot_prepare ... ok
test complete_run_record_retains_source_and_composed_scopes_without_normalization ... ok
test method_incomparability_precedes_values_and_body_fallback ... ok
test chain_and_end_are_explicit_scope_bound_owner_facts_not_text_markers ... ok

test result: ok. 5 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.23s
```

## Frozen current outputs and unchanged parser pins

| File | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/workflow_workspace.rs` | `93eeaf90dc9ed4c1ea2347c7bf026f58ea050bcaf72eb6d103b31aa263c6f97a` |
| `projects/chirality-app-v4/app/src-tauri/tests/workflow_receiving.rs` | `bbe25bb3996cd3728625f3d79e01b0e9e1337c90f30f32df95ebc6c21fa4c370` |
| `projects/chirality-app-v4/app/src-tauri/resources/workflow_role/workspace-registration.schema.json` | `cfd6d3e252b72247d8e1ad0ced3b43b119c5785935002d493407757bd57066e9` |
| `projects/chirality-app-v4/app/src-tauri/resources/workflow_role/SOURCE_MAP.json` | `803df210394c61fa1223ec8efc618431a68028e53ea43294212855dcb61f33f7` |
| `projects/chirality-app-v4/app/src-tauri/src/workflow_declaration.rs` | `db4ead65dc5d4cbc7fbd64fc9ce4c8f4d6112fac2091766658b0a3539341dd07` |
| `projects/chirality-app-v4/app/src-tauri/tests/workflow_role.rs` | `7b6e97e5644c9235d3ca463ee794bb6e0030486e94c47266fea7a46f2f31d6ad` |

First producer/source API unit is ready for fresh independent review. Actual private native page consumer, correlated pagination supply_check, actual run/conversation state ownership, real A15/registered/shipped admission, trusted source/persistence/recovery, public exports and shared App wiring remain required at their original owning points. No whole I2/Group A completion, model adoption, supplier qualification or user acceptance follows.

## TX3 selected-tuple body repair successor

Same reviewer source-included original93ee/bbe reproduction compiled0/run101: matching original markers/full-text and prefix-only wrapper body-equality positives passed, equal value/different method incomparable passed; changing BOTH begin/end name or revision while preserving body returned workflow-bytes-equal and violated selected-tuple scope. Original five-pass result/source association remains above, not rewritten. Actual private repro is retained by the reviewer at /private/tmp/chirality-wr-producer-review-kkvy2ifx/main.rs and outcomes.txt.

Manager resumed a narrow correction to the new PreparedRunText fallback only: exact originally selected workflow name/revision marker lines, first matching begin line/LF and **last** matching end line, are required before body bytes can be compared. Generic legacy framed_body helper is not used as a workaround; no identity/schema/algorithm/parser change. Full source/body/composed identity and method guard semantics remain. Prefix-only changes with valid original markers retain equal body; foreign name/revision, extra marker text and duplicate final end controls cannot identify equal selected body. Same value/different method remains incomparable. Current producer is direct selected-by-person origin only: a future confirmed-proposal caller must use its real owning origin/selection contract, not call this path to fabricate origin.

Preserved exact pre-repair bytes, captured before mutation and independently SHA-verified: /private/tmp/chirality-wr-producer-93ee-before.rs =93eeaf90dc9ed4c1ea2347c7bf026f58ea050bcaf72eb6d103b31aa263c6f97a; /private/tmp/chirality-wr-producer-bbe-before-tests.rs =bbe25bb3996cd3728625f3d79e01b0e9e1337c90f30f32df95ebc6c21fa4c370. Original record11368 remains the predecessor association; this append is explicitly successor evidence.

First attempted repaired target session23648 exited101 BEFORE tests because other-owned attachment_custody.rs inferred unsized Vec<Path> (3 compiler errors). Reported immediately, no other-owner repair/source edit and Cargo released; no WR test failure/pass was claimed then. Core subsequently froze shared inputs after its cargo check --lib passed and manager granted retry. Same offline/locked/skip-stock target session33836: **6 passed, 0 failed, 0 ignored**, time0.22s. Cargo released immediately. No native/auth/model/network/Git operation or parser20 rerun. Warnings remain visible unused helpers/shared source-only capabilities, no unrelated cleanup.

Exact retry completion:

```text
running 6 tests
test actual_holding_revision_tamper_refuses_preparation_without_silent_rebind ... ok
test complete_run_record_retains_source_and_composed_scopes_without_normalization ... ok
test home_generation_source_and_identity_omissions_cannot_prepare ... ok
test method_incomparability_precedes_values_and_body_fallback ... ok
test tx3_body_fallback_requires_original_selected_marker_tuple ... ok
test chain_and_end_are_explicit_scope_bound_owner_facts_not_text_markers ... ok

test result: ok. 6 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.22s
```

Frozen repaired workspace source SHA256`c4bf0c6797f1a906ee67a72045028710aa4ea00ad9384ba476f04fdd224864ca`; focused test SHA256`933279d9fb5794c739603610fb612951562fe190bcc4c7b56d5ecc2754508032`. Mirrorcfd6/SourceMap803d/parserdb4/frozen20target7b6/manifest897d/lockc191 unchanged. Same-reviewer successor backcheck remains required before producer fan-in. Genuine Core private accepted-page supply consumer is still an owning prerequisite, not replaced by this pure comparison correction.

## Legacy public authority API disposition — 2026-10-05

Parent's bounded read found the still-unused legacy `check_run_supply(FnMut -> Value)` returned Verified and used a generic marker body fallback. Earlier wording “no public proof remains” described the newly prepared producer scope too broadly; it did not account for that untouched module-level legacy route. This is not a UI-exploit finding or a reversal of the R1 pure producer's6/6 scope. The source/API route is now deliberately retired before native supply fan-in, not silently treated as authoritative because unused.

Exact predecessor before-bytes captured and hash-verified: /private/tmp/chirality-wr-before-legacy-disposition.rs=c4bf0c6797f1a906ee67a72045028710aa4ea00ad9384ba476f04fdd224864ca; /private/tmp/chirality-wr-before-legacy-disposition-tests.rs=7b6e97e5644c9235d3ca463ee794bb6e0030486e94c47266fea7a46f2f31d6ad. Earlier93ee/bbe5-pass and c4bf/9336-pass associations remain historical. This successor changes two owned module/test files only; no parser grammar, manifest/lock, native/shared/Design/schema/source-map change or actual authentication/model/network/Git operation.

`check_run_supply`, SupplyCheck and SupplyState::Verified are removed. `compare_untrusted_pages` returns UntrustedPageComparison with EqualClaimedText/changed/not-found/unreadable outcomes, explicit untrusted-byte-comparison limits and adoption unknown; it cannot report native Verified/Supplied/A15/active. Legacy body comparison is anchored to exact original expected marker lines/last matching end rather than foreign generic workflow markers. Native supply remains available only through the future genuine Core accepted-page capability consumer, not this data-only API.

`VerifiedRegistrationAct` public fields were an adapter DTO, not a capture-owner capability. That name and DTO-to-RegisteredRevision factory are removed. `RegistrationAdapterClaim` can be compared through RegistrationClaimMatch: immutable reviewed byte/tuple/freshness/subject/review/prior match checks remain, but evidence is explicitly “unverified adapter claim”, selectionEligible=false, with no select/registration authority method. Actual RegisteredRevision has private fields and **no public constructor** until the actual capture-owner closed capability seam exists. No genuine-source constructor or new authority token was invented. Matching fixtures are now matched-but-unverified views; separate labelled synthetic release selections preserve byte/framing/collision tests and establish no actual A15/shipping/release qualification.

All immutable source/method/negative controls remain, including stale/wrong-subject/prior refusal, comparison-only pagination, expected-marker/foreign-marker negatives, descriptor/full-byte body tests, original CommonMark container/raw literal/CRLF/source-range cases, method mismatch and TX3 selected-tuple producer cases. The new regression explicitly proves equality of purported page text and matching claim fields give no authority/native verified state. No production callers existed outside owned tests by actual rg inventory; shared exports/wiring were not modified.

Manager obtained a coherent compile-input freeze; exact command `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home CARGO_NET_OFFLINE=true CHIRALITY_SKIP_CODEX=1 cargo test --offline --locked --test workflow_role --test workflow_receiving`, session93588, exit0: **workflow_role21/21 plus workflow_receiving6/6**, no ignored tests. Cargo released promptly before record polishing so Core could resume its independent guard work. Source-included unused helper/shared capability warnings remain visible. Exact completion output:

```text
     Running tests/workflow_receiving.rs (target/debug/deps/workflow_receiving-454deff12db65585)

running 6 tests
test actual_holding_revision_tamper_refuses_preparation_without_silent_rebind ... ok
test home_generation_source_and_identity_omissions_cannot_prepare ... ok
test complete_run_record_retains_source_and_composed_scopes_without_normalization ... ok
test method_incomparability_precedes_values_and_body_fallback ... ok
test tx3_body_fallback_requires_original_selected_marker_tuple ... ok
test chain_and_end_are_explicit_scope_bound_owner_facts_not_text_markers ... ok

test result: ok. 6 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.24s

     Running tests/workflow_role.rs (target/debug/deps/workflow_role-d77e0b4d9b49e27b)

running 21 tests
test commonmark_container_html_and_eof_contract_controls ... ok
test commonmark_decoded_info_aliases_are_not_reserved_literal_declarations ... ok
test registered_bytes_and_collision_origins_do_not_rebind ... ok
test four_roles_supply_only_at_start_preserve_byte_provenance ... ok
test regression_list_nested_fences_are_not_declarations ... ok
test regression_visual_tab_columns_preserve_root_and_contained_fences ... ok
test descriptor_validates_against_unchanged_design_and_body_is_exact ... ok
test delegation_missing_signal_wins_over_unread_other_signal ... ok
test commonmark_original_source_ranges_and_package_bytes_remain_exact ... ok
test seeded_guidance_missing_symlink_and_modified_bytes_refuse_or_report ... ok
test role_records_validate_and_supply_never_adoption ... ok
test supply_reads_all_pages_and_never_assumes_send_is_verified ... ok
test producer_consumer_unit ... ok
test untrusted_page_bytes_and_adapter_matches_never_grant_authority ... ok
test role_compatibility_is_fixed_and_no_role_is_explicit ... ok
test carriage_declared_empty_absent_unknown_duplicate ... ok
test snapshot_hygiene_and_symlinks_refuse ... ok
test maintained_design_examples_validate_with_element_failures_retained ... ok
test tool_compatibility_missing_optional_unknown_and_guidance ... ok
test regression_missing_or_unknown_necessity_cannot_produce_compatible ... ok
test reviewed_package_identity_matches_independent_vectors_and_all_file_bytes ... ok

test result: ok. 21 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.08s
```

Frozen successor workspace SHA256`e26d659c4edb59a1ed2293fc743c3cbda5b6f5e0258d59018585e3111661a567`; workflow_role21 test SHA256`cdf167c9121827c56137d2557958bc0111044a157041fef5c75fba1ebed1d166`; existing workflow_receiving6 test unchanged SHA256`933279d9fb5794c739603610fb612951562fe190bcc4c7b56d5ecc2754508032`. Fresh affected review is required before integration. Actual registration/capture ownership, native accepted-page supply, imported-source trust, active run state, persistence and public App wiring remain their unchanged full obligations.

## WR-A1 production shipping-constructor boundary successor

Fresh source review WR-A1 (parent-recorded b7a861 association) found that e26's `pub Selection::shipped(Snapshot,WorkflowIdentity)` was still callable in non-test production and could relabel adapter/snapshot data as bundled selection. The previous record called the fixture path synthetic/test-only without a code-enforced cfg boundary. This separate source defect is now dispositioned; no current UI/native exploit or reversal of the pure c4 producer is claimed. Original e26/cdf/933/fffc source/test/record association remains historical.

Actual rg inventory found only six owned test callers and no required production caller. Before mutation exact originals were preserved and SHA-verified: /private/tmp/chirality-wr-e26-shipped-before.rs=e26d659c4edb59a1ed2293fc743c3cbda5b6f5e0258d59018585e3111661a567; /private/tmp/chirality-wr-cdf-shipped-before-tests.rs=cdf167c9121827c56137d2557958bc0111044a157041fef5c75fba1ebed1d166; /private/tmp/chirality-wr-933-shipped-before-receiving.rs=933279d9fb5794c739603610fb612951562fe190bcc4c7b56d5ecc2754508032. Reviewer received those actual paths before disposition.

Minimal repair: constructor is explicitly `#[cfg(test)] pub fn synthetic_shipped`, with all six owned fixture calls renamed. Non-test source inspection verifies that cfg gate immediately guards the only synthetic factory and the old production shipped name is absent. No mirroring test, proof boolean or purported manifest/capture capability was added. RegisteredRevision still has no public DTO constructor. Real shipping/registration selection admission remains unavailable until the corresponding closed owning capability exists; test-only fixture construction proves no actual A15/release authority.

All meaningful immutable byte/method/negative/parser/raw-marker/registration-claim/framing/TX3 controls remain. Parser source db4, schema/method mirrors, Cargo pins and shared sources are not changed. Actual command with manager's stationary Core compile inputs: same offline locked workflow_role/workflow_receiving targets, session44646, exit0, **21+6 passed**, no ignored tests. Cargo released immediately. No native/auth/model/network/source-owner/Git operation. Source-inclusion and unused-capability warnings remain visible, no unrelated cleanup.

Exact completion:

```text
     Running tests/workflow_receiving.rs (target/debug/deps/workflow_receiving-454deff12db65585)

running 6 tests
test actual_holding_revision_tamper_refuses_preparation_without_silent_rebind ... ok
test home_generation_source_and_identity_omissions_cannot_prepare ... ok
test complete_run_record_retains_source_and_composed_scopes_without_normalization ... ok
test method_incomparability_precedes_values_and_body_fallback ... ok
test tx3_body_fallback_requires_original_selected_marker_tuple ... ok
test chain_and_end_are_explicit_scope_bound_owner_facts_not_text_markers ... ok

test result: ok. 6 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.23s

     Running tests/workflow_role.rs (target/debug/deps/workflow_role-d77e0b4d9b49e27b)

running 21 tests
test commonmark_container_html_and_eof_contract_controls ... ok
test commonmark_decoded_info_aliases_are_not_reserved_literal_declarations ... ok
test registered_bytes_and_collision_origins_do_not_rebind ... ok
test four_roles_supply_only_at_start_preserve_byte_provenance ... ok
test regression_list_nested_fences_are_not_declarations ... ok
test regression_visual_tab_columns_preserve_root_and_contained_fences ... ok
test commonmark_original_source_ranges_and_package_bytes_remain_exact ... ok
test delegation_missing_signal_wins_over_unread_other_signal ... ok
test descriptor_validates_against_unchanged_design_and_body_is_exact ... ok
test seeded_guidance_missing_symlink_and_modified_bytes_refuse_or_report ... ok
test role_records_validate_and_supply_never_adoption ... ok
test supply_reads_all_pages_and_never_assumes_send_is_verified ... ok
test producer_consumer_unit ... ok
test carriage_declared_empty_absent_unknown_duplicate ... ok
test untrusted_page_bytes_and_adapter_matches_never_grant_authority ... ok
test role_compatibility_is_fixed_and_no_role_is_explicit ... ok
test snapshot_hygiene_and_symlinks_refuse ... ok
test maintained_design_examples_validate_with_element_failures_retained ... ok
test tool_compatibility_missing_optional_unknown_and_guidance ... ok
test regression_missing_or_unknown_necessity_cannot_produce_compatible ... ok
test reviewed_package_identity_matches_independent_vectors_and_all_file_bytes ... ok

test result: ok. 21 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.09s
```

Frozen successor workspace SHA256`52bc8074d0c65a4478ebc569ea4f71391d24fcb991afd3ac27d7b074ac3bdec6`; workflow_role SHA256`794bb6f169a3aff476ff73c49767b108205fe58632db1bc4563d83a589e02cb3`; workflow_receiving SHA256`84a4b561aa285c5b6a1062d59882ba2d3068f2bc4ad07d1a5860befe656847bc`. Fresh same-reviewer affected boundary backcheck is required before fan-in. Genuine Core native-page supply and real owner admission remain pending; no native proof is created by the new cfg fixture.

