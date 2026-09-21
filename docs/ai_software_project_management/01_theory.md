# Theory: directing a software project through an AI team

This is an explanatory draft. Its propositions are to be examined through the
later worked example; its recommendations do not create operational authority.
Source identities and limitations are in the [reading map](README.md).

## 1. The undertaking and its purpose

Managing software development is project management. A software project is a
coordinated transformation of
intent into a working, maintained product. Its continuity depends on preserving
the relationships between purpose, requirements, decisions, implementation and
evidence while those relationships become more detailed.

AI agents change the means by which work is performed. They permit a person to
commission investigations, compare alternatives, draft artifacts, implement
changes and examine results through many bounded instances. The project still
needs a purpose, a scope, a basis for decisions, responsibilities, dependencies
and a way to judge whether the result serves its intended use.

The unit of management is an **undertaking**: a bounded contribution to that
purpose whose result and remaining obligations can be assessed. An undertaking
may be an investigation, a deliverable, an integration or a release. Its useful
boundary depends on the work. A repository folder, a chat session and a product
feature may each contain several undertakings or only part of one.

**Proposition P1 — coordination follows the condition of the work.** The useful
coordination pattern depends on how well the purpose and interfaces are
understood, how strongly the parts depend on one another, and the consequences
of changing them. A pattern suited to repeated implementation can impede initial
definition; a conversational pattern suited to definition can unnecessarily
constrain execution after the important questions are settled.

This proposition concerns a relationship to investigate, not a universal stage
sequence or a claim that more autonomy always improves performance.

## 2. A vocabulary that preserves important differences

| Term | Meaning in this manual |
|---|---|
| Product | The software and associated outcomes intended to serve users |
| Project | The organized undertaking that develops and hands over the product |
| Requirement | A stated condition or capability whose source, interpretation and status can be examined |
| Deliverable | An identified unit of committed output with a scope and basis for assessing it |
| Work unit | A bounded piece of execution; it need not coincide with a deliverable |
| Record | Externalized information about the work, including decisions and evidence |
| Dependency | A relationship with stated semantics under which one unit bears on another |
| Agent instance | A model operating with instructions, supplied context, tools and actual permissions |
| Role | A responsibility within the undertaking; it is distinct from model capability and reasoning effort |
| Acceptance | An attributable act of reliance or disposition within a stated scope; its particular authority comes from the governing arrangement |
| Understanding | A situated grasp of the work and its relationships, supported but not exhausted by records |

The distinction between the product and its records is essential. A status file
may accurately record that a test passed while the product still fails a user
need. Conversely, a useful implementation can exist without an adequate account
of its scope or verification. The theory concerns keeping those relationships
inspectable, rather than allowing either the implementation or its paperwork to
stand for the whole project.

The thesis distinguishes descriptive records from records that constitute a
governed act, and recorded information from a person's knowing (§§3.2.1, 3.6).
For this manual, an engineering claim remains answerable to its subject, while
an acceptance record identifies a decision and its scope. Neither a valid file
format nor a content hash establishes that the claim is correct, that attribution
is truthful, or that someone has understood the work.

## 3. Four perspectives for coherence

The thesis's four philosophical pillars supply connected questions for this
account. **Ontology** asks what entities and relationships are being discussed.
**Epistemology** asks what supports a claim, what remains unknown and what can
be relied upon. **Praxeology** asks how action is organized and how it produces
an assessable result. **Axiology** asks which purposes, values and consequences
give those choices their importance.

These are evaluative perspectives, not four compartments into which every
artifact must fit. A review has an object, a basis for belief, an enacted method
and a purpose. A dependency has identified endpoints, evidence for the stated
relationship, consequences for execution and a reason the relationship matters.
The perspectives are useful together because each exposes a different kind of
incompleteness in an otherwise plausible account.

Coherence requires more than consistent terminology. A practice that makes the
owner decide every routine action would conflict with an aim of preserving
attention for consequential judgment. A theory that recognizes uncertainty
would conflict with a workflow that silently fills missing facts. A claim that
records support understanding would conflict with a promise that copying those
records transfers an identical understanding to another participant.

**Practice implication:** examine both the statements within each perspective
and the consequences they impose on the others. The resulting questions should
help assess a decision; they need not become four mandatory forms for every task.

## 4. Four structures of the same work

The four structures proposed in thesis §4.3.5 describe how work and its
information can be organized. They are distinct from the four philosophical
perspectives. No one-to-one correspondence between the two sets is assumed.

| Structure | Principal question | Contribution |
|---|---|---|
| Tree | What is this made of, and where does this unit belong? | Composition, identity and focused working context |
| Production graph | What depends on what for this objective? | Ordering, readiness and integration relationships |
| Network | What bears on this question, and who decided it? | Relevance, provenance and memory across structural boundaries |
| Attention | How are the particulars brought into an intelligible whole? | Selection, decomposition, interpretation and synthesis |

The **tree** supplies a stable way to identify and locate parts. In Chirality,
packages, deliverable folders and their local files express this structure.
Their purpose is to make the unit intelligible: its scope, context, sources,
dependencies, state and relevant memory are available where the work occurs.
An unexamined collection of notes in a folder provides storage without necessarily
providing that intelligibility.

The **production graph** expresses relationships among work units. A sequencing
graph has an objective and typed edges; not every relationship is a prerequisite.
The same deliverable may have a place in a project DAG and participate in several
finer session graphs. A worktree provides execution isolation, but does not by
itself express all dependencies or assign integration responsibility.

The **network** connects material that crosses the tree: a decision affecting
many deliverables, a source used in several analyses, a constraint revised by a
later ruling. Its important relationships include provenance and supersession.
Finding similar words is useful retrieval; establishing who decided what, for
which purpose and at which revision requires reading the relevant record.

**Attention** describes bringing those particulars into consideration together.
Here it names the work of selection and synthesis, not a claim that a particular
neural attention algorithm formally represents project judgment. A model may
generate decompositions and comparisons; the people responsible for the project
interpret their significance and exercise the authority allocated to them.

The views participate in successive passes through an undertaking. Attention
to sources and prior decisions supports a decomposition; the resulting tree
locates units whose relationships inform the production graph. Execution adds
observations, proposals, failures and decisions to the network of records.
Subsequent interpretation can draw on that expanded basis when refining the
work. This account develops the connection proposed in thesis §4.3.5.

That recurrence is a relationship among activities, not a requirement to invoke
`LOOP_INIT` during every phase. Human steering shapes the purpose and
consequential changes; acceptance identifies what may be relied upon within
its stated scope. Raw observations and rejected proposals can remain useful
records without acquiring acceptance. The cycle therefore carries both learning
and unresolved questions, rather than only completed or accepted outputs.

**Proposition P2 — completeness requires relationships among the views.** A
locally coherent activity can still fail the undertaking when it neglects a
necessary relationship in another view. Examples to investigate include a
well-formed work package disconnected from a changed requirement, a ready task
based on a superseded decision, or a fluent synthesis that omits relevant history.

The proposal is that these views explain recurring coordination needs. The
claim that they exhaust the structures of knowledge work is not established
here. Nor does classifying a failure under one view independently prove the
classification or the theory.

## 5. From intent to dependency structure

The initial structure of a project develops through requirements, decomposition
and scopes of work. Dependencies can be expressed there before implementation
begins. In the owner's described arrangement, deliverable-local metadata records
those relationships and workflows assemble them into a formal graph. The graph
has a traceable basis in the work's definitions; it is not simply reconstructed
from whatever tasks happened to be performed.

Decomposition makes an intention more explicit. It identifies outcomes, divides
scope into understandable units and exposes relationships that were implicit in
the original description. Project setup makes those units available for work:
identities, folders, local context, sources, scopes and dependency metadata give
participants a place from which to reason and act. The exact files are an
implementation choice under the project's contracts, not a universal ontology.

A graph derived from metadata is no more reliable than the interpretation and
currency of its inputs. Schema validity establishes that the representation is
well formed; it does not establish that all relevant dependencies were captured.
Rebuilding a graph from stale registers preserves the underlying error.

**Proposition P3 — dependency analysis exposes decisions as well as order.**
For fixed node and edge semantics, strongly connected components identify mutual
reachability. Their condensation is a DAG, but collapsing each SCC computationally
does not settle how the corresponding engineering work should be performed.

A cycle may reflect nodes that are too coarse, a contract that needs definition,
a dependency whose interpretation is wrong for the selected objective, or
necessary coupling. An apparent cycle may dissolve as ambiguous relationships
are clarified. A remaining one may be resolved by decomposition, inversion,
grouping the coupled work, or an explicit change to the relationship being
modelled. The engineering rationale matters as much as the resulting topology.

An acyclic graph can still omit an important edge or order the work badly. SCC
analysis detects cycles under its selected semantics; it does not validate
every judgment encoded in the graph. A runtime feedback loop and a build-order
prerequisite are different relationships and need not have the same topology.

Chirality's [cycle doctrine](../CYCLE_DRIVEN_RESOLUTION.md) adds specific
governance: cut and merge decisions are human-gated, unresolved cycle edges do
not drive sequencing, and accepted graph regeneration follows its governing
change trigger. Those are current project rules to consult in execution. This
theory does not authorize deleting edges, silently grouping deliverables or
rebuilding the accepted DAG at every session entry.

## 6. Two resolutions and two readings of the graph

The **project DAG** describes relationships among enduring project commitments.
The **session work graph** describes how a particular undertaking will proceed:
its smaller work units, discoveries, blockers, ownership and integration points.
The latter may cut across packages because the implementation problem does.

Traceability between the two allows local adaptation without losing the ability
to explain its contribution. A provisional link is useful when its uncertainty
is visible. Guessing a deliverable home and then treating it as settled changes
the meaning of the record. Where the owner deliberately permits implementation
to run ahead of deliverable reconciliation, that departure has a scope and a
later reconciliation obligation; it does not erase the original commitments.

The production graph also has **two readings**. The blocker subset helps answer
what can proceed now. The wider closure inquiry asks whether the relevant
commitments, interfaces, evidence and dependency dispositions form an adequate
account of the completed scope. Thesis §4.3.5 distinguishes sequencing from
audit in these terms.

**Proposition P4 — readiness and closure require different views.** Requiring
complete project closure before each bounded action can prevent useful progress.
Conversely, the absence of current blockers cannot establish that every
commitment has been satisfied. Audit completeness is relative to its declared
scope and checks; even a fully connected, hash-consistent graph does not prove
that its claims are true or that no requirement was omitted.

## 7. Coordination as the undertaking becomes clearer

Project conditions suggest different forms of coordination. These are patterns
to recognize and choose, not a mandatory state machine or an automatic phase
classifier.

| Dominant condition | Useful coordination pattern | What permits greater autonomy |
|---|---|---|
| Purpose and product remain uncertain | Human–Agent 0 dialogue, alternatives and bounded investigations | A sufficiently explicit purpose, scope and decision basis |
| Requirements and responsibilities are taking shape | PRD work, decomposition and project setup | Work units with intelligible scopes, interfaces and return criteria |
| Implementation exposes substantial coupling | Coordinated work on connected units, within or across packages | Resolved decisions and workable interface boundaries |
| Contracts and dependencies support independent work | Managed parallel execution and traversal of ready units | Reliable readiness evidence and defined integration ownership |
| Product is nearing completion | Smaller candidate integrations and connected-user verification | A stable candidate and resolved consequential defects |
| A release is authorized | A controlled publishing pipeline | Identified artifacts and satisfied release prerequisites |

During initial definition and SCC resolution, close human–Agent 0 work is the
primary pattern. A recurrent implementation loop presumes enough definition
to identify useful ready work; applying it too early can turn unresolved design
questions into apparent tasks. Bounded research or analysis can still be
delegated during this period. A familiar undertaking may pass through definition
quickly; there is no benefit in prolonging a phase to satisfy its name.

Once the work supports independent contributions, several managers can supervise
parallel groups of agents. Their assignments follow the coordination needs and
write boundaries of the undertaking. Package boundaries may be suitable, but
they are not the only possible division. A single coupled problem may need one
owner across several packages; several independent problems may fit within one.

Near completion, shared state and candidate integrity often favour narrower
integrations. This does not require every remaining activity to become serial.
Independent checking or documentation can proceed concurrently where their
results remain attributable to the correct candidate and shared resources are
controlled. New findings can also reveal an architectural question inside an
otherwise mature project.

The owner steers consequential phase transitions. Different areas may be in
different conditions at the same time. A graph becoming acyclic, a test passing
or a queue becoming empty is evidence to interpret, not an automatic instruction
to change the project's phase.

### Entry, recurrent practice and steering

The init prompt establishes the type of entry: discovery, architecture,
decomposition, implementation, reconciliation or release preparation. Its
steering identifies the current purpose, priorities, boundaries and relevant
state. A recurrent loop supplies reusable discovery and execution practices
where that pattern applies. The session graph supplies the actual work.

These functions can be expressed through several files or a simpler arrangement.
Their distinction matters more than a filename. Stable procedure should not
accumulate a succession of obsolete next actions; current steering should not
silently become a permanent rule. A handoff can describe the previous team's
habits without making those habits owner direction.

**Practice implication:** choose entry to suit the undertaking, verify what
already exists and explain the proposed continuation. Reuse an applicable
approved strategy; seek a new agreement when the owner asks for it or a material
change exceeds it. This passage describes the functions. It does not amend the
current projects' actual launchers or gates.

## 8. Constructing and supervising the team

Delegation assigns a bounded responsibility while preserving responsibility
for integration. The parent assesses whether a child's return meets its brief
and fits the undertaking. Completion of several child tasks does not establish
that their combined result works.

In Chirality's current role vocabulary, Agent 0 maintains alignment with the
human and coordinates the undertaking; Type 1 managers organize coupled work
and validate returns; Type 2 instances execute bounded assignments without
delegating. Agent 0 may dispatch Type 2 work directly. These are responsibility
distinctions, not a ranking of task difficulty or model intelligence. The live
[role instructions](../../AGENTS.md) govern actual execution; older thesis
descriptions of compulsory package managers and exclusive manager routing are
historical implementations, not requirements of this theory.

A manager is useful where implementation, feedback, integration and repair
require sustained coordination. A direct specialist is useful where a result
can be independently specified and checked. Adding a manager to every task can
increase translation and context costs without improving the result. Omitting
management from genuinely coupled work can leave the owner to perform integration
that the apparent delegation never assigned.

Model and reasoning allocation is a separate decision. It can reflect the
uncertainty, context demands, consequences and verification available for an
assignment. A difficult Type 2 review may need more reasoning resources than a
routine Type 1 coordination task. More capable execution does not independently
expand the assigned authority, and additional reasoning does not establish
review independence or correctness.

**Proposition P5 — delegation quality depends on assessable boundaries.**
A useful brief identifies purpose, relevant context, authority, permitted change
and the expected return. A short retained instruction may be enough for a small
read-only question. A coupled assignment may require an evolving work graph and
recorded amendments. In either case, the receiver should be able to tell what
would count as a useful contribution and what remains the parent's decision.

Parallelism also needs explicit integration ownership. Disjoint files reduce
write collisions but do not establish semantic independence. Two changes can
use separate files while disagreeing about the same interface, state transition
or user expectation. Conversely, a shared file need not prevent all concurrency
if one owner integrates agreed contributions against a known basis.

Supervision involves observing returns and intermediate findings, relaying
relevant changes, and changing an unproductive diagnosis. Repeated attempts
without new evidence are a reason to reconsider the approach. The parent need
not transmit every detail to every child; it must preserve the relationships
that can change the validity of their work.

## 9. Building, testing and integrating

Work becomes assessable through explicit outcomes. A component may satisfy its
local contract while the connected workflow fails. A browser result may leave
native behaviour unexamined. A passing test may rely on an oracle that does not
represent the intended requirement. Verification therefore needs a stated
relationship between the claim and the evidence capable of supporting it.

**Proposition P6 — connected verification exposes boundary failures.**
As soon as a meaningful user journey is operable, exercising it can reveal
relationships that isolated checks do not cover: selection and editing, busy
states, cancellation, review/application, persistence and recovery. Which
journeys matter follows the product and the change; an exhaustive suite on every
edit is not implied.

Deterministic checks are useful for properties they actually implement: hashes,
schemas, identifiers, numerical comparisons and reproducible transformations.
Their specifications and implementations can still be wrong. Agent review can
identify reasoning gaps and consequences not represented in those checks, but
the reviewer can share the author's mistakes. Fresh context, independently
derived expectations and deliberate attention to disconfirming cases support
review without guaranteeing it. Using the same model with a different instance
does not create model diversity.

Criteria protect the meaning of the evidence. Changing a test or tolerance to
obtain a pass changes the claim rather than repairing the product. If design
and criterion conflict, the conflict requires an explicit disposition under
the applicable authority, followed by evidence appropriate to the new basis.
The failed result remains part of the history.

Integration is itself work with an owner, a candidate and acceptance conditions.
Evidence must apply to the actual combined revision. Changed inputs may invalidate
some earlier checks without invalidating all of them. The appropriate response
is to assess what changed and repeat affected verification, keeping untouched
evidence attributable to its original basis.

The distinction between local completion and combined behaviour becomes more
important as concurrency grows. More completed tasks can increase the integration
burden. Throughput is consequently a project property, not simply a count of
agent outputs or active workers.

## 10. Maintaining project continuity

Continuity is the preservation of warranted project understanding across change.
It involves intent, scope, configuration, decisions, dependencies, responsibilities
and evidence. The thesis's configuration and attention arguments (§§7.3, 9.2.6)
help explain why it is a project-management discipline in its own right.

### Intent, scope and change

A project needs to remain intelligible as an undertaking even while its solution
changes. Requirements and their interpretations provide a basis for distinguishing
refinement, correction, discovery and scope change. Newly discovered work may be
necessary; its necessity still needs a relationship to the project's purpose
and authorized commitments.

Change control concerns that relationship and its consequences. It can preserve
room for engineering judgment while making consequential departures visible.
A specifically adopted choice is different from an implementation detail left
to the team. Treating every detail as fixed creates needless interventions;
treating every statement as optional destroys the accepted basis.

### Configuration and evidence

The identity of instructions, source, inputs, tools and candidate matters when
interpreting results. Evidence from a previous configuration can be relevant,
but applicability requires a reason. A newer timestamp alone neither invalidates
all older evidence nor transfers it to the new candidate.

Versioned records permit comparison and recovery. They do not automatically
record every relevant fact or enforce honest attribution. A hash establishes
byte identity; it cannot establish that the bytes accurately describe an event
or an owner's intention.

### Decision continuity and memory

The project needs to preserve the difference between what the owner directed,
what an agent interpreted, what the team implemented, what was observed and what
was accepted. Supersession should identify the part of an earlier decision that
changed. A later direction need not erase every earlier commitment.

Working memory makes the current unit actionable. Longer-term memory connects
decisions, sources and lessons across units and phases. Retrieval supports the
search for relevant records; a search result or derived index does not become
the authority for the claim. The BM25/vector and explicit graph facilities
described in the PR819 thesis addition are intended development at that source
basis, not capabilities demonstrated by this manual.

### Responsibilities and interrupted work

Continuity includes knowing who owns integration, what a child returned, what
was checked and what remains incomplete. Useful checkpoints and current graph
state permit another participant to resume from an identified basis. Incomplete
work should be identifiable without being discarded or falsely presented as
verified. An interruption can occur between the last checkpoint and the latest
edit, so a successor must inspect live state as well as the handoff.

A record supports reconstruction of understanding; it cannot guarantee an
identical mental state in another reader. A successor may notice a distinction
the previous team missed. Continuity should make such correction possible while
preserving the evidence of how the earlier position arose.

**Proposition P7 — continuity depends on provenance and interpretation as well
as storage.** Accurate reconstruction requires not just retrievable artifacts,
but reliable relationships among their identities, sources, authority and
supersession. More documentation can worsen reconstruction if it multiplies
contradictory entry points or hides the operative basis among historical copies.

### Attention and proportionality

The owner endorsed a measure framed as warranted confidence per unit of the
accountable person's attention in the [four-structure source record](../../plans/evidence/2026-09-19_owner_words_four_graph_structures.md).
It expresses a design aim here, not an already operationalized scalar metric.
Confidence without adequate grounds would not satisfy it, and reducing attention
by concealing uncertainty would defeat its purpose.

**Proposition P8 — process earns its cost by improving the work or its
assessability.** A record, check or gate is useful when it preserves a consequential
relationship, detects a relevant failure or prepares a decision. Repeatedly
copying evidence, reopening settled choices without changed grounds or requiring
approval for routine acts can consume attention without adding confidence.

Proportionality concerns the effort needed to establish the required result.
It does not permit an executor to lower a protected criterion to finish faster.
Nor does a recommendation for less ceremony establish that a particular control
is unnecessary. That question requires its own basis and the applicable authority.

## 11. Shipping and operational handover

Shipping is a distinct undertaking with a release candidate, an authorization
basis and a sequence that transforms verified source into identifiable artifacts
available to users. The pipeline can include packaging, environment-specific
checks, release notes, distribution and recovery arrangements. Its exact content
depends on the product and the obligations adopted for it.

The release candidate concentrates previously parallel work into an identified
basis. Checks and review must apply to that basis; later changes require an
assessment of what they invalidate. An authorized release can use a repeatable
pipeline, but a successful pipeline establishes only the properties its steps
actually check. Repository merge, product release, user acceptance and any
professional reliance are distinct decisions and states.

Operational handover identifies responsibility after publication: monitoring,
support, defect triage, maintenance, recovery and the basis for later changes.
Continuity makes these responsibilities intelligible; shipping carries out this
particular transition. Keeping them separate prevents continuity from becoming
a last-minute documentation task and prevents an available artifact from being
mistaken for a completed handover.

## 12. What this theory commits us to examining

The central proposition is that AI-assisted software project management
maintains coherence among composition, production dependencies, accumulated
reasons and decisions, and the attention through which these become an
understanding of the whole. The coordination pattern changes with the condition
of the undertaking. Human direction and the allocation of accountable reliance
remain explicit while bounded autonomy expands or contracts.

This account predicts useful patterns, but does not establish them by describing
them. The worked example must examine successful and unsuccessful episodes,
including ones that the four-structure account explains poorly. It must consider
alternative explanations such as task difficulty, model or harness changes,
missing tools and ordinary implementation defects.

The [prospective case method](02_worked_example_method.md) translates these
propositions into questions and possible contrary evidence. It leaves room for
the project history to revise the theory, including finding that a proposed
discipline added ceremony without improving the work.
