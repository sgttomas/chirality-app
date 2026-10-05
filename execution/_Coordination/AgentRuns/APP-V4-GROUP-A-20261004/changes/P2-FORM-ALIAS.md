# P2 form-alias backend gate — narrow staged-candidate repair

2026-10-05. TASK `/root/group_a_execution/runtime_integration`, parent `/root/group_a_execution`, delegated-harness-native descendant; supplied gpt-6.1-sol/medium, no descendants. Own writes only native_requests.rs's exact alias condition plus focused native_requests tests and this record. No lib/UI/Host/recovery/Design/schema/dependency/auth/model/network/Git-index mutation. Original immutable candidate suite session98411 completed with parent-reported exit0; that suite did not establish this missing direct alias gate.

## Original symptom/source retained

Parent relayed the independent P2 integration reviewer finding: README claims the three form aliases validate content, but native_requests::validate_answer gated requestedSchema only when mode == "form". `Host.answer_server_request` directly invokes RequestRegister.prepare; the generated McpServerElicitationRequestResponse accepts generic content and does not bind it to the request's schema. Thus direct valid-origin accepted openai/form or openaiForm could skip requestedSchema and return a prepared reply with invalid content. App answer_preview normalized recognized form modes to a temporary mode=form, so its rendered/preview tests could pass while the backend gate was incomplete.

This original symptom is source-confirmed/independently reported, **not independently executable-reproduced on the old version by this author**. Original indexed module bytes matched the working file before editing and remain retained as the Git blob below; no earlier symptom evidence or failing source has been erased. The old production condition was exactly `&& params["mode"] == "form"`.

## Exact repair and supported modes

The sole production change is that one condition becoming an explicit match for `form`, `openai/form`, `openaiForm`. The unchanged following code requires requestedSchema, compiles the full supplied schema with jsonschema options.offline(), and validates the accepted content. No partial handwritten field check/default schema/retrieval-enabled builder is introduced. Unknown/non-form handling is unchanged; no additional mode or device-proof acceptance is newly adopted. App's unsupported device/unknown acceptance handling remains its separately reviewed path.

The maintained unchanged 0.160.0 McpServerElicitationRequestParams publishes exactly these three form variants, each requiring mode/message/requestedSchema. Normal form names McpElicitationSchema; the OpenAI aliases permit arbitrary schema values but still require the field. Its URL and openai/userVerification variants are separate. The negative action forms still bypass accepted-content validation, allowing an explicit decline/cancel even for an unusable/missing/false schema. There is no automatic negative/default answer.

Raw nativeParameters (including original alias spelling and unknown fields) are never normalized or mutated in the live register. Reply content/meta pass through unchanged once validated. Origin restrictions, complete generation/request lookup, refusal ordering, secret-question redaction, writing and acknowledgment are unchanged. Mechanical reverse of this exact condition plus removal of the appended test block reproduces the original indexed module byte-for-byte; this check passed before freezing.

## Meaningful direct checks

New form_alias_validation_tests has three groups. Each supported alias directly calls RequestRegister.prepare, checking invalid type, missing required answer field, minimum length, unexpected extra field and null content refuse invalid-answer with complete entries unchanged; valid content returns the exact native prepared reply and preserves params/mode/origin. Another per-alias group refuses absent requestedSchema, a false schema and an external reference with retrieval disabled. The third retains exact decline/cancel forms for aliases and existing URL/device/unrecognized-mode negatives, plus refuses affirmative named-App-rule origin. This does not claim future/unknown mode acceptance support or a new device protocol implementation.

Approved cache and parent-granted exclusive Cargo slot; source preparation did not consume the shared Cargo slot while immutable suite98411 ran. Commands from repository root:

- `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home cargo test --offline --locked --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml --lib form_alias_validation_tests`: exit0, **3/3 pass**, 0 failed/ignored, 0.14s.
- Same command with `--lib native_requests::`: exit0, **13/13 pass**, 0 failed/ignored, 0.12s. Existing closed-generation, origin, schema/decline, failed-write, secret redaction, supplier-resolution and exported-contract checks retained.

Cargo slot released immediately after checks. No actual native process/model turn/auth/account/network/download was exercised. External-ref cases use the existing offline builder and establish refusal, not measured socket/provider qualification. Source is frozen for independent added-branch/direct-gate backcheck. **Not staged**; only the manager may stage the repaired file after the actual independent backcheck. Original index/blob remains unchanged now. No whole staged-candidate/full NIR/Group A qualification or acceptance is inferred.

## Exact frozen identities

| Subject | SHA-256 / identity |
|---|---|
| Original indexed module Git blob | `a1e2f035c04d36c07d618d87a8897425c19afec8` |
| Original indexed module SHA-256 | `5879e6d034820e5d26c6dea1a4947ab851a39c0598aa675753ab6948e3030dbe` |
| Repaired full native_requests.rs | `bb3317458e40ade1e623f86ed771c196a97e07ca7e4daa8a89931b3ea6ee6992` |
| Repaired exact MCP schema-gate branch | `cffbbfb077edc603e816ad9bd79def71dfb2eb7fc2bb8abe4da39e26df51b041` |
| Appended focused test block | `8c06746b582769651640bb84ab94a751f084ccdd1ebac29f295c59aa868bb404` |

Branch boundary: the MCP accepted-content condition through immediately before item/tool/requestUserInput validation. Test boundary: cfg(test)/form_alias_validation_tests through EOF.

## Read-source origins

| Repository-relative origin | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/resources/supplier/0.160.0/codex_app_server_protocol.schemas.json` | `7243ba241962af92ca60581f1a81808ebda4212a800f8b205f54703bcfd508c5` |
| `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` | `fbe61326d878fc92d7301773e38e0781dbaca6f98eb46ba87df06b80b6991510` |
| `projects/chirality-app-v4/app/src-tauri/src/runtime_session.rs` | `c96db03894b242f78a7029b5e04063f639fb02dc13b0c8de59de4b3e9e0e88b9` |
| `projects/chirality-app-v4/app/README.md` | `6b219f7f950b546a9bace569626d9d371236a4ee900f334124dd491ba05cfde3` |
