# Native requests, outcomes and attachments — receiving and interaction design

- Named candidate: **NIR-v0.4**, CC-NIR-ATTACHMENT-REF (2026-10-05);
  owning bound/reference/standing changes prepared for joined independent review.
  Historical contribution and source records below remain preserved.
- Contribution: DEL-01-04/NIR-v0.3 (supersedes NIR-v0.2, last changed at
  `e510aa84fb`, sha256 49e180907d39db3d5e6c7fedfaadf9d964aba57b328d84cca1f58fb1aec38ca0;
  NIR-v0.2 superseded NIR-v0.1, committed at
  `63a6e0fa47`, sha256 96765105cec82d16ed3fb53c87daaf5a0ebeef30ae5600772822a850bae0db3c).
  **v0.3 change (R23-22; run `APP-V4-DESIGN-PASS-4-20261003`, owner O-A):**
  §5.1's `Turn.error` source line holds at both pins (0.158.0 and 0.160.0,
  VERSION_ADVANCE Δ3), and TO-4 keeps an interrupted turn that carries an
  error interrupted. **Re-pin (R23-5):** DEL-01-04 ScopeOfWork.md sha256
  8434cc47ec28e1397e7dae548183543567f0b5fcfdefaebc0b44bc1f709aacf3
  (SCA-V4-003); blocks read: G-0104-01…14; bearing on this change: G-0104-06
  (REQ-002: only observed events; an interrupted turn is never shown as an
  end) and G-0104-03 (OUT-002: turn and outcome presentation).
  Companion: [APP_ACT_CONTROL.md](APP_ACT_CONTROL.md) (DEL-01-04/AAC-v0.3),
  which designs the App act control.
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not
  accepted. Beside it: three PROPOSED schemas with a valid and an invalid
  example each (§14), and a design prototype in [`prototype/`](prototype)
  that ran on 2026-10-02 (§13.2). No product code.
- Run and node: `APP-V4-DESIGN-PASS-3-20261001`, node D3 (Type 2 TASK, Claude
  Opus 5.5, high effort; does not delegate), dispatched by HELP_HUMAN.
- Serves: OUT-004 (the receiving contract), the behaviour of OUT-001 and
  OUT-002 (definition only), the design of OUT-003 (fixture cases, some run on
  the model); REQ-001…REQ-007; VER-001…VER-007 as designed cases.
- Paths are relative to `projects/chirality-app-v4/execution` unless they
  start with `docs/` (`projects/chirality-app-v4/docs/`).
- **v0.2 inputs (D round 2, 2026-10-02; sha256 recomputed, first 16 hex):**
  run `BRIEFS.md` 316ea29325a0d450 ("D round 2"); `R18_RESOLUTIONS.md`
  abf5eee6324647ff; `R19_RESOLUTIONS.md` 16930ecdcead7511;
  `OWNER_DECISIONS.md` ea96c55710af41c9 (DECISION-L); `F/F0_JOINS.md`
  e93608be1c6e3eb0 (§2, §6, §7.3); `DEL-01-01/Design/OBS_2_0.158.0.md`
  61cc34ffb811eb27 and `OBS_3_0.158.0.md` 554ac4451d112824 (read only;
  O-1…O-8, W-1…W-6; O-4 only through an adapter, R18-9); DEL-01-03/NPTD-v0.1
  `NATIVE_PLANS_TOOLS_DELEGATION.md` a3b36a454d497e28 (§5.3 PS-1…PS-6, §5.4,
  §6.2 TR-6, §9 TA-4) and `npt.item-anchor.schema.json` d3bc6b117af902e4;
  Root `agents/registry.json` 767fdfe25f3722b8 (`default_for_new_chat`, as
  data). Round-1 inputs stand as listed below.

## Changes from v0.1

| Item | Ruling / source | Where | Change |
|---|---|---|---|
| C-02 read side | R18-1 | §7; `nir.draft-transition.schema.json` 0.2 | `a15_record`, `revision` are optional elements D5 adds; the view takes them from the transition, else from WR's `library_entry`; "registered" is shown only when the A15 record is known |
| C-06 | R18-1 (D2's row DEL-01-04 → DEL-01-03 adopted) | §2 IF-13; §4.7; §5.6; §8 AP-10 | DEL-01-04 composes `turn/start`, including `collaborationMode` from NPTD's plan-mode element, and sends the default mode explicitly on every turn after plan mode was used (OBS-2 O-8); request cards cite NPTD's item anchors; act display on NPTD anchors placed here |
| C-09 | R18-2 | §5.4 ST-3 | A workflow run reads "run not started — no model selected"; an ordinary conversation "not started — no model selected" |
| C-12 | R18-1; R19-4 L-1 | §5.2 | "Stop Codex" and "Restart Codex", each asking first with live work, per App-owned Codex process |
| C-14 | R18-1 | §6 AT-8 | A draft reaches a trial only as a message or attachment the person sends; DEL-02-04 carries no draft |
| C-15 | R18-1; R17-9; L-2 | §5.4 ST-5, ST-6 | Role preselection from `default_for_new_chat`, clearable, "no role" allowed; the role is fixed for the conversation; "guidance changed since this conversation started" |
| C-24 | R18-1 | §4.8 | App-level indicator of waiting requests, also with no window; several windows on one conversation |
| R18-5 (U-NIR-5) | R18-5 | §9 PD-5 | The person's click opening the act control from an arrival row is the person's act, not a reaction: DERIVED; U-NIR-5 closed |
| R19-2 (b) | R19-2; DECISION-L L-2 | §5.7 | "Start ‹workflow›" offered after an agent's proposal line; nothing starts until the person confirms; ordinary input; run start and end marked in the conversation |
| R19-3, R19-8 | R19-3, R19-8; OBS-3 W-6 | §5.8 | "Continue as ‹role›" opens a new conversation with that role's guidance and an editable handoff summary; "Fork" stays a same-role copy |
| R19-7 | R19-7; OBS-3 | §5.6 TC-3; IF-14 | The run-start text element DEL-02-02 composes is placed first in the turn that starts a run |
| O-2 | OBS-2 O-2; F0 §7.3 | §4.4 | The "asked again after restart" note is removed: requests are not raised again; the card ends CS-7 |
| O-1, O-3, O-4, O-6 cells | OBS-2; R18-9 | §4.4, §5.1, §5.5; AAC §7 | Filled (O-1, O-3 confirm; O-4 confirms through an adapter only); O-6 stays open for a signed-in account (AAC) |
| G-4 | R18-7 | §5.1 TO-9 | Items opened and never completed settle "not completed (turn ended)" |
| G-5 | R18-7 | §5.3 V-e | Codex's graceful-stop history marker is shown as Codex's, not the person's |
| C-10 | R18-1 | §4.5 | The actor reference derives from the same three values as RS's person; no plan type |
| RX (residual sweep; in place, no version step) | R20-9, R20-1, R20-5 | §5.7 RN-4, RN-6, new RN-7; UNRESOLVED U-NIR-8 | "End run" (and "End ‹A› and start ‹B›" with a proposal) offered on the exact line `Workflow finished: ‹origin›:‹name›` naming the run in force; the press is the person's end with cause `completed`; both line forms recorded as ruled; U-NIR-8 ruled. Not prototyped (`prototype/` unchanged) |
| RV21 (repairs from V21; in place, no version step) | R21-2 (V21-A M-2); R21-3 (V21-A M-1, IF-5 side); V21-A MINOR 4–9, 14; V21-B's Stop Codex label | §6 (rewritten), AT-1…AT-10, AO-1, AO-2; §5.1 TO-4 and labels paragraph; §5.2; §5.6 TC-2; §5.7 RN-2; §5.8 CA-3; §2 IF-5, IF-13; §13.1 VC-NIR-13, VC-NIR-23; §13.2; §14; UNRESOLVED U-NIR-10; `nir.attachment-supply-record.schema.json` 0.2 and examples; `prototype/` | **M-2 (R21-2):** an attachment is carried as a text element (text files, the file named), as an `image`/`localImage` input (images), or, for other files, by naming the path for the agent to read with its tools; only the first two are "supplied", the third "named; read only if a tool item shows it"; `mention` and `skill` are not attachment forms (OBS-3 W-3, W-1); `supplierRead` is per form; the `mention` example is replaced; AT-8's draft trial follows. **MINOR 4 (and V21-B):** TO-4 and §5.2 use RECOVERY-v0.2 §3.4's labels, "interrupted by quit" and "interrupted by Stop Codex"; §5.1 cites RECOVERY-v0.2, not its draft. **MINOR 5:** IF-13 quotes NPTD §5.4's value "no model selected". **MINOR 6:** TC-2 places the run-end line. **MINOR 7:** RN-2 and VC-NIR-23 follow R20-1 and R20-11 (1). **MINOR 8:** "End run" is DEL-02-03's, with DEL-01-02 DEF-4 as the definition. **MINOR 9:** CA-3 offers the project's last explicit choice (ST-2), not the source's model. **MINOR 14:** S-4 and O-9 are labelled optional third-party cross-checks. Prototype: 151 checks (A-1…A-8, O-3a, O-8a new or rewritten) |
| RX2 (residual sweep 2; in place, no version step) | R20-11 (1), (2), (4); R20-6 | §5.7 RN-3, RN-4, RN-5, RN-7; §5.8 CA-2; UNRESOLVED U-NIR-9; `prototype/` | During a run a proposal is offered only as "End ‹A› and start ‹B›" (enabled; A ends by the person with cause `ended to start ‹B›`, or `completed` on a finished report); a plain "Start ‹B›" only with no run in force. The proposal line is the message's last non-empty line and the finished line the last non-empty line or the one immediately before the proposal line, each at most once (follows WR-v0.2 §16.5). CA-2: the App asks the source conversation's agent, in a visible turn there, to draft the handoff summary; the person edits it under an App header naming the source; U-NIR-9 ruled. Prototype: `start_offer`, new `finished_offer`, `continue_as` and new `handoff_composer`; checks O-11, O-12 rewritten, new O-13 |
| G (closeout node G; in place, no version step, 2026-10-02) | R22-3; C1-A G-A2 (with RECOVERY-v0.2 U-R5, closed at G) | §4.8 new WI-5; §5.2 "Interrupt a turn" row | The stop control's behaviour with several windows on one conversation, beside WI-4: each window shows the Interrupt control; the first press settles it (one stop request, sent once); another window's press is refused (`stop-already-requested`, or `no-live-turn` after the turn ended) and its control shows the turn's state from the same stop request. Inputs (sha256, first 16 hex): `R22_RESOLUTIONS.md` `2acc830206bd40b3`; `closeout/C1-A.md` `0c2a44af8c09ce32`; RECOVERY-v0.2 as edited at G (§3.3, SR-11). Not prototyped (`prototype/` outside node G's fence; unchanged); prototype rerun |

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
| L-1 | Names no act control or person identity (`grep` returns 0) | The App act control is designed in AAC-v0.2, labelled PROPOSED until SCA-V4-003 carries SC2-01-04-1, which this pass amends to include A15 and DEL-02-02 | R17-6; K-8; K1-4 |
| L-2 | REQ-004/CLM-004/REQ-006: "reviewed registration … belong[s] to App DEL-02-02" | DEL-02-02 performs the registration (writes the revision to the library); the person's A15 is captured by the App act control (K-8). DEL-01-04 performs no registration | K-8; R17-2 |
| L-3 | REQ-001 "explicit decline" without saying which form | The decline is the request's own negative form where it has one; two kinds have none, and a PROPOSED form is used (§4.3) | REQ-001; HOSTING U-20 |
| L-4 | REQ-001 is silent on automatic answers after time | No automatic decline, ever; a supplier's own resolution is shown as such | R17-9 |
| L-5 | REQ-005 predates K1-1…K1-4 | The agent asks; earlier acts on current content count, cited with their time; a joint answer after partial lapse; the person is recorded "identity not verified" | DECISION-K1 |
| L-6 | Names neither the App checkpoint display nor DEL-04-02's components | DEL-04-02 defines the components and their meaning; this file places them in the App and owns their behaviour there (§9) | R17-7 |
| L-7 | Names no conversation start display | A new conversation shows "no model selected" until the person chooses (§5.4) | K-3 |
| L-9 | Names no role element, chaining offer or role change | ST-5 (C-15), §5.7 (R19-2 (b)), §5.8 (R19-3, R19-8) | R18-1; R19; DECISION-L |
| L-8 | REQ-002 uses "interrupted" and "stop" without the three operations | Interrupt a turn, end a run and stop the Codex process are presented as three things, as DEL-01-02 defines them (§5.2) | R17-3 |

**Reading note.** Element names defined here (*card*, *card state*, *supply
record*, *draft view*) are semantic names, not wire fields, components or
storage choices. Supplier method, field and value names are facts of the
generated types at the 0.158.0 definition pin, quoted as supplier names; they
select nothing. Standing labels for supplier facts are R17-13's: `observed`
(OBS-1/OBS-1b, through HOSTING §10.1), `observed-in-generated-types`,
`inference`. At v0.1 cells that OBS-2 would settle were marked **OBS-2
pending**; at v0.2 each is filled or says why it stays open.
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
display (§9) in the App, and it owns the **App act control** (AAC-v0.2).

It does not own: the register, its custody, recovery or persistence (DEL-01-01,
DEL-01-02); the definitions of stopping (DEL-01-02, R17-3); plan, tool and
delegation views (DEL-01-03); account, provider and model selection (DEL-01-05);
the workflow workspace, review and registration (DEL-02-02); policy and act
meanings (DEL-04-01); display component meanings (DEL-04-02); the record
format, writer and reader (DEL-04-03). §11 traces each exclusion.

### 1.1 Process placement (R17-5; CC-P-A selects act capture/writing)

The requirements below hold whatever placement implements them. R17-5's
historical proposed division remains the basis of the placement column.
CC-P-A, under this run's separate owner native-confirmation decision, selects
PL-3's Rust-host offer/native capture and authoritative record-writing path for
Group A: the webview proposes selection, while the native surface shows the
full immutable selected statement/consequences and only its actual confirmation
captures (AAC §4.1a/§6.2). Other allocation questions are not silently selected
by that decision. AAC §5.2b records the separately selected project/library
capture roots and visible refusal/discovery rules. Neither decision closes
external OI-013 or remaining OI-014 work, and native qualification is still ahead.

| # | Requirement (holds for any placement) | PROPOSED placement (R17-5) |
|---|---|---|
| PL-1 | The register, the answer write path and the state a card shows have one authoritative source that survives a window reload (HOSTING H2, H3; V4-EXE-01) | Rust host: register and write path; the interface renders cards from it |
| PL-2 | A card never holds an answer as authoritative; closing or reloading a view loses no request and answers none (REQ-001, REQ-002) | Interface state is disposable; cards are rebuilt from "list outstanding" (HOSTING §6.4) |
| PL-3 | No agent tool, MCP operation, App rule, supplier request or interface script can operate the act control or produce its record (EXEC CAP-4) | **Selected for Group A (CC-P-A):** Rust host offer composition, host-native confirmation and capture, authoritative writer; webview presentation/selection only (AAC §6); no per-act OS presence check |
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
| IF-5 | Native draft and attachment interactions; the App act control for A15 (K-8), composed from one WR descriptor, `a15_descriptor` (RB-4) or `a15_multi_descriptor` (§4.7; L-4; R21-3), and reporting the capture back {record, capture evidence, descriptor, bound content} | DEL-01-04 ↔ DEL-02-02 | The workspace's journey | AAC §4.2 failure rows | DEP-02-02-013, mirror DEP-01-04-010 (held); statement update proposed (SC3-02-02-6 by D5) |
| IF-6 | Act names and record kinds (V-01), outcome map (V-05), label rules (V-07), no professional standing from agent output (V-08), routine tool permission (V-21) | DEL-04-01 → DEL-01-04 | Every label this deliverable shows | A value not carried is shown by its record's own words, never invented | DEP-01-04-011 (admitted) |
| IF-7 | Record format and writer (the act control writes `human_act`, `act_declined`); record-out for act and lapse display | DEL-04-03 → DEL-01-04 | Writes: on capture; reads: on view | RS §14 (late write with "record write failed"; *not yet evaluated* never shown as current) | DEP-01-04-012 (held) |
| IF-8 | Checkpoint overlay (K-5) and standing facets (K-6) component meanings; AS §4, §8, §9 display rules | DEL-04-02 → DEL-01-04 | Run panel and act log (§9) | A meaning not supplied is not shown; the display compares with the record (AS §6) | **None. New row proposed (NR-1)**, held, SCC-002, SCC-neutral |
| IF-9 | Display meanings SD-1…SD-5, CE labels and arrival references | DEL-02-03 → DEL-01-04 | Run panel (§9); the act control's "arrival it answers" (AAC §2) | As IF-8 | **None. New row proposed (NR-2)**, held, SCC-002, SCC-neutral (reverse of X-1) |
| IF-10 | Model selection state for the start display (none chosen / chosen / last explicit choice for the project); the Codex account as reported, for the person's identity (K1-4) | DEL-01-05 → DEL-01-04 | Conversation start (§5.4); each act capture (AAC §7) | No selection state → "No model selected"; no account reported → the account element is absent, never guessed | **None. New row proposed (NR-3)**, admitted, SCC-neutral (DEL-01-05 reaches no SCC-002 member) |
| IF-11 | The App act control (capture evidence, RS entries) | DEL-01-04 → DEL-02-03 (App-side positive capture fixtures), DEL-04-03, DEL-04-01 | AAC | AAC §3, §4 | DEP-02-03-027 (X-1, held); mirror R2-01-04-a proposed in pass 2 |
| IF-13 | Plan-mode element (NPTD §5.4: the `collaborationMode` value, "not offered (‹reason›)" or "no model selected"; the composer words the last per R18-2, ST-3) and item anchors (`npt.item-anchor`, TR-6) | DEL-01-03 → DEL-01-04 | Turn composition (§5.6); request cards and act display (§4.7, AP-10) | Element absent → no Plan control; anchor absent → the card shows its supplier item identity only | **D2's row DEL-01-04 → DEL-01-03 adopted (R18-1 C-06)**: admitted, SCC-free |
| IF-14 | Run-start text element (R19-7: the registered revision's bytes framed by DEL-02-02's lines) and the person's selection handed back on "Start ‹workflow›" | DEL-02-02 → DEL-01-04 (text); DEL-01-04 → DEL-02-02 / DEL-02-03 (the person's confirmed selection, a runtime value) | The turn that starts a run (§5.6, §5.7) | No text → no run starts; the turn is not sent as a run start | DEP-01-04-009 (held; statement update proposed) |
| IF-15 | Role list with `default_for_new_chat` (registry data) and "guidance changed since this conversation started" | DEL-02-04 → DEL-01-04 | Start display (ST-5, ST-6); "Continue as ‹role›" (§5.8) | No list → "no role" only | **New row proposed (NR-4)**: held inside SCC-002, SCC-neutral |
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

**After a restart (OBS-2 O-2, observed at 0.158.0).** A pending request is
not raised again after a restart and resume; its card ends CS-7 "Ended
unanswered" for good.

**After a supplier resolution (OBS-2 O-3, observed).** A request pending in an
interrupted turn was resolved by Codex (`serverRequest/resolved` after
`turn/completed`), and a later client answer was silently ignored. The card
therefore withdraws its answer controls on CS-6, and the register refuses any
answer `already-resolved` (HOSTING R4).

### 4.7 Item anchors on cards (C-06)

Each card for a request with an item (`threadId`, `turnId`, `itemId`) cites
NPTD's item anchor for that item (`npt.item-anchor`, anchor kind *item*;
NPTD §6.2 TR-6). The card shows "about: ‹item, as DEL-01-03 shows it›" and
links to the item row; the item row links back. The row never offers an
answer control (A14 is this file's, HOSTING §11). An anchor DEL-01-03 does not
supply leaves the card with the supplier's item identity only.

### 4.8 The App-level indicator of waiting requests (C-24)

| # | Rule |
|---|---|
| WI-1 | The App shows, outside any conversation window, how many supplier requests wait for the person's answer and in which conversations, whether or not a window shows them (HOSTING R6; DEL-01-02's *list outstanding*) |
| WI-2 | It counts supplier requests only. A checkpoint arrival never counts, never raises it and never changes it (NR-7; SD-4) |
| WI-3 | It opens the conversation on the person's click; it answers nothing and never declines (NR-2, NR-3) |
| WI-4 | Several windows on one conversation show the same cards from the same register; the first answer written settles the request, and an answer from another window is refused `already-settled` and that window's card updates (R-4) |
| WI-5 | **The stop control in several windows (R22-3).** Each window on a conversation shows the turn's "Interrupt" control while the turn is live (§5.2). The first person's press settles it: DEL-01-02 writes one stop request and sends it once (RECOVERY-v0.2 §3.4 SR-01). A press in another window is refused, `stop-already-requested` while that request is pending (SR-11) or `no-live-turn` once the turn has ended (RECOVERY-v0.2 §4.1), and that window's control then shows the turn's state from the same stop request (pending, then its outcome under §5.1, for example TO-4 or one of RECOVERY-v0.2 §3.4's labels), as WI-4 does for cards. Nothing is sent twice (RECOVERY-v0.2 §3.3) |


### 4.5 The answer submission (data) and secret values (SE)

A card hands the register's *answer* operation one
[`nir.answer-submission.schema.json`](nir.answer-submission.schema.json)
object: request identity, generation, method, the native answer unchanged.
With CC-H/CI-2 consumer adoption under CC-A (candidate, 2026-10-04): generation
is the complete H5 object {`appSession`, `home`, `spawnCounter`}, and request
correlation/closed-generation checks compare **all three** values. `home` names
the stable App-owned home, never credentials or a filesystem path. Answer
schema/format is 0.2 (`urn:chirality:app-v4:del-01-04:nir:answer-submission:0.2`);
0.1's integer generation is historical, not an admitted alternative. This
changed ID must be registered by DEL-01-01/02 register operations and the
DEL-01-04 card/submission validator before adoption. No automatic answer retry
or new host placement is introduced. The remaining submission fields are
`submittedAs` (*answer* or *decline*), origin `person-via-interaction` with the
actor reference (AAC §7: "person:‹name›/‹OS account›/‹Codex account›
(identity not verified)"), the names of the forms the card showed, the time,
and `secretValuesPresent`. The actor reference is derived from the same three
values RS records as the person: the Codex account is the reported email, or
"ChatGPT account (no email reported)"; no plan type (R18-1 C-10).

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
`Turn.error` on a failed turn, and possibly on an interrupted one (generated
description at 0.158.0 "Only populated when the Turn's status is failed", at
0.160.0 "Error associated with a failed or interrupted turn"; no interrupted
turn observed at either pin carried one, VERSION_ADVANCE Δ3); the status, not
the error, decides the state (TO-4); `thread/status/changed` with active flags
`waitingOnApproval`, `waitingOnUserInput` (`observed-in-generated-types`), and
DEL-01-02's recovered state (IF-2).

| # | Shown as | When | Never |
|---|---|---|---|
| TO-0 | "Not started" (with §5.4's reason where it applies) | No turn was started | — |
| TO-1 | "In progress" | `inProgress` observed while observation is live | — |
| TO-2 | "In progress: Codex waits for your tool-permission answer" / "…for your answer to a question" | Active flag `waitingOnApproval` / `waitingOnUserInput` | "Waiting for the person" as a state of a workflow run, or any checkpoint hold wording (SD-4). The flag is the supplier's report about its own turn |
| TO-3 | "Completed" | `completed` observed | Any statement about descendants (§5.5) |
| TO-4 | "Interrupted (‹cause›)": "interrupted by you" (the person's interrupt, R17-3 op 1), "interrupted by quit" (K-4), "interrupted by Stop Codex" (C-12; cause *codex-stop*), "interrupted after your `cancel` tool-permission answer", or "cause not observed" | `interrupted` observed; the cause only where DEL-01-02's record or this App's own answer shows it. An interrupted turn that carries `Turn.error` (possible at 0.160.0, Δ3) is still TO-4: Codex's message is shown beside the label as "Codex reported: ‹message›", never as the cause and never as TO-5 (v0.3) | "Stopped" (App v3 used it, §10); a run end; "Failed" for an interrupted turn |
| TO-5 | "Failed: ‹supplier's message›" | `failed` with `Turn.error` | A cause of the App's own |
| TO-6 | "Outcome unknown: observation was lost before Codex reported an end" | Observation lost (supplier exit, connection loss) with no terminal status observed, or DEL-01-02 cannot settle it after recovery | Completed, interrupted or failed by inference |
| TO-7 | "Interrupted by quit; resume?" | After relaunch, for turns K-4 recorded "interrupted by quit"; the resume offer is DEL-01-02's | An automatic resume |

**Labels from DEL-01-02.** Where DEL-01-02 supplies an outcome label for a
turn (RECOVERY-v0.2 §3.4, `outcomeLabel`: for example *interrupted by the
person*, *completed (stop requested)*, *interrupted by quit (final status not
observed)*, *interrupted by Stop Codex*, *interrupted by Stop Codex (final
status not observed)*), the view shows that label and, after a relaunch,
Codex's own reported status beside it. TO-0…TO-7 constrain the wording: never "stopped"
for an interruption, unknown stays unknown, no cause the record does not show.

| TO-9 | "‹item› not completed (turn ended)" | A message or reasoning item opened (`item/started`) and never completed by the time the turn ends; such items are also absent from history (OBS-2 O-1, O-3) | Completed; silently dropped (G-4, R18-7) |

**Filled from OBS-2 (2026-10-01, Codex 0.158.0, LM Studio, one local model):**
O-1 observed `turn/interrupt` → `{}`, then `thread/status/changed` idle and
`turn/completed` with status `interrupted`; two deltas arrived after the
request. TO-4 holds; "interrupted by you" comes from the App's record of the
person's act, since Codex's status does not say who interrupted.

### 5.2 The three stop operations, as presented (R17-3)

DEL-01-02 owns the definitions; this file presents them and keeps them apart.

| Operation (R17-3) | Where the person meets it | What the view shows afterwards |
|---|---|---|
| Interrupt a turn | The turn's "Interrupt" control (DEL-01-02's operation, `turn/interrupt`), in every window on the conversation; the first press settles it (§4.8 WI-5) | TO-4 "interrupted by you"; the conversation and any workflow run continue; never "run ended" |
| End a run | The run panel's "End run" control (DEL-02-03's run end, EXEC; DEL-01-02 DEF-4 defines the person's end and neither performs nor records it) | The run-ended event from the record (§9); turns keep their own outcomes |
| Stop the Codex process | Quit, or the App's **"Stop Codex"**. With live work the App asks first (K-4; DEF-5a): the question lists the live turns, the waiting requests and active delegated agents as DEL-01-02 supplies them, and has no timeout | Live turns "interrupted by quit" / "interrupted by Stop Codex" (RECOVERY-v0.2 §3.4; K-4); waiting cards CS-7 (no App decline at stop, DEL-01-02 U-10) |
| Restart the Codex process | **"Restart Codex"** (C-12). With live work the App asks first, as for Stop; then DEL-01-02 stops and starts the process | As Stop, then the conversations re-attach (§5.3) |

Under DECISION-L L-1 the App runs one Codex process per App-owned home
(ChatGPT account; API key). "Stop Codex" and "Restart Codex" are offered for
each, named by the conversations it serves; quitting the App stops all of
them (R19-4).

Observer loss (window close, reload) and connection loss are not stops and
show nothing of the kind.

### 5.3 Reload, reopen and relaunch (SQ-V)

| Step | Action | Failure: what fails · who reports · record · next |
|---|---|---|
| V-a | The view asks DEL-01-02 for the recovered state of the conversation (IF-2) | Not available · DEL-01-02 · — · the view says "recovering" and shows nothing as current |
| V-b | Turns are drawn with their recovered status and cause; each recovered item is marked "recovered at ‹t›" where DEL-01-02 marks it | A status DEL-01-02 cannot settle · TO-6 |
| V-c | Cards are rebuilt from the register's outstanding list and its settled entries for the conversation | Entries of a closed generation · CS-7 |
| V-d | App-kept items Codex does not keep in history (for example plan checklist revisions, R17-4) are shown by their owners as "not recoverable after relaunch"; this file shows nothing in their place | — |
| V-e | After a graceful stop, Codex's history holds a line it wrote itself ("The user interrupted the previous turn on purpose", OBS-2 O-2). The view shows it as "written by Codex when the App stopped it", never as the person's words (G-5) | — |

### 5.4 Conversation start display (K-3)

| # | Rule |
|---|---|
| ST-1 | A new App conversation shows **"No model selected"** until the person chooses one; no model is applied from Codex's own configured default or from any earlier conversation (K-3, owner's answer) |
| ST-2 | Where DEL-01-05 reports a last explicit choice for this project, the start display offers it as a button reading "Use ‹model› via ‹provider› (your last choice for this project, ‹date›)". It is applied only when the person presses it |
| ST-3 | Sending with no model chosen sends nothing to Codex; the message stays in the composer. **An ordinary conversation** reads "not started — no model selected"; **a workflow run** that cannot start reads "run not started — no model selected" (R15-1's wording) (R18-2, C-09) |
| ST-4 | The chosen model, provider and access mode are shown in the conversation header as DEL-01-05 reports them; the observed destination per turn is DEL-01-01's (HOSTING §8.3) and DEL-04-03's to record |
| ST-5 | **Role (C-15).** The start display offers the roles DEL-02-04 lists, plus **"no role"** (R17-9: untyped conversations are allowed). The role whose registry entry has `default_for_new_chat` true (HELP_HUMAN in Root's `agents/registry.json` today) is shown **preselected**, labelled as a preselection, and the person can change it or clear it to "no role" before the first send |
| ST-6 | The role is **fixed for the conversation's life** (DECISION-L L-2). The header shows it; where DEL-02-04 reports that the role's guidance was edited after this conversation started, the header says "guidance changed since this conversation started" (R19-3), and offers "Continue as ‹role›" (§5.8) |

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
DEL-01-02's recovered state and the native delivery (IF-2, IF-3).

**Filled from OBS-2 O-4 — observed through an adapter (OBS-2), not stock
behaviour (R18-9).** `collabAgentToolCall` items (`spawnAgent`, `sendInput`,
`wait`) carried `receiverThreadIds` and `agentsStates`; a child thread is
readable by `thread/read` and has no `thread/started`. With stock LM Studio
0.4.16 the delegation tools never reach the model (they travel inside a
`namespace` tool), so a local-model conversation shows no delegation line at
all. "Primary completed, child still running" was not observed (NPTD NV-04).

### 5.6 Turn composition (C-06; R19-7)

DEL-01-04 composes and sends every `turn/start` (through DEL-01-02's send
path). Prototype O-8, O-9: the composed parameters were valid against the
committed 0.158.0 `TurnStartParams`.

| # | Rule |
|---|---|
| TC-1 | No model chosen → nothing is sent (ST-3) |
| TC-2 | The `input` list holds, in order: the run-start text element when the turn starts a run (TC-3), or, when a run has ended and no run starts with this turn, DEL-02-02's run-end line as its own text element (R20-3; WR-v0.2 §16.2 TX-5; once); then the person's text; then the attachments (§6: text elements, image inputs, and the text element naming paths). A trial text (AT-8; WR TT-3) takes the run-start text's place in a clean trial's first turn (trial text, the person's text, then attachments) and follows the person's text in a delegated trial's message (the person's text, the trial text, then attachments); it is never a run-start text |
| TC-3 | **Run start (R19-7).** The run-start text is DEL-02-02's composition (the registered revision's exact bytes between App-written lines naming the workflow and revision and, when chaining, saying the previous run ended). This file places it as its own text element and changes nothing in it; DEL-02-02 records the bytes and DEL-02-03 starts the run |
| TC-4 | **Plan mode (NPTD §5.4).** When the person chooses Plan (labelled "experimental", C-05), the turn carries NPTD's plan-mode element as `collaborationMode`; when NPTD says "not offered (‹reason›)", the Plan control is absent |
| TC-5 | **Leaving plan mode.** Once a conversation has used plan mode, every later turn carries `collaborationMode` with mode `default` (model the conversation's, `developer_instructions` null) explicitly, because plan mode persists until the default mode is sent (OBS-2 O-8) |
| TC-6 | Role and workflow guidance never go into `collaborationMode.settings.developer_instructions` (NPTD §5.3 F-3; R19-7: `thread/settings/update` is not used for workflows) |

### 5.7 Runs in a conversation and the "Start ‹workflow›" offer (R19-2)

| # | Rule |
|---|---|
| RN-1 | The conversation view marks each run's start ("‹workflow› ‹revision› started", the supplied bytes folded and openable) and end ("run ended: ‹how›") from the run records DEL-02-03 writes; one run at a time (R19-2) |
| RN-2 | **Sequential (a).** After a run ends (only by the person, DEL-01-02 DEF-4, with cause *ended by the person*, *ended to start ‹B›* or *completed*, or by the run owner; R20-1), the workflow selector (DEL-02-02's selection) offers a plain start again in the same conversation; starting B is TC-3. While a run is in force, selecting B is offered only as "End ‹A› and start ‹B›" (RN-4; R20-11 (1)) |
| RN-3 | **Agent-proposed (b).** When the last non-empty line of a completed `agentMessage` is `Next workflow: ‹origin›:‹name›`, the message carries that line form only once (R20-11 (2); WR-v0.2 §16.5 PR-1), and it resolves to exactly one registered workflow, the App shows a button **"Start ‹workflow› (proposed by the agent)"** beneath it when no run is in force (RN-4 otherwise). Nothing starts until the person presses it; the press is ordinary input (R17-9), handed to DEL-02-02 as the person's selection and to DEL-02-03 to start the run |
| RN-4 | **During a run (R20-11 (1)).** While a run is in force, the proposal is offered only as **"End ‹A› and start ‹B›"**, one step and the person's choice: pressing it ends A by the person (DEL-01-02 DEF-4) with cause `ended to start ‹B›` (R20-11 (4), EXEC's wording), or `completed` when the same message carries a finished report (RN-7; R20-1), then starts B by TC-3. A plain "Start ‹workflow›" appears only when no run is in force (one run at a time) |
| RN-5 | A proposal naming no registered workflow, or several, a proposal line that is not the last non-empty line, or a message with more than one proposal line shows no button; prose suggestions are not read (the App never classifies message text as a request: EXEC RC-5). The offer records nothing and is never a selection by the agent |
| RN-6 | The two line forms are ruled (R20-5, R20-9): `Next workflow: ‹origin›:‹name›` and `Workflow finished: ‹origin›:‹name›`, each alone on its own line; the App reads only these exact forms. The shipped product guidance that tells the agent both is DEL-02-04's (ROLE-v0.2 §4.2 GS-7); the run-start text that repeats them for the run in force, and the run-end line the model reads, are DEL-02-02's (WR-v0.2 §16.2, TX-5) (U-NIR-8) |
| RN-7 | **Finished report (R20-1, R20-9; RX).** When a completed `agentMessage` carries the line `Workflow finished: ‹origin›:‹name›`, alone on its line, once in the message, as its last non-empty line or the line immediately before its proposal line (R20-11 (2)), and naming the workflow of the run in force, the App shows an **"End run"** button beneath it; when the same message also carries a proposal that RN-3 accepts, it shows **"End ‹A› and start ‹B›"** beside it. Pressing either is the person's end of the run (DEL-01-02 DEF-4), with cause `completed`, handed to DEL-02-03 (and, for the second, the person's selection of B to DEL-02-02, then B's start by TC-3). The line itself ends nothing: the run stays in force until the person presses, and the App never ends, opens or focuses anything because of it (R18-5's rule for arrivals applies alike). A finished line naming another workflow, or arriving with no run in force, shows nothing. The button records nothing until pressed |

### 5.8 "Continue as ‹role›" and "Fork" (R19-3, R19-8)

| # | Rule |
|---|---|
| CA-1 | "Continue as ‹role›" opens a **new conversation** with that role (fixed for its life, L-2) and the role's guidance composed by DEL-02-04 at start. It does not fork: at 0.158.0 `thread/fork` ignores new instructions, so a fork keeps the source's role (OBS-3 W-6; R19-8) |
| CA-2 | **Handoff summary (R20-6).** When the person chooses "Continue as ‹role›", the App asks the **source conversation's agent**, in a visible turn of that conversation, to draft a handoff summary (the request names what it should cover: the person's last request, the last workflow run and how it ended, and the attachments supplied there by name and content identity). The draft is placed in the new conversation's composer under one App-written header naming the source conversation and its role; the header names and does not instruct, and the summary carries no instructions beyond the person's own text. The person edits it before sending; nothing is sent to the new conversation until the person sends it. If the source turn fails or is interrupted, the composer holds the header only and the person writes the summary (PROPOSED) |
| CA-3 | The new conversation starts with no model chosen (ST-1); the project's last explicit choice is offered exactly as ST-2 defines it, as for any new conversation (K-3). The source conversation's model is not offered as such |
| CA-4 | "Fork" stays available as a same-role copy of a conversation (`thread/fork`), labelled "same role" |


---

## 6. Attachments and the identity of supplied content (OUT-002; REQ-003; AC-003; VER-003)

**CC-NIR-ATTACHMENT-REF candidate (2026-10-05).** App implementation-owner
bound disposition with DEL-01-05 model-context source concurrence:262144 original
file bytes inclusive, UTF-8/no NUL, existing image/named-path fallback. This is
an App carrier threshold, not a supplier/model context limit. Reference and
HOSTING custody joining below are named prepared changes awaiting joined
independent review/adoption; no product dispatch or native witness is claimed.

**Supplier facts.** At 0.158.0 a turn's input is a list of `UserInput`:
`text`; `image` by `url` or by supplier `fileId`; `localImage` by `path`;
`audio` by `url`; `localAudio` by `path`; `skill` {name, path}; `mention`
{name, path} (`observed-in-generated-types`). **Observed (OBS-3, Codex
0.158.0, one local model, 2026-10-02):** `mention` with a file, with a
`SKILL.md` copy and with a discovered skill's canonical path was accepted and
**nothing reached the model**, neither the bytes nor the path, only the
text message (W-3); `skill` was honoured only for a `SKILL.md` at the
canonical path of a skill Codex had discovered, and otherwise accepted and
silently ignored (W-1); a plain text element reached the model byte for byte
and `thread/read` returned it (W-4). Separately, `thread/attachment/add|list|remove`
(stable) persists {`attachmentType`, `identityKey`, `payload`} per thread with
outcome `created` · `existing`; its semantics are not observed.

**Carriers (R21-2; INTEGRATION).** The App carries an attachment in one of
three ways, and records which:

| Form (`suppliedAs`) | For | What the turn carries | Standing (`supplyStanding`) | `supplierRead` |
|---|---|---|---|---|
| `text-element` | A text file (AT-9) | A text element: one App-written line naming the file, then the file's bytes | **supplied** | "not applicable: the bytes are in the turn's own text element" (W-4 observed the text route) |
| `localImage`; `image-url`, `image-fileId` | An image | A `localImage` {path} or `image` {url · fileId} input | **supplied** | `localImage`: "not observed: Codex reads the path itself" (`observed-in-generated-types`; the image route was not observed in OBS-1…3); by reference: "not applicable: content passed by reference" |
| `path-named` | Any other file (including audio, binary and text above the bound) (AT-10) | A text element naming the path for the agent to read with its tools | **named; read only if a tool item shows it** | "not observed: read only if a tool item shows it" |

`mention` and `skill` are **not** attachment forms (W-3, W-1). `audio` and
`localAudio` are not used: an audio file is named (AT-10).

**Consequence (inference).** For `localImage` and a named path the bytes Codex
or the agent reads are not observable from the App; for a text element they
are the bytes the App sent. Nothing at the pin reports provider adoption. The
App states what it read, what it sent and when, and for a named path any
tool item that shows a read.

| # | Rule |
|---|---|
| AT-1 | When the person selects a file, the App takes its content identity (method designation carried; no algorithm chosen: RS U-04, HOSTING U-08) and shows it with the name and the carrier it will use (AT-9, AT-10) |
| AT-2 | When the host writes the turn input, it takes the identity again. If it differs from the selection's, the file is **not sent**: the card says "content changed since you selected it; confirm the current content", and the person confirms the current content or removes it. A file missing at that moment is held the same way |
| AT-3 | One [`nir.attachment-supply-record.schema.json`](nir.attachment-supply-record.schema.json) record (0.2) per attachment: the identities at selection and submission, the form (`suppliedAs`), its standing (`supplyStanding`), the path or reference, the identity of the composed text element (`elementIdentity`, for a text element or a named path), the immutable submission or already-observed turn reference (§6.1), `supplierRead` **per form** (table above), "provider adoption: not observed", and for a named path the tool items that show a read (`toolReads`) |
| AT-4 | Same-named items with different content are different attachments, shown with distinguishing identity prefixes; nothing is merged or substituted by name |
| AT-5 | A URL or supplier `fileId` is recorded as given, with identity "not obtainable (the App does not fetch it)" |
| AT-6 | A later check (the person opens the item, or the view re-checks on display) records "unchanged since supplied" or "changed after it was supplied; what Codex read is not observed"; it never rewrites the supply record's earlier identities |
| AT-7 | `thread/attachment/*` is not used by this design: its semantics are not observed and no requirement needs it (UNRESOLVED U-NIR-4) |
| AT-8 | **Draft trials (WR TT-2…TT-13, revised by the owner's direction of 2026-10-10 on WR U-WR-24).** A draft reaches a trial (K-7) through its **trial text**, DEL-02-02's composition (WR TT-3), which this file places as its own text element and changes nothing in: in a **delegated trial**, after the person's text in the authoring conversation's composer; in a **clean trial**, first in a new conversation's composer, where a run text would be (TC-2). The App pre-fills, never sends (C-14 still holds for this): the person's text stays editable and the trial text is shown as a card "trial ‹n› of draft ‹name› at content ‹id› — not registered; not a workflow run", openable and removable, not edited in place. A clean trial's conversation is a **new** conversation opened in draft as for "Continue as" (§5.8 CA-1, CA-3: role chosen by the person, no model until chosen), without a handoff turn. The trial text is neither an attachment nor a run text and opens no run; it carries its draft reference and trial reference, and DEL-02-02 writes the trial link only on the host's acknowledgment of the send. Other files of the draft are named by the trial text's files line, as a registered run's are (WR §16.2 line 4; TT-8), not attached; AT-10 is not used for drafts. Proposal and finished lines written in a clean trial conversation or a trial's sub-agent show no button (RN-3…RN-7 do not apply), and a clean trial conversation (and a fork of it) offers no workflow start. In an authoring conversation with a run in force, the turn that carries a trial message is labelled as the trial's, its proposal and finished lines show no button, and after a trial of a draft of the run's own workflow RN-7 offers no End run for that run (WR TT-2). The bring-back transcript (WR TT-10) is placed the same way, after an editable prompt. A draft's files that the person attaches as ordinary files are ordinary attachments (AT-1…AT-7, AT-9, AT-10) with no draft standing. No guidance carries a draft, and `skill` is never used for it |
| AT-9 | **Text element (PROPOSED wording).** A file that decodes as UTF-8, has no NUL byte and is within the App implementation-disposed bound (262144 original file bytes inclusive, before adding the naming line; CC-NIR-ATTACHMENT-REF; U-NIR-10 model-context concurrence) goes as its own text element: `[Chirality] Attached file "‹name›" (‹path›; content ‹12 hex›). Its bytes follow this line.`, a line feed, then the bytes exactly. The line names; it instructs nothing |
| AT-10 | **Named path (PROPOSED wording).** Any other file is named in one App-written text element after the person's text: `[Chirality] File named, not supplied: "‹name›" at ‹path› (content ‹12 hex› when attached). Read it with your tools if you need it.` A later tool item of the conversation that names the path (a command or file read) is recorded in `toolReads` (App-observed); the record stays "named": which bytes were read then is not observed |

**Two ways to narrow the gap between the App's read and Codex's read for
`localImage` and named paths (options; not chosen: TBD-003 keeps attachment
storage open, REQ-003 forbids choosing it here).** A text element has no such
gap: its bytes are in the turn.

| Option | What is supplied | For | Against |
|---|---|---|---|
| AO-1 (this design's default) | For `localImage` and a named path: the original path; identity at selection and submission | No copy; no storage choice | A change between the App's read and Codex's or the agent's read is not detected |
| AO-2 | A copy in an App-held, content-addressed store, whose path is supplied or named | The bytes read are the bytes the App identified, unless the copy itself is altered | A storage location and lifecycle must be chosen (TBD-003); the agent sees a different path |

**Sequence (SQ-A).** Select (AT-1) → choose the carrier (AT-9, AT-10) →
compose → write the turn input (AT-2, AT-3) → turn runs (Codex receives the
text element or image input; the agent may read a named path with its tools)
→ later checks (AT-6; tool reads, AT-10). Failures: identity not obtainable at
selection (unreadable file) · the App · nothing sent · the person picks
again; identity differs at submission · the App · held, not sent · the person
confirms or removes; the supply record cannot be written · the App · the item
is still held until the record is written, so the App never sends what it has
not recorded.

---

### 6.1 Submission identity and native correlation (named candidate)

For a new dispatch, the host mints one unique `submission:<opaque UUID>` for
the complete immutable ordered input/attachment list before recording. Each
attachment's existing supply record keeps its own unique opaque attachmentId;
its `turnRef` carries that App-owned submission token, never a guessed native
turn ID. Historical records that name an observed turn keep that actual meaning.
New owning supply references use `attachment:<attachmentId>`; the resolver
removes only that prefix and looks up the exact opaque ID in the owning NIR
supply source. References are not paths, native IDs or authority grants.

Persist all admitted per-attachment records, then the existing HOSTING client
request with its pointer-only `submissionAssociation`:
`{submissionRef,threadId,supplyRefs:[ordered unique attachment references],
expectedTurnId?}`. `expectedTurnId` belongs only to turn/steer and names its
actually observed target. The HOSTING outer generation, allocated RPC identity
and method remain the source authority; no duplicate outer fields or native
payload/transcript copy is stored by NIR. Each resolved record must carry the
same immutable submission token, and the ordered supplied list must equal
`supplyRefs` exactly, with no missing, extra, repeated or reordered item.

The prepared client-request state is `prepared-not-sent`, with `not-attempted`
and an allocated non-null RPC ID/full ready generation. This differs from a
written request's pending/unknown outcome. Failure to durably preserve any
supply member/list association/client custody prevents dispatch. A prepared
supply record proves exact prepared input and carrier, not sent, accepted or
provider adopted. Until the native write is actually observed the view states
*prepared; not sent*. Carrier standing (`supplied` versus `named`) is not a
standalone assertion of pipe write or successful receipt.

HOSTING's new client-custody proposal is
`urn:chirality:del-01-01:hosting-boundary:v0.10:client-request-record`.
NIR consumes that named successor only after joined independent review;
structural string acceptance by its own unchanged-shape0.2 supply schema is not
adoption. HOSTING/RECOVERY preserve source outcome and response/receipt links;
NIR resolves them without adding a correlation store, REC ledger kind, RS kind,
transcript or automatic resend. For turn/start, only the exact full-generation/
RPC matched native result establishes its turn identity. For turn/steer, that
result must also match the explicit expectedTurnId. Nearby events, latest turn,
thread-only equality and equal spawn counters never establish this join.
Only the owning written/pending request can admit its matched response. If a
result reports a thread, it must equal the bound request thread; omission uses
the bound context, never a latest-thread guess. A malformed/null result retains
its original source and native-turn unknown without throwing. Once the owning
RPC reply settles, a conflicting or repeated reply cannot overwrite that first
source/correlation; surface the repeat as uncorrelated with its cause. Error,
unsent, refused or failed-write source states establish no native turn.
Original turnRef/selection/submission identities are never rewritten to a
native turn ID. Multiple submissions to one native turn remain distinct.

If write/result/correlation is absent or uncertain, display its actual unknown
or unavailable limit. In particular, after crash/reload a surviving prepared
record does **not** prove no pipe write occurred; derive unknown/unavailable
unless existing source custody establishes a definite cancellation/no attempt.
Reopening, ending a wait, interruption or a late response never resends. A new
explicit person send receives a fresh submission token. Pre-dispatch picker
cancellation/removal sends nothing; post-dispatch interrupt follows RECOVERY
DEF-3 and makes no rollback or provider-adoption claim.

Native-path identity is held losslessly by the selecting/reading host (tagged
native bytes on a byte-path platform), distinct from escaped display text.
Compute file identity and decode content from one read buffer. A supplier path
carrier receives only an exactly representable native path string; a non-UTF-8
native path cannot silently become a replacement-character/escaped display
path. If the selected supplier carrier cannot represent it, report that carrier
unavailable with cause rather than dispatching a different path. This does not
select a copy/cache or claim all filesystem paths are supplier-representable.
Text file bytes preserve BOM, CRLF, trailing whitespace and newline state;
wrapper overhead does not change carrier eligibility. Image/provider read and
adoption observations remain open.

---

## 7. Draft receiving contract (OUT-004; REQ-004; AC-004; VER-004)

**What DEL-01-04 receives** from the workflow workspace (DEL-02-02; IF-4):
DEL-02-02's `draft_transition` and `draft_reference` (WR-v0.1 §5.1, §8;
`workspace-registration.schema.json`, node D5). DEL-02-02 owns them.
[`nir.draft-transition.schema.json`](nir.draft-transition.schema.json)
restates `draft_transition` **with D5's own element names and values**, so
the two compare line by line, plus the two optional elements R18-1 (C-02)
has D5 add on *registered* and *registration not completed*:

| Element (D5's name) | Meaning for the view |
|---|---|
| `draft` {`draft_location`, `draft_root`, `name`} | Where the draft is; a draft has no workflow identity (EXEC TR-1, HR-3) |
| `event` | *written* · *changed* · *review shown* · *review stale* · *registration refused* · *registered* · *registration not completed* · *re-confirmed* (CC-WR-RECONFIRM) · *removed* |
| `from`, `to` | WR §5.1 draft states: *absent* · *draft* · *not valid* · *under review* · *changed since review* · *registered, unchanged since* · *removed* |
| `content` | The draft's content identity with method (WD §6.1 RV-1…RV-5; algorithm open, WD U-03) |
| `disposition` | WR's codes: *new workflow*, *new revision*, *in place*, or *refused: …* (K-6: *refused: name taken* asks for a new name); *re-confirmation* (DS-8, WR §4.8) |
| `cause`, `time`, `attribution` | As WR §8 states them (*file change item* with thread and item, *app action*, *not observed*) |
| **`a15_record`** (optional, C-02) | For *registered*, *registration not completed* and *re-confirmed*: the RS A15 record the App act control wrote at capture (K-8) |
| **`revision`** (optional, C-02) | For *registered* and *re-confirmed*: the revision identity (for *re-confirmed*, the re-confirmed revision's own; no new revision) |

**Read side (C-02).** The view takes `a15_record` and `revision` from the
transition when present, otherwise from WR's `library_entry` for the same
draft. It shows *registered* only when the A15 record is known from one of the
two (prototype D-7).

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
| *registered, unchanged since*, reached by *re-confirmed* | "re-confirmed as ‹revision› for use in this App session by ‹person› (identity not verified) at ‹t›; registered earlier (not verified in this session)", citing the new A15 record |
| *removed* | "removed" |
| While the act control has captured an A15 and the workspace has not yet reported | "registration in progress" (from the act control's own state, AAC §3) |
| After *registration not completed* | "draft — registration not completed: ‹cause›; the act is recorded and had no effect" |

**Accepted transitions** are WR §5.1's (prototype `DRAFT_ALLOWED`); the view
checks that `from` equals the state it shows and re-reads WR's
`draft_reference` when it does not. CC-WR-RECONFIRM adds: *registered, unchanged since* → *under review* (*review shown*, DS-8); *registered, unchanged since* → *registered, unchanged since* (*registration refused*, DS-3 or DS-4); *under review* → *registered, unchanged since* (*re-confirmed*; *registration not completed* or *review stale* of a DS-8 review begun there); *under review* → *draft* (*registration not completed* of a DS-8 review begun at *draft*). **Refused by the view** (never shown as
transitions): *registered* when neither the transition nor `library_entry`
gives the A15 record and the revision;
*registered* for content other than the reviewed content; *re-confirmed* when neither the transition nor `library_entry` gives the A15 record and the revision; *re-confirmed* for content other than the reviewed content; *registration not
completed* without the recorded act; any local UI action that would make a
draft reviewed or registered (REQ-004: no local transition invents review or
registration). K-7: a draft is never shown as running a workflow; trying it
is a trial, never a run (AT-8; WR TT-2, TT-3).

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
| AP-10 | Where an act record's subject is one of DEL-01-03's anchors (a plan revision, an item), the act is shown on that anchor as NPTD TA-4 states it ("‹act kind› by ‹person› (identity not verified) · recorded by ‹recorder›"); this file places the display (R17-7, C-06) | NPTD §9 TA-4 |

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
| PD-5 | SD-3's "App act control" entry on an arrival row opens the control only when the person clicks it; the offer may carry the arrival's declared act kind, subject, scope and purpose, because the person chose to act on that arrival. **DERIVED (R18-5; K1-1, EXEC RC-4):** the person opened it; the product did not react to the arrival. The App never opens, focuses or notifies because of an arrival |
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

| Case | Setup | Action | Expected | Needs | Prototype (2026-10-01; rerun 2026-10-02) | Serves |
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
| VC-NIR-10 Outcomes | Status set; observation lost; causes (incl. Stop Codex); running descendant | Label | TO-1…TO-6; RECOVERY's labels; never "stopped"; descendants not implied | model; OBS-2 (O-1, O-4); candidate | O-1…O-3, O-3a pass (model) | VER-002 |
| VC-NIR-11 Reload and relaunch | Live turn with a waiting card | Reload; relaunch after quit | Recovered state drawn; cards rebuilt; "interrupted by quit" with resume offer | candidate; DEL-01-02 interface (O-2 settled: no re-raise) | Not run | VER-002 |
| VC-NIR-12 Start display | No selection; last choice exists | Open; send | "No model selected"; offer not applied; message kept | model; candidate | O-4 pass (model) | VER-002 (K-3) |
| VC-NIR-13 Attachment identity and carriers (R21-2) | Same file; changed file; same name different content; missing file; a text file, an image, another file; a tool read of a named path; `mention` and `skill`; a draft's `WORKFLOW.md` | Select and submit | Sent; held; two items; held. Text element and image "supplied"; other files "named; read only if a tool item shows it", the tool read recorded beside it; `mention`/`skill` refused as forms; the draft shown as a draft. Records valid | model; candidate | A-1…A-8 pass (model; rewritten at RV21) | VER-003 |
| VC-NIR-14 Draft transitions | WR §5.1 walk: written, review shown, review stale, review shown, registered; name taken; registration not completed | Receive | WR states shown; stale review; refusals of invented registration | model; DEL-02-02's interface (D5) | D-1…D-6 pass (model) | VER-004 |
| VC-NIR-15 Act presentation | Record-out with direct capture, faithful record, earlier act, joint answer, lapse, decline, A14, agent claim | Display | AP-1…AP-9 | fixture (RS examples), candidate | Not run (display) | VER-005 |
| VC-NIR-16 Positive act case | A person, an App file, the act control | Act; then change the file | Direct-capture record, actor ≠ recorder; then lapse | **person** (DEP-01-04-019), candidate | Model only: AAC K-4, K-6 | VER-005 |
| VC-NIR-17 Receiving review | This file | Trace REQ-006 exclusions; open pairs | §11, §12 complete | review | — | VER-006 |
| VC-NIR-18 Fixture suite | All of the above on a candidate | Run | Simulated vs observed reported | candidate | — | VER-007 |
| VC-NIR-20 Turn composition | Plan chosen; later turns; run start; run-end line with attachments | Compose | Plan element; explicit default after plan; run-start text or run-end line first, then the person's text, then the attachments; valid against `TurnStartParams` | model; bundle | O-8, O-8a, O-9 pass | VER-002 (C-06) |
| VC-NIR-21 Start display wording and role | Run vs conversation; registry default | Open; clear role | R18-2 wording; preselected, clearable, "no role" | model; candidate | O-5, O-6 pass | VER-002 |
| VC-NIR-22 Waiting indicator | Requests in two conversations; two windows | Count; answer twice | Count with no window; second answer refused | model; candidate | O-10 pass | VER-001 (C-24) |
| VC-NIR-23 Start offer | Proposal lines exact, absent, unknown; run in progress | Offer; confirm | Offer only for one registered workflow; with no run in force "Start ‹B›"; during a run only "End ‹A› and start ‹B›" (enabled; R20-11 (1)); the person confirms | model; candidate | O-11 pass | VER-004 (R19-2) |
| VC-NIR-24 Continue as role | A conversation | Continue as another role | New conversation, editable summary, nothing sent, no model | model; candidate | O-12 pass | VER-002 (R19-3) |
| VC-NIR-25 Items never completed | Open reasoning item at turn end | Settle | "not completed (turn ended)" | model; fixture (OBS-2 O-1) | O-7 pass | VER-002 (G-4) |
| VC-NIR-19 Formats | Three schemas and examples | Validate | Valid valid; invalid invalid | model | S-1…S-4 pass | OUT-003 |

### 13.2 Local prototype (R17-1; R12-3)

`prototype/` (Python 3 standard library; read-only imports of DEL-04-03's
`minischema.py` and `record_store.py` and DEL-01-01's `jsonschema_subset.py`;
at RV21 it also reads DEL-02-02's WR schema and examples and DEL-02-01's WD
schema for K-17. Checks S-4 and O-9 are **optional third-party
cross-checks**: they use the already-installed `jsonschema` when it can be
imported and are skipped otherwise; every other check needs only the
standard library).
Command: `python3 run_cases.py` in `prototype/`. Round 2 run on 2026-10-02,
macOS Darwin 25.6.0 arm64, Python 3.13.7: **119 checks, 0 failed**, exit
status 0; output in [`prototype/results/RUN_2026-10-02.txt`](prototype/results/RUN_2026-10-02.txt)
(round 1: 103 checks, `RUN_2026-10-01.txt`, kept). New at v0.2: O-5…O-12,
D-7, K-12b, K-12c; O-9 checks composed turns against the committed bundle
with the installed `jsonschema`. Node F was changing RS's schema while this
ran: the act control's A15 entries are written in whichever form the RS
schema in the working tree has (RS-v0.8's `derivedFrom` string, or FR-06's
`reviewedDraft`/`priorRevision`/`registeredEntries`); the recorded run used
the FR-06 form (RS schema sha256 prefix `ab824dc5974ad128`), and an earlier
round-2 run against RS-v0.8 also passed 119 of 119.
The installed `jsonschema` 4.26.0 (already present; nothing installed) gave
the same verdicts on all schema examples (S-4). **Rerun at RX2** (2026-10-02, same command and host): **120 checks, 0
failed**, exit status 0; O-11 and O-12 rewritten and O-13 added for
R20-11 and R20-6 (RN-3, RN-4, RN-7, CA-2); output in
[`prototype/results/RUN_2026-10-02_RX2.txt`](prototype/results/RUN_2026-10-02_RX2.txt).
**Rerun at RV21** (2026-10-02, same command and host): **151 checks, 0
failed**, exit status 0; A-1…A-8 rewritten for R21-2, O-3a (Stop Codex label),
O-8a (run-end line and attachment order), and AAC's K-12b…K-12d, K-17, K-17b
for R21-3; output in
[`prototype/results/RUN_2026-10-02_RV21.txt`](prototype/results/RUN_2026-10-02_RV21.txt).
A pass is evidence that the
rules run as written, not a VER pass.

## 14. Data formats (PROPOSED; JSON Schema 2020-12)

| Schema | Handed from → to | Examples |
|---|---|---|
| [`nir.answer-submission.schema.json`](nir.answer-submission.schema.json) | DEL-01-04 card → register *answer* (DEL-01-01 / DEL-01-02) | `.example.valid.json` (1), `.example.invalid.json` (6 cases) |
| [`nir.attachment-supply-record.schema.json`](nir.attachment-supply-record.schema.json) (0.2, RV21: R21-2) | DEL-01-04 → conversation view, DEL-02-02 (a draft tried in a conversation), DEL-04-03 (cited as evidence) | 4 valid (text element, named path with a tool read, local image, draft), 11 invalid (among them `mention`, `skill`, a named path recorded as supplied, v0.1's fixed `supplierRead` on a named path, v0.1's `draft-package`) |
| [`nir.draft-transition.schema.json`](nir.draft-transition.schema.json) (0.2) | DEL-02-02 → DEL-01-04 (D5's `draft_transition` with D5's names, plus the two optional elements of C-02) | 1 valid, 5 invalid |

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
| F-NIR-8 (v0.2) | Nobody sent `collaborationMode`; plan mode persists until the default mode is sent (OBS-2 O-8) | §5.6 TC-4, TC-5 (C-06) |
| F-NIR-9 (v0.2) | Codex writes its own "user interrupted … on purpose" line into history on a graceful stop (OBS-2 O-2) | §5.3 V-e (G-5) |
| F-NIR-10 (v0.2) | An agent proposal can only be recognized from message text; reading prose is excluded (EXEC RC-5), so an exact proposal line is designed | §5.7 RN-3, RN-5; U-NIR-8 |

## UNRESOLVED

| Item | Owner | Point of need | Effect |
|---|---|---|---|
| U-NIR-1 Effect of DM-4/DM-5 | App implementation owner with DEL-01-01 | Before card implementation | PROPOSED forms; effect not observed |
| U-NIR-2 AO-1 or AO-2 (TBD-003) | App implementation owner | Before attachment implementation | AO-1 assumed |
| U-NIR-3 *Closed (OBS-2 O-2):* requests are not raised again after a restart | — | — | Note removed |
| U-NIR-4 Use of `thread/attachment/*` | App implementation owner | If a requirement needs per-thread attachment persistence | Not used |
| U-NIR-5 *Closed by R18-5* | — | — | PD-5 DERIVED; EXEC RC-4 gains the sentence (FE-13) |
| U-NIR-6 *Ruled (C-02):* D5 adds `a15_record`, `revision` as optional; the view also reads `library_entry` | — | — | §7 |
| U-NIR-7 *Filled:* O-1 and O-3 confirm TO-4 and CS-6; O-4 confirms the descendant line through an adapter only (R18-9). "Primary completed, child running" stays not observed | DEL-01-03 | When observed | §5.5 |
| U-NIR-8 *Ruled (R20-5, R20-9; recorded at RX):* the line forms `Next workflow: ‹origin›:‹name›` and `Workflow finished: ‹origin›:‹name›`; the shipped product guidance states both (ROLE-v0.2 GS-7) | — | — | RN-3…RN-7; the buttons' wording and placement stay PROPOSED |
| U-NIR-9 *Ruled (R20-6; recorded at RX2):* the source conversation's agent drafts the handoff summary in a visible turn there; the person edits it; the App adds only a header naming the source | — | — | CA-2; the request's wording and the failure fallback stay PROPOSED |
| U-NIR-10 Text bound disposed in CC-NIR-ATTACHMENT-REF candidate; image/provider observation still open | App implementation owner with DEL-01-05 (model context); source concurrence received2026-10-05 | Before attachment implementation and candidate image/provider witness |262144 original-file bytes inclusive (UTF-8/no NUL), existing named/image rules; not a context limit. Image read/adoption remains unobserved; no human gate inferred |

## Changes

- CC-WR-TRIALS (2026-10-10; in place, no version step): AT-8, TC-2 and §7's K-7 sentence follow WR TT-2…TT-13 as revised by the owner's direction on WR U-WR-24 (trial text in place of the draft attachment pre-fill; AT-10 not used for drafts).
- G (closeout node G, 2026-10-02; in place, no version step): R22-3, the stop control in several windows (§4.8 WI-5); row "G" in "Changes from v0.1" at the top.
- RV21 (repairs from V21, 2026-10-02; in place, no version step): R21-2, R21-3 (IF-5), V21-A MINOR 4–9 and 14, V21-B's Stop Codex label; row "RV21" in "Changes from v0.1" at the top.
- RX2 (design pass 3 residual sweep 2, 2026-10-02; in place, no version step): R20-11 and R20-6, row "RX2" in "Changes from v0.1" at the top.
- RX (design pass 3 residual sweep, 2026-10-02; in place, no version step): R20-9 "End run" offer, row "RX" in "Changes from v0.1" at the top.
- v0.2 (D round 2, 2026-10-02): see "Changes from v0.1" at the top.
- v0.1 (D round 1): first version.
