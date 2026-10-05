# P0-ACT-R1 — ACT-1…8 repairs

2026-10-04. TASK `/root/group_a_execution/act_storage_propagation`, native delegated-harness child of WORKING_ITEMS `/root/group_a_execution`; no descendants. Parent explicitly commissioned V1-ACT repair and relayed root's cold-custody disposition plus V0-CUST READY. This is a successor implementation candidate; original P0-ACT.md and V1-ACT.md remain byte-frozen history. No new acceptance, seal adoption, authenticity qualification or scope reduction is claimed. No hosting, schema, Node-runner, shared graph/MEMORY, Git, network, credentials or supplier writes/execution.

## Repairs and checks

- **ACT-1:** private Rust `NativeCapture` memory is created only by the native confirm path. File capture/pending equality never creates that custody. Hot-process retry compares immutable actual captured facts, reserves/retains writer identity and appends only from that custody. Cold unverified captures retain bytes with exact visible `capture origin not verified; automatic act replay held`; they append no act. Exactly one complete matching existing RS record permits backlink repair only, with unchanged recorded-claim provenance. Reader/decision UI explicitly label native capture origin as unverified by this unsealed reader; no valid schema/backlink is promoted to verified native-human evidence. Regression places invented matching schema-valid capture/pending files directly and proves no log/act append or evidence mutation. Another orphan-capture case proves cold publication-before-submission cannot mint an identity or reissue the pending request. Existing cold recorded-claim repair remains covered. Persistent admitted original custody across process restart remains **unfinished**, pending the concrete owner seal/custody decision and witness; legitimate persistent replay is not waived or transferred to packaging.
- **ACT-2:** `create_json` writes into a unique owning-directory temporary file, fsyncs complete bytes, then atomically publishes with hard-link create-new semantics. It never overwrites prior evidence or exposes partially written final evidence. Newly created directory ancestry and the existing ancestor linkage are synced. Append and existing-match recovery sync files plus owning directory publication through project/library root. Backlink replacement uses complete synced temporary bytes and atomic rename; its sole added field remains recordId. Narrow test injection exercises partial temporary write (no final pathname), directory-sync failure after complete publication (no durability success), actual capture-directory failure before writer reservation, and existing-match log-directory failure holding the backlink. These are deterministic fault-path witnesses, not a physical process-kill/native OS-fault qualification.
- **ACT-3:** recorder and compose each read one immutable byte buffer, parse/full-validate it and calculate its identity from that same buffer. Every package/request/offer field comes from that snapshot. Confirmation performs its own single content-identity observation and rejects changed bytes. Controlled file replacement/alternating observed buffers verify body/hash and offered scope/purpose/identity agreement, retaining source-faithful mapping.
- **ACT-4:** writer-log reader detects first-sequence gaps, duplicates, gaps and out-of-order seq as completeness limits while preserving original entries/bytes. Append/recovery fail closed on those limits. Individually schema-valid seq [1,3], [1,1], [2,1] fixtures prove no new append/backlink. Partial/invalid/duplicate-record/disagreeing-capture checks remain intact.
- **ACT-5:** verified durable append remains **AC-7 recorded** when only the annotation fails, with `backlinkPending`, actual cause, and exact `act recorded; capture record link pending` detail. The UI includes these AC-7 pending annotations. Corrected oracle restores the reviewed contract: directory-permission backlink failure remains recorded; subsequent recovery changes only annotation and never appends an act. A complete matching durable claim permits opening a fresh native decision control despite a failed backlink; unrecorded original captures still hold reissue.
- **ACT-6:** writer pending submission keeps original observedAt/captureTime, writer-minted record ID and failure detail. Late write includes original observedAt and subsequent referenced `evidence_limit` `record write failed`. Hot pending batches preserve native-event order, append all delayed acts before their delay limits, and detect already-written limits to avoid duplicates. Tests cover original facts after package edits, cold hold followed by hot retry, exact observedAt/ID, one ordered late-entry/failure-limit pair, and a two-act/two-limit batch with repeat retry unchanged.
- **ACT-7:** AAC publishes and establishes durability of original capture first. `records::prepare_capture_submission` then owns secure identity minting; mutable writer metadata is retained in Rust memory before persistence so failed persistence does not remint on hot retry. The initial capture has no recordId. Fault test proves no pending reservation exists before capture durability and verifies subsequent writer submission/late evidence after hot repair. Cold published capture without a writer submission is held visibly; no ID or act is invented from file contents.
- **ACT-8:** the decision-view no-write census recursively covers project/decisions, legacy records and all `.chirality` logs/captures/metadata. A regression deliberately modifies relocated capture bytes and proves the census detects it; read-only derive preserves the full current census.

## Validation at repaired source

Command from repository root:

```sh
CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home cargo test --offline --locked --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml --test act_storage --test decide_flow --test schema_validation --lib
```

Exit 0: **12 library tests, 17 act_storage tests, 4 decide_flow tests, 6 schema_validation tests passed.** Includes unchanged shared W-1/API negatives, local entropy/collision/concurrent append coverage, original legacy identity/read-only checks, native stand-in refusals and stale-source/lapse assertions. `npm run build` from app exited 0: TypeScript and Vite passed. No live supplier or model was run. Parent owns final connected Node/hosting checks after this freeze. Shared common helper dead-code warning is informational. No Cargo dependencies, lock pins or maintained historical fixture bytes changed in this repair.

## Remaining standing

Independent same-reviewer backcheck required on the exact repaired bytes. Native events are test stand-ins, not evidence a person acted. Fault injection tests exercise production failure handling but do not qualify actual OS power-loss/process-kill behavior. Kernel advisory locks cover cooperating local App writers; network filesystem/noncooperating evidence mutation is unqualified. Cold original capture custody is not persistently established without the still-unselected sealing/custody mechanism. Existing unsigned RS claims and repaired backlinks retain provenance limitations. No actual A15 implementation, common service, SWBPIPE joining, global OI closure, stage acceptance or product release is claimed.

## Frozen input/clarification sources

| File | SHA-256 |
|---|---|
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V1-ACT.md` | `1ac9f852f49b1e41e0e3502692d8df72dfc0818d3f6153b61dd8ded5a5595833` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-CUST-A.md` | `a7f456b25159ed1686432bcd6661dad166b010c8bafae1f7d8b810af42f80648` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/CC-CUST-R.md` | `37e139b466e4b1860c6370d2ed83c7590df8e9fe7b6a97ec2d5f0dbadb11e078` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/P0-ACT.md` | `c2df54c60d6e08a0b5d0d143555ae8a19afaaa57ec8c15783d2e31d04ee7714f` |

| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V0-CUST.md` | `111c7098fff7f4e7c46825716fdc7db6bd6dd80bf48efaca3c31f2ff620a5a41` |

## Repaired output candidate

Original instruction/role/skill origins remain in P0-ACT.md. Additional sources read in this repair are V1-ACT and CC-CUST-A/R above plus root/manager's trusted task messages; V0-CUST READY was relayed by parent and its explicit source-only prerequisite verdict was subsequently read; no independent product-review claim is made here. Manager-owned lib.rs command continues automatic reconciliation on Refresh; this lane changes act APIs and UI display but no host command. Exact outputs:

| File | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/act_control.rs` | `f4975dad3bc902fc3c2ee2c6ff797f7bd5e2393efea2936d74dbb9af80201791` |
| `projects/chirality-app-v4/app/src-tauri/src/recorder.rs` | `96e6c17a34aae58928d7f9339b5e5af7205265c856fc8dd077253ae8f9604ad4` |
| `projects/chirality-app-v4/app/src-tauri/src/records.rs` | `cc61f735ab8dfa987081b5f50d37bd0a8b93c340c80cc5bd72266a307c588fea` |
| `projects/chirality-app-v4/app/src-tauri/src/decision_view.rs` | `051dab738e09895d9b81b3e65891aab843681b585922b0572ac959a309f7762c` |
| `projects/chirality-app-v4/app/src-tauri/src/storage.rs` | `ae8439c47b86a3225bf46e893bfa1159a2189d0cc8579692d468a78ea9267d77` |
| `projects/chirality-app-v4/app/src-tauri/src/util.rs` | `3033b37e0f360ccc2f43e4cd1d55d0d7d8305b19479e741693fd5d772f9f6d5c` |
| `projects/chirality-app-v4/app/src-tauri/tests/decide_flow.rs` | `7b0297fc11fdaf008f84264053a3939db95da947b1486039e42ae48087b57cd7` |
| `projects/chirality-app-v4/app/src-tauri/tests/act_storage.rs` | `c5f3fcecbd1331a52e89a6eb07e4f23df99456d22f85ad818ed9888c88f87e84` |
| `projects/chirality-app-v4/app/src/App.tsx` | `9c80295a3eab50970bc9ba5e668cdc36ca0acf347cc6c4c356b964477e8f415a` |
