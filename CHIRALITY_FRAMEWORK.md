# The Chirality Framework

Chirality AI Ltd.
Date: 2026-07-23, Revision 3, Candidate for Owner Review

**A theory of professional accountability with AI agent systems.**

---

## 1. Purpose

This document defines the Chirality Framework — the theoretical foundation for the Chirality agent operating system and the professional practice it serves. It explains what knowledge means in the context of AI-assisted professional work, what architecture that meaning requires, and what remains irreducibly human.

The framework is not a total theory of agency, politics, or knowledge in every setting. It is a theory of professional accountability within knowledge work: the part of the problem concerned with what may be relied on, by whom, on what grounds, and under what commitment. It is therefore broader than the technical definition of an agent, but narrower than a complete metaphysics of human action.

The framework is referenced by the firm's governance documents, agent instruction architecture, and professional practice standard (`PROFESSIONAL_ENGINEERING.md`). It is the "why beneath the why" — the foundation on which the four-pillar design philosophy, the epistemic architecture, and the regulatory integration rest.

The framework is also practice-grounded: it was developed to explain, organize, and discipline an architecture shaped by recurrent failure modes in real deliverable work, not to claim that the architecture was derived from theory alone.

---

## 2. The Nature of Knowledge in Professional Practice

### 2.1 Knowledge Belongs to a Knower

Information is an externalizable substrate. It can be recorded, transmitted,
copied, cited, compared, and identified without being the knowledge of any
particular person. Knowledge is different in kind: it is a situated
achievement of a knower.

This framework does not require knowledge to be factive. A knower may know
wrongly, incompletely, or provisionally, and may revise what they know. That
possibility is not a defect in the definition. It is one reason professional
practice needs evidence, review, attribution, and correction. Those
mechanisms discipline knowing; they do not relocate knowledge from the
knower into an artifact.

The project's operational `Claim` and `Warrant` primitives describe
information and its grounds. They make a knower's potential basis inspectable,
but neither primitive is itself a knower and their conjunction is not a
definition of knowledge.

### 2.2 Configurational Multiplicity

Identical information may occasion different knowledge for different
knowers. It may also occasion different knowledge for the same knower in a
different context, for another purpose, or at another time. The difference
need not arise because the information changed. It can arise because knowing
is situated.

Chirality calls this **configurational multiplicity**. Schemas, taxonomies,
Knowledge Types, semantic lenses, and knowledge graphs can direct attention
and preserve useful distinctions. They are scaffolding for inquiry and
accountable work, not exhaustive state spaces that determine in advance
everything a knower may find in the information.

### 2.3 Authentication and Accountable Reliance

Professional authentication is an attributable act concerning identified
information. An accountable actor reviews a defined work product, assesses
its grounds, and binds an acceptance to the exact content or SHA, scope, and
purpose for which reliance is authorized.

Authentication therefore confers a status the unauthenticated information
does not possess: **accountable-reliance status** within that stated relation.
It does not create knowledge, make the information true, establish how
reality ultimately is, or determine what every knower must know from the
information. It records that an identified person accepts responsibility for
reliance on identified content under specified conditions.

The Appendix D conjecture describes this act as a double commitment: the
professional assesses a stance toward the work and affirms themselves as
bound to that stance. That conjecture is an interpretive aid, not the
definition of knowledge or a premise required by the architecture.

### 2.4 The Chirality of Knowledge

The framework is named for the permanent **accountability gap** between
externalizable information and accountable knowing. Information can be made
available to a knower, but no informational artifact, schema, provenance
chain, model output, or authentication record is identical with the knower's
knowing. Without a knower, information is not known as knowledge.

This is the sole primary sense in which the framework calls knowledge
*chiral*. The term marks an irreducible orientation: information can be
presented, organized, and warranted, while knowing remains situated in the
person who knows and may differ across knowers. The metaphor does not claim
geometric correspondence, and it does not make every duality in the
architecture another instance of chirality.

The accountability gap is permanent, but it is workable. The architecture
makes information, provenance, gaps, conflicts, rulings, review, and
authentication inspectable so that an accountable person can form, examine,
revise, and stand behind their knowing. Authentication records one such
accountable relation without exhausting the other knowledge that the same
information may occasion.

This permanent gap is distinct from the operational primitive `Gap`. An
operational `Gap` records a missing warrant and can be resolved. The
accountability gap cannot be closed by supplying another citation or by
improving a model; it names the non-identity between information and the
accountable knowing of a person.

### 2.5 Agency, Delegation, and Accountability

The framework uses the word *agent* in a bounded, technical sense and situates that technical sense inside a larger accountability structure.

In Chirality's runtime definition, an agent is a controlled system architecture: model, instructions, access to files, and use of tools. That definition answers an ontological question about what kind of thing is acting in the system. In regulated practice, the same agent is also one of the "others" whose work a licensed professional relies on. That answers a different question: how the outputs of that system are treated within professional responsibility.

These are not competing definitions. They operate at different levels.

- The technical definition explains what an artificial agent is and how it acts.
- The professional definition explains how its work is governed, reviewed, and relied upon.

The resulting distinction is fundamental: artificial agents have bounded operative agency, but not accountable agency. They can produce claims, attach warrants, surface gaps and conflicts, and act within constrained write scopes. They cannot accept duty of care, authenticate a work product, or assume the professional consequences of error. Humans and AI agents therefore participate in the same workflow, but not in the same mode. The difference is not merely one of capability. It is one of responsibility.

### 2.6 Teams, Project Management, and Governance

Once many agents are arranged into bounded roles, gates, dependencies, and handoffs, the system is no longer just a collection of tools. It becomes a form of project management.

This is not metaphorical. The folder structure, stable identifiers,
decomposition, lifecycle states, dependency records, gate reviews, and change
controls are the same kinds of structures that human teams use to coordinate
professional work. In Chirality, those structures are not represented in a
separate management layer; they are the filesystem itself. The project
structure and epistemic record are therefore coupled on purpose. What exists,
what is being worked on, what is claimed or warranted, what is recorded as
unresolved, and what may proceed can be inspected in the same project state.

The same is true of governance. Chirality repeatedly distinguishes normative, operative, and evaluative functions. Normative functions define rules and standards. Operative functions execute within those rules. Evaluative functions assess, audit, reconcile, and judge. This pattern is structurally analogous to the differentiation seen in political governance among rule-setting, administration, and adjudication; at civic scale, these often appear as legislative, executive, and judicial branches. The analogy is useful because the underlying problem is the same: authority, execution, and review must be related, but not collapsed into one undifferentiated power.

The claim is not that project governance and political governance are identical institutions. It is that they share a recurrent governance grammar wherever responsible action must be organized under inspectable authority.

### 2.7 What the Framework Does and Does Not Cover

The Chirality Framework is woven throughout the agent architecture because professional knowledge work cannot be separated from agency, organization, and governance. A person cannot determine what to rely on without also knowing who acted, under what constraints, through what process, and under whose authority.

But the framework does not claim to encompass the whole of human life or all possible forms of knowledge. It addresses a specific region of practice: the relation between information, situated knowing, and warranted reliance in work that carries professional consequences.

That is why the framework contains an account of agents, an account of teams, and an account of governance, yet is reducible to none of them. It is concerned with each only insofar as each bears on the possibility of accountable knowledge.

### 2.8 Normalization Table

The distinctions above can be kept compactly in view:

| Entity | Category | May produce claims | May attach or record warrants | May classify epistemic status | May issue rulings | May authenticate for reliance | Bears professional responsibility |
|---|---|---|---|---|---|---|---|
| **AI agent** | Artificial operative actor | Yes | Yes | Yes | No | No | No |
| **Licensed professional** | Accountable person under duty of care | Yes | Yes | Yes | Yes | Yes | Yes |
| **Claim** | Epistemic primitive | n/a | n/a | Receives classification | No | No | No |
| **Warrant** | Epistemic primitive | No | n/a | No | No | No | No |
| **Ruling** | Binding human decision | No | May cite grounds | n/a | Yes | No | Yes, through the responsible human who issues it |
| **Work product / deliverable** | Informational artifact | Contains claims | Contains warrants | Carries aggregate epistemic state | No | No; it is authenticated by a licensed professional | No |

---

## 3. What the Architecture Must Provide

### 3.1 The Generative Principle

Warranting requires inspectability, and inspectability must be architectural, not aspirational.

A system that recommends transparency is a guideline. A system that makes
material grounds and state structurally inspectable is a governance
framework. Every design decision in Chirality follows the practical
principle that a professional cannot responsibly authorize reliance on what
they cannot inspect. The architecture must therefore expose the information,
grounds, process, and accountable acts relevant to reliance.

### 3.2 The Four Pillars

Professional accountability requires that four questions be answered at every level where a person takes responsibility for work:

| Pillar | Question | What Must Be Inspectable |
|---|---|---|
| **Ontology** | What exists? | The entities, identifiers, state, and relationships in the work |
| **Epistemology** | What is warranted? | The claims, their evidence, their certainty status, and their gaps |
| **Praxiology** | How was the work done? | The processes, boundaries, authorities, and execution history |
| **Axiology** | What values governed? | The principles, constraints, and professional obligations that shaped decisions |

These pillars are not merely a classification scheme selected for this project. In Chirality, they form a compact and coherent structure for professional accountability, and they provide a useful evaluative lens for other systems that aim to support informed professional responsibility. Missing any one creates a specific accountability failure:

- Without ontology: the professional does not know what they are responsible for
- Without epistemology: the professional does not know what to believe
- Without praxiology: the professional does not know how the work was performed
- Without axiology: the professional does not know why the decisions were made the way they were

The pillars are complementary accountability questions, not independent
chiral structures. Each reveals a different possible failure of responsible
reliance, and their value lies in being asked together without pretending
that they exhaust what a knower may perceive in the work.

### 3.3 The Epistemic Architecture

The epistemology is the load-bearing pillar. The other three pillars are necessary — the architecture cannot function without them — but they exist in service of the epistemology. The ontology gives the epistemic architecture something to operate on. The praxiology enforces it through bounded execution and human gates. The axiology anchors it in professional responsibility.

The epistemology is load-bearing because it governs the warrant — the
inspectable ground on which a professional may decide whether to authorize
reliance.

#### 3.3.1 The Epistemic Ontology

The epistemology has its own formal domain model — six primitives that constitute the entities of the epistemic layer:

| Primitive | Definition |
|---|---|
| **Claim** | An assertion that something is the case. The atomic unit. Every non-trivial assertion produced by an agent in a governed workflow is a claim. |
| **Warrant** | The justification for believing a claim. Always extrinsic — a source citation (file, section, quote) — never intrinsic (model confidence or plausibility). |
| **Status** | The epistemic classification of a claim's certainty: FACT, ASSUMPTION, PROPOSAL, or TBD. |
| **Gap** | The explicit, positive assertion that a warrant has not been found. A gap is not the absence of information — it is an entity representing that absence, making it visible and actionable. |
| **Conflict** | Two or more claims with incompatible warrants about the same key. The existence of a conflict is itself an entity that must be resolved through a ruling. |
| **Ruling** | A human decision that resolves a gap or conflict, transforming epistemic status. Rulings are binding and recorded in versioned files. |

The relationships between primitives: a claim HAS a status; a claim MAY HAVE a warrant; a claim WITHOUT a warrant is a gap; in practice an unwarranted claim is marked `TBD` or remains an uncited `PROPOSAL`; two claims may be IN CONFLICT; a conflict REQUIRES a ruling; a ruling TRANSFORMS status.

The four statuses are interpreted as follows:

| Status | Meaning |
|---|---|
| **FACT** | A directly observed claim with citation. |
| **ASSUMPTION** | An inferential claim grounded in cited material. It is not directly stated in the source and still requires validation, but it is not an unwarranted guess. |
| **PROPOSAL** | A suggested interpretation, action, or design move that requires human decision before it becomes binding. A proposal may be cited or uncited. |
| **TBD** | An explicit placeholder for missing information or missing warrant. A TBD is a visible gap, not a silent omission. |

#### 3.3.2 The Four Enforcement Mechanisms

The epistemic ontology is enforced through four architectural mechanisms, each making a category of epistemic failure structurally detectable:

| Mechanism | What It Makes Inspectable |
|---|---|
| **Mandatory provenance** | Whether a claim has a warrant — every claim must cite its source or carry explicit `location TBD` |
| **No invention** | Whether a gap exists — missing data becomes TBD, not a plausible fabrication |
| **Conflict surfacing** | Whether claims disagree — contradictions are exposed with competing sources, not silently resolved |
| **Epistemic labeling** | How certain a claim is — every claim carries FACT, ASSUMPTION, PROPOSAL, or TBD |

The common thread is visibility. The system does not prevent epistemic
failures. Its declared controls make specified omissions and nonconformance
detectable, subject to the enforcement limits described by the operational
governance.

#### 3.3.3 The Warrant Lifecycle

Claims within a work product progress through a lifecycle that tracks their epistemic state:

```
UNWARRANTED → CITED → REVIEWED → AUTHENTICATED
```

| State | Meaning |
|---|---|
| **UNWARRANTED** | A claim exists but has no source citation. Status is TBD or uncited PROPOSAL. The professional cannot yet assess its grounding. |
| **CITED** | A claim has a source citation. Status is FACT, ASSUMPTION, or cited PROPOSAL. The evidence exists but no professional has committed to it. |
| **REVIEWED** | A professional has examined the claim, assessed its warrant, and dispositioned any findings. The inner commitment is being enacted. |
| **AUTHENTICATED** | The professional has bound themselves to the work. The double commitment is complete. The claim is part of a professionally warranted work product. |

The warrant lifecycle is interleaved with the production lifecycle of the work product. A deliverable in progress contains claims in varying warrant states. The deliverable is ready for issuance when the professional determines that the aggregate warrant state is sufficient for reliance.

Thorough review, in operational terms, is the process of auditing warrant sufficiency. The professional examines claims, checks warrants, resolves gaps and conflicts through rulings, and determines whether the aggregate state supports authentication.

Within this unchanged lifecycle, `AUTHENTICATED` is relational: an
accountable actor binds acceptance to identified content or SHA, scope, and
purpose. The status records accountable-reliance standing within that
relation; it does not itself perform the separate `ISSUED` release transition,
certify metaphysical truth, or dictate the knowledge of another knower.

### 3.4 The Fractal Property

The four pillars appear at every level of the system:

| Level | Ontology | Epistemology | Axiology | Praxiology |
|---|---|---|---|---|
| **Governance documents** | TYPES, SPEC | CONTRACT, SE Analysis | DIRECTIVE, PROFESSIONAL_ENGINEERING | DBM, agent protocols |
| **Agent instructions** | Header block, write scope | Invariants, provenance rules | Non-negotiable constraints | Protocol sections |
| **Production documents** | Datasheet | Specification | Guidance | Procedure |

This self-similarity arises because Chirality asks the same four
accountability questions at every level of abstraction. The fractal property
is the recurrence of those questions through governance documents, agent
instructions, and production documents. It is not a claim that one chiral
duality recurs at every level.

### 3.5 The Generative Relationship to Systems Engineering

Given the four-pillar commitments, classical systems engineering disciplines emerge as the principal architectural mechanisms by which those commitments are made operational in Chirality:

| Pillar Commitment | SE Disciplines That Follow |
|---|---|
| Ontology (stable, inspectable state) | Architecture and structural design; configuration management |
| Epistemology (evidence-first, auditable knowledge) | Verification and validation; formal methods; requirements traceability |
| Praxiology (bounded, gate-controlled execution) | Safety and reliability engineering; control theory |
| Axiology (non-delegable professional responsibility) | Human factors; decision authority allocation |

In Chirality, systems engineering is not incidental decoration or a post hoc compliance layer. It is the principal means by which the four-pillar commitments are made architecturally real. The SE disciplines identified here are not claimed to be the only possible implementation, but they are a coherent and defensible implementation of those commitments in this architecture.

---

## 4. What the Architecture Cannot Do

### 4.1 The Boundary

The architecture can organize information and support accountable knowing. It
cannot be the knower.

No architectural completeness — no invariant system, epistemic label, or
provenance trail — performs a person's knowing or professional commitment.
The architecture makes responsible reliance tractable: represented claim
states and grounds are inspectable; declared checks can surface operational
gaps and conflicts for a decision-maker; and approvals bind to identified
content. The professional must still interpret, judge, and decide what they
know and what reliance they will accept.

### 4.2 The Irreducible Human Element

AI agents can produce claims with warrants. They can classify epistemic
status, surface detected gaps and conflicts, generate purpose-specific
semantic structures, and audit represented claim states within their declared
scope. These mechanisms do not guarantee complete detection or exhaustive
categorization.

They cannot authenticate or assume professional responsibility. They can
occasion knowledge in a human knower, as other information can, but they do
not occupy the accountable professional role.

This boundary is not a prediction about future model capability. It concerns
the project's allocation of professional authority. The accountable actor is
an identifiable person who can accept duty of care and be held to an
attributed act. Better output does not erase the accountability gap, because
accuracy and accountability answer different questions.

The invariant K-AUTH-1 — "only humans author binding approval records" —
operationalizes that authority boundary. This framework does not enlarge or
alter the invariant.

---

## 5. The Central Distinction

Productivity tools optimize for output quality — making the agent's output better.

Professional accountability tools optimize for knowing what you can rely on
— requiring represented claim states and grounds to be inspectable so that a
competent professional can determine what reliance to accept.

Both approaches are valid and complementary. Only the second directly
supports accountable reliance: a qualified person committing to identified
information on inspectable grounds under duty of care.

The Chirality Framework provides one rigorous structural implementation of the conditions that make this act possible when the claims are produced by AI agents, organized through project-management structures, and governed under explicit authority.

---

## 6. The Axiom

To know what you know, why you know it, and why you know why.

The first clause is ontological: identify the claims. The second is epistemic: verify the warrants. The third is reflexive: ensure the accountability structure itself is inspectable — that the grounds for your warranting are themselves subject to examination.

The third clause distinguishes accountable professional reliance from knowing
considered only as a personal achievement. A professional's knowing may still
be mistaken or revised, but the grounds and attributed act can withstand
scrutiny because the chain from claim to warrant to commitment is inspectable.

---

## 7. The Closing Principle

AI can accelerate professional work. It cannot inherit professional responsibility.

The accountability gap between externalizable information and accountable
knowing is not a problem to be solved. It is the space in which a person
interprets what has been produced, assesses its grounds, and decides what
reliance to accept. Better AI may change the information available and the
work needed to assess it; it does not eliminate the knower or the accountable
relation.

The Chirality Framework holds that gap open and makes it workable — providing the architecture within which a professional can direct AI agents, review their outputs, and authenticate the result under duty of care, backed by an auditable record.

If we cannot make the grounds auditable, we cannot authorize professional
reliance on them. The architecture makes the relation auditable. The
professional knows, judges, and accepts responsibility.

---

## Document History

| Date | Revision | Description |
|------|----------|-------------|
| 2026-03-29 | 0 | Initial issue |
| 2026-04-04 | 1 | Clarified the framework's scope and its relation to agency, project management, governance, and professional knowledge work |
| 2026-04-04 | 2 | Normalized epistemic status semantics, added a compact normalization table, and aligned the warrant lifecycle with the formal ontology |
| 2026-07-23 | 3 | Reframed knowledge as a situated achievement of a knower, authentication as relational accountable-reliance status, and the accountability gap as the sole primary chirality of knowledge; operational primitives and lifecycle mechanics unchanged |
| 2026-07-23 | 4 | Added the D-GOV-20 shared-runtime boundary: one governed local daemon may execute many model-backed agent instances while authority remains role-, brief-, project-, and human-gate-defined |

### Runtime as institutional machinery

The shared Chirality runtime does not make a model authoritative. It provides
the institutional machinery that binds an executing model to a role, sealed
brief, declared tools, permissions, project boundary, evidence trail, and
acceptance gate. A model may occupy an Agent 0, Agent 1, or Agent 2 seat for a
run; the seat’s authority contract remains stable when the model changes.

One per-user daemon owns runtime state so Desktop, CLI, cloud supervisors, and
local workers cannot silently create competing sessions or permission
systems. Its machine-local state is operational rather than epistemic
authority. The relied-upon record remains inspectable in the governed project
and its Git history.
