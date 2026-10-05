# P0-ACT-R2 — next-append native admission order

2026-10-04. TASK `/root/group_a_execution/act_storage_propagation`, native child of WORKING_ITEMS `/root/group_a_execution`; no descendants. Parent commissioned the independently reproduced ACT-6-R1 order repair in V1-ACT-R1.md. Original P0-ACT/R1 and V1-ACT/R1 remain byte-frozen history. Only act-control queue, Rust command/recorder integration and maintained act regressions changed. No hosting, schema, Design, Node runner, Cargo manifest/lock, shared graph/MEMORY, Git, network/auth or live supplier/model changes/execution.

## Repair

Rust retains writer admission ordinal and original custody in private NativeCapture state. Fresh confirm first durably publishes its own unchanged capture and prepares its writer submission, then drains earlier admitted native pending work before appending the fresh submission. Older pending acts and their required delay account precede fresh continuation. If older work cannot flush, the fresh native event is preserved as pending with its original actor, choice, scope, bound bytes, capture/observed time and writer-reserved ID; no newer act is appended ahead of it. Explicit pending batches still append admitted pending acts in admission order before their delay limits. Queue order does not parse or sort timestamps or opaque record IDs. Backlink-only failure retains AC-7; an unresolved delay account holds writer continuation without discarding new captured facts. Queued offer state updates to Recorded when its actual append is established.

ActControl::refresh_recording is the existing App's ordinary recorder continuation boundary. lib.rs decision_view now reconciles native pending work under the same Rust mutex before identify_packages; genuinely unwritten admitted native work holds new recorder request/limit appends. Unverified cold files neither enter the native admission queue nor establish append authority. Cold-file parsing/validation errors are visible origin-held diagnostics, isolated from unrelated trusted queue/ordinary recorder continuation. Existing cold matching claims remain backlink-only, with unchanged unverified provenance. Native memory also remembers established written status, so an already recorded submission whose history becomes unresolvable is held rather than re-appended.

This is the bounded App A16/request path, not a generic cross-component persistence service or a trustworthy cold replay mechanism. Unfinished persistent original custody remains owned under CC-CUST and requires the concrete seal/custody choice/witness; SEAL-2 remains unselected.

## Regression evidence

Final source command (exclusive manager-granted Cargo slot):

```sh
CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home cargo test --offline --locked --manifest-path projects/chirality-app-v4/app/src-tauri/Cargo.toml --test act_storage --test decide_flow --test schema_validation --lib
```

Exit 0: **13 library, 21 act_storage, 4 decide_flow and 6 schema_validation tests passed.** Existing ACT-1/2/3/4/5/7/8 safeguards and W-1/API negatives remain tested, not waived. No TypeScript or frontend-facing JSON shape changes in R2; R1 frontend build remains applicable. Parent owns final connected Node/hosting checks and independent same-reviewer backcheck after this freeze.

New targeted witnesses:

- Reviewer trigger: A fails on torn log; explicit fixture repair restores bytes; fresh B confirms before any explicit recovery. Written human acts remain A,B, A's reserved ID/time stay fixed, A's failure limit precedes fresh B, and the decision view retains B as latest. No fixture criterion was weakened.
- Backlog cannot flush: B's real native-event stand-in is captured but remains pending; its immutable facts and writer ID survive ordered A,B retry, followed by both delay limits.
- Pending A plus new package input: Refresh holds recorder while A is genuinely pending, then writes A and its delay account before the new request/limit pair when fixture repair permits progress. The test invokes the exact refresh_recording method used by lib.rs.
- Equal observedAt values: a private cfg(test)-only capture-clock override gives both native events exact same second-resolution timestamp. Fresh continuation and recorder Refresh still preserve admission order; opaque UUID identities are retained as tokens rather than used to infer order. Production clock behavior is unchanged.
- Malformed/unverified cold file: visible replay-held diagnostic, no human-act append, and unrelated valid recorder input progresses. Existing schema-valid fabricated pending and orphan cold-capture no-append/no-mint tests remain passing.

Test events/faults are synthetic stand-ins. No human/native authenticity, real process-kill, power-loss, network filesystem or product qualification is claimed. Shared helper dead-code warning is informational.

## Frozen input basis

| File | SHA-256 |
|---|---|
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/P0-ACT-R1.md` | `fb8d9eb89dfbf3c2313e548498c07d4f17d348a6c46b5b625239224a4fd99fb3` |
| `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/reviews/V1-ACT-R1.md` | `c1cce1b57709c15317a8df3e557641eef8a649308fa28a58ca956564d91cd889` |

## Exact successor outputs

| File | SHA-256 |
|---|---|
| `projects/chirality-app-v4/app/src-tauri/src/act_control.rs` | `1d55ff94ad08cf17673dfdae9a16e5ca7d9a98f52a1fe99a9f6101ea30a8876e` |
| `projects/chirality-app-v4/app/src-tauri/src/lib.rs` | `90b96bacfdbfa42d1337084ba50aadd82bcbb464193b5872c3efd468bb83bf15` |
| `projects/chirality-app-v4/app/src-tauri/tests/act_storage.rs` | `f66187eea1c9e7a60c9224a332a3ab7caffa6933d42e741ff227eb76002260bc` |
