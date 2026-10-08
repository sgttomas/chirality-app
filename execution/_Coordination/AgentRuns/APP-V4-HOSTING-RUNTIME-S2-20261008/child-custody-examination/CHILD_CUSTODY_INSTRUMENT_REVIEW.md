# Child custody temporary instrument source review

READY to compile and run only the narrowed released synthetic examination at exact SOURCE_FREEZE.json SHA256 ec5d4793c93eadc4fe3176c84b7f98a4058281f6a27c1a9782930498944cd850. Production remains held. No compilation or execution was performed during this review.

Verified source hashes:
- examine.c: 57b913c052f1eea2af80d2f6d9016e1c212abdca5f45ee565bda3b86d57af994
- driver.py: c1e282bb180bf408ef7fc0b9a2e71282b3852d4cfdc44d9d35962056e8c412ee

Read both complete sources and frozen compiler argv against plan2d6c6bf3 and independent plan review439c9545. No blocking scope/safety finding. Only one fork creates the invented child; no fixture descendants, exec, actual group signal or arbitrary-PID operation exists. setpgid affects the fixture itself; getpgid is limited to its exact fork-returned identity before consumption. All reused-identifier and signal actions in the threaded model are inert records.

The native helper and child install default SIGALRM and explicitly unblock it; SIGPIPE is locally ignored so EPIPE takes the recorded failure route. The isolated SIGCHLD setup clears SA_NOCLDWAIT. Fork/pipe errors cannot enter a wait with an invalid PID. Release closure allows natural fixture exit; bounded exact-child cleanup has no kill fallback. Successful consumption sets reaped irreversibly, so later assertion failure cannot enter cleanup polling. One postconsume ECHILD query is intentional. An initial waitid/consume error can lead to a cleanup query, but cleanup stops immediately on a waitpid error and cannot create or signal any replacement; this is an additional exact-child status query, not restored ownership or retry authority.

Guarded model scheduling holds its owner mutex through inert action. The competing reaper uses trylock; barrier locks are released during timed waits. The broken control deliberately unlocks, permits inert reap/reuse, then acts without revalidation and must record the wrong identity. Reap-first refusal is an explicit model check, not a real OS race. A failed barrier exits the helper rather than joining; completed-barrier joins still rely on the self-alarm for abnormal scheduler stalls. No hard real-time guarantee follows.

Driver launches only exact compiler/helper argv, captures regular-file output, verifies frozen source and compiled-executable hash, records direct PIDs, and uses bounded wait with no signal escalation. A timeout or native failure forbids the next mode. Exclusive phase markers and output creation prevent ordinary rerun/overwrite. Frozen source checks are not protection against hostile concurrent same-user file replacement, which is outside this experiment.

Limits for result review: driver abnormal exceptions may leave a partial packet without RESULT/manifest; preserve it as failure rather than inferring cleanup. Self-alarm, passive grace and pipe closure are not proof of fixture reap. Only the matching native consume record plus direct helper exit permits success. Compile tooling can create its own toolchain subprocesses; this is not an all-process census. Raw native status/code and trace ordering must be inspected in addition to the driver pass flag. There is no production API-support, PGID reservation, foreign-waiter exclusion, descendant census or Host integration result.

Independent TASK under /root/hosting_runtime_manager, delegated harness-native mechanism, no delegation; read-only source examination. This verdict relies on the parent's already supplied narrow execution release and does not expand it.
