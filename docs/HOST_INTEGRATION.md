# Chirality v4 — Host integration

**Status: post-acceptance consolidation for the accepted decomposition basis;
independent substantive fidelity review [completed](../execution/_Coordination/AgentRuns/APP-V4-DEFINITION-20260926/SEED_FIDELITY_REVIEW.md).** This is the host-contract companion
to the [PRD](PRD.md) and [architecture](ARCHITECTURE.md), prepared after the
owner accepted composite **APP-V4-BASIS-20260926** with open matters and
external dependencies. [PRD §0](PRD.md#0-basis-chronology-and-reading-this-set)
identifies the actual accepted sources; the human did not previously
hash-review these newly consolidated bytes. Existing `V4-HI-<nn>` identities
are retained. Amended by scope-change amendment SCA-V4-001, accepted
2026-09-29, for owner decisions DEC-4 and DEC-5 (PRD §0). **Open detail** marks an unruled policy or interface point,
not a cancellation of accepted semantic parity or permission to invent it.

The contract is expressed in terms of behaviour and data, not a particular
programming interface; each host implements it in its own code (M-1).

## 1. Who implements what

| Party | Responsibility |
|---|---|
| The host | Its domain objects and truth; the capability catalog; validation and the one route by which changes are applied; receipts; the human acts it offers; its interface |
| App/shared-contract undertaking | Shared catalog/workflow/checkpoint/record meanings, App-side consumer behavior and selected reusable types/components; allocation follows actual responsibility, not an assumed common service |
| Responsible host implementation owner | The embedded minimal loop and host panel/integration, with host-specific workflow/tool realization; SWBPIPE implementation is in the external session |
| The embedded agent | Acting through the catalog within the autonomy the person has set |
| An external agent | Acting through the same catalog, exposed as an MCP server or command-line interface |
| PEC provider | Existing PEC project; its qualified delivered capability and evidence are distinct from receiving consumer adoption |
| Domains provider, allocation open | Database/search capability and evidence within an identified contract; provider ownership/location are not assigned or excluded by this seed |
| Human coordinating the external session | Relays proposed contracts, questions and returns using repository files; retains consequential decisions |

U1/U5 explicitly keep SWBPIPE implementation outside this undertaking. A
written shared-interface proposal does not establish that the external
session accepted it or delivered it. Domains provider ownership and location
remain open (PRD OQ-03); the current consolidation task's lack of implementation
authority is not a future product-scope exclusion. Each receiving SoW names
its required contribution, actual owner or unresolved allocation, and point
of need before relying on it.

## 2. The capability catalog

- **V4-HI-01** A host describes every operation a person can perform — reads
  and changes alike — once, in a capability catalog.
- **V4-HI-02** Each entry states:

  | Field | Content |
  |---|---|
  | Identity | A stable identifier and a version |
  | Purpose | What the operation does, in words a person and an agent both read |
  | Inputs | A schema for its arguments |
  | Availability | Its preconditions, and the reason it is unavailable when they do not hold (for example "Select a load case in the model tree first") |
  | Effects | Which objects it changes, if any |
  | Result | A schema for what it returns, including the standing of the result |
  | Errors | The errors it can return and what each means |
  | Human-act class | None; **may apply** within granted autonomy; **proposal only**; or **reserved** to the person (§5) |

- **V4-HI-03** The host's interface, its embedded tools and its external
  interface are generated from, or checked against, one catalog. **[open
  detail — PRD OQ-10]** The original promise of adding an operation for all
  three without separate work remains identified under V4-PAR-05. Define
  the generated surfaces and remaining adapter work; trace an extension
  before claiming automatic availability or savings. The absolute promise's
  disposition is explicit, not silently weakened by this consolidation
  (B-HTML 04).
- **V4-HI-04** An operation that is unavailable to the person is unavailable
  to the agent, with the same reason.

## 3. Perception

- **V4-HI-10** The agent reads through catalog read operations that return
  the same views the person sees — tables, results, diagnostics — with the
  same standing marks (V4-PAR-03).
- **V4-HI-11** Every read returns the **basis** it describes: an identity for
  the workspace, its generation, the model revision, and a canonical content
  hash. A later action cites the basis it relied on.
- **V4-HI-12** Results carry their standing — current or historical, the
  checks they passed, known limitations — so that an agent does not present a
  result with more confidence than the host gives it (L-10).

## 4. Changes

- **V4-HI-20** Every change, by person or agent, passes through the host's one
  validation and application route; there is no second route for agents
  (V4-PAR-04).
- **V4-HI-21** An agent's change carries its origin (for example an author
  type of "agent" with the conversation and workflow run it came from) and the
  basis it relied on.
- **V4-HI-22** Where the person has granted the autonomy, the agent may apply a
  change directly; the change is marked with its origin, can be undone, and
  can be checked later (V4-AUT-01).
- **V4-HI-23** Otherwise the change is a **proposal**, with this lifecycle:

  ```text
  drafted → validated → queued → accepted → applied (receipt)
                            ├──→ rejected
                            ├──→ withdrawn
                            └──→ stale   (its basis no longer holds)
  applied or not, if the outcome cannot be observed → outcome unknown
  ```

  A stale proposal is refused with its reason and may be re-drafted on the
  current basis. A later selection never retargets a proposal. Submitting the
  same proposal twice has one effect.
- **V4-HI-24** A proposal shows the person, in the host's own views, what will
  change: old and new values, the objects affected, and why (X-07).
- **V4-HI-25** `success` from an operation means it ran; it never means a
  person accepted anything. A submitted proposal reports "queued" until the
  host records acceptance and application.

## 5. Human acts

- **V4-HI-30** A host names its human-act and operation classes. **[open
  detail — PRD OQ-02]** The exact always-reserved list remains to be settled
  for affected operations. The original draft listed acceptance where
  autonomy requires it, marking checked, approval and professional reliance;
  those different subjects must not be collapsed or that whole list
  silently declared ruled. Professional reliance remains with the human.
- **V4-HI-31** Agents may prepare the person's decisions and ask for an act;
  they do not record an actual human act as performed when it was not.
  Direct operation under granted autonomy is distinct from impersonating
  checking, acceptance or reliance. Finalize the affected reserved-act and
  routine-classifier policy before implementing that operation (V4-AUT-03,
  -04; B-HTML 03).
- **V4-HI-32** A human act binds to the content it concerns (for example a
  row's content hash) and lapses visibly when that content changes (X-20;
  SWBPIPE DEC-104's checked tag).
- **V4-HI-33** Acceptance of a proposed edit is not engineering approval. The
  interface says "accept", never "approve", for proposals (SWBPIPE design
  direction).

## 6. Autonomy settings

- **V4-HI-40** The person sets, per class of operation, whether the agent may
  apply directly or must propose. The setting is visible, can change during
  work, and is recorded with each run (D-04).
- **V4-HI-41** A host chooses conservative defaults for consequential
  operations. For SWBPIPE's model changes the default is proposal with
  row-by-row, multi-row or whole-batch acceptance, following the owner's
  direction of 2026-09-17; the person may widen it.
- **V4-HI-42** Autonomy does not override a workflow's declared checkpoints:
  whatever the autonomy setting, a checkpoint's required act is requested and
  recorded as done only when the person performs it. Holding the run at the
  checkpoint until then is phased to the governance layer (V4-WF-05): in the
  current phase a checkpoint is plan guidance that the person and the agents
  manage, and the reserved acts (V4-HI-30) still bind.

## 7. External agents

- **V4-HI-50** A host may expose its catalog to agents outside it — such as the
  Chirality App's Codex — as an MCP server using the current protocol, or as a
  command-line interface over its live controller. Both are built from the
  catalog and apply the same validation, autonomy settings and reserved acts.
- **V4-HI-51** An external agent cannot perform an act reserved to the
  person by the applicable operation policy. The earlier SWBPIPE no-external-
  `apply` design is scoped historical context; it does not decide all v4
  graduated-autonomy choices. Nor does the new direction amend the current
  host's operative policy without its receiving adoption.
- **V4-HI-52** External access is off unless the person enables it, and it is
  local to the machine.

## 8. Connectors

- **V4-HI-60** **Domains** provides the database/query-tool capability called
  within a research workflow by SWBPIPE's agent. Returned references and
  source standing make its research context inspectable; retrieval is not
  authority or proof of suitability. The provider/query and admission/
  freshness contracts remain to be defined (U1/U3; PRD OQ-03).
- **V4-HI-61** **PEC** is consumed through its own interface when available.
  Covered record-tier claims expose the examined-through pin, source
  reference, coverage and freshness. Operational reliance is confined to
  qualified/released coverage adopted by the consumer. Ephemeral presence
  is not correctness or live-execution authority; PEC does not dispatch,
  own an execution queue or write human rulings (B-HTML 06).
- **V4-HI-62** Consumers distinguish qualified/current, limited/stale/failing
  and absent connectors. They show the affected limitations and support
  source-based reconstruction where the basis is sound; a missing feed
  cannot imply empty work, readiness or permission. Connector-dependent
  work may wait while separately supported work continues.
- **V4-HI-63** Coordination file formats have identified versions and
  consumers. Changes account for PEC feed coverage and receiving adoption;
  a writer is not governed by a projection merely because it reads the
  files. Share the necessary contract, not an assumed implementation.
- **V4-HI-64** Domains develops alongside the first connected activity and
  joins it in a subsequent increment. Record provider, search-tool,
  research-workflow and host contributions and points of need. Initial
  D05 activity does not require Domains; a later database-research activity
  needs its actual query capability and source basis (U2).
- **V4-HI-65** In that later activity, the SWBPIPE agent queries the domain
  database to build context for a design candidate for human approval.
  Candidate creation, source-backed context, the human's approval, host
  application and professional reliance retain distinct identities. This
  is the **SWB Piping Designer agent** application expression, using the
  standing roles rather than adding one (U3; V4-CON-05).

### 8.1 Domains increment: responsibilities and points of need

| Contribution | Responsibility to establish | Point of need / current standing |
|---|---|---|
| Domain database and source basis | Provider owner TBD; content admission, identity, standing and freshness | Before query results are relied on as research context; no corpus or database technology selected here |
| Search-tool/query interface | Provider and receiving tool-contract owners; request/result meanings, source references, limitations and availability | Before dependent tool/consumer implementation; tools must not fabricate context when the input is unavailable |
| Research workflow | Responsible method/host owner, coordinated with App workflow support where used | Before the research-to-candidate increment; distinguish retrieved evidence, inference, gaps and candidate output |
| Host use and human approval | External SWBPIPE implementation owner and human; query use, candidate presentation and actual approval route | Before the connected host witness; a prepared coordination file is not evidence of agreement or readiness |
| App/shared contribution | Method/consumer and shared-contract responsibilities; any Domains provider allocation remains to be decided | Define the receiving contribution and unresolved provider allocation in project definition; SWBPIPE construction stays externally owned |

The provider's deployment and data boundary are open. The Domains direction
does not relax V4-HOST-02: a Domains query service is contacted only as a
destination the person has allowed.
Resolve a compatible query/tool arrangement before relying on it, or obtain
an explicit decision on an affected constraint. No database platform,
corpus, remote service or delivery date is inferred.

PEC and Domains remain independent. Without PEC, agents and managers perform
more file comparison/orientation and retain review/integration ownership;
the human carries more cross-undertaking coordination. With Domains absent,
the first connected activity continues, but its later database-grounded
research capability is not falsely reported as available.

## 9. Records

- **V4-HI-70** Each workflow run leaves a compact record with the host project:
  the workflow and version, the conversation, the autonomy settings, the
  operations requested and their outcomes, the host receipts by reference, the
  human acts performed, the model used and, for a host's agent, each network
  destination contacted (D-07; V4-HOST-02).
- **V4-HI-71** The host's receipts, hashes and origin marks are the evidence of
  what changed; the run record links them and does not copy them.

## 10. Checklist for a new host

For the application builder (PRD §3):

1. Describe every operation once in a capability catalog (§2).
2. Route every change through one validation and application path (§4).
3. Return a basis with every read; check it on every change (§3–4).
4. Mark origins; offer undo; show proposals in the host's own views (§4).
5. Name the reserved human acts and bind them to content (§5).
6. Choose autonomy defaults for consequential operations (§6).
7. Select reusable panel/components where they fit, and implement the host's
   loop/catalog/model connection under that host's ownership and data boundary.
8. Write the host's own workflows and skills; test them in the Chirality App.
9. Optionally expose the catalog to external agents (§7).
10. Where a connector is selected, define its receiving/qualification and
    unavailable paths (§8); stage the later Domains research increment.

This is application-builder guidance for defining the contract. It neither
adds ten human checkpoints nor authorizes this App undertaking to implement
an externally owned host.

## 11. SWBPIPE as the first engineering host

SWBPIPE's actual implementation is owned by the external session identified
in U1/U5. The human relays coordination through repository files. The
initial connected model-adjustment/checking activity and the later Domains
research/design-candidate increment must be coordinated with that owner;
neither is claimed delivered or adopted here.

The original T6 table described `2b0572fe0` and a separate live-control
branch. It remains in the [preserved original seed][original-host] as dated
evidence. It is not a statement of SWBPIPE's current deployment. The later
checked source account at `e548d4cfada4d2105de6231516dc6e5fc4bd4689` establishes:

| Observed source responsibility | Limit relevant to this contract |
|---|---|
| Runtime catalog/binding/call transport | Not a joined live host mutation path or durable exactly-once domain outcome |
| Piping controller through native/WASM domain application, model/history/receipts | Queue-time basis differs from original external inspection basis; stronger frozen-review checks cannot be assumed for every route |
| Workflow identity/supply and App recovery machinery | Resolution differs from provider adoption and behavior; conversation recovery differs from undertaking recovery |
| PEC contract and foundation slices | Not composed qualified delivery or receiving consumer adoption |

These observations are grounded in the accepted decision brief's evidence
account, not new execution. Later mainline/external-session changes require
a targeted applicability check before implementation reliance. The v4
replacement condition still requires the live connected journey; decomposition
acceptance and source inspection are not substitutes for it.

[original-host]: ../execution/_Coordination/Acceptances/APP-V4-BASIS-20260926/original-seed/HOST_INTEGRATION.md
