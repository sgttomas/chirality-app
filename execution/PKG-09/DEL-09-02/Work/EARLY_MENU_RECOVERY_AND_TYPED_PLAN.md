# Early original-App menu recovery and isolated AX discriminator plan

## Selected cleanup boundary

The jag50nz3 failure supplied an owned application self-reference but no distinct
AX main. Neither Raise nor Frontmost was sent. Requiring that missing main before
normal menu Quit coupled recovery to the same unavailable capability. The failed
attempt later closed via owner normal Quit, original CLD_EXITED/status0/adminwait0,
with6972.331693s elapsed and6677.331694s overrun, slot END01:55:50UTC2026-11-02.
No setup/B/Stop/LT23. All used records and current state remain unchanged.
The offline diagnosis/receipt hashes remain in private
app-post-jag-diagnosis-prdbtwyl; no ABI cause or OS/timing explanation was proved.

Agent0 selected an independent EARLY menu request. Implementation confines this
to A, with no other incarnation, no saved setup, no Cancel control, and explicit
false setup/input/Stop flags. Missing flags refuse. Setup is marked before the
maintained form; keyboard, AXPress and control-focus wrappers mark possible
input before invoking it. Stop is marked before request_stop_ui. If a focus
helper started, its actual private trace must explicitly show no Raise/Frontmost
attempts and neither action-intent file may exist. Missing trace or uncertain
helper settlement refuses. This conservative gate does not extend authority to
B, post-setup, post-Stop, or partially dispatched focus.

Retained original Popen/WNOWAIT-live/kernel birth/parent/executable hash checks
remain in admissions.check_birth. The early path also rereads the private
SHA-bound admission, matches its receipt and executable fields, and rejects any
previous Quit request. It consumes the early cleanup before discovery; refusal
or uncertain outcome cannot trigger another menu attempt.

Traversal is solely original AXApplication → AXMenuBar → exact App-title menu →
unique enabled exact Quit item, with original PID checks before content reads,
bounded depth/children/references and AXPress support. No main AX window or
foreground is required. No keys, activation, global traversal, alternate PID or
standalone-script fallback is used. Before dispatch it writes an exclusive0600
intent bound to birth/admission/candidate/incarnation/title, fsyncs file and
parent directory, repeats stage/original identity checks and the complete menu
lookup, and requires the same retained app/bar/menu/target plus helper settlement.
One AXPress records actual rc/error/late status even on uncertain dispatch; no
receipt is treated as effect or successful exit.

The modal state is explicitly UNKNOWN, not absent. This is only a request to the
unchanged product App-menu Quit handler, never a question confirmation. The
existing normal-exit0, helper settlement, exact administrative reap and final
resource closure sequence follows. No-op, question, no exit or uncertain resource
state remains failed/held; no all-conditions closure guarantee. Five seconds and
600 cumulative adapter calls bound this menu operation inside existing cleanup
reserve. Bounds are refusals, not a guarantee that an arbitrary menu fits.

Historical supporting evidence is the am98 original-App menu AXPress0 despite
self-reference, followed by original exit0/wait0. It does not qualify today's
candidate. Current original-custody checks replace the weaker old standalone
PID/heartbeat script; that script is not revived.

### Explicit coverage reduction

All autonomous failures before verified focus now select only this conservative
early gate. B before verified focus, and A with attempted/unknown focus dispatch,
refuse this route and notify the owner; they no longer try the old main-window
cleanup fallback even if that main later becomes available. This is intentional
fail-closed narrowing to the selected no-prior-input scope, not equivalent or
broader recovery coverage. Parent integration must carry this limitation forward.
No fallback cycling or expansion of cleanup authority is implied by the PR.

## Real-path offline checks

Tests exercise the production early traversal and full normal-exit path with
invented AX/Child data and actual private admission/intent files. Cases include
self-only AXWindows (never queried), successful one-press closure; wrong PID,
ambiguous/missing/disabled/actionless Quit; changed identity/retained target;
ineligible A/B/setup/Stop/input or unknown helper/stage; focus attempted/missing
trace/intent refusal; uncertain dispatch/no duplicate; and successful request
without exit (no reap/release). Existing later-stage menu/sheet checks remain.
No native process, App, credentials or permission operation is used by tests.
Independent Claude Opus5.5/high review and fresh exact-head CI are required.

## Exact diagnostic gap and isolation decision — DESIGN ONLY

Source/SDK/retained ABI audit found no pointer-width, out-pointer or premature-CF-
release explanation. The real jag trace implies CFArray → equal-to-app reference
→ successful AXApplication role, while old raw diagnostic also shows correct
CF types/raw success and a distinct owned AXMenuBar. General CF fixture checks
already passed; do not build another generic fixture or add focus mechanisms.

The existing typed_ax/reader.c directly uses SDK calls and receives an AX object,
not a PID. native_b_typed_ax.py supplies Result/decode, checked manifest/library
load, protected staging and a same-reference Python comparison. Its capture(run)
currently LOADS/INVOKES FFI IN THE KEEPER. It is NOT crash isolated. Therefore the
future diagnostic MUST NOT call capture(run) from the sole original-Child keeper.
No claim that existing helper isolation automatically covers this unwired reader.

**Blocking prerequisite:** no production admission currently binds this typed
comparison. A separately authorized NEW diagnostic admission/prepared root must
pin its source/action, reader library and manifest, interpreter, sandbox policy,
request/result schema and helper-supervision budget. Existing consumed roots
cannot be amended or rearmed. This selection authorizes a design only, not that
new admission. Parent must separately select the diagnostic scope and authorize
its preparation before wiring/staging; later actual resource/start coordination
is also required. A keeper-written request cannot select a new library or grant
its own authority: it may only reference the exact already-reviewed admission.
The old B policy filename is not assumed valid for a new A diagnostic profile.

Smallest future wiring:

1. Keeper validates retained original Child/birth/admission/hash and settled
helpers, then writes one private SHA-bound diagnostic request containing that
identity, original keeper PID and selected source/library manifest. No arbitrary
PID/command ingress. It retains the original Child throughout and registers the
diagnostic helper before any launch-side failure can lose helper custody.
2. Spawn ONE isolated supervised diagnostic helper (existing -I/-B/-S conventions,
protected fixed-name sources/library, private temp, no model/auth/network). The
App sandbox must deny mutation/access to the helper-control channel as before.
3. In that helper, recheck exact original kernel PID/birth/parent/UID/executable
hash against the admitted request. Derive the keeper PID from the helper's
actual getppid(), require the App's kernel parent to equal that PID, and use the
request's keeper field only as an additional equality check. Compare the App's
full birth record against the keeper-bound snapshot; refuse orphan/reparented
helpers and stale births. Create ONE local AXApplication from that validated
original identity. Both direct C and Python read the SAME local reference. Do
not serialize or dereference an AX pointer from another process. The original
Child relationship is held by the keeper; the helper must not reuse the old
bound_identity requirement that the App's parent equals helper getpid().
4. Reuse reader.c/reader.h unchanged, and reuse native_b_typed_ax load/decode and
reference.ax_inventory(application=app). Split orchestration from capture(run)
only as necessary. Preserve fixed AXWindows/MainWindow/FocusedWindow/Children,
raw return/type IDs, per-reference owner result, CFEqual-to-app, duplicate and
role/error facts. Record distinct C/Python observation times and partial results;
sequential agreement is not atomic proof, disagreement is not automatic blame.
5. Write/close the C result before starting Python, so a later Python crash does
not erase it. Missing/partial/malformed output never becomes equality or proof.
The helper uses one fixed outer deadline (proposed10s, encompassing existing C3s
and Python4s plus identity/serialization allowance), with at least the existing
57s cleanup headroom reserved before entry. These are proposed budgets needing
review; no current controller budget or native scope is changed by this plan.
The current window-helper runner kills at4s and requires more than6s remaining;
it cannot supply this10s contract unchanged. Use a separately selected diagnostic
supervisor with its own retained helper handle and deadline, leaving the window
runner unchanged. Add that handle, including pending-spawn/unknown state, to
extra_cleanup_ready/original_custody/held reporting. Until diagnostic helper
settlement is proved, early Quit, original-Child reap and resource release must
all refuse. The keeper must never reap/release the original Child while the
helper is unsettled; retaining that original Child prevents PID reuse during
the comparison.
6. On helper exit/crash/timeout, the KEEPER remains alive and retains original
Popen. Existing policy may terminate/reap ONLY its retained disposable helper,
never the App/supplier; unknown helper settlement retains all custody. No helper
retry. Recheck original identity/reservation after helper settlement. The early
App-menu recovery above must be independently usable; diagnostic failure cannot
become qualification or permission for more UI input.

Required before any future native diagnostic: source/policy/library manifests
reconciled against current files; determine whether retained build3 still matches
rather than assume it does (a changed wrapper may require offline rebuild under
normal wrapper). New wiring-specific tests for exact request/decoder, wrong
birth/source/manifest, same-local-reference use, C crash, Python crash, timeout,
partial output, helper unknown and original keeper/Child survival; independent
Claude scrutiny of the helper crash/custody boundary. Reuse existing reviewed
reader and fixture tests where unchanged; no broad re-review or new framework.

No library was loaded or built and no diagnostic wiring was implemented here.
No new native run, admission/prepared root, candidate rebuild, namespace reset,
permission/TCC change or release follows from this source contribution. Parent
owns integration and any separately scoped diagnostic resource/start selection.

Validation before independent review:109 attended Python tests passed through
normal shared wrapper admission with a fresh scratch Codex home. New early-menu
cases exercise the actual traversal/intent/normal-exit code, including stage or
helper changes during final revalidation and intent fsync failure. This replaces
two older stub-only early-cleanup tests. No unchanged broad suites were rerun.

## Independent review return

Claude Opus5.5/high reviewed0daca1e8eba37bf577add801aa8cce1041c50f80
against1d86186ee682237a11b613ec00e528e730ed063e. No blocking/high code defect;
109 attended tests and10 extra offline review probes passed. Lower findings
were the coverage reduction now explicit above and a missing owner-notification
assertion, now restored on refusal/uncertain/intent paths. The medium diagnostic
plan gap is now a named blocking NEW-admission authorization prerequisite;
helper-specific supervision/settlement and actual parent-PID derivation are
explicit. No diagnostic source, root or live action has been added. Native menu
Quit effectiveness for this candidate remains unmeasured, and no review result
is execution approval. Fresh exact-head CI remains required before integration.
