# CCE-INIT-ORDER-01 — D-independent initiation and text admission

PROPOSED SOURCE OPTIONS / CONSEQUENCE ASSESSMENT ONLY. Basis
58e10166a6e5ae1bab1a12b4851e122f293e1c2e. This continues the merged
CCE-ROLE-SOURCE-01 and Host CCE proposal without changing their bytes or any
accepted ROLE/Host/WR/EXEC/Root contract. It selects no implementation, dynamic
tool, native child carrier, permission, graph edit or owner act. All operations
and types newly named below are proposed interfaces, not available capabilities.

## 1. Actual current boundary

Current lib.rs offers ordinary thread_start/conversation_send_text and connector
read/prepare/publish operations. It has no C3 TASK initiation command. The role
composer refuses TASK primary entry. NativeRequests classifies item/tool/call as
known-app-unsupported because the App has no registered dynamic tools. HOSTING
§6.1/§6.8 and ADAPTER F-9 explicitly retain that limitation; registering a tool is
a real Group A source change to the familiar App tool set, not a hidden callback.
Root's permission for WORKING_ITEMS to delegate and its managed delegate_agent /
native-descendant mechanisms do not make an App tool or bridge exist.

The stock child route is different: an actual completed native spawn can expose
receiverThreadIds and child metadata through Group A NPT/Host. ROLE CR-1…5 still
requires real App-supplied child-role configuration and its supported carrier;
current child_status is not-supplied. agentRole alone cannot prove TASK supply.
The existing CCE origin contract also requires an App-submitted original text
request: a native spawn prompt cannot be relabeled as that SourceRequest.

WR pending_notice_for currently reads per-run atomic flags under the root lookup;
WorkflowRun mutates its notice and syncs that flag under its own run ownership.
conversation_send_text checks the notice path before ordinary Host dispatch.
This is not a shared notice/CCE dispatch lease. Host registers a SourceRequest,
then acquires frame_write and the source gate/Inner before actual write-attempt
admission, releasing the source locks for the pipe write. These real boundaries,
not independent snapshots or send/receipt counter comparison, constrain a join.

## 2. Compare the three routes

| Route | Genuine initiation source required | Current gap and consequence |
|---|---|---|
| Person-requested App task | An actual App task-entry invocation, frozen project/base/question and original child thread/start admission; never a person boolean or a human-act claim | No such C3 entry exists. A new narrow task action could serve explicit human requests, but alone it does not let a manager delegate. Requiring the person to drive each graph item would recreate the routine human-facing rail OD-01 rejected. Do not equate renderer input with verified human identity. |
| Source-bound manager request — recommended source target | A real agent→App invocation of a newly registered managed-delegation operation, bound to the actual manager thread's offer, native request and role admission | Currently absent. Requires named Group A Host/catalog/adapter/native-request and ROLE source adoption plus C3's bounded handler. It avoids relying on a child-role carrier that is not established and needs no Fleet service. It is not usable on unchanged current main. |
| Stock native child | Actual original native spawn, supplied TASK carrier/configuration, completed spawn and admitted child relation; then a reviewed CCE origin route | Agent-callable delegation can exist natively, but the App TASK carrier and child-origin proof are missing. A native child is not automatically a qualifying TASK answer. This route needs Group A role/carrier and origin work, not Group D's durable fleet index; it is a valid future alternative, not a fallback for a failed manager request. |

A file watcher or copied final/history JSON is not a fourth route. Ordinary graph
file work and fileChange observations retain OD-01's evidential limits; they do
not silently become a task-request source or a grant. App-origin mcpServer/tool/call
must not impersonate an agent's request (HOSTING R4-12).

## 3. Smallest recommended manager entry — genuinely missing work

Recommend a narrow Group A-owned App receiver for Chirality-managed delegated
sessions, with a C3-specific request contract. The final tool identity/version
must be frozen in the owning catalog/adapter change; `CCE managed-task entry`
here is a design label, not a tool advertised as available. Adopting a tool name
alone does not establish Root delegate_agent compatibility. Group A must define
and prove the managed session mechanism, actual parentage, full TASK guidance,
scopes and enforcement limits under Root/D-GOV-35 before C3 uses it.
D-GOV-35 items 1–2 and SPEC §9.7 require actual governed managed child sessions,
a sealed brief/context, explicit declared scope and reconstructible durable
evidence. A transient thread/start shim is not that managed path; the retired
record-less SDK bridge must not be restored under a new tool name. These
requirements are a hard missing-input condition for the recommendation, not an
optional later enhancement. Group A/Root must identify the actual managed-session
service and its governed evidence interface before implementation; if unavailable,
this route stays unavailable. Do not quietly substitute C3 R2 or Fleet D storage.
Minimal managed-session facts are not a passed R2 recovery/current-status design;
any new storage/atomicity choice requires its own owning source review.

Minimal entry has two bounded operations: request one answer and read that
request's current result. It is not a writer, scheduler/fleet registry or permission
broker. A request identifies an exact existing C3 base (project-relative locator,
ID, raw-byte length/hash), question and claim IDs. C3 resolves/validates them under
the actual associated project and freezes the intent; the argument values are
untrusted selectors, not origin or authority. No role, grant, write target,
home or policy override is accepted from the model as an authority input.

For request issuance all of these must agree:

1. Group A actually offered the exact reviewed tool definition to this manager
   conversation at its genuine thread admission. A valid tool-call-shaped frame
   for an unoffered tool is answered as unsupported, never treated as a request.
   Existing conversations without the offer remain ineligible: no unobserved
   retrofit of tools or re-selection of their role. Native capability absence
   refuses this route without switching provider or vetoing user configuration.
2. Host receives the real item/tool/call on its admitted current source and
   retains request ID, registered tool identity, argument value identity under
   the named Host parsed-frame method (never claimed wire bytes), thread/turn,
   home/H5, receipt cut and pending/reply state in a private source handle.
   on_line does not invoke C3 while holding Inner: existing protocol handling
   retains every request/frame and dispatches a closed handler after release.
3. The role owner supplies the actual current HELP_HUMAN/WORKING_ITEMS lease.
   Root permits their bounded TASK delegation, but this role check is eligibility,
   not a new grant. The existing undertaking must permit the work; effective
   project/home/native user approval and sandbox choices remain governing.
   The service may not derive a more permissive policy from tool arguments or
   pass guessed policy inheritance. Unestablished policy/source correspondence
   is unavailable, not an App override.
4. C3 freezes the exact bounded source/intent and one active attempt. Group A's
   managed session producer performs a fresh stock thread/start with common+TASK
   guidance, preserves native base/configuration, and obtains actual complete
   write/result/active admission before issuing the role entry. Then the exact
   answer turn is separately admitted. delegated=true, a generic bind or an
   external Root tool result cannot stand in for this actual App chain.

The tool reply distinguishes request admitted/in progress/refused/unknown from
answer observed. It is a protocol reply, not a contribution mint or permission.
Return promptly after the actual attempt state is known; do not hold CCE/role/
WR/Host locks while awaiting a child. The result operation reads only that live
attempt under a fresh genuine manager request and original source association;
a token is a selector, not transferable authority or cold hydration. Duplicate
calls cannot create a second child or hidden reservation for the same active
working set. Exact duplicate delivery settles once; conflicts refuse. No numeric
wait duration or new lifetime capacity is selected here. Root-required managed
session evidence cannot be omitted on the pretext that the CCE working set is
transient; if the managed service cannot supply it, no child is started.

A TASK answer still needs CCE-A2's actual request-bound final/terminal join. A
manager final message from the initiating tool-call turn is not automatically
its review: review requires a fresh exact answer-bound App request, a distinct
conversation from TASK and the independent source join. No positive review enum,
integration plan or R2 persistence is supplied. Parent closure/cancellation and
late effects preserve the already described actual/historical distinctions;
no automatic resend, rollback or revived lease follows.

## 4. D independence and consequences

A supplies the generic managed-session/tool-source/admission primitives; C owns
base/question/answer semantics and its handler. Group A can be checked with a
bounded test handler independently of C's completed producer. Optional handler
registration is a consumer extension point, not a requirement for the baseline
Host to depend on C's completed work. No DEL-06-01 record, fleet registry/view,
DEL-03-04 guide completion or Group D witness is an input to initiation.

FLEET FR-D5 calls only native Codex children dispatch_observed; a new App-managed
TASK thread is not that event. Do not mint a native spawn, related_conversation
or external_result merely to fit an existing Fleet enum. This route issues only
its own authentic Role/Host/C3 facts. Future Fleet presentation/recording would
need its own receiving decision/version, and remains outside C3's prerequisite
chain. Nor does native-child initiation itself require D's durable fleet writer:
its missing inputs are the Group A carrier and original-source proof.

Thus the recommendation is new bounded A→C source work, contingent on a genuine Root-compatible managed
service supplied through A rather than a new delegation class, with later optional A/C→D
receiving. It changes no group order or deliverable set and invalidates no prior
Group A result: no-tool/unknown-child-standing were truthful for that increment.
The new increment must explicitly amend/select the affected A interfaces and
rerun their actual receiving checks; it cannot claim prior qualification covers
new tool availability. Record the relationship in affected work graphs at adoption
under GC-8, not in a new standing relationship register.

No GC-7 owner question is raised by this recommendation. A concrete trigger would
arise only if adoption instead required D's Fleet dispatch service/record before
C3 could ask, or insisted App-managed threads count as already accepted native
Fleet dispatch. Then ask whether to change that dependency/meaning or retain this
D-independent route; do not silently reverse A→{B,C}→D. That alternative is not
selected here. Root mechanism or user-policy incompatibility likewise returns
with its exact source conflict before adoption, not a fabricated blanket gate.

## 5. Exact proposed WR/role/Host text-admission sequence

This sequence applies to the fresh TASK answer and later manager review text,
not to the inbound tool request or its ordinary protocol reply. It is a proposed
owner interface, not a claim that current atomic flags implement it.

WR must own a per-conversation notice-admission guard: original owner identity,
monotonic revision and exact pending-notice state. All transitions that can create,
resolve or replace pending status (including chain success/failure, actual notice
send disposition and supported skip) update it at the same owner linearization
point as notice state, before releasing ownership. ABA false→true→false changes
the revision. Existing run/file persistence remains outside the short guard;
its success is never fabricated by updating a flag. CCE never acquires or reads
a mutable WorkflowRun while holding the new dispatch chain.

| Step | Locks and exact operation |
|---|---|
| P0 resolve/prepare | Resolve project/base, read guidance, validate and serialize exact single text, look up source-owned handles and capture CCE/role/WR revisions outside live dispatch locks. Release map/home/root/run locks. Follow CCE-A2's existing base rules; do not claim a filesystem lock or new grant. |
| P1 reserve/register | Reserve the one bounded CCE capture before registering the original Host request; bind immutable frame and role/intent pins, but claim neither write nor emission. Release locks before waiting for output serialization. |
| P2 serialize access | Acquire Host frame_write without holding CCE, role, WR notice, source-gate or Inner locks. A waiting/failed operation can be cancelled; no owner lock is held across that wait. |
| P3 joint admission | With frame_write held, acquire CCE working-set → role owner → WR notice guard → Host source gate → Inner. Recheck exact source/pipe, H5/home/thread, admitted role lineage, CCE intent and WR owner/revision; require no pending notice. Require the original request still eligible. No filesystem parsing, supplier call or arbitrary callback occurs in this chain. |
| P4 ordering cut | Under the same chain, mark actual write-attempt admission and receipt-position dispatch_cut for the reserved capture. This is the shared order point versus WR notice becoming pending. Send/receipt positions remain separate domains. Release Inner/source/WR/role/CCE locks before the pipe write; retain only frame_write for the actual existing serialized write. |
| P5 result/mint | Only actual complete write sets write-complete. Process original responses/events under Host rules, wait outside owner locks, then reacquire the reviewed owner chain for exact mint/freeze/currentness. A prior admission is not successful emission. Release serialization before waiting for turn completion. |

If WR wins P3/P4 first, CCE refuses before its frame admission. It neither prepends
notice bytes to an already frozen intent nor clears/skips the notice. Existing
ordinary text/WR mechanisms may resolve the notice; a later request prepares
again. No empty clearing turn or automatic retry is invented. If CCE wins P4,
a subsequently pending notice belongs to the next eligible turn after that
already admitted request, even if its write is still in progress. This proposed
ordering rule requires explicit WR/EXEC concurrence; it is not inferred from
wall-clock timestamps. A failed/partial write preserves its actual outcome and
the later notice remains pending for fresh admission.

The actual call-graph proof is mandatory. Current WR operations can hold a run
mutex while calling Host's writer. The proposed CCE sender must therefore never
acquire a run/root mutex after frame_write, and no notice-state producer may
acquire frame_write while holding the notice guard. Host on_line/closure hooks
acquire neither CCE, role nor WR guards; existing role receiving may inspect Host
but must not wait for frame_write while holding the lease mutex. If any real
reverse edge exists, return that edge before implementation rather than asserting
the written order fixes it. A private no-notice handle must not be obtainable
from a public boolean, an atomic load or independently valid snapshots.

## 6. Designed proof cases — not executed

| Case | Required result |
|---|---|
| IO-01 offered manager request | Real registered tool call + admitted manager + exact valid base/question produces one genuinely admitted TASK start and exact answer turn; supply observed/adoption unknown, native policy preserved. |
| IO-02 false request origin | Unoffered tool, renderer JSON, transcript text, file watcher, App-origin MCP call or copied server-request DTO cannot issue intent. Always retain normal protocol/error handling. |
| IO-03 absent capability | No registered entry, no genuine managed service/sealed-brief/durable-evidence support, unsupported native carrier/provider, TASK/no-role caller or unknown project/policy correspondence refuses this route without invented fallback or blocking ordinary work. |
| IO-04 actual admission | Failed/partial start, wrong returned thread, changed home/H5 or absent original role provenance cannot become TASK admission; preserve actual effects and no resend. |
| IO-05 notice before preparation | Pending status refuses CCE preparation/dispatch; existing ordinary notice behavior remains. |
| IO-06 notice while queued | Notice appears after P0 or while waiting frame_write: P3 refuses. Cancellation/source closure while queued likewise refuses without stale write. |
| IO-07 notice before cut | Instrument notice creation racing acquisition of the WR guard: exactly one P4 order wins; no check-then-write hole. |
| IO-08 notice after cut | Pause actual write after P4; create notice. The admitted request retains original bytes, later notice is pending for the next eligible turn, no false supplied/recorded claim. |
| IO-09 failed write | Fail/partially write that admitted frame; never infer a completed turn or consume the pending notice; fresh admission observes it. |
| IO-10 ABA and replacement | Notice set/cleared/replaced, owner replacement, role continuation or intent revision change invalidates the prepared pin even if a boolean/label again matches. |
| IO-11 ordinary WR regressions | Real pending notice goes first once, busy run and record-failure/skip semantics remain; no CCE bypass, synthetic clearing turn or new run/act is introduced. |
| IO-12 source/capture | Early item/terminal versus write/result, duplicate/conflicting frames, late closed-generation events and cancellation follow the Host proposal; no current mint from historical facts. |
| IO-13 review separation | Initiating manager-turn output is not answer-bound review; require fresh exact review request and distinct TASK/manager source identities. |
| IO-14 lock/budget | Paused frame writer and concurrent WR/run/role/native callbacks show no reverse edge or owner lock across IO; metadata and buffers remain within the shared CCE budget, no hidden lifetime reservation. |

## 7. Adoption boundary

Future source/consumer fence, subject to owning review (no code authorized here):

| Owner | Actual affected surface |
|---|---|
| Host / DEL-01-01 with DEL-01-04 NIR/AAC | hosting.rs original inbound tool-source and outbound admission; native_requests.rs explicit registered-operation routing and exactly-once protocol reply; lib.rs actual thread-start offer/dispatch wiring. No person-answer or copied reply can create the task. Freeze generated-protocol fields and the offer identity before code. |
| Catalog/adapter / DEL-03-01/02/03 | Name/version and meaning of the new App-offered managed-delegation entry, native capability/absence behavior and familiar-set change. This is new Group A work, not an existing Root tool assumed available. |
| ROLE / DEL-02-04 | role_supply.rs, role_lifecycle.rs and role owner in runtime_session.rs: full TASK composition, authentic original admission and continuation lease; no primary-entry or generic-bind shortcut. |
| WR/EXEC / DEL-02-02/03 | WorkflowRootSession/WorkflowRun notice transitions, source-owned conversation guard and new sender admission hook. Assess existing ordinary send/chain/skip paths for compatibility; no new run, checkpoint or permission interpretation. |
| C3 / DEL-07-02 | New private request/result handler for exact base/question/attempt and bounded capture; no public callable implementation or registry entry exists yet. Keep cold read and future authored producer separate. |
| REC/RS / DEL-01-02 and DEL-04-03 | Original loss/no-resend and recorder/source/current-historical meanings; no human act or persistent live capability. |

Required source selections: Group A Host/native requests and catalog/adapter tool
availability; Root managed-delegation mechanism correspondence; ROLE fresh TASK
and live lineage issuer; EXEC/WR notice guard and P4 semantics; C3 exact handler/
request/result and budget; REC/RS current/historical evidence. These are genuine
missing interfaces, not proof supplied by this options document. Existing Host
capture-core work can remain separate and cannot mint TASK provenance by itself.
OD-01 stays ordinary Codex graph work, with no W1 writer or routine graph approval
UI. OD-02 R2 storage/retention remains separately proposed; no persistent task
queue or cold live authority is introduced. No native/supplier action, code,
accepted-contract edit, download, packaging change or new child is performed.
