# S1-A — Scoping survey: DEL-06-01 and DEL-06-02

Run `APP-V4-DESIGN-PASS-4-20261003`, node S1-A. Executor: Type 2 TASK (Claude
Opus 5.5, high effort), read-only on project state. Written 2026-10-03 at
repository HEAD `63d366c0e7`. This file claims no SWBPIPE join, witness or
adoption, and changes no register, ScopeOfWork, status, graph, DAG, basis or
Design file.

Paths are relative to `projects/chirality-app-v4/execution` unless they start
with `docs/` (then `projects/chirality-app-v4/docs/`). **States** marks what a
file says; **Inference** marks mine.

## 0. What was read and how

| Input | How read | Identity checked (sha256, first 16 hex, `shasum -a 256`) |
|---|---|---|
| Run `BRIEFS.md` (Common rules, S1), `OWNER_DECISIONS.md` (incl. the later download record), `DISPATCH.md`; `WorkGraphs/APP-V4-DESIGN-PASS-4-20261003/WORK_GRAPH.md` | Whole | `3fe0abc84d6abe2e`, `0883eb7d8b88be7c` |
| DEL-06-01 and DEL-06-02: `ScopeOfWork.md`, `Dependencies.csv`, `_CONTEXT.md`, `_STATUS.md`, `_REFERENCES.md` | Whole | SoW `50c88c9f5c753300`, `3f6bb7b8344a8315`; registers `ddcf0d0efd17b107`, `732a2809db079b8f`. `git log`: each SoW has one commit (`ddd721a90a` INIT); the folders' other two commits (`c1038ae5ac`, `85dcc17c3f`) are register evidence; no SCA has edited either SoW (the SCA-V4-001/002/003 post-change checks list both SoWs `OK`, unchanged) |
| `_DAG/DAG-004/HANDOFF_STATE.md`; `DependencyEdges.csv`, `CandidateEdges.csv`, `ExcludedRows.csv`, `DeliverableNodes.csv` | Handoff whole; CSVs by script | `MANIFEST.sha256` passes. Of the 41 source registers, 40 hash to DAG-004's `SourceRegisterSHA256`; DEL-01-03's differs, by the committed `90d3a5b6a7` (TargetLocation made relative, recorded as `CURRENT_WITH_EVIDENCE_DRIFT`), not an arc change. Reach computed by script over both layers |
| `_Decomposition/Open_Issues.csv`, `External_Dependencies.csv`, `ScopeLedger.csv` (SOW-083…089, 116, 185) | Whole / rows | `Open_Issues.csv` `9c2d916c277f8ce4` |
| SCA-V4-001/002/003 `Amendment_Actions.csv`; SCA-V4-003 `AMENDMENT_PACKET/LEDGER.csv`, `BASIS_AMENDMENT.md`, `SOW_REVISIONS_A/B.md`, `DAG_PREP/CHECKPOINT_C.md`, `RV/`, `reviews/V25.md` | Actions whole; others by grep for `DEL-06`/`PKG-06` and read around each hit | `LEDGER.csv` `e28661cdf3375e15` |
| Pass-2 and pass-3 `closeout/` files | grep for `DEL-06`/`PKG-06`; hits read in context (pass-2 C1-B R-11-1; pass-3 C1-A §3, §4, SC3-01-03-8) | — |
| Owner records: FIRST-INCREMENT DECISION-1/2; DESIGN-PASS-2 DECISION-K1; DESIGN-PASS-3 DECISION-K3 (revised), DECISION-L; DECISIONS_PENDING K-10/K-11 | Read at the cited items; all eight OWNER_DECISIONS files grepped for fleet terms | Pass-3 `8a5d11149045770d`; first increment `a9869129753631b8` |
| Basis clauses: `docs/PRD.md` §0, §4.2, §4.3, §4.5–§4.7, OQ-06; `docs/ARCHITECTURE.md` §3; `docs/HOST_INTEGRATION.md` §1, V4-HI-24/25, §5, §8, §9; `docs/EXAMINATION.md` V4-EXM-13; `docs/OPERATING_METHOD.md` V4-OPS-02, 12–14, 30–33; `conceptual/EXEMPLARS_AND_LESSONS.md` X-15…X-18, L-04 | Clause text | PRD `bb6e786f7a6c01dc`, HOST `d4331c39db7f452c`, ARCH `317d5789272c5206`, EXAM `471798bc2f2dc020`, OPS `98836b5240ed235e`. `git log -- docs/` shows only SCA-V4-001/002 commits; their action lists touch none of the clauses above. SCA-V4-003 changed no basis text (`BASIS_AMENDMENT.md` §A: "None") |
| Design files naming PKG-06 | `grep` for `DEL-06`/`PKG-06` over every `PKG-0[1-5]*` and `PKG-09*` `Design/*.md`; hits in NPTD, RECOVERY, HOSTING, RS, ACT only, each read in context. Read further: NPTD §7, §10–§12, §16–§18; RS §2, §3, §6, §7, §10; ACT §2.1–§2.3, §4.7, §8.5, §9, §10; AAC §0–§2; RECOVERY §0–§2, §7; ROLE §3.3, §4.1, §5.3, §6.2–§6.4; OBS-2 §1, §6, UNRESOLVED; HOSTING header, §8 table row, dynamic-tool rows | NPTD `6eed39dcee4acf4b`, `npt.delegation-export.schema.json` `49f32198cd8d8589`, RS `a91882e74064495c`, ACT `4ef8c0428d42fbe3`, AAC `062ce28c8a4ec0bc`, RECOVERY `d84c7e26f4342d26`, ROLE `92bb421b7bccee9a`, HOSTING `ce235650e8a9494c`, OBS-2 `61cc34ffb811eb27` |
| Generated protocol types at 0.158.0 | The scratch folder HOSTING names (`…/scratchpad/codex-0.158.0/`) exists in this session's scratchpad but holds **0** `.ts` files (`find … -name "*.ts" \| wc -l`). Read instead the committed JSON Schema bundle `DEL-01-01/Design/generated/0.158.0/json-schema/experimental/codex_app_server_protocol.v2.schemas.json` by script | `34f28a486d00fbd2`, equal to the hash NPTD-v0.2 cites |
| PIN_SPIKE, OBS_1, OBS_3 | **Not read directly.** Cited only as NPTD, RECOVERY and ROLE state them | — |
| Root practice: `docs/SPEC.md` §9.8; `workflows/construct-local-work-graph/WORKFLOW.md` | Section / head | Evidence of current file-native practice, not a v4 product commitment |
| App v3 exemplar `projects/chirality-app-dev` | grep over `frontend/src`; `lib/harness/managed-delegation.ts` and `mcp/coordination-tools.ts` read in part | Evidence only, never a v4 commitment |

---

# Part 1 — DEL-06-01 Bounded delegation and current work-graph records

Type DATA_MODEL_CHANGE; App fleet-record owner; `_STATUS.md` INITIALIZED
(2026-09-27); no `Design/` folder. Register: 13 ACTIVE (6 anchor, 7
execution).

## 1.1 Obligations (26: 4 OUT, 6 REQ, 8 AC, 8 VER)

Basis keys: **PM** = PRD V4-PM-01/02 (§4.6); **ROLE3** = PRD V4-ROLE-03;
**AUT/REC** = PRD V4-AUT-01…04, V4-REC-02…05; **A3** = ARCHITECTURE §3
properties (last bullet: conversation recovery ≠ undertaking recovery) and
V4-ARC-05; **HI6x** = HOST V4-HI-61…63; **EXM** = V4-EXM-13; **OPS** =
V4-OPS-02, 12, 14; **CD** = accepted composite decisions 03/05/06/07; **SEED**
= original-seed V4-HI-63. The SoW also carries CLM-001…005 and AX-001…004
(read, not counted).

| Item | One line | Rests on |
|---|---|---|
| OUT-001 | CONFIG: versioned delegation-brief and current-work-graph record definitions in ordinary files | PM-01/02; SEED |
| OUT-002 | CODE: App record read/write and native-delegation association; intended work ≠ observed execution ≠ returned ≠ reviewed integration | A3; CD 05/07; ROLE3 |
| OUT-003 | TEST: basis/owner/return/continuation fixtures incl. absent execution evidence and interrupted/changed basis; local contribution to DEL-09-05 | EXM |
| OUT-004 | DOC: coordination-format compatibility account: versions, writers, consumers, PEC coverage/adoption consequences | HI6x; CD 06 |
| REQ-001 | Brief carries purpose, basis, context, authority, tools, write scope, return; instructional vs host-enforced limits kept apart; child association keeps actual native identity and parent; a prepared brief is not a dispatch | PM-01; ROLE3; OPS-12/14 |
| REQ-002 | One identifiable current file graph per undertaking with selected work, prerequisites, owners, results, continuation; ready vs awaiting-input distinguishable; selected ≠ executing; earlier evidence kept | PM-02; OPS-02; EXM |
| REQ-003 | Planned / executing / returned / reviewed / integrated kept distinct through changed basis and interrupted observation; missing evidence or reconnection proves no child, return, review or integration | A3; CD 05/07; EXM |
| REQ-004 | References to evidence and human acts (PKG-04) keep content, scope, purpose, actor; recorder ≠ actor; separate acts, no invented ordering | AUT; REC; CD 03 |
| REQ-005 | Formats name versions and consumers; a change accounts for PEC coverage/adoption first; projection gives no writer authority; works without PEC | HI6x; CD 06 |
| REQ-006 | No act owned by DEL-01-03, DEL-04-03, DEL-06-02, DEL-09-05, DEL-07-01/02, DEL-10-02/04, PEC, managers or the human | Allocation rows; CD 03/05/06 |
| AC-001 | Representative brief has the seven elements; declared limits vs observed enforcement; undispatched brief makes no child claim | REQ-001 |
| AC-002 | Fixture with one current graph incl. independent ready and dependent waiting work; recovery keeps it and its distinction from the project DAG | REQ-002 |
| AC-003 | Round trips keep observed child/parent identity and evidence; no-dispatch and unknown-outcome cases stay distinct; no fabricated event | REQ-001/003 |
| AC-004 | After changed basis and interruption: ownership, returns, findings, continuation kept; return awaiting review not promoted; reconnection not integration | REQ-003 |
| AC-005 | Faithful reference to a performed human act with actor ≠ recorder; negatives manufacture nothing; independent acts keep actual order | REQ-004 |
| AC-006 | Compatibility account traces a proposed format change to PEC coverage/adoption; wire details left to owners | REQ-005 |
| AC-007 | File-only exercise with PEC absent supports brief/graph read/write, ownership, continuation; absence implies nothing | REQ-005 |
| AC-008 | Outputs cover local scope, preserve every named owner, claim only local coverage | REQ-006 |
| VER-001 | Inspect populated brief vs dispatched and undispatched cases and an unenforced declared limit | AC-001 |
| VER-002 | Save/recover a graph fixture; compare selected, prerequisite, ready, owners, results, next; check current-selector and project-DAG reference | AC-002 |
| VER-003 | Exercise reader/writer + association with DEL-01-03's interface; no-dispatch and unknown-outcome inputs; bind to candidate and supplier basis | AC-003 |
| VER-004 | Changed basis + interruption fixture with active worker, pending review, finding, separate review/integration evidence | AC-004 |
| VER-005 | PKG-04 reference: positive actual act with distinct recorder; fabrication negatives; independent acts in actual order | AC-005 |
| VER-006 | Review format/consumer account with a bounded change example; OI-022 details left open | AC-006 |
| VER-007 | File route without PEC; missing observation alters no authority | AC-007 |
| VER-008 | Artifacts vs SOW rows, interface claims and open-issue table; excluded acts one-for-one | AC-008 |

**Overtaken or re-read by later decisions** (the SoW text is unrevised):

- **AX-004 table, OI-001 and OI-002 rows** ("do not decide the unresolved
  operation policy"; "preserve the separate policy choice"): ruled for the App
  and shared contracts by FIRST-INCREMENT DECISION-1 D2 (five reserved acts,
  carried by ACT §2.1) and D3 (routine tool permission is the user's own Codex
  setting; no classifier mode in hosts). The current OI-001 row states this;
  the residue is OI-021 (operation-specific additions) and DEP-001 (host
  adoption). SCA-V4-002 aligned the same rows in DEL-01-04, DEL-02-02 and
  DEL-09-07, not here.
- **AX-004 OI-012 row and DEP-06-01-013** ("historical examples do not choose
  it"): D4 selected Codex 0.158.0 as the definition and generation pin (not a
  qualification); DECISION-L L-7 makes the Owner the App implementation owner.
  This run's VC node (0.160.0 version-advance check, download approved) may
  change the facts in §1.5. The mirror DEP-01-01-030 says INITIALIZED while
  DEP-06-01-013 says TBD (SCA-003 CHECKPOINT_C C-4, carried to both register
  owners).
- **REQ-001 / AC-001 "declared limits vs observed host enforcement"**: read
  with DECISION-K3 K-10 as revised ("stated, not enforced"; the App does not
  override the person's Codex configuration) and ROLE-v0.2 §6.2's limit
  account, which already names a brief: L-ALL-1 "Work within the brief's
  write targets", standing `stated-not-enforced`.
- **REQ-004 / AC-005 "actual human act with its actor"**: read with
  DECISION-K1 K1-4 (App-captured actor named from App name, OS account and
  Codex account, "identity not verified") and with the App act control now in
  DEL-01-04's contract (SC3-01-04-1, applied by SCA-V4-003).
- **CLM-001 native identities from DEL-01-03**: confirmed from the supplier
  side by SC3-01-03-8 (applied by SCA-V4-003 to DEL-01-03 CLM-003: "its
  delegation identities are received by App `DEL-06-01`") and the new mirror
  DEP-01-03-019.
- **Shaping, not overtaking**: DECISION-L L-2 (a conversation's role is fixed;
  another role is a new conversation, "Continue as", or a same-role fork) and
  ROLE §3.3 CA-1…CA-3, F-1 give the App delegation routes other than a native
  child (see K-B, §3.1).
- DEL-09-02's carried OI-009 wording does not bear on PKG-06. OI-009's
  resolution (K-1) bears only through RECOVERY §1: one Codex process per
  App-owned home, every conversation in exactly one home (inference: a
  native child runs in its parent's process).

## 1.2 Joins

All ACTIVE rows in and out. Arc direction consumer → supplier; layer from
DAG-004.

| Row(s) | Consumer → supplier | Type; maturity / satisfaction | DAG-004 |
|---|---|---|---|
| DEP-06-01-007 (rep.); mirror DEP-01-03-019 | DEL-06-01 → DEL-01-03 | INTERFACE; INITIALIZED / TBD | admitted |
| DEP-06-01-008; package row DEP-04-03-013 (PKG-06) | DEL-06-01 → DEL-04-03 | INTERFACE; INITIALIZED / TBD | admitted (package row not topological) |
| DEP-06-01-011 | DEL-06-01 → DEL-07-01 | CONSTRAINT; INITIALIZED / TBD | admitted |
| DEP-06-01-013 (rep.); mirror DEP-01-01-030 | DEL-06-01 → DEL-01-01 | PREREQUISITE; TBD / TBD (mirror INITIALIZED) | admitted |
| DEP-06-02-008 (rep.); mirror DEP-06-01-009 | DEL-06-02 → DEL-06-01 | INTERFACE; INITIALIZED / TBD | admitted |
| DEP-09-05-006 (rep.); mirror DEP-06-01-010 | DEL-09-05 → DEL-06-01 | PREREQUISITE; INITIALIZED / TBD | admitted |
| DEP-01-03-014 | DEL-01-03 → PKG-06 (package) | HANDOVER | not topological |
| DEP-06-01-012 | DEL-06-01 → DEP-002 (PEC owning project) | CONSTRAINT; TBD / TBD | not topological |

No held arc touches either PKG-06 deliverable.

**What the existing Design files already assume or require of DEL-06-01**
(the grep found mentions only in these):

- **DEL-01-03 / NPTD-v0.2 (pass 3).**
  - §7.6: "PKG-06 consumes native delegation identities … DEL-01-03 exports;
    it imports nothing from PKG-06 (REQ-007, R17-10) and adds no fleet
    feature (TBD-004, OI-006)."
  - §7.7 and `npt.delegation-export.schema.json` v0.2: one record per request
    with export identity, producer {deliverable, typesPin,
    observedVersionLabel}, root thread, descendant nodes (threadId,
    parentThreadId with `parentSource`, sessionId, agentPath, nickname,
    agentRole, depth, spawnedBy {thread, turn, item}, requested {model,
    effort}, lastObserved {status, source, at}, observationEnded,
    delegatingRole {TASK, limitId, standing}) and at least four limit
    statements; `additionalProperties` false. The schema states:
    "There is deliberately no element for a child's return, review or
    integration."
  - §7.3 DR-2: a child's `completed` "is shown as Codex's status; return,
    review and integration are never inferred."
  - §10.2: failure behaviour "No descendants → empty `nodes`".
  - §11: DEL-01-03 holds everything in memory; "Nothing is written to disk".
  - §16.3: "Not proposed, by design: DEL-01-03 consuming … DEL-06-01 (each
    would form an SCC)".
  - Pass-3 C1-A §3: "DEL-06-01 (the fleet receiver of the export) has no
    Design file, so the export seam is defined from this side only."
- **DEL-04-03 / RS-v0.9.**
  - §3 record kinds: "Decision / accepted record | A PKG-06 or
    workflow-owned record an act record may cite | Its owning deliverable".
  - §10, PKG-06 row: consumes "Act records; actor ≠ recorder; lapse";
    supplies back "Decision records as act subjects"; limit "Coordination
    recorder never becomes actor". §10.1 lists DEL-06-01/06-02 via the
    package row, admitted.
  - §2 OF-1, OF-2 (derived views and PEC projections "may locate evidence.
    Their assertion that an act occurred creates none"), OF-8 (recorder never
    the actor by writing), OF-9 (App records with the user's project; path not
    selected); §6.2 HA-1, HA-2, HA-7.
- **DEL-01-01 / HOSTING-v0.9 §8 table:** "DEL-06-01, DEL-09-01 (outside) |
  DEP-06-01-013, DEP-09-01-019 (admitted) | The selected supplier pin, before
  protocol generation and qualification | … U-01 (0.158.0 is the definition
  and generation pin only)".
- **DEL-01-02 / RECOVERY-v0.2 (pass 3), no row:** §0 excludes "recovery of a
  branching undertaking (REQ-006 forbids the claim; PKG-06, DEL-09-05)"; §2
  DEF-6 quit asks first when "an active delegated child [is] observed"; DEF-7
  relaunch is "Not recovery of a branching undertaking"; §7 ledger
  `conversation_index` keeps `forkedFrom` and "opaque receiver tags", and
  "Children are not in `thread/list` and are not indexed (§3.4)".
- **DEL-02-04 / ROLE-v0.2 (pass 3), no row:** §4.1 role set (HELP_HUMAN
  offers HELPS_HUMANS, WORKING_ITEMS, TASK as child roles; managers offer
  TASK; TASK none); §5.3 CR-1…CR-6; §6.2 limit account (L-TASK-1, L-ALL-1);
  §6.3 DL-1…DL-6 (handed to DEL-01-03 only).
- **DEL-07-01, DEL-09-05:** no Design files (tranche 2 / S1-C). Their SoWs
  name DEL-06-01 as owner of "bounded briefs, the current graph and
  native-delegation associations" (DEL-09-05 CLM-001) and of "stable
  coordination formats" (DEL-07-01 CLM-004).

## 1.3 Proposed contract changes still open

- **None in the SCA-V4-003 ledger targets DEL-06-01.** Related items:
  SC3-01-03-8 (INCLUDE, applied; names DEL-06-01 as receiver in DEL-01-03);
  R-02-4 (DEFER: one TBD/PENDING convention across registers; every PKG-06
  satisfaction cell is TBD); CHECKPOINT_C C-4 (mirror maturity
  DEP-06-01-013 TBD vs DEP-01-01-030 INITIALIZED, carried to both register
  owners).
- **Inference, for the next amendment:** align AX-004's OI-001/002/012 rows
  and DEP-06-01-013's statement with D2/D3/D4 and L-7, as SCA-V4-002 did for
  other deliverables. No basis text needs changing.

## 1.4 Open items and owner choices

| Item | Shapes the design now? | Options and what the files say | Owner? |
|---|---|---|---|
| **Q-A1 What "delegation" the records cover** | **Yes**: the association model, states and fixtures differ | (a) native Codex children only (`spawnAgent`; NPTD export); (b) also App conversations started in another role ("Continue as", ROLE CA-1…CA-3, relation `continuedFrom`) or same-role forks (F-1, `forkedFromId`); (c) also work outside the App (other harnesses, human-relayed sessions), file-recorded with no native identity. V4-PM-01 says "Delegation carries a bounded brief" without naming a mechanism; EXM-13: "The person delegates two bounded pieces of work". L-2 makes (b) a real App route | **Yes** (K-B) |
| **Q-A2 Who writes the records** | **Yes**: OUT-002's writer, validation and failure behaviour | (a) agents with their ordinary file tools; the App validates, reads, and writes only associations it observes; (b) an App-offered tool. HOSTING §6.1/§8.4: `item/tool/call` is "known-app-unsupported unless the App registers dynamic tools (none defined in this increment)"; `dynamicTools` is experimental-only (the App already declares the opt-in, K-5); (c) the person through App forms. v3 used MCP tools (`delegate_agent`), a wrapper ARCH §3 lists as "Not selected" | **Yes** if (b) (K-D) |
| **Q-A3 Product format vs the method's own files** | **Yes**: OUT-001, OUT-004, consumers | Root SPEC §9.8 and `construct-local-work-graph` already define `_Coordination/WorkGraphs/<undertaking>/WORK_GRAPH.md` and `AgentRuns/<RunID>/` records (current practice, DEL-10-02's in the App). (a) the App reads and writes that layout with a versioned structured part; (b) its own versioned records, which the method may adopt later (an instruction change, DEP-006/OI-018). Location in the user's project is unselected (RS OF-9) | **Yes** (K-C) |
| Q-A4 Binding a brief to a child | Yes, locally | Codex offers no client-writable tag on a thread (`ThreadMetadataUpdateParams`: only `daybreakEnabled`, `gitInfo`, `projectId`; observed-in-generated-types). Candidates: the spawn `prompt` content identity matched to the brief; a brief reference carried in the message; `task_name` under `multi_agent_v2` (person's configuration). Inference: association must be App-side | No |
| Q-A5 What counts as "returned" | Yes, locally | The child's final text arrives in `wait`'s `agentsStates[child].message` (OBS-2, through the adapter); NPTD's export has no such element by design. Alternatives: a named return artifact in the brief, recorded when received. Either way native completion alone is not a return (AC-003/004) | No |
| Q-A6 Review and integration actors | Yes, locally | Managers (agents) review and integrate (CLM-003); A3 "examine" covers agent review findings (ACT §2.1); integration has no canonical act; when the person integrates, it needs evidence of the person's act, not inference | No (DEL-04-01 consulted) |
| Q-A7 Depth | Information | At default depth a child gets no delegation tools (OBS-2 §6.2, adapter; ROLE LA-5), so a WORKING_ITEMS child cannot itself dispatch TASK. Under K-10's precedent the App does not change the person's configuration | Inform only |
| OI-001 (D2; residue OI-021, DEP-001) | Little: carried distinction only | Ruled for the App/shared first increment | No |
| OI-002 (D3) | No | Ruled | No |
| OI-006 further fleet scope | Only if expanded | Option B stands; "No extra fleet feature inferred" | Optional (K-F) |
| OI-012 pin (D4; VC in progress) | Facts in §1.5 | 0.158.0 definition pin; 0.160.0 check running | No (directed) |
| OI-022 / DEP-002 PEC envelope | OUT-004 only states "no consumer adopted" | Before operational consumer reliance | No |
| OI-008 process division | Placement only | R17-5 O-1 PROPOSED | No (phase review) |

## 1.5 What exists to build on

**Supplier facts, Codex 0.158.0** (standing labels as in NPTD/R17-13):

- *Observed, stock pairing* (OBS-2 §6.1): `multi_agent` stable, on by
  default; delegation tools travel only inside a `namespace` tool
  (`multi_agent_v1`: `close_agent`, `resume_agent`, `send_input`,
  `spawn_agent`, `wait_agent`; `spawn_agent` takes `fork_context`, `items`,
  `message`, `model`, `reasoning_effort`). With `multi_agent_v2`: namespace
  `collaboration` (`followup_task`, `interrupt_agent`, `list_agents`,
  `send_message`, `spawn_agent`, `wait_agent`; spawn takes `fork_turns`,
  `message`, `model`, `reasoning_effort`, `task_name`). `[agents.X]` adds
  `agent_type`. `multi_agent = false` sends none. LM Studio 0.4.16 drops
  `namespace`, so delegation never reaches a stock local model.
- *Observed through the OBS-2 adapter, not stock* (§6.2): `spawnAgent` item
  started with `receiverThreadIds` [] and completed with the child;
  `agentsStates` `pendingInit` then (at `wait`) `completed` with the child's
  final text; child notifications on the same connection, no `thread/started`;
  `thread/read` of the child gives `parentThreadId`, `agentRole`,
  `agentNickname`, `source.subAgent.thread_spawn` {parent, depth 1},
  `ephemeral` false; `thread/list` omits children, `thread/loaded/list`
  includes them; the child receives its role file's instructions, not the
  parent's (O-4a); a TASK-guided parent delegated (O-4b).
- *Observed-in-generated-types* (committed JSON Schema, by script):
  `Thread` has `parentThreadId` ("only be set if this thread is a subagent"),
  `forkedFromId`, `sessionId` ("shared by threads that belong to the same
  session tree"), `agentRole`, `agentNickname`, `projectId`, `name`;
  `CollabAgentTool` {spawnAgent, sendInput, resumeAgent, wait, closeAgent,
  sendMessage, followupTask, interruptAgent, listAgents}; `CollabAgentStatus`
  {pendingInit, running, interrupted, completed, errored, shutdown,
  notFound}; `CollabAgentState` {status, message}; `collabAgentToolCall`
  {id, tool, status, senderThreadId, receiverThreadIds, prompt, model,
  reasoningEffort, agentsStates}; `subAgentActivity` {agentThreadId,
  agentPath, kind ∈ started, interacted, interrupted, completed};
  `ThreadSourceKind` includes `subAgentThreadSpawn`.
- HOSTING-v0.9: dynamic tools unsupported in this increment (above); the pin
  row. RECOVERY cites OBS-3 W-6: `forkedFromId` only in `thread/read` and the
  fork response.

**Pass-3 designs to build on:** NPTD §7 (availability rule §7.1, identity
model §7.2, display rules, export §7.7); ROLE §5.3, §6.2, §6.3; RECOVERY §2
(DEF-1…DEF-7: which events are never a stop or a run end) and §7 (ledger:
App-observed pointers only, never content); RS §2, §3, §6, §13.6 (act
requests), §14 (writer/reader states: pending write, partial, read limited,
refused, nonconformant), which a coordination writer can follow.

**Current file-native practice** (evidence; DEL-10-02 owns it in the App):
SPEC §9.8 ("An executed child is required for an execution claim; a brief
alone is insufficient"); this run's `WORK_GRAPH.md` table (ID/outcome, write
scope, needs, check, state with cause, e.g. "WAITING — owner's yes"),
`BRIEFS.md`, `DISPATCH.md`.

**App v3 exemplar** (evidence only; ARCH §3: "Not selected for the target:
… obsolete multi-engine/delegation wrappers"):
`projects/chirality-app-dev/frontend/src/lib/harness/managed-delegation.ts`
(992 lines). `DelegateAgentInput` carries purpose, brief, declaredContext,
tools, writeTargets, dependencies, expectedOutput, acceptanceCriteria,
requiredReturnMarkers, approvalRef. Its `WORK_GRAPH.json` (schema
`chirality-agent-runs/v2`) must declare `nodes`, `edges`,
`concurrencyEligibility`, `expectedReturns`, `fanInGates`,
`humanDecisionPoints`. Files under `_Coordination/AgentRuns/<runId>/`:
`plans/<version>/ORCHESTRATION_PLAN.md` and `WORK_GRAPH.json`,
`instances/<id>/LAUNCH_BRIEF.md`, `STATUS.json`, `RETURN.md`, `notices/`,
`updates/`, `HANDOFF_STATE.md`, written with exclusive create and atomic
rename. *Inference:* v3 set `STATUS.json` to the launcher's
`COMPLETED`, which conflates a child's completion with a return; v4 REQ-003
forbids that.

## 1.6 Design scope for this pass

1. **`Design/FLEET_RECORDS.md`** (one file), containing:
   - record kinds and identity: brief, current-graph selector, graph (work
     items, prerequisites, owners, results, continuation), association
     observation, return, review finding and integration entries, basis-change
     and interruption notes; format name and version on every record, with a
     reader rule for unknown versions (as RS OF-7);
   - per work item, separate facets rather than one status: selected,
     dispatched (evidence), executing (observed), returned (evidence),
     reviewed, integrated, plus `unknown` and `not observed`, each transition
     naming its required evidence (REQ-003);
   - the brief's seven elements and an enforcement account per limit
     (`stated-not-enforced` / `enforced-by-supplier` / `unknown`, consuming
     ROLE's limit account);
   - association rules (Q-A4) for each delegation route the owner selects
     (K-B), including no-dispatch and unknown-outcome;
   - interfaces consumed and offered, with condition and failure behaviour;
   - operating sequences with failure at each step: write brief, dispatch and
     associate, observe, return, review, integrate, basis change, interruption
     (RECOVERY DEF-1/5/6/7), relaunch recovery, two writers, torn write;
   - what PEC absence changes (nothing in authority; AC-007).
2. **PROPOSED schemas** (JSON Schema 2020-12) for brief, graph and
   association/event entries, with valid and invalid examples.
3. **Compatibility account** (OUT-004): versions, writers, consumers (DEL-06-02,
   DEL-09-05; PEC via DEL-07-01, not adopted), change rule, OI-022 left open.
4. **Local prototype** (not product code): round trip, no-dispatch and
   unknown-outcome, changed basis with interruption, PEC absent; designed
   cases for VER-001…VER-008.
5. **Joins and register proposals**: DEL-06-01 → DEL-02-04 (limit account)
   and DEL-06-01 → DEL-01-02 (conversation index, relaunch reads); both
   SCC-safe (§3.2 S-6); any NPTD export extension it needs (§3.2 S-3).

**Leave out:** PEC wire fields and coverage terms (OI-022); the project DAG
(DEL-10-04); views (DEL-06-02); native presentation (DEL-01-03); act records
(DEL-04-03); scheduling, staffing or concurrency budgets (OI-006); numbers;
persistence technology (OI-008 stays PROPOSED); any claim of enforcement.

---

# Part 2 — DEL-06-02 Return, waiting and human-decision workspace

Type UX_UI_SLICE; App fleet-experience owner; `_STATUS.md` INITIALIZED
(2026-09-27); no `Design/` folder. Register: 16 ACTIVE (7 anchor, 9
execution).

## 2.1 Obligations (25: 4 OUT, 7 REQ, 7 AC, 7 VER)

Basis keys: **PM** = PRD V4-PM-03…06; **AUT** = V4-AUT-03…05; **REC** =
V4-REC-01…04; **HA** = HOST V4-HI-25, 30–33; **HI6x** = V4-HI-61…63 and HOST
§8 fallback; **A3**, **EXM**, **CD** as in Part 1; **OPS** = V4-OPS-30…33.
CLM-001…004, AX-001…004 and TBD-001…004 read, not counted.

| Item | One line | Rests on |
|---|---|---|
| OUT-001 | CODE: return-review queue and waiting-cause views, ownership, causes traced to work records | PM-03 |
| OUT-002 | CODE: prepared decision-package view (exact act, alternatives, consequences, recorded standing); file-derived reconstruction | PM-04…06; HA |
| OUT-003 | TEST: cross-session reconstruction and queue/decision fixtures for DEL-09-05 | EXM |
| OUT-004 | DOC: derivation and ownership boundary: file inputs, native-observation distinction, recovery limits, receiving interfaces, accountable actors | PM-05/06; HI6x; OPS-31/32 |
| REQ-001 | Queue shows returns awaiting examination with ownership; receipt, worker stop or success never marks checked/accepted/integrated | PM-03 |
| REQ-002 | Waiting explained by evidenced cause; dependent, ready and pending-review work distinguished; gaps stay visible, no invented readiness or empty queue | PM-03; EXM; HI-62 |
| REQ-003 | Package states exact act, subject/basis, alternatives, consequences; pending vs recorded; acts kept distinct; "accept" not "approve" for proposals | PM-04; AUT-03; HA |
| REQ-004 | Faithful presentation of a recorded performed act: actor ≠ recorder, content binding and lapse; unobserved acts unclaimed; no acceptance-first order | AUT-03; HA; CD 03 |
| REQ-005 | Reconstruct across sessions from files; native running state, conversation recovery and derived view kept apart; rebuild creates nothing | PM-05/06; REC-02/03; A3 |
| REQ-006 | Works without PEC and without prior product views; absent or limited PEC implies no empty work, readiness or permission | HI6x; CD 06 |
| REQ-007 | No act owned by DEL-06-01, DEL-04-01/04-03, DEL-09-05, DEL-10-02/04, managers, the human, PEC or PKG-07 | Allocation rows |
| AC-001 | Recorded return awaiting examination shown with owner and pending state; native completion does not promote it | REQ-001 |
| AC-002 | Waiting fixtures show cause and owner for dependent and pending-review work beside ready work; unavailable cause shown as a limit | REQ-002 |
| AC-003 | Pending decision shown as exact act with subject/basis, alternatives, consequences; accept ≠ check/approve/rely | REQ-003 |
| AC-004 | Performed decision presented from its record (actor ≠ recorder, binding, lapse); no fabrication from tool success or rebuild; independent acts visible | REQ-003/004 |
| AC-005 | After reconstruction, interruption and changed basis, the views recover returns, standing, ownership, causes, pending choices, gaps and lapse; rebuild alters no source | REQ-005 |
| AC-006 | PEC absent: views rebuild from sufficient files; managers keep ownership; documented bootstrap from file-native controls | REQ-006 |
| AC-007 | Derivation documentation and local evidence name every input, actor, open decision; handed to DEL-09-05 without claiming the joined pass | REQ-007 |
| VER-001 | Queue with a return and a success observation lacking review evidence | AC-001 |
| VER-002 | Dependency waiting, pending review, ready work, unavailable cause; no invented exhaustive taxonomy | AC-002 |
| VER-003 | Pending package vs its source; label comparison | AC-003 |
| VER-004 | Positive faithful case with lapse; negatives; independent checking without prior acceptance | AC-004 |
| VER-005 | Rebuild in another session; interruption; changed basis; input hashes before/after | AC-005 |
| VER-006 | No PEC and limited PEC; bootstrap path inspected; no wire experiment | AC-006 |
| VER-007 | OUT-004 and handoff vs CLM-001…004 and REQ-007 | AC-007 |

**Overtaken or re-read by later decisions:**

- **TBD-001 (OI-001) and TBD-002 (OI-002)**, and their register rows
  DEP-06-02-014/-015: ruled at App/shared level by D2 and D3; the statements
  predate the rulings. CHECKPOINT_C C-5 lists "OI-001/002 rows" as an open
  matter; SCA-V4-003 refreshed DEL-01-03's twin row (R3-01-03-e), not these.
- **CLM-002 "Host owners supply … offered/recorded/presented human-act
  interfaces"**: for App content, the capturing surface is now DEL-01-04's
  App act control (SC3-01-04-1; AAC-v0.2). AAC AK-a lists where it is
  reachable (act log, file or output view, draft under review, question card,
  arrival row); a decision package is not among them, and AK-b says no
  request or rule opens it. No register row links DEL-06-02 and DEL-01-04.
- **REQ-003 decision packages**: ACT-POLICY-v0.9 §2.1 says "Other human acts
  keep the attribution invariants but have no canonical name here: … reserved
  coordination decisions (V4-PM-04)". DECISION-K1 K1-1 settles that the agent
  asks and the product never asks in its place. EXEC CAP-7 and RS HA-1: a
  chat statement is never act evidence. Together (inference): an App decision
  package can be prepared by an agent and shown by DEL-06-02, but the
  person's decision on it has no act kind and no capturing surface today
  (K-A, S-1).
- **REQ-004** actor naming per K1-4 ("identity not verified").
- **Phase 1** (SCA-V4-001: V4-WF-05 and V4-HI-42 phased): a checkpoint
  arrival's *waiting* is "a record label in Phase 1" (ACT §4.7 RC-2); a
  waiting-cause view must not present it as a hold.
- **R17-3 / R19-2 / L-2** (RECOVERY §2): an interrupt, Codex stop, quit,
  observer loss or relaunch is never a run end; runs chain in one
  conversation. These become waiting or observation causes, never
  completions.

## 2.2 Joins

| Row(s) | Consumer → supplier | Type; maturity / satisfaction | DAG-004 |
|---|---|---|---|
| DEP-06-02-008 (rep.); mirror DEP-06-01-009 | DEL-06-02 → DEL-06-01 | INTERFACE; INITIALIZED / TBD | admitted |
| DEP-06-02-009 | DEL-06-02 → DEL-04-01 | INTERFACE; INITIALIZED / TBD | admitted |
| DEP-06-02-010; package row DEP-04-03-013 | DEL-06-02 → DEL-04-03 | INTERFACE; INITIALIZED / TBD | admitted |
| DEP-07-02-015 (DOWNSTREAM, in DEL-07-02's register) | DEL-06-02 → DEL-07-02 | HANDOVER; INITIALIZED / **PENDING** | admitted |
| DEP-09-05-007 (rep.); mirror DEP-06-02-011 | DEL-09-05 → DEL-06-02 | PREREQUISITE; INITIALIZED / TBD | admitted |
| DEP-06-02-012 | → host receipts and human-act interfaces (external, no target ID) | INTERFACE; TBD | not topological |
| DEP-06-02-013 | → evidence of an actually performed human act (positive case) | PREREQUISITE; TBD | not topological |
| DEP-06-02-014 / -015 | → OI-001 / OI-002 | CONSTRAINT; TBD | not topological |
| DEP-06-02-016 | → PEC owning project / OI-022 / DEP-002 | CONSTRAINT; TBD | not topological |

DEP-07-02-015 states: "Hand off the source-file recovery route to DEL-06-02
fleet views when those views are available; file reconstruction continues
without them." DEL-07-02 has no Design file.

**What the existing Design files already assume or require of DEL-06-02:**

- **DEL-04-01 / ACT-POLICY-v0.9.** Header and §10.3: DEL-06-02 is a receiver
  "outside the first increment", row "DEL-06-02 | DEP-06-02-009 | none | Not
  mapped in detail". Sections DEL-06-02 consumes: §2.1 (A1–A15; A8 "request
  … naming the exact act kind, subject and purpose … A request is never the
  act"; the uncanonical "reserved coordination decisions (V4-PM-04)"); §2.3
  decision pairs and act-declined events; §4.7 RC-1…RC-6 (request → capture
  → record, with failure rows); §8.5 consequence vocabulary CQ-E/R/X/D
  (PROPOSED for the owner's phase review, U-02); §9 label rules.
- **DEL-04-03 / RS-v0.9.** §3 and §10 as in Part 1 ("Decision / accepted
  record … PKG-06"; "Decision records as act subjects"); §3 act request
  ("Never the act; satisfies nothing"), act-declined, act-lapsed, run-ended
  kinds and the record-state table (what a reader shows for pending write,
  partial, read limited, refused, nonconformant); §7 lapse states, including
  "*Not yet evaluated* never renders as *not lapsed*"; §13.6 requests as
  record elements.
- **DEL-01-04 / AAC-v0.2 and NIR-v0.2 (pass 3), no row:** AAC §0 ("only the
  person can operate"), §1.2 kinds served (A4, A6, A7, A15 on App content; A5,
  A10, A11, A12, A13 not offered, "adding one later is a row, not a
  restructure"), §2 AI-1…AI-8, AK-a/AK-b; RS §10 cites NIR §8 as the act
  presentation that consumes record-out.
- **DEL-01-03 / NPTD-v0.2:** DR-1…DR-4 wording ("Codex's status",
  "observation ended", task-agent delegation standing).
- **DEL-01-02 / RECOVERY-v0.2:** DEF table and the "Shown as" table in §7
  ("interrupted by quit; Codex reports: …", "outcome unknown", "ended
  unanswered").

## 2.3 Proposed contract changes still open

- **None in the SCA-V4-003 ledger targets DEL-06-02.** Related: R-02-4
  (DEFER; DEP-07-02-015 PENDING vs PKG-06's TBD); C-5 (OI-001/002 rows).
- **Inference, for the next amendment:** align TBD-001/002 and
  DEP-06-02-014/015 with D2/D3; name DEL-01-04's act control in CLM-002; add
  whatever K-A decides (decision act kind and capture route), which touches
  DEL-04-01, DEL-04-03 and DEL-01-04 contracts too.

## 2.4 Open items and owner choices

| Item | Shapes the design now? | Options and what the files say | Owner? |
|---|---|---|---|
| **Q-B1 The person's decision on a package: which acts, which act kind, which surface** | **Yes**: OUT-002, AC-003/004, DEL-09-05's "decides one matter" | (a) packages may only request existing kinds (A4, A6, A7, A15 on App content; A5/A10 on proposals; A12/A13) and other coordination matters carry no recorded human decision; (b) a new canonical act kind for choosing among a package's alternatives, captured by DEL-01-04's act control and recorded in RS; (c) faithful transcription of the person's chat answer, as this repository's OWNER_DECISIONS practice does, which CAP-7 and HA-1 currently exclude in the App. ACT §2.1 leaves "reserved coordination decisions (V4-PM-04)" unnamed | **Yes** (K-A) |
| **Q-B2 Which coordination decisions are reserved to the person** | **Yes** | PRD V4-PM-04: "Decisions reserved to the person arrive as decision packages"; D2's five acts concern checking, acceptance, approval, reliance and grants, not fleet matters (route choice, integration, scope or basis change). CLM-003 of this SoW: "the human retains consequential decisions" | **Yes** (part of K-A; OI-001 residue) |
| Q-B3 Where a package lives | Yes (S-2) | RS §3/§10 expect a PKG-06 "decision record"; neither PKG-06 SoW names one. Candidates: a DEL-06-01 record kind; an RS act request (R16) extended with alternatives and consequences | Deliverable owners, after K-A |
| Q-B4 Consequence vocabulary | Moderately | ACT §8.5 PROPOSED CQ-* values, for the owner's phase review (U-02) | Yes, at phase review (K-E) |
| Q-B5 Waiting-cause set | Yes, locally | VER-002 forbids "an invented exhaustive cause taxonomy"; causes come from records (prerequisite, pending review, pending decision, checkpoint label, connector limitation, observation ended, cause not recorded) | No |
| Q-B6 Rebuild trigger and stale input | Yes, locally | On open vs on file change; RS record states give the display for partial/refused/nonconformant inputs | No |
| Content-identity method (RS U-04; HOSTING U-08; NPTD U-P6) | Lapse display only | TEST VALUE until chosen | Owner with DEL-04-03 (carried) |
| OI-001/002 (D2/D3), OI-006, OI-022/DEP-002, OI-008 | As Part 1 | — | As Part 1 |

## 2.5 What exists to build on

- RS §3 record states and §7 lapse states (ready-made display vocabulary);
  ACT §2.3, §4.7, §9; AAC §0–§2 (the act's capture path); RECOVERY's
  "Shown as" wording; NPTD DR-1…DR-4.
- Conceptual exemplars (`conceptual/EXEMPLARS_AND_LESSONS.md`): X-16
  ("candidate product capability for coordination views (review queue,
  waiting-by-cause)"), X-17 ("Present issue, grounds, alternatives,
  recommendation, effects; name the exact act requested; silence is not a
  ruling; agents may transcribe but not originate a human act"), X-18
  (derived, rebuildable views; "deleting it degrades throughput, never
  correctness").
- Current practice (evidence): pass-3 `DECISIONS_PENDING.md` (packages with a
  recommended option per item) and every run's `OWNER_DECISIONS.md` (exact
  text, custody, effects, and the recorder's reading kept apart) are the
  repository's working form of V4-PM-04; `WORK_GRAPH.md` state cells show
  waiting by cause.
- App v3: no queue, waiting or decision-package view found. grep over
  `frontend/src/components` and `app` for `humanDecision`,
  `HUMAN_DECISION`, `expectedReturns`, `awaiting review`, `orchestration`
  hit only `components/shell/persona-picker.tsx`. v3's data had
  `humanDecisionPoints`, `expectedReturns`, `fanInGates` in
  `WORK_GRAPH.json` and an update acknowledgment `HUMAN_DECISION_REQUIRED`
  (`managed-delegation.ts`).
- No supplier surface: Codex has no queue or decision concept for this;
  `ThreadSection` and `projectId` exist (generated types) but are thread
  organisation, not coordination state.

## 2.6 Design scope for this pass

1. **`Design/FLEET_VIEWS.md`**, containing:
   - inputs by record kind and owner (DEL-06-01 records, RS records and their
     states, NPTD observations as runtime values, DEL-07-02's limitation
     states when available);
   - derivation rules per view: queue membership (return evidence present,
     no review evidence), waiting causes with "cause not recorded", decision
     package fields and pending/recorded standing, lapse display;
   - row states and transitions, with the evidence each needs;
   - the route to capture (open DEL-01-04's act control at the person's click,
     passing the package as a runtime value; DEL-06-02 captures nothing);
   - wording per ACT §9, NPTD DR and RECOVERY;
   - rebuild and cross-session sequences, with failure at each step (missing
     graph, two candidate current graphs, partial or refused records, PEC
     absent or stale, unreadable version), and input hashes unchanged by a
     rebuild;
   - the derivation and ownership boundary (OUT-004) as a section.
2. A PROPOSED **derived view-model schema** only if the fixtures need one;
   it is not an authority.
3. **Local prototype**: derive the three views from fixture files; designed
   cases for VER-001…VER-007, including the hash-before/after check.
4. **Joins and register proposals**: DEL-06-02 → DEL-01-04 (act control),
   SCC-safe in this direction only (§3.2 S-6).

**Leave out:** visual layout beyond states and wording; notifications (AAC
AK-b; OI-006); act capture (DEL-01-04); record formats (DEL-04-03, DEL-06-01);
PEC wire (OI-022); the project DAG view (DEL-10-04); scheduling or staffing
(OI-006).

---

# Part 3 — Across both deliverables

## 3.1 Owner choices, merged and ranked by how much design text depends on them

| Rank | Choice | Items | Why it ranks here |
|---|---|---|---|
| 1 | **K-A Decisions on packages:** which coordination decisions are reserved to the person; what act kind records the person's choice; which surface captures it (options (a)/(b)/(c) in Q-B1) | Q-B1, Q-B2, Q-B3 | Sets DEL-06-02's whole decision half and AC-003/004, DEL-09-05's "decides one matter", and possibly ACT §2.1, RS §6.1/§13, AAC §1.2 and NIR §8. Without it, the package view can be designed only as display of a request |
| 2 | **K-B What delegation the records cover:** native children only; plus App conversations (Continue as, fork); plus outside or human-relayed work, file-only | Q-A1 | Sets DEL-06-01's association model, states and fixtures, the sufficiency of NPTD's export, and DEL-06-02's ownership display |
| 3 | **K-C Format relation to the method's own files**, and where the records live in the user's project | Q-A3 | Sets OUT-001/OUT-004 and the compatibility account; decides whether DEL-10-02's practice and the App share one format (a later instruction change, OI-018/DEP-006) |
| 4 | **K-D Who writes the records** (agents' file tools; an App-offered dynamic tool; the person's forms) | Q-A2 | Sets OUT-002's writer and its failure handling; option (b) reopens HOSTING's "none defined in this increment" |
| 5 | **K-E Consequence vocabulary** (ACT §8.5, U-02), already scheduled for the phase review | Q-B4 | Fills the package's "consequences" field; the design can carry free text meanwhile |
| 6 | **K-F OI-006** any fleet scope beyond option B | OI-006 | Default (none) needs no text; only an expansion adds design |

**Information for the owner, no choice proposed:** at default depth a native
child cannot delegate (Q-A7), so a two-level fleet (HELP_HUMAN → WORKING_ITEMS
→ TASK) is not available unless the person configures it; and the delegation
surface is version-sensitive (v1/v2 tool sets, namespace transport), which the
running 0.160.0 check may change.

**Not owner choices** (deliverable owners): Q-A4, Q-A5, Q-A6, Q-B5, Q-B6, the
content-identity TEST VALUE, register maturity and TBD/PENDING alignment.

## 3.2 Structural questions that could force a later restructuring of a first-increment Design file

- **S-1 No act kind for a coordination decision.** ACT §2.1's closed list
  (A1–A15) names "reserved coordination decisions (V4-PM-04)" without a
  canonical name; RS §6.1 enumerates act kinds and its schema refuses others;
  AAC §1.2 serves A4, A6, A7, A15 only. If K-A picks (b), ACT §2.1, §2.3
  (what the negative is), §4.1 (checkpoint-requirable or not) and §9, RS §6.1
  and `RS_RECORD.schema.json`, and AAC §1.2 gain a kind (AAC calls that "a
  row, not a restructure"; ACT and RS changes are larger). If (c), EXEC CAP-7
  and RS HA-1 would have to change, which reverses a settled first-increment
  rule.
- **S-2 A "decision record" nobody owns.** RS §3 and §10 assign the
  "Decision / accepted record" to PKG-06 and expect PKG-06 to supply
  "Decision records as act subjects", but neither PKG-06 SoW names such an
  output (DEL-06-01: briefs and graph; DEL-06-02: derived views). Either
  DEL-06-01's contract gains a package/decision record (an amendment) and RS
  cites it as a runtime value, or the package becomes an extended RS act
  request (RS §13.6 and ACT A8 change). **A register row in which DEL-04-03
  consumes PKG-06 would form an SCC** (DEL-06-01 → DEL-04-03 and DEL-06-02 →
  DEL-04-03 are admitted).
- **S-3 The delegation export may be too narrow.** NPTD §7.7's schema
  (`additionalProperties` false; defined "from this side only") has no
  spawn prompt or its identity, no `fork_context`/`fork_turns`, no
  `task_name`, no child final message, no `sendInput`/`wait`/`closeAgent`
  interactions, and no conversation-level relations (`continuedFrom`,
  `forkedFrom`). If DEL-06-01 needs them, NPTD §7.7 and the schema version
  change; DEL-01-03 still may not consume DEL-06-01 (§16.3). Reading a child's
  final message from Codex history instead needs a DEL-06-01 → DEL-01-02 (or
  DEL-01-01) row, which is SCC-safe.
- **S-4 Dynamic tools.** If K-D picks an App-offered tool, HOSTING §6.1 and
  §8.4 HCG-A06 ("known-app-unsupported … none defined in this increment") and
  the request-card set change, and ADAPTER F-9 (as HOSTING cites it: dynamic
  tools change "the familiar set for the whole App") applies.
- **S-5 Children are not indexed by RECOVERY.** RECOVERY §7 keeps no child
  index and finds children from parent history. If the fleet needs a durable
  child index, DEL-06-01 holding it needs no change; asking RECOVERY to hold
  it would restructure its ledger. Recommended (inference): DEL-06-01 holds
  it.
- **S-6 Cycle guard (computed from DAG-004, both layers).** Admitted:
  DEL-06-01 reaches DEL-01-01, 01-02, 01-03, 04-01, 04-03, 07-01; DEL-06-02
  adds DEL-06-01 and DEL-07-02. With held arcs both reach 23 deliverables,
  including DEL-01-04, DEL-02-04 and DEL-02-03. DEL-06-01 is reached only by
  DEL-06-02 and DEL-09-05; DEL-06-02 only by DEL-09-05. So:
  - new rows **from** PKG-06 to suppliers (DEL-06-01 → DEL-02-04, → DEL-01-02;
    DEL-06-02 → DEL-01-04, → DEL-02-03) form no SCC;
  - any row making a deliverable PKG-06 reaches **consume** PKG-06 is an
    SCC-forming departure for the owner and `scc-resolution-case`: notably
    DEL-01-03 reading graph state (already excluded, NPTD §16.3), DEL-04-03
    consuming decision records (S-2), and **DEL-01-04's act control
    consuming a package from DEL-06-02** (DEL-06-02 reaches DEL-01-04 through
    held arcs). Unlike A15's descriptor (held row DEP-01-04-009, DEL-01-04 →
    DEL-02-02), a decision package must reach the act control as a runtime
    value, which changes AAC §2's interface table by a row.
- **S-7 (not a first-increment file).** If K-C picks a format shared with the
  method, Root SPEC §9.8 and the `construct-local-work-graph` template become
  writers or consumers of the App format: a separately authorized instruction
  change.

## 3.3 Limits

- The generated TypeScript was not available (the scratch tree is empty);
  supplier types come from the committed JSON Schema bundle.
- PIN_SPIKE, OBS_1 and OBS_3 were read only as other files cite them.
  Delegation behaviour is observed through an adapter only (OBS-2 §6.2), not
  on any stock route.
- Design files without a `DEL-06`/`PKG-06` mention (EXEC, WD, C, P, ADAPTER,
  GUIDE, LOOP, PANEL, AS, CA, XT, ACCESS, WR) were not read for implicit
  assumptions.
- DEL-07-01, DEL-07-02, DEL-09-05 and DEL-10-02 have no Design files; their
  ends of the joins are stated from their SoWs and registers.
- Satisfaction is read from the live registers: every DEL-06-0x execution
  row is TBD; DEP-07-02-015 is PENDING. Nothing here makes any work ready.
