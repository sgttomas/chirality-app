# Stock Codex hosting boundary (version-independent)
- Contribution: DEL-01-01/HOSTING-BOUNDARY-v0.1
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001 (boundary definition), OUT-002 (version-identity and plan/revision seam definition only; no pin, no generated types), OUT-003 (responsibility account, OI-008 *proposal*, local-provider requirement account, optional-reuse assessment), OUT-004 (recorded-exchange and upgrade method only); REQ-001…REQ-008; designed cases for VER-001…VER-007
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 eddd122cf8b6e2c1ce5933ddb82aa9ec8591baa138a20f439e171ce5d83c4773; `docs/ARCHITECTURE.md` §1 (priorities, M-2, M-4, M-6, M-7), §2, §3 (V4-ARC-01…05, "Properties the App must hold", reuse candidates, "Left to the implementation session"), §6, §7, §8; `docs/PRD.md` §2.1 (V4-APP-01…04), §4.3 (V4-EXE-01…04), §4.5 (V4-AUT-03/04), §4.7 (V4-REC-03), §5 (V4-CST-01/03/06), §6; `docs/EXAMINATION.md` §2 (V4-EXM-01…03), V4-EXM-11/12; current `_Decomposition/Open_Issues.csv` OI-008, OI-009, OI-012; `External_Dependencies.csv` DEP-005
- Consumed inputs: accepted basis only. DEL-01-02, DEL-01-03, DEL-01-04, DEL-01-05, DEL-01-06, DEL-02-04 and DEL-04-01 are referenced by accepted meaning (their ScopeOfWork.md at 6e18505e3), to be reconciled at V1. Root D-GOV-43 (`docs/governance_harness/_DECISIONS/D-GOV-43_codex_host_replatform.md`, its A2 supplement, and Root `AGENTS.md` "Execution and governance") is cited as governance context for the v3 App and checked against the v4 basis in §2; it is not itself v4 authority (V4-CST-04). Concept-run returns T7/T11 (`_Coordination/AgentRuns/V4-CONCEPT-20260925/tasks/`) and v3 code under `projects/chirality-runtime` / `projects/chirality-app-dev` are dated historical evidence only.
- Receivers: DEL-01-02 (OUT-001; REQ-001, REQ-003, REQ-004, REQ-005, REQ-007; TBD-002) via DEP-01-01-019; DEL-01-03 (OUT-001; REQ-001, REQ-004) via DEP-01-01-020; DEL-01-04 (native request/answer interaction) via DEP-01-01-021; DEL-01-05 (OUT-004; REQ-003, REQ-007, REQ-008) via DEP-01-01-022 and the opposite-direction DEP-01-01-024; DEL-01-06 (stock binary identity for packaging) via DEP-01-01-023; App implementation owner (OI-008 proposal, OI-012 pin); W11 pin spike brief. DEL-01-01 is not a CASE-002 member; receivers come from `Dependencies.csv`.

**Reading note.** Every element name in this file (for example *request
identity*, *generation*, *version identity record*) is a **semantic** name, not
a wire field, type, file or persistence choice. Supplier method or field names
appear only in §9 and §10 as *historically observed, to be confirmed at the
selected pin* evidence. No Codex version is selected here: 0.154.0 (v3 pin) and
0.157.1 / 0.156.1 (dated upstream reports) are evidence only (SOW-135; OI-012
OPEN; owner decision D4 pending in `DECISIONS_PENDING.md`).

---

## 1. What this boundary is

The App's main process owns one stock, unmodified Codex App Server child
process and speaks its published JSON-RPC protocol over the child's standard
input and output (V4-ARC-01, SOW-118). The boundary is the single place where:

1. the supplier binary is identified and verified before it is trusted as the
   pinned supplier (SOW-099, SOW-128, SOW-135);
2. the child is started, handshaken, observed, restarted and deliberately
   stopped (§4);
3. protocol frames are exchanged, correlated and delivered in native form to
   receivers (§5; V4-ARC-05, V4-APP-04, M-2);
4. every server-initiated request is registered and answered, explicitly
   declined or explicitly errored (§6; V4-EXE-02, ARC §3 properties);
5. generated protocol types and the small experimental supplement are bound to
   the pin they were generated from (§7; SOW-121).

It is **not** the place where durable recovery, request cards, plan views,
account flows, packaging, workflow semantics, guidance composition, operation
policy or human acts are produced (§11; REQ-007, REQ-008).

```text
  Interface (webview; React+Vite)            ── observes; composes; presents
        │  receiver interfaces (semantic; transport inside Tauri unselected)
  Main process (Rust; Tauri 2)                ── owns the boundary below
   ┌──────────────────────────────────────────────────────────────────────┐
   │ Supplier identity & verification (§7) → Child lifecycle (§4)         │
   │ Frame exchange & correlation (§5)      → Native delivery to receivers │
   │ Server-request register interface (§6) ← answers from DEL-01-04 path  │
   │ Recording tap for fixtures (§9)                                        │
   └──────────────────────────────────┬───────────────────────────────────┘
                                      │ published JSON-RPC over stdio
                              stock Codex App Server (pinned, unmodified)
```

The Rust/TypeScript division drawn above is the fixed invariant only (ARC §3
properties: process, protocol session and outstanding-request register in the
main process). Everything further is the OI-008 proposal in §12.

## 2. Governance context and its v4 standing

Root D-GOV-43 (v3 App, ruled 2026-09-11) and Root `AGENTS.md` state a stance
for the App: stock App Server owned by the App's host process, full published
protocol, every server request answered, no filtering of Codex notifications,
no veto of the user's Codex configuration, no pinning of approval or sandbox
policy, no patched supplier; the A2 supplement adds "unfamiliar notifications
inspectable, unfamiliar server requests answered explicitly without implying
approval". Checked against the v4 basis:

| D-GOV-43 element | v4 basis | Standing in this definition |
|---|---|---|
| Stock, unmodified, published interface | V4-CST-03, V4-ARC-01, M-2, M-4, SOW-099 | Settled; carried as invariant H1 |
| Host-process ownership of child/session/requests | ARC §3 properties, V4-EXE-01 | Settled; invariants H2, H3 |
| Every server request answered; unknown → explicit error | ARC §3 properties, V4-EXE-02, SOW-123 (DEL-01-02) | Settled; register rules R1–R3 |
| Native items, no translated vocabulary | V4-ARC-05, V4-APP-04, PRD §6, ARC §7 | Settled; invariant H6 |
| No notification filtering; unfamiliar notifications inspectable | Consistent with M-2 native pass-through; not stated as a v4 prohibition | Adopted here as a **definition choice** (H7), open to the App implementation owner to confirm; see UNRESOLVED U-07 |
| Approval/sandbox policy is the user's own choice per project/turn | V4-AUT-04 leaves classifier-mode treatment open (OQ-02/OI-002); D3 recommendation pending | `UNRESOLVED{OI-002}`: the boundary carries whatever setting a person actually chose and never decides it (H9) |
| Additive instruction inputs preserving Codex base instructions | Deliverable interface "PKG-02 supplies guidance/workflow inputs"; production is DEL-02-04 | Boundary carries them unchanged through supported inputs (§8 seam S-6) |

## 3. Invariants (hold in every state and every candidate)

- **H1 Stock supplier.** The child is the identified, unmodified stock binary.
  The App never patches, wraps with a modified binary, or injects code into it.
  Launch arguments and environment the App supplies are recorded as part of the
  configuration identity (§7) so that "unmodified" is inspectable (VER-001).
- **H2 Single owner of the pipe.** Only the main process writes to the child's
  input and reads its output. Interface processes never hold the pipe; losing
  or reloading a window never writes to, closes or signals the child
  (V4-EXE-01).
- **H3 Custody location.** The protocol session and the outstanding
  server-request register live in the main process for the child's lifetime
  (ARC §3). Durable custody across relaunch is DEL-01-02's (§6.5).
- **H4 Verified before ready.** No receiver is told the supplier is ready
  until version verification (§7) and the handshake (§4) have both succeeded
  for that child.
- **H5 Generation tagging.** Each child start receives a new *generation*.
  Every outbound request, inbound response, notification, server request and
  register entry carries its generation. Nothing from one generation settles,
  answers or is attributed to another.
- **H6 Native delivery.** Well-formed notifications, responses and server
  requests reach receivers with the supplier's own method, identifiers and
  payload unchanged, in received order. The boundary may add envelope
  metadata (generation, receipt position, classification) beside the native
  content, never in place of it.
- **H7 No silent loss.** The boundary does not use any supplier facility to
  suppress notifications (definition choice; U-07). Unfamiliar notifications
  are delivered, marked unfamiliar and inspectable. Malformed or oversize
  frames are counted **and** surfaced as an observable boundary condition with
  the generation and position; they are never silently discarded (v3 counted
  but did not surface them — §13 finding F-05).
- **H8 Silence never grants.** No timeout, silence, observer loss, reconnect,
  restart or process exit is ever turned into a grant or an affirmative answer
  (V4-EXE-02).
- **H9 Carries, does not decide.** Approval, sandbox, provider and account
  settings passed to the supplier are those a person actually chose through
  their owning interface (DEL-01-05; policy per DEL-04-01/04-02). The boundary
  defines none of them: `UNRESOLVED{OI-002}` for approval/sandbox treatment,
  `UNRESOLVED{OI-009}` for account home.
- **H10 Unknown stays unknown.** When a request to the supplier was written
  but its response was never observed (exit, timeout, write failure), its
  outcome is *unknown*, not failed and not succeeded (V4-EXE-03; ARC §3).

## 4. Child lifecycle

### 4.1 States (semantic)

| State | Meaning | Receivers may |
|---|---|---|
| `absent` | No child for this App run | Request start (person/App startup) |
| `verifying` | Supplier identity being checked (§7) | Observe |
| `refused` | Verification failed or was unverifiable; child not started as the pinned supplier | Read the reason; not send requests |
| `spawning` | Process being created with recorded arguments/environment | Observe |
| `handshaking` | Initialize exchange in progress | Observe |
| `ready` | Verified and handshaken; generation *g* active | Send requests; answer server requests |
| `exited-unexpectedly` | Child ended without a deliberate stop; generation *g* closed | Read exit facts; see §4.3 |
| `restart-waiting` | Waiting before the next start attempt | Observe; request deliberate stop |
| `halted-after-repeated-failure` | Restart bound reached; no further automatic start | Read failure history; request an explicit restart |
| `stopping` | Deliberate stop requested by a person (quit/stop) | Observe |
| `stopped` | Deliberately stopped; generation closed | Request start |

### 4.2 Operating sequence: start

1. **Resolve** the supplier binary the App candidate declares as its pinned
   supplier (location is a packaging concern, DEL-01-06).
2. **Verify** it (§7.2). Mismatch or unverifiable → `refused` with a reason;
   no child is started as the pinned supplier.
3. **Spawn** with the recorded argument/environment set (configuration
   identity). The account-home/environment element is
   `UNRESOLVED{OI-009}` (DEL-01-05 owns the choice's integration).
4. **Handshake**: send the supplier's initialize request carrying the App's
   client identity and whatever capability opt-ins the selected pin requires
   (whether an experimental opt-in is needed is a pin fact — §10 item P-06).
   Record the supplier's handshake response as part of the version identity
   record (§7.1). Handshake refused or timed out → the child is stopped, the
   generation is closed without becoming `ready`, and the failure counts
   toward the restart bound.
5. **Ready**: assign generation *g*, announce `ready(g)` with the version
   identity record to receivers.

### 4.3 Operating sequence: unexpected exit

On observing the child's exit (process end, closed output, or unrecoverable
pipe error) without a deliberate stop:

1. Close generation *g*; record exit facts (exit status/signal as observed,
   last receipt position, malformed-frame count, bounded redacted diagnostic
   output).
2. Every **client→supplier request** of *g* with no observed response gets
   outcome `unknown-no-response` (H10). Receivers decide what to show; the
   boundary never reports it as failed-and-not-applied.
3. Every **outstanding register entry** of *g* moves to
   `ended-unanswered(process-exit)` (§6.2). It is never answered afterwards
   and never recorded as granted or declined by a person.
4. Announce `exited-unexpectedly(g)` to receivers, including DEL-01-02, which
   owns recovery of actual thread/request state from the supplier after the
   next `ready` (V4-EXE-01, REQ-005 of DEL-01-02).
5. Enter `restart-waiting` unless the restart bound is reached, in which case
   enter `halted-after-repeated-failure`.

### 4.4 Restart rules

- Restart is automatic but **bounded**: a growing delay between attempts and
  a maximum number of failures within a window, after which the boundary halts
  and waits for an explicit person-initiated restart. Numeric values are
  implementation choices (U-05); v3 used 1–30 s backoff and 5 failures in
  180 s (`codex-app-server-client.ts`, historical evidence only).
- Every restart re-runs verification (§7.2); a binary changed on disk between
  generations is detected, not assumed.
- Restart never re-sends a prompt, re-answers an old request or replays a
  client request of a closed generation (D-GOV-43 A2 clarification 2 is
  consistent; V4-EXE-01).

### 4.5 Deliberate stop

A stop is an explicit act (person quits the App or chooses stop), distinct
from closing or hiding a window (V4-EXE-01, V4-EXM-11). Sequence: announce
`stopping`; outstanding register entries are either explicitly declined by
the App with origin `app-on-stop` or left to end with the process — which of
the two is a DEL-01-02 recovery decision (U-10); terminate the child politely,
then forcefully after a grace period (value unselected); record the stop as
deliberate with its actor; enter `stopped`. No unattended execution after
quit is promised.

## 5. Frame exchange and correlation

- **Framing.** The supplier's published framing over stdio (historically
  newline-delimited JSON; to be confirmed at pin, P-03). Diagnostic output on
  the supplier's error stream is captured, bounded, redacted and kept for
  diagnosis; it is never parsed as protocol.
- **Classification of each inbound frame:** response (correlates to one
  outstanding client request of the same generation), notification, server
  request (has an identity and expects an answer), or malformed. A response
  with no matching outstanding request is surfaced as an uncorrelated-response
  condition, not dropped.
- **Client requests.** Each outbound request records: generation, request
  identity, method, send position, write result (`written` / `write-failed`),
  and outcome (`response-observed(result|error)` / `unknown-no-response`).
  A client-side wait limit, if used, ends *waiting*, not the outcome: the
  outcome becomes `unknown-no-response`, never `failed` (H10; v3 converted a
  timeout into an engine-unavailable rejection — finding F-04).
- **Order.** Receivers get inbound frames in received order with a
  per-generation receipt position (semantic) that supports re-attachment
  without gaps or duplicates (replay buffer realization is DEL-01-02's, §6.5).

## 6. Outstanding server-request register — interface

### 6.1 Entry meaning (semantic elements)

| Element | Meaning |
|---|---|
| request identity | The supplier-assigned identity as received (opaque; any identity kind the protocol allows) |
| generation | Generation of the child that raised it |
| method | Supplier method as received |
| classification | `known-answerable` (App presents it for an answer), `known-app-unsupported` (a known kind the App does not serve; gets an explicit error or explicit decline per kind), `unfamiliar` (not in the pin's generated set or supplement) |
| subject references | Thread / turn / item / call references as the supplier provided them, unchanged |
| native parameters | The request payload unchanged |
| receipt position | Per-generation position (H5, §5) |
| state | See 6.2 |
| settlement | Native answer content or explicit error/decline content; **answer origin** (`person-via-interaction`, `app-rule:<named rule>`, `app-explicit-error`); the actor reference supplied by the answering interface |
| reply write result | `written` / `write-failed` / `not-attempted` |
| acknowledgment observation | `observed(<what>)` / `not-observed` / `not-observable-at-pin`. Writing a reply is not an acknowledgment (ARC §3; DEL-01-02 REQ-004) |

### 6.2 States

```text
received ─┬─(unfamiliar)──────────────► errored(explicit error written | write-failed)
          ├─(known-app-unsupported)───► errored / declined (explicit, per kind)
          └─(known-answerable)─► outstanding ─┬─ answer ─► settling ─► answered | declined
                                              │                    └─► settle-write-failed (outcome unknown)
                                              ├─ supplier-reported resolution ─► resolved-by-supplier
                                              └─ generation closed ─► ended-unanswered(process-exit)
```

`declined` covers an explicit negative answer by a person or an explicit App
rule; the origin element says which. `resolved-by-supplier` covers a supplier
notice that the request no longer needs an answer (for example the turn
ended or another client answered), if the selected pin provides one (P-09).

### 6.3 Rules

- **R1** Every inbound server request creates exactly one entry before any
  other handling, including when no window is open.
- **R2** `unfamiliar` requests receive an explicit protocol error immediately.
  They are never ignored, never answered affirmatively and never queued for a
  person as if known. (SOW-123; ARC §3.)
- **R3** `known-answerable` entries wait for an answer. No timeout, observer
  loss or reconnect produces an answer. Whether any automatic *decline* after
  a period is ever wanted is not defined here (U-11); if adopted it must be a
  named App rule recorded as origin `app-rule`, never as a person's answer.
- **R4** An entry is settled at most once. A second answer is refused with
  reason `already-settled`; an answer for a closed generation is refused with
  reason `generation-closed`; an answer for an unknown identity is refused
  with reason `no-such-request`.
- **R5** The answer content must be a valid answer for that method under the
  pin's generated types plus supplement; an invalid answer is refused with
  reason `invalid-answer` and the entry stays outstanding.
- **R6** A known request with no current observer is still `outstanding`; the
  boundary does not refuse it for lack of a window or live view (contrast v3,
  finding F-02).
- **R7** Origin is truthful. The register never records an App rule's answer
  as a person's act, and a person's answer is recorded with the actor the
  answering interface (DEL-01-04) supplies; the boundary does not infer it.
  Which answers an autonomy policy may give automatically is
  `UNRESOLVED{OI-001}` / `UNRESOLVED{OI-002}` (DEL-04-01/04-02); until then
  no automatic affirmative rule exists in this definition.
- **R8** The supplier's approval decisions (for example accept-once,
  accept-for-session, decline, cancel as historically observed) are native
  answer content. The boundary does not collapse them, and an answer of any
  kind is tool-execution permission within the supplier; it is not proposal
  acceptance, checking, approval in the engineering sense or reliance
  (V4-AUT-03, V4-AUT-04).

### 6.4 Register operations offered to receivers (semantic)

| Operation | Caller | Result |
|---|---|---|
| observe entries (current + changes, from a position) | DEL-01-02, DEL-01-04 | Entries and state changes in order |
| list outstanding (by generation / thread) | DEL-01-02, DEL-01-04 | Current outstanding entries |
| answer (request identity, native answer, origin, actor ref) | DEL-01-04 (person path); named App rules | `accepted-for-write` → later `answered`/`declined`/`settle-write-failed`; or refusal with reason (R4/R5) |
| explicit error (request identity, reason) | boundary (R2), named App rules | `errored` |
| read settlement and acknowledgment observation | DEL-01-02, DEL-04-03 evidence handoff via DEL-01-02 | Settlement, write result, acknowledgment observation |

### 6.5 Split with DEL-01-02 (to reconcile at V1)

DEL-01-01 defines entry meaning, classification, R1–R8, the answer write path
and generation tagging, and witnesses the unknown-request path at the
protocol seam (VER-001). DEL-01-02 owns custody behavior across observation
loss, reconnect and relaunch, recovery of outstanding requests from supplier
state after restart, the register's representation and persistence
(DEL-01-02 TBD-002), stop-time handling (U-10) and the settlement fixtures.
Both SoWs name the unknown-request error (DEL-01-01 REQ-001/AC-001;
DEL-01-02 OUT-001/REQ-004): see finding F-01.

## 7. Supplier version identity and verification

### 7.1 Version identity record (semantic)

| Element | Source |
|---|---|
| declared pin | The App candidate's pin record (selected by the App implementation owner; OI-012) |
| observed version label | The binary's own version report |
| binary content identity | Content identity of the resolved binary (algorithm unselected; recorded with the value) |
| expected binary content identity | Recorded when the pin was qualified |
| handshake-reported identity | Whatever identity the supplier returns in the handshake (P-05) |
| generated-schema identity | Pin + generator identity + output content identity from which the App's types were generated |
| supplement identity | Content identity and version of the hand-kept experimental supplement |
| configuration identity | Launch arguments and environment elements supplied by the App (H1) |
| verification result | `verified` / `mismatch(<element>)` / `unverifiable(<reason>)`, with time and generation |

### 7.2 Verification rule

Verified means: observed version label equals the declared pin **and** the
binary content identity equals the expected identity **and** the
generated-schema identity names the same pin. A version label alone is not
sufficient (AC-006: "rather than assuming an upgrade from a version label";
v3 compared only the label — F-06). The handshake-reported identity, where
the pin provides one, must not contradict the declared pin. Mismatch or
unverifiable → `refused`. Whether a person may deliberately run an
unverified binary for development, and how that run is labeled, is U-06; it
is never labeled as the pinned supplier.

### 7.3 Types and supplement binding (SOW-121, REQ-002)

- Protocol types are generated from the selected pin by the supplier's own
  generator and carry generated-schema identity. They are not edited by hand.
- Fields the App needs that the generator omits (historically experimental
  ones, e.g. plan collaboration settings at 0.154 per T11) live in one small,
  separately identified supplement, each entry naming the pin at which it was
  observed and the recorded exchange that evidences it.
- The main process needs, at minimum, the set of server-request methods and
  their answer validity rules (for R2/R5 classification). The payload types
  for composition and presentation serve the interface. How much of the type
  set the Rust side carries is part of OI-008 (§12).

## 8. Seams to receivers

| Seam | Receiver | Supplied by this boundary | Not supplied here |
|---|---|---|---|
| S-1 lifecycle and register | DEL-01-02 | §4 states and transitions with generation; `unknown-no-response`; register interface §6; exit facts; receipt positions | Durable custody, reconnect/relaunch strategy, persistence, recovery reads, settlement fixtures |
| S-2 version identity + plan/revision | DEL-01-03 | Version identity record (§7.1) with each `ready(g)`; native plan items and plan-update notifications, unchanged, with generation and receipt position; the generic client-request path for native plan-revision interactions using generated types + supplement | Plan registry, revision numbering, storage, export, plan UI, checker implementation (SOW-128: registry/checker remain choices) |
| S-3 request answering | DEL-01-04 | Register observe/list/answer operations; refusal reasons; settlement results | Request cards, answer UX, attachments, outcome presentation |
| S-4 embedding and provider | DEL-01-05 | Carriage of supplier account methods and per-conversation provider selection through the generic request path; local-provider requirement account (§8.1); recorded-exchange evidence per §9 | Sign-in/API-key flows, account home, provider configuration UI, server-substitution checks and evidence |
| S-5 binary identity | DEL-01-06 | The pinned binary's expected content identity and version label for the packaged-candidate check | Packaging, signing, entitlements, notarisation, distribution |
| S-6 additive guidance | DEL-02-04 (and DEL-02-01/02-02 inputs) | Carriage of instruction/role inputs through the supplier's supported additive inputs, unchanged, with configuration identity recorded | Guidance composition, role files, workflow semantics, idle-boundary change policy |
| S-7 evidence | DEL-04-03 (through DEL-01-02's handoff) | Observed facts: version identity, generation, settlement with origin, unknown outcomes | Record format, writer/reader, any human act |

### 8.1 Local-provider requirement account (REQ-005, AC-005; to DEL-01-05)

| Requirement | Published / basis claim (dated) | To be observed on the identified candidate |
|---|---|---|
| L-1 Local servers act as Codex model providers chosen per conversation | V4-ARC-04 (per-conversation provider on thread start); T7 (vendor/third-party docs, 2026-09-25): local models via provider configuration or an open-source-model switch | Per-thread provider selection exists at pin; its effect is confined to that conversation; switching back and forth (V4-EXM-12) |
| L-2 Wire interface Codex requires from a provider | ARC §6: "oMLX also serves the Responses API Codex requires" | Which interface(s) the pinned Codex accepts for a configured local provider; behavior when the server offers only Chat Completions |
| L-3 Tool calling through the provider | ARC §6, §8 risk (local tool calling unreliable) | Observed tool-call round trip with the configured server; malformed tool-call behavior surfaces as supplier items/errors, not as App-invented success |
| L-4 Local-operation boundary (priority 3) | ARC §1 priority 3 | Whether the supplier makes any network request other than to the configured provider while a local provider is selected (update checks, telemetry, remote features); recorded as observed, not assumed |
| L-5 Credentials | V4-ARC-04: credentials held by Codex | Local provider needs no key or a supplier-held key; no key passes through the interface |
| L-6 Distinct from host loop interface | ARC §4 V4-ARC-10 (host: Chat Completions with tool calls) | One server may satisfy the App's provider interface, the host's, both or neither; each is qualified separately (DEL-01-05 REQ-008 → DEL-05-01) |

An unqualified server example establishes neither supported substitution nor
provider access (REQ-005). Everything in the right column is `not observed`
at v0.1.

## 9. Recorded-exchange fixture method (M-7, V4-EXM-02, REQ-006)

### 9.1 Capture

A recording tap at the main-process stdio boundary records, for one
controlled scenario on an identified candidate:

- each frame in both directions, unchanged, with direction, generation,
  receipt/send position and a relative time offset;
- capture metadata: version identity record (§7.1), App candidate identity,
  scenario name, provider kind, the approval/sandbox settings actually in
  effect (as chosen by the person, H9), date (V4-EXM-01);
- a redaction record: credentials, tokens, account identifiers and personal
  paths replaced by labeled placeholders. A redacted fixture never claims
  byte identity with the original exchange;
- invented engineering material only (V4-CST-06); fixture subjects are labeled.

Live capture runs are few and deliberate; each needs the owner's own
credential or a local provider and is itself a recorded act.

### 9.2 Fixture standing labels

`recorded` (real exchange, redacted), `recorded-truncated` (real prefix, e.g.
up to a process kill), `mutated` (real exchange with a declared edit, e.g. an
injected unfamiliar request), `constructed` (hand-built, e.g. malformed
frames). The unknown-request and malformed-frame cases are necessarily
`mutated`/`constructed`; they are labeled so and never presented as observed
supplier behavior.

### 9.3 Replay and comparison

- **Supplier-double replay** exercises the App seam: the double emits
  recorded supplier→App frames and checks App→supplier frames against the
  recording by semantic comparison (identities correlated by position;
  declared volatile elements — times, generated identities — excluded).
- **Schema conformance**: every recorded frame is validated against the
  generated types + supplement of the pin it was recorded on.
- **Outcome labels** per case: `pass`, `fail`, `blocked`, `not-run`,
  `inconclusive`, bound to candidate + pin (V4-EXM-03).

### 9.4 Seam regression set (designed)

| ID | Scenario | Standing of fixture |
|---|---|---|
| X-01 | Verify → spawn → handshake → `ready` | recorded |
| X-02 | Conversation start with a selected provider; one turn | recorded |
| X-03 | Plan created, then revised in a later turn | recorded |
| X-04 | Command/file approval request answered affirmatively by a person | recorded |
| X-05 | Same kind of request explicitly declined | recorded |
| X-06 | User-input / elicitation request answered | recorded |
| X-07 | Unfamiliar server request | mutated |
| X-08 | Malformed and oversize frames | constructed |
| X-09 | Child killed with one outstanding request and one un-responded client request | recorded-truncated |
| X-10 | Restart after X-09; recovery read of actual state (DEL-01-02 consumes) | recorded |
| X-11 | Version label matches, content identity differs | constructed |
| X-12 | Answer for a closed generation; second answer to settled entry | constructed |

### 9.5 Deliberate-upgrade comparison procedure (SOW-100, REQ-006, VER-006)

1. Name the current qualified pin *p* and the candidate pin *p′*; nothing is
   adopted by running this procedure.
2. Obtain *p′* from its published distribution; record its version identity
   (§7.1).
3. Generate types at *p′*; record generator identity and output identity.
4. Structural diff of generated output *p* → *p′*: methods, server-request
   kinds, notifications and fields added / removed / changed. Mark each change
   against the consumer map (§8 seams) as `consumed` or `not consumed`.
5. Re-examine the supplement: entries now generated → remove; entries whose
   underlying field vanished or changed → incompatibility.
6. Validate the *p* recordings against *p′* types; record expected and
   unexpected conformance failures.
7. Capture the §9.4 set at *p′* (live runs limited to those needed).
8. Semantic diff of *p* vs *p′* recordings; run App seam replay on *p′*
   recordings with the candidate App.
9. Run the selected-version check (§7.2) on the candidate.
10. Record: *p*, *p′*, candidate, every result and every unresolved
    incompatibility. The App implementation owner decides adoption; *p*
    stays in force until then.

## 10. Pin spike observation list (for briefing W11)

W11 is BLOCKED on owner decision D4 (OI-012). Items below are what a spike
must **observe and record** at the selected pin; historical names are given
only to help find the item and must not be assumed.

**10.1 Distribution and identity**
- P-01 Published package/distribution and platform binary actually used
  (macOS Apple Silicon, V4-CST-02); version label text of the binary's own
  version report; binary content identity (record the algorithm used);
  licence file; size; signing state of the vendor binary as found (for
  DEL-01-06, observed only).
- P-02 Whether the binary runs standalone without extra packaged assets (a
  v3-era 0.149 probe of the generators failed with exit 2 for missing wrapper
  assets — T11, historical).

**10.2 Generation**
- P-03 Generator subcommands present at the pin (historically
  `app-server generate-ts` and `generate-json-schema`, T7/T11), their help
  text, flags (including any flag that includes experimental fields), exit
  status, output tree, and determinism (generate twice, compare identities).
- P-04 Generated inventory: client→server methods, server→client request
  methods, notifications; which are marked experimental; compare to the
  historical v3 usage (16 client methods; approval, user-input, elicitation,
  dynamic-tool, auth-refresh and attestation requests — T11/v3 code) as a
  comparison aid only.

**10.3 Handshake and transport**
- P-05 Handshake request/response: required client identity and capability
  elements; whether an experimental opt-in exists and what it enables;
  identity elements returned (historically user agent, home, platform);
  whether a post-handshake notice is required.
- P-06 Which App-needed features require the experimental opt-in (plan
  collaboration settings were experimental and absent from the exported
  schema at 0.154 — T11, D-GOV-43 proposal, historical).
- P-07 Framing, error-stream behavior, behavior when input closes, response
  to termination signals, and whether the supplier offers a notification
  opt-out facility (record presence; not to be used — H7).

**10.4 Requests, plans, providers**
- P-08 For each server-request kind: valid answer forms (affirmative,
  session-scoped, decline, cancel), what the supplier does with a JSON-RPC
  error reply to a known kind, and what it does if never answered (observe
  with a constructed double where a live run is unnecessary).
- P-09 Whether the supplier reports that a request was resolved/withdrawn
  (supports `resolved-by-supplier` and acknowledgment observation, §6.1).
- P-10 Plan items and plan-update notifications: identities, revision
  information carried natively, and how a plan revision is requested.
- P-11 Per-conversation provider selection element (historically named on
  thread start in ARC V4-ARC-04), provider configuration form, required wire
  interface for custom providers (L-2), built-in local-provider kinds.
- P-12 Account methods present (ChatGPT sign-in, API-key login — feeds
  OI-010 at DEL-01-05) and where credentials are stored.
- P-13 Thread resume/read/list methods and what they return after a child
  restart (feeds DEL-01-02); subagent/delegation item shapes (feeds
  DEL-01-03).
- P-14 Configuration and home directories read or written at start
  (feeds OI-009 at DEL-01-05).
- P-15 Additive instruction inputs the pin supports and whether they apply to
  a resumed conversation (v3 recorded that 0.154 ignored hot-resume overrides
  — T11, historical; feeds DEL-02-04).

**10.5 Spike outputs** — generated output with identities; an
observed-facts table (item, observed value, evidence file, standing
`observed`/`published-only`/`not-observed`); the supplement's initial entries
with evidence; at least X-01 recorded if a live start is authorized; no
adoption claim.

## 11. Owner / act boundary (REQ-007, REQ-008, AC-007, VER-007)

| Act | Owner | This boundary's contribution | Not performed here |
|---|---|---|---|
| Select the supplier pin | App implementation owner (OI-012; owner visibility D4) | §7 record form, §10 observation list, §9.5 upgrade method | Selection |
| Decide Rust/TS allocation | App implementation owner (OI-008) | §12 proposal | Decision |
| Durable session/request custody, reconnect, relaunch, stop | DEL-01-02 | §4, §6 interface, S-1 | Custody code, persistence, recovery |
| Plan/tool/delegation presentation | DEL-01-03 | S-2 | Views, registry, checker |
| Request cards, answers, outcomes, attachments | DEL-01-04 | S-3 register operations | Cards, answer UX |
| Sign-in, API key, local provider, substitution checks | DEL-01-05 | S-4, §8.1 account | Flows, configuration, substitution evidence |
| Packaging, signing, notarisation, distribution | DEL-01-06 (terms obtained by owner, OQ-08) | S-5 identity | Packaging production |
| Workflow semantics / making / registration | DEL-02-01 / DEL-02-02 | S-6 carriage | Semantics, registration |
| Additive guidance production | DEL-02-04 | S-6 carriage | Composition |
| Operation-policy / human-act definition | DEL-04-01 (unresolved classes: owner with host policy owner) | R7/R8 origin truthfulness | Policy, classes (`UNRESOLVED{OI-001}`, `UNRESOLVED{OI-002}`) |
| Run/act records | DEL-04-03 | S-7 observed facts | Records |
| Answer an approval request as a person | The person | Register accepts and records it with supplied actor | Performing or inferring it |
| Proposal acceptance, checking, engineering approval, professional reliance | The person / accountable professional | None; a supplier approval answer is not any of these (R8) | All |
| Supplier engine, credentials, published protocol | OpenAI Codex (DEP-005) | Consumes as published | Any modification |

No act in this table is a prerequisite for another unless its owner's own
contract says so; no universal acceptance-before-checking or
acceptance-before-reliance sequence is implied.

## 12. PROPOSAL for OI-008 — Rust/TypeScript division

**Label: proposal by the DEL-01-01 drafting task for the App implementation
owner, who decides (OI-008, SOW-131, REQ-004). Nothing here is selected.**
Evaluation order: maintainability, then functionality, then local
models/privacy (V4-CST-01, AX-001); few mainstream stacks, no
release-candidate frameworks (M-6, SOW-101).

| Option | Main process (Rust) | Interface (TypeScript) | Assessment |
|---|---|---|---|
| **O-1 Rust envelope core** | Verification, spawn, lifecycle, framing, correlation, generation tagging, register (§6) with R1–R8, unfamiliar-request errors, recording tap. Payloads handled as opaque native values except envelope elements and the server-request method/answer-validity set needed for R2/R5 | Composes typed requests with generated TS types + supplement through one generic request path; presents native items; submits answers through the register operations | One generated type set in the language that consumes payloads; Rust stays small and payload-agnostic, so supplier schema drift mostly lands in TS (maintainability); invariants H2/H3 hold because custody is in Rust. Needs a generated method/answer-validity list on the Rust side. **Recommended.** |
| O-2 Rust fully typed | As O-1 plus typed payloads (types generated from the supplier's schema output), thread/turn orchestration and composition in Rust | Presentation only | Two generated type sets or TS types derived from Rust; more Rust code touched on every schema change; stronger compile-time checking in main |
| O-3 Rust pipe relay, TS protocol client | Spawn and byte relay only | JSON-RPC client, correlation and register in the webview | **Violates** ARC §3: register and session would not survive window reload (V4-EXE-01). Set aside |
| O-4 Node helper in main process | Rust spawns a Node process that runs ported v3 client code | Presentation | Adds a runtime and a process, resembles the excluded v3 service (V4-ARC-03, M-6). Set aside |

**Why O-1:** it keeps every fixed invariant in the main process, keeps the
Rust surface to process/envelope concerns that change rarely, puts
schema-dependent code where the generated TS types already are, and lets the
v3 client *behaviour* (not code) be re-expressed in Rust at small size (v3's
client was ~330 lines, T11). **Open within O-1:** where thread/turn
orchestration and guidance carriage live beyond the generic request path;
which interface-side component re-attaches after reload (DEL-01-02); how
Rust obtains the method/answer-validity list at build time. These are
implementation choices for the App implementation owner and DEL-01-02.

**Optional-reuse assessment (REQ-004, AC-004, ARC §3 reuse candidates).**
v3 code is evidence of behavior, not qualified v4 material.

| v3 source (historical) | Reuse as | Receiving-contract gaps to close |
|---|---|---|
| `chirality-runtime/packages/daemon/src/codex-app-server-client.ts` (host, restart, answer-always) | Behavior specification for O-1 Rust port | F-02…F-05 below; generation tagging kept; timeouts → unknown |
| `codex-supervisor.ts` server-request routing and answer/cancel shapes | Behavior reference for R2/R8 and P-08 | Shapes are 0.154-era; re-derive from generated types; F-02 |
| `app-owned-composition.ts` version assertion; `chirality-app-dev/frontend/scripts/verify-codex-pin.mjs` | Behavior reference for §7.2 | Label-only comparison (F-06) |
| `chirality-runtime/packages/core/src/native-plan-registry.ts` | DEL-01-03's decision (registry remains a choice) | Tied to v3 contracts vocabulary and admission model |
| Translation into Chirality event names; socket/daemon; Next routes | Not selected (ARC §3, §7) | — |

## 13. Findings

- **F-01 Overlap on the unknown-request error.** DEL-01-01 (REQ-001, AC-001,
  VER-001) and DEL-01-02 (OUT-001, REQ-004) both name it. Proposed reading:
  DEL-01-01 supplies classification and the explicit-error path and witnesses
  it at the seam; DEL-01-02 owns custody code that invokes it and its
  settlement/acknowledgment fixture. Needs V1 reconciliation; no scope change.
- **F-02 v3 conflated "no live turn" with "unknown".** v3 answered a known
  approval/input request with a method-not-found error when no supervisor
  turn matched (`codex-supervisor.ts` `handleServerRequest`). Under R6 a
  known request stays outstanding; reuse must not carry this over.
- **F-03 v3 swallowed reply write failures** (`answerServerRequest …
  .catch(() => undefined)`), so a failed write looked settled. v4 records
  `settle-write-failed` / unknown.
- **F-04 v3 turned client-request timeouts into engine-unavailable
  rejections.** For a mutating request that is an unknown outcome (H10).
- **F-05 v3 dropped malformed and oversize frames after counting them** and
  cleared the buffer above 64 MB silently. v4 surfaces them (H7).
- **F-06 v3 version check compared the version label only.** AC-006 and
  VER-001 need stock binary identity; §7.2 adds content identity.
- **F-07 Receivers.** The common brief asks for receivers "from CASE-002";
  DEL-01-01 is not a CASE-002 member. Receivers are taken from
  `Dependencies.csv` DEP-01-01-019…024.
- **F-08 Wire names in the accepted basis.** V4-ARC-04 names a supplier
  field on thread start. This definition treats it as dated evidence to be
  confirmed at the pin (P-11), not a selected representation.
- **F-09 D-GOV-43 vs v4 basis.** "No notification filtering" and "approval
  and sandbox policy are the user's choice" are Root/v3 governance; the v4
  basis supports the first by M-2 but does not state it, and leaves the
  second open under OI-002 (V4-AUT-04; D3 pending). Recorded as U-07 and
  `UNRESOLVED{OI-002}` rather than adopted.
- **F-10 Acknowledgment observability is pin-dependent.** DEL-01-02 REQ-004
  requires distinguishing reply writing from observed acknowledgment; whether
  the supplier emits anything observable (P-09) is unknown until the spike.
- **F-11 No gap found** in the SoW's obligations for this definition; all
  REQ-001…REQ-008 are served at definition level, and every code/test
  artifact remains to be produced after OI-012.

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| U-01 `UNRESOLVED{OI-012}` supplier pin (D4 pending) | App implementation owner (owner visibility) | Before protocol generation and qualification | No pin, types, supplement entries or fixtures; §10 lists what to observe |
| U-02 `UNRESOLVED{OI-008}` Rust/TS division | App implementation owner | Before architecture production contracts | §12 is a proposal only |
| U-03 `UNRESOLVED{OI-009}` account home (environment passed to child) | Owner with App implementation owner (DEL-01-05) | Before account integration | Configuration-identity element left open (§4.2 step 3) |
| U-04 `UNRESOLVED{OI-002}` approval/sandbox/classifier treatment | Owner with App/host design owners | Before permission contract | H9: carried, not decided; no automatic affirmative answer rule |
| U-05 Restart bound values and grace period | App implementation owner with DEL-01-02 | Before implementation | Rules defined; numbers open |
| U-06 Running an unverified binary for development, and its label | App implementation owner | Before implementation | Default: refused as pinned supplier |
| U-07 Use of any supplier notification opt-out | App implementation owner | Before implementation | Definition uses none (H7) |
| U-08 Content-identity algorithm for binary/schema/supplement | App implementation owner (with DEL-04-03 for records) | Before qualification records | Recorded with value; unselected |
| U-09 Acknowledgment observation mechanism | DEL-01-02 with this deliverable, after P-09 | Before settlement fixtures | Element defined; values pin-dependent |
| U-10 Stop-time handling of outstanding entries (explicit App decline vs end with process) | DEL-01-02 | Before recovery implementation | Both paths defined with truthful origin |
| U-11 Any automatic decline after a period | App implementation owner with DEL-01-02; policy owners if act-bearing (`UNRESOLVED{OI-001}`) | Before implementation | Not defined; never affirmative |
| U-12 Whether more than one concurrent supplier child is ever needed | App implementation owner | Before implementation | Definition assumes one active child (ARC §2) |
| U-13 Redaction policy details for fixtures | App implementation owner | Before first capture | Categories listed in §9.1 |
| U-14 DEL-01-01/DEL-01-02 unknown-request split (F-01) | Both owners at V1 | V1 comparison | Proposed reading in §6.5 |

## Verification cases

Designed, not run. None has been executed; no candidate or pin exists.

| Case | Setup | Action | Expected result | Serves |
|---|---|---|---|---|
| VC-01 Stock and unmodified | Identified candidate and pin | Inspect stack (Tauri 2/React/Vite), binary identity vs expected, launch configuration identity | Stack as V4-ARC-02; binary content identity equals recorded; no patch/wrapper; configuration recorded | VER-001 |
| VC-02 Pipe ownership | Candidate running, one turn active | Close and reopen the window | Child untouched (same generation), work continues, register unchanged | VER-001 (DEL-01-02 witnesses recovery) |
| VC-03 Unfamiliar request | X-07 (mutated) replay | Double sends a server request of an unfamiliar method | Entry created (R1), explicit protocol error written (R2), no affirmative answer, receivers see `unfamiliar` | VER-001 |
| VC-04 Malformed frames | X-08 (constructed) | Double emits malformed and oversize frames | Condition surfaced with generation/position; nothing dropped silently; session continues or fails explicitly | VER-001 |
| VC-05 Exit with outstanding work | X-09 (recorded-truncated) | Kill child with one outstanding request and one un-responded client request | Entry → `ended-unanswered(process-exit)`; client request → `unknown-no-response`; no grant; new generation on restart; old answers refused `generation-closed` | VER-001, VER-006 |
| VC-06 Restart bound | Constructed repeated start failures | Force failures past bound | `halted-after-repeated-failure`; explicit person restart required | VER-001 |
| VC-07 Generated provenance | Selected pin | Regenerate types; compare to committed output; inspect supplement | Identical output identity; supplement small, each entry with pin + evidence; no hand edits to generated types | VER-002 |
| VC-08 Native pass-through | X-02/X-03 replay | Compare delivered frames to recorded | Method, identifiers, payload unchanged; only envelope metadata added | VER-002 |
| VC-09 Version identity to plan receiver | X-01/X-03 | Trace `ready(g)` identity record and plan items/revision to DEL-01-03 seam | Identity record complete; plan items native, with generation/position; registry/checker left to DEL-01-03 | VER-003 |
| VC-10 Label-only mismatch | X-11 (constructed) | Same label, different content identity | `refused` with `mismatch(binary content identity)`; not labeled pinned | VER-003, VER-006 |
| VC-11 OI-008 account review | This file §12 and the owner's actual decision | Review against ARC §3 invariants, priority order, M-6 | Decision source recorded; while OI-008 open the allocation criterion is **not met** | VER-004 |
| VC-12 Local-provider account | §8.1 with P-11, L-1…L-6 observations | Compare published claims to candidate observations | Each row labeled observed / published-only / not-observed; no substitution or provider access claimed | VER-005 |
| VC-13 Upgrade comparison | Two identified pins | Run §9.5 | Diff, supplement changes, conformance, replay results and unresolved incompatibilities recorded; no adoption by procedure | VER-006 |
| VC-14 Settlement truthfulness | X-04/X-05/X-12 | Person answers, App rule errors, second answer | Origins recorded truthfully; second answer refused `already-settled`; write failure → `settle-write-failed`, not settled | VER-001, VER-007 |
| VC-15 Act boundary review | §11 table, candidate statements | One-for-one review against CLM-004…006 | Every excluded act resolves to its owner; a supplier approval answer is not presented as acceptance, checking, approval or reliance; no invented prerequisite sequence | VER-007 |
