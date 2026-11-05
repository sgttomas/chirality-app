# J1 Stage A: two agent-operated development attempts and offline preparation

The owner superseded the manual-first-use plan with agent-operated development
checks. This observation uses the App already launched by Agent0 at
2026-11-05T18:42:37Z. It does not reuse the closed GUI qualification loop.
The original reviewed packet remains unchanged; frontend-owned coordination
paragraphs are not edited by this record.

## Attempt 1: the already-launched instance, PID79609

Product source: eaf5d057afb82c28a928a5e347ad5749dd5adc96.
Bundle: Chirality App v4 (development 20261104-dd4a2a30).app under the retained
app-dev-candidate-20261104-dd4a2a30-lqvrfff8 build root.
Development ID: dev.chirality.app-v4.candidate.20261104-dd4a2a30.
Executable SHA256: b98a30fe2dccba062e35a0c02896b67c4441f2b987016f091ea41e6f56caf4fc.
Original PID/PGID79609, UID/realUID501, kernel birth1793904157.439921,
LaunchServices parent1. These live identity/path/hash facts matched before
observation and before the single cleanup press.

The owner reported “Welcome to Chirality” visible and no later setup action.
That remains a limited human observation; the agent did not infer completion.
At18:51:23UTC AXWindows, AXMainWindow and AXFocusedWindow returned success0
with one distinct own AXWindow titled Chirality. A bounded walk of that main
window only yielded7 nodes: window/group/titlebar controls and title text.
No AXWebArea, Welcome text, project-picker or settings control was exposed.
No broad App menu/window inventory, desktop screenshot or capture was made.

Outcome: **setup blocked before input**. Zero project-picker actions, settings
presses, write previews, native confirmations or saves. The new-settings route
and actual native confirmation remain NOT RUN. No credentials/auth files,
model/network, Codex start, Stage B, activation or global input was used.

One independently bound exact App-menu normal Quit AXPress returned0. Original
PID79609 was absent at18:52:54.277351UTC; Agent0 independently corroborated absence
at18:53:36.966UTC in parent-closure-check.json and relayed it to SWBPIPE. Exit
status/reap are unavailable because LaunchServices owned the process. This is
normal-menu request plus process-disappearance evidence, not an exit0/adminwait
or exhaustive helper/resource-settlement claim. No process was signalled.

The first cleanup harness refused before any press because its convenience
accessor returned scalar AXMenuBar as a one-item list. A second retained version
corrected scalar AXUIElement versus CFArray handling; it then sent the sole Quit
press. Both exact scripts and the failed receipt are retained. This is a harness
decoding correction, not a demonstrated App/menu defect or second launch.
The bounded attempt and initial result reconciliation took228.524332s, below10min.

## Retained evidence and state

Evidence root:
/Users/ryan/dev/chirality-t3/scratch/app-j1-stage-a-_i48c648/agent-attempt-bhzpqx_p.
Files include exact scoped_ax.py/identity_backend.py, both normal_quit scripts,
identity-and-roots.json, welcome-main-controls.json, cleanup intent/posted/observed
and first refusal, post-attempt-state.json, result.json, RESULT.md and SHA256SUMS.
result.json SHA256:
b0fae70166d1649e836e3c83860a86d67c14f2b8fb12384f3dec19b7ad333395.
Original SHA256SUMS file SHA256:
b44afa5e3785eaed6c6d4eac74468c66741b02a5f6bd5d01f692cfe32db73470.
Agent0's original launch, initial mistaken preflight, corrected presence-only
preflight and parent closure check remain alongside this evidence, unmodified.

Post-attempt development AppData and desktop-startup/request.json are absent.
WebKit/Caches are present; Preferences/SavedState/HTTPStorages absent. These are
presence facts only; no opaque contents were read or reset. The packet's exact
session/project BRIEF.md and data/pipe-inventory.csv hashes remain unchanged.
No existing owner installed-App data/control was accessed.

Shared instruction path follows current user steering:
/Users/ryan/dev/chirality-library. Its actual HEAD was40d060bf rather than the
stated selected2f981163; WORKING_ITEMS role bytes are identical between them.
The collision is disclosed without switching product/library identities. No
library, production source or packet content was changed by the attempt.

## First return proposal (subsequently consumed once below)

Do not repeat activation/occlusion work or recruit the owner for setup. The
current native result already proves exact App-menu cleanup can be automated
for this subject; setup needs WebKit's content controls exposed to the AX client.
The native window itself and AX trust were available. The observed gap is the
content subtree, not a missing launch/owner foreground permission.

Smallest next native method change for Agent0's review: reuse this exact
App-scoped reader and scalar-reference correction, replacing the one-shot
content read with a read-only content-readiness observation of the retained main
branch: at most3 reads across at most5s, no activation/set-attribute/focus/menu
cycling. Proceed only after a real AXWebArea plus uniquely labelled project,
new-settings and review controls appear. Inputs are the same exact executable/
development ID and the packet's session/project directory; before a separately
agreed relaunch, actual retained development state must be assessed as found,
never made fresh by deletion. This does not authorize that relaunch.

Why this narrow change is grounded: retained AX_FIRST_PRESS_FOCUS evidence
records7/no-WebArea on its first read and283/one-WebArea on the second. It makes
lazy exposure a concrete observation to discriminate, not an established timing
cause or a guarantee of success. A failed bounded readiness observation stops
without coordinates, global keys, screenshots or private DOM/IPC injection.
Normal exact App-menu Quit remains the agent cleanup route where independently
available; its result and process exit must be recorded again rather than
assumed from this one success.

There is also an immediately available source-test path, requiring no owner or
native launch: retained app/tests/desktop-setup.test.mjs already mounts the real
FirstUseSetup component from app/src/FirstUse.tsx and consumes packets from the
Rust desktop_startup::tests::mounted_setup_packets producer. Its existing case
covers the exact sequence desktop_setup_pick({kind:project}) →
desktop_setup_new_settings_preview({projectPath}) → desktop_setup_prepare({previewToken}),
new App-owned settings effects and saved-next-launch UI. That is the concrete
regression harness for a demonstrated frontend/host-join defect. It already
exists; do not rerun it merely to manufacture a new result, or label its injected
picker/confirmation replies as actual native setup. No such source defect has
been established by the seven-node native observation.

No additional native control or source repair is justified merely by absence of
AXWebArea in one sample. The outstanding native acceptance observations are the
actual project selection, contained write preview, native affirmative, saved
setup and process closure on that completed flow. This return proposes one
bounded agent-owned capability check, not an owner-operated test plan or a new
general controller framework. Agent0 must inspect this return before any rebuild
or relaunch. Stage B remains separately owner-selected.


## Attempt 2: bounded lazy-readiness change, PID12997

Agent0 selected one new agent-operated no-model attempt, with ordinary t3_slot
admission and a180s budget including cleanup. The exact controller was prepared
before acquisition and is retained unchanged in
app-j1-stage-a-_i48c648/agent-lazy-attempt-e7a4o477/attempt.py, SHA256
cda2577795aee0e3d19a615e790359e756fe038bfa46c43e0d2cdaae7e698535.
CONTROLLER.sha256 records its reader/scope dependencies. This was a new launch
of the same retained eaf5d057 App; it did not reuse/revive PID79609 or zootd3ob.

Admission rechecked exact executable, packet and invented project hashes,
presence-only route settings, absent AppData/request and actual development
state. Existing WebKit/Caches were preserved. No reset or rebuild. Normal slot2
START19:05:40UTC, runner12991. Exactly one open-n launched PID/PGID12997,
UID/realUID501, full birth1793905540.691166, LaunchServices parent1 and exact
retained executable/hash. launch.json retains the actual identity.

Two content reads were performed: first7 nodes/no AXWebArea at0.255s, second57
nodes/one AXWebArea at1.618s. The actual second tree exposed the labelled project
button, selected new-settings radio and disabled Review setup. This establishes
lazy content exposure in this attempt; it does not identify a general timing/OS
cause. One agent-attributed “Choose project folder…” AXPress returned0 at
19:05:42.531825UTC. No path entry/selection, review, confirmation or save followed.

The controller then rejected its one-main-window invariant (“main window set
ambiguous”). Its failed observation did not retain the new window schema, so
picker appearance/ownership/controls are not claimed as observed. Immediate
normal-menu cleanup refused “App title differs” before any Quit press. A later
read-only observation at19:06:41 again showed one own Chirality window and the
expected App title; this did not prove picker cancellation or setup. The original
work cutoff reserved time but did not own a usable teardown across these window
transitions. This is a controller phase/binding/cleanup defect, not a demonstrated
App defect.

Agent0 issued a separate cleanup-only disposition. The retained
normal_quit_v2-derived disposition_normal_quit.py (SHA256
397e6a9a469feb8989b075d76a08f0447804339c4211a46e5da91770fc8c2ac2)
rechecked the original process but refused its original-main guard at19:07:54.925
before a press. No picker Cancel, other input, signal or controller restart.
The original slot remained held, and expiry was recorded rather than treated as
release. Neither cleanup helper edited the running controller's bytes.

Agent0 then explicitly selected one normal NSRunningApplication terminate()
request independent of AX window/title, addressed only by original PID12997.
normal_terminate_disposition.py SHA256
4bf1b2be263321029604c04ab13f50d631304a9f6d9c4aac6adf53c6daddce46
rechecked full birth/UID/PGID/path/hash plus AppKit processIdentifier,
bundleIdentifier and executableURL. One terminate BOOL returned true. There was
no forceTerminate, signal, activation, key, capture, retry or setup continuation.
Normal termination is recorded as this separately selected cleanup mechanism;
it is not represented as App-menu Quit or completion of the setup/native question.

Original controller observed PID absence at19:09:37.469435UTC and returned1:
236.949777s elapsed,56.949777s over its internal180s clock. Independent cleanup
helper observed absence at19:09:37.558014UTC:237.038388s elapsed/57.038388s overrun
on that same original clock. Agent0 independently corroborated PID12997 and
runner12991 absent at19:11:05.373UTC in parent-normal-termination-check.json and
relayed the57.038s overrun to SWBPIPE. Wrapper END19:09:37UTC rc1 followed its own
process-absence observation; it was held for the complete launch-to-absence path.
Agent0's named UTC deadline was19:08:40.673; the controller's internal clock starts
slightly before admission serialization. Both measures show an overrun; no clock
or interval was relabelled to claim a180s pass. Exit code/reap are unavailable
for the LaunchServices-owned App; no exit0/adminwait/full-settlement inference.

Post-attempt AppData/request are still absent; WebKit/Caches/Preferences present,
HTTPStorages/SavedState absent. Only presence and the exact case hashes were
checked; no opaque contents/auth files read or reset. Project BRIEF/CSV hashes
remain unchanged. No supplier startup was observed by the scoped checks; no
model/auth/network or Stage B was selected. Setup, native confirmation and J1
remain incomplete.

Raw result.json SHA256:
874d1f5a760f6a1c20b7b21f6d899c6c2c62ef9814a5c51b46df85f5a0db419e.
Reconciled-result.json SHA256:
ac97fcc7b09a7e493ce84664748cba45d00c3087706b81d7fad5bc8bfb1e54ab.
Its original SHA256SUMS file SHA256:
984acecc8e6a1311cffe3d7479c385536bad470407b3dafd4cc23474b5d98674.
All launch/admission/content/action/refusal/deadline/cleanup bytes remain retained;
parent receipts are separate corroboration. No original result was rewritten.

## Selected next result: offline preparation only

Agent0 selected a new retained controller version with phase-aware picker and
confirmation binding and prebound normal termination, not another live trial.
The source is j1_stage_a_phase.py with focused test_native_attended_j1_phase.py. The
preparation and its remaining native capability are described in
J1_PHASE_PREPARATION.md. This contribution changes only DEL09-02 Work and does
not touch product/frontend coordination paragraphs, IPC, native confirmation,
packaged resources or the retained development candidate. No further native
launch, model/auth, source build or owner-operated regression is authorized.
Agent0 will commission one independent exact-version code/method review before
any future live selection. No new delegate was created for this preparation.

## Independent review and controller repairs (no new native attempt)

Agent0 commissioned one Codex-Hub gpt-6.1-sol/xhigh/standard review of exact
3d9fb116c22779d317f1fcb1b2e2b65e0a3be1df. Its 31 mocked checks passed, but six
supplemental failure scenarios established controller defects. The review
requested changes; passing hosted CI did not resolve them. Agent0's additive
repair protects cleanup from receipt errors, distinguishes known undispatched
launches, binds full confirmation effects to reviewed destinations, anchors
packet members to the reviewed receipt, refuses unknown picker structures before
text reads, and treats a replacement kernel birth as original-process absence.
The maintained mocked suite grows to43 cases. Details and the remaining
cooperative-timing/unobserved-native-path limits are in J1_PHASE_PREPARATION.md.
No new App/supplier launch, model/auth, native input or candidate change occurred.
The two actual attempt outcomes and all their original bytes above are unchanged.
