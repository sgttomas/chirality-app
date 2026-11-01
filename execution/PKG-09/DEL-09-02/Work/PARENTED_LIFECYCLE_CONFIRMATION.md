# Lifecycle questions attached to the original App window

## Reason and retained result

The i7hfdeyc attempt reached actual source-bound ready/initialize and posted
Stop once on retained candidate `fdcf608fb5-23c6c3f22f5e` (source
`fdcf608fb57c4f8299c7440ffc56519314046cff`). It did **not** confirm Stop or
observe an accepted LT23/supplier settlement. It remains FAILED.
The visible question could not be derived from the original App's owned
WindowServer inventory, AXWindows or main-window AXSheets. No foreign UI was
inspected or clicked by the agent. The owner performed Cancel.

Readback of the same App/generation and restored enabled Stop control was at
2026-11-01 01:37:38.845114Z; one owned-menu Quit was posted at
01:37:39.429186Z. Original Child normal exit 0 and administrative wait 0 were
recorded at 01:37:54.849325Z. Helpers settled; slot 3 ended rc1. Reaping was
**47.303471 seconds after** the fixed end 01:37:07.545854Z. This was an overrun,
not a deadline extension or successful qualification. The resource-closure
record at 01:38:09Z reports individually queried App/Codex/keeper/slot absent,
run marker absent and shared memguard retained; it makes no exhaustive
supplier or detached-descendant settlement claim.

Original private evidence stays in
`/Users/ryan/dev/chirality-t3/scratch/app-successor-native-B-i7hfdeyc`:
`ready-observation.json`, `held-modal-readonly.json`,
`cleanup-cancel-binding-refusal.json`, `owner-cancel-readback.json`,
`cleanup-menu-action-result.json`, administrative release/result and
`resource-closure.json`. Full native AX/protocol text is not republished here.
Earlier failed attempts and preparations remain unchanged.

## Concrete source diagnosis

The retained `lib.rs::confirm_choice` never supplied a dialog parent.
`tauri-plugin-dialog` 2.7.2 initializes `MessageDialogBuilder.parent=None`;
its desktop conversion supplies a parent to rfd only when explicitly present.
`rfd` 0.16.0's macOS `MessageDialog::show_async` selects
`utils::async_pop_dialog` when parent is absent. That calls
`CFUserNotificationDisplayAlert`. Its parent-present branch instead constructs
an `NSAlert` and uses `beginSheetModalForWindow:completionHandler:`.
Thus the route's assumption of an App-owned NSAlert was not supported by the
candidate source. This identifies the selected backend; it does **not** identify
the actual process presenting the historical alert.

Both cached `.crate` SHA256 values matched the retained candidate's Cargo.lock.
The inspected plugin `src/lib.rs`, `src/desktop.rs` and rfd
`src/backend/macos/message_dialog.rs`, `utils/user_alert.rs` matched their
archive entries byte for byte. Read-only source inspection loaded no native API.

## Narrow product repair

`native_lifecycle_confirmation` parents Stop/Restart to the actual Tauri IPC
invoker. Menu Quit retains the configured `main` window before starting its
worker; it does not choose a focused/first/replacement window at presentation.
The default configuration's sole window has Tauri's `main` label.

On the main thread the helper obtains both original window/display handles
and caches the successful borrows. The plugin's `.parent()` silently ignores
handle errors, so passing the checked borrows is essential: unavailable handles
refuse before presentation, without a parentless fallback. The callback API
keeps the main thread available. Only the command/quit worker waits. An
affirmative result rechecks the retained original window on the main thread;
an unavailable original refuses rather than authorizing the act elsewhere.

Question generation, in-App content disclosure, default-safe button ordering,
explicit custom action matching, source/generation/work-change rechecks,
Stop/Restart/Quit decision sequencing and settlement limits remain unchanged.
Presentation changes: sheets attached to one window can queue behind an
already-open sheet. In particular, a Quit refusal notice cannot dismiss an open
Stop sheet, and a Quit question may wait behind another family's sheet.
Overflow content remains inline in the App; its readability/scrolling while a
sheet is attached is unverified. The zero-work qualification does not cover
that case. Cancel,
Escape and the default Keep choice remain non-actions. Invalid statements still
produce a refusal, not a person's cancellation. Explanatory Quit refusals use
the same retained parent; when unavailable they are logged without an unowned
alert. Other confirmation families and SEAL-C code are outside this repair.

## Recovery prerequisite for the next candidate (not a live-ready claim)

Parenting selects a sheet, so the old requirement that every question be a
separate root in AXWindows is **not** assumed sufficient. Before requesting a
live interval, the admitted controller must implement/test this exact method:

1. Retain original Child birth/path/hash, exact main window and full source /
   account / generation from the successful ready observation. Resolve that
   main's AX object through the existing owned window-number bridge and record
   its `AXChildren` and the owned WindowServer inventory before the one Stop
   press. Never rediscover a main by focus or pick a replacement.
2. The discovery path is **original-main AXChildren → AXRole == AXSheet**.
   `AXChildren` must succeed with an array; unsupported/error/truncation is a
   refusal, not an empty list. Enumerate only its bounded direct children,
   deduplicate AX references and require exactly one newly attached sheet.
   Its `AXParent` must equal the retained original-main AX object and map to
   the same main window number: only `original-main-window-parent` is accepted.
   `owned-application-parent`, missing/contradictory parent data, and a role scan
   of the application's roots do not establish this relation. Main `AXSheets`,
   if exposed, is corroboration only and must not contradict that relation.
   Require the sheet to map to its **own distinct newly visible original-App
   WindowServer row**; a sheet mapping to the main row, no row or a foreign row
   remains unsupported. No main-image substitution is allowed. The existing
   `modal_relation` implementation does not implement this contract and must
   not be used unchanged for the new route.
3. During the question, the App must be `AXFrontmost == true` before a press,
   the retained main must remain `AXMain == true`, and `AXFocusedWindow` must
   map to the derived sheet. The expected macOS key window is the sheet; this
   route relies on its AX focus observation, not an invented `AXKey` attribute
   or a foreign/global key-window query. If macOS instead exposes main as the
   focused window, the route refuses and retains that fact; there is no silent
   alternate focus rule. Require the derived sheet to be foremost in the owned
   on-screen inventory. Corroborating capture is of that exact sheet row only,
   with unchanged original identity and complete request/helper equality.
   A main capture cannot stand in for the question. Require the complete exact
   Stop question and exactly the three enabled expected buttons before
   qualification confirmation. Source, generation and immediate pre-press
   revalidation remain mandatory.
4. For cleanup-only cancellation, require fresh original identity, that same
   derived sheet/parent/window/focus binding, and exactly one enabled native
   Cancel. Retain intent before one AXPress and consume the action before
   dispatch. Never treat the owner screenshot, guessed text, Escape or
   coordinates as a substitute. A question-gate refusal cannot become a
   positive Stop result. An uncertain Cancel delivery is not repeated.
5. Verify the sheet is gone from original-main `AXChildren` and the owned
   on-screen inventory; require original main still `AXMain == true`, original
   App frontmost and `AXFocusedWindow` mapping back to that main before any
   further content action. Capture, if required, is again the exact original
   main with fresh full equality, not reused pre-sheet geometry. Read back the
   same-source main state before the one owned-menu Quit; do not press Quit
   while the Stop sheet remains, because the Stop gate refuses it and its
   explanatory notice could queue behind the sheet. Observe original Child
   normal exit 0 and settled helpers before exact offered atomic administrative
   release. Qualification stays false after any refusal.

This is the concrete recovery contract to implement and review; this product
PR does not add controller permissions or assert native sheet observability.

### Fixed-budget allocation and unresolved terminal case

The total remains 295s. Recovery **replaces** the unused 45s settlement phase;
it does not follow it or add another phase. The existing phase table leaves
85s after the 30s modal phase (45s settlement plus 40s exit). Recovery uses at
most 20s for binding/actions/readback and retains the unchanged 40s exit
reserve, fitting within that 85s without changing any cap. Latest recovery
entry is **fixed end minus 60s**; qualification must stop early enough to enter
by then. If that entry point has passed, no new cleanup input is dispatched on
an expired budget; report the actual held state immediately.

The 20s action allocation is four consecutive caps: 5s fresh sheet binding,
5s for one Cancel and its native-call return, 5s dismissal/source readback,
5s owned-menu Quit publication. Each new sheet AX element must have an
explicit successfully set **0.2s messaging timeout** before any attribute read
or action, matching the existing AX route. No default timeout is allowed.
Each step allows at most 20 AX calls and checks its cumulative monotonic
deadline and the fixed end between calls. Do not enter another call when less
than its timeout remains. These limits include identity/evidence/tool overhead
inside the step, not an idealized AX-only duration; any overrun refuses. No
asynchronous operator or parent round trip is part of this recovery path.

The prior actual cancel-readback→Quit cost was 0.584s and
Quit→administrative reap 15.420s; these are single observations, not upper
bounds. New sheet acquisition/AX press/readback costs are **unmeasured**.
A tested bounded recovery implementation and explicit cost allowance must fit
these caps before a new interval; this document alone does not prove fit.

**Unresolved prerequisite:** if the sheet cannot be uniquely bound/cancelled,
normal menu Quit cannot close the App while the Stop gate is held. Current
authority admits no App/supplier signals, force termination, blind dismissal,
or administrative reaping of a live Child. At fixed end the manager must stop
inputs, report the exact condition, retain original custody/guard and report
any overrun; it cannot truthfully promise resource release. Parent notification
and a concrete owner Cancel request must occur immediately on the unsupported
condition, not at the deadline, but owner availability is not a bounded-exit
guarantee. The previous 47.303s overrun remains failed evidence.

Before another live interval, Agent 0 must choose a concrete terminal method
for this exceptional case or explicitly accept that supervised custody may
outlast the resource interval. Recommended: resolve a narrowly reviewed
product-owned cancellation/recovery method first, keeping forced process exit
outside the current scope. This product PR supplies neither such method nor
new authority. No new launch is scheduled; a source build alone does not clear
this prerequisite.

## Verification and ownership reconciliation

Local verification: 6 new parenting tests, 37 existing Stop tests and 18
existing Quit tests passed offline with jobs2 and serial tests through t3_slot,
using a private COW Cargo cache/target and fresh scratch Codex home. The new
cohort is added once to CI shard B; 62 CI-selection tests passed. Deliverable
structure check reported no errors. Logs are retained in
`/Users/ryan/dev/chirality-t3/scratch/app-parented-lifecycle-9bg_3bjr`:
`test-0.log` (6), `test-1.log` (37), `test-2.log` (18) and
`ci-selection-pytest.log` (62). The earlier `ci-selection.log` ran zero tests
and is not passing evidence. Those local logs did not embed a source SHA;
formatting followed the first six-test run. The independent reviewer reran
those six tests at exact `979ea1fd23073ecf62899f122659f3c04d4a2a70` with a
fresh scratch home: 6/6 passed, no rebuild, log
`/Users/ryan/dev/chirality-t3/scratch/pr68-review-PCSpTLs7/test.log`.
The other cohorts were inspected, not independently rerun.

Claude Opus 5.5/high reviewed that exact product delta against `366e7a66` and
found no blocking product defect. The recovery contract corrections in this
note address that review; they are manager edits, not a claimed clean rereview.
Main-thread scheduling/channel lifetime and native sheet behavior were source
inspection only. No candidate build or native execution was part of the review.

Focused tests exercise cached parent handles, unavailable window/display,
destroyed original at affirmative result, safe buttons for Stop/Restart/Quit,
presentation refusal and invalid-statement reporting. The existing Stop and
Quit sequence cohorts check their unchanged lifecycle effects. These are
mock/source checks, not observed native sheet behavior or human acts.

DEL-01-04 owns this native Stop/Restart interaction repair. DEL-09-02 receives
it for the next identified
candidate under REQ-004/005/007/008; no qualification acceptance or scope/needs
change is made. The DEL-01-04 Work note links this account; no separate DEL-01-03
contribution or Work note is claimed. A new build must have
its own source/bundle/namespace identity; the retained fdcf bundle/state are
never relabelled, overwritten or reset. Build only after the product boundary
is reviewed; exact source and fresh admission must include the chosen route
and recovery implementation before live use.
