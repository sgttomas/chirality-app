# Additive role selection and supply

- Contribution: DEL-02-04/ROLE-v0.1 (first Design file of this deliverable)
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Run and node: `APP-V4-DESIGN-PASS-3-20261001`, node D6 (BRIEFS.md "D — design nodes, round 1", row D6). Executor: Type 2 TASK (Claude Opus 5.5, high effort), no delegation. Date 2026-10-01; repository HEAD `dc031b5bec` (branch `claude/chirality-app-v4-60-percent-a41fd5`).
- Binding direction: DECISION-K3 as revised (OWNER_DECISIONS.md of this run): **K-9** (the App ships default role guidance and seeds an editable copy in its own data folder; a change takes effect at the conversation's next idle point, never mid-turn; the record names the guidance by content), **K-10** (the task role's guidance states that a task agent does not delegate, labelled "stated, not enforced"; any delegation a task agent makes is recorded and shown; no override of the user's Codex configuration), K-7 (only registered revisions run), K-3 (no model until the person chooses). Rulings R17-1, R17-5, R17-8, R17-9, R17-10, R17-13, R17-14, R17-15; R1–R16 stand.
- Serves (ScopeOfWork): OUT-001 (design of the code), OUT-002 (the identity and limit account, §6), OUT-003 (fixture design and a design prototype, §10, which is not product code); REQ-001…REQ-006; AC-001…AC-006 by designed verification (§11); VER-001…VER-006 (cases designed; offline prototype cases run; nothing qualified).
- Standing labels (R17-13): `observed` (seen live, cited), `observed-in-generated-types` (the 0.158.0 generated protocol output, read in the session scratch folder `codex-0.158.0/gen`), `inference`, **OBS-2 pending** (a cell the local observations of this run will settle in round 2), **PROPOSED** (a design structure no one has decided). v3 code is cited as historical evidence only, never as a v4 commitment.

**Consumed inputs** (sha256, first 16 hex digits, `shasum -a 256` in the working tree):

| Input | sha256 | How read |
|---|---|---|
| Run `BRIEFS.md`; `OWNER_DECISIONS.md`; `R17_RESOLUTIONS.md`; `DECISIONS_PENDING.md` | `b261394112d7264e`; `9d18c40dd7d894dc`; `b0af81bcbad9bc52`; `431ec4eb22a0b913` | Whole (DECISIONS_PENDING: K-9…K-12 and Part 2) |
| `SURVEY/S1-C.md` | `06a8a6667ca7c64d` | §0, Part B, Part C whole |
| DEL-02-04 `ScopeOfWork.md`; `Dependencies.csv` | `3acfaa62a3bbf003`; `0cb255b3270dfe61` | Whole; rows via S1-C §B.2 and DAG-003 |
| DEL-01-01/HOSTING-BOUNDARY-v0.8 `HOSTING_BOUNDARY.md` | `3cf0381c42358fec` | §8 (S-6, S-7, receivers table), §8.1, §8.2, §8.4, F-16, F-20, UNRESOLVED, VC-19 |
| DEL-01-01 `PIN_SPIKE_0.158.0.md`; `OBS_1_0.158.0.md` | `0e090a4ca14e3ec3`; `7b984b541edca0b1` | P-15 row; instruction and delegation facts by search |
| DEL-02-01/WD-v0.8 `WORKFLOW_DECLARATION.md` | `517821d18fc95830` | §3.5 CR-7, §3.9, §4.2.5 HC-3/HC-4, §4.7, §5, §6.1, §6.2, §6.4 HL-3, §7, §9 A-6, U-09, U-14 |
| DEL-02-03/EXEC-v0.6 `EXECUTION_COMPATIBILITY.md` | `64e732d502d0b91d` | §2.6 A-3, §6.1 *supplied* |
| DEL-04-03/RS-v0.8 `RECORD_SEMANTICS.md`; `RS_RECORD.schema.json` | `b25cc90e9e252f50`; `b63a7e421b885854` | §4 R3, R5a; §10; §13.1–§13.3; `$defs.suppliedGuidance`, `$defs.contentIdentity` |
| DEL-03-04/GUIDE-v0.5 `HOST_INTEGRATION_GUIDE.md` | `5b87996d9c16d5d2` | Row 8, M8.6, X-06, G-1 |
| DAG-003 `DependencyEdges.csv`, `CandidateEdges.csv` | — | Every row naming DEL-02-04, DEL-02-02, DEL-01-03, by script (§7.3) |
| Generated types at 0.158.0 (scratch, read only) | — | `v2/ThreadStartParams`, `ThreadResumeParams`, `ThreadForkParams`, `ThreadStartResponse`, `ThreadResumeResponse`, `Thread`, `ThreadStatus`, `ThreadActiveFlag`, `ThreadItem` (`collabAgentToolCall`, `subAgentActivity`), `CollabAgentTool`, `Config`, `ConfigLayerSource`, `Model`, `MultiAgentVersion`; root `SubAgentSource`, `SessionSource`, `MultiAgentMode`, `CollaborationMode`, `Settings`; experimental `ThreadStartParams`, `TurnStartParams` |
| Root `AGENTS.md`; `agents/registry.json`; `agents/AGENT_TASK.md` (current Root practice, evidence only) | `c8ce87ef342902cb`; `767fdfe25f3722b8`; `1a13a5b00b3ce01f` | Whole |
| v3 exemplar (evidence only): `projects/chirality-runtime/packages/core/src/product-native-role-config.ts`, `native-role-config.ts`; `projects/chirality-app-dev/frontend/electron/product-instructions.ts` | `9a1ca24c6978c15f`, `0da6d44581fa6333`, `465129dff1464e51` | Whole / by search |

**Reading of the ScopeOfWork where it lags (R17-15).** The SoW was revised by
neither amendment (S1-C §B.1). This file reads it as follows, and the return
file proposes the SoW text for SCA-V4-003:

- Its open-matter table: OI-001 and OI-002 were ruled by D2 and D3 for the
  App's contracts; OI-012 is answered by D4 (0.158.0 is the definition and
  generation pin; nothing is qualified, HOSTING U-01); OI-017 is resolved for
  the current definition run; **OI-018 is answered for the App by DECISION-K3
  K-9** and stays open for hosts (WD U-14).
- REQ-002 "supply the selected role's guidance": read as also supplying the
  selected **workflow's** entrypoint, composed with the product guidance and
  the role into `developerInstructions` (R17-8; Part 2 of DECISIONS_PENDING,
  not objected to). Four first-increment files already assume this (S1-C §B.2.2).
- REQ-003 and AC-003/AC-004: read with K-10. The limit is stated, not
  enforced; delegation by a task agent is recorded and shown.
- REQ-001 "exactly the four": read as "exactly four roles are offered". A
  conversation with **no role** (untyped) is allowed (R17-9); it is not a
  fifth role.

---

## 1. What this file defines

| Defined here | Not defined here (owner) |
|---|---|
| Role selection per conversation, with no role allowed, and its states (§3) | The four role meanings (DEL-02-01, WD §5.1, settled) |
| The App's role set and guidance store: shipped defaults, seeded editable copy, release upgrade (§4) | Host guidance distribution (OI-018 for hosts; WD U-14); host seat mapping (WD U-09; deferred, DECISION-3) |
| Composition of product guidance, role and selected workflow into the one supplier input, and what the role supply never sets (§5.1, §5.2) | Carriage and boundary evidence of the input (DEL-01-01, HOSTING S-6, §8.2) |
| Native child roles for delegated children (§5.3) | Delegation views (DEL-01-03, K-5) |
| When a change reaches a conversation: the idle point (§5.4, §5.5) | Durable custody, relaunch and recovery reads (DEL-01-02) |
| The supply record, the limit account and limit observations handed to receivers (§6; two PROPOSED schemas) | Run-record format and writer (DEL-04-03); consumer adoption (DEL-11-02, each consumer owner) |
| Interfaces, sequences and failure behaviour (§5.6, §7) | Workflow registration and selection (DEL-02-02); the compatibility check (DEL-02-03) |
| Reuse account against the v3 exemplar (§9); verification (§11) | Model choice (DEL-01-05; K-3); permission policy (D3: the person's own Codex settings) |

Left out, and why: any fifth role or host role picker (V4-HOST-05; CLM-003);
enforcement of the task limit (K-10); consumer adoption and retirement
(OI-024, DEP-006); placement beyond the R17-5 proposal (OI-008, OI-014).

## 2. Facts and decisions this design rests on

| # | Fact or decision | Standing | Source |
|---|---|---|---|
| B-1 | The four roles and their meanings; no fifth role; supply is DEL-02-04's | SETTLED | WD-v0.8 §5.1; V4-ROLE-01/03 |
| B-2 | Guidance is supplied additively, preserving the harness's own instructions; `developerInstructions` carries it; `baseInstructions` is never set | SETTLED (R17-8; Root AGENTS.md "supported additive instruction inputs that preserve Codex's own base instructions") | R17-8; HOSTING S-6 |
| B-3 | `baseInstructions` and `developerInstructions` exist on `thread/start`, `thread/resume` ("Configuration overrides for the resumed thread") and `thread/fork` ("Configuration overrides for the forked thread") | observed-in-generated-types | `v2/ThreadStartParams.ts`, `ThreadResumeParams.ts`, `ThreadForkParams.ts` |
| B-4 | `turn/start` (stable) carries no instruction field; the experimental `turn/start` carries `collaborationMode` whose `settings.developer_instructions` replaces a mode's built-in instructions when non-null | observed-in-generated-types | stable and experimental `TurnStartParams.ts`; `CollaborationMode.ts`, `Settings.ts` |
| B-5 | The thread `config` override map also accepts `instructions` and `developer_instructions` keys (typed in `Config`) and any other key (open map). No `agents` key is typed | observed-in-generated-types | `v2/Config.ts` |
| B-6 | Start and resume responses report `instructionSources`: "Environment-native paths to instruction source files currently loaded for this thread" | observed-in-generated-types; OBS-1 saw `[]` with no project `AGENTS.md` | `ThreadStartResponse.ts`; OBS_1 s4/r4; HOSTING F-20 |
| B-7 | `developerInstructions` reached the model in addition to Codex's base instructions, once, at 0.158.0, with a local model (LM Studio turned the developer role into system) | observed (one turn; not qualification) | OBS_1 "Content sent to the model"; HOSTING §8.1 L-2 |
| B-8 | Whether a resume override applies to an already-loaded thread | not observed (v3: 0.154 ignored them) | HOSTING §8.2 P-15; PIN_SPIKE P-15 — **OBS-2 pending (O-5)** |
| B-9 | `multiAgentMode` on thread and turn start is "@deprecated Ignored. Use Ultra reasoning effort for proactive multi-agent behavior"; no client method controls delegation | observed-in-generated-types | experimental `ThreadStartParams.ts`, `TurnStartParams.ts`; HOSTING §8.4 HCG-A08 |
| B-10 | Delegation is visible as items: `collabAgentToolCall` {tool ∈ spawnAgent, sendInput, resumeAgent, wait, closeAgent, sendMessage, followupTask, interruptAgent, listAgents; senderThreadId; receiverThreadIds; status} and `subAgentActivity` | observed-in-generated-types (stable `ThreadItem`) | `v2/ThreadItem.ts`, `CollabAgentTool.ts` |
| B-11 | A sub-agent thread reports `parentThreadId` and `agentRole` ("Optional role (agent_role) assigned to an AgentControl-spawned sub-agent"); its source is `subagent.thread_spawn {parent_thread_id, depth, agent_path, agent_nickname, agent_role}` | observed-in-generated-types | `v2/Thread.ts`; `SubAgentSource.ts` |
| B-12 | Thread status is `notLoaded`, `idle`, `systemError` or `active {waitingOnApproval, waitingOnUserInput}` | observed-in-generated-types | `v2/ThreadStatus.ts`, `ThreadActiveFlag.ts` |
| B-13 | Codex owns native global and project instruction discovery; the App supplies common guidance plus the active role; changes take effect at a verified idle boundary, preserving prior supplied content and history; "A full-history fork alone does not establish a different role"; "Fresh named children receive the shared product guidance and their intended full role" | Root doctrine (current practice; evidence of intent for the App) | Root `AGENTS.md` (App paragraph) |
| B-14 | Approval and sandbox are the person's own Codex settings; the App does not pin them or veto the user's configuration | SETTLED (D3; Root AGENTS.md) | HOSTING H9; WD §5.2 |
| B-15 | Native agent-role configuration (`agents.<ROLE>.config_file` naming a TOML file with `developer_instructions`) | inference from v3 at 0.154 (historical); not in the 0.158.0 generated types | v3 `product-native-role-config.ts` — **OBS-2 pending (O-4) or round 2** |

## 3. Selection

### 3.1 Rules

- **SL-1 Four roles.** The App offers HELP_HUMAN, HELPS_HUMANS, WORKING_ITEMS
  and TASK with their WD §5.1 meanings, from the bundled role set (§4.1). No
  other role value is accepted anywhere in this file's formats (both schemas
  enumerate the four).
- **SL-2 No role.** A conversation may have no role (R17-9). Its supplied
  guidance is the product guidance alone (plus a selected workflow, §5.1). It
  is shown as "No role", never as a fifth role.
- **SL-3 Preselection.** A new conversation preselects the role whose
  `default_for_new_chat` is true in the bundled role set, read as data (R17-9;
  PROPOSED). It is shown as a preselection the person can change or clear.
  Root's current registry marks HELP_HUMAN; that value is evidence, and the
  shipped value is a release decision (REQ-002: no historical Root default as
  v4 authority). At most one role may carry the mark; with none, a new
  conversation starts with no role.
- **SL-4 Selection is the person's choice, not a reserved act.** Choosing a
  role grants nothing and is not a human act of ACT-v0.8's list; it is
  recorded as the selection element of the supply record (§6.1). An agent
  cannot select or change a conversation's role.
- **SL-5 Domain expressions.** A domain expression (for example the SWB Piping
  Designer) is a workflow, context and tools within one of the four roles
  (V4-ROLE-03); it never appears as a role value (schema enum; prototype IS-7).
- **SL-6 Model independence.** Role selection is independent of model
  selection. With no model chosen (K-3, DEL-01-05) no thread is started and
  nothing is supplied; the selection waits.
- **SL-7 Compatible roles.** When a workflow run is started, the role in force
  (or "no role") is handed to DEL-02-03's check as a runtime value. A role
  outside the workflow's declared compatible roles (WD §4.7) is shown before
  the run starts and recorded with the check; the person may proceed. A
  workflow that requires `agent-delegation` (WD HC-3) with TASK in force is
  *unsupported* by WD §4.7's own rule. Never silently switch the role
  (INTEGRATION, survey item 9; the check's reading is EXEC's).

### 3.2 Conversation role-selection states (T-2; PROPOSED)

The state is an App-kept pointer per conversation (R17-4), not a copy of
Codex history. Prototype: `role_supply.T2`, cases RC-01, RC-15…RC-17, RC-19.

| State | Event | Next | Effect and record |
|---|---|---|---|
| draft (role = preselection or none) | person selects / clears | draft | role set; `preselected` false |
| draft | person sends first message (model chosen) | starting | compose (§5.1); `thread/start`; supply record `thread-start` |
| starting | response | supplied | record outcome `supplied`, thread identity, `instructionSources` |
| starting | composition refused (§5.6 R-cases) | supply-refused | record `refused-before-send` with reason; nothing sent; message kept unsent |
| starting | error response | not-started | record `request-failed`; the person may retry |
| starting | no response (HOSTING `unknown-no-response`) | start-unknown | record `unknown-no-response`; resolved by reading the thread at the next ready generation (DEL-01-02 custody): present → supplied (outcome stays unknown in this record; a new record is written at the next supply), absent → not-started |
| supply-refused | person fixes (restore, reselect) | draft | — |
| supplied | person selects or clears a role; guidance store change affecting this composition; workflow run starts or ends | change-pending | nothing sent; shown "Role / guidance change applies before your next message" |
| supplied | person sends | supplied | ordinary turn (no supply) |
| change-pending | revert to the role in force | supplied | nothing sent |
| change-pending | person sends, thread at an idle point (§5.4 IP-1) | re-supplying | `thread/resume` with the new composition; supply record `idle-change`; the turn waits for the response |
| re-supplying | response, route A (§5.4) | supplied | role updated; then `turn/start` |
| re-supplying | response, route B; error; or composition refused | change-not-applied | shown "Change not applied to this conversation" with the reason; choices: send anyway with the role in force, start a new conversation with the new role, revert |
| re-supplying | no response | re-supply-unknown | the turn is not sent; at the next ready generation the conversation is re-supplied before any turn |
| re-supplying | person sends again | — (refused) | one supply in flight at a time (RC-19) |
| supplied / change-pending | App relaunch | relaunched | — |
| relaunched | person sends | re-supplying | `thread/resume` with the current composition; record `resume-after-relaunch` (§5.5) |

## 4. Where the guidance comes from (K-9)

### 4.1 The role set (bundled, read-only)

The App release contains a role set `roles.json`: per role its name, meaning
(WD §5.1), guidance file path, delegation statement (`may-delegate` or
`does-not-delegate`), the child roles it offers (§5.3; Root's `delegates_to`
read as data: HELP_HUMAN offers HELPS_HUMANS, WORKING_ITEMS, TASK; the two
managers offer TASK; TASK none) and `default_for_new_chat`. It is not
editable: the four roles are fixed (REQ-001). A role set that does not name
exactly the four roles, or marks more than one default, refuses every supply
(`role-set-invalid`). Its content identity is recorded with each supply.

### 4.2 The guidance store: shipped defaults and the seeded editable copy

The release also ships default guidance: the product guidance `AGENTS.md`
and four role files `agents/AGENT_<ROLE>.md`. Their content and section
structure are the App role-guidance owner's; WD §7 left the Root four-section
form to this deliverable, and this file does not check structure (an
authoring convention, not a supply condition).

- **GS-1 Seed.** At first start the App copies each default into
  `<App data>/instructions/` (same relative paths), creating each file
  exclusively; it never overwrites an existing file. A seed record beside them
  notes the release and the default identity seeded per file (RC-02).
- **GS-2 Edit.** The person edits the copy with any editor. The App does not
  restrict who edits it; an edit is identified only by content.
- **GS-3 State.** Each file is *default* (equal to the shipped default),
  *modified*, *missing* or *unreadable*. The App shows the state and offers
  "restore default" per file.
- **GS-4 Read once, at a supply point.** Guidance is read when a supply is
  composed (§5.4), each file once, and the same bytes are hashed and composed
  (no gap between identity and content).
- **GS-5 No silent fallback.** A missing, unreadable, symbolic-link or
  non-UTF-8 file refuses the supply with its reason (RC-08, RC-09); the App
  never substitutes the shipped default without the person's restore.
- **GS-6 New release.** For each file: if the copy still equals the default
  that was seeded, it takes the new default (`release-default-applied`); if
  the person modified it, it is kept and flagged "a new default is available"
  with compare and restore (RC-18). Conversations take up the change at their
  next idle point. (PROPOSED; U-R9.)

**T-1 Guidance file states (PROPOSED).**

| State | Event | Next | Effect |
|---|---|---|---|
| not seeded | first start | default | exclusive create; seed record |
| default | person edits | modified | detected at the next read or display |
| modified | restore default | default | change cause `guidance-restored` |
| default, modified | file removed | missing | supplies needing it refused (`guidance-file-missing`) |
| any | unreadable, link, not UTF-8 | unreadable | refused with the reason |
| missing, unreadable | restore default | default | — |
| default | release with a new default | default (new bytes) | `release-default-applied` |
| modified | release with a new default | modified, new default available | shown; kept |

A change of state is not itself sent anywhere. It reaches a conversation only
through §5.4.

### 4.3 The harness's own instructions

Codex's base instructions (not set by the App, B-2) and the instruction files
Codex discovers natively (global and project `AGENTS.md`; B-6, B-13) are the
harness's own. The App neither composes, removes nor deduplicates them. It
records what the supplier reports as `instructionSources` with each supply.
In this repository, for example, a project conversation would also load Root
`AGENTS.md` natively; that is the harness's own context, recorded, not
App-supplied guidance (F-R5).

## 5. Supply

### 5.1 Composition (format `chirality.role.compose/0.1`; PROPOSED)

The supplied text is the UTF-8 concatenation, in this order:

1. the product guidance bytes (`AGENTS.md` of the copy);
2. if a role is in force: `\n\n# Active role: <ROLE>\n\n` then the role file bytes;
3. if a workflow run is served: `\n\n# Selected workflow: <name> (<origin>, revision <first 12 hex>)\n\n` then the bytes of `WORKFLOW.md` of the selected registered revision.

Rules:

- **CO-1 Parts are byte ranges.** Each part's offset, length and content
  identity are recorded; the separators belong to no part. A reader recomputes
  each part from the supplied text (RC-03; `verify_composition`).
- **CO-2 No normalization.** Bytes as stored (WD RV-3). Non-UTF-8 is refused.
- **CO-3 Workflow entrypoint only.** Only `WORKFLOW.md` is composed (prose and
  declared block together, WD §3.5). Other package files are read by the agent
  with its tools when the method needs them; such a read is a tool item, not
  evidence of supply (R17-8).
- **CO-4 Registered and verified.** Only a registered revision is composed
  (K-7; a draft is tried in an ordinary conversation with no workflow part,
  RC-07). At composition the package is re-read and its revision recomputed
  (WD §6.1 RV-1…RV-5); a mismatch refuses the supply "revision not verified"
  (WD HL-3; RC-06). Nothing unverified is sent.
- **CO-5 One carrier.** The whole composition goes in `developerInstructions`;
  nothing goes in `baseInstructions` or in the `config` keys `instructions` or
  `developer_instructions` (§5.2).
- **CO-6 Size.** No supplier limit is stated in the generated types; the byte
  length is recorded. No App limit is chosen (U-R4).

### 5.2 Inputs the role supply uses and never uses

| Supplier input (0.158.0) | Role supply | Why |
|---|---|---|
| `developerInstructions` on `thread/start`, `thread/resume`, `thread/fork` | **Carries the composition** | R17-8; B-3 |
| `baseInstructions` | Never | R17-8; preserves Codex's base instructions |
| `config` keys `instructions`, `developer_instructions` | Never | One carrier only (CO-5) |
| `config` keys `agents.<ROLE>.description`, `agents.<ROLE>.config_file` | Additive child roles only (§5.3) | R17-9 |
| `config` keys `features.*`, `agents.enabled`, `agents.max_depth`, or any other key | Never | K-10; Root AGENTS.md (no veto of user configuration) |
| `personality` | Never | Deprecated (B-3) |
| `multiAgentMode`; reasoning effort chosen to steer delegation | Never | Deprecated and ignored (B-9); K-10 |
| `approvalPolicy`, `approvalsReviewer`, `sandbox` | Never by role supply | D3, the person's own settings (B-14) |
| experimental `turn/start` `collaborationMode.settings.developer_instructions` | Never by role supply | Plan mode is DEL-01-03's (K-5); if used non-null it is another guidance input HOSTING §8.2 must record (join J-2) |

The request check refuses a role-supply request that carries any "never"
input (`forbidden-input-in-request`; RC-11; schema IS-1, IS-6).

### 5.3 Native child roles (R17-9; mechanism OBS-2 pending)

- **CR-1** Where 0.158.0 supports native agent-role configuration (B-15), a
  thread whose role offers child roles (§4.1) is started with additive `config`
  keys `agents.<CHILD>.description` and `agents.<CHILD>.config_file`. The file
  is written into the App's data folder, named by its content identity,
  created exclusively and verified on reuse (RC-12), holding
  `developer_instructions` = product guidance + `# Active role: <CHILD>` + the
  child's role file (Root: "Fresh named children receive the shared product
  guidance and their intended full role"). No workflow part: the parent's
  brief carries the assignment.
- **CR-2 Additive only.** The App reads the effective configuration
  (`config/read`, read only) and supplies no child role whose name the
  person's configuration already defines (`user-configuration-defines-role`).
  If the configuration cannot be read, none is supplied
  (`user-configuration-not-read`). Delegation itself stays as the person's
  configuration has it: the App enables, disables and limits nothing.
- **CR-3** TASK offers no child roles and receives none. That is not
  enforcement: Codex can still spawn its own default agents (K-10, §6.2).
- **CR-4 Where the mechanism is absent.** If OBS-2 (or a round-2 observation)
  shows that 0.158.0 does not take `agents.<ROLE>.config_file` per thread,
  each entry reads `mechanism-not-supported-at-pin`, children inherit the
  parent's guidance (an **inference** until observed), and this file says so
  to the person ("Delegated agents use this conversation's guidance").
- **CR-5 Child role facts.** A child thread's role is taken from the
  supplier's `Thread.agentRole` (B-11) when it names a child role the App
  supplied to the parent; otherwise it is "inherited from parent (inference)".

### 5.4 When a change reaches a conversation: the idle point (K-9)

- **IP-1 Idle point.** A conversation is at an idle point when its thread's
  last reported status is `idle` or `notLoaded` (B-12), HOSTING §6's register
  holds no outstanding server request for it, and no client request for it
  is in flight (HOSTING §5.2). `active` (including `waitingOnApproval` and
  `waitingOnUserInput`) is never an idle point.
- **IP-2 Never mid-turn.** A role change, guidance edit, release default or
  workflow run start or end is held as *change pending* (T-2). Nothing is sent
  while the thread is active.
- **IP-3 Applied before the next turn.** At the person's next message, at an
  idle point, the App first sends `thread/resume` {threadId, new
  `developerInstructions`, child-role keys} and sends `turn/start` only after
  the resume response. The supply record names the causes (`changeCause`) and
  the previous supply.
- **IP-4 Route (OBS-2 pending, O-5).** **Route A**: the loaded thread takes up
  resume overrides; IP-3 stands as written. **Route B**: it does not. Then
  IP-3's resume is still recorded as *supplied* (it was carried), the
  conversation enters *change not applied*, and the person chooses: send with
  the guidance in force, start a new conversation with the new role (a
  `thread/fork` carrying the new composition is the candidate means; the
  record keeps `forkedFromId`), or revert. The App never reports a change as
  applied on route B. Which route holds at 0.158.0 is the round-2 fill of this
  cell.
- **IP-5 History is kept.** Earlier supplies and Codex history are not
  rewritten (B-13); the record of each supply stays.
- **IP-6 Adoption.** Under either route the record says *supplied*; adoption
  stays *unknown* (P-15).

### 5.5 Resume after relaunch

After a relaunch a thread is `notLoaded`. Before its first turn the App
resumes it with the **current** composition for its role (trigger
`resume-after-relaunch`; `changeCause` filled if the composition differs
from the last supply), so what the conversation runs under is always the
supply the App recorded. Whether Codex would otherwise re-apply the developer
instructions persisted in the rollout is **OBS-2 pending** (O-2, O-5); the
design does not rely on it.

### 5.6 Operating sequences with failure behaviour

**SQ-1 New conversation (optionally serving a workflow run).**

| Step | What happens | Fails when | Then |
|---|---|---|---|
| 1 | Role preselected from the role set; person keeps, changes or clears it | Role set invalid | Supply refused `role-set-invalid`; the App shows the release defect |
| 2 | Person chooses a model (DEL-01-05) and writes a first message | No model chosen (K-3) | Nothing starts; selection kept |
| 3 | If a run is started: DEL-02-02 hands the registered tuple and package; DEL-02-03 runs its check with the role in force | Not registered (K-7) | `workflow-not-registered`; no workflow part |
| 4 | Compose (§5.1) | Missing / unreadable / non-UTF-8 file; revision not verified | `refused-before-send` with reason; message kept unsent; state supply-refused |
| 5 | Child-role keys (§5.3) | `config/read` fails | No child roles (`user-configuration-not-read`); supply continues |
| 6 | Request check (§5.2) | A forbidden input present | `forbidden-input-in-request`; nothing sent (a design defect) |
| 7 | `thread/start` through HOSTING §5.1 | Not ready; error; no response | `request-failed` or `unknown-no-response`; T-2 |
| 8 | Response: thread identity, `instructionSources`; supply record written; HOSTING §8.2 records the carried identity | The two identities differ | Finding "supply evidence mismatch" recorded (VC-R12); the conversation is not shown as supplied with that composition |

**SQ-2 Change at the idle point.** §5.4; failures as T-2 rows *re-supplying*.

**SQ-3 Relaunch.** §5.5; failures as SQ-1 steps 4–8 with `thread/resume`.

**SQ-4 Delegated child.** A thread with child roles delegates (`collabAgentToolCall`
`spawnAgent`); the child thread starts (`thread/started`, sub-agent source). The
App records the child's role per CR-5. Fails when: the items are not delivered
(observation lost) → the child's role is *unknown* for that span.

**SQ-5 A task agent delegates.** §6.3.

**SQ-6 Store edited while a turn runs.** The edit is detected for display only;
it reaches the conversation at its next idle point (IP-2).

**SQ-7 New release.** GS-6; conversations follow SQ-2.

## 6. Evidence handed to receivers

### 6.1 The supply record (`role-supply-record.schema.json`; PROPOSED)

One record per guidance-carrying client request (`thread/start`,
`thread/resume`, `thread/fork`), including those refused before sending. It
carries: the trigger and causes; the request identity and generation
(HOSTING §5, §4); the selection (role or none, preselected or not, role-set
identity); the composed content identity and byte length; each part with its
source (seeded copy path, release, state default/modified, shipped default's
identity; or the workflow tuple, `WORKFLOW.md`, revision verified, run
reference) and byte range; `baseInstructions: not-set`; the child-role
entries; what the supplier reported (`instructionSources`, `agentRole`); the
outcome; and `adoption: unknown`.

- It is the "source identity supplied by the composing owner" of HOSTING §8.2.
  The record's composed identity must equal the identity HOSTING records for
  the carried element (VC-R12).
- It is the proposed body of RS R3 `supplied_guidance` (join J-11), in the
  way RS's `settings_version` references DEL-04-02's body.
- Outside a run, the App writer appends it to the conversation's App-kept
  log (RS §13.1 S-A form; custody with DEL-01-02). It is App-observed, never
  authority for what Codex holds (R17-4).
- Content identities carry a method designation; the prototype uses the
  illustration `proto-sha256-0`. The algorithm is open (HOSTING U-08).

Valid instance `role-supply-record.valid.example.json` (a TASK conversation
serving a run of the invented `demo-check`); invalid instances
`role-supply-record.invalid.examples.json` IS-1…IS-7.

### 6.2 The limit account (`role-limit-account.schema.json`; PROPOSED)

Per App release, per role: meaning, delegation statement, guidance state and
identity, and each stated limit with its standing.

| Limit | Role | Standing (default guidance) | Shown as | Not reported as enforcement |
|---|---|---|---|---|
| L-TASK-1 A task agent does not delegate | TASK | `stated-not-enforced` (K-10; no supplier control at 0.158.0, B-9) | "Stated, not enforced" | approval policy, sandbox, the person's configuration |
| L-ALL-1 Work within the brief's write targets | all four | `stated-not-enforced` | "Stated, not enforced" | brief text, worktree, sandbox, approval policy (AC-004) |

- **LA-1** `enforced-by-supplier` requires a named mechanism with evidence; no
  limit has one at 0.158.0.
- **LA-2** If the role's guidance copy is *modified*, the App does not read the
  text for the limit: each of that role's limits reads `unknown`, "Not known
  whether the supplied guidance states this" (RC-10; schema IL-2).
- **LA-3** The other three roles keep native delegation as the person's
  configuration allows; the App adds no limit to it (AC-003's last sentence).
- **LA-4** The account is shown where a role is chosen and in the delegation
  view, in the words of the "Shown as" column.

### 6.3 Limit observations: a task agent delegates (K-10)

- **DL-1 Trigger.** A `collabAgentToolCall` item with tool `spawnAgent` whose
  sender thread has TASK in force: supplied to it (§6.1), reported as its
  `agentRole` for a child role the App supplied, or inherited (inference).
- **DL-2 Once per item.** `item/started` and `item/completed` of one item give
  one observation (RC-14).
- **DL-3 Nothing is prevented.** The App does not decline, interrupt or answer
  for the agent; the delegation proceeds as Codex runs it.
- **DL-4 Shown and recorded.** Shown in the conversation; handed to DEL-01-03's
  delegation view as a runtime label (§7.2 O-6); written to the run record
  when the conversation serves a run (RS R3 "limits", join J-11).
- **DL-5 Not observations.** Delegation by a role that may delegate; other
  collab tools of a task agent toward a child it already spawned (they belong
  to the same delegation).
- **DL-6 If items are not delivered** for a spawn (OBS-2 O-4 pending), the
  account says "delegation by a task agent: not observable at this pin".

### 6.4 Selection, supply, adoption, behaviour and consumer adoption kept apart (CLM-004, AC-005)

| Fact | Evidence in this design | Who records | Standing |
|---|---|---|---|
| Selection | T-2 state; supply record `selection` | App (the person's choice) | App-observed |
| Source resolution | Each part's source and content identity | App composition | App-observed |
| Supply | Supply record `outcome: supplied`, matched with HOSTING §8.2's carried identity | App; DEL-01-01 boundary tap | observed at the boundary |
| Provider adoption | None; `adoption: unknown` in every record | — | unknown (P-15); `instructionSources` shows discovered files only |
| Observed behaviour | Codex history read back (R17-4); limit observations | Codex; App observation | per item |
| Consumer adoption | Not here. DEL-11-02 records the adopting consumer's actor and scope | DEL-11-02; the consumer owner | never inferred from supply or publication |

## 7. Interfaces

### 7.1 Consumed

| ID | Supplier and contribution | Row (DAG-003) | Condition of use | When the exchange fails |
|---|---|---|---|---|
| C-1 | DEL-01-01: carriage of `developerInstructions` on start/resume/fork through §5.1, and §8.2 evidence (S-6) | DEP-02-04-010 (admitted) | Child `ready(g)` | `refused-not-sent` → `request-failed`; `unknown-no-response` → T-2 *start-unknown* / *re-supply-unknown* |
| C-2 | DEL-01-01: thread status notifications and the §6 register, for IP-1 | DEP-02-04-010 | Notifications observed in order | Status unknown → not an idle point; change stays pending |
| C-3 | DEL-01-01: item and thread notifications for `collabAgentToolCall` and sub-agent `thread/started` (HCG-A08) | DEP-02-04-010 (scope reading; return file asks to widen its statement) | Observation not lost | Span with lost observation → child role and limit observation *unknown* |
| C-4 | DEL-01-01: `config/read` (HCG-B07), read only | DEP-02-04-010 | — | No child roles supplied (`user-configuration-not-read`) |
| C-5 | DEL-02-01: role meanings (§5.1), compatible roles (§4.7), identity tuple and revision rules (§6.1) | DEP-02-04-011 (held, SCC-002) | — | — (definitions) |
| C-6 | DEL-02-02: the selected registered revision's tuple and package location | **none; new row proposed** (§7.3) | Registered (K-7) | Not resolvable → `workflow-not-registered` / `revision-not-verified` |
| C-7 | DEL-01-05: a chosen model (K-3) | none (runtime condition) | — | No start (SL-6) |

### 7.2 Offered

| ID | Receiver and contribution | Row | Form |
|---|---|---|---|
| O-1 | DEL-01-01: the source identity for §8.2, per request | DEP-02-04-010 (mirror R-11-1 pending) | Supply record (§6.1), runtime |
| O-2 | DEL-04-03: supply records, limit account, limit observations | DEP-02-04-012 (held, SCC-002) | Two schemas; join J-11 |
| O-3 | DEL-11-02: the same evidence, with no adoption claim | DEP-02-04-013 (admitted) | As O-2 |
| O-4 | DEL-03-04: role selection and supply semantics for the guide's row 8 | DEP-03-04-010 (admitted) | §3–§6 |
| O-5 | DEL-10-03: the supply obligations for the responsibility trace | DEP-10-03-010 (admitted) | §3–§6 |
| O-6 | DEL-01-03: the role in force per thread and the L-TASK-1 label for its delegation view | none (runtime value) | §6.3 DL-4 |
| O-7 | DEL-02-03: the role in force for its check; the workflow part (EXEC A-3) | none (runtime value) | §3.1 SL-7; §5.1 |
| O-8 | DEL-01-04: the role selector's state for the conversation start display (K-3) | none (runtime value) | T-2 |

### 7.3 Register rows and cycles (R17-10; checked by script over DAG-003)

- **New row proposed:** DEL-02-04 consumes DEL-02-02 (C-6), UPSTREAM
  INTERFACE. Both are already in SCC-002 (held layer: its members are DEL-01-04,
  DEL-02-01…DEL-02-04, DEL-03-01…DEL-03-03, DEL-04-02, DEL-04-03, DEL-05-01,
  DEL-05-02, DEL-09-09); adding the arc leaves SCC-002's membership unchanged
  (SCC-neutral). In the admitted layer DEL-02-02 does not reach DEL-02-04, so
  no admitted cycle forms.
- **No row toward DEL-01-03.** A row DEL-01-03 → DEL-02-04 would pull DEL-01-03
  into SCC-002 (DEL-02-04 reaches DEL-01-03 through held arcs); so O-6 is a
  runtime value. DEL-02-04 reads the delegation items from DEL-01-01 directly
  (C-3) and needs nothing from DEL-01-03.

## 8. Placement (R17-5; PROPOSED, OI-008)

Composition, store reading, child-role files, the request check and
supply-record writing are in the Rust host, which owns the Codex process and
record writing. The interface presents the selector, the store states, the
limit account and the observations. No agent tool can select a role or write
a supply record. The requirement (SL-4: an agent cannot change a
conversation's role) holds whatever the placement.

## 9. Reuse account (REQ-005, AC-006; v3 is evidence only)

| v3 exemplar | What it does | v4 disposition |
|---|---|---|
| `product-native-role-config.ts` | Per role, writes a TOML file `developer_instructions = common + "# Active role: ROLE" + role`, named by sha256, exclusive create, verified on reuse; returns `agents.<ROLE>.description/config_file` | **Approach reused** for CR-1 (same composition order and file discipline). Must meet CR-2 (additive, user-defined names kept) and the 0.158.0 mechanism check (B-15) |
| `native-role-config.ts` | Pins `agents.enabled=true`, `features.multi_agent=true`, `features.multi_agent_v2=false`, `agents.max_depth=2`; digest over pins and role bytes | **Not reused**: these override the person's configuration (K-10; Root AGENTS.md). The digest idea is covered by the supply record |
| `product-instructions.ts` | Seeds the default `AGENTS.md` into user data `instructions/`, exclusive create, "modified" flag, restore default | **Approach reused** for GS-1…GS-3, extended to the role files and GS-6 |
| v3 turn envelope `requestedRole` incl. "untyped"; ≤ 1 MiB `developerInstructions` | Untyped requests; a size bound | No-role allowed (SL-2); no size bound chosen (U-R4) |
| v3 Runtime service | Hosting topology | Excluded (V4-ARC-03) |

Any reused code is qualified only by candidate evidence against §11; its
history and earlier tests qualify nothing (REQ-005). No common service,
precedence tree or extra UI follows: the selector, the store state with
restore, and the limit labels are the UI this file needs.

## 10. Prototype (R17-1)

`Design/prototype/` (README there): `role_supply.py`, `jsonschema_lite.py`,
`run_cases.py`, invented fixtures. Python 3 standard library; supplier test
double; scratch under `$TMPDIR`.

Run 2026-10-01, from `Design/prototype/`:
`python3 run_cases.py --write-examples --record` (Python 3.13.7), then
`python3 run_cases.py --record`. Output in `prototype/results/run-2026-10-01.txt`:
**33 pass, 0 fail** — RC-01…RC-19 and RC-20 (each example file against its
schema: both valid instances accepted; IS-1…IS-7 and IL-1…IL-5 each rejected
for its named reason).

What it shows, and does not: composition, refusal, record, account, idle-point
and observation rules behave as written against a double. It shows nothing
about Codex: P-15, child roles and delegation items need OBS-2.

## 11. Verification (designed; nothing qualified)

| Case | SoW | What is exercised | Needs | Now |
|---|---|---|---|---|
| VC-R1 | VER-001, AC-001 | Each role selectable; supplied role part equals the role file; no-role conversation; domain expression stays a role (IS-7) | Fixture (prototype); candidate UI | RC-01, RC-03, RC-04 offline |
| VC-R2 | VER-002, AC-002 | Each role's `thread/start` at the boundary: tap bytes vs supply record parts; Codex base instructions present in the provider prompt (OBS-1 method) | Codex at the pin, local model, candidate | OBS-1 once (B-7); per role **OBS-2 pending** |
| VC-R3 | VER-003, AC-003 | TASK conversation asked to delegate: response; observation (DL-1); no enforcing mechanism; a manager role's delegation available | Codex at the pin with delegation, local model | **OBS-2 pending (O-4)**; observation rule RC-14 offline |
| VC-R4 | VER-004, AC-004 | Presented account vs actual controls: "Stated, not enforced"; no sandbox, worktree or brief shown as enforcement | Candidate UI; account fixture | RC-13, IL-1 offline |
| VC-R5 | VER-005, AC-005 | Trace selection → source → supply → adoption unknown → behaviour; supply-only case makes no adoption claim (IS-4); positive consumer adoption | Positive case: DEP-006 / OI-024 evidence | Negative offline; positive AWAITING INPUT |
| VC-R6 | VER-006, AC-006 | Reuse decision and owner mapping (§9) | A reviewer | Designed |
| VC-R7 | — (K-9) | Change pending, applied at the idle point; route B handling | Live for the route | RC-15, RC-16 offline; route **OBS-2 pending (O-5)** |
| VC-R8 | — (K-9) | Relaunch: resume with current composition | Live | **OBS-2 pending (O-2, O-5)** |
| VC-R9 | — (K-9) | Seed, restore, release upgrade | Fixture | RC-02, RC-08, RC-18 offline |
| VC-R10 | REQ-002 | Refusals: revision, draft, missing, non-UTF-8, forbidden input | Fixture | RC-06…RC-09, RC-11 offline |
| VC-R11 | REQ-003 | Child roles additive; user-defined kept; mechanism at the pin | Live for the mechanism | RC-12 offline; **OBS-2 pending (O-4)** |
| VC-R12 | REQ-004 | Supply record identity equals HOSTING §8.2's carried identity | Candidate with the tap | Designed |

## 12. Cells marked OBS-2 pending

| Cell | Question | OBS-2 item | Effect of the answer |
|---|---|---|---|
| B-8, §5.4 IP-4, VC-R7 | Does a loaded thread take up `developerInstructions` on `thread/resume`? | O-5 | Route A or route B |
| §5.5, VC-R8 | After restart, does resume with new instructions replace the persisted ones; what does the thread report? | O-2, O-5 | Confirms or qualifies §5.5 |
| B-15, §5.3, VC-R11 | Does 0.158.0 take `agents.<ROLE>.config_file` per thread, and report `agentRole` on the child? | O-4 (if covered; otherwise a round-2 observation) | CR-1 or CR-4 |
| §6.3 DL-6, VC-R3 | Are `collabAgentToolCall` items delivered for a child spawn; is the child thread readable? | O-4 | DL-1 as written, or "not observable" |
| B-6 | Does `instructionSources` list a project `AGENTS.md` live? | O-4/O-5 incidental | Recording only |

## 13. Findings

- **F-R1 Guidance carriers beyond start and resume.** At 0.158.0
  `thread/fork` also carries `baseInstructions`/`developerInstructions`, the
  experimental `turn/start` carries `collaborationMode.settings.developer_instructions`,
  and the thread `config` map accepts `instructions`, `developer_instructions`
  and (untyped) agent-role keys (B-3…B-5). HOSTING S-6 and §8.2 name start and
  resume only (join J-1, J-2).
- **F-R2 HCG-A08's availability signal is deprecated.** HOSTING §8.4 lists
  `multiAgentMode` as the signal; the generated TS marks it "@deprecated
  Ignored". `Model.multiAgentVersion` (`disabled`, `v1`, `v2`) is a per-model
  signal (join J-3).
- **F-R3 Child role facts exist.** `Thread.parentThreadId`, `Thread.agentRole`
  and `SubAgentSource.thread_spawn.agent_role` (B-11) let the App record a
  child's role (join J-4).
- **F-R4 RS R3 is one source string and one identity.** It cannot hold the
  parts, the selection or the limit observations (join J-11).
- **F-R5 Native discovery inside this repository.** A project conversation on
  this repository would natively load Root `AGENTS.md`; it is the harness's
  own and is recorded, not deduplicated (§4.3).
- **F-R6 The SoW lags** (header reading; SCA-V4-003 proposals in the return).
- **F-R7 Idle is reported.** `ThreadStatus` gives `idle` and `active` with
  flags (B-12), so IP-1 rests on supplier notifications plus the register.
- **F-R8 No typed `agents` configuration at 0.158.0.** Native agent-role
  configuration is not in the generated types; B-15 is an inference from v3.

## 14. UNRESOLVED

| Item | Owner | Point of need | Effect here |
|---|---|---|---|
| U-R1 Content-identity algorithm (HOSTING U-08; WD U-03 for revisions) | App implementation owner with DEL-04-03 | Before qualification records | Method designation carried; illustration used |
| U-R2 Route A or B for an idle-point change | OBS-2 (O-5), then this file | Round 2 | §5.4 IP-4 |
| U-R3 Native child-role mechanism at 0.158.0 | OBS-2 (O-4) or a round-2 observation | Round 2 | §5.3 CR-1/CR-4 |
| U-R4 A size bound for the composition | App implementation owner | Before implementation | Length recorded; none chosen |
| U-R5 Process placement `UNRESOLVED{OI-008}` | App implementation owner | Before architecture production contracts | §8 PROPOSED |
| U-R6 Shared role identity set placement `UNRESOLVED{OI-014}` (WD §9 A-6) | App/shared contract owners | Before structural allocation | Role set is the App's own here |
| U-R7 Host seat mapping (WD U-09); host guidance distribution (OI-018 for hosts) | DEL-02-01 with SWB owner and DEL-02-04 | Deferred (DECISION-3) | Not designed |
| U-R8 Consumer adoption evidence (OI-024; DEP-006) | Owner with affected consumers | Before each adoption | VC-R5 positive case waits |
| U-R9 Release upgrade of unmodified copies taking new defaults automatically (GS-6) | App role-guidance owner (owner may prefer asking) | Before implementation | PROPOSED |
| U-R10 Handling of a compatible-roles mismatch: show and allow (SL-7) | Integrator with DEL-02-03 | Before the check's App display | PROPOSED |
| U-R11 The shipped `default_for_new_chat` value | App role-guidance owner | Before release | Data; Root's value is evidence |

## 15. Excluded acts and owners (REQ-006)

This file performs no act of: DEL-01-01 (carriage, boundary evidence,
qualification); DEL-02-01 (role meanings, shared allocation); DEL-02-02
(registration, selection of workflows); DEL-02-03 (the compatibility check);
DEL-04-01 (operation policy); DEL-04-03 (record format and writer); DEL-11-02
and each consumer owner (adoption); DEL-01-03 (delegation views); DEL-01-05
(model and account); the host implementation owner (host loop, panel, seat);
the person (role choice, guidance edits, restore). It qualifies nothing and
claims no SWBPIPE join, witness or adoption.
