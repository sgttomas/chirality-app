# I3 A15 recorded-claim reader semantics — 2026-10-05

TASK `/root/group_a_execution/catalog_adapter_production`, parent `/root/group_a_execution`, native delegated descendant; no delegation. Ordinary RS/WR existing-contract receiving implementation. New record_semantics.rs and focused tests; only bounded record_relations consuming join changed. No lib/UI/decision_view/records writer/schema/Design/Host/WF/instruction/graph/Git changes, real homes/native/auth/model/network/download or capture/registration admission.

## Recovered gap/API before mutation and parent concurrence

Read RS HA-10/§6.2a/§13.5/§14.2 R-7 and WR ID-1…3/RB-4/ME-3/LS-1…4. Actual records::read_log admits complete-schema-readable RS claims; record_relations groups them and derives current correction candidates without A15 correspondence checks. Schema explicitly describes ordered one-to-one registeredEntries correspondence and boundContent==reviewedDraft.content as a reader rule. Returned exact gap/API before mutation; parent concurred the source limit and authorized proceeding without new authority/method/schema.

Persisted A15 subjects and WR ID-3 references are opaque scalar display references, not full library/sourceRoot tuples; the WR prototype shortens the revision display. No tuple/root/method is parsed or inferred from those labels. Historical method/value and old revisions remain unchanged. Package bytes/coherence, capture proof, NativeOrigin/RootClaims, ledger standing and actual registration remain their owning consumers' evidence.

## Produced subset and actual consuming join

`check_a15_correspondence(record)` uses unchanged full RS shape validation, then checks single-form cardinality or ordered registeredEntries/boundSubject/boundContent cardinality/subject equality and every reviewed/bound method+value+scope. Different/unavailable methods, scope or notObtainable yield incomparable, never a value-only match; comparable unequal content/order/cardinality yields nonconformant. Matching opaque historical inputs are only checked for this R7 subset. Status/reasons/derived-claim eligibility are separate from native custody unknown, actAdmitted=false and registrationEstablished=false; no general conformance verdict.

`check_registration_candidate(record, ordered RegistrationBinding[])` additionally requires actual explicit source inputs: candidate full RS tuple and descriptor's registered full tuple, library origin/sourceRoot/scope, opaque persisted subject/review reference, content identity/prior tuple and source reference. Canonical RS tuple/content definitions validate context shape; full origin/root/name/revision/method/derived-from, library/scope and order comparisons are exact. Missing binding remains incomparable; full candidate mismatch excludes that association. It creates no capture-proof/capability constructor. Root/I2 must provide genuinely supplied descriptor/library facts and independently check actual capture, coherent bytes/ledger/standing before any registration claim.

`record_relations` includes this module and annotates every original schema-readable claim. Raw records, provenance, sources, native limits and correction links remain inspectable. Only semantically checked/not-applicable records can be derived current claim candidates. An invalid/incomparable A15 correction cannot apply precedence or suppress a valid predecessor; a valid semantic repair can correct a bad original. The pre-existing correction identity/ambiguity/cycle/same-writer complete-log order rules stay intact; no recordId sorting, filename order or equal timestamp establishes human chronology. Non-A15 behavior remains unchanged. decision_view's once-read correction projection is the actual existing consumer; no writer/A15 count/current registration is silently added.

## Connected tests and bounded checks

Six new tests use actual temporary UTF-8 JSONL and records::read_log/full schema plus the consuming read_logs projection: original valid single/multi/historical/other-kind controls; schema-valid content/cardinality/ordered-subject mismatches readable but ineligible; same digest under different methods/scopes or unobtainable identities incomparable/native unknown; explicit full tuple/library/revision/order mismatch vs valid single/multi; full prior/derived tuple methods; invalid/incomparable correction cannot suppress a valid original while a valid repair can replace bad source. Canonical Design example bodies are read as identified test inputs and not modified; synthetic fixture seq/correction/context changes are in scratch logs only, not rewritten authoritative records. No real person/capture/store/registration witness. Five original record_relations CI-12 controls are selected for affected preservation alongside the six new tests; Manager granted the exclusive Cargo slot with all relevant Core/shared compile inputs explicitly paused through both target runs, after WR release.

## Actually consulted origins

- `projects/chirality-app-v4/app/src-tauri/src/records.rs` SHA-256 `cc61f735ab8dfa987081b5f50d37bd0a8b93c340c80cc5bd72266a307c588fea`
- `projects/chirality-app-v4/app/src-tauri/src/decision_view.rs` SHA-256 `5e8c471a65da20946c8b84d2fbbae26c4f7f7e413f5d90bd61ec3c9ac7b70e79`
- `projects/chirality-app-v4/app/src-tauri/src/schema_validation.rs` SHA-256 `42545d9d544f0a8ac7be84814bc9285d987888e6c7ef2ca0201041458c2eb3a9`
- `projects/chirality-app-v4/app/src-tauri/tests/record_relations.rs` SHA-256 `ad6ce8a460be42883560bb341eceb2be525e0fe768bd41f7bd6835c32971aa76`
- `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RECORD_SEMANTICS.md` SHA-256 `15266b5078ad1878dae20dc1fa2ef93723d187ce18d5fe780bd1af75c00d5f41`
- `projects/chirality-app-v4/execution/PKG-04_Human acts, autonomy and run evidence/1_Working/DEL-04-03_Content-bound decisions and compact run records/Design/RS_RECORD.valid.act-log.example.jsonl` SHA-256 `b34997bb5168b747a9fe0c91ffa2ca8f5708c518eb1844331b65b294d3895e0a`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Design/WORKSPACE_AND_REGISTRATION.md` SHA-256 `bd61f48ca97eba9c7665b31ff7506672f18152d57a20b0ffd361a168750af989`
- `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-02_Workflow-making workspace and registration/Design/prototype/wrproto.py` SHA-256 `303474582a5192909b7f60e0108009d47efe77fd0477f1ec3c88f00b80fd9c62`

## Actual verification and frozen return

Exact command: `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home CHIRALITY_SKIP_CODEX=1 cargo test --offline --locked --test record_semantics --test record_relations`.

Initial actual exit101: all original record_relations **5/5 passed**, new record_semantics **5/6 passed**. The one failure was the correction test's synthetic `record-original`/`record-invalid-correction` IDs missing the unchanged canonical `^rec:[A-Za-z0-9._:-]+$` prefix; full validator refused before the intended relation case. First failure reported to parent and stdout retained. Diagnosed local repair changed only synthetic IDs and their expected strings to `rec:app:…`; no code/schema/criterion/original oracle weakening.

Final same-command actual exit **0**: original record_relations **5/5**, new record_semantics **6/6**, 0 failed/ignored; durations 0.19s /0.38s, compile0.59s. Cargo and relevant shared-source pause released promptly before this evidence update. No extra broad rerun/native source claim. New module/relations/test frozen for independent review and Root/I2's separate contextual/capture-proof consumption.

The consuming once-read correction projection now makes these schema-readable A15 subset eligibility checks visible; it does not count/admit A15, establish full RS conformance, verify captured people/bytes, repair a library, or prove registration. Raw nonconformant/incomparable sources and all native evidence limits remain readable. Existing five CI-12 order/identity/ambiguity controls passed unchanged. No file/recordId/timestamp ordering was introduced as human chronology.

- `projects/chirality-app-v4/app/src-tauri/src/record_semantics.rs` SHA-256 `dc56618b97a9938f1e53ff1242fdb92c9bd6af1955ad02bb1ce7152ed255ec9f`
- `projects/chirality-app-v4/app/src-tauri/src/record_relations.rs` SHA-256 `21352b5d151d1a2a5e1357f981227c9535c68960c46cc534c822ba9db0a1d011`
- `projects/chirality-app-v4/app/src-tauri/tests/record_semantics.rs` SHA-256 `cef2d98bd1f60d342d54ff7997779c35400b9c8955d8f690e99d987c45514d0d`
- `/tmp/chirality-i3-a15-reader-tests.initial-failure.log` SHA-256 `75a24701a3866012e233b4f3943e7b858041a25c4bfe1878fd2b3323b086c2cd`
- `/tmp/chirality-i3-a15-reader-tests.log` SHA-256 `afc74ef19072abd8f319cc76e7ddfa73a8d9fe3ed0c79f2d64390d58ad0bed48`
