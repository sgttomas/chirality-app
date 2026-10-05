# V2-I4-OBSERVATION — independent bounded supplied-document review

2026-10-05. **NOT READY for snapshot-input fan-in until one blocking P2 robustness defect is repaired.** No major semantic defect or other minor finding identified in the new ordinary file→memory→snapshot path. The existing I4 warrants remain bounded and unchanged; UI/native-selector/command wiring is not implemented or reviewed here.

Independent TASK `/root/group_a_execution/p0_integration_review`, delegated-harness-native child of WORKING_ITEMS `/root/group_a_execution`, supplied Codex gpt-6.1-sol/medium; no descendants or model substitution/diversity claim. Applied retained software-code-review and C/P/ADAPTER/LOOP/PANEL source basis from V2-I4/R1. Read complete frozen external_observation.rs/tests and I4-OBSERVATION.md; traced Catalog/BoundRead/compare_panel callers against their unchanged reviewed behavior. Write only this report; no blanket I4/P0/I1/I2 review. Supplied output hashes match before and after checks.

## Finding

**OBS-1 [P2, blocking] A non-UTF-8 supplied PathBuf panics during snapshot instead of preserving the unavailable observation.** `app/src-tauri/src/external_observation.rs:48`, DocumentEvidence::snapshot's `json!` serialization of self.path. Trigger: SelectedPaths includes a Unix filename with byte 0xff (the precise synthetic basename is `read-<ff>.json`). `load` accepts the PathBuf, reads it unsuccessfully and retains assessment=unavailable, absent bytes and its I/O reason. `snapshot()` then serializes PathBuf through serde_json; serde refuses non-UTF-8 paths and json! unwraps that error, panicking with “path contains invalid UTF-8 characters”. The same serialization is used for catalog/read/counterpart metadata.

Impact: a bounded supplied input which already has a truthful unavailable assessment cannot produce the promised complete observation snapshot. A future command boundary can lose its response rather than returning the source/account; a native selector's actual path encoding must not silently become an authoritative lossy path string. The current code imposes no UTF-8 admission constraint on its PathBuf API.

Repair: safely and explicitly represent exact non-UTF-8 native path bytes with an encoding/disclosure, or refuse unsupported path encoding at the actual selection/admission boundary with retained exact path evidence. Avoid panicking json! and avoid labelling a lossy display spelling the exact selected path. Preserve ordinary UTF-8 output compatibility, original bytes/parsed documents, the unavailable I/O reason and unverified standing. Add a non-UTF-8 unavailable-path snapshot case; where the target filesystem supports it, add an actual selected existing-file case without pretending the current host demonstrated that support.

## Independent reproduction and its limits

Manager authorized a rustc-only scratch harness. Compilation against existing cached serde_json/jsonschema succeeds (exit 0). Focused corrected test exit 0; one symptomatic assertion confirms snapshot panics, with seven unrelated tests filtered. It asserts the defect, not conformance. The exact retained source and filename bytes are recoverable below.

An initial supplemental test attempted to rename the ordinary synthetic read file to the non-UTF-8 basename. Current host returned EPERM/Operation not permitted at setup, before product load/snapshot. That test failed at preparation; it supplies no valid-file or native-selector witness. The corrected reproduction passes the exact non-UTF-8 PathBuf as an unavailable selected input and directly exercises product retention and snapshot serialization. No arbitrary user content, real native selection event or another platform's filesystem behavior is claimed. The distinction does not remove the verified panic at the accepted PathBuf/snapshot boundary.

No Cargo/shared target mutation occurred. Temporary test/executable and invented file workspace were cleaned; only this report is durable. No download/network, credentials/authentication, supplier/model/native process, product/Design/test/instruction/Git changes or host effect occurred.

## Semantic assessment and retained warrants

Each selected file is read once into exact retained bytes. Parsing/validation may run on those same bytes but rereads no file. Later file replacement cannot change the in-memory observation. Malformed/non-UTF-8 content, invalid schema/domain and unavailable files retain raw evidence or explicit absent bytes/I/O reason rather than invented contents. Invalid catalog leaves dependent well-formed reads unassessed with prerequisite-unavailable; original content remains visible.

Successful reads use the reviewed catalog edition, operation/version, exposed surface and basis/profile semantics. Valid non-success results remain source non-success observations, not empty successes or citable bound reads. Original complete source documents, meaningful tables/results/diagnostics/attachments/standing and raw bytes are returned; no upward summary replaces them. Basis citation is complete only **as supplied**, with explicit incomplete/no-lineage limits; it is not proof of host origin or current host state.

The optional counterpart uses the same catalog receiver and reviewed comparison of host/operation/edition/basis/views/standing. Same/different labels are explicitly scoped to supplied documents, not actual host UI parity. Missing/invalid/unavailable counterparts do not become same-content. Snapshot top-level provenance remains person-supplied/host-origin-unverified, qualification not established, reported currency only as reported in this observation and dispatch none.

There is no durable copy, network/dispatch path, native-event mapping, host identity minting, enablement, act, one-effect or model/account choice. The selected-path type itself does not prove a person performed the selection; actual selector custody and complete visible UI rendering remain manager integration work. Imported BoundRead.citable must never be promoted to verified actual host/native admission by future consumers.

Author's I4-OBSERVATION record reports seven offline tests passed (six observation tests and included AAC setup), 0.12s. Read test source covers complete document/diagnostic preservation, post-load replacement, counterpart variants, invalid content/operation version, unavailable/prerequisite states, non-success and incomplete/no-lineage limits. This is author evidence, not a repeated reviewer full suite; it omits OBS-1. Existing catalog/receiving source hashes remain those independently reviewed in V2-I4-R1. No source/schema/example oracle changed.

Return OBS-1 to the original observation producer for repair/backcheck. Keep native-selector→command→main-state→complete UI path and actual host/source qualification as explicit unfinished receiving work. No whole-I4, Group A, gate or release claim follows.

## Exact frozen identities

| Repository-relative path | SHA-256 |
|---|---|
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I4-OBSERVATION.md` | `f11e9512a1c23bbbb9422db7de5a1eb8eedfd3afb0d4063250b905866882607c` |
| `projects/chirality-app-v4/app/src-tauri/src/external_observation.rs` | `b18b8740c3e052c918b7beb889af61fe70e87ab6648d13b71c9f1114c1e0d58c` |
| `projects/chirality-app-v4/app/src-tauri/tests/external_observation.rs` | `bb96445cb023381c328ca3b3dd69ec6eae3b0ba4877b114b7587323c4fb7b98f` |
| `projects/chirality-app-v4/app/src-tauri/src/catalog.rs` | `ded4f3834ed72cca8f5b8a6ff5b4b8ec041ada00ee68967605c3b6897894d6e2` |
| `projects/chirality-app-v4/app/src-tauri/src/receiving.rs` | `3ae79a4eaff1a9c70477f6155be17bb14269ec21ccd70065391b50389d5346eb` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V2-I4-R1.md` | `7038b35762c8736d7210044b14e4e0b1b91b22767e1d456c6aadfe13b456ed89` |

## Reconstructible focused harness

Final harness SHA-256 `040b08c49c4d0a19fd59860a12f59ab1bc800f2af458fc8ca6fcf70b97735891`. Start from the exact external_observation.rs **test file** hash above, replace source-inclusion `../src/<name>` paths with the absolute same-checkout src-tauri/src/<name> paths, then append this block. Compile with the earlier review's rustc --edition=2021 --test/dependency command, extern serde_json `libserde_json-285cf9e31e3ede2e.rlib` and jsonschema `libjsonschema-fb435d8f662f1e55.rlib`, CARGO_MANIFEST_DIR this src-tauri. Run `reviewer_ --nocapture`.

```rust

#[test]
fn reviewer_non_utf8_selected_path_retains_read_but_snapshot_panics() {
 use std::os::unix::ffi::OsStringExt;
 let files=Files::new();let mut selected=files.selected(&fixture("read_result.example-valid.json"),None);
 let name=std::ffi::OsString::from_vec(b"read-\xff.json".to_vec());
 let exact_path=files.0.join(name);selected.read=exact_path.clone();
 let state=ExternalObservation::load(selected);
 assert_eq!(state.read_evidence().assessment(),"unavailable");assert!(state.read_evidence().original_bytes().is_none());assert_eq!(state.read_evidence().selected_path(),exact_path);
 let result=std::panic::catch_unwind(||state.snapshot());assert!(result.is_err());
 println!("supplied unavailable selected filename bytes read-[ff].json; IO reason retained; snapshot panics");
}
```

Actual product panic: external_observation.rs:48, Result::unwrap on serde_json Error("path contains invalid UTF-8 characters", line 0, column 0). Final one symptomatic test passed, seven filtered. The function name is retained from the first preparation attempt; the exact final assertion clearly checks unavailable input, not a successfully read non-UTF-8 file.
