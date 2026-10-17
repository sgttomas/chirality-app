# Fleet records: bounded briefs, the current work graph and coordination events

- Contribution: DEL-06-01/FR-v0.1 and native-links 0.2. Serves OUT-001
  (record definitions: §3 and the two Fleet schemas), OUT-002 (current App
  reader/derived workspace and native-link writer: §6.1–§6.2; full native
  dispatch/brief association remains designed), OUT-003 (local App regression
  coverage and historical prototype fixtures: §9) and OUT-004
  (compatibility account: §8).
- Current App contribution: manual source inspection, reconstructed
  graph/return/waiting views, and protected native Fork/Continue-as records.
  The recorded stock 0.160.0 witnesses do not expose the spawn prompt needed for §4's
  full brief-to-child association. Local regressions and historical prototype
  results establish neither the joined supplier/human witness nor acceptance.
- Original design run and owner: `APP-V4-DESIGN-PASS-4-20261003`, owner O-A (Type 2 TASK,
  Claude Opus 5.5, high effort), unit E-2; written 2026-10-03.
- Original design basis (sha256): this deliverable's `ScopeOfWork.md`
  50c88c9f5c753300e8f5dce403d4003cf119e28c4ee47e752b87bcf18ea38df9 (INIT contract; no SCA-V4-001/002/003
  block changed it, so R23-5's re-pin has no block to read). `docs/PRD.md`
  bb6e786f… (V4-PM-01/02/05, V4-ROLE-03, V4-AUT-03, V4-REC-02…05, V4-EXE-03);
  `docs/ARCHITECTURE.md` 317d5789… (§3 properties; V4-ARC-05);
  `docs/HOST_INTEGRATION.md` d4331c39… (V4-HI-61…63); `docs/EXAMINATION.md`
  471798bc… (V4-EXM-13); `docs/OPERATING_METHOD.md` 98836b52… (V4-OPS-02,
  12, 14, 30). Rulings by ID (R23-21): R23-2, R23-3, R23-4, R23-7, R23-8,
  R23-9.
- Original design suppliers read, by label and section: DEL-01-03/NPTD-v0.2 §7 (identity
  model, display rules, export §7.7, `npt.delegation-export` v0.2);
  DEL-04-03/RS-v0.10 §2, §3, §6, §13.6 (act requests and A16);
  DEL-02-04/ROLE-v0.2 §3.3 (Continue as, fork), §5.3, §6.2 (limit account),
  §6.3; DEL-01-02/RECOVERY-v0.2 §2 (DEF-1…DEF-7), §7 (ledger; children not
  indexed); DEL-01-01/OBS_2 §6 (delegation, through an adapter); the
  committed 0.158.0 JSON Schema bundle (`Thread`, `collabAgentToolCall`,
  `CollabAgentStatus`, `SubAgentSource`, `ThreadMetadataUpdateParams`).
- Current supplier basis: owner-authorized development/definition pin
  0.160.0, received from DEL-01-01 `Design/HOSTING_BOUNDARY.md` and named by
  `hosting.rs` `DECLARED_PIN`; supplier qualification remains separate.
  Historical design observations were written for 0.158.0 and 0.160.0
  (R23-3). VC (VERSION_ADVANCE F16) reports unchanged delegation types at
  0.160.0; it did not repeat the adapter run. Every observation below retains
  its actual pin and standing, including the stock-route limits in §4.
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
  - Later the same day (FV10-R9, offered for closeout): a claim tagged with
    another connector counts as not relied, with case P8x.

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
  (INV-FL-2). Reason: when this was written HOSTING §6.1 had no App-offered
  tool ("none defined in this increment", the `item/tool/call` row at L783
  of HOSTING-v0.9), and adding one changes the whole App's tool set
  (ADAPTER F-9). HOSTING §6.1 now defines one, the read-only records
  capability (RS §13.9); it writes nothing, so agents still write their
  fleet entries with their file tools. Files written with ordinary tools keep the file-native route
  working with or without the App (DEL-10-02; REQ-005; AC-007). The App
  validates and reads them; it does not take over their authorship.
  *Where the App's observations are kept* (owner, 2026-10-12: "Write to
  both (Recommended)"; RS §13.8). The coordination log stays one co-written
  file in the project (FR-D2, FR-D3): the App writes its observations
  (`dispatch_observed`, `child_observed`, `observation_ended`,
  `related_conversation`) there when that producer exists, so agents and file-native readers
  keep every entry, PEC, DEL-10-02's route "with or without the App" and
  FR-D4's child index included. The App also writes each of its
  observations to its records store, in the project's subtree at
  `fleet/coordination.fleet.jsonl`, outside the agents' writable workspace,
  and that copy governs. Inside the App, an App-observation entry in the
  project file that does not match the store's copy is shown as a limit, or
  as the claim of the recorder it names, never as an App observation.
  File-native readers have no such protection: they read the project file as
  it is. INV-FL-2 refuses App-observation kinds only from a recorder other
  than the App, so an entry an agent writes there naming the App as its
  recorder passes it; file-native readers cannot tell it from a real one. The quoted 0.1 shapes remain unchanged. The added 0.2 native-links
  profile and its consumers are accounted for in §8. This
  is read by the current App source slice (§6.1). The 0.2 native-link writer (§6.2) now writes both copies from actual
  source-issued Fork/Continue-as results. The 0.1 dispatch/child producer and
  its association remain Design.
- **FR-D2 Format (PROPOSED).** Its own versioned JSON records,
  `chirality.fleet.record` 0.1 (`fleet.record.schema.json`): one file per
  brief and per graph revision, and one append-only JSON Lines log. Reason:
  V4-HI-63 needs identified versions and consumers. The method's current
  Markdown work graphs (Root SPEC §9.8) are a practice DEL-10-02 owns, not a
  format with identified versions; this format does not change them, and
  their adoption of it would be a separate instruction change. The separate
  0.2 native-links profile (`fleet.native-links.schema.json`, §6.2) carries
  the implemented conversation relationships and mechanical recording outcomes;
  it changes no 0.1 brief/graph shape.
- **FR-D3 Location and placement (settled, owner 2026-10-10).** The records
  live with the user's project (V4-REC-02 as then worded; RS OF-9), in one fixed default
  folder, `<project>/.chirality/fleet/`: `briefs/`, `graphs/<undertaking>/`
  and `coordination.fleet.jsonl`, the layout the prototype uses. It sits
  beside the App's other project folders (`.chirality/workflow-drafts/`,
  `.chirality/records/`; WR §3). v4.0 has no folder picker. The Rust host
  reads and writes the records, as for the draft workspace (WR §11, the
  owner's "A, proceed with the Rust host"): file writes stay out of the
  webview, and the TypeScript interface lists and presents what the host
  hands it. Files written there with
  ordinary tools stay valid input (FR-D1). The owner agreed with this
  recommendation: "For the Fleet workspace I agree with the approach you laid
  out and your recommendations for what the Design leaves open." This settled
  the records' placement and selected their path. The owner's general OI-008
  ruling of the same day extends that placement to the whole App: "The Rust host owns everything that
  writes the person's files or the App's records, talks to Codex, or captures a
  person's act. The web view presents, and sends only what the person
  initiates. It never writes records or operates the act control." Neither
  decides OI-013 or OI-014. On 2026-10-12 the owner moved decisions, accepted
  records and run records to the App's records store (PRD R-STORE). The owner
  then split the fleet files by who writes (owner, 2026-10-12: "Split by who writes (Recommended)"). That split first
  called the coordination log App-written; the log is co-written, so the
  owner refined it for the log
  (2026-10-12: "Write to both (Recommended)"): the log, with every entry,
  stays in `<project>/.chirality/fleet/coordination.fleet.jsonl`, and the
  App also keeps its own observations in the records store, whose copy
  governs inside the App (FR-D1 "Where the App's observations are kept").
  Briefs and graphs stay in `<project>/.chirality/fleet/`. The App now
  writes 0.2 native links and recording outcomes to both copies (§6.2);
  the 0.1 dispatch/child writer remains Design. Fleet stays outside the
  ordinary RS import census; whole Fleet payload export is separate (§6.1). This log is not the registered legacy log
  `records/coordination.rs.jsonl` (RS §13.7), which is an RS record log, a
  different file in a different format.
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

**Native relationship identity (owner, 2026-10-14).**

> You shouldn't link to ephemeral ideas of an objective (an "undertaking") when there's session IDs that presumably are created for each unique session and can be linked to indicate when something was forked?  I don't like this idea of an "undertaking" being used at all as an identity.

Native relationship observations use the actual native conversation IDs,
qualified by their source/home, and preserve the original observed request
and generation context. An observation has its own stable record identity.
An objective or undertaking description supplies no identity, association key
or prerequisite for recording. A fork or continued-from relation links the
identified conversations; it neither requires a classification choice nor
derives that link from a folder, workflow choice or objective description.
The 0.2 native-links profile and current Rust observer/reader implement
this direction for App Fork and Continue-as results. Existing 0.1 files remain readable as quoted source records;
their undertaking fields cannot establish native conversation identity.

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
- **Observed natively at 0.160.0, with limits** ([native witness
  2026-10-10](../../../PKG-01/DEL-01-02/Design/NATIVE_WITNESS_2026-10-10.md) items 11–12). The route was stock Codex through the App
  Server, with a ChatGPT account and `gpt-6-luna`, in one run.
  - Spawn, wait, follow-up and close worked.
  - Only `wait` appeared as a `collabAgentToolCall` item. No spawn item was
    shown, so the spawn prompt was not available from the parent's items.
  - The child was known from `subAgentActivity`, with its parent inferred and
    its status not reported.
  - An agent reached only its own spawn tree: `send_message` to another
    conversation's ID returned "not found".
  - The child's input is not readable either ([trial witness
    2026-10-10](../../../PKG-02/DEL-02-02/Design/TRIAL_WITNESS_2026-10-10.md);
    WR U-WR-25). The spawn task reaches the child as an inter-agent
    `agent_message` (author `/root`, recipient the child's path) whose payload,
    after a readable header, is `encrypted_content`; no user message carries
    it. The App's read of the child's first turn found no user message, and
    reading again read the same.
  - So at 0.160.0 the child thread and its parent are observable (from
    `subAgentActivity`: a `started` row, or by inference), but the spawn prompt is
    observable neither from the parent's items nor as the child's readable
    input. AS-2's spawn item and `spawnPromptContent`
    identity cannot be computed from Codex at this pin, and AS-1's carriage
    of `brief:<briefId>` cannot be seen (§11).

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

## 6. Writer and reader (OUT-002; implemented App slices and retained prototype design)

### 6.1 Current manual App source reader

`fleet_records.rs` reads the fixed `.chirality/fleet/` packet in the Root's
selected project workspace. The path-free `read_fleet_records` native command
is called only by the panel's explicit Refresh. It returns all readable
schema-valid 0.1 brief files, graph revision files and coordination rows, plus
0.2 native-link and mechanical recording-outcome rows, with
their complete record, source path/line, claimed recorder and source limits.
Unknown formats/kinds, malformed files, unreadable members and an unclosed
final log line remain explicit limits. Return/evidence references remain quoted. The Fleet workspace now derives
current-graph, return and waiting claims as described below; ordinary input and
declared connector references are read only inside the fixed Fleet folder.

FR-D1's protected copy governs App observations in its own written order.
Matching compares exact line bytes, including whitespace, key order and line
ending. Replaying a matching old project row cannot move that observation in
the protected order. Project duplicates/conflicts and missing/mismatching copies
are limits and keep their claimed recorder. A healthy protected-only observation
remains readable with its missing project counterpart named. Any unread or
duplicate/conflicting protected row withholds the entire App observation
projection; its readable rows remain explicitly incomplete store claims.
The existing placement check also qualifies provenance: an agent-writable
development override retains its matching store bytes and governing order as
quoted evidence, with the placement limit, but supplies no protected App
observation. Development recording remains permitted under the existing rule.

After a complete stable read, the App retains a length/SHA-256 proof of the
accepted protected log byte prefix in this process, bound to the lossless
project/store source paths and store/project identities. A shortened, rewritten or missing accepted prefix
withholds the governing projection and App provenance with a history-change
limit; a refusal does not reset the proof. Restoring the original prefix, with
an exact append if needed, permits another read. This unsigned proof is only in
memory: a cold restart cannot detect a previously valid tail removed or both
copies rewritten before the first read. It authenticates no recorder and adds
no durable continuity or signing claim.

The identity lookup inspects existing store identity, root registry, project
link, project identity and administrative state. It calls no mint/import path.
It shares only an already-existing regular admission file nonblockingly;
missing/busy controls remain unavailable and are never created or repaired.
Closed retained payloads are readable; disposed/incomplete-disposal payloads
are unavailable even if recreated. Every data file uses the component-bound,
nonblocking regular-file opener; identity and data stamps plus directory
inventories are rechecked across the whole read. A changed protected snapshot
withholds protected row contents and authority. Configured project/store aliases
are resolved to their physical sources, and a changed physical project refuses
the whole result.

BagIt import records exact imported member-prefix lengths and digests through
`records_package_import.rs` (RS §13.8). Imported Fleet rows, including exact
App-named project/store counterparts, are quoted package claims; they establish
no local App observation, native relationship or protected order. A later local
append can have its own protected provenance only after the complete imported
prefix and its surviving original native import/control evidence are verified.
A line crossing that prefix boundary stays imported, including an originally
unterminated row completed by a later newline. Missing, changed or concurrently
replaced package-origin controls withhold all App provenance while stable
readable bytes/order remain quoted. Derivative control repair and recovery of a
missing link are separate explicit native operations; the Fleet reader neither
repairs controls nor mints an identity. A package signature, role/CCE authority
and native receipt are never inferred from imported file placement.

The source-schema copy is embedded and checked by `schemas/sync.py`.
Protected fleet bytes are export payload, while both fleet logs remain outside
the RS corpus, chain-head list, ordinary RS-home decision and legacy import
census. A fleet-only payload can be exported when no ordinary history waits for
import; adding fleet never bypasses a required or unfinished import. An empty
capture folder or its exact ownership-control file establishes no ordinary RS
home, including when export created the control. The completed spawn prompt
is still unavailable from the current native snapshot (§4); no native dispatch
or child-state producer is added. The prototype's graph
content-identity method remains a TEST VALUE (§11). New selectors use the
explicit App method below; historical selectors retain their unsupported-method
limit and are never rebound.

### 6.1a Derived file workspace (App-local implementation)

`fleet_views.rs` consumes the once-read packet and returns `workspace` through
that same path-free native command. `FleetRecordsPanel.tsx` presents each
undertaking's graph, return-review queue, selected work, owners, continuation,
needs, causes and source records. These are file-based recorded claims; they
neither dispatch nor activate a native conversation or perform a human act.

For new `current_graph` selectors this consumer adopts the already reviewed
App method `chirality.app.exact-bytes.sha256/v1` (C §5.5; RS §6.2a): lowercase
64-hex SHA-256 of the exact graph file, including whitespace and its final line
ending. The selector names that file's record identity and undertaking. The
latest selector in written order is checked against the original coherent
buffer. A missing, duplicate, changed or unsupported latest target never falls
back to an older selector. The schema remains open to other designations; a
reader supports only its explicitly adopted method. No prototype, host or
historical identity is relabelled. This is a bounded consumer technical choice,
not a host/global algorithm or an acceptance-criterion change.

Each return remains queued until an integration record names that return.
Reviews and integrations are matched by undertaking, item and return identity.
An integration of an earlier return does not satisfy a dependency on an item's
newer return. Corrections require a prior same-kind target and a reason;
unresolved targets or competing corrections qualify the projection. Duplicate
briefs/items/record identities never select an arbitrary owner or state.

Input references are relative to `.chirality/fleet/`, without absolute paths,
parent traversal, symlinks, hardlinks or special files. Their bytes, ancestor
identities and absent leaves join the packet's first-observation census. A
source changed between reads cannot reset that census. A failed final census
withholds the entire derived workspace. Presence of an ordinary readable input
establishes only the recorded file prerequisite, not truth or permission.
Declared connector records use DEL-07-02's source-mapped standing schema;
record/claim gaps, other-connector claims, advisory tiers and required routes
remain visible. This interprets quoted receiving files, not operational PEC
adoption or source truth. Decision needs remain unknown: the available decision
projection does not admit current native human-act validity, so `decided` alone
cannot satisfy a need. The existing decision workspace remains available.

The protected projection remains the sole source of App-named observations.
Legacy 0.1 statuses are shown only as historical recorded statements and do not
establish current native execution. Unsupported project-only observations
qualify readiness or make the associated item's state unknown. With unread or
conflicting coordination history, readable graph rows are labelled as a last
readable selection with unknown currentness, non-done rows are unknown and the
queue is incomplete. A known integration or external-result claim stays shown.
The current native dispatch producer and the independently joined fleet witness
remain separate, unsupplied obligations.

### 6.2 Native conversation-link recording

`native_conversation_links.rs` records actual source-issued `thread/fork` and
Continue-as `thread/start` results. It retains the selected project's existing
store association, physical project/store source and native home/configuration
source before dispatch. The original project activity custody is acquired under stable admission and
retained through a live unknown request, the known relation, both copies and its
mechanical outcomes, so another controller cannot close/export/dispose over owed
recording. Definite failure or a closed source with no retained response and no
write in progress releases custody with an explicit historical unknown/failure
limit; no timeout/dismissal or new retry lease is introduced. An already-retained
result or in-progress write stays distinct. The native conversation key is the actual thread ID
qualified by that stable home/source; generation, App session, RPC identity and
private request reference are observation context. Neither an objective label
nor a workflow/source-ref joins conversations. The native-links 0.2 schema has
an immutable `observationId`, first `observedAt`, source/destination thread IDs,
the frozen native home and the original RPC context, with no undertaking field.
The 0.1 schema and files remain byte-preserved quoted compatibility; their fields
do not enter the native relationship projection.

The real Continue-as Handoffs guard produces both original start metadata and a
private, non-deserializable source proof before the RPC. Fork retains its genuine
source-issued request before waiting. The observer validates the correlated
successful envelope and full pinned response shape. Unknown waits, definite
failure and closed unknown sources remain explicit status limits; tick reads only
retained original Host facts, with no second command, web polling, native resend,
operational admission or cold receipt mint. A genuinely known result first
observed after generation closure is historical evidence only. Missing original
source/association or an already closed/disposed project is a permanent recording
limit for that operation; native success is not rewritten as recording refusal.

Publication writes the governing store's `fleet/coordination.fleet.jsonl` first,
then copies the same frozen exact line to the co-written project log. App writes
share current store admission/import/terminal guards and writer ownership. Safe
held parent descriptors and nonblocking/no-follow regular single-link leaves,
complete schema/identity checks, prefix proof, source revalidation and ancestor
sync protect the append. Torn, unknown, conflicting or replaced sources are
refused without truncation, reassociation or automatic repair. Failed or uncertain
callbacks retain the original relation bytes, ID and first observation time.
Until the governing store line lands, its original bytes/ID/time and retry proof
are held by this App process only. Under existing AS03/SQ-Q quit semantics, quit
may proceed despite a ledger failure: quitting before that first durable line may
leave no Fleet relation record, and cold files cannot reconstruct the private
native request/handoff proof. Once the governing exact line lands, cold project-copy
recovery remains available. This adds no quit veto or new timeout/dismissal policy.

A separate 0.2 `recording_limit`/`recording_recovered` references that ID once per
meaning/phase transition. Later proved exact presence/sync does not rewrite the
original callback as success. Failure to record these mechanical rows stays in
status rather than recursively logging the logger's failure.

Tick also repairs a missing exact project copy from a healthy existing governing
source. Cold recovery quotes stored lines; it neither observes a new native fact
nor restores role, work state, CCE or current conversation authority. Existing
mechanical failure evidence gets a separate later-presence recovery row. New cold
copy work is not reserved while the project is closed or disposed; already owed
recording retains its original context. Stable unchanged sources reuse their
recovery basis, and completed copies retain compact status rather than a second
full history. Placement limits continue to qualify file provenance, including
agent-writable development stores.

Both Fleet versions remain outside the RS parser, index, capability and legacy
file-migration census (RS §13.7). Verified BagIt import/export includes their
whole payload bytes (RS §13.8), with the quoted-prefix limits in §6.1.
Fleet records are currently **unchained and unsigned**: per-process exact-prefix
proof catches known shrink/rewrite, but cold restart cannot authenticate a prior
valid prefix or detect a tail removed before its first read. BagIt includes the
whole Fleet payload bytes without claiming a Fleet chain head or signature. The
manual panel retains complete source records/order/limits, shows 0.2 relationships
and mechanical outcomes separately. The derived file workspace (§6.1a)
establishes no current native dispatch, child state or conversation relationship.
This implements the native-link contribution alongside the file workspace in
§6.1a. It does not supply the full native brief-to-child association or dispatch
producer in §4, an actual positive human-act witness or DEL-09-05's joined
native supplier examination.

The following rules retain the original writer/derived-reader specification
and prototype account. Current App consumption is bounded by §6.1–§6.1a; in
particular decision needs stay unknown, and file claims are not current native
execution. The ordinary-file brief/graph writer and native dispatch producer
are not supplied by these reader slices.

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
  not read or conform counts as not relied. So does a claim tagged with a
  connector other than the declared one (FV10-R9; closes RV2's
  "claim tagged with the other connector" limit). The other FV10-R9 limit
  stays recorded: a claim missing from the record cannot be detected by the
  consumer. That account is the record's own (PRC PR-6). The fact carries `connectorNeed`,
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
| Consumed (DEP-06-01-013, admitted) | DEL-01-01 | Selected development/definition pin 0.160.0 and its supplied protocol basis | Current supplier identity from HOSTING; actual observations retain their own pin | Qualification and full spawn-prompt association remain separately evidenced |
| Retained compatibility (DEP-06-01-011) | DEL-07-01 | Historical PEC format/coverage account | No current delivery, qualification or adoption prerequisite (PRD V4-CON-02) | Preserve quoted limitations; no reactivation |
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
| `chirality.fleet.record` | 0.1 (quoted compatibility; schema unchanged) | Agents and the person (FR-D1); the App writer for observed kinds | DEL-06-02 (views), DEL-09-05 (witness), DEL-09-11 (reconstruction, through its input set); **PEC: retained compatibility only**, no adopted Fleet coverage | A minor version adds optional elements or kinds; a reader that does not know them reads the rest and lists them as unread. A major version changes meaning. Before any consumer path relies on a change, the change is listed here with its consumers; PEC's retained compatibility account remains with DEL-07-01 (DEP-06-01-011) and creates no current delivery/adoption gate. A projection never governs this writer (V4-HI-63) |
| `chirality.fleet.record` native-links profile | 0.2 | Actual Rust App observer for source-issued Fork/Continue-as facts and mechanical recording outcomes; exact project copies | Rust Fleet reader/manual panel consume 0.1 and 0.2 separately: DEL-06-02 presents locally admitted native relationships and mechanical outcomes outside the graph-derived workspace. Imported 0.2 rows remain quoted, never native relationships. RS readers/index/capability and chain heads exclude both; BagIt import/export includes their complete bytes. DEL-09-05/09-11 consume their own identified evidence, without automatic qualification or native authority. PEC has no adopted Fleet coverage; no receiving adoption is inferred | New narrowly versioned profile, no retrospective rewrite of 0.1. Old readers may list these rows unread. Source-qualified native conversation IDs replace undertaking identity only for the new native profile under the quoted owner direction in §4; no graph or work-state derivation is added |

Example change (bounded): adding a `priority` element to work items is minor.
DEL-06-02 ignores it until it adopts the change. If PEC later consumes items,
DEL-07-01 states whether its coverage includes the element before anyone
relies on it.

## 9. Fixtures and verification (OUT-003; App regressions and historical prototype evidence)

Current product regression sources are `fleet_records_tests.rs` (native reader,
exact counterparts, protected prefix, import provenance and source changes),
`fleet_views_tests.rs` (graph/return/review/integration/input reconstruction),
`native_conversation_links_tests.rs` (source-issued native relationships and
recording recovery), and `app/tests/fleet-records.test.mjs` (presentation).
`records_package_identity_tests.rs` and `records_package_controls_tests.rs`
exercise recovery of the original import identity/control evidence that bounds
Fleet provenance, including missing prior derivatives and same-byte replacement
of an authoritative original. These use invented files and native peers; they
do not substitute for an actual supplier-qualified native association or the
joined two-delegation/human examination. The following prototype results retain
their original date, basis and limited standing.

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

Result on 2026-10-04, after FV10-R7/R8 and the FV10-R9 claim-connector case: 46/46 (42 before), including the
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
- FV10-R9 (P8x): PR-P8 without c3, with `route.needed` false, and with c1
  tagged `domains`/`admitted` is *unknown*, because c1 is never counted as
  relied.
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
| PEC envelope (OI-022), retained compatibility only | App consumer owner and PEC owner | No current PEC delivery/adoption requirement; current DEL-07-01 and PRD V4-CON-02 govern |
| Process placement of reader and writer (OI-008) | *Settled 2026-10-10 by the owner (FR-D3), now under the general OI-008 ruling:* the Rust host reads and writes; fixed folder `<project>/.chirality/fleet/`; no folder picker in v4.0 | — |
| Current graph file identity | App Fleet consumer adopts `chirality.app.exact-bytes.sha256/v1` in §6.1a, receiving the reviewed App definition from RS §6.2a; historical TEST VALUE selectors remain unsupported. Host/global algorithms stay open | Implemented consumer; independent implementation review applies |
| Delegation on a stock route: observed natively at 0.160.0 with limits (§4; one run). No spawn `collabAgentToolCall` item was shown, so AS-2's spawn item and spawn-prompt identity, and AS-1's carriage, are not observable from the parent there; the child came from `subAgentActivity`. The child-thread read does not supply it either: the trial witness found the spawn task delivered to the child as an inter-agent `agent_message` whose payload is `encrypted_content`, with no user message (§4; WR U-WR-25). So at 0.160.0 AS-2's prompt identity cannot be computed from Codex. Whether a later pin exposes a spawn item or the child's readable input is open | A later observation | Before VER-003 on a candidate |
