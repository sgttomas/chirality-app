# STOP-STATE-01 Part1 — REC design review

Verdict: **NOT READY for code release: ownership/reaping protocol and its availability consequence require concrete refinement.** REC concurs with the admission/no-child and independently captured closure/exit semantics, but that concurrence does not close the explicit wider-window issue.

Reviewed `/private/tmp/STOP_PART1_DESIGN.md`, SHA-256 `b932f261f378ac4f09973d3a04ead69a8c97a140551effc258a22a047c503ba0`, against source basis `cd79d9b477f7f33aa4d7a3683e26e6337039d412` and preceding source/diagnostic assessments. TASK `/root/hosting_runtime_manager/attachment_namespace_owner` under WORKING_ITEMS `/root/hosting_runtime_manager`, parent HELP_HUMAN `/root`; harness-native read-only contribution, no delegation. Only this report written. No implementation, tests, build or native execution. Technical source review, not independent implementation review.

## Blocking refinement 1 — signal/reap authority must be atomic with respect to each other

The installed capability establishes source provenance; it does not reserve a numeric process-group identity after reaping. “Currently owned unreaped leader” checked and then unlocked before signalling is also insufficient: EOF can reap between that check and killpg. Name the exact exclusive protocol that serializes permission to signal with leader reaping, including handshake-failure cleanup and repeated Stop. A signal may proceed only while its warranted identity cannot be released/reused during that operation. A numeric group probe is an observation, not an owned-group capability.

The source aggregate should distinguish at least actual child ownership, exit observed but not reaped if supported, reaped, and cleanup ownership unresolved. Do not equate an exit status with proof all descendants ended. Exact OS mechanisms and their supported-platform lifetime semantics need owning review; this report does not assert a particular primitive supplies a process-group capability. If no sufficient capability exists, fail closed before signalling and retain the source/limit. Do not detach/reap merely to let a no-child guard pass.

## Blocking refinement 2 — concrete handle operations and lock graph

The design says both to retain an Arc to a Child slot and to remove blocking wait's lock dependency, but leaves the decisive mechanism open. Specify which operation owns the handle during waiting, which can signal, which can reap, and what Stop does when EOF is waiting. Simply moving Child out of a mutex leaves Stop with a numeric ID; leaving Child behind a mutex while blocking wait prevents Stop obtaining that lock to terminate it. Either can violate the claimed safety/liveness boundary.

Provide a lock/operation table with acquisition and release points for EOF observation/reaping, Stop signal and grace checks, handshake failure, source replacement and final closure installation. No path may hold source gate/Inner while waiting on a child mutex held by a blocking waiter; no waiter may retain that mutex then request source gate against an opposing path. Signal/reap serialization must not keep source gate or REC writer across blocking wait. A source-owned nonblocking observation/reap protocol is a possible design direction, not an implementation selection or proved OS guarantee here. Clarify how a completion reaches the once-set exit component without rereading current Inner.

## Blocking refinement 3 — availability consequence is larger than the stated residual

After LT12, EOF has already reaped the leader. The proposed unreaped-only rule therefore makes later explicit Stop cleanup unavailable when no independent group authority remains. That is a concrete change from current Stop-returned-stopped behavior, not merely retaining the isolated malformed row. It may also affect ordinary Stop or handshake failure if EOF wins reaping between Stop admission and cleanup. Enumerate those schedules and the resulting state/result; do not restrict the stated consequence to post-LT12.

Failing closed against an unowned group is necessary, but the package must explicitly account for the accepted Stop/restart affordance and for what remains incomplete. It cannot return stopped/tree-ended/zero descendants on unresolved ownership, silently promote cleanup-unavailable to a successful no-child cancellation, or automatically start a new child. Parent/Host should decide the bounded source treatment and whether its actual consequence needs the reserved availability/descendant decision. REC does not invent a new human gate, select an automatic-survivor policy, or authorize an unsafe fallback. If Part1 cannot preserve its advertised existing child-stop scope under the new ownership mechanism, narrow that scope and report the exact residual before code release.

## REC capture constraints retained

First closure is the original source's effects/cause/counts and persistence standing, captured once under the source protocol. It may precede actual exit observation. Cleanup-unavailable does not erase or rerun that closure and does not retroactively declare the person caused an earlier supplier exit. Conversely, a cleanup attempt alone is not new evidence that an as-yet-open child ended. Use the accepted existing closure triggers and retain uncertainty about actual process state; do not extend REC trigger meaning to fit the signal failure.

First actual exit is captured for the installed source, independently from closure. Unknown terminal event fields remain immutable if later genuine exit becomes known. Duplicate is idempotent; conflict retains first plus bounded limit. Source reaping status must not be collapsed into the exit component: knowledge of status, handle lifetime and process-group ownership are distinct facts. A no-child LT20–22 cancellation creates neither exit nor closure component and never borrows historical H5 or PID.

The current proposal correctly preserves D4 first totals, no replay for persistence failure, no journal hydration, no resend, exact H5, historical LT12 cause and bounded aggregate shape. No new REC schema/event or human-act category follows. Existing Runtime/native closed-view and S1 receipt behavior cannot turn a cleanup limit into current native authority.

## Evidence required after a concrete design is agreed

Add deterministic barriers at: immediately before signal eligibility; between eligibility and signal while EOF requests reap; reap before Stop admission; Stop before EOF wait; handshake failure versus EOF reap; source replacement before completion. Demonstrate mutually exclusive signal/reap authority, no blocking Child-lock inversion and no signal based only on a reaped historical ID. Use owned invented processes and a signal-observation seam, never unrelated PIDs. Preserve original D2/D4 backchecks and first-closure/late-exit tests, including valid closure with cleanup unavailable and absence of false no-descendant/tree-ended claims.

No code is released by this review. Reassess the exact refined protocol and outcome table; the earlier positive REC capture concurrence remains valid within these unresolved ownership and availability boundaries.
