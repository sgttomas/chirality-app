# I5 native-selected examination receiving producer — 2026-10-05

TASK `/root/group_a_execution/catalog_adapter_production`, parent `/root/group_a_execution`; native delegated descendant, no delegation. Implements finalized I5-TRACE-CONSUMER proposal 80d806… as a disjoint new receiver. Only new trace_receiving.rs/test, receiving fixture subtree and this record written. Existing reviewed external_trace 22d9… and canonical assets, lib/App/runtime_session, Design and Git unchanged. Native UI/model/host/auth/network not operated.

## Concrete APIs and custody

`ActualSelectedSource::read(native_path)` opens once with Unix O_NONBLOCK|O_NOCTTY and verifies the opened descriptor is regular before reading. This follows attachment read_snapshot's source-reviewed descriptor approach; its private text-carrier bound/UTF8 policy does not apply to examination metadata and is not copied. Public attachments::native_path_identity is reused. Unavailable/special sources retain reason/path identity without invented bytes; failed reads retain any partial buffer/hash with explicit partial-only identity scope. `from_complete_selected_buffer` receives a buffer already read by the sole main-process caller, never reopens its filename, and labels that mechanism separately. Buffer SHA uses adopted App exact-bytes method, not host canonical content or executable identity.

`ReceivedTrace::receive(source, explicit RecordKind, explicit EvidenceKind)` retains complete original bytes/parsed document. Exact existing three canonical schemas compile by declared IDs with eager definitions/offline no retrieval; no source/schema rewrite. For complete candidate-bearing EXP/XT, immutable declared basis contains full subject (EXP revision/build tuple), configuration, date/source, case and source reference from that same buffer. Person-stated date remains a source claim, not verified clock/native evidence. TraceAccount receives original bytes and source-declared candidate key/input-custody origin; full tuple remains alongside routing key. Existing semantic refusals, including overlap, false joined pass and misclassification, remain raw refused input with reason. No current App build identity is invented.

`TraceReceivingSession::read_selected` / `receive_selected_source`, `import(index)` and `snapshot` retain independent per-import source/basis/account. A later same filename/revision/different build creates another receipt; none merges, updates or borrows its basis. No snapshot rereads files, writes durable copies or records a new examination/human act. Main-process picker/IPC integration remains the sole shared owner's next consumption: no renderer path/trusted-origin acceptance is implemented here.

## Exact unbound boundary

Non-candidate definition/rehearsal subjects and missing/invalid candidate/config/date retain raw buffers/hash/source metadata without fake sentinel candidate. Standalone XT work schema carries only a subject reference/date, not complete candidate/configuration; its input is retained as unbound, never given the previous selected record's basis. Shape assessment runs, but no candidate TraceAccount semantic admission is claimed in these unbound cases. An explicit linked complete work-account examination basis remains a later owning contribution; no human gate is introduced. Complete source records are unverified claims even after conformity. Current executable/native examination/host origin remain not established; EXM24/25 counts false, OI-003 unresolved, DECISION-3 deferred.

## Focused connected checks

Ten new tests (plus included AAC helper setup) use actual temporary regular files/descriptors or explicit already-read buffer transfer. Cover once-read immutable complete body/hash/person-date/full tuple; same filename/revision/different build receipts; schema-missing/noncandidate/unbound basis; standalone XT work not borrowing prior candidate; malformed bytes/missing date without defaults; selected overlap/false join/misclassification refusals; FIFO with no writer, directory, device and unavailable non-Unicode path; transferred buffer without reopening; examination metadata above attachment text bound without truncation; exact constructed-fixture provenance. These are own-code receiving tests with injected selections, not a real native-picker or actual examination witness. No new size policy/dependency. Manager granted the exclusive Cargo slot; actual check completed and slot released to Core.

## Source clauses and reviewed origins

EXP §3.1 / EXP-R1, §3.2 / EXP-R2/R3, §3.4 and §4.1 bind supplied subject/config/date/provenance; EXP schema explicitly allows stated_by_person date. XT §3.4 X-R1…5 and §5 retain work/result limits. App-owned source buffer identities follow C §5.5 / CC-CONTENT-IDENTITY, not host identity minting. Source/schema/root role origins retained in prior I5 records; concrete filesystem/receiver sources read here:

- `projects/chirality-app-v4/app/src-tauri/src/attachments.rs` sha256 `77791e9bb62dd994ff7f0fa12a04acb667834ca3d5132f2a3d7284b308ffa0a5`
- `projects/chirality-app-v4/app/src-tauri/src/attachment_custody.rs` sha256 `02c562fcf2bc6d7805052fdb387e454516de1a5f4d280f0e3d2b56cab235eaf8`
- `projects/chirality-app-v4/app/src-tauri/src/util.rs` sha256 `4c890ed6e57c5ef5a155dfac18133f9a0ab7c5b7ba1a96b5a42631a2ebceb951`
- `projects/chirality-app-v4/app/src-tauri/src/external_trace.rs` sha256 `22d9ad6b3fa7d8efe1156cb4c77e6e0def94b744ecef41b7ecfe4734b776f407`
- `projects/chirality-app-v4/execution/_Coordination/AgentRuns/APP-V4-GROUP-A-20261004/changes/I5-TRACE-CONSUMER.md` sha256 `80d8060100dffced72a2462561dccab32899520fa267d2ecc742edfd8c066dd1`

## Frozen author verification

`CARGO_HOME=/tmp/chirality-app-v4-group-a-cargo-home cargo test --offline --locked --test trace_receiving`: actual exit **0**, **11 passed / 0 failed / 0 ignored**, 0.17s; ten receiving tests plus included AAC helper setup. Compilation 4.11s. No compile/runtime failure, criterion weakening, new dependency, source/schema/fixture repair or extra rerun followed. FIFO-without-writer, directory/device refusal and unavailable non-Unicode path metadata control passed in this own-code test environment; no actual native selection or valid non-Unicode selected file witness is claimed. Selected regular-file/buffer and later snapshot behavior passed. Partial physical-read error is an implemented retention path, not an observed fault-injection witness in this suite.

New source/tests/receiving assets frozen for independent review and sole-owner native picker/IPC consumption. No complete App UI or real examination witness follows from these producer tests. Exact stdout/stderr retained during execution at `/tmp/chirality-i5-trace-receiving-tests.log`; parent may copy it into run evidence. The original external_trace source remains at reviewed 22d9…; no runtime layer/schema/Design/Git mutation by this TASK.

- `projects/chirality-app-v4/app/src-tauri/src/trace_receiving.rs` sha256 `2bbd8b5c4abb6476da3d953770354ba5cffed0c437822fb7201aaebd634e16e1`
- `projects/chirality-app-v4/app/src-tauri/tests/trace_receiving.rs` sha256 `f6853c0cbedd0927f7634bec837615c1088dd7e7d3cd0c7716acf93166066ab4`
- `projects/chirality-app-v4/app/src-tauri/resources/external_trace/receiving/manifest.json` sha256 `852ca9b5aebdf2ac7d274ebad54481e344225c4753ae2cf79035132a82d1007b`
- `/tmp/chirality-i5-trace-receiving-tests.log` sha256 `65b57df34c8525358764bbbcde138a005f9adf30403c633d28d9ebefcbefd352`

Receiving fixture identities:

- `EXP-missing-build.json` sha256 `9780e2dd10a7b36e813edcde9f216f01286e2e7e3e0b748ef4a043e67f829d21`
- `EXP-overlap-refused.json` sha256 `addb9cca34152d53bfdf3965428001adfbdd8cdda6bd617a07df10e0e9896285`
- `EXP-person-stated-basis.json` sha256 `2b30b824cdd91be6f16639c5ac8c103ddd74942a6be366b262466e5b771610c5`
- `EXP-same-revision-other-build.json` sha256 `3d9f342da3fe99cb2bc48fac8729f17c189391dce7523b69287fb79f5cba2fb5`
- `XT-false-joined-pass.json` sha256 `8045bb74fd10c36540627de7f091a13b0b05119dd99d1aa844d486c66779e4e3`
- `XT-unverified-joined-claim.json` sha256 `d29cde6e38e1aa88190dedf6d1bf4b24dd6b27bdfd73422cf14e64225896cca5`
