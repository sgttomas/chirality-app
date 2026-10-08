# STOP-STATE-01 Part 1 — proposed implementation design, no code release

Basis `cd79d9b477f7f33aa4d7a3683e26e6337039d412`; parent-selected Part1 of STOP_REPAIR_PROPOSAL SHA256 `0b7e1b906e5c354ed0823b86f356548c784c9704924bec3366a52d1e2e05a971`. Part2A is a later completeness target, not implementation scope. No LT25, restart scheduler, canonical/schema change, or post-LT12 mapping repair. This document requests exact Host/RS/REC and independent design review before code.

## Source fence and concrete ownership

Expected production fence is hosting.rs only: start/Stop/EOF/handshake admission, private source ownership and closure observation helpers. Tests may touch maintained Host/successor test modules and add a bounded module. No changes to REC ledger/schema, Runtime/native receiver authority, Store/terminal worker contracts, supplier configuration, descendants policy, UI or Group B. If adapting private reader arguments requires another source file, return the exact call site before expanding.

Introduce a private `InstalledSource` capability created only after successful child spawn and successful H5 allocation, under the same source gate that publishes stdin/child/Inner custody. It contains immutable full H5, the owning spawn attempt captured then, an opaque installation identity, and an Arc to the owned Child slot and bounded observations. Neither current `Inner.start_attempt`, historical `Inner.generation`, nor `child_pid` can mint or substitute it. Keep historical generation/PID for existing views if needed; they have no signalling/no-child authority. Reader/stderr callbacks capture this source at installation rather than reacquiring authority from current Inner. Source checks compare capability identity plus full H5, not only numeric PID.

`Inner` holds at most its current installed-source association and current historical observation reference; each already-existing reader/Stop operation can retain its captured source until completion. No new retired-source registry, queue, transcript or hydration. New accepted start does not repurpose an old source; a new capability is installed only with the newly spawned child. Failed spawn creates no capability/H5. A source remains the owner of its late observations even if a newer start becomes current.

Model current installed child state explicitly: `Running`, `ExitObserved/Reaped`, and `CleanupUnresolved` as appropriate to actual observations, not state-string inference. Removal from *current actionable child* association is permitted only after actual source cleanup/exit observation makes that true; retain its observation component as historical. A no-child guard checks this association plus absence of a locally admitted spawn; it must not inspect only an Option<PID> or clear a slot to make the guard succeed. An inconsistent current child/slot returns a bounded unavailable error before row/state mutation.

## One admission boundary for both start routes

Start's initial state/attempt transition moves under attachment_gate→Inner, so its accepted attempt and Stop revocation are serialized. Allocate the next checked attempt before mutation. Record existing LT01/02/03 and release the gate. Expensive verification, inventory, probe and Store work remain outside all source/REC locks.

After all verification work and final successor audit, both routes acquire existing REC writer then attachment_gate, then Inner. Successor retains existing nonblocking writer/gate refusal to avoid aging its final audit behind waits. Legacy may use the existing writer wait but must acquire the same source gate and recheck afterward. Require the exact captured attempt, verifying state, no admitted installed child for this attempt, and no ended App custody; successor also requires unchanged prospective tuple/counter. This check precedes **every** verification result/state/identity write, including failure/refusal. A stale result returns an error with no source mutation or lifecycle event.

Hold writer+source gate through the actual spawn and complete custody publication (existing successor behavior extended to legacy), without scan/probe/Store IO. Spawn failure mutation is scoped to the captured attempt/state under that gate. Allocate H5 only after actual spawn for both routes; retain local ownership until allocation succeeds, then publish child/stdin/source capability/generation/LT06 together. Allocation failure kills/reaps the locally owned child before returning; never publish orphaned handles or a live generation. Counter semantics remain the existing genuine App monotonic allocation, including truthful failure standing; no pre-spawn reservation or rollback of an allocated counter.

Stop takes only source gate→Inner for admission. If it wins before spawn admission, it revokes the accepted pending attempt; if spawn wins, Stop observes the completely installed source. No check-then-unlocked-spawn gap. Probe cancellation means admission revocation, not a claim that legacy's existing blocking probe is interrupted; its eventual completion cannot mutate/launch.

## Explicit Stop dispatch

Under source gate→Inner, validate a scoped expected H5 as currently required, then choose without wildcard:

- absent/refused/stopped reject; stopping remains duplicate-owner refusal.
- verifying + proven no current installed child: existing LT20 directly to stopped.
- restart-waiting + proven no current installed child: existing LT21 directly to stopped.
- halted-after-repeated-failure + proven no current installed child: existing LT22 directly to stopped.
- ready/handshaking/spawning require actual current installed-source ownership and use LT17/18/19 respectively. The transient spawn-local section is inaccessible to Stop because it owns the same gate; after installation the state is handshaking.
- Unknown state refuses before any mutation.
- exited-unexpectedly remains the explicitly named existing Part2 residual. Preserve its current branch/availability as a conspicuously isolated legacy residual, not a claimed supported tuple or a new row. Part1 does not silently reject it or fix its mapping. Any source-ownership refusal necessary to avoid signalling an unowned process must remain truthful and be reported, not relabelled LT20 or fake success.

For direct no-child rows, compute checked attempt revocation before changing anything; record actor/stop record and the correct row under the gate. Clear only in-flight publication/admission state belonging to that attempt. Do not allocate H5, close generation/registers, touch child stdin, signal a PID/group, wait for EOF, fabricate exit/descendant/count facts, or schedule LT23 publication. A retained historical generation in legacy event shape remains historical and is not reused as a closure capability. No automatic restart exists in Part1; a future scheduler must use the same captured attempt fence.

For child Stop capture the immutable source capability, actual stop record and pipe epoch while holding the gate. Close only its captured stdin; release the gate before grace/wait. Later operations and observations must use that captured source, never `self.child` or `Inner.child_pid` after a wait. A source replacement cannot redirect cleanup or closure. Final current-source mutation rechecks association/H5; old cleanup may finish its old source observations without emitting successor rows.

## Handshake and all post-verification writes

Apply existing successor scoped handshake mechanics to legacy as a common private path: capability+H5+owning attempt+handshaking state check under source gate→Inner before declared capabilities, response identity, held-frame delivery, failure closure or LT09/LT11. Initialize and initialized writes use scoped source dispatch, including its existing final write/generation checks; a response obtained before Stop is not installation authority afterward. Failure handling may signal only its captured current source under the same gate, never call the unscoped current-PID kill helper. Stale success and stale error return without event/identity/ready mutation and without signalling a replacement.

Keep successor artifact publication outside operational locks, with its existing controller→Inner installation check and sequence fencing. Legacy has no fabricated successor evidence. Do not hold source gate while waiting for protocol response. Reuse frame-write→source gate ordering in native writes rather than taking frame_write while already holding the source gate; the two separate checks plus source-scoped dispatch prevent stale write/settlement without an inverse lock edge.

## Independent first-closure and first-exit components

Each installed source owns a bounded private aggregate with two independently once-set components and one bounded conflict indicator:

1. `ClosureObservation`: full H5/installation identity, first actual loss cause, first actual returned counts, and capture/persistence standing. Under source gate→Inner, verify owning source, execute existing close_generation effects in their existing order exactly once, retain returned counts and cause, then mark the closure captured. Later Stop/EOF/failure reads that component; it does not call close_generation again to obtain totals or retry already-applied effects. Existing queue/error state stays authoritative. Do not claim atomic durability: ledger absent, queued/unflushed facts or projection errors remain visible. A failure to persist does not authorize replay of execution/request closure. Unexpected unwind must poison/fail closed for further closure rather than reset to “not captured”; implementation must not catch it and silently replay effects.
2. `ExitObservation`: exact first actual child wait result/status and associated receipt/malformed/diagnostic fields, captured for that installed source. An absent wait result is not a successful exit observation. The first genuine status can arrive after closure. Exact duplicate is idempotent; contradictory later status preserves first and sets one bounded conflict/limit, not overwrite/sum/history growth.

Stop reaching its existing deadline before EOF obtains status can capture closure once and emit its actual LT23 with unknown exit fields. This event is immutable. It must **not** initialize ExitObservation with fabricated nulls and prevent later real observation. Late genuine EOF may fill the separate exit component for the old source, but cannot rewrite LT23, its artifact, a newer source, or repeat closure effects. A private captured-event record identifies which component versions were used when emitting the event; existing closed event schemas receive no new fields. At most one first component of each kind plus one conflict flag is retained.

EOF captures/reaps only its owned Child capability outside source/Inner locks, then takes source gate→Inner to associate the actual facts and close current source once. For an already closed old source, retain its late exit component separately without closing current registers. Stop-first EOF journals the existing exit fact and notifies; Stop reads first closure totals (D4 fix). Ready EOF emits unchanged actual LT12 using first captured exit/counts; later legacy-residual Stop can reuse first observations without rewriting earlier cause, but its invalid row is still a Part2 residual. Repeated EOF cannot replace counts with residual zeros or reclassify supplier-exit as supplier-stop.

## Lock order and liveness

- Start admission: REC writer→source gate→Inner; child handle publication occurs while gate excludes Stop. No scan/probe/Store under these guards.
- Stop/EOF/closure: source gate→Inner. No REC writer acquisition under these guards; existing persistence helpers only stage source-owned observations, and existing nonblocking flush happens after release.
- Child wait/grace and potentially blocking native IO: outside Inner/source/REC writer. Use captured source-owned handle, not a mutable shared later slot. Never acquire source gate while holding a Child mutex if another path holds source gate while waiting for that mutex; extract or snapshot the owned operation under a short handle lock, release it before gate reacquisition.
- Native protocol dispatch keeps existing frame_write→source file lock→source gate→Inner; do not invert it from handshake settlement.
- Terminal publication keeps existing Store/namespace work outside locks, then controller→Inner; no source→controller nesting. Admission/Stop reserve sequence under Inner, schedule after releasing source gate.

No new global lock, worker, queue, persistence store, timeout/SLA or automatic retry. Existing elapsed Stop bound is not strengthened to filesystem cancellation. Existing synchronous native spawn remains within the short custody boundary; no claim that OS spawn itself is wait-free.

## Concrete wider-window issue to settle before READY

A private installed token prevents an old mutable PID from being mistaken for a new attempt, but **does not itself prevent OS PID/PGID reuse after the leader is reaped**. Current on_eof calls Child.wait before source-gate capture; current Stop later uses killpg(pid). Part1 must not advertise a complete no-unrelated-group proof merely from token equality. The existing successor handshake failure helper has the same numeric-group limitation after a raced EOF.

Smallest safe Part1 interpretation: historical/reaped source identity alone never grants a new signal. Signals require a currently owned unreaped leader (or an independently existing warranted owned-group capability, which this source does not currently provide); if EOF has already reaped and group ownership is unresolved, return explicit cleanup unavailable without signalling or claiming no descendants. This must be assessed for its availability consequence against preserving the isolated post-LT12 residual. It cannot silently clear unresolved ownership to permit no-child LT21/22 or invent a survivor policy. If owner review requires signalling descendants after leader reaping, that demands a separately reviewed ownership mechanism/Part2 descendant treatment, not a row-switch workaround.

Also, holding Child mutex across wait currently blocks other child-slot access. Implementing captured source handles must remove this dependency without adding an inverse source-gate/Child edge; the exact extraction/non-reaping wait strategy needs independent lock/lifetime review before coding. This design is therefore **review requested, not self-declared READY**. No wider process-tree policy is selected here.

## Required deterministic regression plan

Preserve original temporary D2 version-gate control exactly: Stop returns before probe release, then both routes refuse with no child or later verification/event mutation. Add pre-final-gate/post-admission spawn schedules, late handshake success/error/contradiction, newer attempt and source replacement; verify no orphan after allocation failure and unchanged monotonic H5 behavior.

Test all direct no-child rows with null and retained historical H5/PID metadata using an inert signal-observation seam; prove no signal/wait/closure/counts/descendant fields and no late launch. Test wrong no-child guard against a genuine installed invented child, checked attempt overflow and unknown/duplicate state refusal before mutation. No arbitrary unrelated PID.

Preserve D4 actual unanswered client+server control: ordinary Stop LT23 uses first1/1 counts and actual exit0; EOF-first LT12 retains exit7/first1/1 and existing post-exit mapping remains explicitly not conformance. Add Stop-deadline-before-EOF, partial persistence/queued REC writer, repeated/contradictory exit/closure observations, old callback after newer source, and independent first-exit fill after first closure. Assert no duplicate closure effect/cause change/resend and no rewriting earlier immutable unknown event.

Run affected LT12/LT23/publication/namespace/old wrong-root and native handshake controls in both feature states once implementation is released. Independent exact candidate review, fresh committed existing-format cohorts and Group B named source-pin adoption remain required. No LT12 exchange or new row/shape inferred.
