# LT-23 terminal exchange — test-only proposal

Read-only proposal after first LT-23 slice PR #1152 merged `6c821d9ccf36d6b5f6a81ccbece6bee5a09fc9e6`. Existing staged author worktree remains untouched. No code/build/export performed. RS, Group B and independent quick review must settle this exact receiving contract before implementation.

## Minimal closed contract

Use a new `group-b-s1-terminal-reader-exchange.v1` format, leaving `group-b-s1-reader-exchange.v1` and its LT-09 exporter byte/behavior contract unchanged. Each case directory contains:

```
exchange.json
predecessor/publication/<untouched LT-09 closure members>
terminal/publication/<untouched LT-23 closure members>
selected-source/<untouched original selected closure>  # selected case only
```

The top object has exactly `format`, `case`, `producer`, `applicationCandidate`, `predecessor`, `terminal`, `selectedSourceMembers`. `case` is `selected` or `unselected`. `predecessor` has exactly `readback`, `actualLt09`, `members`; `terminal` has exactly `readback`, `actualLt23`, `members`. These readback/event JSON values are untouched actual native-held read projections and actual Host lifecycle records, not reconstructed or trimmed fixtures. `members` describes every raw file, including transport, relative to its own publication directory. The original locator values remain unchanged; directory placement is an exchange transport location, not a replacement native source/root locator.

Reuse frozen v1 producer types unchanged: closed `{sourceRevision:40lowerhex,harnessExecutableSha256:64lowerhex,command:nonempty array<string> actual argv,features:sorted unique array<string>,kind:"synthetic-host-test"}`. Application candidate is explicitly supplied `{revision:"INVENTED-S4-APP-REVISION",buildIdentity:"INVENTED-S4-APP-BUILD",standing:"invented-consumer-fixture"}`; never inferred from harness identity. Member arrays are sorted POSIX-lexical `{path,sha256,size}`, contained nonempty relative paths without dot/dotdot/backslash/empty components, lowercase64 digest, nonnegative integer size; duplicates and ancestor collisions refuse. `selectedSourceMembers` is one such array for selected, null with no selected-source directory for unselected. No extra exported capability or trusted issuer field.

## Actual producer sequence and joins

A cfg(test)-only harness reuses Fixture/attach_selected_store, creates genuine AppRuntimeCustody before start, and starts only the invented offline child. Retain the successfully installed LT-09 native reference in memory, successful Host readback, exact actual LT-09 event, and complete raw closure before Stop. Retain selected original bytes once, without structural recursion into opaque evidence. Then call actual Stop and use a finite **test-harness** wait for the actual existing worker to settle. This introduces no production timeout, queue, retry or cancellation policy. Pending, unavailable, busy, panic, deadline expiry or missing worker success fails the export; it never writes a successful exchange from queued evidence.

Obtain the successful terminal Host read using the same full H5 and the actual legacy LT-23 event. Re-read the predecessor via its retained native reference and Store capability, and require equality with its pre-Stop read/bytes; do not deserialize either capability from JSON. Recheck terminal Host read after copying. Both observations and observed artifact references must be byte-identical; readback generation, reference generation, envelope verification_generation, observation generation and each actual legacy event's generation must all agree. Actual LT-23 sequence must follow actual LT-09, transition tuples must remain exact, and each complete legacy event must equal its envelope. Both publications must retain the same original selected-anchor/source association and exact declared source closure; unselected remains truthfully null. The terminal publication is distinct and immutable; neither phase nor legacy event bytes are rewritten. Existing full Store/S1 semantics and at-use guards remain the authority for reads.

Write to an explicitly requested physical temporary parent, a fresh private case directory with no overwrite or symlink/path shortcuts. Verify exact copied member inventories/digests/bytes before writing exchange.json last as completion marker. On any failure no success marker; an incomplete directory is diagnostic only, never a consumer fixture. Raw artifact files are never parsed-and-reserialized for transport. Successful marked exchange means synthetic producer/transport consistency only, not installed qualification or authenticated Git/build provenance.

Author exports from an uncommitted harness are diagnostic precursor evidence with a separate candidate manifest; sourceRevision must not pretend its base commit contains new exporter code. The usable exact-source receiving exports are regenerated after reviewed source commit using its compiled harness and actual full revision. Group B independently validates/adopts them; producer output does not self-accept the consumer.

## Fence and discriminating controls

Test-only child module beside hosting_s4_export.rs, selected from hosting_successor.rs cfg(test) tests; maintained terminal-exchange documentation and bounded author evidence. Prefer a separate terminal module: do not refactor or widen the existing v1 exporter just to share helpers. No production Host/Store/reader semantics, public API, schema/pins, Runtime hydration, UI, Group B implementation, or canonical changes.

Positive selected and unselected exports must prove actual ready→Stop→worker→terminal read, immutable predecessor/raw bytes, exact whole LT-23 including unknown/surviving facts, and successful independent copy recheck. Negatives: no installed LT-09; still pending/busy/worker failure; foreign/restarted H5 or changed sequence; wrong event/predecessor; altered observation/transport/source bytes; source-anchor/subject mismatch refused by live read; extra/missing/duplicate/path-collision members; existing output/symlink/unsafe output path; changed native read during export; selected-source absent/extra or present on unselected. Consumers reject extra top/nested fields and unsupported format/row; no v1 fallback. Existing v1 exports/tests stay unchanged. Run targeted offline tests in both feature states and obtain independent exact-source export/consumer review; no broad build or native App/supplier action is needed.

Remaining limits: historical-byte receipt only, no source/build authentication, S3 issuer, installed custody, SEAL-2, restart hydration, public historical index or new lifecycle support. Pending worker cancellation remains unsupported. The helper must not weaken these limits to make an export pass.

## Exact merged source basis

| Git source | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/hosting_s4_export.rs` | `3114efc75f4c2ca9b3118d82b63d30d25e48455f053bff2c8a75f0ec8c7b1d4c` |
| `projects/chirality-app-v4/app/src-tauri/src/hosting_lt23_tests.rs` | `be03e6119923ee23e1ef3d852af81720158c51b3e10c10ac78fc7dd59799904c` |
| `projects/chirality-app-v4/app/src-tauri/src/hosting.rs` | `7281e582de19ee560b71db0713e8afadc98da617cb1bff02acf2e8382e51edc8` |
| `projects/chirality-app-v4/app/src-tauri/src/distribution_store_s1.rs` | `e89b7a56022fc2c5d0860788fa423a94d8072ca0ed184304183e5923ddbe8c57` |
