# Proposed qualification-only cancellation scope

Status: **UNSELECTED**. Agent 0 selected shipped-path witness first; do not
implement or activate the qualification-only20s feature. Retained as the
alternative considered, not the current plan.

Original proposal after inactive PR69 integration at
`1f67d3822b685c9c0d0ac4d52b0e52a570ef3d52`. No activation, build, interval or
product timeout is selected by this document. Ordinary human reading time
remains unrestricted. The prior 47.303s overrun remains failed evidence.

## Recommended method

Use a separately identified **nonrelease qualification build**, with a
compile-time feature for one narrowly defined zero-work Stop question. This
would exercise the exact App-created sheet backend and ordinary Stop effects
when a verified native affirmative answer arrives in time. Only that build's
question expires conservatively; default and release builds keep the existing
untimed product path. A compile error rejects the feature in release builds.
Do not reuse the synthetic distribution feature: it has a different purpose.

No environment toggle, public IPC cancellation command, filesystem control
endpoint, arbitrary window/PID argument or model call is needed. The deadline
is a private constant selected by the build and starts before presentation.
The controller cannot reset it or ask for another question automatically.
Admission pins the source, feature selection, build configuration, bundle and
executable hashes; the UI and retained diagnostics state that this is a timed
qualification question, not ordinary human confirmation behavior.

The narrow runtime eligibility gate must require the bound original source /
home / full generation, ready state and exactly empty observed work, request,
child and workflow sets (including unresolved-coverage sets). Unknown is a
refusal. There must be no overflow/digest-only statement or another modal.
Only Stop is eligible, not Restart, account/auth, request answers or workflow
acts. An ineligible question refuses in the qualification build rather than
silently falling back to an untimed dialog. There is no general new process
stop authority; the existing Stop assessment, confirmation and changed-work
recheck remain authoritative. The post-Cancel Quit route is the already
existing no-live-work normal Quit path; unexpected live work refuses and is
not converted into a timed affirmative Quit.

The compiled feature alone does not prove the state is invented or grant
permission to use any account. The manager's exact fresh admission must bind
the isolated candidate/state to the authorized invented scope. The old fdcf
candidate and its consumed ledger remain untouched. A new candidate cannot
inherit its successful A as native evidence without a separately justified
same-subject basis; new setup/relaunch provenance must be explicit.

## Deadline and custody contract

Proposed private question lifetime: 20 seconds of monotonic awake time from
before native creation. This is a **qualification-only proposal**, not an
adopted product setting or measured latency. It leaves part of the existing
30s modal phase for presentation, expiry completion and actual readback.
Before the one Stop press, require the existing full Stop/modal/settlement/exit
reserves. After a failure, recovery replaces settlement; latest entry is fixed
end minus 60s and the 40s exit reserve remains untouched. No extension, rearm
or second launch follows a missed budget.

The exact NSAlert+original parent are retained inside the App. At expiry, the
App marks that question nonaffirmative before ending only its retained sheet.
No AX discovery is necessary for this cancellation. AX and original-window
observations are still necessary to verify dismissal and source state before
Quit; lack of those facts remains a refusal. A normal answer before expiry
still requires the full live question/source/identity/AX/focus/image gates.
An expiry cannot satisfy the native Stop journey or LT23 witness.

The caller needs a typed internal outcome: Presented, Held, Dismissed(choice),
ExpiredDismissed or Lost. A worker may report Held/Expired without fabricating
a human act, but must not release the original Stop question gate while native
custody remains. Move the gate lease into the question lifecycle so that only
verified dismissal releases it; do not merely replace recv with recv_timeout
and drop the guard. A bounded worker waits on both result and status, and
reports unsupported custody promptly. No new public act endpoint is needed;
private diagnostic evidence and the existing view can carry non-authorizing
status. The original Child keeper remains owned through normal exit/reap.

AppKit main-thread stalls, process abort and failed native dismissal still
cannot be made into a hard 295s resource-closure guarantee without additional
termination authority, which is not proposed. Under such failures stop inputs,
deliver exact state immediately and retain custody. This is an exceptional
unsupported condition, not a default plan to wait for owner responsiveness.
System sleep also defeats a wall-clock bound because these clocks pause.

## Required repairs and tests before activation

1. Resolve the near-deadline button/endSheet race and exception boundary using
   actual AppKit API semantics. No unchecked claim that a second endSheet is
   harmless; objc2 exceptions escaping dispatch callbacks may abort the App.
   Native experiments, if needed, require a separately selected contained
   method; the inactive backend does not supply that authority or proof.
2. Implement the typed outcome and owned gate lifetime above; test Held status,
   missing completion, worker timeout without custody loss, late dismissal,
   stale callbacks and no action on expiry. Keep bounded later-turn detachment
   checks and one end request. Never substitute an unrelated attached sheet.
3. Wire only the explicit qualification build/eligible Stop path. Test default
   and release exclusion, invalid state, non-Stop calls, another modal, changed
   source/generation and overflow rejection. Supply an explicit displayed
   expiry statement and update only the selected qualification question grammar.
4. Establish actual sheet focus/parent/window mapping and dismissal focus
   behavior; this backend does not implement rfd FocusManager/PolicyManager.
   Controller cancellation recovery must not silently add activation fallback.
5. Account for creation, native calls, evidence writes, AX traversal/capture,
   tool round trips, expiry verification, Quit and exit against fixed caps.
   Existing local timings are samples, not bounds. Do not schedule a native
   journey until source checks, targeted tests, independent Claude scrutiny,
   fresh admission and the controller recovery contract are ready.

## Evidence and acceptance tradeoff

A qualification-feature build can establish an actual same-source
ready/Stop/settlement/Quit journey for **that exact instrumented candidate**.
It can supply bounded expiry-recovery evidence for that candidate. It cannot
by itself qualify the shipped untimed dialog path, unrestricted human reading,
long questions, release configuration, signing or actual workflow/model access.
A later product-path witness remains necessary if the owner requires that
claim. Calling the instrumented journey a release-native pass would be false.

Alternative: use ordinary product sheets and independently supervised AX
Cancel only. That is more representative of the shipped path, but it leaves
the exact unsupported-binding problem that blocked i7 and has no independent
bounded cancellation guarantee. It is not recommended as the next attempt.

Alternative: a general timed product question solves a wider lifetime problem
but reduces human reading time; that product/acceptance choice has not been
adopted and is not needed for the proposed instrumented method.

The concrete owner/Agent0 choice is whether to authorize this limited,
nonrelease instrumented witness as the next useful native milestone while
retaining the ordinary-product witness as open. If selected, specify the
qualification-only20s lifetime and eligibility/presentation boundary above;
then implement and review it as one coherent wiring change. If only an exact
shipped-product native witness is acceptable now, do not activate this feature:
resolve the ordinary-modal observability/recovery method first. No additional
new public controller endpoint is recommended in either case.

The five missing upstream notice texts remain explicit packaging gaps. Current
index correspondence is not complete notice coverage or release readiness.
