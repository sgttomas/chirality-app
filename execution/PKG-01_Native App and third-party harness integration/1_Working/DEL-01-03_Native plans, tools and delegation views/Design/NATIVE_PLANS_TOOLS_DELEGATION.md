# Native plans, tools and delegation views
- Contribution: DEL-01-03/NPTD-v0.1 (first Design file of this deliverable)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Run and node: `APP-V4-DESIGN-PASS-3-20261001`, node D2 (Type 2 TASK, Claude Opus 5.5, high effort), written 2026-10-01. This file claims no SWBPIPE join, witness or adoption, and changes no register, ScopeOfWork, status, graph or other Design file.
- Phase (V4-WF-05 as amended by SCA-V4-001; R8-1; R9-1): Phase 1. No App run holds at a checkpoint; nothing here makes a hold claim.
- Serves: OUT-001 (view definitions: §3–§9, §12, §13), OUT-002 (fixture method and designed cases: §15), OUT-003 (feature and optional-reuse map: §14); REQ-001…REQ-008; designed cases for VER-001…VER-007.
- Basis (accepted, as amended by SCA-V4-001 and SCA-V4-002; sha256 recomputed with `shasum -a 256` at this node): `docs/PRD.md` bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd (V4-APP-01/04, V4-EXE-01…03, V4-AUT-01…05, V4-REC-03/05); `docs/ARCHITECTURE.md` 317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c (M-2, M-7, §3 V4-ARC-01/05 and its properties, "rather than a Chirality copy"); `docs/HOST_INTEGRATION.md` d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f (§1, V4-HI-30…33); `docs/EXAMINATION.md` 471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0 (V4-EXM-01…05, 10, 11, 13). The deliverable's `ScopeOfWork.md` b5d533cb3dbea97b37950792ad2c68f42bf6023effa4ac894209a1ef3fc605f2 (INIT contract, unrevised by either amendment) and `Dependencies.csv` 9ac820166dd07dde8bbad59ba1c2b0818ab7f4ff4b435c6991cc2d887ddeedf4. DAG-003 (`_DAG/DAG-003/`), cited for arc layers.
- Owner and integrator records (run folder `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/`): `OWNER_DECISIONS.md` 9d18c40dd7d894dc20b9edd2803dc6ab63f1deeadb79919411ea71f2ef248b1b (DECISION-K3 as revised: K-5, K-10 bind here; K-3 bears on plan mode); `R17_RESOLUTIONS.md` b0af81bcbad9bc52fddc99119c42a19019a9b174677d5b92a0a2f5c8b4f8e198 (R17-1, -2, -4, -5, -9, -10, -13, -14, -15); `BRIEFS.md` b261394112d7264ef0b87ced64a513eccf0cb41dc96c8dfc8ec955ca62fb05c1 ("Common rules", "D — design nodes, round 1", row D2); `DECISIONS_PENDING.md` 431ec4eb22a0b91323b2f33118c6820527fa9effc85de9e847a221a9023fdd86 (the K-5 and K-10 option texts DECISION-K3 accepted); `SURVEY/S1-A.md` 8f021191f20e4a7e1e6b51fdcfb729bb9a562f3e4c6dd7144be937d77151e8ca (Part 2, §3.1, §3.2). Earlier owner records and rulings R1–R16 stand as the common rules say; DECISION-K1 K1-4 ("identity not verified") applies (§9).
- First-increment Design files read (cited by label and section; none edited, R17-14): DEL-01-01/HOSTING-BOUNDARY-v0.8 `HOSTING_BOUNDARY.md` 3cf0381c42358fec4a2088ab3886e14b66d6d2020482c72e195fda068a6d78b1 (§3 H4–H7, H10; §4.2, §4.6; §5, §5.1; §7.1–§7.3; §8 S-2; §8.4; §9.2; §10.1; §11; §12; F-12, F-13, F-15; U-06, U-08, U-19, U-21; VC-09); DEL-01-01/PIN-SPIKE-v0.1 `PIN_SPIKE_0.158.0.md` 0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115 (P-10, P-13, P-15, S-F-13); `OBS_1_0.158.0.md` 7b984b541edca0b14534d29115e77642c587a32f830bdf25a94a7ecca882cc43 (O-5, O-6; OBS-1b OB-2, OB-3 as HOSTING §10.1 states them); DEL-02-01/WD-v0.8 `WORKFLOW_DECLARATION.md` 517821d18fc958301d3adaeb63caf11ab50f7e1ca3ec5a644a3bb4ec78b25b0e (§4.2.5 `plan-update`, `agent-delegation`, HC-3, HC-4); DEL-02-03/EXEC-v0.6 `EXECUTION_COMPATIBILITY.md` 64e732d502d0b91da00e62069be1b77b61d1e84986b3744bc117b6e67524fa38 (EV-3a rows `agent-delegation`, `plan-update`); DEL-04-03/RS-v0.8 `RECORD_SEMANTICS.md` b25cc90e9e252f50f30fcaed7faf230ec7bbf4689dcc2cd90deb35c7dcf7f47b (§6.1 decision actor and recorder, §6.2 HA-1, HA-2; §10).
- Supplier evidence: the committed 0.158.0 JSON Schema bundle `DEL-01-01/Design/generated/0.158.0/json-schema/experimental/codex_app_server_protocol.v2.schemas.json` (sha256 34f28a486d00fbd20e5da0b0da3422d1d6e20ec897d12b31408f87499198f458), and the generated TS output in the session scratchpad (`…/scratchpad/codex-0.158.0/gen/ts-{stable,experimental}/run1/`, read only). The 34 TS files this file cites were checked against `generated/0.158.0/MANIFEST.sha256` (42b95826…69e): 34/34 equal (experimental variant), and the stable `ThreadItem.ts`, `Thread.ts`, `Model.ts`, `TurnPlanUpdatedNotification.ts` equal too. The Codex binary was not run; no model was run; no network was used.
- App v3 exemplar (`projects/chirality-app-dev`, `projects/chirality-runtime`): evidence of what was built before, never a v4 commitment (§14.2).
- Receivers (from the live register rows; layer per DAG-003): DEL-02-02 via DEP-01-03-013 (admitted; mirror DEP-02-02-012): the plan-revision reference (§5.6); PKG-06 via DEP-01-03-014 (package target, not topological) and DEL-06-01 via its own DEP-06-01-007 (admitted): the delegation export (§7.7); DEL-09-02 via DEP-09-02-011 and DEL-09-05 via DEP-09-05-008 (both admitted): fixtures, designed cases and the descendant presentation (§15). Offered without a register row (proposed in the return, §16.3): DEL-01-04 (item anchors, plan-mode element) and DEL-02-04 (the delegation export for its K-10 limit account). Suppliers: DEL-01-01 via DEP-01-03-011 (admitted) and DEL-01-02 via DEP-01-03-012 (admitted).

**ScopeOfWork reading (R17-15).** The INIT contract lags later decisions in
four places. This file reads it as follows, and the return lists a precise
proposal for each: (1) TBD-001's "selected supplier pin … remains with the
App implementation owner (OI-012)" is read with owner decision D4: 0.158.0 is
the definition and generation pin, not a qualification, so REQ-004's display
says so (§8). (2) CLM-004, AX-002 and TBD-003 "OI-001/002 remain open" are
read with D2 and D3 (reserved acts; routine tool permission is the person's
Codex setting). (3) REQ-005's "faithfully display" is read with DECISION-K1
K1-4: an App-captured act names the person "identity not verified". (4)
REQ-001's plan revisions are read with R17-4: checklist revisions that Codex
does not keep are not copied, and after a relaunch they are shown "not
recoverable after relaunch"; plan-item revisions are recovered from Codex
history. K-5 (experimental surfaces) and K-10 (task-agent delegation shown,
stated not enforced) are applied as DECISION-K3 records them.

**Reading note.** Labels: **SETTLED** (an accepted text or owner decision
says it), **DERIVED** (follows from those), **INTEGRATION** (an integrator
ruling), **PROPOSED** (this file's design, not yet decided by anyone).
Supplier facts carry the standing labels of R17-13: `observed` (live in the
spike or OBS-1), `observed-in-generated-types`, `inference`. Supplier
methods, fields and values are quoted as supplier names; everything else
(display states, identities, schema names) is this file's own semantic
naming, not a wire choice. Cells that OBS-2 (R17-16) will settle are marked
**OBS-2 pending**.

---

## 1. What this deliverable is, and where it sits

DEL-01-03 presents Codex's own plans, tool activity and delegation in the
App, and offers the plan interactions the person uses to direct work
(SOW-003, SOW-004, SOW-006, SOW-014, SOW-128, SOW-129). It renders native
items, never a translated Chirality event vocabulary (V4-APP-04, V4-ARC-05,
CLM-001; HOSTING H6). It does not start the Codex process, hold the request
register, answer requests, keep records or perform any act (§16).

**Placement (PROPOSED under R17-5; OI-008 option O-1, which the phase review
owns).** The Rust host owns the Codex process, the frame exchange, the
request register and record writing (HOSTING §1, §12 O-1). DEL-01-03's views
live in the interface: they compose and present native frames the host
delivers with generation and receipt position beside each frame (HOSTING H6,
§5 Order), plus history reads made through the host's generic request path
(HOSTING §5.1). The view state is derived and in memory only; DEL-01-03 keeps
no file and no copy of Codex history (R17-4, ARCH §3). The requirements below
hold under any placement; only §12's "who re-attaches" changes with OI-008.

```text
 Interface: DEL-01-03 views ── plan view · tool activity · delegation view · version line
     ▲ native frames + (generation, position)     ▲ runtime values handed in (not production inputs):
     │ history reads via the generic request path │  register state of an item's request (DEL-01-02/01-04),
     │ ready(g) record, lifecycle events          │  conversation role (DEL-02-04), act records (DEL-04-03
 Host (Rust): DEL-01-01 boundary + DEL-01-02     │  via DEL-01-04's placement), selected model (composer)
     custody, re-attachment, recovery reads
     │ published JSON-RPC over stdio
 stock Codex App Server 0.158.0 (definition pin)
```

---

## 2. Receiving comparison of seam S-2 (closes HOSTING F-15 for S-2)

HOSTING §8 S-2 states what DEL-01-01 supplies to DEL-01-03 and what it does
not. Compared from the receiving side:

| S-2 element (HOSTING §8) | How DEL-01-03 uses it | Standing |
|---|---|---|
| Version identity record with each `ready(g)` (§7.1) and the verification result (§7.2), via "read version identity and verification result" (§4.6) | Version line (§8); fixture binding (§15.1) | Accepted as supplied |
| Native plan items and plan updates "unchanged with generation and receipt position" | Plan revisions (§5): checklist revision identity is derived from generation and receipt position | Accepted. Needs one thing S-2 does not state: the host keeps the current App session's events re-readable from a position after a window reload (HOSTING §4.6 "observe lifecycle", realization DEL-01-02's). Joined to DEL-01-02 (§17 J-3) |
| Generic request path for plan interactions (§5.1) | Plan-mode turn element (§5.4), `collaborationMode/list`, `model/list`, thread reads (§5.3, §7.4); initiator `receiver:DEL-01-03` for reads and `person-directed` for the person's turn | Accepted |
| Declared capabilities with `ready(g)` (§4.2 step 4) | Whether the experimental opt-in is declared decides the plan-mode control (§4) | Accepted; K-5 means the App declares `experimentalApi` true (joined to HOSTING §4.2, §17 J-1) |
| "At 0.158.0 each plan update carries the whole plan with no revision identity … plan deltas must not be assumed to concatenate … plan mode is experimental-only" (S-F-13) | §5.1, §5.2 | Accepted; re-checked against the generated types (§5.1) |
| Not supplied: "Revision identity (DEL-01-03 derives it …), registry, storage, export, UI, checker (SOW-128)" | Revision identity: §5.2. Registry and storage: none (R17-4). Export: §5.6, §7.7. UI: §3–§9. Checker: none selected (TBD-002) | Taken here as stated |

Nothing in S-2 needs changing. One cell of HOSTING §8.4 does (§7.1, §17
J-2), and HOSTING VC-09's expected result is met by §5.2 (§17 J-4).

---

## 3. Item scope and the split with DEL-01-04 and DEL-01-02 (B-5; PROPOSED)

Every native item kind, notification and request of HOSTING §8.4 Part A is
rendered by exactly one owner. DEL-01-03 owns the item-level views; DEL-01-04
owns conversation messages, turn outcome, request cards and attachments
(CLM-003); DEL-01-02 owns execution state (CLM-002). Both UX slices read
DEL-01-02's state.

| §8.4 group | Native kinds (supplier names) | Rendered by | DEL-01-03's part |
|---|---|---|---|
| HCG-A01 Messages and reasoning | `userMessage`, `agentMessage`, `reasoning` and their deltas | DEL-01-04 (conversation and turn) | None. A `userMessage` is never read as an act (§9 TA-3) |
| HCG-A02 Shell commands | `commandExecution`; `item/commandExecution/outputDelta`, `…/terminalInteraction` | DEL-01-03 | Tool row (§6) |
| HCG-A03 File changes | `fileChange`; `turn/diff/updated`, `item/fileChange/outputDelta`, `…/patchUpdated` | DEL-01-03 | Tool row (§6); the turn diff is shown as supplied |
| HCG-A04 Permission requests and review routing | `item/permissions/requestApproval`; `item/autoApprovalReview/*`, `guardianWarning` | DEL-01-04 (request cards, A14) | The affected item row shows `waiting-on-request` and links to the card by item anchor (§6.2) |
| HCG-A05 MCP tools | `mcpToolCall`; `item/mcpToolCall/progress` | DEL-01-03 | Tool row (§6) |
| HCG-A06 App-offered tools | `dynamicToolCall`, `functionCallOutput`; `item/tool/call` request | DEL-01-03 (items); DEL-01-04 (the request) | Tool row. None is registered in this increment (HOSTING §6.1) |
| HCG-A07 Input from the person | `item/tool/requestUserInput`, `mcpServer/elicitation/request` | DEL-01-04 | A plan clarification answered there is conversation input (§5.3 PS-3) |
| HCG-A08 Native delegation | `collabAgentToolCall`, `subAgentActivity` | DEL-01-03 | Tool row for the call; delegation view (§7) |
| HCG-A09 Planning | `plan`; `turn/plan/updated`, `item/plan/delta`; `collaborationMode/list` (exp) | DEL-01-03 | Plan view (§5) |
| HCG-A10…A15 | `webSearch`, `imageView`, `imageGeneration`, `enteredReviewMode`, `exitedReviewMode`, `contextCompaction`, `sleep`, `hookPrompt` | DEL-01-03 | Tool row; these kinds carry no outcome element except `imageGeneration` (§6.3) |
| HCG-A16, A17 | Memory, realtime voice (client methods only, all experimental) | Not presented in this increment | — |
| HCG-B03 Turn control | `turn/started`, `turn/completed`, `turn/interrupt` | DEL-01-04 (outcome); DEL-01-02 (state, interrupt) | Reads turn end as an event for §13 (PL-06, CL-03, TI-07/08) |
| HCG-B02 Thread lifecycle and history | `thread/read`, `thread/turns/list`, `thread/items/list`, `thread/status/changed` | DEL-01-02 (state and recovery) | Issues history reads for its own views (§12) and reads child threads (§7.4) |

An item kind that 0.158.0 does not list (an unfamiliar item) is shown as
"unfamiliar item `<type>`" with its native content inspectable, never dropped
(HOSTING H7) and never mapped to a known kind.

---

## 4. Experimental surfaces (K-5; SETTLED decision, PROPOSED rule)

DECISION-K3 K-5: use Codex's experimental plan mode and delegation surfaces,
labelled "experimental" where they appear, with the App fully usable without
them (the views are absent).

**What is experimental at 0.158.0** (variant diff of the generated TS, the
only test HOSTING §7.3 allows; `observed-in-generated-types`):

| Surface | Variant at 0.158.0 | Bearing |
|---|---|---|
| `turn/start` → `collaborationMode` {mode `plan` \| `default`, settings {model (required), reasoning_effort, developer_instructions}} | Experimental-only | Plan mode needs the opt-in |
| `collaborationMode/list` (presets: name, mode, model, reasoning_effort) | Experimental-only | Tells the App whether a plan preset exists |
| `multiAgentMode` on `thread/start`, `turn/start` and in thread responses | Experimental-only **and** deprecated: on requests "@deprecated Ignored. Use Ultra reasoning effort for proactive multi-agent behavior"; in `ThreadStartResponse` "@deprecated Always `explicitRequestOnly`" | Not a usable control or signal (F-1) |
| Item kinds `plan`, `collabAgentToolCall`, `subAgentActivity`; `turn/plan/updated`; `item/plan/delta` | Stable | Rendered whether or not the opt-in is declared |
| `Thread.parentThreadId`, `agentNickname`, `agentRole`, `sessionId`; `Model.multiAgentVersion` (`disabled` \| `v1` \| `v2`); `experimentalFeature/list` | Stable | Delegation identity and availability (§7) |

**Rule EX-1 (when the label appears).** A view element carries the label
"experimental" when (a) it uses a protocol element that is experimental-only
by the variant diff of the pin, or (b) it depends on a Codex feature that
`experimentalFeature/list` reports as enabled with stage `beta` or
`underDevelopment`. Which Codex feature names gate delegation and plan mode
at 0.158.0 is runtime data, not in the types: **OBS-2 pending** (O-4). Until
it is known, rule (b) labels nothing, and the delegation view is not labelled
by (a) because its item kinds are stable (F-2).

**Rule EX-2 (the opt-in).** The experimental opt-in is a per-connection
handshake capability (`experimentalApi`, HOSTING §4.2 step 4), recorded in
each `ready(g)` with the declared capabilities. Under K-5 the App declares
it (joined to HOSTING, §17 J-1). DEL-01-03 reads the declared value per
generation, never infers it from an experimental element arriving (HOSTING
§7.3, OB-5).

**Rule EX-3 (fully usable without).** With the opt-in not declared, or with
no `plan` preset in `collaborationMode/list`, the plan-mode control and the
plan-mode composer element are absent. Every stable item still renders:
checklist plans, plan items if Codex sends them, tool rows, delegation. No
other control depends on an experimental surface. (Prototype PC-12.)

---

## 5. Plans (REQ-001, AC-001, VER-001)

### 5.1 The two native plan surfaces at 0.158.0

| Surface | Native shape (`observed-in-generated-types`; P-10) | In history? | Revision identity supplied? |
|---|---|---|---|
| **Checklist**: the agent's step list, updated during a turn | `turn/plan/updated` {threadId, turnId, explanation (string or null), plan: [{step, status `pending` \| `inProgress` \| `completed`}]}; the whole list each time | **No**: `TurnPlanStep` occurs only in `TurnPlanUpdatedNotification` (checked by grep over the TS output; no `ThreadItem` or read response carries it). Inference: Codex keeps no checklist history readable through App Server at 0.158.0 | No |
| **Plan item**: a proposed plan (plan mode) | Item `plan` {id, text} with `item/started` / `item/completed`; `item/plan/delta` {threadId, turnId, itemId, delta}, documented "Clients should not assume concatenated deltas match the completed plan item content" | **Yes**: `plan` is a `ThreadItem`, returned by `thread/items/list` (`ThreadItemEntry` {turnId, item, …}) and `thread/read` with turns | Item identity only |

That plan items are produced in plan mode and checklists in default mode is
an inference from the type documentation; neither has been observed live
(no OBS-2 item covers plans; UNRESOLVED U-P1).

### 5.2 Revision identity and durability (B-2; PROPOSED, R17-4 applied)

- **RV-1 Plan-item revision.** Each completed `plan` item is one revision.
  Identity `pi:<threadId>:<turnId>:<itemId>`, from Codex identities only, so
  the same identity is derived live and from history. Ordinal: position among
  the thread's plan items in history order (turn order, then item order in
  `thread/items/list` ascending). Live, the ordinal is the order of
  `item/completed` receipt; the two orders are expected to agree (inference,
  checked in PC-05 against constructed reads; a disagreement is shown, not
  resolved silently).
- **RV-2 Checklist revision.** Each `turn/plan/updated` received is one
  revision of that turn's checklist. Identity
  `cl:<threadId>:<turnId>:g<generation>:p<receipt position>`; ordinal: receipt
  order within the turn. A repeated identical list is kept as its own
  revision and marked "unchanged from the previous" (not merged: it is what
  Codex sent). An update after the turn's end is kept and marked "after turn
  end".
- **RV-3 Content identity.** Each revision carries a content identity of its
  native content (plan text; or explanation and steps), method recorded with
  the value. Method: SHA-256 over canonical JSON, **TEST VALUE** pending
  HOSTING U-08 (algorithm for records).
- **RV-4 Durability.** Window close or reload: the view re-attaches and
  re-derives from the host's re-readable events of the current App session
  (DEL-01-02's realization, §12 SQ-2), so identities and ordinals are
  unchanged. Supplier restart within the session: plan items are re-read
  from history; checklist revisions of the closed generation stay shown for
  the session if DEL-01-02's re-attachment keeps closed-generation events
  re-readable, otherwise they are shown "not recoverable" (§17 J-3).
  **Relaunch:** plan-item revisions are recovered from history ("recovered
  from Codex history"); checklist revisions are **not recoverable after
  relaunch**, shown as such on each earlier turn, never reconstructed from
  messages or guessed. HOSTING S-2 stays "Not supplied" (R17-4; S1-A S-3
  resolved without a HOSTING change).
- **RV-5 Deltas.** `item/plan/delta` text is a streaming preview labelled
  "in progress; may differ from the completed plan". It never becomes a
  revision; the completed item's text replaces it. A difference between the
  concatenated preview and the completed text is expected and not an error.
- **RV-6 Missing pieces.** A delta or completion with no `item/started`
  starts the item (PL-02, PL-05); a plan item still streaming when its turn
  ends or its generation closes is shown "incomplete — not completed when
  observation ended" and yields no revision (PL-06, PL-07) until a history
  read supplies a completed item (PL-09).

### 5.3 Plan interactions (B-3; PROPOSED)

| ID | Interaction | What is sent (through DEL-01-04's turn composition; §5.4) | Failure behaviour |
|---|---|---|---|
| PS-1 | **Create a plan in plan mode.** The person chooses "Plan" (labelled experimental) and writes the request | `turn/start` with `collaborationMode` {mode `plan`, settings {model: the conversation's selected model, reasoning_effort: as selected or null, developer_instructions: **null** ("use the built-in instructions for the selected mode")}} | Control absent (EX-3). No model selected → "run not started — no model selected" (K-3; R15-1 wording); nothing is sent. Supplier error → shown as the error response (HOSTING §5.1), plan view unchanged |
| PS-2 | **Revise.** The person writes a further instruction in plan mode | As PS-1; Codex's next plan item is revision n+1 | As PS-1 |
| PS-3 | **Answer a plan clarification.** Codex asks through `item/tool/requestUserInput` | Answered on DEL-01-04's card; the answer is conversation input, never act evidence (R9; EXEC CAP-6; HOSTING VC-23) | As DEL-01-04 defines |
| PS-4 | **Edit and resend.** The person copies the plan text into the composer, edits it and sends | Ordinary input; the App never edits Codex's plan item | — |
| PS-5 | **Carry out this plan.** | Ordinary input (R17-9). Once a conversation has used plan mode, every later turn carries `collaborationMode` explicitly, mode `default` here, because the types do not say whether the mode persists across turns (inference; UNRESOLVED U-P2). No act is recorded unless a workflow checkpoint names one, which DEL-01-04's act control then captures | As PS-1 |
| PS-6 | **Checklist in default mode** | Nothing: the agent updates it; the person directs by ordinary input | — |

Which plan revision the person acted on is read from Codex history order (a
`userMessage` after plan item n), not kept by the App. v3 kept "which plan
revision was sent for execution" in local storage (`plan-executions.ts`);
v4 does not (R17-4).

**Plan mode and supplied guidance (F-3).** The generated description of
`collaborationMode` says it "Takes precedence over model, reasoning_effort,
and developer instructions if set". So a plan-mode turn may run with the
mode's built-in instructions in place of the thread's `developerInstructions`,
which carry role and workflow supply (R17-8; DEL-02-04). Whether it replaces
or adds is not observed (inference from the doc comment). DEL-01-03 never
puts role or workflow guidance into the mode's `developer_instructions`
(it sends null), and the plan-mode control shows "plan mode may set aside
the conversation's role guidance for this turn (supplier behaviour not yet
observed)". Joined to DEL-02-04 (§17 J-7); an observation is proposed (U-P3).

### 5.4 The plan-mode element offered to DEL-01-04 (PROPOSED)

DEL-01-04 composes and sends turns (CLM-003 "turn/outcome"). DEL-01-03
offers it one operation: **plan-mode element (mode, selected model, effort)**
→ the `collaborationMode` value of PS-1/PS-5, or "not offered (<reason>)"
when EX-3 applies, or "run not started — no model selected". The selected
model is a runtime value the composer hands in (K-3; DEL-01-05 owns the
selection states). DEL-01-03 consumes nothing from DEL-01-04 (R17-10).
Prototype PC-12 validates both composed `turn/start` parameter sets against
the bundle's `TurnStartParams`.

### 5.5 Plan acceptance standing (B-4; INTEGRATION R17-9)

"Carry out this plan" is ordinary conversation input, not a reserved act,
unless a workflow checkpoint names an act; then the act is the person's
through DEL-01-04's act control, and the plan view only shows the record
handed to it (§9 TA-4). Nothing in the plan view is a control that records
an act.

### 5.6 The plan-revision reference offered to DEL-02-02 (B-8; PROPOSED)

DEL-02-02's workflow-making journey receives plan content from this view
(DEP-01-03-013, admitted; the journey is DEL-02-02's). DEL-01-03 offers a
**plan-revision reference**: one record of `npt.plan-revision.schema.json`
(beside this file): revision identity and kind, thread, turn, item (plan
items), generation and position (checklists), ordinal, native content,
content identity with method, standing (`live-observed` or
`recovered-from-supplier`; a checklist can only be `live-observed`), the
types pin and the observed version label. DEL-02-02 decides what a draft
takes from it; the reference is App-observed, not authority for what Codex
holds.

---

## 6. Tool activity (REQ-002, AC-002, VER-002)

### 6.1 Display states

Each tool row has one display state, derived from native events and the
register state handed in (§13 TI table):

| Display state | Meaning |
|---|---|
| `in-progress` | `item/started` observed, no completion yet |
| `waiting-on-request` | A server request for this item is outstanding in the register (runtime value from DEL-01-02/DEL-01-04). OBS-1b observed the item announced in progress while its approval was pending (OB-3) |
| `completed`, `failed`, `declined`, `interrupted` | `item/completed` observed with that native status (enums: `CommandExecutionStatus`, `PatchApplyStatus` completed/failed/declined; `McpToolCallStatus`, `DynamicToolCallStatus` completed/failed; `CollabAgentToolCallStatus` adds interrupted). Kinds with no status element show `completed` meaning only "completion observed" |
| `unknown` | No completion was observed: the turn ended or the generation closed first, or a history read shows the item still `inProgress`. Never shown as failed or succeeded (V4-EXE-03; HOSTING H10) |

The native status value is always shown beside the display state, unchanged.

### 6.2 Rules

- **TR-1 No translation.** A row carries the native item unchanged; the
  display state is a reading placed beside it. No supplier method, kind or
  value is renamed (V4-APP-04; prototype PC-07).
- **TR-2 Origin of a command.** `source` is shown as supplied at
  `item/started` and at `item/completed` (OBS-1b OB-2 saw `agent` then
  `unifiedExecStartup` on one item). A `userShell` command is the App's own
  call at the person's direction (`thread/shellCommand`, HOSTING §8.4
  HCG-A02), labelled so, never as the agent's action.
- **TR-3 Request settlement.** For an item whose A14 request was settled, the
  row shows the settlement origin exactly as the register supplies it
  (`person-via-interaction`, `supplier-internal`, `app-rule:<name>`; HOSTING
  §6). A `declined` status with no settlement handed in shows no origin:
  the decline may be the person's, the supplier's own reviewer or the
  person's Codex mode (H9, D3), and the row does not guess (prototype PC-06).
- **TR-4 Outcome available or not.** At completion, a row whose kind has
  result elements (`commandExecution` aggregatedOutput and exitCode,
  `fileChange` changes, `mcpToolCall` result and error, `dynamicToolCall`
  contentItems and success) shows "result not supplied by Codex" when all of
  them are null. That is AC-002's *unavailable*: Codex said the call ended
  but gave no result. `unknown` (§6.1) is the different case where no end
  was observed.
- **TR-5 Exit codes and success flags** are shown as supplied; the App does
  not turn an exit code or `success` into its own success judgement.
- **TR-6 Request link.** A `waiting-on-request` row carries an item anchor
  (`npt.item-anchor.schema.json`); DEL-01-04's request card cites the same
  anchor, so the person can move between card and row. The row never offers
  an answer control (A14 is DEL-01-04's, HOSTING §11).

### 6.3 What each row shows

| Kind | Shown (supplier names) |
|---|---|
| `commandExecution` | command, cwd, source (start and completion), commandActions, status, exitCode, durationMs, aggregatedOutput (and live `outputDelta`; OB-2 saw none on one run) |
| `fileChange` | changes (path, kind, diff), status; the turn's `turn/diff/updated` |
| `mcpToolCall` | server, tool, arguments, status, result or error, durationMs, readOnlyHint |
| `dynamicToolCall` / `functionCallOutput` | tool, namespace, arguments, status, success, contentItems / name, output |
| `collabAgentToolCall` | tool, status, sender and receivers, prompt, requested model and effort, agentsStates (also in §7) |
| `webSearch`, `imageView`, `imageGeneration`, review mode, `contextCompaction`, `sleep`, `hookPrompt` | Their elements as supplied; `imageGeneration.status` is a free string and is shown, not mapped |

---

## 7. Delegation (REQ-003, AC-003, VER-003; K-5, K-10)

### 7.1 Availability (F-1; PROPOSED signal)

At 0.158.0 delegation needs no experimental opt-in to be seen: its item
kinds are stable (§4). `multiAgentMode` is deprecated and ignored, and the
thread response always reports `explicitRequestOnly`, so it says nothing
about whether delegation is available (`observed-in-generated-types`). The
stable element that does is `Model.multiAgentVersion` from `model/list`
("Multi-agent runtime declared by this model": `disabled`, `v1`, `v2`, or
null). PROPOSED reading for the delegation view: `disabled` → the view says
"this model declares no multi-agent runtime"; `v1`/`v2` → nothing extra;
null → nothing extra. Whether the person's Codex feature settings also gate
it is **OBS-2 pending** (O-4). HOSTING §8.4 HCG-A08 and EXEC EV-3a both cite
`multiAgentMode` as the signal; the correction is joined (§17 J-2, J-5).

### 7.2 Identity model

A **descendant** is a Codex thread that is a child of another, keyed by its
thread identity. Elements and their sources, in order of authority:

| Element | Source (supplier names) | Standing |
|---|---|---|
| threadId | `collabAgentToolCall.receiverThreadIds`; `subAgentActivity.agentThreadId`; `Thread.id` | observed-in-generated-types |
| parentThreadId | `Thread.parentThreadId` ("only set if this thread is a subagent") from `thread/read`; else `collabAgentToolCall.senderThreadId`; else the thread whose `subAgentActivity` item names the child (**inference**, labelled) | As named in `parentSource` |
| sessionId, agentNickname, agentRole | `Thread` from `thread/read` | observed-in-generated-types |
| depth, agentPath | `Thread.source` {`subAgent`: {`thread_spawn`: {parent_thread_id, depth, agent_path, agent_nickname, agent_role}}}; `subAgentActivity.agentPath` | observed-in-generated-types |
| spawnedBy | The `spawnAgent` call item (thread, turn, item) | observed-in-generated-types |
| requested model, effort | The `spawnAgent` call item | observed-in-generated-types |
| lastObserved {status, source, time} | Latest of: `agentsStates[child].status` (`pendingInit`, `running`, `interrupted`, `completed`, `errored`, `shutdown`, `notFound`; "Last known status … when available"); `subAgentActivity.kind` (`started`, `interacted`, `interrupted`, `completed`); a child frame (`thread/status/changed` type, or "active (frame observed)"); `Thread.status` from a read | As named in `source` |

### 7.3 Display rules

- **DR-1 Last observed, always sourced.** A descendant shows its last
  observed value with its source and time ("running — from the spawn call's
  agent states, 10:42:07"), never a bare state.
- **DR-2 Parent completion says nothing about children.** A completed
  parent turn changes no descendant (no §13 DS row is triggered by it;
  prototype PC-08). With a child last observed running, the view reads
  "parent turn completed; child last observed running". Completion, return,
  review and integration of a child are never inferred, and the export has
  no element for them (REQ-003).
- **DR-3 Observation ended.** When the generation closes, every observed
  descendant is marked "observation ended", keeping its last value (v3's
  "Observation ended with the parent turn. Later child activity is not
  recorded here" is the pattern, §14.2).
- **DR-4 Task-agent delegation (K-10; SETTLED decision).** When the
  delegating conversation's role is TASK (a runtime value DEL-02-04 hands
  in), the descendant is shown and exported with "delegated by a task agent:
  the task role states that a task agent does not delegate (stated, not
  enforced)". Nothing is blocked and no Codex setting is overridden.
- **DR-5 Roles of children (R17-9).** `agentRole` and `agentNickname` are
  shown as Codex reports them; absent → "role not reported". Whether the
  four Chirality roles reach children through Codex's native agent-role
  configuration, or children inherit the parent's guidance, is DEL-02-04's;
  this view shows only what Codex reports.
- **DR-6 Child controls.** The view offers "interrupt this child's turn"
  only as DEL-01-02's interrupt operation (R17-3 operation 1) with the
  child's thread and turn; whether `turn/interrupt` on a child thread
  behaves as on a primary is **OBS-2 pending** (O-1, O-4). It offers no
  close, resume or message control in this increment (the
  `CollabAgentTool` actions are the agent's).

### 7.4 Observing children (B-6)

Two branches, both designed; which applies is **OBS-2 pending** (O-4:
"what items and notifications a child produces; whether a child thread is
readable"):

- **CO-1** Child frames reach the App on the same connection (frames whose
  `threadId` is a known descendant): applied live (DS-03).
- **CO-2** They do not: the view reads the child on demand (`thread/read`;
  then `thread/turns/list` / `thread/items/list` when the person opens it),
  and while the parent's turn is live it re-reads at most every **TEST
  VALUE** 5 s, only while the delegation view is open. Each read is shown
  "read at <time>". After observation ends, a read restores the child
  (DS-05) with Codex's parent, session, role and depth.

### 7.5 States

The descendant state machine is §13's DS table: `observed`,
`observation-ended`, `not-found` (Codex reported `notFound`).

### 7.6 Fleet seam (B-7)

PKG-06 consumes native delegation identities from this slice (CLM-003;
DEP-01-03-014; DEP-06-01-007). DEL-01-03 exports; it imports nothing from
PKG-06, never shows work-graph, return, waiting or decision state (REQ-007,
R17-10), and adds no fleet feature (TBD-004, OI-006).

### 7.7 The delegation export (PROPOSED)

One record of `npt.delegation-export.schema.json` (beside this file) per
request: export identity, time, producer (DEL-01-03, types pin, observed
version label), root thread, the descendant nodes of §7.2 with
`observationEnded` and `delegatingRole` (K-10), and four fixed limit
statements. `additionalProperties` is false throughout, so no return,
review or integration claim can be carried. Receivers: PKG-06 (DEL-06-01)
and DEL-02-04 (its K-10 account of task-agent delegation, §17 J-7).

---

## 8. Version identity display (REQ-004, AC-004, VER-004)

The view shows three lines, read from the `ready(g)` record (HOSTING §4.6,
§7.1, §7.2); it computes none of them:

| Line | Cases (shown text, PROPOSED) |
|---|---|
| Supplier | `verified` → "Codex <label> · verified (<qualification reference, or 'no qualification reference supplied'>)". `mismatch(<element>)` / `unverifiable(<reason>)` → "Codex not started: <result>" (the child is `refused`, HOSTING LT-05). A development run of an unverified distribution, if the App implementation owner allows one (HOSTING U-06) → "Codex <label> · unverified development run — not the pinned supplier" |
| Types | "Views built from generated types at 0.158.0 (manifest 42b95826…), definition pin, not qualified" and either "the running label matches" or "the running supplier reports <x> — compatibility not verified" |
| Experimental opt-in | "declared" / "not declared" (generation g) |

- **VR-1** "Verified" appears only when §7.2's result is `verified`;
  `unverifiable` is a result, never a pass (HOSTING §4.6).
- **VR-2** At present no pin is qualified (DEP-005; HOSTING §7.1 "expected
  distribution content identity: Not yet recorded"), so a §7.2 `verified`
  cannot occur, and any running supplier today is a U-06 development run.
  The display says so rather than implying qualification.
- **VR-3** Every fixture and result of §15 names the pin, the generated
  output identity and its standing label (REQ-004, REQ-008).

---

## 9. Truthful actor (REQ-005, AC-005, VER-005)

- **TA-1** No act is derived from any native item: tool success, a
  completed plan, elapsed time, a session entry or a turn's end establishes
  no acceptance, check, approval or reliance (prototype PC-07, PC-13).
- **TA-2** An A14 settlement is shown only as a tool-permission settlement
  with the origin the register supplies (TR-3), never as A4–A7 or a
  checkpoint act (HOSTING §11; RS HA-1).
- **TA-3** A person's message ("Approved, I accept") is conversation
  content, never act evidence (RS HA-1; R9).
- **TA-4 Faithful display.** When an act record is handed in whose subject
  is one of this file's anchors (a plan revision, an item; §10.2), the view
  shows it as "<act kind> by <person> (identity not verified) · recorded by
  <recorder>" with content, scope and purpose (K1-4; RS §6.1). A record
  naming the recorder as decision actor is not shown as an act (RS HA-2).
  The record is a runtime value: DEL-04-03 defines it, DEL-01-04 places act
  display (R17-7); DEL-01-03 consumes neither as a production input
  (R17-10). No acceptance-first order is imposed between independently
  evidenced acts.

---

## 10. Interfaces

### 10.1 Consumed

| From | What | Condition of use | When it fails |
|---|---|---|---|
| DEL-01-01 (S-2; DEP-01-03-011) | Native frames with generation and position; `ready(g)` with version identity, verification result and declared capabilities; lifecycle events; generic request path | `ready(g)` received | Not ready → views show the §8 supplier line and no live activity; a request refused `refused-not-sent(not-ready)` changes nothing in the view |
| DEL-01-02 (DEP-01-03-012) | Re-attachment from a position after observer loss; history reads after supplier restart and relaunch; thread and turn execution state; the interrupt operation | §12 SQ-2…SQ-4 | Re-attachment unavailable → re-read from Codex history (plan items; tool items) and mark checklists "not recoverable" (RV-4) |
| Runtime values (no register row; R17-10) | Register state of an item's request (DEL-01-02/01-04); conversation role (DEL-02-04); act records (DEL-04-03 via DEL-01-04); selected model (the composer) | Present when handed | Absent → the element is not shown (no origin, no role note, no act); never guessed |

### 10.2 Offered

| Operation | Receiver | Result | Failure behaviour |
|---|---|---|---|
| plan revisions (thread) | DEL-02-02 (DEP-01-03-013); DEL-04-03 and DEL-01-04 as subjects | `npt.plan-revision` records | Checklist revisions after relaunch: none, with "not recoverable after relaunch" |
| item anchor (thread, turn, item / revision) | DEL-01-04 (request card ↔ row); DEL-04-03 (subject reference) | `npt.item-anchor` record with display state and standing | Unknown item → anchor with `standing` and no display state is refused by the schema (an item anchor needs both) |
| plan-mode element (mode, model, effort) | DEL-01-04 turn composition | The `collaborationMode` value, "not offered (<reason>)" or "run not started — no model selected" | §5.3 |
| delegation export (root thread) | PKG-06 / DEL-06-01 (DEP-06-01-007); DEL-02-04 (K-10 account) | `npt.delegation-export` record | No descendants → empty `nodes`; observation ended → nodes marked |
| fixtures and designed cases | DEL-09-02 (DEP-09-02-011), DEL-09-05 (DEP-09-05-008) | §15 | — |

---

## 11. Data

- **Held, in memory only, per App session:** the derived plan revision
  index, checklist revisions, tool rows, descendant nodes, the last
  `collaborationMode/list`, `model/list` and `experimentalFeature/list`
  results. All are derived from native frames and reads; none is written to
  disk by DEL-01-03 (R17-4).
- **Not held:** any copy of Codex history; any record of which plan was
  "carried out"; any act; any descendant return or integration.
- **Formats handed to receivers (PROPOSED JSON Schema 2020-12, beside this
  file; valid and invalid instance each in `prototype/fixtures/`):**
  `npt.plan-revision.schema.json`, `npt.item-anchor.schema.json`,
  `npt.delegation-export.schema.json`. Names are Chirality's own; Codex
  identities and content are carried as data; placement stays open (R12-2).

---

## 12. Operating sequences, with failure at each step

| ID | Sequence | Steps | Failure at a step → behaviour |
|---|---|---|---|
| SQ-1 | Open a conversation | 1 read `ready(g)` → version line; 2 `thread/turns/list`, `thread/items/list` (page by page) → plan items, tool rows; 3 attach to live frames from the current position | 1 not ready → supplier line only. 2 read error → "history not read (<error>)", retry offered; never an empty plan shown as "no plan". 3 a gap in positions → DEL-01-02 re-attaches; DEL-01-03 never fills a gap |
| SQ-2 | Window close or reload | 1 views discarded; 2 on reopen, re-derive from the host's events of the session from position 0 (DEL-01-02) | Re-attachment unavailable → SQ-1 step 2 and checklists "not recoverable" (RV-4) |
| SQ-3 | Supplier exits mid-item | 1 lifecycle `exited-unexpectedly(g)` → streaming plan items `incomplete`, open tool rows `unknown`, descendants "observation ended", checklists ended; 2 after `ready(g+1)`, DEL-01-02's recovery reads; DEL-01-03 re-reads the turn's items | Frames of the closed generation are refused (H5; prototype PC-04). History lacks the completion → states stay `incomplete` / `unknown` |
| SQ-4 | Relaunch | 1 nothing of DEL-01-03 survives; 2 SQ-1 against the threads DEL-01-02 lists | Checklist revisions of earlier turns: "not recoverable after relaunch"; descendants: from `thread/read` only |
| SQ-5 | Pin mismatch | `refused` → "Codex not started: mismatch(<element>)"; no views | — |
| SQ-6 | Opt-in absent | Plan-mode control absent; everything stable renders (EX-3) | — |
| SQ-7 | Plan-mode turn | 1 `collaborationMode/list` at `ready(g)` (receiver:DEL-01-03); 2 the person chooses Plan; 3 DEL-01-04 sends `turn/start` with the element (§5.4) | 1 error → control absent "plan presets not read". 2 no model → "run not started — no model selected". 3 error response → shown; nothing recorded as a plan |
| SQ-8 | Delegated work | 1 spawn call → node; 2 CO-1 or CO-2; 3 parent turn completes → no descendant change | 2 read error → "child not read (<error>)"; last observed value kept |

---

## 13. Transition tables (PROPOSED; R17-1)

Every row is exercised by the prototype (PC-15), which also checks that these
tables equal the model's. Any transition not listed is refused.

**Plan item** (one per `plan` item):

| ID | From | Event | To | Shown |
|---|---|---|---|---|
| PL-01 | `absent` | item-started | `streaming` | Preview |
| PL-02 | `absent` | plan-delta | `streaming` | Preview; "start not observed" |
| PL-03 | `streaming` | plan-delta | `streaming` | Preview grows |
| PL-04 | `streaming` | item-completed | `completed` | Revision n (RV-1); preview replaced |
| PL-05 | `absent` | item-completed | `completed` | Revision n |
| PL-06 | `streaming` | turn-ended | `incomplete` | "incomplete — not completed when observation ended" |
| PL-07 | `streaming` | generation-closed | `incomplete` | As PL-06 |
| PL-08 | `absent` | history-read | `completed` | Revision, "recovered from Codex history" |
| PL-09 | `incomplete` | history-read | `completed` | As PL-08 |
| PL-10 | `completed` | history-read | `completed` | Consistency check; a difference is shown |

**Checklist** (one per thread and turn):

| ID | From | Event | To | Shown |
|---|---|---|---|---|
| CL-01 | `none` | plan-updated | `live` | Revision 1 (RV-2) |
| CL-02 | `live` | plan-updated | `live` | Revision n+1 |
| CL-03 | `live` | turn-ended | `ended` | Last revision is the turn's final checklist |
| CL-04 | `ended` | plan-updated | `ended` | Revision marked "after turn end" |
| CL-05 | `live` | generation-closed | `ended` | "observation ended" |
| CL-06 | `none` | history-read | `not-recoverable` | "Checklist updates are not kept in Codex history; not recoverable after relaunch" |

**Tool row** (one per tool item; "final" means the display state of the
native status, §6.1):

| ID | From | Event | To | Shown |
|---|---|---|---|---|
| TI-01 | `absent` | item-started | `in-progress` | Row |
| TI-02 | `in-progress` | request-outstanding | `waiting-on-request` | Link to the request card (TR-6) |
| TI-03 | `waiting-on-request` | request-settled | `in-progress` | Settlement origin as supplied (TR-3) |
| TI-04 | `in-progress` | item-completed | `final` | Native status; result or "not supplied" (TR-4) |
| TI-05 | `waiting-on-request` | item-completed | `final` | As TI-04; no origin unless supplied |
| TI-06 | `absent` | item-completed | `final` | As TI-04 |
| TI-07 | `in-progress` | turn-ended | `unknown` | "no completion observed" |
| TI-08 | `waiting-on-request` | turn-ended | `unknown` | As TI-07 |
| TI-09 | `in-progress` | generation-closed | `unknown` | As TI-07 |
| TI-10 | `waiting-on-request` | generation-closed | `unknown` | As TI-07 |
| TI-11 | `absent` | history-read | `final` | "recovered from Codex history" |
| TI-12 | `unknown` | history-read | `final` | As TI-11 |
| TI-13 | `absent` | history-read-in-progress | `unknown` | "in progress at the read" or "turn ended without a completion" |

**Descendant** (one per child thread; a parent's turn end is deliberately
not an event of this table, DR-2):

| ID | From | Event | To | Shown |
|---|---|---|---|---|
| DS-01 | `absent` | collab-call | `observed` | Node from the call item |
| DS-02 | `absent` | subagent-activity | `observed` | Node; parent by inference (labelled) |
| DS-03 | `observed` | child-observation | `observed` | Last observed updated |
| DS-04 | `observed` | generation-closed | `observation-ended` | "observation ended" (DR-3) |
| DS-05 | `observation-ended` | thread-read | `observed` | "read at <time>" |
| DS-06 | `observed` | not-found-reported | `not-found` | Codex's `notFound` as reported |
| DS-07 | `absent` | thread-read | `observed` | Node from `Thread` (parent, session, role, depth) |
| DS-08 | `observation-ended` | child-observation | `observed` | Observation resumed |
| DS-09 | `observed` | thread-read | `observed` | Read values merged, sourced |

---

## 14. Feature and optional-reuse map (OUT-003; REQ-006, AC-006, VER-006)

### 14.1 Features, owners and basis

| Feature | Required behaviour (source) | Supplying / receiving owners | Native basis at 0.158.0 | Open matter |
|---|---|---|---|---|
| Plan view: plan items and revisions | REQ-001, SOW-003/128 | DEL-01-01 supplies (S-2); DEL-02-02 receives (§5.6) | `plan`, `item/plan/delta`, history reads | U-P1 (never observed live) |
| Plan view: checklist | REQ-001 | As above | `turn/plan/updated` | Not recoverable after relaunch (R17-4) |
| Plan mode control and element | REQ-001, SOW-129; K-5 | DEL-01-04 composes and sends | `collaborationMode` (exp), `collaborationMode/list` (exp) | U-P2, U-P3 (F-3) |
| Tool activity rows | REQ-002, SOW-004/014 | DEL-01-04 (cards, A14); DEL-01-02 (state) | Part A item kinds | U-19 (MCP items unobserved, OB-1) |
| Delegation view and export | REQ-003, SOW-006; K-10 | PKG-06/DEL-06-01 and DEL-02-04 receive | `collabAgentToolCall`, `subAgentActivity`, `Thread` | OBS-2 O-4; F-1 |
| Version line | REQ-004, SOW-128 | DEL-01-01 supplies; qualification is the App implementation owner's (OI-012) | §7.1 record | U-06; DEP-005 |
| Truthful-actor display | REQ-005 | Act records DEL-04-03; placement DEL-01-04 | — | — |
| Fixtures and cases | REQ-008 | DEL-09-02/09-05 receive | Constructed from types now; recorded later | OI-015 resolved by source; candidate needed |
| Registry storage, checker | SOW-128 "remain design choices" (TBD-002) | — | — | None selected; R17-4 makes a registry unnecessary for plan items |

### 14.2 v3 exemplar, assessed as reuse candidates only (evidence, never a v4 commitment)

File identities are sha256 prefixes computed at this node.

| v3 source (historical) | What it did | Assessment against this contract |
|---|---|---|
| `chirality-runtime/packages/core/src/native-plan-registry.ts` (35825fdaf339cc57) | Admission- and qualification-gated "native Plan adapter" that "persists completed plan items"; revision = per-session ordinal with its source event | **Not reused.** Persisting plan items is a Chirality copy (R17-4); the Runtime service and its admission model are excluded (V4-ARC-03); the ordinal idea survives as RV-1's ordinal derived from history |
| `chirality-app-dev/frontend/src/components/shell/native-plan-panel.tsx` (1983f82da6a62c5f) | Plan tab: revisions, clarifications, plan-mode flag, export status, execution record | **Layout reference only.** Its data came through the excluded translated stream |
| `chirality-app-dev/frontend/src/lib/harness/plan-executions.ts` (221b8f9bbf6f2388) | Kept "which plan revision was sent for execution" in local storage | **Not reused** (R17-4; §5.3 reads the order from history) |
| `…/components/shell/tool-stream-view.tsx` (bcd08e4c01e7350e), `subagent-stream-view.tsx` (479a15366dcca2b9) | Rows from `lib/shell/harness-event-views.ts` (d750848e05042820), which reads the bridged `HarnessEvent` stream | **Patterns only**: status badges, "last observed", "Observation ended with the parent turn". The translated vocabulary is excluded (V4-APP-04, A5) |

No source similarity or historical pass qualifies reuse (REQ-006); any later
reuse is checked against this file's cases on a candidate.

---

## 15. Fixtures and verification (OUT-002; REQ-008)

### 15.1 Fixture method

- Fixtures are native frames and read results, labelled with HOSTING §9.2
  standing: `constructed` now (from the generated 0.158.0 types, validated
  against the committed bundle), `recorded` / `recorded-truncated` /
  `mutated` once captures exist (HOSTING §9.1: X-03 plan revision, X-09/X-10
  exit and restart, and a delegation capture). Each fixture names the pin,
  the generated-output identity and its scenario. Invented material only
  (V4-CST-06); no fixture act is a real decision (VER-005).
- Interface examination covers WebKit and Chromium and the packaged App
  smoke witness (REQ-008, V4-EXM-03); outcome labels `pass`, `fail`,
  `blocked`, `not-run`, `inconclusive`, bound to candidate, configuration
  and date. None can run before a candidate exists.

### 15.2 Designed cases

| Case | Serves | Setup | Expected | Runnable now? |
|---|---|---|---|---|
| NV-01 Plan revisions | VER-001, AC-001 | Recorded X-03 at the pin; then relaunch | Displayed sequence equals the source items; plan items recovered from history with the same identities; checklists "not recoverable after relaunch" | Model only (PC-02…PC-05); live needs a capture |
| NV-02 Plan-mode interaction | VER-001 | Opt-in declared; plan preset | PS-1…PS-5 as specified; no model → refusal; no act recorded for "carry out" | Model only (PC-12) |
| NV-03 Tool outcomes | VER-002, AC-002 | Recorded command, file change, MCP and dynamic tool items, incl. failure, decline and no result | Native values unchanged; `unknown` where no completion; "result not supplied" where Codex gave none; no renaming in the presentation path | Model only (PC-06, PC-07); MCP items unobserved on the local route (OB-1) |
| NV-04 Primary completed, descendant active | VER-003, AC-003 | Delegation capture (OBS-2 O-4) | Parent completed; child last observed running, sourced; export without return/review/integration | Model only (PC-08, PC-09); **OBS-2 pending** |
| NV-05 Task-agent delegation | VER-003; K-10 | Task-role conversation that delegates | Shown and exported "stated, not enforced"; not blocked | Model only (PC-10) |
| NV-06 Version identity | VER-004, AC-004 | `ready(g)` variants: development run, label differs, mismatch, verified | Lines as §8; "verified" only from a verified result | Model only (PC-11) |
| NV-07 Truthful actor | VER-005, AC-005 | (a) tool success, no act; (b) a message "Approved"; (c) a supplied act record | (a),(b) no act; (c) actor ≠ recorder, "identity not verified" | Model only (PC-07, PC-13) |
| NV-08 Map review | VER-006, AC-006 | §14 against the ScopeOfWork, CLM-001…004, issue rows | Each exclusion traced to its owner (§16) | Review only |
| NV-09 Fixture provenance | VER-007, AC-007 | §15.1 records | Pin, output identity, standing, candidate/date/outcome present; no joined-journey claim | Review only |

### 15.3 Prototype (R17-1; R12-3)

`prototype/` holds a Python 3 standard-library model of this file's rules
(`npt_model.py`), constructed scenarios (`scenarios.py`; written out as
`fixtures/native/*.jsonl`), the schema fixtures, a copy of DEL-01-01's
`jsonschema_subset.py` (byte-identical, sha256 486e9286…c0ffc0) and
`run_cases.py`. It reads the committed 0.158.0 bundle of DEL-01-01 and
writes nothing outside its folder. It is not product code and not an App
candidate.

**Run of 2026-10-01** (`python3 run_cases.py` in `Design/prototype/`; output
in `prototype/results/RUN_2026-10-01.txt`): 15/15 cases gave their expected
result (PC-01 bundle conformance of every constructed frame and read; PC-02
…PC-05 plans; PC-06, PC-07 tools; PC-08…PC-10 delegation; PC-11 version;
PC-12 experimental surfaces and plan mode; PC-13 truthful actor; PC-14
schema fixtures; PC-15 every row of §13 reached and the tables equal to the
model's). A pass shows that the rules run as written against constructed
frames; it passes no VER criterion.

---

## 16. Act and owner boundary (REQ-007)

| Act or production | Owner | This file |
|---|---|---|
| Codex process, handshake, frames, register, version verification | DEL-01-01 | Consumes S-2 |
| Custody, re-attachment, recovery, interrupt, stop, quit (R17-3) | DEL-01-02 | Consumes; offers DR-6's child interrupt only through DEL-01-02 |
| Request cards and answers (A14), turn outcome, messages, attachments, act control and act display placement (R17-6, R17-7) | DEL-01-04 | Offers anchors and the plan-mode element |
| Account, provider and model selection (K-3) | DEL-01-05 | Takes the selected model as a runtime value |
| Workflow-making journey, drafts, registration (A15) | DEL-02-02 | Offers plan-revision references |
| Role supply, task-role limit account (K-10), child roles (R17-9) | DEL-02-04 | Shows roles as reported; offers the export |
| Records and their format | DEL-04-03 | Shows supplied records (TA-4); writes none |
| Fleet graph, returns, waiting, decisions | PKG-06 | Exports identities only |
| Reserved acts A4–A7, A12, A13; professional reliance | The person (D2) | Performs, infers and decides none |
| Agent engine, credentials, protocol | OpenAI Codex | Consumes as published; no second engine (CLM-001) |

### 16.3 Register rows proposed (R17-10; checked over DAG-003)

Reachability computed over `DependencyEdges.csv` and `CandidateEdges.csv`
(consumer → supplier): DEL-01-03 reaches only DEL-01-01, DEL-01-02, DEL-01-05
and DEL-04-01; DEL-01-04, DEL-02-02, DEL-02-04, DEL-04-03 and DEL-06-01 all
already reach DEL-01-03. So:

- **DEL-01-04 consumes DEL-01-03** (INTERFACE: item anchors, plan-mode
  element). SCC-neutral (DEL-01-03 does not reach DEL-01-04).
- **DEL-02-04 consumes DEL-01-03** (INTERFACE: the delegation export for the
  K-10 account; child roles as reported). SCC-neutral.
- Deliverable-level mirror rows for DEP-06-01-007, DEP-09-02-011 and
  DEP-09-05-008 in this register (DOWNSTREAM). SCC-neutral (mirrors).
- **Not proposed, by design:** DEL-01-03 consuming DEL-01-04, DEL-02-02,
  DEL-02-04, DEL-04-03 or DEL-06-01. Each would form an SCC; what DEL-01-03
  shows of them is a runtime value (§10.1).

---

## 17. Joins for node F (first-increment files; R17-14)

| ID | File, section | Now | Needed |
|---|---|---|---|
| J-1 | HOSTING §4.2 step 4; U-21; F-13 | Declared capabilities recorded; the opt-in is "required to use plan mode" | Record that under K-5 the App declares `experimentalApi` true, and that DEL-01-03 reads the declared value per generation (EX-2) |
| J-2 | HOSTING §8.4, HCG-A08 availability signal | "`multiAgentMode` on thread and turn start (experimental-only)" | `multiAgentMode` is deprecated: ignored on requests, always `explicitRequestOnly` in responses (generated descriptions). Name `Model.multiAgentVersion` (stable, `model/list`) as the signal; the Codex feature gate is OBS-2 pending (F-1) |
| J-3 | HOSTING §4.6 "observe lifecycle" / §5 Order (realization DEL-01-02's) | Events "kept and re-read from a position" | State, with DEL-01-02, whether closed-generation events of the same App session stay re-readable (RV-4); DEL-01-03 needs it only for checklists |
| J-4 | HOSTING VC-09 | "revision identity left to DEL-01-03" | Cite NPTD §5.2 RV-1, RV-2 as the derivation |
| J-5 | EXEC §3.4 EV-3a, row `agent-delegation` | Present when the thread start reports a `multiAgentMode` | The element is constant when present, so the reading carries no information; use `Model.multiAgentVersion` (`disabled` → missing; `v1`/`v2` → present; null → not read), pending J-2 |
| J-6 | WD §4.2.5 row `agent-delegation` | "`multiAgentMode` on thread and turn start is experimental-only" | Add "and deprecated (ignored)"; the item kinds are stable, so delegation needs no opt-in to be seen |
| J-7 | (DEL-02-04, parallel node D6) | — | (a) plan mode's `collaborationMode` "takes precedence over … developer instructions": role and workflow supply may be set aside on plan-mode turns (F-3); (b) the delegation export carries `delegatingRole` for the K-10 account; (c) children's `agentRole` is shown as reported (R17-9) |
| J-8 | (DEL-01-02, parallel node D1) | — | DEL-01-03 needs: re-attachment from a position (SQ-2), the list of threads after relaunch (SQ-4), the interrupt operation usable on a child thread (DR-6), and the register state of an item's request as a runtime value (TI-02/03) |
| J-9 | (DEL-01-04, parallel node D3) | — | Item anchors on request cards (TR-6); the plan-mode element in turn composition (§5.4); act display of TA-4 placed by DEL-01-04 |

---

## Findings

- **F-1 `multiAgentMode` is not a delegation signal at 0.158.0.** Its
  generated descriptions say it is ignored on requests and always
  `explicitRequestOnly` in responses; HOSTING §8.4 and EXEC EV-3a use it as
  the availability signal (J-2, J-5, J-6).
- **F-2 Delegation is not experimental at the protocol level.** The
  delegation item kinds and the `Thread` child fields are stable. K-5's
  premise ("plan mode and delegation views need an experimental Codex
  setting") holds for plan mode only. The decision's rule ("labelled where
  they appear") is kept through EX-1 (b); for owner visibility, not a
  re-decision.
- **F-3 Plan mode may set aside supplied guidance.** `collaborationMode`
  "Takes precedence over model, reasoning_effort, and developer
  instructions if set" (generated description). Not observed (U-P3).
- **F-4 Plan mode needs a model.** `Settings.model` is required, so a
  plan-mode turn always names the conversation's selected model; it fits
  K-3 (no model chosen until the person chooses).
- **F-5 Checklists are not in history** (`TurnPlanStep` only in the
  notification); R17-4 settles the consequence (RV-4).
- **F-6 A child's depth and spawn source come only from a read**
  (`Thread.source` `subAgent.thread_spawn`).

## UNRESOLVED

| Item | Owner | Point of need | Effect here |
|---|---|---|---|
| U-P1 Plan item and checklist never observed live; which mode produces which | App implementation owner (a later observation; not in OBS-2's O-1…O-7) | Before plan fixtures are recorded (X-03) | §5.1 rests on the types |
| U-P2 Whether `collaborationMode` persists across turns | As U-P1 | Before implementing PS-5 | PS-5 always sends the mode explicitly |
| U-P3 Whether plan mode replaces or adds to the thread's developer instructions (F-3) | DEL-02-04 with the App implementation owner (observation) | Before plan mode is offered with role supply | Warning shown on the control |
| U-P4 Codex feature names that gate delegation and plan mode; whether child frames reach the App; `turn/interrupt` on a child | OBS-2 (O-4, O-1) | Round 2 of this pass | EX-1 (b) labels nothing; CO-1/CO-2 both designed; DR-6 PROPOSED |
| U-P5 CO-2 re-read interval (TEST VALUE 5 s) | App implementation owner | Before implementation | Value open |
| U-P6 Content-identity method (HOSTING U-08) | App implementation owner with DEL-04-03 | Before records cite plan revisions | TEST VALUE |
| U-P7 OI-008 placement | App implementation owner (phase review) | Before allocation | §1 PROPOSED under O-1 |
| HOSTING U-06 Development run of an unverified distribution | App implementation owner | Before implementation | §8 supplier line covers it |

## Verification cases

The designed cases are §15.2 (NV-01…NV-09); the prototype cases are PC-01…
PC-15 (§15.3). No case passes a VER criterion before an App candidate exists.
