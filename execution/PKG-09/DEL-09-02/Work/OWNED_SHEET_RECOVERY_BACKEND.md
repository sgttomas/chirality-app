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
An existing attached/queued sheet or existing pending lifecycle sheet refuses
before display; there is no queue or alternate parent.

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
identities cannot address a subsequent question.

At expiry, the lease is marked nonaffirmative **before** the one end request.
Fresh native object identity must show that the exact sheet's sheetParent is
the retained original and that parent's attachedSheet is the same retained
sheet. The App calls that parent's `endSheet` for only that sheet, with
NSModalResponseCancel. This is the App ending its own question, not an agent
AX press or a recorded person's Cancel. No AX binding is needed.

The completion callback orders out only that retained sheet, verifies no
sheet-parent relation, visibility or original-parent sheet-list entry remains,
then reports the result. If original relation/dismissal cannot be established,
it retains pending custody and the sender instead of releasing the question
gate. This is an explicit unsupported hold, not claimed closure. No alternate
target or repeated end request is attempted.

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
The exact native question grammar, focus/image contract and timing admission
must match the chosen presentation. There is no controller change in this PR.

A functioning AppKit/main event loop is required for both cancellation and
completion. Main-thread stalls, native exceptions and failed native dismissal
remain unsupported conditions; no finite hard-closure guarantee is made.
Original Child/guard custody remains required, with immediate parent reporting.
The existing 295s total and 40s exit reserve are unchanged. New native costs are
unmeasured, so no live interval is scheduled or requested.

## Tests and standing

The pure lease tests cover early answer, exact deadline, late callback before
timer service, once-only expiry consumption, stale timer and stale callback
against a later question. The focused library run includes these five tests
and the six original-parenting tests. It compiles the macOS adapter but invokes
no AppKit/AX/window/capture/input API. It does not establish native dismissal,
queue timing, visibility or end-to-end cleanup.

Local scratch is
`/Users/ryan/dev/chirality-t3/scratch/app-parented-lifecycle-9bg_3bjr`;
`bounded-backend-final-tests.log` records the focused run. Build/test used the
private COW cache/target, scratch Codex home, offline/locked dependencies,
jobs2, serial tests and t3_slot. Old candidate/state/evidence are untouched.

DEL-01-04 remains the interaction owner; DEL-09-02 receives only an inactive
recovery implementation and its limitations. No ScopeOfWork, acceptance or
needs change is claimed. Independent Claude Opus5.5/high scrutiny is required
before activation; no earlier review of PR68 is relabelled as review of this
new native boundary.

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

Before a new candidate build, the packaging owner must reconcile the direct
runtime notices with the five already-locked macOS target-specific dependencies
now directly named in Cargo.toml. The current notice index binds the old
manifest/lock, and its checker enumerates top-level direct dependencies only.
That concrete source/coverage gap was reported to Agent 0 for packaging
ownership; no old notice input is claimed current and no retained build was
modified. It is separate from this receiver-pin repair.
