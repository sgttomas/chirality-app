# P0-VALIDATION-API — complete package and authoritative AAC validation

2026-10-04. TASK `/root/group_a_execution/runtime_schema_writer`, parent `/root/group_a_execution`, delegated-harness-native descendant, Codex gpt-6.1-sol inherited; no substitution/delegation. Parent brief supplies independently ready W1/CC-A/CC-P basis; no new acceptance inferred. Root resolved from active checkout. Prior entry/skill/manual readings and hashes are in P0-W1.md. Bounded follow-up owns schema_validation.rs, maintained schema resources/fixtures/sync/manifest, tests/schema_validation.rs and this record only. No records/lib/Cargo/act-control edits, Git mutation, download, network, authentication, credentials or supplier/model run. Parent reserves Cargo to act-control owner; no Cargo operation performed in this follow-up yet.

## Public API and implementation

```rust
pub fn validate_package(package: &serde_json::Value) -> Result<(), String>
pub fn validate_offer(offer: &serde_json::Value) -> Result<(), String>
pub fn validate_capture(capture: &serde_json::Value) -> Result<(), String>
```

Package is validated as the complete file against `chirality:del-02-03/exec-checkpoint-entry-bodies/proposed-0.7#/$defs/decisionPackageFile`; offer/capture against AAC's exact declared 0.3 IDs. Source interpretation, composition, authoritative custody and sequencing belong to caller; schema validation does not prove an actual person's act or source observation.

Shared internal `compile_targets` parses each schema, requires declared ID/dialect, rejects duplicates/missing required resources, registers by exact IDs with the rejecting retriever, eagerly builds every resource's reachable definitions with `build_map`, and builds target validators through absolute declared refs using `.offline()`. No URI rewrite or retrieval/fallback exists. `RecordValidator::from_resources` preserves core-four required-ID behavior and W1 entry validation; embedded `RESOURCES` now contains six resources. Cached act-route setup requires all six resources, including both AAC resources, and retains setup errors. All three APIs validate the object or return setup/validation failure.

Maintained canonical AAC resources and invented valid example files copied byte-for-byte. Added full valid package/offer/capture tests and negative tests for malformed nested package alternatives, missing package identity and extra property; missing A16 offer requestRef/malformed digest; capture person falsely verified/automation input/missing A16 requestRef. Private unit setup test rejects missing offer/capture, malformed AAC and unresolved HTTPS ref. Existing W1 tests retained. These tests are authored but not yet executed due exclusive Cargo slot; no passing claim made.

## Source verification and next checks

`python3 projects/chirality-app-v4/app/src-tauri/schemas/sync.py`, repository-root cwd, Python3.13.7, exit0: `6 schema resources match source bytes, hashes and declared IDs`. Helper now checks individual maintained AAC/package fixture bytes/hashes as well as concatenated RS fixture composition. No dated-run test dependency.

Required next checks when parent assigns Cargo slot:

```sh
CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home cargo test --offline --locked --test schema_validation --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml
CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home cargo test --offline --locked --lib schema_validation::tests --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml
```

Parent/act owner integrates APIs before package acceptance, offer presentation and capture persistence, checks connected flow and no mutation on refusal, and commissions independent frozen-diff review. No storage/ID/capture-retry implementation in this return.

## Canonical schema and fixture source mapping

| Maintained file | Source | SHA-256 |
|---|---|---|
| `aac.offer.schema.json` | `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/aac.offer.schema.json` | `f2091fcf2583b6863370ba51d86f4c8671dbae5bbd6fe0e39046154d98c7d066` |
| `aac.capture-evidence.schema.json` | `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/aac.capture-evidence.schema.json` | `4405a1228e5982d948eb82776aaaf54d966d4305f8829a656473a523ad1ca4ba` |
| `fixtures/aac.offer.example.valid.json` | `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/aac.offer.example.valid.json` | `f80957322793888d13e0c48c2cc312f91ff38b7cf6c60b622a103cb8cf7e967f` |
| `fixtures/aac.capture-evidence.example.valid.json` | `projects/chirality-app-v4/execution/PKG-01_Native App and third-party harness integration/1_Working/DEL-01-04_Native requests, outcomes and attachments/Design/aac.capture-evidence.example.valid.json` | `e086bdafb4d24c13f24e8fecee151bd803633294adc51d43ed16fe8523528da4` |
| `fixtures/decision-package-file.example.valid.json` | `projects/chirality-app-v4/execution/PKG-02_Workflow and role portability/1_Working/DEL-02-03_Workflow execution compatibility and round-trip support/Design/decision-package-file.example.valid.json` | `3ea08ff575698e769784e0c4788a21c01be81020ad0a3c0534114f5c87895fbe` |

## Frozen follow-up files

| Path | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/schema_validation.rs` | `8877920b116537a7f942a6b20cc1562ff302d7b16572c8b4632dd72d3cf62441` |
| `projects/chirality-app-v4/app/src-tauri/tests/schema_validation.rs` | `1022c3026430fc3d3c14f86adb29e021df99f0b5bc9973578f8d24cac22a6985` |
| `projects/chirality-app-v4/app/src-tauri/schemas/sync.py` | `65640c13b5540a756379bab7f39c01aa303df5521ec0f420ca00f0050ff36200` |
| `projects/chirality-app-v4/app/src-tauri/schemas/manifest.json` | `7c11acfe9f4088b1c4703970341df82ebe2fc23c9938458b8f636af623d2ead5` |
| `projects/chirality-app-v4/app/src-tauri/schemas/aac.offer.schema.json` | `f2091fcf2583b6863370ba51d86f4c8671dbae5bbd6fe0e39046154d98c7d066` |
| `projects/chirality-app-v4/app/src-tauri/schemas/aac.capture-evidence.schema.json` | `4405a1228e5982d948eb82776aaaf54d966d4305f8829a656473a523ad1ca4ba` |
| `projects/chirality-app-v4/app/src-tauri/schemas/fixtures/aac.offer.example.valid.json` | `f80957322793888d13e0c48c2cc312f91ff38b7cf6c60b622a103cb8cf7e967f` |
| `projects/chirality-app-v4/app/src-tauri/schemas/fixtures/aac.capture-evidence.example.valid.json` | `e086bdafb4d24c13f24e8fecee151bd803633294adc51d43ed16fe8523528da4` |
| `projects/chirality-app-v4/app/src-tauri/schemas/fixtures/decision-package-file.example.valid.json` | `3ea08ff575698e769784e0c4788a21c01be81020ad0a3c0534114f5c87895fbe` |
