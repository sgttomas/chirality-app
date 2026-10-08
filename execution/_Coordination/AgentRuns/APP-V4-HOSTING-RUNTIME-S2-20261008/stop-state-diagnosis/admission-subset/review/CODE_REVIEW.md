# STOP-ADMISSION-01 independent frozen review

Verdict: READY for bounded manager fan-in. No blocking findings in the four-file candidate. This is not whole Stop conformance or process-group ownership approval.

Exact base: cd79d9b477f7f33aa4d7a3683e26e6337039d412. Candidate manifest SHA256: acd810629819ba4ac8cf3d2b88bf665b1671763185ff7c2182bb21751d1550cf. Source worktree: /Users/ryan/.codex/worktrees/hosting-lt23/chirality. All four maintained hashes, complete staged patch, base, absence of unstaged differences, and all author evidence-manifest members independently verified. SOURCE_VERIFICATION.json retains exact source hashes. Review covered the complete diff and RETURN/documentation claims against design 5754f9841156b3778d15c50c2ce542b0d8680e71289ecdf589ce8149c68f3933.

## Source assessment

Both routes hold REC writer then attachment gate continuously from final exact attempt/NotSpawned/verifying admission through actual spawn and custody/H5 publication. Initial admission uses gate then Inner; checked increment precedes app-session mutation. Preparation stays outside operational gates. Refusal validates and mutates under the same Inner lock, so cancellation/new admission cannot intervene between those actions. Final spawn/result writes remain protected by the held gate. No new accepted start state or process capability was introduced.

LT20 requires the current matching NotSpawned marker and checked revocation. Its return precedes stdin, PID/group, wait, closure and terminal scheduling paths. The event-local stopRecord leaves historical Inner.stop_record intact. Clearing in-flight successor references does not create an LT20 artifact or assert absence of prior descendants.

Both handshake routes now use captured attempt/H5/Installed/handshaking checks. The failure helper retains gate and Inner through its existing signal and closure action; it does not release a checked source and then call an unscoped current-PID helper. Native request/notice dispatch retains captured source/pipe checks and existing frame-write-before-gate order. Response waits are outside the gate. Legacy initialized-write error handling remains distinct, and legacy does not enter S1 publication. Existing allocation-failure and process-lifetime weaknesses are unchanged and explicitly held.

## Independent execution and discrimination

Ran cargo test --lib stop_admission_ -- --test-threads=1, then the same with --features distribution-successor,custom-protocol, serially in the authorized existing offline target. Both exited 0: 6 passed, 0 failed, 0 ignored per mode. Logs: default.log and production.log. Supplier build execution disabled; invented fixture children only. No author source edit, new checkout, new target or broad duplicate build.

These controls execute the original causal D2 schedule: actual version probe blocks on explicit release, real Stop returns LT20 before release, then both successful and failed probes cannot resurrect either route. Further discrimination covers cancelled/newer attempts, Stop blocked through final check-to-publication, pre-handshake Stop, historical metadata/REC cause with cleanup tripwire, missing/Installed marker inconsistency, and checked overflow. Delayed actual successful handshake is exercised; error and contradiction after replacement are direct private-settlement negative controls, not separately observed supplier error frames. Existing scoped write implementation was traced; no new independent paused-write test was added.

Retained r1/r2 failures are consistent with author chronology: test barrier mutex lifetime blocked a newer attempt, then incomplete synthetic REC fixture failed the strengthened actual-cause assertion. Final fixture includes explicit binding and required turn shape; no REC product changes. Original pre-repair D2 diagnostic remains historical evidence, not silently replaced by these passing runs. Author broad 238-name parity evidence is reused, not represented as independently rerun.

## Limits and next handoff

LT21/LT22, invalid post-LT12 mapping, fallback exit facts, lost first closure counts, signal/reap/group reuse, allocation-failure cleanup and restart completeness remain held. No native supplier/App, bundle, S3 or whole-trace qualification. Exact committed-head integration review and fresh consumer source receipts/adoption remain required. Shared target released after both independent commands completed. Source remained unchanged during review.
