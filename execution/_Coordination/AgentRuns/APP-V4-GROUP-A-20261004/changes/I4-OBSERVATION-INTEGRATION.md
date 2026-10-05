# I4 supplied-observation App integration — bounded source/test unit

2026-10-05. TASK `/root/group_a_execution/runtime_integration`, parent `/root/group_a_execution`, delegated-harness-native descendant, supplied gpt-6.1-sol/medium, no descendants. Production base `38bb2bc87a`. Write ownership: lib.rs, App.tsx, runtime_session.rs, new tests/external_observation_integration.rs and this note. No source/body/Design/schema/dependency/credentials/account/model/Git changes outside that boundary. The earlier authorized I1 evidence appendix is separately retained.

## Basis and serialization boundary

Consumes independently READY `V2-I4-OBSERVATION-R1` at its exact ExternalObservation/Catalog/receiving seals. Read C §2.1 CI-1/CI-3, §5.2 and §6.1 RR-1…4, ADAPTER §4.3 RD-1…3, PANEL §4 H-5/H-6 and the source API. Root/TASK/v4 LOOP/manually identified entry basis was retained from I1; no App v3 loop/profile applied. The contract's receiving/provenance limits are preserved; this source projection does not establish a real host catalog, its origin or current currency.

The manager briefly paused this unit to finish the I1 report seal. All partial I4 bytes were preserved in a scratch snapshot/patch; exact prior I1 lib/session/App/runtime-test seals were restored and checked. After the manager received final V3-I1-INTEGRATION READY, its reviewed bytes were separately preserved in run evidence/I1-V3-reviewed and this partial work was restored only after matching the exact base hashes. Historical I1 report/snapshots were not overwritten. This candidate's source hashes below equal the actually restored partial-work hashes; no source change followed the completed checks.

## Native selector → receiving → main-memory → display

`lib.rs` exports only needed catalog, receiving and external_observation core modules and registers `select_external_observation` with **no IPC arguments**. The main process opens native JSON file pickers for catalog/read, then a native explicitly labelled optional-counterpart choice and picker. Renderer-supplied paths, host identity/origin or source bytes are not accepted by that command. It converts the returned FilePath to its local PathBuf without lossy string conversion; non-local selected URLs refuse visibly. Display strings never feed file reopening, file identity or comparison.

`runtime_session::ExternalObservationSession` retains one reviewed `ExternalObservation` in memory. `receive_external_selection` is the production selection/receiving flow; native command closures supply real pickers, while unit tests explicitly inject typed scratch selections. It serializes reentrant selection, reads through ExternalObservation only after the required selection is complete, and exposes selection state plus the complete original receiving snapshot. Cancel/error at catalog/read/optional-counterpart retains the previous observation and reports its stage/reason; choosing “No counterpart” explicitly commits a primary observation with counterpartSelection=not-requested. Per-document malformed/invalid/unavailable assessments stay distinct inside the returned observation rather than becoming successful host reads. No file contents, event or selection proof is written to App records.

`host_status.externalObservation` returns `{selection, observation}` from main-process memory. Window reload can read that same memory state; no content survives App process relaunch by this mechanism. Selection does not depend on a supplier account/model/ready state and does not reinterpret supplier events or call a host dispatch operation.

`App.tsx` places an independent supplied-observation panel and invokes the native selector **without paths or other arguments**. Its post-selection refresh calls only read-only host_status, not decision_view's recorder-continuation path. Each supplied catalog/read/counterpart displays assessment/reason, displayPath text, visible pathDisplayLimit, authoritative selectedPath tagged native bytes/code units, complete original JSON and original bytes. Complete tables/rows/columns/units, basis, diagnostics/attachments, results and standing remain in the original document; there is no filtered/strengthened model summary. The complete receiving snapshot is also inspectable.

The panel labels provenance “person-supplied document; host origin unverified”, qualification not established and currency “as reported in this observation”. Comparison is scoped to supplied_documents_only; a missing counterpart explicitly says comparison not established. Same meaningful supplied content never becomes verified host equivalence. Dispatch remains none; no model/native-event remapping, endpoint discovery, network, act capture or durable copy is introduced.

## Checks and exact limits

Serialized manager-approved command: `CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home cargo test --offline --test external_observation_integration --test runtime_integration`. Compile exit 0, **4/4 new connected checks** pass (0.12 s), **10/10 affected I1 checks** pass (0.17 s), overall exit 0. Cargo slot returned immediately after completion. New checks run the actual selection-port→reviewed receiving→main-memory snapshot flow for full source content/bytes/path identity/standing and missing comparison; same-content optional counterpart; cancellation/error retaining prior bytes; unavailable non-Unicode selected-path identity/lossy limit; malformed bytes and reentrant selection refusal. Source-file changes after receipt do not rewrite the main-memory result. Tests use unique scratch files and synthetic callbacks, then remove them; no native selection event is asserted.

Transient SSR uses the actual App.tsx component bundled with ReactDOMServer and explicitly stubbed native IPC. Exit 0. It asserts the entire original catalog/read pretty JSON is rendered, including table/basis/diagnostic/standing content, exact tagged selectedPath, visible lossy pathDisplayLimit, unverified provenance/reported currency, missing comparison and cancellation retaining prior content. The script/executable were temporary and removed; reconstructible source and output remain in the tool history. Frontend `node_modules/.bin/tsc --noEmit`: exit 0. Diff whitespace check: passed.

This evidence is connected source/file-mechanics/static rendering, not a physical native picker/window/cancel journey, native IPC event submission, real external host origin/currency or qualified non-Unicode picker/platform behavior. Windows/fallback path encoding remains source-reviewed. No supplier process/model turn/authentication/account/credential/network/download/Git operation was exercised by this unit. Independent complete-glue review remains required before fan-in.

I1's open userVerification device-proof acceptance and Codex history reconstruction remain explicitly unfinished. Reviewed v4 instruction defaults and existing P0 native capture/identity/observer behavior are retained with affected tests. Ledger startup is intentionally unchanged/not adopted: product RT mapping adoption/backcheck and named manager startup unit remain prerequisites; no initialization success or full recovery is claimed. No retention/deletion choice or alternate ledger store was introduced. This is a bounded supplied-document path, not whole I4/Group A completion, acceptance, qualification or release.

## Frozen integration candidate

| Project-relative file | SHA-256 |
|---|---|
| `app/src-tauri/src/lib.rs` | `8b89d0035a3031b63adb0f99ea769a10ef63d804b48eca04deb87f2eca598632` |
| `app/src-tauri/src/runtime_session.rs` | `8ac9ff2cc93362f0f1a0379eb68667d241207eea780db698b77c01e1fd79d964` |
| `app/src/App.tsx` | `a6901699fb62c49f2ae1de1c33d375b37af819ffd4b6c810c1e2a2310de0913f` |
| `app/src-tauri/tests/external_observation_integration.rs` | `1a59b14714d7be5a200d2848a0b15b71c8f71dea27b330659e2741548221eae8` |
| `app/src-tauri/tests/runtime_integration.rs` | `18ed6496863eb76cc950c96e162ddb955139a92d776a313c3a9e7a4591195ee2` |

## Read-source origins

| Repository-relative origin | SHA-256 |
|---|---|
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V2-I4-OBSERVATION-R1.md` | `239c214c8ce4c873888dd3aaad30e428f75537134277fc7acc739f4d79a3f751` |
| `projects/chirality-app-v4/app/src-tauri/src/external_observation.rs` | `1d93deb47887962f796ad3c25e4a42e85be51d45f8e9fab5d1683e40c87d7388` |
| `projects/chirality-app-v4/app/src-tauri/src/catalog.rs` | `ded4f3834ed72cca8f5b8a6ff5b4b8ec041ada00ee68967605c3b6897894d6e2` |
| `projects/chirality-app-v4/app/src-tauri/src/receiving.rs` | `3ae79a4eaff1a9c70477f6155be17bb14269ec21ccd70065391b50389d5346eb` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-01_Capability catalog and read-basis contract/Design/CATALOG_AND_READ_BASIS.md` | `4b5f43011eb276df923377cd0d79e0accaf65afba624814753c5612007412431` |
| `projects/chirality-app-v4/execution/PKG-03_Host capability and operation contracts/1_Working/DEL-03-03_Local external-agent receiving adapter/Design/ADAPTER_ENABLEMENT_AND_RECEIVING.md` | `eed1d912df333822c172593ea81a244661dab305b81c6295493802f252eda761` |
| `projects/chirality-app-v4/execution/PKG-05_Embedded-host receiving integration/1_Working/DEL-05-02_Host panel and shared interaction receiving/Design/PANEL_RECEIVING_CONTRACT.md` | `4898b6f80832b3baae9fd7e2e24e2fe6141a0d2b12359f1c0dce5647ccee6999` |
