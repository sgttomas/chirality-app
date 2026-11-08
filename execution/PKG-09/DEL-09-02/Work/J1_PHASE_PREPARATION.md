# Offline J1 Stage A phase-aware controller preparation

## Nullable content metadata correction (v5)

The owner-available attempt on integrated06d338c9 captured a genuine main, then
refused before content/input on AXTitle/-25212. The SDK AXError.h defines
kAXErrorNoValue as "The requested value or AXUIElementRef does not exist."
The v4 content walker treated that as NotReady even for nullable control titles,
descriptions, values and leaf children, preventing its existing label fallback.
Separately, its picker list exclusion was also applied to the App's own HTML
first-use AXList, hiding that form's controls. These are controller defects;
neither proves an App handler or WebKit/OS cause.

V5 uses an explicit optional-content read for those metadata fields only. NoValue
there becomes absence; CannotComplete, foreign owner and other errors still
refuse. Structural roots/roles, initial-main/native-question titles, parent
relationships and post-write path values remain mandatory. Explicitly optional
reference arrays may be empty on NoValue; required arrays still refuse.
The owned main content walk includes HTML lists; the separate native picker
parser still excludes list/file/history children and rejects unknown containers.
Exact labels, enabled/parent/source checks, full statement/destination checks,
authentic receipts and cleanup/custody logic remain in force.

Six added mocked cases exercise a compact constructed first-use list with missing
optional fields, description fallback through the actual content walker and
target check, missing-label refusal, strict structural/path reads, CannotComplete
and foreign-owner refusal, and unchanged picker list/history exclusion. No raw
runtime dump is committed. These checks are source evidence, not a new native
content/selection/save result. The executed v4 source and original failure remain
unchanged in their retained evidence.
All60 focused mocked cases and the193-test native-attended cohort pass under
normal t3_slot admission with fresh scratch homes; deliverables errors=[] and
diff check passes. Commands/logs are retained at app-j1-nullable-metadata-klklw28_.
The source correction made no product/candidate change. Agent0 later selected
one frozen552445d7/v5 attempt: main and WebArea with9 controls were observed,
and one checked project-picker press returned0. The separate native picker
parser then refused its unclassified structure before any path/selection/save.
Autonomous cleanup/final absence completed in2.84 s without overrun. See attempt6
in the owning account. This exercises the reader but does not establish native
path-entry absence or setup/J1 success; no further input method is selected here.

This began as the selected preparation after the first two actual observations.
The repaired integrated v3 and separately selected frozen PR136 v4 have since
each operated one App instance, with zero setup input; see attempts3/4 in
[the actual account](J1_AGENT_FIRST_USE_20261105.md). All executed controller/helper
bytes and receipts remain at their original private paths and identities.
No product source, native confirmation, credential policy, frontend coordination
paragraph or packaged candidate is changed. The retained product source remains
eaf5d057; implementation changes in this preparation belong to the test controller.

## Concrete change

j1_stage_a_phase.py implements only this Stage A sequence. The source is inert on
import and has no automatic native CLI. A future reviewed runner calls
run_prepared with the exact reviewed Subject/preflight and the included private_journal evidence
writer under ordinary t3_slot admission. It uses exclusive0600 records with
file/directory fsync, including repeated phase observations in sequence. It is not an IPC/control endpoint or a
shared automation framework. Source preparation alone selects no native launch;
Agent0's subsequent exact-version selections and their limits are recorded in
the actual account.

Original binding is full kernel PID/parent/UID/realUID/birth/executable plus PGID
and executable SHA256, preserved throughout. Subject bundle/development ID/data
root/project must match the reviewed receipt; exact manifest member sets and
member digests are compared with its reviewed manifest_checks before opening
member paths. Regenerating local manifests cannot rebind the reviewed case. All
packet/project hashes and
actual state/route-key presence are checked before a single open-n. WebKit/cache
state is recorded as found; AppData/setup present means stop without launch.
The existing fixed identity/AX reader is loaded from exact pinned bytes; a
retained version includes those same bytes, not an ambient module search.

Normal AppKit cleanup APIs are prepared before launch. Immediately after the
original process identity is established, cleanup correspondence is bound using
NSRunningApplication processIdentifier + bundleIdentifier + executableURL. The
controller has one normal terminate request on completion/error/cutoff. It does
not consult AX main/title/menu/picker or await a parent disposition to decide
that cleanup. No forceTerminate, signal, activation, global keys, coordinate or
capture route exists. BOOL is a request result; actual process absence is still
required. LaunchServices exit status/reap is not fabricated.

Main-window identity is retained and never replaced by the first/focused/other
window. A picker/confirmation is an expected distinct AXSheet/Dialog or proven
modal window only when owned by the original PID and related to the retained
main by AXSheets/AXParent. A nested path sheet must have a unique structural
relation through that picker. Extra unrelated windows, ambiguous sheets, stale
references or foreign owners stop input. Missing/transient values have bounded
read-only observation; no focus setters or mechanism cycling. Phase/control and
parent-chain checks repeat immediately before actual input.

Content readiness remains at most3 reads within5s. The configured allowance is180s;
setup cutoff110s leaves70s nominal cleanup/absence reserve. After each ordinary
operation, the cutoff is rechecked. Any setup or provenance error begins cleanup
immediately. The mocked cutoff case starts cleanup at110s without a parent round
trip. Per-object AX messaging uses0.2s and scans have node/depth/time bounds. Every
property verifies its remote owner; full original birth/path/hash checks bracket
each bounded phase and repeat before input. The executable is not rehashed for
every AX property. Unknown path-entry dispatch is retained like unknown presses.
These checks do not guarantee return from arbitrary native/OS stalls. If normal
termination refuses/has unknown outcome or the App remains live, the result is
held/failed; the future slot finalizer retains the wrapper until actual absence.
Unknown launch with no original identity cannot be relabelled closed from a
transient empty lookup. Evidence/observation failure cannot release a live App.
Cleanup receipts are best effort: a write error is retained in the returned
evidence_errors and cannot suppress the sole identity-validated normal request.
Such an evidence gap prevents a successful flow claim. Launch becomes pending
only at the actual dispatch boundary, after its intent was written; a failed
pre-dispatch receipt is not an unknown launched process. Original-process absence
uses kernel birth as well as numeric PID: a replacement birth proves the original
gone without targeting the replacement; an unavailable observation stays held.

## Picker capability: prepared guard, still not a native observation

The actual second attempt never recorded the native picker controls: its
one-main-window guard stopped first. Therefore no writable path field or Go-to
control is asserted to exist on the retained App's picker. Source preparation
cannot prove a native control is absent on a closed instance either.

The only prepared path route is genuinely published AX controls inside the
related picker: an already visible, uniquely labelled Go-to-folder text/combobox
whose AXValue is reported settable, or an actually exposed named Go-to-folder
button that reveals such a related sheet. The controller then enters only the
exact packet session/project, verifies its AXValue, uses the observed Go/Open
controls and requires the exact selected directory/project in actual UI readback.
It does not create these controls or inject a picker result. Setting AXValue on
that proven text field is ordinary scoped text input; no AXFrontmost/AXFocused
write is used. No global-key navigation or filename/sidebar exploration exists.

The conditional supported picker schema is a flat panel of direct controls.
AXTable/Outline/Browser/List/Menu/PopUp children are skipped without traversal.
Unclassified groups/scroll areas refuse the phase before descendant text reads;
the reader does not search arbitrary containers for a useful control. Static text
and control-history children are never read. Only direct admitted control labels
are read, never unknown control values. After exact path entry/readback, a direct
AXPathControl must expose that exact current-directory value before Open. This
schema is unobserved on the retained native picker and may refuse it entirely.
Unknown search fields are not written. If the safe picker exposes neither supported path entry
nor a named action to it, NATIVE_PATH_ENTRY_UNAVAILABLE is the concrete limit:
no path is sent and the prepared normal-termination cleanup runs. There is no
honest full native setup-readiness claim until that actual capability is observed.
The supported agent route within this version is that exact scoped AX text-entry
route; it has no hidden keyboard or DOM fallback and no owner-operated alternative.
A broader route would need separate source/capability evidence and scope.

## Confirmation and saved-state provenance

The new-settings radio/project/review controls are the actual labels from the
retained57-node observation. The preview must expose all3 distinct destinations
under the exact development AppData, with Saved choices equal to
desktop-startup/request.json.
The native related question must contain the full retained new-settings effects
text, with the exact three reviewed destinations/project and exact
Leave/Create/Cancel button set. Abbreviated/digest-only questions are unsupported
and refused. The statement/root/target are rechecked before dispatch; changing
text on the same button does not preserve authority. Project readbacks use whole
lines rather than prefix/substring matches. Only the real affirmative button authorizes the
normal host prepare call. No product token, native question or IPC check is
bypassed. Native UI result is followed by the actual generated pending request.

The saved-request parser follows eaf5 RequestedInputs/Reference/NativePath: tagged
unix_bytes paths plus object metadata. It does not search display strings inside
JSON. AppData, sign-in, shared config/AGENTS/skills and exact project references
must match the reviewed destinations. It reads only that new nonsecret pending
request; never an auth file or existing owner Codex/App state.

## Focused verification and preparation standing

The mocked phase suite covers successful flow; related/nested pickers, wrong
owner/main and ambiguous targets; scalar/array references; lazy, transient or
missing values; stale controls and parent chains; exact paths, destinations and
pending schemas; unknown press/BOOL; identity changes; post-launch receipt
failure; picker re-observation; cutoff cleanup, late closure, no repeat and slot
holding after controller/recording failure. A privacy test refuses file-list or
history child reads. Its 31-case initial run and later 43- and 45-case repair
runs are preparation evidence; OS effects were mocked.
The later runs also exercised native-attended admission without native loading.
The final 45-case run and 178-test native-attended cohort used an owned symlinked
TMPDIR. The v5 correction above has its own 60-case and 193-test results.

Historical PR135 checks passed: the initial 31 focused mocked cases, the 43
focused cases and full 176-test native-attended cohort after the symlinked
temporary-path fixture correction, and the final 45 focused cases and full
178-test cohort on `b1f0317a61e94d3db6f51a8112b8d2a92cbfc975`. Checks used
normal shared-wrapper admission and fresh scratch Codex homes; the portability
and final runs used the owned symlinked TMPDIR. OS effects remained mocked.
The repair cases included receipt failures at both cleanup sites, unknown
launch dispatch, confirmation changes at the actual press boundary, private
content behind unclassified containers, replacement process birth and a slow
operation reported as a failed overrun. The final two regressions exercised
mutating callbacks through the actual hold/finalizer paths, preserving the
original PID/birth and holding until that original process's absence. Late
closure did not relabel the initial failure.

The repairs addressed receipt failures that could skip cleanup, pre-dispatch
slot holding, weak confirmation provenance, manifest rebinding, private content
behind unclassified picker containers, PID reuse and a callback alias in
closure receipts. A symlinked temporary-path fixture also needed canonicalizing;
that correction did not change controller bytes or establish native behavior.
The caller must supply the authentic reviewed Subject/preflight: the controller
does not authenticate a replacement caller-provided receipt or provide signed
attestation. The original version-specific review is not a review of later bytes.
Logs and commands remain in `app-pr135-repair-checks-k0rbj7zf/focused.log` and
`app-pr135-ci-temp-alias-mjepzl1q`, including `identity-repair-checks.json` and
matching `*-identity-final.log` files.

Historical preparation was reconciled onto main
`3f6f7e858147ff07fb1ff9c56e61b88d184d1e7b`. Agent 0's independent review of
`3d9fb116` requested changes for six controller defects. The targeted re-check
of `4a865b51` confirmed those repair paths but recorded 11/12 requested cases
passing, with a remaining held/late/final-closure callback alias and the
temporary-path fixture failure. Agent 0 verified the follow-up directly;
neither independent report becomes a clean review of later bytes. The original
discovery-name/Work-reference adjustment changed no controller or test bytes;
the later v3 repair did. Frozen v2 exports and FINAL_HEAD remain historical
inputs, not receipts for repaired source.

The retained preparation contains the controller, tests, pinned reader, reviewed
input/subject references and a SHA256 manifest. The original `e7a4o477` and
`bhzpqx_p` attempt/helper/result files, frozen v2 export and FINAL_HEAD mapping
retain their historical identities. The focused test uses the existing
`test_native_attended*.py` discovery name. The actual attempts and their limits
remain in [the first-use account](J1_AGENT_FIRST_USE_20261105.md); preparation
itself is not a native admission or proof of picker path-entry capability.

The later [J1 actual result](J1_REAL_MODEL_ACTUAL_20261108.md) records the
completed core path on its own development subject, including saved setup and
real-model work. It does not change the subjects or limits of these controller
observations. J2 remains partial: its earlier renderer preparation includes
[returning to a draft](RENDERER_RETURNING_DRAFT_20261104.md). The later
[J2 actual account](J2_PARTIAL_ACTUAL_20261108.md) records a trial, normal
close/reopen, History continuation and recovery of the unfinished draft and
trial row on its own development subject. Registration and reuse were not
established, so the create/trial/register/reuse journey remains incomplete.
Further native or cloud continuation is not authorized by this preparation.
Qualification and publication remain open.

## v4 correction: initial-main discovery precedes WebKit content readiness

After the exact merged b1f0317a method was used once (PID96500, attempt account
above), Agent0 selected this bounded OFFLINE correction. v3 consumed its3
content-read attempts while initial_main still refused; only the final message,
not actual root counts, was retained. It cannot establish a permanent absence
or timing/permission cause. No new native run is performed here.

StageA.startup now samples initial main at most10 times within20s, clipped to
work_end. It records safe counts/category/elapsed/original PID and only waits
for empty, self-only, AX cannot-complete or no-value states. Extra windows,
wrong owner/identity/title and actual unexpected structures remain immediate
refusals. NativeAX captures one unique original main and refuses replacement.
NativeSession reuses the same original AX application reader during discovery;
content ready() no longer calls original_main. Only after capture does the
unchanged3-read/5s content window begin. Overall180s/work cutoff110s and prebound
normal termination remain unchanged; these are cooperative budgets.

No activation/focus/control workaround or broad discovery/logging was added.
Startup counts remain null when unavailable. Unknown/malformed fact shapes
refuse. This small test-readiness correction leaves authentic reviewed manifest
checks, normal termination, setup/native confirmation/input provenance and
original-birth-aware finalization unchanged. Agent0 will inspect the exact diff
and choose any next live operation; no additional review delegate is created.

Agent0 subsequently directly inspected and selected frozen PR136 headf9059685
for one pre-merge development attempt. Nine retained startup samples over
0.233–18.052s each recorded root1/self1/match0/self_only; no original main or
WebKit content phase was admitted and no setup input occurred. Prebound normal
termination and observed original-process absence closed that instance in
20.713761s with no overrun. This does not identify the self-reference's cause or
qualify setup/path entry/recovery. The method stayed immutable through cleanup;
only its actual account and narrow coordination text are added afterward.
