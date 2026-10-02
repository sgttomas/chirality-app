# Native plans, tools and delegation views
- Contribution: DEL-01-03/NPTD-v0.2 (supersedes DEL-01-03/NPTD-v0.1, committed at `63a6e0fa47` and unchanged since, file sha256 a3b36a454d497e28b0cf0bc3edb17d018f6f724cce0270157ed65c4e1e63ef59)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Run and node: `APP-V4-DESIGN-PASS-3-20261001`, node D2 (Type 2 TASK, Claude Opus 5.5, high effort): round 1 written 2026-10-01; round 2 (this version) 2026-10-02
- **v0.2 inputs (round 2; sha256 recomputed with `shasum -a 256` at this node; run folder `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/`):** `BRIEFS.md` 316ea29325a0d45004ffd59c1b142d2e9f5c371ac765bce7c4b94898a57788d7 ("D round 2"); `R18_RESOLUTIONS.md` abf5eee6324647ff9f126603ff189a21f847d5887f20e24e540fd9a6b4c0bd30 (R18-1 C-03…C-08; R18-4; R18-7 G-3, G-4; R18-9); `R19_RESOLUTIONS.md` 16930ecdcead75118ee264bc78d3a7c4824212323cb9895b9a3c15478122a12c (R19-2, R19-5, R19-7); `OWNER_DECISIONS.md` ea96c55710af41c94afe3721f8881bf5edc5bbfc9ad4d0d9ff68e20ca808e015 (DECISION-L); `F/F0_JOINS.md` e93608be1c6e3eb03e6194f3c6f415e3171492f9828b0fd80b4dccb81fe47dd9 (§2, §6, §7.2); `DEL-01-01/Design/OBS_2_0.158.0.md` 61cc34ffb811eb270542042ce4cfdc195efb0c5be4b89dbbe73eb9b99e104ac0 (O-1, O-2, O-4/O-4a/O-4b, O-5b, O-8); `DEL-01-01/Design/OBS_3_0.158.0.md` 554ac4451d11282450e3ec4a4192448adf67bda6a07820f84a698716c806a843 (W-5, W-6); DEL-02-04 `ROLE_SUPPLY.md` (ROLE-v0.1 §6.2 LA-1/LA-2, §6.3 DL-4, §7.2 O-6; read for the K-10 label as handed). Generated types: `ModelProviderCapabilitiesReadResponse`, `Model.multiAgentVersion`, `ThreadGoal*` read at 0.158.0 (stable and experimental variants equal for the goal types).
- **Round-1 header (v0.1), kept as written:**
  - Phase (V4-WF-05 as amended by SCA-V4-001; R8-1; R9-1): Phase 1. No App run holds at a checkpoint; nothing here makes a hold claim.
  - Serves: OUT-001 (view definitions: §3–§9, §12, §13), OUT-002 (fixture method and designed cases: §15), OUT-003 (feature and optional-reuse map: §14); REQ-001…REQ-008; designed cases for VER-001…VER-007.
  - Basis (accepted, as amended by SCA-V4-001 and SCA-V4-002; sha256 recomputed with `shasum -a 256` at this node): `docs/PRD.md` bb6e786f7a6c01dc5ce2f16f58e6c600989a12808ff47ce4fd87924bcc6c49bd (V4-APP-01/04, V4-EXE-01…03, V4-AUT-01…05, V4-REC-03/05); `docs/ARCHITECTURE.md` 317d5789272c5206599936fa9b4e68551b30016d226b88039f0153afa02d828c (M-2, M-7, §3 V4-ARC-01/05 and its properties, "rather than a Chirality copy"); `docs/HOST_INTEGRATION.md` d4331c39db7f452cd3ba72fdfa4bad540a6053931218359a93646971acb28d9f (§1, V4-HI-30…33); `docs/EXAMINATION.md` 471798bc2f2dc0202ae40d9d5cf033a22ae41af2a0afdf58032cf37a687957d0 (V4-EXM-01…05, 10, 11, 13). The deliverable's `ScopeOfWork.md` b5d533cb3dbea97b37950792ad2c68f42bf6023effa4ac894209a1ef3fc605f2 (INIT contract, unrevised by either amendment) and `Dependencies.csv` 9ac820166dd07dde8bbad59ba1c2b0818ab7f4ff4b435c6991cc2d887ddeedf4. DAG-003 (`_DAG/DAG-003/`), cited for arc layers.
  - Owner and integrator records (run folder `_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/`): `OWNER_DECISIONS.md` 9d18c40dd7d894dc20b9edd2803dc6ab63f1deeadb79919411ea71f2ef248b1b (DECISION-K3 as revised: K-5, K-10 bind here; K-3 bears on plan mode); `R17_RESOLUTIONS.md` b0af81bcbad9bc52fddc99119c42a19019a9b174677d5b92a0a2f5c8b4f8e198 (R17-1, -2, -4, -5, -9, -10, -13, -14, -15); `BRIEFS.md` b261394112d7264ef0b87ced64a513eccf0cb41dc96c8dfc8ec955ca62fb05c1 ("Common rules", "D — design nodes, round 1", row D2); `DECISIONS_PENDING.md` 431ec4eb22a0b91323b2f33118c6820527fa9effc85de9e847a221a9023fdd86 (the K-5 and K-10 option texts DECISION-K3 accepted); `SURVEY/S1-A.md` 8f021191f20e4a7e1e6b51fdcfb729bb9a562f3e4c6dd7144be937d77151e8ca (Part 2, §3.1, §3.2). Earlier owner records and rulings R1–R16 stand as the common rules say; DECISION-K1 K1-4 ("identity not verified") applies (§9).
  - First-increment Design files read (cited by label and section; none edited, R17-14): DEL-01-01/HOSTING-BOUNDARY-v0.8 `HOSTING_BOUNDARY.md` 3cf0381c42358fec4a2088ab3886e14b66d6d2020482c72e195fda068a6d78b1 (§3 H4–H7, H10; §4.2, §4.6; §5, §5.1; §7.1–§7.3; §8 S-2; §8.4; §9.2; §10.1; §11; §12; F-12, F-13, F-15; U-06, U-08, U-19, U-21; VC-09); DEL-01-01/PIN-SPIKE-v0.1 `PIN_SPIKE_0.158.0.md` 0e090a4ca14e3ec323e8302ea4bc4e1fefc66bee50d0d3247e1cd0ddc04eb115 (P-10, P-13, P-15, S-F-13); `OBS_1_0.158.0.md` 7b984b541edca0b14534d29115e77642c587a32f830bdf25a94a7ecca882cc43 (O-5, O-6; OBS-1b OB-2, OB-3 as HOSTING §10.1 states them); DEL-02-01/WD-v0.8 `WORKFLOW_DECLARATION.md` 517821d18fc958301d3adaeb63caf11ab50f7e1ca3ec5a644a3bb4ec78b25b0e (§4.2.5 `plan-update`, `agent-delegation`, HC-3, HC-4); DEL-02-03/EXEC-v0.6 `EXECUTION_COMPATIBILITY.md` 64e732d502d0b91da00e62069be1b77b61d1e84986b3744bc117b6e67524fa38 (EV-3a rows `agent-delegation`, `plan-update`); DEL-04-03/RS-v0.8 `RECORD_SEMANTICS.md` b25cc90e9e252f50f30fcaed7faf230ec7bbf4689dcc2cd90deb35c7dcf7f47b (§6.1 decision actor and recorder, §6.2 HA-1, HA-2; §10).
  - Supplier evidence: the committed 0.158.0 JSON Schema bundle `DEL-01-01/Design/generated/0.158.0/json-schema/experimental/codex_app_server_protocol.v2.schemas.json` (sha256 34f28a486d00fbd20e5da0b0da3422d1d6e20ec897d12b31408f87499198f458), and the generated TS output in the session scratchpad (`…/scratchpad/codex-0.158.0/gen/ts-{stable,experimental}/run1/`, read only). The 34 TS files this file cites were checked against `generated/0.158.0/MANIFEST.sha256` (42b95826…69e): 34/34 equal (experimental variant), and the stable `ThreadItem.ts`, `Thread.ts`, `Model.ts`, `TurnPlanUpdatedNotification.ts` equal too. The Codex binary was not run; no model was run; no network was used.
  - App v3 exemplar (`projects/chirality-app-dev`, `projects/chirality-runtime`): evidence of what was built before, never a v4 commitment (§14.2).
  - Receivers (from the live register rows; layer per DAG-003): DEL-02-02 via DEP-01-03-013 (admitted; mirror DEP-02-02-012): the plan-revision reference (§5.6); PKG-06 via DEP-01-03-014 (package target, not topological) and DEL-06-01 via its own DEP-06-01-007 (admitted): the delegation export (§7.7); DEL-09-02 via DEP-09-02-011 and DEL-09-05 via DEP-09-05-008 (both admitted): fixtures, designed cases and the descendant presentation (§15). Offered without a register row (proposed in the return, §16.3): DEL-01-04 (item anchors, plan-mode element) and DEL-02-04 (the delegation export for its K-10 limit account). Suppliers: DEL-01-01 via DEP-01-03-011 (admitted) and DEL-01-02 via DEP-01-03-012 (admitted).
- **Receivers at v0.2:** as above, except that DEL-02-04 is no longer a receiver of the delegation export (R18-1 C-07: its K-10 label is a runtime value handed to this file), and the offered row DEL-01-04 → DEL-01-03 is adopted (R18-1 C-06; F0 NR-05).

**ScopeOfWork reading (R17-15).** The INIT contract lags later decisions in
four places. This file reads it as follows, and the return lists a precise
proposal for each: (1) TBD-001's "selected supplier pin … remains with the
App implementation owner (OI-012)" is read with owner decision D4: 0.158.0 is
the definition and generation pin, not a qualification, so REQ-004's display
says so (§8); DECISION-L L-7 makes the Owner also the App implementation
owner. (2) CLM-004, AX-002 and TBD-003 "OI-001/002 remain open" are read
with D2 and D3. (3) REQ-005's "faithfully display" is read with DECISION-K1
K1-4: an App-captured act names the person "identity not verified". (4)
REQ-001's plan revisions are read with R17-4 and R18-1 C-03: checklist
revisions that Codex does not keep are not copied, and after a relaunch or a
supplier restart they are shown "not recoverable"; plan-item revisions are
recovered from Codex history. K-5 (only plan mode is experimental, R18-1
C-05) and K-10 (task-agent delegation shown with the standing DEL-02-04
hands, C-08) are applied as ruled.

**Reading note.** Labels: **SETTLED**, **DERIVED**, **INTEGRATION**,
**PROPOSED** as R9. Supplier facts carry R17-13's standing labels:
`observed` (live in the spike, OBS-1, OBS-2 or OBS-3), `observed through an
adapter (OBS-2), not stock behaviour` (R18-9: O-4, O-4a, O-4b),
`observed-in-generated-types`, `inference`. Every supplier fact names Codex
0.158.0 (R19-5; §18). Supplier names are quoted; everything else is this
file's semantic naming.

## Changes from v0.1

| Ruling / item | Change | Where |
|---|---|---|
| R18-1 **C-03** | A closed generation's events are not re-readable; after a supplier restart the views rebuild from Codex history, and the closed generation's checklist revisions are "not recoverable", as after a relaunch. New row CL-07. J-3 withdrawn | §2, §5.2 RV-4, §12 SQ-3, §13 CL-07, §17 |
| R18-1 **C-04** | Delegation availability = `Model.multiAgentVersion` ≠ `disabled` **and** the provider accepts `namespace` tools (`modelProvider/capabilities/read` → `namespaceTools`); an effective `features.multi_agent = false` reads missing. Read at run time (R19-5) | §7.1; prototype PC-16 |
| R18-1 **C-05** | Only plan mode is labelled "experimental"; delegation is stable and never labelled. EX-1 (b) removed | §4 |
| R18-1 **C-06** | DEL-01-04 composes `collaborationMode` on `turn/start` from this file's plan-mode element and sends the default mode explicitly to leave plan mode; the row DEL-01-04 → DEL-01-03 is adopted | §5.3, §5.4, §10.2, §16.3 |
| R18-1 **C-07** | Row DEL-02-04 → DEL-01-03 dropped; the K-10 label is a runtime value from DEL-02-04 (ROLE O-6) | §7.3 DR-4, §7.7, §10, §16.3 |
| R18-1 **C-08** | The export carries the K-10 standing as handed: `stated-not-enforced` · `enforced-by-supplier` · `unknown` (schema changed) | §7.3 DR-4, §7.7; `npt.delegation-export.schema.json` |
| R18-4 | A role-configured child receives its role file's developer instructions, not the parent's (O-4a, through the adapter); a child spawned without a role type: guidance unknown | §7.3 DR-5 |
| R18-7 **G-3** | Codex's goal surface (`get_goal`, `create_goal`, `update_goal` model tools; `thread/goal/updated`, `thread/goal/cleared`, `thread/goal/get`) shown as a native group without translation | §3, §6.4, §9 TA-5; PC-17 |
| R18-7 **G-4** | An item opened and never completed settles "not completed (turn ended)" at turn end: new display state `not-completed`; TI-07/TI-08 changed; TI-14, TI-15 added (schema enum changed) | §6.1, §13; `npt.item-anchor.schema.json` |
| OBS-2 O-8 | Plan mode yields one `plan` item (id `<turnId>-plan`) by `item/plan/delta`, no agentMessage, no `turn/plan/updated`, no `update_plan` tool; plan mode persists until the default mode is sent | §5.1, §5.3; U-P1 narrowed, U-P2 closed |
| OBS-2 O-4 (adapter), O-8 | Feature names filled: delegation gated by stable `multi_agent` (default on) and `multi_agent_v2` (off); plan mode by no listed flag; child frames reach the App on the same connection, no `thread/started` for a child; children absent from `thread/list`; delegation absent on stock LM Studio 0.4.16 | §4, §7.1, §7.2, §7.4, §12 |
| OBS-2 O-5b, OBS-3 W-5 | `collaborationMode.settings.developer_instructions` non-null **replaces** the mode's built-in text and is added beside the thread's developer text; the plan-mode element keeps it null | §5.3 F-3 paragraph; U-P3 narrowed |
| R19-2 | Run boundaries: the views draw none; they show the run in force at a turn from run markers handed in, display only | §5.7; PC-18 |
| R19-5 | Version dependence listed; capabilities read at run time | §18 |
| U-P5 | Closed: no polling; children are read on demand (CO-1 holds) | §7.4 |
| RV21 (repairs from V21; in place, no version step) | **R21-1** (V21-B M-1; HELP_HUMAN's RV21 note): §7.1 states the reading order R21-1 rules and names this section the reference; the prototype now reads a configuration that was never read as *not established* (v0.2's code read it as "nothing set" and answered *present*), PC-16 gains that case, an ordering case and a check of all 64 signal combinations against R21-1. **V21-A MINOR 14:** the `$id`s of the two schemas v0.2 changed are bumped to `…:v0.2` (`npt.item-anchor`: state `not-completed`; `npt.delegation-export`: three-value standing); `npt.plan-revision` is unchanged and stays `…:v0.1`. Rerun 18/18 | §7.1; §11; §15.3; two schemas; `prototype/npt_model.py`, `prototype/run_cases.py` |

---

## 1. What this deliverable is, and where it sits

DEL-01-03 presents Codex's own plans, tool activity, goals and delegation in
the App, and offers the plan interactions the person uses to direct work
(SOW-003, SOW-004, SOW-006, SOW-014, SOW-128, SOW-129). It renders native
items, never a translated Chirality event vocabulary (V4-APP-04, V4-ARC-05,
CLM-001; HOSTING H6). It does not start the Codex process, hold the request
register, compose or send turns, answer requests, keep records or perform
any act (§16).

**Placement (PROPOSED under R17-5; OI-008 option O-1, which the phase review
owns).** The Rust host owns the Codex process, the frame exchange, the
request register and record writing (HOSTING §1, §12 O-1). DEL-01-03's views
live in the interface: they compose and present native frames the host
delivers with generation and receipt position beside each frame (HOSTING H6,
§5 Order), plus reads made through the host's generic request path (HOSTING
§5.1). The view state is derived and in memory only; DEL-01-03 keeps no file
and no copy of Codex history (R17-4, ARCH §3).

```text
 Interface: DEL-01-03 views ── plan view · tool activity · goal line · delegation view · version line
     ▲ native frames + (generation, position)      ▲ runtime values handed in (not production inputs):
     │ reads via the generic request path           │  register state of an item's request (DEL-01-02/01-04),
     │ ready(g) record, lifecycle events            │  K-10 limit label (DEL-02-04), run markers (DEL-02-03),
 Host (Rust): DEL-01-01 boundary + DEL-01-02       │  act records (DEL-04-03 via DEL-01-04's placement),
     custody, re-attachment, recovery reads         │  selected model (DEL-01-04's composer)
     │ published JSON-RPC over stdio
 stock Codex App Server 0.158.0 (definition pin)
```

---

## 2. Receiving comparison of seam S-2 (closes HOSTING F-15 for S-2)

| S-2 element (HOSTING §8) | How DEL-01-03 uses it | Standing |
|---|---|---|
| Version identity record with each `ready(g)` (§7.1) and the verification result (§7.2) | Version line (§8); fixture binding (§15.1) | Accepted as supplied |
| Native plan items and plan updates "unchanged with generation and receipt position" | Plan revisions (§5): checklist revision identity is derived from generation and receipt position | Accepted. Within a generation, re-attachment by position is DEL-01-02's; after a generation closes the views rebuild from Codex history (R18-1 C-03), so S-2 needs nothing further |
| Generic request path (§5.1) | `collaborationMode/list`, `model/list`, `modelProvider/capabilities/read`, `config/read`, `thread/goal/get`, thread reads; initiator `receiver:DEL-01-03`. Turns are sent by DEL-01-04 (`person-directed`) | Accepted |
| Declared capabilities with `ready(g)` (§4.2 step 4) | Whether the experimental opt-in is declared decides the plan-mode element (§4) | Accepted; K-5 means the App declares `experimentalApi` true (J-1) |
| "each plan update carries the whole plan with no revision identity … plan mode is experimental-only" (S-F-13) | §5.1, §5.2 | Accepted; OBS-2 O-8 adds that plan mode produced no plan update at all at 0.158.0 |
| Not supplied: revision identity, registry, storage, export, UI, checker (SOW-128) | §5.2; no registry (R17-4); §5.6, §7.7; §3–§9; no checker (TBD-002) | Taken here as stated |

Nothing in S-2 needs changing. HOSTING §8.4 needs the HCG-A08 signal
replaced (C-04; J-2) and the goals surface placed (G-3; J-10).

---

## 3. Item scope and the split with DEL-01-04 and DEL-01-02 (B-5; PROPOSED)

| §8.4 group | Native kinds (supplier names) | Rendered by | DEL-01-03's part |
|---|---|---|---|
| HCG-A01 Messages and reasoning | `userMessage`, `agentMessage`, `reasoning` and their deltas | DEL-01-04 (conversation and turn) | None. A `userMessage`, including a run-start text element (R19-7), is never read as an act (§9 TA-3) |
| HCG-A02 Shell commands | `commandExecution`; `item/commandExecution/outputDelta`, `…/terminalInteraction` | DEL-01-03 | Tool row (§6) |
| HCG-A03 File changes | `fileChange`; `turn/diff/updated`, `item/fileChange/outputDelta`, `…/patchUpdated` | DEL-01-03 | Tool row (§6) |
| HCG-A04 Permission requests and review routing | `item/permissions/requestApproval`; `item/autoApprovalReview/*`, `guardianWarning` | DEL-01-04 (request cards, A14) | The affected row shows `waiting-on-request` and links to the card by item anchor (§6.2) |
| HCG-A05 MCP tools | `mcpToolCall`; `item/mcpToolCall/progress` | DEL-01-03 | Tool row (§6) |
| HCG-A06 App-offered tools | `dynamicToolCall`, `functionCallOutput`; `item/tool/call` request | DEL-01-03 (items); DEL-01-04 (the request) | Tool row |
| HCG-A07 Input from the person | `item/tool/requestUserInput`, `mcpServer/elicitation/request` | DEL-01-04 | A plan clarification answered there is conversation input (PS-3) |
| HCG-A08 Native delegation | `collabAgentToolCall`, `subAgentActivity` | DEL-01-03 | Tool row for the call; delegation view (§7) |
| HCG-A09 Planning | `plan`; `turn/plan/updated`, `item/plan/delta`; `collaborationMode/list` (exp) | DEL-01-03 | Plan view (§5) |
| **Goals (G-3; HOSTING §8.4 placement by F, J-10)** | Model tools `get_goal`, `create_goal`, `update_goal` (in every captured tool list, OBS-2 §6.1); notifications `thread/goal/updated`, `thread/goal/cleared`; client methods `thread/goal/get`, `thread/goal/set`, `thread/goal/clear` (HCG-B04) | DEL-01-03 | Goal line (§6.4); the App offers no set or clear control in this pass |
| HCG-A10…A15 | `webSearch`, `imageView`, `imageGeneration`, review mode, `contextCompaction`, `sleep`, `hookPrompt` | DEL-01-03 | Tool row (§6.3) |
| HCG-A16, A17 | Memory, realtime voice (experimental client methods) | Not presented in this increment | — |
| HCG-B03 Turn control | `turn/started`, `turn/completed`, `turn/interrupt` | DEL-01-04 (outcome); DEL-01-02 (state, interrupt) | Reads turn end as an event for §13 (PL-06, CL-03, TI-07/08) |
| HCG-B02 Thread lifecycle and history | `thread/read`, `thread/turns/list`, `thread/items/list`, `thread/loaded/list`, `thread/status/changed` | DEL-01-02 (state and recovery) | Issues reads for its own views (§12) and reads child threads (§7.4) |

An unfamiliar item kind is shown as "unfamiliar item `<type>`" with its
native content inspectable, never dropped (HOSTING H7) and never mapped to a
known kind.

---

## 4. Experimental surfaces (K-5 as ruled by R18-1 C-05)

**What is experimental at Codex 0.158.0** (variant diff of the generated TS,
the only test HOSTING §7.3 allows):

| Surface | Variant at 0.158.0 | Bearing |
|---|---|---|
| `turn/start` → `collaborationMode` {mode `plan` \| `default`, settings {model (required), reasoning_effort, developer_instructions}}; `thread/settings/update` | Experimental-only | Plan mode needs the opt-in |
| `collaborationMode/list` | Experimental-only | Tells the App whether a `plan` preset exists (OBS-2 O-8: `Plan` and `Default` returned) |
| `multiAgentMode` | Experimental-only and deprecated: ignored on requests; always `explicitRequestOnly` in responses | Not a control or a signal (F-1) |
| Item kinds `plan`, `collabAgentToolCall`, `subAgentActivity`; `turn/plan/updated`; `item/plan/delta`; `thread/goal/*` | Stable | Rendered whether or not the opt-in is declared |
| `Thread.parentThreadId`, `agentNickname`, `agentRole`, `sessionId`; `Model.multiAgentVersion`; `modelProvider/capabilities/read`; `experimentalFeature/list` | Stable | Delegation identity and availability (§7.1) |

Codex feature flags at 0.158.0 (`observed`, OBS-2 §6.1, §8): delegation is
gated by `multi_agent` (stage stable, default on) and `multi_agent_v2`
(stable, default off); plan mode is gated by no listed flag in use
(`collaboration_modes` is listed `removed`). `config/read` shows `features`
only when set.

- **EX-1 (the label).** A view element carries "experimental" only when it
  uses a protocol element that is experimental-only by the variant diff of
  the pin: at 0.158.0, the plan-mode element and the plan presets. Delegation
  and goals are stable and are never labelled (R18-1 C-05). For owner
  visibility (F-2, not a re-decision): K-5's premise that delegation needs an
  experimental setting does not hold at 0.158.0.
- **EX-2 (the opt-in).** `experimentalApi` is a per-connection handshake
  capability recorded in each `ready(g)`. Under K-5 the App declares it (J-1).
  DEL-01-03 reads the declared value per generation, never infers it from an
  experimental element arriving (HOSTING §7.3, OB-5).
- **EX-3 (fully usable without).** With the opt-in not declared, or no
  `plan` preset, the plan-mode element is "not offered" and the composer
  shows no plan control. When delegation is not available (§7.1), the
  delegation view is absent and one line says why. Every stable item still
  renders.

---

## 5. Plans (REQ-001, AC-001, VER-001)

### 5.1 The two native plan surfaces at Codex 0.158.0

| Surface | Native shape | In history? | Seen live at 0.158.0 |
|---|---|---|---|
| **Plan item** (plan mode) | Item `plan` {id, text} with `item/started` / `item/completed`; `item/plan/delta` ("Clients should not assume concatenated deltas match the completed plan item content") | **Yes**: a `ThreadItem`, returned by `thread/items/list` and `thread/read` | **Observed** (OBS-2 O-8): one `plan` item per plan-mode turn, id `<turnId>-plan`, streamed by 188 `item/plan/delta`, then completed; no agentMessage in that turn |
| **Checklist** (`turn/plan/updated` {threadId, turnId, explanation, plan: [{step, status `pending` \| `inProgress` \| `completed`}]}) | Whole list each time; `TurnPlanStep` occurs only in this notification | **No** (`observed-in-generated-types`, by absence) | **Not observed**: no `turn/plan/updated` and no `update_plan` tool appeared in any captured tool list, in plan or default mode (OBS-2 O-8, §6.1). Kept designed; shown "not observed at Codex 0.158.0" in the feature map |

### 5.2 Revision identity and durability (B-2; PROPOSED; R17-4, R18-1 C-03)

- **RV-1 Plan-item revision.** Each completed `plan` item is one revision.
  Identity `pi:<threadId>:<turnId>:<itemId>`, from Codex identities only, so
  the same identity is derived live and from history. Ordinal: position
  among the thread's plan items in history order; live, the order of
  `item/completed` receipt (expected equal; a disagreement is shown).
- **RV-2 Checklist revision.** Each `turn/plan/updated` received is one
  revision of that turn's checklist. Identity
  `cl:<threadId>:<turnId>:g<generation>:p<receipt position>`; ordinal:
  receipt order within the turn. A repeated identical list is kept and
  marked "unchanged from the previous"; an update after the turn's end is
  kept and marked "after turn end".
- **RV-3 Content identity.** SHA-256 over canonical JSON of the native
  content, method recorded with the value; **TEST VALUE** pending HOSTING
  U-08.
- **RV-4 Durability.** Window close or reload within a generation: the view
  re-derives from DEL-01-02's re-attachment by position; identities and
  ordinals are unchanged. **Supplier restart** (the generation closed) and
  **relaunch**: the views rebuild from Codex history (R18-1 C-03). Plan-item
  revisions are recovered ("recovered from Codex history"); checklist
  revisions are **not recoverable**, shown on each affected turn as
  "checklist updates are not kept in Codex history; not recoverable after a
  restart or relaunch" (CL-06, CL-07). Nothing is reconstructed from
  messages.
- **RV-5 Deltas** are a preview labelled "in progress; may differ from the
  completed plan"; the completed item's text replaces them.
- **RV-6 Missing pieces.** A delta or completion with no `item/started`
  starts the item (PL-02, PL-05). A plan item still streaming at its turn's
  end shows "not completed (turn ended)" (PL-06, G-4); at a generation close
  "not completed when observation ended" (PL-07). Neither yields a revision
  unless a history read supplies a completed item (PL-09).

### 5.3 Plan interactions (B-3; PROPOSED)

| ID | Interaction | What DEL-01-04 sends, using the plan-mode element (§5.4) | Failure behaviour |
|---|---|---|---|
| PS-1 | **Create a plan in plan mode.** The person chooses "Plan" (labelled experimental) | `turn/start` with `collaborationMode` {mode `plan`, settings {model: the conversation's selected model, reasoning_effort, developer_instructions: **null**}} | Element "not offered" (EX-3). No model selected → the composer's K-3 wording (R18-2: "not started — no model selected" for an ordinary conversation; "run not started — no model selected" for a workflow run). Supplier error → shown; plan view unchanged |
| PS-2 | **Revise.** A further instruction in plan mode | As PS-1; the next `plan` item is revision n+1 | As PS-1 |
| PS-3 | **Answer a plan clarification** (`item/tool/requestUserInput`) | Answered on DEL-01-04's card; conversation input, never act evidence | As DEL-01-04 defines |
| PS-4 | **Edit and resend** the plan text | Ordinary input; Codex's plan item is never edited | — |
| PS-5 | **Carry out this plan** | Ordinary input (R17-9) with `collaborationMode` {mode `default`, settings {model, …, developer_instructions: null}}. **Required**: plan mode persists on later turns sent without `collaborationMode` (observed, OBS-2 O-8), so leaving it needs the default mode sent explicitly (R18-1 C-06). No act is recorded unless a workflow checkpoint names one | As PS-1 |
| PS-6 | Checklist in default mode | Nothing (the agent updates it, if Codex produces one) | — |

Which plan revision the person acted on is read from Codex history order,
not kept by the App (R17-4).

**developer_instructions stays null (F-3, as now observed).** At 0.158.0 the
thread's developer text (role guidance, R19-1) is still sent beside the
plan-mode text (OBS-2 O-8); a non-null
`collaborationMode.settings.developer_instructions` is added as a further
developer message (O-5b) and, in plan mode, **replaces Codex's built-in
Plan Mode text** (OBS-3 W-5; null restores it). Workflows are supplied as a
text element of the turn that starts the run (R19-7), not through this
setting. So the element always sends null: the built-in plan text stays,
and neither role nor workflow supply is set aside at the transport level.
Whether the model gives plan mode precedence over the role text could not be
separated from adherence (U-P3, open). Every mode change appends a developer
message that stays in history (W-5); the plan control says "plan mode stays
on until you leave it".

### 5.4 The plan-mode element (offered to DEL-01-04; R18-1 C-06)

DEL-01-04 composes and sends turns and composes `collaborationMode` on
`turn/start` (R18-1 C-06; row DEL-01-04 → DEL-01-03 adopted, F0 NR-05).
DEL-01-03 offers one operation: **plan-mode element (mode `plan` |
`default`, selected model, effort)** → the `collaborationMode` value of PS-1
or PS-5, or "not offered (<reason>)" (EX-3), or "no model selected" (the
composer chooses R18-2's wording). The element never carries
`developer_instructions`. DEL-01-03 consumes nothing from DEL-01-04
(R17-10). Prototype PC-12 validates both composed `turn/start` parameter
sets against the bundle's `TurnStartParams`.

### 5.5 Plan acceptance standing (R17-9)

"Carry out this plan" is ordinary conversation input, not a reserved act,
unless a workflow checkpoint names an act; then the act is captured by
DEL-01-04's act control and the plan view only shows the record handed to
it (TA-4).

### 5.6 The plan-revision reference offered to DEL-02-02 (B-8; PROPOSED)

One record of `npt.plan-revision.schema.json` per revision: identity and
kind, thread, turn, item (plan items), generation and position (checklists),
ordinal, native content, content identity with method, standing
(`live-observed` or `recovered-from-supplier`; a checklist can only be
`live-observed`), types pin, observed version label. DEL-02-02 decides what
a draft takes from it.

### 5.7 Run boundaries (R19-2; display only)

The plan and tool views draw no run start or end markers: the conversation
view does (R19-2). When DEL-02-03 hands run markers (thread, turn, start or
end, the workflow and revision named) as a runtime value, the plan view
labels each revision and the tool view each row with the run in force at its
turn ("during the run of ‹workflow› ‹revision›"). Plan revisions and tool
rows keep their thread-scoped identities across a run boundary: run B does
not reset run A's plan, and no run element enters the plan-revision record
(prototype PC-18). The run-start text element (R19-7) is a `userMessage`,
rendered by DEL-01-04. An agent's proposal of the next workflow (R19-2 (b))
is a message, not shown here as a plan or a selection.

---

## 6. Tool activity and goals (REQ-002, AC-002, VER-002)

### 6.1 Display states

| Display state | Meaning |
|---|---|
| `in-progress` | `item/started` observed, no completion yet |
| `waiting-on-request` | A server request for this item is outstanding in the register (runtime value). OBS-1b OB-3 saw the item announced in progress while its approval was pending |
| `completed`, `failed`, `declined`, `interrupted` | `item/completed` observed with that native status. Kinds with no status element show `completed` meaning only "completion observed" |
| `not-completed` | **New (G-4).** The item's turn ended and no `item/completed` came: shown "not completed (turn ended)". Observed at 0.158.0: an item open at an interrupt never completes and is absent from history (OBS-2 O-1, O-3, O-2) |
| `unknown` | No completion observed and the turn's end not known: the generation closed first, or a history read shows the item `inProgress`. Settles to `not-completed` when history shows its turn ended (TI-14). Never shown as failed or succeeded (V4-EXE-03; HOSTING H10) |

The native status value is always shown beside the display state, unchanged.

### 6.2 Rules

- **TR-1 No translation.** A row carries the native item unchanged; the
  display state is a reading beside it (prototype PC-07).
- **TR-2 Origin of a command.** `source` as supplied at `item/started` and
  `item/completed` (OB-2 saw `agent` then `unifiedExecStartup`); a
  `userShell` command is the App's own call at the person's direction.
- **TR-3 Request settlement.** The settlement origin is shown exactly as the
  register supplies it. A `declined` status with no settlement handed in
  shows no origin. A request resolved by the supplier after an interrupt
  (OBS-2 O-3) is shown as DEL-01-04's card shows it; the row shows
  `not-completed`.
- **TR-4 Outcome available or not.** At completion, a row whose result
  elements are all null shows "result not supplied by Codex" (AC-002's
  *unavailable*); `not-completed` and `unknown` are different cases.
- **TR-5** Exit codes and `success` flags are shown as supplied.
- **TR-6 Request link.** A `waiting-on-request` row carries an item anchor
  (`npt.item-anchor.schema.json`); DEL-01-04's card cites the same anchor.
  The row never offers an answer control.

### 6.3 What each row shows

| Kind | Shown (supplier names) |
|---|---|
| `commandExecution` | command, cwd, source (start and completion), commandActions, status, exitCode, durationMs, aggregatedOutput |
| `fileChange` | changes (path, kind, diff), status; the turn's `turn/diff/updated` |
| `mcpToolCall` | server, tool, arguments, status, result or error, durationMs, readOnlyHint |
| `dynamicToolCall` / `functionCallOutput` | tool, namespace, arguments, status, success, contentItems / name, output |
| `collabAgentToolCall` | tool (any of the nine `CollabAgentTool` values, which cover both the v1 and v2 delegation tool sets OBS-2 §6.1 captured), status, sender and receivers, prompt, requested model (empty at start in OBS-2) and effort, agentsStates |
| `webSearch`, `imageView`, `imageGeneration`, review mode, `contextCompaction`, `sleep`, `hookPrompt` | Their elements as supplied |

### 6.4 Goals (G-3; PROPOSED)

Codex keeps one goal per thread (`ThreadGoal` {objective, status `active` |
`paused` | `blocked` | `usageLimited` | `budgetLimited` | `complete`,
tokenBudget, tokensUsed, timeUsedSeconds, createdAt, updatedAt};
`observed-in-generated-types`). The model can call `get_goal`, `create_goal`
and `update_goal` (tools seen in every captured tool list, OBS-2 §6.1; a call
was not observed). No `ThreadItem` kind exists for them at 0.158.0, so
inference: their effect is visible only through `thread/goal/updated`
{threadId, turnId, goal} and `thread/goal/cleared` {threadId}.

- **GO-1** The goal line shows Codex's objective and status unchanged, with
  "Codex's goal status; not a workflow run, checkpoint or acceptance", and
  its source and time. `thread/goal/cleared` → "No Codex goal". On opening
  a conversation the view reads `thread/goal/get`.
- **GO-2** OBS-2 O-2 saw `thread/goal/cleared` after a resume with no goal
  ever set: the line then reads "No Codex goal" and nothing else (no event
  is shown as the person's).
- **GO-3** The App offers no goal set or clear control in this pass; if one
  is added it is person-directed (HOSTING §5) and DEL-01-04's.

---

## 7. Delegation (REQ-003, AC-003, VER-003; K-10)

### 7.1 Availability (R18-1 C-04; read at run time, R19-5)

Delegation is **available** for a conversation when all hold:
`Model.multiAgentVersion` of the selected model (`model/list`) is `v1` or
`v2` (not `disabled`), **and** `modelProvider/capabilities/read` reports
`namespaceTools` true, **and** the effective configuration does not set
`features.multi_agent = false` (`config/read`; absent unless set).
**Readings, in R21-1's order (this section is the reference R21-1 names;
EXEC EV-3a, its `_delegation` and WD §4.2.5 follow it):** (1)
`multiAgentVersion` = `disabled` → **missing**; (2) effective
`features.multi_agent = false` → **missing**; (3) `namespaceTools` false →
**missing**; (4) any of the three not read (the model entry or its version
not read or null, the configuration not read, the capabilities not read or
`namespaceTools` null) → **not established**; (5) otherwise **present**.
*Missing* hides the view with the first reason in that order; *not
established* shows the view only if delegation items arrive. A configuration
that was read and sets nothing is read, not unread (prototype PC-16, RV21). Reason
(observed, OBS-2 §6.1): at 0.158.0 Codex sends the delegation tools only
inside a `namespace` tool, and with `multi_agent = false` sends none.

**Stock LM Studio 0.4.16 (observed):** it drops `namespace` tools, so
delegation never reaches the model and the view stays absent (OBS-2 O-4;
OBS-1 OB-1). Whether Codex's `namespaceTools` reads false for such a
custom provider is not observed (U-P8); delegation items, if any arrive,
are always shown.

### 7.2 Identity model

| Element | Source (supplier names) | Standing |
|---|---|---|
| threadId | `collabAgentToolCall.receiverThreadIds` (empty while the spawn is in progress, the child at completion); `subAgentActivity.agentThreadId`; `Thread.id`. No `thread/started` arrives for a child | Observed through an adapter (OBS-2), not stock behaviour |
| parentThreadId | `Thread.parentThreadId` from `thread/read`; else `collabAgentToolCall.senderThreadId`; else the thread of a `subAgentActivity` item (**inference**, labelled) | As named in `parentSource` |
| sessionId, agentNickname, agentRole, depth | `Thread` and `Thread.source.subAgent.thread_spawn` from `thread/read` (observed through the adapter: `agentRole` the role, nickname set, depth 1) | As stated |
| spawnedBy; requested model, effort | The `spawnAgent` call item | observed-in-generated-types; seen through the adapter |
| lastObserved {status, source, time} | `agentsStates[child].status` (OBS-2 saw `pendingInit` at spawn completion, `completed` with the child's final text at `wait`); `subAgentActivity.kind`; a child frame; `Thread.status` from a read | As named |

Children are **not** in `thread/list`; they are in `thread/loaded/list` and
readable by `thread/read` (OBS-2 O-4, adapter). After a relaunch the view
finds children from `receiverThreadIds` in the parent's history and reads
them.

### 7.3 Display rules

- **DR-1 Last observed, always sourced.**
- **DR-2 Parent completion says nothing about children.** No §13 DS row is
  triggered by it (PC-08). A child's `completed` (Codex's agent status) is
  shown as Codex's status; return, review and integration are never inferred.
- **DR-3 Observation ended** at a generation close, last value kept.
- **DR-4 Task-agent delegation (K-10; R18-1 C-07, C-08).** DEL-02-04 hands,
  per thread, the K-10 label {role, limit, standing} as a runtime value
  (ROLE §6.3 DL-4, §7.2 O-6). On a spawn from a thread labelled TASK the
  descendant is shown and exported with the standing as handed:
  `stated-not-enforced` → "the task role states that a task agent does not
  delegate (stated, not enforced)"; `enforced-by-supplier` → "enforced by
  Codex (‹mechanism named by DEL-02-04›)"; `unknown` → "not known whether the
  supplied guidance states this". Nothing is blocked. Observed through the
  adapter: a TASK-guided parent delegated and every call was recorded (OBS-2
  O-4b).
- **DR-5 Roles of children (R18-4).** `agentRole` and `agentNickname` are
  shown as Codex reports them. A role-configured child receives its role
  file's developer instructions, not the parent's (OBS-2 O-4a, adapter); a
  child spawned without a role type: its guidance is shown "not known", never
  "inherited".
- **DR-6 Child controls.** "Interrupt this child's turn" only through
  DEL-01-02's interrupt operation; its effect on a child is **not observed**
  (OBS-2 O-1/O-4 did not cover it; U-P4). No other child control.

### 7.4 Observing children

- **CO-1 holds** (observed through the adapter, OBS-2 O-4): child frames
  arrive on the same connection with the child's `threadId`; applied live
  (DS-03).
- **CO-2** On-demand reads when the person opens a child or after observation
  ended (`thread/read`, then `thread/turns/list` / `thread/items/list`),
  each shown "read at <time>". No polling (U-P5 closed).

### 7.5 States

§13's DS table: `observed`, `observation-ended`, `not-found`.

### 7.6 Fleet seam

PKG-06 consumes native delegation identities (CLM-003; DEP-01-03-014;
DEP-06-01-007). DEL-01-03 exports; it imports nothing from PKG-06 (REQ-007,
R17-10) and adds no fleet feature (TBD-004, OI-006).

### 7.7 The delegation export (PROPOSED)

One record of `npt.delegation-export.schema.json` per request: export
identity, time, producer, root thread, the descendant nodes of §7.2 with
`observationEnded` and `delegatingRole` {role TASK, limit id, standing of
three values as handed}, and four fixed limit statements;
`additionalProperties` false throughout. Receiver: PKG-06 (DEL-06-01). Not
DEL-02-04 (R18-1 C-07).

---

## 8. Version identity display (REQ-004, AC-004, VER-004)

| Line | Cases (shown text, PROPOSED) |
|---|---|
| Supplier | `verified` → "Codex <label> · verified (<qualification reference, or 'no qualification reference supplied'>)". `mismatch(<element>)` / `unverifiable(<reason>)` → "Codex not started: <result>". A development run under HOSTING U-06 → "Codex <label> · unverified development run — not the pinned supplier" |
| Types | "Views built from generated types at 0.158.0 (manifest 42b95826…), definition pin, not qualified" and "the running label matches" or "the running supplier reports <x> — compatibility not verified" |
| Experimental opt-in | "declared" / "not declared" (generation g) |

- **VR-1** "Verified" appears only from a §7.2 `verified` result.
- **VR-2** No pin is qualified (DEP-005), so any running supplier today is a
  U-06 development run; the display says so.
- **VR-3** Every fixture and result names the pin, the generated-output
  identity and its standing label.

---

## 9. Truthful actor (REQ-005, AC-005, VER-005)

- **TA-1** No act is derived from any native item (PC-07, PC-13).
- **TA-2** An A14 settlement is shown only as a tool-permission settlement
  with the register's origin.
- **TA-3** A person's message, including a run-start text element, is
  conversation content, never act evidence.
- **TA-4 Faithful display.** An act record handed in whose subject is one of
  this file's anchors is shown "<act kind> by <person> (identity not
  verified) · recorded by <recorder>" with content, scope and purpose (K1-4;
  RS §6.1); a record naming the recorder as actor is not shown as an act (RS
  HA-2). No acceptance-first order.
- **TA-5 Goals (G-3).** A Codex goal status, including `complete`, is
  never shown as a run end, a checkpoint, an acceptance or any act (PC-17).

---

## 10. Interfaces

### 10.1 Consumed

| From | What | Condition of use | When it fails |
|---|---|---|---|
| DEL-01-01 (S-2; DEP-01-03-011) | Native frames with generation and position; `ready(g)`; lifecycle events; generic request path | `ready(g)` received | Not ready → version line only |
| DEL-01-02 (DEP-01-03-012) | Re-attachment by position within a generation; thread list after relaunch; recovery reads; execution state; the interrupt operation | §12 | No re-attachment → rebuild from history (RV-4) |
| Runtime values (no register row; R17-10) | Register state of an item's request (DEL-01-02/01-04); K-10 label (DEL-02-04, ROLE O-6); run markers (DEL-02-03, R19-2); act records (DEL-04-03 via DEL-01-04); selected model (DEL-01-04's composer) | Present when handed | Absent → the element is not shown; never guessed |

### 10.2 Offered

| Operation | Receiver | Result | Failure behaviour |
|---|---|---|---|
| plan revisions (thread) | DEL-02-02 (DEP-01-03-013); DEL-04-03 and DEL-01-04 as subjects | `npt.plan-revision` records | Checklists after restart or relaunch: "not recoverable" |
| item anchor | DEL-01-04 (adopted row, C-06); DEL-04-03 | `npt.item-anchor` record | An item anchor without kind and display state is refused by the schema |
| plan-mode element | DEL-01-04 turn composition (C-06) | `collaborationMode` value, or "not offered (<reason>)", or "no model selected" | §5.3 |
| delegation availability (thread) | DEL-01-04 (whether to show delegation status beside a turn) | present / missing (reason) / not established | §7.1 |
| delegation export (root thread) | PKG-06 / DEL-06-01 (DEP-06-01-007) | `npt.delegation-export` record | No descendants → empty `nodes` |
| fixtures and designed cases | DEL-09-02, DEL-09-05 | §15 | — |

---

## 11. Data

- **Held, in memory only, per App session:** plan revision index,
  checklist revisions of the live generation, tool rows, goal line,
  descendant nodes, the last mode, model, capability and configuration
  reads. Nothing is written to disk by DEL-01-03 (R17-4).
- **Not held:** any copy of Codex history; which plan was "carried out"; any
  act; any child return or integration; run records.
- **Formats (PROPOSED JSON Schema 2020-12, beside this file; valid and
  invalid instance each in `prototype/fixtures/`):**
  `npt.plan-revision.schema.json` (`$id` `…:v0.1`), `npt.item-anchor.schema.json` (v0.2: state
  `not-completed`; `$id` `…:v0.2` since RV21), `npt.delegation-export.schema.json` (v0.2: three-value
  standing; `$id` `…:v0.2` since RV21).

---

## 12. Operating sequences, with failure at each step

| ID | Sequence | Steps | Failure at a step → behaviour |
|---|---|---|---|
| SQ-1 | Open a conversation | 1 `ready(g)` → version line; 2 `thread/turns/list`, `thread/items/list` page by page (not `thread/read {includeTurns}`, which emits `deprecationNotice`, OBS-2 §11) → plan items, tool rows; 3 `thread/goal/get`; 4 availability reads (§7.1); 5 attach to live frames | 1 not ready → version line only. 2–4 read error → "not read (<error>)", retry offered; never an empty plan shown as "no plan". 5 a gap → DEL-01-02 re-attaches |
| SQ-2 | Window close or reload | Re-derive from DEL-01-02's re-attachment from position 0 of the live generation | Unavailable → as SQ-1 |
| SQ-3 | Supplier exits mid-item | 1 `exited-unexpectedly(g)` → streaming plan items "not completed when observation ended", open rows `unknown`, descendants "observation ended", checklists ended; 2 at `ready(g+1)` the views rebuild: checklists of g "not recoverable" (CL-07); turns and items re-read; rows of turns that read back ended settle `not-completed` (TI-14) | Frames of a closed generation are refused (H5; PC-04). OBS-2 O-2: after a stop the turn reads back `interrupted` with the open item absent, so TI-14 applies |
| SQ-4 | Relaunch | Nothing survives; SQ-1 against the threads DEL-01-02 lists; children from `receiverThreadIds` in history, then `thread/read` | Checklists "not recoverable"; children not listed by `thread/list` |
| SQ-5 | Pin mismatch | `refused` → "Codex not started: mismatch(<element>)" | — |
| SQ-6 | Opt-in absent | Plan-mode element not offered; stable items render | — |
| SQ-7 | Plan-mode turn | 1 `collaborationMode/list` at `ready(g)`; 2 the person chooses Plan; 3 DEL-01-04 sends `turn/start` with the element; 4 later turns carry the mode explicitly until the person leaves it | 1 error → "plan presets not read", element not offered. 2 no model → R18-2 wording. 3 error → shown |
| SQ-8 | Delegated work | 1 spawn call → node at completion (receivers known); 2 child frames (CO-1); 3 parent turn completes → no child change | 2 none arrive → CO-2 on demand |

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
| PL-06 | `streaming` | turn-ended | `incomplete` | "not completed (turn ended)" (G-4) |
| PL-07 | `streaming` | generation-closed | `incomplete` | "not completed when observation ended" |
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
| CL-06 | `none` | history-read | `not-recoverable` | "not kept in Codex history; not recoverable after a restart or relaunch" |
| CL-07 | `ended` | view-rebuilt | `not-recoverable` | As CL-06; the closed generation's revisions are dropped (C-03) |

**Tool row** ("final" = the display state of the native status, §6.1):

| ID | From | Event | To | Shown |
|---|---|---|---|---|
| TI-01 | `absent` | item-started | `in-progress` | Row |
| TI-02 | `in-progress` | request-outstanding | `waiting-on-request` | Link to the request card (TR-6) |
| TI-03 | `waiting-on-request` | request-settled | `in-progress` | Settlement origin as supplied (TR-3) |
| TI-04 | `in-progress` | item-completed | `final` | Native status; result or "not supplied" (TR-4) |
| TI-05 | `waiting-on-request` | item-completed | `final` | As TI-04; no origin unless supplied |
| TI-06 | `absent` | item-completed | `final` | As TI-04 |
| TI-07 | `in-progress` | turn-ended | `not-completed` | "not completed (turn ended)" (G-4) |
| TI-08 | `waiting-on-request` | turn-ended | `not-completed` | As TI-07 |
| TI-09 | `in-progress` | generation-closed | `unknown` | "no completion observed" |
| TI-10 | `waiting-on-request` | generation-closed | `unknown` | As TI-09 |
| TI-11 | `absent` | history-read | `final` | "recovered from Codex history" |
| TI-12 | `unknown` | history-read | `final` | As TI-11 |
| TI-13 | `absent` | history-read-in-progress | `unknown` | "in progress at the read" |
| TI-14 | `unknown` | history-turn-ended | `not-completed` | "turn <status> in Codex history; item not completed" (G-4; OBS-2 O-2) |
| TI-15 | `not-completed` | history-read | `final` | History shows a completion after all: Codex's history governs (constructed case; not observed) |

**Descendant** (a parent's turn end is deliberately not an event here, DR-2):

| ID | From | Event | To | Shown |
|---|---|---|---|---|
| DS-01 | `absent` | collab-call | `observed` | Node from the call item |
| DS-02 | `absent` | subagent-activity | `observed` | Node; parent by inference (labelled) |
| DS-03 | `observed` | child-observation | `observed` | Last observed updated |
| DS-04 | `observed` | generation-closed | `observation-ended` | "observation ended" (DR-3) |
| DS-05 | `observation-ended` | thread-read | `observed` | "read at <time>" |
| DS-06 | `observed` | not-found-reported | `not-found` | Codex's `notFound` as reported |
| DS-07 | `absent` | thread-read | `observed` | Node from `Thread` |
| DS-08 | `observation-ended` | child-observation | `observed` | Observation resumed |
| DS-09 | `observed` | thread-read | `observed` | Read values merged, sourced |

---

## 14. Feature and optional-reuse map (OUT-003; REQ-006, AC-006, VER-006)

### 14.1 Features, owners and basis

| Feature | Required behaviour (source) | Supplying / receiving owners | Native basis at Codex 0.158.0 | Standing / open matter |
|---|---|---|---|---|
| Plan view: plan items and revisions | REQ-001, SOW-003/128 | DEL-01-01 (S-2); DEL-02-02 receives | `plan`, `item/plan/delta`, history reads | Observed (O-8) |
| Plan view: checklist | REQ-001 | As above | `turn/plan/updated` | **Not observed at 0.158.0** in any captured configuration; designed |
| Plan-mode element | REQ-001, SOW-129; K-5 | DEL-01-04 composes and sends (C-06) | `collaborationMode` (exp), `collaborationMode/list` (exp) | Observed (O-8); U-P3 precedence |
| Tool activity rows | REQ-002, SOW-004/014 | DEL-01-04 (cards); DEL-01-02 (state) | Part A item kinds | MCP items still unobserved (OB-1) |
| Goal line | REQ-002 (native activity), G-3 | — | `thread/goal/*`; goal tools | Notifications observed (`cleared`, O-2); a goal tool call not observed |
| Delegation view and export | REQ-003, SOW-006; K-10 | PKG-06/DEL-06-01 receives | `collabAgentToolCall`, `subAgentActivity`, `Thread` | Observed through the adapter; absent on stock LM Studio 0.4.16 |
| Version line | REQ-004, SOW-128 | DEL-01-01; the Owner (also the App implementation owner, L-7) qualifies (OI-012) | §7.1 record | U-06; DEP-005 |
| Truthful-actor display | REQ-005 | DEL-04-03 records; DEL-01-04 placement | — | — |
| Fixtures and cases | REQ-008 | DEL-09-02/09-05 | Constructed now | Candidate needed |
| Registry storage, checker | SOW-128 (TBD-002) | — | — | None selected |

### 14.2 v3 exemplar, assessed as reuse candidates only (evidence, never a v4 commitment)

| v3 source (historical) | What it did | Assessment |
|---|---|---|
| `chirality-runtime/packages/core/src/native-plan-registry.ts` (35825fdaf339cc57) | Persisted completed plan items; per-session revision ordinal | **Not reused** (R17-4; V4-ARC-03); the ordinal survives as RV-1's, derived from history |
| `chirality-app-dev/frontend/src/components/shell/native-plan-panel.tsx` (1983f82da6a62c5f) | Plan tab | **Layout reference only** |
| `chirality-app-dev/frontend/src/lib/harness/plan-executions.ts` (221b8f9bbf6f2388) | Kept "which plan revision was sent for execution" in local storage | **Not reused** (R17-4) |
| `…/tool-stream-view.tsx` (bcd08e4c01e7350e), `subagent-stream-view.tsx` (479a15366dcca2b9), `lib/shell/harness-event-views.ts` (d750848e05042820) | Rows from the translated `HarnessEvent` stream | **Patterns only** ("last observed", "Observation ended with the parent turn") |

---

## 15. Fixtures and verification (OUT-002; REQ-008)

### 15.1 Fixture method

Fixtures are native frames and read results labelled with HOSTING §9.2
standing: `constructed` now (validated against the committed 0.158.0
bundle); `recorded` once captures exist. OBS-2's raw logs (`o8`, `o4-o4a`,
`o4-o4b`, `o1`, `o3`) are candidates for the first `recorded` plan,
delegation and interrupt fixtures once redacted under HOSTING §9.1; the
adapter-mediated ones keep R18-9's label. Interface examination covers
WebKit, Chromium and the packaged App smoke witness (REQ-008), on a
candidate only.

### 15.2 Designed cases

| Case | Serves | Setup | Expected | Runnable now? |
|---|---|---|---|---|
| NV-01 Plan revisions | VER-001, AC-001 | Recorded plan-mode turns (from OBS-2 `o8`); restart; relaunch | Plan items with `<turnId>-plan` identities, recovered from history; checklists "not recoverable" | Model only (PC-02…PC-05) |
| NV-02 Plan-mode interaction | VER-001 | Opt-in declared; `Plan` preset | PS-1…PS-5; plan mode left only by an explicit default; no act | Model only (PC-12); behaviour observed (O-8) |
| NV-03 Tool outcomes | VER-002, AC-002 | Recorded command, file change, MCP, dynamic tool items; an interrupt with an open item | Native values unchanged; `not-completed` at turn end; "result not supplied" | Model only (PC-04, PC-06, PC-07) |
| NV-04 Primary completed, descendant active | VER-003, AC-003 | A delegation capture where the parent completes before the child | Parent completed; child last observed running | Model only (PC-08, PC-09); **not observed** (OBS-2's parent waited for its child) |
| NV-05 Task-agent delegation | VER-003; K-10 | TASK-labelled conversation that delegates | Shown and exported with the standing handed | Model (PC-10); observed through the adapter (O-4b) |
| NV-06 Version identity | VER-004, AC-004 | `ready(g)` variants | §8 lines | Model only (PC-11) |
| NV-07 Truthful actor | VER-005, AC-005 | (a) tool success; (b) "Approved" message; (c) supplied act record; (d) a goal `complete` | No act except (c), shown actor ≠ recorder | Model only (PC-07, PC-13, PC-17) |
| NV-08 Map review | VER-006, AC-006 | §14 against the ScopeOfWork | Each exclusion traced to its owner (§16) | Review only |
| NV-09 Fixture provenance | VER-007, AC-007 | §15.1 records | Pin, output identity, standing, candidate/date/outcome | Review only |
| NV-10 Delegation availability | VER-003; C-04 | `model/list`, capabilities, configuration variants | §7.1 readings | Model only (PC-16) |
| NV-11 Run boundaries | R19-2 | Two runs chained in one conversation | Run in force shown per turn; identities unchanged | Model only (PC-18) |

### 15.3 Prototype (R17-1; R12-3)

`prototype/` (Python 3 standard library): `npt_model.py`, `scenarios.py`
(written out as `fixtures/native/*.jsonl`, 11 scenarios), schema fixtures, a
byte-identical copy of DEL-01-01's `jsonschema_subset.py` (sha256
486e9286…c0ffc0) and `run_cases.py`, which reads the committed 0.158.0
bundle of DEL-01-01 and writes nothing outside its folder.

**Run of 2026-10-02** (`python3 run_cases.py` in `Design/prototype/`;
output in `prototype/results/RUN_2026-10-02.txt`; the round-1 run is kept as
`RUN_2026-10-01.txt`): 18/18 cases gave their expected result (PC-01 bundle
conformance; PC-02…PC-05 plans incl. C-03 and G-4; PC-06, PC-07 tools;
PC-08…PC-10 delegation incl. C-08; PC-11 version; PC-12 experimental
surfaces and plan mode (C-05, C-06); PC-13 truthful actor; PC-14 schema
fixtures; PC-16 availability (C-04); PC-17 goals (G-3); PC-18 run boundaries
(R19-2); PC-15 every row of §13 reached and equal to the model's).
**Rerun at RV21** (2026-10-02, same command; output in
`prototype/results/RUN_2026-10-02_RV21.txt`): 18/18; PC-16 now follows
R21-1's order, with a configuration never read giving *not established*
and all 64 signal combinations checked against R21-1. A pass
shows that the rules run as written against constructed frames; it passes
no VER criterion.

---

## 16. Act and owner boundary (REQ-007)

| Act or production | Owner | This file |
|---|---|---|
| Codex process, handshake, frames, register, version verification | DEL-01-01 | Consumes S-2 |
| Custody, re-attachment, recovery, interrupt, stop, quit (R17-3) | DEL-01-02 | Consumes; DR-6 only through DEL-01-02 |
| Turn composition incl. `collaborationMode` (C-06), request cards, A14, turn outcome, messages, run start/end marks in the conversation, act control and act display placement | DEL-01-04 | Offers anchors, the plan-mode element and availability |
| Account, provider and model selection (K-3) | DEL-01-05 | Reads the selected model's `model/list` entry |
| Workflow-making journey, run-start text composition (R19-7) | DEL-02-02 | Offers plan-revision references |
| Run start, run records, chaining (R19-2) | DEL-02-03 | Shows run markers handed in |
| Role supply, K-10 label (C-07), child roles (R18-4) | DEL-02-04 | Shows the label and roles as handed or reported |
| Records and their format | DEL-04-03 | Shows supplied records (TA-4); writes none |
| Fleet graph, returns, waiting, decisions | PKG-06 | Exports identities only |
| Reserved acts A4–A7, A12, A13; professional reliance | The person (D2) | Performs, infers and decides none |
| Agent engine, credentials, protocol | OpenAI Codex | Consumes as published |

### 16.3 Register rows (R17-10, as ruled by R18-1)

- **Adopted (C-06; F0 NR-05):** DEL-01-04 consumes DEL-01-03 (INTERFACE:
  item anchors, plan-mode element, availability), with a DOWNSTREAM mirror
  here. SCC-neutral (DEL-01-03 does not reach DEL-01-04; DAG-003 by script).
- **Dropped (C-07):** DEL-02-04 consumes DEL-01-03.
- **Mirrors (F0 M-3):** DOWNSTREAM mirrors here of DEP-06-01-007,
  DEP-09-02-011, DEP-09-05-008. SCC-neutral.
- **Not proposed, by design:** DEL-01-03 consuming DEL-01-04, DEL-02-02,
  DEL-02-03, DEL-02-04, DEL-04-03 or DEL-06-01 (each would form an SCC);
  those are runtime values (§10.1).

---

## 17. Joins for node F and the parallel D nodes (R17-14)

| ID | File, section | Now | Needed (v0.2) |
|---|---|---|---|
| J-1 | HOSTING §4.2 step 4; U-21; F-13 (FH-11) | Opt-in "required to use plan mode" | Under K-5 the App declares `experimentalApi` true; DEL-01-03 reads the declared value per generation (EX-2). Unchanged |
| J-2 | HOSTING §8.4 HCG-A08 (FH-33) | "`multiAgentMode` on thread and turn start (experimental-only)" | **Changed (C-04):** replace with: available when `Model.multiAgentVersion` ≠ `disabled` and `modelProvider/capabilities/read` → `namespaceTools` true; an effective `features.multi_agent = false` reads missing; `multiAgentMode` deprecated and ignored |
| J-3 | HOSTING §4.6 / §5 Order (FH-05) | — | **Withdrawn (C-03):** closed-generation events are not re-readable; NPTD RV-4 rebuilds from history |
| J-4 | HOSTING VC-09 (FH-35) | "revision identity left to DEL-01-03" | Cite NPTD-v0.2 §5.2 RV-1, RV-2; add that in plan mode only a `plan` item is produced (O-8) |
| J-5 | EXEC §3.4 EV-3a `agent-delegation` (FE-05) | "present when the thread start reports a `multiAgentMode` … Active (experimental opt-in)" | **Changed (C-04, C-05):** the §7.1 rule (present / missing / not read); not experimental |
| J-6 | WD §4.2.5 `agent-delegation` standing (FW-10) | "`multiAgentMode` … is experimental-only" | "deprecated (ignored)"; item kinds and the `multi_agent` feature stable (O-8); signal per C-04 |
| J-7 | DEL-02-04 (D6) | — | **Changed:** (a) the plan-mode element sends `developer_instructions` null, so role supply is not set aside at the transport level (O-8, O-5b, W-5); (b) DEL-01-03 receives the K-10 label {role, limit, standing} as a runtime value per thread (C-07, C-08); (c) children's guidance per R18-4 (DR-5) |
| J-8 | DEL-01-02 (D1) | — | Re-attachment by position within a generation only (C-03); thread list after relaunch; interrupt usable on a child (not observed); register state per item; G-4 wording "not completed (turn ended)" shared with RECOVERY |
| J-9 | DEL-01-04 (D3) | — | **Changed (C-06):** DEL-01-04 composes `collaborationMode` from the plan-mode element and sends `default` explicitly to leave plan mode; cites item anchors on request cards; places TA-4 act display; R18-2 K-3 wording is the composer's; G-4 wording shared with NIR's turn outcome |
| J-10 | HOSTING §8.4 (G-3; F's) | Goals not grouped | **New:** place `thread/goal/updated`, `thread/goal/cleared` and the goal tools in a goals group of Part A (agent capability), beside HCG-B04's client methods; NPTD §6.4 renders them |
| J-11 | DEL-02-03 (run markers, R19-2) | — | **New:** run markers (thread, turn, start/end, workflow and revision) offered as a runtime value to DEL-01-03 for display (§5.7); no row (SCC) |

---

## 18. Version dependence (R19-5)

Each statement below rests on Codex 0.158.0 and is re-checked by the
proposed version-advance check (regenerate, diff, rerun OBS harnesses):

| Statement | Basis at 0.158.0 | Read at run time instead? |
|---|---|---|
| Plan mode is experimental-only; presets | Variant diff; O-8 | `collaborationMode/list` per generation |
| Plan mode persists until `default` is sent; a non-null mode developer text replaces the built-in plan text | O-8; W-5 | No (behaviour) |
| Plan item id `<turnId>-plan`; no `turn/plan/updated` | O-8 | No; checklists stay designed |
| Delegation availability | O-4, O-8; generated types | Yes: `model/list`, `modelProvider/capabilities/read`, `config/read` |
| Delegation item shapes; v1/v2 tool sets | Generated types; O-4 (adapter) | Items rendered as supplied |
| Goal surface | Generated types; O-2 | `thread/goal/get` |
| Items open at an interrupt never complete | O-1, O-3, O-2 | No; TI-07…TI-15 handle either way |
| `multiAgentMode` deprecated | Generated descriptions | Not used |

---

## Findings

- **F-1 `multiAgentMode` is not a delegation signal at 0.158.0** (ignored on
  requests; always `explicitRequestOnly`). Replaced per C-04 (J-2, J-5, J-6).
- **F-2 Delegation is not experimental** (stable items; `multi_agent`
  stable, default on). Resolved by C-05; owner visibility only.
- **F-3 Plan mode and supplied guidance.** Transport: the thread's developer
  text is still sent in plan mode (O-8); a non-null mode developer text
  replaces the built-in plan text (W-5). Model precedence open (U-P3).
- **F-4 Plan mode needs a model** (`Settings.model` required).
- **F-5 Checklists are not in history**, and at 0.158.0 were not produced
  at all in any observed configuration (O-8).
- **F-6 A child's depth and spawn source come only from a read.**
- **F-7 Goals** are a native surface with no item kind; shown from
  notifications and reads (G-3).
- **F-8 Items open at an interrupt never complete** and leave no history
  (O-1, O-3, O-2); settled `not-completed` (G-4).
- **F-9 Delegation is unavailable on stock LM Studio 0.4.16** (namespace
  tools dropped); the view is absent there.

## UNRESOLVED

| Item | Owner | Point of need | Effect here |
|---|---|---|---|
| U-P1 Checklist surface never produced at 0.158.0 (narrowed: plan items observed, O-8) | Owner (as App implementation owner, L-7), at a version advance | Before checklist fixtures | Designed, labelled not observed |
| ~~U-P2~~ | Closed: plan mode persists (O-8) | — | PS-5 required |
| U-P3 Whether the model gives plan mode precedence over role text (narrowed: transport answered by O-8, W-5) | DEL-02-04 with the Owner (a stronger model, later observation) | Before plan mode is offered with role supply | Element sends null; control notes "plan mode stays on until you leave it" |
| U-P4 `turn/interrupt` on a child; primary completed while a child runs (NV-04) | A later observation | Before NV-04, DR-6 | DR-6 PROPOSED |
| ~~U-P5~~ | Closed: no polling | — | — |
| U-P6 Content-identity method (HOSTING U-08) | Owner with DEL-04-03 | Before records cite plan revisions | TEST VALUE |
| U-P7 OI-008 placement | Owner (phase review) | Before allocation | §1 PROPOSED under O-1 |
| U-P8 Whether `namespaceTools` reads false for a provider that drops namespace tools | A later observation (needs `modelProvider/capabilities/read` on that route) | Before relying on "missing" for local providers | §7.1: items shown if they arrive |
| U-P9 A goal tool call by the model: whether an item or only notifications appear | A later observation | Before goal fixtures | GO-1 from notifications |
| HOSTING U-06 Development run of an unverified distribution | Owner | Before implementation | §8 covers it |

## Verification cases

Designed cases: §15.2 (NV-01…NV-11). Prototype cases: PC-01…PC-18 (§15.3).
No case passes a VER criterion before an App candidate exists.
