# Additive role selection and supply

- Contribution: DEL-02-04/ROLE-v0.2 (supersedes DEL-02-04/ROLE-v0.1, committed at `63a6e0fa47`, file sha256 `692873d1d025b4ab0bc3d741a19bf1facad5d39b875e58ac1f0127042059b644`)
- Status: DRAFT DEFINITION — not accepted or qualified. Historical definition/prototype standing remains; §2.1 separately records the current bounded supplier sample and receiving-pin clarification. No complete App implementation/adoption follows.
- Run and node: `APP-V4-DESIGN-PASS-3-20261001`, node D6, round 2 (BRIEFS.md "D round 2"). Executor: Type 2 TASK (Claude Opus 5.5, high effort), no delegation. Date 2026-10-02; repository HEAD `e4e14d6ae6`.
- Binding direction: DECISION-K3 as revised (K-9, K-10, K-7, K-3); **DECISION-L L-2** (a conversation's role is fixed for its life; a different role is a new conversation; edited guidance applies to new conversations; workflows are not bound to the conversation); rulings R17 (R17-1, R17-5, R17-9 as amended, R17-10, R17-13…R17-15), **R18-4, R18-6, R18-9, R18-1 (C-04, C-05, C-07, C-08, C-15, C-19)**, **R19-1, R19-3, R19-5, R19-7, R19-8**; **R20-5, R20-6** (`R20_RESOLUTIONS.md` `516d0fe0d3cddb1e`; added in place, no version step); **R20-9** (`R20_RESOLUTIONS.md` `5e68574054a3353e`; added in place at node RX, no version step); **R20-11** (`R20_RESOLUTIONS.md` `b52e0347ad91ba42`; at node RX2); **R22-1, R22-2** (`R22_RESOLUTIONS.md` `2acc830206bd40b3`; at closeout node G, with `closeout/C1-B.md` `b2b8bfad297f9125` §3.3, §3.4, §7 items 1–2); R1–R16 stand.
- Serves (ScopeOfWork): OUT-001 (design of the code), OUT-002 (identity and limit account, §6), OUT-003 (fixture design and a design prototype, §10, not product code); REQ-001…REQ-006; AC-001…AC-006 by designed verification (§11); VER-001…VER-006 (designed; offline prototype cases run; nothing qualified).
- Standing labels (R17-13; R18-9): `observed` (seen live, cited); **`observed through an adapter (OBS-2), not stock behaviour`** for OBS-2's O-4, O-4a and O-4b, which ran through a loopback adapter that flattened Codex's `namespace` tools for LM Studio; `observed-in-generated-types` (the 0.158.0 generated protocol output); `inference`; **PROPOSED**. Every supplier fact names its actual version (R19-5); §2 retains the historical 0.158.0 facts and §2.1 states the bounded current 0.160.0 receiving account; where Codex reports a capability at run time, the App reads it rather than infer it from the version. v3 code is historical evidence only.

## Changes from v0.1

| Ruling / item | Change | Where |
|---|---|---|
| R19-1, R19-7 | **Role guidance only.** The composition is product guidance + the conversation's role, at conversation start. The "# Selected workflow" part, CO-3, CO-4 and the workflow refusals are removed. A workflow is supplied per run as a text element of the run-start turn, composed by DEL-02-02 and started by DEL-02-03; DEL-02-04 composes no workflow | §1, §5.1, §6.1, §7; schema (no `workflow` part kind) |
| R19-7 | The proposed row DEL-02-04 → DEL-02-02 is **dropped**; C-6 removed | §7.1, §7.3 |
| L-2, R19-3 | **Role fixed for the conversation's life.** T-2 loses *change-pending*, *re-supplying*, *change-not-applied* and the route A/B rows; selecting a role on a started conversation is refused. "Continue as ‹role›" opens a new conversation with a handoff summary the person sees and edits before sending | §3.1 SL-8, §3.2, §3.3 |
| L-2, R19-3 (C-17, OBS-K9 closed) | K-9's "next idle point" becomes **new conversations**. An open conversation shows "guidance changed since this conversation started" when its role's guidance differs from what it started with; §5.4 (idle point, routes A/B) is withdrawn | §4.4, §5.4 |
| R19-8; OBS-3 W-6 | **Forks keep the source's role.** `thread/fork` ignores new instructions at 0.158.0; the App sends none and records the fork as *inherited* from the source's start record | §3.3, §5.2, §5.5, §6.1; schema `trigger: fork`, `inheritedFrom` |
| OBS-2 O-5 | `developerInstructions` on `thread/resume` is accepted and ignored at 0.158.0, loaded or not. The App sends no instructions on resume; a relaunched conversation keeps its original supply (observed) | B-8, §5.2, §5.5 |
| R18-4 (C-16); OBS-2 O-4a | **Native child roles honoured** (observed through an adapter): the role file's `developer_instructions` **replace** the parent's for the child, so each file carries product guidance + role (CR-1). A child spawned without a role type has **unknown** guidance, never "inherited" (CR-4) | B-15, §5.3, §6.3; limit schema `roleBasis` |
| C-3 premise (F0 §6, §7.6) | No `thread/started` is sent for a child. Children are found from a completed `spawnAgent` item's `receiverThreadIds` and read with `thread/read`; `thread/list` omits them | §5.3 CR-5, SQ-4, §7.1 C-3 |
| R18-6 (C-18) | The App home shows the person's global `AGENTS.md` and skills by the same link as `config.toml`, so native discovery matches the person's Codex; `instructionSources` records what Codex reports | §4.3 |
| R18-1 C-04, C-05 | Delegation availability: `Model.multiAgentVersion` ≠ `disabled` and the provider accepts `namespace` tools; an effective `features.multi_agent = false` reads missing. Delegation is a stable surface, not labelled experimental | B-9, §6.2 |
| R18-1 C-07, C-08 | No row toward DEL-01-03; the K-10 standing reaches DEL-01-03 as a runtime value and is carried as handed (three values) | §7.2 O-6 |
| R18-1 C-15 | The role preselection appears in DEL-01-04's start display (its ST-5) | §7.2 O-8 |
| R18-1 C-19 | DEL-02-04 keeps its own supply-record log | §6.1 |
| OBS-2 O-4 (adapter), O-4b | A child at the default depth received no delegation tools; a TASK-guided parent delegated anyway, recorded in full | §6.2 (`depth-limit` is not enforcement), §6.3 |
| OBS-3 W-5, O-5b | `thread/settings/update` and `turn/start` `collaborationMode` developer text persist or add; role supply uses neither | §5.2 |
| R19-5 | Version named on every supplier fact; capabilities read at run time | Header; §2 |
| OBS-2 pending cells | All filled or stated open (B-6 stays open) | §12 |
| Schemas | Both stepped to 0.2; supply record: triggers `thread-start` and `fork`, outcome `inherited`, `continuedFrom`, no workflow part, no `changeCause`/`previousSupply`; limit account: `roleBasis` without the inference value, `depth-limit` in `notEnforcement` | §6; `*.schema.json` |
| Prototype | Rewritten to v0.2: 36 pass, 0 fail | §10 |
| R20-5 (U-NIR-8; in place) | The shipped product guidance tells the agent to propose a next workflow with one exact line `Next workflow: ‹origin›:‹name›`, naming one registered workflow; the App reads only that form (never prose; EXEC RC-5) and DEL-01-04 (NIR §5.7) offers "Start ‹workflow› (proposed by the agent)" | §4.2 GS-7 |
| R20-6 (U-NIR-9; closes U-R12; in place) | "Continue as ‹role›": the App asks the source conversation's agent, in a visible turn of that conversation, to draft the handoff summary; the person edits it in the new conversation; the App adds a header naming the source; the summary carries no instructions beyond the person's own text; nothing is sent until the person sends it | §3.3 CA-2; §14 U-R12 |
| RX (residual sweep; R20-9; in place, no version step) | GS-7 gains the finished line `Workflow finished: ‹origin›:‹name›` beside the proposal line; both alone on their own lines, read only in these exact forms; NIR §5.7 offers "End run" on it; the run-start text (WR-v0.2 §16.2) repeats both for the run in force | §4.2 GS-7 |
| RX2 (residual sweep 2; R20-11 (1), (2); in place, no version step) | GS-7 states the placement of the two lines (proposal last; finished last or just before the proposal; each at most once) and that during a run a proposal is offered only as "End ‹A› and start ‹B›" | §4.2 GS-7 |
| G (closeout node G; R22-1, R22-2; in place, no version step; 2026-10-02) | **R22-1:** O-8 cites D3 NR-4 (DEL-01-04 consumes DEL-02-04: the role list, its preselection and the "guidance changed" notice), adopted as a held arc inside SCC-002 with no SCC change; §7.3 records it. **R22-2:** every section v0.2 kept "as v0.1" is written out from ROLE-v0.1 (`63a6e0fa47`) so the file reads alone, with no change of meaning: v0.1's input table and ScopeOfWork reading, §4.1, GS-1…GS-6, T-1, CO-1…CO-6, §6.4, §8, §9's reuse table, F-R1…F-R8, §15. Text is v0.1's except where v0.2's rulings had already changed it, each marked "(v0.2)" in place: "supply" → "start" (L-2; §4.1, GS-4, GS-5, T-1); GS-6 and T-1's release rows reach new conversations only; T-1's restore row has no supply-record cause; CO-5 names `thread/start`; §6.4 adds `inherited`; §9 cites B-15 and CR-1a; F-R1, F-R3, F-R7, F-R8 carry v0.2's amendments; F-R1, F-R2, F-R4 name the v0.8 files they were written against; §15 merges v0.2's additions. No schema or prototype change; prototype rerun | header; §4.1; §4.2; §5.1; §6.4; §7.2 O-8; §7.3; §8; §9; §13; §15 |

**Consumed inputs added at v0.2** (sha256, first 16 hex): run `BRIEFS.md` `316ea29325a0d450` ("D round 2"); `R18_RESOLUTIONS.md` `abf5eee6324647ff`; `R19_RESOLUTIONS.md` `16930ecdcead7511`; `OWNER_DECISIONS.md` `ea96c55710af41c9` (DECISION-L); `DECISIONS_PENDING_2.md` `0ecbf87aae8d4350` (L-2 only); `F/F0_JOINS.md` `e93608be1c6e3eb0` (§1 rows citing D6, §2 C-03…C-19, §6, §7.6); DEL-01-01 `OBS_2_0.158.0.md` `61cc34ffb811eb27` (§6, §7, §9, item table) and `OBS_3_0.158.0.md` `554ac4451d112824` (§8 W-6, §8.1, §9, UNRESOLVED). v0.1's inputs stand for the rest (HOSTING-v0.8, WD-v0.8, EXEC-v0.6, RS-v0.8, GUIDE-v0.5, the generated types, Root and v3 evidence), at the hashes v0.1 recorded, written out in the next table.

**Consumed inputs recorded at v0.1** (carried unchanged from ROLE-v0.1 at `63a6e0fa47`; sha256, first 16 hex digits, `shasum -a 256` in the working tree at `dc031b5bec`, 2026-10-01). Where the v0.2 line above names a newer hash of the same file (`BRIEFS.md`, `OWNER_DECISIONS.md`), the v0.2 hash is the one this version read.

| Input | sha256 | How read |
|---|---|---|
| Run `BRIEFS.md`; `OWNER_DECISIONS.md`; `R17_RESOLUTIONS.md`; `DECISIONS_PENDING.md` | `b261394112d7264e`; `9d18c40dd7d894dc`; `b0af81bcbad9bc52`; `431ec4eb22a0b913` | Whole (DECISIONS_PENDING: K-9…K-12 and Part 2) |
| `SURVEY/S1-C.md` | `06a8a6667ca7c64d` | §0, Part B, Part C whole |
| DEL-02-04 `ScopeOfWork.md`; `Dependencies.csv` | `2327508f2290e7cf`; `0cb255b3270dfe61` | Whole; rows via S1-C §B.2 and DAG-003. ScopeOfWork (SCA-V4-003 revision; re-pinned at pass-4 closeout C1 under R23-5, was `3acfaa62…6601`; SCA-V4-003 blocks read: G-0204-01…13, none requiring a change to this file's design text) |
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
file proposes the SoW text for SCA-V4-003 (v0.1's reading, with v0.2's
changes marked):

- Its open-matter table: OI-001 and OI-002 were ruled by D2 and D3 for the
  App's contracts; OI-012 is answered by D4 (0.158.0 is the definition and
  generation pin; nothing is qualified, HOSTING U-01); OI-017 is resolved for
  the current definition run; **OI-018 is answered for the App by
  DECISION-K3 K-9 as amended by L-2** (edits apply to new conversations;
  v0.2) and stays open for hosts (WD U-14).
- REQ-002 "supply the selected role's guidance": read as **role guidance
  only** (v0.2: R19-7 withdrew v0.1's reading under R17-8 that it also
  supplies the selected workflow's entrypoint; the SoW already speaks of role
  guidance only, so no SoW text is needed for workflows).
- REQ-003 and AC-003/AC-004: read with K-10. The limit is stated, not
  enforced; delegation by a task agent is recorded and shown.
- REQ-001 "exactly the four": read as "exactly four roles are offered". A
  conversation with **no role** (untyped) is allowed (R17-9); it is not a
  fifth role. Read with L-2 (v0.2): the role is fixed for a conversation's
  life.

---

## 1. What this file defines

| Defined here | Not defined here (owner) |
|---|---|
| Role selection per conversation, with no role allowed; the role fixed for the conversation's life; "Continue as ‹role›"; forks (§3) | The four role meanings (DEL-02-01, WD §5.1) |
| The App's role set and guidance store: shipped defaults, seeded editable copy, release upgrade, "guidance changed since this conversation started" (§4) | Host guidance distribution (OI-018 for hosts; WD U-14); host seat mapping (WD U-09; deferred) |
| Composition of product guidance and role into the one supplier input at conversation start, and what the role supply never sets (§5.1, §5.2) | **Workflow supply per run** (DEL-02-02 composes the run-start text; DEL-02-03 starts the run; R19-7) |
| Native child roles for delegated children (§5.3) | Carriage and boundary evidence (DEL-01-01, HOSTING S-6, §8.2); delegation views (DEL-01-03) |
| The supply record, the limit account and limit observations (§6; two PROPOSED schemas) | Run-record format and writer (DEL-04-03); consumer adoption (DEL-11-02) |
| Interfaces, sequences and failure behaviour (§5.6, §7); reuse account (§9); verification (§11) | Model choice (DEL-01-05; K-3); permission policy (D3); durable custody of other owners' records (DEL-01-02, C-19) |

Left out, and why: any fifth role or host role picker (V4-HOST-05; CLM-003);
enforcement of the task limit (K-10); changing a started conversation's role
(L-2); consumer adoption and retirement (OI-024, DEP-006); placement beyond
R17-5 (OI-008, OI-014).

## 2. Historical facts and decisions (Codex 0.158.0; current account §2.1)

| # | Fact or decision | Standing | Source |
|---|---|---|---|
| B-1 | Four roles and their meanings; no fifth role; supply is DEL-02-04's | SETTLED | WD-v0.8 §5.1; V4-ROLE-01/03 |
| B-2 | Role guidance goes in `developerInstructions`; `baseInstructions` is never set | SETTLED | R17-8; R19-1 |
| B-3 | `baseInstructions` and `developerInstructions` exist on `thread/start`, `thread/resume` and `thread/fork` | observed-in-generated-types | `v2/ThreadStartParams.ts`, `ThreadResumeParams.ts`, `ThreadForkParams.ts` |
| B-4 | Stable `turn/start` carries no instruction field; experimental `turn/start` `collaborationMode.settings.developer_instructions` is **added** to the thread's own text (O-5b); experimental `thread/settings/update` with it **persists for the conversation and piles up** (OBS-3 W-5) | observed | OBS-2 §7 O-5b; OBS-3 §7 |
| B-5 | The thread `config` map accepts `instructions` and `developer_instructions` keys and any other key; no `agents` key is typed. `config.developer_instructions` on `thread/fork` is ignored (W-6b) | observed-in-generated-types; observed (fork) | `v2/Config.ts`; OBS-3 §8.1 |
| B-6 | Start and fork responses report `instructionSources`; every observed value was `[]` (the working folder held no `AGENTS.md`) | observed-in-generated-types; observed `[]` only | `ThreadStartResponse.ts`; OBS-2, OBS-3 — **open** for a non-empty value |
| B-7 | The thread's developer text reaches the model in every request beside Codex's base instructions | observed (one role per observation) | OBS-1; OBS-2 §7 (tap) |
| B-8 | `developerInstructions` on `thread/resume` is **accepted and silently ignored**, for a loaded thread and for one loaded by the resume; nothing reports it; the original text stays in force | observed | OBS-2 §7 O-5 (P-15 answered) |
| B-9 | `multiAgentMode` is "@deprecated Ignored". Delegation is gated by the stable feature `multi_agent` (default on); with `multi_agent_v2` the tool set differs. Delegation tools travel only inside a `namespace` tool, which LM Studio 0.4.16 drops; no setting flattens them. Availability (C-04): `Model.multiAgentVersion` ≠ `disabled` (observed-in-generated-types only) and the provider accepts `namespace` tools; an effective `features.multi_agent = false` reads missing | observed (gate, namespace); observed-in-generated-types (`multiAgentVersion`) | OBS-2 §6.1; R18-1 C-04 |
| B-10 | Delegation items: `collabAgentToolCall` (`spawnAgent` started with `receiverThreadIds` `[]`, completed with the child), `sendInput`, `wait`, with `agentsStates` | observed through an adapter (OBS-2), not stock behaviour | OBS-2 §6.2 |
| B-11 | A child is readable by `thread/read`: `parentThreadId`, `agentRole`, `agentNickname`, `source.subAgent.thread_spawn`. **No `thread/started` for a child**; children are absent from `thread/list`, present in `thread/loaded/list`; child notifications arrive on the same connection with the child's thread id | observed through an adapter (OBS-2), not stock behaviour | OBS-2 §6.2 |
| B-12 | Thread status `notLoaded`, `idle`, `systemError`, `active {waitingOnApproval, waitingOnUserInput}` | observed-in-generated-types | `v2/ThreadStatus.ts` |
| B-13 | Root doctrine: common guidance plus active role; Codex owns native discovery; "A full-history fork alone does not establish a different role"; "Fresh named children receive the shared product guidance and their intended full role" | Root practice (evidence of intent) | Root `AGENTS.md` |
| B-14 | Approval and sandbox are the person's own settings | SETTLED (D3) | HOSTING H9 |
| B-15 | Native agent-role configuration `agents.<role>.description` + `config_file` (a TOML file with `developer_instructions`) is **honoured**: `spawn_agent` gains `agent_type` listing the role beside the built-ins `default`, `explorer`, `worker`; the child's `agentRole` is the role; its developer messages are the role file's text, **not the parent's**. Set in the home's `config.toml` in the observation; **per-thread `config` carriage not observed** | observed through an adapter (OBS-2 O-4a), not stock behaviour | OBS-2 §6.1, §6.2 |
| B-16 | `thread/fork` ignores new `developerInstructions` and `config.developer_instructions`, for a loaded and a not-loaded source; the fork keeps the source's developer text and full history, gets a new id, reports `forkedFromId` (only in the fork response and `thread/read`; `thread/list` shows null); its rollout references the source's | observed | OBS-3 §8 W-6, §8.1 |
| B-17 | A child at the default depth received no delegation tools | observed through an adapter (OBS-2), not stock behaviour | OBS-2 §6.2 |
| B-18 | A TASK-guided parent ("you do not delegate") delegated: `spawnAgent`, `sendInput`, `wait`, all recorded | observed through an adapter (OBS-2 O-4b), not stock behaviour | OBS-2 §6.2 |

### 2.1 Current primary carrier account — 0.160.0 (CC-ROLE-PIN-0160)

Named receiving clarification, 2026-10-05; candidate for independent change
review, not a qualification or owner acceptance. The maintained App supplier
pin is **0.160.0**. The stable generated `thread/start.developerInstructions`
string carrier remains the generic additive contract for the composed common
and selected-role UTF-8 text (§5.1); it is not a role-specific supplier API.
The App keeps `baseInstructions` unset and preserves native discovery and the
person's configuration. Generated field existence alone proves no supplier use.

The independently reviewed paired stock-supplier sample observes exactly the
common + HELP_HUMAN composition on **gpt-6.1-sol / medium**, with a capture-only
loopback provider returning HTTP400 and no prediction. The complete4856-byte
App developer part has SHA256
`ad560fe79f9552fef1042dd613a0274ca87babd7165bc1ecd0a278a3ada98343`.
The supplier's exact21779-byte selected model template is separately identified
from pinned source and fully byte-compared in both captures (SHA256
`e1bdd4f8f0df4b20f4a0ffc8a861ce819df45325d8cecdfb92e80379cf8d142e`).
Responses Lite carries it as a separate **developer** message, not top-level
instructions/system-role text. That source-backed identification must never
relabel arbitrary developer text as native base.

The complete remaining input agrees after removing only the exact App part and
top-level opaque input-row IDs. Native global/project content and separately
reported source paths are preserved; tools carried in an additional_tools row
agree, without proving availability or use. Original probe exit1/UNKNOWN is
retained: its base oracle did not recognize this serialization. The later
structural/source analysis is a separate warrant, not a rewritten PASS.

[ROLE_PIN_0.160.0.md](ROLE_PIN_0.160.0.md) retains exact report, comparison and
review identities, source paths, custody and receiving limits. The generic
field contract does not narrow permitted other-role/no-role composition, but
this sample proves no other/no-role native supply. Rust Host/store/seeding joins,
other primary roles, TASK-child supply, lifetime/resume/fork, child carrier,
provider/model adoption, delegation availability/enforcement and qualification
still require their own candidate evidence. Native child supply stays
**not-supplied** until its actual carrier/custody/configuration evidence exists;
0.158.0 adapter observations below remain historical. Runtime capability values
are read from the actual acting route, never inferred from0.160.0 or this sample.

## 3. Selection

### 3.1 Rules

- **SL-1 Four roles; three conversation roles.** HELP_HUMAN, HELPS_HUMANS,
  WORKING_ITEMS and TASK with their WD §5.1 meanings, from the bundled role
  set (§4.1). Both schemas enumerate the four. A conversation is started
  with HELP_HUMAN, HELPS_HUMANS or WORKING_ITEMS, or with no role (SL-2).
  TASK is not a conversation role: it is the role a manager assigns bounded
  work to, and its guidance is supplied for that delegation (§5.3; owner
  ruling 2026-10-10: "That scope is wrong. TASK is not a conversational
  role. Fix the scope of work as recommended."). The start display does not
  list TASK as a choice; a TASK start that reaches composition anyway is
  refused before anything is sent (`refused-before-send`).
- **SL-2 No role.** A conversation may have no role (R17-9); it is supplied
  the product guidance alone, shown as "No role", never as a fifth role.
- **SL-3 Preselection.** A new conversation preselects the role whose
  `default_for_new_chat` is true in the bundled role set, as data (R17-9;
  PROPOSED), shown in DEL-01-04's start display (C-15) as a preselection the
  person can change or clear. Root's current value (HELP_HUMAN) is evidence;
  the shipped value is a release decision.
- **SL-4 Not a reserved act.** Choosing a role grants nothing and is not one of
  ACT-v0.8's acts; an agent cannot select or change a conversation's role.
- **SL-5 Domain expressions** stay within one of the four roles (V4-ROLE-03;
  schema IS-7).
- **SL-6 Model independence.** With no model chosen (K-3) nothing starts; the
  conversation reads "not started — no model selected" (R18-2).
- **SL-7 Compatible roles.** When a run starts in a conversation, its role (or
  "no role") is handed to DEL-02-03's check as a runtime value. A role outside
  the workflow's compatible roles (WD §4.7) is shown before the run starts and
  recorded; the person may proceed. A workflow requiring `agent-delegation`
  with TASK in force is *unsupported* by WD §4.7. Runs chained in one
  conversation (R19-2) are each checked against the same fixed role
  (INTEGRATION; EXEC owns the reading; U-R10).
- **SL-8 Fixed for life (L-2).** The role chosen when the conversation starts
  stays for the conversation's life. Selecting a role is possible only before
  the first message; afterwards the selector shows the role and offers
  "Continue as ‹role›" (§3.3).

### 3.2 Conversation states (T-2; PROPOSED)

An App-kept pointer per conversation (R17-4). Prototype: `role_supply.T2`,
cases RC-01, RC-07, RC-15…RC-17, RC-19.

| State | Event | Next | Effect and record |
|---|---|---|---|
| draft (role = preselection, a choice, or none) | person selects / clears | draft | `preselected` false |
| draft | person sends first message (model chosen) | starting | compose (§5.1); `thread/start`; supply record `thread-start` |
| starting | response | supplied | outcome `supplied`; thread identity; `instructionSources` |
| starting | composition refused | supply-refused | `refused-before-send` with reason; message kept unsent |
| starting | error | not-started | `request-failed`; the person may retry |
| starting | no response | start-unknown | `unknown-no-response`; settled by reading the thread at the next ready generation: present → supplied (this record stays unknown), absent → not-started |
| starting | person sends again | — (refused) | one start in flight (RC-19) |
| supply-refused, not-started | person fixes (restore, reselect) | draft / not-started | — |
| supplied | person sends | supplied | ordinary turn; no supply. A workflow run may start, end or follow another here (R19-2); none changes the role or the supply |
| supplied | person selects a role | — (refused) | L-2; the App offers "Continue as ‹role›" instead (§3.3) |
| supplied | guidance store change affecting this role | supplied | flag "guidance changed since this conversation started" (§4.4); nothing sent |
| supplied | App relaunch | supplied | `thread/resume` with the thread id only; no supply record (§5.5) |
| supplied | person forks | supplied (source); new conversation *supplied* | §3.3 F-1 |

### 3.3 Another role, and forks (R19-3, R19-8)

- **CA-1 "Continue as ‹role›".** From a started conversation the person may
  choose "Continue as ‹role›" (HELP_HUMAN, HELPS_HUMANS or WORKING_ITEMS, or
  no role; not TASK, SL-1). The App opens a
  **new** conversation in *draft* with that role and pre-fills its first
  message with a **handoff summary**, which the person sees and can edit; it
  is not sent until the person sends it. The source conversation is unchanged.
- **CA-2 The summary (R20-6).** The App asks the source conversation's agent,
  in a **visible turn of the source conversation**, to draft a handoff
  summary. The draft is placed, unsent, as the new conversation's first
  message, under an App-written header naming the source conversation; the
  person edits it there. The summary carries no instructions beyond the
  person's own text, and nothing is sent until the person sends it. It is
  not supplied guidance: the new conversation's guidance is its role's
  composition (§5.1).
- **CA-3 Record.** The new conversation's start record carries
  `continuedFrom` {source thread, source start record}: a relation, not a
  copy. No history is carried: at 0.158.0 a fork cannot take another role's
  guidance (B-16), and Root doctrine says a full-history fork alone does not
  establish a different role.
- **F-1 Fork.** "Fork" stays available as a **same-role copy**: `thread/fork`
  with the thread id and no instructions. The fork keeps the source's role and
  guidance (B-16) and is recorded with trigger `fork`, outcome `inherited`,
  `inheritedFrom` = the source's start record, and the reported
  `forkedFromId` (RC-06). Because the fork's rollout references the source's,
  whether deleting or archiving the source breaks the fork is open (OBS-3
  UNRESOLVED; U-R13).

## 4. Where the guidance comes from (K-9 as amended by L-2)

### 4.1 The role set (bundled, read-only)

The App release contains a role set `roles.json`: per role its name, meaning
(WD §5.1), guidance file path, delegation statement (`may-delegate` or
`does-not-delegate`), the child roles it offers (§5.3; Root's `delegates_to`
read as data: HELP_HUMAN offers HELPS_HUMANS, WORKING_ITEMS, TASK; the two
managers offer TASK; TASK none) and `default_for_new_chat`. It is not
editable: the four roles are fixed (REQ-001). A role set that does not name
exactly the four roles, or marks more than one default, refuses every start
(`role-set-invalid`). Its content identity is recorded with each start.
(v0.2: "start" for v0.1's "supply"; since L-2 a conversation is supplied
only at its start.)

### 4.2 The guidance store

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
- **GS-4 Read once, at a conversation start.** Guidance is read when a
  conversation's start supply is composed (§5.1), each file once, and the
  same bytes are hashed and composed (no gap between identity and content).
  (v0.2: v0.1 read "at a supply point", which included the idle-point
  change of §5.4, withdrawn by L-2.)
- **GS-5 No silent fallback.** A missing, unreadable, symbolic-link or
  non-UTF-8 file refuses the start (v0.2: "start" for "supply") with its
  reason (RC-08, RC-09); the App never substitutes the shipped default
  without the person's restore.
- **GS-6 New release.** For each file: if the copy still equals the default
  that was seeded, it takes the new default (`release-default-applied`); if
  the person modified it, it is kept and flagged "a new default is available"
  with compare and restore (RC-18). The change reaches **new conversations
  only**; open conversations are flagged (§4.4) (v0.2, L-2; v0.1 said "at
  their next idle point"). PROPOSED; U-R9.

- **GS-7 Proposal and finished lines (R20-5; R20-9, added at RX).** The
  shipped product guidance tells the agent two exact lines, each alone on
  its own line and naming the workflow by origin and name: when it proposes
  a next workflow, `Next workflow: ‹origin›:‹name›` naming one registered
  workflow; when it judges the workflow of the run in force finished,
  `Workflow finished: ‹origin›:‹name›` naming that workflow (R20-1). The
  guidance also states their placement (R20-11 (2)): the proposal line is
  the message's last line; the finished line is the last line, or comes
  just before the proposal line when both are written; each at most once.
  The App reads only these exact forms in these places, never prose (EXEC
  RC-5). DEL-01-04 (NIR §5.7) offers "Start ‹workflow› (proposed by the
  agent)" on the first when no run is in force, and only "End ‹A› and start
  ‹B›" during a run (R20-11 (1)); "End run" on the second (with "End ‹A›
  and start ‹B›" when both come in one message); nothing starts or ends until the person confirms
  (R19-2 (b), R20-1), and the person's choice on a finished report ends the
  run with cause `completed`. The run-start text repeats both lines for the
  run in force (WR-v0.2 §16.2, framing WR-FRAME-1); in a conversation with
  no run in force the finished line has no use. The sentences are content
  of the shipped `AGENTS.md`; if the person edits the copy (GS-2) and
  removes them, the lines may no longer arrive in these forms, which the
  App does not check (the lines are guidance, not enforcement).

**T-1 Guidance file states (PROPOSED).** v0.1's table, changed where marked
"(v0.2)": the last two rows' effect (new conversations only; open ones
flagged, §4.4), the restore row (no supply-record cause) and the missing row
("starts" for "supplies").

| State | Event | Next | Effect |
|---|---|---|---|
| not seeded | first start | default | exclusive create; seed record |
| default | person edits | modified | detected at the next read or display |
| modified | restore default | default | `guidance-restored` (the store's result; v0.2: no longer a supply-record change cause, `changeCause` having left the schema with the idle point) |
| default, modified | file removed | missing | starts needing it refused (`guidance-file-missing`) (v0.2: "starts" for "supplies") |
| any | unreadable, link, not UTF-8 | unreadable | refused with the reason |
| missing, unreadable | restore default | default | — |
| default | release with a new default | default (new bytes) | `release-default-applied`; reaches new conversations; open ones are flagged (§4.4) (v0.2) |
| modified | release with a new default | modified, new default available | shown; kept. The copy is unchanged, so nothing reaches any conversation until the person restores or edits it; that change then reaches new conversations and open ones are flagged (§4.4) (v0.2) |

A change of state is not itself sent anywhere. It reaches new conversations
only, and an open conversation is flagged (§4.4) (v0.2; v0.1: "only through
§5.4", the idle point, withdrawn by L-2).

### 4.3 The harness's own instructions (R18-6)

Codex's base instructions and the instruction files Codex discovers natively
are the harness's own; the App neither composes, removes nor deduplicates
them. Under K-1 the App home links the person's `config.toml`; by the same
link it shows the person's **global `AGENTS.md` and skills**, so Codex's
native discovery in the App matches the person's Codex (R18-6, PROPOSED;
DEL-01-05 states the linking). `instructionSources` is recorded as reported
with each start and fork (B-6). A project conversation in this repository, for
example, also loads Root `AGENTS.md` natively; that is recorded, not
App-supplied. Codex lists every discovered skill to the model (OBS-3 §9); the
App places no workflow in a skill root (R19-7).

### 4.4 Guidance changed since a conversation started

- **GC-1** When an open conversation is shown, the App compares each part of
  its start record with the store's current file for the same path. If any
  differs (edited, restored, new release, missing), the conversation shows
  "Guidance changed since this conversation started", naming the file, with
  "Continue as ‹same role›" to take it up in a new conversation (RC-16).
- **GC-2** Nothing is sent to the open conversation; its record is unchanged.

## 5. Supply

### 5.1 Composition (format `chirality.role.compose/0.2`; PROPOSED)

At conversation start the supplied text is the UTF-8 concatenation of:

1. the product guidance bytes (`AGENTS.md` of the copy);
2. if a role is chosen: `\n\n# Active role: <ROLE>\n\n` then the role file bytes.

Rules:

- **CO-1 Parts are byte ranges.** Each part's offset, length and content
  identity are recorded; the separators belong to no part. A reader recomputes
  each part from the supplied text (RC-03; `verify_composition`).
- **CO-2 No normalization.** Bytes as stored (WD RV-3). Non-UTF-8 is refused.
- **CO-3, CO-4 Withdrawn** (workflow part; R19-7): a run's workflow is a text
  element of its run-start turn, composed by DEL-02-02 and recorded per run
  there (RS R3's workflow source), and the model may also see Codex's skill
  list, never a workflow placed there by the App.
- **CO-5 One carrier.** The whole composition goes in `developerInstructions`
  on `thread/start` (v0.2: start only, §5.2); nothing goes in
  `baseInstructions` or in the `config` keys `instructions` or
  `developer_instructions` (§5.2).
- **CO-6 Size.** No supplier limit is stated in the generated types; the byte
  length is recorded. No App limit is chosen (U-R4).

### 5.2 Inputs the role supply uses and never uses (current0.160.0; historical warrants retained)

| Supplier input | Role supply | Why |
|---|---|---|
| `developerInstructions` on `thread/start` | **Carries the composition** | B-2; current generic0.160.0 field and independently reviewed primary HELP_HUMAN sample §2.1 |
| `developerInstructions` on `thread/resume` | Never | Ignored (B-8); sending it would create a "supplied" record the App knows is not taken up |
| `developerInstructions` / `config.developer_instructions` on `thread/fork` | Never | Ignored (B-16) |
| `baseInstructions` | Never | Preserves Codex's base instructions |
| `config` keys `instructions`, `developer_instructions` | Never | One carrier |
| `config` keys `agents.<ROLE>.description`, `agents.<ROLE>.config_file` on `thread/start` | Candidate additive child carrier only; currently not-supplied (§5.3) | R17-9, R18-4; current carrier evidence remains open |
| `config` keys `features.*`, `agents.enabled`, `agents.max_depth`, any other | Never | K-10; no veto of user configuration |
| `personality`, `multiAgentMode`, effort chosen to steer delegation | Never | Deprecated / ignored (B-9); K-10 |
| `approvalPolicy`, `approvalsReviewer`, `sandbox` | Never by role supply | D3 |
| `turn/start` `collaborationMode.settings.developer_instructions`; `thread/settings/update` | Never by role supply | Added or persisting text (B-4); plan mode is DEL-01-03's and DEL-01-04's (C-06); not used for workflows (R19-7) |

The request check refuses a role request with any "never" input, and any
instructions on resume or fork (RC-07, RC-11; schema IS-1, IS-6, IS-9).

### 5.3 Native child roles (R17-9 as amended by R18-4)

**Current0.160.0 receiving standing:** the primary sample §2.1 does not establish
the child carrier. The requirements and historical0.158.0 adapter mechanism
below remain; current native children/config files are not reported supplied
from field existence or primary-role carriage. User-defined role names and the
person's native configuration remain untouched. U-R3 stays open.

- **CR-1** A conversation whose role offers child roles (§4.1) is started with
  additive `agents.<CHILD>.description` and `agents.<CHILD>.config_file`. The
  file, written into the App's data folder, named by its content identity,
  created exclusively and verified on reuse, holds `developer_instructions` =
  **product guidance + `# Active role: <CHILD>` + the child's role file**.
  Because that text **replaces** the parent's for the child (B-15), the
  product guidance must be in it (RC-12).
- **CR-1a Carrier (open).** The mechanism is observed with the keys in the
  home's `config.toml`. Under K-1 that file is the person's (linked) and the
  App never writes it. The App's candidate carriers are the per-thread
  `config` map on `thread/start` (PROPOSED; not observed) and, failing that,
  `-c` session flags at process start (the `sessionFlags` layer is observed
  for `-c` in general, OBS-2 O-6 M2; not for `agents.*`). With session flags
  the roles would be offered in every conversation of that process, TASK and
  no-role included (no enforcement either way). U-R3.
- **CR-2 Additive only.** The App reads the effective configuration
  (`config/read`) and supplies no child role whose name the person's
  configuration defines; if it cannot read it, none
  (`user-configuration-not-read`). It enables, disables and limits nothing.
- **CR-3** TASK offers no child roles. That is not enforcement (K-10).
- **CR-4 A child without a role type.** A child spawned with a built-in type
  (`default`, `explorer`, `worker`) or none has **unknown** guidance: not
  observed, never stated as inherited (R18-4). Its delegation is never
  attributed a role (RC-14).
- **CR-5 Finding children.** No `thread/started` arrives for a child (B-11).
  The App learns a child from a **completed** `spawnAgent` item's
  `receiverThreadIds` (the started item's list is empty) and reads it with
  `thread/read` for `agentRole` and `parentThreadId`. A child's role counts
  only when `agentRole` names a child role the App supplied to that
  conversation; listing children after a relaunch uses `thread/loaded/list`
  or the App's own record, never `thread/list` (B-11).
- **CR-6 Local models.** On a provider that drops `namespace` tools (LM Studio
  0.4.16) delegation never reaches the model (B-9): no child exists, and the
  delegation view is absent (K-5).

### 5.4 Withdrawn

v0.1's idle-point change (IP-1…IP-6, routes A and B) is withdrawn by L-2 and
R19-3; B-8 confirms route A would not have worked at 0.158.0.

### 5.5 Resume after relaunch

After a relaunch a thread is `notLoaded`. Before its next turn the App sends
`thread/resume` with the thread id only. The conversation keeps the guidance
it started with (B-8: the original developer text stays in force in a new
process, observed). No supply record is written; if the store changed, §4.4
flags it.

### 5.6 Operating sequences with failure behaviour

**SQ-1 New conversation.**

| Step | What happens | Fails when | Then |
|---|---|---|---|
| 1 | Role preselected; person keeps, changes or clears it | Role set invalid | `role-set-invalid`; release defect shown |
| 2 | Person chooses a model and writes a first message | No model (K-3) | "not started — no model selected" |
| 3 | Compose (§5.1) | Missing / unreadable / non-UTF-8 file | `refused-before-send`; message kept unsent |
| 4 | Child-role keys (§5.3) | `config/read` fails | None supplied; start continues |
| 5 | Request check (§5.2) | Forbidden input | `forbidden-input-in-request`; nothing sent (a design defect) |
| 6 | `thread/start` (HOSTING §5.1) | Not ready; error; no response | `request-failed` / `unknown-no-response`; T-2 |
| 7 | Response; record written; HOSTING §8.2 records the carried identity | Identities differ | Finding "supply evidence mismatch" (VC-R12) |

**SQ-2 Continue as ‹role›.** CA-1…CA-3, then SQ-1 for the new conversation.
Fails as SQ-1; the source is untouched.

**SQ-3 Relaunch.** §5.5. Fails as HOSTING §4 and DEL-01-02's recovery.

**SQ-4 Delegated child.** A completed `spawnAgent` names the child (CR-5);
`thread/read` gives its role. Fails when the item is not observed → the
child's role is *unknown* for that span; when `thread/read` fails → role
*unknown*.

**SQ-5 A task agent delegates.** §6.3.

**SQ-6 Guidance edited while conversations are open.** §4.4; new
conversations take it up.

**SQ-7 New release.** GS-6; §4.4.

**SQ-8 Fork.** F-1. Fails as `thread/fork`'s request; outcome recorded.

## 6. Evidence handed to receivers

### 6.1 The supply record (`role-supply-record.schema.json` 0.2; PROPOSED)

One record per conversation start (`thread/start`, including refused starts)
and per same-role fork (`thread/fork`, outcome `inherited`, with
`inheritedFrom`). It carries the trigger; the request identity and
generation; the selection (role or none, preselected, role-set identity);
for a start, the composed identity and length, each part (product guidance,
role) with its source (copy path, release, default/modified, shipped default's
identity) and byte range, `baseInstructions: not-set` and the child-role
entries; `continuedFrom` for "Continue as"; what the supplier reported
(`instructionSources`, `agentRole`, `forkedFromId`); the outcome; and
`adoption: unknown`.

- It is the source identity of HOSTING §8.2 for role guidance; the composed
  identity must equal HOSTING's carried identity (VC-R12).
- It is the proposed body of RS R3 `supplied_guidance` for **role guidance**
  (join J-11). The workflow source of R3 is DEL-02-02's per-run record
  (R19-7), not this one.
- DEL-02-04 keeps its own App-kept log of these records (C-19; RS §13.1 S-A
  form); App-observed, never authority for what Codex holds (R17-4).
- **CC-CONTENT-IDENTITY:** App role-set/source-file/shipped-default,
  composed guidance, and child-role file bytes use
  `chirality.app.exact-bytes.sha256/v1`: lowercase 64-hex SHA-256 over their
  exact bytes. No line-ending, UTF-8, whitespace or JSON normalization and no
  bytes excluded. Stored source bytes remain source bytes; composition is
  hashed separately after CO-1…CO-5 framing and UTF-8 encoding, and that exact
  composition is carried to HOSTING. Hashing a parsed/rewritten role-set JSON
  or a workflow package digest is a different method, never substituted.
  Each part keeps its source/byte ranges; identity equality establishes
  byte equality, not supplier/model adoption or human acceptance. Historical
  `proto-sha256-0` records retain their old designation and are not silently
  comparable. Method/value travels into RS R3 and HOSTING §8.2 unchanged;
  unknown and inherited supply still follow their existing outcomes. Broader
  HOSTING U-08 and host-native identities remain unselected.

Valid: `role-supply-record.valid.example.json` (a WORKING_ITEMS start that
supplies TASK as a child role). Invalid: `role-supply-record.invalid.examples.json`
IS-1…IS-9 (IS-8: a workflow part; IS-9: role guidance on `thread/resume`).

### 6.2 The limit account (`role-limit-account.schema.json` 0.2; PROPOSED)

| Limit | Role | Standing (default guidance) | Shown as | Not reported as enforcement |
|---|---|---|---|---|
| L-TASK-1 A task agent does not delegate | TASK | `stated-not-enforced` (K-10; no supplier control at 0.158.0, B-9; B-18 shows the limit not kept) | "Stated, not enforced" | approval policy, sandbox, the person's configuration, **the depth limit** |
| L-ALL-1 Work within the brief's write targets | all four | `stated-not-enforced` | "Stated, not enforced" | brief text, worktree, sandbox, approval policy |

- **LA-1** `enforced-by-supplier` needs a named mechanism; none at 0.158.0.
- **LA-2** A modified role copy makes that role's limits `unknown` (RC-10; IL-2).
- **LA-3** The other roles keep native delegation as the person's
  configuration allows (C-04 availability, B-9); the App adds no limit.
- **LA-4** Shown where a role is chosen and in DEL-01-03's delegation view,
  carried there as handed, all three values (C-08).
- **LA-5 Depth.** A child at the default depth gets no delegation tools
  (B-17). That is the person's configured depth, applying to every child
  whatever its role; it is listed under "not enforcement" and never shown as
  enforcing L-TASK-1.

### 6.3 Limit observations: a task agent delegates (K-10)

- **DL-1 Trigger.** A `collabAgentToolCall` `spawnAgent` whose sender has TASK
  in force: supplied to it at start (`supplied-to-thread`), or a child whose
  `agentRole` is TASK and was supplied by the App
  (`native-child-role-reported`). No other basis exists; a child without a
  role type is never attributed TASK (IL-6).
- **DL-2** One observation per item id (started and completed collapse).
- **DL-3** Nothing is prevented, declined, interrupted or answered (B-18
  observed it proceeds in full).
- **DL-4** Shown in the conversation; handed to DEL-01-03 as a runtime value
  (C-07); written to the run record when a run is in progress (RS R3 limits;
  J-11).
- **DL-5** Delegation by a role that may delegate is not an observation; a
  task agent's later `sendInput`/`wait` to its child belongs to the same
  delegation.
- **DL-6** Items are delivered (B-10, through an adapter). On a provider that
  drops `namespace` tools there is no delegation to observe (CR-6).

### 6.4 The five facts kept apart (CLM-004, AC-005)

| Fact | Evidence in this design | Who records | Standing |
|---|---|---|---|
| Selection | T-2 state; supply record `selection` | App (the person's choice) | App-observed |
| Source resolution | Each part's source and content identity | App composition | App-observed |
| Supply | Supply record `outcome: supplied`, matched with HOSTING §8.2's carried identity (a same-role fork: `inherited`, §6.1; v0.2) | App; DEL-01-01 boundary tap | observed at the boundary |
| Provider adoption | None; `adoption: unknown` in every record | — | unknown (P-15); `instructionSources` shows discovered files only |
| Observed behaviour | Codex history read back (R17-4); limit observations | Codex; App observation | per item |
| Consumer adoption | Not here. DEL-11-02 records the adopting consumer's actor and scope | DEL-11-02; the consumer owner | never inferred from supply or publication |

One observed instance (v0.2): B-8 is a case where an input was carried and
accepted and not taken up, which is why the App sends no instructions on
resume or fork and records adoption as `unknown` always.

## 7. Interfaces

### 7.1 Consumed

| ID | Supplier and contribution | Row (DAG-003) | Condition | When it fails |
|---|---|---|---|---|
| C-1 | DEL-01-01: carriage of `developerInstructions` on `thread/start` (S-6) and §8.2 evidence; `thread/fork` and `thread/resume` without instructions | DEP-02-04-010 (admitted) | `ready(g)` | `request-failed` / `unknown-no-response` (T-2) |
| C-2 | DEL-01-01: thread status and §6 register, for "start in flight" and relaunch | DEP-02-04-010 | — | Status unknown → no new start until settled |
| C-3 | DEL-01-01: completed `collabAgentToolCall` items and `thread/read` of children (**no `thread/started` for a child**, B-11) | DEP-02-04-010 (statement widening proposed, ST-4) | Observation not lost | Child role and limit observation *unknown* for the span |
| C-4 | DEL-01-01: `config/read`, read only | DEP-02-04-010 | — | No child roles |
| C-5 | DEL-02-01: role meanings, compatible roles | DEP-02-04-011 (held) | — | — |
| C-7 | DEL-01-05: a chosen model (K-3); the App home's links (R18-6) | none (runtime) | — | Not started (SL-6) |

C-6 (DEL-02-02's registered revision) is withdrawn (R19-7).

### 7.2 Offered

| ID | Receiver | Row | Form |
|---|---|---|---|
| O-1 | DEL-01-01: source identity for §8.2 | DEP-02-04-010 (mirror R-11-1 pending) | Supply record |
| O-2 | DEL-04-03: supply records, limit account, observations | DEP-02-04-012 (held) | Two schemas; J-11 |
| O-3 | DEL-11-02: the same evidence, no adoption claim | DEP-02-04-013 | As O-2 |
| O-4 | DEL-03-04: semantics for row 8 | DEP-03-04-010 | §3–§6 |
| O-5 | DEL-10-03: supply obligations | DEP-10-03-010 | §3–§6 |
| O-6 | DEL-01-03: role per thread (children per CR-5) and the L-TASK-1 standing, carried as handed (C-07, C-08) | none (runtime) | §6.2, §6.3 |
| O-7 | DEL-02-03: the conversation's fixed role for each run's check | none (runtime) | SL-7 |
| O-8 | DEL-01-04: the role list with its preselection (`default_for_new_chat`), the fixed-role display with "Continue as", and the "guidance changed since this conversation started" notice (C-15; NIR-v0.2 §2 IF-15, §5.4 ST-5, ST-6, §5.8) | **D3 NR-4** (DEL-01-04 consumes DEL-02-04; proposed by D3 R2.5 and NIR IF-15), adopted by R22-1 as a held arc inside SCC-002 with no SCC change; proposed, not yet in a register (§7.3) | §3, §4.1, §4.4 |

### 7.3 Register rows (R17-10)

- **Dropped:** the v0.1 proposal DEL-02-04 → DEL-02-02 (F0 NR-10), by R19-7.
- No row toward DEL-01-03 (C-07: D2's DEL-02-04 → DEL-01-03 is dropped; a
  row DEL-01-03 → DEL-02-04 would pull DEL-01-03 into SCC-002).
- Still proposed: the mirror R-11-1 (M-6); the DEP-02-04-010 statement
  widening (ST-4), now naming child discovery by item and `thread/read`.
- **Adopted (R22-1; added at node G):** D3 NR-4, DEL-01-04 UPSTREAM
  INTERFACE → DEL-02-04 (the role list, its preselection and the "guidance
  changed" notice; O-8). Both deliverables are already in SCC-002, so the arc
  is held and leaves SCC-002's membership unchanged. It is a proposal for
  SCA-V4-003 (DEL-01-04's register), not yet a register row; the DEL-02-04
  mirror is C1-B's R3-02-04-c. v0.2 had O-8 as a runtime value with no row;
  R22-1 replaces that.

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
| `product-native-role-config.ts` | Per role, writes a TOML file `developer_instructions = common + "# Active role: ROLE" + role`, named by sha256, exclusive create, verified on reuse; returns `agents.<ROLE>.description/config_file` | **Approach reused** for CR-1 (same composition order and file discipline). Must meet CR-2 (additive, user-defined names kept) and the 0.158.0 mechanism (B-15, observed through an adapter) and carrier (CR-1a, open) (v0.2; v0.1: "the 0.158.0 mechanism check") |
| `native-role-config.ts` | Pins `agents.enabled=true`, `features.multi_agent=true`, `features.multi_agent_v2=false`, `agents.max_depth=2`; digest over pins and role bytes | **Not reused**: these override the person's configuration (K-10; Root AGENTS.md). The digest idea is covered by the supply record |
| `product-instructions.ts` | Seeds the default `AGENTS.md` into user data `instructions/`, exclusive create, "modified" flag, restore default | **Approach reused** for GS-1…GS-3, extended to the role files and GS-6 |
| v3 turn envelope `requestedRole` incl. "untyped"; ≤ 1 MiB `developerInstructions` | Untyped requests; a size bound | No-role allowed (SL-2); no size bound chosen (U-R4) |
| v3 Runtime service | Hosting topology | Excluded (V4-ARC-03) |

Any reused code is qualified only by candidate evidence against §11; its
history and earlier tests qualify nothing (REQ-005). No common service,
precedence tree or extra UI follows: the selector, the store state with
restore, and the limit labels are the UI this file needs.

One confirmation (v0.2): v3's role-file approach (`product-native-role-config.ts`:
common guidance + "# Active role" + role in each file) matches what B-15 now
requires, since the role file replaces the parent's text. v3's pins of
`features.*` and `agents.max_depth` stay not reused. v3 produced the role keys as
`key=value` override strings (`codexNativeRoleConfigOverrides`), which reads as
`-c` overrides at process start (inference from the code); for v4 that is
CR-1a's fallback carrier, unobserved at 0.158.0.

## 10. Prototype (R17-1)

`Design/prototype/` rewritten for v0.2 (README there). Python 3 standard
library; invented fixtures; a supplier double that ignores instructions on
resume and fork as observed (B-8, B-16). The v0.1 workflow fixture is removed.

Run 2026-10-02 from `Design/prototype/`: `python3 run_cases.py --write-examples --record`,
then `python3 run_cases.py --record` (Python 3.13.7); output in
`prototype/results/run-2026-10-02.txt`: **36 pass, 0 fail**. RC-01…RC-19
(selection; seeding; role-only composition per role; no role; no workflow
part; fork inherited; relaunch without instructions; refusals; modified TASK
guidance; forbidden inputs including instructions on resume or fork; child
roles with product guidance in each file; limit account; children from
completed receivers with a TASK child observed and a `default` child not
attributed; fixed role and "Continue as"; guidance changed since start;
no response; release upgrade; one start in flight) and RC-20 (both valid
examples accepted; IS-1…IS-9 and IL-1…IL-6 each rejected for its reason).
`run-2026-10-01.txt` is v0.1's run, kept.

## 11. Verification (designed; nothing qualified)

| Case | SoW | What is exercised | Needs | Now |
|---|---|---|---|---|
| VC-R1 | VER-001 | Each role; supplied role part; no role; domain expression | Candidate UI | RC-01, RC-03, RC-04 |
| VC-R2 | VER-002 | Each role's start at the boundary vs the record; base instructions intact | Codex, chosen route, candidate | Historical B-7; current0.160.0 HELP_HUMAN capture/source comparison §2.1 observed. Connected App and other/no-role cases remain open; no prediction/adoption |
| VC-R3 | VER-003 | TASK asked to delegate; observation; other roles' delegation | Codex with delegation | B-18 observed through an adapter; on stock LM Studio not provokable (CR-6); RC-14 |
| VC-R4 | VER-004 | Presented account vs actual controls, incl. depth not shown as enforcement | Candidate UI | RC-13, IL-1 |
| VC-R5 | VER-005 | Trace; supply-only makes no adoption claim; positive consumer adoption | DEP-006 / OI-024 | Negative offline (IS-4); positive AWAITING INPUT |
| VC-R6 | VER-006 | Reuse review | A reviewer | Designed |
| VC-R7 | L-2 | Role fixed; "Continue as" with editable summary | Candidate UI | RC-15 |
| VC-R8 | L-2 | Relaunch keeps the start supply; no instructions on resume | Live | B-8 observed; RC-07 |
| VC-R9 | K-9 | Seed, restore, upgrade, guidance-changed flag | Fixture | RC-02, RC-08, RC-16, RC-18 |
| VC-R10 | REQ-002 | Refusals | Fixture | RC-08, RC-09, RC-11 |
| VC-R11 | REQ-003 | Child roles additive, product guidance in each file; the carrier at the pin | Live for CR-1a | RC-12; mechanism observed through an adapter; carrier open |
| VC-R12 | REQ-004 | Record identity = HOSTING §8.2 carried identity | Candidate with tap | Designed |
| VC-R13 | R19-8 | Fork keeps role; recorded inherited | Live | B-16 observed; RC-06 |

## 12. The v0.1 "OBS-2 pending" cells

This table preserves its historical0.158.0 observations. Current §2.1 separately
supplies a nonempty instructionSources sample and HELP_HUMAN carrier/base
comparison at0.160.0; it does not rewrite the old cells or supply their wider
candidate, child or lifetime obligations.

| Cell | Result | Standing |
|---|---|---|
| B-8; IP-4; VC-R7 | Resume ignores new instructions → route A impossible; L-2 removes the need | observed (O-5); cell closed |
| §5.5; VC-R8 | Relaunch keeps the original supply | observed (O-5 (b)); closed |
| B-15; CR-1/CR-4; VC-R11 | Native child roles honoured; role text replaces the parent's | observed through an adapter (O-4a); mechanism closed; **carrier open** (CR-1a, U-R3) |
| DL-6; VC-R3 | Items delivered; TASK-guided delegation recorded | observed through an adapter (O-4, O-4b); closed with that note |
| B-6 | Only `[]` seen | **open** (no project `AGENTS.md` in any observation) |
| VC-R2 | Developer text in every model request, one role | observed (O-5 tap); per-role open |

## 13. Findings

F-R1…F-R8 are v0.1's, written against the first-increment files v0.1 read
(HOSTING-v0.8, RS-v0.8); the joins they name went to node F. v0.2's
amendments are marked "(v0.2)".

- **F-R1 Guidance carriers beyond start and resume.** At 0.158.0
  `thread/fork` also carries `baseInstructions`/`developerInstructions`, the
  experimental `turn/start` carries `collaborationMode.settings.developer_instructions`,
  and the thread `config` map accepts `instructions`, `developer_instructions`
  and (untyped) agent-role keys (B-3…B-5). HOSTING-v0.8 S-6 and §8.2 named
  start and resume only (join J-1, J-2). (v0.2) `thread/resume` and
  `thread/fork` accept their instruction inputs and ignore them (B-8, B-16).
- **F-R2 HCG-A08's availability signal is deprecated.** HOSTING-v0.8 §8.4
  listed `multiAgentMode` as the signal; the generated TS marks it
  "@deprecated Ignored". `Model.multiAgentVersion` (`disabled`, `v1`, `v2`) is
  a per-model signal (join J-3).
- **F-R3 Child role facts exist.** `Thread.parentThreadId`, `Thread.agentRole`
  and `SubAgentSource.thread_spawn.agent_role` (B-11) let the App record a
  child's role (join J-4). (v0.2) Observed through an adapter (OBS-2), not
  stock behaviour; no `thread/started` arrives for a child (CR-5).
- **F-R4 RS R3 is one source string and one identity** (RS-v0.8). It cannot
  hold the parts, the selection or the limit observations (join J-11).
- **F-R5 Native discovery inside this repository.** A project conversation on
  this repository would natively load Root `AGENTS.md`; it is the harness's
  own and is recorded, not deduplicated (§4.3).
- **F-R6 The SoW lags** (header reading; SCA-V4-003 proposals in the return).
- **F-R7 Idle is reported.** `ThreadStatus` gives `idle` and `active` with
  flags (B-12), so the App's status reading rests on supplier notifications
  plus the register (C-2). (v0.2) v0.1 used it for the idle point (IP-1),
  which is withdrawn (§5.4); it now serves "one start in flight" and
  relaunch.
- **F-R8 No typed `agents` configuration at 0.158.0.** Native agent-role
  configuration is not in the generated types. (v0.2) The mechanism is
  observed through an adapter (B-15, OBS-2 O-4a); the per-thread carrier is
  not (CR-1a, U-R3). v0.1 read B-15 as an inference from v3.
- **F-R9 Root doctrine and L-2.** Root `AGENTS.md` says "Instruction changes
  take effect at a verified idle boundary". Under L-2 and B-8 the App applies
  role-guidance changes to new conversations only. This file records the
  difference for an instruction-change notice; it changes no instruction.
- **F-R10 Supplied but ignored.** B-8 and B-16 are inputs the supplier accepts
  without error and does not apply, with nothing reporting it; the App does
  not send them rather than record them as supplied.
- **F-R11 Fork dependence.** A fork's rollout references its source's (B-16);
  a same-role fork may depend on the source's survival (open, U-R13).

## 14. UNRESOLVED

| Item | Owner | Point of need | Effect |
|---|---|---|---|
| U-R1 App role content-identity method (HOSTING broader U-08 remains open) | CC-CONTENT-IDENTITY technical selection; App/RS consumer owners | Independent review and product propagation before qualification records | Exact-byte method selected in §6.1; historical records retain their designation; host identities untouched |
| U-R2 *Closed* (route A/B): L-2, B-8 | — | — | — |
| U-R3 Current0.160.0 child-role carrier (per-thread `config` or `-c` session flags; CR-1a; historical0.158.0 adapter mechanism retained) | App implementation owner; a later observation | Before native child supply | Carrier open; currently not-supplied; primary sample is not child evidence |
| U-R4 Composition size bound | App implementation owner | Before implementation | Length recorded |
| U-R5 `UNRESOLVED{OI-008}` placement | App implementation owner | Before architecture contracts | §8 PROPOSED |
| U-R6 `UNRESOLVED{OI-014}` role identity set placement | App/shared contract owners | Before allocation | Role set is the App's own |
| U-R7 Host seat mapping; host distribution | DEL-02-01 with SWB owner | Deferred (DECISION-3) | Not designed |
| U-R8 Consumer adoption evidence (OI-024; DEP-006) | Owner with consumers | Before adoption | VC-R5 positive waits |
| U-R9 Unmodified copies taking new defaults automatically (GS-6) | App role-guidance owner (owner may prefer asking) | Before implementation | PROPOSED |
| U-R10 Compatible-roles mismatch display | Integrator with DEL-02-03 | Before the check's display | PROPOSED |
| U-R11 Shipped `default_for_new_chat` value | App role-guidance owner | Before release | Data |
| U-R12 *Closed by R20-6*: the source conversation's agent drafts it in a visible turn; the person edits and sends it (CA-2) | — | — | — |
| U-R13 Whether deleting or archiving a source breaks its forks | A later observation | Before offering delete/archive beside fork | Open (OBS-3 UNRESOLVED) |
| U-R14 Non-empty `instructionSources` (historical B-6) and record-view receiving | Runtime/record-view owner | Before relying on it in the record view | Current0.160.0 synthetic global/project sample supplied §2.1; actual record-view and wider-source candidate checks remain open |

## 15. Excluded acts and owners (REQ-006)

This file performs no act of: DEL-01-01 (carriage, boundary evidence,
qualification); DEL-02-01 (role meanings, shared allocation); DEL-02-02
(registration, selection of workflows, and (v0.2) the composition of a run's
workflow text, R19-7); DEL-02-03 (the compatibility check and (v0.2) the run
start, R19-7); DEL-04-01 (operation policy); DEL-04-03 (record format and
writer); DEL-11-02 and each consumer owner (adoption); DEL-01-03 (delegation
views); (v0.2) DEL-01-04 (the start display placement); DEL-01-05 (model and
account, and (v0.2) linking the person's global guidance into the App home,
R18-6); the host implementation owner (host loop, panel, seat); the person
(role choice, guidance edits, restore). It qualifies nothing and claims no
SWBPIPE join, witness or adoption.
