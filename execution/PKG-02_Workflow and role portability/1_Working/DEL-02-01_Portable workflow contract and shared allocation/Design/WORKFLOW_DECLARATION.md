# Portable workflow declaration, roles, source identity and shared allocation
- Contribution: DEL-02-01/WD-v0.1
- Status: DRAFT DEFINITION — proposed, unsupplied, not implemented, not accepted
- Serves: OUT-001, OUT-002, OUT-003 (map version), OUT-004 (fixture design only); REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006; AC-001…AC-007 by designed verification; VER-001…VER-007 (cases designed, none run)
- Basis: repo 6e18505e3; ScopeOfWork.md sha256 080d7f5a8e55d93c06f51e5332b53954deb03e0877b1ee49be3011e3de14a294; P/docs/PRD.md §2.2 (V4-HOST-05/06), §2.4 (V4-SHR-01…03), §4.1 (V4-WF-01…06), §4.2 (V4-ROLE-01…03), §4.3 (V4-EXE-03), §4.5 (V4-AUT-01…05), §4.7 (V4-REC-01…05); P/docs/ARCHITECTURE.md §1 (M-1, M-3, M-5), §4 (V4-ARC-14 and "left to the responsible host"), §5 (V4-ARC-20/21); P/docs/HOST_INTEGRATION.md §1, §2 (V4-HI-02…04), §3 (V4-HI-11/12), §4 (V4-HI-21…25), §5 (V4-HI-30…33), §6 (V4-HI-40…42), §9 (V4-HI-70/71); P/docs/EXAMINATION.md V4-EXM-10, -14, -21, -22; DECISION_BRIEF.html #d2, #d3, #d5; SCC-CASE-002 Case_Datasheet M1 rows; Open_Issues.csv OI-001, OI-002, OI-003, OI-013, OI-014, OI-018, OI-021. Root reuse sources read (not adopted): `workflows/WORKFLOW_TEMPLATE.md`, `workflows/*/execution.json` (66 companions surveyed), `workflows/catalog.yaml`, `workflows/catalog.schema.json`, `workflows/index.json`, `workflows/create-workflow/WORKFLOW.md`, `docs/SPEC.md` §9.1–9.8, `docs/AGENT_WORKFLOW_RUNTIME.md` (Method libraries and catalogs; Workflow packages).
- Consumed inputs: accepted basis only. DEL-03-01 (catalog C) referenced by accepted meaning (V4-HI-02 entry identity/version; DEL-03-01 REQ-002) — to be reconciled at V1. DEL-04-01 (act distinctions) referenced by accepted names from d3/V4-HI-30/33 — to be reconciled at V1. DEL-04-03 (record semantics) referenced by accepted meaning (V4-HI-70/71, V4-REC-04/05) — to be reconciled at V1. DEL-05-01, DEL-05-02, DEL-02-02, DEL-02-03, DEL-02-04 consumer needs taken from their accepted SoWs only; no contribution version received. SWBPIPE consumer needs (DEP-02-01-022): none received.
- Receivers: CASE-002 M1 row "Workflow-contract owner": DEL-02-02 (OUT-001, OUT-004; REQ-005; VER-004); DEL-02-03 (OUT-001, OUT-002; REQ-001, REQ-002, REQ-004; VER-001, VER-002, VER-004); DEL-02-04 (OUT-001, OUT-002; REQ-001, REQ-002, REQ-004; VER-001, VER-005); DEL-05-01 (OUT-001, OUT-004; REQ-005, REQ-007; VER-008); DEL-05-02 (OUT-001; REQ-001; VER-001); DEL-02-01 self-check (OUT-004; REQ-004, REQ-005; VER-004, VER-005). Later: DEL-03-04 host guide (W10), DEL-09-06 connected-activity contract (W9).

Companion: [EXAMPLES.md](EXAMPLES.md) (DEL-02-01/WD-EX-v0.1) carries the long
readable examples. This file is the definition; the examples illustrate it.

---

## 1. Reading this definition

**What it defines.** The meaning of a portable workflow's *declared part* and
its relation to the prose method; the four roles and the single host seat as
received by App and host consumers; workflow source identity and the
promised-versus-observed distinction; and the shared-contract responsibility
map (OUT-003) with each consumer need and each still-open allocation labeled.

**What it does not define.** It does not choose a wire format, field names,
file carriage of the declared part, JSON or TypeScript types, a parser
implementation, a content-identity algorithm, a transport (MCP or CLI),
persistence, process/thread placement or shared-component placement. It does
not define catalog entries (DEL-03-01), act kinds or policy classes
(DEL-04-01), record fields (DEL-04-03), the checkpoint hold machine or transfer
behavior (DEL-02-03), registration (DEL-02-02), role supply (DEL-02-04), loop
events (DEL-05-01) or panel interactions (DEL-05-02).

**Naming convention.** Element names in **bold small phrases** (for example
**expected input**, **required tool reference**) are *semantic element names*.
They are not wire names, keys, headings or type names. A later schema may name
them differently provided the meaning below is preserved.

**Normative words.** "Shall" marks a meaning this contribution proposes as
part of the contract; "settled" marks a distinction already accepted in the
basis and cited; `UNRESOLVED{…}` marks an open owner choice that is neither a
permission nor a default.

---

## 2. Settled distinctions this definition carries

These are carried from the accepted basis, not decided here.

| # | Settled distinction | Citation | Consequence for the declaration |
|---|---|---|---|
| S-A | A workflow is prose method guidance plus a declared part: expected inputs, host tools needed, checkpoints requiring a human act, returned outputs and evidence. | PRD V4-WF-01 | Five declared categories, prose retained (§3–4). |
| S-B | Workflows, skills and role guidance are ordinary open files (`WORKFLOW.md`, `SKILL.md`, `AGENTS.md`) readable by any capable harness; tool schemas stay open. | PRD V4-SHR-02; ARCH M-3 | The declared part must be readable without Chirality software (§3.2). |
| S-C | One workflow format and one set of four roles across the App and every host. | PRD V4-SHR-01, V4-ROLE-01 | No host-specific declaration dialect; host guidance specializes within the format (§5). |
| S-D | Source-qualified identity: project, user, bundled or host-supplied; a selection is never silently rebound to a same-named workflow from another source. | PRD V4-WF-03 | Four origin classes; collisions exposed (§6). |
| S-E | The product can check that a selected workflow's required tools exist in the current host and tell the person when they do not. | PRD V4-WF-04 | Required tools must be referenceable against the host catalog (§4.2). |
| S-F | At a declared checkpoint the required human act is requested and the run does not record it as done until the person performs it; checkpoints override autonomy. | PRD V4-WF-05; HI V4-HI-42 | Checkpoint hold is independent of granted autonomy (§4.3). |
| S-G | `success` means the operation ran; a submitted proposal reports "queued" until the host records acceptance and application. | HI V4-HI-25 | Success never satisfies a checkpoint (§4.3.4). |
| S-H | Applying a change, accepting an edit, marking work checked, approval and professional reliance are distinct; agents may prepare but must not represent an unperformed human act as performed. | PRD V4-AUT-03; HI V4-HI-30/31; d3 | Each checkpoint names one act kind; evidence of one kind satisfies no other (§4.3). |
| S-I | Proposals say "accept", never "approve". | HI V4-HI-33 | Checkpoint wording for proposal acceptance uses "accept" (§4.3.1). |
| S-J | A human act binds to identified content, scope and purpose and lapses visibly when that content changes. | PRD V4-REC-05; HI V4-HI-32 | A checkpoint names its subject so the act can be bound (§4.3.1, §4.3.3). |
| S-K | Only observed events are shown as having happened; unobserved outcomes are unknown. | PRD V4-EXE-03 | Declared outputs/evidence are promises; observation is separate (§4.6). |
| S-L | Nothing the agent produces is presented as certified, sealed, approved or code-compliant. | PRD V4-AUT-05 | Declared outputs cannot claim approval standing (§4.4). |
| S-M | Roles recede in hosts behind one agent seat and the selected workflow; each host carries its own workflows, skills and tools. | PRD V4-HOST-05/06 | Host seat semantics and host origin (§5, §6). |
| S-N | Roles are supplied additively; a bounded executor does not delegate; unenforced limits are stated, not implied. | PRD V4-ROLE-02/03 | Role compatibility is declared, not claimed as enforced (§4.7, §5). |
| S-O | Shared meaning does not prescribe a common executable service; shared implementation needs a concrete repeated responsibility; placement is open. | ARCH V4-ARC-20; PRD V4-SHR-03; d2; OI-014 | OUT-003 map records needs and leaves placement open (§9). |
| S-P | A run leaves a compact record linking host receipts rather than copying them. | PRD V4-REC-04; HI V4-HI-70/71 | Declared evidence is by reference to host-owned evidence (§4.5). |

---

## 3. The workflow package and its two parts

### 3.1 Parts

A portable workflow is one package whose entrypoint is `WORKFLOW.md` (S-B). It
has two parts with different jobs:

| Part | Job | Who reads it | Authority |
|---|---|---|---|
| **Prose method** | Explains purpose, applicability, method, branches, recovery, judgment and handoff in words. | People and agents. | Method guidance; it grants no permission (Root `create-workflow`, retained). |
| **Declared part** | States, in a form a product can observe, what the method expects, needs, stops for and returns. | People, agents and product consumers (requirement check, checkpoint hold, records, panel). | A declaration of the method's expectations. It is not evidence that any expectation was met and grants no host permission. |

Both parts are required for a *declared* workflow. The prose is not
subordinate to the declared part: where they disagree, the consumer reports
the inconsistency (§11 FB-07); it does not silently prefer either.

### 3.2 Readability obligations (OUT-001, OUT-002; REQ-001, REQ-002)

- **R-1** The declared part shall be readable as ordinary text by a person
  opening the package in an ordinary editor, without Chirality software,
  generated indexes or a running host (S-B).
- **R-2** Every declared element shall carry, or sit beside, a short
  human-readable statement of its meaning; an opaque reference alone (for
  example a catalog operation identity) is insufficient without a readable
  purpose line.
- **R-3** The declared part shall live inside the package and travel with it;
  a derived index, registry or host database may *reflect* it but is not its
  authority (Root `index.json` principle, retained; PRD V4-PM-06 analogue).
- **R-4** The physical carriage of the declared part (inside `WORKFLOW.md`
  front matter, a delimited body section, or a companion file within the
  package) is `UNRESOLVED` (U-01). Every option must satisfy R-1…R-3.

### 3.3 Declaration contract version

- **declaration contract version** — identifies which version of this
  declaration meaning the declared part is written against, so a consumer can
  tell whether it understands every element. Representation unselected.

### 3.4 Absent, partial and unrecognized declared parts

| Condition | Consumer meaning (all consumers) |
|---|---|
| No declared part (all current Root bundled workflows; any prose-only package) | The workflow is **undeclared**. It remains a readable, selectable method. Consumers shall report "requirements undeclared", never "no requirements": the required-tool check cannot pass, checkpoints cannot be product-held, and outputs/evidence have no declared promise. |
| Declared part present, a category omitted | That category is **undeclared** for this workflow, distinct from a category **declared empty** (an explicit statement that none are expected). Only "declared empty" supports a statement such as "this workflow declares no checkpoints". |
| Unrecognized element or newer contract version | Preserve it unchanged; report it as unrecognized. An unrecognized element in the required-tool or checkpoint category shall make the corresponding check result **not established**, not pass. |

---

## 4. Declared-part meaning

### 4.1 Expected inputs (SOW-042)

An **expected input** states what the method needs in order to begin or to
proceed at a stage.

| Element | Meaning |
|---|---|
| **input name** | Local name, unique within the workflow; used by the prose and by other declared elements. |
| **input meaning** | Readable statement of what the input is and why the method needs it. |
| **input kind** | One of: a host object or view obtained through a catalog read (see **required tool reference**); a file or document supplied to the run; a value or choice supplied by the person; an output of another identified workflow run. |
| **necessity** | Required, or optional with the effect of its absence stated in words. |
| **quality or basis requirement** | What must hold for the input to be usable (e.g., "read on the current model revision"). Where the input is a host read, the relied-on basis is the read-basis descriptor supplied by DEL-03-01 (workspace identity, generation, model revision, canonical content identity; V4-HI-11). This declaration names the need for a basis; it does not define the descriptor. |
| **stage** | Where in the method the input is needed, anchored to the prose. |

An expected input is a need, not a fetched value. Whether it was supplied, and
on what basis, is an observation for the run record (§4.6).

### 4.2 Required tools (SOW-043, SOW-039)

#### 4.2.1 Two tool classes

| Class | What it refers to | Supplier of meaning |
|---|---|---|
| **host operation requirement** | An operation in a host's capability catalog, referenced by the catalog's operation identity (and, where needed, version compatibility). | DEL-03-01 catalog C: identity and version meaning (V4-HI-02). The reference is **opaque** here: this contract neither parses nor defines catalog identities. |
| **harness capability requirement** | A capability of the agent's harness that is not a host catalog operation (e.g., file writing or native delegation in the App's Codex). | `UNRESOLVED` (U-08): how such capabilities are named portably. |

A workflow designed for a host names host operations. An external agent (the
App's Codex through a host's MCP or CLI surface, V4-HI-50) reaches the *same*
catalog operations; the declaration still references the catalog identity,
never an adapter-specific tool name. Transport is not selected (DEL-03-03).

#### 4.2.2 Elements of a required tool reference

| Element | Meaning |
|---|---|
| **tool reference** | Opaque reference to a DEL-03-01 operation identity (host class) or to a harness capability (harness class). |
| **version compatibility** | Optional statement of which operation versions the method was written against. Its expression is `UNRESOLVED` pending C's version meaning (U-07). |
| **purpose of use** | Readable: what the method uses the operation for. It does **not** restate the operation's human-act/autonomy class; that class belongs to the catalog entry drawn from adopted policy (V4-HI-02; DEL-03-01 REQ-002) and to the person's autonomy setting (V4-HI-40). |
| **necessity** | Required, or optional with the stated fallback or limitation when absent (Root `create-workflow` "practical fallback or limitation", retained). |
| **stage** | Where in the method the tool is used. |

#### 4.2.3 Requirement is not restriction

Root `execution.json` `tools.capabilities` and `tools.commands` are
**restrictions**: a ceiling that intersects outer policy ("empty restriction
lists deny rather than grant"; AGENT_WORKFLOW_RUNTIME.md). V4-WF-01 "the host
tools it needs" is a **requirement**: a floor the current host must meet. They
shall remain distinct elements. A consumer shall not read a restriction list
as a requirement list or the reverse (FB-05; EXAMPLES E6).

#### 4.2.4 Check outcomes a consumer may report (meaning only)

The required-tool check itself is DEL-02-03's behavior (REQ-001 there). This
contract supplies the vocabulary it compares against:

| Outcome | Meaning |
|---|---|
| **present** | The referenced operation exists in the current host's catalog and is exposed to the acting surface. |
| **missing** | Not in the catalog, or not exposed to this surface. Reported to the person with the requirement's purpose line (S-E). |
| **version mismatch** | Present, but outside the declared version compatibility. |
| **present, currently unavailable** | Present but its preconditions do not hold now; reported with the catalog's unavailable reason (V4-HI-04). This is a run-time condition, not a missing requirement. |
| **not established** | The requirement cannot be evaluated (undeclared, unrecognized element, catalog unreadable, reference unresolved). Never reported as present. |

Whether a newly added catalog operation becomes available on all three
surfaces without separate work is `UNRESOLVED{OI-003}`; the declaration does
not assume it (U-16).

### 4.3 Checkpoints requiring human acts (SOW-044; REQ-003)

#### 4.3.1 Elements

| Element | Meaning |
|---|---|
| **checkpoint name** | Stable within the workflow's revision; identifies the checkpoint across interruption, replay and adaptation (DEL-02-03 REQ-002). |
| **required act kind** | Exactly one human act kind, named by its DEL-04-01 accepted name. Accepted-basis names used in this draft: *accept a proposed edit* (d3 "accepting an edit"; V4-HI-33 wording "accept"), *mark checked* (d3; V4-HI-30), *approve* (V4-HI-30; V4-CON-05 design-candidate approval), *accept professional reliance* (d3; V4-AUT-05). Reconcile with DEL-04-01 v0.1 at V1 (U-04). |
| **subject** | What content the act concerns (a declared output, a proposal, identified host rows, a report), stated so a recorder can bind the act to identified content (S-J). The binding itself (content identity, lapse) is DEL-04-03's. |
| **scope** | The extent of the subject covered (e.g., one row, several rows, a whole batch — V4-HI-41 granularity). |
| **purpose** | Why the act is requested at this point, in words the person reads when asked. |
| **actor requirement** | Who must perform it: "the person" by default; "the accountable professional" where the act kind is professional reliance (V4-AUT-05). The declaration names a class, never an identity. |
| **position** | Where in the method the run holds, anchored to the prose stage. |
| **on negative decision** | What the method does if the person decides against (e.g., rejects a proposal, V4-HI-23 "rejected"): stop, return to a named stage, or proceed on a stated branch. Absent this element, the run stops at the checkpoint; it never proceeds as if the act were positive. |
| **expected act evidence** | Reference to the act record expected (DEL-04-03 human-act record meaning). A declaration, not a record. |

#### 4.3.2 What a checkpoint is and is not

- A checkpoint **names** a human act that the run waits for. It does not
  perform, record or imply the act.
- A checkpoint may name only a **human** act kind. Naming *propose*, *apply*,
  an agent's non-mutating check or any execution outcome as a checkpoint's
  required act is invalid (FB-03). An agent's check findings are not a human
  Checked act (V4-EXM-21).
- A checkpoint is not a routine tool permission prompt. Treatment of
  classifier-based routine permissions is `UNRESOLVED{OI-002}` and shall not
  be expressed as, or satisfied by, a checkpoint (U-06).
- A checkpoint does not decide whether the act kind is always reserved to the
  person outside checkpoints; that is `UNRESOLVED{OI-001}` (U-05). Inside a
  declared checkpoint the run waits for the person's act regardless of
  autonomy (S-F).

#### 4.3.3 Independence rules

- **I-1 One kind, one evidence.** A checkpoint is satisfied only by evidence
  of its own act kind, by a qualifying actor, on its subject and scope, on the
  content currently bound. Evidence of another act kind satisfies nothing
  here (S-H).
- **I-2 No success inference.** Operation success, a queued proposal, a
  receipt of application or a completed agent check supplies no human act
  (S-G; d3 "a tool's success must not become an invented human act").
- **I-3 No synthetic ordering.** The contract imposes no rule that proposal
  acceptance must precede checking, approval or reliance. An independently
  evidenced act counts on its own evidence. A workflow author may place
  checkpoints in a method order; that order is the workflow's visible declared
  method, not an ordering inferred from act kinds. The proposal lifecycle's own
  accepted → applied sequence (V4-HI-23) is an operation lifecycle, not a
  checkpoint ordering rule.
- **I-4 Lapse returns the hold.** If the bound content changes after the act,
  the act lapses visibly (S-J) and the checkpoint is again awaiting its act
  for the changed content; the old act is not carried onto new content.
- **I-5 Faithful recording.** A recorder (App, host, agent) may faithfully
  record an act the person actually performed; the recorder does not become
  the decision actor (DEL-02-02 REQ-006; DEL-02-03 REQ-003).

#### 4.3.4 Checkpoint disposition vocabulary (meaning only)

For consumers presenting or recording a run; the state machine is DEL-02-03's.

| Disposition | Meaning |
|---|---|
| **not reached** | The run has not arrived at the checkpoint. |
| **awaiting act** | Reached; the act is requested; the run holds. |
| **performed** | Evidence of the required act, by a qualifying actor, on current bound content, exists (with its record reference). Includes a negative decision where the act kind has one. |
| **lapsed** | A performed act's bound content changed; the checkpoint is awaiting act again. |
| **unknown** | Whether the act was performed cannot be established (e.g., record unavailable after interruption). Never presented as performed (S-K). |
| **run stopped** | The run ended at or before the checkpoint without the act. |

### 4.4 Returned outputs (SOW-045)

| Element | Meaning |
|---|---|
| **output name / meaning** | Local name and readable description. |
| **output form** | One of: a change to host objects (always through the host's one route — proposal or direct application under granted autonomy, V4-HI-20…23); a file or document; a report or message to the person; an input to another workflow. |
| **destination** | Where the output goes (host tables/views; the project; the conversation). Host-changing outputs appear in the host's own views; there is no agent-private surface (V4-HOST-04). |
| **promised standing** | The standing the method expects the output to carry, drawn from the non-approval vocabulary: e.g., *proposed (queued)*, *applied with receipt*, *agent-prepared, unchecked*, *agent-checked (non-mutating)*. An output shall never promise *approved*, *certified*, *sealed* or *code-compliant* standing (S-L). A human-act standing (e.g., *checked by the person*) can only be promised *conditional on a named checkpoint*. |
| **gating checkpoint** | Optional reference to the checkpoint whose act the output's promised standing depends on. |

### 4.5 Returned evidence (SOW-045)

| Element | Meaning |
|---|---|
| **evidence name / meaning** | What the evidence shows and for which output or checkpoint. |
| **evidence kind** | One of: host receipt reference; read-basis reference relied on (V4-HI-11/21); check result reference; human-act record reference; run record reference. |
| **by reference** | Host receipts, hashes and origin marks remain host-owned; declared evidence names a link, not a copy (S-P). |
| **supports** | Which output(s) or checkpoint(s) the evidence supports. Evidence for one act supports no other (I-1). |

### 4.6 Promised versus observed (REQ-004; AC-004)

The declared part states **promises**. Observations belong to the run record
(DEL-04-03) and host evidence. Consumers shall keep them distinguishable.

| Declared promise | Observed counterpart | Observation owner | Absent observation means |
|---|---|---|---|
| expected input | input actually supplied, with its basis | run record (DEL-04-03); host read basis (DEL-03-01) | "not supplied" / "basis unknown" — never inferred from the declaration |
| required tool reference | requirement check outcome at run start and actual operations requested/outcomes | DEL-02-03 check; run record | "not established" |
| checkpoint | disposition and act record reference | DEL-02-03 hold; DEL-04-03 act record | "unknown" or "awaiting act" — never "performed" |
| output with promised standing | produced output and its actual standing (queued, applied with receipt, outcome unknown …) | host (receipts, standing); run record | "not produced" or "outcome unknown" (S-K) |
| evidence | linked receipt / record actually present | host; run record | "missing" — a declared evidence item without its observed counterpart is never a pass |

### 4.7 Compatible roles and restrictions (retained from Root)

| Element | Meaning |
|---|---|
| **compatible roles** | Which of the four roles the method is written for (Root `compatible_roles`, retained). Omission inherits compatibility; it never expands a role. |
| **tool restriction** | Optional ceiling narrowing the tools the method may use (Root `tools`, retained as a *restriction*, distinct from §4.2). |
| **enforcement statement** | None in the declaration. Metadata never proves enforcement (Root, retained; S-N). Where a harness or host cannot enforce a restriction, the consumer reports it as instruction-asserted. |

A workflow requiring delegation is compatible only with a role and seat that
can delegate (Root runtime: "A workflow requiring delegation belongs with a
compatible manager"; S-N). In a host seat without a delegation facility such a
workflow is reported **unsupported**, not silently run without delegation.

---

## 5. The four roles and the single host seat (SOW-021, SOW-022; REQ-001; AC-001)

### 5.1 Common meaning (settled)

| Role | Meaning (V4-ROLE-01) |
|---|---|
| HELP_HUMAN | Alignment with the human |
| HELPS_HUMANS | Design |
| WORKING_ITEMS | Managed execution |
| TASK | Bounded execution; does not delegate (V4-ROLE-03) |

No fifth role: a domain expression such as the SWB Piping Designer specializes
context, tools and workflows within these roles (V4-ROLE-03; V4-CON-05).
Role guidance is supplied additively, never replacing the harness's own
instructions (V4-ROLE-02); supply itself is DEL-02-04's.

### 5.2 Expressions

| Aspect | Chirality App | Host application (e.g., SWBPIPE) |
|---|---|---|
| Role presence | Person selects a role (DEL-02-04). | Roles recede behind **one agent seat** and the selected workflow (S-M). The host need not present a role choice; portability does not impose the App's role-selection UI (REQ-001). |
| Guidance files | Product `AGENTS.md` plus role guidance (Root/App). | The host's own `AGENTS.md` and `SKILL.md` files for its work (V4-HOST-06), open and readable (S-B). Distribution/adoption mechanism is `UNRESOLVED{OI-018}` (U-14). |
| Workflows | Project, user, bundled; host-supplied when opened in App (V4-WF-06). | The host's own library (origin *host*); App-authored workflows carried in and adapted (V4-WF-06). |
| Tools | Codex native tools; host operations through an external surface (V4-HI-50). | The host's capability catalog (V4-HI-01). |
| Delegation | Native delegation for roles permitted to delegate. | Seat's delegation facility is host-defined; absent it, delegation-requiring workflows are unsupported (§4.7). |

### 5.3 What the single seat must still carry

- **SEAT-1** Which role meaning the seat is operating under for a run shall be
  determinable from the host's guidance and the selected workflow's
  **compatible roles**, and recorded with the run (run record meaning is
  DEL-04-03's). If it cannot be determined, the record says so (unknown), not
  a guessed role.
- **SEAT-2** The mapping from the host's single seat to the four role meanings
  (e.g., whether a host seat may act as HELPS_HUMANS when refining a workflow,
  or only as a bounded executor of the selected workflow) is
  `UNRESOLVED` (U-09). Options for the owner are listed there; this draft does
  not pick one.
- **SEAT-3** Receding does not remove the distinctions: the seat's acts remain
  execution; the person's acts remain the person's (S-H).

---

## 6. Source identity (REQ-001, REQ-004; AC-004)

### 6.1 Elements of a source-qualified workflow identity

| Element | Meaning |
|---|---|
| **kind** | Workflow (distinct from skill; Root `kind`, retained). |
| **origin class** | *project*, *user*, *bundled* or *host* (S-D). *host* is new relative to Root (§7). |
| **source root** | Which library within that class: the project root, the user's library, the App bundle and its release, or the host application and its library. Root's `sourceRootId` meaning is retained; values are unselected. |
| **name** | Package name, matching its folder (Root rule retained, §7). |
| **revision** | Identity of the exact package content selected (all files in the package). Algorithm and canonicalization `UNRESOLVED` (U-03). A name plus origin without a revision identifies a *library slot*, not selected content. |
| **derived-from** | For a carried or adapted workflow (V4-WF-06): the full identity (all five elements above) of the workflow it was adapted from. Adaptation creates a new identity; it never edits the original's history. |

### 6.2 The identity chain: promised versus observed

Different facts, each with its own evidence (aligned with DEL-02-04 REQ-004 and
DEL-02-02 REQ-005; V4-EXM-14 "selected/resolved bytes, what was actually
supplied and provider-adopted, and observed behavior are separate"):

| Link | Fact | Typical owner of evidence |
|---|---|---|
| **listed** | A library/catalog reports the workflow exists. | Discovery (DEL-02-02 App; host library) |
| **selected** | The person (or brief) chose a source-qualified identity. | Selection (DEL-02-02; host panel DEL-05-02) |
| **resolved** | That identity resolved to specific revision content. | Resolver (placement open, §9) |
| **supplied** | Those bytes were actually supplied to the agent/loop. | App: DEL-02-04 / DEL-01-01; host: host loop (external) |
| **adopted by provider** | The model/harness took it up. Often unobservable; then "unknown". | Not observable in general; stated as a limit |
| **observed behavior** | What the run actually did. | Run record (DEL-04-03); host evidence |

A matching name or filename at two links establishes nothing about the
others (AX-002: "not inferred from a matching filename").

### 6.3 Collision and rebinding rules

- **C-1** Every discovery that finds more than one origin for a name exposes
  all origins (Root runtime, retained).
- **C-2** A selection holds its full identity including revision; later
  discovery of a same-named workflow in any origin (including a
  higher-precedence one) is reported as a collision and never rebinds the
  selection (S-D).
- **C-3** Only an explicit new selection by the person changes what is
  selected; that is a new selection event, not a rebinding.
- **C-4** A changed revision under the same origin/name is a different
  revision. Whether a selection follows a new revision of the *same* origin
  slot or stays pinned to the selected revision is a selection policy owned by
  DEL-02-02 (App) and the host; the identity chain shall make which occurred
  visible (U-10).
- **C-5** Where *host* sits in unqualified-name precedence (Root: project,
  then user, then bundled) is `UNRESOLVED` (U-10). Source-qualified selection
  makes precedence irrelevant to correctness; precedence only affects the
  default offered.

Examples: EXAMPLES E3 (carried and adapted), E4 (same-name collision).

---

## 7. Root conventions: keep, change or leave open

Root material is a reuse source, not v4 authority (PRD V4-CST-04;
ARCH §5 "Historical placement is not v4 authority").

| Root convention (source) | v4 declaration | Why |
|---|---|---|
| Package = immediate folder containing `WORKFLOW.md`; name matches folder (SPEC §9.3; runtime "Workflow packages") | **Keep** | Satisfies V4-SHR-02 open files; existing App/Root consumers already read it. |
| Name rule: 1–64 lowercase letters/digits in hyphen-separated segments (`catalog.schema.json` `workflowName`; `create-workflow`) | **Keep as reuse candidate**; confirm in OUT-004 fixtures | Source compatibility with existing libraries; no v4 reason to differ. Confirmation is a fixture result, not assumed. |
| YAML front matter with `name` and `description` (`WORKFLOW_TEMPLATE.md`) | **Keep** `name`/`description` meaning; whether the declared part also lives there is **open** (U-01) | Description supports selection; declared-part carriage is a representation choice. |
| Body is free prose, no prescribed headings (`WORKFLOW_TEMPLATE.md`; `create-workflow`) | **Keep** | V4-WF-01 retains prose method guidance. |
| Inputs, outputs, checks, human checkpoints stated only in prose ("Make these facts identifiable, using whatever prose") | **Change**: add the declared part; keep the prose | V4-WF-01 requires a declared part a product can observe (SOW-042…045). |
| `execution.json` `compatible_roles` | **Keep** meaning (§4.7) | Four roles are common (S-C). |
| `execution.json` `tools.capabilities` (Chirality runtime capability names, e.g. `read`, `write`, `delegate_agent`) | **Keep as restriction only**; **do not** reuse as required tools | Restriction ≠ requirement (§4.2.3). v4 required tools reference catalog C identities. |
| `execution.json` `tools.commands` (legacy `<interpreter> tools/path:<glob>`) | **Leave out of the portable declaration**; remains Root compatibility | Host- and repository-specific; not portable across hosts. |
| "Metadata never proves host enforcement"; instruction-asserted boundary reported | **Keep** | S-N; V4-ROLE-03. |
| Origin classes `project`/`user`/`bundled` and `sourceRootId` (`catalog.schema.json`; `index.json`) | **Change**: add *host* origin; add **revision** and **derived-from** to identity | V4-WF-03 host-supplied origin; V4-WF-06 carried/adapted revisions; REQ-004 origins *and revisions*. |
| Unqualified precedence project → user → bundled | **Leave open** for *host* position (U-10) | Not decided by the basis. |
| Source-qualified identity `kind`, `source`, `sourceRootId`, `name`; no silent rebinding; all collision origins exposed | **Keep** | Same as V4-WF-03. |
| `selected-context` returns bodies "with fingerprints and selection order" | **Keep the idea** as **revision** at selection; algorithm open (U-03) | Revision needed for promised-vs-observed. |
| Drafts in `.chirality/workflow-drafts/`, registration via Workflows panel, no overwrite | **Not part of this contract**; DEL-02-02 owns | V4-WF-02 journey is DEL-02-02's; this contract only requires draft vs registered to be distinguishable from identity. |
| `catalog.yaml` navigation (`core`/`specialist`/`superseded`, `centralWorkflowNames`) | **Leave out**; library-maintenance concern | Navigation is not declaration meaning. |
| Derived `index.json` | **Keep principle**: derived, never authority | R-3. |
| Legacy `TaskSkill` adapter, `legacy-methods.json` aliases | **Leave out** | Root compatibility; not a v4 portable meaning. |
| Four-section role files `AGENT_<ROLE>.md` (SPEC §9.1) | **Leave to DEL-02-04 / OI-018** | V4-SHR-02 names `AGENTS.md`; exact role-guidance structure and distribution are not this contract's. |

---

## 8. What each receiver receives from this contribution

| Receiver (CASE-002 M1) | Receives from WD-v0.1 | Expected check at V1 |
|---|---|---|
| DEL-02-02 workspace (OUT-001, OUT-004; REQ-005; VER-004) | §3 package parts and undeclared states; §6 identity, chain and collision rules; §4.6 promised-vs-observed | Can the workspace show the declared part, identity and missing-capability/checkpoint/unknown conditions without redefining them? |
| DEL-02-03 execution (OUT-001, OUT-002; REQ-001, -002, -004; VER-001, -002, -004) | §4.2 requirement references and outcome vocabulary; §4.3 checkpoint elements, independence rules and disposition vocabulary; §6.1 derived-from | Sufficient for missing-tool check, checkpoint hold and transfer trace? |
| DEL-02-04 roles (OUT-001, OUT-002; REQ-001, -002, -004; VER-001, -005) | §5 role meanings, seat, compatible roles; §6.2 identity chain | Role identity and supply chain consistent with its source/byte/limit account? |
| DEL-05-01 loop (OUT-001, OUT-004; REQ-005, REQ-007; VER-008) | §4.3 checkpoint meaning for the checkpoints subject of the loop boundary; §4.2 catalog references; §9 allocation rows OI-013 | Enough meaning for a loop checkpoint event without choosing wire fields? |
| DEL-05-02 panel (OUT-001; REQ-001; VER-001) | §6 identity and collision for workflow selection; §4.3 checkpoint wording ("accept", S-I); §4.4 output standing | Workflow-selection and checks interactions traceable to these meanings? |
| DEL-02-01 self (OUT-004; REQ-004, -005; VER-004, -005) | Whole contribution | Verification cases §13 |

Expected **from** suppliers (none received at v0.1):

| Supplier | Expected element | Used in | If absent |
|---|---|---|---|
| DEL-03-01 (C) | Operation identity and version meaning; exposure-to-surface meaning; unavailable reason; read-basis descriptor | §4.1, §4.2 | References stay opaque; version compatibility stays U-07 |
| DEL-04-01 | Accepted act-kind names and which are human acts; actor classes | §4.3.1 | Accepted-basis names used; reconcile at V1 (U-04) |
| DEL-04-03 | Human-act record meaning (actor, recorder, kind, content identity, scope, purpose, lapse); run record carrying workflow identity/revision and role meaning | §4.3, §4.5, §4.6, §5.3, §6.2 | Referenced by accepted meaning (V4-HI-70/71, V4-REC-05) (U-11) |
| DEL-05-01 | Loop checkpoint/event needs | §9 rows | Need taken from SoW REQ-005/007 only |
| DEL-05-02 | Panel workflow-selection/check needs | §9 rows | Need taken from SoW REQ-001/004 only |
| SWBPIPE owner (external, via human relay) | Host library origin/root, host seat conduct, host checkpoint presentation needs | §5, §6, §9 | Nothing assumed; U-09, U-17 |

---

## 9. Shared contract/component responsibility map (OUT-003; REQ-005; AC-005)

Column meanings: **Consumers** = named consuming owners; **Repeated
responsibility** = the work each would otherwise repeat; **Maintenance
rationale** = consequence of sharing versus local implementations (d2
alternatives: local implementations need conformance work; a library couples
releases; a service adds process/availability/upgrade coordination);
**Candidate** = a *candidate* reusable type or component, named semantically,
not a decision; **Confirmation** = actual owner response; **Placement** =
decided or open.

No owner confirmation has been received for any row. "Need source" states
whether the need comes from a received contribution or only from an accepted
SoW.

| # | Contract part (semantic owner) | Consumers and need source | Repeated responsibility | Maintenance rationale | Candidate | Confirmation | Placement |
|---|---|---|---|---|---|---|---|
| A-1 | Declared-part meaning (DEL-02-01) | DEL-02-02, DEL-02-03, DEL-05-01, DEL-05-02, host loop/panel (external). SoW only. | Each reads the same five categories and undeclared states. | Divergent readers would disagree on "undeclared" vs "empty" and on checkpoint meaning — a correctness risk, not only duplication. | Shared **declared-part reading** type(s) and a parser/validator; conformance fixtures (OUT-004) regardless. | None | `UNRESOLVED{OI-014}` |
| A-2 | Source-qualified identity and chain (DEL-02-01) | DEL-02-02, DEL-02-03, DEL-02-04, DEL-04-03, DEL-05-02, host library (external). SoW only. | Represent origin/root/name/revision/derived-from; detect collisions; never rebind. | Identity drift across consumers breaks V4-WF-03 silently; a shared type is low-coupling. | Shared **workflow identity** type; collision-report meaning. Resolver placement separate. | None | `UNRESOLVED{OI-014}` |
| A-3 | Checkpoint meaning (DEL-02-01) with act kinds (DEL-04-01) | DEL-02-03 (hold), DEL-05-01 (loop checkpoint), DEL-05-02 (panel checks), DEL-04-03 (records), host (external). SoW only. | Name act kind, subject, scope; apply independence rules I-1…I-5. | Independence rules are easy to erode locally (success→act); a shared definition plus shared negative fixtures limits that. | Shared **checkpoint declaration** type; shared negative fixtures. Hold machine stays DEL-02-03. | None | `UNRESOLVED{OI-014}` |
| A-4 | Checkpoint hold state machine (DEL-02-03) | App run (DEL-02-03), host loop (DEL-05-01 receiving; external construction). SoW only. | Wait/advance/lapse/unknown behavior. | Shared *execution* here couples App and host loop lifecycles; d2 requires a concrete shared stateful responsibility first. | Possibly a shared component; not proposed at v0.1. | None | `UNRESOLVED{OI-014}`; host side `UNRESOLVED{OI-013}` |
| A-5 | Required-tool reference and check vocabulary (DEL-02-01 references; DEL-03-01 identities) | DEL-02-03 (check), DEL-02-02 (display), DEL-05-02 (panel), host (external). SoW only. | Compare references to the current catalog; report outcomes §4.2.4. | Reference meaning must match C exactly; the checker's code may stay local per consumer. | Shared **requirement outcome** vocabulary type; checker placement open. | None | `UNRESOLVED{OI-014}` |
| A-6 | Role meaning and compatible roles (DEL-02-01 meaning; DEL-02-04 supply) | DEL-02-04, DEL-02-03, host seat (external). SoW only. | Name four roles; read compatible roles; report unsupported delegation. | Tiny, stable meaning; shared constant set is cheap; enforcement stays per harness. | Shared **role identity** set. | None | `UNRESOLVED{OI-014}` |
| A-7 | Human-act and run record (DEL-04-03) | All above. | — (semantic owner is DEL-04-03) | Recorded here only to keep the owner visible. | Owned by DEL-04-03's allocation. | n/a | DEL-04-03 / `UNRESOLVED{OI-014}` |
| A-8 | Catalog entry and read basis (DEL-03-01) | All above. | — (semantic owner is DEL-03-01) | As A-7. | Owned by DEL-03-01's allocation. | n/a | DEL-03-01 / `UNRESOLVED{OI-014}` |
| A-9 | Host loop use of declarations (external construction; DEL-05-01 receiving) | Host loop. SoW only. | Parse declared part in the host; emit checkpoint events; persist runs. | Loop placement/parsing/persistence are host choices. | None proposed. | None | `UNRESOLVED{OI-013}` |
| A-10 | Panel workflow selection and checks (external construction; DEL-05-02 receiving) | Host panel; possibly App views. SoW only. | Present selection, identity, collisions, checkpoint requests with "accept" wording. | Reusable components only on agreed repeated purpose (DEL-05-02 OUT-004). | Possibly shared presentational components; not proposed at v0.1. | None | `UNRESOLVED{OI-014}`, `UNRESOLVED{OI-013}` |

Allocation result at v0.1: the required map exists with every row's consumer
and open placement; **no** common implementation or service is proposed, and
no row is represented as agreed (AC-005).

---

## 10. Excluded acts and their owners (REQ-006; AC-006)

| Act excluded from DEL-02-01 | Owner | Receiving interface in this contract |
|---|---|---|
| Catalog-semantic definition (identity, version, availability, standing, read basis) | DEL-03-01 | §4.2 opaque references; §4.1 basis need |
| Operation-policy contract definition; carrying adopted policy | DEL-04-01 | §4.3.1 act-kind names; §4.2.2 "does not restate class" |
| Deciding reserved acts / classifier permissions | Owner with App/SWB contract owners (OI-001, OI-002) | U-05, U-06 |
| Human-act and run-record field definition; record implementation | DEL-04-03 | §4.3.1 expected act evidence; §4.5; §4.6; §5.3 |
| Loop receiving design | DEL-05-01 | §8, §9 A-9 |
| Panel receiving design | DEL-05-02 | §8, §9 A-10 |
| App workflow workspace and registration construction | DEL-02-02 | §6.3 C-4/C-5; §7 drafts row |
| Execution/checkpoint hold/transfer implementation | DEL-02-03 | §4.2.4, §4.3.4, §6.1 derived-from |
| Role selection and supply implementation | DEL-02-04 | §5 |
| Host catalog, domain validation/application, receipts, loop, panel, tables, views | External SWBPIPE implementation owner | §4.5 by reference; §5.2 host column |
| Offering/recording/presenting a human act in a host | Host (external) | §4.3.3 I-5 |
| Performing checking, acceptance, approval, reliance | The person; professional assertions by the accountable professional | §4.3 (declaration names, never performs) |
| Shared placement decisions | App/shared contract owners (OI-014); with SWB implementation owner (OI-013) | §9 |

---

## 11. Failure behavior (consumer-facing meaning)

| ID | Condition | Required behavior |
|---|---|---|
| FB-01 | Declared part absent or a category omitted | Report **undeclared** (§3.4); never "none". |
| FB-02 | Declared part unreadable as text or malformed | Workflow stays a prose method; declared part **not established**; report the defect; no partial interpretation that could pass a check. |
| FB-03 | Checkpoint names a non-human act kind or no act kind | Invalid checkpoint; report; the run cannot treat it as satisfied by any execution outcome. |
| FB-04 | Checkpoint names an act kind not recognized by the current DEL-04-01 version | Preserve; disposition can only become **performed** through evidence of that named kind; consumers without the name report **not established** rather than substituting a nearby kind. |
| FB-05 | Root `tools` restriction present, required tools undeclared | Required-tool check **not established**; restriction still honored as ceiling. |
| FB-06 | Tool reference does not resolve against the current catalog | **missing** (or **not established** if the catalog is unreadable); never silently dropped. |
| FB-07 | Prose and declared part disagree (e.g., prose describes a human checkpoint the declared part lacks) | Report inconsistency to the person; do not auto-add or auto-remove a checkpoint. |
| FB-08 | Selected revision no longer resolvable (deleted or changed) | Report; do not substitute the current same-named content; the run record keeps the selected identity. |
| FB-09 | Collision discovered after selection | Report all origins; keep selection (C-2). |
| FB-10 | Output promises approval/certified standing | Invalid declaration element (S-L); report. |
| FB-11 | Declared evidence has no observed counterpart after the run | **missing**; never a pass (§4.6). |
| FB-12 | Role meaning of host seat undeterminable | Record **unknown** role meaning (SEAT-1). |

---

## 12. UNRESOLVED

| ID | Item | Owner | Point of need | Effect on this definition |
|---|---|---|---|---|
| U-01 | Physical carriage of the declared part (front matter, delimited body section, or package companion file) | App/shared workflow-contract owner (DEL-02-01), with consumer confirmation | Before OUT-002 schema and OUT-004 parser fixtures | Examples use an illustrative readable rendering, labeled as such. Options: (a) front matter — one file, but YAML becomes long and less readable; (b) delimited body section — readable, needs a stable delimiter; (c) companion file — mirrors `execution.json`, but two files to keep consistent. Recommendation deferred to V1 once DEL-02-03/DEL-05-01 parsing needs are received. |
| U-02 | Wire field names, value encodings, schema language | DEL-02-01 with consumers | Before OUT-002 schema | All names here are semantic. |
| U-03 | Revision (content identity) algorithm and canonicalization of a multi-file package | DEL-02-01 with DEL-04-03 (record) and DEL-02-02 | Before record/parser fixtures and before any revision comparison claim | Revision meaning defined; comparison untestable until chosen. |
| U-04 | Act-kind names and human/non-human classification | DEL-04-01 (W1 v0.1) | V1 comparison | Accepted-basis names used; reconcile. |
| U-05 | Always-reserved acts: `UNRESOLVED{OI-001}` | Owner with App/SWB contract owners | Before operation-policy production contracts | Checkpoints hold regardless (S-F); no example treats an act as agent-performable. |
| U-06 | Classifier routine permissions: `UNRESOLVED{OI-002}` | Owner with App/SWB contract owners | Before permission-policy implementation | Checkpoints are not permission prompts; no mapping either way. |
| U-07 | Operation version compatibility expression | DEL-03-01 (C) | V1; before DEL-02-03 required-tool fixtures | Element present; expression open. |
| U-08 | Portable naming of harness capability requirements (App-side, non-catalog) | DEL-02-01 with DEL-01-01 and DEL-02-03 | Before App-side required-tool check | Class defined; names open; Root runtime names are not assumed portable. |
| U-09 | Host single seat → role meaning mapping. Options: (a) seat always runs as TASK-equivalent bounded executor of the selected workflow; (b) seat takes the role named by the selected workflow's compatible roles; (c) host guidance names one standing role per conversation. | DEL-02-01 with SWB implementation owner (external) and DEL-02-04 | Before host role-guidance supply and host receiving fixtures | SEAT-1…3 hold for any option; no option chosen. |
| U-10 | Host origin position in unqualified precedence; whether a selection follows new revisions of the same slot | DEL-02-02 (App selection) with DEL-02-01 and host owner | Before host-origin discovery in App | Correctness rests on source-qualified selection; default ordering open. |
| U-11 | Record fields for workflow identity/revision, role meaning, checkpoint disposition and act references | DEL-04-03 | V1 | Referenced by accepted meaning only. |
| U-12 | Placement of shared parts A-1…A-8, A-10: `UNRESOLVED{OI-014}` | App/shared contract owners | Before structural/production contract allocation | Map rows exist; no placement or common implementation proposed. |
| U-13 | Host loop placement/parsing/persistence and panel assembly: `UNRESOLVED{OI-013}` | Shared contract owner with SWB implementation owner | Before shared/host implementation boundary contracts | Rows A-4, A-9, A-10 carry it. |
| U-14 | Instruction/guidance distribution and adoption: `UNRESOLVED{OI-018}` | Owner with shared/project instruction owners | Before instruction changes or dependent supply | Host `AGENTS.md`/`SKILL.md` readability required; distribution not decided. |
| U-15 | First connected operation, autonomy and environment: `UNRESOLVED{OI-021}` | Owner via outside SWB session and App/shared owner | Before connected-activity SoW and execution | The supports fixture's operations are invented placeholders, not the selected operation. |
| U-16 | Automatic catalog extension: `UNRESOLVED{OI-003}` | Owner with host contract owner | Before claiming extension capability | Declarations never assume a new operation is available on all surfaces. |
| U-17 | Consumer confirmations for §9 rows and SWBPIPE consumer needs (DEP-02-01-020…022) | DEL-02-02, -03, -04, DEL-05-01, -05-02; external SWBPIPE owner via human relay | V1 (internal); relay (external) | Every row marked "None"; no confirmation inferred from this document's existence. |
| U-18 | Transfer/adaptation behavior producing derived-from identities | DEL-02-03 (OUT-002) | V1 / W7 | derived-from meaning defined here; transfer procedure not. |

---

## 13. Verification cases (designed, not run)

All cases are designed at v0.1. None has been executed; no parser, consumer or
host exists for them yet. "Fixture subject" material is invented (EXAMPLES).

| Case | Serves | Input | Expected result |
|---|---|---|---|
| VC-01 Four roles and host seat | VER-001 (AC-001) | EXAMPLES E1 read in an App context and in a host single-seat context | Same four role meanings; host reading requires no role-selection UI; compatible roles read identically; seat role meaning recorded or "unknown" (SEAT-1). |
| VC-02 Host-owned library | VER-001 (AC-001) | A host-origin workflow plus host `SKILL.md`/`AGENTS.md` | Identity shows origin *host* and its source root; all files open and readable as text; no App-only construct required. |
| VC-03 Five categories recovered | VER-002 (AC-002) | E1 declared part | A reader recovers every expected input, required tool reference, checkpoint, output and evidence item, and the prose remains intact and associated. |
| VC-04 Undeclared vs empty | VER-002 (AC-002) | E5 (Root prose-only) and a variant declaring "no checkpoints" explicitly | E5 → all categories **undeclared**; variant → checkpoints **declared empty**, others as declared. |
| VC-05 Tool references stay opaque | VER-002 (AC-002) | E1 references; DEL-03-01 C v0.1 when received | Every reference is compared with C; mismatches or unknown C elements recorded as supplier gaps; no wire field invented. |
| VC-06 Restriction not requirement | VER-002 (AC-002) | E6 Root `execution.json` with `tools.capabilities` and no declared required tools | Required-tool check **not established**; restriction retained as ceiling (FB-05). |
| VC-07 Success is not an act | VER-003 (AC-003) | E2 run R-1: proposal operation returns success/queued; no act record | Checkpoint `CP-accept` stays **awaiting act**; output standing **proposed (queued)**; consumer that reports "accepted" is incompatible (REQ-004 negative). |
| VC-08 Independent check without prior acceptance | VER-003 (AC-003) | E2 run R-3: person marks rows checked with evidence; no acceptance act on a proposal | `CP-check` **performed** on its own evidence; no rule demands prior acceptance (I-3); `CP-accept` unaffected. |
| VC-09 Distinct acts | VER-003 (AC-003) | E2 run R-2: acceptance evidence only | `CP-accept` **performed**; `CP-check` still **awaiting act** (I-1). |
| VC-10 Lapse | VER-003 (AC-003) | E2 run R-4: intervening edit to checked rows | Checked act lapses; `CP-check` returns to **awaiting act** for changed content (I-4). |
| VC-11 Direct autonomy does not release checkpoint | VER-003 (AC-003) | E2 run R-5: autonomy widened to direct application for support changes | Change applies with origin/undo; `CP-accept` still holds the run (S-F); applied-with-receipt ≠ accepted. |
| VC-12 Non-human act kind rejected | VER-003 | Variant of E1 whose checkpoint names "apply" | Invalid checkpoint (FB-03). |
| VC-13 Collision without rebinding | VER-004 (AC-004) | E4 | All origins exposed; selection keeps host-origin identity and revision; only explicit reselection changes it. |
| VC-14 Carried and adapted revision | VER-004 (AC-004) | E3 | Adapted workflow has new identity with derived-from = App original incl. revision; original unchanged; App reopening keeps host origin. |
| VC-15 Promised vs observed | VER-004 (AC-004) | E2 run R-6: declared receipt evidence absent after interruption | Output **outcome unknown**; evidence **missing**; nothing reported as passed (FB-11; S-K). |
| VC-16 Unresolved policy not permission | VER-003, VER-004 | E1 read by a consumer that has no OI-001/OI-002 values | No act becomes agent-performable; checkpoints still hold; consumer reports `UNRESOLVED{OI-001}`/`{OI-002}` where a policy value is needed. |
| VC-17 Map rows name consumers | VER-005 (AC-005) | §9 | Every row names consumers, repeated responsibility, maintenance rationale, confirmation state and placement; any row without a consumer is rejected as unjustified; no row is marked agreed without an owner response. |
| VC-18 Excluded acts mapped | VER-006 (AC-006) | §10 vs SoW REQ-006, CLM-002…004 | Every excluded act appears with its owner and receiving interface; host-versus-person distinction present. |
| VC-19 Fixture inventory bound to candidate | VER-007 (AC-007) | This file and EXAMPLES at their v0.x identities | Inventory lists VC-01…VC-18 with candidate identity; all marked "designed, not run"; missing consumer inputs listed (U-17); no joined host witness claimed. |

Limit: passing these cases later would show local contract/fixture
conformance only; it would not establish host implementation, round-trip
execution, adoption or any human act (SoW VER-007).
