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
