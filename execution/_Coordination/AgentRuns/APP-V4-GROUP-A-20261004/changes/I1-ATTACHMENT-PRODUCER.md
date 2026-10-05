# I1-ATTACHMENT-PRODUCER — bounded prepared text carrier

2026-10-05; TASK `/root/group_a_execution/design_aac`, parent WORKING_ITEMS
`/root/group_a_execution`; native descendant, no delegation. Prepared product
producer under actually READY joined definition V0-ATTACHMENT-CORRELATION-R1.
Only new attachments.rs, tests/attachments.rs, resources/attachments exact
canonical assets/manifest and this record are written. No lib/module wiring,
HOSTING/runtime_session/App/recorder/other Design, Git/auth/network/model/download
changes. Cargo ran in the explicit shared-lane reservation: final13/13 pass;
initial fixture-setup failure and repair are retained below. Native picker integration and provider/image witnesses remain open.

## Produced boundary

Host integration supplies actual native selected PathBuf into
`SelectedTextAttachment::from_native_selection(path, optional_WR_draft)`.
It returns an opaque non-deserializable source selection with exact tagged
native path, separate display, explicit text carrier and observed file identity.
`prepare_for_source(exact_native_tag, App_submission_UUID, recorded_at)` rereads
one bounded buffer; digest and UTF8 decoding come from that exact buffer, not
separate reads. Source mismatch/drift, unreadable/missing source, overlimit,
nonUTF8/NUL, image-carrier file or supplier-unrepresentable/relative native path
returns a visible hold for confirmation/removal/appropriate existing carrier.
No truncation, replacement-character dispatch path, copy/cache or alternate
text/file is produced. Confirming current content means a fresh native source
selection, not accepting a stale identity. Image/named-path producers are not
implemented here; their established routes remain assigned/open.

Bound262144 inclusive counts original file bytes, not wrapped input. BOM,
CRLF, whitespace and final newline survive exactly. JSON quoting of display
name and exact path prevents control characters from adding header lines;
file text itself is untouched. File identity uses accepted App exact-byte method
`chirality.app.exact-bytes.sha256/v1`; element identity names sha256 over UTF8
text. Complete actual supply objects validate against the full exact canonical
schema using the shared offline declared-ID registry/retrieval refusal.
Canonical source/schema fixtures are embedded at build time; no dated AgentRuns
or repository path is read by runtime validation.

`prepare_ordered(selections, submission_ref, recorded_at)` returns a private
immutable ordered PreparedAttachmentList only when all entries prepare; repeated
selection refs are refused and any failed member yields no returned partial
list. Its readonly getters expose native inputs, complete records and ordered
`attachment:<opaque attachmentId>` refs, all with the same immutable App token.
New preparation mints fresh attachment IDs; native future turn IDs are never
invented. Copies a consumer obtains cannot rewrite the internal list/records.
Standing is **prepared; not persisted or sent**. Supply carrier standing alone
is not dispatch/receipt/adoption evidence. Native input has only documented
text/text_elements fields; no model/role/permission or submission wire token.

Owning WR draft metadata is passed explicitly into DraftTrialReference; it is
schema-checked and emitted with exact draft/not-registered/not-a-run standing.
WORKFLOW.md uses the same attachment text carrier. No run-start/guidance,
registration, A15 evidence or draft outcome is invented. WR/ROLE retained source
ownership and the person's explicit send remain the next integration boundary.

## Exact next integration interface and limits

The source-owned sender must persist every returned supply record and exact
ordered list, then existing HOSTINGv0.10 submissionAssociation containing this
submissionRef/thread/supplyRefs/optional actually observed steer target, with
its own outer full generation/RPC/method/prepared client custody, before any
pipe write. It must recheck actual generation/pipe/cancellation, resolve exact
complete immutable same-token list, and preserve write/result/cold unknowns.
This producer performs none of that persistence or transport and establishes
no durable receipt. Retain original facts; no automatic retry, nearby-turn
correlation, new transcript/store/RS kind or accepted-effect claim. It is not
wired into lib/UI here; integrating owner owns registration/native picker/composer
and existing transport, review and native execution witnesses. Ordinary text
steering remains disjoint from attachment factory eligibility/persistence.

## Checks prepared/executed

- Source asset comparison:3 maintained files byte-equal current canonical
  schema/fixtures and manifest SHA256 entries; pass.
- `rustfmt --edition2021 --config skip_children=true src/attachments.rs
  tests/attachments.rs`: exit0, only own files formatted.
-11 actual temp-file/path/schema tests prepared: exact bytes/hash/BOM/CRLF/empty;
  threshold/wrapper; drift/missing/directory/nontext/imagehold; foreign/display/
  relative and nonUnicodepath; framingcontrols; ordered immutable/partialfailure;
  same-name distinct/freshIDs; WRdraft meaning; canonical valid/invalid fixtures/
  failclosed setup; embeddedorigin hashes and actual0.160 UserInput shape.
  Executed after explicit Cargo grant; initial failure/repair below; no oracle
  weakened or skipped.

## Current source/output identity

- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V0-ATTACHMENT-CORRELATION-R1.md`: `406a13e04ffacb97d8e9f6051a7c426f3f91008e9a1c698614bce0ea921d513d`
- `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/NATIVE_INTERACTION_RECEIVING.md`: `7d96396172af4e444654809bc6946acd350477faf51eaa5afc1905259cd1c7f4`
- `projects/chirality-app-v4/app/src-tauri/src/schema_validation.rs`: `42545d9d544f0a8ac7be84814bc9285d987888e6c7ef2ca0201041458c2eb3a9`
- `projects/chirality-app-v4/app/src-tauri/src/util.rs`: `4c890ed6e57c5ef5a155dfac18133f9a0ab7c5b7ba1a96b5a42631a2ebceb951`
- `projects/chirality-app-v4/app/src-tauri/src/attachments.rs`: `f9b55fcdb52f675c7b8e7d3bda2bf53cc7ce3f7aba1397e07309982d3d8395e4`
- `projects/chirality-app-v4/app/src-tauri/tests/attachments.rs`: `50efa24bb3e7e1fe398971b596a11400e08b26271372dc8caafd063e2bfd1a19`
- `projects/chirality-app-v4/app/src-tauri/resources/attachments/manifest.json`: `332688c5fccd2e0612f26c2cdbc7363f28661f157129ac7a106c0b5750edd247`
- `projects/chirality-app-v4/app/src-tauri/resources/attachments/nir.attachment-supply-record.example.invalid.json`: `835cd85dcbed2f7c176e3750f430e75a183495a88d9fd2bf19302f097ef87da6`
- `projects/chirality-app-v4/app/src-tauri/resources/attachments/nir.attachment-supply-record.example.valid.json`: `ac5f161cf90a3d890dcc9dd49574b65ec8f793b3fb7a7dba99b42a78e948bbe3`
- `projects/chirality-app-v4/app/src-tauri/resources/attachments/nir.attachment-supply-record.schema.json`: `6562b8efacb75a3814f59b5918cdac9210e968f008059544864fa234e550a8c1`

## Actual Rust checks, initial failure and repair

Exact command: `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home cargo test
--offline --locked --test attachments`, cwd App `app/src-tauri`, shared target
unchanged. Parent granted the lane after prior reviewer released it; this TASK
released promptly after final test. No native App/model/auth/provider execution.

First exit101:12/13 passed. The nonUnicodepath case failed in setup because
`std::fs::write` of an invalid-byte filename returned EPERM/Operation not
permitted before the producer ran. No claim about the underlying host-policy/
filesystem cause is made. The actual strict representation contract is checked
before producer file IO, so the repaired test constructs that exact lossless
nonUnicode native identity, asserts supplier-unavailable without lossy dispatch,
and uses a real readable Unicode-file control. No skip/permissive branch or
relaxed identity oracle is introduced; impossible fixture creation is no longer
an unrelated prerequisite. Removed the unused own InvalidDraft enum variant.

Final exit0: **13/13 tests pass,0ignored** (11 producer tests plus2 imported
existing schema/clock controls). Shared imported dead-code warnings remain;
no warning suppression or shared-source edits. Native/path/hash/schema temp-file
behavior is exercised; actual invalid-byte file creation is unavailable on this
host and is not claimed. Real picker, durable whole-list pre-send, scoped pipe
write/cold resolution/provider/image/actual native-user witnesses remain open
at the next integration. Independent product review is still required.

Compiler/tool versions and host:

- rustc 1.92.0 (ded5c06cf 2025-12-08) (exit0)
- cargo 1.92.0 (344c4567c 2025-10-21) (exit0)
- macOS-26.6.2-arm64-arm-64bit-Mach-O

Frozen final outputs (earlier source hashes above remain historical):

- `projects/chirality-app-v4/app/src-tauri/src/attachments.rs`: `7b68e9c9b1415a4501942a74ad947f2f521ec5205e788a75b6c4f3895afbdbaa`
- `projects/chirality-app-v4/app/src-tauri/tests/attachments.rs`: `15715daba6894cdbab7f24cbcc519dafee1376016efdcc445b43c27eae55386e`
- `projects/chirality-app-v4/app/src-tauri/resources/attachments/manifest.json`: `332688c5fccd2e0612f26c2cdbc7363f28661f157129ac7a106c0b5750edd247`
- `projects/chirality-app-v4/app/src-tauri/resources/attachments/nir.attachment-supply-record.example.invalid.json`: `835cd85dcbed2f7c176e3750f430e75a183495a88d9fd2bf19302f097ef87da6`
- `projects/chirality-app-v4/app/src-tauri/resources/attachments/nir.attachment-supply-record.example.valid.json`: `ac5f161cf90a3d890dcc9dd49574b65ec8f793b3fb7a7dba99b42a78e948bbe3`
- `projects/chirality-app-v4/app/src-tauri/resources/attachments/nir.attachment-supply-record.schema.json`: `6562b8efacb75a3814f59b5918cdac9210e968f008059544864fa234e550a8c1`

## Canonical merged tool output — first run (exit101)

```text
   Compiling chirality-app-v4 v0.0.0-skeleton (/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/app/src-tauri)
warning: variant `InvalidDraft` is never constructed
  --> tests/../src/attachments.rs:53:5
   |
46 | pub enum HoldReason {
   |          ---------- variant in this enum
...
53 |     InvalidDraft,
   |     ^^^^^^^^^^^^
   |
   = note: `HoldReason` has derived impls for the traits `Debug` and `Clone`, but these are intentionally ignored during dead code analysis
   = note: `#[warn(dead_code)]` (part of `#[warn(unused)]`) on by default

warning: struct `RecordValidator` is never constructed
   --> tests/../src/schema_validation.rs:121:12
    |
121 | pub struct RecordValidator(Validator);
    |            ^^^^^^^^^^^^^^^

warning: associated items `from_resources` and `validate` are never used
   --> tests/../src/schema_validation.rs:125:12
    |
122 | impl RecordValidator {
    | -------------------- associated items in this implementation
...
125 |     pub fn from_resources(resources: &[(&str, &str)]) -> Result<Self, String> {
    |            ^^^^^^^^^^^^^^
...
130 |     pub fn validate(&self, entry: &Value) -> Result<(), String> {
    |            ^^^^^^^^

warning: function `bundled` is never used
   --> tests/../src/schema_validation.rs:138:8
    |
138 | pub fn bundled() -> Result<&'static RecordValidator, String> {
    |        ^^^^^^^

warning: fields `package`, `offer`, and `capture` are never read
   --> tests/../src/schema_validation.rs:147:5
    |
146 | struct ActValidators {
    |        ------------- fields in this struct
147 |     package: Validator,
    |     ^^^^^^^
148 |     offer: Validator,
    |     ^^^^^
149 |     capture: Validator,
    |     ^^^^^^^

warning: function `act_validators` is never used
   --> tests/../src/schema_validation.rs:165:4
    |
165 | fn act_validators() -> Result<&'static ActValidators, String> {
    |    ^^^^^^^^^^^^^^

warning: function `validate_package` is never used
   --> tests/../src/schema_validation.rs:174:8
    |
174 | pub fn validate_package(package: &Value) -> Result<(), String> {
    |        ^^^^^^^^^^^^^^^^

warning: function `validate_offer` is never used
   --> tests/../src/schema_validation.rs:181:8
    |
181 | pub fn validate_offer(offer: &Value) -> Result<(), String> {
    |        ^^^^^^^^^^^^^^

warning: function `validate_capture` is never used
   --> tests/../src/schema_validation.rs:188:8
    |
188 | pub fn validate_capture(capture: &Value) -> Result<(), String> {
    |        ^^^^^^^^^^^^^^^^

warning: constant `LEGACY_FILE_IDENTITY_METHOD` is never used
 --> tests/../src/util.rs:8:11
  |
8 | pub const LEGACY_FILE_IDENTITY_METHOD: &str =
  |           ^^^^^^^^^^^^^^^^^^^^^^^^^^^

warning: function `file_identity` is never used
  --> tests/../src/util.rs:21:8
   |
21 | pub fn file_identity(path: &Path) -> Option<String> {
   |        ^^^^^^^^^^^^^

warning: function `now_rfc3339` is never used
  --> tests/../src/util.rs:27:8
   |
27 | pub fn now_rfc3339() -> String {
   |        ^^^^^^^^^^^

warning: function `os_account` is never used
  --> tests/../src/util.rs:63:8
   |
63 | pub fn os_account() -> Option<String> {
   |        ^^^^^^^^^^

warning: function `package_snapshot` is never used
   --> tests/../src/util.rs:106:8
    |
106 | pub fn package_snapshot(bytes: &[u8]) -> Result<(serde_json::Value, String), String> {
    |        ^^^^^^^^^^^^^^^^

warning: `chirality-app-v4` (test "attachments") generated 14 warnings
    Finished `test` profile [unoptimized + debuginfo] target(s) in 7.10s
     Running tests/attachments.rs (target/debug/deps/attachments-d754b5ea3cb5c148)

running 13 tests
test non_unicode_native_path_retains_exact_identity_and_is_never_lossy_dispatched ... FAILED
test foreign_tagged_source_and_relative_source_cannot_become_dispatch_paths ... ok
test name_and_path_controls_cannot_add_framing_but_file_text_is_unchanged ... ok
test draft_workflow_text_keeps_trial_reference_and_never_becomes_registered_guidance ... ok
test same_name_different_sources_stay_distinct_and_preparing_again_mints_new_ids ... ok
test util::tests::epoch_formats ... ok
test exact_snapshot_identity_and_native_text_keep_bom_crlf_whitespace_and_empty_file ... ok
test ordered_list_has_distinct_immutable_refs_one_token_and_no_partial_preparation ... ok
test source_drift_missing_directory_and_nontext_are_visible_holds_not_alternate_content ... ok
test full_canonical_validation_accepts_all_valid_fixtures_and_refuses_each_invalid_fixture ... ok
test original_file_bound_is_inclusive_and_wrapper_does_not_reduce_it ... ok
test schema_validation::tests::act_targets_refuse_unavailable_or_invalid_aac_resources ... ok
test embedded_assets_match_canonical_sources_and_produced_input_matches_actual_supplier_schema ... ok

failures:

---- non_unicode_native_path_retains_exact_identity_and_is_never_lossy_dispatched stdout ----

thread 'non_unicode_native_path_retains_exact_identity_and_is_never_lossy_dispatched' (26118615) panicked at tests/attachments.rs:197:47:
called `Result::unwrap()` on an `Err` value: Os { code: 1, kind: PermissionDenied, message: "Operation not permitted" }
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace


failures:
    non_unicode_native_path_retains_exact_identity_and_is_never_lossy_dispatched

test result: FAILED. 12 passed; 1 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.06s

error: test failed, to rerun pass `--test attachments`
```

## Canonical merged tool output — repaired run (exit0)

```text
   Compiling chirality-app-v4 v0.0.0-skeleton (/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/app/src-tauri)
warning: struct `RecordValidator` is never constructed
   --> tests/../src/schema_validation.rs:121:12
    |
121 | pub struct RecordValidator(Validator);
    |            ^^^^^^^^^^^^^^^
    |
    = note: `#[warn(dead_code)]` (part of `#[warn(unused)]`) on by default

warning: associated items `from_resources` and `validate` are never used
   --> tests/../src/schema_validation.rs:125:12
    |
122 | impl RecordValidator {
    | -------------------- associated items in this implementation
...
125 |     pub fn from_resources(resources: &[(&str, &str)]) -> Result<Self, String> {
    |            ^^^^^^^^^^^^^^
...
130 |     pub fn validate(&self, entry: &Value) -> Result<(), String> {
    |            ^^^^^^^^

warning: function `bundled` is never used
   --> tests/../src/schema_validation.rs:138:8
    |
138 | pub fn bundled() -> Result<&'static RecordValidator, String> {
    |        ^^^^^^^

warning: fields `package`, `offer`, and `capture` are never read
   --> tests/../src/schema_validation.rs:147:5
    |
146 | struct ActValidators {
    |        ------------- fields in this struct
147 |     package: Validator,
    |     ^^^^^^^
148 |     offer: Validator,
    |     ^^^^^
149 |     capture: Validator,
    |     ^^^^^^^

warning: function `act_validators` is never used
   --> tests/../src/schema_validation.rs:165:4
    |
165 | fn act_validators() -> Result<&'static ActValidators, String> {
    |    ^^^^^^^^^^^^^^

warning: function `validate_package` is never used
   --> tests/../src/schema_validation.rs:174:8
    |
174 | pub fn validate_package(package: &Value) -> Result<(), String> {
    |        ^^^^^^^^^^^^^^^^

warning: function `validate_offer` is never used
   --> tests/../src/schema_validation.rs:181:8
    |
181 | pub fn validate_offer(offer: &Value) -> Result<(), String> {
    |        ^^^^^^^^^^^^^^

warning: function `validate_capture` is never used
   --> tests/../src/schema_validation.rs:188:8
    |
188 | pub fn validate_capture(capture: &Value) -> Result<(), String> {
    |        ^^^^^^^^^^^^^^^^

warning: constant `LEGACY_FILE_IDENTITY_METHOD` is never used
 --> tests/../src/util.rs:8:11
  |
8 | pub const LEGACY_FILE_IDENTITY_METHOD: &str =
  |           ^^^^^^^^^^^^^^^^^^^^^^^^^^^

warning: function `file_identity` is never used
  --> tests/../src/util.rs:21:8
   |
21 | pub fn file_identity(path: &Path) -> Option<String> {
   |        ^^^^^^^^^^^^^

warning: function `now_rfc3339` is never used
  --> tests/../src/util.rs:27:8
   |
27 | pub fn now_rfc3339() -> String {
   |        ^^^^^^^^^^^

warning: function `os_account` is never used
  --> tests/../src/util.rs:63:8
   |
63 | pub fn os_account() -> Option<String> {
   |        ^^^^^^^^^^

warning: function `package_snapshot` is never used
   --> tests/../src/util.rs:106:8
    |
106 | pub fn package_snapshot(bytes: &[u8]) -> Result<(serde_json::Value, String), String> {
    |        ^^^^^^^^^^^^^^^^

warning: `chirality-app-v4` (test "attachments") generated 13 warnings
    Finished `test` profile [unoptimized + debuginfo] target(s) in 0.74s
     Running tests/attachments.rs (target/debug/deps/attachments-d754b5ea3cb5c148)

running 13 tests
test foreign_tagged_source_and_relative_source_cannot_become_dispatch_paths ... ok
test non_unicode_native_path_retains_exact_identity_and_is_never_lossy_dispatched ... ok
test name_and_path_controls_cannot_add_framing_but_file_text_is_unchanged ... ok
test draft_workflow_text_keeps_trial_reference_and_never_becomes_registered_guidance ... ok
test same_name_different_sources_stay_distinct_and_preparing_again_mints_new_ids ... ok
test ordered_list_has_distinct_immutable_refs_one_token_and_no_partial_preparation ... ok
test util::tests::epoch_formats ... ok
test exact_snapshot_identity_and_native_text_keep_bom_crlf_whitespace_and_empty_file ... ok
test source_drift_missing_directory_and_nontext_are_visible_holds_not_alternate_content ... ok
test full_canonical_validation_accepts_all_valid_fixtures_and_refuses_each_invalid_fixture ... ok
test original_file_bound_is_inclusive_and_wrapper_does_not_reduce_it ... ok
test schema_validation::tests::act_targets_refuse_unavailable_or_invalid_aac_resources ... ok
test embedded_assets_match_canonical_sources_and_produced_input_matches_actual_supplier_schema ... ok

test result: ok. 13 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.06s

```

## ATT-P1 actual robustness finding and descriptor repair

The first producer candidate (attachments.rs
`7b68e9c9b1415a4501942a74ad947f2f521ec5205e788a75b6c4f3895afbdbaa`,
tests `15715daba6894cdbab7f24cbcc519dafee1376016efdcc445b43c27eae55386e`,
record `08b80a0f3d850898e1eca957ed9afed8549da93396837ae6c36ec8472cdabce3`)
was independently NOT READY under `reviews/V1-ATTACHMENT-PRODUCER.md` ATT-P1.
Reviewer's exact copied read_snapshot function SHA
`feedb96324d4417e1812ac9ab736f33b663ed53d81cc0f4887a3485a15dd454a`
blocked in File::open on an actual owned FIFO with no writer; the independent
2-second timeout killed/reaped it (exit-9). Same exact helper on a regular
file exited0. Original report/source warrant and isolated repro remain the
original evidence; the earlier13-test pass did not cover this defect.

Repair uses the already declared/cached libc dependency (no new dependency or
download). On the Unix MVP host, read-only OpenOptions uses O_NONBLOCK|O_NOCTTY,
then checks **that opened descriptor's** metadata.file_type().is_file before
any bounded read. A special source is visibly held with cause/no send. There
is no vulnerable pre-open pathname-only check, alternate file/text, new path
authority gate or copy/cache. Regular-file identity/decoding still come from
one exact bounded buffer and all original source/token facts remain immutable.
This repairs the owned special-source/replacement case, not a universal storage
latency qualification or a native supplier/provider witness.

Added actual owned initialFIFO(no writer) and selected regular-file→FIFO
replacement tests. Each calls the actual producer in its own test binary
under the original2-second deadline; timeout would kill/reap, and parent owns
cleanup even after failure. The worker is also a normal regular/Unicode-file
positive in the main suite. Existing bounds, Unicode, drift, exact-byte/hash,
schema and draft controls remain, without skips or oracle weakening.

Parent explicitly granted exact same offline/locked command/cache/shared target.
Final Rust run exit0: **16/16,0ignored** (14 producer controls plus2 existing
shared controls), including both FIFO negatives. Cargo promptly released.
Independent same-reviewer successor backcheck still needed before fan-in.
No shared/HOSTING/Design/product wiring/auth/model/native-supplier/Git change.

Frozen repair hashes:

- `projects/chirality-app-v4/app/src-tauri/src/attachments.rs`: `77791e9bb62dd994ff7f0fa12a04acb667834ca3d5132f2a3d7284b308ffa0a5`
- `projects/chirality-app-v4/app/src-tauri/tests/attachments.rs`: `3d15eca729d4e8c5ff045a9386503d730a9c30ec8e7be3e8dc581feb7feda553`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V1-ATTACHMENT-PRODUCER.md`: `b8a4fd797735b4a3aa47bcca3d0a81eb1c25a9e5c56e0413e81d8aca6024b51f`
- `projects/chirality-app-v4/app/src-tauri/Cargo.toml`: `2d89ee516e013d3e8990c15a2eaeebb1ce08588934a26193bfb93b604e4f7d31`

## Canonical merged tool output — descriptor/FIFO repair (exit0)

```text
   Compiling chirality-app-v4 v0.0.0-skeleton (/Users/ryan/.codex/worktrees/077c/chirality/projects/chirality-app-v4/app/src-tauri)
warning: struct `RecordValidator` is never constructed
   --> tests/../src/schema_validation.rs:121:12
    |
121 | pub struct RecordValidator(Validator);
    |            ^^^^^^^^^^^^^^^
    |
    = note: `#[warn(dead_code)]` (part of `#[warn(unused)]`) on by default

warning: associated items `from_resources` and `validate` are never used
   --> tests/../src/schema_validation.rs:125:12
    |
122 | impl RecordValidator {
    | -------------------- associated items in this implementation
...
125 |     pub fn from_resources(resources: &[(&str, &str)]) -> Result<Self, String> {
    |            ^^^^^^^^^^^^^^
...
130 |     pub fn validate(&self, entry: &Value) -> Result<(), String> {
    |            ^^^^^^^^

warning: function `bundled` is never used
   --> tests/../src/schema_validation.rs:138:8
    |
138 | pub fn bundled() -> Result<&'static RecordValidator, String> {
    |        ^^^^^^^

warning: fields `package`, `offer`, and `capture` are never read
   --> tests/../src/schema_validation.rs:147:5
    |
146 | struct ActValidators {
    |        ------------- fields in this struct
147 |     package: Validator,
    |     ^^^^^^^
148 |     offer: Validator,
    |     ^^^^^
149 |     capture: Validator,
    |     ^^^^^^^

warning: function `act_validators` is never used
   --> tests/../src/schema_validation.rs:165:4
    |
165 | fn act_validators() -> Result<&'static ActValidators, String> {
    |    ^^^^^^^^^^^^^^

warning: function `validate_package` is never used
   --> tests/../src/schema_validation.rs:174:8
    |
174 | pub fn validate_package(package: &Value) -> Result<(), String> {
    |        ^^^^^^^^^^^^^^^^

warning: function `validate_offer` is never used
   --> tests/../src/schema_validation.rs:181:8
    |
181 | pub fn validate_offer(offer: &Value) -> Result<(), String> {
    |        ^^^^^^^^^^^^^^

warning: function `validate_capture` is never used
   --> tests/../src/schema_validation.rs:188:8
    |
188 | pub fn validate_capture(capture: &Value) -> Result<(), String> {
    |        ^^^^^^^^^^^^^^^^

warning: constant `LEGACY_FILE_IDENTITY_METHOD` is never used
 --> tests/../src/util.rs:8:11
  |
8 | pub const LEGACY_FILE_IDENTITY_METHOD: &str =
  |           ^^^^^^^^^^^^^^^^^^^^^^^^^^^

warning: function `file_identity` is never used
  --> tests/../src/util.rs:21:8
   |
21 | pub fn file_identity(path: &Path) -> Option<String> {
   |        ^^^^^^^^^^^^^

warning: function `now_rfc3339` is never used
  --> tests/../src/util.rs:27:8
   |
27 | pub fn now_rfc3339() -> String {
   |        ^^^^^^^^^^^

warning: function `os_account` is never used
  --> tests/../src/util.rs:63:8
   |
63 | pub fn os_account() -> Option<String> {
   |        ^^^^^^^^^^

warning: function `package_snapshot` is never used
   --> tests/../src/util.rs:106:8
    |
106 | pub fn package_snapshot(bytes: &[u8]) -> Result<(serde_json::Value, String), String> {
    |        ^^^^^^^^^^^^^^^^

warning: `chirality-app-v4` (test "attachments") generated 13 warnings
    Finished `test` profile [unoptimized + debuginfo] target(s) in 2.06s
     Running tests/attachments.rs (target/debug/deps/attachments-d754b5ea3cb5c148)

running 16 tests
test foreign_tagged_source_and_relative_source_cannot_become_dispatch_paths ... ok
test non_unicode_native_path_retains_exact_identity_and_is_never_lossy_dispatched ... ok
test initial_fifo_without_writer_is_held_before_any_blocking_read ... ok
test name_and_path_controls_cannot_add_framing_but_file_text_is_unchanged ... ok
test draft_workflow_text_keeps_trial_reference_and_never_becomes_registered_guidance ... ok
test fifo_source_worker ... ok
test exact_snapshot_identity_and_native_text_keep_bom_crlf_whitespace_and_empty_file ... ok
test ordered_list_has_distinct_immutable_refs_one_token_and_no_partial_preparation ... ok
test util::tests::epoch_formats ... ok
test same_name_different_sources_stay_distinct_and_preparing_again_mints_new_ids ... ok
test source_drift_missing_directory_and_nontext_are_visible_holds_not_alternate_content ... ok
test full_canonical_validation_accepts_all_valid_fixtures_and_refuses_each_invalid_fixture ... ok
test original_file_bound_is_inclusive_and_wrapper_does_not_reduce_it ... ok
test selected_regular_source_replaced_by_fifo_is_held_without_blocking ... ok
test schema_validation::tests::act_targets_refuse_unavailable_or_invalid_aac_resources ... ok
test embedded_assets_match_canonical_sources_and_produced_input_matches_actual_supplier_schema ... ok

test result: ok. 16 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.05s

```

## Owning NIR physical metadata/source-reader concurrence — 2026-10-05

Read-only actual assessment by this original producer owner, newly commissioned
by parent (not passive queue reuse). Actually read transport plan80fc and the
HOSTING owner's draft physical allocation1d6a, current exact producer77791e9,
NIR0.2 canonical metadata and HOSTING0.10 conditions. **Source-concur** the two
App-own-data runtime/nir/attachment-supplies/<submissionhash>.json ordered
existing0.2 record array and runtime/hosting/client-requests/<typedfullGhash>/
<typedRPChash>.json existing0.10 client object. This is one physical realization
of existing owning logical sources, not a new schema/kind/transcript/cache.
No extra human placement gate or governed acceptance is inferred.

NIR array members are full canonical metadata including original localPath,
name, file/element identity and optional owning WR draft reference. They exclude
native_inputs/text/file bytes. PreparedList private getters provide the complete
immutable ordered actual records; reader must validate every member and compare
all decoded original values, exact ordered attachment:<opaqueID> refs, unique
IDs, complete membership and same original App submission token, not merely
required fields/schema/filenames. Whole array durable/readable first, existing
client association durable/readable second, actual scoped pipewrite last.
Source/currentfullgeneration/thread/target/pipe/cancel changes or failed/unreadable/
partial/conflicting publication/readback refuse dispatch. Root remains host-
resolved/absolute/outsideCodex with existing containment/no redirection or
silent alternate source. Metadata readers must also avoid ATT-P1-style special-
file blocking: descriptor-regular/nonblocking readback; no path-only check race.

Revalidation must compare source identity and exact file/element/native-input
snapshots to the retained original preparation. The current producer API may
mint fresh ephemeral attachment IDs during that check; those IDs must be
discarded and never substitute the original durable association/supply refs.
Use original private selections/metadata; do not turn equality of new IDs into
an oracle or adopt a new unrecorded list. Same-buffer producer/file-byte bound
and strictUTF8/native-path-representability remain unchanged. No SourceBuffer
class is assumed to exist: actual private PreparedAttachmentList/native_inputs
remain transient source data only. WR owns draft/trial context and ROLE/model
configuration remains unchanged.

Client key codec must preserve complete typedgenerationtuple and typedRPCscalar
(1 and string"1" distinct); storage hashes locate, never mint identity. Cold
prepared metadata is last observation, not no-send proof; cold written/error/
resultmetadata reports its App-observed facts with native-source-unavailable
limits. No nativeTurn reconstructed from receiptposition/steertarget, no JSON-
imported private SourceRequest/capability, successor-Host rebinding or resend.

Concur the exact error projection: actual observed valid integercode plus fixed
message `[attachment custody: native error text withheld; original source may be unavailable]`,
no error.data/native message/resultbody. The marker is explicitly redacted
metadata, not native text. Missing/invalid nativecode cannot become fabricated
code0 or response-observed-error (schema requires errorcode/message); retain
actual unknown/malformed-source limitation and hot original source. The native
evidence stream stays with HOSTING, unrewritten; unavailable cold raw source
cannot be replaced by a reply cache.

No technical NIR conflict found once these explicit reader/immutable-revalidation
requirements are carried by the owning packet/implementation. HOSTING owner
received actual source concurrence and is adding the two reader/revalidation
clarifiers before finalseal. This is not actual durable/source-reader/scopedpipe
execution or independent implementation approval; those checks still precede
connected sending. Only this producer record appended; no product/Design/Cargo,
Git/network/auth/native/model execution.

Actual source bytes at concurrence:

- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I1-ATTACHMENT-TRANSPORT-PLAN.md`: `80fcf1dde38f1f92d3ae571503adfebf7096e487392297e0ba1bbf967f363f9a`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-H-ATTACHMENT-PERSISTENCE-ALLOCATION.md`: `1d6a11061ac0b264d95e36749527d9d3637d6554d01865dfbfa85243db6258af`
- `projects/chirality-app-v4/app/src-tauri/src/attachments.rs`: `77791e9bb62dd994ff7f0fa12a04acb667834ca3d5132f2a3d7284b308ffa0a5`
- `projects/chirality-app-v4/app/src-tauri/resources/attachments/nir.attachment-supply-record.schema.json`: `6562b8efacb75a3814f59b5918cdac9210e968f008059544864fa234e550a8c1`
