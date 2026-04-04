# The Chirality Framework

Chirality AI Ltd.
Date: 2026-03-29, Revision 0, Issued for Use

**A theory of professional accountability with AI agent systems.**

---

## 1. Purpose

This document defines the Chirality Framework — the theoretical foundation for the Chirality agent operating system and the professional practice it serves. It establishes what knowledge means in the context of AI-assisted professional work, what architecture that meaning requires, and what remains irreducibly human.

The framework is referenced by the firm's governance documents, agent instruction architecture, and professional practice standard (`PROFESSIONAL_ENGINEERING.md`). It is the "why beneath the why" — the foundation on which the four-pillar design philosophy, the epistemic architecture, and the regulatory integration rest.

---

## 2. The Nature of Knowledge in Professional Practice

### 2.1 Knowledge as Warranted Accountability

Knowledge, in the context of professional practice, is not a property of information. It is a relationship between three elements:

- **A claim** — an assertion that something is the case
- **A warrant** — the justification for believing the claim, grounded in evidence
- **An accountable person** — a qualified professional who commits to the claim on the basis of the warrant, under duty of care

A claim without a warrant is assertion. A warrant without an accountable person is evidence. An accountable person without inspectable grounds is unsupported faith. All three must be present, and the relationship between them must be inspectable, for knowledge to exist in the sense that professional practice requires: something a competent person warrants under duty of care, backed by an auditable record.

### 2.2 The Transition from Information to Knowledge

Information becomes knowledge when an accountable professional warrants it. The transition is not computational — no amount of processing, retrieval, or verification transforms information into knowledge automatically. The transition is an act of commitment: a professional examines the claim, assesses the warrant, and accepts responsibility for the result.

This act cannot be performed by an AI system. AI agents can produce claims. They can attach warrants — source citations, provenance records, evidence chains. They can classify the epistemic status of claims. But they cannot supply the accountable person. The gap between information and knowledge is not a limitation to be engineered away. It is the space in which professional responsibility lives.

### 2.3 The Double Commitment

Professional authentication is not a single act of acceptance. It is a double commitment:

- **The inner commitment:** the professional affirms that the claims in the work product are warranted — that the evidence supports them and the epistemic status of each claim is understood.
- **The outer commitment:** the professional affirms themselves as bound to that stance — they stake their professional standing, their seal, and their personal accountability on the work.

The inner commitment is about the work. The outer commitment is about the professional's relationship to the work. Both are required. A professional who reviews claims without committing to the result has not authenticated. A professional who commits without reviewing has not warranted.

The architecture exists to make both commitments possible with integrity: the inner commitment requires that every claim's warrant state be inspectable; the outer commitment requires that the professional's act of acceptance bind to specific, identified content.

### 2.4 The Chirality of Knowledge

The framework is named for a structural property of knowledge itself.

In chemistry, chirality is the property of a molecule whose mirror image cannot be superimposed on the original. The left hand and the right hand have the same components, the same connections, the same structure — but they are irreducibly distinct.

Knowledge, in professional practice, has this property. It is composed of complementary, non-superimposable components whose pairing is constitutive:

- **Claim and warrant** are chiral. A claim asserts; a warrant justifies. They appear in the same documents, carry the same content format, and are both text — but they are structurally distinct. A claim without a warrant is assertion. A warrant without a claim is evidence. Neither is knowledge. Both are required. Neither can be derived from the other.

- **Meaning and commitment** are chiral. Meaning is given — the professional encounters it in the work. Commitment is enacted — the professional supplies it through the act of authentication. No amount of meaning produces commitment. No amount of commitment compensates for absent meaning. Both are required. Neither can be superimposed on the other.

- **Content and accountability** are chiral. The informational structure of a work product (its claims, warrants, and epistemic state) is one hand. The professional who takes responsibility for that structure is the other. They cannot be collapsed into a single thing. The content exists without the professional (as information). The professional exists without the content (as capability). Knowledge exists only when both are present and bound together.

This chirality is not a limitation to be resolved. It is the structure that makes professional knowledge possible. If claim and warrant could be collapsed, there would be no distinction between grounded and ungrounded assertions. If meaning and commitment could be derived from each other, there would be no need for a professional to decide. If content and accountability could be superimposed, there would be no space for the act of warranting.

The architecture makes both hands visible. The professional holds them together. The seal is the act that binds the chiral pair — declaring that the content has been inspected, the warrant has been assessed, and the professional takes responsibility for both.

The semantic algebra that generates the system's deliverable-level semantic structures formalizes this chirality: Matrix A (how the system is organized) and Matrix B (what adequate knowledge means) are the two non-superimposable inputs. Neither alone generates the semantic space. The algebra brings both hands together.

---

## 3. What the Architecture Must Provide

### 3.1 The Generative Principle

Warranting requires inspectability, and inspectability must be architectural, not aspirational.

A system that recommends transparency is a guideline. A system that makes opacity structurally impossible is a governance framework. The Chirality architecture is the latter. Every design decision in the system derives from this principle: if the professional cannot inspect it, they cannot warrant it; if they cannot warrant it, knowledge does not exist; therefore the architecture must make every element of the warranting act inspectable.

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

The four pillars form two chiral pairs. Ontology and epistemology are the structural pair — what exists and what is warranted about what exists. Praxiology and axiology are the action pair — how work is done and what values govern it. Each pair is internally chiral: ontology without epistemology is structure without knowledge of what the structure means; epistemology without ontology has nothing to attach warrants to. Praxiology without axiology is execution without purpose; axiology without praxiology is values without enactment. The complete framework requires both pairs, and neither pair can be superimposed on the other.

### 3.3 The Epistemic Architecture

The epistemology is the load-bearing pillar. The other three pillars are necessary — the architecture cannot function without them — but they exist in service of the epistemology. The ontology gives the epistemic architecture something to operate on. The praxiology enforces it through bounded execution and human gates. The axiology anchors it in professional responsibility.

The epistemology is load-bearing because it governs the warrant — the element that determines whether the professional's commitment is grounded or empty.

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

The relationships between primitives: a claim HAS a status; a claim MAY HAVE a warrant; a claim WITHOUT a warrant is a gap; two claims may be IN CONFLICT; a conflict REQUIRES a ruling; a ruling TRANSFORMS status.

#### 3.3.2 The Four Enforcement Mechanisms

The epistemic ontology is enforced through four architectural mechanisms, each making a category of epistemic failure structurally detectable:

| Mechanism | What It Makes Inspectable |
|---|---|
| **Mandatory provenance** | Whether a claim has a warrant — every claim must cite its source or carry explicit `location TBD` |
| **No invention** | Whether a gap exists — missing data becomes TBD, not a plausible fabrication |
| **Conflict surfacing** | Whether claims disagree — contradictions are exposed with competing sources, not silently resolved |
| **Epistemic labeling** | How certain a claim is — every claim carries FACT, ASSUMPTION, PROPOSAL, or TBD |

The common thread is visibility. The system does not prevent epistemic failures. It makes them impossible to hide.

#### 3.3.3 The Warrant Lifecycle

Claims within a work product progress through a lifecycle that tracks their epistemic state:

```
UNWARRANTED → CITED → REVIEWED → AUTHENTICATED
```

| State | Meaning |
|---|---|
| **UNWARRANTED** | A claim exists but has no source citation. Status is TBD or PROPOSAL. The professional cannot yet assess its grounding. |
| **CITED** | A claim has a source citation. Status is FACT or ASSUMPTION. The evidence exists but no professional has committed to it. |
| **REVIEWED** | A professional has examined the claim, assessed its warrant, and dispositioned any findings. The inner commitment is being enacted. |
| **AUTHENTICATED** | The professional has bound themselves to the work. The double commitment is complete. The claim is part of a professionally warranted work product. |

The warrant lifecycle is interleaved with the production lifecycle of the work product. A deliverable in progress contains claims in varying warrant states. The deliverable is ready for issuance when the professional determines that the aggregate warrant state is sufficient for reliance.

Thorough review, in operational terms, is the process of auditing warrant sufficiency. The professional examines claims, checks warrants, resolves gaps and conflicts through rulings, and determines whether the aggregate state supports authentication.

### 3.4 The Fractal Property

The four pillars appear at every level of the system:

| Level | Ontology | Epistemology | Axiology | Praxiology |
|---|---|---|---|---|
| **Governance documents** | TYPES, SPEC | CONTRACT, SE Analysis | DIRECTIVE, PROFESSIONAL_ENGINEERING | DBM, agent protocols |
| **Agent instructions** | Header block, write scope | Invariants, provenance rules | Non-negotiable constraints | Protocol sections |
| **Production documents** | Datasheet | Specification | Guidance | Procedure |

This self-similarity arises because Chirality must answer the same four accountability questions at every level of abstraction. In this architecture, the fractal property is not arbitrary repetition; it is evidence that the same accountability logic is being carried through governance documents, agent instructions, and production documents.

More precisely, the fractal property is the chirality of knowledge (§2.4) recurring at every level. Wherever knowledge exists in the system — in a deliverable, in an agent instruction, in a governance document — it is composed of complementary, non-superimposable components whose pairing is constitutive. The same chiral structure — claim and warrant, structure and value, content and accountability — appears at every level because knowledge at every level has the same structural property.

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

The architecture creates the conditions for knowledge. It cannot create knowledge.

No architectural completeness — no invariant system, no epistemic labeling, no provenance trail — can produce the professional's commitment. Facts cannot enact warranting. The double commitment — the professional standing by their own stance — is an act of a person, not a consequence of a system.

The architecture makes the act tractable: every claim's warrant state is visible, every gap is surfaced, every conflict reaches the decision-maker, every approval binds to specific content. But tractable is not automatic. The professional must still look, judge, and commit. The system ensures they can. It cannot ensure they do.

### 4.2 The Irreducible Human Element

AI agents can produce claims with warrants. They can classify epistemic status. They can surface gaps and conflicts. They can generate semantic structures that organize the categories of knowledge a deliverable should contain. They can audit the warrant state of every claim in a work product.

They cannot authenticate. They cannot take responsibility. They cannot enact the commitment that transforms information into knowledge.

This is not a current limitation of AI that future models will resolve. It is a consequence of what knowledge means in professional practice. Knowledge requires an accountable self. The self is not a capability. It is a person — identifiable, liable, and willing to be held to their warrant.

The gap between AI output and professional knowledge is structural, not technological. It cannot be closed from the AI side — not because AI is insufficiently capable, but because the gap is not on the AI side. It is the space where a person commits. Scaling does not produce accountability. Alignment does not produce accountability. Self-assessed confidence does not produce accountability. A model that never hallucinates still does not produce knowledge, because knowledge is not accurate information — it is warranted information, and warranting is an act of a person under duty of care.

The invariant K-AUTH-1 — "only humans author binding approval records" — is not a design constraint. It is an ontological claim about the nature of professional knowledge.

---

## 5. The Central Distinction

Productivity tools optimize for output quality — making the agent's output better.

Professional accountability tools optimize for knowing what you can rely on — making the epistemic status of every claim transparent, so that a competent professional can determine what to warrant.

Both approaches are valid. Both are complementary. But only the second supports the act that constitutes knowledge: a qualified person committing to a claim on inspectable grounds under duty of care.

The Chirality Framework provides one rigorous structural implementation of the conditions that make this act possible when the claims are produced by AI agents.

---

## 6. The Axiom

To know what you know, why you know it, and why you know why.

The first clause is ontological: identify the claims. The second is epistemic: verify the warrants. The third is reflexive: ensure the accountability structure itself is inspectable — that the grounds for your warranting are themselves subject to examination.

The third clause is what makes knowledge professional rather than personal. A professional does not merely know. They know in a way that can withstand scrutiny, because the entire chain — from claim to warrant to their act of commitment — is architecturally visible.

---

## 7. The Closing Principle

AI can accelerate professional work. It cannot inherit professional responsibility.

The gap between acceleration and responsibility is not a problem to be solved. It is not negative space — an absence waiting to be filled by better AI. It is the positive space in which professional responsibility lives. It is the space where a person looks at what has been produced, assesses its grounds, and commits. Without this gap, there is no space for commitment. Without commitment, there is no knowledge. The gap is what makes professional practice professional.

The Chirality Framework holds that gap open and makes it workable — providing the architecture within which a professional can direct AI agents, review their outputs, and authenticate the result under duty of care, backed by an auditable record.

If we cannot make it auditable, we cannot rely on it. If we cannot warrant it, it is not knowledge. The architecture makes it auditable. The professional makes it knowledge.

---

## Document History

| Date | Revision | Description |
|------|----------|-------------|
| 2026-03-29 | 0 | Initial issue |
