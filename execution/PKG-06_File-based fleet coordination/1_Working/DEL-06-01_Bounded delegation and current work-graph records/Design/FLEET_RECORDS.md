# Fleet records: bounded briefs, the current work graph and coordination events

- Contribution: DEL-06-01/FR-v0.1 (new). Serves OUT-001 (record definitions:
  §3, `fleet.record.schema.json`), OUT-002 (writer, reader and native
  association behaviour: §4–§7, designed; the prototype is not product code),
  OUT-003 (fixtures: §9, `prototype/fixtures/FX-FL1/`) and OUT-004
  (compatibility account: §8).
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not
  accepted. No App candidate exists; no case below passes a VER criterion.
- Run and owner: `APP-V4-DESIGN-PASS-4-20261003`, owner O-A (Type 2 TASK,
  Claude Opus 5.5, high effort), unit E-2; written 2026-10-03.
- Basis (sha256): this deliverable's `ScopeOfWork.md`
  50c88c9f5c753300e8f5dce403d4003cf119e28c4ee47e752b87bcf18ea38df9 (INIT contract; no SCA-V4-001/002/003
  block changed it, so R23-5's re-pin has no block to read). `docs/PRD.md`
  bb6e786f… (V4-PM-01/02/05, V4-ROLE-03, V4-AUT-03, V4-REC-02…05, V4-EXE-03);
  `docs/ARCHITECTURE.md` 317d5789… (§3 properties; V4-ARC-05);
  `docs/HOST_INTEGRATION.md` d4331c39… (V4-HI-61…63); `docs/EXAMINATION.md`
  471798bc… (V4-EXM-13); `docs/OPERATING_METHOD.md` 98836b52… (V4-OPS-02,
  12, 14, 30). Rulings by ID (R23-21): R23-2, R23-3, R23-4, R23-7, R23-8,
  R23-9.
- Suppliers read, by label and section: DEL-01-03/NPTD-v0.2 §7 (identity
  model, display rules, export §7.7, `npt.delegation-export` v0.2);
  DEL-04-03/RS-v0.10 §2, §3, §6, §13.6 (act requests and A16);
  DEL-02-04/ROLE-v0.2 §3.3 (Continue as, fork), §5.3, §6.2 (limit account),
  §6.3; DEL-01-02/RECOVERY-v0.2 §2 (DEF-1…DEF-7), §7 (ledger; children not
  indexed); DEL-01-01/OBS_2 §6 (delegation, through an adapter); the
  committed 0.158.0 JSON Schema bundle (`Thread`, `collabAgentToolCall`,
  `CollabAgentStatus`, `SubAgentSource`, `ThreadMetadataUpdateParams`).
- Pin (R23-3): written for 0.158.0 and 0.160.0. VC (VERSION_ADVANCE F16)
  reports the delegation types and features unchanged at 0.160.0; the adapter
  run was not repeated there. Every supplier fact below carries its standing.
- Labels: **SETTLED**, **DERIVED**, **INTEGRATION**, **PROPOSED** as R9.
- **Repairs after RV-E2 (in place, same label FR-v0.1, before acceptance).**
  - E2-R1: RF-10 and RF-12 report unread log lines and orphaned observations.
  - E2-R2: RF-11 makes a torn RS line a limit.
  - E2-N1: §3.1 marks `enforced-by-host` as FR's own value.
  - E2-N2: FR-D1 gives the HOSTING line.
  - R23-25: the latest decision holds (RF-6).
- **Change note (2026-10-04; R23-39; in place, same label FR-v0.1).** RF-5a:
  a connector need is read from its standing under DEL-07-02's CS-R1, not by
  presence. Unknown and nonconformant standings stay *unknown*, as in
  DEL-06-02 FV-10. Adds the §5 need row and cases C2, C5 and C8 in §9.
- **Change note (2026-10-04; RV2 FV10-R1…R3, R23-44).** Connector needs are
  declared (need kind `connector`). RF-5b covers undeclared connector
  records. Damaged records give *unknown* and missing ones *outstanding*,
  never presence. A satisfied need names a route still needed. The inputs
  are vendored and hash-checked, re-pinned to EU-D1 v0.2 (CFB-v0.2).
- **Change note (2026-10-04; RV2 FV10-R7, FV10-R8).**
  - RF-5a reads each claim's standing: an unrelied record-tier claim is
    listed, and with no route it makes the need *unknown*.
  - PR-P8 is vendored.
  - `VENDOR.json` is pinned in code.
  - The schema's connector label now says CFB-v0.2.
  - RF-5b states that the declaration is the contract.

## 1. What these records are

The App's ordinary-file records that let a person and the agents recover an
undertaking's coordination from the project alone (V4-PM-05): what was asked
of whom (the **brief**), what work is selected and how it depends (the
**current work graph**), and what actually happened (the **coordination
log**). They keep apart six facts the basis keeps apart (ARCH §3; REQ-003):
selected, dispatched, executing (as observed), returned, reviewed,
integrated. Each fact rests on its own record and evidence; none is inferred
from another. They are not the project DAG (DEL-10-04, V4-OPS-02), not
DEL-06-02's views, and not human-act records (DEL-04-03).

## 2. Decisions made here (owner O-A's ordinary decisions; reasons stated)

- **FR-D1 Who writes (PROPOSED).** Agents and the person write briefs, graph
  revisions and the log entries they are the actors or recorders of, through
  their ordinary file tools. The **App writer** writes only what the App
  observes: `dispatch_observed`, `child_observed`, `observation_ended` and
  `related_conversation`. The schema refuses those from any other recorder
  (INV-FL-2). Reason: HOSTING §6.1 has no App-offered tool in this increment
  ("none defined in this increment", the `item/tool/call` row at L783 of
  HOSTING-v0.9), and adding one would change the whole App's tool set
  (ADAPTER F-9). Files written with ordinary tools keep the file-native route
  working with or without the App (DEL-10-02; REQ-005; AC-007). The App
  validates and reads them; it does not take over their authorship.
- **FR-D2 Format (PROPOSED).** Its own versioned JSON records,
  `chirality.fleet.record` 0.1 (`fleet.record.schema.json`): one file per
  brief and per graph revision, and one append-only JSON Lines log. Reason:
  V4-HI-63 needs identified versions and consumers. The method's current
  Markdown work graphs (Root SPEC §9.8) are a practice DEL-10-02 owns, not a
  format with identified versions; this format does not change them, and
  their adoption of it would be a separate instruction change.
- **FR-D3 Location.** The records live with the user's project (V4-REC-02;
  RS OF-9). No path is selected (OI-013, OI-014). The prototype uses
  `briefs/`, `graphs/<undertaking>/` and `coordination.fleet.jsonl` under one
  folder.
- **FR-D4 Child index (R23-4).** DEL-06-01 holds the durable index of native
  children: every `dispatch_observed`, associated with a brief or not.
  RECOVERY's ledger is unchanged.
- **FR-D5 What delegation is (R23-9).** A dispatch is a native Codex child,
  recorded with its mechanism ("Codex native subagent"). A "Continue as"
  conversation or a fork is a `related_conversation`, never a dispatch. Work
  done elsewhere is an `external_result`: an owner and a result from files,
  with no execution claimed.
- **FR-D6 Decisions (R23-8).** A work item that waits on a person's decision
  names the package's RS `act_request` as a `decision` need. No PKG-06 record
  holds the package.

## 3. Record kinds (`fleet.record.schema.json`)

Every record carries a header:
- `format` `chirality.fleet.record` and `formatVersion`;
- `recordId` (`fl:…`), `kind` and `undertaking`;
- the **recorder**, an actor {kind agent · person · App · external, identity,
  role, and for a person `identityVerified`};
- `writtenAt`;
- optionally `corrects` with a reason (a correction is a new record naming
  the corrected one, as RS OF-5 does).

### 3.1 Brief (V4-PM-01; REQ-001; AC-001)

| Element | Meaning |
|---|---|
| `briefId`, `workItem` | The brief and the graph item it serves |
| `purpose` | What the work is for |
| `basis` | References, with content identity where known, to the accepted or stated basis |
| `context` | References supplied as context |
| `authority` | `mayDecide`, `escalate` (required, at least one) and `reservedToPerson` (what the executor must not decide) |
| `tools` | Each tool with a **limit** {statement, standing, mechanism where enforced} |
| `writeScope` | Each target with its limit |
| `expectedReturn` | Description, form (file · message · both), return path, artifacts |
| `preparedBy`, `delegateRole` | Who prepared it and the role it is for |
| `limits` | The role's stated limits as ROLE's limit account hands them (L-TASK-1, L-ALL-1), carried as handed |
| `supersedes` | The brief this one replaces; briefs are never edited |

**Limit standing (SETTLED by K-10 and V4-ROLE-03; representation PROPOSED).**
The values are:
- `stated-not-enforced`;
- `enforced-by-supplier` or `enforced-by-host`, each requiring the mechanism
  that enforces it (for example "Codex sandbox mode workspace-write, the
  person's own setting"). `enforced-by-host` is **FR's own value**
  (PROPOSED), for a tool or write limit a host enforces. It is never handed
  from ROLE's limit account or NPTD's export, which use only
  `stated-not-enforced`, `enforced-by-supplier` and `unknown`. A delegating
  role's limit stays within `stated-not-enforced` or `unknown` (ROLE LA-5);
- `unknown`.

The schema refuses an "enforced" standing without a mechanism (INV-FL-1). A
declared limit grants nothing the host does not enforce (V4-OPS-30). The
default depth, which gives a child no delegation tools (OBS-2, adapter), is
the person's configuration and is **never** recorded as enforcing L-TASK-1
(ROLE LA-5).

### 3.2 Work graph and current selector (V4-PM-02; REQ-002; AC-002)

- A `work_graph` record is one **revision** {revision n, `supersedes`, basis,
  `projectDagRef`, items}. Revisions are never edited. Each item has {itemId,
  outcome, owner, brief, writeScope, `needs`, `selected`, results, next,
  check}.
- A `needs` entry is {kind `item` · `decision` · `input` · `connector`,
  ref, condition, and `connector` for kind `connector` only (RF-5a)}.
  The graph holds **selected work only**; an executing state cannot be
  written into it (INV-FL-4).
- `current_graph` is the **one selector** (REQ-002), a log entry {graph
  record, graph content identity}. The latest selector in written order
  holds. Earlier revisions and selectors stay readable.

### 3.3 Coordination log (append-only)

| Kind | Recorder | Records | Never establishes |
|---|---|---|---|
| `dispatch_observed` | App only | A native child observed from a completed spawn: mechanism, child and parent thread, `parentSource`, `agentRole`, spawn item, spawn-prompt content identity, the **association** with a brief, the delegating role's limit standing, the observation {source, time, pin, standing} | That the child did the work, returned, or was reviewed |
| `child_observed` | App only | The child's last status, Codex's value unchanged | A return (NPTD DR-2) |
| `observation_ended` | App only | Observation of a child ended: Codex process stopped or exited, App quit, relaunch, or cause not observed; last status | Any outcome |
| `return_recorded` | Whoever received it (usually the manager) | The returned items with content identity, who returned them, the evidence (the child's final message item, a file) | Review or integration |
| `review_recorded` | The reviewer or the manager | Reviewer, verdict (no blocking findings · findings to repair · not concluded), findings, the content reviewed | Checking (A4), acceptance (A5) or approval (A6), which are RS human-act records |
| `integration_recorded` | The integrator | The return integrated, the review it followed, evidence (for example a commit) | Any human act |
| `basis_changed` | Whoever observed the change | The changed input, its previous identity, the affected items | Reopening by itself |
| `related_conversation` | App only | "continued from" or "forked from", with the source thread | A delegation (R23-9) |
| `external_result` | The manager or the person | An outside owner and the result files, with the mechanism as the files state it | Dispatch or execution |

## 4. Native association (REQ-001, REQ-003; AC-003)

**Supplier facts** (Codex 0.158.0; delegation surfaces unchanged at 0.160.0
per VC):
- **Observed through the OBS-2 adapter, not stock behaviour.** A child is
  known only from a **completed** `collabAgentToolCall` `spawnAgent`, whose
  `receiverThreadIds` names it. No `thread/started` arrives for a child.
  `thread/read` of the child gives `parentThreadId` and `agentRole`.
  `thread/list` omits children; `thread/loaded/list` includes them.
- **Observed-in-generated-types.** `ThreadMetadataUpdateParams` lets a client
  set only `daybreakEnabled`, `gitInfo` and `projectId`, so there is no
  client-writable tag to put a brief's identity on a thread.
- **Observed on the stock pairing.** Stock LM Studio 0.4.16 drops the
  delegation namespace, so no child exists there (OBS-2 §6.1).

**Association rule (PROPOSED).** The App cannot tag a thread, so the brief
travels in the spawn:
- **AS-1.** The manager's guidance asks it to put `brief:<briefId>` in the
  spawn message. This is stated, not enforced.
- **AS-2.** When a spawn completes, the App writer records
  `dispatch_observed`, carrying the `spawnPromptContent` identity and the
  association state:
  - *brief reference in spawn prompt*, when the prompt names a brief that
    exists, with that brief's content identity;
  - *brief reference in spawn prompt; brief changed since*, when the brief
    file's identity now differs;
  - *no brief reference*.
- **AS-3.** A child with no brief reference is still indexed (FR-D4) and
  shown as a child of its parent; it is associated with no work item.
- **AS-4.** Reading the reference out of a supplier item's prompt field
  identifies an association, not an act. It is not RS's act-request
  identification (EXEC RC-5 governs that).
- **AS-5.** A task agent's own delegation is recorded like any other, with
  the `delegatingRoleLimit` standing as ROLE hands it (K-10).

## 5. States and transitions (per work item; PROPOSED; derived by the reader)

| Facet | Values | From | Never from |
|---|---|---|---|
| selected | yes · no | the current graph | — |
| brief | prepared · named, not found · none | brief files | — |
| dispatch | dispatch observed (child, parent, association) · no dispatch observed · not delegated (owner is the person or external) | `dispatch_observed` | a brief alone (AC-001) |
| executing | last observed ‹Codex status› · observation ended (cause, last status) · not observed | `child_observed`, `observation_ended` | a conversation's recovery (ARCH §3) |
| return | returned (by, recorded by) · none | `return_recorded` | a child's `completed`; an agent's message |
| review | ‹verdict› (by) · none | `review_recorded` on that return | a return |
| integration | integrated (by, evidence) · none | `integration_recorded` on that return | a review; reconnection |
| need | satisfied · outstanding · unknown, each with its reason | item: the needed item's integration or external result; decision: an RS `human_act` of the kind the package names, citing it (for A16, a named alternative); input: the file (not a connector record, RF-5b); connector (declared): its standing supports reliance (RF-5a) | readiness from a missing feed (V4-HI-62); a decision from a chat message; a connector record's presence |

DEL-06-02 derives queues and waiting causes from these facts. This file
derives the facts only.

## 6. Writer and reader (OUT-002; PROPOSED; `prototype/fleet_store.py`)

- **W-1** Every record is validated before it is written; an invalid one is
  refused and nothing is written.
- **W-2** Brief and graph files are created exclusively and never
  overwritten; a change is a new record.
- **W-3** Log entries are appended, one per line.
- **RF-1** The current graph is the latest selector's revision. If the
  revision file's content no longer matches the selector, the graph is not
  used and the reader says why.
- **RF-2** A brief is "prepared". Prepared is never "dispatched".
- **RF-3** Dispatch comes only from `dispatch_observed` associated with the
  item's brief.
- **RF-4** Return, review and integration each come only from their own
  record and attach to one return.
- **RF-5** An item need is satisfied by the needed item's integration or
  external result.
- **RF-5a Connector needs (R23-39; RV2 FV10-R1, FV10-R3; DEL-07-02 CFB-v0.2
  §2, CS-R1 per connector, CS-R5).** A connector need is **declared**: need
  kind `connector`, with `connector` (`pec` · `domains`) and the receiving
  record's path as `ref`. The schema requires both and refuses `connector`
  on any other kind (INV-FL-8, INV-FL-9). The reader validates the record's
  standing against DEL-07-02's `connector.standing.schema.json`, using the
  vendored copy, hash-checked before use (R23-44). It reads the need from the
  standing, **never from the file's presence**:

  | Record | Need |
  |---|---|
  | missing | *outstanding*, with the connector named |
  | unreadable (torn, not JSON), without a standing, or with a nonconformant standing (consistent with RF-10, RF-11) | *unknown* |
  | from another connector than declared | *unknown* |
  | standing supports reliance, every relied claim's own standing supporting it | *satisfied*. Where the record's `route.needed` is true, the fact says that reliance covers only the record's covered parts and names the source-file route still needed for the rest (FV10-R3; `routeNeeded`) |
  | standing supports reliance, but a record- or admitted-tier claim's own standing does not (e.g. PR-P8's c3, `unknown` under PR-7), and `route.needed` is true | *satisfied*, and the fact lists each such claim with its condition ("claim(s) not relied: c3 unknown: …") and the route that covers it (FV10-R7; `unreliedClaims`) |
  | the same, but `route.needed` is false | *unknown*: record-level reliance never hides a claim-level gap that no route covers (FV10-R7; CS-R5) |
  | condition *unknown* | *unknown* (CS-R5) |
  | otherwise | *outstanding*, with the facets, each reason and the route account (`ra:…`) |

  Presence-advisory claims (PEC `presence_advisory`) are listed as advisory
  (`advisoryClaims`); they are not reliance gaps. A claim whose standing does
  not read or conform counts as not relied. The fact carries `connectorNeed`,
  `connector`, the record id and the route reference. DEL-06-02's FV-10
  words these facts and does not re-read them.
- **RF-5b (FV10-R1).** A plain input need whose file is a connector receiving
  record (a JSON record with `response_standing`) is *unknown*, with "declare
  it as a connector need".
  - **The contract is the declaration** (RV2 FV10-R8). Only a declared
    connector need is guaranteed the RF-5a reading.
  - RF-5b is a guard for the readable case. A torn connector record named as
    a *plain input* cannot be recognised, so it reads by presence, as any
    plain input does.
  - Connector material must therefore be declared (INV-FL-9 refuses
    `connector` on a plain input).
- **Vendored inputs (R23-44).** RF-5a reads O-D's EU-D1 v0.2 refreeze from
  `prototype/fixtures/vendored/EU-D1/`:
  - the standing schema `bf4cef4d…0719` (committed at `25054b04df`);
  - the records PR-P1, PR-P3 and PR-P6, as O-D's frozen reader-input
    manifest `e68154c6…` lists them.

  - PR-P8 (FV10-R7), taken from O-D's `D/evidence/records/` after the
    R23-48.1 move, before it reached git, so it is re-pinned if O-D's
    committed bytes differ.

  Their hashes and sources are in `VENDOR.json`. **`VENDOR.json` is itself
  pinned** in `fleet_store.py` (`VENDOR_SHA256`; FV10-R8), so a file edited
  together with its entry is refused. A copy whose bytes differ is refused
  (`VendoredInputChanged`). Re-pinned deliberately from EU-D1 v0.1
  (`589f2c5d…`), whose bytes were never committed. Re-pin again at O-D's next
  refreeze.
- **RF-6** A decision need is satisfied only by an RS `human_act` of the
  named kind citing the request (for A16, with a named alternative). Without
  the RS records it is *unknown*. Where several such acts exist, the latest
  holds, and a corrected entry is replaced by its correction (R23-25; RS
  OF-5).
- **RF-7** Basis changes are listed on the items they name.
- **RF-8** The child index lists every observed child.
- **RF-9** Reading writes nothing.
- **RF-10 (RV E2-R1).** Every coordination-log line the reader could not
  read (torn or nonconformant) is reported by line number with the facts
  (`logIncomplete`). Such a line could be any record of any item, so a
  consumer must not derive readiness, an empty queue or any not-done state
  while one exists (DEL-06-02 FV-8a).
- **RF-11 (RV E2-R2).** A torn RS line is a limit, not a failure. A decision
  need with no satisfying act becomes *unknown*, not *outstanding*, while an
  RS line is unread.
- **RF-12 (RV E2-R1).** An observation (`child_observed`,
  `observation_ended`) whose child has no `dispatch_observed` is an orphan.
  It is a limit ("a dispatch record may be missing"), and the child is
  reported with the facts (`orphanChildren`).
- A torn or nonconformant log line is a limit and is not used. An unreadable
  brief or graph is a limit.

**Failure at each step:**

| Step | Failure | Behaviour |
|---|---|---|
| Write a brief or revision | Invalid; file exists | Refused (W-1); refused (W-2) |
| Select a graph | Revision changed after selection | RF-1: not used, reason shown; the previous selector is not silently used either |
| Observe a spawn | Spawn not completed; no reference; brief changed | No record until completed; *no brief reference*; *brief changed since* |
| Observe a child | Codex process stops, App quits or relaunches (RECOVERY DEF-5/6/7) | `observation_ended` with the cause; after a relaunch the App re-reads children from the parent's history and `thread/read` (NPTD SQ-4) and appends new `child_observed` entries; nothing earlier is rewritten |
| Receive a return | No evidence | Refused (schema) |
| Read | Torn log line; torn RS line; missing RS records; orphaned observation | RF-10 (reported by line; consumers derive no completeness); RF-11 (limit; decisions *unknown*); decision needs *unknown*; RF-12 (limit) |

## 7. Interfaces

| Direction | With | What | Condition | When it fails |
|---|---|---|---|---|
| Consumed (DEP-06-01-007, admitted) | DEL-01-03 | The delegation export (§7.7) and spawn items, as the App writer's input for `dispatch_observed`/`child_observed` | A completed spawn | No export → no dispatch recorded; never inferred |
| Consumed (DEP-06-01-008, admitted) | DEL-04-03 | RS `act_request` and `human_act` records for decision needs and act references | Records supplied to the reader | *unknown* |
| Consumed (DEP-06-01-013, admitted) | DEL-01-01 | The pin the observations name | — | The observation's pin says which |
| Consumed (DEP-06-01-011, admitted) | DEL-07-01 | Coverage and adoption account before relying on a changed PEC consumer path | Only at a format change PEC consumes | §8 holds the change |
| Runtime value (no row) | DEL-02-04 | The limit account standings, carried as handed | When a brief or dispatch is recorded | `unknown` |
| Runtime value (no row) | DEL-01-02 | Relaunch and quit facts for `observation_ended` | — | "cause not observed" |
| Offered (DEP-06-02-008) | DEL-06-02 | The records and the reader's facts (§5) | — | — |
| Offered (DEP-09-05-006) | DEL-09-05 | FX-FL1 and the reader, for its joined witness | — | — |

R23-2 cycle note: every consumed row above is from DEL-06-01 to a supplier,
and every one is already admitted. DEL-01-03 must not consume these records
(NPTD §16.3).

## 8. Compatibility account (OUT-004; REQ-005; AC-006)

| Format | Version | Writers | Consumers | Change rule |
|---|---|---|---|---|
| `chirality.fleet.record` | 0.1 (PROPOSED) | Agents and the person (FR-D1); the App writer for observed kinds | DEL-06-02 (views), DEL-09-05 (witness), DEL-09-11 (reconstruction, through its input set); **PEC: none adopted** (OI-022; DEP-002 unestablished) | A minor version adds optional elements or kinds; a reader that does not know them reads the rest and lists them as unread. A major version changes meaning. Before any consumer path relies on a change, the change is listed here with its consumers; for PEC, DEL-07-01 supplies the affected coverage and adoption account (DEP-06-01-011). A projection never governs this writer (V4-HI-63) |

Example change (bounded): adding a `priority` element to work items is minor.
DEL-06-02 ignores it until it adopts the change. If PEC later consumes items,
DEL-07-01 states whether its coverage includes the element before anyone
relies on it.

## 9. Fixtures and verification (OUT-003; designed; prototype results are not candidate evidence)

`prototype/run_fleet.py` builds **FX-FL1** through the writer. FX-FL1 is
undertaking FX-U1 (invented), with:
- items W1–W9 in two graph revisions;
- four briefs with observed dispatches, one brief with none, and one child
  without a brief reference;
- an integrated item, a return awaiting review, a child that completed with
  no return, and a child whose observation ended at quit;
- a basis change;
- a "Continue as" conversation;
- an external result;
- decision needs on the early path's PKG-1 (decided) and PKG-2 (pending).

The fixture is at `prototype/fixtures/FX-FL1/` with `MANIFEST.sha256`. It
reads FX-DP1's RS records for decisions.

| VER | Cases (`run_fleet.py`) |
|---|---|
| VER-001 | Seven elements present; standings with mechanism; a prepared brief claims no child |
| VER-002 | Selector names r2, r1 kept; W3 waits on W2 while W1 is satisfied; external result and input satisfy W9; the graph holds no executing state; re-reading gives the same facts |
| VER-003 | Child and parent kept with association; unassociated child indexed; unknown outcome after quit |
| VER-004 | Completed child without return not promoted; return awaiting review not promoted; return, review, integration on their own records; basis change names W2/W3; Continue as is not a dispatch |
| VER-005 | Decision satisfied by the recorded A16; pending stays outstanding despite an agent's message; without RS records, unknown |
| VER-006 | §8 (review of the account; no executable case) |
| VER-007 | Facts from files alone; reading writes nothing |
| VER-008 | §10 (artifact and owner comparison) |
| Writer, reader | W-1 refusal, W-2 no overwrite, RF-1 changed graph not used, torn line a limit; RF-10/RF-12 a truncated dispatch line reported unread with its child orphaned; RF-11 a torn RS line a limit with decisions unknown; INV-FL-1…7 |

Result on 2026-10-04, after FV10-R7/R8: 45/45 (42 before), including the
committed-fixture check. RF-5a's cases run on a scratch copy of FX-FL1 with
revision r3 and the vendored EU-D1 v0.2 records (hash-checked):
- C2: an adopted but stale record is outstanding, with its route account;
- C5: a stale standing altered to claim reliance is nonconformant, so
  *unknown*;
- C8: an absent connector is outstanding, an adopted and current one is
  satisfied, and a plain input still reads by presence.
- FV10-R3: the satisfied PR-P1 need names route `ra:EUD1-Q1`, still needed
  for the rest of the question.
- FV10-R1 (RV2's probes): a half-truncated record and a renamed standing key
  give *unknown*, a missing record *outstanding*, and an undeclared
  connector record used as a plain input *unknown* (RF-5b).
- R23-44: a vendored copy with changed bytes is refused. FV10-R8: so is a
  file edited together with its `VENDOR.json` entry.
- FV10-R7: PR-P8 with `route.needed` true is satisfied and names c3
  *unknown* and the route. With `route.needed` false (nothing else changed)
  it is *unknown*.
- INV-FL-8 and INV-FL-9: the need kind's schema rules.

## 10. Owner boundary (REQ-006)

| Act or production | Owner | Here |
|---|---|---|
| Native delegation presentation, the export | DEL-01-03 | Consumes the export |
| Act and run records, decision capture | DEL-04-03; DEL-01-04's act control | Cites and reads |
| Queue, waiting, decision views | DEL-06-02 | Supplies facts |
| Joined fleet witness | DEL-09-05 | Supplies FX-FL1 |
| PEC receiving and adoption | DEL-07-01; PEC owning project | §8 only |
| Undertaking practice; project DAG | DEL-10-02; DEL-10-04 | `projectDagRef` cites; nothing restated |
| Review and integration acts | Managers | Recorded by them with evidence |
| Human decisions | The person | Never recorded here; cited from RS |

## 11. Open matters

| Matter | Owner | Point of need |
|---|---|---|
| AS-1 is guidance, not enforcement: a manager may spawn without the reference | O-A, with DEL-02-04 (guidance text) | Before the App's guidance is written |
| PEC envelope (OI-022) | App consumer owner and PEC owner | Before operational consumer reliance |
| Process placement of reader and writer (OI-008) | Owner, at the phase review | Before allocation |
| Content-identity method: the prototype uses sha-256 of file bytes as a TEST VALUE (RS U-04) | Owner with DEL-04-03 | Before reliance |
| Delegation on any stock route is unobserved (adapter only) | A later observation | Before VER-003 on a candidate |
