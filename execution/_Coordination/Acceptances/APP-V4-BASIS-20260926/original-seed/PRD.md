# Chirality v4 — Product Requirements

**Status: DRAFT 1 — candidate, not accepted.** Prepared by HELPS_HUMANS with
the owner, 2026-09-26, for the v4 seed set. Nothing in this document is an
accepted requirement until the owner accepts an identified version. Items
marked **[pending]** use a drafting default the owner has not yet confirmed
(`conceptual/SEED_SET_PLAN.md` §3). Owner directions and decisions are cited
as OD-nn and D-nn (`conceptual/DECISIONS.md`); exemplars and lessons as X-nn
and L-nn (`conceptual/EXEMPLARS_AND_LESSONS.md`).

Companion documents: [architecture](ARCHITECTURE.md),
[host integration](HOST_INTEGRATION.md), [examination](EXAMINATION.md),
[operating method](OPERATING_METHOD.md).

Requirement identifiers take the form `V4-<area>-<nn>` and do not change once
assigned.

---

## 1. Purpose

### 1.1 Statement **[pending — Q-01]**

> Chirality makes a capable general agent work within and for a particular
> application. Each application carries its own workflows, skills and
> tools; the same four agents use them to act on the application's objects
> with the means the professional has, and the professional directs the work
> and validates it to the degree the situation warrants. In host
> applications the agent runs local-first, on a model server the user
> controls. The Chirality App, for creating workflows, is the exemplar each
> application follows.

### 1.2 Why it exists

Agents now have capabilities beyond any individual professional but carry
none of a professional's accountability. The owner's premise is that
harnessing them "at scale, reliably" is the future of professional work, and
that professional delivery — not software culture — already has the model for
organising that work (AT §1 items 5 and 7). Chirality exists to make that
practical inside the tools professionals actually use, while the person
remains the one who decides and answers for the result (thesis CF §2.4–2.5,
preserved in `foundation/thesis/`).

### 1.3 What changes from v3

v3 (released as 3.0.1, the fallback until replaced — OD-09) was one desktop
application in which people planned work with Codex and saved useful methods
as workflows. v4 keeps that core experience (X-01) and moves Chirality's
centre of gravity into the applications where the work's objects live
(OD-04, D-APP-87). The agent harness is not the product (D-05): the product is
what makes a general harness act well within and for a particular
application.

---

## 2. Product expressions

### 2.1 The Chirality App — the App for Creating Workflows

The standalone desktop application. It is where a person develops, tries and
refines workflows through conversation, and it is the exemplar of how
Chirality behaves in every application (D-01). It wraps the full experience of
the best available harness (D-17): at v4.0, Codex through its own published
embedding interface, with native sign-in (D-19; [architecture](ARCHITECTURE.md)).

- **V4-APP-01** The App provides the full native harness experience: planning
  and plan revision, substantive tool use, approvals and questions,
  delegation to subagents, interruption, and continuation after restart.
- **V4-APP-02** The App offers sign-in with the user's Codex (ChatGPT)
  account, an API key, and local model servers; a user may have all three
  configured and choose per conversation (D-06).
- **V4-APP-03** The App shows the four roles as the relationships a person
  can choose among (D-10).
- **V4-APP-04** The App presents what the harness produces in its native form
  — plans, tool activity, delegation, requests — without translating it into
  a Chirality-specific vocabulary (L-05; [architecture](ARCHITECTURE.md) M-2).

### 2.2 Host applications — Chirality inside the owner's applications

Engineering design and analysis applications the owner builds, SWBPIPE first
(OD-04). Each host embeds a simpler, local-first agent (D-18) that acts on the
host's objects through the same operations the professional uses.

- **V4-HOST-01** A host's agent runs against a model server the user controls
  by default; a cloud model is used only if the user chooses one and provides
  an API key (D-18).
- **V4-HOST-02** In local operation, a host's agent sends no data to any
  destination other than the configured model server (D-18).
- **V4-HOST-03** A host's agent can take the same actions as the human user
  of that host, subject only to the human acts in §5 (semantic parity, D-18;
  §4.4).
- **V4-HOST-04** A host presents the agent through a panel for conversation,
  workflow selection, the proposal queue and checks, while the agent's work
  appears in the host's own tables and views — there is no agent-private
  surface (X-07).
- **V4-HOST-05** Roles recede in hosts behind a single agent seat and the
  selected workflow (D-10).
- **V4-HOST-06** Each host carries its own workflows, skills and tools, made
  for its work (D-01).

### 2.3 Connectors

Two independent sources the Chirality App (and, where useful, a host) can
consume (D-08). Neither depends on the other; the product works without
either.

- **V4-CON-01 Domains [pending — meaning, Q-07]** supplies knowledge:
  accepted decompositions of corpora and a search index over them. Search
  results locate evidence; they never prove membership or authority.
- **V4-CON-02 PEC** supplies coordination state: a pinned, freshness-stamped
  view of work across project loops. Chirality acts; PEC observes.
- **V4-CON-03** Whatever a connector supplies is shown with its standing and
  freshness, and the product falls back to the underlying files when a
  connector is absent.

### 2.4 Shared across every expression

- **V4-SHR-01** One workflow format, one set of four roles, and one way of
  recording human acts, used by the Chirality App and every host.
- **V4-SHR-02** Workflows, skills and role guidance are ordinary files in
  open formats (`WORKFLOW.md`, `SKILL.md`, `AGENTS.md`) readable by any
  capable harness.

---

## 3. Users and activities

| User | Where | Principal activities |
|---|---|---|
| **The practitioner** — for SWBPIPE, the stress engineer | A host application | Delegates model changes and checks to the agent; reviews and accepts proposals; asks the agent to check their own work; assembles results and reports with the agent |
| **The workflow maker** | The Chirality App | Develops an approach with an agent, carries it out, turns what worked into a workflow, reuses and refines it |
| **The application builder** — the owner, building a host | A host's code | Defines the host's capability catalog and tools once, so the human interface and both agents share them (§4.4; [host integration](HOST_INTEGRATION.md)) |
| **The coordinator** — the owner directing an agent fleet | The Chirality App | Delegates bounded work, follows one work graph per undertaking, examines returns, decides from prepared decision packages (§4.6) |

The essential hosts for v4.0 are **SWBPIPE and the Chirality App** **[pending
— Q-07]**. Connected activities for each are walked in
[examination](EXAMINATION.md).

---

## 4. Capabilities

### 4.1 Workflows

A workflow is reusable method guidance for an undertaking (Root `AGENTS.md`)
with a small declared part the product can observe (D-03).

- **V4-WF-01** A workflow is prose method guidance plus a declared part
  stating: the inputs it expects; the host tools it needs; the checkpoints
  where a human act is required; and the outputs and evidence it returns.
- **V4-WF-02** A person creates and revises workflows through conversation.
  A new or changed workflow is a draft until the person reviews it and
  registers it explicitly; registration never overwrites silently (X-02).
- **V4-WF-03** Every workflow keeps a source-qualified identity (project,
  user, bundled, or host-supplied). A selection is never rebound silently to a
  same-named workflow from another source.
- **V4-WF-04** The product can check that a selected workflow's required
  tools exist in the current host and tell the person when they do not.
- **V4-WF-05** The product holds a workflow's declared checkpoints: when a
  run reaches one, the required human act is requested, and the run does not
  record the act as done until the person performs it.
- **V4-WF-06** Workflows made in the Chirality App can be carried into a host
  and adapted there; a host's own workflows can be opened and refined in the
  Chirality App.

### 4.2 The four agents

- **V4-ROLE-01** The same four roles apply in every expression: alignment
  with the human (HELP_HUMAN), design (HELPS_HUMANS), managed execution
  (WORKING_ITEMS), and bounded execution (TASK). No further roles are planned
  for v4.0 (D-01).
- **V4-ROLE-02** Roles are supplied as guidance in addition to the harness's
  own instructions, never replacing them (X-06).
- **V4-ROLE-03** A bounded executor does not delegate further. Where the
  harness cannot enforce a role's limits, the product says so rather than
  implying enforcement (L-04).

### 4.3 Conversation, execution and recovery

- **V4-EXE-01** Losing a window stops observation, not work; stopping work is
  an explicit act; reconnection recovers the actual state and any outstanding
  requests (X-03).
- **V4-EXE-02** Every request the agent raises is answered or explicitly
  declined; approval is never implied by silence or timeout (X-04).
- **V4-EXE-03** Only observed events are shown as having happened; an
  unobserved outcome is shown as unknown (X-05).
- **V4-EXE-04** After a restart, a person can continue a conversation and see
  what was done before it.

### 4.4 Semantic parity

Defined in `conceptual/MAINTAINABILITY_ANALYSIS.md` §10.3 (accepted with
D-19); the contract is in [host integration](HOST_INTEGRATION.md).

- **V4-PAR-01** Each host describes every operation a person can perform once,
  in a capability catalog: its inputs, preconditions and reasons it may be
  unavailable, its effects, its result and its errors.
- **V4-PAR-02** The host's interface, the host's embedded agent, and an
  external agent (such as the Chirality App's) all act through that one
  catalog.
- **V4-PAR-03** The agent perceives the same views the person does — tables,
  results, diagnostics — with the same standing marks.
- **V4-PAR-04** An agent's operation passes through the same validation and
  the same application route as the person's, with the same outcomes and
  errors.
- **V4-PAR-05** A new operation added to the catalog becomes available to the
  person and to both agents without separate work.

### 4.5 Autonomy and human decision rights

Shared access does not transfer decision rights (OD-05).

- **V4-AUT-01** The person and the agent decide how they work together: for
  each kind of operation, the agent may propose for acceptance or apply
  directly within a scope the person sets, with origin marks, undo and later
  checking (graduated autonomy, D-04).
- **V4-AUT-02** The person validates results to the degree the situation
  warrants; the product makes the standing of every result visible so that
  judgement can be made (D-04; X-19).
- **V4-AUT-03** **[pending — Q-04]** An agent never originates or represents a
  human act — accepting a proposal, marking work checked, approving, or
  relying on a result — in the person's name. It may prepare these acts; the
  person performs them.
- **V4-AUT-04** **[pending — Q-04]** In the Chirality App, harness modes in
  which a model classifier approves routine requests are a setting the person
  may choose, like any other permission setting. Host agents do not use them.
- **V4-AUT-05** Nothing the agent produces is presented as certified, sealed,
  approved or code-compliant; such statements belong to the accountable
  professional (X-09; SWBPIPE `docs/PROFESSIONAL_BOUNDARY.md`).

### 4.6 Coordinating an agent fleet

For the owner and an agent fleet, in the Chirality App (D-09, option B).

- **V4-PM-01** Delegation carries a bounded brief: purpose, basis, context,
  authority and tools, write scope, and expected return (X-15).
- **V4-PM-02** Each undertaking has one current work graph, kept as a file,
  that shows selected work, prerequisites, owners, results and what comes next.
- **V4-PM-03** Returns awaiting examination form a visible queue; the
  product shows waiting work by its cause (X-16).
- **V4-PM-04** Decisions reserved to the person arrive as decision packages
  naming the exact act requested, with alternatives and consequences (X-17).
- **V4-PM-05** Status is recoverable across sessions from the files.
- **V4-PM-06** Coordination views are derived from files and can be rebuilt;
  they never become the authority (X-18).
- Further project-management scope indicated by the owner is an open question
  (§9, OQ-06).

### 4.7 Records

(D-07.)

- **V4-REC-01** A host's domain truth stays in the host's own store.
- **V4-REC-02** Workflow definitions, the person's decisions and accepted
  records are ordinary files in the user's project or workspace.
- **V4-REC-03** A harness's own session store is operational, not the
  authority for any human act.
- **V4-REC-04** Each workflow run leaves a compact record, kept with the
  project, that links the host's own receipts and hashes rather than copying
  them.
- **V4-REC-05** Every recorded human act binds to the identified content,
  scope and purpose it concerns (thesis CF §2.3; X-20).

---

## 5. Constraints

- **V4-CST-01** Priorities, in order: maintainability, functionality, then
  local models and data privacy (D-16–D-18).
- **V4-CST-02** v4.0 targets macOS on Apple Silicon first (D-06).
- **V4-CST-03** Each harness is used through its own published interface,
  unmodified and pinned to a known version; upgrades are deliberate
  (D-17; [architecture](ARCHITECTURE.md)).
- **V4-CST-04** Root governance applies (Root `AGENTS.md`; OD-10).
- **V4-CST-05** Hosts own their domain truth and their validation; Chirality
  never presents an agent's output as the host's accepted result (X-09).
- **V4-CST-06** No real engineering or client data is required to examine the
  product; examination uses invented material.

## 6. Boundaries for v4.0

Not in v4.0:

- Operating systems other than macOS.
- Team coordination inside host applications (project-management option C).
- A second harness in the Chirality App before a concrete need (M-5).
- A generic agent protocol layer between Chirality and the harness, or a
  Chirality-owned agent loop for the Chirality App (analysis §9).
- Dependence on a third-party harness application, or a fork of one.
- Migration or import of v3 chats **[pending — the owner selected condition
  (b) of Q-10 and did not select (c)]**.

## 7. Interfaces

Summarised here; specified in the companion documents.

| Interface | Between | Document |
|---|---|---|
| Harness interface (Codex App Server) | Chirality App ↔ harness | [architecture](ARCHITECTURE.md) |
| Host agent loop and model server | Host ↔ its embedded agent ↔ model | [architecture](ARCHITECTURE.md) |
| Capability catalog, proposals, receipts | Host ↔ agents (embedded and external) | [host integration](HOST_INTEGRATION.md) |
| Connector consumption | Chirality ↔ PEC, Domains | [host integration](HOST_INTEGRATION.md) |
| Workflow, skill and role files | Every expression ↔ every harness | this PRD §4.1–4.2 |

## 8. Replacing the v3.0.1 fallback

(D-11.)

- **V4-REP-01** v4 may replace v3.0.1 when both hold: the Chirality App
  supports the core loop at least at v3.0.1's level — plan, execute, save a
  workflow, reuse it, approvals, interruption, restart — and one live
  embedded journey in SWBPIPE runs from a request to the person's acceptance.
- The owner decides the replacement; the old projects and archives are kept
  until then (OD-09).

## 9. Open questions

| ID | Question | Consequence if unresolved | Owner | Needed by |
|---|---|---|---|---|
| OQ-01 | The working statement (§1.1) | The PRD's opening remains a draft | Owner | Acceptance |
| OQ-02 | The two autonomy points (V4-AUT-03, -04) | Decision rights remain partly implicit | Owner | Acceptance |
| OQ-03 | What "Domains" means (V4-CON-01) | The connector's scope is ambiguous | Owner | Acceptance |
| OQ-04 | Whether any host besides SWBPIPE is essential to v4.0 | Examination scope | Owner | Acceptance |
| OQ-05 | The build method (Q-11) | The operating method stays a draft | Owner, with HELPS_HUMANS | Before the implementation session |
| OQ-06 | Further project-management scope ("more to it", D-09) | v4.0 carries option B only | Owner | FEED |
| — | OQ-07 and OQ-09 (the App's stack; the host agent's loop) were settled by D-20 | — | — | — |
| OQ-08 | Written confirmation of sign-in terms for distributing the Chirality App (OpenAI) and any Claude sign-in (Anthropic) | Distribution beyond the owner's own use | Owner | Before public release |

## 10. Vocabulary

| Term | Meaning here |
|---|---|
| Host application (host) | An application the owner builds in which Chirality's agent works, SWBPIPE first |
| Chirality App | The standalone App for Creating Workflows |
| Harness | The agent program that runs the model loop and tools (for example Codex) |
| Workflow | Reusable method guidance with a declared part (§4.1) |
| Declared checkpoint | A point in a workflow where a human act is required |
| Capability catalog | A host's single description of every operation a person can perform |
| Semantic parity | The agent can take the same actions as the person, through the same catalog and route |
| Proposal | A change an agent submits for a person's acceptance |
| Human act | Accepting, marking checked, approving, or relying on a result — performed only by the person |
| Receipt | The host's record that an operation was applied, with its identities and hashes |
| Connector | An independent source the product consumes: PEC or Domains |
| Standing | Whether a statement is observed, proposed, assumed, open, or decided |

## 11. Sources

The directions and decisions this document relies on are in
`conceptual/DECISIONS.md` (OD-01…OD-13, D-01…D-19). The evidence behind
exemplars and lessons is in `conceptual/EXEMPLARS_AND_LESSONS.md` and the run
record's TASK returns. The thesis in `foundation/thesis/` is cited for
purpose-level propositions only; it is preserved, nonbinding, and not a
source of requirements.
