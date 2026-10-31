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
plain owned single-link0600 temporary file only after reading the prompt/image,
then atomically rename it to the named control path. It binds
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
never silently repeated after ambiguous delivery. Its confirmation uses the
one derived owned Stop-modal route described below. An unsupported sheet,
ambiguous relationship or unreadable question refuses without confirmation.
An unexpected Quit live-work question is preserved for an explicit confined-
effects disposition, not automatically confirmed by this route.

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

## Historical main-only preparation (superseded)

Read-only capture/preparation succeeded against the unchanged six-row assessment.
The historical main-only basis `/Users/ryan/dev/chirality-t3/scratch/app-owned-window-prep-aqsif0fz/retained-v2-proposed-inputs.json` has SHA256
`990f9ae64d51eac3ee1787de440dd16e32b7a29655dd52f64c5da4a2142eb98a`. The historical unrun attempt is
`/Users/ryan/dev/chirality-t3/scratch/app-successor-native-B-u3ug__xe`, admission SHA256
`8b6245534baa20881330689cf2fe863adbdfde230f237bbdb14003a25d0fabf5`. All source/helper/slot copies match.
Earlier qs9viace,10kf7dnk andjbpa3ayx preparations remain retained but are
superseded by source corrections; none was executed. The u3ug__xe attempt is also
superseded by the modal/helper changes below and must not be executed. No screenshot,
native-window query or UI input was exercised in preparation; installed
capture-tool usage was inspected only. Actual permission/focus/helper delivery,
image mapping and native-question accessibility remain live observation limits.

The slot-wrapped boundary suite ran104 tests:100 passed and4 deferred compiled-C
fixtures were skipped;21 legacy B controller regressions passed separately.
This includes the v2 exact-state refusal fixtures, scoped capture/no-fallback
checks, PNG/coordinate/image-drift checks, retained helper failure without
reaping a harmless original Child, private-control/effect-readback gates and
unknown-helper release refusal. These are not GUI qualification. The original independent review found no blocking defect but identified the
runtime-write gap and practical dialog/time limits. The materially changed
modal/helper boundary requires its own narrow review before ready return.

## Updated Stop-modal boundary and timing preparation

Agent0 separately authorized preparation of one derived owned Stop-confirmation
modal; this supersedes the earlier main-only confirmation limitation for the new
source/admission, not the historical prepared attempts. The profile is now
`chirality.owned-window-ui/v2`. No native execution follows from this preparation.

Only the already full-generation/account/source-bound Stop click may create the
one-shot modal context. The keeper records the original identity, main-window
identity and pre-click owned inventory before posting, then requires the protected
helper's posting result before admitting a modal observation. The candidate must
be the unique newly visible owned window, distinct from the original main window,
with a missing, empty or Stop Codex title, normal-or-modal layer and foremost
owned ordering. A missing WindowServer title is not invented as observed text;
the actual captured question must still establish the exact presentation. No missing
main window is replaced. Before/after original-Child and window binding remains.
Where AX exposes a matching modal/sheet and parent relationship, the isolated
helper records it and refuses contradictions, foreign parents or an unsupported
sheet association. If AX exposes no relation, the unique post-click owned-window
derivation is provisional: the image still must establish the exact actual Stop
presentation before any confirmation. No separate WindowServer row means this
route cannot capture a sheet; it refuses rather than including it in main capture.

The agent must transcribe the actual title and complete question, including the
matching account/session/spawn, exact expected zero-work Stop effects, coverage
limit and timestamp. The physical-home member of the full generation remains
bound by the prior main diagnostic/source gate; it is not invented as displayed
modal text. Digest-only/changed/extra work or effects, missing text and mismatch
refuse. The one confirmation is bound to the current modal image/geometry/focus;
a changed pre-input image posts nothing and requires rereading. An ambiguous
posted confirmation is never repeated. Dismissal and LT23 settlement still need
actual subsequent main-window observations. The image/question transcription is
agent observation, not supplier-native JSON or a personal human act.

The helper Python's resolved prefix/base-prefix are now write-denied to the App
sandbox, and helper TMPDIR is a separate private control-root directory, not the
App-writable tmp subtree. Invented sandbox fixtures verify runtime-module/helper-
temp writes are denied while ordinary App tmp remains allowed. Click/scroll
points exclude the top40-point title band and8-point resize edges. Controls must
be privately completed then atomically renamed. A pending effect permits a
read-only recapture without claiming success; it still forbids another input
until actual expected effect is read. All diagnostics, including cleanup-source
and final settlement, require raw envelopes: even an already-stopped observation
can become the final qualification witness checked by check_requests. Only the
initial failure-recovery source observation may omit them; the next diagnostics
call requires them. Prompts state required sections explicitly. Full source/
account/generation and LT23 leader/descendant gates remain unchanged.
The known source's existing sticky More tools/Connection & access links are
allowed navigation targets; they only reveal/scroll existing sections.

The [offline timing fixture](../Evidence/EXP/owned-window-ui-offline-timing-20261031T165901Z/archive-index.json)
contains82 invented diagnostic lines on3 PNG pages. A blinded Type2 read the
images at original detail and made one private0600 atomic submission, without
reading hidden expected values. Exact comparison and the existing ready gate
passed in17.993596s. The agreed exclusive interval ended rc0 at16:59:19Z and
released; memguard remained. This is one idealized transcription/control sample,
not a measurement of native capture, rendering, navigation or full live B time.

Prepared phase caps, including helper/input/operator work within each phase:

| Phase | Cap | Downstream reserve |
|---|---:|---:|
| Slot-acquired admission/inventory | 15s | 280s before App launch |
| Initial owned-window readiness | 15s | 265s |
| First complete ready witness + navigation | 60s | 205s |
| Complete ready recheck | 35s | 170s |
| Cleanup source/lifecycle refresh | 35s | 135s |
| Locate/post the one Stop click | 20s | 115s |
| Derived modal/read/confirm | 30s | 85s |
| Observe full source/LT23 settlement | 45s | 40s |
| Normal exit or failure cleanup reserve | 40s | — |

These caps total295s. Each phase refuses entry unless its full cap and downstream
reserve remain; helper startup additionally requires6s in the current phase.
The 18s fixture sample leaves42s in first ready and17s in recheck for navigation/
helpers, but those costs remain unmeasured. Scroll is bounded to at most600 points
and window-height minus200, retaining overlap; operation/step caps remain finite.
This is a prepared conditional budget, not a proof that unknown native layout
or animation fits. If observed content/latency cannot finish within its phase,
refuse before further input (especially before Stop), retain complete checks and
return the exact limitation. No deadline extension is automatic. No known
minimum from the representative fixture exceeds295s; native page count and
capture/focus/delivery remain unobserved and are material live-disposition limits.

## Historical modal preparation and validation (superseded after review)

Fresh read-only admission succeeded against the unchanged exact six-row ledger,
saved A request and post-am98 metadata. The basis is
`/Users/ryan/dev/chirality-t3/scratch/app-owned-modal-prep-ynql8fea/retained-v2-modal-inputs.json`,
SHA256 `1758db00e52fa4634116420eb718e1ede23d8800281477c8ef9b22f2a312b711`.
The new unrun root is
`/Users/ryan/dev/chirality-t3/scratch/app-successor-native-B-w8wyelot`,
admission SHA256 `ac6db9a5a4424152df501daaa56e844bf72f36279a78ae37509ffd3578ae7e0c`.
It preserves the earlier main-only preparations unchanged. No execution-start,
actions, artifact check or slot-entry record exists in this new root. This is a
review input, not execution authorization.

The updated slot-wrapped boundary suite ran 125 tests: 121 passed and four
compiled-C fixtures were skipped (the C component remains deferred). All 21
legacy B controller tests also passed. New regressions cover derived-modal
selection and contradictions, complete question effects, one-shot confirmation,
proven-unsent image drift, helper custody during Quit/release, owned-menu cycle
pruning, slot binding, phase reserves and non-extending deadlines. Invented
sandbox fixtures cover Python-runtime and helper-temp write protection.
Deliverables validation and whitespace checks pass. Actual native capture,
modal presentation, focus, input delivery and image-fingerprint stability remain
unobserved. The narrow review and subsequent fixes are recorded below; w8wyelot
is now superseded and must not be executed.

## Narrow review disposition and current preparation

Claude Opus 5.5/high reviewed 72bf33f3..6c5908ce, running 44 focused tests.
The reviewer found no false-success or main-window-substitution path but did not
recommend readiness until three practical defects were fixed. This records that
review and the manager's bounded fixes, not a new clean repeat review:

- Final settlement now always requires raw envelopes, including the already-
  stopped cleanup case, so final request checks cannot fail solely because the
  prompt allowed their omission. Required sections are explicit in each prompt.
- Held screen recovery is advertised only when supplier settlement and Quit are
  already recorded. The inherited 45-second retry cannot fit the observation
  phases; it is not offered as a way to resume those phases. Otherwise supervision
  remains; separately selected owned-menu cleanup and normal-exit administrative
  release remain cleanup only, with no qualification or settlement inference.
- A missing WindowServer modal title is admitted alongside empty/Stop Codex,
  still requiring unique owned derivation and the exact actual question before
  input. No foreign, ambiguous or substituted window is admitted.
- Question grammar uses the exact source states starting, handshaking, ready,
  halted-after-repeated-failure and exited-unexpectedly.
- The screen settlement loop uses the existing non-extending 45-second phase
  deadline instead of the legacy 25-second loop. A phase selected for observed
  stopping remains settlement even without an agent confirmation record. The
  legacy controller retains its 25-second loop; no overall deadline is extended.

Timing limits remain material: helper starts require more than six seconds left,
so the initial 15-second window phase has about nine seconds for starting a new
helper. Full phase reserves leave no guaranteed transition slack if every cap is
used. The 20-second Stop and 30-second modal caps include agent round trips.
The invented timing sample measures none of the native costs. No live fit or
modal/click/fingerprint behavior is claimed; a refusal may retain the App/slot.

After fixes, 130 boundary tests ran: 126 passed, four deferred C fixtures skipped.
All 21 legacy B regressions passed. New regressions cover final envelope prompts,
already-stopped diagnostics, retry-offer truthfulness, missing modal titles and
the actual source state names, plus settlement deadline reuse. Deliverables and
whitespace validation pass.

Fresh read-only v2 preparation succeeded against the same exact six-row state.
Current basis:
`/Users/ryan/dev/chirality-t3/scratch/app-owned-modal-reviewed-prep-gy6xn5lu/retained-v2-modal-inputs.json`
SHA256 `536fab0747c5f16dc4c2433f8b9d3d789d7adb23f056f0dd2f6270dd11a3d9f6`.
Current unrun attempt:
`/Users/ryan/dev/chirality-t3/scratch/app-successor-native-B-8w83gq78`
admission SHA256 `0e467feb15bc22b5f3d60880e35e6f6a9ab592b2d81117064dec3b570665c553`.
All 16 dependency hashes, copied helpers and policy match current sources;
no execution-start/actions/artifact-check/slot-entry exists. All earlier bases,
preparations, candidate and recovery inputs remain retained. This profile awaits
exact-head CI and Agent0's separate live disposition; no launch is authorized.

## Post-8w83gq78 failure diagnostics only

The authorized 8w83gq78 attempt is consumed and closed, FAILED before capture;
see [its evidence account](FAILED_B_OWNED_WINDOW_20261031.md). Its six-row basis
is historical prelaunch state and is not a newly assessed current-state basis.
No preparation or launch is authorized by this follow-up.

The separate helper repair replaces only the equality assertion's reporting:
when the already owner-filtered actual selection differs, it writes a private
0600, exclusive `window-helper-NNN.window-mismatch.json` with both dictionaries,
field-level differences (including individual bounds fields), admission/sequence
binding and initial/before-capture-exec/before-input-post comparison point. It
then raises the same refusal. If diagnostic output fails, it still refuses and
reports the write-error class. No additional native query, window reselection,
image, input, permission or retry is introduced; identity/hash checks remain
before selection and strict equality remains the acceptance rule.

Twenty-two focused helper/window tests pass, including ID/geometry/count drift,
second-comparison refusal before exec, unchanged numeric JSON serialization,
identity change before selection and write-once diagnostic failure. These are
mocked/source tests plus the existing harmless helper fixture, not GUI evidence.
The repair cannot recover the missing actual dictionary from 8w83gq78. Any later
policy that accepts changed presentation facts needs its own explicit scope and
independent scrutiny; no such change is proposed here.

The [explicit post-8w83 v3 admission](RETAINED_B_ADMISSION_V3.md) binds the
subsequent nine-row assessment in a separate unrun preparation. The window
acceptance and mismatch-diagnostic policy remain unchanged; no live authority.
