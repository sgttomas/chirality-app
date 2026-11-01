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
Stop/Restart/Quit sequencing and settlement limits remain unchanged. Cancel,
Escape and the default Keep choice remain non-actions. Invalid statements still
produce a refusal, not a person's cancellation. Explanatory Quit refusals use
the same retained parent; when unavailable they are logged without an unowned
alert. Other confirmation families and SEAL-C code are outside this repair.

## Recovery prerequisite for the next candidate (not a live-ready claim)

Parenting selects a sheet, so the old requirement that every question be a
separate root in AXWindows is **not** assumed sufficient. Before requesting a
live interval, the admitted controller must implement/test this exact method:

1. Retain original Child birth/path/hash, exact main window and full source /
   account / generation from the successful ready observation. Record owned
   inventory and the parent's AXSheets immediately before the one Stop press.
2. Read only that exact parent's AXSheets and original App AXWindows. Admit
   exactly one newly presented native sheet, related to that parent, mapped to
   a newly visible original-App WindowServer window. Deduplicate references;
   no foreign owner, unrelated AX root, unmapped surface or replacement main.
3. Require the complete exact Stop question and exactly the three enabled
   expected buttons before qualification confirmation. Preserve strict source,
   generation, frontmost, image and late-revalidation gates.
4. For cleanup-only cancellation, require fresh original identity, that same
   derived sheet/parent/window binding, and exactly one enabled native Cancel.
   Retain intent before one AXPress and consume the action before dispatch.
   Never treat the owner screenshot, guessed text, Escape or coordinates as a
   substitute. A question-gate refusal cannot become a positive Stop result.
5. Verify disappearance from the original parent's sheets/owned inventory and
   restored same-source main state before the one owned-menu Quit. Observe
   original Child normal exit 0 and settled helpers before exact offered atomic
   administrative release. Qualification stays false after any refusal.

This is the concrete recovery contract to implement and review; this product
PR does not add controller permissions or assert native sheet observability.
If that relation cannot be established, there is no autonomous safe Cancel
route: notify the parent immediately with the held state and concrete owner
Cancel instruction, retaining custody. That contingency is not an achievable
fixed-budget recovery guarantee.

The existing total remains 295s, with its 40s exit reserve. The proposed
cleanup allocation is 5s for fresh sheet binding, 5s for the one Cancel and
its native-call return, 5s for dismissal/source readback, 5s for owned-menu
Quit publication, then the unchanged 40s for original-child/helper exit and
release: **60s remaining at recovery entry**. Before Stop, reserve that entire
amount in addition to the allowed qualification modal-acquisition/question
time. This is a proposed admission minimum, not an extension of a phase. The prior actual
cancel-readback→Quit cost was 0.584s and Quit→administrative reap 15.420s;
these are single observations, not upper bounds. New sheet acquisition/AX
press/readback costs are **unmeasured**. Reserve at least the unchanged 40s for
exit and do not borrow it for diagnosis or parent round trips. A tested bounded
recovery implementation and explicit allowance for the new sheet costs must
fit existing phases before a new interval; this document alone does not prove
that fit. No live launch is scheduled by this repair.

## Verification and ownership reconciliation

Local verification: 6 new parenting tests, 37 existing Stop tests and 18
existing Quit tests passed offline with jobs2 and serial tests through t3_slot,
using a private COW Cargo cache/target and fresh scratch Codex home. The new
cohort is added once to CI shard B; 62 CI-selection tests passed. Deliverable
structure check reported no errors. Logs are retained in
`/Users/ryan/dev/chirality-t3/scratch/app-parented-lifecycle-9bg_3bjr`.

Focused tests exercise cached parent handles, unavailable window/display,
destroyed original at affirmative result, safe buttons for Stop/Restart/Quit,
presentation refusal and invalid-statement reporting. The existing Stop and
Quit sequence cohorts check their unchanged lifecycle effects. These are
mock/source checks, not observed native sheet behavior or human acts.

DEL-01-04 owns the native Stop/Restart interaction repair and DEL-01-03 the
native presentation contribution. DEL-09-02 receives it for the next identified
candidate under REQ-004/005/007/008; no qualification acceptance or scope/needs
change is made. The owning Work notes link this account. A new build must have
its own source/bundle/namespace identity; the retained fdcf bundle/state are
never relabelled, overwritten or reset. Build only after the product boundary
is reviewed; exact source and fresh admission must include the chosen route
and recovery implementation before live use.
