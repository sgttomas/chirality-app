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
