# A15 confirmation on the invoking App window

The first J2 registration attempt on source `0464812488fbc81f4c6c6e15de23d4fb4d3db9e0`
published the complete frozen review and waited for a native result, but the
App's native controls exposed no confirmation. Registration and reuse were not
established. The original App normally quit; that evidence remains a partial
J2 result, not a registration witness.

The source defect is in the presentation boundary: `workflow_register_native`
passed only an App handle and `a15_native` opened a parentless blocking dialog.
The locked `tauri-plugin-dialog` 2.7.2 defaults to no parent; locked `rfd` 0.16.0
selects its CF user-alert path on macOS when no parent is supplied. Its owned
parent route selects an NSAlert sheet. The retained observation cannot establish
where an OS alert appeared or why it was not accessible. This is the same
presentation mismatch previously repaired for setup and lifecycle questions.

The repaired command supplies its actual IPC-invoking window. A15 validates and
caches that original window's window/display handles and presents a parented
callback dialog in one main-thread turn. Only the async command worker waits.
No focus/label lookup, replacement window or parentless fallback is permitted.
An affirmative result revalidates the original window before returning to the
existing actor, owning-home/library/review, frozen-content and ledger checks.
Scheduling, parent or missing-result failures refuse without capture and remove
the temporary in-App content. Only the exact middle **Register** or **Re-confirm**
label can produce the opaque native event. Default, decline and cancellation
meanings, review digests, records and no-automatic-retry behavior are unchanged.

Focused offline checks cover cached parent handles, missing window/display,
destroyed original after either affirmative label, missing callback result,
presentation errors with no capture/log and withdrawn review content, and the
existing A15 capture/content/freshness/default-choice regressions. They use
invented stand-ins, not actual native dialogs or personal acts. No supplier,
sign-in, model, App build/launch or J2 rerun is part of this source repair.
Actual repaired-candidate presentation and the joined J2 registration/reuse
remain with Agent 0's separately authorized native session.

Local verification: the offline locked Rust lib filter `a15` passed **33/33**
serial cases, including the five new parent/refusal cases and the existing
capture/default/freshness cases. The CI selection tests passed **62/62**;
deliverable structure reported **41 deliverables, zero errors**. Maintained
`t3_slot.sh` wrapped these checks, with fresh scratch OS/Codex/temp homes and
private copy-on-write prepared Cargo inputs, jobs 2 and supplier execution
disabled. CI now selects the new parent/refusal tests and existing exact-button
capture regression explicitly. These results qualify the source change only.

Reconciliation: DEL-01-04 REQ-008/OUT-005 and its DEL-02-02 input still require
the same content-bound native A15. This repair supplies the missing owned-window
presentation, with no new upstream condition, acceptance claim or scope change.
