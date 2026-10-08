# Child custody: bounded synthetic mechanism examination

Proposed only; no harness source has been written, compiled or executed. Parent technical release after independent review is required. This plan is separate from the conditional production design `/private/tmp/CHILD_CUSTODY_DESIGN.md`, SHA-256 `3b408153091967c97148328fcae68af70309ca5f47254df9d88fd8f386fc221b`. Repository read basis: `bf795b99d1f7093178b41ca93e638450eca2d8e0`.

## Exact question and decision boundary

Can this recorded macOS environment demonstrate repeated nonconsuming terminal observation of one explicitly created child, followed by exactly one successful consuming wait, while an inert owner model demonstrates check-through-action serialization? The experiment does not establish current Apple API support policy, kernel source equivalence, zombie-based PGID reservation, safe group signalling, complete descendant cleanup, production lock integration, Stop conformance, restart availability or qualification.

Pinned Apple source remains xnu-12377.121.6, commit `ac9718fb1af618d5ce8678d0dc6e8a58f252216f`; the observed running kernel is xnu-12377.161.14. A passing experiment narrows an empirical uncertainty only. It cannot bridge that source/support gap or authorize production reliance. No production code or accepted contract changes are part of this examination.

## Read and write fence

Read-only inputs: the exact design above; this plan and its review/release; basis-owned `hosting.rs`, `hosting_successor.rs`, `lib.rs`; SDK `sys/wait.h`, `signal.h`, `unistd.h` and their included system headers; local wait/sigaction/setpgid manual pages; `/usr/bin/clang` and the installed Python 3.13 executable. Read only OS/build/compiler/interpreter metadata, not hostname, user config, process lists, credential stores or supplier directories. Repository reads use `git show` at the full basis; no checkout switching, stashing or Git mutation.

After release, create one fresh exclusive mode-0700 directory `/private/tmp/child-custody-examination-<random>`. All authored C/Python source, one compiled executable, logs, process ledger, receipts and result live there. No output overwrite; no repository files, manager records, prior evidence or shared Cargo target are written. Set compiler temporary directory to this owned directory; no package installation, cache fetch, network download or extra checkout. The compile is a single small C translation unit against installed system interfaces, not a Cargo/App build. Proposed command, with the fresh directory substituted literally and recorded in argv: `/usr/bin/clang -std=c11 -Wall -Wextra -Werror -pthread <dir>/examine.c -o <dir>/examine`. The C file is the temporary examination instrument, not proposed product implementation. A small Python driver records hashes/argv and uses bounded waits; it never sends signals or starts a shell pipeline.

The source and exact compiler command are frozen and pass source review against this plan before the executable is run. Source mismatch, compilation failure or unexpected extra process creation stops the run without repair-and-rerun hidden in the same result. Any necessary fixture repair is retained as a new named revision with the initial failure.

## Complete process inventory and permitted operations

Sequential operation only; never launch the next mode while a previous process remains unsettled.

| Process | Creation and lifetime | Allowed process actions |
|---|---|---|
| Python driver D | One direct invocation by existing command tool; exits after receipts | Spawn/wait for exact compiler and exact examination executable; no kill, terminate, killpg, process enumeration or arbitrary PID operations |
| Compiler K | One direct child of D, builds the one file | Normal compiler subprocesses from installed toolchain; record compiler argv/version and exit, not a system process inventory. It does not run the examination. A compile timeout stops the procedure; no blind signal escalation. |
| Examination N | One direct child of D for native-observation mode | Single thread; one fork only; waitid/waitpid/getpgid only for the exact returned child PID; self-timer; no group signals |
| Fixture C | The sole child created by N | No exec, fork or descendants. Set its own process group with setpgid(0,0), write ready marker, wait on its private release pipe, then `_exit(37)`; self-timer fallback |
| Examination M | One later direct child of D for inert-model mode | Two pthreads plus main in the same process, no children and no OS process operations other than its own self-timer. All model identifiers are inert values, never passed to kill/wait/getpgid. |

No auto-reap subprocess is included in this first examination. SA_NOCLDWAIT/SIGCHLD mutation, foreign waiter injection, group escape, leader-plus-descendant fixtures and real signal delivery tests are deferred. They are unnecessary for this narrow observation result and complicate safe cleanup. The production design still retains those proof obligations.

Runtime process ledger: D records each helper PID returned by its spawn API before waiting; N records its own PID and C's fork-returned PID, creation role, every wait call/result, release-pipe action and final known disposition. The ledger lists only these owned processes. A missing event remains unknown; no scan attempts to rediscover a PID. Helpers write bounded structured records to owned log files; no compiler/helper output is interpreted as instructions.

## Native observation sequence

N configures its own SIGALRM default disposition and a 15-second alarm before fixture creation. It confirms a usable SIGCHLD disposition in this isolated helper, explicitly installs SIG_DFL without SA_NOCLDWAIT, and records the configuration. This is controlled fixture setup, not evidence about the production App's libraries or process-wide signal state.

Create two private pipes (ready and release), fork once, close the unused ends in both processes. C's first operations restore SIGALRM default and arm a 5-second self alarm; then setpgid(0,0), publish a fixed ready byte and wait at most 2 seconds for release using poll. Ready includes success/failure of group setup, not an assertion of group custody. Release byte or release EOF causes `_exit(37)`; poll timeout causes a distinct fixture-failure exit code. No signal action is used to release C.

N waits at most 1 second for ready. With C waiting on release, call waitid(P_PID,C,WEXITED|WNOHANG|WNOWAIT) using a freshly zeroed siginfo. Expected observation: return zero and si_pid zero. This is only a no-terminal-status result. Record getpgid(C) while C is held by the ready/release protocol; expected value C if setup succeeded. No numeric group probe is made.

N writes the release byte and closes release. For at most 2 seconds, at a maximum 200 finite attempts separated by at least 10 ms, call the same freshly-zeroed waitid until terminal status is observed. Each call logs return/errno and PID/code/status. A syscall that itself stalls is handled by N's self timer, not by an assertion that WNOHANG has a hard wall-clock bound. On matching CLD_EXITED/status37, call the same WNOWAIT observation once more. Require identical identity and terminal status. Optionally recording getpgid(C) at this unreaped point is part of this exact plan: one call only; its result is an observation of this fixture, not reservation proof. No getpgid or group lookup occurs after reap.

Revoke all modelled signal permission (there is no real signal entry point), then call waitpid(C,&status,WNOHANG) exactly once. Require C and exit37. Call waitpid(C,&status,WNOHANG) once more solely to record the expected ECHILD after consumption; it is a child-status query, never a signal fallback. There is no second child creation. Report success only if both WNOWAIT observations, consuming wait and follow-up ECHILD agree and every created child is accounted for.

On setup, pipe, waitid or assertion failure: close release immediately so C can exit naturally; use only exact-child waitpid(C,WNOHANG), no more than 200 attempts over 2 seconds. Preserve the failure and actual cleanup result. If that cannot account for C, stop with unresolved disposition, wait for the self-timer observation window below, and report; never kill the remembered PID or group.

## Inert serialization and reused-identifier controls

M implements only a small model custody cell with mutex, owned/reaped/unavailable state, signal-revoked flag and operation trace. A backend signal operation appends an inert record; a backend reap changes the model state. No production code is imported and no OS signal is sent.

Run two barrier schedules once each: (1) signal path retains mutex after eligibility check; the competing reaper tries the mutex and records busy; after explicit barrier release the inert signal completes, then reap occurs and a later signal is refused; (2) reap first, then replace the backend's numeric-looking identifier with an unrelated invented identity of the same number; old ownership refuses the signal, and the backend trace stays empty. Add one deliberately broken check-unlock-act control in the model: the barrier permits reap/replacement between check and inert act and the model must detect the wrong-identity trace. This is the discriminatory red control, never an OS action.

Each barrier has a one-second timed wait; M arms a 10-second self alarm before threading. No unbounded join follows a failed barrier: record failure and exit the helper process, which terminates its own threads. These checks demonstrate only the examination model's ordering and regression discrimination. They do not test Rust poison handling, the production lock graph or platform PGID reuse.

## Signals, deadlines and hang cleanup

The only signals permitted by this plan are each helper's kernel-generated SIGALRM to itself, with default terminating disposition, and normal SIGCHLD delivery from its own children. C uses 5 seconds, N 15 seconds and M 10 seconds as **test safety ceilings**, not product SLAs. No kill, killpg, raise, Child.kill, subprocess.terminate or external timeout utility is allowed. No arbitrary process/group IDs enter any signal API. The purpose of the timer is to terminate the process that installed it; it does not depend on remembered PID/PGID identity.

D gives N 20 seconds and M 15 seconds to finish; a timeout closes owned pipes, starts no further helper, records the known PID/disposition and returns the failure packet without signalling. N's release writer closing on exit also releases C; C additionally has its own timeout/alarm. Allow a further 6-second passive grace before the final unresolved report if C's exit was not accounted for. If kernel scheduling or an uninterruptible operation defeats these timers, do not claim a hard bound or complete cleanup. Report the exact unresolved owned processes to the parent; no escalation or system enumeration is authorized. Reaping an exited helper through D's direct-child handle is permitted; final unknown child status cannot be repaired by probing a recycled PID.

A fixture timing out is a failed experiment, not an acceptable successful cleanup result. Success requires N's actual exact-child reap record, plus D's helper exit records; a self-timer exit or pipe EOF alone does not prove C was reaped or descendants ended. No descendants are intentionally created by the fixture. Driver/harness abnormal termination remains an explicit failure boundary.

## Evidence and return

Retain source bytes/hashes, compiler/executable hashes, actual full argv, environment names/values relevant to this fixture (no full environment dump), OS/build/kernel/SDK identities, monotonic timestamps, every owned process ledger record, raw stdout/stderr, assertion outcomes and actual cleanup disposition. Record the source basis unchanged before/after. Hash the final packet manifest. No claimed product source identity is inferred from the temporary executable.

Return one compact result table: native live/no-event, repeated terminal observation, exact consume, postconsume ECHILD, optional unreaped getpgid observation, inert signal-first/reap-first, deliberately broken model red control, cleanup accounting. Failed or timed-out steps retain their raw evidence. No broad test matrix, unchanged-format exporter renewal, B pin update or production implementation follows automatically.

A pass establishes only the stated observations on this machine and ordering in this temporary model. It does not prove a zombie preserves a PGID against reuse, that no foreign waiter exists in the App, that a group contains all descendants, or that current macOS officially supports the chosen production mechanism. Those remain in the independently reviewed production design and its owner decision.
