# Minimal-loop and model receiving contract
- Contribution: DEL-05-01/LOOP-v0.1
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001, OUT-002, OUT-003, OUT-004; REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007; AC-001–AC-009; VER-001–VER-009 (all of DEL-05-01)
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 6fbbb580bdacb7f34b4df98a826519a28c087aff6e589ad27330ee556a83b568; P/docs/PRD.md §2.2 V4-HOST-01/02/03/04, §4.1 V4-WF-05, §4.5 V4-AUT-01/03/04/05, §4.7 V4-REC-03/04/05, §6, §9 OQ-02/OQ-11; P/docs/ARCHITECTURE.md §3 (V4-ARC-01/04), §4 (V4-ARC-10–14 and host-agent properties), §5 V4-ARC-20, §6; P/docs/HOST_INTEGRATION.md §1, V4-HI-02/04, V4-HI-10–12, V4-HI-20–25, V4-HI-30–33, V4-HI-40–42, §8.1 closing paragraph, V4-HI-70/71; P/docs/EXAMINATION.md V4-EXM-01–03, V4-EXM-20–23; DECISION_BRIEF.html (sha256 02d38cb1…4c420e8) d2, d3, d5; APP-V4-CLARIFICATION-20260927/DIRECTION.md; SCC-CASE-002 Case_Datasheet M1/M4 rows; Open_Issues OI-001/002/003/013/014/021; External_Dependencies DEP-001
- Consumed inputs: accepted basis only. DEL-03-01/C (catalog entry and read basis), DEL-03-02/P (proposal lifecycle and outcomes per V4-HI-23/25), DEL-02-01 (workflow declaration: checkpoints and required tools), DEL-02-03 (checkpoint hold and receiving behavior), DEL-04-01 (act and operation-policy distinctions), DEL-04-03 (record semantics) are referenced by accepted meaning only, to be reconciled at V1. DEL-05-02/PANEL-v0.1 (panel receiving needs) was co-drafted in this run by the same executor; its independent comparison belongs to V1. DEP-05-01-024 model-interface/protocol basis: UNKNOWN supplier, not supplied. DEP-001 host evidence: not received.
- Receivers: DEL-02-01 (OUT-001, OUT-003; REQ-002, REQ-005; VER-005) and DEL-05-02 (OUT-001, OUT-003; REQ-001, REQ-005; VER-001, VER-005) per CASE-002 M1/M4; external SWBPIPE owner via App-manager preparation and human file relay (CASE-002 M4; DEP-05-01-021); DEL-05-01 itself for OUT-003/VER-001–009 when host evidence arrives

## 0. How to read this definition

- **Semantic names only.** Names such as "call correlation identity",
  "argument text", "termination reason" or "catalog identity" are semantic
  element names. They are not wire fields, JSON/TS types or message names. No
  transport, protocol version, hash or canonicalization algorithm,
  persistence technology, thread/process placement or shared-component
  placement is selected here (OI-013, OI-014, DEL-03-01 TBD-003, DEL-03-02
  TBD-002).
- **Standing.** Every statement below is a proposed receiving requirement
  for review at V1. "Settled" marks a distinction already fixed by the
  accepted basis, with its citation. `UNRESOLVED{…}` marks unruled policy or
  an unsupplied input. It is never a permission, a default choice or a pass.
- **Fixture subjects.** Examples use an invented piping model (runs `R-101`
  and `R-102`, nodes `N-10`…`N-40`, supports `S-1`…). They are fixture
  subjects only. They do not select the first connected operation
  (`UNRESOLVED{OI-021}`), and the V4-EXM-20 supports/run example remains a
  proposed fixture (EXAMINATION §4 preamble).
- **Who builds what.** This contract states what the App/shared side needs
  to receive from a host loop and how that will be checked. It does not
  construct the SWBPIPE loop, native layer, parser, persistence or panel.
  Those belong to the external host owner (SoW CLM-001; HI §1; ARCH §4).

## 1. Position: host loop versus the App's Codex path

The host loop and the App's harness are two different model interfaces. They
must not be merged by this or any consuming contract (SoW REQ-002; ARCH §§3,
4, 6; PRD §6).

| Aspect | Chirality App (not this contract) | Host embedded loop (this contract) |
|---|---|---|
| Agent runtime | Stock Codex App Server, owned by the App process (V4-ARC-01) | Minimal Chirality agent loop in the host (V4-ARC-10) |
| Model interface | Codex's published protocol; Codex speaks to its providers (the Responses API for local providers, ARCH §6) | OpenAI-compatible Chat Completions with tool calls (V4-ARC-10) |
| Credentials | Held by Codex (V4-ARC-04) | Held by the host native layer, outside the interface script (V4-ARC-12) |
| Tools | Codex tools, plus the host catalog through an MCP server or CLI when the person enables it (V4-HI-50, DEL-03-03) | Host catalog operations offered as tools (V4-ARC-13) |
| Replaceability | Harness pinned and upgraded deliberately (V4-CST-03) | Loop replaceable behind the four-subject boundary in §2 (V4-ARC-14) |

Consequences:

1. A local server that serves both interfaces (ARCH §6 notes oMLX) does not
   join them. The App's provider selection and the host's model selection
   remain separate settings with separate owners.
2. Codex protocol types, generated from the App pin, are not the host loop's
   types. The host loop's detailed representation waits for DEP-05-01-024.
3. PRD §6 excludes a Chirality-owned loop for the App. At v4.0, then, the
   minimal loop has **host consumers only**. SWBPIPE is the only identified
   host; further hosts remain open (OQ-04 / OI-005). §10 uses this fact.
4. Pi is a possible later replacement behind the §2 boundary. It is not a
   current dependency (V4-ARC-14; ARCH §6).

## 2. The replaceable boundary: four subjects

The boundary is the set of meanings a loop implementation must accept and
produce. A replacement (Pi's libraries, another library or a rewrite)
conforms when it preserves these meanings. Matching code shape is not
required. For each subject, the table names the consumed meaning, what the
loop owes the boundary, and what the loop must never do.

### 2.1 Messages

| Semantic element | Meaning | Consumed from |
|---|---|---|
| Conversation identity | The conversation the message belongs to; stable across interface reloads while the conversation exists | Record meaning: DEL-04-03 (conversation reference in the run record, V4-HI-70) |
| Speaker kind | Person; agent; tool result; supplied guidance (workflow/role/host instructions) | This contract; guidance source from DEL-02-01 |
| Content | Text or structured content of the turn. For the agent, streamed increments plus a completed form | This contract |
| Run association | The workflow run, if any, and the workflow identity/version selected (V4-HI-70) | DEL-02-01 source identity; DEL-04-03 run record |
| Model configuration reference | Which model setting was in force when the turn was produced (§5); never contains a key | This contract; DEL-04-03 "model used" |
| Completion standing | Streaming, complete, truncated, interrupted, cancelled or failed | This contract |

Loop obligations:

- M-1. Preserve the order and speaker of every message it sends to or
  receives from the model.
- M-2. Distinguish a completed agent message from a streamed partial one. A
  partial message that ends without completion carries the standing
  truncated, interrupted or cancelled, never complete.
- M-3. Carry conversation content only as operational state. A harness or
  loop conversation store is never the authority for a human act (V4-REC-03,
  settled).
- M-4. Keep conversation persistence, its storage and its lifetime with the
  host owner (`UNRESOLVED{OI-013}`). The boundary requires only that the
  conversation identity can be cited by the run record and the panel.

### 2.2 Tools

| Semantic element | Meaning | Consumed from |
|---|---|---|
| Tool offering | One catalog operation offered to the model: operation identity and version, purpose text, argument schema, availability and unavailable reason, human-act class | DEL-03-01/C catalog entry (V4-HI-02); human-act class values `UNRESOLVED{OI-001}` via DEL-04-01 |
| Catalog identity | The identity/version of the adopted catalog from which the offerings were derived | DEL-03-01/C |
| Tool call | A request from the model to run one offered operation: call correlation identity, operation reference, argument text, parse state (§7) | This contract; representation per DEP-05-01-024 |
| Validated call | A tool call whose argument text parsed completely and conformed to the catalog argument schema of the named operation version, bound to that catalog identity | This contract (§6) |
| Tool result | What the loop returns to the model for a call. Either a failure reported by the loop (§6, §7), or the host's outcome with its standing and basis | Host outcome meaning: DEL-03-02/P (V4-HI-23/25); standing: DEL-03-01/C (V4-HI-12) |

Loop obligations:

- TL-1. Offer only operations derived from the adopted catalog. An operation
  unavailable to the person is unavailable to the agent, with the same
  reason (V4-HI-04, settled). The loop does not invent a tool that has no
  catalog entry.
- TL-2. Every tool result returned to the model states which it is: a
  loop-side failure (not sent to the host), a host refusal, or a host
  outcome. It must not collapse them into one "error" or "success".
- TL-3. A host outcome keeps its lifecycle meaning. "Success" means the
  operation ran. A submitted proposal reports "queued" until the host
  records acceptance and application (V4-HI-25, settled). The loop never
  rewrites queued as applied, or applied as accepted.
- TL-4. Reads return the basis they describe (workspace identity, generation,
  model revision, content identity) and their standing (V4-HI-11/12). The
  loop passes basis and standing through unchanged. A later call cites the
  basis it relied on (V4-HI-11, DEL-03-01/C).

### 2.3 Events

Events are the loop's observable account of what happened. The panel
(DEL-05-02) and the run record (DEL-04-03) consume them. Each event states
its **subject**, its **actor** and the **evidence** it rests on. An event is
evidence of what the loop observed. It is never itself a human act.

| Event meaning (semantic) | Subject | Actor | Evidence it may carry |
|---|---|---|---|
| Turn started / completed / cancelled | Conversation turn | Person (request) or agent | Message references |
| Model stream progress | Agent message | Model via loop | Partial content; no standing beyond "streaming" |
| Model request refused at boundary | Model request | Host native layer | Refused destination or missing key (§5), no key content |
| Model interface failure | Model request | Model server or transport | Termination reason as reported (§7) |
| Tool call received | Tool call | Model | Call correlation identity; operation reference; parse state |
| Tool call rejected (unparseable/truncated) | Tool call | Loop | Parse state and reason; "not dispatched" |
| Tool call rejected (schema) | Tool call | Loop | Catalog identity; schema failure description; "not dispatched" |
| Tool call dispatched to host | Validated call | Loop | Catalog identity; relied-on basis |
| Host outcome | Operation | Host | Outcome per DEL-03-02/P (ran, refused with reason, stale, queued, applied with receipt reference, outcome unknown) |
| Proposal queued | Proposal | Host | Proposal reference (DEL-03-02/P); not acceptance |
| Checkpoint reached / waiting for act | Declared checkpoint | Loop | Workflow checkpoint reference (DEL-02-01), required act kind (DEL-04-01) |
| Act requested | Act kind at a checkpoint or proposal | Agent (request only) | Request text; content it concerns |
| Human act observed | Actual act | Person (actor); host (recorder) | Host's record reference, bound content (V4-HI-32) |
| Act lapsed | Previously recorded act | Host | Changed content identity (V4-HI-32) |
| Run ended | Workflow run | Loop | Final state, including unknown outcomes that remain unknown |

Loop obligations:

- E-1. Emit an event only for something the loop actually observed or did.
  An absent observation stays absent. It is not filled by inference (V4-EXM-31
  analogue; SoW AC-009).
- E-2. The "human act observed" event relays a host-recorded act. The loop
  never originates it from model text, a tool success, a queue position or a
  receipt (V4-HI-25/31, V4-AUT-03, settled).
- E-3. Events carry references to host receipts, hashes and origin marks.
  They do not copy them (V4-HI-71, settled).
- E-4. The event set must be enough for the run record's inventory
  (V4-HI-70: workflow and version, conversation, autonomy settings,
  operations requested and outcomes, receipt references, human acts, model
  used). The field-level mapping is reconciled with DEL-04-03 at V1.

### 2.4 Checkpoints

A checkpoint is a point declared in a workflow at which the run waits for a
specified human act (V4-WF-05, V4-HI-42, settled).

| Semantic element | Meaning | Consumed from |
|---|---|---|
| Declared checkpoint | The workflow's declaration of the checkpoint and the act kind it requires | DEL-02-01 workflow declaration |
| Hold state | Waiting; satisfied by an identified act; lapsed; abandoned | DEL-02-03 checkpoint hold behavior |
| Required act kind | Named by DEL-04-01's accepted act names (e.g. accept an edit, mark checked, approve, rely) | DEL-04-01; which acts are always reserved is `UNRESOLVED{OI-001}` |
| Satisfying evidence | The host's record of the actual act, bound to content | DEL-04-03 act record; host recording (HI §1) |

Loop obligations:

- C-1. At a declared checkpoint the loop stops acting on the run and emits
  "checkpoint reached / waiting for act". A checkpoint overrides autonomy
  (V4-HI-42, settled). No autonomy grant lets the loop pass it.
- C-2. The loop resumes only on the host's evidence of the **specified**
  act. Model text, a tool success, an agent finding or an act of a
  different kind does not satisfy it (V4-WF-05; SoW REQ-007).
- C-3. The checkpoint requires its own act, and nothing more. This contract
  adds no general rule that acceptance must precede every checking,
  approval or reliance act (SoW REQ-007, AC-008).
- C-4. If the content an act concerns changes before the run resumes, the
  act lapses visibly (V4-HI-32). The hold returns to waiting, and the lapse
  is an event.

## 3. Operating sequence (one turn)

Semantic sequence; placement of each step (interface thread, worker, native
layer) is owner-selected (`UNRESOLVED{OI-013}`).

```text
person message ─► loop composes request (messages + tool offerings from catalog identity K)
   ─► native layer checks destination and attaches key if cloud (§5) ─► model server
   ◄─ streamed content and/or tool calls, then a termination reason
for each tool call:
   parse-completeness check (§7) ── fail ─► report failure; not dispatched
   operation resolution in catalog K ── unknown ─► report failure; not dispatched
   argument check against K's schema ── fail ─► report schema failure; not dispatched
   host validation and application route (V4-HI-20) ─► host outcome (P) ─► tool result
checkpoint declared at this step? ─► hold (§2.4) until the specified act is recorded
loop repeats until the model ends its turn, the person cancels, or a failure ends the turn
```

## 4. Minimal Chat Completions capability

The receiving contract needs these capabilities from the model interface.
They are stated semantically. The supplier, protocol version and payload
details are `UNRESOLVED{DEP-05-01-024}`.

| Capability | Why needed | Settled or open |
|---|---|---|
| Submit an ordered conversation and a set of tool offerings | Messages and tools subjects | Settled need (V4-ARC-10) |
| Receive assistant content incrementally | Responsiveness (§8) and panel conversation | Settled need (ARCH §4 streaming) |
| Receive tool calls with correlation identity, operation name and argument text, possibly in fragments | Tools subject; §7 assembly | Settled need; fragment representation open (DEP-05-01-024) |
| Receive a termination reason that tells complete apart from length-truncated and error | §7 truncation detection | Need settled; its representation open (DEP-05-01-024) |
| Return a tool result for a correlation identity | Tools subject | Settled need |
| Whether several tool calls in one response are supported, and how | §7 MC-8 | `UNRESOLVED{DEP-05-01-024}` |

No provider, server product, model or version is selected. The ARCH §6 list
(oMLX, LM Studio, Ollama) is a dated assumption. A candidate server needs the
selected interface/tool-call qualification (ARCH §6 "If it fails").

## 5. Model selection, destination and key boundary

### 5.1 Settings (semantic)

| Model setting state | Meaning |
|---|---|
| Local (default) | A user-controlled local model server is configured. This is the default (V4-HOST-01) |
| Cloud chosen, key supplied | The person chose a cloud model and supplied an API key (V4-HOST-01) |
| Cloud chosen, key absent | Chosen but no key supplied. No request may be made |
| Unconfigured | No usable model server. No request may be made. There is no silent cloud fallback |

Settled rules:

- N-1. Local is the default. Cloud is used only on the **person's** choice
  **and** a supplied key (V4-HOST-01, V4-ARC-11).
- N-2. In local operation, agent data goes to no destination other than the
  configured model server (V4-HOST-02).
- N-3. The loop's requests pass through the host's native layer. That layer
  enforces the configured endpoint and holds any key outside the interface
  script (V4-ARC-12).

Derived receiving requirements (proposed; review at V1):

- N-4. Model and endpoint settings change only by the person's act through
  the host. Model output, tool arguments and workflow text cannot change
  them. This follows from N-1: an agent-initiated change is not the person's
  choice.
- N-5. A failed or unreachable local server is reported. It is never
  answered by switching to a cloud model (N-1).
- N-6. The key never appears in interface script memory, in messages, events,
  run records, panel content or error text. Events that concern the key say
  only "key present" or "key absent".
- N-7. The native layer is the **enforcement point**. Interface-script
  checks can help, but they are not evidence of enforcement (SoW AC-002).

Open matters:

- `UNRESOLVED{N-OPEN-1}`: which endpoints count as a "user-controlled local
  model server" (same machine only, or a user-controlled machine on a local
  network). Owner: App/shared embedded-integration owner with the SWBPIPE
  owner; route to the owner if it touches V4-HOST-02's privacy meaning.
  Needed before endpoint-enforcement conformance cases can be finalized.
- `UNRESOLVED{N-OPEN-2}`: the permitted destination set in cloud-chosen
  operation. V4-HOST-02 is stated for local operation only. The proposed
  reading is "only the chosen cloud endpoint", but that is not settled.
  Same owners and point of need.
- `UNRESOLVED{N-OPEN-3}`: traffic caused by tools rather than the loop
  (e.g. a later Domains query tool). HI §8.1 says the Domains direction does
  not relax V4-HOST-02 or authorize an unselected destination. This contract
  covers loop traffic. Tool-caused traffic belongs to the tool's own
  receiving contract, and is recorded as an open interface, not a
  permission.

### 5.2 Case matrix (OUT-002 fixtures / OUT-003 conformance)

| Case | Setting / stimulus | Expected receiving result | Evidence type needed for a host claim |
|---|---|---|---|
| MS-01 | Local default; person asks for a model-table read | Requests go only to the configured local server; the loop's destinations match the configuration | Observed destinations for the candidate, with configuration (V4-EXM-01, V4-EXM-23) |
| MS-02 | Unconfigured | No model request; person told no model is configured; no cloud fallback | Observed absence of requests; interface observation |
| MS-03 | Person chooses cloud and supplies key | Requests go to the chosen cloud endpoint through the native layer; key never visible to script | Native-layer trace and script-side inspection |
| MS-04 | Cloud chosen, key absent | No request; failure reported | Observed absence of requests |
| MS-05 | Model output or tool argument asks the loop to use another endpoint | Refused (N-4); setting unchanged; event recorded | Setting before/after; event |
| MS-06 | Local operation; loop or library attempts a request to another destination (fixture: a hard-coded telemetry URL in a test double) | Refused by the native layer; reported; no data sent | Native-layer refusal observation plus network capture |
| MS-07 | Interface script attempts to read the key | Not available to the script | Script-side inspection of the candidate |
| MS-08 | Cloud request fails with an authentication error | Error reported without key content (N-6) | Error text, event and record inspection |
| MS-09 | Local server unreachable | Failure reported; no cloud switch (N-5) | Observed destinations; event |
| MS-10 | Person switches cloud → local mid-conversation | Later requests go only to the local server; the setting change is attributed to the person | Observed destinations before/after; setting-change record |
| MS-11 | Endpoint on another machine configured as "local" | `UNRESOLVED{N-OPEN-1}`: case held; no expected result asserted | — |

## 6. Validation order: catalog schema before host domain validation

Settled: tool arguments are checked against the adopted catalog schemas
before the host's own validation runs (V4-ARC-13; SOW-139). Every change,
by person or agent, then passes through the host's one validation and
application route (V4-HI-20).

Ordered steps for each tool call (semantic):

| Step | Check | Performed by | On failure |
|---|---|---|---|
| V-1 | Parse completeness (§7) | Loop | Report "not dispatched: malformed/truncated" |
| V-2 | Operation resolution: the operation reference names an operation offered from catalog identity K | Loop | Report "not dispatched: unknown or unoffered operation" |
| V-3 | Catalog argument schema of that operation version in K | Loop (against the adopted schema) | Report "not dispatched: schema failure", with the schema reason |
| V-4 | Host domain validation (availability, preconditions, basis currency, domain rules) | Host route | Host refusal with reason, e.g. unavailable or stale (DEL-03-02/P) |
| V-5 | Application or proposal per the person's autonomy and adopted policy | Host route | Host outcome per DEL-03-02/P |

Receiving requirements:

- O-1. V-3 always runs before V-4. A call that fails V-1 to V-3 never
  reaches V-4.
- O-2. Passing V-3 is not host acceptance, not application and not a human
  act (SoW REQ-003, CLM-004). A schema-valid call can still be refused at V-4.
- O-3. The catalog identity used at V-3 is the one from which the offering
  was made. Proposed: if the host's adopted catalog changed between offering
  and call, the call is reported as needing re-offer rather than validated
  against a different version. Reconcile with DEL-03-01/C versioning at V1.
- O-4. Where availability is checked (at offering, at V-4 or both) follows
  DEL-03-01/C and the host. This contract fixes only O-1 and the parity rule TL-1.

## 7. Malformed and truncated tool calls

Settled: truncated or malformed tool calls are reported failures. They are
never executed as empty arguments (ARCH §4; SOW-142).

| ID | Condition (semantic) | Expected handling |
|---|---|---|
| MC-1 | Termination reason says length/limit truncation while a tool call's argument text is incomplete | Failure "truncated"; not dispatched; reported to model, event and record |
| MC-2 | Stream interrupted (connection loss, server error) during argument text | Failure "interrupted"; not dispatched |
| MC-3 | Argument text complete but not parseable as a structured value | Failure "malformed"; not dispatched |
| MC-4 | Parses, but not the structured form an argument set requires (e.g. a bare string or list where a set of named arguments is expected) | Failure "malformed"; not dispatched |
| MC-5 | Operation reference missing, empty or not an offered operation | Failure at V-2; not dispatched |
| MC-6 | Argument text absent or empty | Never coerced to an empty argument set. Whether an interface can express an explicit "no arguments" for a zero-argument operation, and how, is `UNRESOLVED{DEP-05-01-024}`. Absent text is treated as malformed until then |
| MC-7 | Two calls in one response share a correlation identity | Failure for both; not dispatched (proposed; review at V1) |
| MC-8 | Several calls in one response, one malformed | The malformed one is not dispatched. Whether valid siblings run is `UNRESOLVED{T-OPEN-1}` (proposed: they may run, each on its own validation; review with DEL-03-02/P for proposal batches) |
| MC-9 | Loop "repairs" incomplete text (closes brackets, fills defaults) | Prohibited. A repaired text is not the model's call. The model may issue a new call, which is a new call with its own identity |

Failure reporting has three recipients, each distinct:

1. **The model**, as a tool result marked as a loop-side failure with the
   reason, so the conversation can continue (TL-2 in §2.2).
2. **The event stream / panel**, as "tool call rejected" with parse state and
   "not dispatched" (DEL-05-02 conversation interaction).
3. **The run record**, as an operation requested whose outcome is "not
   executed: rejected before host validation" (DEL-04-03 outcome meaning).

Dispatch observation. The receiving check for every rejected case is that
the host's validation/application route received no call for that
correlation identity. A valid comparison call (FX-V1 in §11) shows
dispatch does happen for legitimate input, so the check separates rejection
from a broken route (SoW AC-005).

## 8. Responsiveness: observation protocol (no numeric thresholds)

Settled: the loop does not block the host's interface. Long parsing and
model streaming run off the interface's main thread where the host needs
it (ARCH §4). Placement is the host owner's choice (`UNRESOLVED{OI-013}`).
This contract sets **no** latency or frame-time threshold (SoW REQ-004,
AC-006). Any quantitative criterion would need an owner decision
(`UNRESOLVED{R-OPEN-1}`).

Observation scenarios (designed, unexecuted):

| ID | Load | Concurrent person interaction to attempt |
|---|---|---|
| RS-1 | A long model stream (fixture: a long explanatory answer) | Scroll and select rows in a host table; open another host view; type in a host field |
| RS-2 | A tool call with large argument text and a large read result (fixture: all nodes of an invented 2,000-node model) | Same interactions, during parse and result handling |
| RS-3 | A stream in progress | Cancel the turn; confirm cancel takes effect and the interface stays usable |
| RS-4 | Stream in progress while the host runs its own work (fixture: a host-side recalculation) | Interact with host views that do not depend on that work |

Each observation records:

- The candidate identity (host build, loop implementation and version) and
  the configuration (model server, model, local or cloud), plus the date
  (V4-EXM-01).
- Environment: machine, OS and webview engine.
- The host owner's implementation choice for placement and parsing, as
  reported by that owner. This contract does not choose it.
- Each interaction attempted, and the observer's account: usable; usable
  with described degradation; blocked; or not observed.
- Any measurement the host already produces, reported as observed, with no
  pass threshold applied by this contract.
- Limitations, e.g. a single machine or a fixture model instead of a real
  model.

Verdict language: "continued usability observed for scenarios X on candidate
Y". A document review or a fixture run can never support "responsive" for an
actual host.

## 9. Distinct acts at the loop boundary

Settled distinctions (V4-HI-25/30–33, V4-AUT-03/05, V4-WF-05; d3 "Preserve the
meanings through the UI"):

| Subject | Actor | What the loop may emit | What the loop must never emit or infer |
|---|---|---|---|
| Execution (operation ran) | Host, on the agent's validated call | Host outcome "ran" with receipt reference if applied | Acceptance, checking, approval or reliance |
| Queued proposal | Host | "Queued" with proposal reference | "Applied" or "accepted" |
| Acceptance of a proposed edit | Person; recorded by host | Relayed "human act observed" (act kind: accept) | Acceptance from success, queueing or receipt |
| Application | Host | Outcome "applied" with receipt reference | Engineering approval |
| Agent check (findings) | Agent | Findings by reference to rows/results; non-mutating (V4-EXM-21) | "Checked" as a human act |
| Marking checked | Person; recorded by host | Relayed "human act observed" (act kind: mark checked) | Created by the agent or inferred from findings |
| Approval | Person | Relayed act only | Any agent statement of approval, certification or compliance (V4-AUT-05) |
| Professional reliance | Person (accountable professional) | Relayed act only, if the host records one | Reliance from any other act |

- A-1. Evidence of one act never establishes another (SoW CLM-004).
- A-2. An agent may request an act and prepare the person's decision. It
  never records the act as performed (V4-HI-31).
- A-3. When an agent or host acts as **recorder** of an act the person
  actually performed, the record keeps the actor (the person) distinct from
  the recorder (DEL-04-03 meaning; DEL-05-02 REQ-003).
- A-4. Which operations have always-reserved acts, and how classifier-based
  routine permissions are treated, are `UNRESOLVED{OI-001}` and
  `UNRESOLVED{OI-002}`. The loop carries whatever DEL-04-01 adopts. It holds
  no default of its own.

## 10. Owner-allocation and open-choice account (OUT-004)

### 10.1 Responsibility map

| Responsibility | App/shared (this DEL-05-01) | Other App-v4 owner | External host owner (SWBPIPE) | Open issue / point of need | Current standing |
|---|---|---|---|---|---|
| Loop receiving requirements, fixtures, conformance cases | Owns (OUT-001–003) | — | Receives through relay | — | This v0.1 draft |
| Loop construction | Excluded | — | Owns | OI-013 before shared/host implementation boundary contracts | Owner-reported building (DEP-001) |
| Loop placement (interface thread, worker, native) | Excluded; requires §8 outcome only | — | Selects | OI-013 | Open |
| Streaming and tool-call parsing implementation | Excluded; requires §7 outcomes only | — | Owns | OI-013 | Open |
| Conversation persistence | Excluded; requires citable identity (M-4) | Record reference meaning: DEL-04-03 | Owns | OI-013 | Open |
| Panel assembly | Excluded | Panel receiving: DEL-05-02 | Owns | OI-013 | Open |
| Native networking, endpoint enforcement, key custody | Excluded; defines §5 cases | — | Owns | N-OPEN-1/2 before conformance cases | Not received |
| Catalog schemas and read basis | Consumes | DEL-03-01 | Implements host catalog | DEL-03-01 TBD-003 | Referenced by meaning; V1 |
| Proposal/validation/outcome meaning | Consumes | DEL-03-02 | Implements route/receipts | DEL-03-02 TBD-002 | Referenced by meaning; V1 |
| Workflow/role/checkpoint declarations | Consumes | DEL-02-01 | Host workflows (V4-HOST-06) | OI-014 | Referenced by meaning; V1 |
| Checkpoint execution/hold behavior | Consumes | DEL-02-03 | Host execution | — | Referenced by meaning; V1 |
| Operation-policy and act distinctions | Consumes | DEL-04-01 (carries adopted policy) | Enforces adopted policy; offers/records acts | OI-001, OI-002 | Unruled |
| Record format and act records | Consumes | DEL-04-03 | Supplies receipts, actual acts | — | Referenced by meaning; V1 |
| Model-interface / protocol fixture basis | Receives or agrees at fixture use | — | Possibly (unknown) | DEP-05-01-024, supplier UNKNOWN | Not supplied |
| Actual host evidence | Receives, audits (VER-009) | Joined witness: DEL-09-06 | Supplies | DEP-001 | Not received |
| Common (shared) loop implementation | Not allocated | OI-014 owners | — | OI-014 / OI-013 | No agreed repeated responsibility |
| Human acts | None | — | Offers, records, presents | — | Performed by the person only |

### 10.2 Common-implementation assessment

A common implementation needs a concrete, agreed, repeated responsibility
(Clarification; V4-ARC-20; d2). The current facts:

- The App runs no Chirality loop (PRD §6). At v4.0 the minimal loop has one
  identified consumer, the SWBPIPE host. Additional hosts are open
  (OQ-04 / OI-005).
- Candidate repeated parts, for later OI-014 consideration only: (a) the
  parse-completeness check (§7); (b) catalog-schema argument checking (§6
  V-3). Part (b) might also serve the external adapter (DEL-03-03), whose
  arguments also need schema checking. That would be a second consumer,
  but it has not been compared.
- Assessment: **no repeated responsibility is established. No common loop
  implementation is proposed.** Candidate (b) goes to V1 as a question for
  DEL-03-01 and DEL-03-03, not as an allocation.

### 10.3 Required inputs and their standing

| Input | Supplier | Needed for | Standing at v0.1 |
|---|---|---|---|
| Catalog entry and read-basis meaning, catalog identity/versioning | DEL-03-01/C | §2.2, §6, fixtures | Referenced by accepted meaning; reconcile at V1 |
| Proposal lifecycle/outcome taxonomy | DEL-03-02/P | §2.2 TL-3, §2.3, §6 V-4/5, MC-8 | Referenced; V1 |
| Checkpoint declaration and required-tool meaning | DEL-02-01 | §2.4 | Referenced; V1 |
| Checkpoint hold behavior | DEL-02-03 | §2.4 | Referenced; not in Wave 1 (W7) |
| Act names and policy classes | DEL-04-01 | §2.4, §9 | Referenced; OI-001/002 open |
| Record inventory and act record | DEL-04-03 | §2.1, §2.3 E-4, §7 | Referenced; V1 |
| Panel receiving needs | DEL-05-02 | §2.3, §7 recipient 2 | DEL-05-02/PANEL-v0.1, same executor; independent V1 comparison needed |
| Model-interface identity and protocol/fixture representation | UNKNOWN (DEP-05-01-024) | §4, §7 MC-6/MC-8, all executable fixtures | Not supplied |
| Host candidate and observations | SWBPIPE (DEP-001) | VER-001/002/004/005/006/009 host claims | Not received; owner-reported building |

## 11. Fixture inventory (OUT-002, designed)

Every fixture names its **catalog basis** (a DEL-03-01/C version, currently
none supplied) and its **model-interface basis** (DEP-05-01-024, currently
UNKNOWN). Until both are supplied, fixtures are case designs. They cannot
be executed, and they carry no field names. Fixture operations are invented
subjects.

| Fixture | Subject (invented) | Input | Expected result | Serves |
|---|---|---|---|---|
| FX-V1 | Read run `R-101` supports | Complete, schema-valid call | Dispatched; host read with basis and standing | VER-004, VER-005 comparison |
| FX-V2 | Propose support `S-7` at node `N-30` on `R-101` | Complete, schema-valid call; autonomy = propose | Dispatched; host outcome "queued"; no acceptance event | VER-004, VER-008 |
| FX-S1 | Same operation, node given as a number where the schema requires a node reference | Schema-invalid | Rejected at V-3; not dispatched | VER-004 |
| FX-S2 | Required argument missing | Schema-invalid | Rejected at V-3 | VER-004 |
| FX-D1 | Support at node `N-99`, not on `R-101` | Schema-valid, domain-invalid | Passes V-3; host refuses at V-4 with reason | VER-004 |
| FX-D2 | Proposal citing basis generation g1 after an intervening edit made g2 | Schema-valid, stale | Host refuses as stale with reason (DEL-03-02/P) | VER-004 |
| FX-U1 | Operation not in the catalog | Unknown operation | Rejected at V-2 | VER-005 |
| FX-U2 | Operation unavailable to the person ("select a load case first") | Unavailable | Refused with the same reason the person sees (V4-HI-04) | VER-004 |
| FX-M1…M9 | Cases MC-1…MC-9 of §7 | Malformed/truncated | As §7; not dispatched; three reports | VER-005 |
| FX-N1…N11 | Cases MS-01…MS-11 of §5.2 | Settings/destinations | As §5.2 | VER-001, VER-002 |
| FX-C1 | Workflow checkpoint "mark checked before issue" (invented) reached | Checkpoint | Hold; resumes only on host-recorded act of that kind | VER-008 |
| FX-C2 | Same checkpoint; model text says "the engineer has checked this" | Model assertion | Hold continues; no act event | VER-008 |
| FX-C3 | Act recorded, then row `N-30` content changes before resume | Content change | Act lapses; hold returns to waiting | VER-008 |
| FX-C4 | Independently evidenced mark-checked act with no preceding proposal acceptance | Independent act | Accepted as that act; no synthetic acceptance prerequisite | VER-008 |

## 12. Evidence standing labels

Every OUT-003 result carries one of these labels, and they are never merged
(V4-EXM-02/03; SoW AC-002, AC-009):

| Label | Means | Can support |
|---|---|---|
| CONTRACT-REVIEWED | This document was inspected against its sources | Completeness of the receiving expectation |
| FIXTURE-EXECUTED | A fixture ran against a test double or recorded exchange with identified catalog and model-interface bases | That the fixture's expectation holds for that double. Nothing about the host |
| HOST-OBSERVED | Observed on an identified host candidate and configuration | Conformance of that candidate only |
| NOT-OBSERVED | No observation | Nothing; recorded as a gap |

Owner-reported construction (DEP-001's current standing) is none of the
above. It supports no conformance, delivery, adoption or joined-witness
claim.

## UNRESOLVED

| Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|
| OI-013 loop placement, parsing, persistence, panel assembly | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Contract fixes outcomes only (§2.1 M-4, §7, §8); no placement stated |
| OI-014 shared contract/component placement | App/shared contract owners | Before structural/production contract allocation | No common loop implementation; candidate (b) in §10.2 raised as a question only |
| DEP-05-01-024 model-interface identity and protocol/fixture representation | UNKNOWN supplier; App/shared embedded-integration owner receives or agrees | At fixture/conformance use | §4 capabilities semantic only; MC-6, MC-8 held; no fixture executable |
| DEP-001 SWBPIPE host candidate and evidence | SWBPIPE outside implementation session | Before corresponding connected integration/examination and fallback-replacement decision | All host conformance NOT-OBSERVED; cases designed only |
| OI-001 always-reserved acts | Owner with App/SWB contract owners | Before operation-policy production contracts | Human-act class in tool offerings and checkpoint act kinds carried as `UNRESOLVED{OI-001}` |
| OI-002 classifier routine permissions | Owner with App/SWB contract owners | Before permission-policy implementation | Loop holds no permission default (§9 A-4) |
| OI-021 first connected operation | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution | Fixtures use invented subjects; no operation selected |
| N-OPEN-1 meaning of "user-controlled local model server" endpoint | App/shared embedded-integration owner with SWBPIPE owner; owner if V4-HOST-02 meaning is affected | Before endpoint-enforcement conformance cases are finalized | MS-11 held |
| N-OPEN-2 permitted destinations in cloud-chosen operation | Same as N-OPEN-1 | Same | MS-03 asserts "chosen endpoint" only as proposed |
| N-OPEN-3 tool-caused network traffic (e.g. later Domains query) | Tool's receiving-contract owner; Domains allocation open (PRD OQ-03) | Before any network-using host tool | Out of this loop contract; not a permission |
| T-OPEN-1 execution of valid sibling calls beside a malformed call | App/shared embedded-integration owner with DEL-03-02 and host owner | Before fixture FX-M8 is finalized | Proposed answer only |
| R-OPEN-1 any quantitative responsiveness criterion | Owner, if one is wanted | Before any numeric criterion is used | None set; observation protocol only |
| Catalog versioning at offer vs call (O-3) | DEL-03-01 owner | V1 | Proposed rule pending reconciliation |
| Reconciliation of all consumed meanings (C, P, declaration, hold, acts, records) | Respective App-v4 owners | V1 | Names used here are accepted meanings, not supplied versions |

## Verification cases

Designed, not run. "Expected" is the result that would satisfy the case.

| Case | Procedure | Expected result | Serves |
|---|---|---|---|
| VC-01 | Trace §5.1 and MS-01…MS-10 to V4-HOST-01/02 and V4-ARC-11; check each has an expected outcome and an evidence type naming configuration and observed destinations | Every rule traced; MS-11 shown as held; host observations recorded as NOT-OBSERVED | VER-001 |
| VC-02 | Inspect §5.1 N-3, N-6, N-7 and MS-03/06/07/08 against V4-ARC-12; check the native layer is named as enforcement point and fixture evidence is labeled apart from native evidence | Enforcement point named; §12 labels applied; no host claim | VER-002 |
| VC-03 | Review §1, §2, §4 for all four subjects, minimal Chat Completions capability, distinct App Codex path, open supplier/version/wire choices and Pi excluded | Four subjects present with obligations; §1 table distinguishes the paths; §4 marks DEP-05-01-024; no field names | VER-003 |
| VC-04 | Review §6 and FX-S1/S2/D1/D2/U2; with a host trace (when supplied) check V-3 rejection precedes and prevents V-4, and schema-valid calls reach V-4 | Order O-1 holds; FX-D1 refused by host after passing V-3; no act inferred | VER-004 |
| VC-05 | Exercise FX-M1…M9 and FX-V1 against a test double once DEP-05-01-024 and a DEL-03-01/C version exist; inspect for dispatch of rejected calls | Zero dispatch for rejected correlation identities; FX-V1 dispatched; three failure reports present; labeled FIXTURE-EXECUTED | VER-005 |
| VC-06 | Review §8 for scenarios, recorded items and absence of thresholds; on receipt of host observations, check they name candidate, configuration and placement choice | Protocol complete; no numeric threshold; host result limited to observed scenarios | VER-006 |
| VC-07 | Compare §10 one-for-one with SoW CLM-001/002/003, REQ-006, OI-013/014, DEP-001 and the Clarification | Every excluded act has its owner; no common construction allocated; OI-013/014/DEP-001 at their points of need | VER-007 |
| VC-08 | Review §2.4, §9 and FX-C1…C4, FX-V2 against DEL-04-01, DEL-04-03 and DEL-02-01 versions at V1 | Success, queue, findings and model text never become acts; checkpoint waits for its specified act; FX-C4 needs no prior acceptance | VER-008 |
| VC-09 | Audit every claim in this file and later OUT-003 results for a §12 label and an exact source/candidate identity | No HOST-OBSERVED claim without identified candidate evidence; DEP-001 building standing not treated as evidence | VER-009 |
