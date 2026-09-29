# Chirality v4 — Product Requirements

**Status: post-acceptance consolidation for the accepted decomposition basis;
independent substantive fidelity review [completed](../execution/_Coordination/AgentRuns/APP-V4-DEFINITION-20260926/SEED_FIDELITY_REVIEW.md).** Prepared by HELPS_HUMANS after the
owner's act recorded as **APP-V4-BASIS-20260926**. The accepted subject is the
composite identified in the [acceptance record][B-ACCEPT], not a claim that
the human previously examined these newly consolidated bytes. Acceptance
includes stated open matters and external dependencies; it authorizes
proceeding with decomposition and project definition, not product implementation,
release, or automatic resolution of unruled details.

Companion documents: [architecture](ARCHITECTURE.md),
[host integration](HOST_INTEGRATION.md), [examination](EXAMINATION.md),
[operating method](OPERATING_METHOD.md).

Requirement identifiers take the form `V4-<area>-<nn>` and do not change once
assigned.

---

## 0. Basis, chronology and reading this set

The owner accepted the original five-file seed as revised by the seven HTML
decision recommendations and later directions. Read later explicit directions
as qualifying those recommendations and the original seed. Unselected
alternatives, the earlier twenty-proposal review, historical descriptions and
unconfirmed drafting defaults are not accepted merely by inclusion.

| Source key | Source and scope |
|---|---|
| B-ACCEPT | [APP-V4-BASIS-20260926 acceptance][B-ACCEPT] and its composite manifest; owner act U4 permits decomposition with open matters and external dependencies. |
| B-HTML | [Accepted decision brief][B-HTML], SHA-256 `02d38cb18041c52989d8a2a0b969e6502ce4b25eec85fb0931bbbc100c4420e8`; recommendations 01–07, with their stated qualifications. |
| U1–U5 | [Later owner messages J–O][B-OWNER]: recommendations and SWBPIPE boundary; Domains timing/purpose; acceptance; human-relayed coordination. |
| A–I | Earlier renewal directions, retained through B-HTML's quoted basis: human governance, Root's conceptual role, manuals, SoWs, thesis, PEC and research. |
| OD-nn / D-nn | Original scoped directions/choices in `../conceptual/DECISIONS.md`, including D-19 and D-20; later direction supersedes only what it addresses. |
| X-nn / L-nn | Historical exemplars/lessons in `../conceptual/EXEMPLARS_AND_LESSONS.md`; evidence with limits, not automatic additional requirements. |

The original handoff's pending-answer list and `SEED_SET_PLAN.md` §3 remain
historical. An **open detail** below is carried to its point of need; it is
not a blanket bar to decomposition. These five documents state the accepted
purpose, constraints and interface commitments. Their technical realization
is developed in the responsible Scopes of Work (SoWs) and derivatives,
without silently discarding a commitment during that allocation.

---

## 1. Purpose

### 1.1 Purpose for decomposition

> Chirality makes a capable general agent work within and for a particular
> application. Each application carries its own workflows, skills and
> tools; the same four agents use them to act on the application's objects
> with the means the professional has, and the professional directs the work
> and validates it to the degree the situation warrants. In host
> applications the agent runs on a model the person chooses — a model server
> the user controls or a cloud model — with no default. The Chirality App,
> for creating workflows, is the exemplar each application follows.

### 1.2 Why it exists

Agents can contribute substantial capabilities while carrying none of a
professional's accountability. The owner's premise is that
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
(OD-04). Each host embeds a simpler agent (D-18), running on a local or cloud
model the person chooses (V4-HOST-01), that acts on the host's objects through
the same operations the professional uses.

- **V4-HOST-01** A host's agent runs on a model the person chooses: a model
  server the user controls, or a cloud model reached by OAuth sign-in or an
  API key. There is no default between them; they are options the person
  chooses among (D-18; DEC-4).
- **V4-HOST-02** A host's agent sends data only to the model service the
  person selected and to destinations the person has allowed — in advance in
  an allow list (by category, such as web access, MCP servers or other APIs,
  or by named destination) or when the agent asks during its work. Nothing
  else is contacted: no analytics, silent provider switch or background
  download unless the person turns it on. Every destination contacted is
  recorded and shown (D-18; DEC-5).
- **V4-HOST-03** A host's agent can take the same actions as the human user
  of that host, within the operation/autonomy and human-act distinctions in §4.5
  (semantic parity, D-18; §4.4).
- **V4-HOST-04** A host presents the agent through a panel for conversation,
  workflow selection, the proposal queue and checks, while the agent's work
  appears in the host's own tables and views — there is no agent-private
  surface (X-07).
- **V4-HOST-05** Roles recede in hosts behind a single agent seat and the
  selected workflow (D-10).
- **V4-HOST-06** Each host carries its own workflows, skills and tools, made
  for its work (D-01).

### 2.3 Connectors

PEC and Domains are independent program capabilities consumed through their
own contracts (D-08; U1–U3; B-HTML decision 06). The first connected activity
can proceed without either. PEC has its existing provider project. Domains
provider ownership and location remain unresolved; this seed neither assigns
that construction to App nor excludes it from future App/program allocation.
Receiving responsibilities remain explicit.

- **V4-CON-01** **Domains** is the intended domain database and search-tool
  capability used within a research workflow by SWBPIPE's agent. Search
  results locate evidence; they do not by themselves prove its standing,
  applicability or authority. Provider ownership, content admission, query
  contract and deployment details remain open (U1/U3; OQ-03).
- **V4-CON-02 PEC** supplies pinned, freshness-stamped coordination claims
  across applications: App first, then Piping, then others. Record-tier
  operational reliance is limited to qualified, released coverage adopted
  by the receiving consumer. PEC does not own execution, an execution queue
  or human rulings. Its absence is not a v4 start gate (A–I/E; B-HTML 06).
- **V4-CON-03** Consumers show a connector's standing, coverage, freshness
  and limitations. Absent, stale, partial or failing feeds produce a visible
  limitation and a source-based route for work whose basis remains sound;
  they do not imply empty work, readiness or permission. A connector-specific
  feature can await its missing input while independent work continues.
- **V4-CON-04** Domains develops alongside the first connected activity and
  joins it in a subsequent increment. The initial activity is not dependent
  on Domains. Its later points of need cover provider/query-tool readiness,
  the research workflow and receiving host integration (U2; §3.1).
- **V4-CON-05** In that later increment, SWBPIPE's agent queries the domain
  database through the research workflow to build context for a design
  candidate for the human to approve. The approval's subject and scope remain
  distinct from applying an edit or accepting professional reliance (U3).

The resulting **SWB Piping Designer agent** is the domain-specialized
application expression described by U3, using the applicable role and
workflow. It does not establish a fifth standing Chirality role, a database
technology, a corpus selection or an implementation schedule.

### 2.4 Shared across every expression

- **V4-SHR-01** One workflow format, one set of four roles, and one way of
  recording human acts, used by the Chirality App and every host.
- **V4-SHR-02** Workflows, skills and role guidance are ordinary files in
  open formats (`WORKFLOW.md`, `SKILL.md`, `AGENTS.md`) readable by any
  capable harness.
- **V4-SHR-03** Shared renewal identifies the meanings, responsibilities,
  records and receiving consumers needed by the intended activities. Common
  contracts do not require a common executable service. Shared libraries or
  other implementation are selected for concrete reusable responsibilities,
  with consumer and maintenance consequences accounted for (B-HTML 01–02).

---

## 3. Users and activities

| User | Where | Principal activities |
|---|---|---|
| **The practitioner** — for SWBPIPE, the stress engineer | A host application | Delegates model changes and checks to the agent; reviews and accepts proposals; asks the agent to check their own work; assembles results and reports with the agent |
| **The workflow maker** | The Chirality App | Develops an approach with an agent, carries it out, turns what worked into a workflow, reuses and refines it |
| **The application builder** — the owner, building a host | A host's code | Defines the host's capability catalog and tools once, so the human interface and both agents share them (§4.4; [host integration](HOST_INTEGRATION.md)) |
| **The coordinator** — the owner directing an agent fleet | The Chirality App | Delegates bounded work, follows one work graph per undertaking, examines returns, decides from prepared decision packages (§4.6) |

The accepted initial expressions are the **standalone Chirality App** and
**SWBPIPE as the first engineering host**. The connected model-adjustment and
checking activity, linked to a reusable workflow, organizes the first
increment (B-HTML 05, qualified by U1/U5). Additional essential hosts remain
open in OQ-04; the selected activities are not an exhaustive product scope.

### 3.1 Delivery ownership and staged connections

- **V4-EXT-01** SWBPIPE implementation belongs to the separate session outside
  this harness. The human relays coordination; repository files may carry
  questions, proposed interfaces, received answers and evidence. This App
  undertaking prepares its own product/shared-contract and consumer work; it
  does not implement SWBPIPE or claim the outside session accepted a proposed
  commitment merely because a handoff was written (U1/U5).
- The first connected activity is defined across the App/host boundary and
  staged as usable inputs arrive. The exact operation, autonomy and candidate
  environment are established with the external owner before dependent
  implementation or live examination. App-independent work may continue.
- The later Domains increment preserves places for provider, search-tool,
  research-workflow and host responsibilities. Provider ownership and the
  receiving contract are resolved before dependent implementation; query
  access and source-admission evidence are needed before research-context
  reliance; host integration and the candidate's human-approval route are
  needed before the connected demonstration. No calendar date is invented.
- PEC provider delivery and each application's adoption remain distinct.
  Without PEC, agents perform more source comparison and managers retain
  review/integration ownership; the human carries more cross-undertaking
  coordination. Domains does not depend on PEC, nor PEC on Domains.

[Host integration](HOST_INTEGRATION.md) allocates the interfaces;
[examination](EXAMINATION.md) states the candidate-specific evidence. These
allocations do not assert delivered or adopted external commitments.

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
- **V4-WF-05** When a run reaches a workflow's declared checkpoint, the
  required human act is requested, and the run does not record the act as
  done until the person performs it. Holding the checkpoint — the run waits
  until the act is performed — is **phased to the governance layer**, not
  withdrawn (DEC-4): in the current phase, declared checkpoints are plan
  guidance that the person and the agents manage, and neither the App nor a
  host's embedded loop enforces a hold, blocks a run, or reports a workflow
  unsupported because a hold cannot be enforced. Enforced holds are applied
  later to the workflows that need them; the declared checkpoint and the
  definitions that enforcement needs are kept so that every such workflow can
  be served. Reserved human acts (§4.5) are unaffected.
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
  implying enforcement (L-04). Domain-specific expressions such as the SWB
  Piping Designer specialize context, tools and workflows within these roles;
  their names do not expand the standing repertoire (U3).

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
- **V4-PAR-05** **[open detail — catalog extension, OQ-10]** The original seed
  promises that a new catalog operation becomes available to the person and
  both agents without separate work. Preserve that identified promise while
  defining which surfaces are generated and which require adapter work.
  Automatic all-actor availability and maintenance savings are unestablished;
  common validation alone does not prove them. The accepted treatment is to
  clarify/qualify this claim through one operation trace, then explicitly
  disposition retaining the absolute promise, narrowing its defined surfaces
  or staging it later before the affected production criterion is fixed.
  This consolidation does not silently select a weaker interface (B-HTML 04).

### 4.5 Autonomy and human decision rights

Shared access does not transfer decision rights (OD-05).

- **V4-AUT-01** The person and the agent decide how they work together: for
  each kind of operation, the agent may propose for acceptance or apply
  directly within a scope the person sets, with origin marks, undo and later
  checking (graduated autonomy, D-04).
- **V4-AUT-02** The person validates results to the degree the situation
  warrants; the product makes the standing of every result visible so that
  judgement can be made (D-04; X-19).
- **V4-AUT-03** Agents may prepare checking, acceptance and reliance decisions;
  they must not represent an actual human act as performed when it was not.
  Applying a change, accepting an edit, marking work checked and professional
  reliance remain distinct. **[open detail — OQ-02]** The exact always-reserved
  list and operation-level allocation remain to be resolved; acceptance of
  graduated autonomy does not answer every item (B-HTML 03).
- **V4-AUT-04** **[open detail — OQ-02]** The treatment of classifier-based
  routine permission modes remains unresolved. The prior drafting default
  was a user setting in the App and no such mode in hosts; that default is
  retained as an option, not an adopted policy. Resolve the affected
  permission contract before implementing it; routine tool permission must
  not be confused with an attributable human or professional act.
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

- **V4-CST-01** For the recorded harness/host choices, the priorities are
  maintainability, native functionality, then local models and data privacy
  (D-16–D-18). Their scope is retained; they are not a universal scoring rule
  for every program tradeoff. Assess whole-lifecycle upkeep and coordination
  cost without asserting unmeasured savings (B-HTML 01–02).
- **V4-CST-02** v4.0 targets macOS on Apple Silicon first (D-06).
- **V4-CST-03** Each harness is used through its own published interface,
  unmodified and pinned to a known version; upgrades are deliberate
  (D-17; [architecture](ARCHITECTURE.md)).
- **V4-CST-04** The human governs the undertaking. Root hosts shared ideas,
  methods and tools; location or historical use does not automatically make
  them v4 authority. The three manuals are core working governance applied
  through selected methods; product technical commitments are developed in
  SoWs and derivatives. This later direction qualifies OD-10's earlier
  blanket wording (A–I/A–C; B-HTML 01; [operating method](OPERATING_METHOD.md)).
- **V4-CST-05** Hosts own their domain truth and their validation; Chirality
  never presents an agent's output as the host's accepted result (X-09).
- **V4-CST-06** No real engineering or client data is required to examine the
  product. Verification scenarios use invented material; the owner's later
  validation in use may use invented or owner-controlled material as already
  described by V4-EXM-40. Provider admission/permissions for a Domains research
  fixture remain explicit; no corpus is selected by this constraint.

## 6. Boundaries for v4.0

Not in v4.0:

- Operating systems other than macOS.
- Team coordination inside host applications (project-management option C).
- A second harness in the Chirality App before a concrete need (M-5).
- A generic agent protocol layer between Chirality and the harness, or a
  Chirality-owned agent loop for the Chirality App (analysis §9).
- Dependence on a third-party harness application, or a fork of one.
- No migration/import of v3 chats is selected as an initial delivery
  commitment. Its scope remains open: D-11 did not select option (c), which
  is not a permanent prohibition. Preserve source history and recovery while
  any later migration choice is made (B-HTML 07; OQ-12).

SWBPIPE implementation is explicitly assigned to the outside session, and
PEC retains its existing provider project. Domains database/search-provider
ownership and location remain open for project definition; they are not
excluded from future App/program scope by this consolidation's no-provider-
implementation execution boundary. All interface and receiving obligations
remain identified with their actual owners or unresolved allocation and points
of need.

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
  until then (OD-09). Staged coexistence preserves current selectors, source
  identity, active work and continuing obligations. Replacement is distinct
  from all-project retirement or professional reliance (B-HTML 07).
- Domains is not a prerequisite to the initial V4-REP-01 journey. Its
  subsequent increment has its own receiving/examination obligations (U2).
  PEC is likewise not a v4 start gate; its absence leaves explicit work with
  agents, managers and the human.

## 9. Open questions

| ID | Question | Consequence if unresolved | Owner | Needed by |
|---|---|---|---|---|
| OQ-01 | Purpose/working statement | **Settled for decomposition** by the accepted composite and embedded-primary/App-exemplar direction; later material changes follow their own decision | Owner | No repeat acceptance needed |
| OQ-02 | Exact always-reserved human acts and classifier-permission policy | Carry the known distinctions; do not implement an unruled policy as accepted | Owner with affected App/host design owners | Before the affected operation/permission contract and examination criterion are fixed |
| OQ-03 | Domains provider owner, query/tool contract, source admission, deployment and freshness | Purpose is **settled** by U1/U3; these integration details remain open. Existing host-agent data constraints (V4-HOST-02) are not relaxed by the new capability: a Domains service is contacted only as a destination the person has allowed | Provider owner TBD; App and external host receiving owners; human coordination | Allocate during project definition; resolve each interface before dependent implementation and research-context reliance |
| OQ-04 | Any additional essential host | Initial App/SWBPIPE direction stands; additional scope is not invented | Owner | Before adding host scope or its delivery commitment |
| OQ-05 | Working method's concrete applicability and entry arrangement | Manuals/selected-method direction is **settled**; record exact editions, selected methods and any necessary local entry without automatically retaining the old precedence | Project-definition manager within authority; owner for consequential departures | Project definition and entry to affected work |
| OQ-06 | Further fleet/project-management scope beyond option B | Carry option B; do not turn the full manuals into product features | Owner | Before expanding dependent scope |
| — | OQ-07 and OQ-09: App stack and host loop | **Settled** by D-20 and retained by B-HTML 02 | — | No repeat supplier selection |
| OQ-08 | Written confirmation of sign-in terms for third-party distribution | Original sign-in assumption remains unconfirmed; this seed does not establish terms | Owner | Before public release; any second supplier only if selected |
| OQ-10 | Catalog extension promise V4-PAR-05 / V4-HI-03 | Define generated and adapter surfaces, examine one extension, and record explicit disposition of the original absolute promise | Owner with App/shared-contract and external host design owners | Before freezing the affected SoW criterion or advertising automatic extension |
| OQ-11 | First connected activity's exact operation, autonomy, environment and externally supplied interfaces | Coordination through human-relayed files; no external commitment or live readiness presumed | App manager, human and external SWBPIPE owner | Before dependent implementation or live connected examination |
| OQ-12 | Chat migration and ending coexistence | No initial chat-import obligation or automatic retirement; account for continuing users, work and history | Owner with affected consumers | Before any migration/retirement act |

Acceptance with open matters permits independent definition/work whose basis
is sound. It does not resolve these details by default or require the human
to repeat already settled direction.

## 10. Vocabulary

| Term | Meaning here |
|---|---|
| Host application (host) | An application the owner builds in which Chirality's agent works, SWBPIPE first |
| Chirality App | The standalone App for Creating Workflows |
| Harness | The agent program that runs the model loop and tools (for example Codex) |
| Workflow | Reusable method guidance with a declared part (§4.1) |
| Declared checkpoint | A point in a workflow where a human act is required |
| Capability catalog | A host's single description of every operation a person can perform |
| Semantic parity | Meaningful reads, operations, validation, results and recovery across human, embedded and external agency; shared semantics does not transfer human decision rights |
| Proposal | A change an agent submits for a person's acceptance |
| Human act | An attributable act actually performed by a person; exact always-reserved operation classes remain in OQ-02, with professional reliance distinct from execution |
| Receipt | The host's record that an operation was applied, with its identities and hashes |
| Connector | A separately identified capability consumed through a receiving contract: PEC or Domains; Domains provider allocation remains open |
| SWB Piping Designer agent | The SWBPIPE agent using domain-database research context to create a design candidate for human approval; an application expression, not a new standing role |
| Scope of Work (SoW) | A production contract for outputs, criteria, interfaces, examination and evidence |
| Accepted composite | The original seed, accepted HTML recommendations and later directions identified in B-ACCEPT; distinct from later consolidated bytes |
| Standing | Whether a statement is observed, proposed, assumed, open, or decided |

## 11. Sources

The source hierarchy for this consolidation is §0. Original OD-01…OD-13 and
D-01…D-20 remain in `../conceptual/DECISIONS.md`. The accepted HTML retains
checked historical/current-source observations and their limits: 51
source-checked claims at repository pin `e548d4cfada4d2105de6231516dc6e5fc4bd4689`
are not complete product coverage or new behavioral qualification. Original
T1–T11 and later source checking are evidence, not extra product scope.

The complete thesis in `../foundation/thesis/` remains byte-identical to tree
`47fc49e96c2931ba18090f1a82d56a49f230b3ee`, retaining attribution and its
nonbinding stated standing. Purpose-level citation does not convert its
historical implementation choices into mandatory v4 requirements. The
original author's historical handoff remains available; its old pending
acceptance position is superseded by B-ACCEPT, not erased from history.

[B-ACCEPT]: ../execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/ACCEPTANCE.md
[B-HTML]: ../execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/DECISION_BRIEF.html
[B-OWNER]: ../execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/OWNER_DIRECTIONS.md
