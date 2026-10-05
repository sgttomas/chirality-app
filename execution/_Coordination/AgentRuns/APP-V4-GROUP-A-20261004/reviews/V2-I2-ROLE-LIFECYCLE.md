# V2-I2-ROLE-LIFECYCLE — independent first-seam review

2026-10-05. **NOT READY for integration at original lifecycle source77e2/test7a7c: native response shape/type validation must be repaired.** No native lifetime/adoption, trusted persistent binding or shared UI/Host integration is established by this review.

Independent TASK `/root/group_a_execution/contract_reviewer`, native descendant of WORKING_ITEMS `/root/group_a_execution`; supplied Codex gpt-6.1-sol/medium, no substitution/diversity claim or delegation. Applied already-loaded repository software-code-review. Read entire new lifecycle module/tests, frozen owner return, actual role composition/guard code, NativeHistory correlation/schema seams, local pinned native definitions and reviewed ROLE/content-method/pin warrants. Only this review written; no product/Design/Git edits, network, model/native/server/auth or downloaded artifact. Parent granted a focused build-resource slot for two pure source-inclusion repro cases; released after the result for queued I5 review. Temporary harness/workspace removed.

## Blocking finding

**RL-1 [P1] Partial field checks admit malformed native results and cache untyped metadata.** Location: role_lifecycle.rs observation() used by PreparedStart::observe and MetadataRequest::observe.

The method checks response id/generation, absence of method/error, nonempty result.thread.id and instructionSources string-array shape. It never validates the pinned method-specific ThreadStartResponse, ThreadResumeResponse or ThreadForkResponse. Native definitions require model, modelProvider, cwd, approvalPolicy, approvalsReviewer, sandbox and complete Thread shape. The seven positive tests intentionally build only thread.id/agentRole/turns/instructionSources, omitting those mandatory fields. Such tests do not establish the stated malformed-response refusal contract.

Independent focused source-inclusion checks against the actual module reproduced both failures:

```text
schema-incomplete correlated result accepted=true
malformed role hint object cached=true
0 passed / 2 failed; test exit101
```

Case1 passes matching generation/id and actual sent composition with `{id:1,result:{thread:{id:"review-thread"}}}`. PreparedStart.observe returns Ok(RoleBinding), even though the response lacks mandatory protocol fields. Case2 supplies agentRole as an object containing an invented unexpected-native-transcript field; the binding evidence retains that object in observation.agent_role. Shape-correct source ids/actual sent text alone do not establish a valid successful native thread or bounded metadata types. This can promote partial/malformed data into AppObserved role state and retain payload content outside the promised metadata-only cache.

Repair: validate exact pinned method-specific result schemas before extracting/caching a NativeObservation, align with NativeHistory's full response validation and reject wrong typed agentRole/forkedFromId/source fields. Keep actual sent frame/id, complete generation/home, relational thread/fork checks and authentic Host provenance requirements in addition to schema validation; schema validity alone must never manufacture a native observation. Correct positive fixtures to complete invented native shapes and add missing-required-field/wrong-metadata-type negatives for start, resume and fork. No supplier shape or criterion should be narrowed to obtain a pass.

## Supported source properties and integration requirements

- Frozen original common/role buffers, default/content identities, path/kind/role/part counts/byte ranges and exact separator reconstruction are checked and retained independently of future-store data. Current file edits/missing/unreadable sources yield future-conversation notices only; native role hints do not reselect the App role. No current selector is substituted for original guidance.
- RoleBinding/PreparedStart/MetadataRequest trusted state is private and not Deserialize. Imported role evidence stays Unknown even when byte/schema-valid. Duplicate home/thread registry insertion rejects replacement. Known no-role None remains distinct from missing/foreign Unknown. This is in-memory custody, not a trusted persistent replay mechanism.
- PreparedStart requires a matching actual outbound id/method/developerInstructions buffer and observed generation/response correlation. Authentic sent-write/current-generation/response provenance remains the real Host caller's duty, not guaranteed cryptographically by callers supplying serde_json::Value. Current source claims that boundary truthfully. Integration must use actual Host observations, not reconstruct a purported sent frame from the selector or file.
- Resume/fork packets are exactly threadId-only and compared to the actual sent params; new instructions/model/provider/settings/policy fields refuse metadata continuation. Resume keeps the original binding, and fork needs a distinct thread plus native forkedFromId source relation while preserving original guidance and separate supply reference. NativeHistory owns transcript/pages, not this role account. Typed metadata repair RL-1 remains required before those shape claims are sound.
- Start integration must preserve ROLE's additive-only direction/baseInstructions-unset and owning user configuration; the lifecycle start check currently proves the exact developer fragment only, not all other actual params. Do not label other settings/base preservation or adoption established from that comparison. Compare role-owned fields at the real dispatcher without vetoing independently user-owned settings.
- NativeHistory HistoryQuery.id() is **local query correlation**, not Host.next_id native RPC identity. Shared dispatcher must retain the map/query reference separately and supply actual Host request id/frame/ref and full generation to this seam. History selection/stream epochs stay with NativeHistory; native resumed_thread is not active Host registration. This seam supplies no current shared lib/UI mapping implementation or supplier-role proof.
- Original App-owned guidance is permitted evidence; no supplier base or native transcript cache should enter it. Persistent-role custody/home/thread reconciliation is required unfinished work before any imported binding becomes current state. Actual supplier lifetime/resume/fork/child/model/qualification and connected Host/store/record/UI evidence remain full obligations, not satisfied or transferred by the seven source tests.

## Independent repro input and command

A reviewer-owned temporary rustc --test harness included **actual** role_supply.rs and role_lifecycle.rs by path, with a tiny SHA256 helper and cached serde/serde_json/sha2 externs. No product source was copied back or edited. It built Guidance::seeded common/HELP_HUMAN bytes, Composition::new and full `{appSession:"review-session",home:"review-home",spawnCounter:1}`, actual sent `{id:1,method:"thread/start",params:{developerInstructions:<same composition>,model:"selected",modelProvider:"selected-provider",cwd:"/review-cwd"}}`. Both observations used the matching generation/id; negatives were malformed result shapes, not mismatched request data. Test1 required an Err for the missing native required fields; test2 required an Err for object-typed agentRole. Both unexpectedly succeeded and failed those original refusal oracles.

Compile: `rustc --edition=2021 --test <reviewer-temp>/shape.rs -L dependency=<app>/src-tauri/target/debug/deps --extern serde=<deps>/libserde-c9f560bb87615823.rlib --extern serde_json=<deps>/libserde_json-285cf9e31e3ede2e.rlib --extern sha2=<deps>/libsha2-36702cb8f24a986f.rlib -o <reviewer-temp>/shape-test`, exit0. Run `<reviewer-temp>/shape-test --nocapture`, exit101,0/2pass. Exact harness SHA256 `d577659b92fb9a5e0dabbc4690f52c65049294f3e1d58f4b9c50545d0da25455`; actual source hash77e2 remained unchanged during reproduction. This executes consumer functions with invented data, never Codex/supplier/provider/native processes. Parent released slot for this test and it was promptly returned.

No blanket rerun of the author's seven positive tests was necessary: they encode the incomplete shapes responsible for this gap. Their reported7/7 remains author evidence, not repair proof. Re-freeze corrected source/tests and backcheck the missing-field/type failures plus affected metadata relations before integration.

## Reviewed original identities

| File | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/role_lifecycle.rs` | `77e2d02ed9867dde6c70b75fc24d27f31e1ba84bed10f5a00c867205c0af2d8f` |
| `projects/chirality-app-v4/app/src-tauri/tests/role_lifecycle.rs` | `7a7c0dfbd4dc00765eae11ec2d6baf8ffb355cdd4212ace74223f3750477c9d2` |

Owner return observed SHA256 `72b58b8f15081dad971b11975b85060c2182a8c05d389636c75f8f4f3cd82c3f`. Relevant source-role/content/pin and NativeHistory/recovery input origins/hashes remain in that return; no historical pin or accepted instruction basis was changed by review. If owner repairs advance the source after this original-hash review, their successor needs a separate backcheck rather than silent rebinding.
