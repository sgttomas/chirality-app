# Exact App-owned sheet recovery backend — inactive

This follow-on is separate from PR68's reviewed parenting repair. Agent 0
selected product-owned bounded cancellation/recovery, without force exit or
reliance on owner response time. **No lifetime policy is activated here.** The
current PR68 presentation path still runs. The new backend has no caller,
public command, IPC capability, environment switch or control file.

A universal 30-second Stop/Restart/Quit expiry would shorten human reading
and overflow-content review time. Agent 0 has referred that product choice to
the owner and recommends preserving unrestricted human reading time. The
mechanism can be reviewed separately, but neither that proposed lifetime nor
a qualification-only activation has been adopted. Do not infer a ready build
or live interval from this source contribution.

## API basis and implementation

The existing plugin/rfd API returns a result, not a retained cancel handle.
Looking up `attachedSheet` after presentation would risk choosing another
question. Instead, `lifecycle_sheet_macos::show` creates and retains the exact
NSAlert, its window and the original App NSWindow on the main thread. It uses
the caller's checked borrowed AppKit handle, never app/focus/window discovery.
An existing attached/queued sheet, occupied lifecycle slot, hidden/miniaturized
parent, a parent that is itself a sheet, or another app-modal window refuses
before display; there is no queue or alternate parent. The App event loop must
be running. These native predicates have a pure tested admission decision.

The cached, locked bindings are objc2 0.6.4, objc2-app-kit and
objc2-foundation 0.3.2, block2 0.6.2 and dispatch2 0.3.1. Cargo.lock changes only
the root crate's direct dependency edges, not package versions or checksums.
No downloads or native API probes were used. Relevant inspected APIs:

- NSAlert `beginSheetModalForWindow:completionHandler:` and `window`.
- NSWindow `sheets`, `attachedSheet`, `sheetParent`, `endSheet:returnCode:`,
  `orderOut:` and `isVisible`.
- DispatchQueue main `after`, using a monotonic duration-based DispatchTime.
- NSAlert button order: first=1000 (Keep), second=1001 (act), third=1002
  (Cancel); Return defaults to first and the Cancel title gets Escape.

The backend accepts only the existing three custom lifecycle buttons or an
informational OK notice. It preserves their labels and presentation order.
The lifetime is an internal required argument; this file supplies no product
value or activation rule.

Each pending sheet has a private never-reused numeric identity. Native objects
stay in main-thread-local storage; a delayed main-queue timer carries only the
identity. No pointer or native object is sent to a worker. Stale timer/callback
identities cannot address a subsequent question. An early timer callback schedules the remaining duration without
moving the original deadline; at most two early rechecks are permitted before
an explicit hold. The single end request is still consumed before dispatch.
The clocks measure awake time: system sleep is not a fixed-wall-clock cleanup
guarantee and must not be hidden in native timing evidence.

At expiry, the lease is marked nonaffirmative **before** the one end request.
Fresh native object identity must show that the exact sheet's sheetParent is
the retained original and that parent's attachedSheet is the same retained
sheet. The App calls that parent's `endSheet` for only that sheet, with
NSModalResponseCancel. This is the App ending its own question, not an agent
AX press or a recorded person's Cancel. No AX binding is needed.

The completion callback orders out only that retained sheet, verifies no
sheet-parent relation, visibility or original-parent sheet-list entry remains,
then reports the result. Verification runs on later main-queue turns (50ms
spacing), limited to 20 checks and one second from completion; the first
transient attached reading does not permanently hold the backend. If original
relation/dismissal cannot be established within those bounds, it retains native
custody and the final-result sender. A separate private status channel emits
`Held` once so an observer can distinguish unsupported custody from reading.
The absence of a completion one second after the end request also reports
Held. A later completion may verify dismissal and release custody, but once
held its result remains nonaffirmative. No alternate target or repeated end
request is attempted.

At result interpretation, a monotonic deadline check also rejects a late
answer even if the timer's main-queue callback was delayed. Expiry returns a
refusal/expired error, never `Custom(Stop)`, affirmative Quit, or a fabricated
person-cancel result. Unknown native result codes also refuse. Normal known
button results remain subject to PR68's original-window recheck and the
existing lifecycle source/generation/work-change gates **when wired**.

## Remaining integration and authority work

The current caller is unchanged. Activating this backend requires an explicit
lifetime/presentation choice and a separately inspected wiring delta. A short
universal product timeout is not adopted just to fit qualification budgets.
A qualification-only policy would instead need a precise nonrelease source /
configuration boundary, default-off behavior and truthful limits on what that
candidate qualifies; this document does not create such a policy.

Controller recovery would wait for expiry/dismissal, read back the same App /
window / generation with the Stop control restored, and only then use the one
owned-menu Quit. It must distinguish expired/refused from owner cancellation
and retain failed qualification. No invented successful Stop or LT23 is allowed.
The existing PR68 `receive.recv()` must **not** be used as unchanged wiring
for this backend: the future caller must use bounded supervision, consume Held
status and preserve the original lifecycle question gate/custody separately
from reporting that failure. The new status sender alone is not that wiring.
All lifecycle sheets must use one gate; other plugin sheet families can still
race to open after admission and need explicit integration handling.

The exact native question grammar, focus/image contract and timing admission
must match the chosen presentation. Unlike rfd, this backend has no
FocusManager/PolicyManager: it does not restore a previous key window or change
activation policy. Focus after dismissal is therefore not presumed equivalent
to PR68, and subsequent capture/control must freshly establish the original
App/main focus without adding an automatic focus fallback. There is no controller change in this PR.

A functioning AppKit/main event loop is required for both cancellation and
completion. Main-thread stalls and failed native dismissal remain unsupported holds.
An Objective-C exception or Rust panic escaping a dispatch/block callback may
**abort the App process**, not preserve custody: no exception containment is
implemented here. A button may start ending the sheet before its completion
callback arrives, so a deadline endSheet could race with AppKit's own ending;
although duplicate callbacks cannot authorize twice, exception-free behavior
is unverified. Both normal-button and expiry ordering need native qualification
under an explicitly adequate recovery method before activation. The present
inactive source is not a ready recovery solution or a finite hard-closure
guarantee.
Original Child/guard custody remains required, with immediate parent reporting.
The existing 295s total and 40s exit reserve are unchanged. New native costs are
unmeasured, so no live interval is scheduled or requested.

## Tests and standing

The pure lease tests cover early answer, exact deadline, late callback before
timer service, once-only expiry consumption, stale timer and stale callback
against a later question. The repaired focused library run passes 18 tests: the original five lease
checks, seven new admission/result/dismissal/early-timer cases, and six original
parenting tests. New cases exercise native response codes 0, -1000, -1001,
1000–1003, the single-OK case, bounded delayed detachment, occupied/hidden/modal
parent refusal, and held expiry followed by late verified completion. It compiles the macOS adapter but invokes
no AppKit/AX/window/capture/input API. It does not establish native dismissal,
queue timing, visibility or end-to-end cleanup.

Local scratch is
`/Users/ryan/dev/chirality-t3/scratch/app-parented-lifecycle-9bg_3bjr`;
`bounded-review-fix-tests.log` records the repaired focused run;
`bounded-exact-head-tests.log` and its provenance retain the earlier 7fdb470b
11-test subject rather than being relabelled. Build/test used the
private COW cache/target, scratch Codex home, offline/locked dependencies,
jobs2, serial tests and t3_slot. Old candidate/state/evidence are untouched.

DEL-01-04 remains the interaction owner; DEL-09-02 receives only an inactive
recovery implementation and its limitations. No ScopeOfWork, acceptance or
needs change is claimed. Claude Opus5.5/high reviewed exact 7fdb470b versus 48d4ca8c. The review
identified notice-input drift, one-shot dismissal verification, invisible holds,
early-timer loss, presentation differences and missing pure tests. These
manager fixes address the concrete source/test issues; the exception, native
ordering and future wiring limits above remain explicit. No clean rereview or
execution approval is claimed. Material activation/wiring needs meaningful
scrutiny; PR68's earlier review is not relabelled as this native-boundary review.

## Current-source consumer repair after CI

CI at `7fdb470b` compiled the new native source but the package→EXP→SQ cohort
stopped in setup: its current source profile still pinned the earlier Cargo
manifest/lock. The maintained
`app/examination/package_receiving/generate.py` rederived only those two source
digests and their dependent profile/reader hashes in four files. No receiver
acceptance rule, historical profile or native backend changed. The focused
joined cohort then passed 20 tests and 15 subtests offline under t3_slot;
`pr69-package-cohort.log` and the original CI failure log remain in the private
scratch above. Re-derivation does not establish package/native qualification.

The packaging owner supplied an apply-ready patch SHA256
`2cbcc45cefe135cf07b704bb9f8bfc07a12ef45d48cbbcbd70dbd062a30c89ff`,
applied without overlap. Its v2 input explicitly covers common plus macOS-arm64
target-specific direct runtime declarations and preserves historical v1 meaning.
All 13 notice tests passed after application. The owner checked all 18 selected
Cargo archives offline; five lack root notice text and are explicit gaps.
The current index/asset correspondence is true, notice-text coverage remains
incomplete, and no missing text/asset or legal/release claim was invented. See
DEL-01-06 Work/PR69_MACOS_NOTICE_INPUTS.md. No retained build was modified.
This reconciliation is separate from the four generated receiver-pin files.

### Recorded-replay fixture synchronization

Shard B at `ac910cc1` failed in the existing recorded-ST5 relaunch fixture:
`stored_entries` reopened the disk ledger concurrently with its Host writer,
and SQLite's transient journal failed the physical single-link guard. The
fixture's `ledger()` now holds that same Host ledger mutex during its independent
reopen. It still reads the persisted database and preserves the product guard;
no production recovery or native lifecycle code changes. The full six-test
recorded-replay cohort passed offline/locked, jobs2/serial under t3_slot after
the repair. Original CI failure and `pr69-recorded-replay-fix.log` are retained
in the private scratch above. No sleep/retry or weakened assertion was added.
