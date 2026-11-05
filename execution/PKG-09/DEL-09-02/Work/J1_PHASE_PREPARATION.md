# Offline J1 Stage A phase-aware controller preparation

This is the selected preparation after the two actual observations recorded in
J1_AGENT_FIRST_USE_20261105.md. The new source has not operated an App. All executed
controller/helper bytes and receipts remain at their original private paths.
No product source, native confirmation, credential policy, frontend coordination
paragraph or packaged candidate is changed. The retained product source remains
eaf5d057; implementation changes in this preparation belong to the test controller.

## Concrete change

j1_stage_a_phase.py implements only this Stage A sequence. The source is inert on
import and has no automatic native CLI. A future reviewed runner calls
run_prepared with the exact reviewed Subject/preflight and the included private_journal evidence
writer under ordinary t3_slot admission. It uses exclusive0600 records with
file/directory fsync, including repeated phase observations in sequence. It is not an IPC/control endpoint or a
shared automation framework. No native launch is selected by this PR.

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

## Focused verification and handoff

The initial 31 focused tests passed through normal shared-wrapper admission with a fresh
scratch Codex home. All OS effects are mocked. They cover successful phase flow;
related/nested picker relationships; wrong owner/main or ambiguous targets;
scalar reference/array distinction; lazy/transient/missing values; stale control
and parent chains; exact path/destination/pending schemas; unknown press/BOOL;
identity changes; post-launch receipt failure; transient picker re-observation;
cleanup beginning at cutoff; separate late closure without changing initial failure;
no repeat; and a slot finalizer that holds across controller/recording failure.
The no-file-list/history test raises if a private child is visited. Tests are
preparation evidence, not native picker, confirmation, save or cleanup success.

Agent0's independent review at exact head3d9fb116 returned changes requested:
receipt failures could skip termination, a pre-dispatch failure could hold an
unlaunched slot, confirmation provenance/readback was weak, regenerated manifests
could rebind the case, generic picker containers were read before filtering,
and PID reuse could hold for a replacement process. The additive v3 repair
addresses those six findings in this PR. The maintained suite now has43 tests,
including the review's failure scenarios, an actual NativeSession admission
path stopped before native loading, receipt failure at both cleanup sites,
unknown launch dispatch, same-button statement changes at the actual press
boundary, private text behind unclassified containers, replacement birth and a
slow operation that produces a failed overrun. All OS effects remain mocked.
The original exact-version review is not relabelled as a clean review of v3.
Private focused log: app-pr135-repair-checks-k0rbj7zf/focused.log (initial repair
run); final checked commands/results are retained with the PR repair return.

Hosted CI on4a865b51 exposed a temporary-path fixture issue before its admission
assertion: macOS's symlinked temp path differed from the resolved reviewed project.
An owned symlinked TMPDIR reproduced that failure. Canonicalizing the fixture
root fixes it; the controller's exact-path guard and all controller bytes are
unchanged. The43 focused cases and full176-test native-attended cohort both pass
with that symlinked TMPDIR. Before/after logs and exact commands are retained in
app-pr135-ci-temp-alias-mjepzl1q. This fixes test portability, not native behavior,
and supplies no new App execution or independent review of a different controller.

The targeted re-check of4a865b51 confirmed the six repair paths, and found one
remaining callback alias in held/late/final-closure receipts plus the temp-path
fixture issue above (11/12 requested cases passed at that old subject). Agent0
detached every remaining original-identity receipt and the returned closure,
with two regression cases exercising the actual hold/finalizer paths against
a mutating callback. Those cases require the original to remain held until its
own absence and preserve its PID/birth in retained and returned facts. This small
follow-up is parent-verified; neither prior report is relabelled clean on new
bytes. The maintained focused suite now has45 cases. No further delegate or
native attempt was started for this correction. The caller must still supply
the authentic reviewed Subject/preflight; the controller does not authenticate
a replacement caller-provided receipt or constitute signed attestation.
All45 focused cases and the full178-test native-attended cohort pass under the
owned symlinked TMPDIR; deliverables reports errors=[] and diff check passes.
Exact commands, source hashes and logs: app-pr135-ci-temp-alias-mjepzl1q,
identity-repair-checks.json and the matching *-identity-final.log files.

Deliverables/diff checks and the exact prepared source manifest accompany the
PR return. Agent0, not this manager, will commission the one independent review
of this concrete version before any new live launch. The actual two attempts
stay failed/incomplete at their precise observed stages. J1/J2/publication and
native qualification remain open. No owner test task is assigned.


## Current prepared identity and review route

Preparation is based on main3f6f7e858147ff07fb1ff9c56e61b88d184d1e7b by normal
fast-forward reconciliation of the isolated contribution branch. Frontend
coordination and product/package/lock bytes are untouched by this contribution.
Current manager/settings: codex-hub/gpt-6.1-sol, reasoningEffort=xhigh,
serviceTier=default. The initial manager preparation created no Type2. Agent0
commissioned the independent exact-version review described above and owns the
repair/integration disposition. Historical reviews/models retain their actual standing.

The retained phase-aware preparation contains the exact controller, tests, pinned
reader, reviewed input/subject references and a manifest with their SHA256s.
The original e7a4o477 and bhzpqx_p attempt/helper/result files were not edited.
This is source preparation, not a fresh native admission or another live root.
No current process/window/dev-state probe, model/auth, build, download or native
trial was performed in this preparation. The actual native picker path-entry
capability remains the explicit unresolved observation above.

The focused test file uses the existing test_native_attended*.py discovery name
so the maintained native CI cohort runs these cases without a workflow change.
That original filename/Work-reference adjustment did not change controller or
test bytes. The later v3 repair does; the frozen v2 export and FINAL_HEAD mapping
remain historical inputs, not a receipt for the repaired bytes.
