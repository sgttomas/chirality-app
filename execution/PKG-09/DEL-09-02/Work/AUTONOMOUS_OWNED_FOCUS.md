# Autonomous original-App focus and early normal-Quit recovery

Owner/Agent0 selected ordinary autonomous UI automation after el3pvau4. The
owner did reply Foreground at23:14:45.041UTC (parent message
0c4948b6-18ec-46cf-a179-ee5aaab8ce45, position3222). No completion file arrived
before the controller deadline. This was parent handoff failure, not absent
owner action or established App failure. The exact original Child54862 exited
normally0/adminwait0; all tracked resources closed in93.08127051172778s, no
overrun, slot END23:15:59UTC. No setup/B/Stop/LT23. Owner Quit message
5be8b59d-3598-4350-98df-48f71e3f9b69 arrived23:16:02.908UTC. The used root and
its original result/closure remain unchanged; supplemental facts/receipt hashes
are in private app-post-el3-assessment-y2ps41jf/closure-and-handoff-facts.json.

## Selected implementation

The prepared admission now selects autonomous-owned-focus/v1. The actual staged
helper reads that selection from the SHA-bound admission inputs, not a caller
request choosing arbitrary mechanisms. Both incarnations use the existing one
focus request; no Foreground event, reply or completion file is needed. The old
owner-foreground methods remain historical fixture support, not this route.

Inside the existing supervised helper, retain the exact original-PID AX app and
one distinct AXWindow whose number/title matches the existing owned WindowServer
binding. Require modal false and bounded nonmodal children. If already actually
frontmost, send no focus action. Otherwise require AXRaise support and settable
AXFrontmost, recheck original identity/window, perform one AXRaise, recheck the
same original window/reference, set AXFrontmost once, then observe real focus.
No AppKit fallback, alternate flags, LaunchServices substitution, global clicks,
foreign input, permissions/TCC changes, signals or retry mechanism is introduced.
A successful return code is never focus proof. Fresh bound capture follows the
helper; original/no-modal/menu-Quit and fresh foreground checks must also pass
before setup/readiness. A changed window or unknown effect refuses continuation.

Focus-dependent setup control/typing/popup operations still require actual
foreground and existing original source/window guards. No blanket background
keyboard allowance. Existing exact-owned menu-Quit remains an AXPress without
requiring foreground. Sheet Cancel retains its own original-sheet/focus gates.
The App's native questions, Stop/Cancel semantics and inactive PR69 are unchanged.

Early autonomous focus failure does not require a successful focus gate to try
normal cleanup: existing cleanup_original_main plus unique enabled menu target
must independently pass before the single owned-menu Quit. No Esc/Cmd-Q or
activation fallback. Missing original main, modal uncertainty, helper uncertainty
or ambiguous menu means no agent Quit; immediate exact owner normal-Quit recovery
is reported and original Child/helpers remain supervised. Routine attendance is
not required on the successful route; unsupported/catastrophic recovery is not
claimed autonomous or deterministic.

## Budgets, native limits and validation

The existing45s per-incarnation initial phase and shared160s pre-Stop cutoff,
135s Stop-entry reserve and295s total remain unchanged. No human reply allocation
is consumed. The port requires18s remaining before starting focus/helper/capture/
preflight. The new helper transaction has a3s deadline anchored at helper module startup, at most400 cumulative
AX/CG/libproc calls through its wrappers, with AX messaging capped at0.2s;
at most10 focus observations follow the one set. This count covers the new
transaction (including its bound rechecks), not earlier helper initialization/
initial binding or local CF conversions. These retain the existing whole-helper
4s wait and1s helper-only reap custody. Calls can consume the deadline before the
count cap. CF conversion/executable hashes share wall time, not a guaranteed fit.
Late action returns retain their rc/attempt trace before refusal. Native abort or
keeper timeout may leave no final trace; stderr/helper custody remains evidence.

Fresh post-el3 exact metadata basis:
app-post-el3-assessment-y2ps41jf/assessment.json, SHA256
fdec6b5490858f043199513ed019e9e936f8c5ec9517f835f75c666230452291.
AppData/setup/ledger, Preferences/SavedState/HTTPStorages remain absent;
WebKit21/Caches10. Repeated metadata matched, listed descriptor lsof was empty,
and candidate executable absent from process comm. Opaque contents were not read.
V3 pins this exact path/hash/prior attempt; v1/v2 remain unchanged. A new prepared
root is needed for these changed helper bytes; old roots are never rearmed.
Product candidate/source remains1f67d3822b-8c83d74ae3ce; no rebuild or repin.

Focused offline tests exercise one action sequence and actual observation,
unsupported/nonsettable/failed Raise/set/false focus, changed window/modal,
actual staged admission decoding/route refusal, cumulative native call cap and
unsent-action accounting, full A/B entry with no owner completion, and cleanup
success/refusal before foreground verification. Native effectiveness remains
unmeasured: AXRaise plus AXFrontmost is a selected supported method, not proof it
will overcome earlier AXFrontmost-only refusal. Missing AXModal/main semantics
can still refuse. Required independent Claude scrutiny and exact-head CI precede
parent integration; fresh resource/start coordination precedes any live interval.

Validation before independent review:101 attended tests,18 fixed-helper tests
and38 AX-route tests pass under the shared wrapper with fresh scratch homes.

## Independent review and bounded repairs

Claude Opus5.5/high reviewed5b670c7d0850c5a705aa7a001afc5750701f48a4;
no safety defect in focus/Quit gates, but CI failed because the newly exercised
helper fixture used a hard-coded sibling scratch path. It now uses system temp.
Mixed original application-self references are ignored after AXApplication role
validation, as cleanup already does; self-only/unknown/other windows refuse.

Each action now writes/fsyncs a separate exclusive-create intent before native
dispatch, bound to original identity/window/admission/sequence. Intent is not
proof the call occurred: a kill or post-write budget refusal leaves dispatch
unknown. Actual attempt flags are set only immediately before the native call;
returned rc is retained before lateness refusal. Native abort can still prevent
return/effect evidence. The transaction deadline includes initial source/hash
work since helper module startup, bounded by the existing outer helper limit.

The full AX/window/modal structure is rechecked immediately before Raise too.
The400-call cap covers four checks at the accepted8-root/8-child bounds, actions,
identity/WindowServer rechecks and at most12 total foreground reads; it is not
extra wall time. Support traces retain actions and settable rc/value. The port
rejects inconsistent attempt/rc/call-count traces. Recovery messages now identify
consumed focus and requested/posted Quit, without falsely claiming no input.
The bounded10-read focus wait is retained; a slow animation still refuses and
uses independently checked cleanup. No claim that native activation will work.

## Frozen review-repaired preparation

Repair source15d09ebc877b256c7622cbd49edc8f328239b81d;104 attended tests and
18 helper tests pass, alongside38 AX-route tests on the unchanged route code.
The native focus/early-Quit boundary was independently reviewed at5b670c7d;
bounded findings are repaired above. Fresh exact-head CI remains required.

UNRUN root:`app-attended-prepared-jag50nz3`; run:`2358c604b9b24b06b2b595754eb2670b`.
Prepared SHA256:`848fbab719bc6c69d9d48dad573884a858c1118df4f16d7d0ef43e77b357ff9d`.
All37 dependency hashes and8 staged artifacts bind the repaired source.
Candidate inventory/executable and v3 retained metadata were rechecked by actual
prepare. A remains prospective; B is not admitted and saved A is null.

Separate simulation-consumed root:`app-attended-prepared-xoyr2v0h`, prepared
SHA256:`63e7629434625975995e5ad00474f084f221759c7d2d78a51e9e57811a58518e`.
Six entry scenarios passed, including autonomous A/B gates with no owner offer
or completion file. Actual emitted A/B admission parsed through staged helper
sources for A-main, B-main and B-modal with a native-backend sentinel. B's
invented generation home validates format only, not actual B admission.
No App or native backend was invoked. Old roots remain consumed/historical.

Private report:app-post-el3-assessment-y2ps41jf/autonomous-preparation-result.json.
Guarded invocation:app-post-el3-assessment-y2ps41jf/coordinated-manager-jag50nz3.js,
SHA256:`e51c17a0fd5de3a9672093d4406e99a2b239cc805a8c4eeb6313c61881a7ef26`. Start/resource placeholders remain unfilled. No
Foreground callback exists on this route. Routine owner attendance is not an
admission requirement; parent integration/resource concurrence/start are.
Parent must still handle exceptional unsupported cleanup or an actual Cancel
fallback honestly; arbitrary native stalls cannot promise unattended closure.
No implementation permission implies live start or renewal of an expired root.
