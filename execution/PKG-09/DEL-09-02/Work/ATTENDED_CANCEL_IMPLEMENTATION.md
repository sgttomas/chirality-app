# Attended Cancel boundary implementation (not admitted)

Owner attendance was selected for one ordinary shipped-path Stop→Cancel
witness, with an immediate owner Cancel request if automated binding fails.
It does not select Stop confirmation, LT23, PR69 activation or a product timeout.

`native_sheet_cancel.py` implements one bounded discovery and a retained-ref
Cancel action. It requires original Child/window binding from its keeper,
exact original-main AXSheet parent/window mapping and unique enabled native
Cancel. Its adapter operates on the already-owned AX instance and does not
load native code or discover a PID. The keeper retains CF references through
cleanup. No public endpoint or launch entrypoint exists in this module.

Initial discovery has a60-call cap and15s cumulative cap supplied by caller.
Immediate revalidation uses the retained sheet/button references; it does not
repeat discovery or permit replacement. It refreshes original process/window
binding, sheet parent/role/modal/window number, control membership and uniqueness,
button parent/title/role/enabled/action and original App/sheet focus. It uses
at most42 calls within10s, allowing8.4s of0.2s calls and1.6s other work. These
are refusal caps, not native timing measurements. The modal allocation is now
15s discovery +10s revalidation/Cancel +5s contingency within the existing30s;
the previous proposed5s immediate step is superseded as inadequate. All
process/hash/WindowServer/evidence costs consume the same cumulative deadline.

Timeout installation, ownership checks and attribute/action calls count
separately. CFEqual compares retained references locally; no native subtree
search is hidden in equality. Mandatory evidence must succeed before dispatch.
The action is consumed before AXPress, including uncertain or late delivery;
there is never an automatic retry. Dispatch rc0 does not establish dismissal.
A failed corroborating image/question has its own retained failure, separate
from valid Cancel binding. Unsupported binding reports owner-Cancel-needed-now
with remaining fixed end and retained custody rather than waiting silently.

Ten fixture tests cover one Cancel only, separate failed observation,
changed identity/parent/focus/control, duplicate Cancel, unsupported discovery,
evidence failure, uncertain/late dispatch with no retry, native-call/cumulative
budget exhaustion and immediate fallback reporting. No test invokes a native
API. The actual native layout and costs remain unverified.

Still required before readiness: adapter/boundary independent review, integration
with candidate-bound keeper/readiness and Stop post, preflight placement before the Stop post,
actual source readback callback and normal Quit/administrative release,
owner-report delivery wiring, complete state admission and full inventory.
No old B qualification result/check_requests path may classify Cancel as Stop
success; this witness must have its own result type and no LT23 assertion.
The source-export build is ordinary product source1f67d382; PR69 is inactive.
No live start until checked candidate/controller/admission and resource concurrence
are delivered to Agent0 for the start announcement.

`for_owned_run` supplies the actual keeper-derived original identity/inventory
callback from the already posted source-bound Stop context. It rechecks original
identity on both sides and never accepts a caller PID. The attended runner must
still select it explicitly; the old B launcher is unchanged. `dismissed` gates
hierarchy/focus and requires a fresh source callback; the result never asserts
Stop confirmation or LT23. Ownership of adapter.close stays with the keeper.

Actual product build preparation is frozen at1f67d382 in private scratch
app-parented-witness-prep-9tc0cg33, release profile/custom-protocol and
existing distribution-successor, publisherNone, unqualified package-test
namespace, copied dependencies/offline/jobs2/no-sign. This is the ordinary
untimed product; no PR69 cancellation caller exists. Build/resource evidence
must finish before candidate identification or state admission. Missing notice
texts remain explicit, not manufactured or downloaded.

Build completed with exit0 and slot release. Identified build subject:
`1f67d3822b-3bf68520e11f`, bundle-tree SHA256
`3bf68520e11f058bdf987ce481d8fe8cacf67b502a145f3474ac82193c5b7a91`,
identifier `dev.chirality.app-v4.package-test.9tc0cg33`.
All50 resource mappings match source bytes; tracked source export verification
passed. All three declared namespace directories were absent at identification.
Private `build-observation.json` and `bundle-inventory.json` retain exact facts.
No native launch or state admission follows from these read-only checks.

Concrete admission dependency: this new namespace has no saved A setup request
or initialized ledger. The old fdcf/A/B state must not be relabelled or reset.
A candidate-bound setup plan must supply the authorized invented choices via
the ordinary product path before this candidate can reach source-bound ready.
No direct DB seeding or auth read is authorized/implemented. This is an actual
remaining preparation dependency, not an additional owner permission request
for the already authorized offline work.

## Selected two-incarnation sequence and actual preparation

Agent0 explicitly selected the required setup relaunch within ONE attended
witness and ONE295s slot allowance: A native setup/save→normal Quit and fully
closed original Child/helpers/release→fresh B state admission→B launch/actual
ready→one Stop→Cancel→normal Quit/closure. No third launch or retry is allowed.
`native_attended_sequence.py` implements this sequence over explicit keeper
ports and is exercised end-to-end with invented ports. It consumes Quit and
Stop intents before dispatch, blocks B after failed A closure/readmission,
refuses reused incarnation/release/helper identities, and closes before Stop
if the160s combined setup/readiness cutoff is missed. No Cancel observation is
promoted to Stop/LT23 qualification. Failed question/capture evidence is retained
while independent Cancel remains usable. Unsupported binding immediately asks
for the selected owner Cancel fallback; dismissal/source must still be read.
The actual keeper-port adapter is not yet complete; this is not a runnable
native launch entrypoint or an admitted execution root.

Ten sequence tests cover normal two-incarnation flow, A closure failure,
fresh admission failure, both cutoff cases, failed question with valid Cancel,
unsupported binding, uncertain Cancel/no repeat, failed dismissal/no Quit and
reused Child identity. Two additional admission tests require precisely three
initial session-start/empty-Quit/normal-end rows with original A session, no
previous session, no work/Stop requests; extra/wrong rows refuse. Actual B
readmission uses ro/immutable/query_only SQLite, typed schema validation,
no App sidecars and current-user descriptor checks plus stable before/after
hash/stat. It does not read supplier contents or accept arbitrary future rows.

Private exact invented input plan now exists under the new build's
`witness-inputs/input-plan.json`, SHA256
`7964cfea36437b5da93efcfa701115f0c6300b87db514484ab999d717d9253a3`.
It binds candidate/source/bundle/executable, four invented source paths, closed
file hashes, two-launch limit,295s total and135s Stop-entry reserve. It records
saved_A=null, ledger=null, launch_ready=false. Only ordinary setup may create
those state artifacts. Empty account/fallback Codex fixtures contain no auth;
no ~/.codex read is needed. Fresh full bundle inventory and the three absent
namespace checks passed in `candidate-A-offline-preflight.json`; that record
explicitly grants no launch authority and no B admission.

Budget: total295s; Stop requires135s remaining, so all setup/first normal exit/
fresh-state admission/second launch/readiness/preflight must finish before160s.
There is no source-backed shortcut around next-launch-only setup. No native
measurement establishes that this first candidate will fit. Crossing the
cutoff forbids Stop and requests only known-safe current-child Quit within the
remaining reserve. Native timing and actual new-state row shape may refuse;
those outcomes are preserved rather than patched by guessing or resetting.

Review separation: the retained-sheet component review was dispatched at
38b755f2. The two-incarnation custody/readmission addition requires its own
meaningful scrutiny before live use; that earlier review is not claimed to
cover it. Native keeper-port integration, source readback/parent report delivery,
actual complete input-policy admission and shared start coordination remain
open. No owner attendance or live interval has been requested.

## Review-response corrections (supersede earlier component limits)

Claude review of38b755f2 found missing exact Stop button identity, unchecked
readback claims, repeatable failed discovery, an oversized admitted layout,
missing late dispatch receipts, fallback delivery blocked by record errors and
unbound preflight. Source corrections require exactly Keep Codex running /
Stop Codex / Cancel during discovery and immediate revalidation, retain those
button observations, and consume each discovery/preflight/cancel/dismissal phase
on entry. Initial main children are capped at5, sheet children6; the maximum
accepted layout now fits the60call discovery cap. Immediate revalidation cap
is46calls (9.2s timeout allowance within10s; remaining overhead may refuse).
All phases share an enforced190call lifetime cap. No failed phase can reset
that allowance or silently repeat discovery. The first absent sheet therefore
requests attended fallback immediately, not an uncounted poll.

Cancel dispatch separately prechecks budget, sets attempted immediately before
the native call, and retains return code/error/start/end/late status even when
it returns after the deadline. Unknown/late delivery is never repeated.
Fallback messages say to click Cancel only if the Stop sheet is still visible.
Delivery precedes sequenced evidence writes, which cannot suppress delivery.
Preflight resolves original keeper identity/main facts and checks the passed
AX main's window number. Stop context and generation are rechecked on each
binding call; preflight can now run before Stop is posted.

Dismissal requires typed actual generation, ready state, enabled Stop, absent
sheet row, successful full source gate and empty same-generation stopping /
LT23 rows. It does not manufacture a negative LT23 claim without that readback.
Actor is agent only after rc0 and no owner fallback; uncertain delivery is
undetermined unless an actual owner Cancel completion was supplied. If automatic
binding never succeeded, actual owner completion plus no remaining sheets,
restored main focus and no new owned on-screen windows/full-source readback is
required. The callback must derive those facts from live observations; the
current component fixture is not a substitute for that unfinished integration.

Seventeen component fixtures now pass, including maximal accepted layout,
Cancel-only unrelated sheet rejection, failed-discovery no repeat, typed
readback refusal, uncertain actor and retained late rc. These manager fixes are
not a clean independent rereview claim. Native layout/timing remain unverified.

## Two-incarnation review correction — supersedes three-row assumption

Independent Claude review atf53ccb18 identified launch-exception custody loss,
escaping fallback delivery errors, stage-inappropriate/duplicate Cancel notices,
missing owner-completion ingress, record-error suppression of valid Cancel and
receipt identity checks after custody release. Corrections mark custody unknown
before either launch port, retain/report unknown custody on any BaseException,
consume one fallback delivery attempt, distinguish sheet-pending from post-
dismissal/identity failure, and require an actual bounded owner-completion port
before the owner fallback readback. Unknown delivery does not escape or repeat.
Question-observation record failure retains failed evidence status but does not
block independently valid Cancel. Closure receipt helper/release presence and
distinctness are checked before clearing custody on every path. Actual component
dispatch standing supplies cancel_attempted; prechecks alone are not a click.

The prior fixed-three-row A admission was **unsupported and is removed**.
Source basis: lib.rs2617–2646 requires resolved host config/namespaces for
recovery initialization; runtime_session.rs initialize_with_namespaces propagates
that failure before opening the ledger; desktop_startup NewHome preparation
only saves pending references for next launch and does not reconfigure current
owners. app_quit records only where a ledger host exists. Consequently the
selected empty-namespace/setup-only A expects **no runtime recovery ledger**.
Any legacy JSONL, SQLite or mutable sidecar is an unexpected state refusal,
not a guessed alternative row count. B must validate the actual ordinary saved
request digest, account/source references and links after A closure, while
observing the expected ledger absence. B's fresh startup generation and
protocol/source proof must bind that exact request/account; no invented A
generation or previousSession linkage is required when A had no ledger.

The admission reader now directly enforces this absence locally (no injectable
sidecar-check object), checks build-observation.json as a plain owned file,
and requires empty fallback Codex home/tmp without reading auth contents.
Additional prelaunch metadata-only absence checks cover Preferences plist,
Saved Application State and HTTPStorages. Their post-A actual metadata still
needs bounded collection/readmission; absence at build time is not a promise
that they remain absent after normal use.

Sixteen sequence tests now include A/B launch exceptions, failed owner delivery,
double-failure single fallback, post-dismissal Quit failure without a Cancel
request, observation-record failure with valid Cancel, and missing helper receipt.
Two admission tests verify true absence and rejection of any unexpected ledger /
sidecar without creating files. These18 tests and17 sheet-component tests pass.
The report is scoped source/mock verification, not a completed native port
adapter or exact-head integration review. No launch authorization is inferred.

## Build-selection correction and distinct current candidate

The release-profile artifact `1f67d3822b-3bf68520e11f` remains unchanged/unrun as
packaging evidence. It is **ineligible** for the selected unsigned owner-use
startup: desktop_startup.rs951 restricts that branch to debug assertions; the
production successor path instead requires installed custody/publisher inputs.
Neither guard was changed. Treating that release artifact as ready-capable was
a preparation error, caught offline before any App launch.

Agent0 accepted a distinct ordinary debug build of exact1f67d382 with only
custom-protocol/default distribution selection, no PR69 caller/qualification
feature. It completed rc0 under normal shared t3_slot/jobs2/offline/copied cache,
without bypassing SWB exclusive locks or starting a native interval. The first
configuration attempt was rejected by Tauri before compilation for an underscore
in the generated identifier; its config/log/result remain retained, and only the
new configuration was corrected before the successful build.

Current candidate `1f67d3822b-8c83d74ae3ce`, identifier
`dev.chirality.app-v4.candidate.gvpud8q`, bundle-tree SHA256
`8c83d74ae3ce1ea0116234ff654f1db23ebb6ccc760d05c1af66c325b19039b1`,
is retained under `app-parented-debug-_gvpud8q`. Full source-export verification
and50 mapped resource byte comparisons pass; declared namespace directories
remain absent. The separate invented input plan SHA256 is
`f0da12bb0b631d77ee94ce0b4abdc584c2077925b2ea6d60e03871230ae292a7`.
A fresh preflight verifies full bundle/executable, exact build invocation/debug
selection and input paths/hashes/empty fallback home/tmp/additional namespace
absence. It reports B_admitted=false, saved_A=null, launch_authorized=false.
The older release input plan is retained as ineligible, never relabelled.
Five missing notice texts remain explicit; no signing/publication/native pass.

`native_attended_readback.source_after_cancel` now supplies a concrete read-only
callback over the existing keeper/main AX path. It revalidates original identity
and complete main/inventory before/after, rejects any newly visible owned window,
decodes actual displayed protocol text, calls the existing source/ready gates,
requires the actual enabled Stop control and rejects same-generation stopping
or LT23 rows. An instance-only AX library wrapper counts nested native owner /
timeout/attribute/window-number calls and enforces the cumulative deadline;
CF decoding/evidence/hash costs also consume that deadline. A2000call maximum
is a hard expansion limit, **not** a2000×0.2s timing-fit claim. Timeout-heavy
observations will refuse before completing. The original library is restored
on all exceptions. Six fixtures cover cap/deadline/late return and complete,
changed-source and terminal-effect readbacks. Total current focused fixtures:
17 sheet +16 sequence +2 admission +6 readback =41, all pass offline.

Native two-incarnation launch/keeper-port wiring, setup-form sheet observation,
actual T3 delivery/owner completion ingress and full phase policy admission are
still incomplete. Existing source tests and source-readback callback do not
establish native timing or authorize running the draft. The next reviewable
integration must connect these exact components without calling the old B
Stop-confirmation/qualification path or old A forced-termination cleanup.

## Native adapter integration draft

`native_attended_ports.py` now connects the sequence methods to the retained
B original-Child reservation, guard monitor, exact-window helper, maintained
ordinary setup form and fresh AX route. Launch registers the Run before spawn,
then reserves the actual Child before other IO. A and B have separate roots,
admission hashes, helpers, birth bindings and administrative receipts. A's
policy forbids process-fork; B uses the reviewed exact App/supplier/allocator
policy, with build/source paths additionally write-protected. No signals or
old A forced-termination cleanup are used. No native CLI execution entrypoint
or launch-ready admission root is supplied yet.

The setup native question is now derived from direct original-main AXSheet
children, original parent/PID/window mapping, unique new owned row and actual
native title/affirmative control. The maintained form still verifies the full
actual invented effects before one setup confirmation. Original main capture
uses the supervised exact helper. This requires scrutiny: it changes the
setup observation boundary, not the product question or human reading time.

The attended phase adapter keeps caps ready60/recheck35/Stop20/modal30/
settlement45 and shortens them to the shared absolute cutoff. It does not
reuse the earlier chained minimum reserves, which would make B readiness
require265s left after A. All pre-Stop work ends by fixedEnd−135; no cap is
extended, and insufficient setup time refuses before Stop. The full setup AX
walk/calls are cumulatively deadline-counted; the expansion cap is not a
worst-case timing-fit claim.

The native question callback reads actual sheet AX text and runs the existing
exact Stop question grammar without pressing its affirmative control. It does
not fabricate a sheet screenshot; initial/ready owned-main images remain
corroboration. Dismissal uses the actual counted source callback and closes the
sheet adapter CF references before Quit. Quit is exactly one owned menu action,
never a Quit-question confirmation; normal original Child exit0 and settled
helpers are mandatory before the fresh admission-bound administrative intent
and original wait. Guard thread closure is required before returning released.

`native_attended_owner.py` defines the private manager handoff: an immediately
flushed event requires the active tool-session manager to forward it to Agent0
through T3. A candidate/incarnation/admission-bound0600 single-link completion
file is accepted once and only after the actual new owner 'Cancelled' response.
This is a manager control channel, not App IPC. Emission is **not proof of T3
delivery**; the eventual supervising execution cell must implement/record that
forwarding and remain engaged. No old owner response or screenshot substitutes.

Five native-port mock tests cover normal Quit/reap ordering, unknown helper,
nonzero exit, unsettled guard and pending B sheet refusal. Two owner-channel
tests cover exact one-time completion and missing/wrong admission. Current
focused tests:31 attended modules plus17 sheet =48. No native call was executed
by these tests. Complete native entrypoint admission/policy staging, active
manager tool-forwarding/held supervision and post-cutoff supported recovery
remain explicit readiness prerequisites; this draft cannot be run unattended
or presented as checked live readiness. Meaningful review of this newly
connected custody/setup boundary precedes activation.

## Native-hookup review corrections

Claude review of0718b69c found that setup keyboard calls were rejected by the
AX-only wrapper, normal BAX walks exceeded the chosen call caps, original Child
binding raced sandbox-exec, setup-sheet association lacked a pre-post baseline,
Stop set cleanup before dispatch (skipping guard checks), and guard joining was
too short. The following are manager corrections, not a claimed clean rereview.

The setup counter explicitly permits only the four existing keyboard CG calls
and checks CGEventPostToPid against the original Child PID. Readback remains
AX-only. An actual BAX fixture traversing416nodes uses8320 counted calls; the
former2000cap could not pass an ordinary walk. New expansion caps are20000 for
one source readback,4000 for the native question, and1000000 for the multiwalk
setup form. No elapsed deadline is increased: these are expansion ceilings,
not worst-case latency claims. All nested owner/timeout/attribute calls still
consume the same absolute phase deadline, and timeout-heavy runs refuse.

Original birth binding now waits at most5s/26samples for the same unreaped
sandbox-exec Child to exec the exact App. Kernel pid/parent/uid/start tuple must
remain unchanged; any other executable or birth refuses. Fresh App hash and
identity are then checked. Accessibility trust is checked without prompting
before spawn. Controller roots must be outside protected build/repository
paths; A policy replacement must occur exactly once, phase roots must be0700,
and stdout/stderr use exclusive creation.

Setup records original owned inventory immediately before its one web-level
prepare/save post. Native sheet lookup then uses a fresh inventory after AX
children: missing AX children/WS row may receive only the existing bounded
read-only wait, while ambiguous/contradictory facts refuse. The sheet requires
a new distinct owned row, supported title/layer/bounds, original-main parent,
modality and sheet focus. The same source effect checks precede affirmation.

Stop keeps cleanup=false and guard/heartbeat/reason checks through its post;
only after the Stop intent has been consumed does cleanup mode apply. Quit is
now an explicit bounded cycle-pruned original App menu traversal and one
AXPress, with no activation, Esc or Cmd-Q. It retains rc/error/late timestamps
before refusing late delivery. No Quit question is affirmed. Menu lookup/post
is capped at5s and cannot borrow the40s exit reserve. Guard join uses the prior
8s bound, and retained-state reports separately list reaped App versus still-
live guard custody. A's normal-exit wait may consume the remaining resource
interval; if A closure is past160s, B is refused, not launched on a new budget.

Current focused mocks:35 attended modules +17 sheet =52. Added fixtures cover
416-node BAX traversal, exact-PID setup keyboard counting, original exec transition
and birth replacement refusal. Native adapter use remains unexecuted. The entry
supervisor must still stay active through late owner recovery/guard closure;
these tests do not establish hard closure or native timing fit.
