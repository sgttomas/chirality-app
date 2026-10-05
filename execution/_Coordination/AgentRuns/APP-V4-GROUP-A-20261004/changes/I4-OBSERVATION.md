# I4 external observation consuming state — 2026-10-05

TASK `/root/group_a_execution/catalog_adapter_production`, parent `/root/group_a_execution`, native delegated descendant, no delegation. Bounded App main-process input receiver; shared lib/UI integration stays with sole owner `runtime_integration`. Reviewed V2-I4-R1 core stays frozen.

## Produced boundary

New `app/src-tauri/src/external_observation.rs`: `ExternalObservation::load(SelectedPaths)` reads each caller-native-selected catalog/read/optional counterpart path once, keeps exact bytes and parsed complete documents in memory, validates with existing Catalog/BoundRead, and returns complete source data plus display account. `snapshot()` marks provenance "person-supplied document; host origin unverified", qualification not established, reported currency "as reported in this observation", basis citation assessment, limits and optional supplied-document comparison. Missing counterpart is explicit; an invalid/unavailable counterpart is not same-content. Malformed/invalid claims retain raw bytes/reasons; unavailable reads retain the I/O reason without invented bytes; invalid catalog leaves the dependent read unassessed with prerequisite-unavailable reason. Valid host non-success stays non-success. Replacing a file later never updates the retained state.

No durable copies, dispatch, host enablement, native event remapping, host identity minting, account/model choice, network, act capture, one-effect or real-host qualification. Caller must pass paths from the actual native selector; this pure receiving entry does not prove a selection event occurred. These files do not yet create a UI journey; manager must integrate file selector → command → main state → complete visible tables and raw rejected inputs.

## Exact contract basis

C §2.1 CI-1/CI-3: supplied catalog edition/host identity/completeness/basis profile. C §5.2 rules 1/3/6 and §5.5: basis completeness and immutable host-supplied identities; App exact-byte identities do not establish host identity. C §6.1 RR-1…RR-4: complete tables, results, diagnostics, attachments and standing without upward summary. ADAPTER §4.3 RD-1…RD-3: complete read/basis and standing from host result. ADAPTER §4.1 NM-1…NM-3: future native event mapping needs host-provided catalog identity/version mapping; this intake creates none. PANEL §4 H-5/H-6: no invented domain truth, references retained and meaningful views/standing carried. LOOP §2.2 TL-1 / §6 O-3: future actual tool path must keep offered edition/version and cannot synthesize catalog operations from Codex tool events. Current import is only supplied-document reception and comparison.

## Connected checks

New `tests/external_observation.rs` drives actual selected temporary files through load and snapshot: complete original data and diagnostic attachment preservation; exact-byte custody after file replacement; counterpart same/different/missing; malformed JSON/non-UTF8/schema-invalid/domain-invalid bytes; unavailable file; invalid catalog prerequisite; invalid counterpart; valid unavailable host result; incomplete basis and missing lineage limits. Explicit invented diagnostic additions and host counterpart documents test receiving mechanics, not new host observations. No new fixture copies needed. Exclusive manager-granted Cargo check completed: `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home cargo test --offline --locked --test external_observation`, actual exit **0**, **7 passed / 0 failed / 0 ignored**, 0.12s (six observation tests plus included AAC setup test). Cargo slot released promptly. No code repairs or criterion changes needed after this run. Source frozen for independent review.

## Consulted origins (read-only)

- `projects/chirality-app-v4/app/src-tauri/src/catalog.rs` sha256 `ded4f3834ed72cca8f5b8a6ff5b4b8ec041ada00ee68967605c3b6897894d6e2`
- `projects/chirality-app-v4/app/src-tauri/src/receiving.rs` sha256 `3ae79a4eaff1a9c70477f6155be17bb14269ec21ccd70065391b50389d5346eb`
- `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/CATALOG_AND_READ_BASIS.md` sha256 `4b5f43011eb276df923377cd0d79e0accaf65afba624814753c5612007412431`
- `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Design/ADAPTER_ENABLEMENT_AND_RECEIVING.md` sha256 `eed1d912df333822c172593ea81a244661dab305b81c6295493802f252eda761`
- `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-01_Minimal-loop and model receiving contract/Design/LOOP_RECEIVING_CONTRACT.md` sha256 `2bac33a883b176e24cd17e6fb78361efea63ce4c254810dcf8ab6e1d13cd7004`
- `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-02_Host panel and shared interaction receiving/Design/PANEL_RECEIVING_CONTRACT.md` sha256 `4898b6f80832b3baae9fd7e2e24e2fe6141a0d2b12359f1c0dce5647ccee6999`

## Frozen produced identities

- `projects/chirality-app-v4/app/src-tauri/src/external_observation.rs` sha256 `b18b8740c3e052c918b7beb889af61fe70e87ab6648d13b71c9f1114c1e0d58c`
- `projects/chirality-app-v4/app/src-tauri/tests/external_observation.rs` sha256 `bb96445cb023381c328ca3b3dd69ec6eae3b0ba4877b114b7587323c4fb7b98f`

## Original-owner native-path repair — source ready, check pending

Manager returned an independent repro: `json!(PathBuf)` panics on Unix selected filename `read-[ff].json`, even when the read is unavailable. Original candidate hashes/receipt above remain historical and unchanged; this is a successor. No supplied schemas, core receiving modules, review, fixtures, shared lib/UI or Design modified.

`DocumentEvidence::snapshot()` now carries `selectedPath` as tagged lossless native identity (`unix_bytes` with byte array; `windows_utf16` with code-unit array; other targets preserve tagged platform-native encoded bytes). `displayPath` is separate. A non-Unicode native path explicitly marks `pathDisplayLimit` as lossy display and points to native identity. Native PathBuf stays exact internally; display is never used for reading, identity or document validation. Normal Unicode paths have no display limit. This changes the new App projection only, not a host wire or identity method.

Two regressions added: exact unavailable `read-[ff].json` metadata/whole-snapshot serialization with raw path-byte assertions and no document/currency/readiness upgrade; normal `résultat-Δ.json` file control with exact native identity and display. The non-UTF8 file is not created: reviewer reported its valid-file creation was host-denied, and neither this metadata repro nor the Unicode temporary-file control establishes a native selection witness. Actual selector/command/UI integration stays with `runtime_integration`, which must display `displayPath` and preserve `selectedPath` separately. Cargo slot requested before testing.

### Native-path successor frozen verification

`CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home cargo test --offline --locked --test external_observation`: actual exit **0**, **9 passed / 0 failed / 0 ignored**, 0.13s. Eight observation tests plus included AAC setup test. Exact unavailable Unix byte-path regression and ordinary Unicode control passed. Cargo slot released. No native valid non-UTF8 file or actual selection witness supplied. Source frozen for independent backcheck.

- `projects/chirality-app-v4/app/src-tauri/src/external_observation.rs` sha256 `1d93deb47887962f796ad3c25e4a42e85be51d45f8e9fab5d1683e40c87d7388`
- `projects/chirality-app-v4/app/src-tauri/tests/external_observation.rs` sha256 `255b1a0bdfee4a1a4cb09625da771da006c606b32e73f317a3ddeb30ba858a3d`
