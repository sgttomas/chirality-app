# SWBPIPE embedded-agent connection proposal

Status: revised design proposal from App HELP_HUMAN, 2026-10-28, incorporating
SWBPIPE HELP_HUMAN's native-interface review at Chirality `1560bbf7f7`.
The coordinators agree on a small host-owned adapter, a minimal functional
panel and dynamic-tool dispatch through the existing webview-owned session.
Implementation remains with the respective owners. After the closure-only
resume, the owner explicitly authorized the new SWBPIPE coordination manager to
build shared integration needs with the App manager. Host adoption and
implementation are authorized. The source-qualified catalog adoption and offline
App checks are recorded in [the receiving account](SWBPIPE_RECEIVING_BINDING.md).
This proposal itself is not evidence of live operation.

Current authorization: the owner opened Type 1 integration and desktop
publication fronts. Their initial App-side preparation used light source/document
work, offline fixtures and small checks during the demo pause. The later owner
steer permits the joint integration's host implementation. Coordinate interfaces
and heavy-build load through
[SWBPIPE's Type 1 counterpart](t3-thread://v1/thread:delegated-task:command%3Amcp%3A430b7a29-d695-474c-bb92-8f42bc864914%3Adelegate-task%3Aa0-appv4-coord-mgr-20261028),
which routes reserved choices and merges to its Agent 0. RT-E1/criterion 17
were owner-approved and merged through #1732 at Chirality
`541446a9f16e4e020a5703cda76e7fb94fbec819`, verified locally by App HELP_HUMAN.
The owner approved stock Codex binary downloads from official releases and
selected the existing oMLX server for the local witness. Hosted-model use is
also allowed, with any sign-in/credential supplied by the owner. No other
downloads are authorized. SWBPIPE owns
the catalog source of truth. The App contribution retains its frozen origin
catalog proposal in the stateless MCP 2026-07-28 shape with explicit
handles, projected through dynamic tools; full MCP transport is separate.
Decisions API work is entirely excluded by the owner, including consideration
as a later option.

## Purpose and current direction

**Receiving status, 2026-10-29.** The [current receiving basis](SWBPIPE_RECEIVING_BINDING.md#current-joined-receiving-basis-2026-10-29)
identifies merged host catalog/Design, the actual harmless local-model summary
witness and unwired Rust transport/session components. Catalog bytes remain at
the existing v2 pin. The earlier Python witness does not qualify the restrictive
Rust launch profile, production desktop integration or full reference-system
capability. SWBPIPE owns native fixture discrimination and activation; no App
implementation prerequisite is identified for that fixture. The
[DEL-09-07 receiving map](../../DEL-09-07/Work/SWBPIPE_RECEIVING.md) names the
remaining joined evidence and exact acceptance reconciliation still owed.

The owner directed in the SWBPIPE session:

> I want you to add the App v4 integration into SWBPIPE for the v1.0 target.
> I want you two to discuss how to make it connect, but I thought this had
> already been decided on (check the deliverables). I'm not interested in
> having all the governance for the workflows working perfectly, my focus is
> just on getting the agent harness into SWBPIPE and able to operate that
> application effectively.

The owner then directed in the App session:

> take note of what was done in the past, but don't take from it. There's
> better examples now elsewhere and just from your own ideas.

These statements govern this proposal. DEC-041 and the older App minimal-loop
design explain history; neither dictates the new architecture. SWBPIPE's merged
PR #1732 carries the owner-approved RT-E1 and exit criterion 17. The intended
experience is a request in the desktop, useful model operations, solve, and an
explanation grounded in the actual results. Workflow governance is not a
prerequisite to the first functional slice.

## Proposed connection

SWBPIPE owns a small Rust client of the stock Codex app-server protocol and a
focused React conversation panel. Codex owns inference, conversation and its
agent loop. SWBPIPE owns model truth, tool validation, permissions, application,
solve, results and human controls. The standalone App need not be running.

The live model is owned by the webview's `workspaceSession.ts`, including its
hash, undo/redo, selection, review queue and run-sheet ledger. Rust's model
operation commands take a model, batch and claimed hash and return a result;
they do not hold the live model. Solve jobs are managed by `SolveJobRegistry`
from the document supplied by the session. App HELP_HUMAN checked
`apps/desktop/src-tauri/src/lib.rs`, `command_ingress.rs` and
`apps/desktop/src/features/workspace/workspaceSession.ts` at the reported
Chirality revision. Moving live-session authority into Rust is outside this
increment. The earlier proposal's assumption of a Rust-owned live model is
withdrawn.

- Start one stock app-server child for the admitted application/profile context
  over private stdio. Initialize, start/resume a conversation, submit turns,
  stream events, answer supported requests and interrupt/stop explicitly.
- Offer SWBPIPE's tool definitions using `dynamicTools` on `thread/start`.
  Receive `item/tool/call` in Rust, validate its arguments, and forward an
  identified request to the admitted webview session. That session performs
  reads, queues proposals or starts solve through its existing routes. It
  returns the outcome through one new ingress-admitted command; Rust validates
  correspondence to the original pending call and answers Codex. The frame
  reader remains responsive while operations or human review wait.
- Keep one SWBPIPE-owned catalog of names, descriptions, argument schemas,
  effects and availability. Use it to produce tool declarations and the panel's
  operation descriptions; do not infer a safe tool merely from an exposed Tauri
  command. Validate full arguments in Rust even if a provider drops schema
  constraints when presenting them to the model. Tool arguments and results
  use the model document's canonical units, with explicit unit fields in the
  catalog schema. Display-unit conversion belongs only in the panel.
- Start with bounded model/object/results/diagnostic reads; propose model
  operations; observe their outcomes; solve; and read the resulting run.
  Export/report capabilities follow the same table and existing user-release
  boundaries. A report-generation tool cannot perform the person's release act.
  Reads are paged or selected by object id, table or filter, with no default
  whole-document dump. Results use existing CSV/value-record paths and their
  redaction floors. Agent-visible content follows the person's view boundaries,
  not raw private records beyond them.
- Each call carries the originating application generation, conversation,
  turn/call identity and the bound workspace-session identity. Reads return the
  session model hash and current state/run ids, or explicit unavailable values.
  Pages retain their basis; a change between pages cannot silently produce a
  mixed-state result. Proposals carry `claimedModelHash`, using the existing
  applier's mismatch refusal. The session also rechecks its current generation
  and revision when admitting a result; a new project cannot inherit an old call.
- Proposed changes use the existing validation, diff/review and single apply
  route. **The first increment is proposal-only:** every change waits for the
  person's acceptance or rejection. SWBPIPE has no autonomy-grant facility yet;
  direct application under a grant is a separate later slice. Agent batches
  carry `author_type: agent` and conversation/turn/call ids, never `user`.
  Attribution is not verified identity. The panel distinguishes pending review,
  withdrawn, rejected, applied and unknown.
- Initially use session outcomes and existing model/run hashes truthfully.
  Keep interrupted/uncertain mutations unknown and never blindly retry them.
  Full durable acceptance history and workflow-act machinery can be staged;
  they must not be claimed available before implemented. Turn interruption
  withdraws a still-pending proposal. Once application has started, interrupt
  does not cancel or undo it: preserve its actual applied result or unknown
  standing. Serialize this transition with the session's apply admission so
  cancellation cannot be reported after application has won the race.
- Bind tools to the live SWBPIPE model, not arbitrary paths in agent arguments.
  Keep the agent workspace separate from authoritative project storage and
  use a fresh scratch Codex home and empty agent working directory. Disable
  shell, patch/file-write and web-search capabilities where the selected pin
  supports it, and apply the necessary read-only/network sandbox restrictions.
  Verify actual behavior with harmless denied-operation probes in slice 1;
  configuration, an empty cwd or a prompt alone does not establish isolation.
  Read-only access is not a privacy boundary against unrestricted file reads.

Rust retains each pending call's original RPC id and conversation/turn/call,
application generation and workspace binding. The webview returns a host-issued
request reference, not an independently chosen Codex destination. Refuse
unsolicited, duplicate or mismatched completions; a lost/replaced session yields
unavailable or unknown, never success or automatic redispatch. Size admission
must precede materialization of tool arguments and returned model-sized data.
New commands use `command_ingress`; update the pinned reach scan and obtain the
project-required permissions scrutiny. Existing memory/admission limits apply
in both directions across the new session request path.

Long solve calls expose progress through the existing job/panel notifications
and finish with run id, evaluated basis and health. Send Codex only progress
messages supported by the selected supplier protocol; do not invent a streaming
tool-result channel. A turn interruption and a solve-job cancellation are
distinct operations. Their actual outcomes remain visible.

No MCP process or network listener is needed for this embedded path. An MCP
adapter could later expose the same catalog to an external controller, but
authentication, live-desktop attachment, call ownership and recovery would
still need their own implementation. CA/X is not obtained for free.

The initial panel is minimal and functional, pending the owner's focused
conversations about interaction and visual design. Existing review mechanics
are integration inputs, not an endorsement of the present table/review UI.
It needs messages, progress and tool outcomes, model/provider selection,
send/interrupt, native permission/question controls, and navigation to the host's
review queue and results. It need not import the App's workflow registration,
trials, fleet or formal act-control interfaces.

## Present source evidence and reuse assessment

App source inspected at `5e61fbd88ff8a4fe221b25cbd9e967d2a6fdce09`:

| Question | Evidence and conclusion |
|---|---|
| Where is the host? | `app/src-tauri/src/hosting.rs` implements `Host`/`HostConfig`, spawning and protocol handling; `runtime_session.rs`, `native_items.rs`, `native_requests.rs` and `native_history.rs` supply receiving behavior; `lib.rs` wires Tauri. `hosting.rs` has 5,714 lines and references 19 sibling modules directly, including records, workflows, roles and recovery. It is not a small standalone library |
| Where is the panel? | `ConversationPanel` is in the 2,072-line `app/src/App.tsx`, coupled to workflow/trial/record features. `NativeActivity.tsx` is 473 lines and imports React only; `RequestCards.tsx` is 391 lines, importing React, activity helpers and exact-text labels. These are useful current examples, not a ready package |
| What transport exists? | `hosting.rs::offered_start_params` supplies the read-only records tool, `on_frame` classifies its `item/tool/call`, and `answer_records_call` returns the result. `records_access.rs::definition` defines the tool. Dispatch is specific to App capabilities, not a general catalog interface |
| Is it versioned for consumption? | The Rust crate is `publish = false`; the frontend is private and has no library build/export contract. A Git pin can identify source but does not decouple it. Do not make extraction or a package-release chain a prerequisite to SWBPIPE's first slice |

Recommendation: write the small SWBPIPE protocol adapter and focused panel
against the supplier API, using current implementations as evidence where
helpful. This implements a client, not a replacement agent loop or SDK. Share
a library only when a concrete stable common responsibility warrants it.

The current [official app-server guide](https://learn.chatgpt.com/docs/app-server)
was fetched through `https://developers.openai.com/codex/app-server/` on
2026-10-28. It documents default stdio, initialization, streaming turns and
experimental `dynamicTools` / `item/tool/call`. The selected binary's generated
schema remains the implementation reference; current documentation does not
establish the behavior of every older pin.

The App's stock 0.160.0 generated schema contains `DynamicToolCallParams`
(`threadId`, `turnId`, `callId`, `tool`, `arguments`, optional `namespace`) and
`DynamicToolCallResponse` (`contentItems`, `success`). Its existing supplier
check observes declaration carriage through start/resume/fork using capture-only
providers, not a real local-model tool call. The historical 0.158.0/LM Studio
observation dropped namespaced MCP tools while a flat built-in function worked.
That is a reason to test the new pair early, not a claim about today's server.

## First implementation slices and evidence

1. **Pin and prove the round trip.** Identify an available stock Codex package,
   local server and local model. Use its generated protocol and experimental
   opt-in. In a fresh scratch home, offer one harmless SWBPIPE-shaped dynamic
   tool and observe an actual model call, host validation, response and a
   follow-up answer grounded in the result. Check malformed arguments and
   interruption with controlled protocol tests, and exercise the built-in tool
   isolation described above. Do not infer success from a
   greeting, tool listing or captured model request. Only the approved official
   stock Codex binary downloads are permitted; other downloads and credentials
   still require the owner. No supplier upgrade is
   selected merely by reading current docs.
2. **Connect the live desktop.** Bind the catalog to the existing model session,
   add the minimal functional panel and route proposals through the existing
   webview session and review/application commands. Exercise an actual accepted
   change, rejection, stale-basis refusal, wrong-session/duplicate completion
   refusal and interruption/unknown outcome without duplicate application.
   No direct-autonomy path is included. Update command ingress/reach evidence
   and review permission and persistence changes independently under project rules.
3. **Demonstrate useful operation.** Use the proposed invented W9-A L-frame for
   the first build/solve/explain journey, comparing actual results with its
   independent references. **W9-A is only this slice's development witness.**
   Criterion 17 requires criterion 1's full reference system, being authored
   under W-17/O-1 according to the SWBPIPE return. Its build/solve/explain witness
   is separate. Then test corrections and representative use cases, not only
   one scripted happy path. Package and native launch evidence remain release work.

Before a live run, identify the exact Codex binary and the existing oMLX
server/model, and check available authorized artifacts. Official stock Codex
binary downloads are approved; record the exact file, source, size and digest.
No other download is approved. Coordinate acquisition and model load through
the SWBPIPE witness owner. Hosted-model use is also allowed, with any credential
or sign-in supplied by the owner; keep hosted evidence distinct from the local
witness rather than silently substituting it. Report actual model capability
against the full reference system. The owner's focused UI discussion still
precedes substantive interaction/visual design.

SWBPIPE owns adapter, panel, catalog, model operations, numerical checks and its
release-target reconciliation. App HELP_HUMAN owns the App-side definition and
joined-evidence reconciliation. Each implementation return names its source pin,
actual checks, unresolved limits and affected deliverables. Direct session
coordination is authorized; cross-repository implementation rights do not transfer.

## Consequences for existing App contracts

The following are explicit reconciliation items, not extra prerequisites to
the first functional slice:

- V4-ARC-10 and DEL-05-01's minimal Chat Completions loop differ from stock
  Codex app-server reuse. V4-ARC-13's catalog responsibility fits the proposal;
  its transport changes to dynamic tools. Reconcile DEL-05-02's panel to the
  focused host experience, without adopting its full older UI by default.
- Codex local-provider protocol/tool support must be established for the chosen
  pin/server/model. Do not treat a Chat Completions endpoint as automatically
  compatible with Codex's local-provider path.
- V4-HOST-02 / V4-ARC-12 and DEL-09-07's network case require stronger evidence
  than selected-provider configuration. Measure and describe actual supplier
  traffic; resolve the retained destination-control claim explicitly rather
  than promising it from the presence of stdio or a local model.
- DEL-09-07 AC-002 describes a support/run adjustment, individual row acceptance
  and rejection, while the proposed first witness builds and solves W9-A.
  AC-003/REQ-007 also require outcome recovery and durable joined evidence.
  Record the functional witness for what it demonstrates and reconcile release
  criteria to the owner's effective-operation focus. It is not an automatic
  pass of every old scenario. Basic stale-state refusal, controlled mutation
  and truthful outcomes remain necessary for effective operation.
- Stage complete workflow round trips, checkpoint/act governance and durable
  decision history according to the owner's current priority. The old
  qualification packet is not the work plan to inherit. Reconcile exact
  changed acceptance text with the owner-confirmed release criterion in the
  owning documents; implementation should not grow to satisfy historical
  machinery by default.

## Decisions API and MCP: coordination answers

Source check by App HELP_HUMAN, 2026-10-28; documentation and pinned schemas
only, with no API request, model turn or MCP cancellation experiment.

**Decisions.** The [official guide](https://developers.openai.com/api/docs/guides/decisions)
states that the Decisions API is generally available, uses `POST /v1/decisions`,
and currently supports only `gpt-6-luna`. It returns predicate probabilities,
choices from supplied options, or rubric scores; a question can also receive
a refusal. The [create reference](https://developers.openai.com/api/reference/resources/decisions/methods/create)
confirms these typed answers. These are managed OpenAI API requests; no local
deployment is documented. Private Link is connectivity to the service, not a
local model option.

The guide explicitly recommends function calling for requests that generate
tool arguments. Decisions could select a tool name or an already constructed,
fully bound candidate action; it cannot synthesize arbitrary geometry, object
ids and argument structures. Even schema-valid function arguments still need
SWBPIPE's semantic, units, basis and permission validation. Precise validation
errors allow the agent to repair a proposal without changing the engine's rules.

**Owner disposition:** exclude Decisions entirely and do not consider it for
these fronts. The factual answer above preserves the research already done;
it is not an integration option or a deferred work item. Use a small catalog
and deterministic validation. Catalog narrowing per turn is not assumed:
the present dynamic-tool declaration is supplied at thread start; any later
loading/change mechanism needs its own pin-specific support.

**Catalog compatibility.** Adopt MCP-compatible shapes as a design convention,
without claiming the dynamic-tool wire is MCP:

- Tool descriptor: `name`, `description`, `inputSchema`, optional `outputSchema`
  and `annotations`. Keep SWBPIPE's effect, availability, canonical-unit and
  basis requirements alongside these fields. The host implements policy;
  `readOnlyHint`, `destructiveHint` and `idempotentHint` are descriptive hints,
  not authorization or a guarantee that retry is safe.
- Tool result: `content`, `structuredContent` and `isError`, separate from the
  descriptor. Validate structured output against the selected output schema.
  Keep pending/rejected/withdrawn/applied/unknown domain outcomes explicit;
  a user's rejection is not automatically a tool execution error.
- Dynamic adapter at 0.160.0: offer the supported function definition
  (`type`, `name`, `description`, `inputSchema`). Retain output schema and
  annotations in the application; these are not fields of that function
  definition. Encode validated structured results as JSON text in
  `contentItems`; map execution error standing to `success` under the stated
  result policy. Do not send unsupported `structuredContent`/`isError` fields
  on the dynamic-tool wire or imply their native preservation.
- A later MCP adapter can project the same descriptors/results. Discovery
  helps other clients consume the catalog, but client capabilities, workspace
  attachment, permission and outcome semantics still require qualification.
  It also supplies the negotiated MCP wire envelope (including the current
  edition's `resultType` and input-required behavior where applicable); the
  internal result is not blindly passed through as a complete MCP response.
  Resources/subscriptions and elicitation are optional additions, not promises
  inferred from a tool descriptor. An elicitation `accept` means accepting the
  requested input; model-change acceptance still binds to the actual proposal,
  current basis and person's action in SWBPIPE.

The current [MCP tools specification](https://modelcontextprotocol.io/specification/2026-07-28/server/tools)
defines these descriptor/result distinctions and says annotations from untrusted
servers must be treated as untrusted. It separates server-produced structured
content from model structured-output generation. Version the projection;
the current MCP edition is not proof of every feature in Codex 0.160.0.

**Present pin evidence.** 0.160.0 is the App development pin, not a newly
qualified SWBPIPE integration pin. Its generated protocol supplies:

- `item/mcpToolCall/progress`: `McpToolCallProgressNotification` has message,
  thread, turn and item ids. This is an explicit protocol surface, not evidence
  that numeric MCP progress/total fields arrive unchanged or a live SWBPIPE
  call has emitted it.
- `mcpServer/elicitation/request`: form and URL requests and
  `accept`/`decline`/`cancel` response actions are represented. App RequestCards
  implements form/URL input controls; device-proof acceptance remains unsupported
  in that App path. This does not provide SWBPIPE's proposal-review binding.
- `turn/interrupt`: an explicit thread/turn cancellation request. No examined
  evidence here establishes downstream MCP cancellation delivery, host-job
  termination or rollback. Test those separately if MCP is adopted; an empty
  interrupt response cannot prove them.

The [MCP progress](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/progress),
[cancellation](https://modelcontextprotocol.io/specification/2026-07-28/basic/patterns/cancellation)
and [elicitation](https://modelcontextprotocol.io/specification/2026-07-28/client/elicitation)
specifications define protocol mechanisms, not these application outcomes.
The current elicitation specification also has input-required/multi-roundtrip
semantics; do not silently equate it with all older server-request behavior.

Recommendation remains dynamic tools for slice 2. SWBPIPE already owns the job
progress and human review UI; MCP adds a process/transport attachment to the live
session without eliminating those responsibilities. MCP-compatible catalog
shapes preserve a practical external-client path without making it a dependency.
