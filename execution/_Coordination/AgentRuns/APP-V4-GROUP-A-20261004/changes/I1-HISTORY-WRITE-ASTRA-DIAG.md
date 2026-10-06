# I1 history write — Astra diagnosis and private repair proposal

2026-10-05. TASK `/root/group_a_execution_astra/history_write_diagnosis`, native descendant of sole WORKING_ITEMS `/root/group_a_execution_astra`, actual gpt-6-astra/low, no delegation. Software-defect-diagnosis applied. This is diagnosis/private experiment, not maintained repair, independent approval, archive acceptance or publication.

## Finding

**High confidence: the failed-write fixture has an invalid concurrency assumption.** `install_broken_test_input` at original hosting.rs1939 spawns a piped cat, takes stdin, kills and waits for that cat, and assumes no reader survives. Under concurrent spawn, another child can temporarily inherit the pipe read endpoint. Killing/reaping the intended reader therefore does not establish a broken pipe. A small complete write can succeed, and the Host correctly records `sentFrame`.

Earliest divergence is the fixture precondition, before the Host write. Direct Darwin `proc_pidfdinfo(PROC_PIDFDPIPEINFO)` observation links the writer's peer handle to a read descriptor in a different owned child **after** killed-child wait and a successful write. For example, killed PID37007's read endpoint handle `4cce6274fa6b1b40` was present in surviving child PID37011 fd22, flags1 (read), status3 (shared/close-on-exec). A close-on-exec descriptor may still be inherited before exec. The controlled probe launches only `/bin/cat`, enumerates only its own children, and examines their pipe descriptors. No user/auth process or credential data is inspected.

The trace found667 such matching records. It is not a complete lifetime trace for every success: process exit and fd sampling race, and logging interleaves. It establishes actual alternate reader ownership, not an inferred shared-Host-state cause. Determining the supplier stdlib/kernel internal spawn implementation is unnecessary for this fixture repair; no precise internal fork mechanism beyond observed inherited descriptors is claimed.

Producer trace: `write_complete` at905 calls real `write_all` then `flush`; request source code at1002–1008 sets `written=true` only on `Ok(())`; source evidence at215 publishes `sentFrame` only when written. Distinct Hosts do not share Inner. There is no evidence warranting production sender changes. Producer defects outside this narrow vector are not globally excluded.

## Preserved checks and exact associations

Original a515 archive failure remains213 passed/1 failed/1 ignored and blocks publication. Original binary SHA dd319259d831b156bf3581a6b0949162fbc3e29fd67c202601be9b2a3ba18c84 is unchanged. Prior isolated1/0 was not a repair. This assignment's unchanged exact binary `hosting:: --nocapture`, default concurrency, returned93 passed/1 failed/1 ignored, exit101: sibling `scoped_start_refuses_replaced_registration_and_keeps_write_failure_unknown` also failed the same helper assumption. Its original history oracle happened to pass; that is not erasure of the archive failure.

Raw fixture reduction retains spawn/take/kill/wait/write-all/flush:

| Experiment | Result |
|---|---|
|16 threads ×100 trials, original fixture|1545 actual successful writes after kill/wait, of1600|
|1 thread ×100 trials, original fixture|0 successes of100|
|16 threads ×100 with parent reader lookup|1434 successes; no matching reader sampled in parent|
|16 threads ×100 with owned-child reader lookup|1425 successes;667 alternate-child reader matches|
|16 threads ×100, same ongoing cat spawns, read-only descriptor substitution plus `try_clone`|0 successful writes of1600|

The single-thread probe's inherited final display string incorrectly says1600; its preserved source unambiguously runs1×100. This is reported rather than silently rewriting original evidence.

Private full App snapshot was compared against247 regular App files in the immutable archive: only `src-tauri/src/hosting.rs` differs, solely the cfg(test) helper. Original/live Host SHA e5b908ba9635b74ff27c79f4f568c139967aaa4edfa0f9a16dadde50dfe4db34 remains unchanged. Private helper candidate SHA c8fcbfa53c7e3db24fc771c9dc883d8bfd6481512f6d06ecc39164bff71a92f3. Private repaired binary `/tmp/history-astra-diag/repaired-tests`, SHA7eeb55acac6ada51e3bb8180c5b240ed8dbc3112de6ec63ceae7af1d5251c436.

Offline locked private compilation used the reserved shared target, CARGO_HOME `/tmp/chirality-app-v4-group-a-cargo-home`, CARGO_NET_OFFLINE=true, CHIRALITY_SKIP_CODEX=1. **All Host tests at unchanged default concurrency passed94/0/1 ignored**, including the original exact history vector and every helper caller (guidance, conversation start/steer, history, native-page/source and credential-failure observations). Repaired exact original history selector separately passed1/0. No assertions, filters of the Host set, ignored states or concurrency settings were modified. These are focused regression checks, not whole-candidate/archive validation.

## Narrow maintained proposal and return

Replace only cfg(test) `install_broken_test_input` with read-only `/dev/null` opened as File, converted to OwnedFd then ChildStdin. Add the short causal comment in the supplied patch. This preserves capture/fstat/dup/source binding, reaches the real OS write, and fails with a non-writable descriptor rather than relying on child death to remove every reader. It does not simulate a producer result or weaken `sentFrame`/write-failed/unknown-no-response assertions. The fixture tests generic actual write failure, not an EPIPE-specific contract; its callers do not require EPIPE. Host code is already Unix-specific (fd/fcntl and `/bin/cat`); `/dev/null` introduces no broader platform restriction within this target. If a future test specifically requires peer-disconnect EPIPE, it should use a separate explicitly synchronized fixture.

Manager should authorize only this helper/comment edit, then obtain independent source/criterion review and original-vector/concurrent caller backcheck on maintained bytes. Parent must perform repaired exact checkpoint/archive validation, retaining the original failed archive record, before publication. No production changes or other test edits are warranted by this finding.

Evidence: [manifest](../evidence/HISTORY-WRITE-ASTRA-DIAG/manifest.json), [private patch](../evidence/HISTORY-WRITE-ASTRA-DIAG/private-helper.patch), [alternate reader trace](../evidence/HISTORY-WRITE-ASTRA-DIAG/child-reader-matches.log), [original concurrent run](../evidence/HISTORY-WRITE-ASTRA-DIAG/original-host-concurrent.log), [repaired concurrent run](../evidence/HISTORY-WRITE-ASTRA-DIAG/private-repair-host.log). Sources/raw logs and actual source/binary/instruction hashes are preserved there.

All sessions finished. No owned process, Cargo or source hold remains; shared lane released to manager. Private snapshot/probes/binaries retained for review; no diagnostic instrumentation entered maintained source. Writes are restricted to this report, its evidence directory and private scratch. No auth-home/auth.json/stock/native/model/network/download/credential operation occurred. No old agents reactivated.
