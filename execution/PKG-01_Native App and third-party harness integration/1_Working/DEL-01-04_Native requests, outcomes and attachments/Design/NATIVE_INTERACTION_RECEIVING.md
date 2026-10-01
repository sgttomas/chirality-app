# Native requests, outcomes and attachments — receiving and interaction design

- Contribution: DEL-01-04/NIR-v0.1 (first version). Companion:
  [APP_ACT_CONTROL.md](APP_ACT_CONTROL.md) (DEL-01-04/AAC-v0.1), which designs
  the App act control.
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not
  accepted. Beside it: three PROPOSED schemas with a valid and an invalid
  example each (§14), and a design prototype in [`prototype/`](prototype/)
  that ran on 2026-10-01 (§13.2). No product code.
- Run and node: `APP-V4-DESIGN-PASS-3-20261001`, node D3 (Type 2 TASK, Claude
  Opus 5.5, high effort; does not delegate), dispatched by HELP_HUMAN.
- Serves: OUT-004 (the receiving contract), the behaviour of OUT-001 and
  OUT-002 (definition only), the design of OUT-003 (fixture cases, some run on
  the model); REQ-001…REQ-007; VER-001…VER-007 as designed cases.
- Paths are relative to `projects/chirality-app-v4/execution` unless they
  start with `docs/` (`projects/chirality-app-v4/docs/`).

**Basis and inputs (sha256 recomputed with `shasum -a 256` at this node;
repository HEAD `dc031b5bec`).** The accepted basis as amended by SCA-V4-001
and SCA-V4-002 (`docs/PRD.md` V4-APP-01, V4-APP-04, V4-EXE-01…04, V4-WF-02,
V4-WF-03, V4-WF-05, V4-AUT-03…05; `docs/ARCHITECTURE.md` §3; `docs/EXAMINATION.md`
V4-EXM-10, V4-EXM-11), cited through the first-increment files below; DAG-003
(`_DAG/DAG-003/HANDOFF_STATE.md` 56d849b6d078d8d5…, `DependencyEdges.csv`
4716ca287d23835c…, `CandidateEdges.csv` 07b969209e273310…). Run records under
`_Coordination/AgentRuns/APP-V4-DESIGN-PASS-3-20261001/`: `BRIEFS.md`
b261394112d7264e… ("Common rules"; "D — design nodes, round 1", row D3),
`OWNER_DECISIONS.md` 9d18c40dd7d894dc… (DECISION-K3 as revised: binding),
`R17_RESOLUTIONS.md` b0af81bcbad9bc52… (R17-1…R17-16: binding),
`DECISIONS_PENDING.md` 431ec4eb22a0b913… (K-1…K-12 options; Part 2),
`SURVEY/S1-B.md` c947d4d478fe21d3… (Part A, the starting list; A.6 overridden
by R17 where they differ), `SURVEY/S1-C.md` 06a8a6667ca7c64d… (DEL-02-02
passages naming DEL-01-04 and A15). Pass 2: `OWNER_DECISIONS.md`
b2fa81871cbf44b9… (DECISION-K1 K1-1…K1-4), `closeout/C1-A.md`
e2cb79e22ea5cf75… (SC2-01-04-1). This deliverable: `ScopeOfWork.md`
0cdb44e297010b70…, `Dependencies.csv` 20ce3808597bf283…. First-increment
Design files, read by section (cited by version label and section):
DEL-01-01/HOSTING-BOUNDARY-v0.8 `HOSTING_BOUNDARY.md` 3cf0381c42358fec… (§1,
§3, §4, §5, §6, §8, §10.1, §11, §12, UNRESOLVED, verification cases) with
`hosting.server-request-entry.schema.json` dda16758d28b4c20…;
DEL-02-03/EXEC-v0.6 `EXECUTION_COMPATIBILITY.md` 64e732d502d0b91d… (§2.1,
§2.4, §2.5, §2.6, §2.7, §4.5, §4.9, §5, §9, §10); DEL-04-01/ACT-POLICY-v0.8
`ACT_AND_POLICY_CONTRACT.md` 6fb6b9e883fa8d20… (§2, §4.7, §9, §10);
DEL-04-02/AS-v0.8 `AUTONOMY_AND_STANDING_EXCHANGE.md` d6f26801b0146800… (§4, §8,
§9, §13); DEL-04-03/RS-v0.8 `RECORD_SEMANTICS.md` b25cc90e9e252f50… (§3, §6,
§7, §10, §13, §14) with `RS_RECORD.schema.json` b63a7e421b885854… and
`prototype/minischema.py` 2851bb7cd4977b96…. Generated protocol types at the
0.158.0 definition pin, read only from the session scratch folder named in
R17-13 (`…/scratchpad/codex-0.158.0/gen`): the 16 files this file cites
(`ServerRequest.ts`; `v2/` `CommandExecutionRequestApprovalParams`,
`CommandExecutionApprovalDecision`, `FileChangeApprovalDecision`,
`PermissionsRequestApprovalResponse`, `PermissionGrantScope`,
`ToolRequestUserInputParams`, `ToolRequestUserInputQuestion`,
`McpServerElicitationAction`, `McpServerElicitationRequestParams`,
`ServerRequestResolvedNotification`, `TurnStatus`, `Turn`, `UserInput`,
`ThreadAttachment`, `ThreadActiveFlag`) were each matched by sha256 against the
committed `DEL-01-01/Design/generated/0.158.0/MANIFEST.sha256`
(42b95826d7bd6d58…): 16 of 16 equal. The decision descriptions quoted in §4.2
are from the JSON Schema output `CommandExecutionRequestApprovalResponse.json`
and `ExecCommandApprovalResponse.json` of the same scratch folder. The App v3
exemplar (`projects/chirality-app-dev/frontend`) is cited as historical
evidence only (§10).

**How this file reads its ScopeOfWork where it lags (R17-15).** The
ScopeOfWork (sha256 0cdb44e2…) predates DECISION-K1, DECISION-K3 and R17. This
file reads it as follows; the precise proposals for SCA-V4-003 are in the
return file `D/D3.md` (SC3-01-04-1…8).

| # | ScopeOfWork text | Reading used here | Source |
|---|---|---|---|
| L-1 | Names no act control or person identity (`grep` returns 0) | The App act control is designed in AAC-v0.1, labelled PROPOSED until SCA-V4-003 carries SC2-01-04-1, which this pass amends to include A15 and DEL-02-02 | R17-6; K-8; K1-4 |
| L-2 | REQ-004/CLM-004/REQ-006: "reviewed registration … belong[s] to App DEL-02-02" | DEL-02-02 performs the registration (writes the revision to the library); the person's A15 is captured by the App act control (K-8). DEL-01-04 performs no registration | K-8; R17-2 |
| L-3 | REQ-001 "explicit decline" without saying which form | The decline is the request's own negative form where it has one; two kinds have none, and a PROPOSED form is used (§4.3) | REQ-001; HOSTING U-20 |
| L-4 | REQ-001 is silent on automatic answers after time | No automatic decline, ever; a supplier's own resolution is shown as such | R17-9 |
| L-5 | REQ-005 predates K1-1…K1-4 | The agent asks; earlier acts on current content count, cited with their time; a joint answer after partial lapse; the person is recorded "identity not verified" | DECISION-K1 |
| L-6 | Names neither the App checkpoint display nor DEL-04-02's components | DEL-04-02 defines the components and their meaning; this file places them in the App and owns their behaviour there (§9) | R17-7 |
| L-7 | Names no conversation start display | A new conversation shows "no model selected" until the person chooses (§5.4) | K-3 |
| L-8 | REQ-002 uses "interrupted" and "stop" without the three operations | Interrupt a turn, end a run and stop the Codex process are presented as three things, as DEL-01-02 defines them (§5.2) | R17-3 |

**Reading note.** Element names defined here (*card*, *card state*, *supply
record*, *draft view*) are semantic names, not wire fields, components or
storage choices. Supplier method, field and value names are facts of the
generated types at the 0.158.0 definition pin, quoted as supplier names; they
select nothing. Standing labels for supplier facts are R17-13's: `observed`
(OBS-1/OBS-1b, through HOSTING §10.1), `observed-in-generated-types`,
`inference`. Cells that OBS-2 will settle are marked **OBS-2 pending**.
Design labels are R9's: SETTLED, DERIVED, INTEGRATION, PROPOSED; anything new
here and unlabelled is PROPOSED (D3).

---

## 0. Act names and words used

Act names are ACT-POLICY-v0.8 §2.1's canonical names (A1…A15). Following ACT
§9, this file's own prose says "approve"/"approval" only for A6 and "accept"
only for A5. Supplier names that contain those words (for example
`item/commandExecution/requestApproval`, the decision `accept`) are quoted as
supplier names and denote A14 subjects or supplier input forms.

## 1. What this deliverable is

DEL-01-04 is the App's native interaction surface for three things the stock
Codex App Server produces and the person meets in a conversation:

1. **requests** the supplier raises (tool permission, questions, elicitations)
   and the person answers (§4);
2. **turns and their outcomes**, shown only from observed facts (§5), with the
   conversation's start display (§5.4);
3. **content the person supplies** (attachments, drafts handed to a
   conversation) with the identity of what was actually supplied (§6), and the
   native **draft view** that receives the workflow workspace's transitions (§7).

It also places the human-act presentation (§8) and the checkpoint and standing
display (§9) in the App, and it owns the **App act control** (AAC-v0.1).

It does not own: the register, its custody, recovery or persistence (DEL-01-01,
DEL-01-02); the definitions of stopping (DEL-01-02, R17-3); plan, tool and
delegation views (DEL-01-03); account, provider and model selection (DEL-01-05);
the workflow workspace, review and registration (DEL-02-02); policy and act
meanings (DEL-04-01); display component meanings (DEL-04-02); the record
format, writer and reader (DEL-04-03). §11 traces each exclusion.

### 1.1 Process placement (R17-5: PROPOSED; requirements stated apart)

The requirements below hold whatever OI-008 decides. The placement column is
R17-5's PROPOSED division (HOSTING §12 O-1); the phase review owns OI-008.

| # | Requirement (holds for any placement) | PROPOSED placement (R17-5) |
|---|---|---|
| PL-1 | The register, the answer write path and the state a card shows have one authoritative source that survives a window reload (HOSTING H2, H3; V4-EXE-01) | Rust host: register and write path; the interface renders cards from it |
| PL-2 | A card never holds an answer as authoritative; closing or reloading a view loses no request and answers none (REQ-001, REQ-002) | Interface state is disposable; cards are rebuilt from "list outstanding" (HOSTING §6.4) |
| PL-3 | No agent tool, MCP operation, App rule, supplier request or interface script can operate the act control or produce its record (EXEC CAP-4) | Host: offer composition, native confirmation and capture (AAC §6) |
| PL-4 | The content identity of a supplied file is taken as close as possible to the supplier's read (§6) | Host: identity taken when it writes the turn input |
| PL-5 | Draft transitions are received from the workspace and rendered, never produced locally (REQ-004) | Host receives, interface renders |

---

## 2. Interfaces

Arc direction is consumer → supplier. Layers are DAG-003's (admitted / held
in SCC-002). R17-10: DEL-01-02 and DEL-01-03 consume nothing from this
deliverable; what DEL-01-02 receives from it at run time (an answer submission
to the register it keeps) is a runtime value handed to it, not a production
input.

| # | Exchange | Supplier → receiver | Condition of use | Failure behaviour | Register / arc |
|---|---|---|---|---|---|
| IF-1 | Register operations: observe entries, list outstanding, answer, read settlement and acknowledgment (HOSTING §6.4); refusal reasons in U-26 order | DEL-01-01 (definition) with DEL-01-02 (custody) → DEL-01-04 | After `ready(g)` for the generation; the person's path only (origin `person-via-interaction`) | A refused answer leaves the card waiting and shows the reason (§4.4); a write failure is shown as outcome unknown (CS-5); a closed generation ends the card (CS-7). Nothing is retried by itself | DEP-01-04-007 (admitted), DEP-01-04-008 (admitted) |
| IF-2 | Recovered state: threads, turns with their observed status and cause, observation-lost markers, outstanding requests, run association, descendant states as the supplier reported them | DEL-01-02 → DEL-01-04 | On every view open, reload, reconnect and relaunch | Where DEL-01-02 cannot settle a state it says so and the view shows *unknown* (TO-6); the view never synthesizes completion or interruption (REQ-002) | DEP-01-04-008 (admitted) |
| IF-3 | Native items and notifications delivered unchanged (`turn/completed`, `thread/status/changed`, `error`, `serverRequest/resolved`, `item/*`) | DEL-01-01 → DEL-01-04 (through DEL-01-02's view of them) | Live session | Gaps are DEL-01-02's to report; the view shows the gap, not a guess | DEP-01-04-007, -008 |
| IF-4 | Draft identity and transitions: DEL-02-02's `draft_transition` and `draft_reference` (WR-v0.1 §5.1, §8), restated with D5's names in `nir.draft-transition.schema.json` plus two requested elements | DEL-02-02 → DEL-01-04 | When the workspace changes a draft's standing | A transition not in WR §5.1, or a *registered* without its A15 record, is refused and shown as an error of the feed; the view re-reads `draft_reference` | DEP-01-04-009 (held, SCC-002) |
| IF-5 | Native draft and attachment interactions; the App act control for A15 (K-8), composed from WR's `a15_descriptor` (RB-4) and reporting the capture back {record, capture evidence, descriptor, bound content} | DEL-01-04 ↔ DEL-02-02 | The workspace's journey | AAC §4.2 failure rows | DEP-02-02-013, mirror DEP-01-04-010 (held); statement update proposed (SC3-02-02-6 by D5) |
| IF-6 | Act names and record kinds (V-01), outcome map (V-05), label rules (V-07), no professional standing from agent output (V-08), routine tool permission (V-21) | DEL-04-01 → DEL-01-04 | Every label this deliverable shows | A value not carried is shown by its record's own words, never invented | DEP-01-04-011 (admitted) |
| IF-7 | Record format and writer (the act control writes `human_act`, `act_declined`); record-out for act and lapse display | DEL-04-03 → DEL-01-04 | Writes: on capture; reads: on view | RS §14 (late write with "record write failed"; *not yet evaluated* never shown as current) | DEP-01-04-012 (held) |
| IF-8 | Checkpoint overlay (K-5) and standing facets (K-6) component meanings; AS §4, §8, §9 display rules | DEL-04-02 → DEL-01-04 | Run panel and act log (§9) | A meaning not supplied is not shown; the display compares with the record (AS §6) | **None. New row proposed (NR-1)**, held, SCC-002, SCC-neutral |
| IF-9 | Display meanings SD-1…SD-5, CE labels and arrival references | DEL-02-03 → DEL-01-04 | Run panel (§9); the act control's "arrival it answers" (AAC §2) | As IF-8 | **None. New row proposed (NR-2)**, held, SCC-002, SCC-neutral (reverse of X-1) |
| IF-10 | Model selection state for the start display (none chosen / chosen / last explicit choice for the project); the Codex account as reported, for the person's identity (K1-4) | DEL-01-05 → DEL-01-04 | Conversation start (§5.4); each act capture (AAC §7) | No selection state → "No model selected"; no account reported → the account element is absent, never guessed | **None. New row proposed (NR-3)**, admitted, SCC-neutral (DEL-01-05 reaches no SCC-002 member) |
| IF-11 | The App act control (capture evidence, RS entries) | DEL-01-04 → DEL-02-03 (App-side positive capture fixtures), DEL-04-03, DEL-04-01 | AAC | AAC §3, §4 | DEP-02-03-027 (X-1, held); mirror R2-01-04-a proposed in pass 2 |
| IF-12 | Native interaction view and scoped request/outcome checks | DEL-01-04 → DEL-09-02 | Before the joined request witness | Nothing is claimed beyond the cases run (§13) | DEP-09-02-012 (admitted) |

The SCC effect of NR-1…NR-3 was computed from DAG-003's two edge files (202
arcs, both layers): with any or all three added, the SCCs are unchanged
(sizes 2, 2, 2, 2, 3, 13; SCC-002 stays the same 13 members). Script and
output are recorded in the return file.

---

## 3. Rules that hold throughout

| # | Rule | Standing |
|---|---|---|
| NR-1 | **Native semantics.** A card offers the supplier's own answer forms and sends the supplier's own content, unchanged; no Chirality vocabulary replaces a request or an answer (REQ-001; V4-APP-04) | SETTLED (SoW REQ-001) |
| NR-2 | **Silence never answers.** No elapsed time, observer loss, window close, reload, reconnect or restart produces an answer, a decline or a grant (HOSTING H8, R3, R6) | SETTLED |
| NR-3 | **No automatic decline.** No App rule declines a waiting request after any period; the legacy `timed_out` form is never sent. A supplier's own resolution is shown as resolved by the supplier, never as an answer (HOSTING RT-10) | SETTLED (R17-9) |
| NR-4 | **Truthful origin.** The person's answers carry origin `person-via-interaction` and the actor as AAC §7 forms it; an App rule's decline or error is shown with its rule name; a decision made inside Codex is shown as Codex's (HOSTING R7, R9, §6.6) | DERIVED |
| NR-5 | **Unknown stays unknown.** A write attempt is not acknowledgment; a lost observation is *unknown*; nothing is back-filled (REQ-002; HOSTING H10) | SETTLED |
| NR-6 | **App-kept records are App-observed.** Conversation content is read back from Codex; the App keeps only its own records and pointers (supply records, capture evidence, run association) and labels them App-observed, never authority for what Codex holds | DERIVED (R17-4) |
| NR-7 | **No reaction to an arrival.** Nothing here is raised, opened, focused or notified because a checkpoint arrival was recorded (EXEC RC-4, SD-4); the act control is a standing facility (RC-6) | SETTLED (K1-1) |
| NR-8 | **Answers to questions are conversation.** An answer to `item/tool/requestUserInput` or `mcpServer/elicitation/request` is input to the agent, never act evidence (EXEC CAP-6) | ADOPTED (R4-12) |
| NR-9 | **Tool permission is not a reserved act.** An A14 answer of any kind never stands for A4–A7, A12, A13 or a checkpoint act (HOSTING R8; CAP-5) | SETTLED (D2, D3) |
| NR-10 | **Words.** ACT §9 and AS §9 DS-1…DS-6 govern every label; §4.2 LB-1…LB-4 apply them to cards | SETTLED (V-07) |

---

## 4. Request cards (OUT-001; REQ-001; AC-001; VER-001)

### 4.1 Kinds at 0.158.0 and how each is met

The 11 server-request kinds of the generated types (`ServerRequest.ts`,
`observed-in-generated-types`). Classification and origin class are HOSTING
§6.1's proposed partition (U-20), which names DEL-01-04 as co-owner for the
answer path; the card column is this file's position on that path.

| Kind | HOSTING class / R9 origin class | Card | What the person sees |
|---|---|---|---|
| `item/commandExecution/requestApproval` (`kind` `command` or `writeStdin`) | known-answerable / A14 | **Tool permission** | The command, working folder, reason, proposed rule amendments, and the forms offered (§4.2) |
| `item/fileChange/requestApproval` | known-answerable / A14 | **Tool permission** | The item's changes as the supplier reported them, the reason, any `grantRoot` (supplier-marked UNSTABLE) |
| `item/permissions/requestApproval` | known-answerable / A14 | **Permission grant** | The requested network and file-system permissions, reason, working folder; grant all, part or nothing, for the turn or the session |
| `execCommandApproval`, `applyPatchApproval` (legacy v1) | known-answerable / A14, if raised (whether they are raised on the v2 surface is not observed) | **Tool permission (legacy request)** | As above, with the legacy forms |
| `item/tool/requestUserInput` | known-answerable / person-input | **Question** | Each question's header and text, options, free-text where `isOther`, masked input where `isSecret`; "not blocking the turn" where `isBlocking` is false |
| `mcpServer/elicitation/request` (modes `form`, `openai/form`, `openaiForm`, `url`, `openai/userVerification`) | known-answerable / person-input | **Input request** | The message and requested fields; for `url`, the address (never opened by the App); for `openai/userVerification`, the challenge, which only the person completes. Requester shown "MCP server ‹name› or the agent (not established)" (EXEC RC-5) |
| `item/tool/call` | known-app-unsupported | None: an information line | "The agent called an App tool the App does not offer: answered with an error by rule `app-rule:no-dynamic-tools`" |
| `account/chatgptAuthTokens/refresh` | known-app-unsupported unless DEL-01-05 adopts external-token login | None: an information line | As above, rule `app-rule:external-token-login-not-adopted` (DEL-01-05 may change the class) |
| `attestation/generate` | unfamiliar while `requestAttestation` is false; else known-app-unsupported | None: an information line | "Unrecognized request from Codex (‹method›): answered with an error" (REQ-001: received unknown-request errors stay explicit) |
| `currentTime/read` (experimental) | unfamiliar unless the opt-in is declared; then a named service kind | None: an information line | "Codex asked for the time; answered by rule `app-rule:current-time`" |
| Any other method | unfamiliar | None: an information line | As `attestation/generate` |

**Inference.** At 0.158.0 the generated `ToolRequestUserInputParams` and its
question and answer types carry the comment "EXPERIMENTAL" although the method
is in the stable request set; the card treats it as present whenever received.

### 4.2 What a card offers (FO) and the words it uses (LB)

| # | Rule |
|---|---|
| FO-1 | When a command request carries `availableDecisions`, the card offers **exactly** those forms, in that order, and no other. OBS-1b observed it arriving without the experimental opt-in and listing `accept`, `acceptWithExecpolicyAmendment`, `cancel` under approval policy `untrusted` (`observed`, HOSTING §10.1 OB-5). An answer the request does not offer is refused `invalid-answer` by the register (R5); the card never builds one |
| FO-2 | Without `availableDecisions`, the card offers the generated forms (`CommandExecutionApprovalDecision`: `accept`, `acceptForSession`, `acceptWithExecpolicyAmendment`, `applyNetworkPolicyAmendment`, `decline`, `cancel`), the two amendment forms only when the request proposes an amendment (`proposedExecpolicyAmendment`, `proposedNetworkPolicyAmendments`), each carrying the proposed content unchanged |
| FO-3 | Legacy requests offer `ReviewDecision` forms except `timed_out`, which is never a person's answer (NR-3) |
| FO-4 | A permission request offers: grant the requested profile; grant a subset (the person removes entries); grant nothing (§4.3). Scope `turn` or `session` (`PermissionGrantScope`) is the person's choice, `turn` shown first. `strictAutoReview` is offered only as the supplier names it, off by default |
| FO-5 | A question card collects one answer list per question identity (`ToolRequestUserInputResponse`); options as given; free text only where `isOther`; a question may be left unanswered |
| FO-6 | An elicitation card offers `accept` with content (form modes: fields as the requested schema names them), `decline`, `cancel` |

The supplier's own descriptions of the command decisions
(`CommandExecutionRequestApprovalResponse.json`, `observed-in-generated-types`):
`decline` — "User denied the command. The agent will continue the turn."
`cancel` — "User denied the command. The turn will also be immediately
interrupted." Their live effect is not observed at the pin.

| # | Label rule (applies ACT §9, AS DS-1; V-07) |
|---|---|
| LB-1 | A tool-permission card is titled "Tool permission: ‹what›" and its App words are "Allow once", "Allow for this session", "Allow, and add the proposed rule to your Codex exec policy", "Apply the proposed network rule for this host", "Don't allow; the agent continues the turn" (`decline`), "Don't allow, and interrupt the turn" (`cancel`). The native value is shown beside the words, verbatim, as a code span |
| LB-2 | The App's own words on a tool-permission card never include "accept", "approve", "approval" or "approved"; the native values that contain them appear only as quoted supplier names. The prototype checks every A14 card (C-6) |
| LB-3 | Every A14 card says, once and plainly, that it is tool permission only and stands for no check, acceptance, engineering approval or reliance (NR-9) |
| LB-4 | Question and input-request cards say that the answer goes to the agent as conversation input and is not a recorded act (NR-8). A question card also offers a plain entry "Open the App act control" on every question card, whether or not an arrival is current; it is never pre-filled from an arrival and never opened by itself (CAP-6: "The App may respond by presenting its own CAP-2 control"; NR-7) |

### 4.3 The explicit decline, per kind (DM)

REQ-001 asks for an explicit decline. At 0.158.0 two kinds have no negative
answer form; for them this file proposes the native "nothing given" content.

| # | Kind | Decline sent | Standing |
|---|---|---|---|
| DM-1 | Command | `decline` if the request offers it; otherwise `cancel` if offered, labelled "Don't allow, and interrupt the turn"; otherwise none, and the card says the request offers no negative form | Native form. Under `untrusted` the only negative form offered was `cancel` (OB-5): declining then interrupts the turn, per the supplier's description |
| DM-2 | File change | `decline` (or `cancel`, as DM-1) | Native form |
| DM-3 | Legacy | `denied` with an empty `rejection` text unless the person writes one; `abort` labelled "Don't allow; the agent waits for your next message" | Native form (legacy descriptions) |
| DM-4 | Permissions | `{permissions: {}, scope: "turn"}`, labelled "Grant nothing" | **PROPOSED**; the effect of an empty grant is not observed |
| DM-5 | Question | `{answers: {}}`, labelled "Decline to answer" | **PROPOSED**; the agent's handling of an empty answer map is not observed |
| DM-6 | Elicitation | `{action: "decline", content: null, _meta: null}`; `cancel` offered separately | Native form |

The person's path never sends a protocol error: HOSTING §6.4 gives the
"explicit error" operation to the boundary and named App rules only. DM-4 and
DM-5 need the register to treat those contents as negative forms (join J-H3).

### 4.4 Card states (CS) over the register states

One card per register entry. The card's state is a function of the entry
(HOSTING §6.2.1); the card adds the person's view and nothing else. Every
register row maps to one card transition; the prototype reached all 13 rows
and checked every entry it produced against HOSTING's PROPOSED entry schema
(R-15, R-16).

| Register row (HOSTING §6.2.1) | Entry state | Card state | Label (the person's words) |
|---|---|---|---|
| RT-01 | `received` | CS-0 | not shown yet |
| RT-02 | `errored`, origin `app-explicit-error` | CS-E | "Unrecognized request from Codex (‹method›): answered with an error" |
| RT-03 | `errored`, origin `app-rule` | CS-U | "Codex asked for something the App does not provide (‹method›): answered with an error by rule ‹rule›" |
| RT-04 | `outstanding` | CS-1 | "Waiting for your answer" |
| RT-05 | `outstanding` (answer refused) | CS-1 | "Waiting for your answer (last answer not taken: ‹reason›)", the reason in words: *no such request* "this request is no longer known"; *generation closed* "Codex restarted since this was asked"; *already resolved* "Codex already resolved it"; *already settled* "already answered"; *invalid answer* "that answer is not one this request offers" |
| RT-06 | `settling` | CS-2 | "Sending your answer: not yet written to Codex" |
| RT-07 | `answered`, acknowledgment not observed | CS-3 | "Your answer was written to Codex; Codex has not confirmed it" |
| RT-12 | `answered`, acknowledgment observed | CS-3a | "Your answer was written; Codex reported the request resolved" |
| RT-08 | `declined`, origin the person | CS-4 | "You declined; written to Codex; Codex has not confirmed it" |
| RT-13 | `declined`, acknowledgment observed | CS-4a | "You declined; written; Codex reported the request resolved" |
| RT-08 | `declined`, origin `app-rule` (for example `app-rule:on-stop`, if DEL-01-02 chooses it under HOSTING U-10) | CS-4r | "Declined by App rule ‹rule›, not by you" |
| RT-09 | `settle-write-failed` | CS-5 | "Your answer could not be written; whether Codex received it is unknown" |
| RT-10 | `resolved-by-supplier` | CS-6 | "Resolved by Codex before you answered (cause: ‹as reported› / not reported)" |
| RT-11 | `ended-unanswered` | CS-7 | "Ended unanswered: the Codex process ended" (with "when you quit" where DEL-01-02's stop record says so, K-4) |

**Transitions of the card itself.** CS-1 → CS-2 only by the person's answer
from a presented card; every other change follows the register. A card in
CS-1 stays in CS-1 for any length of time (NR-2, NR-3); the prototype keeps
an unanswered question waiting through a simulated day (R-7). Closing,
reloading or reopening the view rebuilds the same cards from "list
outstanding" (R-8). A supplier-internal decision (HOSTING §6.6; the user's
own `approvalsReviewer` setting) creates no card; its notifications are shown
in the conversation as "decided inside Codex by your Codex setting", origin
`supplier-internal`, never as the person's answer.

**Re-raised after a restart (OBS-2 pending, O-2).** Whether the supplier raises
a pending request again after a restart and resume is not observed. If it
does, the new request is a new entry of the new generation and a new card;
the old card stays CS-7. The card may say "asked again after restart" only
when the thread, turn and item references are equal (an observed equality,
never a guess).

### 4.5 The answer submission (data) and secret values (SE)

A card hands the register's *answer* operation one
[`nir.answer-submission.schema.json`](nir.answer-submission.schema.json)
object: request identity, generation, method, the native answer unchanged,
`submittedAs` (*answer* or *decline*), origin `person-via-interaction` with the
actor reference (AAC §7: "person:‹name›/‹OS account›/‹Codex account›
(identity not verified)"), the names of the forms the card showed, the time,
and `secretValuesPresent`.

| # | Rule |
|---|---|
| SE-1 | An answer to a question with `isSecret` is masked on screen, never shown again after sending, and marked `secretValuesPresent: true` |
| SE-2 | The register and its custody must not keep secret values readable after the reply is written (join J-H4 with HOSTING §6.1 *settlement*; DEL-01-02's persistence) |
| SE-3 | No App record (supply record, capture evidence, RS entry) ever contains an answer value to a secret question |

### 4.6 Operating sequence: answer a request (SQ-R)

| Step | Action | By | Record | Failure: what fails · who reports · record · next |
|---|---|---|---|---|
| R-a | A server request arrives; the register makes its entry (R1) | DEL-01-01 | Register entry | Nothing for this file; unfamiliar or unsupported kinds become CS-E / CS-U |
| R-b | The card is built from the entry and shown | DEL-01-04 | — | No view open: nothing is lost; the card appears when a view opens (R6). The App may notify that a request waits; that notice is about a supplier request, never about an arrival (NR-7) |
| R-c | The person chooses a form | Person | — | The person closes the card: nothing is sent (CS-1 stays) |
| R-d | The submission is handed to *answer* | DEL-01-04 | — | Refused (U-26 order) · the register · none · CS-1 with the reason; the person may choose again |
| R-e | The reply is written | DEL-01-01 | Settlement, write result | Write fails · the register · `settle-write-failed` · CS-5; no automatic resend |
| R-f | Acknowledgment observed or not | DEL-01-01 | Acknowledgment observation | Not observed · — · CS-3/CS-4 stays "not confirmed" |
| R-g | A14 evidence | DEL-01-01 → DEL-04-03 | RS `tool_permission_settlement` (R13) only | Never a human-act record (NR-9) |

---

## 5. Turns and outcomes (OUT-002; REQ-002; AC-002; VER-002)

### 5.1 Turn outcome states (TO)

Sources: `TurnStatus` = `completed` · `interrupted` · `failed` · `inProgress`;
`Turn.error` only when failed; `thread/status/changed` with active flags
`waitingOnApproval`, `waitingOnUserInput` (`observed-in-generated-types`), and
DEL-01-02's recovered state (IF-2).

| # | Shown as | When | Never |
|---|---|---|---|
| TO-0 | "Not started" (with §5.4's reason where it applies) | No turn was started | — |
| TO-1 | "In progress" | `inProgress` observed while observation is live | — |
| TO-2 | "In progress: Codex waits for your tool-permission answer" / "…for your answer to a question" | Active flag `waitingOnApproval` / `waitingOnUserInput` | "Waiting for the person" as a state of a workflow run, or any checkpoint hold wording (SD-4). The flag is the supplier's report about its own turn |
| TO-3 | "Completed" | `completed` observed | Any statement about descendants (§5.5) |
| TO-4 | "Interrupted (‹cause›)": "interrupted by you" (the person's interrupt, R17-3 op 1), "interrupted by quit" (K-4), "interrupted after your `cancel` tool-permission answer", or "cause not observed" | `interrupted` observed; the cause only where DEL-01-02's record or this App's own answer shows it | "Stopped" (App v3 used it, §10); a run end |
| TO-5 | "Failed: ‹supplier's message›" | `failed` with `Turn.error` | A cause of the App's own |
| TO-6 | "Outcome unknown: observation was lost before Codex reported an end" | Observation lost (supplier exit, connection loss) with no terminal status observed, or DEL-01-02 cannot settle it after recovery | Completed, interrupted or failed by inference |
| TO-7 | "Interrupted by quit; resume?" | After relaunch, for turns K-4 recorded "interrupted by quit"; the resume offer is DEL-01-02's | An automatic resume |

**Labels from DEL-01-02.** Where DEL-01-02 supplies an outcome label for a
turn (its node-D1 draft, read in progress, names for example *interrupted by
the person*, *completed (stop requested)*, *interrupted by quit (final status
not observed)*), the view shows that label and, after a relaunch, Codex's own
reported status beside it. TO-0…TO-7 constrain the wording: never "stopped"
for an interruption, unknown stays unknown, no cause the record does not show.

What OBS-2 settles here: the turn status and items after `turn/interrupt`, and
what happens to a pending request then (O-1) — **OBS-2 pending**; until then
TO-4 "interrupted by you" rests on DEL-01-02's record of the person's act and
on `observed-in-generated-types` only.

### 5.2 The three stop operations, as presented (R17-3)

DEL-01-02 owns the definitions; this file presents them and keeps them apart.

| Operation (R17-3) | Where the person meets it | What the view shows afterwards |
|---|---|---|
| Interrupt a turn | The turn's "Interrupt" control (DEL-01-02's operation, `turn/interrupt`) | TO-4 "interrupted by you"; the conversation and any workflow run continue; never "run ended" |
| End a run | The run panel's "End run" control (DEL-01-02 / EXEC run end) | The run-ended event from the record (§9); turns keep their own outcomes |
| Stop the Codex process | Quit, or the App's "Stop Codex". With live work the App asks first (K-4): the question lists the live turns, the waiting requests and active delegated agents as DEL-01-02 supplies them, and has no timeout | Live turns "interrupted by quit" (K-4); waiting cards CS-7, or CS-4r if DEL-01-02 chose an App decline at stop (its node-D1 draft proposes none, HOSTING U-10) |

Observer loss (window close, reload) and connection loss are not stops and
show nothing of the kind.

### 5.3 Reload, reopen and relaunch (SQ-V)

| Step | Action | Failure: what fails · who reports · record · next |
|---|---|---|
| V-a | The view asks DEL-01-02 for the recovered state of the conversation (IF-2) | Not available · DEL-01-02 · — · the view says "recovering" and shows nothing as current |
| V-b | Turns are drawn with their recovered status and cause; each recovered item is marked "recovered at ‹t›" where DEL-01-02 marks it | A status DEL-01-02 cannot settle · TO-6 |
| V-c | Cards are rebuilt from the register's outstanding list and its settled entries for the conversation | Entries of a closed generation · CS-7 |
| V-d | App-kept items Codex does not keep in history (for example plan checklist revisions, R17-4) are shown by their owners as "not recoverable after relaunch"; this file shows nothing in their place | — |

### 5.4 Conversation start display (K-3)

| # | Rule |
|---|---|
| ST-1 | A new App conversation shows **"No model selected"** until the person chooses one; no model is applied from Codex's own configured default or from any earlier conversation (K-3, owner's answer) |
| ST-2 | Where DEL-01-05 reports a last explicit choice for this project, the start display offers it as a button reading "Use ‹model› via ‹provider› (your last choice for this project, ‹date›)". It is applied only when the person presses it |
| ST-3 | Sending a message with no model chosen sends nothing to Codex; the message stays in the composer and the display reads "not started — no model selected" (R15-1's wording, reused per R17-2) |
| ST-4 | The chosen model, provider and access mode are shown in the conversation header as DEL-01-05 reports them; the observed destination per turn is DEL-01-01's (HOSTING §8.3) and DEL-04-03's to record |

The selection states and the last-choice store are DEL-01-05's (IF-10; NR-3
new row). This file only places them.

### 5.5 Delegated agents (descendants)

Primary-turn completion never implies that delegated agents finished
(REQ-002). Where the supplier reports delegated agents (the stable thread item
`collabAgentToolCall` carries `agentsStates` with `CollabAgentStatus`
`pendingInit` · `running` · `interrupted` · `completed` · `errored` ·
`shutdown` · `notFound`, "when available"; `observed-in-generated-types`), the
turn line adds "‹n› delegated agent(s) last reported running" or "…with no
reported state", and links to DEL-01-03's delegation view, which owns
everything else about them (K-5, K-10). The facts reach this view through
DEL-01-02's recovered state and the native delivery (IF-2, IF-3); no row to
DEL-01-03 is needed (R17-10). What a child produces and whether its thread is
readable is **OBS-2 pending** (O-4).

---

## 6. Attachments and the identity of supplied content (OUT-002; REQ-003; AC-003; VER-003)

**Supplier facts (`observed-in-generated-types`).** At 0.158.0 a turn's input
is a list of `UserInput`: `text`; `image` by `url` or by supplier `fileId`;
`localImage` by `path`; `audio` by `url`; `localAudio` by `path`; `skill`
{name, path}; `mention` {name, path}. The supplier reads a path itself.
Separately, `thread/attachment/add|list|remove` (stable) persists
{`attachmentType`, `identityKey`, `payload`} per thread with outcome
`created` · `existing`; its semantics are not observed.

**Consequence (inference).** For path forms, the bytes Codex reads are not
observable from the App, and nothing at the pin reports provider adoption. The
App can only state what it read and when.

| # | Rule |
|---|---|
| AT-1 | When the person selects a file, the App takes its content identity (method designation carried; no algorithm chosen: RS U-04, HOSTING U-08) and shows it with the name |
| AT-2 | When the host writes the turn input, it takes the identity again. If it differs from the selection's, the file is **not sent**: the card says "content changed since you selected it; confirm the current content", and the person confirms the current content or removes it. A file missing at that moment is held the same way |
| AT-3 | One [`nir.attachment-supply-record.schema.json`](nir.attachment-supply-record.schema.json) record per supplied item: the identities at selection and submission, the form used, the path or reference, the turn, and the fixed labels "supplier read: not observed: Codex reads the path itself" and "provider adoption: not observed" |
| AT-4 | Same-named items with different content are different attachments, shown with distinguishing identity prefixes; nothing is merged or substituted by name |
| AT-5 | A URL or supplier `fileId` is recorded as given, with identity "not obtainable (the App does not fetch it)" |
| AT-6 | A later check (the person opens the item, or the view re-checks on display) records "unchanged since supplied" or "changed after it was supplied; what Codex read is not observed"; it never rewrites the supply record's earlier identities |
| AT-7 | `thread/attachment/*` is not used by this design: its semantics are not observed and no requirement needs it (UNRESOLVED U-NIR-4) |
| AT-8 | A draft handed to an ordinary conversation for trying out (K-7) is shown as "draft ‹name› at content ‹id› — not a registered workflow; this conversation is not a workflow run", with a supply record of form `draft-package`. How the draft reaches the conversation is DEL-02-02's (with DEL-02-04 for guidance carriage) |

**Two ways to narrow the gap between the App's read and Codex's read (options;
not chosen: TBD-003 keeps attachment storage open, REQ-003 forbids choosing
it here).**

| Option | What is supplied | For | Against |
|---|---|---|---|
| AO-1 (this design's default) | The original path; identity at selection and submission | No copy; no storage choice | A change between the App's read and Codex's read is not detected |
| AO-2 | A copy in an App-held, content-addressed store, whose path is supplied | The bytes Codex reads are the bytes the App identified, unless the copy itself is altered | A storage location and lifecycle must be chosen (TBD-003); the agent sees a different path |

**Sequence (SQ-A).** Select (AT-1) → compose → write the turn input (AT-2,
AT-3) → turn runs (Codex reads) → later checks (AT-6). Failures: identity not
obtainable at selection (unreadable file) · the App · nothing sent · the
person picks again; identity differs at submission · the App · held, not sent
· the person confirms or removes; the supply record cannot be written · the
App · the item is still held until the record is written, so the App never
sends what it has not recorded.

---

## 7. Draft receiving contract (OUT-004; REQ-004; AC-004; VER-004)

**What DEL-01-04 receives** from the workflow workspace (DEL-02-02; IF-4):
DEL-02-02's `draft_transition` and `draft_reference` (WR-v0.1 §5.1, §8;
`workspace-registration.schema.json`, node D5). DEL-02-02 owns them.
[`nir.draft-transition.schema.json`](nir.draft-transition.schema.json)
restates `draft_transition` **with D5's own element names and values**, so
the two compare line by line, and adds the two elements this view needs that
D5's shape does not yet carry (a request to DEL-02-02, join J-W1):

| Element (D5's name) | Meaning for the view |
|---|---|
| `draft` {`draft_location`, `draft_root`, `name`} | Where the draft is; a draft has no workflow identity (EXEC TR-1, HR-3) |
| `event` | *written* · *changed* · *review shown* · *review stale* · *registration refused* · *registered* · *registration not completed* · *removed* |
| `from`, `to` | WR §5.1 draft states: *absent* · *draft* · *not valid* · *under review* · *changed since review* · *registered, unchanged since* · *removed* |
| `content` | The draft's content identity with method (WD §6.1 RV-1…RV-5; algorithm open, WD U-03) |
| `disposition` | WR's codes: *new workflow*, *new revision*, *in place*, or *refused: …* (K-6: *refused: name taken* asks for a new name) |
| `cause`, `time`, `attribution` | As WR §8 states them (*file change item* with thread and item, *app action*, *not observed*) |
| **`a15_record`** (requested) | For *registered* and *registration not completed*: the RS A15 record the App act control wrote at capture (K-8) |
| **`revision`** (requested) | For *registered*: the revision identity. Until DEL-02-02 carries these two, the view reads them from WR's `library_entry` |

Per R17-11 an A15 names its subject by the **reviewed draft** and, for a new
revision (K-6), the **prior revision**; *derived-from* stays WD's relation
for the parent workflow identity and the view never uses it for an A15.

**Display (DR) of each state the workspace reports:**

| WR state (`to`) | Shown as |
|---|---|
| *draft* | "draft — not registered" (REQ-004) |
| *not valid* | "draft — not valid for registration", with WR's findings |
| *under review* | "under review", with the reviewed content identity; the App act control's A15 offer is available (AAC §4.2) |
| *changed since review* | "changed since review — review again before registering" (K-8; WR RB-3) |
| *registered, unchanged since* | "registered as ‹revision› by ‹person› (identity not verified) at ‹t›", citing the A15 record; earlier revisions remain (K-6) |
| *removed* | "removed" |
| While the act control has captured an A15 and the workspace has not yet reported | "registration in progress" (from the act control's own state, AAC §3) |
| After *registration not completed* | "draft — registration not completed: ‹cause›; the act is recorded and had no effect" |

**Accepted transitions** are WR §5.1's (prototype `DRAFT_ALLOWED`); the view
checks that `from` equals the state it shows and re-reads WR's
`draft_reference` when it does not. **Refused by the view** (never shown as
transitions): *registered* without the A15 record and the revision;
*registered* for content other than the reviewed content; *registration not
completed* without the recorded act; any local UI action that would make a
draft reviewed or registered (REQ-004: no local transition invents review or
registration). K-7: a draft is never shown as running a workflow; trying it
is an ordinary conversation (AT-8).

**Where the complete journey is verified.** DEL-02-02 owns the create, try,
review, register, reuse and refine journey and its witness (CLM-004); this
file's cases cover the native view only (§13).

---

## 8. Act presentation (REQ-005; AC-005; VER-005)

What the App shows of human acts, from DEL-04-03's record-out (IF-7), with
DEL-04-01's words (IF-6) and DEL-04-02's display rules (IF-8):

| # | Rule | Source |
|---|---|---|
| AP-1 | One label per act kind: "mark checked" (A4), "accept"/"rejected the item" (A5/A10), "approve" only for A6 with its accountable person, "rely" (A7), "set grant" (A12), "register workflow revision" (A15), "tool permission" (A14) | ACT §9; AS DS-1 |
| AP-2 | Decision actor and recorder are both shown when they differ; an App-captured act names the person "(identity not verified)" and the recorder "App interface" | AS DS-2; K1-4 |
| AP-3 | No act is shown without a record carrying capture evidence. A14 settlements appear in the conversation as tool permission, never in an act list; answers to questions are conversation | AS DS-3; NR-8, NR-9 |
| AP-4 | At an arrival: "by earlier act ‹act› at ‹t›" (K1-2), "answered by ‹n› acts" (K1-3), "prior act not counted — ‹reason›" | EXEC RC-7; RS L-13 |
| AP-5 | Lapse as recorded: "act lapsed at ‹t›" after the resume point; *lapsed* only after run end; *not yet evaluated* never shown as current | RS §7; AS §8 |
| AP-6 | An act-declined event reads "declined ‹act kind›", never as the act; a run-ended event is shown apart and resolves nothing | AS DS-5 |
| AP-7 | No act is shown as a prerequisite of another; an independently evidenced act without an acceptance is shown as it is | AS DS-4; ACT §2 |
| AP-8 | Agent text that claims a check, approval or certification is conversation, never an act or a standing | V-08 |
| AP-9 | An act captured after its run ended is marked "after run end" | RS §3 |

The positive faithful-recording case of VER-005 needs an actual act by a
person (DEP-01-04-019); the App act control (AAC) is the construction that
case uses on App content.

---

## 9. Checkpoint and standing display in the App (R17-7)

DEL-04-02 defines the components and their meaning (AS §13 K-5 "Checkpoint
overlay", K-6 "Standing facets"; AS §4 OV-1…OV-7, §8, §9) and DEL-02-03 the
display meanings of the current-phase recorder (EXEC §2.4.4 SD-1…SD-5). This
file places them in the App and owns their behaviour there. For App surfaces
this is AS §13's CS-3 ("The App builds K-1…K-7 for App surfaces"); where the
code lives stays OI-014's.

| # | Placement and behaviour |
|---|---|
| PD-1 | **Run panel** beside a conversation that is a workflow run: the checkpoint list at run start (SD-1, OV-1), each arrival's record label in words (SD-2, OV-2), where the act is performed (SD-3), "continued past ‹checkpoint› before ‹act›" as information (SD-5, OV-6) |
| PD-2 | **Act log** for acts outside any run (for example A15, App-file acts) with the K-6 human-act facet (AS §8) |
| PD-3 | **Standing facets** (K-6) beside results and outputs shown in the run panel |
| PD-4 | The panel and log change only when the record changes. Nothing is modal; nothing is notified, focused or opened because of an arrival (SD-4, NR-7) |
| PD-5 | SD-3's "App act control" entry on an arrival row opens the control only when the person clicks it; the offer may carry the arrival's declared act kind, subject, scope and purpose, because the person chose to act on that arrival. **INTEGRATION reading, open to the integrator:** opening the control from the person's own click is not a reaction to the arrival under EXEC RC-4, since the arrival changes neither the facility nor what anyone is sent |
| PD-6 | Never shown: "held", "blocked", "paused", "waiting for the person" as a run state; a hold-support value; *unsupported* for a hold reason (SD-4, OV-3). The grant display and the checkpoint indicator never merge |
| PD-7 | The display compares itself with the record-out (AS §6 K-3): *missing in record* and *missing in display* are shown, never hidden |

---

## 10. Optional reuse of the App v3 exemplar (REQ-007; CLM-006)

v3 is historical evidence of what was built, never a v4 commitment. Files read
by head and grep in `projects/chirality-app-dev/frontend/src`.

| v3 source (historical) | What it did | Disposition | Receiving gaps to close if reused |
|---|---|---|---|
| `lib/harness/server-request-answer.ts` | Translated answers to `{kind: 'approval', verdict: 'allow'\|'deny'\|'allowForSession'}` (lines 18–21) | **Not reusable as is**: a translated vocabulary (NR-1; REQ-001) | Send native content (§4.5) |
| `components/shell/request-card.tsx` | Cards for approval, user input and elicitation; `acceptForSession` only when offered | Behaviour reference | FO-1 exact forms; DM-1…DM-6; LB-1…LB-4; secret handling SE-1…SE-3 |
| `lib/shell/turn-phase.ts` | Phases `idle · preparing · working · waiting · reconnecting · stopping`; outcomes `completed · interrupted · failed · unknown`; "interrupted" labelled "Stopped" | Behaviour reference for TO-1…TO-6 | Never "Stopped" for an interruption (R17-3); cause shown only when observed; descendants (§5.5) |
| `lib/harness/attachment-resolver.ts`, `ui-attachments.ts`, `native-attachments.ts` | Path picker limited to the project root and nine extensions; size limits; no content hashing found (S1-B §A.5) | Behaviour reference for selection limits only | AT-1…AT-6 identity and substitution handling |
| `lib/harness/workflow-drafts.ts`, `components/woven-dialogue/workflow-draft-review.tsx` | Draft with a review token over the package bytes; registration posts the token | Evidence that content-bound review works; the token is not a CAP-4 control (any local caller holding it could register; S1-C §A.4 item 4, inference) | Registration through the App act control (K-8; AAC) |

---

## 11. Excluded acts and owners (REQ-006; AC-006; VER-006)

| Excluded act | Owner (ScopeOfWork CLM) | Interface here |
|---|---|---|
| Supplier pin, generated types, protocol qualification | DEL-01-01 (CLM-002) | IF-1, IF-3 consume |
| Register custody, settlement, recovery, stop definitions | DEL-01-02 (CLM-003; R17-3) | IF-1, IF-2 consume; §5.2 presents |
| Plan, tool and delegation views | DEL-01-03 (CLM-003) | §5.5 links only |
| Account, provider and model selection | DEL-01-05 | IF-10 consumes; §5.4 places |
| Workflow workspace, review, the registration itself, catalog, selection | DEL-02-02 (CLM-004) | IF-4, IF-5; the act control captures A15 (K-8), DEL-02-02 registers |
| Policy and act meanings | DEL-04-01 (CLM-005) | IF-6 |
| Display component meanings | DEL-04-02 (R17-7) | IF-8 |
| Record format, writer, reader | DEL-04-03 (CLM-005) | IF-7; the act control writes through the writer |
| Unresolved policy decisions; OI-021 additions | Owner with App/SWB contract owners | §12 |
| Every human act (A4–A7, A10, A12, A13, A15), professional reliance | The person; the accountable professional | Presented (§8) and offered (AAC); never performed or inferred |
| OI-008 placement, OI-014 shared placement | App implementation owner; App/shared contract owners | §1.1, §9 state requirements only |

No row promotes a presenter or recorder into a decision actor.

## 12. Open choices at their owner and point of need (REQ-007)

| Item | Owner | Point of need | Effect here |
|---|---|---|---|
| TBD-001 OI-001 residue, OI-021 additions | Owner with App/SWB contract owners | Before operation-policy production contracts | Labels come from ACT V-07; additions fill slots |
| TBD-002 OI-002 | Ruled (D3) | — | NR-9; LB-3 |
| TBD-003 OI-008 process division; attachment storage | App implementation owner | Before architecture production contracts | §1.1 placement PROPOSED; AO-1/AO-2 open |
| TBD-004 OI-012 implementation/qualification pin | App implementation owner | Before protocol generation and qualification | Designed at 0.158.0 only |
| TBD-005 OI-014 shared placement | App/shared contract owners | Before structural/production allocation | §9 places App surfaces; code placement open |
| U-NIR-1 Effect of the PROPOSED empty-answer and empty-grant declines (DM-4, DM-5) | App implementation owner with DEL-01-01 (U-20) | Before card implementation | Not observed; not in OBS-2's list |
| U-NIR-2 AO-1 or AO-2 | App implementation owner | Before attachment implementation | AO-1 assumed |

---

## 13. Verification

### 13.1 Designed cases

"Needs": *model* = runs on this file's prototype; *fixture* = a recorded or
constructed exchange; *double* = HOSTING's supplier double; *person* = an
actual act; *candidate* = an App build. No case can pass a VER criterion
until a candidate exists.

| Case | Setup | Action | Expected | Needs | Prototype (2026-10-01) | Serves |
|---|---|---|---|---|---|---|
| VC-NIR-01 Card per kind | 11 kinds, capabilities off/on | Build cards | 7 cards, 4 information lines; classes as §4.1 | model; candidate for rendering | C-1, C-2 pass (model) | VER-001 |
| VC-NIR-02 Forms offered | OB-5-shaped request; one without `availableDecisions` | Build card | Exactly the listed forms; generated forms with amendments only when proposed | model, fixture (OBS-1b transcript) | C-3, C-5 pass (model) | VER-001 |
| VC-NIR-03 Words | Every A14 card | Read App prose | No "accept/approve/approval/approved" as App words | model; candidate | C-6 pass (model) | VER-001, VER-005 |
| VC-NIR-04 Explicit decline | Each card kind | Decline | DM-1…DM-6 content; `cancel` labelled as interrupting | model; candidate + double for effect | C-4, C-7, R-5, R-11 pass (model); DM-4/DM-5 effect not observed | VER-001 |
| VC-NIR-05 Silence and closure | Waiting question | No answer for a day; close and reopen the view | Still waiting; same card; no answer written | model; candidate for real closure | R-7, R-8 pass (model) | VER-001 |
| VC-NIR-06 Unknown request | Unfamiliar and unsupported kinds | Receive | Explicit error shown CS-E/CS-U | model, double (HOSTING VC-03) | R-15 pass (model) | VER-001 |
| VC-NIR-07 Attempt ≠ acknowledgment | Answer; acknowledgment later; write failure | Walk | CS-3 → CS-3a; CS-5 | model, double | R-3, R-6 pass (model) | VER-001, VER-002 |
| VC-NIR-08 Refusals | Second answer, closed generation, unknown identity, resolved, invalid form, App-rule affirmative | Answer | U-26 reasons shown; card waits | model | R-1, R-4, R-10, R-12, R-13, R-14 pass (model) | VER-001 |
| VC-NIR-09 Register coverage | All RT rows | Walk | 13/13 rows; entries valid against HOSTING's schema | model | R-15, R-16 pass (model) | VER-001 |
| VC-NIR-10 Outcomes | Status set; observation lost; causes; running descendant | Label | TO-1…TO-6; never "stopped"; descendants not implied | model; OBS-2 (O-1, O-4); candidate | O-1…O-3 pass (model) | VER-002 |
| VC-NIR-11 Reload and relaunch | Live turn with a waiting card | Reload; relaunch after quit | Recovered state drawn; cards rebuilt; "interrupted by quit" with resume offer | candidate; DEL-01-02 interface; OBS-2 (O-2) | Not run | VER-002 |
| VC-NIR-12 Start display | No selection; last choice exists | Open; send | "No model selected"; offer not applied; message kept | model; candidate | O-4 pass (model) | VER-002 (K-3) |
| VC-NIR-13 Attachment identity | Same file; changed file; same name different content; missing file | Select and submit | Sent; held; two items; held. Records valid | model; candidate | A-1…A-5 pass (model) | VER-003 |
| VC-NIR-14 Draft transitions | WR §5.1 walk: written, review shown, review stale, review shown, registered; name taken; registration not completed | Receive | WR states shown; stale review; refusals of invented registration | model; DEL-02-02's interface (D5) | D-1…D-6 pass (model) | VER-004 |
| VC-NIR-15 Act presentation | Record-out with direct capture, faithful record, earlier act, joint answer, lapse, decline, A14, agent claim | Display | AP-1…AP-9 | fixture (RS examples), candidate | Not run (display) | VER-005 |
| VC-NIR-16 Positive act case | A person, an App file, the act control | Act; then change the file | Direct-capture record, actor ≠ recorder; then lapse | **person** (DEP-01-04-019), candidate | Model only: AAC K-4, K-6 | VER-005 |
| VC-NIR-17 Receiving review | This file | Trace REQ-006 exclusions; open pairs | §11, §12 complete | review | — | VER-006 |
| VC-NIR-18 Fixture suite | All of the above on a candidate | Run | Simulated vs observed reported | candidate | — | VER-007 |
| VC-NIR-19 Formats | Three schemas and examples | Validate | Valid valid; invalid invalid | model | S-1…S-4 pass | OUT-003 |

### 13.2 Local prototype (R17-1; R12-3)

`prototype/` (Python 3 standard library; read-only imports of DEL-04-03's
`minischema.py` and `record_store.py` and DEL-01-01's `jsonschema_subset.py`).
Command: `python3 run_cases.py` in `prototype/`. Run on 2026-10-01, macOS
Darwin 25.6.0 arm64, Python 3.13.7: **103 checks, 0 failed**, exit status 0;
output in [`prototype/results/RUN_2026-10-01.txt`](prototype/results/RUN_2026-10-01.txt).
The installed `jsonschema` 4.26.0 (already present; nothing installed) gave
the same verdicts on all schema examples (S-4). A pass is evidence that the
rules run as written, not a VER pass.

## 14. Data formats (PROPOSED; JSON Schema 2020-12)

| Schema | Handed from → to | Examples |
|---|---|---|
| [`nir.answer-submission.schema.json`](nir.answer-submission.schema.json) | DEL-01-04 card → register *answer* (DEL-01-01 / DEL-01-02) | `.example.valid.json` (1), `.example.invalid.json` (6 cases) |
| [`nir.attachment-supply-record.schema.json`](nir.attachment-supply-record.schema.json) | DEL-01-04 → conversation view, DEL-02-02 (draft attachments), DEL-04-03 (cited as evidence) | 1 valid, 4 invalid |
| [`nir.draft-transition.schema.json`](nir.draft-transition.schema.json) | DEL-02-02 → DEL-01-04 (D5's `draft_transition` with D5's names, plus two requested elements) | 1 valid, 5 invalid |

The act control's two formats are AAC §5. All five use the keyword subset
DEL-04-03's prototype validator accepts, so one validator checks them with
RS's own schema.

## 15. Findings

| # | Finding | Disposition |
|---|---|---|
| F-NIR-1 | Two answerable kinds have no native negative form at 0.158.0 (`requestUserInput`, `permissions/requestApproval`) | DM-4, DM-5 PROPOSED; J-H3; U-NIR-1 |
| F-NIR-2 | Under `untrusted`, the only negative command form offered was `cancel`, which per the supplier's description also interrupts the turn | DM-1, LB-1, TO-4 cause |
| F-NIR-3 | HOSTING's *settlement* keeps native answer content; for `isSecret` answers that would keep secrets in the register and its persistence | SE-1…SE-3; J-H4 |
| F-NIR-4 | The person's actor reference for `person-via-interaction` was "as supplied by DEL-01-04" with no form | §4.5 and AAC §7 give the form; J-H5 |
| F-NIR-5 | The App's checkpoint display (EXEC §2.4.4) and DEL-04-02's K-5/K-6 overlapped | Resolved by R17-7: §9; J-E2, J-S1 |
| F-NIR-6 | This deliverable needs three inputs no register row names (DEL-04-02, DEL-02-03, DEL-01-05) | NR-1…NR-3 proposed, all SCC-neutral |
| F-NIR-7 | App v3 called an interrupted turn "Stopped" | §10; TO-4 |

## UNRESOLVED

| Item | Owner | Point of need | Effect |
|---|---|---|---|
| U-NIR-1 Effect of DM-4/DM-5 | App implementation owner with DEL-01-01 | Before card implementation | PROPOSED forms; effect not observed |
| U-NIR-2 AO-1 or AO-2 (TBD-003) | App implementation owner | Before attachment implementation | AO-1 assumed |
| U-NIR-3 Re-raised requests after restart (O-2) | OBS-2, then DEL-01-02 | Round 2 | §4.4 note |
| U-NIR-4 Use of `thread/attachment/*` | App implementation owner | If a requirement needs per-thread attachment persistence | Not used |
| U-NIR-5 PD-5 reading of RC-4 | Integrator | Before node F | INTEGRATION reading |
| U-NIR-6 The two requested elements `a15_record`, `revision` on D5's `draft_transition` (J-W1) | DEL-02-02 with DEL-01-04 | Node F / comparison | Until carried, read from WR's `library_entry` |
| U-NIR-7 Interrupt effects (O-1), supplier resolution (O-3), delegation items (O-4) | OBS-2 | Round 2 | TO-4, CS-6, §5.5 cells OBS-2 pending |

## Changes

- v0.1 (this node): first version.
