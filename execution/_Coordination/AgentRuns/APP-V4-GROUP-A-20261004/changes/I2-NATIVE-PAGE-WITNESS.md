# I2 native accepted-page observation witness

2026-10-05. TASK `/root/group_a_execution/runtime_integration`, parent WORKING_ITEMS `/root/group_a_execution`; no delegation. **Frozen source/test prerequisite; independent review pending.** Own only `native_history.rs`, new `tests/native_page_witness.rs` and this run packet. No Host/runtime_session/lib/UI, operational admission, resume, auth/recovery, SDK/schema/resource/dependency, durable/cache/transcript, native/model/network or Git mutation.

## Recovered seam and actual concurrence

Recovered current NativeHistory source, existing native_history/history_integration tests, I1-HISTORY.md and actual HistorySession reconcile usage. Existing query acceptance is typed owner/factory + selected home/full generation + selection epoch + latest logical stream revision; full maintained0.160 SDK response validation and thread/turn relational checks happen before page mutation. Only its transient latest Selection.items_page stores raw result. Original read-only receipt does not authenticate actual transport or enable operational use.

Before mutation, Core and WR each explicitly concurred with the exact borrowed accessor/API and refusal semantics. Core confirmed compile-coherent stationary Host/recovery/auth source for this short Cargo run, then was explicitly released. Core owns the separate final private Host mint: actual written/correlated SourceRequest/HistoryDispatch, native RPC/reference, full generation, exact native query/params and the SAME received raw result, current ready/open source and all current Root/home/selection epochs. WR concurred it must consume that resulting private capability, never this accessor alone or a public receive DTO as authentic native/active/A15 proof.

## Frozen API and bounded behavior

`pub(crate) fn NativeHistory::accepted_items_observation<'a>(&'a self, query: &HistoryQuery) -> Result<AcceptedItemsObservation<'a>, String>`.

Witness is crate-private, has private fields and no public constructor, Deserialize, Serialize or Clone. Borrowed getters:

- `query() -> &HistoryQuery` retains exact owner query; existing getters supply query ID, home/full generation, method and native params including thread/turn/cursor/direction.
- `owner_instance() -> u64`, `selection_epoch() -> u64`, `stream_revision() -> u64` expose local correlation metadata only, not authority or supplier RPC IDs.
- `stream() -> &str` is exactly `item-pages`.
- `page() -> &Value` borrows the existing transient Selection.items_page; no transcript duplicate or durable store.

Only latest successfully accepted Items receipt captures typed query/epoch/revision metadata. Access checks closed/home/full-generation/factory/method, exact accepted query, selected thread and current selection/stream revision; current item-stream pending/error refuses. Preparing a newer query immediately withholds the prior witness. Waiting, failed/malformed/foreign reply or native error never promotes a prior page to current evidence. Existing prior raw page remains visible as last observed; refusal is explicit unavailable/stale, not missing history, changed bytes or tamper. A superseded old pending query does not mask a newer accepted page. Other stream operations retain their existing meanings and do not revoke an unrelated accepted item stream merely by being pending.

Selection replacement and generation closure remove metadata with the existing selected page. SDK validation, opaque/missing/null cursor behavior, page replacement, known-turn restrictions, Continue and read-only-versus-operational standing are unchanged. Read-only `receive` remains callable with synthetic input: its acceptance can never prove supplier authenticity. No public ScopedItemsPage, serde proof DTO, test-source proof constructor, active registration or reserved act is added.

## Actual verification and source freeze

Parent's exclusive grant; Core's explicit stationary-source concurrence. Exact command from repository root:

```sh
CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home CHIRALITY_SKIP_CODEX=1 cargo test --offline --locked --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml --test native_page_witness --test native_history --test history_integration
```

Exit **0**, compile8.68s, **5/5 new witness**, **13/13 unchanged native_history**, **7/7 existing history_integration**, 0 failed/ignored. Test durations0.23/0.24/0.25s respectively. Cargo and Core stationary-source hold released immediately after actual results, before this record. No initial compilation/test failure. Dead-code warnings remain visible for the not-yet-consumed private accessor in production and broader unused APIs in source-import tests; no warning suppression or unrelated cleanup.

Meaningful new controls: exact query/metadata/native-extra/raw text preservation and pointer-equal borrowed existing page; newer opaque cursor pending→waiting→error retains prior raw view but refuses witness, later accepted empty/null-cursor tail restores current witness; foreign factory/home/full generation, malformed SDK payload and wrong turn reject before witness; reselect and close refuse; old superseded pending result cannot mutate/block latest acceptance, unrelated goal remains independent. Existing thirteen native-history and seven connected HistorySession/Host-double tests preserve prior Continue/unknown/selection/error behavior. No live transport, native window, model, credential or real-home witness.

## Custody and exact bytes

`probes/NATIVE-PAGE-WITNESS/native_history.rs.before` and PREIMAGE.sha256 preserve this task's actual pre-edit source, not historical owner custody. SOURCE_SEALS.json pins frozen owned files. Core/Host genuine provenance mint and WR consuming supply check remain next independently reviewed work, not implied by these synthetic tests.

- `projects/chirality-app-v4/app/src-tauri/src/native_history.rs` — `5d9a268639399ff70e44b9217c2a317986ddc653d4684e64f40af6acd77922ab`
- `projects/chirality-app-v4/app/src-tauri/tests/native_page_witness.rs` — `6bc02752d0cf33b09116fc15ac90f1c9bfc72b8040cf6f534299c7ab7660ebf0`
