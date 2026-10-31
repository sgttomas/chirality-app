# Owned-window B route and retained-state/v2 preparation

Agent0 deferred the in-process C comparison: do not wire or load it. Its merged
source, reviewed build/staging artifacts and crash limits remain retained.
This route instead uses the existing original-Child keeper, public WindowServer
identity and the system capture tool in a separately supervised process. It is
preparation only: no additional App launch, screenshot or native input has run.

## One practical route, not another AX root-cause experiment

Available connector device screenshots capture a device screen, not this exact
owned window; browser preview tools are not the native desktop surface. The
existing A controller already used `/usr/sbin/screencapture -l`. Its installed
usage supports the narrower `-x -a -o -t png -l <windowID>` command: no sound,
no attached windows, no shadow, PNG, one window. No desktop rectangle/monitor,
clipboard, interactive selection, graphical-error, permission-request or fallback
capture option is used. System tool and Python executable identities are bound
in preparation and rechecked. The App/Codex sandbox executable list stays exactly
App + bundled Codex + mktemp; keeper-side helpers do not expand supplier exec.

The keeper freshly checks its original Child with WNOWAIT, kernel birth/parent/
UID/path and inventoried executable hash. WindowServer rows are owner-filtered
before decoding; exactly one visible layer0 window with the retained main title
is required. Its ID/title/bounds are bound before and after capture and input.
Initial window construction gets a bounded15-second read-only readiness wait;
absence, ambiguity and capture refusal are distinct. Permission is preflighted
in the keeper and helper; false refuses without a prompt or settings change.

A copied, hash-bound Python helper lives in the sandbox-denied private controller
root and runs with isolated/no-site imports from protected sibling copies. For
capture it revalidates identity/window/permission and execs the fixed system tool.
The keeper retains the helper's own Popen separately from the App Child, waits
four seconds, and on timeout kills **only that retained helper**, then waits one
second. This is not a numeric App/supplier signal. If helper settlement remains
unknown, no second helper or administrative App release is allowed; its actual
Child reference, keeper/guard/slot remain held and the state reports that limit.
A helper crash does not kill or reap the original App keeper. Detached helper
scope is not converted into an exhaustive process-cleanup claim.

Capture output initially has an `.unverified.png` name. Only matching post-
identity/window checks, regular-file/size/PNG validation and exact integral
pixel-to-point scale admit it as `window-NNN.png` with a receipt. Never view or
export an unverified image after a binding failure. Before/after WindowServer
checks are not an atomic lifetime handle for a window number; an unavailable or
changed binding is refused, not represented as a valid image. The image is only
this window; attached native dialogs are deliberately excluded.

## Ordinary UI operation and observations

The profile exposes a fixed B-only operator loop: focus the owned App, click a
currently observed disclosure (Host diagnostics, Lifecycle, Raw envelopes or
Connection/access), scroll inside the main window, observe, refuse, and later
one gated Stop click. No keyboard text, sign-in/provider/model/thread/tool action,
arbitrary command or generic automation interface is accepted. Click/scroll
requires fresh App-frontmost observation, exactly one owned visible layer0
window, current geometry and a point inside the receipt's original pixel bounds.
Coordinates are mapped only with the verified pixel/point scale; no guessed
inset or old coordinates. A new capture immediately before input must match the
image-data/rendering-metadata fingerprint and geometry. Drift posts no event and
requires rereading the new capture. Focus has its own actual AXFrontmost readback.

Input is posted only to the original App PID, revalidated by the isolated helper;
mouse flags are cleared, click count is one, and scrolling is one bounded axis.
Return codes and posted events are not proof of UI effect. Each action is followed
by a verified capture. The next action requires an agent statement that the
actual expected effect was read there. Unknown/unexpected effects must use
`refuse`, not an assertion or automatic retry. An ambiguous helper failure keeps
that readback requirement. Prequeued controls are refused. The semantic target
caption/point and visual readback are agent observations, not machine-verified
DOM selectors; the private control channel is protected from App/supplier writes,
not claimed to authenticate every process sharing the host UID.

Use `view_image` with original detail only for the path in the current verified
receipt. Operator points use that receipt's original PNG pixel dimensions, not a
resized thumbnail. Each prompt names its new `screen-control-NNN.json`; create a
plain owned single-link0600 file only after reading the prompt/image. It binds
candidate, admission SHA and current capture SHA. Controls cannot be batched
before actual effects. The observer keeps its guard and deadline active while
waiting; the manager must stay active and report failures/resident state promptly.

An `observe` control supplies actual complete displayed strings for the state/
generation header, Lifecycle+clientRequests JSON and raw envelope JSON, with
references to verified captures from **this observation phase**. It must mark
those sections complete and readable. Never fill a missing field from the saved
A tuple, a previous phase, source expectations or guessed pixels. Those are
comparison inputs only. Raw strings, captures and decoded observations are
retained with `agent-transcribed-owned-native-UI` provenance. No synthetic AX
window or native snapshot is fabricated. Truncation, unreadable text, uncertain
request completeness or mismatched source must refuse. No clipboard or opaque
supplier-file read is used to obtain the text.

Existing `decode_diagnostics`, full account/generation/source checks, expected
request checks, ready gate and LT23 leader/descendant settlement gate remain in
force. The B-only Stop click is available only after a bound generation and is
never silently repeated after ambiguous delivery. Its native confirmation still
uses the existing owned AX dialog read and exact account/session/spawn-counter
checks. The actually read question is effect evidence before confirmation. If
that native dialog remains inaccessible, the route refuses; it does not capture
an extra window or invent a confirmation from pixels. An unexpected Quit live-
work question is preserved for an explicit confined-effects disposition, not
automatically confirmed by this route.

After known settlement, normal Quit uses the exact owned App-menu object, not a
cached coordinate or keyboard shortcut. Failure with missing source/observation
keeps FAILED/unknown standing. The separately selected owned-menu cleanup and
normal-exit0, admission-bound administrative release remain available under a
live disposition; administrative release now also requires the capture/input
helper to be settled. No B pass or supplier settlement follows from cleanup.

## Explicit v2 state and execution budget

`native_b_retained_v2.py` preserves A-only and v1 unchanged. It binds the exact
saved request, original A/candidate/root identities, fixed post-am98 assessment,
source/schema digests, current owned metadata and six schema-valid rows across
two distinct quit-ended sessions with empty recorded work/stop lists. The second
start must link to the first session and read its end as clean. App ledger SHA:
`2d09bb9af4a653c3eca7fc663f32096664f2dfd2fd1307c07fa38f12bb4b164c`.
The current metadata must exactly match the retained assessment, including the
three observed supplier WAL/SHM additions. Supplier contents remain opaque.
App ledger no-WAL/SHM/journal/no-observed-open-descriptor checks and immutable
read-only/query-only hash/metadata stability are repeated before/after reading.
Unknown observations, auth additions, missing/changed facts, unexpected links,
ownership or unexplained metadata drift refuse; no reset or synthetic freshness.

Preparation copies the capture/input sources and the fixed slot-entry shim into
a new private attempt. After actual slot acquisition the shim exclusively records
its PID/parent/admission/source binding and an absolute end295seconds later, then
execs the unchanged bound controller. Execution verifies that exact slot record,
re-admits v2 state/source/tool/policy/copies and rechecks the complete candidate
inventory and current guard/slot gates. Queue time is not the native allowance;
the end is never extended. The ordinary180-second work budget and remaining
cleanup deadline apply, with six seconds required before launching any helper.
No live run is authorized by preparation. Report actual overrun/resident facts;
no finite budget is a guarantee that all UI/cleanup observations will succeed.

The C comparison and prior standalone WindowServer/raw-AX diagnostic are not
called on this v2 screen route. WindowServer checks here serve current target
binding, not repeated window-existence hypotheses. Parent decides live execution
after meaningful Claude Opus5.5/high scrutiny of these capture/input/cleanup
changes. Tests use mocks, invented PNG/SQLite data and harmless child processes;
they are source/boundary evidence, not actual GUI qualification.

## Concrete unrun preparation

Read-only capture/preparation succeeded against the unchanged six-row assessment.
Final proposed basis `/Users/ryan/dev/chirality-t3/scratch/app-owned-window-prep-aqsif0fz/retained-v2-proposed-inputs.json` has SHA256
`990f9ae64d51eac3ee1787de440dd16e32b7a29655dd52f64c5da4a2142eb98a`. The new attempt is
`/Users/ryan/dev/chirality-t3/scratch/app-successor-native-B-u3ug__xe`, admission SHA256
`8b6245534baa20881330689cf2fe863adbdfde230f237bbdb14003a25d0fabf5`. All source/helper/slot copies match.
Earlier qs9viace,10kf7dnk andjbpa3ayx preparations remain retained but are
superseded by the final source corrections; none was executed. No screenshot,
native-window query or UI input was exercised in preparation; installed
capture-tool usage was inspected only. Actual permission/focus/helper delivery,
image mapping and native-question accessibility remain live observation limits.

The slot-wrapped boundary suite ran104 tests:100 passed and4 deferred compiled-C
fixtures were skipped;21 legacy B controller regressions passed separately.
This includes the v2 exact-state refusal fixtures, scoped capture/no-fallback
checks, PNG/coordinate/image-drift checks, retained helper failure without
reaping a harmless original Child, private-control/effect-readback gates and
unknown-helper release refusal. These are not GUI qualification. Meaningful
independent scrutiny remains required before returning a live-ready profile.
