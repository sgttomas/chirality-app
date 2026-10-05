# V2-I4-OBSERVATION-R1 — same-reviewer native-path repair backcheck

2026-10-05. **READY for bounded supplied-document observation fan-in at the successor hashes below. OBS-1 is repaired; no unresolved blocking, major or minor finding in this backcheck.** Original V2-I4-OBSERVATION remains unchanged and historical. This does not qualify a native file-selection/UI journey, real host origin/currency, valid non-UTF-8 filesystem support, another platform, or whole I4/Group A completion.

Same independent TASK `/root/group_a_execution/p0_integration_review`, delegated-harness-native child of WORKING_ITEMS `/root/group_a_execution`, supplied Codex gpt-6.1-sol/medium; no descendants/substitution/diversity claim. Retained software-code-review/C/ADAPTER/LOOP/PANEL basis from the original review. Own durable write only this report. Read current full observation source, added tests and successor change account; checked exact hashes and unchanged Catalog/receiving source identities. No unrelated source or selector/UI review.

## Repair and independent checks

DocumentEvidence no longer serializes PathBuf through serde. selectedPath is a tagged lossless native identity: Unix byte array, Windows UTF-16 code units, or explicitly platform-tagged native encoded bytes on other targets. The exact internal PathBuf remains the source of file reads; displayPath is separate. Non-Unicode display carries an explicit lossy limit; ordinary Unicode display has no such limit. This is App projection metadata, not a host identity-method or wire change.

Manager authorized rustc-only scratch verification. Reused the original exact unavailable `read-<ff>.json` typed input, changing the symptomatic panic assertion to the required successful snapshot/native-byte/display-limit oracle. Compile exit 0 and focused test exit 0: **1/1** passes with exact native bytes, retained unavailable/no-bytes account, marked lossy display and successful full JSON serialization. Independently ran the successor's normal `résultat-Δ.json` temporary-file control in the same compiled harness: exit 0, **1/1** passes; exact native path identity and Unicode display, no lossy limit. Each run filtered nine unrelated tests. No Cargo or shared target modification occurred.

Harness names retain the original symptomatic name to preserve derivation; assertions now test conformity. Author reports nine focused offline cases passing (eight observation tests plus included AAC setup), 0.13s; this broader run was not repeated by this reviewer. Original ordinary custody/provenance/complete-content tests remain, with the two path regressions added. Catalog and receiving modules are unchanged at their V2-I4-R1 identities. Source hashes match before and after checks. Windows/fallback encoding is source-reviewed only, with no independent target-platform execution claimed.

The prior current-host EPERM when attempting to create a non-UTF-8 file remains historical setup evidence. This repaired metadata reproduction neither creates that file nor establishes an actual native selection event. The normal Unicode temporary-file check demonstrates the receiving code's file mechanics, not native UI custody or actual host origin.

## Consumer obligations and preserved scope

Upcoming native-selector/command/UI integration must render displayPath as text, show pathDisplayLimit when present, and retain selectedPath's tag/native bytes or code units as authoritative identity. Never derive reopening, comparisons or identity from the lossy display string or treat the new object as the old scalar selectedPath. Internal selected_path() remains exact. This binding requirement is necessary for the repaired receiving result to remain truthful.

Complete original documents/bytes, invalid/unavailable reasons, catalog/basis binding and optional supplied-counterpart comparison retain the original reviewed semantics. Snapshot provenance remains person-supplied/host-origin-unverified; qualification remains not established, currency remains as reported, and dispatch remains none. No durable copy, network/dispatch/native-event remap, act, account/model choice or host verification upgrade was introduced.

Native selector→command→main-state→complete visible UI is still manager-owned and unreviewed here. Actual host/source/native qualification and full I4 integration remain required at their own points of use. No stage gate, acceptance, release or whole-Group-A claim follows.

No product/Design/shared-test/instruction/Git edits, download/network, credentials/authentication, live model/supplier/native process or human/lifecycle act occurred. Scratch harness/executable and test workspace were removed after reconstructible evidence was retained; only this review is durable.

## Exact successor and preserved identities

| Repository-relative path | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/external_observation.rs` | `1d93deb47887962f796ad3c25e4a42e85be51d45f8e9fab5d1683e40c87d7388` |
| `projects/chirality-app-v4/app/src-tauri/tests/external_observation.rs` | `255b1a0bdfee4a1a4cb09625da771da006c606b32e73f317a3ddeb30ba858a3d` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I4-OBSERVATION.md` | `6aa6370941185a761c0f64c3ab3f7da18e466dc5cd22508f9e449fb4fde97e47` |
| `projects/chirality-app-v4/app/src-tauri/src/catalog.rs` | `ded4f3834ed72cca8f5b8a6ff5b4b8ec041ada00ee68967605c3b6897894d6e2` |
| `projects/chirality-app-v4/app/src-tauri/src/receiving.rs` | `3ae79a4eaff1a9c70477f6155be17bb14269ec21ccd70065391b50389d5346eb` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V2-I4-OBSERVATION.md` | `8f19d405c5fad2bace336187003768bd6d07a4adc20b9fa33c47f1feed36bbf7` |

## Reconstructible focused harness

SHA-256 `4fd97a227b78a730592519ec16ac6eb6a89e90b41d1a5b70552bbc3062b68cdd`. Use the successor tests/external_observation.rs hash above, replace ../src source-inclusion paths with their absolute same-checkout src-tauri/src paths, append the exact block below. Compile with the original review's rustc/dependency command and CARGO_MANIFEST_DIR; unchanged extern serde_json `libserde_json-285cf9e31e3ede2e.rlib`, jsonschema `libjsonschema-fb435d8f662f1e55.rlib`. Run filters `reviewer_ --nocapture` and `normal_unicode_selected_path --nocapture` separately.

```rust

#[test]
fn reviewer_non_utf8_selected_path_retains_read_but_snapshot_panics() {
 use std::os::unix::ffi::OsStringExt;
 let files=Files::new();let mut selected=files.selected(&fixture("read_result.example-valid.json"),None);
 let name=std::ffi::OsString::from_vec(b"read-\xff.json".to_vec());
 let exact_path=files.0.join(name);selected.read=exact_path.clone();
 let state=ExternalObservation::load(selected);
 assert_eq!(state.read_evidence().assessment(),"unavailable");assert!(state.read_evidence().original_bytes().is_none());assert_eq!(state.read_evidence().selected_path(),exact_path);
 let result=std::panic::catch_unwind(||state.snapshot());assert!(result.is_ok()); let view=result.unwrap(); use std::os::unix::ffi::OsStrExt; assert_eq!(view["read"]["selectedPath"]["encoding"],"unix_bytes"); assert_eq!(view["read"]["selectedPath"]["bytes"],json!(exact_path.as_os_str().as_bytes())); assert!(view["read"]["pathDisplayLimit"].as_str().unwrap().contains("lossy")); assert_eq!(view["read"]["assessment"],"unavailable"); serde_json::to_vec(&view).unwrap();
 println!("same unavailable read-[ff].json input: exact path bytes retained; lossy display marked; snapshot serializes");
}
```

Observed original-input output: same unavailable read-[ff].json input: exact path bytes retained; lossy display marked; snapshot serializes. Original-input and Unicode control each pass 1/1, no native event or valid non-UTF-8 file witness.
