# Chapter 3 — Philosophical Framework

---

## 3.1 Introduction

This chapter presents the philosophical framework that governs the Chirality
architecture [CITE:Chirality_FRAMEWORK]. Where Chapter 4 describes what the
architecture is—its structures, mechanisms, and constraints—this chapter
explains why those structures take the form they do. The argument is that the
architecture rests on four foundational pillars, that these pillars form a
coherent basis and evaluative lens for professional engineering governance of
AI agent systems, and that one pillar—epistemology—is load-bearing in the
operational sense defined below.

The four pillars are not a taxonomy imposed after construction. They are the structural logic the architecture was built from, and they appear at every level of the system — from the governance documents that define the rules, through the agent instructions that enforce them, to the production documents that agents create for every deliverable. This self-similar property, termed the fractal property, is itself a sign of architectural coherence: the system practices what it produces.

The framework draws on established philosophical traditions. Ontology, the study of what exists, has a long history in information systems through Bunge's ontological framework as applied by Wand and Weber [CITE:Wand_Weber_ontology]. Epistemology, the study of knowledge and justification, has been operationalized in knowledge engineering through provenance models such as W3C PROV [CITE:W3C_PROV2013]. Praxiology, the study of human action and practical reasoning, finds expression in SE through workflow engineering and process modeling [CITE:INCOSE2023]. Axiology, the study of value, manifests in engineering through professional codes of ethics and standards of care [CITE:APEGA_RWO2021]. What is distinctive about Chirality is not the use of any single pillar, but the claim that all four must be addressed in any governance architecture that aims to support professional reliance, and that omitting one introduces a specific governance failure mode.

---

## 3.2 The Four Pillars

### 3.2.1 Ontology — What Exists in the System

The ontological commitment of the Chirality architecture is that project state is defined entirely through filesystem structures. Deliverable folders are nodes. Dependency rows in CSV registers are edges. Markdown files carry properties — identity (`_CONTEXT.md`), lifecycle state (`_STATUS.md`), dependency summaries (`_DEPENDENCIES.md`), source references (`_REFERENCES.md`), and working memory (`_MEMORY.md`). The entity hierarchy — packages containing deliverables in a flat, non-nested structure — stable identifiers assigned once and persistent across renames, enumerated types with canonical values, and the lifecycle state machine form the ontological layer.

This ontology is not a schema imposed on a database. It IS the filesystem. There is no separate representation, no translation layer, no synchronization discipline. The folder structure is the project structure. The file contents are the project state. A human, an agent, and a static analysis tool all observe the same structures and parse the same files.

The ontological commitment is formalized in `TYPES.md`, which defines the canonical vocabulary; `SPEC.md`, which defines the physical structures and file formats; and the structural invariants K-HIER-1 (flat package-to-deliverable hierarchy) and K-ID-1 (stable identifiers). The entity model is described in detail in Chapter 4, §4.3.

In philosophical terms, the Chirality ontology follows the principle that Bunge [CITE:Bunge_ontology] and Wand and Weber [CITE:Wand_Weber_ontology] applied to information systems: the representational model should reflect the real-world domain it serves, and every construct in the model should correspond to a thing in the domain. In Chirality, every folder corresponds to a real work item. Every dependency row corresponds to a real relationship. Every status file corresponds to a real lifecycle state. There are no constructs that exist only for system convenience.

One distinction within this ontology deserves explicit statement, because
the rest of the chapter depends on it. The filesystem carries two kinds of
record. Most records *describe* facts that exist independently of them — a
claim about a pipe's stress state is answerable to the pipe, and the record
can be wrong. Some records *constitute* the facts they carry — a ruling, an
approval, a lifecycle status. There is no fact of a deliverable being ISSUED
apart from the governed record of its issuance; for this kind of record, the
maxim that what is not in a versioned file does not exist for purposes of
reliance is not an evidentiary policy but a literal truth. The seam between
the two kinds runs exactly along the epistemic primitives of the next
section: a `Claim` is a descriptive record, answerable to the world and
warrantable; a `Ruling` is a constitutive record, an act performed in the
record itself. Keeping the two kinds distinct is what allows the
architecture to be simultaneously deflationary about institutional facts and
realist about engineering ones.

### 3.2.2 Epistemology — What Can Be Known, and How

This is the system's most distinctive and load-bearing contribution, and the section that this chapter develops most fully.

The fundamental problem of using large language models in professional
practice is not only that they produce bad outputs. It is that incorrect and
correct outputs may be indistinguishable by surface inspection alone. LLM
outputs are plausible by construction—the model optimizes for producing text
that reads as though it were written by a competent author. A well-formed
sentence with a specific numerical value and a plausible-sounding source
citation may be fabricated without a reliable surface signal. The model's
output therefore carries no intrinsic epistemic warrant. It is not
self-certifying and cannot be assumed grounded merely because it reads that
way.

Most approaches to this problem focus on improving the model: reinforcement learning from human feedback (RLHF), retrieval-augmented generation (RAG), fine-tuning on domain-specific corpora, or post-hoc factuality checking [CITE:Ji2023]. These are valuable but insufficient for professional practice. They reduce the probability of error without eliminating it, and — critically — they do not make the epistemic status of any particular claim transparent to the reviewer. A RAG-augmented model that retrieves a relevant document and generates a summary does not, by that fact alone, tell the reviewer which parts of the summary are grounded in the retrieved document and which are interpolated by the model.

Chirality takes a different approach. Rather than relying on a guarantee of
model reliability for a specific output, the architecture requires
represented claim states and grounds to be inspectable and auditable so that
a qualified professional can determine what to rely on.

Four architectural mechanisms enforce this:

**Mandatory provenance (K-PROV-1).** Every extracted or aggregated claim must
cite its source file and section reference, or carry an explicit `location
TBD` marker. A represented claim without provenance is detectable as
ungrounded. This is not a style guideline; it is a declared invariant with
specified enforcement layers. The provenance fields in `Dependencies.csv`
(`EvidenceFile`, `SourceRef`, `EvidenceQuote`) are required columns in the
schema, not optional metadata. A reviewer can trace a conforming represented
claim to its source or observe the missing source.

**No invention (K-INVENT-1).** When required information is missing, agents label it `TBD` and surface the gap as an open issue. They do not guess, default-fill, or silently infer. Missing data is a finding, not a problem to solve. This rule eliminates the most dangerous failure mode of LLM-assisted work: the generation of plausible-sounding values for quantities that are actually unknown. An engineer reviewing an agent's output will see `TBD` where information is missing, not a confident-looking number that happens to be fabricated.

**Conflict surfacing (K-CONFLICT-1).** When a conflict is detected, agents
produce a Conflict Table with the competing claims, pointers to their sources,
a proposed resolution marked as `PROPOSAL`, and a `HumanRuling = TBD` column.
The conforming path does not silently resolve contradictions; the human owns
the ruling. The declared controls are designed to route detected disagreements
to the decision-maker, without claiming that every conflict will necessarily
be found.

**Epistemic labeling.** Every non-trivial claim is classified with one of four labels: FACT (directly observed in source text with citation), ASSUMPTION (reasonable inference not directly stated, requiring validation), PROPOSAL (agent suggestion requiring human decision), or TBD (unknown, placeholder requiring resolution). These labels are defined in `TYPES.md` §10 as a specified convention across the suite; per D-GOV-08 (ruled 2026-07-01) the labeling act is assessed at audit time, bounded by K-CLAIM-1, with the warranting function carried by the citation, SHA-binding, and attribution mechanisms. The licensed professional does not need to guess whether a value is grounded or inferred — the label tells them.

Together, these four mechanisms mean that gaps in evidence are findings, not hidden failures. The system does not try to prevent hallucination — it requires provenance, making unsupported claims structurally visible. This is the architectural response to the epistemic limitation of LLMs: since the model's output carries no intrinsic warrant, the architecture imposes an extrinsic warrant requirement and makes its absence detectable.

Two additional epistemic commitments complete the architecture:

**Filesystem as single source of governed project state.** If a decision,
approval, or state change is not recorded in a versioned file, it does not
exist for purposes of governed reliance. There is no hidden memory, transient
chat context, or external database that may silently substitute for the
filesystem record. This commitment, stated in `DIRECTIVE.md` §2.1 and §2.5
and enforced by agent instruction invariants, makes the recorded epistemic
state of the project inspectable. It is a rule about authoritative project
state, not a claim that files establish metaphysical truth or exhaust what a
person may know.

**Content-addressed approval (K-AUTH-2).** Approvals bind to a specific git SHA. If the content changes after approval, the approval is void. This makes the integrity of the approval relationship mechanically verifiable — not dependent on trust or process discipline alone. The reviewer does not need to believe that the document has not changed since approval; they can verify it computationally.

#### The Ontology of the Epistemology

The epistemology itself has an ontology — the set of entities that the epistemic mechanisms operate on. Six primitives constitute this layer:

| Primitive | Definition |
|---|---|
| **Claim** | An assertion that something is the case. The atomic unit of the epistemology. Every non-trivial assertion produced by an agent in a governed workflow is a claim. |
| **Warrant** | The justification for believing a claim. Always extrinsic — a source citation (file + section + quote) — never intrinsic (model confidence or plausibility). |
| **Status** | The epistemic classification of a claim's certainty, expressed as one of the four labels: FACT, ASSUMPTION, PROPOSAL, TBD. |
| **Gap** | The explicit, positive assertion that a warrant has not been found. A gap is not the absence of information — it is an entity representing that absence, making it visible and actionable. |
| **Conflict** | Two or more claims with incompatible warrants about the same key. The existence of a conflict is itself an epistemic entity that must be resolved before the deliverable can advance. |
| **Ruling** | A human decision that resolves a gap or conflict, transforming epistemic status. Rulings are binding and recorded in versioned files. |

These primitives are not documentation constructs. They are the things that the invariants K-PROV-1, K-INVENT-1, K-CONFLICT-1, and K-AUTH-1 govern:

| Invariant | Epistemic Primitive Governed |
|---|---|
| K-PROV-1 (mandatory provenance) | Warrant — every claim must have an extrinsic warrant or explicit `location TBD` |
| K-INVENT-1 (no invention) | Gap — missing data must be represented as a gap, not filled with a fabrication |
| K-CONFLICT-1 (conflict surfacing) | Conflict — disagreements must be exposed, not silently resolved |
| K-AUTH-1 (human authority) | Ruling — only humans may author binding rulings and approval records |
| K-AUTH-2 (SHA-bound approval) | The warrant-to-content binding is mechanically verifiable |

The relationships between primitives are formal: a claim HAS a status; a claim MAY HAVE a warrant; a claim WITHOUT a warrant has status TBD or ASSUMPTION; two claims may be IN CONFLICT; a conflict REQUIRES a ruling; a ruling TRANSFORMS the status of claims. These relationships are formalized in `TYPES.md` §10.

#### The Warrant Lifecycle

The epistemic primitives give rise to a lifecycle that is distinct from, but interleaved with, the deliverable production lifecycle. Where the deliverable lifecycle (OPEN → INITIALIZED → SEMANTIC_READY → IN_PROGRESS → CHECKING → ISSUED) tracks the production state of a work product, the **warrant lifecycle** tracks the epistemic state of the claims within it:

```
UNWARRANTED → CITED → REVIEWED → AUTHENTICATED
```

| Warrant State | Meaning | Transition Mechanism |
|---|---|---|
| UNWARRANTED | Claim exists but has no source citation; status is TBD or PROPOSAL | Agent produces claim; K-INVENT-1 requires TBD marking for unknowns |
| CITED | Claim has a source citation; status is FACT or ASSUMPTION | Agent attaches provenance; K-PROV-1 enforces |
| REVIEWED | Claim has been examined by a licensed professional; findings dispositioned | REVIEW gates; human rules on findings |
| AUTHENTICATED | Claim is part of an authenticated PWP; the professional warrants it under duty of care | Authentication binds to git SHA; K-AUTH-2 enforces |

The two lifecycles are correlated but not identical. A deliverable in IN_PROGRESS contains a mixture of warranted and unwarranted claims. The transition to CHECKING requires that critical claims have been warranted — all CRITICAL findings must have non-TBD human disposition. The transition to ISSUED requires that the professional has authenticated the work: the act of declaring that the epistemic state of the claims is sufficient for reliance under professional responsibility.

The warrant lifecycle expresses thorough review (APEGA §3.1.2) operationally
as auditing warrant sufficiency. The professional examines represented
claims, checks their warrants, resolves surfaced gaps and conflicts through
rulings, and decides whether the aggregate state supports authentication. The
architecture makes represented warrant states inspectable within its declared
coverage; it does not guarantee complete claim capture.

One feature of the lifecycle should be flagged, because the uniform notation
can obscure it. The first transitions mark changes in evidential standing: a
claim gains a citation, then survives professional examination. The final
transition marks a change in normative standing: nothing about the claim's
evidence changes at authentication — what changes is that an accountable
person has bound themselves to it under duty of care. The arrow from
REVIEWED to AUTHENTICATED is therefore not one more step of the same kind
but the point where the epistemology hands off to the axiology — the
accountability gap of §3.6 traversed by an act rather than closed by
evidence. Appendix D offers an interpretive reading of this crossing — an
inner act of assessed assertion and an outer act of binding oneself to that
stance — as an analogue of, not a definition of, REVIEWED and AUTHENTICATED.

The epistemic architecture is the subject of Chapter 5, which develops the argument in full with worked examples and comparison to alternative approaches. The purpose of this section is to establish that the epistemology is a coherent philosophical commitment with its own formal ontology — not merely a collection of quality rules — and that it addresses a specific, identifiable limitation of LLM-based systems that other approaches do not address at the architectural level.

### 3.2.3 Praxiology — How Work Is Done

The praxiological commitment of the Chirality architecture is that work must be bounded, gate-controlled, and auditable. Three structural decisions implement this:

**The Agent 0/1/2 runtime hierarchy.** Standards define the rules from outside the runtime hierarchy. Agent 0 is the Supervising Architect, Agent 1 is the Manager, and Agent 2 is the Specialist. Agent 0 delegates only to Agent 1; Agent 1 delegates bounded work to Agent 2; Agent 2 does not delegate. Authority and capability do not increase through delegation, escalation flows upward, and no agent may bypass a human gate or approve professional reliance. The hierarchy is described in detail in Chapter 4, §4.5.

**Gate-controlled workflows.** Type 1 agents operate through multi-phase workflows with explicit gate questions at each phase. Each gate pauses for human confirmation. No gate may be skipped. The gate question makes the decision explicit and recorded. Type 2 agents operate in straight-through mode — they receive a structured brief, execute without mid-run human decisions, and return a structured report. The distinction between interactive and straight-through execution is a formal classification property (`AGENT_CLASS: PERSONA | TASK`) declared in every agent's header block.

**Write quarantine.** Every agent declares an explicit write scope. Tool roots — where derived outputs are written — are isolated from source truth — where human-accepted deliverables live. No agent writes outside its declared scope. This separation — declared per agent under K-WRITE-1 and checked in diff review, with deterministic path containment for bounded task writes under K-WRITE-2 — creates formal fault containment zones: under the sanctioned workflow, a Type 2 agent failure is contained away from source truth. Cross-deliverable operations (reconciliation, aggregation, closure analysis) are explicit, opt-in, and write to isolated tool roots — never to deliverable folders.

The operational model also separates the instruction root (release-managed agent operating system bundled with the application) from the working root (user-controlled project state). This ensures that the rules governing agent behavior are stable across projects and releases while execution remains fully filesystem-native.

### 3.2.4 Axiology — What the System Values

The axiological commitment of the Chirality architecture is that professional responsibility is non-negotiable, non-delegable, and architecturally enforced.

**Public welfare is the first constraint.** When tradeoffs exist between safety and commercial pressure, schedule, or convenience, safety prevails. This obligation is stated in `DIRECTIVE.md` §3.1 and operationalized in `PROFESSIONAL_ENGINEERING.md` §3.1.

**Professional responsibility is personal and non-transferable.** A licensed
professional retains decision rights for scope boundaries, governing codes
and standards, hazard and risk acceptance, conflict adjudication, and
approval for reliance. No AI system may claim to certify, approve, sign,
seal, or issue engineering work for reliance. This is enforced by K-AUTH-1.
AI agent outputs are drafts and structured assistance. A licensed
professional determines whether a completed output is a PWP and, where
required, authenticates that PWP for accountable reliance.

**Evidence is required, not plausibility.** The hierarchy of authority in technical matters — laws and regulations, codes and standards, project specifications, verified engineering analysis, professional judgment — governs all technical decisions. Agent outputs carry no professional authority. This hierarchy is stated in `DIRECTIVE.md` §3.4 and enforced through agent instruction invariants.

These values are not aspirational. They are enforced as architectural invariants (K-AUTH-1, K-AUTH-2, K-BIND-1) and as structural properties of the system (write quarantine, gate control, provenance requirements). A system that merely recommends these values would be a guideline. A system that enforces them architecturally is a governance framework. The distinction matters: guidelines can be ignored under pressure; architectural constraints resist it, because the sanctioned workflow offers no conforming path to the prohibited action and the surrounding layers — write quarantine, gate control, audit — are positioned to catch deviations (the enforcement model and its limits are stated in Chapter 8, §8.6).

A reader will notice that this pillar receives a thinner formal treatment
than the other three: the ontology has schemas, the epistemology has a
lifecycle, the praxiology has a hierarchy, while the axiology largely defers
to the professional code and the person who holds it. The thinness is
deliberate, not neglect. The axiology is the one pillar that cannot be
proceduralized without contradicting itself: a mechanized value system would
relocate commitment into the machinery, which is precisely what the
architecture exists to refuse. Its architectural expression is therefore
negative and structural — prohibitions on agent authentication, the human
gate that no automation may close — while its positive content lives where
it must: in the professional obligations of Chapter 6 and in the person who
bears them. The axiology is thin in the document because it is thick in the
knower.

---

## 3.3 The Fractal Property

The four-document kit that agents produce for every deliverable mirrors the philosophical structure of the system itself:

| Philosophical Pillar | Document Kit Instantiation |
|---|---|
| Ontology — what is this thing? | **Datasheet** — key parameters, identification, structured metadata |
| Epistemology — what must be true? how do we verify? | **Specification** — technical requirements, acceptance criteria, scope definition |
| Axiology — why these choices? what principles govern? | **Guidance** — design rationale, best practices, contextual direction |
| Praxiology — how do we execute? | **Procedure** — step-by-step workflow, sequencing, checklists |

This correspondence is not a retrospective classification. It arises because both the governance structure and the production format answer the same question: what does a professional need in order to take responsibility for work?

To take responsibility, the professional needs to know what the thing is (ontology / datasheet), what must be true about it and how that can be verified (epistemology / specification), why it was designed this way and what values governed the decisions (axiology / guidance), and how to execute, maintain, and reproduce it (praxiology / procedure). These four needs are invariant across scale: they apply whether the "thing" is a single deliverable or the entire agent system.

The governance documents follow the same structure at the system level:

| Pillar | System-Level Document |
|---|---|
| Ontology | `TYPES.md` (vocabulary, entities), `SPEC.md` (physical structures) |
| Epistemology | `CONTRACT.md` (invariants, enforcement), `SE_Design_Analysis.md` (verification) |
| Axiology | `DIRECTIVE.md` (founding intent, values), `PROFESSIONAL_ENGINEERING.md` (professional responsibility) |
| Praxiology | `DBM_Agent_Instruction_Architecture.md` (orchestration, workflows), agent PROTOCOL sections |

This self-similarity is what the thesis calls the fractal property: the same
four accountability questions are asked at the governance level, the agent
instruction level, and the production-document level. It is evidence of
architectural coherence, not recurrence of a chiral duality and not proof
that the four questions exhaust every possible knowing of the work.

---

## 3.4 The Load-Bearing Pillar

The four pillars are not equally weighted. The ontology, praxiology, and axiology exist to serve the epistemology. This claim requires formalization.

A pillar is **load-bearing** if removing it causes the system to lose its ability to support the primary use case — in this instance, professional reliance on AI-assisted work products. The test is a thought experiment: if we remove the pillar while keeping the other three, does the system still support professional authentication?

**Remove the ontology** (no stable entities, identifiers, or filesystem-native state). The epistemic controls have nothing to attach provenance to. You cannot cite the source of a claim if there is no stable identifier for the claim or the source. The system collapses.

**Remove the praxiology** (no gate-controlled workflows, no write quarantine, no type hierarchy). The epistemic controls exist as rules but cannot be enforced. An agent could bypass provenance requirements, write outside its scope, or advance a workflow without human approval. The system collapses.

**Remove the axiology** (no professional responsibility commitment, no public welfare constraint, no hierarchy of authority). The epistemic controls produce evidence, but there is no value framework that requires anyone to act on it. The evidence trail becomes a data warehouse rather than a governance mechanism. The system does not collapse mechanically, but it loses its purpose: there is no one accountable for relying on the evidence, and no constraint that requires evidence to be relied upon rather than ignored. The system ceases to serve professional practice.

**Remove the epistemology** (no mandatory provenance, no invention allowed, conflicts silently resolved, no epistemic labeling). The ontology still defines entities. The praxiology still gates workflows. The axiology still declares values. But the professional cannot determine which claims are grounded and which are fabricated. The evidence trail does not exist. The system produces outputs that look authoritative but carry no epistemic warrant. The licensed professional cannot conduct thorough review as defined in APEGA §3.1.2 because there is no evidence to review — only plausible-sounding text.

This thought experiment reveals that the epistemology is the pillar whose removal most completely defeats the purpose of the system. The other three pillars are necessary — the system cannot function without them — but they are necessary in service of the epistemology. The ontology gives the epistemic architecture something to operate on. The praxiology enforces it through gates and write quarantine. The axiology anchors it in professional responsibility.

Two senses of priority should be kept distinct here, because the axiology
case above already hints at the second. The priority this thought experiment
establishes is architectural: within the design, the other pillars serve the
epistemology, because the system's product is inspectable warrant. The
priority of the axiology is justificatory: the reason the design exists at
all — the reason inspectable warrant matters — is duty of care and the
public-welfare obligation (Chapter 6). The two orderings answer different
questions — what organizes the system, and what obligates it — and no
circularity results: the axiology motivates the epistemology from outside
the architecture, while inside the architecture everything is arranged so
that the epistemology can do its work.

The thesis-level claim, then, is:

> *Productivity tools optimize for output quality. Professional engineering tools optimize for knowing what you can rely on.*

The epistemology is what distinguishes an agent system that produces deliverables from an agent system that produces deliverables whose epistemic status is transparent and auditable. The former may be useful. The latter is suitable for professional practice.

---

## 3.5 The Pillars as the Ontology of Professional Accountability

The four pillars are situated within a higher-order accountability structure. In this thesis they are proposed as a compact and practically useful ontology for professional accountability rather than as the only possible classification scheme for every domain. At every level where accountability exists, analogous questions must be answered:

- What exists? (ontology)
- What is warranted? (epistemology)
- How was the work done? (praxiology)
- What values governed the decisions? (axiology)

Missing any one creates a specific, identifiable accountability failure:

| Missing Pillar | Accountability Failure |
|---|---|
| Ontology | The professional does not know what they are responsible for |
| Epistemology | The professional does not know what to believe |
| Praxiology | The professional does not know how the work was performed |
| Axiology | The professional does not know why the decisions were made the way they were |

This is the deeper reason the fractal property exists within Chirality. The four pillars appear at the governance level, at the agent instruction level, and at the document kit level not because the design was made to repeat itself, but because the architecture reuses the same accountability questions at each level of abstraction. The fractal property is therefore an architectural consequence of this framework rather than a proof that all accountable systems must instantiate the same structure in the same way.

This insight has a practical consequence: the four pillars serve as an evaluation framework for any governance architecture, not only Chirality's. For any system in which professionals delegate work to AI agents, one can ask: does the system define a complete ontology? does it enforce epistemic transparency? does it bound agent praxis through formal constraints? does it articulate and enforce values? A system missing any pillar has a specific, identifiable governance gap. The four pillars are not prescriptive about how each pillar should be implemented — only that each must be addressed.

---

## 3.6 The Chirality of Knowledge

The project name identifies one explanatory claim: there is a permanent
accountability gap between externalizable information and accountable
knowing. The metaphor is deliberately bounded. It does not supply a geometry
of knowledge, divide knowledge into a fixed number of parts, or make every
duality in the architecture chiral.

### 3.6.1 Information and the Knower

Information can be recorded, transmitted, copied, cited, compared, and
organized. Knowledge is a situated achievement of a knower. Without a knower,
information is not known as knowledge. The thesis does not impose the usual
factive condition that only true belief can count as knowledge: a person may
know wrongly, incompletely, or provisionally and later revise what they know.
Professional evidence and review matter partly because knowing can be
mistaken.

This position separates two questions that are easily conflated:

1. **What does a person know from the information?** This is situated in the
   knower and may differ with context, purpose, experience, and time.
2. **What reliance has an accountable actor accepted?** This is recorded by a
   scoped act bound to identified content.

Evidence and review may discipline what a person knows. Authentication
answers the second question by evidencing the actor's attributable acceptance
of reliance; it neither creates knowledge nor establishes reality as it
ultimately is.

### 3.6.2 The Accountability Gap and Operational `Gap`

The permanent **accountability gap** is the non-identity between information
and accountable knowing. No artifact, provenance chain, semantic model, or
approval record is identical with a person's knowing. More information may
change what a person knows; it does not remove the need for a knower or make
the resulting knowing universal.

The operational primitive `Gap` has a narrower meaning. It records that a
warrant has not been found for a claim. An operational `Gap` is remediable:
a source may be located, a claim revised, or a human ruling recorded. The
accountability gap is not missing evidence and cannot be closed by another
citation. Keeping the terms separate prevents a permanent feature of knowing
from being mistaken for a workflow defect.

### 3.6.3 Configurational Multiplicity

Identical information may occasion different knowledge in different knowers,
or in one knower under different contexts, purposes, or times. This thesis
calls that openness **configurational multiplicity**. The phrase does not
claim that every interpretation is equally good or that evidence is
irrelevant. It says that information underdetermines the situated knowing it
may occasion.

Chirality's schemas, Knowledge Types, semantic lenses, and knowledge graphs
are therefore scaffolding rather than exhaustive categorizations. They make
important questions and relationships inspectable, support comparison, and
focus professional review. They do not define a closed state space containing
everything any knower can perceive in the information. The semantic algebra
organizes a work product for a stated purpose; it does not legislate the
limits of knowledge.

Authentication stabilizes one accountable relation within this multiplicity.
An identifiable actor binds acceptance to identified content or SHA, scope,
and purpose. That act gives the information accountable-reliance status
within the stated relation. Another knower may know something different from
the same information, and the authenticating actor may later revise their own
knowing through a new attributable act.

### 3.6.4 Philosophical Precedents and Limits

The framework draws resources from six philosophical precedents without
claiming exact correspondence or derivation.

**Niels Bohr's complementarity** [CITE:Bohr1958] provides a precedent for
resisting the demand that every adequate account collapse into one
description. The thesis borrows only that restraint. It does not import a
physical theory into epistemology.

**Michael Polanyi's personal and tacit knowing** [CITE:Polanyi1958]
[CITE:Polanyi1966] and his later work with Harry Prosch [CITE:Polanyi1975]
support the priority of the knower, the personal contribution to knowing, and
the fiduciary character of professional commitment. Polanyi is a principal
resource for understanding why knowing cannot be exhausted by explicit
information. The framework does not claim to formalize Polanyi exactly.

**Brian Cantwell Smith's registration and answerability**
[CITE:Smith1996], together with his distinction between computational
reckoning and judgment [CITE:Smith2019], provides a principal resource for
the accountability gap. Registration is an achievement of a situated
subject, and judgment involves answerability not supplied by formal
calculation alone. The framework uses this to distinguish organized
information from the accountable act of relying on it, without treating
Smith's metaphysics as an architectural specification.

**Wilfrid Sellars' space of reasons** [CITE:Sellars1956] clarifies that
justification is not reducible to causal description. In Chirality this
supports the practical distinction between producing an output and giving
inspectable grounds for reliance. It does not place machines and humans in
mutually exclusive metaphysical realms.

**Robert Brandom's inferentialism** [CITE:Brandom1994] illuminates the
normative statuses undertaken when a person makes and defends a claim. It
helps explain why attributed commitment matters, but the project's
operational `Claim`, `Warrant`, and `Ruling` primitives are governance
constructs rather than translations of Brandom's system.

**Nishida Kitaro's account of maintained tension**
[CITE:Nishida1945] provides a precedent for relations whose difference need
not be erased through synthesis. The framework takes from Nishida the
permission to leave a constitutive gap open, not a claim that his
contradictory self-identity and this accountability account share one
structure.

Polanyi and Smith carry the principal philosophical weight: Polanyi for the
knower's personal and fiduciary involvement, Smith for situated registration,
judgment, and answerability. The other precedents sharpen particular
features. None warrants a claim of geometric refinement or exact
correspondence.

### 3.6.5 What the Chirality Metaphor Contributes

The metaphor gives the project a compact name for an orientation that cannot
be delegated away: information may be externalized, while knowing and
accountable reliance remain situated in persons. The architecture can expose
the informational substrate and record an accountable relation across the
gap. It cannot replace the knower with the record.

Polanyi's account of tacit integration gives this limit a positive structure
[CITE:Polanyi1975]. In the from–to structure of knowing, a person attends
*from* subsidiary particulars *to* a focal whole, and particulars scrutinized
in themselves lose the joint meaning they subtend. The governed record is
designed to occupy the subsidiary position: the practitioner attends from
claims, warrants, labels, and lifecycle states to the engineering reality
that remains focal. On this reading, the architecture's program of
explicitation does not compete with integrated understanding; it fails only
when the record itself becomes the focal object — a failure mode this thesis
names directly (§6.9.4, §9.2.6). Several architectural disciplines serve this
orientation: generated harness output may not claim acceptance in its own
voice (§6.8.3), and review effort is proportioned to represented uncertainty
(§5.7), so that the record remains an instrument looked through rather than
an artifact looked at.

This contribution is narrower than the earlier formulations of the
framework. `Claim` and `Warrant`, meaning and commitment, and the four
accountability pillars remain important distinctions, but they are not
independent chiral structures. The primary chirality is only the
accountability gap. The value of the metaphor is explanatory economy, not
formal precision.

### 3.6.6 Why the Gap Is Not a Synthesis Problem

The contrast with Hegelian synthesis is practical rather than a claim about
all dialectical philosophy. In professional AI governance, it would be a
mistake to treat better output as progressively eliminating the accountable
professional. Capability can reduce effort and error while leaving the
allocation of authority unchanged.

Chirality therefore optimizes for visibility and attributable reliance
across the gap, not for erasing it. This position does not deny that human and
machine activity can be deeply integrated. It denies only that integration,
accuracy, or fluency by itself transfers duty of care or makes authentication
automatic. The gap persists because information and accountable knowing are
not the same kind of status.

### 3.6.7 Engineering Regulation and Accountable Reliance

The APEGA practice standard *Relying on the Work of Others and Outsourcing*
[CITE:APEGA_RWO2021] is evidence for the practical importance of this
distinction, not proof of a metaphysical thesis. Its requirements for direct
supervision and control, thorough review, and authentication place obligations
on the professional who relies on work prepared by others. They do not make
the producer's capability a substitute for the professional's attributable
act.

Authentication, as used here, binds an accountable actor to identified
content, scope, and purpose. It confers accountable-reliance status; it does
not turn information into knowledge, guarantee correctness, or determine what
another knower must know. That interpretation preserves the governed warrant
lifecycle while locating professional responsibility where the regulatory
framework places it.

Other frameworks address supporting parts of the architecture. Bunge and
Wand and Weber [CITE:Bunge_ontology] [CITE:Wand_Weber_ontology] inform the
ontological pillar; W3C PROV [CITE:W3C_PROV2013] supplies a provenance
vocabulary; Toulmin [CITE:Toulmin1958] is a precedent for the operational
distinction between claims and warrants; and the INCOSE handbook
[CITE:INCOSE2023] supplies the systems-engineering disciplines discussed in
Chapter 7. These relationships support the architecture without multiplying
the primary chirality.

---

## 3.7 Summary

The Chirality architecture implements an explicit epistemic layer alongside
its ontology, praxiology, and axiology. Its distinctive move is to require
extrinsic warrants and make their absence visible rather than treating fluent
model output as self-certifying. Chapter 5 develops that operational account.

The framework is named for one narrower claim: externalizable information is
not identical with the situated knowing of an accountable person. That
permanent accountability gap permits configurational multiplicity—the same
information may occasion different, revisable knowledge—while authentication
records one attributable relation of accountable reliance. The metaphor adds
a memorable orientation, not a geometry or a universal theory of duality.

The fractal property is correspondingly modest. It is the recurrence of four
accountability questions across governance, agent instructions, and
production documents. Together, the four pillars provide the generative logic
of this architecture without claiming to exhaust every category through
which a knower may understand the work.
